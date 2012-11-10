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

from . import the
from the import *
from . import posebone
from posebone import addPoseBone

offs = [0,0.6,0]
prcLegTrg = 0.2

LegJoints = [
    #('r-knee',              'f', ('r-knee-raw', 'r-upper-leg', 'r-ankle', [0,0,0.1])),
    #('l-knee',              'f', ('l-knee-raw', 'l-upper-leg', 'l-ankle', [0,0,0.1])),
    ('r-knee',              'j', 'r-knee'),
    ('l-knee',              'j', 'l-knee'),

    ('r-upleg1',            'l', ((0.75, 'r-upper-leg'), (0.25, 'r-knee'))),
    ('r-upleg2',            'l', ((0.5, 'r-upper-leg'), (0.5, 'r-knee'))),
    ('l-upleg1',            'l', ((0.75, 'l-upper-leg'), (0.25, 'l-knee'))),
    ('l-upleg2',            'l', ((0.5, 'l-upper-leg'), (0.5, 'l-knee'))),
    ('r-loleg1',            'l', ((0.75, 'r-knee'), (0.25, 'r-ankle'))),
    ('l-loleg1',            'l', ((0.75, 'l-knee'), (0.25, 'l-ankle'))),

    ('r-knee-stretch1',     'vl', ((0.25, 3985), (0.75, 3794))),
    ('r-knee-stretch2',     'vl', ((0.25, 3860), (0.75, 5710))),
    ('l-knee-stretch1',     'vl', ((0.25, 7024), (0.75, 7217))), 
    ('l-knee-stretch2',     'vl', ((0.25, 7149), (0.75, 6772))),

    ('r-legtrg',            'l', ((1-prcLegTrg, 'r-upper-leg'), (prcLegTrg, 'r-knee'))),
    ('l-legtrg',            'l', ((1-prcLegTrg, 'l-upper-leg'), (prcLegTrg, 'l-knee'))),

    ('r-midfoot',           'l', ((0.5, 'r-ankle'), (0.5, 'r-foot-1'))),
    ('r-midtoe',            'l', ((0.5, 'r-foot-1'), (0.5, 'r-foot-2'))),
    ('l-midfoot',           'l', ((0.5, 'l-ankle'), (0.5, 'l-foot-1'))),
    ('l-midtoe',            'l', ((0.5, 'l-foot-1'), (0.5, 'l-foot-2'))),

    ('r-heel0',             'v', 5721),
    #('r-heel',              'p', ['r-foot-2', 'r-foot-1', 'r-heel0']),
    ('r-heel',              'l', ((-2.5,'r-foot-2'), (3.5,'r-foot-1'))),
    ('r-ankle-tip',         'o', ('r-ankle', [0.0, 0.0, -1.0])),
    ('r-loleg-fan',         'l', ((0.75, 'r-knee'), (0.25, 'r-ankle'))),

    ('l-heel0',             'v', 13338),
    #('l-heel',              'p', ['l-foot-2', 'l-foot-1', 'l-heel0']),
    ('l-heel',              'l', ((-2.5,'l-foot-2'), (3.5,'l-foot-1'))),
    ('l-ankle-tip',         'o', ('l-ankle', [0.0, 0.0, -1.0])),
    ('l-loleg-fan',         'l', ((0.75, 'l-knee'), (0.25, 'l-ankle'))),

    ('r-knee-pt',           'o', ('r-knee', [0,0,3])),
    ('l-knee-pt',           'o', ('l-knee', [0,0,3])),

    ('r-knee-head',         'v', 4500),
    ('r-knee-tail',         'v', 5703),
    ('l-knee-head',         'v', 6865),
    ('l-knee-tail',         'v', 6779),

    ('r-legout-head',       'vl', ((0.4, 6555), (0.6, 4462))),
    ('r-legout-tail',       'vl', ((1.0, 3973), (0.0, 3832))),
    ('l-legout-head',       'vl', ((0.4, 6757), (0.6, 6903))),
    ('l-legout-tail',       'vl', ((1.0, 7035), (0.0, 7177))),

    ('r-legfront-head',     'vl', ((0.8, 6562), (0.2, 4463))),
    ('r-legfront-tail',     'vl', ((0.7, 3942), (0.3, 3841))),
    ('l-legfront-head',     'vl', ((0.8, 6750), (0.2, 6902))),
    ('l-legfront-tail',     'vl', ((0.7, 7067), (0.3, 7168))),    
]

if MuscleBones:    
    LegJoints += [
    ('r-butt',              'v', 4475),
    ('l-butt',              'v', 6890),

    ('r-legback-head',      'vl', ((0.1, 6562), (0.9, 2120))),
    ('r-legback-tail',      'vl', ((0.1, 3942), (0.9, 3841))),
    ('l-legback-head',      'vl', ((0.1, 6750), (0.9, 7481))),
    ('l-legback-tail',      'vl', ((0.1, 7067), (0.9, 7168))),

    ('r-legin-head',        'vl', ((0.5, 7298), (0.5, 7258))),
    ('r-legin-tail',        'vl', ((0.2, 3973), (0.8, 3832))),
    ('l-legin-head',        'vl', ((0.5, 7298), (0.5, 7258))),
    ('l-legin-tail',        'vl', ((0.2, 7035), (0.8, 7177))),
]

LegHeadsTails = [
    # Hip = leg location
    ('Hip_L',           'r-upper-leg', ('r-upper-leg', the.ysmall)),
    ('Hip_R',           'l-upper-leg', ('l-upper-leg', the.ysmall)),

    # Leg
    ('UpLeg_L',         'r-upper-leg', 'r-knee'),
    ('LoLeg_L',         'r-knee', 'r-ankle'),
    ('Foot_L',          'r-ankle', 'r-foot-1'),
    ('Toe_L',           'r-foot-1', 'r-foot-2'),
    ('LegFK_L',         'r-heel', 'r-foot-2'),
    
    ('UpLeg_R',         'l-upper-leg', 'l-knee'),
    ('LoLeg_R',         'l-knee', 'l-ankle'),
    ('Foot_R',          'l-ankle', 'l-foot-1'),
    ('Toe_R',           'l-foot-1', 'l-foot-2'),
    ('LegFK_R',         'l-heel', 'l-foot-2'),
    
    # IK Leg
    ('UpLegIK_L',       'r-upper-leg', 'r-knee'),
    ('LoLegIK_L',       'r-knee', 'r-ankle'),
    ('Ankle_L',         'r-ankle', 'r-ankle-tip'),
    ('AnkleIK_L',       'r-ankle', 'r-ankle-tip'),
    ('LegIK_L',         'r-heel', 'r-foot-2'),
    ('ToeRev_L',        'r-foot-2', 'r-foot-1'),
    ('FootRev_L',       'r-foot-1', 'r-ankle'),

    ('UpLegIK_R',       'l-upper-leg', 'l-knee'),
    ('LoLegIK_R',       'l-knee', 'l-ankle'),
    ('Ankle_R',         'l-ankle', 'l-ankle-tip'),
    ('AnkleIK_R',       'l-ankle', 'l-ankle-tip'),
    ('LegIK_R',         'l-heel', 'l-foot-2'),
    ('ToeRev_R',        'l-foot-2', 'l-foot-1'),
    ('FootRev_R',       'l-foot-1', 'l-ankle'),

    # Deform 
    ('DfmUpLeg1_L',      'r-upper-leg', 'r-upleg2'),
    ('DfmUpLeg2_L',      'r-upleg2', 'r-knee'),
    ('DfmLoLeg_L',      'r-knee', 'r-ankle'),
    ('DfmLoLegFan_L',   'r-knee', 'r-loleg-fan'),
    ('DfmFoot_L',       'r-ankle', 'r-foot-1'),
    ('DfmToe_L',        'r-foot-1', 'r-foot-2'),

    ('DfmUpLeg1_R',      'l-upper-leg', 'l-upleg2'),
    ('DfmUpLeg2_R',      'l-upleg2', 'l-knee'),
    ('DfmLoLeg_R',      'l-knee', 'l-ankle'),
    ('DfmLoLegFan_R',   'l-knee', 'l-loleg-fan'),
    ('DfmFoot_R',       'l-ankle', 'l-foot-1'),
    ('DfmToe_R',        'l-foot-1', 'l-foot-2'),

    # Tweaks
    ('UpLegVec_L',      'r-upper-leg', 'r-upleg1'),
    ('UpLegVec_R',      'l-upper-leg', 'l-upleg1'),
    ('UpLegVecNeg_L',    'r-upper-leg', 'r-upleg1'),
    ('UpLegVecNeg_R',    'l-upper-leg', 'l-upleg1'),

    # Pole Targets
    #('LegTrg_L',        'r-upper-leg', 'r-legtrg'),
    ('UpLeg2PT_L',      ('r-upleg1', (0,0,-1)), ('r-upleg1', (0,0,-2))),
    ('UpLeg3PT_L',      ('r-upleg2', (0,0,-1)), ('r-upleg2', (0,0,-2))),
    ('KneePT_L',        'r-knee-pt', ('r-knee-pt', offs)),
    ('KneePTFK_L',      'r-knee-pt', ('r-knee-pt', offs)),
    ('KneeLinkPT_L',    'r-knee', 'r-knee-pt'),
    ('FootPT_L',        ('r-midfoot', (0,1,0.2)), ('r-midfoot', (0,1.3,0.2))),
    ('ToePT_L',         ('r-midtoe', (0,1,0)), ('r-midtoe', (0,1.3,0))),

    #('LegTrg_R',        'l-upper-leg', 'l-legtrg'),
    ('UpLeg2PT_R',      ('l-upleg1', (0,0,-1)), ('l-upleg1', (0,0,-2))),
    ('UpLeg3PT_R',      ('l-upleg2', (0,0,-1)), ('l-upleg2', (0,0,-2))),
    ('KneePT_R',        'l-knee-pt', ('l-knee-pt', offs)),
    ('KneePTFK_R',      'l-knee-pt', ('l-knee-pt', offs)),
    ('KneeLinkPT_R',    'l-knee', 'l-knee-pt'),
    ('FootPT_R',        ('l-midfoot', (0,1,0.2)), ('l-midfoot', (0,1.3,0.2))),
    ('ToePT_R',         ('l-midtoe', (0,1,0)), ('l-midtoe', (0,1.3,0))),

    # Muscles
    ('DfmLegOut_L',     'r-legout-head', 'r-legout-tail'),
    ('DfmLegOut_R',     'l-legout-head', 'l-legout-tail'),
    #('DfmLegFront_L',   'r-legfront-head', 'r-legfront-tail'),
    #('DfmLegFront_R',   'l-legfront-head', 'l-legfront-tail'),

    ('LegOutTrg_L',     'r-knee', 'r-legout-tail'),
    ('LegOutTrg_R',     'l-knee', 'l-legout-tail'),
    ('LegFrontTrg_L',   'r-knee', 'r-legfront-tail'),
    ('LegFrontTrg_R',   'l-knee', 'l-legfront-tail'),

    # Fan bones    
    ('DfmHipFan_L',      'r-upper-leg', 'r-upleg1'),
    ('DfmHipFan_R',      'l-upper-leg', 'l-upleg1'),

    ('DfmKneeFan_L',      'r-knee', 'r-loleg1'),
    ('DfmKneeFan_R',      'l-knee', 'l-loleg1'),

    ('DfmKneeBack_L',   'r-knee-stretch1', 'r-knee-stretch2'),
    ('DfmKneeBack_R',   'l-knee-stretch1', 'l-knee-stretch2'),
    ('KneeBackTrg_L',   'r-ankle', 'r-knee-stretch2'),
    ('KneeBackTrg_R',   'l-ankle', 'l-knee-stretch2'),

    #('DfmKneeBack_L',   ('r-upper-leg', (0,0,-1)), ('r-ankle', (0,0,-1))),
    #('DfmKneeBack_R',   ('l-upper-leg', (0,0,-1)), ('l-ankle', (0,0,-1))),
    #('KneeBackTrg_L',  'r-ankle', ('r-ankle', (0,0,-1))),
    #('KneeBackTrg_R',  'l-ankle', ('l-ankle', (0,0,-1))),

    # Directions    
    ('DirUpLegFwd_L',     'r-upper-leg', ('r-upper-leg', (0,0,1))),
    ('DirUpLegFwd_R',     'l-upper-leg', ('l-upper-leg', (0,0,1))),
    ('DirUpLegBack_L',    'r-upper-leg', ('r-upper-leg', (0,0,-1))),
    ('DirUpLegBack_R',    'l-upper-leg', ('l-upper-leg', (0,0,-1))),
    ('DirUpLegOut_L',     'r-upper-leg', ('r-upper-leg', (1,0,0))),
    ('DirUpLegOut_R',     'l-upper-leg', ('l-upper-leg', (-1,0,0))),

    ('DirKneeBack_L',     'r-knee', ('r-knee', (0,0,-1))),
    ('DirKneeBack_R',     'l-knee', ('l-knee', (0,0,-1))),
    ('DirKneeInv_L',      'r-knee', ('r-knee', (0,1,0))),
    ('DirKneeInv_R',      'l-knee', ('l-knee', (0,1,0))),
]

#
#   LegArmature
#

footRoll = 3.0665693283081055
toeRoll = 0
footCtrlRoll = 0

LegArmature = [
    # Leg
    ('UpLeg_L',         0, 'Hip_L', F_WIR, L_LLEGFK, NoBB),
    ('LoLeg_L',         0, 'UpLeg_L', F_WIR+F_SCALE, L_LLEGFK, NoBB),
    ('Foot_L',          footRoll, 'LoLeg_L', F_WIR+F_CON, L_LLEGFK+L_LEXTRA, NoBB),
    ('Toe_L',           toeRoll, 'Foot_L', F_WIR, L_LLEGFK+L_LEXTRA, NoBB),
    ('LegFK_L',         footCtrlRoll, 'Toe_L', 0, L_HELP2, NoBB),

    ('UpLeg_R',         -0, 'Hip_R', F_WIR, L_RLEGFK, NoBB),
    ('LoLeg_R',         -0, 'UpLeg_R', F_WIR+F_SCALE, L_RLEGFK, NoBB),
    ('Foot_R',          -footRoll, 'LoLeg_R', F_WIR+F_CON, L_RLEGFK+L_REXTRA, NoBB),
    ('Toe_R',           -toeRoll, 'Foot_R', F_WIR, L_RLEGFK+L_REXTRA, NoBB),
    ('LegFK_R',         footCtrlRoll, 'Toe_R', 0, L_HELP2, NoBB),  
    
    # IK Leg
    
    ('UpLegIK_L',       0, 'Hip_L', 0, L_HELP2, NoBB),
    ('LoLegIK_L',       0, 'UpLegIK_L', 0, L_HELP2, NoBB),
    ('LegIK_L',         -footCtrlRoll, Master, F_WIR, L_LLEGIK, NoBB),
    ('ToeRev_L',        0, 'LegIK_L', F_WIR, L_LLEGIK, NoBB),
    ('FootRev_L',       0, 'ToeRev_L', F_WIR, L_LLEGIK, NoBB),
    ('Ankle_L',         0, Master, F_WIR, L_LEXTRA, NoBB),
    ('AnkleIK_L',       0, 'FootRev_L', 0, L_HELP2, NoBB),

    ('UpLegIK_R',       -0, 'Hip_R', 0, L_HELP2, NoBB),
    ('LoLegIK_R',       -0, 'UpLegIK_R', 0, L_HELP2, NoBB),
    ('LegIK_R',         -footCtrlRoll, Master, F_WIR, L_RLEGIK, NoBB),
    ('ToeRev_R',        0, 'LegIK_R', F_WIR, L_RLEGIK, NoBB),
    ('FootRev_R',       0, 'ToeRev_R', F_WIR, L_RLEGIK, NoBB),
    ('Ankle_R',         0, Master, F_WIR, L_REXTRA, NoBB),
    ('AnkleIK_R',       0, 'FootRev_L', 0, L_HELP2, NoBB),

    # Tweaks
    ('UpLegVec_L',      0, 'Hip_L', 0, L_HELP, NoBB),
    ('UpLegVec_R',      0, 'Hip_R', 0, L_HELP, NoBB),
    ('UpLegVecNeg_L',   -90*D, 'UpLegVec_L', 0, L_HELP, NoBB),
    ('UpLegVecNeg_R',   90*D, 'UpLegVec_R', 0, L_HELP, NoBB),
    
    # Deform
    ('DfmUpLeg1_L',      0, 'Hip_L', F_DEF, L_DEF, NoBB),
    ('DfmUpLeg2_L',      0, 'UpLeg_L', F_DEF, L_DEF, NoBB),
    ('DfmLoLeg_L',      0, 'LoLeg_L', F_DEF, L_DEF, NoBB),
    ('DfmLoLegFan_L',   0, 'UpLeg_L', F_DEF, L_DEF, NoBB),
    ('DfmFoot_L',       footRoll, 'Foot_L', F_DEF, L_DEF, NoBB),
    ('DfmToe_L',        toeRoll, 'Toe_L', F_DEF, L_DEF, NoBB),

    ('DfmUpLeg1_R',      0, 'Hip_R', F_DEF, L_DEF, NoBB),
    ('DfmUpLeg2_R',      0, 'UpLeg_R', F_DEF, L_DEF, NoBB),
    ('DfmLoLeg_R',      -0, 'LoLeg_R', F_DEF, L_DEF, NoBB),
    ('DfmLoLegFan_R',   -0, 'UpLeg_R', F_DEF, L_DEF, NoBB),
    ('DfmFoot_R',       -footRoll, 'Foot_R', F_DEF, L_DEF, NoBB),
    ('DfmToe_R',        -toeRoll, 'Toe_R', F_DEF, L_DEF, NoBB),

    # Pole targets
    #('LegTrg_L',        0.0, 'Hip_L', 0, L_HELP2, NoBB),
    ('KneePT_L',        0.0, 'FootRev_L', F_WIR, L_LLEGIK+L_LEXTRA, NoBB),
    ('KneePTFK_L',      0.0, 'UpLeg_L', 0, L_HELP2, NoBB),
    ('KneeLinkPT_L',    0.0, 'UpLeg_L', F_RES, L_LLEGIK+L_LEXTRA, NoBB),
    ('FootPT_L',        0.0, 'FootRev_L', 0, L_HELP2, NoBB),
    ('ToePT_L',         0.0, 'ToeRev_L', 0, L_HELP2, NoBB),

    #('LegTrg_R',        0.0, 'Hip_R', 0, L_HELP2, NoBB),
    ('KneePT_R',        0.0, 'FootRev_R', F_WIR, L_RLEGIK+L_REXTRA, NoBB),
    ('KneePTFK_R',      0.0, 'UpLeg_R', 0, L_HELP2, NoBB),
    ('KneeLinkPT_R',    0.0, 'UpLeg_R', F_RES, L_RLEGIK+L_REXTRA, NoBB),
    ('FootPT_R',        0.0, 'FootRev_R', 0, L_HELP2, NoBB),
    ('ToePT_R',         0.0, 'ToeRev_R', 0, L_HELP2, NoBB),

    # Muscles
    ('LegOutTrg_L',     0, 'DfmUpLeg1_L', 0, L_HELP, NoBB),
    ('LegOutTrg_R',     0, 'DfmUpLeg1_R', 0, L_HELP, NoBB),
    ('DfmLegOut_L',     0, 'DfmHips', F_DEF, L_MSCL, NoBB),
    ('DfmLegOut_R',     0, 'DfmHips', F_DEF, L_MSCL, NoBB),

    #('DfmLegFront_L',   0, 'DfmHips', F_DEF, L_MSCL, NoBB),
    #('DfmLegFront_R',   0, 'DfmHips', F_DEF, L_MSCL, NoBB),
    #('LegFrontTrg_L',   0, 'DfmUpLeg1_L', 0, L_HELP, NoBB),
    #('LegFrontTrg_R',   0, 'DfmUpLeg1_R', 0, L_HELP, NoBB),

    # Fan bones
    ('DfmHipFan_L',     0, 'Hip_L', F_DEF, L_MSCL, NoBB),
    ('DfmHipFan_R',     0, 'Hip_R', F_DEF, L_MSCL, NoBB),
    
    ('DfmKneeFan_L',   0, 'DfmUpLeg2_L', F_DEF, L_MSCL, NoBB),
    ('DfmKneeFan_R',   0, 'DfmUpLeg2_R', F_DEF, L_MSCL, NoBB),

    ('KneeBackTrg_L',   0, 'DfmLoLeg_L', 0, L_HELP, NoBB),
    ('KneeBackTrg_R',   0, 'DfmLoLeg_R', 0, L_HELP, NoBB),
    ('DfmKneeBack_L',   0, 'DfmUpLeg2_L', F_DEF, L_MSCL, NoBB),
    ('DfmKneeBack_R',   0, 'DfmUpLeg2_R', F_DEF, L_MSCL, NoBB),

    # Directions
    ('DirUpLegFwd_L',       180*D, 'Hip_L', 0, L_HELP, NoBB),
    ('DirUpLegFwd_R',       180*D, 'Hip_R', 0, L_HELP, NoBB),
    ('DirUpLegBack_L',      0*D, 'Hip_L', 0, L_HELP, NoBB),
    ('DirUpLegBack_R',      0*D, 'Hip_R', 0, L_HELP, NoBB),
    ('DirUpLegOut_L',       -90*D, 'Hip_L', 0, L_HELP, NoBB), 
    ('DirUpLegOut_R',       90*D, 'Hip_R', 0, L_HELP, NoBB),

    ('DirKneeBack_L',       0*D, 'UpLeg_L', 0, L_HELP, NoBB),
    ('DirKneeBack_R',       0*D, 'UpLeg_R', 0, L_HELP, NoBB),
    ('DirKneeInv_L',        0*D, 'UpLeg_L', 0, L_HELP, NoBB),
    ('DirKneeInv_R',        0*D, 'UpLeg_R', 0, L_HELP, NoBB),
]

if MuscleBones:
    LegArmature += [

    # Pubis
    ('Pubis_L',            0, 'DfmUpLeg1_L', 0, L_HELP, NoBB),
    ('Pubis_R',            0, 'DfmUpLeg1_R', 0, L_HELP, NoBB),

    # Muscles
    ('DfmLegback_L',    0, 'DfmHips', F_DEF, L_MSCL, NoBB),
    ('DfmLegback_R',    0, 'DfmHips', F_DEF, L_MSCL, NoBB),
    ('DfmLegIn_L',      0, 'DfmHips', F_DEF, L_MSCL, NoBB),
    ('DfmLegIn_R',      0, 'DfmHips', F_DEF, L_MSCL, NoBB),

    ('LegbackTrg_L',    0, 'DfmUpLeg1_L', 0, L_HELP, NoBB),
    ('LegbackTrg_R',    0, 'DfmUpLeg1_R', 0, L_HELP, NoBB),
    ('LegInTrg_L',      0, 'DfmUpLeg1_L', 0, L_HELP, NoBB),
    ('LegInTrg_R',      0, 'DfmUpLeg1_R', 0, L_HELP, NoBB),
    
]

#
#   LegControlPoses(fp):
#

limUpLeg_L = (-160*D,120*D, -90*D,90*D, -170*D,80*D)
limUpLeg_R = (-160*D,120*D, -90*D,90*D, -80*D,170*D)

limLoLeg_L = (-20*D,170*D,-40*D,40*D, -40*D,40*D)
limLoLeg_R = (-20*D,170*D,-40*D,40*D, -40*D,40*D)

limFoot_L = (-90*D,45*D, -30*D,15*D, 0*D,0*D)
limFoot_R = (-90*D,45*D, -15*D,30*D, 0*D,0*D)

limToe_L = (-20*D,60*D, 0,0, 0,0)
limToe_R = (-20*D,60*D, 0,0, 0,0)

limRevFoot_L = (-20*D,60*D, 0,0, 0,0)
limRevFoot_R = (-20*D,60*D, 0,0, 0,0)

limRevToe_L = (-10*D,45*D, 0,0, 0,0)
limRevToe_R = (-10*D,45*D, 0,0, 0,0)


def LegControlPoses(fp):
    deltaKnee = -2.5*D

    # Leg
    addPoseBone(fp, 'Hip_L', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'Hip_R', 'MHBall025', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'UpLeg_L', 'GZM_Circle025', 'FK_L', (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_L, (1,1,1)]),
         #('CopyTrans', 0, 0, ['LegIK', 'UpLegIK_L', 0]),
         ('IK', 0, 0, ['LegIK', 'LoLegIK_L', 1, None, (1,0,0)]),
        ])

    addPoseBone(fp, 'UpLeg_R', 'GZM_Circle025', 'FK_R', (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limUpLeg_R, (1,1,1)]),
         #('CopyTrans', 0, 0, ['LegIK', 'UpLegIK_R', 0]),
         ('IK', 0, 0, ['LegIK', 'LoLegIK_R', 1, None, (1,0,0)]),
        ])

    addPoseBone(fp, 'LoLeg_L', 'GZM_Circle025', 'FK_L', (1,1,1), (0,0,1), (1,0,1), (1,1,1), P_YZX, 
        [
         ('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_L, (1,1,1)]),
         #('CopyTrans', 0, 0, ['LegIK', 'LoLegIK_L', 0]),
         ('IK', 0, 0, ['LegIK', 'AnkleIK_L', 1, None, (1,0,0)]),
        ])

    addPoseBone(fp, 'LoLeg_R', 'GZM_Circle025', 'FK_R', (1,1,1), (0,0,1), (1,0,1), (1,1,1), P_YZX, 
        [
         ('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limLoLeg_R, (1,1,1)]),
         #('CopyTrans', 0, 0, ['LegIK', 'LoLegIK_R', 0]),
         ('IK', 0, 0, ['LegIK', 'AnkleIK_R', 1, None, (1,0,0)]),
        ])

    addPoseBone(fp, 'Foot_L', 'MHFoot', 'FK_L', (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limFoot_L, (1,1,1)]),
         ('IK', 0, 0, ['RevIK', 'FootRev_L', 1, (90*D, 'FootPT_L'), (1,0,1)]),
         ('IK', 0, 0, ['FreeIK', None, 2, None, (True, False,True)])])

    addPoseBone(fp, 'Foot_R', 'MHFoot', 'FK_R', (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limFoot_R, (1,1,1)]),
         ('IK', 0, 0, ['RevIK', 'FootRev_R', 1, (90*D, 'FootPT_R'), (1,0,1)]),
         ('IK', 0, 0, ['FreeIK', None, 2, None, (True, False,True)])])

    addPoseBone(fp, 'Toe_L', 'MHToe_L', 'FK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 0, ['RevIK', 'ToeRev_L', 1, (90*D, 'ToePT_L'), (1,0,1)])])

    addPoseBone(fp, 'Toe_R', 'MHToe_R', 'FK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 0, ['RevIK', 'ToeRev_R', 1, (90*D, 'ToePT_R'), (1,0,1)])])
    
    # Leg IK

    if the.Config.exporting:
        addPoseBone(fp, 'UpLegIK_L', None, 'IK_L', (1,1,1), (0,0,0), (1,0,1), 
                    ((1,1,1), (0,0,0), 0.05, limUpLeg_L), 0, [])

        addPoseBone(fp, 'UpLegIK_R', None, 'IK_R', (1,1,1), (0,0,0), (1,0,1), 
                    ((1,1,1), (0,0,0), 0.05, limUpLeg_R), 0, [])

        addPoseBone(fp, 'LoLegIK_L', None, 'IK_L', (1,1,1), (0,1,1), (1,0,1), 
                    ((1,0,0), (0,0,0), 0.05, limLoLeg_L), 0, 
            [('LimitRot', C_OW_LOCAL, 1, ['Hint', (18*D,18*D, 0,0, 0,0), (1,0,0)]),
             ('IK', 0, 1, ['LegIK', 'AnkleIK_L', 2, (-90*D+deltaKnee, 'KneePT_L'), (1,0,0)]),
            ])

        addPoseBone(fp, 'LoLegIK_R', None, 'IK_R', (1,1,1), (0,1,1), (1,0,1), 
                    ((1,0,0), (0,0,0), 0.05, limLoLeg_R), 0, 
            [('LimitRot', C_OW_LOCAL, 1, ['Hint', (18*D,18*D, 0,0, 0,0), (1,0,0)]),
             ('IK', 0, 1, ['LegIK', 'AnkleIK_R', 2, (-90*D-deltaKnee, 'KneePT_R'), (1,0,0)])
            ])

        addPoseBone(fp, 'LegIK_L', 'MHFootCtrl_L', 'IK_L', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
            [
            #('ChildOf', C_CHILDOF, 0, ['Hip', 'Hip_L', (1,1,1), (1,1,1), (1,1,1)]),
            ('LimitDist', 0, 1, ['DistHip', 'Hip_L', 'LIMITDIST_INSIDE'])])

        addPoseBone(fp, 'LegIK_R', 'MHFootCtrl_R', 'IK_R', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
            [
            #('ChildOf', C_CHILDOF, 0, ['Hip', 'Hip_R', (1,1,1), (1,1,1), (1,1,1)]),
            ('LimitDist', 0, 1, ['DistHip', 'Hip_R', 'LIMITDIST_INSIDE'])])

        addPoseBone(fp, 'FootRev_L', 'MHRevFoot', 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
            [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevFoot_L, (1,1,1)])])

        addPoseBone(fp, 'FootRev_R', 'MHRevFoot', 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0,
            [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevFoot_R, (1,1,1)])])

        addPoseBone(fp, 'ToeRev_L', 'MHRevToe', 'IK_L', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
            [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevToe_L, (1,1,1)])])

        addPoseBone(fp, 'ToeRev_R', 'MHRevToe', 'IK_R', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, 
            [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limRevToe_R, (1,1,1)])])
    
        addPoseBone(fp, 'Ankle_L', 'MHBall025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

        addPoseBone(fp, 'Ankle_R', 'MHBall025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

        addPoseBone(fp, 'AnkleIK_L', None, None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
            [('CopyLoc', 0, 1, ['Foot', 'FootRev_L', (1,1,1), (0,0,0), 1, False]),
             ('CopyLoc', 0, 0, ['Ankle', 'Ankle_L', (1,1,1), (0,0,0), 0, False]) ])

        addPoseBone(fp, 'AnkleIK_R', None, None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0,
            [('CopyLoc', 0, 1, ['Foot', 'FootRev_R', (1,1,1), (0,0,0), 1, False]),
             ('CopyLoc', 0, 0, ['Ankle', 'Ankle_R', (1,1,1), (0,0,0), 0, False]) ])


        # Pole target

        addPoseBone(fp, 'KneePT_L', 'MHCube025', 'IK_L', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

        addPoseBone(fp, 'KneeLinkPT_L', None, 'IK_L', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
            [('StretchTo', 0, 1, ['Stretch', 'KneePT_L', 0, 1, 3.0])])

        addPoseBone(fp, 'KneePT_R', 'MHCube025', 'IK_R', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

        addPoseBone(fp, 'KneeLinkPT_R', None, 'IK_R', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
            [('StretchTo', 0, 1, ['Stretch', 'KneePT_R', 0, 1, 3.0])])


    # Upper leg deform 

    addPoseBone(fp, 'UpLegVec_L', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
        [('IK', 0, 1, ['IK', 'LoLeg_L', 1, None, (True, False,True)])])

    addPoseBone(fp, 'DfmUpLeg1_L', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
        [('IK', 0, 1, ['IK', 'LoLeg_L', 1, None, (True, False,True)])])


    addPoseBone(fp, 'UpLegVec_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
        [('IK', 0, 1, ['IK', 'LoLeg_R', 1, None, (True, False,True)])])

    addPoseBone(fp, 'DfmUpLeg1_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
        [('IK', 0, 1, ['IK', 'LoLeg_R', 1, None, (True, False,True)])])


    # Lower leg deform
    
    addPoseBone(fp, 'DfmLoLeg_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'Foot_L', 0, 1])])

    addPoseBone(fp, 'DfmLoLeg_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'Foot_R', 0, 1])])


    addPoseBone(fp, 'DfmLegOut_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'LegOutTrg_L', 1, 1])])

    addPoseBone(fp, 'DfmLegOut_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'LegOutTrg_R', 1, 1])])

    #addPoseBone(fp, 'DfmLegFront_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
    #    [('StretchTo', 0, 1, ['Stretch', 'LegFrontTrg_L', 1, 1])])

    #addPoseBone(fp, 'DfmLegFront_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
    #    [('StretchTo', 0, 1, ['Stretch', 'LegFrontTrg_R', 1, 1])])

    addPoseBone(fp, 'DfmKneeBack_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'KneeBackTrg_L', 1, 1])])

    addPoseBone(fp, 'DfmKneeBack_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'KneeBackTrg_R', 1, 1])])


    # Fan bones
    
    addPoseBone(fp, 'DfmHipFan_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', C_LOCAL, 0.5, ['Rot', 'DfmUpLeg1_L', (1,1,1), (0,0,0), False])])

    addPoseBone(fp, 'DfmHipFan_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', C_LOCAL, 0.5, ['Rot', 'DfmUpLeg1_R', (1,1,1), (0,0,0), False])])

    addPoseBone(fp, 'DfmKneeFan_L', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', C_LOCAL, 0.5, ['Rot', 'LoLeg_L', (1,0,1), (0,0,0), False])])

    addPoseBone(fp, 'DfmKneeFan_R', None, None, (1,1,1), (1,0,1), (1,1,1), (1,1,1), 0,
        [('CopyRot', C_LOCAL, 0.5, ['Rot', 'LoLeg_R', (1,0,1), (0,0,0), False])])

    if not MuscleBones:
        return
        
    # Tweak
    """
    addPoseBone(fp, 'DfmButt_L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, 
        [('StretchTo', 0, 1, ['Stretch', 'Butt_L', 0, 1])])

    addPoseBone(fp, 'Butt_L', 'MHCube01', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'DfmButt_R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'Butt_R', 0, 1])])

    addPoseBone(fp, 'Butt_R', 'MHCube01', None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])
    """
    # Muscles

    addPoseBone(fp, 'DfmLegback_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'LegbackTrg_L', 1, 1])])

    addPoseBone(fp, 'DfmLegback_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'LegbackTrg_R', 1, 1])])

    addPoseBone(fp, 'DfmLegIn_L', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'LegInTrg_L', 1, 1])])

    addPoseBone(fp, 'DfmLegIn_R', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'LegInTrg_R', 1, 1])])

    return

#
#   LegPropLRDrivers
#   (Bone, Name, Props, Expr)
#

LegPropLRDrivers = [
    ('UpLeg', 'LegIK', ['LegIk'], 'x1'),
    ('LoLeg', 'LegIK', ['LegIk'], 'x1'),
    ('Foot', 'RevIK', ['LegIk', 'LegIkToAnkle'], 'x1*(1-x2)'),
    ('Foot', 'FreeIK', ['LegIk'], '1-x1'),
    ('Toe', 'RevIK', ['LegIk', 'LegIkToAnkle'], 'x1*(1-x2)'),
    ('LegIK', 'DistHip', ['LegStretch'], '1-x1'),
]

SoftLegPropLRDrivers = [
    #('KneePT', 'Foot', ['KneeFollowsFoot'], 'x1'),
    #('KneePT', 'Hip', ['KneeFollowsHip', 'KneeFollowsFoot'], 'x1*(1-x2)'),  
    ('AnkleIK', 'Foot', ['LegIkToAnkle'], '1-x1'),
    ('AnkleIK', 'Ankle', ['LegIkToAnkle'], 'x1'),
]

LegPropDrivers = [
    ('UpLeg_L', 'LimitRot', ['RotationLimits', 'LegIk_L'], 'x1*(1-x2)'),
    ('LoLeg_L', 'LimitRot', ['RotationLimits', 'LegIk_L'], 'x1*(1-x2)'),    
    ('Foot_L', 'LimitRot', ['RotationLimits', 'LegIk_L'], 'x1*(1-x2)'),    

    ('UpLeg_R', 'LimitRot', ['RotationLimits', 'LegIk-R'], 'x1*(1-x2)'),
    ('LoLeg_R', 'LimitRot', ['RotationLimits', 'LegIk_R'], 'x1*(1-x2)'),    
    ('Foot_R', 'LimitRot', ['RotationLimits', 'LegIk_R'], 'x1*(1-x2)'),    
]

#
#   LegDeformDrivers
#   Bone : (constraint, driver, rotdiff, keypoints)
#

LegDeformDrivers = []

#
#   LegShapeDrivers
#   Shape : (driver, rotdiff, keypoints)
#

LegShapeDrivers = {
}

expr90 = "%.3f*(1-%.3f*x1)" % (90.0/90.0, 2/pi)
expr70 = "%.3f*(1-%.3f*x1)" % (90.0/70.0, 2/pi)
expr60 = "%.3f*(1-%.3f*x1)" % (90.0/60.0, 2/pi)
expr45 = "%.3f*(1-%.3f*x1)" % (90.0/45.0, 2/pi)
expr90_90 = "%.3f*max(1-%.3f*x1,0)*max(1-%.3f*x2,0)" % (90.0/90.0, 2/pi, 2/pi)


HipTargetDrivers = []
"""
    ("legs-forward-90", "LR", expr90,
        [("UpLegVec", "DirUpLegFwd")]),
    ("legs-back-60", "LR", expr60,
        [("UpLegVec", "DirUpLegBack")]),
    ("legs-out-90", "LR", expr90_90,
        [("UpLegVec", "DirUpLegOut"),
         ("UpLeg", "UpLegVec")]),
    ("legs-out-90-neg-90", "LR", expr90_90,
        [("UpLegVec", "DirUpLegOut"),
         ("UpLeg", "UpLegVecNeg")]),
]
"""
KneeTargetDrivers = [
#    ("lolegs-back-90", "LR", expr90,
#        [("LoLeg", "DirKneeBack")]),
#    ("lolegs-back-135", "LR", expr45,
#        [("LoLeg", "DirKneeInv")]),
]


