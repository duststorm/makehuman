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
#    www.accad.Accad.edu/research/mocap/mocap_data.htm
#
# ACCAD bone : ( MHX bone, twist)

Armature = {
    'hips' : ('Root', 0),
    'tospine' : ('Spine1', 0),
    'spine' : ('Spine2', 0),
    'spine1' : ('Spine3', 0), 
    'neck' : ('Neck', 0), 
    'head' : ('Head', 0), 

    'leftshoulder' : ('Clavicle_L', 0),
    'leftarm' : ('UpArm_L', 0), 
    'leftforearm' : ('LoArm_L', 0),
    'lefthand' : ('Hand_L', 0), 

    'rightshoulder' : ('Clavicle_R', 0),
    'rightarm' : ('UpArm_R', 0), 
    'rightforearm' : ('LoArm_R', 0),
    'righthand' : ('Hand_R', 0),

    'leftupleg' : ('UpLeg_L', 0), 
    'leftleg' : ('LoLeg_L', 0), 
    'leftfoot' : ('Foot_L', 0), 
    'lefttoebase' : ('Toe_L', 0),

    'rightupleg' : ('UpLeg_R', 0),
    'rightleg' : ('LoLeg_R', 0), 
    'rightfoot' : ('Foot_R', 0), 
    'righttoebase' : ('Toe_R', 0),
}
