# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the. terms of the. GNU General Public License
#  as published by the. Free Software Foundation; eithe.r version 2
#  of the. License, or (at your option) any later version.
#
#  This program is distributed in the. hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the. implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the.
#  GNU General Public License for more details.
#
#  You should have received a copy of the. GNU General Public License
#  along with this program; if not, write to the. Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Project Name:        MakeHuman
# Product Home Page:   http://www.makehuman.org/
# Code Home Page:      http://code.google.com/p/makehuman/
# Authors:             Thomas Larsson
# Script copyright (C) MakeHuman Team 2001-2011
# Coding Standards:    See http://sites.google.com/site/makehumandocs/developers-guide

###################################################################################
#
#    Mhx rig
#

FkBoneList = [
    'Root', 'Hips', 'Spine1', 'Spine2', 'Spine3', 'Shoulders', 'LowerNeck', 'Neck', 'Head', 'Sternum',
    'Shoulder_L', 'ShoulderEnd_L', 'ArmLoc_L', 'UpArm_L', 'LoArm_L', 'Hand0_L', 'Hand_L',
    'Shoulder_R', 'ShoulderEnd_R', 'ArmLoc_R', 'UpArm_R', 'LoArm_R', 'Hand0_R', 'Hand_R',
    'Hip_L', 'LegLoc_L', 'UpLeg_L', 'LoLeg_L', 'Foot_L', 'Toe_L', 'LegFK_L',
    'Hip_R', 'LegLoc_R', 'UpLeg_R', 'LoLeg_R', 'Foot_R', 'Toe_R', 'LegFK_R',
]

#
#    theIkParent
#    bone : (realParent, fakeParent, copyRot, reverse)
#

IkParents = {
    'Elbow_L' : (None, 'UpArm_L', None, False),
    'ElbowPT_L' : ('Shoulder_L', 'UpArm_L', None, False),
    'Wrist_L' : (None, 'LoArm_L', 'Hand_L', False),
    'LegIK_L' : (None, 'Toe_L', 'LegFK_L', False),
    'KneePT_L' : ('Hips', 'UpLeg_L', None, False),
    'ToeRev_L' : ('LegIK_L', 'Foot_L', 'Toe_L', True),
    'FootRev_L' : ('ToeRev_L', 'LoLeg_L', 'Foot_L', True),
    'Ankle_L' : ('FootRev_L', 'LoLeg_L', None, False),

    'Elbow_R' : (None, 'UpArm_R', None, False),
    'ElbowPT_R' : ('Shoulder_R', 'UpArm_R', None, False),
    'Wrist_R' : (None, 'LoArm_R', 'Hand_R', False),
    'LegIK_R' : (None, 'Toe_R', 'LegFK_R', False),
    'KneePT_R' : ('Hips', 'UpLeg_R', None, False),
    'ToeRev_R' : ('LegIK_R', 'Foot_R', 'Toe_R', True),
    'FootRev_R' : ('ToeRev_R', 'LoLeg_R', 'Foot_R', True),
    'Ankle_R' : ('FootRev_R', 'LoLeg_R', None, False),
}

IkBoneList = [
    'Elbow_L', 'ElbowPT_L', 'Wrist_L',
    'LegIK_L', 'KneePT_L', # 'ToeRev_L', 'FootRev_L', 'Ankle_L',

    'Elbow_R', 'ElbowPT_R', 'Wrist_R',
    'LegIK_R', 'KneePT_R', # 'ToeRev_R', 'FootRev_R', 'Ankle_R',
]

GlobalBoneList = [
    'Root', 
]


