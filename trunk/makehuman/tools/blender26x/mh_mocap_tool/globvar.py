# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under  terms of  GNU General Public License
#  as published by  Free Software Foundation; eir version 2
#  of  License, or (at your option) any later version.
#
#  This program is distributed in  hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even  implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See 
#  GNU General Public License for more details.
#
#  You should have received a copy of  GNU General Public License
#  along with this program; if not, write to  Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Project Name:        MakeHuman
# Product Home Page:   http://www.makehuman.org/
# Code Home Page:      http://code.google.com/p/makehuman/
# Authors:             Thomas Larsson
# Script copyright (C) MakeHuman Team 2001-2011
# Coding Standards:    See http://sites.google.com/site/makehumandocs/developers-guide

target = None
fkBoneList = []
ikBoneList = []
globalBoneList = []
ikParents = []
srcBone = None
trgBone = None
parents = []
targetRolls = []
targetMats = []
actions = []


F_Rev = 1
F_LR = 2


T_MHX = 1
T_Game = 2
T_Simple = 3
T_SecondLife = 4
T_Custom = 5

###################################################################################
#
#    Supported source armatures

from . import accad, mb, mega, hdm, eyes, max, daz

armatures = {
    'MB' : mb.MBArmature, 
    'Accad' : accad.AccadArmature,
    'Mega' : mega.MegaArmature,
    'HDM' : hdm.HDMArmature,
    '3dsMax' : max.MaxArmature,
    'Eyes' : eyes.EyesArmature,
    'Daz' : daz.DazArmature,
}

armatureList = [ 'Accad', 'MB', 'Mega', 'HDM', 'Eyes', 'Daz', '3dsMax' ]

fixesList = {
    'MB'  : mb.MBFixes,
    'Accad' : accad.AccadFixes,
    'Mega' : mega.MegaFixes,
    'HDM' : hdm.HDMFixes,
    '3dsMax': max.MaxFixes,
    'Eyes': eyes.EyesFixes,
    'Daz' : daz.DazFixes,
}

#
#    end supported source armatures

