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
import os
import sys
import mh2proxy
import armature

from . import the
from the import *
from . import mhxbones
from . import posebone
from . import read_expression
from . import mhx_custom
from . import read_rig

from . import rig_joints_25
from . import rig_body_25
from . import rig_shoulder_25
from . import rig_arm_25
from . import rig_finger_25
from . import rig_leg_25
from . import rig_toe_25
from . import rig_face_25
from . import rig_panel_25
from . import rig_skirt_25
from . import rigify_rig

        
#
#    newSetupJoints (obj, joints):
#    setupHeadsTails(headsTails):
#    findLocation(joint):
#
def newSetupJoints (obj, joints):
    the.Locations = {}
    for (key, typ, data) in joints:
        #print(key)
        if typ == 'j':
            loc = mh2proxy.calcJointPos(obj, data)
            the.Locations[key] = loc
            the.Locations[data] = loc
        elif typ == 'v':
            v = int(data)
            the.Locations[key] = obj.verts[v].co
        elif typ == 'x':
            the.Locations[key] = [float(data[0]), float(data[2]), -float(data[1])]
        elif typ == 'vo':
            v = int(data[0])
            loc = obj.verts[v].co
            the.Locations[key] = [loc[0]+float(data[1]), loc[1]+float(data[3]), loc[2]-float(data[2])]
        elif typ == 'vl':
            ((k1, v1), (k2, v2)) = data
            loc1 = obj.verts[int(v1)].co
            loc2 = obj.verts[int(v2)].co
            the.Locations[key] = vadd(vmul(loc1, k1), vmul(loc2, k2))
        elif typ == 'f':
            (raw, head, tail, offs) = data
            rloc = the.Locations[raw]
            hloc = the.Locations[head]
            tloc = the.Locations[tail]
            #print(raw, rloc)
            vec = aljabr.vsub(tloc, hloc)
            vec2 = aljabr.vdot(vec, vec)
            vraw = aljabr.vsub(rloc, hloc)
            x = aljabr.vdot(vec, vraw) / vec2
            rvec = aljabr.vmul(vec, x)
            nloc = aljabr.vadd(hloc, rvec, offs)
            #print(key, nloc)
            the.Locations[key] = nloc
        elif typ == 'b':
            the.Locations[key] = the.Locations[data]
        elif typ == 'p':
            x = the.Locations[data[0]]
            y = the.Locations[data[1]]
            z = the.Locations[data[2]]
            the.Locations[key] = [x[0],y[1],z[2]]
        elif typ == 'vz':
            v = int(data[0])
            z = obj.verts[v].co[2]
            loc = the.Locations[data[1]]
            the.Locations[key] = [loc[0],loc[1],z]
        elif typ == 'X':
            r = the.Locations[data[0]]
            (x,y,z) = data[1]
            r1 = [float(x), float(y), float(z)]
            the.Locations[key] = aljabr.vcross(r, r1)
        elif typ == 'l':
            ((k1, joint1), (k2, joint2)) = data
            the.Locations[key] = vadd(vmul(the.Locations[joint1], k1), vmul(the.Locations[joint2], k2))
        elif typ == 'o':
            (joint, offsSym) = data
            if type(offsSym) == str:
                offs = the.Locations[offsSym]
            else:
                offs = offsSym
            the.Locations[key] = vadd(the.Locations[joint], offs)
        else:
            raise NameError("Unknown %s" % typ)
    return

def moveOriginToFloor(config):
    if config.feetonground:
        the.Origin = the.Locations['floor']
        for key in the.Locations.keys():
            the.Locations[key] = aljabr.vsub(the.Locations[key], the.Origin)
    else:
        the.Origin = [0,0,0]
    return

def setupHeadsTails(headsTails):
    the.RigHead = {}
    the.RigTail = {}
    for (bone, head, tail) in headsTails:
        the.RigHead[bone] = findLocation(head)
        the.RigTail[bone] = findLocation(tail)
    return 

def findLocation(joint):
    try:
        (bone, offs) = joint
    except:
        offs = 0
    if offs:
        return vadd(the.Locations[bone], offs)
    else:
        return the.Locations[joint]

#
#    writeArmature(fp, config, boneList):
#    addBone25(bone, roll, parent, flags, layers, bbone, fp):
#    addBone24(bone, roll, parent, flags, layers, bbone, fp):
#

def writeArmature(fp, config, boneList):
    if config.mhx25:
        for (bone, roll, parent, flags, layers, bbone) in boneList:
            addBone25(bone, True, roll, parent, flags, layers, bbone, fp)
    else:
        for (bone, roll, parent, flags, layers, bbone) in boneList:
            addBone24(bone, True, roll, parent, flags, layers, bbone, fp)
    return


def addBone25(bone, cond, roll, parent, flags, layers, bbone, fp):
    conn = (flags & F_CON != 0)
    deform = (flags & F_DEF != 0)
    restr = (flags & F_RES != 0)
    wire = (flags & F_WIR != 0)
    lloc = (flags & F_NOLOC == 0)
    lock = (flags & F_LOCK != 0)
    cyc = (flags & F_NOCYC == 0)

    fp.write("\n  Bone %s %s\n" % (bone, cond))
    (x, y, z) = the.RigHead[bone]
    fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,-z,y))
    (x, y, z) = the.RigTail[bone]
    fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,-z,y))
    if type(parent) == tuple:
        (soft, hard) = parent
        if hard:
            fp.write(
"#if toggle&T_HardParents\n" +
"    parent Refer Bone %s ;\n" % hard +
"#endif\n")
        if soft:
            fp.write(
"#if toggle&T_HardParents==0\n" +
"    parent Refer Bone %s ;\n" % soft +
"#endif\n")
    elif parent:
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
    flags24 = 0
    if flags & F_CON:
        flags24 += 0x001
    if flags & F_DEF == 0:
        flags24 += 0x004
    if flags & F_NOSCALE:
        flags24 += 0x0e0

    fp.write("\n\tbone %s %s %x %x\n" % (bone, parent, flags24, layers))
    (x, y, z) = the.RigHead[bone]
    fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,y,z))
    (x, y, z) = the.RigTail[bone]
    fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,y,z))
    fp.write("    roll %.6g %.6g ; \n" % (roll, roll))
    fp.write("\tend bone\n")
    return

#
#    writeBoneGroups(fp, config):
#

def writeBoneGroups(fp, config):
    print "BG", config.boneGroups
    if not fp:
        return
    for (name, the.me) in config.boneGroups:
        fp.write(
"    BoneGroup %s\n" % name +
"      name '%s' ;\n" % name +
"      color_set '%s' ;\n" % the.me +
"    end BoneGroup\n")
    return


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
        cnsData = ("ik", 'TRANSFORMS', [('OBJECT', the.Human, targ, channel, C_LOC)])
        for cnsName in cnsFK:
            writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsName), -1, (mx,-mx), [cnsData])
        for cnsName in cnsIK:
            writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsName), -1, (0,mx), [cnsData])
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
#    setupRig(obj, config, proxyData):
#    writeAllArmatures(fp, config)    
#    writeAllPoses(fp, config)    
#    writeAllActions(fp, config)    
#    writeAllDrivers(fp, config)    
#

def setupRig(obj, config, proxyData):
    the.RigHead = {}
    the.RigTail = {}
    config.vertexWeights = []
    config.customShapes = {}
    config.poseInfo = {}

    print "setupRig", config.rigtype
    if config.rigtype == 'mhx':
        config.boneGroups = [
            ('Master', 'THEME13'),
            ('Spine', 'THEME05'),
            ('FK_L', 'THEME09'),
            ('FK_R', 'THEME02'),
            ('IK_L', 'THEME03'),
            ('IK_R', 'THEME04'),
        ]
        config.recalcRoll = "['Foot_L','Toe_L','Foot_R','Toe_R','DfmFoot_L','DfmToe_L','DfmFoot_R','DfmToe_R']"
        #config.recalcRoll = []
        config.gizmoFiles = ["./shared/mhx/templates/custom-shapes25.mhx", 
                      "./shared/mhx/templates/panel_gizmo25.mhx",
                      "./shared/mhx/templates/gizmos25.mhx"]

        config.objectProps = [("MhxRig", '"MHX"')]
        config.armatureProps = []
        config.headName = 'Head'
        
        config.vertexGroupFiles = ["head", "bones", "palm", "tight"]
        if config.skirtrig == "own":
            config.vertexGroupFiles.append("skirt-rigged")    
        elif config.skirtrig == "inh":
            config.vertexGroupFiles.append("skirt")    

        if config.malerig:
            config.vertexGroupFiles.append( "male" )
                                                        
        joints = (
            rig_joints_25.DeformJoints +
            rig_body_25.BodyJoints +
            rig_body_25.FloorJoints +
            rig_arm_25.ArmJoints +
            rig_shoulder_25.ShoulderJoints +
            rig_finger_25.FingerJoints +
            rig_leg_25.LegJoints +
            #rig_toe_25.ToeJoints +
            rig_face_25.FaceJoints
        )            
        
        headsTails = (
            rig_body_25.BodyHeadsTails +
            rig_shoulder_25.ShoulderHeadsTails +
            rig_arm_25.ArmHeadsTails +
            rig_finger_25.FingerHeadsTails +
            rig_leg_25.LegHeadsTails +
            #rig_toe_25.ToeHeadsTails +
            rig_face_25.FaceHeadsTails
        )

        config.armatureBones = list(rig_body_25.BodyArmature1)
        if config.advancedspine:
            config.armatureBones += rig_body_25.BodyArmature2Advanced
        else:
            config.armatureBones += rig_body_25.BodyArmature2Simple
        config.armatureBones += rig_body_25.BodyArmature3
        if config.advancedspine:
            config.armatureBones += rig_body_25.BodyArmature4Advanced
        else:
            config.armatureBones += rig_body_25.BodyArmature4Simple
        config.armatureBones += rig_body_25.BodyArmature5
        if config.advancedspine:
            config.armatureBones += rig_shoulder_25.ShoulderArmature1Advanced
        else:
            config.armatureBones += rig_shoulder_25.ShoulderArmature1Simple
        config.armatureBones += (
            rig_shoulder_25.ShoulderArmature2 +
            rig_arm_25.ArmArmature +            
            rig_finger_25.FingerArmature +
            rig_leg_25.LegArmature +
            #rig_toe_25.ToeArmature +
            rig_face_25.FaceArmature
        )

    elif config.rigtype == "rigify":
        config.boneGroups = []
        config.recalcRoll = []              
        config.vertexGroupFiles = ["head", "rigify"]
        config.gizmoFiles = ["./shared/mhx/templates/panel_gizmo25.mhx",
                          "./shared/mhx/templates/rigify_gizmo25.mhx"]
        config.headName = 'head'
        faceArmature = swapParentNames(rig_face_25.FaceArmature, 
                           {'Head' : 'head', 'MasterFloor' : None} )
            
        joints = (
            rig_joints_25.DeformJoints +
            rig_body_25.BodyJoints +
            rig_body_25.FloorJoints +
            rigify_rig.RigifyJoints +
            rig_face_25.FaceJoints
        )
        
        headsTails = (
            rigify_rig.RigifyHeadsTails +
            rig_face_25.FaceHeadsTails
        )

        config.armatureBones = (
            rigify_rig.RigifyArmature +
            faceArmature
        )

        config.objectProps = rigify_rig.RigifyObjectProps + [("MhxRig", '"Rigify"')]
        config.armatureProps = rigify_rig.RigifyArmatureProps

    else:
        rigfile = "data/rigs/%s.rig" % config.rigtype
        (locations, boneList, config.vertexWeights) = read_rig.readRigFile(rigfile, obj)        
        joints = (
            rig_joints_25.DeformJoints +
            rig_body_25.FloorJoints +
            rig_face_25.FaceJoints
        )
        headsTails = []
        config.armatureBones = []
        #if config.facepanel:            
        #    joints += rig_panel_25.PanelJoints
        #    headsTails += rig_panel_25.PanelHeadsTails
        #    config.armatureBones += rig_panel_25.PanelArmature
        newSetupJoints(obj, joints)        
        moveOriginToFloor(config)
        for (bone, head, tail) in headsTails:
            the.RigHead[bone] = findLocation(head)
            the.RigTail[bone] = findLocation(tail)

        appendRigBones(boneList, obj, "", L_MAIN, [], config)
        config.boneGroups = []
        config.recalcRoll = []              
        config.vertexGroupFiles = []
        config.gizmoFiles = []
        config.headName = 'Head'
        config.objectProps = [("MhxRig", '"%s"' % config.rigtype)]
        config.armatureProps = []
        config.customProps = []
        print("Default rig %s" % config.rigtype)
        return

    """        
    if config.facepanel:            
        joints += rig_panel_25.PanelJoints
        headsTails += rig_panel_25.PanelHeadsTails
        config.armatureBones += rig_panel_25.PanelArmature
    """
    
    if config.rigtype == 'mhx':
        if config.skirtrig == "own":
            joints += rig_skirt_25.SkirtJoints
            headsTails += rig_skirt_25.SkirtHeadsTails
            config.armatureBones += rig_skirt_25.SkirtArmature        
        if config.malerig:
            config.armatureBones += rig_body_25.MaleArmature        

    (custJoints, custHeadsTails, custArmature, config.customProps) = mhx_custom.setupCustomRig(config)
    joints += custJoints
    headsTails += custHeadsTails
    config.armatureBones += custArmature
    
    newSetupJoints(obj, joints)
    moveOriginToFloor(config)    

    if config.rigtype == 'mhx':
        rig_body_25.BodyDynamicLocations()
    for (bone, head, tail) in headsTails:
        the.RigHead[bone] = findLocation(head)
        the.RigTail[bone] = findLocation(tail)
        
    #print "H1", the.RigHead["UpLeg_L"]
    #print "T1", the.RigTail["UpLeg_L"]

    if not config.clothesrig:
        return
    body = the.RigHead.keys()
    for proxy in proxyData.values():
        if proxy.rig:
            verts = []
            for bary in proxy.realVerts:
                verts.append(mh2proxy.proxyCoord(bary))
            (locations, boneList, weights) = read_rig.readRigFile(proxy.rig, obj, verts=verts) 
            proxy.weights = prefixWeights(weights, proxy.name, body)
            appendRigBones(boneList, obj, proxy.name, L_CLO, body, config)
    return

def prefixWeights(weights, prefix, body):
    pweights = {}
    for name in weights.keys():
        if name in body:
            pweights[name] = weights[name]
        else:
            pweights[prefix+name] = weights[name]
    return pweights

def appendRigBones(boneList, obj, prefix, layer, body, config):        
        for data in boneList:
            (bone0, head, tail, roll, parent0, options) = data
            if bone0 in body:
                continue
            bone = prefix + bone0
            if parent0 == "-":
                parent = None
            elif parent0 in body:
                parent = parent0
            else:
                parent = prefix + parent0
            flags = F_DEF|F_CON
            for (key, value) in options.items():
                if key == "-nc":
                    flags &= ~F_CON
                elif key == "-nd":
                    flags &= ~F_DEF
                elif key == "-res":
                    flags |= F_RES
                elif key == "-circ":
                    name = "Circ"+value[0]
                    config.customShapes[name] = (key, int(value[0]))
                    addPoseInfo(bone, ("CS", name), config)
                    flags |= F_WIR
                elif key == "-box":
                    name = "Box" + value[0]
                    config.customShapes[name] = (key, int(value[0]))
                    addPoseInfo(bone, ("CS", name), config)
                    flags |= F_WIR
                elif key == "-ik":
                    try:
                        pt = options["-pt"]
                    except KeyError:
                        pt = None
                    print(value, pt)
                    value.append(pt)
                    addPoseInfo(bone, ("IK", value), config)
                elif key == "-ik":
                    pass
            config.armatureBones.append((bone, roll, parent, flags, layer, NoBB))
            the.RigHead[bone] = aljabr.vsub(head, the.Origin)
            the.RigTail[bone] = aljabr.vsub(tail, the.Origin)
            
def addPoseInfo(bone, info, config):
    try:
        config.poseInfo[bone]
    except:
        config.poseInfo[bone] = []
    config.poseInfo[bone].append(info)
    return        
        
def swapParentNames(bones, changes):
    nbones = []
    for bone in bones:
        (name, roll, par, flags, level, bb) = bone
        try:
            nbones.append( (name, roll, changes[par], flags, level, bb) )
        except KeyError:
            nbones.append(bone)
    return nbones

def writeControlPoses(fp, config):
    writeBoneGroups(fp, config)
    if config.rigtype == 'mhx':            
        rig_body_25.BodyControlPoses(fp, config)
        rig_shoulder_25.ShoulderControlPoses(fp, config)
        rig_arm_25.ArmControlPoses(fp, config)
        rig_finger_25.FingerControlPoses(fp, config)
        rig_leg_25.LegControlPoses(fp, config)
        #rig_toe_25.ToeControlPoses(fp, config)
        rig_face_25.FaceControlPoses(fp, config)
        if config.malerig:
            rig_body_25.MaleControlPoses(fp, config)
        if config.skirtrig == "own":
            rig_skirt_25.SkirtControlPoses(fp, config)
    elif config.rigtype == 'blenrig':
        blenrig_rig.BlenrigWritePoses(fp, config)
    elif config.rigtype == 'rigify':
        rigify_rig.RigifyWritePoses(fp, config)
        rig_face_25.FaceControlPoses(fp, config)
        
    #if config.facepanel:
    #    rig_panel_25.PanelControlPoses(fp, config)
        
    for (bone, info) in config.poseInfo.items():
        cs = None
        constraints = []
        for (key, value) in info:
            if key == "CS":
                cs = value
            elif key == "IK":
                goal = value[0]
                n = int(value[1])
                inf = float(value[2])
                pt = value[3]
                if pt:
                    print(goal, n, inf, pt)
                    subtar = pt[0]
                    poleAngle = float(pt[1])
                    pt = (poleAngle, subtar)
                constraints =  [('IK', 0, inf, ['IK', goal, n, pt, (True,False,True)])]
        posebone.addPoseBone(fp, config, bone, cs, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, constraints)       
        
    #for (path, modname) in config.customRigs:
    #    mod = sys.modules[modname]                
    #    mod.ControlPoses(fp, config)

    return

def writeAllActions(fp, config):
    #rig_arm_25.ArmWriteActions(fp)
    #rig_leg_25.LegWriteActions(fp)
    #rig_finger_25.FingerWriteActions(fp)
    return


def writeAllDrivers(fp, config):
    if config.rigtype == 'mhx':      
        driverList = (
            armature.drivers.writePropDrivers(fp, rig_arm_25.ArmPropDrivers, "", "Mha") +
            armature.drivers.writePropDrivers(fp, rig_arm_25.ArmPropLRDrivers, "_L", "Mha") +
            armature.drivers.writePropDrivers(fp, rig_arm_25.ArmPropLRDrivers, "_R", "Mha") +
            armature.drivers.writePropDrivers(fp, rig_arm_25.SoftArmPropLRDrivers, "_L", "Mha") +
            armature.drivers.writePropDrivers(fp, rig_arm_25.SoftArmPropLRDrivers, "_R", "Mha") +
            #writeScriptedBoneDrivers(fp, rig_leg_25.LegBoneDrivers) +
            armature.drivers.writePropDrivers(fp, rig_leg_25.LegPropDrivers, "", "Mha") +
            armature.drivers.writePropDrivers(fp, rig_leg_25.LegPropLRDrivers, "_L", "Mha") +
            armature.drivers.writePropDrivers(fp, rig_leg_25.LegPropLRDrivers, "_R", "Mha") +
            armature.drivers.writePropDrivers(fp, rig_leg_25.SoftLegPropLRDrivers, "_L", "Mha") +
            armature.drivers.writePropDrivers(fp, rig_leg_25.SoftLegPropLRDrivers, "_R", "Mha") +
            armature.drivers.writePropDrivers(fp, rig_body_25.BodyPropDrivers, "", "Mha")
        )
        if config.advancedspine:
            driverList += armature.drivers.writePropDrivers(fp, rig_body_25.BodyPropDriversAdvanced, "", "Mha") 
        driverList += (
            armature.drivers.writePropDrivers(fp, rig_face_25.FacePropDrivers, "", "Mha") +
            armature.drivers.writePropDrivers(fp, rig_face_25.SoftFacePropDrivers, "", "Mha")
        )
        fingDrivers = rig_finger_25.getFingerPropDrivers()
        driverList += (
            armature.drivers.writePropDrivers(fp, fingDrivers, "_L", "Mha") +
            armature.drivers.writePropDrivers(fp, fingDrivers, "_R", "Mha") +
            #rig_panel_25.FingerControlDrivers(fp)
            armature.drivers.writeMuscleDrivers(fp, rig_shoulder_25.ShoulderDeformDrivers, the.Human) +
            armature.drivers.writeMuscleDrivers(fp, rig_arm_25.ArmDeformDrivers, the.Human) +
            armature.drivers.writeMuscleDrivers(fp, rig_leg_25.LegDeformDrivers, the.Human)
        )
        faceDrivers = rig_face_25.FaceDeformDrivers(fp)
        driverList += armature.drivers.writeDrivers(fp, True, faceDrivers)
        return driverList
    elif config.rigtype == 'blenrig':            
        drivers = blenrig_rig.getBlenrigDrivers()
        armature.drivers.writeDrivers(fp, True, drivers)
    elif rigtype == 'rigify':            
        rig_face_25.FaceDeformDrivers(fp)        
        armature.drivers.writePropDrivers(fp, rig_face_25.FacePropDrivers, "", "Mha")
        armature.drivers.writePropDrivers(fp, rig_face_25.SoftFacePropDrivers, "", "Mha")
    return []
    

def writeAllProperties(fp, typ, config):
    if typ != 'Object':
        return
    for (key, val) in config.objectProps:
        fp.write("  Property %s %s ;\n" % (key, val))
    for (key, val, string, min, max) in config.customProps:
        fp.write('  DefProp Float Mha%s %.2f %s min=-%.2f,max=%.2f ;\n' % (key, val, string, min, max) )

    """
    if (config.faceshapes and not config.facepanel):
        fp.write("#if toggle&T_Shapekeys\n")
        for skey in rig_panel_25.BodyLanguageShapeDrivers.keys():
            fp.write("  DefProp Float Mhf%s 0.0 %s min=-1.0,max=2.0 ;\n" % (skey, skey))
        fp.write("#endif\n")
    """
    
    if config.expressionunits:
        fp.write("#if toggle&T_Shapekeys\n")
        for skey in read_expression.ExpressionUnits:
            fp.write("  DefProp Float Mhs%s 0.0 %s min=-1.0,max=2.0 ;\n" % (skey, skey))
        fp.write("#endif\n")
    return


