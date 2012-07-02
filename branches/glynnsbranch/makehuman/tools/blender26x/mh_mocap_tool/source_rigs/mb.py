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

# MB bone : ( MHX bone, twist)

Armature = {
    'hips' : ('Root', 0), 
    'lowerback' : ('Spine1', 0),
    'spine' : ('Spine2', 0), 
    'spine1' : ('Spine3', 0),
    'neck' : ('Neck', 0),
    'neck1' : ('Head', 0), 
    'head' : (None, 0),

    'leftshoulder' : ('Clavicle_L', 0),
    'leftarm' : ('UpArm_L', 0), 
    'leftforearm' : ('LoArm_L', 0),
    'lefthand' : ('Hand_L', 0),
    'lefthandindex1' : (None, 0),
    'leftfingerbase' : (None, 0),
    'lfingers' : (None, 0),
    'lthumb' : (None, 0), 

    'rightshoulder' : ('Clavicle_R', 0), 
    'rightarm' : ('UpArm_R', 0), 
    'rightforearm' : ('LoArm_R', 0),
    'righthand' : ('Hand_R', 0),
    'righthandindex1' : (None, 0),
    'rightfingerbase' : (None, 0),
    'rfingers' : (None, 0),
    'rthumb' : (None, 0), 

    'lhipjoint' : (None, 0), 
    'leftupleg' : ('UpLeg_L', -20),
    'leftleg' : ('LoLeg_L', -20), 
    'leftfoot' : ('Foot_L', -20), 
    'lefttoebase' : ('Toe_L', -20),

    'rhipjoint' : (None, 0), 
    'rightupleg' : ('UpLeg_R', 20),
    'rightleg' : ('LoLeg_R', 20), 
    'rightfoot' : ('Foot_R', 20), 
    'righttoebase' : ('Toe_R', 20),
}

