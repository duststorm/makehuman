import os
from scipy import array,matrix,zeros
from scipy.io import mmwrite

def load_targets(directory,vertices,lookup):
	""" Load all targets from a directory and returns an array
	    of size (ntargets,3*nvertices).
	"""
	files = [f for f in os.listdir(directory) if f.lower().endswith(".target")]
	files.sort()
	ntargets = len(files)
	nvertices = len(vertices)
	print ntargets, "target files found !"
	raw_base = zeros((ntargets,nvertices,3))
	itarg = 0
	target_names = [os.path.splitext(f)[0] for f in files]
	for fname in files :
		f = open(directory+'/'+fname,'r')
		for line in f.readlines() :
			lsplit = line.split()
			vert = int(lsplit[0])
			if vert not in vertices : continue
			raw_base[itarg,lookup[vert]] = array([float(v) for v in lsplit[1:]])
		f.close()
		itarg+=1
	return raw_base.reshape((ntargets,nvertices*3)),target_names

def _build_diag(d):
    N = len(d)
    try :
        from scipy.sparse import dia_matrix
        return dia_matrix((d,0),shape = (N,N))
    except ImportError :
        from scipy.sparse import spdiags
        from scipy import array
        return spdiags(array(d).reshape((1,N)),0, N,N )

        

def make_base(raw_base,cut_off=1e-10):
	""" Compute the orthonormal projection base from the target raw
	    base. 
		Singular values lower than 'cut_off' are considered as null.
	"""
	from scipy.linalg import eigh
	#from scipy.sparse import dia_matrix
	from numpy import sqrt
	mrb = matrix(raw_base)
	w,u = eigh(mrb*mrb.T)
	mmwrite("singular_values",w.reshape((len(w),1)) )
	range = (w<cut_off).sum()
	ww = zeros(len(w)-range)
	ww = 1.0/sqrt(w[range:])
	dim = u.shape[0]-range
	W = _build_diag(ww)
	print "Rank: ",dim
	base = W*u.T[range:,:]*mrb
	back = u[:,range:]*W*base
	return base,back

def read_vertices(list_file):
    f = open(list_file)
    vertices = [int(v) for v in f.readlines()]
    f.close()
    lookup = {}
    for i in xrange(len(vertices)):
        lookup[vertices[i]] = i
    return vertices,lookup

if __name__ == '__main__' :
	import sys
	
	try :
		directory = sys.argv[1]
		list_file = sys.argv[2]
	except IndexError :
		print "usage: python buildbase.py <target_directory> <verts file with _vertices suffix> [<cut off>]"
                print "example: python buildbase.py targetsdb head_vertices.dat 2"
		sys.exit(-1)
		
	try : cutoff = float(sys.argv[3])
	except IndexError : cutoff = 1.0e-10
	
	base_file = list_file.replace("_vertices","_base")
	vertices,lookup  = read_vertices(list_file)

	print "Loading targets..."
	rb,target_names = load_targets(directory,vertices,lookup)
	print "Making base..."
	base,back = make_base(rb,cutoff)
	del rb
	print "Saving base..."
	f = open(base_file,'w')
	mmwrite(f,base)
	f.close()
	del base
