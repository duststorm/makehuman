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
#    AccadArmature
#    www.accad.Accad.edu/research/mocap/mocap_data.htm
#

AccadArmature = {
    'hips' : 'Root',
    'tospine' : 'Spine1',
    'spine' : 'Spine2',
    'spine1' : 'Spine3', 
    'neck' : 'Neck', 
    'head' : 'Head', 

    'leftshoulder' : 'Shoulder_L',
    'leftarm' : 'UpArm_L', 
    'leftforearm' : 'LoArm_L',
    'lefthand' : 'Hand_L', 

    'rightshoulder' : 'Shoulder_R',
    'rightarm' : 'UpArm_R', 
    'rightforearm' : 'LoArm_R',
    'righthand' : 'Hand_R',

    'leftupleg' : 'UpLeg_L', 
    'leftleg' : 'LoLeg_L', 
    'leftfoot' : 'Foot_L', 
    'lefttoebase' : 'Toe_L',

    'rightupleg' : 'UpLeg_R',
    'rightleg' : 'LoLeg_R', 
    'rightfoot' : 'Foot_R', 
    'righttoebase' : 'Toe_R',
}

AccadFixes = {}

