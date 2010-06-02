#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import mh
print 'Pose plugin imported'


class PoseTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Example', category.app.getThemeResource('images', 'button_pose.png'))        
        
        
        self.acromioclavicularAbductionVal = 0       
        self.acromioclavicularProtractionVal = 0 
        self.sternoclavicularAbductionVal = 0 
        self.sternoclavicularProtractionVal = 0 
        self.lordosiVal = 0
        self.testVal = 0
        self.test2Val = 0
       
        self.acromioclavicularAbductionSlider = gui3d.Slider(self, position=[10, 100, 9.5], value = 0.0, label = "Acromio Abdct")
        self.acromioclavicularProtractionSlider = gui3d.Slider(self, position=[10, 140, 9.5], value = 0.0, label = "Acromnio Protr")
        self.sternoclavicularAbductionSlider = gui3d.Slider(self, position=[10, 220, 9.5], value = 0.0, label = "Sterno Abdct")
        self.sternoclavicularProtractionSlider = gui3d.Slider(self, position=[10, 180, 9.5], value = 0.0, label = "Sterno Protr")
        #self.lordosiSlider = gui3d.Slider(self, position=[10, 260, 9.5], value = 0.0, label = "Lordosi")
        self.testSlider = gui3d.Slider(self, position=[10, 300, 9.5], value = 0.0, label = "test")
        self.test2Slider = gui3d.Slider(self, position=[10, 340, 9.5], value = 0.0, label = "test2")
           
            
        @self.acromioclavicularAbductionSlider.event
        def onChange(value):
            self.acromioclavicularAbductionVal = value
            self.applyPose() 
            
        @self.acromioclavicularProtractionSlider.event
        def onChange(value):
            self.acromioclavicularProtractionVal = value
            self.applyPose()
            
        @self.sternoclavicularAbductionSlider.event
        def onChange(value):
            self.sternoclavicularAbductionVal = value
            self.applyPose()
            
        @self.sternoclavicularProtractionSlider.event
        def onChange(value):
            self.sternoclavicularProtractionVal = value
            self.applyPose()
            
        #@self.lordosiSlider.event
        #def onChange(value):
            #self.lordosiVal = value
            #self.applyPose()
            
        @self.testSlider.event
        def onChange(value):
            self.testVal = value
            self.applyPose()
            
        @self.test2Slider.event
        def onChange(value):
            self.test2Val = value
            self.applyPose()
        
    #maybe this should be moved in human class
    def applyPose(self):
        
        self.app.scene3d.selectedHuman.restoreMesh() #restore the mesh without rotations
        
        #Now all rotations are applied, taking account of hierarchy.
        self.app.scene3d.selectedHuman.rotateLimb("data/targets/poseengine/female-young/right-shoulder/shoulder-girdle/test", self.testVal)
        self.app.scene3d.selectedHuman.rotateLimb("data/targets/poseengine/female-young/right-shoulder/shoulder-girdle/acromioclavicular-abduction", self.acromioclavicularAbductionVal)
        self.app.scene3d.selectedHuman.rotateLimb("data/targets/poseengine/female-young/right-shoulder/shoulder-girdle/acromioclavicular-protraction", self.acromioclavicularProtractionVal)
        self.app.scene3d.selectedHuman.rotateLimb("data/targets/poseengine/female-young/right-shoulder/shoulder-girdle/sternoclavicular-abduction", self.sternoclavicularAbductionVal)
        self.app.scene3d.selectedHuman.rotateLimb("data/targets/poseengine/female-young/right-shoulder/shoulder-girdle/sternoclavicular-protraction", self.sternoclavicularProtractionVal)
        #self.app.scene3d.selectedHuman.rotateLimb("data/targets/poseengine/female-young/right-shoulder/shoulder-girdle/lordosi", self.lordosiVal)
        self.app.scene3d.selectedHuman.rotateLimb("data/targets/poseengine/female-young/right-shoulder/shoulder-girdle/test2", self.test2Val)
        self.app.scene3d.selectedHuman.meshData.calcNormals(facesToUpdate=[f for f in self.app.scene3d.selectedHuman.meshData.faces])
        self.app.scene3d.selectedHuman.meshData.update()
        #self.app.scene3d.redraw()
        


    def onShow(self, event):
        self.app.scene3d.selectedHuman.storeMesh()
        self.applyPose()
        gui3d.TaskView.onShow(self, event)
       
    def onHide(self, event):
        self.app.scene3d.selectedHuman.restoreMesh()
        self.app.scene3d.selectedHuman.meshData.update()
        gui3d.TaskView.onHide(self, event)
        
category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = gui3d.Category(app, 'Example', app.getThemeResource('images', 'button_pose.png'))
    taskview = PoseTaskView(category)
    print 'pose loaded'
    
    @taskview.event
    def onMouseWheel(event):
        if event.wheelDelta > 0:
            mh.cameras[0].eyeZ -= 0.65
            app.scene3d.redraw()
        else:
            mh.cameras[0].eyeZ += 0.65
            app.scene3d.redraw()

    @taskview.event
    def onMouseDragged(event):
        diff = app.scene3d.getMouseDiff()
        leftButtonDown = event.button & 1
        middleButtonDown = event.button & 2
        rightButtonDown = event.button & 4

        if leftButtonDown and rightButtonDown or middleButtonDown:
            mh.cameras[0].eyeZ += 0.05 * diff[1]
        elif leftButtonDown:
            human = app.scene3d.selectedHuman
            rot = human.getRotation()
            rot[0] += 0.5 * diff[1]
            rot[1] += 0.5 * diff[0]
            human.setRotation(rot)
        elif rightButtonDown:
            human = app.scene3d.selectedHuman
            trans = human.getPosition()
            trans[0] += 0.1 * diff[0]
            trans[1] -= 0.1 * diff[1]
            human.setPosition(trans)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements

def unload(app):
    print 'example unloaded'


