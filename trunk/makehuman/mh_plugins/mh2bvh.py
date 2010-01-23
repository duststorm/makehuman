#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Export anatomical and pose data as Biovision motion capture data in BVH format.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni

**Copyright(c):**      MakeHuman Team 2001-2009

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

import module3d
import aljabr


class Joint:

    """
  This class contains a simple constructor method for a data structure used to support 
  the BVH export functions. 
  A hierarchical nested list of these objects is defined to hold the joint positions and
  the relationship between joints. 
  """

    def __init__(self, name, children):
        self.name = name
        self.children = children
        self.position = [0.0, 0.0, 0.0]
        self.offset = [0.0, 0.0, 0.0]


skeletonRoot = Joint('joint-pelvis', [Joint('joint-spine3', [Joint('joint-spine2', [Joint('joint-spine1', [Joint('joint-neck', [Joint('joint-head', [Joint('joint-mouth',
                     []), Joint('joint-l-eye', []), Joint('joint-r-eye', [])])]), Joint('joint-r-clavicle', [Joint('joint-r-shoulder', [Joint('joint-r-elbow',
                     [Joint('joint-r-hand', [Joint('joint-r-finger-1-1', [Joint('joint-r-finger-1-2', [Joint('joint-r-finger-1-3', [])])]), Joint('joint-r-finger-2-1',
                     [Joint('joint-r-finger-2-2', [Joint('joint-r-finger-2-3', [])])]), Joint('joint-r-finger-3-1', [Joint('joint-r-finger-3-2',
                     [Joint('joint-r-finger-3-3', [])])]), Joint('joint-r-finger-4-1', [Joint('joint-r-finger-4-2', [Joint('joint-r-finger-4-3', [])])]),
                     Joint('joint-r-finger-5-1', [Joint('joint-r-finger-5-2', [Joint('joint-r-finger-5-3', [])])])])])])]), Joint('joint-l-clavicle',
                     [Joint('joint-l-shoulder', [Joint('joint-l-elbow', [Joint('joint-l-hand', [Joint('joint-l-finger-1-1', [Joint('joint-l-finger-1-2',
                     [Joint('joint-l-finger-1-3', [])])]), Joint('joint-l-finger-2-1', [Joint('joint-l-finger-2-2', [Joint('joint-l-finger-2-3', [])])]),
                     Joint('joint-l-finger-3-1', [Joint('joint-l-finger-3-2', [Joint('joint-l-finger-3-3', [])])]), Joint('joint-l-finger-4-1',
                     [Joint('joint-l-finger-4-2', [Joint('joint-l-finger-4-3', [])])]), Joint('joint-l-finger-5-1', [Joint('joint-l-finger-5-2',
                     [Joint('joint-l-finger-5-3', [])])])])])])])])])]), Joint('joint-r-upper-leg', [Joint('joint-r-knee', [Joint('joint-r-ankle',
                     [Joint('joint-r-toe-1-1', [Joint('joint-r-toe-1-2', [])]), Joint('joint-r-toe-2-1', [Joint('joint-r-toe-2-2', [Joint('joint-r-toe-2-3', [])])]),
                     Joint('joint-r-toe-3-1', [Joint('joint-r-toe-3-2', [Joint('joint-r-toe-3-3', [])])]), Joint('joint-r-toe-4-1', [Joint('joint-r-toe-4-2',
                     [Joint('joint-r-toe-4-3', [])])]), Joint('joint-r-toe-5-1', [Joint('joint-r-toe-5-2', [Joint('joint-r-toe-5-3', [])])])])])]),
                     Joint('joint-l-upper-leg', [Joint('joint-l-knee', [Joint('joint-l-ankle', [Joint('joint-l-toe-1-1', [Joint('joint-l-toe-1-2', [])]),
                     Joint('joint-l-toe-2-1', [Joint('joint-l-toe-2-2', [Joint('joint-l-toe-2-3', [])])]), Joint('joint-l-toe-3-1', [Joint('joint-l-toe-3-2',
                     [Joint('joint-l-toe-3-3', [])])]), Joint('joint-l-toe-4-1', [Joint('joint-l-toe-4-2', [Joint('joint-l-toe-4-3', [])])]), Joint('joint-l-toe-5-1',
                     [Joint('joint-l-toe-5-2', [Joint('joint-l-toe-5-3', [])])])])])])])


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

    calcJointOffsets(obj, skeletonRoot)

    # Write bvh file

    f = open(filename, 'w')
    f.write('HIERARCHY\n')
    f.write('ROOT ' + skeletonRoot.name + '\n')
    f.write('{\n')
    f.write("\tOFFSET	0.00	0.00	0.00\n")
    f.write('\tCHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation\n')
    for joint in skeletonRoot.children:
        writeJoint(f, joint, 1)
    f.write('}\n')
    f.write('MOTION\n')
    f.write('Frames:    0\n')
    f.write('Frame Time: 0.0\n')
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


def calcJointOffsets(obj, joint, parent=None):
    """
    This function calculates the position and offset for a joint and calls itself for 
    each 'child' joint in the hierarchical joint structure. 
    
    Parameters
    ----------
    
    obj:     
      *Object3D*.  The object whose information is to be used for the calculation.
    joint:     
      *Joint Object*.  The joint object to be processed by this function call.
    parent:     
      *Joint Object*.  The parent joint object or 'None' if not specified.
    """

    # Calculate joint positions

    g = obj.getFaceGroup(joint.name)
    verts = []
    print joint.name
    for f in g.faces:
        for v in f.verts:
            verts.append(v.co)
    joint.position = aljabr.centroid(verts)

    # Calculate offset

    if parent:
        joint.offset = aljabr.vsub(joint.position, parent.position)

    # Calculate child offsets

    for child in joint.children:
        calcJointOffsets(obj, child, joint)


