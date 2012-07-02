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
    ('root', 'Root'),
    ('spine.02', 'Spine1'),
    ('spine.03', 'Spine2'),
    ('spine.04', 'Spine3'),
    ('neck', 'Neck'),
    ('head', 'Head'),
    
    ('shoulder.L', 'Clavicle_L'),
    ('upper_arm.L', 'UpArm_L'),
    ('forearm.L', 'LoArm_L'),
    ('hand.L', 'Hand_L'),
    
    ('shoulder.R', 'Clavicle_R'),
    ('upper_arm.R', 'UpArm_R'),
    ('forearm.R', 'LoArm_R'),
    ('hand.R', 'Hand_R'),
        
    ('thigh.L', 'UpLeg_L'),
    ('shin.L', 'LoLeg_L'),
    ('foot.L', 'Foot_L'),
    ('toe.L', 'Toe_L'),
        
    ('thigh.R', 'UpLeg_R'),
    ('shin.R', 'LoLeg_R'),
    ('foot.R', 'Foot_R'),
    ('toe.R', 'Toe_R'),
]

IkBones = [ 
    ('hand_ik.L', 'hand.L'),
    ('elbow_target.L', 'forearm.L'),
    ('foot_ik.L', 'foot.L'),
    ('knee_target.L', 'shin.L'),
    
    ('hand_ik.R', 'hand.R'),
    ('elbow_target.R', 'forearm.R'),
    ('foot_ik.R', 'foot.R'),
    ('knee_target.R', 'shin.R'),
]

Renames = {
    'pelvis' :          'root',
    'spine.01':         'pelvis',
    'MCH-rot_spine.01': 'pelvis',
    'MCH-rot_spine.02': 'spine.01',
    'MCH-rot_spine.03': 'spine.02',
    'MCH-rot_spine.04': 'spine.03',
    'Hips' :            'pelvis',
    'Hip_L' :           'pelvis',
    'Hip_R' :           'pelvis',
}

