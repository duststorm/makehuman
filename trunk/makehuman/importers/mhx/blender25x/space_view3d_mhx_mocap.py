# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_addon_info = {
	"name": "MHX Mocap",
	"author": "Thomas Larsson",
	"version": "0.5",
	"blender": (2, 5, 5),
	"api": 32930,
	"location": "View3D > Properties > MHX Mocap",
	"description": "Mocap tool for MHX rig",
	"warning": "",
	"category": "3D View"}

"""
Run from text window. 
Access from UI panel (N-key) when MHX rig is active.

Properties:
Scale:	
	for BVH import. Choose scale so that the vertical distance between hands and feet
	are the same for MHX and BVH rigs.
	Good values are: CMU: 0.6, OSU: 0.1
Start frame:	
	for BVH import
Rot90:	
	for BVH import. Rotate armature 90 degrees, so Z points up.
Simplify FCurves:	
	Include FCurve simplifcation.
Max loc error:	
	Max error allowed for simplification of location FCurves
Max rot error:	
	Max error allowed for simplification of rotation FCurves

Buttons:
Load BVH file (.bvh): 
	Load bvh file with Z up
Silence constraints:
	Turn off constraints that may conflict with mocap data.
Retarget selected to MHX: 
	Retarget actions of selected BVH rigs to the active MHX rig.
Simplify FCurves:
	Simplifiy FCurves of active action, allowing max errors specified above.
Load, retarget, simplify:
	Load bvh file, retarget the action to the active MHX rig, and simplify FCurves.
Batch run:
	Load all bvh files in the given directory, whose name start with the
	given prefix, and create actions (with simplified FCurves) for the active MHX rig.
"""

MAJOR_VERSION = 0
MINOR_VERSION = 2
BLENDER_VERSION = (2, 54, 0)

import bpy, os, mathutils, math, time
from mathutils import *
from bpy.props import *

###################################################################################
#	BVH importer. 
#	The importer that comes with Blender had memory leaks which led to instability.
#	It also creates a weird skeleton from CMU data, with hands theat start at the wrist
#	and ends at the elbow.
#

#
#	class CNode:
#

class CNode:
	def __init__(self, words, parent):
		name = words[1]
		for word in words[2:]:
			name += ' '+word
		
		self.name = name
		self.parent = parent
		self.children = []
		self.head = Vector((0,0,0))
		self.offset = Vector((0,0,0))
		if parent:
			parent.children.append(self)
		self.channels = []
		self.matrix = None
		self.inverse = None
		return

	def __repr__(self):
		return "CNode %s" % (self.name)

	def display(self, pad):
		vec = self.offset
		if vec.length < Epsilon:
			c = '*'
		else:
			c = ' '
		print("%s%s%10s (%8.3f %8.3f %8.3f)" % (c, pad, self.name, vec[0], vec[1], vec[2]))
		for child in self.children:
			child.display(pad+"  ")
		return

	def build(self, amt, orig, parent):
		self.head = orig + self.offset
		if not self.children:
			return self.head
		
		zero = (self.offset.length < Epsilon)
		eb = amt.edit_bones.new(self.name)		
		if parent:
			eb.parent = parent
		eb.head = self.head
		tails = Vector((0,0,0))
		for child in self.children:
			tails += child.build(amt, self.head, eb)
		n = len(self.children)
		eb.tail = tails/n
		self.matrix = eb.matrix.rotation_part()
		self.inverse = self.matrix.copy().invert()
		if zero:
			return eb.tail
		else:		
			return eb.head

#
#	readBvhFile(context, filepath, scn):
#	Custom importer
#

Location = 1
Rotation = 2
Hierarchy = 1
Motion = 2
Frames = 3

Deg2Rad = math.pi/180
Epsilon = 1e-5

def readBvhFile(context, filepath, scn):
	scale = scn['MhxBvhScale']
	startFrame = scn['MhxStartFrame']
	endFrame = scn['MhxEndFrame']
	rot90 = scn['MhxRot90Anim']
	subsample = scn['MhxSubsample']
	defaultSS = scn['MhxDefaultSS']
	print(filepath)
	fileName = os.path.realpath(os.path.expanduser(filepath))
	(shortName, ext) = os.path.splitext(fileName)
	if ext.lower() != ".bvh":
		raise NameError("Not a bvh file: " + fileName)
	print( "Loading BVH file "+ fileName )

	time1 = time.clock()
	level = 0
	nErrors = 0
	scn = context.scene
			
	fp = open(fileName, "rU")
	print( "Reading skeleton" )
	lineNo = 0
	for line in fp: 
		words= line.split()
		lineNo += 1
		if len(words) == 0:
			continue
		key = words[0].upper()
		if key == 'HIERARCHY':
			status = Hierarchy
		elif key == 'MOTION':
			if level != 0:
				raise NameError("Tokenizer out of kilter %d" % level)	
			amt = bpy.data.armatures.new("BvhAmt")
			rig = bpy.data.objects.new("BvhRig", amt)
			scn.objects.link(rig)
			scn.objects.active = rig
			bpy.ops.object.mode_set(mode='EDIT')
			root.build(amt, Vector((0,0,0)), None)
			#root.display('')
			bpy.ops.object.mode_set(mode='OBJECT')
			status = Motion
			print("Reading motion")
		elif status == Hierarchy:
			if key == 'ROOT':	
				node = CNode(words, None)
				root = node
				nodes = [root]
			elif key == 'JOINT':
				node = CNode(words, node)
				nodes.append(node)
			elif key == 'OFFSET':
				(x,y,z) = (float(words[1]), float(words[2]), float(words[3]))
				if rot90:					
					node.offset = scale*Vector((x,-z,y))
				else:
					node.offset = scale*Vector((x,y,z))
			elif key == 'END':
				node = CNode(words, node)
			elif key == 'CHANNELS':
				oldmode = None
				for word in words[2:]:
					if rot90:
						(index, mode, sign) = channelZup(word)
					else:
						(index, mode, sign) = channelYup(word)
					if mode != oldmode:
						indices = []
						node.channels.append((mode, indices))
						oldmode = mode
					indices.append((index, sign))
			elif key == '{':
				level += 1
			elif key == '}':
				level -= 1
				node = node.parent
			else:
				raise NameError("Did not expect %s" % words[0])
		elif status == Motion:
			if key == 'FRAMES:':
				nFrames = int(words[1])
			elif key == 'FRAME' and words[1].upper() == 'TIME:':
				frameTime = float(words[2])
				frameFactor = int(1.0/(25*frameTime) + 0.49)
				if defaultSS:
					subsample = frameFactor
				status = Frames
				frame = 0
				frameno = 1
				bpy.ops.object.mode_set(mode='POSE')
				pbones = rig.pose.bones
				for pb in pbones:
					pb.rotation_mode = 'QUATERNION'
		elif status == Frames:
			if (frame >= startFrame and
				frame <= endFrame and
				frame % subsample == 0):
				addFrame(words, frameno, nodes, pbones, scale)
				if frameno % 200 == 0:
					print(frame)
				frameno += 1
			frame += 1

	fp.close()
	setInterpolation(rig)
	time2 = time.clock()
	print("Bvh file loaded in %.3f s" % (time2-time1))
	return rig

#
#	addFrame(words, frame, nodes, pbones, scale):
#

def addFrame(words, frame, nodes, pbones, scale):
	m = 0
	first = True
	for node in nodes:
		name = node.name
		try:
			pb = pbones[name]
		except:
			pb = None
		if pb:
			for (mode, indices) in node.channels:
				if mode == Location:
					vec = Vector((0,0,0))
					for (index, sign) in indices:
						vec[index] = sign*float(words[m])
						m += 1
					if first:
						pb.location = (scale * vec - node.head) * node.inverse
						for n in range(3):
							pb.keyframe_insert('location', index=n, frame=frame, group=name)
					first = False
				elif mode == Rotation:
					mats = []
					for (axis, sign) in indices:
						angle = sign*float(words[m])*Deg2Rad
						mats.append(Matrix.Rotation(angle, 3, axis))
						m += 1
					mat = node.inverse * mats[0] * mats[1] * mats[2] * node.matrix
					pb.rotation_quaternion = mat.to_quat()
					for n in range(4):
						pb.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=name)
	return

#
#	channelYup(word):
#	channelZup(word):
#

def channelYup(word):
	if word == 'Xrotation':
		return ('X', Rotation, +1)
	elif word == 'Yrotation':
		return ('Y', Rotation, +1)
	elif word == 'Zrotation':
		return ('Z', Rotation, +1)
	elif word == 'Xposition':
		return (0, Location, +1)
	elif word == 'Yposition':
		return (1, Location, +1)
	elif word == 'Zposition':
		return (2, Location, +1)

def channelZup(word):
	if word == 'Xrotation':
		return ('X', Rotation, +1)
	elif word == 'Yrotation':
		return ('Z', Rotation, +1)
	elif word == 'Zrotation':
		return ('Y', Rotation, -1)
	elif word == 'Xposition':
		return (0, Location, +1)
	elif word == 'Yposition':
		return (2, Location, +1)
	elif word == 'Zposition':
		return (1, Location, -1)

#
# 	end Bvh importer
###################################################################################

###################################################################################
#
#	Supported armatures

#
#	OsuArmature
#	www.accad.osu.edu/research/mocap/mocap_data.htm
#

OsuArmature = {
	'hips' : 'Root',
	'tospine' : 'Spine1',
	'spine' : 'Spine2',
	'spine1' : 'Spine3', 
	'neck' : 'Neck', 
	'head' : 'Head', 

	'leftshoulder' : 'Shoulder_L',
	'leftarm' : 'UpArmFK_L', 
	'leftforearm' : 'LoArmFK_L',
	'lefthand' : 'HandFK_L', 

	'rightshoulder' : 'Shoulder_R',
	'rightarm' : 'UpArmFK_R', 
	'rightforearm' : 'LoArmFK_R',
	'righthand' : 'HandFK_R',

	'leftupleg' : 'UpLegFK_L', 
	'leftleg' : 'LoLegFK_L', 
	'leftfoot' : 'FootFK_L', 
	'lefttoebase' : 'ToeFK_L',

	'rightupleg' : 'UpLegFK_R',
	'rightleg' : 'LoLegFK_R', 
	'rightfoot' : 'FootFK_R', 
	'righttoebase' : 'ToeFK_R',
}

#
#	MBArmature
#

MBArmature = {
	'hips' : 'Root', 
	'lowerback' : 'Spine1',
	'spine' : 'Spine2', 
	'spine1' : 'Spine3',
	'neck' : 'Neck',
	'neck1' : 'Head', 
	'head' : None,

	'leftshoulder' : 'Shoulder_L',
	'leftarm' : 'UpArmFK_L', 
	'leftforearm' : 'LoArmFK_L',
	'lefthand' : 'HandFK_L',
	'lefthandindex1' : None,
	'leftfingerbase' : None,
	'lfingers' : None,
	'lthumb' : None, 

	'rightshoulder' : 'Shoulder_R', 
	'rightarm' : 'UpArmFK_R', 
	'rightforearm' : 'LoArmFK_R',
	'righthand' : 'HandFK_R',
	'righthandindex1' : None,
	'rightfingerbase' : None,
	'rfingers' : None,
	'rthumb' : None, 

	'lhipjoint' : 'Hip_L', 
	'leftupleg' : 'UpLegFK_L',
	'leftleg' : 'LoLegFK_L', 
	'leftfoot' : 'FootFK_L', 
	'lefttoebase' : 'ToeFK_L',

	'rhipjoint' : 'Hip_R', 
	'rightupleg' : 'UpLegFK_R',
	'rightleg' : 'LoLegFK_R', 
	'rightfoot' : 'FootFK_R', 
	'righttoebase' : 'ToeFK_R',
}

#
#	Xx1Armature
#

Xx1Armature = {
	'hip' : 'Root', 
	'abdomen' : 'Spine1',
	'chest' : 'Spine3',
	'neck' : 'Neck',
	'head' : 'Head', 
	'left eye' : None,
	'right eye' : None,

	'left collar' : 'Shoulder_L',
	'left shoulder' : 'UpArmFK_L', 
	'left forearm' : 'LoArmFK_L',
	'left hand' : 'HandFK_L',
	'left thumb 1' : None, 
	'left thumb 2' : None, 
	'left thumb 3' : None, 
	'left index 1' : None, 
	'left index 2' : None, 
	'left index 3' : None, 
	'left mid 1' : None, 
	'left mid 2' : None, 
	'left mid 3' : None, 
	'left ring 1' : None, 
	'left ring 2' : None, 
	'left ring 3' : None, 
	'left pinky 1' : None, 
	'left pinky 2' : None, 
	'left pinky 3' : None, 

	'right collar' : 'Shoulder_R',
	'right shoulder' : 'UpArmFK_R', 
	'right forearm' : 'LoArmFK_R',
	'right hand' : 'HandFK_R',
	'right thumb 1' : None, 
	'right thumb 2' : None, 
	'right thumb 3' : None, 
	'right index 1' : None, 
	'right index 2' : None, 
	'right index 3' : None, 
	'right mid 1' : None, 
	'right mid 2' : None, 
	'right mid 3' : None, 
	'right ring 1' : None, 
	'right ring 2' : None, 
	'right ring 3' : None, 
	'right pinky 1' : None, 
	'right pinky 2' : None, 
	'right pinky 3' : None, 

	'left thigh' : 'UpLegFK_L',
	'left shin' : 'LoLegFK_L', 
	'left foot' : 'FootFK_L', 
	'left toe' : 'ToeFK_L',

	'right thigh' : 'UpLegFK_R',
	'right shin' : 'LoLegFK_R', 
	'right foot' : 'FootFK_R', 
	'right toe' : 'ToeFK_R',
}

MocapDataArmature = {
	'hips' : 'Root',
	'lefthip' : 'UpLegFK_L',
	'leftknee' : 'LoLegFK_L',
	'leftankle' : 'FootFK_L',
	'righthip' : 'UpLegFK_R',
	'rightknee' : 'LoLegFK_R',
	'rightankle' : 'FootFK_R',
	'chest' : 'Spine2',
	'chest2' : 'Spine3',
	'cs_bvh' : 'Spine3',
	'leftcollar' : 'Shoulder_L',
	'leftshoulder' : 'UpArmFK_L',
	'leftelbow' : 'LoArmFK_L',
	'leftwrist' : 'HandFK_L',
	'rightcollar' : 'Shoulder_R',
	'rightshoulder' : 'UpArmFK_R',
	'rightelbow' : 'LoArmFK_R',
	'rightwrist' : 'HandFK_R',
	'neck' : 'Neck',
	'head' : 'Head',
}

DazArmature = {
	'hip' : 'Root', 
	'abdomen' : 'Spine1',

	'chest' : 'Spine3',
	'neck' : 'Neck',
	'head' : 'Head', 
	'lefteye' : None,
	'righteye' : None,
	'figurehair' : None,

	'lcollar' : 'Shoulder_L',
	'lshldr' : 'UpArmFK_L', 
	'lforearm' : 'LoArmFK_L',
	'lhand' : 'HandFK_L',
	'lthumb1' : None, 
	'lthumb2' : None, 
	'lthumb3' : None, 
	'lindex1' : None, 
	'lindex2' : None, 
	'lindex3' : None, 
	'lmid1' : None, 
	'lmid2' : None, 
	'lmid3' : None, 
	'lring1' : None, 
	'lring2' : None, 
	'lring3' : None, 
	'lpinky1' : None, 
	'lpinky2' : None, 
	'lpinky3' : None, 

	'rcollar' : 'Shoulder_R',
	'rshldr' : 'UpArmFK_R', 
	'rforearm' : 'LoArmFK_R',
	'rhand' : 'HandFK_R',
	'rthumb1' : None, 
	'rthumb2' : None, 
	'rthumb3' : None, 
	'rindex1' : None, 
	'rindex2' : None, 
	'rindex3' : None, 
	'rmid1' : None, 
	'rmid2' : None, 
	'rmid3' : None, 
	'rring1' : None, 
	'rring2' : None, 
	'rring3' : None, 
	'rpinky1' : None, 
	'rpinky2' : None, 
	'rpinky3' : None, 

	'lbuttock' : 'Hip_L',
	'lthigh' : 'UpLegFK_L',
	'lshin' : 'LoLegFK_L', 
	'lfoot' : 'FootFK_L', 
	'ltoe' : 'ToeFK_L',

	'rbuttock' : 'Hip_R',
	'rthigh' : 'UpLegFK_R',
	'rshin' : 'LoLegFK_R', 
	'rfoot' : 'FootFK_R', 
	'rtoe' : 'ToeFK_R',
}

theArmatures = {
	'MB' : MBArmature, 
	'OSU' : OsuArmature,
	'XX1' : Xx1Armature,
	'McpD' : MocapDataArmature,
	'Daz' : DazArmature,
}

MBFixes = {
	'UpLegFK_L' : (Matrix.Rotation(-0.32, 3, 'Z'), None),
	'UpLegFK_R' : (Matrix.Rotation(0.32, 3, 'Z'), None),
	'UpArmFK_L' : (Matrix.Rotation(0.1, 3, 'X'), None),
	'UpArmFK_R' : (Matrix.Rotation(0.1, 3, 'X'), None),
}

OsuFixes = {}

XX1Fixes = {}

McpdFixes = {
	'Spine2' : (Matrix.Rotation(0.3, 3, 'X'), None),
	'UpArmFK_L' :  (Matrix.Rotation(1.57, 3, 'Z'), 'XZ'),
	'LoArmFK_L' :  (None, 'XZ'),
	'HandFK_L' :  (None, 'XZ'),
	'UpArmFK_R' :  (Matrix.Rotation(-1.57, 3, 'Z'), 'ZX'),
	'LoArmFK_R' :  (None, 'ZX'),
	'HandFK_R' :  (None, 'ZX'),
}

DazFixes = {}

FixesList = {
	'MB'  : MBFixes,
	'OSU' : OsuFixes,
	'XX1' : XX1Fixes,
	'McpD': McpdFixes,
	'Daz' : DazFixes,
}

#
#	end supported armatures
###################################################################################

theArmature = None

FkBoneList = [
	'Root', 'Hips', 'Spine1', 'Spine2', 'Spine3', 'Neck', 'Head',
	'Shoulder_L', 'UpArmFK_L', 'LoArmFK_L', 'HandFK_L', 'ElbowPTFK_L',
	'Shoulder_R', 'UpArmFK_R', 'LoArmFK_R', 'HandFK_R', 'ElbowPTFK_R',
	'Hip_L', 'UpLegFK_L', 'LoLegFK_L', 'FootFK_L', 'ToeFK_L',
	'Hip_R', 'UpLegFK_R', 'LoLegFK_R', 'FootFK_R', 'ToeFK_R',
	'LegFK_L', 'AnkleFK_L', 'KneePTFK_L',
	'LegFK_R', 'AnkleFK_R', 'KneePTFK_R',
]

F_Rev = 1
F_LR = 2

IkArmature = {
	'UpArmIK' : ('UpArmFK', F_LR, 'Shoulder'),
	'LoArmIK' : ('LoArmFK', F_LR, 'UpArmIK'),
	'HandIK' : ('HandFK', 0, None),
	'ElbowPTIK' : ('ElbowPTFK', 0, None),

	'UpLegIK' : ('UpLegFK', 0, 'Hip'),
	'LoLegIK' : ('LoLegFK', F_LR, 'UpLegIK'),
	#'FootIK' : ('FootFK', 0, None),
	#'ToeIK' : ('ToeFK', F_LR, 'FootIK'),

	'LegIK' : ('LegFK', 0, None),
	'ToeRevIK' : ('ToeFK', F_LR+F_Rev, 'LegIK'),
	'FootRevIK' : ('FootFK', F_LR+F_Rev, 'ToeRevIK'),
	'AnkleIK' : ('AnkleFK', F_LR, 'FootRevIK'),
	'KneePTIK' : ('KneePTFK', 0, None),
}

IkBoneList = [
	'UpArmIK', 'LoArmIK', 'HandIK', 'ElbowPTIK',
	'UpLegIK', 'LoLegIK', 'LegIK', 'ToeRevIK', 'FootRevIK', 'AnkleIK', 'KneePTIK',
]

GlobalBoneList = [
	'Root', 
]
'''
	'UpArmFK_L', 'LoArmFK_L', 'HandFK_L',
	'UpArmFK_R', 'LoArmFK_R', 'HandFK_R',
	'UpLegFK_L', 'LoLegFK_L', 'FootFK_L', 'ToeFK_L',
	'UpLegFK_R', 'LoLegFK_R', 'FootFK_R', 'ToeFK_R',
	'LegFK_L', 'AnkleFK_L',
	'LegFK_R', 'AnkleFK_R',
]
'''
#			
#	class CEditBone():
#

class CEditBone():
	def __init__(self, bone):
		self.name = bone.name
		self.head = bone.head.copy()
		self.tail = bone.tail.copy()
		self.roll = bone.roll
		if bone.parent:
			self.parent = bone.parent.name
			self.use_connect = bone.use_connect
		else:
			self.parent = None
			self.use_connect = False
		self.matrix = bone.matrix.copy().rotation_part()
		self.inverse = self.matrix.copy().invert()

	def __repr__(self):
		return ("%s p %s\n  h %s\n  t %s\n" % (self.name, self.parent, self.head, self.tail))

#
#	renameFKBones(bones00, rig00, action):
#

def renameFKBones(bones00, rig00, action):
	bones90 = {}
	bpy.ops.object.mode_set(mode='EDIT')
	ebones = rig00.data.edit_bones
	setbones = []
	for bone00 in bones00:
		name00 = bone00.name
		name90 = theArmature[name00.lower()]
		eb = ebones[name00]
		if name90:
			eb.name = name90
			bones90[name90] = CEditBone(eb)
			grp = action.groups[name00]
			grp.name = name90
			setbones.append((eb, name90))
		else:
			eb.name = '_' + name00
	for (eb, name) in setbones:
		eb.name = name
	createExtraBones(ebones, bones90)
	bpy.ops.object.mode_set(mode='POSE')
	return

#
#	createExtraBones(ebones, bones90):
#

def createExtraBones(ebones, bones90):
	for suffix in ['_L', '_R']:
		try:
			foot = ebones['FootFK'+suffix]
		except:
			foot = None
		try:
			toe = ebones['ToeFK'+suffix]
		except:
			toe = None

		if not toe:
			name90 = 'ToeFK'+suffix
			toe = ebones.new(name=name90)
			toe.head = foot.tail
			toe.tail = toe.head - Vector((0, 0.5*foot.length, 0))
			toe.parent = foot
			bones90[name90] = CEditBone(toe)
			
		name90 = 'LegFK'+suffix
		eb = ebones.new(name=name90)
		eb.head = 2*toe.head - toe.tail
		eb.tail = 4*toe.head - 3*toe.tail
		eb.parent = toe
		bones90[name90] = CEditBone(eb)

		name90 = 'AnkleFK'+suffix
		eb = ebones.new(name=name90)
		eb.head = foot.head
		eb.tail = 2*foot.head - foot.tail
		eb.parent = ebones['LoLegFK'+suffix]
		bones90[name90] = CEditBone(eb)
	return

#
#	makeVectorDict(ob, channel):
#

def makeVectorDict(ob, channel):
	fcuDict = {}
	for fcu in ob.animation_data.action.fcurves:
		words = fcu.data_path.split('"')
		if words[2] == channel:
			name = words[1]
			try:
				x = fcuDict[name]
			except:
				fcuDict[name] = []
			fcuDict[name].append((fcu.array_index, fcu))

	vecDict = {}
	for name in fcuDict.keys():
		fcuDict[name].sort()		
		vectors = []
		(index,fcu) = fcuDict[name][0]
		for kp in fcu.keyframe_points:
			vectors.append([])
		for (index, fcu) in fcuDict[name]:			
			n = 0
			for kp in fcu.keyframe_points:
				vectors[n].append(kp.co[1])
				n += 1
		vecDict[name] = vectors
	return vecDict
			
	
#
#	renameBvhRig(rig00, filepath):
#

def renameBvhRig(rig00, filepath):
	base = os.path.basename(filepath)
	(filename, ext) = os.path.splitext(base)
	print("File", filename, len(filename))
	if len(filename) > 12:
		words = filename.split('_')
		name = 'Y_'
		for word in words[1:]:
			name += word
	else:
		name = 'Y_' + filename
	print("Name", name)

	rig00.name = name
	action = rig00.animation_data.action
	action.name = name

	bones00 = []
	bpy.ops.object.mode_set(mode='EDIT')
	for bone in rig00.data.edit_bones:
		bones00.append( CEditBone(bone) )
	bpy.ops.object.mode_set(mode='POSE')

	return (rig00, bones00, action)

#
#	createIKBones(rig90):
#

def createIKBones(rig90):
	bpy.ops.object.mode_set(mode='EDIT')
	ebones = rig90.data.edit_bones
	for suffix in ['_L', '_R']:
		for nameIK in IkBoneList:
			(nameFK, flags, parent) = IkArmature[nameIK]
			eb = ebones.new(name=nameIK+suffix)
			fb = ebones[nameFK+suffix]
			if flags & F_Rev:
				eb.head = fb.tail
				eb.tail = fb.head
				eb.roll = fb.roll
			else:
				eb.head = fb.head
				eb.tail = fb.tail
				eb.roll = fb.roll
			eb.use_local_location = False
			if parent:
				if flags & F_LR:
					eb.parent = ebones[parent+suffix]
				else:
					eb.parent = ebones[parent]
	return

#
#	constrainIkBones(rig90):
#

def constrainIkBones(rig90):
	bpy.ops.object.mode_set(mode='POSE')
	pbones = rig90.pose.bones
	for pb in pbones:
		if pb.parent:
			pb.lock_location = (True, True, True)		

	for suffix in ['_L', '_R']:
		cns = pbones['LoArmIK'+suffix].constraints.new(type='IK')
		cns.target = rig90
		cns.subtarget = 'HandIK'+suffix
		cns.chain_count = 2

		cns = pbones['LoLegIK'+suffix].constraints.new(type='IK')
		cns.target = rig90
		cns.subtarget = 'AnkleIK'+suffix
		cns.chain_count = 2
	return

#
#	copyAnglesFKIK():
#	'UpArmIK' : ('UpArmFK', F_LR, 'Shoulder')

def copyAnglesFKIK(context):
	bpy.ops.object.mode_set(mode='EDIT')
	ebones = context.object.data.edit_bones
	for nameIK in IkBoneList:
		(nameFK, flags, parent) = IkArmature[nameIK]
		for suffix in ['_L', '_R']:
			ebones[nameIK+suffix].roll = ebones[nameFK+suffix].roll
	bpy.ops.object.mode_set(mode='POSE')
	return
	
#
#	guessArmature(rig):
#	setArmature(rig)
#

def guessArmature(rig):
	global theArmature, theArmatures
	bestMisses = 1000
	misses = {}
	bones = rig.data.bones
	for (name, amt) in theArmatures.items():
		nMisses = 0
		for bone in bones:
			try:
				amt[bone.name.lower()]
			except:
				nMisses += 1
		misses[name] = nMisses
		if nMisses < bestMisses:
			best = amt
			bestName = name
			bestMisses = nMisses
	if bestMisses > 0:
		for bone in bones:
			print("'%s'" % bone.name)
		for (name, n) in misses.items():
			print(name, n)
		raise NameError('Did not find matching armature. nMisses = %d' % bestMisses)
	theArmature = best
	rig['MhxArmature'] = bestName
	print("Using matching armature %s." % rig['MhxArmature'])
	return

def setArmature(rig):
	global theArmature, theArmatures
	try:
		name = rig['MhxArmature']
	except:
		raise NameError("No armature set")
	theArmature = theArmatures[name]
	print("Set armature %s" % name)
	return
	
#
#	importAndRename(context, filepath):
#

def importAndRename(context, filepath):
	rig = readBvhFile(context, filepath, context.scene)
	(rig00, bones00, action) =  renameBvhRig(rig, filepath)
	guessArmature(rig00)
	renameFKBones(bones00, rig00, action)
	setInterpolation(rig00)
	return (rig00, action)

#
#	class CAnimData():
#

class CAnimData():
	def __init__(self, name):
		self.nFrames = 0
		self.parent = None

		self.headRest = None
		self.vecRest = None
		self.tailRest = None
		self.offsetRest = None
		self.matrixRest = None
		self.inverseRest = None
		self.matrixRel = None
		self.inverseRel = None

		self.heads = {}
		self.tails = {}
		self.quats = {}
		self.matrices = {}
		self.name = name

		
#
#	createAnimation(context, rig):
#	createAnimData(name, animations, ebones):
#

def createAnimation(context, rig):
	context.scene.objects.active = rig
	animations = {}
	#bpy.ops.object.mode_set(mode='EDIT')
	for name in FkBoneList:
		createAnimData(name, animations, rig.data.bones)
	#bpy.ops.object.mode_set(mode='POSE')
	return animations

def createAnimData(name, animations, bones):
	try:
		b = bones[name]
	except:
		return
	anim = CAnimData(name)
	animations[name] = anim
	anim.headRest = b.head_local.copy()
	anim.tailRest = b.tail_local.copy()
	anim.vecRest = anim.tailRest - anim.headRest
	if b.parent:
		anim.parent = b.parent.name
		animPar = animations[anim.parent]
		anim.offsetRest = anim.headRest - animPar.headRest
	else:
		anim.offsetRest = Vector((0,0,0))	
	anim.matrixRest = b.matrix_local.rotation_part()
	anim.inverseRest = anim.matrixRest.copy().invert()
	anim.matrixRel = b.matrix.copy()
	anim.inverseRel = anim.matrixRel.copy().invert()
	return
'''
def relativizeBones(rig90, mhxrig, mhxAnims):
	for bone90 in rig90.data.bones:
		if bone90.parent:
			name = bone90.name
			pname = bone90.parent.name
			anim = mhxAnims[name]
			bone = mhxrig.data.bones[name].parent
			while bone and bone.name != pname:			
				anim.matrixRel = bone.matrix * anim.matrixRel
				bone = bone.parent
			anim.inverseRel = anim.matrixRel.copy().invert()
	return
'''
#
#	insertAnimation(context, rig, animations):
#	insertAnimRoot(root, animations, nFrames, locs, rots):
#	insertAnimChild(name, animations, rots):
#

def insertAnimation(context, rig, animations):
	context.scene.objects.active = rig
	bpy.ops.object.mode_set(mode='POSE')
	locs = makeVectorDict(rig, '].location')
	rots = makeVectorDict(rig, '].rotation_quaternion')
	root = 'Root'
	insertAnimRoot(root, animations, len(rots[root]), locs[root], rots[root])
	for name in FkBoneList:
		if name != root:
			try:
				rot = rots[name]
			except:
				rot = None
			insertAnimChild(name, animations, rot)

def insertAnimRoot(root, animations, nFrames, locs, rots):
	anim = animations[root]
	anim.nFrames = nFrames
	for frame in range(nFrames):
		quat = Quaternion(rots[frame])
		anim.quats[frame] = quat
		matrix = anim.matrixRest * quat.to_matrix() * anim.inverseRest
		anim.matrices[frame] = matrix
		anim.heads[frame] =  Vector(locs[frame]) * anim.matrixRest + anim.headRest
		anim.tails[frame] = anim.heads[frame] + anim.vecRest * matrix
	return

def insertAnimChildLoc(nameIK, nameFK, animations, locs):
	animIK = animations[nameIK]
	animFK = animations[nameFK]
	animPar = animations[animFK.parent]
	animIK.nFrames = animFK.nFrames
	for frame in range(animFK.nFrames):
		parmat = animPar.matrices[frame]
		animIK.heads[frame] = animPar.heads[frame] + animFK.offsetRest * parmat
	return

def insertAnimChild(name, animations, rots):
	try:
		anim = animations[name]
	except:
		return None
	animPar = animations[anim.parent]
	anim.nFrames = animPar.nFrames
	quat = Quaternion().identity()
	for frame in range(anim.nFrames):
		parmat = animPar.matrices[frame]
		if rots:
			quat = Quaternion(rots[frame])
		anim.quats[frame] = quat
		locmat = anim.matrixRest * quat.to_matrix() * anim.inverseRest
		matrix = parmat * locmat
		anim.matrices[frame] = matrix
		anim.heads[frame] = animPar.heads[frame] + anim.offsetRest*parmat
		anim.tails[frame] = anim.heads[frame] + anim.vecRest*matrix
	return anim
		
#
#	poseMhxFKBones(context, mhxrig, rig90Animations, mhxAnimations, fixes)
#

def poseMhxFKBones(context, mhxrig, rig90Animations, mhxAnimations, fixes):
	context.scene.objects.active = mhxrig
	bpy.ops.object.mode_set(mode='POSE')
	pbones = mhxrig.pose.bones
	
	name = 'Root'
	insertLocationKeyFrames(name, pbones[name], rig90Animations[name], mhxAnimations[name])
	for name in FkBoneList:
		try:
			pb = pbones[name]
			anim90 = rig90Animations[name]
			animMhx =  mhxAnimations[name]
			success = True
		except:
			success = False
		if not success:
			pass
		elif name in GlobalBoneList:
			insertGlobalRotationKeyFrames(name, pb, anim90, animMhx)
		else:
			try:
				fix = fixes[name]
			except:
				fix = None
			if fix:
				fixAndInsertLocalRotationKeyFrames(name, pb, anim90, animMhx, fix)
			else:
				insertLocalRotationKeyFrames(name, pb, anim90, animMhx)

	insertAnimation(context, mhxrig, mhxAnimations)

	for suffix in ['_L', '_R']:
		for name in ['ElbowPT', 'KneePT']:
			nameFK = name+'FK'+suffix
			insertAnimChild(nameFK, mhxAnimations, None)

	setInterpolation(mhxrig)
	return

#
#	insertLocationKeyFrames(name, pb, anim90, animMhx):
#	insertGlobalRotationKeyFrames(name, pb, anim90, animMhx):
#	insertGlobalRotationKeyFrames(name, pb, anim90, animMhx):
#	insertReverseRotationKeyFrames(name, pb, animFK, animIK, animPar):
#

def insertLocationKeyFrames(name, pb, anim90, animMhx):
	locs = []
	for frame in range(anim90.nFrames):
		loc0 = anim90.heads[frame] - animMhx.headRest
		loc = loc0 * animMhx.inverseRest
		locs.append(loc)
		pb.location = loc
		for n in range(3):
			pb.keyframe_insert('location', index=n, frame=frame, group=name)	
	return locs

def insertIKFKLocationKeyFrames(nameIK, nameFK, pb, animations):
	pb.select = True
	animIK = animations[nameIK]
	animFK = animations[nameFK]
	if animIK.parent:
		animPar = animations[animIK.parent]
	else:
		animPar = None
	locs = []
	for frame in range(animFK.nFrames):		
		if animPar:
			loc0 = animPar.heads[frame] + animIK.offsetRest*animPar.matrices[frame]
			offset = animFK.heads[frame] - loc0
			mat = animPar.matrices[frame] * animIK.matrixRest
			loc = offset*mat.invert()
		else:
			offset = animFK.heads[frame] - animIK.headRest
			loc = offset * animIK.inverseRest
		pb.location = loc
		for n in range(3):
			pb.keyframe_insert('location', index=n, frame=frame, group=nameIK)	
	return


def insertGlobalRotationKeyFrames(name, pb, anim90, animMhx):
	rots = []
	for frame in range(anim90.nFrames):
		mat90 = anim90.matrices[frame]
		animMhx.matrices[frame] = mat90
		matMhx = animMhx.inverseRest * mat90 * animMhx.matrixRest
		rot = matMhx.to_quat()
		rots.append(rot)
		pb.rotation_quaternion = rot
		for n in range(4):
			pb.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=name)
	return rots

def insertLocalRotationKeyFrames(name, pb, anim90, animMhx):
	rots = []
	for frame in range(anim90.nFrames):
		rot = anim90.quats[frame]
		rots.append(rot)
		pb.rotation_quaternion = rot
		for n in range(4):
			pb.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=name)
	return rots

def fixAndInsertLocalRotationKeyFrames(name, pb, anim90, animMhx, fix):
	rots = []
	(fixMat, exchange) = fix
	for frame in range(anim90.nFrames):
		mat90 = anim90.quats[frame].to_matrix()
		if fixMat:
			matMhx = fixMat * mat90
		else:
			matMhx = mat90
		rot0 = matMhx.to_quat()
		if exchange == 'XZ':
			rot = rot0.copy()
			rot.z = rot0.x
			rot.x = -rot0.z
		elif exchange == 'ZX':
			rot = rot0.copy()
			rot.z = -rot0.x
			rot.x = rot0.z
		else:
			rot = rot0
		rots.append(rot)
		pb.rotation_quaternion = rot
		for n in range(4):
			pb.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=name)
	return rots

def insertReverseRotationKeyFrames(name, pb, animFK, animIK, animPar):
	rots = []
	for frame in range(animFK.nFrames):
		matFK = animPar.matrices[frame].copy().invert() * animFK.matrices[frame]
		matIK = animIK.inverseRest * matFK * animIK.matrixRest
		rot = matIK.to_quat()
		rots.append(rot)
		pb.rotation_quaternion = rot
		for n in range(4):
			pb.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=name)
	return rots

#
#	poseMhxIKBones(context, mhxrig, mhxAnimations)
#

def poseMhxIKBones(context, mhxrig, mhxAnimations):
	bpy.ops.object.mode_set(mode='POSE')
	pbones = mhxrig.pose.bones
	for suffix in ['_L', '_R']:
		for name in ['UpArm', 'LoArm', 'UpLeg', 'LoLeg']:
			nameIK = name+'IK'+suffix
			nameFK = name+'FK'+suffix
			insertLocalRotationKeyFrames(nameIK, pbones[nameIK], mhxAnimations[nameFK], mhxAnimations[nameFK])

		for name in ['Hand', 'Leg']:
			nameIK = name+'IK'+suffix
			nameFK = name+'FK'+suffix
			createAnimData(nameIK, mhxAnimations, mhxrig.data.bones)		
			animFK = mhxAnimations[nameFK]
			loc = insertLocationKeyFrames(nameIK, pbones[nameIK], animFK, mhxAnimations[nameIK])
			rot = insertGlobalRotationKeyFrames(nameIK, pbones[nameIK],animFK, mhxAnimations[nameIK])
			insertAnimRoot(nameIK, mhxAnimations, animFK.nFrames, loc, rot)

		for name in ['ElbowPT', 'KneePT']:
			nameIK = name+'IK'+suffix
			nameFK = name+'FK'+suffix
			createAnimData(nameIK, mhxAnimations, mhxrig.data.bones)		
			insertIKFKLocationKeyFrames(nameIK, nameFK, pbones[nameIK], mhxAnimations)

		for name in ['Toe', 'Foot']:
			nameIK = name+'RevIK'+suffix
			nameFK = name+'FK'+suffix
			createAnimData(nameIK, mhxAnimations, mhxrig.data.bones)		
			animFK = mhxAnimations[nameFK]
			animIK = mhxAnimations[nameIK]
			rot = insertReverseRotationKeyFrames(nameIK, pbones[nameIK], animFK, animIK, mhxAnimations[animIK.parent])
			insertAnimChild(nameIK, mhxAnimations, rot)

	setInterpolation(mhxrig)
	return

#
#	prettifyBones(rig):
#

def prettifyBones(rig):
	bpy.ops.object.mode_set(mode='POSE')
	rig.data.layers[1] = True
	rig.data.layers[2] = True
	for index in range(4):
		bpy.ops.pose.group_add()

	index = 0
	colorSet = ['THEME02', 'THEME03', 'THEME04', 'THEME09']
	for suffix in ['_L', '_R']:
		for name in ['LegFK', 'AnkleFK', 'AnkleIK']:
			rig.data.bones[name+suffix].hide = True

		bgrpIK = rig.pose.bone_groups[index]
		bgrpIK.color_set = colorSet[index]
		bgrpIK.name = 'IK'+suffix
		bgrpFK = rig.pose.bone_groups[index+1]
		bgrpFK.color_set = colorSet[index+1]
		bgrpFK.name = 'FK'+suffix

		for nameIK in IkBoneList:
			(nameFK, flags, parent) = IkArmature[nameIK]
			pb = rig.pose.bones[nameIK+suffix]
			pb.bone_group = bgrpIK
			b = rig.data.bones[nameIK+suffix]
			b.layers[1] = True
			b.layers[0] = False

			pb = rig.pose.bones[nameFK+suffix]
			pb.bone_group = bgrpFK
			b = rig.data.bones[nameFK+suffix]
			b.layers[2] = True
			b.layers[0] = False
		index += 2
	return

#
#	retargetMhxRig(context, rig90, mhxrig):
#

def retargetMhxRig(context, rig90, mhxrig):
	scn = context.scene
	setArmature(rig90)
	print("Retarget %s --> %s" % (rig90, mhxrig))
	if mhxrig.animation_data:
		mhxrig.animation_data.action = None

	mhxAnimations = createAnimation(context, mhxrig)
	rig90Animations = createAnimation(context, rig90)
	insertAnimation(context, rig90, rig90Animations)
	onoff = toggleLimitConstraints(mhxrig)
	setLimitConstraints(mhxrig, 0.0)
	if scn['MhxApplyFixes']:
		fixes = FixesList[rig90['MhxArmature']]
	else:
		fixes = None
	poseMhxFKBones(context, mhxrig, rig90Animations, mhxAnimations, fixes)
	poseMhxIKBones(context, mhxrig, mhxAnimations)
	if onoff == 'OFF':
		setLimitConstraints(mhxrig, 1.0)
	else:
		setLimitConstraints(mhxrig, 0.0)

	mhxrig.animation_data.action.name = mhxrig.name[:4] + rig90.name[2:]
	print("Retargeted %s --> %s" % (rig90, mhxrig))
	return

#
#	deleteFKRig(context, rig00, action, prefix):
#

def deleteFKRig(context, rig00, action, prefix):
	context.scene.objects.unlink(rig00)
	if rig00.users == 0:
		bpy.data.objects.remove(rig00)
		#del rig00
	if bpy.data.actions:
		for act in bpy.data.actions:
			if act.name[0:2] == prefix:
				act.use_fake_user = False
				if act.users == 0:
					bpy.data.actions.remove(act)
					del act
	return

#
#	simplifyFCurves(context, rig):
#

def simplifyFCurves(context, rig):
	if not context.scene.MhxDoSimplify:
		return
	try:
		act = rig.animation_data.action
	except:
		act = None
	if not act:
		print("No FCurves to simplify")
		return

	maxErrLoc = context.scene.MhxErrorLoc
	maxErrRot = context.scene.MhxErrorRot * math.pi/180
	for fcu in act.fcurves:
		simplifyFCurve(fcu, act, maxErrLoc, maxErrRot)
	setInterpolation(rig)
	print("Curves simplified")
	return

#
#	simplifyFCurve(fcu, act, maxErrLoc, maxErrRot):
#

def simplifyFCurve(fcu, act, maxErrLoc, maxErrRot):
	words = fcu.data_path.split('.')
	if words[-1] == 'location':
		maxErr = maxErrLoc
	elif words[-1] == 'rotation_quaternion':
		maxErr = maxErrRot
	else:
		raise NameError("Unknown FCurve type %s" % words[-1])

	points = fcu.keyframe_points
	nPoints = len(points)
	if nPoints <= 2:
		return
	keeps = []
	new = [0, nPoints-1]
	while new:
		keeps += new
		keeps.sort()
		new = iterateFCurves(points, keeps, maxErr)

	newVerts = []
	for n in keeps:
		newVerts.append(points[n].co.copy())
	
	path = fcu.data_path
	index = fcu.array_index
	grp = fcu.group.name
	act.fcurves.remove(fcu)
	nfcu = act.fcurves.new(path, index, grp)
	for co in newVerts:
		t = co[0]
		try:
			dt = t - int(t)
		except:
			dt = 0.5
		if abs(dt) > 1e-5:
			print(path, co)
		else:
			nfcu.keyframe_points.add(frame=co[0], value=co[1])

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

#
#	plantKeys(context)
#	plantFCurves(fcurves, first, last):
#

def plantKeys(context):
	rig = context.object
	scn = context.scene
	if not rig.animation_data:
		print("Cannot plant: no animation data")
		return
	act = rig.animation_data.action
	if not act:
		print("Cannot plant: no action")
		return
	bone = rig.data.bones.active
	if not bone:
		print("Cannot plant: no active bone")
		return

	markers = []
	for mrk in scn.timeline_markers:
		if mrk.select:
			markers.append(mrk.frame)
	markers.sort()
	if len(markers) >= 2:
		first = markers[0]
		last = markers[-1]
		print("Delete keys between %d and %d" % (first, last))
	else:
		print("Cannot plant: need two selected time markers")
		return

	locPath = 'pose.bones["%s"].location' % bone.name
	rotPath = 'pose.bones["%s"].rotation_quaternion' % bone.name
	rots = []
	locs = []
	for fcu in act.fcurves:
		if fcu.data_path == locPath:
			locs.append(fcu)
		if fcu.data_path == rotPath:
			rots.append(fcu)

	pb = rig.pose.bones[bone.name]
	useCrnt = scn['MhxPlantCurrent']
	if scn['MhxPlantLoc']:
		plantFCurves(locs, first, last, useCrnt, pb.location)
	if scn['MhxPlantRot']:
		plantFCurves(rots, first, last, useCrnt, pb.rotation_quaternion)
	return

def plantFCurves(fcurves, first, last, useCrnt, values):
	for fcu in fcurves:
		print("Plant", fcu.data_path, fcu.array_index)
		kpts = fcu.keyframe_points
		sum = 0.0
		dellist = []
		firstx = first - 1e-4
		lastx = last + 1e-4
		print("Btw", firstx, lastx)
		for kp in kpts:
			(x,y) = kp.co
			if x > firstx and x < lastx:
				dellist.append(kp)
				sum += y
		nterms = len(dellist)
		if nterms == 0:
			return
		if useCrnt:
			ave = values[fcu.array_index]
			print("Current", ave)
		else:
			ave = sum/nterms
		for kp in dellist:
			kp.co[1] = ave
		kpts.add(first, ave, fast=True)
		kpts.add(last, ave, fast=False)
	return

#
#	iterateFCurves(points, keeps, maxErr):
#

def iterateFCurves(points, keeps, maxErr):
	new = []
	for edge in range(len(keeps)-1):
		n0 = keeps[edge]
		n1 = keeps[edge+1]
		(x0, y0) = points[n0].co
		(x1, y1) = points[n1].co
		if x1 > x0:
			dxdn = (x1-x0)/(n1-n0)
			dydx = (y1-y0)/(x1-x0)
			err = 0
			for n in range(n0+1, n1):
				(x, y) = points[n].co
				xn = n0 + dxdn*(n-n0)
				yn = y0 + dydx*(xn-x0)
				if abs(y-yn) > err:
					err = abs(y-yn)
					worst = n
			if err > maxErr:
				new.append(worst)
	return new
		
#
#	togglePoleTargets(mhxrig):
#	toggleIKLimits(mhxrig):
#	toggleLimitConstraints(mhxrig):
#	setLimitConstraints(mhxrig, inf):
#

def togglePoleTargets(mhxrig):
	bones = mhxrig.data.bones
	pbones = mhxrig.pose.bones
	if bones['ElbowPTIK_L'].hide:
		hide = False
		poletar = mhxrig
		res = 'ON'
	else:
		hide = True
		poletar = None
		res = 'OFF'
	for suffix in ['_L', '_R']:
		for name in ['ElbowPTIK', 'ElbowLinkPTIK', 'ElbowPTFK', 'KneePTIK', 'KneeLinkPTIK', 'KneePTFK']:
			bones[name+suffix].hide = hide
		cns = pbones['LoLegIK'+suffix].constraints['IK']
		cns.pole_target = poletar
	return res

def toggleIKLimits(mhxrig):
	pbones = mhxrig.pose.bones
	if pbones['UpLegIK_L'].use_ik_limit_x:
		use = False
		res = 'OFF'
	else:
		use = True
		res = 'ON'
	for suffix in ['_L', '_R']:
		for name in ['UpArmIK', 'LoArmIK', 'UpLegIK', 'LoLegIK']:
			pb = pbones[name+suffix]
			pb.use_ik_limit_x = use
			pb.use_ik_limit_y = use
			pb.use_ik_limit_z = use
	return res

def toggleLimitConstraints(mhxrig):
	pbones = mhxrig.pose.bones
	first = True
	for pb in pbones:
		for cns in pb.constraints:
			if (cns.type == 'LIMIT_LOCATION' or
				cns.type == 'LIMIT_ROTATION' or
				cns.type == 'LIMIT_DISTANCE' or
				cns.type == 'LIMIT_SCALE'):
				if first:
					first = False
					if cns.influence > 0.5:
						inf = 0.0
						res = 'OFF'
					else:
						inf = 1.0
						res = 'ON'
				cns.influence = inf
	return res

def setLimitConstraints(mhxrig, inf):
	pbones = mhxrig.pose.bones
	for pb in pbones:
		for cns in pb.constraints:
			if (cns.type == 'LIMIT_LOCATION' or
				cns.type == 'LIMIT_ROTATION' or
				cns.type == 'LIMIT_DISTANCE' or
				cns.type == 'LIMIT_SCALE'):
				cns.influence = inf
	return

#
#	silenceConstraints(rig):
#

def silenceConstraints(rig):
	for pb in rig.pose.bones:
		pb.lock_location = (False, False, False)
		pb.lock_rotation = (False, False, False)
		pb.lock_scale = (False, False, False)
		for cns in pb.constraints:
			if cns.type == 'CHILD_OF':
				cns.influence = 0.0
			elif False and (cns.type == 'LIMIT_LOCATION' or
				cns.type == 'LIMIT_ROTATION' or
				cns.type == 'LIMIT_DISTANCE' or
				cns.type == 'LIMIT_SCALE'):
				cns.influence = 0.0
	return

###################################################################################	
#	User interface
#
#	getBvh(mhx)
#	initInterface(context)
#

def getBvh(mhx):
	for (bvh, mhx1) in theArmature.items():
		if mhx == mhx1:
			return bvh
	return None

def initInterface(context):
	scn = context.scene
	bpy.types.Scene.MhxBvhScale = FloatProperty(
		name="Scale", 
		description="Scale the BVH by this value", 
		min=0.0001, max=1000000.0, 
		soft_min=0.001, soft_max=100.0)
	scn['MhxBvhScale'] = 0.65

	bpy.types.Scene.MhxStartFrame = IntProperty(
		name="Start Frame", 
		description="Starting frame for the animation")
	scn['MhxStartFrame'] = 1

	bpy.types.Scene.MhxEndFrame = IntProperty(
		name="Last Frame", 
		description="Last frame for the animation")
	scn['MhxEndFrame'] = 32000

	bpy.types.Scene.MhxSubsample = IntProperty(
		name="Subsample", 
		description="Sample only every n:th frame")
	scn['MhxSubsample'] = 1

	bpy.types.Scene.MhxDefaultSS = BoolProperty(
		name="Use default subsample")
	scn['MhxDefaultSS'] = True

	bpy.types.Scene.MhxRot90Anim = BoolProperty(
		name="Rotate 90 deg", 
		description="Rotate 90 degress so Z points up")
	scn['MhxRot90Anim'] = True

	bpy.types.Scene.MhxDoSimplify = BoolProperty(
		name="Simplify FCurves", 
		description="Simplify FCurves")
	scn['MhxDoSimplify'] = True

	bpy.types.Scene.MhxApplyFixes = BoolProperty(
		name="Apply found fixes", 
		description="Apply found fixes")
	scn['MhxApplyFixes'] = True

	bpy.types.Scene.MhxPlantCurrent = BoolProperty(
		name="Use current", 
		description="Plant at current")
	scn['MhxPlantCurrent'] = True

	bpy.types.Scene.MhxPlantLoc = BoolProperty(
		name="Loc", 
		description="Plant location keys")
	scn['MhxPlantLoc'] = True

	bpy.types.Scene.MhxPlantRot = BoolProperty(
		name="Rot", 
		description="Plant rotation keys")
	scn['MhxPlantRot'] = False

	bpy.types.Scene.MhxErrorLoc = FloatProperty(
		name="Max loc error", 
		description="Max error for location FCurves when doing simplification",
		min=0.001)
	scn['MhxErrorLoc'] = 0.01

	bpy.types.Scene.MhxErrorRot = FloatProperty(
		name="Max rot error", 
		description="Max error for rotation (degrees) FCurves when doing simplification",
		min=0.001)
	scn['MhxErrorRot'] = 0.1

	bpy.types.Scene.MhxDirectory = StringProperty(
		name="Directory", 
		description="Directory", 
		maxlen=1024)
	scn['MhxDirectory'] = "~/makehuman/bvh/Female1_bvh"

	bpy.types.Scene.MhxReallyDelete = BoolProperty(
		name="Really delete action", 
		description="Delete button deletes action permanently")
	scn['MhxReallyDelete'] = False

	listAllActions(context)
	setAction()

	bpy.types.Scene.MhxPrefix = StringProperty(
		name="Prefix", 
		description="Prefix", 
		maxlen=1024)
	scn['MhxPrefix'] = "Female1_A"

	bpy.types.Object.MhxArmature = StringProperty()

	'''
	for mhx in FkBoneList:
		bpy.types.Scene.StringProperty(
			attr=mhx, 
			name=mhx, 
			description="Bvh bone corresponding to %s" % mhx, 
			default = ''
		)
		bvh = getBvh(mhx)
		if bvh:
			scn[mhx] = bvh
	'''

	loadDefaults(context)
	return

#
#	saveDefaults(context):
#	loadDefaults(context):
#

def saveDefaults(context):
	filename = os.path.realpath(os.path.expanduser("~/makehuman/mhx_defaults.txt"))
	try:
		fp = open(filename, "w")
	except:
		print("Unable to open %s for writing" % filename)
		return
	for (key,value) in context.scene.items():
		if key[:3] == 'Mhx':
			fp.write("%s %s\n" % (key, value))
	fp.close()
	return

def loadDefaults(context):
	filename = os.path.realpath(os.path.expanduser("~/makehuman/mhx_defaults.txt"))
	try:
		fp = open(filename, "r")
	except:
		print("Unable to open %s for reading" % filename)
		return
	for line in fp:
		words = line.split()
		try:
			val = eval(words[1])
		except:
			val = words[1]
		context.scene[words[0]] = val
	fp.close()
	return

#		
#	class MhxBvhAssocPanel(bpy.types.Panel):
#
"""
class MhxBvhAssocPanel(bpy.types.Panel):
	bl_label = "Mhx Bvh associations"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_options = "HIDE_HEADER"
	
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
		for mhx in FkBoneList:
			try:				
				layout.prop(context.scene, mhx)
			except:
				pass
		return
"""

#
#	makeMhxRig(ob)
#

def makeMhxRig(ob):
		try:
			test = ob['MhxRig']
		except:
			test = False
		if not test:
			return

#
#	class Bvh2MhxPanel(bpy.types.Panel):
#

class Bvh2MhxPanel(bpy.types.Panel):
	bl_label = "Bvh to Mhx"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	@classmethod
	def poll(cls, context):
		if context.object and context.object.type == 'ARMATURE':
			return True

	def draw(self, context):
		layout = self.layout
		scn = context.scene
		layout.operator("object.InitInterfaceButton")
		layout.operator("object.SaveDefaultsButton")
		layout.operator("object.CopyAnglesFKIKButton")

		layout.label('Load')
		layout.prop(scn, "MhxBvhScale")
		layout.prop(scn, "MhxStartFrame")
		layout.prop(scn, "MhxEndFrame")
		layout.prop(scn, "MhxSubsample")
		layout.prop(scn, "MhxDefaultSS")
		layout.prop(scn, "MhxRot90Anim")
		layout.prop(scn, "MhxDoSimplify")
		layout.prop(scn, "MhxApplyFixes")
		layout.operator("object.LoadBvhButton")
		layout.operator("object.RetargetMhxButton")
		layout.separator()
		layout.operator("object.LoadRetargetSimplifyButton")

		layout.label('Toggle')
		layout.operator("object.TogglePoleTargetsButton")
		layout.operator("object.ToggleIKLimitsButton")
		layout.operator("object.ToggleLimitConstraintsButton")

		layout.label('Plant')
		row = layout.row()
		row.prop(scn, "MhxPlantLoc")
		row.prop(scn, "MhxPlantRot")
		layout.prop(scn, "MhxPlantCurrent")
		layout.operator("object.PlantButton")

		layout.label('Simplify')
		layout.prop(scn, "MhxErrorLoc")
		layout.prop(scn, "MhxErrorRot")
		layout.operator("object.SimplifyFCurvesButton")

		layout.label('Batch conversion')
		layout.prop(scn, "MhxDirectory")
		layout.prop(scn, "MhxPrefix")
		layout.operator("object.BatchButton")

		layout.label('Manage actions')
		listAllActions(context)
		setAction()
		layout.prop_menu_enum(scn, "MhxActions")
		layout.operator("object.SelectButton")
		layout.prop(scn, "MhxReallyDelete")
		layout.operator("object.DeleteButton")
		return

#
#	class OBJECT_OT_LoadBvhButton(bpy.types.Operator):
#

class OBJECT_OT_LoadBvhButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_LoadBvhButton"
	bl_label = "Load BVH file (.bvh)"
	filepath = StringProperty(name="File Path", description="Filepath used for importing the OBJ file", maxlen=1024, default="")

	def execute(self, context):
		import bpy, os
		importAndRename(context, self.properties.filepath)
		print("%s imported" % self.properties.filepath)
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.window_manager.add_fileselect(self)
		return {'RUNNING_MODAL'}	

#
#	class OBJECT_OT_RetargetMhxButton(bpy.types.Operator):
#

class OBJECT_OT_RetargetMhxButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_RetargetMhxButton"
	bl_label = "Retarget selected to MHX"

	def execute(self, context):
		import bpy, mathutils
		mhxrig = context.object
		for rig90 in context.selected_objects:
			if rig90 != mhxrig:
				retargetMhxRig(context, rig90, mhxrig)
		return{'FINISHED'}	

#
#	class OBJECT_OT_SimplifyFCurvesButton(bpy.types.Operator):
#

class OBJECT_OT_SimplifyFCurvesButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_SimplifyFCurvesButton"
	bl_label = "Simplify FCurves"

	def execute(self, context):
		import bpy, mathutils
		simplifyFCurves(context, context.object)
		return{'FINISHED'}	

#
#	class OBJECT_OT_SilenceConstraintsButton(bpy.types.Operator):
#

class OBJECT_OT_SilenceConstraintsButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_SilenceConstraintsButton"
	bl_label = "Silence constraints"

	def execute(self, context):
		import bpy, mathutils
		silenceConstraints(context.object)
		print("Constraints silenced")
		return{'FINISHED'}	

#
#	class OBJECT_OT_TogglePoleTargetsButton(bpy.types.Operator):
#

class OBJECT_OT_TogglePoleTargetsButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_TogglePoleTargetsButton"
	bl_label = "Toggle pole targets"

	def execute(self, context):
		import bpy
		res = togglePoleTargets(context.object)
		print("Pole targets toggled", res)
		return{'FINISHED'}	

#
#	class OBJECT_OT_ToggleIKLimitsButton(bpy.types.Operator):
#

class OBJECT_OT_ToggleIKLimitsButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_ToggleIKLimitsButton"
	bl_label = "Toggle IK limits"

	def execute(self, context):
		import bpy
		res = toggleIKLimits(context.object)
		print("IK limits toggled", res)
		return{'FINISHED'}	

#
#	class OBJECT_OT_ToggleLimitConstraintsButton(bpy.types.Operator):
#

class OBJECT_OT_ToggleLimitConstraintsButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_ToggleLimitConstraintsButton"
	bl_label = "Toggle Limit constraints"

	def execute(self, context):
		import bpy
		res = toggleLimitConstraints(context.object)
		print("Limit constraints toggled", res)
		return{'FINISHED'}	

#
#	class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
#

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_InitInterfaceButton"
	bl_label = "Initialize"

	def execute(self, context):
		import bpy
		initInterface(context)
		print("Interface initialized")
		return{'FINISHED'}	

#
#	class OBJECT_OT_SaveDefaultsButton(bpy.types.Operator):
#

class OBJECT_OT_SaveDefaultsButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_SaveDefaultsButton"
	bl_label = "Save defaults"

	def execute(self, context):
		saveDefaults(context)
		return{'FINISHED'}	

#
#	class OBJECT_OT_PlantButton(bpy.types.Operator):
#

class OBJECT_OT_PlantButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_PlantButton"
	bl_label = "Plant"

	def execute(self, context):
		import bpy
		plantKeys(context)
		print("Keys planted")
		return{'FINISHED'}	

#
#	class OBJECT_OT_CopyAnglesFKIKButton(bpy.types.Operator):
#

class OBJECT_OT_CopyAnglesFKIKButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_CopyAnglesFKIKButton"
	bl_label = "Angles FK --> IK"

	def execute(self, context):
		import bpy
		copyAnglesFKIK(context)
		print("Angles copied")
		return{'FINISHED'}	

#
#	loadRetargetSimplify(context, filepath):
#	class OBJECT_OT_LoadRetargetSimplify(bpy.types.Operator):
#

def loadRetargetSimplify(context, filepath):
	print("Load and retarget %s" % filepath)
	time1 = time.clock()
	mhxrig = context.object
	(rig90, action) = importAndRename(context, filepath)
	retargetMhxRig(context, rig90, mhxrig)
	if context.scene['MhxDoSimplify']:
		simplifyFCurves(context, mhxrig)
	deleteFKRig(context, rig90, action, 'Y_')
	time2 = time.clock()
	print("%s finished in %.3f s" % (filepath, time2-time1))
	return

class OBJECT_OT_LoadRetargetSimplifyButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_LoadRetargetSimplifyButton"
	bl_label = "Load, retarget, simplify"
	filepath = StringProperty(name="File Path", description="Filepath used for importing the BVH file", maxlen=1024, default="")

	def execute(self, context):
		import bpy, os, mathutils
		loadRetargetSimplify(context, self.properties.filepath)
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.window_manager.add_fileselect(self)
		return {'RUNNING_MODAL'}	

#
#	readDirectory(directory, prefix):
#	class OBJECT_OT_BatchButton(bpy.types.Operator):
#

def readDirectory(directory, prefix):
	realdir = os.path.realpath(os.path.expanduser(directory))
	files = os.listdir(realdir)
	n = len(prefix)
	paths = []
	for fileName in files:
		(name, ext) = os.path.splitext(fileName)
		if name[:n] == prefix and ext == '.bvh':
			paths.append("%s/%s" % (realdir, fileName))
	return paths

class OBJECT_OT_BatchButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_BatchButton"
	bl_label = "Batch run"

	def execute(self, context):
		import bpy, os, mathutils
		paths = readDirectory(context.scene['MhxDirectory'], context.scene['MhxPrefix'])
		mhxrig = context.object
		for filepath in paths:
			context.scene.objects.active = mhxrig
			loadRetargetSimplify(context, filepath)
		return{'FINISHED'}	


#
#	Select or delete action
#   Delete button really deletes action. Handle with care.
#
#	listAllActions(context):
#	findAction(name):
#	OBJECT_OT_SelectButton(bpy.types.Operator):
#	class OBJECT_OT_DeleteButton(bpy.types.Operator):
#

def listAllActions(context):
	global theActions
	actions = [] 
	for act in bpy.data.actions:
		name = act.name
		actions.append((name, name, name))
	theActions = actions
	return

def setAction():
	global theActions
	bpy.types.Scene.MhxActions = EnumProperty(
		items = theActions,
		name = "Actions")
	return theActions

def findAction(name):
	global theActions
	for n,action in enumerate(theActions):
		(name1, name2, name3) = action		
		if name == name1:
			return n
	raise NameError("Unrecognized action %s" % name)

class OBJECT_OT_SelectButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_SelectButton"
	bl_label = "Select action"

	@classmethod
	def poll(cls, context):
		return context.object

	def execute(self, context):
		import bpy
		global theActions
		ob = context.ob
		name = scn.MhxActions		
		print('Select action', name)	
		try:
			act = bpy.data.actions[name]
		except:
			act = None
		if act and ob.animation_data:
			ob.animation_data.action = act

		return{'FINISHED'}	

class OBJECT_OT_DeleteButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_DeleteButton"
	bl_label = "Delete action"

	@classmethod
	def poll(cls, context):
		return context.scene.MhxReallyDelete

	def execute(self, context):
		import bpy
		global theActions
		scn = context.scene
		name = scn.MhxActions		
		print('Delete action', name)	
		try:
			act = bpy.data.actions[name]
		except:
			act = None
		if act:
			act.use_fake_user = False
			if act.users == 0:
				print("Deleting", act)
				n = findAction(name)
				theActions.pop(n)
				bpy.data.actions.remove(act)
				print('Action', act, 'deleted')
				listAllActions(context)
				setAction()
				#del act
			else:
				print("Cannot delete. %s has %d users." % (act, act.users))

		return{'FINISHED'}	

initInterface(bpy.context)

def register():
	pass

def unregister():
	pass

if __name__ == "__main__":
	register()

#readBvhFile(context, filepath, scale, startFrame, rot90, 1)
#readBvhFile(bpy.context, '/home/thomas/makehuman/bvh/Male1_bvh/Male1_A5_PickUpBox.bvh', 1.0, 1, False)
#readBvhFile(bpy.context, '/home/thomas/makehuman/bvh/cmu/10/10_03.bvh', 1.0, 1, False)
