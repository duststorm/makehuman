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

VertWeightLowerThreshold = 0.05

#
#	Texture channels
#

T_COLOR = 0x01
T_REF	= 0x02
T_ALPHA	= 0x04
T_MIX	= 0x08

#
#	exportMhx(obj, filename):
#

def exportMhx(obj, filename):	
	print "Writing MHX file"
	fp = open(filename, 'w')
	fp.write("# MakeHuman exported MHX\n")
	fp.write("# www.makehuman.org\n")
	fp.write("MHX 0 1\n")

	data = loadFromMhxBase("data/3dobjs/mhxbase.mhx")
	if data:
		mhxWriteDispObs(fp, data)

	fp.write("object %s %d %d add\n" % ("Human", 0x001, 0x000))

	fp.write("material Human\n")
	fp.write("color 0.8 0.8 0.8\n")
	fp.write("specular 1.0 1.0 1.0\n")
	fp.write("alpha 0\n")
	fp.write("texture HumanColor texture.tif %d\n" % (T_COLOR))
	fp.write("texture HumanMix texture_mix.tif %d\n" % (T_MIX))
	fp.write("texture HumanOpacity texture_opacity.tif %d\n" % (T_ALPHA))
	fp.write("texture HumanRef texture_ref.tif %d\n" % (T_REF))

	fp.write("mesh %s\n" % ("Human"))
	for v in obj.verts:
		fp.write("v %f %f %f\n" %(v.co[0], v.co[1], v.co[2]))
	print "Verts saved";
		
	for uv in obj.uvValues:
		fp.write("vt %f %f\n" %(uv[0], uv[1]))
	print "UVs saved"

	faces = files3d.loadFacesIndices("data/3dobjs/base.obj")
	for f in faces:
		fp.write("f")
		for v in f:
			fp.write(" %i/%i " %(v[0], v[1]))
		fp.write("\n")
	print "Faces saved"

	if data == None:
		mhxWriteJointVertgroup(fp, 1, mh2bvh.skeletonRoot, obj)
	else:
		mhxWriteData(fp, data)
	print "Data saved"

	mhxbones.writeBones(fp, obj)
	print "Bones saved"
		
	fp.close()
	print "MHX file written"

#
#	loadFromMhxBase(fileName):
#

def loadFromMhxBase(fileName):
	try:
		print "Trying to open "+fileName
		fp = open(fileName, "r")
	except:
		print "Failed to open "+fileName
		return None

	line_nr = 0
	vertgroups = []
	shapekeys = []
	objects = []
	dispOb = False
	for line in fp: 
		line_nr = line_nr + 1
		line_split= line.split()
		if (line_split[0] == 'vertgroup'):
			vgroup = []
			vertgroups.append( (line_split[1], vgroup))
		elif (line_split[0] == 'wv'):
			vgroup.append( ( int(line_split[1]), float(line_split[2]) ))
		elif (line_split[0] == 'shapekey'):
			shkey = []
			shapekeys.append( (line_split[1], line_split[2], line_split[3], line_split[4], shkey))
		elif (line_split[0] == 'sv'):
			shkey.append( ( int(line_split[1]), float(line_split[2]), float(line_split[3]), float(line_split[4]) ))
		elif (line_split[0] == 'object'):
			lay1 = int(line_split[2])
			lay2 = int(line_split[3])
			print "Object ", line_split[1], lay1, lay2
			if (lay2 & 0x200):
				verts = []
				edges = []
				faces = []
				objects.append( (line_split[1], verts, edges, faces))
				dispOb = True
			else:
				dispOb = False
		elif (line_split[0] == 'v' and dispOb):
			verts.append( ( float(line_split[1]), float(line_split[2]), float(line_split[3]) ))
		elif (line_split[0] == 'e' and dispOb):	
			edges.append( ( int(line_split[1]), int(line_split[2]) ))
		elif (line_split[0] == 'f' and dispOb):	
			if (len(line_split) == 4):
				v4 = -1
			else:
				v4 = int(line_split[4])
			faces.append( ( int(line_split[1]), int(line_split[2]), int(line_split[3]), v4 ))
		else:
			pass
	fp.close()
	del fp
	return (vertgroups, shapekeys, objects)

#
#	mhxWriteData(fp, data):
#

def mhxWriteData(fp, (vertgroups, shapekeys, dispObjects)):
	for (g, vgroup) in vertgroups:
		fp.write("vertgroup %s\n" % (g) )
		for (v, w) in vgroup:
			if w > VertWeightLowerThreshold:
				fp.write("wv %d %f\n" % (v, w))
	
	for (key, min, max, vg, shkey) in shapekeys:
		fp.write("shapekey %s %s %s %s\n" % (key, min, max, vg))
		for (v, x, y, z) in shkey:
			fp.write("sv %d %f %f %f\n" % (v, x, y, z))

#
#	mhxWriteDispObs(fp, data)
#

def mhxWriteDispObs(fp, (vertgroups, shapekeys, dispObjects)):
	for (ob, verts, edges, faces) in dispObjects:
		fp.write("object %s %d %d keep\n" % (ob, 0x000, 0x200))
		fp.write("mesh %s\n" % (ob))
		for (x,y,z) in verts:
			fp.write("v %f %f %f\n" % (x,y,z))
		for (v1,v2) in edges:
			fp.write("e %d %d \n" % (v1,v2))
		for (v1,v2,v3,v4) in faces:
			if (v4 < 0):
				fp.write("f %d %d %d\n" % (v1,v2,v3))
			else:
				fp.write("f %d %d %d %d\n" % (v1,v2,v3,v4))

#
#	mhxWriteJointVertgroup(fp, level, joint, obj):
#

def mhxWriteJointVertgroup(fp, level, joint, obj):
	g = obj.getFaceGroup(joint.name)
	fp.write("vertgroup %s\n" % (joint.name))
	for fc in g.faces:
		for v in fc.verts:
			fp.write("wv %i %f \n" % (v.idx, 1.0))
	if joint.children:
		for child in joint.children:
			mhxWriteJointVertgroup(fp, level+1, child, obj)



