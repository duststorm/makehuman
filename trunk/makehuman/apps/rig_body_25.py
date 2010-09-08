#
#	Body bone definitions
#

import mhx_rig
from mhx_rig import *

BodyJoints = [
	('hips-tail',			'o', ('pelvis', [0,-1.0,0])),
	('mid-uplegs',			'l', ((0.5, 'l-upper-leg'), (0.5, 'r-upper-leg'))),

	('chest-front',			'v', 7292),
	('l-rib-top',			'v', 10134),
	('r-rib-top',			'v', 3667),
	('l-rib-bot',			'v', 10361),
	('r-rib-bot',			'v', 3400),
	('l-hip',				'v', 6754),
	('r-hip',				'v', 6558),
	('abdomen-front',		'v', 7359),
	('abdomen-back',		'v', 7186),

	('r-toe-1-1',			'j', 'r-toe-1-1'),
	('l-toe-1-1',			'j', 'l-toe-1-1'),
	('mid-feet',			'l', ((0.5, 'l-toe-1-1'), (0.5, 'r-toe-1-1'))),
	('floor',				'o', ('mid-feet', [0,-0.3,0])),
]


BodyHeadsTails = [

	('MasterFloor',			'floor', ('floor', zunit)),
	('MasterHips',			'pelvis', ('pelvis', zunit)),
	('MasterNeck',			'neck', ('neck', zunit)),

	('Root',			'spine3', 'spine4'),
	('Hips',			'pelvis', 'hips-tail'),

	('Spine1',			'spine3', 'spine2'),
	('Spine2',			'spine2', 'spine1'),
	('Spine3',			'spine1', 'neck'),
	('Neck',			'neck', 'head'),
	('Head',			'head', 'head-end'),

	('Rib_L',			'r-rib-top', 'r-rib-bot'),
	('Stomach_L',		'r-rib-bot', 'r-upper-leg'),
	('Rib_R',			'l-rib-top', 'l-rib-bot'),
	('Stomach_R',		'l-rib-bot', 'l-upper-leg'),
	('Abdomen',			'abdomen-front', 'abdomen-back'),
]

BodyArmature = [
	('MasterFloor',		0.0, None, F_WIR, L_MAIN, (1,1,1) ),
	('MasterHips',		0.0, None, F_WIR+F_HID, L_HELP, (1,1,1) ),
	('MasterNeck',		0.0, None, F_WIR+F_HID, L_HELP, (1,1,1) ),

	('Root',			0.0, None, F_WIR, L_MAIN+L_SPINE, (1,1,1) ),
	('Hips',			0.0, 'Root', F_DEF+F_WIR, L_DEF, (1,1,1) ),

	('Spine1',			0.0, 'Root', F_DEF+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Spine2',			0.0, 'Spine1', F_DEF+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Spine3',			0.0, 'Spine2', F_DEF+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Neck',			0.0, 'Spine3', F_DEF+F_WIR, L_SPINE+L_HEAD+L_DEF, (1,1,1) ),
	('Head',			0.0, 'Neck', F_DEF+F_WIR, L_SPINE+L_HEAD+L_DEF, (1,1,1) ),

	('Rib_L',			0.0, 'Spine3', F_DEF, L_DEF, (1,1,1) ),
	('Rib_R',			0.0, 'Spine3', F_DEF, L_DEF, (1,1,1) ),
	('Stomach_L',		0.0, 'Rib_L', F_DEF, L_DEF, (1,1,1) ),
	('Stomach_R',		0.0, 'Rib_R', F_DEF, L_DEF, (1,1,1) ),
]

BodyPoses = [
	('poseBone', 'MasterFloor', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'MasterHips', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'MasterNeck', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'Root', 'MHCube05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['Floor', 'MasterFloor', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Hips', 'MasterHips', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Neck', 'MasterNeck', 0.0, (1,1,1), (1,1,1), (1,1,1)])]),

	('poseBone', 'Hips', 'MHHips', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, []),

	# Spinal column
	('poseBone', 'Spine1', 'MHCircle10', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, []),

	('poseBone', 'Spine2', 'MHCircle15', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, []),

	('poseBone', 'Spine3', 'MHCircle10', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, []),

	('poseBone', 'Neck', 'GoboNeck', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'Head', 'GoboHead', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, []),

	# Deform
	('poseBone', 'Stomach_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['UpLeg_L', 'UpLeg_L', 'PLANE_X'])]),

	('poseBone', 'Stomach_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['UpLeg_R', 'UpLeg_R', 'PLANE_X'])]),
]

