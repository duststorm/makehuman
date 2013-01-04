"""===========================  ===============================================================
Project Name:                **MakeHuman**
Module File Location:        utils/maketarget/svdprojection.py
Product Home Page:           http://www.makehuman.org/
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/
Authors:                     Alexis Mignon
Copyright(c):                MakeHuman Team 2001-2013
Licensing:                   AGPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
===========================  ===============================================================

This module provides core functionalities to use target bases built using
SVD.

For each base, two files are provided, one suffixed with "_base.dat"
containing the base itself and one suffixed with "_vertices.dat"
containing the indices of the vertices used to build the base.

"""

def _mat_mult_vector(m,v):
    """ Multiplies matrix m by vector v
		
		args : 
			- m : a list of list considered as a matrix
			- v : a list considered as a column vector
	
		returns :
			- a list corresponding to the elements of the column vecor
			  given by: v' = m*v
    """
    dim1 = len(m)
    dim2 = len(m[0])
    if len(v) != dim2 : raise ValueError("Matrix and vector shapes mismatch : (%i x %i) and %i"%(dim1,dim2,len(v)))
    
    res = [0]*dim1
    for i in xrange(dim1):
        for j in xrange(dim2):
                res[i] += m[i][j]*v[j]
    return res
    
def _mat_trans_mult_vector(m,v):
    """ Multiplies the transpose of matrix m by vector v
		
		args : 
			- m : a list of list considered as a matrix
			- v : a list considered as a column vector
	
		returns :
			- a list corresponding to the elements of the column vecor
			  given by: v' = m^T*v
	"""
    dim1 = len(m)
    dim2 = len(m[0])
    if len(v) != dim1 : raise ValueError("Matrix and vector shapes mismatch : (%i x %i) and %i"%(dim2,dim1,len(v)))
    
    res = [0]*dim2
    for i in xrange(dim2):
        for j in xrange(dim1):
                res[i] += m[j][i]*v[j]
    return res

def read_vertex_list(list_file):
    """ read_vertex_list(list_file) -> vertex list 
		
		Reads a list of vertices from a file.
	"""
    f = open(list_file)
    vlist = [int(i) for i in f.readlines()]
    f.close()
    return vlist,_build_lookup_dict(vlist)


def read_target_base(base_file):
    """ 
		read_target_base(base_file) -> base matrix
		
		Reads a base from a file and return the corresponding matrix as
	    a list of lists
	"""
    f = open(base_file)

    while True  :
        l = f.readline()
        if not l.startswith("%") : # if not a comment
            output_dim,input_dim = [int(v) for v in l.split()]
            base = [[0]*input_dim for i in xrange(output_dim)]
            break
    for j in xrange(input_dim):
        for i in xrange(output_dim):
            base[i][j] = float(f.readline())
    f.close()
    return base

def load_base(base_file):
    """
        Loads both base and vertex_list.
        
        args :
            - base_file : can be either the name of the base file
                  or the common prefix to base and vertex file.
        returns :
            - the target base
            - the list of vertex indices
            - the lookup table associating vertex indices to target
              indices
    """
    if not base_file.lower().endswith("_base.dat") :
        base_file += "_base.dat"
    base = read_target_base(base_file)
    vlist,lookup = read_vertex_list(base_file.replace("_base","_vertices"))
    return base,vlist,lookup

def _build_lookup_dict(idx_list):
    lookup_dict = {}
    for i in xrange(len(idx_list)):
        lookup_dict[idx_list[i]]=i
    return lookup_dict



def apply_projection(base,target):
    """ apply_projection(base,target) -> projected target
        
        Project a target on the base.
        
        args :
            - base : the projection base. It is a matrix d x D given 
                     as a list of list, where D is the input dimension
                     an d the output dimension.
                     The lines of the matrix represents the vectors of the
                     base.
                     
            - target : the target to project. it is given as a list of floats
                     representing the coordinate of the target in input space.
                     
        returns :
            - the projected target given with the same format as the input target.
    
    """
    proj = _mat_mult_vector(base,target)
    return _mat_trans_mult_vector(base,proj)

