#
#	Panel bone definitions
#

import mhx_rig
from mhx_rig import *

PanelJoints = [
	('origin',			'o', ('head', [-2.5, 0.5, 0.0])),
	('PFace_tail',			'o', ('origin', [0.0, 0.0, 1.0])),
	('PBrow_R_head',		'o', ('origin', [-0.4, 0.8, 0.0])),
	('PBrow_R_tail',		'o', ('origin', [-0.4, 0.8, 0.3])),
	('PBrow_L_head',		'o', ('origin', [0.4, 0.8, 0.0])),
	('PBrow_L_tail',		'o', ('origin', [0.4, 0.8, 0.3])),
	('PBrows_head',			'o', ('origin', [0.0, 0.8, 0.0])),
	('PBrows_tail',			'o', ('origin', [0.0, 0.8, 0.3])),
	('PUpLid_R_head',		'o', ('origin', [-0.4, 0.6, 0.0])),
	('PUpLid_R_tail',		'o', ('origin', [-0.4, 0.6, 0.3])),
	('PUpLid_L_head',		'o', ('origin', [0.4, 0.6, 0.0])),
	('PUpLid_L_tail',		'o', ('origin', [0.4, 0.6, 0.3])),
	('PLoLid_R_head',		'o', ('origin', [-0.4, 0.2, 0.0])),
	('PLoLid_R_tail',		'o', ('origin', [-0.4, 0.2, 0.3])),
	('PLoLid_L_head',		'o', ('origin', [0.4, 0.2, 0.0])),
	('PLoLid_L_tail',		'o', ('origin', [0.4, 0.2, 0.3])),
	('PCheek_R_head',		'o', ('origin', [-0.4, 0.0, 0.0])),
	('PCheek_R_tail',		'o', ('origin', [-0.4, 0.0, 0.3])),
	('PCheek_L_head',		'o', ('origin', [0.4, 0.0, 0.0])),
	('PCheek_L_tail',		'o', ('origin', [0.4, 0.0, 0.3])),
	('PNose_tail',			'o', ('origin', [0.0, 0.0, 0.3])),
	('PUpLip_head',			'o', ('origin', [0.0, -0.2, 0.0])),
	('PUpLip_tail',			'o', ('origin', [0.0, -0.2, 0.3])),
	('PLoLip_head',			'o', ('origin', [0.0, -0.8, 0.0])),
	('PLoLip_tail',			'o', ('origin', [0.0, -0.8, 0.3])),
	('PMouth_head',			'o', ('origin', [0.0, -0.5, 0.0])),
	('PMouth_tail',			'o', ('origin', [0.0, -0.5, 0.3])),
	('PUpLip_R_head',		'o', ('origin', [-0.2, -0.4, 0.0])),
	('PUpLip_R_tail',		'o', ('origin', [-0.2, -0.4, 0.3])),
	('PUpLip_L_head',		'o', ('origin', [0.2, -0.4, 0.0])),
	('PUpLip_L_tail',		'o', ('origin', [0.2, -0.4, 0.3])),
	('PLoLip_R_head',		'o', ('origin', [-0.2, -0.6, 0.0])),
	('PLoLip_R_tail',		'o', ('origin', [-0.2, -0.6, 0.3])),
	('PLoLip_L_head',		'o', ('origin', [0.2, -0.6, 0.0])),
	('PLoLip_L_tail',		'o', ('origin', [0.2, -0.6, 0.3])),
	('PMouth_R_head',		'o', ('origin', [-0.5, -0.5, 0.0])),
	('PMouth_R_tail',		'o', ('origin', [-0.5, -0.5, 0.3])),
	('PMouth_L_head',		'o', ('origin', [0.5, -0.5, 0.0])),
	('PMouth_L_tail',		'o', ('origin', [0.5, -0.5, 0.3])),
	('PTounge_head',		'o', ('origin', [0.0, -1.0, 0.0])),
	('PTounge_tail',		'o', ('origin', [0.0, -1.0, 0.3])),
	('PJaw_head',			'o', ('origin', [0.0, -1.1, 0.0])),
	('PJaw_tail',			'o', ('origin', [0.0, -1.1, 0.3])),
	('PArmIK_R_head',		'o', ('origin', [-1.1, 2.0, 0.0])),
	('PArmIK_R_tail',		'o', ('origin', [-1.1, 2.0, 0.3])),
	('PArmIK_L_head',		'o', ('origin', [0.1, 2.0, 0.0])),
	('PArmIK_L_tail',		'o', ('origin', [0.1, 2.0, 0.3])),
	('PLegIK_R_head',		'o', ('origin', [-1.1, 1.5, 0.0])),
	('PLegIK_R_tail',		'o', ('origin', [-1.1, 1.5, 0.3])),
	('PLegIK_L_head',		'o', ('origin', [0.1, 1.5, 0.0])),
	('PLegIK_L_tail',		'o', ('origin', [0.1, 1.5, 0.3])),

	('ikfk_foot_L_head',		'o', ('foot_roll_L_head', [0.0,0,0.6])),
	('ikfk_foot_L_tail',		'o', ('ikfk_foot_L_head', [-0.6,0,0])),
	('ikfk_foot_R_head',		'o', ('foot_roll_R_head', [0,0,0.6])),
	('ikfk_foot_R_tail',		'o', ('ikfk_foot_R_head', [-0.6,0,0])),

	('ikfk_hand_L_head',		'o', ('r-finger-3-3', [2,0,0])),
	('ikfk_hand_L_tail',		'o', ('ikfk_hand_L_head', [-1,0,0])),
	('ikfk_hand_R_head',		'o', ('l-finger-3-3', [-2,0,0])),
	('ikfk_hand_R_tail',		'o', ('ikfk_hand_R_head', [1,0,0])),
]

PanelHeadsTails = [
	('PFace',			'origin', 'PFace_tail'),
	('PBrow_R',			'PBrow_R_head', 'PBrow_R_tail'),
	('PBrow_L',			'PBrow_L_head', 'PBrow_L_tail'),
	('PBrows',			'PBrows_head', 'PBrows_tail'),
	('PUpLid_R',			'PUpLid_R_head', 'PUpLid_R_tail'),
	('PUpLid_L',			'PUpLid_L_head', 'PUpLid_L_tail'),
	('PLoLid_R',			'PLoLid_R_head', 'PLoLid_R_tail'),
	('PLoLid_L',			'PLoLid_L_head', 'PLoLid_L_tail'),
	('PCheek_R',			'PCheek_R_head', 'PCheek_R_tail'),
	('PCheek_L',			'PCheek_L_head', 'PCheek_L_tail'),
	('PNose',			'origin', 'PNose_tail'),
	#('PUpLip',			'PUpLip_head', 'PUpLip_tail'),
	#('PLoLip',			'PLoLip_head', 'PLoLip_tail'),
	#('PMouth',			'PMouth_head', 'PMouth_tail'),
	('PUpLip_R',			'PUpLip_R_head', 'PUpLip_R_tail'),
	('PUpLip_L',			'PUpLip_L_head', 'PUpLip_L_tail'),
	('PLoLip_R',			'PLoLip_R_head', 'PLoLip_R_tail'),
	('PLoLip_L',			'PLoLip_L_head', 'PLoLip_L_tail'),
	('PMouth_R',			'PMouth_R_head', 'PMouth_R_tail'),
	('PMouth_L',			'PMouth_L_head', 'PMouth_L_tail'),
	('PTounge',			'PTounge_head', 'PTounge_tail'),
	('PJaw',			'PJaw_head', 'PJaw_tail'),
	('PArmIK_R',			'PArmIK_R_head', 'PArmIK_R_tail'),
	('PArmIK_L',			'PArmIK_L_head', 'PArmIK_L_tail'),
	('PLegIK_R',			'PLegIK_R_head', 'PLegIK_R_tail'),
	('PLegIK_L',			'PLegIK_L_head', 'PLegIK_L_tail'),
	]
'''
	('LegFkIk_L',			'ikfk_foot_L_head', 'ikfk_foot_L_tail'),
	('LegFkIk_R',			'ikfk_foot_R_head', 'ikfk_foot_R_tail'),

	('ArmFkIk_L',			'ikfk_hand_L_head', 'ikfk_hand_L_tail'),
	('ArmFkIk_R',			'ikfk_hand_R_head', 'ikfk_hand_R_tail'),
'''	
PanelArmature = [
	('PFace', 'toggle&T_Panel',	-3.14159, None, F_WIR, L_PANEL, (1,1,1) ),
	('PBrow_R', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PBrow_L', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PBrows', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLid_R', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLid_L', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLid_R', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLid_L', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PCheek_R', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PCheek_L', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PNose', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PUpLip', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PLoLip', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PMouth', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLip_R', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLip_L', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLip_R', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLip_L', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PMouth_R', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PMouth_L', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PTounge', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PJaw', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PArmIK_R', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PArmIK_L', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLegIK_R', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLegIK_L', 'toggle&T_Panel',	-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),

]
'''
	('LegFkIk_L', 'rigLeg&T_LocalFKIK',	-1.5708, 'FootCtrl_L', F_WIR, L_MAIN+L_LEGIK+L_LEGFK, (1,1,1)),
	('LegFkIk_R', 'rigLeg&T_LocalFKIK',	-1.5708, 'FootCtrl_R', F_WIR, L_MAIN+L_LEGIK, (1,1,1)),

	('ArmFkIk_L', 'rigArm&T_LocalFKIK',	-1.5708, 'Clavicle_L', F_WIR, L_MAIN+L_ARMIK+L_ARMFK, (1,1,1)),
	('ArmFkIk_R', 'rigArm&T_LocalFKIK',	-1.5708, 'Clavicle_R', F_WIR, L_MAIN+L_ARMIK+L_ARMFK, (1,1,1)),
'''

#
#	PanelWritePoses(fp):
#

MX = 0.25


def PanelWritePoses(fp):
	addPoseBone(fp, 'toggle&T_Panel', 'PFace', 'MHFace', None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PBrow_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PBrow_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PBrows', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PUpLid_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PUpLid_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PLoLid_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PLoLid_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PCheek_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PCheek_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PNose', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])
	"""
	addPoseBone(fp, 'toggle&T_Panel', 'PUpLip', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PLoLip', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PMouth', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])
	"""
	addPoseBone(fp, 'toggle&T_Panel', 'PUpLip_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PUpLip_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PLoLip_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PLoLip_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PMouth_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PMouth_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PTounge', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PJaw', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, 
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (-MX,MX, 0,0, -MX,MX), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PArmIK_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (0,1, 0,0, 0,0), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PArmIK_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (0,1, 0,0, 0,0), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PLegIK_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (0,1, 0,0, 0,0), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'toggle&T_Panel', 'PLegIK_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER+C_LTRA, ['Const', (0,1, 0,0, 0,0), (1,1,1,1,1,1)])])

	return
'''
	# Leg FK ik
	addPoseBone(fp, 'rigLeg&T_LocalFKIK', 'LegFkIk_L', 'GoboIkfk', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (0,1, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'rigLeg&T_LocalFKIK', 'LegFkIk_R', 'GoboIkfk', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (0,1, 0,0, 0,0), (True,True, False,False, False,False)])])


	# Arm FK/IK
	addPoseBone(fp, 'rigArm&T_LocalFKIK', 'ArmFkIk_L', 'GoboIkfk', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (0,1, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'rigArm&T_LocalFKIK', 'ArmFkIk_R', 'GoboIkfk', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (0,1, 0,0, 0,0), (True,True, False,False, False,False)])])
	return
'''

'''
	'BendElbowForward_L' : ('LoArm_L', 'ROT_X', 1, 0, 1)],
	'BendElbowForward_R' : ('LoArm_R', 'ROT_X', 1, 0, 1)],
	'BendHeadForward' : ('Head', 'ROT_X', 3, 0, 1)],
	'BendKneeBack_L' : ('LoLeg_L', 'ROT_X', -2, -1, 0)],
	'BendKneeBack_R' : ('LoLeg_R', 'ROT_X', -2, -1, 0)],
	'BendLegBack_L' : ('UpLeg_L'), 'ROT_X', -1, -1, 0)],
	'BendLegBack_R' : ('UpLeg_R', 'ROT_X', -1, -1, 0)],
	'BendLegForward_L' : ('UpLeg_L', 'ROT_X', 1, 0, 1)],
	'BendLegForward_R' : ('UpLeg_R', 'ROT_X', 1, 0, 1)],
	'ShoulderDown_L' : ('UpArm_L', 'ROT_Z', 1, -1, 0)],
	'ShoulderDown_R' : ('UpArm_R', 'ROT_Z', 1, 0, 1)],
'''
#
#	Face representation
#

K = 1.0/MX

FaceDrivers = {
	# Brows
	'BrowsMidDown' : ('PBrows', 'LOC_Z', (0,K)),
	'BrowsMidUp' : ('PBrows', 'LOC_Z', (0,-K)),
	'BrowsSqueeze' : ('PBrows', 'LOC_X', (0,-K)),
	'BrowsDown_L' : ('PBrow_L', 'LOC_Z', (0,K)),
	'BrowsDown_R' : ('PBrow_R', 'LOC_Z', (0,K)),
	'BrowsOutUp_L' : ('PBrow_L', 'LOC_Z', (0,-K)),
	'BrowsOutUp_R' : ('PBrow_R', 'LOC_Z', (0,-K)),

#	Lids
	'UpLidDown_L' : ('PUpLid_L', 'LOC_Z', (0,K)),
	'UpLidDown_R' : ('PUpLid_R', 'LOC_Z', (0,K)),
	'LoLidUp_L' : ('PLoLid_L', 'LOC_Z', (0,-K)),
	'LoLidUp_R' : ('PLoLid_R', 'LOC_Z', (0,-K)),

#	Nose and jaw

	'Sneer_L' : ('PNose', 'LOC_X', (0,K)), 
	'Sneer_R' : ('PNose', 'LOC_X', (0,-K)), 
	'CheekUp_L' : ('PCheek_L', 'LOC_Z', (0,-K)),
	'CheekUp_R' : ('PCheek_R', 'LOC_Z', (0,-K)),
	'Squint_L' : ('PCheek_L', 'LOC_X', (0,K)),
	'Squint_R' : ('PCheek_R', 'LOC_X', (0,-K)),

#	Jaw and tounge
	'MouthOpen' : ('PJaw', 'LOC_Z', (0,K)),
	'TongueOut' : ('PJaw', 'LOC_X', (0,-K)),
	'ToungeUp' : ('PTounge', 'LOC_Z', (0,-K)),
	'ToungeLeft' : ('PTounge', 'LOC_X', (0,K)),
	'ToungeRight' : ('PTounge', 'LOC_X', (0,-K)),

#	Mouth expressions
	'Smile_L' : ('PMouth_L', 'LOC_X', (0,K)),
	'Smile_R' : ('PMouth_R', 'LOC_X', (0,-K)),
	'Frown_L' : ('PMouth_L', 'LOC_Z', (0,K)),
	'Frown_R' : ('PMouth_R', 'LOC_Z', (0,K)), 
	'Narrow_L' : ('PMouth_L', 'LOC_X', (0,-K)), 
	'Narrow_R' : ('PMouth_R', 'LOC_X', (0,K)),

#	Lips
	'UpLipUp_L' : ('PUpLip_L', 'LOC_Z', (0,-K)), 
	'UpLipUp_R' : ('PUpLip_R', 'LOC_Z', (0,-K)), 
	'UpLipDown_L' : ('PUpLip_L', 'LOC_Z', (0,K)), 
	'UpLipDown_R' : ('PUpLip_R', 'LOC_Z', (0,K)), 
	'LoLipUp_L' : ('PLoLip_L', 'LOC_Z', (0,-K)), 
	'LoLipUp_R' : ('PLoLip_R', 'LOC_Z', (0,-K)), 
	'LoLipDown_L' : ('PLoLip_L', 'LOC_Z', (0,K)), 
	'LoLipDown_R' : ('PLoLip_R', 'LOC_Z', (0,K)), 
}

