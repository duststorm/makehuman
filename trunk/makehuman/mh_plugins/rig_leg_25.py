#
#	Leg bone definitions
#

import mhx_rig
from mhx_rig import *

LegJoints = [
	# Deform
	('r-upper-leg',			'j', 'r-upper-leg'),
	('r-knee',			'j', 'r-knee'),
	('r-ankle',			'j', 'r-ankle'),
	('r-ball',			'v', 5742),
	('r-heel',			'v', 5721),
	('r-toes-tip',			'v', 12262),
	('r-ankle-tip',			'o', ('r-ankle', [0.0, 0.0, -1.0])),

	('l-upper-leg',			'j', 'l-upper-leg'),
	('l-knee',			'j', 'l-knee'),
	('l-ankle',			'j', 'l-ankle'),
	('l-ball',			'v', 13320),
	('l-heel',			'v', 13338),
	('l-toes-tip',			'v', 13254),
	('l-ankle-tip',			'o', ('l-ankle', [0.0, 0.0, -1.0])),

	# Control classic
	('footCtrl_L_vec',		'l', ((1,'r-toes-tip'), (-1, 'r-heel'))),
	('legRoot_L_head',		'l', ((1,'r-upper-leg'), (-1,'Root_offs'))),
	('footCtrl_R_vec',		'l', ((1,'l-toes-tip'), (-1, 'l-heel'))),
	('legRoot_R_head',		'l', ((1,'l-upper-leg'), (-1,'Root_offs'))),

	# Knee pole target
	('knee_L_tail'	,		'o', ('r-knee', [0,0,6.0])),
	('knee_L_head'	,		'o', ('knee_L_tail', [0,-0.6,0])),
	('knee_R_tail'	,		'o', ('l-knee', [0,0,6.0])),
	('knee_R_head'	,		'o', ('knee_R_tail', [0,-0.6,0])),

	# Control gobo
	('foot_L_center',		'v', 5736),
	('footGobo_L_head',		'o', ('r-ankle', [0,-0.3,-0.3])),
	('footGobo_L_tail',		'o', ('footGobo_L_head', [0,1.5,0])),
	('tiptoe_L_head',		'b', 'r-toes-tip'),
	('tipr-toes-tip',		'o', ('tiptoe_L_head', [0,0.6,0])),
	('tumble_out_L_head',		'l', ((1.25, 'foot_L_center'), (-0.25, 'foot_R_center'))),
	('tumble_out_L_tail',		'o', ('tumble_out_L_head', [0,0.6,0])),
	('tumble_in_L_head',		'l', ((0.7, 'foot_L_center'), (0.3, 'foot_R_center'))),
	('tumble_in_L_tail',		'o', ('tumble_in_L_head', [0,0.6,0])),
	('heel_L_tail'	,		'o', ('r-heel', [0,0.6,0])),
	('rotate_toe_L_head',		'b', 'r-ball'),
	('rotate_r-toes-tip',		'o', ('rotate_toe_L_head', [0,0.6,0])),
	('toe_target_L_head',		'b', 'r-toes-tip'),
	('toe_target_L_tail',		'l', ((2, 'r-toes-tip'), (-1, 'r-ball'))),
	('foot_target_L_head',		'b', 'r-ball'),
	('foot_target_L_tail',		'l', ((2, 'r-ball'), (-1, 'r-ankle'))),
	('leg_target_L_head',		'b', 'r-ankle'),
	('leg_target_L_tail',		'l', ((2, 'r-ankle'), (-1, 'r-knee'))),
	('foot_tumble_L_head',		'o', ('tiptoe_L_head', [0,1.0,0])),
	('foot_tumble_L_tail',		'o', ('foot_tumble_L_head', [0,0.6,0])),
	('foot_roll_L_head',		'o', ('r-toes-tip', [0.3,0,0.6])),
	('foot_roll_L_tail',		'o', ('foot_roll_L_head', [-0.6,0,0])),

	('foot_R_center',		'v', 13326),
	('footGobo_R_head',		'o', ('l-ankle', [0,-0.3,-0.3])),
	('footGobo_R_tail',		'o', ('footGobo_R_head', [0,1.5,0])),
	('tiptoe_R_head',		'b', 'l-toes-tip'),
	('tipl-toes-tip',		'o', ('tiptoe_R_head', [0,0.6,0])),
	('tumble_out_R_head',		'l', ((1.25, 'foot_R_center'), (-0.25, 'foot_L_center'))),
	('tumble_out_R_tail',		'o', ('tumble_out_R_head', [0,0.6,0])),
	('tumble_in_R_head',		'l', ((0.7, 'foot_R_center'), (0.3, 'foot_L_center'))),
	('tumble_in_R_tail',		'o', ('tumble_in_R_head', [0,0.6,0])),
	('heel_R_tail'	,		'o', ('l-heel', [0,0.6,0])),
	('rotate_toe_R_head',		'b', 'l-ball'),
	('rotate_l-toes-tip',		'o', ('rotate_toe_R_head', [0,0.6,0])),
	('toe_target_R_head',		'b', 'l-toes-tip'),
	('toe_target_R_tail',		'l', ((2, 'l-toes-tip'), (-1, 'l-ball'))),
	('foot_target_R_head',		'b', 'l-ball'),
	('foot_target_R_tail',		'l', ((2, 'l-ball'), (-1, 'l-ankle'))),
	('leg_target_R_head',		'b', 'l-ankle'),
	('leg_target_R_tail',		'l', ((2, 'l-ankle'), (-1, 'l-knee'))),
	('foot_tumble_R_head',		'o', ('tiptoe_R_head', [0,1.0,0])),
	('foot_tumble_R_tail',		'o', ('foot_tumble_R_head', [0,0.6,0])),
	('foot_roll_R_head',		'o', ('l-toes-tip', [0.3,0,0.6])),
	('foot_roll_R_tail',		'o', ('foot_roll_R_head', [-0.6,0,0])),

]

LegHeadsTails = [
	# Root
	('Hip_L',			'pelvis', 'r-upper-leg'),
	('LegRoot_L',			'legRoot_L_head', 'r-upper-leg'),
	('LegRootShadow_L',		'legRoot_L_head', 'r-upper-leg'),

	('Hip_R',			'pelvis', 'l-upper-leg'),
	('LegRoot_R',			'legRoot_R_head', 'l-upper-leg'),
	('LegRootShadow_R',		'legRoot_R_head', 'l-upper-leg'),

	# Deform 
	('UpLegTwist_L',		'r-upper-leg', 'r-knee'),
	('UpLeg_L',			'r-upper-leg', 'r-knee'),
	('LoLeg_L',			'r-knee', 'r-ankle'),
	('Foot_L',			'r-ankle', 'r-ball'),
	('Toe_L',			'r-ball', 'r-toes-tip'),

	('UpLegTwist_R',		'l-upper-leg', 'l-knee'),
	('UpLeg_R',			'l-upper-leg', 'l-knee'),
	('LoLeg_R',			'l-knee', 'l-ankle'),
	('Foot_R',			'l-ankle', 'l-ball'),
	('Toe_R',			'l-ball', 'l-toes-tip'),

	# FK
	('UpLegFK_L',			'r-upper-leg', 'r-knee'),
	('LoLegFK_L',			'r-knee', 'r-ankle'),
	('FootFK_L',			'r-ankle', 'r-ball'),
	('ToeFK_L',			'r-ball', 'r-toes-tip'),
	('UpLegFK_R',			'l-upper-leg', 'l-knee'),
	('LoLegFK_R',			'l-knee', 'l-ankle'),
	('FootFK_R',			'l-ankle', 'l-ball'),
	('ToeFK_R',			'l-ball', 'l-toes-tip'),
	
	# IK common
	('UpLegIK_L',			'r-upper-leg', 'r-knee'),
	('LoLegIK_L',			'r-knee', 'r-ankle'),
	('UpLegIK_R',			'l-upper-leg', 'l-knee'),
	('LoLegIK_R',			'l-knee', 'l-ankle'),
	('LegIK_L',			'r-ankle', 'r-ankle-tip'),
	('LegIK_R',			'l-ankle', 'l-ankle-tip'),
	('FootIK_L',			'r-ankle', 'r-ball'),
	('FootIK_R',			'l-ankle', 'l-ball'),
	('ToeIK_L',			'r-ball', 'r-toes-tip'),
	('ToeIK_R',			'l-ball', 'l-toes-tip'),

	# IK pole target
	('KneePT_L',			'knee_L_head', 'knee_L_tail'),
	('KneePT_R',			'knee_R_head', 'knee_R_tail'),
	('KneeHandle_L',		'r-knee', 'knee_L_head'),
	('KneeHandle_R',		'l-knee', 'knee_R_head'),

	# IK rev foot
	('FootCtrl_L',			'r-heel', 'r-toes-tip'),
	('FootCtrl_R',			'l-heel', 'l-toes-tip'),
	('ToeRevIK_L',			'r-toes-tip', 'r-ball'),
	('ToeRevIK_R',			'l-toes-tip', 'l-ball'),
	('FootRevIK_L',			'r-ball', 'r-ankle'),
	('FootRevIK_R',			'l-ball', 'l-ankle'),
	('Ankle_L',			'r-ankle', 'r-ankle-tip'),
	('Ankle_R',			'l-ankle', 'l-ankle-tip'),

	# IK gobo
	('Heel_L',			'r-heel', 'heel_L_tail'),
	('Heel_R',			'l-heel', 'heel_R_tail'),
	('FootGobo_L',			'footGobo_L_head', 'footGobo_L_tail'),
	('FootGobo_R',			'footGobo_R_head', 'footGobo_R_tail'),

	('TipToe_L',			'tiptoe_L_head', 'tipr-toes-tip'),
	('TumbleOut_L',			'tumble_out_L_head', 'tumble_out_L_tail'),
	('TumbleIn_L',			'tumble_in_L_head', 'tumble_in_L_tail'),
	('RotateToe_L',			'rotate_toe_L_head', 'rotate_r-toes-tip'),
	('ToeTarget_L',			'toe_target_L_head', 'toe_target_L_tail'),
	('FootTarget_L',		'foot_target_L_head', 'foot_target_L_tail'),
	('LegTarget_L',			'leg_target_L_head', 'leg_target_L_tail'),
	('FootTumble_L',		'foot_tumble_L_head', 'foot_tumble_L_tail'),
	('FootRoll_L',			'foot_roll_L_head', 'foot_roll_L_tail'),

	('TipToe_R',			'tiptoe_R_head', 'tipl-toes-tip'),
	('TumbleOut_R',			'tumble_out_R_head', 'tumble_out_R_tail'),
	('TumbleIn_R',			'tumble_in_R_head', 'tumble_in_R_tail'),
	('RotateToe_R',			'rotate_toe_R_head', 'rotate_l-toes-tip'),
	('ToeTarget_R',			'toe_target_R_head', 'toe_target_R_tail'),
	('FootTarget_R',		'foot_target_R_head', 'foot_target_R_tail'),
	('LegTarget_R',			'leg_target_R_head', 'leg_target_R_tail'),
	('FootTumble_R',		'foot_tumble_R_head', 'foot_tumble_R_tail'),
	('FootRoll_R',			'foot_roll_R_head', 'foot_roll_R_tail'),

]

hipRoll = 1.62316
upLegRoll = -3.08923
loLegRoll = deg180
footRoll = deg180
toeRoll = -2.813
footCtrlRoll = -2.597

LegArmature = [
	# Root
	('Hip_L', 'True',		0.0, 'Hips', F_DEF, L_DEF, (1,1,1) ),
	('LegRoot_L', 'True',		0.0, 'Hip_L', 0, L_HELP, (1,1,1) ),
	
	('Hip_R', 'True',		0.0, 'Hips', F_DEF, L_DEF, (1,1,1) ),
	('LegRoot_R', 'True',		0.0, 'Hip_R', 0, L_HELP, (1,1,1) ),
	
	# Deform
	('UpLeg_L', 'True',		upLegRoll, 'LegRoot_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpLegTwist_L', 'True',	upLegRoll, 'LegRoot_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoLeg_L', 'True',		loLegRoll, 'UpLeg_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Foot_L', 'True',		footRoll, 'LoLeg_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Toe_L', 'True',		toeRoll, 'Foot_L', F_DEF+F_CON, L_DEF, (1,1,1) ),

	('UpLeg_R', 'True',		-upLegRoll, 'LegRoot_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpLegTwist_R', 'True',	-upLegRoll, 'LegRoot_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoLeg_R', 'True',		-loLegRoll, 'UpLeg_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Foot_R', 'True',		-footRoll, 'LoLeg_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Toe_R', 'True',		-toeRoll, 'Foot_R', F_DEF+F_CON, L_DEF, (1,1,1) ),

	# FK
	('UpLegFK_L', 'True',		upLegRoll, 'LegRoot_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('LoLegFK_L', 'True',		loLegRoll, 'UpLegFK_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('FootFK_L', 'True',		footRoll, 'LoLegFK_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('ToeFK_L', 'True',		toeRoll, 'FootFK_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),

	('UpLegFK_R', 'True',		-upLegRoll, 'LegRoot_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('LoLegFK_R', 'True',		-loLegRoll, 'UpLegFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('FootFK_R', 'True',		-footRoll, 'LoLegFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('ToeFK_R', 'True',		-toeRoll, 'FootFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),

	# IK Common
	('UpLegIK_L', 'True',		upLegRoll, 'LegRoot_L', F_CON, L_HLPIK, (1,1,1) ),
	('LoLegIK_L', 'True',		loLegRoll, 'UpLegIK_L', F_CON, L_HLPIK, (1,1,1) ),
	('FootIK_L', 'True',		footRoll, 'LoLegIK_L', F_CON, L_HLPIK, (1,1,1)),
	('ToeIK_L', 'True',		toeRoll, 'FootIK_L', F_CON, L_HLPIK, (1,1,1)),

	('UpLegIK_R', 'True',		-upLegRoll, 'LegRoot_R', F_CON, L_HLPIK, (1,1,1) ),
	('LoLegIK_R', 'True',		-loLegRoll, 'UpLegIK_R', F_CON, L_HLPIK, (1,1,1) ),
	('FootIK_R', 'True',		-footRoll, 'LoLegIK_R', F_CON, L_HLPIK, (1,1,1)),
	('ToeIK_R', 'True',		-toeRoll, 'FootIK_R', F_CON, L_HLPIK, (1,1,1)),

	# IK Inverse foot
	('FootCtrl_L', 'rigLeg&T_InvFoot',	footCtrlRoll, 'Root', F_WIR, L_LEGIK, (1,1,1) ),
	('ToeRevIK_L', 'rigLeg&T_InvFoot',	0, 'FootCtrl_L', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('FootRevIK_L', 'rigLeg&T_InvFoot',	deg180, 'ToeRevIK_L', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('Ankle_L', 'rigLeg&T_InvFoot',		deg180, 'FootRevIK_L', F_CON+F_CON, L_HELP, (1,1,1) ),
	('KneePT_L', 'rigLeg&T_InvFoot',	0.0, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),

	('FootCtrl_R', 'rigLeg&T_InvFoot',	-footCtrlRoll, 'Root', F_WIR, L_LEGIK, (1,1,1) ),
	('ToeRevIK_R', 'rigLeg&T_InvFoot',	0, 'FootCtrl_R', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('FootRevIK_R', 'rigLeg&T_InvFoot',	deg180, 'ToeRevIK_R', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('Ankle_R', 'rigLeg&T_InvFoot',		deg180, 'FootRevIK_R', F_CON, L_HELP, (1,1,1) ),
	('KneePT_R', 'rigLeg&T_InvFoot',	0.0, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),

	# IK Gobo
	('LegTarget_L', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_L', F_RES, L_HELP, (1,1,1)),
	('LegTarget_R', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_R', F_RES, L_HELP, (1,1,1)),
	('FootGobo_L', 'rigLeg&T_GoboFoot',	0.0, 'Root', F_WIR, L_LEGIK, (1,1,1)),
	('FootGobo_R', 'rigLeg&T_GoboFoot',	0.0, 'Root', F_WIR, L_LEGIK, (1,1,1)),
	('KneePT_L', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_L', F_WIR, L_LEGIK, (1,1,1)),
	('KneePT_R', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_R', F_WIR, L_LEGIK, (1,1,1)),

	('TipToe_L', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_L', F_WIR, L_LEGIK, (1,1,1)),
	('TumbleOut_L', 'rigLeg&T_GoboFoot',	0.0, 'TipToe_L', F_RES, L_HELP, (1,1,1)),
	('TumbleIn_L', 'rigLeg&T_GoboFoot',	0.0, 'TumbleOut_L', F_RES, L_HELP, (1,1,1)),
	('Heel_L', 'rigLeg&T_GoboFoot',		0.0, 'TumbleIn_L', F_RES, L_HELP, (1,1,1)),
	('RotateToe_L', 'rigLeg&T_GoboFoot',	0.0, 'Heel_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootTumble_L', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootRoll_L', 'rigLeg&T_GoboFoot',	-deg90, 'FootGobo_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootTarget_L', 'rigLeg&T_GoboFoot',	2.779, 'Heel_L', F_RES, L_HELP, (1,1,1)),
	('ToeTarget_L', 'rigLeg&T_GoboFoot',	toeRoll, 'RotateToe_L', F_RES, L_HELP, (1,1,1)),

	('TipToe_R', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_R', F_WIR, L_LEGIK, (1,1,1)),
	('TumbleOut_R', 'rigLeg&T_GoboFoot',	0.0, 'TipToe_R', F_RES, L_HELP, (1,1,1)),
	('TumbleIn_R', 'rigLeg&T_GoboFoot',	0.0, 'TumbleOut_R', F_RES, L_HELP, (1,1,1)),
	('Heel_R', 'rigLeg&T_GoboFoot',		0.0, 'TumbleIn_R', F_RES, L_HELP, (1,1,1)),
	('RotateToe_R', 'rigLeg&T_GoboFoot',	0.0, 'Heel_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootTumble_R', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootRoll_R', 'rigLeg&T_GoboFoot',	-deg90, 'FootGobo_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootTarget_R', 'rigLeg&T_GoboFoot',	-2.779, 'Heel_R', F_RES, L_HELP, (1,1,1)),
	('ToeTarget_R', 'rigLeg&T_GoboFoot',	-toeRoll, 'RotateToe_R', F_RES, L_HELP, (1,1,1)),

	# Both

	('KneeHandle_L', True,			0.0, 'UpLeg_L', F_RES, L_LEGIK, (1,1,1)),
	('KneeHandle_R', True,			0.0, 'UpLeg_R', F_RES, L_LEGIK, (1,1,1)),
]

limUpLeg_L = (-60*deg1,140*deg1, -70*deg1,70*deg1, -deg45,deg90)
limUpLeg_R = (-60*deg1,140*deg1, -70*deg1,70*deg1, -deg90,deg45)

limLoLeg_L = (-140*deg1,0, 0,0, 0,0)
limLoLeg_R = (-140*deg1,0, 0,0, 0,0)

limFoot_L = (-deg45,deg45, 0,0, 0,0)
limFoot_R = (-deg45,deg45, 0,0, 0,0)

limToe_L = (-deg45,deg45, 0,0, 0,0)
limToe_R = (-deg45,deg45, 0,0, 0,0)

limRevFoot_L = (-deg45,deg45, 0,0, 0,0)
limRevFoot_R = (-deg45,deg45, 0,0, 0,0)

limRevToe_L = (-deg45,deg45, 0,0, 0,0)
limRevToe_R = (-deg45,deg45, 0,0, 0,0)


def LegWritePoses(fp):
	global boneGroups
	boneGroups = {}

	# Root
	
	addPoseBone(fp, True, 'LegRoot_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, True, 'LegRoot_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])	

	# Deform 
	addPoseBone(fp, 'True', 'UpLeg_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'UpLegIK_L', 'fLegIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'UpLegFK_L', '1-fLegIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'True', 'UpLegTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		#[('IK', 0, ['IK', 'LoLeg_L', 1, None, (True, False), 1.0])])
		[('CopyRot', 0, ['UnTwist', 'UpLeg_L', 'True', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'True', 'LoLeg_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'LoLegIK_L', 'fLegIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'LoLegFK_L', '1-fLegIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'True', 'Foot_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'FootIK_L', 'fLegIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'FootFK_L', '1-fLegIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'True', 'Toe_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'ToeIK_L', 'fLegIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'ToeFK_L', '1-fLegIK', (1,1,1), (0,0,0), False])])


	addPoseBone(fp, 'True', 'UpLeg_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'UpLegIK_R', 'fLegIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'UpLegFK_R', '1-fLegIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'True', 'UpLegTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		#[('IK', 0, ['IK', 'LoLeg_R', 1, None, (True, False), 1.0])])
		[('CopyRot', 0, ['UnTwist', 'UpLeg_R', 'True', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'True', 'LoLeg_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'LoLegIK_R', 'fLegIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'LoLegFK_R', '1-fLegIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'True', 'Foot_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'FootIK_R', 'fLegIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'FootFK_R', '1-fLegIK', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, 'True', 'Toe_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'ToeIK_R', 'fLegIK', (1,1,1), (0,0,0), False]),
		('CopyRot', 0, ['ConstFK', 'ToeFK_R', '1-fLegIK', (1,1,1), (0,0,0), False])])


	# FK
	addPoseBone(fp, 'True', 'UpLegFK_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpLeg_L, (1,1,1)])])

	addPoseBone(fp, 'True', 'LoLegFK_L', 'MHCircle025', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_L, (1,0,0)])])

	addPoseBone(fp, 'True', 'FootFK_L', 'MHFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limFoot_L, (1,0,0)])])

	addPoseBone(fp, 'True', 'ToeFK_L', 'MHToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limToe_L, (1,0,0)])])

	addPoseBone(fp, 'True', 'UpLegFK_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpLeg_R, (1,1,1)])])

	addPoseBone(fp, 'True', 'LoLegFK_R', 'MHCircle025', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_R, (1,0,0)])])

	addPoseBone(fp, 'True', 'FootFK_R', 'MHFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limFoot_R, (1,0,0)])])

	addPoseBone(fp, 'True', 'ToeFK_R', 'MHToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limToe_R, (1,0,0)])])



	# IK reverse foot

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootCtrl_L', 'MHFootCtrl_L', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['World', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Local', 'LegRoot_L', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'LegRoot_L'])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootCtrl_R', 'MHFootCtrl_R', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['World', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Local', 'LegRoot_R', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'LegRoot_R'])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'LoLegIK_L', None, 'ik', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Ankle_L', 2, (deg90, 'KneePT_L'), (True, False), 1.0]),
		 ('LimitRot', C_OW_LOCAL, ['LimitRot', limFoot_L, (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'LoLegIK_R', None, 'ik', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Ankle_R', 2, (deg90, 'KneePT_R'), (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limFoot_R, (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootRevIK_L', 'MHRevFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevFoot_L, (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootRevIK_R', 'MHRevFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevFoot_R, (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootIK_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootRevIK_L', 1, None, (True, False), 1.0])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootIK_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootRevIK_R', 1, None, (True, False), 1.0])]),

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'ToeRevIK_L', 'MHRevToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevToe_L, (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'ToeRevIK_R', 'MHRevToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevToe_R, (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'ToeIK_L', None, None, (1,1,1), (0,1,1), (1,1,0), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeRevIK_L', 1, None, (True, False), 1.0])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'ToeIK_R', None, None, (1,1,1), (0,1,1), (1,1,0), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeRevIK_R', 1, None, (True, False), 1.0])]),

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'KneePT_L', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Root', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Foot', 'FootCtrl_L', 0.0, (1,1,1), (1,1,1), (1,1,1)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'KneePT_R', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Root', 'FootCtrl_R', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Foot', 'FootCtrl_R', 0.0, (1,1,1), (1,1,1), (1,1,1)])])



	# IK Gobo
		
	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'LoLegIK_L', None, 'ik', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'LegTarget_L', 2, (1.2708, 'KneePT_L'), (True, False), 1.0]),
		 ('LimitRot', C_OW_LOCAL, ['LimitRot', (-2.6,0, 0,0, 0,0), (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'LoLegIK_R', None, 'ik', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'LegTarget_R', 2, (1.8708, 'KneePT_R'), (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-2.6,0, 0,0, 0,0), (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootGobo_L', 'GoboFootCtrl_L', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['ChildOf', 'LegRoot_L', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'LegRoot_L'])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootGobo_R', 'GoboFootCtrl_R', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['ChildOf', 'LegRoot_R', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'LegRoot_R'])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'KneePT_L', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Root', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Foot', 'FootGobo_L', 0.0, (1,1,1), (1,1,1), (1,1,1)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'KneePT_R', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Root', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Foot', 'FootGobo_R', 0.0, (1,1,1), (1,1,1), (1,1,1)])])



	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootIK_L', 'MHFoot', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootTarget_L', 1, None, (True, True), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'ToeIK_L', 'MHToe', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeTarget_L', 1, None, (True, True), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TipToe_L', 'GoboTipToe_L', None, (1,1,1), (0,0,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (0,2.96706, 0,0, 0,0), (1,0,0)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootRoll_L', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (1,1, 0,0, 0,0)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootTumble_L', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (1,1, 0,0, 0,0)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TumbleOut_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootTumble', 'FootTumble_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TumbleIn_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootTumble', 'FootTumble_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'Heel_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootRoll', 'FootRoll_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'RotateToe_L', 'GoboRotate_L', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootTarget_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootRoll', 'FootRoll_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])


	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootIK_R', 'MHFoot', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootTarget_R', 1, None, (True, True), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'ToeIK_R', 'MHToe', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeTarget_R', 1, None, (True, True), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TipToe_R', 'GoboTipToe_R', None, (1,1,1), (0,0,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (0,2.96706, 0,0, 0,0), (1,0,0)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootRoll_R', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (1,1, 0,0, 0,0)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootTumble_R', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (1,1, 0,0, 0,0)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TumbleOut_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootTumble', 'FootTumble_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TumbleIn_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootTumble', 'FootTumble_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'Heel_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootRoll', 'FootRoll_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'RotateToe_R', 'GoboRotate_R', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootTarget_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootRoll', 'FootRoll_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])


	# IK both

	addPoseBone(fp, True, 'KneeHandle_L', None, 'ik', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['StretchTo', 'KneePT_L', 'X'])])

	addPoseBone(fp, True, 'KneeHandle_R', None, 'ik', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['StretchTo', 'KneePT_R', 'X'])])

	return

#
#	LegWriteActions(fp)
#

actionFootTumble = [
	('TumbleIn_L',  [ (1, 0.7071, 0, 0, 0.7071),  (11, 1, 0, 0, 0),  (21, 1, 0, 0, 0) ]),
	('TumbleIn_R',  [ (1, 1, 0, 0, 0),  (11, 1, 0, 0, 0),  (21, 0.7071, 0, 0, -0.7071) ]),
	('TumbleOut_L',  [ (1, 1, 0, 0, 0),  (11, 1, 0, 0, 0),  (21, 0.7071, 0, 0, -0.7071) ]),
	('TumbleOut_R',  [ (1, 0.7071, 0, 0, 0.7071),  (11, 1, 0, 0, 0),  (21, 1, 0, 0, 0) ]),
]

actionFootRoll = [
	('FootTarget_L',  [ (1, 1, 0, 0, 0),  (11, 1, 0, 0, 0),  (21, 0.7071, 0.7071, 0, 0) ]),
	('FootTarget_R',  [ (1, 1, 0, 0, 0),  (11, 1, 0, 0, 0),  (21, 0.7071, 0.7071, 0, 0) ]),
	('Heel_L',  [ (1, 0.7071, -0.7071, 0, 0),  (11, 1, 0, 0, 0),  (21, 1, 0, 0, 0) ]),
	('Heel_R',  [ (1, 0.7071, -0.7071, 0, 0),  (11, 1, 0, 0, 0),  (21, 1, 0, 0, 0) ]),
]


def LegWriteActions(fp):
	writeAction(fp, 'rigLeg&T_GoboFoot', "goboFootRoll", actionFootRoll, False,  False)
	writeAction(fp, 'rigLeg&T_GoboFoot', "goboFootTumble", actionFootTumble, False,  False)
	return

#
#	LegDrivers
#	(Bone, cond, FK constraint, IK constraint, driver, channel)
#

LegDrivers = [
	("UpLeg_L", True, "ConstFK", "ConstIK", "PLegIK_L", "LOC_X"),
	("LoLeg_L", True, "ConstFK", "ConstIK", "PLegIK_L", "LOC_X"),
	("Foot_L", True, "ConstFK", "ConstIK", "PLegIK_L", "LOC_X"),
	("Toe_L", True, "ConstFK", "ConstIK", "PLegIK_L", "LOC_X"),
	
	("UpLeg_R", True, "ConstFK", "ConstIK", "PLegIK_R", "LOC_X"),
	("LoLeg_R", True, "ConstFK", "ConstIK", "PLegIK_R", "LOC_X"),
	("Foot_R", True, "ConstFK", "ConstIK", "PLegIK_R", "LOC_X"),
	("Toe_R", True, "ConstFK", "ConstIK", "PLegIK_R", "LOC_X"),

]
'''
	("FootCtrl_L", 'rigLeg&T_InvFoot', "World", "Local", "PFootLocal_L", "LOC_X"),
	("FootCtrl_R", 'rigLeg&T_InvFoot', "World", "Local", "PFootLocal_R", "LOC_X"),

	("FootGobo_L", 'rigLeg&T_GoboFoot', "World", "Local", "PFootLocal_L", "LOC_X"),
	("FootGobo_R", 'rigLeg&T_GoboFoot', "World", "Local", "PFootLocal_R", "LOC_X"),
'''
#
#	LegProcess
#	(bone, axis, angle)
#

LegProcess = [
	("UpLeg_L", "X", 0.3),
	("UpLegTwist_L", "X", 0.3),
	("UpLegFK_L", "X", 0.3),
	("UpLegIK_L", "X", 0.3),
	("LoLeg_L", "X", -0.5),
	("LoLegFK_L", "X", -0.5),
	("LoLegIK_L", "X", -0.5),

	("UpLeg_R", "X", 0.3),
	("UpLegTwist_R", "X", 0.3),
	("UpLegFK_R", "X", 0.3),
	("UpLegIK_R", "X", 0.3),
	("LoLeg_R", "X", -0.5),
	("LoLegFK_R", "X", -0.5),
	("LoLegIK_R", "X", -0.5),
]	

LegParents = [
	("FootGobo_L", "LoLegIK_L"),
	("FootGobo_R", "LoLegIK_R"),
]
	

