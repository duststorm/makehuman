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
    "version": "0.2",
    "blender": (2, 5, 8),
    "api": 37702,
    "location": "View3D > Properties > MHX Rigify",
    "description": "Modify MHX rig for use with modifiy",
    "warning": "",
    'wiki_url': "",
    "category": "3D View"}

import bpy

#
#   rigifyMhx(context, mhx):
#

def rigifyMhx(context, mhx):
    print("Modifying MHX rig to Rigify")
    # Delete widgets
    scn = context.scene 
    for ob in scn.objects:
        if ob.type == 'MESH' and ob.name[0:3] == "WGT":
            scn.objects.unlink(ob)

    # Save mhx bone locations    
    name = mhx.name
    mhx['MhxRigify'] = True
    heads = {}
    tails = {}
    rolls = {}
    parents = {}
    extras = {}
    bpy.ops.object.mode_set(mode='EDIT')

    newParents = {
        'head' : 'DEF-head',
        'ribs' : 'DEF-ribs',
        'upper_arm.L' : 'DEF-upper_arm.L.02',
        'thigh.L' : 'DEF-thigh.L.02',
        'upper_arm.R' : 'DEF-upper_arm.R.02',
        'thigh.R' : 'DEF-thigh.R.02',
    }

    for eb in mhx.data.edit_bones:
        heads[eb.name] = eb.head.copy()
        tails[eb.name] = eb.tail.copy()
        rolls[eb.name] = eb.roll
        if eb.parent:            
            par = eb.parent.name
            print(eb.name, par)
            try:
                parents[eb.name] = newParents[par]
            except:
                parents[eb.name] = par
        else:
            parents[eb.name] = None
        extras[eb.name] = not eb.layers[16]
    bpy.ops.object.mode_set(mode='OBJECT')
   
    # Find corresponding meshes. Can be several (clothes etc.)   
    meshes = []
    for ob in scn.objects:
        for mod in ob.modifiers:
            if (mod.type == 'ARMATURE' and mod.object == mhx):
                meshes.append((ob, mod))
    if meshes == []:
        raise NameError("Did not find matching mesh")
        
    # Rename Head vertex group    
    for (mesh, mod) in meshes:
        try:
            vg = mesh.vertex_groups['DfmHead']
            vg.name = 'DEF-head'
        except:
            pass

    # Change rigify bone locations    
    scn.objects.active = None 
    try:
        bpy.ops.object.armature_human_advanced_add()
        success = True
    except:
        success = False
    if not success:
        raise NameError("Unable to create advanced human. Make sure that the Rigify add-on is enabled. It is found under Rigging.")
        return

    rigify = context.object
    bpy.ops.object.mode_set(mode='EDIT')
    for eb in rigify.data.edit_bones:
        eb.head = heads[eb.name]
        eb.tail = tails[eb.name]
        eb.roll = rolls[eb.name]
        extras[eb.name] = False

    fingerPlanes = [
        ('UP-thumb.L', 'thumb.01.L', 'thumb.03.L', ['thumb.02.L']),
        ('UP-index.L', 'finger_index.01.L', 'finger_index.03.L', ['finger_index.02.L']),
        ('UP-middle.L', 'finger_middle.01.L', 'finger_middle.03.L', ['finger_middle.02.L']),
        ('UP-ring.L', 'finger_ring.01.L', 'finger_ring.03.L', ['finger_ring.02.L']),
        ('UP-pinky.L', 'finger_pinky.01.L', 'finger_pinky.03.L', ['finger_pinky.02.L']),
        ('UP-thumb.R', 'thumb.01.R', 'thumb.03.R', ['thumb.02.R']),
        ('UP-index.R', 'finger_index.01.R', 'finger_index.03.R', ['finger_index.02.R']),
        ('UP-middle.R', 'finger_middle.01.R', 'finger_middle.03.R', ['finger_middle.02.R']),
        ('UP-ring.R', 'finger_ring.01.R', 'finger_ring.03.R', ['finger_ring.02.R']),
        ('UP-pinky.R', 'finger_pinky.01.R', 'finger_pinky.03.R', ['finger_pinky.02.R']),
    ]

    for (upbone, first, last, middles) in fingerPlanes:
        extras[upbone] = False
        #lineateChain(upbone, first, last, middles, 0.01, rigify, heads, tails)

    ikPlanes = [
        ('UP-leg.L', 'thigh.L', 'shin.L'),
        ('UP-arm.L', 'upper_arm.L', 'forearm.L'),
        ('UP-leg.R', 'thigh.R', 'shin.R'),
        ('UP-arm.R', 'upper_arm.R', 'forearm.R'),
    ]

    for (upbone, first, last) in ikPlanes:
        extras[upbone] = False
        lineateChain(upbone, first, last, [], 0.1, rigify, heads, tails)

    bpy.ops.object.mode_set(mode='OBJECT')

    # Generate meta rig    
    bpy.ops.pose.rigify_generate()
    scn.objects.unlink(rigify)
    meta = context.object
    meta.name = name+"Meta"
    meta.show_x_ray = True
    for (mesh, mod) in meshes:
        mod.object = meta

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
            b2.hide_select = b1.hide_select
            b2.show_wire = b1.show_wire
            layers = 32*[False]
            if b1.layers[8]:
                layers[28] = True
            else:
                layers[29] = True
            if b1.layers[10]:
                layers[2] = True
            b2.layers = layers
            for cns1 in pb1.constraints:
                cns2 = copyConstraint(cns1, pb1, pb2, mhx, meta)    
                if cns2.type == 'CHILD_OF':
                    meta.data.bones.active = pb2.bone
                    bpy.ops.constraint.childof_set_inverse(constraint=cns2.name, owner='BONE')    
    
    # Create animation data
    if mhx.animation_data:
        for fcu in mhx.animation_data.drivers:
            meta.animation_data.drivers.from_existing(src_driver=fcu)

    fixDrivers(meta.animation_data, mhx, meta)
    for (mesh, mod) in meshes:
        fixDrivers(mesh.data.shape_keys.animation_data, mhx, meta)

    scn.objects.unlink(mhx)
    print("Rigify rig complete")    
    return

#
#   lineateChain(upbone, first, last, middles, minDist, rigify, heads, tails):
#   lineate(pt, start, minDist, normal, offVector):
#

def lineateChain(upbone, first, last, middles, minDist, rigify, heads, tails):
    fb = rigify.data.edit_bones[first]
    lb = rigify.data.edit_bones[last]
    uhead = heads[upbone]
    utail = tails[upbone]
    tang = lb.tail - fb.head
    tangent = tang/tang.length
    up = (uhead+utail)/2 - fb.head
    norm = up - tangent*tangent.dot(up)
    normal = norm/norm.length
    offVector = tangent.cross(normal)
    vec = utail - uhead
    fb.tail = lineate(fb.tail, fb.head, minDist, normal, offVector)
    lb.head = lineate(lb.head, fb.head, minDist, normal, offVector)
    for bone in middles:
        mb = rigify.data.edit_bones[bone]
        mb.head = lineate(mb.head, fb.head, minDist, normal, offVector)
        mb.tail = lineate(mb.tail, fb.head, minDist, normal, offVector)
    return

def lineate(pt, start, minDist, normal, offVector):
    diff = pt - start
    diff = diff - offVector*offVector.dot(diff) 
    dist = diff.dot(normal)
    if dist < minDist:
        diff += (minDist - dist)*normal
    return start + diff

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
    substitute = {
        'Head' : 'DEF-head',
        'MasterFloor' : 'root',
        'upper_arm.L' : 'DEF-upper_arm.L.01',
        'upper_arm.R' : 'DEF-upper_arm.R.01',
        'thigh.L' : 'DEF-thigh.L.01',
        'thigh.R' : 'DEF-thigh.R.01',
        'shin.L' : 'DEF-shin.L.01',
        'shin.R' : 'DEF-shin.R.01'
    }

    cns2 = pb2.constraints.new(cns1.type)
    for prop in dir(cns1):
        if prop == 'target':
            if cns1.target == mhx:
                cns2.target = meta
            else:
                cns2.target = cns1.target
        elif prop == 'subtarget':
            try:
                cns2.subtarget = substitute[cns1.subtarget]
            except:
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
        rigifyMhx(context, context.object)
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
        if context.object:
            try:
                return context.object['MhxRigify']
            except:
                return False
        return False

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

    
