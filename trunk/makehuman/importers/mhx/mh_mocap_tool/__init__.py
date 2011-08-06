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
Tool for loading bvh files onto the MHX rig in Blender 2.5x
Version 0.8

Place the script in the .blender/scripts/addons dir
Activate the script in the "Add-Ons" tab (user preferences).
Access from UI panel (N-key) when MHX rig is active.

Alternatively, run the script in the script editor (Alt-P), and access from UI panel.
"""

bl_info = {
    "name": "MHX Mocap",
    "author": "Thomas Larsson",
    "version": "0.8",
    "blender": (2, 5, 8),
    "api": 35774,
    "location": "View3D > Properties > MHX Mocap",
    "description": "Mocap tool for MHX rig",
    "warning": "",
    'wiki_url': 'http://sites.google.com/site/makehumandocs/blender-export-and-mhx/mocap-tool',
    "category": "Animation"}

"""
Properties:
Scale:    
    for BVH import. Choose scale so that the vertical distance between hands and feet
    are the same for MHX and BVH rigs.
    Good values are: CMU: 0.6, OSU: 0.1
Start frame:    
    for BVH import
Rot90:    
    for BVH import. Rotate armature 90 degrees, so Z points up.
Simplify FCurves:    
    Include FCurve simplifcation.
Max loc error:    
    Max error allowed for simplification of location FCurves
Max rot error:    
    Max error allowed for simplification of rotation FCurves

Buttons:
Load BVH file (.bvh): 
    Load bvh file with Z up
Silence constraints:
    Turn off constraints that may conflict with mocap data.
Retarget selected to MHX: 
    Retarget actions of selected BVH rigs to the active MHX rig.
Simplify FCurves:
    Simplifiy FCurves of active action, allowing max errors specified above.
Load, retarget, simplify:
    Load bvh file, retarget the action to the active MHX rig, and simplify FCurves.
Batch run:
    Load all bvh files in the given directory, whose name start with the
    given prefix, and create actions (with simplified FCurves) for the active MHX rig.
"""

# To support reload properly, try to access a package var, if it's there, reload everything
if "bpy" in locals():
    print("Reloading Mocap tool")
    import imp
    imp.reload(utils)
    imp.reload(globvar)
    imp.reload(props)
    imp.reload(load)
    imp.reload(old_retarget)
    imp.reload(new_retarget)
    imp.reload(source)
    imp.reload(target)
    imp.reload(toggle)
    imp.reload(simplify)
    imp.reload(loop)
    imp.reload(plant)
    imp.reload(accad)
    imp.reload(action)
    imp.reload(sigproc)
    imp.reload(daz)
    imp.reload(eyes)
    imp.reload(hdm)
    imp.reload(max)
    imp.reload(mb)
    imp.reload(mega)
    imp.reload(rig_mhx)
    imp.reload(rig_rorkimaru)
    imp.reload(rig_game)
else:
    print("Loading Mocap tool")
    import bpy, os
    from bpy_extras.io_utils import ImportHelper
    from bpy.props import *

    from . import utils
    from . import globvar
    from . import props
    from . import load
    from . import old_retarget
    from . import new_retarget
    from . import source
    from . import target
    from . import toggle
    from . import simplify
    from . import loop
    from . import plant
    from . import action
    from . import sigproc
    from . import accad, daz, eyes, hdm, max, mb, mega
    from . import rig_mhx, rig_rorkimaru, rig_game


#
#    Debugging
#
"""
def debugOpen():
    global theDbgFp
    theDbgFp = open("/home/thomas/myblends/debug.txt", "w")

def debugClose():
    global theDbgFp
    theDbgFp.close()

def debugPrint(string):
    global theDbgFp
    theDbgFp.write("%s\n" % string)

def debugPrintVec(vec):
    global theDbgFp
    theDbgFp.write("(%.3f %.3f %.3f)\n" % (vec[0], vec[1], vec[2]))

def debugPrintVecVec(vec1, vec2):
    global theDbgFp
    theDbgFp.write("(%.3f %.3f %.3f) (%.3f %.3f %.3f)\n" %
        (vec1[0], vec1[1], vec1[2], vec2[0], vec2[1], vec2[2]))
"""

#
#    init 
#

props.initInterface(bpy.context)

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()


