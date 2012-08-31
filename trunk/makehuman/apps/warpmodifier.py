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

    def __init__(self, modifier, human):
        
        algos3d.Target.__init__(self, human.meshData, modifier.warppath)
        
        self.human = human
        self.modifier = modifier
        #self.bases = modifier.bases
        #self.warppath = modifier.warppath
        #self.bodypart = modifier.bodypart
        self.isWarp = True
        self.isDirty = True
        

    def __repr__(self):
        return ( "<WarpTarget %s>" % self.modifier.warppath )
        
        
    def reinit(self, obj):
    
        if self.isDirty:
            print "reinit"
            shape = self.modifier.compileWarpTarget(self.human)
            saveWarpedTarget(shape, self.modifier.warppath)
            self.__init__(self.modifier, self.human)
            self.isDirty = False
        

    def apply(self, obj, morphFactor, update=True, calcNormals=True, faceGroupToUpdateName=None, scale=(1.0,1.0,1.0)):
    
        self.reinit(obj)
        algos3d.Target.apply(self, obj, morphFactor, update, calcNormals, faceGroupToUpdateName, scale)


def saveWarpedTarget(shape, path): 
    slist = list(shape.items())
    slist.sort()
    fp = open(path, "w")
    for (n, dr) in slist:
        fp.write("%d %.4f %.4f %.4f\n" % (n, dr[0], dr[1], dr[2]))
    fp.close()
    
    
def resetAllWarpTargets():
    print "Resetting warp targets"
    for target in algos3d.targetBuffer.values():
        if target.isWarp:
            target.isDirty = True

#----------------------------------------------------------
#   class WarpModifier
#----------------------------------------------------------

class WarpModifier (humanmodifier.SimpleModifier):

    def __init__(self, template, bodypart, fallback):
                
        string = template.replace('$','').replace('{','').replace('}','')                
        warppath = os.path.join(mh.getPath(""), "warp", string)
        if not os.path.exists(os.path.dirname(warppath)):
            os.makedirs(os.path.dirname(warppath))
        if not os.path.exists(warppath):
            fp = open(warppath, "w")
            fp.close()
            
        humanmodifier.SimpleModifier.__init__(self, warppath)
        self.fallback = eval( "humanmodifier.%s('%s')" % (fallback, template))

        self.warppath = warppath
        self.template = template
        paths = self.fallback.expandTemplate([(self.template, [])])
        self.bases = {}
        for path in paths:
            self.bases[path[0]] = (getBaseCharacter(path[1]), -1, -1)
        self.isWarp = True
        self.bodypart = bodypart
        self.refTargets = {}
        self.refTargetVerts = {}
            
    
    def __repr__(self):
        return ("<WarpModifier %s>" % (self.template))
            

    def updateValue(self, human, value, updateNormals=1):
        
        if warp.numpy:
            target = self.getWarpTarget(human)    
            target.reinit(human.meshData)
            return humanmodifier.SimpleModifier.updateValue(self, human, value, updateNormals)
        else:            
            return self.fallback.updateValue(human, value, updateNormals)
        

    # overrides

    def clampValue(self, value):
        return max(0.0, min(1.0, value))
        
        
    def compileWarpTarget(self, human):
        print "Warp", self.warppath
        landmarks = theLandMarks[self.bodypart]
        self.getRefTarget(human)
        warpfield = warp.CWarp()
        shape = warpfield.warpTarget(self.refTargetVerts, theRefObjectVerts, human.meshData.verts, landmarks)
        return shape
    
    
    def getRefTarget(self, human):
        global theRefObjects, theRefObjectVerts, theBaseObjectVerts
        
        charChanged = False
        targetChanged = False
        for target in self.bases.keys():
            char,cval0,tval0 = self.bases[target]
    
            try:
                verts = theRefObjects[char]
            except KeyError:
                verts = None
            if verts == None:
                verts = readTarget(char)
                theRefObjects[char] = verts
            if not verts:
                self.bases[target] = char,0,0
                continue
    
            if verts:
                cval1 = human.getDetail(char)            
            else:
                cval1 = 0
            if cval0 != cval1:
                #print "Character changed", os.path.basename(char), cval0, cval1
                self.bases[target] = char,cval1,tval0
                charChanged = True
    
            try:
                verts = self.refTargets[target]
            except KeyError:
                verts = None
            if verts == None:
                verts = readTarget(target)
                self.refTargets[target] = verts
                
            if verts:
                tval1 = human.getDetail(target)            
            else:
                tval1 = 0
            if tval0 != tval1:
                #print "Target changed", target, tval0, tval1
                self.bases[target] = char,cval1,tval1
                targetChanged = True
    
        
        if charChanged:
            print "Reference character changed"
    
            theRefObjectVerts = {}
            for n,v in theBaseObjectVerts.items():
                theRefObjectVerts[n] = list(v)
    
            for target in self.bases.keys():
                char,cval,tval = self.bases[target]
                if cval:
                    print "  ", os.path.basename(char), cval
                    verts = theRefObjects[char]
                    for n,v in verts.items():
                        r = fastmath.vmul3d(v, cval)
                        theRefObjectVerts[n] = fastmath.vadd3d(theRefObjectVerts[n], r)
    
        if targetChanged or charChanged:
            print "Reference target changed"
    
            self.refTargetVerts = {}
            for target in self.bases.keys():
                char,cval,tval = self.bases[target]
                if cval:
                    print "   ", target, cval, tval
                    verts = self.refTargets[target]
                    for n,v in verts.items():
                        dr = fastmath.vmul3d(v, cval)
                        try:
                            self.refTargetVerts[n] = fastmath.vadd3d(self.refTargetVerts[n], dr)
                        except KeyError:
                            self.refTargetVerts[n] = dr
                            

    def getWarpTarget(self, human):
        try:
            target = algos3d.targetBuffer[self.warppath]
        except KeyError:
            target = None
    
        if target:
            if not target.isWarp:
                raise NameError("Target %s should be warp" % self.warppath)
            return target
            
        target = WarpTarget(self, human)
        algos3d.targetBuffer[self.warppath] = target
        return target    
    

def getBaseCharacter(path):
    if "african" in path:
        race = "african"
    elif "asian" in path:
        race = "asian"
    else:
        race = "neutral"

    if "male" in path:
        gender = "male"
    else:
        gender = "female"

    if "child" in path:
        age = "child"
    elif "old" in path:
        age = "old"
    else:
        age = "young"
        
    return "data/targets/macrodetails/%s-%s-%s.target" % (race, gender, age)
        

#----------------------------------------------------------
#   Call from exporter
#----------------------------------------------------------

def compileWarpTarget(template, fallback, human, bodypart):
    mod = WarpModifier(template, bodypart, fallback)
    return mod.compileWarpTarget(human)
                
#----------------------------------------------------------
#   Reference object
#----------------------------------------------------------
                

def readTarget(path):
    target = {}
    try:        
        fp = open(path, "r")
    except:
        fp = None
    if fp:
        #print("Loading target %s" % path)
        for line in fp:
            words = line.split()
            if len(words) >= 4:
                n = int(words[0])
                if n < NMHVerts:
                    target[n] = [float(words[1]), float(words[2]), float(words[3])]
        fp.close()
        return target
    else:
        print("Could not find %s" % os.path.realpath(path))
        return {}

        
#----------------------------------------------------------
#   Init globals
#----------------------------------------------------------

def defineGlobals():
    global theLandMarks, theBaseObjectVerts, theRefObjects
    
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

    obj = files3d.loadMesh("data/3dobjs/base.obj")
    theBaseObjectVerts = {}
    for n,v in enumerate(obj.verts):
        theBaseObjectVerts[n] = v.co
    theRefObjects = {}


defineGlobals()
       
  