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

bl_info = {
    "name": "Warp Target",
    "author": "Thomas Larsson",
    "version": "0.1",
    "blender": (2, 6, 4),
    "location": "View3D > Properties > Warp Target",
    "description": "Warp MakeHuman Targets To New Characters",
    "warning": "",
    'wiki_url': "http://www.makehuman.org/node/223",
    "category": "MakeHuman"}

if "bpy" in locals():
    print("Reloading warptarget")
    import imp    
    imp.reload(mh_utils)
    imp.reload(utils)
    imp.reload(settings)
    imp.reload(proxy)
    imp.reload(warp)
    imp.reload(import_obj)
    imp.reload(character)    
else:
    print("Loading warptarget")
    import bpy
    import os
    from bpy.props import *
    from bpy_extras.io_utils import ImportHelper, ExportHelper

    import mh_utils
    from mh_utils import globvars as the
    from mh_utils import utils
    from mh_utils import settings
    from mh_utils import proxy
    from mh_utils import warp
    from mh_utils import import_obj
    from mh_utils import character
        
#----------------------------------------------------------
#   class WarpTargetPanel(bpy.types.Panel):
#----------------------------------------------------------

class WarpTargetPanel(bpy.types.Panel):
    bl_label = "Warp Target"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene        
        if not utils.drawConfirm(layout, scn):
            return
        settings.drawDirectories(layout, scn)

        layout.label("Source Character")
        the.SourceCharacter.draw(layout, scn)

        layout.label("Source Morph")
        layout.operator("mh.set_source_morph")
        layout.prop(scn, "MhSourceMorphDir")
        layout.prop(scn, "MhSourceMorphFile")

        layout.separator()
        layout.label("Target Character")
        character.drawItems(layout, scn)
        layout.operator("mh.update_target_character")
        the.TargetCharacter.draw(layout, scn)
        
        layout.label("Target Morph")
        layout.prop(scn, "MhTargetMorphDir")
        layout.prop(scn, "MhTargetMorphFile")

        layout.separator()
        layout.operator("mh.warp_morph")

#----------------------------------------------------------
#   Settings buttons
#----------------------------------------------------------

class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
    bl_idname = "mh.factory_settings"
    bl_label = "Restore Factory Settings"

    def execute(self, context):
        settings.restoreFactorySettings(context)
        return{'FINISHED'}    


class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
    bl_idname = "mh.save_settings"
    bl_label = "Save Settings"

    def execute(self, context):
        settings.saveDefaultSettings(context)
        return{'FINISHED'}    


class OBJECT_OT_ReadSettingsButton(bpy.types.Operator):
    bl_idname = "mh.read_settings"
    bl_label = "Read Settings"

    def execute(self, context):
        settings.readDefaultSettings(context)
        return{'FINISHED'}    

#----------------------------------------------------------
#   Register
#----------------------------------------------------------

def register():
    character.init()
    bpy.utils.register_module(__name__)
  
def unregister():
    bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
    register()
