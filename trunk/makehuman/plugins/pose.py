#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import mh
import os
import algos3d
import aljabr
print 'Pose plugin imported'


class PoseTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Example', category.app.getThemeResource('images', 'button_pose.png'))        
        
        
        self.shoulderX = 0       
        self.shoulderY = 0 
        self.shoulderZ = 0
        self.shoulderSamples = []
        
        sData = os.listdir("data/targets/poseengine/female-young/right-shoulder")      
        for dat in sData:
            if dat not in ("shoulder-girdle",".svn"):
                d = dat.split('_')
                x = float(d[0])
                y = float(d[1])
                z = float(d[2])
                for i in xrange(1,10):
                    i = float(i)/10.0
                    fillerSample = (x*i,y*i,z*i,x,y,z,i)                   
                    self.shoulderSamples.append(fillerSample)
        
       
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

        @self.resetPoseButton.event
        def onClicked(event):
            self.resetShoulder()           
            
        @self.shoulderXslider.event
        def onChange(value):
            self.shoulderX = value
            self.shoulderXLabel.setText('%d' % self.shoulderX)
            self.applyPose()

        @self.shoulderYslider.event
        def onChange(value):
            self.shoulderY = value
            self.shoulderYLabel.setText('%d' % self.shoulderY)
            self.applyPose()

        @self.shoulderZslider.event
        def onChange(value):
            self.shoulderZ = value
            self.shoulderZLabel.setText('%d' % self.shoulderZ)
            self.applyPose()


    def resetShoulder(self):
        self.shoulderX = 0       
        self.shoulderY = 0 
        self.shoulderZ = 0
        self.shoulderXslider.setValue(0.0)
        self.shoulderYslider.setValue(0.0)
        self.shoulderZslider.setValue(0.0)
        self.shoulderXLabel.setText('0')
        self.shoulderYLabel.setText('0')        
        self.shoulderZLabel.setText('0')
        self.applyPose()

        
    def applyShoulderTargets(self,angle):

        dirpath = "data/targets/poseengine/female-young/right-shoulder"
        closerSamples = {}
        for s in self.shoulderSamples:
            s1 = (s[0],s[1],s[2])
            d = aljabr.vdist(angle,s1)
            closerSamples[d] = s
            
        k = closerSamples.keys()
        k.sort()

        print "K ", k[0],k[1],k[2]
        #Normalize 1. "+0.001" is to prevent division by zero.
        weight1 = (k[0]+0.001)/(k[0]+0.001)
        weight2 = (k[0]+0.001)/(k[1]+0.001)
        weight3 = (k[0]+0.001)/(k[2]+0.001)

        #Normalize 2. "+0.001" is to prevent division by zero.
        n = weight1+weight2+weight3+0.001
        weight1 = weight1/n
        weight2 = weight2/n
        weight3 = weight3/n

        sample1 = closerSamples[k[0]]
        sample2 = closerSamples[k[1]]
        sample3 = closerSamples[k[2]]
        
        sampleTarget1 = str(int(sample1[3]))+"_"+str(int(sample1[4]))+"_"+str(int(sample1[5]))
        sampleTarget2 = str(int(sample2[3]))+"_"+str(int(sample2[4]))+"_"+str(int(sample2[5]))
        sampleTarget3 = str(int(sample3[3]))+"_"+str(int(sample3[4]))+"_"+str(int(sample3[5]))
        
        morphVal1 = sample1[6]*weight1
        morphVal2 = sample2[6]*weight2
        morphVal3 = sample3[6]*weight3
        
        path1 = os.path.join(dirpath,sampleTarget1)
        path2 = os.path.join(dirpath,sampleTarget2)
        path3 = os.path.join(dirpath,sampleTarget3)
        
        print "-------"
        self.applyTargetsInFolder(path1,morphVal1)
        self.applyTargetsInFolder(path2,morphVal2)
        self.applyTargetsInFolder(path3,morphVal3)          
 
 
    def applyTargetsInFolder(self,path,morphFactor):
        print path,morphFactor
        targets = os.listdir(path)        
        traslations = []
        rotations = []
        for t in targets:
            tpath = os.path.join(path,t)            
            if os.path.isfile(tpath):
                if os.path.splitext(t)[1] == ".rot":
                    rotations.append(tpath)
                if os.path.splitext(t)[1] == ".target":
                    traslations.append(tpath)
         
        for targetPath in traslations:
            algos3d.loadTranslationTarget(self.app.scene3d.selectedHuman.meshData, targetPath, morphFactor, None, 1, 0)
        for targetPath in rotations:
            algos3d.loadRotationTarget(self.app.scene3d.selectedHuman.meshData, targetPath, morphFactor)               
                
 
            
        
    #maybe this should be moved in human class
    def applyPose(self):
        
        self.app.scene3d.selectedHuman.restoreMesh() #restore the mesh without rotations
        
        angle = (self.shoulderX,self.shoulderY,self.shoulderZ)
        self.applyShoulderTargets(angle)
        
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


