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
from . import globvar as the

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

    hasLocation = {}
    for fcu in fcurves:
        (name, mode) = utils.fCurveIdentity(fcu)
        if utils.isRotation(mode):
            loopFCurve(fcu, minTime, maxTime, scn)
        elif utils.isLocation(mode):
            hasLocation[name] = True

    if scn['McpLoopInPlace']:
        frames = utils.activeFrames(rig)
        root = utils.getBone('Root', rig)    
        
        for frame in frames:
            scn.frame_set(frame)
            root.keyframe_insert("location", group=root.name)

        for name in hasLocation.keys():
            pb = rig.pose.bones[name]
            print(pb, root)
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
            for fcu in fcurves:
                (name, mode) = utils.fCurveIdentity(fcu)
                if (utils.isLocation(mode) and
                    (fcu.array_index != 2 or scn['McpLoopZInPlace'])):
                    loopFCurve(fcu, minTime, maxTime, scn)

    print("Curves looped")
    return
    
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
#   quadDict():
#

def quadDict():
    return {
        0: {},
        1: {},
        2: {},
        3: {},
    }
    
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

    origLoc = quadDict()
    origRot = quadDict()
    touchedLoc = {}
    touchedRot = {}
    for fcu in act.fcurves:
        (name, mode) = utils.fCurveIdentity(fcu)
        for pb in context.selected_pose_bones:
            if pb.name == name:
                kp = fcu.keyframe_points[frame]
                if utils.isRotation(mode):
                    origRot[fcu.array_index][fcu.data_path] = kp.co[1]
                    touchedRot[pb.name] = True
                elif utils.isLocation(mode):
                    origLoc[fcu.array_index][fcu.data_path] = kp.co[1]
                    touchedLoc[pb.name] = True

    for name in touchedRot.keys():
        pb = rig.pose.bones[name]
        utils.insertRotationKeyFrame(pb, frame)
    for name in touchedLoc.keys():
        pb = rig.pose.bones[name]
        pb.keyframe_insert("location", frame=frame, group=pb.name)
    
    for fcu in act.fcurves:
        (name, mode) = utils.fCurveIdentity(fcu)
        try:
            if utils.isRotation(mode):
                dy = fcu.evaluate(frame) - origRot[fcu.array_index][fcu.data_path]
            elif utils.isLocation(mode):
                dy = fcu.evaluate(frame) - origLoc[fcu.array_index][fcu.data_path]
        except:
            continue     
        for kp in fcu.keyframe_points:
            if kp.co[0] != frame:
                kp.co[1] += dy
    return        

class VIEW3D_OT_McpShiftBoneFCurvesButton(bpy.types.Operator):
    bl_idname = "mcp.shift_bone"
    bl_label = "Shift bone F-curves"

    def execute(self, context):
        shiftBoneFCurves(context)
        print("Bones shifted")
        return{'FINISHED'}    

    
#
#   storeAction(context, toProp, prefix):
#   class VIEW3D_OT_McpStoreActionButton(bpy.types.Operator):
#

def storeAction(context, toProp, prefix):
    rig = context.object
    act = utils.getAction(rig)
    if not act:
        return
    aname = act.name        
    act.name = prefix+aname
    act.use_fake_user = True
    nact = context.blend_data.actions.new(aname)
    rig.animation_data.action = nact
    rig[toProp] = act.name
    rig['McpActionName'] = aname

    for fcu in act.fcurves:
        (name, mode) = utils.fCurveIdentity(fcu)
        nfcu = nact.fcurves.new(fcu.data_path, index=fcu.array_index, action_group=name)
        n = len(fcu.keyframe_points)
        nfcu.keyframe_points.add(count=n)
        for i in range(n):
            nfcu.keyframe_points[i].co = fcu.keyframe_points[i].co
    utils.setInterpolation(rig)        
    print("Action stored")
    return nact       

class VIEW3D_OT_McpStoreActionButton(bpy.types.Operator):
    bl_idname = "mcp.store_action"
    bl_label = "Store action"

    def execute(self, context):
        storeAction(context, 'McpUndoAction', '#')
        return{'FINISHED'}    

#
#   undoAction(context, fromProp, toProp, prefix, handle):
#   class VIEW3D_OT_McpUndoActionButton(bpy.types.Operator):
#   class VIEW3D_OT_McpRedoActionButton(bpy.types.Operator):
#

def undoAction(context, fromProp, toProp, prefix, handle):
    rig = context.object
    try:
        name = rig[fromProp]
        oact = context.blend_data.actions[name]
    except:
        oact = None
    if not oact:
        print("No action to %s" % handle)
        return
    act = utils.getAction(rig)
    if act:
        act.name = prefix+act.name
    act.use_fake_user = True
    rig[toProp] = act.name
    rig[fromProp] = ""
    oact.name = rig['McpActionName'] 
    rig.animation_data.action = oact        
    print("Action changes %sne" % handle)
    return

class VIEW3D_OT_McpUndoActionButton(bpy.types.Operator):
    bl_idname = "mcp.undo_action"
    bl_label = "Undo action"

    def execute(self, context):
        undoAction(context, 'McpUndoAction', 'McpRedoAction', '#', 'undo')
        return{'FINISHED'} 
        
class VIEW3D_OT_McpRedoActionButton(bpy.types.Operator):
    bl_idname = "mcp.redo_action"
    bl_label = "Redo action"

    def execute(self, context):
        undoAction(context, 'McpRedoAction', 'McpUndoAction', '%', 'redo')
        return{'FINISHED'} 
        
#
#   displaceFCurves(context):
#   setupCatmullRom(kpoints, modified): 
#   evalCatmullRom(t, fcn):
#   class VIEW3D_OT_McpDisplaceFCurvesButton(bpy.types.Operator):
#

def displaceFCurves(context):
    rig = context.object
    try:
        name = rig['McpUndoAction']
        oact = context.blend_data.actions[name]
    except:
        oact = None
    if not oact:
        print("No stored action")
        return
    act = utils.getAction(rig)
    if not act:
        return
    nact = storeAction(context, 'McpRedoAction', '%')

    nCurves = 0
    for fcu in nact.fcurves:
        ofcu = utils.findFCurve(fcu.data_path, fcu.array_index, oact.fcurves)
        if not ofcu:
            continue
        (name,mode) =  utils.fCurveIdentity(fcu)
        print(name, mode)
        print("  ", ofcu)
        modified = []
        first = True
        for kp in fcu.keyframe_points:            
            t = kp.co[0]
            dy = kp.co[1] - ofcu.evaluate(t)
            if abs(dy) > 1e-4 or first:
                modified.append((t,dy))
            first = False
        modified.append((t,dy))
        
        if len(modified) > 2:
            nCurves += 1
            fcn = setupCatmullRom(modified)            
            for kp in fcu.keyframe_points:
                t = int(kp.co[0])
                y = ofcu.evaluate(t)
                dy = evalCatmullRom(t, fcn)
                #if utils.isLocation(mode):
                #    print(" ", t, y, dy, y+dy)
                kp.co[1] = y+dy
    print("%d F-curves changed" % nCurves)
    return                
                        
def setupCatmullRom(points): 
    n = len(points)-1
    fcn = []
    tension = 0.5
    
    # First interval
    (t0,y0) = points[0]
    (t1,y1) = points[1]
    (t2,y2) = points[2]
    d = y0
    a = y1
    c = 3*d + tension*(y1-y0)
    b = 3*a - tension*(y2-y0)
    tfac = 1.0/(t1-t0)
    fcn.append((t0, t1, tfac, (a,b,c,d)))
    
    # Inner intervals
    for i in range(1,n-1):
        (t_1,y_1) = points[i-1]
        (t0,y0) = points[i]
        (t1,y1) = points[i+1]
        (t2,y2) = points[i+2]
        d = y0
        a = y1
        c = 3*d + tension*(y1-y_1)
        b = 3*a - tension*(y2-y0)
        tfac = 1.0/(t1-t0)
        fcn.append((t0, t1, tfac, (a,b,c,d)))
        
    # Last interval
    (t_1,y_1) = points[n-2]
    (t0,y0) = points[n-1]
    (t1,y1) = points[n]
    if t1-t0 > 1e-4:
        d = y0
        a = y1
        c = 3*d + tension*(y1-y_1)
        b = 3*a - tension*(y1-y0)
        tfac = 1.0/(t1-t0)
        fcn.append((t0, t1, tfac, (a,b,c,d)))

    return fcn  
    
def evalCatmullRom(t, fcn):
    (t0, t1, tfac, params) = fcn[0]
    if t < t0:
        return evalCRInterval(t, t0, t1, tfac, params)
    for (t0, t1, tfac, params) in fcn:
        if t >= t0 and t < t1:
            return evalCRInterval(t, t0, t1, tfac, params)
    return evalCRInterval(t, t0, t1, tfac, params)

def evalCRInterval(t, t0, t1, tfac, params):
    (a,b,c,d) = params
    x = tfac*(t-t0)
    x1 = 1-x
    f = x*x*(a*x + b*x1) + x1*x1*(c*x+d*x1)
    return f
        
class VIEW3D_OT_McpDisplaceFCurvesButton(bpy.types.Operator):
    bl_idname = "mcp.displace_fcurves"
    bl_label = "Displace F-curves"

    def execute(self, context):
        displaceFCurves(context)
        return{'FINISHED'} 

########################################################################
#
#   class AdjustPanel(bpy.types.Panel):
#

class AdjustPanel(bpy.types.Panel):
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
        layout.label("Loop animation")
        layout.prop(scn, "McpLoopBlendRange")
        layout.prop(scn, "McpLoopInPlace")
        if scn['McpLoopInPlace']:
            layout.prop(scn, "McpLoopZInPlace")
        layout.operator("mcp.loop_fcurves")
        layout.label("Repeat animation")
        layout.prop(scn, "McpRepeatNumber")
        layout.operator("mcp.repeat_fcurves")
        layout.label("Shift")
        layout.operator("mcp.shift_bone")
        layout.label("Displace animation")
        layout.operator("mcp.store_action")
        layout.operator("mcp.undo_action")
        layout.operator("mcp.redo_action")
        layout.operator("mcp.displace_fcurves")
                
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

