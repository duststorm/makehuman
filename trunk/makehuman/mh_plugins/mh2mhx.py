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
MakeHuman to MHX (MakeHuman eXchange format) exporter. MHX files can be loaded into
Blender by mhx_import.py.

TO DO

"""

import module3d, aljabr, files3d, mh2bvh, mhxbones
import os


#
#	exportMhx(obj, filename):
#

def exportMhx(obj, filename):	
	print "Writing MHX file"
	fp = open(filename, 'w')
	mhxFile = "data/3dobjs/mhxbase.mhx"
	try:
		print "Trying to open "+mhxFile
		tmpl = open(mhxFile, "r")
	except:
		print "Failed to open "+mhxFile
		tmpl = None
	if tmpl:
		exportFromMhxTemplate(obj, tmpl, fp)
	else:
		exportRaw(obj, fp)

	


def exportRaw(obj, fp):
	fp.write(\
"# MakeHuman exported MHX\n" \
"# www.makehuman.org\n" \
"MHX 0 2 ;\n\n" \
"mesh Human Human \n")
	
	for v in obj.verts:
		fp.write("v %f %f %f ;\n" %(v.co[0], v.co[1], v.co[2]))
		
	for uv in obj.uvValues:
		fp.write("vt %f %f ;\n" %(uv[0], uv[1]))

	faces = files3d.loadFacesIndices("data/3dobjs/base.obj")
	for f in faces:
		fp.write("f")
		for v in f:
			fp.write(" %i/%i " %(v[0], v[1]))
		fp.write(";\n")
	
	fp.write("end mesh\n")

	mhxbones.writeJoints(fp, obj)
	fp.write("\narmature HumanRig HumanRig\n")
	mhxbones.writeBones(fp, obj)
	fp.write("end armature\n")

	fp.write("\npose HumanRig\n")
	mhxbones.writePose(fp, obj)
	fp.write("end pose\n")
		
	fp.write(\
"\nobject HumanRig Armature HumanRig \n "\
"  layers 1 0 ;\n" \
"end object\n\n"\
"object Human Mesh Human \n"\
"  layers 1 0 ;\n"\
"end object\n")

	fp.close()
	print "MHX file written"

#
#	exportFromMhxTemplate(obj, tmpl, fp):
#

def exportFromMhxTemplate(obj, tmpl, fp):

	inZone = False
	noSkip = True
	lineNo = 0
	
	for line in tmpl:
		lineNo += 1
		lineSplit= line.split()

		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == 'end':
			if lineSplit[1] == 'mesh' or \
			   lineSplit[1] == 'armature' or \
			   lineSplit[1] == 'pose':
				inZone = False
				noSkip = True
		elif lineSplit[0] == 'mesh' and lineSplit[1] == 'Human':
			inZone = True
		elif lineSplit[0] == 'armature' and lineSplit[2] == 'HumanRig':
			inZone = True
			noSkip = False
			mhxbones.writeJoints(fp, obj)
			fp.write("\narmature HumanRig HumanRig\n")
			mhxbones.writeBones(fp, obj)
		elif lineSplit[0] == 'pose' and lineSplit[1] == 'HumanRig':
			inZone = True
			noSkip = False
			fp.write("\npose HumanRig\n")
			mhxbones.writePose(fp, obj)
		elif lineSplit[0] == 'v' and inZone:
			if noSkip:
				for v in obj.verts:
					fp.write("v %f %f %f ;\n" %(v.co[0], v.co[1], v.co[2]))
				noSkip = False
		elif lineSplit[0] == 'vt':
			inZone = False
			noSkip = True
		else:
			pass

		if noSkip:			
			fp.write(line)
	return



