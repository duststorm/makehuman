#
#	Leg bone definitions
#

import mhx_rig
from mhx_rig import *

offs = [0,0.6,0]

LegJoints = [

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
	('UpLegTwist_L',	'r-upper-leg', 'r-knee'),
	('UpLeg_L',			'r-upper-leg', 'r-knee'),
	('LoLeg_L',			'r-knee', 'r-ankle'),
	('LoLegFan_L',		'r-knee', 'r-loleg-fan'),
	('Foot_L',			'r-ankle', 'r-foot-1'),
	('Toe_L',			'r-foot-1', 'r-foot-2'),

	('UpLegTwist_R',	'l-upper-leg', 'l-knee'),
	('UpLeg_R',			'l-upper-leg', 'l-knee'),
	('LoLeg_R',			'l-knee', 'l-ankle'),
	('LoLegFan_R',		'l-knee', 'l-loleg-fan'),
	('Foot_R',			'l-ankle', 'l-foot-1'),
	('Toe_R',			'l-foot-1', 'l-foot-2'),

	# Rotation diffs
	('BendLegForwDown_L',	'r-upper-leg', ('r-upper-leg', (0,-0.5,1))),
	('BendLegForwUp_L',		'r-upper-leg', ('r-upper-leg', (0,0.5,1))),
	('BendLegBack_L',		'r-upper-leg', ('r-upper-leg', (0,0,-1))),
	('BendLegOut_L',		'r-upper-leg', ('r-upper-leg', (1,0,0))),

	('BendLegForwDown_R',	'l-upper-leg', ('l-upper-leg', (0,-0.5,1))),
	('BendLegForwUp_R',		'l-upper-leg', ('l-upper-leg', (0,0.5,1))),
	('BendLegBack_R',		'l-upper-leg', ('l-upper-leg', (0,0,-1))),
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
#toeRoll = 0
toeRoll = -63.5*deg1
footCtrlRoll = 0.0

LegArmature = [
	# Deform
	('UpLegTwist_L',	upLegRoll, 'Hip_L', F_DEF, L_DEF, (1,1,1) ),
	('UpLeg_L',			upLegRoll, 'Hip_L', F_DEF, L_DEF, (1,1,1) ),
	('LoLeg_L',			loLegRoll, 'UpLeg_L', F_DEF, L_DEF, (1,1,1) ),
	('LoLegFan_L',		loLegRoll, 'UpLeg_L', F_DEF, L_DEF, (1,1,1) ),
	('Foot_L',			footRoll, 'LoLeg_L', F_DEF, L_DEF, (1,1,1) ),
	('Toe_L',			toeRoll, 'Foot_L', F_DEF, L_DEF, (1,1,1) ),

	('UpLegTwist_R',	-upLegRoll, 'Hip_R', F_DEF, L_DEF, (1,1,1) ),
	('UpLeg_R',			-upLegRoll, 'Hip_R', F_DEF, L_DEF, (1,1,1) ),
	('LoLeg_R',			-loLegRoll, 'UpLeg_R', F_DEF, L_DEF, (1,1,1) ),
	('LoLegFan_R',		-loLegRoll, 'UpLeg_R', F_DEF, L_DEF, (1,1,1) ),
	('Foot_R',			-footRoll, 'LoLeg_R', F_DEF, L_DEF, (1,1,1) ),
	('Toe_R',			-toeRoll, 'Foot_R', F_DEF, L_DEF, (1,1,1) ),

	# Rotation diffs
	('BendLegForwDown_L',	0, 'Hip_L', 0, L_HELP, (1,1,1) ),
	('BendLegForwUp_L',		0, 'Hip_L', 0, L_HELP, (1,1,1) ),
	('BendLegBack_L',		0, 'Hip_L', 0, L_HELP, (1,1,1) ),
	('BendLegOut_L',		-deg90, 'Hip_L', 0, L_HELP, (1,1,1) ),

	('BendLegForwDown_R',	0, 'Hip_R', 0, L_HELP, (1,1,1) ),
	('BendLegForwUp_R',		0, 'Hip_R', 0, L_HELP, (1,1,1) ),
	('BendLegBack_R',		0, 'Hip_R', 0, L_HELP, (1,1,1) ),
	('BendLegOut_R',		deg90, 'Hip_R', 0, L_HELP, (1,1,1) ),

	# Hip deform
	('LegForward_L',		0, 'Hip_L', F_DEF, L_DEF, (1,1,1) ),
	('LegBack_L',			0, 'Hip_L', F_DEF, L_DEF, (1,1,1) ),
	('LegOut_L',			0, 'Hip_L', F_DEF, L_DEF, (1,1,1) ),
	('LegForwardTrg_L',		0, 'UpLegTwist_L', 0, L_HELP, (1,1,1) ),
	('LegBackTrg_L',		0, 'UpLegTwist_L', 0, L_HELP, (1,1,1) ),
	('LegOutTrg_L',			0, 'UpLegTwist_L', 0, L_HELP, (1,1,1) ),

	('LegForward_R',		0, 'Hip_R', F_DEF, L_DEF, (1,1,1) ),
	('LegBack_R',			0, 'Hip_R', F_DEF, L_DEF, (1,1,1) ),
	('LegOut_R',			0, 'Hip_R', F_DEF, L_DEF, (1,1,1) ),
	('LegForwardTrg_R',		0, 'UpLegTwist_R', 0, L_HELP, (1,1,1) ),
	('LegBackTrg_R',		0, 'UpLegTwist_R', 0, L_HELP, (1,1,1) ),
	('LegOutTrg_R',			0, 'UpLegTwist_R', 0, L_HELP, (1,1,1) ),

	# FK
	('UpLegFK_L',		upLegRoll, 'Hip_L', F_WIR, L_LEGFK, (1,1,1) ),
	('LoLegFK_L',		loLegRoll, 'UpLegFK_L', F_WIR, L_LEGFK, (1,1,1) ),
	('FootFK_L',		footRoll, 'LoLegFK_L', F_WIR, L_LEGFK, (1,1,1) ),
	('ToeFK_L',			toeRoll, 'FootFK_L', F_WIR, L_LEGFK, (1,1,1) ),
	('LegFK_L',			footCtrlRoll, 'ToeFK_L', 0, L_HELP, (1,1,1) ),
	('AnkleFK_L',		0, 'LoLegFK_L', 0, L_HELP, (1,1,1) ),

	('UpLegFK_R',		-upLegRoll, 'Hip_R', F_WIR, L_LEGFK, (1,1,1) ),
	('LoLegFK_R',		-loLegRoll, 'UpLegFK_R', F_WIR, L_LEGFK, (1,1,1) ),
	('FootFK_R',		-footRoll, 'LoLegFK_R', F_WIR, L_LEGFK, (1,1,1) ),
	('ToeFK_R',			-toeRoll, 'FootFK_R', F_WIR, L_LEGFK, (1,1,1) ),
	('LegFK_R',			-footCtrlRoll, 'ToeFK_R', 0, L_HELP, (1,1,1) ),
	('AnkleFK_R',		0, 'LoLegFK_L', 0, L_HELP, (1,1,1) ),

	# IK
	('UpLegIK_L',		upLegRoll, 'Hip_L', 0, L_LEGIK, (1,1,1) ),
	('LoLegIK_L',		loLegRoll, 'UpLegIK_L', 0, L_LEGIK, (1,1,1) ),
	('FootIK_L',		footRoll, 'LoLegIK_L', 0, L_HLPIK, (1,1,1)),
	('ToeIK_L',			toeRoll, 'FootIK_L', 0, L_HLPIK, (1,1,1)),
	('LegIK_L',			footCtrlRoll, None, F_WIR, L_LEGIK, (1,1,1) ),
	('ToeRevIK_L',		0, 'LegIK_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootRevIK_L',		0, 'ToeRevIK_L', F_WIR, L_LEGIK, (1,1,1)),
	('AnkleIK_L',		0, 'FootRevIK_L', 0, L_HELP, (1,1,1) ),

	('UpLegIK_R',		-upLegRoll, 'Hip_R', 0, L_LEGIK, (1,1,1) ),
	('LoLegIK_R',		-loLegRoll, 'UpLegIK_R', 0, L_LEGIK, (1,1,1) ),
	('FootIK_R',		-footRoll, 'LoLegIK_R', 0, L_HLPIK, (1,1,1)),
	('ToeIK_R',			-toeRoll, 'FootIK_R', 0, L_HLPIK, (1,1,1)),
	('LegIK_R',			-footCtrlRoll, None, F_WIR, L_LEGIK, (1,1,1) ),
	('ToeRevIK_R',		0, 'LegIK_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootRevIK_R',		0, 'ToeRevIK_R', F_WIR, L_LEGIK, (1,1,1)),
	('AnkleIK_R',		0, 'FootRevIK_R', 0, L_HELP, (1,1,1) ),

	# Pole target
	('KneePTIK_L',		0.0, 'Hip_L', F_WIR, L_LEGIK, (1,1,1)),
	('KneePTIK_R',		0.0, 'Hip_R', F_WIR, L_LEGIK, (1,1,1)),
	('KneeLinkPTIK_L',	0.0, 'UpLegIK_L', F_RES, L_LEGIK, (1,1,1)),
	('KneeLinkPTIK_R',	0.0, 'UpLegIK_R', F_RES, L_LEGIK, (1,1,1)),
	('KneePTFK_L',		0.0, 'UpLegFK_L', 0, L_HELP, (1,1,1)),
	('KneePTFK_R',		0.0, 'UpLegFK_R', 0, L_HELP, (1,1,1)),
]

#
#	LegWritePoses(fp):
#

limUpLeg_L = (-150*deg1,100*deg1, -30*deg1,30*deg1, -deg90,deg30)
limUpLeg_R = (-150*deg1,100*deg1, -30*deg1,30*deg1, -deg30,deg90)

limLoLeg_L = (0,150*deg1,-deg30,deg30, -deg30,deg30)
limLoLeg_R = (0,150*deg1,-deg30,deg30, -deg30,deg30)

limFoot_L = (-deg45,deg45, -deg30,deg30, -deg30,deg30)
limFoot_R = (-deg45,deg45, -deg30,deg30, -deg30,deg30)

limToe_L = (-deg45,deg45, 0,0, 0,0)
limToe_R = (-deg45,deg45, 0,0, 0,0)

limRevFoot_L = (-deg45,deg45, -deg30,deg30, -deg30,deg30)
limRevFoot_R = (-deg45,deg45, -deg30,deg30, -deg30,deg30)

limRevToe_L = (-deg45,deg45, 0,0, 0,0)
limRevToe_R = (-deg45,deg45, 0,0, 0,0)


def LegWritePoses(fp):
	# Deform 
	addPoseBone(fp, 'UpLegTwist_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, 1, ['IK', 'LoLeg_L', 1, None, (True, False,True)]),
		 ('CopyRot', C_LOCAL, 0, ['Rot', 'UpLeg_L', (0,1,0), (0,0,0), False])])

	addDeformLimb(fp, 'UpLeg_L', 'UpLegIK_L', (1,1,1), 'UpLegFK_L', (1,1,1), 0, P_STRETCH)

	addDeformLimb(fp, 'LoLeg_L', 'LoLegIK_L', (1,1,1), 'LoLegFK_L', (1,1,1), 0, P_STRETCH)

	addPoseBone(fp, 'LoLegFan_L', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', C_LOCAL, 0, ['Rot', 'LoLeg_L', (1,0,1), (0,0,0), False])])

	addDeformLimb(fp, 'Foot_L', 'FootIK_L', (1,1,1), 'FootFK_L', (1,1,1), 0, 0)

	addDeformLimb(fp, 'Toe_L', 'ToeIK_L', (1,1,1), 'ToeFK_L', (1,1,1), 0, 0)


	addPoseBone(fp, 'UpLegTwist_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, 1, ['IK', 'LoLeg_R', 1, None, (True, False,True)]),
		 ('CopyRot', C_LOCAL, 0, ['Rot', 'UpLeg_R', (0,1,0), (0,0,0), False])])

	addDeformLimb(fp, 'UpLeg_R', 'UpLegIK_R', (1,1,1), 'UpLegFK_R', (1,1,1), 0, P_STRETCH)

	addDeformLimb(fp, 'LoLeg_R', 'LoLegIK_R', (1,1,1), 'LoLegFK_R', (1,1,1), 0, P_STRETCH)

	addPoseBone(fp, 'LoLegFan_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', C_LOCAL, 0, ['Rot', 'LoLeg_R', (1,0,1), (0,0,0), False])])

	addDeformLimb(fp, 'Foot_R', 'FootIK_R', (1,1,1), 'FootFK_R', (1,1,1), 0, 0)

	addDeformLimb(fp, 'Toe_R', 'ToeIK_R', (1,1,1), 'ToeFK_R', (1,1,1), 0, 0)

	# Hip deform

	addPoseBone(fp, 'LegForward_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegForwardTrg_L', 'PLANE_X', 0]),
 		 ('LimitScale', C_OW_LOCAL, 0, ['LimitScale', (0,0, 0,0, 0,0), (0,1,0)])])

	addPoseBone(fp, 'LegBack_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegBackTrg_L', 'PLANE_X', 0])])

	addPoseBone(fp, 'LegOut_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegOutTrg_L', 'PLANE_X', 0])])


	addPoseBone(fp, 'LegForward_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegForwardTrg_R', 'PLANE_X', 0]),
 		 ('LimitScale', C_OW_LOCAL, 0, ['LimitScale', (0,0, 0,0, 0,0), (0,1,0)])])

	addPoseBone(fp, 'LegBack_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegBackTrg_R', 'PLANE_X', 0])])

	addPoseBone(fp, 'LegOut_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'LegOutTrg_R', 'PLANE_X', 0])])

	# FK
	addPoseBone(fp, 'UpLegFK_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_L, (1,1,1)])])

	addPoseBone(fp, 'LoLegFK_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_L, (1,1,1)])])

	addPoseBone(fp, 'FootFK_L', 'MHFoot', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limFoot_L, (1,1,1)])])

	addPoseBone(fp, 'ToeFK_L', 'MHToe', 'FK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limToe_L, (1,0,0)])])

	addPoseBone(fp, 'UpLegFK_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_R, (1,1,1)])])

	addPoseBone(fp, 'LoLegFK_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_R, (1,1,1)])])

	addPoseBone(fp, 'FootFK_R', 'MHFoot', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limFoot_R, (1,1,1)])])

	addPoseBone(fp, 'ToeFK_R', 'MHToe', 'FK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limToe_R, (1,0,0)])])


	# IK 
	addPoseBone(fp, 'UpLegIK_L', None, 'IK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_L, (1,1,1)])])

	addPoseBone(fp, 'UpLegIK_R', None, 'IK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_R, (1,1,1)])])

	addPoseBone(fp, 'LegIK_L', 'MHFootCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Hip', 'Hip_L', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 'fNoStretch', ['Hip_L', 'Hip_L'])])

	addPoseBone(fp, 'LegIK_R', 'MHFootCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Hip', 'Hip_R', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 'fNoStretch', ['Hip_R', 'Hip_R'])])

	addPoseBone(fp, 'LoLegIK_L', None, 'IK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, 1, ['IK', 'AnkleIK_L', 2, (-deg90, 'KneePTIK_L'), (1,0,1)]),
		('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_L, (1,1,1)])
		])

	addPoseBone(fp, 'LoLegIK_R', None, 'IK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, 1, ['IK', 'AnkleIK_R', 2, (-deg90, 'KneePTIK_R'), (1,0,1)]),
		('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_R, (1,1,1)])
		])

	addPoseBone(fp, 'FootRevIK_L', 'MHRevFoot', 'IK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevFoot_L, (1,1,1)])])

	addPoseBone(fp, 'FootRevIK_R', 'MHRevFoot', 'IK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevFoot_R, (1,1,1)])])

	addPoseBone(fp, 'ToeRevIK_L', 'MHRevToe', 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevToe_L, (1,1,1)])])

	addPoseBone(fp, 'ToeRevIK_R', 'MHRevToe', 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevToe_R, (1,1,1)])])
	
	addPoseBone(fp, 'FootIK_L', None, 'IK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, 1, ['IK', 'FootRevIK_L', 1, None, (1,0,1)])])

	addPoseBone(fp, 'FootIK_R', None, 'IK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, 1, ['IK', 'FootRevIK_R', 1, None, (1,0,1)])])

	addPoseBone(fp, 'ToeIK_L', None, 'IK_L', (1,1,1), (0,1,1), (1,1,0), (1,1,1), 0, 
		[('IK', 0, 1, ['IK', 'ToeRevIK_L', 1, None, (1,0,1)])])

	addPoseBone(fp, 'ToeIK_R', None, 'IK_R', (1,1,1), (0,1,1), (1,1,0), (1,1,1), 0, 
		[('IK', 0, 1, ['IK', 'ToeRevIK_R', 1, None, (1,0,1)])])
	
	# Pole target

	addPoseBone(fp, 'KneePTIK_L', 'MHCube025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'KneeLinkPTIK_L', None, 'IK_L', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'KneePTIK_L', 'PLANE_X', 0])])

	addPoseBone(fp, 'KneePTIK_R', 'MHCube025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'KneeLinkPTIK_R', None, 'IK_R', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'KneePTIK_R', 'PLANE_X', 0])])

	return

#
#	LegFKIKDrivers
#	(Bone, cond, FK constraint, IK constraint, driver, channel, max)
#

LegFKIKDrivers = [
	("UpLeg_L", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PLegIK_L", "LOC_X", 1.0),
	("LoLeg_L", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PLegIK_L", "LOC_X", 1.0),
	("Foot_L", True, ["RotFK"], ["RotIK"], "PLegIK_L", "LOC_X", 1.0),
	("Toe_L", True, ["RotFK"], ["RotIK"], "PLegIK_L", "LOC_X", 1.0),
	
	("UpLeg_R", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PLegIK_R", "LOC_X", 1.0),
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
		[("f", "UpLeg_L", "BendLegForwDown_L"), ("o", "UpLeg_L", "BendLegOut_L")], 
		[(0,1), (45*deg1,1), (deg60,0)]),
	("LegForward_L", "LimitScale",  None,
		[("f", "UpLeg_L", "BendLegForwUp_L")], 
		[(0,1), (deg30,1), (45*deg1,0)]),
	("LegBack_L", "Stretch",   None,
		[("b", "UpLeg_L", "BendLegBack_L"), ("o", "UpLeg_L", "BendLegOut_L")], 
		[(0,1), (deg60,1), (deg90,0)]),
	("LegOut_L", "Stretch",  None,
		[("o", "UpLeg_L", "BendLegOut_L")], 
		[(0,1), (deg60,1), (deg90,0)]),

	("LegForward_R", "Stretch",  None,
		[("f", "UpLeg_R", "BendLegForwDown_R"), ("o", "UpLeg_R", "BendLegOut_R")], 
		[(0,1), (45*deg1,1), (deg60,0)]),
	("LegForward_R", "LimitScale",  None,
		[("f", "UpLeg_R", "BendLegForwUp_R")], 
		[(0,1), (deg30,1), (45*deg1,0)]),
	("LegBack_R", "Stretch",  None,
		[("b", "UpLeg_R", "BendLegBack_R"), ("o", "UpLeg_R", "BendLegOut_R")], 
		[(0,1), (deg60,1), (deg90,0)]),
	("LegOut_R", "Stretch", None,
		 [("o", "UpLeg_R", "BendLegOut_R")], 
		[(0,1), (deg60,1), (deg90,0)]),
]

#
#	LegShapeDrivers
#	Shape : (driver, rotdiff, keypoints)
#

LegShapeDrivers = {
	'BendLegForward_L' : ( 'UpLegTwist_L', 'BendLegForward_L', [(0,0), (15*deg1,1), (deg90,0)] ),
	'BendLegBack_L' : ( 'UpLegTwist_L', 'BendLegBack_L', [(0,1), (deg90,0)] ),
	'BendLegOut_L' : ( 'UpLegTwist_L', 'BendLegOut_L', [(0,1), (deg90,0)] ),

	'BendLegForward_R' : ( 'UpLegTwist_R', 'BendLegForward_R', [(0,0), (15*deg1,1), (deg90,0)] ),
	'BendLegBack_R' : ( 'UpLegTwist_R', 'BendLegBack_R', [(0,1), (deg90,0)] ),
	'BendLegOut_R' : ( 'UpLegTwist_R', 'BendLegOut_R', [(0,1), (deg90,0)] ),
}
#
#	LegProcess
#	(bone, axis, angle)
#

LegProcess = [
	("UpLeg_L", "X", 0.2),
	("LoLeg_L", "X", -0.4),
	("Foot_L", "X", 0.2),

	("UpLeg_R", "X", 0.2),
	("LoLeg_R", "X", -0.4),
	("Foot_R", "X", 0.2),
]	

LegSnaps = [
	("UpLegFK_L", "UpLeg_L", 'Both'),
	("UpLegIK_L", "UpLeg_L", 'Both'),
	("LoLegFK_L", "LoLeg_L", 'Both'),
	("LoLegIK_L", "LoLeg_L", 'Both'),
	("FootFK_L", "Foot_L", 'Both'),
	("FootIK_L", "Foot_L", 'Both'),
	("FootRevIK_L", "Foot_L", 'Inv'),
	("ToeFK_L", "Toe_L", 'Both'),
	("ToeIK_L", "Toe_L", 'Both'),
	("ToeRevIK_L", "Toe_L", 'Inv'),

	("UpLegFK_R", "UpLeg_R", 'Both'),
	("UpLegIK_R", "UpLeg_R", 'Both'),
	("LoLegFK_R", "LoLeg_R", 'Both'),
	("LoLegIK_R", "LoLeg_R", 'Both'),
	("FootFK_R", "Foot_R", 'Both'),
	("FootIK_R", "Foot_R", 'Both'),
	("FootRevIK_R", "Foot_R", 'Inv'),
	("ToeFK_R", "Toe_R", 'Both'),
	("ToeIK_R", "Toe_R", 'Both'),
	("ToeRevIK_R", "Toe_R", 'Inv'),
]


LegParents = [
	('AnkleIK_L', 'LoLeg_L'),
	('LegIK_L', 'Foot_L'),
	('AnkleIK_R', 'LoLeg_R'),
	('LegIK_R', 'Foot_R'),
]

LegSelects = [
	'Foot_L', 'Toe_L', 'FootFK_L', 'ToeFK_L', 'FootIK_L', 'ToeIK_L', 'FootRevIK_L', 'ToeRevIK_L', 'LegIK_L', 
	'Foot_R', 'Toe_R', 'FootFK_R', 'ToeFK_R', 'FootIK_R', 'ToeIK_R', 'FootRevIK_R', 'ToeRevIK_R', 'LegIK_R', 
]	

LegRolls = [
	('LegIK_L', -0.23),
	('LegIK_R', 0.23),
	('FootRevIK_L', pi),
	('FootRevIK_R', pi),
]


