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
        
        algos3d.Target.__init__(self, human, modifier.warppath)
        
        self.human = human
        self.modifier = modifier
        #self.bases = modifier.bases
        #self.warppath = modifier.warppath
        #self.bodypart = modifier.bodypart
        self.isWarp = True
        self.isDirty = True
        

    def __repr__(self):
        return ( "<WarpTarget %s %s>" % (os.path.basename(self.modifier.warppath), self.isDirty) )
        
        
    def reinit(self, human):
    
        if self.isDirty:
            shape = self.modifier.compileWarpTarget(self.human)
            saveWarpedTarget(shape, self.modifier.warppath)
            self.__init__(self.modifier, self.human)
            self.isDirty = False
    #print "After reinit", self            
        

    def apply(self, human, morphFactor, update=True, calcNormals=True, faceGroupToUpdateName=None, scale=(1.0,1.0,1.0)):
    
        self.reinit(human)
        algos3d.Target.apply(self, human, morphFactor, update, calcNormals, faceGroupToUpdateName, scale)


def saveWarpedTarget(shape, path): 
    slist = list(shape.items())
    slist.sort()
    fp = open(path, "w")
    for (n, dr) in slist:
        fp.write("%d %.4f %.4f %.4f\n" % (n, dr[0], dr[1], dr[2]))
    fp.close()
    
    
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
        if len(paths) == 1:
            path = paths[0]
            char = getBaseCharacter(path[0])
            self.bases[path[0]] = (char, -1)
        else:
            for path in paths:
                char = getBaseCharacter(path[1])            
                self.bases[path[0]] = (char, -1)
        self.isWarp = True
        self.bodypart = bodypart
        self.refTargets = {}
        self.refTargetVerts = {}
            
    
    def __repr__(self):
        return ("<WarpModifier %s>" % (os.path.basename(self.template)))
            

    def updateValue(self, human, value, updateNormals=1):
        
        if warp.numpy:
            target = self.getWarpTarget(human)    
            target.reinit(human)
            return humanmodifier.SimpleModifier.updateValue(self, human, value, updateNormals)
        else:            
            return self.fallback.updateValue(human, value, updateNormals)
        

    # overrides

    def clampValue(self, value):
        return max(0.0, min(1.0, value))
        
        
    def compileWarpTarget(self, human):
        print "Warp", self
        landmarks = theLandMarks[self.bodypart]
        self.getRefTarget(human)
        warpfield = warp.CWarp()        
        shape = warpfield.warpTarget(self.refTargetVerts, theRefObjectVerts, human.shadowVerts, landmarks)
        return shape
    
    
    def getRefTarget(self, human):
        global theRefObjects, theRefObjectVerts, theBaseObjectVerts
        
        if algos3d.theCharacterHasChanged:
            print "Reference character changed"
            algos3d.theCharacterHasChanged = False                        
    
            theRefObjectVerts = {}
            for n,v in theBaseObjectVerts.items():
                theRefObjectVerts[n] = list(v)
    
            for (char, verts) in theRefObjects.items():
                cval = human.getDetail(char)
                if cval:
                    print "  ", os.path.basename(char), cval
                    for n,v in verts.items():
                        dr = fastmath.vmul3d(v, cval)
                        theRefObjectVerts[n] = fastmath.vadd3d(theRefObjectVerts[n], dr)
                            
        targetChanged = False
        for target in self.bases.keys():
            char,cval0 = self.bases[target]
    
            verts = theRefObjects[char]
            if not verts:
                self.bases[target] = char,0
                continue
    
            cval1 = human.getDetail(char)            
            if cval0 != cval1:
                #print "Target changed", os.path.basename(char), cval0, cval1
                self.bases[target] = char,cval1
                targetChanged = True
            
        if targetChanged:
            print "Reference target changed"
    
            self.refTargetVerts = {}
            for target in self.bases.keys():
                char,cval = self.bases[target]
                if cval:
                    print "   ", target, cval

                    try:
                        verts = self.refTargets[target]
                    except KeyError:
                        verts = None
                    if verts == None:
                        verts = readTarget(target)
                        self.refTargets[target] = verts

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

    if "female" in path:
        gender = "female"
    else:
        gender = "male"

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
                
                
def compileSimpleWarpTarget(filepath, human, bodypart):    
    landmarks = theLandMarks[bodypart]
    base = getBaseCharacter(filepath)
    baseVerts = theRefObjects[base]
    targetVerts = readTarget(filepath)
    return targetVerts
    warpfield = warp.CWarp()        
    shape = warpfield.warpTarget(targetVerts, baseVerts, human.shadowVerts, landmarks)
    return shape
    
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
    for race in ["african", "asian", "neutral"]:
        for gender in ["female", "male"]:
            for age in ["child", "young", "old"]:
                path = "data/targets/macrodetails/%s-%s-%s.target" % (race, gender, age)
                theRefObjects[path] = readTarget(path)
    


defineGlobals()
       
  