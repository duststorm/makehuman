import math
import numpy as np
import glmodule as gl
from core import G

class Object3D(object):
    def __init__(self, parent):
        self.parent = parent

        self.texture = 0
        self.uniforms = None

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
        return gl.objectTransform(self)

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
    def shader(self):
        return self.parent.shader

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

        cx = camera.eyeX
        cy = camera.eyeY
        cz = camera.eyeZ

        indices = self.primitives[self.nPrimitives - self.nTransparentPrimitives:]

        # Rotate camera position according to object position
        # This is less costly that transforming all points
        cx -= self.x
        cy -= self.y
        cz -= self.z

        # Rotate X
        alpha = math.radians(-self.rx)
        c = math.cos(alpha)
        s = math.sin(alpha)
        tx = cx
        ty = cy*c - cz*s
        tz = cy*s + cz*c

        # Rotate Y
        alpha = math.radians(-self.ry)
        c = math.cos(alpha)
        s = math.sin(alpha)
        cx = tz*s + tx*c
        cy = ty
        cz = tz*c - tx*s

        # Rotate Z
        alpha = math.radians(-self.rz)
        c = math.cos(alpha)
        s = math.sin(alpha)
        tx = cx*c - cy*s
        ty = cx*s + cy*c
        tz = cz

        cx = tx + self.x
        cy = ty + self.y
        cz = tz + self.z

        # Prepare sorting data
        verts = self.verts[self.primitives] - (cx, cy, cz)
        distances = np.sum(verts ** 2, axis = -1)
        distances = np.amin(distances, axis = -1)
        distances = -distances
        # Sort
        order = np.argsort(distances)
        indices2 = indices[order,:]

        indices[...] = indices2
