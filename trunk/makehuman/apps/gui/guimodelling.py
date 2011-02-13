#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module containing classes to handle modelling mode GUI operations.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2011

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

class ModellingCategory(gui3d.Category):

    def __init__(self, parent):
        gui3d.Category.__init__(self, parent, 'Modelling')
        
        mesh = gui3d.RectangleMesh(420, 420, self.app.getThemeResource("images", 'background.png'))
        self.background = gui3d.Object(self, [190, 90, -89.98], mesh)
        
        y = 600-110
        self.viewBox = gui3d.GroupBox(self, [10, y, 9.0], 'View settings', gui3d.GroupBoxStyle._replace(height=25+24*2+6));y+=25
        
        modifierStyle = gui3d.ButtonStyle._replace(width=(112-4)/2.0, height=20)
        
        x = 18
        x+=modifierStyle.width+4
        self.anaglyphsButton = gui3d.ToggleButton(self.viewBox, [round(x), y, 9.1], 'Anaglyphs',
            style=modifierStyle);x+=modifierStyle.width+4
        y += 24
        x = 18
        self.wireButton = gui3d.ToggleButton(self.viewBox, [round(x), y, 9.1], 'Wireframe',
            style=modifierStyle)
        x+=modifierStyle.width+4
        self.subdivisionButton = gui3d.ToggleButton(self.viewBox, [round(x), y, 9.1], 'Smooth',
            style=modifierStyle)

        @self.anaglyphsButton.event
        def onClicked(event):
            self.app.toggleStereo()
            self.anaglyphsButton.setSelected(mh.cameras[0].stereoMode != 0)
            
        @self.wireButton.event
        def onClicked(event):
            self.app.toggleSolid()
            self.wireButton.setSelected(self.app.selectedHuman.mesh.solid == 0)
            
        @self.subdivisionButton.event
        def onClicked(event):
            self.app.toggleSubdivision()
            self.subdivisionButton.setSelected(self.app.selectedHuman.isSubdivided())
        
        guimacromodelling.MacroModelingTaskView(self)
        guidetailmodelling.DetailModelingTaskView(self)
        guidetailmodelling.MicroModelingTaskView(self)

    def onResized(self, event):
        self.background.mesh.resize(event[0] - 190 * 2, event[1] - 90 * 2)
        self.viewBox.setPosition([10, event[1]-110, 9.0])
