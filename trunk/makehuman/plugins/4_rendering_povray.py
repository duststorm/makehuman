#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os

# We need this for rendering

import mh2povray

# We need this for gui controls

import gui3d
import mh
import gui

class PovrayTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Povray')
        
        # for path to PovRay binaries file
        binarie = ''

        bintype = []
        pathBox = self.addLeftWidget(gui.GroupBox('Povray  bin  path'))
        # this part load old settings values for next session; str(povray_bin)
        povray_bin = gui3d.app.settings.get('povray_bin', '')
        self.path= pathBox.addWidget(gui.TextEdit(str(povray_bin)))
        #
        if os.name == 'nt':
            #
            if os.environ['PROCESSOR_ARCHITECTURE'] == 'x86':
                self.win32sse2Button = pathBox.addWidget(gui.CheckBox('Use SSE2 bin', True))
        #
        @self.path.mhEvent
        def onChange(value):
            gui3d.app.settings['povray_bin'] = 'Enter your path' if not value else str(value)
        #------------------------------------------------------------------------------------
        filter = []
        # Options box
        optionsBox = self.addLeftWidget(gui.GroupBox('Options'))
        self.useSSS = optionsBox.addWidget(gui.CheckBox('Use S.S. Scattering', False))
        self.SSSQ = optionsBox.addWidget(gui.Slider(value=0.5, label="SSS Quality"))
        
        # box
        #optionsBox = self.addLeftWidget(gui.GroupBox('Options'))
        
        #Buttons
        # Simplified the gui a bit for the average user. Uncomment to clutter it up with developer - useful stuff.
        #source=[]
        #self.iniButton = optionsBox.addWidget(gui.RadioButton(source, 'Use ini settings'))
        #self.guiButton = optionsBox.addWidget(gui.RadioButton(source, 'Use gui settings', selected = True))
        format=[]
        self.arrayButton = optionsBox.addWidget(gui.RadioButton(format, 'Array  format'))
        self.mesh2Button = optionsBox.addWidget(gui.RadioButton(format, 'Mesh2 format', selected = True))
        #action=[]
        #self.exportButton = optionsBox.addWidget(gui.RadioButton(action , 'Export only', selected = True))
        #self.exportandrenderButton = optionsBox.addWidget(gui.RadioButton(action , 'Export and render'))
        self.renderButton = optionsBox.addWidget(gui.Button('Render'))
        
        #        
        @self.renderButton.mhEvent
        def onClicked(event):            
            
            reload(mh2povray)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
            # it is necessary to put this code here, so that it is executed with the 'renderButton.event'
            if os.name == 'nt':
                #
                if os.environ['PROCESSOR_ARCHITECTURE'] == "x86":
                    binarie = 'win32'
                    #
                    if self.win32sse2Button.selected:
                        binarie = 'win32sse2'
                #
                else:
                    binarie = 'win64'
            # for Ubuntu.. atm
            if sys.platform == 'linux2':
                binarie = 'linux'
            #
            mh2povray.povrayExport(gui3d.app.selectedHuman.mesh, gui3d.app,
                                   {'source':'gui',         # 'ini' if self.iniButton.selected else 'gui',
                                    'format':'array' if self.arrayButton.selected else 'mesh2',
                                    'action':'render',      # 'export' if self.exportButton.selected else 'render',
                                    'bintype': binarie,
                                    'SSS': True if self.useSSS.selected else False,
                                    'SSSQ':50 * self.SSSQ.getValue()}) 

    def onShow(self, event):
        self.renderButton.setFocus()
        gui3d.TaskView.onShow(self, event)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Rendering')
    taskview = category.addTask(PovrayTaskView(category))

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass
