#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import mh
import qtgui as gui

class RenderingSettingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Rendering Setting', label='Settings')

        #Rendering resolution
        rendering_width = gui3d.app.settings.get('rendering_width', 800)
        rendering_height = gui3d.app.settings.get('rendering_height', 600)
        resBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Resolution')))
        self.width  = resBox.addWidget(gui.TextEdit(str(rendering_width), validator = gui.intValidator))
        self.height = resBox.addWidget(gui.TextEdit(str(rendering_height), validator = gui.intValidator))

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
    print 'Rendering setting imported'

def unload(app):
    pass


