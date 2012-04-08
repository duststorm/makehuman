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

from mathutils import *
from math import pi

EyesArmature = {
    'hips' : 'Root',
    'lefthip' : 'UpLeg_L',
    'leftknee' : 'LoLeg_L',
    'leftankle' : 'Foot_L',
    'righthip' : 'UpLeg_R',
    'rightknee' : 'LoLeg_R',
    'rightankle' : 'Foot_R',
    'chest' : 'Spine1',
    'chest2' : 'Spine2',
    'cs_bvh' : 'Spine3',
    'leftcollar' : 'Clavicle_L',
    'leftshoulder' : 'UpArm_L',
    'leftelbow' : 'LoArm_L',
    'leftwrist' : 'Hand_L',
    'rightcollar' : 'Clavicle_R',
    'rightshoulder' : 'UpArm_R',
    'rightelbow' : 'LoArm_R',
    'rightwrist' : 'Hand_R',
    'neck' : 'Neck',
    'head' : 'Head',
}


EyesRolls = {
    'UpArm_L' :  90,
    'LoArm_L' :  90,
    'Hand_L' :  90,
    'UpArm_R' :  -90,
    'LoArm_R' :  -90,
    'Hand_R' :  -90,
}

