#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Export mesh data as a Wavefront obj format file.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010

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
from os.path import basename

def exportObj(obj, filename, exportGroups = True, groupFilter=None):
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
    f.write('mtllib ' + basename(filename) + '.mtl\n')

    for v in obj.verts:
        f.write('v %f %f %f\n' % (v.co[0], v.co[1], v.co[2]))

    if not (obj.uvValues==None):
      for uv in obj.uvValues:
          f.write('vt %f %f\n' % (uv[0], uv[1]))

    for v in obj.verts:
        f.write('vn %f %f %f\n' % (v.no[0], v.no[1], v.no[2]))

    f.write('usemtl basic\n')
    f.write('s off\n')
      
    for fg in obj.facesGroups:
        if not groupFilter or groupFilter(fg):
            if exportGroups:
                f.write('g %s\n' % fg.name)
            for face in fg.faces:
                f.write('f')
                for i, v in enumerate(face.verts):
                    if (obj.uvValues == None):
                        f.write(' %i//%i ' % (v.idx + 1, v.idx + 1))
                    else:
                        f.write(' %i/%i/%i ' % (v.idx + 1, face.uv[i] + 1, v.idx + 1))
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
    if not (obj.texture==None): f.write('map_Kd %s\n' % basename(obj.texture).replace('.tif', '.png'))
    f.close()
    
def exportAsCurves(file, guides):
    DEG_ORDER_U = 2 #formerly 3, but blender adds 1 to teh degree
    # use negative indices
    for guide in guides:
      N = len(guide)
      for i in xrange(0,N):
        file.write('v %.6f %.6f %.6f\n' % (guide[i][0], guide[i][1],\
                                           guide[i][2]))
      #name = group.name+"_"+guide.name 
      #file.write('g %s\n' % name)
      file.write('cstype bspline\n') # not ideal, hard coded
      file.write('deg %d\n' % DEG_ORDER_U) # not used for curves but most files have it still
    
      curve_ls = [-(i+1) for i in xrange(N)]
      file.write('curv 0.0 1.0 %s\n' % (' '.join( [str(i) for i in curve_ls] ))) # hair  has no U and V values for the curve
    
      # 'parm' keyword
      tot_parm = (DEG_ORDER_U + 1) + N
      tot_parm_div = float(tot_parm-1)
      parm_ls = [(i/tot_parm_div) for i in xrange(tot_parm)]
      #our hairs dont do endpoints.. *sigh*
      file.write('parm u %s\n' % ' '.join( [str(i) for i in parm_ls] ))
    
      file.write('end\n')
