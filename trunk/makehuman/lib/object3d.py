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

import math
import numpy as np
import glmodule as gl
import texture
import shader
import matrix
import log
from core import G

class Object3D(object):
    def __init__(self, parent):
        self.parent = parent
        self._texturePath = None
        self._textureTex = None
        self._shaderPath = None
        self._shaderObj = None

    @property
    def verts(self):
        return self.parent.r_coord

    @property
    def norms(self):
        return self.parent.r_vnorm

    @property
    def color(self):
        return self.parent.r_color

    @property
    def UVs(self):
        return self.parent.r_texco

    @property
    def primitives(self):
        return self.parent.index

    @property
    def nPrimitives(self):
        return len(self.primitives)

    @property
    def groups(self):
        return self.parent.grpix

    @property
    def shadeless(self):
        return self.parent.shadeless

    @property
    def depthless(self):
        return self.parent.depthless

    @property
    def vertsPerPrimitive(self):
        return self.parent.vertsPerPrimitive

    @property
    def shaderParameters(self):
        return self.parent.shaderParameters

    @property
    def visibility(self):
        return self.parent.visibility

    @property
    def cameraMode(self):
        return self.parent.cameraMode

    @property
    def pickable(self):
        return self.parent.pickable

    @property
    def solid(self):
        return self.parent.solid

    @property
    def translation(self):
        return self.parent.loc[:]

    @property
    def rotation(self):
        return self.parent.rot[:]

    @property
    def scale(self):
        return self.parent.scale[:]

    @property
    def nTransparentPrimitives(self):
        return self.parent.transparentPrimitives

    @property
    def transform(self):
        return self.parent.transform

    @property
    def x(self):
        return self.parent.x

    @property
    def y(self):
        return self.parent.y

    @property
    def z(self):
        return self.parent.z

    @property
    def rx(self):
        return self.parent.rx

    @property
    def ry(self):
        return self.parent.ry

    @property
    def rz(self):
        return self.parent.rz

    @property
    def sx(self):
        return self.parent.sx

    @property
    def sy(self):
        return self.parent.sy

    @property
    def sz(self):
        return self.parent.sz

    @property
    def shaderObj(self):
        if not shader.Shader.supported():
            return None
        if self._shaderPath != self.parent.shader:
            self._shaderObj = None
        if self._shaderObj is False:
            return None
        if self._shaderObj is None:
            self._shaderPath = self.parent.shader
            if self._shaderPath is None:
                self._shaderObj = None
            else:
                self._shaderObj = shader.getShader(self._shaderPath)
        if self._shaderObj is False:
            return None
        return self._shaderObj

    @property
    def shader(self):
        if self.shaderObj is None:
            return 0
        return self.shaderObj.shaderId

    @property
    def priority(self):
        return self.parent.priority

    @property
    def cull(self):
        return self.parent.cull

    def clrid(self, idx):
        return self.parent._faceGroups[idx].colorID

    def gcolor(self, idx):
        return self.parent._faceGroups[idx].color

    def draw(self, *args, **kwargs):
        return gl.drawMesh(self, *args, **kwargs)

    def pick(self, *args, **kwargs):
        return gl.pickMesh(self, *args, **kwargs)

    def sortFaces(self):
        camera = G.cameras[0]

        indices = self.primitives[self.nPrimitives - self.nTransparentPrimitives:]

        m = matrix.translate(-self.translation)
        m = matrix.rotx(-self.rx) * m
        m = matrix.roty(-self.ry) * m
        m = matrix.rotz(-self.rz) * m
        m = matrix.translate(self.translation) * m
        cxyz = matrix.transform3(m, camera.eye)

        # Prepare sorting data
        verts = self.verts[self.primitives] - cxyz
        distances = np.sum(verts ** 2, axis = -1)
        distances = np.amin(distances, axis = -1)
        distances = -distances
        # Sort
        order = np.argsort(distances)
        indices2 = indices[order,:]

        indices[...] = indices2

    @property
    def textureTex(self):
        if self._texturePath != self.parent.texture:
            self._textureTex = None
        if self._textureTex is False:
            return None
        if self._textureTex is None:
            self._texturePath = self.parent.texture
            if self._texturePath is None:
                self._textureTex = None
            else:
                self._textureTex = texture.getTexture(self._texturePath)
        if self._textureTex is False:
            return None
        return self._textureTex

    @property
    def texture(self):
        if self.textureTex is None:
            return 0
        return self.textureTex.textureId

    @classmethod
    def attach(cls, mesh):
        if mesh.object3d:
            log.debug('mesh is already attached')
            return

        mesh.object3d = cls(mesh)
        G.world.append(mesh.object3d)

    @classmethod
    def detach(cls, mesh):
        if not mesh.object3d:
            log.debug('mesh is not attached')
            return

        G.world.remove(mesh.object3d)
        mesh.object3d = None
