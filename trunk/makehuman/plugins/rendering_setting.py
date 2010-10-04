#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
class RenderingSettingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Rendering Setting', category.app.getThemeResource('images', 'button_setting.png'), category.app.getThemeResource('images', 'button_setting_on.png'))

        #Rendering size
        self.widthSize= gui3d.Slider(self, position=[10, 100, 9], value=800, min=10, max=5000, label = "Rendering Width: 800")
        self.widthSize.label.setPosition([20,85,8])
        self.heightSize= gui3d.Slider(self, position=[10, 165, 9], value=600, min=10, max=5000, label = "Rendering Height: 600")
        self.heightSize.label.setPosition([20,150,8])

        #Hair data
        self.clumpRadius = gui3d.Slider(self, position=[10, 230, 9], value=0.09, min=0.05,max=0.5, label = "Hair clump radius: 0.09")
        self.clumpRadius.label.setPosition([20,215,8])
        self.clumpChildren= gui3d.Slider(self, position=[10, 295, 9], value=0, min=0, max=150, label = "Hair clump children: 0")
        self.clumpChildren.label.setPosition([20,280,8])
        self.multiStrand= gui3d.Slider(self, position=[10, 360, 9], value=0, min=0, max=150, label = "Multistrand children: 0")
        self.multiStrand.label.setPosition([20,345,8])


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


