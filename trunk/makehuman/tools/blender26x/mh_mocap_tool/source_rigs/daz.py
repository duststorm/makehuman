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

DazArmature = {
    'hip' : 'Root', 
    'abdomen' : 'Spine1',

    'chest' : 'Spine3',
    'neck' : 'Neck',
    'head' : 'Head', 
    'lefteye' : None,
    'righteye' : None,
    'figurehair' : None,

    'lcollar' : 'Clavicle_L',
    'lshldr' : 'UpArm_L', 
    'lforearm' : 'LoArm_L',
    'lhand' : 'Hand_L',
    'lthumb1' : None, 
    'lthumb2' : None, 
    'lthumb3' : None, 
    'lindex1' : None, 
    'lindex2' : None, 
    'lindex3' : None, 
    'lmid1' : None, 
    'lmid2' : None, 
    'lmid3' : None, 
    'lring1' : None, 
    'lring2' : None, 
    'lring3' : None, 
    'lpinky1' : None, 
    'lpinky2' : None, 
    'lpinky3' : None, 

    'rcollar' : 'Clavicle_R',
    'rshldr' : 'UpArm_R', 
    'rforearm' : 'LoArm_R',
    'rhand' : 'Hand_R',
    'rthumb1' : None, 
    'rthumb2' : None, 
    'rthumb3' : None, 
    'rindex1' : None, 
    'rindex2' : None, 
    'rindex3' : None, 
    'rmid1' : None, 
    'rmid2' : None, 
    'rmid3' : None, 
    'rring1' : None, 
    'rring2' : None, 
    'rring3' : None, 
    'rpinky1' : None, 
    'rpinky2' : None, 
    'rpinky3' : None, 

    'lbuttock' : None,
    'lthigh' : 'UpLeg_L',
    'lshin' : 'LoLeg_L', 
    'lfoot' : 'Foot_L', 
    'ltoe' : 'Toe_L',

    'rbuttock' : None,
    'rthigh' : 'UpLeg_R',
    'rshin' : 'LoLeg_R', 
    'rfoot' : 'Foot_R', 
    'rtoe' : 'Toe_R',
}

DazRolls = {}

