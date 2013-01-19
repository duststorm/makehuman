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

import sys
import os

# We need this for rendering

import mh2mitsuba

# We need this for gui controls

import gui3d
import mh
import gui

class MitsubaTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Mitsuba')

        # Buttons
        pathBox = self.addLeftWidget(gui.GroupBox('Mitsuba  bin  path'))
        mitsuba_bin = gui3d.app.settings.get('mitsuba_bin', '')
        self.path= pathBox.addWidget(gui.TextEdit(str(mitsuba_bin)), 0, 0, 1, 2)
        self.browse = pathBox.addWidget(gui.BrowseButton(), 1, 0, 1, 1)
        self.browse.setPath(mitsuba_bin)
        if sys.platform == 'win32':
            self.browse.setFilter('Executable programs (*.exe);;All files (*.*)')
        #
        @self.path.mhEvent
        def onChange(value):
            gui3d.app.settings['mitsuba_bin'] = 'Enter your path' if not value else str(value)

        @self.browse.mhEvent
        def onClicked(path):
            if os.path.isfile(path):
                gui3d.app.settings['mitsuba_bin'] = path
                self.path.setText(path)
        
        # Type of lighting method
        lightingBox = self.addLeftWidget(gui.GroupBox('Integrators'))
        lighting = []
        self.dlButton = lightingBox.addWidget(gui.RadioButton(lighting, 'DirectLighting', selected = True))
        self.ptButton = lightingBox.addWidget(gui.RadioButton(lighting, 'Path Tracing'))
        self.pmButton = lightingBox.addWidget(gui.RadioButton(lighting, 'Photon Mapping'))
        
        #
        samplerBox = self.addLeftWidget(gui.GroupBox('Sampler Options'))
        sampler = []
        self.lowdButton = samplerBox.addWidget(gui.RadioButton(sampler, 'Low Discrepancy', selected = True))
        self.indepButton = samplerBox.addWidget(gui.RadioButton(sampler, 'Independent'))
        #
        renderBox = self.addLeftWidget(gui.GroupBox('Render Options'))
        source=[]
        self.consoleButton = renderBox.addWidget(gui.RadioButton(source, 'Render console'))
        self.guiButton = renderBox.addWidget(gui.RadioButton(source, 'Render GUI', selected = True))
        self.xmlButton = renderBox.addWidget(gui.RadioButton(source, 'Write XML'))
        self.renderButton = renderBox.addWidget(gui.Button('Render'))
               

        @self.renderButton.mhEvent
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
    taskview = category.addTask(MitsubaTaskView(category))

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass
