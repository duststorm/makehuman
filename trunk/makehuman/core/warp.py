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

Warp vertex locations from a source character to a target character.

Let

    x_n             Location of vertex n in source character
    y_n             Location of vertex n in target character
    
    x + dx = f(x)   Morph of source character    
    y + dy = g(y)   Morph of target character
    
Given the sets (x_n) and (y_n) and the function f(x), we want to find g(y). To this
end, introduce the warp field U(x) and its inverse V(y)

    y = U(x)        Warp source location to target location
    x = V(y)        Warp target location to source location
    
Clearly, g = U o f o V, or

    g(y) = U(f(V(y)))
    
We only need the inverse warp field at vertex locations, viz. V(y_n) = x_n.  
The target morph (dy_n) is thus given by

    y_n + dy_n = U(x_n + dx_n)

The warp field U(x) is needed outside the original vertex set. 
Pick a set of landmark points (x_i), which is a subset of the vertices of the source 
character. The landmarks should be denser in interesting detail, and can be chosen 
differently depending on the morph. The warp function is assumed to be of the form

    U(x) = sum_i w_i h_i(x)
    
where (w_i) is a set of weights, and h_i(x) is a basis of RBFs (Radial Basis Function).
An RBF only depends on the distance from the landmark, i.e.

    h_i(x) = phi(|x - x_i|).
    
Our RBFs are Hardy functions,

    h_i(x) = sqrt( |x - x_i|^2 + s_i^2 ),
    
where s_i = min_(j != i) |x_j - x_i| is the minimal distance to another landmark.
To determine the weights w_i, we require that the warp field is exact for the landmarks:

    y_i = y(x_i) = U(x_i)
    
    y_i = sum_j H_ij w_j
    
    H_ij = h_j(x_i)
    
This can be written in matrix form: w = (w_j), y = (y_i), H = (H_ij):

    y = H w
    
We solve the equivalent equation, which probably has better numerical properties
    
    A w = b, 
    
where A = HT H, b = HT b, where HT is the transpose of H.
    
"""
   
import math
import fastmath

#----------------------------------------------------------
#   Try to load numpy.
#   Will only work if it is installed and for 32 bits.
#----------------------------------------------------------

#import numpy
import sys
import imp
import os

def getModule(modname, folder):        
    try:
        return sys.modules[modname]
    except KeyError:
        pass
    print("Trying to load %s" % modname)
    
    if modname not in os.listdir(folder):
        print("%s does not exist in %s" % (modname, folder))
        return None
        
    path = os.path.realpath(folder)
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.realpath(os.path.join(folder, modname))
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
    numpy = getModule("numpy", "lib/site-packages")  
except:
    numpy = None
if numpy:
    print("Numpy successfully loaded")
else:
    print("Failed to load numpy. Warping will not work")
    print("Continuing happily.")

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
            mindist2 = 1e12
            vxi = xverts[i]
            for j in range(n):
                if i != j:
                    vec = fastmath.vsub3d(vxi, xverts[j])
                    dist2 = fastmath.vsqr3d(vec)
                    if dist2 < mindist2:
                        mindist2 = dist2
                        if mindist2 < 1e-6:
                            print("  ", mindist2, i, j)
            self.s2[i] = mindist2

        self.H = numpy.identity(n, float)
        for i in range(n):
            xi = xverts[i]
            for j in range(n):
                self.H[i][j] = self.rbf(j, xi)
        
        self.HT = self.H.transpose()
        self.HTH = numpy.dot(self.HT, self.H)    
        #print("  Warp field set up: %d points" % n)

        self.solve(0)
        self.solve(1)
        self.solve(2)
        return
    
    
    def solve(self, index):        
        A = self.HTH
        b = numpy.dot(self.HT, self.y[index])
        self.w[index] = numpy.linalg.solve(A, b)
        e = self.y[index] - numpy.dot(self.H, self.w[index])
        ee = numpy.dot(e.transpose(), e)
        #print("Solved for index %d: Error %g" % (index, math.sqrt(ee)))
        #print(self.w[index])
        return
       

    def rbf(self, vn, x):
        vec = fastmath.vsub3d(x, self.x[vn])
        vec2 = fastmath.vsqr3d(vec)
        return math.sqrt(vec2 + self.s2[vn])
        
        
    def warpLoc(self, x):
        f = {}        
        for i in range(self.n):
            f[i] = self.rbf(i, x)

        y0 = 0
        w = self.w[0]            
        for i in range(self.n):
            y0 += w[i]*f[i]

        y1 = 0
        w = self.w[1]            
        for i in range(self.n):
            y1 += w[i]*f[i]

        y2 = 0
        w = self.w[2]            
        for i in range(self.n):
            y2 += w[i]*f[i]
            
        return [y0,y1,y2]
        
        
    def warpTarget(self, morph, source, target, landmarks):
        xverts = {}
        yverts = {}  
        for (m,n) in landmarks.items():
            xverts[m] = list(source[n])
            yverts[m] = list(target[n])
    
        self.setup(xverts, yverts)
        self.solve(0)
        self.solve(1)
        self.solve(2)

        ymorph = {}
        for n in morph.keys():
            xloc = fastmath.vadd3d(morph[n], source[n])
            yloc = self.warpLoc(xloc)
            ymorph[n] = fastmath.vsub3d(yloc, target[n])
            
        """
            print n
            print "  X0", source[n]
            print "  Y0", target[n].co
            print "  X ", xloc
            print "  Y ", yloc
            print "  DX", morph[n]
            print "  DY", ymorph[n]
        halt
        """
        return ymorph        
        
           
      