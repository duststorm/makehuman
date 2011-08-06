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
from math import sin, cos
from mathutils import *


#
#   invert(mat):
#

def invert(mat):
    inv = mat.copy()
    inv.invert()
    return inv

"""
#
#   getBone(rig, bone)
#

def getBone(rig, bone):
    try:
        return rig[bone]
    except:
        return bone
""" 
#
#   getBone(name, rig):        
#

def getBone(name, rig): 
    try:
        return rig.pose.bones[rig[name]]
    except:
        pass
    print(rig["MhxRigType"])
    try:
        mhxRig = rig["MhxRigType"]
    except:
        return None    
    if mhxRig == "MHX":
        return rig.pose.bones[name]
    elif mhxRig == "Rigify":
        print("Not yet")
    return None        
 
#
#   activeFrames(ob):
#

def activeFrames(ob):
    active = {}
    act = ob.animation_data.action
    if not act:
        return []
    for fcu in act.fcurves:
        for kp in fcu.keyframe_points:
            active[kp.co[0]] = True
    frames = list(active.keys())
    frames.sort()
    return frames

#
#   fCurveIdentity(fcu):
#

def fCurveIdentity(fcu):
    words = fcu.data_path.split('"')
    name = words[1]
    words = fcu.data_path.split('.')
    mode = words[-1]
    return (name, mode)

#
#    setRotation(pb, mat, frame, group):
#

def setRotation(pb, rot, frame, group):
    if pb.rotation_mode == 'QUATERNION':
        try:
            quat = rot.to_quaternion()
        except:
            quat = rot
        pb.rotation_quaternion = quat
        for n in range(4):
            pb.keyframe_insert('rotation_quaternion', index=n, frame=frame, group=group)
    else:
        try:
            euler = rot.to_euler(pb.rotation_mode)
        except:
            euler = rot
        pb.rotation_euler = euler
        for n in range(3):
            pb.keyframe_insert('rotation_euler', index=n, frame=frame, group=group)

#
#    setInterpolation(rig):
#

def setInterpolation(rig):
    if not rig.animation_data:
        return
    act = rig.animation_data.action
    if not act:
        return
    for fcu in act.fcurves:
        for pt in fcu.keyframe_points:
            pt.interpolation = 'LINEAR'
        fcu.extrapolation = 'CONSTANT'
    return

#
#   insertRotationKeyFrame(pb, frame):    
#

def insertRotationKeyFrame(pb, frame):    
    rotMode = pb.rotation_mode
    grp = pb.name
    if rotMode == "QUATERNION":
        pb.keyframe_insert("rotation_quaternion", frame=frame, group=grp)
    elif rotMode == "AXIS_ANGLE":
        pb.keyframe_insert("rotation_axis_angle", frame=frame, group=grp)
    else:
        pb.keyframe_insert("rotation_euler", frame=frame, group=grp)
        