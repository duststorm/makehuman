#
#	Face bone definitions
#

import mhx_rig
from mhx_rig import *

FaceJoints = [
	('head-end',			'l', ((2.0, 'head'), (-1.0, 'neck'))),
	('r-mouth',			'v', 2490),
	('l-mouth',			'v', 8907),

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
	('Jaw',			0.0, 'Head', F_DEF+F_WIR, L_HEAD+L_DEF, (1,1,1) ),
	('TongueBase',	0.0, 'Jaw', F_DEF+F_WIR, L_HEAD+L_DEF, (1,1,1) ),
	('TongueMid',	0.0, 'TongueBase', F_DEF+F_WIR, L_HEAD+L_DEF, (1,1,1) ),
	('TongueTip',	0.0, 'TongueMid', F_DEF+F_WIR, L_HEAD+L_DEF, (1,1,1) ),
	('Eye_R',		0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('Eye_L',		0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('UpLid_R',		0.279253, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('LoLid_R',		0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('UpLid_L',		-0.279253, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('LoLid_L',		0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('Gaze',		pi, 'Head', F_WIR, L_HEAD, (1,1,1) ),
	('Gaze_R',		pi, 'Gaze', F_WIR, L_HEAD, (1,1,1) ),
	('Gaze_L',		pi, 'Gaze', F_WIR, L_HEAD, (1,1,1) ),
]

#
#	FaceWritePoses(fp):
#

def FaceWritePoses(fp):
	addPoseBone(fp, 'Jaw', 'MHJaw', None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-5*deg1,deg45, 0,0, -deg20,deg20), (1,1,1)])])

	addPoseBone(fp, 'TongueBase', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'TongueMid', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'TongueTip', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'UpLid_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoLid_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'UpLid_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoLid_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Gaze', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
		#[('ChildOf', C_CHILDOF, 1, ['ChildOf', 'Head', (1,1,1), (1,1,1), (1,1,1)])])

	addPoseBone(fp, 'Gaze_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Eye_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, 1, ['IK', 'Gaze_R', 1, None, (True, False,False), 1.0])])

	addPoseBone(fp, 'Gaze_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Eye_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, 1, ['IK', 'Gaze_L', 1, None, (True, False,False), 1.0])])
	return

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
		 [("var", 'TRANSFORMS', [('Human', driver, 'LOC_Z', C_LOC)])]) )
	writeDrivers(fp, True, drivers)
	return


