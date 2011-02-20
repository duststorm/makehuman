""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
Arm bone definitions 

"""

import mhx_rig
from mhx_rig import *

prcArmTrg	= 0.35

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

	('r-armtrg',			'l', ((1-prcArmTrg, 'r-shoulder'), (prcArmTrg, 'r-elbow'))),
	('l-armtrg',			'l', ((1-prcArmTrg, 'l-shoulder'), (prcArmTrg, 'l-elbow'))),
	('r-uparmrot',			'l', ((1-prcArmTrg/2, 'r-shoulder'), (prcArmTrg/2, 'r-elbow'))),
	('l-uparmrot',			'l', ((1-prcArmTrg/2, 'l-shoulder'), (prcArmTrg/2, 'l-elbow'))),

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
	('r-latdorsi',			'v', 4432),
	('r-deltoid',			'v', 2854),
	('r-armpit',			'v', 4431),

	('l-pectoralis',		'v', 10410),
	('l-latdorsi',			'v', 9995),
	('l-deltoid'	,		'v', 10820),
	('l-armpit',			'v', 9996),

	('r-trapezeus-1',		'v', 2584),
	('r-trapezeus-2',		'v', 3633),
	('l-trapezeus-1',		'v', 11024),
	('l-trapezeus-2',		'v', 10159),

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
	('ArmTrg_L',			'r-shoulder', 'r-armtrg'),
	('ArmPit_L',			'r-armpit', 'r-armtrg'),
	('Pectoralis_L',		'r-pectoralis', 'r-armtrg'),
	('Trapezeus_L',			'r-trapezeus-2', 'r-armtrg'),
	#('LatDorsi_L',			'r-latdorsi', 'r-armtrg'),
	('Deltoid_L',			'r-deltoid', 'r-armtrg'),

	('ArmTrg_R',			'l-shoulder', 'l-armtrg'),
	('ArmPit_R',			'l-armpit', 'l-armtrg'),
	('Pectoralis_R',		'l-pectoralis', 'l-armtrg'),
	('Trapezeus_R',			'l-trapezeus-2', 'l-armtrg'),
	#('LatDorsi_R',			'l-latdorsi', 'l-armtrg'),
	('Deltoid_R',			'l-deltoid', 'l-armtrg'),

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
	('BendArmForward_L',	'r-shoulder', ('r-shoulder', (0,0,1))),
	('BendArmForward_R',	'l-shoulder', ('l-shoulder', (0,0,1))),
	('BendArmBack_L',		'r-shoulder', ('r-shoulder', (0,0,-1))),
	('BendArmBack_R',		'l-shoulder', ('l-shoulder', (0,0,-1))),

	('BendShoulderUp_L',	'r-shoulder-head', ('r-shoulder-head', (0,1,0))),
	('BendShoulderUp_R',	'l-shoulder-head', ('l-shoulder-head', (0,1,0))),
	('BendLoArmForward_L',	'r-elbow', ('r-elbow', (0,0,1))),
	('BendLoArmForward_R',	'l-elbow', ('l-elbow', (0,0,1))),

	# Pole Targets

	('UpArmRot_L',			'r-shoulder', 'r-uparmrot'),
	('UpArmDir_L',			'r-uparm1', ('r-uparm1', yunit)),
	('UpArm1PT_L',			('r-uparm1', yunit), ('r-uparm1', ybis)),
	('UpArm2PT_L',			('r-uparm2', yunit), ('r-uparm2', ybis)),
	('LoArmPT_L',			('r-loarm2', yunit), ('r-loarm2', ybis)),

	('UpArmRot_R',			'l-shoulder', 'l-uparmrot'),
	('UpArmDir_R',			'l-uparm1', ('l-uparm1', yunit)),
	('UpArm1PT_R',			('l-uparm1', yunit), ('l-uparm1', ybis)),
	('UpArm2PT_R',			('l-uparm2', yunit), ('l-uparm2', ybis)),
	('LoArmPT_R',			('l-loarm2', yunit), ('l-loarm2', ybis)),

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
	('ArmTrg_L',		0.0, 'ArmLoc_L', 0, L_HELP, NoBB),
	('UpArmRot_L',		0.0, 'ArmLoc_L', F_WIR, L_LARMFK+L_LARMIK, NoBB),
	('UpArm1PT_L',		0.0, 'UpArmRot_L', 0, L_HELP, NoBB),
	('UpArm2PT_L',		0.0, 'UpArm_L', 0, L_HELP, NoBB),
	('LoArmPT_L',		0.0, 'LoArm_L', 0, L_HELP, NoBB),

	('ArmTrg_R',		0.0, 'ArmLoc_R', 0, L_HELP, NoBB),
	('UpArmRot_R',		0.0, 'ArmLoc_R', F_WIR, L_RARMFK+L_RARMIK, NoBB),
	('UpArm1PT_R',		0.0, 'UpArmRot_R', 0, L_HELP, NoBB),
	('UpArm2PT_R',		0.0, 'UpArm_R', 0, L_HELP, NoBB),
	('LoArmPT_R',		0.0, 'LoArm_R', 0, L_HELP, NoBB),

	# Pole target
	('ElbowPT_L',		0.0, 'Shoulder_L', F_WIR, L_LARMIK, NoBB),
	('ElbowPT_R',		0.0, 'Shoulder_R', F_WIR, L_RARMIK, NoBB),
	('ElbowLinkPT_L',	0.0, 'UpArm_L', F_RES, L_LARMIK, NoBB),
	('ElbowLinkPT_R',	0.0, 'UpArm_R', F_RES, L_RARMIK, NoBB),

	# Rotation diffs
	('BendArmDown_L',		90*D, 'Shoulder_L', 0, L_HELP, NoBB),
	('BendArmDown_R',		-90*D, 'Shoulder_R', 0, L_HELP, NoBB),
	('BendArmUp_L',			-90*D, 'Shoulder_L', 0, L_HELP, NoBB),
	('BendArmUp_R',			90*D, 'Shoulder_R', 0, L_HELP, NoBB),
	('BendArmForward_L',	0*D, 'Shoulder_L', 0, L_HELP, NoBB),
	('BendArmForward_R',	0*D, 'Shoulder_R', 0, L_HELP, NoBB),
	('BendArmBack_L',		0*D, 'Shoulder_L', 0, L_HELP, NoBB),
	('BendArmBack_R',		0*D, 'Shoulder_R', 0, L_HELP, NoBB),

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
	('UpArm1_L',		upArmRoll, 'ArmLoc_L', F_DEF, L_MAIN, NoBB),
	('UpArm2_L',		upArmRoll, 'UpArm1_L', F_DEF+F_CON, L_MAIN,(0,0,5) ),
	('UpArm3_L',		upArmRoll, 'UpArm2_L', F_DEF+F_CON, L_MAIN, NoBB),
	('LoArm1_L',		loArmRoll, 'UpArm3_L', F_DEF, L_MAIN, NoBB),
	('LoArm2_L',		loArmRoll, 'LoArm1_L', F_DEF+F_CON, L_MAIN, (0,0,5) ),
	('LoArm3_L',		loArmRoll, 'LoArm2_L', F_DEF+F_CON, L_MAIN, NoBB),
	('LoArmFan_L',		loArmRoll, 'UpArm3_L', F_DEF, L_MAIN, NoBB),
	('Hand_L',			handRoll, 'LoArm3_L', F_DEF, L_MAIN, NoBB),

	('UpArm1_R',		upArmRoll, 'ArmLoc_R', F_DEF, L_MAIN, NoBB),
	('UpArm2_R',		upArmRoll, 'UpArm1_R', F_DEF+F_CON, L_MAIN,(0,0,5) ),
	('UpArm3_R',		upArmRoll, 'UpArm2_R', F_DEF+F_CON, L_MAIN, NoBB),
	('LoArm1_R',		loArmRoll, 'UpArm3_R', F_DEF, L_MAIN, NoBB),
	('LoArm2_R',		loArmRoll, 'LoArm1_R', F_DEF+F_CON, L_MAIN, (0,0,5) ),
	('LoArm3_R',		loArmRoll, 'LoArm2_R', F_DEF+F_CON, L_MAIN, NoBB),
	('LoArmFan_R',		loArmRoll, 'UpArm3_R', F_DEF, L_MAIN, NoBB),
	('Hand_R',			handRoll, 'LoArm3_R', F_DEF, L_MAIN, NoBB),

	# Shoulder deform
	('ArmPit_L',			0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	('Pectoralis_L',		0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	('Trapezeus_L',			0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	#('LatDorsi_L',			0.0, 'Spine1', F_DEF, L_DEF, NoBB),
	('Deltoid_L',			0.0, 'Shoulder_L', F_DEF, L_DEF, NoBB),

	('ArmPit_R',			0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	('Pectoralis_R',		0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	('Trapezeus_R',			0.0, 'Spine3', F_DEF, L_DEF, NoBB),
	#('LatDorsi_R',			0.0, 'Spine1', F_DEF, L_DEF, NoBB),
	('Deltoid_R',			0.0, 'Shoulder_R', F_DEF, L_DEF, NoBB),

]
"""
	('BendShoulderUp_L',	-90*D, 'Spine3', 0, L_HELP, NoBB),
	('BendShoulderUp_R',	90*D, 'Spine3', 0, L_HELP, NoBB),
	('BendLoArmForward_L',	0, 'UpArm3_L', 0, L_HELP, NoBB),
	('BendLoArmForward_R',	0, 'UpArm3_R', 0, L_HELP, NoBB),

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

limShoulder_L = (-16*D,40*D, -40*D,40*D,  -45*D,45*D)
limShoulder_R = (-16*D,40*D,  -40*D,40*D,  -45*D,45*D)

limUpArm_L = (-90*D,90*D, -100*D,45*D, -90*D,90*D)
limUpArm_R = (-90*D,90*D, -45*D,100*D, -90*D,90*D)

limLoArm_L = (-90*D,90*D, -180*D,45*D, -135*D,0)
limLoArm_R = (-90*D,90*D, -45*D,180*D, 0,135*D)

limHand_L = (-90*D,70*D, 0,0, -20*D,20*D)
limHand_R = (-90*D,70*D, 0,0, -20*D,20*D)

#
#	Rotation modes
#	Dmod = Deform rig mode
#	Cmod = Control rig mode
#

DmodUpArm = P_YXZ
DmodLoArm = P_YXZ
DmodHand = P_YXZ

DmodUpArm = 0
DmodLoArm = 0
DmodHand = 0

CmodUpArm = 0
CmodLoArm = 0
CmodHand = 0

#
#	ArmControlPoses(fp):
#

def ArmControlPoses(fp):
	addPoseBone(fp, 'Sternum', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'SternumTarget', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Shoulder
	addPoseBone(fp, 'Shoulder_L', 'MHEndCube01', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), CmodUpArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_L, (True, True, True)])])

	addPoseBone(fp, 'Shoulder_R', 'MHEndCube01', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), CmodUpArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_R, (True, True, True)])])

	addPoseBone(fp, 'ArmLoc_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, 1, ['Shoulder', 'ShoulderEnd_L', (1,1,1), (0,0,0), False]),
		 ('CopyRot', 0, 0, ['Root', 'BendRoot', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'ArmLoc_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, 1, ['Shoulder', 'ShoulderEnd_R', (1,1,1), (0,0,0), False]),
		 ('CopyRot', 0, 0, ['Root', 'BendRoot', (1,1,1), (0,0,0), False])])



	# Arm
	deltaElbow = 0.6*D

	addPoseBone(fp, 'UpArm_L', 'GZM_Circle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), CmodUpArm, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_L, (True, True, True)]),
		 ('StretchTo', 0, 0, ['Elbow', 'Elbow_L', 0]),
		])

	addPoseBone(fp, 'Elbow_L', 'MHCube025', 'FK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), CmodLoArm, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_L', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_L', 'ONSURFACE']),
		])

	addPoseBone(fp, 'LoArm_L', 'GZM_Circle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), CmodLoArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArm_L, (True, True, True)]),
		 ('IK', 0, 0, ['ArmIK', 'Wrist_L', 2, (pi-deltaElbow, 'ElbowPT_L'), (True, False,True)]),
		 ('StretchTo', 0, 0, ['Wrist', 'Wrist_L', 0]),
		])

	addPoseBone(fp, 'Wrist_L', 'MHHandCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), CmodHand, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_L', (1,1,1), (1,1,1), (1,1,1)]),
		 ('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_L', 'INSIDE']),
		 ('LimitDist', 0, 0, ['DistElbow', 'Elbow_L', 'ONSURFACE']),
		])

	addPoseBone(fp, 'Hand_L', 'MHHand', 'FK_L', (0,0,0), (0,1,0), (1,1,1), (1,1,1), CmodHand,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_L, (True, True, True)]),
		 ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,True)]),
		 ('CopyLoc', 0, 0, ['WristLoc', 'Wrist_L', (1,1,1), (0,0,0), False]),
		 ('CopyRot', 0, 0, ['WristRot', 'Wrist_L', (1,1,1), (0,0,0), False])
		])
		

	addPoseBone(fp, 'UpArm_R', 'GZM_Circle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), CmodUpArm, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_R, (True, True, True)]),
		 ('StretchTo', 0, 0, ['Elbow', 'Elbow_R', 0]),
		])

	addPoseBone(fp, 'Elbow_R', 'MHCube025', 'FK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), CmodLoArm, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_R', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_R', 'ONSURFACE']),
		])

	addPoseBone(fp, 'LoArm_R', 'GZM_Circle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), CmodLoArm,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArm_R, (True, True, True)]),
		 ('IK', 0, 0, ['ArmIK', 'Wrist_R', 2, (deltaElbow, 'ElbowPT_R'), (True, False,True)]),
		 ('StretchTo', 0, 0, ['Wrist', 'Wrist_R', 0]),
		])

	addPoseBone(fp, 'Wrist_R', 'MHHandCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), CmodHand, 
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Shoulder_R', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistShoulder', 'ArmLoc_R', 'INSIDE']),
		('LimitDist', 0, 0, ['DistElbow', 'Elbow_R', 'ONSURFACE']),
		])

	addPoseBone(fp, 'Hand_R', 'MHHand', 'FK_R', (0,0,0), (0,1,0), (1,1,1), (1,1,1), CmodHand,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_R, (True, True, True)]),
		 ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,True)]),
		 ('CopyLoc', 0, 0, ['WristLoc', 'Wrist_R', (1,1,1), (0,0,0), False]),
		 ('CopyRot', 0, 0, ['WristRot', 'Wrist_R', (1,1,1), (0,0,0), False])
		])


	addPoseBone(fp, 'ElbowPT_L', 'MHCube025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'ElbowLinkPT_L', None, 'IK_L', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'ElbowPT_L', 0])])

	addPoseBone(fp, 'ArmTrg_L', None, 'FK_L', (1,1,1), (1,0,1), (1,1,1), (1,1,1), P_YXZ, 
		 [('IK', 0, 1, ['ArmIK', 'LoArm_L', 1, None, (True, False,True)])])

	addPoseBone(fp, 'UpArmRot_L', 'GZM_Circle10', 'IK_L', (1,1,1), (1,0,1), (1,1,1), (1,1,1), P_YXZ, 
		 [('IK', 0, 1, ['ArmIK', 'LoArm_L', 1, None, (True, False,True)])])


	addPoseBone(fp, 'ElbowPT_R', 'MHCube025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'ElbowLinkPT_R', None, 'IK_R', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'ElbowPT_R', 0])])

	addPoseBone(fp, 'ArmTrg_R', None, 'FK_R', (1,1,1), (1,0,1), (1,1,1), (1,1,1), P_YXZ, 
		 [('IK', 0, 1, ['ArmIK', 'LoArm_R', 1, None, (True, False,True)])])

	addPoseBone(fp, 'UpArmRot_R', 'GZM_Circle10', 'IK_R', (1,1,1), (1,0,1), (1,1,1), (1,1,1), P_YXZ, 
		 [('IK', 0, 1, ['ArmIK', 'LoArm_R', 1, None, (True, False,True)])])


	return
	
#
#	ArmDeformPoses(fp):
#

def ArmDeformPoses(fp):
	copyDeform(fp, 'Sternum', 0, U_LOC+U_ROT, None, [])
	copyDeform(fp, 'Shoulder_L', DmodUpArm, U_LOC+U_ROT, 'MHDefShoulder', [])
	copyDeform(fp, 'Shoulder_R', DmodUpArm, U_LOC+U_ROT, 'MHDefShoulder', [])
	copyDeform(fp, 'ArmLoc_L', 0, U_ROT, None, [])
	copyDeform(fp, 'ArmLoc_R', 0, U_ROT, None, [])
	
	# Shoulder	
	addPoseBone(fp, 'ShoulderPivot_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, 0.5, ['Rot', 'Shoulder_L', (1,1,1), (0,0,0), False])])
	
	addPoseBone(fp, 'ShoulderUp_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	
	addDeformIK(fp, 'ShoulderAim_L', 'SternumTarget', (-90*D, 'ShoulderUp_L'))
	
	addPoseBone(fp, 'Scapula_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	
	
	addPoseBone(fp, 'ShoulderPivot_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, 0.5, ['Rot', 'Shoulder_R', (1,1,1), (0,0,0), False])])
	
	addPoseBone(fp, 'ShoulderUp_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	
	addDeformIK(fp, 'ShoulderAim_R', 'SternumTarget', (-90*D, 'ShoulderUp_L'))
	
	addPoseBone(fp, 'Scapula_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])


	addPoseBone(fp, 'ShoulderTwist_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), DmodUpArm,
		[('CopyRot', 0, 0.5, ['Rot', 'UpArm_L', (1,1,1), (0,0,0), False]),
		 ('StretchTo', C_DEFRIG, 1, ['Stretch', 'UpArm2_L', 0])])

	addPoseBone(fp, 'ShoulderTwist_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), DmodUpArm,
		[('CopyRot', 0, 0.5, ['Rot', 'UpArm_R', (1,1,1), (0,0,0), False]),
		 ('StretchTo', C_DEFRIG, 1, ['Stretch', 'UpArm2_R', 0])])	
	

	# Shoulder deform
	addPoseBone(fp, 'ArmPit_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo',0, 1, ['Stretch', 'ArmTrg_L', 1])])
	
	addPoseBone(fp, 'Pectoralis_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Forward', 'ArmTrg_L', 1])])
	
	addPoseBone(fp, 'Trapezeus_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo',0, 1, ['Back', 'ArmTrg_L', 1])])
	
	addPoseBone(fp, 'Deltoid_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_PLANEZ, 1, ['Up', 'ArmTrg_L', 1])])
	

	addPoseBone(fp, 'ArmPit_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'ArmTrg_R', 1])])
	
	addPoseBone(fp, 'Pectoralis_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Forward', 'ArmTrg_R', 1])])
	
	addPoseBone(fp, 'Trapezeus_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Back', 'ArmTrg_R', 1])])
	
	addPoseBone(fp, 'Deltoid_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_PLANEZ, 1, ['Up', 'ArmTrg_R', 1])])
	
	'''
	
	addPoseBone(fp, 'ElbowBend_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'ElbowBendTrg_L', 0])])
	
		addPoseBone(fp, 'ElbowBend_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'ElbowBendTrg_R', 0])])
	'''
	(0, 'LoArmPT_L')

	deltaUpArm = 3*D
	deltaLoArm = 0*D
	
	# Arm deform
	copyDeformPartial(fp, 'UpArm1_L', 'UpArm_L', (1,0,1), DmodUpArm, U_LOC+U_SCALE, None, 
		[('IK', 0, 1, ['IK', 'LoArm_L', 1, (90*D-deltaUpArm, 'UpArm1PT_L'), (True, False,True)])])
		#[('CopyRot', C_LOCAL, 0.5, ['RotY', 'UpArm_L', (0,1,0), (0,0,0), False])])
	
	copyDeformPartial(fp, 'UpArm2_L', 'UpArm_L', (1,1,1), DmodUpArm, U_SCALE, 'MHDefUpArm2', [])
		
	copyDeformPartial(fp, 'UpArm3_L', 'UpArm_L', (0,1,0), DmodUpArm, U_SCALE, 'MHDefUpArm3', 
		[('IK', 0, 1, ['IK', 'LoArm_L', 1, (90*D-deltaUpArm, 'UpArm2PT_L'), (True, False,True)])])
		#[('CopyRot', C_LOCAL, 1, ['RotY', 'UpArm_L', (0,1,0), (0,0,0), False])])

	copyDeformPartial(fp, 'LoArm1_L', 'LoArm_L', (1,0,1), DmodLoArm, U_LOC+U_SCALE, None,
		[('IK', 0, 1, ['IK', 'Hand_L', 1, None, (True, False,True)])])
	
	copyDeformPartial(fp, 'LoArm2_L', 'LoArm_L', (1,1,1), DmodLoArm, U_SCALE, 'MHDefArm', [])
		
	copyDeformPartial(fp, 'LoArm3_L', 'LoArm_L', (0,1,0), DmodLoArm, U_SCALE, None,
		[('IK', 0, 1, ['IK', 'Hand_L', 1, (90*D-deltaLoArm, 'LoArmPT_L'), (True, False,True)])])
		
	addPoseBone(fp, 'LoArmFan_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), DmodLoArm, 
		#[('IK', 0, 0.5, ['IK', 'Hand_L', 1, (90*D-deltaUpArm, 'LoArmPT_L'), (True, False,True)])])
		[('CopyRot', 0, 0.5, ['Rot', 'LoArm_L', (1,1,1), (0,0,0), False])])
	
	copyDeform(fp, 'Hand_L', DmodHand, U_LOC+U_ROT, 'MHDefHand', [])


	copyDeformPartial(fp, 'UpArm1_R', 'UpArm_R', (1,1,1), DmodUpArm, U_LOC+U_SCALE, None, 
		[('IK', 0, 1, ['IK', 'LoArm_R', 1, (90*D+deltaUpArm, 'UpArm1PT_R'), (True, False,True)])])
		#[('CopyRot', C_LOCAL, 0.5, ['RotY', 'UpArm_R', (0,1,0), (0,0,0), False])])
	
	copyDeformPartial(fp, 'UpArm2_R', 'UpArm_R', (1,1,1), DmodUpArm, U_SCALE, 'MHDefUpArm2', [])
		
	copyDeformPartial(fp, 'UpArm3_R', 'UpArm_R', (0,1,0), DmodUpArm, U_SCALE, 'MHDefUpArm3',
		[('IK', 0, 1, ['IK', 'LoArm_R', 1, (90*D+deltaUpArm, 'UpArm2PT_R'), (True, False,True)])])
		#[('CopyRot', C_LOCAL, 1, ['RotY', 'UpArm_R', (0,1,0), (0,0,0), False])])

	copyDeformPartial(fp, 'LoArm1_R', 'LoArm_R', (1,0,1), DmodLoArm, U_LOC+U_SCALE, None, 
		[('IK', 0, 1, ['IK', 'Hand_R', 1, None, (True, False,True)])])
	
	copyDeformPartial(fp, 'LoArm2_R', 'LoArm_R', (1,1,1), DmodLoArm, U_SCALE, 'MHDefArm', [])
		
	copyDeformPartial(fp, 'LoArm3_R', 'LoArm_R', (0,1,0), DmodLoArm, U_SCALE, None,
		[('IK', 0, 1, ['IK', 'Hand_R', 1, (90*D+deltaLoArm, 'LoArmPT_R'), (True, False,True)])])
		
	addPoseBone(fp, 'LoArmFan_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), DmodLoArm,
		#[('IK', 0, 0.5, ['IK', 'Hand_R', 1, (90*D+deltaUpArm, 'LoArmPT_R'), (True, False,True)])])
		[('CopyRot', 0, 0.5, ['Rot', 'LoArm_R', (1,1,1), (0,0,0), False])])
	
	copyDeform(fp, 'Hand_R', DmodHand, U_LOC+U_ROT, 'MHDefHand', [])

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

ArmDeformDrivers = [
	("Deltoid_L", "Up", "min(u,2.7-d)", 
		[("u", "ArmTrg_L", "BendArmUp_L"), ("d", "ArmTrg_L", "BendArmDown_L")], 
		[(0,1), (40*D,1), (90*D,0)]),

	("Pectoralis_L", "Forward", "f", 
		 [("f", "ArmTrg_L", "BendArmForward_L")], [(0,1), (70*D,1), (90*D,1)]),

	("Trapezeus_L", "Back", "b", 
		 [("b", "ArmTrg_L", "BendArmBack_L")], [(0,1), (50*D,1), (90*D,0.5)]),


	("Deltoid_R", "Up", "min(u,2.7-d)", 
		[("u", "ArmTrg_R", "BendArmUp_R"), ("d", "ArmTrg_R", "BendArmDown_R")], 
		[(0,1), (40*D,1), (90*D,0)]),

	("Pectoralis_R", "Forward", "f", 
		 [("f", "ArmTrg_R", "BendArmForward_R")], [(0,1), (70*D,1), (90*D,1)]),

	("Trapezeus_R", "Back", "b", 
		 [("b", "ArmTrg_R", "BendArmBack_R")], [(0,1), (50*D,1), (90*D,0.5)]),

]

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


