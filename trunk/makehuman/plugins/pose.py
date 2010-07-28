#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import mh
import os
import algos3d
import aljabr
import math
import poseengine
print 'Pose plugin imported'


class PoseTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Example', category.app.getThemeResource('images', 'button_pose.png'))      

        self.engine = poseengine.Poseengine(self.app.scene3d.selectedHuman)        
        self.shoulder = self.engine.getLimb("joint-r-shoulder")
        self.shoulder.rotOrder = "xzy"

        self.shoulderXslider = gui3d.Slider(self, position=[10, 100, 9.5], value = 0.0, min = -85, max = 80, label = "Shoulder RotX")
        self.shoulderYslider = gui3d.Slider(self, position=[10, 140, 9.5], value = 0.0, min = -140, max = 50, label = "Shoulder RotY")
        self.shoulderZslider = gui3d.Slider(self, position=[10, 180, 9.5], value = 0.0, min = -120, max = 90, label = "Shoulder RotZ")


        self.shoulderXLabel = gui3d.TextView(self, mesh='data/3dobjs/empty.obj', position=[180, 100, 9.5])
        self.shoulderYLabel = gui3d.TextView(self, mesh='data/3dobjs/empty.obj', position=[180, 140, 9.5])
        self.shoulderZLabel = gui3d.TextView(self, mesh='data/3dobjs/empty.obj', position=[180, 180, 9.5])


        self.shoulderXLabel.setText('0')
        self.shoulderYLabel.setText('0')
        self.shoulderZLabel.setText('0')

        self.resetPoseButton = gui3d.Button(self, mesh='data/3dobjs/button_standard.obj', label = "Reset", position=[50, 240, 9.5])
        self.testPoseButton = gui3d.Button(self, mesh='data/3dobjs/button_standard.obj', label = "Test", position=[50, 260, 9.5])
            

        @self.testPoseButton.event
        def onClicked(event):
            self.testShoulder()

        @self.resetPoseButton.event
        def onClicked(event):
            self.resetShoulder()

        @self.shoulderXslider.event
        def onChange(value):            
            self.shoulder.angle[0] = value
            self.shoulderXLabel.setText('%d' % value)
            self.shoulder.applyPose()            

        @self.shoulderYslider.event
        def onChange(value):            
            self.shoulder.angle[1] = value 
            self.shoulderYLabel.setText('%d' % value)
            self.shoulder.applyPose()           

        @self.shoulderZslider.event
        def onChange(value):
            self.shoulder.angle[2] = value 
            self.shoulderZLabel.setText('%d' % value)
            self.shoulder.applyPose()
            
    def onShow(self, event):
        self.app.scene3d.selectedHuman.storeMesh()
        #self.applyPose()
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
    print 'pose unloaded'

