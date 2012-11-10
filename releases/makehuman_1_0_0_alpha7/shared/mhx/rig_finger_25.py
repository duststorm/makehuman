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
Finger bone definitions 

"""

import mhx_globals as the
from mhx_globals import *
from mhx_rig import addPoseBone

FingerJoints = [
    #('l-hand-2',       'j', 'l-hand-2'),
    #('l-hand-3',       'j', 'l-hand-3'),
    #('r-hand-2',       'j', 'r-hand-2'),
    #('r-hand-3',       'j', 'r-hand-3'),
    ('r-hand-2',        'l', ((0.7, 'r-hand'), (0.3, 'r-finger-5-1'))),
    ('r-hand-3',        'l', ((0.7, 'r-hand'), (0.3, 'r-finger-2-1'))),
    ('l-hand-2',        'l', ((0.7, 'l-hand'), (0.3, 'l-finger-5-1'))),
    ('l-hand-3',        'l', ((0.7, 'l-hand'), (0.3, 'l-finger-2-1'))),
]

FingerHeadsTails = [
    ('Finger-1-1_L',        'r-finger-1-1', 'r-finger-1-2'),
    ('Finger-1-2_L',        'r-finger-1-2', 'r-finger-1-3'),
    ('Finger-1-3_L',        'r-finger-1-3', 'r-finger-1-4'),
    ('Finger-2-1_L',        'r-finger-2-1', 'r-finger-2-2'),
    ('Finger-2-2_L',        'r-finger-2-2', 'r-finger-2-3'),
    ('Finger-2-3_L',        'r-finger-2-3', 'r-finger-2-4'),
    ('Finger-3-1_L',        'r-finger-3-1', 'r-finger-3-2'),
    ('Finger-3-2_L',        'r-finger-3-2', 'r-finger-3-3'),
    ('Finger-3-3_L',        'r-finger-3-3', 'r-finger-3-4'),
    ('Finger-4-1_L',        'r-finger-4-1', 'r-finger-4-2'),
    ('Finger-4-2_L',        'r-finger-4-2', 'r-finger-4-3'),
    ('Finger-4-3_L',        'r-finger-4-3', 'r-finger-4-4'),
    ('Finger-5-1_L',        'r-finger-5-1', 'r-finger-5-2'),
    ('Finger-5-2_L',        'r-finger-5-2', 'r-finger-5-3'),
    ('Finger-5-3_L',        'r-finger-5-3', 'r-finger-5-4'),

    ('Finger-1-1_R',        'l-finger-1-1', 'l-finger-1-2'),
    ('Finger-1-2_R',        'l-finger-1-2', 'l-finger-1-3'),
    ('Finger-1-3_R',        'l-finger-1-3', 'l-finger-1-4'),
    ('Finger-2-1_R',        'l-finger-2-1', 'l-finger-2-2'),
    ('Finger-2-2_R',        'l-finger-2-2', 'l-finger-2-3'),
    ('Finger-2-3_R',        'l-finger-2-3', 'l-finger-2-4'),
    ('Finger-3-1_R',        'l-finger-3-1', 'l-finger-3-2'),
    ('Finger-3-2_R',        'l-finger-3-2', 'l-finger-3-3'),
    ('Finger-3-3_R',        'l-finger-3-3', 'l-finger-3-4'),
    ('Finger-4-1_R',        'l-finger-4-1', 'l-finger-4-2'),
    ('Finger-4-2_R',        'l-finger-4-2', 'l-finger-4-3'),
    ('Finger-4-3_R',        'l-finger-4-3', 'l-finger-4-4'),
    ('Finger-5-1_R',        'l-finger-5-1', 'l-finger-5-2'),
    ('Finger-5-2_R',        'l-finger-5-2', 'l-finger-5-3'),
    ('Finger-5-3_R',        'l-finger-5-3', 'l-finger-5-4'),

    ('Finger-1_R',          'l-finger-1-2', 'l-finger-1-4'),
    ('Finger-2_R',          'l-finger-2-1', 'l-finger-2-4'),
    ('Finger-3_R',          'l-finger-3-1', 'l-finger-3-4'),
    ('Finger-4_R',          'l-finger-4-1', 'l-finger-4-4'),
    ('Finger-5_R',          'l-finger-5-1', 'l-finger-5-4'),

    ('Finger-1_L',          'r-finger-1-2', 'r-finger-1-4'),
    ('Finger-2_L',          'r-finger-2-1', 'r-finger-2-4'),
    ('Finger-3_L',          'r-finger-3-1', 'r-finger-3-4'),
    ('Finger-4_L',          'r-finger-4-1', 'r-finger-4-4'),
    ('Finger-5_L',          'r-finger-5-1', 'r-finger-5-4'),

    ('Wrist-1_L',           'r-hand', 'r-hand-3'),
    ('Wrist-2_L',           'r-hand', 'r-hand-2'),
    ('Palm-1_L',            'r-hand', 'r-finger-1-1'),
    ('Palm-2_L',            'r-hand-3', 'r-finger-2-1'),
    ('Palm-3_L',            'r-hand-3', 'r-finger-3-1'),
    ('Palm-4_L',            'r-hand-2', 'r-finger-4-1'),
    ('Palm-5_L',            'r-hand-2', 'r-finger-5-1'),

    ('Wrist-1_R',           'l-hand', 'l-hand-3'),
    ('Wrist-2_R',           'l-hand', 'l-hand-2'),
    ('Palm-1_R',            'l-hand', 'l-finger-1-1'),
    ('Palm-2_R',            'l-hand-3', 'l-finger-2-1'),
    ('Palm-3_R',            'l-hand-3', 'l-finger-3-1'),
    ('Palm-4_R',            'l-hand-2', 'l-finger-4-1'),
    ('Palm-5_R',            'l-hand-2', 'l-finger-5-1'),
]

#
#   FingerArmature
#

ThumbRoll = 90*D

FingerArmature = [
    # Palm
    ('Wrist-1_L',       0.0, 'Hand_L', F_DEF, L_LPALM, NoBB),
    ('Wrist-2_L',       0.0, 'Hand_L', F_DEF, L_LPALM, NoBB),
    ('Palm-1_L',        0.0, 'Hand_L', F_DEF, L_LPALM, NoBB),
    ('Palm-2_L',        0.0, 'Wrist-1_L', F_DEF, L_LPALM, NoBB),
    ('Palm-3_L',        0.0, 'Wrist-1_L', F_DEF, L_LPALM, NoBB),
    ('Palm-4_L',        0.0, 'Wrist-2_L', F_DEF, L_LPALM, NoBB),
    ('Palm-5_L',        0.0, 'Wrist-2_L', F_DEF, L_LPALM, NoBB),

    ('Wrist-1_R',       0.0, 'Hand_R', F_DEF, L_RPALM, NoBB),
    ('Wrist-2_R',       0.0, 'Hand_R', F_DEF, L_RPALM, NoBB),
    ('Palm-1_R',        0.0, 'Hand_R', F_DEF, L_RPALM, NoBB),
    ('Palm-2_R',        0.0, 'Wrist-1_R', F_DEF, L_RPALM, NoBB),
    ('Palm-3_R',        0.0, 'Wrist-1_R', F_DEF, L_RPALM, NoBB),
    ('Palm-4_R',        0.0, 'Wrist-2_R', F_DEF, L_RPALM, NoBB),
    ('Palm-5_R',        0.0, 'Wrist-2_R', F_DEF, L_RPALM, NoBB),

    # Fingers
    ('Finger-1-1_L',        ThumbRoll, 'Palm-1_L', F_DEF, L_LHANDFK+L_LHANDIK, NoBB),
    ('Finger-1-2_L',        ThumbRoll, 'Finger-1-1_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-1-3_L',        ThumbRoll, 'Finger-1-2_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-2-1_L',        0.0, 'Palm-2_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-2-2_L',        0.0, 'Finger-2-1_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-2-3_L',        0.0, 'Finger-2-2_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-3-1_L',        0.0, 'Palm-3_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-3-2_L',        0.0, 'Finger-3-1_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-3-3_L',        0.0, 'Finger-3-2_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-4-1_L',        0.0, 'Palm-4_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-4-2_L',        0.0, 'Finger-4-1_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-4-3_L',        0.0, 'Finger-4-2_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-5-1_L',        0.0, 'Palm-5_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-5-2_L',        0.0, 'Finger-5-1_L', F_DEF, L_LHANDFK, NoBB),
    ('Finger-5-3_L',        0.0, 'Finger-5-2_L', F_DEF, L_LHANDFK, NoBB),

    ('Finger-1-1_R',        -ThumbRoll, 'Palm-1_R', F_DEF, L_RHANDFK+L_RHANDIK, NoBB),
    ('Finger-1-2_R',        -ThumbRoll, 'Finger-1-1_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-1-3_R',        -ThumbRoll, 'Finger-1-2_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-2-1_R',        0.0, 'Palm-2_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-2-2_R',        0.0, 'Finger-2-1_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-2-3_R',        0.0, 'Finger-2-2_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-3-1_R',        0.0, 'Palm-3_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-3-2_R',        0.0, 'Finger-3-1_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-3-3_R',        0.0, 'Finger-3-2_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-4-1_R',        0.0, 'Palm-4_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-4-2_R',        0.0, 'Finger-4-1_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-4-3_R',        0.0, 'Finger-4-2_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-5-1_R',        0.0, 'Palm-5_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-5-2_R',        0.0, 'Finger-5-1_R', F_DEF, L_RHANDFK, NoBB),
    ('Finger-5-3_R',        0.0, 'Finger-5-2_R', F_DEF, L_RHANDFK, NoBB),

    # Finger controls
    ('Finger-1_L',      ThumbRoll, 'Finger-1-1_L', F_WIR, L_LHANDIK, NoBB),
    ('Finger-2_L',      0.0, 'Palm-2_L', F_WIR, L_LHANDIK, NoBB),
    ('Finger-3_L',      0.0, 'Palm-3_L', F_WIR, L_LHANDIK, NoBB),
    ('Finger-4_L',      0.0, 'Palm-4_L', F_WIR, L_LHANDIK, NoBB),
    ('Finger-5_L',      0.0, 'Palm-5_L', F_WIR, L_LHANDIK, NoBB),
    
    ('Finger-1_R',      -ThumbRoll, 'Finger-1-1_R', F_WIR, L_RHANDIK, NoBB),
    ('Finger-2_R',      0.0, 'Palm-2_R', F_WIR, L_RHANDIK, NoBB),
    ('Finger-3_R',      0.0, 'Palm-3_R', F_WIR, L_RHANDIK, NoBB),
    ('Finger-4_R',      0.0, 'Palm-4_R', F_WIR, L_RHANDIK, NoBB),
    ('Finger-5_R',      0.0, 'Palm-5_R', F_WIR, L_RHANDIK, NoBB),
]

#
#   defineFingerConstraints():
#

limitRotThumb = ('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-1.37,0.5, 0,0, -60*D,60*D), (1,0,1)]) 
limitRotFingers = ('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-1.37,0.5, 0,0, -30*D,30*D), (1,0,1)]) 

def defineFingerConstraints():
    fconstraints = {}
    for fnum in range(1,6):
        for suffix in ["_L", "_R"]:
            finger = "Finger-%d%s" % (fnum, suffix)
            for lnum in range(1,4):
                if fnum == 1:
                    if lnum == 1:
                        cnss = []
                    else:
                        cnss = [ ('CopyRot', C_LOCAL, 1, ['Rot', finger, (1,0,0), (0,0,0), True]) ]
                    cnss.append( limitRotThumb )
                else:
                    if lnum == 1:
                        cnss = [ ('CopyRot', C_LOCAL, 1, ['Rot', finger, (1,0,1), (0,0,0), True]) ]
                    else:
                        cnss = [ ('CopyRot', C_LOCAL, 1, ['Rot', finger, (1,0,0), (0,0,0), True]) ]
                    cnss.append( limitRotFingers )
                fconstraints["%d-%d%s" % (fnum, lnum, suffix)] = cnss
    return fconstraints
    
fconstraints = defineFingerConstraints()    

#
#   FingerControlPoses(fp):
#

customShape = 'MHCircle05'
customShape = None
        
def FingerControlPoses(fp):
    for suffix in ['_L', '_R']:
        for fnum in range(1,6):
            fing = 'Finger-%d%s' % (fnum, suffix)
            if fnum == 1:
                lim = limitRotThumb
            else:
                lim = limitRotFingers
            addPoseBone(fp, fing, 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [lim])
            
            for lnum in range(1,4):
                if (fnum == 1 and lnum <= 2) or (fnum >= 2 and lnum == 1):
                    rot = (0,1,0)
                    ik = (1,0,1)
                else:
                    rot = (0,1,1)
                    ik = (0,0,1)                
                fing = 'Finger-%d-%d%s' % (fnum, lnum, suffix)
                addPoseBone(fp, fing, customShape, None, (1,1,1), rot, (1,1,1), ik, 0, 
                    fconstraints["%d-%d%s" % (fnum, lnum, suffix)])             

            palm = 'Palm-%d%s' % (fnum, suffix)
            addPoseBone(fp, palm, None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

        addPoseBone(fp, 'Wrist-1%s' % suffix, None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
        addPoseBone(fp, 'Wrist-2%s' % suffix, None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
    return  

#
#   getFingerPropDrivers():
#

def getFingerPropDrivers():
    drivers = []
    for fnum in range(1,6):
        for lnum in range(1,4):
            if (fnum != 1) or (lnum != 1):
                finger = 'Finger-%d-%d' % (fnum,lnum)
                drivers.append( (finger, 'Rot', ['FingerControl'], 'x1') )
    return drivers

