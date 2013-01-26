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

import events3d
from core import G
import glmodule as gl
import matrix

class Camera(events3d.EventHandler):
    def __init__(self):
        super(Camera, self).__init__()

        self.changedPending = False

        self._fovAngle = 25.0
        self._nearPlane = 0.1
        self._farPlane = 100.0
        self._projection = 1
        self._stereoMode = 0
        self._eyeX = 0.0
        self._eyeY = 0.0
        self._eyeZ = 60.0
        self._focusX = 0.0
        self._focusY = 0.0
        self._focusZ = 0.0
        self._upX = 0.0
        self._upY = 1.0
        self._upZ = 0.0
        self._scale = 1.0

        self.eyeSeparation = 1.0

    def changed(self):
        self.callEvent('onChanged', self)
        self.changedPending = False

    def getProjection(self):
        return self._projection

    def setProjection(self, value):
        self._projection = value
        self.changed()

    projection = property(getProjection, setProjection)

    def getFovAngle(self):
        return self._fovAngle

    def setFovAngle(self, value):
        self._fovAngle = value
        self.changed()

    fovAngle = property(getFovAngle, setFovAngle)

    def getNearPlane(self):
        return self._nearPlane

    def setNearPlane(self, value):
        self._nearPlane = value
        self.changed()

    nearPlane = property(getNearPlane, setNearPlane)

    def getFarPlane(self):
        return self._farPlane

    def setFarPlane(self, value):
        self._farPlane = value
        self.changed()

    farPlane = property(getFarPlane, setFarPlane)

    def getEyeX(self):
        return self._eyeX

    def setEyeX(self, value):
        self._eyeX = value
        self.changed()

    eyeX = property(getEyeX, setEyeX)

    def getEyeY(self):
        return self._eyeY

    def setEyeY(self, value):
        self._eyeY = value
        self.changed()

    eyeY = property(getEyeY, setEyeY)

    def getEyeZ(self):
        return self._eyeZ

    def setEyeZ(self, value):
        self._eyeZ = value
        self.changed()

    eyeZ = property(getEyeZ, setEyeZ)

    def getEye(self):
        return (self._eyeX, self._eyeY, self._eyeZ)

    def setEye(self, xyz):
        (self._eyeX, self._eyeY, self._eyeZ) = xyz
        self.changed()

    eye = property(getEye, setEye)

    def getFocusX(self):
        return self._focusX

    def setFocusX(self, value):
        self._focusX = value
        self.changed()

    focusX = property(getFocusX, setFocusX)

    def getFocusY(self):
        return self._focusY

    def setFocusY(self, value):
        self._focusY = value
        self.changed()

    focusY = property(getFocusY, setFocusY)

    def getFocusZ(self):
        return self._focusZ

    def setFocusZ(self, value):
        self._focusZ = value
        self.changed()

    focusZ = property(getFocusZ, setFocusZ)

    def getFocus(self):
        return (self._focusX, self._focusY, self._focusZ)

    def setFocus(self, xyz):
        (self._focusX, self._focusY, self._focusZ) = xyz
        self.changed()

    focus = property(getFocus, setFocus)

    def getUpX(self):
        return self._upX

    def setUpX(self, value):
        self._upX = value
        self.changed()

    upX = property(getUpX, setUpX)

    def getUpY(self):
        return self._upY

    def setUpY(self, value):
        self._upY = value
        self.changed()

    upY = property(getUpY, setUpY)

    def getUpZ(self):
        return self._upZ

    def setUpZ(self, value):
        self._upZ = value
        self.changed()

    upZ = property(getUpZ, setUpZ)

    def getUp(self):
        return (self._upX, self._upY, self._upZ)

    def setUp(self, xyz):
        (self._upX, self._upY, self._upZ) = xyz
        self.changed()

    up = property(getUp, setUp)

    def getScale(self):
        return self._scale

    def setScale(self, value):
        self._scale = value
        self.changed()

    scale = property(getScale, setScale)

    def getStereoMode(self):
        return self._stereoMode

    def setStereoMode(self, value):
        self._stereoMode = value
        self.changed()

    stereoMode = property(getStereoMode, setStereoMode)

    def switchToOrtho(self):
        fov = math.tan(self.fovAngle * 0.5 * math.pi / 180.0)
        delta = np.array(self.eye) - np.array(self.focus)
        scale = math.sqrt(np.sum(delta ** 2)) * fov

        self._projection = 0
        self._scale = scale
        self._nearPlane = -100.0
        self.changed()

    def switchToPerspective(self):
        self._projection = 1
        self._nearPlane = 0.1
        self.changed()

    def getMatrices(self, eye):
        def lookat(ex, ey, ez, tx, ty, tz, ux, uy, uz):
            e = np.array([ex, ey, ez])
            t = np.array([tx, ty, tz])
            u = np.array([ux, uy, uz])
            return matrix.lookat(e, t, u)

        stereoMode = 0
        if eye:
            stereoMode = self.stereoMode

        aspect = float(max(1, G.windowWidth)) / float(max(1, G.windowHeight))

        if stereoMode == 0:
            # No stereo
            if self.projection:
                proj = matrix.perspective(self.fovAngle, aspect, self.nearPlane, self.farPlane)
            else:
                height = self.scale
                width = self.scale * aspect
                proj = matrix.ortho(-width, width, -height, height, self.nearPlane, self.farPlane)

            mv = lookat(self.eyeX, self.eyeY, self.eyeZ,       # Eye
                        self.focusX, self.focusY, self.focusZ, # Focus
                        self.upX, self.upY, self.upZ)          # Up
        elif stereoMode == 1:
            # Toe-in method, uses different eye positions, same focus point and projection
            proj = matrix.perspective(self.fovAngle, aspect, self.nearPlane, self.farPlane)

            if eye == 1:
                mv = lookat(self.eyeX - 0.5 * self.eyeSeparation, self.eyeY, self.eyeZ, # Eye
                            self.focusX, self.focusY, self.focusZ,                      # Focus
                            self.upX, self.upY, self.upZ)                               # Up
            elif eye == 2:
                mv = lookat(self.eyeX + 0.5 * self.eyeSeparation, self.eyeY, self.eyeZ, # Eye
                            self.focusX, self.focusY, self.focusZ,                      # Focus
                            self.upX, self.upY, self.upZ)                               # Up
        elif stereoMode == 2:
            # Off-axis method, uses different eye positions, focus points and projections
            widthdiv2 = math.tan(math.radians(self.fovAngle) / 2) * self.nearPlane
            left  = - aspect * widthdiv2
            right = aspect * widthdiv2
            top = widthdiv2
            bottom = -widthdiv2

            if eye == 1:        # Left
                eyePosition = -0.5 * self.eyeSeparation
            elif eye == 2:      # Right
                eyePosition = 0.5 * self.eyeSeparation
            else:
                eyePosition = 0.0

            left -= eyePosition * self.nearPlane / self.eyeZ
            right -= eyePosition * self.nearPlane / self.eyeZ

            # Left frustum is moved right, right frustum moved left
            proj = matrix.frustum(left, right, bottom, top, self.nearPlane, self.farPlane)

            # Left camera is moved left, right camera moved right
            mv = lookat(self.eyeX + eyePosition, self.eyeY, self.eyeZ,       # Eye
                        self.focusX + eyePosition, self.focusY, self.focusZ, # Focus
                        self.upX, self.upY, self.upZ)                        # Up

        return proj, mv

    def getTransform(self):
        _, mv = self.getMatrices(0)
        return tuple(np.asarray(mv).flat)

    transform = property(getTransform, None, None, "The transform of the camera.")

    @staticmethod
    def getFlipMatrix():
        t = matrix.translate((0, G.windowHeight, 0))
        s = matrix.scale((1,-1,1))
        return t * s

    def getConvertToScreenMatrix(self, obj = None):
        viewport = matrix.viewport(0, 0, G.windowWidth, G.windowHeight)
        projection, modelview = self.getMatrices(0)
        m = viewport * projection * modelview
        if obj:
            m = m * obj.transform
        return self.getFlipMatrix() * m

    def convertToScreen(self, x, y, z, obj = None):
        "Convert 3D OpenGL world coordinates to screen coordinates."
        m = self.getConvertToScreenMatrix(obj)
        sx, sy, sz = matrix.transform3(m, [x, y, z])
        return [sx, sy, sz]

    def convertToWorld2D(self, sx, sy, obj = None):
        "Convert 2D (x, y) screen coordinates to OpenGL world coordinates."
        sz = gl.queryDepth(sx, sy)
        return convertToWorld3D(sx, sy, sz, obj)

    def convertToWorld3D(self, sx, sy, sz, obj = None):
        "Convert 3D (x, y, depth) screen coordinates to 3D OpenGL world coordinates."
        m = self.getConvertToScreenMatrix(obj)
        x, y, z = matrix.transform3(m.I, [sx, sy, sz])
        return [x, y, z]
