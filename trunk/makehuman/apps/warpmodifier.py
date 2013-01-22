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
            shape = self.modifier.compileWarpTarget(self.human)
            saveWarpedTarget(shape, self.modifier.warppath)
            self.__init__(self.modifier, self.human)
            self.isDirty = False
        

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

theModifierTypes = {
    "GenderAgeEthnic" : [
        ('macrodetails', None, 'Gender', 0.0, 1.0),
        ('macrodetails', None, 'Age', 0.0, 1.0),
        ('macrodetails', None, 'African', 0.0, 1.0),
        ('macrodetails', None, 'Asian', 0.0, 1.0),
    ],
    "GenderAgeToneWeight" : [
        ('macrodetails', None, 'Gender', 0.0, 1.0),
        ('macrodetails', None, 'Age', 0.0, 1.0),
        ('macrodetails', 'universal', 'Tone', 0.0, 1.0),
        ('macrodetails', 'universal', 'Weight', 0.0, 1.0),
        #('macrodetails', 'universal-stature', 'Height', -1.0, 1.0),
    ],
}


class TargetSpec:
    def __init__(self, path, factors):
        self.path = path
        self.factors = factors
    
    def __repr__(self):
        return ("<TargetSpec %s %s>" % (self.path, self.factors))
    
    
class WarpModifier (humanmodifier.SimpleModifier):

    def __init__(self, template, bodypart, modtype):
        global theModifierTypes, theBaseCharacterParts
                
        string = template.replace('$','').replace('{','').replace('}','')                
        warppath = os.path.join(mh.getPath(""), "warp", string)
        if not os.path.exists(os.path.dirname(warppath)):
            os.makedirs(os.path.dirname(warppath))
        if not os.path.exists(warppath):
            fp = open(warppath, "w")
            fp.close()
            
        humanmodifier.SimpleModifier.__init__(self, warppath)
        self.warppath = warppath
        self.template = template
        self.isWarp = True
        self.bodypart = bodypart
        self.slider = None
        self.refTargets = {}
        self.refTargetVerts = {}        
        self.modtype = modtype
        
        self.fallback = None
        for (tlabel, tname, tvar, tmin, tmax) in theModifierTypes[modtype]:
            self.fallback = humanmodifier.MacroModifier(tlabel, tname, tvar, tmin, tmax)
            break
            
        self.bases = {}
        self.targetSpecs = {}
        if modtype == "GenderAgeEthnic":            
            self.setupBaseCharacters("Gender", "Age", "Ethnic", "NoUniv", "NoUniv")
        elif modtype == "GenderAgeToneWeight":
            self.setupBaseCharacters("Gender", "Age", "NoEthnic", "Tone", "Weight")


    def setupBaseCharacters(self, genders, ages, ethnics, tones, weights):
    
        baseCharacterParts = {
            "Gender" : ("male", "female"),
            "Age" : ("child", "young", "old"),
            "Ethnic" : ("caucasian", "african", "asian"),
            "NoEthnic" : ["caucasian"],
            "Tone" : ("flaccid", None, "muscle"),
            "Weight" : ("light", None, "heavy"),
            "NoUniv" : [None]
        }

        for gender in baseCharacterParts[genders]:
            for age in baseCharacterParts[ages]:
                for ethnic1 in baseCharacterParts[ethnics]:
                    if ethnic1 == "caucasian":
                        ethnic2 = "neutral"
                    else:
                        ethnic2 = ethnic1

                    base = "data/targets/macrodetails/%s-%s-%s.target" % (ethnic2, gender, age)    
                    key = "%s-%s-%s" % (ethnic1, gender, age)  
                    self.bases[key] = (base, -1)

                    path1 = self.template
                    path1 = path1.replace("${ethnic}", ethnic1).replace("${gender}", gender).replace("${age}",age)
                    factors = [ethnic1, gender, age]
                    
                    for tone in baseCharacterParts[tones]:
                        for weight in baseCharacterParts[weights]:            
                            if tone and weight:    
                                base = "data/targets/macrodetails/universal-%s-%s-%s-%s.target" % (gender, age, tone, weight)
                                key = "universal-%s-%s-%s-%s" % (gender, age, tone, weight)
                                self.bases[key] = (base, -1)
                                path2 = path1.replace("${tone}", tone).replace("${weight}", weight)
                                self.targetSpecs[key] = TargetSpec(path2, factors + [tone, weight])
                                
                            elif tone:    
                                base = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, tone)
                                key = "universal-%s-%s-%s" % (gender, age, tone)
                                self.bases[key] = (base, -1)
                                path2 = path1.replace("${tone}", tone).replace("-${weight}", "")
                                self.targetSpecs[key] = TargetSpec(path2, factors + [tone])
                        
                            elif weight:    
                                base = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, weight)
                                key = "universal-%s-%s-%s" % (gender, age, weight)
                                self.bases[key] = (base, -1)
                                path2 = path1.replace("-${tone}", "").replace("${weight}", weight)
                                self.targetSpecs[key] = TargetSpec(path2, factors + [weight])
                                
                            else:                            
                                path2 = path1.replace("-${tone}", "").replace("-${weight}", "")
                                self.targetSpecs[key] = TargetSpec(path2, factors)




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
        if self.refTargetVerts and theRefObjectVerts[self.modtype]:
            shape = warp.warp_target(self.refTargetVerts, theRefObjectVerts[self.modtype], ShadowCoords, landmarks)
        else:
            shape = {}
        log.message("...done")
        return shape


    def getRefTarget(self, human, objectChanged):       
        targetChanged = self.getBases(human)
        if targetChanged or objectChanged:
            #log.message("Reference target changed")
            if not self.makeRefTarget(human):
                #log.message("Updating character")
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
                self.bases[key] = char,cval1
                targetChanged = True
        return targetChanged
        

    def makeRefTarget(self, human):
        self.refTargetVerts = zeroVerts()
        madeRefTarget = False
        factors = self.fallback.getFactors(human, 1.0)
        
        for target in self.targetSpecs.values():
            cval = reduce(mul, [factors[factor] for factor in target.factors])
            if cval > 0:
                log.debug("  reftrg %s %s", target.path, cval)
                madeRefTarget = True
                verts = self.getTargetInsist(target.path)
                if verts is not None:
                    self.refTargetVerts = addVerts(self.refTargetVerts, cval, verts)
        return madeRefTarget                            
    

    def getTargetInsist(self, path):
        verts = self.getTarget(path)
        if verts is not None:
            self.refTargets[path] = verts
            return verts
            
        for string in ["flaccid", "muscle", "light", "heavy"]:
            if string in path:
                log.message("  Did not find %s", path)
                return None
    
        path1 = path.replace("asian", "caucasian").replace("neutral", "caucasian").replace("african", "caucasian")
        path1 = path1.replace("cauccaucasian", "caucasian")
        verts = self.getTarget(path1)
        if verts is not None:
            self.refTargets[path] = verts
            log.message("   Replaced %s\n  -> %s", path, path1)
            return verts
            
        path2 = path1.replace("child", "young").replace("old", "young")
        verts = self.getTarget(path2)
        if verts is not None:
            self.refTargets[path] = verts
            log.message("   Replaced %s\n  -> %s", path, path2)
            return verts
            
        path3 = path2.replace("male", "female")
        path3 = path3.replace("fefemale", "female")
        verts = self.getTarget(path3)
        self.refTargets[path] = verts
        if verts is None:
            log.message("Warning: Found none of:\n    %s\n    %s\n    %s\n    %s", path, path1, path2, path3)
        else:
            log.message("   Replaced %s\n  -> %s", path, path3)        
        return verts


    def getTarget(self, path):
        try:
            verts = self.refTargets[path]
        except KeyError:
            verts = None
        if verts is None:
            verts = readTarget(path)
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
        for line in fp:
            words = line.split()
            if len(words) >= 4:
                n = int(words[0])
                if n < algos3d.NMHVerts:
                    target[n] = [float(words[1]), float(words[2]), float(words[3])]
        fp.close()
        return target
    else:
        log.message("Could not find %s" % os.path.realpath(path))
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
    global theRefObjectVerts, theModifierTypes
    theRefObjectVerts = {}
    for mtype in theModifierTypes.keys():
        theRefObjectVerts[mtype] = None
    

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

    for ethnic in ["african", "asian", "neutral"]:
        for age in ["child", "young", "old"]:
            for gender in ["female", "male"]:
                path = "data/targets/macrodetails/%s-%s-%s.target" % (ethnic, gender, age)
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
       
  
