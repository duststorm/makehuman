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


NMhVerts = 18528

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
    exprs = {}
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
        gexprs = {}
        exprs[gender] = gexprs
        asums[gender] = 0.0
        if gval < epsilon:
            continue
        gsum += gval
        
        for (age, aval) in ages:
            if aval < epsilon:
                continue
            fp,filename = targetFile(typ, name, gender, age)                
            if fp:
                aexpr = {}                    
                for line in fp:
                    words = line.split()
                    n = int(words[0])
                    if n < NMhVerts:
                        aexpr[n] = (float(words[1]), float(words[2]), float(words[3]))    
                fp.close()
                print("    %s copied" % filename)
                gexprs[age] = aexpr
                asums[gender] += aval
                    
    expr = {}
    wsum = 0.0
    for (gender, gval) in genders:
        if gval < epsilon or asums[gender] < epsilon:
            continue
        gw = gval/gsum
        gexprs = exprs[gender]
        for (age, aval) in ages:
            if aval < epsilon:
                continue
            aw = aval/asums[gender]
            w = gw*aw
            try:
                aexpr = gexprs[age]
            except:
                aexpr = None
            if not aexpr:
                continue
            wsum += w
            for v in aexpr.keys():
                try:
                    (x,y,z) = expr[v]
                    (dx,dy,dz) = aexpr[v]
                    expr[v] = (x+w*dx, y+w*dy, z+w*dz)
                except:
                    expr[v] = aexpr[v]
                            
    dwarf = 0.8324
    giant = 1.409
    height = human.getHeight()
    if height < 0:
        k = 1 + (1-dwarf)*height
    elif height > 0:
        k = 1 + (giant-1)*height
    else:
        return expr
        
    for v in expr.keys():
        (x,y,z) = expr[v]
        expr[v] = (k*x, k*y, k*z)    
    return expr


def targetFile(typ, name, gender, age):                
    if typ == "Expressions":        
        filename = ('data/targets/expression/%s_%s/neutral_%s_%s_%s.target' % 
                    (gender, age, gender, age, name) )
    elif typ == "ExpressionUnits":        
        filename = ('data/targets/expression/units/caucasian/%s_%s/%s.target' % 
                    (gender, age, name) )
    elif typ == "Corrective":
        filename = ("data/correctives/%s/%s-%s.target" % 
                    (name, gender, age))
    else:
        raise NameError("Unknown type %s" % typ)
    #print ("Try", filename)        
    try:
        fp = open(filename, "rU")
        return fp,filename
    except:
        print("*** Cannot open %s" % filename)
        return 0,filename


def readExpressions(human):
    if warp.numpy:
        warpmodifier.removeAllWarpModifiers(human)
    exprList = []
    for name in Expressions:
        if warp.numpy:
            modifier = warpmodifier.WarpModifier(
                'data/targets/expression/female_young/neutral_female_young_%s.target' % name,
                "face",
                "GenderAgeModifier",
                'data/targets/expression/${gender}_${age}/neutral_${gender}_${age}_%s.target' % name)
            expr = modifier.updateValue(human, 1.0, updateHuman=False)
        else:
            expr = loopGendersAges(name, human, "Expressions")
        exprList.append((name, expr))
    return exprList


def readExpressionUnits(human):
    exprList = []
    for name in ExpressionUnits:
        if 0 and warp.numpy:
            modifier = warpmodifier.WarpModifier(
                "data/targets/expression/units/caucasian/female_young/%s.target" % name,
                "face",
                "GenderAgeModifier",
                'data/targets/expression/${gender}_${age}/neutral_${gender}_${age}_%s.target' % name)
            expr = modifier.updateValue(human, 1.0, updateHuman=False)
        else:
            expr = loopGendersAges(name, human, "ExpressionUnits")
        #expr = readTarget(name, human, "Expressions")
        exprList.append((name, expr))
        #print("    Done %s weight %.3f" % (name, wsum))
    return exprList


def readCorrective(human, part, pose):
    print "Corrective", part, pose
    if 0 and warp.numpy:
        modifier = warpmodifier.WarpModifier(
            "data/correctives/%s/%s/female-young.target" % (part, pose),
            part,
            "GenderAgeModifier",
            'data/correctives/%s/%s/${gender}_${age}.target' % (part, pose))
        expr = modifier.updateValue(human, 1.0, updateHuman=False)
    else:
        expr = loopGendersAges("%s/%s" % (part, pose), human, "Corrective")
    #for e in list(expr.items())[:10]:
    #    print e
    return expr

            



