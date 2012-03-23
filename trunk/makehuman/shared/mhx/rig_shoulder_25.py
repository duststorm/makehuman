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

import mhx_globals as the
from mhx_globals import *
from mhx_rig import addPoseBone, copyDeform

ShoulderJoints = [
    ('r-pect1',             'vl', ((0.96, 2870), (0.04, 2591))),
    ('l-pect1',             'vl', ((0.96, 10804), (0.04, 11017))),
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
    
    ('r-deltoid-head',      'vl', ((0.5, 3729), (0.5, 2601))),
    ('l-deltoid-head',      'vl', ((0.5, 10104), (0.5, 11009))),
    ('r-deltoid-tail',      'vl', ((0.5, 3444), (0.5, 3449))),
    ('l-deltoid-tail',      'vl', ((0.5, 10319), (0.5, 10324))),
        
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
    ('ShoulderUp_L',        ('r-clav-tail', the.yunit), ('r-clav-tail', the.ybis)),
    ('ShoulderAim_L',       'r-clav-tail', 'r-clav-aim'),
    ('DfmClavicle_L',       'r-clavicle', 'r-clav-tail'),

    ('Clavicle_R',          'l-clavicle', 'l-clav-tail'),
    ('ShoulderPivot_R',     'l-clavicle', 'l-clav-tail'),
    ('ShoulderUp_R',        ('l-clav-tail', the.yunit), ('l-clav-tail', the.ybis)),
    ('ShoulderAim_R',       'l-clav-tail', 'l-clav-aim'),
    ('DfmClavicle_R',       'l-clavicle', 'l-clav-tail'),

    # Shoulder
    ('ShoulderEnd_L',       'r-uparm0', ('r-uparm0', the.yunit)),
    ('ShoulderEnd_R',       'l-uparm0', ('l-uparm0', the.yunit)),
    ('Shoulder_L',          'r-uparm0', ('r-uparm0', the.ysmall)),
    ('Shoulder_R',          'l-uparm0', ('l-uparm0', the.ysmall)),

    # Scapula
    
    ('DfmScapula_L',        'r-scapula2-head', 'r-scapula2-tail'),
    ('DfmScapula_R',        'l-scapula2-head', 'l-scapula2-tail'),

    # Muscles
    
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
    
    ('DfmDeltoid_L',         'r-deltoid-head', 'r-deltoid-tail'),
    ('DfmDeltoid_R',         'l-deltoid-head', 'l-deltoid-tail'),
    
    # Elbow lock

    ('Elbow_L',              'r-elbow', ('r-elbow',the.yunit)),
    ('ELClavicle_L',         'r-clavicle', 'r-clav-tail'),
    ('ELUpArm_L',            'r-uparm0', 'r-elbow'),
    ('ELClavPT_L',           ('r-clav-tail', [0,2,0]), ('r-clav-tail', [0,3,0])),
    ('ELClavLinkPT_L',       'r-clav-tail', ('r-clav-tail', [0,2,0])),
    
    ('Elbow_R',              'l-elbow', ('l-elbow',the.yunit)),
    ('ELClavicle_R',         'l-clavicle', 'l-clav-tail'),
    ('ELUpArm_R',            'l-uparm0', 'l-elbow'),
    ('ELClavPT_R',           ('l-clav-tail', [0,2,0]), ('l-clav-tail', [0,3,0])),
    ('ELClavLinkPT_R',       'l-clav-tail', ('l-clav-tail', [0,2,0])),
        
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
    ('Shoulder_L',         0, 'ShoulderEnd_L', F_WIR+F_NOROT, L_TWEAK, NoBB),
    ('Shoulder_R',         0, 'ShoulderEnd_R', F_WIR+F_NOROT, L_TWEAK, NoBB),

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

    ('DfmDeltoid_L',       0, 'DfmClavicle_L', F_DEF, L_MSCL, NoBB ),
    ('DfmDeltoid_R',       0, 'DfmClavicle_R', F_DEF, L_MSCL, NoBB ),
    
    # Elbow lock        
    ('Elbow_L',            0, Master, F_WIR, L_LEXTRA, NoBB),
    ('ELClavicle_L',       0, 'Sternum', 0, L_HELP, NoBB),
    ('ELUpArm_L',          0, 'ELClavicle_L', F_CON, L_HELP, NoBB),
    ('ELClavPT_L',         0, 'Sternum', F_WIR, L_LEXTRA, NoBB),
    ('ELClavLinkPT_L',     0, 'Clavicle_L', F_RES, L_LEXTRA, NoBB),

    ('Elbow_R',            0, Master, F_WIR, L_REXTRA, NoBB),
    ('ELClavicle_R',       0, 'Sternum', 0, L_HELP, NoBB),
    ('ELUpArm_R',          0, 'ELClavicle_R', F_CON, L_HELP, NoBB),
    ('ELClavPT_R',         0, 'Sternum', F_WIR, L_REXTRA, NoBB),
    ('ELClavLinkPT_R',     0, 'Clavicle_R', F_RES, L_REXTRA, NoBB),

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
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_L, (True, True, True)]),
         ('CopyTrans', 0, 0, ['Elbow', 'ELClavicle_L', 0])
        ])

    addPoseBone(fp, 'Clavicle_R', 'MHShoulder', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_R, (True, True, True)]),
         ('CopyTrans', 0, 0, ['Elbow', 'ELClavicle_R', 0])
        ])

    copyDeform(fp, 'DfmClavicle_L', 'Clavicle_L', 0, U_LOC+U_ROT, None, [])
    copyDeform(fp, 'DfmClavicle_R', 'Clavicle_R', 0, U_LOC+U_ROT, None, [])
    

    # Shoulder
    
    addPoseBone(fp, 'Shoulder_L', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 1, ['Shoulder', 'ShoulderEnd_L', (1,1,1), (0,0,0), False]),
         ('CopyRot', 0, 0, ['Root', 'BendRoot', (1,1,1), (0,0,0), False])])

    addPoseBone(fp, 'Shoulder_R', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 1, ['Shoulder', 'ShoulderEnd_R', (1,1,1), (0,0,0), False]),
         ('CopyRot', 0, 0, ['Root', 'BendRoot', (1,1,1), (0,0,0), False])])

    # Muscles
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


    addPoseBone(fp, 'DfmDeltoid_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('DampedTrack', 0, 0.5, ['DampedTrack', 'UpArm_L', 'TRACK_Y', 1])])

    addPoseBone(fp, 'DfmDeltoid_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('DampedTrack', 0, 0.5, ['DampedTrack', 'UpArm_R', 'TRACK_Y', 1])])


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

    # Elbow lock
    
    addPoseBone(fp, 'Elbow_L', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
        the.RootChildOfConstraints + [
        ('LimitDist', 0, 0, ['DistSternum', 'Sternum', 'LIMITDIST_INSIDE']),
        ])
        
    addPoseBone(fp, 'ELClavicle_L', None, None, (1,1,1), (0,0,0), (1,1,1), 
                ((1,0,1), (0.6,1,0.6), 0.0, None), 0, [])

    addPoseBone(fp, 'ELUpArm_L', None, None, (1,1,1), (0,0,0), (1,1,1), 
                ((1,1,1), (0.2,0.6,0.2), 0.05, None), 0,     
        [('IK', 0, 1, ['IK', 'Elbow_L', 2, (90*D, 'ELClavPT_L'), (True, False,True)])])

    addPoseBone(fp, 'ELClavPT_L', 'MHCube025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'ELClavLinkPT_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ELClavPT_L', 0, 1])])
        

    addPoseBone(fp, 'Elbow_R', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
        the.RootChildOfConstraints + [
        ('LimitDist', 0, 0, ['DistSternum', 'Sternum', 'LIMITDIST_INSIDE']),
        ])
        
    addPoseBone(fp, 'ELClavicle_R', None, None, (1,1,1), (0,0,0), (1,1,1), 
                ((1,0,1), (0.6,1,0.6), 0.0, None), 0, [])

    addPoseBone(fp, 'ELUpArm_R', None, None, (1,1,1), (0,0,0), (1,1,1), 
                ((1,1,1), (0.2,0.6,0.2), 0.05, None), 0,     
        [('IK', 0, 1, ['IK', 'Elbow_R', 2, (90*D, 'ELClavPT_R'), (True, False,True)])])

    addPoseBone(fp, 'ELClavPT_R', 'MHCube025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'ELClavLinkPT_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ELClavPT_R', 0, 1])])
        
    return
    
#
#    ShoulderDeformDrivers
#    (Bone, constraint, driver, rotdiff, keypoints)
#

ShoulderDeformDrivers = [
    ("DfmDeltoid_L", "DampedTrack", "2*cos(x)", [("x", "DfmUpArm1_L", "BendArmUp_L")], []),
    ("DfmDeltoid_R", "DampedTrack", "2*cos(x)", [("x", "DfmUpArm1_R", "BendArmUp_R")], []),
]
