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
	('Finger-1-2_L', 'True',	1.5708, 'Finger-1-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-3_L', 'True',	1.5708, 'Finger-1-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
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
	('Finger-1-2_R', 'True',	1.5708, 'Finger-1-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-3_R', 'True',	1.5708, 'Finger-1-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
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

	addPoseBone(fp, 'True', 'Finger-1-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, 
		[('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-1-2_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, 
		[('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-1-3_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-1-IK_L', 3, None, (True, False), 'fFingerIK']),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-1-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-1-2_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0,
		[('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-1-3_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-1-IK_R', 3,  None, (True, False), 'fFingerIK']),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-2-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-2-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-2-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-2-IK_L', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-2-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-2-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-2-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-2-IK_R', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-3-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-3-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-3-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-3-IK_L', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-3-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-3-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-3-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-3-IK_R', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-4-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-4-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-4-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-4-IK_L', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-4-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-4-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-4-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-4-IK_R', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-5-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-5-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-5-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-5-IK_L', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_L', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	addPoseBone(fp, 'True', 'Finger-5-1_R', customShape, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-5-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])
	addPoseBone(fp, 'True', 'Finger-5-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['IK', 'Finger-5-IK_R', 3,  None, (True, False), 'fFingerIK']),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]),
		('Action', C_TG_LOCAL, ['Action', 'goboFingerCurl', 'FingerCurl_R', 'LOCATION_X', (1,21), (-0.5,0.5), 'fFingerCurl'])])

	# Finger IK
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-1_L', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-1_R', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-2_L', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-2_R', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-3_L', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-3_R', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-4_L', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-4_R', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-5_L', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, 'rigArm&T_FingerIK', 'Finger-5_R', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

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
	('Finger-1-1_L',  [ (0.975, -0.0577, 0.01267, -0.2141),  (1, 0, 0, 0),  (0.9994, 0.0269, 0.0006276, 0.02332) ]),
	('Finger-1-2_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8246, -0.5485, -0.07666, 0.1153) ]),
	('Finger-1-3_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.746, -0.6509, -0.09243, 0.1059) ]),
	('Finger-2-1_L',  [ (0.98, -0.04539, 0.008959, -0.1934),  (1, 0, 0, 0),  (0.8703, -0.4792, -0.05481, 0.09955) ]),
	('Finger-2-2_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.712, -0.7022, 0, 0) ]),
	('Finger-2-3_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.85, -0.5268, 0, 0) ]),
	('Finger-3-1_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8713, -0.4899, -0.01351, 0.02403) ]),
	('Finger-3-2_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.7076, -0.7066, 0, 0) ]),
	('Finger-3-3_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8405, -0.5418, 0, 0) ]),
	('Finger-4-1_L',  [ (0.9972, 0.0031, 0.0002317, 0.07453),  (1, 0, 0, 0),  (0.8707, -0.489, 0.02597, -0.04625) ]),
	('Finger-4-2_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.71, -0.7042, 0, 0) ]),
	('Finger-4-3_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.84, -0.5426, 0, 0) ]),
	('Finger-5-1_L',  [ (0.9537, 0.02048, 0.006446, 0.3001),  (1, 0, 0, 0),  (0.8735, -0.485, 0.02113, -0.03806) ]),
	('Finger-5-2_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.7168, -0.6973, 0, 0) ]),
	('Finger-5-3_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8445, -0.5356, 0, 0) ]),

	('Finger-1-1_R',  [ (0.9386, -0.08983, -0.03174, 0.3316),  (1, 0, 0, 0),  (0.9958, 0.02071, -0.001852, -0.08907) ]),
	('Finger-1-2_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.9594, 0.2739, 0.0185, 0.0648) ]),
	('Finger-1-3_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.7585, 0.6297, 0.1072, 0.1291) ]),
	('Finger-2-1_R',  [ (0.9599, -0.06575, -0.01863, 0.272),  (1, 0, 0, 0),  (0.9256, -0.369, 0.031, -0.07775) ]),
	('Finger-2-2_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8702, -0.4927, 0, 0) ]),
	('Finger-2-3_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8933, -0.4494, 0, 0) ]),
	('Finger-3-1_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.9262, -0.3769, 0.004653, -0.01144) ]),
	('Finger-3-2_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8698, -0.4935, 0, 0) ]),
	('Finger-3-3_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8928, -0.4504, 0, 0) ]),
	('Finger-4-1_R',  [ (0.9959, 0.003674, -0.0003333, -0.09034),  (1, 0, 0, 0),  (0.9274, -0.3741, 0.0001118, -0.000277) ]),
	('Finger-4-2_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8707, -0.4918, 0, 0) ]),
	('Finger-4-3_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8936, -0.4489, 0, 0) ]),
	('Finger-5-1_R',  [ (0.9811, 0.01696, -0.003332, -0.1927),  (1, 0, 0, 0),  (0.9291, -0.3689, 0.01023, -0.02576) ]),
	('Finger-5-2_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8738, -0.4862, 0, 0) ]),
	('Finger-5-3_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.8961, -0.4438, 0, 0) ]),
]
def FingerWriteActions(fp):
	writeAction(fp, 'rigArm&T_FingerCurl', "goboFingerCurl", actionFingerCurl, False, False)

#
#	FingerProcess
#	(bone, axis, angle)
#

FingerProcess = [
	("Finger-1-1_L", "X", -0.0),
	("Finger-1-2_L", "X", -0.5),
	("Finger-1-3_L", "X", -0.5),
	("Finger-2-1_L", "X", -0.0),
	("Finger-2-2_L", "X", -0.5),
	("Finger-2-3_L", "X", -0.5),
	("Finger-3-1_L", "X", -0.0),
	("Finger-3-2_L", "X", -0.5),
	("Finger-3-3_L", "X", -0.5),
	("Finger-4-1_L", "X", -0.0),
	("Finger-4-2_L", "X", -0.5),
	("Finger-4-3_L", "X", -0.5),
	("Finger-5-1_L", "X", -0.0),
	("Finger-5-2_L", "X", -0.5),
	("Finger-5-3_L", "X", -0.5),

	("Finger-1-1_R", "X", 0.0),
	("Finger-1-2_R", "X", 0.5),
	("Finger-1-3_R", "X", 0.5),
	("Finger-2-1_R", "X", -0.0),
	("Finger-2-2_R", "X", -0.5),
	("Finger-2-3_R", "X", -0.5),
	("Finger-3-1_R", "X", -0.0),
	("Finger-3-2_R", "X", -0.5),
	("Finger-3-3_R", "X", -0.5),
	("Finger-4-1_R", "X", -0.0),
	("Finger-4-2_R", "X", -0.5),
	("Finger-4-3_R", "X", -0.5),
	("Finger-5-1_R", "X", -0.0),
	("Finger-5-2_R", "X", -0.5),
	("Finger-5-3_R", "X", -0.5),
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


