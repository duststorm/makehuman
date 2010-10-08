#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
class RenderingSettingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Rendering Setting', category.app.getThemeResource('images', 'button_setting.png'), category.app.getThemeResource('images', 'button_setting_on.png'))

        #Rendering size
        self.widthSize= gui3d.Slider(self, position=[10, 80, 9.3], value=800, min=10, max=5000, label = "Rendering Width: 800")
        self.widthSize.label.setPosition([15,75,9.5])
        self.heightSize= gui3d.Slider(self, position=[10, 120, 9.3], value=600, min=10, max=5000, label = "Rendering Height: 600")
        self.heightSize.label.setPosition([15,115,9.5])

        #Hair data
        self.clumpRadius = gui3d.Slider(self, position=[10, 160, 9.3], value=0.09, min=0.05,max=0.5, label = "Hair clump radius: 0.09")
        self.clumpRadius.label.setPosition([15,155,9.5])
        self.clumpChildren= gui3d.Slider(self, position=[10, 200, 9.3], value=0, min=0, max=150, label = "Hair clump children: 0")
        self.clumpChildren.label.setPosition([15,195,9.5])
        self.multiStrand= gui3d.Slider(self, position=[10, 240, 9.3], value=0, min=0, max=150, label = "Multistrand children: 0")
        self.multiStrand.label.setPosition([15,235,9.5])
        self.randomHair= gui3d.Slider(self, position=[10, 280, 9.3], value=0.04, min=0.0, max=0.09, label = "Hair Randomness: 0.04")
        self.randomHair.label.setPosition([15,275,9.5])


        self.human = self.app.scene3d.selectedHuman

        @self.clumpRadius.event
        def onChanging(value):
            self.clumpRadius.label.setText("Hair clump radius: "+str(round(self.clumpRadius.getValue(),4)))
            self.human.hairs.interpolationRadius = self.clumpRadius.getValue()

        @self.clumpChildren.event
        def onChanging(value):
            self.clumpChildren.label.setText("Hair clump children: "+str(self.clumpChildren.getValue()))
            self.human.hairs.clumpInterpolationNumber = self.clumpChildren.getValue()
            
        @self.multiStrand.event
        def onChanging(value):
            self.multiStrand.label.setText("Multistrand children: "+str(self.multiStrand.getValue()))
            self.human.hairs.multiStrandNumber = self.multiStrand.getValue()
        
        @self.randomHair.event
        def onChanging(value):
            self.randomHair.label.setText("Hair Randomness: "+str(round(self.randomHair.getValue(),4)))
            self.human.hairs.randomness = self.randomHair.getValue()


        @self.widthSize.event
        def onChanging(value):
            self.widthSize.label.setText("Rendering Width: "+str(self.widthSize.getValue()))
            self.app.settings['rendering_width'] = self.widthSize.getValue() #Using global dictionary in app for global settings

        @self.heightSize.event
        def onChanging(value):
            self.heightSize.label.setText("Rendering Height: "+str(self.heightSize.getValue()))
            self.app.settings['rendering_height'] = self.heightSize.getValue() #Using global dictionary in app for global settings


def load(app):
    category = app.getCategory('Rendering','button_render.png','button_render_on.png')
    taskview = RenderingSettingTaskView(category)
    print 'Rendering setting imported'

def unload(app):
    pass


