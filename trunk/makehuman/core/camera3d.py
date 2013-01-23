#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers, Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import math
import events3d
import mh
import aljabr

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
        self.changed()
        
    eyeZ = property(getEyeZ, setEyeZ)

    def getEye(self):
        return (self.camera.eyeX, self.camera.eyeY, self.camera.eyeZ)
    
    def setEye(self, xyz):
        (self.camera.eyeX, self.camera.eyeY, self.camera.eyeZ) = xyz
        self.changed()

    eye = property(getEye, setEye)

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
        self.changed()
        
    focusZ = property(getFocusZ, setFocusZ)
    
    def getFocus(self):
        return (self.camera.focusX, self.camera.focusY, self.camera.focusZ)

    def setFocus(self, xyz):
        (self.camera.focusX, self.camera.focusY, self.camera.focusZ) = xyz
        self.changed()
        
    focus = property(getFocus, setFocus)

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
    
    def getUp(self):
        return (self.camera.upX, self.camera.upY, self.camera.upZ)

    def setUp(self, xyz):
        (self.camera.upX, self.camera.upY, self.camera.upZ) = xyz
        self.changed()

    up = property(getUp, setUp)

    def getScale(self):
        return self.camera.scale

    def setScale(self, value):
        self.camera.scale = value
        self.changed()

    scale = property(getScale, setScale)

    def getStereoMode(self):
    
        return self.camera.stereoMode

    def setStereoMode(self, value):
    
        self.camera.stereoMode = value
        self.changed()
        
    stereoMode = property(getStereoMode, setStereoMode)
        
    def convertToScreen(self, x, y, z, obj=None):
        return self.camera.convertToScreen(x, y, z, obj)
        
    def convertToWorld3D(self, x, y, z, obj=None):
        return self.camera.convertToWorld3D(x, y, z, obj)
        
    def convertToWorld2D(self, x, y, z, obj=None):
        return self.camera.convertToWorld2D(x, y, z, obj)

    def changed(self):
        self.callEvent('onChanged', self)
        self.changedPending = False
        
    def switchToOrtho(self):
        fov = math.tan(self.camera.fovAngle * 0.5 * math.pi / 180.0)
        scale = aljabr.vdist(self.eye, self.focus) * fov

        self.camera.projection = 0
        self.camera.scale = scale
        self.camera.nearPlane = -100.0
        
    def switchToPerspective(self):
    
        self.camera.projection = 1
        self.camera.nearPlane = 0.1
