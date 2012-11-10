import os
import numpy as np
NVERTICES = 14638

def lookup(vertices_list):
	return dict([(vertices_list[i],i) for i in xrange(len(vertices))])

def read_target(target,vertices_list = None, look_up = None ):
	if vertices_list is None :
		nvert = NVERTICES
		vertices = range(nvert)
		if look_up is None : look_up = range(nvert)
	else :
		nvert = len(vertices_list)
		if look_up is None : look_up = lookup(vertices_list)
		
	t = np.zeros((nvert,3),'float32')
	with open(target) as f :
		for line in f.readlines():
			values = line.split()
			ivert = int(values[0])
			t[look_up[ivert]] = np.array(map(float,values[1:]),'float32')
	return t

def load_targets(target_files,vertices_list=None):
	"""
		Loads a list of targets either from a directory
		either given as a list of file names.
	
		a vertex_list can be given so only the vertices in the base
		will be used.
		
		returns :
			- the set of targets as a 3 D array with dimensions corresponding
			to target,vertex,coordinates
			- the list of target names as used in a body setting file
	"""
	if vertices_list is None :
		nvert = NVERTICES
		vertices_list = range(NVERTICES)
		look_up = range(nvert)
	else :
		nvert = len(vertices_list)
		look_up = lookup(vertices_list)
	
	try :	
		target_files.sort()
	except AttributeError : # target_files is a directory
		target_files = [target_files+"/"+f for f in os.listdir(target_files)]
		target_files.sort()

	ntargets = len(target_files)
	base = np.zeros((ntargets,nvert,3),'float32')
	for i,tfile in enumerate(target_files) :
		base[i] = read_target(tfile,vertices_list,look_up)
	return base, [ os.path.splitext(os.path.basename(t))[0] for t in target_files]

def read_vertex_list(filename):
	try :
		with open(filename) as f :
			vl = map(int,f.readlines())
	except IOError :
		vl = None
	return vl
