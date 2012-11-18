
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

    def get_co(self):
        return list(self.object.coord[self.idx])

    def set_co(self, co):
        self.object.coord[self.idx] = co

    co = property(get_co, set_co)

    def get_no(self):
        return list(self.object.vnorm[self.idx])

    def set_no(self, no):
        self.object.vnorm[self.idx] = no

    no = property(get_no, set_no)

    def get_color(self):
        return list(self.object.color[self.idx])

    def set_color(self, color):
        self.object.color[self.idx] = color

    color = property(get_color, set_color)

    class FaceList(list):
        def __init__(self, callback, it):
            self.__callback = callback
            super(FaceList, self).__init__(it)

        def append(self, value):
            super(FaceList, self).append(value)
            self.__callback(self)

    def get_faces(self):
        faces = self.object.vface[self.idx,:self.object.nfaces]
        return self.FaceList(self.set_faces, [FaceProxy(self.object, idx) for idx in faces])

    def set_faces(self, faces):
        self.object.vface[self.idx,...] = [face.idx for face in faces]
        self.object.nfaces[self.idx] = len(faces)

    sharedFaces = property(get_faces, set_faces)

    def setCoordinates(self, co):
        """
        Replaces the coordinates.
        
        :param co: The coordinates for this face.
        :type co: [float, float, float]
        """
        self.co = co
        self.update(False, True, False)
        
    def setNormal(self, no):
        """
        Replaces the normal.
        
        :param no: The normal for this face.
        :type no: [float, float, float]
        """
        self.no = no
        self.update(True, False, False)
    
    def setColor(self, color):
        """
        Replaces the color.
        
        :param no: The color for this face.
        :type no: [byte, byte, byte, byte]
        """
        self.color = color
        self.update(False, False, True)

    def update(self, updateNor=True, updateCoo=True, updateCol=False):
        """
        This method updates the coordinates, normal and/or color of a vertex in the C
        OpenGL world, based upon the values currently held in the Python Vert class.

        The vertex indexing system in the Python code differs from the
        OpenGL vertex indexing system used in the C code, as discussed in the description
        of this *Vert* class (see above).

          - In Python, a single vertex can be shared by multiple faces. In OpenGL, there
            are always multiple copies of any such vertex.

        Because one Python Vert object can appear multiple times in the C vertex list,
        each Python Vert object has an attribute, *__indicesInFullVertArray*, which lists
        the conceptual 'index' in the C lists of coordinates and colors.

        From this 'conceptual' index, we can find where the vertex's coordinates lie in the full C
        coordinate list. Because each vertex has three coordinates (x, y, and z), the
        coordinate list will be three times as long as this 'conceptual' index. So, a vertex
        listed in the *__indicesInFullVertArray* at positions 1 and 4 (the second and fifth
        positions) will have its coordinates listed on the C coordinates list at
        positions 3, 4, and 5, and again at positions 12, 13, and 14. Or:

          (n*3), (n*3)+1, (n*3)+2   for both n = 1 and n = 4.

        The C color list is similar to the coordinate list. As each color is defined by
        four components 'red, green, blue, and alpha (transparency)' the C color list is
        four times as long as this 'conceptual' index. So, a vertex listed in the
        *__indicesInFullVertArray* at positions 1 and 4 will have its color component values listed in the C
        color list at positions 4, 5, 6, and 7, and again at positions 16, 17, 18, and
        19. Or:

          (n*4), (n*4)+1, (n*4)+2, (n*4)+3   for both n = 1 and n = 4.

        The color passed into this method can originate from various sources, depending upon what the
        color is to represent at this moment in time. Colors can be manipulated to indicate 
        faces or vertices that have been selected, to indicate morph target strengths at different 
        locations on the model or control or to show base colors.
        
        When updating the color information, this method usually sets all vertex colors in the C array
        that were derived from a single Python Vert object to be the same color.

        :param updateNor: Whether the normal needs to be updated.
        :type updateNor: Boolean
        :param updateCoo: Whether the coordinates needs to be updated.
        :type updateCoo: Boolean
        :param updateCol: Whether the color needs to be updated.
        :type updateCol: Boolean
        """
        
        if not self.object.object3d:
            return

        self.object.markCoords(self.idx, updateCoo, updateNor, updateCol)

    def calcNorm(self):
        """
        This method calculates the vertex surface normal based upon a mathematical average
        of the physical normals of all faces sharing this vertex. This results in a smooth surface.

        .. image:: _static/vert_norm.png

        The physical normal of a surface is a direction vector at right angles
        to that surface. Although the triangular mesh consists of a series of flat
        faces, the surface normal calculated for a vertex averages out the
        physical normals of the faces that share that vertex, enabling the
        rendering engine (OpenGL) to shade the object so that the surface looks
        like a single, smooth shape.

        Because the actual 3D engine uses optimized glDrawElements,
        where each vertex can have only one normal, it is impossible
        in MakeHuman to draw the geometry in a \"flat\" mode.

        MakeHuman is organically oriented, so the benefits of using this optimized technique
        outweigh potential performance costs.

        """

        self.object.calcVertexNormals([ix])

    def vertsShared(self):
        """
        This method returns a list of the vertices of all faces that share this vertex.

        .. image:: _static/vert_shared.png

        If processing the vector V in the image above this function would return [v1,v2,v3,v4,v5,v6,v7]

        """

        faces = self.object.vface[self.idx,:self.object.nfaces[self.idx]]
        verts = self.object.fvert[faces]
        return [VertProxy(self.object, v) for v in set(verts.flat)]

    def __str__(self):

        return 'vert num %s, coord(%s,%s,%s)' % (self.idx, self.co[0], self.co[1], self.co[2])

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

    def get_no(self):
        return tuple(self.object.fnorm[self.idx])

    def set_no(self, no):
        self.object.fnorm[self.idx] = no

    no = property(get_no, set_no)

    def get_verts(self):
        verts = self.object.fvert[self.idx]
        return [VertProxy(self.object, idx) for idx in verts]

    def set_verts(self):
        self.object.fvert[self.idx,...] = [vert.idx for vert in verts]
        for v in verts:
            self.object.coord[v.idx,:] = v.co
            self.object.vnorm[v.idx,:] = v.no
            self.object.color[v.idx,:] = v.color
            self.object.vface[v.idx,:] = [f.idx for f in v.sharedFaces]
            self.object.nfaces[v.idx] = len(v.sharedFaces)

    verts = property(get_verts, set_verts)

    def get_uv(self):
        return list(self.object.fuvs[self.idx])

    def set_uv(self, uvs):
        self.object.fuvs[self.idx] = uvs

    uv = property(get_uv, set_uv)

    def get_group(self):
        return self.object._faceGroups[self.idx]

    group = property(get_group)

    def isTriangle(self):
        return (self.verts[0].idx == self.verts[3].idx)
 
    def setColor(self, color):
        """
        Sets the color for this face.
        
        :param color: The color in rgba.
        :type: [byte, byte, byte, byte]
        """
        self.color = [color for v in self.object.fvert[self.idx]]
        self.updateColors()

    def calcNormal(self):
        """
        This method calculates the physical surface normal of the face using the :py:func:`aljabr.planeNorm` function from
        the aljabr module. This results in a direction vector at right angles to the
        two edges vt2_vt1 and vt2_vt3.
        """

        self.object.calcFaceNormals([self.idx])

    def updateColors(self):
        """
        This method updates the color attributes for each vertex on this face.
        """

        self.object.color[self.object.fvert[self.idx]] = self.color

    def __str__(self):

        return 'face %i: verts: %s' % (self.idx, [v.idx for v in self.verts])

class ListProxy(object):
    def __init__(self, object):
        self._object = object

class VertsProxy(ListProxy):
    def __len__(self):
        return len(self._object.coord)

    def __getitem__(self, idx):
        return VertProxy(self._object, idx)

    def __iter__(self):
        for idx in xrange(len(self)):
            yield VertProxy(self._object, idx)

class FacesProxy(ListProxy):
    def __len__(self):
        return len(self._object.fnorm)

    def __getitem__(self, idx):
        return FaceProxy(self._object, idx)

    def __iter__(self):
        for idx in xrange(len(self)):
            yield FaceProxy(self._object, idx)
