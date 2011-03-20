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

from aljabr import vadd, makeUnit, makeTranslation, makeRotation, mmul, mtransform, degree2rad, makeScale

class bvhJoint:
    
    def __init__(self, name):
        
        self.name = name
        self.offset = None
        self.position = None
        self.channels = None
        self.parent = None
        self.children = []
        self.frames = []
        self.transform = makeUnit()
        
    #Note: BVH rotation is a static ZXY , thus use szxy in matrix2euler
    def calcTransform(self, frame, scale=0.25):
        
        if self.parent:
            
            self.transform = self.parent.transform[:]
            
        else:
            self.transform = makeScale(scale)
            
        m = makeTranslation(self.offset[0], self.offset[1], self.offset[2])
        self.transform = mmul(self.transform, m)
        
        if frame >= 0 and frame < len(self.frames):
            
            index = 0
            
            for index, channel in enumerate(self.channels):
                #we scale things by 0.25
                if channel == 'Xposition':
                    self.transform[3] = self.transform[3] + scale*self.frames[frame][index]
                elif channel == 'Yposition':
                    self.transform[7] = self.transform[7] + scale*self.frames[frame][index]
                elif channel == 'Zposition':
                    self.transform[11] = self.transform[11] + scale*self.frames[frame][index]
                
                if channel == 'Xrotation':
                    m = makeRotation([1.0, 0.0, 0.0], self.frames[frame][index] * degree2rad)
                    self.transform = mmul(self.transform, m)
                elif channel == 'Yrotation':
                    m = makeRotation([0.0, 1.0, 0.0], self.frames[frame][index] * degree2rad)
                    self.transform = mmul(self.transform, m)
                elif channel == 'Zrotation':
                    m = makeRotation([0.0, 0.0, 1.0], self.frames[frame][index] * degree2rad)
                    self.transform = mmul(self.transform, m)
            
        self.position = [self.transform[3], self.transform[7], self.transform[11]]
            
        for child in self.children:
            
            child.calcTransform(frame)

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
                
    def __readJoint(self, joint):
        
        self.__expectKeyword('{')

        items = self.__expectKeyword('OFFSET')
        joint.offset = [float(x) for x in items[1:]]
        
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
                child.offset = [float(x) for x in items[1:]]
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
        
    def updateFrame(self, frame):
        
        self.root.calcTransform(frame)