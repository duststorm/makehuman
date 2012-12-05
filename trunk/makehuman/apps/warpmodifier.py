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
            bases = getBaseCharacter(path[0])
            for char,key,repl in bases:
                trgPath = fixTargetPath(path[0], repl)
                self.bases[key] = (trgPath, char, -1)
        else:
            for path in paths:
                bases = getBaseCharacter(path[1])            
                for char,key,repl in bases:
                    trgPath = fixTargetPath(path[0], repl)
                    self.bases[key] = (trgPath, char, -1)
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
        print "Compile", self
        landmarks = theLandMarks[self.bodypart]
        hasChanged = getRefObject(human)
        self.getRefTarget(human)    
        #print len(list(self.refTargetVerts)), len(list(theRefObjectVerts)), len(list(human.shadowCoords))
        if self.refTargetVerts:
            shape = warp.warp_target(self.refTargetVerts, theRefObjectVerts, human.shadowCoords, landmarks)
        else:
            shape = {}
        print "...done"
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
        targetChanged = False
        for key in self.bases.keys():
            target,char,cval0 = self.bases[key]
    
            verts = getRefObjectVerts(char)
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
            folder = os.path.dirname(target)
            if cval:
                #print "ch", key, folder.split("/")[-1], cval
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
            
        for string in ["flaccid", "muscle", "light", "heavy"]:
            if string in target:
                print("  Did not find %s" % target)
                return {}
    
        target1 = target.replace("asian", "caucasian").replace("neutral", "caucasian").replace("african", "caucasian")
        target1 = target1.replace("cauccaucasian", "caucasian")
        verts = self.getTarget(target1)
        if verts:
            self.refTargets[target] = verts
            print("   Replaced %s\n  -> %s" % (target, target1))
            return verts
            
        target2 = target1.replace("child", "young").replace("old", "young")
        verts = self.getTarget(target2)
        if verts:
            self.refTargets[target] = verts
            print("   Replaced %s\n  -> %s" % (target, target2))
            return verts
            
        target3 = target2.replace("male", "female")
        target3 = target3.replace("fefemale", "female")
        verts = self.getTarget(target3)
        self.refTargets[target] = verts
        if not verts:
            print("Warning: Found none of:\n    %s\n    %s\n    %s\n    %s" % (target, target1, target2, target3))
        else:
            print("   Replaced %s\n  -> %s" % (target, target3))        
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
    global theRefObjectPaths, theRefObjectVerts, theBaseObjectVerts
       
    if human.iHaveChanged:
        print "Reference character changed"
        human.iHaveChanged = False                        
    
        theRefObjectVerts = [ list(v) for v in theBaseObjectVerts ]
    
        for char in theRefObjectPaths:
            cval = human.getDetail(char)
            if cval:
                print "  ", os.path.basename(char), cval
                verts = getRefObjectVerts(char)
                for n,v in verts.items():
                    dr = fastmath.vmul3d(v, cval)
                    theRefObjectVerts[n] = fastmath.vadd3d(theRefObjectVerts[n], dr)
        return True
    else:
        return False
        

def getRefObjectVerts(path):
    global theRefObjects
    
    try:
        return theRefObjects[path]
    except KeyError:
        pass
    verts = readTarget(path)
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
    repl = "%s-%s" % (gender, age)  
    bases = [(path, race+"-"+repl, repl)]
    
    if tone:    
        path = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, tone)
        repl = "%s-%s-%s" % (gender, age, tone)
        bases.append( (path, race+"-"+repl, repl) )

    if weight:    
        path = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, weight)
        repl = "%s-%s-%s" % (gender, age, weight)
        bases.append( (path, race+"-"+repl, repl) )

    if tone and weight:    
        path = "data/targets/macrodetails/universal-%s-%s-%s-%s.target" % (gender, age, tone, weight)
        repl = "%s-%s-%s-%s" % (gender, age, tone, weight)
        bases.append( (path, race+"-"+repl, repl) )

    return bases


def fixTargetPath(path, repl):
    (before,orig,name) = path.rsplit("/", 2)
    if "_" in orig:
        repl = repl.replace("-", "_")
    return "%s/%s/%s" % (before, repl, name)
    


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
    global theLandMarks, theBaseObjectVerts, theRefObjectPaths, theRefObjects
    
    obj = files3d.loadMesh("data/3dobjs/base.obj")
    theBaseObjectVerts = [ v.co for v in obj.verts ]

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
    
    theRefObjectPaths = []
    theRefObjects = {}

    for race in ["african", "asian", "neutral"]:
        for age in ["child", "young", "old"]:
            for gender in ["female", "male"]:
                path = "data/targets/macrodetails/%s-%s-%s.target" % (race, gender, age)
                theRefObjectPaths.append(path)
                
    for age in ["child", "young", "old"]:
        for gender in ["female", "male"]:
            for tone in ["flaccid", "muscle"]:
                path = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, tone)
                theRefObjectPaths.append(path)
                for weight in ["light", "heavy"]:
                    path = "data/targets/macrodetails/universal-%s-%s-%s-%s.target" % (gender, age, tone, weight)
                    theRefObjectPaths.append(path)
            for weight in ["light", "heavy"]:
                path = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, weight)
                theRefObjectPaths.append(path)

defineGlobals()
       
  
