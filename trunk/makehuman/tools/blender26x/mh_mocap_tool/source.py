# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; eithe.r version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the.
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



import bpy, os
#from math import sin, cos
from mathutils import *
from bpy.props import *
from bpy_extras.io_utils import ImportHelper

from . import target
from . import globvar as the
from . import utils
from .utils import MocapError
              
#
#    guessSrcArmature(rig, scn):
#

def guessSrcArmature(rig, scn):
    ensureSourceInited(scn)
    bestMisses = 1000
    misses = {}
    bones = rig.data.bones
    for name in the.sourceArmatures.keys():
        amt = the.sourceArmatures[name]
        nMisses = 0
        for bone in bones:
            try:
                amt[bone.name.lower()]
            except:
                nMisses += 1
        misses[name] = nMisses
        if nMisses < bestMisses:
            best = amt
            bestName = name
            bestMisses = nMisses
    if bestMisses == 0:
        scn.McpSourceRig = name
    else:
        for bone in bones:
            print("'%s'" % bone.name)
        for (name, n) in misses.items():
            print(name, n)
        raise MocapError('Did not find matching armature. nMisses = %d' % bestMisses)
    return (best, bestName)

#
#   findSrcArmature(context, rig):
#

def findSrcArmature(context, rig):
    scn = context.scene
    if scn.McpGuessSourceRig:
        (the.srcArmature, name) = guessSrcArmature(rig, scn)
    else:
        name = scn.McpSourceRig
        the.srcArmature = the.sourceArmatures[name]
    rig.McpArmature = name
    print("Using matching armature %s." % name)
    return

#
#    setArmature(rig, scn)
#

def setArmature(rig, scn):
    try:
        name = rig.McpArmature
    except:    
        name = scn.McpSourceRig
    if name:
        print("Setting armature to %s" % name)
        rig.McpArmature = name
        scn.McpSourceRig = name
    else:
        raise MocapError("No armature set")
    the.srcArmature = the.sourceArmatures[name]
    print("Set armature %s" % name)
    return
    
#
#   findSourceKey(mhx, struct):
#

def findSourceKey(mhx, struct):
    for bone in struct.keys():
        (mhx1, twist) = struct[bone]
        if mhx == mhx1:
            return (bone, twist)
    return (None, 0)
    
def getSourceRoll(mhx):
    (bone, roll) = findSourceKey(mhx, the.srcArmature)
    return roll
            
    
###############################################################################
#
#    Source initialization
#
###############################################################################


def isSourceInited(scn):
    try:
        scn.McpSourceRig
        return True
    except:
        return False


def initSources(scn):       
    the.sourceArmatures = {}
    path = os.path.join(os.path.dirname(__file__), "source_rigs")
    for fname in os.listdir(path):
        file = os.path.join(path, fname)
        (name, ext) = os.path.splitext(fname)
        if ext == ".src" and os.path.isfile(file):
            (name, armature) = readSrcArmature(file, name)
            the.sourceArmatures[name] = armature
    the.srcArmatureEnums = []
    keys = list(the.sourceArmatures.keys())
    keys.sort()
    for key in keys:
        the.srcArmatureEnums.append((key,key,key))
        
    bpy.types.Scene.McpSourceRig = EnumProperty(
        items = the.srcArmatureEnums,
        name = "Source rig",
        default = 'MB')
    scn.McpSourceRig = 'MB'
    print("Defined McpSourceRig")
    return    


def readSrcArmature(file, name):
    print("Read source file", file)
    fp = open(file, "r")
    status = 0    
    armature = {}
    for line in fp:
        words = line.split()
        if len(words) > 0:
            key = words[0].lower()
            if key[0] == "#":
                continue
            elif key == "name:":
                name = words[1]
            elif key == "armature:":
                status = 1
            elif len(words) < 3:
                print("Ignored illegal line", line)
            elif status == 1:
                for n in range(1,len(words)-2):
                    key += " " + words[n].lower()                    
                armature[key] = (utils.nameOrNone(words[-2]), float(words[-1]))
    fp.close()                
    return (name, armature)                
    

def ensureSourceInited(scn):
    if not isSourceInited(scn):
        initSources(scn)
        

class VIEW3D_OT_McpInitSourcesButton(bpy.types.Operator):
    bl_idname = "mcp.init_sources"
    bl_label = "Init Source Panel"
    bl_options = {'UNDO'}

    def execute(self, context):
        initSources(context.scene)
        return{'FINISHED'}    
