import os.path
#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import math
#import poseengine
from aljabr import * #axisAngleToQuaternion, quaternionVectorTransform, degree2rad, vadd, vsub, vdist
from skeleton import Skeleton
print 'Pose2 plugin imported'


jointZones = ('l-eye','r-eye', 'jaw', 'nose', 'mouth', 'head', 'neck', #'torso', 
'r-torso-clavicle', 'l-torso-clavicle', 'hip', 'pelvis', 'r-upperarm', 'l-upperarm', 'r-lowerarm', 'l-lowerarm', 'l-hand', 'r-hand', 'r-upperleg', 'l-upperleg', 'r-lowerleg', 'l-lowerleg', 'l-foot', 'r-foot')

zonesToJointsMapping = {
    'pelvis':'joint-pelvis',
    'hip':'joint-spine-2',
     #'torso':'joint-spine-1',
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
        gui3d.TaskView.__init__(self, category, 'Pose2')      

        self.jointSelected = False
        self.zone = ""
        self.skeleton = Skeleton()
        self.selectedGroups = []
        self.joint = None
                
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Rotation', gui3d.GroupBoxStyle._replace(height=25+36*3+4+24*3+6));y+=25

        self.Xslider = gui3d.Slider(self, position=[10, y, 9.3], value = 0.0, min = -180.0, max = 180.0, label = "RotX: %d");y+=36
        self.Yslider = gui3d.Slider(self, position=[10, y, 9.3], value = 0.0, min = -180.0, max = 180.0, label = "RotY: %d");y+=36
        self.Zslider = gui3d.Slider(self, position=[10, y, 9.3], value = 0.0, min = -180.0, max = 180.0, label = "RotZ: %d");y+=36
        y+=4

        self.resetPoseButton = gui3d.Button(self, [18, y, 9.5], "Reset");y+=24
        self.testPoseButton = gui3d.Button(self, [18, y, 9.5], "Test");y+=24
        
        self.savePoseToggle = gui3d.CheckBox(self, [18, y, 9.5], "SavePose");y+=24

        @self.testPoseButton.event
        def onClicked(event):
            self.test()

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
        if not (self.jointSelected):
          human = self.app.selectedHuman
          groups = []
          self.zone = self.getJointZones(event.group.name)

          if self.zone:
              for g in human.mesh.facesGroups:
                  if self.zone in g.name:
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
        if self.jointSelected: 
            self.jointSelected = False
        else:
            self.joint = self.skeleton.getJoint(zonesToJointsMapping.get(self.zone))
            self.Xslider.setValue(self.joint.rotation[0])
            self.Yslider.setValue(self.joint.rotation[1])
            self.Zslider.setValue(self.joint.rotation[2])
            self.jointSelected = True


    
    def onShow(self, event):
        self.app.selectedHuman.storeMesh()
        self.skeleton.update(self.app.selectedHuman.meshData)
        gui3d.TaskView.onShow(self, event)

    def onHide(self, event):
        self.app.selectedHuman.restoreMesh()
        self.app.selectedHuman.meshData.update()
        gui3d.TaskView.onHide(self, event)
        
    def test(self):
        #get the group name involving the right arm
        human = self.app.selectedHuman.meshData
        self.skeleton.update(human)
        
        #for shoulder
        #j = self.skeleton.getJoint("joint-r-shoulder")
        
        j = self.skeleton.getJoint("joint-head")
        angle = 20
        axis = [1,0,0]
        #q = axisAngleToQuaternion(axis, angle*degree2rad)
        Ryxz = [-4.48*degree2rad,	-1.24*degree2rad,	-7.02*degree2rad]
        #deform(j, q , j.position, human.verts) 
        deform2(j, Ryxz , j.position, human.verts) 
        human.calcNormals()
        human.update()
        
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
    category = app.getCategory('Experiments')
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

def Oldtest(self):
    #get the group name involving the right arm
    self.skeleton.update(self.app.selectedHuman.meshData)
    #get the position of the right shoulder joint
    j = self.skeleton.getJoint("joint-r-shoulder")
    bindedVGroups = []
    for group in self.app.selectedHuman.meshData.facesGroups:
      if (group.name.startswith("r-hand") or group.name.startswith("r-upperarm") or \
      group.name.startswith("r-lowerarm") or (group.name.startswith("r-") and group.name.find("-shoulder") > -1)):
        bindedVGroups.append(group.name)
    bindedVGroups.append("r-torso-back-scapula")
    verts = self.app.selectedHuman.meshData.getVerticesAndFacesForGroups(bindedVGroups)[0]
    clavicle = self.skeleton.getJoint("joint-r-clavicle").position
    angle = -20
    #maximum rotation of shoulder joint about y-axis without clavicle joint rotation is 20
    q = axisAngleToQuaternion([0,1,0], -angle*degree2rad)
    #NOTE and todo: We need to use unmodified T-shaped base mesh when doing this operation
    j.radius = 0.4
    rotatedDist = angle*degree2rad*j.radius
    for v in verts:
      distClavicle = vdist(v.co,clavicle) #distance to clavicle
      dist = vdist(v.co, j.position) #distance to joint of interest
      dx = (dist*dist) - (j.radius*j.radius) #this can be negative if vertex is at the fingers, so qe dont do sqrt
      tempv = vadd(quaternionVectorTransform(q,vsub(v.co, j.position)), j.position) #supposing transformed vertex
      
      if (v.co[0] - j.position[0]> -0.1): #is vertex at the right side (arm) of joint of interest?
        v.co = tempv
      #else: #the vertex is in the clavicle area!
         #scalar = bump(distClavicle, 1.6)
         #newq = vadd(vmul(q,scalar), vmul([0,0,0,1],1-scalar))
         #newq = vnorm(newq)
         #v.co = vadd(quaternionVectorTransform(newq,vsub(v.co, j.position)), j.position)
        
    self.app.selectedHuman.meshData.calcNormals()
    self.app.selectedHuman.meshData.update()        

    
def deform(j, q, center, verts):
    for i in j.bindedVects:          
      v = verts[i]
      # commented for arm
      #if (v.co[0] - center[0]> -0.1): #is vertex at the right side (arm) of joint of interest?
      v.co = vadd(quaternionVectorTransform(q,vsub(v.co, center)), center)
    for child in j.children:
      deform(child, q, center, verts)

def deform2(j, Ryxz, center, verts):
    m = euler2matrix(Ryxz, "syxz")
    for i in j.bindedVects:          
      v = verts[i]
      # commented for arm
      #if (v.co[0] - center[0]> -0.1): #is vertex at the right side (arm) of joint of interest?
      v.co = vadd(mtransform(m,vsub(v.co, center)), center)
    for child in j.children:
      deform(child, Ryxz, center, verts)
