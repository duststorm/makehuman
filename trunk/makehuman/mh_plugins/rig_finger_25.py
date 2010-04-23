#
#	Face bone definitions
#

import mhx_rig
from mhx_rig import *

FingerJoints = [
	('r-finger-1-1',		'j', 'r-finger-1-1'),
	('r-finger-1-2',		'j', 'r-finger-1-2'),
	('r-finger-1-3',		'j', 'r-finger-1-3'),
	('r-finger-2-1',		'j', 'r-finger-2-1'),
	('r-finger-2-2',		'j', 'r-finger-2-2'),
	('r-finger-2-3',		'j', 'r-finger-2-3'),
	('r-finger-3-1',		'j', 'r-finger-3-1'),
	('r-finger-3-2',		'j', 'r-finger-3-2'),
	('r-finger-3-3',		'j', 'r-finger-3-3'),
	('r-finger-4-1',		'j', 'r-finger-4-1'),
	('r-finger-4-2',		'j', 'r-finger-4-2'),
	('r-finger-4-3',		'j', 'r-finger-4-3'),
	('r-finger-5-1',		'j', 'r-finger-5-1'),
	('r-finger-5-2',		'j', 'r-finger-5-2'),
	('r-finger-5-3',		'j', 'r-finger-5-3'),

	('l-finger-1-1',		'j', 'l-finger-1-1'),
	('l-finger-1-2',		'j', 'l-finger-1-2'),
	('l-finger-1-3',		'j', 'l-finger-1-3'),
	('l-finger-2-1',		'j', 'l-finger-2-1'),
	('l-finger-2-2',		'j', 'l-finger-2-2'),
	('l-finger-2-3',		'j', 'l-finger-2-3'),
	('l-finger-3-1',		'j', 'l-finger-3-1'),
	('l-finger-3-2',		'j', 'l-finger-3-2'),
	('l-finger-3-3',		'j', 'l-finger-3-3'),
	('l-finger-4-1',		'j', 'l-finger-4-1'),
	('l-finger-4-2',		'j', 'l-finger-4-2'),
	('l-finger-4-3',		'j', 'l-finger-4-3'),
	('l-finger-5-1',		'j', 'l-finger-5-1'),
	('l-finger-5-2',		'j', 'l-finger-5-2'),
	('l-finger-5-3',		'j', 'l-finger-5-3'),

	('l-finger-1-end',		'l', ((2.0, 'l-finger-1-3'), (-1.0, 'l-finger-1-2'))),
	('l-finger-2-end',		'l', ((2.0, 'l-finger-2-3'), (-1.0, 'l-finger-2-2'))),
	('l-finger-3-end',		'l', ((2.0, 'l-finger-3-3'), (-1.0, 'l-finger-3-2'))),
	('l-finger-4-end',		'l', ((2.0, 'l-finger-4-3'), (-1.0, 'l-finger-4-2'))),
	('l-finger-5-end',		'l', ((2.0, 'l-finger-5-3'), (-1.0, 'l-finger-5-2'))),
	('r-finger-1-end',		'l', ((2.0, 'r-finger-1-3'), (-1.0, 'r-finger-1-2'))),
	('r-finger-2-end',		'l', ((2.0, 'r-finger-2-3'), (-1.0, 'r-finger-2-2'))),
	('r-finger-3-end',		'l', ((2.0, 'r-finger-3-3'), (-1.0, 'r-finger-3-2'))),
	('r-finger-4-end',		'l', ((2.0, 'r-finger-4-3'), (-1.0, 'r-finger-4-2'))),
	('r-finger-5-end',		'l', ((2.0, 'r-finger-5-3'), (-1.0, 'r-finger-5-2'))),

	('Fingers_R_head',		'o', ('l-finger-3-1', [0.0, 1.0, 0.0])),
	('Fingers_R_tail',		'o', ('l-finger-3-end', [0.0, 1.0, 0.0])),
	('Fingers_L_head',		'o', ('r-finger-3-1', [0.0, 1.0, 0.0])),
	('Fingers_L_tail',		'o', ('r-finger-3-end', [0.0, 1.0, 0.0])),
]

FingerHeadsTails = [
	('Finger-1-1_L',		'r-finger-1-1', 'r-finger-1-2'),
	('Finger-1-2_L',		'r-finger-1-2', 'r-finger-1-3'),
	('Finger-1-3_L',		'r-finger-1-3', 'r-finger-1-end'),
	('Finger-2-1_L',		'r-finger-2-1', 'r-finger-2-2'),
	('Finger-2-2_L',		'r-finger-2-2', 'r-finger-2-3'),
	('Finger-2-3_L',		'r-finger-2-3', 'r-finger-2-end'),
	('Finger-3-1_L',		'r-finger-3-1', 'r-finger-3-2'),
	('Finger-3-2_L',		'r-finger-3-2', 'r-finger-3-3'),
	('Finger-3-3_L',		'r-finger-3-3', 'r-finger-3-end'),
	('Finger-4-1_L',		'r-finger-4-1', 'r-finger-4-2'),
	('Finger-4-2_L',		'r-finger-4-2', 'r-finger-4-3'),
	('Finger-4-3_L',		'r-finger-4-3', 'r-finger-4-end'),
	('Finger-5-1_L',		'r-finger-5-1', 'r-finger-5-2'),
	('Finger-5-2_L',		'r-finger-5-2', 'r-finger-5-3'),
	('Finger-5-3_L',		'r-finger-5-3', 'r-finger-5-end'),

	('Finger-1-1_R',		'l-finger-1-1', 'l-finger-1-2'),
	('Finger-1-2_R',		'l-finger-1-2', 'l-finger-1-3'),
	('Finger-1-3_R',		'l-finger-1-3', 'l-finger-1-end'),
	('Finger-2-1_R',		'l-finger-2-1', 'l-finger-2-2'),
	('Finger-2-2_R',		'l-finger-2-2', 'l-finger-2-3'),
	('Finger-2-3_R',		'l-finger-2-3', 'l-finger-2-end'),
	('Finger-3-1_R',		'l-finger-3-1', 'l-finger-3-2'),
	('Finger-3-2_R',		'l-finger-3-2', 'l-finger-3-3'),
	('Finger-3-3_R',		'l-finger-3-3', 'l-finger-3-end'),
	('Finger-4-1_R',		'l-finger-4-1', 'l-finger-4-2'),
	('Finger-4-2_R',		'l-finger-4-2', 'l-finger-4-3'),
	('Finger-4-3_R',		'l-finger-4-3', 'l-finger-4-end'),
	('Finger-5-1_R',		'l-finger-5-1', 'l-finger-5-2'),
	('Finger-5-2_R',		'l-finger-5-2', 'l-finger-5-3'),
	('Finger-5-3_R',		'l-finger-5-3', 'l-finger-5-end'),

	('Fingers_L',			'Fingers_L_head', 'Fingers_L_tail'),
	('Fingers_R',			'Fingers_R_head', 'Fingers_R_tail'),

	('Finger-1_R',			'l-finger-1-1', 'l-finger-1-end'),
	('Finger-2_R',			'l-finger-2-1', 'l-finger-2-end'),
	('Finger-3_R',			'l-finger-3-1', 'l-finger-3-end'),
	('Finger-4_R',			'l-finger-4-1', 'l-finger-4-end'),
	('Finger-5_R',			'l-finger-5-1', 'l-finger-5-end'),

	('Finger-1_L',			'r-finger-1-1', 'r-finger-1-end'),
	('Finger-2_L',			'r-finger-2-1', 'r-finger-2-end'),
	('Finger-3_L',			'r-finger-3-1', 'r-finger-3-end'),
	('Finger-4_L',			'r-finger-4-1', 'r-finger-4-end'),
	('Finger-5_L',			'r-finger-5-1', 'r-finger-5-end'),

	('Finger-1-IK_R',		'l-finger-1-end', 'l-finger-1-3'),
	('Finger-2-IK_R',		'l-finger-2-end', 'l-finger-2-3'),
	('Finger-3-IK_R',		'l-finger-3-end', 'l-finger-3-3'),
	('Finger-4-IK_R',		'l-finger-4-end', 'l-finger-4-3'),
	('Finger-5-IK_R',		'l-finger-5-end', 'l-finger-5-3'),

	('Finger-1-IK_L',		'r-finger-1-end', 'r-finger-1-3'),
	('Finger-2-IK_L',		'r-finger-2-end', 'r-finger-2-3'),
	('Finger-3-IK_L',		'r-finger-3-end', 'r-finger-3-3'),
	('Finger-4-IK_L',		'r-finger-4-end', 'r-finger-4-3'),
	('Finger-5-IK_L',		'r-finger-5-end', 'r-finger-5-3'),
]

FingerArmature = [
	# Deform
	('Finger-1-1_L', 'True',	0.0, 'Hand_L', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-1-2_L', 'True',	0.0, 'Finger-1-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-3_L', 'True',	0.0, 'Finger-1-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-1_L', 'True',	0.0, 'Hand_L', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-2-2_L', 'True',	0.0, 'Finger-2-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-3_L', 'True',	0.0, 'Finger-2-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-1_L', 'True',	0.0, 'Hand_L', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-3-2_L', 'True',	0.0, 'Finger-3-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-3_L', 'True',	0.0, 'Finger-3-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-1_L', 'True',	0.0, 'Hand_L', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-4-2_L', 'True',	0.0, 'Finger-4-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-3_L', 'True',	0.0, 'Finger-4-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-1_L', 'True',	0.0, 'Hand_L', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-5-2_L', 'True',	0.0, 'Finger-5-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-3_L', 'True',	0.0, 'Finger-5-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),

	('Finger-1-1_R', 'True',	0.0, 'Hand_R', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-1-2_R', 'True',	0.0, 'Finger-1-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-3_R', 'True',	0.0, 'Finger-1-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-1_R', 'True',	0.0, 'Hand_R', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-2-2_R', 'True',	0.0, 'Finger-2-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-3_R', 'True',	0.0, 'Finger-2-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-1_R', 'True',	0.0, 'Hand_R', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-3-2_R', 'True',	0.0, 'Finger-3-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-3_R', 'True',	0.0, 'Finger-3-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-1_R', 'True',	0.0, 'Hand_R', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-4-2_R', 'True',	0.0, 'Finger-4-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-3_R', 'True',	0.0, 'Finger-4-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-1_R', 'True',	0.0, 'Hand_R', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-5-2_R', 'True',	0.0, 'Finger-5-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-3_R', 'True',	0.0, 'Finger-5-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),

	#
	#('Fingers_L', 'rigArm&T_FingerIK',	0.0, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	#('Fingers_R', 'rigArm&T_FingerIK',	0.0, 'Hand_R', 0, L_HANDIK, (1,1,1) ),

	# Finger controls
	('Finger-1_L', 'rigArm&T_FingerIK',	0.0, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-2_L', 'rigArm&T_FingerIK',	0.0, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-3_L', 'rigArm&T_FingerIK',	0.0, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-4_L', 'rigArm&T_FingerIK',	0.0, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-5_L', 'rigArm&T_FingerIK',	0.0, 'Hand_L', 0, L_HANDIK, (1,1,1) ),

	('Finger-1_R', 'rigArm&T_FingerIK',	0.0, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-2_R', 'rigArm&T_FingerIK',	0.0, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-3_R', 'rigArm&T_FingerIK',	0.0, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-4_R', 'rigArm&T_FingerIK',	0.0, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-5_R', 'rigArm&T_FingerIK',	0.0, 'Hand_R', 0, L_HANDIK, (1,1,1) ),

	# IK targets
	('Finger-1-IK_L', 'rigArm&T_FingerIK',	0.0, 'Finger-1_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-2-IK_L', 'rigArm&T_FingerIK',	0.0, 'Finger-2_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-3-IK_L', 'rigArm&T_FingerIK',	0.0, 'Finger-3_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-4-IK_L', 'rigArm&T_FingerIK',	0.0, 'Finger-4_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-5-IK_L', 'rigArm&T_FingerIK',	0.0, 'Finger-5_L', F_CON, L_HELP, (1,1,1) ),

	('Finger-1-IK_R', 'rigArm&T_FingerIK',	0.0, 'Finger-1_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-2-IK_R', 'rigArm&T_FingerIK',	0.0, 'Finger-2_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-3-IK_R', 'rigArm&T_FingerIK',	0.0, 'Finger-3_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-4-IK_R', 'rigArm&T_FingerIK',	0.0, 'Finger-4_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-5-IK_R', 'rigArm&T_FingerIK',	0.0, 'Finger-5_R', F_CON, L_HELP, (1,1,1) ),
]

def FingerWritePoses(fp):
	global boneGroups
	boneGroups = {}

	customShape = 'MHCircle05'
	customShape = None
	# Deform with finger IK

	addPoseBone(fp, 'True', 'Finger-1-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, [])
	addPoseBone(fp, 'True', 'Finger-1-2_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, [])
	addPoseBone(fp, 'True', 'Finger-1-3_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-1-IK_L', 3, None, (True, False), 'fFingerIK'])])

	addPoseBone(fp, 'True', 'Finger-1-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, [])
	addPoseBone(fp, 'True', 'Finger-1-2_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, [])
	addPoseBone(fp, 'True', 'Finger-1-3_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-1-IK_R', 3,  None, (True, False), 'fFingerIK'])])

	addPoseBone(fp, 'True', 'Finger-2-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-2-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-2-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-2-IK_L', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-2-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-2-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-2-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-2-IK_R', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-3-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-3-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-3-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-3-IK_L', 3,  None, (True, False), 'fFingerIK']),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-3-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-3-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-3-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-3-IK_R', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-4-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-4-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-4-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-4-IK_L', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-4-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-4-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-4-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-4-IK_R', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-5-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-5-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-5-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-5-IK_L', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-5-1_R', customShape, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-5-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-5-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-5-IK_R', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.57,0, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	# Finger IK
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-1_L', None, None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-1_R', None, None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-2_L', None, None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-2_R', None, None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-3_L', None, None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-3_R', None, None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-4_L', None, None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-4_R', None, None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-5_L', None, None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-5_R', None, None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

	# Ik targets
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-1-IK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-1-IK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-2-IK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-2-IK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-3-IK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-3-IK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-4-IK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-4-IK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-5-IK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-5-IK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	
	return 

#
#	actionFingerCurl
#	FingerWriteActions(fp):
#

actionFingerCurl = [
	("Finger-2-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-2-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-2-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-3-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-3-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-3-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-4-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-4-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-4-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-5-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-5-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-5-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
]
def FingerWriteActions(fp):
	writeAction(fp, 'rigArm&T_FingerCurl', "goboFingerCurl", actionFingerCurl, True, False)

#
#	FingerProcess
#	(bone, axis, angle)
#

FingerProcess = [
	("Finger-1-1_L", "Z", -0.3),
	("Finger-1-2_L", "Z", -0.3),
	("Finger-1-3_L", "Z", -0.3),
	("Finger-2-1_L", "Z", -0.3),
	("Finger-2-2_L", "Z", -0.3),
	("Finger-2-3_L", "Z", -0.3),
	("Finger-3-1_L", "Z", -0.3),
	("Finger-3-2_L", "Z", -0.3),
	("Finger-3-3_L", "Z", -0.3),
	("Finger-4-1_L", "Z", -0.3),
	("Finger-4-2_L", "Z", -0.3),
	("Finger-4-3_L", "Z", -0.3),
	("Finger-5-1_L", "Z", -0.3),
	("Finger-5-2_L", "Z", -0.3),
	("Finger-5-3_L", "Z", -0.3),

	("Finger-1-1_R", "Z", 0.3),
	("Finger-1-2_R", "Z", 0.3),
	("Finger-1-3_R", "Z", 0.3),
	("Finger-2-1_R", "Z", 0.3),
	("Finger-2-2_R", "Z", 0.3),
	("Finger-2-3_R", "Z", 0.3),
	("Finger-3-1_R", "Z", 0.3),
	("Finger-3-2_R", "Z", 0.3),
	("Finger-3-3_R", "Z", 0.3),
	("Finger-4-1_R", "Z", 0.3),
	("Finger-4-2_R", "Z", 0.3),
	("Finger-4-3_R", "Z", 0.3),
	("Finger-5-1_R", "Z", 0.3),
	("Finger-5-2_R", "Z", 0.3),
	("Finger-5-3_R", "Z", 0.3),
]

FingerParents = [
	("Finger-1-IK_L", "Finger-1-3_L"),
	("Finger-2-IK_L", "Finger-2-3_L"),
	("Finger-3-IK_L", "Finger-3-3_L"),
	("Finger-4-IK_L", "Finger-4-3_L"),
	("Finger-5-IK_L", "Finger-5-3_L"),

	("Finger-1-IK_R", "Finger-1-3_R"),
	("Finger-2-IK_R", "Finger-2-3_R"),
	("Finger-3-IK_R", "Finger-3-3_R"),
	("Finger-4-IK_R", "Finger-4-3_R"),
	("Finger-5-IK_R", "Finger-5-3_R"),
]


