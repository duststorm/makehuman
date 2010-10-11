#
#	Panel bone definitions
#

import mhx_rig
from mhx_rig import *

offs = [0, 0, 0.3]

PanelJoints = [
	('origin',		'o', ('head', [-3.3, 0.5, 0.0])),
	('PFace',		'o', ('origin', [0.0, -1.5, 0.0])),
	('PBrow_R',		'o', ('origin', [-0.4, 0.8, 0.0])),
	('PBrow_L',		'o', ('origin', [0.4, 0.8, 0.0])),
	('PBrows',		'o', ('origin', [0.0, 0.8, 0.0])),
	('PUpLid_R',		'o', ('origin', [-0.4, 0.6, 0.0])),
	('PUpLid_L',		'o', ('origin', [0.4, 0.6, 0.0])),
	('PLoLid_R',		'o', ('origin', [-0.4, 0.2, 0.0])),
	('PLoLid_L',		'o', ('origin', [0.4, 0.2, 0.0])),
	('PCheek_R',		'o', ('origin', [-0.4, 0.0, 0.0])),
	('PCheek_L',		'o', ('origin', [0.4, 0.0, 0.0])),
	('PUpLip',		'o', ('origin', [0.0, -0.2, 0.0])),
	('PLoLip',		'o', ('origin', [0.0, -0.8, 0.0])),
	('PMouth',		'o', ('origin', [0.0, -0.5, 0.0])),
	('PUpLip_R',		'o', ('origin', [-0.2, -0.4, 0.0])),
	('PUpLip_L',		'o', ('origin', [0.2, -0.4, 0.0])),
	('PLoLip_R',		'o', ('origin', [-0.2, -0.6, 0.0])),
	('PLoLip_L',		'o', ('origin', [0.2, -0.6, 0.0])),
	('PMouth_R',		'o', ('origin', [-0.5, -0.5, 0.0])),
	('PMouth_L',		'o', ('origin', [0.5, -0.5, 0.0])),
	('PTongue',		'o', ('origin', [0.0, -1.0, 0.0])),
	('PJaw',		'o', ('origin', [0.0, -1.1, 0.0])),

	('PArmIK_R',		'o', ('origin', [-1.1, 2.0, 0.0])),
	('PArmIK_L',		'o', ('origin', [0.1, 2.0, 0.0])),
	('PLegIK_R',		'o', ('origin', [-1.1, 1.5, 0.0])),
	('PLegIK_L',		'o', ('origin', [0.1, 1.5, 0.0])),

	('PFinger-1_R',		'o', ('origin', [-2.0, 1.0, 0.0])),
	('PFinger-2_R',		'o', ('origin', [-2.0, 0.5, 0.0])),
	('PFinger-3_R',		'o', ('origin', [-2.0, 0.0, 0.0])),
	('PFinger-4_R',		'o', ('origin', [-2.0, -0.5, 0.0])),
	('PFinger-5_R',		'o', ('origin', [-2.0, -1.0, 0.0])),

	('PFinger-1_L',		'o', ('origin', [1.2, 1.0, 0.0])),
	('PFinger-2_L',		'o', ('origin', [1.2, 0.5, 0.0])),
	('PFinger-3_L',		'o', ('origin', [1.2, 0.0, 0.0])),
	('PFinger-4_L',		'o', ('origin', [1.2, -0.5, 0.0])),
	('PFinger-5_L',		'o', ('origin', [1.2, -1.0, 0.0])),
]

PanelHeadsTails = [
	('PFace',			'PFace', ('PFace', [0,0,-1])),
	('PFaceDisp',			'origin', ('origin', [0,0,-1])),
	('PBrow_R',			'PBrow_R', ('PBrow_R', offs)),
	('PBrow_L',			'PBrow_L', ('PBrow_L', offs)),
	('PBrows',			'PBrows', ('PBrows', offs)),
	('PUpLid_R',			'PUpLid_R', ('PUpLid_R', offs)),
	('PUpLid_L',			'PUpLid_L', ('PUpLid_L', offs)),
	('PLoLid_R',			'PLoLid_R', ('PLoLid_R', offs)),
	('PLoLid_L',			'PLoLid_L', ('PLoLid_L', offs)),
	('PCheek_R',			'PCheek_R', ('PCheek_R', offs)),
	('PCheek_L',			'PCheek_L', ('PCheek_L', offs)),
	('PNose',			'origin', ('origin', offs)),
	#('PUpLip',			'PUpLip', ('PUpLip', offs)),
	#('PLoLip',			'PLoLip', ('PLoLip', offs)),
	#('PMouth',			'PMouth', ('PMouth', offs)),
	('PUpLip_R',			'PUpLip_R', ('PUpLip_R', offs)),
	('PUpLip_L',			'PUpLip_L', ('PUpLip_L', offs)),
	('PLoLip_R',			'PLoLip_R', ('PLoLip_R', offs)),
	('PLoLip_L',			'PLoLip_L', ('PLoLip_L', offs)),
	('PMouth_R',			'PMouth_R', ('PMouth_R', offs)),
	('PMouth_L',			'PMouth_L', ('PMouth_L', offs)),
	('PTongue',			'PTongue', ('PTongue', offs)),
	('PJaw',			'PJaw', ('PJaw', offs)),

	('PArmIK_R',			'PArmIK_R', ('PArmIK_R', offs)),
	('PArmIK_L',			'PArmIK_L', ('PArmIK_L', offs)),
	('PLegIK_R',			'PLegIK_R', ('PLegIK_R', offs)),
	('PLegIK_L',			'PLegIK_L', ('PLegIK_L', offs)),

	('PFinger-1_L',			'PFinger-1_L', ('PFinger-1_L', offs)),
	('PFinger-2_L',			'PFinger-2_L', ('PFinger-2_L', offs)),
	('PFinger-3_L',			'PFinger-3_L', ('PFinger-3_L', offs)),
	('PFinger-4_L',			'PFinger-4_L', ('PFinger-4_L', offs)),
	('PFinger-5_L',			'PFinger-5_L', ('PFinger-5_L', offs)),

	('PFinger-1_R',			'PFinger-1_R', ('PFinger-1_R', offs)),
	('PFinger-2_R',			'PFinger-2_R', ('PFinger-2_R', offs)),
	('PFinger-3_R',			'PFinger-3_R', ('PFinger-3_R', offs)),
	('PFinger-4_R',			'PFinger-4_R', ('PFinger-4_R', offs)),
	('PFinger-5_R',			'PFinger-5_R', ('PFinger-5_R', offs)),

]


PanelArmature = [
	('PFace',		pi, None, F_WIR, L_PANEL, (1,1,1) ),
	('PFaceDisp',	pi, 'PFace', F_WIR+F_RES, L_PANEL, (1,1,1) ),
	('PBrow_R',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PBrow_L',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PBrows',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLid_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLid_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLid_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLid_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PCheek_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PCheek_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PNose',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PUpLip',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PLoLip',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	#('PMouth',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLip_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLip_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLip_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLip_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PMouth_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PMouth_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PTongue',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PJaw',		pi, 'PFace', 0, L_PANEL, (1,1,1) ),

	('PArmIK_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PArmIK_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLegIK_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLegIK_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),

	('PFinger-1_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PFinger-2_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PFinger-3_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PFinger-4_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PFinger-5_L',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),

	('PFinger-1_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PFinger-2_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PFinger-3_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PFinger-4_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PFinger-5_R',	pi, 'PFace', 0, L_PANEL, (1,1,1) ),
]

#
#	PanelWritePoses(fp):
#

#MX = 0.25
#K = 1.0/MX

MX = "0.25"
pos = ('0', '4.0')
neg = ('0', '-4.0')

FMX = 0.7

def PanelWritePoses(fp):
	addPoseBone(fp, 'PFace', 'MHCube05', None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0, 
		[('ChildOf', C_CHILDOF, 1, ['World', 'Root', (1,1,1), (1,1,1), (1,1,1)]) ])

	addPoseBone(fp, 'PFaceDisp', 'MHFace', None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addCSlider(fp, 'PBrow_L', MX)
	addCSlider(fp, 'PBrow_R', MX)
	addCSlider(fp, 'PBrows', MX)
	addCSlider(fp, 'PUpLid_L', MX)
	addCSlider(fp, 'PUpLid_R', MX)
	addCSlider(fp, 'PLoLid_L', MX)
	addCSlider(fp, 'PLoLid_R', MX)
	addCSlider(fp, 'PCheek_L', MX)
	addCSlider(fp, 'PCheek_R', MX)
	addCSlider(fp, 'PNose', MX)
	addCSlider(fp, 'PUpLip_L', MX)
	addCSlider(fp, 'PUpLip_R', MX)
	addCSlider(fp, 'PLoLip_L', MX)
	addCSlider(fp, 'PLoLip_R', MX)
	addCSlider(fp, 'PMouth_L', MX)
	addCSlider(fp, 'PMouth_R', MX)
	addCSlider(fp, 'PTongue', MX)
	addCSlider(fp, 'PJaw', MX)

	addXSlider(fp, 'PArmIK_L', 0.0, 1.0, 1.0)
	addXSlider(fp, 'PArmIK_R', 0.0, 1.0, 1.0)
	addXSlider(fp, 'PLegIK_L', 0.0, 1.0, 1.0)
	addXSlider(fp, 'PLegIK_R', 0.0, 1.0, 1.0)

	addXSlider(fp, 'PFinger-1_L', 0.0, FMX, FMX)
	addXSlider(fp, 'PFinger-2_L', 0.0, FMX, FMX)
	addXSlider(fp, 'PFinger-3_L', 0.0, FMX, FMX)
	addXSlider(fp, 'PFinger-4_L', 0.0, FMX, FMX)
	addXSlider(fp, 'PFinger-5_L', 0.0, FMX, FMX)

	addXSlider(fp, 'PFinger-1_R', 0.0, FMX, FMX)
	addXSlider(fp, 'PFinger-2_R', 0.0, FMX, FMX)
	addXSlider(fp, 'PFinger-3_R', 0.0, FMX, FMX)
	addXSlider(fp, 'PFinger-4_R', 0.0, FMX, FMX)
	addXSlider(fp, 'PFinger-5_R', 0.0, FMX, FMX)
	return

#
#	Face representation
#

FaceShapeDrivers = {
	# Brows
	'BrowsMidDown' : ('PBrows', 'LOC_Z', pos),
	'BrowsMidUp' : ('PBrows', 'LOC_Z', neg),
	'BrowsSqueeze' : ('PBrows', 'LOC_X', neg),
	'BrowsDown_L' : ('PBrow_L', 'LOC_Z', pos),
	'BrowsDown_R' : ('PBrow_R', 'LOC_Z', pos),
	'BrowsOutUp_L' : ('PBrow_L', 'LOC_Z', neg),
	'BrowsOutUp_R' : ('PBrow_R', 'LOC_Z', neg),

#	Lids
	#'UpLidDown_L' : ('PUpLid_L', 'LOC_Z', pos),
	#'UpLidDown_R' : ('PUpLid_R', 'LOC_Z', pos),
	#'LoLidUp_L' : ('PLoLid_L', 'LOC_Z', neg),
	#'LoLidUp_R' : ('PLoLid_R', 'LOC_Z', neg),

#	Nose and jaw

	'Sneer_L' : ('PNose', 'LOC_X', pos), 
	'Sneer_R' : ('PNose', 'LOC_X', neg), 
	'CheekUp_L' : ('PCheek_L', 'LOC_Z', neg),
	'CheekUp_R' : ('PCheek_R', 'LOC_Z', neg),
	'Squint_L' : ('PCheek_L', 'LOC_X', pos),
	'Squint_R' : ('PCheek_R', 'LOC_X', neg),

#	Jaw and tongue
	'MouthOpen' : ('PJaw', 'LOC_Z', pos),
	'TongueOut' : ('PJaw', 'LOC_X', neg),
	'TongueUp' : ('PTongue', 'LOC_Z', neg),
	'TongueLeft' : ('PTongue', 'LOC_X', pos),
	'TongueRight' : ('PTongue', 'LOC_X', neg),

#	Mouth expressions
	'Smile_L' : ('PMouth_L', 'LOC_X', pos),
	'Smile_R' : ('PMouth_R', 'LOC_X', neg),
	'Frown_L' : ('PMouth_L', 'LOC_Z', pos),
	'Frown_R' : ('PMouth_R', 'LOC_Z', pos), 
	'Narrow_L' : ('PMouth_L', 'LOC_X', neg), 
	'Narrow_R' : ('PMouth_R', 'LOC_X', pos),

#	Lips
	'UpLipUp_L' : ('PUpLip_L', 'LOC_Z', neg), 
	'UpLipUp_R' : ('PUpLip_R', 'LOC_Z', neg), 
	'UpLipDown_L' : ('PUpLip_L', 'LOC_Z', pos), 
	'UpLipDown_R' : ('PUpLip_R', 'LOC_Z', pos), 
	'LoLipUp_L' : ('PLoLip_L', 'LOC_Z', neg), 
	'LoLipUp_R' : ('PLoLip_R', 'LOC_Z', neg), 
	'LoLipDown_L' : ('PLoLip_L', 'LOC_Z', pos), 
	'LoLipDown_R' : ('PLoLip_R', 'LOC_Z', pos), 
}

#
#	FingerWriteDrivers(fp):
#

def FingerWriteDrivers(fp):
	drivers = []
	coeff = (0, 1.0/FMX)
	for suffix in ['_L', '_R']:
		for fnum in range(1,6):
			driver = "PFinger-%d%s" % (fnum, suffix)
			for lnum in range(1,4):
				driven = "Finger-%d-%d%s" % (fnum, lnum, suffix)
				cnsData = ("var", 'TRANSFORMS', [('Human', driver, 'LOC_X', C_LOCAL)])
				writeDriver(fp, True, 'AVERAGE', "", "pose.bones[\"%s\"].constraints[\"Rot\"].influence" % driven, -1, coeff, [cnsData])
	return

#
#	ArmShapeDrivers
#	Shape : (Driver, channel, (min, max))
#

ArmShapeDrivers = {
	'BendElbowForward_L' : ( -pi/2, 
		('PArmIK_L', 'LOC_X', pos), 
		('LoArmFK_L', 'ROT_Z', (0, deg90)), 
		('LoArmIK_L', 'ROT_Z', (0, deg90)) ),
	'BendArmUp_L' : ( pi/2, 
		('PArmIK_L', 'LOC_X', pos), 
		('UpArmFK_L', 'ROT_X', (0, deg90)), 
		('UpArmIK_L', 'ROT_X', (0, deg90)) ),
	'BendArmDown_L' : ( -pi/2, 
		('PArmIK_L', 'LOC_X', pos), 
		('UpArmFK_L', 'ROT_X', (-deg90, 0)), 
		('UpArmIK_L', 'ROT_X', (-deg90, 0)) ),

	'BendElbowForward_R' : ( pi/2, 
		('PArmIK_R', 'LOC_X', pos), 
		('LoArmFK_R', 'ROT_Z', (0, deg90)), 
		('LoArmIK_R', 'ROT_Z', (0, deg90)) ),
	'BendArmUp_R' : ( pi/2, 
		('PArmIK_R', 'LOC_X', pos), 
		('UpArmFK_R', 'ROT_X', (0, deg90)), 
		('UpArmIK_R', 'ROT_X', (0, deg90)) ),
	'BendArmDown_R' : ( -pi/2, 
		('PArmIK_R', 'LOC_X', pos), 
		('UpArmFK_R', 'ROT_X', (-deg90, 0)), 
		('UpArmIK_R', 'ROT_X', (-deg90, 0)) ),
}

#
#	LegShapeDrivers
#	Shape : (Driver, channel, (min, max))
#

LegShapeDrivers = {
	'BendKneeBack_L' : ( pi/2, 
		('PLegIK_L', 'LOC_X', pos), 
		('LoLegFK_L', 'ROT_X', (0, deg90)), 
		('LoLegIK_L', 'ROT_X', (0, deg90)) ),

	'BendKneeBack_R' : ( pi/2, 
		('PLegIK_R', 'LOC_X', pos), 
		('LoLegFK_R', 'ROT_X', (0, deg90)), 
		('LoLegIK_R', 'ROT_X', (0, deg90)) ),
}

"""
	'BendLegForward_L' : ( -pi/2, 
		('PLegIK_L', 'LOC_X', pos), 
		('UpLegFK_L', 'ROT_X', (0, deg90)), 
		('UpLegIK_L', 'ROT_X', (0, deg90)) ),
	'BendLegForward_R' : ( -pi/2, 
		('PLegIK_R', 'LOC_X', pos), 
		('UpLegFK_R', 'ROT_X', (0, deg90)), 
		('UpLegIK_R', 'ROT_X', (0, deg90)) ),
"""
