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
from mathutils import Vector
from bpy.props import *
from bpy_extras.io_utils import ExportHelper, ImportHelper

from . import globvars as the
from . import proxy
from . import import_obj


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
            deleteAll(context)
        the.Proxy = proxy.CProxy()
        filepath = os.path.join(context.scene.MhProgramPath, "data/3dobjs/base.mhclo")
        the.Proxy.read(filepath)
        ob = import_obj.importObj(the.Proxy.obj_file, context)
        ob["NTargets"] = 0
        ob["ProxyFile"] = filepath
        ob["ObjFile"] = the.Proxy.obj_file
        ob["MhxMesh"] = True
        setupVertexPairs(context, True)
        print("Base object imported")
        print(the.Proxy)
        return{'FINISHED'}    


class VIEW3D_OT_ImportBaseObjButton(bpy.types.Operator):
    bl_idname = "mh.import_base_obj"
    bl_label = "Obj"
    bl_options = {'UNDO'}
    delete = BoolProperty()

    def execute(self, context):
        if self.delete:
            deleteAll(context)
        the.Proxy = None
        filepath = os.path.join(context.scene.MhProgramPath, "data/3dobjs/base.obj")
        ob = import_obj.importObj(filepath, context)
        ob["NTargets"] = 0
        ob["ProxyFile"] = 0
        ob["ObjFile"] =  filepath
        ob["MhxMesh"] = True
        setupVertexPairs(context, True)
        print("Base object imported")
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
        removeShapeKeys(ob)
        ob.shape_key_add(name="Basis")
        ob["NTargets"] = 0
        ob["ProxyFile"] = 0
        ob["ObjFile"] =  0
        ob["MhxMesh"] = True        
        setupVertexPairs(context, True)
        return{'FINISHED'}    


class VIEW3D_OT_DeleteHelpersButton(bpy.types.Operator):
    bl_idname = "mh.delete_clothes"
    bl_label = "Delete Clothes Helpers"
    bl_options = {'UNDO'}

    def execute(self, context):
        ob = context.object
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        nverts = len(ob.data.vertices)
        for n in range(the.NBodyVerts):
            ob.data.vertices[n].select = False
        for n in range(the.NBodyVerts,nverts):
            ob.data.vertices[n].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set(mode='OBJECT')
        return{'FINISHED'}    


#----------------------------------------------------------
#   setupVertexPairs(ob, insist):
#----------------------------------------------------------

Left = {}
Right = {}
Mid = {}

def setupVertexPairs(context, insist):
    global Left, Right, Mid
    if Left.keys() and not insist:
        print("Vertex pair already set up")
        return
    ob = context.object
    verts = []
    for v in ob.data.vertices:
        x = v.co[0]
        y = v.co[1]
        z = v.co[2]
        verts.append((z,y,x,v.index))
    verts.sort()        
    Left = {}
    Right = {}
    Mid = {}
    nmax = len(verts)
    notfound = []
    for n,data in enumerate(verts):
        (z,y,x,vn) = data
        n1 = n - 20
        n2 = n + 20
        if n1 < 0: n1 = 0
        if n2 >= nmax: n2 = nmax
        vmir = findVert(verts[n1:n2], vn, -x, y, z, notfound)
        if vmir < 0:
            Mid[vn] = vn
        elif x > the.Epsilon:
            Left[vn] = vmir
        elif x < -the.Epsilon:
            Right[vn] = vmir
        else:
            Mid[vn] = vmir
    if notfound:            
        print("Did not find mirror image for vertices:")
        for msg in notfound:
            print(msg)
    print("Left-right-mid", len(Left.keys()), len(Right.keys()), len(Mid.keys()))
    return
    

def findVert(verts, v, x, y, z, notfound):
    for (z1,y1,x1,v1) in verts:
        dx = x-x1
        dy = y-y1
        dz = z-z1
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < the.Epsilon:
            return v1
    if abs(x) > the.Epsilon:            
        notfound.append("  %d at (%.4f %.4f %.4f)" % (v, x, y, z))
    return -1            

#----------------------------------------------------------
#   loadTarget(filepath, context):
#----------------------------------------------------------

def loadTarget(filepath, context):
    realpath = os.path.realpath(os.path.expanduser(filepath))
    fp = open(realpath, "rU")  
    #print("Loading target %s" % realpath)

    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    for v in ob.data.vertices:
        v.select = False
    name = the.nameFromPath(filepath)
    skey = ob.shape_key_add(name=name, from_mix=False)
    ob.active_shape_key_index = shapeKeyLen(ob) - 1
    #bpy.ops.object.shape_key_add(from_mix=False)
    #skey = ob.active_shape_key
    skey.name = name
    #print("Active", ob.active_shape_key.name)
    nverts = len(ob.data.vertices)
    for line in fp:
        words = line.split()
        if len(words) == 0:
            pass
        else:
            index = int(words[0])
            if index >= nverts:
                print("Stopped loading at index %d" % index)
                break
            dx = float(words[1])
            dy = float(words[2])
            dz = float(words[3])
            #vec = ob.data.vertices[index].co
            vec = skey.data[index].co
            vec[0] += dx
            vec[1] += -dz
            vec[2] += dy
            ob.data.vertices[index].select = True
    fp.close()     
    skey.slider_min = -1.0
    skey.slider_max = 1.0
    skey.value = 1.0
    ob.show_only_shape_key = False
    ob.use_shape_key_edit_mode = True
    ob["NTargets"] += 1
    ob["FilePath"] = realpath
    ob["SelectedOnly"] = False
    return skey


def shapeKeyLen(ob):
    n = 0
    for skey in ob.data.shape_keys.key_blocks:
        n += 1
    return n


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

    def execute(self, context):
        loadTarget(self.properties.filepath, context)
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
    if not isBaseOrTarget(ob):
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
    ob.active_shape_key_index = shapeKeyLen(ob) - 1
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
    ob["SelectedOnly"] = False
    scn.objects.unlink(trg)
    return


class VIEW3D_OT_LoadTargetFromMeshButton(bpy.types.Operator):
    bl_idname = "mh.load_target_from_mesh"
    bl_label = "Load Target From Mesh"
    bl_options = {'UNDO'}

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
    ob.active_shape_key_index = shapeKeyLen(ob) - 1
    skey.slider_min = -1.0
    skey.slider_max = 1.0
    skey.value = 1.0
    ob.show_only_shape_key = False
    ob.use_shape_key_edit_mode = True
    ob["NTargets"] += 1
    ob["FilePath"] = 0
    ob["SelectedOnly"] = False
    return


class VIEW3D_OT_NewTargetButton(bpy.types.Operator):
    bl_idname = "mh.new_target"
    bl_label = "New Target"
    bl_options = {'UNDO'}

    def execute(self, context):
        newTarget(context)
        return {'FINISHED'}

#----------------------------------------------------------
#   saveTarget(context):
#----------------------------------------------------------
    
def doSaveTarget(ob, filepath):    
    if not isTarget(ob):
        raise NameError("%s is not a target")
    bpy.ops.object.mode_set(mode='OBJECT')
    ob.active_shape_key_index = ob["NTargets"]
    if not checkValid(ob):
        return
    saveAll = not ob["SelectedOnly"]
    skey = ob.active_shape_key    
    if skey.name[0:6] == "Target":
        skey.name = the.nameFromPath(filepath)
    verts = evalVertLocations(ob)
    
    (fname,ext) = os.path.splitext(filepath)
    filepath = fname + ".target"
    fp = open(filepath, "w")  
    print("Saving target %s to %s" % (ob, filepath))
    for n,vco in verts.items():
        bv = ob.data.vertices[n]
        vec = vco - bv.co
        if vec.length > the.Epsilon and (saveAll or bv.select):
            fp.write("%d %.6f %.6f %.6f\n" % (n, vec[0], vec[2], -vec[1]))
    fp.close()    
    ob["FilePath"] = filepath
    return

       
def evalVertLocations(ob):    
    verts = {}
    for v in ob.data.vertices:
        verts[v.index] = v.co.copy()
    for skey in ob.data.shape_keys.key_blocks:
        if skey.name == "Basis":
            continue       
        for n,v in enumerate(skey.data):
            bv = ob.data.vertices[n]
            vec = v.co - bv.co
            verts[n] += skey.value*vec
    return verts            

       
class VIEW3D_OT_SaveTargetButton(bpy.types.Operator):
    bl_idname = "mh.save_target"
    bl_label = "Save Target"
    bl_options = {'UNDO'}

    def execute(self, context):
        ob = context.object
        path = ob["FilePath"]
        if the.Confirm:
            the.Confirm = None
            doSaveTarget(ob, path)
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

    def execute(self, context):
        doSaveTarget(context.object, self.properties.filepath)
        print("Target saved")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#----------------------------------------------------------
#   Apply targets
#----------------------------------------------------------

def applyTargets(context):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    verts = evalVertLocations(ob)   
    removeShapeKeys(ob)
    for prop in ob.keys():
        del ob[prop]
    for v in ob.data.vertices:
        v.co = verts[v.index]
    return
    

def removeShapeKeys(ob):    
    if not ob.data.shape_keys:
        return
    skeys = ob.data.shape_keys.key_blocks
    n = len(skeys)
    while n >= 0:
        ob.active_shape_key_index = n
        bpy.ops.object.shape_key_remove()
        n -= 1
    return        


class VIEW3D_OT_ApplyTargetsButton(bpy.types.Operator):
    bl_idname = "mh.apply_targets"
    bl_label = "Apply Targets"
    bl_options = {'UNDO'}

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
            loadTarget(file, context)        
            fitTarget(context)
            doSaveTarget(context.object, file)
            discardTarget(context)  
        elif os.path.isdir(file):
            batchFixTargets(context, file)
    return            

            
class VIEW3D_OT_BatchFixButton(bpy.types.Operator):
    bl_idname = "mh.batch_fix"
    bl_label = "Batch Fix Targets"
    bl_options = {'UNDO'}

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
            loadTarget(file, context)        
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

def relaxTarget(context):
    ob = context.object
    skey = ob.active_shape_key
    if not skey:
        print("No active shapekey")
        return
    relaxMesh(skey.data, ob.data.edges, the.NBodyVerts, context.scene["Relax"])


def relaxMesh(verts, edges, first, k):
    neighbors = {}
    for e in edges:
        v0 = e.vertices[0]
        v1 = e.vertices[1]
        if v0 >= first:
            try:
                neighbors[v0].append(v1)
            except:
                neighbors[v0] = [v1]
            try:
                neighbors[v1].append(v0)
            except:
                neighbors[v1] = [v0]
    average = {}                
    for v0 in neighbors.keys():
        sum = Vector((0,0,0))
        n = 0
        for vn in neighbors[v0]:
            sum += verts[vn].co
            n += 1
        average[v0] = sum/n            
    for v in neighbors.keys():
        verts[v].co = (1-k)*verts[v].co + k*average[v]
    return

    
class VIEW3D_OT_RelaxTargetButton(bpy.types.Operator):
    bl_idname = "mh.relax_target"
    bl_label = "Relax Target"
    bl_options = {'UNDO'}

    def execute(self, context):
        relaxTarget(context)
        return{'FINISHED'}      
        
    
#----------------------------------------------------------
#   fitTarget(context):
#----------------------------------------------------------

def fitTarget(context):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    scn = context.scene
    if not isTarget(ob):
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
    the.Proxy.update(ob.active_shape_key.data, ob.data.vertices)
    return


class VIEW3D_OT_FitTargetButton(bpy.types.Operator):
    bl_idname = "mh.fit_target"
    bl_label = "Fit Target"
    bl_options = {'UNDO'}

    def execute(self, context):
        fitTarget(context)
        return{'FINISHED'}      
        
#----------------------------------------------------------
#   discardTarget(context):
#----------------------------------------------------------

def discardTarget(context):
    ob = context.object
    if not isTarget(ob):
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
    while isTarget(ob):
        discardTarget(context)
    return
    
    
def checkValid(ob):
    nShapes = shapeKeyLen(ob)
    if nShapes != ob["NTargets"]+1:
        print("Consistency problem:\n  %d shapes, %d targets" % (nShapes, ob["NTargets"]))
        return False
    return True


class VIEW3D_OT_DiscardTargetButton(bpy.types.Operator):
    bl_idname = "mh.discard_target"
    bl_label = "Discard Target"
    bl_options = {'UNDO'}

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
# symmetrizeTarget(context, left2right):
#----------------------------------------------------------

def symmetrizeTarget(context, left2right):
    global Left, Mid
    setupVertexPairs(context, False)
    ob = context.object
    scn = context.scene
    if not isTarget(ob):
        return
    bpy.ops.object.mode_set(mode='OBJECT')
    verts = ob.active_shape_key.data
    bverts = ob.data.vertices
    for vn in Mid.keys():
        v = verts[vn]
        v.co[0] = 0
    for (lvn,rvn) in Left.items():
        lv = verts[lvn].co
        rv = verts[rvn].co
        if left2right:
            rv[0] = -lv[0]
            rv[1] = lv[1]
            rv[2] = lv[2]
            bverts[rvn].select = bverts[lvn].select
        else:
            lv[0] = -rv[0]
            lv[1] = rv[1]
            lv[2] = rv[2]
            bverts[lvn].select = bverts[rvn].select
    print("Target symmetrized")
    return

class VIEW3D_OT_SymmetrizeTargetButton(bpy.types.Operator):
    bl_idname = "mh.symmetrize_target"
    bl_label = "Symmetrize"
    bl_options = {'UNDO'}
    left2right = BoolProperty()

    def execute(self, context):
        symmetrizeTarget(context, self.left2right)
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
        print("Skipped:", the.ConfirmString)
        the.Confirm = None
        the.ConfirmString = "?"
        the.ConfirmString2 = None
        return{'FINISHED'}            


#----------------------------------------------------------
#   Utililies
#----------------------------------------------------------

def findBase(context):
    for ob in context.scene.objects:
        if isBase(ob):
            return ob
    raise NameError("No base object found")

def isBase(ob):
    try:
        return (ob["NTargets"] == 0)
    except:
        return False

def isTarget(ob):
    try:
        return (ob["NTargets"] > 0)
    except:
        return False
        
def isBaseOrTarget(ob):
    try:
        ob["NTargets"]
        return True
    except:
        return False

def isSaving(ob):
    try:
        return ob["Saving"]
    except:
        return False
        
def isDiscarding(ob):
    try:
        return ob["Discarding"]
    except:
        return False
        
def deleteAll(context):
    scn = context.scene
    for ob in scn.objects:
        if isBaseOrTarget(ob):
            scn.objects.unlink(ob)
    return                    

#----------------------------------------------------------
#   Settings
#----------------------------------------------------------

def settingsFile(name):
    outdir = os.path.expanduser("~/makehuman/settings/")        
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    return os.path.join(outdir, "make_target.%s" % name)
    

def readDefaultSettings(context):
    fname = settingsFile("settings")
    try:
        fp = open(fname, "rU")
    except:
        print("Did not find %s. Using default settings" % fname)
        return
    
    scn = context.scene    
    for line in fp:
        words = line.split()
        prop = words[0]
        value = words[1].replace("\%20", " ")
        scn[prop] = value
    fp.close()
    return
    

def saveDefaultSettings(context):
    fname = settingsFile("settings")
    fp = open(fname, "w")
    scn = context.scene
    for (key, value) in [
        ("MhProgramPath", scn.MhProgramPath), 
        ("MhUserPath", scn.MhUserPath), 
        ("MhTargetPath", scn.MhTargetPath)]:
        fp.write("%s %s\n" % (key, value.replace(" ", "\%20")))
    fp.close()
    return

    
class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
    bl_idname = "mh.factory_settings"
    bl_label = "Restore Factory Settings"

    def execute(self, context):
        scn = context.scene
        scn.MhProgramPath = "/program/makehuman"
        scn.MhUserPath = "~/documents/makehuman"
        scn.MhTargetPath = "/program/makehuman/data/correctives"
        return{'FINISHED'}    


class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
    bl_idname = "mh.save_settings"
    bl_label = "Save Settings"

    def execute(self, context):
        saveDefaultSettings(context)
        return{'FINISHED'}    


class OBJECT_OT_ReadSettingsButton(bpy.types.Operator):
    bl_idname = "mh.read_settings"
    bl_label = "Read Settings"

    def execute(self, context):
        readDefaultSettings(context)
        return{'FINISHED'}    


#----------------------------------------------------------
#   Init
#----------------------------------------------------------

def init():
    the.Confirm = None
    the.ConfirmString = "?"

    bpy.types.Scene.MhProgramPath = StringProperty(
        name = "Program Path",
        default = "/program/makehuman"
    )        
    bpy.types.Scene.MhUserPath = StringProperty(
        name = "User Path",
        default = "~/documents/makehuman"
    )        
    bpy.types.Scene.MhTargetPath = StringProperty(
        name = "Target Path",
        default = "/program/makehuman/data/correctives" 
    )        
    bpy.types.Scene.MhRelax = FloatProperty(default = 0.5)
    bpy.types.Scene.MhUnlock = BoolProperty(default = False)
    bpy.types.Scene.MhLoadMaterial = EnumProperty(
        items = [('None','None','None'), ('Groups','Groups','Groups'), ('Materials','Materials','Materials')],
        name="Load as materials",
        default = 'None')
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

    def execute(self, context):
        initScene(context.scene)
        return{'FINISHED'}                

