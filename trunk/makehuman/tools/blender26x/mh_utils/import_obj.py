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
import sys
import math
import random
from mathutils import Vector
from bpy.props import *
from bpy_extras.io_utils import ExportHelper, ImportHelper

from . import globvars as the
from . import utils
from . import proxy

#----------------------------------------------------------
#   importBaseObj(context):
#   Simple obj importer which reads only verts, faces, and texture verts
#----------------------------------------------------------

def importBaseObj(context):
    the.Proxy = None
    filepath = os.path.join(context.scene.MhProgramPath, "data/3dobjs/base.obj")
    ob = importObj(filepath, context)
    ob["NTargets"] = 0
    ob["ProxyFile"] = 0
    ob["ObjFile"] =  filepath
    ob["MhxMesh"] = True
    utils.setupVertexPairs(context, True)
    print("Base object imported")
    return ob


def importBaseMhclo(context):
    the.Proxy = proxy.CProxy()
    filepath = os.path.join(context.scene.MhProgramPath, "data/3dobjs/base.mhclo")
    the.Proxy.read(filepath)
    ob = importObj(the.Proxy.obj_file, context)
    ob["NTargets"] = 0
    ob["ProxyFile"] = filepath
    ob["ObjFile"] = the.Proxy.obj_file
    ob["MhxMesh"] = True
    utils.setupVertexPairs(context, True)
    print("Base object imported")
    print(the.Proxy)
    return ob
    

#----------------------------------------------------------
#   importObj(filepath, context):
#   Simple obj importer which reads only verts, faces, and texture verts
#----------------------------------------------------------

def importObj(filepath, context):
    scn = context.scene
    obname = utils.nameFromPath(filepath)
    fp = open(filepath, "rU")  
    print("Importing %s" % filepath)

    verts = []
    faces = []
    texverts = []
    texfaces = []
    groups = {}
    materials = {}

    group = []
    matlist = []
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
    
    try:
        me.polygons
        the.BMeshAware = True
        print("Using BMesh")
    except:
        the.BMeshAware = False
        print("Not using BMesh")

    if texverts:
        if the.BMeshAware:
            addUvLayerBMesh(obname, me, texverts, texfaces)
        else:
            addUvLayerNoBMesh(obname, me, texverts, texfaces)
                
    if scn.MhLoadMaterial == 'Groups':
        addMaterials(groups, me, "Group")
    elif scn.MhLoadMaterial == 'Materials':
        addMaterials(materials, me, "Material")
        for (name,group) in groups.items():
            vgrp = ob.vertex_groups.new(name=name)
            if vgrp.name != name:
                print("WARNING: Group name %s => %s" % (name, vgrp.name))
            if the.BMeshAware:
                for nf in group:
                    f = me.polygons[nf]
                    for v in f.vertices:
                        vgrp.add([v], 1.0, 'REPLACE')
            else:
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


def addUvLayerBMesh(obname, me, texverts, texfaces):            
    uvtex = me.uv_textures.new(name=obname)
    uvloop = me.uv_layers[-1]
    data = uvloop.data
    n = 0
    for tf in texfaces:
        data[n].uv = texverts[tf[0]]
        n += 1
        data[n].uv = texverts[tf[1]]
        n += 1
        data[n].uv = texverts[tf[2]]
        n += 1
        if len(tf) == 4:
            data[n].uv = texverts[tf[3]]
            n += 1
    return


def addUvLayerNoBMesh(obname, me, texverts, texfaces):            
        uvtex = me.uv_textures.new(name=obname)
        data = uvtex.data
        for n in range(len(texfaces)):
            tf = texfaces[n]
            data[n].uv1 = texverts[tf[0]]
            data[n].uv2 = texverts[tf[1]]
            data[n].uv3 = texverts[tf[2]]
            if len(tf) == 4:
                data[n].uv4 = texverts[tf[3]]


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
        if the.BMeshAware:
            for nf in group:
                f = me.polygons[nf]
                f.material_index = mn
        else:
            for nf in group:
                f = me.faces[nf]
                f.material_index = mn
        mn += 1
    return        
