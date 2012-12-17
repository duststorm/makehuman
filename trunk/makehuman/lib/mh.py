import sys
import os
if sys.platform == 'win32':
    import _winreg
from core import G
import glmodule as gl

import qtui as ui

from image import Image
from texture import Texture
from object3d import Object3D
from camera import Camera

world = G.world
cameras = G.cameras

Keys = ui.Keys
Buttons = ui.Buttons
Modifiers = ui.Modifiers

def updatePickingBuffer():
    gl.updatePickingBuffer()

def getColorPicked():
    return G.color_picked

def getMousePos():
    if G.mouse_pos is None:
        return 0, 0
    return G.mouse_pos

def getKeyModifiers():
    return ui.getKeyModifiers()

def getWindowSize():
    return G.windowWidth, G.windowHeight

def startWindow(useTimer = False):
    ui.createWindow(useTimer)

def startEventLoop():
    ui.eventLoop()

def shutDown():
    ui.shutDown()

def redraw(async):
    if async:
        ui.queueUpdate()
    else:
        gl.draw()

def drawOneMesh(obj):
    gl.drawOneMesh(obj.object3d)

def setFullscreen(fullscreen):
    ui.setFullscreen(fullscreen)

def setCaption(caption):
    ui.setCaption(caption)

def setClearColor(r, g, b, a):
    gl.setClearColor(r, g, b, a);

def createVertexShader(source):
    return gl.createVertexShader(source)

def createFragmentShader(source):
    return gl.createFragmentShader(source)

def createShader(vertexShader, fragmentShader):
    return gl.createShader(vertexShader, fragmentShader)

def grabScreen(x, y, width, height, path):
    gl.grabScreen(x, y, width, height, path)

def addTimer(milliseconds, callback):
    return ui.addTimer(milliseconds, callback)

def removeTimer(id):
    ui.removeTimer(id)

def callAsync(callback):
    ui.callAsync(callback)

def setResizeCallback(callback):
    G.resizeCallback = callback

def setMouseDownCallback(callback):
    G.mouseDownCallback = callback

def setMouseUpCallback(callback):
    G.mouseUpCallback = callback

def setMouseWheelCallback(callback):
    G.mouseWheelCallback = callback

def setMouseMovedCallback(callback):
    G.mouseMovedCallback = callback

def setKeyDownCallback(callback):
    G.keyDownCallback = callback

def setKeyUpCallback(callback):
    G.keyUpCallback = callback

def setQuitCallback(callback):
    G.quitCallback = callback

def getPath(type):
    if isinstance(type, (str, unicode)):
        typeStr = str(type)
    elif type is None:
        typeStr = ""
    else:
        raise TypeError("String expected")

    if sys.platform == 'win32':
        keyname = r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'
        name = 'Personal'
        k = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyname)
        value, type = _winreg.QueryValueEx(k, 'Personal')
        if type == _winreg.REG_EXPAND_SZ:
            path = _winreg.ExpandEnvironmentStrings(value)
        elif type == _winreg.REG_SZ:
            path = value
        else:
            raise RuntimeError("Couldn't determine user folder")

        if typeStr == "exports":
            path += u"\\makehuman\\exports\\"
        elif typeStr == "models":
            path += u"\\makehuman\\models\\"
        elif typeStr == "grab":
            path += u"\\makehuman\\grab\\"
        elif typeStr == "render":
            path += u"\\makehuman\\render\\"
        elif typeStr == "":
            path += u"\\makehuman\\"
        else:
            raise ValueError("Unknown value '%s' for getPath()!" % typeStr)
    else:
        path = os.path.expanduser('~')
        if sys.platform.startswith("darwin"): 
            path = os.path.join(path,"Documents")
            path = os.path.join(path,"MakeHuman")
        else:
            path = os.path.join(path,"makehuman")

        if typeStr == "exports":
            path += "/exports/"
        elif typeStr == "models":
            path += "/models/"
        elif typeStr == "grab":
            path += "/grab/"
        elif typeStr == "render":
            path += "/render/"
        elif typeStr == "":
            path += "/"
        else:
            raise ValueError("Unknown property '%s' for getPath()!" % typeStr);

    return path
