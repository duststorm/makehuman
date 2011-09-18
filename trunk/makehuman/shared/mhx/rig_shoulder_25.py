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
Shoulder 1 bone definitions 

"""

import mhx_rig
from mhx_rig import *

prcArmTrg    = 0.35

ShoulderJoints = [
    ('r-uparm-front',        'v', 3440),
    ('r-uparm-back',        'v', 3438),
    ('r-uparm-over',        'v', 3014),
    ('r-uparm-under',        'v', 3053),

    ('l-uparm-front',        'v', 10175),
    ('l-uparm-back',        'v', 10330),
    ('l-uparm-over',        'v', 10712),
    ('l-uparm-under',        'v', 10678),

    ('r-clavicle-back',        'v', 2583),
    ('r-clavicle-end',        'v', 2879),
    ('l-clavicle-back',        'v', 11025),
    ('l-clavicle-end',        'v', 10795),

    ('r-pectoralis',        'v', 3341),
    ('r-latdorsi',            'v', 4432),
    ('r-deltoid',            'v', 2854),
    ('r-armpit',            'v', 4431),

    ('l-pectoralis',        'v', 10410),
    ('l-latdorsi',            'v', 9995),
    ('l-deltoid'    ,        'v', 10820),
    ('l-armpit',            'v', 9996),

    ('r-trapezeus-1',        'v', 2584),
    ('r-trapezeus-2',        'v', 3633),
    ('l-trapezeus-1',        'v', 11024),
    ('l-trapezeus-2',        'v', 10159),

    ('r-shoulder-head',        'l', ((0.7, 'r-scapula'), (0.3, 'l-scapula'))),
    ('l-shoulder-head',        'l', ((0.3, 'r-scapula'), (0.7, 'l-scapula'))),

    ('r-shoulder-top',        'v', 2862),
    ('l-shoulder-top',        'v', 10812),
    ('r-shoulder-tail',        'l', ((0.5, 'r-shoulder-top'), (0.5, 'r-uparm0'))),
    ('l-shoulder-tail',        'l', ((0.5, 'l-shoulder-top'), (0.5, 'l-uparm0'))),

    ('sternum-tail',        'v', 7279),
    ('sternum-head',        'l', ((0.5, 'neck'), (0.5, 'sternum-tail'))),
    ('r-shoulder-aim',        'l', ((0.5, 'sternum-head'), (0.5, 'r-shoulder-tail'))),
    ('l-shoulder-aim',        'l', ((0.5, 'sternum-head'), (0.5, 'l-shoulder-tail'))),

    ('r-scapula-head',        'v', 2602),
    ('r-scapula-tail',        'v', 2584),
    ('l-scapula-head',        'v', 11008),
    ('l-scapula-tail',        'v', 11024),
]

ShoulderHeadsTails = [
    ('Sternum',                'neck', 'sternum-tail'),
    ('SternumTarget',        'sternum-head', 'sternum-tail'),
    
    # Shoulder
    ('Shoulder_L',            'r-clavicle', 'r-shoulder-tail'),
    ('ShoulderPivot_L',        'r-clavicle', 'r-shoulder-tail'),
    ('ShoulderUp_L',        ('r-shoulder-tail', yunit), ('r-shoulder-tail', ybis)),
    ('ShoulderAim_L',        'r-shoulder-tail', 'r-shoulder-aim'),
    ('DfmShoulder_L',        'r-clavicle', 'r-shoulder-tail'),
    ('DfmScapula_L',        'r-scapula-head', 'r-scapula-tail'),

    ('Shoulder_R',            'l-clavicle', 'l-shoulder-tail'),
    ('ShoulderPivot_R',        'l-clavicle', 'l-shoulder-tail'),
    ('ShoulderUp_R',        ('l-shoulder-tail', yunit), ('l-shoulder-tail', ybis)),
    ('ShoulderAim_R',        'l-shoulder-tail', 'l-shoulder-aim'),
    ('DfmShoulder_R',        'l-clavicle', 'l-shoulder-tail'),
    ('DfmScapula_R',        'l-scapula-head', 'l-scapula-tail'),

    ('DfmShoulderTwist_L',    'r-shoulder-aim', 'r-uparm1'),
    ('DfmShoulderTwist_R',    'l-shoulder-aim', 'l-uparm1'),

    # Shoulder deform
    ('DfmArmPit_L',            'r-armpit', 'r-armtrg'),
    ('DfmPectoralis_L',        'r-pectoralis', 'r-armtrg'),
    ('DfmTrapezeus_L',        'r-trapezeus-2', 'r-armtrg'),
    #('DfmLatDorsi_L',        'r-latdorsi', 'r-armtrg'),
    ('DfmDeltoid_L',        'r-deltoid', 'r-armtrg'),

    ('DfmArmPit_R',            'l-armpit', 'l-armtrg'),
    ('DfmPectoralis_R',        'l-pectoralis', 'l-armtrg'),
    ('DfmTrapezeus_R',        'l-trapezeus-2', 'l-armtrg'),
    #('DfmLatDorsi_R',        'l-latdorsi', 'l-armtrg'),
    ('DfmDeltoid_R',        'l-deltoid', 'l-armtrg'),

    # Rotation diffs
    ('BendArmDown_L',        'r-uparm0', ('r-uparm0', (0,-1,0))),
    ('BendArmDown_R',        'l-uparm0', ('l-uparm0', (0,-1,0))),
    ('BendArmUp_L',            'r-uparm0', ('r-uparm0', (0,1,0))),
    ('BendArmUp_R',            'l-uparm0', ('l-uparm0', (0,1,0))),
    ('BendArmForward_L',    'r-uparm0', ('r-uparm0', (0,0,1))),
    ('BendArmForward_R',    'l-uparm0', ('l-uparm0', (0,0,1))),
    ('BendArmBack_L',        'r-uparm0', ('r-uparm0', (0,0,-1))),
    ('BendArmBack_R',        'l-uparm0', ('l-uparm0', (0,0,-1))),
]

#upArmRoll = 1.69297
#loArmRoll = 90*D
#handRoll = 1.22173

upArmRoll = 0.0
loArmRoll = 0.0
handRoll = 0.0

L_LSHOULDER = L_LARMFK+L_LARMIK+L_UPSPNFK+L_UPSPNIK
L_RSHOULDER = L_RARMFK+L_RARMIK+L_UPSPNFK+L_UPSPNIK

ShoulderArmature = [
    ('Sternum',                0.0, 'Spine3', 0, L_HELP, NoBB),
    ('SternumTarget',        0.0, 'Sternum', 0, L_HELP, NoBB),

    # Shoulder
    ('Shoulder_L',            0.0, 'Sternum', F_WIR, L_LSHOULDER, NoBB),
    ('Shoulder_R',            0.0, 'Sternum', F_WIR, L_RSHOULDER, NoBB),

    # Rotation diffs
    ('BendArmDown_L',        90*D, 'Shoulder_L', 0, L_HELP, NoBB),
    ('BendArmDown_R',        -90*D, 'Shoulder_R', 0, L_HELP, NoBB),
    ('BendArmUp_L',            -90*D, 'Shoulder_L', 0, L_HELP, NoBB),
    ('BendArmUp_R',            90*D, 'Shoulder_R', 0, L_HELP, NoBB),
    ('BendArmForward_L',    0*D, 'Shoulder_L', 0, L_HELP, NoBB),
    ('BendArmForward_R',    0*D, 'Shoulder_R', 0, L_HELP, NoBB),
    ('BendArmBack_L',        0*D, 'Shoulder_L', 0, L_HELP, NoBB),
    ('BendArmBack_R',        0*D, 'Shoulder_R', 0, L_HELP, NoBB),

    # Shoulder
    ('ShoulderPivot_L',        0.0, 'Sternum', 0, L_HELP, NoBB),
    ('ShoulderUp_L',        0.0, 'ShoulderPivot_L', 0, L_HELP, NoBB),
    ('ShoulderAim_L',        0.0, 'ShoulderPivot_L', 0, L_HELP, NoBB),

    ('ShoulderPivot_R',        0.0, 'Sternum', 0, L_HELP, NoBB),
    ('ShoulderUp_R',        0.0, 'ShoulderPivot_R', 0, L_HELP, NoBB),
    ('ShoulderAim_R',        0.0, 'ShoulderPivot_R', 0, L_HELP, NoBB),

    ('DfmShoulder_L',        0.0, 'Sternum', F_DEF, L_DMAIN, NoBB),
    ('DfmScapula_L',        0.0, 'ShoulderAim_L', F_DEF, L_DMAIN, NoBB),
    ('DfmShoulderTwist_L',    0.0, 'ShoulderAim_L', 0, L_DEF, NoBB),

    ('DfmShoulder_R',        0.0, 'Sternum', F_DEF, L_DMAIN, NoBB),
    ('DfmScapula_R',        0.0, 'ShoulderAim_R', F_DEF, L_DMAIN, NoBB),
    ('DfmShoulderTwist_R',    0.0, 'ShoulderAim_R', 0, L_DEF, NoBB),

    # Shoulder deform
    ('DfmArmPit_L',            0.0, 'Spine3', F_DEF, L_DEF, NoBB),
    ('DfmPectoralis_L',        0.0, 'Spine3', F_DEF, L_DEF, NoBB),
    ('DfmTrapezeus_L',        0.0, 'Spine3', F_DEF, L_DEF, NoBB),
    #('DfmLatDorsi_L',        0.0, 'Spine1', F_DEF, L_DEF, NoBB),
    ('DfmDeltoid_L',        0.0, 'Spine3', F_DEF, L_DEF, NoBB),

    ('DfmArmPit_R',            0.0, 'Spine3', F_DEF, L_DEF, NoBB),
    ('DfmPectoralis_R',        0.0, 'Spine3', F_DEF, L_DEF, NoBB),
    ('DfmTrapezeus_R',        0.0, 'Spine3', F_DEF, L_DEF, NoBB),
    #('DfmLatDorsi_R',        0.0, 'Spine1', F_DEF, L_DEF, NoBB),
    ('DfmDeltoid_R',        0.0, 'Spine3', F_DEF, L_DEF, NoBB),

]

#
#
#

limShoulder_L = (-16*D,40*D, -40*D,40*D,  -45*D,45*D)
limShoulder_R = (-16*D,40*D,  -40*D,40*D,  -45*D,45*D)

#
#    Rotation modes
#    Dmod = Deform rig mode
#    Cmod = Control rig mode
#

#
#    ShoulderControlPoses(fp):
#

def ShoulderControlPoses(fp):
    addPoseBone(fp, 'Sternum', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'SternumTarget', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

    # Shoulder
    addPoseBone(fp, 'Shoulder_L', 'MHEndCube01', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_L, (True, True, True)])])

    addPoseBone(fp, 'Shoulder_R', 'MHEndCube01', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_R, (True, True, True)])])

    addPoseBone(fp, 'ArmLoc_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 1, ['Shoulder', 'ShoulderEnd_L', (1,1,1), (0,0,0), False]),
         ('CopyRot', 0, 0, ['Root', 'BendRoot', (1,1,1), (0,0,0), False])])

    addPoseBone(fp, 'ArmLoc_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 1, ['Shoulder', 'ShoulderEnd_R', (1,1,1), (0,0,0), False]),
         ('CopyRot', 0, 0, ['Root', 'BendRoot', (1,1,1), (0,0,0), False])])

    # Deform poses

    copyDeform(fp, 'DfmShoulder_L', 'Shoulder_L', 0, U_LOC+U_ROT, None, [])
    copyDeform(fp, 'DfmShoulder_R', 'Shoulder_R', 0, U_LOC+U_ROT, None, [])
    
    # Scapula    
    addPoseBone(fp, 'ShoulderPivot_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 0.5, ['Rot', 'Shoulder_L', (1,1,1), (0,0,0), False])])
    
    addPoseBone(fp, 'ShoulderUp_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
    
    addPoseBone(fp, 'ShoulderAim_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 1, ['IK', 'SternumTarget', 1, (90*D, 'ShoulderUp_L'), (True, False,True)])])
    
    addPoseBone(fp, 'DfmScapula_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
    
    
    addPoseBone(fp, 'ShoulderPivot_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 0.5, ['Rot', 'Shoulder_R', (1,1,1), (0,0,0), False])])
    
    addPoseBone(fp, 'ShoulderUp_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
    
    addPoseBone(fp, 'ShoulderAim_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 1, ['IK', 'SternumTarget', 1, (90*D, 'ShoulderUp_R'), (True, False,True)])])
    
    addPoseBone(fp, 'DfmScapula_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])


    addPoseBone(fp, 'DfmShoulderTwist_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 0.5, ['Rot', 'UpArm_L', (1,1,1), (0,0,0), False]),
         ('StretchTo', 0, 1, ['Stretch', 'UpArm2_L', 0])])

    addPoseBone(fp, 'DfmShoulderTwist_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 0.5, ['Rot', 'UpArm_R', (1,1,1), (0,0,0), False]),
         ('StretchTo', 0, 1, ['Stretch', 'UpArm2_R', 0])])    
    

    # Shoulder deform
    addPoseBone(fp, 'DfmArmPit_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
        [('StretchTo',0, 1, ['Stretch', 'ArmTrg_L', 1])])
    
    addPoseBone(fp, 'DfmPectoralis_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
        [('StretchTo', 0, 1, ['Forward', 'ArmTrg_L', 1])])
    
    addPoseBone(fp, 'DfmTrapezeus_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
        [('StretchTo',0, 1, ['Back', 'ArmTrg_L', 1])])
    
    addPoseBone(fp, 'DfmDeltoid_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
        [('StretchTo', C_PLANEZ, 1, ['Up', 'ArmTrg_L', 1])])
    

    addPoseBone(fp, 'DfmArmPit_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
        [('StretchTo', 0, 1, ['Stretch', 'ArmTrg_R', 1])])
    
    addPoseBone(fp, 'DfmPectoralis_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
        [('StretchTo', 0, 1, ['Forward', 'ArmTrg_R', 1])])
    
    addPoseBone(fp, 'DfmTrapezeus_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
        [('StretchTo', 0, 1, ['Back', 'ArmTrg_R', 1])])
    
    addPoseBone(fp, 'DfmDeltoid_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
        [('StretchTo', C_PLANEZ, 1, ['Up', 'ArmTrg_R', 1])])
    
    return
    
#
#    ShoulderDeformDrivers
#    (Bone, constraint, driver, rotdiff, keypoints)
#

ShoulderDeformDrivers = [
    ("DfmDeltoid_L", "Up", "min(u,2.7-d)", 
        [("u", "ArmTrg_L", "BendArmUp_L"), ("d", "ArmTrg_L", "BendArmDown_L")], 
        [(0,1), (40*D,1), (90*D,0)]),

    ("DfmPectoralis_L", "Forward", "f", 
         [("f", "ArmTrg_L", "BendArmForward_L")], [(0,1), (70*D,1), (90*D,1)]),

    ("DfmTrapezeus_L", "Back", "b", 
         [("b", "ArmTrg_L", "BendArmBack_L")], [(0,1), (50*D,1), (90*D,0.5)]),


    ("DfmDeltoid_R", "Up", "min(u,2.7-d)", 
        [("u", "ArmTrg_R", "BendArmUp_R"), ("d", "ArmTrg_R", "BendArmDown_R")], 
        [(0,1), (40*D,1), (90*D,0)]),

    ("DfmPectoralis_R", "Forward", "f", 
         [("f", "ArmTrg_R", "BendArmForward_R")], [(0,1), (70*D,1), (90*D,1)]),

    ("DfmTrapezeus_R", "Back", "b", 
         [("b", "ArmTrg_R", "BendArmBack_R")], [(0,1), (50*D,1), (90*D,0.5)]),

]


