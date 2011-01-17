""" 
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyright(c):**	  MakeHuman Team 2001-2010

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
Lipsync for the MHX rig and Blender 2.5x.
Version 0.3

"""

bl_info = {
	'name': 'MakeHuman lipsync',
	'author': 'Thomas Larsson',
	'version': '0.5',
	'blender': (2, 5, 6),
	"api": 34076,
	"location": "View3D > UI panel > MHX Mocap",
	"description": "Lipsync for the MHX rig",
	"warning": "",
	"category": "3D View"}

"""
Run from text window. 
Access from UI panel (N-key) when MHX rig is active.
"""

MAJOR_VERSION = 0
MINOR_VERSION = 5
BLENDER_VERSION = (2, 56, 0)

import bpy, os, mathutils
from mathutils import *
from bpy.props import *

theRig = None
theMesh = None

#
#	visemes
#

stopStaringVisemes = ({
	'Rest' : [
		('PMouth', (0,0)), 
		('PUpLip', (0,-0.1)), 
		('PLoLip', (0,0.1)), 
		('PJaw', (0,0.05)), 
		('PTongue', (0,0.0))], 
	'Etc' : [
		('PMouth', (0,0)),
		('PUpLip', (0,-0.1)),
		('PLoLip', (0,0.1)),
		('PJaw', (0,0.15)),
		('PTongue', (0,0.0))], 
	'MBP' : [('PMouth', (-0.3,0)),
		('PUpLip', (0,1)),
		('PLoLip', (0,0)),
		('PJaw', (0,0.1)),
		('PTongue', (0,0.0))], 
	'OO' : [('PMouth', (-1.5,0)),
		('PUpLip', (0,0)),
		('PLoLip', (0,0)),
		('PJaw', (0,0.2)),
		('PTongue', (0,0.0))], 
	'O' : [('PMouth', (-1.1,0)),
		('PUpLip', (0,0)),
		('PLoLip', (0,0)),
		('PJaw', (0,0.5)),
		('PTongue', (0,0.0))], 
	'R' : [('PMouth', (-0.9,0)),
		('PUpLip', (0,-0.2)),
		('PLoLip', (0,0.2)),
		('PJaw', (0,0.2)),
		('PTongue', (0,0.0))], 
	'FV' : [('PMouth', (0,0)),
		('PUpLip', (0,0)),
		('PLoLip', (0,-0.8)),
		('PJaw', (0,0.1)),
		('PTongue', (0,0.0))], 
	'S' : [('PMouth', (0,0)),
		('PUpLip', (0,-0.2)),
		('PLoLip', (0,0.2)),
		('PJaw', (0,0.05)),
		('PTongue', (0,0.0))], 
	'SH' : [('PMouth', (-0.6,0)),
		('PUpLip', (0,-0.5)),
		('PLoLip', (0,0.5)),
		('PJaw', (0,0)),
		('PTongue', (0,0.0))], 
	'EE' : [('PMouth', (0.3,0)),
		('PUpLip', (0,-0.3)),
		('PLoLip', (0,0.3)),
		('PJaw', (0,0.025)),
		('PTongue', (0,0.0))], 
	'AH' : [('PMouth', (-0.1,0)),
		('PUpLip', (0,-0.4)),
		('PLoLip', (0,0)),
		('PJaw', (0,0.35)),
		('PTongue', (0,0.0))], 
	'EH' : [('PMouth', (0.1,0)),
		('PUpLip', (0,-0.2)),
		('PLoLip', (0,0.2)),
		('PJaw', (0,0.2)),
		('PTongue', (0,0.0))], 
	'TH' : [('PMouth', (0,0)),
		('PUpLip', (0,-0.5)),
		('PLoLip', (0,0.5)),
		('PJaw', (-0.2,0.1)),
		('PTongue', (0,-0.6))], 
	'L' : [('PMouth', (0,0)),
		('PUpLip', (0,-0.2)),
		('PLoLip', (0,0.2)),
		('PJaw', (0.2,0.2)),
		('PTongue', (0,-0.8))], 
	'G' : [('PMouth', (0,0)),
		('PUpLip', (0,-0.1)),
		('PLoLip', (0,0.1)),
		('PJaw', (-0.3,0.1)),
		('PTongue', (0,-0.6))], 

	'Blink' : [('PUpLid', (0,1.0)), ('PLoLid', (0,-1.0))], 
	'UnBlink' : [('PUpLid', (0,0)), ('PLoLid', (0,0))], 
})

bodyLanguageVisemes = ({
	'Rest' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,-0.6)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'Etc' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,-0.4)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'MBP' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'OO' : [
		('PMouth', (-1.0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0.4)), 
		('PTongue', (0,0))], 
	'O' : [
		('PMouth', (-0.9,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0.8)), 
		('PTongue', (0,0))], 
	'R' : [
		('PMouth', (-0.5,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.2)), 
		('PLoLipMid', (0,0.2)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'FV' : [
		('PMouth', (-0.2,0)), 
		('PMouthMid', (0,1.0)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (-0.6,-0.3)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'S' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.5)), 
		('PLoLipMid', (0,0.7)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'SH' : [
		('PMouth', (-0.8,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-1.0)), 
		('PLoLipMid', (0,1.0)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'EE' : [
		('PMouth', (0.2,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.6)), 
		('PLoLipMid', (0,0.6)), 
		('PJaw', (0,0.05)), 
		('PTongue', (0,0))], 
	'AH' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.4)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0.7)), 
		('PTongue', (0,0))], 
	'EH' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.5)), 
		('PLoLipMid', (0,0.6)), 
		('PJaw', (0,0.25)), 
		('PTongue', (0,0))], 
	'TH' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0.2)), 
		('PTongue', (1.0,1.0))], 
	'L' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.5)), 
		('PLoLipMid', (0,0.5)), 
		('PJaw', (0,-0.2)), 
		('PTongue', (1.0,1.0))], 
	'G' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.5)), 
		('PLoLipMid', (0,0.5)), 
		('PJaw', (0,-0.2)), 
		('PTongue', (-1.0,0))], 

	'Blink' : [('PUpLid', (0,1.0)), ('PLoLid', (0,-1.0))], 
	'UnBlink' : [('PUpLid', (0,0)), ('PLoLid', (0,0))], 
})

#
#	mohoVisemes
#	magpieVisemes
#

mohoVisemes = dict({
	'rest' : 'Rest', 
	'etc' : 'Etc', 
	'AI' : 'AH', 
	'O' : 'O', 
	'U' : 'OO', 
	'WQ' : 'AH', 
	'L' : 'L', 
	'E' : 'EH', 
	'MBP' : 'MBP', 
	'FV' : 'FV', 
})

magpieVisemes = dict({
	"CONS" : "t,d,k,g,T,D,s,z,S,Z,h,n,N,j,r,tS", 
	"AI" : "i,&,V,aU,I,0,@,aI", 
	"E" : "eI,3,e", 
	"O" : "O,@U,oI", 
	"UW" : "U,u,w", 
	"MBP" : "m,b,p", 
	"L" : "l", 
	"FV" : "f,v", 
	"Sh" : "dZ", 
})

#
#	Expressions - the same as in read_expression.py
#

Expressions = [
	'smile',
	'hopeful',
	'innocent',
	'tender',
	'seductive',

	'grin',
	'excited',
	'ecstatic',

	'proud',
	'pleased',
	'amused',
	'laughing1',
	'laughing2',

	'so-so',
	'blue',
	'depressed',
	'sad',
	'distressed',
	'crying',
	'pain',

	'disappointed',
	'frustrated',
	'stressed',
	'worried',
	'scared',
	'terrified',

	'shy',
	'guilty',
	'embarassed',
	'relaxed',
	'peaceful',
	'refreshed',

	'lazy',
	'bored',
	'tired',
	'drained',
	'sleepy',
	'groggy',

	'curious',
	'surprised',
	'impressed',
	'puzzled',
	'shocked',
	'frown',
	'upset',
	'angry',
	'enraged',

	'skeptical',
	'vindictive',
	'pout',
	'furious',
	'grumpy',
	'arrogant',
	'sneering',
	'haughty',
	'disgusted',
]

#
#	setViseme(context, vis, setKey, frame):
#	setBoneLocation(context, pbone, loc, mirror, setKey, frame):
#

def getVisemeSet(context):
	if context.scene['MhxBodyLanguage'] == True:
		return bodyLanguageVisemes
	else:
		return stopStaringVisemes

def setViseme(context, vis, setKey, frame):
	global theRig
	pbones = theRig.pose.bones
	try:
		scale = pbones['PFace'].bone.length
	except:
		return
	visemes = getVisemeSet(context)
	for (b, (x, z)) in visemes[vis]:
		loc = mathutils.Vector((float(x),0,float(z)))
		try:
			pb = pbones[b]
		except:
			pb = None
			
		if pb:
			setBoneLocation(context, pb, scale, loc, False, setKey, frame)
		else:
			setBoneLocation(context, pbones[b+'_L'], scale, loc, False, setKey, frame)
			setBoneLocation(context, pbones[b+'_R'], scale, loc, True, setKey, frame)
	return

def setBoneLocation(context, pb, scale, loc, mirror, setKey, frame):
	if mirror:
		loc[0] = -loc[0]
	pb.location = loc*scale*0.2
	if setKey or context.scene['MhxSyncAutoKeyframe']:
		for n in range(3):
			pb.keyframe_insert('location', index=n, frame=frame, group=pb.name)
	return

#
#	openFile(context, filepath):
#	readMoho(context, filepath, offs):
#	readMagpie(context, filepath, offs):
#

def openFile(context, filepath):
	(path, fileName) = os.path.split(filepath)
	(name, ext) = os.path.splitext(fileName)
	return open(filepath, "rU")

def readMoho(context, filepath, offs):
	context.scene.objects.active = theRig
	bpy.ops.object.mode_set(mode='POSE')	
	fp = openFile(context, filepath)		
	for line in fp:
		words= line.split()
		if len(words) < 2:
			pass
		else:
			vis = mohoVisemes[words[1]]
			setViseme(context, vis, True, int(words[0])+offs)
	fp.close()
	setInterpolation(context.object)
	print("Moho file %s loaded" % filepath)
	return

def readMagpie(context, filepath, offs):
	context.scene.objects.active = theRig
	bpy.ops.object.mode_set(mode='POSE')	
	fp = openFile(context, filepath)		
	for line in fp: 
		words= line.split()
		if len(words) < 3:
			pass
		elif words[2] == 'X':
			vis = magpieVisemes[words[3]]
			setViseme(context, vis, True, int(words[0])+offs)
	fp.close()
	setInterpolation(context.object)
	print("Magpie file %s loaded" % filepath)
	return

#
#	setInterpolation(rig):
#

def setInterpolation(rig):
	if not rig.animation_data:
		return
	act = rig.animation_data.action
	if not act:
		return
	for fcu in act.fcurves:
		for pt in fcu.keyframe_points:
			pt.interpolation = 'LINEAR'
		fcu.extrapolation = 'CONSTANT'
	return
	
###################################################################################	
#	User interface
#
#	initInterface()
#

def initInterface(scn):
	bpy.types.Scene.MhxSyncAutoKeyframe = BoolProperty(
		name="Auto keyframe", 
		description="Auto keyframe",
		default=False)

	bpy.types.Scene.MhxBodyLanguage = BoolProperty(
		name="Body Language", 
		description="Use Body Language shapekey set",
		default=True)		

	if scn:
		scn['MhxSyncAutoKeyframe'] = False
		scn['MhxBodyLanguage'] = True
	return

#
#	class MhxLipsyncPanel(bpy.types.Panel):
#

class MhxLipsyncPanel(bpy.types.Panel):
	bl_label = "MHX Lipsync"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	@classmethod
	def poll(cls, context):
		return context.object

	def draw(self, context):
		global theRig, theMesh, theScale	
		if context.object.type == 'ARMATURE':
			theRig = context.object
			theMesh = None
			for child in theRig.children:
				if (child.type == 'MESH' and meshHasExpressions(child)):
					theMesh = child
					break
		elif context.object.type == 'MESH':
			if meshHasExpressions(context.object):
				theMesh = context.object
				theRig = theMesh.parent
			else:
				return
		else:
			return
		
		layout = self.layout
		layout.operator("object.InitInterfaceButton")
		
		if theRig:
			layout.separator()
			layout.prop(context.scene, 'MhxSyncAutoKeyframe')
			layout.prop(context.scene, 'MhxBodyLanguage')
			layout.label(text="Visemes")
			row = layout.row()
			row.operator("object.RestButton")
			row.operator("object.EtcButton")
			row.operator("object.AHButton")
			row = layout.row()
			row.operator("object.MBPButton")
			row.operator("object.OOButton")
			row.operator("object.OButton")
			row = layout.row()
			row.operator("object.RButton")
			row.operator("object.FVButton")
			row.operator("object.SButton")
			row = layout.row()
			row.operator("object.SHButton")
			row.operator("object.EEButton")
			row.operator("object.EHButton")
			row = layout.row()
			row.operator("object.THButton")
			row.operator("object.LButton")
			row.operator("object.GButton")
			layout.separator()
			row = layout.row()
			row.operator("object.BlinkButton")
			row.operator("object.UnBlinkButton")
			layout.label(text="Load file")
			row = layout.row()
			row.operator("object.LoadMohoButton")
			row.operator("object.LoadMagpieButton")

		if theRig and rigHasExpressions(theRig):
			layout.separator()
			layout.label(text="Expressions (driven)")
			layout.operator("object.ResetBoneExpressionsButton")
			layout.separator()
			pbones = theRig.pose.bones
			for name in Expressions:
				try:
					pb = pbones['P%s' % name]
					layout.prop(pb, 'location', index=1, text=name)
				except:
					pass
		
		elif theMesh and meshHasExpressions(theMesh):	
			layout.separator()
			layout.label(text="Expressions")
			layout.operator("object.ResetExpressionsButton")
			layout.operator("object.CreateDriversButton")
			layout.separator()
			keys = theMesh.data.shape_keys
			if keys:
				for name in Expressions:
					try:
						datum = keys.keys[name]
						layout.prop(datum, 'value', text=name)
					except:
						pass
		return

# Define viseme buttons

def defineVisemeButtons():
	visemes = bodyLanguageVisemes
	for vis in visemes.keys():
		expr = (
"class OBJECT_OT_%sButton(bpy.types.Operator):\n" % vis+
"	bl_idname = 'OBJECT_OT_%sButton'\n" % vis+
"	bl_label = '%s'\n" % vis +	
"	def invoke(self, context, event):\n" +
"		global bpy, mathutils\n" +
"		setViseme(context, '%s', False, context.scene.frame_current)\n" % vis +
"		return{'FINISHED'}\n"
		)
		# print(expr)
		exec(expr, globals(), locals())
	return

#
#	class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
#

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_InitInterfaceButton"
	bl_label = "Initialize"

	def execute(self, context):
		import bpy
		initInterface(context.scene)
		print("Interface initialized")
		return{'FINISHED'}	

# 
#	class OBJECT_OT_LoadMohoButton(bpy.types.Operator):
#

class OBJECT_OT_LoadMohoButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_LoadMohoButton"
	bl_label = "Moho (.dat)"
	filepath = StringProperty(name="File Path", description="File path used for importing the file", maxlen= 1024, default= "")
	startFrame = IntProperty(name="Start frame", description="First frame to import", default=1)

	def execute(self, context):
		import bpy, os, mathutils
		readMoho(context, self.properties.filepath, self.properties.startFrame-1)		
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}	

#
#	class OBJECT_OT_LoadMagpieButton(bpy.types.Operator):
#

class OBJECT_OT_LoadMagpieButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_LoadMagpieButton"
	bl_label = "Magpie (.mag)"
	filepath = StringProperty(name="File Path", description="File path used for importing the file", maxlen= 1024, default= "")
	startFrame = IntProperty(name="Start frame", description="First frame to import", default=1)

	def execute(self, context):
		import bpy, os, mathutils
		readMagpie(context, self.properties.filepath, self.properties.startFrame-1)		
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}	


#
#	meshHasExpressions(mesh):
#	rigHasExpressions(rig):
#
	
def meshHasExpressions(mesh):
	return ('guilty' in mesh.data.shape_keys.keys.keys())

def rigHasExpressions(rig):
	return ('Pguilty' in rig.pose.bones.keys())

#
#	class OBJECT_OT_ResetExpressionsButton(bpy.types.Operator):
#

class OBJECT_OT_ResetExpressionsButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_ResetExpressionsButton"
	bl_label = "Reset expressions"

	def execute(self, context):
		global theMesh
		keys = theMesh.data.shape_keys
		if keys:
			for name in Expressions:
				try:
					keys.keys[name].value = 0.0
				except:
					pass
		print("Expressions reset")
		return{'FINISHED'}	

#
#	class OBJECT_OT_ResetBoneExpressionsButton(bpy.types.Operator):
#

class OBJECT_OT_ResetBoneExpressionsButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_ResetBoneExpressionsButton"
	bl_label = "Reset expressions"

	def execute(self, context):
		global theRig
		pbones = theRig.pose.bones
		if pbones:
			for name in Expressions:
				try:
					pb = pbones['P%s' % name]
					pb.location[1] = 0.0
				except:
					pass
		print("Expressions reset")
		return{'FINISHED'}
		
#
#	createDrivers(context):	
#
#	class OBJECT_OT_CreateDriversButton(bpy.types.Operator):
#

def createDrivers(context):		
	global theMesh, theRig
	keys = theMesh.data.shape_keys
	if keys:
		context.scene.objects.active = theRig
		bpy.ops.object.mode_set(mode = 'EDIT')
		ebones = theRig.data.edit_bones		
		pface = ebones['PFace']
		layers = 32*[False]
		layers[31] = True
		
		for name in Expressions:
			eb = ebones.new("P%s" % name)
			eb.head = pface.head
			eb.tail = pface.tail
			eb.parent = pface
			eb.layers = layers

		bpy.ops.object.mode_set(mode = 'POSE')
		for name in Expressions:			
			try:
				createDriver(name, keys)
			except:
				pass
	return
				
def createDriver(name, keys):
	global theRig
	print("Create driver %s" % name)
	fcu = keys.keys[name].driver_add('value')

	drv = fcu.driver
	drv.type = 'AVERAGE'
	drv.show_debug_info = True

	var = drv.variables.new()
	var.name = 'x'
	var.type = 'TRANSFORMS'
	
	trg = var.targets[0]
	trg.id = theRig
	trg.transform_type = 'LOC_Y'
	trg.bone_target = 'P%s' % name
	trg.use_local_space_transform = True
	
	#fmod = fcu.modifiers.new('GENERATOR')
	fmod = fcu.modifiers[0]
	fmod.coefficients = (0, 1.0)
	fmod.show_expanded = True
	fmod.mode = 'POLYNOMIAL'
	fmod.mute = False
	fmod.poly_order = 1

	return
	
class OBJECT_OT_CreateDriversButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_CreateDriversButton"
	bl_label = "Create drivers"

	def execute(self, context):
		createDrivers(context)
		print("Drivers created")
		return{'FINISHED'}	

#
#	initialize and register
#

initInterface(bpy.context.scene)
defineVisemeButtons()

def register():
	pass

def unregister():
	pass

if __name__ == "__main__":
	register()


