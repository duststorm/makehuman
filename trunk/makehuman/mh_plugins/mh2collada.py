#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyright(c):**	  MakeHuman Team 2001-2009

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
MakeHuman to Collada (MakeHuman eXchange format) exporter. Collada files can be loaded into
Blender by collada_import.py.

TO DO

"""

import module3d
import aljabr
import mh
import files3d
import mh2bvh
import mhxbones
import os

#
# ....exportCollada(obj, filename):
#


def exportCollada(obj, filename):
	daeFile = 'data/templates/base.dae'
	try:
		tmpl = open(daeFile, 'r')
	except:
		return
	print 'Writing Collada file %s' % filename
	print daeFile + ' opened'
	fp = open(filename, 'w')
	exportFromDaeTemplate(obj, tmpl, fp)
	print daeFile + ' closed'
	tmpl.close()
	fp.close()
	print 'Collada file %s written' % filename
	return


#
# ....exportFromDaeTemplate(obj, tmpl, fp):
#
#	<node layer="L1" sid="Root" type="JOINT" id="Root" name="Root">
#	<node sid="Clavicle_R" type="JOINT" id="Clavicle_R" name="Clavicle_R">
#	<translate sid="translate">-0.27260 -0.89248 1.11365</translate>
#

def exportFromDaeTemplate(obj, tmpl, fp):
	doBones = False
	lineNo = 0
	mhxbones.setupBones(obj)

	for line in tmpl:
		lineNo += 1
		lineSplit = line.split()
		skipOne = False

		if len(lineSplit) == 0:
			fp.write(line)
		elif lineSplit[0] == '***':
			if lineSplit[1] == 'Position':
				for v in obj.verts:
					fp.write('%.6g %.6g %.6g ' % (v.co[0], v.co[1], v.co[2]))
				fp.write('\n')
			elif lineSplit[1] == 'Normals':
				for v in obj.verts:
					fp.write('%.6g %.6g %.6g ' % (v.no[0], v.no[1], v.no[2]))
				fp.write('\n')
			elif lineSplit[1] == 'BeginJoints':
				doBones = True
			elif lineSplit[1] == 'EndJoints':
				doBones = False
			else:
				raise NameError("Error in base.dae: "+line)
		elif doBones and lineSplit[0] == '<node':
			words = lineSplit[1].split('"')
			if words[0] == 'layer=':
				words = lineSplit[2].split('"')
			if words[0] != 'sid=':
				raise NameError("Node error in base.dae: "+line)
			word = words[1]
			bone = word
			print("Node "+bone)
			fp.write(line)
		elif doBones and lineSplit[0] == '<translate':
			(x, y, z) = mhxbones.boneHead[bone]
			fp.write('\t\t\t<translate sid="translate">%.6g %.6g %.6g</translate>\n' % (x, y, z))
		else:
			fp.write(line)

	return


