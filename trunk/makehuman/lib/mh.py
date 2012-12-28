from core import G
from getpath import getPath
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

def addWidget(edge, widget, *args, **kwargs):
    return ui.addWidget(edge, widget, *args, **kwargs)

def removeWidget(edge, widget):
    return ui.removeWidget(edge, widget)

def addPanels():
    return ui.addPanels()

def showPanels(left, right):
    return ui.showPanels(left, right)

class Frame:
    Bottom      = ui.Frame.Bottom
    Top         = ui.Frame.Top
    LeftBottom  = ui.Frame.LeftBottom
    RightBottom = ui.Frame.RightBottom

def changeCategory(category):
    ui.changeCategory(category)

def changeTask(category, task):
    ui.changeCategory(category)
    ui.changeTask(category, task)

def refreshLayout():
    ui.refreshLayout()

Application = ui.Application
