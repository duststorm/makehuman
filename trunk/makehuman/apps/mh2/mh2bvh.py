#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Export anatomical and pose data as Biovision motion capture data in BVH format.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements a plugin to export MakeHuman skeleton data in Biovision BVH format.
The BioVision Hierarchy formmat (BVH) is widely supported as a means of exchanging anatomical 
and pose data with other applications used for animating human forms.  

Requires:

- base modules

"""

__docformat__ = 'restructuredtext'

from skeleton import Skeleton

def exportSkeleton(obj, filename):
    """
    This function exports joint information describing the structure of the 
    MakeHuman humanoid mesh object in Biovision BVH format. 
    
    Parameters
    ----------
   
    obj:     
      *Object3D*.  The object whose information is to be used for the export.
    filename:     
      *string*.  The filename of the file to export the object to.
    """

    skeleton = Skeleton()
    skeleton.update(obj)

    # Write bvh file

    f = open(filename, 'w')
    f.write('HIERARCHY\n')
    f.write('ROOT ' + skeleton.root.name + '\n')
    f.write('{\n')
    f.write("\tOFFSET	%f  %f  %f\n" %(skeleton.root.position[0],skeleton.root.position[1],skeleton.root.position[2]))
    f.write('\tCHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation\n')
    for joint in skeleton.root.children:
        writeJoint(f, joint, 1)
    f.write('}\n')
    f.write('MOTION\n')
    f.write('Frames:    1\n')
    f.write('Frame Time: 0.0\n')
    f.write(" %f  %f  %f" %(skeleton.root.position[0],skeleton.root.position[1],skeleton.root.position[2]) )
    for i in xrange(skeleton.endEffectors):
      f.write(" 0.0000 0.0000 0.0000")
    f.write("\n")
    f.close()


def writeJoint(f, joint, ident):
    """
  This function writes out information describing one joint in BVH format. 
  
  Parameters
  ----------
  
  f:     
    *file handle*.  The handle of the file being written to.
  joint:     
    *Joint object*.  The joint object to be processed by this function call.
  ident:     
    *integer*.  The joint identifier.
  """

    f.write('\t' * ident + 'JOINT ' + joint.name + '\n')
    f.write('\t' * ident + '{\n')
    f.write('\t' * (ident + 1) + "OFFSET	%f  %f  %f\n" % (joint.offset[0], joint.offset[1], joint.offset[2]))
    f.write('\t' * (ident + 1) + 'CHANNELS 3 Zrotation Xrotation Yrotation\n')
    if joint.children:
        for joint in joint.children:
            writeJoint(f, joint, ident + 1)
    else:
        f.write('\t' * (ident + 1) + 'End Site\n')
        f.write('\t' * (ident + 1) + '{\n')
        f.write('\t' * (ident + 2) + "OFFSET	0.00	0.00	0.00\n")
        f.write('\t' * (ident + 1) + '}\n')
    f.write('\t' * ident + '}\n')
