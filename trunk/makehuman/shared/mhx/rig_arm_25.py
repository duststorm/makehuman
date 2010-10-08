#
#	Arm bone definitions
#

import mhx_rig
from mhx_rig import *

ArmJoints = [
	('hand_L_tail',			'j', 'r-finger-3-1'),
	('r-shoulder-head',		'l', ((0.7, 'r-shoulder'), (0.3, 'l-shoulder'))),
	('r-loarm-mid',			'l', ((0.5, 'r-hand'), (0.5, 'r-elbow'))),
	('r-loarm-fan',			'l', ((0.25, 'r-hand'), (0.75, 'r-elbow'))),
	('r-shoulder-bump',		'v', 5878),
	('r-clavicle-back',		'v', 2583),
	('r-clavicle-end',		'v', 2879),
	('r-pectoralis',		'v', 3341),
	('r-uparm-025',			'l', ((0.75, 'r-shoulder'), (0.25, 'r-elbow'))),
	('r-dorsal',			'v', 2619),

	('r-scapula-root',		'l', ((0.2, 'r-clavicle'), (0.8, 'r-clavicle-back'))),
	('r-scapula-top',		'v', 3048),
	('r-scapula-bot',		'v', 3600),

	('r-bicep-start',		'v', 3616),
	('r-bicep-end',			'v', 2987),

	('r-uparm-front',		'v', 2989),
	('r-uparm-back',		'v', 3001),

	('hand_R_tail',			'j', 'l-finger-3-1'),
	('l-shoulder-head',		'l', ((0.7, 'l-shoulder'), (0.3, 'r-shoulder'))),
	('l-loarm-mid',			'l', ((0.5, 'l-hand'), (0.5, 'l-elbow'))),
	('l-loarm-fan',			'l', ((0.25, 'l-hand'), (0.75, 'l-elbow'))),
	('l-shoulder-bump',		'v', 9663),
	('l-clavicle-back',		'v', 11025),
	('l-clavicle-end',		'v', 10795),
	('l-pectoralis',		'v', 10410),
	('l-uparm-025',			'l', ((0.75, 'l-shoulder'), (0.25, 'l-elbow'))),
	('l-dorsal',			'v', 10991),

	('l-bicep-start',		'v', 10321),
	('l-bicep-end',			'v', 10739),

	('l-scapula-root',		'l', ((0.2, 'l-clavicle'), (0.8, 'l-clavicle-back'))),
	('l-scapula-top',		'v', 10683),
	('l-scapula-bot',		'v', 10192),

]

offs = [0,0.1,0]

ArmHeadsTails = [
	# Shoulder
	('Shoulder_L',			'r-shoulder-head', 'r-shoulder'),
	('ShoulderBump_L',		'r-shoulder-bump', ('r-shoulder-bump', offs)),
	('Clavicle_L',			'r-clavicle', 'r-clavicle-end'),
	('ClavicleTarget_L',	'r-clavicle-end', ('r-clavicle-end', offs)),

	('Shoulder_R',			'l-shoulder-head', 'l-shoulder'),
	('ShoulderBump_R',		'l-shoulder-bump', ('l-shoulder-bump', offs)),
	('Clavicle_R',			'l-clavicle', 'l-clavicle-end'),
	('ClavicleTarget_R',	'l-clavicle-end', ('l-clavicle-end', offs)),

	# Pectoralis & BackArm
	('Pectoralis_L',		'r-pectoralis', 'r-uparm-025'),
	('PectoralisTarget_L',	'r-uparm-025', ('r-uparm-025', offs)),
	#('BackArm_L',			'r-dorsal', 'r-uparm-025'),

	('Pectoralis_R',		'l-pectoralis', 'l-uparm-025'),
	('PectoralisTarget_R',	'l-uparm-025', ('l-uparm-025', offs)),
	#('BackArm_R',			'l-dorsal', 'l-uparm-025'),

	# Scapula
	('Scapula_L',			'r-scapula-top', 'r-scapula-bot'),
	('Scapula_R',			'l-scapula-top', 'l-scapula-bot'),

	# Deform
	('UpArm_L',				'r-shoulder', 'r-elbow'),
	('LoArmUp_L',		'r-elbow', 'r-loarm-mid'),
	('LoArmFan_L',			'r-elbow', 'r-loarm-fan'),
	('LoArmDwn_L',				'r-loarm-mid', 'r-hand'),
	('Hand_L',				'r-hand', 'hand_L_tail'),

	('UpArm_R',				'l-shoulder', 'l-elbow'),
	('LoArmUp_R',		'l-elbow', 'l-loarm-mid'),
	('LoArmFan_R',			'l-elbow', 'l-loarm-fan'),
	('LoArmDwn_R',				'l-loarm-mid', 'l-hand'),
	('Hand_R',				'l-hand', 'hand_R_tail'),

	# Biceps
	('Bicep_L',				'r-bicep-start', 'r-bicep-end'),
	('BicepTarget_L',		'r-bicep-end', ('r-bicep-end', offs)),
	('Bicep_R',				'l-bicep-start', 'l-bicep-end'),
	('BicepTarget_R',		'l-bicep-end', ('l-bicep-end', offs)),

	# FK
	('UpArmFK_L',			'r-shoulder', 'r-elbow'),
	('LoArmFK_L',			'r-elbow', 'r-hand'),
	('HandFK_L',			'r-hand', 'hand_L_tail'),
	('UpArmFK_R',			'l-shoulder', 'l-elbow'),
	('LoArmFK_R',			'l-elbow', 'l-hand'),
	('HandFK_R',			'l-hand', 'hand_R_tail'),

	# IK
	('UpArmIK_L',			'r-shoulder', 'r-elbow'),
	('LoArmIK_L',			'r-elbow', 'r-hand'),
	('HandIK_L',			'r-hand', 'hand_L_tail'),
	('UpArmIK_R',			'l-shoulder', 'l-elbow'),
	('LoArmIK_R',			'l-elbow', 'l-hand'),
	('HandIK_R',			'l-hand', 'hand_R_tail'),
]

#upArmRoll = 1.69297
#loArmRoll = deg90
#handRoll = 1.22173

upArmRoll = 0.0
loArmRoll = 0.0
handRoll = 0.0

spineTop = 'Spine3'
L_SHOULDER = L_ARMFK+L_ARMIK+L_SPINE

ArmArmature = [
	# Shoulder
	('Shoulder_L',			0.0, spineTop, F_DEF+F_WIR, L_SHOULDER+L_DEF, (1,1,1) ),
	('ShoulderBump_L',		0.0, 'Shoulder_L', F_DEF, L_DEF, (1,1,1) ),
	('Clavicle_L',			0.0, 'Spine3', F_DEF, L_DEF, (1,1,1) ),
	('ClavicleTarget_L',	0.0, 'Shoulder_L', 0, L_HELP, (1,1,1) ),

	('Shoulder_R',			0.0, spineTop, F_DEF+F_WIR, L_SHOULDER+L_DEF, (1,1,1) ),
	('ShoulderBump_R',		0.0, 'Shoulder_R', F_DEF, L_DEF, (1,1,1) ),
	('Clavicle_R',			0.0, 'Spine3', F_DEF, L_DEF, (1,1,1) ),
	('ClavicleTarget_R',	0.0, 'Shoulder_R', 0, L_HELP, (1,1,1) ),

	# Scapula
	('Scapula_L',		0.0, 'Shoulder_L', F_DEF, L_DEF, (1,1,1) ),
	('Scapula_R',		0.0, 'Shoulder_R', F_DEF, L_DEF, (1,1,1) ),

	# Deform
	('UpArm_L',			upArmRoll, 'Shoulder_L', F_DEF, L_DEF, (1,1,1) ),
	('LoArmUp_L',		loArmRoll, 'UpArm_L', F_DEF, L_DEF, (1,1,1) ),
	('LoArmFan_L',		loArmRoll, 'UpArm_L', F_DEF, L_DEF, (1,1,1) ),
	('LoArmDwn_L',		loArmRoll, 'LoArmUp_L', F_DEF, L_DEF, (1,1,1) ),
	('Hand_L',			handRoll, 'LoArmDwn_L', F_DEF, L_DEF, (1,1,1) ),

	('UpArm_R',			upArmRoll, 'Shoulder_R', F_DEF, L_DEF, (1,1,1) ),
	('LoArmUp_R',		loArmRoll, 'UpArm_R', F_DEF, L_DEF, (1,1,1) ),
	('LoArmFan_R',		loArmRoll, 'UpArm_R', F_DEF, L_DEF, (1,1,1) ),
	('LoArmDwn_R',		loArmRoll, 'LoArmUp_R', F_DEF, L_DEF, (1,1,1) ),
	('Hand_R',			handRoll, 'LoArmDwn_R', F_DEF, L_DEF, (1,1,1) ),

	# Biceps
	('Bicep_L',			upArmRoll, 'UpArm_L', F_DEF, L_DEF, (1,1,1) ),
	('BicepTarget_L',	0.0, 'UpArm_L', 0, L_HELP, (1,1,1) ),
	('Bicep_R',			upArmRoll, 'UpArm_R', F_DEF, L_DEF, (1,1,1) ),
	('BicepTarget_R',	0.0, 'UpArm_R', 0, L_HELP, (1,1,1) ),

	# Pectoralis & BackArm
	('Pectoralis_L',		0.0, 'Spine2', F_DEF, L_DEF, (1,1,1) ),
	('PectoralisTarget_L',	0.0, 'UpArm_L', 0, L_HELP, (1,1,1) ),
	#('BackArm_L',			0.0, 'Spine2', F_DEF, L_DEF, (1,1,1) ),

	('Pectoralis_R',		0.0, 'Spine2', F_DEF, L_DEF, (1,1,1) ),
	('PectoralisTarget_R',	0.0, 'UpArm_R', 0, L_HELP, (1,1,1) ),
	#('BackArm_R',			0.0, 'Spine2', F_DEF, L_DEF, (1,1,1) ),

	# FK
	('UpArmFK_L',		upArmRoll, 'Shoulder_L', F_WIR, L_ARMFK, (1,1,1) ),
	('LoArmFK_L',		loArmRoll, 'UpArmFK_L', F_WIR, L_ARMFK, (1,1,1) ),
	('HandFK_L',		handRoll, 'LoArmFK_L', F_WIR, L_ARMFK, (1,1,1) ),
	('UpArmFK_R',		-upArmRoll, 'Shoulder_R', F_WIR, L_ARMFK, (1,1,1) ),
	('LoArmFK_R',		-loArmRoll, 'UpArmFK_R', F_WIR, L_ARMFK, (1,1,1) ),
	('HandFK_R',		-handRoll, 'LoArmFK_R', F_WIR, L_ARMFK, (1,1,1) ),

	# IK 
	('UpArmIK_L',		upArmRoll, 'Shoulder_L', 0, L_ARMIK, (1,1,1) ),
	('LoArmIK_L',		loArmRoll, 'UpArmIK_L', 0, L_ARMIK, (1,1,1) ),
	('HandIK_L',		handRoll, None, F_WIR, L_ARMIK, (1,1,1)),
	('UpArmIK_R',		-upArmRoll, 'Shoulder_R', 0, L_ARMIK, (1,1,1) ),
	('LoArmIK_R',		-loArmRoll, 'UpArmIK_R', 0, L_ARMIK, (1,1,1) ),
	('HandIK_R',		-handRoll, None, F_WIR, L_ARMIK, (1,1,1)),
]

#
#
#

limClavicle_L = (-deg45,deg45, 0,0, -deg20,deg20)
limClavicle_R = (-deg45,deg45, 0,0, -deg20,deg20)

limUpArm_L = (-deg90,deg90, -deg45,deg90, -deg90,deg45)
limUpArm_R = (-deg90,deg90, -deg90,deg45, -deg45,deg90)

limLoArmDwn_L = (0,0, -deg90,deg90, -deg90,deg10)
limLoArmDwn_R = (0,0, -deg90,deg90, -deg10,deg90)

limHand_L = (-deg90,70*deg1, 0,0, -deg20,deg20)
limHand_R = (-deg90,70*deg1, 0,0, -deg20,deg20)

def ArmWritePoses(fp):
	# Shoulder
	addPoseBone(fp, 'Shoulder_L', 'GoboShldr_L', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Clavicle_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'ClavicleTarget_L', 'PLANE_X', 0])])

	addPoseBone(fp, 'ShoulderBump_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('Transform', C_OW_LOCAL+C_TG_LOCAL, 1, ['Transform', 'UpArm_L',
			'ROTATION', (0,0,0), (60,0,0), ('X', 'X', 'X'),
			'LOCATION', (0,0,0), (0,'0.3*theScale',0)])
		])

	addPoseBone(fp, 'Shoulder_R', 'GoboShldr_R', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Clavicle_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'ClavicleTarget_R', 'PLANE_X', 0])])

	addPoseBone(fp, 'ShoulderBump_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('Transform', C_OW_LOCAL+C_TG_LOCAL, 1, ['Transform', 'UpArm_R',

			'ROTATION', (0,0,0), (60,0,0), ('X', 'X', 'X'),
			'LOCATION', (0,0,0), (0,'0.3*theScale',0)])
		])

	# Pectoralis & BackArm
	addPoseBone(fp, 'Pectoralis_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'PectoralisTarget_L', 'PLANE_X', 0])])

	addPoseBone(fp, 'Pectoralis_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'PectoralisTarget_R', 'PLANE_X', 0])])
	'''
	addPoseBone(fp, 'BackArm_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'PectoralisTarget_L', 'PLANE_X', 0])])

	addPoseBone(fp, 'BackArm_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'PectoralisTarget_R', 'PLANE_X', 0])])
	'''
	# Scapula
	addPoseBone(fp, 'Scapula_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Scapula_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Biceps
	vec = aljabr.vsub(mhx_rig.locations['r-uparm-front'], mhx_rig.locations['r-uparm-back'])
	dist = aljabr.vlen(vec) - 0.5
	if dist < 0: dist = 0
	bicepMove = str(0.4*dist)+'*theScale'

	addPoseBone(fp, 'Bicep_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('Transform', C_OW_LOCAL+C_TG_LOCAL, 1, ['Transform', 'LoArmUp_L',
			'ROTATION', (0,0,-90), (0,0,0), ('Z', 'Z', 'Z'),
			'LOCATION', (bicepMove,0,0), (0,0,0)]),
		('StretchTo', 0, 1, ['Stretch', 'BicepTarget_L', 'PLANE_X', 0])
		])

	addPoseBone(fp, 'BicepTarget_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('Transform', C_OW_LOCAL+C_TG_LOCAL, 1, ['Transform', 'LoArmUp_L',
			'ROTATION', (0,0,-90), (0,0,0), ('Z', 'Z', 'Z'),
			'LOCATION', (0,0,bicepMove), (0,0,0)])
		])

	addPoseBone(fp, 'Bicep_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('Transform', C_OW_LOCAL+C_TG_LOCAL, 1, ['Transform', 'LoArmUp_R',
			'ROTATION', (0,0,0), (0,0,90), ('Z', 'Z', 'Z'),
			'LOCATION', (0,0,0), ('-'+bicepMove,0,0)]),
		('StretchTo', 0, 1, ['Stretch', 'BicepTarget_R', 'PLANE_X', 0])
		])

	addPoseBone(fp, 'BicepTarget_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('Transform', C_OW_LOCAL+C_TG_LOCAL, 1, ['Transform', 'LoArmUp_R',
			'ROTATION', (0,0,0), (0,0,90), ('Z', 'Z', 'Z'),
			'LOCATION', (0,0,0), (0,0,bicepMove)])
		])

	# Deform
	addDeformLimb(fp, 'UpArm_L', 'UpArmIK_L', (1,1,1), 'UpArmFK_L', (1,1,1), 0, P_STRETCH)

	addPoseBone(fp, 'LoArmUp_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 0, ['RotIKXZ', 'LoArmIK_L', (1,0,1), (0,0,0), False]),
		('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 1, ['RotFKXZ', 'LoArmFK_L', (1,0,1), (0,0,0), False]),
		('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 0, ['RotIKY', 'LoArmIK_L', (0,1,0), (0,0,0), False]),
		('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 0.5, ['RotFKY', 'LoArmFK_L', (0,1,0), (0,0,0), False])])

	addPoseBone(fp, 'LoArmFan_L', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 0.5, ['Rot', 'LoArmUp_L', (1,0,1), (0,0,0), False])])

	addDeformLimb(fp, 'LoArmDwn_L', 'LoArmIK_L', (1,1,1), 'LoArmFK_L', (1,1,1), 0, P_STRETCH)

	addDeformLimb(fp, 'Hand_L', 'HandIK_L', (1,1,1), 'HandFK_L', (1,1,1), 0, 0)

	addDeformLimb(fp, 'UpArm_R', 'UpArmIK_R', (1,1,1), 'UpArmFK_R', (1,1,1), 0, P_STRETCH)

	addPoseBone(fp, 'LoArmUp_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 0, ['RotIKXZ', 'LoArmIK_R', (1,0,1), (0,0,0), False]),
		('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 1, ['RotFKXZ', 'LoArmFK_R', (1,0,1), (0,0,0), False]),
		('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 0, ['RotIKY', 'LoArmIK_R', (0,1,0), (0,0,0), False]),
		('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 0.5, ['RotFKY', 'LoArmFK_R', (0,1,0), (0,0,0), False])])

	addPoseBone(fp, 'LoArmFan_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 0.5, ['Rot', 'LoArmUp_R', (1,0,1), (0,0,0), False])])

	addDeformLimb(fp, 'LoArmDwn_R', 'LoArmIK_R', (1,1,1), 'LoArmFK_R', (1,1,1), 0, P_STRETCH)

	addDeformLimb(fp, 'Hand_R', 'HandIK_R', (1,1,1), 'HandFK_R', (1,1,1), 0, 0)

	# FK
	addPoseBone(fp, 'UpArmFK_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_L, (True, True, True)])])

	addPoseBone(fp, 'LoArmFK_L', 'MHCircle025', 'FK_L', (1,1,1), (1,0,0), (0,0,0), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArmDwn_L, (True, True, True)])])

	addPoseBone(fp, 'HandFK_L', 'MHHand', 'FK_L', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_L, (True, True, True)])])
		

	addPoseBone(fp, 'UpArmFK_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_R, (True, True, True)])])

	addPoseBone(fp, 'LoArmFK_R', 'MHCircle025', 'FK_R', (1,1,1), (1,0,0), (0,0,0), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArmDwn_R, (True, True, True)])])

	addPoseBone(fp, 'HandFK_R', 'MHHand', 'FK_R', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_R, (True, True, True)])])


	# IK

	addPoseBone(fp, 'UpArmIK_L', None, 'IK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_L, (True, True, True)])])

	addPoseBone(fp, 'LoArmIK_L', None, 'IK_L', (1,1,1), (1,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, 1, ['IK', 'HandIK_L', 2, None, (True, False,True)]),
		('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 1, ['CopyRotY', 'HandIK_L', (0,1,0), (0,0,0), False]),
		#('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArmDwn_L, (True, True, True)])
		])

	addPoseBone(fp, 'HandIK_L', 'GoboHandCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_L', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['Shoulder_L', 'fNoStretch', 'Shoulder_L'])])


	addPoseBone(fp, 'UpArmIK_R', None, 'IK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_R, (True, True, True)])])

	addPoseBone(fp, 'LoArmIK_R', None, 'IK_R', (1,1,1), (1,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, 1, ['IK', 'HandIK_R', 2, None, (True, False,True)]),
		('CopyRot', C_OW_LOCAL+C_TG_LOCAL, 1, ['CopyRotY', 'HandIK_R', (0,1,0), (0,0,0), False])
		#('LimitRot', C_OW_LOCAL, 0, ['LimitRot', limLoArmDwn_R, (True, True, True)])
		])

	addPoseBone(fp, 'HandIK_R', 'GoboHandCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_R', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['Shoulder_R', 'fNoStretch', 'Shoulder_R'])])

	return
	
#
#	ArmWriteActions(fp)
#

def ArmWriteActions(fp):
	return

#
#	ArmDrivers
#	(Bone, FK constraint, IK constraint, driver, channel, max)
#

ArmDrivers = [
	("UpArm_L", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PArmIK_L", "LOC_X", 1.0),
	("LoArmUp_L", True, ["RotFKXZ"], ["RotIKXZ"], "PArmIK_L", "LOC_X", 1),
	("LoArmUp_L", True, ["RotFKY"], ["RotIKY"], "PArmIK_L", "LOC_X", 0.5),
	("LoArmDwn_L", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PArmIK_L", "LOC_X", 1.0),
	("Hand_L", True, ["RotFK"], ["RotIK"], "PArmIK_L", "LOC_X", 1.0),

	("UpArm_R", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PArmIK_R", "LOC_X", 1.0),
	("LoArmUp_R", True, ["RotFKXZ"], ["RotIKXZ"], "PArmIK_R", "LOC_X", 1),
	("LoArmUp_R", True, ["RotFKY"], ["RotIKY"], "PArmIK_R", "LOC_X", 0.5),
	("LoArmDwn_R", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PArmIK_R", "LOC_X", 1.0),
	("Hand_R", True, ["RotFK"], ["RotIK"], "PArmIK_R", "LOC_X", 1.0),

]

#
#	ArmProcess
#	(bone, axis, angle)
#

ArmProcess = [
	("LoArmDwn_L", "Z", -deg20),
	("LoArmDwn_R", "Z", deg20),
	("LoArmUp_L", "Z", -deg20),
	("LoArmUp_R", "Z", deg20),
]	

ArmSnaps = [
	("LoArmFK_L", "LoArmDwn_L", 'Both'),
	("LoArmIK_L", "LoArmDwn_L", 'Both'),
	("HandFK_L", "Hand_L", 'Both'),
	("HandIK_L", "Hand_L", 'Both'),

	("LoArmFK_R", "LoArmDwn_R", 'Both'),
	("LoArmIK_R", "LoArmDwn_R", 'Both'),
	("HandFK_R", "Hand_R", 'Both'),
	("HandIK_R", "Hand_R", 'Both'),
]

ArmParents = [
]

ArmSelects = []

ArmRolls = []


