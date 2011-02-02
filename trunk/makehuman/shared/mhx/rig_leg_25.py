#
#	Leg bone definitions 
#

import mhx_rig
from mhx_rig import *

offs = [0,0.6,0]

LegJoints = [
	('r-upleg1',			'l', ((1-bbMarg, 'r-upper-leg'), (bbMarg, 'r-knee'))),
	('r-upleg2',			'l', ((0.5, 'r-upper-leg'), (0.5, 'r-knee'))),

	('l-upleg1',			'l', ((1-bbMarg, 'l-upper-leg'), (bbMarg, 'l-knee'))),
	('l-upleg2',			'l', ((0.5, 'l-upper-leg'), (0.5, 'l-knee'))),

	('r-heel0',			'v', 5721),
	('r-heel',			'p', ['r-foot-2', 'r-foot-1', 'r-heel0']),
	('r-ankle-tip',		'o', ('r-ankle', [0.0, 0.0, -1.0])),
	('r-upleg-025',		'l', ((0.75, 'r-upper-leg'), (0.25, 'r-knee'))),
	('r-loleg-fan',		'l', ((0.75, 'r-knee'), (0.25, 'r-ankle'))),
	('r-buttock-top',		'v', 4473),
	('r-buttock-bot',		'v', 4476),

	('l-heel0',			'v', 13338),
	('l-heel',			'p', ['l-foot-2', 'l-foot-1', 'l-heel0']),
	('l-ankle-tip',		'o', ('l-ankle', [0.0, 0.0, -1.0])),
	('l-upleg-025',		'l', ((0.75, 'l-upper-leg'), (0.25, 'l-knee'))),
	('l-loleg-fan',		'l', ((0.75, 'l-knee'), (0.25, 'l-ankle'))),
	('l-buttock-top',		'v', 6892),
	('l-buttock-bot',		'v', 6889),

	('r-knee-pt',			'o', ('r-knee', [0,0,3])),
	('l-knee-pt',			'o', ('l-knee', [0,0,3])),

	('r-knee-head',			'v', 4500),
	('r-knee-tail',			'v', 5703),
	('l-knee-head',			'v', 6865),
	('l-knee-tail',			'v', 6779),

	('r-legout-head',		'v', 2935),
	('r-legout-tail',		'v', 3968),
	('l-legout-head',		'v', 7301),
	('l-legout-tail',		'v', 7041),

	('r-legback-head',		'v', 4472),
	('r-legback-tail',		'v', 3837),
	('l-legback-head',		'v', 6893),
	('l-legback-tail',		'v', 7172),

	('r-legforward-head',	'v', 6560),
	('r-legforward-tail',	'v', 3796),
	('l-legforward-head',	'v', 6752),
	('l-legforward-tail',	'v', 7215),
]

LegHeadsTails = [
	# Deform 
	('UpLeg1_L',		'r-upper-leg', 'r-upleg1'),
	('UpLeg2_L',		'r-upleg1', 'r-upleg2'),
	('UpLeg3_L',		'r-upleg2', 'r-knee'),
	('LoLeg_L',			'r-knee', 'r-ankle'),
	('LoLegFan_L',		'r-knee', 'r-loleg-fan'),
	('Foot_L',			'r-ankle', 'r-foot-1'),
	('Toe_L',			'r-foot-1', 'r-foot-2'),

	('UpLeg1_R',		'l-upper-leg', 'l-upleg1'),
	('UpLeg2_R',		'l-upleg1', 'l-upleg2'),
	('UpLeg3_R',		'l-upleg2', 'l-knee'),
	('LoLeg_R',			'l-knee', 'l-ankle'),
	('LoLegFan_R',		'l-knee', 'l-loleg-fan'),
	('Foot_R',			'l-ankle', 'l-foot-1'),
	('Toe_R',			'l-foot-1', 'l-foot-2'),

	# Rotation diffs
	('BendLegForward_L',	'r-upper-leg', ('r-upper-leg', (0,0,1))),
	('BendLegBack_L',		'r-upper-leg', ('r-upper-leg', (0,0,-1))),
	('BendLegUp_L',			'r-upper-leg', ('r-upper-leg', (0,1,0))),
	('BendLegDown_L',		'r-upper-leg', ('r-upper-leg', (0,-1,0))),
	('BendLegOut_L',		'r-upper-leg', ('r-upper-leg', (1,0,0))),

	('BendLegForward_R',	'l-upper-leg', ('l-upper-leg', (0,0,1))),
	('BendLegBack_R',		'l-upper-leg', ('l-upper-leg', (0,0,-1))),
	('BendLegUp_R',			'l-upper-leg', ('l-upper-leg', (0,1,0))),
	('BendLegDown_R',		'l-upper-leg', ('l-upper-leg', (0,-1,0))),
	('BendLegOut_R',		'l-upper-leg', ('l-upper-leg', (-1,0,0))),

	# Hip deform
	('LegForward_L',		'r-legforward-head', 'r-legforward-tail'),
	('LegBack_L',			'r-legback-head', 'r-legback-tail'),
	('LegOut_L',			'r-legout-head', 'r-legout-tail'),
	('LegForwardTrg_L',		'r-legforward-tail', ('r-legforward-tail', zunit)),
	('LegBackTrg_L',		'r-legback-tail', ('r-legback-tail', zunit)),
	('LegOutTrg_L',			'r-legout-tail', ('r-legout-tail', zunit)),

	('LegForward_R',		'l-legforward-head', 'l-legforward-tail'),
	('LegBack_R',			'l-legback-head', 'l-legback-tail'),
	('LegOut_R',			'l-legout-head', 'l-legout-tail'),
	('LegForwardTrg_R',		'l-legforward-tail', ('l-legforward-tail', zunit)),
	('LegBackTrg_R',		'l-legback-tail', ('l-legback-tail', zunit)),
	('LegOutTrg_R',			'l-legout-tail', ('l-legout-tail', zunit)),

	# Knee deform
	('Knee_L',			'r-knee-head', 'r-knee-tail'),
	('KneeTrg_L',		'r-knee-tail', ('r-knee-tail', yunit)),
	('Knee_R',			'l-knee-head', 'l-knee-tail'),
	('KneeTrg_R',		'l-knee-tail', ('l-knee-tail', yunit)),

	# FK
	('UpLegFK_L',		'r-upper-leg', 'r-knee'),
	('LoLegFK_L',		'r-knee', 'r-ankle'),
	('FootFK_L',		'r-ankle', 'r-foot-1'),
	('ToeFK_L',			'r-foot-1', 'r-foot-2'),
	('LegFK_L',			'r-heel', 'r-foot-2'),
	('AnkleFK_L',		'r-ankle', 'r-ankle-tip'),

	('UpLegFK_R',		'l-upper-leg', 'l-knee'),
	('LoLegFK_R',		'l-knee', 'l-ankle'),
	('FootFK_R',		'l-ankle', 'l-foot-1'),
	('ToeFK_R',			'l-foot-1', 'l-foot-2'),
	('LegFK_R',			'l-heel', 'l-foot-2'),
	('AnkleFK_R',		'l-ankle', 'l-ankle-tip'),
	
	# IK 
	('UpLegIK_L',		'r-upper-leg', 'r-knee'),
	('LoLegIK_L',		'r-knee', 'r-ankle'),
	('AnkleIK_L',		'r-ankle', 'r-ankle-tip'),
	('FootIK_L',		'r-ankle', 'r-foot-1'),
	('ToeIK_R',			'l-foot-1', 'l-foot-2'),
	('LegIK_L',			'r-heel', 'r-foot-2'),
	('ToeRevIK_L',		'r-foot-2', 'r-foot-1'),
	('FootRevIK_L',		'r-foot-1', 'r-ankle'),
	('AnkleIK_L',		'r-ankle', 'r-ankle-tip'),

	('UpLegIK_R',		'l-upper-leg', 'l-knee'),
	('LoLegIK_R',		'l-knee', 'l-ankle'),
	('AnkleIK_R',		'l-ankle', 'l-ankle-tip'),
	('FootIK_R',		'l-ankle', 'l-foot-1'),
	('ToeIK_L',			'r-foot-1', 'r-foot-2'),
	('LegIK_R',			'l-heel', 'l-foot-2'),
	('ToeRevIK_R',		'l-foot-2', 'l-foot-1'),
	('FootRevIK_R',		'l-foot-1', 'l-ankle'),
	('AnkleIK_R',		'l-ankle', 'l-ankle-tip'),

	# Pole Target
	('KneePTIK_L',			'r-knee-pt', ('r-knee-pt', offs)),
	('KneePTIK_R',			'l-knee-pt', ('l-knee-pt', offs)),
	('KneeLinkPTIK_L',		'r-knee', 'r-knee-pt'),
	('KneeLinkPTIK_R',		'l-knee', 'l-knee-pt'),
	('KneePTFK_L',			'r-knee-pt', ('r-knee-pt', offs)),
	('KneePTFK_R',			'l-knee-pt', ('l-knee-pt', offs)),
]

upLegRoll = 0
loLegRoll = 0
footRoll = 0
#toeRoll = -63.5*D
toeRoll = 135*D
footCtrlRoll = 0.0

LegArmature = [
	# Deform
	('UpLeg1_L',		upLegRoll, 'Hip_L', F_DEF, L_DEF, NoBB),
	('UpLeg2_L',		upLegRoll, 'UpLeg1_L', F_DEF+F_CON, L_DEF,(0,0,5) ),
	('UpLeg3_L',		upLegRoll, 'UpLeg2_L', F_DEF+F_CON, L_DEF, NoBB),
	('LoLeg_L',			loLegRoll, 'UpLeg3_L', F_DEF, L_DEF, NoBB),
	('LoLegFan_L',		loLegRoll, 'UpLeg3_L', F_DEF, L_DEF, NoBB),
	('Foot_L',			footRoll, 'LoLeg_L', F_DEF, L_DEF, NoBB),
	('Toe_L',			toeRoll, 'Foot_L', F_DEF, L_DEF, NoBB),

	('UpLeg1_R',		upLegRoll, 'Hip_R', F_DEF, L_DEF, NoBB),
	('UpLeg2_R',		upLegRoll, 'UpLeg1_R', F_DEF+F_CON, L_DEF,(0,0,5) ),
	('UpLeg3_R',		upLegRoll, 'UpLeg2_R', F_DEF+F_CON, L_DEF, NoBB),
	('LoLeg_R',			-loLegRoll, 'UpLeg3_R', F_DEF, L_DEF, NoBB),
	('LoLegFan_R',		-loLegRoll, 'UpLeg3_R', F_DEF, L_DEF, NoBB),
	('Foot_R',			-footRoll, 'LoLeg_R', F_DEF, L_DEF, NoBB),
	('Toe_R',			-toeRoll, 'Foot_R', F_DEF, L_DEF, NoBB),

	# Rotation diffs
	('BendLegForward_L',	pi, 'Hip_L', 0, L_HELP, NoBB),
	('BendLegBack_L',		0, 'Hip_L', 0, L_HELP, NoBB),
	('BendLegUp_L',			0, 'Hip_L', 0, L_HELP, NoBB),
	('BendLegDown_L',		0, 'Hip_L', 0, L_HELP, NoBB),
	('BendLegOut_L',		-90*D, 'Hip_L', 0, L_HELP, NoBB),

	('BendLegForward_R',	pi, 'Hip_R', 0, L_HELP, NoBB),
	('BendLegBack_R',		0, 'Hip_R', 0, L_HELP, NoBB),
	('BendLegUp_R',			0, 'Hip_R', 0, L_HELP, NoBB),
	('BendLegDown_R',		0, 'Hip_R', 0, L_HELP, NoBB),
	('BendLegOut_R',		90*D, 'Hip_R', 0, L_HELP, NoBB),

	# Hip deform
	('LegForward_L',		0, 'Hip_L', F_DEF, L_DEF, NoBB),
	('LegBack_L',			0, 'Hip_L', F_DEF, L_DEF, NoBB),
	('LegOut_L',			0, 'Hip_L', F_DEF, L_DEF, NoBB),
	('LegForwardTrg_L',		0, 'UpLeg1_L', 0, L_HELP, NoBB),
	('LegBackTrg_L',		0, 'UpLeg1_L', 0, L_HELP, NoBB),
	('LegOutTrg_L',			0, 'UpLeg1_L', 0, L_HELP, NoBB),

	('LegForward_R',		0, 'Hip_R', F_DEF, L_DEF, NoBB),
	('LegBack_R',			0, 'Hip_R', F_DEF, L_DEF, NoBB),
	('LegOut_R',			0, 'Hip_R', F_DEF, L_DEF, NoBB),
	('LegForwardTrg_R',		0, 'UpLeg1_R', 0, L_HELP, NoBB),
	('LegBackTrg_R',		0, 'UpLeg1_R', 0, L_HELP, NoBB),
	('LegOutTrg_R',			0, 'UpLeg1_R', 0, L_HELP, NoBB),

	# Knee deform
	('Knee_L',				0, 'UpLeg3_L', F_DEF, L_DEF, NoBB),
	('KneeTrg_L',			0, 'LoLeg_L', 0, L_HELP, NoBB),
	('Knee_R',				0, 'UpLeg3_R', F_DEF, L_DEF, NoBB),
	('KneeTrg_R',			0, 'LoLeg_R', 0, L_HELP, NoBB),

	# FK
	('UpLegFK_L',		upLegRoll, 'Hip_L', F_WIR, L_LEGFK, NoBB),
	('LoLegFK_L',		loLegRoll, 'UpLegFK_L', F_WIR, L_LEGFK, NoBB),
	('FootFK_L',		footRoll, 'LoLegFK_L', F_CON+F_WIR, L_LEGFK, NoBB),
	('ToeFK_L',			toeRoll, 'FootFK_L', F_WIR, L_LEGFK, NoBB),
	('LegFK_L',			footCtrlRoll, 'ToeFK_L', 0, L_HELP, NoBB),
	('AnkleFK_L',		0, 'LoLegFK_L', 0, L_HELP, NoBB),

	('UpLegFK_R',		-upLegRoll, 'Hip_R', F_WIR, L_LEGFK, NoBB),
	('LoLegFK_R',		-loLegRoll, 'UpLegFK_R', F_WIR, L_LEGFK, NoBB),
	('FootFK_R',		-footRoll, 'LoLegFK_R', F_CON+F_WIR, L_LEGFK, NoBB),
	('ToeFK_R',			-toeRoll, 'FootFK_R', F_WIR, L_LEGFK, NoBB),
	('LegFK_R',			-footCtrlRoll, 'ToeFK_R', 0, L_HELP, NoBB),
	('AnkleFK_R',		0, 'LoLegFK_L', 0, L_HELP, NoBB),

	# IK
	('UpLegIK_L',		upLegRoll, 'Hip_L', 0, L_LEGIK, NoBB),
	('LoLegIK_L',		loLegRoll, 'UpLegIK_L', 0, L_LEGIK, NoBB),
	('FootIK_L',		footRoll, 'LoLegIK_L', 0, L_HLPIK, NoBB),
	('ToeIK_L',			toeRoll, 'FootIK_L', 0, L_HLPIK, NoBB),
	('LegIK_L',			footCtrlRoll, Master, F_WIR, L_LEGIK, NoBB),
	('ToeRevIK_L',		0, 'LegIK_L', F_WIR, L_LEGIK, NoBB),
	('FootRevIK_L',		0, 'ToeRevIK_L', F_WIR, L_LEGIK, NoBB),
	('AnkleIK_L',		0, 'FootRevIK_L', 0, L_HELP, NoBB),

	('UpLegIK_R',		-upLegRoll, 'Hip_R', 0, L_LEGIK, NoBB),
	('LoLegIK_R',		-loLegRoll, 'UpLegIK_R', 0, L_LEGIK, NoBB),
	('FootIK_R',		-footRoll, 'LoLegIK_R', 0, L_HLPIK, NoBB),
	('ToeIK_R',			-toeRoll, 'FootIK_R', 0, L_HLPIK, NoBB),
	('LegIK_R',			-footCtrlRoll, Master, F_WIR, L_LEGIK, NoBB),
	('ToeRevIK_R',		0, 'LegIK_R', F_WIR, L_LEGIK, NoBB),
	('FootRevIK_R',		0, 'ToeRevIK_R', F_WIR, L_LEGIK, NoBB),
	('AnkleIK_R',		0, 'FootRevIK_R', 0, L_HELP, NoBB),

	# Pole target
	('KneePTIK_L',		0.0, 'Hip_L', F_WIR, L_LEGIK, NoBB),
	('KneePTIK_R',		0.0, 'Hip_R', F_WIR, L_LEGIK, NoBB),
	('KneeLinkPTIK_L',	0.0, 'UpLegIK_L', F_RES, L_LEGIK, NoBB),
	('KneeLinkPTIK_R',	0.0, 'UpLegIK_R', F_RES, L_LEGIK, NoBB),
	('KneePTFK_L',		0.0, 'UpLegFK_L', 0, L_HELP, NoBB),
	('KneePTFK_R',		0.0, 'UpLegFK_R', 0, L_HELP, NoBB),
]

#
#	LegWritePoses(fp):
#

limUpLeg_L = (-110*D,90*D, -90*D,90*D, -110*D,40*D)
limUpLeg_R = (-110*D,90*D, -90*D,90*D, -40*D,110*D)

limLoLeg_L = (-20*D,150*D,-40*D,40*D, -40*D,40*D)
limLoLeg_R = (-20*D,150*D,-40*D,40*D, -40*D,40*D)

limFoot_L = (-50*D,50*D, -40*D,40*D, -40*D,40*D)
limFoot_R = (-50*D,50*D, -40*D,40*D, -40*D,40*D)

limToe_L = (-20*D,60*D, 0,0, 0,0)
limToe_R = (-20*D,60*D, 0,0, 0,0)

limRevFoot_L = (-20*D,60*D, 0,0, 0,0)
limRevFoot_R = (-20*D,60*D, 0,0, 0,0)

limRevToe_L = (-10*D,45*D, 0,0, 0,0)
limRevToe_R = (-10*D,45*D, 0,0, 0,0)

RmodUpLeg = P_YZX
RmodLoLeg = P_YZX
RmodFoot = P_YZX
RmodToe = P_YZX

def LegWritePoses(fp):
	# Deform 
	addDeformLimb(fp, 'UpLeg1_L', 'UpLegIK_L', (1,0,1), 'UpLegFK_L', (1,0,1), C_LOCAL, RmodUpLeg, [])

	addPoseBone(fp, 'UpLeg2_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpLeg, [])

	addDeformLimb(fp, 'UpLeg3_L', 'UpLegIK_L', (0,1,0), 'UpLegFK_L', (0,1,0), C_LOCAL, RmodUpLeg, [])

	addDeformLimb(fp, 'LoLeg_L', 'LoLegIK_L', (1,1,1), 'LoLegFK_L', (1,1,1), 0, P_STRETCH+RmodLoLeg, [])

	addPoseBone(fp, 'LoLegFan_L', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), RmodLoLeg,
		[('CopyRot', C_LOCAL, 0, ['Rot', 'LoLeg_L', (1,0,1), (0,0,0), False])])

	addDeformLimb(fp, 'Foot_L', 'FootIK_L', (1,1,1), 'FootFK_L', (1,1,1), 0, RmodFoot, [])

	addDeformLimb(fp, 'Toe_L', 'ToeIK_L', (1,1,1), 'ToeFK_L', (1,1,1), 0, RmodToe, [])


	addDeformLimb(fp, 'UpLeg1_R', 'UpLegIK_R', (1,0,1), 'UpLegFK_R', (1,0,1), C_LOCAL, RmodUpLeg, [])

	addPoseBone(fp, 'UpLeg2_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpLeg, [])

	addDeformLimb(fp, 'UpLeg3_R', 'UpLegIK_R', (0,1,0), 'UpLegFK_R', (0,1,0), C_LOCAL, RmodUpLeg, [])

	addDeformLimb(fp, 'LoLeg_R', 'LoLegIK_R', (1,1,1), 'LoLegFK_R', (1,1,1), 0, P_STRETCH+RmodLoLeg, [])

	addPoseBone(fp, 'LoLegFan_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), RmodLoLeg,
		[('CopyRot', C_LOCAL, 0, ['Rot', 'LoLeg_R', (1,0,1), (0,0,0), False])])

	addDeformLimb(fp, 'Foot_R', 'FootIK_R', (1,1,1), 'FootFK_R', (1,1,1), 0, RmodFoot, [])

	addDeformLimb(fp, 'Toe_R', 'ToeIK_R', (1,1,1), 'ToeFK_R', (1,1,1), 0, RmodToe, [])

	# Hip deform

	addPoseBone(fp, 'LegForward_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegForwardTrg_L', 0]),
 		 ('LimitScale', C_OW_LOCAL, 0, ['Scale', (0,0, 0,0, 0,0), (0,1,0)])])

	addPoseBone(fp, 'LegBack_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegBackTrg_L', 0])])

	addPoseBone(fp, 'LegOut_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegOutTrg_L', 0])])


	addPoseBone(fp, 'LegForward_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegForwardTrg_R', 0]),
 		 ('LimitScale', C_OW_LOCAL, 0, ['Scale', (0,0, 0,0, 0,0), (0,1,0)])])

	addPoseBone(fp, 'LegBack_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegBackTrg_R', 0])])

	addPoseBone(fp, 'LegOut_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegOutTrg_R', 0])])

	# Knee deform

	addPoseBone(fp, 'Knee_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'KneeTrg_L', 0])])

	addPoseBone(fp, 'Knee_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'KneeTrg_R', 0])])


	# FK
	addPoseBone(fp, 'UpLegFK_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpLeg,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_L, (1,1,1)])])

	addPoseBone(fp, 'LoLegFK_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodLoLeg, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_L, (1,1,1)])])

	addPoseBone(fp, 'FootFK_L', 'MHFoot', 'FK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), RmodFoot, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limFoot_L, (1,1,1)]),
		 ('IK', 0, 1, ['IK', None, 2, None, (True, False,True)])])

	addPoseBone(fp, 'ToeFK_L', 'MHToe_L', 'FK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), RmodToe, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limToe_L, (1,0,0)])])

	addPoseBone(fp, 'UpLegFK_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodUpLeg,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_R, (1,1,1)])])

	addPoseBone(fp, 'LoLegFK_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), RmodLoLeg,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_R, (1,1,1)])])

	addPoseBone(fp, 'FootFK_R', 'MHFoot', 'FK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), RmodFoot, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limFoot_R, (1,1,1)]),
		 ('IK', 0, 1, ['IK', None, 2, None, (True, False,True)])])

	addPoseBone(fp, 'ToeFK_R', 'MHToe_R', 'FK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), RmodToe, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limToe_R, (1,0,0)])])


	# IK 
	addPoseBone(fp, 'UpLegIK_L', None, 'IK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+RmodUpLeg,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_L, (1,1,1)])])

	addPoseBone(fp, 'UpLegIK_R', None, 'IK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+RmodUpLeg,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_R, (1,1,1)])])

	addPoseBone(fp, 'LegIK_L', 'MHFootCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Hip', 'Hip_L', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistHip', 'Hip_L', 'INSIDE'])])

	addPoseBone(fp, 'LegIK_R', 'MHFootCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Hip', 'Hip_R', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistHip', 'Hip_R', 'INSIDE'])])

	deltaKnee = -2.5*D

	addPoseBone(fp, 'LoLegIK_L', None, 'IK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+RmodLoLeg,
		[('IK', 0, 1, ['IK', 'AnkleIK_L', 2, (-90*D+deltaKnee, 'KneePTIK_L'), (1,0,1)]),
		('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_L, (1,1,1)])
		])

	addPoseBone(fp, 'LoLegIK_R', None, 'IK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+RmodLoLeg,
		[('IK', 0, 1, ['IK', 'AnkleIK_R', 2, (-90*D-deltaKnee, 'KneePTIK_R'), (1,0,1)]),
		('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_R, (1,1,1)])
		])

	addPoseBone(fp, 'FootRevIK_L', 'MHRevFoot', 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), RmodFoot, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevFoot_L, (1,1,1)])])

	addPoseBone(fp, 'FootRevIK_R', 'MHRevFoot', 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), RmodFoot,

		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevFoot_R, (1,1,1)])])

	addPoseBone(fp, 'ToeRevIK_L', 'MHRevToe', 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), RmodToe, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevToe_L, (1,1,1)])])

	addPoseBone(fp, 'ToeRevIK_R', 'MHRevToe', 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), RmodToe, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevToe_R, (1,1,1)])])
	
	addPoseBone(fp, 'FootIK_L', None, 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), RmodFoot, 
		[('CopyRot', C_LOCAL, 1, ['Rot', 'FootRevIK_L', (0,1,0), (0,0,0), True]),
		 ('IK', 0, 1, ['IK', 'FootRevIK_L', 1, None, (1,0,1)])])

	addPoseBone(fp, 'FootIK_R', None, 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), RmodFoot, 
		[('CopyRot', C_LOCAL, 1, ['Rot', 'FootRevIK_R', (0,1,0), (0,0,0), True]),
		 ('IK', 0, 1, ['IK', 'FootRevIK_R', 1, None, (1,0,1)])])

	addPoseBone(fp, 'ToeIK_L', None, 'IK_L', (1,1,1), (0,1,1), (1,1,0), (1,1,1), RmodToe, 
		[('IK', 0, 1, ['IK', 'ToeRevIK_L', 1, None, (1,0,1)])])

	addPoseBone(fp, 'ToeIK_R', None, 'IK_R', (1,1,1), (0,1,1), (1,1,0), (1,1,1), RmodToe, 
		[('IK', 0, 1, ['IK', 'ToeRevIK_R', 1, None, (1,0,1)])])
	
	# Pole target

	addPoseBone(fp, 'KneePTIK_L', 'MHCube025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'KneeLinkPTIK_L', None, 'IK_L', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'KneePTIK_L', 0])])

	addPoseBone(fp, 'KneePTIK_R', 'MHCube025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'KneeLinkPTIK_R', None, 'IK_R', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'KneePTIK_R', 0])])

	return

#
#	LegFKIKDrivers
#	(Bone, cond, FK constraint, IK constraint, driver, channel, max)
#

LegFKIKDrivers = [
	("UpLeg1_L", True, ["RotFK"], ["RotIK"], "PLegIK_L", "LOC_X", 1.0),
	("UpLeg3_L", True, ["RotFK"], ["RotIK"], "PLegIK_L", "LOC_X", 1.0),
	("LoLeg_L", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PLegIK_L", "LOC_X", 1.0),
	("Foot_L", True, ["RotFK"], ["RotIK"], "PLegIK_L", "LOC_X", 1.0),
	("Toe_L", True, ["RotFK"], ["RotIK"], "PLegIK_L", "LOC_X", 1.0),
	
	("UpLeg1_R", True, ["RotFK"], ["RotIK"], "PLegIK_R", "LOC_X", 1.0),
	("UpLeg3_R", True, ["RotFK"], ["RotIK"], "PLegIK_R", "LOC_X", 1.0),
	("LoLeg_R", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PLegIK_R", "LOC_X", 1.0),
	("Foot_R", True, ["RotFK"], ["RotIK"], "PLegIK_R", "LOC_X", 1.0),
	("Toe_R", True, ["RotFK"], ["RotIK"], "PLegIK_R", "LOC_X", 1.0),
]

#
#	LegDeformDrivers
#	Bone : (constraint, driver, rotdiff, keypoints)
#

LegDeformDrivers = [
	("LegForward_L", "Stretch", None,
		[("f", "UpLeg1_L", "BendLegForward_L"), ("o", "UpLeg1_L", "BendLegOut_L")], 
		[(0,1), (60*D,1), (90*D,0.3)]),
	("LegForward_L", "Scale",  "(d-u)*(f<%.2f)" % (75*D),
		[("u", "UpLeg1_L", "BendLegUp_L"), ("d", "UpLeg1_L", "BendLegDown_L"), ("f", "UpLeg1_L", "BendLegForward_L")], 
		[(0,0), (20*D,1)]),
	("LegBack_L", "Stretch",   "min(b,o+0.5)",
		[("b", "UpLeg1_L", "BendLegBack_L"), ("o", "UpLeg1_L", "BendLegOut_L")], 
		[(0,1), (60*D,1), (90*D,0.3)]),
	("LegOut_L", "Stretch",  None,
		[("o", "UpLeg1_L", "BendLegOut_L")], 
		[(0,1), (60*D,1), (90*D,0.3)]),

	("LegForward_R", "Stretch", None,
		[("f", "UpLeg1_R", "BendLegForward_R"), ("o", "UpLeg1_R", "BendLegOut_R")], 
		[(0,1), (60*D,1), (90*D,0.3)]),
	("LegForward_R", "Scale",  "(d-u)*(f<%.2f)" % (75*D),
		[("u", "UpLeg1_R", "BendLegUp_R"), ("d", "UpLeg1_R", "BendLegDown_R"), ("f", "UpLeg1_R", "BendLegForward_R")], 
		[(0,0), (20*D,1)]),
	("LegBack_R", "Stretch",   "min(b,o+0.5)",
		[("b", "UpLeg1_R", "BendLegBack_R"), ("o", "UpLeg1_R", "BendLegOut_R")], 
		[(0,1), (60*D,1), (90*D,0.3)]),
	("LegOut_R", "Stretch",  None,
		[("o", "UpLeg1_R", "BendLegOut_R")], 
		[(0,1), (60*D,1), (90*D,0.3)]),
]

#
#	LegShapeDrivers
#	Shape : (driver, rotdiff, keypoints)
#

LegShapeDrivers = {
}




