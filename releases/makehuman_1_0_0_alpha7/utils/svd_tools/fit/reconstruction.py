##
#
# Author : Alexis Mignon
# email : alexis.mignon@gmail.com
# Date : 24/03/2010
###

"""
	Reconstruction of a target given a target base using
	constrainted regularized least-square.
	
	We first compute the Singular Value Decomposition
	of the target base to project the problem in a lower dimensional
	space. Then we minimze the distance between the fit result
	and the target under constrained that target coefficients
	must have their values between 0 and 1.
	
	if 'A' is the target base, 'x' the coefficient vector we are looking
	for and b the target to reconstruct, we have the following
	optimisation problem.
	
	minimize || A*x - b ||
	s.t. x>=0 and x<=1
	
	where ||.|| stands for the L2-norm (euclidean norm)
	
	Optionnaly we compute the L1-regularized version of this problem :
	minimize || A*x - b || + r * |x|
	s.t. x>=0 and x<=1
	
	where |.| stands for the L1-norm and 'r' is a parameter that
	controls the importance of the regularisation.
	
"""
from mh_utils import *
from scipy.linalg import svd
from scipy import save,load,dot
from cvxmod import optvar,param,norm2,norm1,problem,matrix,minimize

def compute_matrices(base,prefix):
	"""
		Computes and saves the matrices from the Singular Value
		Decomposition (SVD) of the target base :
		A = U*S*V^t
		
		The suffixes "_U.npy", "_S.npy", "_S.npy"
		are added to the prefix.
	"""
	if base.ndim == 3 :
		ntargets,nvertices,dim = base.shape
		base = base.reshape(ntargets,nvertices*3)
	else :
		ntargets,nvertices = base.shape
		nvertices/=3
	U,S,Vt = svd(base.T,full_matrices = False, overwrite_a = True)
	#We keep only significant singular values
	Scum = S.cumsum()/S.sum()
	save(prefix+'_U',U[:,Scum<1.])
	save(prefix+'_S',S) # we still save the full singular values just in case...
	save(prefix+'_V',Vt.T[:,Scum<1.])

def reconstruct_target(target_file,base_prefix,regul = None):
	"""
		Reconstruct the target in 'target_file' using constrained, 
		and optionally regularized, least square optimisation.
		
		arguments :
			target_file : file contaiing the target to fit
			base_prefix : prefix for the files of the base.
	"""
	
	vlist = read_vertex_list(base_prefix+'_vertices.dat')
	t = read_target(target_file,vlist)
	U = load(base_prefix+"_U.npy").astype('float')
	S = load(base_prefix+"_S.npy").astype('float')
	V = load(base_prefix+"_V.npy").astype('float')

	ntargets,dim = V.shape
	nvert = len(t)
	pt = dot(U.T,t.reshape(nvert*3,1))
	pbase = S[:dim].reshape(dim,1)*V.T
	A = param('A',value = matrix(pbase))
	b = param('b',value = matrix(pt))
	x = optvar('x',ntargets)

	if regul is None : prob = problem(minimize(norm2(A*x-b)),[x>=0.,x<=1.])
	else : prob = problem(minimize(norm2(A*x-b) + regul * norm1(x)),[x>=0.,x<=1.])
	
	prob.solve()
	
	targ_names_file = base_prefix+"_names.txt"
	with open(targ_names_file) as f :
		tnames = [line.strip() for line in f.readlines() ]
	tnames.sort()
	
	base,ext = os.path.splitext(target_file)
	bs_name = base+".bs"
	with open(bs_name,"w") as f :
		for tn,v in zip(tnames,x.value):
			if v >= 1e-3 : f.write("%s %0.3f\n"%(tn,v))

def usage():
	import sys
	print """usage : $ python reconstruction.py command args
		
Possible commands are :
	- build :
		$ python reconstruction.py build target_dir base_prefix [vertex_list]
		
		- target_dir : directory with base targets
		- base_prefix : prefix that will be added to all the file names created
		- vertex_list : list of vertex to limit the base to a given set of vertices
		(not implemented yet)
		
		Given a base_prefix 'prefix', the following files will be created :
		- prefix_names.txt : the names of the targets in the base (used to 
		     build the body setting files)
			 
		- prefix_U.pny,
		  prefix_S.pny,
		  prefix_V.pny : The matrices of the SVD in numpy format.
		
	- fit :
		$ python reconstruction.py fit target_file base_prefix [regularisation]
		
		- target_file : target to fit
		- base_prefix : prefix added to all the file names of the base
		- regularisation : controls the sparsity of the result
			it corresponds to the 'r' variable in the function
			we minimize : ||A*x-b|| + r*|x|
			where ||.|| corresponds to the L2-norm
			and |.| corresponds to the L1-norm.

	"""
	sys.exit(-1)
	
if __name__ == "__main__" :
	import sys
	try :
		command = sys.argv[1]
	except IndexError : usage()
	if command == "build" :
		try :
			dir = sys.argv[2]
			prefix = sys.argv[3]
		except IndexError : usage()
		
		print "Loading targets..."
		base,names = load_targets(dir)
		
		with open(prefix+"_names.txt","w") as f :
			f.write("%s\n"%"\n".join(names))
		print "Computing matrices..."
		compute_matrices(base,prefix)
	elif command == "fit":
		try :
			target_file = sys.argv[2]
			base_prefix = sys.argv[3]
			try :
				regul = float(sys.argv[4])
			except IndexError :
				regul = None
		except IndexError : usage()
		
		reconstruct_target(target_file,base_prefix,regul)
	else : usage()
		
		
