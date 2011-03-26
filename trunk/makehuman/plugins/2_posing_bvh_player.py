#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

Skeleton visualizer
"""

import os.path
import gui3d
import module3d
import aljabr
from bvh_importer import bvhSkeleton
from skeleton import Skeleton
from math import pi
import mh

'''
bvhToMhMapping = {
    'Hips':'joint-pelvis',
    'LeftHip':'joint-r-upper-leg',
    'RightHip':'joint-l-upper-leg',
    'LeftKnee':'joint-r-knee',
    'RightKnee':'joint-l-knee',
    'LeftAnkle':'joint-r-ankle',
    'RightAnkle':'joint-l-ankle',
    'Chest':'joint-spine2',
    'CS_BVH':'joint-spine1',
    'LeftCollar':'joint-r-clavicle',
    'RightCollar':'joint-l-clavicle',
    'LeftShoulder':'joint-r-shoulder',
    'RightShoulder':'joint-l-shoulder',
    'LeftElbow':'joint-r-elbow',
    'RightElbow':'joint-l-elbow',
    'LeftWrist':'joint-r-hand',
    'RightWrist':'joint-l-hand',
    'Neck':'joint-neck',
    'Head':'joint-head'
}
'''

bvhToMhMapping = {
    'hip':'joint-pelvis',
    'abdomen':'joint-spine-2',
    'chest':'joint-spine-1',
    'neck':'joint-neck',
    'head':'joint-head',
    'leftEye':'joint-r-eye',
    'rightEye':'joint-l-eye',
    'rCollar':'joint-l-clavicle',
    'rShldr':'joint-l-shoulder',
    'rForeArm':'joint-l-elbow',
    'rHand':'joint-l-hand',
    'rThumb1':'joint-l-finger-1-1',
    'rThumb2':'joint-l-finger-1-2',
    'rIndex1':'joint-l-finger-2-1',
    'rIndex2':'joint-l-finger-2-2',
    'rMid1':'joint-l-finger-3-1',
    'rMid2':'joint-l-finger-3-2',
    'rRing1':'joint-l-finger-4-1',
    'rRing2':'joint-l-finger-4-2',
    'rPinky1':'joint-l-finger-5-1',
    'rPinky2':'joint-l-finger-5-2',
    'lCollar':'joint-r-clavicle',
    'lShldr':'joint-r-shoulder',
    'lForeArm':'joint-r-elbow',
    'lHand':'joint-r-hand',
    'lThumb1':'joint-r-finger-1-1',
    'lThumb2':'joint-r-finger-1-2',
    'lIndex1':'joint-r-finger-2-1',
    'lIndex2':'joint-r-finger-2-2',
    'lMid1':'joint-r-finger-3-1',
    'lMid2':'joint-r-finger-3-2',
    'lRing1':'joint-r-finger-4-1',
    'lRing2':'joint-r-finger-4-2',
    'lPinky1':'joint-r-finger-5-1',
    'lPinky2':'joint-r-finger-5-2',
    #'rButtock':'joint-l-upper-leg',
    'rThigh':'joint-l-upper-leg',
    'rShin':'joint-l-knee',
    'rFoot':'joint-l-ankle',
    #'lButtock':'joint-r-upper-leg',
    'lThigh':'joint-r-upper-leg',
    'lShin':'joint-r-knee',
    'lFoot':'joint-r-ankle'
}

mhToBvhMapping = dict([(value, key) for key, value in bvhToMhMapping.iteritems()])

class BvhView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'BVH Player')
        
        self.status = gui3d.TextView(self, [10, 585, 9.1])
        
        self.__skeleton = bvhSkeleton('data/bvhs/03_03.bvh')
        self.__skeleton.updateFrame(-1)
        self.__skeletonMesh = None
        self.__skeletonObject = None
        self.bone = None
        
        self.__humanSkeleton = Skeleton()
        
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=24+25+36*1+24*1+6));y+=25

        self.frameSlider = gui3d.Slider(self, position=[10, y, 9.3], value = 0, min = 0, max = self.__skeleton.frames, label = "Frame: 0");y+=36
        self.playPause = gui3d.Button(self, [18, y, 9.3], "Play");y+=24
        self.showHuman = gui3d.ToggleButton(self, [18,y,9.1],"Show Human"); y+=24
        
        @self.frameSlider.event
        def onChanging(value):
            self.frameSlider.label.setText('Frame: %d' % value)
            self.__updateSkeletonMesh(value-1)
            self.__updateHumanMesh(self.__humanSkeleton.root)
            self.app.selectedHuman.meshData.calcNormals()
            self.app.selectedHuman.meshData.update()
            
        @self.frameSlider.event
        def onChange(value):
            self.frameSlider.label.setText('Frame: %d' % value)
            self.__updateSkeletonMesh(value-1)
            self.__updateHumanMesh(self.__humanSkeleton.root)
            self.app.selectedHuman.meshData.calcNormals()
            self.app.selectedHuman.meshData.update()
                
        @self.playPause.event
        def onClicked(value):
            if self.playPause.label.getText() == 'Play':
                self.playPause.label.setText('Pause')
                self.timer = mh.addTimer(max(30, int(self.__skeleton.frameTime * 1000)), self.onFrameChanged)
            else:
                self.playPause.label.setText('Play')
                mh.removeTimer(self.timer)
                
        @self.showHuman.event
        def onClicked(event):
            self.showHuman.setSelected(not self.showHuman.selected)
            if self.showHuman.selected:
                self.app.selectedHuman.show()
                self.getSkeleton().hide()
            else:
                self.app.selectedHuman.hide()
                self.getSkeleton().show()
                
    def onFrameChanged(self):
        
        frame = self.frameSlider.getValue() + 1
        
        if frame > self.frameSlider.max:
            frame = 1
            
        self.frameSlider.setValue(frame)
        self.__updateSkeletonMesh(frame-1)
        self.app.redraw()
            
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        
        self.app.selectedHuman.hide()
        self.getSkeleton().show()
        
        self.app.selectedHuman.storeMesh()
        self.__humanSkeleton.update(self.app.selectedHuman.meshData)
        
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        self.app.selectedHuman.show()
        self.getSkeleton().hide()
        
        self.app.selectedHuman.restoreMesh()
        self.app.selectedHuman.meshData.calcNormals()
        self.app.selectedHuman.meshData.update()
        
    def getSkeleton(self):
        
        human = self.app.selectedHuman
        
        if not self.__skeletonObject:
            
            self.__buildSkeletonMesh()
            self.__skeletonObject = gui3d.Object(self, aljabr.vadd(human.getPosition(), [0.0, -20.0, 0.0]), self.__skeletonMesh)
            self.app.scene3d.update()
            
        else:
            
            self.__skeletonObject.setPosition(aljabr.vadd(human.getPosition(), [0.0, -20.0, 0.0]))
        
        self.__skeletonObject.setRotation(human.getRotation())
        
        return self.__skeletonObject
        
    def __buildSkeletonMesh(self):
           
        self.__skeletonMesh = module3d.Object3D('skeleton')
        
        self.__skeletonMesh.uvValues = []
        self.__skeletonMesh.indexBuffer = []

        self.__buildBoneMesh(self.__skeleton.root)
        
        self.__skeletonMesh.setCameraProjection(0)
        self.__skeletonMesh.setShadeless(0)
        self.__skeletonMesh.setSolid(0)
        self.__skeletonMesh.calcNormals()
        self.__skeletonMesh.updateIndexBuffer()
        
    def __buildBoneMesh(self, joint):
         
        if joint.parent:
            position = [joint.transform[3],joint.transform[7],joint.transform[11]]
            parentPosition = [joint.parent.transform[3],
                              joint.parent.transform[7],
                              joint.parent.transform[11]]
            joint.p = self.__addPrism(self.__skeletonMesh, parentPosition, position, 'bone-' + joint.name)
            #joint.p = self.__addPrism(self.__skeletonMesh, joint.parent.position, joint.position, 'bone-' + joint.name)
        
        for child in joint.children:
            self.__buildBoneMesh(child)
            
    def __updateSkeletonMesh(self, frame):
        
        self.__skeleton.updateFrame(frame)
            
        index = 0
        self.__updateBoneMesh(self.__skeleton.root, index)
        
        self.__skeletonMesh.calcNormals()
        self.__skeletonMesh.update()

    def __updateHumanMesh(self, joint, src=None, dst=None):
        
        # copy angles
        bvhName = mhToBvhMapping.get(joint.name, '')
        if bvhName:
            bvhJoint = self.__skeleton.getJoint(bvhName)
            joint.rotation = bvhJoint.rotation[:]
            #joint.translation = bvhJoint.translation[:]
        else:
            joint.rotation = [0.0, 0.0, 0.0]
            #joint.translation = [0.0, 0.0, 0.0]
        joint.calcTransform(False)
        
        if not src:
            src = self.app.selectedHuman.meshStored
            
        if not dst:
            dst = self.app.selectedHuman.meshData.verts
            
        for i in joint.bindedVects:
            dst[i].co = aljabr.mtransform(joint.transform, aljabr.mtransform(joint.inverseTransform, src[i]))
        
        for child in joint.children:
            self.__updateHumanMesh(child, src, dst)
        
      #note: don't do skeleton update
      
    def __updateBoneMesh(self, joint, index):

        if joint.parent:
            position = [joint.transform[3],joint.transform[7],joint.transform[11]]
            parentPosition = [joint.parent.transform[3],
                              joint.parent.transform[7],
                              joint.parent.transform[11]]
            self.__updatePrism(self.__skeletonMesh, parentPosition, position, index, joint.p)
            index += 6
        
        for child in joint.children:
            index = self.__updateBoneMesh(child, index)
            
        return index
            
    def __addPrism(self, mesh, o=[0.0, 0.0, 0.0], e=[0.0, 1.0, 0.0], name='prism'):
            
        fg = mesh.createFaceGroup(name)

        dir = aljabr.vsub(e, o) # direction vector from o to e
        len = aljabr.vlen(dir) # distance from o to e
        scale = 0.5 # the thickness is 10% of the length
        i = aljabr.vadd(o, aljabr.vmul(dir, 0.25)) # the thickest part is 25% from o
        n = aljabr.vmul(dir, 1.0 / len) # the normalized direction
        q = aljabr.axisAngleToQuaternion(n, pi / 2.0) # a quaternion to rotate the point p1 to obtain the other points
        p = p1 = aljabr.randomPointFromNormal(n) # a random point in the plane defined by 0,0,0 and n
        p1 = aljabr.vmul(aljabr.vnorm(p1), scale) # the point scaled to the thickness
        p2 = aljabr.quaternionVectorTransform(q, p1) # the other points
        p3 = aljabr.quaternionVectorTransform(q, p2)
        p4 = aljabr.quaternionVectorTransform(q, p3)
        
        p1 = aljabr.vadd(i, p1) # translate by i since we were working in the origin
        p2 = aljabr.vadd(i, p2)
        p3 = aljabr.vadd(i, p3)
        p4 = aljabr.vadd(i, p4)

        # The 6 vertices
        v = []
        v.append(mesh.createVertex(o))      # 0             0
        v.append(mesh.createVertex(p1))     # 1            /|\
        v.append(mesh.createVertex(p2))     # 2           /.2.\
        v.append(mesh.createVertex(p3))     # 3          1` | `3
        v.append(mesh.createVertex(p4))     # 4          \`.4.`/ 
        v.append(mesh.createVertex(e))      # 5           \ | /
                                            #              \|/
                                            #               5
        
        # The 8 faces
        fg.createFace(v[0], v[1], v[4], v[0])
        fg.createFace(v[0], v[4], v[3], v[0])
        fg.createFace(v[0], v[3], v[2], v[0])
        fg.createFace(v[0], v[2], v[1], v[0])
        fg.createFace(v[5], v[4], v[1], v[5])
        fg.createFace(v[5], v[1], v[2], v[5])
        fg.createFace(v[5], v[2], v[3], v[5])
        fg.createFace(v[5], v[3], v[4], v[5])
        
        return p
            
    def __addCube(self, mesh, position=[0.0, 0.0, 0.0], scale=1.0, name='cube'):
            
        fg = mesh.createFaceGroup(name)

        # The 8 vertices
        v = []
        v.append(mesh.createVertex(aljabr.vadd(position, [-scale, -scale, -scale]))) # 0         /0-----1\
        v.append(mesh.createVertex(aljabr.vadd(position, [scale, -scale, -scale])))  # 1        / |     | \
        v.append(mesh.createVertex(aljabr.vadd(position, [scale, scale, -scale])))   # 2       |4---------5|
        v.append(mesh.createVertex(aljabr.vadd(position, [-scale, scale, -scale])))  # 3       |  |     |  |
        v.append(mesh.createVertex(aljabr.vadd(position, [-scale, -scale, scale])))  # 4       |  3-----2  |  
        v.append(mesh.createVertex(aljabr.vadd(position, [scale, -scale, scale])))   # 5       | /       \ |
        v.append(mesh.createVertex(aljabr.vadd(position, [scale, scale, scale])))    # 6       |/         \|
        v.append(mesh.createVertex(aljabr.vadd(position, [-scale, scale, scale])))   # 7       |7---------6|
        
        # The 6 faces
        fg.createFace(v[4], v[5], v[6], v[7]) # front
        fg.createFace(v[1], v[0], v[3], v[2]) # back
        fg.createFace(v[0], v[4], v[7], v[3]) # left
        fg.createFace(v[5], v[1], v[2], v[6]) # right
        fg.createFace(v[0], v[1], v[5], v[4]) # top
        fg.createFace(v[7], v[6], v[2], v[3]) # bottom
        
    def __updatePrism(self, mesh, o, e, index, p):
            
        dir = aljabr.vsub(e, o) # direction vector from o to e
        len = aljabr.vlen(dir) # distance from o to e
        scale = 0.5 # the thickness is 10% of the length
        i = aljabr.vadd(o, aljabr.vmul(dir, 0.25)) # the thickest part is 25% from o
        n = aljabr.vmul(dir, 1.0 / len) # the normalized direction
        q = aljabr.axisAngleToQuaternion(n, pi / 2.0) # a quaternion to rotate the point p1 to obtain the other points
        p1 = p # a random point in the plane defined by 0,0,0 and n
        p1 = aljabr.vmul(aljabr.vnorm(p1), scale) # the point scaled to the thickness
        p2 = aljabr.quaternionVectorTransform(q, p1) # the other points
        p3 = aljabr.quaternionVectorTransform(q, p2)
        p4 = aljabr.quaternionVectorTransform(q, p3)
        
        p1 = aljabr.vadd(i, p1) # translate by i since we were working in the origin
        p2 = aljabr.vadd(i, p2)
        p3 = aljabr.vadd(i, p3)
        p4 = aljabr.vadd(i, p4)

        # The 6 vertices
        mesh.verts[index].co = o
        mesh.verts[index+1].co = p1
        mesh.verts[index+2].co = p2
        mesh.verts[index+3].co = p3
        mesh.verts[index+4].co = p4
        mesh.verts[index+5].co = e
        
    def onMouseDragged(self, event):
      
      self.app.selectedHuman.show()
      self.getSkeleton().hide()
      
      gui3d.TaskView.onMouseDragged(self, event)
      if self.showHuman.selected:
        pass
      else:
        self.app.selectedHuman.hide()
        self.getSkeleton().show()
        
    def onMouseWheel(self, event):
      
      if self.showHuman.selected:
        pass
      else:
        self.app.selectedHuman.show()
        self.getSkeleton().hide()
      
      gui3d.TaskView.onMouseWheel(self, event)
      
      if self.showHuman.selected:
        pass
      else:
        self.app.selectedHuman.hide()
        self.getSkeleton().show()
        
    def onMouseEntered(self, event):
        
        gui3d.TaskView.onMouseEntered(self, event)
        
        if 'bone' in event.group.name:
            self.bone = event.group
            self.bone.setColor([0, 255, 0, 255])
            self.status.setText(event.group.name)
        self.app.redraw()

    def onMouseExited(self, event):
        
        gui3d.TaskView.onMouseExited(self, event)
        
        if self.bone:
            self.bone.setColor([255, 255, 255, 255])
            self.status.setText('')
        self.app.redraw()
        
    def onMouseMoved(self, event):
        
        gui3d.TaskView.onMouseMoved(self, event)
        
        if 'bone' in event.group.name and self.bone != event.group:
            self.bone.setColor([255, 255, 255, 255])
            self.bone = event.group
            self.bone.setColor([0, 255, 0, 255])
            self.status.setText(event.group.name)
        self.app.redraw()
        
    def onResized(self, event):
        
        self.status.setPosition([10, event[1]-15, 9.1])

def load(app):
    
    category = app.getCategory('Posing')
    taskview = BvhView(category)
    
    print 'BVH Player loaded'

def unload(app):
    pass
