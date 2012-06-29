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

from . import maketarget

#----------------------------------------------------------
#   loadMhmFile(context):
#----------------------------------------------------------

class CMhmFile:
    def __init__(self):

        self.gender = {}
        self.gender["male"] = 0.5
        self.gender["female"] = 0.5
        
        self.age = {}
        self.age["young"] = 1.0

        self.race = {}
        self.race["neutral"] = 1.0
        self.race["african"] = 0.0
        self.race["asian"] = 0.0
        
        self.weight = {}
        self.tone = {}        
        self.stature = {}
        
        self.breastPosition = {}
        self.breastPoint = {}
        self.breastFirmness = {}
        self.breastSize = {}
        self.breastDistance = {}

        self.genitals = {}
        self.pelvistone = {}
        self.stomach = {}
        self.buttocks = {}
        
        
    def __repr__(self):
        string = "<MHM\n" 
        for (key,value) in self.gender.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.age.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.race.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.weight.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.tone.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.stature.items(): string += "%s %.3f, " % (key, value)

        for (key,value) in self.breastPosition.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.breastPoint.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.breastFirmness.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.breastSize.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.breastDistance.items(): string += "%s %.3f, " % (key, value)

        for (key,value) in self.genitals.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.pelvistone.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.stomach.items(): string += "%s %.3f, " % (key, value)
        for (key,value) in self.buttocks.items(): string += "%s %.3f, " % (key, value)
        string += ">"        
        return string
            
        
        
    def setValuePosPair(self, key, value, struct, small, big):            
        value = float(value)  
        if value < 0.5:
            struct[small] = 1-2*value
            struct[big] = 0
        else:
            struct[small] = 0
            struct[big] = 2*value-1


    def setValuePair(self, key, value, struct, small, big):            
        value = float(value)  
        if value < 0.0:
            struct[small] = 1-value
            struct[big] = 0
        else:
            struct[small] = 0
            struct[big] = value


    def setSlider(self, key, value):      
        if key == "gender":
            value = float(value)  
            self.gender["female"] = 1-value
            self.gender["male"] = value
        elif key == "age":
            value = float(value)    
            if value < 0.5:
                self.age["child"] = 1-2*value
                self.age["young"] = 2*value
            else:
                self.age["young"] = 2-2*value
                self.age["old"] = 2*value-1            
        elif key == "muscle":
            self.setValuePosPair(key, value, self.tone, "flaccid", "muscle")
        elif key == "weight":
            self.setValuePosPair(key, value, self.weight, "light", "heavy")
        elif key == "height":
            self.setValuePair(key, value, self.stature, "dwarf", "giant")
        elif key == "african":
            self.race["african"] = float(value)
        elif key == "asian":
            self.race["asian"] = float(value)

        elif key == "breastPosition":
            self.setValuePair(key, value, self.breastPosition, "down", "up")
        elif key == "breastPoint":
            self.setValuePair(key, value, self.breastPoint, "point-min", "point-max")
        elif key == "breastFirmness":
            self.setValuePosPair(key, value, self.breastFirmness, "firmness0", "firmness1")
        elif key == "breastSize":
            self.setValuePair(key, value, self.breastSize, "cup1", "cup2")
        elif key == "breastDistance":
            self.setValuePair(key, value, self.breastDistance, "dist-min", "dist-max")
        
        elif key == "genitals":
            self.setValuePair(key, value, self.genitals, "feminine", "masculine")
        elif key == "pelvistone":
            self.setValuePair(key, value, self.pelvistone, "pelvis-tone1", "pelvis-tone2")
        elif key == "stomach":
            self.setValuePair(key, value, self.stomach, "stomach1", "stomach2")
        elif key == "buttocks":
            self.setValuePair(key, value, self.buttocks, "cup1", "cup2")
        else:
            print("  skip %s" % key)
    
        sum = self.race["african"] + self.race["asian"] 
        if sum > 1.0:
            self.race["african"] /= sum
            self.race["asian"] /= sum
            self.race["neutral"] = 0.0
        else:        
            self.race["neutral"] = 1 - sum
            
            
    def loopItems(self, context, glue, path, structs, value):
        structs.reverse()
        self.loopItems1(context, glue, path, structs, value, "  ")

    def loopItems1(self, context, glue, path, structs, value, pad):        
        if value < 1e-4:
            return
        elif structs == []:
            self.loadTarget(context, "%s.target" % path[:-1], value)
        else:
            rest = list(structs)
            struct = rest.pop()
            for (key, val) in struct.items():
                self.loopItems1(context, glue, "%s%s%s" % (path, key, glue), rest, value*val, pad+"  ")
            

    def loadTarget(self, context, file, value):
        if value > 0.01:
            path = os.path.join(context.scene.MhProgramPath, "data/targets", file)
            #print(path, value)
            try:
                skey = maketarget.loadTarget(path, context)
            except IOError:
                skey = None
            if skey:
                skey.value = value
            else:
                print("No such file", path)
        return

            
    def setAllItems(self, context):
        female = self.gender["female"]
        
        self.loopItems(context, "-", "macrodetails/", [self.race, self.gender, self.age], 1.0)
        self.loopItems(context, "-", "macrodetails/universal-", [self.gender, self.age, self.weight], 1.0)
        self.loopItems(context, "-", "macrodetails/universal-", [self.gender, self.age, self.tone], 1.0)
        self.loopItems(context, "-", "macrodetails/universal-", [self.gender, self.age, self.weight, self.tone], 1.0)
        self.loopItems(context, "-", "macrodetails/universal-stature-", [self.stature], 1.0)

        self.loopItems(context, "-", "breast/breast-", [self.breastPosition], 1.0)
        self.loopItems(context, "-", "breast/breast-", [self.breastDistance], 1.0)
        self.loopItems(context, "-", "breast/female-", [self.age, self.breastSize, self.breastFirmness], female)
        self.loopItems(context, "-", "breast/female-", [self.age, self.weight, self.breastSize, self.breastFirmness], female)
        self.loopItems(context, "-", "breast/female-", [self.age, self.tone, self.breastSize, self.breastFirmness], female)
        self.loopItems(context, "-", "breast/female-", [self.age, self.weight, self.tone, self.breastSize, self.breastFirmness], female)

        self.loopItems(context, "_", "details/genitals_", [self.gender, self.genitals, self.age], 1.0)
        self.loopItems(context, "-", "details/", [self.gender, self.age, self.pelvistone], 1.0)
        self.loopItems(context, "-", "details/", [self.gender, self.age, self.stomach], 1.0)
        self.loopItems(context, "-", "details/", [self.gender, self.age, self.tone, self.stomach], 1.0)
        self.loopItems(context, "-", "details/", [self.gender, self.age, self.weight, self.stomach], 1.0)
        self.loopItems(context, "-", "details/", [self.gender, self.age, self.tone, self.weight, self.stomach], 1.0)
    
    
MhmDisplay = [
    ("Macro", ["gender", "age", "muscle", "weight", "height", "african", "asian"]),
    ("", ["genitals", "buttocks", "stomach", "pelvisTone"]),
    ("Breasts", ["breastPoint", "breastFirmness", "breastSize", "breastPosition", "breastDistance"]),
]

    
MhmNameProps = {
    "gender" : "MhGender",
    "age" : "MhAge",
    "muscle" : "MhMuscle",
    "weight" : "MhWeight",
    "height" : "MhHeight",
    "african" : "MhAfrican",
    "asian" : "MhAsian",
    
    "genitals" : "MhGenitals",
    "buttocks" : "MhButtocks",
    "stomach" : "MhStomach",
    "pelvisTone" : "MhPelvisTone",
    
    "breastPoint" : "MhBreastPoint",
    "breastFirmness" : "MhBreastFirmness",
    "breastSize" : "MhBreastSize",
    "breastPosition" : "MhBreastPosition",
    "breastDistance" : "MhBreastDistance",
}
    
    
def updateSlider(context, prop, name):
    me = context.object.data
    mhm = CMhmFile()
    mhm.setSlider(name, eval("me.%s" % prop))
    print(mhm)
    mhm.setAllItems(context)              
    return
    

class VIEW3D_OT_UpdateSliderButton(bpy.types.Operator):
    bl_idname = "mh.update_slider"
    bl_label = "Update Slider"
    bl_options = {'UNDO'}
    name = StringProperty()

    def execute(self, context):
        updateSlider(context, self.name)
        print("Slider %s updated" % self.name)
        return {'FINISHED'}

  
def updateAllSliders(context):
    me = context.object.data
    mhm = CMhmFile()
    maketarget.discardAllTargets(context)
    for name,prop in MhmNameProps.items():
        mhm.setSlider(name, eval("me.%s" % prop))
    print(mhm)
    mhm.setAllItems(context)              
    return
    

class VIEW3D_OT_UpdateAllSlidersButton(bpy.types.Operator):
    bl_idname = "mh.update_all_sliders"
    bl_label = "Update All Sliders"
    bl_options = {'UNDO'}

    def execute(self, context):
        updateAllSliders(context)
        print("All sliders updated")
        return {'FINISHED'}


def resetAllSliders(context):
    me = context.object.data
    maketarget.discardAllTargets(context)
    for name,prop in MhmNameProps.items():
        try:
            del me[prop]
        except:
            continue
    return
    

class VIEW3D_OT_ResetAllSlidersButton(bpy.types.Operator):
    bl_idname = "mh.reset_all_sliders"
    bl_label = "Reset All Sliders"
    bl_options = {'UNDO'}

    def execute(self, context):
        resetAllSliders(context)
        print("All sliders reset")
        return {'FINISHED'}

   
def loadMhmFile(filepath, context):
    maketarget.discardAllTargets(context)
    me = context.object.data
    realpath = os.path.realpath(os.path.expanduser(filepath))
    fp = open(realpath, "rU")  
    print("Loading mhm file %s" % realpath)
    mhm = CMhmFile()
    for line in fp:
        words = line.split()
        key = words[0]
        try:
            prop = MhmNameProps[key]
        except:
            continue
        value = float(words[1])
        me[prop] = value
        mhm.setSlider(key, value)
    print(mhm)
    fp.close()    
    mhm.setAllItems(context)              
    return                

  
class VIEW3D_OT_LoadMhmFileButton(bpy.types.Operator):
    bl_idname = "mh.load_mhm_file"
    bl_label = "Load mhm file"
    bl_options = {'UNDO'}

    filename_ext = ".mhm"
    filter_glob = StringProperty(default="*.mhm", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for mhm file", 
        maxlen= 1024, default= "")

    def execute(self, context):
        loadMhmFile(self.properties.filepath, context)
        print("Mhm file loaded")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def init():
    bpy.types.Mesh.MhGender = FloatProperty(name = "Gender", min = 0.0, max = 1.0, default = 0.5)
    bpy.types.Mesh.MhAge = FloatProperty(name = "Age",  min = 0.0, max = 1.0, default = 0.5)
    bpy.types.Mesh.MhMuscle = FloatProperty(name = "Tone", min = 0.0, max = 1.0, default = 0.5)
    bpy.types.Mesh.MhWeight = FloatProperty(name = "Weight", min = 0.0, max = 1.0, default = 0.5)
    bpy.types.Mesh.MhHeight = FloatProperty(name = "Height", min = -1.0, max = 1.0, default = 0.0)
    bpy.types.Mesh.MhAfrican = FloatProperty(name = "African", min = 0.0, max = 1.0, default = 0.0)
    bpy.types.Mesh.MhAsian = FloatProperty(name = "Asian", min = 0.0, max = 1.0, default = 0.0)

    bpy.types.Mesh.MhGenitals = FloatProperty(name = "Genitalia", min = -1.0, max = 1.0, default = 0.0)
    bpy.types.Mesh.MhButtocks = FloatProperty(name = "Buttocks", min = -1.0, max = 1.0, default = 0.0)
    bpy.types.Mesh.MhStomach = FloatProperty(name = "Stomach", min = -1.0, max = 1.0, default = 0.0)
    bpy.types.Mesh.MhPelvisTone = FloatProperty(name = "Pelvis Tone", min = -1.0, max = 1.0, default = 0.0)

    bpy.types.Mesh.MhBreastPoint = FloatProperty(name = "Breast Taper", min = -1.0, max = 1.0, default = 0.0)
    bpy.types.Mesh.MhBreastFirmness = FloatProperty(name = "Breast Firmness", min = -1.0, max = 1.0,default = 0.0)
    bpy.types.Mesh.MhBreastSize = FloatProperty(name = "Breast Size", min = -1.0, max = 1.0, default = 0.0)
    bpy.types.Mesh.MhBreastPosition = FloatProperty(name = "Breast Position", min = -1.0, max = 1.0, default = 0.0)
    bpy.types.Mesh.MhBreastDistance = FloatProperty(name = "Breast Distance", min = -1.0, max = 1.0, default = 0.0)
    