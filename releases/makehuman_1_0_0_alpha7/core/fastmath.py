#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Common 3D Algebric functions.

B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2011

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

This module contains some specific versions of often used vector methods which are faster than the ones in aljabr.
"""

from math import sqrt, cos, sin, tan, atan2, fabs, acos, pow

def vadd3d(v1, v2):
    return [v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2]]

def vsub3d(v1, v2):
    return [v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]]

def vmul3d(v, s):
    return [v[0]*s, v[1]*s, v[2]*s]
    
def vlen3d(v):
    return sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
    
def vsqr3d(v):
    return (v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
    
def vnorm3d(v):
    len = sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
    if len:
        return [v[0]/len, v[1]/len, v[2]/len]
    else:
        return [0.0, 0.0, 0.0]
    
def vavg2d(v1, v2):
    return [(v1[0] + v2[0]) / 2.0, (v1[1] + v2[1]) / 2.0]
        
def vavg2d4(v1, v2, v3, v4):
    return [(v1[0] + v2[0] + v3[0] + v4[0]) / 4.0, (v1[1] + v2[1] + v3[1] + v4[1]) / 4.0]
    
def vavg3d(v1, v2):
    return [(v1[0] + v2[0]) / 2.0, (v1[1] + v2[1]) / 2.0, (v1[2] + v2[2]) / 2.0]
    
def vavg3d4(v1, v2, v3, v4):
    return [(v1[0] + v2[0] + v3[0] + v4[0]) / 4.0, (v1[1] + v2[1] + v3[1] + v4[1]) / 4.0, (v1[2] + v2[2] + v3[2] + v4[2]) / 4.0]
