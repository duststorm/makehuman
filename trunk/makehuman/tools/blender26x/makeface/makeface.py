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
import mathutils
import math
from bpy.props import *

from mh_utils import globvars as the
from mh_utils import utils
from mh_utils import proxy
from mh_utils import character
from mh_utils import warp
from mh_utils import import_obj

#----------------------------------------------------------
#   Generate mask
#----------------------------------------------------------

def loadMaskTarget(context, gender, age, value):
    file = "neutral-%s-%s.target" % (gender, age)
    path = os.path.join(context.scene.MhProgramPath, "data/targets/macrodetails/", file)
    print(path, value)
    try:
        skey = utils.loadTarget(path, context)
    except IOError:
        skey = None
    if skey:
        skey.value = value
    else:
        print("No such file", path)
    return


def loadMaskProxy(context, gender, age):
    maskProxy = proxy.CProxy()
    #userpath = os.path.expanduser(scn.MhUserPath)
    #filepath = os.path.join(userpath, "data/clothes/mask/mask.mhclo")
    userpath = os.path.expanduser(os.path.dirname(__file__))
    filepath = os.path.join(userpath, "mask.mhclo")
    print(filepath)
    maskProxy.read(filepath)
    return maskProxy


class VIEW3D_OT_GenerateMaskButton(bpy.types.Operator):
    bl_idname = "mh.generate_mask"
    bl_label = "Generate Mask"
    bl_options = {'UNDO'}
    delete = BoolProperty()

    def execute(self, context):
        if self.delete:
            utils.deleteAll(context)
        scn = context.scene
            
        base = import_obj.importBaseObj(context)
        base.layers[1] = True
        base.layers[0] = False
        scn.objects.active = base
        loadMaskTarget(context, scn.MhGender, scn.MhAge, 1.0)
        
        maskProxy = loadMaskProxy(context, scn.MhGender, scn.MhAge)
        mask = import_obj.importObj(maskProxy.obj_file, context)
        print(mask)
        mask.draw_type = 'WIRE'
        mask.show_x_ray = True        
        scn.objects.active = mask

        #utils.removeShapeKeys(mask)
        skey = mask.shape_key_add(name=base.active_shape_key.name)
        skey.value = 1.0
        mask.active_shape_key_index = 1        
        maskProxy.update(base.active_shape_key.data, mask.active_shape_key.data)
        skey = mask.shape_key_add(name="Shape", from_mix=False)
        skey.value = 1.0
        mask.use_shape_key_edit_mode = True
        mask.active_shape_key_index = 2

        mask["MhAge"] = scn.MhAge
        mask["MhGender"] = scn.MhGender
        mask["MaskFilePath"] = ""
        mask["MaskObjFile"] = maskProxy.obj_file
        
        

        print("Mask imported")
        print(maskProxy)
        return{'FINISHED'}    


def shapekeyMask(context):
    scn = context.scene
    mask,base = findMaskAndBase(context)
    if mask.data.shape_keys:
        print("Mask already has shapekeys")
        return
    verts = {}
    for v in mask.data.vertices:
        verts[v.index] = v.co.copy()
    maskProxy = loadMaskProxy(context, mask["MhGender"], mask["MhAge"])
    maskProxy.update(base.active_shape_key.data, mask.data.vertices)
    scn.objects.active = mask
    mask.shape_key_add(name="Basis")
    skey = mask.shape_key_add(name="Shape")
    mask.active_shape_key_index = 1
    for (i,x) in verts.items():
        skey.data[i].co = x
    print("Mask shapekeys generated")
    return            
    
    
class VIEW3D_OT_ShapekeyMaskButton(bpy.types.Operator):
    bl_idname = "mh.shapekey_mask"
    bl_label = "Shapekey Mask"
    bl_options = {'UNDO'}
    delete = BoolProperty()

    def execute(self, context):
        shapekeyMask(context)
        return{'FINISHED'}    
    
      

        
    

def generateFace(context):
    mask,base = findMaskAndBase(context)
    warpField = warp.CWarp(context)
    warpField.setupFromObject(mask, context)
    createTestFace(context, warpField, mask)
    warpField.warpMesh(mask, base)


def printVec(string, vec):
    print(string, "(%.4f %.4f %.4f)" % (vec[0], vec[1], vec[2]))
    
    

def createTestFace(context, warpField, mask):
    bpy.ops.object.duplicate()
    ob = context.object
    ob.name = "Test"
    utils.removeShapeKeys(ob)
    ob.layers[2] = True
    ob.layers[0] = False
    print(ob)
    for v in mask.data.vertices:
        v1 = ob.data.vertices[v.index]
        v1.co = warpField.estimate(v.co)
        #printVec("X%d" % v.index, v.co)
        #printVec("Y%d" % v1.index, v1.co)

    
class VIEW3D_OT_GenerateFaceButton(bpy.types.Operator):
    bl_idname = "mh.generate_face"
    bl_label = "Generate Face"
    bl_options = {'UNDO'}
    delete = BoolProperty()

    def execute(self, context):
        generateFace(context)
        return{'FINISHED'}    

#----------------------------------------------------------
#   Save face as
#----------------------------------------------------------

class VIEW3D_OT_SaveFaceButton(bpy.types.Operator):
    bl_idname = "mh.save_face"
    bl_label = "Save Face"
    bl_options = {'UNDO'}

    def execute(self, context):
        mask,base = findMaskAndBase(context)
        path = mask["MaskFilePath"]
        if the.Confirm:
            the.Confirm = None
            doSaveTarget(context, path, False)
        else:
            the.Confirm = "mh.save_face"
            the.ConfirmString = "Overwrite target file?"
            the.ConfirmString2 = ' "%s?"' % os.path.basename(path)
        return{'FINISHED'}    


class VIEW3D_OT_SaveFaceAsButton(bpy.types.Operator):
    bl_idname = "mh.save_face_as"
    bl_label = "Save Face As"
    bl_options = {'UNDO'}

    filename_ext = ".target"
    filter_glob = StringProperty(default="*.target", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for target file", 
        maxlen= 1024, default= "")

    def execute(self, context):
        doSaveTarget(context, self.properties.filepath, True)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def doSaveTarget(context, filepath, saveas):    
    mask,base = findMaskAndBase(context)    
    (fname,ext) = os.path.splitext(filepath)
    filepath = fname + ".target"
    fp = open(filepath, "w")  
    skey = base.data.shape_keys.key_blocks[-1]
    if skey.name == "Shape":
        skey.name = os.path.basename(fname)
    print("Saving target %s to %s" % (skey.name, filepath))
    for v in base.data.vertices:
        vn = v.index
        vec = skey.data[vn].co - v.co
        if vec.length > the.Epsilon:
            fp.write("%d %.4f %.4f %.4f\n" % (vn, vec[0], vec[2], -vec[1]))
    fp.close()    
    mask["MaskFilePath"] = filepath
    print("Target saved")
    return

#----------------------------------------------------------
#   Utilities
#----------------------------------------------------------

class VIEW3D_OT_MakeMaskButton(bpy.types.Operator):
    bl_idname = "mh.make_mask"
    bl_label = "Make Mask"
    bl_options = {'UNDO'}

    def execute(self, context):
        ob = context.object
        ob["MhAge"] = "old"
        ob["MaskFilePath"] = ""
        ob.shape_key_add(name="Basis")
        ob.shape_key_add(name="Target")
        ob.shape_key_add(name="Shape")
        ob.active_shape_key_index = 2
        return {'FINISHED'}


def isMask(ob):
    try:
        ob["MhAge"]
        return True
    except:
        return False


def findMaskAndBase(context):
    scn = context.scene
    mask = None
    base = None
    for ob in scn.objects:
        if utils.isBaseOrTarget(ob):
            base = ob
        elif isMask(ob):
            mask = ob
    if not base:
        raise NameError("No base object found")
    if not mask:
        raise NameError("No mask found")
    return mask,base        


#----------------------------------------------------------
#   Init
#----------------------------------------------------------

def init():

    bpy.types.Scene.MhAge = EnumProperty(
        items = [('child','child','child'), ('young','young','young'), ('old','old','old')],
        name="Age",
        default = 'child')

    bpy.types.Scene.MhGender = EnumProperty(
        items = [('female','female','female'), ('male','male','male')],
        name="Gender",
        default = 'female')

    bpy.types.Scene.MhStiffness = FloatProperty(
        name="Stiffness",
        default = 0.06)

    bpy.types.Scene.MhLambda = FloatProperty(
        name="Lambda",
        default = 0.0)

    bpy.types.Scene.MhIterations = IntProperty(
        name="Iterations",
        default = 1)
        
    return  
    
