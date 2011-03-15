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
from math import pi
import mh

class BvhView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'BVH Player')
        
        self.status = gui3d.TextView(self, [10, 585, 9.1])
        
        self.__skeleton = bvhSkeleton('data/bvhs/10_01.bvh')
        self.__skeleton.updateFrame(-1)
        self.__skeletonMesh = None
        self.__skeletonObject = None
        
        self.bone = None
        
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+36*1+24*1+6));y+=25

        self.frameSlider = gui3d.Slider(self, position=[10, y, 9.3], value = 0, min = 0, max = self.__skeleton.frames, label = "Frame: 0");y+=36
        self.playPause = gui3d.Button(self, [18, y, 9.3], "Play");y+=24
            
        @self.frameSlider.event
        def onChanging(value):
            self.frameSlider.label.setText('Frame: %d' % value)
            self.__updateSkeletonMesh(value-1)
            
        @self.frameSlider.event
        def onChange(value):
            self.frameSlider.label.setText('Frame: %d' % value)
            self.__updateSkeletonMesh(value-1)
                
        @self.playPause.event
        def onClicked(value):
            if self.playPause.label.getText() == 'Play':
                self.playPause.label.setText('Pause')
                self.timer = mh.addTimer(int(self.__skeleton.frameTime * 1000), self.onFrameChanged)
            else:
                self.playPause.label.setText('Play')
                mh.removeTimer(self.timer)
                
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
        
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        
        self.app.selectedHuman.show()
        self.getSkeleton().hide()
        
    def getSkeleton(self):
        
        human = self.app.selectedHuman
        
        if not self.__skeletonObject:
            
            self.__buildSkeletonMesh()
            self.__skeletonObject = gui3d.Object(self, human.getPosition(), self.__skeletonMesh)
            self.app.scene3d.update()
            
        else:
            
            self.__skeletonObject.setPosition(human.getPosition())
        
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
            self.__addPrism(self.__skeletonMesh, joint.parent.position, joint.position, 'bone-' + joint.name)
        
        for child in joint.children:
            self.__buildBoneMesh(child)
            
    def __updateSkeletonMesh(self, frame):
        
        self.__skeleton.updateFrame(frame)
            
        index = 0
        self.__updateBoneMesh(self.__skeleton.root, index)
        
        self.__skeletonMesh.calcNormals()
        self.__skeletonMesh.update()
        
    def __updateBoneMesh(self, joint, index):
        
        if joint.parent:
            self.__updatePrism(self.__skeletonMesh, joint.parent.position, joint.position, index)
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
        p1 = aljabr.randomPointFromNormal(n) # a random point in the plane defined by 0,0,0 and n
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
        
    def __updatePrism(self, mesh, o, e, index):
            
        dir = aljabr.vsub(e, o) # direction vector from o to e
        len = aljabr.vlen(dir) # distance from o to e
        scale = 0.5 # the thickness is 10% of the length
        i = aljabr.vadd(o, aljabr.vmul(dir, 0.25)) # the thickest part is 25% from o
        n = aljabr.vmul(dir, 1.0 / len) # the normalized direction
        q = aljabr.axisAngleToQuaternion(n, pi / 2.0) # a quaternion to rotate the point p1 to obtain the other points
        p1 = aljabr.randomPointFromNormal(n) # a random point in the plane defined by 0,0,0 and n
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
            
        self.app.selectedHuman.hide()
        self.getSkeleton().show()
        
    def onMouseWheel(self, event):
        
        self.app.selectedHuman.show()
        self.getSkeleton().hide()
        
        gui3d.TaskView.onMouseWheel(self, event)
            
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
