#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2012

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TO DO

"""

__docformat__ = 'restructuredtext'

import algos3d
import files3d
import fastmath
import math
from operator import mul
import os
import warp
import humanmodifier


NMHVerts = 18528


class WarpModifier:

    def __init__(self, target, part, fallback, template):
        
        self.target = target
        self.verts = None
        self.faces = None
        self.landmarks = theLandMarks[part]
        self.warp = warp.CWarp()

        if warp.numpy:
            self.fallback = None
        else:
            self.fallback = eval( "humanmodifier.%s('%s')" % (fallback, template))
        

    def setValue(self, human, value):
    
        if self.fallback:
            return self.fallback.setValue(human, value)
            
        value = self.clampValue(value)
        human.setDetail(self.target, value)
            

    def getValue(self, human):
        
        if self.fallback:
            return self.fallback.getValue(human)
            
        return human.getDetail(self.target)
        

    def updateValue(self, human, value, updateNormals=1):
        
        if self.fallback:
            return self.fallback.updateValue(human, value, updateNormals)
            
        # Collect vertex and face indices if we didn't yet
        if not (self.verts or self.faces):
            #refTarget = algos3d.getTarget(theRefObject, self.target)
            refTarget = getRefTarget(self.target)
            self.verts = self.warp.warpTarget(refTarget, theRefVerts, human.meshData.verts, self.landmarks)

            self.faces = []
            for vindex in self.verts:
                self.faces += [face.idx for face in human.meshData.verts[vindex].sharedFaces]
            self.faces = list(set(self.faces))
        
        # Remove old targets
        algos3d.loadTranslationTarget(human.meshData, self.target, -human.getDetail(self.target), None, 0, 0)
        
        # Update detail state
        self.setValue(human, value)
        
        # Add new targets
        algos3d.loadTranslationTarget(human.meshData, self.target, human.getDetail(self.target), None, 0, 0)
            
        # Update vertices
        faces = [human.meshData.faces[i] for i in self.faces]
        vertices = [human.meshData.verts[i] for i in self.verts]
        if updateNormals:
            human.meshData.calcNormals(1, 1, vertices, faces)
        human.meshData.update(vertices, updateNormals)


    def clampValue(self, value):
        return max(0.0, min(1.0, value))


def getRefTarget(path):
    global theRefTargets
    try:
        return theRefTargets[path]
    except:
        pass

    target = {}
    try:        
        fp = open(path, "r")
    except:
        fp = None
    if fp:
        print("Loading reference target %s" % path)
        for line in fp:
            words = line.split()
            if len(words) >= 4:
                n = int(words[0])
                if n < NMHVerts:
                    target[n] = [float(words[1]), float(words[2]), float(words[3])]
        fp.close()
        print("  ...done")
    else:
        print("Could not find %s" % path)
    theRefTargets[path] = target
    return target

    
def defineGlobals():
    global theLandMarks, theRefObject, theRefVerts, theRefTargets
    
    theRefTargets = {}
    
    theLandMarks = {}
    folder = "apps/landmarks"
    for file in os.listdir(folder):
        (name, ext) = os.path.splitext(file)
        if ext != ".txt":
            continue
        path = os.path.join(folder, file)
        print("Load", path)
        fp = open(path, "r")
        landmark = {}
        locs = {}
        n = 0
        for line in fp:
            words = line.split()    
            if len(words) > 0:
                m = int(words[0])
                landmark[n] = m
                n += 1
        fp.close()
        theLandMarks[name] = landmark

    theRefObject = files3d.loadMesh("data/3dobjs/base.obj")
    #for n in range(10):
    #    print "A", theRefObject.verts[n]

    refChar = algos3d.getTarget(theRefObject, "data/targets/macrodetails/neutral-female-young.target")
    theRefVerts = {}
    for n,vert in enumerate(theRefObject.verts):
        theRefVerts[n] = fastmath.vadd3d(vert.co, refChar.data[n])
    #for n in range(10):
    #    print "B", theRefVerts[n]


defineGlobals()
       
  