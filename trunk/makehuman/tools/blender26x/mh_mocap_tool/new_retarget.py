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
from bpy.props import *

from . import utils, props, source, target, rig_mhx, toggle, load, simplify
from . import globvar as the

    
#
#   class CBoneData:
#

class CBoneData:
    def __init__(self, srcBone, trgBone):
        self.name = trgBone.name
        self.parent = None        
        self.matrices = {}        
        self.srcPoseBone = srcBone        
        self.trgPoseBone = trgBone
        self.trgRestMat = None
        self.trgRestInv = None
        self.trgBakeMat = None
        self.trgBakeInv = None
        self.trgOffset = None
        self.rotOffset = None
        self.rotOffsInv = None
        self.rollMat = None
        self.rollInv = None
        return
        
class CMatrixGroup:
    def __init__(self, srcMat, frame):
        self.frame = frame
        self.srcMatrix = srcMat.copy()
        self.trgMatrix = None
        return
        
    def __repr__(self):
        return "<CMat %d %s %s>" % (self.frame, self.srcMatrix, self.trgMatrix)
        
        
class CAnimation:
    def __init__(self, srcRig, trgRig):
        self.srcRig = srcRig
        self.trgRig = trgRig
        self.boneDatas = {}
        self.boneDataList = []
        return

#
#
#

KeepRotationOffset = [
    "Root", "Pelvis", "Hips",
    "Spine1",
    "Spine2", "Spine3",
    "Neck", "Head",
    "Clavicle_L", "Clavicle_R",
    "Foot_L", "Foot_R", "Toe_L", "Toe_R"
]

SpineBone = [
    "Spine1",
    "Spine2", "Spine3",
    "Neck", "Head",
    "Foot_L", "Foot_R", 
    "Toe_L", "Toe_R"
]

PatchX = [
    "Toe_L", "Toe_R"
]

#
#
#

def setTranslation(mat, loc):
    for m in range(3):
        mat[m][3] = loc[m][3]

def setRotation(mat, rot):
    for m in range(3):
        for n in range(3):
            mat[m][n] = rot[m][n]
            
def keepRollOnly(mat):
    for n in range(4):
        mat[1][n] = 0
        mat[n][1] = 0
        mat[3][n] = 0
        mat[n][3] = 0
    mat[1][1] = 1
            
#
#   retargetFkBone(boneData, frame):
#

def retargetFkBone(boneData, frame):
    srcBone = boneData.srcPoseBone
    trgBone = boneData.trgPoseBone
    name = trgBone.name
    matGrp = boneData.matrices[frame]
    srcRot = matGrp.srcMatrix  #* srcData.rig.matrix_world
    bakeMat = matGrp.srcMatrix

    # Set translation offset
    parent = boneData.parent
    if parent:
        parMat = parent.matrices[frame].srcMatrix
        parInv = parMat.inverted()
        loc = parMat * boneData.trgOffset
        setTranslation(bakeMat, loc)
        bakeMat = parInv * bakeMat
        parRest = parent.trgRestMat
        if 0 and parent.rollMat:
            print("parent", name)
            utils.printMat4("roll", boneData.rollMat)
            utils.printMat4("prol", parent.rollMat)
            utils.printMat4("rest1", parRest)
            parRot = parent.rollInv * parRest * parent.rollMat
            #setRotation(parRest, parRot)
            utils.printMat4("rest2", parRest)
            #setRotation(parRest, parRoll)
        bakeMat = parRest * bakeMat
    else:
        parMat = None
        parRotInv = None

    # Set rotation offset        
    if boneData.rotOffset:
        rot = boneData.rotOffset
        if parent and parent.rotOffsInv:
            rot = rot * parent.rotOffsInv        
        bakeRot = bakeMat * rot
        setRotation(bakeMat, bakeRot)
    else:
        rot = None
        
    trgMat = boneData.trgRestInv * bakeMat
    trgBone.matrix_basis = trgMat
    if 0 and trgBone.name == "Hip_L":
        print(name)
        utils.printMat4(" PM", parMat, "  ")
        utils.printMat4(" PR", parent.rotOffsInv, "  ")
        utils.printMat4(" RO", boneData.rotOffset, "  ")
        utils.printMat4(" BR", bakeRot, "  ")
        utils.printMat4(" BM", bakeMat, "  ")
        utils.printMat4(" Trg", trgMat, "  ")
        #halt
    
    if trgBone.name in PatchX:
        trgBone.rotation_euler[0] = 0
        
    utils.insertRotationKeyFrame(trgBone, frame)
    if 0 or not boneData.parent:
        trgBone.keyframe_insert("location", frame=frame, group=trgBone.name)
    matGrp.trgMatrix = trgBone.matrix.copy()
    return        
   
#
#   collectSrcMats(anim, frames, scn):
#

def hideObjects(scn, rig):
    objects = []
    for ob in scn.objects:
        if ob != rig:
            objects.append((ob, list(ob.layers)))
            ob.layers = 20*[False]
    return objects
    
def unhideObjects(objects):
    for (ob,layers) in objects:
        ob.layers = layers
    return
    
def collectSrcMats(anim, frames, scn):
    objects = hideObjects(scn, anim.srcRig)
    try:            
        for frame in frames:
            scn.frame_set(frame)
            if frame % 100 == 0:
                print("Collect", int(frame))
            for boneData in anim.boneDataList:
                mat = CMatrixGroup(boneData.srcPoseBone.matrix, frame)
                boneData.matrices[frame] = mat
    finally:
        unhideObjects(objects)
    return                

#
#   retargetMatrices(anim, frames, scn):
#

def retargetMatrices(anim, frames, scn):
    for frame in frames:
        if frame % 100 == 0:
            print("Retarget", int(frame))
        for boneData in anim.boneDataList:
            retargetFkBone(boneData, frame)
        retargetIkBones(anim.trgRig, frame)        
    return               
 
  
#
#   setupFkBones(srcRig, trgRig, boneAssoc, parAssoc, anim):
#
    
def getParent(parName, parAssoc, trgRig, anim):
    if not parName:
        return None
    try:
        trgParent = trgRig.pose.bones[parName]
    except KeyError:
        return None
    try:
        anim.boneDatas[trgParent.name]        
        return trgParent
    except        :
        pass
    return getParent(parAssoc[trgParent.name], parAssoc, trgRig, anim)
    
def setupFkBones(srcRig, trgRig, boneAssoc, parAssoc, anim):
    for (trgName, srcName) in boneAssoc:
        try:
            trgBone = trgRig.pose.bones[trgName]
            srcBone = srcRig.pose.bones[srcName]
        except:
            print("  -", trgName, srcName)
            continue
        boneData = CBoneData(srcBone, trgBone)
        anim.boneDatas[trgName] = boneData   
        anim.boneDataList.append(boneData)
        boneData.trgRestMat = trgBone.bone.matrix_local

        trgRoll = utils.getRoll(trgBone.bone)
        srcRoll = utils.getRoll(srcBone.bone)
        diff = srcRoll-trgRoll
        if abs(diff) > 0.1:            
            boneData.rollMat = Matrix.Rotation(diff, 4, 'Y') 
            boneData.rollInv = boneData.rollMat.inverted()

        boneData.trgRestInv = trgBone.bone.matrix_local.inverted()
        boneData.trgBakeMat = boneData.trgRestMat  

        trgParent = None        
        if trgBone.parent:  #trgBone.bone.use_inherit_rotation:
            trgParent = getParent(parAssoc[trgName], parAssoc, trgRig, anim)
            if trgParent:
                boneData.parent = anim.boneDatas[trgParent.name]
                parRest = boneData.parent.trgRestMat
                parRestInv = boneData.parent.trgRestInv
                offs = trgBone.bone.head_local - trgParent.bone.head_local
                boneData.trgOffset = parRestInv * Matrix.Translation(offs) * parRest
                boneData.trgBakeMat = parRestInv * boneData.trgRestMat

        if trgName in KeepRotationOffset:        
            offs = trgBone.bone.matrix_local*srcBone.bone.matrix_local.inverted()
            boneData.rotOffset = boneData.trgRestInv * offs * boneData.trgRestMat
            if trgParent and (trgName in SpineBone):                
                boneData.rotOffsInv = boneData.rotOffset.inverted()
                        
        boneData.trgBakeInv = boneData.trgBakeMat.inverted()   
    return


#
#    retargetMhxRig(context, srcRig, trgRig):
#

def retargetMhxRig(context, srcRig, trgRig):
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.rot_clear()
    bpy.ops.pose.loc_clear()

    scn = context.scene
    if scn.McpGuessSrcRig:
        source.scanSourceRig(scn, srcRig)
    source.setArmature(srcRig)
    print("Retarget %s --> %s" % (srcRig, trgRig))
    if trgRig.animation_data:
        trgRig.animation_data.action = None

    frames = utils.activeFrames(srcRig)
    anim = CAnimation(srcRig, trgRig)
    (boneAssoc, ikBoneAssoc, parAssoc, rolls, mats, ikBones, ikParents) = target.makeTargetAssoc(trgRig, scn)
 
    setupFkBones(srcRig, trgRig, boneAssoc, parAssoc, anim)

    scn.objects.active = trgRig
    scn.update()
    bpy.ops.object.mode_set(mode='POSE')  
    bpy.ops.pose.select_all(action='DESELECT')
    for name in ["Root", "Hips", "Pelvis"]:
        trgRig.data.bones[name].select = True

    try:
        scn.frame_current = frames[0]
    except:
        print("No frames found. Quitting.")
        return
    oldData = changeTargetData(trgRig)
    frameBlock = frames[0:100]
    index = 0
    try:
        while frameBlock:
            collectSrcMats(anim, frameBlock, scn)
            retargetMatrices(anim, frameBlock, scn)
            index += 100
            frameBlock = frames[index:index+100]
            
        scn.frame_current = frames[0]
        setInverse(trgRig, trgRig.pose.bones["Ankle_L"])
        setInverse(trgRig, trgRig.pose.bones["Ankle_R"])
    finally:                
        restoreTargetData(trgRig, oldData)
            
    utils.setInterpolation(trgRig)
    act = trgRig.animation_data.action
    act.name = trgRig.name[:4] + srcRig.name[2:]
    act.use_fake_user = True
    print("Retargeted %s --> %s" % (srcRig, trgRig))
    return

#
#   changeTargetData(rig):    
#   restoreTargetData(rig, data):
#
    
def changeTargetData(rig):    
    tempProps = [
        ("&RotationLimits", 0.0),
        ("&ArmIk_L", 0.0),
        ("&ArmIk_R", 0.0),
        ("&LegIk_L", 0.0),
        ("&LegIk_R", 0.0),
        ("&SpineIk", 0),
        ("&SpineInvert", 0),
        ("&ElbowPlant_L", 0),
        ("&ElbowPlant_R", 0),
        ]

    props = []
    for (key, value) in tempProps:
        try:
            props.append((key, rig[key]))
            rig[key] = value
        except KeyError:
            pass

    permProps = [
        ("&HandFollowsShoulder", 0),
        ("&HandFollowsWrist", 0),
        ("&FootFollowsHip", 0),
        ("&FootFollowsFoot", 0),
        ]

    for (key, value) in permProps:
        rig[key+"_L"] = value
        rig[key+"_R"] = value
 
    layers = list(rig.data.layers)
    rig.data.layers = 32*[True]
    locks = []
    for pb in rig.pose.bones:
        constraints = []
        for cns in pb.constraints:
            if cns.type in ['LIMIT_ROTATION', 'LIMIT_SCALE', 'LIMIT_DISTANCE']:
                constraints.append( (cns, cns.mute) )
                cns.mute = True
        if pb.name in PatchX:
            mode = pb.rotation_mode
            pb.rotation_mode = 'YXZ'
        else:
            mode = None
        locks.append( (pb, pb.lock_location, pb.lock_rotation, pb.lock_scale, mode, constraints) )
        pb.lock_location = [False, False, False]
        pb.lock_rotation = [False, False, False]
        pb.lock_scale = [False, False, False]
    return (props, layers, locks)
    
def restoreTargetData(rig, data):
    (props, rig.data.layers, locks) = data
    
    for (key,value) in props:
        rig[key] = value
    return
    
    for lock in locks:
        (pb, lockLoc, lockRot, lockScale, mode, constraints) = lock
        pb.lock_location = lockLoc
        pb.lock_rotation = lockRot
        pb.lock_scale = lockScale
        if mode:
            pb.rotation_mode = mode
        for (cns, mute) in constraints:
            cns.mute = mute
    return        
        

#########################################
#
#   FK-IK snapping. 
#   The bulk of this code was shamelessly stolen from Rigify.
#
#########################################

def getPoseMatrixInOtherSpace(mat, pb):
    rest = pb.bone.matrix_local.copy()
    restInv = rest.inverted()
    if pb.parent:
        parMat = pb.parent.matrix.copy()
        parInv = parMat.inverted()
        parRest = pb.parent.bone.matrix_local.copy()
    else:
        parMat = Matrix()
        parInv = Matrix()
        parRest = Matrix()

    # Get matrix in bone's current transform space
    smat = restInv * (parRest * (parInv * mat))
    return smat


def getLocalPoseMatrix(pb):
    return getPoseMatrixInOtherSpace(pb.matrix, pb)


def setPoseTranslation(pb, mat, frame):
    if pb.bone.use_local_location == True:
        pb.location = mat.to_translation()
        pb.keyframe_insert("location", frame=frame, group=pb.name)
    else:
        loc = mat.to_translation()

        rest = pb.bone.matrix_local.copy()
        parent = getParent(pb)
        if parent:
            parRest = parent.bone.matrix_local.copy()
        else:
            parRest = Matrix()

        q = (parRest.inverted() * rest).to_quaternion()
        pb.location = q * loc
        pb.keyframe_insert("location", frame=frame, group=pb.name)


def setPoseRotation(pb, mat, frame):
    q = mat.to_quaternion()

    if pb.rotation_mode == 'QUATERNION':
        pb.rotation_quaternion = q
        pb.keyframe_insert("rotation_quaternion", frame=frame, group=pb.name)
    elif pb.rotation_mode == 'AXIS_ANGLE':
        pb.rotation_axis_angle[0] = q.angle
        pb.rotation_axis_angle[1] = q.axis[0]
        pb.rotation_axis_angle[2] = q.axis[1]
        pb.rotation_axis_angle[3] = q.axis[2]
        pb.keyframe_insert("rotation_axis_angle", frame=frame, group=pb.name)
    else:
        pb.rotation_euler = q.to_euler(pb.rotation_mode)
        pb.keyframe_insert("rotation_euler", frame=frame, group=pb.name)


def setPoseScale(pb, mat, frame):
    pb.scale = mat.to_scale()
    #pb.keyframe_insert("scale", frame=frame, group=pb.name)

def matchPoseTranslation(pb, tarPb, frame):
    mat = getPoseMatrixInOtherSpace(tarPb.matrix, pb)
    setPoseTranslation(pb, mat, frame)
    #bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.ops.object.mode_set(mode='POSE')

def matchPoseRotation(pb, tarPb, frame):
    mat = getPoseMatrixInOtherSpace(tarPb.matrix, pb)
    setPoseRotation(pb, mat, frame)
    #bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.ops.object.mode_set(mode='POSE')

def matchPoseScale(pb, tarPb, frame):
    mat = getPoseMatrixInOtherSpace(tarPb.matrix, pb)
    setPoseScale(pb, mat, frame)
    #bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.ops.object.mode_set(mode='POSE')

def ik2fkArm(rig, ikBones, fkBones, suffix, frame):
    (uparmIk, loarmIk, elbow, elbowPt, wrist) = ikBones
    (uparmFk, loarmFk, elbowPtFk, handFk) = fkBones
    matchPoseTranslation(wrist, handFk, frame)
    matchPoseRotation(wrist, handFk, frame)  
    matchPoseTranslation(elbow, elbowPtFk, frame)
    matchPoseTranslation(elbowPt, elbowPtFk, frame)
    return

def ik2fkLeg(rig, ikBones, fkBones, legIkToAnkle, suffix, frame):
    (uplegIk, lolegIk, kneePt, ankleIk, legIk, legFk) = ikBones
    (uplegFk, lolegFk, kneePtFk, footFk) = fkBones

    if legIkToAnkle:
        matchPoseTranslation(ankleIk, footFk, frame)
    else:
        ankleIk.location = (0,0,0)
        ankleIk.rotation_quaternion = (1,0,0,0)
        #ankleIk.keyframe_insert("location", frame=frame, group=ankleIk.name)
        #ankleIk.keyframe_insert("rotation_quaternion", frame=frame, group=ankleIk.name)
        #setInverse(rig, ankleIk)
    matchPoseTranslation(legIk, legFk, frame)
    matchPoseRotation(legIk, legFk, frame)  
    matchPoseTranslation(kneePt, kneePtFk, frame)
    return
   
def retargetIkBones(rig, frame):
    lArmIkBones = getSnapBones(rig, "ArmIK", "_L")
    lArmFkBones = getSnapBones(rig, "ArmFK", "_L")
    rArmIkBones = getSnapBones(rig, "ArmIK", "_R")
    rArmFkBones = getSnapBones(rig, "ArmFK", "_R")
    lLegIkBones = getSnapBones(rig, "LegIK", "_L")
    lLegFkBones = getSnapBones(rig, "LegFK", "_L")
    rLegIkBones = getSnapBones(rig, "LegIK", "_R")
    rLegFkBones = getSnapBones(rig, "LegFK", "_R")
        
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')
    ik2fkArm(rig, lArmIkBones, lArmFkBones, "_L", frame)
    ik2fkArm(rig, rArmIkBones, rArmFkBones, "_R", frame)
    ik2fkLeg(rig, lLegIkBones, lLegFkBones, rig["&LegIkToAnkle_L"], "_L", frame)
    ik2fkLeg(rig, rLegIkBones, rLegFkBones, rig["&LegIkToAnkle_R"], "_R", frame)
    return        
        
#
#   setInverse(rig, pb):
#

def setInverse(rig, pb):
    rig.data.bones.active = pb.bone
    pb.bone.select = True
    for cns in pb.constraints:
        if cns.type == 'CHILD_OF':
            bpy.ops.constraint.childof_set_inverse(constraint=cns.name, owner='BONE')
    return

def clearInverse(rig, pb):
    rig.data.bones.active = pb.bone
    pb.bone.select = True
    bpy.ops.pose.loc_clear()
    bpy.ops.pose.rot_clear()
    for cns in pb.constraints:
        if cns.type == 'CHILD_OF':
            bpy.ops.constraint.childof_clear_inverse(constraint=cns.name, owner='BONE')
    return

def fixAnkles(rig, scn):
    layers = list(rig.data.layers)
    try:
        rig.data.layers = 32*[True]
        clearInverse(rig, rig.pose.bones["Ankle_L"])
        clearInverse(rig, rig.pose.bones["Ankle_R"])
        scn.frame_current = scn.frame_current
    finally:
        rig.data.layers = layers
    return

class VIEW3D_OT_FixAnklesButton(bpy.types.Operator):
    bl_idname = "mcp.fix_ankles"
    bl_label = "Fix ankles"
    bl_description = "Set inverse for ankle Child-of constraints"

    def execute(self, context):
        fixAnkles(context.object, context.scene)
        return{'FINISHED'}    
#
#
#

SnapBones = {
    "ArmFK" : ["UpArm", "LoArm", "ElbowPTFK", "Hand"],
    "ArmIK" : ["UpArmIK", "LoArmIK", "Elbow", "ElbowPT", "Wrist"],
    "LegFK" : ["UpLeg", "LoLeg", "KneePTFK", "Foot"],
    "LegIK" : ["UpLegIK", "LoLegIK", "KneePT", "Ankle", "LegIK", "LegFK"],
}

def getSnapBones(rig, key, suffix):
    names = SnapBones[key]
    pbones = []
    for name in names:
        pb = rig.pose.bones[name+suffix]
        pbones.append(pb)
    return tuple(pbones)

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
    scn = context.scene
    if scn.McpDoSimplify:
        simplify.simplifyFCurves(context, trgRig, False, False)
    if scn.McpRescale:
        simplify.rescaleFCurves(context, trgRig, scn.McpRescaleFactor)
    load.deleteSourceRig(context, srcRig, 'Y_')
    time2 = time.clock()
    print("%s finished in %.3f s" % (filepath, time2-time1))
    return


########################################################################
#
#   class VIEW3D_OT_NewRetargetMhxButton(bpy.types.Operator):
#

class VIEW3D_OT_NewRetargetMhxButton(bpy.types.Operator):
    bl_idname = "mcp.new_retarget_mhx"
    bl_label = "Retarget selected to active"

    def execute(self, context):
        trgRig = context.object
        target.guessTargetArmature(trgRig, context.scene)
        for srcRig in context.selected_objects:
            if srcRig != trgRig:
                retargetMhxRig(context, srcRig, trgRig)
        return{'FINISHED'}    

#
#   class VIEW3D_OT_NewLoadRetargetSimplify(bpy.types.Operator):
#

class VIEW3D_OT_NewLoadRetargetSimplifyButton(bpy.types.Operator, ImportHelper):
    bl_idname = "mcp.new_load_retarget_simplify"
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

