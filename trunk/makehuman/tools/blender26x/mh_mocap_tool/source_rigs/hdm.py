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

HDMArmature = {
    'hip' : 'Root',
    'lhipjoint' : None,
    'lfemur' : 'UpLeg_L',
    'ltibia' : 'LoLeg_L',
    'lfoot' : 'Foot_L',
    'ltoes' : 'Toe_L',
    'rhipjoint' : None,
    'rfemur' : 'UpLeg_R',
    'rtibia' : 'LoLeg_R',
    'rfoot' : 'Foot_R',
    'rtoes' : 'Toe_R',
    'lowerback' : 'Spine1',
    'upperback' : 'Spine2',
    'thorax' : 'Spine3',
    'lowerneck' : 'LowerNeck',
    'upperneck' : 'Neck',
    'head' : 'Head',
    'lclavicle' : 'Clavicle_L',
    'lhumerus' : 'UpArm_L',
    'lradius' : 'LoArm_L',
    'lwrist' : 'Hand0_L',
    'lhand' : 'Hand_L',
    'lfingers' : None,
    'lthumb' : 'Finger1_L',
    'rclavicle' : 'Clavicle_R',
    'rhumerus' : 'UpArm_R',
    'rradius' : 'LoArm_R',
    'rwrist' : 'Hand0_R',
    'rhand' : 'Hand_R',
    'rfingers' : None,
    'rthumb' : 'Finger1_R',
}

HDMRolls = {
    'UpLeg_L' : -20,
    'LoLeg_L' : -20,
    'Foot_L'  : -20,
    'Toe_L'   : -20,

    'UpLeg_R' : 20,
    'LoLeg_R' : 20,
    'Foot_R'  : 20,
    'Toe_R'   : 20,
}

