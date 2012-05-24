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
#
# Abstract
# Utility for making clothes to MH characters.
#

bl_info = {
    "name": "Make Clothes",
    "author": "Thomas Larsson",
    "version": "0.6",
    "blender": (2, 6, 1),
    "api": 40000,
    "location": "View3D > Properties > Make MH clothes",
    "description": "Make clothes and UVs for MakeHuman characters",
    "warning": "",
    'wiki_url': "http://www.makehuman.org/node/228",
    "category": "MakeHuman"}


if "bpy" in locals():
    print("Reloading makeclothes")
    import imp
    imp.reload(error)
    imp.reload(makeclothes)
    imp.reload(makeuvs)
    imp.reload(base_uv)
else:
    print("Loading makeclothes")
    import bpy
    import os
    from bpy.props import *
    from . import error
    from . import makeclothes
    from . import makeuvs
    from . import base_uv
  
#
#    class MakeClothesPanel(bpy.types.Panel):
#

Confirm = None
ConfirmString = "?"

def isInited(scn):
    global Confirm
    try:
        scn.MCDirectory
        Confirm
        return True
    except:
        return False
    


class MakeClothesPanel(bpy.types.Panel):
    bl_label = "Make Clothes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'MESH')

    def draw(self, context):
        global Confirm, ConfirmString
        layout = self.layout
        scn = context.scene
        if not isInited(scn):
            layout.operator("mhclo.init_interface", text="Initialize")
            return
        if Confirm:
            layout.label(ConfirmString)
            layout.operator(Confirm, text="yes").answer="yes"
            layout.operator(Confirm, text="no").answer="no"
            return
        layout.label("Initialization")
        layout.operator("mhclo.init_interface", text="ReInitialize")
        layout.operator("mhclo.factory_settings")
        layout.operator("mhclo.save_settings")
        layout.separator()
        layout.prop(scn, "MCDirectory")

        layout.separator()
        layout.label("Vertex groups")
        layout.operator("mhclo.print_vnums")
        layout.operator("mhclo.copy_vert_locs")
        layout.separator()
        layout.prop(scn, "MCRemoveGroupType", expand=True)
        layout.operator("mhclo.remove_vertex_groups")
        layout.separator()
        layout.prop(scn, "MCAutoGroupType", expand=True)
        layout.operator("mhclo.auto_vertex_groups")        
        layout.separator()
        layout.prop(scn, "MCKeepVertsUntil", expand=True)
        layout.operator("mhclo.delete_helpers")        
        
        layout.separator()
        layout.label("Materials")
        layout.prop(scn, "MCMaterials")
        layout.prop(scn, "MCBlenderMaterials")
        layout.prop(scn, "MCHairMaterial")
        
        layout.separator()
        layout.label("Textures")
        row = layout.row()
        col = row.column()
        col.prop(scn, "MCUseTexture")   
        col.prop(scn, "MCUseMask")           
        col.prop(scn, "MCUseBump")   
        col.prop(scn, "MCUseNormal")   
        col.prop(scn, "MCUseDisp")   
        col = row.column()
        col.prop(scn, "MCTextureLayer", text = "")   
        col.prop(scn, "MCMaskLayer", text="")   
        col.prop(scn, "MCBumpStrength", text="")   
        col.prop(scn, "MCNormalStrength", text="")   
        col.prop(scn, "MCDispStrength", text="")   
        layout.prop(scn, "MCAllUVLayers")   

        layout.separator()
        layout.label("Mesh type")
        layout.prop(scn, "MCIsMHMesh")
        row = layout.row()
        row.operator("mhclo.make_human", text="Human").isHuman = True
        row.operator("mhclo.make_human", text="Clothing").isHuman = False

        layout.separator()
        layout.label("Make clothes")
        layout.operator("mhclo.make_clothes")
        layout.operator("mhclo.print_clothes")
        layout.separator()
        layout.operator("mhclo.export_obj_file")
        layout.operator("mhclo.export_blender_material")
        
        layout.separator()
        layout.label("UV projection")
        layout.operator("mhclo.recover_seams")
        layout.operator("mhclo.set_seams")
        layout.operator("mhclo.project_uvs")
        layout.operator("mhclo.reexport_mhclo")        
        
        layout.separator()
        layout.label("Shapekeys")
        for skey in makeclothes.ShapeKeys:
            layout.prop(scn, "MC%s" % skey)   
        
        layout.separator()
        layout.label("Z depth")
        layout.prop(scn, "MCZDepthName")   
        layout.operator("mhclo.set_zdepth")
        layout.prop(scn, "MCZDepth")   

        layout.separator()
        layout.label("Boundary")
        layout.prop(scn, "MCBodyPart")   
        layout.prop(scn, "MCExamineBoundary")           
        layout.operator("mhclo.set_boundary")        
        row = layout.row()
        row.prop(scn, "MCX1")
        row.prop(scn, "MCX2")
        row = layout.row()
        row.prop(scn, "MCY1")
        row.prop(scn, "MCY2")
        row = layout.row()
        row.prop(scn, "MCZ1")
        row.prop(scn, "MCZ2")   

        layout.separator()
        drawLicenseInfo(layout, scn)
            
        if not scn.MCUseInternal:
            return
        layout.separator()
        layout.label("For internal use")
        layout.prop(scn, "MCLogging")
        layout.prop(scn, "MCSelfClothed")
        layout.prop(scn, "MCMakeHumanDirectory")
        layout.operator("mhclo.split_human")
        layout.operator("mhclo.export_base_uvs_py")

        #layout.prop(scn, "MCVertexGroups")
        #layout.operator("mhclo.offset_clothes")
        return
        

def drawLicenseInfo(layout, scn):        
        layout.label("Licensing")
        layout.prop(scn, "MCAuthor")
        layout.prop(scn, "MCLicense")
        layout.prop(scn, "MCHomePage")
        layout.label("Tags")
        layout.prop(scn, "MCTag1")
        layout.prop(scn, "MCTag2")
        layout.prop(scn, "MCTag3")
        layout.prop(scn, "MCTag4")
        layout.prop(scn, "MCTag5")
        return        

        
class MakeUVsPanel(bpy.types.Panel):
    bl_label = "Make UVS"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'MESH')

    def draw(self, context):
        global Confirm, ConfirmString
        layout = self.layout
        scn = context.scene
        if not isInited(scn):
            layout.operator("mhclo.init_interface", text="Initialize")
            return
        if Confirm:
            layout.label(ConfirmString)
            layout.operator(Confirm, text="yes").answer="yes"
            layout.operator(Confirm, text="no").answer="no"
            return
        layout.label("Initialization")
        layout.operator("mhclo.init_interface", text="ReInitialize")
        layout.operator("mhclo.factory_settings")
        layout.operator("mhclo.save_settings")
        layout.separator()
        layout.prop(scn, "MCDirectory")

        layout.separator()
        layout.operator("mhclo.recover_seams")
        layout.operator("mhclo.set_seams")

        layout.separator()
        layout.operator("mhclo.export_uvs")
       
        layout.separator()
        drawLicenseInfo(layout, scn)
        return
#
#    class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
#

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
    bl_idname = "mhclo.init_interface"
    bl_label = "Init"

    def execute(self, context):
        makeclothes.initInterface()
        makeclothes.readDefaultSettings(context)
        print("Interface initialized")
        return{'FINISHED'}    

#
#    class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
#

class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
    bl_idname = "mhclo.factory_settings"
    bl_label = "Restore factory settings"

    def execute(self, context):
        makeclothes.initInterface()
        return{'FINISHED'}    

#
#    class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
#

class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
    bl_idname = "mhclo.save_settings"
    bl_label = "Save settings"

    def execute(self, context):
        makeclothes.saveDefaultSettings(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_RecoverSeamsButton(bpy.types.Operator):
#

class OBJECT_OT_RecoverSeamsButton(bpy.types.Operator):
    bl_idname = "mhclo.recover_seams"
    bl_label = "Recover seams"

    def execute(self, context):
        try:
            makeclothes.recoverSeams(context)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    


class OBJECT_OT_SetSeamsButton(bpy.types.Operator):
    bl_idname = "mhclo.set_seams"
    bl_label = "Set seams"

    def execute(self, context):
        try:
            makeclothes.setSeams(context)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
#

class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.make_clothes"
    bl_label = "Make clothes"

    def execute(self, context): 
        try:
            makeclothes.makeClothes(context, True)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    
        
class OBJECT_OT_PrintClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.print_clothes"
    bl_label = "Print mhclo file"

    def execute(self, context):   
        try:
            makeclothes.makeClothes(context, False)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    
        
#
#    class OBJECT_OT_ProjectUVsButton(bpy.types.Operator):
#

class OBJECT_OT_ProjectUVsButton(bpy.types.Operator):
    bl_idname = "mhclo.project_uvs"
    bl_label = "Project UVs"

    def execute(self, context):
        try:
            (human, clothing) = makeclothes.getObjectPair(context)
            makeclothes.unwrapObject(clothing, context)
            makeclothes.projectUVs(human, clothing, context)
            print("UVs projected")
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    
        
#
#   class OBJECT_OT_CopyVertLocsButton(bpy.types.Operator):
#

class OBJECT_OT_CopyVertLocsButton(bpy.types.Operator):
    bl_idname = "mhclo.copy_vert_locs"
    bl_label = "Copy vertex locations"

    def execute(self, context):
        src = context.object
        for trg in context.scene.objects:
            if trg != src and trg.select and trg.type == 'MESH':
                print("Copy vertex locations from %s to %s" % (src.name, trg.name))
                for n,sv in enumerate(src.data.vertices):
                    tv = trg.data.vertices[n]
                    tv.co = sv.co
                print("Vertex locations copied")
        return{'FINISHED'}    

        
#
#   class OBJECT_OT_ExportObjFileButton(bpy.types.Operator):
#

class OBJECT_OT_ExportObjFileButton(bpy.types.Operator):
    bl_idname = "mhclo.export_obj_file"
    bl_label = "Export Obj file"

    def execute(self, context):
        try:
            makeclothes.exportObjFile(context)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    

#
#   class OBJECT_OT_ReexportMhcloButton(bpy.types.Operator):
#

class OBJECT_OT_ReexportMhcloButton(bpy.types.Operator):
    bl_idname = "mhclo.reexport_mhclo"
    bl_label = "Reexport Mhclo file"

    def execute(self, context):
        try:
            makeclothes.reexportMhclo(context)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    

#
#   class OBJECT_OT_ExportBaseUvsPyButton(bpy.types.Operator):
#   class OBJECT_OT_SplitHumanButton(bpy.types.Operator):
#

class OBJECT_OT_ExportBaseUvsPyButton(bpy.types.Operator):
    bl_idname = "mhclo.export_base_uvs_py"
    bl_label = "Export base UV py file"

    def execute(self, context):
        try:
            makeclothes.exportBaseUvsPy(context)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    
        
class OBJECT_OT_SplitHumanButton(bpy.types.Operator):
    bl_idname = "mhclo.split_human"
    bl_label = "Split human"

    def execute(self, context):
        try:
            makeclothes.getObjectPair(context)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    
                
#
#    class OBJECT_OT_ExportBlenderMaterialsButton(bpy.types.Operator):
#

class OBJECT_OT_ExportBlenderMaterialButton(bpy.types.Operator):
    bl_idname = "mhclo.export_blender_material"
    bl_label = "Export Blender material"

    def execute(self, context):
        try:
            pob = makeclothes.getClothing(context)
            (outpath, outfile) = makeclothes.getFileName(pob, context, "mhx")
            makeclothes.exportBlenderMaterial(pob.data, outpath)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_MakeHumanButton(bpy.types.Operator):
#

class OBJECT_OT_MakeHumanButton(bpy.types.Operator):
    bl_idname = "mhclo.make_human"
    bl_label = "Make human"
    isHuman = BoolProperty()

    def execute(self, context):
        try:
            ob = context.object
            ob["MhxMesh"] = self.isHuman
            print("Object %s: Human = %s" % (ob.name, ob["MhxMesh"]))
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_SetBoundaryButton(bpy.types.Operator):
#

class OBJECT_OT_SetBoundaryButton(bpy.types.Operator):
    bl_idname = "mhclo.set_boundary"
    bl_label = "Set boundary"

    def execute(self, context):
        try:
            makeclothes.setBoundary(context)        
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_OffsetClothesButton(bpy.types.Operator):
#

class OBJECT_OT_OffsetClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.offset_clothes"
    bl_label = "Offset clothes"

    def execute(self, context):     
        try:
            makeclothes.offsetCloth(context)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_SetZDepthButton(bpy.types.Operator):
#

class OBJECT_OT_SetZDepthButton(bpy.types.Operator):
    bl_idname = "mhclo.set_zdepth"
    bl_label = "Set Z depth"

    def execute(self, context):
        try:
            makeclothes.setZDepth(context.scene)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    
   
#
#    class VIEW3D_OT_PrintVnumsButton(bpy.types.Operator):
#

class VIEW3D_OT_PrintVnumsButton(bpy.types.Operator):
    bl_idname = "mhclo.print_vnums"
    bl_label = "Print vertex numbers"

    def execute(self, context):
        try:
            makeclothes.printVertNums(context)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    

#
#    class VIEW3D_OT_DeleteHelpersButton(bpy.types.Operator):
#

class VIEW3D_OT_DeleteHelpersButton(bpy.types.Operator):
    bl_idname = "mhclo.delete_helpers"
    bl_label = "Delete helpers until above"
    answer = StringProperty()

    def execute(self, context):
        global Confirm, ConfirmString
        ob = context.object
        scn = context.scene
        if makeclothes.isHuman(ob):
            ConfirmString = "?"
            if self.answer == "":
                nmax = makeclothes.LastVertices[scn.MCKeepVertsUntil]
                ConfirmString = "Delete vertices until %d?" % nmax
                Confirm = self.bl_idname
            elif self.answer == "yes":
                Confirm = ""
                makeclothes.deleteHelpers(context)
            else:
                Confirm = ""
        return{'FINISHED'}    

#
#    class VIEW3D_OT_RemoveVertexGroupsButton(bpy.types.Operator):
#

class VIEW3D_OT_RemoveVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhclo.remove_vertex_groups"
    bl_label = "Remove vertex groups"

    def execute(self, context):
        try:
            makeclothes.removeVertexGroups(context, context.scene.MCRemoveGroupType)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    

#
#   class VIEW3D_OT_AutoVertexGroupsButton(bpy.types.Operator):
#

class VIEW3D_OT_AutoVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhclo.auto_vertex_groups"
    bl_label = "Auto vertex groups"

    def execute(self, context):
        try:
            makeclothes.removeVertexGroups(context, 'All')
            makeclothes.autoVertexGroups(context)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}   

    
#
#    class OBJECT_OT_ExportUVsButton(bpy.types.Operator):
#

class OBJECT_OT_ExportUVsButton(bpy.types.Operator):
    bl_idname = "mhclo.export_uvs"
    bl_label = "Export UVs"

    def execute(self, context):
        try:    
            makeuvs.exportUVs(context)
        except error.MhcloError:
            error.handleError(context)
        return{'FINISHED'}    


#
#    Init and register
#

def register():
    makeclothes.initInterface()
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

