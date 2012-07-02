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

# Eyes Japan bone : ( MHX bone, twist)

Armature = {
    'hips' : ('Root', 0),
    'lefthip' : ('UpLeg_L', 0),
    'leftknee' : ('LoLeg_L', 0),
    'leftankle' : ('Foot_L', 0),
    'righthip' : ('UpLeg_R', 0),
    'rightknee' : ('LoLeg_R', 0),
    'rightankle' : ('Foot_R', 0),
    'chest' : ('Spine1', 0),
    'chest2' : ('Spine2', 0),
    'cs_bvh' : ('Spine3', 0),
    'leftcollar' : ('Clavicle_L', 0),
    'leftshoulder' : ('UpArm_L', 90),
    'leftelbow' : ('LoArm_L', 90),
    'leftwrist' : ('Hand_L', 90),
    'rightcollar' : ('Clavicle_R', 0),
    'rightshoulder' : ('UpArm_R', -90),
    'rightelbow' : ('LoArm_R', -90),
    'rightwrist' : ('Hand_R', -90),
    'neck' : ('Neck', 0),
    'head' : ('Head', 0),
}


