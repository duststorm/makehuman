#
#	Arm bone definitions
#

import mhx_rig
from mhx_rig import *

ArmJoints = [
	('r-clavicle',			'j', 'r-clavicle'),
	('r-shoulder',			'j', 'r-shoulder'),
	('ShoulderIK_L_tail',		'l', ((2,'r-shoulder'), (-1,'r-clavicle'))),
	('r-elbow',			'j', 'r-elbow'),
	('r-hand',			'j', 'r-hand'),
	('hand_L_tail',			'j', 'r-finger-3-1'),
	('r-loarm-vec',			'l', ((1, 'r-hand'), (-1, 'r-elbow'))),
	('armRoot_L_head',		'l', ((1,'r-shoulder'), (-1,'Root_offs'))),
	('wristCtrl_L_tail',		'l', ((1, 'r-hand'), (1, 'r-loarm-vec'))),

	('l-clavicle',			'j', 'l-clavicle'),
	('l-shoulder',			'j', 'l-shoulder'),
	('ShoulderIK_R_tail',		'l', ((2,'l-shoulder'), (-1,'l-clavicle'))),
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

]

ArmHeadsTails = [
	# Root
	('Clavicle_L',			'r-clavicle', 'r-shoulder'),
	('ArmRoot_L',			'armRoot_L_head', 'r-shoulder'),
	('Clavicle_R',			'l-clavicle', 'l-shoulder'),
	('ArmRoot_R',			'armRoot_R_head', 'l-shoulder'),
	('ShoulderIK_L',		'r-shoulder', 'ShoulderIK_L_tail'),
	('ShoulderIK_R',		'l-shoulder', 'ShoulderIK_R_tail'),

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
	('ElbowHandle_L',		'r-elbow', 'elbowPT_L_head'),
	('ElbowPT_L',			'elbowPT_L_head', 'elbowPT_L_tail'),

	('UpArmIK_R',			'l-shoulder', 'l-elbow'),
	('LoArmIK_R',			'l-elbow', 'l-hand'),
	('HandIK_R',			'l-hand', 'hand_R_tail'),
	('WristCtrl_R',			'l-hand', 'wristCtrl_R_tail'),
	('ElbowHandle_R',		'l-elbow', 'elbowPT_R_head'),
	('ElbowPT_R',			'elbowPT_R_head', 'elbowPT_R_tail'),

]

#upArmRoll = 1.69297
#loArmRoll = deg90
#handRoll = 1.22173


upArmRoll = 0.0
loArmRoll = 0.0
handRoll = 0.0

ArmArmature = [
	# Root
	('Clavicle_L', True,		0.0, 'Spine1', F_DEF+F_WIR, L_DEF, (1,1,1) ),
	('ArmRoot_L', True,		0.0, 'Clavicle_L', 0, L_HELP, (1,1,1) ),
	('ShoulderIK_L', True,		0.0, 'Spine1', F_WIR, L_ARMFK+L_ARMIK, (1,1,1) ),
	
	('Clavicle_R', True,		0.0, 'Spine1', F_DEF+F_WIR, L_DEF, (1,1,1) ),
	('ArmRoot_R', True,		0.0, 'Clavicle_R', 0, L_HELP, (1,1,1) ),
	('ShoulderIK_R', True,		0.0, 'Spine1', F_WIR, L_ARMFK+L_ARMIK, (1,1,1) ),

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
	('ElbowHandle_L', True,		0.0, 'LoArmIK_L', F_RES, L_ARMIK, (1,1,1)),
	('ElbowPT_L', True,		loArmRoll, 'ArmRoot_L', F_WIR,  L_ARMIK, (1,1,1)),

	('UpArmIK_R', True,		-upArmRoll, 'ArmRoot_R', F_CON, L_HLPIK, (1,1,1) ),
	('LoArmIK_R', True,		-loArmRoll, 'UpArmIK_R', F_CON, L_HLPIK, (1,1,1) ),
	('WristCtrl_R', True,		-loArmRoll, 'Root', F_WIR, L_ARMIK, (1,1,1)),
	('HandIK_R', True,		-handRoll, 'LoArmIK_R', F_WIR, L_ARMIK, (1,1,1)),
	('ElbowHandle_R', True,		0.0, 'LoArmIK_R', F_RES, L_ARMIK, (1,1,1)),
	('ElbowPT_R', True,		-loArmRoll, 'ArmRoot_R', F_WIR, L_ARMIK, (1,1,1)),

]

limClavicle_L = (-deg45,deg45, 0,0, -deg20,deg20)
limClavicle_R = (-deg45,deg45, 0,0, -deg20,deg20)

limUpArm_L = (-deg90,deg90, -deg45,deg45, -deg90,deg45)
limUpArm_R = (-deg90,deg90, -deg45,deg45, -deg45,deg90)

limLoArm_L = (0,0, -deg90,deg90, -deg90,deg10)
limLoArm_R = (0,0, -deg90,deg90, -deg10,deg90)

limHand_L = (-deg90,70*deg1, 0,0, -deg20,deg20)
limHand_R = (-deg90,70*deg1, 0,0, -deg20,deg20)


def ArmWritePoses(fp):
	global boneGroups
	boneGroups = {}

	# Root 
	
	addPoseBone(fp, True, 'ArmRoot_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, True, 'ArmRoot_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'ShoulderIK_L', 'MHCube01', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['LimitDist', 'Spine1'])])

	addPoseBone(fp, 'True', 'ShoulderIK_R', 'MHCube01', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['LimitDist', 'Spine1'])])

	# Deform

	addPoseBone(fp, True, 'Clavicle_L', 'GoboShldr_L', 'grabable', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'ShoulderIK_L', 1, None, (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limClavicle_L, (True, True, True)])])

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

	addPoseBone(fp, True, 'LoArmTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Hand_L', 1, None, (True, False), 1.0])])
		#[('CopyRot', 0, ['UnTwist', 'LoArm_L', True, (1,1,1), (0,0,0), False])])



	addPoseBone(fp, True, 'Clavicle_R', 'GoboShldr_R', 'grabable', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'ShoulderIK_R', 1, None, (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limClavicle_R, (True, True, True)])])

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

	addPoseBone(fp, True, 'LoArmTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Hand_R', 1, None, (True, False), 1.0])])
		#[('CopyRot', 0, ['UnTwist', 'LoArm_R', True, (1,1,1), (0,0,0), False])])


	# FK

	addPoseBone(fp, True, 'UpArmFK_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpArm_L, (True, True, True)])])

	addPoseBone(fp, True, 'LoArmFK_L', 'MHCircle025', None, (0,0,0), (1,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limLoArm_L, (True, True, True)])])

	addPoseBone(fp, True, 'HandFK_L', 'MHHand', None, (0,0,0), (0,1,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limHand_L, (True, True, True)])])
		

	addPoseBone(fp, True, 'UpArmFK_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpArm_R, (True, True, True)])])

	addPoseBone(fp, True, 'LoArmFK_R', 'MHCircle025', None, (0,0,0), (1,0,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limLoArm_R, (True, True, True)])])

	addPoseBone(fp, True, 'HandFK_R', 'MHHand', None, (0,0,0), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limHand_R, (True, True, True)])])


	# IK

	addPoseBone(fp, True, 'UpArmIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpArm_L, (True, True, True)])])

	addPoseBone(fp, True, 'LoArmIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,0,1), 0,
		[('IK', 0, ['IK', 'WristCtrl_L', 2, (deg180, 'ElbowPT_L'), (True, False), 1.0]),
		#('CopyRot', 0, ['CopyRotY', 'WristCtrl_L', 1.0, (0,1,0), (0,0,0), False]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limLoArm_L, (True, True, True)])])

	addPoseBone(fp, True, 'WristCtrl_L', 'MHCube025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['World', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Local', 'ArmRoot_L', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'Clavicle_L'])])

	addPoseBone(fp, True, 'HandIK_L', 'MHHand', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limHand_L, (True, True, True)])])

	addPoseBone(fp, True, 'ElbowPT_L', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Arm', 'ArmRoot_L', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Wrist', 'WristCtrl_L', 0.0, (1,1,1), (1,1,1), (1,1,1)])])

	addPoseBone(fp, True, 'ElbowHandle_L', None, 'ik', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['StretchTo', 'ElbowPT_L', 'PLANE_X'])])


	addPoseBone(fp, True, 'UpArmIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpArm_R, (True, True, True)])])

	addPoseBone(fp, True, 'LoArmIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,0,1), 0,
		[('IK', 0, ['IK', 'WristCtrl_R', 2, (0, 'ElbowPT_R'), (True, False), 1.0]),
		#('CopyRot', 0, ['CopyRotY', 'WristCtrl_R', 1.0, (0,1,0), (0,0,0), False]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limLoArm_R, (True, True, True)])])

	addPoseBone(fp, True, 'WristCtrl_R', 'MHCube025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['World', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Local', 'ArmRoot_R', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'Clavicle_R'])])

	addPoseBone(fp, True, 'HandIK_R', 'MHHand', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limHand_R, (True, True, True)])])

	addPoseBone(fp, True, 'ElbowPT_R', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Arm', 'ArmRoot_R', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Wrist', 'WristCtrl_R', 0.0, (1,1,1), (1,1,1), (1,1,1)])])

	addPoseBone(fp, True, 'ElbowHandle_R', None, 'ik', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['StretchTo', 'ElbowPT_R', 'PLANE_X'])])


	# Finger curl
	'''
	addPoseBone(fp, 'rigArm&T_FingerCurl', 'FingerCurl_L', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'rigArm&T_FingerCurl', 'FingerCurl_R', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])
	'''

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

]
'''
	("WristCtrl_L", True, "World", "Local", "PHandLocal_L", "LOC_X"),
	("WristCtrl_R", True, "World", "Local", "PHandLocal_R", "LOC_X"),
'''
#
#	ArmProcess
#	(bone, axis, angle)
#

ArmProcess = [
	("LoArm_L", "Z", -deg20),
	("LoArm_R", "Z", deg20),
]	

ArmSnaps = [
	("LoArmTwist_L", "LoArm_L", 0),
	("LoArmFK_L", "LoArm_L", 0),
	("LoArmIK_L", "LoArm_L", 0),
	("HandIK_L", "Hand_L", 0),

	("LoArmTwist_R", "LoArm_R", 0),
	("LoArmFK_R", "LoArm_R", 0),
	("LoArmIK_R", "LoArm_R", 0),
	("HandIK_R", "Hand_R", 0),
]

ArmParents = [
	("WristCtrl_L", "LoArmIK_L"),
	("WristCtrl_R", "LoArmIK_R"),
]
