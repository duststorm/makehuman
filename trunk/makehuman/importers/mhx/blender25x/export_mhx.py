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
MHX (MakeHuman eXchange format) exporter for Blender 2.5.
Version 0.5

TO DO

"""
__author__= ['Thomas Larsson']
__url__ = ("www.makehuman.org")
__version__= '0.6'
__bpydoc__= '''\
MHX importer for Blender 2.5
0.6 Sixth version
'''

import bpy
import Mathutils
import os
import types
import array
import struct

MAJOR_VERSION = 0
MINOR_VERSION = 6
verbosity = 1
Epsilon = 1e-5
done = 0

#
#
#

MaxDepth = 6
Optimize = 3

M_Mat	= 0x01
M_Geo	= 0x02
M_Amt	= 0x04
M_Obj	= 0x08
M_Game	= 0x10
M_Scn	= 0x20
M_Tool	= 0x40
M_Anim	= 0x80
M_All = 0xff

M_Rigify = 0x100
M_MHX	= 0x200
M_Shape	= 0x400
M_VGroup = 0x800
M_Part = 0x1000
M_MHPart = 0x2000

expMsk = 0
theRig = ""

#
#	RegisteredBlocks: ( local, refer, creator )
#

RegisteredBlocks = {
	'Scene' : (False, True, "''"),
	'World' : (False, True, "''"),
	'Object' : (False, True, "''"),
	'Group' : (False, True, "''"),
	'Action' : (False, True, "''"),

	'Mesh' : (False, True, "''"),
	'Armature' : (False, True, "''"),
	'Lamp' : (False, True, "''"),
	'Camera' : (False, True, "''"),
	'Curve' : (False, True, "''"),
	'Empty' : (False, True, "''"),

	'Material' : (False, True, "''"),
	'Texture' : (False, True, "''"),
	'Image' : (False, True, "''"),

	'Modifier' : (True, False, "'rna.modifiers.new(\"%s\",\"%s\")' % (name, subtype)"),
	'Constraint' : (True, False, "'rna.constraints.new(\"%s\")' % (subtype)"),
	'MeshTextureFaceLayer' : (True, True, "'uvTexCreator(rna,\"%s\")' % (name)"),
	'MeshColorLayer' : (True, True, "'vertColCreator(rna,\"%s\")' % (name)"),
	'VertexGroup' : (True, True, "'vertGroupCreator(rna,\"%s\")' % (name)"),
	'ShapeKey' : (True, True, "'shapeKeyCreator(rna,\"%s\")' % (name)"),
	'ParticleSystem' : (True, True, "'partSysCreator(rna,\"%s\")' % (name)"),

	'Bone' : (True, True, "'edit_bones.new(\"%s\")' % (name)"),
	'BoneGroup' : (True, True, "'boneGroupCreator(rna,\"%s\")' % (name)"),
	
	'FCurve' : (True, False, "'drivers.new(\"%s\")' % (name)"),
	'DriverVariable' : (True, False, "'variables.new(\"%s\")' % (name)"),

	'Nurb' : (True, False, "'rna.modifiers.new(\"%s\",\"%s\")' % (name, subtype)"),
	'BezierSplinePoint' : (True, False, "'rna.modifiers.new(\"%s\",\"%s\")' % (name, subtype)"),

}

createdLocal = {
	'Modifier' : {},
	'Constraint' : {},
	'Bone' : {}, 
	'BoneGroup' : {}, 
	'Nurb' : {},
	'BezierSplinePoint' : {},

	'MeshTextureFaceLayer' : {},
	'MeshColorLayer' : {},
	'VertexGroup' : {},
	'ShapeKey' : {},
	'ParticleSystem' : {},
}

ModifierTypes = {
	'ArrayModifier' : 'ARRAY', 
	'BevelModifier' : 'BEVEL', 
	'BooleanModifier' : 'BOOLEAN', 
	'BuildModifier' : 'BUILD', 
	'DecimateModifier' : 'DECIMATE', 
	'EdgeSplitModifier' : 'EDGE_SPLIT', 
	'MaskModifier' : 'MASK', 
	'MirrorModifier' : 'MIRROR', 
	'MultiresModifier' : 'MULTIRES', 
	'SolidifyModifier' : 'SOLIDIFY', 
	'SubsurfModifier' : 'SUBSURF', 
	'UVProjectModifier' : 'UV_PROJECT', 
	'ArmatureModifier' : 'ARMATURE', 
	'CastModifier' : 'CAST', 
	'CurveModifier' : 'CURVE', 
	'DisplaceModifier' : 'DISPLACE', 
	'HookModifier' : 'HOOK', 
	'LatticeModifier' : 'LATTICE', 
	'MeshDeformModifier' : 'MESH_DEFORM', 
	'ShrinkWrapModifier' : 'SHRINKWRAP', 
	'SimpleDeformModifier' : 'SIMPLE_DEFORM', 
	'SmoothModifier' : 'SMOOTH', 
	'WaveModifier' : 'WAVE', 
	'ClothModifier' : 'CLOTH', 
	'CollisionModifier' : 'COLLISION', 
	'ExplodeModifier' : 'EXPLODE', 
	'FluidSimulationModifier' : 'FLUID_SIMULATION', 
	'ParticleInstanceModifier' : 'PARTICLE_INSTANCE', 
	'ParticleSystemModifier' : 'PARTICLE_SYSTEM', 
	'SmokeModifier' : 'SMOKE', 
	'SoftBodyModifier' : 'SOFT_BODY', 
	'SurfaceModifier' : 'SURFACE'
}

ConstraintTypes = {
	'CopyLocationConstraint' : 'COPY_LOCATION', 
	'CopyRotationConstraint' : 'COPY_ROTATION', 
	'CopyScaleConstraint' : 'COPY_SCALE', 
	'CopyTransformsConstraint' : 'COPY_TRANSFORMS', 
	'LimitDistanceConstraint' : 'LIMIT_DISTANCE', 
	'LimitLocationConstraint' : 'LIMIT_LOCATION', 
	'LimitRotationConstraint' : 'LIMIT_ROTATION',
	'LimitScaleConstraint' : 'LIMIT_SCALE', 
	'TransformConstraint' : 'TRANSFORM', 
	'ClampToConstraint' : 'CLAMP_TO', 
	'DampedTrackConstraint' : 'DAMPED_TRACK', 
	'IKConstraint' : 'IK', 
	'LockedTrackConstraint' : 'LOCKED_TRACK', 
	'SplineIKConstraint' : 'SPLINE_IK', 
	'StretchToConstraint' : 'STRETCH_TO', 
	'TrackToConstraint' : 'TRACK_TO', 
	'ActionConstraint' : 'ACTION', 
	'ChildOfConstraint' : 'CHILD_OF', 
	'FloorConstraint' : 'FLOOR', 
	'FollowPathConstraint' : 'FOLLOW_PATH', 
	'RigidBodyJointConstraint' : 'RIGID_BODY_JOINT', 
	'ScriptConstraint' : 'SCRIPT', 
	'ShrinkWrapConstraint' : 'SHRINKWRAP'
}

TextureTypes = {
	'ImageTexture' : 'IMAGE',
	'MarbleTexture' : 'MARBLE',
	'EnvironmentMapTexture' : 'ENVIRONMENT_MAP',
	'PointDensityTexture' : 'POINT_DENSITY',
	'VoxelDataTexture' : 'VOXEL_DATA',
	'BlendTexture' : 'BLEND',
	'MusgraveTexture' : 'MUSGRAVE',
	'StucciTexture' : 'STUCCI',
	'VoronoiTexture' : 'VORONOI',
	'CloudsTexture' : 'CLOUDS',
	'MagicTexture' : 'MAGIC',
	'PluginTexture' : 'PLUGIN',
	'WoodTexture' : 'WOOD',
	'DistortedNoiseTexture' : 'DISTORTED_NOISE',
	'NoiseTexture' : 'NOISE',
}

PropertyTypes = {
	'BoolProperty' : 'BOOLEAN',
	'IntProperty' : 'INT',
	'FloatProperty' : 'FLOAT',
	'StringProperty' : 'STRING',
	'EnumProperty' : 'ENUM',
	'PointerProperty' : 'POINTER',
	'CollectionProperty' : 'COLLECTION',

	'BoolVectorProperty' : 'BOOLEAN',
	'IntVectorProperty' : 'INT',
	'FloatVectorProperty' : 'FLOAT',
}

MinBlockLevel = {
	
	'Object' : M_Geo,
	'Mesh' : M_Geo,
	'MeshTextureFaceLayer' : M_Geo,
	'MeshColorLayer' : M_Geo,
	'ShapeKey' : M_Geo,
	'VertexGroup' : M_Geo,
	'Armature' : M_Geo,
	'Pose' : M_Geo,
	'PoseBone' : M_Geo,
	'Material' : M_Geo,
	'Texture' : M_Geo,
	'Image' : M_Geo,
	'Group' : M_Geo,
	'NodeGroup' : M_Geo,
	'Particle' : M_Geo,
	'ParticleSystem' : M_Geo,
	'Action' : M_Anim, 
	'Camera' : M_Scn, 
	'Lamp' : M_Scn, 
	'Scene' : M_Scn,
	'Brush' : M_Tool,
	'Actuator' : M_Game,
	'Controller' : M_Game,
	'Property' : M_Game, 
	'Sensor' : M_Game, 

	'MaterialHalo' : M_Scn, 
	'MaterialPhysics' : M_Game, 
	'MaterialRaytraceTransparency' : M_Scn, 
	'MaterialStrand' : M_Geo, 
	'MaterialVolume' : M_Geo, 
	'AnimViz' : M_Anim, 
	'AnimVizOnionSkinning' : M_Anim, 
	'AnimVizMotionPaths' : M_Anim, 
	'FieldSettings' : M_Scn, 
	'CurveMapping' : M_Scn, 
	'EffectorWeights' : M_Geo, 
	'PointCache' : 0, 
	'SceneRenderData' : 0,
	'GameObjectSettings' : M_Game,
}
		
#
#	exportDefault(typ, data, header, prio, exclude, fp):
#

def exportDefault(typ, data, header, prio, exclude, fp):
	pad = ""
	try:
		if not data.enabled:
			return
	except:
		pass
	try:
		name = data.name.replace(' ','_')
	except:
		name = ''

	fp.write("%s%s %s" % (pad, typ, name))
	for val in header:
		fp.write(" %s" % val)
	fp.write("\n")
	writePrio(data, prio, pad+"  ", fp)
	writeDir(data, prio+exclude, pad+"  ", fp)
	fp.write("%send %s\n" % (pad,typ))
	return

#
#
#

def initLocalData():
	global createdLocal
	for key in createdLocal.keys():
		createdLocal[key] = []

#
#	writePrio(data, prio, pad, fp):
#	writeDir(data, exclude, pad, fp):
#	writeSubDir(data, exclude, pad, depth, fp):
#

def writePrio(data, prio, pad, fp):
	for ext in prio:
		writeExt(ext, "data", [], pad, 0, fp, globals(), locals())

def writeDir(data, exclude, pad, fp):
	for ext in dir(data):
		writeExt(ext, "data", exclude, pad, 0, fp, globals(), locals())
	try:
		props = data.items()
	except:
		props = []
	for (key,val) in props:
		if key != '_RNA_UI':
			fp.write("%sProperty %s " % (pad, key))
			writeQuoted(val, fp)
			fp.write(" ;\n")
	return

def writeSubDir(data, exclude, pad, depth, fp):
	if depth > MaxDepth:
		msg = "OVERFLOW in writeSubDir\n"
		# raise NameError(msg)
		fp.write(msg)
		return
	for ext in dir(data):
		writeExt(ext, "data", exclude, pad, depth, fp, globals(), locals())
	return

def writeQuoted(arg, fp):
	typ = type(arg)
	if typ == int or typ == float or typ == bool:
		fp.write("%s" % arg)
	elif typ == str:
		fp.write("'%s'"% stringQuote(arg.replace(' ', '_')))
	elif len(arg) > 1:
		c = '['
		for elt in arg:
			fp.write(c)
			writeQuoted(elt, fp)
			c = ','
		fp.write("]")
	else:
		raise NameError("Unknown property %s %s" % (arg, typ))

def stringQuote(string):
	s = ""
	for c in string:
		if c == '\\':
			s += "\\\\"
		elif c == '\"':
			s += "\\\""
		elif c == '\'':
			s += "\\\'"
		else:
			s += c
	return s
		
			
#
#	writeExt(ext, name, exclude, pad, depth, fp, globals, locals):		
#

def writeExt(ext, name, exclude, pad, depth, fp, globals, locals):		
	expr = name+"."+ext
	try:
		arg = eval(expr, globals, locals)
		success = True
	except:
		success = False
		arg = None
	if success:
		writeValue(ext, arg, exclude, pad, depth, fp)
	return

#
#	writeValue(ext, arg, exclude, pad, depth, fp):
#

excludeList = [\
	# 'material', 'materials', 'active_material', 
	'bl_rna', 'fake_user', 'id_data', 'rna_type', 'name', 'tag', 'users', 'type'
]

Danger = []	# ['ParticleEdit', 'color_ramp']


def writeValue(ext, arg, exclude, pad, depth, fp):
	global todo

	if len(str(arg)) == 0 or\
	   arg == None or\
	   arg == [] or\
	   ext[0] == '_' or\
	   ext in excludeList or\
	   ext in exclude or\
	   ext in Danger:
		return
		
	if ext == 'targets':
		print("TARG", ext, arg)
		return

	if ext == 'end':
		print("RENAME end", arg)
		ext = '\\ end'

	# print("D", ext)

	typ = type(arg)
	typeSplit = str(typ).split("'")
	if typ == int:
		fp.write("%s%s %d ;\n" % (pad, ext, arg))
	elif typ == float:
		fp.write("%s%s %.6g ;\n" % (pad, ext, arg))
	elif typ == bool:
		fp.write("%s%s %s ;\n" % (pad, ext, arg))
	elif typ == str:
		fp.write("%s%s '%s' ;\n" % (pad, ext, stringQuote(arg.replace(' ','_'))))
	elif typ == list:
		fp.write("%s%s List\n" % (pad, ext))
		n = 0
		for elt in arg:
			writeValue("[%d]" % n, elt, [], pad+"  ", depth+1, fp)
			n += 1
		fp.write("%send List\n" % pad)
	elif typ == Mathutils.Vector:
		c = '('
		fp.write("%s%s " % (pad, ext))
		for elt in arg:
			fp.write("%s%.6g" % (c,elt))
			c = ','
		fp.write(") ;\n")
	elif typ == Mathutils.Euler:
		fp.write("%s%s (%.6g,%.6g,%.6g) ;\n" % (pad, ext, arg[0], arg[1], arg[2]))
	elif typ == Mathutils.Quaternion:
		fp.write("%s%s (%.6g,%.6g,%.6g,%.6g) ;\n" % (pad, ext, arg[0], arg[1], arg[2], arg[3]))
	elif typ == Mathutils.Matrix:
		fp.write("%s%s Matrix\n" % (pad, ext))
		n = len(arg)
		for i in range(n):
			fp.write("%s  row " %pad)
			for j in range(n):
				fp.write("%s " % arg[i][j])
			fp.write(";\n")
		fp.write("%send Matrix\n" %pad)
	elif writeArray(ext, arg, pad, depth, fp):
		pass
	elif typeSplit[0] == '<class ':
		writeClass(typeSplit, ext, arg, pad, depth, fp)
	else:
		fp.write("# *** %s %s %s %s \n" % (ext, type(arg), arg))

	'''
	elif typ == dict:
		fp.write("%s%s dict\n" % (pad, ext))
		for (key,val) in arg.items():
			fp.write("%s  %s : %s ; \n" % (pad, key, val))
		fp.write("%send dict\n" % pad)
	elif type(arg) == tuple:
		fp.write("%s%s %s ;\n" % (pad, ext, arg))
	elif typ == array:
		fp.write("%s%s array %s ;\n" % (pad, ext, arg))
	elif type(arg) == struct:
		fp.write("%s%s struct %s ;\n" % (pad, ext, arg))
	'''

#
#	extractBpyType(data):
#

def extractBpyType(data):
	typeSplit = str(type(data)).split("'")
	if typeSplit[0] != '<class ':
		return None
	print(typeSplit)
	classSplit = typeSplit[1].split(".")
	if classSplit[0] == 'bpy' and classSplit[1] == 'types':
		return classSplit[2]
	elif classSplit[0] == 'bpy_types':
		return classSplit[1]
	else:
		return None
#
#	writeClass(string, ext, arg, pad, depth, fp):
#

def writeClass(list, ext, arg, pad, depth, fp):
	if depth > MaxDepth:
		fp.write("OVERFLOW in writeClass\n")
		return
	
	classSplit = list[1].split('.')
	if classSplit[0] == "bpy" and classSplit[1] == 'types':
		#<class 'bpy.types.GameObjectSettings'>
		writeBpyType(classSplit[2], ext, arg, pad, depth, fp)		
	elif classSplit[0] == "bpy_types":
		#<class 'bpy.types.GameObjectSettings'>
		writeBpyType(classSplit[1], ext, arg, pad, depth, fp)		
	elif classSplit[0] == "'netrender":
		return
	elif classSplit[0] == "builtin_function_or_method":
		return
		propName = str(arg).split()[2]
		writeProperty(propName, ext, arg, pad, depth, fp)
	elif classSplit[0] == "PropertyRNA" or classSplit[0] == "PropertyCollectionRNA":
		#<class 'PropertyRNA'>
		#print("PROP", arg, dir(arg))
		if 0 and dir(arg) != []:
			typeSplit = str(type(arg.rna_type)).split("'")
			fp.write("%s%s PropertyRNA\n" % (pad, ext))
			writeSubDir(arg, [], pad+"  ", depth+1, fp)
			# writeClass(typeSplit[1], ext, arg, pad+"  ", depth+1, fp)
			fp.write("%send PropertyRNA\n" % pad)
		return
	elif classSplit[0] == "method":
		return
		print("METHOD", arg)
	else:
		fp.write("# **CLASS** %s %s %s \n" % (ext, classSplit, arg))
	return
	
#

def writeProperty(propName, ext, prop, pad, depth, fp):
	if propName == '<generic':
		return
	return
	print("BUILTIN", propName, prop, dir(prop))
	fp.write("%s%s Property %s\n" % (pad, ext, PropertyTypes[propName]))
	writeDir(prop, [], pad+"  ", fp)
	fp.write("%send Property\n" % pad)
	
#
#	writeArray(ext, arg, pad, depth, fp):
#

def writeArray(ext, arg, pad, depth, fp):
	try:
		elt = arg[0]
	except:
		return False

	typ = type(elt)
	if typ == int or typ == float:
		fp.write("%s%s Array " % (pad, ext))
		for elt in arg:
			fp.write("%s " % elt)
		fp.write(" ;\n")
	elif typ == bool:
		fp.write("%s%s Array " % (pad, ext))
		for elt in arg:
			if elt:
				fp.write('1 ')
			else:
				fp.write('0 ')
		fp.write(' ;\n')
	else:
		for n,elt in enumerate(arg):
			if elt != None:
				writeValue("%s[%d]" %(ext,n), elt, [], pad, depth+1, fp)		

			
	return True

#
#	writeBpyType(typ, ext, data, pad, depth, fp):
#

def writeBpyType(typ, ext, data, pad, depth, fp):
	if typ in Danger:
		fp.write(" DANGER %s ;\n" % typ)
		return

	try:
		msk = MinBlockLevel[typ]
	except:
		msk = M_All			
	if msk & expMsk == 0:
		return

	try:
		name = data.name.replace(' ','_')
	except:
		name = "None"

	try:
		enabled = data.enabled
	except:
		enabled = True
	if not enabled:
		return

	subtype = None
	try:
		subtype = ModifierTypes[typ]
		typ = 'Modifier'
	except:
		pass
	try:
		subtype = ConstraintTypes[typ]
		typ = 'Constraint'
	except:
		pass
	try:
		subtype = TextureTypes[typ]
		typ = 'Texture'
	except:
		pass

	try:
		(locl, refer, quoted) = RegisteredBlocks[typ]
	except:
		locl = True
		refer = False

	try:
		creator = eval(quoted)
	except:
		creator = ""
	if creator == None:
		creator = ""
	
	if locl:
		if refer:
			if name in createdLocal[typ]:
				fp.write("%s%s Refer %s %s ;\n" % (pad, ext, typ, name))
				return
			rnaType = 'Define'
			createdLocal[typ].append(name)
		else:
			rnaType = 'Struct'
	else:
		if refer:
			fp.write("%s%s Refer %s %s ;\n" % (pad, ext, typ, name))
			return
		else:
			raise NameError("Global Refer %s %s %s" % (ext, typ, name))
		
	fp.write("%s%s %s %s %s %s" % (pad, ext, rnaType, typ, name, creator))
	fp.write("\n")
	writeSubDir(data, [], pad+"  ", depth+1, fp)
	fp.write("%send %s\n" % (pad, rnaType))
	return


#
#	exportAnimationData(anim, fp):
#	exportAction(act, fp):
#	exportFCurve(fcu, fp):
#	exportActionGroup(grp, fp):
#	exportChannel(chnl, fp):
#	exportDriver(drv, fp):
#	exportDriverVariable(drv, fp):
#

def exportAnimationData(anim, fp):
	pad = "  "
	#name = anim.name.replace(' ', '_')
	fp.write("%sAnimationData\n" % pad)
	for drv in anim.drivers:
		exportFCurve(drv, pad+"  ", fp)
	writeDir(anim, ['drivers'], pad+"  ", fp)
	fp.write("%send AnimationData\n\n" % pad)

def exportAction(act, fp):
	name = act.name.replace(' ', '_')
	fp.write("Action %s \n" % name)
	for fcu in act.fcurves:
		exportFCurve(fcu, "  ", fp)
	writeDir(act, ['fcurves', 'groups'], "  ", fp)
	fp.write("end Action\n\n")

def exportFCurve(fcu, pad, fp):
	fp.write("%sFCurve %s %d\n"  % (pad, fcu.data_path.replace(' ', '_'), fcu.array_index))
	if fcu.driver:
		exportDriver(fcu.driver, pad+"  ", fp)
	for kpt in fcu.keyframe_points:
		exportKeyFramePoint(kpt, pad+"  ", fp)
	# exportActionGroup(fcu.group, pad+"  ", fp)
	writeDir(fcu, ['keyframe_points', 'group', 'data_path', 'array_index', 'driver'], pad+"  ", fp)
	fp.write("%send FCurve\n\n" % pad)

def exportDriver(drv, pad, fp):
	fp.write("%sDriver \n" % pad)
	for var in drv.variables:
		exportDriverVariable(var, pad+"  ", fp)
	writeDir(drv, ['variables'], pad+"  ", fp)
	fp.write("%send Driver\n\n" % pad)

def exportDriverVariable(var, pad, fp):
	name = var.name.replace(' ', '_')
	fp.write("%sDriverVariable %s \n" % (pad,name))
	targets = var.targets
	fp.write("%s  Targets %s ;\n" % (pad, targets))
	for targ in targets:
		fp.write("%s  Target  ;\n" % (pad))
	writeDir(var, [], pad+"  ", fp)
	fp.write("%send exportDriverVariable\n\n" % pad)

def exportActionGroup(grp, fp):
	fp.write("%sGroup %s \n" % (pad,grp.name.replace(' ', '_')))
	for chnl in grp.channels:
		exportChannel(chnl, pad+"  ", fp)
	writeDir(grp, ['channels'], "      ", fp)
	fp.write("%send Group\n\n" % pad)

def exportChannel(chnl, pad, fp):
	fp.write("%sChannel %s %d\n" % (pad, chnl.data_path.replace(' ', '_'), chnl.array_index))
	for kpt in chnl.keyframe_points:
		exportKeyFramePoint(kpt, pad+"  ", fp)
	writeDir(chnl, ['keyframe_points', 'group', 'data_path', 'array_index'], pad+"  ", fp)
	fp.write("%send Channels\n\n" % pad)

def exportKeyFramePoint(kpt, pad, fp):
	fp.write("%skp " % pad)
	writeTuple(kpt.co, fp)
	writeTuple(kpt.handle1, fp)
	writeTuple(kpt.handle2, fp)
	fp.write(";\n")

def writeTuple(list, fp):
	c = '('
	for elt in list:
		fp.write("%s%s" % (c, elt))
		c = ','
	fp.write(") ")
	return
#
#	exportMaterial(mat, fp):
#	exportMTex(index, mtex, use, fp):
#	exportTexture(tex, fp):
#	exportImage(img, fp)
#

def exportMaterial(mat, fp):
	fp.write("Material %s \n" % mat.name.replace(' ', '_'))
	for (n,mtex) in enumerate(mat.texture_slots):
		if mtex:
			exportMTex(n, mtex, mat.use_textures[n], fp)
	prio = ['diffuse_color', 'diffuse_shader', 'specular_color', 'specular_shader']
	writePrio(mat, prio, "  ", fp)
	exportRamp(mat.diffuse_ramp, "diffuse_ramp", fp)
	exportRamp(mat.specular_ramp, "specular_ramp", fp)
	writeDir(mat, prio+['texture_slots', 'volume', 'diffuse_ramp', 'specular_ramp'], "  ", fp)
	fp.write("end Material\n\n")

MapToTypes = {
	'map_alpha' : 'ALPHA',
	'map_ambient' : 'AMBIENT',
	'map_colordiff' : 'COLOR',
	'map_coloremission' : 'COLOR_EMISSION',
	'map_colorreflection' : 'COLOR_REFLECTION',
	'map_colorspec' : 'COLOR_SPEC',
	'map_colortransmission' : 'COLOR_TRANSMISSION',
	'map_density' : 'DENSITY',
	'map_diffuse' : 'DIFFUSE',
	'map_displacement' : 'DISPLACEMENT',
	'map_emission' : 'EMISSION',
	'map_emit' : 'EMIT', 
	'map_hardness' : 'HARDNESS',
	'map_mirror' : 'MIRROR',
	'map_normal' : 'NORMAL',
	'map_raymir' : 'RAYMIR',
	'map_reflection' : 'REFLECTION',
	'map_scattering' : 'SCATTERING',
	'map_specular' : 'SPECULAR_COLOR', 
	'map_translucency' : 'TRANSLUCENCY',
	'map_warp' : 'WARP',
}

def exportMTex(index, mtex, use, fp):
	tex = mtex.texture
	texname = tex.name.replace(' ','_')
	mapto = None
	prio = []
	for ext in MapToTypes.keys():
		if eval("mtex.%s" % ext):
			if mapto == None:
				mapto = MapToTypes[ext]
			prio.append(ext)	
			print("Mapto", ext, mapto)
			
	fp.write("  MTex %d %s %s %s\n" % (index, texname, mtex.texture_coordinates, mapto))
	writePrio(mtex, ['texture']+prio, "    ", fp)
	print("MTEX", texname,  list(MapToTypes.keys()) )
	writeDir(mtex, list(MapToTypes.keys()) + ['texture', 'type', 'texture_coordinates', 'offset'], "    ", fp)
	print("DONE MTEX", texname)
	fp.write("  end MTex\n\n")
	return

def exportTexture(tex, fp):
	fp.write("Texture %s %s\n" % (tex.name.replace(' ', '_'), tex.type))
	if tex.type == 'IMAGE':
		fp.write("  Image %s ;\n" % tex.image.name.replace(' ', '_'))
	else:
		exportRamp(tex.color_ramp, "color_ramp", fp)
		writeDir(tex, ['color_ramp', 'image_user', 'use_nodes', 'use_textures', 'type'], "  ", fp)
	fp.write("end Texture\n\n")

def exportImage(img, fp):
	imgName = img.name.replace(' ', '_')
	if imgName == 'Render_Result':
		return
	fp.write("Image %s\n" % imgName)
	if expMsk & M_MHX:
		(path, name) = os.path.split(img.filename)
		fp.write("  *** Filename %s ;\n" % (name))
	else:
		fp.write("  Filename %s ;\n" % (img.filename))
	# writeDir(img, [], "  ", fp)
	fp.write("end Image\n\n")

def exportRamp(ramp, name, fp):
	if ramp == None:
		return
	print(ramp)
	fp.write("  Ramp %s\n" % name)
	for elt in ramp.elements:
		col = elt.color
		fp.write("    Element (%.6g,%.6g,%.6g,%.6g) %.6g ;\n" % (col[0], col[1], col[2], col[3], elt.position))
	writeDir(ramp, ['elements'], "    ", fp)
	fp.write("  end Ramp\n")


#
#	exportObject(ob, fp):
# 

def exportObject(ob, fp):
	global hairFile

	fp.write("\n# ----------------------------- %s --------------------- # \n\n" % ob.type )
	if ob.type == "MESH":
		exportMesh(ob, fp)
	elif ob.type == "ARMATURE":
		exportArmature(ob, fp)
	elif ob.type == "EMPTY":
		pass
	elif ob.type == "CURVE":
		exportCurve(ob, fp)
	elif ob.type == 'LATTICE':
		exportLattice(ob, fp)
	elif not expMsk & M_Obj:
		return
	else:
		exportRestObject(ob,fp)

	if ob.data:
		datName = ob.data.name.replace(' ','_')
	else:
		datName = 'None'
	fp.write("\nObject %s %s %s\n" % (ob.name.replace(' ', '_'), ob.type, datName))

	writeArray('layers', ob.layers, "    ", 1, fp)

	for mod in ob.modifiers:
		exportModifier(mod, fp)

	for cns in ob.constraints:
		exportConstraint(cns, fp)

	for psys in ob.particle_systems:
		if expMsk & M_MHX:
			fp.write("*** ParticleSystem\n")
			fp1 = mhxOpen(M_Part, hairFile)
			exportParticleSystem(psys, "  ", fp1)
			mhxClose(fp1)
		else:
			exportParticleSystem(psys, "  ", fp)

	print("AD", ob.animation_data)
	# exportAnimationData(ob.animation_data, fp)
	writeDir(ob, 
		['data','parent_vertices', 'mode', 'scene_users', 'children', 'pose', 
		'material_slots', 'modifiers', 'constraints', 'layers', 'bound_box', 'group_users',
		'animation_visualisation', 'animation_data', 'particle_systems', 'active_particle_system',
		'active_shape_key', 'vertex_groups', 'active_vertex_group', 'materials'], "  ", fp)
	fp.write("end Object\n\n")
	return 

#
#	exportParticleSystem(psys, pad, fp):
#	exportParticleSettings(settings, psys, pad, fp):
#	exportParticle(par, nmax, pad, fp):
#

def exportParticleSystem(psys, pad, fp):
	name = psys.name.replace(' ', '_')
	fp.write("%sParticleSystem %s %s \n" % (pad,name, psys.settings.type))
	createdLocal['ParticleSystem'].append(name)
	exportParticleSettings(psys.settings, psys, pad, fp)
	writeDir(psys,
		['settings', 'child_particles', 'particles', 'editable', 'edited', 'global_hair', 'multiple_caches'], 
		pad+"  ", fp)
	if psys.edited:
		exportParticles(psys.particles,  psys.settings.amount, pad+"  ", fp)
	fp.write("%send ParticleSystem\n" % pad)

def exportParticleSettings(settings, psys, pad, fp):
	fp.write("%ssettings Struct ParticleSettings %s \n" % (pad, settings.name.replace(' ','_')))
	if expMsk & (M_MHX+M_MHPart) == M_MHX+M_MHPart:
		fp.write("%s  *** ParticleSettings\n" % pad)
	prio = ['amount', 'hair_step', 'rendered_child_nbr', 'child_radius', 'child_random_size']
	writePrio(settings, prio, pad+"  ", fp)
	if expMsk & M_MHX:
		fp.write("%s  *** EndIgnore\n" % pad)
	writeDir(settings, prio, pad+"  ", fp)
	fp.write("%send Struct\n" % pad)

def exportParticles(particles, nmax, pad, fp):
	if expMsk & (M_MHX+M_MHPart) == M_MHX+M_MHPart:
		fp.write("%s  *** Particles\n" % pad)
	else:
		fp.write("%sParticles\n" % pad)
	n = 0
	prio = ['location']
	for par in particles:
		if n < nmax:
			fp.write("%s  Particle \n" % pad)
			for h in par.hair:
				fp.write("%s    h " % pad)
				writeTuple(h.location, fp)
				fp.write(" %d %.6g ;\n" % (h.time, h.weight))
			writePrio(par, prio, pad+"    ", fp)
			fp.write("%s  end Particle\n" % pad)
			n += 1
	if expMsk & M_MHX:
		fp.write("%s  *** EndIgnore\n" % pad)
	writeDir(particles[0], prio+['hair'], pad+"  ", fp)
	fp.write("%send Particles\n" % pad)

	
#
#	exportMesh(ob, fp):
#

def exportMesh(ob, fp):
	me = ob.data
	meName = me.name.replace(' ', '_')
	obName = ob.name.replace(' ', '_')
	if verbosity > 0:
		print( "Saving mesh "+meName )

	fp.write("Mesh %s %s \n" % (meName, obName))

	if me.verts:
		fp.write("  Verts\n")
		if expMsk & M_MHX and obName == "Human":
			fp.write("  *** Verts\n")
		else:
			for v in me.verts:
				fp.write("    v %.6g %.6g %.6g ;\n" %(v.co[0], v.co[1], v.co[2]))
		v = me.verts[0]
		#writeDir(v, ['co', 'index', 'normal'], "      ", fp)
		fp.write("  end Verts\n")

	if me.faces:
		fp.write("  Faces\n")
		for f in me.faces:
			fp.write("    f ")
			for v in f.verts:
				fp.write("%d " % v)
			fp.write(";\n")
		if len(me.materials) <= 1:
			f = me.faces[0]
			fp.write("    ftall %d %d ;\n" % (f.material_index, f.smooth))
		else:
			for f in me.faces:
				fp.write("    ft %d %d ;\n" % (f.material_index, f.smooth))
		fp.write("  end Faces\n")
	elif me.edges:
		fp.write("  Edges\n")
		for e in me.edges:
			fp.write("  e %d %d ;\n" % (e.verts[0], e.verts[1]))
		e = me.edges[0]
		writeDir(e, ['verts'], "      ", fp)
		fp.write("  end Edges\n")

	for uvtex in me.uv_textures:
		uvtexName = uvtex.name.replace(' ','_')
		fp.write("  MeshTextureFaceLayer %s\n" % uvtexName)
		fp.write("    Data \n")
		for data in uvtex.data.values():
			v = data.uv_raw
			fp.write("      vt %.6g %.6g %.6g %.6g %.6g %.6g %.6g %.6g ;\n" % (v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7]))
		writeDir(uvtex.data[0], ['uv1', 'uv2', 'uv3', 'uv4', 'uv', 'uv_raw', 'uv_pinned', 'uv_selected'], "      ", fp)
		fp.write("    end Data\n")
		writeDir(uvtex, ['data'], "    ", fp)
		createdLocal['MeshTextureFaceLayer'].append(uvtexName)
		fp.write("  end MeshTextureFaceLayer\n")
		
	for vcol in me.vertex_colors:
		vcolName = vcol.name.replace(' ','_')
		fp.write("  MeshColorLayer %s\n" % vcolName)
		if Optimize < 2:
			fp.write("    Data \n")
			for data in vcol.data.values():
				fp.write("      cv ")
				writeTuple(data.color1, fp)
				writeTuple(data.color2, fp)
				writeTuple(data.color3, fp)
				writeTuple(data.color4, fp)
				fp.write(" ;\n")
			fp.write("    end Data\n")
		writeDir(vcol, ['data'], "    ", fp)
		createdLocal['MeshColorLayer'].append(vcolName)
		fp.write("  end MeshColorLayer\n")

	"""
	for v in me.sticky:
		fp.write("  sticky %.6g %.6g\n" % (v.co[0], v.co[1]))
	"""	

	for mat in me.materials:
		fp.write("  Material %s ;\n" % mat.name.replace(" ", "_"))
	
	if expMsk & M_MHX and obName == "Human":
		fp.write("    *** VertexGroup\n")
		fp1 = mhxOpen(M_VGroup, "vertexgroups-common25.mhx")
		exportVertexGroups(ob, me, True, fp1)
		mhxClose(fp1)
		fp1 = mhxOpen(M_VGroup, "vertexgroups-%s25.mhx" % theRig)
		exportVertexGroups(ob, me, False, fp1)
		mhxClose(fp1)
	else:
		exportVertexGroups(ob, me, True, fp)
		exportVertexGroups(ob, me, False, fp)

	if me.shape_keys:
		if expMsk & M_MHX and obName == "Human":
			fp.write("    *** ShapeKey\n")
			fp1 = mhxOpen(M_Shape, "shapekeys-facial25.mhx")
			exportShapeKeys(me, fp1)
			mhxClose(fp1)
		else:
			if expMsk & M_Shape:
				exportShapeKeys(me, fp)
		 
	if verbosity > 1:
		print( "Faces saved" )

	#writePrio(me, ['vertex_colors'], "  ", fp)

	exclude = ['edge_face_count', 'edge_face_count_dict', 'edge_keys', 'edges', 'faces', 'verts', 'texspace_loc', 
		'texspace_size', 'active_uv_texture', 'active_vertex_color', 'uv_texture_clone', 'uv_texture_stencil',
		'float_layers', 'int_layers', 'string_layers', 'shape_keys', 'uv_textures', 'vertex_colors', 'materials', 
		'total_face_sel', 'total_edge_sel', 'total_vert_sel']
	writeDir(me, exclude, "  ", fp)
	fp.write("end Mesh\n")
	return # exportMesh

CommonVertGroups = [
	'Eye_L', 'Eye_R', 'Gums', 'Head', 'Jaw', 'Left', 'LoLid_L', 'LoLid_R', 'Middle', 'Right',
	'Toe-1-1_L', 'Toe-1-1_R', 'Toe-1-2_L', 'Toe-1-2_R', 
	'Toe-2-1_L', 'Toe-2-1_R', 'Toe-2-2_L', 'Toe-2-2_R', 'Toe-2-3_L', 'Toe-2-3_R', 
	'Toe-3-1_L', 'Toe-3-1_R', 'Toe-3-2_L', 'Toe-3-2_R', 'Toe-3-3_L', 'Toe-3-3_R', 
	'Toe-4-1_L', 'Toe-4-1_R', 'Toe-4-2_L', 'Toe-4-2_R', 'Toe-4-3_L', 'Toe-4-3_R', 
	'Toe-5-1_L', 'Toe-5-1_R', 'Toe-5-2_L', 'Toe-5-2_R', 'Toe-5-3_L', 'Toe-5-3_R',
	'ToungeBase', 'ToungeTip', 'UpLid_L', 'UpLid_R', 'Scalp']

def exportVertexGroups(ob, me, common, fp):
	for vg in ob.vertex_groups:
		index = vg.index
		vgName = vg.name.replace(' ','_')
		if (common and vgName in CommonVertGroups) or\
		   (not common and vgName not in CommonVertGroups):
			fp.write("  VertexGroup %s\n" % (vgName))
			for v in me.verts:
				for grp in v.groups:
					if grp.group == index:
						fp.write("    wv %d %.6g ;\n" % (v.index, grp.weight))
			fp.write("  end VertexGroup\n")
			createdLocal['VertexGroup'].append(vgName)

#
#	exportShapeKeys(me, fp
#

FacialKey = {
	"Basis" : "Sym",
	"BrowsDown" : "LR",
	"BrowsMidDown" : "Sym",
	"BrowsMidUp" : "Sym",
	"BrowsOutUp" : "LR",
	"BrowsSqueeze" : "Sym",
	"CheekUp" : "LR",
	"Frown" : "LR",
	"UpLidDown" : "LR",
	"LoLidUp" : "LR",
	"Narrow" : "LR",
	"Smile" : "LR",
	"Sneer" : "LR",
	"Squint" : "LR",
	"TongueOut" : "Sym",
	"ToungeUp" : "Sym",
	"ToungeLeft" : "Sym",
	"ToungeRight" : "Sym",
	"UpLipUp" : "LR",
	"LoLipDown" : "LR",
	"MouthOpen" : "Sym",
	"UpLipDown" : "LR",
	"LoLipUp" : "LR",
}

#
def exportShapeKeys(me, fp):
	skeys = me.shape_keys
	for skey in skeys.keys:
		skeyName = skey.name.replace(' ','_')
		try:
			lr = FacialKey[skeyName]
		except:
			if expMsk & M_MHX:
				lr = None
			else:
				lr = "Sym"
		if lr:
			fp.write("  ShapeKey %s %s\n" % (skeyName, lr))
			writeDir(skey, ['data', 'relative_key', 'frame'], "    ", fp)
			for (n,pt) in enumerate(skey.data):
				dv = pt.co - me.verts[n].co
				if dv.length > Epsilon:
					fp.write("    sv %d %.6g %.6g %.6g ;\n" %(n, dv[0], dv[1], dv[2]))
			fp.write("  end ShapeKey\n")
			print(skey)
		createdLocal['ShapeKey'].append(skeyName)

#
#	exportArmature(ob, fp):
#	exportBone(fp, n, bone):
#	exportPoseBone(fp, pb):
#

def exportArmature(ob, fp):
	amt = ob.data
	amtName = amt.name.replace(' ','_')
	obName = ob.name.replace(' ','_')
	pbones = ob.pose.bones.values()
	
	if verbosity > 0:
		print( "Saving amt "+amtName )

	bpy.context.scene.objects.active = ob
	fp.write("Armature %s %s " % (amtName, obName))

	typ = None
	ntypes = 0
	for pb in pbones:
		try:
			typ = pb['type']
			ntypes += 1
		except:
			pass
	if ntypes > 1: 
		typ = "human"

	bpy.ops.object.mode_set(mode='EDIT')
	bones = amt.edit_bones.values()

	if typ and expMsk & M_Rigify:
		fp.write("  Rigify \n")
		fp.write("  MetaRig %s ;\n" %typ)
		for bone in bones:
			writeBone(bone, fp)
			fp.write("  end Bone\n\n")
		fp.write("end Armature\n")
		bpy.ops.object.mode_set(mode='OBJECT')
		return
	else:
		fp.write("  Normal \n")
	
	for b in bones:
		if b.parent == None:
			exportBone(fp, b)
			fp.write("\n")


	# prio = ['animation_data']
	prio = []
	writePrio(amt, prio, "  ", fp)
	writeDir(amt, prio+['animation_data', 'edit_bones', 'bones'], "  ", fp)
	fp.write("end Armature\n")
	bpy.ops.object.mode_set(mode='OBJECT')

	fp.write("Pose %s \n" % (obName))	
	for pb in pbones:
		exportPoseBone(fp, pb)
	fp.write("end Pose\n")
	return # exportArmature

def writeBone(bone, fp):
	fp.write("  Bone %s \n" % (bone.name.replace(' ','_')))
	x = bone.head
	fp.write("    head %.6g %.6g %.6g ; \n" % (x[0], x[1], x[2]))
	x = bone.tail
	fp.write("    tail %.6g %.6g %.6g ; \n" % (x[0], x[1], x[2]))
	writePrio(bone, ['roll'], "    ", fp)
	return


def exportBone(fp, bone):
	flags = 0
	if expMsk & M_MHX:
		fp.write("  *** Bone %s \n" % (bone.name.replace(' ','_')))
		fp.write("    *** head ;\n")
		fp.write("    *** tail ;\n")
		fp.write("    *** roll ;\n")
	else:
		writeBone(bone, fp)

	prio = ['connected', 'deform', 'layer']
	writePrio(bone, prio, "    ", fp)
	if bone.parent:
		fp.write("    parent Refer Bone %s ;\n" % (bone.parent.name.replace(' ','_')))

	if expMsk & M_MHX == 0:
		writeDir(bone, prio + 
		['head', 'tail', 'roll', 'parent', 'head_local', 'tail_local', 'matrix_local', 'children'], 
		"    ", fp)

	fp.write("  end Bone\n\n")
	if bone.children:
		for child in bone.children:
			exportBone(fp, child)
	return

def exportPoseBone(fp, pb):
	fp.write("\n  Posebone %s \n" % (pb.name.replace(' ', '_')))
	for cns in pb.constraints:
		exportConstraint(cns, fp)
	writeArray('ik_dof', [pb.ik_dof_x, pb.ik_dof_y, pb.ik_dof_z], "    ", 1, fp)
	writeArray('ik_limit', [pb.ik_limit_x, pb.ik_limit_y, pb.ik_limit_z], "    ", 1, fp)
	writeArray('ik_max', [pb.ik_max_x, pb.ik_max_y, pb.ik_max_z], "    ", 1, fp)
	writeArray('ik_min', [pb.ik_min_x, pb.ik_min_y, pb.ik_min_z], "    ", 1, fp)
	writeArray('ik_stiffness', [pb.ik_stiffness_x, pb.ik_stiffness_y, pb.ik_stiffness_z], "    ", 1, fp)
	exclude = ['constraints', 'ik_dof_x', 'ik_dof_y', 'ik_dof_z', 
		'ik_limit_x', 'ik_limit_y', 'ik_limit_z', 
		'ik_max_x', 'ik_max_y', 'ik_max_z', 
		'ik_min_x', 'ik_min_y', 'ik_min_z', 
		'ik_stiffness_x', 'ik_stiffness_y', 'ik_stiffness_z',
		'bone_group_index','parent', 'children', 'bone', 'child', 'head', 'tail', 'has_ik']
	writeDir(pb, exclude, "    ", fp)	
	fp.write("  end Posebone\n")
	return

#
#	exportConstraint(cns, fp):
#

def exportConstraint(cns, fp):
	try:
		name = cns.name.replace(' ', '_')
	except:
		return
	fp.write("    Constraint %s %s\n" % (name, cns.type))
	writePrio(cns, ['target'], "      ", fp)
	try:
		writeArray('invert', [cns.invert_x, cns.invert_y, cns.invert_z], "      ", 2, fp)
	except:
		pass
	try:
		writeArray('use', [cns.use_x, cns.use_y, cns.use_z], "      ", 2, fp)
	except:
		pass
	writeDir(cns, [
		'invert_x', 'invert_y', 'invert_z', 'use_x', 'use_y', 'use_z',
		'disabled', 'lin_error', 'rot_error', 'target', 'type'], "      ", fp)	
	fp.write("    end Constraint\n")
	return

#
#	exportModifier(mod, fp):
#

def exportModifier(mod, fp):
	name = mod.name.replace(' ', '_')
	fp.write("    Modifier %s %s\n" % (name, mod.type))
	writeDir(mod, [], "      ", fp)	
	fp.write("    end Modifier\n")
	return

#
#	exportRestObject(ob,fp):
#

def exportRestObject(ob,fp):
	data = ob.data
	obtype = ob.type.capitalize()
	fp.write("%s %s \n" % (obtype, data.name.replace(' ', '_')))
	writeDir(data, [], "  ", fp)
	fp.write("end %s\n" % obtype)

#
#	exportCurve(ob, fp):
#	exportNurb(spl, pad, fp):
#	exportBezierPoint(bz, pad, fp):
#

def exportCurve(ob, fp):
	cu = ob.data
	cuname = cu.name.replace(' ', '_') 
	obname = ob.name.replace(' ', '_') 
	fp.write("Curve %s %s\n" % (cuname, obname))
	writeDir(cu, ['splines', 'points'], "  ", fp)
	for nurb in cu.splines:
		exportNurb(nurb, "  ", fp)
	fp.write("end Curve\n")

def exportNurb(nurb, pad, fp):
	fp.write("%sNurb\n" % pad)
	writeDir(nurb, ['bezier_points', 'points'], "    ", fp)
	for bz in nurb.bezier_points:
		fp.write("%s  bz " % pad)
		writeTuple(bz.co, fp)
		writeTuple(bz.handle1, fp)
		fp.write("%s " % bz.handle1_type)
		writeTuple(bz.handle2, fp)
		fp.write("%s ;\n" % bz.handle2_type)
	for pt in nurb.points:
		fp.write("%s  pt " % pad)
		writeTuple(pt.co, fp)
		fp.write(" ;\n")
	fp.write("%send Nurb\n" % pad)

#
#	exportLattice(ob, fp):
#

def exportLattice(ob, fp):
	lat = ob.data
	latName = lat.name.replace(' ', '_') 
	obName = ob.name.replace(' ', '_') 
	fp.write("Lattice %s %s\n" % (latName, obName))
	writeDir(lat, ['points'], "  ", fp)
	fp.write("  Points\n")
	for pt in lat.points:
		x = pt.co
		y = pt.deformed_co
		fp.write("    pt (%.6g,%.6g,%.6g) (%.6g,%.6g,%.6g) ;\n" % (x[0], x[1], x[2], y[0], y[1], y[2]))
	fp.write("  end Points\n")
	fp.write("end Lattice\n")

#
#	exportGroup(grp, fp):
#

def exportGroup(grp, fp):
	name = grp.name.replace(' ', '_') 
	fp.write("Group %s\n" % (name))
	fp.write("  Objects\n")
	for ob in grp.objects:
		fp.write("    ob %s ;\n" % ob.name.replace(' ','_'))
	fp.write("  end Objects\n")
	writeDir(grp, ['objects'], "  ", fp)
	fp.write("end Group\n")


#
#	writeHeader(fp):
#	writeMaterials(fp):
#	writeAnimations(fp):
#	writeArmatures(fp):
#	writeMeshes(fp):
#	writeTools(fp):
#	writeScenes(fp):
#

def writeHeader(fp):
	fp.write(
"# Blender 2.5 exported MHX \n" +
"MHX %d %d ;\n" % (MAJOR_VERSION, MINOR_VERSION) +
"if Blender24\n" +
"  error 'This file can only be read with Blender 2.5' ;\n" +
"end if\n")
	return

def writeMaterials(fp):
	if bpy.data.images:
		fp.write("\n# --------------- Images ----------------------------- # \n \n")
		for img in bpy.data.images:
			initLocalData()
			exportImage(img, fp)

	if bpy.data.textures:
		fp.write("\n# --------------- Textures ----------------------------- # \n \n")			
		for tex in bpy.data.textures:
			initLocalData()
			exportTexture(tex, fp)
			
	if bpy.data.materials:
		fp.write("\n# --------------- Materials ----------------------------- # \n \n")
		for mat in bpy.data.materials:
			print(mat)
			initLocalData()
			exportMaterial(mat, fp)
	return

def writeAnimations(fp):
	if bpy.data.actions:
		fp.write("\n# --------------- Actions ----------------------------- # \n \n")
		for act in bpy.data.actions:
			initLocalData()
			exportAction(act, fp)
	return

def writeArmatures(fp):
	if bpy.data.objects:		
		fp.write("\n# --------------- Armatures ----------------------------- # \n \n")
		for ob in bpy.data.objects:
			if ob.type == 'ARMATURE':
				initLocalData()
				exportObject(ob, fp)
	return

def writeMeshes(fp):
	if bpy.data.objects:		
		for ob in bpy.data.objects:
			if ob.type != 'ARMATURE':
				initLocalData()
				exportObject(ob, fp)
	if bpy.data.groups:
		fp.write("\n# ---------------- Groups -------------------------------- # \n \n")
		for grp in bpy.data.groups:
			initLocalData()
			exportGroup(grp, fp)

	return

def writeTools(fp):
	if bpy.data.brushes:
		print(bpy.data.brushes)
		for brush in bpy.data.brushes:
			initLocalData()
			exportDefault('Brush', brush, [], [], [], fp)

	if bpy.data.libraries:		
		fp.write("\n# --------------- Libraries ----------------------------- # \n \n")
		for lib in bpy.data.libraries:
			initLocalData()
			exportDefault("Library", lib, [], [], [], fp)
	return
		
def writeScenes(fp):
	if bpy.data.node_groups:		
		fp.write("\n# --------------- Node groups ----------------------------- # \n \n")
		for grp in bpy.data.node_groups:
			initLocalData()
			exportDefault("Node_group", grp, [], [], [], fp)

	if bpy.data.worlds:
		fp.write("\n# --------------- Worlds ----------------------------- # \n \n")
		for world in bpy.data.worlds:
			initLocalData()
			exportDefault("World", world, [], [], [], fp)

	if bpy.data.scenes:
		fp.write("\n# --------------- Scenes ----------------------------- # \n \n")
		for scn in bpy.data.scenes:
			initLocalData()
			exportDefault("Scene", scn, [], [], [], fp)
	return

#
#	writeMhxFile(fileName):
#	writeMhxTemplates():
#

def writeMhxFile(fileName, msk):
	global expMsk
	expMsk = msk
	print("expMsk %x %x %x" %( expMsk, M_Mat, expMsk&M_Mat))
	n = len(fileName)
	if fileName[n-3:] != "mhx":
		raise NameError("Not a mhx file: " + fileName)
	fp = open(fileName, "w")
	writeHeader(fp)
	if expMsk & M_Mat:
		writeMaterials(fp)
	if expMsk & M_Anim:
		writeAnimations(fp)
	if expMsk & M_Amt:
		writeArmatures(fp)
	if expMsk & M_Geo:
		writeMeshes(fp)
	if expMsk & M_Tool:
		writeTools(fp)
	if expMsk & M_Scn:
		writeScenes(fp)
	mhxClose(fp)
	return

def writeMhxTemplates(msk):
	global expMsk
	expMsk = msk

	fp = mhxOpen(M_Mat, "materials25.mhx")
	writeHeader(fp)
	writeMaterials(fp)
	mhxClose(fp)
	
	if expMsk & M_Geo:
		fp = mhxOpen(M_Geo, "meshes25.mhx")
		writeMeshes(fp)
		mhxClose(fp)

	if expMsk & M_Amt:
		fp = mhxOpen(M_Amt, "armatures-%s25.mhx" % theRig)
		writeArmatures(fp)
		mhxClose(fp)
	return

#
#	MakeHuman directory
#

MHXDir = '/home/thomas/svn/makehuman/data/templates/'
TrashDir = '/home/thomas/mhx5/trash/'

# MHXDir = 'C:/home/svn/data/templates/'
# TrashDir = 'C:/home/thomas/mhx5/trash/'

def mhxOpen(msk, name):
	if expMsk & msk:
		fdir = MHXDir
	else:
		fdir = TrashDir
	fileName = "%s%s" % (fdir, name)
	print( "Writing MHX file " + fileName )
	return open(fileName, 'w')

def mhxClose(fp):	
	print("%s written" % fp.name)
	fp.close()
	return

#
#	Testing
#
hairFile = "particles25.mhx"
theRig = "classic"
#writeMhxFile('/home/thomas/mhx5/test1.mhx', M_Mat+M_Geo+M_Amt+M_Obj+M_Anim)
writeMhxTemplates(M_MHX+M_Mat+M_Geo+M_Amt+M_VGroup)
#writeMhxTemplates(M_MHX+M_Part)
#theRig = "rigify"
#writeMhxTemplates(M_Geo+M_Mat+M_MHX+M_Amt+M_VGroup+M_Rigify)



