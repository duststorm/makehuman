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
Panel bone definitions 

"""

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
	('PNose',		'o', ('origin', [0.0, 0.1, 0.0])),
	('PCheek_R',		'o', ('origin', [-0.4, 0.0, 0.0])),
	('PCheek_L',		'o', ('origin', [0.4, 0.0, 0.0])),
	('PUpLipMid',		'o', ('origin', [0.0, -0.2, 0.0])),
	('PLoLipMid',		'o', ('origin', [0.0, -0.8, 0.0])),
	('PMouthMid',		'o', ('origin', [0.0, -0.5, 0.0])),
	('PUpLip_R',		'o', ('origin', [-0.25, -0.3, 0.0])),
	('PUpLip_L',		'o', ('origin', [0.25, -0.3, 0.0])),
	('PLoLip_R',		'o', ('origin', [-0.25, -0.7, 0.0])),
	('PLoLip_L',		'o', ('origin', [0.25, -0.7, 0.0])),
	('PMouth_R',		'o', ('origin', [-0.5, -0.5, 0.0])),
	('PMouth_L',		'o', ('origin', [0.5, -0.5, 0.0])),
	('PTongue',		'o', ('origin', [0.45, -1.5, 0.0])),
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
	('PNose',			'PNose', ('PNose', offs)),
	('PUpLipMid',			'PUpLipMid', ('PUpLipMid', offs)),
	('PLoLipMid',			'PLoLipMid', ('PLoLipMid', offs)),
	('PMouthMid',			'PMouthMid', ('PMouthMid', offs)),
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
	('PFace',		pi, Master, F_WIR, L_PANEL, NoBB),
	('PFaceDisp',	pi, 'PFace', F_WIR+F_RES, L_PANEL, NoBB),
	('PBrow_R',		pi, 'PFace', 0, L_PANEL, NoBB),
	('PBrow_L',		pi, 'PFace', 0, L_PANEL, NoBB),
	('PBrows',		pi, 'PFace', 0, L_PANEL, NoBB),
	('PUpLid_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PUpLid_L',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PLoLid_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PLoLid_L',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PCheek_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PCheek_L',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PNose',		pi, 'PFace', 0, L_PANEL, NoBB),
	('PUpLipMid',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PLoLipMid',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PMouthMid',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PUpLip_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PUpLip_L',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PLoLip_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PLoLip_L',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PMouth_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PMouth_L',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PTongue',		pi, 'PFace', 0, L_PANEL, NoBB),
	('PJaw',		pi, 'PFace', 0, L_PANEL, NoBB),

	('PArmIK_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PArmIK_L',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PLegIK_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PLegIK_L',	pi, 'PFace', 0, L_PANEL, NoBB),

	('PFinger-1_L',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PFinger-2_L',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PFinger-3_L',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PFinger-4_L',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PFinger-5_L',	pi, 'PFace', 0, L_PANEL, NoBB),

	('PFinger-1_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PFinger-2_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PFinger-3_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PFinger-4_R',	pi, 'PFace', 0, L_PANEL, NoBB),
	('PFinger-5_R',	pi, 'PFace', 0, L_PANEL, NoBB),
]

#
#	PanelControlPoses(fp):
#

#MX = 0.25
#K = 1.0/MX

MX = "0.25"
pos = ('0', '4.0')
neg = ('0', '-4.0')

FMX = 0.7

def PanelControlPoses(fp):
	addPoseBone(fp, 'PFace', 'MHCube05', None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0, [])
		#[('ChildOf', C_CHILDOF, 1, ['Body', 'Root', (1,1,1), (1,1,1), (1,1,1)]) ])

	addPoseBone(fp, 'PFaceDisp', 'MHFace', None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addYSlider(fp, 'PBrow_L', MX)
	addYSlider(fp, 'PBrow_R', MX)
	addCSlider(fp, 'PBrows', MX)
	addYSlider(fp, 'PUpLid_L', MX)
	addYSlider(fp, 'PUpLid_R', MX)
	addYSlider(fp, 'PLoLid_L', MX)
	addYSlider(fp, 'PLoLid_R', MX)
	addCSlider(fp, 'PCheek_L', MX)
	addCSlider(fp, 'PCheek_R', MX)
	addCSlider(fp, 'PNose', MX)
	addCSlider(fp, 'PUpLipMid', MX)
	addCSlider(fp, 'PLoLipMid', MX)
	addYSlider(fp, 'PUpLip_L', MX)
	addYSlider(fp, 'PUpLip_R', MX)
	addYSlider(fp, 'PLoLip_L', MX)
	addYSlider(fp, 'PLoLip_R', MX)
	addCSlider(fp, 'PMouthMid', MX)
	addCSlider(fp, 'PMouth_L', MX)
	addCSlider(fp, 'PMouth_R', MX)
	addCSlider(fp, 'PTongue', MX)
	addYSlider(fp, 'PJaw', MX)

	addXSlider(fp, 'PArmIK_L', 0.0, 1.0, 0.0)
	addXSlider(fp, 'PArmIK_R', 0.0, 1.0, 0.0)
	addXSlider(fp, 'PLegIK_L', 0.0, 1.0, 0.0)
	addXSlider(fp, 'PLegIK_R', 0.0, 1.0, 0.0)

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

"""
	"MouthOpen" : ("Sym", -0.5, 2.0),
	"MouthCornerDepth" : ("LR", -0.5, 2.0),
	"LipsOut" : ("LRHJ", -0.5, 2.0),
	"LipsIn" : ("LRHJ", -0.5, 2.0),
	"MouthHeight" : ("LR", -0.5, 2.0),
	"LipsMidHeight" : ("HJ", -0.5, 2.0),
	"MouthCornerHeight" : ("LRHJ", -0.5, 2.0),
	"MouthWidth" : ("LR", 0, 2.0),
	"MouthNarrow" : ("Sym", 0, 2.0),
	"LipsPart" : ("Sym", -0.5, 2.0),
	"TongueHeight" : ("Sym", -0.5, 2.0),
	"TongueDepth" : ("Sym", -0.5, 2.0),
	"TongueWidth" : ("Sym", -0.5, 2.0),
	"TongueBackHeight" : ("Sym", -0.5, 2.0),
	"BrowsMidHeight" : ("Sym", 0, 2.0),
	"BrowsMidDown" : ("Sym", 0, 2.0),
	"BrowsSqueeze" : ("Sym", -0.5, 2.0),
	"BrowsOuterHeight" : ("LR", -0.5, 2.0),
	"NoseWrinkle" : ("Sym", -0.5, 2.0),
	"CheekFlex" : ("LR", -0.0, 2.0),
	"Squint" : ("LR", -0.5, 2.0),
	"CheekBalloon" : ("Sym", -1, 2.0),
"""

BodyLanguageShapeDrivers = {
	# Brows
	'BrowsMidHeight' : ('PBrows', 'LOC_Z', neg),
	'BrowsMidDown' : ('PBrows', 'LOC_Z', pos),
	'BrowsSqueeze' : ('PBrows', 'LOC_X', neg),
	'BrowsOuterHeight_L' : ('PBrow_L', 'LOC_Z', neg),
	'BrowsOuterHeight_R' : ('PBrow_R', 'LOC_Z', neg),

#	Nose and jaw

	'NoseWrinkle' : ('PNose', 'LOC_Z', neg), 
	'CheekBalloon' : ('PNose', 'LOC_X', pos), 
	'CheekFlex_L' : ('PCheek_L', 'LOC_Z', neg),
	'CheekFlex_R' : ('PCheek_R', 'LOC_Z', neg),
	'Squint_L' : ('PCheek_L', 'LOC_X', pos),
	'Squint_R' : ('PCheek_R', 'LOC_X', neg),

#	Jaw and tongue
	'MouthOpen' : ('PJaw', 'LOC_Z', pos),
	'TongueDepth' : ('PJaw', 'LOC_X', neg),
	'TongueHeight' : ('PTongue', 'LOC_Z', neg),
	'TongueWidth' : ('PTongue', 'LOC_X', pos),
	'TongueBackHeight' : ('PTongue', 'LOC_X', neg),

#	Mouth expressions
	'MouthWidth_L' : ('PMouth_L', 'LOC_X', pos),
	'MouthWidth_R' : ('PMouth_R', 'LOC_X', neg),
	'MouthCornerDepth_L' : ('PMouth_L', 'LOC_Z', neg),
	'MouthCornerDepth_R' : ('PMouth_R', 'LOC_Z', neg), 
	'MouthNarrow_L' : ('PMouth_L', 'LOC_X', neg), 
	'MouthNarrow_R' : ('PMouth_R', 'LOC_X', pos),

#	Lips part
	'LipsPart' : ('PMouthMid', 'LOC_Z', neg),

#
	'UpMouthCornerHeight_L' : ('PUpLip_L', 'LOC_Z', pos),
	'LoMouthCornerHeight_L' : ('PLoLip_L', 'LOC_Z', pos),
	'UpMouthCornerHeight_R' : ('PUpLip_R', 'LOC_Z', pos),
	'LoMouthCornerHeight_R' : ('PLoLip_R', 'LOC_Z', pos),

#	Lips in - out
	'UpLipsOut' : ('PUpLipMid', 'LOC_X', pos), 
	'UpLipsIn' : ('PUpLipMid', 'LOC_X', neg), 
	'LoLipsOut' : ('PLoLipMid', 'LOC_X', pos), 
	'LoLipsIn' : ('PLoLipMid', 'LOC_X', neg), 

#	Lips up - down
	'UpLipsMidHeight' : ('PUpLipMid', 'LOC_Z', neg), 
	'LoLipsMidHeight' : ('PLoLipMid', 'LOC_Z', neg), 

}

BodyLanguageTextureDrivers = {
	# Brows
	'browsMidDown' : (3, 'PBrows', 'LOC_Z', neg),
	'browsSqueeze' : (4, 'PBrows', 'LOC_X', neg),
	'squint_L' : (5, 'PCheek_L', 'LOC_X', pos),
	'squint_R' : (6, 'PCheek_R', 'LOC_X', neg),
}

#
#	FaceShapeKeyScale
#

eyeDist = 0.598002
mouthDist = 0.478831
tongueDist = 0.283124

FaceShapeKeyScale = {
	'BrowsDown'			: ('r-eye', 'l-eye', eyeDist),
	'BrowsMidDown'		: ('r-eye', 'l-eye', eyeDist),
	'BrowsMidUp'		: ('r-eye', 'l-eye', eyeDist),
	'BrowsOutUp'		: ('r-eye', 'l-eye', eyeDist),
	'BrowsSqueeze'		: ('r-eye', 'l-eye', eyeDist),
	'BrowsMidHeight'	: ('r-eye', 'l-eye', eyeDist),
	'BrowsOuterHeight'	: ('r-eye', 'l-eye', eyeDist),

	'NoseWrinkle'		: ('r-eye', 'l-eye', eyeDist),
	'Frown'				: ('r-mouth', 'l-mouth', mouthDist),
	'Squint'			: ('r-eye', 'l-eye', eyeDist),
	'CheekUp'			: ('r-mouth', 'l-mouth', mouthDist),
	'CheekFlex'			: ('r-mouth', 'l-mouth', mouthDist),
	'CheekBalloon'		: ('r-mouth', 'l-mouth', mouthDist),

	'UpLipUp'			: ('r-mouth', 'l-mouth', mouthDist),
	'LoLipDown'			: ('r-mouth', 'l-mouth', mouthDist),
	'UpLipsOut'			: ('r-mouth', 'l-mouth', mouthDist),
	'LoLipsOut'			: ('r-mouth', 'l-mouth', mouthDist),
	'UpLipsIn'			: ('r-mouth', 'l-mouth', mouthDist),
	'LoLipsIn'			: ('r-mouth', 'l-mouth', mouthDist),
	'UpLipDown'			: ('r-mouth', 'l-mouth', mouthDist),
	'LoLipUp'			: ('r-mouth', 'l-mouth', mouthDist),
	'UpLipsMidHeight'	: ('r-mouth', 'l-mouth', mouthDist),
	'LoLipsMidHeight'	: ('r-mouth', 'l-mouth', mouthDist),
	'LipsPart'			: ('r-mouth', 'l-mouth', mouthDist),

	'MouthOpen'			: ('r-mouth', 'l-mouth', mouthDist),
	'MouthCornerDepth'	: ('r-mouth', 'l-mouth', mouthDist),
	'MouthHeight'		: ('r-mouth', 'l-mouth', mouthDist),
	'UpMouthCornerHeight'	: ('r-mouth', 'l-mouth', mouthDist),
	'LoMouthCornerHeight'	: ('r-mouth', 'l-mouth', mouthDist),
	'MouthWidth'		: ('r-mouth', 'l-mouth', mouthDist),
	'MouthNarrow'		: ('r-mouth', 'l-mouth', mouthDist),

	'Narrow'			: ('r-mouth', 'l-mouth', mouthDist),
	'Smile'				: ('r-mouth', 'l-mouth', mouthDist),
	'Sneer'				: ('r-mouth', 'l-mouth', mouthDist),

	'TongueOut'			: ('tongue-1', 'tongue-2', tongueDist),
	'TongueUp'			: ('tongue-1', 'tongue-2', tongueDist),
	'TongueLeft'		: ('tongue-1', 'tongue-2', tongueDist),
	'TongueRight'		: ('tongue-1', 'tongue-2', tongueDist),
	'TongueHeight'		: ('tongue-1', 'tongue-2', tongueDist),
	'TongueDepth'		: ('tongue-1', 'tongue-2', tongueDist),
	'TongueWidth'		: ('tongue-1', 'tongue-2', tongueDist),
	'TongueBackHeight'	: ('tongue-1', 'tongue-2', tongueDist),

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
			if fnum == 1:
				first = 2
			else:
				first = 1
			for lnum in range(first,4):
				driven = "Finger-%d-%d%s" % (fnum, lnum, suffix)
				cnsData = ("var", 'TRANSFORMS', [(mh2mhx.theHuman, driver, 'LOC_X', C_LOC)])
				writeDriver(fp, True, 'AVERAGE', "", "pose.bones[\"%s\"].constraints[\"Rot\"].influence" % driven, -1, coeff, [cnsData])
	return

