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


#----------------------------------------------------------
#   class WarpTarget
#----------------------------------------------------------

class WarpTarget(algos3d.Target):

    def __init__(self, modifier, human):
        
        algos3d.Target.__init__(self, human.meshData, modifier.warppath)
        
        self.human = human
        self.modifier = modifier
        self.isWarp = True
        self.isPose = True
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

        self.warppath = warppath
        self.template = template
        paths = self.fallback.expandTemplate([(self.template, [])])
        self.bases = {}
        if len(paths) == 1:
            path = paths[0]
            char,key = getBaseCharacter(path[0])            
            self.bases[key] = (path[0], char, -1)
        else:
            for path in paths:
                char,key = getBaseCharacter(path[1])            
                self.bases[key] = (path[0], char, -1)
        self.isWarp = True
        self.bodypart = bodypart
        self.slider = None
        self.refTargets = {}
        self.refTargetVerts = {}
            
    
    def __repr__(self):
        return ("<WarpModifier %s>" % (os.path.basename(self.template)))
            

    def updateValue(self, human, value, updateNormals=1):        
        target = self.getWarpTarget(algos3d.theHuman)    
        if not target:
            return
        target.reinit()
        return humanmodifier.SimpleModifier.updateValue(self, human, value, updateNormals)
        

    # overrides

    def clampValue(self, value):
        return max(0.0, min(1.0, value))


    def compileWarpTarget(self, human):
        landmarks = theLandMarks[self.bodypart]
        hasChanged = getRefObject(human)
        self.getRefTarget(human)    
        print "Compile", self
        #print len(list(self.refTargetVerts)), len(list(theRefObjectVerts)), len(list(human.shadowCoords))
        if self.refTargetVerts:
            shape = warp.warp_target(self.refTargetVerts, theRefObjectVerts, human.shadowCoords, landmarks)
        else:
            shape = {}
        return shape

    def getRefTarget(self, human):       
        targetChanged = self.getBases(human)
        if targetChanged:
            #print "Reference target changed"
            if not self.makeRefTarget():
                print "Updating character"
                human.applyAllTargets()
                self.getBases(human)
                if not self.makeRefTarget():
                    raise NameError("Character is empty")

    
    def getBases(self, human):
        global theRefObjects
        
        targetChanged = False
        for key in self.bases.keys():
            target,char,cval0 = self.bases[key]
    
            verts = theRefObjects[char]
            if not verts:
                self.bases[key] = target,char,0
                continue
    
            cval1 = human.getDetail(char)            
            if cval0 != cval1:
                #print "Target changed", os.path.basename(char), cval0, cval1
                self.bases[key] = target,char,cval1
                targetChanged = True
        return targetChanged
        

    def makeRefTarget(self):
        self.refTargetVerts = {}
        madeRefTarget = False
        for key in self.bases.keys():
            target,char,cval = self.bases[key]
            if cval:
                #print "ch", target, cval
                madeRefTarget = True
                verts = self.getTargetInsist(target)
                for n,v in verts.items():
                    dr = fastmath.vmul3d(v, cval)
                    try:
                        self.refTargetVerts[n] = fastmath.vadd3d(self.refTargetVerts[n], dr)
                    except KeyError:
                        self.refTargetVerts[n] = dr
        return madeRefTarget                            
                            

    def getTargetInsist(self, target):
        verts = self.getTarget(target)
        if verts:
            self.refTargets[target] = verts
            return verts
        target1 = target.replace("asian", "caucasian").replace("neutral", "caucasian").replace("african", "caucasian")
        target1 = target1.replace("caucaucasian", "caucasian")
        verts = self.getTarget(target1)
        if verts:
            self.refTargets[target] = verts
            return verts
        target2 = target1.replace("child", "young").replace("old", "young")
        verts = self.getTarget(target2)
        if verts:
            self.refTargets[target] = verts
            return verts
        target3 = target2.replace("male", "female")
        target3 = target3.replace("fefemale", "female")
        verts = self.getTarget(target3)
        self.refTargets[target] = verts
        if not verts:
            print("Warning: Found none of:\n    %s\n    %s\n    %s\n    %s" % (target, target1, target2, target3))
        return verts


    def getTarget(self, target):
        try:
            verts = self.refTargets[target]
        except KeyError:
            verts = None
        if verts == None:
            verts = readTarget(target)
        return verts            
          

    def getWarpTarget(self, human):
        try:
            target = algos3d.targetBuffer[self.warppath]
        except KeyError:
            target = None
    
        if target:
            if not hasattr(target, "isWarp"):
                print "Found non-warp target:", target.name, ". Deleted"
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
        

def getRefObject(human):
    global theRefObjects, theRefObjectVerts, theBaseObjectVerts
       
    if human.iHaveChanged:
        print "Reference character changed"
        human.iHaveChanged = False                        
    
        theRefObjectVerts = [ list(v) for v in theBaseObjectVerts ]
    
        for (char, verts) in theRefObjects.items():
            cval = human.getDetail(char)
            if cval:
                print "  ", os.path.basename(char), cval
                for n,v in verts.items():
                    dr = fastmath.vmul3d(v, cval)
                    theRefObjectVerts[n] = fastmath.vadd3d(theRefObjectVerts[n], dr)
        return True
    else:
        return False
    


def getBaseCharacter(path):    
    if "african" in path:
        race = "african"
    elif "asian" in path:
        race = "asian"
    else:
        race = "neutral"
    
    if "female" in path:
        gender = "female"
    elif "male" in path:
        gender = "male"
    else:
        gender = "female"
    
    if "child" in path:
        age = "child"
    elif "old" in path:
        age = "old"
    else:
        age = "young"

    path = "data/targets/macrodetails/%s-%s-%s.target" % (race, gender, age)
    key = "%s-%s-%s" % (race, gender, age)
    return path,key

#----------------------------------------------------------
#   Call from exporter
#----------------------------------------------------------

def resetWarpTargets(human):
    human.applyAllTargets(forceWarpReset=True)    


def compileWarpTarget(template, fallback, human, bodypart):
    mod = WarpModifier(template, bodypart, fallback)
    return mod.compileWarpTarget(human)
                
#----------------------------------------------------------
#   Read target
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
                if n < algos3d.NMHVerts:
                    target[n] = [float(words[1]), float(words[2]), float(words[3])]
        fp.close()
        return target
    else:
        #print("Could not find %s" % os.path.realpath(path))
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
        with open(path, "r") as fp:
            landmark = []
            for line in fp:
                words = line.split()    
                if len(words) > 0:
                    m = int(words[0])
                    landmark.append(m)

        theLandMarks[name] = landmark

    obj = files3d.loadMesh("data/3dobjs/base.obj")
    theBaseObjectVerts = [ v.co for v in obj.verts ]

    theRefObjects = {}
    for race in ["african", "asian", "neutral"]:
        for gender in ["female", "male"]:
            for age in ["child", "young", "old"]:
                path = "data/targets/macrodetails/%s-%s-%s.target" % (race, gender, age)
                theRefObjects[path] = readTarget(path)
    


defineGlobals()
       
  
