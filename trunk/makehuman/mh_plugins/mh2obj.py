#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Export mesh data as a Wavefront obj format file.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements a plugin to export a mesh object in Wavefront obj format.
Requires:

- base modules

"""

__docformat__ = 'restructuredtext'

import files3d
import types


def exportObj(obj, filename, base=True):
    """
    This function exports a mesh object in Wavefront obj format. It is assumed that obj will have at least vertices and
    faces (exception handling for vertices/faces must be done outside this method).
    
    Parameters
    ----------
   
    obj:     
      *Object3D*.  The object to export.
    filename:     
      *string*.  The filename of the file to export the object to.
    """

    # Write obj file

    f = open(filename, 'w')
    f.write('# MakeHuman exported OBJ\n')
    f.write('# www.makehuman.org\n')
    f.write('mtllib ' + filename + '.mtl\n')

    for v in obj.verts:
        f.write('v %f %f %f\n' % (v.co[0], v.co[1], v.co[2]))

    if not (obj.uvValues==None):
      for uv in obj.uvValues:
          f.write('vt %f %f\n' % (uv[0], uv[1]))

    for v in obj.verts:
        f.write('vn %f %f %f\n' % (v.no[0], v.no[1], v.no[2]))

    f.write('usemtl basic\n')
    f.write('s off\n')

    if base:
      faces = files3d.loadFacesIndices('data/3dobjs/base.obj', True)
    else:
      faces = obj.faces
    for fc in faces:
        if type(fc) is types.StringType:
            f.write('g %s\n' % fc)
        else:
            f.write('f')
            for v in fc:
                f.write(' %i/%i/%i ' % (v[0] + 1, v[1] + 1, v[0] + 1))
            f.write('\n')
    f.close()

    # Write material file

    f = open(filename + '.mtl', 'w')
    f.write('# MakeHuman exported MTL\n')
    f.write('# www.makehuman.org\n')
    f.write('newmtl basic\n')
    f.write('Ka 1.0 1.0 1.0\n')
    f.write('Kd 1.0 1.0 1.0\n')
    f.write('Ks 0.33 0.33 0.52\n')
    f.write('illum 5\n')
    f.write('Ns 50.0\n')
    if not (obj.texture==None): f.write('map_Kd -clamp on ' + obj.texture + '\n')
    f.close()


