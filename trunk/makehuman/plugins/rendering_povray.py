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
        gui3d.GroupBox(self, [10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*1+6));y+=25
        
        #Buttons
        self.renderButton = gui3d.Button(self, [18, y, 9.02], 'Render');y+=24

        @self.renderButton.event
        def onClicked(event):            
            
            reload(mh2povray)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
            for obj in self.app.scene3d.objects:

            # print "POV-Ray Export test: ", obj.name
            # Only process the humanoid figure

                if obj.name == 'base.obj':
                    mh2povray.povrayExport(obj, self.app)

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


