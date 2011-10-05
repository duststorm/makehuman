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
Functions shared by all rigs 

Limit angles from http://hippydrome.com/

"""

import aljabr
from aljabr import *
import math
import mhxbones
import mhx_main
import read_expression
import sys
import mhx_custom
        
pi = 3.14159
D = pi/180
yunit = [0,1,0]
ysmall = [0,0.5,0]
zunit = [0,0,-1]
ybis = [0,2,0]

unlimited = (-pi,pi, -pi,pi, -pi,pi)
NoBB = (1,1,1)
NoBB = None
bbMarg = 0.05

#
#    Bone layers
#

L_MAIN =    0x0001
L_XPRT =    0x00010000

L_UPSPNFK = 0x0002
L_UPSPNIK = 0x00020000

L_LARMIK =  0x0004
L_LARMFK =  0x0008
L_LLEGIK =  0x0010
L_LLEGFK =  0x0020
L_LHANDIK = 0x0040
L_LHANDFK = 0x0080

L_RARMIK =  0x00040000
L_RARMFK =  0x00080000
L_RLEGIK =  0x00100000
L_RLEGFK =  0x00200000
L_RHANDIK = 0x00400000
L_RHANDFK = 0x00800000

L_PANEL =   0x0100
L_TWEAK =   0x0200
L_TOE =     0x0200
L_HEAD =    0x0400

L_LPALM =   0x0800
L_LEXTRA =  0x1000
L_RPALM =   0x08000000
L_REXTRA =  0x10000000

L_DNSPNFK = 0x2000
L_DNSPNIK = 0x20000000

L_HELP =    0x4000
L_DEF =     0x8000
L_MSCL =    0x40000000
L_DMAIN =   0x80000000

#
#    Flags
#


F_CON = 0x0001
F_DEF = 0x0002
F_RES = 0x0004
#F_RES = 0
F_WIR = 0x0008
F_NOLOC = 0x0020
F_LOCK = 0x0040
F_HID = 0x0080
F_NOCYC = 0x0100

F_NOSCALE = 0x0200
F_NOROT = 0x0400
F_SCALE = 0x0800


P_LKROT4 = 0x0001
P_LKROTW = 0x0002
P_IKLIN = 0x0004
P_IKROT = 0x0008
P_HID = 0x0020

P_ROTMODE = 0x0f00
P_QUAT = 0x0000
P_XYZ = 0x0100
P_XZY = 0x0200
P_YXZ = 0x0300
P_YZX = 0x0400
P_ZXY = 0x0500
P_ZYX = 0x0600

def rotationMode(flags):
    modes = ['QUATERNION', 'XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX']
    return modes[(flags&P_ROTMODE) >> 8]

C_ACT = 0x0004
C_EXP = 0x0008
C_LTRA = 0x0010
C_LOC = 0x0020
C_STRVOL = 0x0040
C_PLANEZ = 0x0080

C_OW_MASK = 0x0300
C_OW_WORLD = 0x0000
C_OW_LOCAL = 0x0100
C_OW_LOCPAR = 0x0200
C_OW_POSE = 0x0300

C_DEFRIG = 0x0400
C_TAIL = 0x0800

C_TG_MASK = 0x3000
C_TG_WORLD = 0x0000
C_TG_LOCAL = 0x1000
C_TG_LOCPAR = 0x2000
C_TG_POSE = 0x3000

C_CHILDOF = C_OW_POSE+C_TG_WORLD
C_LOCAL = C_OW_LOCAL+C_TG_LOCAL

# Fix for ChildOf bug

Master = 'MasterFloor'
rootChildOfConstraints = []

#        ('ChildOf', C_CHILDOF, 1, ['Floor', 'MasterFloor', (1,1,1), (1,1,1), (1,1,1)]),
#        ('ChildOf', C_CHILDOF, 0, ['Hips', 'MasterHips', (1,1,1), (1,1,1), (1,1,1)]),
#        ('ChildOf', C_CHILDOF, 0, ['Neck', 'MasterNeck', (1,1,1), (1,1,1), (1,1,1)])
#]

#Master = None
Origin = [0,0,0]

#
#    newSetupJoints (obj, joints, moveOrigin):
#    setupHeadsTails(headsTails):
#    findLocation(joint):
#
def newSetupJoints (obj, joints, moveOrigin):
    global locations, Origin
    locations = {}
    for (key, typ, data) in joints:
        #print(key)
        if typ == 'j':
            loc = mhxbones.calcJointPos(obj, data)
            locations[key] = loc
            locations[data] = loc
        elif typ == 'v':
            v = int(data)
            locations[key] = obj.verts[v].co
        elif typ == 'x':
            locations[key] = [float(data[0]), float(data[2]), -float(data[1])]
        elif typ == 'vo':
            v = int(data[0])
            loc = obj.verts[v].co
            locations[key] = [loc[0]+float(data[1]), loc[1]+float(data[3]), loc[2]-float(data[2])]
        elif typ == 'vl':
            ((k1, v1), (k2, v2)) = data
            loc1 = obj.verts[int(v1)].co
            loc2 = obj.verts[int(v2)].co
            locations[key] = vadd(vmul(loc1, k1), vmul(loc2, k2))
        elif typ == 'f':
            (raw, head, tail, offs) = data
            rloc = locations[raw]
            hloc = locations[head]
            tloc = locations[tail]
            #print(raw, rloc)
            vec = aljabr.vsub(tloc, hloc)
            vec2 = aljabr.vdot(vec, vec)
            vraw = aljabr.vsub(rloc, hloc)
            x = aljabr.vdot(vec, vraw) / vec2
            rvec = aljabr.vmul(vec, x)
            nloc = aljabr.vadd(hloc, rvec, offs)
            #print(key, nloc)
            locations[key] = nloc
        elif typ == 'b':
            locations[key] = locations[data]
        elif typ == 'p':
            x = locations[data[0]]
            y = locations[data[1]]
            z = locations[data[2]]
            locations[key] = [x[0],y[1],z[2]]
        elif typ == 'X':
            r = locations[data[0]]
            (x,y,z) = data[1]
            r1 = [float(x), float(y), float(z)]
            locations[key] = aljabr.vcross(r, r1)
        elif typ == 'l':
            ((k1, joint1), (k2, joint2)) = data
            locations[key] = vadd(vmul(locations[joint1], k1), vmul(locations[joint2], k2))
        elif typ == 'o':
            (joint, offsSym) = data
            if type(offsSym) == str:
                offs = locations[offsSym]
            else:
                offs = offsSym
            locations[key] = vadd(locations[joint], offs)
        else:
            raise NameError("Unknown %s" % typ)

    if moveOrigin:
        Origin = locations['floor']
        for key in locations.keys():
            locations[key] = aljabr.vsub(locations[key], Origin)
    return

def setupHeadsTails(headsTails):
    global rigHead, rigTail
    rigHead = {}
    rigTail = {}
    for (bone, head, tail) in headsTails:
        rigHead[bone] = findLocation(head)
        rigTail[bone] = findLocation(tail)
    return 

def findLocation(joint):
    try:
        (bone, offs) = joint
    except:
        offs = 0
    if offs:
        return vadd(locations[bone], offs)
    else:
        return locations[joint]

#
#    writeArmature(fp, armature, mhx25):
#    boolString(val):
#    addBone25(bone, roll, parent, flags, layers, bbone, fp):
#    addBone24(bone, roll, parent, flags, layers, bbone, fp):
#

def writeArmature(fp, armature, mhx25):
    global Mhx25
    Mhx25 = mhx25
    if Mhx25:
        for (bone, roll, parent, flags, layers, bbone) in armature:
            addBone25(bone, True, roll, parent, flags, layers, bbone, fp)
    else:
        for (bone, roll, parent, flags, layers, bbone) in armature:
            addBone24(bone, True, roll, parent, flags, layers, bbone, fp)
    return

def boolString(val):
    if val:
        return "True"
    else:
        return "False"

def addBone25(bone, cond, roll, parent, flags, layers, bbone, fp):
    global rigHead, rigTail

    conn = boolString(flags & F_CON)
    deform = boolString(flags & F_DEF)
    restr = boolString(flags & F_RES)
    wire = boolString(flags & F_WIR)
    lloc = boolString(flags & F_NOLOC == 0)
    lock = boolString(flags & F_LOCK)
    cyc = boolString(flags & F_NOCYC == 0)

    fp.write("\n  Bone %s %s\n" % (bone, cond))
    (x, y, z) = rigHead[bone]
    fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,-z,y))
    (x, y, z) = rigTail[bone]
    fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,-z,y))
    if parent:
        fp.write("    parent Refer Bone %s ; \n" % (parent))
    fp.write(
"    roll %.6g ; \n" % (roll)+
"    use_connect %s ; \n" % (conn) +
"    use_deform %s ; \n" % (deform) +
"    show_wire %s ; \n" % (wire))

    if 1 and (flags & F_HID):
        fp.write("    hide True ; \n")

    if bbone:
        (bin, bout, bseg) = bbone
        fp.write(
"    bbone_in %d ; \n" % (bin) +
"    bbone_out %d ; \n" % (bout) +
"    bbone_segments %d ; \n" % (bseg))

    if flags & F_NOROT:
        fp.write("    use_inherit_rotation False ; \n")
    if flags & F_SCALE:
        fp.write("    use_inherit_scale True ; \n")
    else:
        fp.write("    use_inherit_scale False ; \n")
    fp.write("    layers Array ")

    bit = 1
    for n in range(32):
        if layers & bit:
            fp.write("1 ")
        else:
            fp.write("0 ")
        bit = bit << 1

#"    use_cyclic_offset %s ; \n" % cyc +
    fp.write(" ; \n" +
"    use_local_location %s ; \n" % lloc +
"    lock %s ; \n" % lock +
"    use_envelope_multiply False ; \n"+
"    hide_select %s ; \n" % (restr) +
"  end Bone \n")

def addBone24(bone, cond, roll, parent, flags, layers, bbone, fp):
    global rigHead, rigTail

    flags24 = 0
    if flags & F_CON:
        flags24 += 0x001
    if flags & F_DEF == 0:
        flags24 += 0x004
    if flags & F_NOSCALE:
        flags24 += 0x0e0

    fp.write("\n\tbone %s %s %x %x\n" % (bone, parent, flags24, layers))
    (x, y, z) = rigHead[bone]
    fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,y,z))
    (x, y, z) = rigTail[bone]
    fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,y,z))
    fp.write("    roll %.6g %.6g ; \n" % (roll, roll))
    fp.write("\tend bone\n")
    return

#
#    writeBoneGroups(fp):
#

def boneGroupIndex(grp):
    index = 1
    for (name, theme) in BoneGroups:
        if name == grp:
            return index
        index += 1
    raise NameError("Unknown bonegroup %s" % grp)

def writeBoneGroups(fp):
    for (name, theme) in BoneGroups:
        fp.write(
"    BoneGroup %s\n" % name +
"      name '%s' ;\n" % name +
"      color_set '%s' ;\n" % theme +
"    end BoneGroup\n")
    return


#
#    addIkHandle(fp, bone, customShape, limit):
#    addSingleIk(fp, bone, lockRot, target, limit):
#    addDeformLimb(fp, bone, ikBone, ikRot, fkBone, fkRot, cflags, pflags, constraints):
#    addDeformYBone(fp, bone, ikBone, fkBone, cflags, pflags):
#    addCSlider(fp, bone, mx):
#    addYSlider(fp, bone, mx):
#    addXSlider(fp, bone, mn, mx):
#

def addIkHandle(fp, bone, customShape, limit):
    if limit:
        cns = [('LimitDist', 0, 1, ['LimitDist', limit])]
    else:
        cns = []
    addPoseBone(fp, bone, customShape, None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, cns)

def addSingleIk(fp, bone, lockRot, target, limit):
    cns = [('IK', 0, 1, ['IK', target, 1, None, (True, False, True), 1.0])]
    if limit:
        cns.append( ('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limit, (True, True, True)]) )
    addPoseBone(fp, bone, None, None, (1,1,1), lockRot, (1,1,1), (1,1,1), 0, cns)

def addDeformYBone(fp, bone, ikBone, fkBone, cflags, pflags):
    space = cflags & (C_OW_MASK + C_TG_MASK)
    constraints = [
        ('CopyRot', space, 0, ['RotIKXZ', ikBone, (1,0,1), (0,0,0), False]),
        ('CopyRot', space, 0, ['RotIKY', ikBone, (0,1,0), (0,0,0), False]),
        ('CopyRot', space, 1, ['RotFKXZ', fkBone, (1,0,1), (0,0,0), False]),
        ('CopyRot', space, 1, ['RotFKY', fkBone, (0,1,0), (0,0,0), False])
        ]
    addPoseBone(fp, bone, None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), pflags, constraints)
    return

def addDeformLimb(fp, bone, ikBone, ikRot, fkBone, fkRot, cflags, pflags, constraints):
    space = cflags & (C_OW_MASK + C_TG_MASK)
    constraints += [
        ('CopyRot', space, 0, ['RotIK', ikBone, ikRot, (0,0,0), False]),
        ('CopyRot', space, 1, ['RotFK', fkBone, fkRot, (0,0,0), False])
        ]
    (fX,fY,fZ) = fkRot
    addPoseBone(fp, bone, None, None, (1,1,1), (1-fX,1-fY,1-fZ), (0,0,0), (1,1,1), pflags, constraints)
    return

def addStretchBone(fp, bone, target, parent):
    addPoseBone(fp, bone, None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', target, 0, 1]),
          ('LimitScale', C_OW_LOCAL, 0, ['LimitScale', (0,0, 0,0, 0,0), (0,1,0)])])
    #addPoseBone(fp, target, None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
     #    [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-deg90,deg90, 0,0, -deg90,deg90), (1,1,1)])])
    return

def addCSlider(fp, bone, mx):
    mn = "-"+mx
    addPoseBone(fp, bone, 'MHCube025', None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
        [('LimitLoc', C_OW_LOCAL+C_LTRA, 1, ['Const', (mn,mx, '0','0', mn,mx), (1,1,1,1,1,1)])])
    
def addYSlider(fp, bone, mx):
    mn = "-"+mx
    addPoseBone(fp, bone, 'MHCube025', None, (1,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
        [('LimitLoc', C_OW_LOCAL+C_LTRA, 1, ['Const', ('0','0', '0','0', mn,mx), (1,1,1,1,1,1)])])
    
def addXSlider(fp, bone, mn, mx, dflt):
    addPoseBone(fp, bone, 'MHCube025', None, ((0,1,1), (dflt,0,0)), (1,1,1), (1,1,1), (1,1,1), 0,
        [('LimitLoc', C_OW_LOCAL+C_LTRA, 1, ['Const', (mn,mx, '0','0', mn,mx), (1,1,1,1,1,1)])])

#
#
#

U_LOC = 1
U_ROT = 2
U_SCALE = 4

def copyDeformPartial(fp, dbone, cbone, channels, flags, copy, customShape, constraints):
    fp.write("\n  Posebone %s %s \n" % (dbone, True))
    rotMode = rotationMode(flags)
    fp.write(
"  rotation_mode '%s' ;\n" % rotMode +
"    lock_location Array 1 1 1 ;\n" +
"    lock_rotation Array 1 1 1 ;\n" +
"    lock_rotation_w True ;\n" + 
"    lock_rotations_4d True ;\n" +
"    lock_scale Array 1 1 1  ; \n")
    if customShape:
        fp.write("    custom_shape Refer Object %s ; \n" % customShape)
    if copy & U_LOC:
        addCopyLocConstraint(fp, 0, 1, ['Loc', cbone, (1,1,1), (0,0,0), 0, False])
    if copy & U_ROT:
        addCopyRotConstraint(fp, 0, 1, ['Rot', cbone, channels, (0,0,0), False])
    if copy & U_SCALE:
        addCopyScaleConstraint(fp, 0, 1, ['Scale', cbone, (1,1,1), False])
    addConstraints(fp, dbone, constraints, (1,1,1), (1,1,1))
    fp.write("  end Posebone\n")
    return

def copyDeform(fp, dbone, cbone, flags, copy, customShape, constraints):
    copyDeformPartial(fp, dbone, cbone, (1,1,1), flags, copy, customShape, constraints)

#
#    addPoseBone(fp, bone, customShape, boneGroup, locArg, lockRot, lockScale, ik_dof, flags, constraints):
#

def addPoseBone(fp, bone, customShape, boneGroup, locArg, lockRot, lockScale, ik_dof, flags, constraints):
    global BoneGroups, Mhx25

    try:
        (lockLoc, location) = locArg
    except:
        lockLoc = locArg
        location = (0,0,0)        
    
    (locX, locY, locZ) = location
    (lockLocX, lockLocY, lockLocZ) = lockLoc
    (lockRotX, lockRotY, lockRotZ) = lockRot
    (lockScaleX, lockScaleY, lockScaleZ) = lockScale

    ikLin = boolString(flags & P_IKLIN)
    ikRot = boolString(flags & P_IKROT)
    lkRot4 = boolString(flags & P_LKROT4)
    lkRotW = boolString(flags & P_LKROTW)
    hide = boolString(flags & P_HID)

    if Mhx25:
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
        index = boneGroupIndex(boneGroup)
        fp.write("    bone_group Refer BoneGroup %s ;\n" % boneGroup)

    addConstraints(fp, bone, constraints, lockLoc, lockRot)

    if not Mhx25:
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

#
#    addConstraints(fp, bone, constraints, lockLoc, lockRot)
#

def addConstraints(fp, bone, constraints, lockLoc, lockRot):
    uses = (0,0,0)
    mins = (-pi, -pi, -pi)
    maxs = (pi, pi, pi)

    for (label, cflags, inf, data) in constraints:
        if type(label) == str:
            typ = label
        else:
            raise NameError("Switch in", bone)

        if typ == 'IK':
            addIkConstraint(fp, cflags, inf, data, lockLoc, lockRot)
        elif typ == 'Action':
            addActionConstraint(fp, cflags, inf, data)
        elif typ == 'CopyLoc':
            addCopyLocConstraint(fp, cflags, inf, data)
        elif typ == 'CopyRot':
            addCopyRotConstraint(fp, cflags, inf, data)
        elif typ == 'CopyScale':
            addCopyScaleConstraint(fp, cflags, inf, data)
        elif typ == 'CopyTrans':
            addCopyTransConstraint(fp, cflags, inf, data)
        elif typ == 'LimitRot':
            addLimitRotConstraint(fp, cflags, inf, data)
            (xmin, xmax, ymin, ymax, zmin, zmax) = data[1]
            mins = (xmin, ymin, zmin)
            maxs = (xmax, ymax, zmax)
            #uses = data[2]            
        elif typ == 'LimitLoc':
            addLimitLocConstraint(fp, cflags, inf, data)
        elif typ == 'LimitScale':
            addLimitScaleConstraint(fp, cflags, inf, data)
        elif typ == 'Transform':
            addTransformConstraint(fp, cflags, inf, data)
        elif typ == 'LockedTrack':
            addLockedTrackConstraint(fp, cflags, inf, data)
        elif typ == 'DampedTrack':
            addDampedTrackConstraint(fp, cflags, inf, data)
        elif typ == 'StretchTo':
            addStretchToConstraint(fp, cflags, inf, data)
        elif typ == 'TrackTo':
            addTrackToConstraint(fp, cflags, inf, data)
        elif typ == 'LimitDist':
            addLimitDistConstraint(fp, cflags, inf, data)
        elif typ == 'ChildOf':
            addChildOfConstraint(fp, cflags, inf, data)
        elif typ == 'SplineIK':
            addSplineIkConstraint(fp, cflags, inf, data)
        elif typ == 'Floor':
            addFloorConstraint(fp, cflags, inf, data)
        else:
            print(label)
            print(typ)
            raise NameError("Unknown constraint type %s" % typ)
    return (uses, mins, maxs)

#
#    addIkConstraint(fp, flags, inf, data, lockLoc, lockRot)
#
def addIkConstraint(fp, flags, inf, data, lockLoc, lockRot):
    global Mhx25
    name = data[0]
    subtar = data[1]
    chainlen = data[2]
    pole = data[3]
    (useLoc, useRot, useStretch) = data[4]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)
    (lockLocX, lockLocY, lockLocZ) = lockLoc
    (lockRotX, lockRotY, lockRotZ) = lockRot

    if Mhx25:
        fp.write(
"    Constraint %s IK True\n" % name)

        if subtar:
            fp.write(
"      target Refer Object %s ;\n" % (mhx_main.theHuman) +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp +
"      use_tail True ;\n" +
"      use_target True ;\n")
        else:
            fp.write(
"      use_tail False ;\n" +
"      use_target True ;\n")

        fp.write(
"      pos_lock Array 1 1 1  ;\n" +
"      rot_lock Array 1 1 1  ;\n" +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      reference_axis 'BONE' ;\n" +
"      chain_count %d ;\n" % chainlen +
"      ik_type 'COPY_POSE' ;\n" +
"      influence %s ;\n" % inf +
"      iterations 500 ;\n" +
"      limit_mode 'LIMITDIST_INSIDE' ;\n" +
"      orient_weight 1 ;\n" +
"      owner_space '%s' ;\n" % ownsp)

        if pole:
            (angle, ptar) = pole
            fp.write(
"      pole_angle %.6g ;\n" % angle +
"      pole_subtarget '%s' ;\n" % ptar +
"      pole_target Refer Object %s ;\n" % (mhx_main.theHuman))

        fp.write(
"      is_proxy_local False ;\n" +
"      use_location %s ;\n" % useLoc +
"      use_rotation %s ;\n" % useRot +
"      use_stretch %s ;\n" % useStretch +
"      weight 1 ;\n" +
"    end Constraint\n")

    else:
        fp.write("\t\tconstraint IKSOLVER %s 1.0 \n" % name)
        fp.write(
"\t\t\tCHAINLEN    int %d ; \n" % chainlen +
"\t\t\tTARGET    obj Human ; \n" +
"\t\t\tBONE    str %s ; \n" % subtar +
"\t\tend constraint\n")

    return

#
#    addActionConstraint(fp, flags, inf, data):
#
def addActionConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    action = data[1]
    subtar = data[2]
    channel = data[3]
    (sframe, eframe) = data[4]
    (amin, amax) = data[5]
    inf = data[6]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    fp.write(
"    Constraint %s ACTION True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman)+
"      action Refer Action %s ; \n" % action+
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      frame_start %s ; \n" % sframe +
"      frame_end %d ; \n" % eframe+
"      influence %s ; \n" % inf)

    if channel[0:3] == 'LOC':
        fp.write(
"      maximum %.4f*theScale ; \n" % amax +
"      minimum %.4f*theScale ; \n" % amin)
    else:
        fp.write(
"      maximum %.4f ; \n" % amax +
"      minimum %.4f ; \n" % amin)
    
    fp.write(
"      owner_space '%s' ; \n" % ownsp +
"      is_proxy_local False ; \n"+
"      subtarget '%s' ; \n" % subtar +
"      target_space '%s' ; \n" % targsp +
"      transform_channel '%s' ;\n" % channel +
"    end Constraint \n")
    return

#
#    addCopyRotConstraint(fp, flags, inf, data):
#
def addCopyRotConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    subtar = data[1]
    (useX, useY, useZ) = data[2]
    (invertX, invertY, invertZ) = data[3]
    useOffs = data[4]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    if Mhx25:
        fp.write(
"    Constraint %s COPY_ROTATION True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman)+
"      invert Array %d %d %d ; \n" % (invertX, invertY, invertZ)+
"      use Array %d %d %d  ; \n" % (useX, useY, useZ)+
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ; \n" % inf +
"      owner_space '%s' ; \n" % ownsp+
"      is_proxy_local False ; \n"+
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ; \n" % targsp+
"      use_offset %s ; \n" % useOffs +
"    end Constraint \n")

    else:
        copy = useX + 2*useY + 4*useZ
        fp.write(
"\t\tconstraint COPYROT %s 1.0 \n" % name +
"\t\t\tTARGET    obj Human ;\n" +
"\t\t\tBONE    str %s ; \n" % subtar +
"\t\t\tCOPY    hex %x ;\n" %  copy +
"\t\tend constraint\n")
    return

#
#    addCopyLocConstraint(fp, flags, inf, data):
#
def addCopyLocConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    subtar = data[1]
    (useX, useY, useZ) = data[2]
    (invertX, invertY, invertZ) = data[3]
    head_tail = data[4]
    useOffs = data[5]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    if Mhx25:
        fp.write(
"    Constraint %s COPY_LOCATION True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman)+
"      invert Array %d %d %d ; \n" % (invertX, invertY, invertZ)+
"      use Array %d %d %d  ; \n" % (useX, useY, useZ)+
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ; \n" % inf +
"      owner_space '%s' ; \n" % ownsp +
"      is_proxy_local False ; \n"+
"      head_tail %.3f ;\n" % head_tail +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ; \n" % targsp+
"      use_offset %s ; \n" % useOffs +
"    end Constraint \n")

    else:
        fp.write(
"\t\tconstraint COPYLOC %s 1.0 \n" % name +
"\t\t\tTARGET    obj Human ;\n" +
"\t\t\tBONE    str %s ; \n" % subtar +
"\t\tend constraint\n")
    return

#
#    addCopyScaleConstraint(fp, flags, inf, data):
#
def addCopyScaleConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    subtar = data[1]
    (useX, useY, useZ) = data[2]
    useOffs = data[3]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    fp.write(
"    Constraint %s COPY_SCALE True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman) +
"      use Array %d %d %d  ; \n" % (useX, useY, useZ)+
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp +
"      use_offset %s ;\n" % useOffs +
"    end Constraint\n")
    return

#
#    addCopyTransConstraint(fp, flags, inf, data):
#
def addCopyTransConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    subtar = data[1]
    head_tail = data[2]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)
    
    fp.write(
"    Constraint %s COPY_TRANSFORMS True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      head_tail %.3f ;\n" % head_tail +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp +
"    end Constraint\n")
    return

#
#    addLimitRotConstraint(fp, flags, inf, data):
#
def addLimitRotConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    (xmin, xmax, ymin, ymax, zmin, zmax) = data[1]
    (usex, usey, usez) = data[2]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)
    ltra = boolString(flags & C_LTRA)
    
    if Mhx25:
        fp.write(    
"    Constraint %s LIMIT_ROTATION True\n" % name +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ; \n" % inf +
"      use_transform_limit %s ; \n" % ltra+
"      max_x %.6g ;\n" % xmax +
"      max_y %.6g ;\n" % ymax +
"      max_z %.6g ;\n" % zmax +
"      min_x %.6g ;\n" % xmin +
"      min_y %.6g ;\n" % ymin +
"      min_z %.6g ;\n" % zmin +
"      owner_space '%s' ; \n" % ownsp+
"      is_proxy_local False ; \n"+
"      target_space '%s' ; \n" % targsp+
"      use_limit_x %s ; \n" % usex +
"      use_limit_y %s ; \n" % usey +
"      use_limit_z %s ; \n" % usez +
"   end Constraint \n")

    else:
        limit = usex + 2*usey + 4*usez
        fp.write(
"\t\tconstraint LIMITROT Const 1.0 \n" +
"\t\t\tLIMIT    hex %x ;\n" % limit +
"\t\t\tOWNERSPACE       hex 1 ;\n" +
"\t\t\tXMIN       float %g ; \n" % xmin +
"\t\t\tXMAX       float %g ; \n" % xmax +
"\t\t\tYMIN       float %g ; \n" % ymin +
"\t\t\tYMAX       float %g ; \n" % ymax +
"\t\t\tZMIN       float %g ; \n" % zmin +
"\t\t\tZMAX       float %g ; \n" % zmax +
"\t\tend constraint\n")
    return

#
#    addLimitLocConstraint(fp, flags, inf, data):
#
def addLimitLocConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    (xmin, xmax, ymin, ymax, zmin, zmax) = data[1]
    (useminx, usemaxx, useminy, usemaxy, useminz, usemaxz) = data[2]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)
    
    if Mhx25:
        fp.write(
"    Constraint %s LIMIT_LOCATION True\n" % name +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      use_transform_limit True ;\n" +
"      max_x %s*theScale ;\n" % xmax +
"      max_y %s*theScale ;\n" % ymax +
"      max_z %s*theScale ;\n" % zmax +
"      min_x %s*theScale ;\n" % xmin +
"      min_y %s*theScale ;\n" % ymin +
"      min_z %s*theScale ;\n" % zmin +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      target_space '%s' ;\n" % targsp +
"      use_max_x %s ;\n" % usemaxx +
"      use_max_y %s ;\n" % usemaxy +
"      use_max_z %s ;\n" % usemaxz +
"      use_min_x %s ;\n" % useminx +
"      use_min_y %s ;\n" % useminy +
"      use_min_z %s ;\n" % useminz +
"    end Constraint\n")

    else:
        limit = useminx + 2*useminy + 4*useminz + 8*usemaxx + 16*usemaxy + 32*usemaxz
        fp.write("\t\tconstraint LIMITLOC Const 1.0 \n")
        fp.write(
"\t\t\tLIMIT    hex %x ;\n" % limit +
"\t\t\tOWNERSPACE       hex 1 ;\n" +
"\t\t\tXMIN       float %g ; \n" % xmin +
"\t\t\tXMAX       float %g ; \n" % xmax +
"\t\t\tYMIN       float %g ; \n" % ymin +
"\t\t\tYMAX       float %g ; \n" % ymax +
"\t\t\tZMIN       float %g ; \n" % zmin +
"\t\t\tZMAX       float %g ; \n" % zmax +
"\t\tend constraint\n")

    return

#
#    addLimitScaleConstraint(fp, flags, inf, data):
#
def addLimitScaleConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    (xmin, xmax, ymin, ymax, zmin, zmax) = data[1]
    (usex, usey, usez) = data[2]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)
    
    if Mhx25:
        fp.write(
"    Constraint %s LIMIT_SCALE True\n" % name +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      use_transform_limit True ;\n" +
"      max_x %.6g ;\n" % xmax +
"      max_y %.6g ;\n" % ymax +
"      max_z %.6g ;\n" % zmax +
"      min_x %.6g ;\n" % xmin +
"      min_y %.6g ;\n" % ymin +
"      min_z %.6g ;\n" % zmin +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      target_space '%s' ;\n" % targsp +
"      use_max_x %s ;\n" % usex +
"      use_max_y %s ;\n" % usey +
"      use_max_z %s ;\n" % usez +
"      use_min_x %s ;\n" % usex +
"      use_min_y %s ;\n" % usey +
"      use_min_z %s ;\n" % usez +
"    end Constraint\n")
    return

#
#    addTransformConstraint(fp, flags, inf, data):
#
def addTransformConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    subtar = data[1]
    map_from = data[2]
    from_min = data[3]
    from_max = data[4]
    map_to_from = data[5]
    map_to = data[6]
    to_min = data[7]
    to_max = data[8]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    fp.write(
"    Constraint %s TRANSFORM True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      use_motion_extrapolate 0 ;\n" +
"      owner_space '%s' ;\n" % ownsp+
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"      map_from '%s' ;\n" % map_from + 
"      from_min_x %s ;\n" % from_min[0] + 
"      from_min_y %s ;\n" % from_min[1] + 
"      from_min_z %s ;\n" % from_min[2] + 
"      from_max_x %s ;\n" % from_max[0] + 
"      from_max_y %s ;\n" % from_max[1] + 
"      from_max_z %s ;\n" % from_max[2] + 
"      map_to '%s' ;\n" % map_to + 
"      map_to_x_from '%s' ;\n" % map_to_from[0] +
"      map_to_y_from '%s' ;\n" % map_to_from[1] +
"      map_to_z_from '%s' ;\n" % map_to_from[2] +
"      to_min_x %s ;\n" % to_min[0] + 
"      to_min_y %s ;\n" % to_min[1] + 
"      to_min_z %s ;\n" % to_min[2] + 
"      to_max_x %s ;\n" % to_max[0] + 
"      to_max_y %s ;\n" % to_max[1] + 
"      to_max_z %s ;\n" % to_max[2] + 
"    end Constraint\n")
    return

#
#    addDampedTrackConstraint(fp, flags, inf, data):
#
def addDampedTrackConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    subtar = data[1]
    track = data[2]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    fp.write(
"    Constraint %s DAMPED_TRACK True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      owner_space '%s' ;\n" % ownsp+
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"      track_axis '%s' ;\n" % track + 
"    end Constraint\n")
    return


#
#    addLockedTrackConstraint(fp, flags, inf, data):
#
def addLockedTrackConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    subtar = data[1]
    trackAxis = data[2]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    fp.write(
"    Constraint %s LOCKED_TRACK True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      owner_space '%s' ;\n" % ownsp+
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"      track_axis '%s' ;\n" % trackAxis + 
"    end Constraint\n")
    return

#
#    addStretchToConstraint(fp, flags, inf, data):
#
def addStretchToConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    subtar = data[1]
    head_tail = data[2]
    bulge = data[3]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)
    if flags & C_STRVOL:
        volume = 'VOLUME_XZX'
    else:
        volume = 'NO_VOLUME'
    if flags & C_PLANEZ:
        axis = 'PLANE_Z'
    else:
        axis = 'PLANE_X'

    if Mhx25:
        fp.write(
"    Constraint %s STRETCH_TO True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      bulge %.2f ;\n" % bulge +
"      head_tail %s ;\n" % head_tail +
"      influence %s ;\n" % inf +
"      keep_axis '%s' ;\n" % axis +
"      owner_space '%s' ;\n" % ownsp+
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"      volume '%s' ;\n" % volume +
"    end Constraint\n")

    else:
        fp.write(
"\t\tconstraint STRETCHTO %s 1.0 \n" % name +
"\t\t\tTARGET    obj Human ;\n" +
"\t\t\tBONE    str %s ;\n" % subtar +
"\t\t\tPLANE    hex 2 ;\n" +
"\t\tend constraint\n")
    return

#
#    addTrackToConstraint(fp, flags, inf, data):
#
def addTrackToConstraint(fp, flags, inf, data):
    name = data[0]
    subtar = data[1]
    head_tail = data[2]
    track_axis = data[3]
    up_axis = data[4]
    use_target_z = data[5]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    fp.write(
"    Constraint %s TRACK_TO True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      head_tail %s ;\n" % head_tail +
"      influence %s ;\n" % inf +
"      track_axis '%s' ;\n" % track_axis +
"      up_axis '%s' ;\n" % up_axis +
"      owner_space '%s' ;\n" % ownsp+
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"      use_target_z %s ;\n" % use_target_z +
"    end Constraint\n")
    return

#
#    addLimitDistConstraint(fp, flags, inf, data):
#
def addLimitDistConstraint(fp, flags, inf, data):
    global Mhx25
    name = data[0]
    subtar = data[1]
    typ = data[2]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    if Mhx25:
        fp.write(
"    Constraint %s LIMIT_DISTANCE True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      limit_mode '%s' ;\n" % typ +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"    end Constraint\n")

    else:
        fp.write(
"\t\tconstraint LIMITDIST %s 1.0 \n" % name +
"\t\t\tTARGET    obj Human ;\n" +
"\t\t\tBONE    str %s ;\n" % subtar +
"\t\tend constraint\n")
    return

#
#    addChildOfConstraint(fp, flags, inf, data):
#
def addChildOfConstraint(fp, flags, inf, data):
    global Mhx25
    # return
    name = data[0]
    subtar = data[1]
    (locx, locy, locz) = data[2]
    (rotx, roty, rotz) = data[3]
    (scalex, scaley, scalez) = data[4]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    #ownsp = 'WORLD'
    #targsp = 'WORLD'

    if Mhx25:
        fp.write(
"    Constraint %s CHILD_OF True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp +
"      use_location_x %s ;\n" % locx +
"      use_location_y %s ;\n" % locy +
"      use_location_z %s ;\n" % locz +
"      use_rotation_x %s ;\n" % rotx +
"      use_rotation_y %s ;\n" % roty +
"      use_rotation_z %s ;\n" % rotz +
"      use_scale_x %s ;\n" % scalex +
"      use_scale_y %s ;\n" % scaley +
"      use_scale_z %s ;\n" % scalez +
"    end Constraint\n")
#"    bpyops constraint.childof_set_inverse(constraint='%s',owner='BONE') ;\n" % name)
    return

#
#    addSplineIkConstraint(fp, flags, inf, data):
#
#"      joint_bindings Array 1.0 0.741504311562 0.483008384705 0.253476023674 -5.96046447754e-08  ;\n" +

def addSplineIkConstraint(fp, flags, inf, data):
    global Mhx25, rigHead, rigTail
    # return
    name = data[0]
    target = data[1]
    count = data[2]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    fp.write(
"    Constraint %s SPLINE_IK True\n" % name +
"      target Refer Object %s ;\n" % target +
"      active %s ;\n" % active +
"      chain_count %d ;\n" % count +
"      influence %s ;\n" % inf +
"      owner_space '%s' ;\n" % ownsp +
"      show_expanded %s ;\n" % expanded +
"      target_space '%s' ;\n" % targsp +
"      use_chain_offset False ;\n" +
"      use_curve_radius True ;\n" +
"      use_even_divisions False ;\n" +
"      use_y_stretch True ;\n" +
"      xz_scale_mode 'NONE' ;\n" +
"    end Constraint\n")
    return

#
#    addFloorConstraint(fp, flags, inf, data):
#

def addFloorConstraint(fp, flags, inf, data):
    name = data[0]
    subtar = data[1]
    floor_location = data[2]
    offset = data[3]
    use_rotation = data[4]
    use_sticky = data[5]
    (ownsp, targsp, active, expanded) = constraintFlags(flags)

    fp.write(
"    Constraint %s FLOOR True\n" % name +
"      target Refer Object %s ;\n" % (mhx_main.theHuman) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      floor_location '%s' ;\n" % floor_location +
"      offset %.4f ;\n" % offset +
"      owner_space '%s' ;\n" % ownsp+
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"      use_rotation %s ;\n" % use_rotation +
"      use_sticky %s ;\n" % use_sticky +
"    end Constraint\n")
    return


#
#    constraintFlags(flags):
#
def constraintFlags(flags):
    ow = flags & C_OW_MASK
    if ow == 0:
        ownsp = 'WORLD'
    elif ow == C_OW_LOCAL:
        ownsp = 'LOCAL'
    elif ow == C_OW_LOCPAR:
        ownsp = 'LOCAL_WITH_PARENT'
    elif ow == C_OW_POSE:
        ownsp = 'POSE'

    tg = flags & C_TG_MASK
    if tg == 0:
        targsp = 'WORLD'
    elif tg == C_TG_LOCAL:
        targsp = 'LOCAL'
    elif tg == C_TG_LOCPAR:
        targsp = 'LOCAL_WITH_PARENT'
    elif tg == C_TG_POSE:
        targsp = 'POSE'

    active = boolString(flags & C_ACT == 0)
    expanded = boolString(flags & C_EXP)
    return (ownsp, targsp, active, expanded)


#
#    writeAction(fp, cond, name, action, lr, ikfk):
#    writeFCurves(fp, name, (x01, y01, z01, w01), (x21, y21, z21, w21)):
#

def writeAction(fp, cond, name, action, lr, ikfk):
    fp.write("Action %s %s\n" % (name,cond))
    if ikfk:
        iklist = ["IK", "FK"]
    else:
        iklist = [""]
    if lr:
        for (bone, quats) in action:
            rquats = []
            for (t,x,y,z,w) in rquats:
                rquats.append((t,x,y,-z,-w))
            for ik in iklist:
                writeFCurves(fp, "%s%s_L" % (bone, ik), quats)
                writeFCurves(fp, "%s%s_R" % (bone, ik), rquats)
    else:
        for (bone, quats) in action:
            for ik in iklist:
                writeFCurves(fp, "%s%s" % (bone, ik), quats)
    fp.write("end Action\n\n")
    return

def writeFCurves(fp, name, quats):
    n = len(quats)
    for index in range(4):
        fp.write("\n" +
"  FCurve pose.bones[\"%s\"].rotation_quaternion %d\n" % (name, index))
        for m in range(n):
            t = quats[m][0]
            x = quats[m][index+1]
            fp.write("    kp %d %.4g ;\n" % (t,x))
        fp.write(
"    extrapolation 'CONSTANT' ;\n" +
"  end FCurve \n")
    return

#
#    writeFkIkSwitch(fp, drivers)
#

def writeFkIkSwitch(fp, drivers):
    for (bone, cond, cnsFK, cnsIK, targ, channel, mx) in drivers:
        cnsData = ("ik", 'TRANSFORMS', [('OBJECT', mhx_main.theHuman, targ, channel, C_LOC)])
        for cnsName in cnsFK:
            writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsName), -1, (mx,-mx), [cnsData])
        for cnsName in cnsIK:
            writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsName), -1, (0,mx), [cnsData])
                       
#
#    writeEnumDrivers(fp, drivers):
#
"""
def writeEnumDrivers(fp, drivers):
    for (bone, cns, targ, channel) in drivers:
        drvVars = [("x", 'TRANSFORMS', [('OBJECT', mhx_main.theHuman, targ, channel, C_LOC)])]
        for n, cnsName in enumerate(cns):
            expr = '(x>%.1f)*(x<%.1f)' % (n-0.5, n+0.5)
            writeDriver(fp, True, ('SCRIPTED', expr), "","pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsName), -1, (0,1), drvVars)
"""

#
#   writePropDrivers(fp, drivers, suffix, prefix):
#

def writePropDrivers(fp, drivers, suffix, prefix):
    for (bone, cns, props, expr) in drivers:
        drvVars = []
        n = 1
        for prop in props:
            drvVars.append( ("x%d" % n, 'SINGLE_PROP', [('OBJECT', mhx_main.theHuman, '["%s%s%s"]' % (prefix,prop,suffix))]) )
            n += 1
        writeDriver(fp, True, ('SCRIPTED', expr), "",
            "pose.bones[\"%s%s\"].constraints[\"%s\"].influence" % (bone, suffix, cns), 
            -1, (0,1), drvVars)
    return            
#
#   writeShapePropDrivers(fp, skeys, proxy, prefix):
#

def writeShapePropDrivers(fp, skeys, proxy, prefix):
    for skey in skeys:
        if mhx_main.useThisShape(skey, proxy):
            drvVar = ("x", 'SINGLE_PROP', [('OBJECT', mhx_main.theHuman, '["%s%s"]' % (prefix, skey))])
            writeDriver(fp, True, ('SCRIPTED', "x"), "",
                "key_blocks[\"%s\"].value" % (skey), 
                -1, (0,1), [drvVar])
    return            
    
#
#   writePropDriver(fp, props, expr, dataPath, index):
#

def writePropDriver(fp, props, expr, dataPath, index):
    drvVars = []
    n = 1
    for prop in props:
        drvVars.append( ("x%d" % n, 'SINGLE_PROP', [('OBJECT', mhx_main.theHuman, '["%s"]' % (prop))]) )
        n += 1
    writeDriver(fp, True, ('SCRIPTED', expr), "", dataPath, index, (0,1), drvVars)
    return            
    
#
#    writeTextureDrivers(fp, drivers):
#

def writeTextureDrivers(fp, drivers):
    for (tex, vlist) in drivers.items():
        drvVars = []
        (texnum, targ, channel, coeff) = vlist
        drvVars.append( (targ, 'TRANSFORMS', [('OBJECT', mhx_main.theHuman, targ, channel, C_LOC)]) )
        writeDriver(fp, 'toggle&T_Face', 'AVERAGE', "", "texture_slots[%d].normal_factor" % (texnum), -1, coeff, drvVars)
    return

#
#    writeShapeDrivers(fp, drivers):
# 'BrowsMidDown' : [('PBrows', 'LOC_Z', (0,K), 0, fullScale)]
#

def writeShapeDrivers(fp, drivers, proxy):
    for (shape, vlist) in drivers.items():
        if mhx_main.useThisShape(shape, proxy):
            drvVars = []
            (targ, channel, coeff) = vlist
            drvVars.append( (targ, 'TRANSFORMS', [('OBJECT', mhx_main.theHuman, targ, channel, C_LOC)]) )
            writeDriver(fp, 'toggle&T_Face', 'AVERAGE', "", "key_blocks[\"%s\"].value" % (shape), -1, coeff, drvVars)
    return

#
#    writeMuscleDrivers(fp, drivers, rig):
#     ("LegForward_L", "StretchTo", expr, [("f", "UpLegDwn_L", "BendLegForward_L")], [(0,1), (deg30,1), (deg45,0)])
#

def writeMuscleDrivers(fp, drivers, rig):
    for (bone, cnsName, expr, targs, keypoints)  in drivers:
        drvVars = []
        if expr:
            drvdata = ('SCRIPTED', expr)
        else:
            drvdata = 'MIN'
        for (var, targ1, targ2) in targs:
            drvVars.append( (var, 'ROTATION_DIFF', [('OBJECT', rig, targ1, C_LOC), ('OBJECT', rig, targ2, C_LOC)]) )
        writeDriver(fp, True, drvdata, "","pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsName), -1, keypoints, drvVars)
    return


#
#    writeRotDiffDrivers(fp, drivers, proxy):
#

def writeRotDiffDrivers(fp, drivers, proxy):
    for (shape, vlist) in drivers.items():
        if mhx_main.useThisShape(shape, proxy):
            (targ1, targ2, keypoints) = vlist
            drvVars = [(targ2, 'ROTATION_DIFF', [
            ('OBJECT', mhx_main.theHuman, targ1, C_LOC),
            ('OBJECT', mhx_main.theHuman, targ2, C_LOC)] )]
            writeDriver(fp, True, 'MIN', "", "key_blocks[\"%s\"].value" % (shape), -1, keypoints, drvVars)
    return

#
#    writeDrivers(fp, cond, drivers):
#

def writeDrivers(fp, cond, drivers):
    for drv in drivers:
        (bone, typ, drvdata, name, index, coeffs, variables) = drv
        if typ == 'INFL':
            writeDriver(fp, cond, drvdata, "", "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, name), index, coeffs, variables)
        elif typ == 'ROTE':
            writeDriver(fp, cond, drvdata, "", "pose.bones[\"%s\"].rotation_euler" % bone, index, coeffs, variables)
        elif typ == 'ROTQ':
            writeDriver(fp, cond, drvdata, "", "pose.bones[\"%s\"].rotation_quaternion" % bone, index, coeffs, variables)
        elif typ == 'LOC':
            writeDriver(fp, cond, drvdata, "*theScale", "pose.bones[\"%s\"].location" % bone, index, coeffs, variables)
        elif typ == 'SCALE':
            writeDriver(fp, cond, drvdata, "", "pose.bones[\"%s\"].scale" % bone, index, coeffs, variables)
        else:
            print drv
            raise NameError("Unknown driver type %s" % typ)

#
#    writeDriver(fp, cond, drvdata, extra, channel, index, coeffs, variables):
#

def writeDriver(fp, cond, drvdata, extra, channel, index, coeffs, variables):
    useLoc = False
    useKeypoints = False
    useMod = False
    try:
        (drvtype, expr) = drvdata
    except:
        drvtype = drvdata

    fp.write("\n"+
"    FCurve %s %d %s\n" % (channel, index, cond) +
"      Driver %s\n" % drvtype )

    if drvtype == 'SCRIPTED':
        fp.write("        expression '%s' ;\n" % expr)

    for (var, typ, targets) in variables:
        fp.write("        DriverVariable %s %s\n" % (var,typ))

        if typ == 'TRANSFORMS':
            useMod = True
            for (idtype, targ, boneTarg, ttype, flags) in targets:
                if ttype[0:3] == 'LOC':
                    useLoc = True
                fp.write(
"          Target %s %s\n" % (targ, idtype) +
"            transform_type '%s' ;\n" % ttype +
"            bone_target '%s' ;\n" % boneTarg)
            if flags & C_LOC:
                fp.write("            transform_space 'LOCAL_SPACE' ;\n")
            else:
                fp.write("            transform_space 'WORLD_SPACE' ;\n")
            fp.write("          end Target\n")

        elif typ == 'ROTATION_DIFF':
            useKeypoints = True
            for (idtype, targ, boneTarg, flags) in targets:
                fp.write(
"          Target %s %s\n" % (targ, idtype) +
"            bone_target '%s' ;\n" % boneTarg +
"            transform_space 'WORLD_SPACE' ; \n" +
"          end Target\n")

        elif typ == 'SINGLE_PROP':
            useMod = True
            for (idtype, targ, datapath) in targets:
                fp.write(
"          Target %s %s\n" % (targ, idtype) +
"            data_path '%s' ;\n" % datapath +
"          end Target\n")

        else:
            raise NameError("Unknown driver var type %s" % typ)

        fp.write("        end DriverVariable\n")

    fp.write(
"        show_debug_info True ;\n" +
"      end Driver\n")

    if useMod:
        fp.write(
"      FModifier GENERATOR \n" +
"        active False ;\n" +
"        use_additive False ;\n")

        (a0,a1) = coeffs
        if useLoc:
            fp.write("        coefficients Array %s %s*One%s ;\n" % (a0,a1,extra))
        else:
            fp.write("        coefficients Array %s %s%s ;\n" % (a0,a1,extra))

        fp.write(
"        show_expanded True ;\n" +
"        mode 'POLYNOMIAL' ;\n" +
"        mute False ;\n" +
"        poly_order 1 ;\n" +
"      end FModifier\n")

    if useKeypoints:
        for (x,y) in coeffs:
            fp.write("      kp %.4f %.4f ; \n" % (x,y))

    fp.write(
"      extrapolation 'CONSTANT' ;\n" +
"      lock False ;\n" +
"      select False ;\n" +
"    end FCurve\n")

    return

#
#    setupCircle(fp, name, r):
#    setupCube(fp, name, r):
#    setupCircles(fp):
#

def setupCircle(fp, name, r):
    fp.write("\n"+
"Mesh %s %s \n" % (name, name) +
"  Verts\n")
    for n in range(16):
        v = n*pi/8
        y = 0.5 + 0.02*sin(4*v)
        fp.write("    v %.3f %.3f %.3f ;\n" % (r*math.cos(v), y, r*math.sin(v)))
    fp.write(
"  end Verts\n" +
"  Edges\n")
    for n in range(15):
        fp.write("    e %d %d ;\n" % (n, n+1))
    fp.write("    e 15 0 ;\n")
    fp.write(
"  end Edges\n"+
"end Mesh\n"+
"Object %s MESH %s\n" % (name, name) +
"  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;\n"+
"  parent Refer Object CustomShapes ;\n"+
"end Object\n")
    return

def setupCubeMesh(fp, name, r, offs):
    try:
        (rx,ry,rz) = r
    except:
        (rx,ry,rz) = (r,r,r)
    try:
        (dx,dy,dz) = offs
    except:
        (dx,dy,dz) = (0,offs,0)

    fp.write("\n"+
"Mesh %s %s \n" % (name, name) +
"  Verts\n")
    for x in [-rx,rx]:
        for y in [-ry,ry]:
            for z in [-rz,rz]:
                fp.write("    v %.2f %.2f %.2f ;\n" % (x+dx,y+dy,z+dz))
    fp.write(
"  end Verts\n" +
"  Faces\n" +
"    f 0 1 3 2 ;\n" +
"    f 4 6 7 5 ;\n" +
"    f 0 2 6 4 ;\n" +
"    f 1 5 7 3 ;\n" +
"    f 1 0 4 5 ;\n" +
"    f 2 3 7 6 ;\n" +
"  end Faces\n" +
"end Mesh\n")
    return

def setupCube(fp, name, r, offs):
    setupCubeMesh(fp, name, r, offs)
    fp.write(
"Object %s MESH %s\n" % (name, name) +
"  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;\n" +
"  parent Refer Object CustomShapes ;\n" +
"end Object\n")

def setupCylinder(fp, name, r, h, offs, mat):
    try:
        (rx,ry) = r
    except:
        (rx,ry) = (r,r)
    try:
        (dx,dy,dz) = offs
    except:
        (dx,dy,dz) = (0,offs,0)

    fp.write(
"Mesh %s %s \n" % (name, name) +
"  Verts\n")
    z = h + dz
    for n in range(6):
        a = n*pi/3
        x = -rx*cos(a) + dx
        y = ry*sin(a) + dy
        fp.write("    v %.3f %.3f %.3f ;\n" % (x,z,y))
    z = dz
    for n in range(6):
        a = n*pi/3
        x = -rx*cos(a) + dx
        y = ry*sin(a) + dy
        fp.write("    v %.3f %.3f %.3f ;\n" % (x,z,y))
    fp.write(
"  end Verts\n" +
"  Edges\n" +
"    e 5 7 ;\n" +
"    e 0 1 ;\n" +
"    e 6 7 ;\n" +
"    e 3 7 ;\n" +
"    e 0 2 ;\n" +
"    e 1 3 ;\n" +
"    e 4 5 ;\n" +
"    e 1 5 ;\n" +
"    e 4 6 ;\n" +
"    e 2 3 ;\n" +
"    e 2 6 ;\n" +
"    e 0 4 ;\n" +
"  end Edges\n" +
"  Material %s ;\n" % mat +
"end Mesh\n" +
"Object %s MESH %s\n" % (name, name) +
"  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;\n" +
"  parent Refer Object CustomShapes ;\n" +
#"  Modifier Subsurf SUBSURF\n" +
#"  end Modifier\n" +
"end Object\n")


def setupCircles(fp):
    setupCircle(fp, "MHCircle01", 0.1)
    setupCircle(fp, "MHCircle025", 0.25)
    setupCircle(fp, "MHCircle05", 0.5)
    setupCircle(fp, "MHCircle10", 1.0)
    setupCircle(fp, "MHCircle15", 1.5)
    setupCircle(fp, "MHCircle20", 2.0)
    setupCube(fp, "MHCube01", 0.1, 0)
    setupCube(fp, "MHCube025", 0.25, 0)
    setupCube(fp, "MHCube05", 0.5, 0)
    setupCube(fp, "MHEndCube01", 0.1, 1)
    setupCube(fp, "MHChest", (0.7,0.25,0.5), (0,0.5,0.35))
    setupCube(fp, "MHRoot", (1.25,0.5,1.0), 1)
    return

#
#    setupRig(obj):
#    writeAllArmatures(fp)    
#    writeAllPoses(fp)    
#    writeAllActions(fp)    
#    writeAllDrivers(fp)    
#

import rig_joints_25, rig_body_25
import rig_shoulder_25, rig_arm_25, rig_finger_25
import rig_leg_25, rig_toe_25, rig_face_25, rig_panel_25
#import blenrig_rig        
import rigify_rig

def setupRig(obj):
    global BoneGroups, RecalcRoll, GizmoFiles, VertexGroupFiles
    global ObjectProps, ArmatureProps, CustomProps
    global Joints, HeadsTails, Armature, HeadName

    if mhx_main.theConfig.useRig in ['mhx', 'game']:
        BoneGroups = [
            ('Master', 'THEME13'),
            ('Spine', 'THEME05'),
            ('FK_L', 'THEME09'),
            ('FK_R', 'THEME02'),
            ('IK_L', 'THEME03'),
            ('IK_R', 'THEME04'),
        ]
        RecalcRoll = "['Foot_L','Toe_L','Foot_R','Toe_R','DfmFoot_L','DfmToe_L','DfmFoot_R','DfmToe_R']"
        GizmoFiles = ["./shared/mhx/templates/custom-shapes25.mhx", 
                      "./shared/mhx/templates/panel_gizmo25.mhx",
                      "./shared/mhx/templates/gizmos25.mhx"]

        ObjectProps = [("MhxRig", '"MHX"')]
        ArmatureProps = []
        HeadName = 'Head'
        
        if mhx_main.theConfig.malegenitalia:
            genitalia = "./shared/mhx/templates/vertexgroups-male25.mhx"
        else:
            genitalia = "./shared/mhx/templates/vertexgroups-female25.mhx"

        VertexGroupFiles = ["./shared/mhx/templates/vertexgroups-head25.mhx",
                            "./shared/mhx/templates/vertexgroups-bones25.mhx",
                            genitalia,
                            "./shared/mhx/templates/vertexgroups-palm25.mhx"]
                                                        
        Joints = (
            rig_joints_25.DeformJoints +
            rig_body_25.BodyJoints +
            rig_arm_25.ArmJoints +
            rig_shoulder_25.ShoulderJoints +
            rig_finger_25.FingerJoints +
            rig_leg_25.LegJoints +
            #rig_toe_25.ToeJoints +
            rig_face_25.FaceJoints +
            rig_panel_25.PanelJoints
        )
        
        HeadsTails = (
            rig_body_25.BodyHeadsTails +
            rig_shoulder_25.ShoulderHeadsTails +
            rig_arm_25.ArmHeadsTails +
            rig_finger_25.FingerHeadsTails +
            rig_leg_25.LegHeadsTails +
            #rig_toe_25.ToeHeadsTails +
            rig_face_25.FaceHeadsTails +
            rig_panel_25.PanelHeadsTails
        )

        Armature = (
            rig_body_25.BodyArmature +
            rig_shoulder_25.ShoulderArmature +
            rig_arm_25.ArmArmature +            
            rig_finger_25.FingerArmature +
            rig_leg_25.LegArmature +
            #rig_toe_25.ToeArmature +
            rig_face_25.FaceArmature +
            rig_panel_25.PanelArmature
        )

    elif mhx_main.theConfig.useRig == "blenrig":
        BoneGroups = [('GEN', 'THEME13'),
                      ('IK', 'THEME05'),
                      ('FK', 'THEME09'),
                      ('FACIAL', 'THEME02')]
        RecalcRoll = []              
        VertexGroupFiles = ["./shared/mhx/templates/blenrigmesh_weights.mhx"]
        GizmoFiles = ["./shared/mhx/templates/blenrig_gizmos.mhx"]
            
        Joints = blenrig_rig.BlenrigJoints
        HeadsTails = blenrig_rig.BlenrigHeadsTails
        Armature = blenrig_rig.BlenrigArmature
        ObjectProps = blenrig_rig.BlenrigObjectProps + [("MhxRig", '"Blenrig"')]
        ArmatureProps = blenrig_rig.BlenrigArmatureProps

    elif mhx_main.theConfig.useRig == "rigify":
        BoneGroups = []
        RecalcRoll = []              
        VertexGroupFiles = ["./shared/mhx/templates/vertexgroups-head25.mhx",
                            "./shared/mhx/templates/rigifymesh_weights.mhx"]
        GizmoFiles = ["./shared/mhx/templates/panel_gizmo25.mhx"]
        HeadName = 'head'
        faceArmature = swapParentName(rig_face_25.FaceArmature, 'Head', 'head')
            
        Joints = (
            rig_joints_25.DeformJoints +
            rig_body_25.BodyJoints +
            rigify_rig.RigifyJoints +
            rig_face_25.FaceJoints +
            rig_panel_25.PanelJoints
        )
        
        HeadsTails = (
            rigify_rig.RigifyHeadsTails +
            rig_face_25.FaceHeadsTails +
            rig_panel_25.PanelHeadsTails
        )

        Armature = (
            rigify_rig.RigifyArmature +
            faceArmature +
            rig_panel_25.PanelArmature
        )

        ObjectProps = rigify_rig.RigifyObjectProps + [("MhxRig", '"Rigify"')]
        ArmatureProps = rigify_rig.RigifyArmatureProps

    else:
        raise NameError("Unknown rig %s" % mhx_main.theConfig.useRig)

    (custJoints, custHeadsTails, custArmature, CustomProps) = mhx_custom.setupCustomRig()
    Joints += custJoints
    HeadsTails += custHeadsTails
    Armature += custArmature
    
    newSetupJoints(obj, Joints, True)
    if mhx_main.theConfig.useRig == 'mhx':
        rig_body_25.BodyDynamicLocations()
    setupHeadsTails(HeadsTails)
    return
    
        
def swapParentName(bones, old, new):
    nbones = []
    for bone in bones:
        (name, roll, par, flags, level, bb) = bone
        if par == old:
            nbones.append( (name, roll, new, flags, level, bb) )
        else:
            nbones.append(bone)
    return nbones
    
def writeControlArmature(fp):
    amt = Armature    
    if mhx_main.theConfig.breasts:
        amt += rig_body_25.BreastArmature
    if mhx_main.theConfig.biceps:
        amt += rig_arm_25.BicepsArmature
    if mhx_main.theConfig.malegenitalia:
        amt += rig_body_25.MaleArmature
    writeArmature(fp, amt, True)
    return

def writeControlPoses(fp):
    writeBoneGroups(fp)
    if mhx_main.theConfig.useRig == 'mhx':            
        rig_body_25.BodyControlPoses(fp)
        rig_shoulder_25.ShoulderControlPoses(fp)
        rig_arm_25.ArmControlPoses(fp)
        rig_finger_25.FingerControlPoses(fp)
        rig_leg_25.LegControlPoses(fp)
        #rig_toe_25.ToeControlPoses(fp)
        rig_face_25.FaceControlPoses(fp)
        rig_panel_25.PanelControlPoses(fp)
    elif mhx_main.theConfig.useRig == 'blenrig':
        blenrig_rig.BlenrigWritePoses(fp)
    elif mhx_main.theConfig.useRig == 'rigify':
        rigify_rig.RigifyWritePoses(fp)
        rig_face_25.FaceControlPoses(fp)
        rig_panel_25.PanelControlPoses(fp)
        
    if mhx_main.theConfig.breasts:
        rig_body_25.BreastControlPoses(fp)
    if mhx_main.theConfig.biceps:
        rig_arm_25.BicepsControlPoses(fp)
    if mhx_main.theConfig.malegenitalia:
        rig_body_25.MaleControlPoses(fp)
    for (path, modname) in mhx_main.theConfig.customrigs:
        mod = sys.modules[modname]                
        mod.ControlPoses(fp)

    return

def writeAllActions(fp):
    #rig_arm_25.ArmWriteActions(fp)
    #rig_leg_25.LegWriteActions(fp)
    #rig_finger_25.FingerWriteActions(fp)
    return

def writeAllDrivers(fp):
    if mhx_main.theConfig.useRig == 'mhx':      
        writePropDrivers(fp, rig_arm_25.ArmPropDrivers, "", "&")
        writePropDrivers(fp, rig_arm_25.ArmPropLRDrivers, "_L", "&")
        writePropDrivers(fp, rig_arm_25.ArmPropLRDrivers, "_R", "&")
        writePropDrivers(fp, rig_leg_25.LegPropDrivers, "", "&")
        writePropDrivers(fp, rig_leg_25.LegPropLRDrivers, "_L", "&")
        writePropDrivers(fp, rig_leg_25.LegPropLRDrivers, "_R", "&")
        writePropDrivers(fp, rig_body_25.BodyPropDrivers, "", "&")
        writePropDrivers(fp, rig_face_25.FacePropDrivers, "", "&")
        fingDrivers = rig_finger_25.getFingerPropDrivers()
        writePropDrivers(fp, fingDrivers, "_L", "&")            
        writePropDrivers(fp, fingDrivers, "_R", "&")            
        #rig_panel_25.FingerControlDrivers(fp)
        writeMuscleDrivers(fp, rig_shoulder_25.ShoulderDeformDrivers, mhx_main.theHuman)
        writeMuscleDrivers(fp, rig_arm_25.ArmDeformDrivers, mhx_main.theHuman)
        writeMuscleDrivers(fp, rig_leg_25.LegDeformDrivers, mhx_main.theHuman)
        rig_face_25.FaceDeformDrivers(fp)
    elif mhx_main.theConfig.useRig == 'blenrig':            
        drivers = blenrig_rig.getBlenrigDrivers()
        writeDrivers(fp, True, drivers)
    elif mhx_main.theConfig.useRig == 'rigify':            
        rig_face_25.FaceDeformDrivers(fp)        
    return

def writeAllProperties(fp, typ):
    if typ != 'Object':
        return
    for (key, val) in ObjectProps:
        fp.write("  Property %s %s ;\n" % (key, val))
    for (key, val, string, min, max) in CustomProps:
        fp.write(
'  Property &%s %.2f %s ;\n' % (key, val, string) +
'  PropKeys &%s "min":-%.2f,"max":%.2f, ;\n\n' % (key, min, max) )        
    if mhx_main.theConfig.expressions:
        fp.write("#if toggle&T_Face\n")
        for skey in read_expression.Expressions:
            fp.write(
"  Property *%s 0.0 %s ;\n" % (skey, skey) +
"  PropKeys *%s \"min\":-1.0,\"max\":2.0, ;\n" % skey)
        fp.write("#endif\n")
    return


