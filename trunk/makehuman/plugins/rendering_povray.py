#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
if 'nt' in sys.builtin_module_names:
    sys.path.append('./pythonmodules')
import subprocess

# We need this for rendering

import mh2povray

# We need this for gui controls

import gui3d

print 'povray imported'

class PovrayTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Povray')

        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6));y+=25
        
        #Buttons
        source=[]
        self.iniButton = gui3d.RadioButton(self, source, [18, y, 9.02], 'Use ini settings');y+=24
        self.guiButton = gui3d.RadioButton(self, source, [18, y, 9.02], 'Use gui settings', selected = True);y+=24
        format=[]
        self.arrayButton = gui3d.RadioButton(self, format, [18, y, 9.02], 'Array format');y+=24
        self.mesh2Button = gui3d.RadioButton(self, format, [18, y, 9.02], 'Mesh2 format', selected = True);y+=24
        action=[]
        self.exportButton = gui3d.RadioButton(self, action, [18, y, 9.02], 'Export only', selected = True);y+=24
        self.exportandrenderButton = gui3d.RadioButton(self, action, [18, y, 9.02], 'Export and render');y+=24
        self.renderButton = gui3d.Button(self, [18, y, 9.02], 'Render');y+=24

        @self.renderButton.event
        def onClicked(event):            
            
            reload(mh2povray)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
            mh2povray.povrayExport(self.app.scene3d.getObject('base.obj'), self.app,
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
    taskview = PovrayTaskView(category)

    print 'Povray loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    
    print 'Povray unloaded'


