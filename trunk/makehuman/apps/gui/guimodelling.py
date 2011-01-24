#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module containing classes to handle modelling mode GUI operations.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements the 'guimodelling' class structures and methods to support GUI
Modelling mode operations.
Modelling mode is invoked by selecting the Modelling mode icon from the main GUI control
bar at the top of the screen.
While in this mode, user actions (keyboard and mouse events) are passed into
this class for processing. Having processed an event this class returns control to the
main OpenGL/SDL/Application event handling loop.


"""

__docformat__ = 'restructuredtext'

import mh
import events3d
import gui3d
import guimacromodelling
import guidetailmodelling
import os

HairButtonStyle = gui3d.Style(**{
    'width':None,
    'height':None,
    'mesh':'data/3dobjs/button_standard_little.obj',
    'normal':None,
    'selected':None,
    'focused':None,
    'fontSize':gui3d.defaultFontSize,
    'border':None
    })

class ModellingCategory(gui3d.Category):

    def __init__(self, parent):
        gui3d.Category.__init__(self, parent, 'Modelling')
        
        gui3d.GroupBox(self, [10, 472, 9.0], 'View settings')
        
        self.background = gui3d.Object(self, 'data/3dobjs/background.obj', position=[400, 300, -89.98])

        hairTexture = self.app.scene3d.selectedHuman.hairFile.replace('.hair', '.png')
        self.currentHair = gui3d.Button(self, [600, 580, 9.2], style=HairButtonStyle._replace(normal=hairTexture))

        @self.currentHair.event
        def onClicked(event):
            self.app.switchCategory('Library')
            self.app.scene3d.redraw(1)

        self.backgroundImage = gui3d.Object(self, 'data/3dobjs/background.obj', position=[400, 300, 1], visible=False)
        self.backgroundImageToggle = gui3d.ToggleButton(self, [15, 514, 9.1], 'Bkg',
            style=gui3d.ButtonStyle._replace(width=32, height=16))

        @self.backgroundImageToggle.event
        def onClicked(event):
            if self.backgroundImage.isVisible():
                self.backgroundImage.hide()
                self.backgroundImageToggle.setSelected(False)
            elif self.backgroundImage.hasTexture():
                self.backgroundImage.show()
                self.backgroundImageToggle.setSelected(True)
            else:
                self.app.switchCategory('Library')
                self.app.switchTask('Background')
            self.app.scene3d.redraw(1)
            
        self.anaglyphsButton = gui3d.ToggleButton(self, [51, 514, 9.1], '3D',
            style=gui3d.ButtonStyle._replace(width=32, height=16))

        @self.anaglyphsButton.event
        def onClicked(event):
            self.app.toggleStereo()
            self.anaglyphsButton.selected = mh.cameras[0].stereoMode
            
        self.wireButton = gui3d.ToggleButton(self, [87, 514, 9.1], 'Wire',
            style=gui3d.ButtonStyle._replace(width=32, height=16))
            
        @self.wireButton.event
        def onClicked(event):
            self.app.toggleSolid()
            self.wireButton.selected = self.app.selectedHuman.mesh.solid
        
        guimacromodelling.MacroModelingTaskView(self)
        guidetailmodelling.DetailModelingTaskView(self)
        guidetailmodelling.MicroModelingTaskView(self)

