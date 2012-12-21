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
import gui3d
import guimacromodelling
import guidetailmodelling
import qtgui as gui

class ModellingCategory(gui3d.Category):

    def __init__(self, parent):
        gui3d.Category.__init__(self, parent, 'Modelling')

        self.viewBox = self.addWidget(mh.addWidget(mh.Frame.LeftBottom, gui.GroupBox('View settings')))
        
        self.anaglyphsButton = self.viewBox.addWidget(gui.ToggleButton('Anaglyphs'))
        self.wireButton = self.viewBox.addWidget(gui.ToggleButton('Wireframe'))
        self.subdivisionButton = self.viewBox.addWidget(gui.ToggleButton('Smooth'))

        @self.anaglyphsButton.mhEvent
        def onClicked(event):
            gui3d.app.toggleStereo()
            self.anaglyphsButton.setSelected(mh.cameras[0].stereoMode != 0)
            
        @self.wireButton.mhEvent
        def onClicked(event):
            gui3d.app.toggleSolid()
            self.wireButton.setSelected(gui3d.app.selectedHuman.mesh.solid == 0)
            
        @self.subdivisionButton.mhEvent
        def onClicked(event):
            gui3d.app.toggleSubdivision()
            self.subdivisionButton.setSelected(gui3d.app.selectedHuman.isSubdivided())
        
        self.addView(guimacromodelling.MacroModelingTaskView(self))
        self.addView(guidetailmodelling.DetailModelingTaskView(self))
