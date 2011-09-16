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
    ('r-shoulder-in',       'v', 14160),
    ('l-shoulder-in',       'v', 14382),
    ('r-uparm0',            'l', ((2.0, 'r-shoulder-in'), (-1.0, 'r-shoulder'))),
    ('l-uparm0',            'l', ((2.0, 'l-shoulder-in'), (-1.0, 'l-shoulder'))),
    
    ('r-deltoidTrg',    	'vl', ((0.5, 3036), (0.5, 3507))),
    ('l-deltoidTrg',   		'vl', ((0.5, 10277), (0.5, 10690))),
    ('r-pect1',        		'v', 3666),
    ('l-pect1',        		'v', 10135),
    ('r-pect2',        		'v', 4167),
    ('l-pect2',        		'v', 10062),
    #('r-trap',       	 	'vo', [2598, -0.079100, -0.017038, -0.048916]),
    #('l-trap',        		'vo', [11068, 0.079100, -0.017038, -0.048916]),
    ('r-lat',        		'v', 2620),
    ('l-lat',        		'v', 10990),
    ('r-deltoid',        	'vl', ((0.5, 4202), (0.5, 4447))),
    ('l-deltoid',        	'vl', ((0.5, 9980), (0.5, 10032))),

    ('r-shoulder-head',     'l', ((0.7, 'r-scapula'), (0.3, 'l-scapula'))),
    ('l-shoulder-head',     'l', ((0.3, 'r-scapula'), (0.7, 'l-scapula'))),

    ('r-shoulder-top',      'v', 2862),
    ('l-shoulder-top',      'v', 10812),
    ('r-shoulder-tail',     'l', ((0.5, 'r-shoulder-top'), (0.5, 'r-uparm0'))),
    ('l-shoulder-tail',     'l', ((0.5, 'l-shoulder-top'), (0.5, 'l-uparm0'))),

    ('sternum-tail',        'v', 7279),
    ('sternum-head',        'l', ((0.5, 'neck'), (0.5, 'sternum-tail'))),
    ('r-shoulder-aim',      'l', ((0.5, 'sternum-head'), (0.5, 'r-shoulder-tail'))),
    ('l-shoulder-aim',      'l', ((0.5, 'sternum-head'), (0.5, 'l-shoulder-tail'))),
    
    ('r-scapula-1',     	 'v', 2602),
    ('r-scapula-2',     	 'v', 2584),
    ('r-scapula-3',     	 'v', 2607),
    ('l-scapula-1',     	 'v', 11008),
    ('l-scapula-2',     	 'v', 11024),
    ('l-scapula-3',     	 'v', 11003),
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

    ('Shoulder_R',            'l-clavicle', 'l-shoulder-tail'),
    ('ShoulderPivot_R',        'l-clavicle', 'l-shoulder-tail'),
    ('ShoulderUp_R',        ('l-shoulder-tail', yunit), ('l-shoulder-tail', ybis)),
    ('ShoulderAim_R',        'l-shoulder-tail', 'l-shoulder-aim'),
    ('DfmShoulder_R',        'l-clavicle', 'l-shoulder-tail'),

    ('ShoulderEnd_L',        'r-uparm0', ('r-uparm0', yunit)),
    ('ShoulderEnd_R',        'l-uparm0', ('l-uparm0', yunit)),
    ('ArmLoc_L',            'r-uparm0', ('r-uparm0', yunit)),
    ('ArmLoc_R',            'l-uparm0', ('l-uparm0', yunit)),

	# Scapula
	
    ('DfmScapula1_L',        'r-scapula-1', 'r-scapula-2'),
    ('DfmScapula2_L',        'r-scapula-2', 'r-scapula-3'),
    ('DfmScapula1_R',        'l-scapula-1', 'l-scapula-2'),
    ('DfmScapula2_R',        'l-scapula-2', 'l-scapula-3'),

    # Muscles
    
    ('DeltoidTrg_L',        'r-uparm0', 'r-deltoidTrg'),
    ('DeltoidTrg_R',        'l-uparm0', 'l-deltoidTrg'),
    ('DfmPect1_L',            'r-pect1', 'r-uparm0'),
    ('DfmPect1_R',            'l-pect1', 'l-uparm0'),
    ('DfmPect2_L',            'r-pect2', 'r-uparm0'),
    ('DfmPect2_R',            'l-pect2', 'l-uparm0'),
    ('DfmLat_L',            'r-lat', 'r-uparm0'),
    ('DfmLat_R',            'l-lat', 'l-uparm0'),
    #('DfmTrap_L',            'r-trap', 'r-uparm0'),
    #('DfmTrap_R',            'l-trap', 'l-uparm0'),
    ('DfmDeltoid_L',            'r-deltoid', 'r-deltoidTrg'),
    ('DfmDeltoid_R',            'l-deltoid', 'l-deltoidTrg'),
]

'''
    # Rotation diffs
    ('BendArmDown_L',        'r-uparm0', ('r-uparm0', (0,-1,0))),
    ('BendArmDown_R',        'l-uparm0', ('l-uparm0', (0,-1,0))),
    ('BendArmUp_L',            'r-uparm0', ('r-uparm0', (0,1,0))),
    ('BendArmUp_R',            'l-uparm0', ('l-uparm0', (0,1,0))),
    ('BendArmForward_L',    'r-uparm0', ('r-uparm0', (0,0,1))),
    ('BendArmForward_R',    'l-uparm0', ('l-uparm0', (0,0,1))),
    ('BendArmBack_L',        'r-uparm0', ('r-uparm0', (0,0,-1))),
    ('BendArmBack_R',        'l-uparm0', ('l-uparm0', (0,0,-1))),

    ('BendShoulderUp_L',    'r-shoulder-head', ('r-shoulder-head', (0,1,0))),
    ('BendShoulderUp_R',    'l-shoulder-head', ('l-shoulder-head', (0,1,0))),
    ('BendLoArmForward_L',    'r-elbow', ('r-elbow', (0,0,1))),
    ('BendLoArmForward_R',    'l-elbow', ('l-elbow', (0,0,1))),
'''

L_LSHOULDER = L_LARMFK+L_LARMIK+L_SPINEFK+L_SPINEIK
L_RSHOULDER = L_RARMFK+L_RARMIK+L_SPINEFK+L_SPINEIK

ShoulderArmature = [
    ('Sternum',            0.0, 'Spine3', 0, L_HELP, NoBB),
    ('SternumTarget',      0.0, 'Sternum', 0, L_HELP, NoBB),

    # Shoulder
    ('Shoulder_L',         0.0, 'Sternum', F_WIR, L_LSHOULDER, NoBB),
    ('Shoulder_R',         0.0, 'Sternum', F_WIR, L_RSHOULDER, NoBB),
    ('ShoulderEnd_L',      0.0, 'Shoulder_L', 0, L_HELP, NoBB),
    ('ShoulderEnd_R',      0.0, 'Shoulder_R', 0, L_HELP, NoBB),
    ('ArmLoc_L',           0.0, 'ShoulderEnd_L', F_NOROT, L_HELP, NoBB),
    ('ArmLoc_R',           0.0, 'ShoulderEnd_R', F_NOROT, L_HELP, NoBB),

    ('DfmShoulder_L',     0, 'Sternum', F_DEF, L_DMAIN, NoBB),
    ('DfmShoulder_R',        0.0, 'Sternum', F_DEF, L_DMAIN, NoBB),
    
    # Scapula
    ('ShoulderPivot_L',        0.0, 'Sternum', 0, L_HELP, NoBB),
    ('ShoulderUp_L',        0.0, 'ShoulderPivot_L', 0, L_HELP, NoBB),
    ('ShoulderAim_L',        0.0, 'ShoulderPivot_L', 0, L_HELP, NoBB),

    ('ShoulderPivot_R',        0.0, 'Sternum', 0, L_HELP, NoBB),
    ('ShoulderUp_R',        0.0, 'ShoulderPivot_R', 0, L_HELP, NoBB),
    ('ShoulderAim_R',        0.0, 'ShoulderPivot_R', 0, L_HELP, NoBB),

    ('DfmScapula1_L',      0, 'ShoulderAim_L', F_DEF, L_DMAIN, NoBB),
    ('DfmScapula2_L',      0, 'DfmScapula1_L', F_DEF, L_DMAIN, NoBB),
    ('DfmScapula1_R',        0.0, 'ShoulderAim_R', F_DEF, L_DMAIN, NoBB),
    ('DfmScapula2_R',      0, 'DfmScapula1_R', F_DEF, L_DMAIN, NoBB),

	# Muscles
    ('DeltoidTrg_L',    0, 'Shoulder_L', 0, L_HELP, NoBB ),
    ('DeltoidTrg_R',    0, 'Shoulder_R', 0, L_HELP, NoBB ),
    ('DfmPect1_L',            0.0, 'Spine3', F_DEF, L_DEF, NoBB ),
    ('DfmPect1_R',            0.0, 'Spine3', F_DEF, L_DEF, NoBB ),
    ('DfmPect2_L',            0.0, 'Spine3', F_DEF, L_DEF, NoBB ),
    ('DfmPect2_R',            -0.0, 'Spine3', F_DEF, L_DEF, NoBB ),
    ('DfmLat_L',            0, 'Spine3', F_DEF, L_DEF, NoBB ),
    ('DfmLat_R',            0, 'Spine3', F_DEF, L_DEF, NoBB ),
    #('DfmTrap_L',            0.0, 'Spine3', F_DEF, L_DEF, NoBB ),
    #('DfmTrap_R',            0.0, 'Spine3', F_DEF, L_DEF, NoBB ),
    ('DfmDeltoid_L',        0, 'Spine3', F_DEF, L_DEF, NoBB ),
    ('DfmDeltoid_R',        0, 'Spine3', F_DEF, L_DEF, NoBB ),
]

""" 
    # Rotation diffs
    ('BendArmDown_L',     90*D, 'Shoulder_L', 0, L_HELP, NoBB),
    ('BendArmDown_R',     -90*D, 'Shoulder_R', 0, L_HELP, NoBB),
    ('BendArmUp_L',       -90*D, 'Shoulder_L', 0, L_HELP, NoBB),
    ('BendArmUp_R',       90*D, 'Shoulder_R', 0, L_HELP, NoBB),
    ('BendArmForward_L',  0*D, 'Shoulder_L', 0, L_HELP, NoBB),
    ('BendArmForward_R',  0*D, 'Shoulder_R', 0, L_HELP, NoBB),
    ('BendArmBack_L',     0*D, 'Shoulder_L', 0, L_HELP, NoBB),
    ('BendArmBack_R',     0*D, 'Shoulder_R', 0, L_HELP, NoBB),
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

    # Deform

    copyDeform(fp, 'DfmShoulder_L', 'Shoulder_L', 0, U_LOC+U_ROT, None, [])
    copyDeform(fp, 'DfmShoulder_R', 'Shoulder_R', 0, U_LOC+U_ROT, None, [])
    
    # Shoulder deform
    addPoseBone(fp, 'DeltoidTrg_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0, [])

    addPoseBone(fp, 'DeltoidTrg_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0, [])

    addPoseBone(fp, 'DfmPect1_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch_To', 'ArmLoc_L', 0])])

    addPoseBone(fp, 'DfmPect2_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch_To', 'ArmLoc_L', 0])])

    addPoseBone(fp, 'DfmPect1_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch_To', 'ArmLoc_R', 0])])

    addPoseBone(fp, 'DfmPect2_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch_To', 'ArmLoc_R', 0])])

    addPoseBone(fp, 'DfmLat_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch_To', 'ArmLoc_L', 0])])

    addPoseBone(fp, 'DfmLat_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch_To', 'ArmLoc_R', 0])])

    #addPoseBone(fp, 'DfmTrap_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
    #     [('StretchTo', 0, 1, ['Stretch_To', 'ArmLoc_L', 0])])

    #addPoseBone(fp, 'DfmTrap_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
    #    [('StretchTo', 0, 1, ['Stretch_To', 'ArmLoc_R', 0])])

    addPoseBone(fp, 'DfmDeltoid_L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch_To', 'DeltoidTrg_L', 1])])

    addPoseBone(fp, 'DfmDeltoid_R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch_To', 'DeltoidTrg_R', 1])])

	# Scapula
	
    addPoseBone(fp, 'ShoulderPivot_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 0.5, ['Rot', 'Shoulder_L', (1,1,1), (0,0,0), False])])
    
    addPoseBone(fp, 'ShoulderUp_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
    
    addPoseBone(fp, 'ShoulderAim_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 1, ['IK', 'SternumTarget', 1, (90*D, 'ShoulderUp_L'), (True, False,True)])])
    
    
    addPoseBone(fp, 'ShoulderPivot_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('CopyRot', 0, 0.5, ['Rot', 'Shoulder_R', (1,1,1), (0,0,0), False])])
    
    addPoseBone(fp, 'ShoulderUp_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
    
    addPoseBone(fp, 'ShoulderAim_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('IK', 0, 1, ['IK', 'SternumTarget', 1, (90*D, 'ShoulderUp_R'), (True, False,True)])])

    return
    
#
#    ShoulderDeformDrivers
#    (Bone, constraint, driver, rotdiff, keypoints)
#

ShoulderDeformDrivers = []


