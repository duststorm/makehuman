import os.path
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
        gui3d.TaskView.__init__(self, category, 'Posing')      

        self.engine = poseengine.Poseengine(self.app.scene3d.selectedHuman)        
        self.shoulder = self.engine.getLimb("joint-r-shoulder")
        self.shoulder.oBoundingBox = [[0.0, 8.1955895],[3.674790375, 6.1586085],[-1.120018, 1.192948875]]
        self.shoulder.rotOrder = "xzy"
        
        self.shoulder.keyRot0 = [-90,90]
        self.shoulder.keyRot1 = [-135,-67,0,45]
        self.shoulder.keyRot2 = [-115,-90,-67,-45,-22,0,22,45,67,90]

        gui3d.GroupBox(self, label = 'Shoulder', position=[10, 80, 9.0], width=128, height=256)

        self.shoulderXslider = gui3d.Slider(self, position=[10, 115, 9.3], value = 0.0, min = -85, max = 80, label = "RotX: 0")
        self.shoulderYslider = gui3d.Slider(self, position=[10, 155, 9.3], value = 0.0, min = -140, max = 50, label = "RotY: 0")
        self.shoulderZslider = gui3d.Slider(self, position=[10, 195, 9.3], value = 0.0, min = -120, max = 90, label = "RotZ: 0")

        self.savePoseFiles = 0

        self.resetPoseButton = gui3d.Button(self, [18, 235, 9.5], "Reset")
        self.testPoseButton = gui3d.Button(self, [18, 265, 9.5], "Test")
        
        self.savePoseToggle = gui3d.CheckBox(self, [18, 295, 9.5], "SavePose")

        @self.savePoseToggle.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.savePoseToggle, event)
            if self.savePoseToggle.selected:
                print "Save Pose activated"
            else:
                print "Save Pose deactivated"

        @self.testPoseButton.event
        def onClicked(event):
            self.test(self.shoulder)

        @self.resetPoseButton.event
        def onClicked(event):
            self.reset(self.shoulder)

        @self.shoulderXslider.event
        def onChange(value):            
            self.shoulder.angle[0] = value
            self.shoulder.applyPose()
            self.shoulderXslider.label.setText('RotX: %d' % value)
            
        @self.shoulderYslider.event
        def onChange(value):            
            self.shoulder.angle[1] = value 
            self.shoulder.applyPose()
            self.shoulderYslider.label.setText('RotY: %d' % value)

        @self.shoulderZslider.event
        def onChange(value):
            self.shoulder.angle[2] = value 
            self.shoulder.applyPose()
            self.shoulderZslider.label.setText('RotZ: %d' % value)
            
    def onShow(self, event):
        self.app.scene3d.selectedHuman.storeMesh()
        #self.applyPose()
        gui3d.TaskView.onShow(self, event)

    def onHide(self, event):
        self.app.scene3d.selectedHuman.restoreMesh()
        self.app.scene3d.selectedHuman.meshData.update()
        gui3d.TaskView.onHide(self, event)

    def test(self, limbToSave, sliderX,sliderY,sliderZ,savePose = None):

        homedir = os.path.expanduser('~')
        if self.savePoseToggle.selected:
            poseDir = os.path.join(homedir, limbToSave.name)
            if not os.path.isdir(poseDir):
                os.mkdir(poseDir)

        for angle in limbToSave.examplesTrasl:
            
            if self.savePoseToggle.selected:
                tName = "limb_%s_%s_%s.pose"%(angle[0],angle[1],angle[2])
                savePath = os.path.join(poseDir,tName)
                print "saved in %s"%(savePath)

            self.shoulderXslider.label.setText('RotX: %d'%(angle[0]))
            self.shoulderYslider.label.setText('RotY: %d'%(angle[1]))
            self.shoulderZslider.label.setText('RotZ: %d'%(angle[2]))
            self.shoulderXslider.setValue(angle[0])
            self.shoulderYslider.setValue(angle[1])
            self.shoulderYslider.setValue(angle[2])
            limbToSave.angle = angle
            limbToSave.applyPose(savePath)
            self.app.scene3d.redraw(0)


    def reset(self, limbToTest):
        limbToTest.angle = [0,0,0]        
        self.shoulderXslider.label.setText('RotX: 0')
        self.shoulderYslider.label.setText('RotY: 0')
        self.shoulderZslider.label.setText('RotZ: 0')
        self.shoulderXslider.setValue(0.0)
        self.shoulderYslider.setValue(0.0)
        self.shoulderZslider.setValue(0.0)
        limbToTest.applyPose()
        self.app.scene3d.redraw(0)
        

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Experiments')
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
            trans = app.modelCamera.convertToScreen(trans[0], trans[1], trans[2])
            trans[0] += diff[0]
            trans[1] += diff[1]
            trans = app.modelCamera.convertToWorld3D(trans[0], trans[1], trans[2])
            human.setPosition(trans)
    @taskview.event
    def onMouseDown(event):
        part = app.scene3d.getSelectedFacesGroup()
        print part.name

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements

def unload(app):
    print 'pose unloaded'

