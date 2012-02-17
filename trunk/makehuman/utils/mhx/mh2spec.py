#
#	Utility to extra rig bones and weights.
#
#	To use this file, move it to mh_plugins and modify mh2collada
#

import os
import rig_body_25, rig_arm_25, rig_finger_25, rig_leg_25, rig_toe_25, rig_face_25, rig_panel_25
import mhx_rig, mh2collada
import mhx_globals as the

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
 
theJoints = rig_body_25.BodyJoints +\
	rig_arm_25.ArmJoints +\
	rig_finger_25.FingerJoints +\
	rig_leg_25.LegJoints +\
	rig_face_25.FaceJoints
	
theHeadTails = rig_body_25.BodyHeadsTails +\
	rig_arm_25.ArmHeadsTails +\
	rig_finger_25.FingerHeadsTails +\
	rig_leg_25.LegHeadsTails +\
	rig_face_25.FaceHeadsTails
	
theArmature = rig_body_25.BodyArmature +\
	rig_arm_25.ArmArmature +\
	rig_finger_25.FingerArmature +\
	rig_leg_25.LegArmature +\
	rig_face_25.FaceArmature
	
thePoses = rig_body_25.BodyPoses +\
	rig_arm_25.ArmPoses +\
	rig_finger_25.FingerPoses +\
	rig_leg_25.LegPoses +\
	rig_face_25.FacePoses

#
#
#

def includeBone(cond, flags, bone, parent): 		
		if 1:
			return mh2collada.boneOK(flags, bone, parent)
		elif bone == 'Root':
			return 'None'
		elif cond == 'rigLeg&T_GoboFoot' or cond == 'rigArm&T_FingerPanel':
			return None
		else:
			return parent
	
#
#	writeSkeleton(fileName):
#

def writeSkeleton(fileName):
	fp = open(fileName, "w")
	(rig, usedJoint) = setupRig(theHeadTails, theArmature)
	jointNum = writeJoints(fp, usedJoint, theJoints)
	boneNum = writeRig(fp, theArmature, rig, jointNum)
	
	# writePoses(fp, thePoses, boneNum)

	weights = {}
	mh2collada.readSkinWeights(weights, "data/templates/vertexgroups-minimal.mhx")	

	bones = []
	for (bone, bn) in boneNum.items():
		bones.append((bn,bone))
	bones.sort()
	
	for (bn, bone) in bones:
		try:
			wts = weights[bone]
		except:
			wts = []
		if wts:
			fp.write("\n# weights %s\n" % bone)
			for (vn,w) in wts:
				fp.write("  %s %s\n" % (vn, w))
	fp.close()
	return

#
#	setupRig(headTails, armature):
#

def setupRig(headTails, armature):
	rig = {}
	usedJoint = {}
	for (bone, cond, roll, parent, flags, layers, bbone) in armature:
		par = includeBone(cond, flags, bone, parent)
		if par:
			rig[bone] = [0.0, 0.0]
	for (bone, head, tail) in headTails:
		print(bone, head, tail)
		try:
			rigBone = rig[bone]
		except:
			rigBone = None
		if rigBone:			
			rigBone[0] = head
			rigBone[1] = tail
			if type(head) == str:
				usedJoint[head] = True
			if type(tail) == str:
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
				fp.write("  %s offset %s %s %s %s\n" % (loc, point, offs[0], offs[1], offs[2]))
			elif typ == 'l':
				((k1, x1), (k2, x2)) = data
				fp.write("  %s line %s %s %s %s \n" % (loc, k1, x1, k2, x2))
			elif typ == 'p':
				(x, y, z) = data
				fp.write("  %s position %s %s %s \n" % (loc, x, y, z))
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
			par = includeBone(cond, flags, bone, parent)
			print("   ", head, tail, roll, par)
			fp.write("  %s %s %s %.4f" % (bone, head, tail, roll))
			if parent:
				fp.write(" %s" % par)
			else:
				fp.write(" -")
			fp.write("\n")
			bn += 1
	return boneNum
	
#
#	writePoses(fp, poses, boneNum)
#

def writePoses(fp, poses, boneNum):
	for pose in poses:
		print(pose)
		try:
			(typ, cond, bone, customShape, boneGroup, lockLoc, lockRot, lockScale, ik_dof, flags, constraints) = pose
		except:
			typ = None
		if not typ:
			try:
				(typ, bone, mx) = pose
			except:
				typ = None
		if not typ:
			try:
				(typ, bone, mn, mx) = pose
			except:
				typ = None
		if not typ:
			try:
				(typ, bone, lockRot, target, limit) = pose
			except:
				typ = None
		if not typ:
			try:
				(typ, bone, ikBone, ikRot, fkBone, fkRot, cflags, pflags) = pose
			except:
				typ = None
				
		if typ == 'poseBone':
			pass			
		elif typ == 'cSlider':
			(lockLoc, lockRot, lockScale, ik_dof, flags) = ((0,1,0), (1,1,1), (1,1,1), (1,1,1), 0)
			constraints = [('LimitLoc', C_OW_LOCAL+C_LTRA, ['Const', (-mx,mx, 0,0, -mx,mx), (1,1,1,1,1,1)])]

		elif typ == 'xSlider':
			(lockLoc, lockRot, lockScale, ik_dof, flags) = ((0,1,1), (1,1,1), (1,1,1), (1,1,1), 0)
			constraints = [('LimitLoc', C_OW_LOCAL+C_LTRA, ['Const', (mn,mx, 0,0, 0,0), (1,1,1,1,1,1)])]

		elif typ == 'ikHandle':
			if limit:
				constraints = [('LimitDist', 0, ['LimitDist', 1.0, limit])]
			else:
				constraints = []
			(cond, lockLoc, lockRot, lockScale, ik_dof, flags) = (True, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0)

		elif typ == 'singleIK':
			constraints = [('IK', 0, ['IK', target, 1, None, (True, False, True), 1.0])]
			if limit:
				constraints.append( ('LimitRot', C_OW_LOCAL, ['LimitRot', limit, (True, True, True)]) )
			(cond, lockLoc, lockScale, ik_dof, flags) = (True, (1,1,1), (1,1,1), (1,1,1), 0)

		elif typ == 'deformLimb':
			space = cflags & (C_OW_MASK + C_TG_MASK)
			constraints = [
				('CopyRot', space, ['RotIK', ikBone, 0.0, ikRot, (0,0,0), False]),
				('CopyRot', space, ['RotFK', fkBone, 1.0, fkRot, (0,0,0), False])
				]
			if pflags & P_STRETCH:
				constraints += [
				('CopyScale', 0, ['StretchIK', ikBone, 0.0, (0,1,0), False]),
				('CopyScale', 0, ['StretchFK', fkBone, 1.0, (0,1,0), False]),
				]		
			(cond, lockLoc, lockRot, lockScale, ik_dof, flags) = (True, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0)

		else:
			raise NameError("Unknown pose type %s" % typ)


		if includeBone(cond, flags, bone, True):
			fp.write("\nposebone %s %s %s %s %s\n" % (bone, lockLoc, lockRot, lockScale, ik_dof) )
			for (ctyp, cflags, cdata) in constraints:
				fp.write("  constraint %s %x %s\n" % (ctyp, cflags, cdata))
	return

			
		
		
		

			
		
		
		
	
	

