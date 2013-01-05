#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

__docformat__ = 'restructuredtext'

import algos3d
import files3d
import fastmath
import math
from operator import mul
import mh
import os
import warp
import humanmodifier
import log

ShadowCoords = None

#----------------------------------------------------------
#   class WarpTarget
#----------------------------------------------------------

class WarpTarget(algos3d.Target):

    def __init__(self, modifier, human):
        
        algos3d.Target.__init__(self, human.meshData, modifier.warppath)
        
        self.human = human
        self.modifier = modifier
        self.isWarp = True
        self.isDirty = True
        self.isObsolete = False
        

    def __repr__(self):
        return ( "<WarpTarget %s d:%s o:%s>" % (os.path.basename(self.modifier.warppath), self.isDirty, self.isObsolete) )
        
        
    def reinit(self):
    
        if self.isObsolete:
            halt
        if self.isDirty:
            #print "reinit", self
            shape = self.modifier.compileWarpTarget(self.human)
            saveWarpedTarget(shape, self.modifier.warppath)
            self.__init__(self.modifier, self.human)
            self.isDirty = False
    #print "After reinit", self            
        

    def apply(self, obj, morphFactor, update=True, calcNormals=True, faceGroupToUpdateName=None, scale=(1.0,1.0,1.0)):
    
        self.reinit()
        algos3d.Target.apply(self, obj, morphFactor, update, calcNormals, faceGroupToUpdateName, scale)


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
        self.modtype = fallback

        self.warppath = warppath
        self.template = template
        paths = self.fallback.expandTemplate([(self.template, [])])
        self.paths = [(path.replace("-/","/"), factors) for (path,factors) in paths]
        self.bases = {}

        if len(self.paths) == 1:
            path = self.paths[0]
            bases = getBaseCharacter(path[0])
            for char,key in bases:
                self.bases[key] = (char, -1)
        else:
            for path in self.paths:
                bases = getBaseCharacter(path[1])            
                for char,key in bases:
                    self.bases[key] = (char, -1)
        self.isWarp = True
        self.bodypart = bodypart
        self.slider = None
        self.refTargets = {}
        self.refTargetVerts = {}
            
    
    def __repr__(self):
        return ("<WarpModifier %s>" % (os.path.basename(self.template)))
            

    def setValue(self, human, value):
        humanmodifier.SimpleModifier.setValue(self, human, value)
        human.warpNeedReset = False


    def updateValue(self, human, value, updateNormals=1):        
        target = self.getWarpTarget(algos3d.theHuman)    
        if not target:
            return
        target.reinit()
        humanmodifier.SimpleModifier.updateValue(self, human, value, updateNormals)
        human.warpNeedReset = False
        

    def clampValue(self, value):
        return max(0.0, min(1.0, value))


    def compileWarpTarget(self, human):
        global ShadowCoords
        log.message("Compile %s", self)
        landmarks = theLandMarks[self.bodypart]
        objectChanged = self.getRefObject(human)
        self.getRefTarget(human, objectChanged)    
        #print len(list(self.refTargetVerts)), len(list(theRefObjectVerts[self.modtype])), len(list(ShadowCoords))
        if self.refTargetVerts and theRefObjectVerts[self.modtype]:
            shape = warp.warp_target(self.refTargetVerts, theRefObjectVerts[self.modtype], ShadowCoords, landmarks)
        else:
            shape = {}
        log.message("...done")
        return shape


    def getRefTarget(self, human, objectChanged):       
        targetChanged = self.getBases(human)
        if targetChanged or objectChanged:
            log.message("Reference target changed")
            if not self.makeRefTarget(human):
                log.message("Updating character")
                human.applyAllTargets()
                self.getBases(human)
                if not self.makeRefTarget(human):
                    raise NameError("Character is empty")

    
    def getBases(self, human):
        targetChanged = False
        for key in self.bases.keys():
            char,cval0 = self.bases[key]
    
            verts = self.getRefObjectVerts(char)
            if verts is None:
                self.bases[key] = char,0
                continue
    
            cval1 = human.getDetail(char)    
            if cval0 != cval1:
                #print "Target changed", os.path.basename(char), cval0, cval1
                self.bases[key] = char,cval1
                targetChanged = True
        return targetChanged
        

    def makeRefTarget(self, human):
        self.refTargetVerts = zeroVerts()
        madeRefTarget = False
        factors = self.fallback.getFactors(human, 1.0)
        for data in self.paths:
            cval = reduce(mul, [factors[factor] for factor in data[1]])
            if cval > 0:
                log.debug("  reftrg %s %s", data[0], cval)
                madeRefTarget = True
                verts = self.getTargetInsist(data[0])
                if verts is not None:
                    self.refTargetVerts = addVerts(self.refTargetVerts, cval, verts)
        return madeRefTarget                            
    

    def getTargetInsist(self, target):
        verts = self.getTarget(target)
        if verts is not None:
            self.refTargets[target] = verts
            return verts
            
        for string in ["flaccid", "muscle", "light", "heavy"]:
            if string in target:
                log.message("  Did not find %s", target)
                return None
    
        target1 = target.replace("asian", "caucasian").replace("neutral", "caucasian").replace("african", "caucasian")
        target1 = target1.replace("cauccaucasian", "caucasian")
        verts = self.getTarget(target1)
        if verts is not None:
            self.refTargets[target] = verts
            log.message("   Replaced %s\n  -> %s", target, target1)
            return verts
            
        target2 = target1.replace("child", "young").replace("old", "young")
        verts = self.getTarget(target2)
        if verts is not None:
            self.refTargets[target] = verts
            log.message("   Replaced %s\n  -> %s", target, target2)
            return verts
            
        target3 = target2.replace("male", "female")
        target3 = target3.replace("fefemale", "female")
        verts = self.getTarget(target3)
        self.refTargets[target] = verts
        if verts is None:
            log.message("Warning: Found none of:\n    %s\n    %s\n    %s\n    %s", target, target1, target2, target3)
        else:
            log.message("   Replaced %s\n  -> %s", target, target3)        
        return verts


    def getTarget(self, target):
        try:
            verts = self.refTargets[target]
        except KeyError:
            verts = None
        if verts is None:
            verts = readTarget(target)
        return verts            
          

    def getWarpTarget(self, human):
        try:
            target = algos3d.targetBuffer[self.warppath]
        except KeyError:
            target = None
    
        if target:
            if not hasattr(target, "isWarp"):
                log.message("Found non-warp target: %s. Deleted", target.name)
                del algos3d.targetBuffer[self.warppath]
                return None
                #raise NameError("%s should be warp" % target)
            return target
            
        target = WarpTarget(self, human)
        algos3d.targetBuffer[self.warppath] = target
        return target    
        
        
    def removeTarget(self):
        try:
            target = algos3d.targetBuffer[self.warppath]
        except KeyError:
            return        
        del algos3d.targetBuffer[self.warppath]
        
        
    def getRefObject(self, human):
        global theRefObjects, theRefObjectVerts, theBaseObjectVerts
    
        if theRefObjectVerts[self.modtype]:
            return False
        else:
            log.message("Reset warps")
            refverts = copyArray(theBaseObjectVerts)
            for char in theRefObjects.keys():
                cval = human.getDetail(char)
                if cval:
                    log.debug("  refobj %s %s", os.path.basename(char), cval)
                    verts = self.getRefObjectVerts(char)
                    if verts is not None:
                        refverts = addVerts(refverts, cval, verts)
            theRefObjectVerts[self.modtype] = refverts                
            return True


    def getRefObjectVerts(self, path):
        global theRefObjects
    
        if theRefObjects[path]:
            return theRefObjects[path]
        else:
            verts = readTarget(path)
            if verts is not None:
                theRefObjects[path] = verts
            return verts            
    

def getBaseName(path, name1, name2, name3):
    if name1 in path:
        return name1
    elif name2 in path:
        return name2
    else:
        return name3


def getBaseCharacter(path):    
    race = getBaseName(path, "african", "asian", "neutral")
    gender = getBaseName(path, "female", "male", "female")
    age = getBaseName(path, "child", "old", "young")
    tone = getBaseName(path, "muscle", "flaccid", None)
    weight = getBaseName(path, "heavy", "light", None)

    path = "data/targets/macrodetails/%s-%s-%s.target" % (race, gender, age)    
    key = "%s-%s-%s" % (race, gender, age)  
    bases = [(path, key)]
    
    if tone and weight:    
        path0 = "data/targets/macrodetails/universal-%s-%s-%s-%s.target" % (gender, age, tone, weight)
        repl = "%s-%s-%s-%s-%s" % (race, gender, age, tone, weight)
        bases.append((path, key))
        
    elif tone:    
        path = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, tone)
        repl = "%s-%s-%s-%s" % (race, gender, age, tone)
        bases.append((path, key))

    elif weight:    
        path = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, weight)
        repl = "%s-%s-%s-%s" % (race, gender, age, weight)
        bases.append((path, key))
        
    return bases


def removeAllWarpTargets(human):
    log.message("Removing all warp targets")
    for target in algos3d.targetBuffer.values():
        if hasattr(target, "isWarp"):
            log.message("  %s", target)
            target.isDirty = True
            target.isObsolete = True
            human.setDetail(target.name, 0)
            target.morphFactor = 0
            target.modifier.setValue(human, 0)
            if target.modifier.slider:
                target.modifier.slider.update()     
            del algos3d.targetBuffer[target.name]


def getWarpedCoords():
    coords = ShadowCoords.copy()
    for target in algos3d.targetBuffer.values():
        if hasattr(target, "isWarp") and not hasattr(target, "isPose"):
            verts = algos3d.targetBuffer[target.name].verts
            coords[verts] += target.morphFactor * target.data
    return coords                
            

#----------------------------------------------------------
#   Call from exporter
#----------------------------------------------------------

def compileWarpTarget(template, fallback, human, bodypart):
    mod = WarpModifier(template, bodypart, fallback)
    return mod.compileWarpTarget(human)
                
#----------------------------------------------------------
#   Read target
#----------------------------------------------------------                

def readTarget(path):
    try:        
        fp = open(path, "r")
    except:
        fp = None
    if fp:
        target = zeroVerts()
        #print("Loading target %s" % path)
        for line in fp:
            words = line.split()
            if len(words) >= 4:
                n = int(words[0])
                if n < algos3d.NMHVerts:
                    target[n] = [float(words[1]), float(words[2]), float(words[3])]
        fp.close()
        return target
    else:
        #print("Could not find %s" % os.path.realpath(path))
        return None

#----------------------------------------------------------
#   For testing numpy
#----------------------------------------------------------

"""    
import numpy
 
def zeroVerts():
    return numpy.zeros((algos3d.NMHVerts,3), float)
    
def addVerts(targetVerts, cval, verts):     
    return targetVerts + cval*verts
    
def makeArray(verts):
    return numpy.array(verts, float)

def copyArray(verts):
    return numpy.array(verts, float)

""" 
def zeroVerts():
    return {}
    
def addVerts(targetVerts, cval, verts):                    
    for n,v in verts.items():
        dr = fastmath.vmul3d(v, cval)
        try:
            targetVerts[n] = fastmath.vadd3d(targetVerts[n], dr)
        except KeyError:
            targetVerts[n] = dr
    return targetVerts            
    
def makeArray(verts):
    return verts

def copyArray(verts):
    return [ list(v) for v in verts ] 
                          
#----------------------------------------------------------
#   Init globals
#----------------------------------------------------------

def clearRefObject():
    global theRefObjectVerts
    theRefObjectVerts = {}
    theRefObjectVerts["GenderAgeMuscleWeightModifier"] = None
    theRefObjectVerts["GenderAgeEthnicModifier2"] = None
    

def defineGlobals():
    global theLandMarks, theBaseObjectVerts, theRefObjects
    
    obj = files3d.loadMesh("data/3dobjs/base.obj")
    theBaseObjectVerts = [ v.co for v in obj.verts ]
    theBaseObjectVerts = makeArray(theBaseObjectVerts)

    theLandMarks = {}
    folder = "data/landmarks"
    for file in os.listdir(folder):
        (name, ext) = os.path.splitext(file)
        if ext != ".lmk":
            continue
        path = os.path.join(folder, file)
        with open(path, "r") as fp:
            landmark = []
            for line in fp:
                words = line.split()    
                if len(words) > 0:
                    m = int(words[0])
                    landmark.append(m)

        theLandMarks[name] = landmark
    
    clearRefObject()
    theRefObjects = {}

    for race in ["african", "asian", "neutral"]:
        for age in ["child", "young", "old"]:
            for gender in ["female", "male"]:
                path = "data/targets/macrodetails/%s-%s-%s.target" % (race, gender, age)
                theRefObjects[path] = None
                
    for age in ["child", "young", "old"]:
        for gender in ["female", "male"]:
            for tone in ["flaccid", "muscle"]:
                path = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, tone)
                theRefObjects[path] = None
                for weight in ["light", "heavy"]:
                    path = "data/targets/macrodetails/universal-%s-%s-%s-%s.target" % (gender, age, tone, weight)
                    theRefObjects[path] = None
            for weight in ["light", "heavy"]:
                path = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, weight)
                theRefObjects[path] = None

defineGlobals()
       
  
