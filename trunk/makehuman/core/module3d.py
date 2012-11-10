import os
import weakref

import numpy as np

import mh
from compat import VertProxy, FaceProxy, VertsProxy, FacesProxy

class Texture(mh.Texture):

    """
    A subclass of the base texture class extended to hold a modification date.
    """

    def __init__(self, *args, **kwargs):
        mh.Texture.__init__(self, *args, **kwargs)
        self.modified = None
        
textureCache = {}

def getTexture(path, cache=None):
    texture = None
    cache = cache or textureCache
    
    if path in cache:
        texture = cache[path]
        
        if os.stat(path).st_mtime != texture.modified:
            print ('reloading ', path)	# TL: unicode problems unbracketed

            try:
                img = mh.Image(path=path)
                texture.loadImage(img)
            except RuntimeError, text:
                print text
                return
            else:
                texture.modified = os.stat(path).st_mtime
    else:
        try:
            img = mh.Image(path=path)
            texture = Texture(img)
            #texture.loadSubImage('data/themes/default/images/slider_focused.png', 0, 0)
        except RuntimeError, text:
            print text
        else:
            texture.modified = os.stat(path).st_mtime
            cache[path] = texture

    return texture
    
def reloadTextures():
    print 'Reloading textures'
    for path in textureCache:
        try:
            textureCache[path].loadImage(path)
        except RuntimeError, text:
            print text

class FaceGroup(object):
    """
    A FaceGroup (a group of faces with a unique name).

    Each Face object can be part of one FaceGroup. Each face object has an
    attribute, *group*, storing the FaceGroup it is a member of.

    The FaceGroup object contains a list of the faces in the group and must be
    kept in sync with the FaceGroup references stored by the individual faces.
    
    .. py:attribute:: name
    
        The name. str
        
    .. py:attribute:: parent
    
        The parent. :py:class:`module3d.Object3D`

    :param name: The name of the group.
    :type name: str
    """

    black = np.zeros(3, dtype=np.uint8)

    def __init__(self, object, name, idx):
        self.object = object
        self.parent = object
        self.name = name
        self.idx = idx
        self.color = None
        self.colorID = self.black

    def __str__(self):
        """
        This method returns a string containing the name of the FaceGroup. This
        method is called when the object is passed to the 'print' function.

        **Parameters:** This method has no parameters.

        """

        return 'facegroup %s' % self.name

    def setColor(self, rgba):
        self.color = np.asarray(rgba, dtype = np.uint8)

    @property
    def faces(self):
        for f in self.object.getFacesForGroups([self.name]):
            yield FaceProxy(self.object, f)

class Object3D(object):
    def __init__(self, objName, vertsPerPrimitive=4):

        self.name = objName
        self.vertsPerPrimitive = vertsPerPrimitive
        self.loc = np.zeros(3)
        self.rot = np.zeros(3)
        self.scale = np.ones(3)
        self._faceGroups = []
        self._groups_rev = {}
        self.cameraMode = 1
        self.visibility = 1
        self.pickable = 1
        self.texture = None
        self.textureId = 0
        self.shader = 0
        self.shaderParameters = {}
        self.shadeless = 0
        self.solid = 1
        self.transparentPrimitives = 0
        self.object3d = None
        self.vmap = None
        self.tmap = None

        self.__object = None

    MAX_FACES = 8

    def get_x(self):
        return self.loc[0]

    def set_x(self, x):
        self.loc[0] = x

    x = property(get_x, set_x)

    def get_y(self):
        return self.loc[1]

    def set_y(self, y):
        self.loc[1] = y

    y = property(get_y, set_y)

    def get_z(self):
        return self.loc[2]

    def set_z(self, z):
        self.loc[2] = z

    z = property(get_z, set_z)

    def get_rx(self):
        return self.rot[0]

    def set_rx(self, rx):
        self.rot[0] = rx

    rx = property(get_rx, set_rx)

    def get_ry(self):
        return self.rot[1]

    def set_ry(self, ry):
        self.rot[1] = ry

    ry = property(get_ry, set_ry)

    def get_rz(self):
        return self.rot[2]

    def set_rz(self, rz):
        self.rot[2] = rz

    rz = property(get_rz, set_rz)

    def get_sx(self):
        return self.scale[0]

    def set_sx(self, sx):
        self.scale[0] = sx

    sx = property(get_sx, set_sx)

    def get_sy(self):
        return self.scale[1]

    def set_sy(self, sy):
        self.scale[1] = sy

    sy = property(get_sy, set_sy)

    def get_sz(self):
        return self.scale[2]

    def set_sz(self, sz):
        self.scale[2] = sz

    sz = property(get_sz, set_sz)

    @property
    def verts(self):
        return VertsProxy(self)

    @property
    def faces(self):
        return FacesProxy(self)

    def calcFaceNormals(self, ix = None):
        if ix is None:
            ix = np.s_[:]
        fvert = self.coord[self.fvert[ix]]
        v1 = fvert[:,0,:]
        v2 = fvert[:,1,:]
        v3 = fvert[:,2,:]
        va = v1 - v2
        vb = v2 - v3
        self.fnorm[ix] = np.cross(va, vb)

    def calcVertexNormals(self, ix = None):
        sync_all = ix is None
        self.markCoords(ix, norm=True)
        if ix is None:
            ix = np.s_[:]

        vface = self.vface[ix]
        norms = self.fnorm[vface]
        norms *= np.arange(self.MAX_FACES)[None,:,None] < self.nfaces[ix][:,None,None]
        norms = np.sum(norms, axis=1)
        norms /= np.sqrt(np.sum(norms ** 2, axis=-1))[:,None]
        self.vnorm[ix] = norms

    def getObject(self):
        if self.__object:
            return self.__object()
        else:
            return None
        
    def setObject(self, value):
        self.__object = weakref.ref(value)
    
    object = property(getObject, setObject)
    
    @property
    def faceGroups(self):
        return iter(self._faceGroups)
        
    @property
    def faceGroupCount(self):
        return len(self._faceGroups)

    def clear(self):
        """
        Clears both local and remote data to repurpose this object
        """
    
        # Clear remote data
        self.detach()

        self._faceGroups = []

        del self.fvert
        del self.fnorm
        del self.fuvs
        del self.group

        del self.coord
        del self.vnorm
        del self.color
        del self.texco
        del self.vface
        del self.nfaces

        del self.ucoor
        del self.unorm
        del self.ucolr
        del self.utexc

        self.index = None
        self.grpix = None
        self.vmap = None
        self.tmap = None
        
    def attach(self):
        """
        Prepares the object for rendering.
        """
        if self.object3d:
            return

        nverts = len(self.vmap)

        selectionColorMap.assignSelectionID(self)

        self.object3d = mh.Object3D(self)
        mh.world.append(self.object3d)

        if self.texture:
            self.setTexture(self.texture)
        
    def detach(self):
        """
        Detaches the object, clearing all remote data
        """

        if self.object3d:
            mh.world.remove(self.object3d)
            self.object3d = None

    def setCoords(self, coords):
        nverts = len(coords)
        self.coord = np.asarray(coords, dtype=np.float32)
        self.vnorm = np.zeros((nverts, 3), dtype=np.float32)
        self.color = np.zeros((nverts, 4), dtype=np.uint8) + 255
        self.vface = np.zeros((nverts, self.MAX_FACES), dtype=np.uint32)
        self.nfaces = np.zeros(nverts, dtype=np.uint8)

        self.ucoor = True
        self.unorm = True
        self.ucolr = True

        self.markCoords(None, True, True, True)

    def getVertexCount(self):
        return len(self.coord)

    def getCoords(self, indices = None):
        if indices is None:
            indices = np.s_[...]
        return self.coord[indices]

    def getNormals(self, indices = None):
        if indices is None:
            indices = np.s_[...]
        return self.vnorm[indices]

    def markCoords(self, indices = None, coor = False, norm = False, colr = False):
        if isinstance(indices, tuple):
            indices = indices[0]

        nverts = len(self.coord)

        if coor:
            if indices is None:
                self.ucoor = True
            else:
                if self.ucoor is False:
                    self.ucoor = np.zeros(nverts, dtype=bool)
                if self.ucoor is not True:
                    self.ucoor[indices] = True

        if norm:
            if indices is None:
                self.unorm = True
            else:
                if self.unorm is False:
                    self.unorm = np.zeros(nverts, dtype=bool)
                if self.unorm is not True:
                    self.unorm[indices] = True

        if colr:
            if indices is None:
                self.ucolr = True
            else:
                if self.ucolr is False:
                    self.ucolr = np.zeros(nverts, dtype=bool)
                if self.ucolr is not True:
                    self.ucolr[indices] = True

    def changeCoords(self, coords, indices = None):
        sync_all = indices is None

        self.markCoords(indices, coor=True)

        if indices is None:
            indices = np.s_[...]
        nverts = len(coords)
        self.coord[indices] = coords

    def setUVs(self, uvs):
        ntexco = len(uvs)
        self.texco = np.asarray(uvs, dtype=np.float32)
        self.utexc = True

    def getUVCount(self):
        return len(self.texco)

    def getUVs(self, indices = None):
        if indices is None:
            indices = np.s_[...]
        return self.texco[indices]

    def markUVs(self, indices = None):
        if isinstance(indices, tuple):
            indices = indices[0]

        ntexco = len(self.texco)

        if indices is None:
            self.utexc = True
        else:
            if self.utexc is False:
                self.utexc = np.zeros(ntexco, dtype=bool)
            if self.utexc is not True:
                self.utexc[indices] = True

    def setFaces(self, verts, uvs = None, groups = None):
        nfaces = len(verts)

        self.fvert = np.empty((nfaces, self.vertsPerPrimitive), dtype=np.uint32)
        self.fnorm = np.zeros((nfaces, 3), dtype=np.float32)
        self.fuvs = np.zeros(self.fvert.shape, dtype=np.uint32)
        self.group = np.zeros(nfaces, dtype=np.uint16)

        if nfaces != 0:
            self.fvert[...] = verts
            if uvs is not None:
                self.fuvs[...] = uvs
            if groups is not None:
                self.group[...] = groups

        self.has_uv = uvs is not None

        self._update_faces()

    def hasUVs(self):
        return self.has_uv

    def getFaceCount(self):
        return len(self.fvert)

    def getFaceVerts(self, indices = None):
        if indices is None:
            indices = np.s_[...]
        return self.fvert[indices]

    def getFaceUVs(self, indices = None):
        if indices is None:
            indices = np.s_[...]
        return self.fuvs[indices]

    def _update_faces(self):
        for i, f in enumerate(self.fvert):
            for v in f:
                self.vface[v, self.nfaces[v]] = i
                self.nfaces[v] += 1

    def updateIndexBuffer(self):
        ngroup = len(self._faceGroups)

        group_mask = np.ones(len(self._faceGroups), dtype=bool)
        for g in self._faceGroups:
            if 'joint' in g.name or 'helper' in g.name:
                group_mask[g.idx] = False

        unwelded = []
        unwelded_map = {}

        coord = []
        texco = []
        index = [[] for g in self._faceGroups]

        for i in xrange(len(self.fvert)):
            g = self.group[i]
            if not group_mask[g]:
                continue
            verts = []
            for v, t in zip(self.fvert[i], self.fuvs[i]):
                p = v, t
                if p not in unwelded_map:
                    idx = len(unwelded)
                    unwelded_map[p] = idx
                    unwelded.append(p)
                    coord.append(self.coord[v])
                    texco.append(self.texco[t])
                else:
                    idx = unwelded_map[p]
                verts.append(idx)

            index[g].append(verts)

        del unwelded_map

        unwelded2 = np.empty((len(unwelded),2), dtype=np.uint32)
        if unwelded:
            unwelded2[...] = unwelded
        self.vmap = unwelded2[:,0]
        self.tmap = unwelded2[:,1]
        del unwelded2

        nverts = len(coord)
        self.r_coord = np.empty((nverts, 3), dtype=np.float32)
        self.r_texco = np.empty((nverts, 2), dtype=np.float32)
        self.r_vnorm = np.zeros((nverts, 3), dtype=np.float32)
        self.r_color = np.zeros((nverts, 4), dtype=np.uint8) + 255

        grpix = []
        allix = []
        for g, ix in enumerate(index):
            grpix.append((len(allix), len(ix)))
            allix.extend(ix)
        index = allix

        _index = np.empty((len(index), self.vertsPerPrimitive), dtype=np.uint32)
        if len(index):
            _index[...] = index
        self.index = _index

        _grpix = np.empty((len(grpix),2), dtype=np.uint32)
        if len(grpix):
            _grpix[...] = grpix
        self.grpix = _grpix

        self.ucoor = True
        self.unorm = True
        self.ucolr = True
        self.utexc = True
        self.sync_all()

    def sync_coord(self):
        if self.ucoor is False:
            return
        if self.vmap is None or len(self.vmap) == 0:
            return
        if self.ucoor is True:
            self.r_coord[...] = self.coord[self.vmap]
        else:
            self.r_coord[self.ucoor[self.vmap]] = self.coord[self.vmap][self.ucoor[self.vmap]]
        self.ucoor = False

    def sync_norms(self):
        if self.unorm is False:
            return
        if self.vmap is None or len(self.vmap) == 0:
            return
        if self.unorm is True:
            self.r_vnorm[...] = self.vnorm[self.vmap]
        else:
            self.r_vnorm[self.unorm[self.vmap]] = self.vnorm[self.vmap][self.unorm[self.vmap]]
        self.unorm = False

    def sync_color(self):
        if self.ucolr is False:
            return
        if self.vmap is None or len(self.vmap) == 0:
            return
        if self.ucolr is True:
            self.r_color[...] = self.color[self.vmap]
        else:
            self.r_color[self.ucolr[self.vmap]] = self.color[self.vmap][self.ucolr[self.vmap]]
        self.ucolr = False

    def sync_texco(self):
        if self.utexc is False:
            return
        if self.tmap is None or len(self.tmap) == 0:
            return
        if self.utexc is True:
            self.r_texco[...] = self.texco[self.tmap]
        else:
            self.r_texco[self.utexc[self.tmap]] = self.texco[self.tmap][self.utexc[self.tmap]]
        self.utexc = False

    def sync_all(self):
        self.sync_coord()
        self.sync_norms()
        self.sync_color()
        self.sync_texco()

    def createFaceGroup(self, name):
        """
        Creates a new module3d.FaceGroup with the given name.

        :param name: The name for the face group.
        :type name: [float, float, float]
        :return: The new face group.
        :rtype: :py:class:`module3d.FaceGroup`
        """
        idx = len(self._faceGroups)
        fg = FaceGroup(self, name, idx)
        self._groups_rev[name] = fg
        self._faceGroups.append(fg)
        return fg

    def setColor(self, color):
        """
        Sets the color for the entire object.

        :param color: The color in rgba.
        :type color: [byte, byte, byte, byte]
        """
        color = np.asarray(color, dtype=np.uint8)
        self.color[...] = color[None,:]
        self.markCoords(colr=True)
        self.sync_color()

    def setLoc(self, locx, locy, locz):
        """
        This method is used to set the location of the object in the 3D coordinate space of the scene.

        :param locx: The x coordinate of the object.
        :type locx: float
        :param locy: The y coordinate of the object.
        :type locy: float
        :param locz: The z coordinate of the object.
        :type locz: float
        """

        self.loc[...] = (locx, locy, locz)

    def setRot(self, rx, ry, rz):
        """
        This method sets the orientation of the object in the 3D coordinate space of the scene.

        :param rx: Rotation around the x-axis.
        :type rx: float
        :param ry: Rotation around the y-axis.
        :type ry: float
        :param rz: Rotation around the z-axis.
        :type rz: float
        """

        self.rot[...] = (rx, ry, rz)

    def setScale(self, sx, sy, sz):
        """
        This method sets the scale of the object in the 3D coordinate space of
        the scene, relative to the initially defined size of the object.

        :param sx: Scale along the x-axis.
        :type sx: float
        :param sy: Scale along the x-axis.
        :type sy: float
        :param sz: Scale along the x-axis.
        :type sz: float
        """

        self.scale[...] = (sx, sy, sz)

    def setVisibility(self, visible):
        """
        This method sets the visibility of the object.

        :param visible: Whether or not the object is visible.
        :type visible: Boolean
        """

        self.visibility = visible

    def setPickable(self, pickable):
        """
        This method sets the pickable flag of the object.

        :param pickable: Whether or not the object is pickable.
        :type pickable: Boolean
        """

        self.pickable = pickable

    def setTexture(self, path, cache=None):
        """
        This method is used to specify the path of a file on disk containing the object texture.

        :param path: The path of a texture file.
        :type path: str
        :param cache: The texture cache to use.
        :type cache: dict
        """
        
        self.texture = path
        
        if not path:
            self.clearTexture()

        if not self.object3d:
            return
        
        texture = getTexture(path, cache)
        
        if texture:
            self.object3d.texture = texture.textureId

    def clearTexture(self):
        """
        This method is used to clear an object's texture.
        """

        self.texture = None
        self.textureId = 0

    def hasTexture(self):
        return self.textureId != 0

    def setShader(self, shader):
        """
        This method is used to specify the shader.
        
        :param shadeless: The shader.
        :type shadeless: int
        """

        self.shader = shader

    def setShaderParameter(self, name, value):
        self.shaderParameters[name] = value

    def setShadeless(self, shadeless):
        """
        This method is used to specify whether or not the object is affected by lights.
        This is used for certain GUI controls to give them a more 2D type
        appearance (predominantly the top bar of GUI controls).

        :param shadeless: Whether or not the object is unaffected by lights.
        :type shadeless: Boolean
        """

        self.shadeless = shadeless
            
    def setSolid(self, solid):
        """
        This method is used to specify whether or not the object is drawn solid or wireframe.

        :param solid: Whether or not the object is drawn solid or wireframe.
        :type solid: Boolean
        """
        
        self.solid = solid
            
    def setTransparentPrimitives(self, transparentPrimitives):
        """
        This method is used to specify the amount of transparent faces.

        :param transparentPrimitives: The amount of transparent faces.
        :type transparentPrimitives: int
        """
        
        self.transparentPrimitives = transparentPrimitives

    def getFaceGroup(self, name):
        """
        This method searches the list of FaceGroups held for this object, and
        returns the FaceGroup with the specified name. If no FaceGroup is found
        for that name, this method returns None.

        :param name: The name of the FaceGroup to retrieve.
        :type name: str
        :return: The FaceGroup if found, None otherwise.
        :rtype: :py:class:`module3d.FaceGroup`
        """

        return self._groups_rev.get(name, None)

    def getGroupMaskForGroups(self, groupNames):
        groups = np.zeros(len(self._faceGroups), dtype=bool)
        for name in groupNames:
            groups[self._groups_rev[name].idx] = True
        return groups

    def getFaceMaskForGroups(self, groupNames):
        groups = self.getGroupMaskForGroups(groupNames)
        face_mask = groups[self.group]
        return face_mask

    def getFacesForGroups(self, groupNames):
        face_mask = self.getFaceMaskForGroups(groupNames)
        faces = np.argwhere(face_mask)[...,0]
        return faces

    def getVertexMaskForGroups(self, groupNames):
        face_mask = self.getFaceMaskForGroups(groupNames)
        verts = self.fvert[face_mask]
        vert_mask = np.zeros(len(self.coord), dtype = bool)
        vert_mask[verts] = True
        return vert_mask

    def getVerticesForGroups(self, groupNames):
        vert_mask = self.getVertexMaskForGroups(groupNames)
        verts = np.argwhere(vert_mask)[...,0]
        return verts

    def getVertexAndFaceMasksForGroups(self, groupNames):
        face_mask = self.getFaceMaskForGroups(groupNames)
        verts = self.fvert[face_mask]
        vert_mask = np.zeros(len(self.coord), dtype = bool)
        vert_mask[verts] = True
        return vert_mask, face_mask

    def getVerticesAndFacesForGroups(self, groupNames):
        vert_mask, face_mask = self.getVertexAndFaceMasksForGroups(groupNames)
        faces = np.argwhere(face_mask)[...,0]
        verts = np.argwhere(vert_mask)[...,0]
        return [VertProxy(self, idx) for idx in verts], [FaceProxy(self, idx) for idx in faces]

    def updateGroups(self, groupnames, recalcNormals=True, update=True):
        if recalcNormals or update:
            (vertices, faces) = self.getVertexAndFaceMasksForGroups(groupnames)
            if recalcNormals:
                self.calcNormals(1, 1, vertices, faces)
            if update:
                self.update(vertices, recalcNormals)

    def getFaceMaskForVertices(self, verts):
        mask = np.zeros(len(self.fvert), dtype = bool)
        valid = np.arange(self.MAX_FACES)[None,:] < self.nfaces[verts][:,None]
        vface = self.vface[verts]
        faces = np.where(valid, vface, vface[:,:1])
        mask[faces] = True
        return mask

    def getFacesForVertices(self, verts):
        return np.argwhere(self.getFaceMaskForVertices(verts))[...,0]

    def setCameraProjection(self, cameraMode):
        """
        This method sets the camera mode used to visualize this object (fixed or movable).
        The 3D engine has two camera modes (both perspective modes).
        The first is moved by the mouse, while the second is fixed.
        The first is generally used to model 3D objects (a human, clothes,
        etc.), while the second is used for 3D GUI controls.

        :param cameraMode: The camera mode. 0 = fixed camera; 1 = movable camera.
        :type cameraMode: int
        """

        self.cameraMode = cameraMode

    def update(self, verticesToUpdate=None, updateNormals=True):
        """
        This method is used to call the update methods on each of a list of vertices or all vertices that form part of this object.

        :param verticesToUpdate: The list of vertices to update.
        :type verticesToUpdate: [:py:class:`module3d.Vert`, ..]
        :param updateNormals: Whether to update the normals as well.
        :type updateNormals: [:py:class:`module3d.Vert`, ..]
        """
        # if verticesToUpdate is not None:
        #     self.markCoords(verticesToUpdate, coor=True)
        self.sync_all()

    def calcNormals(self, recalcVertexNormals=1, recalcFaceNormals=1, verticesToUpdate=None, facesToUpdate=None):
        """
        Updates the given vertex and/or face normals.
        
        :param recalcVertexNormals: A flag to indicate whether or not the vertex normals should be recalculated.
        :type recalcVertexNormals: Boolean
        :param recalcFaceNormals: A flag to indicate whether or not the face normals should be recalculated.
        :type recalcFaceNormals: Boolean
        :param verticesToUpdate: The list of vertices to be updated, if None all vertices are updated.
        :type verticesToUpdate: list of :py:class:`module3d.Vert`
        :param facesToUpdate: The list of faces to be updated, if None all faces are updated.
        :type facesToUpdate: list of :py:class:`module3d.Face`
        """

        if recalcFaceNormals:
            self.calcFaceNormals(facesToUpdate)

        if recalcVertexNormals:
            self.calcVertexNormals(verticesToUpdate)
                
    def calcBBox(self):
        """
        Calculates the axis aligned bounding box of this object in the object's coordinate system. 
        """
        if len(self.coord) == 0:
            return np.zeros((2,3), dtype = np.float32)
        v0 = np.amin(self.coord, axis=0)
        v1 = np.amax(self.coord, axis=0)
        return np.vstack((v0, v1))

    def __str__(self):
        x, y, z = self.loc
        return 'object3D named: %s, nverts: %s, nfaces: %s, at |%s,%s,%s|' % (self.name, len(self.fvert), len(self.vface), x, y, z)

class SelectionColorMap:

    """
    The objects support the use of a technique called *Selection Using Unique
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
    
    - **self.colorIDToFaceGroup**: *Dictionary of colors IDs* A dictionary of the color IDs used for
      selection (see MakeHuman Selectors, above).
    - **self.colorID**: *float list* A progressive color ID.
    
    The attributes *self.colorID* and *self.colorIDToFaceGroup*
    support a technique called *Selection Using Unique Color IDs* to make each
    FaceGroup independently clickable.

    The attribute *self.colorID* stores a progressive color that is incremented for each successive
    FaceGroup added to the scene.
    The *self.colorIDToFaceGroup* attribute contains a list that serves as a directory to map
    each color back to the corresponding FaceGroup by using its color ID.
    """

    def __init__(self):
    
        self.colorIDToFaceGroup = {}
        self.colorID = 0

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

        :param obj: The object3D object for which color dictionary entries need to be generated.
        :type obj: module3d.Object 3D
        """

        # print "DEBUG COLOR AND GROUPS, obj", obj.name
        # print "---------------------------"

        for g in obj.faceGroups:
            self.colorID += 1

            # 555 to 24-bit rgb

            idR = (self.colorID % 32) * 8
            idG = ((self.colorID >> 5) % 32) * 8
            idB = ((self.colorID >> 10) % 32) * 8

            g.colorID = (idR, idG, idB)
            
            self.colorIDToFaceGroup[self.colorID] = g

            # print "SELECTION DEBUG INFO: facegroup %s of obj %s has the colorID = %s,%s,%s or %s"%(g.name,obj.name,idR,idG,idB, self.colorID)

    def getSelectedFaceGroup(self):
        """
        This method uses a non-displayed image containing color-coded faces
        to return the index of the FaceGroup selected by the user with the mouse.
        This is part of a technique called *Selection Using Unique Color IDs* to make each
        FaceGroup independently clickable.

        :return: The selected face group.
        :rtype: :py:class:`module3d.FaceGroup`
        """

        picked = mh.getColorPicked()

        IDkey = picked[0] / 8 | picked[1] / 8 << 5 | picked[2] / 8 << 10  # 555

        # print "DEBUG COLOR PICKED: %s,%s,%s %s"%(picked[0], picked[1], picked[2], IDkey)

        try:
            groupSelected = self.colorIDToFaceGroup[IDkey]
        except:

            # print groupSelected.name
            #this print should only come on while debugging color picking
            #print 'Color %s (%s) not found' % (IDkey, picked)
            groupSelected = None
        return groupSelected

    def getSelectedFaceGroupAndObject(self):
        """
        This method determines whether a FaceGroup or a non-selectable zone has been
        clicked with the mouse. It returns a tuple, showing the FaceGroup and the parent
        Object3D object, or None.
        If no object is picked, this method will simply print \"no clickable zone.\"

        :return: The selected face group and object.
        :rtype: (:py:class:`module3d.FaceGroup`, :py:class:`module3d.Object3d`)
        """

        facegroupPicked = self.getSelectedFaceGroup()
        if facegroupPicked:
            objPicked = facegroupPicked.parent
            return (facegroupPicked, objPicked)
        else:
            #this print should only be made while debugging picking
            #print 'not a clickable zone'
            return None
    
selectionColorMap = SelectionColorMap()
