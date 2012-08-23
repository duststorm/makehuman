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
   
import fastmath

#----------------------------------------------------------
#   Try to load numpy.
#   Will only work if it is installed and for 32 bits.
#----------------------------------------------------------

#import numpy
import sys
import imp
import os

def getModule(modname):        
    try:
        return sys.modules[modname]
    except KeyError:
        pass
    print("Trying to load %s" % modname)
    
    if modname not in os.listdir("pythonmodules"):
        print("%s does not exist in pythonmodules" % modname)
        return None
        
    path = os.path.realpath("pythonmodules/%s" % modname)
    if path not in sys.path:
        sys.path.append(path)
        
    fp, pathname, description = imp.find_module(modname)
    try:
        imp.load_module(modname, fp, pathname, description)
    finally:
        if fp:
            fp.close()
    return sys.modules[modname]
    
try:    
    numpy = getModule("numpy")  
    print("Numpy successfully loaded")
except:
    numpy = None
    print("Failed to load numpy. Warping will not work")

#----------------------------------------------------------
#   class CWarp
#----------------------------------------------------------

class CWarp:
    def __init__(self):
        self.n = 0
        self.x = {}
        self.y = {}
        self.w = {}       
        self.H = None
        self.s2 = {}
            
        
    def setup(self, xverts, yverts):
        self.n = len(xverts)
        n = self.n
        
        for i in range(n):
            self.x[i] = xverts[i]
            
        for k in range(3):
            self.w[k] = numpy.arange(n, dtype=float)
            for i in range(n):
                self.w[k][i] = 0.1

            self.y[k] = numpy.arange(n, dtype=float)
            for i in range(n):
                self.y[k][i] = yverts[i][k]

        for i in range(n):
            mindist = 1e6
            vxi = xverts[i]
            for j in range(n):
                if i != j:
                    vec = vxi - xverts[j]
                    if vec.length < mindist:                        
                        mindist = vec.length
                        if mindist < 1e-3:
                            print("  ", mindist, i, j)
            self.s2[i] = (mindist*mindist)

        self.H = numpy.identity(n, float)
        for i in range(n):
            xi = xverts[i]
            for j in range(n):
                self.H[i][j] = self.rbf(j, xi)
        
        self.HT = self.H.transpose()
        self.HTH = numpy.dot(self.HT, self.H)    
        print("Warp set up: %d points" % n)

        self.solve(0)
        self.solve(1)
        self.solve(2)
        return
    
    
    def solve(self, index):        
        A = self.HTH + self.lamb * numpy.identity(self.n, float) 
        b = numpy.dot(self.HT, self.y[index])
        self.w[index] = numpy.linalg.solve(A, b)
        e = self.y[index] - numpy.dot(self.H, self.w[index])
        ee = numpy.dot(e.transpose(), e)
        print("Solved for index %d: Error %g" % (index, math.sqrt(ee)))
        #print(self.w[index])
        return
       

    def rbf(self, vn, x):
        vec = x - self.x[vn]
        vec2 = vec.dot(vec)
        return math.sqrt(vec2 + self.s2[vn])
        
        
    def warpLoc(self, x):
        y = mathutils.Vector((0,0,0))
        f = {}        
        for i in range(self.n):
            f[i] = self.rbf(i, x)
        for k in range(3):
            w = self.w[k]
            for i in range(self.n):
                y[k] += w[i]*f[i]
            """                
            for k in range(3):
                y[k] += w[self.n+k]*x[k]
            y[k] += w[self.n+3]
            """
        return y    
        
        
    def warpTarget(self, morph, source, target, landmarks):
        xverts = {}
        yverts = {}  
        m = 0
        for n in landmarks:
            xverts[m] = source[n]
            yverts[m] = target[n]
            m += 1

        self.setup(xverts, yverts)
        self.solve(0)
        self.solve(1)
        self.solve(2)

        ymorph = {}
        for n in morph.verts.keys():
            xloc = fastmath.vadd3d(morph.verts[n].co, source.verts[n].co)
            yloc = self.warpLoc(xloc)
            ymorph[n] = fastmath.vsub3d(yloc, target.verts[n].co)
        return ymorph        
        
           
      