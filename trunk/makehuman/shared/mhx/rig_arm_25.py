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

prcArmTrg    = 0.15
prcBicepsTail = 0.2

ArmJoints = [
    ('r-shoulder-in',       'v', 14160),
    ('l-shoulder-in',       'v', 14382),
    ('r-uparm0',            'l', ((4.0, 'r-shoulder-in'), (-3.0, 'r-shoulder'))),
    ('l-uparm0',            'l', ((4.0, 'l-shoulder-in'), (-3.0, 'l-shoulder'))),
    #('r-uparm0',            'j', 'r-shoulder'),
    #('l-uparm0',            'j', 'l-shoulder'),
    
    ('r-elbow',             'f', ('r-elbow-raw', 'r-uparm0', 'r-hand', [0,0,-0.1])),
    ('l-elbow',             'f', ('l-elbow-raw', 'l-uparm0', 'l-hand', [0,0,-0.1])),

    ('hand_L_tail',         'j', 'r-finger-3-1'),
    ('hand_R_tail',         'j', 'l-finger-3-1'),

    ('r-uparm1',            'l', ((1-bbMarg, 'r-uparm0'), (bbMarg, 'r-elbow'))),
    ('r-uparm2',            'l', ((bbMarg, 'r-uparm0'), (1-bbMarg, 'r-elbow'))),
    ('r-loarm1',            'l', ((1-bbMarg, 'r-elbow'), (bbMarg, 'r-hand'))),
    ('r-loarm2',            'l', ((bbMarg, 'r-elbow'), (1-bbMarg, 'r-hand'))),

    ('l-uparm1',            'l', ((1-prcArmTrg, 'l-uparm0'), (prcArmTrg, 'l-elbow'))),
    ('l-uparm2',            'l', ((bbMarg, 'l-uparm0'), (1-bbMarg, 'l-elbow'))),
    ('l-loarm1',            'l', ((1-bbMarg, 'l-elbow'), (bbMarg, 'l-hand'))),
    ('l-loarm2',            'l', ((bbMarg, 'l-elbow'), (1-bbMarg, 'l-hand'))),

    ('r-armtrg',            'l', ((1-prcArmTrg, 'r-uparm0'), (prcArmTrg, 'r-elbow'))),
    ('l-armtrg',            'l', ((1-prcArmTrg, 'l-uparm0'), (prcArmTrg, 'l-elbow'))),
    ('r-uparmrot',          'l', ((1-2*prcArmTrg, 'r-uparm0'), (2*prcArmTrg, 'r-elbow'))),
    ('l-uparmrot',          'l', ((1-2*prcArmTrg, 'l-uparm0'), (2*prcArmTrg, 'l-elbow'))),

    ('r-uparm-front',       'v', 3440),
    ('r-uparm-back',        'v', 3438),
    ('r-uparm-over',        'v', 3014),
    ('r-uparm-under',       'v', 3053),

    ('l-uparm-front',       'v', 10175),
    ('l-uparm-back',        'v', 10330),
    ('l-uparm-over',        'v', 10712),
    ('l-uparm-under',       'v', 10678),

    ('r-loarm-mid',         'l', ((0.5, 'r-hand'), (0.5, 'r-elbow'))),
    ('r-loarm-fan',         'l', ((0.25, 'r-hand'), (0.75, 'r-elbow'))),

    ('l-loarm-mid',         'l', ((0.5, 'l-hand'), (0.5, 'l-elbow'))),
    ('l-loarm-fan',         'l', ((0.25, 'l-hand'), (0.75, 'l-elbow'))),

    ('r-elbow-pt',          'o', ('r-elbow', [0,0,-3])),
    ('l-elbow-pt',          'o', ('l-elbow', [0,0,-3])),

    ('r-elbow-head',        'v', 2987),
    ('r-elbow-tail',        'v', 4569),
    ('l-elbow-head',        'v', 10739),
    ('l-elbow-tail',        'v', 9904),
    
    ('r-biceps-head',       'vl', ((0.7, 3441), (0.3, 3469))),
    ('l-biceps-head',       'vl', ((0.7, 10719), (0.3, 10300))),
    ('r-biceps-tail',       'l', ((prcBicepsTail, 'r-hand'), (1-prcBicepsTail, 'r-elbow'))),
    ('l-biceps-tail',       'l', ((prcBicepsTail, 'l-hand'), (1-prcBicepsTail, 'l-elbow'))),
]

ArmHeadsTails = [
    # Arm
    ('ArmTrg_L',            'r-uparm0', 'r-armtrg'),
    ('UpArm_L',             'r-uparm0', 'r-elbow'),
    ('DfmUpArm1_L',         'r-uparm0', 'r-uparm1'),
    ('DfmUpArm2_L',         'r-uparm1', 'r-uparm2'),
    ('DfmUpArm3_L',         'r-uparm2', 'r-elbow'),
    ('Elbow_L',             'r-elbow', ('r-elbow',yunit)),
    ('LoArm_L',             'r-elbow', 'r-hand'),

    ('ArmTrg_R',            'l-uparm0', 'l-armtrg'),
    ('UpArm_R',             'l-uparm0', 'l-elbow'),
    ('DfmUpArm1_R',         'l-uparm0', 'l-uparm1'),
    ('DfmUpArm2_R',         'l-uparm1', 'l-uparm2'),
    ('DfmUpArm3_R',         'l-uparm2', 'l-elbow'),
    ('Elbow_R',             'l-elbow', ('l-elbow',yunit)),
    ('LoArm_R',             'l-elbow', 'l-hand'),

    # Deform
    ('DfmLoArm1_L',         'r-elbow', 'r-loarm1'),
    ('DfmLoArm2_L',         'r-loarm1', 'r-loarm2'),
    ('DfmLoArm3_L',         'r-loarm2', 'r-hand'),
    #('DfmLoArmFan_L',       'r-elbow', 'r-loarm-fan'),
    ('Wrist_L',             'r-hand', 'hand_L_tail'),
    ('Hand_L',              'r-hand', 'hand_L_tail'),
    ('DfmHand_L',           'r-hand', 'hand_L_tail'),

    ('DfmLoArm1_R',         'l-elbow', 'l-loarm1'),
    ('DfmLoArm2_R',         'l-loarm1', 'l-loarm2'),
    ('DfmLoArm3_R',         'l-loarm2', 'l-hand'),
    #('DfmLoArmFan_R',       'l-elbow', 'l-loarm-fan'),
    ('Wrist_R',             'l-hand', 'hand_R_tail'),
    ('Hand_R',              'l-hand', 'hand_R_tail'),
    ('DfmHand_R',           'l-hand', 'hand_R_tail'),

    # Inverse stretching targets
    ('UpArm3Inv_L',         'r-elbow', 'r-uparm2'),
    ('UpArm3Inv_R',         'l-elbow', 'l-uparm2'),
    ('LoArm3Inv_L',         'r-hand', 'r-loarm2'),
    ('LoArm3Inv_R',         'l-hand', 'l-loarm2'),

    #('BendLoArmForward_L',     'r-elbow', ('r-elbow', (0,0,1))),
    #('BendLoArmForward_R',     'l-elbow', ('l-elbow', (0,0,1))),

     # Elbow bend
    ('DfmElbowBend_L',     'r-elbow-head', 'r-elbow-tail'),
    ('ElbowBendTrg_L',     'r-elbow-tail', ('r-elbow-tail', yunit)),
    ('DfmElbowBend_R',     'l-elbow-head', 'l-elbow-tail'),
    ('ElbowBendTrg_R',     'l-elbow-tail', ('l-elbow-tail', yunit)),

   # Pole Targets

    ('UpArmRot_L',         'r-uparm0', 'r-uparmrot'),
    ('UpArmDir_L',         'r-uparm1', ('r-uparm1', yunit)),
    ('UpArm1PT_L',         ('r-uparm1', yunit), ('r-uparm1', ybis)),
    ('UpArm2PT_L',         ('r-uparm2', yunit), ('r-uparm2', ybis)),
    ('LoArmPT_L',          ('r-loarm2', yunit), ('r-loarm2', ybis)),

    ('UpArmRot_R',         'l-uparm0', 'l-uparmrot'),
    ('UpArmDir_R',         'l-uparm1', ('l-uparm1', yunit)),
    ('UpArm1PT_R',         ('l-uparm1', yunit), ('l-uparm1', ybis)),
    ('UpArm2PT_R',         ('l-uparm2', yunit), ('l-uparm2', ybis)),
    ('LoArmPT_R',          ('l-loarm2', yunit), ('l-loarm2', ybis)),

    ('ElbowPT_L',         'r-elbow-pt', ('r-elbow-pt', yunit)),
    ('ElbowPT_R',         'l-elbow-pt', ('l-elbow-pt', yunit)),
    ('ElbowLinkPT_L',     'r-elbow', 'r-elbow-pt'),
    ('ElbowLinkPT_R',     'l-elbow', 'l-elbow-pt'),
    
    # Muscles
    
    ('DfmBiceps_L',       'r-uparm1', 'r-biceps-tail'),
    ('DfmBiceps_R',       'l-uparm1', 'l-biceps-tail'),
    ('BicepsTrg_L',       'r-elbow', 'r-biceps-tail'),
    ('BicepsTrg_R',       'l-elbow', 'l-biceps-tail'),
    
    # Shoulder bone with arm parent
    ('DeltoidTrg1_L',     'r-deltoidtrg', ('r-deltoidtrg', yunit)),
    ('DeltoidTrg1_R',     'l-deltoidtrg', ('l-deltoidtrg', yunit)),
]

"""
    # Rotation diffs
    ('BendArmDown_L',       'r-uparm0', ('r-uparm0', (0,-1,0))),
    ('BendArmDown_R',       'l-uparm0', ('l-uparm0', (0,-1,0))),
    ('BendArmUp_L',         'r-uparm0', ('r-uparm0', (0,1,0))),
    ('BendArmUp_R',         'l-uparm0', ('l-uparm0', (0,1,0))),
    ('BendArmForward_L',    'r-uparm0', ('r-uparm0', (0,0,1))),
    ('BendArmForward_R',    'l-uparm0', ('l-uparm0', (0,0,1))),
    ('BendArmBack_L',       'r-uparm0', ('r-uparm0', (0,0,-1))),
    ('BendArmBack_R',       'l-uparm0', ('l-uparm0', (0,0,-1))),
"""

#upArmRoll = 1.69297
#loArmRoll = 90*D
#handRoll = 1.22173

upArmRoll = 0.0
loArmRoll = 0.0
handRoll = 0.0

#L_LSHOULDER = L_LARMFK+L_LARMIK+L_UPSPNFK+L_UPSPNIK+L_DNSPNFK+L_DNSPNIK
#L_RSHOULDER = L_RARMFK+L_RARMIK+L_UPSPNFK+L_UPSPNIK+L_DNSPNFK+L_DNSPNIK

ArmArmature = [
    # Arm
    ('UpArm_L',            upArmRoll, 'Shoulder_L', F_WIR, L_LARMFK, NoBB),
    ('Elbow_L',            0, Master, F_WIR, L_LTWEAK, NoBB),
    ('LoArm_L',            loArmRoll, 'UpArm_L', F_WIR, L_LARMFK, NoBB),
    ('Wrist_L',            handRoll, Master, F_WIR, L_LARMIK, NoBB),
    ('Hand_L',             handRoll, 'LoArm_L', F_CON+F_WIR, L_LARMFK+L_LARMIK, NoBB),
    ('UpArm_R',            -upArmRoll, 'Shoulder_R', F_WIR, L_RARMFK, NoBB),
    ('Elbow_R',            0, Master, F_WIR, L_RTWEAK, NoBB),
    ('LoArm_R',            -loArmRoll, 'UpArm_R', F_WIR, L_RARMFK, NoBB),
    ('Wrist_R',            handRoll, Master, F_WIR, L_RARMIK, NoBB),
    ('Hand_R',             -handRoll, 'LoArm_R', F_CON+F_WIR, L_RARMFK+L_RARMIK, NoBB),

    #
    ('ArmTrg_L',          0, 'Shoulder_L', 0, L_HELP, NoBB),
    ('UpArmRot_L',        0, 'Shoulder_L', 0, L_LTWEAK, NoBB),
    ('UpArm1PT_L',        0, 'UpArmRot_L', 0, L_HELP, NoBB),
    ('UpArm2PT_L',        0, 'UpArm_L', 0, L_HELP, NoBB),
    ('LoArmPT_L',         0, 'LoArm_L', 0, L_HELP, NoBB),

    ('ArmTrg_R',          0, 'Shoulder_R', 0, L_HELP, NoBB),
    ('UpArmRot_R',        0, 'Shoulder_R', 0, L_RTWEAK, NoBB),
    ('UpArm1PT_R',        0, 'UpArmRot_R', 0, L_HELP, NoBB),
    ('UpArm2PT_R',        0, 'UpArm_R', 0, L_HELP, NoBB),
    ('LoArmPT_R',         0, 'LoArm_R', 0, L_HELP, NoBB),

    # Pole target
    ('ElbowPT_L',         0, None, F_WIR, L_LARMIK, NoBB),
    ('ElbowPT_R',         0, None, F_WIR, L_RARMIK, NoBB),
    ('ElbowLinkPT_L',     0, 'UpArm_L', F_RES, L_LARMIK, NoBB),
    ('ElbowLinkPT_R',     0, 'UpArm_R', F_RES, L_RARMIK, NoBB),

    # Arm deform
    ('DfmUpArm1_L',       upArmRoll, 'Shoulder_L', F_DEF+F_NOSCALE, L_DMAIN, NoBB),
    ('DfmUpArm2_L',       upArmRoll, 'DfmUpArm1_L', F_DEF+F_CON+F_NOSCALE, L_DMAIN,(0,0,5) ),
    ('DfmUpArm3_L',       upArmRoll, 'DfmUpArm2_L', F_DEF+F_CON+F_NOSCALE, L_DMAIN, NoBB),
    ('DfmLoArm1_L',       loArmRoll, 'DfmUpArm3_L', F_DEF+F_NOSCALE, L_DMAIN, NoBB),
    ('DfmLoArm2_L',       loArmRoll, 'DfmLoArm1_L', F_DEF+F_CON+F_NOSCALE, L_DMAIN, (0,0,5) ),
    ('DfmLoArm3_L',       loArmRoll, 'DfmLoArm2_L', F_DEF+F_CON+F_NOSCALE, L_DMAIN, NoBB),
    #('DfmLoArmFan_L',     loArmRoll, 'DfmUpArm2_L', F_DEF, L_DMAIN, NoBB),
    ('DfmHand_L',         handRoll, 'DfmLoArm3_L', F_DEF, L_DMAIN, NoBB),

    ('DfmUpArm1_R',       upArmRoll, 'Shoulder_R', F_DEF+F_NOSCALE, L_DMAIN, NoBB),
    ('DfmUpArm2_R',       upArmRoll, 'DfmUpArm1_R', F_DEF+F_CON+F_NOSCALE, L_DMAIN,(0,0,5) ),
    ('DfmUpArm3_R',       upArmRoll, 'DfmUpArm2_R', F_DEF+F_CON+F_NOSCALE, L_DMAIN, NoBB),
    ('DfmLoArm1_R',       loArmRoll, 'DfmUpArm3_R', F_DEF+F_NOSCALE, L_DMAIN, NoBB),
    ('DfmLoArm2_R',       loArmRoll, 'DfmLoArm1_R', F_DEF+F_CON+F_NOSCALE, L_DMAIN, (0,0,5) ),
    ('DfmLoArm3_R',       loArmRoll, 'DfmLoArm2_R', F_DEF+F_CON+F_NOSCALE, L_DMAIN, NoBB),
    #('DfmLoArmFan_R',     loArmRoll, 'DfmUpArm2_R', F_DEF, L_DMAIN, NoBB),
    ('DfmHand_R',         handRoll, 'DfmLoArm3_R', F_DEF, L_DMAIN, NoBB),
    
    # Muscles
    ('DfmBiceps_L',       0, 'DfmUpArm1_L', F_DEF, L_MSCL, NoBB),
    ('DfmBiceps_R',       0, 'DfmUpArm1_R', F_DEF, L_MSCL, NoBB),    
    ('BicepsTrg_L',       0, 'LoArm_L', 0, L_HELP, NoBB),
    ('BicepsTrg_R',       0, 'LoArm_R', 0, L_HELP, NoBB),

    # Inverse stretching targets
    ('UpArm3Inv_L',       F_NOSCALE, 'UpArm_L', 0, L_HELP, NoBB),
    ('LoArm3Inv_L',       F_NOSCALE, 'LoArm_L', 0, L_HELP, NoBB),
    ('UpArm3Inv_R',       F_NOSCALE, 'UpArm_R', 0, L_HELP, NoBB),
    ('LoArm3Inv_R',       F_NOSCALE, 'LoArm_R', 0, L_HELP, NoBB),

    # Shoulder bone with arm parent
    ('DeltoidTrg1_L',      0, 'UpArm_L', 0, L_HELP, NoBB ),
    ('DeltoidTrg1_R',      0, 'UpArm_R', 0, L_HELP, NoBB ),

]

#
#
#

limUpArm_L = (-90*D,90*D, -100*D,45*D, -90*D,90*D)
limUpArm_R = (-90*D,90*D, -45*D,100*D, -90*D,90*D)

limLoArm_L = (-90*D,90*D, -180*D,45*D, -135*D,0)
limLoArm_R = (-90*D,90*D, -45*D,180*D, 0,135*D)

limHand_L = (-90*D,70*D, 0,0, -20*D,20*D)
limHand_R = (-90*D,70*D, 0,0, -20*D,20*D)

#
#    Rotation modes
#    Dmod = Deform rig mode
#    Cmod = Control rig mode
#

DmodUpArm = P_YXZ
DmodLoArm = P_YXZ
DmodHand = P_YXZ

DmodUpArm = 0
DmodLoArm = 0
DmodHand = 0

CmodUpArm = 0
CmodLoArm = 0
CmodHand = 0

#
#    ArmControlPoses(fp):
#

def ArmControlPoses(fp):

    # Arm
    
    deltaElbow = 0.6*D

    addPoseBone(fp, 'UpArm_L', 'GZM_Circle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), 
            ((1,1,1), (0,0,0), 0.05, None), CmodUpArm, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_L, (True, True, True)]),
         ('IK', 0, 0, ['Elbow', 'Elbow_L', 1, None, (True, False,True)]),
         #('StretchTo', C_STRVOL, 0, ['Elbow', 'Elbow_L', 0, 1]),
        ])

    addPoseBone(fp, 'Elbow_L', 'MHBall025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), CmodLoArm, 
        mhx_rig.rootChildOfConstraints + [
        ('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Clavicle_L', (1,1,1), (1,1,1), (1,1,1)]),
        ('LimitDist', 0, 0, ['DistShoulder', 'Shoulder_L', 'LIMITDIST_ONSURFACE']),
        ])

    addPoseBone(fp, 'LoArm_L', 'GZM_Circle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), 
                ((1,1,1), (0,0,0), 0.05, None), CmodLoArm, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArm_L, (True, True, True)]),
         ('IK', 0, 0, ['ArmIK', 'Wrist_L', 2, (pi-deltaElbow, 'ElbowPT_L'), (True, False,True)]),
         ('IK', 0, 0, ['Wrist', 'Wrist_L', 1, None, (True, False,True)]),
         #('StretchTo', C_STRVOL, 0, ['Wrist', 'Wrist_L', 0, 1]),
        ])

    addPoseBone(fp, 'Wrist_L', 'MHHandCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), CmodHand, 
        mhx_rig.rootChildOfConstraints + [
        ('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Clavicle_L', (1,1,1), (1,1,1), (1,1,1)]),
         ('LimitDist', 0, 0, ['DistShoulder', 'Shoulder_L', 'LIMITDIST_INSIDE']),
         ('LimitDist', 0, 0, ['DistElbow', 'Elbow_L', 'LIMITDIST_ONSURFACE']),
        ])

    addPoseBone(fp, 'Hand_L', 'MHHand', 'FK_L', (0,0,0), (0,1,0), (1,1,1), (1,1,1), CmodHand,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_L, (True, True, True)]),
         ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,False)]),
         ('CopyLoc', 0, 0, ['WristLoc', 'Wrist_L', (1,1,1), (0,0,0), 0, False]),
         ('CopyRot', 0, 0, ['WristRot', 'Wrist_L', (1,1,1), (0,0,0), False])
        ])
        

    addPoseBone(fp, 'UpArm_R', 'GZM_Circle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), 
            ((1,1,1), (0,0,0), 0.05, None), CmodUpArm, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_R, (True, True, True)]),
         #('StretchTo', C_STRVOL, 0, ['Elbow', 'Elbow_R', 0, 1]),
         ('IK', 0, 0, ['Elbow', 'Elbow_R', 1, None, (True, False,True)]),
        ])

    addPoseBone(fp, 'Elbow_R', 'MHBall025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), CmodLoArm, 
        mhx_rig.rootChildOfConstraints + [
        ('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Clavicle_R', (1,1,1), (1,1,1), (1,1,1)]),
        ('LimitDist', 0, 0, ['DistShoulder', 'Shoulder_R', 'LIMITDIST_ONSURFACE']),
        ])

    addPoseBone(fp, 'LoArm_R', 'GZM_Circle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), 
            ((1,1,1), (0,0,0), 0.05, None), CmodLoArm, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArm_R, (True, True, True)]),
         ('IK', 0, 0, ['ArmIK', 'Wrist_R', 2, (deltaElbow, 'ElbowPT_R'), (True, False,True)]),
         ('IK', 0, 0, ['Wrist', 'Wrist_R', 1, None, (True, False,True)]),
         #('StretchTo', C_STRVOL, 0, ['Wrist', 'Wrist_R', 0, 1]),
        ])

    addPoseBone(fp, 'Wrist_R', 'MHHandCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), CmodHand, 
        mhx_rig.rootChildOfConstraints + [
        ('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Clavicle_R', (1,1,1), (1,1,1), (1,1,1)]),
        ('LimitDist', 0, 0, ['DistShoulder', 'Shoulder_R', 'LIMITDIST_INSIDE']),
        ('LimitDist', 0, 0, ['DistElbow', 'Elbow_R', 'LIMITDIST_ONSURFACE']),
        ])

    addPoseBone(fp, 'Hand_R', 'MHHand', 'FK_R', (0,0,0), (0,1,0), (1,1,1), (1,1,1), CmodHand,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_R, (True, True, True)]),
         ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,False)]),
         ('CopyLoc', 0, 0, ['WristLoc', 'Wrist_R', (1,1,1), (0,0,0), 0, False]),
         ('CopyRot', 0, 0, ['WristRot', 'Wrist_R', (1,1,1), (0,0,0), False])
        ])


    addPoseBone(fp, 'ElbowPT_L', 'MHCube025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
        [('ChildOf', C_CHILDOF, 0, ['Hand', 'Wrist_L', (1,1,1), (1,1,1), (1,1,1)]),
         ('ChildOf', C_CHILDOF, 1, ['Shoulder', 'Clavicle_L', (1,1,1), (1,1,1), (1,1,1)]) ])

    addPoseBone(fp, 'ElbowLinkPT_L', None, 'IK_L', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ElbowPT_L', 0, 1])])

    addPoseBone(fp, 'ArmTrg_L', None, 'FK_L', (1,1,1), (1,0,1), (1,1,1), (1,1,1), P_YXZ, 
         [('IK', 0, 1, ['ArmIK', 'LoArm_L', 1, None, (True, False,True)])])

    addPoseBone(fp, 'UpArmRot_L', 'MHCircle05', None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 1, ['ArmIK', 'LoArm_L', 1, None, (True, False,True)]),
         #('CopyRot', C_LOCAL, 0.45, ['Rot', 'UpArm_L', (0,1,0), (0,0,0), False])
        ])

    addPoseBone(fp, 'ElbowPT_R', 'MHCube025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
        [('ChildOf', C_CHILDOF, 0, ['Hand', 'Wrist_R', (1,1,1), (1,1,1), (1,1,1)]),
         ('ChildOf', C_CHILDOF, 1, ['Shoulder', 'Clavicle_R', (1,1,1), (1,1,1), (1,1,1)]) ])

    addPoseBone(fp, 'ElbowLinkPT_R', None, 'IK_R', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ElbowPT_R', 0, 1])])

    addPoseBone(fp, 'ArmTrg_R', 'MHCircle05', 'FK_R', (1,1,1), (1,0,1), (1,1,1), (1,1,1), P_YXZ, 
         [('IK', 0, 1, ['ArmIK', 'LoArm_R', 1, None, (True, False,True)])])

    addPoseBone(fp, 'UpArmRot_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 1, ['ArmIK', 'LoArm_R', 1, None, (True, False,True)]),
         #('CopyRot', C_LOCAL, 0.45, ['Rot', 'UpArm_R', (0,1,0), (0,0,0), False])
        ])

    deltaUpArm = 3*D
    deltaLoArm = 0*D
    
    # Arm deform
    
    copyDeformPartial(fp, 'DfmUpArm1_L', 'UpArm_L', (1,0,1), DmodUpArm, U_LOC, None, 
        [('IK', 0, 1, ['IK', 'LoArm_L', 1, (90*D-deltaUpArm, 'UpArm1PT_L'), (True, False,True)])])
    
    copyDeformPartial(fp, 'DfmUpArm2_L', 'UpArm_L', (1,1,1), DmodUpArm, U_ROT, None, 
        [('StretchTo', 0, 1, ['Stretch', 'UpArm3Inv_L', 1, 1])])
        
    copyDeformPartial(fp, 'DfmUpArm3_L', 'UpArm_L', (0,1,0), DmodUpArm, 0, None, 
        [('IK', 0, 1, ['IK', 'LoArm_L', 1, (90*D-deltaUpArm, 'UpArm2PT_L'), (True, False,True)])])

    copyDeformPartial(fp, 'DfmLoArm1_L', 'LoArm_L', (1,0,1), DmodLoArm, U_LOC, None,
        [('IK', 0, 1, ['IK', 'Hand_L', 1, None, (True, False,True)])])
    
    copyDeformPartial(fp, 'DfmLoArm2_L', 'LoArm_L', (1,1,1), DmodLoArm, 0, None, 
        [('StretchTo', 0, 1, ['Stretch', 'LoArm3Inv_L', 1, 1])])
        
    copyDeformPartial(fp, 'DfmLoArm3_L', 'LoArm_L', (0,1,0), DmodLoArm, 0, None,
        [('IK', 0, 1, ['IK', 'Hand_L', 1, (90*D-deltaLoArm, 'LoArmPT_L'), (True, False,True)])])
        
    #addPoseBone(fp, 'DfmLoArmFan_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), DmodLoArm, 
    #    [('CopyRot', 0, 0.5, ['Rot', 'LoArm_L', (1,1,1), (0,0,0), False])])
    
    copyDeform(fp, 'DfmHand_L', 'Hand_L', DmodHand, U_LOC+U_ROT, None, [])


    copyDeformPartial(fp, 'DfmUpArm1_R', 'UpArm_R', (1,1,1), DmodUpArm, U_LOC, None, 
        [('IK', 0, 1, ['IK', 'LoArm_R', 1, (90*D+deltaUpArm, 'UpArm1PT_R'), (True, False,True)])])
    
    copyDeformPartial(fp, 'DfmUpArm2_R', 'UpArm_R', (1,1,1), DmodUpArm, 0, None,
        [('StretchTo', 0, 1, ['Stretch', 'UpArm3Inv_R', 1, 1])])    
        
    copyDeformPartial(fp, 'DfmUpArm3_R', 'UpArm_R', (0,1,0), DmodUpArm, 0, None,
        [('IK', 0, 1, ['IK', 'LoArm_R', 1, (90*D+deltaUpArm, 'UpArm2PT_R'), (True, False,True)])])

    copyDeformPartial(fp, 'DfmLoArm1_R', 'LoArm_R', (1,0,1), DmodLoArm, U_LOC, None, 
        [('IK', 0, 1, ['IK', 'Hand_R', 1, None, (True, False,True)])])
    
    copyDeformPartial(fp, 'DfmLoArm2_R', 'LoArm_R', (1,1,1), DmodLoArm, 0, None,
        [('StretchTo', 0, 1, ['Stretch', 'LoArm3Inv_R', 1, 1])])
        
    copyDeformPartial(fp, 'DfmLoArm3_R', 'LoArm_R', (0,1,0), DmodLoArm, 0, None,
        [('IK', 0, 1, ['IK', 'Hand_R', 1, (90*D+deltaLoArm, 'LoArmPT_R'), (True, False,True)])])
        
    #addPoseBone(fp, 'DfmLoArmFan_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), DmodLoArm,
    #    [('CopyRot', 0, 0.5, ['Rot', 'LoArm_R', (1,1,1), (0,0,0), False])])
    
    copyDeform(fp, 'DfmHand_R', 'Hand_R', DmodHand, U_LOC+U_ROT, None, [])
    
    # Muscles

    addPoseBone(fp, 'DfmBiceps_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'BicepsTrg_L', 1, 1])])

    addPoseBone(fp, 'DfmBiceps_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'BicepsTrg_R', 1, 1])])

    return
    
#
#    ArmWriteActions(fp)
#

def ArmWriteActions(fp):
    return

#
#    ArmFKIKDrivers
#    (Bone, FK constraint, IK constraint, driver, channel, max)
#
"""
ArmFKIKDrivers = [
    ("UpArm_L", True, [], [], "PArmIK_L", "LOC_X", 1.0),
    ("LoArm_L", True, [], ["ArmIK"], "PArmIK_L", "LOC_X", 1.0),
    ("Hand_L", True, ["FreeIK"], ["WristLoc", "WristRot"], "PArmIK_L", "LOC_X", 1.0),

    ("UpArm_R", True, [], [], "PArmIK_R", "LOC_X", 1.0),
    ("LoArm_R", True, [], ["ArmIK"], "PArmIK_R", "LOC_X", 1.0),
    ("Hand_R", True, ["FreeIK"], ["WristLoc", "WristRot"], "PArmIK_R", "LOC_X", 1.0),
]
"""
#
#   ArmPropLRDrivers
#   (Bone, Name, Props, Expr)
#

ArmPropLRDrivers = [
    ('UpArm', 'Elbow', ['ElbowPlant'], 'x1'),
    ('Elbow', 'DistShoulder', ['ArmStretch', 'ElbowPlant'], '(1-x1)*x2'),
    ('LoArm', 'ArmIK', ['ArmIk', 'ElbowPlant'], 'x1*(1-x2)'),
    ('LoArm', 'Wrist', ['ArmIk', 'ElbowPlant'], 'x1*x2'),
    ('Wrist', 'DistShoulder', ['ArmStretch', 'ElbowPlant'], '(1-x1)*(1-x2)'),
    ('Wrist', 'DistElbow', ['ArmStretch', 'ElbowPlant'], '(1-x1)*x2'),
    ('Hand', 'FreeIK', ['ArmIk', 'ElbowPlant'], '(1-x1)*(1-x2)'),
    ('Hand', 'WristLoc', ['ArmIk'], 'x1'),
    ('Hand', 'WristRot', ['ArmIk', 'HandFollowsWrist'], 'x1*x2'),
    ('Shoulder', 'Shoulder', ['ArmHinge'], '1-x1'),
    ('Shoulder', 'Root', ['ArmHinge'], 'x1'),
    ('ElbowPT', 'Hand', ['ElbowFollowsWrist'], 'x1'),
    ('ElbowPT', 'Shoulder', ['ElbowFollowsWrist'], '1-x1'),
]

ArmPropDrivers = [
    ('UpArm_L', 'LimitRot', ['RotationLimits'], 'x1'),
    ('LoArm_L', 'LimitRot', ['RotationLimits'], 'x1'),    
    ('Hand_L', 'LimitRot', ['RotationLimits'], 'x1'),
    ('UpArm_R', 'LimitRot', ['RotationLimits'], 'x1'),
    ('LoArm_R', 'LimitRot', ['RotationLimits'], 'x1'),    
    ('Hand_R', 'LimitRot', ['RotationLimits'], 'x1'),
 ]

#
#    ArmDeformDrivers
#    (Bone, constraint, driver, rotdiff, keypoints)
#

ArmDeformDrivers = []

#
#    ArmShapeDrivers
#    Shape : (driver, rotdiff, keypoints)
#

ArmShapeDrivers = {}
'''
    'BicepFlex_L' : ( 'LoArm1_L', 'BendLoArmForward_L',  [(0,1), (90*D,0)] ),
    'BicepFlex_R' : ( 'LoArm1_R', 'BendLoArmForward_R',  [(0,1), (90*D,0)] ),
}
'''


