#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
print 'Pose plugin imported'


class PoseTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Example', category.app.getThemeResource('images', 'button_pose.png'))        
        
        self.rscapulaProtractionVal = 0 
        self.rscapulaTiltingUpVal = 0       
        
        self.rscapulaProtractionSlider = gui3d.Slider(self, position=[10, 100, 9.5], value = 0.0, label = "Scapula protraction")
        self.rscapulaTiltingUpSlider = gui3d.Slider(self, position=[10, 140, 9.5], value = 0.0, label = "Scapula tilting up")


        @self.rscapulaProtractionSlider.event
        def onChange(value):
            self.rscapulaProtractionVal = value
            self.applyPose()   
            
        @self.rscapulaTiltingUpSlider.event
        def onChange(value):
            self.rscapulaTiltingUpVal = value
            self.applyPose() 
        
    #maybe this should be moved in human class
    def applyPose(self):
        self.app.scene3d.selectedHuman.restoreMesh() #restore the mesh without rotations
        
        #Now all rotations are applied, taking account of hierarchy.
        self.app.scene3d.selectedHuman.rotateLimb("data/targets/poseengine/female-young/right-shoulder/shoulder-girdle/rscapula-tilting-up", self.rscapulaTiltingUpVal)
        self.app.scene3d.selectedHuman.rotateLimb("data/targets/poseengine/female-young/right-shoulder/shoulder-girdle/rscapula-protraction", self.rscapulaProtractionVal)


    def onShow(self, event):
        self.app.scene3d.selectedHuman.storeMesh()
        gui3d.TaskView.onShow(self, event)
        
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


