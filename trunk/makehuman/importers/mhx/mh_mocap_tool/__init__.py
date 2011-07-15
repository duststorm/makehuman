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
    "category": "3D View"}

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
    imp.reload(action)
    imp.reload(globvar)
    imp.reload(props)
    imp.reload(load)
    imp.reload(plant)
    imp.reload(retarget)
    imp.reload(simplify)
    imp.reload(source)
    imp.reload(target)
    imp.reload(toggle)
    imp.reload(accad)
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
    from bpy.props import StringProperty, FloatProperty, IntProperty, BoolProperty, EnumProperty

    from . import globvar
    from . import props
    from . import action
    from . import simplify
    from . import plant
    from . import load
    from . import source
    from . import target
    from . import toggle
    from . import retarget
    from . import accad, daz, eyes, hdm, max, mb, mega
    from . import rig_mhx, rig_rorkimaru, rig_game


###################################################################################    
#    User interface
#
#    getBvh(mhx)
#

def getBvh(mhx):
    for (bvh, mhx1) in the.armature.items():
        if mhx == mhx1:
            return bvh
    return None

#
#    class Bvh2MhxPanel(bpy.types.Panel):
#

class Bvh2MhxPanel(bpy.types.Panel):
    bl_label = "Bvh to Mhx"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        if context.object and context.object.type == 'ARMATURE':
            return True

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        ob = context.object
                
        layout.operator("mhx.mocap_init_interface")
        layout.operator("mhx.mocap_save_defaults")
        layout.operator("mhx.mocap_copy_angles_fk_ik")

        layout.separator()
        layout.label('Load')
        layout.prop(scn, "MhxBvhScale")
        layout.prop(scn, "MhxAutoScale")
        layout.prop(scn, "MhxStartFrame")
        layout.prop(scn, "MhxEndFrame")
        layout.prop(scn, "MhxSubsample")
        layout.prop(scn, "MhxDefaultSS")
        layout.prop(scn, "MhxRot90Anim")
        layout.prop(scn, "MhxDoSimplify")
        layout.prop(scn, "MhxApplyFixes")
        layout.operator("mhx.mocap_load_bvh")
        layout.operator("mhx.mocap_retarget_mhx")
        layout.separator()
        layout.operator("mhx.mocap_load_retarget_simplify")

        layout.separator()
        layout.label('Toggle')
        row = layout.row()
        row.operator("mhx.mocap_toggle_pole_targets")
        row.prop(ob, "MhxTogglePoleTargets")
        row = layout.row()
        row.operator("mhx.mocap_toggle_ik_limits")
        row.prop(ob, "MhxToggleIkLimits")
        row = layout.row()
        row.operator("mhx.mocap_toggle_limit_constraints")
        row.prop(ob, "MhxToggleLimitConstraints")

        layout.separator()
        layout.label('Plant')
        row = layout.row()
        row.prop(scn, "MhxPlantLoc")
        row.prop(scn, "MhxPlantRot")
        layout.prop(scn, "MhxPlantCurrent")
        layout.operator("mhx.mocap_plant")

        layout.separator()
        layout.label('Simplify')
        layout.prop(scn, "MhxErrorLoc")
        layout.prop(scn, "MhxErrorRot")
        layout.prop(scn, "MhxSimplifyVisible")
        layout.prop(scn, "MhxSimplifyMarkers")
        layout.operator("mhx.mocap_simplify_fcurves")

        layout.separator()
        layout.label('Batch conversion')
        layout.prop(scn, "MhxDirectory")
        layout.prop(scn, "MhxPrefix")
        layout.operator("mhx.mocap_batch")

        layout.separator()
        layout.label('Manage actions')
        layout.prop_menu_enum(scn, "MhxActions")
        layout.operator("mhx.mocap_update_action_list")
        layout.prop(scn, "MhxReallyDelete")
        layout.operator("mhx.mocap_delete")
        return

########################################################################
#
#   props.py
#
#   class VIEW3D_OT_MhxInitInterfaceButton(bpy.types.Operator):
#   class VIEW3D_OT_MhxSaveDefaultsButton(bpy.types.Operator):
#
#
#

class VIEW3D_OT_MhxInitInterfaceButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_init_interface"
    bl_label = "Initialize"

    def execute(self, context):
        from . import props
        props.initInterface(context)
        print("Interface initialized")
        return{'FINISHED'}    


class VIEW3D_OT_MhxSaveDefaultsButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_save_defaults"
    bl_label = "Save defaults"

    def execute(self, context):
        props.saveDefaults(context)
        return{'FINISHED'}    

#
#    class VIEW3D_OT_MhxCopyAnglesIKButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxCopyAnglesIKButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_copy_angles_fk_ik"
    bl_label = "Angles  --> IK"

    def execute(self, context):
        copyAnglesIK(context)
        print("Angles copied")
        return{'FINISHED'}    


#
#    readDirectory(directory, prefix):
#    class VIEW3D_OT_MhxBatchButton(bpy.types.Operator):
#

def readDirectory(directory, prefix):
    realdir = os.path.realpath(os.path.expanduser(directory))
    files = os.listdir(realdir)
    n = len(prefix)
    paths = []
    for fileName in files:
        (name, ext) = os.path.splitext(fileName)
        if name[:n] == prefix and ext == '.bvh':
            paths.append("%s/%s" % (realdir, fileName))
    return paths

class VIEW3D_OT_MhxBatchButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_batch"
    bl_label = "Batch run"

    def execute(self, context):
        paths = readDirectory(context.scene['MhxDirectory'], context.scene['MhxPrefix'])
        trgRig = context.object
        for filepath in paths:
            context.scene.objects.active = trgRig
            loadRetargetSimplify(context, filepath)
        return{'FINISHED'}    


########################################################################
#
#   load.py
#
#   class VIEW3D_OT_MhxLoadBvhButton(bpy.types.Operator, ImportHelper):
#

class VIEW3D_OT_MhxLoadBvhButton(bpy.types.Operator, ImportHelper):
    bl_idname = "mhx.mocap_load_bvh"
    bl_label = "Load BVH file (.bvh)"

    filename_ext = ".bvh"
    filter_glob = StringProperty(default="*.bvh", options={'HIDDEN'})
    filepath = StringProperty(name="File Path", description="Filepath used for importing the BVH file", maxlen=1024, default="")

    def execute(self, context):
        retarget.importAndRename(context, self.properties.filepath)
        print("%s imported" % self.properties.filepath)
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    


########################################################################
#
#   retarget.py
#
#   class VIEW3D_OT_MhxRetargetMhxButton(bpy.types.Operator):
#   class VIEW3D_OT_MhxLoadRetargetSimplify(bpy.types.Operator):
#

class VIEW3D_OT_MhxRetargetMhxButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_retarget_mhx"
    bl_label = "Retarget selected to MHX"

    def execute(self, context):
        trgRig = context.object
        target.guessTargetArmature(trgRig)
        for srcRig in context.selected_objects:
            if srcRig != trgRig:
                retarget.retargetMhxRig(context, srcRig, trgRig)
        return{'FINISHED'}    

class VIEW3D_OT_MhxLoadRetargetSimplifyButton(bpy.types.Operator, ImportHelper):
    bl_idname = "mhx.mocap_load_retarget_simplify"
    bl_label = "Load, retarget, simplify"

    filename_ext = ".bvh"
    filter_glob = StringProperty(default="*.bvh", options={'HIDDEN'})
    filepath = StringProperty(name="File Path", description="Filepath used for importing the BVH file", maxlen=1024, default="")

    def execute(self, context):
        retarget.loadRetargetSimplify(context, self.properties.filepath)
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    

########################################################################
#
#   simplify.py
#
#   class VIEW3D_OT_MhxSimplifyFCurvesButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxSimplifyFCurvesButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_simplify_fcurves"
    bl_label = "Simplify FCurves"

    def execute(self, context):
        scn = context.scene
        simplify.simplifyFCurves(context, context.object, scn.MhxSimplifyVisible, scn.MhxSimplifyMarkers)
        return{'FINISHED'}    

########################################################################
#
#   toggle.py
#
#   class VIEW3D_OT_MhxTogglePoleTargetsButton(bpy.types.Operator):
#   class VIEW3D_OT_MhxToggleIKLimitsButton(bpy.types.Operator):
#   class VIEW3D_OT_MhxToggleLimitConstraintsButton(bpy.types.Operator):
#   class VIEW3D_OT_MhxSilenceConstraintsButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxTogglePoleTargetsButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_toggle_pole_targets"
    bl_label = "Toggle pole targets"

    def execute(self, context):
        res = toggle.togglePoleTargets(context.object)
        print("Pole targets toggled", res)
        return{'FINISHED'}    

class VIEW3D_OT_MhxToggleIKLimitsButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_toggle_ik_limits"
    bl_label = "Toggle IK limits"

    def execute(self, context):
        res = toggle.toggleIKLimits(context.object)
        print("IK limits toggled", res)
        return{'FINISHED'}    

class VIEW3D_OT_MhxToggleLimitConstraintsButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_toggle_limit_constraints"
    bl_label = "Toggle Limit constraints"

    def execute(self, context):
        res = toggle.toggleLimitConstraints(context.object)
        print("Limit constraints toggled", res)
        return{'FINISHED'}    

class VIEW3D_OT_MhxSilenceConstraintsButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_silence_constraints"
    bl_label = "Silence constraints"

    def execute(self, context):
        toggle.silenceConstraints(context.object)
        print("Constraints silenced")
        return{'FINISHED'}    

########################################################################
#
#   plant.py
#
#   class VIEW3D_OT_MhxPlantButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxPlantButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_plant"
    bl_label = "Plant"

    def execute(self, context):
        plant.plantKeys(context)
        print("Keys planted")
        return{'FINISHED'}    

########################################################################
#
#   action.py
#
#   class VIEW3D_OT_MhxUpdateActionListButton(bpy.types.Operator):
#   class VIEW3D_OT_MhxDeleteButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxUpdateActionListButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_update_action_list"
    bl_label = "Update action list"

    @classmethod
    def poll(cls, context):
        return context.object

    def execute(self, context):
        action.listAllActions(context)
        return{'FINISHED'}    

class VIEW3D_OT_MhxDeleteButton(bpy.types.Operator):
    bl_idname = "mhx.mocap_delete"
    bl_label = "Delete action"

    @classmethod
    def poll(cls, context):
        return context.scene.MhxReallyDelete

    def execute(self, context):
        action.deleteAction(context)
        return{'FINISHED'}    



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
#    init and register
#

props.initInterface(bpy.context)

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

#readBvhFile(context, filepath, scale, startFrame, rot90, 1)
#readBvhFile(bpy.context, '/home/thomas/makehuman/bvh/Male1_bvh/Male1_A5_PickUpBox.bvh', 1.0, 1, False)
#readBvhFile(bpy.context, '/home/thomas/makehuman/bvh/cmu/10/10_03.bvh', 1.0, 1, False)
