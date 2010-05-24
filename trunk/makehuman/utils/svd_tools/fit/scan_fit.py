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


class TargetBase(object):
	"""
		Object used to manage target projection bases.
		
		important attributes are :
		- names : list of target names. This can be used for creating
		          the combinaison of targets to use (boddy setting files)
		- vert_list : the vertices that will be used. 
		- targets : the targets as a 3D array (ntargets,nvertices,3)
		- prefix  : prefix used to load or save the different components
		            of the base.
	
	"""
	def __init__(self,names = None,vert_list=None,targets=None,prefix = None):
		self._names = names
		self._vert_list = vert_list
		self._targets = None if targets is None else np.array(targets)

		if targets is None :
			self._u = self._s = self._vt = None
		else :
			print "Computing svd decomposition..."
			ntargs,nverts,dim = targets.shape
			targets = targets.reshape(ntargs,nverts*dim)
			self._u,self._s,self._vt = svd(targets.T,full_matrices = False)
			print "OK"

		self.prefix = prefix

	@property
	def u(self):
		if self._u is None and self.prefix is not None :
			self._u  = np.load(prefix+"_u.npy")
		return self._u

	@property
	def s(self):
		if self._s is None and self.prefix is not None :
			self._s  = np.load(prefix+"_s.npy")
		return self._s

	@property
	def vt(self):
		if self._vt is None and self.prefix is not None :
			self._vt  = np.load(prefix+"_vt.npy")
		return self._vt

	@property
	def vert_list(self):
		if self._vert_list is None and self.prefix is not None :
			try :
				self._vert_list  = np.loadtxt(prefix+".verts",'int')
			except IOError : pass
		return self._vert_list
	
	@property
	def targets(self):
		if self._targets is None and self.prefix is not None :
			self._targets  = np.load(prefix+"_targets.npy")
		return self._targets

	@property
	def names(self):
		if self._names is None and self.prefix is not None :
			with open(prefix+".names","r") as f :
				self._names = [ l.strip() for l in f]
		return self._names

	def save(self,prefix = None):
		if prefix is not None : self.prefix = prefix

		with open(prefix+".names","w") as f :
			f.write("\n".join(self.names)+"\n")
		
		if self.vert_list is not None : np.savetxt(prefix+".verts",self.vert_list,"%i")
		np.save(prefix+"_targets.npy",self.targets)
		np.save(prefix+"_u.npy",self.u)
		np.save(prefix+"_s.npy",self.s)
		np.save(prefix+"_vt.npy",self.vt)

	def project_target(self,target,rcond = 0.0):
		"""
			Rebuild 'target' as a combinaison of 'targets' using 'u'.
			t' = u* u.T * t
			
			arguments :
			- target : target to fit
			- rcond : cut off on the singular values as a fraction of
			          the biggest one. Only base vectors corresponding
			          to singular values bigger than rcond*largest_singular_value
		"""
		
		u = self.u[ : , self.s>= rcond*self.s[0]]
		
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
			
	def compute_combinaison(self,target,rcond = 0.0):
		"""
			Computes the combination of base targets allowing to reproduce
			'target' (or giving the best approximation).
			
			arguments :
			- target : target to fit
			- rcond : cut off on the singular values as a fraction of
			          the biggest one. Only base vectors corresponding
			          to singular values bigger than rcond*largest_singular_value
			
		"""
		cond = self.s>= rcond*self.s[0]
		u = self.u[ : , cond ]
		vt = self.vt[ cond ]
		s = self.s[cond]
		
		return np.dot(np.dot(target,u),vt*1./s)
		
	def compute_combinaison_safe(self,target,rcond = 0.0,regul = None):
		"""
			Computes the combination of base targets allowing to reproduce
			'target' (or giving the best approximation), while keeping
			coefficients between 0 and 1.

			arguments :
			- target : target to fit
			- rcond : cut off on the singular values as a fraction of
			          the biggest one. Only base vectors corresponding
			          to singular values bigger than rcond*largest_singular_value
			          
			- regul : regularisation factor for least square fitting. This force
			          the algorithm to use fewer targets.
			
		"""
		from cvxmod import optvar,param,norm2,norm1,problem,matrix,minimize
		if type(target) is str or type(target) is unicode :
			target = read_target(target)
		cond = self.s>= rcond*self.s[0]
		u = self.u[ : , cond ]
		vt = self.vt[ cond ]
		s = self.s[cond]
		
		t = target.flatten()
		dim,ntargets = self.vt.shape
		nvert = target.shape[0]
		
		pt = np.dot(u.T,t.reshape(nvert*3,1))
		A = param('A',value = matrix(s.reshape(dim,1)*vt))
		b = param('b',value = matrix(pt))
		x = optvar('x',ntargets)

		if regul is None : prob = problem(minimize(norm2(A*x-b)),[x>=0.,x<=1.])
		else : prob = problem(minimize(norm2(A*x-b) + regul * norm1(x)),[x>=0.,x<=1.])
		
		prob.solve()
		bs = np.array(x.value).flatten()
		# Body setting files have a precision of at most 1.e-3
		return bs*(bs>=1e-3)
		
	
	def combine_targets(self,coefs):
		return (self.targets*coefs).sum(0)

def select(choice,subchoice):
	lup = dict([(v,i) for i,v in enumerate(choices)])
	return [lup[c] for c in subchoice]

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
	for f in files:
		t = load_target(dirname+"/"+f)
		targets.append(t)
		vertices |= set(t.keys())
		
	return [os.path.splitext(f)[1] for f in files],list(vertices),targets

def build_matrix(vert_list,targets):
	look_up = dict([(v,i) for i,v in enumerate(vert_list)])
	base = np.zeros((len(targets),len(vert_list),3))
	for i,t in enumerate(targets):
		for v,coords in t.iteritems() :
			base[i,look_up[v]]=coords
	return base

def fine_fit(head_mesh,scan_mesh,prefix,tofit_verts,niter,alpha = 0.2,rcond = 0.0,constrained = False,regul = None):
	import sys
	
	tofit_verts = np.loadtxt(tofit_verts,'int')
	base = TargetBase(prefix = prefix)
	verts = base.vert_list
	ntargs = len(base.targets)
	print "init...",
	sys.stdout.flush()
	# initial fit
	
	m = head_mesh.copy()
	nverts = len(scan_mesh.vertices)
	
	kd = KDTree(scan_mesh.vertices)
	
	for i in xrange(niter) :
		dist,indx = kd.query(m.vertices[tofit_verts])

		target = np.zeros((nverts,3))
		target[tofit_verts] = scan_mesh.vertices[indx] - m.vertices[tofit_verts]
		target = target[verts]
		if constrained :
			coefs = base.compute_combinaison_safe(target,rcond,regul = regul)
			proj = (coefs.reshape(ntargs,1,1)*base.targets).sum(0)
		proj = base.project_target(target)

		m.vertices[verts] += proj

		if alpha> 0.0 :
			m.vertices[tofit_verts] = scan_mesh.vertices[indx]
			m.smooth(tofit_verts,alpha = alpha)
	
	return dict(zip(verts,(m.vertices - head_mesh.vertices)[verts]))

def save_target(filename,target):
	with open(filename,'w') as f :
		for v,c in target.iteritems():
			if np.abs(c).max()>=1e-6 :
				f.write( "%i %s\n"%(v," ".join(["%0.6f"%cc for cc in c]) ) )		

if __name__ == '__main__' :
	import sys
	
	try :
		cmd = sys.argv[1]
	except IndexError :
		print "usage : python scan_fit.py build|project args"
		sys.exit(-1)
	
	if cmd == 'build' :
		try : 
			target_dir = sys.argv[2]
			output = sys.argv[3]

		except IndexError :
			print "usage : python scan_fit.py build target_dir output_prefix"
			sys.exit(-1)

		print "Read targets...",
		sys.stdout.flush()
		names,head_verts,targets = load_targets(target_dir)
		print "OK"
		
		print "Build bases...",
		sys.stdout.flush()
		
		targs = build_matrix(head_verts,targets)
		base = TargetBase(names,head_verts,targs)
		
		print "OK"
		base.save(output)

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
			print "usage : python scan_fit.py fit head_mesh head_mask scan_mesh scan_mask fit_verts prefix output_target"
			sys.exit(-1)

		head_mesh = wf.read_obj(head_mesh)
		head_mask = wf.read_obj(head_mask)
		scan_mask = wf.read_obj(scan_mask)
		scan_mesh = wf.read_obj(scan_mesh)
		
		print "Align masks...",
		sys.stdout.flush()
		scan_mesh.vertices = align_scan(scan_mask.vertices,head_mask.vertices,scan_mesh.vertices)
		print "OK"
		
		# fit
		print "fit...",		
		sys.stdout.flush()
					
		target = fine_fit(head_mesh,scan_mesh,prefix,fit_verts,1,alpha = 0.0,rcond = 0.0,constrained = True)
		print "OK"

		save_target(output,target)
	else :
		print "usage : python scan_fit.py build|project args"
