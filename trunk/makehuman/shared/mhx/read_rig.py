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
#	setupRigJoint (words, obj, locations):
#
def setupRigJoint (words, obj, locations):
	key = words[0]
	typ = words[1]
	if typ == 'joint':
		loc = mhxbones.calcJointPos(obj, words[2])
		locations[key] = loc
	elif typ == 'vertex':
		v = int(words[2])
		locations[key] = obj.verts[v].co
	elif typ == 'position':
		x = locations[words[2]]
		y = locations[words[3]]
		z = locations[words[4]]
		locations[key] = [x[0],y[1],z[2]]
	elif typ == 'line':
		k1 = float(words[2])
		k2 = float(words[4])
		locations[key] = vadd(vmul(locations[words[3]], k1), vmul(locations[words[5]], k2))
	elif typ == 'offset':
		x = float(words[3])
		y = float(words[4])
		z = float(words[5])
		locations[key] = vadd(locations[words[2]], [x,y,z])
	else:
		raise NameError("Unknown %s" % typ)


def readRigFile(fileName, obj):
	fp= open(fileName, "rU")

	doLocations = 1
	doBones = 2
	doWeights = 3
	status = 0

	locations = {}
	armature = []
	weights = {}

	for line in fp: 
		words = line.split()
		if len(words) == 0:
			pass
		elif words[0] == '#':
			if words[1] == 'locations':
				status = doLocations
			elif words[1] == 'bones':
				status = doBones
			elif words[1] == 'weights':
				status = doWeights
				wts = []
				weights[words[2]] = wts
		elif status == doWeights:
			wts.append((int(words[0]), float(words[1])))
		elif status == doLocations:
			setupRigJoint (words, obj, locations)
		elif status == doBones:
			bone = words[0]
			head = locations[words[1]]
			tail = locations[words[2]]
			roll = float(words[3])
			parent = words[4]
			options = {}
			for word in words[5:]:
				if word[0] == '-':
					values = []
					options[word] = values
				else:
					values.append(word)
			armature.append((bone, head, tail, roll, parent, options))
		else:
			raise NameError("Unknown status %d" % status)

	fp.close()
	return (locations, armature, weights)

