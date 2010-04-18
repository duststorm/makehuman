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
	('foot_L_tail',			'j', 'r-toe-3-1'),
	('toe_L_tail',			'v', 12258),

	('l-upper-leg',			'j', 'l-upper-leg'),
	('l-knee',			'j', 'l-knee'),
	('l-ankle',			'j', 'l-ankle'),
	('foot_R_tail',			'j', 'l-toe-3-1'),
	('toe_R_tail',			'v', 13258),

	# IK classic
	('r-knee-target',		'l', ((1.2, 'r-knee'), (-0.2, 'r-upper-leg'))),
	('clFootCtrl_L_head',		'o', ('r-ankle', [0.0, -1.0, 0.0])),
	('clFootCtrl_L_tail',		'o', ('r-ankle', [0.0, -1.0, -2.0])),
	('Ankle_L_tail',		'o', ('r-ankle', [0.0, 0.0, -1.0])),
	('KneeIK_L_tail',		'o', ('r-knee-target', [0.0, 0.5, 0.5])),

	('l-knee-target',		'l', ((1.2, 'l-knee'), (-0.2, 'l-upper-leg'))),
	#('clFootCtrl_R_head',		'o', ('l-ankle', [0.0, -1.0, 0.0])),
	#('clFootCtrl_R_tail',		'o', ('l-ankle', [0.0, -1.0, -2.0])),
	('Ankle_R_tail',		'o', ('l-ankle', [0.0, 0.0, -1.0])),
	('KneeIK_R_tail',		'o', ('l-knee-target', [0.0, 0.5, 0.5])),

	# Control gobo
	('thigh_root_L_head',		'l', ((0.5, 'pelvis'), (0.5, 'r-upper-leg'))),
	('foot_L_center',		'v', 5736),
	('footCtrl_L_head',		'o', ('r-ankle', [0,-0.3,-0.3])),
	('footCtrl_L_tail',		'o', ('footCtrl_L_head', [0,1.5,0])),
	('tiptoe_L_head',		'b', 'toe_L_tail'),
	('tiptoe_L_tail',		'o', ('tiptoe_L_head', [0,0.6,0])),
	('tumble_out_L_head',		'l', ((1.25, 'foot_L_center'), (-0.25, 'foot_R_center'))),
	('tumble_out_L_tail',		'o', ('tumble_out_L_head', [0,0.6,0])),
	('tumble_in_L_head',		'l', ((0.7, 'foot_L_center'), (0.3, 'foot_R_center'))),
	('tumble_in_L_tail',		'o', ('tumble_in_L_head', [0,0.6,0])),
	('heel_L_head'	,		'v', 5721),
	('heel_L_tail'	,		'o', ('heel_L_head', [0,0.6,0])),
	('rotate_toe_L_head',		'b', 'foot_L_tail'),
	('rotate_toe_L_tail',		'o', ('rotate_toe_L_head', [0,0.6,0])),
	('toe_target_L_head',		'b', 'toe_L_tail'),
	('toe_target_L_tail',		'l', ((2, 'toe_L_tail'), (-1, 'foot_L_tail'))),
	('foot_target_L_head',		'b', 'foot_L_tail'),
	('foot_target_L_tail',		'l', ((2, 'foot_L_tail'), (-1, 'r-ankle'))),
	('leg_target_L_head',		'b', 'r-ankle'),
	('leg_target_L_tail',		'l', ((2, 'r-ankle'), (-1, 'r-knee'))),
	('foot_tumble_L_head',		'o', ('tiptoe_L_head', [0,1.0,0])),
	('foot_tumble_L_tail',		'o', ('foot_tumble_L_head', [0,0.6,0])),
	('foot_roll_L_head',		'o', ('toe_L_tail', [0.3,0,0.6])),
	('foot_roll_L_tail',		'o', ('foot_roll_L_head', [-0.6,0,0])),
	('knee_L_tail'	,		'o', ('r-knee', [0,0,6.0])),
	('knee_L_head'	,		'o', ('knee_L_tail', [0,-0.6,0])),

	('thigh_root_R_head',		'l', ((0.5, 'pelvis'), (0.5, 'l-upper-leg'))),
	('foot_R_center',		'v', 13326),
	('footCtrl_R_head',		'o', ('l-ankle', [0,-0.3,-0.3])),
	('footCtrl_R_tail',		'o', ('footCtrl_R_head', [0,1.5,0])),
	('tiptoe_R_head',		'b', 'toe_R_tail'),
	('tiptoe_R_tail',		'o', ('tiptoe_R_head', [0,0.6,0])),
	('tumble_out_R_head',		'l', ((1.25, 'foot_R_center'), (-0.25, 'foot_L_center'))),
	('tumble_out_R_tail',		'o', ('tumble_out_R_head', [0,0.6,0])),
	('tumble_in_R_head',		'l', ((0.7, 'foot_R_center'), (0.3, 'foot_L_center'))),
	('tumble_in_R_tail',		'o', ('tumble_in_R_head', [0,0.6,0])),
	('heel_R_head'	,		'v', 13338),
	('heel_R_tail'	,		'o', ('heel_R_head', [0,0.6,0])),
	('rotate_toe_R_head',		'b', 'foot_R_tail'),
	('rotate_toe_R_tail',		'o', ('rotate_toe_R_head', [0,0.6,0])),
	('toe_target_R_head',		'b', 'toe_R_tail'),
	('toe_target_R_tail',		'l', ((2, 'toe_R_tail'), (-1, 'foot_R_tail'))),
	('foot_target_R_head',		'b', 'foot_R_tail'),
	('foot_target_R_tail',		'l', ((2, 'foot_R_tail'), (-1, 'l-ankle'))),
	('leg_target_R_head',		'b', 'l-ankle'),
	('leg_target_R_tail',		'l', ((2, 'l-ankle'), (-1, 'l-knee'))),
	('foot_tumble_R_head',		'o', ('tiptoe_R_head', [0,1.0,0])),
	('foot_tumble_R_tail',		'o', ('foot_tumble_R_head', [0,0.6,0])),
	('foot_roll_R_head',		'o', ('toe_R_tail', [0.3,0,0.6])),
	('foot_roll_R_tail',		'o', ('foot_roll_R_head', [-0.6,0,0])),
	('knee_R_tail'	,		'o', ('l-knee', [0,0,6.0])),
	('knee_R_head'	,		'o', ('knee_R_tail', [0,-0.6,0])),

]

LegHeadsTails = [
	# Deform 
	('Hip_L',			'pelvis', 'r-upper-leg'),
	('UpLegTwist_L',		'r-upper-leg', 'r-knee'),
	('UpLeg_L',			'r-upper-leg', 'r-knee'),
	('LoLeg_L',			'r-knee', 'r-ankle'),
	('Foot_L',			'r-ankle', 'foot_L_tail'),
	('Toe_L',			'foot_L_tail', 'toe_L_tail'),

	('Hip_R',			'pelvis', 'l-upper-leg'),
	('UpLegTwist_R',		'l-upper-leg', 'l-knee'),
	('UpLeg_R',			'l-upper-leg', 'l-knee'),
	('LoLeg_R',			'l-knee', 'l-ankle'),
	('Foot_R',			'l-ankle', 'foot_R_tail'),
	('Toe_R',			'foot_R_tail', 'toe_R_tail'),

	# FK
	('UpLegFK_L',			'r-upper-leg', 'r-knee'),
	('LoLegFK_L',			'r-knee', 'r-ankle'),
	('FootFK_L',			'r-ankle', 'foot_L_tail'),
	('ToeFK_L',			'foot_L_tail', 'toe_L_tail'),
	('UpLegFK_R',			'l-upper-leg', 'l-knee'),
	('LoLegFK_R',			'l-knee', 'l-ankle'),
	('FootFK_R',			'l-ankle', 'foot_R_tail'),
	('ToeFK_R',			'foot_R_tail', 'toe_R_tail'),
	
	# IK common
	('UpLegIK_L',			'r-upper-leg', 'r-knee'),
	('LoLegIK_L',			'r-knee', 'r-ankle'),
	('UpLegIK_R',			'l-upper-leg', 'l-knee'),
	('LoLegIK_R',			'l-knee', 'l-ankle'),
	('LegIK_L',			'r-ankle', 'Ankle_L_tail'),
	('LegIK_R',			'l-ankle', 'Ankle_R_tail'),
	('ToeIK_L',			'foot_L_tail', 'toe_L_tail'),
	('ToeIK_R',			'foot_R_tail', 'toe_R_tail'),
	('FootCtrl_L',			'footCtrl_L_head', 'footCtrl_L_tail'),
	('FootCtrl_R',			'footCtrl_R_head', 'footCtrl_R_tail'),

	# IK thigh ik
	('KneeIK_L',			'r-knee-target', 'KneeIK_L_tail'),
	('KneeIK_R',			'l-knee-target', 'KneeIK_R_tail'),

	# IK pole target
	('KneePT_L',			'knee_L_head', 'knee_L_tail'),
	('KneePT_R',			'knee_R_head', 'knee_R_tail'),

	# IK classic
	('FootRevIK_L',			'foot_L_tail', 'r-ankle'),
	('Ankle_L',			'r-ankle', 'Ankle_L_tail'),
	('FootRevIK_R',			'foot_R_tail', 'l-ankle'),
	('Ankle_R',			'l-ankle', 'Ankle_R_tail'),

	# IK gobo
	('FootIK_L',			'r-ankle', 'foot_L_tail'),
	('TipToe_L',			'tiptoe_L_head', 'tiptoe_L_tail'),
	('TumbleOut_L',			'tumble_out_L_head', 'tumble_out_L_tail'),
	('TumbleIn_L',			'tumble_in_L_head', 'tumble_in_L_tail'),
	('Heel_L',			'heel_L_head', 'heel_L_tail'),
	('RotateToe_L',			'rotate_toe_L_head', 'rotate_toe_L_tail'),
	('ToeTarget_L',			'toe_target_L_head', 'toe_target_L_tail'),
	('FootTarget_L',		'foot_target_L_head', 'foot_target_L_tail'),
	('LegTarget_L',			'leg_target_L_head', 'leg_target_L_tail'),
	('FootTumble_L',		'foot_tumble_L_head', 'foot_tumble_L_tail'),
	('FootRoll_L',			'foot_roll_L_head', 'foot_roll_L_tail'),

	('FootIK_R',			'l-ankle', 'foot_R_tail'),
	('TipToe_R',			'tiptoe_R_head', 'tiptoe_R_tail'),
	('TumbleOut_R',			'tumble_out_R_head', 'tumble_out_R_tail'),
	('TumbleIn_R',			'tumble_in_R_head', 'tumble_in_R_tail'),
	('Heel_R',			'heel_R_head', 'heel_R_tail'),
	('RotateToe_R',			'rotate_toe_R_head', 'rotate_toe_R_tail'),
	('ToeTarget_R',			'toe_target_R_head', 'toe_target_R_tail'),
	('FootTarget_R',		'foot_target_R_head', 'foot_target_R_tail'),
	('LegTarget_R',			'leg_target_R_head', 'leg_target_R_tail'),
	('FootTumble_R',		'foot_tumble_R_head', 'foot_tumble_R_tail'),
	('FootRoll_R',			'foot_roll_R_head', 'foot_roll_R_tail'),

]

LegArmature = [
	# Deform
	('Hip_L', 'True',		1.62316, 'Hips', F_DEF, L_HELP, (1,1,1) ),
	#('LegRoot_L', 'True'		0.0, 'Hip_L', F_CON+F_RES, L_SKEL, (0,0,2)),
	#('UpLeg_L',  'True'		0.0, 'LegRoot_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,8)),
	('UpLeg_L', 'True',		-3.08923, 'Hip_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpLegTwist_L', 'True',	-3.08923, 'Hip_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoLeg_L', 'True',		-3.14159, 'UpLeg_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Foot_L', 'True',		-0.488688, 'LoLeg_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Toe_L', 'True',		-2.86233, 'Foot_L', F_DEF+F_CON, L_DEF, (1,1,1) ),

	('Hip_R', 'True',		-1.62316, 'Hips', F_DEF, L_HELP, (1,1,1) ),
	('UpLeg_R', 'True',		3.08923, 'Hip_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpLegTwist_R', 'True',	3.08923, 'Hip_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoLeg_R', 'True',		-3.14159, 'UpLeg_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Foot_R', 'True',		0.488689, 'LoLeg_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Toe_R', 'True',		2.86233, 'Foot_R', F_DEF+F_CON, L_DEF, (1,1,1) ),

	# FK
	('UpLegFK_L', 'True',		-3.08923, 'Hip_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('LoLegFK_L', 'True',		-3.14159, 'UpLegFK_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('FootFK_L', 'True',		-0.488688, 'LoLegFK_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('ToeFK_L', 'True',		-2.86233, 'FootFK_L', F_WIR, L_LEGFK, (1,1,1) ),

	('UpLegFK_R', 'True',		3.08923, 'Hip_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('LoLegFK_R', 'True',		-3.14159, 'UpLegFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('FootFK_R', 'True',		0.488689, 'LoLegFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('ToeFK_R', 'True',		2.86233, 'FootFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),

	# IK Common
	('UpLegIK_L', 'True',			-3.08923, 'Hip_L', F_CON, L_HELP, (1,1,1) ),
	('LoLegIK_L', 'True',			-3.14159, 'UpLegIK_L', F_CON, L_HELP, (1,1,1) ),
	('UpLegIK_R', 'True',			3.08923, 'Hip_R', F_CON, L_HELP, (1,1,1) ),
	('LoLegIK_R', 'True',			-3.14159, 'UpLegIK_R', F_CON, L_HELP, (1,1,1) ),
	('FootCtrl_L', 'True',			0.0, 'Root', F_WIR, L_LEGIK, (1,1,1)),
	('FootCtrl_R', 'True',			0.0, 'Root', F_WIR, L_LEGIK, (1,1,1)),
	('LegTarget_L', 'True',			0.0, 'FootCtrl_L', F_RES, L_HELP, (1,1,1)),
	('LegTarget_R', 'True',			0.0, 'FootCtrl_R', F_RES, L_HELP, (1,1,1)),

	# IK Inverse foot
	('FootRevIK_L', 'rigLeg&T_InvFoot',	-3.08923, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1) ),
	('Ankle_L', 'rigLeg&T_InvFoot',		-3.14159, 'FootRevIK_L', 0, L_HELP, (1,1,1) ),
	('ToeIK_L', 'rigLeg&T_InvFoot',		-2.86234, 'FootCtrl_L', 0, L_LEGIK, (1,1,1) ),

	('FootRevIK_R', 'rigLeg&T_InvFoot',	3.08923, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1) ),
	('Ankle_R', 'rigLeg&T_InvFoot',		-3.14159, 'FootRevIK_R', 0, L_HELP, (1,1,1) ),
	('ToeIK_R', 'rigLeg&T_InvFoot',		2.86234, 'FootCtrl_R', 0, L_LEGIK, (1,1,1) ),

	# IK Gobo
	('FootIK_L', 'rigLeg&T_GoboFoot',	-0.488689, 'LoLegIK_L', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('ToeIK_L', 'rigLeg&T_GoboFoot',	-2.86233, 'FootIK_L', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('TipToe_L', 'rigLeg&T_GoboFoot',	0.0, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('TumbleOut_L', 'rigLeg&T_GoboFoot',	0.0, 'TipToe_L', F_RES, L_HELP, (1,1,1)),
	('TumbleIn_L', 'rigLeg&T_GoboFoot',	0.0, 'TumbleOut_L', F_RES, L_HELP, (1,1,1)),
	('Heel_L', 'rigLeg&T_GoboFoot',		0.0, 'TumbleIn_L', F_RES, L_HELP, (1,1,1)),
	('RotateToe_L', 'rigLeg&T_GoboFoot',	0.0, 'Heel_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootTumble_L', 'rigLeg&T_GoboFoot',	0.0, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootRoll_L', 'rigLeg&T_GoboFoot',	-1.5708, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootTarget_L', 'rigLeg&T_GoboFoot',	-0.488689, 'Heel_L', F_RES, L_HELP, (1,1,1)),
	('ToeTarget_L', 'rigLeg&T_GoboFoot',	-2.86233, 'RotateToe_L', F_RES, L_HELP, (1,1,1)),

	('FootIK_R', 'rigLeg&T_GoboFoot',	0.488689, 'LoLegIK_R', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('ToeIK_R', 'rigLeg&T_GoboFoot',	2.86233, 'FootIK_R', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('TipToe_R', 'rigLeg&T_GoboFoot',	0.0, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
	('TumbleOut_R', 'rigLeg&T_GoboFoot',	0.0, 'TipToe_R', F_RES, L_HELP, (1,1,1)),
	('TumbleIn_R', 'rigLeg&T_GoboFoot',	0.0, 'TumbleOut_R', F_RES, L_HELP, (1,1,1)),
	('Heel_R', 'rigLeg&T_GoboFoot',		0.0, 'TumbleIn_R', F_RES, L_HELP, (1,1,1)),
	('RotateToe_R', 'rigLeg&T_GoboFoot',	0.0, 'Heel_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootTumble_R', 'rigLeg&T_GoboFoot',	0.0, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootRoll_R', 'rigLeg&T_GoboFoot',	-1.5708, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootTarget_R', 'rigLeg&T_GoboFoot',	0.488689, 'Heel_R', F_RES, L_HELP, (1,1,1)),
	('ToeTarget_R', 'rigLeg&T_GoboFoot',	2.86233, 'RotateToe_R', F_RES, L_HELP, (1,1,1)),

	# IK Knee thigh ik
	('KneeIK_L', 'rigLeg&T_KneeIK',		0.0, 'Hip_L', F_WIR, L_LEGIK, (1,1,1) ),
	('KneeIK_R', 'rigLeg&T_KneeIK',		0.0, 'Hip_R', F_WIR, L_LEGIK, (1,1,1) ),

	# IK knee pole target
	('KneePT_L', 'rigLeg&T_KneePT',		0.0, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('KneePT_R', 'rigLeg&T_KneePT',		0.0, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
]

def LegWritePoses(fp):
	global boneGroups
	boneGroups = {}

	# Deform 
	addPoseBone(fp, 'True', 'UpLeg_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'UpLegIK_L', 'fLegIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'UpLegFK_L', '1-fLegIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'True', 'UpLegTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'LoLeg_L', 1, None, (True, False), 1.0])])

	addPoseBone(fp, 'True', 'LoLeg_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'LoLegIK_L', 'fLegIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'LoLegFK_L', '1-fLegIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'Foot_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'FootIK_L', 'fLegIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'FootFK_L', '1-fLegIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'Foot_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['ConstIK', 'ToeIK_L', 1, None, (True, False), 'fLegIK']),
		('CopyRot', 0, ['ConstFK', 'FootFK_L', '1-fLegIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'True', 'Toe_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'ToeIK_L', 'fLegIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'ToeFK_L', '1-fLegIK', (1,1,1), (0,0,0)])])


	addPoseBone(fp, 'True', 'UpLeg_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'UpLegIK_R', 'fLegIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'UpLegFK_R', '1-fLegIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'True', 'UpLegTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'LoLeg_R', 1, None, (True, False), 1.0])])

	addPoseBone(fp, 'True', 'LoLeg_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'LoLegIK_R', 'fLegIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'LoLegFK_R', '1-fLegIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'Foot_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'FootIK_R', 'fLegIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'FootFK_R', '1-fLegIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'Foot_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['ConstIK', 'ToeIK_R', 1, None, (True, False), 'fLegIK']),
		('CopyRot', 0, ['ConstFK', 'FootFK_R', '1-fLegIK', (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'True', 'Toe_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['ConstIK', 'ToeIK_R', 'fLegIK', (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['ConstFK', 'ToeFK_R', '1-fLegIK', (1,1,1), (0,0,0)])])


	# FK
	addPoseBone(fp, 'True', 'UpLegFK_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'LoLegFK_L', 'MHCircle025', None, (0,0,0), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'FootFK_L', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'ToeFK_L', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'UpLegFK_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'LoLegFK_R', 'MHCircle025', None, (0,0,0), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'FootFK_R', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'ToeFK_R', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])


	# IK Common

	addPoseBone(fp, 'True', 'FootCtrl_L', 'GoboFootCtrl_L', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Hip_L'])])

	addPoseBone(fp, 'True', 'FootCtrl_R', 'GoboFootCtrl_R', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Hip_R'])])
		

	# Knee thigh ik 

	addPoseBone(fp, 'rigLeg&T_KneeIK', 'KneeIK_L', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Hip_L'])])

	addPoseBone(fp, 'rigLeg&T_KneeIK', 'KneeIK_R', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Hip_R'])])

	addPoseBone(fp, 'rigLeg&T_KneeIK', 'UpLegIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'KneeIK_L', 1, None, (True, False), 'fKneeIK'])])

	addPoseBone(fp, 'rigLeg&T_KneeIK', 'UpLegIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['IK', 'KneeIK_R', 1, None, (True, False), 'fKneeIK'])])

	addPoseBone(fp, 'rigLeg&T_KneePT==0', 'LoLegIK_L', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
			[('IK', 0, ['IK', 'LegTarget_L', 2, None, (True, False), 1.0])])
	
	addPoseBone(fp, 'rigLeg&T_KneePT==0', 'LoLegIK_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
			[('IK', 0, ['IK', 'LegTarget_R', 2, None, (True, False), 1.0])])


	# Knee pole target

	addPoseBone(fp, 'rigLeg&T_KneePT', 'KneePT_L', 'MHCircle10', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_KneePT', 'KneePT_R', 'MHCircle10', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_KneePT', 'LoLegIK_L', None, 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('IK', 0, ['IK', 'LegTarget_L', 2, (1.2708, 'KneePT_L'), (True, False), 1.0])])

	addPoseBone(fp, 'rigLeg&T_KneePT', 'LoLegIK_R', None, 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('IK', 0, ['IK', 'LegTarget_R', 2, (1.8708, 'KneePT_R'), (True, False), 1.0])])


	# IK inverse foot

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'LegTarget_L', None, 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('CopyLoc', 0, ['CopyLoc', 'Ankle_L', 1, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'LegTarget_R', None, 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('CopyLoc', 0, ['CopyLoc', 'Ankle_R', 1, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootRevIK_L', 'MHFoot', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_InvFoot', 'FootRevIK_R', 'MHFoot', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])


	# IK Gobo
	
	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootTarget_L', 1, None, (True, True), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'ToeIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeTarget_L', 1, None, (True, True), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TipToe_L', 'GoboTipToe_L', None, (1,1,1), (0,0,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OWNER, ['LimitRot', (0,2.96706, 0,0, 0,0), (True, False, False)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootRoll_L', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootTumble_L', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TumbleOut_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['Action', 'goboFootTumble', 'FootTumble_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TumbleIn_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['Action', 'goboFootTumble', 'FootTumble_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'Heel_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['Action', 'goboFootRoll', 'FootRoll_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'RotateToe_L', 'GoboRotate_L', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootTarget_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['Action', 'goboFootRoll', 'FootRoll_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])


	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootTarget_R', 1, None, (True, True), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'ToeIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeTarget_R', 1, None, (True, True), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TipToe_R', 'GoboTipToe_R', None, (1,1,1), (0,0,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OWNER, ['LimitRot', (0,2.96706, 0,0, 0,0), (True, False, False)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootRoll_R', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootTumble_R', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TumbleOut_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['Action', 'goboFootTumble', 'FootTumble_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'TumbleIn_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['Action', 'goboFootTumble', 'FootTumble_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'Heel_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['Action', 'goboFootRoll', 'FootRoll_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'RotateToe_R', 'GoboRotate_R', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_GoboFoot', 'FootTarget_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['Action', 'goboFootRoll', 'FootRoll_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])])


	return

#
#	LegWriteActions(fp)
#

actionFootTumble = [
	("TumbleOut_L", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.0, 0.0, -0.707107) ),
	("TumbleIn_L", (0.707107, 0.0, 0.0, 0.707107), (1.0, 0.0, 0.0, 0.0) ),
	("TumbleOut_R", (0.707107, 0.0, 0.0, 0.707107), (1.0, 0.0, 0.0, 0.0) ),
	("TumbleIn_R", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.0, 0.0, -0.707107) ),
]

actionFootRoll = [
	("Heel_L", (0.707107, -0.707107, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ),
	("FootTarget_L", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.707107, 0.0, 0.0) ),
	("Heel_R", (0.707107, -0.707107, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ),
	("FootTarget_R", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.707107, 0.0, 0.0) ),
]


def LegWriteActions(fp):
	writeAction(fp, 'rigLeg&T_GoboFoot', "goboFootRoll", actionFootRoll, False,  False)
	writeAction(fp, 'rigLeg&T_GoboFoot', "goboFootTumble", actionFootTumble, False,  False)
	return

#
#	LegDrivers
#	(Bone, FK constraint, IK constraint, driver)
#

LegDrivers = [
	("UpLeg_L", "ConstFK", "ConstIK", "PLegIK_L"),
	("LoLeg_L", "ConstFK", "ConstIK", "PLegIK_L"),
	("Foot_L", "ConstFK", "ConstIK", "PLegIK_L"),
	#("Foot_L", "IK", "ConstIK", "PLegIK_L"),
	("Toe_L", "ConstFK", "ConstIK", "PLegIK_L"),
	
	("UpLeg_R", "ConstFK", "ConstIK", "PLegIK_R"),
	("LoLeg_R", "ConstFK", "ConstIK", "PLegIK_R"),
	("Foot_R", "ConstFK", "ConstIK", "PLegIK_R"),
	#("Foot_R", "IK", "ConstIK", "PLegIK_R"),
	("Toe_R", "ConstFK", "ConstIK", "PLegIK_R"),
]

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
	("FootCtrl_L", "LoLegIK_L"),	("FootCtrl_R", "LoLegIK_R"),]	

