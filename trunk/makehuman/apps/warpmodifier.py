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
import mh
import os
import warp
import humanmodifier


NMHVerts = 18528

#----------------------------------------------------------
#   class WarpTarget
#----------------------------------------------------------

class WarpTarget(algos3d.Target):

    def __init__(self, obj, refpath, warppath, landmarks):
        
        algos3d.Target.__init__(self, obj, warppath)
        
        self.refpath = refpath
        self.warppath = warppath
        self.landmarks = landmarks
        self.isWarp = True
        self.isDirty = True
        
        
    def reinit(self, obj):
    
        if self.isDirty:
            print "reinit", self.warppath
            shape = compileWarpTarget1(self.refpath, obj, self.landmarks)
            saveWarpedTarget(shape, self.warppath)
            self.__init__(obj, self.refpath, self.warppath, self.landmarks)
            self.isDirty = False
        

    def apply(self, obj, morphFactor, update=True, calcNormals=True, faceGroupToUpdateName=None, scale=(1.0,1.0,1.0)):
    
        self.reinit(obj)
        algos3d.Target.apply(self, obj, morphFactor, update, calcNormals, faceGroupToUpdateName, scale)



def compileWarpTarget(path, obj, part):
    return compileWarpTarget1(path, obj, theLandMarks[part])

def compileWarpTarget1(path, obj, landmarks):
    refTarget = getRefTarget(path)
    print "Compiling warp target"
    warpfield = warp.CWarp()
    shape = warpfield.warpTarget(refTarget, theRefVerts, obj.verts, landmarks)
    print "  ...done"
    return shape


def saveWarpedTarget(shape, path): 
    slist = list(shape.items())
    slist.sort()
    fp = open(path, "w")
    for (n, dr) in slist:
        fp.write("%d %.4f %.4f %.4f\n" % (n, dr[0], dr[1], dr[2]))
    fp.close()
    
    
def getWarpTarget(obj, refpath, warppath, landmarks):
    try:
        target = algos3d.targetBuffer[warppath]
    except KeyError:
        target = None

    if target:
        if not target.isWarp:
            raise NameError("Target %s should be warp" % warppath)
        return target
        
    target = WarpTarget(obj, refpath, warppath, landmarks)
    algos3d.targetBuffer[warppath] = target
    
    return target


def resetAllWarpTargets():
    for target in algos3d.targetBuffer.values():
        if target.isWarp:
            target.isDirty = True

#----------------------------------------------------------
#   class WarpModifier
#----------------------------------------------------------

class WarpModifier (humanmodifier.SimpleModifier):

    def __init__(self, target, part, fallback, template):
        
        warppath = os.path.join(mh.getPath(""), "warp", target)
        if not os.path.exists(os.path.dirname(warppath)):
            os.makedirs(os.path.dirname(warppath))
        if not os.path.exists(warppath):
            fp = open(warppath, "w")
            fp.close()
            
        humanmodifier.SimpleModifier.__init__(self, warppath)

        self.warppath = warppath
        self.refpath = target
        self.landmarks = theLandMarks[part]
        self.warp = warp.CWarp()

        if warp.numpy:
            self.fallback = None
        else:
            self.fallback = eval( "humanmodifier.%s('%s')" % (fallback, template))
            
    
    def __repr__(self):
        return ("<WarpModifier %s>" % (self.target))
            

    def setValue(self, human, value):
    
        if self.fallback:
            return self.fallback.setValue(human, value)
        else:    
            return humanmodifier.SimpleModifier.setValue(self, human, value)
                        

    def getValue(self, human):
        
        if self.fallback:
            return self.fallback.getValue(human)
        else:    
            return humanmodifier.SimpleModifier.getValue(self, human)
        

    def updateValue(self, human, value, updateNormals=1):
        
        if self.fallback:
            return self.fallback.updateValue(human, value, updateNormals)
        else:            
            target = getWarpTarget(human.meshData, self.refpath, self.warppath, self.landmarks)    
            target.reinit(human.meshData)
            return humanmodifier.SimpleModifier.updateValue(self, human, value, updateNormals)
        

    def clampValue(self, value):
        return max(0.0, min(1.0, value))

#----------------------------------------------------------
#   class CWarpTarget
#----------------------------------------------------------

"""
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
"""
                   
#----------------------------------------------------------
#   Reference object
#----------------------------------------------------------

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
    
    theRefTargets = {}
    
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
       
  