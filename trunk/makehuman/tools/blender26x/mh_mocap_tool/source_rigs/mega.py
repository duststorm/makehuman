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

# Mega bone : ( MHX bone, twist)

Armature = {
    'hip' : ('Root', 0), 
    'abdomen' : ('Spine1', 0),
    'chest' : ('Spine3', 0),
    'neck' : ('Neck', 0),
    'head' : ('Head', 0), 
    'left eye' : (None, 0),
    'right eye' : (None, 0),

    'left collar' : ('Clavicle_L', 0),
    'left shoulder' : ('UpArm_L', 0), 
    'left forearm' : ('LoArm_L', 0),
    'left hand' : ('Hand_L', 0),
    'left thumb 1' : (None, 0), 
    'left thumb 2' : (None, 0), 
    'left thumb 3' : (None, 0), 
    'left index 1' : (None, 0), 
    'left index 2' : (None, 0), 
    'left index 3' : (None, 0), 
    'left mid 1' : (None, 0), 
    'left mid 2' : (None, 0), 
    'left mid 3' : (None, 0), 
    'left ring 1' : (None, 0), 
    'left ring 2' : (None, 0), 
    'left ring 3' : (None, 0), 
    'left pinky 1' : (None, 0), 
    'left pinky 2' : (None, 0), 
    'left pinky 3' : (None, 0), 

    'right collar' : ('Clavicle_R', 0),
    'right shoulder' : ('UpArm_R', 0), 
    'right forearm' : ('LoArm_R', 0),
    'right hand' : ('Hand_R', 0),
    'right thumb 1' : (None, 0), 
    'right thumb 2' : (None, 0), 
    'right thumb 3' : (None, 0), 
    'right index 1' : (None, 0), 
    'right index 2' : (None, 0), 
    'right index 3' : (None, 0), 
    'right mid 1' : (None, 0), 
    'right mid 2' : (None, 0), 
    'right mid 3' : (None, 0), 
    'right ring 1' : (None, 0), 
    'right ring 2' : (None, 0), 
    'right ring 3' : (None, 0), 
    'right pinky 1' : (None, 0), 
    'right pinky 2' : (None, 0), 
    'right pinky 3' : (None, 0), 

    'left thigh' : ('UpLeg_L', 0),
    'left shin' : ('LoLeg_L', 0), 
    'left foot' : ('Foot_L', 0), 
    'left toe' : ('Toe_L', 0),

    'right thigh' : ('UpLeg_R', 0),
    'right shin' : ('LoLeg_R', 0), 
    'right foot' : ('Foot_R', 0), 
    'right toe' : ('Toe_R', 0),
}
