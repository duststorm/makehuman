""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

**Adapted from:**
/* dqconv.c

  Conversion routines between (regular quaternion, translation) and dual quaternion.

  Version 1.0.0, February 7th, 2007

  Copyright (C) 2006-2007 University of Dublin, Trinity College, All Rights 
  Reserved

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the author(s) be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.

  Author: Ladislav Kavan, kavanl@cs.tcd.ie

Abstract
--------
Dual quaternions

"""


import math
import numpy
import transformations as tm


class DualQuaternion:
    def __init__(self):
        self.even = numpy.zeros(4, float)
        self.odd = numpy.zeros(4, float)
        
    def __repr__(self):
        e = self.even
        o = self.odd
        return ("<DualQuat (%.4g %.4g %.4g %.4g) (%.4g %.4g %.4g %.4g)>" % 
            (e[0], e[1], e[2], e[3], o[0], o[1], o[2], o[3]))
        
    def zero(self):
        for n in range(4):
            self.even[n] = 0.0
            self.odd[n] = 0.0
    
    def weightedBoneSum(self, groups):
        self.zero()
        for bone,w in groups:
            dq = bone.dualQuat
            self.even += w * dq.even
            self.odd += w * dq.odd
        
    def normalize(self):
        q0 = self.even
        q1 = self.odd
        len0 = math.sqrt(q0[0]*q0[0] + q0[1]*q0[1] + q0[2]*q0[2] + q0[3]*q0[3]) 
        if len0 > 1e-4:
            for n in range(4):
                q0 /= len0
                q1 /= len0
    
    def fromMatrix(self, matrix):
        q0 = tm.quaternion_from_matrix(matrix)
        t = matrix[:3,3]
        self.even = q0
        q1 = self.odd
        q1[0] = -0.5*(t[0]*q0[1] + t[1]*q0[2] + t[2]*q0[3])
        q1[1] = 0.5*( t[0]*q0[0] + t[1]*q0[3] - t[2]*q0[2])
        q1[2] = 0.5*(-t[0]*q0[3] + t[1]*q0[0] + t[2]*q0[1])
        q1[3] = 0.5*( t[0]*q0[2] - t[1]*q0[1] + t[2]*q0[0])

    def toMatrix(self):
        q0 = self.even
        mat = tm.quaternion_matrix(q0)
        q1 = self.odd        
        mat[0,3] = 2.0*(-q1[0]*q0[1] + q1[1]*q0[0] - q1[2]*q0[3] + q1[3]*q0[2])
        mat[1,3] = 2.0*(-q1[0]*q0[2] + q1[1]*q0[3] + q1[2]*q0[0] - q1[3]*q0[1])
        mat[2,3] = 2.0*(-q1[0]*q0[3] - q1[1]*q0[2] + q1[2]*q0[1] + q1[3]*q0[0])
        return mat

