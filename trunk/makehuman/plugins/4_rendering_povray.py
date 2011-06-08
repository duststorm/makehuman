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

        optionsBox = gui3d.GroupBox(self, [10, 80, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6))
        
        #Buttons
        source=[]
        self.iniButton = gui3d.RadioButton(optionsBox, source, 'Use ini settings')
        self.guiButton = gui3d.RadioButton(optionsBox, source, 'Use gui settings', selected = True)
        format=[]
        self.arrayButton = gui3d.RadioButton(optionsBox, format, 'Array format')
        self.mesh2Button = gui3d.RadioButton(optionsBox, format, 'Mesh2 format', selected = True)
        action=[]
        self.exportButton = gui3d.RadioButton(optionsBox, action , 'Export only', selected = True)
        self.exportandrenderButton = gui3d.RadioButton(optionsBox, action , 'Export and render')
        self.renderButton = gui3d.Button(optionsBox, 'Render')

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


