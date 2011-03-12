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
from skeleton import Skeleton, Joint
from math import pi

class bvhJoint:
    
    def __init__(self, name):
        
        self.name = name
        self.offset = None
        self.channels = None
        self.parent = None
        self.children = []
        self.frames = []

class bvhImporter:
    
    def __init__(self, filename):
        
        self.file = open(filename, 'r')
            
        self.expectKeyword('HIERARCHY')
            
        items = self.expectKeyword('ROOT')
        
        root = bvhJoint(items[1])
        
        self.readJoint(root)
            
        # Read motion
        
        self.expectKeyword('MOTION')
        
        items = self.expectKeyword('Frames:')
        frames = int(items[1])
        items = self.expectKeyword('Frame') # Time:
        frameTime = float(items[2])
            
        for i in range(frames):
            
            line = self.file.readline()
            items = line.split()
            data = [float(item) for item in items]
            data = self.getChannelData(root, data)
                
    def readJoint(self, joint):
        
        self.expectKeyword('{')

        items = self.expectKeyword('OFFSET')
        joint.offset = [float(x) for x in items[1:]]
        
        items = self.expectKeyword('CHANNELS')
        joint.channels = items[1:]
        
        # Read child joints
        while 1:
            line = self.file.readline()
            items = line.split()
            
            if items[0] == 'JOINT':
                
                child = bvhJoint(items[1])
                joint.children.append(child)
                child.parent = joint
                self.readJoint(child)
                
            elif items[0] == 'End': # Site
                
                self.expectKeyword('{')
                self.expectKeyword('OFFSET')
                self.expectKeyword('}')
                
            elif items[0] == '}':
                
                break
                
            else:
                
                raise RuntimeError('Expected %s found %s' % ('JOINT, End Site or }', items[0]))
                    
    def expectKeyword(self, keyword):
        
        line = self.file.readline()
        items = line.split()
        
        if items[0] != keyword:
            raise RuntimeError('Expected %s found %s' % (keyword, items[0]))
                
        return items
        
    def getChannelData(self, joint, data):
        
        channels = len(joint.channels)
        joint.frames.append(data[0:channels])
        data = data[channels:]
        
        for child in joint.children:
            data = self.getChannelData(child, data)
        
        return data

class SkeletonView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Skeleton')
        
        self.status = gui3d.TextView(self, [10, 585, 9.1])
        
        self.__skeleton = Skeleton()
        self.__skeletonMesh = None
        self.__skeletonObject = None
        
        self.bone = None
            
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        
        human = self.app.selectedHuman
        
        human.hide()
        self.getSkeleton().show()
        self.__updateSkeletonMesh(human)
        
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        
        self.app.selectedHuman.show()
        self.getSkeleton().hide()
        
    def getSkeleton(self):
        
        human = self.app.selectedHuman
        
        if not self.__skeletonObject:
            
            self.__buildSkeletonMesh(human)
            self.__skeletonObject = gui3d.Object(self, human.getPosition(), self.__skeletonMesh)
            self.app.scene3d.update()
            
        else:
            
            self.__skeletonObject.setPosition(human.getPosition())
        
        self.__skeletonObject.setRotation(human.getRotation())
        
        return self.__skeletonObject
        
    def __buildSkeletonMesh(self, human):
           
        self.__skeleton.update(human.meshData)
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
         
        #self.__addCube(self.__skeletonMesh, joint.position, aljabr.vlen(joint.offset) / 10.0, joint.name.replace('joint', 'bone'))
        if joint.parent:
            self.__addPrism(self.__skeletonMesh, joint.parent.position, joint.position, joint.name.replace('joint', 'bone'))
        
        for child in joint.children:
            self.__buildBoneMesh(child)
            
    def __updateSkeletonMesh(self, human):
        
        self.__skeleton.update(human.meshData)
            
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
        scale = len * 0.1 # the thickness is 10% of the length
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
        scale = len * 0.1 # the thickness is 10% of the length
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
        
        self.bone = event.group
        self.bone.setColor([0, 255, 0, 255])
        self.status.setText(event.group.name)
        self.app.redraw()

    def onMouseExited(self, event):
        
        gui3d.TaskView.onMouseExited(self, event)
        
        self.bone.setColor([255, 255, 255, 255])
        self.status.setText('')
        self.app.redraw()
        
    def onMouseMoved(self, event):
        
        gui3d.TaskView.onMouseMoved(self, event)
        
        if self.bone != event.group:
            self.bone.setColor([255, 255, 255, 255])
            self.bone = event.group
            self.bone.setColor([0, 255, 0, 255])
            self.status.setText(event.group.name)
        self.app.redraw()
        
    def onResized(self, event):
        
        self.status.setPosition([10, event[1]-15, 9.1])

def load(app):
    
    category = app.getCategory('Posing')
    taskview = SkeletonView(category)
    
    bvhImporter('Example1.bvh')
    
    print 'Skeleton loaded'

def unload(app):
    pass
