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

# 3DSMax bone : ( MHX bone, twist)

Armature = {
    'hips' : ('Root', 0),

    'lhipjoint' : (None, 0),
    'lefthip' : ('UpLeg_L', -20),
    'leftknee' : ('LoLeg_L', -20),
    'leftankle' : ('Foot_L', -20),
    'lefttoe' : ('Toe_L', -20),

    'rhipjoint' : (None, 0),
    'righthip' : ('UpLeg_R', 20),
    'rightknee' : ('LoLeg_R', 20),
    'rightankle' : ('Foot_R', 20),
    'righttoe' : ('Toe_R', 20),

    'lowerback' : ('Spine1', 0),
    'chest' : ('Spine2', 0),
    'chest2' : ('Spine3', 0),
    'lowerneck' : ('LowerNeck', 0),
    'neck' : ('Neck', 0),
    'head' : ('Head', 0),

    'leftcollar' : ('Clavicle_L', 0),
    'leftshoulder' : ('UpArm_L', 90),
    'leftelbow' : ('LoArm_L', 90),
    'leftwrist' : ('Hand_L', 90),
    'lhand' : (None, 0),
    'lfingers' : (None, 0),
    'lthumb' : (None, 0),

    'rightcollar' : ('Clavicle_R', 0),
    'rightshoulder' : ('UpArm_R', -90),
    'rightelbow' : ('LoArm_R', -90),
    'rightwrist' : ('Hand_R', -90),
    'rhand' : (None, 0),
    'rfingers' : (None, 0),
    'rthumb' : (None, 0),
}
