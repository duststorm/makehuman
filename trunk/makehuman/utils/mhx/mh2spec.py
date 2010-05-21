#
#	Utility to extra rig bones and weights.
#
#	To use this file, move it to mh_plugins and modify mh2collada
#

import os
import rig_body_25, rig_arm_25, rig_finger_25, rig_leg_25, rig_toe_25, rig_face_25, rig_panel_25
import mhx_rig, mh2collada
from mhx_rig import *

'''
rigFiles = ['
#joints
joint-finger-1-1
joint-finger-1-2
 
# skeleton
1 0 # joint parentjoint
 
# weights
1 0 1.0 # vertex, joint, weight
'''
 

joints = rig_body_25.BodyJoints +\
	rig_arm_25.ArmJoints +\
	rig_finger_25.FingerJoints +\
	rig_leg_25.LegJoints +\
	rig_face_25.FaceJoints
	
headTails = rig_body_25.BodyHeadsTails +\
	rig_arm_25.ArmHeadsTails +\
	rig_finger_25.FingerHeadsTails +\
	rig_leg_25.LegHeadsTails +\
	rig_face_25.FaceHeadsTails
	
armature = rig_body_25.BodyArmature +\
	rig_arm_25.ArmArmature +\
	rig_finger_25.FingerArmature +\
	rig_leg_25.LegArmature +\
	rig_face_25.FaceArmature
	

	
#
#	writeSkeleton(fileName):
#

def writeSkeleton(fileName):
	fp = open(fileName, "w")
	(rig, usedJoint) = setupRig(headTails, armature)
	jointNum = writeJoints(fp, usedJoint, joints)
	boneNum = writeRig(fp, armature, rig, jointNum)

	weights = {}
	mh2collada.readSkinWeights(weights, "data/templates/vertexgroups-bones25.mhx")	
	fp.write("\n# weights\n")
	for (bone, bn) in boneNum.items():
		try:
			wts = weights[bone]
		except:
			wts = []
		for (vn,w) in wts:
			fp.write("  %s %s %s\n" % (vn, bn, w))
	fp.close()
	return

#
#	setupRig(headTails, armature):
#

def setupRig(headTails, armature):
	rig = {}
	usedJoint = {}
	for (bone, cond, roll, parent, flags, layers, bbone) in armature:
		par = mh2collada.boneOK(flags, bone, parent)
		if par:
			rig[bone] = [0.0, 0.0]
	for (bone, head, tail) in headTails:
		try:
			rigBone = rig[bone]
		except:
			rigBone = None
		if rigBone:
			rigBone[0] = head
			rigBone[1] = tail
			usedJoint[head] = True
			usedJoint[tail] = True
	return (rig, usedJoint)
	
#
#	writeJoints(fp, usedJoint, joints):
#

def writeJoints(fp, usedJoint, joints):
	jn = 0
	jointNum = {}
	fp.write("# locations\n")

	for (loc, typ, data) in joints:
		try:
			used = usedJoint[loc]
		except:
			used = True
		if used:
			print(loc, typ, data)
			jointNum[loc] = jn
			if typ == 'j' or typ == 'b':
				fp.write("  %s joint %s\n" % (loc, data))
			elif typ == 'v':
				fp.write("  %s vertex %s\n" % (loc, data))
			jn += 1
				
	for (loc, typ, data) in joints:
		try:
			used = usedJoint[loc]
		except:
			used = True
		if used:
			if typ == 'j' or typ == 'b' or typ == 'v':
				pass
			elif typ == 'o':
				(point, offs) = data
				fp.write("  %s offset %d %s %s %s\n" % (loc, jointNum[point], offs[0], offs[1], offs[2]))
			elif typ == 'l':
				((k1, x1), (k2, x2)) = data
				fp.write("  %s line %s %d %s %d \n" % (loc, k1, jointNum[x1], k2, jointNum[x2]))
			elif typ == 'p':
				(x, y, z) = data
				fp.write("  %s position %d %d %d \n" % (loc, jointNum[x], jointNum[y], jointNum[z]))
			else:
				raise NameError("Unknown joint type %s" % typ)
			jn += 1
			
	return jointNum			

#
#	writeRig(fp, armature, rig, jointNum):
#

def writeRig(fp, armature, rig, jointNum):
	bn = 0
	boneNum = {}
	fp.write("\n# bones\n")
	for (bone, cond, roll, parent, flags, layers, bbone) in armature:
		print(bone)
		try:
			rigBone = rig[bone]
		except:
			rigBone = None
		if rigBone:
			boneNum[bone] = bn
			head = rigBone[0]
			tail = rigBone[1]
			par = mh2collada.boneOK(flags, bone, parent)
			print("   ", head, tail, roll, par)
			fp.write("  %s %d %d %.4f" % (bone, jointNum[head], jointNum[tail], roll))
			if parent:
				fp.write(" %d" % boneNum[par])
			else:
				fp.write(" -")
			fp.write("\n")
			bn += 1
	return boneNum
	
	

			
		
		
		

			
		
		
		
	
	

