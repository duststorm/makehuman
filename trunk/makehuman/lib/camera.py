import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from core import G
from object3d import Object3D
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
        self.left = 0.0
        self.right = 0.0
        self.bottom = 0.0
        self.top = 0.0

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

        if stereoMode == 0:
            # No stereo
            if self.projection:
                proj = matrix.perspective(self.fovAngle, float(max(1, G.windowWidth)) / float(max(1, G.windowHeight)), self.nearPlane, self.farPlane)
            elif self.left == self.right and self.top == self.bottom:
                proj = matrix.ortho(0.0, max(1, G.windowWidth), max(1, G.windowHeight), 0.0, self.nearPlane, self.farPlane)
            else:
                proj = matrix.ortho(self.left, self.right, self.bottom, self.top, self.nearPlane, self.farPlane)

            mv = lookat(self.eyeX, self.eyeY, self.eyeZ,       # Eye
                        self.focusX, self.focusY, self.focusZ, # Focus
                        self.upX, self.upY, self.upZ)          # Up
        elif stereoMode == 1:
            # Toe-in method, uses different eye positions, same focus point and projection
            proj = matrix.perspective(self.fovAngle, float(max(1, G.windowWidth)) / float(max(1, G.windowHeight)), self.nearPlane, self.farPlane)

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
            aspectratio = float(max(1, G.windowWidth)) / float(max(1, G.windowHeight))
            widthdiv2 = math.tan(math.radians(self.fovAngle) / 2) * self.nearPlane
            left  = - aspectratio * widthdiv2
            right = aspectratio * widthdiv2
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

    def convertToScreen(self, x, y, z, obj = None):
        "Convert 3D OpenGL world coordinates to screen coordinates."
        world = x, y, z

        viewport = matrix.viewport(0, 0, G.windowWidth, G.windowHeight)
        projection, modelview = self.getMatrices(0)

        if obj and isinstance(obj, Object3D):
            m = modelview
            m = m * matrix.translate((obj.x, obj.y, obj.z))
            m = m * matrix.rotx(obj.rx)
            m = m * matrix.roty(obj.ry)
            m = m * matrix.rotz(obj.rz)
            m = m * matrix.scale((obj.sx, obj.sy, obj.sz))
            modelview = m

        m = viewport * projection * modelview

        sx, sy, sz = matrix.transform3(m, [x, y, z])

        sy = G.windowHeight - sy

        return [sx, sy, sz]

    def convertToWorld2D(self, sx, sy):
        "Convert 2D (x, y) screen coordinates to OpenGL world coordinates."

        viewport = matrix.viewport(0, 0, G.windowWidth, G.windowHeight)
        projection, modelview = self.getMatrices(0)

        sy = G.windowHeight - sy

        sz = c_double(0)
        glReadPixels(sx, sy, 1, 1, GL_DEPTH_COMPONENT, GL_DOUBLE, byref(sz))
        sz = sz.value

        m = viewport * projection * modelview
        x, y, z = matrix.transform3(m.I, [sx, sy, sz])

        return [x, y, z]

    def convertToWorld3D(self, sx, sy, sz):
        "Convert 3D (x, y, depth) screen coordinates to 3D OpenGL world coordinates."

        viewport = matrix.viewport(0, 0, G.windowWidth, G.windowHeight)
        projection, modelview = self.getMatrices(0)

        sy = G.windowHeight - sy

        m = viewport * projection * modelview

        x, y, z = matrix.transform3(m.I, [sx, sy, sz])

        return [x, y, z]
