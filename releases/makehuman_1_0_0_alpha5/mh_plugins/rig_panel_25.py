#
#	Panel bone definitions
#

import mhx_rig
from mhx_rig import *

offs = [0, 0, 0.3]

PanelJoints = [
	('origin',			'o', ('head', [-3.3, 0.5, 0.0])),
	('PFaceDisp_tail',		'o', ('origin', [0.0, 0.0, 1.0])),
	('PFace_head',			'o', ('origin', [0.0, -1.5, 0.0])),
	('PFace_tail',			'o', ('PFace_head', [0.0, 0.0, 1.0])),
	('PBrow_R_head',		'o', ('origin', [-0.4, 0.8, 0.0])),
	('PBrow_R_tail',		'o', ('PBrow_R_head', offs)),
	('PBrow_L_head',		'o', ('origin', [0.4, 0.8, 0.0])),
	('PBrow_L_tail',		'o', ('PBrow_L_head', offs)),
	('PBrows_head',			'o', ('origin', [0.0, 0.8, 0.0])),
	('PBrows_tail',			'o', ('PBrows_head', offs)),
	('PUpLid_R_head',		'o', ('origin', [-0.4, 0.6, 0.0])),
	('PUpLid_R_tail',		'o', ('PUpLid_R_head', offs)),
	('PUpLid_L_head',		'o', ('origin', [0.4, 0.6, 0.0])),
	('PUpLid_L_tail',		'o', ('PUpLid_L_head', offs)),
	('PLoLid_R_head',		'o', ('origin', [-0.4, 0.2, 0.0])),
	('PLoLid_R_tail',		'o', ('PLoLid_R_head', offs)),
	('PLoLid_L_head',		'o', ('origin', [0.4, 0.2, 0.0])),
	('PLoLid_L_tail',		'o', ('PLoLid_L_head', offs)),
	('PCheek_R_head',		'o', ('origin', [-0.4, 0.0, 0.0])),
	('PCheek_R_tail',		'o', ('PCheek_R_head', offs)),
	('PCheek_L_head',		'o', ('origin', [0.4, 0.0, 0.0])),
	('PCheek_L_tail',		'o', ('PCheek_L_head', offs)),
	('PNose_tail',			'o', ('origin', offs)),
	('PUpLip_head',			'o', ('origin', [0.0, -0.2, 0.0])),
	('PUpLip_tail',			'o', ('PUpLip_head', offs)),
	('PLoLip_head',			'o', ('origin', [0.0, -0.8, 0.0])),
	('PLoLip_tail',			'o', ('PLoLip_head', offs)),
	('PMouth_head',			'o', ('origin', [0.0, -0.5, 0.0])),
	('PMouth_tail',			'o', ('PMouth_head', offs)),
	('PUpLip_R_head',		'o', ('origin', [-0.2, -0.4, 0.0])),
	('PUpLip_R_tail',		'o', ('PUpLip_R_head', offs)),
	('PUpLip_L_head',		'o', ('origin', [0.2, -0.4, 0.0])),
	('PUpLip_L_tail',		'o', ('PUpLip_L_head', offs)),
	('PLoLip_R_head',		'o', ('origin', [-0.2, -0.6, 0.0])),
	('PLoLip_R_tail',		'o', ('PLoLip_R_head', offs)),
	('PLoLip_L_head',		'o', ('origin', [0.2, -0.6, 0.0])),
	('PLoLip_L_tail',		'o', ('PLoLip_L_head', offs)),
	('PMouth_R_head',		'o', ('origin', [-0.5, -0.5, 0.0])),
	('PMouth_R_tail',		'o', ('PMouth_R_head', offs)),
	('PMouth_L_head',		'o', ('origin', [0.5, -0.5, 0.0])),
	('PMouth_L_tail',		'o', ('PMouth_L_head', offs)),
	('PTounge_head',		'o', ('origin', [0.0, -1.0, 0.0])),
	('PTounge_tail',		'o', ('PTounge_head', offs)),
	('PJaw_head',			'o', ('origin', [0.0, -1.1, 0.0])),
	('PJaw_tail',			'o', ('PJaw_head', offs)),

	('PArmIK_R_head',		'o', ('origin', [-1.1, 2.0, 0.0])),
	('PArmIK_R_tail',		'o', ('PArmIK_R_head', offs)),
	('PArmIK_L_head',		'o', ('origin', [0.1, 2.0, 0.0])),
	('PArmIK_L_tail',		'o', ('PArmIK_L_head', offs)),

	('PLegIK_R_head',		'o', ('origin', [-1.1, 1.5, 0.0])),
	('PLegIK_R_tail',		'o', ('PLegIK_R_head', offs)),
	('PLegIK_L_head',		'o', ('origin', [0.1, 1.5, 0.0])),
	('PLegIK_L_tail',		'o', ('PLegIK_L_head', offs)),

	('PHandLocal_R_head',		'o', ('origin', [-1.1, 2.0, 0.0])),
	('PHandLocal_R_tail',		'o', ('PHandLocal_R_head', offs)),
	('PHandLocal_L_head',		'o', ('origin', [0.1, 2.0, 0.0])),
	('PHandLocal_L_tail',		'o', ('PHandLocal_L_head', offs)),

	('PFootLocal_R_head',		'o', ('origin', [-1.1, 1.5, 0.0])),
	('PFootLocal_R_tail',		'o', ('PFootLocal_R_head', offs)),
	('PFootLocal_L_head',		'o', ('origin', [0.1, 1.5, 0.0])),
	('PFootLocal_L_tail',		'o', ('PFootLocal_L_head', offs)),

	('MHRelax_L_head',		'o', ('origin', [1.5, 1.0, 0.0])),
	('MHRelax_L_tail',		'o', ('MHRelax_L_head', offs)),
	('MHCurl_L_head',		'o', ('MHRelax_L_head', [0.0, -0.5, 0.0])),
	('MHCurl_L_tail',		'o', ('MHCurl_L_head', offs)),
	('MHCone_L_head',		'o', ('MHRelax_L_head', [0.0, -1.0, 0.0])),
	('MHCone_L_tail',		'o', ('MHCone_L_head', offs)),
	('MHSpread_L_head',		'o', ('MHRelax_L_head', [0.0, -1.5, 0.0])),
	('MHSpread_L_tail',		'o', ('MHSpread_L_head', offs)),
	('MHScrunch_L_head',		'o', ('MHRelax_L_head', [0.0, -2.0, 0.0])),
	('MHScrunch_L_tail',		'o', ('MHScrunch_L_head', offs)),
	('MHLean_L_head',		'o', ('MHRelax_L_head', [0.0, -2.5, 0.0])),
	('MHLean_L_tail',		'o', ('MHLean_L_head', offs)),

	('MHRelax_R_head',		'o', ('origin', [-1.5, 1.0, 0.0])),
	('MHRelax_R_tail',		'o', ('MHRelax_R_head', offs)),
	('MHCurl_R_head',		'o', ('MHRelax_R_head', [0.0, -0.5, 0.0])),
	('MHCurl_R_tail',		'o', ('MHCurl_R_head', offs)),
	('MHCone_R_head',		'o', ('MHRelax_R_head', [0.0, -1.0, 0.0])),
	('MHCone_R_tail',		'o', ('MHCone_R_head', offs)),
	('MHSpread_R_head',		'o', ('MHRelax_R_head', [0.0, -1.5, 0.0])),
	('MHSpread_R_tail',		'o', ('MHSpread_R_head', offs)),
	('MHScrunch_R_head',		'o', ('MHRelax_R_head', [0.0, -2.0, 0.0])),
	('MHScrunch_R_tail',		'o', ('MHScrunch_R_head', offs)),
	('MHLean_R_head',		'o', ('MHRelax_R_head', [0.0, -2.5, 0.0])),
	('MHLean_R_tail',		'o', ('MHLean_R_head', offs)),

]

PanelHeadsTails = [
	('PFace',			'PFace_head', 'PFace_tail'),
	('PFaceDisp',			'origin', 'PFaceDisp_tail'),
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
	#('PHandLocal_R',		'PHandLocal_R_head', 'PHandLocal_R_tail'),
	#('PHandLocal_L',		'PHandLocal_L_head', 'PHandLocal_L_tail'),
	#('PFootLocal_R',		'PFootLocal_R_head', 'PFootLocal_R_tail'),
	#('PFootLocal_L',		'PFootLocal_L_head', 'PFootLocal_L_tail'),

	('MHRelax_L',			'MHRelax_L_head', 'MHRelax_L_tail'),
	('MHCurl_L',			'MHCurl_L_head', 'MHCurl_L_tail'),
	('MHCone_L',			'MHCone_L_head', 'MHCone_L_tail'),
	('MHSpread_L',			'MHSpread_L_head', 'MHSpread_L_tail'),
	('MHScrunch_L',			'MHScrunch_L_head', 'MHScrunch_L_tail'),
	('MHLean_L',			'MHLean_L_head', 'MHLean_L_tail'),

	('MHRelax_R',			'MHRelax_R_head', 'MHRelax_R_tail'),
	('MHCurl_R',			'MHCurl_R_head', 'MHCurl_R_tail'),
	('MHCone_R',			'MHCone_R_head', 'MHCone_R_tail'),
	('MHSpread_R',			'MHSpread_R_head', 'MHSpread_R_tail'),
	('MHScrunch_R',			'MHScrunch_R_head', 'MHScrunch_R_tail'),
	('MHLean_R',			'MHLean_R_head', 'MHLean_R_tail'),
	]


PanelArmature = [
	('PFace', 'toggle&T_Panel',		pi, None, F_WIR, L_PANEL, (1,1,1) ),
	('PFaceDisp', 'toggle&T_Panel',		pi, 'PFace', F_WIR+F_RES, L_PANEL, (1,1,1) ),
	('PBrow_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PBrow_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PBrows', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLid_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLid_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLid_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLid_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PCheek_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PCheek_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PNose', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PUpLip', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PLoLip', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PMouth', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLip_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLip_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLip_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLip_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PMouth_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PMouth_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PTounge', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PJaw', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),

	('PArmIK_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PArmIK_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLegIK_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLegIK_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PHandLocal_R', 'toggle&T_Panel',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PHandLocal_L', 'toggle&T_Panel',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PFootLocal_R', 'toggle&T_Panel',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PFootLocal_L', 'toggle&T_Panel',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),

	('MHRelax_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('MHCurl_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('MHCone_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('MHSpread_L', 'toggle&T_Panel',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('MHScrunch_L', 'toggle&T_Panel',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('MHLean_L', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),

	('MHRelax_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('MHCurl_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('MHCone_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('MHSpread_R', 'toggle&T_Panel',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('MHScrunch_R', 'toggle&T_Panel',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('MHLean_R', 'toggle&T_Panel',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),

]

#
#	PanelWritePoses(fp):
#

MX = 0.25


def PanelWritePoses(fp):
	addPoseBone(fp, 'toggle&T_Panel', 'PFace', 'MHCube05', None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0, [])

	addPoseBone(fp, 'toggle&T_Panel', 'PFaceDisp', 'MHFace', None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])

	cSlider(fp,  'PBrow_L', MX)
	cSlider(fp,  'PBrow_R', MX)
	cSlider(fp,  'PBrows', MX)
	cSlider(fp,  'PUpLid_L', MX)
	cSlider(fp,  'PUpLid_R', MX)
	cSlider(fp,  'PLoLid_L', MX)
	cSlider(fp,  'PLoLid_R', MX)
	cSlider(fp,  'PCheek_L', MX)
	cSlider(fp,  'PCheek_R', MX)
	cSlider(fp,  'PNose', MX)
	cSlider(fp,  'PUpLip_L', MX)
	cSlider(fp,  'PUpLip_R', MX)
	cSlider(fp,  'PLoLip_L', MX)
	cSlider(fp,  'PLoLip_R', MX)
	cSlider(fp,  'PMouth_L', MX)
	cSlider(fp,  'PMouth_R', MX)
	cSlider(fp,  'PTounge', MX)
	cSlider(fp,  'PJaw', MX)

	xSlider(fp, 'PArmIK_L', 0.0, 1.0)
	xSlider(fp, 'PArmIK_R', 0.0, 1.0)
	xSlider(fp, 'PLegIK_L', 0.0, 1.0)
	xSlider(fp, 'PLegIK_R', 0.0, 1.0)
	#xSlider(fp, 'PHandLocal_L', 0.0, 1.0)
	#xSlider(fp, 'PHandLocal_R', 0.0, 1.0)
	#xSlider(fp, 'PFootLocal_L', 0.0, 1.0)
	#xSlider(fp, 'PFootLocal_R', 0.0, 1.0)

	xSlider(fp, 'MHRelax_L', -0.25, 0.5)
	xSlider(fp, 'MHCurl_L', -0.25, 0.5)
	xSlider(fp, 'MHCone_L', -0.25, 0.5)
	xSlider(fp, 'MHSpread_L', -0.25, 0.5)
	xSlider(fp, 'MHScrunch_L', -0.25, 0.5)
	xSlider(fp, 'MHLean_L', -0.5, 0.5)

	xSlider(fp, 'MHRelax_R', -0.5, 0.25)
	xSlider(fp, 'MHCurl_R', -0.5, 0.25)
	xSlider(fp, 'MHCone_R', -0.5, 0.25)
	xSlider(fp, 'MHSpread_R', -0.5, 0.25)
	xSlider(fp, 'MHScrunch_R', -0.5, 0.25)
	xSlider(fp, 'MHLean_R', -0.5, 0.5)

	return

def cSlider(fp, bone, mx):
	addPoseBone(fp, 'toggle&T_Panel', bone, 'MHSolid025', None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL+C_LTRA, ['Const', (-mx,mx, 0,0, -mx,mx), (1,1,1,1,1,1)])])

def xSlider(fp, bone, mn, mx):
	addPoseBone(fp, 'toggle&T_Panel', bone, 'MHSolid025', None, (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OW_LOCAL+C_LTRA, ['Const', (mn,mx, 0,0, 0,0), (1,1,1,1,1,1)])])

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

