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
	('r-tit',				'v', 3718),
	('r-stomach',			'v', 6568),
	('r-hip',				'v', 6563),

	('l-rib-top',			'v', 10134),
	('l-rib-bot',			'v', 10361),
	('l-tit',				'v', 10115),
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

BodyHeadsTails = [
	('MasterFloor',			'floor', ('floor', zunit)),
	('MasterHips',			'pelvis', ('pelvis', zunit)),
	('MasterNeck',			'neck', ('neck', zunit)),

	('Root',				'spine3', 'spine4'),
	('Hips',				'pelvis', 'hips-tail'),
	('Hip_L',				'spine3', 'r-upper-leg'),
	('Hip_R',				'spine3', 'l-upper-leg'),
	
	('Spine1',				'spine3', 'spine2'),
	('Spine2',				'spine2', 'spine1'),
	('Spine3',				'spine1', 'neck'),
	('Neck',				'neck', 'head'),
	('Head',				'head', 'head-end'),

	('Rib',					'mid-rib-top', 'mid-rib-bot'),
	('StomachUp',			'mid-rib-bot', 'stomach-front'),
	('StomachLo',			'mid-hip', 'stomach-front'),
	('StomachTarget',		'stomach-front', ('stomach-front', zunit)),
	('Breathe',				'mid-rib-bot', ('mid-rib-bot', zunit)),
	('Breast_L',			'r-tit', ('r-tit', zunit)),
	('Breast_R',			'l-tit', ('l-tit', zunit)),
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

	('Rib',				0.0, 'Spine3', F_DEF+F_WIR, L_DEF, (1,1,1) ),
	('Breast_L',		0.0, 'Rib', F_DEF+F_WIR, L_TORSO+L_DEF, (1,1,1) ),
	('Breast_R',		0.0, 'Rib', F_DEF+F_WIR, L_TORSO+L_DEF, (1,1,1) ),
	('Breathe',			0.0, 'Rib', F_DEF+F_WIR, L_TORSO, (1,1,1) ),
	('StomachUp',		0.0, 'Rib', F_DEF, L_DEF, (1,1,1) ),
	('StomachLo',		0.0, 'Hips', F_DEF, L_DEF, (1,1,1) ),
	('StomachTarget',	0, 'Spine1', F_WIR, L_TORSO, (1,1,1) ),
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
	addPoseBone(fp,  'Spine1', 'MHCircle10', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-deg20,deg90, -deg60,deg60, -deg60,deg60), (1,1,1)])])

	addPoseBone(fp,  'Spine2', 'MHCircle15', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-deg20,deg30, -deg45,deg45, -deg30,deg30), (1,1,1)])])

	addPoseBone(fp,  'Spine3', 'MHCircle10', None, (1,1,1), (0,0,0), (1,1,1), (1,0,1), P_STRETCH,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-deg20,deg20, -deg20,deg20, -deg20,deg20), (1,1,1)])])

	addPoseBone(fp,  'Neck', 'GoboNeck', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-deg60,deg30, -deg45,deg45, -deg60,deg60), (1,1,1)])])

	addPoseBone(fp,  'Head', 'GoboHead', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-deg60,deg30, -deg60,deg60, -deg45,deg45), (1,1,1)])])

	# Stomach
	addPoseBone(fp,  'StomachTarget', 'MHCube01', None, (0,0,0), (1,1,1), (0,0,0), (1,1,1), 0, 
		[('LimitDist', 0, 1, ['LimitDist', 1, 'Rib'])])

	addPoseBone(fp,  'StomachLo', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget', 'PLANE_X', 0]),
		 ('CopyScale', C_OW_LOCAL+C_TG_LOCAL, 1, ['CopyScale', 'StomachTarget', (1,0,1), False]),
		])

	addPoseBone(fp,  'StomachUp', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget', 'PLANE_X', 0]),
		 ('CopyScale', C_OW_LOCAL+C_TG_LOCAL, 1, ['CopyScale', 'StomachTarget', (1,0,1), False]),
		])

	addPoseBone(fp,  'Breathe', 'MHCube01', None, (1,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'Breast_L', 'MHCube01', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'Breast_R', 'MHCube01', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])
	return

#
#	BodyShapeDrivers
#	Shape : (driver, channel, coeff)
#

BodyShapeDrivers = {
	'BreatheIn' : ('Breathe', 'LOC_Z', ('0', '2.0')), 
}

#
#	BodyShapeKeyScale = {
#

BodyShapeKeyScale = {
	'BendElbowForward' 	: ('r-shoulder', 'r-hand', 4.705061),
	'BendKneeBack'		: ('r-upper-leg', 'r-ankle', 8.207247),
	'BendArmDown'		: ('r-shoulder', 'l-shoulder', 3.388347),
	'BendArmUp'			: ('r-shoulder', 'l-shoulder', 3.388347),
	'BendLegForward'	: ('r-upper-leg', 'r-knee', 4.164895),
	'BendLegBack'		: ('r-upper-leg', 'r-knee', 4.164895),
	'BendLegOut'		: ('r-upper-leg', 'r-knee', 4.164895),
	'BreatheIn'			: ('spine1', 'neck', 1.89623),
}


