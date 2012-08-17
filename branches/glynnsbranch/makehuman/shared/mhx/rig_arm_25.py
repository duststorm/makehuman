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
from mhx_rig import addPoseBone, copyDeform, copyDeformPartial

prcUpArmVec    = 0.15
offs = (0,0.6,0)

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

    ('r-uparm1',            'l', ((0.67, 'r-uparm0'), (0.33, 'r-elbow'))),
    ('r-uparm2',            'l', ((0.33, 'r-uparm0'), (0.67, 'r-elbow'))),
    ('r-loarm1',            'l', ((0.67, 'r-elbow'), (0.33, 'r-hand'))),
    ('r-loarm2',            'l', ((0.33, 'r-elbow'), (0.67, 'r-hand'))),

    ('l-uparm1',            'l', ((0.67, 'l-uparm0'), (0.33, 'l-elbow'))),
    ('l-uparm2',            'l', ((0.33, 'l-uparm0'), (0.67, 'l-elbow'))),
    ('l-loarm1',            'l', ((0.67, 'l-elbow'), (0.33, 'l-hand'))),
    ('l-loarm2',            'l', ((0.33, 'l-elbow'), (0.67, 'l-hand'))),

    #('r-armtrg',            'l', ((1-prcUpArmVec, 'r-uparm0'), (prcUpArmVec, 'r-elbow'))),
    #('l-armtrg',            'l', ((1-prcUpArmVec, 'l-uparm0'), (prcUpArmVec, 'l-elbow'))),
    ('r-armtrg',            'o', ('r-uparm0', [1,0,0])),
    ('l-armtrg',            'o', ('l-uparm0', [-1,0,0])),
    
    ('r-uparmrot',          'l', ((1-2*prcUpArmVec, 'r-uparm0'), (2*prcUpArmVec, 'r-elbow'))),
    ('l-uparmrot',          'l', ((1-2*prcUpArmVec, 'l-uparm0'), (2*prcUpArmVec, 'l-elbow'))),

    ('r-elbow-pt',          'o', ('r-elbow', [0,0,-3])),
    ('l-elbow-pt',          'o', ('l-elbow', [0,0,-3])),

    ('r-elbow-head',        'v', 2987),
    ('r-elbow-tail',        'v', 4569),
    ('l-elbow-head',        'v', 10739),
    ('l-elbow-tail',        'v', 9904),
    
]

"""
if MuscleBones:
    ArmJoints += [    
    ('r-loarm-fan',         'l', ((0.25, 'r-hand'), (0.75, 'r-elbow'))),
    ('l-loarm-fan',         'l', ((0.25, 'l-hand'), (0.75, 'l-elbow'))),

    ('r-elbow-compress1',     'l', ((0.5, 'r-elbow'), (0.5, 'r-uparm0'))),
    ('r-elbow-compress2',     'l', ((0.5, 'r-elbow'), (0.5, 'r-hand'))),
    ('l-elbow-compress1',     'l', ((0.5, 'l-elbow'), (0.5, 'l-uparm0'))),
    ('l-elbow-compress2',     'l', ((0.5, 'l-elbow'), (0.5, 'l-hand'))),
    
]
"""

ArmHeadsTails = [
    # Upper arm
    ('UpArmVec_L',            'r-uparm0', 'r-armtrg'),
    ('UpArmVecPos_L',         'r-uparm0', 'r-armtrg'),
    ('UpArmVecNeg_L',         'r-uparm0', 'r-armtrg'),
    ('UpArm_L',             'r-uparm0', 'r-elbow'),
    ('UpArmIK_L',           'r-uparm0', 'r-elbow'),
    #('UpArmRot_L',          'r-uparm0', 'r-uparm1'),
    ('DfmUpArm_L',          'r-uparm0', 'r-elbow'),

    ('UpArmVec_R',            'l-uparm0', 'l-armtrg'),
    ('UpArmVecPos_R',         'l-uparm0', 'l-armtrg'),
    ('UpArmVecNeg_R',         'l-uparm0', 'l-armtrg'),
    ('UpArm_R',             'l-uparm0', 'l-elbow'),
    ('UpArmIK_R',           'l-uparm0', 'l-elbow'),
    #('UpArmRot_R',          'l-uparm0', 'l-uparm1'),
    ('DfmUpArm_R',          'l-uparm0', 'l-elbow'),

    # Lower arm
    ('LoArmVec_L',          'r-elbow', 'r-loarm1'),
    ('LoArm_L',             'r-elbow', 'r-hand'),
    ('LoArmIK_L',           'r-elbow', 'r-hand'),
    ('LoArmRot_L',          'r-elbow', 'r-loarm1'),
    ('HlpLoArm_L',          'r-elbow', 'r-hand'),
    ('DfmLoArm1_L',         'r-elbow', 'r-loarm1'),
    ('DfmLoArm2_L',         'r-loarm1', 'r-loarm2'),
    ('DfmLoArm3_L',         'r-loarm2', 'r-hand'),

    ('LoArmVec_R',          'l-elbow', 'l-loarm1'),
    ('LoArm_R',             'l-elbow', 'l-hand'),
    ('LoArmIK_R',           'l-elbow', 'l-hand'),
    ('LoArmRot_R',          'l-elbow', 'l-loarm1'),
    ('HlpLoArm_R',          'l-elbow', 'l-hand'),
    ('DfmLoArm1_R',         'l-elbow', 'l-loarm1'),
    ('DfmLoArm2_R',         'l-loarm1', 'l-loarm2'),
    ('DfmLoArm3_R',         'l-loarm2', 'l-hand'),
    
    # Hand
    ('Wrist_L',             'r-hand', 'hand_L_tail'),
    ('Hand_L',              'r-hand', 'hand_L_tail'),
    ('DfmHand_L',           'r-hand', 'hand_L_tail'),
    ('Wrist_R',             'l-hand', 'hand_R_tail'),
    ('Hand_R',              'l-hand', 'hand_R_tail'),
    ('DfmHand_R',           'l-hand', 'hand_R_tail'),


   # Pole Targets

    ('UpArmDir_L',         'r-uparm1', ('r-uparm1', the.yunit)),
    ('UpArmDir_R',         'l-uparm1', ('l-uparm1', the.yunit)),

    ('LoArm2PT_L',         ('r-loarm1', the.yunit), ('r-loarm1', ybis)),
    ('LoArm3PT_L',         ('r-loarm2', the.yunit), ('r-loarm2', ybis)),
    ('LoArm2PT_R',         ('l-loarm1', the.yunit), ('l-loarm1', ybis)),
    ('LoArm3PT_R',         ('l-loarm2', the.yunit), ('l-loarm2', ybis)),

    ('ElbowPT_L',         'r-elbow-pt', ('r-elbow-pt', offs)),
    ('ElbowPT_R',         'l-elbow-pt', ('l-elbow-pt', offs)),
    ('ElbowPTFK_L',       'r-elbow-pt', ('r-elbow-pt', offs)),
    ('ElbowPTFK_R',       'l-elbow-pt', ('l-elbow-pt', offs)),
    ('ElbowLinkPT_L',     'r-elbow', 'r-elbow-pt'),
    ('ElbowLinkPT_R',     'l-elbow', 'l-elbow-pt'),   
    
    # Directions
    
    #('DirUpArm_L',           'r-uparm0', ('r-uparm0', (1,0,0))),
    #('DirUpArm_R',           'l-uparm0', ('l-uparm0', (-1,0,0))),

    ('DirElbowFwd_L',        'r-elbow', ('r-elbow', (0,0,1))),
    ('DirElbowFwd_R',        'l-elbow', ('l-elbow', (0,0,1))),
    ('DirElbowInv_L',        'r-elbow', ('r-elbow', (-1,0,0))),
    ('DirElbowInv_R',        'l-elbow', ('l-elbow', (1,0,0))),
]

if MuscleBones:
    ArmHeadsTails = [
     # Elbow bend
    ('DfmElbowBend_L',     'r-elbow-head', 'r-elbow-tail'),
    ('ElbowBendTrg_L',     'r-elbow-tail', ('r-elbow-tail', the.yunit)),
    ('DfmElbowBend_R',     'l-elbow-head', 'l-elbow-tail'),
    ('ElbowBendTrg_R',     'l-elbow-tail', ('l-elbow-tail', the.yunit)),

    # Elbow deform
    ('DfmLoArmFan_L',       'r-elbow', 'r-loarm-fan'),
    ('DfmLoArmFan_R',       'l-elbow', 'l-loarm-fan'),

    ('DfmElbowCompress_L', 'r-elbow-compress1', 'r-elbow-compress2'),
    ('ElbowCompressTrg_L', 'r-elbow-compress2', ('r-elbow-compress2', the.yunit)),
    ('DfmElbowCompress_R', 'l-elbow-compress1', 'l-elbow-compress2'),
    ('ElbowCompressTrg_R', 'l-elbow-compress2', ('l-elbow-compress2', the.yunit)),
]


#upArmRoll = 1.69297
#loArmRoll = 90*D
#handRoll = 1.22173

upArmRoll = 0.0
loArmRoll = 0.0
handRoll = 0.0

ArmArmature = [
    # Arm
    ('UpArm_L',            upArmRoll, 'UpArmHinge_L', F_WIR, L_LARMFK, NoBB),
    ('LoArm_L',            loArmRoll, 'UpArm_L', F_WIR+F_SCALE, L_LARMFK, NoBB),
    ('Hand_L',             handRoll, 'LoArm_L', F_CON+F_WIR, L_LARMFK+L_LEXTRA, NoBB),
    
    ('UpArm_R',            -upArmRoll, 'UpArmHinge_R', F_WIR, L_RARMFK, NoBB),
    ('LoArm_R',            -loArmRoll, 'UpArm_R', F_WIR+F_SCALE, L_RARMFK, NoBB),
    ('Hand_R',             -handRoll, 'LoArm_R', F_CON+F_WIR, L_RARMFK+L_REXTRA, NoBB),
    
    # IK arm
    ('UpArmIK_L',          upArmRoll, 'UpArmHinge_R', 0, L_HELP, NoBB),
    ('LoArmIK_L',          loArmRoll, 'UpArmIK_L', F_CON, L_HELP, NoBB),
    ('HlpLoArm_L',         loArmRoll, 'UpArm_L', F_NOROT+F_CON+F_WIR, L_HELP, NoBB),
    ('Wrist_L',            handRoll, Master, F_WIR, L_LARMIK, NoBB),

    ('UpArmIK_R',          -upArmRoll, 'UpArmHinge_R', 0, L_HELP, NoBB),
    ('LoArmIK_R',          -loArmRoll, 'UpArmIK_R', F_CON, L_HELP, NoBB),
    ('HlpLoArm_R',         -loArmRoll, 'UpArm_R', F_NOROT+F_CON+F_WIR, L_HELP, NoBB),
    ('Wrist_R',            handRoll, Master, F_WIR, L_RARMIK, NoBB),
    
     # Arm targets
    ('UpArmVec_L',          0, 'UpArmSocket_L', 0, L_HELP, NoBB),
    ('UpArmVec_R',          0, 'UpArmSocket_R', 0, L_HELP, NoBB),
    ('UpArmVecPos_L',       60*D, 'UpArmSocket_L', 0, L_HELP, NoBB),
    ('UpArmVecPos_R',       -60*D, 'UpArmSocket_R', 0, L_HELP, NoBB),
    ('UpArmVecNeg_L',       -60*D, 'UpArmSocket_L', 0, L_HELP, NoBB),
    ('UpArmVecNeg_R',       60*D, 'UpArmSocket_R', 0, L_HELP, NoBB),

    ('LoArmVec_L',        0, 'UpArm_L', 0, L_HELP, NoBB),
    ('LoArmVec_R',        0, 'UpArm_R', 0, L_HELP, NoBB),
    
    # Pole target
    ('ElbowPT_L',         0, (None, 'UpArmSocket_L'), F_WIR, L_LARMIK, NoBB),
    ('ElbowPT_R',         0, (None, 'UpArmSocket_R'), F_WIR, L_RARMIK, NoBB),
    ('ElbowPTFK_L',       0, 'UpArm_L', 0, L_HELP, NoBB),
    ('ElbowPTFK_R',       0, 'UpArm_R', 0, L_HELP, NoBB),
    ('ElbowLinkPT_L',     0, 'UpArm_L', F_RES, L_LARMIK, NoBB),
    ('ElbowLinkPT_R',     0, 'UpArm_R', F_RES, L_RARMIK, NoBB),

    # Arm deform
    #('UpArmRot_L',        upArmRoll, 'UpArm_L', F_WIR, L_TWEAK, NoBB),
    ('DfmUpArm_L',        upArmRoll, 'UpArm_L', F_DEF, L_DMAIN, NoBB),
    ('LoArmRot_L',        loArmRoll, 'UpArm_L', F_WIR, L_TWEAK, NoBB),
    ('DfmLoArm1_L',       loArmRoll, 'LoArmRot_L', F_DEF, L_DMAIN, NoBB),
    ('DfmLoArm2_L',       loArmRoll, 'DfmLoArm1_L', F_DEF+F_SCALE, L_DMAIN, NoBB ),
    ('DfmLoArm3_L',       loArmRoll, 'LoArm_L', F_DEF, L_DMAIN, NoBB),
    ('DfmHand_L',         handRoll, 'LoArm_L', F_DEF, L_DMAIN, NoBB),

    #('UpArmRot_R',        upArmRoll, 'UpArm_R', F_WIR, L_TWEAK, NoBB),
    ('DfmUpArm_R',        upArmRoll, 'UpArm_R', F_DEF, L_DMAIN, NoBB),
    ('LoArmRot_R',        loArmRoll, 'UpArm_R', F_WIR, L_TWEAK, NoBB),
    ('DfmLoArm1_R',       loArmRoll, 'LoArmRot_R', F_DEF, L_DMAIN, NoBB),
    ('DfmLoArm2_R',       loArmRoll, 'DfmLoArm1_R', F_DEF+F_SCALE, L_DMAIN, NoBB ),
    ('DfmLoArm3_R',       loArmRoll, 'LoArm_R', F_DEF, L_DMAIN, NoBB),
    ('DfmHand_R',         handRoll, 'LoArm_R', F_DEF, L_DMAIN, NoBB),
    
    # Pole targets
    ('LoArm2PT_L',        0, 'DfmLoArm1_L', 0, L_HELP, NoBB),
    ('LoArm3PT_L',        0, 'HlpLoArm_L', 0, L_HELP, NoBB),
    ('LoArm2PT_R',        0, 'DfmLoArm1_R', 0, L_HELP, NoBB),
    ('LoArm3PT_R',        0, 'HlpLoArm_R', 0, L_HELP, NoBB),
    
    # Directions
    #('DirUpArm_L',         0, 'UpArm_L', 0, L_HELP, NoBB),
    #('DirUpArm_R',         0, 'UpArm_R', 0, L_HELP, NoBB),

    ('DirElbowFwd_L',       0*D, 'UpArm_L', 0, L_HELP, NoBB),
    ('DirElbowFwd_R',       0*D, 'UpArm_R', 0, L_HELP, NoBB),
    ('DirElbowInv_L',       0*D, 'UpArm_L', 0, L_HELP, NoBB),
    ('DirElbowInv_R',       0*D, 'UpArm_R', 0, L_HELP, NoBB),

]

if MuscleBones:
    ArmArmature += [
    # Elbow deform
    ('DfmLoArmFan_L',     loArmRoll, 'UpArm_L', F_DEF, L_DMAIN, NoBB),
    ('DfmLoArmFan_R',     loArmRoll, 'UpArm_R', F_DEF, L_DMAIN, NoBB),
    ('DfmElbowCompress_L',       0, 'DfmUpArm3_L', F_DEF, L_DEF, NoBB),
    ('ElbowCompressTrg_L',       0, 'DfmLoArm1_L', 0, L_HELP, NoBB),
    ('DfmElbowCompress_R',       0, 'DfmUpArm3_R', F_DEF, L_DEF, NoBB),
    ('ElbowCompressTrg_R',       0, 'DfmLoArm1_R', 0, L_HELP, NoBB),
]

#
#
#

#limUpArm_L = (-135*D,135*D, -120*D,90*D, -135*D,135*D)
#limUpArm_R = (-135*D,135*D, -90*D,120*D, -135*D,135*D)
limUpArm_L = (-135*D,135*D, -60*D,60*D, -135*D,135*D)
limUpArm_R = (-135*D,135*D, -60*D,60*D, -135*D,135*D)

limLoArm_L = (-10*D,10*D, -178*D,150*D, -175*D,10*D)
limLoArm_R = (-10*D,10*D, -150*D,178*D, -10*D,175*D)

limHand_L = (-90*D,70*D, -10*D,10*D, -20*D,20*D)
limHand_R = (-90*D,70*D, -10*D,10*D, -20*D,20*D)


#
#    ArmControlPoses(fp):
#

def ArmControlPoses(fp):

    # Arm
    
    deltaElbow = 0.6*D
    deltaWrist = 0.0*D

    addPoseBone(fp, 'UpArm_L', 'GZM_Circle025', 'FK_L', (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_L, (True, True, True)]),
         #('CopyTrans', 0, 0, ['ArmIK', 'UpArmIK_L', 0]),
         ('IK', 0, 0, ['ArmIK', 'LoArmIK_L', 1, None, (True, False,False)]),
         ('CopyTrans', 0, 0, ['Elbow', 'ELUpArm_L', 0])
        ])

    addPoseBone(fp, 'LoArm_L', 'GZM_Circle025', 'FK_L', (1,1,1), (1,0,0), (1,0,1), (1,1,1), P_YXZ, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArm_L, (True, True, True)]),
         #('CopyTrans', 0, 0, ['ArmIK', 'LoArmIK_L', 0]),
         ('IK', 0, 0, ['ArmIK', 'Wrist_L', 1, None, (True, False,False)]),
         ('IK', 0, 0, ['Wrist', 'Wrist_L', 1, None, (True, False,False)]),
        ])

    addPoseBone(fp, 'Hand_L', 'MHHand', 'FK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_L, (True, True, True)]),
         ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,False)]),
         ('CopyLoc', 0, 0, ['WristLoc', 'Wrist_L', (1,1,1), (0,0,0), 0, False]),
         ('CopyRot', 0, 0, ['WristRot', 'Wrist_L', (1,1,1), (0,0,0), False])
        ])
        
        
    addPoseBone(fp, 'UpArm_R', 'GZM_Circle025', 'FK_R', (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpArm_R, (True, True, True)]),
         #('CopyTrans', 0, 0, ['ArmIK', 'UpArmIK_R', 0]),
         ('IK', 0, 0, ['ArmIK', 'LoArmIK_R', 1, None, (True, False,False)]),
         ('CopyTrans', 0, 0, ['Elbow', 'ELUpArm_R', 0])
        ])

    addPoseBone(fp, 'LoArm_R', 'GZM_Circle025', 'FK_R', (1,1,1), (1,0,0), (1,0,1), (1,1,1), P_YXZ, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoArm_R, (True, True, True)]),
         #('CopyTrans', 0, 0, ['ArmIK', 'LoArmIK_R', 0]),
         ('IK', 0, 0, ['ArmIK', 'Wrist_R', 1, None, (True, False,False)]),
         ('IK', 0, 0, ['Wrist', 'Wrist_R', 1, None, (True, False,False)]),
        ])

    addPoseBone(fp, 'Hand_R', 'MHHand', 'FK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHand_R, (True, True, True)]),
         ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,False)]),
         ('CopyLoc', 0, 0, ['WristLoc', 'Wrist_R', (1,1,1), (0,0,0), 0, False]),
         ('CopyRot', 0, 0, ['WristRot', 'Wrist_R', (1,1,1), (0,0,0), False])
        ])

    # IK arm
    
    addPoseBone(fp, 'UpArmIK_L', None, 'IK_L', (1,1,1), (0,0,0), (1,1,1), 
            ((1,1,1), (0,0,0), 0.05, limUpArm_L), 0, [])

    addPoseBone(fp, 'LoArmIK_L', None, 'IK_L', (1,1,1), (0,0,0), (1,1,1), 
                ((0,1,1), (0,0,0), 0.05, limLoArm_L), 0, 
        [('IK', 0, 1, ['ArmIK', 'Wrist_L', 2, (pi-deltaElbow, 'ElbowPT_L'), (True, False,False)]),
         ])

    addPoseBone(fp, 'HlpLoArm_L', 'GZM_Circle025', 'IK_L', (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, 
        [('CopyTrans', 0, 1, ['Arm', 'LoArm_L', 0]),
         ('CopyRot', C_LOCAL, 0, ['WristRot', 'Wrist_L', (0,1,0), (0,0,0), False]),
        ])

    addPoseBone(fp, 'Wrist_L', 'MHHandCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Clavicle_L', (1,1,1), (1,1,1), (1,1,1)]),
         ('LimitDist', 0, 0, ['DistShoulder', 'Shoulder_L', 'LIMITDIST_INSIDE']),
         ('LimitDist', 0, 0, ['DistElbow', 'Elbow_L', 'LIMITDIST_ONSURFACE']),
        ])

    addPoseBone(fp, 'UpArmIK_R', None, 'IK_R', (1,1,1), (0,0,0), (1,1,1), 
            ((1,1,1), (0,0,0), 0.05, limUpArm_R), 0, [])

    addPoseBone(fp, 'LoArmIK_R', None, 'IK_R', (1,1,1), (0,0,0), (1,1,1), 
            ((0,1,1), (0,0,0), 0.05, limLoArm_R), 0, 
        [('IK', 0, 1, ['ArmIK', 'Wrist_R', 2, (deltaElbow, 'ElbowPT_R'), (True, False,False)]),        
        ])

    addPoseBone(fp, 'HlpLoArm_R', 'GZM_Circle025', 'IK_R', (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, 
        [('CopyTrans', 0, 1, ['Arm', 'LoArm_R', 0]),
         ('CopyRot', C_LOCAL, 0, ['WristRot', 'Wrist_R', (0,1,0), (0,0,0), False]),
        ])

    addPoseBone(fp, 'Wrist_R', 'MHHandCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('ChildOf', C_CHILDOF, 0, ['Shoulder', 'Clavicle_R', (1,1,1), (1,1,1), (1,1,1)]),
        ('LimitDist', 0, 0, ['DistShoulder', 'Shoulder_R', 'LIMITDIST_INSIDE']),
        ('LimitDist', 0, 0, ['DistElbow', 'Elbow_R', 'LIMITDIST_ONSURFACE']),
        ])

    # Pole target
    
    addPoseBone(fp, 'ElbowPT_L', 'MHCube025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, 
        [('ChildOf', C_CHILDOF, 1, ['Shoulder', 'Clavicle_L', (1,1,1), (1,1,1), (1,1,1)]),
         ('ChildOf', C_CHILDOF, 0, ['Hand', 'Wrist_L', (1,1,1), (1,1,1), (1,1,1)]),
         ])

    addPoseBone(fp, 'ElbowLinkPT_L', None, 'IK_L', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ElbowPT_L', 0, 1, 3.0])])

    addPoseBone(fp, 'ElbowPT_R', 'MHCube025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
        [('ChildOf', C_CHILDOF, 1, ['Shoulder', 'Clavicle_R', (1,1,1), (1,1,1), (1,1,1)]),
         ('ChildOf', C_CHILDOF, 0, ['Hand', 'Wrist_R', (1,1,1), (1,1,1), (1,1,1)]),
         ])

    addPoseBone(fp, 'ElbowLinkPT_R', None, 'IK_R', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'ElbowPT_R', 0, 1, 3.0])])

    # Targets
    
    armTrgIk_L = ('IK', 0, 1, ['ArmIK', 'LoArm_L', 1, None, (True, False,True)])
    addPoseBone(fp, 'UpArmVec_L', None, 'FK_L', (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0, [armTrgIk_L])
    addPoseBone(fp, 'UpArmVecPos_L', None, 'FK_L', (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0, [armTrgIk_L])
    addPoseBone(fp, 'UpArmVecNeg_L', None, 'FK_L', (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0, [armTrgIk_L])

    armTrgIk_R = ('IK', 0, 1, ['ArmIK', 'LoArm_R', 1, None, (True, False,True)])
    addPoseBone(fp, 'UpArmVec_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0, [armTrgIk_R])
    addPoseBone(fp, 'UpArmVecPos_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0, [armTrgIk_R])
    addPoseBone(fp, 'UpArmVecNeg_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0, [armTrgIk_R])
    
    loUpArmVecIk_L = ('IK', 0, 1, ['IK', 'Hand_L', 1, None, (True, False,True)])
    addPoseBone(fp, 'LoArmVec_L', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0, [loUpArmVecIk_L])
    
    loUpArmVecIk_R = ('IK', 0, 1, ['IK', 'Hand_R', 1, None, (True, False,True)])
    addPoseBone(fp, 'LoArmVec_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0, [loUpArmVecIk_R])
    

    deltaUpArm = 3*D
    deltaLoArm = 0*D
    
    # Upper arm deform
    
    #addPoseBone(fp, 'UpArmRot_L', 'MHCircle05', 'FK_L', (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
    #    [('IK', 0, 1, ['IK', 'LoArm_L', 1, None, (True, False,True)])])
        
    copyDeform(fp, 'DfmUpArm_L', 'UpArm_L', 0, U_LOC+U_ROT, None, [])


    #addPoseBone(fp, 'UpArmRot_R', 'MHCircle05', 'FK_R', (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
    #    [('IK', 0, 1, ['IK', 'LoArm_R', 1, None, (True, False,True)])])

    copyDeform(fp, 'DfmUpArm_R', 'UpArm_R', 0, U_LOC+U_ROT, None, [])


    # Lower arm deform
    
    addPoseBone(fp, 'LoArm2PT_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [#('CopyLoc', 0, 1, ['LoArm1', 'LoArm1PT_L', (1,1,1), (0,0,0), 0, False]),
         ('CopyLoc', 0, 0.5, ['LoArm3', 'LoArm3PT_L', (1,1,1), (0,0,0), 0, False])])

    addPoseBone(fp, 'LoArmRot_L', 'MHCircle05', 'FK_L', (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
        [('IK', 0, 1, ['IK', 'Hand_L', 1, None, (True, False,True)])])         

    copyDeformPartial(fp, 'DfmLoArm1_L', 'LoArm_L', (1,0,1), 0, U_LOC, None,
        [('CopyScale', C_LOCAL, 1, ['Scale', 'LoArm_L', (0,1,0), False]),
        ])
    
    copyDeformPartial(fp, 'DfmLoArm2_L', 'LoArm_L', (1,1,1), 0, 0, None, 
        [('IK', 0, 1, ['IK', 'Hand_L', 1, (90*D, 'LoArm2PT_L'), (True, False,True)])])
        
    copyDeformPartial(fp, 'DfmLoArm3_L', 'LoArm_L', (0,1,0), 0, 0, None,
        [('StretchTo', 0, 1, ['Stretch', 'Hand_L', 0, 1]),
         ('IK', 0, 1, ['IK', 'Hand_L', 1, (90*D, 'LoArm3PT_L'), (True, False,True)])])


    addPoseBone(fp, 'LoArm2PT_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyLoc', 0, 0.5, ['LoArm3', 'LoArm3PT_R', (1,1,1), (0,0,0), 0, False])])

    addPoseBone(fp, 'LoArmRot_R', 'MHCircle05', 'FK_R', (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
        [('IK', 0, 1, ['IK', 'Hand_R', 1, None, (True, False,True)])])

    copyDeformPartial(fp, 'DfmLoArm1_R', 'LoArm_R', (1,0,1), 0, U_LOC, None, 
        [('CopyScale', C_LOCAL, 1, ['Scale', 'LoArm_R', (0,1,0), False]),
        ])
    
    copyDeformPartial(fp, 'DfmLoArm2_R', 'LoArm_R', (1,1,1), 0, 0, None,
        [('IK', 0, 1, ['IK', 'Hand_R', 1, (90*D, 'LoArm2PT_R'), (True, False,True)])])
        
    copyDeformPartial(fp, 'DfmLoArm3_R', 'LoArm_R', (0,1,0), 0, 0, None,
        [('StretchTo', 0, 1, ['Stretch', 'Hand_R', 0, 1]),
         ('IK', 0, 1, ['IK', 'Hand_R', 1, (90*D, 'LoArm2PT_R'), (True, False,True)])])
        
    # Hand deform
    
    copyDeform(fp, 'DfmHand_L', 'Hand_L', 0, U_LOC+U_ROT, None, [])

    copyDeform(fp, 'DfmHand_R', 'Hand_R', 0, U_LOC+U_ROT, None, [])
    
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
    ('Clavicle', 'Elbow', ['ElbowPlant'], 'x1'),
    ('UpArm', 'ArmIK', ['ArmIk', 'ElbowPlant'], 'x1*(1-x2)'),
    ('UpArm', 'Elbow', ['ElbowPlant'], 'x1'),
    #('Elbow', 'DistSternum', ['ArmStretch', 'ElbowPlant'], '(1-x1)*x2'),
    ('LoArm', 'ArmIK', ['ArmIk', 'ElbowPlant'], 'x1*(1-x2)'),
    ('LoArm', 'Wrist', ['ArmIk', 'ElbowPlant'], 'x1*x2'),
    ('Wrist', 'DistShoulder', ['ArmStretch', 'ElbowPlant'], '(1-x1)*(1-x2)'),
    ('Wrist', 'DistElbow', ['ArmStretch', 'ElbowPlant'], '(1-x1)*x2'),
    ('Hand', 'FreeIK', ['ArmIk', 'ElbowPlant'], '(1-x1)*(1-x2)'),
    ('Hand', 'WristLoc', ['ArmIk'], 'x1'),
    ('Hand', 'WristRot', ['ArmIk', 'HandFollowsWrist'], 'x1*x2'),
    ('HlpLoArm', 'WristRot', ['ArmIk', 'HandFollowsWrist'], 'x1*x2'),
]

SoftArmPropLRDrivers = [
    ('UpArmSocket', 'Shoulder', ['ArmHinge'], '1-x1'),
    ('ElbowPT', 'Hand', ['ElbowFollowsWrist'], 'x1'),
    ('ElbowPT', 'Shoulder', ['ElbowFollowsShoulder', 'ElbowFollowsWrist'], 'x1*(1-x2)'),
]

ArmPropDrivers = [
    ('UpArm_L', 'LimitRot', ['RotationLimits', 'ArmIk_L'], 'x1*(1-x2)'),
    ('LoArm_L', 'LimitRot', ['RotationLimits', 'ArmIk_L'], 'x1*(1-x2)'),    
    ('Hand_L', 'LimitRot', ['RotationLimits', 'ArmIk_L', 'HandFollowsWrist_L'], 'x1*(1-x2*x3)'),
    ('UpArm_R', 'LimitRot', ['RotationLimits', 'ArmIk_R'], 'x1*(1-x2)'),
    ('LoArm_R', 'LimitRot', ['RotationLimits', 'ArmIk_R'], 'x1*(1-x2)'),    
    ('Hand_R', 'LimitRot', ['RotationLimits', 'ArmIk_R', 'HandFollowsWrist_R'], 'x1*(1-x2*x3)'),
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
    'BicepFlex_L' : ( 'LoArm1_L', 'ROTATION_DIFF', 'BendLoArmForward_L',  [(0,1), (90*D,0)] ),
    'BicepFlex_R' : ( 'LoArm1_R', 'ROTATION_DIFF', 'BendLoArmForward_R',  [(0,1), (90*D,0)] ),
}
'''

expr90 = "(1-%.3f*x1)" % (2/pi)
expr135 = "2*(1-%.3f*x1)" % (2/pi)

ElbowTargetDrivers = [    
    ("loarms-forward-90",  "LR", expr90,
        [("LoArmVec", "DirElbowFwd")]),
#    ("loarms-forward-135",  "LR", expr135,
#        [("LoArmVec", "DirElbowInv")]),
]    
