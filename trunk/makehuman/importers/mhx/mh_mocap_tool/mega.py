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

#
#    MegaArmature
#

MegaArmature = {
    'hip' : 'Root', 
    'abdomen' : 'Spine1',
    'chest' : 'Spine3',
    'neck' : 'Neck',
    'head' : 'Head', 
    'left eye' : None,
    'right eye' : None,

    'left collar' : 'Shoulder_L',
    'left shoulder' : 'UpArm_L', 
    'left forearm' : 'LoArm_L',
    'left hand' : 'Hand_L',
    'left thumb 1' : None, 
    'left thumb 2' : None, 
    'left thumb 3' : None, 
    'left index 1' : None, 
    'left index 2' : None, 
    'left index 3' : None, 
    'left mid 1' : None, 
    'left mid 2' : None, 
    'left mid 3' : None, 
    'left ring 1' : None, 
    'left ring 2' : None, 
    'left ring 3' : None, 
    'left pinky 1' : None, 
    'left pinky 2' : None, 
    'left pinky 3' : None, 

    'right collar' : 'Shoulder_R',
    'right shoulder' : 'UpArm_R', 
    'right forearm' : 'LoArm_R',
    'right hand' : 'Hand_R',
    'right thumb 1' : None, 
    'right thumb 2' : None, 
    'right thumb 3' : None, 
    'right index 1' : None, 
    'right index 2' : None, 
    'right index 3' : None, 
    'right mid 1' : None, 
    'right mid 2' : None, 
    'right mid 3' : None, 
    'right ring 1' : None, 
    'right ring 2' : None, 
    'right ring 3' : None, 
    'right pinky 1' : None, 
    'right pinky 2' : None, 
    'right pinky 3' : None, 

    'left thigh' : 'UpLeg_L',
    'left shin' : 'LoLeg_L', 
    'left foot' : 'Foot_L', 
    'left toe' : 'Toe_L',

    'right thigh' : 'UpLeg_R',
    'right shin' : 'LoLeg_R', 
    'right foot' : 'Foot_R', 
    'right toe' : 'Toe_R',
}

MegaFixes = {}

