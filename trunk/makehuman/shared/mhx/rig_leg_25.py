#
#	Leg bone definitions
#

import mhx_rig
from mhx_rig import *

offs = [0,0.6,0]

LegJoints = [
	# Deform
	('r-heel0',			'v', 5721),
	('r-heel',			'p', ['r-foot-2', 'r-foot-1', 'r-heel0']),
	('r-ankle-tip',		'o', ('r-ankle', [0.0, 0.0, -1.0])),

	('l-heel0',			'v', 13338),
	('l-heel',			'p', ['l-foot-2', 'l-foot-1', 'l-heel0']),
	('l-ankle-tip',			'o', ('l-ankle', [0.0, 0.0, -1.0])),

]

LegHeadsTails = [
	# Deform 
	('UpLeg_L',			'r-upper-leg', 'r-knee'),
	('LoLeg_L',			'r-knee', 'r-ankle'),
	('Foot_L',			'r-ankle', 'r-foot-1'),
	('Toe_L',			'r-foot-1', 'r-foot-2'),

	('UpLeg_R',			'l-upper-leg', 'l-knee'),
	('LoLeg_R',			'l-knee', 'l-ankle'),
	('Foot_R',			'l-ankle', 'l-foot-1'),
	('Toe_R',			'l-foot-1', 'l-foot-2'),

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
]

upLegRoll = 0
loLegRoll = 0
footRoll = 0
toeRoll = 0
#toeRoll = -0.646
footCtrlRoll = 0.0

LegArmature = [
	# Deform
	('UpLeg_L',			upLegRoll, 'Hip_L', F_DEF, L_DEF, (1,1,1) ),
	('LoLeg_L',			loLegRoll, 'UpLeg_L', F_DEF, L_DEF, (1,1,1) ),
	('Foot_L',			footRoll, 'LoLeg_L', F_DEF, L_DEF, (1,1,1) ),
	('Toe_L',			toeRoll, 'Foot_L', F_DEF, L_DEF, (1,1,1) ),

	('UpLeg_R',			-upLegRoll, 'Hip_R', F_DEF, L_DEF, (1,1,1) ),
	('LoLeg_R',			-loLegRoll, 'UpLeg_R', F_DEF, L_DEF, (1,1,1) ),
	('Foot_R',			-footRoll, 'LoLeg_R', F_DEF, L_DEF, (1,1,1) ),
	('Toe_R',			-toeRoll, 'Foot_R', F_DEF, L_DEF, (1,1,1) ),

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
]

limUpLeg_L = (-140*deg1,60*deg1, -70*deg1,70*deg1, -deg90,deg45)
limUpLeg_R = (-140*deg1,60*deg1, -70*deg1,70*deg1, -deg45,deg90)

limLoLeg_L = (0,140*deg1, 0,0, 0,0)
limLoLeg_R = (0,140*deg1, 0,0, 0,0)

limFoot_L = (-deg45,deg45, 0,0, 0,0)
limFoot_R = (-deg45,deg45, 0,0, 0,0)

limToe_L = (-deg45,deg45, 0,0, 0,0)
limToe_R = (-deg45,deg45, 0,0, 0,0)

limRevFoot_L = (-deg45,deg45, 0,0, 0,0)
limRevFoot_R = (-deg45,deg45, 0,0, 0,0)

limRevToe_L = (-deg45,deg45, 0,0, 0,0)
limRevToe_R = (-deg45,deg45, 0,0, 0,0)


LegPoses = [
	# Deform 
	('deformLimb', 'UpLeg_L', 'UpLegIK_L', (1,1,1), 'UpLegFK_L', (1,1,1), C_OW_LOCAL+C_TG_LOCAL, P_STRETCH),
	('deformLimb', 'LoLeg_L', 'LoLegIK_L', (1,1,1), 'LoLegFK_L', (1,1,1), 0, P_STRETCH),
	('deformLimb', 'Foot_L', 'FootIK_L', (1,1,1), 'FootFK_L', (1,1,1), 0, 0),
	('deformLimb', 'Toe_L', 'ToeIK_L', (1,1,1), 'ToeFK_L', (1,1,1), 0, 0),

	('deformLimb', 'UpLeg_R', 'UpLegIK_R', (1,1,1), 'UpLegFK_R', (1,1,1), C_OW_LOCAL+C_TG_LOCAL, P_STRETCH),
	('deformLimb', 'LoLeg_R', 'LoLegIK_R', (1,1,1), 'LoLegFK_R', (1,1,1), 0, P_STRETCH),
	('deformLimb', 'Foot_R', 'FootIK_R', (1,1,1), 'FootFK_R', (1,1,1), 0, 0),
	('deformLimb', 'Toe_R', 'ToeIK_R', (1,1,1), 'ToeFK_R', (1,1,1), 0, 0),

	# FK
	('poseBone', 'UpLegFK_L', 'MHCircle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpLeg_L, (1,1,1)])]),

	('poseBone', 'LoLegFK_L', 'MHCircle025', 'FK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_L, (1,0,0)])]),

	('poseBone', 'FootFK_L', 'MHFoot', 'FK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limFoot_L, (1,0,0)])]),

	('poseBone', 'ToeFK_L', 'MHToe', 'FK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limToe_L, (1,0,0)])]),

	('poseBone', 'UpLegFK_R', 'MHCircle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpLeg_R, (1,1,1)])]),

	('poseBone', 'LoLegFK_R', 'MHCircle025', 'FK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_R, (1,0,0)])]),

	('poseBone', 'FootFK_R', 'MHFoot', 'FK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limFoot_R, (1,0,0)])]),

	('poseBone', 'ToeFK_R', 'MHToe', 'FK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limToe_R, (1,0,0)])]),


	# IK 
	('poseBone', 'UpLegIK_L', None, 'IK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpLeg_L, (True, True, True)])]),

	('poseBone', 'UpLegIK_R', None, 'IK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limUpLeg_R, (True, True, True)])]),

	('poseBone', 'LegIK_L', 'MHFootCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, ['Hip', 'Hip_L', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Hip_L', 'fNoStretch', 'Hip_L'])]),

	('poseBone', 'LegIK_R', 'MHFootCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		mhx_rig.rootChildOfConstraints + [
		('ChildOf', C_CHILDOF, ['Hip', 'Hip_R', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('LimitDist', 0, ['Hip_R', 'fNoStretch', 'Hip_R'])]),

	('poseBone', 'LoLegIK_L', None, 'IK_L', (1,1,1), (0,1,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IKPT', 'AnkleIK_L', 2, (90*deg1, 'KneePT_L'), (True, False,True), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_L, (True, True, True)]),
		]),

	('poseBone', 'LoLegIK_R', None, 'IK_R', (1,1,1), (0,1,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IKPT', 'AnkleIK_R', 2, (90*deg1, 'KneePT_R'), (True, False,True), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_R, (True, True, True)]),
		]),

	('poseBone', 'LoLegIK_L', None, 'IK_L', (1,1,1), (0,1,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IKNoPT', 'AnkleIK_L', 2, None, (True, False,True), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_L, (True, True, True)]),
		]),

	('poseBone', 'LoLegIK_R', None, 'IK_R', (1,1,1), (0,1,0), (1,1,1), (1,1,1), P_STRETCH,
		[('IK', 0, ['IKNoPT', 'AnkleIK_R', 2, None, (True, False,True), 1.0]),
		('LimitRot', C_OW_LOCAL, ['LimitRot', limLoLeg_R, (True, True, True)]),
		]),

	('poseBone', 'FootRevIK_L', 'MHRevFoot', 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevFoot_L, (True, True, True)])]),

	('poseBone', 'FootRevIK_R', 'MHRevFoot', 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevFoot_R, (True, True, True)])]),

	('poseBone', 'FootIK_L', None, 'IK_L', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootRevIK_L', 1, None, (True, False,True), 1.0])]),

	('poseBone', 'FootIK_R', None, 'IK_R', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['IK', 'FootRevIK_R', 1, None, (True, False,True), 1.0])]),

	('poseBone', 'ToeRevIK_L', 'MHRevToe', 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevToe_L, (True, True, True)])]),

	('poseBone', 'ToeRevIK_R', 'MHRevToe', 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitRot', C_OW_LOCAL, ['LimitRot', limRevToe_R, (True, True, True)])]),

	('poseBone', 'ToeIK_L', None, 'IK_L', (1,1,1), (0,1,1), (1,1,0), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeRevIK_L', 1, None, (True, False,True), 1.0])]),

	('poseBone', 'ToeIK_R', None, 'IK_R', (1,1,1), (0,1,1), (1,1,0), (1,1,1), 0, 
		[('IK', 0, ['IK', 'ToeRevIK_R', 1, None, (True, False,True), 1.0])]),
]

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


