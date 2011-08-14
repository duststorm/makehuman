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
    def __init__(self, pb, rig):
        self.rig = rig
        self.posebone = pb
        self.parent = None
        self.rest_mat = None
        self.rest_inv = None
        self.offset = None
        self.roll = None
        return
        
#
#   getLitBoneOrNone(name, rig):        
#

def getLitBoneOrNone(name, rig):        
    if name:
        return rig.pose.bones[name]
    else:
        return None    
        
#
#   retargetBone(srcData, trgData, frame):
#

def retargetBone(srcData, trgData, frame):
    srcBone = srcData.posebone
    trgBone = trgData.posebone
    trgParent = trgData.parent
    if srcBone:
        srcRot = srcBone.matrix  # * srcData.rig.matrix_world
        bakeMat = srcBone.matrix
    else:
        srcRot = Matrix.Rotation(0, 4, 'X')
        bakeMat = Matrix.Rotation(0, 4, 'X')
        #print(srcRot)

    if trgParent:
        parMatInv = utils.invert(srcData.parent.posebone.matrix)
        bakeMat = parMatInv * bakeMat
    trgBone.matrix_basis = trgData.rest_inv * bakeMat
    
    if trgParent:    
        trgBone.location = trgData.offset

    load.insertRotationKeyFrame(trgBone, frame)
    if not trgParent:
        trgBone.keyframe_insert("location", group=grp)
    return        
    
#
#    retargetMhxRig(context, srcRig, trgRig):
#
    
def retargetMhxRig(context, srcRig, trgRig):
    scn = context.scene
    source.setArmature(srcRig)
    fixes = the.fixesList[srcRig['McpArmature']]
    print("Retarget %s --> %s" % (srcRig, trgRig))
    if trgRig.animation_data:
        trgRig.animation_data.action = None

    frames = utils.activeFrames(srcRig)
    (boneAssoc, ikBoneAssoc, parAssoc, rolls, mats, ikBones, ikParents) = target.makeTargetAssoc(trgRig, scn)
    
    fkAssoc = []
    trgDatas = {}
    srcDatas = {}
    for (trgName, name) in boneAssoc:
        try:
            trgBone = trgRig.pose.bones[trgName]
            srcBone = srcRig.pose.bones[name]
        except:
            print("  -", trgName, name)
            continue
        trgData = CBoneData(trgBone, trgRig)
        srcData = CBoneData(srcBone, srcRig)
        trgDatas[trgName] = trgData
        srcDatas[name] = srcData
        
        trgData.rest_mat = trgBone.bone.matrix_local
        try:
            (mat, srcRoll) = fixes[name]
        except:
            srcRoll = 0
        trgRoll = rolls[trgName]
        trgData.roll = Matrix.Rotation(srcRoll-trgRoll, 4, 'Y')
        parName = None
        trgParent = None
        if trgBone.parent:  #trgBone.bone.use_inherit_rotation:
            parName = parAssoc[trgName]
            while True:
                if not parName:                 
                    break
                trgParent = getLitBoneOrNone(parName, trgRig)
                srcParName = target.assocValue(parName, boneAssoc)
                try:
                    srcParent = srcRig.pose.bones[srcParName]
                    srcData.parent = srcDatas[srcParent.name]
                    break
                except:
                    parName = parAssoc[parName]

            if trgParent:
                trgData.parent = trgDatas[trgParent.name]
                trgData.offset = trgBone.bone.head_local - trgParent.bone.tail_local
                parRestInv = utils.invert(trgParent.bone.matrix_local)
                parRollInv = utils.invert(trgData.parent.roll)
                trgData.rest_mat = parRestInv * trgData.rest_mat

        trgData.rest_inv = utils.invert(trgData.rest_mat)            
        print("BP", trgName, parName)        
        print("rest", trgData.rest_mat)
        print("roll", trgData.roll)
        fkAssoc.append( (srcData, trgData) )

    ikAssoc = []
    """
    for trgName in ikBones:
        try:
            trgData = CBoneData(trgRig.pose.bones[trgName], trgRig)
        except:
            print("  -", trgName)
            continue
        (par, fakePar, fkName, reverse) = ikParents[trgName]        
        if fkName:
            fkBone = trgRig.pose.bones[fkName]
        else:
            fkBone = None
        fkData = CBoneData(fkBone, trgRig)
        if True or trgBone.bone.use_inherit_rotation:
            parName = parAssoc[trgName]
            while True:
                if not parName:
                    break
                trgParent = getLitBoneOrNone(parName, trgRig)
                trgData.parent = trgParent
                try:
                    fkData.parent = trgRig.pose.bones[fakePar]
                    break
                except:
                    parName = parAssoc[parName]
            
        ikAssoc.append( (fkData, trgData) )    
    """
    
    scn.objects.active = trgRig
    scn.update()
    bpy.ops.object.mode_set(mode='POSE')        
    
    constraints = []
    for (srcData, trgData) in fkAssoc:
        for cns in trgBone.constraints:
            #print(cns.type)
            if cns.type in ['IK', 'LIMIT_ROTATION', 'LIMIT_SCALE', 'LIMIT_LOCATION']:
               constraints.append((cns, cns.influence))
               cns.influence = 0.0

    for frame in frames:            
        scn.frame_set(frame)
        if frame % 10 == 0:
            print("Frame", frame)
        for (srcData, trgData) in fkAssoc:
            #print("  ", srcBone.name, trgBone.name, srcParent, trgParent)
            retargetBone(srcData, trgData, frame)
        for (srcData, trgData) in ikAssoc:            
            pass
            #print(" *", fkBone, trgBone, fkParent, trgParent)
            #retargetBone(srcData, trgData, frame)
            #trgBone.keyframe_insert("location", group=trgBone.name)
            """
            print(trgBone.name)
            print("  FK", fkBone.head)
            print("  rs", trgBone.bone.matrix_local.to_translation())
            print("  L1", trgBone.location)
            #trgBone.location = fkBone.head - trgBone.bone.matrix_local.to_translation()
            trgBone.keyframe_insert("location", group=trgBone.name)
            print("  L2", trgBone.location)
            print("  hd", trgBone.head)
            print("")
            """
        #x = foo            
            
    for (cns, inf) in constraints:
        #print(cns.type)
        cns.influence = 0.0

    utils.setInterpolation(trgRig)
    act = trgRig.animation_data.action
    act.name = trgRig.name[:4] + srcRig.name[2:]
    act.use_fake_user = True
    print("Retargeted %s --> %s" % (srcRig, trgRig))
    return
    

#
#    loadRetargetSimplify(context, filepath):
#

def loadRetargetSimplify(context, filepath):
    print("Load and retarget %s" % filepath)
    time1 = time.clock()
    scn = context.scene
    trgRig = context.object
    srcRig = load.readBvhFile(context, filepath, scn, False)
    print("T", trgRig, "S", srcRig)
    load.renameAndRescaleBvh(context, srcRig, trgRig)
    retargetMhxRig(context, srcRig, trgRig)
    scn = context.scene
    if scn['McpDoSimplify']:
        simplify.simplifyFCurves(context, trgRig, False, False)
    if scn['McpRescale']:
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
    bl_label = "Retarget selected to MHX"

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

#
#   class NewRetargetPanel(bpy.types.Panel):
#

class NewRetargetPanel(bpy.types.Panel):
    bl_label = "Mocap: New retarget"
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
        layout.prop(scn, "McpDoSimplify")
        layout.prop(scn, "McpApplyFixes")
        layout.operator("mcp.new_retarget_mhx")
        layout.operator("mcp.new_load_retarget_simplify")

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()


