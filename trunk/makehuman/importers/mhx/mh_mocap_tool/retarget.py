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

from . import props, source, target, rig_mhx, toggle, load, simplify
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

    if isTarget and the.target == target.T_Custom:
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
    anim.inverseRest = anim.matrixRest.copy()
    anim.inverseRest.invert()
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
    return vecDict
                
#
#    insertAnimation(context, rig, animations, boneList):
#    insertAnimRoot(root, animations, nFrames, locs, rots):
#    insertAnimChild(name, animations, nFrames, rots):
#

def insertAnimation(context, rig, animations, boneList):
    context.scene.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')
    locs = makeVectorDict(rig, ['].location'])
    rots = makeVectorDict(rig, ['].rotation_quaternion', '].rotation_euler'])
    try:
        root = 'Root'
        nFrames = len(locs[root])
    except:
        root = target.getTrgBone('Root')
        nFrames = len(locs[root])
    insertAnimRoot(root, animations, nFrames, locs[root], rots[root])
    bones = rig.data.bones
    for nameSrc in boneList:
        try:
            bones[nameSrc]
            success = (nameSrc != root)
        except:
            success = False
        if success:
            try:
                rot = rots[nameSrc]
            except:
                rot = None
            insertAnimChild(nameSrc, animations, nFrames, rot)

def insertAnimRoot(root, animations, nFrames, locs, rots):
    anim = animations[root]
    if nFrames < 0:
        nFrames = len(locs)
    anim.nFrames = nFrames
    for frame in range(anim.nFrames):
        quat = Quaternion(rots[frame])
        anim.quats[frame] = quat
        matrix = anim.matrixRest * quat.to_matrix() * anim.inverseRest
        anim.matrices[frame] = matrix
        anim.heads[frame] =  Vector(locs[frame]) * anim.matrixRest + anim.headRest
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

def insertAnimChild(name, animations, nFrames, rots):
    try:
        anim = animations[name]
    except:
        return None
    if nFrames < 0:
        nFrames = len(rots)
    par = anim.parent
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
            try:
                quat = Quaternion(rots[frame])
            except:
                quat = Euler(rots[frame]).to_quaternion()
        anim.quats[frame] = quat
        locmat = anim.matrixRest * quat.to_matrix() * anim.inverseRest
        parmat = animPar.matrices[frame]
        matrix = parmat * locmat
        anim.matrices[frame] = matrix
        anim.heads[frame] = animPar.heads[frame] + anim.offsetRest*parmat
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
            print("Fail", nameSrc, nameTrg)
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
    load.setInterpolation(trgRig)
    return

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
        loc = loc0 * animTrg.inverseRest
        locs.append(loc)
        pb.location = loc
        for n in range(3):
            pb.keyframe_insert('location', index=n, frame=frame, group=name)    
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
            loc0 = animPar.heads[frame] + animIK.offsetRest*animPar.matrices[frame]
            offset = anim.heads[frame] - loc0
            mat = animPar.matrices[frame] * animIK.matrixRest
            loc = offset*mat.invert()
        else:
            offset = anim.heads[frame] - animIK.headRest
            loc = offset * animIK.inverseRest
        pb.location = loc
        for n in range(3):
            pb.keyframe_insert('location', index=n, frame=frame, group=nameIK)    
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
        load.setRotation(pb, rot, frame, name)
    return rots

def insertLocalRotationKeyFrames(name, pb, animSrc, animTrg, trgRoll):
    animTrg.nFrames = animSrc.nFrames
    for frame in range(animSrc.nFrames):
        rot = animSrc.quats[frame]
        rollRot(rot, trgRoll)
        animTrg.quats[frame] = rot
        load.setRotation(pb, rot, frame, name)
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
        load.setRotation(pb, rot, frame, name)
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

#
#    poseTrgIkBones(context, trgRig, trgAnimations)
#

def poseTrgIkBones(context, trgRig, trgAnimations):
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
        locAbs = animFake.heads[frame] + offsetFake*animFake.matrices[frame]
        headAbs = animReal.heads[frame] + offsetReal*animReal.matrices[frame]
        #debugPrintVecVec(locAbs, headAbs)
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
        for n in range(3):
            pb.keyframe_insert('location', index=n, frame=frame, group=name)    

        if animCopy:
            mat = mat * animCopy.inverseRest * animCopy.matrices[frame]
        anim.matrices[frame] = mat
        matMhx = anim.inverseRest * mat * anim.matrixRest
        rot = matMhx.to_quaternion()
        #rollRot(rot, roll)
        load.setRotation(pb, rot, frame, name)
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
        locAbs = animCopy.heads[frame] + offsetCopy*animCopy.matrices[frame]
        headAbs = animReal.heads[frame] + offsetReal*animReal.matrices[frame]
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
        for n in range(3):
            pb.keyframe_insert('location', index=n, frame=frame, group=name)    

        mat = mat * animCopy.inverseRest * animCopy.matrices[frame]
        anim.matrices[frame] = mat
        matMhx = rotX * anim.inverseRest * mat * anim.matrixRest * rotX
        rot = matMhx.to_quaternion()
        load.setRotation(pb, rot, frame, name)
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
        locAbs = animFake.heads[frame] + offsetFake*animFake.matrices[frame]
        offset = locAbs - anim.headRest
        if pb.bone.use_local_location:
            loc = offset * anim.inverseRest
            pb.location = loc
        else:
            pb.location = offset
        anim.heads[frame] = locAbs
        for n in range(3):
            pb.keyframe_insert('location', index=n, frame=frame, group=name)    

        mat = anim.matrixRest
        if animCopy:
            mat = mat * animCopy.inverseRest * animCopy.matrices[frame] 
        anim.matrices[frame] = mat
        matMhx = anim.inverseRest * mat * anim.matrixRest
        rot = matMhx.to_quaternion()
        #rollRot(rot, roll)
        load.setRotation(pb, rot, frame, name)
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
    if scn['MhxApplyFixes']:
        srcFixes = the.fixesList[srcRig['MhxArmature']]
    else:
        srcFixes = None
    #debugOpen()
    poseTrgFkBones(context, trgRig, srcAnimations, trgAnimations, srcFixes)
    poseTrgIkBones(context, trgRig, trgAnimations)
    #debugClose()
    load.setInterpolation(trgRig)
    if onoff == 'OFF':
        toggle.setLimitConstraints(trgRig, 1.0)
    else:
        toggle.setLimitConstraints(trgRig, 0.0)

    trgRig.animation_data.action.name = trgRig.name[:4] + srcRig.name[2:]
    print("Retargeted %s --> %s" % (srcRig, trgRig))
    return

#
#    deleteRig(context, rig00, action, prefix):
#

def deleteRig(context, rig00, action, prefix):
    context.scene.objects.unlink(rig00)
    if rig00.users == 0:
        bpy.data.objects.remove(rig00)
        #del rig00
    if bpy.data.actions:
        for act in bpy.data.actions:
            if act.name[0:2] == prefix:
                act.use_fake_user = False
                if act.users == 0:
                    bpy.data.actions.remove(act)
                    del act
    return

#
#    importAndRename(context, filepath):
#

def importAndRename(context, filepath):
    trgRig = context.object
    rig = load.readBvhFile(context, filepath, context.scene, False)
    (srcRig, srcBones, action) =  load.renameBvhRig(rig, filepath)
    source.findSrcArmature(context, srcRig)
    load.renameBones(srcBones, srcRig, action)
    load.setInterpolation(srcRig)
    load.rescaleRig(context.scene, trgRig, srcRig, action)
    return (srcRig, action)

#
#    loadRetargetSimplify(context, filepath):
#

def loadRetargetSimplify(context, filepath):
    print("Load and retarget %s" % filepath)
    time1 = time.clock()
    trgRig = context.object
    (srcRig, action) = importAndRename(context, filepath)
    retargetMhxRig(context, srcRig, trgRig)
    if context.scene['MhxDoSimplify']:
        simplify.simplifyFCurves(context, trgRig, False, False)
    deleteRig(context, srcRig, action, 'Y_')
    time2 = time.clock()
    print("%s finished in %.3f s" % (filepath, time2-time1))
    return


########################################################################
#
#   class VIEW3D_OT_MhxLoadBvhButton(bpy.types.Operator, ImportHelper):
#

class VIEW3D_OT_MhxLoadBvhButton(bpy.types.Operator, ImportHelper):
    bl_idname = "mhx.mocap_load_bvh"
    bl_label = "Load BVH file (.bvh)"

    filename_ext = ".bvh"
    filter_glob = StringProperty(default="*.bvh", options={'HIDDEN'})
    filepath = StringProperty(name="File Path", description="Filepath used for importing the BVH file", maxlen=1024, default="")

    def execute(self, context):
        importAndRename(context, self.properties.filepath)
        print("%s imported" % self.properties.filepath)
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    


#
#   class VIEW3D_OT_MhxRetargetMhxButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxRetargetMhxButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_retarget_mhx"
    bl_label = "Retarget selected to MHX"

    def execute(self, context):
        trgRig = context.object
        target.guessTargetArmature(trgRig)
        for srcRig in context.selected_objects:
            if srcRig != trgRig:
                retargetMhxRig(context, srcRig, trgRig)
        return{'FINISHED'}    

#
#   class VIEW3D_OT_MhxLoadRetargetSimplify(bpy.types.Operator):
#

class VIEW3D_OT_MhxLoadRetargetSimplifyButton(bpy.types.Operator, ImportHelper):
    bl_idname = "mhx.mocap_load_retarget_simplify"
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

#
#   class RetargetPanel(bpy.types.Panel):
#

class RetargetPanel(bpy.types.Panel):
    bl_label = "Retarget BVH"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        if context.object and context.object.type == 'ARMATURE':
            return True

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        ob = context.object
        layout.operator("mhx.mocap_load_bvh")
        layout.operator("mhx.mocap_retarget_mhx")
        layout.operator("mhx.mocap_load_retarget_simplify")
        layout.separator()
        layout.prop(scn, "MhxBvhScale")
        layout.prop(scn, "MhxAutoScale")
        layout.prop(scn, "MhxStartFrame")
        layout.prop(scn, "MhxEndFrame")
        layout.prop(scn, "MhxSubsample")
        layout.prop(scn, "MhxDefaultSS")
        layout.prop(scn, "MhxRot90Anim")
        layout.prop(scn, "MhxDoSimplify")
        layout.prop(scn, "MhxApplyFixes")

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()


