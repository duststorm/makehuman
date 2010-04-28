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

	# Knee pole target
	('knee_L_tail'	,		'o', ('r-knee', [0,0,6.0])),
	('knee_L_head'	,		'o', ('knee_L_tail', [0,-0.6,0])),
	('knee_R_tail'	,		'o', ('l-knee', [0,0,6.0])),
	('knee_R_head'	,		'o', ('knee_R_tail', [0,-0.6,0])),

	# Control gobo
	('thigh_root_L_head',		'l', ((0.5, 'pelvis'), (0.5, 'r-upper-leg'))),
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

	('thigh_root_R_head',		'l', ((0.5, 'pelvis'), (0.5, 'l-upper-leg'))),
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
	# Deform 
	('Hip_L',			'pelvis', 'r-upper-leg'),
	('UpLegTwist_L',		'r-upper-leg', 'r-knee'),
	('UpLeg_L',			'r-upper-leg', 'r-knee'),
	('LoLeg_L',			'r-knee', 'r-ankle'),
	('Foot_L',			'r-ankle', 'r-ball'),
	('Toe_L',			'r-ball', 'r-toes-tip'),

	('Hip_R',			'pelvis', 'l-upper-leg'),
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


upLegRoll = -3.08923
loLegRoll = -3.14159
footRoll = 3.14159
toeRoll = -2.813

LegArmature = [
	# Deform
	('Hip_L', 'True',		1.62316, 'Hips', F_DEF, L_HELP, (1,1,1) ),
	('UpLeg_L', 'True',		upLegRoll, 'Hip_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpLegTwist_L', 'True',	upLegRoll, 'Hip_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoLeg_L', 'True',		loLegRoll, 'UpLeg_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Foot_L', 'True',		footRoll, 'LoLeg_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Toe_L', 'True',		toeRoll, 'Foot_L', F_DEF+F_CON, L_DEF, (1,1,1) ),

	('Hip_R', 'True',		-1.62316, 'Hips', F_DEF, L_HELP, (1,1,1) ),
	('UpLeg_R', 'True',		-upLegRoll, 'Hip_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpLegTwist_R', 'True',	-upLegRoll, 'Hip_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoLeg_R', 'True',		-loLegRoll, 'UpLeg_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Foot_R', 'True',		-footRoll, 'LoLeg_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Toe_R', 'True',		-toeRoll, 'Foot_R', F_DEF+F_CON, L_DEF, (1,1,1) ),

	# FK
	('UpLegFK_L', 'True',		upLegRoll, 'Hip_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('LoLegFK_L', 'True',		loLegRoll, 'UpLegFK_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('FootFK_L', 'True',		footRoll, 'LoLegFK_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('ToeFK_L', 'True',		toeRoll, 'FootFK_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),

	('UpLegFK_R', 'True',		-upLegRoll, 'Hip_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('LoLegFK_R', 'True',		-loLegRoll, 'UpLegFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('FootFK_R', 'True',		-footRoll, 'LoLegFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('ToeFK_R', 'True',		-toeRoll, 'FootFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),

	# IK Common
	('UpLegIK_L', 'True',		upLegRoll, 'Hip_L', F_CON, L_HLPIK, (1,1,1) ),
	('LoLegIK_L', 'True',		loLegRoll, 'UpLegIK_L', F_CON, L_HLPIK, (1,1,1) ),
	('FootIK_L', 'True',		footRoll, 'LoLegIK_L', F_CON, L_HLPIK, (1,1,1)),
	('ToeIK_L', 'True',		toeRoll, 'FootIK_L', F_CON, L_HLPIK, (1,1,1)),

	('UpLegIK_R', 'True',		-upLegRoll, 'Hip_R', F_CON, L_HLPIK, (1,1,1) ),
	('LoLegIK_R', 'True',		-loLegRoll, 'UpLegIK_R', F_CON, L_HLPIK, (1,1,1) ),
	('FootIK_R', 'True',		-footRoll, 'LoLegIK_R', F_CON, L_HLPIK, (1,1,1)),
	('ToeIK_R', 'True',		-toeRoll, 'FootIK_R', F_CON, L_HLPIK, (1,1,1)),

	# IK Inverse foot
	('FootCtrl_L', 'rigLeg&T_InvFoot',	-2.597, 'Root', F_WIR, L_LEGIK, (1,1,1) ),
	('ToeRevIK_L', 'rigLeg&T_InvFoot',	0.0, 'FootCtrl_L', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('FootRevIK_L', 'rigLeg&T_InvFoot',	3.14159, 'ToeRevIK_L', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('Ankle_L', 'rigLeg&T_InvFoot',		3.14159, 'FootRevIK_L', F_CON+F_CON, L_HELP, (1,1,1) ),
	('KneePT_L', 'rigLeg&T_InvFoot',	0.0, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),

	('FootCtrl_R', 'rigLeg&T_InvFoot',	2.597, 'Root', F_WIR, L_LEGIK, (1,1,1) ),
	('ToeRevIK_R', 'rigLeg&T_InvFoot',	0.0, 'FootCtrl_R', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('FootRevIK_R', 'rigLeg&T_InvFoot',	-3.14159, 'ToeRevIK_R', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('Ankle_R', 'rigLeg&T_InvFoot',		-3.14159, 'FootRevIK_R', F_CON, L_HELP, (1,1,1) ),
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
	('FootRoll_L', 'rigLeg&T_GoboFoot',	-1.5708, 'FootGobo_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootTarget_L', 'rigLeg&T_GoboFoot',	2.779, 'Heel_L', F_RES, L_HELP, (1,1,1)),
	('ToeTarget_L', 'rigLeg&T_GoboFoot',	toeRoll, 'RotateToe_L', F_RES, L_HELP, (1,1,1)),

	('TipToe_R', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_R', F_WIR, L_LEGIK, (1,1,1)),
	('TumbleOut_R', 'rigLeg&T_GoboFoot',	0.0, 'TipToe_R', F_RES, L_HELP, (1,1,1)),
	('TumbleIn_R', 'rigLeg&T_GoboFoot',	0.0, 'TumbleOut_R', F_RES, L_HELP, (1,1,1)),
	('Heel_R', 'rigLeg&T_GoboFoot',		0.0, 'TumbleIn_R', F_RES, L_HELP, (1,1,1)),
	('RotateToe_R', 'rigLeg&T_GoboFoot',	0.0, 'Heel_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootTumble_R', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootRoll_R', 'rigLeg&T_GoboFoot',	-1.5708, 'FootGobo_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootTarget_R', 'rigLeg&T_GoboFoot',	-2.779, 'Heel_R', F_RES, L_HELP, (1,1,1)),
	('ToeTarget_R', 'rigLeg&T_GoboFoot',	-toeRoll, 'RotateToe_R', F_RES, L_HELP, (1,1,1)),
]

def LegWritePoses(fp):
	global boneGroups
	boneGroups = {}

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
 		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.05,2.6, -1.05,1.05, -0.7805,1.5708), (1,1,1)])])

	addPoseBone(fp, 'True', 'LoLegFK_L', 'MHCircle025', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-2.6,0, 0,0, 0,0), (1,0,0)])])

	addPoseBone(fp, 'True', 'FootFK_L', 'MHFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'ToeFK_L', 'MHToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'UpLegFK_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-1.05,2.6, -1.05,1.05, -1.5708,0.7805), (1,1,1)])])

	addPoseBone(fp, 'True', 'LoLegFK_R', 'MHCircle025', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', (-2.6,0, 0,0, 0,0), (1,0,0)])])

	addPoseBone(fp, 'True', 'FootFK_R', 'MHFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'ToeFK_R', 'MHToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])



	# IK reverse foot

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootCtrl_L', 'MHFootCtrl_L', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_OW_WORLD+C_TG_WORLD, ['ChildOf', 'Hip_L', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'Hip_L'])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootCtrl_R', 'MHFootCtrl_R', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_OW_WORLD+C_TG_WORLD, ['ChildOf', 'Hip_R', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'Hip_R'])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'LoLegIK_L', None, 'ik', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Ankle_L', 2, (1.2708, 'KneePT_L'), (True, False), 1.0]),
		 ('LimitRot', C_OW_LOCAL, ['LimitRot', (-2.6,0, 0,0, 0,0), (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'LoLegIK_R', None, 'ik', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'Ankle_R', 2, (1.8708, 'KneePT_R'), (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-2.6,0, 0,0, 0,0), (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootRevIK_L', 'MHRevFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootRevIK_R', 'MHRevFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootIK_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootRevIK_L', 1, None, (True, False), 1.0])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootIK_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootRevIK_R', 1, None, (True, False), 1.0])]),

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'ToeRevIK_L', 'MHRevToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'ToeRevIK_R', 'MHRevToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'ToeIK_L', None, None, (1,1,1), (0,1,1), (1,1,0), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeRevIK_L', 1, None, (True, False), 1.0])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'ToeIK_R', None, None, (1,1,1), (0,1,1), (1,1,0), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeRevIK_R', 1, None, (True, False), 1.0])]),

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'KneePT_L', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_OW_WORLD+C_TG_WORLD, ['ChildOf', 'Root', 0.0, (1,1,1), (1,1,1), (1,1,1)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'KneePT_R', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_OW_WORLD+C_TG_WORLD, ['ChildOf', 'Root', 0.0, (1,1,1), (1,1,1), (1,1,1)])])



	# IK Gobo
		
	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'LoLegIK_L', None, 'ik', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'LegTarget_L', 2, (1.2708, 'KneePT_L'), (True, False), 1.0]),
		 ('LimitRot', C_OW_LOCAL, ['LimitRot', (-2.6,0, 0,0, 0,0), (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'LoLegIK_R', None, 'ik', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'LegTarget_R', 2, (1.8708, 'KneePT_R'), (True, False), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-2.6,0, 0,0, 0,0), (True, True, True)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootGobo_L', 'GoboFootCtrl_L', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_OW_WORLD+C_TG_WORLD, ['ChildOf', 'Root', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'Hip_L'])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootGobo_R', 'GoboFootCtrl_R', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_OW_WORLD+C_TG_WORLD, ['ChildOf', 'Root', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Const', 'Hip_R'])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'KneePT_L', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_OW_WORLD+C_TG_WORLD, ['ChildOf', 'Root', 0.0, (1,1,1), (1,1,1), (1,1,1)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'KneePT_R', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_OW_WORLD+C_TG_WORLD, ['ChildOf', 'Root', 0.0, (1,1,1), (1,1,1), (1,1,1)])])



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


	return

#
#	LegWriteActions(fp)
#

actionFootTumble = [
	('TumbleIn_L',  [ (0.7071, 0, 0, 0.7071),  (1, 0, 0, 0),  (1, 0, 0, 0) ]),
	('TumbleIn_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.7071, 0, 0, -0.7071) ]),
	('TumbleOut_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.7071, 0, 0, -0.7071) ]),
	('TumbleOut_R',  [ (0.7071, 0, 0, 0.7071),  (1, 0, 0, 0),  (1, 0, 0, 0) ]),
]

actionFootRoll = [
	('FootTarget_L',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.7071, 0.7071, 0, 0) ]),
	('FootTarget_R',  [ (1, 0, 0, 0),  (1, 0, 0, 0),  (0.7071, 0.7071, 0, 0) ]),
	('Heel_L',  [ (0.7071, -0.7071, 0, 0),  (1, 0, 0, 0),  (1, 0, 0, 0) ]),
	('Heel_R',  [ (0.7071, -0.7071, 0, 0),  (1, 0, 0, 0),  (1, 0, 0, 0) ]),
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
	("FootCtrl_L", 'toggle&T_InvFoot', None, "ChildOf", "PLegIK_L", "LOC_Z"),
	("FootCtrl_R", 'toggle&T_InvFoot', None, "ChildOf", "PLegIK_R", "LOC_Z"),

	("FootGobo_L", 'toggle&T_GoboFoot', None, "ChildOf", "PLegIK_L", "LOC_Z"),
	("FootGobo_R", 'toggle&T_GoboFoot', None, "ChildOf", "PLegIK_R", "LOC_Z"),
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
	("FootGobo_L", "LoLegIK_L"),	("FootGobo_R", "LoLegIK_R"),]	

