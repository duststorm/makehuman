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
Clothes bone definitions 

"""

from . import the
from the import *
from . import posebone
from posebone import addPoseBone

s = 0.8
a = 0.8*s
b = 1-a
c = 0.9*s
d = 1-c

SkirtJoints = [
    ('r-skirt-hip1-front',      'vl', ((a,15746),(b,15750))),
    ('r-skirt-hip1-back',       'vl', ((b,15746),(a,15750))),
    ('r-skirt-hip2-front',      'vl', ((a,15845),(b,15841))),
    ('r-skirt-hip2-back',       'vl', ((b,15845),(a,15841))),
    ('r-skirt-knee-front',      'vl', ((a,15965),(b,15961))),
    ('r-skirt-knee-back',       'vl', ((b,15965),(a,15961))),    
    ('r-skirt-wrist-front',     'vl', ((a,16085),(b,16081))),
    ('r-skirt-wrist-back',      'vl', ((b,16085),(a,16081))),    
    ('r-skirt-upleg-front',     'l', ((0.5,'r-skirt-hip2-front'), (0.5,'r-skirt-knee-front'))),
    ('r-skirt-upleg-back',      'l', ((0.5,'r-skirt-hip2-back'), (0.5,'r-skirt-knee-back'))),
    ('r-skirt-loleg-front',     'l', ((0.5,'r-skirt-knee-front'), (0.5,'r-skirt-wrist-front'))),
    ('r-skirt-loleg-back',      'l', ((0.5,'r-skirt-knee-back'), (0.5,'r-skirt-wrist-back'))),

    ('l-skirt-hip1-front',      'vl', ((a,15352),(b,15356))),
    ('l-skirt-hip1-back',       'vl', ((b,15352),(a,15356))),
    ('l-skirt-hip2-front',      'vl', ((a,15459),(b,15455))),
    ('l-skirt-hip2-back',       'vl', ((b,15459),(a,15455))),
    ('l-skirt-knee-front',      'vl', ((a,15591),(b,15587))),
    ('l-skirt-knee-back',       'vl', ((b,15591),(a,15587))),
    ('l-skirt-wrist-front',     'vl', ((a,15723),(b,15719))),
    ('l-skirt-wrist-back',      'vl', ((b,15723),(a,15719))),
    ('l-skirt-upleg-front',     'l', ((0.5,'l-skirt-hip2-front'), (0.5,'l-skirt-knee-front'))),
    ('l-skirt-upleg-back',      'l', ((0.5,'l-skirt-hip2-back'), (0.5,'l-skirt-knee-back'))),
    ('l-skirt-loleg-front',     'l', ((0.5,'l-skirt-knee-front'), (0.5,'l-skirt-wrist-front'))),
    ('l-skirt-loleg-back',      'l', ((0.5,'l-skirt-knee-back'), (0.5,'l-skirt-wrist-back'))),

    ('r-skirt-top-out',         'v', 15747),
    ('l-skirt-top-out',         'v', 15353),
    ('r-skirt-top-in',          'l', ((0.5,'r-skirt-hip1-front'), (0.5,'r-skirt-hip1-back'))),
    ('l-skirt-top-in',          'l', ((0.5,'l-skirt-hip1-front'), (0.5,'l-skirt-hip1-back'))),
    ('r-skirt-hip1-out',        'l', ((0.5,'r-skirt-top-out'), (0.5,'r-skirt-top-in'))),
    ('l-skirt-hip1-out',        'l', ((0.5,'l-skirt-top-out'), (0.5,'l-skirt-top-in'))),
    
    ('r-skirt-hip2-out',        'vl', ((a,15844),(b,17952))),
    ('l-skirt-hip2-out',        'vl', ((a,15458),(b,16708))),
    ('r-skirt-knee-out',        'vl', ((a,15964),(b,3852))),
    ('l-skirt-knee-out',        'vl', ((a,15590),(b,7157))),
    ('r-skirt-wrist-out',       'vl', ((a,16084),(b,4101))),
    ('l-skirt-wrist-out',       'vl', ((a,15722),(b,6946))),
    ('r-skirt-upleg-out',       'l', ((0.5,'r-skirt-hip2-out'), (0.5,'r-skirt-knee-out'))),
    ('r-skirt-loleg-out',       'l', ((0.5,'r-skirt-knee-out'), (0.5,'r-skirt-wrist-out'))),
    ('l-skirt-upleg-out',       'l', ((0.5,'l-skirt-hip2-out'), (0.5,'l-skirt-knee-out'))),
    ('l-skirt-loleg-out',       'l', ((0.5,'l-skirt-knee-out'), (0.5,'l-skirt-wrist-out'))),
        
    ('skirt-hip1-midfront',     'vl', ((c,15340),(d,15341))),
    ('skirt-hip1-midback',      'vl', ((d,15340),(c,15341))),
    ('skirt-hip2-midfront',     'vl', ((c,15471),(d,15470))),
    ('skirt-hip2-midback',      'vl', ((d,15471),(c,15470))),
    ('skirt-hip3-midfront',     'vl', ((c,15516),(d,15517))),
    ('skirt-hip3-midback',      'vl', ((d,15516),(c,15517))),
    ('skirt-knee-midfront',     'vl', ((c,15603),(d,15602))),
    ('skirt-knee-midback',      'vl', ((d,15603),(c,15602))),
    ('skirt-loleg-midfront',    'vl', ((c,15648),(d,15649))),
    ('skirt-loleg-midback',     'vl', ((d,15648),(c,15649))),
    ('skirt-wrist-midfront',    'vl', ((c,15735),(d,15734))),
    ('skirt-wrist-midback',     'vl', ((d,15735),(c,15734))),
            
]

SkirtHeadsTails = [
    # Skirt
    ('SkirtUp1Front_L',      'r-skirt-hip1-front', 'r-skirt-hip2-front'),
    ('SkirtUp2Front_L',      'r-skirt-hip2-front', 'r-skirt-upleg-front'),
    ('SkirtUp3Front_L',      'r-skirt-upleg-front', 'r-skirt-knee-front'),
    ('SkirtLo1Front_L',      'r-skirt-knee-front', 'r-skirt-loleg-front'),
    ('SkirtLo2Front_L',      'r-skirt-loleg-front', 'r-skirt-wrist-front'),
    
    ('SkirtUp1Front_R',      'l-skirt-hip1-front', 'l-skirt-hip2-front'),
    ('SkirtUp2Front_R',      'l-skirt-hip2-front', 'l-skirt-upleg-front'),
    ('SkirtUp3Front_R',      'l-skirt-upleg-front', 'l-skirt-knee-front'),
    ('SkirtLo1Front_R',      'l-skirt-knee-front', 'l-skirt-loleg-front'),
    ('SkirtLo2Front_R',      'l-skirt-loleg-front', 'l-skirt-wrist-front'),

    ('SkirtUp1Back_L',       'r-skirt-hip1-back', 'r-skirt-hip2-back'),
    ('SkirtUp2Back_L',       'r-skirt-hip2-back', 'r-skirt-upleg-back'),
    ('SkirtUp3Back_L',       'r-skirt-upleg-back', 'r-skirt-knee-back'),
    ('SkirtLo1Back_L',       'r-skirt-knee-back', 'r-skirt-loleg-back'),
    ('SkirtLo2Back_L',       'r-skirt-loleg-back', 'r-skirt-wrist-back'),
    
    ('SkirtUp1Back_R',       'l-skirt-hip1-back', 'l-skirt-hip2-back'),
    ('SkirtUp2Back_R',       'l-skirt-hip2-back', 'l-skirt-upleg-back'),
    ('SkirtUp3Back_R',       'l-skirt-upleg-back', 'l-skirt-knee-back'),
    ('SkirtLo1Back_R',       'l-skirt-knee-back', 'l-skirt-loleg-back'),
    ('SkirtLo2Back_R',       'l-skirt-loleg-back', 'l-skirt-wrist-back'),

    ('SkirtUp1Out_L',        'r-skirt-hip1-out', 'r-skirt-hip2-out'),
    ('SkirtUp2Out_L',        'r-skirt-hip2-out', 'r-skirt-upleg-out'),
    ('SkirtUp3Out_L',        'r-skirt-upleg-out', 'r-skirt-knee-out'),
    ('SkirtLo1Out_L',        'r-skirt-knee-out', 'r-skirt-loleg-out'),
    ('SkirtLo2Out_L',        'r-skirt-loleg-out', 'r-skirt-wrist-out'),
    
    ('SkirtUp1Out_R',        'l-skirt-hip1-out', 'l-skirt-hip2-out'),
    ('SkirtUp2Out_R',        'l-skirt-hip2-out', 'l-skirt-upleg-out'),
    ('SkirtUp3Out_R',        'l-skirt-upleg-out', 'l-skirt-knee-out'),
    ('SkirtLo1Out_R',        'l-skirt-knee-out', 'l-skirt-loleg-out'),
    ('SkirtLo2Out_R',        'l-skirt-loleg-out', 'l-skirt-wrist-out'),

    ('SkirtUp1MidFront',     'skirt-hip1-midfront', 'skirt-hip2-midfront'),
    ('SkirtUp2MidFront',     'skirt-hip2-midfront', 'skirt-hip3-midfront'),
    ('SkirtUp3MidFront',     'skirt-hip3-midfront', 'skirt-knee-midfront'),
    ('SkirtLo1MidFront',     'skirt-knee-midfront', 'skirt-loleg-midfront'),
    ('SkirtLo2MidFront',     'skirt-loleg-midfront', 'skirt-wrist-midfront'),
    
    ('SkirtUp1MidBack',      'skirt-hip1-midback', 'skirt-hip2-midback'),
    ('SkirtUp2MidBack',      'skirt-hip2-midback', 'skirt-hip3-midback'),
    ('SkirtUp3MidBack',      'skirt-hip3-midback', 'skirt-knee-midback'),
    ('SkirtLo1MidBack',      'skirt-knee-midback', 'skirt-loleg-midback'),
    ('SkirtLo2MidBack',      'skirt-loleg-midback', 'skirt-wrist-midback'),
    
    ('SkirtFrontFix',        'r-skirt-hip1-front', 'l-skirt-hip1-front'),
    ('SkirtBackFix',         'r-skirt-hip1-back', 'l-skirt-hip1-back'),
    ('SkirtOutFix',          'r-skirt-hip1-out', 'l-skirt-hip1-out'),
    ('SkirtMidFix',          'skirt-hip1-midfront', 'skirt-hip1-midback'),
]

rollOut = 90*D
rollFront = 180*D
rollBack = 0*D

SkirtArmature = [
    # Skirt
    ('SkirtUp1Front_L',      rollFront, 'UpLeg_L', F_DEF|F_WIR, L_CLO, NoBB),
    ('SkirtUp2Front_L',      rollFront, 'SkirtUp1Front_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtUp3Front_L',      rollFront, 'SkirtUp2Front_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo1Front_L',      rollFront, 'SkirtUp3Front_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo2Front_L',      rollFront, 'SkirtLo1Front_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),

    ('SkirtUp1Front_R',      rollFront, 'UpLeg_R', F_DEF|F_WIR, L_CLO, NoBB),
    ('SkirtUp2Front_R',      rollFront, 'SkirtUp1Front_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtUp3Front_R',      rollFront, 'SkirtUp2Front_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo1Front_R',      rollFront, 'SkirtUp3Front_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo2Front_R',      rollFront, 'SkirtLo1Front_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),

    ('SkirtUp1Back_L',       rollBack, 'UpLeg_L', F_DEF|F_WIR, L_CLO, NoBB),
    ('SkirtUp2Back_L',       rollBack, 'SkirtUp1Back_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtUp3Back_L',       rollBack, 'SkirtUp2Back_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo1Back_L',       rollBack, 'SkirtUp3Back_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo2Back_L',       rollBack, 'SkirtLo1Back_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),

    ('SkirtUp1Back_R',       rollBack, 'UpLeg_R', F_DEF|F_WIR, L_CLO, NoBB),
    ('SkirtUp2Back_R',       rollBack, 'SkirtUp1Back_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtUp3Back_R',       rollBack, 'SkirtUp2Back_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo1Back_R',       rollBack, 'SkirtUp3Back_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo2Back_R',       rollBack, 'SkirtLo1Back_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),

    ('SkirtUp1Out_L',        rollOut, 'UpLeg_L', F_DEF|F_WIR, L_CLO, NoBB),
    ('SkirtUp2Out_L',        rollOut, 'SkirtUp1Out_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtUp3Out_L',        rollOut, 'SkirtUp2Out_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo1Out_L',        rollOut, 'SkirtUp3Out_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo2Out_L',        rollOut, 'SkirtLo1Out_L', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    
    ('SkirtUp1Out_R',        -rollOut, 'UpLeg_R', F_DEF|F_WIR, L_CLO, NoBB),
    ('SkirtUp2Out_R',        -rollOut, 'SkirtUp1Out_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtUp3Out_R',        -rollOut, 'SkirtUp2Out_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo1Out_R',        -rollOut, 'SkirtUp3Out_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo2Out_R',        -rollOut, 'SkirtLo1Out_R', F_DEF|F_WIR|F_CON, L_CLO, NoBB),

    ('SkirtUp1MidFront',     rollFront, 'DfmHips', F_DEF|F_WIR, L_CLO, NoBB),
    ('SkirtUp2MidFront',     rollFront, 'SkirtUp1MidFront', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtUp3MidFront',     rollFront, 'SkirtUp2MidFront', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo1MidFront',     rollFront, 'SkirtUp3MidFront', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo2MidFront',     rollFront, 'SkirtLo1MidFront', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    
    ('SkirtUp1MidBack',      rollBack, 'DfmHips', F_DEF|F_WIR, L_CLO, NoBB),
    ('SkirtUp2MidBack',      rollBack, 'SkirtUp1MidBack', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtUp3MidBack',      rollBack, 'SkirtUp2MidBack', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo1MidBack',      rollBack, 'SkirtUp3MidBack', F_DEF|F_WIR|F_CON, L_CLO, NoBB),
    ('SkirtLo2MidBack',      rollBack, 'SkirtLo1MidBack', F_DEF|F_WIR|F_CON, L_CLO, NoBB),

    ('SkirtFrontFix',        0, 'DfmHips', 0, L_CLO, NoBB),
    ('SkirtBackFix',         0, 'DfmHips', 0, L_CLO, NoBB),
    ('SkirtOutFix',          0, 'DfmHips', 0, L_CLO, NoBB),
    ('SkirtMidFix',          0, 'DfmHips', 0, L_CLO, NoBB),

]

def SkirtControlPoses(fp, config):
    # Skirt
    addPoseBone(fp, config, 'SkirtUp1Front_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0,
        [('CopyLoc', 0, 1, ['SkirtFrontFix', 'SkirtFrontFix', (1,1,1), (0,0,0), 0, False])])

    addPoseBone(fp, config, 'SkirtUp2Front_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SkirtUp3Front_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SkirtLo1Front_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
        #[('CopyLoc', 0, 1, ['SkirtUp3Front_L', 'SkirtUp3Front_L', (1,1,1), (0,0,0), 1, False])])

    addPoseBone(fp, config, 'SkirtLo2Front_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])


    addPoseBone(fp, config, 'SkirtUp1Front_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
        #[('CopyLoc', 0, 1, ['SkirtFrontFix', 'SkirtFrontFix', (1,1,1), (0,0,0), 1, False])])

    addPoseBone(fp, config, 'SkirtUp2Front_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    
    addPoseBone(fp, config, 'SkirtUp3Front_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    
    addPoseBone(fp, config, 'SkirtLo1Front_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
        #[('CopyLoc', 0, 1, ['SkirtUp3Front_R', 'SkirtUp3Front_R', (1,1,1), (0,0,0), 1, False])])
        
    addPoseBone(fp, config, 'SkirtLo2Front_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    

    addPoseBone(fp, config, 'SkirtUp1Back_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
        #[('CopyLoc', 0, 1, ['SkirtBackFix', 'SkirtBackFix', (1,1,1), (0,0,0), 0, False])])

    addPoseBone(fp, config, 'SkirtUp2Back_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SkirtUp3Back_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SkirtLo1Back_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
        #[('CopyLoc', 0, 1, ['SkirtUp3Back_L', 'SkirtUp3Back_L', (1,1,1), (0,0,0), 1, False])])

    addPoseBone(fp, config, 'SkirtLo2Back_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])


    addPoseBone(fp, config, 'SkirtUp1Back_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
        #[('CopyLoc', 0, 1, ['SkirtBackFix', 'SkirtBackFix', (1,1,1), (0,0,0), 1, False])])

    addPoseBone(fp, config, 'SkirtUp2Back_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    
    addPoseBone(fp, config, 'SkirtUp3Back_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    
    addPoseBone(fp, config, 'SkirtLo1Back_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, []) 
        #[('CopyLoc', 0, 1, ['SkirtUp3Back_R', 'SkirtUp3Back_R', (1,1,1), (0,0,0), 1, False])])
        
    addPoseBone(fp, config, 'SkirtLo2Back_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    

    addPoseBone(fp, config, 'SkirtUp1Out_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
        #[('CopyLoc', 0, 1, ['SkirtOutFix', 'SkirtOutFix', (1,1,1), (0,0,0), 0, False])])

    addPoseBone(fp, config, 'SkirtUp2Out_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SkirtUp3Out_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SkirtLo1Out_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
        #[('CopyLoc', 0, 1, ['SkirtUp3Out_L', 'SkirtUp3Out_L', (1,1,1), (0,0,0), 1, False])])

    addPoseBone(fp, config, 'SkirtLo2Out_L', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])


    addPoseBone(fp, config, 'SkirtUp1Out_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
        #[('CopyLoc', 0, 1, ['SkirtOutFix', 'SkirtOutFix', (1,1,1), (0,0,0), 1, False])])

    addPoseBone(fp, config, 'SkirtUp2Out_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    
    addPoseBone(fp, config, 'SkirtUp3Out_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    
    addPoseBone(fp, config, 'SkirtLo1Out_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
        #[('CopyLoc', 0, 1, ['SkirtUp3Out_R', 'SkirtUp3Out_R', (1,1,1), (0,0,0), 1, False])])
        
    addPoseBone(fp, config, 'SkirtLo2Out_R', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    

    addPoseBone(fp, config, 'SkirtUp1MidFront', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SkirtUp2MidFront', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SkirtUp3MidFront', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SkirtLo1MidFront', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SkirtLo2MidFront', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])


    addPoseBone(fp, config, 'SkirtUp1MidBack', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])

    addPoseBone(fp, config, 'SkirtUp2MidBack', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    
    addPoseBone(fp, config, 'SkirtUp3MidBack', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    
    addPoseBone(fp, config, 'SkirtLo1MidBack', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
        
    addPoseBone(fp, config, 'SkirtLo2MidBack', 'MHHook', None, (1,1,1), (0,0,0), (1,0,1), (1,1,1), 0, [])
    

    return



