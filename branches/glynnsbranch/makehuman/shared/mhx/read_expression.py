#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------


TO DO

"""

import os
import mhx_globals as the
import fastmath
import math
import warp
import warpmodifier
import algos3d


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


Expressions = setupExpressions("data/targets/expression/female_young", 
                               "neutral_female_young_")
                               
#Expressions = ["laughing1"]                               

ExpressionUnits = setupExpressions("data/targets/expression/units/caucasian/female_young", "")

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
    if typ == "Expressions":        
        return ('data/targets/expression/%s_%s/neutral_%s_%s_%s.target' % (gender, age, gender, age, name) )
    elif typ == "ExpressionUnits":        
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
        print("*** Cannot open %s" % filename)
        return None
        
    shape = {}                    
    for line in fp:
        words = line.split()
        n = int(words[0])
        if n < algos3d.NMHVerts:
            shape[n] = (float(words[1]), float(words[2]), float(words[3]))    
    fp.close()
    print("    %s copied" % filename)
    return shape

#----------------------------------------------------------
#   
#----------------------------------------------------------

def readFaceShapes(human, drivers):
    shapeList = []
    shapes = {}
    warpmodifier.resetWarpTargets(human)
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
            if warp.numpy:
                shape = warpmodifier.compileWarpTarget(
                    'shared/mhx/targets/body_language/${gender}-${age}/%s.target' % fname, 
                    "GenderAgeEthnicModifier",
                    human, 
                    "face")
            else:
                shape = readShape('shared/mhx/targets/body_language/female-young/%s.target' % fname)  
            shapes[fname] = shape                
            shapeList.append((sname, shape, lr, min, max))
    shapeList.sort()
    return shapeList
        

def readExpressions(human):
    shapeList = []
    warpmodifier.resetWarpTargets(human)
    for name in Expressions:
        if warp.numpy:
            shape = warpmodifier.compileWarpTarget(
                'data/targets/expression/${gender}_${age}/neutral_${gender}_${age}_%s.target' % name,
                "GenderAgeEthnicModifier", 
                human, 
                "face")
        else:
            shape = loopGendersAges(name, human, "Expressions")
        shapeList.append((name, shape))
    return shapeList


def readExpressionUnits(human):
    shapeList = []
    warpmodifier.resetWarpTargets(human)
    for name in ExpressionUnits:
        if warp.numpy:
            shape = warpmodifier.compileWarpTarget(
                'data/targets/expression/units/${ethnic}/${gender}_${age}/%s.target' % name,
                "GenderAgeEthnicModifier2",
                human, 
                "face")
        else:
            shape = loopGendersAges(name, human, "ExpressionUnits")
        shapeList.append((name, shape))
    return shapeList


def readCorrectives(drivers, human, part):
    shapeList = []
    warpmodifier.resetWarpTargets(human)
    for (pose, lr, expr, vars) in drivers:
        print "Corrective", part, pose
        if warp.numpy:
            shape = warpmodifier.compileWarpTarget(
                "shared/mhx/targets/correctives/%s/${ethnic}/${gender}-${age}/%s.target" % (part, pose),
                'GenderAgeEthnicModifier',
                human, 
                part)
        else:
            shape = loopGendersAges((part, pose), human, "Corrective")

        shapeList.append((shape, pose, lr))
    return shapeList        

def readCorrective(human, part, pose):
    #for e in list(shape.items())[:10]:
    #    print e
    return shape

            



