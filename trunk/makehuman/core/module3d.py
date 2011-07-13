#!/usr/bin/python
# -*- coding: utf-8 -*-

# You may use, modify and redistribute this module under the terms of the GNU GPL.
# .. include:: docs/includes/example1.txt

"""
Base 3D MakeHuman classes.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module contains all of the base classes needed to manage the 3D MakeHuman
data structures at runtime. This includes the data structures themselves as well
as methods to handle their manipulation in memory. For example, the Vert class
defines the data structures to hold information about mesh vertices objects,
while the Face class defines data structures to hold information about mesh face
objects.

These base classes implement a nested hierarchical structure for the objects
that make up the scene that is shown to the user. For example, a FaceGroup
object contains groups of mesh face objects as defined by the Face class. An
Object3D object contains all of the FaceGroup objects that go to make up a
particular discrete object, such as the humanoid body or one of the GUI
controls. The Scene3D object contains all of the Object3D objects that go
to make up the entire scene.

"""

__docformat__ = 'restructuredtext'

import mh
import aljabr
import time
from types import *
import os
from fastmath import vnorm3d

textureCache = {}


class Texture(mh.Texture):

    """
    A simple handler for textures loaded in the scene.
    
    Attributes
    ----------
    
    - **self.id** : *int* The texture identifier.
    - **self.modified**: *int* A flag to indicate if a texture is modified, used to reload the texture if needed.
    """

    def __init__(self):
        mh.Texture.__init__(self)
        self.modified = None
        
def getTexture(path, cache=None):

    texture = None
    cache = cache or textureCache
    
    if path in cache:
        
        texture = cache[path]
        
        if os.stat(path).st_mtime != texture.modified:
            
            print 'reloading ' + path
            
            try:
                texture.loadImage(path)
            except RuntimeError, text:
                print text
                return
            else:
                texture.modified = os.stat(path).st_mtime
    else:
        
        try:
            texture = Texture()
            texture.loadImage(path)
            #texture.loadSubImage('data/themes/default/images/slider_focused.png', 0, 0)
        except RuntimeError, text:
            print text
        else:
            texture.modified = os.stat(path).st_mtime
            cache[path] = texture
            
    return texture

class Vert:

    """
    A 3D vertex object. This object records the 3D location and surface normal
    of the vertex and an RGBA color value. It also records references to
    other related data objects.

    Vertex information from this object is passed into the OpenGL 3D
    engine via the C code in *glmodule.c*, which uses the glDrawArray
    OpenGL function to draw objects.

    A single Python Vert object is usually used for all of the faces within a 
    given face group that share that same vertex. The exception to this is 
    where the UV-data used to define the object (as read in from an obj file) 
    used more than one UV-index for the same vertex index, in which case a 
    copy of the vertex exists for each unique UV-index. You can therefore get
    multiple (not usually more than 2) Python Vert objects sharing the same 
    coordinates, but different UV-mapping data, color etc.
    
    However, the OpenGL code considers a vertex shared by multiple faces to
    be multiple vertices. So, a Vert object that appears once on the Python
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

    In addition, the C vertex list is actually an expanded coordinate list,
    containing each coordinate of each vertex (x, y, and z) in one long list
    (stored as a one dimensional array):

      [v1x,v1y,v1z,v2x,v2y,v2z,v3x,v3y,v3z,v3x,v3y,v3z,v2x,v2y,v2z,v4x,v4y,v4z]

    Similarly, the four color components (r, g, b, and a) of each vertex are
    stored in the C vertex color list.

    Each Python Vert object contains a list attribute, *indicesInFullVertArray*,
    listing the various locations where the vertex appears in the C vertex list.
    This allows information held against a single Vert object in Python to be
    copied to multiple locations in the coordinate and color lists in the
    C-based OpenGL world. See the description of the *update* method, below,
    for more detail about how the information in the Python-based Vert class is
    translated to the lists used by OpenGL.

    Basic usage:
    ------------

    ::

        import module3d

        x,y,z = 1,1,1
        v = module3d.Vert([x,y,z])
        v.update()
        
    Attributes
    ----------
    
    - **self.co**: *float list*. The coordinates of the vertex.
      Default: [coX, coY, coZ]).
    - **self.no**: *float list*. The normal of this vertex (or 0).
      Default: [0, 0, 0].
    - **self.object**: *Object3d*. The object of which this vertex is a part.
      Default: None
    - **self.sharedFaces**: *faces list*. The list of faces that share this vertex.
    - **self.indicesInFullVertArray**: *Int list*. The list of corresponding vertices in the C OpenGL list.
    - **self.idx**: *Int* The index of this vertex in the vertices list.
    - **self.color**: *float list*. A list of 4 floats [r,g,b,a] used as the vertex color (including an alpha channel).
    """

    def __init__(self, co=[0, 0, 0], idx=0, object=None):
        """
        This is the constructor method for the Vert class. It initializes the
        vert attributes.



        Parameters
        ----------

        coX:
            *float*. The x coordinate of the vertex. Default is 0.

        coY:
            *float*. The y coordinate of the vertex. Default is 0.

        coZ:
            *float*. The z coordinate of the vertex. Default is 0.

        idx:
            *int*. The index of this vertex in the vertices list. Default is 0.

        object:
            *Object3d*. The Object3D object that uses this vertex. Default is None.

        """

        self.co = co
        self.no = [0, 0, 0]
        self.object = object
        self.sharedFaces = []
        self.indicesInFullVertArray = []
        self.idx = idx
        self.color = [255, 255, 255, 255]
    
    def setCoordinates(self, co):
        self.co = co
        self.update(False, True, False)
        
    def setNormal(self, no):
        self.no = no
        self.update(True, False, False)
    
    def setColor(self, color):
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
          - Vertex information is expanded, so the x, y and z coordinates
            that are stored for a vertex in the Vert class take up 3 times as many
            positions in the OpenGL coordinate list (and rgba color values
            take 4 times as many index positions).

        Because one Python Vert object can appear multiple times in the C vertex list,
        each Python Vert object has an attribute, *indicesInFullVertArray*, which lists
        the conceptual 'index' in the C lists of coordinates and colors.

        From this 'conceptual' index, we can find where the vertex's coordinates lie in the full C
        coordinate list. Because each vertex has three coordinates (x, y, and z), the
        coordinate list will be three times as long as this 'conceptual' index. So, a vertex
        listed in the *indicesInFullVertArray* at positions 1 and 4 (the second and fifth
        positions) will have its coordinates listed on the C coordinates list at
        positions 3, 4, and 5, and again at positions 12, 13, and 14. Or:

          (n*3), (n*3)+1, (n*3)+2   for both n = 1 and n = 4.

        The C color list is similar to the coordinate list. As each color is defined by
        four components 'red, green, blue, and alpha (transparency)' the C color list is
        four times as long as this 'conceptual' index. So, a vertex listed in the
        *indicesInFullVertArray* at positions 1 and 4 will have its color component values listed in the C
        color list at positions 4, 5, 6, and 7, and again at positions 16, 17, 18, and
        19. Or:

          (n*4), (n*4)+1, (n*4)+2, (n*4)+3   for both n = 1 and n = 4.

        The color passed into this method can originate from various sources, depending upon what the
        color is to represent at this moment in time. Colors can be manipulated to indicate 
        faces or vertices that have been selected, to indicate morph target strengths at different 
        locations on the model or control or to show base colors.
        
        When updating the color information, this method usually sets all vertex colors in the C array
        that were derived from a single Python Vert object to be the same color. 
        **Editorial Note. The colorIndexToUpdate Parameter seems to allow for only a single C vertex
        to be updated, but there don't seem to be any method calls that use this parameter.**

        Parameters
        ----------

        updateNor:
            *int*. If anything other than None, the normal will be updated.

        updateCoo:
            *int*. If anything other than None, the coords will be updated.

        updateCol:
            *int*. If anything other than None, the color will be updated.

        colorIndexToUpdate:
            *int*. If specified, this parameter is used as the index of a color
            in the C array of colors. A vertex can be shared by various faces
            and it's possible to assign it different colors on different faces.
            If this parameter is left to default to 'None' the default color
            index will be calculated based on the index of the vertex.

        """

        if updateCoo:
            for i in self.indicesInFullVertArray:
                self.object.object3d.setVertCoord(i, self.co)
        if updateNor:
            for i in self.indicesInFullVertArray:
                self.object.object3d.setNormCoord(i, self.no)
        if updateCol:
            for i in self.indicesInFullVertArray:
                self.object.object3d.setColorComponent(i, self.color)

    def calcNorm(self):
        """
        This method calculates the vertex surface normal based upon a mathematical average
        of the physical normals of all faces sharing this vertex. This results in a smooth surface.

        .. image:: ../images/vert_norm.png

        The physical normal of a surface is a direction vector at right angles
        to that surface. Although the triangular mesh consists of a series of flat
        faces, the surface normal calculated for a vertex averages out the
        physical normals of the faces that share that vertex, enabling the
        rendering engine (OpenGL) to shade the object so that the surface looks
        like a single, smooth shape.

        Note for API developers
        -----------------------

        Because the actual 3D engine uses optimized glDrawElements,
        where each vertex can have only one normal, it is impossible
        in MakeHuman to draw the geometry in a \"flat\" mode.

        MakeHuman is organically oriented, so the benefits of using this optimized technique
        outweigh potential performance costs.

        **Parameters:** This method has no parameters.

        """

        no = [0.0, 0.0, 0.0]
        for f in self.sharedFaces:
            no[0] += f.no[0]
            no[1] += f.no[1]
            no[2] += f.no[2]
        self.no = vnorm3d(no)

    def vertsShared(self):
        """
        This method returns a list of the vertices of all faces that share this vertex.

        .. image:: ../images/vert_shared.png

        If processing the vector V in the image above this function would return [v1,v2,v3,v4,v5,v6,v7]

        **Parameters:** This method has no parameters.

        """

        sharedVertices = set()
        for f in self.sharedFaces:
            for v in f.verts:
                sharedVertices.add(v)
        return list(sharedVertices)

    def __str__(self):
        """
        This method returns a string listing the index of the vertex and the
        x, y, and z coordinates of this vertex. This method is called when 
        the vertex object is passed to the 'print' function.

        **Parameters:** This method has no parameters.

        """

        return 'vert num %s, coord(%s,%s,%s)' % (self.idx, self.co[0], self.co[1], self.co[2])


class Face:

    """
    A face object.

    Basic usage
    ------------

    ::

        import module3d

        v1 = module3d.Vert([0,0,0])
        v2 = module3d.Vert([0,1,0])
        v3 = module3d.Vert([1,1,0])
        v3 = module3d.Vert([1,0,0])

        f = module3d.Face(v1,v2,v3,v4)
        
    Attributes
    ----------
    
    - **self.no**: *float list* The physical surface normal of the face (x,y,z). Default: [0, 0, 0].
    - **self.verts**: *verts list* A list of 4 vertices that represent the corners of this face.
    - **self.idx**: *int* The index of this face in the list of faces.
    - **self.group**: *FaceGroup* The face group that is the parent of this face.
    - **self.color**: *list of list of ints*. A list of 3 lists of 4 integers (0-255)
      [[r,g,b,a],[r,g,b,a],[r,g,b,a]] used as the 3 vertex colors (including an alpha channel).
    - **self.colorID**: *list of list of ints*. A list of 3 integers (0-255) [index1,index2,index3]
      used as a 'selection' color.
    - **self.uv**: *list of ints*. A list of 4 ints [i,i,i,i]
      holding the index to the UV coordinates in the objects' uvValues list for the uv-mapping of textures to this face.
    """

    def __init__(self, *verts):
        """
        This is the constructor method for the Face class.
        It initializes all face attributes.

        Parameters
        ----------

        v0:
            *vert*. First vertex of face

        v1:
            *vert*. Second vertex of face

        v2:
            *vert*. Third vertex of face
            
        v3:
            *vert*. Fourth vertex of face

        """

        self.no = [0.0, 0.0, 0.0]
        self.verts = verts[:]
        self.uv = None
        self.color = None
        self.colorID = [0, 0, 0]
        self.idx = None
        self.group = None

    def setColor(self, color):
        self.color = [color for v in self.verts]
        self.updateColors()

    def calcNormal(self):
        """
        This method calculates the physical surface normal of the face using the planeNorm function from
        the aljabr.py module. This results in a direction vector at right angles to the
        two edges vt2_vt1 and vt2_vt3.

        **Parameters:** This method has no parameters.

        """

        if len(self.verts) > 2:
            vt1 = self.verts[0].co
            vt2 = self.verts[1].co
            vt3 = self.verts[2].co
            self.no = aljabr.planeNorm(vt1, vt2, vt3)
        else:
            self.no = [0.0, 0.0, 1.0]

    def updateColors(self):
        """
        This method updates the color attributes for each vertex on this face.
        """

        # The position of color index to update in C color array
        # is given by the index of face * 3 * 4
        # because for each face we have 3 verts, and for each vert we have
        # 4 floats R,G,B,A.

        for (i, v) in enumerate(self.verts):
            v.color = self.color[i]
            v.update(0, 0, 1)

    def __str__(self):
        """
        This method returns a string listing the index of the face and the
        indices of the three vertices. This method is called when the face
        object is passed to the 'print' function.

        **Parameters:** This method has no parameters.

        """

        return 'face %i: verts: %s' % (self.idx, [v.idx for v in self.verts])


class FaceGroup:

    """
    A FaceGroup (a group of faces with a unique name).

    Each Face object can be part of one FaceGroup. Each face object has an
    attribute, *group*, storing the FaceGroup it is a member of.

    The FaceGroup object contains a list of the faces in the group and must be
    kept in sync with the FaceGroup references stored by the individual faces.
    
    Attributes
    ----------
    
    - **self.name**: *string*. The name of this FaceGroup.
    - **self.faces**: *faces list*. A list of faces. Default: empty.
    - **self.parent**: *Object3d*. The object3D object that contains this FaceGroup. Default: None.

    """

    def __init__(self, name):
        """
        This is the constructor method for the FaceGroup class.
        It initializes all facegroups attributes.

        Parameters
        ----------

        name:
            *string* The name of this FaceGroup.
        """

        self.name = name
        self.__faces = []
        self.parent = None
        self.elementIndex = 0
        self.elementCount = 0

    def __str__(self):
        """
        This method returns a string containing the name of the FaceGroup. This
        method is called when the object is passed to the 'print' function.

        **Parameters:** This method has no parameters.

        """

        return 'facegroup %s' % self.name
        
    def clear(self):
        
        del self.__faces[:]
        
    @property
    def faces(self):
        return iter(self.__faces)

    def createFace(self, verts, uvs=None):
        
        if len(verts) != self.parent.vertsPerPrimitive:
            raise RuntimeError('The amount of vertices does not match the amount of vertices per primitive of the object')
        
        f = Face(*verts)
        f.group = self
        f.idx = len(self.parent.faces)
        self.__faces.append(f)
        self.parent.faces.append(f)

        if uvs:
            if len(verts) != len(uvs):
                raise RuntimeError('The amount of uv coordinates does not match the amount of vertices')
            f.uv = [self.parent.addUv(uv) for uv in uvs]
            
        for v in verts:
            v.sharedFaces.append(f)

        return f

    def setColor(self, color):
        for f in self.__faces:
            f.setColor(color)

class Object3D:

    """
    A 3D object, made up of faces and vertices (i.e. containing Face objects and Vert objects).
    The humanoid object manipulated by the MakeHuman application is an instance of this
    class, as are all the GUI controls. Multiple 3D objects can be added to the 3D scene.

    This object has a position and orientation of its own, and the positions and
    orientations of faces and vertices that make up this object are defined relative to
    it. 
    
    Attributes:
    -----------
    
    - **self.name**: *string* The name of this Object3D object.
    - **self.object3d**: *mh.Object3d* The object in the OpenGL engine array.
    - **self.x**: *float* The x coordinate of the position of this object in the coordinate space of the scene.
    - **self.y**: *float* The y coordinate of the position of this object in the coordinate space of the scene.
    - **self.z**: *float* The z coordinate of the position of this object in the coordinate space of the scene.
    - **self.rx**: *float* The x rotation component of the orientation of this object within the coordinate space of the scene.
    - **self.ry**: *float* The y rotation component of the orientation of this object within the coordinate space of the scene.
    - **self.rz**: *float* The z rotation component of the orientation of this object within the coordinate space of the scene.
    - **self.sx**: *float* The x scale component of the size of this object within the coordinate space of the scene.
    - **self.sy**: *float* The y scale component of the size of this object within the coordinate space of the scene.
    - **self.sz**: *float* The z scale component of the size of this object within the coordinate space of the scene.
    - **self.verts**: *verts list* The list of vertices that go to make up this object.
    - **self.faces**: *faces list* The list of faces that go to make up this object.
    - **self.faceGroups**: *faceGroups list* The list of FaceGroups that go to make up this object.
    - **self.cameraMode**: *int flag* A flag to indicate which of the two available perspective camera projections, fixed or movable, is to be used to draw this object.
    - **self.visibility**: *int flag* A flag to indicate whether or not this object is visible.
    - **self.texture**: *string* The path of a TGA file on disk containing the object texture.
    - **self.shader**: *int* The shader.
    - **self.shaderParameters**: *dictionary* The shader parameters.
    - **self.shadeless**: *int flag* A flag to indicate whether this object is unaffected by variations in lighting (certain GUI elements aren't).
    - **self.indexBuffer**: *faces list* The list of faces as indices to the vertexbuffer.
    - **self.vertexBufferSize**: *int* size in vertices of the vertexbuffer.
    - **self.uvValues**: *uv list* The list of uv values referenced to by the faces.
    - **self.pickable**: *int flag* A flag to indicate whether this object is pickable by mouse or not.

    """

    def __init__(self, objName, vertsPerPrimitive=4):
        """
        This is the constructor method for the Object3D class.
        It initializes all object attributes.

        Parameters
        ----------

        objName:
            *string* The name of the object. This name is used to reference this object in the scene3D dictionary.

        """

        self.name = objName
        self.object3d = None
        self.x = 0
        self.y = 0
        self.z = 0
        self.rx = 0
        self.ry = 0
        self.rz = 0
        self.sx = 1
        self.sy = 1
        self.sz = 1
        self.verts = []
        self.faces = []
        self.__faceGroups = []
        self.cameraMode = 1
        self.visibility = 1
        self.pickable = 1
        self.texture = None
        self.shader = 0
        self.shaderParameters = {}

        # self.colors = []

        self.shadeless = 0
        self.solid = 1
        self.transparentPrimitives = 0
        self.vertsPerPrimitive = vertsPerPrimitive
        self.indexBuffer = []
        self.vertexBufferSize = None
        
        self.uvValues = None
        self.uvMap = {}
        
    @property
    def faceGroups(self):
        return iter(self.__faceGroups)
        
    @property
    def faceGroupCount(self):
        return len(self.__faceGroups)
        
    def clear(self):

        if self.indexBuffer:
            del self.indexBuffer[:]
        if self.uvValues:
            del self.uvValues[:]
        self.uvMap.clear()
        # Remove verts
        for v in self.verts:
            del v.object
            del v.sharedFaces[:]
        del self.verts[:]
        # Remove faces
        for f in self.faces:
            del f.verts
            del f.group
        del self.faces[:]
        # Remove face groups
        for fg in self.__faceGroups:
            del fg.parent
            fg.clear()
        del self.__faceGroups[:]

    def updateIndexBuffer(self):
        # Build the lists of vertex indices and UV-indices for this face group.
        # In the Python data structures a single vertex can be shared between
        # multiple faces in the same face group. However, if a single vertex
        # has multiple UV-settings, then we generate additional vertices so
        # that we have a place to record the separate UV-indices.
        # Where the UV-map needs a sharp transition (e.g. where the eyelids
        # meet the eyeball) we therefore create duplicate vertices.
        del self.indexBuffer[:]
        fullArrayIndex = 0
        for g in self.__faceGroups:
          if 'joint' in g.name:
            continue
          g.elementIndex = fullArrayIndex  # first index in opengl array
          groupVerts = {}
          for f in g.faces:
              for (i, v) in enumerate(f.verts):
                  if f.uv:
                      t = f.uv[i]
                  else:
                      t = -1
                  if (v.idx, t) not in groupVerts:
                      v.indicesInFullVertArray.append(fullArrayIndex)
                      groupVerts[(v.idx, t)] = fullArrayIndex
                      self.indexBuffer.append(fullArrayIndex)
                      fullArrayIndex += 1
                  else:
                      self.indexBuffer.append(groupVerts[(v.idx, t)])
          g.elementCount = g.elementIndex - fullArrayIndex

        self.vertexBufferSize = fullArrayIndex

    def createFaceGroup(self, name):
        fg = FaceGroup(name)
        fg.parent = self
        self.__faceGroups.append(fg)
        return fg

    def createVertex(self, co):
        v = Vert(co, len(self.verts), self)
        self.verts.append(v)
        return v
        
    def addUv(self, uv):
        key = tuple(uv)
        try:
            return self.uvMap[key]
        except:
            index = len(self.uvValues)
            self.uvMap[key] = index
            self.uvValues.append(uv)
            return index
            
    def setColor(self, color):
        for g in self.__faceGroups:
            g.setColor(color)

    def setLoc(self, locx, locy, locz):
        """
        This method is used to set the location of the object in the 3D coordinate space of the scene.

        Parameters
        ----------

        locx:
            *float*. The x coordinate of the object.
        locy:
            *float*. The y coordinate of the object.
        locz:
            *float*. The z coordinate of the object.
        """

        self.x = locx
        self.y = locy
        self.z = locz
        try:
            self.object3d.translation = (self.x, self.y, self.z)
        except AttributeError, text:
            pass

    def setRot(self, rx, ry, rz):
        """
        This method sets the orientation of the object in the 3D coordinate space of the scene.

        Parameters
        ----------

        rx:
            *float*. Rotation around the x-axis.
        ry:
            *float*. Rotation around the y-axis.
        rz:
            *float*. Rotation around the z-axis.
        """

        self.rx = rx
        self.ry = ry
        self.rz = rz
        try:
            self.object3d.rotation = (self.rx, self.ry, self.rz)
        except AttributeError, text:
            pass

    def setScale(self, sx, sy, sz):
        """
        This method sets the scale of the object in the 3D coordinate space of
        the scene, relative to the initially defined size of the object.

        Parameters
        ----------

        sx:
            *float*. Scale along the x-axis.
        sy:
            *float*. Scale along the y-axis.
        sz:
            *float*. Scale along the z-axis.
        """

        self.sx = sx
        self.sy = sy
        self.sz = sz
        try:
            self.object3d.scale = (self.sx, self.sy, self.sz)
        except AttributeError, text:
            pass

    def setVisibility(self, visible):
        """
        This method sets the visibility of the object.

        Parameters
        ----------

        visib:
            *int flag*. Whether or not the object is visible. 1=Visible, 0=Invisible.
        """

        self.visibility = visible
        try:
            self.object3d.visibility = int(visible)
        except AttributeError, text:
            pass

    def setPickable(self, pickable):
        """
        This method sets the pickable flag of the object.

        Parameters
        ----------

        visib:
            *int flag*. Whether or not the object is pickable. 0=not pickable, 1=pickable.
        """

        self.pickable = pickable
        try:
            self.object3d.pickable = pickable
        except IndexError, text:
            pass

    def setTexture(self, path, cache=None):
        """
        This method is used to specify the path of a TGA file on disk containing the object texture.

        Parameters
        ----------

        path:
            *string* The path of a texture TGA file.
        """
        
        self.texture = path
        
        if not path:
            self.clearTexture()
        
        texture = getTexture(path, cache)
        
        if texture:
            try:
                self.object3d.texture = texture.textureId
            except AttributeError, text:
                pass

    def clearTexture(self):
        """
        This method is used to clear an object's texture.

        **Parameters:** This method has no parameters.
        
        """

        self.texture = None
        try:
            self.object3d.texture = 0
        except AttributeError, text:
            pass

    def hasTexture(self):
        return self.object3d.texture != 0

    def setShader(self, shader):
        """
        This method is used to specify the shader.

        Parameters
        ----------
        
        path:
            *int* The shader.
        """

        self.shader = shader
        try:
            self.object3d.shader = shader
        except AttributeError, text:
            pass

    def setShaderParameter(self, name, value):
        self.shaderParameters[name] = value
        try:
            self.object3d.shaderParameters[name] = value
        except AttributeError, text:
            pass

    def setShadeless(self, shadeless):
        """
        This method is used to specify whether or not the object is affected by lights.
        This is used for certain GUI controls to give them a more 2D type
        appearance (predominantly the top bar of GUI controls).

        Parameters
        ----------

        shadeVal:
            *int* Whether or not the object is unaffected by lights. If 0, it is affected by lights; if 0, it is not.

        """

        self.shadeless = shadeless
        try:
            self.object3d.shadeless = self.shadeless
        except AttributeError, text:
            pass
            
    def setSolid(self, solid):
        self.solid = solid
        try:
            self.object3d.solid = self.solid
        except AttributeError, text:
            pass
            
    def setTransparentPrimitives(self, transparentPrimitives):
        self.transparentPrimitives = transparentPrimitives
        try:
            self.object3d.transparentPrimitives = self.transparentPrimitives
        except AttributeError, text:
            pass
            
    def setVertsPerPrimitive(self, vertsPerPrimitive):
        self.vertsPerPrimitive = vertsPerPrimitive
        try:
            self.object3d.vertsPerPrimitive = self.vertsPerPrimitive
        except AttributeError, text:
            pass

    def getFaceGroup(self, name):
        """
        This method searches the list of FaceGroups held for this object, and
        returns the FaceGroup with the specified name. If no FaceGroup is found
        for that name, this method returns None.

        Parameters
        ----------

        name:
            *string*  The name of the FaceGroup to retrieve.
        """

        for fg in self.__faceGroups:
            if fg.name == name:
                return fg
        return None

    def getVerticesAndFacesForGroups(self, groupNames):
        vertices = []
        faces = []

        for name in groupNames:
            group = self.getFaceGroup(name)
            faces.extend(group.faces)
            for f in group.faces:
                vertices.extend(f.verts)
        vertices = list(set(vertices))
        return (vertices, faces)

    def updateGroups(self, groupnames, recalcNormals=True, update=True):
        if recalcNormals or update:
            (vertices, faces) = self.getVerticesAndFacesForGroups(groupnames)
            if recalcNormals:
                self.calcNormals(1, 1, vertices, faces)
            if update:
                self.update(vertices)

    def setCameraProjection(self, cameraMode):
        """
        This method sets the camera mode used to visualize this object (fixed or movable).
        The 3D engine has two camera modes (both perspective modes).
        The first is moved by the mouse, while the second is fixed.
        The first is generally used to model 3D objects (a human, clothes,
        etc.), while the second is used for 3D GUI controls.

        Parameters
        ----------

        mode:
            *int*  The camera mode to be used for this object. 0 = fixed camera; 1 = movable camera
        """

        self.cameraMode = cameraMode
        try:
            self.object3d.cameraMode = self.cameraMode
        except AttributeError, text:
            pass

    def update(self, verticesToUpdate=None, updateN=True):
        """
        This method is used to call the update methods on each of a list of vertices that form part of this object.

        Parameters
        ----------

        indexToUpdate:
            *int list*  The list of vertex indices to update

        """

        if verticesToUpdate == None:
            verticesToUpdate = self.verts
        
        for v in verticesToUpdate:
            v.update(updateNor=updateN)
            
        #print "updated %d vertices" % len(verticesToUpdate)

    def applySelectionColor(self):
        """
        This method applies the 'selection' color to all of the vertices within this object.

        Selection of a vertex is indicated on the screen by increasing
        the Red color component and decreasing the Green and Blue color
        components by a fixed amount (50) and then capping the value so
        that it remains within the bounds of 0-255.

        **Parameters:** This method has no parameters.

        """

        for v in self.verts:
            v.update(0, 0, 1)

    def applyDefaultColor(self):
        """
        This method applies the color white to all of the vertices within this object.

        **Parameters:** This method has no parameters.

        """

        for v in self.verts:
            v.color = [255, 255, 255, 255]
            v.update(0, 0, 1)

    def calcNormals(self, recalcVertexNormals=1, recalcFaceNormals=1, verticesToUpdate=None, facesToUpdate=None):
        """
        This method calls the calcNormal method for a subset of the faces
        in this Object3D object and the calcNorm method on a subset of the
        vertices in this Object3D object.

        If no faces are specified the face normals are not recalculated. If the
        recalcNorms flag is set to None the vertex normals are not recalculated.
        If 'None' is specified for the vertex indices then all vertex indices
        are recalculated (so long as recalcNorms is not set to None).

        The calcNormal method of a face will recalculate the actual physical
        surface normal.
        The calcNorm method of a vertex calculates the vertex's surface normal
        as an average of the  physical surface normals of the faces that share
        that vertex.

        Parameters
        ----------

        indexToUpdate:
            *int list*  The list of indices pointing to the vertices that need to be updated.

        facesToRecalcNorm:
            *int list*  The list of indices pointing to the faces to be updated.

        recalcNorms:
            *flag*  A flag to indicate whether or not the vertex normals should be recalculated.
            If set to anything other than None, the vertex normals are recalculated.
            Otherwise only need the face normals are recalculated.

        """

        if recalcFaceNormals:
            if facesToUpdate == None:
                facesToUpdate = self.faces
            for f in facesToUpdate:
                f.calcNormal()

        if recalcVertexNormals:
            if verticesToUpdate == None:
                verticesToUpdate = self.verts
            for v in verticesToUpdate:
                v.calcNorm()
                
    def calcBBox(self):
        
        if self.verts:
            bbox =  [self.verts[0].co[:],self.verts[0].co[:]]
            for v in self.verts:
                if v.co[0] < bbox[0][0]: #minX
                    bbox[0][0] = v.co[0]
                if v.co[0] > bbox[1][0]: #maxX
                    bbox[1][0] = v.co[0]
                if v.co[1] < bbox[0][1]: #minY
                    bbox[0][1] = v.co[1]
                if v.co[1] > bbox[1][1]: #maxY
                    bbox[1][1] = v.co[1]
                if v.co[2] < bbox[0][2]: #minZ
                    bbox[0][2] = v.co[2]
                if v.co[2] > bbox[1][2]: #maxX
                    bbox[1][2] = v.co[2]
        else:
            bbox = [[0,0,0], [0,0,0]]
        return bbox

    def __str__(self):
        """
        This method returns a string containing the object name, the number of
        vertices, the number of faces, and the location of the object. It is
        called when the object is passed to the 'print' function.

        **Parameters:** This method has no parameters.

        """

        return 'object3D named: %s, nverts: %s, nfaces: %s, at |%s,%s,%s|' % (self.name, len(self.verts), len(self.faces), self.x, self.y, self.z)


class Scene3D:

    """
    A 3D object that stores the contents of a scene (made up primarily of
    one or more Object3D objects).
    As a minimum the MakeHuman scene usually consists of a humanoid object
    that can be manipulated by the MakeHuman application, plus a set of 3D GUI
    controls.

    Multiple 3D model objects can theoretically be added to the 3D scene.
    Future versions of MakeHuman are likely to support multiple humanoid
    objects, and potentially separate objects such as clothing and props.

    MakeHuman Selectors
    -------------------

    This object supports the use of a technique called *Selection Using Unique
    Color IDs*, that internally uses color-coding of components within the
    scene to support the selection of objects by the user using the mouse.

    This technique generates a sequence of colors (color IDs), assigning a
    unique color to each uniquely selectable object or component in the scene.
    These colors are not displayed, but are used by MakeHuman to generates an
    unseen image of the various selectable elements. This image uses the same
    camera settings currently being used for the actual, on-screen image.
    When the mouse is clicked, the position of the mouse is used with the
    unseen image to retrieve a color. MakeHuman uses this color as an ID to
    identify which object or component the user clicked with the mouse.

    This technique uses glReadPixels() to read the single pixel at the
    current mouse location, using the unseen, color-coded image.

    For further information on this technique, see:

      - http://www.opengl.org/resources/faq/technical/selection.htm and
      - http://wiki.gamedev.net/index.php/OpenGL_Selection_Using_Unique_Color_IDs

    **Note.** Because the 3D engine uses glDrawElements in a highly opimized
    way and each vertex can have only one color ID, there there is a known
    problem with selecting individual faces with very small FaceGroups using
    this technique. However, this is not a major problem for MakeHuman, which
    doesn't use such low polygon groupings.

    Attributes
    ----------
    
    - **self.objects**: *3Dobject list* A list of the 3D objects in the scene.
    - **self.faceGroupColorID**: *Dictionary of colors IDs* A dictionary of the color IDs used for
      selection (see MakeHuman Selectors, above).
    - **self.colorID**: *float list* A progressive color ID.
    
    The attributes *self.colorID* and *self.faceGroupColorID*
    support a technique called *Selection Using Unique Color IDs* to make each
    FaceGroup independently clickable.

    The attribute *self.colorID* stores a progressive color that is incremented for each successive
    FaceGroup added to the scene.
    The *self.faceGroupColorID* attribute contains a list that serves as a directory to map
    each color back to the corresponding FaceGroup by using its color ID.
    """

    def __init__(self):
        """
        This is the constructor method for the Scene3D class.
        It initializes the following attributes:        

        **Parameters:** This method has no parameters.

        """

        self.objects = []
        self.faceGroupColorID = {}
        self.colorID = 0

    def __str__(self):
        """
        This method is the Print method for a Scene3D object, which returns a string containing the words
        \"scene_type\".

        **Parameters:** This method has no parameters.

        """

        return 'scene_type'

    def clear(self, obj):
        
        if obj.object3d:
            mh.world.remove(obj.object3d)
            del obj.object3d
            obj.object3d = None
        obj.clear()
        
    def delete(self, obj):
        
        self.clear(obj)
        self.objects.remove(obj)

    def attach(self, obj):
        if obj.object3d:
            return
        if not obj.vertexBufferSize:
            return

        self.assignSelectionID(obj)

        #print "sending: ", obj.name, len(obj.verts)

        coIdx = 0
        fidx = 0
        uvIdx = 0
        colIdx = 0

        # create an object with vertexBufferSize vertices and len(indexBuffer) / 3 triangles

        obj.object3d = mh.Object3D(obj.vertexBufferSize, obj.indexBuffer)
        mh.world.append(obj.object3d)

        for g in obj.faceGroups:
            if 'joint' in g.name:
                continue
            groupVerts = set()
            for f in g.faces:
                faceColor = f.color
                if faceColor == None:
                    faceColor = [[255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255]]
                fUV = f.uv
                if fUV == None:
                    fUV = [-1, -1, -1, -1]

                i = 0
                for v in f.verts:
                    if (v.idx, fUV[i]) not in groupVerts:

                        # obj.object3d.setAllCoord(coIdx, colIdx, v.co, v.no, f.colorID, faceColor[i])

                        obj.object3d.setVertCoord(coIdx, v.co)
                        obj.object3d.setNormCoord(coIdx, v.no)
                        obj.object3d.setColorIDComponent(coIdx, f.colorID)
                        obj.object3d.setColorComponent(colIdx, faceColor[i])
                        groupVerts.add((v.idx, fUV[i]))

                        coIdx += 1
                        colIdx += 1

                        if obj.uvValues:
                            obj.object3d.setUVCoord(uvIdx, obj.uvValues[fUV[i]])
                            uvIdx += 1

                    i += 1

        if obj.texture:
            obj.setTexture(obj.texture)

        obj.object3d.shader = obj.shader

        for (name, value) in obj.shaderParameters.iteritems():
            obj.object3d.shaderParameters[name] = value

        obj.object3d.translation = (obj.x, obj.y, obj.z)
        obj.object3d.rotation = (obj.rx, obj.ry, obj.rz)
        obj.object3d.scale = (obj.sx, obj.sy, obj.sz)
        obj.object3d.visibility = obj.visibility
        obj.object3d.shadeless = obj.shadeless
        obj.object3d.pickable = obj.pickable
        obj.object3d.solid = obj.solid
        obj.object3d.transparentPrimitives = obj.transparentPrimitives
        obj.object3d.vertsPerPrimitive = obj.vertsPerPrimitive
        obj.object3d.cameraMode = obj.cameraMode

        # TODO add all obj attributes

    def detach(self, obj):
        mh.world.remove(obj.object3d)
        del obj.object3d
        obj.object3d = None

    def update(self):
        """
        This method sends scene data to the OpenGL engine to regenerate the OpenGL scene based on the objects
        currently contained in this Scene3D object.
        This is a very important function, but it is expensive in terms of processing time, so it must be called
        only when absolutely necessary; in particular, when one or more new objects are added to the scene.

        If you only need to *redraw* the scene, use the scene.redraw() method instead.

        **Parameters:** This method has no parameters.

        """

        for obj in self.objects:
            self.attach(obj)

    def reloadTextures(self):
        print 'Reloading textures'
        for path in textureCache:
            try:
                textureCache[path].loadImage(path)
            except RuntimeError, text:
                print text

    def getWindowSize(self):
        """
        This method returns the width and height of the drawable area within 
        the MakeHuman window in pixels (the viewport size).
        It calls the getWindowSize function on the 'mh' module 
        (a module created dynamically at run time by main.c) to retrieve the 
        width and height of the window (the OpenGL viewport) from global 
        variables updated before an event was passed up to the Python code. 

        **Parameters:** This method has no parameters.
        """

        return mh.getWindowSize()

    def getObject(self, name):
        """
        This method searches the list of 3D objects contained within the scene and returns the object with
        the specified name, or None if no object with that name could be found.

        Parameters
        ----------

        name:
            *string*. The name of the object to retrieve.
        """

        for obj in self.objects:
            if obj.name == name:
                return obj
        return None

        # print "Obj %s not found"%(name)

    def grabScreen(self, x, y, width, height, filename):
        """
        This method calls the grabScreen method on the 'mh' class which invokes the 
        corresponding C function (mhGrabScreen) to take a rectangular section from 
        the screen and write an image to a bitmap image file on disk containing the 
        pixels currently displayed in that section of screen.

        Parameters
        ----------

        x:
            *int* an int containing the x coordinate of the corner of the area (in pixels).
        y:
            *int* an int containing the y coordinate of the corner of the area (in pixels).
        width:
            *int* an int containing the width of the area in pixels. 
        length:
            *int* an int containing the height of the area in pixels. 
        filename:
            *string* a string containing the full path of the file on disk.

        """

        # cursor = self.getObject("cursor.obj")
        # cursor.setVisibility(0)

        mh.grabScreen(x, y, width, height, filename)

        # cursor.setVisibility(1)

    def newObj(self, name):
        """
        This method creates a newly initialized Object3D instance within this Scene3D object
        and returns it to the calling code ready to be populated.

        Parameters
        ----------

        name:
            *string*. The name for the new Object3D object.

        """

        newObj = Object3D(name)
        self.objects.append(newObj)
        return newObj

    def instanceObj(self, obj, name):
        """
        This macro creates a reference copy of the Object3D object that is passed in as a parameter.
        It instantiates new FaceGroups which contain the same faces as the original.

        This new object shares the same vertices and faces as the original. Only
        index references are copied, and no new vertices or faces are created.

        The new object is added into the Scene3D object and is returned to the calling code.

        Parameters
        ----------

        obj:
            *object 3D*. The object3D object to be copied.

        name:
            *string*. The name of the new instance.

        """

        newObj = Object3D(name)
        newObj.x = obj.x
        newObj.y = obj.y
        newObj.z = obj.z
        newObj.rx = obj.rx
        newObj.ry = obj.ry
        newObj.rz = obj.rz
        newObj.r = obj.r
        newObj.g = obj.g
        newObj.b = obj.b
        newObj.verts = obj.verts
        newObj.faces = obj.faces

        for fg in obj.__faceGroups:
            newFg = FaceGroup(name + fg.name)
            newFg.faces = fg.faces
            newObj.addFaceGroup(newFg)

        newObj.cameraMode = obj.cameraMode
        newObj.visibility = obj.visibility
        newObj.texture = obj.texture
        newObj.shader = obj.shader
        newObj.colors = obj.colors
        newObj.cameraMode = obj.cameraMode
        self.objects.append(newObj)
        return newObj

    def deleteObj(self, name):
        """
        This method searches the list of Object3D objects contained within this Scene3D object by name and,
        if found, it deletes that object.
        First, the instance of the object is deleted. Then the index of objects,
        used to identify the object in the OpenGL engine array, is updated and
        renumbered to close the gap.

        Parameters
        ----------

        name:
            *string*. The name of object to delete.
        """

        for obj in self.objects:
            if obj.name == name:
                self.objects.remove(obj)
                mh.world.remove(obj)
                break

    def assignSelectionID(self, obj):
        """
        This method generates a new, unique color ID for each FaceGroup,
        within a particular Object3D object, that forms a part of this scene3D
        object. This color ID can subsequently be used in a non-displayed
        image map to determine the FaceGroup that a mouse click was made in.

        This method loops through the FaceGroups, assigning the next color
        in the sequence to each subsequent FaceGroup. The color value is
        written into a 'dictionary' to serve as a color ID that can be
        translated back into the corresponding FaceGroup name when a mouse
        click is detected.
        This is part of a technique called *Selection Using Unique Color IDs*
        to make each FaceGroup independently clickable.

        (See 'MakeHuman Selectors' above.)

        Parameters
        ----------

        obj:
            *object 3D*. The object3D object for which a color dictionary is to be generated.

        """

        # print "DEBUG COLOR AND GROUPS, obj", obj.name
        # print "---------------------------"

        for g in obj.faceGroups:
            self.colorID += 1

            # 555 to 24-bit rgb

            idR = (self.colorID % 32) * 8
            idG = ((self.colorID >> 5) % 32) * 8
            idB = ((self.colorID >> 10) % 32) * 8

            for f in g.faces:
                f.colorID = (idR, idG, idB)
            
            self.faceGroupColorID[self.colorID] = g

            # print "SELECTION DEBUG INFO: facegroup %s of obj %s has the colorID = %s,%s,%s or %s"%(g.name,obj.name,idR,idG,idB, self.colorID)

    def getSelectedFacesGroup(self):
        """
        This method uses a non-displayed image containing color-coded faces
        to return the index of the FaceGroup selected by the user with the mouse.
        This is part of a technique called *Selection Using Unique Color IDs* to make each
        FaceGroup independently clickable.
        (see 'MakeHuman Selectors' above.)

        **Parameters:** This method has no parameters.

        """

        picked = mh.getColorPicked()

        IDkey = picked[0] / 8 | picked[1] / 8 << 5 | picked[2] / 8 << 10  # 555

        # print "DEBUG COLOR PICKED: %s,%s,%s %s"%(picked[0], picked[1], picked[2], IDkey)

        try:
            groupSelected = self.faceGroupColorID[IDkey]
        except:

            # print groupSelected.name
            #this print should only come on while debugging color picking
            #print 'Color %s (%s) not found' % (IDkey, picked)
            groupSelected = None
        return groupSelected

    def getPickedObject(self):
        """
        This method determines whether a FaceGroup or a non-selectable zone has been
        clicked with the mouse. It returns a tuple, showing the FaceGroup and the parent
        Object3D object, or None.
        If no object is picked, this method will simply print \"no clickable zone.\"

        **Parameters:** This method has no parameters.

        """

        facegroupPicked = self.getSelectedFacesGroup()
        if facegroupPicked:
            objPicked = facegroupPicked.parent
            return (facegroupPicked, objPicked)
        else:
            #this print should only be made while debugging picking
            #print 'not a clickable zone'
            return None
            
def getFacesFromVerts(vertIndices, verts):
  #F = set();
  #for index in vertIndices:
  #  F = F.union(verts[index].sharedFaces)
  return set([f for f in verts[i].sharedFaces for i in verIndices])