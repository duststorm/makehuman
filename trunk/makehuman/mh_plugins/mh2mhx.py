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

import module3d, aljabr, mh, files3d, mh2bvh, mhxbones, mhxbones_rigify
import os

splitLeftRight = True

#
#	exportMhx(obj, filename):
#
def exportMhx(obj, filename):	
	print("Writing MHX file " + filename )
	fp = open(filename, 'w')
	exportMhx_249(obj, fp)
	#exportMhx_250(obj, fp)
	fp.close()
	print("MHX file %s written" % filename)
	return

#
#	exportMhx_249(obj,fp):
#

def exportMhx_249(obj, fp):
	fp.write(
"# MakeHuman exported MHX\n" +
"# www.makehuman.org\n" +
"MHX 0 5 ;\n")

	fp.write("if Blender24\n")
	copyMaterialFile("data/3dobjs/materials24.mhx", fp)	
	fp.write("end if\n")
	
	fp.write("if Blender25\n")
	copyMaterialFile("data/3dobjs/materials25.mhx", fp)	
	fp.write("end if\n")
	
	exportArmature(obj, fp)

	tmpl = open("data/3dobjs/meshes24.mhx")
	if tmpl:
		copyMeshFile(obj, tmpl, fp)	
		tmpl.close()
	return

#
#	exportRawMhx(obj, fp)
#

def exportRawMhx(obj, fp):
	exportArmature(obj, fp)
	fp.write(
"if useMesh \n" +
"mesh Human Human \n")
	exportRawData(obj, fp)
	fp.write(
"end mesh\n" +
"\nobject Human Mesh Human \n" +
"\tlayers 1 0 ;\n" +
"end object\n" +
"end useMesh\n")
	return

#
#	exportMhx_250(obj,fp):
#

def exportMhx_250(obj,fp):
	fp.write(
"# MakeHuman exported MHX\n" +
"# www.makehuman.org\n" +
"MHX 0 5 ;\n")

	copyMaterialFile("data/3dobjs/materials25.mhx", fp)	
	mhxbones_rigify.writeBones(obj, fp)

	fp.write(
"if useMesh \n" +
"mesh Human Human \n")
	exportRawData(obj, fp)

	tmpl = open("data/3dobjs/meshes25.mhx")
	if tmpl:
		copyMeshFile(obj, tmpl, fp)	
		tmpl.close()
	return

#
#	copyMaterialFile(infile, fp):
#

def copyMaterialFile(infile, fp):
	tmpl = open(infile, "rU")
	for line in tmpl:
		lineSplit= line.split()
		if len(lineSplit) == 0:
			fp.write(line)
		elif lineSplit[0] == 'filename':
			path1 = os.path.expanduser("./data/textures/")
			(path, filename) = os.path.split(lineSplit[1])
			file1 = os.path.realpath(path1+filename)
			fp.write("  filename %s ;\n" % file1)
		else:
			fp.write(line)
	tmpl.close()

#
#	copyMeshFile(obj, tmpl, fp):
#

def copyMeshFile(obj, tmpl, fp):
	inZone = False
	skip = False
	mainMesh = False
	
	for line in tmpl:
		lineSplit= line.split()
		skipOne = False

		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == 'end':
			if lineSplit[1] == 'object' and mainMesh:
				fp.write(line)
				skipOne = True
				fp.write("end if\n")
				mainMesh = False
			elif lineSplit[1] == 'mesh' and mainMesh:
				shpfp = open("data/3dobjs/shapekeys24.mhx", "rU")
				exportShapeKeys(obj, shpfp, fp)
				shpfp.close()
				writeIpo(fp)
				fp.write(line)
				skipOne = True
				fp.write("end if\n")
				mainMesh = False
				inZone = False
				skip = False
		elif lineSplit[0] == 'mesh' and lineSplit[1] == 'Human':
			inZone = True
			mainMesh = True
			fp.write("if useMesh\n")
		elif lineSplit[0] == 'object' and lineSplit[1] == 'Human':
			mainMesh = True
			fp.write("if useMesh\n")
		elif lineSplit[0] == 'v' and inZone:
			if not skip:
				exportRawData(obj, fp)
				skip = True
		elif lineSplit[0] == 'f' and skip:
			skip = False
			skipOne = True

		if not (skip or skipOne):
			fp.write(line)
	
	return

#
#	exportRawData(obj, fp):	
#

def exportRawData(obj, fp):	
	# Ugly klugdy fix of extra vert
	x1 = aljabr.vadd(obj.verts[11137].co, obj.verts[11140].co)
	x2 = aljabr.vadd(obj.verts[11162].co, obj.verts[11178].co)
	x = aljabr.vadd(x1,x2)
	obj.verts[14637].co = aljabr.vmul(x, 0.25)
	# end ugly kludgy

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

#
#	exportArmature(obj, fp):
#

def exportArmature(obj, fp):
	mhxbones.writeJoints(obj, fp)
	fp.write("\narmature HumanRig HumanRig\n")


	mhxbones.writeBones(obj, fp)
	fp.write(
"\tlayerMask 0x101 ;\n" +
"\tautoIK false ;\n" +
"\tdelayDeform false ;\n" +
"\tdrawAxes false ;\n" +
"\tdrawNames false ;\n" +
"\tenvelopes false ;\n" +
"\tmirrorEdit true ;\n" +
"\trestPosition false ;\n" +
"\tvertexGroups true ;\n" +
"end armature\n")

	fp.write("\npose HumanRig\n")
	mhxbones.writePose(obj, fp)
	fp.write("end pose\n")
		
	fp.write(
"\nobject HumanRig Armature HumanRig \n" +
"\tlayers 1 0 ;\n" +
"\txRay true ;\n" +
"end object\n")

	return exportArmature
	
#
#	exportShapeKeys(obj, tmpl, fp):
#

def exportShapeKeys(obj, tmpl, fp):
	global splitLeftRight
	if tmpl == None:
		return
	lineNo = 0	
	store = False
	for line in tmpl:
		lineNo += 1
		lineSplit= line.split()
		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == 'end' and lineSplit[1] == 'shapekey' and store:
			if leftRightKey[shapekey] and splitLeftRight:
				writeShapeKey(fp, shapekey+"_L", shapeVerts, "Left", sliderMin, sliderMax)
				writeShapeKey(fp, shapekey+"_R", shapeVerts, "Right", sliderMin, sliderMax)
			else:
				writeShapeKey(fp, shapekey, shapeVerts, "None", sliderMin, sliderMax)
		elif lineSplit[0] == 'shapekey':
			shapekey = lineSplit[1]
			sliderMin = lineSplit[2]
			sliderMax = lineSplit[3]
			shapeVerts = []
			if shapekey[5:] == 'Bend' or shapekey[5:] == 'Shou':
				store = False
			else:
				store = True
		elif lineSplit[0] == 'sv' and store:
			shapeVerts.append(line)
	return

#
#	leftRightKey - True if shapekey comes in two parts
#

leftRightKey = {
	"Basis" : False,
	"BendElbowForward" : True,
	"BendHeadForward" : False,
	"BendKneeBack" : True,
	"BendLegBack" : True,
	"BendLegForward" : True,
	"BrowsDown" : True,
	"BrowsMidDown" : False,
	"BrowsMidUp" : False,
	"BrowsOutUp" : True,
	"BrowsSqueeze" : False,
	"CheekUp" : True,
	"Frown" : True,
	"UpLidDown" : True,
	"LoLidUp" : True,
	"Narrow" : True,
	"ShoulderDown" : True,
	"Smile" : True,
	"Sneer" : True,
	"Squint" : True,
	"TongueOut" : False,
	"ToungeUp" : False,
	"ToungeLeft" : False,
	"ToungeRight" : False,
	"UpLipUp" : True,
	"LoLipDown" : True,
	"MouthOpen" : False,
	"UpLipDown" : True,
	"LoLipUp" : True,
}

#
#	writeShapeKey(fp, shapekey, shapeVerts, vgroup, sliderMin, sliderMax):
#

def writeShapeKey(fp, shapekey, shapeVerts, vgroup, sliderMin, sliderMax):
	fp.write("shapekey %s %s %s %s\n" % (shapekey, sliderMin, sliderMax, vgroup))
	for line in shapeVerts:
		fp.write(line)
	fp.write("end shapekey\n")

#
#	writeIcu(fp, shape, expr):
#

def writeIcu(fp, shape, expr):
	fp.write(
"\ticu %s 0 1\n" +
"\t\tdriver 2 ;\n" +
"\t\tdriverObject _object['Human'] ;\n" +
"\t\tdriverChannel 1 ;\n" +
"\t\tdriverExpression '%s' ;\n" +
"\tend icu\n" % (shape, expr))

def writeIpo(fp):
	global splitLeftRight

	mhxFile = "data/3dobjs/mhxipos.mhx"
	try:
		print("Trying to open "+mhxFile)
		tmpl = open(mhxFile, "r")
	except:
		print("Failed to open "+mhxFile)
		tmpl = None

	if tmpl and splitLeftRight:
		for line in tmpl:
			fp.write(line)
	else:
		fp.write("ipo Key KeyIpo\n")
		for (shape, lr) in leftRightKey.items():
			if shape == 'Basis':
				pass
			elif lr and splitLeftRight:
				writeIcu(fp, shape+'_L', 'p.ctrl'+shape+'_L()')
				writeIcu(fp, shape+'_R', 'p.ctrl'+shape+'_R()')
			else:
				writeIcu(fp, shape, 'p.ctrl'+shape+'()')
		fp.write("end ipo\n")
	
	if tmpl:
		print(mhxFile+" closed")
		tmpl.close()
	return