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

#
#    togglePoleTargets(trgRig):
#

def togglePoleTargets(trgRig):
    bones = trgRig.data.bones
    pbones = trgRig.pose.bones
    if bones['ElbowPT_L'].hide:
        hide = False
        poletar = trgRig
        res = 'ON'
        trgRig.McpTogglePoleTargets = True
    else:
        hide = True
        poletar = None
        res = 'OFF'
        trgRig.McpTogglePoleTargets = False
    for suffix in ['_L', '_R']:
        for name in ['ElbowPT', 'ElbowLinkPT', 'Elbow', 'KneePT', 'KneeLinkPT', 'Knee']:
            try:
                bones[name+suffix].hide = hide
            except:
                pass
        cns = pbones['LoArm'+suffix].constraints['ArmIK']
        cns = pbones['LoLeg'+suffix].constraints['LegIK']
        cns.pole_target = poletar
    return res

#
#    toggleIKLimits(trgRig):
#

def toggleIKLimits(trgRig):
    pbones = trgRig.pose.bones
    if pbones['UpLeg_L'].use_ik_limit_x:
        use = False
        res = 'OFF'
        trgRig.McpToggleIkLimits = False
    else:
        use = True
        res = 'ON'
        trgRig.McpToggleIkLimits = True
    for suffix in ['_L', '_R']:
        for name in ['UpArm', 'LoArm', 'UpLeg', 'LoLeg']:
            pb = pbones[name+suffix]
            pb.use_ik_limit_x = use
            pb.use_ik_limit_y = use
            pb.use_ik_limit_z = use
    return res

#
#    toggleLimitConstraints(trgRig):
#    setLimitConstraints(trgRig, inf):
#

def toggleLimitConstraints(trgRig):
    pbones = trgRig.pose.bones
    first = True
    trgRig.McpToggleLimitConstraints = False
    for pb in pbones:
        if onUserLayer(pb.bone.layers):
            for cns in pb.constraints:
                if (cns.type == 'LIMIT_LOCATION' or
                    cns.type == 'LIMIT_ROTATION' or
                    cns.type == 'LIMIT_DISTANCE' or
                    cns.type == 'LIMIT_SCALE'):
                    if first:
                        first = False
                        if cns.influence > 0.5:
                            inf = 0.0
                            res = 'OFF'
                        else:
                            inf = 1.0
                            res = 'ON'
                            trgRig.McpToggleLimitConstraints = True
                    cns.influence = inf
    if first:
        return 'NOT FOUND'
    return res

def onUserLayer(layers):
    for n in [0,1,2,3,4,5,6,7, 9,10,11,12,13]:
        if layers[n]:
            return True
    return False

def setLimitConstraints(trgRig, inf):
    pbones = trgRig.pose.bones
    for pb in pbones:
        if onUserLayer(pb.bone.layers):
            for cns in pb.constraints:
                if (cns.type == 'LIMIT_LOCATION' or
                    cns.type == 'LIMIT_ROTATION' or
                    cns.type == 'LIMIT_DISTANCE' or
                    cns.type == 'LIMIT_SCALE'):
                    cns.influence = inf
    return

#
#    silenceConstraints(rig):
#

def silenceConstraints(rig):
    for pb in rig.pose.bones:
        pb.lock_location = (False, False, False)
        pb.lock_rotation = (False, False, False)
        pb.lock_scale = (False, False, False)
        for cns in pb.constraints:
            if cns.type == 'CHILD_OF':
                cns.influence = 0.0
            elif False and (cns.type == 'LIMIT_LOCATION' or
                cns.type == 'LIMIT_ROTATION' or
                cns.type == 'LIMIT_DISTANCE' or
                cns.type == 'LIMIT_SCALE'):
                cns.influence = 0.0
    return

########################################################################
#
#   class VIEW3D_OT_McpTogglePoleTargetsButton(bpy.types.Operator):
#

class VIEW3D_OT_McpTogglePoleTargetsButton(bpy.types.Operator):
    bl_idname = "mcp.toggle_pole_targets"
    bl_label = "Toggle pole targets"

    def execute(self, context):
        res = togglePoleTargets(context.object)
        print("Pole targets toggled", res)
        return{'FINISHED'}    

#
#   class VIEW3D_OT_McpToggleIKLimitsButton(bpy.types.Operator):
#

class VIEW3D_OT_McpToggleIKLimitsButton(bpy.types.Operator):
    bl_idname = "mcp.toggle_ik_limits"
    bl_label = "Toggle IK limits"

    def execute(self, context):
        res = toggleIKLimits(context.object)
        print("IK limits toggled", res)
        return{'FINISHED'}    

#
#   class VIEW3D_OT_McpToggleLimitConstraintsButton(bpy.types.Operator):
#

class VIEW3D_OT_McpToggleLimitConstraintsButton(bpy.types.Operator):
    bl_idname = "mcp.toggle_limit_constraints"
    bl_label = "Toggle Limit constraints"

    def execute(self, context):
        res = toggleLimitConstraints(context.object)
        print("Limit constraints toggled", res)
        return{'FINISHED'}    

#
#   class VIEW3D_OT_McpSilenceConstraintsButton(bpy.types.Operator):
#

class VIEW3D_OT_McpSilenceConstraintsButton(bpy.types.Operator):
    bl_idname = "mcp.silence_constraints"
    bl_label = "Silence constraints"

    def execute(self, context):
        silenceConstraints(context.object)
        print("Constraints silenced")
        return{'FINISHED'}    

#
#   class ToggleConstraintPanel(bpy.types.Panel):
#

class ToggleConstraintPanel(bpy.types.Panel):
    bl_label = "Mocap: Toggle constraints"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        if context.object and context.object.type == 'ARMATURE':
            return True

    def draw(self, context):
        layout = self.layout
        ob = context.object
        row = layout.row()
        row.operator("mcp.toggle_pole_targets")
        row.prop(ob, "McpTogglePoleTargets")
        row = layout.row()
        row.operator("mcp.toggle_ik_limits")
        row.prop(ob, "McpToggleIkLimits")
        row = layout.row()
        row.operator("mcp.toggle_limit_constraints")
        row.prop(ob, "McpToggleLimitConstraints")

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()


