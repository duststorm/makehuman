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
        pathBox = self.addView(gui3d.GroupBox([10, y, 9.0], 'Povray  bin  path')); y +=25 #, gui3d.GroupBoxStyle._replace(height=25+24*2+6)))
        povray_bin = gui3d.app.settings.get('povray_bin', '')
        self.path= pathBox.addView(gui3d.TextEdit(str(povray_bin), gui3d.TextEditStyle._replace(width=112))); y +=24
        
        #
        if os.name == 'nt':
            #
            if os.environ['PROCESSOR_ARCHITECTURE'] == 'x86':
                 self.win32Button = pathBox.addView(gui3d.RadioButton(bintype, 'Use win32 bin', selected = True)); y +=24
                 self.win32sse2Button = pathBox.addView(gui3d.RadioButton(bintype, 'Use SSE2 bin')); y +=24
                 y +=16
            #
            if os.environ['PROCESSOR_ARCHITECTURE'] ==  'AMD64':
                # not need button, only have one option
                y +=16
        #
        if sys.platform == 'linux2':
            print 'OS name: ', str(os.name)
            print 'Platform: ', str(sys.platform)
            y +=16
            
        @self.path.event
        def onChange(value):
            gui3d.app.settings['povray_bin'] = 'Enter your path' if not value else str(value)
        # box
        optionsBox = self.addView(gui3d.GroupBox([10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        
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
            # it is necessary to put this code here, so that it is executed with the 'renderButton.event'
            if os.name == 'nt':
                #
                if os.environ['PROCESSOR_ARCHITECTURE'] == "x86":
                    binarie = 'win32'
                    if self.win32sse2Button.selected:
                        binarie = 'win32sse2'
                #
                else:
                    binarie = 'win64'
            #
            if sys.platform == 'linux2':
                binarie = 'linux'
            #
            mh2povray.povrayExport(gui3d.app.selectedHuman.mesh, gui3d.app,
                {'source':'ini' if self.iniButton.selected else 'gui',
                 'format':'array' if self.arrayButton.selected else 'mesh2',
                 'action':'export' if self.exportButton.selected else 'render',
                 'bintype': binarie}) 

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


