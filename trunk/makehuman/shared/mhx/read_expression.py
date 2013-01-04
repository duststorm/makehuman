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

import os
import fastmath
import math
import gui3d
import warp
import warpmodifier
import algos3d
import log

from . import the
from the import *


#----------------------------------------------------------
#   Setup expressions
#----------------------------------------------------------

def setupExpressions(folder, prefix):
    expressions = []
    for file in os.listdir(folder):
        (fname, ext) = os.path.splitext(file)
        if ext == ".target":
            if prefix:
                (before, sep, after) = fname.partition(prefix)
                if sep:
                    expressions.append(after)
            else:
                expressions.append(fname)
    return(expressions)


#Expressions = setupExpressions("./data/targets/expression/female_young", "neutral_female_young_")
                               
ExpressionUnits = setupExpressions("./data/targets/expression/units/caucasian/female_young", "")

#----------------------------------------------------------
#   Loop
#----------------------------------------------------------

def loopGendersAges(name, human, typ):
    epsilon = 0.05
    shapes = {}
    asums = {}
    gsum = 0.0
    genders = [
        ('female', human.femaleVal),
        ('male', human.maleVal)
    ]
        
    ages = [
        ('child', human.childVal),
        ('young', human.youngVal),
        ('old', human.oldVal)
    ]

    for (gender, gval) in genders:
        gshapes = {}
        shapes[gender] = gshapes
        asums[gender] = 0.0
        if gval < epsilon:
            continue
        gsum += gval
        
        for (age, aval) in ages:
            if aval < epsilon:
                continue
            filename = targetFileName(typ, name, gender, age) 
            ashape = readShape(filename)
            if ashape:
                gshapes[age] = ashape
                asums[gender] += aval
                    
    shape = {}
    wsum = 0.0
    for (gender, gval) in genders:
        if gval < epsilon or asums[gender] < epsilon:
            continue
        gw = gval/gsum
        gshapes = shapes[gender]
        for (age, aval) in ages:
            if aval < epsilon:
                continue
            aw = aval/asums[gender]
            w = gw*aw
            try:
                ashape = gshapes[age]
            except:
                ashape = None
            if not ashape:
                continue
            wsum += w
            for v in ashape.keys():
                try:
                    (x,y,z) = shape[v]
                    (dx,dy,dz) = ashape[v]
                    shape[v] = (x+w*dx, y+w*dy, z+w*dz)
                except:
                    shape[v] = ashape[v]
                            
    dwarf = 0.8324
    giant = 1.409
    height = human.getHeight()
    if height < 0:
        k = 1 + (1-dwarf)*height
    elif height > 0:
        k = 1 + (giant-1)*height
    else:
        return shape
        
    for v in shape.keys():
        (x,y,z) = shape[v]
        shape[v] = (k*x, k*y, k*z)    
    return shape


def targetFileName(typ, name, gender, age):                
    #if typ == "Expressions":        
    #    return ('data/targets/expression/%s_%s/neutral_%s_%s_%s.target' % (gender, age, gender, age, name) )
    if typ == "ExpressionUnits":        
        return ('data/targets/expression/units/caucasian/%s_%s/%s.target' %  (gender, age, name) )
    elif typ == "Corrective":
        (part, pose) = name
        return ("shared/mhx/targets/correctives/%s/caucasian/%s-%s/%s.target" % (part, gender, age, pose))
    else:
        raise NameError("Unknown type %s" % typ)
        

def readShape(filename):                
    #print ("Try", filename)        
    try:
        fp = open(filename, "rU")
    except:
        log.error("*** Cannot open %s" % filename)
        return None
        
    shape = {}                    
    for line in fp:
        words = line.split()
        n = int(words[0])
        if n < algos3d.NMHVerts:
            shape[n] = (float(words[1]), float(words[2]), float(words[3]))    
    fp.close()
    log.message("    %s copied" % filename)
    return shape

#----------------------------------------------------------
#   
#----------------------------------------------------------
"""
def readFaceShapes(human, drivers, t0, t1):
    shapeList = []
    shapes = {}
    t,dt = initTimes(drivers.keys(), 0.0, 1.0)

    for name,value in drivers.items():
        (fname, bone, channel, sign, min, max) = value
        if (name[-2:] in ["_L", "_R"]):
            lr = "LR"
            sname = name[:-2]
        else:
            lr = "Sym"
            sname = name

        try:
            shape = shapes[fname]
            doLoad = False
        except:
            doLoad = True
        if doLoad:
            gui3d.app.progress(t, text="Reading face shape %s" % fname)
                
            shape = warpmodifier.compileWarpTarget(
                    'shared/mhx/targets/body_language/${gender}-${age}/%s.target' % fname, 
                    "GenderAgeEthnicModifier",
                    human, 
                    "face")

            shapes[fname] = shape                
            shapeList.append((sname, shape, lr, min, max))
            t += dt
    shapeList.sort()
    return shapeList
        

def readExpressions(human, t0, t1):
    shapeList = []
    t,dt = initTimes(Expressions, 0.0, 1.0)

    for name in Expressions:
        gui3d.app.progress(t, text="Reading expression %s" % name)
            
        shape = warpmodifier.compileWarpTarget(
                'data/targets/expression/${gender}_${age}/neutral_${gender}_${age}_%s.target' % name,
                "GenderAgeEthnicModifier", 
                human, 
                "face")

        shapeList.append((name, shape))
        t += dt
    return shapeList
"""

def readExpressionUnits(human, t0, t1):
    shapeList = []
    t,dt = initTimes(ExpressionUnits, 0.0, 1.0)
    
    for name in ExpressionUnits:
        gui3d.app.progress(t, text="Reading expression %s" % name)

        shape = warpmodifier.compileWarpTarget(
                'data/targets/expression/units/${ethnic}/${gender}_${age}/%s.target' % name,
                "GenderAgeEthnicModifier2",
                human, 
                "face")

        shapeList.append((name, shape))
        t += dt
    return shapeList


def readCorrectives(drivers, human, folder, landmarks, t0, t1):
    shapeList = []
    t,dt = initTimes(drivers, 0.0, 1.0)
    
    for (pose, lr, expr, vars) in drivers:
        gui3d.app.progress(t, text="Reading corrective %s %s" % (folder, pose))

        shape = warpmodifier.compileWarpTarget(
                "shared/mhx/targets/correctives/%s/caucasian/${gender}-${age}-${tone}-${weight}/%s.target" % (folder, pose),
                'GenderAgeMuscleWeightModifier',
                human, 
                landmarks)

        shapeList.append((shape, pose, lr))
        t += dt
    return shapeList        

def readCorrective(human, part, pose):
    #for e in list(shape.items())[:10]:
    #    print e
    return shape


def initTimes(flist, t0, t1):    
    dt = t1-t0
    n = len(flist)
    if n > 0:
        dt /= n
    return t0,dt
    

def readExpressionMhm(folder):
    exprList = []
    for file in os.listdir(folder):
        (fname, ext) = os.path.splitext(file)
        if ext == ".mhm":
            path = os.path.join(folder, file)
            fp = open(path, "rU")
            units = []
            for line in fp:
                words = line.split()
                if len(words) < 3:
                    pass
                elif words[0] == "expression":
                    units.append(words[1:3])
            fp.close()
            exprList.append((fname,units))
    return exprList                    
    



