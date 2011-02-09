#
#	Body bone definitions 
#

import mhx_rig, mhx_spine
from mhx_rig import *
from mhx_spine import spineDeform

BodyJoints = [
	('root-tail',			'o', ('spine3', [0,-1,0])),
	('hips-tail',			'o', ('pelvis', [0,-1,0])),
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

	('Root',				'root-tail', 'spine3'),
	('BendRoot',			'spine3', ('spine3', yunit)),
	('Hips',				'pelvis', 'hips-tail'),
	('Hip_L',				'spine3', 'r-upper-leg'),
	('Hip_R',				'spine3', 'l-upper-leg'),

	('Spine1',				'spine3', 'spine2'),
	('Spine2',				'spine2', 'spine1'),
	('Spine3',				'spine1', 'neck'),
	('Shoulders',			'neck', ('neck', [0,0.5,0])),

	('Spine1IK',			'spine3', ('spine3', [0,0.5,0])),
	('Spine2IK',			'spine2', ('spine2', [0,0.5,0])),
	('Spine3IK',			'spine1', ('spine1', [0,0.5,0])),

	('Neck',				'neck', 'head'),
	('Head',				'head', 'head-end'),

	('Spine1Def',			'spine3', 'spine2'),
	('Spine2Def',			'spine2', 'spine1'),
	('Spine3Def',			'spine1', 'neck'),

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

BodyControlArmature = [
	('MasterFloor',		0.0, None, F_WIR, L_MAIN, NoBB),
	('MasterHips',		0.0, None, F_WIR+F_HID, L_MAIN, NoBB),
	('MasterNeck',		0.0, None, F_WIR+F_HID, L_MAIN, NoBB),

	('Root',			0.0, Master, F_WIR, L_MAIN+L_SPINEFK, NoBB),
	('BendRoot',		0.0, 'Root', 0, L_HELP, NoBB),
	('Hips',			0.0, 'Root', F_WIR, L_SPINEFK, NoBB),
	#('Hip_L',			0.0, 'Hips', 0, L_HELP, NoBB),
	#('Hip_R',			0.0, 'Hips', 0, L_HELP, NoBB),

	('Spine1',			0.0, 'Root', F_WIR, L_SPINEFK, NoBB),
	('Spine2',			0.0, 'Spine1', F_WIR, L_SPINEFK, NoBB),
	('Spine3',			0.0, 'Spine2', F_WIR, L_SPINEFK, NoBB),

	('Spine1IK',		0.0, 'Root', F_WIR, L_SPINEIK, NoBB),
	('Spine2IK',		0.0, 'Spine1', F_WIR+F_NOLOC, L_SPINEIK, NoBB),
	('Spine3IK',		0.0, 'Spine2', F_WIR+F_NOLOC, L_SPINEIK, NoBB),
	('Shoulders',		0.0, 'Spine3', F_WIR, L_SPINEIK, NoBB),

	('Neck',			0.0, 'Shoulders', F_WIR, L_SPINEFK+L_HEAD, NoBB),
	('Head',			0.0, 'Neck', F_WIR, L_SPINEFK+L_HEAD, NoBB),

	('Rib',				0.0, 'Shoulders', F_DEF, L_DEF, NoBB),
	('Breast_L',		-45*D, 'Rib', 0, L_TORSO, NoBB),
	('Breast_R',		45*D, 'Rib', 0, L_TORSO, NoBB),
	('Breathe',			0.0, 'Rib', F_WIR, L_TORSO, NoBB),
	('StomachTarget',	0, 'Spine1', F_WIR, L_TORSO, NoBB),

	('Penis',			0.0, 'Hips', 0, L_TORSO, (1,5,1) ),
	('Scrotum',			0.0, 'Hips', 0, L_TORSO, NoBB),
]

BodyDeformArmature = [
	('Root',			0.0, None, F_WIR, L_MAIN+L_SPINEFK, NoBB),
	('Hips',			0.0, 'Root', F_DEF, L_MAIN, NoBB),
	#('Hip_L',			0.0, 'Hips', 0, L_HELP, NoBB),
	#('Hip_R',			0.0, 'Hips', 0, L_HELP, NoBB),

	('Spine1',			0.0, 'Root', F_DEF, L_MAIN, (0,1,3) ),
	('Spine2',			0.0, 'Spine1', F_DEF+F_CON, L_MAIN, (1,1,3) ),
	('Spine3',			0.0, 'Spine2', F_DEF+F_CON, L_MAIN, (1,1,3) ),
	#('Shoulders',		0.0, 'Spine3', 0, L_HELP, NoBB),

	('Neck',			0.0, 'Spine3', F_DEF+F_CON, L_MAIN, (1,1,3) ),
	('Head',			0.0, 'Neck', F_DEF, L_MAIN, NoBB),

	('Rib',				0.0, 'Spine3', F_DEF, L_MAIN, NoBB),
	('Breast_L',		-45*D, 'Rib', F_DEF, L_DEF, NoBB),
	('Breast_R',		45*D, 'Rib', F_DEF, L_DEF, NoBB),
	('StomachUp',		0.0, 'Rib', F_DEF, L_MAIN, NoBB),
	('StomachLo',		0.0, 'Hips', F_DEF, L_MAIN, NoBB),

	('Penis',			0.0, 'Hips', F_DEF, L_DEF, (1,5,1) ),
	('Scrotum',			0.0, 'Hips', F_DEF, L_DEF, NoBB),
]

#
#	BodyControlPoses(fp):
#

limBreastRot = (-45*D,45*D, -10*D,10*D, -20*D,20*D)
limBreastScale =  (0.8,1.25, 0.7,1.5, 0.8,1.25)

def BodyControlPoses(fp):
	addPoseBone(fp,  'MasterFloor', 'GZM_Root', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'MasterHips', 'GZM_Root', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_HID, [])

	addPoseBone(fp,  'MasterNeck', 'GZM_Root', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_HID, [])

	addPoseBone(fp,  'Root', 'GZM_IK_Hips', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, mhx_rig.rootChildOfConstraints)

	addPoseBone(fp,  'Hips', 'GZM_CircleHips', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-50*D,40*D, -45*D,45*D, -16*D,16*D), (1,1,1)])])

	#addPoseBone(fp,  'Hip_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	#addPoseBone(fp,  'Hip_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Spine FK
	addPoseBone(fp,  'Spine1', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH, 
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,90*D, -60*D,60*D, -60*D,60*D), (1,1,1)])])

	addPoseBone(fp,  'Spine2', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-90*D,70*D, -20*D,20*D, -50*D,50*D), (1,1,1)])])

	addPoseBone(fp,  'Spine3', 'GZM_CircleChest', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-20*D,20*D, 0,0, -20*D,20*D), (1,1,1)]) ])

	# Spine IK
	addPoseBone(fp,  'Spine1IK', 'GZM_Ball', 'Spine', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	
	addPoseBone(fp,  'Spine2IK', 'GZM_Ball', 'Spine', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
		#[('ChildOf', C_CHILDOF, 0.7, ['Hips', 'Root', (1,1,1), (1,1,1), (1,1,1)]),
		# ('ChildOf', C_CHILDOF, 0.3, ['Shoulders', 'Shoulders', (1,1,1), (1,1,1), (1,1,1)])])
	
	addPoseBone(fp,  'Spine3IK', 'GZM_Ball', 'Spine', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
		#[('ChildOf', C_CHILDOF, 0.3, ['Hips', 'Root', (1,1,1), (1,1,1), (1,1,1)]),
		#('ChildOf', C_CHILDOF, 0.7, ['Shoulders', 'Shoulders', (1,1,1), (1,1,1), (1,1,1)])])

	addPoseBone(fp,  'Shoulders', 'GZM_IK_Shoulder', 'Spine', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Neck and head
	addPoseBone(fp,  'Neck', 'MHNeck', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,40*D, -45*D,45*D, -60*D,60*D), (1,1,1)])])

	addPoseBone(fp,  'Head', 'MHHead', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,40*D, -60*D,60*D, -45*D,45*D), (1,1,1)])])

	addPoseBone(fp,  'Breathe', 'MHCube01', None, (1,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'Breast_L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, 
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
		 ('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])	])

	addPoseBone(fp,  'Breast_R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
		 ('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])	])

	addPoseBone(fp,  'StomachTarget', 'MHCube01', None, (0,0,0), (1,1,1), (0,0,0), (1,1,1), 0, 
		[('LimitDist', 0, 1, ['LimitDist', 'Spine1', 'INSIDE'])])

	addPoseBone(fp,  'Penis', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

	addPoseBone(fp,  'Scrotum', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

	return

def BodyDeformPoses(fp):
	copyDeform(fp,'Root', 0, U_LOC+U_ROT, None, [])
	copyDeform(fp,'Hips', 0, U_LOC+U_ROT, 'MHDefHips', [])
	#copyDeform(fp,'Hip_L', 0, U_LOC+U_ROT, None, [])
	#copyDeform(fp,'Hip_R', 0, U_LOC+U_ROT, None, [])

	'''
	copyDeform(fp,'Spine1', 0, U_LOC+U_ROT, 'MHDefSpine1', [])
	copyDeform(fp,'Spine2', 0, U_LOC+U_ROT, 'MHDefSpine2', [])
	copyDeform(fp,'Spine3', 0, U_LOC+U_ROT, 'MHDefChest', [])
	'''
	copyDeformPartial(fp, 'Spine1', 'Spine1IK', (1,1,1), 0, U_LOC, 'MHDefSpine1', 
		[('StretchTo', 0, 1, ['Stretch', 'Spine2IK', 0])])

	copyDeformPartial(fp, 'Spine2', 'Spine2IK', (1,1,1), 0, U_LOC, 'MHDefSpine2', 
		[('StretchTo', 0, 1, ['Stretch', 'Spine3IK', 0])])

	copyDeformPartial(fp, 'Spine3', 'Spine3IK', (1,1,1), 0, U_LOC, 'MHDefChest', 
		[('StretchTo', 0, 1, ['Stretch', 'Shoulders', 0])])
	'''
	spineDeform(fp, 'Spine1', 'Spine', 0, 0, 0, 'MHDefSpine1', [])
	spineDeform(fp, 'Spine2', 'Spine', 0, 1, 0, 'MHDefSpine2', [])
	spineDeform(fp, 'Spine3', 'Spine', 0, 2, 3, 'MHDefChest', [])
	'''
	#copyDeform(fp,'Shoulders', 0, U_LOC+U_ROT, None, [])
	copyDeform(fp,'Neck', 0, U_LOC+U_ROT, 'MHDefNeck', [])
	copyDeform(fp,'Head', 0, U_LOC+U_ROT, 'MHDefHead', [])

	copyDeform(fp,'Rib', 0, U_LOC+U_ROT, 'MHDefRib', [])
	copyDeform(fp,'Breast_L', 0, U_LOC+U_ROT, None, [])
	copyDeform(fp,'Breast_R', 0, U_LOC+U_ROT, None, [])

	addPoseBone(fp,  'StomachLo', 'MHDefStomach', None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget', 0]),
		 #('CopyScale', C_LOCAL, 1, ['CopyScale', 'StomachTarget', (1,0,1), False]),
		])

	addPoseBone(fp,  'StomachUp', 'MHDefRib', None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget', 0]),
		 #('CopyScale', C_LOCAL, 1, ['CopyScale', 'StomachTarget', (1,0,1), False]),
		])

	copyDeform(fp,'Penis', 0, U_LOC+U_ROT, None, [])
	copyDeform(fp,'Scrotum', 0, U_LOC+U_ROT, None, [])
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

BodySpines = [
	('Spine', ['Root', 'Spine1', 'Spine2', 'Spine3', 'Shoulders'])
]



