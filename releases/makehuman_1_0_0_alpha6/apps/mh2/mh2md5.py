#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Export to id Software's MD5 format.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2011

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
from os.path import basename
from skeleton import Skeleton

groupWeights = (
    ('head-back-skull', 'joint-head', 1.0),
    ('head-brow', 'joint-head', 1.0),
    ('head-tongue', 'joint-head', 1.0),
    ('head-upper-skull', 'joint-head', 1.0),
    ('hip-navel', 'joint-spine2', 1.0),
    ('inner-mouth', 'joint-mouth', 1.0),
    ('jaw-chin', 'joint-head', 1.0),
    ('jaw-lower-chin', 'joint-head', 1.0),
    ('l-ear-helix', 'joint-head', 1.0),
    ('l-ear-inner', 'joint-head', 1.0),
    ('l-ear-lobe', 'joint-head', 1.0),
    ('l-ear-tubercle', 'joint-head', 1.0),
    ('l-eye-ball', 'joint-l-eye', 1.0),
    ('l-eye-inner-brow-ridge', 'joint-head', 1.0),
    ('l-eye-lower-inner-lid', 'joint-head', 1.0),
    ('l-eye-lower-middle-lid', 'joint-head', 1.0),
    ('l-eye-lower-middle-orbital', 'joint-head', 1.0),
    ('l-eye-lower-outer-lid', 'joint-head', 1.0),
    ('l-eye-lower-outer-orbital', 'joint-head', 1.0),
    ('l-eye-middle-brow-ridge', 'joint-head', 1.0),
    ('l-eye-outer-brow-ridge', 'joint-head', 1.0),
    ('l-eye-upper-inner-lid', 'joint-head', 1.0),
    ('l-eye-upper-inner-orbital', 'joint-head', 1.0),
    ('l-eye-upper-middle-lid', 'joint-head', 1.0),
    ('l-eye-upper-middle-orbital', 'joint-head', 1.0),
    ('l-eye-upper-outer-lid', 'joint-head', 1.0),
    ('l-eye-upper-outer-orbital', 'joint-head', 1.0),
    ('l-foot-ankle', 'joint-l-ankle', 1.0),
    ('l-foot-core', 'joint-l-ankle', 1.0),
    ('l-foot-heel', 'joint-l-ankle', 1.0),
    ('l-foot-nail1', 'joint-l-toe-1-2', 1.0),
    ('l-foot-nail2', 'joint-l-toe-2-3', 1.0),
    ('l-foot-nail3', 'joint-l-toe-3-3', 1.0),
    ('l-foot-nail4', 'joint-l-toe-4-3', 1.0),
    ('l-foot-nail5', 'joint-l-toe-5-3', 1.0),
    ('l-foot-toe-1-1', 'joint-l-toe-1-1', 1.0),
    ('l-foot-toe-1-2', 'joint-l-toe-1-2', 1.0),
    ('l-foot-toe-2-1', 'joint-l-toe-2-1', 1.0),
    ('l-foot-toe-2-2', 'joint-l-toe-2-2', 1.0),
    ('l-foot-toe-2-3', 'joint-l-toe-2-3', 1.0),
    ('l-foot-toe-3-1', 'joint-l-toe-3-1', 1.0),
    ('l-foot-toe-3-2', 'joint-l-toe-3-2', 1.0),
    ('l-foot-toe-3-3', 'joint-l-toe-3-3', 1.0),
    ('l-foot-toe-4-1', 'joint-l-toe-4-1', 1.0),
    ('l-foot-toe-4-2', 'joint-l-toe-4-2', 1.0),
    ('l-foot-toe-4-3', 'joint-l-toe-4-3', 1.0),
    ('l-foot-toe-5-1', 'joint-l-toe-5-1', 1.0),
    ('l-foot-toe-5-2', 'joint-l-toe-5-2', 1.0),
    ('l-foot-toe-5-3', 'joint-l-toe-5-3', 1.0),
    ('l-hand-finger-1-1', 'joint-l-finger-1-1', 1.0),
    ('l-hand-finger-1-2', 'joint-l-finger-1-2', 1.0),
    ('l-hand-finger-1-3', 'joint-l-finger-1-3', 1.0),
    ('l-hand-finger-2-1', 'joint-l-finger-2-1', 1.0),
    ('l-hand-finger-2-2', 'joint-l-finger-2-2', 1.0),
    ('l-hand-finger-2-3', 'joint-l-finger-2-3', 1.0),
    ('l-hand-finger-3-1', 'joint-l-finger-3-1', 1.0),
    ('l-hand-finger-3-2', 'joint-l-finger-3-2', 1.0),
    ('l-hand-finger-3-3', 'joint-l-finger-3-3', 1.0),
    ('l-hand-finger-4-1', 'joint-l-finger-4-1', 1.0),
    ('l-hand-finger-4-2', 'joint-l-finger-4-2', 1.0),
    ('l-hand-finger-4-3', 'joint-l-finger-4-3', 1.0),
    ('l-hand-finger-5-1', 'joint-l-finger-5-1', 1.0),
    ('l-hand-finger-5-2', 'joint-l-finger-5-2', 1.0),
    ('l-hand-finger-5-3', 'joint-l-finger-5-3', 1.0),
    ('l-hand-nail1', 'joint-l-finger-1-3', 1.0),
    ('l-hand-nail2', 'joint-l-finger-2-3', 1.0),
    ('l-hand-nail3', 'joint-l-finger-3-3', 1.0),
    ('l-hand-nail4', 'joint-l-finger-4-3', 1.0),
    ('l-hand-nail5', 'joint-l-finger-5-3', 1.0),
    ('l-hand-palm', 'joint-r-hand', 1.0),
    ('l-head-cheek', 'joint-head', 1.0),
    ('l-head-cheek-arc', 'joint-head', 1.0),
    ('l-head-lower-inner-orbital', 'joint-head', 1.0),
    ('l-head-maxilla', 'joint-head', 1.0),
    ('l-head-outer-chin', 'joint-head', 1.0),
    ('l-head-temple', 'joint-head', 1.0),
    ('l-head-zygoma', 'joint-head', 1.0),
    ('l-hip', '', 1.0),
    ('l-hip-lower-abdomen', '', 1.0),
    ('l-hip-middle-abdomen', '', 1.0),
    ('l-hip-upper-abdomen', '', 1.0),
    ('l-jaw', 'joint-head', 1.0),
    ('l-lowerarm', 'joint-l-elbow', 1.0),
    ('l-lowerleg', 'joint-l-knee', 1.0),
    ('l-lowerleg-calf', 'joint-l-knee', 1.0),
    ('l-mouth-lower', 'joint-mouth', 1.0),
    ('l-mouth-lower-lip', 'joint-mouth', 1.0),
    ('l-mouth-upper-lip', 'joint-mouth', 1.0),
    ('l-nose-nostril', 'joint-head', 1.0),
    ('l-pelvis-gluteus', '', 1.0),
    ('l-teeth-low-cent-incisor', 'joint-head', 1.0),
    ('l-teeth-low-cuspid', 'joint-head', 1.0),
    ('l-teeth-low-first-bicuspid', 'joint-head', 1.0),
    ('l-teeth-low-first-molar', 'joint-head', 1.0),
    ('l-teeth-low-lat-incisor', 'joint-head', 1.0),
    ('l-teeth-low-sec-bicuspid', 'joint-head', 1.0),
    ('l-teeth-low-sec-molar', 'joint-head', 1.0),
    ('l-teeth-low-third-molar', 'joint-head', 1.0),
    ('l-teeth-up-cent-incisor', 'joint-head', 1.0),
    ('l-teeth-up-cuspid', 'joint-head', 1.0),
    ('l-teeth-up-first-bicuspid', 'joint-head', 1.0),
    ('l-teeth-up-first-molar', 'joint-head', 1.0),
    ('l-teeth-up-lat-incisor', 'joint-head', 1.0),
    ('l-teeth-up-sec-bicuspid', 'joint-head', 1.0),
    ('l-teeth-up-sec-molar', 'joint-head', 1.0),
    ('l-teeth-up-third-molar', 'joint-head', 1.0),
    ('l-torso-axilla', '', 1.0),
    ('l-torso-back-scapula', '', 1.0),
    ('l-torso-back-shoulder', '', 1.0),
    ('l-torso-clavicle', '', 1.0),
    ('l-torso-front-shoulder', '', 1.0),
    ('l-torso-inner-pectoralis', '', 1.0),
    ('l-torso-lower-back', '', 1.0),
    ('l-torso-lower-pectoralis', '', 1.0),
    ('l-torso-middle-pectoralis', '', 1.0),
    ('l-torso-nipple', '', 1.0),
    ('l-torso-outer-pectoralis', '', 1.0),
    ('l-torso-ribs', '', 1.0),
    ('l-torso-trapezius', '', 1.0),
    ('l-torso-upper-middle-back', '', 1.0),
    ('l-torso-upper-pectoralis', '', 1.0),
    ('l-torso-upper-shoulder', '', 1.0),
    ('l-upperarm-biceps', 'joint-l-shoulder', 1.0),
    ('l-upperarm-triceps', 'joint-l-shoulder', 1.0),
    ('l-upperleg-frontal-thigh', 'joint-l-upper-leg', 1.0),
    ('l-upperleg-knee', 'joint-l-upper-leg', 1.0),
    ('l-upperleg-thigh-back', 'joint-l-upper-leg', 1.0),
    ('mouth-lower-middle-lip', 'joint-mouth', 1.0),
    ('mouth-upper-middle-lip', 'joint-mouth', 1.0),
    ('neck', 'joint-neck', 1.0),
    ('neck-adam-apple', 'joint-neck', 1.0),
    ('neck-upper', 'joint-neck', 1.0),
    ('nose-bridge', 'joint-head', 1.0),
    ('nose-glabella', 'joint-head', 1.0),
    ('nose-philtrum', 'joint-head', 1.0),
    ('nose-sellion', 'joint-head', 1.0),
    ('nose-tip', 'joint-head', 1.0),
    ('pelvis-genital-area', '', 1.0),
    ('r-ear-helix', 'joint-head', 1.0),
    ('r-ear-inner', 'joint-head', 1.0),
    ('r-ear-lobe', 'joint-head', 1.0),
    ('r-ear-tubercle', 'joint-head', 1.0),
    ('r-eye-ball', 'joint-head', 1.0),
    ('r-eye-inner-brow-ridge', 'joint-head', 1.0),
    ('r-eye-lower-inner-lid', 'joint-head', 1.0),
    ('r-eye-lower-middle-lid', 'joint-head', 1.0),
    ('r-eye-lower-middle-orbital', 'joint-head', 1.0),
    ('r-eye-lower-outer-lid', 'joint-head', 1.0),
    ('r-eye-lower-outer-orbital', 'joint-head', 1.0),
    ('r-eye-middle-brow-ridge', 'joint-head', 1.0),
    ('r-eye-outer-brow-ridge', 'joint-head', 1.0),
    ('r-eye-upper-inner-lid', 'joint-head', 1.0),
    ('r-eye-upper-inner-orbital', 'joint-head', 1.0),
    ('r-eye-upper-middle-lid', 'joint-head', 1.0),
    ('r-eye-upper-middle-orbital', 'joint-head', 1.0),
    ('r-eye-upper-outer-lid', 'joint-head', 1.0),
    ('r-eye-upper-outer-orbital', 'joint-head', 1.0),
    ('r-foot-ankle', 'joint-r-ankle', 1.0),
    ('r-foot-core', 'joint-r-ankle', 1.0),
    ('r-foot-heel', 'joint-r-ankle', 1.0),
    ('r-foot-nail1', 'joint-r-toe-1-2', 1.0),
    ('r-foot-nail2', 'joint-r-toe-2-3', 1.0),
    ('r-foot-nail3', 'joint-r-toe-3-3', 1.0),
    ('r-foot-nail4', 'joint-r-toe-4-3', 1.0),
    ('r-foot-nail5', 'joint-r-toe-5-3', 1.0),
    ('r-foot-toe-1-1', 'joint-r-toe-1-1', 1.0),
    ('r-foot-toe-1-2', 'joint-r-toe-1-2', 1.0),
    ('r-foot-toe-2-1', 'joint-r-toe-2-1', 1.0),
    ('r-foot-toe-2-2', 'joint-r-toe-2-2', 1.0),
    ('r-foot-toe-2-3', 'joint-r-toe-2-3', 1.0),
    ('r-foot-toe-3-1', 'joint-r-toe-3-1', 1.0),
    ('r-foot-toe-3-2', 'joint-r-toe-3-2', 1.0),
    ('r-foot-toe-3-3', 'joint-r-toe-3-3', 1.0),
    ('r-foot-toe-4-1', 'joint-r-toe-4-1', 1.0),
    ('r-foot-toe-4-2', 'joint-r-toe-4-2', 1.0),
    ('r-foot-toe-4-3', 'joint-r-toe-4-3', 1.0),
    ('r-foot-toe-5-1', 'joint-r-toe-5-1', 1.0),
    ('r-foot-toe-5-2', 'joint-r-toe-5-2', 1.0),
    ('r-foot-toe-5-3', 'joint-r-toe-5-3', 1.0),
    ('r-hand-finger-1-1', 'joint-r-finger-1-1', 1.0),
    ('r-hand-finger-1-2', 'joint-r-finger-1-2', 1.0),
    ('r-hand-finger-1-3', 'joint-r-finger-1-3', 1.0),
    ('r-hand-finger-2-1', 'joint-r-finger-2-1', 1.0),
    ('r-hand-finger-2-2', 'joint-r-finger-2-2', 1.0),
    ('r-hand-finger-2-3', 'joint-r-finger-2-3', 1.0),
    ('r-hand-finger-3-1', 'joint-r-finger-3-1', 1.0),
    ('r-hand-finger-3-2', 'joint-r-finger-3-2', 1.0),
    ('r-hand-finger-3-3', 'joint-r-finger-3-3', 1.0),
    ('r-hand-finger-4-1', 'joint-r-finger-4-1', 1.0),
    ('r-hand-finger-4-2', 'joint-r-finger-4-2', 1.0),
    ('r-hand-finger-4-3', 'joint-r-finger-4-3', 1.0),
    ('r-hand-finger-5-1', 'joint-r-finger-5-1', 1.0),
    ('r-hand-finger-5-2', 'joint-r-finger-5-2', 1.0),
    ('r-hand-finger-5-3', 'joint-r-finger-5-3', 1.0),
    ('r-hand-nail1', 'joint-r-finger-1-3', 1.0),
    ('r-hand-nail2', 'joint-r-finger-2-3', 1.0),
    ('r-hand-nail3', 'joint-r-finger-3-3', 1.0),
    ('r-hand-nail4', 'joint-r-finger-4-3', 1.0),
    ('r-hand-nail5', 'joint-r-finger-5-3', 1.0),
    ('r-hand-palm', 'joint-r-hand', 1.0),
    ('r-head-cheek', 'joint-head', 1.0),
    ('r-head-cheek-arc', 'joint-head', 1.0),
    ('r-head-lower-inner-orbital', '', 1.0),
    ('r-head-maxilla', 'joint-head', 1.0),
    ('r-head-outer-chin', 'joint-head', 1.0),
    ('r-head-temple', 'joint-head', 1.0),
    ('r-head-zygoma', 'joint-head', 1.0),
    ('r-hip', '', 1.0),
    ('r-hip-lower-abdomen', '', 1.0),
    ('r-hip-middle-abdomen', '', 1.0),
    ('r-hip-upper-abdomen', '', 1.0),
    ('r-jaw', 'joint-head', 1.0),
    ('r-lowerarm', 'joint-r-elbow', 1.0),
    ('r-lowerleg', 'joint-l-knee', 1.0),
    ('r-lowerleg-calf', 'joint-l-knee', 1.0),
    ('r-mouth-lower', 'joint-mouth', 1.0),
    ('r-mouth-lower-lip', 'joint-mouth', 1.0),
    ('r-mouth-upper-lip', 'joint-mouth', 1.0),
    ('r-nose-nostril', 'joint-head', 1.0),
    ('r-pelvis-gluteus', '', 1.0),
    ('r-teeth-low-cent-incisor', 'joint-head', 1.0),
    ('r-teeth-low-cuspid', 'joint-head', 1.0),
    ('r-teeth-low-first-bicuspid', 'joint-head', 1.0),
    ('r-teeth-low-first-molar', 'joint-head', 1.0),
    ('r-teeth-low-lat-incisor', 'joint-head', 1.0),
    ('r-teeth-low-sec-bicuspid', 'joint-head', 1.0),
    ('r-teeth-low-sec-molar', 'joint-head', 1.0),
    ('r-teeth-low-third-molar', 'joint-head', 1.0),
    ('r-teeth-up-cent-incisor', 'joint-head', 1.0),
    ('r-teeth-up-cuspid', 'joint-head', 1.0),
    ('r-teeth-up-first-bicuspid', 'joint-head', 1.0),
    ('r-teeth-up-first-molar', 'joint-head', 1.0),
    ('r-teeth-up-lat-incisor', 'joint-head', 1.0),
    ('r-teeth-up-sec-bicuspid', 'joint-head', 1.0),
    ('r-teeth-up-sec-molar', 'joint-head', 1.0),
    ('r-teeth-up-third-molar', 'joint-head', 1.0),
    ('r-torso-axilla', '', 1.0),
    ('r-torso-back-scapula', '', 1.0),
    ('r-torso-back-shoulder', '', 1.0),
    ('r-torso-clavicle', '', 1.0),
    ('r-torso-front-shoulder', '', 1.0),
    ('r-torso-inner-pectoralis', '', 1.0),
    ('r-torso-lower-back', '', 1.0),
    ('r-torso-lower-pectoralis', '', 1.0),
    ('r-torso-middle-pectoralis', '', 1.0),
    ('r-torso-nipple', '', 1.0),
    ('r-torso-outer-pectoralis', '', 1.0),
    ('r-torso-ribs', '', 1.0),
    ('r-torso-trapezius', '', 1.0),
    ('r-torso-upper-middle-back', '', 1.0),
    ('r-torso-upper-pectoralis', '', 1.0),
    ('r-torso-upper-shoulder', '', 1.0),
    ('r-upperarm-biceps', 'joint-r-shoulder', 1.0),
    ('r-upperarm-triceps', 'joint-r-shoulder', 1.0),
    ('r-upperleg-frontal-thigh', 'joint-l-upper-leg', 1.0),
    ('r-upperleg-knee', 'joint-l-upper-leg', 1.0),
    ('r-upperleg-thigh-back', 'joint-l-upper-leg', 1.0),
    ('torso-spine', '', 1.0),
    ('l-eye-cornea', 'joint-head', 1.0),
    ('r-eye-cornea', 'joint-head', 1.0),
    ('r-eye-eyebrown', 'joint-head', 1.0),
    ('l-eye-eyebrown', 'joint-head', 1.0),
    ('l-eye-lower-lash', 'joint-head', 1.0),
    ('l-eye-upper-lash', 'joint-head', 1.0),
    ('r-eye-lower-lash', 'joint-head', 1.0),
    ('r-eye-upper-lash', 'joint-head', 1.0))

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

    skeleton = Skeleton()
    skeleton.update(obj)

    f = open(filename, 'w')
    f.write('MD5Version 10\n')
    f.write('commandline ""\n\n')
    f.write('numJoints %d\n' % (skeleton.joints+1)) # Amount of joints + the hardcoded origin below
    f.write('numMeshes %d\n\n' % (1)) # TODO: 2 in case of hair
    f.write('joints {\n')
    f.write('\t"%s" %d ( %f %f %f ) ( %f %f %f )\n' % ('origin', -1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    writeJoint(f, skeleton.root)
    f.write('}\n\n')
    f.write('mesh {\n')
    f.write('\tshader "%s"\n' % (basename(obj.texture))) # TODO: create the shader file
    f.write('\n\tnumverts %d\n' % (len(obj.verts)))
    for vert in obj.verts:
        if obj.uvValues:
            face = vert.sharedFaces[0]
            u, v = obj.uvValues[face.uv[face.verts.index(vert)]]
        else:
            u, v = 0, 0
        # vert [vertIndex] ( [texU] [texV] ) [weightIndex] [weightElem]
        f.write('\tvert %d ( %f %f ) %d %d\n' % (vert.idx, u, 1.0-v, vert.idx, 1))
    f.write('\n\tnumtris %d\n' % (len(obj.faces) * 2))
    for face in obj.faces:
        # tri [triIndex] [vertIndex1] [vertIndex2] [vertIndex3]
        f.write('\ttri %d %d %d %d\n' % (face.idx*2, face.verts[2].idx, face.verts[1].idx, face.verts[0].idx))
        f.write('\ttri %d %d %d %d\n' % (face.idx*2+1, face.verts[0].idx, face.verts[3].idx, face.verts[2].idx))
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
