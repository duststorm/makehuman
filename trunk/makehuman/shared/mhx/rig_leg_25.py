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
Leg bone definitions 

"""

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
	('UpLeg_L',			'r-upper-leg', 'r-knee'),
	('UpLeg1_L',		'r-upper-leg', 'r-upleg1'),
	('UpLeg2_L',		'r-upleg1', 'r-upleg2'),
	('UpLeg3_L',		'r-upleg2', 'r-knee'),
	('LoLeg_L',			'r-knee', 'r-ankle'),
	('LoLegFan_L',		'r-knee', 'r-loleg-fan'),
	('Ankle_L',			'r-ankle', 'r-ankle-tip'),
	('Foot_L',			'r-ankle', 'r-foot-1'),
	('Toe_R',			'l-foot-1', 'l-foot-2'),
	('Leg_L',			'r-heel', 'r-foot-2'),
	('ToeRev_L',		'r-foot-2', 'r-foot-1'),
	('FootRev_L',		'r-foot-1', 'r-ankle'),
	('Ankle_L',			'r-ankle', 'r-ankle-tip'),

	('UpLeg_R',			'l-upper-leg', 'l-knee'),
	('UpLeg1_R',		'l-upper-leg', 'l-upleg1'),
	('UpLeg2_R',		'l-upleg1', 'l-upleg2'),
	('UpLeg3_R',		'l-upleg2', 'l-knee'),
	('LoLeg_R',			'l-knee', 'l-ankle'),
	('LoLegFan_R',		'l-knee', 'l-loleg-fan'),
	('Ankle_R',			'l-ankle', 'l-ankle-tip'),
	('Foot_R',			'l-ankle', 'l-foot-1'),
	('Toe_L',			'r-foot-1', 'r-foot-2'),
	('Leg_R',			'l-heel', 'l-foot-2'),
	('ToeRev_R',		'l-foot-2', 'l-foot-1'),
	('FootRev_R',		'l-foot-1', 'l-ankle'),
	('Ankle_R',			'l-ankle', 'l-ankle-tip'),

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

	# Pole Target
	('KneePT_L',			'r-knee-pt', ('r-knee-pt', offs)),
	('KneePT_R',			'l-knee-pt', ('l-knee-pt', offs)),
	('KneeLinkPT_L',		'r-knee', 'r-knee-pt'),
	('KneeLinkPT_R',		'l-knee', 'l-knee-pt'),
	('KneePTFK_L',			'r-knee-pt', ('r-knee-pt', offs)),
	('KneePTFK_R',			'l-knee-pt', ('l-knee-pt', offs)),
]

#
#	LegControlArmature
#

upLegRoll = 0
loLegRoll = 0
footRoll = 0
#toeRoll = -63.5*D
toeRoll = 135*D
footCtrlRoll = 0.0

LegControlArmature = [
	# Leg
	('UpLeg_L',			upLegRoll, 'Hips', F_WIR, L_LLEGFK, NoBB),
	('LoLeg_L',			loLegRoll, 'UpLeg_L', F_WIR, L_LLEGFK, NoBB),
	('Foot_L',			footRoll, 'LoLeg_L', F_WIR+F_CON, L_LLEGFK, NoBB),
	('Toe_L',			toeRoll, 'Foot_L', F_WIR, L_LLEGFK, NoBB),
	('Leg_L',			footCtrlRoll, Master, F_WIR, L_LLEGIK, NoBB),
	('ToeRev_L',		0, 'Leg_L', F_WIR, L_LLEGIK, NoBB),
	('FootRev_L',		0, 'ToeRev_L', F_WIR, L_LLEGIK, NoBB),
	('Ankle_L',			0, 'FootRev_L', 0, L_HELP, NoBB),

	('UpLeg_R',			-upLegRoll, 'Hips', F_WIR, L_RLEGFK, NoBB),
	('LoLeg_R',			-loLegRoll, 'UpLeg_R', F_WIR, L_RLEGFK, NoBB),
	('Foot_R',			-footRoll, 'LoLeg_R', F_WIR+F_CON, L_RLEGFK, NoBB),
	('Toe_R',			-toeRoll, 'Foot_R', F_WIR, L_RLEGFK, NoBB),
	('Leg_R',			-footCtrlRoll, Master, F_WIR, L_RLEGIK, NoBB),
	('ToeRev_R',		0, 'Leg_R', F_WIR, L_RLEGIK, NoBB),
	('FootRev_R',		0, 'ToeRev_R', F_WIR, L_RLEGIK, NoBB),
	('Ankle_R',			0, 'FootRev_R', 0, L_HELP, NoBB),

	# Pole target
	('KneePT_L',		0.0, 'Hips', F_WIR, L_LLEGIK, NoBB),
	('KneePT_R',		0.0, 'Hips', F_WIR, L_RLEGIK, NoBB),
	('KneeLinkPT_L',	0.0, 'UpLeg_L', F_RES, L_LLEGIK, NoBB),
	('KneeLinkPT_R',	0.0, 'UpLeg_R', F_RES, L_RLEGIK, NoBB),
]

#
#	LegDeformArmature
#

LegDeformArmature = [
	# Deform
	('UpLeg1_L',		upLegRoll, 'Hips', F_DEF, L_DEF, NoBB),
	('UpLeg2_L',		upLegRoll, 'UpLeg1_L', F_DEF+F_CON, L_MAIN,(0,0,5) ),
	('UpLeg3_L',		upLegRoll, 'UpLeg2_L', F_DEF+F_CON, L_MAIN, NoBB),
	('LoLeg_L',			loLegRoll, 'UpLeg3_L', F_DEF, L_MAIN, NoBB),
	('LoLegFan_L',		loLegRoll, 'UpLeg3_L', F_DEF, L_DEF, NoBB),
	('Foot_L',			footRoll, 'LoLeg_L', F_DEF+F_CON, L_MAIN, NoBB),
	('Toe_L',			toeRoll, 'Foot_L', F_DEF, L_MAIN, NoBB),

	('UpLeg1_R',		upLegRoll, 'Hips', F_DEF, L_DEF, NoBB),
	('UpLeg2_R',		upLegRoll, 'UpLeg1_R', F_DEF+F_CON, L_MAIN,(0,0,5) ),
	('UpLeg3_R',		upLegRoll, 'UpLeg2_R', F_DEF+F_CON, L_MAIN, NoBB),
	('LoLeg_R',			-loLegRoll, 'UpLeg3_R', F_DEF, L_MAIN, NoBB),
	('LoLegFan_R',		-loLegRoll, 'UpLeg3_R', F_DEF, L_DEF, NoBB),
	('Foot_R',			-footRoll, 'LoLeg_R', F_DEF+F_CON, L_MAIN, NoBB),
	('Toe_R',			-toeRoll, 'Foot_R', F_DEF, L_MAIN, NoBB),

	# Rotation diffs
	('BendLegForward_L',	pi, 'Hips', 0, L_HELP, NoBB),
	('BendLegBack_L',		0, 'Hips', 0, L_HELP, NoBB),
	('BendLegUp_L',			0, 'Hips', 0, L_HELP, NoBB),
	('BendLegDown_L',		0, 'Hips', 0, L_HELP, NoBB),
	('BendLegOut_L',		-90*D, 'Hips', 0, L_HELP, NoBB),

	('BendLegForward_R',	pi, 'Hips', 0, L_HELP, NoBB),
	('BendLegBack_R',		0, 'Hips', 0, L_HELP, NoBB),
	('BendLegUp_R',			0, 'Hips', 0, L_HELP, NoBB),
	('BendLegDown_R',		0, 'Hips', 0, L_HELP, NoBB),
	('BendLegOut_R',		90*D, 'Hips', 0, L_HELP, NoBB),

	# Hip deform
	('LegForward_L',		0, 'Hips', F_DEF, L_DEF, NoBB),
	('LegBack_L',			0, 'Hips', F_DEF, L_DEF, NoBB),
	('LegOut_L',			0, 'Hips', F_DEF, L_DEF, NoBB),
	('LegForwardTrg_L',		0, 'UpLeg1_L', 0, L_HELP, NoBB),
	('LegBackTrg_L',		0, 'UpLeg1_L', 0, L_HELP, NoBB),
	('LegOutTrg_L',			0, 'UpLeg1_L', 0, L_HELP, NoBB),

	('LegForward_R',		0, 'Hips', F_DEF, L_DEF, NoBB),
	('LegBack_R',			0, 'Hips', F_DEF, L_DEF, NoBB),
	('LegOut_R',			0, 'Hips', F_DEF, L_DEF, NoBB),
	('LegForwardTrg_R',		0, 'UpLeg1_R', 0, L_HELP, NoBB),
	('LegBackTrg_R',		0, 'UpLeg1_R', 0, L_HELP, NoBB),
	('LegOutTrg_R',			0, 'UpLeg1_R', 0, L_HELP, NoBB),

	# Knee deform
	('Knee_L',				0, 'UpLeg3_L', F_DEF, L_DEF, NoBB),
	('KneeTrg_L',			0, 'LoLeg_L', 0, L_HELP, NoBB),
	('Knee_R',				0, 'UpLeg3_R', F_DEF, L_DEF, NoBB),
	('KneeTrg_R',			0, 'LoLeg_R', 0, L_HELP, NoBB),

]

#
#	LegControlPoses(fp):
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

#
#	Rotation modes
#	Dmod = Deform rig mode
#	Cmod = Control rig mode
#

DmodUpLeg = P_YZX
DmodLoLeg = P_YZX
DmodFoot = P_YZX
DmodToe = P_YZX

CmodUpLeg = 0
CmodLoLeg = 0
CmodFoot = 0
CmodToe = 0

def LegControlPoses(fp):
	addPoseBone(fp, 'UpLeg_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+CmodUpLeg,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_L, (1,1,1)])])

	addPoseBone(fp, 'UpLeg_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+CmodUpLeg,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_R, (1,1,1)])])

	deltaKnee = -2.5*D

	addPoseBone(fp, 'LoLeg_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+CmodLoLeg,
		[('IK', 0, 0, ['LegIK', 'Ankle_L', 2, (-90*D+deltaKnee, 'KneePT_L'), (1,0,1)]),
		('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_L, (1,1,1)])
		])

	addPoseBone(fp, 'LoLeg_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+CmodLoLeg,
		[('IK', 0, 0, ['LegIK', 'Ankle_R', 2, (-90*D-deltaKnee, 'KneePT_R'), (1,0,1)]),
		('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_R, (1,1,1)])
		])

	addPoseBone(fp, 'Leg_L', 'MHFootCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Hip', 'Hips', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistHip', 'Hips', 'INSIDE'])])

	addPoseBone(fp, 'Leg_R', 'MHFootCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, 0, ['Hip', 'Hips', (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, 1, ['DistHip', 'Hips', 'INSIDE'])])

	addPoseBone(fp, 'FootRev_L', 'MHRevFoot', 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), CmodFoot, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevFoot_L, (1,1,1)])])

	addPoseBone(fp, 'FootRev_R', 'MHRevFoot', 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), CmodFoot,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevFoot_R, (1,1,1)])])

	addPoseBone(fp, 'ToeRev_L', 'MHRevToe', 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), CmodToe, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevToe_L, (1,1,1)])])

	addPoseBone(fp, 'ToeRev_R', 'MHRevToe', 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), CmodToe, 
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevToe_R, (1,1,1)])])
	
	addPoseBone(fp, 'Foot_L', 'MHFoot', 'FK_L', (0,0,0), (0,1,1), (1,1,1), (1,1,1), CmodFoot, 
		[('IK', 0, 0, ['RevIK', 'FootRev_L', 1, None, (1,0,1)]),
		 ('CopyRot', C_LOCAL, 0, ['RevRot', 'FootRev_L', (0,1,0), (0,0,0), True]),
		 ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,True)])])

	addPoseBone(fp, 'Foot_R', 'MHFoot', 'FK_R', (0,0,0), (0,1,1), (1,1,1), (1,1,1), CmodFoot, 
		[('IK', 0, 0, ['RevIK', 'FootRev_R', 1, None, (1,0,1)]),
		 ('CopyRot', C_LOCAL, 0, ['RevRot', 'FootRev_R', (0,1,0), (0,0,0), True]),
		 ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,True)])])

	addPoseBone(fp, 'Toe_L', 'MHToe_L', 'FK_L', (1,1,1), (0,1,1), (1,1,0), (1,1,1), CmodToe, 
		[('IK', 0, 0, ['RevIK', 'ToeRev_L', 1, None, (1,0,1)])])

	addPoseBone(fp, 'Toe_R', 'MHToe_R', 'FK_R', (1,1,1), (0,1,1), (1,1,0), (1,1,1), CmodToe, 
		[('IK', 0, 0, ['RevIK', 'ToeRev_R', 1, None, (1,0,1)])])
	
	# Pole target

	addPoseBone(fp, 'KneePT_L', 'MHCube025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'KneeLinkPT_L', None, 'IK_L', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'KneePT_L', 0])])

	addPoseBone(fp, 'KneePT_R', 'MHCube025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'KneeLinkPT_R', None, 'IK_R', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', 0, 1, ['Stretch', 'KneePT_R', 0])])

	return

#
#	LegDeformPoses(fp):
#

def LegDeformPoses(fp):
	# Deform 
	copyDeformPartial(fp, 'UpLeg1_L', 'UpLeg_L', (1,0,1), DmodUpLeg, U_LOC+U_ROT+U_SCALE, None, [])
	
	copyDeformPartial(fp, 'UpLeg2_L', 'UpLeg_L', (1,1,1), DmodUpLeg, U_SCALE, 'MHDefUpLeg2', [])
		
	copyDeformPartial(fp, 'UpLeg3_L', 'UpLeg_L', (0,1,0), DmodUpLeg, U_ROT+U_SCALE, 'MHDefUpLeg3', [])

	copyDeform(fp, 'LoLeg_L', DmodLoLeg, U_LOC+U_ROT+U_SCALE, 'MHDefLeg', [])

	addPoseBone(fp, 'LoLegFan_L', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), DmodLoLeg,
		[('CopyRot', C_LOCAL, 0, ['Rot', 'LoLeg_L', (1,0,1), (0,0,0), False])])

	copyDeform(fp, 'Foot_L', DmodFoot, U_LOC+U_ROT, 'MHDefFoot', [])

	copyDeform(fp, 'Toe_L', DmodToe, U_LOC+U_ROT, 'MHDefToe', [])


	copyDeformPartial(fp, 'UpLeg1_R', 'UpLeg_R', (1,0,1), DmodUpLeg, U_LOC+U_ROT+U_SCALE, None, [])
	
	copyDeformPartial(fp, 'UpLeg2_R', 'UpLeg_R', (1,1,1), DmodUpLeg, U_SCALE, 'MHDefUpLeg2', [])
		
	copyDeformPartial(fp, 'UpLeg3_R', 'UpLeg_R', (0,1,0), DmodUpLeg, U_ROT+U_SCALE, 'MHDefUpLeg3', [])

	copyDeform(fp, 'LoLeg_R', DmodLoLeg, U_LOC+U_ROT+U_SCALE, 'MHDefLeg', [])

	addPoseBone(fp, 'LoLegFan_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), DmodLoLeg,
		[('CopyRot', C_LOCAL, 0, ['Rot', 'LoLeg_R', (1,0,1), (0,0,0), False])])

	copyDeform(fp, 'Foot_R', DmodFoot, U_LOC+U_ROT, 'MHDefFoot', [])

	copyDeform(fp, 'Toe_R', DmodToe, U_LOC+U_ROT, 'MHDefToe', [])


	# Hip deform

	addPoseBone(fp, 'LegForward_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegForwardTrg_L', 0]),
 		 ('LimitScale', C_OW_LOCAL, 0, ['Scale', (0,0, 0,0, 0,0), (0,1,0)])])

	addPoseBone(fp, 'LegBack_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegBackTrg_L', 0])])

	addPoseBone(fp, 'LegOut_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegOutTrg_L', 0])])


	addPoseBone(fp, 'LegForward_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegForwardTrg_R', 0]),
 		 ('LimitScale', C_OW_LOCAL, 0, ['Scale', (0,0, 0,0, 0,0), (0,1,0)])])

	addPoseBone(fp, 'LegBack_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegBackTrg_R', 0])])

	addPoseBone(fp, 'LegOut_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegOutTrg_R', 0])])

	# Knee deform

	addPoseBone(fp, 'Knee_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'KneeTrg_L', 0])])

	addPoseBone(fp, 'Knee_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('StretchTo', C_DEFRIG, 1, ['Stretch', 'KneeTrg_R', 0])])

	return

#
#	LegFKIKDrivers
#	(Bone, cond, FK constraint, IK constraint, driver, channel, max)
#

LegFKIKDrivers = [
	("UpLeg_L", True, [], [], "PLegIK_L", "LOC_X", 1.0),
	("LoLeg_L", True, [], ["LegIK"], "PLegIK_L", "LOC_X", 1.0),
	("Foot_L", True, ["FreeIK"], ["RevIK", "RevRot"], "PLegIK_L", "LOC_X", 1.0),
	("Toe_L", True, [], ["RevIK"], "PLegIK_L", "LOC_X", 1.0),
	
	("UpLeg_R", True, [], [], "PLegIK_R", "LOC_X", 1.0),
	("LoLeg_R", True, [], ["LegIK"], "PLegIK_R", "LOC_X", 1.0),
	("Foot_R", True, ["FreeIK"], ["RevIK", "RevRot"], "PLegIK_R", "LOC_X", 1.0),
	("Toe_R", True, [], ["RevIK"], "PLegIK_R", "LOC_X", 1.0),
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




