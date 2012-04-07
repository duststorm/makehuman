# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Project Name:        MakeHuman
# Product Home Page:   http://www.makehuman.org/
# Code Home Page:      http://code.google.com/p/makehuman/
# Authors:             Thomas Larsson
# Script copyright (C) MakeHuman Team 2001-2011
# Coding Standards:    See http://sites.google.com/site/makehumandocs/developers-guide



import bpy, os, mathutils, math, time
from math import sin, cos
from mathutils import *
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, FloatProperty, IntProperty, BoolProperty, EnumProperty

from . import utils, props, source, target, rig_mhx, toggle, load, simplify
from . import globvar as the

###################################################################################
#
#    class CAnimData():
#

class CAnimData():
    def __init__(self, name):
        self.nFrames = 0
        self.parent = None

        self.headRest = None
        self.vecRest = None
        self.tailRest = None
        self.roll = 0
        self.offsetRest = None
        self.matrixRest = None
        self.inverseRest = None

        self.frames = {}
        self.heads = {}
        self.quats = {}
        self.matrices = {}
        self.name = name

    def __repr__(self):
        return "<CAnimData n %s p %s f %d>" % (self.name, self.parent, self.nFrames)

#
#    createSourceAnimation(context, rig):
#    createTargetAnimation(context, rig):
#    createAnimData(name, animations, ebones, isTarget):
#

def createSourceAnimation(context, rig):
    context.scene.objects.active = rig
    animations = {}
    for name in rig_mhx.FkBoneList:
        createAnimData(name, animations, rig.data.bones, False)
    return animations

def createTargetAnimation(context, rig):
    context.scene.objects.active = rig
    print(rig.name)
    animations = {}
    for name in the.fkBoneList+the.IkBoneList:
        createAnimData(name, animations, rig.data.bones, True)
    return animations

def createAnimData(name, animations, bones, isTarget):
    try:
        b = bones[name]
    except:
        return
    anim = CAnimData(name)
    animations[name] = anim
    anim.headRest = b.head_local.copy()
    anim.tailRest = b.tail_local.copy()
    anim.vecRest = anim.tailRest - anim.headRest
    try:
        anim.roll = b['Roll']
    except:
        anim.roll = 0

    if isTarget and the.target == the.T_Custom:
        anim.parent = the.parents[name]
    elif b.parent:
        if isTarget:
            anim.parent = target.getParentName(b.parent.name)
        else:
            anim.parent = b.parent.name
    else:
        anim.parent = None

    if anim.parent:
        try:
            animPar = animations[anim.parent]
        except:
            animPar = None
    else:
        animPar = None

    #print("AD", isTarget, anim.name, anim.parent, animPar)

    if animPar:
        anim.offsetRest = anim.headRest - animPar.headRest
    else:
        anim.offsetRest = Vector((0,0,0))    

    (loc, rot, scale) = b.matrix_local.decompose()
    anim.matrixRest = rot.to_matrix()
    anim.inverseRest = anim.matrixRest.inverted()
    return

#
#    makeVectorDict(ob, channels):
#

def makeVectorDict(ob, channels):
    fcuDict = {}
    for fcu in ob.animation_data.action.fcurves:
        words = fcu.data_path.split('"')
        if words[2] in channels:
            name = words[1]
            try:
                x = fcuDict[name]
            except:
                fcuDict[name] = []
            fcuDict[name].append((fcu.array_index, fcu))

    vecDict = {}
    timeDict = {}
    for name in fcuDict.keys():
        fcuDict[name].sort()        
        (index, fcu) = fcuDict[name][0]
        m = len(fcu.keyframe_points)
        for (index, fcu) in fcuDict[name]:
            if len(fcu.keyframe_points) != m:
                raise NameError("Not all F-Curves for %s have the same length" % name)

        vectors = []
        for kp in range(m):
            vectors.append([])
        for (index, fcu) in fcuDict[name]:            
            n = 0
            for kp in fcu.keyframe_points:
                vectors[n].append(kp.co[1])
                n += 1
        vecDict[name] = vectors

        times = []
        for kp in fcu.keyframe_points:
            times.append(kp.co[0])
        timeDict[name] = times                
                    
    return (timeDict, vecDict)
                
#
#    insertAnimation(context, rig, animations, boneList):
#    insertAnimRoot(root, animations, nFrames, locs, rots):
#    insertAnimChild(name, animations, nFrames, rots):
#

def insertAnimation(context, rig, animations, boneList):
    context.scene.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')
    (times,locs) = makeVectorDict(rig, ['].location'])
    (times,rots) = makeVectorDict(rig, ['].rotation_quaternion', '].rotation_euler'])
    try:
        root = 'Root'
        nFrames = len(locs[root])
    except:
        root = target.getTrgBone('Root')
        nFrames = len(locs[root])
    insertAnimRoot(root, animations, nFrames, times[root], locs[root], rots[root])
    bones = rig.data.bones
    for nameSrc in boneList:
        try:
            bones[nameSrc]
            success = (nameSrc != root)
        except:
            success = False
        if success:
            try:
                time = times[nameSrc]
            except:
                time = None
            try:                
                rot = rots[nameSrc]
            except:
                rot = None
            insertAnimChild(nameSrc, animations, nFrames, time, rot)

def insertAnimRoot(root, animations, nFrames, times, locs, rots):
    anim = animations[root]
    if nFrames < 0:
        nFrames = len(locs)
    anim.nFrames = nFrames
    for frame in range(anim.nFrames):
        anim.frames[frame] = times[frame]
        quat = Quaternion(rots[frame])
        anim.quats[frame] = quat
        matrix = anim.matrixRest * quat.to_matrix() * anim.inverseRest
        anim.matrices[frame] = matrix
        anim.heads[frame] =  anim.matrixRest * Vector(locs[frame])+ anim.headRest
    return

def insertAnimChildLoc(nameIK, name, animations, locs):
    animIK = animations[nameIK]
    anim = animations[name]
    animPar = animations[anim.parent]
    animIK.nFrames = anim.nFrames
    for frame in range(anim.nFrames):
        parmat = animPar.matrices[frame]
        animIK.heads[frame] = animPar.heads[frame] + anim.offsetRest * parmat
    return

def fixParent(name, par, animations):
    try:
        animations[par]   
        return par
    except:
        pass
    if not par in animations.keys():
        #print("fix", par)
        if par[0:3] == 'Dfm':
            return par[3:]
        #elif par == 'Shoulder_L':
        #    return 'Clavicle_L'
        #elif par == 'Clavicle_L':
        #    return 'Shoulder_L'
        #elif par == 'Shoulder_R':
        #    return 'Clavicle_R'
        #elif par == 'Clavicle_R':
        #    return 'Shoulder_R'
        else:
            raise NameError("Could not guess parent %s -> %s" % (name, par))

def insertAnimChild(name, animations, nFrames, times, rots):
    try:
        anim = animations[name]
    except:
        return None
    if nFrames < 0:
        nFrames = len(rots)
    par = fixParent(name, anim.parent, animations)
    #print("iAC", name, par)
    animPar = animations[par]   
    anim.nFrames = nFrames
    quat = Quaternion()
    quat.identity()

    parmat = None
    while (not parmat) and animPar:
        try:
            parmat = animPar.matrices[0]
        except:
            parmat = None
        if not parmat:
            animPar = animations[animPar.parent]
            print("Skipped parent %s to %s" % (par, animPar.name))

    for frame in range(anim.nFrames):
        if rots:
            anim.frames[frame] = times[frame]
            try:
                quat = Quaternion(rots[frame])
            except:
                quat = Euler(rots[frame]).to_quaternion()
        anim.quats[frame] = quat
        locmat = anim.matrixRest * quat.to_matrix() * anim.inverseRest
        parmat = animPar.matrices[frame]
        matrix = parmat * locmat
        anim.matrices[frame] = matrix
        anim.heads[frame] = animPar.heads[frame] + parmat * anim.offsetRest
    return anim
            
#
#    poseTrgFkBones(context, trgRig, srcAnimations, trgAnimations, srcFixes)
#

def poseTrgFkBones(context, trgRig, srcAnimations, trgAnimations, srcFixes):
    context.scene.objects.active = trgRig
    bpy.ops.object.mode_set(mode='POSE')
    pbones = trgRig.pose.bones
    
    rootSrc = 'Root'
    rootTrg = target.getTrgBone(rootSrc)
    insertLocationKeyFrames(rootTrg, pbones[rootTrg], srcAnimations[rootSrc], trgAnimations[rootTrg])
    nFrames = srcAnimations[rootSrc].nFrames

    for nameTrg in the.fkBoneList:
        nameSrc = target.getSrcBone(nameTrg)
        trgRoll = safeGet(nameTrg, the.targetRolls)
        trgFix = safeGet(nameTrg, the.targetMats)
        try:
            pb = pbones[nameTrg]
            animTrg = trgAnimations[nameTrg]
        except:
            animTrg = None
        try:
            animSrc = srcAnimations[nameSrc]
        except:
            animSrc = None
        if (not animTrg) or (not animSrc):
            #print("Fail", nameSrc, nameTrg)
            pass
        elif (nameTrg in the.GlobalBoneList) or (not pb.bone.use_inherit_rotation):
            print("global", pb)
            insertGlobalRotationKeyFrames(nameTrg, pb, animSrc, animTrg, trgRoll, trgFix)
        else:
            try:
                srcFix = srcFixes[nameSrc]
            except:
                srcFix = None
            if srcFix or trgFix:
                fixAndInsertLocalRotationKeyFrames(nameTrg, pb, animSrc, animTrg, srcFix, trgRoll, trgFix)
            else:
                insertLocalRotationKeyFrames(nameTrg, pb, animSrc, animTrg, trgRoll)

    insertAnimation(context, trgRig, trgAnimations, the.fkBoneList)
    utils.setInterpolation(trgRig)
    return nFrames

#
#    safeGet(name, struct):
#

def safeGet(name, struct):
    try:
        return struct[name]
    except:
        return None

#
#    insertLocationKeyFrames(name, pb, animSrc, animTrg):
#    insertGlobalRotationKeyFrames(name, pb, animSrc, animTrg, trgRoll, trgFix):
#

def insertLocationKeyFrames(name, pb, animSrc, animTrg):
    locs = []
    for frame in range(animSrc.nFrames):
        loc0 = animSrc.heads[frame] - animTrg.headRest
        loc = animTrg.inverseRest * loc0
        locs.append(loc)
        pb.location = loc
        tframe = animSrc.frames[frame]
        for n in range(3):
            pb.keyframe_insert('location', index=n, frame=tframe, group=name)    
    return locs

def insertIKLocationKeyFrames(nameIK, name, pb, animations):
    pb.bone.select = True
    animIK = animations[nameIK]
    anim = animations[name]
    if animIK.parent:
        animPar = animations[animIK.parent]
    else:
        animPar = None
    locs = []
    for frame in range(anim.nFrames):        
        if animPar:
            loc0 = animPar.heads[frame] + animPar.matrices[frame]*animIK.offsetRest
            offset = anim.heads[frame] - loc0
            mat = animPar.matrices[frame] * animIK.matrixRest
            loc = offset*mat.invert()
        else:
            offset = anim.heads[frame] - animIK.headRest
            loc = animIK.inverseRest * offset
        pb.location = loc
        tframe = anim.frames[frame]
        for n in range(3):
            pb.keyframe_insert('location', index=n, frame=tframe, group=nameIK)    
    return


def insertGlobalRotationKeyFrames(name, pb, animSrc, animTrg, trgRoll, trgFix):
    rots = []
    animTrg.nFrames = animSrc.nFrames
    for frame in range(animSrc.nFrames):
        mat90 = animSrc.matrices[frame]
        animTrg.matrices[frame] = mat90
        matMhx = animTrg.inverseRest * mat90 * animTrg.matrixRest
        rot = matMhx.to_quaternion()
        rots.append(rot)
        utils.setRotation(pb, rot, animSrc.frames[frame], name)
    return rots

def insertLocalRotationKeyFrames(name, pb, animSrc, animTrg, trgRoll):
    animTrg.nFrames = animSrc.nFrames
    for frame in range(animSrc.nFrames):
        rot = animSrc.quats[frame]
        rollRot(rot, trgRoll)
        animTrg.quats[frame] = rot
        utils.setRotation(pb, rot, animSrc.frames[frame], name)
    return

def fixAndInsertLocalRotationKeyFrames(name, pb, animSrc, animTrg, srcFix, trgRoll, trgFix):
    (fixMat, srcRoll) = srcFix
    animTrg.nFrames = animSrc.nFrames
    for frame in range(animSrc.nFrames):
        matSrc = animSrc.quats[frame].to_matrix()
        if fixMat:
            matMhx = fixMat * matSrc
        else:
            matMhx = matSrc
        if trgFix:
            matTrg = trgFix * matMhx
        else:
            matTrg = matMhx
        rot = matMhx.to_quaternion()
        rollRot(rot, srcRoll)
        rollRot(rot, trgRoll)
        animTrg.quats[frame] = rot
        utils.setRotation(pb, rot, animSrc.frames[frame], name)
    return



#
#    rollRot(rot, roll):
#

def rollRot(rot, roll):
    if not roll:
        return
    x = rot.x
    z = rot.z
    rot.x = x*cos(roll) - z*sin(roll)
    rot.z = x*sin(roll) + z*cos(roll)
    return


# ------------------------------------------------------------------------------------
#
#   "New" IK Retarget
#
# ------------------------------------------------------------------------------------

#
#   newPoseTrgIkBones(context, trgRig, nFrames):
#   copyMatrix(info):
#   revertMatrix(pb):
#

class CIkInfo:
    def __init__(self, rig, ikname):
        self.ik = rig.pose.bones[ikname]
        self.fk = None
        self.parent = None
        self.fakepar = None
        self.empty = None
        self.reverse = False
        self.hasLoc = True
        self.restInv = None
        self.rotmode = None

def setupIkInfo(rig):
    infos = []
    for (ikname, fkname) in [
        ("Wrist_L", "Hand_L"), 
        ("Wrist_R", "Hand_R"),
        ("LegIK_L", "LegFK_L"), 
        ("LegIK_R", "LegFK_R")
        ]:
        info = CIkInfo(rig, ikname)
        info.fk = rig.pose.bones[fkname]
        info.parent = info.ik.parent
        infos.append(info)
        
    for (ikname, parname, fakepar) in [
        ("ElbowPT_L", "Clavicle_L", "UpArm_L"), 
        ("ElbowPT_R", "Clavicle_R", "UpArm_R"),
        ("KneePT_L", "LegIK_L", "UpLeg_L"), 
        ("KneePT_R", "LegIK_R", "UpLeg_R")
        ]:
        info = CIkInfo(rig, ikname)
        info.parent = rig.pose.bones[parname]
        info.fakepar = rig.pose.bones[fakepar]
        infos.append(info)

    for (ikname, parname, fkname) in [
        ("ToeRev_L", "LegIK_L", "Toe_L"), 
        ("ToeRev_L", "LegIK_L", "Toe_L"),
        ("FootRev_L", "ToeRev_L", "Foot_L"), 
        ("FootRev_L", "ToeRev_L", "Foot_L")
        ]:
        info = CIkInfo(rig, ikname)
        info.fk = rig.pose.bones[fkname]
        info.parent = rig.pose.bones[parname]
        info.reverse = True
        info.hasLoc = False
        infos.append(info)

    for info in infos:
        if info.ik.rotation_mode == 'QUATERNION':
            info.rotmode = "rotation_quaternion"
        else:
            info.rotmode = "rotation_euler"
        info.restInv = info.ik.bone.matrix_local.inverted()
        if info.parent:
            info.restInv = info.restInv * info.parent.bone.matrix_local
    
    return infos

def turnOffDrivers(rig):    
    fkBones = [
        "UpArm_L", "UpArm_R", 
        "LoArm_L", "LoArm_R", 
        "Hand_L", "Hand_R",
        "UpLeg_L", "UpLeg_R",
        "LoLeg_L", "LoLeg_R",
        "Foot_L", "Foot_R",
        "Toe_L", "Toe_R"
        ]
    drivers = []
    for fcu in rig.animation_data.drivers:
        words = fcu.data_path.split('"')
        if words[1] in fkBones:
            drv = fcu.driver
            drivers.append((fcu, drv.type, drv.expression))
            drv.type = 'SCRIPTED'
            drv.expression = "0.0"
    return drivers    

def turnOnDrivers(drivers):    
    for (fcu, type, expression) in drivers:
        fcu.driver.type = type
        fcu.driver.expression = expression
    return
    
def newPoseTrgIkBones(context, rig, nFrames):
    bpy.ops.object.mode_set(mode='POSE')

    drivers = turnOffDrivers(rig)    
    infos = setupIkInfo(rig)    
    rig.data.pose_position = 'REST'
    for info in infos:
        if info.fakepar:
            empty = bpy.data.objects.new("_"+info.ik.name, None)
            context.scene.objects.link(empty)
            empty.parent = rig
            empty.parent_type = 'BONE'
            empty.parent_bone = info.fakepar.name
            offs = info.ik.bone.head_local - info.fakepar.bone.tail_local
            mat = info.fakepar.bone.matrix_local.to_3x3().inverted()
            empty.location = mat*offs
            info.empty = empty
    rig.data.pose_position = 'POSE'  

    print("Copy animation to IK bones")
    for frame in range(nFrames):
        context.scene.frame_set(frame)
        for info in infos:
            copyMatrix(info, frame)
        if frame % 10 == 0:
            print(frame)

    turnOnDrivers(drivers)
          
    for info in infos:
        if info.empty:
            info.empty.parent = None
            info.empty.name = "#"+info.empty.name
            context.scene.objects.unlink(info.empty)
            info.empty = None
    return            

def copyMatrix(info, frame):
    #print(info.ik.name, info.fk, info.empty, info.parent)

    if info.empty:
        #fkMat = Matrix.Translation(info.empty.location)
        fkMat = info.empty.matrix_world
    elif info.reverse:
        fkMat = revertMatrix(info.fk)
    else:
        fkMat = info.fk.matrix
    if info.parent:
        parInv = info.parent.matrix.inverted()        
        info.ik.matrix_basis = info.restInv * parInv * fkMat
    else:
        info.ik.matrix_basis = info.restInv * fkMat
    if info.hasLoc:
        info.ik.keyframe_insert("location", frame=frame, group=info.ik.name)
    info.ik.keyframe_insert(info.rotmode, frame=frame, group=info.ik.name)    
    return
    
def revertMatrix(pb):
    mat = pb.matrix.copy()
    for i in range(3):
        mat[3][i] = pb.tail[i]
        for j in range(0,2):
            mat[j][i] *= -1
    return mat            

# ------------------------------------------------------------------------------------
#
#   Old IK Retarget
#
# ------------------------------------------------------------------------------------

#
#    oldPoseTrgIkBones(context, trgRig, trgAnimations)
#

def oldPoseTrgIkBones(context, trgRig, trgAnimations):
    bpy.ops.object.mode_set(mode='POSE')
    pbones = trgRig.pose.bones

    for name in the.IkBoneList:        
        (realPar, fakePar, copyRot, reverse) = the.IkParents[name]
        pb = pbones[name]
        pb.bone.select = True
        if copyRot:
            animCopy = trgAnimations[copyRot]
        else:
            animCopy = None
        if reverse:    
            insertReverseIkKeyFrames(name, pb, trgAnimations[name],  trgAnimations[realPar], animCopy)
        elif realPar:
            insertParentedIkKeyFrames(name, pb, trgAnimations[name],  trgAnimations[realPar], trgAnimations[fakePar], animCopy)
        else:
            insertRootIkKeyFrames(name, pb, trgAnimations[name], trgAnimations[fakePar], animCopy)
    return
    
#
#    insertParentedIkKeyFrames(name, pb, anim, animReal, animFake, animCopy):
#

def insertParentedIkKeyFrames(name, pb, anim, animReal, animFake, animCopy):
    offsetFake = anim.headRest - animFake.headRest
    offsetReal = anim.headRest - animReal.headRest
    if animCopy:
        roll = anim.roll - animCopy.roll
    else:
        roll = 0
    for frame in range(animFake.nFrames):        
        locAbs = animFake.heads[frame] + animFake.matrices[frame] * offsetFake
        headAbs = animReal.heads[frame] + animReal.matrices[frame] * offsetReal
        #debugPrintVecVec(locAbs, headAbs)
        offset = locAbs - headAbs
        mat = animReal.matrices[frame] * anim.matrixRest
        if pb.bone.use_local_location:
            inv = mat.copy()
            inv.invert()
            loc = inv*offset
            pb.location = loc
        else:
            pb.location = offset
        anim.heads[frame] = locAbs
        tframe = animFake.frames[frame]
        for n in range(3):
            pb.keyframe_insert('location', index=n, frame=tframe, group=name)    

        if animCopy:
            mat = mat * animCopy.inverseRest * animCopy.matrices[frame]
        anim.matrices[frame] = mat
        matMhx = anim.inverseRest * mat * anim.matrixRest
        rot = matMhx.to_quaternion()
        #rollRot(rot, roll)
        utils.setRotation(pb, rot, animFake.frames[frame], name)
    return

#
#    insertReverseIkKeyFrames(name, pb, anim, animReal, animCopy):
#
    
def vecString(vec):
    return "%.3f %.3f %.3f" % (vec[0], vec[1], vec[2])

def insertReverseIkKeyFrames(name, pb, anim, animReal, animCopy):
    offsetCopy = anim.headRest - animCopy.headRest
    offsetReal = anim.headRest - animReal.headRest
    rotX = Matrix.Rotation(math.pi, 3, 'X')
    #print("*** %s %s %s" % (name, vecString(animCopy.headRest), vecString(offsetCopy)))
    for frame in range(animCopy.nFrames):        
        locAbs = animCopy.heads[frame] + animCopy.matrices[frame] * offsetCopy
        headAbs = animReal.heads[frame] + animReal.matrices[frame] * offsetReal
        offset = locAbs - headAbs
        mat = animReal.matrices[frame] * anim.matrixRest
        if pb.bone.use_local_location:
            inv = mat.copy()
            inv.invert()
            loc = offset*inv
            pb.location = loc
        else:
            pb.location = offset
        anim.heads[frame] = locAbs
        tframe = animCopy.frames[frame]
        for n in range(3):
            pb.keyframe_insert('location', index=n, frame=tframe, group=name)    

        mat = mat * animCopy.inverseRest * animCopy.matrices[frame]
        anim.matrices[frame] = mat
        matMhx = rotX * anim.inverseRest * mat * anim.matrixRest * rotX
        rot = matMhx.to_quaternion()
        utils.setRotation(pb, rot, animCopy.frames[frame], name)
    return

#
#    insertRootIkKeyFrames(name, pb, anim, animFake, animCopy):
#

def insertRootIkKeyFrames(name, pb, anim, animFake, animCopy):
    locs = []
    offsetFake = anim.headRest - animFake.headRest
    if animCopy:
        roll = anim.roll - animCopy.roll
    else:
        roll = 0
    for frame in range(animFake.nFrames):        
        locAbs = animFake.heads[frame] + animFake.matrices[frame] * offsetFake
        offset = locAbs - anim.headRest
        if pb.bone.use_local_location:
            loc = anim.inverseRest * offset
            pb.location = loc
        else:
            pb.location = offset
        anim.heads[frame] = locAbs
        tframe = animFake.frames[frame]
        for n in range(3):
            pb.keyframe_insert('location', index=n, frame=tframe, group=name)    

        mat = anim.matrixRest
        if animCopy:
            mat = mat * animCopy.inverseRest * animCopy.matrices[frame] 
        anim.matrices[frame] = mat
        matMhx = anim.inverseRest * mat * anim.matrixRest
        rot = matMhx.to_quaternion()
        #rollRot(rot, roll)
        utils.setRotation(pb, rot, animFake.frames[frame], name)
    return

#
#    retargetMhxRig(context, srcRig, trgRig):
#

def retargetMhxRig(context, srcRig, trgRig):
    scn = context.scene
    source.setArmature(srcRig)
    print("Retarget %s --> %s" % (srcRig, trgRig))
    if trgRig.animation_data:
        trgRig.animation_data.action = None

    trgAnimations = createTargetAnimation(context, trgRig)
    srcAnimations = createSourceAnimation(context, srcRig)
    insertAnimation(context, srcRig, srcAnimations, rig_mhx.FkBoneList)
    onoff = toggle.toggleLimitConstraints(trgRig)
    toggle.setLimitConstraints(trgRig, 0.0)
    if scn.McpApplyFixes:
        srcFixes = the.fixesList[srcRig["McpArmature"]]
    else:
        srcFixes = None
    #debugOpen()
    nFrames = poseTrgFkBones(context, trgRig, srcAnimations, trgAnimations, srcFixes)
    if scn.McpNewIkRetarget:
        newPoseTrgIkBones(context, trgRig, nFrames)
    else:
        oldPoseTrgIkBones(context, trgRig, trgAnimations)
    #debugClose()
    utils.setInterpolation(trgRig)
    if onoff == 'OFF':
        toggle.setLimitConstraints(trgRig, 1.0)
    else:
        toggle.setLimitConstraints(trgRig, 0.0)

    act = trgRig.animation_data.action
    act.name = trgRig.name[:4] + srcRig.name[2:]
    act.use_fake_user = True
    print("Retargeted %s --> %s" % (srcRig, trgRig))
    return
    
#
#    normalizeAnimation(rig):
#

def normalizeAnimation(rig):
    if not rig.animation_data:
        return
    act = rig.animation_data.action
    if not act:
        return
    active = {}
    for fcu in act.fcurves:
        for kp in fcu.keyframe_points:
            active[kp.co[0]] = True
    for fcu in act.fcurves:
        for frame in active.keys():
            value = fcu.evaluate(frame)
            fcu.keyframe_points.insert(frame, value)
    return        

#
#    loadRetargetSimplify(context, filepath):
#

def loadRetargetSimplify(context, filepath):
    print("Load and retarget %s" % filepath)
    time1 = time.clock()
    scn = context.scene
    (srcRig, trgRig) = load.readBvhFile(context, filepath, scn, False)
    load.renameAndRescaleBvh(context, srcRig, trgRig)
    retargetMhxRig(context, srcRig, trgRig)
    if scn.McpDoSimplify:
        simplify.simplifyFCurves(context, trgRig, False, False)
    if scn.McpRescale:
        simplify.rescaleFCurves(context, trgRig, scn.McpRescaleFactor)
    load.deleteSourceRig(context, srcRig, 'Y_')
    time2 = time.clock()
    print("%s finished in %.3f s" % (filepath, time2-time1))
    return

#
#   class VIEW3D_OT_OldRetargetMhxButton(bpy.types.Operator):
#

class VIEW3D_OT_OldRetargetMhxButton(bpy.types.Operator):
    bl_idname = "mcp.old_retarget_mhx"
    bl_label = "Retarget selected to active"

    def execute(self, context):
        trgRig = context.object
        target.guessTargetArmature(trgRig, context.scene)
        for srcRig in context.selected_objects:
            if srcRig != trgRig:
                normalizeAnimation(srcRig)
                retargetMhxRig(context, srcRig, trgRig)
        return{'FINISHED'}    

#
#   class VIEW3D_OT_OldLoadRetargetSimplify(bpy.types.Operator):
#

class VIEW3D_OT_OldLoadRetargetSimplifyButton(bpy.types.Operator, ImportHelper):
    bl_idname = "mcp.old_load_retarget_simplify"
    bl_label = "Load, retarget, simplify"

    filename_ext = ".bvh"
    filter_glob = StringProperty(default="*.bvh", options={'HIDDEN'})
    filepath = StringProperty(name="File Path", description="Filepath used for importing the BVH file", maxlen=1024, default="")

    def execute(self, context):
        loadRetargetSimplify(context, self.properties.filepath)
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    
