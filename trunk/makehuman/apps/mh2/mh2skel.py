#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

from os.path import basename
from skeleton import Skeleton

def exportSkel(obj, filename):

    skeleton = Skeleton()
    skeleton.update(obj)

    f = open(filename, 'w')
    
    writeJoint(f, skeleton.root)
    
    f.close()

def writeJoint(f, joint):

    if joint.parent:
        parentIndex = joint.parent.index
    else:
        parentIndex = -1

    f.write('%d %f %f %f %d\n' % (joint.index, joint.position[0], joint.position[1], joint.position[2], parentIndex))

    for joint in joint.children:
        writeJoint(f, joint)
