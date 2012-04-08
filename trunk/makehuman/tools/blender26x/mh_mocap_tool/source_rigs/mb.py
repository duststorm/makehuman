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
#    MBArmature
#

MBArmature = {
    'hips' : 'Root', 
    'lowerback' : 'Spine1',
    'spine' : 'Spine2', 
    'spine1' : 'Spine3',
    'neck' : 'Neck',
    'neck1' : 'Head', 
    'head' : None,

    'leftshoulder' : 'Clavicle_L',
    'leftarm' : 'UpArm_L', 
    'leftforearm' : 'LoArm_L',
    'lefthand' : 'Hand_L',
    'lefthandindex1' : None,
    'leftfingerbase' : None,
    'lfingers' : None,
    'lthumb' : None, 

    'rightshoulder' : 'Clavicle_R', 
    'rightarm' : 'UpArm_R', 
    'rightforearm' : 'LoArm_R',
    'righthand' : 'Hand_R',
    'righthandindex1' : None,
    'rightfingerbase' : None,
    'rfingers' : None,
    'rthumb' : None, 

    'lhipjoint' : None, 
    'leftupleg' : 'UpLeg_L',
    'leftleg' : 'LoLeg_L', 
    'leftfoot' : 'Foot_L', 
    'lefttoebase' : 'Toe_L',

    'rhipjoint' : None, 
    'rightupleg' : 'UpLeg_R',
    'rightleg' : 'LoLeg_R', 
    'rightfoot' : 'Foot_R', 
    'righttoebase' : 'Toe_R',
}


MBRolls = {
    'UpLeg_L' : -20,
    'LoLeg_L' : -20,
    'Foot_L'  : -20,
    'Toe_L'   : -20,

    'UpLeg_R' : 20,
    'LoLeg_R' : 20,
    'Foot_R'  : 20,
    'Toe_R'   : 20,
}

