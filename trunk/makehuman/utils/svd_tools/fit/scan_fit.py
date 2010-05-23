from scipy.linalg import pinv,svd
from scipy.spatial import KDTree
import numpy as np
import os

def find_transform(mask_scan,mask_mh):
	"""
		Computes the transformation to align mask_scan
		and mask_mh.
		
		mask_scan' = scale * R * mask_scan + T
		
		arguments :
			mask_scan, mask_mh : 2D arrays where each row contains
			          the 3D coordinate of a vertex. Vertices in
			          mask_scan and mask_mh are assumed to be in the
			          same order.
			          
		returns :
			(scale,R,T)
			scale : the scaling factor.
			R : the rotation matrix
			T : the translation
			
	"""
	mask_scan = np.array(mask_scan)
	mask_mh = np.array(mask_mh)
	
	# compute barycenters
	mscan = mask_scan.mean(0)
	mmh = mask_mh.mean(0)

	# compute mean distance to barycenter
	sscan = np.sqrt(((mask_scan - mscan)**2).sum(1)).mean()
	smh =   np.sqrt(((mask_mh - mmh)**2).sum(1)).mean()

	scale = smh/sscan

	# Put both meshes barycenter to origin

	mask_scan -= mscan
	mask_mh -= mmh
	
	# rescale  mask_scan
	mask_scan *= scale

	# find rotation matrix
	# Let X be the vertices coordinates (one vertex per row) and we apply
	# a rotation R :   X' = X*R^T
	#              X^T*X' = X^T*X*R^T 
    #      (X^T*X)*X.^T*X' = R^T
    #                 R^T = X^+ * X'
    # where X^+ stands for the pseudo invert of X'

	R = np.dot(pinv(mask_scan),mask_mh).T
    
	# We want to have x' = scale * R * x +  T
	# What we have is
	#                 x' = scale * R * (x - c) + c'
	# where c and c' are the barycenters of mask_scan
	# and mask_mh respectively.
	#                 x' = scale * R * x - scale*R*c + c'
	# hence :         T = c' - scale * R * c
	
	T = mmh - scale * np.dot(mscan,R.T)
	return scale,R,T

def apply_transform(scale,R,T,points):
	"""
		Apply the transformation 
		x' = scale*R*x + T
		for each point in points (one point per row).
	"""
	return scale*np.dot(points,R.T) + T

def align_scan(mask_scan,mask_mh,scan):
	"""
		Align 'scan' using mask_scan and mask_mh.
		
		mask_scan, mask_mh, and scan are 2D arrays
		with one 3d point per row
	"""
	scale,R,T = find_transform(mask_scan,mask_mh)
	return apply_transform(scale,R,T,scan)

def compute_base(targets,rcond = None):
	"""
		Compute the projection base to project a new target on
		the base of known targets.
		
		arguments :
			- targets : a list of targets. each target is given
			as a 2D array with one 3D vertex per raw.
			- rcond : cut-off on singular values. Singular values
			  smaller than rcond*greatest-singular-value are considered
			  as zero.
			  
		returns the projection base B so that B*target give the coefficient
		of the targets to use.
		
		NB : the rcond value [0,1] allows to control the precision of the
		projection base. Value 1 will give a higher precision. Smaller
		values will 'smooth' the result.
	"""

	targets = np.array(targets)
	ntargs,nverts,dim = targets.shape
	targets = targets.reshape(ntargs,nverts*dim)
	u,s,vt = svd(targets.T,full_matrices = False)
	if rcond is not None :
		select = s>=rcond*s[0]
		return u[:,select],s,vt[select]
	else :
		return u,s,vt

def compute_coefs(u,s,vt,target):
	"""
	
	
	"""
	size,ns = u.shape
	nt = vt.shape[1]
	
	if not isinstance(target,np.ndarray) :
		target = np.array(target)
	try :
		nverts,dim = target.shape
		target = target.reshape(size)
		return np.dot(np.dot(target,u*s[ns]),nt)
	except ValueError :
		ntargs,nverts,dim = target.shape
		target = target.reshape(ntargs,size)
		return np.dot(np.dot(target,u),u.T).reshape(ntargs,nt)
 

def project_target(u,target):
	"""
		Rebuild 'target' as a combinaison of 'targets' using 'u'.
		t' = u* u.T * t
		
		arguments :
		- u : projection base as given by 'compute_base'
		- target : target to fit
	"""

	if not isinstance(target,np.ndarray) :
		target = np.array(target)
	if target.ndim == 2 :
		nverts,dim = target.shape
		target = target.reshape(nverts*dim)
		return np.dot(np.dot(target,u),u.T).reshape(nverts,dim)
	else :
		ntargs,nverts,dim = target.shape
		target = target.reshape(ntargs,nverts*dim)
		return np.dot(np.dot(target,u),u.T).reshape(ntargs,nverts,dim)

def find_match(mask,mesh):
	kd = KDTree(mesh)
	return kd.query(mask)

def load_target(filename):
	t = {}
	with open(filename) as f:
		for line in f :
			sp = line.split()
			i = int(sp[0])
			coords = map(float,sp[1:])
			t[i] = coords
	return t

def load_targets(dirname):
	files = os.listdir(dirname)
	files.sort()
	targets = []
	vertices = set()
	for f in files :
		t = load_target(dirname+"/"+f)
		targets.append(t)
		vertices |= set(t.keys())
		
	return [os.path.splitext(f)[1] for f in files],list(vertices),targets

def build_matrix(vert_list,targets):
	look_up = {}
	for i,v in enumerate(vert_list) :
		look_up[v] = i
	base = np.zeros((len(targets),len(vert_list),3))
	for i,t in enumerate(targets):
		for v,coords in t.iteritems() :
			base[i,look_up[v]]=coords
	return base,look_up

def fine_fit(head_mesh,scan_mesh,prefix,head_verts,niter,alpha = 0.2):
	import sys
	verts = np.loadtxt(prefix+".verts",'int')
	
	kd = KDTree(scan_mesh.vertices)
	dist,indx = kd.query(head_mesh.vertices[verts])
	print "init...",
	sys.stdout.flush()
	# initial fit
	target = scan_mesh.vertices[indx] - head_mesh.vertices[verts]
	u = np.load(prefix+"_u.npy")
	proj = project_target(u,target)

	m = head_mesh.copy()
	m.vertices[verts] += proj
	print "final...",
	sys.stdout.flush()
	# finalize fit
	verts = np.loadtxt(head_verts,'int')
	
	for i in xrange(niter) :
		dist,indx = kd.query(m.vertices[verts])
		m.vertices[verts] = scan_mesh.vertices[indx]
		m.smooth(verts)
	
	return dict(zip(verts,(m.vertices - head_mesh.vertices)[verts]))

if __name__ == '__main__' :
	import sys
	
	cmd = sys.argv[1]
	
	if cmd == 'build' :
		try : 
			target_dir = sys.argv[2]
			mask_verts_file = sys.argv[3]
			output = sys.argv[4]
			print "Read targets...",
			sys.stdout.flush()
			names,head_verts,targets = load_targets(target_dir)
			mask_verts = np.loadtxt(mask_verts_file)
			print "OK"
			print "Build bases...",
			sys.stdout.flush()
			targs,lup = build_matrix(head_verts,targets)
			base = compute_base(targs)
			print "OK"
			
			with open(output+".names","w") as f :
				f.write("\n".join(names)+"\n")
			
			np.savetxt(output+".verts",head_verts,"%i")
			np.save(output+"_base.npy",targets)
			np.save(output+"_u.npy",base[0])
			np.save(output+"_s.npy",base[1])
			np.save(output+"_vt.npy",base[2])
		except IndexError :
			print "usage : python scan_fit.py build target_dir mask_verts output_prefix"
	elif cmd == 'fit' :
		import wavefront as wf
		try :
			head_mesh = sys.argv[2]
			head_mask = sys.argv[3]
			scan_mesh = sys.argv[4]
			scan_mask = sys.argv[5]
			fit_verts = sys.argv[6]
			prefix = sys.argv[7]
			output = sys.argv[8]
		except IndexError :
			print "usage : python scan_fit.py fit head_mesh head_mask scan_mesh scan_mesh fit_verts prefix output_obj"
			sys.exit(-1)

		head_mesh = wf.read_obj(head_mesh)
		head_mask = wf.read_obj(head_mask)
		scan_mask = wf.read_obj(scan_mask)
		scan_mesh = wf.read_obj(scan_mesh)
		
		print "Align masks...",
		sys.stdout.flush()
		scan_mesh.vertices = align_scan(scan_mask.vertices,head_mask.vertices,scan_mesh.vertices)
		print "OK"
		
		# finalize fit
		print "fit...",		
		sys.stdout.flush()			
		target = fine_fit(head_mesh,scan_mesh,prefix,fit_verts,2,alpha = 0.2)
		
		print "OK"

		with open(output,'w') as f :
			for v,c in target.iteritems():
				if np.abs(c).max()>=1e-6 :
					f.write( "%i %s\n"%(v," ".join(["%0.6f"%cc for cc in c]) ) )

			
	else :
		print "usage : python scan_fit.py build|project args"
