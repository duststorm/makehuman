from scipy.linalg import pinv,svd
import numpy as np


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
	u,s,vt = svd(targets.T)
	return u.T[s>=rcond*s[0]]

def project_target(base,target):
	"""
		Rebuild 'target' as a combinaison of 'targets' using 'base'.
		t' = base^T * base * t
		
		arguments :
		- base : projection base as given by 'compute_base'
	"""
	if not isinstance(target,np.ndarray) :
		target = np.array(target)
	try :
		nverts,dim = target.shape
		target = target.reshape(nverts*dim)
		return np.dot(np.dot(target,base.T),base).reshape(nverts,dim)
	except ValueError :
		ntargs,nverts,dim = target.shape
		target = target.reshape(ntargs,nverts*dim)
		return np.dot(np.dot(target,base.T),base).reshape(ntargs,nverts,dim)
