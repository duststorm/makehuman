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



import bpy
from bpy.props import *

from . import utils
from . import target_rigs
#from .target_rigs import rig_mhx, rig_simple, rig_game, rig_second_life
from . import globvar as the

Deg2Rad = math.pi/180

#
#   getTrgBone(b):
#

def getTrgBone(b):
    try:
        return the.trgBone[b]
    except:
        return None
        
        
def renameBone(b):
    try:
        return the.Renames[b]
    except:
        return b

#
#   getTargetArmature(rig, scn):
#

def getTargetArmature(rig, scn):
    bones = rig.data.bones.keys()
    if scn.McpGuessTargetRig:
        name = guessArmature(rig, bones, scn)
    else:
        name = scn.McpTargetRig
    the.target = name        
    (boneAssoc, the.Renames, the.IkBones) = target_rigs.TargetInfo[name]
    if not testTargetRig(name, bones, boneAssoc):
        print("Bones", bones)
        raise NameError("Target armature %s does not match armature %s" % (rig.name, name))
    print("Target armature %s" % name)
    parAssoc = assocParents(rig, boneAssoc, the.Renames)                        
    return (boneAssoc, parAssoc, None)


def guessArmature(rig, bones, scn):
    print("Guessing")
    if 'KneePT_L' in bones:
        return 'MHX'
    else:
        for (name, info) in target_rigs.TargetInfo.items():
            (boneAssoc, the.Renames, the.IkBones) = info
            if testTargetRig(name, bones, boneAssoc):           
                return name
    print("Bones", bones)
    raise NameError("Did not recognize target armature %s" % rig.name)        


def assocParents(rig, boneAssoc, names):          
    parAssoc = {}
    the.trgBone = {}
    taken = { None : True }
    for (name, mhx) in boneAssoc:
        name = getName(name, names)
        the.trgBone[mhx] = name
        pb = rig.pose.bones[name]
        taken[name] = True
        parAssoc[name] = None
        while pb.parent:
            pname = getName(pb.parent.name, names)
            if taken[pname]:
                parAssoc[name] = pname
                break
    return parAssoc                 


def getName(name, names):        
    try:
        return names[name]
    except:
        return name


def testTargetRig(name, bones, rigBones):
    #print("Testing %s" % name)
    for (b, mb) in rigBones:
        if b not in bones:
            #print("Failed to find", b, mb)
            return False
    return True
        
#
#   findTargetKey(mhx, list):
#

def findTargetKey(mhx, list):
    for (bone, mhx1) in list:
        if mhx1 == mhx:
            return bone
    return None            
    
###############################################################################
#
#    Target armatures
#
###############################################################################

#    (mhx bone, text)

TargetBoneNames = [
    ('Root',        'Root bone'),
    ('Spine1',        'Lower spine'),
    ('Spine2',        'Middle spine'),
    ('Spine3',        'Upper spine'),
    ('Neck',        'Neck'),
    ('Head',        'Head'),
    None,
    ('Clavicle_L',    'L clavicle'),
    ('UpArm_L',        'L upper arm'),
    ('LoArm_L',        'L forearm'),
    ('Hand_L',        'L hand'),
    None,
    ('Clavicle_R',    'R clavicle'),
    ('UpArm_R',        'R upper arm'),
    ('LoArm_R',        'R forearm'),
    ('Hand_R',        'R hand'),
    None,
    ('Hips',        'Hips'),
    None,
    ('Hip_L',        'L hip'),
    ('UpLeg_L',        'L thigh'),
    ('LoLeg_L',        'L shin'),
    ('Foot_L',        'L foot'),
    ('Toe_L',        'L toes'),
    None,
    ('Hip_R',        'R hip'),
    ('UpLeg_R',        'R thigh'),
    ('LoLeg_R',        'R shin'),
    ('Foot_R',        'R foot'),
    ('Toe_R',        'R toes'),
]

###############################################################################
#
#    Target initialization
#
###############################################################################


def isTargetInited(scn):
    try:
        scn.McpTargetRig
        return True
    except:
        return False


def initTargets(scn):        
    the.trgArmatureEnums = []
    keys = list(target_rigs.TargetInfo.keys())
    keys.sort()
    for key in keys:
        the.trgArmatureEnums.append((key,key,key))
        
    bpy.types.Scene.McpTargetRig = EnumProperty(
        items = the.trgArmatureEnums,
        name = "Target rig",
        default = 'MHX')
    scn.McpTargetRig = 'MHX'
    print("Defined McpTargetRig")
    return    
       

def ensureTargetInited(scn):
    if not isTargetInited(scn):
        initTargets(scn)
        

class VIEW3D_OT_McpInitTargetsButton(bpy.types.Operator):
    bl_idname = "mcp.init_targets"
    bl_label = "Init Target Panel"
    bl_options = {'UNDO'}


    def execute(self, context):
        initTargets(context.scene)
        return{'FINISHED'}    
