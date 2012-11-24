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
"""

from . import the
from the import *

import armature

"""
def addIkHandle(fp, config, bone, customShape, limit):
    if limit:
        cns = [('LimitDist', 0, 1, ['LimitDist', limit])]
    else:
        cns = []
    addPoseBone(fp, config, bone, customShape, None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, cns)

def addSingleIk(fp, config, bone, lockRot, target, limit):
    cns = [('IK', 0, 1, ['IK', target, 1, None, (True, False, True), 1.0])]
    if limit:
        cns.append( ('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limit, (True, True, True)]) )
    addPoseBone(fp, config, bone, None, None, (1,1,1), lockRot, (1,1,1), (1,1,1), 0, cns)

def addDeformYBone(fp, config, bone, ikBone, fkBone, cflags, pflags):
    space = cflags & (C_OW_MASK + C_TG_MASK)
    constraints = [
        ('CopyRot', space, 0, ['RotIKXZ', ikBone, (1,0,1), (0,0,0), False]),
        ('CopyRot', space, 0, ['RotIKY', ikBone, (0,1,0), (0,0,0), False]),
        ('CopyRot', space, 1, ['RotFKXZ', fkBone, (1,0,1), (0,0,0), False]),
        ('CopyRot', space, 1, ['RotFKY', fkBone, (0,1,0), (0,0,0), False])
        ]
    addPoseBone(fp, config, bone, None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), pflags, constraints)
    return

def addDeformLimb(fp, config, bone, ikBone, ikRot, fkBone, fkRot, cflags, pflags, constraints):
    space = cflags & (C_OW_MASK + C_TG_MASK)
    constraints += [
        ('CopyRot', space, 0, ['RotIK', ikBone, ikRot, (0,0,0), False]),
        ('CopyRot', space, 1, ['RotFK', fkBone, fkRot, (0,0,0), False])
        ]
    (fX,fY,fZ) = fkRot
    addPoseBone(fp, config, bone, None, None, (1,1,1), (1-fX,1-fY,1-fZ), (0,0,0), (1,1,1), pflags, constraints)
    return

def addStretchBone(fp, config, bone, target, parent):
    addPoseBone(fp, config, bone, None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', target, 0, 1]),
          ('LimitScale', C_OW_LOCAL, 0, ['LimitScale', (0,0, 0,0, 0,0), (0,1,0)])])
    #addPoseBone(fp, config, target, None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
     #    [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-deg90,deg90, 0,0, -deg90,deg90), (1,1,1)])])
    return
"""

def addCSlider(fp, config, bone, mx):
    mn = "-"+mx
    addPoseBone(fp, config, bone, 'MHCube025', None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
        [('LimitLoc', C_OW_LOCAL+C_LTRA, 1, ['Const', (mn,mx, '0','0', mn,mx), (1,1,1,1,1,1)])])
    
def addYSlider(fp, config, bone, mx):
    mn = "-"+mx
    addPoseBone(fp, config, bone, 'MHCube025', None, (1,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
        [('LimitLoc', C_OW_LOCAL+C_LTRA, 1, ['Const', ('0','0', '0','0', mn,mx), (1,1,1,1,1,1)])])
    
def addXSlider(fp, config, bone, mn, mx, dflt):
    addPoseBone(fp, config, bone, 'MHCube025', None, ((0,1,1), (dflt,0,0)), (1,1,1), (1,1,1), (1,1,1), 0,
        [('LimitLoc', C_OW_LOCAL+C_LTRA, 1, ['Const', (mn,mx, '0','0', mn,mx), (1,1,1,1,1,1)])])

#
#    addPoseBone(fp, config, bone, customShape, boneGroup, locArg, lockRot, lockScale, ik_dof, flags, constraints):
#

def addPoseBone(fp, config, bone, customShape, boneGroup, locArg, lockRot, lockScale, ik_dof, flags, constraints):
    try:
        (lockLoc, location) = locArg
    except:
        lockLoc = locArg
        location = (0,0,0)        
    
    (locX, locY, locZ) = location
    (lockLocX, lockLocY, lockLocZ) = lockLoc
    (lockRotX, lockRotY, lockRotZ) = lockRot
    (lockScaleX, lockScaleY, lockScaleZ) = lockScale

    ikLin = (flags & P_IKLIN != 0)
    ikRot = (flags & P_IKROT != 0)
    lkRot4 = (flags & P_LKROT4 != 0)
    lkRotW = (flags & P_LKROTW != 0)
    hide = (flags & P_HID != 0)

    if not fp:
        the.createdArmature.bones[bone].constraints = armature.constraints.getConstraints(bone, constraints, lockLoc, lockRot)
        return
    
    if the.Mhx25:
        fp.write("\n  Posebone %s %s \n" % (bone, True))
    else:
        # limitX = flags & 1
        # limitY = (flags >> 1) & 1
        # limitZ = (flags >> 2) & 1
        # lockXRot = (flags >> 3) & 1
        # lockYRot = (flags >> 4) & 1
        # lockZRot = (flags >> 5) & 1
        ikFlags = 8*lockRotX + 16*lockRotY + 32*lockRotZ
        fp.write("\tposebone %s %x \n" % (bone, ikFlags))
        if customShape:
            fp.write("\t\tdisplayObject _object['%s'] ;\n" % customShape)
        
    if boneGroup:
        index = boneGroupIndex(boneGroup, config)
        fp.write("    bone_group Refer BoneGroup %s ;\n" % boneGroup)

    (uses, mins, maxs) = armature.constraints.writeConstraints(fp, bone, constraints, lockLoc, lockRot)

    if not the.Mhx25:
        fp.write("\tend posebone\n")
        return
    
    ik_stretch = None
    ik_stiff = None
    ik_lim = None
    try:
        (ik_dof_x, ik_dof_y, ik_dof_z) = ik_dof
    except:
        (ik_dof1, ik_stiff, ik_stretch, ik_lim) = ik_dof
        (ik_dof_x, ik_dof_y, ik_dof_z) = ik_dof1
   
    fp.write(
"    lock_ik_x %d ;\n" % (1-ik_dof_x) +
"    lock_ik_y %d ;\n" % (1-ik_dof_y) +
"    lock_ik_z %d ;\n" % (1-ik_dof_z))


    if ik_lim:
        (xmin,xmax, ymin,ymax, zmin,zmax) = ik_lim
        fp.write(
"    use_ik_limit_x True ;\n" +
"    use_ik_limit_y True ;\n" +
"    use_ik_limit_z True ;\n" +
"    ik_max Array %.4f %.4f %.4f ; \n" % (xmax, ymax, zmax) +
"    ik_min Array %.4f %.4f %.4f ; \n" % (xmin, ymin, zmin))

    if ik_stiff:
        (ik_stiff_x, ik_stiff_y, ik_stiff_z) = ik_stiff
        fp.write("    ik_stiffness  Array %.4f %.4f %.4f ;\n" % (ik_stiff_x, ik_stiff_y, ik_stiff_z))
    else:
        fp.write("    ik_stiffness Array 0.0 0.0 0.0  ; \n")

    if customShape:
        fp.write("    custom_shape Refer Object %s ; \n" % customShape)

    rotMode = rotationMode(flags)
    fp.write("  rotation_mode '%s' ;\n" % rotMode)

    fp.write(
"    use_ik_linear_control %s ; \n" % ikLin +
"    ik_linear_weight 0 ; \n"+
"    use_ik_rotation_control %s ; \n" % ikRot +
"    ik_rotation_weight 0 ; \n" +
"    hide %s ; \n" % hide)
    
    if ik_stretch:
        fp.write("    ik_stretch %.3f ; \n" % ik_stretch)
    else:
        fp.write("    ik_stretch 0 ; \n")

    fp.write(
"    location Array %.3f %.3f %.3f ; \n" % (locX, locY, locZ) +
"    lock_location Array %d %d %d ;\n"  % (lockLocX, lockLocY, lockLocZ)+
"    lock_rotation Array %d %d %d ;\n"  % (lockRotX, lockRotY, lockRotZ) +
"    lock_rotation_w %s ; \n" % lkRotW +
"    lock_rotations_4d %s ; \n" % lkRot4 +
"    lock_scale Array %d %d %d  ; \n" % (lockScaleX, lockScaleY, lockScaleZ)+
"  end Posebone \n")
    return    


def rotationMode(flags):
    modes = ['QUATERNION', 'XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX']
    return modes[(flags&P_ROTMODE) >> 8]
        

def boneGroupIndex(grp, config):
    index = 1
    for (name, the.me) in config.boneGroups:
        if name == grp:
            return index
        index += 1
    raise NameError("Unknown bonegroup %s" % grp)



