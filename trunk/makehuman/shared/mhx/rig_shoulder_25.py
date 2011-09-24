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
Arm bone definitions 

"""

import mhx_rig
from mhx_rig import *

ShoulderJoints = [
    #('r-deltoidtrg',        'vl', ((0.5, 3617), (0.5, 3625))),
    #('l-deltoidtrg',        'vl', ((0.5, 10167), (0.5, 10175))),
    ('r-deltoidtrg',        'l', ((0.5, 'r-uparm0'), (0.5, 'r-elbow'))),
    ('l-deltoidtrg',        'l', ((0.5, 'l-uparm0'), (0.5, 'l-elbow'))),
    ('r-deltoid',           'vl', ((0.5, 2914), (0.5, 3067))),
    ('l-deltoid',           'vl', ((0.5, 10671), (0.5, 10787))),

    ('r-pect1',             'v', 2909),
    ('l-pect1',             'v', 10792),
    ('r-pect2',             'v', 3535),
    ('l-pect2',             'v', 10257),

    ('r-trap1',             'v', 3417),
    ('l-trap1',             'v', 10347),
    ('r-trap2',             'v', 2614),
    ('l-trap2',             'v', 10996),

    ('r-lattrg',            'v', 3424),
    ('l-lattrg',            'v', 10344),
    ('r-lat',               'v', 4430),
    ('l-lat',               'v', 9997),
    
    ('r-clav-head',         'l', ((0.7, 'r-scapula'), (0.3, 'l-scapula'))),
    ('l-clav-head',         'l', ((0.3, 'r-scapula'), (0.7, 'l-scapula'))),

    ('r-clav-top',          'v', 2862),
    ('l-clav-top',          'v', 10812),
    ('r-clav-tail',         'l', ((0.5, 'r-clav-top'), (0.5, 'r-uparm0'))),
    ('l-clav-tail',         'l', ((0.5, 'l-clav-top'), (0.5, 'l-uparm0'))),

    ('sternum-tail',        'v', 7279),
    ('sternum-head',        'l', ((0.5, 'neck'), (0.5, 'sternum-tail'))),
    ('r-clav-aim',          'l', ((0.5, 'sternum-head'), (0.5, 'r-clav-tail'))),
    ('l-clav-aim',          'l', ((0.5, 'sternum-head'), (0.5, 'l-clav-tail'))),
    
    ('r-scapula1-head',     'vl', ((0.9, 3044), (0.1, 4444))),
    ('r-scapula1-tail',     'v', 2584),
    ('r-scapula2-head',     'l', ((0.5, 'r-scapula1-head'), (0.5, 'r-scapula1-tail'))),
    ('r-scapula2-tail',     'v', 2607),
    ('l-scapula1-head',     'vl', ((0.9, 10687), (0.1, 9983))),
    ('l-scapula1-tail',     'v', 11024),
    ('l-scapula2-head',     'l', ((0.5, 'l-scapula1-head'), (0.5, 'l-scapula1-tail'))),
    ('l-scapula2-tail',     'v', 11003),
]

ShoulderHeadsTails = [
    ('Sternum',             'neck', 'sternum-tail'),
    ('SternumTarget',       'sternum-head', 'sternum-tail'),
    
    # Clavicle

    ('Clavicle_L',          'r-clavicle', 'r-clav-tail'),
    ('ShoulderPivot_L',     'r-clavicle', 'r-clav-tail'),
    ('ShoulderUp_L',        ('r-clav-tail', yunit), ('r-clav-tail', ybis)),
    ('ShoulderAim_L',       'r-clav-tail', 'r-clav-aim'),
    ('DfmClavicle_L',       'r-clavicle', 'r-clav-tail'),

    ('Clavicle_R',          'l-clavicle', 'l-clav-tail'),
    ('ShoulderPivot_R',     'l-clavicle', 'l-clav-tail'),
    ('ShoulderUp_R',        ('l-clav-tail', yunit), ('l-clav-tail', ybis)),
    ('ShoulderAim_R',       'l-clav-tail', 'l-clav-aim'),
    ('DfmClavicle_R',       'l-clavicle', 'l-clav-tail'),

    # Shoulder
    ('ShoulderEnd_L',       'r-uparm0', ('r-uparm0', yunit)),
    ('ShoulderEnd_R',       'l-uparm0', ('l-uparm0', yunit)),
    ('Shoulder_L',          'r-uparm0', ('r-uparm0', yunit)),
    ('Shoulder_R',          'l-uparm0', ('l-uparm0', yunit)),
    ('ArmLoc_L',            'r-uparm0', ('r-uparm0', yunit)),
    ('ArmLoc_R',            'l-uparm0', ('l-uparm0', yunit)),

    # Scapula
    
    ('DfmScapula_L',        'r-scapula2-head', 'r-scapula2-tail'),
    ('DfmScapula_R',        'l-scapula2-head', 'l-scapula2-tail'),

    # Muscles
    
    ('DeltoidTrg2_L',        'r-deltoidtrg', ('r-deltoidtrg', yunit)),
    ('DeltoidTrg2_R',        'l-deltoidtrg', ('l-deltoidtrg', yunit)),
    ('Deltoid_L',            'r-deltoidtrg', ('r-deltoidtrg', yunit)),
    ('Deltoid_R',            'l-deltoidtrg', ('l-deltoidtrg', yunit)),
    ('DfmDeltoid_L',         'r-deltoid', 'r-deltoidtrg'),
    ('DfmDeltoid_R',         'l-deltoid', 'l-deltoidtrg'),

    ('DfmPect1_L',           'r-pect1', 'r-armtrg'),
    ('DfmPect1_R',           'l-pect1', 'l-armtrg'),
    ('DfmPect2_L',           'r-pect2', 'r-armtrg'),
    ('DfmPect2_R',           'l-pect2', 'l-armtrg'),

    ('DfmTrap1_L',           'r-trap1', 'r-armtrg'),
    ('DfmTrap1_R',           'l-trap1', 'l-armtrg'),
    ('DfmTrap2_L',           'r-trap2', 'r-armtrg'),
    ('DfmTrap2_R',           'l-trap2', 'l-armtrg'),

    ('DfmLat_L',             'r-lat', 'r-armtrg'),
    ('DfmLat_R',             'l-lat', 'l-armtrg'),
    
    # Rotation diffs
    ('BendArmDown_L',        'r-uparm0', ('r-uparm0', (0,-1,0))),
    ('BendArmDown_R',        'l-uparm0', ('l-uparm0', (0,-1,0))),
    ('BendArmUp_L',          'r-uparm0', ('r-uparm0', (0,1,0))),
    ('BendArmUp_R',          'l-uparm0', ('l-uparm0', (0,1,0))),
    ('BendArmForward_L',     'r-uparm0', ('r-uparm0', (0,0,1))),
    ('BendArmForward_R',     'l-uparm0', ('l-uparm0', (0,0,1))),
    ('BendArmBack_L',        'r-uparm0', ('r-uparm0', (0,0,-1))),
    ('BendArmBack_R',        'l-uparm0', ('l-uparm0', (0,0,-1))),
]

L_LSHOULDER = L_LARMFK+L_LARMIK+L_UPSPNFK+L_UPSPNIK
L_RSHOULDER = L_RARMFK+L_RARMIK+L_UPSPNFK+L_UPSPNIK

ShoulderArmature = [
    ('Sternum',            0, 'DfmSpine3', 0, L_HELP, NoBB),
    ('SternumTarget',      0, 'Sternum', 0, L_HELP, NoBB),

    # Clavicle
    ('Clavicle_L',         0, 'Sternum', F_WIR, L_LSHOULDER, NoBB),
    ('Clavicle_R',         0, 'Sternum', F_WIR, L_RSHOULDER, NoBB),
    ('DfmClavicle_L',      0, 'Sternum', F_DEF, L_DMAIN, NoBB),
    ('DfmClavicle_R',      0, 'Sternum', F_DEF, L_DMAIN, NoBB),
    
    # Shoulder    
    ('ShoulderEnd_L',      0, 'Clavicle_L', 0, L_HELP, NoBB),
    ('ShoulderEnd_R',      0, 'Clavicle_R', 0, L_HELP, NoBB),
    ('Shoulder_L',         0, 'ShoulderEnd_L', F_WIR+F_NOROT, L_LARMFK+L_LARMIK, NoBB),
    ('Shoulder_R',         0, 'ShoulderEnd_R', F_WIR+F_NOROT, L_RARMFK+L_RARMIK, NoBB),
    ('ArmLoc_L',           0, None, 0, L_HELP, NoBB),
    ('ArmLoc_R',           0, None, 0, L_HELP, NoBB),

    # Scapula
    ('ShoulderPivot_L',    0, 'Sternum', 0, L_HELP, NoBB),
    ('ShoulderUp_L',       0, 'ShoulderPivot_L', 0, L_HELP, NoBB),
    ('ShoulderAim_L',      0, 'ShoulderPivot_L', 0, L_HELP, NoBB),

    ('ShoulderPivot_R',    0, 'Sternum', 0, L_HELP, NoBB),
    ('ShoulderUp_R',       0, 'ShoulderPivot_R', 0, L_HELP, NoBB),
    ('ShoulderAim_R',      0, 'ShoulderPivot_R', 0, L_HELP, NoBB),

    ('DfmScapula_L',       0, 'ShoulderAim_L', F_DEF, L_DMAIN, NoBB),
    ('DfmScapula_R',       0, 'ShoulderAim_R', F_DEF, L_DMAIN, NoBB),

    # Muscles
    ('DeltoidTrg2_L',      0, 'Clavicle_L', 0, L_HELP, NoBB ),
    ('DeltoidTrg2_R',      0, 'Clavicle_R', 0, L_HELP, NoBB ),
    ('Deltoid_L',          pi, 'DeltoidTrg2_L', F_WIR, L_LTWEAK, NoBB ),
    ('Deltoid_R',          0, 'DeltoidTrg2_R', F_WIR, L_RTWEAK, NoBB ),
    ('DfmDeltoid_L',       0, 'DfmClavicle_L', F_DEF, L_MSCL, NoBB ),
    ('DfmDeltoid_R',       0, 'DfmClavicle_R', F_DEF, L_MSCL, NoBB ),
    
    ('DfmPect1_L',         0, 'DfmRib', F_DEF, L_MSCL, NoBB ),
    ('DfmPect1_R',         0, 'DfmRib', F_DEF, L_MSCL, NoBB ),
    ('DfmPect2_L',         0, 'DfmRib', F_DEF, L_MSCL, NoBB ),
    ('DfmPect2_R',         0, 'DfmRib', F_DEF, L_MSCL, NoBB ),
    
    ('DfmTrap1_L',         0, 'DfmNeck', F_DEF, L_MSCL, NoBB ),
    ('DfmTrap1_R',         0, 'DfmNeck', F_DEF, L_MSCL, NoBB ),
    ('DfmTrap2_L',         0, 'DfmSpine2', F_DEF, L_MSCL, NoBB ),
    ('DfmTrap2_R',         0, 'DfmSpine2', F_DEF, L_MSCL, NoBB ),

    ('DfmLat_L',           0, 'DfmSpine1', F_DEF, L_MSCL, NoBB ),
    ('DfmLat_R',           0, 'DfmSpine1', F_DEF, L_MSCL, NoBB ),

    # Rotation diffs

    ('BendArmUp_L',        -90*D, 'Clavicle_L', 0, L_HELP, NoBB),
    ('BendArmUp_R',        90*D, 'Clavicle_R', 0, L_HELP, NoBB),
]
"""
    ('BendArmDown_L',      90*D, 'Clavicle_L', 0, L_HELP, NoBB),
    ('BendArmDown_R',      -90*D, 'Clavicle_R', 0, L_HELP, NoBB),
    ('BendArmForward_L',   0*D, 'Clavicle_L', 0, L_HELP, NoBB),
    ('BendArmForward_R',   0*D, 'Clavicle_R', 0, L_HELP, NoBB),
    ('BendArmBack_L',      0*D, 'Clavicle_L', 0, L_HELP, NoBB),
    ('BendArmBack_R',      0*D, 'Clavicle_R', 0, L_HELP, NoBB),
]
"""
#
#
#

limShoulder_L = (-16*D,40*D, -40*D,40*D,  -45*D,45*D)
limShoulder_R = (-16*D,40*D,  -40*D,40*D,  -45*D,45*D)

#
#    ShoulderControlPoses(fp):
#

def ShoulderControlPoses(fp):
    addPoseBone(fp, 'Sternum', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'SternumTarget', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

    # Clavicle
    addPoseBone(fp, 'Clavicle_L', 'MHShoulder', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_L, (True, True, True)])])

    addPoseBone(fp, 'Clavicle_R', 'MHShoulder', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_R, (True, True, True)])])

    copyDeform(fp, 'DfmClavicle_L', 'Clavicle_L', 0, U_LOC+U_ROT, None, [])
    copyDeform(fp, 'DfmClavicle_R', 'Clavicle_R', 0, U_LOC+U_ROT, None, [])
    

    # Shoulder
    
    addPoseBone(fp, 'Shoulder_L', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 1, ['Shoulder', 'ShoulderEnd_L', (1,1,1), (0,0,0), False]),
         ('CopyRot', 0, 0, ['Root', 'BendRoot', (1,1,1), (0,0,0), False])])

    addPoseBone(fp, 'Shoulder_R', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 1, ['Shoulder', 'ShoulderEnd_R', (1,1,1), (0,0,0), False]),
         ('CopyRot', 0, 0, ['Root', 'BendRoot', (1,1,1), (0,0,0), False])])

    addPoseBone(fp, 'ArmLoc_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
    	[('CopyTrans', 0, 1, ['Shoulder', 'Shoulder_L', 0])])

    addPoseBone(fp, 'ArmLoc_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
    	[('CopyTrans', 0, 1, ['Shoulder', 'Shoulder_R', 0])])

    # Muscles
    addPoseBone(fp, 'Deltoid_L', 'MHDeltoid', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'Deltoid_R', 'MHDeltoid', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'DeltoidTrg2_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
         [('CopyLoc', 0, 1, ['CopyLoc', 'DeltoidTrg1_L', (1,1,1), (0,0,0), 0, False])])

    addPoseBone(fp, 'DeltoidTrg2_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
         [('CopyLoc', 0, 1, ['CopyLoc', 'DeltoidTrg1_R', (1,1,1), (0,0,0), 0, False])])

    addPoseBone(fp, 'DfmDeltoid_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Up', 'Deltoid_L', 0, 1])])

    addPoseBone(fp, 'DfmDeltoid_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Up', 'Deltoid_R', 0, 1])])


    addPoseBone(fp, 'DfmPect1_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ArmTrg_L', 1, 1])])

    addPoseBone(fp, 'DfmPect1_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ArmTrg_R', 1, 1])])

    addPoseBone(fp, 'DfmPect2_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ArmTrg_L', 1, 1])])

    addPoseBone(fp, 'DfmPect2_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ArmTrg_R', 1, 1])])


    addPoseBone(fp, 'DfmTrap1_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
         [('StretchTo', 0, 1, ['Stretch', 'ArmTrg_L', 1, 1])])

    addPoseBone(fp, 'DfmTrap1_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ArmTrg_R', 1, 1])])

    addPoseBone(fp, 'DfmTrap2_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
         [('StretchTo', 0, 1, ['Stretch', 'ArmTrg_L', 1, 1])])

    addPoseBone(fp, 'DfmTrap2_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ArmTrg_R', 1, 1])])


    addPoseBone(fp, 'DfmLat_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ArmTrg_L', 1, 1])])

    addPoseBone(fp, 'DfmLat_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ArmTrg_R', 1, 1])])


    # Scapula
    
    addPoseBone(fp, 'ShoulderPivot_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 0.5, ['Rot', 'Clavicle_L', (1,1,1), (0,0,0), False])])
    
    addPoseBone(fp, 'ShoulderUp_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
    
    addPoseBone(fp, 'ShoulderAim_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 1, ['IK', 'SternumTarget', 1, (90*D, 'ShoulderUp_L'), (True, False,True)])])
    
    
    addPoseBone(fp, 'ShoulderPivot_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 0.5, ['Rot', 'Clavicle_R', (1,1,1), (0,0,0), False])])
    
    addPoseBone(fp, 'ShoulderUp_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
    
    addPoseBone(fp, 'ShoulderAim_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 1, ['IK', 'SternumTarget', 1, (90*D, 'ShoulderUp_R'), (True, False,True)])])

    return
    
#
#    ShoulderDeformDrivers
#    (Bone, constraint, driver, rotdiff, keypoints)
#

ShoulderDeformDrivers = [
    ("DeltoidTrg2_L", "CopyLoc", "u", 
        [("u", "ArmTrg_L", "BendArmUp_L")], 
        [(0,1), (70*D,1), (90*D,0)]),

    ("DeltoidTrg2_R", "CopyLoc", "u", 
        [("u", "ArmTrg_R", "BendArmUp_R")], 
        [(0,1), (70*D,1), (90*D,0)]),
]