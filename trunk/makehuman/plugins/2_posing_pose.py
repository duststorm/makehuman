import os.path
#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import math
from aljabr import * #todo: import the necessities only
from skeleton import Skeleton
from mh2obj import exportObj
from mh import getPath
print 'Pose2 plugin imported'

exportPath = getPath('exports')

#torso comes after clavicle because of getJointZones :P
jointZones = ('l-eye','r-eye', 'jaw', 'nose', 'mouth', 'head', 'neck',  
'r-torso-clavicle', 'l-torso-clavicle', 'torso', 'hip', 'pelvis', 
'r-upperarm', 'l-upperarm', 'r-lowerarm', 'l-lowerarm', 'l-hand', 'r-hand', 'r-upperleg', 'l-upperleg', 'r-lowerleg', 'l-lowerleg', 'l-foot', 'r-foot')

zonesToJointsMapping = {
    'pelvis':'joint-pelvis',
    'hip':'joint-spine2',
    'torso':'joint-spine1',
    'neck':'joint-neck',
    'head':'joint-head',
    'r-eye':'joint-r-eye',
    'l-eye':'joint-l-eye',
    'l-torso-clavicle':'joint-l-clavicle',
    'l-upperarm':'joint-l-shoulder',
    'l-lowerarm':'joint-l-elbow',
    'l-hand':'joint-l-hand',
    'r-torso-clavicle':'joint-r-clavicle',
    'r-upperarm':'joint-r-shoulder',
    'r-lowerarm':'joint-r-elbow',
    'r-hand':'joint-r-hand',
    'l-upperleg':'joint-l-upper-leg',
    'l-lowerleg':'joint-l-knee',
    'l-foot':'joint-l-ankle',
    'r-upperleg':'joint-r-upper-leg',
    'r-lowerleg':'joint-r-knee',
    'r-foot':'joint-r-ankle'
}

class PoseTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Pose')      

        self.jointSelected = False
        self.zone = ""
        self.skeleton = Skeleton()
        self.selectedGroups = []
        self.joint = None
                
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Rotation', gui3d.GroupBoxStyle._replace(height=25+36*3+4+24*4+6));y+=25

        self.Xslider = gui3d.Slider(self, position=[10, y, 9.3], value = 0.0, min = -180.0, max = 180.0, label = "RotX: %d");y+=36
        self.Yslider = gui3d.Slider(self, position=[10, y, 9.3], value = 0.0, min = -180.0, max = 180.0, label = "RotY: %d");y+=36
        self.Zslider = gui3d.Slider(self, position=[10, y, 9.3], value = 0.0, min = -180.0, max = 180.0, label = "RotZ: %d");y+=36
        y+=4

        self.resetPoseButton = gui3d.Button(self, [18, y, 9.5], "Reset");y+=24
        self.savePoseButton = gui3d.Button(self, [18, y, 9.5], "Save");y+=24
        self.testButton = gui3d.Button(self, [18, y, 9.5], "Test");y+=24

        @self.testButton.event
        def onClicked(event):
            self.skinTest()
        
        @self.savePoseButton.event
        def onClicked(event):
            exportObj(self.app.selectedHuman.meshData, os.path.join(exportPath, "posed.obj"))

        @self.resetPoseButton.event
        def onClicked(event):
            self.reset(self.shoulder)

        @self.Xslider.event
        def onChange(value):
            if self.joint:
                rotation = [value - self.joint.rotation[0], 0.0, 0.0]
                self.joint.rotation[0] = value
                self.rotateJoint(self.joint, self.joint.position, rotation)
                self.app.selectedHuman.meshData.calcNormals()
                self.app.selectedHuman.meshData.update()
            
        @self.Xslider.event
        def onChanging(value):
            pass
            
        @self.Yslider.event
        def onChange(value):
            if self.joint:
                rotation = [0.0, value - self.joint.rotation[1], 0.0]
                self.joint.rotation[1] = value
                self.rotateJoint(self.joint, self.joint.position, rotation)
                self.app.selectedHuman.meshData.calcNormals()
                self.app.selectedHuman.meshData.update()
            
        @self.Yslider.event
        def onChanging(value):
            pass

        @self.Zslider.event
        def onChange(value):
            if self.joint:
                rotation = [0.0, 0.0, value - self.joint.rotation[2]]
                self.joint.rotation[2] = value
                self.rotateJoint(self.joint, self.joint.position,rotation)
                self.app.selectedHuman.meshData.calcNormals()
                self.app.selectedHuman.meshData.update()
            
        @self.Zslider.event
        def onChanging(value):
            pass
            
    def onMouseMoved(self, event):
        if not (self.joint): #(self.jointSelected):
          human = self.app.selectedHuman
          groups = []
          self.zone = self.getJointZones(event.group.name)

          if self.zone:
              for g in human.mesh.facesGroups:
                  if self.zone != "torso":
                    if self.zone in g.name:
                        groups.append(g)
                  elif (self.zone in g.name) and not g.name.endswith("clavicle"):
                    groups.append(g)

              for g in self.selectedGroups:
                  if g not in groups:
                      g.setColor([255, 255, 255, 255])

              for g in groups:
                  if g not in self.selectedGroups:
                      g.setColor([0, 169, 184, 255])
                    
              self.selectedGroups = groups
              self.app.redraw()
    
    def onMouseUp(self, event):
        if self.joint: 
            #self.jointSelected = False
            self.joint = None
        else:
            self.joint = self.skeleton.getJoint(zonesToJointsMapping.get(self.zone))
            self.Xslider.setValue(self.joint.rotation[0])
            self.Yslider.setValue(self.joint.rotation[1])
            self.Zslider.setValue(self.joint.rotation[2])
            #self.jointSelected = True
    
    def onShow(self, event):
        self.app.selectedHuman.storeMesh()
        self.skeleton.update(self.app.selectedHuman.meshData)
        gui3d.TaskView.onShow(self, event)

    def onHide(self, event):
        self.app.selectedHuman.restoreMesh()
        self.app.selectedHuman.meshData.update()
        gui3d.TaskView.onHide(self, event)
        
    def getJointZones(self, groupName):
        for k in jointZones:
            if k in groupName:
              return k
        return None
    
    def rotateJoint(self, joint, center, rotation, transform=None):                
        #src = self.app.selectedHuman.meshStored
        dst = self.app.selectedHuman.meshData.verts
        if not transform:
            transform = euler2matrix(vmul(rotation,degree2rad), "sxyz")
        else:
            joint.position = vadd(mtransform(transform, vsub(joint.position, center)),center)

        for i in joint.bindedVects:
            dst[i].co = vadd(mtransform(transform, vsub(dst[i].co, center)),center)
        for child in joint.children:
            self.rotateJoint(child, center, rotation, transform)
    
    def skinTest(self):
        #rotating the shoulders in z desu..
        theta = -45
        rotation = [0.0, 0.0, theta]
        joint = self.skeleton.getJoint('joint-r-shoulder')
        dst = self.app.selectedHuman.meshData.verts
        center = joint.position
        transform = euler2matrix(vmul(rotation,degree2rad), "sxyz")
        joint.radius = 0.6
        l = math.fabs(theta*degree2rad*joint.radius)
        
        for i in joint.bindedVects:
            v= dst[i].co
            d = math.fabs(v[0]-center[0])
            #skinning upper part of shoulder, shape should be like a sphere 
            if d < l and v[1] > center[1]:
              #print "Geronimo"
              #theta = math.fabs(v[0] - center[0])/joint.radius #in radians
              theta2 = theta*(1-bump(d, l))
              t = euler2matrix([0,0,theta2*degree2rad], "sxyz")
              #x = center[0] + joint.radius * math.sin(theta)
              #y = center[1] + joint.radius * math.cos(theta)
              #z = v[2]
              dst[i].co = vadd(mtransform(t, vsub(v, center)),center)
            else:
              dst[i].co = vadd(mtransform(transform, vsub(v, center)),center)
        for child in joint.children:
            self.rotateJoint(child, joint.position, rotation, transform)
        
        self.app.selectedHuman.meshData.calcNormals()
        self.app.selectedHuman.meshData.update()
    
    def reset(self, limbToTest):
        self.Xslider.setValue(0.0)
        self.Yslider.setValue(0.0)
        self.Zslider.setValue(0.0)
        self.app.redraw()
        

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Posing')
    taskview = PoseTaskView(category)
    print 'pose loaded'
            
    @taskview.event
    def onMouseDown(event):
        part = app.scene3d.getSelectedFacesGroup()
        print part.name

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements

def unload(app):
    print 'pose unloaded'

    
"""
TEST STUFFS

joints[0] is the root of the joint linkage
given a positon v in the mesh, compute the weight of the vertex with respect to the joint
len(widths) = len(joints)
len(dist) = len(joints)
len(dist[i]) = 2*len(joints)-1 for all i = 1,..., len(joints)
"""