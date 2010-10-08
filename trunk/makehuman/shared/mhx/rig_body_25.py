#
#	Body bone definitions
#

import mhx_rig
from mhx_rig import *

BodyJoints = [
	('hips-tail',			'o', ('pelvis', [0,-1.0,0])),
	('mid-uplegs',			'l', ((0.5, 'l-upper-leg'), (0.5, 'r-upper-leg'))),

	('chest-front',			'v', 7292),
	('r-rib-top',			'v', 3667),
	('r-rib-bot',			'v', 3400),
	('r-stomach',			'v', 6568),
	('r-hip',				'v', 6563),

	('l-rib-top',			'v', 10134),
	('l-rib-bot',			'v', 10361),
	('l-hip',				'v', 6749),
	('l-stomach',			'v', 6744),

	('mid-rib-top',			'l', ((0.5, 'r-rib-top'), (0.5, 'l-rib-top'))),
	('mid-rib-bot',			'l', ((0.5, 'r-rib-bot'), (0.5, 'l-rib-bot'))),
	('mid-stomach',			'l', ((0.5, 'r-stomach'), (0.5, 'l-stomach'))),
	('mid-hip',				'l', ((0.5, 'r-hip'), (0.5, 'l-hip'))),

	('abdomen-front',		'v', 7359),
	('abdomen-back',		'v', 7186),
	('stomach-top',			'v', 7336),
	('stomach-bot',			'v', 7297),
	('stomach-front',		'v', 7313),
	('stomach-back',		'v', 7472),

	('r-toe-1-1',			'j', 'r-toe-1-1'),
	('l-toe-1-1',			'j', 'l-toe-1-1'),
	('mid-feet',			'l', ((0.5, 'l-toe-1-1'), (0.5, 'r-toe-1-1'))),
	('floor',				'o', ('mid-feet', [0,-0.3,0])),
]

offs = [0,0.3,0]

BodyHeadsTails = [
	('MasterFloor',			'floor', ('floor', zunit)),
	('MasterHips',			'pelvis', ('pelvis', zunit)),
	('MasterNeck',			'neck', ('neck', zunit)),

	('Root',			'spine3', 'spine4'),
	('Hips',			'pelvis', 'hips-tail'),
	('Hip_L',			'pelvis', 'r-upper-leg'),
	('Hip_R',			'pelvis', 'l-upper-leg'),

	('Spine1',			'spine3', 'spine2'),
	('Spine2',			'spine2', 'spine1'),
	('Spine3',			'spine1', 'neck'),
	('Neck',			'neck', 'head'),
	('Head',			'head', 'head-end'),

	('Rib',				'mid-rib-top', 'mid-rib-bot'),
	('StomachUp',			'mid-rib-bot', 'stomach-front'),
	('StomachLo',			'mid-hip', 'stomach-front'),
	('StomachTarget',	'stomach-front', ('stomach-front', offs)),
]

BodyArmature = [
	('MasterFloor',		0.0, None, F_WIR, L_MAIN, (1,1,1) ),
	('MasterHips',		0.0, None, F_WIR+F_HID, L_MAIN, (1,1,1) ),
	('MasterNeck',		0.0, None, F_WIR+F_HID, L_MAIN, (1,1,1) ),

	('Root',			0.0, None, F_WIR, L_MAIN+L_SPINE, (1,1,1) ),
	('Hips',			0.0, 'Root', F_DEF+F_WIR, L_DEF+L_SPINE, (1,1,1) ),
	('Hip_L',			0.0, 'Hips', 0, L_HELP, (1,1,1) ),
	('Hip_R',			0.0, 'Hips', 0, L_HELP, (1,1,1) ),

	('Spine1',			0.0, 'Root', F_DEF+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Spine2',			0.0, 'Spine1', F_DEF+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Spine3',			0.0, 'Spine2', F_DEF+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Neck',			0.0, 'Spine3', F_DEF+F_WIR, L_SPINE+L_HEAD+L_DEF, (1,1,1) ),
	('Head',			0.0, 'Neck', F_DEF+F_WIR, L_SPINE+L_HEAD+L_DEF, (1,1,1) ),

	('Rib',				0.0, 'Spine3', F_DEF, L_DEF, (1,1,1) ),
	('StomachUp',			0.0, 'Rib', F_DEF, L_DEF, (1,1,1) ),
	('StomachLo',			0.0, 'Hips', F_DEF, L_DEF, (1,1,1) ),
	('StomachTarget',	0, 'Spine1', 0, L_HELP, (1,1,1) ),
]

#
#	BodyWritePoses(fp):
#

def BodyWritePoses(fp):
	addPoseBone(fp,  'MasterFloor', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'MasterHips', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_HID, [])

	addPoseBone(fp,  'MasterNeck', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_HID, [])

	addPoseBone(fp,  'Root', 'MHHips', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, mhx_rig.rootChildOfConstraints)

	addPoseBone(fp,  'Hips', 'MHCircle15', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'Hip_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'Hip_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Spinal column
	addPoseBone(fp,  'Spine1', 'MHCircle10', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, [])

	addPoseBone(fp,  'Spine2', 'MHCircle15', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, [])

	addPoseBone(fp,  'Spine3', 'MHCircle10', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, [])

	addPoseBone(fp,  'Neck', 'GoboNeck', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'Head', 'GoboHead', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Deform

	vec = aljabr.vsub(mhx_rig.locations['stomach-front'], mhx_rig.locations['stomach-back'])
	dist = aljabr.vlen(vec) - 0.5
	if dist < 0: dist = 0.0
	stomachFwdPos = str(0.4*dist) + '*theScale'
	stomachUpPos = str(0.8*dist) + '*theScale'
	stomachFwdNeg = str(-0.2*dist) + '*theScale'
	stomachUpNeg = str(-0.4*dist) + '*theScale'
	print('Stm', stomachFwdPos)

	addPoseBone(fp,  'StomachTarget', None, None, (0,0,0), (0,1,0), (0,0,0), (1,1,1), 0, 
		[('Transform', C_OW_LOCAL+C_TG_LOCAL, 1, ['Transform', 'Spine1',
			'ROTATION', (-45,0,0), (90,0,0), ('X', 'X', 'X'),
			'LOCATION', (0,stomachUpNeg, stomachFwdNeg),(0, stomachUpPos, stomachFwdPos)])
		])

	addPoseBone(fp,  'StomachUp', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget', 'PLANE_X', 0])])

	addPoseBone(fp,  'StomachLo', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget', 'PLANE_X', 0])])

	return


