#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import os
import sys
if 'nt' in sys.builtin_module_names:
    sys.path.append('./pythonmodules')
import subprocess
import mh2renderman
import mh
import qtgui as gui
import log

def which(program):
    """
    Checks whether a program exists, similar to http://en.wikipedia.org/wiki/Which_(Unix)
    """

    import os
    import sys
    
    if sys.platform == "win32" and not program.endswith(".exe"):
        program += ".exe"

    log.message("looking for %s", program)
        
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            log.message("testing %s", exe_file)
            if is_exe(exe_file):
                return exe_file

    return None

class AqsisTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Aqsis')

        self.sceneToRender = None

        optionsBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.SliderBox('Options')))
                                              
        #Sliders                            
        self.shadingRateSlider= optionsBox.addWidget(gui.Slider(value=2, min=0.1, max=10, label = "ShadingRate: %.2f"))
        self.samplesSlider= optionsBox.addWidget(gui.Slider(value=2, min=1.0, max=10, label = "Samples: %.2f"))
        self.skinOilSlider= optionsBox.addWidget(gui.Slider(value=0.3, min=0.0, max=10, label = "Skin Oil: %.2f"))
        
        #Buttons
        self.renderButton = optionsBox.addWidget(gui.Button('Render'))
            
        @self.shadingRateSlider.mhEvent
        def onChanging(value):
            gui3d.app.settings['rendering_aqsis_shadingrate'] = value #Using global dictionary in app for global settings
            
        @self.samplesSlider.mhEvent
        def onChanging(value):
            gui3d.app.settings['rendering_aqsis_samples'] = value
            
        @self.skinOilSlider.mhEvent
        def onChanging(value):
            gui3d.app.settings['rendering_aqsis_oil'] = value
            
        @self.renderButton.mhEvent
        def onClicked(event):
            
            if not which("aqsis"):
                gui3d.app.prompt('Aqsis not found', 'You don\'t seem to have aqsis installed.', 'Download', 'Cancel', self.downloadAqsis)
                return
            
            if not self.sceneToRender:
                self.sceneToRender = mh2renderman.RMRScene(gui3d.app)
            self.buildShaders()
            self.sceneToRender.render()
            
    def buildShaders(self):
        
        shaders = ['hairpoly','skin2', 'envlight', 'skinbump', 'scatteringtexture', 'bakelightmap', 'eyeball', 'cornea', 'mixer', 'teeth']
        
        for shader in shaders:
            self.buildShader(shader)
        
    def buildShader(self, shader):
        
        srcPath = os.path.join('data/shaders/aqsis', shader + '.sl')
        dstPath = os.path.join(self.sceneToRender.usrShaderPath, shader + '.slx')
        
        if not os.path.exists(dstPath) or os.stat(srcPath).st_mtime > os.stat(dstPath).st_mtime:
            subprocess.Popen(u'aqsl %s -o "%s"' % (srcPath, dstPath), shell=True)
    
    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.renderButton.setFocus()
        gui3d.app.prompt('Warning', 'The rendering is still an experimental feature since posing is not yet implemented.',
            'OK', helpId='alphaRenderWarning')

    def downloadAqsis(self):
    
        import webbrowser
        webbrowser.open('http://www.aqsis.org/')

def load(app):
    category = app.getCategory('Rendering')
    taskview = category.addTask(AqsisTaskView(category))

def unload(app):
    pass


