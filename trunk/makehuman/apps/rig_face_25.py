#
#	Face bone definitions
#

import mhx_rig
from mhx_rig import *

FaceJoints = [
	('head-end',			'l', ((2.0, 'head'), (-1.0, 'neck'))),
	('mouth',			'j', 'mouth'),
	('jaw',				'j', 'jaw'),

	('tongue-1',			'j', 'tongue-1'),
	('tongue-2',			'j', 'tongue-2'),
	('tongue-3',			'j', 'tongue-3'),
	('tongue-4',			'j', 'tongue-4'),

	('l-eye',			'j', 'l-eye'),
	('r-eye',			'j', 'r-eye'),
	('l-eye-target',		'j', 'l-eye-target'),
	('r-eye-target',		'j', 'r-eye-target'),
	('l-upperlid',			'j', 'l-upperlid'),
	('l-lowerlid',			'j', 'l-lowerlid'),
	('r-upperlid',			'j', 'r-upperlid'),
	('r-lowerlid',			'j', 'r-lowerlid'),

	('mid-eyes',			'l', ((0.5, 'l-eye'), (0.5, 'r-eye'))),
	('gaze',			'o', ('mid-eyes', [0.0, 0.0, 5.2])),
	('gaze-target',			'o', ('mid-eyes', [0.0, 0.0, 4.2])),
	('l-gaze',			'o', ('l-eye', [0.0, 0.0, 5.0])),
	('l-gaze-target',		'o', ('l-eye', [0.0, 0.0, 4.5])),
	('r-gaze',			'o', ('r-eye', [0.0, 0.0, 5.0])),
	('r-gaze-target',		'o', ('r-eye', [0.0, 0.0, 4.5])),
]

FaceHeadsTails = [
	('Jaw',				'mouth', 'jaw'),
	('TongueBase',			'tongue-1', 'tongue-2'),
	('TongueMid',			'tongue-2', 'tongue-3'),
	('TongueTip',			'tongue-3', 'tongue-4'),

	('Eye_R',			'l-eye', 'l-eye-target'),
	('UpLid_R',			'l-eye', 'l-upperlid'),
	('LoLid_R',			'l-eye', 'l-lowerlid'),
	('Eye_L',			'r-eye', 'r-eye-target'),
	('UpLid_L',			'r-eye', 'r-upperlid'),
	('LoLid_L',			'r-eye', 'r-lowerlid'),

	('Gaze',			'gaze', 'gaze-target'),
	('Gaze_R',			'l-gaze', 'l-gaze-target'),
	('Gaze_L',			'r-gaze', 'r-gaze-target'),
]


FaceArmature = [
	('Jaw', 'True',			0.0, 'Head', F_DEF+F_WIR, L_MAIN+L_HEAD+L_DEF, (1,1,1) ),
	('TongueBase', 'True',		0.0, 'Jaw', F_DEF+F_WIR, L_HEAD+L_DEF, (1,1,1) ),
	('TongueMid', 'True',		0.0, 'TongueBase', F_DEF+F_CON+F_WIR, L_HEAD+L_DEF, (1,1,1) ),
	('TongueTip', 'True',		0.0, 'TongueMid', F_DEF+F_CON+F_WIR, L_HEAD+L_DEF, (1,1,1) ),
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

	('poseBone', 'True', 'TongueBase', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, []),

	('poseBone', 'True', 'TongueMid', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, []),

	('poseBone', 'True', 'TongueTip', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, []),

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


