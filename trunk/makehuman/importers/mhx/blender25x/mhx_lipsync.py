""" 
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyright(c):**	  MakeHuman Team 2001-2010

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
MHX (MakeHuman eXchange format) importer for Blender 2.5x.
Version 0.15

"""

bl_addon_info = {
	'name': 'MakeHuman lipsync',
	'author': 'Thomas Larsson',
	'version': '0.1',
	'blender': (2, 53, 1),
	"location": "File > Import",
	"description": "Lipsync for the MHX rig",
	"warning": "",
	"wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/Scripts/",
	"tracker_url": "https://projects.blender.org/tracker/index.php?func=detail&aid=21872&group_id=153&atid=469",
	"category": "Import/Export"}

"""
Place this file in the .blender/scripts/addons dir
You have to activated the script in the "Add-Ons" tab (user preferences).
Access from the File > Import menu.
"""

MAJOR_VERSION = 0
MINOR_VERSION = 1
BLENDER_VERSION = (2, 53, 1)

import bpy, mathutils, os
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

	'Blink' : [('PUpLid', (0,1.0)), ('PLoLid', (0,-0.5))], 
	'UnBlink' : [('PUpLid', (0,0)), ('PLoLid', (0,0))], 
})

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
#	setViseme(self, context, vis):
#

def setViseme(self, context, vis):
	overallScale = 0.2
	rig = context.object
	if rig.type != 'ARMATURE':
		return False
	pbones = rig.pose.bones
	for (bone, (x, z)) in self.Visemes[vis]:
		loc = self.Mathutils.Vector((float(x),0,float(z)))
		try:
			pbones[bone].location = loc*overallScale
			lr = False
		except:
			lr = True
		if lr:
			pbones[bone+"_L"].location = loc*overallScale
			loc[0] = -loc[0]
			pbones[bone+"_R"].location = loc*overallScale
	return	True

#
#	openFile(self, context, file):
#	readMoho(self, fp, ob, offs):
#	readMagpie(self, fp, ob, offs):
#	readPose(self, frame, vis, ob):
#	setBonePose(self, pb, frame, loc):
#

def openFile(self, context, file):
	ob = context.object
	if ob.type != 'ARMATURE':
		raise NameError("No armature selected")
	(path, fileName) = self.Os.path.split(file)
	(name, ext) = self.Os.path.splitext(fileName)
	return open(file, "rU")

def readMoho(self, fp, ob, offs):
	for line in fp:
		words= line.split()
		if len(words) < 2:
			pass
		else:
			vis = self.MohoVisemes[words[1]]
			self.ReadPose(int(words[0])+offs, vis, ob)
	return
	
def readMagpie(self, fp, ob, offs):
	overallScale = 0.2
	for line in fp: 
		words= line.split()
		if len(words) < 3:
			pass
		elif words[2] == 'X':
			vis = self.MagpieVisemes[words[3]]
			self.ReadPose(int(words[0])+offs, vis, ob)
	return
	
def readPose(self, frame, vis, ob):
	overallScale = 0.2
	pbones = ob.pose.bones
	for (b, (x, z)) in self.Visemes[vis]:
		loc = self.Mathutils.Vector((float(x),0,float(z)))*overallScale
		try:
			pb = pbones[b]
		except:
			pb = None
			
		if pb:
			self.SetBonePose(pb, frame, loc)
		else:
			self.SetBonePose(pbones[b+'_L'], frame, loc)
			loc[0] *= -1
			self.SetBonePose(pbones[b+'_R'], frame, loc)
	return
	
def setBonePose(self, pb, frame, loc):
	pb.location = loc
	for n in range(3):
		pb.keyframe_insert('location', index=n, frame=frame, group=pb.name)
	return

#
#	User interface
#
holder = bpy.ops.object.add(type='EMPTY')
#holder['autoKeyframe'] = BoolProperty(name="Auto keyframes", default=False)

class MhxLipsyncPanel(bpy.types.Panel):
	bl_label = "MHX Lipsync"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	#bl_options = {'REGISTER', 'UNDO'}
	
	def draw(self, context):
		global holder
		layout = self.layout
		layout.label(text="visemes")
		layout.operator("object.RestButton")
		layout.operator("object.EtcButton")
		layout.operator("object.MBPButton")
		layout.operator("object.OOButton")
		layout.operator("object.OButton")
		layout.operator("object.RButton")
		layout.operator("object.FVButton")
		layout.operator("object.SButton")
		layout.operator("object.SHButton")
		layout.operator("object.EEButton")
		layout.operator("object.AHButton")
		layout.operator("object.EHButton")
		layout.operator("object.THButton")
		layout.operator("object.LButton")
		layout.operator("object.GButton")
		layout.label(text="Other")
		layout.operator("object.BlinkButton")
		layout.operator("object.UnBlinkButton")
		layout.label(text="Load file")
		layout.operator("object.LoadMohoButton")
		layout.operator("object.LoadMagpieButton")

# Define viseme buttons

def defineVisemeButtons():
	for vis in visemes.keys():
		expr = (
"class OBJECT_OT_%sButton(bpy.types.Operator):\n" % vis+
"	bl_idname = 'OBJECT_OT_%sButton'\n" % vis+
"	bl_label = '%s'\n" % vis +	
"	SetViseme = setViseme\n" +
"	Visemes = visemes\n" +
"	Mathutils = mathutils\n" +
"\n" +
"	def invoke(self, context, event):\n" +
"		self.SetViseme(context, '%s')\n" % vis +
"		return{'FINISHED'}\n"
		)
		print(expr)
		exec(expr, globals(), locals())
	return

defineVisemeButtons()

class OBJECT_OT_LoadMohoButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_LoadMohoButton"
	bl_label = "Load Moho (.dat)"
	filepath = StringProperty(name="File Path", description="File path used for importing the file", maxlen= 1024, default= "")
	startFrame = IntProperty(name="Start frame", description="First frame to import", default=1)

	Bpy = bpy
	Os = os
	Mathutils = mathutils
	OpenFile = openFile
	ReadMoho = readMoho
	ReadPose = readPose
	SetBonePose = setBonePose
	Visemes = visemes
	MohoVisemes = mohoVisemes

	def execute(self, context):
		fp = self.OpenFile(context, self.properties.filepath)		
		self.Bpy.ops.object.mode_set(mode='POSE')	
		self.ReadMoho(fp, context.object, self.properties.startFrame-1)
		fp.close()
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.manager.add_fileselect(self)
		return {'RUNNING_MODAL'}	

class OBJECT_OT_LoadMagpieButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_LoadMagpieButton"
	bl_label = "Load Magpie (.mag)"
	filepath = StringProperty(name="File Path", description="File path used for importing the file", maxlen= 1024, default= "")
	startFrame = IntProperty(name="Start frame", description="First frame to import", default=1)

	Bpy = bpy
	Os = os
	Mathutils = mathutils
	OpenFile = openFile
	ReadMagpie = readMagpie
	ReadPose = readPose
	SetBonePose = setBonePose
	Visemes = visemes
	MagpieVisemes = magpieVisemes
	
	def execute(self, context):
		fp = self.OpenFile(context, self.properties.filepath)		
		self.Bpy.ops.object.mode_set(mode='POSE')	
		self.ReadMoho(fp, context.object, self.properties.startFrame-1)
		fp.close()
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.manager.add_fileselect(self)
		return {'RUNNING_MODAL'}	

'''		  
def menu_func(self, context):
	self.layout.operator(MhxLipsyncPanel.bl_idname, text="MakeHuman (.mhx)...")

def register():
	bpy.types.INFO_MT_file_import.append(menu_func)

def unregister():
	bpy.types.INFO_MT_file_import.remove(menu_func)

if __name__ == "__main__":
	try:
		unregister()
	except:
		pass
	register()
'''