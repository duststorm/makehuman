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
Leg bone definitions 

"""

import mhx_rig
from mhx_rig import *

offs = [0,0.6,0]
prcLegTrg = 0.2

LegJoints = [
    ('r-knee',              'f', ('r-knee-raw', 'r-upper-leg', 'r-ankle', [0,0,0.1])),
    ('l-knee',              'f', ('l-knee-raw', 'l-upper-leg', 'l-ankle', [0,0,0.1])),

    ('r-upleg1',            'l', ((1-bbMarg, 'r-upper-leg'), (bbMarg, 'r-knee'))),
    ('r-upleg2',            'l', ((0.5, 'r-upper-leg'), (0.5, 'r-knee'))),

    ('l-upleg1',            'l', ((1-bbMarg, 'l-upper-leg'), (bbMarg, 'l-knee'))),
    ('l-upleg2',            'l', ((0.5, 'l-upper-leg'), (0.5, 'l-knee'))),

    ('r-legtrg',            'l', ((1-prcLegTrg, 'r-upper-leg'), (prcLegTrg, 'r-knee'))),
    ('l-legtrg',            'l', ((1-prcLegTrg, 'l-upper-leg'), (prcLegTrg, 'l-knee'))),

    ('r-midfoot',           'l', ((0.5, 'r-ankle'), (0.5, 'r-foot-1'))),
    ('r-midtoe',            'l', ((0.5, 'r-foot-1'), (0.5, 'r-foot-2'))),
    ('l-midfoot',           'l', ((0.5, 'l-ankle'), (0.5, 'l-foot-1'))),
    ('l-midtoe',            'l', ((0.5, 'l-foot-1'), (0.5, 'l-foot-2'))),

    ('r-heel0',             'v', 5721),
    ('r-heel',              'p', ['r-foot-2', 'r-foot-1', 'r-heel0']),
    ('r-ankle-tip',         'o', ('r-ankle', [0.0, 0.0, -1.0])),
    ('r-loleg-fan',         'l', ((0.75, 'r-knee'), (0.25, 'r-ankle'))),

    ('l-heel0',             'v', 13338),
    ('l-heel',              'p', ['l-foot-2', 'l-foot-1', 'l-heel0']),
    ('l-ankle-tip',         'o', ('l-ankle', [0.0, 0.0, -1.0])),
    ('l-loleg-fan',         'l', ((0.75, 'l-knee'), (0.25, 'l-ankle'))),

    ('r-knee-pt',           'o', ('r-knee', [0,0,3])),
    ('l-knee-pt',           'o', ('l-knee', [0,0,3])),

    ('r-knee-head',         'v', 4500),
    ('r-knee-tail',         'v', 5703),
    ('l-knee-head',         'v', 6865),
    ('l-knee-tail',         'v', 6779),

    ('r-legout-head',       'v', 2935),
    ('r-legout-tail',       'v', 3968),
    ('l-legout-head',       'v', 7301),
    ('l-legout-tail',       'v', 7041),

    ('r-legback-head',      'v', 4472),
    ('r-legback-tail',      'v', 3837),
    ('l-legback-head',      'v', 6893),
    ('l-legback-tail',      'v', 7172),

    ('r-legforward-head',   'v', 6560),
    ('r-legforward-tail',   'v', 3796),
    ('l-legforward-head',   'v', 6752),
    ('l-legforward-tail',   'v', 7215),
]

LegHeadsTails = [
    # Hip. Apparently necessary for good mocap
    ('Hip_L',           'spine3', 'r-upper-leg'),
    ('Hip_R',           'spine3', 'l-upper-leg'),

    # Deform 
    ('UpLeg_L',         'r-upper-leg', 'r-knee'),
    ('DfmUpLeg1_L',     'r-upper-leg', 'r-upleg1'),
    ('DfmUpLeg2_L',     'r-upleg1', 'r-upleg2'),
    ('DfmUpLeg3_L',     'r-upleg2', 'r-knee'),
    ('LoLeg_L',         'r-knee', 'r-ankle'),
    ('DfmLoLeg_L',      'r-knee', 'r-ankle'),
    ('DfmLoLegFan_L',   'r-knee', 'r-loleg-fan'),
    ('Ankle_L',         'r-ankle', 'r-ankle-tip'),
    ('Foot_L',          'r-ankle', 'r-foot-1'),
    ('Toe_L',           'r-foot-1', 'r-foot-2'),
    ('DfmFoot_L',       'r-ankle', 'r-foot-1'),
    ('DfmToe_L',        'r-foot-1', 'r-foot-2'),
    ('LegIK_L',         'r-heel', 'r-foot-2'),
    ('LegFK_L',         'r-heel', 'r-foot-2'),
    ('ToeRev_L',        'r-foot-2', 'r-foot-1'),
    ('FootRev_L',       'r-foot-1', 'r-ankle'),

    ('UpLeg_R',         'l-upper-leg', 'l-knee'),
    ('DfmUpLeg1_R',     'l-upper-leg', 'l-upleg1'),
    ('DfmUpLeg2_R',     'l-upleg1', 'l-upleg2'),
    ('DfmUpLeg3_R',     'l-upleg2', 'l-knee'),
    ('LoLeg_R',         'l-knee', 'l-ankle'),
    ('DfmLoLeg_R',      'l-knee', 'l-ankle'),
    ('DfmLoLegFan_R',   'l-knee', 'l-loleg-fan'),
    ('Ankle_R',         'l-ankle', 'l-ankle-tip'),
    ('Foot_R',          'l-ankle', 'l-foot-1'),
    ('Toe_R',           'l-foot-1', 'l-foot-2'),
    ('DfmFoot_R',       'l-ankle', 'l-foot-1'),
    ('DfmToe_R',        'l-foot-1', 'l-foot-2'),
    ('LegIK_R',         'l-heel', 'l-foot-2'),
    ('LegFK_R',         'l-heel', 'l-foot-2'),
    ('ToeRev_R',        'l-foot-2', 'l-foot-1'),
    ('FootRev_R',       'l-foot-1', 'l-ankle'),

    # Rotation diffs
    ('BendLegForward_L',    'r-upper-leg', ('r-upper-leg', (0,0,1))),
    ('BendLegBack_L',       'r-upper-leg', ('r-upper-leg', (0,0,-1))),
    ('BendLegUp_L',         'r-upper-leg', ('r-upper-leg', (0,1,0))),
    ('BendLegDown_L',       'r-upper-leg', ('r-upper-leg', (0,-1,0))),
    ('BendLegOut_L',        'r-upper-leg', ('r-upper-leg', (1,0,0))),

    ('BendLegForward_R',    'l-upper-leg', ('l-upper-leg', (0,0,1))),
    ('BendLegBack_R',       'l-upper-leg', ('l-upper-leg', (0,0,-1))),
    ('BendLegUp_R',         'l-upper-leg', ('l-upper-leg', (0,1,0))),
    ('BendLegDown_R',       'l-upper-leg', ('l-upper-leg', (0,-1,0))),
    ('BendLegOut_R',        'l-upper-leg', ('l-upper-leg', (-1,0,0))),

    # Hip deform
    ('DfmLegForward_L',     'r-legforward-head', 'r-legforward-tail'),
    ('DfmLegBack_L',        'r-legback-head', 'r-legback-tail'),
    ('DfmLegOut_L',         'r-legout-head', 'r-legout-tail'),
    ('LegForwardTrg_L',     'r-legforward-tail', ('r-legforward-tail', zunit)),
    ('LegBackTrg_L',        'r-legback-tail', ('r-legback-tail', zunit)),
    ('LegOutTrg_L',         'r-legout-tail', ('r-legout-tail', zunit)),

    ('DfmLegForward_R',     'l-legforward-head', 'l-legforward-tail'),
    ('DfmLegBack_R',        'l-legback-head', 'l-legback-tail'),
    ('DfmLegOut_R',         'l-legout-head', 'l-legout-tail'),
    ('LegForwardTrg_R',     'l-legforward-tail', ('l-legforward-tail', zunit)),
    ('LegBackTrg_R',        'l-legback-tail', ('l-legback-tail', zunit)),
    ('LegOutTrg_R',         'l-legout-tail', ('l-legout-tail', zunit)),

    # Knee deform
    ('DfmKnee_L',           'r-knee-head', 'r-knee-tail'),
    ('KneeTrg_L',           'r-knee-tail', ('r-knee-tail', yunit)),
    ('DfmKnee_R',           'l-knee-head', 'l-knee-tail'),
    ('KneeTrg_R',           'l-knee-tail', ('l-knee-tail', yunit)),

    # Pole Targets
    ('LegTrg_L',            'r-upper-leg', 'r-legtrg'),
    ('UpLegRot_L',          'r-upper-leg', 'r-legtrg'),
    ('UpLeg1PT_L',          ('r-upleg1', (0,0,-1)), ('r-upleg1', (0,0,-2))),
    ('UpLeg2PT_L',          ('r-upleg2', (0,0,-1)), ('r-upleg2', (0,0,-2))),
    ('KneePT_L',            'r-knee-pt', ('r-knee-pt', offs)),
    ('KneeLinkPT_L',        'r-knee', 'r-knee-pt'),
    ('FootPT_L',            ('r-midfoot', (0,1,0.2)), ('r-midfoot', (0,1.3,0.2))),
    ('ToePT_L',             ('r-midtoe', (0,1,0)), ('r-midtoe', (0,1.3,0))),

    ('LegTrg_R',            'l-upper-leg', 'l-legtrg'),
    ('UpLegRot_R',          'l-upper-leg', 'l-legtrg'),
    ('UpLeg1PT_R',          ('l-upleg1', (0,0,-1)), ('l-upleg1', (0,0,-2))),
    ('UpLeg2PT_R',          ('l-upleg2', (0,0,-1)), ('l-upleg2', (0,0,-2))),
    ('KneePT_R',            'l-knee-pt', ('l-knee-pt', offs)),
    ('KneeLinkPT_R',        'l-knee', 'l-knee-pt'),
    ('FootPT_R',            ('l-midfoot', (0,1,0.2)), ('l-midfoot', (0,1.3,0.2))),
    ('ToePT_R',             ('l-midtoe', (0,1,0)), ('l-midtoe', (0,1.3,0))),
]

#
#   LegArmature
#

upLegRoll = 0
loLegRoll = 0
footRoll = 0
#toeRoll = -63.5*D
toeRoll = 135*D
footCtrlRoll = 0.0

LegArmature = [
    # Leg
    #('Hip_L',          0, 'DfmHips', 0, L_HELP, NoBB),
    ('UpLeg_L',         upLegRoll, 'DfmHips', F_WIR, L_LLEGFK, NoBB),
    ('LoLeg_L',         loLegRoll, 'UpLeg_L', F_WIR, L_LLEGFK, NoBB),
    ('Foot_L',          footRoll, 'LoLeg_L', F_WIR+F_CON, L_LLEGFK, NoBB),
    ('Toe_L',           toeRoll, 'Foot_L', F_WIR, L_LLEGFK, NoBB),
    ('LegIK_L',         footCtrlRoll, Master, F_WIR, L_LLEGIK, NoBB),
    ('ToeRev_L',        0, 'LegIK_L', F_WIR, L_LLEGIK, NoBB),
    ('FootRev_L',       0, 'ToeRev_L', F_WIR, L_LLEGIK, NoBB),
    ('Ankle_L',         0, 'FootRev_L', 0, L_HELP, NoBB),
    ('LegFK_L',         footCtrlRoll, 'LoLeg_L', 0, L_HELP, NoBB),

    #('Hip_R',          0, 'DfmHips', 0, L_HELP, NoBB),
    ('UpLeg_R',         -upLegRoll, 'DfmHips', F_WIR, L_RLEGFK, NoBB),
    ('LoLeg_R',         -loLegRoll, 'UpLeg_R', F_WIR, L_RLEGFK, NoBB),
    ('Foot_R',          -footRoll, 'LoLeg_R', F_WIR+F_CON, L_RLEGFK, NoBB),
    ('Toe_R',           -toeRoll, 'Foot_R', F_WIR, L_RLEGFK, NoBB),
    ('LegIK_R',         -footCtrlRoll, Master, F_WIR, L_RLEGIK, NoBB),
    ('ToeRev_R',        0, 'LegIK_R', F_WIR, L_RLEGIK, NoBB),
    ('FootRev_R',       0, 'ToeRev_R', F_WIR, L_RLEGIK, NoBB),
    ('Ankle_R',         0, 'FootRev_R', 0, L_HELP, NoBB),
    ('LegFK_R',         footCtrlRoll, 'LoLeg_R', 0, L_HELP, NoBB),  

    # Pole targets
    ('LegTrg_L',        0.0, 'DfmHips', 0, L_HELP, NoBB),
    ('UpLegRot_L',      0.0, 'DfmHips', F_WIR, L_LLEGFK+L_LLEGIK, NoBB),
    ('UpLeg1PT_L',      0.0, 'UpLegRot_L', 0, L_HELP, NoBB),
    ('UpLeg2PT_L',      0.0, 'UpLeg_L', 0, L_HELP, NoBB),
    ('KneePT_L',        0.0, 'LegIK_L', F_WIR, L_LLEGIK, NoBB),
    ('KneeLinkPT_L',    0.0, 'UpLeg_L', F_RES, L_LLEGIK, NoBB),
    ('FootPT_L',        0.0, 'FootRev_L', 0, L_HELP, NoBB),
    ('ToePT_L',         0.0, 'ToeRev_L', 0, L_HELP, NoBB),

    ('LegTrg_R',        0.0, 'DfmHips', 0, L_HELP, NoBB),
    ('UpLegRot_R',      0.0, 'DfmHips', F_WIR, L_LLEGFK+L_LLEGIK, NoBB),
    ('UpLeg1PT_R',      0.0, 'UpLegRot_R', 0, L_HELP, NoBB),
    ('UpLeg2PT_R',      0.0, 'UpLeg_R', 0, L_HELP, NoBB),
    ('KneePT_R',        0.0, 'LegIK_R', F_WIR, L_LLEGIK, NoBB),
    ('KneeLinkPT_R',    0.0, 'UpLeg_R', F_RES, L_LLEGIK, NoBB),
    ('FootPT_R',        0.0, 'FootRev_R', 0, L_HELP, NoBB),
    ('ToePT_R',         0.0, 'ToeRev_R', 0, L_HELP, NoBB),

    # Rotation diffs
    ('BendLegForward_L',    pi, 'DfmHips', 0, L_HELP, NoBB),
    ('BendLegBack_L',       0, 'DfmHips', 0, L_HELP, NoBB),
    ('BendLegUp_L',         0, 'DfmHips', 0, L_HELP, NoBB),
    ('BendLegDown_L',       0, 'DfmHips', 0, L_HELP, NoBB),
    ('BendLegOut_L',        -90*D, 'DfmHips', 0, L_HELP, NoBB),

    ('BendLegForward_R',    pi, 'DfmHips', 0, L_HELP, NoBB),
    ('BendLegBack_R',       0, 'DfmHips', 0, L_HELP, NoBB),
    ('BendLegUp_R',         0, 'DfmHips', 0, L_HELP, NoBB),
    ('BendLegDown_R',       0, 'DfmHips', 0, L_HELP, NoBB),
    ('BendLegOut_R',        90*D, 'DfmHips', 0, L_HELP, NoBB),

    # Deform
    ('DfmUpLeg1_L',         upLegRoll, 'DfmHips', F_DEF, L_DMAIN, NoBB),
    ('DfmUpLeg2_L',         upLegRoll, 'DfmUpLeg1_L', F_DEF+F_CON, L_DMAIN,(0,0,5) ),
    ('DfmUpLeg3_L',         upLegRoll, 'DfmUpLeg2_L', F_DEF+F_CON, L_DMAIN, NoBB),
    ('DfmLoLeg_L',          loLegRoll, 'DfmUpLeg3_L', F_DEF, L_DMAIN, NoBB),
    ('DfmLoLegFan_L',       loLegRoll, 'DfmUpLeg3_L', F_DEF, L_DEF, NoBB),
    ('DfmFoot_L',           footRoll, 'DfmLoLeg_L', F_DEF+F_CON, L_DMAIN, NoBB),
    ('DfmToe_L',            toeRoll, 'DfmFoot_L', F_DEF, L_DMAIN, NoBB),

    ('DfmUpLeg1_R',         upLegRoll, 'DfmHips', F_DEF, L_DMAIN, NoBB),
    ('DfmUpLeg2_R',         upLegRoll, 'DfmUpLeg1_R', F_DEF+F_CON, L_DMAIN,(0,0,5) ),
    ('DfmUpLeg3_R',         upLegRoll, 'DfmUpLeg2_R', F_DEF+F_CON, L_DMAIN, NoBB),
    ('DfmLoLeg_R',          -loLegRoll, 'DfmUpLeg3_R', F_DEF, L_DMAIN, NoBB),
    ('DfmLoLegFan_R',       -loLegRoll, 'DfmUpLeg3_R', F_DEF, L_DEF, NoBB),
    ('DfmFoot_R',           -footRoll, 'DfmLoLeg_R', F_DEF+F_CON, L_DMAIN, NoBB),
    ('DfmToe_R',            -toeRoll, 'DfmFoot_R', F_DEF, L_DMAIN, NoBB),

    # Hip deform
    ('DfmLegForward_L',     0, 'DfmHips', F_DEF, L_DEF, NoBB),
    ('DfmLegBack_L',        0, 'DfmHips', F_DEF, L_DEF, NoBB),
    ('DfmLegOut_L',         0, 'DfmHips', F_DEF, L_DEF, NoBB),
    ('LegForwardTrg_L',     0, 'DfmUpLeg1_L', 0, L_HELP, NoBB),
    ('LegBackTrg_L',        0, 'DfmUpLeg1_L', 0, L_HELP, NoBB),
    ('LegOutTrg_L',         0, 'DfmUpLeg1_L', 0, L_HELP, NoBB),

    ('DfmLegForward_R',     0, 'DfmHips', F_DEF, L_DEF, NoBB),
    ('DfmLegBack_R',        0, 'DfmHips', F_DEF, L_DEF, NoBB),
    ('DfmLegOut_R',         0, 'DfmHips', F_DEF, L_DEF, NoBB),
    ('LegForwardTrg_R',     0, 'DfmUpLeg1_R', 0, L_HELP, NoBB),
    ('LegBackTrg_R',        0, 'DfmUpLeg1_R', 0, L_HELP, NoBB),
    ('LegOutTrg_R',         0, 'DfmUpLeg1_R', 0, L_HELP, NoBB),

    # Knee deform
    ('DfmKnee_L',           0, 'DfmUpLeg3_L', F_DEF, L_DEF, NoBB),
    ('KneeTrg_L',           0, 'LoLeg_L', 0, L_HELP, NoBB),
    ('DfmKnee_R',           0, 'DfmUpLeg3_R', F_DEF, L_DEF, NoBB),
    ('KneeTrg_R',           0, 'LoLeg_R', 0, L_HELP, NoBB),

]

#
#   LegControlPoses(fp):
#

limUpLeg_L = (-110*D,90*D, -90*D,90*D, -110*D,40*D)
limUpLeg_R = (-110*D,90*D, -90*D,90*D, -40*D,110*D)

limLoLeg_L = (-20*D,150*D,-40*D,40*D, -40*D,40*D)
limLoLeg_R = (-20*D,150*D,-40*D,40*D, -40*D,40*D)

limFoot_L = (-50*D,50*D, -40*D,40*D, -40*D,40*D)
limFoot_R = (-50*D,50*D, -40*D,40*D, -40*D,40*D)

limToe_L = (-20*D,60*D, 0,0, 0,0)
limToe_R = (-20*D,60*D, 0,0, 0,0)

limRevFoot_L = (-20*D,60*D, 0,0, 0,0)
limRevFoot_R = (-20*D,60*D, 0,0, 0,0)

limRevToe_L = (-10*D,45*D, 0,0, 0,0)
limRevToe_R = (-10*D,45*D, 0,0, 0,0)

#
#   Rotation modes
#   Dmod = Deform rig mode
#   Cmod = Control rig mode
#

DmodUpLeg = P_YZX
DmodLoLeg = P_YZX
DmodFoot = P_YZX
DmodToe = P_YZX

CmodUpLeg = 0
CmodLoLeg = 0
CmodFoot = 0
CmodToe = 0

def LegControlPoses(fp):
    addPoseBone(fp, 'UpLeg_L', 'GZM_Circle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+CmodUpLeg,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_L, (1,1,1)])])

    addPoseBone(fp, 'UpLeg_R', 'GZM_Circle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+CmodUpLeg,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_R, (1,1,1)])])

    deltaKnee = -2.5*D

    addPoseBone(fp, 'LoLeg_L', 'GZM_Circle025', 'FK_L', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+CmodLoLeg,
        [('IK', 0, 0, ['LegIK', 'Ankle_L', 2, (-90*D+deltaKnee, 'KneePT_L'), (1,0,1)]),
        ('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_L, (1,1,1)])
        ])

    addPoseBone(fp, 'LoLeg_R', 'GZM_Circle025', 'FK_R', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH+CmodLoLeg,
        [('IK', 0, 0, ['LegIK', 'Ankle_R', 2, (-90*D-deltaKnee, 'KneePT_R'), (1,0,1)]),
        ('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_R, (1,1,1)])
        ])

    addPoseBone(fp, 'LegIK_L', 'MHFootCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
        mhx_rig.rootChildOfConstraints + [
        ('ChildOf', C_CHILDOF, 0, ['Hip', 'DfmHips', (1,1,1), (1,1,1), (1,1,1)]),
        ('LimitDist', 0, 1, ['DistHip', 'DfmHips', 'LIMITDIST_INSIDE'])])

    addPoseBone(fp, 'LegIK_R', 'MHFootCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
        mhx_rig.rootChildOfConstraints + [
        ('ChildOf', C_CHILDOF, 0, ['Hip', 'DfmHips', (1,1,1), (1,1,1), (1,1,1)]),
        ('LimitDist', 0, 1, ['DistHip', 'DfmHips', 'LIMITDIST_INSIDE'])])

    addPoseBone(fp, 'FootRev_L', 'MHRevFoot', 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), CmodFoot, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevFoot_L, (1,1,1)])])

    addPoseBone(fp, 'FootRev_R', 'MHRevFoot', 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), CmodFoot,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevFoot_R, (1,1,1)])])

    addPoseBone(fp, 'ToeRev_L', 'MHRevToe', 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), CmodToe, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevToe_L, (1,1,1)])])

    addPoseBone(fp, 'ToeRev_R', 'MHRevToe', 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), CmodToe, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevToe_R, (1,1,1)])])
    
    addPoseBone(fp, 'Foot_L', 'MHFoot', 'FK_L', (0,0,0), (0,1,1), (1,1,1), (1,1,1), CmodFoot, 
        [('IK', 0, 0, ['RevIK', 'FootRev_L', 1, (90*D, 'FootPT_L'), (1,0,1)]),
         #('CopyRot', C_LOCAL, 0, ['RevRot', 'FootRev_L', (0,1,0), (0,0,0), True]),
         ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,True)])])

    addPoseBone(fp, 'Foot_R', 'MHFoot', 'FK_R', (0,0,0), (0,1,1), (1,1,1), (1,1,1), CmodFoot, 
        [('IK', 0, 0, ['RevIK', 'FootRev_R', 1, (90*D, 'FootPT_R'), (1,0,1)]),
         #('CopyRot', C_LOCAL, 0, ['RevRot', 'FootRev_R', (0,1,0), (0,0,0), True]),
         ('IK', 0, 1, ['FreeIK', None, 2, None, (True, False,True)])])

    addPoseBone(fp, 'Toe_L', 'MHToe_L', 'FK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), CmodToe, 
        [('IK', 0, 0, ['RevIK', 'ToeRev_L', 1, (90*D, 'ToePT_L'), (1,0,1)])])

    addPoseBone(fp, 'Toe_R', 'MHToe_R', 'FK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), CmodToe, 
        [('IK', 0, 0, ['RevIK', 'ToeRev_R', 1, (90*D, 'ToePT_R'), (1,0,1)])])
    
    addPoseBone(fp, 'Ankle_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])
    addPoseBone(fp, 'Ankle_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'LegFK_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])
    addPoseBone(fp, 'LegFK_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])


    # Pole target

    addPoseBone(fp, 'KneePT_L', 'MHCube025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'KneeLinkPT_L', None, 'IK_L', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', 0, 1, ['Stretch', 'KneePT_L', 0])])

    addPoseBone(fp, 'LegTrg_L', None, 'FK_L', (1,1,1), (1,0,1), (1,1,1), (1,1,1), P_YXZ, 
         [('IK', 0, 1, ['LegIK', 'LoLeg_L', 1, None, (True, False,True)])])

    addPoseBone(fp, 'UpLegRot_L', 'GZM_Circle10', 'IK_L', (1,1,1), (1,0,1), (1,1,1), (1,1,1), P_YXZ, 
         [('IK', 0, 1, ['LegIK', 'LoLeg_L', 1, None, (True, False,True)])])


    addPoseBone(fp, 'KneePT_R', 'MHCube025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'KneeLinkPT_R', None, 'IK_R', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', 0, 1, ['Stretch', 'KneePT_R', 0])])

    addPoseBone(fp, 'LegTrg_R', None, 'FK_R', (1,1,1), (1,0,1), (1,1,1), (1,1,1), P_YXZ, 
         [('IK', 0, 1, ['LegIK', 'LoLeg_R', 1, None, (True, False,True)])])

    addPoseBone(fp, 'UpLegRot_R', 'GZM_Circle10', 'IK_R', (1,1,1), (1,0,1), (1,1,1), (1,1,1), P_YXZ, 
         [('IK', 0, 1, ['LegIK', 'LoLeg_R', 1, None, (True, False,True)])])

    deltaUpLeg = 0

    # Deform 
    copyDeformPartial(fp, 'DfmUpLeg1_L', 'UpLeg_L', (1,0,1), DmodUpLeg, U_LOC+U_SCALE, None, 
        [('IK', 0, 1, ['IK', 'LoLeg_L', 1, (90*D-deltaUpLeg, 'UpLeg1PT_L'), (True, False,True)])])
    
    copyDeformPartial(fp, 'DfmUpLeg2_L', 'UpLeg_L', (1,1,1), DmodUpLeg, U_SCALE, None, [])
        
    copyDeformPartial(fp, 'DfmUpLeg3_L', 'UpLeg_L', (0,1,0), DmodUpLeg, U_SCALE, None, 
        [('IK', 0, 1, ['IK', 'LoLeg_L', 1, (90*D-deltaUpLeg, 'UpLeg2PT_L'), (True, False,True)])])

    copyDeform(fp, 'DfmLoLeg_L', 'LoLeg_L', DmodLoLeg, U_LOC+U_ROT+U_SCALE, None, [])

    addPoseBone(fp, 'DfmLoLegFan_L', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), DmodLoLeg,
        [('CopyRot', 0, 0.5, ['Rot', 'LoLeg_L', (1,1,1), (0,0,0), False])])

    copyDeform(fp, 'DfmFoot_L', 'Foot_L', DmodFoot, U_LOC+U_ROT, None, [])

    copyDeform(fp, 'DfmToe_L', 'Toe_L', DmodToe, U_LOC+U_ROT, None, [])


    copyDeformPartial(fp, 'DfmUpLeg1_R', 'UpLeg_R', (1,1,1), DmodUpLeg, U_LOC+U_SCALE, None, 
        [('IK', 0, 1, ['IK', 'LoLeg_R', 1, (90*D+deltaUpLeg, 'UpLeg1PT_R'), (True, False,True)])])
    
    copyDeformPartial(fp, 'DfmUpLeg2_R', 'UpLeg_R', (1,1,1), DmodUpLeg, U_SCALE, None, [])
        
    copyDeformPartial(fp, 'DfmUpLeg3_R', 'UpLeg_R', (0,1,0), DmodUpLeg, U_SCALE, None,
        [('IK', 0, 1, ['IK', 'LoLeg_R', 1, (90*D+deltaUpLeg, 'UpLeg2PT_R'), (True, False,True)])])

    copyDeform(fp, 'DfmLoLeg_R', 'LoLeg_R', DmodLoLeg, U_LOC+U_ROT+U_SCALE, None, [])

    addPoseBone(fp, 'DfmLoLegFan_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), DmodLoLeg,
        [('CopyRot', 0, 0.5, ['Rot', 'LoLeg_R', (1,1,1), (0,0,0), False])])

    copyDeform(fp, 'DfmFoot_R', 'Foot_R', DmodFoot, U_LOC+U_ROT, None, [])

    copyDeform(fp, 'DfmToe_R', 'Toe_R', DmodToe, U_LOC+U_ROT, None, [])


    # Hip deform

    addPoseBone(fp, 'DfmLegForward_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegForwardTrg_L', 0]),
         ('LimitScale', C_OW_LOCAL, 0, ['Scale', (0,0, 0,0, 0,0), (0,1,0)])])

    addPoseBone(fp, 'DfmLegBack_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegBackTrg_L', 0])])

    addPoseBone(fp, 'DfmLegOut_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegOutTrg_L', 0])])


    addPoseBone(fp, 'DfmLegForward_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegForwardTrg_R', 0]),
         ('LimitScale', C_OW_LOCAL, 0, ['Scale', (0,0, 0,0, 0,0), (0,1,0)])])

    addPoseBone(fp, 'DfmLegBack_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegBackTrg_R', 0])])

    addPoseBone(fp, 'DfmLegOut_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', C_DEFRIG, 1, ['Stretch', 'LegOutTrg_R', 0])])

    # Knee deform

    addPoseBone(fp, 'DfmKnee_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', C_DEFRIG, 1, ['Stretch', 'KneeTrg_L', 0])])

    addPoseBone(fp, 'DfmKnee_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', C_DEFRIG, 1, ['Stretch', 'KneeTrg_R', 0])])

    return

#
#   LegFKIKDrivers
#   (Bone, cond, FK constraint, IK constraint, driver, channel, max)
#

LegFKIKDrivers = [
    ("UpLeg_L", True, [], [], "PLegIK_L", "LOC_X", 1.0),
    ("LoLeg_L", True, [], ["LegIK"], "PLegIK_L", "LOC_X", 1.0),
    ("Foot_L", True, ["FreeIK"], ["RevIK"], "PLegIK_L", "LOC_X", 1.0),
    ("Toe_L", True, [], ["RevIK"], "PLegIK_L", "LOC_X", 1.0),
    
    ("UpLeg_R", True, [], [], "PLegIK_R", "LOC_X", 1.0),
    ("LoLeg_R", True, [], ["LegIK"], "PLegIK_R", "LOC_X", 1.0),
    ("Foot_R", True, ["FreeIK"], ["RevIK"], "PLegIK_R", "LOC_X", 1.0),
    ("Toe_R", True, [], ["RevIK"], "PLegIK_R", "LOC_X", 1.0),
]

#
#   LegPropLRDrivers
#   (Bone, Name, Props, Expr)
#

LegPropLRDrivers = [
    ('LoLeg', 'LegIK', ['LegFkIk'], 'x1'),
    ('Foot', 'RevIK', ['LegFkIk'], 'x1'),
    ('Foot', 'FreeIK', ['LegFkIk'], '1-x1'),
    ('Toe', 'RevIK', ['LegFkIk'], 'x1'),
]

#
#   LegDeformDrivers
#   Bone : (constraint, driver, rotdiff, keypoints)
#

LegDeformDrivers = [
    ("DfmLegForward_L", "Stretch", None,
        [("f", "LegTrg_L", "BendLegForward_L"), ("o", "LegTrg_L", "BendLegOut_L")], 
        [(0,1), (60*D,1), (90*D,0.3)]),
    ("DfmLegForward_L", "Scale",  "(d-u)*(f<%.2f)" % (75*D),
        [("u", "LegTrg_L", "BendLegUp_L"), ("d", "LegTrg_L", "BendLegDown_L"), ("f", "LegTrg_L", "BendLegForward_L")], 
        [(0,0), (20*D,1)]),
    ("DfmLegBack_L", "Stretch",   "min(b,o+0.5)",
        [("b", "LegTrg_L", "BendLegBack_L"), ("o", "LegTrg_L", "BendLegOut_L")], 
        [(0,1), (60*D,1), (90*D,0.3)]),
    ("DfmLegOut_L", "Stretch",  None,
        [("o", "LegTrg_L", "BendLegOut_L")], 
        [(0,1), (60*D,1), (90*D,0.3)]),

    ("DfmLegForward_R", "Stretch", None,
        [("f", "LegTrg_R", "BendLegForward_R"), ("o", "LegTrg_R", "BendLegOut_R")], 
        [(0,1), (60*D,1), (90*D,0.3)]),
    ("DfmLegForward_R", "Scale",  "(d-u)*(f<%.2f)" % (75*D),
        [("u", "LegTrg_R", "BendLegUp_R"), ("d", "LegTrg_R", "BendLegDown_R"), ("f", "LegTrg_R", "BendLegForward_R")], 
        [(0,0), (20*D,1)]),
    ("DfmLegBack_R", "Stretch",   "min(b,o+0.5)",
        [("b", "LegTrg_R", "BendLegBack_R"), ("o", "LegTrg_R", "BendLegOut_R")], 
        [(0,1), (60*D,1), (90*D,0.3)]),
    ("DfmLegOut_R", "Stretch",  None,
        [("o", "LegTrg_R", "BendLegOut_R")], 
        [(0,1), (60*D,1), (90*D,0.3)]),
]

#
#   LegShapeDrivers
#   Shape : (driver, rotdiff, keypoints)
#

LegShapeDrivers = {
}




