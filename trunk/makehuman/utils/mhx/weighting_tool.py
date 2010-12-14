""" 
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyright(c):**	  MakeHuman Team 2001-2010

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
Bone weighting utility

"""
import bpy, os, mathutils
from mathutils import *
from bpy.props import *

#
#	printVertNums(context):
#	class OBJECT_OT_PrintVnumsButton(bpy.types.Operator):
#
 
def printVertNums(context):
	ob = context.object
	print("Verts in ", ob)
	for v in ob.data.vertices:
		if v.select:
			print(v.index)
	print("End")

class OBJECT_OT_PrintVnumsButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_PrintVnumsButton"
	bl_label = "Print vnums"

	def execute(self, context):
		import bpy
		printVertNums(context)
		return{'FINISHED'}	

#
#	selectQuads():
#	class OBJECT_OT_SelectQuadsButton(bpy.types.Operator):
#

def selectQuads(context):
	ob = context.object
	for f in ob.data.faces:
		if len(f.vertices) == 4:
			f.select = True
		else:
			f.select = False
	return

class OBJECT_OT_SelectQuadsButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_SelectQuadsButton"
	bl_label = "Select quads"

	def execute(self, context):
		import bpy
		selectQuads(context)
		print("Quads selected")
		return{'FINISHED'}	

#
#	unVertexDiamonds(context):
#	class OBJECT_OT_UnvertexDiamondsButton(bpy.types.Operator):
#

def unVertexDiamonds(context):
	ob = context.object
	print("Unvertex diamonds in %s" % ob)
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.select_all(action='DESELECT')
	bpy.ops.object.mode_set(mode='OBJECT')
	me = ob.data
	for f in me.faces:		
		if len(f.vertices) < 4:
			for vn in f.vertices:
				me.vertices[vn].select = True
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.object.vertex_group_remove_from(all=True)
	bpy.ops.object.mode_set(mode='OBJECT')
	return

class OBJECT_OT_UnvertexDiamondsButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_UnvertexDiamondsButton"
	bl_label = "Unvertex diamonds"

	def execute(self, context):
		import bpy
		unVertexDiamonds(context)
		print("Diamonds unvertexed")
		return{'FINISHED'}	


#
#	pairWeight(context):
#

def pairWeight(context):
	ob = context.object
	scn = context.scene
	name1 = scn['MhxBone1']
	name2 = scn['MhxBone2']
	weight = scn['MhxWeight']
	index1 = -1
	index2 = -1
	for vgrp in ob.vertex_groups:
		if vgrp.name == name1:
			index1 = vgrp.index
		if vgrp.name == name2:
			index2 = vgrp.index
	if index1 < 0 or index2 < 0:
		raise NameError("Did not find vertex groups %s or %s" % (name1, name2))
	for v in ob.data.vertices:
		if v.select:
			for grp in v.groups:
				if grp.index == index1:
					grp.weight = weight
				elif grp.index == index2:
					grp.weight = 1-weight
				else:
					ob.remove_from_group(grp, v.index)
	return

class OBJECT_OT_PairWeightButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_PairWeightButton"
	bl_label = "Weight pair"

	def execute(self, context):
		import bpy
		pairWeight(context)
		return{'FINISHED'}	

#
#	symmetrizeWeights(context):
#	rightVerts(factor, me):
#	class OBJECT_OT_SymmetrizeWeightsButton(bpy.types.Operator):
#

Epsilon = 1e-3

def symmetrizeWeights(context):
	ob = context.object
	scn = context.scene

	left = {}
	leftIndex = {}
	right = {}
	rightIndex = {}
	symm = {}
	symmIndex = {}
	for vgrp in ob.vertex_groups:
		nameStripped = vgrp.name[:-2]
		if vgrp.name[-2:] == '_L':
			left[nameStripped] = vgrp
			leftIndex[vgrp.index] = nameStripped
		elif vgrp.name[-2:] == '_R':
			right[nameStripped] = vgrp
			rightIndex[vgrp.index] = nameStripped
		else:
			symm[vgrp.name] = vgrp
			symmIndex[vgrp.index] = vgrp.name

	print('Left', left.items())
	print('Right', right.items())
	print('Symm', symm.items())

	if scn['MhxLeft2Right']:
		factor = 1
		fleft = left
		fright = right
	else:
		factor = -1
		fleft = right
		fright = left

	rverts = rightVerts(factor, ob.data)
	for (vn, rv) in rverts.items():
		v = ob.data.vertices[vn]
		print(v.index, rv.index)
		for rgrp in rv.groups:
			rgrp.weight = 0
		for grp in v.groups:
			rgrp = None
			try:
				name = leftIndex[grp.group]
				rgrp = right[name]
			except:
				pass
			try:
				name = rightIndex[grp.group]
				rgrp = left[name]
			except:
				pass
			try:
				name = symmIndex[grp.group]
				rgrp = symm[name]
			except:
				pass
			#print("  ", name, grp, rgrp)
			ob.vertex_groups.assign([rv.index], rgrp, grp.weight, 'REPLACE')
	return len(rverts)

def rightVerts(factor, me):
	rverts = {}
	threshold = 0
	for v in me.vertices:
		if v.select and factor*v.co[0] > Epsilon:
			rco = v.co.copy()
			rco[0] = -rco[0]
			for rv in me.vertices:
				dx = rv.co - rco
				if dx.length < Epsilon:
					rverts[v.index] = rv
					continue
			if (v.index >= threshold):
				print(v.index)
				threshold += 1000
	return rverts

class OBJECT_OT_SymmetrizeWeightsButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_SymmetrizeWeightsButton"
	bl_label = "Symmetrize weights"

	def execute(self, context):
		import bpy
		n = symmetrizeWeights(context)
		print("Weights symmetrized, %d vertices" % n)
		return{'FINISHED'}	

#
#	symmetrizeShapes(context):
#	class OBJECT_OT_SymmetrizeShapesButton(bpy.types.Operator):
#

def symmetrizeShapes(context):
	ob = context.object
	scn = context.scene
	if scn['MhxLeft2Right']:
		factor = 1
	else:
		factor = -1

	verts = ob.data.vertices
	rverts = rightVerts(factor, ob.data)
	for key in ob.data.shape_keys.keys:
		print(key.name)
		for rv in rverts.values():
			key.data[rv.index].co = rv.co

		for v in verts:
			try:
				rv = rverts[v.index]
			except:
				rv = None
			if rv:
				lco = key.data[v.index].co
				rco = lco.copy()
				rco[0] = -rco[0]
				key.data[rv.index].co = rco

	return len(rverts)

class OBJECT_OT_SymmetrizeShapesButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_SymmetrizeShapesButton"
	bl_label = "Symmetrize shapes"

	def execute(self, context):
		import bpy
		n = symmetrizeShapes(context)
		print("Shapes symmetrized, %d vertices" % n)
		return{'FINISHED'}	


#
#	initInterface(context):
#	class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
#

def initInterface(context):
	bpy.types.Scene.MhxWeight = FloatProperty(
		name="Weight", 
		description="Weight of bone1, 1-weight of bone2", 
		min=0, max=1)

	bpy.types.Scene.MhxBone1 = StringProperty(
		name="Bone 1", 
		maxlen=40,
		default='')

	bpy.types.Scene.MhxBone2 = StringProperty(
		name="Bone 2", 
		maxlen=40,
		default='')

	bpy.types.Scene.MhxLeft2Right = BoolProperty(
		name="Left -> right", 
		default=True)


	scn = context.scene
	if scn:
		scn['MhxWeight'] = 1.0
		scn['Bone1'] = 'Bone1'
		scn['Bone2'] = 'Bone2'
		scn['MhxLeft2Right'] = True

	return

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_InitInterfaceButton"
	bl_label = "Initialize"

	def execute(self, context):
		import bpy
		initInterface(context)
		print("Interface initialized")
		return{'FINISHED'}	

#
#	class MhxWeightToolsPanel(bpy.types.Panel):
#

class MhxWeightToolsPanel(bpy.types.Panel):
	bl_label = "Weight tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	@classmethod
	def poll(cls, context):
		return context.object and context.object.type == 'MESH'

	def draw(self, context):
		layout = self.layout
		layout.operator("object.PrintVnumsButton")
		layout.operator("object.SelectQuadsButton")
		layout.operator("object.UnvertexDiamondsButton")

		layout.separator()
		layout.prop(context.scene, 'MhxLeft2Right')
		layout.operator("object.SymmetrizeWeightsButton")	
		layout.operator("object.SymmetrizeShapesButton")	

		layout.label('Weight pair')
		layout.prop(context.scene, 'MhxWeight')
		layout.prop(context.scene, 'MhxBone1')
		layout.prop(context.scene, 'MhxBone2')
		layout.operator("object.PairWeightButton")

#
#	Init and register
#

initInterface(bpy.context)

def register():
	pass

def unregister():
	pass

if __name__ == "__main__":
	register()


