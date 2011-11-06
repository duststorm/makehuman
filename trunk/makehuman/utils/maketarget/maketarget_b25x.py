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
from bpy.props import *
from bpy_extras.io_utils import ExportHelper, ImportHelper

MHDIR = "/home/svn/makehuman/"
sys.path.append(MHDIR+"apps/")
sys.path.append(MHDIR+"core/")
import mh2proxy

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
        return
        
    def update(self, mesh):
        rlen = len(self.refVerts)
        mlen = len(mesh.vertices)
        first = self.firstVert
        if (first+rlen) != mlen:
            raise NameError( "Bug: %d refVerts != %d meshVerts" % (rlen, mlen) )
        for n in range(rlen):
            vert = mesh.vertices[n+first]
            refVert = self.refVerts[n]
            if type(refVert) == tuple:
                (rv0, rv1, rv2, w0, w1, w2, d0, d1, d2) = refVert
                v0 = mesh.vertices[rv0]
                v1 = mesh.vertices[rv1]
                v2 = mesh.vertices[rv2]
                vert.co[0] = w0*v0.co[0] + w1*v1.co[0] + w2*v2.co[0] + d0
                vert.co[1] = w0*v0.co[1] + w1*v1.co[1] + w2*v2.co[1] + d1
                vert.co[2] = w0*v0.co[2] + w1*v1.co[2] + w2*v2.co[2] + d2
            else:
                vert.co = mesh.vertices[refVert].co
#
#    readProxyFile(filepath):
#

def readProxyFile(filepath):
    realpath = os.path.realpath(os.path.expanduser(filepath))
    folder = os.path.dirname(realpath)
    try:
        tmpl = open(filepath, "rU")
    except:
        tmpl = None
    if tmpl == None:
        print("*** Cannot open %s" % realpath)
        return None

    proxy = CProxy()
    useProjection = True
    ignoreOffset = False
    xScale = 1.0
    yScale = 1.0
    zScale = 1.0
    
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
                    proxy.firstVert = int(words[2])                    
                status = doVerts
            elif words[1] == 'name':
                proxy.name = words[2]
            #elif words[1] == 'x_scale':
            #    xScale = getScale(words, verts, 0)
            #elif words[1] == 'y_scale':
            #    yScale = getScale(words, verts, 1)
            #elif words[1] == 'z_scale':
            #    zScale = getScale(words, verts, 2)                
            elif words[1] == 'obj_file':
                proxy.obj_file = os.path.join(folder, words[2])
            else:
                pass
        elif status == doVerts:
            if len(words) == 1:
                v = int(words[0])
                proxy.refVerts.append(v)
            else:                
                v0 = int(words[0])
                v1 = int(words[1])
                v2 = int(words[2])
                w0 = float(words[3])
                w1 = float(words[4])
                w2 = float(words[5])            
                d0 = float(words[6]) * xScale
                d1 = float(words[7]) * yScale
                d2 = float(words[8]) * zScale
                proxy.refVerts.append( (v0,v1,v2,w0,w1,w2,d0,-d2,d1) )
    return proxy

#
#   getScale(words, verts, index):                
#

def getScale(words, verts, index):                
    v1 = int(words[2])
    v2 = int(words[3])
    den = float(words[4])
    num = abs(verts[v1].co[index] - verts[v2].co[index])
    return num/den
    
#----------------------------------------------------------
#   import_obj(filepath):
#   Simple obj importer which reads only verts, faces, and texture verts
#----------------------------------------------------------

def import_obj(filepath):
    name = os.path.basename(filepath)
    fp = open(filepath, "rU")  
    print("Importing %s" % filepath)

    verts = []
    faces = []
    texverts = []
    texfaces = []

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
        else:
            pass
    print("%s successfully imported" % filepath)
    fp.close()

    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()

    if texverts:
        uvtex = me.uv_textures.new()
        uvtex.name = name
        data = uvtex.data
        for n in range(len(texfaces)):
            tf = texfaces[n]
            data[n].uv1 = texverts[tf[0]]
            data[n].uv2 = texverts[tf[1]]
            data[n].uv3 = texverts[tf[2]]
            if len(tf) == 4:
                data[n].uv4 = texverts[tf[3]]

    scn = bpy.context.scene
    ob = bpy.data.objects.new(name, me)
    scn.objects.link(ob)
    scn.objects.active = ob
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

class VIEW3D_OT_ImportBaseButton(bpy.types.Operator):
    bl_idname = "mh.import_base"
    bl_label = "Import base"

    filename_ext = ".mhclo"
    filter_glob = StringProperty(default="*.mhclo", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for mhclo file", 
        maxlen= 1024, default= "")

    def execute(self, context):
        global theProxy
        theProxy = readProxyFile(self.properties.filepath)
        ob = import_obj(theProxy.obj_file)
        ob["MakeTarget"] = "Base"
        ob["ProxyFile"] = self.properties.filepath
        ob["ObjFile"] = theProxy.obj_file
        setupVertexPairs(context)
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
    ob = findBase(context)
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
    print("Did not find mirror image for vertices")
    for n,data in enumerate(verts):
        (z,y,x,vn) = data
        n1 = n - 20
        n2 = n + 20
        if n1 < 0: n1 = 0
        if n2 >= nmax: n2 = nmax
        vmir = findVert(verts[n1:n2], vn, -x, y, z)
        if x > Epsilon and vmir >= 0:
            Left[vn] = vmir
        elif x < Epsilon and vmir >= 0:
            Right[vn] = vmir
        else:
            Mid[vn] = vn
        #for (lv,rv) in Left.items():
        #    print("* ", lv, ob.data.vertices[lv].co)
        #    print("  ", rv, ob.data.vertices[rv].co)
    print("end")        
    return
    
def findVert(verts, v, x, y, z):
    for (z1,y1,x1,v1) in verts:
        dx = x-x1
        dy = y-y1
        dz = z-z1
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < Epsilon:
            return v1
    if abs(x) > Epsilon:            
        print("  %d at (%.4f %.4f %.4f)" % (v, x, y, z))
    return -1            

#----------------------------------------------------------
#   loadTarget(filepath, context):
#----------------------------------------------------------

def loadTarget(filepath, context):
    realpath = os.path.realpath(os.path.expanduser(filepath))
    fp = open(realpath, "rU")  
    print("Loading target %s" % realpath)

    base = findBase(context)
    base.select = True
    context.scene.objects.active = base
    print("Old", context.object)
    bpy.ops.object.duplicate(linked=False)
    ob = context.object
    print("New", ob)
    name = os.path.basename(filepath)
    ob.name = name
    ob.data.name = name
    ob["MakeTarget"] = "Target"
    ob["FilePath"] = realpath
    ob["ProxyFile"] = base["ProxyFile"]
    for line in fp:
        words = line.split()
        if len(words) == 0:
            pass
        else:
            index = int(words[0])
            dx = float(words[1])
            dy = float(words[2])
            dz = float(words[3])
            vec = ob.data.vertices[index].co
            vec[0] += dx
            vec[1] += -dz
            vec[2] += dy
    fp.close()     
    base.hide = True
    print("Target loaded")
    return


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
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#----------------------------------------------------------
#   saveTarget(context):
#----------------------------------------------------------

def saveTarget(context):
    ob = context.object
    scn = context.scene
    if not isTarget(ob):
        raise NameError("%s is not a target")
    base = findBase(context)
    filepath = ob["FilePath"] 
    fp = open(filepath, "w")  
    print("Saving target %s to %s" % (ob, filepath))
    
    for n,v in enumerate(ob.data.vertices):
        bv = base.data.vertices[n]
        vec = v.co - bv.co
        if vec.length > Epsilon:
            fp.write("%d %.6f %.6f %.6f\n" % (n, vec[0], vec[2], -vec[1]))
    fp.close()    
    base.hide = False
    scn.objects.active = base
    scn.objects.unlink(ob)
    print("Target saved and deleted")
    return
                            
class VIEW3D_OT_SaveTargetButton(bpy.types.Operator):
    bl_idname = "mh.save_target"
    bl_label = "Save target"

    def execute(self, context):
        saveTarget(context)
        return{'FINISHED'}            

#----------------------------------------------------------
#   fitTarget(context):
#----------------------------------------------------------

def fitTarget(context):
    global theProxy
    ob = context.object
    scn = context.scene
    if not isTarget(ob):
        return
    if not theProxy:
        print("Rereading %s" % ob["ProxyFile"])
        theProxy = readProxyFile(ob["ProxyFile"])
    theProxy.update(ob.data)
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
    scn = context.scene
    if not isTarget(ob):
        return
    base = findBase(context)
    base.hide = False
    scn.objects.active = base
    scn.objects.unlink(ob)
    return

class VIEW3D_OT_DiscardTargetButton(bpy.types.Operator):
    bl_idname = "mh.discard_target"
    bl_label = "Discard target"

    def execute(self, context):
        discardTarget(context)
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
    verts = ob.data.vertices
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
        else:
            lv[0] = -rv[0]
            lv[1] = rv[1]
            lv[2] = rv[2]
    print("Target symmetrized")
    return

class VIEW3D_OT_SymmetrizeTargetButton(bpy.types.Operator):
    bl_idname = "mh.symmetrize_target"
    bl_label = "Symmetrize"
    left2right = BoolProperty()

    def execute(self, context):
        symmetrizeTarget(context, self.left2right)
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
        return (ob["MakeTarget"] == "Base")
    except:
        return False

def isTarget(ob):
    try:
        return (ob["MakeTarget"] == "Target")
    except:
        return False

#----------------------------------------------------------
#   class MakeTargetPanel(bpy.types.Panel):
#----------------------------------------------------------


class MakeTargetPanel(bpy.types.Panel):
    bl_label = "Make target"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("mh.import_base")
        ob = context.object
        if isBase(ob):
            layout.operator("mh.load_target")
        if isTarget(ob):
            layout.operator("mh.fit_target")
            layout.operator("mh.symmetrize_target", text="Symm Left->Right").left2right = True
            layout.operator("mh.symmetrize_target", text="Symm Right->Left").left2right = False
            layout.operator("mh.discard_target")
            layout.operator("mh.save_target")           

#
#    Init and register
#
def register():
    bpy.utils.register_module(__name__)
    pass

if __name__ == "__main__":
    register()
