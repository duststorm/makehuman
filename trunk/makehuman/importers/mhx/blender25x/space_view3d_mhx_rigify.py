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

"""
Abstract

"""

bl_info = {
    "name": "MHX Rigify",
    "author": "Thomas Larsson",
    "version": "0.1",
    "blender": (2, 5, 8),
    "api": 37702,
    "location": "View3D > Properties > MHX Rigify",
    "description": "Modify MHX rig for use with modifiy",
    "warning": "",
    'wiki_url': "",
    "category": "3D View"}

import bpy

#
#   rigifyMhxRig(context):
#

def rigifyMhx(context):
    print("Modifying MHX rig to Rigify")
    # Delete widgets
    scn = context.scene 
    for ob in scn.objects:
        if ob.type == 'MESH' and ob.name[0:3] == "WGT":
            scn.objects.unlink(ob)

    # Save mhx bone locations    
    mhx = context.object
    name = mhx.name
    heads = {}
    tails = {}
    rolls = {}
    parents = {}
    extras = {}
    bpy.ops.object.mode_set(mode='EDIT')
    for eb in mhx.data.edit_bones:
        heads[eb.name] = eb.head.copy()
        tails[eb.name] = eb.tail.copy()
        rolls[eb.name] = eb.roll
        if eb.parent:
            par = eb.parent.name
            if par == 'head':
                parents[eb.name] = 'DEF-head'
            else:
                parents[eb.name] = par
        else:
            parents[eb.name] = None
        extras[eb.name] = True
    bpy.ops.object.mode_set(mode='OBJECT')
   
    # Find corresponding mesh   
    mesh = None
    for ob in scn.objects:
        for mod in ob.modifiers:
            if (mod.type == 'ARMATURE' and mod.object == mhx):
                mesh = ob
                amtMod = mod
    if not mesh:
        raise NameError("Did not find matching mesh")
        
    # Rename Head vertex group    
    vg = mesh.vertex_groups['DfmHead']
    vg.name = 'DEF-head'

    # Change rigify bone locations    
    scn.objects.active = None 
    bpy.ops.object.armature_human_advanced_add()
    rigify = context.object
    bpy.ops.object.mode_set(mode='EDIT')
    for eb in rigify.data.edit_bones:
        eb.head = heads[eb.name]
        eb.tail = tails[eb.name]
        extras[eb.name] = False

    bpy.ops.object.mode_set(mode='OBJECT')

    # Generate meta rig    
    bpy.ops.pose.rigify_generate()
    scn.objects.unlink(rigify)
    meta = context.object
    meta.name = name+"Meta"
    amtMod.object = meta

    # Copy extra bones to meta rig
    bpy.ops.object.mode_set(mode='EDIT')
    for name in heads.keys():
        if extras[name]:
            eb = meta.data.edit_bones.new(name)
            eb.head = heads[name]
            eb.tail = tails[name]
            eb.roll = rolls[name]            
    for name in heads.keys():
        if extras[name] and parents[name]:
            eb = meta.data.edit_bones[name]
            eb.parent = meta.data.edit_bones[parents[name]]

    # Copy constraints etc.
    bpy.ops.object.mode_set(mode='POSE')
    for name in heads.keys():
        if extras[name]:
            pb1 = mhx.pose.bones[name]
            pb2 = meta.pose.bones[name]
            pb2.custom_shape = pb1.custom_shape
            pb2.lock_location = pb1.lock_location
            pb2.lock_rotation = pb1.lock_rotation
            pb2.lock_scale = pb1.lock_scale
            b1 = pb1.bone
            b2 = pb2.bone
            b2.use_deform = b1.use_deform
            b2.hide = b1.hide
            b2.hide_select = b1.hide_select
            b2.show_wire = b1.show_wire
            for cns1 in pb1.constraints:
                cns2 = copyConstraint(cns1, pb1, pb2, mhx, meta)    
                if cns2.type == 'CHILD_OF':
                    pass
                    #bpy.ops.constraint.childof_set_inverse(constraint=cns2.name, owner='BONE')    
    
    # Create animation data
    if mhx.animation_data:
        for fcu in mhx.animation_data.drivers:
            meta.animation_data.drivers.from_existing(src_driver=fcu)

    fixDrivers(meta.animation_data, mhx, meta)
    fixDrivers(mesh.data.shape_keys.animation_data, mhx, meta)

    scn.objects.unlink(mhx)
    print("Rigify rig complete")    
    return

#
#   fixDrivers(adata, mhx, meta):
#

def fixDrivers(adata, mhx, meta):
    if not adata:
        return
    for fcu in adata.drivers:
        for var in fcu.driver.variables:
            for targ in var.targets:
                if targ.id == mhx:
                    targ.id = meta
    return

#
#   copyConstraint(cns1, pb1, pb2, mhx, meta):
#

def copyConstraint(cns1, pb1, pb2, mhx, meta):
    cns2 = pb2.constraints.new(cns1.type)
    for prop in dir(cns1):
        if prop == 'target':
            if cns1.target == mhx:
                cns2.target = meta
            else:
                cns2.target = cns1.target
        elif prop == 'subtarget':
            if cns1.subtarget == 'Head':
                cns2.subtarget = 'DEF-head'
            elif cns1.subtarget == 'MasterFloor':
                cns2.subtarget = 'root'
            else:
                cns2.subtarget = cns1.subtarget
        elif prop[0] != '_':
            try:
                expr = "cns2.%s = cns1.%s" % (prop, prop)
                #print(pb1.name, expr)
                exec(expr)
            except:
                pass
    return cns2

#
#   class OBJECT_OT_RigifyMhxButton(bpy.types.Operator):
#

class OBJECT_OT_RigifyMhxButton(bpy.types.Operator):
    bl_idname = "mhxrig.rigify_mhx"
    bl_label = "Rigify MHX rig"

    def execute(self, context):
        rigifyMhx(context)
        return{'FINISHED'}    
    
#
#   class RigifyMhxPanel(bpy.types.Panel):
#

class RigifyMhxPanel(bpy.types.Panel):
    bl_label = "Rigify MHX"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return (context.object and 
            (context.object.type == 'ARMATURE'))

    def draw(self, context):
        layout = self.layout
        layout.operator("mhxrig.rigify_mhx")
        return

#
#    Register
#

def register():
    bpy.utils.register_module(__name__)
    pass

def unregister():
    bpy.utils.unregister_module(__name__)
    pass

if __name__ == "__main__":
    register()

    
