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
	('r-breast1',			'v', 3559),
	('r-breast2',			'v', 2944),
	('r-breast',			'l', ((0.4, 'r-breast1'), (0.6, 'r-breast2'))),
	('r-tit',				'v', 3718),
	('r-stomach',			'v', 6568),
	('r-hip',				'v', 6563),

	('l-rib-top',			'v', 10134),
	('l-rib-bot',			'v', 10361),
	('l-breast1',			'v', 10233),
	('l-breast2',			'v', 10776),
	('l-breast',			'l', ((0.4, 'l-breast1'), (0.6, 'l-breast2'))),
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

	('penis-tip',			'v', 7415),
	('r-penis',				'v', 2792),
	('l-penis',				'v', 7448),
	('penis-root',			'l', ((0.5, 'r-penis'), (0.5, 'l-penis'))),
	('scrotum-tip',			'v', 7444),
	('r-scrotum',			'v', 2807),
	('l-scrotum',			'v', 7425),
	('scrotum-root',		'l', ((0.5, 'r-scrotum'), (0.5, 'l-scrotum'))),

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
	('Breast_L',			'r-breast', 'r-tit'),
	('Breast_R',			'l-breast', 'l-tit'),

	('Penis',				'penis-root', 'penis-tip'),
	('Scrotum',				'scrotum-root', 'scrotum-tip'),
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
	('Breast_L',		-deg45, 'Rib', F_DEF, L_TORSO+L_DEF, (1,1,1) ),
	('Breast_R',		deg45, 'Rib', F_DEF, L_TORSO+L_DEF, (1,1,1) ),
	('Breathe',			0.0, 'Rib', F_DEF+F_WIR, L_TORSO, (1,1,1) ),
	('StomachUp',		0.0, 'Rib', F_DEF, L_DEF, (1,1,1) ),
	('StomachLo',		0.0, 'Hips', F_DEF, L_DEF, (1,1,1) ),
	('StomachTarget',	0, 'Spine1', F_WIR, L_TORSO, (1,1,1) ),

	('Penis',			0.0, 'Hips', F_DEF, L_DEF+L_TORSO, (1,5,1) ),
	('Scrotum',			0.0, 'Hips', F_DEF, L_DEF+L_TORSO, (1,1,1) ),
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
		[('LimitDist', 0, 1, ['LimitDist', 'Spine1', 'Rib'])])

	addPoseBone(fp,  'StomachLo', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget', 0]),
		 ('CopyScale', C_OW_LOCAL+C_TG_LOCAL, 1, ['CopyScale', 'StomachTarget', (1,0,1), False]),
		])

	addPoseBone(fp,  'StomachUp', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget', 0]),
		 ('CopyScale', C_OW_LOCAL+C_TG_LOCAL, 1, ['CopyScale', 'StomachTarget', (1,0,1), False]),
		])

	addPoseBone(fp,  'Breathe', 'MHCube01', None, (1,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	limBreastRot = (-deg45,deg45, -10*deg1,10*deg1, -deg20,deg20)
	limBreastScale =  (0.8,1.25, 0.7,1.5, 0.8,1.25)

	addPoseBone(fp,  'Breast_L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, 
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
		 ('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])	])

	addPoseBone(fp,  'Breast_R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
		 ('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])	])

	addPoseBone(fp,  'Penis', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

	addPoseBone(fp,  'Scrotum', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

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
	'BreatheIn'			: ('spine1', 'neck', 1.89623),
	'BicepFlex'			: ('r-uparm-front', 'r-uparm-back', 0.93219),
}


