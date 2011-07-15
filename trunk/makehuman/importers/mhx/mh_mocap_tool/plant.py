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
from . import simplify

#
#    plantKeys(context)
#    plantFCurves(fcurves, first, last):
#

def plantKeys(context):
    rig = context.object
    scn = context.scene
    if not rig.animation_data:
        print("Cannot plant: no animation data")
        return
    act = rig.animation_data.action
    if not act:
        print("Cannot plant: no action")
        return
    bone = rig.data.bones.active
    if not bone:
        print("Cannot plant: no active bone")
        return

    (first, last) = simplify.getMarkedTime(scn)
    if first == None:
        print("Cannot plant: need two selected time markers")
        return

    pb = rig.pose.bones[bone.name]
    locPath = 'pose.bones["%s"].location' % bone.name
    if pb.rotation_mode == 'QUATERNION':
        rotPath = 'pose.bones["%s"].rotation_quaternion' % bone.name
        pbRot = pb.rotation_quaternion
    else:
        rotPath = 'pose.bones["%s"].rotation_euler' % bone.name
        pbRot = pb.rotation_euler
    rots = []
    locs = []
    for fcu in act.fcurves:
        if fcu.data_path == locPath:
            locs.append(fcu)
        if fcu.data_path == rotPath:
            rots.append(fcu)

    useCrnt = scn['MhxPlantCurrent']
    if scn['MhxPlantLoc']:
        plantFCurves(locs, first, last, useCrnt, pb.location)
    if scn['MhxPlantRot']:
        plantFCurves(rots, first, last, useCrnt, pbRot)
    return

def plantFCurves(fcurves, first, last, useCrnt, values):
    for fcu in fcurves:
        print("Plant", fcu.data_path, fcu.array_index)
        kpts = fcu.keyframe_points
        sum = 0.0
        dellist = []
        firstx = first - 1e-4
        lastx = last + 1e-4
        print("Btw", firstx, lastx)
        for kp in kpts:
            (x,y) = kp.co
            if x > firstx and x < lastx:
                dellist.append(kp)
                sum += y
        nterms = len(dellist)
        if nterms == 0:
            return
        if useCrnt:
            ave = values[fcu.array_index]
            print("Current", ave)
        else:
            ave = sum/nterms
        for kp in dellist:
            kp.co[1] = ave
        kpts.insert(first, ave, options='FAST')
        kpts.insert(last, ave)
    return
        
