#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Class for handling Render mode in the GUI.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements the 'guirender' class structures and methods to support GUI 
Render mode operations.
Render mode is invoked by selecting the Render mode icon from the main GUI control 
bar at the top of the screen. 
While in this mode, user actions (keyboard and mouse events) are passed into 
this class for processing. Having processed an event this class returns control to the 
main OpenGL/SDL/Application event handling loop.  

"""

__docformat__ = 'restructuredtext'

import gui3d


class RenderingCategory(gui3d.Category):

    def __init__(self, parent):
        gui3d.Category.__init__(self, parent, 'Rendering', parent.app.getThemeResource('images', 'button_render.png'), parent.app.getThemeResource('images', 'button_render_on.png'))
        self.guideArea = gui3d.Slider(self, position=[10, 150, 9], value=0.6, min=0.2,max=1.0, label = "0.6") 
        self.guideArea.label.setPosition([20,135,9])
    
        @self.guideArea.event
        def onChanging(value):
            self.guideArea.label.setText(str(self.guideArea.getValue()))


    def onShow(self, event):
        self.setFocus()
        gui3d.Category.onShow(self, event)


