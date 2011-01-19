#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import mh
import os
import sys
if 'nt' in sys.builtin_module_names:
    sys.path.append('./pythonmodules')
import subprocess
import mh2renderman


class AqsisTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Aqsis')

        self.sceneToRender = mh2renderman.RMRScene(self.app)
        #Create aqsis shaders
        subprocess.Popen('aqsl data/shaders/aqsis/skin2.sl -o "%s"' % os.path.join(self.sceneToRender.usrShaderPath, 'skin2.slx'), shell=True)
        subprocess.Popen('aqsl data/shaders/aqsis/hair.sl -o "%s"' % os.path.join(self.sceneToRender.usrShaderPath, 'hair.slx'), shell=True)
        subprocess.Popen('aqsl data/shaders/aqsis/envlight.sl -o "%s"' % os.path.join(self.sceneToRender.usrShaderPath, 'envlight.slx'), shell=True)
        subprocess.Popen('aqsl data/shaders/aqsis/skinbump.sl -o "%s"' % os.path.join(self.sceneToRender.usrShaderPath, 'skinbump.slx'), shell=True)
        subprocess.Popen('aqsl data/shaders/aqsis/scatteringtexture.sl -o "%s"' % os.path.join(self.sceneToRender.usrShaderPath, 'scatteringtexture.slx'), shell=True)
        subprocess.Popen('aqsl data/shaders/aqsis/bakelightmap.sl -o "%s"' % os.path.join(self.sceneToRender.usrShaderPath, 'bakelightmap.slx'), shell=True)
        subprocess.Popen('aqsl data/shaders/aqsis/eyeball.sl -o "%s"' % os.path.join(self.sceneToRender.usrShaderPath, 'eyeball.slx'), shell=True)
        subprocess.Popen('aqsl data/shaders/aqsis/cornea.sl -o "%s"' % os.path.join(self.sceneToRender.usrShaderPath, 'cornea.slx'), shell=True)
        subprocess.Popen('aqsl data/shaders/aqsis/mixer.sl -o "%s"' % os.path.join(self.sceneToRender.usrShaderPath, 'mixer.slx'), shell=True)

        gui3d.GroupBox(self, label = 'Options', position=[10, 80, 9.0], width=128, height=256)
                                              
        #Sliders                            
        self.shadingRateSlider= gui3d.Slider(self, position=[10, 115, 9.3], value=2, min=0.1, max=10, label = "ShadingRate: 2.00")
        self.samplesSlider= gui3d.Slider(self, position=[10, 155, 9.01], value=2, min=1.0, max=10, label = "Samples: 2.00")       
        self.skinOilSlider= gui3d.Slider(self, position=[10, 200, 9.02], value=0.3, min=0.0, max=10, label = "Skin Oil: 0.3")     
        
        #Buttons
        self.renderButton = gui3d.Button(self, [18, 250, 9.02], 'Render')

        @self.renderButton.event
        def onClicked(event):            
            self.sceneToRender.render()

        
            
        @self.shadingRateSlider.event
        def onChanging(value):
            self.shadingRateSlider.label.setText("ShadingRate: "+str(round(value,3)))
            self.app.settings['rendering_aqsis_shadingrate'] = value #Using global dictionary in app for global settings
            
        @self.samplesSlider.event
        def onChanging(value):
            self.samplesSlider.label.setText("Samples: "+str(round(value,3)))
            self.app.settings['rendering_aqsis_samples'] = value
            
        @self.skinOilSlider.event
        def onChanging(value):
            self.skinOilSlider.label.setText("Skin Oil: "+str(round(value,3)))
            self.app.settings['rendering_aqsis_oil'] = value
    
    def onShow(self, event):
        self.renderButton.setFocus()
        gui3d.TaskView.onShow(self, event)

def load(app):
    category = app.getCategory('Rendering')
    taskview = AqsisTaskView(category)

def unload(app):
    pass


