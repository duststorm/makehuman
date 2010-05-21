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
	('tounge-midfront',		'v', 8089),
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
	('ToungeMid',			'tounge-mid', 'tounge-midfront'),
	('ToungeTip',			'tounge-midfront', 'tounge-tip'),
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
	('ToungeMid', 'True',		0.0, 'ToungeBase', F_DEF+F_CON+F_WIR, L_HEAD+L_DEF, (1,1,1) ),
	('ToungeTip', 'True',		0.0, 'ToungeMid', F_DEF+F_CON+F_WIR, L_HEAD+L_DEF, (1,1,1) ),
	('Eye_R', 'True',		0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('Eye_L', 'True',		0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('UpLid_R', 'True',		0.279253, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('LoLid_R', 'True',		0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('UpLid_L', 'True',		-0.279253, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('LoLid_L', 'True',		0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('Gaze', 'True',		pi, 'Root', F_WIR, L_HEAD, (1,1,1) ),
	('Gaze_R', 'True',		pi, 'Gaze', F_WIR, L_HEAD, (1,1,1) ),
	('Gaze_L', 'True',		pi, 'Gaze', F_WIR, L_HEAD, (1,1,1) ),
]

#
#	FaceWritePoses(fp):
#

FacePoses = [
	('poseBone', 'True', 'Jaw', 'MHJaw', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'ToungeBase', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, []),

	('poseBone', 'True', 'ToungeMid', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, []),

	('poseBone', 'True', 'ToungeTip', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, []),

	('poseBone', 'True', 'UpLid_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'LoLid_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'UpLid_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'LoLid_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'Gaze', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'Gaze_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'Eye_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Gaze_R', 1, None, (True, False,False), 1.0])]),

	('poseBone', 'True', 'Gaze_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'Eye_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Gaze_L', 1, None, (True, False,False), 1.0])]),
]

lidBones = [
	('UpLid_L', 'PUpLid_L', (0, 40*deg1)),
	('LoLid_L', 'PLoLid_L', (0, 20*deg1)),
	('UpLid_R', 'PUpLid_R', (0, 40*deg1)),
	('LoLid_R', 'PLoLid_R', (0, 20*deg1)),
]

def FaceWriteDrivers(fp):
	drivers = []
	for (driven, driver, coeff) in lidBones:
		drivers.append(	(driven, 'ROTQ', None, 1, coeff,
		 [("var", 'TRANSFORMS', [('HumanRig', driver, 'LOC_Z', C_LOCAL)])]) )
	writeDrivers(fp, T_Panel, drivers)
	return


