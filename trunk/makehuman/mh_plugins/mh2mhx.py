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
	print("Writing MHX file")
	fp = open(filename, 'w')
	mhxFile = "data/3dobjs/mhxbase.mhx"
	try:
		print("Trying to open "+mhxFile)
		tmpl = open(mhxFile, "r")
	except:
		print("Failed to open "+mhxFile)
		tmpl = None
	if tmpl:
		exportFromMhxTemplate(obj, tmpl, fp)
		print(mhxFile+" closed")
	else:
		exportRawMesh(obj, fp)
		exportArmature(obj, fp)
	fp.close()
	print("MHX file written")
	return
	


def exportRawMesh(obj, fp):
	fp.write(\
"# MakeHuman exported MHX\n" \
"# www.makehuman.org\n" \
"MHX 0 3 ;\n\n")

	fp.write(\
"if useMesh \n\
mesh Human Human \n")
	
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
	
	fp.write(\
"end mesh\n\
\nobject Human Mesh Human \n\
\tlayers 1 0 ;\n\
end object\n\
end useMesh\n")
	return

#
#	exportArmature(obj, fp):
#

def exportArmature(obj, fp):
	mhxbones.writeJoints(obj, fp)
	fp.write("\narmature HumanRig HumanRig\n")

	mhxbones.writeBones(obj, fp)
	fp.write(\
"\tlayerMask 0x101 ;\n\
\tautoIK false ;\n\
\tdelayDeform false ;\n\
\tdrawAxes false ;\n\
\tdrawNames false ;\n\
\tenvelopes false ;\n\
\tghost false ;\n\
\tghostStep 0 ;\n\
\tmirrorEdit true ;\n\
\trestPosition false ;\n\
\tvertexGroups true ;\n\
end armature\n")

	fp.write("\npose HumanRig\n")
	mhxbones.writePose(obj, fp)
	fp.write("end pose\n")
		
	fp.write("\n\
object HumanRig Armature HumanRig \n\
\tlayers 1 0 ;\n\
\txRay true ;\n\
end object\n")

	mhxbones.writeEmpties(fp)

	return exportArmature


#
#	exportFromMhxTemplate(obj, tmpl, fp):
#

def exportFromMhxTemplate(obj, tmpl, fp):

	inZone = False
	skip = False
	lineNo = 0
	mainMesh = False
	
	for line in tmpl:
		lineNo += 1
		lineSplit= line.split()
		skipOne = False

		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == 'end':
			if lineSplit[1] == 'object' and mainMesh:
				fp.write("end if\n")
				mainMesh = False
			elif lineSplit[1] == 'mesh' and mainMesh:
				fp.write("end if\n")
				mainMesh = False
				inZone = False
				skip = False
			elif lineSplit[1] == 'armature' or lineSplit[1] == 'pose':
				mainMesh = False
				inZone = False
				skip = False
				skipOne = True
		elif lineSplit[0] == 'mesh' and lineSplit[1] == 'Human':
			inZone = True
			mainMesh = True
			exportArmature(obj, fp)
			fp.write("if useMesh\n")
		elif lineSplit[0] == 'object' and lineSplit[1] == 'Human':
			mainMesh = True
			fp.write("if useMesh\n")
		elif lineSplit[0] == 'armature' and lineSplit[2] == 'HumanRig':
			skip = True
		elif lineSplit[0] == 'pose' and lineSplit[1] == 'HumanRig':
			skip = True
		elif lineSplit[0] == 'v' and inZone:
			if not skip:
				for v in obj.verts:
					fp.write("v %f %f %f ;\n" %(v.co[0], v.co[1], v.co[2]))
				skip = True
		elif lineSplit[0] == 'vt' and skip:
			inZone = False
			skip = False

		if not (skip or skipOne):
			fp.write(line)
	
	return