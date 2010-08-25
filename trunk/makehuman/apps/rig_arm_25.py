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
	('wristCtrl_L_tail',		'l', ((1, 'r-hand'), (1, 'r-loarm-vec'))),

	('r-clavicle-back',		'v', 2583),
	('r-scapula-root',		'l', ((0.2, 'r-clavicle'), (0.8, 'r-clavicle-back'))),
	('r-scapula-top',		'v', 3048),
	('r-scapula-bot',		'v', 3600),

	('l-clavicle',			'j', 'l-clavicle'),
	('l-shoulder',			'j', 'l-shoulder'),
	('l-elbow',			'j', 'l-elbow'),
	('l-hand',			'j', 'l-hand'),
	('hand_R_tail',			'j', 'l-finger-3-1'),

	('l-loarm-vec',			'l', ((1, 'l-hand'), (-1, 'l-elbow'))),
	('wristCtrl_R_tail',		'l', ((1, 'l-hand'), (1, 'l-loarm-vec'))),

	('l-clavicle-back',		'v', 11025),
	('l-scapula-root',		'l', ((0.2, 'l-clavicle'), (0.8, 'l-clavicle-back'))),
	('l-scapula-top',		'v', 10683),
	('l-scapula-bot',		'v', 10192),


	# elbow pole target
	('r-loarm-vec',			'l', ((0.25, 'r-hand'), (-0.25, 'r-elbow'))),
	('l-loarm-vec',			'l', ((0.25, 'l-hand'), (-0.25, 'l-elbow'))),
	('elbowPT_L_head',		'o', ('r-elbow', [0,0,-3])),
	('elbowPT_R_head',		'o', ('l-elbow', [0,0,-3])),
	('elbowPT_L_tail',		'o', ('elbowPT_L_head', 'r-loarm-vec')),
	('elbowPT_R_tail',		'o', ('elbowPT_R_head', 'l-loarm-vec')),

]

ArmHeadsTails = [
	# Shoulder
	('Clavicle_L',			'r-clavicle', 'r-shoulder'),
	('ShoulderIK_L',		'r-shoulder', ('r-shoulder', yunit)),
	('ScapulaTop_L',		'r-clavicle', 'r-scapula-top'),
	('ScapulaTopIK_L',		'r-scapula-top', ('r-scapula-top', yunit)),
	('Scapula_L',			'r-scapula-top', 'r-scapula-bot'),
	('ScapulaIK_L',		'r-scapula-bot', ('r-scapula-bot', yunit)),

	('Clavicle_R',			'l-clavicle', 'l-shoulder'),
	('ShoulderIK_R',		'l-shoulder', ('l-shoulder', yunit)),
	('ScapulaTop_R',		'l-clavicle', 'l-scapula-top'),
	('ScapulaTopIK_R',		'l-scapula-top', ('l-scapula-top', yunit)),
	('Scapula_R',			'l-scapula-top', 'l-scapula-bot'),
	('ScapulaIK_R',			'l-scapula-bot', ('l-scapula-bot', yunit)),

	# Root
	('ArmRoot_L',			('r-shoulder', yunit), 'r-shoulder'),
	('ArmRoot_R',			('l-shoulder', yunit), 'l-shoulder'),

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

spineTop = 'Spine3'
L_SHOULDER = L_ARMFK+L_ARMIK+L_SPINE

ArmArmature = [
	# Shoulder
	('Clavicle_L', True,		0.0, spineTop, F_DEF, L_DEF, (1,1,1) ),
	('ShoulderIK_L', True,		0.0, spineTop, F_WIR, L_SHOULDER, (1,1,1) ),
	('Scapula_L', True,		0.0, spineTop, F_WIR+F_DEF, L_SHOULDER+L_DEF, (1,1,1) ),
	('ScapulaIK_L', True,		0.0, spineTop, F_WIR,L_SHOULDER, (1,1,1) ),

	('Clavicle_R', True,		0.0, spineTop, F_DEF, L_DEF, (1,1,1) ),
	('ShoulderIK_R', True,		0.0, spineTop, F_WIR, L_SHOULDER, (1,1,1) ),
	('Scapula_R', True,		0.0, spineTop, F_WIR+F_DEF, L_SHOULDER+L_DEF, (1,1,1) ),
	('ScapulaIK_R', True,		0.0, spineTop, F_WIR, L_SHOULDER, (1,1,1) ),

	# Root
	('ArmRoot_L', True,		0.0, 'Clavicle_L', 0, L_HELP, (1,1,1) ),
	('ArmRoot_R', True,		0.0, 'Clavicle_R', 0, L_HELP, (1,1,1) ),

	# Deform
	('UpArm_L', True,		upArmRoll, 'ArmRoot_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpArmTwist_L', True,		upArmRoll, 'ArmRoot_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArm_L', True,		loArmRoll, 'UpArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArmTwist_L', True,		loArmRoll, 'UpArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Hand_L', True,		handRoll, 'LoArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),

	('UpArm_R', True,		upArmRoll, 'ArmRoot_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpArmTwist_R', True,		upArmRoll, 'ArmRoot_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArm_R', True,		loArmRoll, 'UpArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArmTwist_R', True,		loArmRoll, 'UpArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Hand_R', True,		handRoll, 'LoArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),


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
	('WristCtrl_L', True,		loArmRoll, None, F_WIR, L_ARMIK, (1,1,1)),
	('HandIK_L', True,		handRoll, 'LoArmIK_L', F_WIR, L_ARMIK, (1,1,1)),
	('ElbowHandle_L', True,		0.0, 'LoArmIK_L', F_RES, L_ARMIK, (1,1,1)),
	('ElbowPT_L', True,		loArmRoll, None, F_WIR,  L_ARMIK, (1,1,1)),

	('UpArmIK_R', True,		-upArmRoll, 'ArmRoot_R', F_CON, L_HLPIK, (1,1,1) ),
	('LoArmIK_R', True,		-loArmRoll, 'UpArmIK_R', F_CON, L_HLPIK, (1,1,1) ),
	('WristCtrl_R', True,		-loArmRoll, None, F_WIR, L_ARMIK, (1,1,1)),
	('HandIK_R', True,		-handRoll, 'LoArmIK_R', F_WIR, L_ARMIK, (1,1,1)),
	('ElbowHandle_R', True,		0.0, 'LoArmIK_R', F_RES, L_ARMIK, (1,1,1)),
	('ElbowPT_R', True,		-loArmRoll, None, F_WIR, L_ARMIK, (1,1,1)),

]

limClavicle_L = (-deg45,deg45, 0,0, -deg20,deg20)
limClavicle_R = (-deg45,deg45, 0,0, -deg20,deg20)

limUpArm_L = (-deg90,deg90, -deg45,deg45, -deg90,deg45)
limUpArm_R = (-deg90,deg90, -deg45,deg45, -deg45,deg90)

limLoArm_L = (0,0, -deg90,deg90, -deg90,deg10)
limLoArm_R = (0,0, -deg90,deg90, -deg10,deg90)

limHand_L = (-deg90,70*deg1, 0,0, -deg20,deg20)
limHand_R = (-deg90,70*deg1, 0,0, -deg20,deg20)


ArmPoses = [
	# Shoulder 
	
	('singleIK', 'Clavicle_L', (0,1,0), 'ShoulderIK_L', limClavicle_L),
	('ikHandle', 'ShoulderIK_L', 'MHCube025', spineTop),
	('poseBone', True, 'Scapula_L', 'MHCube01', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'ScapulaIK_L', 1, None, (True, False,False), 1.0])]),
	('ikHandle', 'ScapulaIK_L', 'MHCube01', None),

	('singleIK', 'Clavicle_R', (0,1,0), 'ShoulderIK_R', limClavicle_R),
	('ikHandle', 'ShoulderIK_R', 'MHCube025', spineTop),
	('poseBone', True, 'Scapula_R', 'MHCube01', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'ScapulaIK_R', 1, None, (True, False,False), 1.0])]),
	('ikHandle', 'ScapulaIK_R', 'MHCube01', None),

	# Root

	('poseBone', True, 'ArmRoot_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, []),
	('poseBone', True, 'ArmRoot_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, []),

	# Deform

	('deformLimb', 'UpArm_L', 'UpArmIK_L', (1,1,1), 'UpArmFK_L', (1,1,1), 0, P_STRETCH),
	('poseBone', True, 'UpArmTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('CopyRot', C_OW_LOCAL+C_TG_LOCAL, ['CopyRotY', 'UpArm_L', 1.0, (1,1,1), (0,0,0), False])]),
	#	[('IK', 0, ['IK', 'LoArm_L', 1, None, (True, False,False), 1.0])]),
	('deformLimb', 'LoArm_L', 'LoArmIK_L', (1,1,1), 'LoArmFK_L', (1,1,1), 0, P_STRETCH),
	('poseBone', True, 'LoArmTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'Hand_L', 1, None, (True, False,True), 1.0])]),
	('deformLimb', 'Hand_L', 'HandIK_L', (1,1,1), 'HandFK_L', (1,1,1), 0, 0),

	('deformLimb', 'UpArm_R', 'UpArmIK_R', (1,1,1), 'UpArmFK_R', (1,1,1), 0, P_STRETCH),
	('poseBone', True, 'UpArmTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('CopyRot', C_OW_LOCAL+C_TG_LOCAL, ['CopyRotY', 'UpArm_R', 1.0, (1,1,1), (0,0,0), False])]),
	#	[('IK', 0, ['IK', 'LoArm_R', 1, None, (True, False,False), 1.0])]),
	('deformLimb', 'LoArm_R', 'LoArmIK_R', (1,1,1), 'LoArmFK_R', (1,1,1), 0, P_STRETCH),
	('poseBone', True, 'LoArmTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'Hand_R', 1, None, (True, False,True), 1.0])]),
	('deformLimb', 'Hand_R', 'HandIK_R', (1,1,1), 'HandFK_R', (1,1,1), 0, 0),

	# FK

	('poseBone', True, 'UpArmFK_L', 'MHCircle025', None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpArm_L, (True, True, True)])]),

	('poseBone', True, 'LoArmFK_L', 'MHCircle025', None, (0,0,0), (1,0,0), (0,0,0), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limLoArm_L, (True, True, True)])]),

	('poseBone', True, 'HandFK_L', 'MHHand', None, (0,0,0), (0,1,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limHand_L, (True, True, True)])]),
		

	('poseBone', True, 'UpArmFK_R', 'MHCircle025', None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpArm_R, (True, True, True)])]),

	('poseBone', True, 'LoArmFK_R', 'MHCircle025', None, (0,0,0), (1,0,0), (0,0,0), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limLoArm_R, (True, True, True)])]),

	('poseBone', True, 'HandFK_R', 'MHHand', None, (0,0,0), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limHand_R, (True, True, True)])]),


	# IK

	('poseBone', True, 'UpArmIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpArm_L, (True, True, True)])]),

	('poseBone', True, 'LoArmIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'WristCtrl_L', 2, (deg180, 'ElbowPT_L'), (True, False,True), 1.0]),
		('CopyRot', C_OW_LOCAL+C_TG_LOCAL, ['CopyRotY', 'WristCtrl_L', 1.0, (0,1,0), (0,0,0), False]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limLoArm_L, (True, True, True)])]),

	('poseBone', True, 'WristCtrl_L', 'MHCube025', None, (0,0,0), (1,0,1), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['World', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Shoulder', 'ArmRoot_L', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Clavicle_L', 'fNoStretch', 'Clavicle_L'])]),

	('poseBone', True, 'HandIK_L', 'MHHand', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limHand_L, (True, True, True)])]),

	('poseBone', True, 'ElbowPT_L', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Shoulder', 'ArmRoot_L', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Wrist', 'WristCtrl_L', 0.0, (1,1,1), (1,1,1), (1,1,1)])]),

	('poseBone', True, 'ElbowHandle_L', None, 'ik', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['StretchTo', 'ElbowPT_L', 'PLANE_X'])]),


	('poseBone', True, 'UpArmIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpArm_R, (True, True, True)])]),

	('poseBone', True, 'LoArmIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'WristCtrl_R', 2, (0, 'ElbowPT_R'), (True, False,True), 1.0]),
		('CopyRot', C_OW_LOCAL+C_TG_LOCAL, ['CopyRotY', 'WristCtrl_R', 1.0, (0,1,0), (0,0,0), False]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limLoArm_R, (True, True, True)])]),

	('poseBone', True, 'WristCtrl_R', 'MHCube025', None, (0,0,0), (1,0,1), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['World', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Shoulder', 'ArmRoot_R', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Clavicle_R', 'fNoStretch', 'Clavicle_R'])]),

	('poseBone', True, 'HandIK_R', 'MHHand', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limHand_R, (True, True, True)])]),

	('poseBone', True, 'ElbowPT_R', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Shoulder', 'ArmRoot_R', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Wrist', 'WristCtrl_R', 0.0, (1,1,1), (1,1,1), (1,1,1)])]),

	('poseBone', True, 'ElbowHandle_R', None, 'ik', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['StretchTo', 'ElbowPT_R', 'PLANE_X'])]),
]

'''
	# Finger curl
	('poseBone', 'rigArm&T_FingerCurl', 'FingerCurl_L', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])]),

	('poseBone', 'rigArm&T_FingerCurl', 'FingerCurl_R', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])]),
'''

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
	("UpArm_L", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PArmIK_L", "LOC_X"),
	("LoArm_L", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PArmIK_L", "LOC_X"),
	("Hand_L", True, ["RotFK"], ["RotIK"], "PArmIK_L", "LOC_X"),

	("UpArm_R", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PArmIK_R", "LOC_X"),
	("LoArm_R", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PArmIK_R", "LOC_X"),
	("Hand_R", True, ["RotFK"], ["RotIK"], "PArmIK_R", "LOC_X"),

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
	("LoArmTwist_L", "Z", -deg20),
	("LoArmTwist_R", "Z", deg20),
]	

ArmSnaps = [
	("LoArmFK_L", "LoArm_L", 'Both'),
	("LoArmIK_L", "LoArm_L", 'Both'),
	("HandFK_L", "Hand_L", 'Both'),
	("HandIK_L", "Hand_L", 'Both'),

	("LoArmFK_R", "LoArm_R", 'Both'),
	("LoArmIK_R", "LoArm_R", 'Both'),
	("HandFK_R", "Hand_R", 'Both'),
	("HandIK_R", "Hand_R", 'Both'),
]

ArmParents = [
	("WristCtrl_L", "LoArm_L"),
	("WristCtrl_R", "LoArm_R"),
]

ArmSelects = []

ArmRolls = []


