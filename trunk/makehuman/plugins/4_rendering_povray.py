#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
if 'nt' in sys.builtin_module_names:
    sys.path.append('./pythonmodules')

# We need this for rendering

import mh2povray

# We need this for gui controls

import gui3d

print 'povray imported'

class PovrayTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Povray')

        optionsBox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        
        #Buttons
        source=[]
        self.iniButton = optionsBox.addView(gui3d.RadioButton(source, 'Use ini settings'))
        self.guiButton = optionsBox.addView(gui3d.RadioButton(source, 'Use gui settings', selected = True))
        format=[]
        self.arrayButton = optionsBox.addView(gui3d.RadioButton(format, 'Array format'))
        self.mesh2Button = optionsBox.addView(gui3d.RadioButton(format, 'Mesh2 format', selected = True))
        action=[]
        self.exportButton = optionsBox.addView(gui3d.RadioButton(action , 'Export only', selected = True))
        self.exportandrenderButton = optionsBox.addView(gui3d.RadioButton(action , 'Export and render'))
        self.renderButton = optionsBox.addView(gui3d.Button('Render'))

        @self.renderButton.event
        def onClicked(event):            
            
            reload(mh2povray)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
            mh2povray.povrayExport(gui3d.app.selectedHuman.mesh, gui3d.app,
                {'source':'ini' if self.iniButton.selected else 'gui',
                 'format':'array' if self.arrayButton.selected else 'mesh2',
                 'action':'export' if self.exportButton.selected else 'render'})

    def onShow(self, event):
        self.renderButton.setFocus()
        gui3d.TaskView.onShow(self, event)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Rendering')
    taskview = category.addView(PovrayTaskView(category))

    print 'Povray loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    
    print 'Povray unloaded'


