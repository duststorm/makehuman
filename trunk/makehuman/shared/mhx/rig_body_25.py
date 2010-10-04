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
	('r-hip',				'v', 6563),
	('r-buttock-top',		'v', 4473),
	('r-buttock-bot',		'v', 4476),

	('l-rib-top',			'v', 10134),
	('l-rib-bot',			'v', 10361),
	('l-hip',				'v', 6749),
	('l-buttock-top',		'v', 6892),
	('l-buttock-bot',		'v', 6889),

	('abdomen-front',		'v', 7359),
	('abdomen-back',		'v', 7186),
	('stomach-top',			'v', 7336),
	('stomach-bot',			'v', 7297),

	('r-toe-1-1',			'j', 'r-toe-1-1'),
	('l-toe-1-1',			'j', 'l-toe-1-1'),
	('mid-feet',			'l', ((0.5, 'l-toe-1-1'), (0.5, 'r-toe-1-1'))),
	('floor',				'o', ('mid-feet', [0,-0.3,0])),
]

offs = [0,0.1,0]

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

	('Rib_L',			'r-rib-top', 'r-rib-bot'),
	('Stomach_L',		'r-rib-bot', 'r-hip'),
	('StomachTarget_L',	'r-hip', ('r-hip', offs)),
	('Buttock_L',		'r-buttock-top', 'r-buttock-bot'),
	
	('Rib_R',			'l-rib-top', 'l-rib-bot'),
	('Stomach_R',		'l-rib-bot', 'l-hip'),
	('StomachTarget_R',	'l-hip', ('l-hip', offs)),
	('Buttock_R',		'l-buttock-top', 'l-buttock-bot'),

	('Abdomen',			'abdomen-front', 'abdomen-back'),
	('Stomach',			'stomach-bot', 'stomach-top'),
]

BodyArmature = [
	('MasterFloor',		0.0, None, F_WIR, L_MAIN, (1,1,1) ),
	('MasterHips',		0.0, None, F_WIR+F_HID, L_HELP, (1,1,1) ),
	('MasterNeck',		0.0, None, F_WIR+F_HID, L_HELP, (1,1,1) ),

	('Root',			0.0, None, F_WIR, L_MAIN+L_SPINE, (1,1,1) ),
	('Hips',			0.0, 'Root', F_DEF+F_WIR, L_DEF+L_SPINE, (1,1,1) ),
	('Hip_L',			0.0, 'Hips', 0, L_HELP, (1,1,1) ),
	('Hip_R',			0.0, 'Hips', 0, L_HELP, (1,1,1) ),

	('Spine1',			0.0, 'Root', F_DEF+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Spine2',			0.0, 'Spine1', F_DEF+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Spine3',			0.0, 'Spine2', F_DEF+F_WIR, L_SPINE+L_DEF, (1,1,5) ),
	('Neck',			0.0, 'Spine3', F_DEF+F_WIR, L_SPINE+L_HEAD+L_DEF, (1,1,1) ),
	('Head',			0.0, 'Neck', F_DEF+F_WIR, L_SPINE+L_HEAD+L_DEF, (1,1,1) ),

	('Rib_L',			0.0, 'Spine3', F_DEF, L_DEF, (1,1,1) ),
	('Rib_R',			0.0, 'Spine3', F_DEF, L_DEF, (1,1,1) ),
	('Stomach_L',		0.0, 'Rib_L', F_DEF, L_DEF, (1,1,1) ),
	('Stomach_R',		0.0, 'Rib_R', F_DEF, L_DEF, (1,1,1) ),
	('StomachTarget_L',	0.0, 'Hips', 0, L_HELP, (1,1,1) ),
	('StomachTarget_R',	0.0, 'Hips', 0, L_HELP, (1,1,1) ),
	#('Buttock_L',		0.0, 'Hips', F_DEF, L_DEF, (1,1,1) ),
	#('Buttock_R',		0.0, 'Hips', F_DEF, L_DEF, (1,1,1) ),
	
	('Stomach',			0.0, 'Hips', F_DEF, L_DEF, (1,1,1) ),	
]

BodyPoses = [
	('poseBone', 'MasterFloor', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'MasterHips', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'MasterNeck', 'MHMaster', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'Root', 'MHHips', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, mhx_rig.rootChildOfConstraints),

	('poseBone', 'Hips', 'MHCircle15', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'Hip_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'Hip_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, []),

	# Spinal column
	('poseBone', 'Spine1', 'MHCircle10', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, []),

	('poseBone', 'Spine2', 'MHCircle15', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, []),

	('poseBone', 'Spine3', 'MHCircle10', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH, []),

	('poseBone', 'Neck', 'GoboNeck', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'Head', 'GoboHead', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, []),

	# Deform
	('poseBone', 'Rib_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'Rib_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'Stomach_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget_L', 'PLANE_X'])]),

	('poseBone', 'Stomach_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget_R', 'PLANE_X'])]),

	('poseBone', 'Stomach', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('Transform', C_OW_LOCAL+C_TG_LOCAL, 1, ['Transform', 'Spine1',
			'ROTATION', (-20,0,-45), (50,0,45),
			'ROTATION', (-20,0,-45), (50,0,45)])]),
]

