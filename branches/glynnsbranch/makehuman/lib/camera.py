from OpenGL.GL import *
from OpenGL.GLU import *
from object3d import Object3D
import glmodule as gl

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

    def getTransform(self):
	gl.cameraPosition(self, 0)
        matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
	return tuple(matrix)

    transform = property(getTransform, None, None, "The transform of the camera.")

    def convertToScreen(self, x, y, z, obj = None):
        "Convert 3D OpenGL world coordinates to screen coordinates."
        world = x, y, z

        gl.cameraPosition(self, 0)

        if obj and isinstance(obj, Object3D):
            glPushMatrix()
            glTranslatef(obj.x, obj.y, obj.z)
            glRotatef(obj.rx, 1, 0, 0)
            glRotatef(obj.ry, 0, 1, 0)
            glRotatef(obj.rz, 0, 0, 1)
            glScalef(obj.sx, obj.sy, obj.sz)

        viewport = glGetIntegerv(GL_VIEWPORT)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)

        if obj and isinstance(obj, Object3D):
            glPopMatrix()

        sx, sy, sz = gluProject(x, y, z, modelview, projection, viewport)
        sy = viewport[3] - sy

        return [sx, sy, sz]

    def convertToWorld2D(self, sx, sy):
        "Convert 2D (x, y) screen coordinates to OpenGL world coordinates."

        gl.cameraPosition(self, 0);

        viewport = glGetIntegerv(GL_VIEWPORT)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)

        sy = viewport[3] - sy

        sz = c_double(0)
        glReadPixels(sx, sy, 1, 1, GL_DEPTH_COMPONENT, GL_DOUBLE, byref(sz))

        world = gluUnProject(sx, sy, sz, modelview, projection, viewport)

        return list(world)

    def convertToWorld3D(self, sx, sy, sz):
        "Convert 3D (x, y, depth) screen coordinates to 3D OpenGL world coordinates."

        gl.cameraPosition(self, 0);

        viewport = glGetIntegerv(GL_VIEWPORT)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)

        sy = viewport[3] - sy

        world = gluUnProject(sx, sy, sz, modelview, projection, viewport)

        return list(world)
