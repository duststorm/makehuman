import events3d
import mh

class Camera(events3d.EventHandler):

    def __init__(self, app):
        self.app = app
        self.camera = mh.Camera()
        self.changedPending = False
        
    def getProjection(self):
    
        return self.camera.projection

    def setProjection(self, value):
    
        self.camera.projection = value
        self.changed()
        
    projection = property(getProjection, setProjection)
        
    def getFovAngle(self):
    
        return self.camera.fovAngle

    def setFovAngle(self, value):
    
        self.camera.fovAngle = value
        self.changed()
        
    fovAngle = property(getFovAngle, setFovAngle)
    
    def getNearPlane(self):
    
        return self.camera.nearPlane

    def setNearPlane(self, value):
    
        self.camera.nearPlane = value
        self.changed()
        
    nearPlane = property(getNearPlane, setNearPlane)
    
    def getFarPlane(self):
    
        return self.camera.farPlane

    def setFarPlane(self, value):
    
        self.camera.farPlane = value
        self.changed()
        
    farPlane = property(getFarPlane, setFarPlane)
    
    def getEyeX(self):
    
        return self.camera.eyeX

    def setEyeX(self, value):
    
        self.camera.eyeX = value
        self.changed()
        
    eyeX = property(getEyeX, setEyeX)
        
    def getEyeY(self):
    
        return self.camera.eyeY

    def setEyeY(self, value):
    
        self.camera.eyeY = value
        self.changed()
        
    eyeY = property(getEyeY, setEyeY)
    
    def getEyeZ(self):
    
        return self.camera.eyeZ

    def setEyeZ(self, value):
    
        self.camera.eyeZ = value
        if self.camera.projection == 0:
            self.switchToOrtho()
        self.changed()
        
    eyeZ = property(getEyeZ, setEyeZ)
    
    @property
    def eye(self):
        return (self.camera.eyeX, self.camera.eyeY, self.camera.eyeZ)
        
    def getFocusX(self):
    
        return self.camera.focusX

    def setFocusX(self, value):
    
        self.camera.focusX = value
        self.changed()
        
    focusX = property(getFocusX, setFocusX)
        
    def getFocusY(self):
    
        return self.camera.focusY

    def setFocusY(self, value):
    
        self.camera.focusY = value
        self.changed()
        
    focusY = property(getFocusY, setFocusY)
    
    def getFocusZ(self):
    
        return self.camera.focusZ

    def setFocusZ(self, value):
    
        self.camera.focusZ = value
        if self.camera.projection == 0:
            self.switchToOrtho()
        self.changed()
        
    focusZ = property(getFocusZ, setFocusZ)
    
    @property
    def focus(self):
        return (self.camera.focusX, self.camera.focusY, self.camera.focusZ)
    
    def getUpX(self):
    
        return self.camera.upX

    def setUpX(self, value):
    
        self.camera.upX = value
        self.changed()
        
    upX = property(getUpX, setUpX)
        
    def getUpY(self):
    
        return self.camera.upY

    def setUpY(self, value):
    
        self.camera.upY = value
        self.changed()
        
    upY = property(getUpY, setUpY)
    
    def getUpZ(self):
    
        return self.camera.upZ

    def setUpZ(self, value):
    
        self.camera.upZ = value
        self.changed()
        
    upZ = property(getUpZ, setUpZ)
    
    @property
    def focus(self):
        return (self.camera.upX, self.camera.upY, self.camera.upZ)
        
    def getLeft(self):
    
        return self.camera.left

    def setLeft(self, value):
    
        self.camera.left = value
        self.changed()
        
    left = property(getLeft, setLeft)
    
    def getRight(self):
    
        return self.camera.right

    def setRight(self, value):
    
        self.camera.right = value
        self.changed()
        
    right = property(getRight, setRight)
    
    def getBottom(self):
    
        return self.camera.bottom

    def setBottom(self, value):
    
        self.camera.bottom = value
        self.changed()
        
    bottom = property(getBottom, setBottom)
    
    def getTop(self):
    
        return self.camera.top

    def setTop(self, value):
    
        self.camera.top = value
        self.changed()
        
    top = property(getTop, setTop)
    
    def getStereoMode(self):
    
        return self.camera.stereoMode

    def setStereoMode(self, value):
    
        self.camera.stereoMode = value
        self.changed()
        
    stereoMode = property(getStereoMode, setStereoMode)
        
    def convertToScreen(self, x, y, z, obj=None):
    
        return self.camera.convertToScreen(x, y, z, obj)
        
    def convertToWorld3D(self, x, y, z):
    
        return self.camera.convertToWorld3D(x, y, z)
        
    def changed(self):
        
        if self.changedPending:
            return
            
        self.changedPending = True
        mh.callAsync(self.callChanged)
        
    def callChanged(self):
    
        self.callEvent('onChanged', self)
        self.changedPending = False
        
    def switchToOrtho(self):
    
        self.camera.projection = 0
        
        self.camera.nearPlane = 0.001
            
        width, height = self.app.getWindowSize()
        aspect = float(width) / float(height)
        fov = tan(self.camera.fovAngle * 0.5 * pi / 180.0)
        y = vdist(self.eye, self.focus) * fov
        x = y * aspect
        
        self.camera.left = -x
        self.camera.right = x
        self.camera.bottom = -y
        self.camera.top = y
        
        self.camera.nearPlane = -100.0
        
    def switchToPerspective(self):
    
        self.camera.projection = 0

