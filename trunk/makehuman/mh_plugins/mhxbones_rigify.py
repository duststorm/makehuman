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
Definition of bones for creation of a rig within MakeHuman.

TO DO

"""

__docformat__ = 'restructuredtext'

import aljabr
from aljabr import *

F_CON = True

#
#	List of joints
#	Those are the diamonds in the MH mesh
#


palmEps = 2.5

joints = dict({
  'root_head' : 'r-ankle' ,
  'root_tail' : 'l-ankle' ,
  'pelvis_head' : 'spine3',
  'pelvis_tail' : 'pelvis' ,
  'torso_head' : 'spine3' ,
  'torso_tail' : 'spine2' ,
  'spine.01_head' : 'pelvis' ,
  'spine.01_tail' : 'spine3' ,
  'spine.02_tail' : 'spine3' ,
  'spine.03_tail' : 'spine2' ,
  'spine.04_tail' : 'spine1' ,
  'neck_base_tail' : 'neck' ,
  'head_tail' : 'head' ,
  'neck.01_head' : 'neck' ,
  'neck.01_tail' : 'head' ,
  'neck.02_tail' : [(1.5,'head') , (-0.5,'neck')] ,
  'neck.03_tail' : [(2,'head') , (-1,'neck')] ,

  'DLT-shoulder.L_head' :'r-clavicle'  ,
  'DLT-shoulder.L_tail' : 'r-shoulder' ,
  'shoulder.L_head' : 'r-clavicle' ,
  'shoulder.L_tail' : 'r-shoulder' ,
  'DLT-upper_arm.L_head' : 'r-shoulder' ,
  'DLT-upper_arm.L_tail' : [(0.25,'r-elbow') , (0.75, 'r-shoulder')] ,
  'upper_arm.L_head' : 'r-shoulder' ,
  'upper_arm.L_tail' : 'r-elbow' ,
  'forearm.L_tail' : 'r-hand' ,
  'hand.L_tail' : [(0.7,'r-hand') , (0.3,'r-finger-3-1')] ,
  'palm.04.L_head' : [(palmEps,'r-finger-5-1') , (1-palmEps,'r-finger-5-2')] ,
  'palm.04.L_tail' : 'r-finger-5-1'  ,
  'finger_pinky.01.L_tail' : 'r-finger-5-2' ,
  'finger_pinky.02.L_tail' : 'r-finger-5-3' ,
  'finger_pinky.03.L_tail' : [(2,'r-finger-5-3') , (-1,'r-finger-5-2')] ,
  'palm.03.L_head' : [(palmEps,'r-finger-4-1') , (1-palmEps,'r-finger-4-2')] ,
  'palm.03.L_tail' : 'r-finger-4-1' ,
  'finger_ring.01.L_tail' : 'r-finger-4-2' ,
  'finger_ring.02.L_tail' : 'r-finger-4-3' ,
  'finger_ring.03.L_tail' : [(2,'r-finger-4-3') , (-1,'r-finger-4-2')] ,
  'palm.02.L_head' : [(palmEps,'r-finger-3-1') , (1-palmEps,'r-finger-3-2')] ,
  'palm.02.L_tail' : 'r-finger-3-1' ,
  'finger_middle.01.L_tail' : 'r-finger-3-2' ,
  'finger_middle.02.L_tail' : 'r-finger-3-3' ,
  'finger_middle.03.L_tail' : [(2,'r-finger-3-3') , (-1,'r-finger-3-2')] ,
  'palm.01.L_head' : [(palmEps,'r-finger-2-1') , (1-palmEps,'r-finger-2-2')] ,
  'palm.01.L_tail' : 'r-finger-2-1' ,
  'finger_index.01.L_tail' : 'r-finger-2-2' ,
  'finger_index.02.L_tail' : 'r-finger-2-3' ,
  'finger_index.03.L_tail' : [(2,'r-finger-2-3') , (-1,'r-finger-2-2')] ,
  'thumb.01.L_head' : 'r-finger-1-1' ,
  'thumb.01.L_tail' : 'r-finger-1-2' ,
  'thumb.02.L_tail' : 'r-finger-1-3' ,
  'thumb.03.L_tail' : [(2,'r-finger-1-3') , (-1,'r-finger-1-2')] ,

  'DLT-shoulder.R_head' : 'l-clavicle' ,
  'DLT-shoulder.R_tail' : 'l-shoulder' ,
  'shoulder.R_head' : 'l-clavicle' ,
  'shoulder.R_tail' : 'l-shoulder' ,
  'DLT-upper_arm.R_head' : 'l-shoulder' ,
  'DLT-upper_arm.R_tail' : [(0.25,'l-elbow') , (0.75, 'l-shoulder')] ,
  'upper_arm.R_head' : 'l-shoulder' ,
  'upper_arm.R_tail' : 'l-elbow' ,
  'forearm.R_tail' : 'l-hand' ,
  'hand.R_tail' : [(0.7,'l-hand') , (0.3,'l-finger-3-1')]  ,
  'palm.04.R_head' : [(palmEps,'l-finger-5-1') , (1-palmEps,'l-finger-5-2')] ,
  'palm.04.R_tail' : 'l-finger-5-1' ,
  'finger_pinky.01.R_tail' :  'l-finger-5-2' ,
  'finger_pinky.02.R_tail' :  'l-finger-5-3' ,
  'finger_pinky.03.R_tail' : [(2,'l-finger-5-3') , (-1,'l-finger-5-2')] ,
  'palm.03.R_head' : [(palmEps,'l-finger-4-1') , (1-palmEps,'l-finger-4-2')] ,
  'palm.03.R_tail' :  'l-finger-4-1' ,
  'finger_ring.01.R_tail' :  'l-finger-4-2' ,
  'finger_ring.02.R_tail' :  'l-finger-4-3' ,
  'finger_ring.03.R_tail' : [(2,'l-finger-4-3') , (-1,'l-finger-4-2')] ,
  'palm.02.R_head' : [(palmEps,'l-finger-3-1') , (1-palmEps,'l-finger-3-2')] ,
  'palm.02.R_tail' :  'l-finger-3-1' ,
  'finger_middle.01.R_tail' :  'l-finger-3-2' ,
  'finger_middle.02.R_tail' :  'l-finger-3-3' ,
  'finger_middle.03.R_tail' : [(2,'l-finger-3-3') , (-1,'l-finger-3-2')] ,
  'palm.01.R_head' : [(palmEps,'l-finger-2-1') , (1-palmEps,'l-finger-2-2')] ,
  'palm.01.R_tail' :  'l-finger-2-1' ,
  'finger_index.01.R_tail' :  'l-finger-2-2' ,
  'finger_index.02.R_tail' :  'l-finger-2-3' ,
  'finger_index.03.R_tail' : [(2,'l-finger-2-3') , (-1,'l-finger-2-2')] ,
  'thumb.01.R_head' :  'l-finger-1-1' ,
  'thumb.01.R_tail' :  'l-finger-1-2' ,
  'thumb.02.R_tail' :  'l-finger-1-3' ,
  'thumb.03.R_tail' : [(2,'l-finger-1-3') , (-1,'l-finger-1-2')] ,
 
  'thigh.L_head' : 'r-upper-leg' ,
  'thigh.L_tail' : 'r-knee' ,
  'shin.L_tail' : 'r-ankle' ,
  'foot.L_tail' : 'r-toe-3-1' ,
  'toe.L_tail' : 'r-toe-3-3' ,
  'heel.L_head' : [(1.5, 'r-ankle') , (-0.5, 'r-toe-3-1')] ,
  'heel.L_tail' : [(2, 'r-ankle') , (-1, 'r-toe-3-1')] ,

  'thigh.R_head' : 'l-upper-leg' ,
  'thigh.R_tail' : 'l-knee' ,
  'shin.R_tail' : 'l-ankle' ,
  'foot.R_tail' : 'l-toe-3-1' ,
  'toe.R_tail' : 'l-toe-3-3' ,
  'heel.R_head' : [(1.5, 'l-ankle') , (-0.5, 'l-toe-3-1')] ,
  'heel.R_tail' : [(2, 'l-ankle') , (-1, 'l-toe-3-1')] ,
})


armature = [
	('root', 'None', 'root_head', 'root_tail', 0, 'root'), 
	('pelvis', 'root', 'pelvis_head', 'pelvis_tail', 0, ''), 
	('torso', 'pelvis', 'torso_head', 'torso_tail', 0, 'spine_pivot_flex'), 
	('spine.01', 'torso', 'spine.01_head', 'spine.01_tail', 0, ''), 
	('spine.02', 'spine.01', 'spine.01_tail', 'spine.02_tail', F_CON, ''), 
	('spine.03', 'spine.02', 'spine.02_tail', 'spine.03_tail', F_CON, ''), 
	('spine.04', 'spine.03', 'spine.03_tail', 'spine.04_tail', F_CON, ''), 
	('neck_base', 'spine.04', 'spine.04_tail', 'neck_base_tail', F_CON, ''), 
	('head', 'neck_base', 'neck_base_tail', 'head_tail', F_CON, 'neck_flex'), 
	('neck.01', 'head', 'neck.01_head', 'neck.01_tail', 0, ''), 
	('neck.02', 'neck.01', 'neck.01_tail', 'neck.02_tail', F_CON, ''), 
	('neck.03', 'neck.02', 'neck.02_tail', 'neck.03_tail', F_CON, ''), 
	('DLT-shoulder.L', 'neck_base', 'DLT-shoulder.L_head', 'DLT-shoulder.L_tail', 0, 'delta'), 
	('shoulder.L', 'DLT-shoulder.L', 'shoulder.L_head', 'shoulder.L_tail', 0, 'copy'), 
	('DLT-upper_arm.L', 'shoulder.L', 'DLT-upper_arm.L_head', 'DLT-upper_arm.L_tail', 0, 'delta'), 
	('upper_arm.L', 'DLT-upper_arm.L', 'upper_arm.L_head', 'upper_arm.L_tail', 0, 'arm_biped_generic'), 
	('forearm.L', 'upper_arm.L', 'upper_arm.L_tail', 'forearm.L_tail', F_CON, ''), 
	('hand.L', 'forearm.L', 'forearm.L_tail', 'hand.L_tail', F_CON, ''), 
	('palm.04.L', 'hand.L', 'palm.04.L_head', 'palm.04.L_tail', 0, ''), 
	('finger_pinky.01.L', 'palm.04.L', 'palm.04.L_tail', 'finger_pinky.01.L_tail', F_CON, 'finger_curl'), 
	('finger_pinky.02.L', 'finger_pinky.01.L', 'finger_pinky.01.L_tail', 'finger_pinky.02.L_tail', F_CON, ''), 
	('finger_pinky.03.L', 'finger_pinky.02.L', 'finger_pinky.02.L_tail', 'finger_pinky.03.L_tail', F_CON, ''), 
	('palm.03.L', 'hand.L', 'palm.03.L_head', 'palm.03.L_tail', 0, ''), 
	('finger_ring.01.L', 'palm.03.L', 'palm.03.L_tail', 'finger_ring.01.L_tail', F_CON, 'finger_curl'), 
	('finger_ring.02.L', 'finger_ring.01.L', 'finger_ring.01.L_tail', 'finger_ring.02.L_tail', F_CON, ''), 
	('finger_ring.03.L', 'finger_ring.02.L', 'finger_ring.02.L_tail', 'finger_ring.03.L_tail', F_CON, ''), 
	('palm.02.L', 'hand.L', 'palm.02.L_head', 'palm.02.L_tail', 0, ''), 
	('finger_middle.01.L', 'palm.02.L', 'palm.02.L_tail', 'finger_middle.01.L_tail', F_CON, 'finger_curl'), 
	('finger_middle.02.L', 'finger_middle.01.L', 'finger_middle.01.L_tail', 'finger_middle.02.L_tail', F_CON, ''), 
	('finger_middle.03.L', 'finger_middle.02.L', 'finger_middle.02.L_tail', 'finger_middle.03.L_tail', F_CON, ''), 
	('palm.01.L', 'hand.L', 'palm.01.L_head', 'palm.01.L_tail', 0, 'palm_curl'), 
	('finger_index.01.L', 'palm.01.L', 'palm.01.L_tail', 'finger_index.01.L_tail', F_CON, 'finger_curl'), 
	('finger_index.02.L', 'finger_index.01.L', 'finger_index.01.L_tail', 'finger_index.02.L_tail', F_CON, ''), 
	('finger_index.03.L', 'finger_index.02.L', 'finger_index.02.L_tail', 'finger_index.03.L_tail', F_CON, ''), 
	('thumb.01.L', 'hand.L', 'thumb.01.L_head', 'thumb.01.L_tail', 0, 'finger_curl'), 
	('thumb.02.L', 'thumb.01.L', 'thumb.01.L_tail', 'thumb.02.L_tail', F_CON, ''), 
	('thumb.03.L', 'thumb.02.L', 'thumb.02.L_tail', 'thumb.03.L_tail', F_CON, ''), 
	('DLT-shoulder.R', 'neck_base', 'DLT-shoulder.R_head', 'DLT-shoulder.R_tail', 0, 'delta'), 
	('shoulder.R', 'DLT-shoulder.R', 'shoulder.R_head', 'shoulder.R_tail', 0, 'copy'), 
	('DLT-upper_arm.R', 'shoulder.R', 'DLT-upper_arm.R_head', 'DLT-upper_arm.R_tail', 0, 'delta'), 
	('upper_arm.R', 'DLT-upper_arm.R', 'upper_arm.R_head', 'upper_arm.R_tail', 0, 'arm_biped_generic'), 
	('forearm.R', 'upper_arm.R', 'upper_arm.R_tail', 'forearm.R_tail', F_CON, ''), 
	('hand.R', 'forearm.R', 'forearm.R_tail', 'hand.R_tail', F_CON, ''), 
	('palm.04.R', 'hand.R', 'palm.04.R_head', 'palm.04.R_tail', 0, ''), 
	('finger_pinky.01.R', 'palm.04.R', 'palm.04.R_tail', 'finger_pinky.01.R_tail', F_CON, 'finger_curl'), 
	('finger_pinky.02.R', 'finger_pinky.01.R', 'finger_pinky.01.R_tail', 'finger_pinky.02.R_tail', F_CON, ''), 
	('finger_pinky.03.R', 'finger_pinky.02.R', 'finger_pinky.02.R_tail', 'finger_pinky.03.R_tail', F_CON, ''), 
	('palm.03.R', 'hand.R', 'palm.03.R_head', 'palm.03.R_tail', 0, ''), 
	('finger_ring.01.R', 'palm.03.R', 'palm.03.R_tail', 'finger_ring.01.R_tail', F_CON, 'finger_curl'), 
	('finger_ring.02.R', 'finger_ring.01.R', 'finger_ring.01.R_tail', 'finger_ring.02.R_tail', F_CON, ''), 
	('finger_ring.03.R', 'finger_ring.02.R', 'finger_ring.02.R_tail', 'finger_ring.03.R_tail', F_CON, ''), 
	('palm.02.R', 'hand.R', 'palm.02.R_head', 'palm.02.R_tail', 0, ''), 
	('finger_middle.01.R', 'palm.02.R', 'palm.02.R_tail', 'finger_middle.01.R_tail', F_CON, 'finger_curl'), 
	('finger_middle.02.R', 'finger_middle.01.R', 'finger_middle.01.R_tail', 'finger_middle.02.R_tail', F_CON, ''), 
	('finger_middle.03.R', 'finger_middle.02.R', 'finger_middle.02.R_tail', 'finger_middle.03.R_tail', F_CON, ''), 
	('thumb.01.R', 'hand.R', 'thumb.01.R_head', 'thumb.01.R_tail', 0, 'finger_curl'), 
	('thumb.02.R', 'thumb.01.R', 'thumb.01.R_tail', 'thumb.02.R_tail', F_CON, ''), 
	('thumb.03.R', 'thumb.02.R', 'thumb.02.R_tail', 'thumb.03.R_tail', F_CON, ''), 
	('palm.01.R', 'hand.R', 'palm.01.R_head', 'palm.01.R_tail', 0, 'palm_curl'), 
	('finger_index.01.R', 'palm.01.R', 'palm.01.R_tail', 'finger_index.01.R_tail', F_CON, 'finger_curl'), 
	('finger_index.02.R', 'finger_index.01.R', 'finger_index.01.R_tail', 'finger_index.02.R_tail', F_CON, ''), 
	('finger_index.03.R', 'finger_index.02.R', 'finger_index.02.R_tail', 'finger_index.03.R_tail', F_CON, ''), 
	('thigh.L', 'spine.01', 'thigh.L_head', 'thigh.L_tail', 0, 'leg_biped_generic'), 
	('shin.L', 'thigh.L', 'thigh.L_tail', 'shin.L_tail', F_CON, ''), 
	('foot.L', 'shin.L', 'shin.L_tail', 'foot.L_tail', F_CON, ''), 
	('toe.L', 'foot.L', 'foot.L_tail', 'toe.L_tail', F_CON, ''), 
	('heel.L', 'foot.L', 'heel.L_head', 'heel.L_tail', 0, ''), 
	('thigh.R', 'spine.01', 'thigh.R_head', 'thigh.R_tail', 0, 'leg_biped_generic'), 
	('shin.R', 'thigh.R', 'thigh.R_tail', 'shin.R_tail', F_CON, ''), 
	('foot.R', 'shin.R', 'shin.R_tail', 'foot.R_tail', F_CON, ''), 
	('toe.R', 'foot.R', 'foot.R_tail', 'toe.R_tail', F_CON, ''), 
	('heel.R', 'foot.R', 'heel.R_head', 'heel.R_tail', 0, ''), 
]

Bone = 0 
Obj = 1 
constraints = [
]

toeArmature = [
	("toe-1-1.L", "toe.L", "r-toe-1-1", "r-toe-1-2", 0),
	("toe-1-2.L", "toe-1-1.L", "r-toe-1-2", [(2,"r-toe-1-2") , (-1,"r-toe-1-1")], F_CON),

	("toe-2-1.L", "toe.L", "r-toe-2-1", "r-toe-2-2", 0),
	("toe-2-2.L", "toe-2-1.L", "r-toe-2-2", "r-toe-2-3", F_CON),
	("toe-2-3.L", "toe-2-2.L", "r-toe-2-3", [(2,"r-toe-2-3") , (-1,"r-toe-2-2")], F_CON),

	("toe-3-1.L", "toe.L", "r-toe-3-1", "r-toe-3-2", 0),
	("toe-3-2.L", "toe-3-1.L", "r-toe-3-2", "r-toe-3-3", F_CON),
	("toe-3-3.L", "toe-3-2.L", "r-toe-3-3", [(2,"r-toe-3-3") , (-1,"r-toe-3-2")], F_CON),

	("toe-4-1.L", "toe.L", "r-toe-4-1", "r-toe-4-2", 0),
	("toe-4-2.L", "toe-4-1.L", "r-toe-4-2", "r-toe-4-3", F_CON),
	("toe-4-3.L", "toe-4-2.L", "r-toe-4-3", [(2,"r-toe-4-3") , (-1,"r-toe-4-2")], F_CON),

	("toe-5-1.L", "toe.L", "r-toe-5-1", "r-toe-5-2", 0),
	("toe-5-2.L", "toe-5-1.L", "r-toe-5-2", "r-toe-5-3", F_CON),
	("toe-5-3.L", "toe-5-2.L", "r-toe-5-3", [(2,"r-toe-5-3") , (-1,"r-toe-5-2")], F_CON),

	("toe-1-1.R", "toe.R", "l-toe-1-1", "l-toe-1-2", 0),
	("toe-1-2.R", "toe-1-1.R", "l-toe-1-2", [(2,"l-toe-1-2") , (-1,"l-toe-1-1")], F_CON),

	("toe-2-1.R", "toe.R", "l-toe-2-1", "l-toe-2-2", 0),
	("toe-2-2.R", "toe-2-1.R", "l-toe-2-2", "l-toe-2-3", F_CON),
	("toe-2-3.R", "toe-2-2.R", "l-toe-2-3", [(2,"l-toe-2-3") , (-1,"l-toe-2-2")], F_CON),

	("toe-3-1.R", "toe.R", "l-toe-3-1", "l-toe-3-2", 0),
	("toe-3-2.R", "toe-3-1.R", "l-toe-3-2", "l-toe-3-3", F_CON),
	("toe-3-3.R", "toe-3-2.R", "l-toe-3-3", [(2,"l-toe-3-3") , (-1,"l-toe-3-2")], F_CON),

	("toe-4-1.R", "toe.R", "l-toe-4-1", "l-toe-4-2", 0),
	("toe-4-2.R", "toe-4-1.R", "l-toe-4-2", "l-toe-4-3", F_CON),
	("toe-4-3.R", "toe-4-2.R", "l-toe-4-3", [(2,"l-toe-4-3") , (-1,"l-toe-4-2")], F_CON),

	("toe-5-1.R", "toe.R", "l-toe-5-1", "l-toe-5-2", 0),
	("toe-5-2.R", "toe-5-1.R", "l-toe-5-2", "l-toe-5-3", F_CON),
	("toe-5-3.R", "toe-5-2.R", "l-toe-5-3", [(2,"l-toe-5-3") , (-1,"l-toe-5-2")], F_CON),
]

#
#	calcJointPos(obj, joint):
#

def calcJointPos(obj, joint):
	g = obj.getFaceGroup("joint-"+joint)
	verts = []
	for f in g.faces:
		for v in f.verts:
			verts.append(v.co)
	return centroid(verts)

#
#	setupLocations (obj):
#
def setupLocations (obj):
	global newLocs, oldLocs
	newLocs = {}
	oldLocs = {}
	for (key,j) in joints.items():
		if type(j) == str:
			loc = calcJointPos(obj, j)
			newLocs[key] = loc
			oldLocs[j] = loc
	for (key,j) in joints.items():
		if type(j) == list:
			newLocs[key] = jointAdd(j[0], j[1])

def jointAdd((f0,j0), (f1,j1)):
	global oldLocs
	loc0 = vmul(oldLocs[j0],f0)
	loc1 = vmul(oldLocs[j1],f1)
	return vadd(loc0, loc1)

#
#	writeBones(obj, fp)
#

def writeBones(obj, fp):
	global oldLocs, newLocs
	setupLocations(obj)
	fp.write("\narmature RigifyRig RigifyRig\n\trigify ;")
	for bone in armature:
		writeBone(bone, fp)
	'''
	for (bone, par, hjoint, tjoint, conn) in toeArmature:
		if type(hjoint) == str:
			loc = calcJointPos(obj, hjoint)
			oldLocs[hjoint] = loc
			newLocs[hjoint] = loc
	for bone in toeArmature:
		writeBone(bone, fp)
	'''
	fp.write("end armature\n")
	fp.write("pose RigifyRig\n")
	for bone in armature:
		writePoseBone(bone, fp)
	fp.write("end pose\n")

def getLoc(j):
	global newLocs
	if type(j) == str:
		return newLocs[j]
	elif type(j) == list:
		return jointAdd(j[0], j[1])

def writeBone((bone, par, hjoint, tjoint, flags, btype), fp):
	head = getLoc(hjoint)
	tail = getLoc(tjoint)
	fp.write("\n\
\tbone %s %s %d\n\
\t\thead %f %f %f ;\n\
\t\ttail %f %f %f ;\n\
\tend bone\n" % (bone, par, flags, head[0], head[1], head[2], tail[0], tail[1], tail[2]))

def writePoseBone((bone, par, hjoint, tjoint, flags, btype), fp):
	if btype != '':
		fp.write("\
\n\tposebone %s\n\
\t\ttype %s ;\n\
\tend posebone\n" % (bone, btype))


