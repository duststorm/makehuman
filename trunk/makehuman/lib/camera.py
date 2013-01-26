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
from core import G
import glmodule as gl
import matrix

class Camera(object):
    def __new__(cls, *args, **kwargs):
        self = super(Camera, cls).__new__(cls)

        self.fovAngle = 25.0
        self.nearPlane = 0.1
        self.farPlane = 100.0

        self.projection = 1

        self.stereoMode = 0
        self.eyeSeparation = 1.0

        self.eyeX = 0.0
        self.eyeY = 0.0
        self.eyeZ = 60.0
        self.focusX = 0.0
        self.focusY = 0.0
        self.focusZ = 0.0
        self.upX = 0.0
        self.upY = 1.0
        self.upZ = 0.0
        self.scale = 1.0

        return self

    def __init__(self, path = None):
        pass

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

    def getEye(self):
        return (self.eyeX, self.eyeY, self.eyeZ)

    def setEye(self, eye):
        (self.eyeX, self.eyeY, self.eyeZ) = eye

    eye = property(getEye, setEye)

    def getFocus(self):
        return (self.focusX, self.focusY, self.focusZ)

    def setFocus(self, focus):
        (self.focusX, self.focusY, self.focusZ) = focus

    focus = property(getFocus, setFocus)

    def getUp(self):
        return (self.upX, self.upY, self.upZ)

    def setUp(self, up):
        (self.upX, self.upY, self.upZ) = up

    up = property(getUp, setUp)
