#
#	Arm bone definitions 
#

import mhx_rig
from mhx_rig import *

ArmJoints = [
	('hand_L_tail',			'j', 'r-finger-3-1'),
	('hand_R_tail',			'j', 'l-finger-3-1'),

	('r-uparm1',			'l', ((1-bbMarg, 'r-shoulder'), (bbMarg, 'r-elbow'))),
	('r-uparm2',			'l', ((0.5, 'r-shoulder'), (0.5, 'r-elbow'))),
	('r-loarm1',			'l', ((1-bbMarg, 'r-elbow'), (bbMarg, 'r-hand'))),
	('r-loarm2',			'l', ((bbMarg, 'r-elbow'), (1-bbMarg, 'r-hand'))),

	('l-uparm1',			'l', ((1-bbMarg, 'l-shoulder'), (bbMarg, 'l-elbow'))),
	('l-uparm2',			'l', ((0.5, 'l-shoulder'), (0.5, 'l-elbow'))),
	('l-loarm1',			'l', ((1-bbMarg, 'l-elbow'), (bbMarg, 'l-hand'))),
	('l-loarm2',			'l', ((bbMarg, 'l-elbow'), (1-bbMarg, 'l-hand'))),

	('r-uparm-front',		'v', 3440),
	('r-uparm-back',		'v', 3438),
	('r-uparm-over',		'v', 3014),
	('r-uparm-under',		'v', 3053),

	('l-uparm-front',		'v', 10175),
	('l-uparm-back',		'v', 10330),
	('l-uparm-over',		'v', 10712),
	('l-uparm-under',		'v', 10678),

	('r-loarm-mid',			'l', ((0.5, 'r-hand'), (0.5, 'r-elbow'))),
	('r-loarm-fan',			'l', ((0.25, 'r-hand'), (0.75, 'r-elbow'))),

	('l-loarm-mid',			'l', ((0.5, 'l-hand'), (0.5, 'l-elbow'))),
	('l-loarm-fan',			'l', ((0.25, 'l-hand'), (0.75, 'l-elbow'))),

	('r-clavicle-back',		'v', 2583),
	('r-clavicle-end',		'v', 2879),
	('l-clavicle-back',		'v', 11025),
	('l-clavicle-end',		'v', 10795),

	('r-pectoralis',		'v', 3341),
	('r-trapezeus-1',		'v', 2584),
	('r-trapezeus-2',		'v', 3633),
	('r-latdorsi',			'v', 4432),
	('r-deltoid',			'v', 2854),

	('l-pectoralis',		'v', 10410),
	('l-trapezeus-1',		'v', 11024),
	('l-trapezeus-2',		'v', 10159),
	('l-latdorsi',			'v', 9995),
	('l-deltoid'	,		'v', 10820),

	('r-shoulder-head',		'l', ((0.7, 'r-scapula'), (0.3, 'l-scapula'))),
	('l-shoulder-head',		'l', ((0.3, 'r-scapula'), (0.7, 'l-scapula'))),

	('r-shoulder-top',		'v', 2862),
	('l-shoulder-top',		'v', 10812),
	('r-shoulder-tail',		'l', ((0.5, 'r-shoulder-top'), (0.5, 'r-shoulder'))),
	('l-shoulder-tail',		'l', ((0.5, 'l-shoulder-top'), (0.5, 'l-shoulder'))),
	
	('sternum-tail',		'v', 7279),
	('sternum-head',		'l', ((0.5, 'neck'), (0.5, 'sternum-tail'))),
	('r-shoulder-aim',		'l', ((0.5, 'sternum-head'), (0.5, 'r-shoulder-tail'))),
	('l-shoulder-aim',		'l', ((0.5, 'sternum-head'), (0.5, 'l-shoulder-tail'))),

	('r-scapula-head',		'v', 2602),
	('r-scapula-tail',		'v', 2584),
	('l-scapula-head',		'v', 11008),
	('l-scapula-tail',		'v', 11024),

	('r-elbow-pt',			'o', ('r-elbow', [0,0,-3])),
	('l-elbow-pt',			'o', ('l-elbow', [0,0,-3])),

	('r-elbow-head',		'v', 2987),
	('r-elbow-tail',		'v', 4569),
	('l-elbow-head',		'v', 10739),
	('l-elbow-tail',		'v', 9904),
]

'''
	#('Shoulder_L',			'r-clavicle', 'r-scapula'),
	#('ShoulderScapula_L',	'r-shoulder', 'r-scapula'),
	#('Clavicle_L',			'r-shoulder-head', 'r-shoulder-tail'),
	#('Trapezeus-1_L',		'r-trapezeus-1', 'r-scapula'),
	#('Trapezeus-2_L',		'r-trapezeus-2', 'r-uparm-back'),

	('Shoulder_R',			'l-shoulder-head', 'l-scapula'),
	#('Shoulder_R',			'l-clavicle', 'l-scapula'),
	#('ShoulderScapula_R',	'l-shoulder', 'l-scapula'),
	('Clavicle_R',			'l-clavicle', 'l-scapula'),
	('Trapezeus-1_R',		'l-trapezeus-1', 'l-scapula'),
	('Trapezeus-2_R',		'l-trapezeus-2', 'l-uparm-back'),

'''
ArmHeadsTails = [
	('Sternum',				'neck', 'sternum-tail'),
	('SternumTarget',		'sternum-head', 'sternum-tail'),
	
	# Shoulder
	('Shoulder_L',			'r-clavicle', 'r-shoulder-tail'),
	('ShoulderPivot_L',		'r-clavicle', 'r-shoulder-tail'),
	('ShoulderUp_L',		('r-shoulder-tail', yunit), ('r-shoulder-tail', ybis)),
	('ShoulderAim_L',		'r-shoulder-tail', 'r-shoulder-aim'),
	('Scapula_L',			'r-scapula-head', 'r-scapula-tail'),

	('Shoulder_R',			'l-clavicle', 'l-shoulder-tail'),
	('ShoulderPivot_R',		'l-clavicle', 'l-shoulder-tail'),
	('ShoulderUp_R',		('l-shoulder-tail', yunit), ('l-shoulder-tail', ybis)),
	('ShoulderAim_R',		'l-shoulder-tail', 'l-shoulder-aim'),
	('Scapula_R',			'l-scapula-head', 'l-scapula-tail'),

	('ArmLoc_L',			'r-shoulder-tail', ('r-shoulder-tail', yunit)),
	('ArmLoc_R',			'l-shoulder-tail', ('l-shoulder-tail', yunit)),

	# Shoulder deform
	('Pectoralis_L',		'r-pectoralis', 'r-uparm-front'),
	('PectoralisTrg_L',		'r-uparm-front', ('r-uparm-front', yunit)),
	('LatDorsi_L',			'r-latdorsi', 'r-uparm-back'),
	('LatDorsiTrg_L',		'r-uparm-back', ('r-uparm-back', yunit)),
	('Deltoid_L',			'r-deltoid', 'r-uparm-over'),
	('DeltoidTrg_L',		'r-uparm-over', ('r-uparm-over', yunit)),

	('Pectoralis_R',		'l-pectoralis', 'l-uparm-front'),
	('PectoralisTrg_R',		'l-uparm-front', ('l-uparm-front', yunit)),
	('LatDorsi_R',			'l-latdorsi', 'l-uparm-back'),
	('LatDorsiTrg_R',		'l-uparm-back', ('l-uparm-back', yunit)),
	('Deltoid_R',			'l-deltoid', 'l-uparm-over'),
	('DeltoidTrg_R',		'l-uparm-over', ('l-uparm-over', yunit)),

	# Elbow bend
	('ElbowBend_L',			'r-elbow-head', 'r-elbow-tail'),
	('ElbowBendTrg_L',		'r-elbow-tail', ('r-elbow-tail', yunit)),
	('ElbowBend_R',			'l-elbow-head', 'l-elbow-tail'),
	('ElbowBendTrg_R',		'l-elbow-tail', ('l-elbow-tail', yunit)),

	# Deform
	('UpArm1_L',			'r-shoulder', 'r-uparm1'),
	('UpArm2_L',			'r-uparm1', 'r-uparm2'),
	('UpArm3_L',			'r-uparm2', 'r-elbow'),
	('LoArm1_L',			'r-elbow', 'r-loarm1'),
	('LoArm2_L',			'r-loarm1', 'r-loarm2'),
	('LoArm3_L',			'r-loarm2', 'r-hand'),
	('LoArmFan_L',			'r-elbow', 'r-loarm-fan'),
	('Hand_L',				'r-hand', 'hand_L_tail'),

	('UpArm1_R',			'l-shoulder', 'l-uparm1'),
	('UpArm2_R',			'l-uparm1', 'l-uparm2'),
	('UpArm3_R',			'l-uparm2', 'l-elbow'),
	('LoArm1_R',			'l-elbow', 'l-loarm1'),
	('LoArm2_R',			'l-loarm1', 'l-loarm2'),
	('LoArm3_R',			'l-loarm2', 'l-hand'),
	('LoArmFan_R',			'l-elbow', 'l-loarm-fan'),
	('Hand_R',				'l-hand', 'hand_R_tail'),

	# Rotation diffs
	('BendArmDown_L',		'r-shoulder', ('r-shoulder', (0,-1,0))),
	('BendArmDown_R',		'l-shoulder', ('l-shoulder', (0,-1,0))),
	('BendArmUp_L',			'r-shoulder', ('r-shoulder', (0,1,0))),
	('BendArmUp_R',			'l-shoulder', ('l-shoulder', (0,1,0))),
	('BendShoulderUp_L',	'r-shoulder-head', ('r-shoulder-head', (0,1,0))),
	('BendShoulderUp_R',	'l-shoulder-head', ('l-shoulder-head', (0,1,0))),
	('BendLoArmForward_L',	'r-elbow', ('r-elbow', (0,0,1))),
	('BendLoArmForward_R',	'l-elbow', ('l-elbow', (0,0,1))),
	
	# FK
	('UpArmFK_L',			'r-shoulder', 'r-elbow'),
	('LoArmFK_L',			'r-elbow', 'r-hand'),
	('HandFK_L',			'r-hand', 'hand_L_tail'),
	('UpArmFK_R',			'l-shoulder', 'l-elbow'),
	('LoArmFK_R',			'l-elbow', 'l-hand'),
	('HandFK_R',			'l-hand', 'hand_R_tail'),

	# IK
	('UpArmIK_L',			'r-shoulder', 'r-elbow'),
	('ElbowIK_L',			'r-elbow', ('r-elbow',yunit)),
	('LoArmIK_L',			'r-elbow', 'r-hand'),
	('WristIK_L',			'r-hand', 'hand_L_tail'),
	('HandIK_L',			'r-hand', 'hand_L_tail'),
	('UpArmIK_R',			'l-shoulder', 'l-elbow'),
	('ElbowIK_R',			'l-elbow', ('l-elbow',yunit)),
	('LoArmIK_R',			'l-elbow', 'l-hand'),
	('WristIK_R',			'l-hand', 'hand_R_tail'),
	('HandIK_R',			'l-hand', 'hand_R_tail'),

	#
	('UpArmPTFK_L',			('r-shoulder', yunit), ('r-shoulder', ybis)),
	('LoArmPTFK_L',			('r-elbow', yunit), ('r-elbow', ybis)),
	('UpArmPTFK_R',			('l-shoulder', yunit), ('l-shoulder', ybis)),
	('LoArmPTFK_R',			('l-elbow', yunit), ('l-elbow', ybis)),

	('UpArmPTIK_L',			('r-shoulder', yunit), ('r-shoulder', ybis)),
	('LoArmPTIK_L',			('r-elbow', yunit), ('r-elbow', ybis)),
	('UpArmPTIK_R',			('l-shoulder', yunit), ('l-shoulder', ybis)),
	('LoArmPTIK_R',			('l-elbow', yunit), ('l-elbow', ybis)),

	# Pole Target
	('ElbowPTIK_L',			'r-elbow-pt', ('r-elbow-pt', yunit)),
	('ElbowPTIK_R',			'l-elbow-pt', ('l-elbow-pt', yunit)),
	('ElbowLinkPTIK_L',		'r-elbow', 'r-elbow-pt'),
	('ElbowLinkPTIK_R',		'l-elbow', 'l-elbow-pt'),
	('ElbowPTFK_L',			'r-elbow-pt', ('r-elbow-pt', yunit)),
	('ElbowPTFK_R',			'l-elbow-pt', ('l-elbow-pt', yunit)),
]

#upArmRoll = 1.69297
#loArmRoll = 90*D
#handRoll = 1.22173

upArmRoll = 0.0
loArmRoll = 0.0
handRoll = 0.0

L_SHOULDER = L_ARMFK+L_ARMIK+L_SPINE

'''
	('Clavicle_L',			0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	('Trapezeus-1_L',		0.0, 'Spine2', F_DEF, L_DEF, NoBB),
	('Trapezeus-2_L',		0.0, 'Spine2', F_DEF, L_DEF, NoBB),

	('Clavicle_R',			0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	('Trapezeus-1_R',		0.0, 'Spine2', F_DEF, L_DEF, NoBB),
	('Trapezeus-2_R',		0.0, 'Spine2', F_DEF, L_DEF, NoBB),
'''

ArmArmature = [
	('Sternum',				0.0, 'Spine3', 0, L_HELP, NoBB),
	('SternumTarget',		0.0, 'Sternum', 0, L_HELP, NoBB),

	# Shoulder
	('Shoulder_L',			0.0, 'Sternum', F_WIR+F_DEF, L_SHOULDER+L_DEF, NoBB),
	('ShoulderPivot_L',		0.0, 'Sternum', 0, L_HELP, NoBB),
	('ShoulderUp_L',		0.0, 'ShoulderPivot_L', 0, L_HELP, NoBB),
	('ShoulderAim_L',		0.0, 'ShoulderPivot_L', 0, L_HELP, NoBB),
	('Scapula_L',			0.0, 'ShoulderAim_L', F_DEF, L_DEF, NoBB),

	('Shoulder_R',			0.0, 'Sternum', F_WIR+F_DEF, L_SHOULDER+L_DEF, NoBB),
	('ShoulderPivot_R',		0.0, 'Sternum', 0, L_HELP, NoBB),
	('ShoulderUp_R',		0.0, 'ShoulderPivot_R', 0, L_HELP, NoBB),
	('ShoulderAim_R',		0.0, 'ShoulderPivot_R', 0, L_HELP, NoBB),
	('Scapula_R',			0.0, 'ShoulderAim_R', F_DEF, L_DEF, NoBB),

	('ArmLoc_L',			0.0, 'Shoulder_L', 0, L_HELP, NoBB),
	('ArmLoc_R',			0.0, 'Shoulder_R', 0, L_HELP, NoBB),

	# Arm deform
	('UpArm1_L',		upArmRoll, 'ArmLoc_L', F_DEF, L_DEF, NoBB),
	('UpArm2_L',		upArmRoll, 'UpArm1_L', F_DEF+F_CON, L_DEF,(0,0,5) ),
	('UpArm3_L',		upArmRoll, 'UpArm2_L', F_DEF+F_CON, L_DEF, NoBB),
	('LoArm1_L',		loArmRoll, 'UpArm3_L', F_DEF, L_DEF, NoBB),
	('LoArm2_L',		loArmRoll, 'LoArm1_L', F_DEF+F_CON, L_DEF, (0,0,5) ),
	('LoArm3_L',		loArmRoll, 'LoArm2_L', F_DEF+F_CON, L_DEF, NoBB),
	('LoArmFan_L',		loArmRoll, 'UpArm3_L', F_DEF, L_DEF, NoBB),
	('Hand_L',			handRoll, 'LoArm3_L', F_DEF, L_DEF, NoBB),

	('UpArm1_R',		upArmRoll, 'ArmLoc_R', F_DEF, L_DEF, NoBB),
	('UpArm2_R',		upArmRoll, 'UpArm1_R', F_DEF+F_CON, L_DEF,(0,0,5) ),
	('UpArm3_R',		upArmRoll, 'UpArm2_R', F_DEF+F_CON, L_DEF, NoBB),
	('LoArm1_R',		loArmRoll, 'UpArm3_R', F_DEF, L_DEF, NoBB),
	('LoArm2_R',		loArmRoll, 'LoArm1_R', F_DEF+F_CON, L_DEF, (0,0,5) ),
	('LoArm3_R',		loArmRoll, 'LoArm2_R', F_DEF+F_CON, L_DEF, NoBB),
	('LoArmFan_R',		loArmRoll, 'UpArm3_R', F_DEF, L_DEF, NoBB),
	('Hand_R',			handRoll, 'LoArm3_R', F_DEF, L_DEF, NoBB),

	# Shoulder deform
	('Pectoralis_L',		0.0, 'Spine2', F_DEF, L_DEF, NoBB),
	('PectoralisTrg_L',		0.0, 'UpArm1_L', 0, L_HELP, NoBB),
	('LatDorsi_L',			0.0, 'Spine1', F_DEF, L_DEF, NoBB),
	('LatDorsiTrg_L',		0.0, 'UpArm1_L', 0, L_HELP, NoBB),
	('Deltoid_L',			0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	('DeltoidTrg_L',		0.0, 'UpArm1_L', 0, L_HELP, NoBB),

	('Pectoralis_R',		0.0, 'Spine2', F_DEF, L_DEF, NoBB),
	('PectoralisTrg_R',		0.0, 'UpArm1_R', 0, L_HELP, NoBB),
	('LatDorsi_R',			0.0, 'Spine1', F_DEF, L_DEF, NoBB),
	('LatDorsiTrg_R',		0.0, 'UpArm1_R', 0, L_HELP, NoBB),
	('Deltoid_R',			0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	('DeltoidTrg_R',		0.0, 'UpArm1_R', 0, L_HELP, NoBB),

	# Elbow deform
	('ElbowBend_L',			0.0, 'UpArm3_L', F_DEF, L_DEF, NoBB),
	('ElbowBendTrg_L',		0.0, 'LoArm1_L', 0, L_HELP, NoBB),
	('ElbowBend_R',			0.0, 'UpArm3_R', F_DEF, L_DEF, NoBB),
	('ElbowBendTrg_R',		0.0, 'LoArm1_R', 0, L_HELP, NoBB),

	# Rotation diffs
	('BendArmDown_L',		90*D, 'Shoulder_L', 0, L_HELP, NoBB),
	('BendArmDown_R',		-90*D, 'Shoulder_R', 0, L_HELP, NoBB),
	('BendArmUp_L',			-90*D, 'Shoulder_L', 0, L_HELP, NoBB),
	('BendArmUp_R',			90*D, 'Shoulder_R', 0, L_HELP, NoBB),
	('BendShoulderUp_L',	-90*D, 'Spine3', 0, L_HELP, NoBB),
	('BendShoulderUp_R',	90*D, 'Spine3', 0, L_HELP, NoBB),
	('BendLoArmForward_L',	0, 'UpArm3_L', 0, L_HELP, NoBB),
	('BendLoArmForward_R',	0, 'UpArm3_R', 0, L_HELP, NoBB),

	# FK
	('UpArmFK_L',		upArmRoll, 'ArmLoc_L', F_WIR, L_ARMFK, NoBB),
	('LoArmFK_L',		loArmRoll, 'UpArmFK_L', F_WIR, L_ARMFK, NoBB),
	('HandFK_L',		handRoll, 'LoArmFK_L', F_CON+F_WIR, L_ARMFK, NoBB),
	('UpArmFK_R',		-upArmRoll, 'ArmLoc_R', F_WIR, L_ARMFK, NoBB),
	('LoArmFK_R',		-loArmRoll, 'UpArmFK_R', F_WIR, L_ARMFK, NoBB),
	('HandFK_R',		-handRoll, 'LoArmFK_R', F_CON+F_WIR, L_ARMFK, NoBB),

	# IK 
	('UpArmIK_L',		upArmRoll, 'ArmLoc_L', 0, L_ARMIK, NoBB),
	('ElbowIK_L',		0, Master, F_WIR, L_ARMIK, NoBB),
	('LoArmIK_L',		loArmRoll, 'UpArmIK_L', 0, L_ARMIK, NoBB),
	('WristIK_L',		handRoll, Master, F_WIR, L_ARMIK, NoBB),
	('HandIK_L',		handRoll, 'LoArmIK_L', F_WIR, L_ARMIK, NoBB),
	('UpArmIK_R',		-upArmRoll, 'ArmLoc_R', 0, L_ARMIK, NoBB),
	('ElbowIK_R',		0, Master, F_WIR, L_ARMIK, NoBB),
	('LoArmIK_R',		-loArmRoll, 'UpArmIK_R', 0, L_ARMIK, NoBB),
	('WristIK_R',		handRoll, Master, F_WIR, L_ARMIK, NoBB),
	('HandIK_R',		handRoll, 'LoArmIK_R', F_WIR, L_ARMIK, NoBB),

	#
	('UpArmPTFK_L',		0.0, 'UpArmFK_L', 0, L_HELP, NoBB),
	('LoArmPTFK_L',		0.0, 'LoArmFK_L', 0, L_HELP, NoBB),
	('UpArmPTFK_R',		0.0, 'UpArmFK_R', 0, L_HELP, NoBB),
	('LoArmPTFK_R',		0.0, 'LoArmFK_R', 0, L_HELP, NoBB),

	('UpArmPTIK_L',		0.0, 'UpArmIK_L', 0, L_HELP, NoBB),
	('LoArmPTIK_L',		0.0, 'LoArmIK_L', 0, L_HELP, NoBB),
	('UpArmPTIK_R',		0.0, 'UpArmIK_R', 0, L_HELP, NoBB),
	('LoArmPTIK_R',		0.0, 'LoArmIK_R', 0, L_HELP, NoBB),

	# Pole target
	('ElbowPTIK_L',		0.0, 'Shoulder_L', F_WIR, L_ARMIK, NoBB),
	('ElbowPTIK_R',		0.0, 'Shoulder_R', F_WIR, L_ARMIK, NoBB),
	('ElbowLinkPTIK_L',	0.0, 'UpArmIK_L', F_RES, L_ARMIK, NoBB),
	('ElbowLinkPTIK_R',	0.0, 'UpArmIK_R', F_RES, L_ARMIK, NoBB),
	('ElbowPTFK_L',		0.0, 'UpArmFK_L', 0, L_HELP, NoBB),
	('ElbowPTFK_R',		0.0, 'UpArmFK_R', 0, L_HELP, NoBB),
]

#
#
#

limShoulder_L = (-16*D,40*D, -40*D,40*D,  -17*D,45*D)
limShoulder_R = (-16*D,40*D,  -40*D,40*D,  -17*40*D,45*D)

limUpArm_L = (-90*D,90*D, -100*D,45*D, -90*D,90*D)
limUpArm_R = (-90*D,90*D, -45*D,100*D, -90*D,90*D)

limLoArm_L = (-90*D,90*D, -180*D,45*D, -135*D,0)
limLoArm_R = (-90*D,90*D, -45*D,180*D, 0,135*D)

limHand_L = (-90*D,70*D, 0,0, -20*D,20*D)
limHand_R = (-90*D,70*D, 0,0, -20*D,20*D)

RmodUpArm = P_YZX
RmodLoArm = P_YXZ
RmodHand = P_ZYX

def ArmWritePoses(fp):
	addPoseBone(fp, 'Sternum', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'SternumTarget', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])


	# Shoulder
	addPoseBone(fp, 'Shoulder_L', 'MHEndCube01', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_L, (True, True, True)])])

	addPoseBone(fp, 'ShoulderPivot_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', C_LOCAL, 0.5, ['Rot', 'Shoulder_L', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'ShoulderUp_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addDeformIK(fp, 'ShoulderAim_L', 'SternumTarget', (90*D, 'ShoulderUp_L'))

	addPoseBone(fp, 'Scapula_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])


	addPoseBone(fp, 'Shoulder_R', 'MHEndCube01', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_R, (True, True, True)])])

	addPoseBone(fp, 'ShoulderPivot_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', C_LOCAL, 0.5, ['Rot', 'Shoulder_R', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'ShoulderUp_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addDeformIK(fp, 'ShoulderAim_R', 'SternumTarget', (90*D, 'ShoulderUp_L'))

	addPoseBone(fp, 'Scapula_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])


	'''
	addPoseBone(fp, 'Clavicle_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'Shoulder_L', 1])])

	addPoseBone(fp, 'Trapezeus-1_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'Shoulder_L', 1])])

	addPoseBone(fp, 'Trapezeus-2_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'LatDorsiTrg_L', 0])])

	addPoseBone(fp, 'Clavicle_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'Shoulder_R', 1])])

	addPoseBone(fp, 'Trapezeus-1_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'Shoulder_R', 1])])

	addPoseBone(fp, 'Trapezeus-2_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'LatDorsiTrg_R', 0])])
	'''


	# Shoulder deform
	addPoseBone(fp, 'Pectoralis_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'PectoralisTrg_L', 0])])

	addPoseBone(fp, 'LatDorsi_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'LatDorsiTrg_L', 0])])

	addPoseBone(fp, 'Deltoid_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Up', 'DeltoidTrg_L', 0])])

	addPoseBone(fp, 'ElbowBend_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'ElbowBendTrg_L', 0])])


	addPoseBone(fp, 'Pectoralis_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'PectoralisTrg_R', 0])])

	addPoseBone(fp, 'LatDorsi_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'LatDorsiTrg_R', 0])])

	addPoseBone(fp, 'Deltoid_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Up', 'DeltoidTrg_R', 0])])

	addPoseBone(fp, 'ElbowBend_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'ElbowBendTrg_R', 0])])


	# Arm deform
	addDeformLimb(fp, 'UpArm1_L', 'UpArmIK_L', (1,0,1), 'UpArmFK_L', (1,0,1), C_LOCAL, RmodUpArm, [])
	#addDeformIK2(fp, 'UpArm1_L', 'LoArmIK_L', 'LoArmFK_L', None, None, RmodUpArm, [])

	addPoseBone(fp, 'UpArm2_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpArm, 
		[('CopyScale', C_LOCAL, 0, ['ScaleIK', 'UpArmIK_L', (1,1,1), False])])

	addDeformLimb(fp, 'UpArm3_L', 'UpArmIK_L', (0,1,0), 'UpArmFK_L', (0,1,0), C_LOCAL, RmodUpArm, 
	#addDeformIK2(fp, 'UpArm3_L', 'LoArmIK_L', 'LoArmFK_L', (90*D, 'UpArmPTIK_L'), (90*D, 'UpArmPTFK_L'), RmodUpArm, 
		[('CopyScale', C_LOCAL, 0, ['ScaleIK', 'UpArmIK_L', (1,1,1), False])])

	addDeformLimb(fp, 'LoArm1_L', 'LoArmIK_L', (1,0,1), 'LoArmFK_L', (1,0,1), C_LOCAL, RmodLoArm, [])
	#addDeformIK2(fp, 'LoArm1_L', 'HandIK_L', 'HandFK_L', None, None, RmodLoArm, [])

	addPoseBone(fp, 'LoArm2_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodLoArm,
		[('CopyScale', C_LOCAL, 0, ['ScaleIK', 'LoArmIK_L', (1,1,1), False])])

	addDeformLimb(fp, 'LoArm3_L', 'LoArmIK_L', (0,1,0), 'LoArmFK_L', (0,1,0), C_LOCAL, RmodLoArm, [])
	#addDeformIK2(fp, 'LoArm3_L', 'HandIK_L', 'HandFK_L', (90*D, 'LoArmPTIK_L'), (90*D, 'LoArmPTFK_L'), [])

	addPoseBone(fp, 'LoArmFan_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), RmodLoArm,
		[('CopyRot', C_LOCAL, 0.5, ['Rot', 'LoArm1_L', (1,1,1), (0,0,0), False])])

	addDeformLimb(fp, 'Hand_L', 'HandIK_L', (1,1,1), 'HandFK_L', (1,1,1), 0, RmodHand, [])


	#addDeformLimb(fp, 'UpArm1_R', 'UpArmIK_R', (1,0,1), 'UpArmFK_R', (1,0,1), C_LOCAL, RmodUpArm, [])
	addDeformIK2(fp, 'UpArm1_R', 'LoArmIK_R', 'LoArmFK_R', None, None, RmodUpArm, []),

	addPoseBone(fp, 'UpArm2_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpArm,
		[('CopyScale', C_LOCAL, 0, ['ScaleIK', 'UpArmIK_R', (1,1,1), False])])

	#addDeformLimb(fp, 'UpArm3_R', 'UpArmIK_R', (0,1,0), 'UpArmFK_R', (0,1,0), C_LOCAL, RmodUpArm, [])
	addDeformIK2(fp, 'UpArm3_R', 'LoArmIK_R', 'LoArmFK_R', (90*D, 'UpArmPTIK_R'), (90*D, 'UpArmPTFK_R'), RmodUpArm, 
		[('CopyScale', C_LOCAL, 0, ['ScaleIK', 'UpArmIK_R', (1,1,1), False])])

	#addDeformLimb(fp, 'LoArm1_R', 'LoArmIK_R', (1,0,1), 'LoArmFK_R', (1,0,1), C_LOCAL, RmodLoArm, [])
	addDeformIK2(fp, 'LoArm1_R', 'HandIK_R', 'HandFK_R', None, None, RmodLoArm, []),

	addPoseBone(fp, 'LoArm2_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodLoArm, 
		[('CopyScale', C_LOCAL, 0, ['ScaleIK', 'LoArmIK_R', (1,1,1), False])])

	#addDeformLimb(fp, 'LoArm3_R', 'LoArmIK_R', (0,1,0), 'LoArmFK_R', (0,1,0), C_LOCAL, RmodLoArm, [])
	addDeformIK2(fp, 'LoArm3_R', 'HandIK_R', 'HandFK_R', (90*D, 'LoArmPTIK_R'), (90*D, 'LoArmPTFK_R'), RmodLoArm, []),

	addPoseBone(fp, 'LoArmFan_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), RmodLoArm,
		[('CopyRot', C_LOCAL, 0.5, ['Rot', 'LoArm1_R', (1,1,1), (0,0,0), False])])

	addDeformLimb(fp, 'Hand_R', 'HandIK_R', (1,1,1), 'HandFK_R', (1,1,1), 0, RmodHand, [])


	# FK
	addPoseBone(fp, 'UpArmFK_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpArm, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_L, (True, True, True)])])

	addPoseBone(fp, 'LoArmFK_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodLoArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArm_L, (True, True, True)])])

	addPoseBone(fp, 'HandFK_L', 'MHHand', 'FK_L', (0,0,0), (0,1,0), (1,1,1), (1,1,1), RmodHand,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_L, (True, True, True)]),
		 ('IK', 0, 1, ['IK', None, 2, None, (True, False,True)])])
		

	addPoseBone(fp, 'UpArmFK_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_R, (True, True, True)]),])

	addPoseBone(fp, 'LoArmFK_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodLoArm, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArm_R, (True, True, True)])])

	addPoseBone(fp, 'HandFK_R', 'MHHand', 'FK_R', (0,0,0), (0,1,0), (1,1,1), (1,1,1), RmodHand, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_R, (True, True, True)]),
		 ('IK', 0, 1, ['IK', None, 2, None, (True, False,True)])])


	# IK

	deltaElbow = 0.6*D

	addPoseBone(fp, 'UpArmIK_L', 'MHCircle025', 'IK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+RmodUpArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_L, (True, True, True)]),
		('StretchTo', 0, 0, ['ElbowIK', 'ElbowIK_L', 0])
		])

	addPoseBone(fp, 'LoArmIK_L', 'MHCircle025', 'IK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+RmodLoArm,
		[('IK', 0, 1, ['ArmIK', 'WristIK_L', 2, (pi-deltaElbow, 'ElbowPTIK_L'), (True, False,True)]),
		#('IK', 0, 0, ['HandIK', 'WristIK_L', 1, None, (True, False,True)]),
		('StretchTo', 0, 0, ['WristIK', 'WristIK_L', 0]),
		('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArm_L, (True, True, True)])
		])

	addPoseBone(fp, 'ElbowIK_L', 'MHCube025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_L', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_L', 'ONSURFACE']),
		])

	addPoseBone(fp, 'WristIK_L', 'MHHandCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_L', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_L', 'INSIDE']),
		('LimitDist', 0, 0, ['DistElbow', 'ElbowIK_L', 'ONSURFACE']),
		])

	addPoseBone(fp, 'HandIK_L', 'MHHand', 'IK_L', (1,1,1), (0,1,0), (1,1,1), (1,1,1), RmodHand, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_L, (True, True, True)]),
		('CopyLoc', 0, 1, ['WristLoc', 'WristIK_L', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, 1, ['WristRot', 'WristIK_L', (1,1,1), (0,0,0), False])
		])


	addPoseBone(fp, 'UpArmIK_R', 'MHCircle025', 'IK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+RmodUpArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_R, (True, True, True)]),
		('StretchTo', 0, 0, ['ElbowIK', 'ElbowIK_R', 0])
		])

	addPoseBone(fp, 'LoArmIK_R', 'MHCircle025', 'IK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+RmodLoArm,
		[('IK', 0, 1, ['ArmIK', 'WristIK_R', 2, (0+deltaElbow, 'ElbowPTIK_R'), (True, False,True)]),
		#('IK', 0, 0, ['HandIK', 'WristIK_R', 1, None, (True, False,True)]),
		('StretchTo', 0, 0, ['WristIK', 'WristIK_R', 0]),
		('LimitRot', C_OW_LOCAL, 0, ['LimitRot', limLoArm_R, (True, True, True)])
		])

	addPoseBone(fp, 'ElbowIK_R', 'MHCube025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_R', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_R', 'ONSURFACE']),
		])

	addPoseBone(fp, 'WristIK_R', 'MHHandCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_R', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_R', 'INSIDE']),
		('LimitDist', 0, 0, ['DistElbow', 'ElbowIK_R', 'ONSURFACE']),
		])

	addPoseBone(fp, 'HandIK_R', 'MHHand', 'IK_R', (1,1,1), (0,1,0), (1,1,1), (1,1,1), RmodHand, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_R, (True, True, True)]),
		('CopyLoc', 0, 1, ['WristLoc', 'WristIK_R', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, 1, ['WristRot', 'WristIK_R', (1,1,1), (0,0,0), False])
		])

	# Pole target

	addPoseBone(fp, 'ElbowPTIK_L', 'MHCube025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'ElbowLinkPTIK_L', None, 'IK_L', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'ElbowPTIK_L', 0])])

	addPoseBone(fp, 'ElbowPTIK_R', 'MHCube025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'ElbowLinkPTIK_R', None, 'IK_R', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'ElbowPTIK_R', 0])])

	return
	
#
#	ArmWriteActions(fp)
#

def ArmWriteActions(fp):
	return

#
#	ArmFKIKDrivers
#	(Bone, FK constraint, IK constraint, driver, channel, max)
#

ArmFKIKDrivers = [
	("UpArm1_L", True, ["FK"], ["IK"], "PArmIK_L", "LOC_X", 1.0),
	("UpArm3_L", True, ["FK"], ["IK"], "PArmIK_L", "LOC_X", 1.0),
	#("UpArm3_L", True, ["RotFK"], ["RotIK"], "PArmIK_L", "LOC_X", 1.0),
	("LoArm1_L", True, ["FK"], ["IK"], "PArmIK_L", "LOC_X", 1.0),
	("LoArm3_L", True, ["FK"], ["IK"], "PArmIK_L", "LOC_X", 1.0),
	#("LoArm3_L", True, ["RotFK"], ["RotIK"], "PArmIK_L", "LOC_X", 1.0),
	("Hand_L", True, ["RotFK"], ["RotIK"], "PArmIK_L", "LOC_X", 1.0),

	("UpArm1_R", True, ["FK"], ["IK"], "PArmIK_R", "LOC_X", 1.0),
	("UpArm3_R", True, ["FK"], ["IK"], "PArmIK_R", "LOC_X", 1.0),
	#("UpArm3_R", True, ["RotFK"], ["RotIK"], "PArmIK_R", "LOC_X", 1.0),
	("LoArm1_R", True, ["FK"], ["IK"], "PArmIK_R", "LOC_X", 1.0),
	("LoArm3_R", True, ["FK"], ["IK"], "PArmIK_R", "LOC_X", 1.0),
	#("LoArm3_R", True, ["RotFK"], ["RotIK"], "PArmIK_R", "LOC_X", 1.0),
	("Hand_R", True, ["RotFK"], ["RotIK"], "PArmIK_R", "LOC_X", 1.0),
]

#
#	ArmProperties
#	ArmPropDrivers
#

ArmStates = ['Whole_arm_FK', 'Whole_arm_IK', 'Locked_elbow,_forearm_FK', 'Locked_elbow,_forearm_IK']
ArmProperties = [
	('Left_arm_state', D_ENUM, ArmStates, ['name="Left_arm_state"', 'description=""'] ),
	('Right_arm_state', D_ENUM, ArmStates, ['name="Right_arm_state"', 'description=""'] ),
	('Left_arm_stretch', D_BOOL, False, ['name="Left_arm_stretch"', 'description=""'] ),
	('Right_arm_stretch', D_BOOL, False, ['name="Right_arm_stretch"', 'description=""'] ),
	('Left_hand_follows_wrist', D_BOOL, True, ['name="Left_hand_follows_wrist"', 'description=""'] ),
	('Right_hand_follows_wrist', D_BOOL, True, ['name="Right_hand_follows_wrist"', 'description=""'] ),
]

ArmRotDrivers = [('RotFK','x==0'), ('RotIK','x>=1')]
UpArmScaleDrivers = [('ScaleIK', '((x1)and(x2==1))or(x2>=2)')]

ArmPropDrivers = [
	('UpArm1_L', 'Left_arm_state', D_ENUM, ArmRotDrivers),
	('UpArm2_L',  ['Left_arm_stretch', 'Left_arm_state'], D_MULTIVAR, UpArmScaleDrivers),
	('UpArm3_L',  ['Left_arm_stretch', 'Left_arm_state'], D_MULTIVAR, UpArmScaleDrivers),
	('UpArm3_L', 'Left_arm_state', D_ENUM, ArmRotDrivers),
	('LoArm1_L', 'Left_arm_state', D_ENUM, ArmRotDrivers),
	('LoArm2_L', 'Left_arm_state', D_ENUM, [('ScaleIK', '(x==1)or(x==3)')]),
	('LoArm3_L', 'Left_arm_state', D_ENUM, ArmRotDrivers),
	('Hand_L', 'Left_arm_state', D_ENUM, ArmRotDrivers),

	('UpArm1_R', 'Right_arm_state', D_ENUM, ArmRotDrivers),
	('UpArm2_R',  ['Right_arm_stretch', 'Right_arm_state'], D_MULTIVAR, UpArmScaleDrivers),
	('UpArm3_R',  ['Right_arm_stretch', 'Right_arm_state'], D_MULTIVAR, UpArmScaleDrivers),
	('UpArm3_R', 'Right_arm_state', D_ENUM, ArmRotDrivers),
	('LoArm1_R', 'Right_arm_state', D_ENUM, ArmRotDrivers),
	('LoArm2_R', 'Right_arm_state', D_ENUM, [('ScaleIK', '(x==1)or(x==3)')]),
	('LoArm3_R', 'Right_arm_state', D_ENUM, ArmRotDrivers),
	('Hand_R', 'Right_arm_state', D_ENUM, ArmRotDrivers),

	('UpArmIK_L', 'Left_arm_state', D_ENUM, [('ElbowIK', 'x>=2')]),
	('LoArmIK_L', 'Left_arm_state', D_ENUM, [('ArmIK', 'x==1'), ('WristIK', 'x==3')]),
	('HandIK_L', 'Left_arm_state', D_ENUM, [('WristLoc', '(x==1)or(x==3)')]),

	('UpArmIK_R', 'Right_arm_state', D_ENUM, [('ElbowIK', 'x>=2')]),
	('LoArmIK_R', 'Right_arm_state', D_ENUM, [('ArmIK', 'x==1'), ('WristIK', 'x==3')]),
	('HandIK_R', 'Right_arm_state', D_ENUM, [('WristLoc', '(x==1)or(x==3)')]),

	('ElbowIK_L', 'Left_arm_stretch', D_BOOLINV, ['DistShoulder']),
	('WristIK_L',  ['Left_arm_stretch', 'Left_arm_state'], D_MULTIVAR, 
		[('DistElbow', '(not(x1))and(x2>=2)'),
		 ('DistShoulder', '(not(x1))and(x2==1)')]),

	('ElbowIK_R', 'Right_arm_stretch', D_BOOLINV, ['DistShoulder']),
	('WristIK_R',  ['Right_arm_stretch', 'Right_arm_state'], D_MULTIVAR, 
		[('DistElbow', '(not(x1))and(x2>=2)'),
		 ('DistShoulder', '(not(x1))and(x2==1)')]),

	('HandIK_L',  ['Left_arm_follows_wrist', 'Left_arm_state'], D_MULTIVAR, 
		[('WristRot', '(x1)and(x2!=3)')]),
	('HandIK_R',  ['Right_arm_follows_wrist', 'Right_arm_state'], D_MULTIVAR, 
		[('WristRot', '(x1)and(x2!=3)')]),

]


#
#	ArmDeformDrivers
#	(Bone, constraint, driver, rotdiff, keypoints)
#

ArmDeformDrivers = []
'''
	("Deltoid_L", "Up", "min(a,3*(s-0.5))", 
		 [("a", "UpArm1_L", "BendArmUp_L"), ("s", "Shoulder_L", "BendShoulderUp_L")], 
			[(0,1), (90*D,1), (110*D,0)]),
	("Deltoid_R", "Up", "min(a,3*(s-0.5))", 
		 [("a", "UpArm1_R", "BendArmUp_R"), ("s", "Shoulder_R", "BendShoulderUp_R")], 
			[(0,1), (90*D,1), (110*D,0)])
]
'''
#
#	ArmShapeDrivers
#	Shape : (driver, rotdiff, keypoints)
#

ArmShapeDrivers = {}
'''
	'BicepFlex_L' : ( 'LoArm1_L', 'BendLoArmForward_L',  [(0,1), (90*D,0)] ),
	'BicepFlex_R' : ( 'LoArm1_R', 'BendLoArmForward_R',  [(0,1), (90*D,0)] ),
}
'''

#
#	ArmProcess
#	(bone, axis, angle)
#

ArmProcess = [
	("LoArm3_L", "Z", -20*D),
	("LoArm3_R", "Z", 20*D),
	("LoArm1_L", "Z", -20*D),
	("LoArm1_R", "Z", 20*D),
]	

ArmSnaps = [
	("LoArmFK_L", "LoArm3_L", 'Both'),
	("LoArmIK_L", "LoArm3_L", 'Both'),
	("HandFK_L", "Hand_L", 'Both'),
	("HandIK_L", "Hand_L", 'Both'),

	("LoArmFK_R", "LoArm3_R", 'Both'),
	("LoArmIK_R", "LoArm3_R", 'Both'),
	("HandFK_R", "Hand_R", 'Both'),
	("HandIK_R", "Hand_R", 'Both'),
]

ArmParents = [
]

ArmSelects = []

ArmRolls = []


