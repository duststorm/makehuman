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

bl_info = {
    "name": "Make target",
    "author": "Manuel Bastioni, Thomas Larsson",
    "version": "0.2",
    "blender": (2, 6, 0),
    "api": 40000,
    "location": "View3D > Properties > Make target",
    "description": "Make MakeHuman target",
    "warning": "",
    'wiki_url': '',
    "category": "MakeHuman"}


import bpy
import os
import sys
import math
import random
from mathutils import Vector
from bpy.props import *
from bpy_extras.io_utils import ExportHelper, ImportHelper

#----------------------------------------------------------
#   Global variables
#----------------------------------------------------------

# Distance below which translations are ignored (in mm)
Epsilon = 1e-3

# Number of verts which are body, not clothes
NBodyVerts = 15340

theProxy = None
        
#----------------------------------------------------------
# 
#----------------------------------------------------------

#
#    class CProxy
#

class CProxy:
    def __init__(self):
        self.name = None
        self.obj_file = None
        self.refVerts = []
        self.firstVert = 0
        self.xScale = None
        self.yScale = None
        self.zScale = None
        return
        
    def __repr__(self):
        return ("<CProxy %s %d\n  %s\n  x %s\n  y %s\n  z %s>" % 
            (self.name, self.firstVert, self.obj_file, self.xScale, self.yScale, self.zScale))
        
    def update(self, verts, bverts):
        rlen = len(self.refVerts)
        mlen = len(verts)
        first = self.firstVert
        if (first+rlen) != mlen:
            raise NameError( "Bug: %d refVerts != %d meshVerts" % (first+rlen, mlen) )
        s0 = getScale(self.xScale, verts, 0)
        s1 = getScale(self.yScale, verts, 2)
        s2 = getScale(self.zScale, verts, 1)
        #print("Scales", s0, s1, s2)
        for n in range(rlen):
            vert = verts[n+first]
            refVert = self.refVerts[n]
            if type(refVert) == tuple:
                (rv0, rv1, rv2, w0, w1, w2, d0, d1, d2) = refVert
                v0 = verts[rv0]
                v1 = verts[rv1]
                v2 = verts[rv2]
                vert.co[0] = w0*v0.co[0] + w1*v1.co[0] + w2*v2.co[0] + d0*s0
                vert.co[1] = w0*v0.co[1] + w1*v1.co[1] + w2*v2.co[1] - d2*s2
                vert.co[2] = w0*v0.co[2] + w1*v1.co[2] + w2*v2.co[2] + d1*s1
                bverts[n+first].select = (bverts[rv0].select or bverts[rv1].select or bverts[rv2].select)
            else:
                v0 = verts[refVert]
                vert.co = v0.co
                bvert[n+first].select = bverts[rv0].select
        return

    def read(self, filepath):
        realpath = os.path.realpath(os.path.expanduser(filepath))
        folder = os.path.dirname(realpath)
        try:
            tmpl = open(filepath, "rU")
        except:
            tmpl = None
        if tmpl == None:
            print("*** Cannot open %s" % realpath)
            return None

        status = 0
        doVerts = 1
        vn = 0
        for line in tmpl:
            words= line.split()
            if len(words) == 0:
                pass
            elif words[0] == '#':
                status = 0
                if len(words) == 1:
                    pass
                elif words[1] == 'verts':
                    if len(words) > 2:
                        self.firstVert = int(words[2])                    
                    status = doVerts
                elif words[1] == 'name':
                    self.name = words[2]
                elif words[1] == 'x_scale':
                    self.xScale = scaleInfo(words)
                elif words[1] == 'y_scale':
                    self.yScale = scaleInfo(words)
                elif words[1] == 'z_scale':
                    self.zScale = scaleInfo(words)                
                elif words[1] == 'obj_file':
                    self.obj_file = os.path.join(folder, words[2])
                else:
                    pass
            elif status == doVerts:
                if len(words) == 1:
                    v = int(words[0])
                    self.refVerts.append(v)
                else:                
                    v0 = int(words[0])
                    v1 = int(words[1])
                    v2 = int(words[2])
                    w0 = float(words[3])
                    w1 = float(words[4])
                    w2 = float(words[5])            
                    d0 = float(words[6])
                    d1 = float(words[7])
                    d2 = float(words[8])
                    self.refVerts.append( (v0,v1,v2,w0,w1,w2,d0,d1,d2) )
        return

def scaleInfo(words):                
    v1 = int(words[2])
    v2 = int(words[3])
    den = float(words[4])
    return (v1, v2, den)

def getScale(info, verts, index):
    (v1, v2, den) = info
    num = abs(verts[v1].co[index] - verts[v2].co[index])
    return num/den
    
#----------------------------------------------------------
#   importObj(filepath, context):
#   Simple obj importer which reads only verts, faces, and texture verts
#----------------------------------------------------------

def importObj(filepath, context):
    scn = context.scene
    obname = os.path.basename(filepath)
    fp = open(filepath, "rU")  
    print("Importing %s" % filepath)

    verts = []
    faces = []
    texverts = []
    texfaces = []
    groups = {}
    materials = {}

    group = []
    nf = 0
    for line in fp:
        words = line.split()
        if len(words) == 0:
            pass
        elif words[0] == "v":
            verts.append( (float(words[1]), -float(words[3]), float(words[2])) )
        elif words[0] == "vt":
            texverts.append( (float(words[1]), float(words[2])) )
        elif words[0] == "f":
            (f,tf) = parseFace(words)
            faces.append(f)
            if tf:
                texfaces.append(tf)
            group.append(nf)
            matlist.append(nf)
            nf += 1
        elif words[0] == "g":
            name = words[1]
            try:
                group = groups[name]
            except KeyError:
                group = []
                groups[name] = group
        elif words[0] == "usemtl":
            name = words[1]
            try:
                matlist = materials[name]
            except KeyError:
                matlist = []
                materials[name] = matlist
        else:
            pass
    print("%s successfully imported" % filepath)
    fp.close()

    me = bpy.data.meshes.new(obname)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(obname, me)

    if texverts:
        uvtex = me.uv_textures.new()
        uvtex.name = obname
        data = uvtex.data
        for n in range(len(texfaces)):
            tf = texfaces[n]
            data[n].uv1 = texverts[tf[0]]
            data[n].uv2 = texverts[tf[1]]
            data[n].uv3 = texverts[tf[2]]
            if len(tf) == 4:
                data[n].uv4 = texverts[tf[3]]
                
    if scn.MhLoadMaterial == 'Groups':
        addMaterials(groups, me, "Group")
    elif scn.MhLoadMaterial == 'Materials':
        addMaterials(materials, me, "Material")
        for (name,group) in groups.items():
            vgrp = ob.vertex_groups.new(name=name)
            if vgrp.name != name:
                print("WARNING: Group name %s => %s" % (name, vgrp.name))
            for nf in group:
                f = me.faces[nf]
                for v in f.vertices:
                    vgrp.add([v], 1.0, 'REPLACE')
                    
    scn.objects.link(ob)
    ob.select = True
    scn.objects.active = ob
    ob.shape_key_add(name="Basis")
    bpy.ops.object.shade_smooth()
    return ob
    
def parseFace(words):
    face = []
    texface = []
    for n in range(1, len(words)):
        li = words[n].split("/")
        face.append( int(li[0])-1 )
        try:
            texface.append( int(li[1])-1 )
        except:
            pass
    return (face, texface)

def addMaterials(groups, me, string):        
    mn = 0
    for (name,group) in groups.items():
        try:
            mat = bpy.data.materials[name]
        except:
            mat = bpy.data.materials.new(name=name)
        if mat.name != name:
            print("WARNING: %s name %s => %s" % (string, name, mat.name))
        mat.diffuse_color = (random.random(), random.random(), random.random())
        me.materials.append(mat)
        for nf in group:
            f = me.faces[nf]
            f.material_index = mn
        mn += 1
    return        

class VIEW3D_OT_ImportBaseMhcloButton(bpy.types.Operator):
    bl_idname = "mh.import_base_mhclo"
    bl_label = "Mhclo"
    delete = BoolProperty()

    filename_ext = ".mhclo"
    filter_glob = StringProperty(default="*.mhclo", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for mhclo file", 
        maxlen= 1024, default= "")

    def execute(self, context):
        global theProxy
        if self.delete:
            deleteAll(context)
        theProxy = CProxy()
        theProxy.read(self.properties.filepath)
        ob = importObj(theProxy.obj_file, context)
        ob["NTargets"] = 0
        ob["ProxyFile"] = self.properties.filepath
        ob["ObjFile"] = theProxy.obj_file
        setupVertexPairs(context)
        makeRestorePoint()
        print("Base object imported")
        print(theProxy)
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class VIEW3D_OT_ImportBaseObjButton(bpy.types.Operator):
    bl_idname = "mh.import_base_obj"
    bl_label = "Obj"
    delete = BoolProperty()

    filename_ext = ".obj"
    filter_glob = StringProperty(default="*.obj", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for obj file", 
        maxlen= 1024, default= "")

    def execute(self, context):
        global theProxy
        if self.delete:
            deleteAll(context)
        theProxy = None
        ob = importObj(self.properties.filepath, context)
        ob["NTargets"] = 0
        ob["ProxyFile"] = 0
        ob["ObjFile"] = self.properties.filepath
        setupVertexPairs(context)
        makeRestorePoint()
        print("Base object imported")
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#----------------------------------------------------------
#   setupVertexPairs(ob):
#----------------------------------------------------------

Left = {}
Right = {}
Mid = {}

def setupVertexPairs(context):
    global Left, Right, Mid
    if Left.keys():
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
        elif x > Epsilon:
            Left[vn] = vmir
        elif x < -Epsilon:
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
        if dist < Epsilon:
            return v1
    if abs(x) > Epsilon:            
        notfound.append("  %d at (%.4f %.4f %.4f)" % (v, x, y, z))
    return -1            

#----------------------------------------------------------
#   loadTarget(filepath, context):
#----------------------------------------------------------

def loadTarget(filepath, context):
    realpath = os.path.realpath(os.path.expanduser(filepath))
    fp = open(realpath, "rU")  
    print("Loading target %s" % realpath)

    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    for v in ob.data.vertices:
        v.select = False
    name = os.path.basename(filepath)
    skey = ob.shape_key_add(name=name, from_mix=False)
    ob.active_shape_key_index = shapeKeyLen(ob) - 1
    #bpy.ops.object.shape_key_add(from_mix=False)
    #skey = ob.active_shape_key
    skey.name = name
    #print("Active", ob.active_shape_key.name)
    for line in fp:
        words = line.split()
        if len(words) == 0:
            pass
        else:
            index = int(words[0])
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
    return

def shapeKeyLen(ob):
    n = 0
    for skey in ob.data.shape_keys.key_blocks:
        n += 1
    return n

class VIEW3D_OT_LoadTargetButton(bpy.types.Operator):
    bl_idname = "mh.load_target"
    bl_label = "Load target"

    filename_ext = ".target"
    filter_glob = StringProperty(default="*.target", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for target file", 
        maxlen= 1024, default= "")

    def execute(self, context):
        loadTarget(self.properties.filepath, context)
        makeRestorePoint()
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
    bl_label = "Load target from mesh"

    def execute(self, context):
        loadTargetFromMesh(context)
        makeRestorePoint()
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
    bl_label = "New target"

    def execute(self, context):
        newTarget(context)
        makeRestorePoint()
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
        skey.name = os.path.basename(filepath)
    verts = evalVertLocations(ob)
    
    (fname,ext) = os.path.splitext(filepath)
    filepath = fname + ".target"
    fp = open(filepath, "w")  
    print("Saving target %s to %s" % (ob, filepath))
    for n,vco in verts.items():
        bv = ob.data.vertices[n]
        vec = vco - bv.co
        if vec.length > Epsilon and (saveAll or bv.select):
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
    bl_label = "Save target"

    def execute(self, context):
        global Confirm, ConfirmString, ConfirmString2
        ob = context.object
        path = ob["FilePath"]
        if Confirm:
            Confirm = None
            doSaveTarget(ob, path)
            print("Target saved")
        else:
            Confirm = "mh.save_target"
            ConfirmString = "Overwrite target file?"
            ConfirmString2 = ' "%s?"' % os.path.basename(path)
        return{'FINISHED'}            

class VIEW3D_OT_SaveasTargetButton(bpy.types.Operator):
    bl_idname = "mh.saveas_target"
    bl_label = "Save target as"

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
    skeys = ob.data.shape_keys.key_blocks
    n = len(skeys)
    while n >= 0:
        ob.active_shape_key_index = n
        bpy.ops.object.shape_key_remove()
        n -= 1
    for prop in ob.keys():
        del ob[prop]
    for v in ob.data.vertices:
        v.co = verts[v.index]
    return

class VIEW3D_OT_ApplyTargetsButton(bpy.types.Operator):
    bl_idname = "mh.apply_targets"
    bl_label = "Apply targets"

    def execute(self, context):
        global Confirm, ConfirmString, ConfirmString2
        if Confirm:
            Confirm = None
            applyTargets(context)
            makeRestorePoint()
            print("All targets applied")
        else:
            Confirm = "mh.apply_targets"
            ConfirmString = "Apply all targets to mesh?"
            ConfirmString2 = None
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
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.shape_key_remove()            
        elif os.path.isdir(file):
            batchFixTargets(context, file)
    return            
            
class VIEW3D_OT_BatchFixButton(bpy.types.Operator):
    bl_idname = "mh.batch_fix"
    bl_label = "Batch fix targets"

    def execute(self, context):
        global TargetSubPaths, Confirm, ConfirmString, ConfirmString2
        scn = context.scene
        if not Confirm:
            ConfirmString = "Really batch fix targets?"
            ConfirmString2 = None
            Confirm = "mh.batch_fix"
            return
        Confirm = None
        folder = os.path.expanduser(scn["TargetPath"])
        for subfolder in TargetSubPaths:
            if scn["Mh%s" % subfolder]:
                batchFixTargets(context, os.path.join(folder, subfolder))
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
    bl_label = "Batch render"
    opengl = BoolProperty()

    def execute(self, context):
        global TargetSubPaths
        scn = context.scene
        folder = os.path.expanduser(scn["TargetPath"])
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
    relaxMesh(skey.data, ob.data.edges, NBodyVerts, context.scene["Relax"])

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
    bl_label = "Relax target"

    def execute(self, context):
        relaxTarget(context)
        return{'FINISHED'}      
        
    
#----------------------------------------------------------
#   fitTarget(context):
#----------------------------------------------------------

def fitTarget(context):
    global theProxy
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    scn = context.scene
    if not isTarget(ob):
        return
    ob.active_shape_key_index = ob["NTargets"]
    if not checkValid(ob):
        return
    if not theProxy:
        path = ob["ProxyFile"]
        if path:
            print("Rereading %s" % path)
            theProxy = CProxy()
            theProxy.read(path)
        else:
            raise NameError("Object %s has no associated mhclo file. Cannot fit" % ob.name)
            return
    #print(theProxy)
    theProxy.update(ob.active_shape_key.data, ob.data.vertices)
    return

class VIEW3D_OT_FitTargetButton(bpy.types.Operator):
    bl_idname = "mh.fit_target"
    bl_label = "Fit target"

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
    
def checkValid(ob):
    nShapes = shapeKeyLen(ob)
    if nShapes != ob["NTargets"]+1:
        print("Consistency problem:\n  %d shapes, %d targets" % (nShapes, ob["NTargets"]))
        return False
    return True

class VIEW3D_OT_DiscardTargetButton(bpy.types.Operator):
    bl_idname = "mh.discard_target"
    bl_label = "Discard target"

    def execute(self, context):
        global Confirm, ConfirmString, ConfirmString2
        if Confirm:        
            Confirm = None
            discardTarget(context)
        else:
            Confirm = "mh.discard_target"
            ConfirmString = "Really discard target?"
            ConfirmString2 = None
        return{'FINISHED'}                

#----------------------------------------------------------
# symmetrizeTarget(context, left2right):
#----------------------------------------------------------

def symmetrizeTarget(context, left2right):
    global Left, Mid
    setupVertexPairs(context)
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
    left2right = BoolProperty()

    def execute(self, context):
        symmetrizeTarget(context, self.left2right)
        makeRestorePoint()
        return{'FINISHED'}                
                        
#----------------------------------------------------------
#   Skip
#----------------------------------------------------------

class VIEW3D_OT_SkipButton(bpy.types.Operator):
    bl_idname = "mh.skip"
    bl_label = "No"

    def execute(self, context):
        global Confirm, ConfirmString, ConfirmString2
        print("Skipped:", ConfirmString)
        Confirm = None
        ConfirmString = "?"
        ConfirmString2 = None
        return{'FINISHED'}            

class VIEW3D_OT_FixInconsistencyButton(bpy.types.Operator):
    bl_idname = "mh.fix_inconsistency"
    bl_label = "Fix it!"

    def execute(self, context):
        ob = context.object
        if ob.data.shape_keys:
            ob["NTargets"] = len(ob.data.shape_keys.key_blocks)
        else:
            ob.shape_key_add(name="Basis")
            ob["NTargets"] = 0
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

def makeRestorePoint():
    bpy.ops.transform.translate(value=(0,0,0))

#----------------------------------------------------------
#   class MakeTargetPanel(bpy.types.Panel):
#----------------------------------------------------------


class MakeTargetPanel(bpy.types.Panel):
    bl_label = "Make target"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        layout = self.layout
        ob = context.object
        scn = context.scene
        if not isInited(scn):
            layout.operator("mh.init")
            return
        if Confirm:
            layout.label("Hej")
            layout.label(ConfirmString)            
            if ConfirmString2:
                layout.label(ConfirmString2)            
            layout.operator(Confirm, text="Yes") 
            layout.operator("mh.skip")
            return            
        layout.label("Load materials from")
        layout.prop(scn, "MhLoadMaterial", expand=True)
        layout.separator()
        if isBaseOrTarget(ob):
            layout.operator("mh.import_base_mhclo", text="Reimport base mhclo").delete = True
            layout.operator("mh.import_base_obj", text="Reimport base obj").delete = True
        else:
            layout.operator("mh.import_base_mhclo", text="Import base mhclo").delete = False
            layout.operator("mh.import_base_obj", text="Import base obj").delete = False
        if isBase(ob):
            layout.operator("mh.new_target")
            layout.operator("mh.load_target")            
            layout.operator("mh.load_target_from_mesh")                        
        elif isTarget(ob):
            if not ob.data.shape_keys:
                layout.label("Warning: Internal inconsistency")
                layout.operator("mh.fix_inconsistency")
                return
            layout.separator()
            layout.prop(ob, "show_only_shape_key")
            box = layout.box()
            n = 0
            for skey in ob.data.shape_keys.key_blocks:
                if n == 0:
                    n += 1
                    continue
                row = box.row()
                if n == ob.active_shape_key_index:
                    icon='LAMP'
                else:
                    icon='X'
                row.label("", icon=icon)
                row.prop(skey, "value", text=skey.name)
                n += 1
            layout.separator()
            layout.operator("mh.new_target", text="New secondary target")
            layout.operator("mh.load_target", text="Load secondary target")            
            layout.operator("mh.fit_target")
            layout.operator("mh.symmetrize_target", text="Symm Left->Right").left2right = True
            layout.operator("mh.symmetrize_target", text="Symm Right->Left").left2right = False
            #layout.separator()
            #layout.prop(scn, '["Relax"]')
            #layout.operator("mh.relax_target")
            layout.separator()
            layout.operator("mh.discard_target")
            layout.separator()
            layout.operator("mh.apply_targets")
            layout.separator()
            layout.prop(ob, '["SelectedOnly"]')
            if ob["FilePath"]:
                layout.operator("mh.save_target")           
            layout.operator("mh.saveas_target")           

class MakeTargetBatchPanel(bpy.types.Panel):
    bl_label = "Batch make targets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        return False and isInited(context.scene)
        
    def draw(self, context):
        if isBase(context.object):
            layout = self.layout
            scn = context.scene
            for fname in TargetSubPaths:
                layout.prop(scn, "Mh%s" % fname)
            layout.operator("mh.batch_fix")
            layout.operator("mh.batch_render", text="Batch render").opengl = False
            layout.operator("mh.batch_render", text="Batch OpenGL render").opengl = True

#----------------------------------------------------------
#   Init
#----------------------------------------------------------

def initScene(scn):
    global TargetSubPaths, Confirm, ConfirmString, ConfirmString2
    scn["TargetPath"] = "/home/svn/makehuman/data/targets"            
    scn["Relax"] = 0.5
    bpy.types.Scene.MhLoadMaterial = EnumProperty(
        items = [('None','None','None'), ('Groups','Groups','Groups'), ('Materials','Materials','Materials')],
        name="Load as materials")
    scn.MhLoadMaterial = 'None'
    Confirm = None
    ConfirmString = "?"
    TargetSubPaths = []
    folder = os.path.realpath(os.path.expanduser(scn["TargetPath"]))
    for fname in os.listdir(folder):
        file = os.path.join(folder, fname)        
        if os.path.isdir(file) and fname[0] != ".":
            TargetSubPaths.append(fname)
            expr = 'bpy.types.Scene.Mh%s = BoolProperty(name="%s")' % (fname,fname)
            exec(expr)
            scn["Mh%s" % fname] = False
    return  
    
def isInited(scn):
    try:
        TargetSubPaths
        scn["TargetPath"]
        return True
    except:
        return False    

class VIEW3D_OT_InitButton(bpy.types.Operator):
    bl_idname = "mh.init"
    bl_label = "Initialize"

    def execute(self, context):
        initScene(context.scene)
        return{'FINISHED'}                

#----------------------------------------------------------
#   Register
#----------------------------------------------------------

def register():
    try:
        initScene(bpy.context.scene)
    except:
        pass
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
