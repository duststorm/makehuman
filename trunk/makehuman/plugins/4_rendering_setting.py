#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
class RenderingSettingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Rendering Setting', label='Settings')

        #Rendering resolution
        resBox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Resolution', gui3d.GroupBoxStyle._replace(height=25+24*2+6)))
        rendering_width = gui3d.app.settings.get('rendering_width', 800)
        self.width= resBox.addView(gui3d.TextEdit(str(rendering_width), gui3d.TextEditStyle._replace(width=112),
            gui3d.intValidator))
        rendering_height = gui3d.app.settings.get('rendering_height', 600)
        self.height= resBox.addView(gui3d.TextEdit(str(rendering_height), gui3d.TextEditStyle._replace(width=112),
            gui3d.intValidator))

        @self.width.event
        def onChange(value):
            gui3d.app.settings['rendering_width'] = 0 if not value else int(value)

        @self.height.event
        def onChange(value):
            gui3d.app.settings['rendering_height'] = 0 if not value else int(value)

    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        gui3d.app.saveSettings()

def load(app):
    category = app.getCategory('Rendering')
    taskview = category.addView(RenderingSettingTaskView(category))
    print 'Rendering setting imported'

def unload(app):
    pass


