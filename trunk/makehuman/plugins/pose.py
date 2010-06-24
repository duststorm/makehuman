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
        self.trasl = {}
        self.rot = {}       
           

                    
        sData = os.listdir("data/targets/poseengine/female-young/right-shoulder/r-shoulder")      
        for dat in sData:
            if dat not in ("shoulder-girdle",".svn"):        
                sample = [float(x) for x in dat.split('_')]               
                self.shoulderSamples.append(sample)
        
       
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

            
    def calcIAS(self,d1,d2):
    #Index of Angle Similarity
        D = d1+d2
        IAS1 = 1-(d1/D)
        IAS2 = 1-(d2/D)
        return IAS1,IAS2

    def calcIAR(self,v1,v2):
    #Index of Angle Ratio
        l1 = aljabr.vlen(v1)
        l2 = aljabr.vlen(v2)
        return l1/l2
        


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
        
        
    def seekNearestSamples(self,angle):
        direction = aljabr.vnorm(angle)
        similarity = {}
        for sample in self.shoulderSamples:
            direction2 = aljabr.vnorm(sample)
            similarity[aljabr.vdist(direction,direction2)] = sample                
        d = similarity.keys()
        d.sort()
        nearestSample1 = similarity[d[0]]
        nearestSample2 = similarity[d[1]]
        IAS1,IAS2 = self.calcIAS(d[0],d[1])
        IAR1 = self.calcIAR(angle, nearestSample1)
        IAR2 = self.calcIAR(angle, nearestSample2)
        factor1 = IAS1* IAR1
        factor2 = IAS2* IAR2
        print "DEBUG",nearestSample2,nearestSample1
        if factor1 > 1 or factor2 >1:
            print "WARNING. Angle %f,%f,%f is impossible for human shoulder"% (angle[0],angle[1],angle[2])        
        return (nearestSample1,nearestSample2,factor1,factor2)

        
    def applyShoulderTargets(self,angle):
        
        shoulderDir = "data/targets/poseengine/female-young/right-shoulder/r-shoulder"
        samples = self.seekNearestSamples(angle)
        target1 = "_".join([str(int(x)) for x in samples[0]])
        target2 = "_".join([str(int(x)) for x in samples[1]])
        morphVal1 = samples[2]
        morphVal2 = samples[3]
        
        path1 = os.path.join(shoulderDir,target1)
        path2 = os.path.join(shoulderDir,target2)
        print "-------"
        self.storeTargetsFromFolder(path1,morphVal1)
        self.storeTargetsFromFolder(path2,morphVal2)  
 
        
        
    def storeTargetsFromFolder(self,path,morphFactor):
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
                    
        rotations.sort()
        traslations.sort()
         
        for targetPath in traslations:
            self.trasl[targetPath] = morphFactor
        for targetPath in rotations:
            self.rot[targetPath] = morphFactor  
             
                
 
            
        
    #maybe this should be moved in human class
    def applyPose(self):
        self.rot = {}
        self.trasl = {}
        
        self.app.scene3d.selectedHuman.restoreMesh() #restore the mesh without rotations
        
        angle = (self.shoulderX,self.shoulderY,self.shoulderZ)
        self.applyShoulderTargets(angle)
        
        rotPaths = self.rot.keys()
        traslPaths = self.trasl.keys()
        
        rotPaths.sort()
        traslPaths.sort()
        
        for targetPath in traslPaths:
            morphFactor = self.trasl[targetPath]
            algos3d.loadTranslationTarget(self.app.scene3d.selectedHuman.meshData, targetPath, morphFactor, None, 1, 0)
        for targetPath in rotPaths:
            morphFactor = self.rot[targetPath]
            algos3d.loadRotationTarget(self.app.scene3d.selectedHuman.meshData, targetPath, morphFactor)  
        
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


