""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
Utility for making rig to MH characters.

For more info see: http://sites.google.com/site/makehumandocs/blender-export-and-mhx/making-rig

"""
bl_info = {
    "name": "Make Rig",
    "author": "Thomas Larsson",
    "version": "0.1",
    "blender": (2, 6, 1),
    "api": 40000,
    "location": "View3D > Properties > Make MH rig",
    "description": "Make rigs for MakeHuman characters",
    "warning": "",
    'wiki_url': '',
    "category": "MakeHuman"}


if "bpy" in locals():
    print("Reloading makerig")
    import imp
    imp.reload(main)
else:
    print("Loading makerig")
    import bpy
    import os
    from bpy.props import *
    from . import main
  
#
#    class MakeRigPanel(bpy.types.Panel):
#

Confirm = None
ConfirmString = "?"

def isInited(scn):
    global Confirm
    try:
        scn.MRDirectory
        Confirm
        return True
    except:
        return False
    


class MakeRigPanel(bpy.types.Panel):
    bl_label = "Make rig"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return (context.object)

    def draw(self, context):
        global Confirm, ConfirmString
        layout = self.layout
        scn = context.scene
        if not isInited(scn):
            layout.operator("mhrig.init_interface", text="Initialize")
            return
        if Confirm:
            layout.label(ConfirmString)
            layout.operator(Confirm, text="yes").answer="yes"
            layout.operator(Confirm, text="no").answer="no"
            return
        layout.label("Initialization")
        layout.operator("mhrig.init_interface", text="ReInitialize")
        layout.operator("mhrig.factory_settings")
        layout.operator("mhrig.save_settings")

        layout.label("Make rig")      
        layout.prop(scn, "MRDirectory")
        layout.prop(scn, "MRMakeHumanDir")
        layout.operator("mhrig.auto_weight_body")
        layout.operator("mhrig.auto_weight_helpers")
        layout.operator("mhrig.export_rig_file")

        layout.separator()
        layout.label("Licensing")
        layout.prop(scn, "MRAuthor")
        layout.prop(scn, "MRLicense")
        layout.prop(scn, "MRHomePage")
    
        return

#
#    Buttons
#

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
    bl_idname = "mhrig.init_interface"
    bl_label = "Init"

    def execute(self, context):
        main.initInterface()
        main.readDefaultSettings(context)
        print("Interface initialized")
        return{'FINISHED'}    

class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
    bl_idname = "mhrig.factory_settings"
    bl_label = "Restore factory settings"

    def execute(self, context):
        main.initInterface()
        return{'FINISHED'}    

class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
    bl_idname = "mhrig.save_settings"
    bl_label = "Save settings"

    def execute(self, context):
        main.saveDefaultSettings(context)
        return{'FINISHED'}    

class OBJECT_OT_ExportRigFileButton(bpy.types.Operator):
    bl_idname = "mhrig.export_rig_file"
    bl_label = "Export Rig file"

    def execute(self, context):
        main.exportRigFile(context)
        return{'FINISHED'}    

class OBJECT_OT_AutoWeightBodyButton(bpy.types.Operator):
    bl_idname = "mhrig.auto_weight_body"
    bl_label = "Auto weight MH body"

    def execute(self, context):
        main.autoWeightBody(context)
        return{'FINISHED'}    

class OBJECT_OT_AutoWeightHelpersButton(bpy.types.Operator):
    bl_idname = "mhrig.auto_weight_helpers"
    bl_label = "Auto weight MH helpers"

    def execute(self, context):
        main.autoWeightHelpers(context)
        return{'FINISHED'}    

#
#    Init and register
#

def register():
    main.initInterface()
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

