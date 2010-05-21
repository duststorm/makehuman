#
#	Face bone definitions
#

import mhx_rig
from mhx_rig import *

T_FIK = 'rigArm&T_FingerIK'
T_FRot = 'rigArm&T_FingerRot'
T_FPanel = 'rigArm&T_FingerPanel'

dx = 0.2
dy = 0.3
dz = 0.1
yoffs = [0,dy,0]

FingerJoints = [
	('r-finger-1-1',	'j', 'r-finger-1-1'),
	('r-finger-1-2',	'j', 'r-finger-1-2'),
	('r-finger-1-3',	'j', 'r-finger-1-3'),
	('r-finger-2-1',	'j', 'r-finger-2-1'),
	('r-finger-2-2',	'j', 'r-finger-2-2'),
	('r-finger-2-3',	'j', 'r-finger-2-3'),
	('r-finger-3-1',	'j', 'r-finger-3-1'),
	('r-finger-3-2',	'j', 'r-finger-3-2'),
	('r-finger-3-3',	'j', 'r-finger-3-3'),
	('r-finger-4-1',	'j', 'r-finger-4-1'),
	('r-finger-4-2',	'j', 'r-finger-4-2'),
	('r-finger-4-3',	'j', 'r-finger-4-3'),
	('r-finger-5-1',	'j', 'r-finger-5-1'),
	('r-finger-5-2',	'j', 'r-finger-5-2'),
	('r-finger-5-3',	'j', 'r-finger-5-3'),

	('l-finger-1-1',	'j', 'l-finger-1-1'),
	('l-finger-1-2',	'j', 'l-finger-1-2'),
	('l-finger-1-3',	'j', 'l-finger-1-3'),
	('l-finger-2-1',	'j', 'l-finger-2-1'),
	('l-finger-2-2',	'j', 'l-finger-2-2'),
	('l-finger-2-3',	'j', 'l-finger-2-3'),
	('l-finger-3-1',	'j', 'l-finger-3-1'),
	('l-finger-3-2',	'j', 'l-finger-3-2'),
	('l-finger-3-3',	'j', 'l-finger-3-3'),
	('l-finger-4-1',	'j', 'l-finger-4-1'),
	('l-finger-4-2',	'j', 'l-finger-4-2'),
	('l-finger-4-3',	'j', 'l-finger-4-3'),
	('l-finger-5-1',	'j', 'l-finger-5-1'),
	('l-finger-5-2',	'j', 'l-finger-5-2'),
	('l-finger-5-3',	'j', 'l-finger-5-3'),

	('l-finger-1-end',	'l', ((2.0, 'l-finger-1-3'), (-1.0, 'l-finger-1-2'))),
	('l-finger-2-end',	'l', ((2.0, 'l-finger-2-3'), (-1.0, 'l-finger-2-2'))),
	('l-finger-3-end',	'l', ((2.0, 'l-finger-3-3'), (-1.0, 'l-finger-3-2'))),
	('l-finger-4-end',	'l', ((2.0, 'l-finger-4-3'), (-1.0, 'l-finger-4-2'))),
	('l-finger-5-end',	'l', ((2.0, 'l-finger-5-3'), (-1.0, 'l-finger-5-2'))),
	('r-finger-1-end',	'l', ((2.0, 'r-finger-1-3'), (-1.0, 'r-finger-1-2'))),
	('r-finger-2-end',	'l', ((2.0, 'r-finger-2-3'), (-1.0, 'r-finger-2-2'))),
	('r-finger-3-end',	'l', ((2.0, 'r-finger-3-3'), (-1.0, 'r-finger-3-2'))),
	('r-finger-4-end',	'l', ((2.0, 'r-finger-4-3'), (-1.0, 'r-finger-4-2'))),
	('r-finger-5-end',	'l', ((2.0, 'r-finger-5-3'), (-1.0, 'r-finger-5-2'))),

	('l-palm-1',		'l', ((0.6, 'l-hand'), (0.4, 'l-finger-2-1'))),
	('l-palm-2',		'l', ((0.6, 'l-hand'), (0.4, 'l-finger-5-1'))),
	('r-palm-1',		'l', ((0.6, 'r-hand'), (0.4, 'r-finger-2-1'))),
	('r-palm-2',		'l', ((0.6, 'r-hand'), (0.4, 'r-finger-5-1'))),

	('DrvHand_L',		'o', ('r-hand', [0,1,0])),
	('DrvFinger-1_L',	'o', ('DrvHand_L', [dx,0,2*dz])),
	('DrvFinger-2_L',	'o', ('DrvHand_L', [dx,0,dz])),
	('DrvFinger-3_L',	'o', ('DrvHand_L', [dx,0,0])),
	('DrvFinger-4_L',	'o', ('DrvHand_L', [dx,0,-dz])),
	('DrvFinger-5_L',	'o', ('DrvHand_L', [dx,0,-2*dz])),

	('DrvHand_R',		'o', ('l-hand', [0,1,0])),
	('DrvFinger-1_R',	'o', ('DrvHand_R', [-dx,0,2*dz])),
	('DrvFinger-2_R',	'o', ('DrvHand_R', [-dx,0,dz])),
	('DrvFinger-3_R',	'o', ('DrvHand_R', [-dx,0,0])),
	('DrvFinger-4_R',	'o', ('DrvHand_R', [-dx,0,-dz])),
	('DrvFinger-5_R',	'o', ('DrvHand_R', [-dx,0,-2*dz])),

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

	('Wrist-1_L',			'r-hand', 'r-palm-1'),
	('Wrist-2_L',			'r-hand', 'r-palm-2'),
	('Palm-1_L',			'r-hand', 'r-finger-1-1'),
	('Palm-2_L',			'r-palm-1', 'r-finger-2-1'),
	('Palm-3_L',			'r-palm-1', 'r-finger-3-1'),
	('Palm-4_L',			'r-palm-2', 'r-finger-4-1'),
	('Palm-5_L',			'r-palm-2', 'r-finger-5-1'),

	('Wrist-1_R',			'l-hand', 'l-palm-1'),
	('Wrist-2_R',			'l-hand', 'l-palm-2'),
	('Palm-1_R',			'l-hand', 'l-finger-1-1'),
	('Palm-2_R',			'l-palm-1', 'l-finger-2-1'),
	('Palm-3_R',			'l-palm-1', 'l-finger-3-1'),
	('Palm-4_R',			'l-palm-2', 'l-finger-4-1'),
	('Palm-5_R',			'l-palm-2', 'l-finger-5-1'),

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

	('DrvHand_L',			'DrvHand_L', ('DrvHand_L', yoffs)),
	('DrvFinger-1_L',		'DrvFinger-1_L', ('DrvFinger-1_L', yoffs)),
	('DrvFinger-2_L',		'DrvFinger-2_L', ('DrvFinger-2_L', yoffs)),
	('DrvFinger-3_L',		'DrvFinger-3_L', ('DrvFinger-3_L', yoffs)),
	('DrvFinger-4_L',		'DrvFinger-4_L', ('DrvFinger-4_L', yoffs)),
	('DrvFinger-5_L',		'DrvFinger-5_L', ('DrvFinger-5_L', yoffs)),

	('DrvHand_R',			'DrvHand_R', ('DrvHand_R', yoffs)),
	('DrvFinger-1_R',		'DrvFinger-1_R', ('DrvFinger-1_R', yoffs)),
	('DrvFinger-2_R',		'DrvFinger-2_R', ('DrvFinger-2_R', yoffs)),
	('DrvFinger-3_R',		'DrvFinger-3_R', ('DrvFinger-3_R', yoffs)),
	('DrvFinger-4_R',		'DrvFinger-4_R', ('DrvFinger-4_R', yoffs)),
	('DrvFinger-5_R',		'DrvFinger-5_R', ('DrvFinger-5_R', yoffs)),
]
'''
	('PHand_L',			'PHand_L', ('PHand_L', yoffs)),
	('PFinger-1_L',			'PFinger-1_L', ('PFinger-1_L', yoffs)),
	('PFinger-2_L',			'PFinger-2_L', ('PFinger-2_L', yoffs)),
	('PFinger-3_L',			'PFinger-3_L', ('PFinger-3_L', yoffs)),
	('PFinger-4_L',			'PFinger-4_L', ('PFinger-4_L', yoffs)),
	('PFinger-5_L',			'PFinger-5_L', ('PFinger-5_L', yoffs)),

	('PHand_R',			'PHand_R', ('PHand_R', yoffs)),
	('PFinger-1_R',			'PFinger-1_R', ('PFinger-1_R', yoffs)),
	('PFinger-2_R',			'PFinger-2_R', ('PFinger-2_R', yoffs)),
	('PFinger-3_R',			'PFinger-3_R', ('PFinger-3_R', yoffs)),
	('PFinger-4_R',			'PFinger-4_R', ('PFinger-4_R', yoffs)),
	('PFinger-5_R',			'PFinger-5_R', ('PFinger-5_R', yoffs)),
'''

ThumbRoll = 90*deg1

FingerArmature = [
	# Deform
	('Wrist-1_L', True,		0.0, 'Hand_L', F_DEF, L_PALM, (1,1,1) ),
	('Wrist-2_L', True,		0.0, 'Hand_L', F_DEF, L_PALM, (1,1,1) ),
	('Palm-1_L', True,		0.0, 'Hand_L', F_DEF, L_PALM, (1,1,1) ),
	('Palm-2_L', True,		0.0, 'Wrist-1_L', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-3_L', True,		0.0, 'Wrist-1_L', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-4_L', True,		0.0, 'Wrist-2_L', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-5_L', True,		0.0, 'Wrist-2_L', F_DEF+F_CON, L_PALM, (1,1,1) ),

	('Wrist-1_R', True,		0.0, 'Hand_R', F_DEF, L_PALM, (1,1,1) ),
	('Wrist-2_R', True,		0.0, 'Hand_R', F_DEF, L_PALM, (1,1,1) ),
	('Palm-1_R', True,		0.0, 'Hand_R', F_DEF, L_PALM, (1,1,1) ),
	('Palm-2_R', True,		0.0, 'Wrist-1_R', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-3_R', True,		0.0, 'Wrist-1_R', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-4_R', True,		0.0, 'Wrist-2_R', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-5_R', True,		0.0, 'Wrist-2_R', F_DEF+F_CON, L_PALM, (1,1,1) ),

	('Finger-1-1_L', True,		ThumbRoll, 'Palm-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-2_L', True,		ThumbRoll, 'Finger-1-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-3_L', True,		ThumbRoll, 'Finger-1-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-1_L', True,		0.0, 'Palm-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-2_L', True,		0.0, 'Finger-2-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-3_L', True,		0.0, 'Finger-2-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-1_L', True,		0.0, 'Palm-3_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-2_L', True,		0.0, 'Finger-3-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-3_L', True,		0.0, 'Finger-3-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-1_L', True,		0.0, 'Palm-4_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-2_L', True,		0.0, 'Finger-4-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-3_L', True,		0.0, 'Finger-4-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-1_L', True,		0.0, 'Palm-5_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-2_L', True,		0.0, 'Finger-5-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-3_L', True,		0.0, 'Finger-5-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),

	('Finger-1-1_R', True,		-ThumbRoll, 'Palm-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-2_R', True,		-ThumbRoll, 'Finger-1-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-3_R', True,		-ThumbRoll, 'Finger-1-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-1_R', True,		0.0, 'Palm-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-2_R', True,		0.0, 'Finger-2-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-3_R', True,		0.0, 'Finger-2-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-1_R', True,		0.0, 'Palm-3_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-2_R', True,		0.0, 'Finger-3-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-3_R', True,		0.0, 'Finger-3-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-1_R', True,		0.0, 'Palm-4_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-2_R', True,		0.0, 'Finger-4-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-3_R', True,		0.0, 'Finger-4-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-1_R', True,		0.0, 'Palm-5_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-2_R', True,		0.0, 'Finger-5-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-3_R', True,		0.0, 'Finger-5-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),

	# Finger controls
	('Finger-1_L', True,		ThumbRoll, 'Hand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-2_L', True,		0.0, 'Hand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-3_L', True,		0.0, 'Hand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-4_L', True,		0.0, 'Hand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-5_L', True,		0.0, 'Hand_L', F_WIR, L_HANDIK, (1,1,1) ),
	
	('Finger-1_R', True,		-ThumbRoll, 'Hand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-2_R', True,		0.0, 'Hand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-3_R', True,		0.0, 'Hand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-4_R', True,		0.0, 'Hand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-5_R', True,		0.0, 'Hand_R', F_WIR, L_HANDIK, (1,1,1) ),

	# IK targets
	('Finger-1-IK_L', T_FIK,	ThumbRoll, 'Finger-1_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-2-IK_L', T_FIK,	0.0, 'Finger-2_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-3-IK_L', T_FIK,	0.0, 'Finger-3_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-4-IK_L', T_FIK,	0.0, 'Finger-4_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-5-IK_L', T_FIK,	0.0, 'Finger-5_L', F_CON, L_HELP, (1,1,1) ),

	('Finger-1-IK_R', T_FIK,	-ThumbRoll, 'Finger-1_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-2-IK_R', T_FIK,	0.0, 'Finger-2_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-3-IK_R', T_FIK,	0.0, 'Finger-3_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-4-IK_R', T_FIK,	0.0, 'Finger-4_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-5-IK_R', T_FIK,	0.0, 'Finger-5_R', F_CON, L_HELP, (1,1,1) ),

	# Drivers
	('DrvHand_L', T_FPanel,		0.0, 'Hand_L', 0, L_HELP, (1,1,1) ),
	('DrvFinger-1_L', T_FPanel,	0.0, 'DrvHand_L', 0, L_HELP, (1,1,1) ),
	('DrvFinger-2_L', T_FPanel,	0.0, 'DrvHand_L', 0, L_HELP, (1,1,1) ),
	('DrvFinger-3_L', T_FPanel,	0.0, 'DrvHand_L', 0, L_HELP, (1,1,1) ),
	('DrvFinger-4_L', T_FPanel,	0.0, 'DrvHand_L', 0, L_HELP, (1,1,1) ),
	('DrvFinger-5_L', T_FPanel,	0.0, 'DrvHand_L', 0, L_HELP, (1,1,1) ),

	('DrvHand_R', T_FPanel,		0.0, 'Hand_R', 0, L_HELP, (1,1,1) ),
	('DrvFinger-1_R', T_FPanel,	0.0, 'DrvHand_R', 0, L_HELP, (1,1,1) ),
	('DrvFinger-2_R', T_FPanel,	0.0, 'DrvHand_R', 0, L_HELP, (1,1,1) ),
	('DrvFinger-3_R', T_FPanel,	0.0, 'DrvHand_R', 0, L_HELP, (1,1,1) ),
	('DrvFinger-4_R', T_FPanel,	0.0, 'DrvHand_R', 0, L_HELP, (1,1,1) ),
	('DrvFinger-5_R', T_FPanel,	0.0, 'DrvHand_R', 0, L_HELP, (1,1,1) ),
]
'''
	('PHand_L', T_FPanel,		0.0, 'Hand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-1_L', T_FPanel,	0.0, 'PHand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-2_L', T_FPanel,	0.0, 'PHand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-3_L', T_FPanel,	0.0, 'PHand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-4_L', T_FPanel,	0.0, 'PHand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-5_L', T_FPanel,	0.0, 'PHand_L', F_WIR, L_HANDIK, (1,1,1) ),

	('PHand_R', T_FPanel,		0.0, 'Hand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-1_R', T_FPanel,	0.0, 'PHand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-2_R', T_FPanel,	0.0, 'PHand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-3_R', T_FPanel,	0.0, 'PHand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-4_R', T_FPanel,	0.0, 'PHand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-5_R', T_FPanel,	0.0, 'PHand_R', F_WIR, L_HANDIK, (1,1,1) ),
'''

#
#	fingerConstraints(hand, finger):	
#	fingerDrivers(fnum, suffix):
#	FingerWriteDrivers(fp):
#	FingerWritePoses(fp):
#

def fingerSetProps(fp):
	if not PanelWorks: return
	props = ['MHRelax', 'MHCurl', 'MHCone', 'MHSpread', 'MHScrunch', 'MHLean']
	values = [0, 0, 0, 0, 0, 0]
	for suffix in ["_L", "_R"]:
		for fnum in range(1,6):
			setProps(fp, 'Finger-%s%s' % (fnum, suffix), props, values)
		setProps(fp, 'Hand%s' % suffix, props, values)
	return

def setProps(fp, bone, props, values):
	for (n,prop) in enumerate(props):
		fp.write("  SetProp %s %s %s ;\n" % (bone, prop, values[n]))
	return


def fingerConstraints(fnum, lnum, suffix):
	drvhand = "DrvHand%s" % suffix
	drvfinger = "DrvFinger-%d%s" % (fnum, suffix)
	finger = "Finger-%d%s" % (fnum, suffix)
	enable = 1.0
	if lnum == 1:
		copyRot = (('CopyRot', True), C_OW_LOCAL+C_TG_LOCAL, ['Rot', finger, enable, (1,0,1), (0,0,0), True])
	else:
		copyRot = (('CopyRot', T_FPanel), C_OW_LOCAL+C_TG_LOCAL, ['Rot', finger, enable, (1,0,0), (0,0,0), True])

	constraints = [copyRot,
		(('Action', T_FPanel), C_TG_LOCAL, ['Relax', 'ActionHand', drvhand, 'LOCATION_X', (1,7), (-0.2,0.4), enable]),
		(('Action', T_FPanel), C_TG_LOCAL, ['Curl', 'ActionHand', drvhand, 'LOCATION_Y', (11,17), (-0.2,0.4), enable]),
		(('Action', T_FPanel), C_TG_LOCAL, ['Cone', 'ActionHand', drvhand, 'LOCATION_Z', (21,27), (-0.2,0.4), enable]),
		(('Action', T_FPanel), C_TG_LOCAL, ['Spread', 'ActionHand', drvhand, 'ROTATION_X', (31,37), (-20,40), enable]),
		(('Action', T_FPanel), C_TG_LOCAL, ['Scrunch', 'ActionHand', drvhand, 'ROTATION_Y', (41,47), (-20,40), enable]),
		(('Action', T_FPanel), C_TG_LOCAL, ['Lean', 'ActionHand', drvhand, 'ROTATION_Z', (52,58), (-40,40), enable]),
		]
	return constraints

def actionDrivers(driven, suffix):
	if PanelWorks:
		path = 'pose.bones["PHand%s"]' % suffix
		return [
			(driven, 'LOC', None, 0, (0,0.8), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHRelax"]')])]), 
			(driven, 'LOC', None, 1, (0,0.8), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHCurl"]')])]), 
			(driven, 'LOC', None, 2, (0,0.8), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHCone"]')])]), 
			(driven, 'ROTE', None, 0, (0,deg80), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHSpread"]')])]), 
			(driven, 'ROTE', None, 1, (0,deg80), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHScrunch"]')])]), 
			(driven, 'ROTE', None, 2, (0,deg80), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHLean"]')])]), 
			]
	else:
		if suffix == '_R': sign = -1 
		else: sign = 1
		return [
			(driven, 'LOC', None, 0, (0,sign*0.8), [("var", 'TRANSFORMS', [('HumanRig', 'MHRelax%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			(driven, 'LOC', None, 1, (0,sign*0.8), [("var", 'TRANSFORMS', [('HumanRig', 'MHCurl%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			(driven, 'LOC', None, 2, (0,sign*0.8), [("var", 'TRANSFORMS', [('HumanRig', 'MHCone%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			(driven, 'ROTE', None, 0, (0,sign*deg80), [("var", 'TRANSFORMS', [('HumanRig', 'MHSpread%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			(driven, 'ROTE', None, 1, (0,sign*deg80), [("var", 'TRANSFORMS', [('HumanRig', 'MHScrunch%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			(driven, 'ROTE', None, 2, (0,sign*deg80), [("var", 'TRANSFORMS', [('HumanRig', 'MHLean%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			]

def rotationDrivers(fnum, suffix, driven):
	return [
		(driven, 'ROTQ', None, 1, (-120*deg1,120*deg1),
		 [("var", 'TRANSFORMS', [('HumanRig', 'Finger-%d%s' % (fnum, suffix), 'SCALE_Y', C_LOCAL)])]),
		]

def FingerWriteDrivers(fp):
	drivers = []
	for suffix in ["_L", "_R"]:
		'''
		for fnum in range(1,6):
			driven = 'DrvFinger-%s%s' % (fnum, suffix)
			path = 'pose.bones["Finger-%s%s"]' % (fnum, suffix)
			drivers += actionDrivers(driven, path)
		'''
		driven = 'DrvHand%s' % suffix
		drivers += actionDrivers(driven, suffix)
	# (bone, typ, name, index, coeffs, variables)
	writeDrivers(fp, T_FPanel, drivers)

	drivers = []
	for suffix in ["_L", "_R"]:
		for fnum in range(1,6):
			for lnum in range(2,4):
				driven = 'Finger-%d-%d%s' % (fnum, lnum, suffix)
				drivers += rotationDrivers(fnum, suffix, driven)
	writeDrivers(fp, T_FRot, drivers)


	#fingerSetProps(fp)
	#for fnum in range(1,6):
	#	addControlFinger(fp, fnum, "_L")
	#	addControlFinger(fp, fnum, "_R")
	return

#
#	defineFingerConstraints():
#

def defineFingerConstraints():
	fconstraints = {}
	for fnum in range(1,6):
		for suffix in ["_L", "_R"]:
			for lnum in range(1,4):
				constraints = fingerConstraints(fnum, lnum, suffix)
				if lnum == 3:
					constraints.append( (('IK', T_FIK), 0, ['IK', 'Finger-%d-IK_L' % fnum, 3, None, (True, False,True), 1.0]) )
				if fnum >= 2:
					constraints.append( ('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)]) )
				fconstraints["%d-%d%s" % (fnum, lnum, suffix)] = constraints
	return fconstraints
	
fconstraints = defineFingerConstraints()	
customShape = 'MHCircle05'
customShape = None
		
FingerPoses = [
	('poseBone', True, 'Finger-1-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, fconstraints["1-1_L"]),
	('poseBone', True, 'Finger-1-2_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, fconstraints["1-2_L"]),
	('poseBone', True, 'Finger-1-3_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, fconstraints["1-3_L"]),

	('poseBone', True, 'Finger-1-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, fconstraints["1-1_R"]),
	('poseBone', True, 'Finger-1-2_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, fconstraints["1-2_R"]),
	('poseBone', True, 'Finger-1-3_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, fconstraints["1-3_R"]),

	('poseBone', True, 'Finger-2-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, fconstraints["2-1_L"]),
	('poseBone', True, 'Finger-2-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["2-2_L"]),
	('poseBone', True, 'Finger-2-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["2-3_L"]),

	('poseBone', True, 'Finger-2-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, fconstraints["2-1_R"]),
	('poseBone', True, 'Finger-2-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["2-2_R"]),
	('poseBone', True, 'Finger-2-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["2-3_R"]),

	('poseBone', True, 'Finger-3-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, fconstraints["3-1_L"]),
	('poseBone', True, 'Finger-3-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["3-2_L"]),
	('poseBone', True, 'Finger-3-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["3-3_L"]),

	('poseBone', True, 'Finger-3-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, fconstraints["3-1_R"]),
	('poseBone', True, 'Finger-3-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["3-2_R"]),
	('poseBone', True, 'Finger-3-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["3-3_R"]),

	('poseBone', True, 'Finger-4-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, fconstraints["4-1_L"]),
	('poseBone', True, 'Finger-4-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["4-2_L"]),
	('poseBone', True, 'Finger-4-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["4-3_L"]),

	('poseBone', True, 'Finger-4-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, fconstraints["4-1_R"]),
	('poseBone', True, 'Finger-4-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["4-2_R"]),
	('poseBone', True, 'Finger-4-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["4-3_R"]),

	('poseBone', True, 'Finger-5-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, fconstraints["5-1_L"]),
	('poseBone', True, 'Finger-5-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["5-2_L"]),
	('poseBone', True, 'Finger-5-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["5-3_L"]),

	('poseBone', True, 'Finger-5-1_R', customShape, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, fconstraints["5-1_R"]),
	('poseBone', True, 'Finger-5-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["5-2_R"]),
	('poseBone', True, 'Finger-5-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, fconstraints["5-3_R"]),

	# Panel fingers
	('poseBone', T_FPanel, 'DrvHand_L', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), P_XYZ, []),
	('poseBone', T_FPanel, 'DrvFinger-1_L', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, []),
	('poseBone', T_FPanel, 'DrvFinger-2_L', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, []),
	('poseBone', T_FPanel, 'DrvFinger-3_L', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, []),
	('poseBone', T_FPanel, 'DrvFinger-4_L', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, []),
	('poseBone', T_FPanel, 'DrvFinger-5_L', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, []),
	
	('poseBone', T_FPanel, 'DrvHand_R', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), P_XYZ, []),
	('poseBone', T_FPanel, 'DrvFinger-1_R', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, []),
	('poseBone', T_FPanel, 'DrvFinger-2_R', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, []),
	('poseBone', T_FPanel, 'DrvFinger-3_R', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, []),
	('poseBone', T_FPanel, 'DrvFinger-4_R', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, []),
	('poseBone', T_FPanel, 'DrvFinger-5_R', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, []),
	
	# Control fingers
	('poseBone', True, 'Finger-1_L', 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, 
		[('LimitScale', 0, ['LimitScale', (1,1, 0.1,1.5, 1,1), (0,1,0)])]),
	('poseBone', True, 'Finger-2_L', 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, 
		[('LimitScale', 0, ['LimitScale', (1,1, 0.1,1.5, 1,1), (0,1,0)])]),
	('poseBone', True, 'Finger-3_L', 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, 
		[('LimitScale', 0, ['LimitScale', (1,1, 0.1,1.5, 1,1), (0,1,0)])]),
	('poseBone', True, 'Finger-4_L', 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, 
		[('LimitScale', 0, ['LimitScale', (1,1, 0.1,1.5, 1,1), (0,1,0)])]),
	('poseBone', True, 'Finger-5_L', 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, 
		[('LimitScale', 0, ['LimitScale', (1,1, 0.1,1.5, 1,1), (0,1,0)])]),
	
	('poseBone', True, 'Finger-1_R', 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, 
		[('LimitScale', 0, ['LimitScale', (1,1, 0.1,1.5, 1,1), (0,1,0)])]),
	('poseBone', True, 'Finger-2_R', 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, 
		[('LimitScale', 0, ['LimitScale', (1,1, 0.1,1.5, 1,1), (0,1,0)])]),
	('poseBone', True, 'Finger-3_R', 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, 
		[('LimitScale', 0, ['LimitScale', (1,1, 0.1,1.5, 1,1), (0,1,0)])]),
	('poseBone', True, 'Finger-4_R', 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, 
		[('LimitScale', 0, ['LimitScale', (1,1, 0.1,1.5, 1,1), (0,1,0)])]),
	('poseBone', True, 'Finger-5_R', 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, 
		[('LimitScale', 0, ['LimitScale', (1,1, 0.1,1.5, 1,1), (0,1,0)])]),
]	


def addControlFinger(fp, fnum, suffix):
	('poseBone', True, 'Finger-%s%s' % (fnum, suffix), 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, 
		[('LimitScale', 0, ['LimitScale', (1,1, 0.1,1.5, 1,1), (0,1,0)])])

	('poseBone', T_FIK, 'Finger-%s-IK%s' % (fnum, suffix), None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	('poseBone', T_FPanel, 'DrvFinger-%s%s' % (fnum, suffix), None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, [])
	return 

#
#	actionFingerCurl
#	FingerWriteActions(fp):
#

import actions_finger_25

def FingerWriteActions(fp):
	writeAction(fp, T_FPanel, "ActionHand", actions_finger_25.ActionHand, False, False)

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


