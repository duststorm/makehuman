#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

class VertProxy(object):

    """
    A vertex object. This object holds the 3D location and surface normal
    of the vertex and an RGBA color value. It also has references to
    other related data structures.

    Vertex information from this object is passed into the OpenGL 3D
    engine via the C code in *glmodule.c*, which uses the glDrawArray
    OpenGL function to draw objects.

    A single Python Vert object is used for all of the faces within a 
    given face group that share that same vertex. This is why the uv coordinates
    are stored in the Face object instead. This way one vertex might have more
    than one uv coordinate pair depending on the face. It is similar to using an
    uv layer.
    
    However, the OpenGL code considers a vertex shared by multiple faces with different
    uv to be different vertices. So, a Vert object that appears once on the Python
    vertex list may appear multiple times on the C vertex list.

    For example: Two faces share the edge 'v2-v3'. One face is defined by
    vertices v1, v2 and v3, and the other face is defined by vertices
    v3, v2, and v4. The Python vertex list could contain four vertices:

      [v1,v2,v3,v4]

    However, the C vertex list will repeat vertices that are shared by more
    than one face in the faces do not belong to the same group. So, the C
    vertex list will be based on the list:

      [v1,v2,v3,v4]
      
      or
      
      [v1,v2,v3,v3,v2,v4]

    Each Python Vert object contains a list attribute, *__indicesInFullVertArray*,
    listing the various locations where the vertex appears in the C vertex list.
    This allows information held against a single Vert object in Python to be
    copied to multiple locations in the coordinate and color lists in the
    C-based OpenGL world.
    
    .. py:attribute:: co
    
        The coordinates of the vertex. [float, float, float]
        
    .. py:attribute:: no
    
        The normal of this vertex. [float, float, float]
        
    .. py:attribute:: object
    
        The object of which this vertex is a part. :py:class:`module3d.Object3D`
        
    .. py:attribute:: sharedFaces
    
        The list of faces that share this vertex. [:py:class:`module3d.Face`, ..]
        
    .. py:attribute:: idx
    
        The index of this vertex in the vertices list. int
        
    .. py:attribute:: color
    
        The color of the vertex in rgba. [byte, byte, byte, byte]
    
    :param co: The coordinates for this face.
    :type co: [float, float, float]
    :param idx: The index in the mesh for this face.
    :type idx: int
    :param object: The object which will own this face.
    :type object: :py:class:`module3d.Object3d`
    """

    def __init__(self, object, idx):
        self.idx = idx
        self.object = object

    @property
    def co(self):
        return tuple(self.object.coord[self.idx])

    @property
    def no(self):
        return tuple(self.object.vnorm[self.idx])

    @property
    def color(self):
        return tuple(self.object.color[self.idx])

    @property
    def sharedFaces(self):
        faces = self.object.vface[self.idx,:self.object.nfaces[self.idx]]
        return IndexedFacesProxy(self.object, faces)

    def vertsShared(self):
        """
        This method returns a list of the vertices of all faces that share this vertex.

        .. image:: _static/vert_shared.png

        If processing the vector V in the image above this function would return [v1,v2,v3,v4,v5,v6,v7]

        """

        faces = self.object.vface[self.idx,:self.object.nfaces[self.idx]]
        verts = self.object.fvert[faces]
        return IndexedVertsProxy(self.object, list(set(verts.flat)))

    def __str__(self):

        return 'vert num %s, coord(%s,%s,%s)' % (self.idx, self.co[0], self.co[1], self.co[2])

    def __eq__(self, other):
        return self.object is other.object and self.idx == other.idx

class FaceProxy(object):

    """
    An object representing a point, line, triangle or quad.
    
    .. py:attribute:: no
        
        The normal of the face. [float, float, float]
        
    .. py:attribute:: verts
    
        A list of vertices that represent the corners of this face. [:py:class:`module3d.Vert`, ..]
        
    .. py:attribute:: idx
    
        The index of this face in the list of faces. int
        
    .. py:attribute:: group
    
        The face group that is the parent of this face. :py:class:`module3d.FaceGroup`
        
    .. py:attribute:: color
    
        A list of rgba colors, one for each vertex. [[byte, byte, byte, byte], ..]
        
    .. py:attribute:: uv
    
        A list of indices to uv coordinates, one for each vertex. [int, ..]
      
    :param verts: The vertices for this face.
    :type: :py:class:`module3d.Vert`, ..
    """

    def __init__(self, object, idx):
        self.object = object
        self.idx = idx
        self.color = None

    @property
    def no(self):
        return tuple(self.object.fnorm[self.idx])

    @property
    def verts(self):
        verts = self.object.fvert[self.idx]
        return IndexedVertsProxy(self.object, verts)

    @property
    def uv(self):
        uvs = self.object.fuvs[self.idx]
        return IndexedUVsProxy(self.object, uvs)

    @property
    def group(self):
        return self.object._faceGroups[self.object.group[self.idx]]

    def isTriangle(self):
        return (self.verts[0].idx == self.verts[3].idx)

    def __str__(self):

        return 'face %i: verts: %s' % (self.idx, [v.idx for v in self.verts])

class ListProxy(object):
    def __init__(self, object):
        self._object = object

    def __iter__(self):
        for idx in xrange(len(self)):
            yield self[idx]

class VertsProxy(ListProxy):
    def __len__(self):
        return len(self._object.coord)

    def __getitem__(self, idx):
        return VertProxy(self._object, idx)

class FacesProxy(ListProxy):
    def __len__(self):
        return len(self._object.fnorm)

    def __getitem__(self, idx):
        return FaceProxy(self._object, idx)

class IndexedProxy(ListProxy):
    def __init__(self, object, indices):
        super(IndexedProxy, self).__init__(object)
        self._indices = indices

    def __len__(self):
        return len(self._indices)

    def __getitem__(self, idx):
        raise NotImplementedError

class IndexedVertsProxy(IndexedProxy):
    def __getitem__(self, idx):
        return VertProxy(self._object, self._indices[idx])

class IndexedFacesProxy(IndexedProxy):
    def __getitem__(self, idx):
        return FaceProxy(self._object, self._indices[idx])

class IndexedUVsProxy(IndexedProxy):
    def __getitem__(self, idx):
        return tuple(self._object.texco[self._indices[idx]])

class MaterialsProxy(object):
    def __init__(self, object):
        self._object = object

    def __len__(self):
        return len(self._object.fmtls)

    def __getitem__(self, idx):
        return self._object._materials[self._object.fmtls[idx]]

    def __iter__(self):
        for idx in xrange(len(self)):
            yield self[idx]

    def __contains__(self, idx):
        return idx >= 0 and idx < len(self)

    def iterkeys(self):
        return xrange(len(self))

    def itervalues(self):
        for idx in xrange(len(self)):
            yield self[idx]

    def iteritems(self):
        for idx in xrange(len(self)):
            yield idx, self[idx]

    def keys(self):
        return range(len(self))

    def values(self):
        return [self[idx] for idx in xrange(len(self))]

    def items(self):
        return [(idx, self[idx]) for idx in xrange(len(self))]
