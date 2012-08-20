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
from bpy.props import *
import mathutils

from . import globvars as the
from . import maketarget

class CCharacter:

    def __init__(self, name):
        self.name = name
        self.files = []
        self.verts = {}
        self.landmarks = {}
        self.landmarkVerts = {}
        
        self.race = "neutral"
        self.gender = "female"
        self.age = "young"
        self.weight = "normal"
        self.tone = "normal"
        
    
    def __repr__(self):
        return (
            "<CCharacter %s\n" % self.name +
            "  race %s\n" % self.race +    
            "  gender %s\n" % self.gender +    
            "  age %s\n" % self.age +    
            "  weight %s\n" % self.weight +    
            "  tone %s\n" % self.tone +
            ">")
            
            
    def setCharacterProps(self, context):
        scn = context.scene
        self.race = scn.MhRace
        self.gender = scn.MhGender
        self.age = scn.MhAge
        self.weight = scn.MhWeight
        self.tone = scn.MhTone


    def setSceneProps(self, context):
        scn = context.scene
        scn.MhRace = self.race
        scn.MhGender = self.gender
        scn.MhAge = self.age
        scn.MhWeight = self.weight
        scn.MhTone = self.tone


    def updateFiles(self):
        if self.race == "caucasian":
            race = "neutral"
        else:
            race = self.race
        macro = race + "-" + self.gender + "-" + self.age
        self.files = [(macro, 1.0)]
        
        univ = "universal-" + self.gender + "-" + self.age
        if self.weight != "normal":
            weight = univ + "-" + self.weight        
            self.files.append( (weight, 1.0) )
        
        if self.tone != "normal":
            tone = univ + "-" + self.tone        
            self.files.append( (tone, 1.0) )
            if self.weight != "normal":
                weight = tone + "-" + self.weight        
                self.files.append( (weight, 1.0) )
                
    
    def fromFilePath(self, context, filepath, update):
        string = filepath
        for char in ["/", "\\", "-", "_", "."]:
            string = string.replace(char, " ")
        words = string.split()
        print(words)

        table = {
            "caucasian" : "race",
            "asian" : "race",
            "african" : "race",
            
            "female" : "gender",
            "male" : "gender",
            
            "child" : "age",
            "young" : "age",
            "old" : " age",

            "flaccid" : "tone",
            "muscle" : "tone",
            
            "light" : "weight",
            "heavy" : "weight",
        }
                
        if update:                
            for word in words:
                try:
                    exec("self.%s = word" % table[word])
                except KeyError:
                    continue
                print("set", table[word], word)
        else:
            for word in words:
                try:
                    prop = eval("self.%s" % table[word])
                except KeyError:
                    continue
                print("change", word, prop)
                filepath = filepath.replace(word, prop)
                print(filepath)
        
        #self.setSceneProps(context)
        self.updateFiles()
        return filepath
    
    
    def loadTargets(self, context):                
        scn = context.scene
        prefix = os.path.join(scn.MhProgramPath, "data/targets/macrodetails/")
        ext = ".target"
        base = maketarget.importBaseObj(context)
        scn.objects.active = base
        for (file, value) in self.files:
            path = os.path.join(prefix, file + ".target")
            print(path, value)
            try:
                skey = maketarget.loadTarget(path, context)
                skey.value = value
            except IOError:
                skey = None
                print("No such file", path)
                
                
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
        for (file, value) in self.files:
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
        
        
                    
    def draw(self, layout, scn):
        for (file, weight) in self.files:
            split = layout.split(0.8)
            split.label("    " + file)
            split.label("%.2f" % weight)
        if self.files:            
            layout.operator("mh.load_character", text="Load %s Character" % self.name).name = self.name


the.SourceCharacter = CCharacter("Source")
the.TargetCharacter = CCharacter("Target")


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
        char.loadTargets(context)
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
        the.SourceCharacter = CCharacter("Source")
        the.SourceCharacter.fromFilePath(context, scn.MhSourceMorphDir, True)
        the.SourceCharacter.fromFilePath(context, scn.MhSourceMorphFile, True)
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
        the.TargetCharacter.setCharacterProps(context)
        updateTargetMorph(context)
        the.TargetCharacter.updateFiles()
        return{'FINISHED'}    


def updateTargetMorph(context):
    scn = context.scene
    scn.MhTargetMorphDir = the.TargetCharacter.fromFilePath(context, scn.MhSourceMorphDir, False)
    scn.MhTargetMorphFile = the.TargetCharacter.fromFilePath(context, scn.MhSourceMorphFile, False)


#----------------------------------------------------------
#   Init
#----------------------------------------------------------

def drawItems(layout, scn):
    layout.prop(scn, "MhRace", expand=True) 
    layout.prop(scn, "MhAge", expand=True) 
    layout.prop(scn, "MhGender", expand=True) 
    layout.prop(scn, "MhWeight", expand=True) 
    layout.prop(scn, "MhTone", expand=True) 


def init():

    bpy.types.Scene.MhRace = EnumProperty(
        items = [('caucasian','caucasian','caucasian'), ('african','african','african'), ('asian','asian','asian')],
        name="Race",
        default = 'caucasian')

    bpy.types.Scene.MhAge = EnumProperty(
        items = [('child','child','child'), ('young','young','young'), ('old','old','old')],
        name="Age",
        default = 'child')

    bpy.types.Scene.MhGender = EnumProperty(
        items = [('female','female','female'), ('male','male','male')],
        name="Gender",
        default = 'female')

    bpy.types.Scene.MhWeight = EnumProperty(
        items = [('light','light','light'), ('normal','normal','normal'), ('heavy','heavy','heavy')],
        name="Weight",
        default = 'normal')

    bpy.types.Scene.MhTone = EnumProperty(
        items = [('flaccid','flaccid','flaccid'), ('normal','normal','normal'), ('muscle','muscle','muscle')],
        name="Age",
        default = 'normal')
        
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
        

