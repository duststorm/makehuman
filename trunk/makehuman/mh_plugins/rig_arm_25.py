#
#	Arm bone definitions
#

import mhx_rig
from mhx_rig import *

ArmJoints = [
	('r-clavicle',			'j', 'r-clavicle'),
	('r-shoulder',			'j', 'r-shoulder'),
	('r-elbow',			'j', 'r-elbow'),
	('r-hand',			'j', 'r-hand'),
	('hand_L_tail',			'j', 'r-finger-3-1'),
	('r-loarm-vec',			'l', ((1, 'r-hand'), (-1, 'r-elbow'))),
	('armRoot_L_head',		'l', ((1,'r-shoulder'), (-1,'Root_offs'))),
	('wristCtrl_L_tail',		'l', ((1, 'r-hand'), (1, 'r-loarm-vec'))),

	('l-clavicle',			'j', 'l-clavicle'),
	('l-shoulder',			'j', 'l-shoulder'),
	('l-elbow',			'j', 'l-elbow'),
	('l-hand',			'j', 'l-hand'),
	('hand_R_tail',			'j', 'l-finger-3-1'),
	('l-loarm-vec',			'l', ((1, 'l-hand'), (-1, 'l-elbow'))),
	('armRoot_R_head',		'l', ((1,'l-shoulder'), (-1,'Root_offs'))),
	('wristCtrl_R_tail',		'l', ((1, 'l-hand'), (1, 'l-loarm-vec'))),

	# elbow pole target
	('r-loarm-vec',			'l', ((0.25, 'r-hand'), (-0.25, 'r-elbow'))),
	('l-loarm-vec',			'l', ((0.25, 'l-hand'), (-0.25, 'l-elbow'))),
	('elbowPT_L_head',		'o', ('r-elbow', [0,0,-3])),
	('elbowPT_R_head',		'o', ('l-elbow', [0,0,-3])),
	('elbowPT_L_tail',		'o', ('elbowPT_L_head', 'r-loarm-vec')),
	('elbowPT_R_tail',		'o', ('elbowPT_R_head', 'l-loarm-vec')),

	# finger curl
	('finger_curl_L_head',		'o', ('r-hand', [0, 1.0, 0])),
	('finger_curl_L_tail',		'o', ('finger_curl_L_head', [0, 1.0, 0])),
	('finger_curl_R_head',		'o', ('l-hand', [0, 1.0, 0])),
	('finger_curl_R_tail',		'o', ('finger_curl_R_head', [0, 1.0, 0])),

]

ArmHeadsTails = [
	# Root
	('Clavicle_L',			'r-clavicle', 'r-shoulder'),
	('ArmRootShadow_L',		'armRoot_L_head', 'r-shoulder'),
	('ArmRoot_L',			'armRoot_L_head', 'r-shoulder'),

	('Clavicle_R',			'l-clavicle', 'l-shoulder'),
	('ArmRootShadow_R',		'armRoot_R_head', 'l-shoulder'),
	('ArmRoot_R',			'armRoot_R_head', 'l-shoulder'),

	# Deform
	('UpArm_L',			'r-shoulder', 'r-elbow'),
	('UpArmTwist_L',		'r-shoulder', 'r-elbow'),
	('LoArm_L',			'r-elbow', 'r-hand'),
	('LoArmTwist_L',		'r-elbow', 'r-hand'),
	('Hand_L',			'r-hand', 'hand_L_tail'),

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
	('WristCtrl_L',			'r-hand', 'wristCtrl_L_tail'),
	('ElbowPT_L',			'elbowPT_L_head', 'elbowPT_L_tail'),

	('UpArmIK_R',			'l-shoulder', 'l-elbow'),
	('LoArmIK_R',			'l-elbow', 'l-hand'),
	('HandIK_R',			'l-hand', 'hand_R_tail'),
	('WristCtrl_R',			'l-hand', 'wristCtrl_R_tail'),
	('ElbowPT_R',			'elbowPT_R_head', 'elbowPT_R_tail'),

	# finger curl
	('FingerCurl_L',		'finger_curl_L_head', 'finger_curl_L_tail'),
	('FingerCurl_R',		'finger_curl_R_head', 'finger_curl_R_tail'),

]

upArmRoll = 1.69297
loArmRoll = pihalf
handRoll = 1.22173

ArmArmature = [
	# Root
	('Clavicle_L', True,		0.0, 'Spine1', F_DEF+F_WIR, L_ARMFK+L_ARMIK+L_DEF, (1,1,1) ),
	('ArmRootShadow_L', True,	0.0, 'Clavicle_L', 0, L_HELP, (1,1,1) ),
	('ArmRoot_L', True,		0.0, 'Root', 0, L_HELP, (1,1,1) ),
	
	('Clavicle_R', True,		0.0, 'Spine1', F_DEF+F_WIR, L_ARMFK+L_ARMIK+L_DEF, (1,1,1) ),
	('ArmRootShadow_R', True,	0.0, 'Clavicle_R', 0, L_HELP, (1,1,1) ),
	('ArmRoot_R', True,		0.0, 'Root', 0, L_HELP, (1,1,1) ),

	# Deform
	('UpArm_L', True,		upArmRoll, 'ArmRoot_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpArmTwist_L', True,		upArmRoll, 'ArmRoot_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArm_L', True,		loArmRoll, 'UpArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArmTwist_L', True,		loArmRoll, 'UpArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Hand_L', True,		handRoll, 'LoArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),

	('UpArm_R', True,		-upArmRoll, 'ArmRoot_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpArmTwist_R', True,		-upArmRoll, 'ArmRoot_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArm_R', True,		-loArmRoll, 'UpArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArmTwist_R', True,		-loArmRoll, 'UpArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Hand_R', True,		-handRoll, 'LoArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),

	# FK
	('UpArmFK_L', True,		upArmRoll, 'ArmRoot_L', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('LoArmFK_L', True,		loArmRoll, 'UpArmFK_L', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('HandFK_L', True,		handRoll, 'LoArmFK_L', F_CON+F_WIR, L_ARMFK, (1,1,1) ),

	('UpArmFK_R', True,		-upArmRoll, 'ArmRoot_R', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('LoArmFK_R', True,		-loArmRoll, 'UpArmFK_R', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('HandFK_R', True,		-handRoll, 'LoArmFK_R', F_CON+F_WIR, L_ARMFK, (1,1,1) ),

	# IK common
	('UpArmIK_L', True,		upArmRoll, 'ArmRoot_L', F_CON, L_HLPIK, (1,1,1) ),
	('LoArmIK_L', True,		loArmRoll, 'UpArmIK_L', F_CON, L_HLPIK, (1,1,1) ),
	('WristCtrl_L', True,		loArmRoll, 'Root', F_WIR, L_ARMIK, (1,1,1)),
	('HandIK_L', True,		handRoll, 'LoArmIK_L', F_WIR, L_ARMIK, (1,1,1)),
	('ElbowPT_L', True,		loArmRoll, 'WristCtrl_L', F_WIR,  L_ARMIK, (1,1,1)),

	('UpArmIK_R', True,		-upArmRoll, 'ArmRoot_R', F_CON, L_HLPIK, (1,1,1) ),
	('LoArmIK_R', True,		-loArmRoll, 'UpArmIK_R', F_CON, L_HLPIK, (1,1,1) ),
	('WristCtrl_R', True,		-loArmRoll, 'Root', F_WIR, L_ARMIK, (1,1,1)),
	('HandIK_R', True,		-handRoll, 'LoArmIK_R', F_WIR, L_ARMIK, (1,1,1)),
	('ElbowPT_R', True,		-loArmRoll, 'WristCtrl_R', F_WIR, L_ARMIK, (1,1,1)),

	# Finger curl
	('FingerCurl_L', 'rigArm&T_FingerCurl',		0, 'LoArm_L', F_WIR, L_ARMIK+L_ARMFK, (1,1,1)),
	('FingerCurl_R', 'rigArm&T_FingerCurl',		-3.14158, 'LoArm_R', F_WIR, L_ARMFK+L_ARMIK, (1,1,1)),


]

def ArmWritePoses(fp):
	global boneGroups
	boneGroups = {}

	# Root 
	
	addPoseBone(fp, True, 'ArmRootShadow_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, True, 'ArmRootShadow_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, True, 'ArmRoot_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRot', 'ArmRootShadow_L', 1.0, (1,1,1), (0,0,0), False]),
		('CopyLoc', 0, ['CopyLoc', 'ArmRootShadow_L', 1.0, (1,1,1), (0,0,0), False])])

	addPoseBone(fp, True, 'ArmRoot_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRot', 'ArmRootShadow_R', 1.0, (1,1,1), (0,0,0), False]),
		('CopyLoc', 0, ['CopyLoc', 'ArmRootShadow_R', 1.0, (1,1,1), (0,0,0), False])])

	# Deform

	addPoseBone(fp, True, 'Clavicle_L', 'GoboShldr_L', 'grabable', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.785398,0.785398, 0,0, -0.349066,0.785398), (True, True, True)])])

	addPoseBone(fp, True, 'UpArm_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'UpArmIK_L', 'fArmIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'UpArmFK_L', '1-fArmIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, True, 'LoArm_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'LoArmIK_L', 'fArmIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'LoArmFK_L', '1-fArmIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, True, 'Hand_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'HandIK_L', 'fArmIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'HandFK_L', '1-fArmIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, True, 'UpArmTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		#[('IK', 0, ['IK', 'LoArm_L', 1, None, (True, False), 1.0])])
		[('CopyRot', 0, ['UnTwist', 'UpArm_L', True, (1,1,1), (0,0,0), False])])

	addPoseBone(fp, True, 'LoArmTwist_L', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Hand_L', 1, None, (True, False), 1.0])])
		#[('CopyRot', 0, ['UnTwist', 'LoArm_L', True, (1,1,1), (0,0,0), False])])


	addPoseBone(fp, True, 'Clavicle_R', 'GoboShldr_R', 'grabable', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.785398,0.785398, 0,0, -0.785398,0.349066), (True, True, True)])])

	addPoseBone(fp, True, 'UpArm_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'UpArmIK_R', 'fArmIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'UpArmFK_R', '1-fArmIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, True, 'LoArm_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'LoArmIK_R', 'fArmIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'LoArmFK_R', '1-fArmIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, True, 'Hand_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'HandIK_R', 'fArmIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'HandFK_R', '1-fArmIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, True, 'UpArmTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		#[('IK', 0, ['IK', 'LoArm_R', 1, None, (True, False), 1.0])])
		[('CopyRot', 0, ['UnTwist', 'UpArm_R', True, (1,1,1), (0,0,0), False])])

	addPoseBone(fp, True, 'LoArmTwist_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Hand_R', 1, None, (True, False), 1.0])])
		#[('CopyRot', 0, ['UnTwist', 'LoArm_R', True, (1,1,1), (0,0,0), False])])


	# FK

	addPoseBone(fp, True, 'UpArmFK_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.523,pihalf, -0.5,0.5, -1.7,0.78), (True, True, True)])])

	addPoseBone(fp, True, 'LoArmFK_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.2,1.8, -pihalf,pihalf, -0.1,0.1), (True, True, True)])])

	addPoseBone(fp, True, 'HandFK_L', 'MHHand', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.3,0.3, -0.1,0.1, -pihalf,pihalf), (True, True, True)])])
		

	addPoseBone(fp, True, 'UpArmFK_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.523,pihalf, -0.5,0.5, -0.78,1.7), (True, True, True)])])

	addPoseBone(fp, True, 'LoArmFK_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.2,1.8, -pihalf,pihalf, -0.1,0.1), (True, True, True)])])

	addPoseBone(fp, True, 'HandFK_R', 'MHHand', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.3,0.3, -0.1,0.1, -pihalf,pihalf), (True, True, True)])])


	# IK

	addPoseBone(fp, True, 'UpArmIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.523,pihalf, -0.5,0.5, -1.7,0.78), (True, True, True)])])

	addPoseBone(fp, True, 'LoArmIK_L', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'WristCtrl_L', 2, (-pihalf, 'ElbowPT_L'), (True, False), 1.0]),
		 ('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.2,1.8, -pihalf,pihalf, -0.1,0.1), (True, True, True)])])

	addPoseBone(fp, True, 'WristCtrl_L', 'MHWristCtrl_L', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['ChildOf', 'ArmRoot_L', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'Clavicle_L'])])

	addPoseBone(fp, True, 'HandIK_L', 'MHHand', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.3,0.3, -0.1,0.1, -pihalf,pihalf), (True, True, True)])])

	addPoseBone(fp, True, 'ElbowPT_L', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['ChildOf', 'WristCtrl_L', 0.0, (1,1,1), (1,1,1), (1,1,1)])])


	addPoseBone(fp, True, 'UpArmIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.523,pihalf, -0.5,0.5, -0.78,1.7), (True, True, True)])])

	addPoseBone(fp, True, 'LoArmIK_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'WristCtrl_R', 2, (-pihalf, 'ElbowPT_R'), (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.2,1.8, -pihalf,pihalf, -0.1,0.1), (True, True, True)])])

	addPoseBone(fp, True, 'WristCtrl_R', 'MHWristCtrl_R', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['ChildOf', 'ArmRoot_R', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'Clavicle_R'])])

	addPoseBone(fp, True, 'HandIK_R', 'MHHand', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-0.3,0.3, -0.1,0.1, -pihalf,pihalf), (True, True, True)])])

	addPoseBone(fp, True, 'ElbowPT_R', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['ChildOf', 'WristCtrl_R', 0.0, (1,1,1), (1,1,1), (1,1,1)])])


	# Finger curl

	addPoseBone(fp, 'rigArm&T_FingerCurl', 'FingerCurl_L', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'rigArm&T_FingerCurl', 'FingerCurl_R', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])


	return

#
#	ArmWriteActions(fp)
#

def ArmWriteActions(fp):
	return

#
#	ArmDrivers
#	(Bone, FK constraint, IK constraint, driver, channel)
#

ArmDrivers = [
	("UpArm_L", True, "ConstFK", "ConstIK", "PArmIK_L", "LOC_X"),
	("LoArm_L", True, "ConstFK", "ConstIK", "PArmIK_L", "LOC_X"),
	("Hand_L", True, "ConstFK", "ConstIK", "PArmIK_L", "LOC_X"),
	("UpArm_R", True, "ConstFK", "ConstIK", "PArmIK_R", "LOC_X"),
	("LoArm_R", True, "ConstFK", "ConstIK", "PArmIK_R", "LOC_X"),
	("Hand_R", True, "ConstFK", "ConstIK", "PArmIK_R", "LOC_X"),

	("WristCtrl_L", True, None, "ChildOf", "PHandLocal_L", "LOC_X"),
	("WristCtrl_R", True, None, "ChildOf", "PHandLocal_R", "LOC_X"),
]

#
#	ArmProcess
#	(bone, axis, angle)
#

ArmProcess = [
	("LoArm_L", "X", 0.3),
	("LoArmTwist_L", "X", 0.3),
	("LoArmFK_L", "X", 0.3),
	("LoArmIK_L", "X", 0.3),

	("LoArm_R", "X", 0.3),
	("LoArmTwist_R", "X", 0.3),
	("LoArmFK_R", "X", 0.3),
	("LoArmIK_R", "X", 0.3),
]	
ArmParents = [
	("HandIK_L", "LoArmIK_L"),
	("HandIK_R", "LoArmIK_R"),
]
