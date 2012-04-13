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

# HDM bone : ( MHX bone, twist)

Armature = {
    'hip' : ('Root', 0),
    'lhipjoint' : (None, 0),
    'lfemur' : ('UpLeg_L', -20),
    'ltibia' : ('LoLeg_L', -20),
    'lfoot' : ('Foot_L', -20),
    'ltoes' : ('Toe_L', -20),
    
    'rhipjoint' : (None, 0),
    'rfemur' : ('UpLeg_R', 20),
    'rtibia' : ('LoLeg_R', 20),
    'rfoot' : ('Foot_R', 20),
    'rtoes' : ('Toe_R', 20),
    
    'lowerback' : ('Spine1', 0),
    'upperback' : ('Spine2', 0),
    'thorax' : ('Spine3', 0),
    'lowerneck' : ('LowerNeck', 0),
    'upperneck' : ('Neck', 0),
    'head' : ('Head', 0),
    
    'lclavicle' : ('Clavicle_L', 0),
    'lhumerus' : ('UpArm_L', 0),
    'lradius' : ('LoArm_L', 0),
    'lwrist' : ('Hand0_L', 0),
    'lhand' : ('Hand_L', 0),
    'lfingers' : (None, 0),
    'lthumb' : ('Finger1_L', 0),
    
    'rclavicle' : ('Clavicle_R', 0),
    'rhumerus' : ('UpArm_R', 0),
    'rradius' : ('LoArm_R', 0),
    'rwrist' : ('Hand0_R', 0),
    'rhand' : ('Hand_R', 0),
    'rfingers' : (None, 0),
    'rthumb' : ('Finger1_R', 0),
}

