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

    'lhipjoint' : 'Hip_L', 
    'leftupleg' : 'UpLeg_L',
    'leftleg' : 'LoLeg_L', 
    'leftfoot' : 'Foot_L', 
    'lefttoebase' : 'Toe_L',

    'rhipjoint' : 'Hip_R', 
    'rightupleg' : 'UpLeg_R',
    'rightleg' : 'LoLeg_R', 
    'rightfoot' : 'Foot_R', 
    'righttoebase' : 'Toe_R',
}


MBFixes = {
    'UpLeg_L' : ( Matrix.Rotation(0.4, 3, 'Y') * Matrix.Rotation(-0.45, 3, 'Z'), 0),
    'UpLeg_R' : ( Matrix.Rotation(-0.4, 3, 'Y') * Matrix.Rotation(0.45, 3, 'Z'), 0),
    'LoLeg_L' : ( Matrix.Rotation(-0.2, 3, 'Y'), 0),
    'LoLeg_R' : ( Matrix.Rotation(0.2, 3, 'Y'), 0),
    'Foot_L'  : ( Matrix.Rotation(-0.3, 3, 'Z'), 0),
    'Foot_R'  : ( Matrix.Rotation(0.3, 3, 'Z'), 0),
    #'UpArm_L' : ( Matrix.Rotation(0.1, 3, 'X'), 0),
    #'UpArm_R' : ( Matrix.Rotation(0.1, 3, 'X'), 0),
}

