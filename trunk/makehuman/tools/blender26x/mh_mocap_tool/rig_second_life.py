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

Bones = [
    ('mPelvis',        'Root'),
    ('mTorso',      'Spine1'),
    ('mChest',      'Spine2'),
    ('mNeck',        'Neck'),
    ('mHead',        'Head'),

    ('mCollarLeft',  'Clavicle_L'),
    ('mShoulderLeft',     'UpArm_L'),
    ('mElbowLeft',     'LoArm_L'),
    ('mWristLeft',      'Hand_L'),

    ('mCollarRight',  'Clavicle_R'),
    ('mShoulderRight',     'UpArm_R'),
    ('mElbowRight',     'LoArm_R'),
    ('mWristRight',      'Hand_R'),

    ('mHipLeft',     'UpLeg_L'),
    ('mKneeLeft',     'LoLeg_L'),
    ('mAnkleLeft',      'Foot_L'),
    ('mFootLeft',       'Toe_L'),

    ('mHipRight',     'UpLeg_R'),
    ('mKneeRight',     'LoLeg_R'),
    ('mAnkleRight',      'Foot_R'),
    ('mFootRight',       'Toe_R'),
]

Names = {}
IkBones = []


