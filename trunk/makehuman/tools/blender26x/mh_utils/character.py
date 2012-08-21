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

from . import globvars as the
from . import utils
from . import import_obj

class CCharacter:

    def __init__(self, name):
        self.name = name
        self.files = []
        
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
        base = import_obj.importBaseObj(context)
        scn.objects.active = base
        for (file, value) in self.files:
            path = os.path.join(prefix, file + ".target")
            print(path, value)
            try:
                skey = utils.loadTarget(path, context)
                skey.value = value
            except IOError:
                skey = None
                print("No such file", path)
                                        
                    
    def draw(self, layout, scn):
        layout.label("Files:")
        box = layout.box()
        for (file, weight) in self.files:
            split = box.split(0.8)
            split.label("    " + file)
            split.label("%.2f" % weight)
        if self.files:            
            layout.operator("mh.load_character", text="Load %s Character" % self.name).name = self.name


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
        

