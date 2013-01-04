#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Finger bone definitions 
"""

from . import the
from the import *
from . import posebone
from posebone import addPoseBone

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
    ('Thumb-1_L',        'r-finger-1-1', 'r-finger-1-2'),
    ('Thumb-2_L',        'r-finger-1-2', 'r-finger-1-3'),
    ('Thumb-3_L',        'r-finger-1-3', 'r-finger-1-4'),
    ('Index-1_L',        'r-finger-2-1', 'r-finger-2-2'),
    ('Index-2_L',        'r-finger-2-2', 'r-finger-2-3'),
    ('Index-3_L',        'r-finger-2-3', 'r-finger-2-4'),
    ('Middle-1_L',        'r-finger-3-1', 'r-finger-3-2'),
    ('Middle-2_L',        'r-finger-3-2', 'r-finger-3-3'),
    ('Middle-3_L',        'r-finger-3-3', 'r-finger-3-4'),
    ('Ring-1_L',        'r-finger-4-1', 'r-finger-4-2'),
    ('Ring-2_L',        'r-finger-4-2', 'r-finger-4-3'),
    ('Ring-3_L',        'r-finger-4-3', 'r-finger-4-4'),
    ('Pinky-1_L',        'r-finger-5-1', 'r-finger-5-2'),
    ('Pinky-2_L',        'r-finger-5-2', 'r-finger-5-3'),
    ('Pinky-3_L',        'r-finger-5-3', 'r-finger-5-4'),

    ('Thumb-1_R',        'l-finger-1-1', 'l-finger-1-2'),
    ('Thumb-2_R',        'l-finger-1-2', 'l-finger-1-3'),
    ('Thumb-3_R',        'l-finger-1-3', 'l-finger-1-4'),
    ('Index-1_R',        'l-finger-2-1', 'l-finger-2-2'),
    ('Index-2_R',        'l-finger-2-2', 'l-finger-2-3'),
    ('Index-3_R',        'l-finger-2-3', 'l-finger-2-4'),
    ('Middle-1_R',        'l-finger-3-1', 'l-finger-3-2'),
    ('Middle-2_R',        'l-finger-3-2', 'l-finger-3-3'),
    ('Middle-3_R',        'l-finger-3-3', 'l-finger-3-4'),
    ('Ring-1_R',        'l-finger-4-1', 'l-finger-4-2'),
    ('Ring-2_R',        'l-finger-4-2', 'l-finger-4-3'),
    ('Ring-3_R',        'l-finger-4-3', 'l-finger-4-4'),
    ('Pinky-1_R',        'l-finger-5-1', 'l-finger-5-2'),
    ('Pinky-2_R',        'l-finger-5-2', 'l-finger-5-3'),
    ('Pinky-3_R',        'l-finger-5-3', 'l-finger-5-4'),

    ('Thumb_R',          'l-finger-1-2', 'l-finger-1-4'),
    ('Index_R',          'l-finger-2-1', 'l-finger-2-4'),
    ('Middle_R',          'l-finger-3-1', 'l-finger-3-4'),
    ('Ring_R',          'l-finger-4-1', 'l-finger-4-4'),
    ('Pinky_R',          'l-finger-5-1', 'l-finger-5-4'),

    ('Thumb_L',          'r-finger-1-2', 'r-finger-1-4'),
    ('Index_L',          'r-finger-2-1', 'r-finger-2-4'),
    ('Middle_L',          'r-finger-3-1', 'r-finger-3-4'),
    ('Ring_L',          'r-finger-4-1', 'r-finger-4-4'),
    ('Pinky_L',          'r-finger-5-1', 'r-finger-5-4'),

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

    ('Thumb-1_L',        ThumbRoll, 'Palm-1_L', F_DEF, L_LHANDFK+L_LHANDIK, NoBB),
    ('Thumb-1_R',        -ThumbRoll, 'Palm-1_R', F_DEF, L_RHANDFK+L_RHANDIK, NoBB),

    # Finger controls
    ('Thumb_L',      ThumbRoll, 'Thumb-1_L', F_WIR, L_LHANDIK, NoBB),
    ('Index_L',      0.0, 'Palm-2_L', F_WIR, L_LHANDIK, NoBB),
    ('Middle_L',      0.0, 'Palm-3_L', F_WIR, L_LHANDIK, NoBB),
    ('Ring_L',      0.0, 'Palm-4_L', F_WIR, L_LHANDIK, NoBB),
    ('Pinky_L',      0.0, 'Palm-5_L', F_WIR, L_LHANDIK, NoBB),
    
    ('Thumb_R',      -ThumbRoll, 'Thumb-1_R', F_WIR, L_RHANDIK, NoBB),
    ('Index_R',      0.0, 'Palm-2_R', F_WIR, L_RHANDIK, NoBB),
    ('Middle_R',      0.0, 'Palm-3_R', F_WIR, L_RHANDIK, NoBB),
    ('Ring_R',      0.0, 'Palm-4_R', F_WIR, L_RHANDIK, NoBB),
    ('Pinky_R',      0.0, 'Palm-5_R', F_WIR, L_RHANDIK, NoBB),

    # Fingers
    ('Thumb-2_L',        ThumbRoll, 'Thumb-1_L', F_DEF, L_LHANDFK, NoBB),
    ('Thumb-3_L',        ThumbRoll, 'Thumb-2_L', F_DEF, L_LHANDFK, NoBB),
    ('Index-1_L',        0.0, 'Palm-2_L', F_DEF, L_LHANDFK, NoBB),
    ('Index-2_L',        0.0, 'Index-1_L', F_DEF, L_LHANDFK, NoBB),
    ('Index-3_L',        0.0, 'Index-2_L', F_DEF, L_LHANDFK, NoBB),
    ('Middle-1_L',        0.0, 'Palm-3_L', F_DEF, L_LHANDFK, NoBB),
    ('Middle-2_L',        0.0, 'Middle-1_L', F_DEF, L_LHANDFK, NoBB),
    ('Middle-3_L',        0.0, 'Middle-2_L', F_DEF, L_LHANDFK, NoBB),
    ('Ring-1_L',        0.0, 'Palm-4_L', F_DEF, L_LHANDFK, NoBB),
    ('Ring-2_L',        0.0, 'Ring-1_L', F_DEF, L_LHANDFK, NoBB),
    ('Ring-3_L',        0.0, 'Ring-2_L', F_DEF, L_LHANDFK, NoBB),
    ('Pinky-1_L',        0.0, 'Palm-5_L', F_DEF, L_LHANDFK, NoBB),
    ('Pinky-2_L',        0.0, 'Pinky-1_L', F_DEF, L_LHANDFK, NoBB),
    ('Pinky-3_L',        0.0, 'Pinky-2_L', F_DEF, L_LHANDFK, NoBB),

    ('Thumb-2_R',        -ThumbRoll, 'Thumb-1_R', F_DEF, L_RHANDFK, NoBB),
    ('Thumb-3_R',        -ThumbRoll, 'Thumb-2_R', F_DEF, L_RHANDFK, NoBB),
    ('Index-1_R',        0.0, 'Palm-2_R', F_DEF, L_RHANDFK, NoBB),
    ('Index-2_R',        0.0, 'Index-1_R', F_DEF, L_RHANDFK, NoBB),
    ('Index-3_R',        0.0, 'Index-2_R', F_DEF, L_RHANDFK, NoBB),
    ('Middle-1_R',        0.0, 'Palm-3_R', F_DEF, L_RHANDFK, NoBB),
    ('Middle-2_R',        0.0, 'Middle-1_R', F_DEF, L_RHANDFK, NoBB),
    ('Middle-3_R',        0.0, 'Middle-2_R', F_DEF, L_RHANDFK, NoBB),
    ('Ring-1_R',        0.0, 'Palm-4_R', F_DEF, L_RHANDFK, NoBB),
    ('Ring-2_R',        0.0, 'Ring-1_R', F_DEF, L_RHANDFK, NoBB),
    ('Ring-3_R',        0.0, 'Ring-2_R', F_DEF, L_RHANDFK, NoBB),
    ('Pinky-1_R',        0.0, 'Palm-5_R', F_DEF, L_RHANDFK, NoBB),
    ('Pinky-2_R',        0.0, 'Pinky-1_R', F_DEF, L_RHANDFK, NoBB),
    ('Pinky-3_R',        0.0, 'Pinky-2_R', F_DEF, L_RHANDFK, NoBB),
]

#
#   defineFingerConstraints():
#

limitRotThumb = ('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-1.37,0.5, 0,0, -60*D,60*D), (1,0,1)]) 
limitRotFingers = ('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-1.37,0.5, 0,0, -30*D,30*D), (1,0,1)]) 

FingerName = ["Dummy", "Thumb", "Index", "Middle", "Ring", "Pinky"]

def defineFingerConstraints():
    fconstraints = {}
    for fnum in range(1,6):
        for suffix in ["_L", "_R"]:
            finger = "%s%s" % (FingerName[fnum], suffix)
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
#   FingerControlPoses(fp, config):
#

customShape = 'MHCircle05'
customShape = None
        
def FingerControlPoses(fp, config):
    for suffix in ['_L', '_R']:
        for fnum in range(1,6):
            fing = '%s%s' % (FingerName[fnum], suffix)
            if fnum == 1:
                lim = limitRotThumb
            else:
                lim = limitRotFingers
            addPoseBone(fp, config, fing, 'MHKnuckle', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [lim])
            
            for lnum in range(1,4):
                if (fnum == 1 and lnum <= 2) or (fnum >= 2 and lnum == 1):
                    rot = (0,1,0)
                    ik = (1,0,1)
                else:
                    rot = (0,1,1)
                    ik = (0,0,1)                
                fing = '%s-%d%s' % (FingerName[fnum], lnum, suffix)
                addPoseBone(fp, config, fing, customShape, None, (1,1,1), rot, (1,1,1), ik, 0, 
                    fconstraints["%d-%d%s" % (fnum, lnum, suffix)])             

            palm = 'Palm-%d%s' % (fnum, suffix)
            addPoseBone(fp, config, palm, None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

        addPoseBone(fp, config, 'Wrist-1%s' % suffix, None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
        addPoseBone(fp, config, 'Wrist-2%s' % suffix, None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
    return  

#
#   getFingerPropDrivers():
#

def getFingerPropDrivers():
    drivers = []
    for fnum in range(1,6):
        for lnum in range(1,4):
            if (fnum != 1) or (lnum != 1):
                finger = '%s-%d' % (FingerName[fnum],lnum)
                drivers.append( (finger, 'Rot', ['FingerControl'], 'x1') )
    return drivers

