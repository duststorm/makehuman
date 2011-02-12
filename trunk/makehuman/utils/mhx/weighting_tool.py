""" 
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyright(c):**	  MakeHuman Team 2001-2011

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
#	class VIEW3D_OT_MhxPrintVnumsButton(bpy.types.Operator):
#
 
def printVertNums(context):
	ob = context.object
	print("Verts in ", ob)
	for v in ob.data.vertices:
		if v.select:
			print(v.index)
	print("End")

class VIEW3D_OT_MhxPrintVnumsButton(bpy.types.Operator):
	bl_idname = "mhx.weight_print_vnums"
	bl_label = "Print vnums"

	def execute(self, context):
		import bpy
		printVertNums(context)
		return{'FINISHED'}	

#
#	selectVertNum8m(context):
#	class VIEW3D_OT_MhxSelectVnumButton(bpy.types.Operator):
#
 
def selectVertNum(context):
	n = context.scene.MhxVertNum
	ob = context.object
	bpy.ops.object.mode_set(mode='OBJECT')
	for v in ob.data.vertices:
		v.select = False
	v = ob.data.vertices[n]
	v.select = True
	bpy.ops.object.mode_set(mode='EDIT')

class VIEW3D_OT_MhxSelectVnumButton(bpy.types.Operator):
	bl_idname = "mhx.weight_select_vnum"
	bl_label = "Select vnum"

	def execute(self, context):
		selectVertNum(context)
		return{'FINISHED'}	

#
#	printFaceNums(context):
#	class VIEW3D_OT_MhxPrintVnumsButton(bpy.types.Operator):
#
 
def printFaceNums(context):
	ob = context.object
	print("Faces in ", ob)
	for f in ob.data.faces:
		if f.select:
			print(f.index)
	print("End")

class VIEW3D_OT_MhxPrintFnumsButton(bpy.types.Operator):
	bl_idname = "mhx.weight_print_fnums"
	bl_label = "Print fnums"

	def execute(self, context):
		import bpy
		printFaceNums(context)
		return{'FINISHED'}	

#
#	selectQuads():
#	class VIEW3D_OT_MhxSelectQuadsButton(bpy.types.Operator):
#

def selectQuads(context):
	ob = context.object
	for f in ob.data.faces:
		if len(f.vertices) == 4:
			f.select = True
		else:
			f.select = False
	return

class VIEW3D_OT_MhxSelectQuadsButton(bpy.types.Operator):
	bl_idname = "mhx.weight_select_quads"
	bl_label = "Select quads"

	def execute(self, context):
		import bpy
		selectQuads(context)
		print("Quads selected")
		return{'FINISHED'}	

#
#	removeVertexGroups(context):
#	class VIEW3D_OT_MhxRemoveVertexGroupsButton(bpy.types.Operator):
#

def removeVertexGroups(context):
	ob = context.object
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.vertex_group_remove(all=True)
	return

class VIEW3D_OT_MhxRemoveVertexGroupsButton(bpy.types.Operator):
	bl_idname = "mhx.weight_remove_vertex_groups"
	bl_label = "Unvertex all"

	def execute(self, context):
		removeVertexGroups(context)
		print("All vertex groups removed")
		return{'FINISHED'}	

#
#	unVertexDiamonds(context):
#	class VIEW3D_OT_MhxUnvertexDiamondsButton(bpy.types.Operator):
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

class VIEW3D_OT_MhxUnvertexDiamondsButton(bpy.types.Operator):
	bl_idname = "mhx.weight_unvertex_diamonds"
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

class VIEW3D_OT_MhxPairWeightButton(bpy.types.Operator):
	bl_idname = "mhx.weight_pair_weight"
	bl_label = "Weight pair"

	def execute(self, context):
		import bpy
		pairWeight(context)
		return{'FINISHED'}	

#
#	symmetrizeWeights(context):
#	rightVerts(factor, me):
#	class VIEW3D_OT_MhxSymmetrizeWeightsButton(bpy.types.Operator):
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
			if rgrp:
				rgrp.add([rv.index], grp.weight, 'REPLACE')
			else:
				raise NameError("No rgrp for %s %s %s" % (list(v.groups), grp, grp.group))
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

class VIEW3D_OT_MhxSymmetrizeWeightsButton(bpy.types.Operator):
	bl_idname = "mhx.weight_symmetrize_weights"
	bl_label = "Symmetrize weights"

	def execute(self, context):
		import bpy
		n = symmetrizeWeights(context)
		print("Weights symmetrized, %d vertices" % n)
		return{'FINISHED'}	

#
#	symmetrizeShapes(context):
#	class VIEW3D_OT_MhxSymmetrizeShapesButton(bpy.types.Operator):
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

class VIEW3D_OT_MhxSymmetrizeShapesButton(bpy.types.Operator):
	bl_idname = "mhx.weight_symmetrize_shapes"
	bl_label = "Symmetrize shapes"

	def execute(self, context):
		import bpy
		n = symmetrizeShapes(context)
		print("Shapes symmetrized, %d vertices" % n)
		return{'FINISHED'}	

#
#	shapekeyFromObject(ob, targ):
#	class VIEW3D_OT_MhxShapeKeysFromObjectsButton(bpy.types.Operator):
#

def shapekeyFromObject(ob, targ):
	verts = ob.data.vertices
	tverts = targ.data.vertices
	print("Create shapekey %s" % targ.name)
	print(len(verts), len(tverts))
	if len(verts) != len(tverts):
		print("%s and %s do not have the same number of vertices" % (ob, targ))
		return
	if not ob.data.shape_keys:
		ob.shape_key_add(name='Basis', from_mix=False)
	skey = ob.shape_key_add(name=targ.name, from_mix=False)
	for n,v in enumerate(verts):
		vt = tverts[n].co
		pt = skey.data[n].co
		pt[0] = vt[0]
		pt[1] = vt[1]
		pt[2] = vt[2]
	print("Shape %s created" % skey)
	return	

class VIEW3D_OT_MhxShapeKeysFromObjectsButton(bpy.types.Operator):
	bl_idname = "mhx.weight_shapekeys_from_objects"
	bl_label = "Shapes from objects"

	def execute(self, context):
		import bpy
		ob = context.object
		for targ in context.scene.objects:
			if targ.type == 'MESH' and targ.select and targ != ob:
				shapekeyFromObject(ob, targ)
		print("Shapekeys created for %s" % ob)
		return{'FINISHED'}	

#
#	recoverDiamonds(context):
#	class VIEW3D_OT_MhxRecoverDiamondsButton(bpy.types.Operator):
#

def recoverDiamonds(context):
	dob = context.scene.objects['DiamondMesh']
	dverts = dob.data.vertices
	ob = context.object
	verts = ob.data.vertices
	Epsilon = 1e-4

	context.scene.objects.active = dob
	bpy.ops.object.vertex_group_remove(all=True)

	vassoc = {}
	dn = 0
	for v in verts:
		vec = dverts[dn].co - v.co
		while vec.length > Epsilon:
			dn += 1
			vec = dverts[dn].co - v.co
		vassoc[v.index] = dn

	for grp in ob.vertex_groups:
		group = dob.vertex_groups.new(grp.name)
		index = group.index
		for v in verts:	
			for vgrp in v.groups:
				if vgrp.group == index:
					dn = vassoc[v.index]
					#dob.vertex_groups.assign( [dn], group, vgrp.weight, 'REPLACE' )
					group.add( [dn], vgrp.weight, 'REPLACE' )
					continue

	print("Diamonds recovered")
	return
	

class VIEW3D_OT_MhxRecoverDiamondsButton(bpy.types.Operator):
	bl_idname = "mhx.weight_recover_diamonds"
	bl_label = "Recover diamonds"

	def execute(self, context):
		recoverDiamonds(context)
		return{'FINISHED'}	

#
#	exportVertexGroups(filePath)
#	class VIEW3D_OT_MhxExportVertexGroupsButton(bpy.types.Operator):
#

def exportVertexGroups(context):
	filePath = context.scene['MhxVertexGroupFile']
	fileName = os.path.expanduser(filePath)
	fp = open(fileName, "w")
	ob = context.object
	me = ob.data
	for vg in ob.vertex_groups:
		index = vg.index
		weights = []
		for v in me.vertices:
			for grp in v.groups:
				if grp.group == index and grp.weight > 0.005:
					weights.append((v.index, grp.weight))

		exportList(context, weights, vg.name, fp)
	fp.close()
	return

class VIEW3D_OT_MhxExportVertexGroupsButton(bpy.types.Operator):
	bl_idname = "mhx.weight_export_vertex_groups"
	bl_label = "Export vertex groups"

	def execute(self, context):
		exportVertexGroups(context)
		return{'FINISHED'}	

#
#	exportSumGroups(context):
#	exportListAsVertexGroup(weights, name, fp):
#	class VIEW3D_OT_MhxExportSumGroupsButton(bpy.types.Operator):
#

def exportSumGroups(context):
	filePath = context.scene['MhxVertexGroupFile']
	fileName = os.path.expanduser(filePath)
	fp = open(fileName, "w")
	ob = context.object
	me = ob.data
	for name in ['UpArm', 'LoArm', 'UpLeg']:
		for suffix in ['_L', '_R']:
			weights = {}
			for n in range(1,4):
				vg = ob.vertex_groups["%s%d%s" % (name, n, suffix)]
				index = vg.index
				for v in me.vertices:
					for grp in v.groups:
						if grp.group == index:
							try:
								w = weights[v.index]
							except:
								w = 0
							weights[v.index] = grp.weight + w
				# ob.vertex_groups.remove(vg)
			exportList(context, weights.items(), name+'3'+suffix, fp)
	fp.close()
	return

def exportList(context, weights, name, fp):
	#if len(weights) == 0:
	#	return
	if context.scene['MhxExportAsWeightFile']:
		if len(weights) > 0:
			fp.write("\n# weights %s\n" % vg.name)
			for (vn,w) in weights:
				if w > 0.005:
					fp.write("  %d %.3g\n" % (vn, w))
	else:
		fp.write("\n  VertexGroup %s\n" % name)
		for (vn,w) in weights:
			if w > 0.005:
				fp.write("	wv %d %.3g ;\n" % (vn, w))
		fp.write("  end VertexGroup %s\n" % name)
	return

class VIEW3D_OT_MhxExportSumGroupsButton(bpy.types.Operator):
	bl_idname = "mhx.weight_export_sum_groups"
	bl_label = "Export sum groups"

	def execute(self, context):
		exportSumGroups(context)
		return{'FINISHED'}	

#
#	initInterface(context):
#	class VIEW3D_OT_MhxInitInterfaceButton(bpy.types.Operator):
#

def initInterface(context):
	bpy.types.Scene.MhxVertNum = IntProperty(
		name="Vert number", 
		description="Vertex number to select")

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

	bpy.types.Scene.MhxExportAsWeightFile = BoolProperty(
		name="Export as weight file", 
		default=False)

	bpy.types.Scene.MhxVertexGroupFile = StringProperty(
		name="Vertex group file", 
		maxlen=100,
		default='')


	scn = context.scene
	if scn:
		scn['MhxWeight'] = 1.0
		scn['MhxBone1'] = 'Bone1'
		scn['MhxBone2'] = 'Bone2'
		scn['MhxLeft2Right'] = True
		scn['MhxExportAsWeightFile'] = False
		scn['MhxVertexGroupFile'] = '~/vgroups.txt'

	return

class VIEW3D_OT_MhxInitInterfaceButton(bpy.types.Operator):
	bl_idname = "mhx.weight_init_interface"
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
		layout.operator("mhx.weight_print_vnums")
		layout.operator("mhx.weight_print_fnums")
		layout.operator("mhx.weight_select_quads")
		layout.operator("mhx.weight_remove_vertex_groups")
		layout.operator("mhx.weight_unvertex_diamonds")
		layout.operator("mhx.weight_recover_diamonds")

		layout.separator()
		layout.prop(context.scene, 'MhxVertNum')
		layout.operator("mhx.weight_select_vnum")

		layout.separator()
		layout.prop(context.scene, 'MhxLeft2Right')
		layout.operator("mhx.weight_symmetrize_weights")	
		layout.operator("mhx.weight_symmetrize_shapes")	

		layout.separator()
		layout.prop(context.scene, 'MhxVertexGroupFile')
		layout.prop(context.scene, 'MhxExportAsWeightFile')
		layout.operator("mhx.weight_export_vertex_groups")	
		layout.operator("mhx.weight_export_sum_groups")	

		layout.separator()
		layout.operator("mhx.weight_shapekeys_from_objects")	

		layout.label('Weight pair')
		layout.prop(context.scene, 'MhxWeight')
		layout.prop(context.scene, 'MhxBone1')
		layout.prop(context.scene, 'MhxBone2')
		layout.operator("mhx.weight_pair_weight")

#
#	Init and register
#

initInterface(bpy.context)

def register():
	bpy.utils.register_module(__name__)
	pass

def unregister():
	bpy.utils.unregister_module(__name__)
	pass

if __name__ == "__main__":
	register()


