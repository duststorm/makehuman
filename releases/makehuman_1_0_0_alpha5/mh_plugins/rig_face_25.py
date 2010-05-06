#
#	Face bone definitions
#

import mhx_rig
from mhx_rig import *

FaceJoints = [
	('mouth',			'j', 'mouth'),
	('l-eye',			'j', 'l-eye'),
	('r-eye',			'j', 'r-eye'),
	('jaw-tip',			'v', 8162),
	('tounge-tip',			'v', 8049),
	('tounge-mid',			'v', 8103),
	('tounge-root',			'v', 8099),
	('l-upLid-v',			'v', 12630),
	('l-loLid-v',			'v', 12594),
	('r-upLid-v',			'v', 2442),
	('r-loLid-v',			'v', 2520),
	('l-upLid',			'l', ((2.5, 'l-upLid-v'), (-1.5, 'l-eye'))),
	('l-loLid',			'l', ((2.5, 'l-loLid-v'), (-1.5, 'l-eye'))),
	('r-upLid',			'l', ((2.5, 'r-upLid-v'), (-1.5, 'r-eye'))),
	('r-loLid',			'l', ((2.5, 'r-loLid-v'), (-1.5, 'r-eye'))),
	('head-end',			'l', ((2.0, 'head'), (-1.0, 'neck'))),

	('mouth-end',			'l', ((3.0, 'mouth'), (-2.0, 'head'))),
	('Eye_R_tail',			'o', ('l-eye', [0.0, 0.0, 0.5])),
	('Eye_L_tail',			'o', ('r-eye', [0.0, 0.0, 0.5])),
	('mid-eyes',			'l', ((0.5, 'l-eye'), (0.5, 'r-eye'))),
	('Gaze_head',			'o', ('mid-eyes', [0.0, 0.0, 5.2])),
	('Gaze_tail',			'o', ('mid-eyes', [0.0, 0.0, 4.2])),
	('Gaze_R_head',			'o', ('l-eye', [0.0, 0.0, 5.0])),
	('Gaze_R_tail',			'o', ('l-eye', [0.0, 0.0, 4.5])),
	('Gaze_L_head',			'o', ('r-eye', [0.0, 0.0, 5.0])),
	('Gaze_L_tail',			'o', ('r-eye', [0.0, 0.0, 4.5])),
]

FaceHeadsTails = [
	#('Head-inv',			'head-end', 'mouth'),
	('Jaw',				'mouth', 'jaw-tip'),
	('ToungeBase',			'tounge-root', 'tounge-mid'),
	('ToungeTip',			'tounge-mid', 'tounge-tip'),
	('Eye_R',			'l-eye', 'Eye_R_tail'),
	('UpLid_R',			'l-eye', 'l-upLid'),
	('LoLid_R',			'l-eye', 'l-loLid'),
	('Eye_L',			'r-eye', 'Eye_L_tail'),
	('UpLid_L',			'r-eye', 'r-upLid'),
	('LoLid_L',			'r-eye', 'r-loLid'),
	('Gaze',			'Gaze_head', 'Gaze_tail'),
	('Gaze_R',			'Gaze_R_head', 'Gaze_R_tail'),
	('Gaze_L',			'Gaze_L_head', 'Gaze_L_tail'),
]


FaceArmature = [
	('Jaw', 'True',			0.0, 'Head', F_DEF+F_WIR, L_MAIN+L_HEAD+L_DEF, (1,1,1) ),
	('ToungeBase', 'True',		0.0, 'Jaw', F_DEF+F_WIR, L_HEAD+L_DEF, (1,1,1) ),
	('ToungeTip', 'True',		0.0, 'ToungeBase', F_DEF+F_CON+F_WIR, L_HEAD+L_DEF, (1,1,1) ),
	('Eye_R', 'True',		0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('Eye_L', 'True',		0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('UpLid_R', 'True',		0.279253, 'Head', F_DEF, L_DEF+L_HEAD, (1,1,1) ),
	('LoLid_R', 'True',		0.296705, 'Head', F_DEF, L_DEF+L_HEAD, (1,1,1) ),
	('UpLid_L', 'True',		-0.279253, 'Head', F_DEF, L_DEF+L_HEAD, (1,1,1) ),
	('LoLid_L', 'True',		-0.296705, 'Head', F_DEF, L_DEF+L_HEAD, (1,1,1) ),
	('Gaze', 'True',		-3.14159, 'Root', F_WIR, L_HEAD, (1,1,1) ),
	('Gaze_R', 'True',		-3.14159, 'Gaze', F_WIR, L_HEAD, (1,1,1) ),
	('Gaze_L', 'True',		-3.14159, 'Gaze', F_WIR, L_HEAD, (1,1,1) ),
]

#
#	FaceWritePoses(fp):
#

def FaceWritePoses(fp):
	addPoseBone(fp, 'True', 'Jaw', 'MHJaw', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'ToungeBase', 'MHCircle025', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'ToungeTip', 'MHCircle025', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'UpLid_R', 'MHCircle01', None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'LoLid_R', 'MHCircle01', None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'UpLid_L', 'MHCircle01', None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'LoLid_L', 'MHCircle01', None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Gaze', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Gaze_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Eye_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Gaze_R', 1, None, (True, False), 1.0])])

	addPoseBone(fp, 'True', 'Gaze_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Eye_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Gaze_L', 1, None, (True, False), 1.0])])

	return

