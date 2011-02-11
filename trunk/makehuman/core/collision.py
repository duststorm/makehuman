#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Collision Avoidance Algorithm for Hair

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Jose Capco

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
========

This module contains methods for collision avoidance of hair strands. When MakeHuman loads a hair, this hair is a model based
on a neutral body model. However when the model properties are changed (for instance: age, height, etc.) then there is the possibility of
hair strands to pierce through the model mesh. Thus hair appears to go inside the body. The methods in this module will allow the hair strand to
be re-edited such that they follow the tangent of the mesh of the body instead of piercing through the body. Costume made hair may also pierce 
through the body. The methods can be used to enhance some costume modelled hair for MakeHuman.
"""

import math
import simpleoctree
from aljabr import *


def getTangent(point, i, verts, size, isNurb=False, res=0.08):  # default Octree Resolution is set to 0.08
    """
    To be Documented
    """
    l = (1.5 * res) * math.sqrt(3.0)  # longest distance of an octree smallest cube
    if size < l:
        l = size
    size = size - l  # josenow
    L2 = verts[i].co
    vec1 = vsub(point, L2)
    normal = verts[i].no

    # if math.abs(diffang(vec1,normal))

    scalar = vdot(normal, vec1)
    point2 = []
    if isNurb and not scalar == 0 and math.fabs(math.acos(scalar / vlen(vec1))) > math.pi / 2:

    # For nurbs.. is angle of incidence obtuse? if so deflect through the same direction as incident from point

        point2 = vmul(vec1, -res / vlen(vec1))
        point2 = vadd(L2, point2)
        print 'point2 is: ', point2
        print 'Deflection is done through incidence'
    else:

        # YES! then try to deflect through the tangent space

        tangent = vsub(vec1, vmul(normal, scalar))
        N = vlen(tangent)
        if not N == 0:
            tangent = vmul(tangent, -l / N)
            point2 = vadd(L2, tangent)
            point2 = vadd(point2, vmul(normal, res))
        else:
            print 'Collision and normal lines are parallel'
            tangent = [normal[0], -normal[2], normal[1]]  # arbitrary rotation of 90deg.. choose x-axis rotation!
            tangent = vmul(tangent, l)
            point2 = vadd(L2, tangent)
    if size <= 0:
        return [L2, point2]
    else:
        return [L2, point2, vadd(point2, vmul(normal, size))]


# check if an unordered interval (i.e. we can have [a,b] with a>=b) is in an ordered interval (i.e. [a,b] has always a<=b)
def unordInOrd(unord, ord):
    if unord[0] <= unord[1]:
        return unord[0] <= ord[1] and ord[0] <= unord[1]
    else:
        return unord[1] <= ord[1] and ord[0] <= unord[0]


# checks if 2 ordered interval in real numbers intersect


def intIntersects(int1, int2):
    return int1[0] <= int2[1] and int2[0] <= int1[1]


# checks if line crosses cube!
# line consists of two vertices


def lineInCube(line, cube):
    """
    This methods returns true if the given line passes through the cube (a cuboid can be used). Otherwise it returns false. Note that our
    definition of cuboid is based on U{http://mathworld.wolfram.com/Cuboid.html} rather than the more general 
    U{http://en.wikipedia.org/wiki/Cuboid}.
    
    @rtype: bool
    @return: True if line passes through a cuboid, otherwise false
    @type line: List of list of floats
    @param line: This is a list consisting of two endpoints in the 3D space representing a line. Each endpoint is a list of 3 float coordinates.
    @type cube: List of list of floats
    @param cube: This is a list consisting of two corner points of a cuboid in 3D. Each corner point is a list of 3 float coordinates.
    """
    returnValue = False
    x = [line[0][0], line[1][0]]

    # Projection on 1dim, x-axis:

    if unordInOrd(x, [cube[0][0], cube[1][0]]):
        if x[0] <= x[1]:
            if x[0] < cube[0][0]:
                x[0] = cube[0][0]
            if x[1] > cube[1][0]:
                x[1] = cube[1][0]
        else:
            if x[1] < cube[0][0]:
                x[1] = cube[0][0]
            if x[0] > cube[1][0]:
                x[0] = cube[1][0]

        # Projection on 2dimensions, x and y-axes
        y = [[], []]
        (t1, t2) = ([], [])
        if not line[1][0] == line[0][0]:
            t1 = (x[0] - line[0][0]) / (line[1][0] - line[0][0])  # basic homlogical algebra
            y[0] = line[0][1] * (1 - t1) + line[1][1] * t1  # intersection between line and cube in y-axis
            t2 = (x[1] - line[0][0]) / (line[1][0] - line[0][0])
            y[1] = line[0][1] * (1 - t2) + line[1][1] * t2
        else:
            # line is vertical, i.e. x remains constant!
            y[0] = line[0][1]
            y[1] = line[1][1]
            (t1, t2) = (0, 1)
        
        if unordInOrd(y, [cube[0][1], cube[1][1]]):
            # Entire 3D
            z = [[], []]
            z[0] = line[0][2] * (1 - t1) + line[1][2] * t1  # intersection between line and cube in z-axis
            z[1] = line[0][2] * (1 - t2) + line[1][2] * t2
            returnValue = unordInOrd(z, [cube[0][2], cube[1][2]])
    return returnValue


def lineThruQuad(line,quad):
    pass
    
def lineInColoredLeaf(line, root):  # root is of type SimpleOctreeVolume found in simpleoctree.py
    cube = [root.bounds[0], root.bounds[6]]  # take the two corners that fully defines a cube
    if not lineInCube(line, cube):
        return False
    elif len(root.children) == 0:
        # is it a leaf?
        if len(root.verts) == 0:  # is it an empty leaf?
            return False
        else:
            return True  # line passes through a colored leaf!
    else:
        returnValue = False
        i = 0
        while returnValue == False and i < len(root.children):
            returnValue = lineInColoredLeaf(line, root.children[i])
            i = i + 1  # recursive search through children and ask if line passes a colored leaf
    return returnValue


# line consist of two vertices in world coordinates, line is in general two subsequent control point of a curve
# i is the ith vertex of object by which line must be deflected
# isNurb asks whether line is subsequent controlPoint of a nurb, if yes then the algorithm is improved so deflection regards the actualy
# curve and not the line connecting controlpoints
# line consist of two vertices in world coordinates, line is in general two subsequent control point of a curve
# i is the ith vertex of object by which line must be deflected
# isNurb asks whether line is subsequent controlPoint of a nurb, if yes then the algorithm is improved so deflection regards the actualy
# curve and not the line connecting controlpoints
def deflect(line, verts, gravity, isNurb=True):  # assume gravity is negative y-direction!
    G = [0, -1, 0]  # vector direction of gravity

    dist = ()  # infinity in python
    near = []
    for j in range(0, len(verts)):
        if [verts[j].co[0], verts[j].co[1], verts[j].co[2]] == line[1]:
            return 0  # 0 means do not change the curve
            print 'line[1] and mesh verts match'
        if gravity and verts[j].co[1] < line[0][1] or not gravity:  # assume G=[0,-1,0]
            distTemp = vdist(line[0], verts[j].co)
            if distTemp < dist:
                dist = distTemp
                near = j
    if near == []:
        return 0
    else:
        size = vdist(verts[near].co, line[1])

    if size > 0.0001:  # TODO add minimal unit
        if not gravity:
            return getTangent(line[0], near, mesh, size, isNurb)
        else:
            point = [verts[near].co[0], verts[near].co[1], verts[near].co[2]]
            point = vsub(point, G)
            return getTangent(point, near, verts, size, isNurb)

def collision(octree, curve, verts, res, cPIndices, gravity=True):
    """
    To be documented
    """
    j=1
    for j in xrange(1,len(cPIndices),2):
        i=cPIndices[j]
        if i>= len(curve): break
        if (j==(len(cPIndices)-1)):
            N = len(curve)
        else:
            N = cPIndices[j+1]
        #changed = False #for debugging
        while i < N:
            if lineInColoredLeaf([curve[i-1], curve[i]], octree.root):
                if i == N - 1:
                    tangent = deflect([curve[i - 1], curve[i]], verts, gravity)
                else:
                    tangent = deflect([curve[i - 1], curve[i], curve[i + 1]], verts, gravity)
                n = 1
                if not tangent == 0:
                    if not curve[i - 1] == tangent[0]:  # TODO in case after Tangent deflection we passthrough a second part of the body!
                        if len(tangent) == 3:
                            n = 2
                        delta = vsub(tangent[1], curve[i])
                        for k in range(0, n):
                            curve.insert(i, tangent[(n - 1) - k])
                        for j in range(i + n, len(curve)):
                            curve[j] = vadd(curve[j], delta)
                        #changed = True #for debugging
                        N = N + n
                i = i + n
            i = i + 1


