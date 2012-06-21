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

Expressions = [
    'smile',
    'hopeful',
    'innocent',
    'tender',
    'seductive',

    'grin',
    'excited',
    'ecstatic',

    'proud',
    'pleased',
    'amused',
    'laughing1',
    'laughing2',

    'so-so',
    'blue',
    'depressed',
    'sad',
    'distressed',
    'crying',
    'pain',

    'disappointed',
    'frustrated',
    'stressed',
    'worried',
    'scared',
    'terrified',

    'shy',
    'guilty',
    'embarassed',
    'relaxed',
    'peaceful',
    'refreshed',

    'lazy',
    'bored',
    'tired',
    'drained',
    'sleepy',
    'groggy',

    'curious',
    'surprised',
    'impressed',
    'puzzled',
    'shocked',
    'frown',
    'upset',
    'angry',
    'enraged',

    'skeptical',
    'vindictive',
    'pout',
    'furious',
    'grumpy',
    'arrogant',
    'sneering',
    'haughty',
    'disgusted',
]


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
                
            if typ == "Expressions":                
                filename = 'data/targets/expression/%s_%s/neutral_%s_%s_%s.target' % (gender, age, gender, age, name)
            elif typ == "Corrective":
                filename = "data/correctives/%s/%s-%s.target" % (name, gender, age)
            #print ("Try", filename)                
            try:
                fp = open(filename, "rU")
            except:
                print("*** Cannot open %s" % filename)
                fp = 0
                
            if fp:
                aexpr = {}                    
                for line in fp:
                    words = line.split()
                    aexpr[int(words[0])] = (float(words[1]), -float(words[3]), float(words[2]))    
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


def readExpressions(human):
    exprList = []
    for name in Expressions:
        (expr, wsum) = loopGendersAges(name, human, "Expressions")
        exprList.append((name, expr))
        #print("    Done %s weight %.3f" % (name, wsum))
    return exprList


def readCorrective(human, path):
    (expr, wsum) = loopGendersAges(path, human, "Corrective")
    #print("    Done %s weight %.3f" % (path, wsum))
    return expr

            



