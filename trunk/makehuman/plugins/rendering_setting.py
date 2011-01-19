#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
class RenderingSettingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Rendering Setting', label='Settings')

        #Rendering resolution
        gui3d.GroupBox(self, [10, 80, 9.0], 'Resolution', gui3d.GroupBoxStyle._replace(height=128))
        self.widthSize= gui3d.Slider(self, position=[10, 115, 9.1], value=800, min=10, max=5000, label = "Width: 800")
        self.heightSize= gui3d.Slider(self, position=[10, 155, 9.1], value=600, min=10, max=5000, label = "Height: 600")

        #Hair data
        gui3d.GroupBox(self, [10, 215, 9.0], 'Hair', gui3d.GroupBoxStyle._replace(height=256))
        self.clumpRadius = gui3d.Slider(self, position=[10, 250, 9.3], value=0.09, min=0.05,max=0.5, label = "Clump radius: 0.09")
        self.clumpChildren= gui3d.Slider(self, position=[10, 300, 9.3], value=0, min=0, max=150, label = "Clump children: 0")
        self.multiStrand= gui3d.Slider(self, position=[10, 350, 9.3], value=0, min=0, max=150, label = "Multistrand children: 0")
        self.randomHair= gui3d.Slider(self, position=[10, 400, 9.3], value=0.04, min=0.0, max=0.5, label = "Randomness: 0.04")


        self.human = self.app.scene3d.selectedHuman

        @self.clumpRadius.event
        def onChanging(value):
            self.clumpRadius.label.setText("Clump radius: "+str(round(self.clumpRadius.getValue(),4)))
            self.human.hairs.interpolationRadius = self.clumpRadius.getValue()

        @self.clumpChildren.event
        def onChanging(value):
            self.clumpChildren.label.setText("Clump children: "+str(self.clumpChildren.getValue()))
            self.human.hairs.clumpInterpolationNumber = self.clumpChildren.getValue()
            
        @self.multiStrand.event
        def onChanging(value):
            self.multiStrand.label.setText("Multistrand children: "+str(self.multiStrand.getValue()))
            self.human.hairs.multiStrandNumber = self.multiStrand.getValue()
        
        @self.randomHair.event
        def onChanging(value):
            self.randomHair.label.setText("Randomness: "+str(round(self.randomHair.getValue(),4)))
            self.human.hairs.randomness = self.randomHair.getValue()


        @self.widthSize.event
        def onChanging(value):
            self.widthSize.label.setText("Width: "+str(self.widthSize.getValue()))
            self.app.settings['rendering_width'] = self.widthSize.getValue() #Using global dictionary in app for global settings

        @self.heightSize.event
        def onChanging(value):
            self.heightSize.label.setText("Height: "+str(self.heightSize.getValue()))
            self.app.settings['rendering_height'] = self.heightSize.getValue() #Using global dictionary in app for global settings


def load(app):
    category = app.getCategory('Rendering')
    taskview = RenderingSettingTaskView(category)
    print 'Rendering setting imported'

def unload(app):
    pass


