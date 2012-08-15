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
import random
from mathutils import Vector
from bpy.props import *
from bpy_extras.io_utils import ExportHelper, ImportHelper

from . import proxy
from . import import_obj

#----------------------------------------------------------
#   class CMask
#----------------------------------------------------------

class CMask:
    def __init__(self):
        self.gender = {}
        self.gender["male"] = 0.5
        self.gender["female"] = 0.5
        
        self.age = {}
        self.age["child"] = 0.0
        self.age["young"] = 1.0
        self.age["old"] = 0.0


    def setSliders(self, scn):      
        value = scn.MhGender
        self.gender["female"] = 1-value
        self.gender["male"] = value
        
        value = scn.MhAge
        if value < 0.5:
            self.age["child"] = 1-2*value
            self.age["young"] = 2*value
        else:
            self.age["young"] = 2-2*value
            self.age["old"] = 2*value-1            


#----------------------------------------------------------
#   Generate mask
#----------------------------------------------------------

class VIEW3D_OT_GenerateMaskButton(bpy.types.Operator):
    bl_idname = "mh.generate_mask"
    bl_label = "Generate Mask"
    bl_options = {'UNDO'}
    delete = BoolProperty()

    def execute(self, context):
        return{'FINISHED'}    


#----------------------------------------------------------
#   Generate face
#----------------------------------------------------------

class VIEW3D_OT_GenerateFaceButton(bpy.types.Operator):
    bl_idname = "mh.generate_face"
    bl_label = "Generate Face"
    bl_options = {'UNDO'}
    delete = BoolProperty()

    def execute(self, context):
        return{'FINISHED'}    


#----------------------------------------------------------
#   Utilities
#----------------------------------------------------------

def isMask(ob):
    try:
        return (ob["MhAge"] == 0)
    except:
        return False


#----------------------------------------------------------
#   Init
#----------------------------------------------------------

def init():

    bpy.types.Scene.MhAge = FloatProperty(
        name = "Age",
        default = 0.5,
        min = 0.0, max = 1.0,
    )        

    bpy.types.Scene.MhGender = FloatProperty(
        name = "Gender",
        default = 0.5,
        min = 0.0, max = 1.0,
    )        
    return  
    
