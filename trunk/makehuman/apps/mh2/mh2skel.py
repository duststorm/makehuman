#!/usr/bin/python
# -*- coding: utf-8 -*-

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