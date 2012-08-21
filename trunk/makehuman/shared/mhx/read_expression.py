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
                        aexpr[n] = (float(words[1]), -float(words[3]), float(words[2]))    
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
    else:
        k = 1 + (giant-1)*height
    for v in expr.keys():
        (x,y,z) = expr[v]
        expr[v] = (k*x, k*y, k*z)
    
    return (expr, wsum)


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

"""
def readTarget(name, human, typ):
    warp = setupWarpField(human.meshData)
    fp,filename = targetFile(typ, name, "female", "young")
    if fp:
        expr = {}            
        for line in fp:
            words = line.split()
            vn = int(words[0])
            s = warp[vn]
            expr[vn] = (s[0]*float(words[1]), -s[2]*float(words[3]), s[1]*float(words[2]))    
        fp.close()
        print("    %s copied" % filename)
    return expr


def setupWarpField(obj):
    warp = the.Config.warpField
    if warp:
        return warp

    vertEdges = {}
    for v in obj.verts:
        vertEdges[v.idx] = []
        
    for f in obj.faces:
        vn0 = f.verts[-1].idx
        for v1 in f.verts:
            vn1 = v1.idx
            if vn0 < vn1:
                e = (vn0,vn1)
            else:
                e = (vn1,vn0)
            try:
                test = (e in vertEdges[vn0])
            except:
                test = False
            if not test:
                vertEdges[vn0].append(e)
                vertEdges[vn1].append(e)
            vn0 = vn1                

    for v in obj.verts:
        (sx,sy,sz) = (0,0,0)
        for (vn0,vn1) in vertEdges[v.idx]:
            v0 = obj.verts[vn0]
            v1 = obj.verts[vn1]
            s = fastmath.vsub3d(v0.co, v1.co)
            sx += math.fabs(s[0])
            sy += math.fabs(s[1])
            sz += math.fabs(s[2])
        warp[v.idx] = (sx,sy,sz)            

    if True:        
        fp = open("shared/mhx/female_young_warp.txt", "r")
        vn = 0
        for line in fp:
            words = line.split()
            (sx,sy,sz) = warp[vn]
            (rx,ry,rz) = (float(words[0]), float(words[1]), float(words[2]))
            #print vn
            #print "  ", (sx,sy,sz)
            #print "  ", (rx,ry,rz)
            warp[vn] = (sx/rx, sy/ry, sz/rz)
            vn += 1
        fp.close()
        the.Config.warpField = warp
        return warp        
    else:        
        fp = open("shared/mhx/female_young_warp.txt", "w")
        n = len(obj.verts)
        eps = 1e-4
        for vn in range(n):
            (sx,sy,sz) = warp[vn]
            if sx < eps: sx = eps
            if sy < eps: sy = eps
            if sz < eps: sz = eps
            fp.write("%.4g %.4g %.4g\n" % (sx,sy,sz))
        fp.close()
        halt
"""

def readExpressions(human):
    exprList = []

    for name in Expressions:
        (expr, wsum) = loopGendersAges(name, human, "Expressions")
        #expr = readTarget(name, human, "Expressions")
        exprList.append((name, expr))
        #print("    Done %s weight %.3f" % (name, wsum))
    return exprList


def readExpressionUnits(human):
    exprList = []
    for name in ExpressionUnits:
        (expr, wsum) = loopGendersAges(name, human, "ExpressionUnits")
        #expr = readTarget(name, human, "Expressions")
        exprList.append((name, expr))
        #print("    Done %s weight %.3f" % (name, wsum))
    return exprList


def readCorrective(human, path):
    (expr, wsum) = loopGendersAges(path, human, "Corrective")
    #expr = readTarget(path, human, "Corrective")
    #print("    Done %s weight %.3f" % (path, wsum))
    return expr

            



