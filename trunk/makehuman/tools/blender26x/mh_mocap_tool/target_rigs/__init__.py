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

if "bpy" in locals():
    print("Reloading target rigs")
    import imp
    imp.reload(rig_mhx)
    imp.reload(rig_simple)
    imp.reload(rig_game)
    imp.reload(rig_second_life)
else:
    from .. import globvar as the
    from . import rig_mhx
    from . import rig_simple
    from . import rig_game
    from . import rig_second_life


the.T_MHX = 1
the.T_Game = 2
the.T_Simple = 3
the.T_SecondLife = 4
the.T_Custom = 5

