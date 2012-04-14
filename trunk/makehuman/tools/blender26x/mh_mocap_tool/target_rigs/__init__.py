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

"""
Abstract
Target rigs 
"""

from .. import globvar as the
from . import rig_mhx
from . import rig_simple
from . import rig_game
from . import rig_second_life
from . import rig_sintel_light


TargetInfo = {
    "MHX" : (rig_mhx.Bones, rig_mhx.Renames, rig_mhx.IkBones),
    "Simple": (rig_simple.Bones, rig_simple.Renames, rig_simple.IkBones),
    "Game": (rig_game.Bones, rig_game.Renames, rig_game.IkBones),
    "Second Life": (rig_second_life.Bones, rig_second_life.Renames, rig_second_life.IkBones),
    "Sintel Light": (rig_sintel_light.Bones, rig_sintel_light.Renames, rig_sintel_light.IkBones),
}
