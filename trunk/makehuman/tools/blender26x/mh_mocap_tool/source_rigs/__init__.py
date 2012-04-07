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
Source rigs 
"""

if "bpy" in locals():
    print("Reloading source rigs")
    import imp
    imp.reload(accad)
    imp.reload(daz)
    imp.reload(eyes)
    imp.reload(hdm)
    imp.reload(max)
    imp.reload(mb)
    imp.reload(mega)    
else:
    from .. import globvar as the
    from . import accad
    from . import daz
    from . import eyes
    from . import hdm
    from . import max
    from . import mb
    from . import mega

 
the.armatures = {
    'MB' : mb.MBArmature, 
    'Accad' : accad.AccadArmature,
    'Mega' : mega.MegaArmature,
    'HDM' : hdm.HDMArmature,
    '3dsMax' : max.MaxArmature,
    'Eyes' : eyes.EyesArmature,
    'Daz' : daz.DazArmature,
}

the.armatureList = [ 'Accad', 'MB', 'Mega', 'HDM', 'Eyes', 'Daz', '3dsMax' ]

the.fixesList = {
    'MB'  : mb.MBFixes,
    'Accad' : accad.AccadFixes,
    'Mega' : mega.MegaFixes,
    'HDM' : hdm.HDMFixes,
    '3dsMax': max.MaxFixes,
    'Eyes': eyes.EyesFixes,
    'Daz' : daz.DazFixes,
}

 