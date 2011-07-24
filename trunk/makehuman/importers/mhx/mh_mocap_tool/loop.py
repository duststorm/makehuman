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
from . import load, simplify, props

#
#   loopFCurves(context, rig):
#

def loopFCurves(context, rig):
    scn = context.scene
    (fcurves, minTime, maxTime) = simplify.getRigFCurves(rig, False, True, scn)
    if not fcurves:
        return
    act = rig.animation_data.action

    root = props.getBone(rig, 'Root')
    rootLoc = {}
    for fcu in fcurves:
        name = fcu.data_path.split('"')[1]
        if name == root:
            mode = fcu.data_path.split('.')[-1]
            if mode == 'location':
                rootLoc[fcu.array_index] = fcu    
  
    print(rootLoc.items())
    
    for fcu in fcurves:
        name = fcu.data_path.split('"')[1]
        if name != root:
            offsetFCurve(fcu, rootLoc, scn)
            loopFCurve(fcu, minTime, maxTime, scn)

    for fcu in fcurves:
        name = fcu.data_path.split('"')[1]
        if name == root:
            offsetFCurve(fcu, rootLoc, scn)
            loopFCurve(fcu, minTime, maxTime, scn)            
    print("Curves looped")
    return

#
#   offsetFCurve(fcu, rootLoc, scn):            
#

def offsetFCurve(fcu, rootLoc, scn):            
    mode = fcu.data_path.split('.')[-1]
    if mode == 'location' and scn['MhxLoopInPlace']:
        root = rootLoc[fcu.array_index]
        for kp in fcu.keyframe_points:
            frame = kp.co[0]
            kp.co[1] -= root.evaluate(frame)
    return    
    
#
#   loopFCurve(fcu, minTime, maxTime, scn):
#

def loopFCurve(fcu, t0, tn, scn):
    delta = scn['MhxLoopBlendRange']
    
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
        
    print(fcu.data_path)        
    newpoints.sort()
    #for (t,v) in newpoints: 
        #fcu.keyframe_points.insert(frame=t, value=v)
    return
    

########################################################################
#
#   class VIEW3D_OT_MhxSimplifyFCurvesButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxSimplifyFCurvesButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_loop_fcurves"
    bl_label = "Loop F-curves"

    def execute(self, context):
        loopFCurves(context, context.object)
        return{'FINISHED'}    

#
#   class LoopPanel(bpy.types.Panel):
#

class LoopPanel(bpy.types.Panel):
    bl_label = "Mocap: Loop"
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
        layout.prop(scn, "MhxLoopBlendRange")
        layout.prop(scn, "MhxLoopInPlace")
        #if scn['MhxLoopInPlace']:
        #    layout.prop(scn, "MhxLoopZInPlace")
        layout.operator("mhx.mocap_loop_fcurves")
                
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

