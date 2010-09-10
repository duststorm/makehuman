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
    "version": 0.1,
    "blender": (2, 5, 3),
    "api": 31683,
    "location": "View3D > Properties > MHX Mocap",
    "description": "Mocap tool for MHX rig",
    "warning": "",
    "category": "3D View"}

"""
Run from text window. 
Access from UI panel (N-key) when MHX rig is active.
Buttons:
Load BVH file (.bvh): 
	Load bvh file with Z up
Retarget selected to MHX: 
	Retarget actions of selected BVH rigs to the active MHX rig.
Load BVH and retarget rig:
	Load bvh file and retarget the action to the active MHX rig.
Batch load BVH and retarget rig:
	Load all bvh files in the given directory, whose name start with the
	given prefix, and create actions for the active MHX rig.
"""

MAJOR_VERSION = 0
MINOR_VERSION = 1
BLENDER_VERSION = (2, 53, 1)

import bpy, os, mathutils, math
from mathutils import *
from bpy.props import *

#
#	FkArmature
#

FkArmature = {
	'Hips' : ('Root', None),
	'ToSpine' :  ('Spine1', 'Root'),
	'Spine' :  ('Spine2', 'Spine1'),
	'Spine1' :  ('Spine3', 'Spine2'),
	'Neck' :  ('Neck', 'Spine3'),
	'Head' :  ('Head', 'Neck'),

	'LeftShoulder' :  ('Clavicle_L', 'Spine3'),
	'LeftArm' :  ('UpArmFK_L', 'Clavicle_L'),
	'LeftForeArm' :  ('LoArmFK_L', 'UpArmFK_L'),
	'LeftHand' :  ('HandFK_L', 'LoArmFK_L'),

	'RightShoulder' :  ('Clavicle_R', 'Spine3'),
	'RightArm' :  ('UpArmFK_R', 'Clavicle_R'),
	'RightForeArm' :  ('LoArmFK_R', 'UpArmFK_R'),
	'RightHand' :  ('HandFK_R', 'LoArmFK_R'),

	'LeftUpLeg' :  ('UpLegFK_L', 'Root'),
	'LeftLeg' :  ('LoLegFK_L', 'UpLegFK_L'),
	'LeftFoot' :  ('FootFK_L', 'LoLegFK_L'),
	'LeftToeBase' :  ('ToeFK_L', 'FootFK_L'),

	'RightUpLeg' :  ('UpLegFK_R', 'Root'),
	'RightLeg' :  ('LoLegFK_R', 'UpLegFK_R'),
	'RightFoot' :  ('FootFK_R', 'LoLegFK_R'),
	'RightToeBase' :  ('ToeFK_R', 'FootFK_R'),
}

FkAmtList = [
	'Root', 'Spine1', 'Spine2', 'Spine3', 'Neck', 'Head',
	'Clavicle_L', 'UpArmFK_L', 'LoArmFK_L', 'HandFK_L',
	'Clavicle_R', 'UpArmFK_R', 'LoArmFK_R', 'HandFK_R',
	'UpLegFK_L', 'LoLegFK_L', 'FootFK_L', 'ToeFK_L',
	'UpLegFK_R', 'LoLegFK_R', 'FootFK_R', 'ToeFK_R',
	'LegFK_L', 'AnkleFK_L',
	'LegFK_R', 'AnkleFK_R',
]

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
#	createFKRig(scn, bones, rig):
#

def createFKRig(scn, bones, rig):
	amt = bpy.data.armatures.new(rig.data.name[2:])
	rig90 = bpy.data.objects.new(rig.name[2:], amt)
	scn.objects.link(rig90)
	scn.objects.active = rig90

	bpy.ops.object.mode_set(mode='EDIT')
	ebones = amt.edit_bones
	for bone in bones:
		(name90, parent) = FkArmature[bone.name]
		eb = ebones.new(name=name90)
		eb.head = rot90(bone.head)
		eb.tail = rot90(bone.tail)
		if bone.parent:
			eb.parent = ebones[parent]
			eb.use_connect = bone.use_connect
		eb.roll = bone.roll
	bones90 = []

	for suffix in ['_L', '_R']:
		eb = ebones.new(name='LegFK'+suffix)
		toe = ebones['ToeFK'+suffix]
		eb.head = 2*toe.head - toe.tail
		eb.tail = 4*toe.head - 3*toe.tail
		eb.parent = toe

		eb = ebones.new(name='AnkleFK'+suffix)
		foot = ebones['FootFK'+suffix]
		eb.head = foot.head
		eb.tail = 2*foot.head - foot.tail
		eb.parent = ebones['LoLegFK'+suffix]

	for bone in rig90.data.edit_bones:
		bones90.append( CEditBone(bone) )

	bpy.ops.object.mode_set(mode='POSE')
	return (rig90, bones90)

def rot90(vec):
	#return vec
	return (vec[0], -vec[2], vec[1])

def printMatrices(name, bones, bones90):
	n = 0
	while bones[n].name != name:
		n += 1
	print(name)
	print(bones[n].matrix)
	print(bones90[n].matrix)

#
#	setupTranformMatrix(bones, bones90):
#

def setupTranformMatrix(bones, bones90):
	tMatrix = {}
	tInverse = {}
	tRot90 = Matrix.Rotation(-math.pi/2, 3, 'X')
	for n in range(len(bones)):
		bone = bones[n]
		newBone = bones90[n]
		tMatrix[bone.name] = newBone.matrix * tRot90 * bone.inverse
		tInverse[bone.name] = tMatrix[bone.name].copy().invert()
	return (tMatrix, tInverse)

#
#	insertAction(bones00, rig00, rig90, tMatrix, tInverse):
#

def insertAction(bones00, rig00, rig90, tMatrix, tInverse):
	locs = makeVectorDict(rig00, '].location')
	rots = makeVectorDict(rig00, '].rotation_quaternion')
	root = bones00[0]
	nFrames = len(rots[root.name])

	for frame in range(nFrames):
		for bone in bones00:
			name00 = bone.name
			(name90, parent) = FkArmature[name00]
			pb = rig90.pose.bones[name90]
			
			try:
				vec = Vector(locs[name00][frame])
			except:
				vec = None
			if vec:
				nloc = tMatrix[name00] * vec
				pb.location = nloc
				for n in range(3):
					pb.keyframe_insert('location', index=n, frame=frame, group=name90)

			try:
				quat = Quaternion(rots[name00][frame])
			except:
				quat = None
			if quat:
				mat = quat.to_matrix()
				nmat = tMatrix[name00] * mat * tInverse[name00]
				pb.rotation_quaternion = nmat.to_quat()
				for n in range(4):
					pb.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=name90)

		frame += 1
	return

#
#	rotateRig90(context, rig00, bones00):
#

def rotateRig90(context, rig00, bones00):
	(rig90, bones90) = createFKRig(context.scene, bones00, rig00)
	(tMatrix, tInverse) = setupTranformMatrix(bones00, bones90)
	insertAction(bones00, rig00, rig90, tMatrix, tInverse)
	return rig90

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
	(name, ext) = os.path.splitext(base)
	rig00.name = 'Y_'+name
	action = rig00.animation_data.action
	action.name = 'Y_'+name

	bones00 = []
	bpy.ops.object.mode_set(mode='EDIT')
	for bone in rig00.data.edit_bones:
		bones00.append( CEditBone(bone) )
	bpy.ops.object.mode_set(mode='POSE')

	return (rig00, bones00, action)

#
#	createIKBones(rig90):
#

F_Rev = 1
F_LR = 2

IkArmature = {
	'UpArmIK' : ('UpArmFK', F_LR, 'Clavicle'),
	'LoArmIK' : ('LoArmFK', F_LR, 'UpArmIK'),
	'HandIK' : ('HandFK', 0, None),

	'UpLegIK' : ('UpLegFK', 0, 'Root'),
	'LoLegIK' : ('LoLegFK', F_LR, 'UpLegIK'),
	#'FootIK' : ('FootFK', 0, None),
	#'ToeIK' : ('ToeFK', F_LR, 'FootIK'),

	'LegIK' : ('LegFK', 0, None),
	'ToeRevIK' : ('ToeFK', F_LR+F_Rev, 'LegIK'),
	'FootRevIK' : ('FootFK', F_LR+F_Rev, 'ToeRevIK'),
	'AnkleIK' : ('AnkleFK', F_LR, 'FootRevIK'),
}

IkAmtList = [
	'UpArmIK', 'LoArmIK', 'HandIK',
	'UpLegIK', 'LoLegIK', 'LegIK', 'ToeRevIK', 'FootRevIK', 'AnkleIK'
]

def createIKBones(rig90):
	bpy.ops.object.mode_set(mode='EDIT')
	ebones = rig90.data.edit_bones
	for suffix in ['_L', '_R']:
		for nameIK in IkAmtList:
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

		self.headMhxRest = None
		self.vecMhxRest = None
		self.tailMhxRest = None
		self.offsetMhxRest = None
		self.matrixMhxRest = None
		self.inverseMhxRest = None

		self.heads = {}
		self.tails = {}
		self.quats = {}
		self.matrices = {}
		self.name = name
		
#
#	createAnimData(name, animations, ebones):
#

def createAnimData(name, animations, ebones):
	eb = ebones[name]
	anim = CAnimData(name)
	animations[name] = anim
	anim.headRest = eb.head.copy()
	anim.tailRest = eb.tail.copy()
	anim.vecRest = anim.tailRest - anim.headRest
	matrix = eb.matrix.rotation_part()
	if eb.parent:
		anim.parent = eb.parent.name
		animPar = animations[anim.parent]
		anim.offsetRest = anim.headRest - animPar.headRest
	else:
		anim.offsetRest = Vector((0,0,0))	
	anim.matrixRest = matrix
	anim.inverseRest = anim.matrixRest.copy().invert()
	return anim

#
#	createAnimation(context, rig):
#	insertAnimation(context, rig, animations):
#	insertAnimRoot(root, animations, nFrames, locs, rots):
#	insertAnimChild(name, animations, rots):
#

def createAnimation(context, rig):
	context.scene.objects.active = rig
	animations = {}
	bpy.ops.object.mode_set(mode='EDIT')
	for name in FkAmtList:
		createAnimData(name, animations, rig.data.edit_bones)
	bpy.ops.object.mode_set(mode='POSE')
	return animations

def insertAnimation(context, rig, animations):
	context.scene.objects.active = rig
	bpy.ops.object.mode_set(mode='POSE')
	locs = makeVectorDict(rig, '].location')
	rots = makeVectorDict(rig, '].rotation_quaternion')
	root = 'Root'
	insertAnimRoot(root, animations, len(rots[root]), locs[root], rots[root])
	for name in FkAmtList:
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
		anim.heads[frame] = anim.matrixRest * Vector(locs[frame]) + anim.headRest
		anim.tails[frame] = anim.heads[frame] + matrix*anim.vecRest
	return

def insertAnimChild(name, animations, rots):
	anim = animations[name]
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
		anim.heads[frame] = animPar.heads[frame] + parmat*anim.offsetRest
		anim.tails[frame] = anim.heads[frame] + matrix*anim.vecRest
	return


#
#	createEmpties(context, animations):
#	For debugging
#

def createEmpties(context, animations):
	for name in FkAmtList:
		anim = animations[name]
		createEmpty(context, name+'HD', anim.heads, anim.nFrames)
		createEmpty(context, name+'TL', anim.tails, anim.nFrames)
	return

def createEmpty(context, name, locs, nFrames):
	empty = bpy.data.objects.new(name, None)
	empty.show_name = True
	empty.layers[1] = True
	empty.layers[0] = False
	context.scene.objects.link(empty)
	for frame in range(nFrames):
		empty.location = locs[frame]
		for n in range(3):
			empty.keyframe_insert('location', index=n, frame=frame, group=name)
	return
		
#
#		poseMhxFKBones(context, mhxrig, rig90Animations, mhxAnimations)
#

def poseMhxFKBones(context, mhxrig, rig90Animations, mhxAnimations):
	context.scene.objects.active = mhxrig
	bpy.ops.object.mode_set(mode='POSE')
	pbones = mhxrig.pose.bones

	root = 'Root'
	anim = rig90Animations[root]
	pb = pbones[root]
	for frame in range(anim.nFrames):
		pb.location = anim.heads[frame]
		for n in range(3):
			pb.keyframe_insert('location', index=n, frame=frame, group=root)	

	for name in FkAmtList:
		anim = rig90Animations[name]
		pb = pbones[name]
		for frame in range(anim.nFrames):
			quat = anim.quats[frame]
			pb.rotation_quaternion = quat
			for n in range(4):
				pb.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=name)

	insertAnimation(context, mhxrig, mhxAnimations)
	return

#
#	poseMhxIKBones(context, mhxrig, mhxAnimations)
#

def poseMhxIKBones(context, mhxrig, mhxAnimations):
	bpy.ops.object.mode_set(mode='POSE')
	pbones = mhxrig.pose.bones
	for suffix in ['_L', '_R']:
		for name in ['UpArm', 'LoArm', 'UpLeg', 'LoLeg']:
			nameIK = name+'IK'+suffix
			anim = mhxAnimations[name+'FK'+suffix]
			pbIK = pbones[nameIK]
			print(pbIK, anim.nFrames)
			for frame in range(anim.nFrames):
				quat = anim.quats[frame]
				pbIK.rotation_quaternion = quat
				for n in range(4):
					pbIK.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=nameIK)

		for name in ['Hand', 'Leg']:
			nameIK = name+'IK'+suffix
			anim = mhxAnimations[name+'FK'+suffix]
			pbIK = pbones[nameIK]
			locs = []
			rots = []
			for frame in range(anim.nFrames):
				loc = anim.inverseRest * (anim.heads[frame] - anim.headRest)
				pbIK.location = loc
				locs.append(loc)
				mat = anim.inverseRest * anim.matrices[frame] * anim.matrixRest
				quat = mat.to_quat()
				pbIK.rotation_quaternion = quat
				rots.append(quat)
				for n in range(3):
					pbIK.keyframe_insert('location', index=n, frame=frame, group=nameIK)
				for n in range(4):
					pbIK.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=nameIK)
			bpy.ops.object.mode_set(mode='EDIT')
			createAnimData(nameIK, mhxAnimations, mhxrig.data.edit_bones)		
			bpy.ops.object.mode_set(mode='POSE')
			insertAnimRoot(nameIK, mhxAnimations, anim.nFrames, locs, rots)

		mirror = Matrix.Rotation(math.pi, 3, 'Z')
		for name in ['Toe', 'Foot']:
			nameIK = name+'RevIK'+suffix
			bpy.ops.object.mode_set(mode='EDIT')
			animIK = createAnimData(nameIK, mhxAnimations, mhxrig.data.edit_bones)		
			bpy.ops.object.mode_set(mode='POSE')
			animFK = mhxAnimations[name+'FK'+suffix]
			animPar = mhxAnimations[animIK.parent]
			pbIK = pbones[nameIK]
			rots = []
			for frame in range(anim.nFrames):
				locmat = animPar.matrices[frame].copy().invert() * animFK.matrices[frame]
				mat = animIK.inverseRest * locmat * animIK.matrixRest
				quat = mat.to_quat()
				pbIK.rotation_quaternion = quat
				rots.append(quat)
				for n in range(4):
					pbIK.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=nameIK)
			insertAnimChild(nameIK, mhxAnimations, rots)
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

		for nameIK in IkAmtList:
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

#
#	retargetMhxRig(context, rig90, mhxrig):
#

def retargetMhxRig(context, rig90, mhxrig):
	print("Retarget %s --> %s" % (rig90, mhxrig))
	if mhxrig.animation_data:
		mhxrig.animation_data.action = None
	#silenceConstraints(mhxrig)

	mhxAnimations = createAnimation(context, mhxrig)
	rig90Animations = createAnimation(context, rig90)
	insertAnimation(context, rig90, rig90Animations)
	poseMhxFKBones(context, mhxrig, rig90Animations, mhxAnimations)

	#simplifyFCurves(context, mhxrig)

	mhxAnimations = createAnimation(context, mhxrig)
	insertAnimation(context, mhxrig, mhxAnimations)
	poseMhxIKBones(context, mhxrig, mhxAnimations)

	words = rig90.name.split('_')
	name = '_'.join([mhxrig.name] + words[1:])
	mhxrig.animation_data.action.name = name
	return

#
#	deleteFKRig(context, rig00, action):
#

def deleteFKRig(context, rig00, action):
	context.scene.objects.unlink(rig00)
	bpy.data.objects.remove(rig00)
	del rig00
	if bpy.data.actions:
		for act in bpy.data.actions:
			if act.name[0:2] == 'Y_':
				act.use_fake_user = False
				bpy.data.actions.remove(act)
				del act
	return

#
#	simplifyFCurves(context, mhxrig):
#

def simplifyFCurves(context, mhxrig):
	if not context.scene.MhxDoSimplify:
		return
	try:
		act = mhxrig.animation_data.action
	except:
		act = None
	if not act:
		print("No FCurves to simplify")
		return

	maxErrLoc = context.scene.MhxErrorLoc
	maxErrRot = context.scene.MhxErrorRot * math.pi/180
	for fcu in act.fcurves:
		simplifyFCurve(fcu, act, maxErrLoc, maxErrRot)
	return

#
#	simplifyFCurve(fcu, act, maxErrLoc, maxErrRot):
#

def simplifyFCurve(fcu, act, maxErrLoc, maxErrRot):
	print(fcu.data_path)
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
		newVerts.append(points[n].co)

	path = fcu.data_path
	index = fcu.array_index
	grp = fcu.group.name
	act.fcurves.remove(fcu)
	nfcu = act.fcurves.new(path, index, grp)
	for co in newVerts:
		nfcu.keyframe_points.add(frame=co[0], value=co[1])

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
#	User interface
#	getBvh(mhx)
#	init()
#

def getBvh(mhx):
	for (bvh, value) in FkArmature.items():
		(mhx1, parent) = value
		if mhx == mhx1:
			return bvh
	return None

def init(scn):
	bpy.types.Scene.BoolProperty(
		attr= "MhxDoSimplify", 
		name="Simplify FCurves", 
		description="Simplify FCurves")
	scn['MhxDoSimplify'] = True

	bpy.types.Scene.FloatProperty(
		attr= "MhxErrorLoc", 
		name="Max loc error", 
		description="Max error for location FCurves when doing simplification",
		min=0.001)
	scn['MhxErrorLoc'] = 0.1

	bpy.types.Scene.FloatProperty(
		attr= "MhxErrorRot", 
		name="Max rot error", 
		description="Max error for rotation (degrees) FCurves when doing simplification",
		min=0.001)
	scn['MhxErrorRot'] = 1.0

	bpy.types.Scene.StringProperty(
		attr= "MhxDirectory", 
		name="Directory", 
		description="Directory", 
		maxlen=1024)
	scn['MhxDirectory'] = "~/makehuman/bvh/Female1_bvh"

	bpy.types.Scene.StringProperty(
		attr="MhxPrefix", 
		name="Prefix", 
		description="Prefix", 
		maxlen=1024)
	scn['MhxPrefix'] = "Female1_A"

	for mhx in FkAmtList:
		bpy.types.Scene.StringProperty(
			attr=mhx, 
			name=mhx, 
			description="Bvh bone corresponding to %s" % mhx, 
			default = ''
		)
		bvh = getBvh(mhx)
		if bvh:
			scn[mhx] = bvh
	return

init(bpy.context.scene)

#
#	class MhxBvhAssocPanel(bpy.types.Panel):
#

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
		for mhx in FkAmtList:
			try:				
				layout.prop(context.scene, mhx)
			except:
				pass
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
			try:
				return context.object['MhxRig']
			except:
				pass
		return False

	def draw(self, context):
		layout = self.layout
		scn = context.scene
		layout.prop(scn, "MhxDoSimplify")
		layout.prop(scn, "MhxErrorLoc")
		layout.prop(scn, "MhxErrorRot")
		layout.operator("object.LoadBvhButton")
		layout.operator("object.RetargetMhxButton")
		layout.operator("object.SimplifyFCurvesButton")
		layout.separator()
		layout.operator("object.LoadRetargetSimplifyButton")
		layout.prop(scn, "MhxDirectory")
		layout.prop(scn, "MhxPrefix")
		layout.operator("object.BatchButton")
		return

#
#	importAndRename(context, filepath, scale, frame_start, loop):
#	class OBJECT_OT_LoadBvhButton(bpy.types.Operator):
#
import sys
bvhPath = os.path.realpath('./2.53/scripts/op/io_anim_bvh')
if bvhPath not in sys.path:
	sys.path.append(bvhPath)
import import_bvh

def importAndRename(context, filepath, scale, frame_start, loop):
	bvh_nodes = import_bvh.read_bvh(context, filepath,
		ROT_MODE='QUATERNION',
		GLOBAL_SCALE=scale)
	import_bvh.bvh_node_dict2armature(context, bvh_nodes,
		ROT_MODE='QUATERNION',
		IMPORT_START_FRAME=frame_start,
		IMPORT_LOOP=loop)
	(rig00, bones00, action) =  renameBvhRig(context.object, filepath)
	rig90 = rotateRig90(context, rig00, bones00)
	deleteFKRig(context, rig00, action)
	return (rig90, action)

class OBJECT_OT_LoadBvhButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_LoadBvhButton"
	bl_label = "Load BVH file (.bvh)"
	filepath = StringProperty(name="File Path", description="Filepath used for importing the OBJ file", maxlen=1024, default="")
	scale = FloatProperty(name="Scale", description="Scale the BVH by this value", min=0.0001, max=1000000.0, soft_min=0.001, soft_max=100.0, default=0.1)
	frame_start = IntProperty(name="Start Frame", description="Starting frame for the animation", default=1)
	loop = BoolProperty(name="Loop", description="Loop the animation playback", default=False)

	def execute(self, context):
		import bpy, os, import_bvh
		importAndRename(context, self.properties.filepath, self.properties.scale, self.properties.frame_start, self.properties.loop)
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
				print("Done retarget %s --> %s" % (rig90, mhxrig))
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
#	loadRetargetSimplify(context, filepath, scale, frame_start, loop):
#	class OBJECT_OT_LoadRetargetSimplify(bpy.types.Operator):
#

def loadRetargetSimplify(context, filepath, scale, frame_start, loop):
	print("Load and retarget %s" % filepath)
	mhxrig = context.object
	(rig90, action) = importAndRename(context, filepath, scale, frame_start, loop)
	print(rig90, action)
	retargetMhxRig(context, rig90, mhxrig)
	deleteFKRig(context, rig90, action)
	print("%s finished" % filepath)
	return

class OBJECT_OT_LoadRetargetSimplifyButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_LoadRetargetSimplifyButton"
	bl_label = "Load, retarget, simplify"
	filepath = StringProperty(name="File Path", description="Filepath used for importing the OBJ file", maxlen=1024, default="")
	scale = FloatProperty(name="Scale", description="Scale the BVH by this value", min=0.0001, max=1000000.0, soft_min=0.001, soft_max=100.0, default=0.1)
	frame_start = IntProperty(name="Start Frame", description="Starting frame for the animation", default=1)
	loop = BoolProperty(name="Loop", description="Loop the animation playback", default=False)

	def execute(self, context):
		import bpy, os, import_bvh, mathutils
		loadRetargetSimplify(context, self.properties.filepath, self.properties.scale, self.properties.frame_start, self.properties.loop)
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
	bl_label = "Batch load BVH and retarget rig"

	def execute(self, context):
		import bpy, os, import_bvh, mathutils
		paths = readDirectory(context.scene['MhxDirectory'], context.scene['MhxPrefix'])
		for filepath in paths:
			loadAndRetarget(context, filepath, 0.1, 1, False)
		return{'FINISHED'}	

#retargetMhxRig(bpy.context)


