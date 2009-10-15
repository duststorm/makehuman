#!BPY
""" 
Name: 'Makehuman (.mhx)'
Blender: 249
Group: 'Export'
Tooltip: 'Export from MakeHuman eXchange format (.mhx)'
"""

__author__= ['Thomas Larsson']
__url__ = ("www.makehuman.org")
__version__= '0.1'
__bpydoc__= '''\
MHX exporter for Blender
0.1 First version
'''
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
MHX (MakeHuman eXchange format) exporter for Blender.

TO DO

"""

import Blender
from Blender import *
from Blender.Mathutils import *
import os

MAJOR_VERSION = 0
MINOR_VERSION = 1

Epsilon = 1e-6

#
#	Bone flags
#

F_CON = 0x01
F_NODEF = 0x02

#
#	Texture channels
#

T_COLOR	= 0x01
T_REF	= 0x02
T_ALPHA	= 0x04
T_MIX	= 0x08

#
#	writeMhxFile(fileName):
#

def writeMhxFile(fileName):
	# Check fileName
	n = len(fileName)
	if fileName[n-3:] != "mhx":
		Draw.PupMenu("Error: Not a mhx file: " + fileName)
		return

	# Write MHX file
	print "Writing MHX file " + fileName
	fp = open(fileName, 'w')
	fp.write("# Blender exported MHX\n")
	scn = Scene.GetCurrent()
	for ob in scn.objects:
		if (ob.type == "Mesh"):
			exportMesh(ob, fp)
		elif (ob.type == "Armature"):
			exportRig(ob, fp)
	fp.close()
	print "MHX file %s written\n" % (fileName)

#
#	exportMesh(ob, fp):
#

def exportMesh(ob, fp):
	me = ob.getData(False, True)

	for mat in me.materials:
		fp.write("material %s\n" % mat.name)
		fp.write("color %f %f %f\n" %(mat.rgbCol[0], mat.rgbCol[1], mat.rgbCol[2]))
		fp.write("alpha %f\n" % (mat.alpha) )
		for mtex in mat.textures:
			if mtex != None and mtex.tex.type == Texture.Types.IMAGE: 
				file = mtex.tex.image.filename
				file_split = file.split('/')
				n = len(file_split)
				if mtex.tex.image != None:
					fp.write("texture %s %s.%s\n" % ( mtex.tex.name, file_split[n-2], file_split[n-1] ))

	lay1 = ob.Layers & 0x3ff
	lay2 = (ob.Layers >> 10) & 0x3ff
	fp.write("object %s %d %d add\n" % (ob.name, lay1, lay2))
	fp.write("mesh %s\n" % (me.name))
	for v in me.verts:
		fp.write("v %f %f %f\n" %(v.co[0], v.co[1], v.co[2]))
	print "Verts saved";
	'''		
	for uv in v.uvco:
		fp.write("vt %f %f\n" %(uv[0], uv[1]))
	print "UVs saved"

	for v in me.verts:
		fp.write("vn %f %f %f\n" %(v.no[0], v.no[1], v.no[2]))
	print "Normals saved"
	'''
	
	if me.faces:
		for f in me.faces:
			fp.write("f")
			for v in f.verts:
				fp.write(" %i" %( v.index ))
			fp.write("\n")
		print "Faces saved"
	else:
		for e in me.edges:
			fp.write("e %i %i\n" % (e.v1.index, e.v2.index))
		print "Edges saved"
			

	vertgroups = me.getVertGroupNames()
	for g in vertgroups:
		save = True
		n = len(g)
		if g[:5] == "joint":
			save = False
		#elif g[n-2:] == "_L":
		#	g1 = g[:n-2] + "_R"
		#elif g[n-2:] == "_R":
		#	g1 = g[:n-2] + "_L"
		else:
			g1 = g
			
		if save:	
			print "vg ", g, " to ", g1
			fp.write("vertgroup %s\n" % g1 )
			vgroup = me.getVertsFromGroup(g, True)
			for (v, w) in vgroup:
				fp.write("wv %i %f\n" % (v, w) )
	print "Vertgroups saved"

	# Shape keys
	if me.key:
		if me.key.relative == False:
			Draw.Pupmenu("Keys should be relative")
		blocks = me.key.blocks
		for b in blocks:
			if b.vgroup:
				vgname = b.vgroup
			else:
				vgname = "None"
			fp.write("shapekey %s %f %f %s\n" % (b.name, b.slidermin, b.slidermax, vgname))
			for (n,v) in enumerate(b.data):
				dv = v - me.verts[n].co
				if dv.length > Epsilon:
					fp.write("sv %d %f %f %f\n" %(n, dv[0], dv[1], dv[2]))


def exportRig(ob, fp):
	amt = ob.getData()
	bones = amt.bones.values()
	lay1 = ob.Layers & 0x3ff
	lay2 = (ob.Layers >> 10) & 0x3ff
	fp.write("object %s %d %d add\n" % (ob.name, lay1, lay2))
	fp.write("armature %s\n" % (amt.name))
	for b in bones:
		if b.name == "Root":
			break
	exportJoint(fp, b)
	print "Rig saved"
			
#
#	exportJoint(fp, bone):
#

def exportJoint(fp, bone):
	print "Bone "+bone.name
	flags = 0
	#if bone.options[Armature.CONNECTED]:
	#	flags |= F_CON
	#if bone.options[Armature.NO_DEFORM]:
	#	flags |= F_NODEF
	if bone.parent:
		parent = bone.parent.name
	else:
		parent = "None"
	fp.write("bone %s %s %f %d %d\n" %(bone.name, parent, 0.0, flags, bone.layerMask))
	head = bone.head['ARMATURESPACE']
	fp.write("head %f %f %f\n" % (head[0], head[1], head[2]))
	tail = bone.tail['ARMATURESPACE']
	fp.write("tail %f %f %f\n" % (tail[0], tail[1], tail[2]))
	
	if bone.children:
		for child in bone.children:
			exportJoint(fp, child)

#
#	Main entry point
#	Change the filename to point to your MakeHuman directory
#

#writeMhxFile("/home/thomas/makehuman/data/3dobjs/mhxbase.mhx")

Blender.Window.FileSelector (writeMhxFile, 'SAVE MHX FILE')