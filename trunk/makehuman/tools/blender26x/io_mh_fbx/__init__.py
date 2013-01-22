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

bl_info = {
    "name": "MH FBX I/O",
    "author": "Thomas Larsson",
    "version": "0.1",
    "blender": (2, 6, 5),
    "api": 40000,
    "location": "View3D > Properties > FBX Test",
    "description": "Yet another FBX exporter/importer",
    "warning": "",
    'wiki_url': "",
    "category": "MakeHuman"}

if "bpy" in locals():
    print("Reloading FBX importer")
    import imp
    imp.reload(fbx)
    imp.reload(fbx_basic)
    imp.reload(fbx_props)
    imp.reload(fbx_model)

    imp.reload(fbx_image)
    imp.reload(fbx_texture)
    imp.reload(fbx_material)
    imp.reload(fbx_geometry)
    imp.reload(fbx_deformer)
    imp.reload(fbx_constraint)    
    imp.reload(fbx_anim)

    imp.reload(fbx_mesh)
    imp.reload(fbx_nurb)
    imp.reload(fbx_armature)
    imp.reload(fbx_lamp)
    imp.reload(fbx_camera)

    imp.reload(fbx_group)
    imp.reload(fbx_object)
    imp.reload(fbx_null)
    imp.reload(fbx_scene)
    imp.reload(fbx_data)

    imp.reload(fbx_token)
    imp.reload(fbx_export)
    imp.reload(fbx_import)
    imp.reload(fbx_build)
else:
    print("Loading FBX importer")
    import bpy
    from bpy_extras.io_utils import *
    from bpy.props import *
    import os

    from . import fbx
    from . import fbx_basic
    from . import fbx_props
    from . import fbx_model

    from . import fbx_image
    from . import fbx_texture
    from . import fbx_material
    from . import fbx_geometry
    from . import fbx_deformer
    from . import fbx_constraint    
    from . import fbx_anim

    from . import fbx_mesh
    from . import fbx_nurb
    from . import fbx_armature
    from . import fbx_lamp
    from . import fbx_camera

    from . import fbx_group
    from . import fbx_object
    from . import fbx_null
    from . import fbx_scene
    from . import fbx_data

    from . import fbx_token
    from . import fbx_export
    from . import fbx_import
    from . import fbx_build
    

class ImportFBX(bpy.types.Operator, ImportHelper):
    """Import a Filmbox FBX File"""
    bl_idname = "import_scene.fbx_mh"
    bl_label = "Import FBX via MH"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".fbx"
    filter_glob = StringProperty(default="*.fbx", options={'HIDDEN'})

    createNewScenes = BoolProperty(name="Create New Scenes", default=False)
    changeCsys = BoolProperty(name="Change Coordinate System", default=False)        
    
    def execute(self, context):
        fbx.settings.createNewScenes = self.createNewScenes
        fbx.settings.changeCsys = self.changeCsys
        fbx_import.importFbxFile(context, self.filepath)
        return {'FINISHED'}

 
class ExportFBX(bpy.types.Operator, ExportHelper):
    """Export a Filmbox FBX File"""
    bl_idname = "export_scene.fbx_mh"
    bl_label = "Export FBX via MH"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".fbx"
    filter_glob = StringProperty(default="*.fbx", options={'HIDDEN'} )
    
    changeCsys = BoolProperty(name="Change Coordinate System", default=False)        
    includePropertyTemplates = BoolProperty(name="Include Property Templates", default=True)
    makeSceneNode = BoolProperty(name="Make Scene Node", default=False)
    selectedOnly = BoolProperty(name="Selected Objects Only", default=True)

    def execute(self, context):
        fbx.settings.changeCsys = self.changeCsys
        fbx.settings.includePropertyTemplates = self.includePropertyTemplates
        fbx.settings.makeSceneNode = self.makeSceneNode
        fbx.settings.selectedOnly = self.selectedOnly
        fbx_export.exportFbxFile(context, self.filepath)
        return {'FINISHED'}
 
  
  
class FbxTestPanel(bpy.types.Panel):
    bl_label = "FBX Test"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):    
        self.layout.operator("fbx.test_export")
        self.layout.operator("fbx.test_import").filepath="/home/myblends/fbx-stuff/test.fbx"
        self.layout.operator("fbx.test_import", text="Test Import foo").filepath="/Users/Thomas/Documents/makehuman/exports/foo/foo.fbx"
        self.layout.operator("fbx.test_build")

#
#    Init and register
#

def menu_func_import(self, context):
    self.layout.operator(ImportFBX.bl_idname, text="Filmbox via MH (.fbx)")


def menu_func_export(self, context):
    self.layout.operator(ExportFBX.bl_idname, text="Filmbox via MH (.fbx)")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.INFO_MT_file_import.append(menu_func_import)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

