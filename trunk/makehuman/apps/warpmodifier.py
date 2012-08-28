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
import os
import warp
import humanmodifier


NMHVerts = 18528

#----------------------------------------------------------
#   class CModifier
#----------------------------------------------------------

class WarpModifier:

    def __init__(self, target, part, fallback, template):
        global theWarpModifiers
        theWarpModifiers.append(self)            
                
        self.target = target
        self.verts = None
        self.faces = None
        self.landmarks = theLandMarks[part]
        self.warp = warp.CWarp()
        self.isDirty = False

        if warp.numpy:
            self.fallback = None
        else:
            self.fallback = eval( "humanmodifier.%s('%s')" % (fallback, template))
            
    
    def __repr__(self):
        return ("<WarpModifier %s %s>" % (self.target, self.isDirty))
            

    def setValue(self, human, value):
    
        if self.fallback:
            return self.fallback.setValue(human, value)
            
        value = self.clampValue(value)
        human.setDetail(self.target, value)
            

    def getValue(self, human):
        
        if self.fallback:
            return self.fallback.getValue(human)
            
        return human.getDetail(self.target)
        

    def updateValue(self, human, morphFactor, updateNormals=1, updateHuman=True):
        
        if self.fallback:
            return self.fallback.updateValue(human, morphFactor, updateNormals)
            
        # Collect vertex and face indices if we didn't yet
        if not self.verts:
            refTarget = getRefTarget(self.target)
            print "Compiling warp target"
            self.verts = self.warp.warpTarget(refTarget, theRefVerts, human.meshData.verts, self.landmarks)
            print "  ...done"

        # Return morphed verts if called by exporter
        if not updateHuman:
            return self.verts

        self.isDirty = True
        target = getWarpTarget(human.meshData, self.target)    
        target.apply(human.meshData, morphFactor, self.verts)
        
        # Update detail state
        self.setValue(human, morphFactor)

        if not self.faces:        
            self.faces = []
            for vindex in self.verts:
                self.faces += [face.idx for face in human.meshData.verts[vindex].sharedFaces]
            self.faces = list(set(self.faces))
            
        # Update vertices
        faces = [human.meshData.faces[i] for i in self.faces]
        vertices = [human.meshData.verts[i] for i in self.verts]
        
        if updateNormals:
            human.meshData.calcNormals(1, 1, vertices, faces)
        human.meshData.update(vertices, updateNormals)


    def clampValue(self, value):
        return max(0.0, min(1.0, value))

#----------------------------------------------------------
#   class CWarpTarget
#----------------------------------------------------------

class CWarpTarget:
    def __init__(self, path):
        self.path = path
        self.verts = {}
        self.morphFactor = 0
        
        
    def apply(self, obj, morphFactor, verts):

        verticesToUpdate = self.remove(obj)

        for (n, dr) in verts.items():
            v = obj.verts[n]
            v.co[0] += morphFactor * dr[0]
            v.co[1] += morphFactor * dr[1]
            v.co[2] += morphFactor * dr[2]
            verticesToUpdate.append(v)

        verticesToUpdate = set(verticesToUpdate)
        if verticesToUpdate:
            obj.update(verticesToUpdate)            

        self.verts = verts
        self.morphFactor = morphFactor
        
        
    def remove(self, obj):
        verticesToUpdate = []
        for (n, dr) in self.verts.items():
            v = obj.verts[n]
            v.co[0] -= self.morphFactor * dr[0]
            v.co[1] -= self.morphFactor * dr[1]
            v.co[2] -= self.morphFactor * dr[2]
            verticesToUpdate.append(v)
        return verticesToUpdate

                   
#----------------------------------------------------------
#   
#----------------------------------------------------------

def removeAllWarpModifiers(human):
    global theWarpModifiers, theWarpTargetBuffer
    return
    
    print "Removing warps"
    verticesToUpdate = []
    for mod in theWarpModifiers:
        if mod.isDirty:
            print "  Remove", mod
            target = getWarpTarget(human.meshData, mod.target)    
            verticesToUpdate += target.remove(human.meshData) 

    verticesToUpdate = set(verticesToUpdate)
    if verticesToUpdate:
        human.meshData.update(verticesToUpdate)            
        
    theWarpTargetBuffer = {}
    theWarpModifiers = []
        

def getWarpTarget(obj, path):
    global theWarpTargetBuffer
    
    try:
        target = theWarpTargetBuffer[path]
    except KeyError:
        pass
    else:
        return target
        
    target = CWarpTarget(path)
    theWarpTargetBuffer[path] = target    
    return target

    
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
        raise NameError("Could not find %s" % path)
    theRefTargets[path] = target
    return target

        
def defineGlobals():
    global theLandMarks, theRefObject, theRefVerts, theRefTargets
    global theWarpTargetBuffer, theWarpModifiers
    
    theRefTargets = {}
    theWarpTargetBuffer = {}
    theWarpModifiers = []
    
    theLandMarks = {}
    folder = "data/landmarks"
    for file in os.listdir(folder):
        (name, ext) = os.path.splitext(file)
        if ext != ".lmk":
            continue
        path = os.path.join(folder, file)
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
       
  