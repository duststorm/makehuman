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

	('ShoulderEnd_L',		'r-shoulder', ('r-shoulder', yunit)),
	('ShoulderEnd_R',		'l-shoulder', ('l-shoulder', yunit)),
	('ArmLoc_L',			'r-shoulder', ('r-shoulder', yunit)),
	('ArmLoc_R',			'l-shoulder', ('l-shoulder', yunit)),

	('ShoulderTwist_L',		'r-shoulder-aim', 'r-uparm1'),
	('ShoulderTwist_R',		'l-shoulder-aim', 'l-uparm1'),

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
	('UpArm_L',				'r-shoulder', 'r-elbow'),
	('UpArm1_L',			'r-shoulder', 'r-uparm1'),
	('UpArm2_L',			'r-uparm1', 'r-uparm2'),
	('UpArm3_L',			'r-uparm2', 'r-elbow'),
	('Elbow_L',				'r-elbow', ('r-elbow',yunit)),
	('LoArm_L',				'r-elbow', 'r-hand'),
	('LoArm1_L',			'r-elbow', 'r-loarm1'),
	('LoArm2_L',			'r-loarm1', 'r-loarm2'),
	('LoArm3_L',			'r-loarm2', 'r-hand'),
	('LoArmFan_L',			'r-elbow', 'r-loarm-fan'),
	('Wrist_L',				'r-hand', 'hand_L_tail'),
	('Hand_L',				'r-hand', 'hand_L_tail'),

	('UpArm_R',				'l-shoulder', 'l-elbow'),
	('UpArm1_R',			'l-shoulder', 'l-uparm1'),
	('UpArm2_R',			'l-uparm1', 'l-uparm2'),
	('UpArm3_R',			'l-uparm2', 'l-elbow'),
	('Elbow_R',				'l-elbow', ('l-elbow',yunit)),
	('LoArm_R',				'l-elbow', 'l-hand'),
	('LoArm1_R',			'l-elbow', 'l-loarm1'),
	('LoArm2_R',			'l-loarm1', 'l-loarm2'),
	('LoArm3_R',			'l-loarm2', 'l-hand'),
	('LoArmFan_R',			'l-elbow', 'l-loarm-fan'),
	('Wrist_R',				'l-hand', 'hand_R_tail'),
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

	# Pole Targets

	('UpArmPT_L',			('r-shoulder', yunit), ('r-shoulder', ybis)),
	('LoArmPT_L',			('r-elbow', yunit), ('r-elbow', ybis)),
	('UpArmPT_R',			('l-shoulder', yunit), ('l-shoulder', ybis)),
	('LoArmPT_R',			('l-elbow', yunit), ('l-elbow', ybis)),

	('ElbowPT_L',			'r-elbow-pt', ('r-elbow-pt', yunit)),
	('ElbowPT_R',			'l-elbow-pt', ('l-elbow-pt', yunit)),
	('ElbowLinkPT_L',		'r-elbow', 'r-elbow-pt'),
	('ElbowLinkPT_R',		'l-elbow', 'l-elbow-pt'),
]

#upArmRoll = 1.69297
#loArmRoll = 90*D
#handRoll = 1.22173

upArmRoll = 0.0
loArmRoll = 0.0
handRoll = 0.0

L_LSHOULDER = L_LARMFK+L_LARMIK+L_SPINEFK+L_SPINEIK
L_RSHOULDER = L_RARMFK+L_RARMIK+L_SPINEFK+L_SPINEIK

'''
	('Clavicle_L',			0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	('Trapezeus-1_L',		0.0, 'Spine2', F_DEF, L_DEF, NoBB),
	('Trapezeus-2_L',		0.0, 'Spine2', F_DEF, L_DEF, NoBB),

	('Clavicle_R',			0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	('Trapezeus-1_R',		0.0, 'Spine2', F_DEF, L_DEF, NoBB),
	('Trapezeus-2_R',		0.0, 'Spine2', F_DEF, L_DEF, NoBB),
'''

ArmControlArmature = [
	('Sternum',				0.0, 'Spine3', 0, L_HELP, NoBB),
	('SternumTarget',		0.0, 'Sternum', 0, L_HELP, NoBB),

	# Shoulder
	('Shoulder_L',			0.0, 'Sternum', F_WIR+F_DEF, L_LSHOULDER, NoBB),
	('Shoulder_R',			0.0, 'Sternum', F_WIR+F_DEF, L_RSHOULDER, NoBB),
	('ShoulderEnd_L',		0.0, 'Shoulder_L', 0, L_HELP, NoBB),
	('ShoulderEnd_R',		0.0, 'Shoulder_R', 0, L_HELP, NoBB),
	('ArmLoc_L',			0.0, 'ShoulderEnd_L', F_NOROT, L_HELP, NoBB),
	('ArmLoc_R',			0.0, 'ShoulderEnd_R', F_NOROT, L_HELP, NoBB),

	# Arm
	('UpArm_L',			upArmRoll, 'ArmLoc_L', F_WIR, L_LARMFK, NoBB),
	('Elbow_L',			0, Master, F_WIR, L_LARMFK+L_LARMIK, NoBB),
	('LoArm_L',			loArmRoll, 'UpArm_L', F_WIR, L_LARMFK, NoBB),
	('Wrist_L',			handRoll, Master, F_WIR, L_LARMIK, NoBB),
	('Hand_L',			handRoll, 'LoArm_L', F_CON+F_WIR, L_LARMFK+L_LARMIK, NoBB),
	('UpArm_R',			-upArmRoll, 'ArmLoc_R', F_WIR, L_RARMFK, NoBB),
	('Elbow_R',			0, Master, F_WIR, L_RARMFK+L_RARMIK, NoBB),
	('LoArm_R',			-loArmRoll, 'UpArm_R', F_WIR, L_RARMFK, NoBB),
	('Wrist_R',			handRoll, Master, F_WIR, L_RARMIK, NoBB),
	('Hand_R',			-handRoll, 'LoArm_R', F_CON+F_WIR, L_RARMFK+L_RARMIK, NoBB),

	#
	('UpArmPT_L',		0.0, 'UpArm_L', 0, L_HELP, NoBB),
	('LoArmPT_L',		0.0, 'LoArm_L', 0, L_HELP, NoBB),
	('UpArmPT_R',		0.0, 'UpArm_R', 0, L_HELP, NoBB),
	('LoArmPT_R',		0.0, 'LoArm_R', 0, L_HELP, NoBB),

	# Pole target
	('ElbowPT_L',		0.0, 'Shoulder_L', F_WIR, L_LARMIK, NoBB),
	('ElbowPT_R',		0.0, 'Shoulder_R', F_WIR, L_RARMIK, NoBB),
	('ElbowLinkPT_L',	0.0, 'UpArm_L', F_RES, L_LARMIK, NoBB),
	('ElbowLinkPT_R',	0.0, 'UpArm_R', F_RES, L_RARMIK, NoBB),
]

ArmDeformArmature = [
	('Sternum',				0.0, 'Spine3', 0, L_HELP, NoBB),

	# Shoulder
	('Shoulder_L',			0.0, 'Sternum', F_DEF, L_LSHOULDER+L_MAIN, NoBB),
	('ShoulderPivot_L',		0.0, 'Sternum', 0, L_HELP, NoBB),
	('ShoulderUp_L',		0.0, 'ShoulderPivot_L', 0, L_HELP, NoBB),
	('ShoulderAim_L',		0.0, 'ShoulderPivot_L', 0, L_HELP, NoBB),
	('Scapula_L',			0.0, 'ShoulderAim_L', F_DEF, L_DEF, NoBB),

	('Shoulder_R',			0.0, 'Sternum', F_DEF, L_RSHOULDER+L_MAIN, NoBB),
	('ShoulderPivot_R',		0.0, 'Sternum', 0, L_HELP, NoBB),
	('ShoulderUp_R',		0.0, 'ShoulderPivot_R', 0, L_HELP, NoBB),
	('ShoulderAim_R',		0.0, 'ShoulderPivot_R', 0, L_HELP, NoBB),
	('Scapula_R',			0.0, 'ShoulderAim_R', F_DEF, L_DEF, NoBB),

	('ArmLoc_L',			0.0, 'Shoulder_L', F_NOROT, L_HELP, NoBB),
	('ArmLoc_R',			0.0, 'Shoulder_R', F_NOROT, L_HELP, NoBB),

	('ShoulderTwist_L',		0.0, 'ShoulderAim_L', 0, L_DEF, NoBB),
	('ShoulderTwist_R',		0.0, 'ShoulderAim_R', 0, L_DEF, NoBB),

	# Arm deform
	('UpArm1_L',		upArmRoll, 'ArmLoc_L', F_DEF, L_DEF, NoBB),
	('UpArm2_L',		upArmRoll, 'UpArm1_L', F_DEF+F_CON, L_MAIN,(1,1,5) ),
	('UpArm3_L',		upArmRoll, 'UpArm2_L', F_DEF+F_CON, L_MAIN, NoBB),
	('LoArm1_L',		loArmRoll, 'UpArm3_L', F_DEF, L_DEF, NoBB),
	('LoArm2_L',		loArmRoll, 'LoArm1_L', F_DEF+F_CON, L_MAIN, (1,1,5) ),
	('LoArm3_L',		loArmRoll, 'LoArm2_L', F_DEF+F_CON, L_DEF, NoBB),
	('LoArmFan_L',		loArmRoll, 'UpArm3_L', F_DEF, L_DEF, NoBB),
	('Hand_L',			handRoll, 'LoArm3_L', F_DEF, L_MAIN, NoBB),

	('UpArm1_R',		upArmRoll, 'ArmLoc_R', F_DEF, L_DEF, NoBB),
	('UpArm2_R',		upArmRoll, 'UpArm1_R', F_DEF+F_CON, L_MAIN,(1,1,5) ),
	('UpArm3_R',		upArmRoll, 'UpArm2_R', F_DEF+F_CON, L_MAIN, NoBB),
	('LoArm1_R',		loArmRoll, 'UpArm3_R', F_DEF, L_DEF, NoBB),
	('LoArm2_R',		loArmRoll, 'LoArm1_R', F_DEF+F_CON, L_MAIN, (1,1,5) ),
	('LoArm3_R',		loArmRoll, 'LoArm2_R', F_DEF+F_CON, L_DEF, NoBB),
	('LoArmFan_R',		loArmRoll, 'UpArm3_R', F_DEF, L_DEF, NoBB),
	('Hand_R',			handRoll, 'LoArm3_R', F_DEF, L_MAIN, NoBB),
]
"""
	# Rotation diffs
	('BendArmDown_L',		90*D, 'Shoulder_L', 0, L_HELP, NoBB),
	('BendArmDown_R',		-90*D, 'Shoulder_R', 0, L_HELP, NoBB),
	('BendArmUp_L',			-90*D, 'Shoulder_L', 0, L_HELP, NoBB),
	('BendArmUp_R',			90*D, 'Shoulder_R', 0, L_HELP, NoBB),
	('BendShoulderUp_L',	-90*D, 'Spine3', 0, L_HELP, NoBB),
	('BendShoulderUp_R',	90*D, 'Spine3', 0, L_HELP, NoBB),
	('BendLoArmForward_L',	0, 'UpArm3_L', 0, L_HELP, NoBB),
	('BendLoArmForward_R',	0, 'UpArm3_R', 0, L_HELP, NoBB),

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
]
"""
#
#
#

limShoulder_L = (-16*D,40*D, -40*D,40*D,  -45*D,17*D)
limShoulder_R = (-16*D,40*D,  -40*D,40*D,  -17*D,45*D)

limUpArm_L = (-90*D,90*D, -100*D,45*D, -90*D,90*D)
limUpArm_R = (-90*D,90*D, -45*D,100*D, -90*D,90*D)

limLoArm_L = (-90*D,90*D, -180*D,45*D, -135*D,0)
limLoArm_R = (-90*D,90*D, -45*D,180*D, 0,135*D)

limHand_L = (-90*D,70*D, 0,0, -20*D,20*D)
limHand_R = (-90*D,70*D, 0,0, -20*D,20*D)

RmodUpArm = P_YXZ
RmodLoArm = P_YXZ
RmodHand = P_YXZ

#RmodUpArm = P_XZY
#RmodLoArm = P_XZY
#RmodHand = P_XYZ

#
#	ArmControlPoses(fp):
#

def ArmControlPoses(fp):
	addPoseBone(fp, 'Sternum', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'SternumTarget', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Shoulder
	addPoseBone(fp, 'Shoulder_L', 'MHEndCube01', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_L, (True, True, True)])])

	addPoseBone(fp, 'Shoulder_R', 'MHEndCube01', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_R, (True, True, True)])])

	addPoseBone(fp, 'ArmLoc_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, 1, ['Shoulder', 'ShoulderEnd_L', (1,1,1), (0,0,0), False]),
		 ('CopyRot', 0, 0, ['Root', 'BendRoot', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'ArmLoc_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, 1, ['Shoulder', 'ShoulderEnd_R', (1,1,1), (0,0,0), False]),
		 ('CopyRot', 0, 0, ['Root', 'BendRoot', (1,1,1), (0,0,0), False])])



	# Arm
	deltaElbow = 0.6*D

	addPoseBone(fp, 'UpArm_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpArm, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_L, (True, True, True)]),
		 ('StretchTo', 0, 0, ['Elbow', 'Elbow_L', 0]),
		])

	addPoseBone(fp, 'Elbow_L', 'MHCube025', 'FK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), RmodLoArm, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_L', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_L', 'ONSURFACE']),
		])

	addPoseBone(fp, 'LoArm_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodLoArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArm_L, (True, True, True)]),
		 ('IK', 0, 0, ['ArmIK', 'Wrist_L', 2, (pi-deltaElbow, 'ElbowPT_L'), (True, False,True)]),
		 ('StretchTo', 0, 0, ['Wrist', 'Wrist_L', 0]),
		])

	addPoseBone(fp, 'Wrist_L', 'MHHandCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), RmodHand, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_L', (1,1,1), (1,1,1), (1,1,1)]),
		 ('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_L', 'INSIDE']),
		 ('LimitDist', 0, 0, ['DistElbow', 'Elbow_L', 'ONSURFACE']),
		])

	addPoseBone(fp, 'Hand_L', 'MHHand', 'FK_L', (0,0,0), (0,1,0), (1,1,1), (1,1,1), RmodHand,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_L, (True, True, True)]),
		 ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,True)]),
		 ('CopyLoc', 0, 0, ['WristLoc', 'Wrist_L', (1,1,1), (0,0,0), False]),
		 ('CopyRot', 0, 0, ['WristRot', 'Wrist_L', (1,1,1), (0,0,0), False])
		])
		
	addPoseBone(fp, 'ElbowPT_L', 'MHCube025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'ElbowLinkPT_L', None, 'IK_L', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'ElbowPT_L', 0])])



	addPoseBone(fp, 'UpArm_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpArm, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_R, (True, True, True)]),
		 ('StretchTo', 0, 0, ['Elbow', 'Elbow_R', 0]),
		])

	addPoseBone(fp, 'Elbow_R', 'MHCube025', 'FK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), RmodLoArm, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_R', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_R', 'ONSURFACE']),
		])

	addPoseBone(fp, 'LoArm_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodLoArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArm_R, (True, True, True)]),
		 ('IK', 0, 0, ['ArmIK', 'Wrist_R', 2, (deltaElbow, 'ElbowPT_R'), (True, False,True)]),
		 ('StretchTo', 0, 0, ['Wrist', 'Wrist_R', 0]),
		])

	addPoseBone(fp, 'Wrist_R', 'MHHandCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), RmodHand, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_R', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_R', 'INSIDE']),
		('LimitDist', 0, 0, ['DistElbow', 'Elbow_R', 'ONSURFACE']),
		])

	addPoseBone(fp, 'Hand_R', 'MHHand', 'FK_R', (0,0,0), (0,1,0), (1,1,1), (1,1,1), RmodHand,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_R, (True, True, True)]),
		 ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,True)]),
		 ('CopyLoc', 0, 0, ['WristLoc', 'Wrist_R', (1,1,1), (0,0,0), False]),
		 ('CopyRot', 0, 0, ['WristRot', 'Wrist_R', (1,1,1), (0,0,0), False])
		])

	addPoseBone(fp, 'ElbowPT_R', 'MHCube025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'ElbowLinkPT_R', None, 'IK_R', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'ElbowPT_R', 0])])

	return
	
#
#	ArmDeformPoses(fp):
#

def ArmDeformPoses(fp):
	copyDeform(fp, 'Sternum', 0, U_LOC+U_ROT, None, [])
	copyDeform(fp, 'Shoulder_L', RmodUpArm, U_LOC+U_ROT, 'MHDefShoulder', [])
	copyDeform(fp, 'Shoulder_R', RmodUpArm, U_LOC+U_ROT, 'MHDefShoulder', [])
	copyDeform(fp, 'ArmLoc_L', 0, U_ROT, None, [])
	copyDeform(fp, 'ArmLoc_R', 0, U_ROT, None, [])
	
	# Shoulder	
	addPoseBone(fp, 'ShoulderPivot_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', C_LOCAL, 0.5, ['Rot', 'Shoulder_L', (1,1,1), (0,0,0), False])])
	
	addPoseBone(fp, 'ShoulderUp_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	
	addDeformIK(fp, 'ShoulderAim_L', 'SternumTarget', (-90*D, 'ShoulderUp_L'))
	
	addPoseBone(fp, 'Scapula_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	
	
	addPoseBone(fp, 'ShoulderPivot_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', C_LOCAL, 0.5, ['Rot', 'Shoulder_R', (1,1,1), (0,0,0), False])])
	
	addPoseBone(fp, 'ShoulderUp_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	
	addDeformIK(fp, 'ShoulderAim_R', 'SternumTarget', (-90*D, 'ShoulderUp_L'))
	
	addPoseBone(fp, 'Scapula_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])


	addPoseBone(fp, 'ShoulderTwist_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), RmodUpArm,
		[('CopyRot', C_LOCAL, 0.5, ['Rot', 'UpArm_L', (1,1,1), (0,0,0), False]),
		 ('StretchTo', C_DEFRIG, 1, ['Stretch', 'UpArm2_L', 0])])

	addPoseBone(fp, 'ShoulderTwist_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), RmodUpArm,
		[('CopyRot', C_LOCAL, 0.5, ['Rot', 'UpArm_R', (1,1,1), (0,0,0), False]),
		 ('StretchTo', C_DEFRIG, 1, ['Stretch', 'UpArm2_R', 0])])	
	
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
	
	
	# Shoulder deform
	addPoseBone(fp, 'Pectoralis_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'PectoralisTrg_L', 0])])
	
	addPoseBone(fp, 'LatDorsi_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'LatDorsiTrg_L', 0])])
	
	addPoseBone(fp, 'Deltoid_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_DEFRIG, 1, ['Up', 'DeltoidTrg_L', 0])])
	
	addPoseBone(fp, 'ElbowBend_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'ElbowBendTrg_L', 0])])
	
	
	addPoseBone(fp, 'Pectoralis_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'PectoralisTrg_R', 0])])
	
	addPoseBone(fp, 'LatDorsi_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'LatDorsiTrg_R', 0])])
	
	addPoseBone(fp, 'Deltoid_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_DEFRIG, 1, ['Up', 'DeltoidTrg_R', 0])])
	
	addPoseBone(fp, 'ElbowBend_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'ElbowBendTrg_R', 0])])
	'''
	
	
	# Arm deform
	copyDeformPartial(fp, 'UpArm1_L', 'UpArm_L', (1,0,1), RmodUpArm, U_LOC+U_ROT+U_SCALE, None, 
		[('CopyRot', C_LOCAL, 0.5, ['RotY', 'UpArm_L', (0,1,0), (0,0,0), False])])
	
	copyDeformPartial(fp, 'UpArm2_L', 'UpArm_L', (1,1,1), RmodUpArm, U_SCALE, 'MHDefUpArm2', [])
		
	copyDeformPartial(fp, 'UpArm3_L', 'UpArm_L', (1,1,1), RmodUpArm, U_SCALE, 'MHDefUpArm3',
		[('CopyRot', C_LOCAL, 0.5, ['RotY', 'UpArm_L', (0,1,0), (0,0,0), False])])

	copyDeformPartial(fp, 'LoArm1_L', 'LoArm_L', (1,0,1), RmodLoArm, U_LOC+U_ROT+U_SCALE, None, [])
	
	copyDeformPartial(fp, 'LoArm2_L', 'LoArm_L', (1,1,1), RmodLoArm, U_SCALE, 'MHDefArm', [])
		
	copyDeformPartial(fp, 'LoArm3_L', 'LoArm_L', (0,1,0), RmodLoArm, U_ROT+U_SCALE, None, [])
		
	addPoseBone(fp, 'LoArmFan_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), RmodLoArm,
		[('CopyRot', C_LOCAL, 0.5, ['Rot', 'LoArm_L', (1,1,1), (0,0,0), False])])
	
	copyDeform(fp, 'Hand_L', RmodHand, U_LOC+U_ROT, 'MHDefHand', [])


	copyDeformPartial(fp, 'UpArm1_R', 'UpArm_R', (1,0,1), RmodUpArm, U_LOC+U_ROT+U_SCALE, None, 
		[('CopyRot', C_LOCAL, 0.5, ['RotY', 'UpArm_R', (0,1,0), (0,0,0), False])])
	
	copyDeformPartial(fp, 'UpArm2_R', 'UpArm_R', (1,1,1), RmodUpArm, U_SCALE, 'MHDefUpArm2', [])
		
	copyDeformPartial(fp, 'UpArm3_R', 'UpArm_R', (1,1,1), RmodUpArm, U_SCALE, 'MHDefUpArm3',
		[('CopyRot', C_LOCAL, 0.5, ['RotY', 'UpArm_R', (0,1,0), (0,0,0), False])])

	copyDeformPartial(fp, 'LoArm1_R', 'LoArm_R', (1,0,1), RmodLoArm, U_LOC+U_ROT+U_SCALE, None, [])
	
	copyDeformPartial(fp, 'LoArm2_R', 'LoArm_R', (1,1,1), RmodLoArm, U_SCALE, 'MHDefArm', [])
		
	copyDeformPartial(fp, 'LoArm3_R', 'LoArm_R', (0,1,0), RmodLoArm, U_ROT+U_SCALE, None, [])
		
	addPoseBone(fp, 'LoArmFan_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), RmodLoArm,
		[('CopyRot', C_LOCAL, 0.5, ['Rot', 'LoArm_R', (1,1,1), (0,0,0), False])])
	
	copyDeform(fp, 'Hand_R', RmodHand, U_LOC+U_ROT, 'MHDefHand', [])

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
	("UpArm_L", True, [], [], "PArmIK_L", "LOC_X", 1.0),
	("LoArm_L", True, [], ["ArmIK"], "PArmIK_L", "LOC_X", 1.0),
	("Hand_L", True, ["FreeIK"], ["WristLoc", "WristRot"], "PArmIK_L", "LOC_X", 1.0),

	("UpArm_R", True, [], [], "PArmIK_R", "LOC_X", 1.0),
	("LoArm_R", True, [], ["ArmIK"], "PArmIK_R", "LOC_X", 1.0),
	("Hand_R", True, ["FreeIK"], ["WristLoc", "WristRot"], "PArmIK_R", "LOC_X", 1.0),
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


