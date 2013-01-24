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

Python compatibility layer replacing the old C functions of MakeHuman.
"""

from core import G
from getpath import getPath

from image import Image
from texture import Texture, getTexture, reloadTextures
from camera import Camera

from qtui import Keys, Buttons, Modifiers, Application
from qtui import callAsyncThread, setShortcut
from qtui import getSaveFileName, getOpenFileName, getExistingDirectory

from glmodule import createVertexShader, createFragmentShader, createShader
from glmodule import updatePickingBuffer, grabScreen, hasRenderSkin, renderSkin

from inifile import parseINI, formatINI

cameras = G.cameras

def getColorPicked():
    return G.color_picked

def setClearColor(r, g, b, a):
    G.clearColor = (r, g, b, a)

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

def addTopWidget(widget, *args, **kwargs):
    return G.app.mainwin.addTopWidget(widget, *args, **kwargs)

def removeTopWidget(widget):
    return G.app.mainwin.removeTopWidget(widget)

def addToolBar(name):
    return G.app.mainwin.addToolBar(name)

def redraw():
    G.app.redraw()

def getKeyModifiers():
    return int(G.app.keyboardModifiers())

def addTimer(milliseconds, callback):
    return G.app.addTimer(milliseconds, callback)

def removeTimer(id):
    G.app.removeTimer(id)

def callAsync(func, *args, **kwargs):
    G.app.callAsync(func, *args, **kwargs)
