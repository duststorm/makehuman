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

bl_info = {
	"name": "MHX Mocap",
	"author": "Thomas Larsson",
	"version": "0.5",
	"blender": (2, 5, 5),
	"api": 33590,
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
#	Supported source armatures

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

BlugArmature = {
	'hip' : 'Root',
	'lhipjoint' : 'Hip_L',
	'lfemur' : 'UpLegFK_L',
	'ltibia' : 'LoLegFK_L',
	'lfoot' : 'FootFK_L',
	'ltoes' : 'ToeFK_L',
	'rhipjoint' : 'Hip_R',
	'rfemur' : 'UpLegFK_R',
	'rtibia' : 'LoLegFK_R',
	'rfoot' : 'FootFK_R',
	'rtoes' : 'ToeFK_R',
	'lowerback' : 'Spine1',
	'upperback' : 'Spine2',
	'thorax' : 'Spine3',
	'lowerneck' : 'LowerNeck',
	'upperneck' : 'Neck',
	'head' : 'Head',
	'lclavicle' : 'Shoulder_L',
	'lhumerus' : 'UpArmFK_L',
	'lradius' : 'LoArmFK_L',
	'lwrist' : 'WristFK_L',
	'lhand' : 'HandFK_L',
	'lfingers' : None,
	'lthumb' : 'Finger1_L',
	'rclavicle' : 'Shoulder_R',
	'rhumerus' : 'UpArmFK_R',
	'rradius' : 'LoArmFK_R',
	'rwrist' : 'WristFK_R',
	'rhand' : 'HandFK_R',
	'rfingers' : None,
	'rthumb' : 'Finger1_R',
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

MaxArmature = {
	'hips' : 'Root',

	'lhipjoint' : 'Hip_L',
	'lefthip' : 'UpLegFK_L',
	'leftknee' : 'LoLegFK_L',
	'leftankle' : 'FootFK_L',
	'lefttoe' : 'ToeFK_L',

	'rhipjoint' : 'Hip_R',
	'righthip' : 'UpLegFK_R',
	'rightknee' : 'LoLegFK_R',
	'rightankle' : 'FootFK_R',
	'righttoe' : 'ToeFK_R',

	'lowerback' : 'Spine1',
	'chest' : 'Spine2',
	'chest2' : 'Spine3',
	'lowerneck' : 'LowerNeck',
	'neck' : 'Neck',
	'head' : 'Head',

	'leftcollar' : 'Shoulder_L',
	'leftshoulder' : 'UpArmFK_L',
	'leftelbow' : 'LoArmFK_L',
	'leftwrist' : 'HandFK_L',
	'lhand' : None,
	'lfingers' : None,
	'lthumb' : None,

	'rightcollar' : 'Shoulder_R',
	'rightshoulder' : 'UpArmFK_R',
	'rightelbow' : 'LoArmFK_R',
	'rightwrist' : 'HandFK_R',
	'rhand' : None,
	'rfingers' : None,
	'rthumb' : None,
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
	'Blug' : BlugArmature,
	'3dsMax' : MaxArmature,
	'McpD' : MocapDataArmature,
	'Daz' : DazArmature,
}

MBFixes = {
	'UpLegFK_L' : ( Matrix.Rotation(0.4, 3, 'Y') * Matrix.Rotation(-0.45, 3, 'Z'), None),
	'UpLegFK_R' : ( Matrix.Rotation(-0.4, 3, 'Y') * Matrix.Rotation(0.45, 3, 'Z'), None),
	'LoLegFK_L' : ( Matrix.Rotation(-0.2, 3, 'Y'), None),
	'LoLegFK_R' : ( Matrix.Rotation(0.2, 3, 'Y'), None),
	'FootFK_L'  : ( Matrix.Rotation(-0.3, 3, 'Z'), None),
	'FootFK_R'  : ( Matrix.Rotation(0.3, 3, 'Z'), None),
	'UpArmFK_L' : ( Matrix.Rotation(0.1, 3, 'X'), None),
	'UpArmFK_R' : ( Matrix.Rotation(0.1, 3, 'X'), None),
}

OsuFixes = {}

XX1Fixes = {}

MaxFixes = {
	'UpLegFK_L' : ( Matrix.Rotation(0.4, 3, 'Y') * Matrix.Rotation(-0.45, 3, 'Z'), None),
	'UpLegFK_R' : ( Matrix.Rotation(-0.4, 3, 'Y') * Matrix.Rotation(0.45, 3, 'Z'), None),
	'LoLegFK_L' : ( Matrix.Rotation(-0.2, 3, 'Y'), None),
	'LoLegFK_R' : ( Matrix.Rotation(0.2, 3, 'Y'), None),
	'FootFK_L'  : ( Matrix.Rotation(-0.3, 3, 'Z'), None),
	'FootFK_R'  : ( Matrix.Rotation(0.3, 3, 'Z'), None),

	'UpArmFK_L' :  (Matrix.Rotation(1.57, 3, 'Z'), 'XZ'),
	'LoArmFK_L' :  (None, 'XZ'),
	'HandFK_L'  :  (None, 'XZ'),
	'UpArmFK_R' :  (Matrix.Rotation(-1.57, 3, 'Z'), 'ZX'),
	'LoArmFK_R' :  (None, 'ZX'),
	'HandFK_R'  :  (None, 'ZX'),
}

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
	'Blug' : MBFixes,
	'3dsMax': MaxFixes,
	'McpD': McpdFixes,
	'Daz' : DazFixes,
}

#
#	end supported source armatures
###################################################################################
#
#	Mhx rig
#

MhxFkBoneList = [
	'Root', 'Hips', 'Spine1', 'Spine2', 'Spine3', 'LowerNeck', 'Neck', 'Head',
	'Shoulder_L', 'UpArmFK_L', 'LoArmFK_L', 'WristFK_L', 'HandFK_L', 'ElbowPTFK_L',
	'Shoulder_R', 'UpArmFK_R', 'LoArmFK_R', 'WristFK_R', 'HandFK_R', 'ElbowPTFK_R',
	'Hip_L', 'UpLegFK_L', 'LoLegFK_L', 'FootFK_L', 'ToeFK_L',
	'Hip_R', 'UpLegFK_R', 'LoLegFK_R', 'FootFK_R', 'ToeFK_R',
	'LegFK_L', 'AnkleFK_L', 'KneePTFK_L',
	'LegFK_R', 'AnkleFK_R', 'KneePTFK_R',
]

F_Rev = 1
F_LR = 2

MhxIkArmature = {
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

MhxIkBoneList = [
	'UpArmIK', 'LoArmIK', 'HandIK', 'ElbowPTIK',
	'UpLegIK', 'LoLegIK', 'LegIK', 'ToeRevIK', 'FootRevIK', 'AnkleIK', 'KneePTIK',
]

MhxGlobalBoneList = [
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

###################################################################################
#
#	Other supported target armatures
#
#	If you want to use the mocap tool for your own armature, it should suffice to 
#	modify this section (down to getParentName()).
#

T_MHX = 1
T_Rorkimaru = 2
T_Game = 3
theTarget = 0
theArmature = None

RorkimaruBones = [
	('Root',		'Root'),
	('Spine1',		'Spine1'),
	('Spine2',		'Spine3'),
	('Neck',		'Neck'),
	('Head',		'Head'),

	('Clavicle_L',	'Shoulder_L'),
	('UpArm_L',		'UpArmFK_L'),
	('LoArm_L',		'LoArmFK_L'),
	('Hand_L',		'HandFK_L'),

	('Clavicle_R',	'Shoulder_R'),
	('UpArm_R',		'UpArmFK_R'),
	('LoArm_R',		'LoArmFK_R'),
	('Hand_R',		'HandFK_R'),

	('UpLeg_L',		'UpLegFK_L'),
	('LoLeg_L',		'LoLegFK_L'),
	('Foot_L',		'FootFK_L'),
	('Toe_L',		'ToeFK_L'),

	('UpLeg_R',		'UpLegFK_R'),
	('LoLeg_R',		'LoLegFK_R'),
	('Foot_R',		'FootFK_R'),
	('Toe_R',		'ToeFK_R'),
]

GameBones = [
	('Root',		'Root'),
	('Spine1',		'Spine1'),
	('Spine2',		'Spine2'),
	('Spine3',		'Spine3'),
	('Neck',		'Neck'),
	('Head',		'Head'),

	('Clavicle_L',	'Shoulder_L'),
	('UpArm_L',		'UpArmFK_L'),
	('LoArm_L',		'LoArmFK_L'),
	('Hand_L',		'HandFK_L'),

	('Clavicle_R',	'Shoulder_R'),
	('UpArm_R',		'UpArmFK_R'),
	('LoArm_R',		'LoArmFK_R'),
	('Hand_R',		'HandFK_R'),

	('Hip_L',		'Hip_L'),
	('UpLeg_L',		'UpLegFK_L'),
	('LoLeg_L',		'LoLegFK_L'),
	('Foot_L',		'FootFK_L'),
	('Toe_L',		'ToeFK_L'),

	('Hip_R',		'Hip_R'),
	('UpLeg_R',		'UpLegFK_R'),
	('LoLeg_R',		'LoLegFK_R'),
	('Foot_R',		'FootFK_R'),
	('Toe_R',		'ToeFK_R'),
]

GameIkBones = [ 'Wrist_L', 'Wrist_R', 'Ankle_L', 'Ankle_R' ]

GameParents = {
	'MasterFloor' :	None,
	'MasterFloorInv' :	None,
	'RootInv' :		'Root',
	'HipsInv' :		'Root',
	'Hips' :		'Root',
	'Spine3Inv' :	'Spine3',
}

RorkimaruParents = {
	'MasterFloor' :	None,
	'MasterFloorInv' :	None,
	'RootInv' :		'Root',
	'HipsInv' :		'Root',
	'Hips' :		'Root',
	'Spine2Inv' :	'Spine2',
	'Spine3' :		'Spine2',
}

#
#	getTrgBone(b):
#	getSrcBone(b):
#	getParentName(b):
#

def getTrgBone(b):
	if theTarget == T_MHX:
		return b
	else:
		try:
			return theTrgBone[b]
		except:
			return None
			
def getSrcBone(b):
	if theTarget == T_MHX:
		return b
	else:
		try:
			return theSrcBone[b]
		except:
			return None			

def getParentName(b):
	if b == None:
		return None
	elif theTarget == T_MHX:
		if b == 'MasterFloor':
			return None
		else:
			return b
	elif theTarget == T_Game:
		try:
			return GameParents[b]
		except:
			return b
	elif theTarget == T_Rorkimaru:
		try:
			return RorkimaruParents[b]
		except:
			return b

#
#	guessTargetArmature(trgRig):
#	setupTargetArmature():
#	testTargetRig(bones, rigBones):
#

def guessTargetArmature(trgRig):
	global theTarget
	bones = trgRig.data.bones.keys()
	if 'KneePTFK_L' in bones:
		theTarget = T_MHX
		name = "MHX"
	elif testTargetRig(bones, GameBones):
		theTarget = T_Game
		name = "Game"
	elif testTargetRig(bones, RorkimaruBones):
		theTarget = T_Rorkimaru
		name = "Rorkimaru"
	else:
		raise NameError("Did not recognize target armature")
	setupTargetArmature()
	return

def testTargetRig(bones, rigBones):
	for (b, mb) in rigBones:
		if b not in bones:
			return False
	return True

def setupTargetArmature():
	global theFkBoneList, theIkBoneList, theGlobalBoneList, theIkArmature, theSrcBone, theTrgBone
	if theTarget == T_MHX:
		theFkBoneList = MhxFkBoneList
		theIkBoneList = MhxIkBoneList
		theIkArmature = MhxIkArmature
		theGlobalBoneList = MhxGlobalBoneList
	else:
		theFkBoneList = []
		theIkBoneList = []
		theGlobalBoneList = []
		theIkArmature = {}
		theTrgBone = {}
		theSrcBone = {}
		if theTarget == T_Rorkimaru:
			bones = RorkimaruBones
			theIkBoneList = GameIkBones
		elif theTarget == T_Game:
			bones = GameBones
			theIkBoneList = GameIkBones
		for (trg,src) in bones:
			theFkBoneList.append(trg)
			theSrcBone[trg] = src
			theTrgBone[src] = trg
			if src in MhxGlobalBoneList:
				theGlobalBoneList.append(trg)
	return

#	end supported target armatures
###################################################################################

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
			self.parent = getParentName(bone.parent.name)
		else:
			self.parent = None
		if self.parent:
			self.use_connect = bone.use_connect
		else:
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
			nameSrc = 'ToeFK'+suffix
			toe = ebones.new(name=nameSrc)
			toe.head = foot.tail
			toe.tail = toe.head - Vector((0, 0.5*foot.length, 0))
			toe.parent = foot
			bones90[nameSrc] = CEditBone(toe)
			
		nameSrc = 'LegFK'+suffix
		eb = ebones.new(name=nameSrc)
		eb.head = 2*toe.head - toe.tail
		eb.tail = 4*toe.head - 3*toe.tail
		eb.parent = toe
		bones90[nameSrc] = CEditBone(eb)

		nameSrc = 'AnkleFK'+suffix
		eb = ebones.new(name=nameSrc)
		eb.head = foot.head
		eb.tail = 2*foot.head - foot.tail
		eb.parent = ebones['LoLegFK'+suffix]
		bones90[nameSrc] = CEditBone(eb)
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
		(index, fcu) = fcuDict[name][0]
		m = len(fcu.keyframe_points)
		for (index, fcu) in fcuDict[name]:
			if len(fcu.keyframe_points) != m:
				raise NameError("Not all F-Curves for %s have the same length" % name)
		vectors = []
		for kp in range(m):
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
		if len(words) == 1:
			words = filename.split('-')
		name = 'Y_'
		if len(words) > 1:
			words = words[1:]
		for word in words:
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
#	createIKBones(srcRig):
#

def createIKBones(srcRig):
	bpy.ops.object.mode_set(mode='EDIT')
	ebones = srcRig.data.edit_bones
	for suffix in ['_L', '_R']:
		for nameIK in theIkBoneList:
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
#	constrainIkBones(srcRig):
#

def constrainIkBones(srcRig):
	bpy.ops.object.mode_set(mode='POSE')
	pbones = srcRig.pose.bones
	for pb in pbones:
		if pb.parent:
			pb.lock_location = (True, True, True)		

	for suffix in ['_L', '_R']:
		cns = pbones['LoArmIK'+suffix].constraints.new(type='IK')
		cns.target = srcRig
		cns.subtarget = 'HandIK'+suffix
		cns.chain_count = 2

		cns = pbones['LoLegIK'+suffix].constraints.new(type='IK')
		cns.target = srcRig
		cns.subtarget = 'AnkleIK'+suffix
		cns.chain_count = 2
	return

#
#	copyAnglesFKIK():
#

def copyAnglesFKIK(context):
	trgRig = context.object
	guessTargetArmature(trgRig)
	trgAnimations = createTargetAnimation(context, trgRig)
	insertAnimation(context, trgRig, trgAnimations, theFkBoneList)
	onoff = toggleLimitConstraints(trgRig)
	setLimitConstraints(trgRig, 0.0)
	print(trgRig, theTarget)
	print(trgAnimations)
	if theTarget == T_MHX:
		poseTrgIkBonesMHX(context, trgRig, trgAnimations)
	elif theTarget == T_Game or theTarget == T_Rorkimaru:
		poseTrgIkBonesGame(context, trgRig, trgAnimations)
	setInterpolation(trgRig)
	if onoff == 'OFF':
		setLimitConstraints(trgRig, 1.0)
	else:
		setLimitConstraints(trgRig, 0.0)
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
	trgRig = context.object
	rig = readBvhFile(context, filepath, context.scene)
	(rig00, bones00, action) =  renameBvhRig(rig, filepath)
	guessArmature(rig00)
	renameFKBones(bones00, rig00, action)
	setInterpolation(rig00)
	rescaleRig(context.scene, trgRig, rig00, action)
	return (rig00, action)

#
#	rescaleRig(scn, trgRig, srcRig, action):
#

def rescaleRig(scn, trgRig, srcRig, action):
	if not scn['MhxAutoScale']:
		return
	try:
		trgScale = trgRig.data.bones['UpLegFK_L'].length
	except:
		trgScale = trgRig.data.bones['UpLeg_L'].length
	srcScale = srcRig.data.bones['UpLegFK_L'].length
	scale = trgScale/srcScale
	print("Rescale %s with factor %f" % (scn.objects.active, scale))
	
	bpy.ops.object.mode_set(mode='EDIT')
	ebones = srcRig.data.edit_bones
	for eb in ebones:
		oldlen = eb.length
		eb.head *= scale
		eb.tail *= scale
	bpy.ops.object.mode_set(mode='POSE')
	for fcu in action.fcurves:
		words = fcu.data_path.split('.')
		if words[-1] == 'location':
			for kp in fcu.keyframe_points:
				kp.co[1] *= scale
	return


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

	def __repr__(self):
		return "<CAnimData n %s p %s f %d>" % (self.name, self.parent, self.nFrames)

		
#
#	createSourceAnimation(context, rig):
#	createTargetAnimation(context, rig):
#	createAnimData(name, animations, ebones, isTarget):
#

def createSourceAnimation(context, rig):
	context.scene.objects.active = rig
	animations = {}
	for name in MhxFkBoneList:
		createAnimData(name, animations, rig.data.bones, False)
	return animations

def createTargetAnimation(context, rig):
	context.scene.objects.active = rig
	animations = {}
	for name in theFkBoneList:
		createAnimData(name, animations, rig.data.bones, True)
	return animations

def createAnimData(name, animations, bones, isTarget):
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
		if isTarget:
			anim.parent = getParentName(b.parent.name)
		else:
			anim.parent = b.parent.name
	else:
		anim.parent = None
	if anim.parent:
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
def relativizeBones(srcRig, trgRig, mhxAnims):
	for bone90 in srcRig.data.bones:
		if bone90.parent:
			name = bone90.name
			pname = bone90.parent.name
			anim = mhxAnims[name]
			bone = trgRig.data.bones[name].parent
			while bone and bone.name != pname:			
				anim.matrixRel = bone.matrix * anim.matrixRel
				bone = bone.parent
			anim.inverseRel = anim.matrixRel.copy().invert()
	return
'''
#
#	insertAnimation(context, rig, animations, boneList):
#	insertAnimRoot(root, animations, nFrames, locs, rots):
#	insertAnimChild(name, animations, nFrames, rots):
#

def insertAnimation(context, rig, animations, boneList):
	context.scene.objects.active = rig
	bpy.ops.object.mode_set(mode='POSE')
	locs = makeVectorDict(rig, '].location')
	rots = makeVectorDict(rig, '].rotation_quaternion')
	root = 'Root'
	nFrames = len(locs[root])
	insertAnimRoot(root, animations, nFrames, locs[root], rots[root])
	bones = rig.data.bones
	for nameSrc in boneList:
		try:
			bones[nameSrc]
			success = (nameSrc != root)
		except:
			success = False
		if success:
			try:
				rot = rots[nameSrc]
			except:
				rot = None
			insertAnimChild(nameSrc, animations, nFrames, rot)

def insertAnimRoot(root, animations, nFrames, locs, rots):
	anim = animations[root]
	if nFrames < 0:
		nFrames = len(locs)
	anim.nFrames = nFrames
	for frame in range(anim.nFrames):
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

def insertAnimChild(name, animations, nFrames, rots):
	try:
		anim = animations[name]
	except:
		return None
	if nFrames < 0:
		nFrames = len(rots)
	animPar = animations[anim.parent]
	anim.nFrames = nFrames
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
#	poseTrgFkBones(context, trgRig, srcAnimations, trgAnimations, fixes)
#

def poseTrgFkBones(context, trgRig, srcAnimations, trgAnimations, fixes):
	context.scene.objects.active = trgRig
	bpy.ops.object.mode_set(mode='POSE')
	pbones = trgRig.pose.bones
	
	nameSrc = 'Root'
	nameTrg = getTrgBone(nameSrc)
	insertLocationKeyFrames(nameTrg, pbones[nameTrg], srcAnimations[nameSrc], trgAnimations[nameTrg])
	for nameTrg in theFkBoneList:
		nameSrc = getSrcBone(nameTrg)
		try:
			pb = pbones[nameTrg]
			animSrc = srcAnimations[nameSrc]
			animTrg =  trgAnimations[nameTrg]
			success = True
		except:
			success = False
		if not success:
			pass
		elif nameTrg in theGlobalBoneList:
			insertGlobalRotationKeyFrames(nameTrg, pb, animSrc, animTrg)
		else:
			try:
				fix = fixes[nameSrc]
			except:
				fix = None
			if fix:
				fixAndInsertLocalRotationKeyFrames(nameTrg, pb, animSrc, animTrg, fix)
			else:
				insertLocalRotationKeyFrames(nameTrg, pb, animSrc, animTrg)

	insertAnimation(context, trgRig, trgAnimations, theFkBoneList)
	if theTarget == T_MHX:
		for suffix in ['_L', '_R']:
			for name in ['ElbowPT', 'KneePT']:
				nameFK = name+'FK'+suffix
				insertAnimChild(nameFK, trgAnimations, animSrc.nFrames, None)

	setInterpolation(trgRig)
	return

#
#	insertLocationKeyFrames(name, pb, animSrc, animTrg):
#	insertGlobalRotationKeyFrames(name, pb, animSrc, animTrg):
#	insertGlobalRotationKeyFrames(name, pb, animSrc, animTrg):
#	insertReverseRotationKeyFrames(name, pb, animFK, animIK, animPar):
#

def insertLocationKeyFrames(name, pb, animSrc, animTrg):
	locs = []
	for frame in range(animSrc.nFrames):
		loc0 = animSrc.heads[frame] - animTrg.headRest
		loc = loc0 * animTrg.inverseRest
		locs.append(loc)
		pb.location = loc
		for n in range(3):
			pb.keyframe_insert('location', index=n, frame=frame, group=name)	
	return locs

def insertIKFKLocationKeyFrames(nameIK, nameFK, pb, animations):
	pb.bone.select = True
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


def insertGlobalRotationKeyFrames(name, pb, animSrc, animTrg):
	rots = []
	animTrg.nFrames = animSrc.nFrames
	for frame in range(animSrc.nFrames):
		mat90 = animSrc.matrices[frame]
		animTrg.matrices[frame] = mat90
		matMhx = animTrg.inverseRest * mat90 * animTrg.matrixRest
		rot = matMhx.to_quat()
		rots.append(rot)
		pb.rotation_quaternion = rot
		for n in range(4):
			pb.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=name)
	return rots

def insertLocalRotationKeyFrames(name, pb, animSrc, animTrg):
	animTrg.nFrames = animSrc.nFrames
	for frame in range(animSrc.nFrames):
		rot = animSrc.quats[frame]
		animTrg.quats[frame] = rot
		pb.rotation_quaternion = rot
		for n in range(4):
			pb.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=name)
	return

def fixAndInsertLocalRotationKeyFrames(name, pb, animSrc, animTrg, fix):
	(fixMat, exchange) = fix
	animTrg.nFrames = animSrc.nFrames
	for frame in range(animSrc.nFrames):
		mat90 = animSrc.quats[frame].to_matrix()
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
		pb.rotation_quaternion = rot
		animTrg.quats[frame] = rot
		for n in range(4):
			pb.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=name)
	return

def insertReverseRotationKeyFrames(name, pb, animFK, animIK, animPar):
	rots = []
	animIK.nFrames = animFK.nFrames
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
#	poseTrgIkBones(context, trgRig, trgAnimations)
#

def poseTrgIkBonesMHX(context, trgRig, trgAnimations):
	bpy.ops.object.mode_set(mode='POSE')
	pbones = trgRig.pose.bones
	for suffix in ['_L', '_R']:
		for name in ['UpArm', 'LoArm', 'UpLeg', 'LoLeg']:
			nameIK = name+'IK'+suffix
			nameFK = name+'FK'+suffix
			createAnimData(nameIK, trgAnimations, trgRig.data.bones, True)		
			insertLocalRotationKeyFrames(nameIK, pbones[nameIK], trgAnimations[nameFK], trgAnimations[nameIK])

		for name in ['Hand', 'Leg']:
			nameIK = name+'IK'+suffix
			nameFK = name+'FK'+suffix
			createAnimData(nameIK, trgAnimations, trgRig.data.bones, True)		
			animFK = trgAnimations[nameFK]
			animIK = trgAnimations[nameIK]
			locs = insertLocationKeyFrames(nameIK, pbones[nameIK], animFK, animIK)
			rots = insertGlobalRotationKeyFrames(nameIK, pbones[nameIK],animFK, animIK)
			insertAnimRoot(nameIK, trgAnimations, -1, locs, rots)

		for name in ['ElbowPT', 'KneePT']:
			nameIK = name+'IK'+suffix
			nameFK = name+'FK'+suffix
			createAnimData(nameIK, trgAnimations, trgRig.data.bones, True)		
			insertIKFKLocationKeyFrames(nameIK, nameFK, pbones[nameIK], trgAnimations)

		for name in ['Toe', 'Foot']:
			nameIK = name+'RevIK'+suffix
			nameFK = name+'FK'+suffix
			createAnimData(nameIK, trgAnimations, trgRig.data.bones, True)		
			animFK = trgAnimations[nameFK]
			animIK = trgAnimations[nameIK]
			rots = insertReverseRotationKeyFrames(nameIK, pbones[nameIK], animFK, animIK, trgAnimations[animIK.parent])
			insertAnimChild(nameIK, trgAnimations, -1, rots)
	return

def poseTrgIkBonesGame(context, trgRig, trgAnimations):
	bpy.ops.object.mode_set(mode='POSE')
	pbones = trgRig.pose.bones
	for suffix in ['_L', '_R']:
		for (namefk, nameik) in [('Hand', 'Wrist'), ('Foot', 'Ankle')]:
			nameIK = nameik+suffix
			nameFK = namefk+suffix
			createAnimData(nameIK, trgAnimations, trgRig.data.bones, True)		
			animFK = trgAnimations[nameFK]
			animIK = trgAnimations[nameIK]
			locs = insertLocationKeyFrames(nameIK, pbones[nameIK], animFK, animIK)
			#rots = insertGlobalRotationKeyFrames(nameIK, pbones[nameIK],animFK, animIK)
			#insertAnimRoot(nameIK, trgAnimations, -1, locs, rots)
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

		for nameIK in theIkBoneList:
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
#	retargetMhxRig(context, srcRig, trgRig):
#

def retargetMhxRig(context, srcRig, trgRig):
	scn = context.scene
	setArmature(srcRig)
	print("Retarget %s --> %s" % (srcRig, trgRig))
	if trgRig.animation_data:
		trgRig.animation_data.action = None

	trgAnimations = createTargetAnimation(context, trgRig)
	srcAnimations = createSourceAnimation(context, srcRig)
	insertAnimation(context, srcRig, srcAnimations, MhxFkBoneList)
	onoff = toggleLimitConstraints(trgRig)
	setLimitConstraints(trgRig, 0.0)
	if scn['MhxApplyFixes']:
		fixes = FixesList[srcRig['MhxArmature']]
	else:
		fixes = None
	poseTrgFkBones(context, trgRig, srcAnimations, trgAnimations, fixes)
	if theTarget == T_MHX:
		poseTrgIkBonesMHX(context, trgRig, trgAnimations)
	elif theTarget == T_Game or theTarget == T_Rorkimaru:
		poseTrgIkBonesGame(context, trgRig, trgAnimations)
	setInterpolation(trgRig)
	if onoff == 'OFF':
		setLimitConstraints(trgRig, 1.0)
	else:
		setLimitConstraints(trgRig, 0.0)

	trgRig.animation_data.action.name = trgRig.name[:4] + srcRig.name[2:]
	print("Retargeted %s --> %s" % (srcRig, trgRig))
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
#	togglePoleTargets(trgRig):
#	toggleIKLimits(trgRig):
#	toggleLimitConstraints(trgRig):
#	setLimitConstraints(trgRig, inf):
#

def togglePoleTargets(trgRig):
	bones = trgRig.data.bones
	pbones = trgRig.pose.bones
	if bones['ElbowPTIK_L'].hide:
		hide = False
		poletar = trgRig
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

def toggleIKLimits(trgRig):
	pbones = trgRig.pose.bones
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

def toggleLimitConstraints(trgRig):
	pbones = trgRig.pose.bones
	first = True
	for pb in pbones:
		if onUserLayer(pb.bone.layers):
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
	if first:
		return 'NOT FOUND'
	return res

def onUserLayer(layers):
	for n in [0,1,2,3,4,5,6,7, 9,10,11,12,13]:
		if layers[n]:
			return True
	return False

def setLimitConstraints(trgRig, inf):
	pbones = trgRig.pose.bones
	for pb in pbones:
		if onUserLayer(pb.bone.layers):
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
	bpy.types.Scene.MhxBvhScale = FloatProperty(
		name="Scale", 
		description="Scale the BVH by this value", 
		min=0.0001, max=1000000.0, 
		soft_min=0.001, soft_max=100.0,
		default=0.65)

	bpy.types.Scene.MhxAutoScale = BoolProperty(
		name="Auto scale",
		description="Rescale skeleton to match target",
		default=True)

	bpy.types.Scene.MhxStartFrame = IntProperty(
		name="Start Frame", 
		description="Starting frame for the animation",
		default=1)

	bpy.types.Scene.MhxEndFrame = IntProperty(
		name="Last Frame", 
		description="Last frame for the animation",
		default=32000)

	bpy.types.Scene.MhxSubsample = IntProperty(
		name="Subsample", 
		description="Sample only every n:th frame",
		default=1)

	bpy.types.Scene.MhxDefaultSS = BoolProperty(
		name="Use default subsample",
		default=True)

	bpy.types.Scene.MhxRot90Anim = BoolProperty(
		name="Rotate 90 deg", 
		description="Rotate 90 degress so Z points up",
		default=True)

	bpy.types.Scene.MhxDoSimplify = BoolProperty(
		name="Simplify FCurves", 
		description="Simplify FCurves",
		default=True)

	bpy.types.Scene.MhxApplyFixes = BoolProperty(
		name="Apply found fixes", 
		description="Apply found fixes",
		default=True)

	bpy.types.Scene.MhxPlantCurrent = BoolProperty(
		name="Use current", 
		description="Plant at current",
		default=True)

	bpy.types.Scene.MhxPlantLoc = BoolProperty(
		name="Loc", 
		description="Plant location keys",
		default=True)

	bpy.types.Scene.MhxPlantRot = BoolProperty(
		name="Rot", 
		description="Plant rotation keys",
		default=False)

	bpy.types.Scene.MhxErrorLoc = FloatProperty(
		name="Max loc error", 
		description="Max error for location FCurves when doing simplification",
		min=0.001,
		default=0.01)

	bpy.types.Scene.MhxErrorRot = FloatProperty(
		name="Max rot error", 
		description="Max error for rotation (degrees) FCurves when doing simplification",
		min=0.001,
		default=0.1)

	bpy.types.Scene.MhxDirectory = StringProperty(
		name="Directory", 
		description="Directory", 
		maxlen=1024,
		default='')

	bpy.types.Scene.MhxReallyDelete = BoolProperty(
		name="Really delete action", 
		description="Delete button deletes action permanently",
		default=False)

	bpy.types.Scene.MhxPrefix = StringProperty(
		name="Prefix", 
		description="Prefix", 
		maxlen=1024,
		default='')

	scn = context.scene
	if scn:
		scn['MhxPlantCurrent'] = True
		scn['MhxPlantLoc'] = True
		scn['MhxBvhScale'] = 0.65
		scn['MhxAutoScale'] = True
		scn['MhxStartFrame'] = 1
		scn['MhxEndFrame'] = 32000
		scn['MhxSubsample'] = 1
		scn['MhxDefaultSS'] = True
		scn['MhxRot90Anim'] = True
		scn['MhxDoSimplify'] = True
		scn['MhxApplyFixes'] = True

		scn['MhxPlantLoc'] = True
		scn['MhxPlantRot'] = False
		scn['MhxErrorLoc'] = 0.01
		scn['MhxErrorRot'] = 0.1

		scn['MhxPrefix'] = "Female1_A"
		scn['MhxDirectory'] = "~/makehuman/bvh/Female1_bvh"
		scn['MhxReallyDelete'] = False
		listAllActions(context)
		setAction()
	else:
		print("Warning - no scene - scene properties not set")

	bpy.types.Object.MhxArmature = StringProperty()

	'''
	for mhx in theFkBoneList:
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
	if not context.scene:
		return
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
	if not context.scene:
		return
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
		for mhx in theFkBoneList:
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
		layout.prop(scn, "MhxAutoScale")
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
		guessTargetArmature(context.object)
		importAndRename(context, self.properties.filepath)
		print("%s imported" % self.properties.filepath)
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}	

#
#	class OBJECT_OT_RetargetMhxButton(bpy.types.Operator):
#

class OBJECT_OT_RetargetMhxButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_RetargetMhxButton"
	bl_label = "Retarget selected to MHX"

	def execute(self, context):
		import bpy, mathutils
		trgRig = context.object
		guessTargetArmature(trgRig)
		for srcRig in context.selected_objects:
			if srcRig != trgRig:
				retargetMhxRig(context, srcRig, trgRig)
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
	trgRig = context.object
	(srcRig, action) = importAndRename(context, filepath)
	retargetMhxRig(context, srcRig, trgRig)
	if context.scene['MhxDoSimplify']:
		simplifyFCurves(context, trgRig)
	deleteFKRig(context, srcRig, action, 'Y_')
	time2 = time.clock()
	print("%s finished in %.3f s" % (filepath, time2-time1))
	return

class OBJECT_OT_LoadRetargetSimplifyButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_LoadRetargetSimplifyButton"
	bl_label = "Load, retarget, simplify"
	filepath = StringProperty(name="File Path", description="Filepath used for importing the BVH file", maxlen=1024, default="")

	def execute(self, context):
		import bpy, os, mathutils
		guessTargetArmature(context.object)
		loadRetargetSimplify(context, self.properties.filepath)
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
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
		trgRig = context.object
		for filepath in paths:
			context.scene.objects.active = trgRig
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
