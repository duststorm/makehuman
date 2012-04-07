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
    ('Root',        'Root'),
    ('Spine1',      'Spine1'),
    ('Spine2',      'Spine3'),
    ('Neck',        'Neck'),
    ('Head',        'Head'),

    ('Clavicle_L',  'Clavicle_L'),
    ('UpArm_L',     'UpArm_L'),
    ('LoArm_L',     'LoArm_L'),
    ('Hand_L',      'Hand_L'),

    ('Clavicle_R',  'Clavicle_R'),
    ('UpArm_R',     'UpArm_R'),
    ('LoArm_R',     'LoArm_R'),
    ('Hand_R',      'Hand_R'),

    ('UpLeg_L',     'UpLeg_L'),
    ('LoLeg_L',     'LoLeg_L'),
    ('Foot_L',      'Foot_L'),
    ('Toe_L',       'Toe_L'),

    ('UpLeg_R',     'UpLeg_R'),
    ('LoLeg_R',     'LoLeg_R'),
    ('Foot_R',      'Foot_R'),
    ('Toe_R',       'Toe_R'),
]

IkBones = [ 
    ('Wrist_L', 'Hand_L'),
    ('Wrist_R', 'Hand_R'),
    ('Ankle_L', 'Foot_L'),
    ('Ankle_R', 'Foot_R')
]

Names = {
    'MasterFloor' :     None,
    'MasterFloorInv' :  None,
    'RootInv' :        'Root',
    'HipsInv' :        'Root',
    'Hips' :           'Root',
    'Spine2Inv' :      'Spine2',
    'Spine3' :         'Spine2',
}

