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
from math import pi, sqrt
from mathutils import *
from . import utils, load, simplify, props, rig_mhx, action
from . import globvar as the

#
#   normalizeRotCurves(scn, rig, fcurves, frames)
#

        
def normalizeRotCurves(scn, rig, fcurves, frames):        
    hasQuat = {}
    for fcu in fcurves:
        (name, mode) = utils.fCurveIdentity(fcu)
        if mode == 'rotation_quaternion':
            hasQuat[name] = rig.pose.bones[name]

    for frame in frames:
        scn.frame_set(frame)
        for (name, pb) in hasQuat.items():
            pb.rotation_quaternion.normalize()
            pb.keyframe_insert("rotation_quaternion", group=name)  
    return            

#
#   loopFCurves(context):
#   loopFCurve(fcu, minTime, maxTime, scn):
#   class VIEW3D_OT_McpLoopFCurvesButton(bpy.types.Operator):
#

def loopFCurves(context):
    scn = context.scene
    rig = context.object
    act = utils.getAction(rig)
    if not act:
        return
    (fcurves, minTime, maxTime) = simplify.getActionFCurves(act, False, True, scn)
    if not fcurves:
        return

    frames = utils.activeFrames(rig)
    normalizeRotCurves(scn, rig, fcurves, frames)

    hasLocation = {}
    for fcu in fcurves:
        (name, mode) = utils.fCurveIdentity(fcu)
        if utils.isRotation(mode) and scn['McpLoopRot']:
            loopFCurve(fcu, minTime, maxTime, scn)

    if scn['McpLoopLoc']:
        if scn['McpLoopInPlace']:
            for pb in utils.ikBoneList(rig):
                scn.frame_set(minTime)
                head0 = pb.head.copy()
                scn.frame_set(maxTime)
                head1 = pb.head.copy()
                offs = (head1-head0)/(maxTime-minTime)
                if not scn['McpLoopZInPlace']:
                    offs[2] = 0
                print("Loc", pb.name, offs)

                restMat = pb.bone.matrix_local.to_3x3()
                restInv = utils.invert(restMat)
                #if pb.parent:
                #    parRest = pb.parent.bone.matrix_local.to_3x3()
                #    restInv = restInv * parRest

                for frame in frames:
                    scn.frame_set(frame)    
                    head = pb.head.copy() - (frame-minTime)*offs
                    diff = head - pb.bone.head_local
                    #if pb.parent:
                    #    parMat = pb.parent.matrix.to_3x3()                        
                    #    diff = utils.invert(parMat) * diff                        
                    pb.location = restInv * diff                    
                    pb.keyframe_insert("location", group=pb.name)  
                # pb.matrix_basis = utils.invert(pb.bone.matrix_local) * par.bone.matrix_local * utils.invert(par.matrix) * pb.matrix

        for fcu in fcurves:
            (name, mode) = utils.fCurveIdentity(fcu)
            if utils.isLocation(mode):
                loopFCurve(fcu, minTime, maxTime, scn)
    print("F-curves looped")                
    return
    
    
    
def loopFCurve(fcu, t0, tn, scn):
    delta = scn['McpLoopBlendRange']
    
    v0 = fcu.evaluate(t0)
    vn = fcu.evaluate(tn)
    fcu.keyframe_points.insert(frame=t0, value=v0)
    fcu.keyframe_points.insert(frame=tn, value=vn)
    (mode, upper, lower, diff) = simplify.getFCurveLimits(fcu) 
    if mode == 'location': 
        dv = vn-v0        
    else:
        dv = 0.0
        
    newpoints = []
    for dt in range(delta):
        eps = 0.5*(1-dt/delta)

        t1 = t0+dt
        v1 = fcu.evaluate(t1)
        tm = tn+dt
        vm = fcu.evaluate(tm) - dv
        if (v1 > upper) and (vm < lower):
            vm += diff
        elif (v1 < lower) and (vm > upper):
            vm -= diff
        pt1 = (t1, (eps*vm + (1-eps)*v1))
        
        t1 = t0-dt
        v1 = fcu.evaluate(t1) + dv
        tm = tn-dt
        vm = fcu.evaluate(tm)
        if (v1 > upper) and (vm < lower):
            v1 -= diff
        elif (v1 < lower) and (vm > upper):
            v1 += diff
        ptm = (tm, eps*v1 + (1-eps)*vm)
        
        #print("  ", pt1,ptm)
        newpoints.extend([pt1,ptm])
        
    newpoints.sort()
    for (t,v) in newpoints: 
        fcu.keyframe_points.insert(frame=t, value=v)
    return

class VIEW3D_OT_McpLoopFCurvesButton(bpy.types.Operator):
    bl_idname = "mcp.loop_fcurves"
    bl_label = "Loop F-curves"

    def execute(self, context):
        loopFCurves(context)
        return{'FINISHED'}    
    
#    
#   repeatFCurves(context, nRepeats):
#

def repeatFCurves(context, nRepeats):
    act = utils.getAction(context.object)
    if not act:
        return
    (fcurves, minTime, maxTime) = simplify.getActionFCurves(act, False, True, context.scene)
    if not fcurves:
        return
    dt0 = maxTime-minTime
    for fcu in fcurves:
        (name, mode) = utils.fCurveIdentity(fcu)
        dy0 = fcu.evaluate(maxTime) - fcu.evaluate(minTime)
        points = []
        for kp in fcu.keyframe_points:
            t = kp.co[0]
            if t >= minTime and t < maxTime:
                points.append((t, kp.co[1]))
        for n in range(1,nRepeats):
            dt = n*dt0
            dy = n*dy0
            for (t,y) in points:
                fcu.keyframe_points.insert(t+dt, y+dy, options={'FAST'})
    print("F-curves repeated %d times" % nRepeats)
    return
                
class VIEW3D_OT_McpRepeatFCurvesButton(bpy.types.Operator):
    bl_idname = "mcp.repeat_fcurves"
    bl_label = "Repeat F-curves"

    def execute(self, context):
        repeatFCurves(context, context.scene["McpRepeatNumber"])
        return{'FINISHED'}    
    

#
#   stitchActions(context):
#

def stitchActions(context):
    action.listAllActions(context)
    scn = context.scene
    rig = context.object
    act1 = action.selectedAction(scn['McpFirstAction'])
    if not act1: return
    act2 = action.selectedAction(context.scene['McpSecondAction'])
    if not act2: return
    frame1 = scn['McpFirstEndFrame']
    frame2 = scn['McpSecondStartFrame'] 
    delta = scn['McpLoopBlendRange']

    if not rig.animation_data:
        pb = context.active_posebone
        pb.keyframe_insert("location", group=pb.name)
        rig.animation_data.action = None
        
    actionTarget = scn["McpActionTarget"]
    print("Acttar", actionTarget)
    if actionTarget == 0:   # Second to new
        act = None
    elif actionTarget == 1:   # Extend second
        act = act2
    elif actionTarget == 2:   # Stitch new
        act = None        
    if not act:
        act = utils.copyAction(act2, "#TmpAct")

    matrix = {}
    matrix1 = {}
    matrix2 = {}
    rig.animation_data.action = act1
    scn.frame_set(frame1)
    for pb in context.selected_pose_bones:
        matrix1[pb.name] = utils.invert(pb.bone.matrix_local) * pb.matrix
    rig.animation_data.action = act2
    scn.frame_set(frame2)
    for pb in context.selected_pose_bones:
        matrix2[pb.name] = utils.invert(pb.bone.matrix_local) * pb.matrix
        matrix[pb.name] = matrix1[pb.name] * utils.invert(matrix2[pb.name])
        #print(pb.name, scn.frame_current)        
        #print(pb.matrix)
        #print(matrix1[pb.name])
        #print(matrix2[pb.name])
        #print(matrix[pb.name])

    #act = bpy.data.actions.new(name=act1.name)
    #rig.animation_data.action = act
    frames = utils.activeFrames(rig)
    for frame in frames:
        scn.frame_set(frame)
        for pb in context.selected_pose_bones:
            if pb.rotation_mode == 'QUATERNION':
                mode = 'rotation_quaternion'
            else:
                mode = 'rotation_euler'
            pb.matrix_basis = matrix[pb.name] * pb.matrix_basis
            pb.keyframe_insert("location", frame=frame, group=pb.name)
            pb.keyframe_insert(mode, frame=frame, group=pb.name)
        
    if act:
        name = act2.name
        act2.name = scn["McpOutputActionName"]
        act.name = name
        act = None

    if actionTarget == 0:   # Second to new
        translateFCurves(act2.fcurves, delta - frame2)
        utils.setInterpolation(rig)
    elif actionTarget == 1:   # Extend second
        return
    elif actionTarget == 2:   # Stitch new
        shift = frame1 - frame2 + 2*delta
        translateFCurves(act2.fcurves, shift)
        for fcu2 in act2.fcurves:
            fcu1 = utils.findFCurve(fcu2.data_path, fcu2.array_index, act1.fcurves)
            for kp1 in fcu1.keyframe_points:
                t = kp1.co[0]
                y1 = kp1.co[1]
                if t <= frame1 - delta:
                    y = y1
                elif t <= frame1 + delta:
                    y2 = fcu2.evaluate(t+shift)
                    eps = (t - frame1 + delta)/(2*delta)
                    y = y1*(1-eps) + y2*eps
                else:
                    break
                fcu2.keyframe_points.insert(t, y, options={'FAST'})
            for kp2 in fcu2.keyframe_points:
                t = kp2.co[0] - shift
                if t >= frame1 + delta:
                    fcu2.keyframe_points.insert(t, kp2.co[1], options={'FAST'})
        utils.setInterpolation(rig)
    return        

def translateFCurves(fcurves, dt):
    for fcu in fcurves:
        if dt > 0:
            kpts = list(fcu.keyframe_points)
            kpts.reverse()
            for kp in kpts:
                kp.co[0] += dt
        elif dt < 0:                
            for kp in fcu.keyframe_points:
                kp.co[0] += dt
    return
    
class VIEW3D_OT_McpStitchActionsButton(bpy.types.Operator):
    bl_idname = "mcp.stitch_actions"
    bl_label = "Stitch actions"

    def execute(self, context):
        stitchActions(context)
        return{'FINISHED'}    
    
    
#
#   shiftBoneFCurves(context):
#   class VIEW3D_OT_McpShiftBoneFCurvesButton(bpy.types.Operator):
#

def shiftBoneFCurves(context):
    frame = context.scene.frame_current
    rig = context.object
    act = utils.getAction(rig)
    if not act:
        return
    (origLoc, origRot, touchedLoc, touchedRot) = setupOrigAndTouched(context, act, frame)
    touchBones(rig, frame, touchedLoc, touchedRot)    
    for fcu in act.fcurves:
        (name, mode) = utils.fCurveIdentity(fcu)
        try:
            if utils.isRotation(mode):
                dy = fcu.evaluate(frame) - origRot[fcu.array_index][fcu.data_path]
            elif  utils.isLocation(mode):
                dy = fcu.evaluate(frame) - origLoc[fcu.array_index][fcu.data_path]
        except:
            continue     
        for kp in fcu.keyframe_points:
            if kp.co[0] != frame:
                kp.co[1] += dy
    return
    
def setupOrigAndTouched(context, act, frame):
    origLoc = utils.quadDict()
    origRot = utils.quadDict()
    touchedLoc = {}
    touchedRot = {}
    for fcu in act.fcurves:
        (name, mode) = utils.fCurveIdentity(fcu)
        for pb in context.selected_pose_bones:
            if pb.name == name:
                #kp = fcu.keyframe_points[frame]
                y = fcu.evaluate(frame)
                if utils.isRotation(mode):
                    origRot[fcu.array_index][fcu.data_path] = y
                    touchedRot[pb.name] = True
                elif utils.isLocation(mode):
                    origLoc[fcu.array_index][fcu.data_path] = y
                    touchedLoc[pb.name] = True
    return (origLoc, origRot, touchedLoc, touchedRot)                    

def touchBones(rig, frame, touchedLoc, touchedRot):
    for name in touchedRot.keys():
        pb = rig.pose.bones[name]
        utils.insertRotationKeyFrame(pb, frame)
    for name in touchedLoc.keys():
        pb = rig.pose.bones[name]
        pb.keyframe_insert("location", frame=frame, group=pb.name)
    return        

class VIEW3D_OT_McpShiftBoneFCurvesButton(bpy.types.Operator):
    bl_idname = "mcp.shift_bone"
    bl_label = "Shift bone F-curves"

    def execute(self, context):
        shiftBoneFCurves(context)
        print("Bones shifted")
        return{'FINISHED'}    
        
########################################################################
#
#   class LoopStitchPanel(bpy.types.Panel):
#

class LoopStitchPanel(bpy.types.Panel):
    bl_label = "Mocap: Loop and stitch"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        if context.object and context.object.type == 'ARMATURE':
            return True

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        ob = context.object
        layout.label("Loop animation")
        layout.prop(scn, "McpLoopBlendRange")
        row = layout.row()
        row.prop(scn, "McpLoopLoc")
        row.prop(scn, "McpLoopRot")
        layout.prop(scn, "McpLoopInPlace")
        if scn['McpLoopInPlace']:
            layout.prop(scn, "McpLoopZInPlace")
        layout.operator("mcp.loop_fcurves")

        layout.label("Repeat animation")
        layout.prop(scn, "McpRepeatNumber")
        layout.operator("mcp.repeat_fcurves")

        layout.label("Stitch")        
        layout.operator("mcp.update_action_list")
        layout.prop(scn, "McpFirstAction")
        row = layout.row()
        row.prop(scn, "McpFirstEndFrame")
        row.operator("mcp.set_current_action").prop = "McpFirstAction"

        layout.prop(scn, "McpSecondAction")
        row = layout.row()
        row.prop(scn, "McpSecondStartFrame")
        row.operator("mcp.set_current_action").prop = "McpSecondAction"
        
        layout.prop(scn, "McpActionTarget")
        layout.prop(scn, "McpOutputActionName")
        
        layout.operator("mcp.stitch_actions")

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

