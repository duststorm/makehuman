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
Face bone definitions 

"""

import mhx_globals as the
from mhx_globals import *
from mhx_rig import addPoseBone, writeDrivers

FaceJoints = [
    ('head-end',        'l', ((2.0, 'head'), (-1.0, 'neck'))),
    ('r-mouth',            'v', 2490),
    ('l-mouth',            'v', 8907),

    ('mid-eyes',        'l', ((0.5, 'l-eye'), (0.5, 'r-eye'))),
    ('gaze',            'o', ('mid-eyes', [0.0, 0.0, 5.2])),
    ('gaze-target',        'o', ('mid-eyes', [0.0, 0.0, 4.2])),
    ('l-gaze',            'o', ('l-eye', [0.0, 0.0, 5.0])),
    ('l-gaze-target',    'o', ('l-eye', [0.0, 0.0, 4.5])),
    ('r-gaze',            'o', ('r-eye', [0.0, 0.0, 5.0])),
    ('r-gaze-target',    'o', ('r-eye', [0.0, 0.0, 4.5])),
]

FaceHeadsTails = [
    ('Jaw',                    'mouth', 'jaw'),
    ('TongueBase',            'tongue-1', 'tongue-2'),
    ('TongueMid',            'tongue-2', 'tongue-3'),
    ('TongueTip',            'tongue-3', 'tongue-4'),

    ('Eye_R',                'l-eye', 'l-eye-target'),
    ('DfmUpLid_R',            'l-eye', 'l-upperlid'),
    ('DfmLoLid_R',            'l-eye', 'l-lowerlid'),
    ('Eye_L',                'r-eye', 'r-eye-target'),
    ('DfmUpLid_L',            'r-eye', 'r-upperlid'),
    ('DfmLoLid_L',            'r-eye', 'r-lowerlid'),

    ('Gaze',                'gaze', 'gaze-target'),
    ('Gaze_R',                'l-gaze', 'l-gaze-target'),
    ('Gaze_L',                'r-gaze', 'r-gaze-target'),
]


FaceArmature = [
    ('Jaw',                0.0, 'Head', F_DEF+F_WIR, L_HEAD, NoBB),
    ('TongueBase',        0.0, 'Jaw', F_DEF+F_WIR, L_HEAD, NoBB),
    ('TongueMid',        0.0, 'TongueBase', F_DEF+F_WIR, L_HEAD, NoBB),
    ('TongueTip',        0.0, 'TongueMid', F_DEF+F_WIR, L_HEAD, NoBB),
    ('Gaze',            pi, (None, 'Head'), F_WIR, L_HEAD, NoBB),
    ('Gaze_R',            pi, 'Gaze', F_WIR, L_HEAD, NoBB),
    ('Gaze_L',            pi, 'Gaze', F_WIR, L_HEAD, NoBB),
    ('Eye_R',            0.0, 'Head', F_DEF, L_DEF, NoBB),
    ('Eye_L',            0.0, 'Head', F_DEF, L_DEF, NoBB),
    ('DfmUpLid_R',        0.279253, 'Head', F_DEF, L_DEF, NoBB),
    ('DfmLoLid_R',        0.0, 'Head', F_DEF, L_DEF, NoBB),
    ('DfmUpLid_L',        -0.279253, 'Head', F_DEF, L_DEF, NoBB),
    ('DfmLoLid_L',        0.0, 'Head', F_DEF, L_DEF, NoBB),
]


#
#    FaceControlPoses(fp):
#

def FaceControlPoses(fp):
    addPoseBone(fp, 'Jaw', 'MHJaw', None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-5*D,45*D, 0,0, -20*D,20*D), (1,1,1)])])

    addPoseBone(fp, 'TongueBase', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, 'TongueMid', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, 'TongueTip', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, 'Gaze', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
        [('ChildOf', C_CHILDOF, 1, ['Head', 'Head', (1,1,1), (1,1,1), (1,1,1)]),
         ('ChildOf', C_CHILDOF, 0, ['World', 'MasterFloor', (1,1,1), (1,1,1), (1,1,1)]),
        ])

    addPoseBone(fp, 'Gaze_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'Gaze_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'DfmUpLid_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'DfmLoLid_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'DfmUpLid_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'DfmLoLid_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'Eye_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('IK', 0, 1, ['IK', 'Gaze_R', 1, None, (True, False,False), 1.0])])

    addPoseBone(fp, 'Eye_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('IK', 0, 1, ['IK', 'Gaze_L', 1, None, (True, False,False), 1.0])])
    return

#
#    FaceDeformDrivers(fp):
#

def FaceDeformDrivers(fp):
    lidBones = [
    ('DfmUpLid_L', 'PUpLid_L', (0, 40*D)),
    ('DfmLoLid_L', 'PLoLid_L', (0, 20*D)),
    ('DfmUpLid_R', 'PUpLid_R', (0, 40*D)),
    ('DfmLoLid_R', 'PLoLid_R', (0, 20*D)),
    ]

    drivers = []
    for (driven, driver, coeff) in lidBones:
        drivers.append(    (driven, 'ROTQ', 'AVERAGE', None, 1, coeff,
         [("var", 'TRANSFORMS', [('OBJECT', the.Human, driver, 'LOC_Z', C_LOC)])]) )
    writeDrivers(fp, True, drivers)
    return

#
#   FacePropDrivers
#   (Bone, Name, Props, Expr)
#

FacePropDrivers = []

SoftFacePropDrivers = [
    ('Gaze', 'Head', ['GazeFollowsHead'], 'x1'),
    ('Gaze', 'World', ['GazeFollowsHead'], '1-x1'),
]

