#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
if 'nt' in sys.builtin_module_names:
    sys.path.append('./pythonmodules')

# We need this for rendering

import mh2mitsuba

# We need this for gui controls

import gui3d

print 'Mitsuba imported'

class MitsubaTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Mitsuba')

        # Buttons
        
        renderBox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Render Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        source=[]
        self.consoleButton = renderBox.addView(gui3d.RadioButton(source, 'Render console'))
        self.guiButton = renderBox.addView(gui3d.RadioButton(source, 'Render GUI', selected = True))
        self.xmlButton = renderBox.addView(gui3d.RadioButton(source, 'Write XML'))
        self.renderButton = renderBox.addView(gui3d.Button('Render'))            

        @self.renderButton.event
        def onClicked(event):            
            
            reload(mh2mitsuba)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
            mh2mitsuba.MitsubaExport(gui3d.app.selectedHuman.mesh, gui3d.app,
                {'source':'console' if self.consoleButton.selected else 'gui' if self.guiButton.selected else 'xml'})
            '''
                 'lighting':'dl' if self.dlButton.selected else 'pm',
                 'world':'sunsky' if self.sunskyButton.selected else 'texture' if self.texButton.selected else 'color'})
            '''

    def onShow(self, event):
        self.renderButton.setFocus()
        gui3d.TaskView.onShow(self, event)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Rendering')
    taskview = category.addView(MitsubaTaskView(category))

    print 'Mitsuba loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    
    print 'Mitsuba unloaded'


