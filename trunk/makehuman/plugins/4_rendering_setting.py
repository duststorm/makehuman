#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import gui3d
import mh
import gui
import log

class RenderingSettingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Rendering Setting', label='Settings')

        #Rendering resolution
        rendering_width = gui3d.app.settings.get('rendering_width', 800)
        rendering_height = gui3d.app.settings.get('rendering_height', 600)
        resBox = self.addLeftWidget(gui.GroupBox('Resolution'))
        self.width  = resBox.addWidget(gui.SpinBox(rendering_width), 0, 0)
        self.height = resBox.addWidget(gui.SpinBox(rendering_height), 0, 1)

        @self.width.mhEvent
        def onChange(value):
            gui3d.app.settings['rendering_width'] = 0 if not value else int(value)

        @self.height.mhEvent
        def onChange(value):
            gui3d.app.settings['rendering_height'] = 0 if not value else int(value)

    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        gui3d.app.saveSettings()

def load(app):
    category = app.getCategory('Rendering')
    taskview = category.addTask(RenderingSettingTaskView(category))

def unload(app):
    pass


