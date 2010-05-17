#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Export to id Software's MD5 format.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements a plugin to export MakeHuman mesh and skeleton data to id Software's MD5 format.
See http://www.modwiki.net/wiki/MD5MESH_(file_format) for information on the format.

Requires:

- base modules

"""

__docformat__ = 'restructuredtext'

import module3d
import aljabr
from math import acos

class Joint:

    """
  This class contains a simple constructor method for a data structure used to support 
  the skeleton export functions. 
  A hierarchical nested list of these objects is defined to hold the joint positions and
  the relationship between joints. 
  """

    def __init__(self, name, children):
        self.name = name
        self.parent = None
        self.children = children
        self.position = [0.0, 0.0, 0.0]         # Global position in the scene
        self.offset = [0.0, 0.0, 0.0]           # Position Relative to the parent joint
        self.direction = [0.0, 0.0, 0.0, 0.0]   # Global rotation in the scene
        self.rotation = [0.0, 0.0, 0.0, 0.0]    # Rotation relative to the parent joint
        self.index = 0

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


def exportMd5(obj, filename):
    """
    This function exports MakeHuman mesh and skeleton data to id Software's MD5 format. 
    
    Parameters
    ----------
   
    obj:     
      *Object3D*.  The object whose information is to be used for the export.
    filename:     
      *string*.  The filename of the file to export the object to.
    """

    joints = calcJointOffsets(obj, skeletonRoot)

    f = open(filename, 'w')
    f.write('MD5Version 10\n')
    f.write('commandline ""\n\n')
    f.write('numJoints %d\n' % (joints+1)) # Amount of joints + the hardcoded origin below
    f.write('numMeshes %d\n\n' % (1)) # TODO: 2 in case of hair
    f.write('joints {\n')
    f.write('\t"%s" %d ( %f %f %f ) ( %f %f %f )\n' % ('origin', -1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    writeJoint(f, skeletonRoot)
    f.write('}\n\n')
    f.write('mesh {\n')
    f.write('\tshader "%s"\n' % (obj.texture or "")) # TODO: create the shader file
    f.write('\n\tnumverts %d\n' % (len(obj.verts)))
    for vert in obj.verts:
        if obj.uvValues:
            face = vert.sharedFaces[0]
            u, v = obj.uvValues[face.uv[face.verts.index(vert)]]
        else:
            u, v = 0, 0
        # vert [vertIndex] ( [texU] [texV] ) [weightIndex] [weightElem]
        f.write('\tvert %d ( %f %f ) %d %d\n' % (vert.idx, u, v, vert.idx, 1))
    f.write('\n\tnumtris %d\n' % (len(obj.faces)))
    for face in obj.faces:
        # tri [triIndex] [vertIndex1] [vertIndex2] [vertIndex3]
        f.write('\ttri %d %d %d %d\n' % (face.idx, face.verts[2].idx, face.verts[1].idx, face.verts[0].idx))
    f.write('\n\tnumweights %d\n' % (len(obj.verts)))
    for vert in obj.verts:
        # TODO: We attach all vertices to the root with weight 1.0, this should become
        # real weights to the correct bones
        # weight [weightIndex] [jointIndex] [weightValue] ( [xPos] [yPos] [zPos] )
        f.write('\tweight %d %d %f ( %f %f %f )\n' % (vert.idx, 0, 1.0, vert.co[0], -vert.co[2], vert.co[1]))
    f.write('}\n\n')
    f.close()


def writeJoint(f, joint):
    """
  This function writes out information describing one joint in MD5 format. 
  
  Parameters
  ----------
  
  f:     
    *file handle*.  The handle of the file being written to.
  joint:     
    *Joint object*.  The joint object to be processed by this function call.
  ident:     
    *integer*.  The joint identifier.
  """
    if joint.parent:
        parentIndex = joint.parent.index
    else:
        parentIndex = 0
    # "[boneName]"   [parentIndex] ( [xPos] [yPos] [zPos] ) ( [xOrient] [yOrient] [zOrient] )
    f.write('\t"%s" %d ( %f %f %f ) ( %f %f %f )\n' % (joint.name, parentIndex,
        joint.position[0], joint.position[1], joint.position[2],
        joint.direction[0], joint.direction[1], joint.direction[2]))

    for joint in joint.children:
        writeJoint(f, joint)

def calcJointOffsets(obj, joint, index = 0, parent=None):
    """
    This function calculates the position and offset for a joint and calls itself for 
    each 'child' joint in the hierarchical joint structure. It returns the amount of joints
    visited.
    
    Parameters
    ----------
    
    obj:     
      *Object3D*.  The object whose information is to be used for the calculation.
    joint:     
      *Joint Object*.  The joint object to be processed by this function call.
    parent:     
      *Joint Object*.  The parent joint object or 'None' if not specified.
    """
    
    # Store parent
    joint.parent = parent

    # Calculate position
    g = obj.getFaceGroup(joint.name)
    verts = []
    for f in g.faces:
        for v in f.verts:
            verts.append(v.co)
    joint.position = aljabr.centroid(verts)
    joint.position[1], joint.position[2] = -joint.position[2], joint.position[1]

    # Calculate offset
    if parent:
        joint.offset = aljabr.vsub(joint.position, parent.position)
        
    # Calculate direction
    direction = aljabr.vnorm(joint.offset)
    axis = aljabr.vnorm(aljabr.vcross([0.0, 0.0, 1.0], direction))
    angle = acos(aljabr.vdot([0.0, 0.0, 1.0], direction))
    joint.direction = aljabr.axisAngleToQuaternion(axis, angle)
    
    # Calculate rotation
    if parent:
        pass
        
    # Calculate index
    index += 1
    joint.index = index

    # Calculate child offsets
    for child in joint.children:
        index = calcJointOffsets(obj, child, index, joint)

    return index
