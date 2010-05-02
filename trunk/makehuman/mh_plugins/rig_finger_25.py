#
#	Face bone definitions
#

import mhx_rig
from mhx_rig import *

T_FIK = 'rigArm&T_FingerIK'
T_FPanel = 'rigArm&T_FingerPanel'

dx = 0.2
dy = 0.3
dz = 0.1

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

	('l-palm-1',			'l', ((0.6, 'l-hand'), (0.4, 'l-finger-2-1'))),
	('l-palm-2',			'l', ((0.6, 'l-hand'), (0.4, 'l-finger-5-1'))),
	('r-palm-1',			'l', ((0.6, 'r-hand'), (0.4, 'r-finger-2-1'))),
	('r-palm-2',			'l', ((0.6, 'r-hand'), (0.4, 'r-finger-5-1'))),

	('Fingers_R_head',		'o', ('l-finger-3-1', [0.0, 1.0, 0.0])),
	('Fingers_R_tail',		'o', ('l-finger-3-end', [0.0, 1.0, 0.0])),
	('Fingers_L_head',		'o', ('r-finger-3-1', [0.0, 1.0, 0.0])),
	('Fingers_L_tail',		'o', ('r-finger-3-end', [0.0, 1.0, 0.0])),

	('PHand_L_head',		'o', ('r-hand', [0,1,0])),
	('PFinger-1_L_head',		'o', ('PHand_L_head', [dx,0,2*dz])),
	('PFinger-2_L_head',		'o', ('PHand_L_head', [dx,0,dz])),
	('PFinger-3_L_head',		'o', ('PHand_L_head', [dx,0,0])),
	('PFinger-4_L_head',		'o', ('PHand_L_head', [dx,0,-dz])),
	('PFinger-5_L_head',		'o', ('PHand_L_head', [dx,0,-2*dz])),

	('PHand_L_tail',		'o', ('PHand_L_head', [0,dy,0])),
	('PFinger-1_L_tail',		'o', ('PFinger-1_L_head', [0,dy,0])),
	('PFinger-2_L_tail',		'o', ('PFinger-2_L_head', [0,dy,0])),
	('PFinger-3_L_tail',		'o', ('PFinger-3_L_head', [0,dy,0])),
	('PFinger-4_L_tail',		'o', ('PFinger-4_L_head', [0,dy,0])),
	('PFinger-5_L_tail',		'o', ('PFinger-5_L_head', [0,dy,0])),

	('PHand_R_head',		'o', ('l-hand', [0,1,0])),
	('PFinger-1_R_head',		'o', ('PHand_R_head', [-dx,0,2*dz])),
	('PFinger-2_R_head',		'o', ('PHand_R_head', [-dx,0,dz])),
	('PFinger-3_R_head',		'o', ('PHand_R_head', [-dx,0,0])),
	('PFinger-4_R_head',		'o', ('PHand_R_head', [-dx,0,-dz])),
	('PFinger-5_R_head',		'o', ('PHand_R_head', [-dx,0,-2*dz])),

	('PHand_R_tail',		'o', ('PHand_R_head', [0,dy,0])),
	('PFinger-1_R_tail',		'o', ('PFinger-1_R_head', [0,dy,0])),
	('PFinger-2_R_tail',		'o', ('PFinger-2_R_head', [0,dy,0])),
	('PFinger-3_R_tail',		'o', ('PFinger-3_R_head', [0,dy,0])),
	('PFinger-4_R_tail',		'o', ('PFinger-4_R_head', [0,dy,0])),
	('PFinger-5_R_tail',		'o', ('PFinger-5_R_head', [0,dy,0])),

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

	('PHand_L',			'PHand_L_head', 'PHand_L_tail'),
	('PFinger-1_L',			'PFinger-1_L_head', 'PFinger-1_L_tail'),
	('PFinger-2_L',			'PFinger-2_L_head', 'PFinger-2_L_tail'),
	('PFinger-3_L',			'PFinger-3_L_head', 'PFinger-3_L_tail'),
	('PFinger-4_L',			'PFinger-4_L_head', 'PFinger-4_L_tail'),
	('PFinger-5_L',			'PFinger-5_L_head', 'PFinger-5_L_tail'),

	('DrvHand_L',			'PHand_L_head', 'PHand_L_tail'),
	('DrvFinger-1_L',		'PFinger-1_L_head', 'PFinger-1_L_tail'),
	('DrvFinger-2_L',		'PFinger-2_L_head', 'PFinger-2_L_tail'),
	('DrvFinger-3_L',		'PFinger-3_L_head', 'PFinger-3_L_tail'),
	('DrvFinger-4_L',		'PFinger-4_L_head', 'PFinger-4_L_tail'),
	('DrvFinger-5_L',		'PFinger-5_L_head', 'PFinger-5_L_tail'),

	('PHand_R',			'PHand_R_head', 'PHand_R_tail'),
	('PFinger-1_R',			'PFinger-1_R_head', 'PFinger-1_R_tail'),
	('PFinger-2_R',			'PFinger-2_R_head', 'PFinger-2_R_tail'),
	('PFinger-3_R',			'PFinger-3_R_head', 'PFinger-3_R_tail'),
	('PFinger-4_R',			'PFinger-4_R_head', 'PFinger-4_R_tail'),
	('PFinger-5_R',			'PFinger-5_R_head', 'PFinger-5_R_tail'),

	('DrvHand_R',			'PHand_R_head', 'PHand_R_tail'),
	('DrvFinger-1_R',		'PFinger-1_R_head', 'PFinger-1_R_tail'),
	('DrvFinger-2_R',		'PFinger-2_R_head', 'PFinger-2_R_tail'),
	('DrvFinger-3_R',		'PFinger-3_R_head', 'PFinger-3_R_tail'),
	('DrvFinger-4_R',		'PFinger-4_R_head', 'PFinger-4_R_tail'),
	('DrvFinger-5_R',		'PFinger-5_R_head', 'PFinger-5_R_tail'),
]

FingerArmature = [
	# Deform
	('Wrist-1_L', 'True',		0.0, 'Hand_L', F_DEF, L_PALM, (1,1,1) ),
	('Wrist-2_L', 'True',		0.0, 'Hand_L', F_DEF, L_PALM, (1,1,1) ),
	('Palm-1_L', 'True',		0.0, 'Hand_L', F_DEF, L_PALM, (1,1,1) ),
	('Palm-2_L', 'True',		0.0, 'Wrist-1_L', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-3_L', 'True',		0.0, 'Wrist-1_L', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-4_L', 'True',		0.0, 'Wrist-2_L', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-5_L', 'True',		0.0, 'Wrist-2_L', F_DEF+F_CON, L_PALM, (1,1,1) ),

	('Wrist-1_R', 'True',		0.0, 'Hand_R', F_DEF, L_PALM, (1,1,1) ),
	('Wrist-2_R', 'True',		0.0, 'Hand_R', F_DEF, L_PALM, (1,1,1) ),
	('Palm-1_R', 'True',		0.0, 'Hand_R', F_DEF, L_PALM, (1,1,1) ),
	('Palm-2_R', 'True',		0.0, 'Wrist-1_R', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-3_R', 'True',		0.0, 'Wrist-1_R', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-4_R', 'True',		0.0, 'Wrist-2_R', F_DEF+F_CON, L_PALM, (1,1,1) ),
	('Palm-5_R', 'True',		0.0, 'Wrist-2_R', F_DEF+F_CON, L_PALM, (1,1,1) ),

	('Finger-1-1_L', 'True',	0.0, 'Palm-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-2_L', 'True',	deg90, 'Finger-1-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-3_L', 'True',	deg90, 'Finger-1-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-1_L', 'True',	0.0, 'Palm-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-2_L', 'True',	0.0, 'Finger-2-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-3_L', 'True',	0.0, 'Finger-2-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-1_L', 'True',	0.0, 'Palm-3_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-2_L', 'True',	0.0, 'Finger-3-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-3_L', 'True',	0.0, 'Finger-3-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-1_L', 'True',	0.0, 'Palm-4_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-2_L', 'True',	0.0, 'Finger-4-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-3_L', 'True',	0.0, 'Finger-4-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-1_L', 'True',	0.0, 'Palm-5_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-2_L', 'True',	0.0, 'Finger-5-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-3_L', 'True',	0.0, 'Finger-5-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),

	('Finger-1-1_R', 'True',	0.0, 'Palm-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-2_R', 'True',	-deg90, 'Finger-1-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-3_R', 'True',	-deg90, 'Finger-1-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-1_R', 'True',	0.0, 'Palm-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-2_R', 'True',	0.0, 'Finger-2-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-3_R', 'True',	0.0, 'Finger-2-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-1_R', 'True',	0.0, 'Palm-3_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-2_R', 'True',	0.0, 'Finger-3-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-3_R', 'True',	0.0, 'Finger-3-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-1_R', 'True',	0.0, 'Palm-4_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-2_R', 'True',	0.0, 'Finger-4-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-3_R', 'True',	0.0, 'Finger-4-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-1_R', 'True',	0.0, 'Palm-5_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-2_R', 'True',	0.0, 'Finger-5-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-3_R', 'True',	0.0, 'Finger-5-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),

	# Finger controls
	('Finger-1_L', T_FIK,		0.0, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-2_L', T_FIK,		0.0, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-3_L', T_FIK,		0.0, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-4_L', T_FIK,		0.0, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-5_L', T_FIK,		0.0, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	
	('Finger-1_R', T_FIK,		0.0, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-2_R', T_FIK,		0.0, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-3_R', T_FIK,		0.0, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-4_R', T_FIK,		0.0, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-5_R', T_FIK,		0.0, 'Hand_R', 0, L_HANDIK, (1,1,1) ),

	# IK targets
	('Finger-1-IK_L', T_FIK,	0.0, 'Finger-1_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-2-IK_L', T_FIK,	0.0, 'Finger-2_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-3-IK_L', T_FIK,	0.0, 'Finger-3_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-4-IK_L', T_FIK,	0.0, 'Finger-4_L', F_CON, L_HELP, (1,1,1) ),
	('Finger-5-IK_L', T_FIK,	0.0, 'Finger-5_L', F_CON, L_HELP, (1,1,1) ),

	('Finger-1-IK_R', T_FIK,	0.0, 'Finger-1_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-2-IK_R', T_FIK,	0.0, 'Finger-2_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-3-IK_R', T_FIK,	0.0, 'Finger-3_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-4-IK_R', T_FIK,	0.0, 'Finger-4_R', F_CON, L_HELP, (1,1,1) ),
	('Finger-5-IK_R', T_FIK,	0.0, 'Finger-5_R', F_CON, L_HELP, (1,1,1) ),

	# Drivers
	('PHand_L', T_FPanel,		0.0, 'Hand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-1_L', T_FPanel,	0.0, 'PHand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-2_L', T_FPanel,	0.0, 'PHand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-3_L', T_FPanel,	0.0, 'PHand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-4_L', T_FPanel,	0.0, 'PHand_L', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-5_L', T_FPanel,	0.0, 'PHand_L', F_WIR, L_HANDIK, (1,1,1) ),

	('DrvHand_L', T_FPanel,		0.0, 'PHand_L', 0, L_HELP, (1,1,1) ),
	('DrvFinger-1_L', T_FPanel,	0.0, 'PHand_L', 0, L_HELP, (1,1,1) ),
	('DrvFinger-2_L', T_FPanel,	0.0, 'PHand_L', 0, L_HELP, (1,1,1) ),
	('DrvFinger-3_L', T_FPanel,	0.0, 'PHand_L', 0, L_HELP, (1,1,1) ),
	('DrvFinger-4_L', T_FPanel,	0.0, 'PHand_L', 0, L_HELP, (1,1,1) ),
	('DrvFinger-5_L', T_FPanel,	0.0, 'PHand_L', 0, L_HELP, (1,1,1) ),

	('PHand_R', T_FPanel,		0.0, 'Hand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-1_R', T_FPanel,	0.0, 'PHand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-2_R', T_FPanel,	0.0, 'PHand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-3_R', T_FPanel,	0.0, 'PHand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-4_R', T_FPanel,	0.0, 'PHand_R', F_WIR, L_HANDIK, (1,1,1) ),
	('PFinger-5_R', T_FPanel,	0.0, 'PHand_R', F_WIR, L_HANDIK, (1,1,1) ),

	('DrvHand_R', T_FPanel,		0.0, 'PHand_R', 0, L_HELP, (1,1,1) ),
	('DrvFinger-1_R', T_FPanel,	0.0, 'PHand_R', 0, L_HELP, (1,1,1) ),
	('DrvFinger-2_R', T_FPanel,	0.0, 'PHand_R', 0, L_HELP, (1,1,1) ),
	('DrvFinger-3_R', T_FPanel,	0.0, 'PHand_R', 0, L_HELP, (1,1,1) ),
	('DrvFinger-4_R', T_FPanel,	0.0, 'PHand_R', 0, L_HELP, (1,1,1) ),
	('DrvFinger-5_R', T_FPanel,	0.0, 'PHand_R', 0, L_HELP, (1,1,1) ),
]

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
			setProps(fp, 'PFinger-%s%s' % (fnum, suffix), props, values)
		setProps(fp, 'PHand%s' % suffix, props, values)
	return

def setProps(fp, bone, props, values):
	for (n,prop) in enumerate(props):
		fp.write("  SetProp %s %s %s ;\n" % (bone, prop, values[n]))
	return


def fingerConstraints(fnum, suffix):
	hand = "DrvHand%s" % suffix
	finger = "DrvFinger-%s%s" % (fnum, suffix)
	enable = 1.0
	constraints = [
		(('Action', T_FPanel), C_TG_LOCAL, ['Relax', 'ActionHand', hand, 'LOCATION_X', (1,7), (-0.2,0.4), enable]),
		(('Action', T_FPanel), C_TG_LOCAL, ['Curl', 'ActionHand', hand, 'LOCATION_Y', (11,17), (-0.2,0.4), enable]),
		(('Action', T_FPanel), C_TG_LOCAL, ['Cone', 'ActionHand', hand, 'LOCATION_Z', (21,27), (-0.2,0.4), enable]),
		(('Action', T_FPanel), C_TG_LOCAL, ['Spread', 'ActionHand', hand, 'ROTATION_X', (31,37), (-20,40), enable]),
		(('Action', T_FPanel), C_TG_LOCAL, ['Scrunch', 'ActionHand', hand, 'ROTATION_Y', (41,47), (-20,40), enable]),
		(('Action', T_FPanel), C_TG_LOCAL, ['Lean', 'ActionHand', hand, 'ROTATION_Z', (52,58), (-40,40), enable]),
		]
	return constraints

def fingerDrivers(driver, suffix):
	if PanelWorks:
		path = 'pose.bones["PHand%s"]' % suffix
		return [
			(driver, 'LOC', None, 0, (0,0.4), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHRelax"]')])]), 
			(driver, 'LOC', None, 1, (0,0.4), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHCurl"]')])]), 
			(driver, 'LOC', None, 2, (0,0.4), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHCone"]')])]), 
			(driver, 'ROTE', None, 0, (0,deg40), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHSpread"]')])]), 
			(driver, 'ROTE', None, 1, (0,deg40), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHScrunch"]')])]), 
			(driver, 'ROTE', None, 2, (0,deg40), [("var", 'SINGLE_PROP', [('HumanRig', path+'["MHLean"]')])]), 
			]
	else:
		if suffix == '_R': sign = -1 
		else: sign = 1
		return [
			(driver, 'LOC', None, 0, (0,sign*0.4), [("var", 'TRANSFORMS', [('HumanRig', 'MHRelax%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			(driver, 'LOC', None, 1, (0,sign*0.4), [("var", 'TRANSFORMS', [('HumanRig', 'MHCurl%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			(driver, 'LOC', None, 2, (0,sign*0.4), [("var", 'TRANSFORMS', [('HumanRig', 'MHCone%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			(driver, 'ROTE', None, 0, (0,sign*deg40), [("var", 'TRANSFORMS', [('HumanRig', 'MHSpread%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			(driver, 'ROTE', None, 1, (0,sign*deg40), [("var", 'TRANSFORMS', [('HumanRig', 'MHScrunch%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			(driver, 'ROTE', None, 2, (0,sign*deg40), [("var", 'TRANSFORMS', [('HumanRig', 'MHLean%s' % suffix, 'LOC_X', C_LOCAL)])]), 
			]


def FingerWriteDrivers(fp):
	drivers = []
	for suffix in ["_L", "_R"]:
		'''
		for fnum in range(1,6):
			driver = 'DrvFinger-%s%s' % (fnum, suffix)
			path = 'pose.bones["PFinger-%s%s"]' % (fnum, suffix)
			drivers += fingerDrivers(driver, path)
		'''
		driver = 'DrvHand%s' % suffix
		drivers += fingerDrivers(driver, suffix)
	# (bone, typ, name, index, coeffs, variables)
	writeDrivers(fp, T_FPanel, drivers)
	return

def FingerWritePoses(fp):
	global boneGroups
	boneGroups = {}

	customShape = 'MHCircle05'
	customShape = None
	# Deform with finger IK

	fingerSetProps(fp)

	constraints = fingerConstraints("1-1", "_L") 
	addPoseBone(fp, 'True', 'Finger-1-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, constraints)

	constraints = fingerConstraints("1-2", "_L") 
	addPoseBone(fp, 'True', 'Finger-1-2_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, constraints)

	constraints = fingerConstraints("1-3", "_L") 
	constraints += [ (('IK', T_FIK), 0, ['IK', 'Finger-1-IK_L', 3, None, (True, False), 1.0]) ]
	addPoseBone(fp, 'True', 'Finger-1-3_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, constraints)

	constraints = fingerConstraints("1-1", "_R") 
	addPoseBone(fp, 'True', 'Finger-1-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, constraints)

	constraints = fingerConstraints("1-2", "_R") 
	addPoseBone(fp, 'True', 'Finger-1-2_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, constraints)

	constraints = fingerConstraints("1-3", "_R") 
	constraints += [(('IK', T_FIK), 0, ['IK', 'Finger-1-IK_R', 3,  None, (True, False), 1.0])]
	addPoseBone(fp, 'True', 'Finger-1-3_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, constraints)

	constraints = fingerConstraints("2-1", "_L") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-2-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, constraints)

	constraints = fingerConstraints("2-2", "_L") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-2-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,  constraints)

	constraints = fingerConstraints("2-3", "_L") 
	constraints += [(('IK', T_FIK), 0, ['IK', 'Finger-2-IK_L', 3,  None, (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-2-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, constraints)

	constraints = fingerConstraints("2-1", "_R") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-2-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, constraints)

	constraints = fingerConstraints("2-2", "_R") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-2-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,  constraints)

	constraints = fingerConstraints("2-3", "_R") 
	constraints += [(('IK', T_FIK), 0, ['IK', 'Finger-2-IK_R', 3,  None, (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-2-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, constraints)

	constraints = fingerConstraints("3-1", "_L") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-3-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, constraints)

	constraints = fingerConstraints("3-2", "_L") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-3-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,  constraints)

	constraints = fingerConstraints("3-3", "_L") 
	constraints += [(('IK', T_FIK), 0, ['IK', 'Finger-3-IK_L', 3,  None, (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-3-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, constraints)

	constraints = fingerConstraints("3-1", "_R") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-3-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, constraints)

	constraints = fingerConstraints("3-2", "_R") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-3-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,  constraints)

	constraints = fingerConstraints("3-3", "_R") 
	constraints += [(('IK', T_FIK), 0, ['IK', 'Finger-3-IK_R', 3,  None, (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-3-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, constraints)

	constraints = fingerConstraints("4-1", "_L") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-4-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, constraints)

	constraints = fingerConstraints("4-2", "_L") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-4-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,  constraints)

	constraints = fingerConstraints("4-3", "_L") 
	constraints += [(('IK', T_FIK), 0, ['IK', 'Finger-4-IK_L', 3,  None, (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-4-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, constraints)

	constraints = fingerConstraints("4-1", "_R") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-4-1_R', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, constraints)

	constraints = fingerConstraints("4-2", "_R") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-4-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,  constraints)

	constraints = fingerConstraints("4-3", "_R") 
	constraints += [(('IK', T_FIK), 0, ['IK', 'Finger-4-IK_R', 3,  None, (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-4-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, constraints)

	constraints = fingerConstraints("5-1", "_L") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-5-1_L', customShape, None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0, constraints)

	constraints = fingerConstraints("5-2", "_L") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-5-2_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,  constraints)

	constraints = fingerConstraints("5-3", "_L") 
	constraints += [(('IK', T_FIK), 0, ['IK', 'Finger-5-IK_L', 3,  None, (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-5-3_L', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, constraints)

	constraints = fingerConstraints("5-1", "_R") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.6, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-5-1_R', customShape, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, constraints)

	constraints = fingerConstraints("5-2", "_R") 
	constraints += [('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-5-2_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0,  constraints)

	constraints = fingerConstraints("5-3", "_R") 
	constraints +=	[(('IK', T_FIK), 0, ['IK', 'Finger-5-IK_R', 3,  None, (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.37,0.5, 0,0, 0,0), (1,0,0)])]
	addPoseBone(fp, 'True', 'Finger-5-3_R', customShape, None, (0,0,0), (0,1,1), (1,1,1), (0,0,1), 0, constraints)

	# Control
	addPoseBone(fp, T_FPanel, 'PHand_L', 'MHCircle05', None, (1,1,1), (1,1,1), (1,1,1), (0,0,0), 0, [])
	addPoseBone(fp, T_FPanel, 'PHand_R', 'MHCircle05', None, (1,1,1), (1,1,1), (1,1,1), (0,0,0), 0, [])
	addPoseBone(fp, T_FPanel, 'DrvHand_L', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), P_XYZ, [])
	addPoseBone(fp, T_FPanel, 'DrvHand_R', None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), P_XYZ, [])
	for fnum in range(1,6):
		addControlFinger(fp, fnum, "_L")
		addControlFinger(fp, fnum, "_R")
	return


def addControlFinger(fp, fnum, suffix):
	addPoseBone(fp, T_FIK, 'Finger-%s%s' % (fnum, suffix), None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])
	addPoseBone(fp, T_FIK, 'Finger-%s-IK%s' % (fnum, suffix), None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, T_FPanel, 'PFinger-%s%s' % (fnum, suffix), 'MHCircle025', None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, T_FPanel, 'DrvFinger-%s%s' % (fnum, suffix), None, None, (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0, [])
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


