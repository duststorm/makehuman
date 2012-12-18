#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
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
        
        # for path to PovRay binaries file
        binarie = ''
        y = 80
        bintype = []
        pathBox = self.addView(gui3d.GroupBox([10, y, 9.0], 'Povray  bin  path')); y +=25+16 
        # this part load old settings values for next session; str(povray_bin)
        povray_bin = gui3d.app.settings.get('povray_bin', '')
        self.path= pathBox.addView(gui3d.TextEdit(str(povray_bin), gui3d.TextEditStyle._replace(width=112))); y +=24 
        #
        if os.name == 'nt':
            #
            if os.environ['PROCESSOR_ARCHITECTURE'] == 'x86':
                self.win32sse2Button = pathBox.addView(gui3d.CheckBox('Use SSE2 bin', True)); y +=24
        #
        @self.path.mhEvent
        def onChange(value):
            gui3d.app.settings['povray_bin'] = 'Enter your path' if not value else str(value)
        #------------------------------------------------------------------------------------
        filter = []
        # Options box
        optionsBox = self.addView(gui3d.GroupBox([10, y, 9.0], 'Options')); y +=25+16 
        self.useSSS = optionsBox.addView(gui3d.CheckBox('Use S.S. Scattering', False)); y +=24
        
        # box
        #optionsBox = self.addView(gui3d.GroupBox([10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6))); y +=25+16
        
        #Buttons
        # Simplified the gui a bit for the average user. Uncomment to clutter it up with developer - useful stuff.
        #source=[]
        #self.iniButton = optionsBox.addView(gui3d.RadioButton(source, 'Use ini settings')); y +=24
        #self.guiButton = optionsBox.addView(gui3d.RadioButton(source, 'Use gui settings', selected = True)); y +=24
        format=[]
        self.arrayButton = optionsBox.addView(gui3d.RadioButton(format, 'Array  format')); y +=24
        self.mesh2Button = optionsBox.addView(gui3d.RadioButton(format, 'Mesh2 format', selected = True)); y +=24
        #action=[]
        #self.exportButton = optionsBox.addView(gui3d.RadioButton(action , 'Export only', selected = True)); y +=24
        #self.exportandrenderButton = optionsBox.addView(gui3d.RadioButton(action , 'Export and render')); y +=24
        self.renderButton = optionsBox.addView(gui3d.Button('Render')); y +=24
        
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
                                    'SSS': True if self.useSSS.selected else False}) 

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


