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
# Script copyright (C) MakeHuman Team 2001-2013
# Coding Standards:    See http://www.makehuman.org/node/165

"""
Abstract

The MakeHuman application uses predefined morph target files to distort
the humanoid model when physiological changes or changes to the pose are
applied by the user. The morph target files contain extreme mesh
deformations for individual joints and features which can used
proportionately to apply less extreme deformations and which can be
combined to provide a very wide range of options to the user of the
application.

This module contains a set of functions used by 3d artists during the
development cycle to create these extreme morph target files from
hand-crafted models.

"""

import bpy
import os
import sys
import math
import random
from mathutils import Vector, Quaternion, Matrix
from bpy.props import *
from bpy_extras.io_utils import ExportHelper, ImportHelper

from mh_utils import globvars as the
from mh_utils import utils
from mh_utils import proxy
from mh_utils import import_obj

#----------------------------------------------------------
#   
#----------------------------------------------------------

class VIEW3D_OT_ImportBaseMhcloButton(bpy.types.Operator):
    bl_idname = "mh.import_base_mhclo"
    bl_label = "Mhclo"
    bl_options = {'UNDO'}
    delete = BoolProperty()

    def execute(self, context):    
        if self.delete:
            utils.deleteAll(context)
        import_obj.importBaseMhclo(context)
        return{'FINISHED'}    


class VIEW3D_OT_ImportBaseObjButton(bpy.types.Operator):
    bl_idname = "mh.import_base_obj"
    bl_label = "Obj"
    bl_options = {'UNDO'}
    delete = BoolProperty()

    def execute(self, context):
        if self.delete:
            utils.deleteAll(context)
        import_obj.importBaseObj(context)
        return{'FINISHED'}    


class VIEW3D_OT_MakeBaseObjButton(bpy.types.Operator):
    bl_idname = "mh.make_base_obj"
    bl_label = "Make Base Object"
    bl_options = {'UNDO'}

    def execute(self, context):
        the.Proxy = None
        ob = context.object
        for mod in ob.modifiers:
            if mod.type == 'ARMATURE':
                mod.show_in_editmode = True
                mod.show_on_cage = True
            else:
                ob.modifiers.remove(mod)
        utils.removeShapeKeys(ob)
        ob.shape_key_add(name="Basis")
        ob["NTargets"] = 0
        ob["ProxyFile"] = 0
        ob["ObjFile"] =  0
        ob["MhxMesh"] = True        
        utils.setupVertexPairs(context, True)
        return{'FINISHED'}    


def deleteBetween(ob, first, last):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        for n in range(first):
            ob.data.vertices[n].select = False
        for n in range(first, last):
            ob.data.vertices[n].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set(mode='OBJECT')


IrrelevantVerts = {
    'Body' : (the.FirstSkirtVert, the.NTotalVerts),
    'Skirt' : (the.NTotalVerts, the.NTotalVerts),
    'Tights' : (the.FirstSkirtVert, the.FirstTightsVert),
}

AffectedVerts = {
    'Body' : (0, the.FirstSkirtVert),
    'Skirt' : (the.FirstSkirtVert, the.FirstTightsVert),
    'Tights' : (the.FirstTightsVert, the.NTotalVerts),
}

OffsetVerts = {
    'Body' : 0,
    'Skirt' : 0,
    'Tights' : the.FirstTightsVert-the.FirstSkirtVert,
}

class VIEW3D_OT_DeleteIrrelevantButton(bpy.types.Operator):
    bl_idname = "mh.delete_irrelevant"
    bl_label = "Delete Irrelevant Verts"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        ob = context.object
        if ob.MhIrrelevantDeleted:
            return
        if ob.MhAffectOnly != 'All':
            first,last = IrrelevantVerts[ob.MhAffectOnly]
            deleteBetween(ob, first, last)
            if ob.MhAffectOnly in ['Tights']:
                ob.MhMeshVertsDeleted = True
            ob.MhIrrelevantDeleted = True
        return{'FINISHED'}    

 
class VIEW3D_OT_LoadTargetButton(bpy.types.Operator):
    bl_idname = "mh.load_target"
    bl_label = "Load Target File"
    bl_options = {'UNDO'}

    filename_ext = ".target"
    filter_glob = StringProperty(default="*.target", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for target file", 
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        ob = context.object
        if ob.MhMeshVertsDeleted:
            first,last = IrrelevantVerts[ob.MhAffectOnly]
            offset = OffsetVerts[ob.MhAffectOnly]
            utils.loadTarget(self.properties.filepath, context, firstIrrelevant=first, lastIrrelevant=last, offset=offset)
        else:
            utils.loadTarget(self.properties.filepath, context)
        print("Target loaded")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#----------------------------------------------------------
#   loadTargetFromMesh(context):
#----------------------------------------------------------

def loadTargetFromMesh(context):
    ob = context.object
    if not utils.isBaseOrTarget(ob):
        raise NameError("Active object %s is not a base object" % ob.name)
    scn = context.scene
    trg = None
    for ob1 in scn.objects:
        if ob1.select and ob1.type == 'MESH' and ob1 != ob:
            trg = ob1
            break
    if not trg:
        raise NameError("Two meshes must be selected")        
    bpy.ops.object.mode_set(mode='OBJECT')
    
    scn.objects.active = trg
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    scn.objects.active = ob
    name = trg.name
    skey = ob.shape_key_add(name=name, from_mix=False)
    ob.active_shape_key_index = utils.shapeKeyLen(ob) - 1
    skey.name = name
    for v in trg.data.vertices:
        skey.data[v.index].co = v.co
    skey.slider_min = -1.0
    skey.slider_max = 1.0
    skey.value = 1.0
    ob.show_only_shape_key = False
    ob.use_shape_key_edit_mode = True
    ob["NTargets"] += 1
    ob["FilePath"] = 0
    ob.SelectedOnly = False
    scn.objects.unlink(trg)
    return


class VIEW3D_OT_LoadTargetFromMeshButton(bpy.types.Operator):
    bl_idname = "mh.load_target_from_mesh"
    bl_label = "Load Target From Mesh"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return (pollRelax(context) and not context.object.MhMeshVertsDeleted)

    def execute(self, context):
        loadTargetFromMesh(context)
        return {'FINISHED'}


#----------------------------------------------------------
#   newTarget(context):
#----------------------------------------------------------

def newTarget(context):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    skey = ob.shape_key_add(name="Target", from_mix=False)
    ob.active_shape_key_index = utils.shapeKeyLen(ob) - 1
    skey.slider_min = -1.0
    skey.slider_max = 1.0
    skey.value = 1.0
    ob.show_only_shape_key = False
    ob.use_shape_key_edit_mode = True
    ob["NTargets"] += 1
    ob["FilePath"] = 0
    ob.SelectedOnly = False
    return


class VIEW3D_OT_NewTargetButton(bpy.types.Operator):
    bl_idname = "mh.new_target"
    bl_label = "New Target"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        newTarget(context)
        return {'FINISHED'}

#----------------------------------------------------------
#   saveTarget(context):
#----------------------------------------------------------
    
def doSaveTarget(context, filepath):    
    ob = context.object
    if not utils.isTarget(ob):
        raise NameError("%s is not a target")
    bpy.ops.object.mode_set(mode='OBJECT')
    ob.active_shape_key_index = ob["NTargets"]
    if not checkValid(ob):
        return
    saveAll = not ob.SelectedOnly
    skey = ob.active_shape_key    
    if skey.name[0:6] == "Target":
        skey.name = utils.nameFromPath(filepath)
    verts = evalVertLocations(ob)
    
    (fname,ext) = os.path.splitext(filepath)
    filepath = fname + ".target"
    print("Saving target %s to %s" % (ob, filepath))
    if ob.MhAffectOnly != 'All':
        first,last = AffectedVerts[ob.MhAffectOnly]
        before,after = readLines(filepath, first,last)
        fp = open(filepath, "w")  
        for line in before:
            fp.write(line)
        if ob.MhMeshVertsDeleted:
            offset = OffsetVerts[ob.MhAffectOnly]
        else:
            offset = 0
        saveVerts(fp, ob, verts, saveAll, first, last, offset)
        for (vn, string) in after:
            fp.write("%d %s" % (vn, string))
    else:
        fp = open(filepath, "w")  
        saveVerts(fp, ob, verts, saveAll, 0, the.NTotalVerts, 0)
    fp.close()    
    ob["FilePath"] = filepath


def readLines(filepath, first, last):
    before = []
    after = []
    try:
        fp = open(filepath, "rU")
    except NameError:
        return before,after
    for line in fp:
        words = line.split(None, 1)
        if len(words) >= 2:
            vn = int(words[0])
            if vn < first:
                before.append(line)
            elif vn >= last:
                after.append((vn, words[1]))
    fp.close()
    return before,after
    
    
def saveVerts(fp, ob, verts, saveAll, first, last, offs):
    for n in range(first, last):
        vco = verts[n-offs]
        bv = ob.data.vertices[n-offs]
        vec = vco - bv.co
        if vec.length > the.Epsilon and (saveAll or bv.select):
            fp.write("%d %.6f %.6f %.6f\n" % (n, vec[0], vec[2], -vec[1]))

          
def evalVertLocations(ob):    
    verts = {}
    for v in ob.data.vertices:
        verts[v.index] = v.co.copy()
        
    for skey in ob.data.shape_keys.key_blocks:
        if (skey.name == "Basis" or
            (ob.MhZeroOtherTargets and skey != ob.active_shape_key)):
            print("Skipped", skey.name)
            continue       
        print("Adding", skey.name)
        for n,v in enumerate(skey.data):
            bv = ob.data.vertices[n]
            vec = v.co - bv.co
            verts[n] += skey.value*vec
    return verts            

       
class VIEW3D_OT_SaveTargetButton(bpy.types.Operator):
    bl_idname = "mh.save_target"
    bl_label = "Save Target"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        ob = context.object
        path = ob["FilePath"]
        if True or the.Confirm:
            the.Confirm = None
            doSaveTarget(context, path)
            print("Target saved")
        else:
            the.Confirm = "mh.save_target"
            the.ConfirmString = "Overwrite target file?"
            the.ConfirmString2 = ' "%s?"' % os.path.basename(path)
        return{'FINISHED'}            


class VIEW3D_OT_SaveasTargetButton(bpy.types.Operator, ExportHelper):
    bl_idname = "mh.saveas_target"
    bl_label = "Save Target As"
    bl_options = {'UNDO'}

    filename_ext = ".target"
    filter_glob = StringProperty(default="*.target", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for target file", 
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        doSaveTarget(context, self.properties.filepath)
        print("Target saved")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


#----------------------------------------------------------
#   
#----------------------------------------------------------

def pruneTarget(ob, filepath):
    lines = []
    before,after = readLines(filepath, -1,-1)
    for vn,string in after:
        if vn < the.NTotalVerts and ob.data.vertices[vn].select:
            lines.append((vn, string))
    print("Pruning", len(before), len(after), len(lines))
    fp = open(filepath, "w")
    for vn,string in lines:            
        fp.write(str(vn) + " " + string)
    fp.close()


def pruneFolder(ob, folder):            
    for file in os.listdir(folder):    
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            if ob.MhPruneRecursively:
                pruneFolder(ob, path)
        else:
            (name,ext) = os.path.splitext(file)
            if ext == ".target":
                print("Prune", path)
                pruneTarget(ob, path)


class VIEW3D_OT_PruneTargetFileButton(bpy.types.Operator, ExportHelper):
    bl_idname = "mh.prune_target_file"
    bl_label = "Prune Target File"
    bl_options = {'UNDO'}

    filename_ext = ".target"
    filter_glob = StringProperty(default="*.target", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for target file", 
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return (pollRelax(context) and context.object.MhPruneEnabled)

    def execute(self, context):
        ob = context.object
        if ob.MhPruneWholeDir:
            folder = os.path.dirname(self.properties.filepath)
            pruneFolder(ob, folder)
            print("Targets pruned")
        else:
            pruneTarget(ob, self.properties.filepath)
            print("Target pruned")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


#----------------------------------------------------------
#   saveMhpFile(context, filepath):
#   loadMhpFile(context, filepath):
#----------------------------------------------------------

def saveMhpFile(context, filepath):
    ob = context.object
    rig = ob.parent
    scn = context.scene
    if rig and rig.type == 'ARMATURE': 
        roots = rigRoots(rig)
        if len(roots) > 1:
            raise NameError("Armature %s has multiple roots: %s" % (rig.name, roots))
        (pname, ext) = os.path.splitext(filepath)
        mhppath = pname + ".mhp"
        
        fp = open(mhppath, "w")
        root = rig.pose.bones[roots[0]]
        writeMhpBones(fp, root)
        fp.close()
        print("Mhp file %s saved" % mhppath)
        
        
def writeMhpBones(fp, pb):
    b = pb.bone
    if pb.parent:
        string = "quat"
        mat = b.matrix_local.inverted() * b.parent.matrix_local * pb.parent.matrix.inverted() * pb.matrix
    else:
        string = "gquat"
        mat = pb.matrix.copy()
        maty = mat[1].copy()
        matz = mat[2].copy()
        mat[1] = matz
        mat[2] = -maty
    q = mat.to_quaternion()
    fp.write("%s\t%s\t%.4f\t%.4f\t%.4f\t%.4f\n" % (pb.name, string, q.w, q.x, q.y, q.z))
    for child in pb.children:
        writeMhpBones(fp, child)


def loadMhpFile(context, filepath):
    ob = context.object
    rig = ob.parent
    scn = context.scene
    if rig and rig.type == 'ARMATURE':
        (pname, ext) = os.path.splitext(filepath)
        mhppath = pname + ".mhp"
        
        fp = open(mhppath, "rU")
        for line in fp:
            words = line.split()
            if len(words) < 5:
                continue
            elif words[1] == "quat":
                q = Quaternion((float(words[2]), float(words[3]), float(words[4]), float(words[5])))
                mat = q.to_matrix().to_4x4()
                pb = rig.pose.bones[words[0]]
                pb.matrix_basis = mat
            elif words[1] == "gquat":
                q = Quaternion((float(words[2]), float(words[3]), float(words[4]), float(words[5])))
                mat = q.to_matrix().to_4x4()
                maty = mat[1].copy()
                matz = mat[2].copy()
                mat[1] = -matz
                mat[2] = maty
                pb = rig.pose.bones[words[0]]
                pb.matrix_basis = pb.bone.matrix_local.inverted() * mat
        fp.close()
        print("Mhp file %s loaded" % mhppath)
                
                

class VIEW3D_OT_LoadMhpButton(bpy.types.Operator):
    bl_idname = "mh.load_mhp"
    bl_label = "Load MHP File"
    bl_options = {'UNDO'}

    filename_ext = ".mhp"
    filter_glob = StringProperty(default="*.mhp", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for mhp file", 
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        loadMhpFile(context, self.properties.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class VIEW3D_OT_SaveasMhpFileButton(bpy.types.Operator, ExportHelper):
    bl_idname = "mh.saveas_mhp"
    bl_label = "Save MHP File"
    bl_options = {'UNDO'}

    filename_ext = ".mhp"
    filter_glob = StringProperty(default="*.mhp", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for mhp file", 
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        saveMhpFile(context, self.properties.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#----------------------------------------------------------
#   saveBvhFile(context, filepath):
#   loadBvhFile(context, filepath):
#----------------------------------------------------------

import io_anim_bvh
from io_anim_bvh import export_bvh, import_bvh

def saveBvhFile(context, filepath):
    ob = context.object
    rig = ob.parent
    scn = context.scene
    if rig and rig.type == 'ARMATURE': 
        roots = rigRoots(rig)
        if len(roots) > 1:
            raise NameError("Armature %s has multiple roots: %s" % (rig.name, roots))
        scn.objects.active = rig
        (pname, ext) = os.path.splitext(filepath)
        bvhpath = pname + ".bvh"
        
        export_bvh.write_armature(context, bvhpath,
           frame_start = scn.frame_current,
           frame_end = scn.frame_current,
           global_scale = 1.0,
           rotate_mode = scn.MhExportRotateMode,
           root_transform_only = True
           )    
        scn.objects.active = ob
        print("Saved %s" % bvhpath)
        return True
    else:
        return False


def rigRoots(rig):
    roots = []
    for bone in rig.data.bones:
        if not bone.parent:
            roots.append(bone.name)
    return roots
    
    
def loadBvhFile(context, filepath):
    ob = context.object
    rig = ob.parent
    scn = context.scene
    if rig and rig.type == 'ARMATURE':
        (pname, ext) = os.path.splitext(filepath)
        bvhpath = pname + ".bvh"

        bvh_nodes = import_bvh.read_bvh(context, bvhpath,
            rotate_mode=scn.MhImportRotateMode,
            global_scale=1.0)

        frame_orig = context.scene.frame_current

        bvh_name = bpy.path.display_name_from_filepath(bvhpath)

        import_bvh.bvh_node_dict2armature(context, bvh_name, bvh_nodes,
                               rotate_mode = scn.MhImportRotateMode,
                               frame_start = scn.frame_current,
                               IMPORT_LOOP = False,
                               global_matrix = rig.matrix_world,
                               )
        context.scene.frame_set(frame_orig)

        tmp = context.object
        bpy.ops.object.mode_set(mode='POSE')
        scn.objects.active = rig
        bpy.ops.object.mode_set(mode='POSE')
        copyPose(tmp, rig)
        scn.objects.active = ob
        scn.objects.unlink(tmp)
        del tmp
        print("Loaded %s" % bvhpath)
        return True
    else:
        return False


def copyPose(src, trg):
    for name,srcBone in src.pose.bones.items():
        trgBone = trg.pose.bones[srcBone.name]
        s = srcBone.matrix_basis
        t = trgBone.matrix_basis.copy()
        for i in range(3):
            for j in range(3):
                t[i][j] = s[i][j]
        trgBone.matrix_basis = t
        

class VIEW3D_OT_LoadBvhButton(bpy.types.Operator):
    bl_idname = "mh.load_bvh"
    bl_label = "Load BVH File"
    bl_options = {'UNDO'}

    filename_ext = ".bvh"
    filter_glob = StringProperty(default="*.bvh", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for bvh file", 
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        loadBvhFile(context, self.properties.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class VIEW3D_OT_SaveasBvhFileButton(bpy.types.Operator, ExportHelper):
    bl_idname = "mh.saveas_bvh"
    bl_label = "Save BVH File"
    bl_options = {'UNDO'}

    filename_ext = ".bvh"
    filter_glob = StringProperty(default="*.bvh", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for bvh file", 
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        saveBvhFile(context, self.properties.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#----------------------------------------------------------
#   Apply bvhs
#----------------------------------------------------------

def applyTargets(context):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    verts = evalVertLocations(ob)   
    utils.removeShapeKeys(ob)
    for prop in ob.keys():
        del ob[prop]
    for v in ob.data.vertices:
        v.co = verts[v.index]
    return
    

class VIEW3D_OT_ApplyTargetsButton(bpy.types.Operator):
    bl_idname = "mh.apply_targets"
    bl_label = "Apply Targets"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return (pollRelax(context) and not context.object.MhMeshVertsDeleted)

    def execute(self, context):
        if the.Confirm:
            the.Confirm = None
            applyTargets(context)
            print("All targets applied")
        else:
            the.Confirm = "mh.apply_targets"
            the.ConfirmString = "Apply all targets to mesh?"
            the.ConfirmString2 = None
        return{'FINISHED'}            

#----------------------------------------------------------
#   batch
#----------------------------------------------------------

def batchFixTargets(context, folder):
    print("Batch", folder)
    for fname in os.listdir(folder):
        (root, ext) = os.path.splitext(fname)
        file = os.path.join(folder, fname)        
        if os.path.isfile(file) and ext == ".target":
            print(file)            
            utils.loadTarget(file, context)        
            fitTarget(context)
            doSaveTarget(context, file)
            discardTarget(context)  
        elif os.path.isdir(file):
            batchFixTargets(context, file)
    return            

            
class VIEW3D_OT_BatchFixButton(bpy.types.Operator):
    bl_idname = "mh.batch_fix"
    bl_label = "Batch Fix Targets"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        global TargetSubPaths
        scn = context.scene
        if not the.Confirm:
            the.ConfirmString = "Really batch fix targets?"
            the.ConfirmString2 = None
            the.Confirm = "mh.batch_fix"
            return {'FINISHED'} 
        the.Confirm = None
        folder = os.path.realpath(os.path.expanduser(scn.MhTargetPath))
        batchFixTargets(context, folder)
        #for subfolder in TargetSubPaths:
        #    if scn["Mh%s" % subfolder]:
        #        batchFixTargets(context, os.path.join(folder, subfolder))
        print("All targets fixed")
        return {'FINISHED'}            
 
#----------------------------------------------------------
#   batch render
#----------------------------------------------------------

def batchRenderTargets(context, folder, opengl, outdir):
    print("Batch render", folder)
    for fname in os.listdir(folder):
        (root, ext) = os.path.splitext(fname)
        file = os.path.join(folder, fname)        
        if os.path.isfile(file) and ext == ".target":
            print(file)                    
            context.scene.render.filepath = os.path.join(outdir, root)
            utils.loadTarget(file, context)        
            if opengl:
                bpy.ops.render.opengl(animation=True)
            else:
                bpy.ops.render.render(animation=True)
            discardTarget(context)  
        elif os.path.isdir(file):
            batchRenderTargets(context, file, opengl, outdir)
    return            


class VIEW3D_OT_BatchRenderButton(bpy.types.Operator):
    bl_idname = "mh.batch_render"
    bl_label = "Batch Render"
    bl_options = {'UNDO'}
    opengl = BoolProperty()

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        global TargetSubPaths
        scn = context.scene
        folder = os.path.expanduser(scn.MhTargetPath)
        outdir = os.path.expanduser("~/makehuman/pictures/")        
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        scn.frame_start = 1
        scn.frame_end = 1
        for subfolder in TargetSubPaths:
            if scn["Mh%s" % subfolder]:
                batchRenderTargets(context, os.path.join(folder, subfolder), self.opengl, outdir)
        print("All targets rendered")
        return {'FINISHED'}            
        
#----------------------------------------------------------
#   relaxTarget(context):
#----------------------------------------------------------

def pollRelax(context):
     return (context.object and not context.object.MhRelaxing)

theNeighbors = {}
theOriginalMesh = {}
theRelaxedMesh = {}
        
def buildNeighbors(ob):
    global theNeighbors
    theNeighbors = {}
    for e in ob.data.edges:
        v0 = e.vertices[0]
        v1 = e.vertices[1]
        try:
            theNeighbors[v0].append(v1)
        except KeyError:
            theNeighbors[v0] = [v1]
        try:
            theNeighbors[v1].append(v0)
        except KeyError:
            theNeighbors[v1] = [v0]


def relaxSelected(context):
    global theNeighbors, theOriginalMesh, theRelaxedMesh
    ob = context.object
    if theNeighbors == {}:
        buildNeighbors(ob)

    theRelaxedMesh = {}  
    theOriginalMesh = {}
    verts = ob.active_shape_key.data
    for v in ob.data.vertices:
        if v.select:
            vn = v.index
            theRelaxedMesh[vn] = None   
            theOriginalMesh[vn] = verts[vn].co.copy()

    for vn in theRelaxedMesh.keys():
        lsum = Vector((0,0,0))
        for nn in theNeighbors[vn]:
            lsum += verts[nn].co
        theRelaxedMesh[vn] = lsum/len(theNeighbors[vn])
        
    updateRelaxedMesh(ob, ob.MhRelaxAmount)            

    
def updateRelaxedMesh(ob, value): 
    global theOriginalMesh, theRelaxedMesh
    bpy.ops.object.mode_set(mode='OBJECT')
    verts = ob.active_shape_key.data
    for vn in theRelaxedMesh.keys():
        verts[vn].co = (1-value)*theOriginalMesh[vn] + value*theRelaxedMesh[vn]
        if not ob.MhRelaxX:
            verts[vn].co[0] = theOriginalMesh[vn][0]
        if not ob.MhRelaxY:
            verts[vn].co[1] = theOriginalMesh[vn][1]
        if not ob.MhRelaxZ:
            verts[vn].co[2] = theOriginalMesh[vn][2]
        


class VIEW3D_OT_RelaxSelectedButton(bpy.types.Operator):
    bl_idname = "mh.relax_selected"
    bl_label = "Relax Selected"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        relaxSelected(context)
        context.object.MhRelaxing = True
        return{'FINISHED'}      
        
    
class VIEW3D_OT_CommitAndRelaxMoreButton(bpy.types.Operator):
    bl_idname = "mh.commit_and_relax_more"
    bl_label = "Commit And Relax More"
    bl_options = {'UNDO'}

    def execute(self, context):
        global theOriginalMesh, theRelaxedMesh
        ob = context.object
        updateRelaxedMesh(ob, ob.MhRelaxAmount)
        relaxSelected(context)
        ob.MhRelaxing = True
        return{'FINISHED'}      
        
    
class VIEW3D_OT_TestRelaxButton(bpy.types.Operator):
    bl_idname = "mh.test_relax"
    bl_label = "Test Relax"
    bl_options = {'UNDO'}

    def execute(self, context):
        ob = context.object
        updateRelaxedMesh(ob, ob.MhRelaxAmount)
        ob.MhRelaxing = True
        return{'FINISHED'}      
        
    
class VIEW3D_OT_DiscardRelaxButton(bpy.types.Operator):
    bl_idname = "mh.discard_relax"
    bl_label = "Discard Relax"

    def execute(self, context):
        global theOriginalMesh, theRelaxedMesh
        ob = context.object
        updateRelaxedMesh(ob, 0.0)
        theOriginalMesh = {}
        theRelaxedMesh = {}        
        ob.MhRelaxing = False
        return{'FINISHED'}      
        
    
class VIEW3D_OT_CommitRelaxButton(bpy.types.Operator):
    bl_idname = "mh.commit_relax"
    bl_label = "Commit Relax"

    def execute(self, context):
        global theOriginalMesh, theRelaxedMesh
        ob = context.object
        updateRelaxedMesh(ob, ob.MhRelaxAmount)
        theOriginalMesh = {}
        theRelaxedMesh = {}        
        ob.MhRelaxing = False
        return{'FINISHED'}              
    
#----------------------------------------------------------
#   fitTarget(context):
#----------------------------------------------------------

def fitTarget(context):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    scn = context.scene
    if not utils.isTarget(ob):
        return
    ob.active_shape_key_index = ob["NTargets"]
    if not checkValid(ob):
        return
    if not the.Proxy:
        path = ob["ProxyFile"]
        if path:
            print("Rereading %s" % path)
            the.Proxy = proxy.CProxy()
            the.Proxy.read(path)
        else:
            raise NameError("Object %s has no associated mhclo file. Cannot fit" % ob.name)
            return
    #print(the.Proxy)
    if ob.MhAffectOnly != 'All':
        first,last = AffectedVerts[ob.MhAffectOnly]
        the.Proxy.update(ob.active_shape_key.data, ob.active_shape_key.data, skipBefore=first, skipAfter=last)
    else:
        the.Proxy.update(ob.active_shape_key.data, ob.active_shape_key.data)
    return


class VIEW3D_OT_FitTargetButton(bpy.types.Operator):
    bl_idname = "mh.fit_target"
    bl_label = "Fit Target"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return (pollRelax(context) and not context.object.MhMeshVertsDeleted)

    def execute(self, context):
        fitTarget(context)
        return{'FINISHED'}      
        
#----------------------------------------------------------
#   discardTarget(context):
#----------------------------------------------------------

def discardTarget(context):
    ob = context.object
    if not utils.isTarget(ob):
        return
    bpy.ops.object.mode_set(mode='OBJECT')
    ob.active_shape_key_index = ob["NTargets"]
    bpy.ops.object.shape_key_remove()
    ob["NTargets"] -= 1
    ob.active_shape_key_index = ob["NTargets"]
    checkValid(ob)
    return

    
def discardAllTargets(context):
    ob = context.object
    while utils.isTarget(ob):
        discardTarget(context)
    return
    
    
def checkValid(ob):
    nShapes = utils.shapeKeyLen(ob)
    if nShapes != ob["NTargets"]+1:
        print("Consistency problem:\n  %d shapes, %d targets" % (nShapes, ob["NTargets"]))
        return False
    return True


class VIEW3D_OT_DiscardTargetButton(bpy.types.Operator):
    bl_idname = "mh.discard_target"
    bl_label = "Discard Target"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        discardTarget(context)
        """
        if the.Confirm:        
            the.Confirm = None
            discardTarget(context)
        else:
            the.Confirm = "mh.discard_target"
            the.ConfirmString = "Really discard target?"
            the.ConfirmString2 = None
        """            
        return{'FINISHED'}                


class VIEW3D_OT_DiscardAllTargetsButton(bpy.types.Operator):
    bl_idname = "mh.discard_all_targets"
    bl_label = "Discard All Targets"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        if the.Confirm:        
            the.Confirm = None
            discardAllTargets(context)
        else:
            the.Confirm = "mh.discard_all_targets"
            the.ConfirmString = "Really discard all targets?"
            the.ConfirmString2 = None
        return{'FINISHED'}                

#----------------------------------------------------------
# symmetrizeTarget(context, left2right, mirror):
#----------------------------------------------------------

def symmetrizeTarget(context, left2right, mirror):
    utils.setupVertexPairs(context, False)
    ob = context.object
    scn = context.scene
    if not utils.isTarget(ob):
        return
    bpy.ops.object.mode_set(mode='OBJECT')
    verts = ob.active_shape_key.data
    
    for vn in the.Mid.keys():
        v = verts[vn]
        v.co[0] = 0
        
    for (lvn,rvn) in the.Left.items():
        lv = verts[lvn].co
        rv = verts[rvn].co
        if mirror:
            tv = rv.copy()
            verts[rvn].co = (-lv[0], lv[1], lv[2])
            verts[lvn].co = (-tv[0], tv[1], tv[2])
        elif left2right:
            rv[0] = -lv[0]
            rv[1] = lv[1]
            rv[2] = lv[2]
        else:
            lv[0] = -rv[0]
            lv[1] = rv[1]
            lv[2] = rv[2]

    bverts = ob.data.vertices    
    selected = {}
    for v in bverts:
        selected[v.index] = v.select

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
        
    for vn in the.Mid.keys():
        bverts[vn].select = selected[vn]

    for (lvn,rvn) in the.Left.items():
        if mirror:
            bverts[lvn].select = selected[rvn]
            bverts[rvn].select = selected[lvn]
        elif left2right:
            bverts[lvn].select = selected[lvn]
            bverts[rvn].select = selected[lvn]
        else:
            bverts[lvn].select = selected[rvn]
            bverts[rvn].select = selected[rvn]

    print("Target symmetrized")
    return


class VIEW3D_OT_SymmetrizeTargetButton(bpy.types.Operator):
    bl_idname = "mh.symmetrize_target"
    bl_label = "Symmetrize"
    bl_options = {'UNDO'}
    action = StringProperty()

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        
        symmetrizeTarget(context, (self.action=="Right"), (self.action=="Mirror"))
        return{'FINISHED'}                
                        
#----------------------------------------------------------
#   Snapping
#----------------------------------------------------------

SkirtWaist =   [15340, 15341, 15736, 15737, 15738, 15739, 15740, 15741, 15742, 15743, 15744, 15745, 15746, 15747, 15748, 15749, 15750, 15751, 15752, 15753, 15754, 15755, ]
TightsWaist =  [16893, 16898, 17824, 17825, 17826, 17827, 17828, 17829, 17830, 17831, 17832, 17833, 17834, 17849, 17864, 17879, 17915, 17916, 17917, 18091, 18096, 18475, ]


XYSkirtColumns = [
  [15340, 15383, 15384, 15427, 15428, 15471, 15472, 15515, 15516, 15559, 15560, 15603, 15604, 15647, 15648, 15691, 15692, 15735, ],
  [15754, 15757, 15794, 15797, 15834, 15837, 15874, 15877, 15914, 15917, 15954, 15957, 15994, 15997, 16034, 16037, 16074, 16077, ],
  [15738, 15773, 15778, 15813, 15818, 15853, 15858, 15893, 15898, 15933, 15938, 15973, 15978, 16013, 16018, 16053, 16058, 16093, ],
  [15737, 15774, 15777, 15814, 15817, 15854, 15857, 15894, 15897, 15934, 15937, 15974, 15977, 16014, 16017, 16054, 16057, 16094, ],
  [15736, 15775, 15776, 15815, 15816, 15855, 15856, 15895, 15896, 15935, 15936, 15975, 15976, 16015, 16016, 16055, 16056, 16095, ],
  [15746, 15765, 15786, 15805, 15826, 15845, 15866, 15885, 15906, 15925, 15946, 15965, 15986, 16005, 16026, 16045, 16066, 16085, ],
  [15740, 15771, 15780, 15811, 15820, 15851, 15860, 15891, 15900, 15931, 15940, 15971, 15980, 16011, 16020, 16051, 16060, 16091, ],
  [15745, 15766, 15785, 15806, 15825, 15846, 15865, 15886, 15905, 15926, 15945, 15966, 15985, 16006, 16025, 16046, 16065, 16086, ],
  [15739, 15772, 15779, 15812, 15819, 15852, 15859, 15892, 15899, 15932, 15939, 15972, 15979, 16012, 16019, 16052, 16059, 16092, ],

  [15741, 15770, 15781, 15810, 15821, 15850, 15861, 15890, 15901, 15930, 15941, 15970, 15981, 16010, 16021, 16050, 16061, 16090, ],
  [15742, 15769, 15782, 15809, 15822, 15849, 15862, 15889, 15902, 15929, 15942, 15969, 15982, 16009, 16022, 16049, 16062, 16089, ],
  [15748, 15763, 15788, 15803, 15828, 15843, 15868, 15883, 15908, 15923, 15948, 15963, 15988, 16003, 16028, 16043, 16068, 16083, ],
  [15747, 15764, 15787, 15804, 15827, 15844, 15867, 15884, 15907, 15924, 15947, 15964, 15987, 16004, 16027, 16044, 16067, 16084, ],
  [15743, 15768, 15783, 15808, 15823, 15848, 15863, 15888, 15903, 15928, 15943, 15968, 15983, 16008, 16023, 16048, 16063, 16088, ],
  [15749, 15762, 15789, 15802, 15829, 15842, 15869, 15882, 15909, 15922, 15949, 15962, 15989, 16002, 16029, 16042, 16069, 16082, ],
  [15744, 15767, 15784, 15807, 15824, 15847, 15864, 15887, 15904, 15927, 15944, 15967, 15984, 16007, 16024, 16047, 16064, 16087, ],
  [15755, 15756, 15795, 15796, 15835, 15836, 15875, 15876, 15915, 15916, 15955, 15956, 15995, 15996, 16035, 16036, 16075, 16076, ],

  [15750, 15761, 15790, 15801, 15830, 15841, 15870, 15881, 15910, 15921, 15950, 15961, 15990, 16001, 16030, 16041, 16070, 16081, ],
  [15751, 15760, 15791, 15800, 15831, 15840, 15871, 15880, 15911, 15920, 15951, 15960, 15991, 16000, 16031, 16040, 16071, 16080, ],
  [15752, 15759, 15792, 15799, 15832, 15839, 15872, 15879, 15912, 15919, 15952, 15959, 15992, 15999, 16032, 16039, 16072, 16079, ],
  [15753, 15758, 15793, 15798, 15833, 15838, 15873, 15878, 15913, 15918, 15953, 15958, 15993, 15998, 16033, 16038, 16073, 16078, ],
  [15341, 15382, 15385, 15426, 15429, 15470, 15473, 15514, 15517, 15558, 15561, 15602, 15605, 15646, 15649, 15690, 15693, 15734, ],
]  

ZSkirtRows = [
  [15472, 15473, 15856, 15857, 15858, 15859, 15860, 15861, 15862, 15863, 15864, 15865, 15866, 15867, 15868, 15869, 15870, 15871, 15872, 15873, 15874, 15875, ],
  [15514, 15515, 15876, 15877, 15878, 15879, 15880, 15881, 15882, 15883, 15884, 15885, 15886, 15887, 15888, 15889, 15890, 15891, 15892, 15893, 15894, 15895, ],
  [15516, 15517, 15896, 15897, 15898, 15899, 15900, 15901, 15902, 15903, 15904, 15905, 15906, 15907, 15908, 15909, 15910, 15911, 15912, 15913, 15914, 15915, ],
  [15558, 15559, 15916, 15917, 15918, 15919, 15920, 15921, 15922, 15923, 15924, 15925, 15926, 15927, 15928, 15929, 15930, 15931, 15932, 15933, 15934, 15935, ],
  [15560, 15561, 15936, 15937, 15938, 15939, 15940, 15941, 15942, 15943, 15944, 15945, 15946, 15947, 15948, 15949, 15950, 15951, 15952, 15953, 15954, 15955, ],
  [15602, 15603, 15956, 15957, 15958, 15959, 15960, 15961, 15962, 15963, 15964, 15965, 15966, 15967, 15968, 15969, 15970, 15971, 15972, 15973, 15974, 15975, ],
  [15604, 15605, 15976, 15977, 15978, 15979, 15980, 15981, 15982, 15983, 15984, 15985, 15986, 15987, 15988, 15989, 15990, 15991, 15992, 15993, 15994, 15995, ],
  [15646, 15647, 15996, 15997, 15998, 15999, 16000, 16001, 16002, 16003, 16004, 16005, 16006, 16007, 16008, 16009, 16010, 16011, 16012, 16013, 16014, 16015, ],
  [15648, 15649, 16016, 16017, 16018, 16019, 16020, 16021, 16022, 16023, 16024, 16025, 16026, 16027, 16028, 16029, 16030, 16031, 16032, 16033, 16034, 16035, ],
  [15690, 15691, 16036, 16037, 16038, 16039, 16040, 16041, 16042, 16043, 16044, 16045, 16046, 16047, 16048, 16049, 16050, 16051, 16052, 16053, 16054, 16055, ],
  [15692, 15693, 16056, 16057, 16058, 16059, 16060, 16061, 16062, 16063, 16064, 16065, 16066, 16067, 16068, 16069, 16070, 16071, 16072, 16073, 16074, 16075, ],
  [15734, 15735, 16076, 16077, 16078, 16079, 16080, 16081, 16082, 16083, 16084, 16085, 16086, 16087, 16088, 16089, 16090, 16091, 16092, 16093, 16094, 16095, ],
]


class VIEW3D_OT_SnapWaistButton(bpy.types.Operator):
    bl_idname = "mh.snap_waist"
    bl_label = "Snap Skirt Waist"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        ob = context.object
        bpy.ops.object.mode_set(mode='OBJECT')
        nVerts = len(SkirtWaist)
        if len(TightsWaist) != nVerts:
            halt
        skey = ob.data.shape_keys.key_blocks[-1]
        verts = skey.data
        for n in range(nVerts):
            verts[SkirtWaist[n]].co = verts[TightsWaist[n]].co
        bpy.ops.object.mode_set(mode='EDIT')
        return{'FINISHED'}            


class VIEW3D_OT_StraightenSkirtButton(bpy.types.Operator):
    bl_idname = "mh.straighten_skirt"
    bl_label = "Straighten Skirt Columns"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        ob = context.object
        bpy.ops.object.mode_set(mode='OBJECT')
        skey = ob.data.shape_keys.key_blocks[-1]
        verts = skey.data

        for col in XYSkirtColumns:
            xsum = 0.0
            ysum = 0.0
            for vn in col:
                xsum += verts[vn].co[0]
                ysum += verts[vn].co[1]
            x = xsum/len(col)
            y = ysum/len(col)
            print("xy col", x, y)
            for vn in col:
                verts[vn].co[0] = x
                verts[vn].co[1] = y
                
        for row in ZSkirtRows:
            zsum = 0.0
            for vn in row:
                zsum += verts[vn].co[2]
            z = zsum/len(row)
            print("z row", z)
            for vn in row:
                verts[vn].co[2] = z
                
        bpy.ops.object.mode_set(mode='EDIT')
        return{'FINISHED'}            


#----------------------------------------------------------
#   Skip
#----------------------------------------------------------

def fixInconsistency(context):
    ob = context.object
    if ob.data.shape_keys:
        ob["NTargets"] = len(ob.data.shape_keys.key_blocks)
    else:
        ob.shape_key_add(name="Basis")
        ob["NTargets"] = 0

class VIEW3D_OT_FixInconsistencyButton(bpy.types.Operator):
    bl_idname = "mh.fix_inconsistency"
    bl_label = "Fix It!"
    bl_options = {'UNDO'}

    def execute(self, context):
        fixInconsistency(context)
        return{'FINISHED'}            

class VIEW3D_OT_SkipButton(bpy.types.Operator):
    bl_idname = "mh.skip"
    bl_label = "No"
    bl_options = {'UNDO'}

    def execute(self, context):
        utils.skipConfirm()
        return{'FINISHED'}           

#----------------------------------------------------------
#   Convert weights
#----------------------------------------------------------

def readWeights(filepath, nVerts):
    weights = {}
    for n in range(nVerts):
        weights[n] = []
    bone = None
    fp = open(filepath, "rU")
    for line in fp:
        words = line.split()
        if len(words) < 2:
            pass
        elif words[0] == "#":
            if words[1] == "weights":
                bone = words[2]
            else:
                bone = None
        elif bone:
            vn = int(words[0])
            if vn < the.NBodyVerts:
                weights[vn].append( (bone, float(words[1])) )
    fp.close()           
    
    normedWeights = {}
    for vn,data in weights.items():
        wsum = 0.0
        for bone,w in data:
            wsum += w
        ndata = []
        for bone,w in data:
            ndata.append((bone,w/wsum))
        normedWeights[vn] = ndata

    return normedWeights            


def defineMatrices(rig):
    mats = {}
    for pb in rig.pose.bones:
        mats[pb.name] = pb.matrix * pb.bone.matrix_local.inverted()
    return mats
        

def getPoseLocs(mats, restLocs, weights, nVerts):
    locs = {}
    for n in range(nVerts):
        if weights[n]:
            mat = getMatrix(mats, weights[n])
            locs[n] = mat * restLocs[n]
        else:
            locs[n] = restLocs[n]
    return locs
    
    
def getRestLocs(mats, poseLocs, weights, nVerts):
    locs = {}
    for n in range(nVerts):
        if weights[n]:
            mat = getMatrix(mats, weights[n])
            locs[n] = mat.inverted() * poseLocs[n]
        else:
            locs[n] = poseLocs[n]
    return locs
    
    
def getMatrix(mats, weight):        
    mat = Matrix()
    mat.zero()
    for bname,w in weight:
        mat += w * mats[bname]
    return mat


def getShapeLocs(ob, nVerts):
    locs = {}
    filename = "test"
    for n in range(nVerts):
        locs[n] = Vector((0,0,0))
    for skey in ob.data.shape_keys.key_blocks:
        if skey.name == "Basis":
            continue       
        filename = skey.name
        for n,v in enumerate(skey.data):
            bv = ob.data.vertices[n]
            vec = v.co - bv.co
            locs[n] += skey.value*vec
    return locs, filename
    
    
def addLocs(locs1, locs2, nVerts):
    locs = {}
    for n in range(nVerts):
        locs[n] = locs1[n] + locs2[n]
    return locs


def subLocs(locs1, locs2, nVerts):
    locs = {}
    for n in range(nVerts):
        locs[n] = locs1[n] - locs2[n]
    return locs


def saveNewTarget(filepath, locs, nVerts):
    fp = open(filepath, "w")
    locList = list(locs.items())
    locList.sort()
    for (n, dr) in locList:
        if dr.length > 1e-4:
            fp.write("%d %.5f %.5f %.5f\n" % (n, dr[0], dr[2], -dr[1]))
    fp.close()
    return
        

class VIEW3D_OT_ConvertRigButton(bpy.types.Operator):
    bl_idname = "mh.convert_rig"
    bl_label = "Convert to rig"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        scn = context.scene
        ob = context.object
        rig = ob.parent
        nVerts = len(ob.data.vertices)
        oldWeights = readWeights(os.path.join(scn.MhProgramPath, "data/rigs", scn.MhSourceRig+".rig"), nVerts)
        newWeights = readWeights(os.path.join(scn.MhProgramPath, "data/rigs",scn.MhTargetRig+".rig"), nVerts)
        mats = defineMatrices(rig)
        restLocs = {}
        for n in range(nVerts):
            restLocs[n] = ob.data.vertices[n].co
        oldShapeDiffs, filename = getShapeLocs(ob, nVerts)
        oldRestLocs = addLocs(restLocs, oldShapeDiffs, nVerts)
        globalLocs = getPoseLocs(mats, oldRestLocs, oldWeights, nVerts)
        newRestLocs = getRestLocs(mats, globalLocs, newWeights, nVerts)
        newShapeDiffs = subLocs(newRestLocs, restLocs, nVerts)
        saveNewTarget(os.path.join(scn.MhProgramPath, "data/poses", scn.MhPoseTargetDir, filename + ".target"), newShapeDiffs, nVerts)

        for vn in [3815,3821,4378]: #,,13288]: #, , 13288]:
            print("\nv", vn, ob.data.vertices[vn].co)
            print("  os", oldShapeDiffs[vn])
            print("  or", oldRestLocs[vn])
            print("  gl", globalLocs[vn])
            print("  nr", newRestLocs[vn])            
            print("  ns", newShapeDiffs[vn])            
            for bone,w in oldWeights[vn]:
                print("   ", bone, w)
            for bone,w in newWeights[vn]:
                print("   ", bone, w)

        return{'FINISHED'}           

#----------------------------------------------------------
#   Init
#----------------------------------------------------------

def init():
    bpy.types.Object.MhRelaxAmount = FloatProperty(name="Relax amount", description="0 = original mesh, 1 = fully relaxed mesh", default = 0.5, min=0.0, max=2.0)
    bpy.types.Object.MhRelaxing = BoolProperty(default = False)
    bpy.types.Object.MhRelaxX = BoolProperty(name="Relax X", description="Relaxing affects X coordinate", default = True)
    bpy.types.Object.MhRelaxY = BoolProperty(name="Relax Y", description="Relaxing affects Y coordinate", default = True)
    bpy.types.Object.MhRelaxZ = BoolProperty(name="Relax Z", description="Relaxing affects Z coordinate", default = True)
    
    bpy.types.Scene.MhUnlock = BoolProperty(default = False)
    
    bpy.types.Object.MhPruneWholeDir = BoolProperty(name="Prune Entire Directory", default = False)
    bpy.types.Object.MhPruneEnabled = BoolProperty(name="Pruning Enabled", default = False)
    bpy.types.Object.MhPruneRecursively = BoolProperty(name="Prune Folders Recursively", default = False)

    bpy.types.Scene.MhSourceRig = StringProperty(default = "rigid")
    bpy.types.Scene.MhTargetRig = StringProperty(default = "soft1")
    bpy.types.Scene.MhPoseTargetDir = StringProperty(default = "dance1-soft1")
    
    #bpy.types.Object.MhTightsOnly = BoolProperty(default = False)
    #bpy.types.Object.MhSkirtOnly = BoolProperty(default = False)
                 
    bpy.types.Object.MhAffectOnly = EnumProperty(
        items = [('Body','Body','Body'),
                 ('Skirt','Skirt','Skirt'),
                 ('Tights','Tights','Tights'),
                 ('All','All','All')],
    default='All')
    
    bpy.types.Object.MhIrrelevantDeleted = BoolProperty(name="Irrelevant deleted", default = False)
    bpy.types.Object.MhMeshVertsDeleted = BoolProperty(name="Cannot load", default = False)

    bpy.types.Object.SelectedOnly = BoolProperty(name="Selected verts only", default = True)
    bpy.types.Object.MhZeroOtherTargets = BoolProperty(name="Only save active target", description="Set values of all other targets to 0", default = True)

    bpy.types.Scene.MhImportRotateMode = EnumProperty(
            name="Rotation",
            description="Rotation conversion",
            items=(('QUATERNION', "Quaternion",
                    "Convert rotations to quaternions"),
                   ('NATIVE', "Euler (Native)", ("Use the rotation order "
                                                 "defined in the BVH file")),
                   ('XYZ', "Euler (XYZ)", "Convert rotations to euler XYZ"),
                   ('XZY', "Euler (XZY)", "Convert rotations to euler XZY"),
                   ('YXZ', "Euler (YXZ)", "Convert rotations to euler YXZ"),
                   ('YZX', "Euler (YZX)", "Convert rotations to euler YZX"),
                   ('ZXY', "Euler (ZXY)", "Convert rotations to euler ZXY"),
                   ('ZYX', "Euler (ZYX)", "Convert rotations to euler ZYX"),
                   ),
            default='NATIVE',
            )

    bpy.types.Scene.MhExportRotateMode = EnumProperty(
            name="Rotation",
            description="Rotation conversion",
            items=(('NATIVE', "Euler (Native)",
                    "Use the rotation order defined in the BVH file"),
                   ('XYZ', "Euler (XYZ)", "Convert rotations to euler XYZ"),
                   ('XZY', "Euler (XZY)", "Convert rotations to euler XZY"),
                   ('YXZ', "Euler (YXZ)", "Convert rotations to euler YXZ"),
                   ('YZX', "Euler (YZX)", "Convert rotations to euler YZX"),
                   ('ZXY', "Euler (ZXY)", "Convert rotations to euler ZXY"),
                   ('ZYX', "Euler (ZYX)", "Convert rotations to euler ZYX"),
                   ),
            default='ZYX',
            )
    
    return


def initBatch():
    global TargetSubPaths
    TargetSubPaths = []
    folder = os.path.realpath(os.path.expanduser(scn.MhTargetPath))
    for fname in os.listdir(folder):
        file = os.path.join(folder, fname)        
        if os.path.isdir(file) and fname[0] != ".":
            TargetSubPaths.append(fname)
            expr = 'bpy.types.Scene.Mh%s = BoolProperty(name="%s")' % (fname,fname)
            exec(expr)
            scn["Mh%s" % fname] = False
    return  

    
def isInited(scn):
    return True
    try:
        TargetSubPaths
        scn.MhTargetPath
        return True
    except:
        return False    
        

class VIEW3D_OT_InitButton(bpy.types.Operator):
    bl_idname = "mh.init"
    bl_label = "Initialize"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return pollRelax(context)

    def execute(self, context):
        initScene(context.scene)
        return{'FINISHED'}                

