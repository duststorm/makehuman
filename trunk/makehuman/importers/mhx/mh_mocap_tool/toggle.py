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

#
#    togglePoleTargets(trgRig):
#

def togglePoleTargets(trgRig):
    bones = trgRig.data.bones
    pbones = trgRig.pose.bones
    if bones['ElbowPT_L'].hide:
        hide = False
        poletar = trgRig
        res = 'ON'
        trgRig.MhxTogglePoleTargets = True
    else:
        hide = True
        poletar = None
        res = 'OFF'
        trgRig.MhxTogglePoleTargets = False
    for suffix in ['_L', '_R']:
        for name in ['ElbowPT', 'ElbowLinkPT', 'Elbow', 'KneePT', 'KneeLinkPT', 'Knee']:
            try:
                bones[name+suffix].hide = hide
            except:
                pass
        cns = pbones['LoArm'+suffix].constraints['ArmIK']
        cns = pbones['LoLeg'+suffix].constraints['LegIK']
        cns.pole_target = poletar
    return res

#
#    toggleIKLimits(trgRig):
#

def toggleIKLimits(trgRig):
    pbones = trgRig.pose.bones
    if pbones['UpLeg_L'].use_ik_limit_x:
        use = False
        res = 'OFF'
        trgRig.MhxToggleIkLimits = False
    else:
        use = True
        res = 'ON'
        trgRig.MhxToggleIkLimits = True
    for suffix in ['_L', '_R']:
        for name in ['UpArm', 'LoArm', 'UpLeg', 'LoLeg']:
            pb = pbones[name+suffix]
            pb.use_ik_limit_x = use
            pb.use_ik_limit_y = use
            pb.use_ik_limit_z = use
    return res

#
#    toggleLimitConstraints(trgRig):
#    setLimitConstraints(trgRig, inf):
#

def toggleLimitConstraints(trgRig):
    pbones = trgRig.pose.bones
    first = True
    trgRig.MhxToggleLimitConstraints = False
    for pb in pbones:
        if onUserLayer(pb.bone.layers):
            for cns in pb.constraints:
                if (cns.type == 'LIMIT_LOCATION' or
                    cns.type == 'LIMIT_ROTATION' or
                    cns.type == 'LIMIT_DISTANCE' or
                    cns.type == 'LIMIT_SCALE'):
                    if first:
                        first = False
                        if cns.influence > 0.5:
                            inf = 0.0
                            res = 'OFF'
                        else:
                            inf = 1.0
                            res = 'ON'
                            trgRig.MhxToggleLimitConstraints = True
                    cns.influence = inf
    if first:
        return 'NOT FOUND'
    return res

def onUserLayer(layers):
    for n in [0,1,2,3,4,5,6,7, 9,10,11,12,13]:
        if layers[n]:
            return True
    return False

def setLimitConstraints(trgRig, inf):
    pbones = trgRig.pose.bones
    for pb in pbones:
        if onUserLayer(pb.bone.layers):
            for cns in pb.constraints:
                if (cns.type == 'LIMIT_LOCATION' or
                    cns.type == 'LIMIT_ROTATION' or
                    cns.type == 'LIMIT_DISTANCE' or
                    cns.type == 'LIMIT_SCALE'):
                    cns.influence = inf
    return

#
#    silenceConstraints(rig):
#

def silenceConstraints(rig):
    for pb in rig.pose.bones:
        pb.lock_location = (False, False, False)
        pb.lock_rotation = (False, False, False)
        pb.lock_scale = (False, False, False)
        for cns in pb.constraints:
            if cns.type == 'CHILD_OF':
                cns.influence = 0.0
            elif False and (cns.type == 'LIMIT_LOCATION' or
                cns.type == 'LIMIT_ROTATION' or
                cns.type == 'LIMIT_DISTANCE' or
                cns.type == 'LIMIT_SCALE'):
                cns.influence = 0.0
    return




