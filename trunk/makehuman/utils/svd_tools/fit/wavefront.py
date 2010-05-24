"""
	module wavefront

	Module to parse wavefront *.obj files

	Not all functionalities are implemented yet.
	Only the most useful (for us) mesh-related commands are recognized.
	
	Author : Alexis Mignon
	email  : alexis.mignon@info.unicaen.fr
	Date   : 01/03/2010

"""

import numpy as np
from scipy.sparse import lil_matrix,lil_diags

class Mesh(object) :
	def __init__(self,vertices = None,faces = None ,uvcoords = None , uvfaces  = None, groups = None, normals = None, mtllib = None, name = ""):
		self.name = name

		if vertices is None : vertices = []
		if faces	is None : faces = []
		if uvcoords is None : uvcoords = []
		if uvfaces  is None : uvfaces = []
		if groups   is None : groups = {}
		if normals  is None : normals = []
		
		
		self.vertices = np.array(vertices,'float64')
		try :
			self.faces = np.array(faces,'int32')
		except ValueError :
			self.faces = faces
		self.uvcoords = np.array(uvcoords,'float64')
		try :
			self.uvfaces = np.array(uvfaces,'int32')
		except ValueError :
			self.uvfaces = uvfaces
		self.groups = groups
		self.normals = np.array(normals,'float64')
		self.mtllib = mtllib
		self.first_gr = {}
		self._neighbours = None
		self._adj = None
 
	def neighbours(self):
		if self._neighbours is None :
			self._compute_neighbours()
		return self._neighbours

	def _compute_neighbours(self):
		nverts = len(self.vertices)
		self._neighbours = [set() for i in xrange(nverts)]
		for i,j in self.edges() :
			self._neighbours[i].add(j)
			self._neighbours[j].add(i)
		
		for i,n in enumerate(self._neighbours) :
			self._neighbours[i] = list(n)

		self._adj = lil_matrix((nverts,nverts))
		for i,n in enumerate(self._neighbours) :
			for j in n :
				self._adj[i,j] = 1.
		

	def smooth(self,verts = None,alpha = 1.0):
		if self._adj is None : self._compute_neighbours()
		nverts = len(self.vertices)
		ns = lil_diags( [1./np.array(self._adj.sum(1)).flatten()],[0],(nverts,nverts) )
		reg = ns*self._adj*np.matrix(self.vertices)
		if verts is None :
			self.vertices = np.array((1.-alpha)*self.vertices + alpha*reg)
		else :
			self.vertices[verts] = (1.-alpha)*self.vertices[verts] + alpha*np.array(reg)[verts]

	def translate(self,translation):
		self.vertices += translation
	
	def rotate(self,*rotation):
		if len(rotation) == 1 :
			alpha,beta,gamma = rotation[0]
		else :
			alpha,beta,gamma = rotation
		self.vertices = np.dot(self.vertices,_rotXYZ(alpha,beta,gamma))

	def transform(self,transformation):
		"""
			Apply a transformation to each vertex.
			if T is the transformation matrix,
			and V the column-vector representing the coordinates
			of the vertex. Then the transformed vector V' is
			V' = T*V.
			
			transformation matrix can be 3x3 or 4x4 for homogenous
			coordinates.
		"""
		
		if transformation.shape == (3,3) :		
			self.vertices = np.dot(self.vertices,transformation.T)
		
		elif transformation.shape == (4,4) :
			vertices = np.ones( (len(self.vertices),4) )
			vertices[:,:-1] = self.vertices
			vertices = np.dot(vertices,transformation.T)
			vertices[:,:-1]/=vertices[:,-1].reshape(len(vertices),1)
			self.vertices = vertices[:,:-1]
		else : raise ValueError("Invalid shape for the transformation matrix (should be 3x3 or 4x4")

	def copy(self) :
		m = Mesh(vertices = self.vertices.copy(), faces = self.faces[:], 
				 uvcoords = self.uvcoords.copy(), uvfaces = self.uvfaces[:],
				 groups = self.groups.copy(), normals = self.normals.copy(),
				 mtllib = self.mtllib, name = self.name)
		return m
	
	

	def to_obj(self):
		out = ""
		if self.mtllib is not None :
			out+="mtllib %s\n"%self.mtllib
		if self.name != "" :
			out+="o %s\n"%self.name
		for v in self.vertices :
			out+="v %0.6f %0.6f %0.6f\n"%tuple(v)
		for vt in self.uvcoords :
			out+="vt %0.6f %0.6f\n"%tuple(vt)
		
		for gname,gr in self.groups.iteritems() :
			if gname != "all_faces" :
				out+="g %s\n"%gname
			if gr.material is not None :
				out+="usemtl %s\n"%gr.material
			for fid in gr.faces :
				if self.uvfaces is not None and len(self.uvfaces) > 0:
					f = np.array(self.faces[fid])+1
					uf = np.array(self.uvfaces[fid])+1
					out+="f "+" ".join(["%i/%i"%fv for fv in zip(f,uf)])+"\n"
				else :
					out+="f "+" ".join(map(str,np.array(self.faces[fid])+1))+"\n"
		return out

	def save(self,filename):
		with open(filename,'w') as f :
			f.write(self.to_obj()+"\n")
	
	def edges(self):
		edges = []
		for f in self.faces :
			edges.append((f[-1],f[0]))
			for i in xrange(len(f)-1):
				edges.append((f[i],f[i+1]))
		# sort vertices in edges
		edges = map(lambda (x,y) : (x,y) if x<=y else (y,x),edges)
		edges = list(set(edges))
		edges.sort()
		return edges
 



class Group(object) :
	 def __init__(self,name,faces = None,material = None):
		 self.name = name
		 if faces is None : faces = []
		 self.faces = faces
		 self.material = material


def read_obj(filename):
	"""
		Read an *.obj file and returns the corresponding objects.
	"""
	group_name = None
	group = None
	object_name = None
	object = None
	object_type = None
	mtllib = None
	nobjects = 0
	objects = []
	face_id = 0
	with open(filename) as f :
		for line in f.readlines() :
			if line.startswith('o '): # New object
				# Save the previous one if any
				if object is not None :
					objects.append(object_type(**object))
				object_name = line.split()[1]
				object = None
				object_type = None
			if   line.startswith('v '): # New vertex
				if object is None :
					object_type = Mesh
					object = {}
					if object_name is not None : # if a name was given
						object['name'] = object_name
					else :
						object['name'] = ''
					object['mtllib'] = None
					object['vertices'] = []
					object['faces'] = []
					object['uvcoords'] = []
					object['uvfaces']  = []
					object['groups']   = {}
					object['normals']  = []
				if mtllib is not None :
					object['mtllib'] = mtllib
					mtllib = None
				object['vertices'].append(map(float,line.split()[1:]))
				
			elif line.startswith('vt '):  # texture vertex
				object['uvcoords'].append(map(float,line.split()[1:]))
				
			elif line.startswith('vn '):  # vertex normal
				object['normals'].append(map(float,line.split()[1:]))
				
			elif line.startswith('f '):   # face
				indices = line.split()[1:]
				if len(indices) < 3 : continue
				if line.find('//')!=-1 : # we also have uv faces information
					coords = [ map(lambda x : int(x) -1 ,i.split('//')) for i in indices ]
					object['faces'].append( [ c[0] for c in coords ] )
					object['uvfaces'].append( [c[1] for c in coords ] )
				elif line.find('/')!=-1 :
					coords = [ map(lambda x : int(x) -1,i.split('/')) for i in indices ]
					object['faces'].append( [ c[0] for c in coords ] )
					object['uvfaces'].append( [c[1] for c in coords ] )					
				else :
					object['faces'].append( map(lambda x : int(x) -1,line.split()[1:]) )

				if group is not None : group.faces.append(face_id)
				face_id += 1
	
			elif line.startswith('g ') : # new group
				group_name = line.split()[1]
				group = Group(name = group_name)
				object['groups'][group_name] = group
				
			elif line.startswith('usemtl ') : # material for the group
				if group is None :			 # no group is defined
					group_name = 'all_faces'   # so the material is for the all object
					group = Group(name = group_name)
					object['groups'][group_name] = group
				group.material = line.split()[1]

			elif line.startswith('mtllib '): # the material file to use
				mtllib = line.split()[1]

	if object is not None :
		objects.append(object_type(**object))
	if len(objects) == 1 : return objects[0]
	else : return objects

def _rot_matrix_X(alpha):
	return np.array([[1.,0.			,0.],
					 [0.,np.cos(alpha) ,np.sin(alpha)],
					 [0.,-np.sin(alpha),np.cos(alpha)]])

def _rot_matrix_Y(beta):
	return np.array([[np.cos(beta), 0. , np.sin(beta) ],
					 [ 0.		  , 1. , 0.		   ],
					 [ -np.sin(beta), 0. , np.cos(beta) ]])

def _rot_matrix_Z(gamma):
	return np.array([[ np.cos(gamma), np.sin(gamma), 0.],
					 [-np.sin(gamma), np.cos(gamma), 0.],
					 [0.			, 0.		   , 1.]])


def _rotXYZ(alpha,beta,gamma):
	Rx = _rot_matrix_X(alpha)
	Ry = _rot_matrix_Y(beta)
	Rz = _rot_matrix_Z(gamma)
	
	return np.dot(Rz,np.dot(Ry,Rx))
