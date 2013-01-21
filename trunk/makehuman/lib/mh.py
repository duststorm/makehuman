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

import json

from core import G
from getpath import getPath
import glmodule as gl

import qtui as ui

from image import Image
from texture import Texture, getTexture, reloadTextures
from object3d import Object3D
from camera import Camera

from qtui import getKeyModifiers, addTimer, removeTimer, callAsync
from qtui import getSaveFileName, getOpenFileName, getExistingDirectory
from glmodule import createVertexShader, createFragmentShader, createShader
from glmodule import updatePickingBuffer, grabScreen, hasRenderSkin, renderSkin

cameras = G.cameras

Keys = ui.Keys
Buttons = ui.Buttons
Modifiers = ui.Modifiers

def getColorPicked():
    return G.color_picked

def setClearColor(r, g, b, a):
    G.clearColor = (r, g, b, a)

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

def addTopWidget(widget, *args, **kwargs):
    return G.app.mainwin.addTopWidget(widget, *args, **kwargs)

def removeTopWidget(widget):
    return G.app.mainwin.removeTopWidget(widget)

def setShortcut(modifier, key, method):
    G.app.mainwin.setShortcut(modifier, key, method)

def _u2s(value):
    if isinstance(value, unicode):
        return str(value)
    elif isinstance(value, dict):
        return dict([(str(key), _u2s(val)) for key, val in value.iteritems()])
    elif isinstance(value, list):
        return [_u2s(val) for val in value]
    else:
        return value

def parseINI(s, replace = []):
    try:
        result = json.loads(s)
    except ValueError:
        for src, dst in replace + [("'",'"'), (": True",": true"), (": False",": false"), (": None",": null")]:
            s = s.replace(src, dst)
        result = json.loads(s)
    return _u2s(result)

def formatINI(d):
    return json.dumps(d, indent=4, ensure_ascii=True, encoding='iso-8859-1') + '\n'
