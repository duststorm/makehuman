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
    "name": "Make Target",
    "author": "Manuel Bastioni, Thomas Larsson",
    "version": "0.3",
    "blender": (2, 6, 2),
    "location": "View3D > Properties > Make Target",
    "description": "Make MakeHuman Target",
    "warning": "",
    'wiki_url': "http://www.makehuman.org/node/223",
    "category": "MakeHuman"}

if "bpy" in locals():
    print("Reloading maketarget")
    import imp
    imp.reload(maketarget)
    imp.reload(mhm)
    #imp.reload(rig)
    imp.reload(export_mh_obj)
else:
    print("Loading maketarget")
    import bpy
    import os
    from bpy.props import *
    from bpy_extras.io_utils import ImportHelper, ExportHelper
    from . import maketarget
    from . import mhm
    #from . import rig
    from . import export_mh_obj
  
#----------------------------------------------------------
#   class MakeTargetPanel(bpy.types.Panel):
#----------------------------------------------------------

class MakeTargetPanel(bpy.types.Panel):
    bl_label = "Make Target"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        layout = self.layout
        ob = context.object
        scn = context.scene
        if not maketarget.isInited(scn):
            layout.operator("mh.init")
            return
        if maketarget.Confirm:
            layout.label(maketarget.ConfirmString)            
            if maketarget.ConfirmString2:
                layout.label(maketarget.ConfirmString2)            
            layout.operator(maketarget.Confirm, text="Yes") 
            layout.operator("mh.skip")
            return            
        layout.label("Directories")
        layout.operator("mh.factory_settings")
        layout.operator("mh.save_settings")
        layout.operator("mh.read_settings")
        layout.prop(scn, "MhProgramPath")
        layout.prop(scn, "MhUserPath")
        layout.label("Load materials from")
        layout.prop(scn, "MhLoadMaterial", expand=True)
        layout.separator()
        if maketarget.isBaseOrTarget(ob):
            layout.operator("mh.import_base_mhclo", text="Reimport Base Mhclo").delete = True
            layout.operator("mh.import_base_obj", text="Reimport Base Obj").delete = True
            layout.operator("mh.delete_clothes")
            layout.separator()
        else:
            layout.operator("mh.import_base_mhclo", text="Import Base Mhclo").delete = False
            layout.operator("mh.import_base_obj", text="Import Base Obj").delete = False
            layout.operator("mh.make_base_obj")
        if maketarget.isBase(ob):
            layout.operator("mh.new_target")
            layout.operator("mh.load_target")            
            layout.operator("mh.load_target_from_mesh")                        
        elif maketarget.isTarget(ob):
            if not ob.data.shape_keys:
                layout.label("Warning: Internal inconsistency")
                layout.operator("mh.fix_inconsistency")
                return
            layout.separator()
            layout.prop(ob, "show_only_shape_key")
            box = layout.box()
            n = 0
            for skey in ob.data.shape_keys.key_blocks:
                if n == 0:
                    n += 1
                    continue
                row = box.row()
                if n == ob.active_shape_key_index:
                    icon='LAMP'
                else:
                    icon='X'
                row.label("", icon=icon)
                row.prop(skey, "value", text=skey.name)
                n += 1
            layout.separator()
            layout.operator("mh.new_target", text="New Secondary Target")
            layout.operator("mh.load_target", text="Load Secondary From File")            
            layout.operator("mh.load_target_from_mesh", text="Load Secondary From Mesh")                        
            layout.operator("mh.fit_target")
            layout.operator("mh.symmetrize_target", text="Symm Left->Right").left2right = False
            layout.operator("mh.symmetrize_target", text="Symm Right->Left").left2right = True
            #layout.separator()
            #layout.prop(scn, '["Relax"]')
            #layout.operator("mh.relax_target")
            layout.separator()
            layout.operator("mh.discard_target")
            layout.operator("mh.discard_all_targets")
            layout.separator()
            layout.operator("mh.apply_targets")
            layout.separator()
            layout.prop(ob, '["SelectedOnly"]')
            if ob["FilePath"]:
                layout.operator("mh.save_target")           
            layout.operator("mh.saveas_target")           

#----------------------------------------------------------
#   class MhmPanel(bpy.types.Panel):
#----------------------------------------------------------

class MhmPanel(bpy.types.Panel):
    bl_label = "MHM"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        return False and maketarget.isInited(context.scene)

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scn = context.scene
        if maketarget.Confirm:
            layout.label(maketarget.ConfirmString)            
            if maketarget.ConfirmString2:
                layout.label(maketarget.ConfirmString2)            
            layout.operator(maketarget.Confirm, text="Yes") 
            layout.operator("mh.skip")
            return            
        if maketarget.isBaseOrTarget(ob):
            for (label, names) in mhm.MhmDisplay:
                layout.label(label)
                for name in names:
                    prop = mhm.MhmNameProps[name]
                    split = layout.split(0.8)
                    split.prop(ob.data, prop)
                    split.operator("mh.update_all_sliders")
            layout.separator()                
            layout.operator("mh.update_all_sliders")        
            layout.operator("mh.reset_all_sliders")        
            layout.operator("mh.load_mhm_file")                        
            layout.operator("mh.discard_all_targets")


#----------------------------------------------------------
#   class MakeTargetBatchPanel(bpy.types.Panel):
#----------------------------------------------------------

class MakeTargetBatchPanel(bpy.types.Panel):
    bl_label = "Batch make targets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        return context.scene.MhUnlock and maketarget.isInited(context.scene)
        
    def draw(self, context):
        if maketarget.isBase(context.object):
            layout = self.layout
            scn = context.scene
            #for fname in maketarget.TargetSubPaths:
            #    layout.prop(scn, "Mh%s" % fname)
            layout.prop(scn, "MhTargetPath")
            layout.operator("mh.batch_fix")
            layout.operator("mh.batch_render", text="Batch Render").opengl = False
            layout.operator("mh.batch_render", text="Batch OpenGL Render").opengl = True
  
#----------------------------------------------------------
#   class ExportObj(bpy.types.Operator, ExportHelper):
#----------------------------------------------------------

class ExportObj(bpy.types.Operator, ExportHelper):
    '''Export to OBJ file format (.obj)''' 
    bl_idname = "mh.export_obj"
    bl_description = 'Export to OBJ file format (.obj)'
    bl_label = "Export MH OBJ"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = ".obj"
    filter_glob = StringProperty(default="*.obj", options={'HIDDEN'})
    filepath = StringProperty(name="File Path", description="File path for the exported OBJ file", maxlen= 1024, default= "")
    
    groupsAsMaterials = BoolProperty(name="Groups as materials", default=False)
 
    def execute(self, context):        
        export_mh_obj.exportObjFile(self.properties.filepath, self.groupsAsMaterials, context)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
 
#----------------------------------------------------------
#   Register
#----------------------------------------------------------

def menu_func(self, context):
    self.layout.operator(ExportObj.bl_idname, text="MakeHuman OBJ (.obj)...")
 
def register():
    try:
        maketarget.initScene(bpy.context.scene)
    except:
        pass
    mhm.init()        
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func)
  
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func)
 
if __name__ == "__main__":
    register()
