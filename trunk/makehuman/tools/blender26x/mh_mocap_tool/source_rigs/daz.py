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

# DAZ bone : ( MHX bone, twist)

Armature = {
    'hip' : ('Root', 0), 
    'abdomen' : ('Spine2', 0),

    'chest' : ('Spine3', 0),
    'neck' : ('Neck', 0),
    'head' : ('Head', 0), 
    'lefteye' : (None, 0),
    'righteye' : (None, 0),
    'figurehair' : (None, 0),

    'lcollar' : ('Clavicle_L', 0),
    'lshldr' : ('UpArm_L', 0), 
    'lforearm' : ('LoArm_L', 0),
    'lhand' : ('Hand_L', 0),
    'lthumb1' : (None, 0), 
    'lthumb2' : (None, 0), 
    'lthumb3' : (None, 0), 
    'lindex1' : (None, 0), 
    'lindex2' : (None, 0), 
    'lindex3' : (None, 0), 
    'lmid1' : (None, 0), 
    'lmid2' : (None, 0), 
    'lmid3' : (None, 0), 
    'lring1' : (None, 0), 
    'lring2' : (None, 0), 
    'lring3' : (None, 0), 
    'lpinky1' : (None, 0), 
    'lpinky2' : (None, 0), 
    'lpinky3' : (None, 0), 

    'rcollar' : ('Clavicle_R', 0),
    'rshldr' : ('UpArm_R', 0), 
    'rforearm' : ('LoArm_R', 0),
    'rhand' : ('Hand_R', 0),
    'rthumb1' : (None, 0), 
    'rthumb2' : (None, 0), 
    'rthumb3' : (None, 0), 
    'rindex1' : (None, 0), 
    'rindex2' : (None, 0), 
    'rindex3' : (None, 0), 
    'rmid1' : (None, 0), 
    'rmid2' : (None, 0), 
    'rmid3' : (None, 0), 
    'rring1' : (None, 0), 
    'rring2' : (None, 0), 
    'rring3' : (None, 0), 
    'rpinky1' : (None, 0), 
    'rpinky2' : (None, 0), 
    'rpinky3' : (None, 0), 

    'lbuttock' : (None, 0),
    'lthigh' : ('UpLeg_L', 0),
    'lshin' : ('LoLeg_L', 0), 
    'lfoot' : ('Foot_L', 0), 
    'ltoe' : ('Toe_L', 0),

    'rbuttock' : (None, 0),
    'rthigh' : ('UpLeg_R', 0),
    'rshin' : ('LoLeg_R', 0), 
    'rfoot' : ('Foot_R', 0), 
    'rtoe' : ('Toe_R', 0),
}
