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

from . import props, source, target, rig_mhx, toggle, load, simplify
from . import globvar as the

#
#   activeFrames(ob):
#

def activeFrames(ob):
    active = {}
    act = ob.animation_data.action
    if not act:
        return []
    for fcu in act.fcurves:
        for kp in fcu.keyframe_points:
            active[kp.co[0]] = True
    frames = list(active.keys())
    frames.sort()
    return frames
    
#
#   invert(mat):
#

def invert(mat):
    inv = mat.copy()
    inv.invert()
    return inv

#
#   getBone(name, rig):        
#

def getBone(name, rig):        
    if name:
        return rig.pose.bones[name]
    else:
        return None    
    
#
#   retargetBone(srcBone, trgBone, srcParent, trgParent, srcRig, trgRig):
#

def retargetBone(srcBone, trgBone, srcParent, trgParent, srcRig, trgRig):
    if srcBone:
        srcRot = srcBone.matrix * srcRig.matrix_world
        bakeMat = srcBone.matrix
    else:
        srcRot = Matrix.Rotation(0, 4, 'X')
        bakeMat = Matrix.Rotation(0, 4, 'X')
        #print(srcRot)
        
    restMat = trgBone.bone.matrix_local 
    if trgParent:
        parMatInv = invert(srcParent.matrix)
        bakeMat = parMatInv * bakeMat
        parRestInv = invert(trgParent.bone.matrix_local)
        restMat = parRestInv * restMat   
    restMatInv = invert(restMat)
    trgBone.matrix_basis = restMatInv * bakeMat      

    rotMode = trgBone.rotation_mode
    grp = trgBone.name
    if rotMode == "QUATERNION":
        trgBone.keyframe_insert("rotation_quaternion", group=grp)
    elif rotMode == "AXIS_ANGLE":
        trgBone.keyframe_insert("rotation_axis_angle", group=grp)
    else:
        trgBone.keyframe_insert("rotation_euler", group=grp)

    if not trgParent:
        trgBone.keyframe_insert("location", group=grp)
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

    frames = activeFrames(srcRig)
    (boneAssoc, ikBoneAssoc, parAssoc, rolls, mats, ikBones, ikParents) = target.makeTargetAssoc(trgRig)
    print("IK")
    print(ikBones)
    print("IKPAR")
    print(ikParents)
    print("PAR")
    print(parAssoc)

    fkAssoc = []
    for (trgName, name) in boneAssoc:
        try:
            trgBone = trgRig.pose.bones[trgName]
            srcBone = srcRig.pose.bones[name]
        except:
            print("  -", trgName, name)
            continue
        if trgBone.bone.use_inherit_rotation:
            parName = parAssoc[trgName]
            while True:
                if not parName:
                    trgParent = None
                    srcParent = None
                    break
                trgParent = getBone(parName, trgRig)
                srcParName = target.assocValue(parName, boneAssoc)
                try:
                    srcParent = srcRig.pose.bones[srcParName]
                    break
                except:
                    parName = parAssoc[parName]
            print("BP", trgName, parName)
        fkAssoc.append( (srcBone, trgBone, srcParent, trgParent) )

    ikAssoc = []
    for trgName in ikBones:
        try:
            trgBone = trgRig.pose.bones[trgName]
        except:
            print("  -", trgName)
            continue
        (par, fakePar, fkName, reverse) = ikParents[trgName]        
        if True or trgBone.bone.use_inherit_rotation:
            parName = parAssoc[trgName]
            while True:
                if not parName:
                    trgParent = None
                    fkParent = None
                    break
                trgParent = getBone(parName, trgRig)
                try:
                    fkParent = trgRig.pose.bones[fakePar]
                    break
                except:
                    parName = parAssoc[parName]
            
        if fkName:
            fkBone = trgRig.pose.bones[fkName]
        else:
            fkBone = None
            print(trgName, parName)
        ikAssoc.append( (fkBone, trgBone, fkParent, trgParent) )    

    scn.objects.active = trgRig
    scn.update()
    bpy.ops.object.mode_set(mode='POSE')        
    
    constraints = []
    for (srcBone, trgBone, srcParent, trgParent) in fkAssoc:
        for cns in trgBone.constraints:
            #print(cns.type)
            if cns.type in ['IK', 'LIMIT_ROTATION', 'LIMIT_SCALE', 'LIMIT_LOCATION']:
               constraints.append((cns, cns.influence))
               cns.influence = 0.0

    for frame in frames:            
        scn.frame_set(frame)
        print("Frame", frame)
        for (srcBone, trgBone, srcParent, trgParent) in fkAssoc:
            #print("  ", srcBone.name, trgBone.name, srcParent, trgParent)
            retargetBone(srcBone, trgBone, srcParent, trgParent, srcRig, trgRig)
        for (fkBone, trgBone, fkParent, trgParent) in ikAssoc:            
            pass
            #print(" *", fkBone, trgBone, fkParent, trgParent)
            #retargetBone(fkBone, trgBone, fkParent, trgParent, trgRig, trgRig)
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

            
    for (cns, inf) in constraints:
        #print(cns.type)
        cns.influence = 0.0

    load.setInterpolation(trgRig)
    trgRig.animation_data.action.name = trgRig.name[:4] + srcRig.name[2:]
    print("Retargeted %s --> %s" % (srcRig, trgRig))
    return
    

#
#    deleteRig(context, rig, action, prefix):
#

def deleteRig(context, rig, action, prefix):
    ob = context.object
    scn = context.scene
    scn.objects.active = rig
    bpy.ops.object.mode_set(mode='OBJECT')
    scn.objects.active = ob    
    scn.objects.unlink(rig)
    if rig.users == 0:
        bpy.data.objects.remove(rig)
    if bpy.data.actions:
        for act in bpy.data.actions:
            if act.name[0:2] == prefix:
                act.use_fake_user = False
                if act.users == 0:
                    bpy.data.actions.remove(act)
                    del act
    return

#
#    loadRetargetSimplify(context, filepath):
#

def loadRetargetSimplify(context, filepath):
    print("Load and retarget %s" % filepath)
    time1 = time.clock()
    scn = context.scene
    trgRig = context.object
    rig = load.readBvhFile(context, filepath, scn, False)
    (srcRig, action) = load.renameBvh(context, rig, trgRig)
    retargetMhxRig(context, srcRig, trgRig)
    scn = context.scene
    if scn['McpDoSimplify']:
        simplify.simplifyFCurves(context, trgRig, False, False)
    if scn['McpRescale']:
        simplify.rescaleFCurves(context, trgRig, scn.McpRescaleFactor)
    deleteRig(context, srcRig, action, 'Y_')
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
        target.guessTargetArmature(trgRig)
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
        layout.operator("mcp.load_bvh")
        layout.operator("mcp.rename_bvh")
        layout.operator("mcp.new_retarget_mhx")
        layout.operator("mcp.new_load_retarget_simplify")
        layout.separator()
        layout.prop(scn, "McpBvhScale")
        layout.prop(scn, "McpAutoScale")
        layout.prop(scn, "McpStartFrame")
        layout.prop(scn, "McpEndFrame")
        layout.prop(scn, "McpRot90Anim")
        layout.prop(scn, "McpDoSimplify")
        layout.prop(scn, "McpApplyFixes")

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()


