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
from bpy.props import *
import mathutils

from mh_utils import globvars as the
from mh_utils import utils
from mh_utils import character
from mh_utils import warp

class CWarpCharacter:

    def __init__(self, name):
        self.character = character.CCharacter(name)
        self.verts = {}
        self.landmarks = {}
        self.landmarkVerts = {}


    def readVerts(self, context):                
        scn = context.scene

        base = os.path.join(scn.MhProgramPath, "data/3dobjs/base.obj")
        print("Load", base)
        fp = open(base, "r")
        self.verts = {}
        n = 0
        for line in fp:
            words = line.split()
            if len(words) >= 4:
                if words[0] == "v":
                    self.verts[n] = mathutils.Vector( (float(words[1]),  float(words[2]),  float(words[3])) )
                    n += 1
        fp.close()                    
        print("   ...done")                   
        
        prefix = os.path.join(scn.MhProgramPath, "data/targets/macrodetails/")
        ext = ".target"
        for (file, value) in self.character.files:
            path = os.path.join(prefix, file + ".target")
            print("Load", path, value)
            try:
                fp = open(path, "r")
            except:
                print("No such file", path)
                continue
            for line in fp:
                words = line.split()
                if len(words) >= 4:
                    n = int(words[0])
                    self.verts[n] += value*mathutils.Vector( (float(words[1]),  float(words[2]),  float(words[3])) )
            fp.close()  
            print("   ...done")       
            
        path = os.path.join( os.path.dirname(__file__), "landmarks_body.txt")
        print("Load", path)
        self.landmarks = {}
        self.landmarkLocs = {}
        n = 0
        fp = open(path, "r")
        for line in fp:
            words = line.split()    
            m = int(words[0])
            self.landmarks[n] = m
            self.landmarkVerts[n] = self.verts[m]
            n += 1
        fp.close()
        print("   ...done")       
        
        
    def readMorph(self, path):
        print("Morph", path)
        fp = open(path, "r")
        dx = {}
        for line in fp:
            words = line.split()
            if len(words) >= 4:
                n = int(words[0])
                dx[n] = mathutils.Vector( (float(words[1]),  float(words[2]),  float(words[3])) )
        fp.close()
        return dx

#----------------------------------------------------------
#   Load Character
#----------------------------------------------------------

def findCharacter(name):
    struct = {
        "Source" : the.SourceCharacter,
        "Target" : the.TargetCharacter,
    }    
    return struct[name]
    
        
class VIEW3D_OT_LoadCharacterButton(bpy.types.Operator):
    bl_idname = "mh.load_character"
    bl_label = "Load Character"
    bl_options = {'UNDO'}
    name = StringProperty()

    def execute(self, context):
        char = findCharacter(self.name)
        char.character.loadTargets(context)
        return{'FINISHED'}    
    
        
#----------------------------------------------------------
#   Set Morph
#----------------------------------------------------------

class VIEW3D_OT_SetSourceMorphButton(bpy.types.Operator):
    bl_idname = "mh.set_source_morph"
    bl_label = "Set Source Morph"
    bl_options = {'UNDO'}

    filename_ext = ".target"
    filter_glob = StringProperty(default="*.target", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for source target file", 
        maxlen= 1024, default= "")

    def execute(self, context):
        scn = context.scene
        scn.MhSourceMorphDir = os.path.dirname(self.properties.filepath)
        scn.MhSourceMorphFile = os.path.basename(self.properties.filepath)    
        the.SourceCharacter = CWarpCharacter("Source")
        the.SourceCharacter.character.fromFilePath(context, scn.MhSourceMorphDir, True)
        the.SourceCharacter.character.fromFilePath(context, scn.MhSourceMorphFile, True)
        updateTargetMorph(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class VIEW3D_OT_UpdateTargetCharacterButton(bpy.types.Operator):
    bl_idname = "mh.update_target_character"
    bl_label = "Update Target Character"
    bl_options = {'UNDO'}

    def execute(self, context):
        the.TargetCharacter.character.setCharacterProps(context)
        updateTargetMorph(context)
        the.TargetCharacter.character.updateFiles()
        return{'FINISHED'}    


def updateTargetMorph(context):
    scn = context.scene
    scn.MhTargetMorphDir = the.TargetCharacter.character.fromFilePath(context, scn.MhSourceMorphDir, False)
    scn.MhTargetMorphFile = the.TargetCharacter.character.fromFilePath(context, scn.MhSourceMorphFile, False)

#----------------------------------------------------------
#   Warp morph
#----------------------------------------------------------

def addToMorph(dxs, x0):
    xlocs = {}
    for n in dxs.keys():
        xlocs[n] = dxs[n] + x0[n]
    return xlocs        


def subFromMorph(ylocs, y0):
    dys = {}
    for n in ylocs.keys():
        dys[n] = ylocs[n] - y0[n]
    return dys
    
    
def saveTarget(path, dxs):
    print("Saving target %s" % path)
    fp = open(path, "w")
    keys = list( dxs.keys() )
    keys.sort()
    for n in keys:
        dx = dxs[n]
        fp.write("%d %.4g %.4g %.4g\n" % (n, dx[0], dx[1], dx[2]))
    fp.close()
    print("   ... done")
    return        


def printVerts(string, verts, keys):
    print(string)
    for n in keys[0:6]:
        x = verts[n]
        print("  %d %.4g %.4g %.4g" % (n, x[0], x[1], x[2]))
        

def warpMorph(context):    
    scn = context.scene
    warpField = warp.CWarp(context)
    warpField.setupFromCharacters(context, the.SourceCharacter, the.TargetCharacter)
    srcPath = os.path.join(scn.MhSourceMorphDir, scn.MhSourceMorphFile)
    dxs = the.SourceCharacter.readMorph(srcPath)
    xlocs = addToMorph(dxs, the.SourceCharacter.verts)
    ylocs = warpField.warpLocations(xlocs)
    dys = subFromMorph(ylocs, the.TargetCharacter.verts)
    trgPath = os.path.join(scn.MhTargetMorphDir, scn.MhTargetMorphFile)
    saveTarget(trgPath, dys)            
    """
    keys = list( dxs.keys() )
    keys.sort()
    printVerts("x0", the.SourceCharacter.verts, keys)
    printVerts("y0", the.TargetCharacter.verts, keys)
    printVerts("dx", dxs, keys)
    printVerts("xlocs", xlocs, keys)
    printVerts("ylocs", ylocs, keys)
    printVerts("dy", dys, keys)
    """
    return


class VIEW3D_OT_WarpMorphButton(bpy.types.Operator):
    bl_idname = "mh.warp_morph"
    bl_label = "Warp Morph"
    bl_options = {'UNDO'}

    def execute(self, context):
        warpMorph(context)
        return{'FINISHED'}   

#----------------------------------------------------------
#   Initialization
#----------------------------------------------------------

def init():
    bpy.types.Scene.MhSourceMorphDir = StringProperty(
        name = "Source Directory",
        default = "")
        
    bpy.types.Scene.MhSourceMorphFile = StringProperty(
        name = "Source File",
        default = "")
        
    bpy.types.Scene.MhTargetMorphDir = StringProperty(
        name = "Target Directory",
        default = "")
        
    bpy.types.Scene.MhTargetMorphFile = StringProperty(
        name = "Target File",
        default = "")
        
    the.SourceCharacter = CWarpCharacter("Source")
    the.TargetCharacter = CWarpCharacter("Target")
    
    print("theS", the.SourceCharacter)
