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
Blender API mockup

"""


import numpy
import armature
from armature import transformations as tm

#------------------------------------------------------------------
#   Data types
#------------------------------------------------------------------

#class Vector:
#   def __init__(self, vec):
#        self.vector = numpy.array(vec)

Vector = numpy.array
        

class Matrix:        
    def __init__(self, size=4, data=None):
        self.size = size
        if data:
            self.matrix = numpy.array(data)    
        else:
            self.matrix = numpy.identity(4,float)
        
    def to_3x3(self):
        return Matrix(3, self.matrix[:3,:3])        
        
    def to_4x4(self):
        mat = Matrix(4)
        mat[:3,:3] = self.matrix[:3,:3]
        return mat        
        
    def decompose(self):
        loc = Vector(self.matrix[:3,3])
        rot = Matrix(self.matrix[:3,:3])
        scale = Vector(self.matrix[3,:3])
        return (loc,rot,scale)
                
    def to_euler(self):
        return tm.euler_from_matrix(self.matrix)
    
    def to_quaternion(self):
        return tm.quaternion_from_matrix(self.matrix)
    
        
        