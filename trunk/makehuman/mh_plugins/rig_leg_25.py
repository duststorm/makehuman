#
#	Leg bone definitions
#

import mhx_rig
from mhx_rig import *

offs = [0,0.6,0]

LegJoints = [
	# Deform
	('r-upper-leg',			'j', 'r-upper-leg'),
	('r-knee',			'j', 'r-knee'),
	('r-ankle',			'j', 'r-ankle'),
	('r-foot-1',			'j', 'r-foot-1'),
	('r-foot-2',			'j', 'r-foot-2'),
	('r-heel0',			'v', 5721),
	('r-heel',			'p', ['r-foot-2', 'r-foot-1', 'r-heel0']),
	('r-ankle-tip',			'o', ('r-ankle', [0.0, 0.0, -1.0])),
	
	#('r-ball',			'v', 5742),
	#('r-toes-tip0',			'v', 12262),
	#('r-heel',			'p', ['r-toes-tip0', 'r-ball', 'r-heel0']),
	#('r-toes-tip',			'p', ['r-toes-tip0', 'r-ball', 'r-toes-tip0']),

	('l-upper-leg',			'j', 'l-upper-leg'),
	('l-knee',			'j', 'l-knee'),
	('l-ankle',			'j', 'l-ankle'),
	('l-foot-1',			'j', 'l-foot-1'),
	('l-foot-2',			'j', 'l-foot-2'),
	('l-heel0',			'v', 13338),
	('l-heel',			'p', ['l-foot-2', 'l-foot-1', 'l-heel0']),
	('l-ankle-tip',			'o', ('l-ankle', [0.0, 0.0, -1.0])),

	#('l-ball',			'v', 13320),
	#('l-toes-tip0',			'v', 13254),
	#('l-heel',			'p', ['l-toes-tip0', 'l-ball', 'l-heel0']),
	#('l-toes-tip',			'p', ['l-toes-tip0', 'l-ball', 'l-toes-tip0']),

	# Knee pole target
	('knee_L'	,		'o', ('r-knee', [0,0.6,6.0])),
	('knee_R'	,		'o', ('l-knee', [0,0.6,6.0])),

	# Control gobo
	('foot_L_center',		'v', 5736),
	('footGobo_L',			'o', ('r-ankle', [0,-0.3,-0.3])),
	('footGobo_L_tail',		'o', ('footGobo_L', [0,1.5,0])),
	('tumble_out_L',		'l', ((1.25, 'foot_L_center'), (-0.25, 'foot_R_center'))),
	('tumble_in_L',			'l', ((0.7, 'foot_L_center'), (0.3, 'foot_R_center'))),
	('toe_target_L_tail',		'l', ((2, 'r-foot-2'), (-1, 'r-foot-1'))),
	('foot_target_L_tail',		'l', ((2, 'r-foot-1'), (-1, 'r-ankle'))),
	('leg_target_L_tail',		'l', ((2, 'r-ankle'), (-1, 'r-knee'))),
	('foot_tumble_L',		'o', ('r-foot-2', [0,1.0,0])),
	('foot_roll_L',			'o', ('r-foot-2', [0.3,0,0.6])),
	('rotate_toe_L',		'b', 'r-foot-2'),

	('foot_R_center',		'v', 13326),
	('footGobo_R',			'o', ('l-ankle', [0,-0.3,-0.3])),
	('footGobo_R_tail',		'o', ('footGobo_R', [0,1.5,0])),
	('tumble_out_R',		'l', ((1.25, 'foot_R_center'), (-0.25, 'foot_L_center'))),
	('tumble_in_R',			'l', ((0.7, 'foot_R_center'), (0.3, 'foot_L_center'))),
	('toe_target_R_tail',		'l', ((2, 'l-foot-2'), (-1, 'l-foot-1'))),
	('foot_target_R_tail',		'l', ((2, 'l-foot-1'), (-1, 'l-ankle'))),
	('leg_target_R_tail',		'l', ((2, 'l-ankle'), (-1, 'l-knee'))),
	('foot_tumble_R',		'o', ('l-foot-2', [0,1.0,0])),
	('foot_roll_R',			'o', ('l-foot-2', [0.3,0,0.6])),
	('rotate_toe_R',		'b', 'l-foot-2'),

]

LegHeadsTails = [
	# Root
	('LegRoot_L',			('r-upper-leg', yunit), 'r-upper-leg'),
	('LegRoot_R',			('l-upper-leg', yunit), 'l-upper-leg'),

	# Deform 

	('UpLeg_L',			'r-upper-leg', 'r-knee'),
	('UpLegTwist_L',		'r-upper-leg', 'r-knee'),
	('LoLeg_L',			'r-knee', 'r-ankle'),
	('Foot_L',			'r-ankle', 'r-foot-1'),
	('Toe_L',			'r-foot-1', 'r-foot-2'),

	('UpLeg_R',			'l-upper-leg', 'l-knee'),
	('UpLegTwist_R',		'l-upper-leg', 'l-knee'),
	('LoLeg_R',			'l-knee', 'l-ankle'),
	('Foot_R',			'l-ankle', 'l-foot-1'),
	('Toe_R',			'l-foot-1', 'l-foot-2'),

	# FK
	('UpLegFK_L',			'r-upper-leg', 'r-knee'),
	('LoLegFK_L',			'r-knee', 'r-ankle'),
	('FootFK_L',			'r-ankle', 'r-foot-1'),
	('ToeFK_L',			'r-foot-1', 'r-foot-2'),
	('UpLegFK_R',			'l-upper-leg', 'l-knee'),
	('LoLegFK_R',			'l-knee', 'l-ankle'),
	('FootFK_R',			'l-ankle', 'l-foot-1'),
	('ToeFK_R',			'l-foot-1', 'l-foot-2'),
	
	# IK common
	('UpLegIK_L',			'r-upper-leg', 'r-knee'),
	('LoLegIK_L',			'r-knee', 'r-ankle'),
	('UpLegIK_R',			'l-upper-leg', 'l-knee'),
	('LoLegIK_R',			'l-knee', 'l-ankle'),
	('LegIK_L',			'r-ankle', 'r-ankle-tip'),
	('LegIK_R',			'l-ankle', 'l-ankle-tip'),
	('FootIK_L',			'r-ankle', 'r-foot-1'),
	('FootIK_R',			'l-ankle', 'l-foot-1'),
	('ToeIK_L',			'r-foot-1', 'r-foot-2'),
	('ToeIK_R',			'l-foot-1', 'l-foot-2'),

	# IK pole target
	('KneePT_L',			'knee_L', ('knee_L', offs)),
	('KneePT_R',			'knee_R', ('knee_R', offs)),
	('KneeHandle_L',		'r-knee', 'knee_L'),
	('KneeHandle_R',		'l-knee', 'knee_R'),

	# IK rev foot
	('FootCtrl_L',			'r-heel', 'r-foot-2'),
	('FootCtrl_R',			'l-heel', 'l-foot-2'),
	('ToeRevIK_L',			'r-foot-2', 'r-foot-1'),
	('ToeRevIK_R',			'l-foot-2', 'l-foot-1'),
	('FootRevIK_L',			'r-foot-1', 'r-ankle'),
	('FootRevIK_R',			'l-foot-1', 'l-ankle'),
	('Ankle_L',			'r-ankle', 'r-ankle-tip'),
	('Ankle_R',			'l-ankle', 'l-ankle-tip'),

	# IK gobo
	('Heel_L',			'r-heel', ('r-heel',offs)),
	('Heel_R',			'l-heel', ('l-heel',offs)),
	('FootGobo_L',			'footGobo_L', 'footGobo_L_tail'),
	('FootGobo_R',			'footGobo_R', 'footGobo_R_tail'),

	('TipToe_L',			'r-foot-2', ('r-foot-2',offs)),
	('TumbleOut_L',			'tumble_out_L', ('tumble_out_L',offs)),
	('TumbleIn_L',			'tumble_in_L', ('tumble_in_L',offs)),
	('RotateToe_L',			'rotate_toe_L', ('rotate_toe_L',offs)),
	('ToeTarget_L',			'r-foot-2', 'toe_target_L_tail'),
	('FootTarget_L',		'r-foot-1', 'foot_target_L_tail'),
	('LegTarget_L',			'r-ankle', 'leg_target_L_tail'),
	('FootTumble_L',		'foot_tumble_L', ('foot_tumble_L',offs)),
	('FootRoll_L',			'foot_roll_L', ('foot_roll_L',[-0.6,0,0])),

	('TipToe_R',			'l-foot-2', ('l-foot-2',offs)),
	('TumbleOut_R',			'tumble_out_R', ('tumble_out_R',offs)),
	('TumbleIn_R',			'tumble_in_R',('tumble_in_R',offs)),
	('RotateToe_R',			'rotate_toe_R', ('rotate_toe_R',offs)),
	('ToeTarget_R',			'l-foot-2', 'toe_target_R_tail'),
	('FootTarget_R',		'l-foot-1', 'foot_target_R_tail'),
	('LegTarget_R',			'l-ankle', 'leg_target_R_tail'),
	('FootTumble_R',		'foot_tumble_R', ('foot_tumble_R',offs)),
	('FootRoll_R',			'foot_roll_R', ('foot_roll_R',[-0.6,0,0])),

]

upLegRoll = deg180
loLegRoll = deg180
footRoll = deg180
toeRoll = deg180
toeRoll = -0.646
footCtrlRoll = 0.0

LegArmature = [
	# Root
	('LegRoot_L', 'True',		0.0, 'Hip_L', 0, L_HELP, (1,1,1) ),
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
	('FootCtrl_L', 'rigLeg&T_InvFoot',	footCtrlRoll, None, F_WIR, L_LEGIK, (1,1,1) ),
	('ToeRevIK_L', 'rigLeg&T_InvFoot',	0, 'FootCtrl_L', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('FootRevIK_L', 'rigLeg&T_InvFoot',	deg180, 'ToeRevIK_L', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('Ankle_L', 'rigLeg&T_InvFoot',		deg180, 'FootRevIK_L', F_CON, L_HELP, (1,1,1) ),

	('FootCtrl_R', 'rigLeg&T_InvFoot',	-footCtrlRoll, None, F_WIR, L_LEGIK, (1,1,1) ),
	('ToeRevIK_R', 'rigLeg&T_InvFoot',	0, 'FootCtrl_R', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('FootRevIK_R', 'rigLeg&T_InvFoot',	deg180, 'ToeRevIK_R', F_CON+F_WIR, L_LEGIK, (1,1,1)),
	('Ankle_R', 'rigLeg&T_InvFoot',		deg180, 'FootRevIK_R', F_CON, L_HELP, (1,1,1) ),

	# IK Gobo
	('FootGobo_L', 'rigLeg&T_GoboFoot',	0.0, None, F_WIR, L_LEGIK, (1,1,1)),
	('FootGobo_R', 'rigLeg&T_GoboFoot',	0.0, None, F_WIR, L_LEGIK, (1,1,1)),
	('LegTarget_L', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_L', F_RES, L_HELP, (1,1,1)),
	('LegTarget_R', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_R', F_RES, L_HELP, (1,1,1)),

	('TipToe_L', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_L', F_WIR, L_LEGIK, (1,1,1)),
	('TumbleOut_L', 'rigLeg&T_GoboFoot',	0.0, 'TipToe_L', F_RES, L_HELP, (1,1,1)),
	('TumbleIn_L', 'rigLeg&T_GoboFoot',	0.0, 'TumbleOut_L', F_RES, L_HELP, (1,1,1)),
	('Heel_L', 'rigLeg&T_GoboFoot',		0.0, 'TumbleIn_L', F_RES, L_HELP, (1,1,1)),
	('RotateToe_L', 'rigLeg&T_GoboFoot',	0.0, 'Heel_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootTumble_L', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootRoll_L', 'rigLeg&T_GoboFoot',	-deg90, 'FootGobo_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootTarget_L', 'rigLeg&T_GoboFoot',	footRoll, 'Heel_L', F_RES, L_HELP, (1,1,1)),
	('ToeTarget_L', 'rigLeg&T_GoboFoot',	toeRoll, 'RotateToe_L', F_RES, L_HELP, (1,1,1)),

	('TipToe_R', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_R', F_WIR, L_LEGIK, (1,1,1)),
	('TumbleOut_R', 'rigLeg&T_GoboFoot',	0.0, 'TipToe_R', F_RES, L_HELP, (1,1,1)),
	('TumbleIn_R', 'rigLeg&T_GoboFoot',	0.0, 'TumbleOut_R', F_RES, L_HELP, (1,1,1)),
	('Heel_R', 'rigLeg&T_GoboFoot',		0.0, 'TumbleIn_R', F_RES, L_HELP, (1,1,1)),
	('RotateToe_R', 'rigLeg&T_GoboFoot',	0.0, 'Heel_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootTumble_R', 'rigLeg&T_GoboFoot',	0.0, 'FootGobo_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootRoll_R', 'rigLeg&T_GoboFoot',	-deg90, 'FootGobo_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootTarget_R', 'rigLeg&T_GoboFoot',	-footRoll, 'Heel_R', F_RES, L_HELP, (1,1,1)),
	('ToeTarget_R', 'rigLeg&T_GoboFoot',	-toeRoll, 'RotateToe_R', F_RES, L_HELP, (1,1,1)),

	# Both

	('KneePT_L', True,			0.0, None, F_WIR, L_LEGIK, (1,1,1)),
	('KneePT_R', True,			0.0, None, F_WIR, L_LEGIK, (1,1,1)),
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


LegPoses = [
	# Root
	
	('poseBone', True, 'LegRoot_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, []),
	('poseBone', True, 'LegRoot_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, []),	

	# Deform 

	('deformLimb', 'UpLeg_L', 'UpLegIK_L', (1,1,1), 'UpLegFK_L', (1,1,1), C_OW_LOCAL+C_TG_LOCAL, P_STRETCH),
	('poseBone', True, 'UpLegTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'LoLeg_L', 1, None, (True, False,False), 1.0])]),
	('deformLimb', 'LoLeg_L', 'LoLegIK_L', (1,1,1), 'LoLegFK_L', (1,1,1), 0, P_STRETCH),
	('deformLimb', 'Foot_L', 'FootIK_L', (1,1,1), 'FootFK_L', (1,1,1), 0, 0),
	('deformLimb', 'Toe_L', 'ToeIK_L', (1,1,1), 'ToeFK_L', (1,1,1), 0, 0),

	('deformLimb', 'UpLeg_R', 'UpLegIK_R', (1,1,1), 'UpLegFK_R', (1,0,1), C_OW_LOCAL+C_TG_LOCAL, P_STRETCH),
	('poseBone', True, 'UpLegTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'LoLeg_R', 1, None, (True, False,False), 1.0])]),
	('deformLimb', 'LoLeg_R', 'LoLegIK_R', (1,1,1), 'LoLegFK_R', (1,1,1), 0, P_STRETCH),
	('deformLimb', 'Foot_R', 'FootIK_R', (1,1,1), 'FootFK_R', (1,1,1), 0, 0),
	('deformLimb', 'Toe_R', 'ToeIK_R', (1,1,1), 'ToeFK_R', (1,1,1), 0, 0),


	# FK
	('poseBone', 'True', 'UpLegFK_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpLeg_L, (1,1,1)])]),

	('poseBone', 'True', 'LoLegFK_L', 'MHCircle025', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_L, (1,0,0)])]),

	('poseBone', 'True', 'FootFK_L', 'MHFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limFoot_L, (1,0,0)])]),

	('poseBone', 'True', 'ToeFK_L', 'MHToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limToe_L, (1,0,0)])]),

	('poseBone', 'True', 'UpLegFK_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpLeg_R, (1,1,1)])]),

	('poseBone', 'True', 'LoLegFK_R', 'MHCircle025', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_R, (1,0,0)])]),

	('poseBone', 'True', 'FootFK_R', 'MHFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limFoot_R, (1,0,0)])]),

	('poseBone', 'True', 'ToeFK_R', 'MHToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limToe_R, (1,0,0)])]),



	# IK Common

	('poseBone', True, 'UpLegIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpLeg_L, (True, True, True)])]),


	('poseBone', True, 'UpLegIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpLeg_R, (True, True, True)])]),


	# IK reverse foot

	('poseBone', 'rigLeg&T_InvFoot', 'FootCtrl_L', 'MHFootCtrl_L', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['World', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Hip', 'LegRoot_L', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['LegRoot_L', 'fNoStretch', 'LegRoot_L'])]),

	('poseBone', 'rigLeg&T_InvFoot', 'FootCtrl_R', 'MHFootCtrl_R', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['World', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Hip', 'LegRoot_R', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['LegRoot_R', 'fNoStretch', 'LegRoot_R'])]),

	('poseBone', 'rigLeg&T_InvFoot', 'LoLegIK_L', None, 'ik', (1,1,1), (0,1,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'Ankle_L', 2, (90*deg1, 'KneePT_L'), (True, False,True), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_L, (True, True, True)]),
		]),

	('poseBone', 'rigLeg&T_InvFoot', 'LoLegIK_R', None, 'ik', (1,1,1), (0,1,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'Ankle_R', 2, (90*deg1, 'KneePT_R'), (True, False,True), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_R, (True, True, True)]),
		]),

	('poseBone', 'rigLeg&T_InvFoot', 'FootRevIK_L', 'MHRevFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevFoot_L, (True, True, True)])]),

	('poseBone', 'rigLeg&T_InvFoot', 'FootRevIK_R', 'MHRevFoot', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevFoot_R, (True, True, True)])]),

	('poseBone', 'rigLeg&T_InvFoot', 'FootIK_L', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootRevIK_L', 1, None, (True, False,True), 1.0])]),

	('poseBone', 'rigLeg&T_InvFoot', 'FootIK_R', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootRevIK_R', 1, None, (True, False,True), 1.0])]),

	('poseBone', 'rigLeg&T_InvFoot', 'ToeRevIK_L', 'MHRevToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevToe_L, (True, True, True)])]),

	('poseBone', 'rigLeg&T_InvFoot', 'ToeRevIK_R', 'MHRevToe', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevToe_R, (True, True, True)])]),

	('poseBone', 'rigLeg&T_InvFoot', 'ToeIK_L', None, None, (1,1,1), (0,1,1), (1,1,0), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeRevIK_L', 1, None, (True, False,True), 1.0])]),

	('poseBone', 'rigLeg&T_InvFoot', 'ToeIK_R', None, None, (1,1,1), (0,1,1), (1,1,0), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeRevIK_R', 1, None, (True, False,True), 1.0])]),

	('poseBone', 'rigLeg&T_InvFoot', 'KneePT_L', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Foot', 'FootCtrl_L', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Hip', 'LegRoot_L', 0.0, (1,1,1), (1,1,1), (1,1,1)])]),

	('poseBone', 'rigLeg&T_InvFoot', 'KneePT_R', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Foot', 'FootCtrl_R', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Hip', 'LegRoot_R', 0.0, (1,1,1), (1,1,1), (1,1,1)])]),



	# IK Gobo
		
	('poseBone', 'rigLeg&T_GoboFoot', 'LoLegIK_L', None, 'ik', (1,1,1), (0,1,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'LegTarget_L', 2, (1.2708, 'KneePT_L'), (True, False,True), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-2.6,0, 0,0, 0,0), (True, True, True)]),
		]),

	('poseBone', 'rigLeg&T_GoboFoot', 'LoLegIK_R', None, 'ik', (1,1,1), (0,1,1), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IK', 'LegTarget_R', 2, (1.8708, 'KneePT_R'), (True, False,True), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', (-2.6,0, 0,0, 0,0), (True, True, True)]),
		]),

	('poseBone', 'rigLeg&T_GoboFoot', 'FootGobo_L', 'GoboFootCtrl_L', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['World', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Hip', 'LegRoot_L', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['LegRoot_L', 'fNoStretch',  'LegRoot_L'])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'FootGobo_R', 'GoboFootCtrl_R', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('ChildOf', C_CHILDOF, ['World', 'Root', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Hip', 'LegRoot_R', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['LegRoot_R', 'fNoStretch', 'LegRoot_R'])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'KneePT_L', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Hip', 'LegRoot_L', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Foot', 'FootGobo_L', 1.0, (1,1,1), (1,1,1), (1,1,1)])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'KneePT_R', 'MHCube05', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, ['Hip', 'LegRoot_L', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Foot', 'FootGobo_R', 1.0, (1,1,1), (1,1,1), (1,1,1)])]),



	('poseBone', 'rigLeg&T_GoboFoot', 'FootIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootTarget_L', 1, None, (True, True,True), 1.0])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'ToeIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeTarget_L', 1, None, (True, True,True), 1.0])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'TipToe_L', 'GoboTipToe_L', None, (1,1,1), (0,0,1), (1,1,1), (1,1,1), 0, []),
	#	[('LimitRot', C_OW_LOCAL, ['LimitRot', (0,2.96706, 0,0, 0,0), (1,0,0)])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'FootRoll_L', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (1,1, 0,0, 0,0)])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'FootTumble_L', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (1,1, 0,0, 0,0)])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'TumbleOut_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootTumble', 'FootTumble_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'TumbleIn_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootTumble', 'FootTumble_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'Heel_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootRoll', 'FootRoll_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'RotateToe_L', 'GoboRotate_L', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'rigLeg&T_GoboFoot', 'FootTarget_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootRoll', 'FootRoll_L', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])]),


	('poseBone', 'rigLeg&T_GoboFoot', 'FootIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootTarget_R', 1, None, (True, True,True), 1.0])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'ToeIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeTarget_R', 1, None, (True, True,True), 1.0])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'TipToe_R', 'GoboTipToe_R', None, (1,1,1), (0,0,1), (1,1,1), (1,1,1), 0, []),
	#	[('LimitRot', C_OW_LOCAL, ['LimitRot', (0,2.96706, 0,0, 0,0), (1,0,0)])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'FootRoll_R', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (1,1, 0,0, 0,0)])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'FootTumble_R', 'GoboArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (1,1, 0,0, 0,0)])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'TumbleOut_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootTumble', 'FootTumble_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'TumbleIn_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootTumble', 'FootTumble_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'Heel_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootRoll', 'FootRoll_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])]),

	('poseBone', 'rigLeg&T_GoboFoot', 'RotateToe_R', 'GoboRotate_R', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, []),

	('poseBone', 'rigLeg&T_GoboFoot', 'FootTarget_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TG_LOCAL, ['Action', 'goboFootRoll', 'FootRoll_R', 'LOCATION_X', (1,21), (-0.5,0.5), 1.0])]),


	# IK both

	('poseBone', True, 'KneeHandle_L', None, 'ik', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['StretchTo', 'KneePT_L', 'PLANE_X'])]),

	('poseBone', True, 'KneeHandle_R', None, 'ik', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, ['StretchTo', 'KneePT_R', 'PLANE_X'])]),
]


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
	("UpLeg_L", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PLegIK_L", "LOC_X"),
	("LoLeg_L", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PLegIK_L", "LOC_X"),
	("Foot_L", True, ["RotFK"], ["RotIK"], "PLegIK_L", "LOC_X"),
	("Toe_L", True, ["RotFK"], ["RotIK"], "PLegIK_L", "LOC_X"),
	
	("UpLeg_R", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PLegIK_R", "LOC_X"),
	("LoLeg_R", True, ["RotFK", "StretchFK"], ["RotIK", "StretchIK"], "PLegIK_R", "LOC_X"),
	("Foot_R", True, ["RotFK"], ["RotIK"], "PLegIK_R", "LOC_X"),
	("Toe_R", True, ["RotFK"], ["RotIK"], "PLegIK_R", "LOC_X"),

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
	("UpLeg_L", "X", 0.2),
	("UpLegTwist_L", "X", 0.2),
	("LoLeg_L", "X", -0.4),
	("Foot_L", "X", 0.2),

	("UpLeg_R", "X", 0.2),
	("UpLegTwist_R", "X", 0.2),
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
	('KneePT_L', 'UpLeg_L'),
	('Ankle_L', 'LoLeg_L'),
	('FootCtrl_L', 'Foot_L'),

	('KneePT_R', 'UpLeg_R'),
	('Ankle_R', 'LoLeg_R'),
	('FootCtrl_R', 'Foot_R'),

	('FootGobo_L', 'LoLeg_L'),
	('LegTarget_L', 'LoLeg_L'),
	('TipToe_L', 'Toe_L'),
	('TumbleOut_L', 'Foot_L'),
	('TumbleIn_L', 'Foot_L'),
	('Heel_L', 'Foot_L',),
	('RotateToe_L', 'Toe_L'),
	('FootRoll_L', 'Toe_L'),
	('FootTumble_L', 'Toe_L'),
	('FootTarget_L', 'Foot_L'),
	('ToeTarget_L', 'Toe_L'),

	('FootGobo_R', 'LoLeg_R'),
	('LegTarget_R', 'LoLeg_R'),
	('TipToe_R', 'Toe_R'),
	('TumbleOut_R', 'Foot_R'),
	('TumbleIn_R', 'Foot_R'),
	('Heel_R', 'Foot_R',),
	('RotateToe_R', 'Toe_R'),
	('FootRoll_R', 'Toe_R'),
	('FootTumble_R', 'Toe_R'),
	('FootTarget_R', 'Foot_R'),
	('ToeTarget_R', 'Toe_R'),
]

LegSelects = [
	'Foot_L', 'Toe_L', 'FootFK_L', 'ToeFK_L', 'FootIK_L', 'ToeIK_L', 'FootRevIK_L', 'ToeRevIK_L', 'FootCtrl_L', 'FootGobo_L',
	'Foot_R', 'Toe_R', 'FootFK_R', 'ToeFK_R', 'FootIK_R', 'ToeIK_R', 'FootRevIK_R', 'ToeRevIK_R', 'FootCtrl_R', 'FootGobo_R',
]	

LegRolls = [
	('FootCtrl_L', -0.23),
	('FootCtrl_R', 0.23),
	('FootRevIK_L', pi),
	('FootRevIK_R', pi),
]


