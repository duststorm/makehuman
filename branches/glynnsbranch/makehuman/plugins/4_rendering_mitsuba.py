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
        # Test for path to Mitsuba binaries
        pathBox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Mitsuba path', gui3d.GroupBoxStyle._replace(height=25+24*2+6)))
        binpath = []
        path_bin = gui3d.app.settings.get('path_bin', 'c:/Mitsuba')
        self.path= pathBox.addView(gui3d.TextEdit(str(path_bin), gui3d.TextEditStyle._replace(width=112)))
        #
        @self.path.event
        def onChange(value):
            gui3d.app.settings['path_bin'] = 'Enter your path' if not value else str(value)
        
        # Type of lighting method
        lightingBox = self.addView(gui3d.GroupBox([10, 140, 9.0], 'Integrators', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        lighting = []
        self.dlButton = lightingBox.addView(gui3d.RadioButton(lighting, 'DirectLighting', selected = True))
        self.ptButton = lightingBox.addView(gui3d.RadioButton(lighting, 'Path Tracing'))
        self.pmButton = lightingBox.addView(gui3d.RadioButton(lighting, 'Photon Mapping'))
        
        #
        samplerBox = self.addView(gui3d.GroupBox([10, 250, 9.0], 'Sampler Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        sampler = []
        self.lowdButton = samplerBox.addView(gui3d.RadioButton(sampler, 'Low Discrepancy', selected = True))
        self.indepButton = samplerBox.addView(gui3d.RadioButton(sampler, 'Independent'))
        #
        renderBox = self.addView(gui3d.GroupBox([10, 336, 9.0], 'Render Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        source=[]
        self.consoleButton = renderBox.addView(gui3d.RadioButton(source, 'Render console'))
        self.guiButton = renderBox.addView(gui3d.RadioButton(source, 'Render GUI', selected = True))
        self.xmlButton = renderBox.addView(gui3d.RadioButton(source, 'Write XML'))
        self.renderButton = renderBox.addView(gui3d.Button('Render'))
               

        @self.renderButton.event
        def onClicked(event):            
            
            reload(mh2mitsuba)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
            mh2mitsuba.MitsubaExport(gui3d.app.selectedHuman.mesh, gui3d.app,
                {'source':'console' if self.consoleButton.selected else 'gui' if self.guiButton.selected else 'xml',
                 'lighting':'dl' if self.dlButton.selected else 'pt' if self.ptButton.selected else 'pm',
                 'sampler':'low' if self.lowdButton.selected else 'ind'})

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


