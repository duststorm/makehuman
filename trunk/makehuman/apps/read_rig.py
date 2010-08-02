#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyright(c):**	  MakeHuman Team 2001-2010

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
MakeHuman to Collada (MakeHuman eXchange format) exporter. Collada files can be loaded into
Blender by collada_import.py.

TO DO

"""

import aljabr
import mhxbones
from aljabr import *

#
#	setupRigJoint (lineSplit, obj, locations):
#
def setupRigJoint (lineSplit, obj, locations):
	key = lineSplit[0]
	typ = lineSplit[1]
	if typ == 'joint':
		loc = mhxbones.calcJointPos(obj, lineSplit[2])
		locations[key] = loc
	elif typ == 'vertex':
		v = int(lineSplit[2])
		locations[key] = obj.verts[v].co
	elif typ == 'position':
		x = locations[lineSplit[2]]
		y = locations[lineSplit[3]]
		z = locations[lineSplit[4]]
		locations[key] = [x[0],y[1],z[2]]
	elif typ == 'line':
		k1 = float(lineSplit[2])
		k2 = float(lineSplit[4])
		locations[key] = vadd(vmul(locations[lineSplit[3]], k1), vmul(locations[lineSplit[5]], k2))
	elif typ == 'offset':
		x = float(lineSplit[3])
		y = float(lineSplit[4])
		z = float(lineSplit[5])
		locations[key] = vadd(locations[lineSplit[2]], [x,y,z])
	else:
		raise NameError("Unknown %s" % typ)


def readRigFile(fileName, obj):
	fp= open(fileName, "rU")
	inLocations = False
	inBones = False
	inWeights = False
	locations = {}
	armature = []
	weights = {}
	for line in fp: 
		lineSplit = line.split()
		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == '#':
			if lineSplit[1] == 'locations':
				inLocations = True
			elif lineSplit[1] == 'bones':
				inLocations = False
				inBones = True
			elif lineSplit[1] == 'weights':
				inBones = False
				inWeights = True
				wts = []
				weights[lineSplit[2]] = wts
		elif inWeights:
			wts.append((int(lineSplit[0]), float(lineSplit[1])))
		elif inLocations:
			setupRigJoint (lineSplit, obj, locations)
		elif inBones:
			bone = lineSplit[0]
			head = locations[lineSplit[1]]
			tail = locations[lineSplit[2]]
			roll = float(lineSplit[3])
			parent = lineSplit[4]
			armature.append((bone, head, tail, roll, parent))

	fp.close()
	return (locations, armature, weights)

