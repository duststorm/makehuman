#
#	Arm bone definitions
#

import mhx_rig
from mhx_rig import *

ArmJoints = [
	('r-clavicle',			'j', 'r-clavicle'),
	('r-shoulder',			'j', 'r-shoulder'),
	('armRoot_L_head',		'o', ('r-shoulder', [0,0.5,0])),
	('r-elbow',			'j', 'r-elbow'),
	('r-hand',			'j', 'r-hand'),
	('hand_L_tail',			'j', 'r-finger-3-1'),

	('l-clavicle',			'j', 'l-clavicle'),
	('l-shoulder',			'j', 'l-shoulder'),
	('armRoot_R_head',		'o', ('l-shoulder', [0,0.5,0])),
	('l-elbow',			'j', 'l-elbow'),
	('l-hand',			'j', 'l-hand'),
	('hand_R_tail',			'j', 'l-finger-3-1'),

	# elbow uparm ik
	('r-elbow-target',		'l', ((1.2, 'r-elbow'), (-0.2, 'r-shoulder'))),
	('l-elbow-target',		'l', ((1.2, 'l-elbow'), (-0.2, 'l-shoulder'))),
	('ElbowIK_L_tail',		'o', ('r-elbow-target', [0.0, 0.0, -0.5])),
	('ElbowIK_R_tail',		'o', ('l-elbow-target', [0.0, 0.0, -0.5])),

	# elbow pole target
	('elbowPT_L_head',		'o', ('r-shoulder', [0,0,-3])),
	('elbowPT_L_tail',		'o', ('elbowPT_L_head', [0,0.5,0])),
	('elbowPT_R_head',		'o', ('l-shoulder', [0,0,-3])),
	('elbowPT_R_tail',		'o', ('elbowPT_R_head', [0,0.5,0])),

	# finger curl
	('finger_curl_L_head',		'o', ('r-hand', [0, 1.0, 0])),
	('finger_curl_L_tail',		'o', ('finger_curl_L_head', [0, 1.0, 0])),
	('finger_curl_R_head',		'o', ('l-hand', [0, 1.0, 0])),
	('finger_curl_R_tail',		'o', ('finger_curl_R_head', [0, 1.0, 0])),

]

ArmHeadsTails = [
	# Deform
	('Clavicle_L',			'r-clavicle', 'r-shoulder'),
	('ArmRoot_L',			'armRoot_L_head', 'r-shoulder'),
	('UpArm_L',			'r-shoulder', 'r-elbow'),
	('UpArmTwist_L',		'r-shoulder', 'r-elbow'),
	('LoArm_L',			'r-elbow', 'r-hand'),
	('LoArmTwist_L',		'r-elbow', 'r-hand'),
	('Hand_L',			'r-hand', 'hand_L_tail'),

	('Clavicle_R',			'l-clavicle', 'l-shoulder'),
	('ArmRoot_R',			'armRoot_R_head', 'l-shoulder'),
	('UpArm_R',			'l-shoulder', 'l-elbow'),
	('UpArmTwist_R',		'l-shoulder', 'l-elbow'),
	('LoArm_R',			'l-elbow', 'l-hand'),
	('LoArmTwist_R',		'l-elbow', 'l-hand'),
	('Hand_R',			'l-hand', 'hand_R_tail'),

	# FK
	('UpArmFK_L',			'r-shoulder', 'r-elbow'),
	('LoArmFK_L',			'r-elbow', 'r-hand'),
	('HandFK_L',			'r-hand', 'hand_L_tail'),
	('UpArmFK_R',			'l-shoulder', 'l-elbow'),
	('LoArmFK_R',			'l-elbow', 'l-hand'),
	('HandFK_R',			'l-hand', 'hand_R_tail'),

	# IK
	('UpArmIK_L',			'r-shoulder', 'r-elbow'),
	('LoArmIK_L',			'r-elbow', 'r-hand'),
	('HandIK_L',			'r-hand', 'hand_L_tail'),
	('UpArmIK_R',			'l-shoulder', 'l-elbow'),
	('LoArmIK_R',			'l-elbow', 'l-hand'),
	('HandIK_R',			'l-hand', 'hand_R_tail'),

	# IK uparm ik
	('ElbowIK_L',			'r-elbow-target', 'ElbowIK_L_tail'),
	('ElbowIK_R',			'l-elbow-target', 'ElbowIK_R_tail'),

	# IK uparm pole target
	('ElbowPT_L',			'elbowPT_L_head', 'elbowPT_L_tail'),
	('ElbowPT_R',			'elbowPT_R_head', 'elbowPT_R_tail'),

	# finger curl
	('FingerCurl_L',		'finger_curl_L_head', 'finger_curl_L_tail'),
	('FingerCurl_R',		'finger_curl_R_head', 'finger_curl_R_tail'),

]

ArmArmature = [
	# Deform
	('Clavicle_L', 'True',		1.91986, 'Spine1', F_DEF+F_WIR, L_ARMFK+L_ARMIK+L_DEF, (1,1,1) ),
	('ArmRoot_L', 'True',		1.69297, 'Clavicle_L', 0, L_HELP, (1,1,1) ),
	('UpArm_L', 'True',		1.69297, 'ArmRoot_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpArmTwist_L', 'True',	1.69297, 'ArmRoot_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArm_L', 'True',		1.58825, 'UpArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArmTwist_L', 'True',	1.58825, 'UpArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Hand_L', 'True',		1.22173, 'LoArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),

	('Clavicle_R', 'True',		-1.91986, 'Spine1', F_DEF+F_WIR, L_ARMFK+L_ARMIK+L_DEF, (1,1,1) ),
	('ArmRoot_R', 'True',		-1.69297, 'Clavicle_R', 0, L_HELP, (1,1,1) ),
	('UpArm_R', 'True',		-1.69297, 'ArmRoot_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpArmTwist_R', 'True',	-1.69297, 'ArmRoot_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArm_R', 'True',		-1.58825, 'UpArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArmTwist_R', 'True',	-1.58825, 'UpArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Hand_R', 'True',		-1.22173, 'LoArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),

	# FK
	('UpArmFK_L', 'True',		1.69297, 'ArmRoot_L', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('LoArmFK_L', 'True',		1.58825, 'UpArmFK_L', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('HandFK_L', 'True',		1.22173, 'LoArmFK_L', F_CON+F_WIR, L_ARMFK, (1,1,1) ),

	('UpArmFK_R', 'True',		-1.69297, 'ArmRoot_R', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('LoArmFK_R', 'True',		-1.58825, 'UpArmFK_R', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('HandFK_R', 'True',		-1.22173, 'LoArmFK_R', F_CON+F_WIR, L_ARMFK, (1,1,1) ),

	# IK common
	('UpArmIK_L', 'True',		1.69297, 'ArmRoot_L', F_CON, L_HELP, (1,1,1) ),
	('LoArmIK_L', 'True',		1.58825, 'UpArmIK_L', F_CON, L_HELP, (1,1,1) ),
	('HandIK_L', 'True',		1.5708, 'Root', F_WIR, L_ARMIK, (1,1,1)),

	('UpArmIK_R', 'True',		-1.69297, 'ArmRoot_R', F_CON, L_HELP, (1,1,1) ),
	('LoArmIK_R', 'True',		-1.58825, 'UpArmIK_R', F_CON, L_HELP, (1,1,1) ),
	('HandIK_R', 'True',		-1.5708, 'Root', F_WIR, L_ARMIK, (1,1,1)),

	# IK elbow uparm ik
	('ElbowIK_L', 'rigArm&T_ElbowIK',	-2.40855, 'ArmRoot_L', F_WIR, L_ARMIK, (1,1,1) ),
	('ElbowIK_R', 'rigArm&T_ElbowIK',	2.40855, 'ArmRoot_R', F_WIR, L_ARMIK, (1,1,1) ),

	# IK elbow pole target
	('ElbowPT_L', 'rigArm&T_ElbowPT',	0, 'ArmRoot_L', F_WIR,  L_ARMIK, (1,1,1)),
	('ElbowPT_R', 'rigArm&T_ElbowPT',	0, 'ArmRoot_R', F_WIR, L_ARMIK, (1,1,1)),

	# Finger curl
	('FingerCurl_L', 'rigArm&T_FingerCurl',	0, 'LoArm_L', F_WIR, L_ARMIK+L_ARMFK, (1,1,1)),
	('FingerCurl_R', 'rigArm&T_FingerCurl',	-3.14158, 'LoArm_R', F_WIR, L_ARMFK+L_ARMIK, (1,1,1)),


]

def ArmWritePoses(fp):
	global boneGroups
	boneGroups = {}

	# Deform

	#addPoseBone(fp, 'True', 'Clavicle_L', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Clavicle_L', 'GoboShldr_L', 'grabable', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OWNER, ['LimitRot', (-0.785398,0.349066, 0,0, -0.349066,0.785398), (True, True, True)])])

	addPoseBone(fp, 'True', 'UpArm_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'UpArmIK_L', 'fArmIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'UpArmFK_L', '1-fArmIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'True', 'LoArm_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'LoArmIK_L', 'fArmIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'LoArmFK_L', '1-fArmIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'True', 'Hand_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'HandIK_L', 'fArmIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'HandFK_L', '1-fArmIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'True', 'UpArmTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'LoArm_L', 1, None, (True, False), 1.0])])

	addPoseBone(fp, 'True', 'LoArmTwist_L', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Hand_L', 1, None, (True, False), 1.0])])


	#addPoseBone(fp, 'True', 'Clavicle_R', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Clavicle_R', 'GoboShldr_R', 'grabable', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OWNER, ['LimitRot', (-0.785398,0.349066, 0,0, -0.785398,0.349066), (True, True, True)])])

	addPoseBone(fp, 'True', 'UpArm_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'UpArmIK_R', 'fArmIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'UpArmFK_R', '1-fArmIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'True', 'LoArm_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'LoArmIK_R', 'fArmIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'LoArmFK_R', '1-fArmIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'True', 'Hand_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'HandIK_R', 'fArmIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'HandFK_R', '1-fArmIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'True', 'UpArmTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'LoArm_R', 1, None, (True, False), 1.0])])

	addPoseBone(fp, 'True', 'LoArmTwist_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Hand_R', 1, None, (True, False), 1.0])])


	# FK

	addPoseBone(fp, 'True', 'UpArmFK_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'LoArmFK_L', 'MHCircle025', None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'HandFK_L', 'MHHandCtrl_L', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'UpArmFK_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'LoArmFK_R', 'MHCircle025', None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'HandFK_R', 'MHHandCtrl_R', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])


	# IK Common

	addPoseBone(fp, 'True', 'HandIK_L', 'MHHandCtrl_L', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Clavicle_L'])])

	addPoseBone(fp, 'True', 'HandIK_R', 'MHHandCtrl_R', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Clavicle_R'])])

	addPoseBone(fp, 'True', 'UpArmIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'ElbowIK_L', 1, None, (True, False), 'fElbowIK'])])

	addPoseBone(fp, 'True', 'UpArmIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'ElbowIK_R', 1, None, (True, False), 'fElbowIK'])])


	# IK Elbow uparm ik

	addPoseBone(fp, 'rigArm&T_ElbowIK', 'ElbowIK_L', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Clavicle_L'])])

	addPoseBone(fp, 'rigArm&T_ElbowIK', 'ElbowIK_R', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Clavicle_R'])])

	addPoseBone(fp, 'rigArm&T_ElbowPT==0', 'LoArmIK_L', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'HandIK_L', 2, None, (True, False), 1.0])])

	addPoseBone(fp, 'rigArm&T_ElbowPT==0', 'LoArmIK_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'HandIK_R', 2, None, (True, False), 1.0])])


	# IK Elbow pole target

	addPoseBone(fp, 'rigArm&T_ElbowPT', 'LoArmIK_L', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'HandIK_L', 2, (-1.5708, 'ElbowPT_L'), (True, False), 1.0])])

	addPoseBone(fp, 'rigArm&T_ElbowPT', 'LoArmIK_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'HandIK_R', 2, (-1.5708, 'ElbowPT_R'), (True, False), 1.0])])

	addPoseBone(fp, 'rigArm&T_ElbowPT', 'ElbowPT_L', 'GoboCircle', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigArm&T_ElbowPT', 'ElbowPT_R', 'GoboCircle', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])


	# Finger curl

	addPoseBone(fp, 'rigArm&T_FingerCurl', 'FingerCurl_L', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.2,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'rigArm&T_FingerCurl', 'FingerCurl_R', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.2,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])


	return

#
#	ArmWriteActions(fp)
#

def ArmWriteActions(fp):
	return

#
#	ArmDrivers
#	(Bone, FK constraint, IK constraint, driver)
#

ArmDrivers = [
	("UpArm_L", "ConstFK", "ConstIK", "PArmIK_L"),
	("LoArm_L", "ConstFK", "ConstIK", "PArmIK_L"),
	("Hand_L", "ConstFK", "ConstIK", "PArmIK_L"),
	("UpArm_R", "ConstFK", "ConstIK", "PArmIK_R"),
	("LoArm_R", "ConstFK", "ConstIK", "PArmIK_R"),
	("Hand_R", "ConstFK", "ConstIK", "PArmIK_R"),
]
	

