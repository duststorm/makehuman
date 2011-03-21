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

BVH importer
"""

from aljabr import vadd, makeUnit, makeRotation, mtransform, degree2rad, makeScale, makeTranslation, mmul, makeTransform, euler2matrix, vmul
from skeleton import Joint

class bvhJoint(Joint):
  def __init__(self, name):
    Joint.__init__(self,name, [])
    self.channels = None
    self.frames = []
    self.rotation = [0.0, 0.0, 0.0]
    self.translation = [0.0, 0.0, 0.0]
  
  def updateFrame(self, frame, scale=0.25):
      
    if self.parent:
        self.transform = self.parent.transform[:]
    else:
        self.transform = makeUnit() #makeScale(scale)
    
    m = makeTranslation(self.offset[0], self.offset[1], self.offset[2])
    self.transform = mmul(self.transform, m) #parent postmultiply with offset
    
    if frame >= 0 and frame < len(self.frames):
        index = 0
      
        Ryxz = [0.0, 0.0, 0.0]
        Txyz = [0.0, 0.0, 0.0]
        for index, channel in enumerate(self.channels):
            if channel == 'Xposition':
                Txyz[0] = scale*self.frames[frame][index]
            elif channel == 'Yposition':
                Txyz[1] = scale*self.frames[frame][index]
            elif channel == 'Zposition':
                Txyz[2] = scale*self.frames[frame][index]
              
            if channel == 'Xrotation':
                Ryxz[1] = self.frames[frame][index] * degree2rad
            elif channel == 'Yrotation':
                Ryxz[0] = self.frames[frame][index] * degree2rad
            elif channel == 'Zrotation':
                Ryxz[2] = self.frames[frame][index] * degree2rad
        self.translation = Txyz[:]
        self.rotation = Ryxz[:]
        m = euler2matrix(Ryxz, "syxz")
        m[3], m[7], m[11] = Txyz[0], Txyz[1], Txyz[2] 
        self.transform = mmul(self.transform, m) # parent post multiply with transformations
    
    for child in self.children:
        child.updateFrame(frame)

class bvhSkeleton:
    
    def __init__(self, filename):
        
        self.file = open(filename, 'r')
            
        # Read hierarchy
        self.__expectKeyword('HIERARCHY')
            
        items = self.__expectKeyword('ROOT')
        
        self.root = bvhJoint(items[1])
        
        self.__readJoint(self.root)
            
        # Read motion
        self.__expectKeyword('MOTION')
        
        items = self.__expectKeyword('Frames:')
        self.frames = int(items[1])
        items = self.__expectKeyword('Frame') # Time:
        self.frameTime = float(items[2])
            
        for i in range(self.frames):
            line = self.file.readline()
            items = line.split()
            data = [float(item) for item in items]
            data = self.__getChannelData(self.root, data)
                
    def getJoint(self, name):
        
        return self.__getJoint(self.root, name)
        
    def __getJoint(self, joint, name):
        
        if joint.name == name:
            return joint
            
        for child in joint.children:
            j = self.__getJoint(child, name)
            if j:
                return j
                
        return None
                
    def __readJoint(self, joint, scale=0.25):
        
        self.__expectKeyword('{')

        items = self.__expectKeyword('OFFSET')
        joint.offset = [scale*float(x) for x in items[1:]]
        
        if joint.parent:
            joint.position = vadd(joint.parent.position, joint.offset)
        else:
            joint.position = joint.offset[:]
        
        items = self.__expectKeyword('CHANNELS')
        joint.channels = items[2:]
        
        if int(items[1]) != len(joint.channels):
            RuntimeError('Expected %d channels found %d' % (items[1], len(joint.channels)))
        
        # Read child joints
        while 1:
            line = self.file.readline()
            items = line.split()
            
            if items[0] == 'JOINT':
                
                child = bvhJoint(items[1])
                joint.children.append(child)
                child.parent = joint
                self.__readJoint(child)
                
            elif items[0] == 'End': # Site
                
                child = bvhJoint('End effector')
                joint.children.append(child)
                child.channels = []
                child.parent = joint
                
                self.__expectKeyword('{')
                
                items = self.__expectKeyword('OFFSET')
                child.offset = [scale*float(x) for x in items[1:]]
                child.position = vadd(joint.position, child.offset)
                
                self.__expectKeyword('}')
                
            elif items[0] == '}':
                
                break
                
            else:
                
                raise RuntimeError('Expected %s found %s' % ('JOINT, End Site or }', items[0]))
                    
    def __expectKeyword(self, keyword):
        
        line = self.file.readline()
        items = line.split()
        
        if items[0] != keyword:
            raise RuntimeError('Expected %s found %s' % (keyword, items[0]))
                
        return items
        
    def __getChannelData(self, joint, data):
        
        channels = len(joint.channels)
        joint.frames.append(data[0:channels])
        data = data[channels:]
        
        for child in joint.children:
            data = self.__getChannelData(child, data)
        
        return data
        
    def updateFrame(self, frame, scale = 0.25):
        self.root.updateFrame(frame)