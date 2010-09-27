#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Class for handling Render mode in the GUI.

B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Manuel Bastioni, Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2010

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

This module implements the 'guirender' class structures and methods to support GUI 
Render mode operations.
Render mode is invoked by selecting the Render mode icon from the main GUI control 
bar at the top of the screen. 
While in this mode, user actions (keyboard and mouse events) are passed into 
this class for processing. Having processed an event this class returns control to the 
main OpenGL/SDL/Application event handling loop.  

"""

import gui3d


class RenderingCategory(gui3d.Category):

    def __init__(self, parent):
        gui3d.Category.__init__(self, parent, 'Rendering', parent.app.getThemeResource('images', 'button_render.png'), parent.app.getThemeResource('images', 'button_render_on.png'))
        self.clumpRadius = gui3d.Slider(self, position=[10, 150, 9], value=0.09, min=0.05,max=0.5, label = "Clump Interpolation Radius: 0.09") 
        self.clumpRadius.label.setPosition([20,135,8])
        #self.fallingHair = gui3d.ToggleButton(self, mesh='data/3dobjs/button_generic_long.obj', position=[15, 200,9], label="Falling Hair")
        #self.guidesOnly = gui3d.ToggleButton(self, mesh='data/3dobjs/button_generic_long.obj', position=[15, 250,9], label="Guides Only")
        self.hairsClass = None 
        
        @self.clumpRadius.event
        def onChanging(value):
            self.clumpRadius.label.setText("Clump Interpolation Radius: "+str(self.clumpRadius.getValue()))
            self.hairsClass.interpolationRadius = self.clumpRadius.getValue()


    def onShow(self, event):
        self.setFocus()
        gui3d.Category.onShow(self, event)


