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

from . import the
from the import *
from . import posebone
from posebone import addPoseBone

ShoulderJoints = [
    ('r-clav-head',         'l', ((0.7, 'r-scapula'), (0.3, 'l-scapula'))),
    ('l-clav-head',         'l', ((0.3, 'r-scapula'), (0.7, 'l-scapula'))),

    ('r-clav-top',          'v', 2862),
    ('l-clav-top',          'v', 10812),
    ('r-clav-tail',         'l', ((0.5, 'r-clav-top'), (0.5, 'r-uparm0'))),
    ('l-clav-tail',         'l', ((0.5, 'l-clav-top'), (0.5, 'l-uparm0'))),

    ('r-deltoid-head',      'l', ((0.6, 'r-clav-tail'), (0.4, 'l-clav-tail'))),
    ('l-deltoid-head',      'l', ((0.4, 'r-clav-tail'), (0.6, 'l-clav-tail'))),
]

if MuscleBones:
    ShoulderJoints += [
    ('sternum-tail',        'v', 7279),
    ('sternum-head',        'l', ((0.5, 'neck'), (0.5, 'sternum-tail'))),

    ('r-shldr-front',       'v', 3008),
    ('l-shldr-front',       'v', 10718),
    ('r-shldr-back',        'v', 3452),
    ('l-shldr-back',        'v', 10316),
    ('r-shldr-bot',         'v', 3424),
    ('l-shldr-bot',         'v', 10344),

    ('r-pect1',             'vl', ((0.9, 2870), (0.1, 2591))),
    ('l-pect1',             'vl', ((0.9, 10804), (0.1, 11017))),
    ('r-pect2',             'vl', ((0.9, 3535), (0.1, 3600))),
    ('l-pect2',             'vl', ((0.9, 10257), (0.1, 10192))),
    ('r-pecttrg',           'l', ((0.7, 'r-shldr-front'), (0.3, 'r-shldr-back'))),
    ('l-pecttrg',           'l', ((0.7, 'l-shldr-front'), (0.3, 'l-shldr-back'))),

    ('r-trap1',             'vl', ((0.9, 3417), (0.1, 2483))),
    ('l-trap1',             'vl', ((0.9, 10347), (0.1, 8914))),
    ('r-trap2',             'vl', ((0.9, 2614), (0.1, 2945))),
    ('l-trap2',             'vl', ((0.9, 10996), (0.1, 10775))),
    ('r-traptrg',           'l', ((0.3, 'r-shldr-front'), (0.7, 'r-shldr-back'))),
    ('l-traptrg',           'l', ((0.3, 'l-shldr-front'), (0.7, 'l-shldr-back'))),

    ('r-lat',               'vl', ((0.9, 4430), (0.1, 2948))),
    ('l-lat',               'vl', ((0.9, 9997), (0.1, 10772))),
    ('r-lattrg',            'l', ((0.4, 'r-armtrg'), (0.6, 'r-shldr-bot'))),
    ('l-lattrg',            'l', ((0.4, 'l-armtrg'), (0.6, 'l-shldr-bot'))),
    
    ('r-deltoid-head',      'vl', ((0.5, 3729), (0.5, 2601))),
    ('l-deltoid-head',      'vl', ((0.5, 10104), (0.5, 11009))),
    ('r-deltoid-tail',      'vl', ((0.5, 3444), (0.5, 3449))),
    ('l-deltoid-tail',      'vl', ((0.5, 10319), (0.5, 10324))),
        
    ('r-clav-aim',          'l', ((0.5, 'sternum-head'), (0.5, 'r-clav-tail'))),
    ('l-clav-aim',          'l', ((0.5, 'sternum-head'), (0.5, 'l-clav-tail'))),
    
    ('r-scapula1-head',     'vl', ((0.9, 3044), (0.1, 4444))),
    ('r-scapula1-tail',     'v', 2584),
    ('r-scapula2-head',     'l', ((0.5, 'r-scapula1-head'), (0.5, 'r-scapula1-tail'))),
    ('r-scapula2-tail',     'vl', ((0.9, 2607), (0.1, 3550))),
    ('l-scapula1-head',     'vl', ((0.9, 10687), (0.1, 9983))),
    ('l-scapula1-tail',     'v', 11024),
    ('l-scapula2-head',     'l', ((0.5, 'l-scapula1-head'), (0.5, 'l-scapula1-tail'))),
    ('l-scapula2-tail',     'vl', ((0.9, 11003), (0.1, 10242))),
]

ShoulderHeadsTails = [
    # Clavicle
    ('Clavicle_L',          'r-clavicle', 'r-clav-tail'),
    ('Clavicle_R',          'l-clavicle', 'l-clav-tail'),
    ('DfmClavicle_L',       'r-clavicle', 'r-clav-tail'),
    ('DfmClavicle_R',       'l-clavicle', 'l-clav-tail'),
    ('DfmDeltoid_L',        'r-deltoid-head', 'r-clav-tail'),
    ('DfmDeltoid_R',        'l-deltoid-head', 'l-clav-tail'),

    # Shoulder
    ('Shoulder_L',          'r-uparm0', ('r-uparm0', (0,1,0))),
    ('Shoulder_R',          'l-uparm0', ('l-uparm0', (0,1,0))),
    ('UpArmSocket_L',       'r-uparm0', ('r-uparm0', (0,0.5,0))),
    ('UpArmSocket_R',       'l-uparm0', ('l-uparm0', (0,0.5,0))),
    ('UpArmHinge_L',        ('r-clav-tail', (0,1,0)), 'r-clav-tail'),
    ('UpArmHinge_R',        ('l-clav-tail', (0,1,0)), 'l-clav-tail'),

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
        
    # Directions
    ('DirShldrOut_L',        'r-uparm0', ('r-uparm0', (1,0,0))),
    ('DirShldrOut_R',        'l-uparm0', ('l-uparm0', (-1,0,0))),
    ('DirShldrDown_L',        'r-uparm0', ('r-uparm0', (0,-1,0))),
    ('DirShldrDown_R',        'l-uparm0', ('l-uparm0', (0,-1,0))),
    ('DirShldrUp_L',          'r-uparm0', ('r-uparm0', (0,1,0))),
    ('DirShldrUp_R',          'l-uparm0', ('l-uparm0', (0,1,0))),
    ('DirShldrFwd_L',         'r-uparm0', ('r-uparm0', (0,0,1))),
    ('DirShldrFwd_R',         'l-uparm0', ('l-uparm0', (0,0,1))),
    ('DirShldrBack_L',        'r-uparm0', ('r-uparm0', (0,0,-1))),
    ('DirShldrBack_R',        'l-uparm0', ('l-uparm0', (0,0,-1))),
]

if MuscleBones:
    ShoulderHeadsTails += [    
    ('Sternum',             'neck', 'sternum-tail'),
    ('SternumTarget',       'sternum-head', 'sternum-tail'),
    
    # Clavicle
    ('ShoulderPivot_L',     'r-clavicle', 'r-clav-tail'),
    ('ShoulderUp_L',        ('r-clav-tail', the.yunit), ('r-clav-tail', the.ybis)),
    ('ShoulderAim_L',       'r-clav-tail', 'r-clav-aim'),

    ('ShoulderPivot_R',     'l-clavicle', 'l-clav-tail'),
    ('ShoulderUp_R',        ('l-clav-tail', the.yunit), ('l-clav-tail', the.ybis)),
    ('ShoulderAim_R',       'l-clav-tail', 'l-clav-aim'),

    # Scapula
    
    ('DfmScapula_L',        'r-scapula2-head', 'r-scapula2-tail'),
    ('DfmScapula_R',        'l-scapula2-head', 'l-scapula2-tail'),

    # Muscles
    
    ('DfmPect1_L',           'r-pect1', 'r-pecttrg'),
    ('DfmPect1_R',           'l-pect1', 'l-pecttrg'),
    ('DfmPect2_L',           'r-pect2', 'r-pecttrg'),
    ('DfmPect2_R',           'l-pect2', 'l-pecttrg'),
    ('PectTrg_L',            'r-armtrg', 'r-pecttrg'),
    ('PectTrg_R',            'l-armtrg', 'l-pecttrg'),

    ('DfmTrap1_L',           'r-trap1', 'r-traptrg'),
    ('DfmTrap1_R',           'l-trap1', 'l-traptrg'),
    ('DfmTrap2_L',           'r-trap2', 'r-traptrg'),
    ('DfmTrap2_R',           'l-trap2', 'l-traptrg'),
    ('TrapTrg_L',            'r-armtrg', 'r-traptrg'),
    ('TrapTrg_R',            'l-armtrg', 'l-traptrg'),

    ('DfmLat_L',             'r-lat', 'r-armtrg'),
    ('DfmLat_R',             'l-lat', 'l-armtrg'),
    ('LatTrg_L',             'r-lattrg', 'r-armtrg'),
    ('LatTrg_R',             'l-lattrg', 'l-armtrg'),
    
    ('DfmDeltoid_L',         'r-deltoid-head', 'r-deltoid-tail'),
    ('DfmDeltoid_R',         'l-deltoid-head', 'l-deltoid-tail'),
    
]

L_LSHOULDER = L_LARMFK+L_LARMIK+L_UPSPNFK+L_UPSPNIK
L_RSHOULDER = L_RARMFK+L_RARMIK+L_UPSPNFK+L_UPSPNIK

ShoulderArmature1Advanced = [
    # Clavicle
    ('Clavicle_L',         0, 'DfmSpine3', F_WIR, L_LSHOULDER, NoBB),
    ('Clavicle_R',         0, 'DfmSpine3', F_WIR, L_RSHOULDER, NoBB),
]

ShoulderArmature1Simple = [
    # Clavicle
    ('Clavicle_L',         0, 'Spine3', F_WIR, L_LSHOULDER, NoBB),
    ('Clavicle_R',         0, 'Spine3', F_WIR, L_RSHOULDER, NoBB),
]

ShoulderArmature2 = [
    # Shoulder    
    ('DfmClavicle_L',      0, 'Clavicle_L', F_DEF, L_DEF, NoBB),
    ('DfmClavicle_R',      0, 'Clavicle_R', F_DEF, L_DEF, NoBB),
    ('Shoulder_L',         0, 'Clavicle_L', F_WIR, L_TWEAK, NoBB),
    ('Shoulder_R',         0, 'Clavicle_R', F_WIR, L_TWEAK, NoBB),
    ('UpArmSocket_L',      0, 'Root', 0, L_HELP, NoBB),
    ('UpArmSocket_R',      0, 'Root', 0, L_HELP, NoBB),
    ('UpArmHinge_L',       0, 'UpArmSocket_L', 0, L_HELP, NoBB),
    ('UpArmHinge_R',       0, 'UpArmSocket_R', 0, L_HELP, NoBB),
    ('UpArm_L',            0, 'UpArmHinge_L', F_WIR, L_LARMFK, NoBB),
    ('UpArm_R',            0, 'UpArmHinge_R', F_WIR, L_RARMFK, NoBB),
    ('DfmDeltoid_L',       0, 'DfmClavicle_L', F_DEF, L_MSCL, NoBB ),
    ('DfmDeltoid_R',       0, 'DfmClavicle_R', F_DEF, L_MSCL, NoBB ),
    
    # Elbow lock        
    ('Elbow_L',            0, Master, F_WIR, L_LEXTRA, NoBB),
    ('ELClavicle_L',       0, 'DfmSpine3', 0, L_HELP2, NoBB),
    ('ELUpArm_L',          0, 'ELClavicle_L', F_CON, L_HELP2, NoBB),
    ('ELClavPT_L',         0, 'DfmSpine3', F_WIR, L_LEXTRA, NoBB),
    ('ELClavLinkPT_L',     0, 'Clavicle_L', F_RES, L_LEXTRA, NoBB),

    ('Elbow_R',            0, Master, F_WIR, L_REXTRA, NoBB),
    ('ELClavicle_R',       0, 'DfmSpine3', 0, L_HELP2, NoBB),
    ('ELUpArm_R',          0, 'ELClavicle_R', F_CON, L_HELP2, NoBB),
    ('ELClavPT_R',         0, 'DfmSpine3', F_WIR, L_REXTRA, NoBB),
    ('ELClavLinkPT_R',     0, 'Clavicle_R', F_RES, L_REXTRA, NoBB),

    # Directions

    ('DirShldrOut_L',       0*D, 'Clavicle_L', 0, L_HELP, NoBB),
    ('DirShldrOut_R',       180*D, 'Clavicle_R', 0, L_HELP, NoBB),

    ('DirShldrUp_L',        -90*D, 'Clavicle_L', 0, L_HELP, NoBB),
    ('DirShldrUp_R',        90*D, 'Clavicle_R', 0, L_HELP, NoBB),

    ('DirShldrDown_L',      90*D, 'Clavicle_L', 0, L_HELP, NoBB),
    ('DirShldrDown_R',      -90*D, 'Clavicle_R', 0, L_HELP, NoBB),

    ('DirShldrFwd_L',       0*D, 'Clavicle_L', 0, L_HELP, NoBB),
    ('DirShldrFwd_R',       0*D, 'Clavicle_R', 0, L_HELP, NoBB),

    ('DirShldrBack_L',      0*D, 'Clavicle_L', 0, L_HELP, NoBB),
    ('DirShldrBack_R',      0*D, 'Clavicle_R', 0, L_HELP, NoBB),
]    
"""
if MuscleBones:
    ShoulderArmature += [
    ('Sternum',            0, 'DfmSpine3', 0, L_HELP, NoBB),
    ('SternumTarget',      0, 'Sternum', 0, L_HELP, NoBB),

    # Scapula
    ('ShoulderPivot_L',    0, 'Sternum', 0, L_HELP, NoBB),
    ('ShoulderUp_L',       0, 'ShoulderPivot_L', 0, L_HELP, NoBB),
    ('ShoulderAim_L',      0, 'ShoulderPivot_L', 0, L_HELP, NoBB),

    ('ShoulderPivot_R',    0, 'Sternum', 0, L_HELP, NoBB),
    ('ShoulderUp_R',       0, 'ShoulderPivot_R', 0, L_HELP, NoBB),
    ('ShoulderAim_R',      0, 'ShoulderPivot_R', 0, L_HELP, NoBB),

    ('DfmScapula_L',       0, 'ShoulderAim_L', F_DEF1, L_DEF, NoBB),
    ('DfmScapula_R',       0, 'ShoulderAim_R', F_DEF1, L_DEF, NoBB),

    # Muscles
    ('DfmPect1_L',         0, 'DfmRib', F_DEF1, L_MSCL, NoBB ),
    ('DfmPect1_R',         0, 'DfmRib', F_DEF1, L_MSCL, NoBB ),
    ('DfmPect2_L',         0, 'DfmRib', F_DEF1, L_MSCL, NoBB ),
    ('DfmPect2_R',         0, 'DfmRib', F_DEF1, L_MSCL, NoBB ),
    ('PectTrg_L',          0, 'UpArmVec_L', 0, L_HELP, NoBB),
    ('PectTrg_R',          0, 'UpArmVec_R', 0, L_HELP, NoBB),
    
    ('DfmTrap1_L',         0, 'DfmNeck', F_DEF1, L_MSCL, NoBB ),
    ('DfmTrap1_R',         0, 'DfmNeck', F_DEF1, L_MSCL, NoBB ),
    ('DfmTrap2_L',         0, 'DfmSpine2', F_DEF1, L_MSCL, NoBB ),
    ('DfmTrap2_R',         0, 'DfmSpine2', F_DEF1, L_MSCL, NoBB ),
    ('TrapTrg_L',          0, 'UpArmVec_L', 0, L_HELP, NoBB),
    ('TrapTrg_R',          0, 'UpArmVec_R', 0, L_HELP, NoBB),

    ('DfmLat_L',           0, 'DfmSpine1', F_DEF1, L_MSCL, NoBB ),
    ('DfmLat_R',           0, 'DfmSpine1', F_DEF1, L_MSCL, NoBB ),
    ('LatTrg_L',           0, 'UpArmVec_L', 0, L_HELP, NoBB),
    ('LatTrg_R',           0, 'UpArmVec_R', 0, L_HELP, NoBB),

    ('DfmDeltoid_L',       0, 'DfmClavicle_L', F_DEF1, L_MSCL, NoBB ),
    ('DfmDeltoid_R',       0, 'DfmClavicle_R', F_DEF1, L_MSCL, NoBB ),
]
"""
#
#
#

limShoulder_L = (-16*D,40*D, -40*D,40*D,  -45*D,45*D)
limShoulder_R = (-16*D,40*D,  -40*D,40*D,  -45*D,45*D)

#
#    ShoulderControlPoses(fp, config):
#

def ShoulderControlPoses(fp, config):
    # Clavicle
    addPoseBone(fp, config, 'Clavicle_L', 'MHShoulder', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_L, (True, True, True)]),
         ('CopyTrans', 0, 0, ['Elbow', 'ELClavicle_L', 0])
        ])

    addPoseBone(fp, config, 'Clavicle_R', 'MHShoulder', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limShoulder_R, (True, True, True)]),
         ('CopyTrans', 0, 0, ['Elbow', 'ELClavicle_R', 0])
        ])

    # Shoulder
    
    addPoseBone(fp, config, 'Shoulder_L', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'Shoulder_R', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'UpArmSocket_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyLoc', 0, 0, ['Hinge', 'Shoulder_L', (1,1,1), (0,0,0), 0, False]),
         ('CopyTrans', 0, 1, ['Shoulder', 'Shoulder_L', 0])])

    addPoseBone(fp, config, 'UpArmSocket_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyLoc', 0, 0, ['Hinge', 'Shoulder_R', (1,1,1), (0,0,0), 0, False]),
         ('CopyTrans', 0, 1, ['Shoulder', 'Shoulder_R', 0])])

    addPoseBone(fp, config, 'UpArmHinge_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'UpArmHinge_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])
         

    # Elbow lock
    
    if config.exporting:
        addPoseBone(fp, config, 'Elbow_L', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
            [
            #('LimitDist', 0, 0, ['DistSternum', 'Sternum', 'LIMITDIST_INSIDE']),
            ])
        
        addPoseBone(fp, config, 'ELClavicle_L', None, None, (1,1,1), (0,0,0), (1,1,1), 
                    ((1,0,1), (0.6,1,0.6), 0.0, None), 0, [])

        addPoseBone(fp, config, 'ELUpArm_L', None, None, (1,1,1), (0,0,0), (1,1,1), 
                    ((1,1,1), (0.2,0.6,0.2), 0.05, None), 0,     
            [('IK', 0, 1, ['IK', 'Elbow_L', 2, (90*D, 'ELClavPT_L'), (True, False,True)])])

        addPoseBone(fp, config, 'ELClavPT_L', 'MHCube025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

        addPoseBone(fp, config, 'ELClavLinkPT_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
            [('StretchTo', 0, 1, ['Stretch', 'ELClavPT_L', 0, 1])])
        

        addPoseBone(fp, config, 'Elbow_R', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
            [
            #('LimitDist', 0, 0, ['DistSternum', 'Sternum', 'LIMITDIST_INSIDE']),
            ])
        
        addPoseBone(fp, config, 'ELClavicle_R', None, None, (1,1,1), (0,0,0), (1,1,1), 
                    ((1,0,1), (0.6,1,0.6), 0.0, None), 0, [])

        addPoseBone(fp, config, 'ELUpArm_R', None, None, (1,1,1), (0,0,0), (1,1,1), 
                    ((1,1,1), (0.2,0.6,0.2), 0.05, None), 0,     
            [('IK', 0, 1, ['IK', 'Elbow_R', 2, (90*D, 'ELClavPT_R'), (True, False,True)])])

        addPoseBone(fp, config, 'ELClavPT_R', 'MHCube025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

        addPoseBone(fp, config, 'ELClavLinkPT_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
            [('StretchTo', 0, 1, ['Stretch', 'ELClavPT_R', 0, 1])])


    addPoseBone(fp, config, 'DfmDeltoid_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('Transform', C_LOCAL, 1, 
            ['Transform', 'UpArm_L', 
            'ROTATION', (0,0,0), (120,0,0), ('X','Y','Z'),
            'ROTATION', (0,0,0), (60,0,0)]) ])

    addPoseBone(fp, config, 'DfmDeltoid_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('Transform', C_LOCAL, 1, 
            ['Transform', 'UpArm_R', 
            'ROTATION', (0,0,0), (120,0,0), ('X','Y','Z'),
            'ROTATION', (0,0,0), (60,0,0)]) ])


        
    if not MuscleBones:
        return        
         
    addPoseBone(fp, config, 'Sternum', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SternumTarget', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

    # Muscle bones
    
    addPoseBone(fp, config, 'DfmPect1_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'PectTrg_L', 1.0, 1])])

    addPoseBone(fp, config, 'DfmPect1_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'PectTrg_R', 1.0, 1])])

    addPoseBone(fp, config, 'DfmPect2_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'PectTrg_L', 1.0, 1])])

    addPoseBone(fp, config, 'DfmPect2_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'PectTrg_R', 1.0, 1])])


    addPoseBone(fp, config, 'DfmTrap1_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
         [('StretchTo', 0, 1, ['Stretch', 'TrapTrg_L', 1.0, 1])])
    addPoseBone(fp, config, 'DfmTrap1_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'TrapTrg_R', 1.0, 1])])

    addPoseBone(fp, config, 'DfmTrap2_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
         [('StretchTo', 0, 1, ['Stretch', 'TrapTrg_L', 1.0, 1])])

    addPoseBone(fp, config, 'DfmTrap2_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'TrapTrg_R', 1.0, 1])])


    addPoseBone(fp, config, 'DfmLat_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'UpArmVec_L', 1.0, 1])])

    addPoseBone(fp, config, 'DfmLat_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'UpArmVec_R', 1.0, 1])])


    addPoseBone(fp, config, 'DfmDeltoid_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('DampedTrack', 0, 0.5, ['DampedTrack', 'UpArm_L', 'TRACK_Y', 1])])

    addPoseBone(fp, config, 'DfmDeltoid_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('DampedTrack', 0, 0.5, ['DampedTrack', 'UpArm_R', 'TRACK_Y', 1])])


    # Scapula
    
    addPoseBone(fp, config, 'ShoulderPivot_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 0.5, ['Rot', 'Clavicle_L', (1,1,1), (0,0,0), False])])
    
    addPoseBone(fp, config, 'ShoulderUp_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
    
    addPoseBone(fp, config, 'ShoulderAim_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 1, ['IK', 'SternumTarget', 1, (90*D, 'ShoulderUp_L'), (True, False,True)])])
    
    
    addPoseBone(fp, config, 'ShoulderPivot_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 0.5, ['Rot', 'Clavicle_R', (1,1,1), (0,0,0), False])])
    
    addPoseBone(fp, config, 'ShoulderUp_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
    
    addPoseBone(fp, config, 'ShoulderAim_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 1, ['IK', 'SternumTarget', 1, (90*D, 'ShoulderUp_R'), (True, False,True)])])
        
    return
    
#
#    ShoulderDeformDrivers
#    (Bone, constraint, driver, rotdiff, keypoints)
#

if MuscleBones:
    ShoulderDeformDrivers = [
    ("DfmDeltoid_L", "DampedTrack", "o*i+(1-o)*max(2*cos(u),max(0.5*cos(f),1.5*cos(b)))", 
        [("u", 'ROTATION_DIFF', "DfmUpArm1_L", "DirShldrUp_L"),
         ("f", 'ROTATION_DIFF', "DfmUpArm1_L", "DirShldrFwd_L"),
         ("b", 'ROTATION_DIFF', "DfmUpArm1_L", "DirShldrBack_L"),
         ("i", 'SINGLE_PROP', "&TweakDeltoidInfluence_L", ""),
         ("o", 'SINGLE_PROP', "&TweakDeltoidOn_L", ""),
        ], []),
    ("DfmDeltoid_R", "DampedTrack", "o*i+(1-o)*max(2*cos(u),max(0.5*cos(f),1.5*cos(b)))", 
        [("u", 'ROTATION_DIFF', "DfmUpArm1_R", "DirShldrUp_R"),
         ("f", 'ROTATION_DIFF', "DfmUpArm1_R", "DirShldrFwd_R"),
         ("b", 'ROTATION_DIFF', "DfmUpArm1_R", "DirShldrBack_R"),
         ("i", 'SINGLE_PROP', "&TweakDeltoidInfluence_R", ""),
         ("o", 'SINGLE_PROP', "&TweakDeltoidOn_R", ""),
        ], []),
]

    ShoulderTargetDrivers = []
else:
    ShoulderDeformDrivers = []
    ShoulderTargetDrivers = []
    
"""    
    expr70 = "%.3f*(1-%.3f*x1)" % (90.0/70.0, 2/pi)
    expr70_60 = "%.3f*max(1-%.3f*x1,0)*max(1-%.3f*x2,0)" % (90.0/70.0, 2/pi, 3/pi)

    ShoulderTargetDrivers = [
    ("arms-up-70", "LR", expr70_60, 
        [("UpArmVec", "DirShldrUp"),
         ("UpArm", "UpArmVec")]),
    ("arms-up-70-pos-60", "LR", expr70_60,
        [("UpArmVec", "DirShldrUp"),
         ("UpArm", "UpArmVecPos")]),
    ("arms-up-70-neg-60", "LR", expr70_60,
        [("UpArmVec", "DirShldrUp"),
         ("UpArm", "UpArmVecNeg")]),

    ("arms-down-70", "LR", expr70_60,
        [("UpArmVec", "DirShldrDown"),
         ("UpArm", "UpArmVec")]),
    ("arms-down-70-pos-60", "LR", expr70_60,
        [("UpArmVec", "DirShldrDown"),
         ("UpArm", "UpArmVecPos")]),
    ("arms-down-70-neg-60", "LR", expr70_60,
        [("UpArmVec", "DirShldrDown"),
         ("UpArm", "UpArmVecNeg")]),

    ("arms-forward-70", "LR", expr70_60,
        [("UpArmVec", "DirShldrFwd"),
         ("UpArm", "UpArmVec")]),
    ("arms-forward-70-pos-60", "LR", expr70_60,
        [("UpArmVec", "DirShldrFwd"),
         ("UpArm", "UpArmVecPos")]),
    ("arms-forward-70-neg-60", "LR", expr70_60,
        [("UpArmVec", "DirShldrFwd"),
         ("UpArm", "UpArmVecNeg")]),

    ("arms-back-70", "LR", expr70_60,
        [("UpArmVec", "DirShldrBack"),
         ("UpArm", "UpArmVec")]),
    ("arms-back-70-pos-60", "LR", expr70_60,
        [("UpArmVec", "DirShldrBack"),
         ("UpArm", "UpArmVecPos")]),
    ("arms-back-70-neg-60", "LR", expr70_60,
        [("UpArmVec", "DirShldrBack"),
         ("UpArm", "UpArmVecNeg")]),
    
    ("arms-twist-pos-60", "LR", expr70_60,  
        [("UpArmVec", "DirShldrOut"),
         ("UpArm", "UpArmVecPos")]),
    ("arms-twist-neg-60", "LR", expr70_60,  
        [("UpArmVec", "DirShldrOut"),
         ("UpArm", "UpArmVecNeg")]),
]
"""