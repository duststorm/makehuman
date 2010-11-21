#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Export to stereolithography format.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements a plugin to export MakeHuman mesh to stereolithography format.
See http://en.wikipedia.org/wiki/STL_(file_format) for information on the format.

Requires:

- base modules

"""

__docformat__ = 'restructuredtext'

import module3d
import aljabr
from math import acos

def exportStlAscii(obj, filename, exportJoints = False):
    """
    This function exports MakeHuman mesh and skeleton data to stereolithography format. 
    
    Parameters
    ----------
   
    obj:     
      *Object3D*.  The object whose information is to be used for the export.
    filename:     
      *string*.  The filename of the file to export the object to.
    """
    
    f = open(filename, 'w')
    f.write('solid human\n')
    for face in obj.faces:
        if not exportJoints and 'joint' in face.group.name:
            continue
        f.write('facet normal %f %f %f\n' % (face.no[0], face.no[1], face.no[2]))
        f.write('\touter loop\n')
        f.write('\t\tvertex %f %f %f\n' % (face.verts[0].co[0], face.verts[0].co[1], face.verts[0].co[2]))
        f.write('\t\tvertex %f %f %f\n' % (face.verts[1].co[0], face.verts[1].co[1], face.verts[1].co[2]))
        f.write('\t\tvertex %f %f %f\n' % (face.verts[2].co[0], face.verts[2].co[1], face.verts[2].co[2]))
        f.write('\tendloop\n')
        f.write('\tendfacet\n')
    f.write('endsolid human\n')
    