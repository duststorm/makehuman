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
                if ( utils.isLocation(mode) and
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
        pt1 = (t1, (eps*vm + (1-eps)*v1))
        
        t1 = t0-dt
        v1 = fcu.evaluate(t1) + dt*dv
        tm = tn-dt
        vm = fcu.evaluate(tm)
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
            elif  utils.isLocation(mode):
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
#   startEdit(context):
#   class VIEW3D_OT_McpStartEditButton(bpy.types.Operator):
#

def startEdit(context):
    rig = context.object
    try:
        if (rig['McpUndoAction'] or rig['McpActionName']):
            print("Action already being edited. Undo or confirm edit first")
            return
    except:
        pass
    act = utils.getAction(rig)
    if not act:
        return
    aname = act.name        
    act.name = '#'+aname
    nact = bpy.data.actions.new(aname)
    rig.animation_data.action = nact
    rig['McpUndoAction'] = act.name
    rig['McpActionName'] = aname

    the.editLoc = quadDict()
    the.editRot = quadDict()

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

class VIEW3D_OT_McpStartEditButton(bpy.types.Operator):
    bl_idname = "mcp.start_edit"
    bl_label = "Start edit"

    def execute(self, context):
        startEdit(context)
        return{'FINISHED'}    

#
#   undoEdit(context):
#   class VIEW3D_OT_McpUndoEditButton(bpy.types.Operator):
#

def undoEdit(context):
    rig = context.object
    try:
        name = rig['McpUndoAction']
        oact = bpy.data.actions[name]
    except:
        oact = None
    if not oact:
        print("No action to undo")
        return
    rig['McpUndoAction'] = ""
    the.editLoc = None
    the.editRot = None
    rig['McpActionName'] = ""
    act = rig.animation_data.action
    act.name = "#Delete"
    oact.name = rig['McpActionName'] 
    rig.animation_data.action = oact
    utils.deleteAction(act)
    print("Action changes undone")
    return

class VIEW3D_OT_McpUndoEditButton(bpy.types.Operator):
    bl_idname = "mcp.undo_edit"
    bl_label = "Undo edit"

    def execute(self, context):
        undoEdit(context)
        return{'FINISHED'} 
        
#
#   getActionPair(context):
#

def getActionPair(context):
    rig = context.object
    try:
        name = rig['McpUndoAction']
        oact = context.blend_data.actions[name]
    except:
        oact = None
    if not oact:
        print("No stored action")
        return None
    try:
        the.editLoc
        the.editRot
    except:
        the.editLoc = quadDict()
        the.editRot = quadDict()
    act = utils.getAction(rig)
    if act:
        return (act, oact)
    else:
        return None

#
#   confirmEdit(context):
#   class VIEW3D_OT_McpConfirmEditButton(bpy.types.Operator):
#

def confirmEdit(context):
    rig = context.object
    pair = getActionPair(context)
    if not pair:
        return
    (act, oact) = pair

    for fcu in act.fcurves:
        ofcu = utils.findFCurve(fcu.data_path, fcu.array_index, oact.fcurves)
        if not ofcu:
            continue
        (name,mode) =  utils.fCurveIdentity(fcu)
        if utils.isRotation(mode):
            try:
                edit = the.editRot[fcu.array_index][name]
            except:
                continue
            displaceFCurve(fcu, ofcu, edit)
        elif  utils.isLocation(mode):
            try:
                edit = the.editLoc[fcu.array_index][name]
            except:
                continue
            displaceFCurve(fcu, ofcu, edit)

    rig['McpUndoAction'] = ""
    rig['McpActionName'] = ""
    the.editLoc = None
    the.editRot = None
    utils.deleteAction(oact)
    print("Action changed")
    return                
            
class VIEW3D_OT_McpConfirmEditButton(bpy.types.Operator):
    bl_idname = "mcp.confirm_edit"
    bl_label = "Confirm edit"

    def execute(self, context):
        confirmEdit(context)
        return{'FINISHED'} 

#
#   setEditDict(editDict, frame, name, channel, index):
#   insertKey(context, useLoc, useRot):
#   class VIEW3D_OT_McpInsertLocButton(bpy.types.Operator):
#   class VIEW3D_OT_McpInsertRotButton(bpy.types.Operator):
#   class VIEW3D_OT_McpInsertLocRotButton(bpy.types.Operator):
#

def setEditDict(editDict, frame, name, channel, n):
    for index in range(n):        
        try:
            editDict[index][name]
        except:
            editDict[index][name] = {}
        edit = editDict[index][name]
        edit[frame] = channel[index]
    return        

def insertKey(context, useLoc, useRot):
    rig = context.object
    pair = getActionPair(context)
    if not pair:
        return
    (act, oact) = pair
    
    pb = bpy.context.active_pose_bone
    frame = context.scene.frame_current    
    for pb in rig.pose.bones:
        if not pb.bone.select:
            continue
        if useLoc:
            setEditDict(the.editLoc, frame, pb.name, pb.location, 3)
        if useRot:        
            if pb.rotation_mode == 'QUATERNION':
                setEditDict(the.editRot, frame, pb.name, pb.rotation_quaternion, 4)
            else:
                setEditDict(the.editRot, frame, pb.name, pb.rotation_euler, 3)
        for fcu in act.fcurves:
            ofcu = utils.findFCurve(fcu.data_path, fcu.array_index, oact.fcurves)
            if not ofcu:
                continue
            (name,mode) =  utils.fCurveIdentity(fcu)
            if name == pb.name:
                if utils.isRotation(mode) and useRot:
                    displaceFCurve(fcu, ofcu, the.editRot[fcu.array_index][name])
                if  utils.isLocation(mode) and useLoc:
                    displaceFCurve(fcu, ofcu, the.editLoc[fcu.array_index][name])
    return                

class VIEW3D_OT_McpInsertLocButton(bpy.types.Operator):
    bl_idname = "mcp.insert_loc"
    bl_label = "Loc"

    def execute(self, context):
        insertKey(context, True, False)
        return{'FINISHED'} 
        
class VIEW3D_OT_McpInsertRotButton(bpy.types.Operator):
    bl_idname = "mcp.insert_rot"
    bl_label = "Rot"

    def execute(self, context):
        insertKey(context, False, True)
        return{'FINISHED'} 
        
class VIEW3D_OT_McpInsertLocRotButton(bpy.types.Operator):
    bl_idname = "mcp.insert_locrot"
    bl_label = "LocRot"

    def execute(self, context):
        insertKey(context, True, True)
        return{'FINISHED'} 
        
#
#   displaceFCurve(fcu, ofcu, edits):       
#   setupCatmullRom(kpoints, modified): 
#   evalCatmullRom(t, fcn):
#
        
def displaceFCurve(fcu, ofcu, edits):        
    modified = []
    editList = list(edits.items())
    editList.sort()
    for (t,y) in editList:
        dy = y - ofcu.evaluate(t)
        modified.append((t,dy))
        
    if len(modified) >= 1:
        kp = fcu.keyframe_points[0].co
        t0 = int(kp[0])
        (t1,y1) = modified[0]
        kp = fcu.keyframe_points[-1].co
        tn = int(kp[0])
        (tn_1,yn_1) = modified[-1]
        modified = [(t0, y1)] + modified
        modified.append( (tn, yn_1) )
        fcn = setupCatmullRom(modified)            
        for kp in fcu.keyframe_points:
            t = kp.co[0]
            y = ofcu.evaluate(t)
            dy = evalCatmullRom(t, fcn)
            kp.co[1] = y+dy
    return
    
                        
def setupCatmullRom(points): 
    points.sort()
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
        layout.operator("mcp.start_edit")
        layout.operator("mcp.undo_edit")
        row = layout.row()
        row.operator("mcp.insert_loc")
        row.operator("mcp.insert_rot")
        row.operator("mcp.insert_locrot")
        layout.operator("mcp.confirm_edit")
                
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

