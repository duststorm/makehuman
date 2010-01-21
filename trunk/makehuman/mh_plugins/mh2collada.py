""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
MakeHuman to Collada (MakeHuman eXchange format) exporter. Collada files can be loaded into
Blender by collada_import.py.

TO DO

"""

import module3d, aljabr, mh, files3d, mh2bvh, mhxbones
import os

#
#	exportCollada(obj, filename):
#

def exportCollada(obj, filename):	
	daeFile = "data/3dobjs/daebase.dae"
	try:
		tmpl = open(daeFile, "r")
	except:
		return
	print("Writing Collada file %s" % filename)
	print(daeFile+" opened")
	fp = open(filename, 'w')
	exportFromDaeTemplate(obj, tmpl, fp)
	print(daeFile+" closed")
	tmpl.close()
	fp.close()
	print("Collada file %s written" % filename)
	return
	


#
#	exportFromDaeTemplate(obj, tmpl, fp):
#
	
def exportFromDaeTemplate(obj, tmpl, fp):
	doBones = False
	lineNo = 0
	mhxbones.setupBones(obj)
	
	for line in tmpl:
		lineNo += 1
		lineSplit= line.split()
		skipOne = False

		if len(lineSplit) == 0:
			fp.write(line)
		elif lineSplit[0] == '***':
			if lineSplit[1] == 'Human-mesh-positions':
				for v in obj.verts:
					fp.write("%f %f %f " %(v.co[0], v.co[1], v.co[2]))
				fp.write("\n")
			elif lineSplit[1] == 'Human-mesh-normals':
				for v in obj.verts:
					fp.write("%f %f %f " %(v.no[0], v.no[1], v.no[2]))
				fp.write("\n")
			elif lineSplit[1] == 'Begin_bones':
				doBones = True
			elif lineSplit[1] == 'End_bones':
				doBones = False
		elif doBones and lineSplit[0] == '<node': 
			words = lineSplit[1].split('"')
			word = words[1]
			if word[:9] == 'HumanRig_':
				bone = words[1][9:]	# eliminate HumanRig_
				print("Node "+bone)
			fp.write(line)
		elif doBones and lineSplit[0] == '<translate': 
			(x,y,z) = mhxbones.boneHead[bone]
			fp.write('\t\t\t<translate sid="location">%g %g %g</translate>\n' % (x,y,z))
		else:
			fp.write(line)
	
	return
