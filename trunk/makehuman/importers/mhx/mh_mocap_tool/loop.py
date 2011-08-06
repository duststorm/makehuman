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

import bpy
from math import pi
from . import utils, load, simplify, props

#
#   loopFCurves(context, rig):
#

def loopFCurves(context, rig):
    scn = context.scene
    (fcurves, minTime, maxTime) = simplify.getRigFCurves(rig, False, True, scn)
    if not fcurves:
        return
    act = rig.animation_data.action

    hasLocation = {}
    for fcu in fcurves:
        (name, mode) = utils.fCurveIdentity(fcu)
        if mode[0:8] == 'rotation':
            loopFCurve(fcu, minTime, maxTime, scn)
        elif mode[0:8] == 'location':
            hasLocation[name] = True

    if scn['McpLoopInPlace']:
        frames = utils.activeFrames(rig)
        root = utils.getBone('Root', rig)    
        
        for frame in frames:
            scn.frame_set(frame)
            root.keyframe_insert("location", group=root.name)

        for name in hasLocation.keys():
            pb = rig.pose.bones[name]
            if pb != root:
                continue
            restMat = pb.bone.matrix_local
            if pb.parent:
                restMat = utils.invert(pb.parent.bone.matrix_local) * restMat
            restRot = restMat.to_3x3()
            restInv = utils.invert(restRot)
            for frame in frames:
                scn.frame_set(frame)            
                head = pb.head - root.head
                if not scn['McpLoopZInPlace']:
                    head[2] = pb.head[2]
                pb.location = restInv * head
                pb.keyframe_insert("location", group=pb.name)  
                #print(pb.head)

    print("Curves looped")
    return
    
#
#   loopFCurve(fcu, minTime, maxTime, scn):
#

def loopFCurve(fcu, t0, tn, scn):
    delta = scn['McpLoopBlendRange']
    
    v0 = fcu.evaluate(t0)
    vn = fcu.evaluate(tn)
    fcu.keyframe_points.insert(frame=t0, value=v0)
    fcu.keyframe_points.insert(frame=tn, value=vn)
    (mode, upper, lower, diff) = simplify.getFCurveLimits(fcu) 
    if mode == 'location': 
        dv = (vn-v0)/(tn-t0)
    else:
        dv = 0.0
        
    newpoints = []
    for dt in range(delta):
        eps = 0.5*(1-dt/delta)

        t1 = t0+dt
        v1 = fcu.evaluate(t1)
        tm = tn+dt
        vm = fcu.evaluate(tm) - dt*dv
        newpoints.append((t1, eps*v1 + (1-eps)*vm))
        
        t1 = t0-dt
        v1 = fcu.evaluate(t1) + dt*dv
        tm = tn-dt
        vm = fcu.evaluate(tm)
        newpoints.append((tm, eps*vm + (1-eps)*v1))
        
    newpoints.sort()
    for (t,v) in newpoints: 
        fcu.keyframe_points.insert(frame=t, value=v)
    return
    
    
#
#   shiftBoneFCurves(context):
#

def shiftBoneFCurves(context):
    frame = context.scene.frame_current
    rig = context.object
    anim = rig.animation_data
    if not anim:
        return

    orig = {
        0: {},
        1: {},
        2: {},
        3: {},
    }
    touched = {}
    for fcu in anim.action.fcurves:
        (name, mode) = utils.fCurveIdentity(fcu)
        for pb in context.selected_pose_bones:
            if (pb.name == name and 
                mode in ["rotation_euler", "rotation_quaternion", "rotation_axis_angle"]):
                kp = fcu.keyframe_points[frame]
                orig[fcu.array_index][fcu.data_path] = kp.co[1]
                touched[pb.name] = True

    for name in touched.keys():
        pb = rig.pose.bones[name]
        utils.insertRotationKeyFrame(pb, frame)
    
    for fcu in anim.action.fcurves:
        try:
            dy = fcu.evaluate(frame) - orig[fcu.array_index][fcu.data_path]
        except:
            continue     
        (name, mode) = utils.fCurveIdentity(fcu)
        for kp in fcu.keyframe_points:
            if kp.co[0] != frame:
                kp.co[1] += dy
    return        
    
########################################################################
#
#   class VIEW3D_OT_McpLoopFCurvesButton(bpy.types.Operator):
#

class VIEW3D_OT_McpLoopFCurvesButton(bpy.types.Operator):
    bl_idname = "mcp.mocap_loop_fcurves"
    bl_label = "Loop F-curves"

    def execute(self, context):
        loopFCurves(context, context.object)
        return{'FINISHED'}    

#
#   class VIEW3D_OT_McpShiftBoneFCurvesButton(bpy.types.Operator):
#

class VIEW3D_OT_McpShiftBoneFCurvesButton(bpy.types.Operator):
    bl_idname = "mcp.mocap_shift_bone"
    bl_label = "Shift bone F-curves"

    def execute(self, context):
        shiftBoneFCurves(context)
        print("Bones shifted")
        return{'FINISHED'}    

#
#   class LoopPanel(bpy.types.Panel):
#

class LoopPanel(bpy.types.Panel):
    bl_label = "Mocap: Adjust"
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
        layout.prop(scn, "McpLoopBlendRange")
        layout.prop(scn, "McpLoopInPlace")
        if scn['McpLoopInPlace']:
            layout.prop(scn, "McpLoopZInPlace")
        layout.operator("mcp.mocap_loop_fcurves")
        layout.operator("mcp.mocap_shift_bone")
                
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

