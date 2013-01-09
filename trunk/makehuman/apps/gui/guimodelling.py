#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module containing classes to handle modelling mode GUI operations.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

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
import guidetailmodelling
import gui

class ModellingCategory(gui3d.Category):

    def __init__(self):
        super(ModellingCategory, self).__init__('Modelling')

        self.viewBox = self.addBottomWidget(gui.GroupBox('View settings'))
        
        self.anaglyphsButton = self.viewBox.addWidget(gui.ToggleButton('Anaglyphs'))
        self.wireButton = self.viewBox.addWidget(gui.ToggleButton('Wireframe'))
        self.subdivisionButton = self.viewBox.addWidget(gui.ToggleButton('Smooth'))

        self.symmetryBox = self.addBottomWidget(gui.GroupBox('Symmetry'))

        self.rightSymmetryButton = self.symmetryBox.addWidget(gui.Button('Sym<'), 0, 0)
        self.leftSymmetryButton = self.symmetryBox.addWidget(gui.Button('Sym>'), 0, 1)
        self.symmetryButton = self.symmetryBox.addWidget(gui.ToggleButton('Sym'), 1, 0, 1, -1)

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

        @self.rightSymmetryButton.mhEvent
        def onClicked(event):
            human = gui3d.app.selectedHuman
            human.applySymmetryRight()

        @self.leftSymmetryButton.mhEvent
        def onClicked(event):
            human = gui3d.app.selectedHuman
            human.applySymmetryLeft()

        @self.symmetryButton.mhEvent
        def onClicked(event):
            human = gui3d.app.selectedHuman
            human.symmetryModeEnabled = self.symmetryButton.selected
        
        self.addTask(guidetailmodelling.DetailModelingTaskView(self))
