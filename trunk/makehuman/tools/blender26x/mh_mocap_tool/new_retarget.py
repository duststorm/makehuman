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
        self.firstFrame = 0
        self.lastFrame = 100
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
#   retargetBone(boneData, frame):
#

def retargetBone(boneData, frame):
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
    return        
   
def collectSrcMats(anim, frames, scn):
    objects = []
    for ob in scn.objects:
        if ob != anim.srcRig:
            objects.append((ob, list(ob.layers)))
            ob.layers = 20*[False]
    try:            
        for frame in frames:
            scn.frame_set(frame)
            if frame % 100 == 0:
                print("Collect", frame)
            for boneData in anim.boneDataList:
                mat = CMatrixGroup(boneData.srcPoseBone.matrix, frame)
                boneData.matrices[frame] = mat
    finally:
        for (ob,layers) in objects:
            ob.layers = layers
    return                

def retargetMats(anim, frames):
    for frame in frames:
        if frame % 100 == 0:
            print("Retarget", frame)
        for boneData in anim.boneDataList:
            retargetBone(boneData, frame)
    return                
 
  
#
#    setupFkBones(srcRig, trgRig, boneAssoc):
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
    oldProps = mhxPropertiesReset(trgRig)

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
    
    oldData = changeTargetData(trgRig)
    frameBlock = frames[0:100]
    index = 0
    try:
        while frameBlock:
            collectSrcMats(anim, frameBlock, scn)
            retargetMats(anim, frameBlock)
            index += 100
            frameBlock = frames[index:index+100]
    finally:                
        restoreTargetData(trgRig, oldData)
            
    utils.setInterpolation(trgRig)
    act = trgRig.animation_data.action
    act.name = trgRig.name[:4] + srcRig.name[2:]
    act.use_fake_user = True
    print("Retargeted %s --> %s" % (srcRig, trgRig))
    return

def changeTargetData(rig):    
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
    return (layers, locks)
    
def restoreTargetData(rig, data):
    (rig.data.layers, locks) = data
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
        
    

#
#   mhxPropertiesReset(rig):
#

def mhxPropertiesReset(rig):
    mhxProps = [
        ("&RotationLimits", 0.0),
        ("&ArmIk_L", 0.0),
        ("&ArmIk_R", 0.0),
        ("&LegIk_L", 0.0),
        ("&LegIk_R", 0.0),
        ("&SpineIk", 0.0),
        ("&SpineInvert", 0.0),
        ("&ElbowPlant_L", 0.0),
        ("&ElbowPlant_R", 0.0),
        ]
    oldProps = []
    for (key, value) in mhxProps:
        try:
            oldProps.append((key, rig[key]))
            rig[key] = value
        except KeyError:
            pass
    return oldProps        

#
#   poseTrgIkBones(context, trgRig, nFrames):
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
    
def poseTrgIkBones(context, rig, nFrames):
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


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()


