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
Body bone definitions 

"""

import mhx_rig
from mhx_rig import *

BodyJoints = [
    ('root-tail',      'o', ('spine3', [0,-1,0])),
    ('hips-tail',      'o', ('pelvis', [0,-1,0])),
    ('mid-uplegs',     'l', ((0.5, 'l-upper-leg'), (0.5, 'r-upper-leg'))),
    #('spine0',        'l', ((0.5, 'spine1'), (0.5, 'neck'))),
    ('spine-pt',       'o', ('spine2', [0,0,-10])),

    ('r-breast',       'vl', ((0.4, 3559), (0.6, 2944))),
    ('r-tit',          'v', 3718),
    ('l-breast',       'vl', ((0.4, 10233), (0.6, 10776))),
    ('l-tit',          'v', 10115),

    ('mid-rib-top',    'v', 7273),
    ('mid-rib-bot',    'v', 6908),

    ('neck2',          'vl', ((0.5, 6531), (0.5, 8253))),
    ('abdomen-front',  'v', 7359),
    ('abdomen-back',   'v', 7186),
    ('stomach-top',    'v', 7336),
    ('stomach-bot',    'v', 7297),
    ('stomach-front',  'v', 7313),
    ('stomach-back',   'v', 7472),

    ('penis-tip',      'v', 7415),
    ('penis-root',     'vl', ((0.5, 2792), (0.5, 7448))),
    ('scrotum-tip',    'v', 7444),
    ('scrotum-root',   'vl', ((0.5, 2807), (0.5, 7425))),

    ('r-toe-1-1',      'j', 'r-toe-1-1'),
    ('l-toe-1-1',      'j', 'l-toe-1-1'),
    ('mid-feet',       'l', ((0.5, 'l-toe-1-1'), (0.5, 'r-toe-1-1'))),
    ('floor',          'o', ('mid-feet', [0,-0.3,0])),
]

BodyHeadsTails = [
    ('MasterFloor',    'floor', ('floor', zunit)),

    ('Root',           'root-tail', 'spine3'),
    ('Shoulders',      'neck', ('neck', [0,0.5,0])),

    # Up spine
    ('Hips',           'spine3', 'root-tail'),
    ('Spine1',         'spine3', 'spine2'),
    ('Spine2',         'spine2', 'spine1'),
    ('Spine3',         'spine1', 'neck'),
    ('Neck',           'neck', 'neck2'),
    ('Head',           'neck2', 'head-end'),

    ('SpinePT',        'spine-pt', ('spine-pt', yunit)),
    ('SpineLinkPT',    'spine2', 'spine-pt'),

    # Down spine    
    ('DownHips',       'spine3', 'root-tail'),
    ('DownSpine1',     'spine3', 'spine2'),
    ('DownSpine2',     'spine2', 'spine1'),
    ('DownSpine3',     'spine1', 'neck'),
    ('DownNeck',       'neck', 'neck2'),

    # Help spine    
    ('HlpHips',        'spine3', 'root-tail'),
    ('HlpSpine1',      'spine3', 'spine2'),
    ('HlpSpine2',      'spine2', 'spine1'),
    ('HlpSpine3',      'spine1', 'neck'),
    ('HlpNeck',        'neck', 'neck2'),

    # Deform spine
    ('DfmHips',        'spine3', 'root-tail'),
    ('DfmSpine1',      'spine3', 'spine2'),
    ('DfmSpine2',      'spine2', 'spine1'),
    ('DfmSpine3',      'spine1', 'neck'),
    ('DfmNeck',        'neck', 'neck2'),
    ('DfmHead',        'neck2', 'head-end'),

    # Deform torso
    ('DfmRib',         'mid-rib-top', 'mid-rib-bot'),
    #('RibTarget',      'spine2', 'mid-rib-bot'),
    ('DfmStomach',     'stomach-bot', 'mid-rib-bot'),
    #('HipBone',        'root-tail', 'stomach-bot'),
    ('Breathe',        'mid-rib-bot', ('mid-rib-bot', zunit)),
    ('Breast_L',       'r-breast', 'r-tit'),
    ('Breast_R',       'l-breast', 'l-tit'),

    ('Penis',          'penis-root', 'penis-tip'),
    ('Scrotum',        'scrotum-root', 'scrotum-tip'),
]

L_UPSPN = L_UPSPNFK+L_UPSPNIK
L_DNSPN = L_DNSPNFK+L_DNSPNIK

BodyArmature = [
    ('MasterFloor',        0, None, F_WIR, L_MAIN, NoBB),

    ('Root',               0, Master, F_WIR, L_UPSPN+L_DNSPNIK, NoBB),
    ('Shoulders',          0, Master, F_WIR, L_UPSPNIK+L_DNSPN, NoBB),

    # Up spine
    ('Hips',               0, 'Root', F_WIR, L_UPSPN, NoBB),
    ('Spine1',             0, 'Root', F_WIR, L_UPSPNFK, NoBB),
    ('Spine2',             0, 'Spine1', F_WIR, L_UPSPNFK, NoBB),
    ('Spine3',             0, 'Spine2', F_WIR, L_UPSPNFK, NoBB),
    ('Neck',               0, 'Spine3', F_WIR, L_UPSPN, NoBB),
    ('Head',               0, 'Neck', F_WIR, L_UPSPN+L_DNSPN+L_HEAD, NoBB),

    ('SpinePT'   ,         0, 'Shoulders', F_WIR, L_UPSPNIK, NoBB),
    ('SpineLinkPT',        0, 'Spine2', F_RES, L_UPSPNIK, NoBB),

    # Down spine
    ('DownNeck',           0, 'Shoulders', F_WIR, L_DNSPN, NoBB),
    ('DownSpine3',         0, 'Shoulders', F_WIR, L_DNSPNFK, NoBB),
    ('DownSpine2',         0, 'DownSpine3', F_WIR, L_DNSPNFK, NoBB),
    ('DownSpine1',         0, 'DownSpine2', F_WIR, L_DNSPNFK, NoBB),
    ('DownHips',           0, 'DownSpine1', F_WIR, L_DNSPN, NoBB),

    #('DownSpinePT'   ,     0, 'Root', F_WIR, L_DNSPNIK, NoBB),
    #('DownSpineLinkPT',    0, 'DownSpine2', F_RES, L_DNSPNIK, NoBB),

    # Help spine
    ('HlpHips',            0, None, 0, L_HELP, NoBB),
    ('HlpSpine1',          0, None, 0, L_HELP, NoBB),
    ('HlpSpine2',          0, None, 0, L_HELP, NoBB),
    ('HlpSpine3',          0, None, 0, L_HELP, NoBB),
    ('HlpNeck',            0, None, 0, L_HELP, NoBB),

    # Deform spine    
    ('DfmHips',            0, 'Root', F_DEF, L_DMAIN, NoBB),
    ('DfmSpine1',          0, 'Root', F_DEF+F_CON, L_DMAIN, (1,1,3) ),
    ('DfmSpine2',          0, 'DfmSpine1', F_DEF+F_CON, L_DMAIN, (1,1,3) ),
    ('DfmSpine3',          0, 'DfmSpine2', F_DEF+F_CON, L_DMAIN, (1,1,3) ),
    ('DfmNeck',            0, 'DfmSpine3', F_DEF+F_CON, L_DMAIN, (1,1,3) ),
    ('DfmHead',            0, 'DfmNeck', F_DEF+F_CON, L_DMAIN, NoBB),

    # Deform torso
    ('DfmRib',             0, 'DfmSpine3', F_DEF, L_DMAIN, NoBB),
    #('RibTarget',          0, 'DfmSpine2', 0, L_HELP, NoBB),
    ('DfmStomach',         0, 'DfmHips', F_DEF, L_DMAIN, NoBB),
    #('HipBone',            0, 'DfmHips', 0, L_HELP, NoBB),

    ('Breast_L',           -45*D, 'DfmRib', F_DEF, L_DEF, NoBB),
    ('Breast_R',           45*D, 'DfmRib', F_DEF, L_DEF, NoBB),
    ('Breathe',            0, 'DfmRib', F_WIR, L_TORSO, NoBB),

    ('Penis',              0, 'DfmHips', F_DEF, L_TORSO, (1,5,1) ),
    ('Scrotum',            0, 'DfmHips', F_DEF, L_TORSO, NoBB),
]

#
#   copyHelp(fp, hlpBone, upBone, downBone):
#

def copyHelp(fp, hlpBone, upBone, downBone):
    addPoseBone(fp, hlpBone, None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
         [('CopyTrans', 0, 1, ['Up', upBone, 0]),
          ('CopyTrans', 0, 0, ['Down', downBone, 0])
         ])

#
#    BodyControlPoses(fp):
#

limBreastRot = (-45*D,45*D, -10*D,10*D, -20*D,20*D)
limBreastScale =  (0.8,1.25, 0.7,1.5, 0.8,1.25)

limHips = (-50*D,40*D, -45*D,45*D, -16*D,16*D)
limSpine1 = (-60*D,90*D, -60*D,60*D, -60*D,60*D)
limSpine2 = (-90*D,70*D, -20*D,20*D, -50*D,50*D)
limSpine3 = (-20*D,20*D, 0,0, -20*D,20*D)
limNeck = (-60*D,40*D, -45*D,45*D, -60*D,60*D)

def BodyControlPoses(fp):
    addPoseBone(fp,  'MasterFloor', 'GZM_Root', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp,  'Root', 'MHHips', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, mhx_rig.rootChildOfConstraints)

    addPoseBone(fp,  'Shoulders', 'GZM_IK_Shoulder', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (0,0, -45*D,45*D, 0,0), (1,1,1)]),
         #('LimitDist', 0, 1, ['LimitDist', 'Root', 'LIMITDIST_INSIDE'])
        ])

    # Up spine

    addPoseBone(fp,  'Hips', 'GZM_CircleHips', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHips, (1,1,1)])])

    addPoseBone(fp,  'Spine1', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), ((1,1,1), (0.2,0.2,0.2)), P_STRETCH, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine1, (1,1,1)])])

    addPoseBone(fp,  'Spine2', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), ((1,1,1), (0.2,0.2,0.2)), P_STRETCH,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine2, (1,1,1)])])

    addPoseBone(fp,  'Spine3', 'GZM_CircleChest', 'Spine', (1,1,1), (0,0,0), (1,1,1), ((1,1,1), (0.96,0.96,0.96)), P_STRETCH,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine3, (1,1,1)]),
          #('IK', 0, 1, ['IK', 'Shoulders', 3, (-90*D, 'SpinePT'), (1,0,1)]),
         ])
         
    addPoseBone(fp,  'Neck', 'MHNeck', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limNeck, (1,1,1)])])

    # Spine IK
    addPoseBone(fp, 'SpinePT', 'MHCube025', 'Spine', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'SpineLinkPT', None, 'Spine', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', 0, 1, ['Stretch', 'SpinePT', 0])])

    # Down spine

    addPoseBone(fp,  'DownHips', 'GZM_CircleHips', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHips, (1,1,1)])])

    addPoseBone(fp,  'DownSpine1', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), ((1,1,1), (0.2,0.2,0.2)), P_STRETCH, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine1, (1,1,1)])])

    addPoseBone(fp,  'DownSpine2', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), ((1,1,1), (0.2,0.2,0.2)), P_STRETCH,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine2, (1,1,1)])])

    addPoseBone(fp,  'DownSpine3', 'GZM_CircleChest', 'Spine', (1,1,1), (0,0,0), (1,1,1), ((1,1,1), (0.96,0.96,0.96)), P_STRETCH,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine3, (1,1,1)]),
          #('IK', 0, 1, ['IK', 'Shoulders', 3, (-90*D, 'SpinePT'), (1,0,1)]),
         ])
         
    addPoseBone(fp,  'DownNeck', 'MHNeck', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limNeck, (1,1,1)])])

    # Help spine
    copyHelp(fp, 'HlpHips', 'Hips', 'DownHips')
    copyHelp(fp, 'HlpSpine1', 'Spine1', 'DownSpine1')
    copyHelp(fp, 'HlpSpine2', 'Spine2', 'DownSpine2')
    copyHelp(fp, 'HlpSpine3', 'Spine3', 'DownSpine3')
    copyHelp(fp, 'HlpNeck', 'Neck', 'DownNeck')
    
   
    # Deform spine
    copyDeform(fp, 'DfmHips', 'HlpHips', 0, U_LOC+U_ROT, None, [])
    copyDeform(fp, 'DfmSpine1', 'HlpSpine1', 0, U_LOC+U_ROT, None, [])
    copyDeform(fp, 'DfmSpine2', 'HlpSpine2', 0, U_ROT, None, [])
    copyDeform(fp, 'DfmSpine3', 'HlpSpine3', 0, U_ROT, None, [])
    copyDeform(fp, 'DfmNeck', 'HlpNeck', 0, U_ROT, None, [])
    copyDeform(fp, 'DfmHead', 'Head', 0, U_ROT, None, [])

    # Head
    addPoseBone(fp,  'Head', 'MHHead', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,40*D, -60*D,60*D, -45*D,45*D), (1,1,1)])])

    # Torso
    addPoseBone(fp,  'DfmStomach',None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', C_STRVOL, 1, ['Stretch', 'DfmRib', 1]),
        ])

    #addPoseBone(fp, 'RibTarget', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])
    #addPoseBone(fp, 'HipBone', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])
    addPoseBone(fp,  'Breathe', 'MHCube01', None, (1,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp,  'Breast_L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, 
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
         ('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])    ])

    addPoseBone(fp,  'Breast_R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
         ('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])    ])

    addPoseBone(fp,  'Penis', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

    addPoseBone(fp,  'Scrotum', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

    return

#
#    BodyShapeDrivers
#    Shape : (driver, channel, coeff)
#

BodyShapeDrivers = {
    'BreatheIn' : ('Breathe', 'LOC_Z', ('0', '2.0')), 
}

#
#    BodyShapeKeyScale = {
#

BodyShapeKeyScale = {
    'BreatheIn'            : ('spine1', 'neck', 1.89623),
    'BicepFlex'            : ('r-uparm-front', 'r-uparm-back', 0.93219),
}

BodySpines = [
    ('Spine', ['Spine1IK', 'Spine2IK', 'Spine3IK', 'Spine4IK', 'Shoulders'])
]



