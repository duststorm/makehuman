from core import G
from getpath import getPath
import glmodule as gl

import qtui as ui

from image import Image
from texture import Texture
from object3d import Object3D
from camera import Camera

cameras = G.cameras

Keys = ui.Keys
Buttons = ui.Buttons
Modifiers = ui.Modifiers

def updatePickingBuffer():
    gl.updatePickingBuffer()

def getColorPicked():
    return G.color_picked

def getKeyModifiers():
    return ui.getKeyModifiers()

def setCaption(caption):
    ui.setCaption(caption)

def setClearColor(r, g, b, a):
    G.clearColor = (r, g, b, a)

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

Application = ui.Application

def setCaption(caption):
    G.app.mainwin.setWindowTitle(caption)

def removeWidget(edge, widget):
    return G.app.mainwin.removeWidget(edge, widget)

def changeCategory(category):
    G.app.mainwin.tabs.changeTab(category)

def changeTask(category, task):
    changeCategory(category)
    G.app.mainwin.tabs.findTab(category).child.changeTab(task)

def refreshLayout():
    G.app.mainwin.refreshLayout()

def addPanels():
    return G.app.mainwin.addPanels()

def showPanels(left, right):
    return G.app.mainwin.showPanels(left, right)

def addPanelBottomLeft():
    return G.app.mainwin.addPanelBottomLeft()

def showPanelBottomLeft(panel):
    return G.app.mainwin.showPanelBottomLeft(panel)

def getPanelBottomRight():
    return G.app.mainwin.getPanelBottomRight()

def addTopWidget(widget, *args, **kwargs):
    return G.app.mainwin.addTopWidget(widget, *args, **kwargs)

def removeTopWidget(widget):
    return G.app.mainwin.removeTopWidget(widget)

def addObject(obj):
    G.world.append(obj)

def removeObject(obj):
    G.world.remove(obj)

def setShortcut(modifier, key, method):
    G.app.mainwin.setShortcut(modifier, key, method)
