#
#	Body bone definitions
#

import mhx_rig
from mhx_rig import *

BodyJoints = [
	('pelvis',			'j', 'pelvis'),
	('spine3',			'j', 'spine3'),
	('spine2',			'j', 'spine2'),
	('spine1',			'j', 'spine1'),
	('neck',			'j', 'neck'),
	('head',			'j', 'head'),

	('root-head',			'o', ('pelvis', [0,-1.5,0])),

	('chest-front',			'v', 7292),
	('l-rib-top',			'v', 10134),
	('r-rib-top',			'v', 3667),
	('l-rib-bot',			'v', 10361),
	('r-rib-bot',			'v', 3400),
	('l-hip',			'v', 6754),
	('r-hip',			'v', 6558),
	('abdomen-front',		'v', 7359),
	('abdomen-back',		'v', 7186),

	('r-toe-1-1',			'j', 'r-toe-1-1'),
	('l-toe-1-1',			'j', 'l-toe-1-1'),
	('mid-feet',			'l', ((0.5, 'l-toe-1-1'), (0.5, 'r-toe-1-1'))),
	('floor',			'o', ('mid-feet', [0,-0.3,0])),
]


BodyHeadsTails = [

	('MasterFloor',			'floor', ('floor', zunit)),
	('MasterHips',			'pelvis', ('pelvis', zunit)),
	('MasterNeck',			'neck', ('neck', zunit)),

	('Root',			'root-head', 'spine3'),
	('Hips',			'spine3', 'root-head'),
	('HipsInv',			'root-head', 'spine3'),

	('Spine1',			'spine3', 'spine2'),
	('Spine2',			'spine2', 'spine1'),
	('Spine3',			'spine1', 'neck'),
	('Neck',			'neck', 'head'),
	('Head',			'head', 'head-end'),

	('Rib_L',			'r-rib-top', 'r-rib-bot'),
	('Stomach_L',			'r-rib-bot', 'r-upper-leg'),
	('Rib_R',			'l-rib-top', 'l-rib-bot'),
	('Stomach_R',			'l-rib-bot', 'l-upper-leg'),
	('Abdomen',			'abdomen-front', 'abdomen-back'),

	('Hip_L',			'root-head', 'r-upper-leg'),
	('Hip_R',			'root-head', 'l-upper-leg'),
]

BodyArmature = [
	('MasterFloor', 'True',		0.0, None, F_WIR, L_MAIN, (1,1,1) ),
	('MasterHips', 'True',		0.0, None, F_WIR+F_HID, L_HELP, (1,1,1) ),
	('MasterNeck', 'True',		0.0, None, F_WIR+F_HID, L_HELP, (1,1,1) ),

	('Root', 'True',		0.0, None, F_WIR, L_MAIN, (1,1,1) ),
	('Hips', 'True',		pi, 'Root', F_DEF+F_WIR, L_SPINE+L_DEF, (1,1,1) ),
	('HipsInv', 'True',		0.0, 'Hips', F_CON, L_HELP, (1,1,1) ),

	('Spine1', 'True',		0.0, 'HipsInv', F_DEF+F_CON+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Spine2', 'True',		0.0, 'Spine1', F_DEF+F_CON+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Spine3', 'True',		0.0, 'Spine2', F_DEF+F_CON+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Neck', 'True',		0.0, 'Spine3', F_DEF+F_CON+F_WIR, L_SPINE+L_HEAD+L_DEF, (1,1,1) ),
	('Head', 'True',		0.0, 'Neck', F_DEF+F_CON+F_WIR, L_SPINE+L_HEAD+L_DEF, (1,1,1) ),

	('Rib_L', 'True',		0.0, 'Spine3', F_DEF, L_DEF, (1,1,1) ),
	('Rib_R', 'True',		0.0, 'Spine3', F_DEF, L_DEF, (1,1,1) ),
	('Stomach_L', 'True',		0.0, 'Rib_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Stomach_R', 'True',		0.0, 'Rib_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	
	('Hip_L', 'True',		0.0, 'Hips', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Hip_R', 'True',		0.0, 'Hips', F_DEF+F_CON, L_DEF, (1,1,1) ),
]

BodyPoses = [
	('poseBone', 'True', 'MasterFloor', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'MasterHips', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'MasterNeck', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'Root', 'MHCube025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['Floor', 'MasterFloor', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Hips', 'MasterHips', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Neck', 'MasterNeck', 0.0, (1,1,1), (1,1,1), (1,1,1)])]),

	('poseBone', 'True', 'Hips', 'MHHips', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'Hip_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'Hip_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, []),

	# Spinal column
	#('poseBone', 'True', 'Pelvis', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'Spine1', 'MHCircle10', None, (0,0,0), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, []),

	('poseBone', 'True', 'Spine2', 'MHCircle15', None, (0,0,0), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, []),

	('poseBone', 'True', 'Spine3', 'MHCircle10', None, (0,0,0), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, []),

	('poseBone', 'True', 'Neck', 'GoboNeck', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'True', 'Head', 'GoboHead', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	# Deform

	('poseBone', 'True', 'Stomach_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['UpLeg_L', 'UpLeg_L', 'PLANE_X'])]),

	('poseBone', 'True', 'Stomach_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['UpLeg_R', 'UpLeg_R', 'PLANE_X'])]),
]

