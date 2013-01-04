#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Panel bone definitions 
"""

from . import the
from the import *
from . import posebone
from posebone import addPoseBone, addYSlider, addCSlider

offs = [0, 0, 0.3]

PanelJoints = [
    ('origin',      'o', ('head', [-3.3, 0.5, 0.0])),
    ('PFace',       'o', ('origin', [0.0, -1.5, 0.0])),
    ('PBrow_R',     'o', ('origin', [-0.4, 0.8, 0.0])),
    ('PBrow_L',     'o', ('origin', [0.4, 0.8, 0.0])),
    ('PBrows',      'o', ('origin', [0.0, 0.8, 0.0])),
    ('PUpLid_R',        'o', ('origin', [-0.4, 0.6, 0.0])),
    ('PUpLid_L',        'o', ('origin', [0.4, 0.6, 0.0])),
    ('PLoLid_R',        'o', ('origin', [-0.4, 0.2, 0.0])),
    ('PLoLid_L',        'o', ('origin', [0.4, 0.2, 0.0])),
    ('PNose',       'o', ('origin', [0.0, 0.1, 0.0])),
    ('PCheek_R',        'o', ('origin', [-0.4, 0.0, 0.0])),
    ('PCheek_L',        'o', ('origin', [0.4, 0.0, 0.0])),
    ('PUpLipMid',       'o', ('origin', [0.0, -0.2, 0.0])),
    ('PLoLipMid',       'o', ('origin', [0.0, -0.8, 0.0])),
    ('PMouthMid',       'o', ('origin', [0.0, -0.5, 0.0])),
    ('PUpLip_R',        'o', ('origin', [-0.25, -0.3, 0.0])),
    ('PUpLip_L',        'o', ('origin', [0.25, -0.3, 0.0])),
    ('PLoLip_R',        'o', ('origin', [-0.25, -0.7, 0.0])),
    ('PLoLip_L',        'o', ('origin', [0.25, -0.7, 0.0])),
    ('PMouth_R',        'o', ('origin', [-0.5, -0.5, 0.0])),
    ('PMouth_L',        'o', ('origin', [0.5, -0.5, 0.0])),
    ('PTongue',     'o', ('origin', [0.45, -1.5, 0.0])),
    ('PJaw',        'o', ('origin', [0.0, -1.1, 0.0])),
]    

PanelHeadsTails = [
    ('PFace',           'PFace', ('PFace', [0,0,-1])),
    ('PFaceDisp',           'origin', ('origin', [0,0,-1])),
    ('PBrow_R',         'PBrow_R', ('PBrow_R', offs)),
    ('PBrow_L',         'PBrow_L', ('PBrow_L', offs)),
    ('PBrows',          'PBrows', ('PBrows', offs)),
    ('PUpLid_R',            'PUpLid_R', ('PUpLid_R', offs)),
    ('PUpLid_L',            'PUpLid_L', ('PUpLid_L', offs)),
    ('PLoLid_R',            'PLoLid_R', ('PLoLid_R', offs)),
    ('PLoLid_L',            'PLoLid_L', ('PLoLid_L', offs)),
    ('PCheek_R',            'PCheek_R', ('PCheek_R', offs)),
    ('PCheek_L',            'PCheek_L', ('PCheek_L', offs)),
    ('PNose',           'PNose', ('PNose', offs)),
    ('PUpLipMid',           'PUpLipMid', ('PUpLipMid', offs)),
    ('PLoLipMid',           'PLoLipMid', ('PLoLipMid', offs)),
    ('PMouthMid',           'PMouthMid', ('PMouthMid', offs)),
    ('PUpLip_R',            'PUpLip_R', ('PUpLip_R', offs)),
    ('PUpLip_L',            'PUpLip_L', ('PUpLip_L', offs)),
    ('PLoLip_R',            'PLoLip_R', ('PLoLip_R', offs)),
    ('PLoLip_L',            'PLoLip_L', ('PLoLip_L', offs)),
    ('PMouth_R',            'PMouth_R', ('PMouth_R', offs)),
    ('PMouth_L',            'PMouth_L', ('PMouth_L', offs)),
    ('PTongue',         'PTongue', ('PTongue', offs)),
    ('PJaw',            'PJaw', ('PJaw', offs)),
]

PanelArmature = [
    ('PFace',       pi, None, F_WIR, L_PANEL, NoBB),
    ('PFaceDisp',   pi, 'PFace', F_WIR+F_RES, L_PANEL, NoBB),
    ('PBrow_R',     pi, 'PFace', 0, L_PANEL, NoBB),
    ('PBrow_L',     pi, 'PFace', 0, L_PANEL, NoBB),
    ('PBrows',      pi, 'PFace', 0, L_PANEL, NoBB),
    ('PUpLid_R',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PUpLid_L',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PLoLid_R',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PLoLid_L',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PCheek_R',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PCheek_L',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PNose',       pi, 'PFace', 0, L_PANEL, NoBB),
    ('PUpLipMid',   pi, 'PFace', 0, L_PANEL, NoBB),
    ('PLoLipMid',   pi, 'PFace', 0, L_PANEL, NoBB),
    ('PMouthMid',   pi, 'PFace', 0, L_PANEL, NoBB),
    ('PUpLip_R',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PUpLip_L',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PLoLip_R',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PLoLip_L',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PMouth_R',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PMouth_L',    pi, 'PFace', 0, L_PANEL, NoBB),
    ('PTongue',     pi, 'PFace', 0, L_PANEL, NoBB),
    ('PJaw',        pi, 'PFace', 0, L_PANEL, NoBB),
]

#
#   PanelControlPoses(fp, config):
#

#MX = 0.25
#K = 1.0/MX

MX = "0.25"
pos = ('0', '4.0')
neg = ('0', '-4.0')

FMX = 0.7

def PanelControlPoses(fp, config):
    if config.exporting:
        addPoseBone(fp, config, 'PFace', 'MHCube05', None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0, [])
            #[('ChildOf', C_CHILDOF, 1, ['Body', 'Root', (1,1,1), (1,1,1), (1,1,1)]) ])

        addPoseBone(fp, config, 'PFaceDisp', 'MHFace', None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])

        addYSlider(fp, config, 'PBrow_L', MX)
        addYSlider(fp, config, 'PBrow_R', MX)
        addCSlider(fp, config, 'PBrows', MX)
        addYSlider(fp, config, 'PUpLid_L', MX)
        addYSlider(fp, config, 'PUpLid_R', MX)
        addYSlider(fp, config, 'PLoLid_L', MX)
        addYSlider(fp, config, 'PLoLid_R', MX)
        addCSlider(fp, config, 'PCheek_L', MX)
        addCSlider(fp, config, 'PCheek_R', MX)
        addCSlider(fp, config, 'PNose', MX)
        addCSlider(fp, config, 'PUpLipMid', MX)
        addCSlider(fp, config, 'PLoLipMid', MX)
        addYSlider(fp, config, 'PUpLip_L', MX)
        addYSlider(fp, config, 'PUpLip_R', MX)
        addYSlider(fp, config, 'PLoLip_L', MX)
        addYSlider(fp, config, 'PLoLip_R', MX)
        addCSlider(fp, config, 'PMouthMid', MX)
        addCSlider(fp, config, 'PMouth_L', MX)
        addCSlider(fp, config, 'PMouth_R', MX)
        addCSlider(fp, config, 'PTongue', MX)
        addYSlider(fp, config, 'PJaw', MX)


#
#   Face representation
#
"""
FaceShapeDrivers = {
    # Brows
    'BrowsMidDown' : ('PBrows', 'LOC_Z', pos),
    'BrowsMidUp' : ('PBrows', 'LOC_Z', neg),
    'BrowsSqueeze' : ('PBrows', 'LOC_X', neg),
    'BrowsDown_L' : ('PBrow_L', 'LOC_Z', pos),
    'BrowsDown_R' : ('PBrow_R', 'LOC_Z', pos),
    'BrowsOutUp_L' : ('PBrow_L', 'LOC_Z', neg),
    'BrowsOutUp_R' : ('PBrow_R', 'LOC_Z', neg),

#   Lids
    #'UpLidDown_L' : ('PUpLid_L', 'LOC_Z', pos),
    #'UpLidDown_R' : ('PUpLid_R', 'LOC_Z', pos),
    #'LoLidUp_L' : ('PLoLid_L', 'LOC_Z', neg),
    #'LoLidUp_R' : ('PLoLid_R', 'LOC_Z', neg),

#   Nose and jaw

    'Sneer_L' : ('PNose', 'LOC_X', pos), 
    'Sneer_R' : ('PNose', 'LOC_X', neg), 
    'CheekUp_L' : ('PCheek_L', 'LOC_Z', neg),
    'CheekUp_R' : ('PCheek_R', 'LOC_Z', neg),
    'Squint_L' : ('PCheek_L', 'LOC_X', pos),
    'Squint_R' : ('PCheek_R', 'LOC_X', neg),

#   Jaw and tongue
    'MouthOpen' : ('PJaw', 'LOC_Z', pos),
    'TongueOut' : ('PJaw', 'LOC_X', neg),
    'TongueUp' : ('PTongue', 'LOC_Z', neg),
    'TongueLeft' : ('PTongue', 'LOC_X', pos),
    'TongueRight' : ('PTongue', 'LOC_X', neg),

#   Mouth expressions
    'Smile_L' : ('PMouth_L', 'LOC_X', pos),
    'Smile_R' : ('PMouth_R', 'LOC_X', neg),
    'Frown_L' : ('PMouth_L', 'LOC_Z', pos),
    'Frown_R' : ('PMouth_R', 'LOC_Z', pos), 
    'Narrow_L' : ('PMouth_L', 'LOC_X', neg), 
    'Narrow_R' : ('PMouth_R', 'LOC_X', pos),

#   Lips
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

BodyLanguageShapeDrivers = {
    # Brows
    'BrowsMidHeight' : ('brows_mid_height', 'PBrows', 'LOC_Z', neg, 0, 1),
    'BrowsMidDown' : ('brows_mid_down', 'PBrows', 'LOC_Z', pos, 0, 1),
    'BrowsSqueeze' : ('brows_squeeze', 'PBrows', 'LOC_X', neg, 0, 2),
    'BrowsOuterHeight_L' : ('brows_outer_height', 'PBrow_L', 'LOC_Z', neg, -1, 2),
    'BrowsOuterHeight_R' : ('brows_outer_height', 'PBrow_R', 'LOC_Z', neg, -1, 2),

#   Nose and jaw

    'NoseWrinkle' : ('nose_wrinkle', 'PNose', 'LOC_Z', neg, 0, 2), 
    'CheekBalloon' : ('cheek_balloon', 'PNose', 'LOC_X', pos, -1, 2), 
    'CheekFlex_L' : ('cheek_flex', 'PCheek_L', 'LOC_Z', neg, 0, 2),
    'CheekFlex_R' : ('cheek_flex', 'PCheek_R', 'LOC_Z', neg, 0, 2),
    'Squint_L' : ('squint', 'PCheek_L', 'LOC_X', pos, 0, 2),
    'Squint_R' : ('squint', 'PCheek_R', 'LOC_X', neg, 0, 2),

#   Jaw and tongue
    'MouthOpen' : ('mouth_open', 'PJaw', 'LOC_Z', pos, 0, 2),
    'TongueDepth' : ('tongue_depth', 'PJaw', 'LOC_X', neg, 0, 2),
    'TongueHeight' : ('tongue_height', 'PTongue', 'LOC_Z', neg, 0, 2),
    'TongueWidth' : ('tongue_width', 'PTongue', 'LOC_X', pos, 0, 1),
    'TongueBackHeight' : ('tongue_back_height', 'PTongue', 'LOC_X', neg, 0, 1),

#   Mouth expressions
    'MouthWidth_L' : ('mouth_width', 'PMouth_L', 'LOC_X', pos, 0, 1),
    'MouthWidth_R' : ('mouth_width', 'PMouth_R', 'LOC_X', neg, 0, 1),
    'MouthCornerDepth_L' : ('mouth_corner_depth', 'PMouth_L', 'LOC_Z', neg, -1, 2),
    'MouthCornerDepth_R' : ('mouth_corner_depth', 'PMouth_R', 'LOC_Z', neg, -1, 2), 
    'MouthNarrow_L' : ('mouth_narrow', 'PMouth_L', 'LOC_X', neg, 0, 1), 
    'MouthNarrow_R' : ('mouth_narrow', 'PMouth_R', 'LOC_X', pos, 0, 1),

#   Lips part
    'LipsPart' : ('lips_part', 'PMouthMid', 'LOC_Z', neg, -1, 2),
    'MouthHeight_L' : ('mouth_height', 'PMouthMid', 'LOC_X', pos, -1, 2),
    'MouthHeight_R' : ('mouth_height', 'PMouthMid', 'LOC_X', neg, -1, 2),

#
    'UpMouthCornerHeight_L' : ('upper_mouth_corner_height', 'PUpLip_L', 'LOC_Z', pos, -1, 2),
    'LoMouthCornerHeight_L' : ('lower_mouth_corner_height', 'PLoLip_L', 'LOC_Z', pos, -1, 2),
    'UpMouthCornerHeight_R' : ('upper_mouth_corner_height', 'PUpLip_R', 'LOC_Z', pos, -1, 2),
    'LoMouthCornerHeight_R' : ('lower_mouth_corner_height', 'PLoLip_R', 'LOC_Z', pos, -1, 2),

#   Lips in - out
    'UpLipsOut' : ('upper_lips_out', 'PUpLipMid', 'LOC_X', pos, 0, 2), 
    'UpLipsIn' : ('upper_lips_in', 'PUpLipMid', 'LOC_X', neg, 0, 2), 
    'LoLipsOut' : ('lower_lips_out', 'PLoLipMid', 'LOC_X', pos, 0, 2), 
    'LoLipsIn' : ('lower_lips_in', 'PLoLipMid', 'LOC_X', neg, 0, 2), 

#   Lips up - down
    'UpLipsMidHeight' : ('upper_lips_mid_height', 'PUpLipMid', 'LOC_Z', neg, -1, 2), 
    'LoLipsMidHeight' : ('lower_lips_mid_height', 'PLoLipMid', 'LOC_Z', neg, -1, 2), 

}

BodyLanguageTextureDrivers = {
    # Brows
    'browsMidDown' : (3, 'PBrows', 'LOC_Z', neg),
    'browsSqueeze' : (4, 'PBrows', 'LOC_X', neg),
    'squint_L' : (5, 'PCheek_L', 'LOC_X', pos),
    'squint_R' : (6, 'PCheek_R', 'LOC_X', neg),
}

"""
#
#   FaceShapeKeyScale
#

eyeDist = 0.598002
mouthDist = 0.478831
tongueDist = 0.283124

FaceShapeKeyScale = {
    'BrowsDown'         : ('r-eye', 'l-eye', eyeDist),
    'BrowsMidDown'      : ('r-eye', 'l-eye', eyeDist),
    'BrowsMidUp'        : ('r-eye', 'l-eye', eyeDist),
    'BrowsOutUp'        : ('r-eye', 'l-eye', eyeDist),
    'BrowsSqueeze'      : ('r-eye', 'l-eye', eyeDist),
    'BrowsMidHeight'    : ('r-eye', 'l-eye', eyeDist),
    'BrowsOuterHeight'  : ('r-eye', 'l-eye', eyeDist),

    'NoseWrinkle'       : ('r-eye', 'l-eye', eyeDist),
    'Frown'             : ('r-mouth', 'l-mouth', mouthDist),
    'Squint'            : ('r-eye', 'l-eye', eyeDist),
    'CheekUp'           : ('r-mouth', 'l-mouth', mouthDist),
    'CheekFlex'         : ('r-mouth', 'l-mouth', mouthDist),
    'CheekBalloon'      : ('r-mouth', 'l-mouth', mouthDist),

    'UpLipUp'           : ('r-mouth', 'l-mouth', mouthDist),
    'LoLipDown'         : ('r-mouth', 'l-mouth', mouthDist),
    'UpLipsOut'         : ('r-mouth', 'l-mouth', mouthDist),
    'LoLipsOut'         : ('r-mouth', 'l-mouth', mouthDist),
    'UpLipsIn'          : ('r-mouth', 'l-mouth', mouthDist),
    'LoLipsIn'          : ('r-mouth', 'l-mouth', mouthDist),
    'UpLipDown'         : ('r-mouth', 'l-mouth', mouthDist),
    'LoLipUp'           : ('r-mouth', 'l-mouth', mouthDist),
    'UpLipsMidHeight'   : ('r-mouth', 'l-mouth', mouthDist),
    'LoLipsMidHeight'   : ('r-mouth', 'l-mouth', mouthDist),
    'LipsPart'          : ('r-mouth', 'l-mouth', mouthDist),

    'MouthOpen'         : ('r-mouth', 'l-mouth', mouthDist),
    'MouthCornerDepth'  : ('r-mouth', 'l-mouth', mouthDist),
    'MouthHeight'       : ('r-mouth', 'l-mouth', mouthDist),
    'UpMouthCornerHeight'   : ('r-mouth', 'l-mouth', mouthDist),
    'LoMouthCornerHeight'   : ('r-mouth', 'l-mouth', mouthDist),
    'MouthWidth'        : ('r-mouth', 'l-mouth', mouthDist),
    'MouthNarrow'       : ('r-mouth', 'l-mouth', mouthDist),

    'Narrow'            : ('r-mouth', 'l-mouth', mouthDist),
    'Smile'             : ('r-mouth', 'l-mouth', mouthDist),
    'Sneer'             : ('r-mouth', 'l-mouth', mouthDist),

    'TongueOut'         : ('tongue-1', 'tongue-2', tongueDist),
    'TongueUp'          : ('tongue-1', 'tongue-2', tongueDist),
    'TongueLeft'        : ('tongue-1', 'tongue-2', tongueDist),
    'TongueRight'       : ('tongue-1', 'tongue-2', tongueDist),
    'TongueHeight'      : ('tongue-1', 'tongue-2', tongueDist),
    'TongueDepth'       : ('tongue-1', 'tongue-2', tongueDist),
    'TongueWidth'       : ('tongue-1', 'tongue-2', tongueDist),
    'TongueBackHeight'  : ('tongue-1', 'tongue-2', tongueDist),

}

"""
