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

from aljabr import vadd

class bvhJoint:
    
    def __init__(self, name):
        
        self.name = name
        self.offset = None
        self.position = None
        self.channels = None
        self.parent = None
        self.children = []
        self.frames = []

class bvhSkeleton:
    
    def __init__(self, filename):
        
        self.file = open(filename, 'r')
            
        # Read hierarchy
        self.expectKeyword('HIERARCHY')
            
        items = self.expectKeyword('ROOT')
        
        self.root = bvhJoint(items[1])
        
        self.readJoint(self.root)
            
        # Read motion
        self.expectKeyword('MOTION')
        
        items = self.expectKeyword('Frames:')
        self.frames = int(items[1])
        items = self.expectKeyword('Frame') # Time:
        self.frameTime = float(items[2])
            
        for i in range(self.frames):
            
            line = self.file.readline()
            items = line.split()
            data = [float(item) for item in items]
            data = self.getChannelData(self.root, data)
                
    def readJoint(self, joint):
        
        self.expectKeyword('{')

        items = self.expectKeyword('OFFSET')
        joint.offset = [float(x) for x in items[1:]]
        
        if joint.parent:
            joint.position = vadd(joint.parent.position, joint.offset)
        else:
            joint.position = joint.offset[:]
        
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
                
                child = bvhJoint('End effector')
                joint.children.append(child)
                child.channels = []
                child.parent = joint
                
                self.expectKeyword('{')
                
                items = self.expectKeyword('OFFSET')
                child.offset = [float(x) for x in items[1:]]
                child.position = vadd(joint.position, child.offset)
                
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