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
Version 0.1

"""

bl_addon_info = {
	'name': 'MakeHuman lipsync',
	'author': 'Thomas Larsson',
	'version': '0.1',
	'blender': (2, 53, 1),
    "api": 31683,
	"location": "UI panel",
	"description": "Lipsync for the MHX rig",
	"warning": "",
	"category": "Import/Export"}

"""
Run from text window. 
Access from UI panel (N-key) when MHX rig is active.
"""

MAJOR_VERSION = 0
MINOR_VERSION = 1
BLENDER_VERSION = (2, 53, 1)

import bpy, os, mathutils
from mathutils import *
from bpy.props import *

#
#	visemes
#

visemes = ({
	'Rest' : [('PMouth', (0,0)), ('PUpLip', (0,-0.1)), ('PLoLip', (0,0.1)), ('PJaw', (0,0.05)), ('PTongue', (0,0.0))], 
	'Etc' : [('PMouth', (0,0)), ('PUpLip', (0,-0.1)), ('PLoLip', (0,0.1)), ('PJaw', (0,0.15)), ('PTongue', (0,0.0))], 
	'MBP' : [('PMouth', (-0.3,0)), ('PUpLip', (0,1)), ('PLoLip', (0,0)), ('PJaw', (0,0.1)), ('PTongue', (0,0.0))], 
	'OO' : [('PMouth', (-1.5,0)), ('PUpLip', (0,0)), ('PLoLip', (0,0)), ('PJaw', (0,0.2)), ('PTongue', (0,0.0))], 
	'O' : [('PMouth', (-1.1,0)), ('PUpLip', (0,0)), ('PLoLip', (0,0)), ('PJaw', (0,0.5)), ('PTongue', (0,0.0))], 
	'R' : [('PMouth', (-0.9,0)), ('PUpLip', (0,-0.2)), ('PLoLip', (0,0.2)), ('PJaw', (0,0.2)), ('PTongue', (0,0.0))], 
	'FV' : [('PMouth', (0,0)), ('PUpLip', (0,0)), ('PLoLip', (0,-0.8)), ('PJaw', (0,0.1)), ('PTongue', (0,0.0))], 
	'S' : [('PMouth', (0,0)), ('PUpLip', (0,-0.2)), ('PLoLip', (0,0.2)), ('PJaw', (0,0.05)), ('PTongue', (0,0.0))], 
	'SH' : [('PMouth', (-0.6,0)), ('PUpLip', (0,-0.5)), ('PLoLip', (0,0.5)), ('PJaw', (0,0)), ('PTongue', (0,0.0))], 
	'EE' : [('PMouth', (0.3,0)), ('PUpLip', (0,-0.3)), ('PLoLip', (0,0.3)), ('PJaw', (0,0.025)), ('PTongue', (0,0.0))], 
	'AH' : [('PMouth', (-0.1,0)), ('PUpLip', (0,-0.4)), ('PLoLip', (0,0)), ('PJaw', (0,0.35)), ('PTongue', (0,0.0))], 
	'EH' : [('PMouth', (0.1,0)), ('PUpLip', (0,-0.2)), ('PLoLip', (0,0.2)), ('PJaw', (0,0.2)), ('PTongue', (0,0.0))], 
	'TH' : [('PMouth', (0,0)), ('PUpLip', (0,-0.5)), ('PLoLip', (0,0.5)), ('PJaw', (-0.2,0.1)), ('PTongue', (0,-0.6))], 
	'L' : [('PMouth', (0,0)), ('PUpLip', (0,-0.2)), ('PLoLip', (0,0.2)), ('PJaw', (0.2,0.2)), ('PTongue', (0,-0.8))], 
	'G' : [('PMouth', (0,0)), ('PUpLip', (0,-0.1)), ('PLoLip', (0,0.1)), ('PJaw', (-0.3,0.1)), ('PTongue', (0,-0.6))], 

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
#	setViseme(context, vis, setKey, frame):
#	setBoneLocation(context, pbone, loc, mirror, setKey, frame):
#

def setViseme(context, vis, setKey, frame):
	pbones = context.object.pose.bones
	for (b, (x, z)) in visemes[vis]:
		loc = mathutils.Vector((float(x),0,float(z)))
		try:
			pb = pbones[b]
		except:
			pb = None
			
		if pb:
			setBoneLocation(context, pb, loc, False, setKey, frame)
		else:
			setBoneLocation(context, pbones[b+'_L'], loc, False, setKey, frame)
			setBoneLocation(context, pbones[b+'_R'], loc, True, setKey, frame)
	return

def setBoneLocation(context, pb, loc, mirror, setKey, frame):
	scale = context.object['MhxScale']
	if mirror:
		loc[0] = -loc[0]
	pb.location = loc*scale*0.2
	if setKey or context.scene['MhxAutoKeyframe']:
		for n in range(3):
			pb.keyframe_insert('location', index=n, frame=frame, group=pb.name)
	return

#
#	openFile(context, file):
#	readMoho(context, fp, offs):
#	readMagpie(context, fp, offs):
#

def openFile(context, file):
	ob = context.object
	if ob.type != 'ARMATURE':
		raise NameError("No armature selected")
	(path, fileName) = os.path.split(file)
	(name, ext) = os.path.splitext(fileName)
	return open(file, "rU")

def readMoho(context, fp, offs):
	for line in fp:
		words= line.split()
		if len(words) < 2:
			pass
		else:
			vis = mohoVisemes[words[1]]
			setViseme(context, vis, True, int(words[0])+offs)
	return
	
def readMagpie(context, fp, offs):
	for line in fp: 
		words= line.split()
		if len(words) < 3:
			pass
		elif words[2] == 'X':
			vis = magpieVisemes[words[3]]
			setViseme(context, vis, True, int(words[0])+offs)
	return
	
#
#	User interface
#	BoolProperty
#	class MhxLipsyncPanel(bpy.types.Panel):
#

bpy.types.Scene.BoolProperty(attr="MhxAutoKeyframe", name="Auto keyframe", description="Auto keyframe", default=False)
bpy.context.scene['MhxAutoKeyframe'] = False

class MhxLipsyncPanel(bpy.types.Panel):
	bl_label = "MHX Lipsync"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	@classmethod
	def poll(cls, context):
		if context.object and context.object.type == 'ARMATURE':
			try:
				return context.object['MhxRig']
			except:
				pass
		return False

	def draw(self, context):
		layout = self.layout
		layout.prop(context.scene, 'MhxAutoKeyframe', text="Auto keyframe", icon='BLENDER', toggle=True)
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

# Define viseme buttons

def defineVisemeButtons():
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

defineVisemeButtons()

# 
#	class OBJECT_OT_LoadMohoButton(bpy.types.Operator):
#

class OBJECT_OT_LoadMohoButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_LoadMohoButton"
	bl_label = "Moho (.dat)"
	filepath = StringProperty(name="File Path", description="File path used for importing the file", maxlen= 1024, default= "")
	startFrame = IntProperty(name="Start frame", description="First frame to import", default=1)

	def execute(self, context):
		global bpy, os, mathutils
		fp = openFile(context, self.properties.filepath)		
		bpy.ops.object.mode_set(mode='POSE')	
		readMoho(context, fp, self.properties.startFrame-1)
		fp.close()
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.manager.add_fileselect(self)
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
		global bpy, os, mathutils
		fp = openFile(context, self.properties.filepath)		
		bpy.ops.object.mode_set(mode='POSE')	
		readMagpie(context, fp, self.properties.startFrame-1)
		fp.close()
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.manager.add_fileselect(self)
		return {'RUNNING_MODAL'}	


