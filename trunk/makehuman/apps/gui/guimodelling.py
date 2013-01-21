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
import gui

class ModellingCategory(gui3d.Category):

    def __init__(self):
        super(ModellingCategory, self).__init__('Modelling')
        self.createActions()

    def createActions(self):
        self.actions = gui.Actions()

        Action = gui.Action

        self.actions.mono      = Action('mono',      'Mono',      gui3d.app.setMono,    group='stereo')
        self.actions.stereo1   = Action('stereo1',   'Stereo 1',  gui3d.app.setStereo1, group='stereo')
        self.actions.stereo2   = Action('stereo2',   'Stereo 2',  gui3d.app.setStereo2, group='stereo')
        self.actions.wireframe = Action('wireframe', 'Wireframe', gui3d.app.toggleSolid, toggle=True)

        self.actions.symmetryR = Action('symm1', 'Symmmetry R>L', self.symmetryRight)
        self.actions.symmetryL = Action('symm2', 'Symmmetry L>R', self.symmetryLeft)
        self.actions.symmetry  = Action('symm',  'Symmmetry L>R', self.symmetry, toggle=True)

        for action in self.actions:
            gui3d.app.mainwin.toolbar.addAction(action)

    def symmetryRight(self):
        human = gui3d.app.selectedHuman
        human.applySymmetryRight()

    def symmetryLeft(self):
        human = gui3d.app.selectedHuman
        human.applySymmetryLeft()

    def symmetry(self):
        human = gui3d.app.selectedHuman
        human.symmetryModeEnabled = self.actions.symmetry.isChecked()
