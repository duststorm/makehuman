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
import os
import math

from . import globvars as the
  
#----------------------------------------------------------
#   Common panel parts
#----------------------------------------------------------

def drawConfirm(layout, scn):        
    #if not maketarget.isInited(scn):
    #    layout.operator("mh.init")
    #    return False
    if the.Confirm:
        layout.label(the.ConfirmString)            
        if the.ConfirmString2:
           layout.label(the.ConfirmString2)            
        layout.operator(the.Confirm, text="Yes") 
        layout.operator("mh.skip")
        return False
    return True
            
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

def deleteAll(context):
    scn = context.scene
    for ob in scn.objects:
        if isBaseOrTarget(ob):
            scn.objects.unlink(ob)
    return                    

def nameFromPath(filepath):
    (name,ext) = os.path.splitext(os.path.basename(filepath))
    return name


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

#----------------------------------------------------------
#   setupVertexPairs(ob, insist):
#----------------------------------------------------------

the.Left = {}
the.Right = {}
the.Mid = {}

def setupVertexPairs(context, insist):
    if the.Left.keys() and not insist:
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
    the.Left = {}
    the.Right = {}
    the.Mid = {}
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
            the.Mid[vn] = vn
        elif x > the.Epsilon:
            the.Left[vn] = vmir
        elif x < -the.Epsilon:
            the.Right[vn] = vmir
        else:
            the.Mid[vn] = vmir
    if notfound:            
        print("Did not find mirror image for vertices:")
        for msg in notfound:
            print(msg)
    print("the.Left-right-mid", len(the.Left.keys()), len(the.Right.keys()), len(the.Mid.keys()))
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
    name = nameFromPath(filepath)
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
