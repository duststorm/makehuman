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

from . import globvars as the
from . import proxy
from . import import_obj
from . import maketarget

#----------------------------------------------------------
#   Generate mask
#----------------------------------------------------------

def loadMaskTarget(context, gender, age, value):
    file = "neutral-%s-%s.target" % (gender, age)
    path = os.path.join(context.scene.MhProgramPath, "data/targets/macrodetails/", file)
    print(path, value)
    try:
        skey = maketarget.loadTarget(path, context)
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
            deleteAll(context)
        scn = context.scene
            
        base = maketarget.importBaseObj(context)
        scn.objects.active = base
        if scn.MhGender == 'neutral':
            loadMaskTarget(context, 'female', scn.MhAge, 0.5)
            loadMaskTarget(context, 'male', scn.MhAge, 0.5)
        else:
            loadMaskTarget(context, scn.MhGender, scn.MhAge, 1.0)
        maskProxy = loadMaskProxy(context, scn.MhGender, scn.MhAge)
        
        mask = import_obj.importObj(maskProxy.obj_file, context)
        scn.objects.active = mask
        #maketarget.removeShapeKeys(mask)
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
        
        layers = 20*[False]
        layers[1] = True
        base.layers = layers
        mask.draw_type = 'WIRE'
        mask.show_x_ray = True        
        

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
    
      
#----------------------------------------------------------
#   Try to load numpy.
#   Will only work if it is installed and for 32 bits.
#----------------------------------------------------------

#import numpy
import sys
import imp

def getModule(modname):        
    try:
        return sys.modules[modname]
    except KeyError:
        pass
    print("Trying to load %s" % modname)
    fp, pathname, description = imp.find_module(modname)
    try:
        imp.load_module(modname, fp, pathname, description)
    finally:
        if fp:
            fp.close()
    return sys.modules[modname]
    
try:    
    numpy = getModule("numpy")  
    the.foundNumpy = True
    print("Numpy successfully loaded")
except:
    numpy = None
    the.foundNumpy = False
    print("Failed to load numpy. MakeFace will not work")
    
#----------------------------------------------------------
#   Generate face
#----------------------------------------------------------

class CMatch:
    def __init__(self, mask, scn):
        self.name = mask.name
        self.stiffness = scn.MhStiffness
        xverts = mask.data.vertices
        self.n = len(xverts)   
        n = self.n
        yverts = self.getShapeSumVerts(mask)
                
        xsum = mathutils.Vector((0,0,0))
        for k in range(n):
            xsum += xverts[k].co
        
        self.y = {}
        self.w = {}       
        for k in range(3):
            self.w[k] = numpy.arange(n, dtype=float)
            for i in range(n):
                self.w[k][i] = 0.1
            """
            for j in range(3):
                self.w[k][n+j] = -xsum[j]
            self.w[k][n+3] = -n*0.1
            """
            self.y[k] = numpy.arange(n, dtype=float)
            for i in range(n):
                self.y[k][i] = yverts[i][k]
            """                
            for j in range(4):
                self.y[k][n+j] = 0
            """
            
        self.x = {}
        self.s2 = {}
        self.lamb = 0
        self.zMin = 1e6

        for i in range(n):
            vx0 = xverts[i]
            self.x[i] = vx0.co.copy()
            if yverts[i][2] < self.zMin:
                self.zMin = yverts[i][2]
            mindist = 1e6
            for vx1 in xverts:
                if vx1 != vx0:
                    vec = vx0.co - vx1.co
                    if vec.length < mindist:                        
                        mindist = vec.length
                        if mindist < 1e-3:
                            print(vx0.index, vx1.index, mindist)
                            print("  ", vx0.co, vx1.co)
            self.s2[k] = (mindist*mindist)
                
        # Set up matrix
        self.H = numpy.identity(n, float)
        for i in range(n):
            xi = xverts[i].co
            for j in range(n):
                self.H[i][j] = self.rbf(j, xi)
        
        """                
            for j in range(4):
                self.H[i][n+j] = 0
        for i in range(3):                
            xj = xverts[j].co
            for j in range(n):
                self.H[n+i][j] = xj[i]
        for j in range(n):
            self.H[n+3][j] = 1
        for j in range(4):
            self.H[n+3][n+j] = 0
        """
        """
        for i in range(6):
            printVec("X%d" % i, self.x[i])            
        for i in range(3):
            print("Y%d" % i, self.y[i])            
        print(self.H)
        """
        
        self.HT = self.H.transpose()
        self.HTH = numpy.dot(self.HT, self.H)      
        print("Match set up")        
        return

        uc,zc = numpy.linalg.eig(HH)
        self.u = uc.real
        self.z = zc.real
        print("Eval", self.u)
        print("Match set up")
        
        return
        
        
    def getShapeSumVerts(self, ob):
        verts = {}
        for v in ob.data.vertices:
            verts[v.index] = v.co.copy()
        for skey in ob.data.shape_keys.key_blocks[1:]:
            for v in ob.data.vertices:
                vn = v.index
                verts[vn] += skey.data[vn].co - v.co
        return verts


    def train(self, index):        
        A = self.HTH + self.lamb * numpy.identity(self.n, float) 
        b = numpy.dot(self.HT, self.y[index])
        self.w[index] = numpy.linalg.solve(A, b)
        #self.w[index] = numpy.linalg.solve(self.H, self.y[index])
        e = self.y[index] - numpy.dot(self.H, self.w[index])
        ee = numpy.dot(e.transpose(), e)
        print("Trained for index", index, "Error", math.sqrt(ee))
        #print(self.w[index])
        return
        
        eta = 0
        ee = 0
        wAw = 0
        ngamma = 0
        for i in range(self.n):
            ui = self.u[i]
            zi = self.z[i]
            zi2 = numpy.dot(zi.transpose(),zi)
            uil = ui + self.lamb
            eta += ui/(uil*uil)
            ee += self.lamb*self.lamb*zi2/(uil*uil)
            wAw += ui*zi2/(uil*uil*uil)
            ngamma += self.lamb/uil
        gcv = self.n*ee/(ngamma*ngamma)
        self.lamb = eta/ngamma * ee/wAw
        print("GCV", gcv, "Lambda", self.lamb)            
        
        return gcv

        
    def rbf(self, vn, x):
        vec = x - self.x[vn]
        vec2 = vec.dot(vec)
        #return math.sqrt(vec2 + self.s2[vn])
        r = math.sqrt(vec2)
        return math.exp(-self.stiffness*r)
        
        
    def estimate(self, x):
        y = mathutils.Vector((0,0,0))
        f = {}        
        for i in range(self.n):
            f[i] = self.rbf(i, x)
        for k in range(3):
            w = self.w[k]
            for i in range(self.n):
                y[k] += w[i]*f[i]
            """                
            for k in range(3):
                y[k] += w[self.n+k]*x[k]
            y[k] += w[self.n+3]
            """
        return y    
        
        
    def warpMesh(self, mask, base):
        xverts = self.getShapeSumVerts(base)
        skey = base.shape_key_add(name=self.name, from_mix=False) 
        blocks = base.data.shape_keys.key_blocks
        nKeys = len(blocks)
        base.active_shape_key_index = nKeys-1
        skey.value = 1.0
        basis = blocks[0]
        n = len(base.data.vertices)
        nwarped = 0
        for i in range(n):
            if i%1000 == 0:
                print(i)
            x = xverts[i]
            if x[2] > self.zMin:
                x0 = basis.data[i].co
                xest = self.estimate(x0)
                skey.data[i].co = xest - x + x0
                nwarped += 1
        print("%d vertices warped" % nwarped)                
           
            
        
    

def generateFace(context):
    mask,base = findMaskAndBase(context)
    match = CMatch(mask, context.scene)
    for n in range(context.scene.MhIterations):
        match.train(0)
        match.train(1)
        match.train(2)
        print("Match trained")

    """        
    skey = mask.active_shape_key        
    for v in mask.data.vertices:        
        x = v.co
        y = skey.data[v.index].co
        z = match.estimate(x)
        n = v.index
        if n == 16:
            print(" ")
            printVec("X%d" % n, x)
            printVec("Y%d" % n, y)
            printVec("Z%d" % n, z)
    """            
    createTestFace(context, match, mask)
    match.warpMesh(mask, base)


def printVec(string, vec):
    print(string, "(%.4f %.4f %.4f)" % (vec[0], vec[1], vec[2]))
    
    

def createTestFace(context, match, mask):
    bpy.ops.object.duplicate()
    ob = context.object
    ob.name = "Test"
    maketarget.removeShapeKeys(ob)
    ob.layers[2] = True
    ob.layers[0] = False
    print(ob)
    for v in mask.data.vertices:
        v1 = ob.data.vertices[v.index]
        v1.co = match.estimate(v.co)
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
        if maketarget.isBaseOrTarget(ob):
            base = ob
        elif isMask(ob):
            mask = ob
    if not base:
        raise NameError("No base object found")
    if not mask:
        raise NameError("No mask found")
    return mask,base        


def deleteAll(context):
    scn = context.scene
    for ob in scn.objects:
        if maketarget.isBaseOrTarget(ob) or isMask(ob):
            scn.objects.unlink(ob)
            del ob
    return                    

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
    
