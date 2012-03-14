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


import bpy, os
from bpy.props import *

from . import action

def initInterface(context):

    # Load and retarget
    
    bpy.types.Scene.McpBvhScale = FloatProperty(
        name="Scale", 
        description="Scale the BVH by this value", 
        min=0.0001, max=1000000.0, 
        soft_min=0.001, soft_max=100.0,
        default=0.65)

    bpy.types.Scene.McpAutoScale = BoolProperty(
        name="Auto scale",
        description="Rescale skeleton to match target",
        default=True)

    bpy.types.Scene.McpStartFrame = IntProperty(
        name="Start Frame", 
        description="Starting frame for the animation",
        default=1)

    bpy.types.Scene.McpEndFrame = IntProperty(
        name="Last Frame", 
        description="Last frame for the animation",
        default=32000)

    bpy.types.Scene.McpRot90Anim = BoolProperty(
        name="Rotate 90 deg", 
        description="Rotate 90 degress so Z points up",
        default=True)

    bpy.types.Scene.McpDoSimplify = BoolProperty(
        name="Simplify FCurves", 
        description="Simplify FCurves",
        default=True)
        
    bpy.types.Scene.McpApplyFixes = BoolProperty(
        name="Apply found fixes", 
        description="Apply found fixes",
        default=True)

    bpy.types.Scene.McpNewIkRetarget = BoolProperty(
        name="New IK retarget", 
        description="Use new retarget for IK bones",
        default=False)


    # Subsample and rescale
    
    bpy.types.Scene.McpSubsample = BoolProperty(
        name="Subsample",
        default=False)

    bpy.types.Scene.McpSSFactor = IntProperty(
        name="Subsample factor", 
        description="Sample only every n:th frame",
        min=1, default=1)

    bpy.types.Scene.McpRescale = BoolProperty(
        name="Rescale",
        description="Rescale F-curves after loading",
        default=False)

    bpy.types.Scene.McpRescaleFactor = IntProperty(
        name="Rescale factor", 
        description="Factor for rescaling time",
        min=1, default=1)

    bpy.types.Scene.McpDefaultSS = BoolProperty(
        name="Use default subsample",
        default=True)

    # Simplify

    bpy.types.Scene.McpSimplifyVisible = BoolProperty(
        name="Only visible", 
        description="Simplify only visible F-curves",
        default=False)

    bpy.types.Scene.McpSimplifyMarkers = BoolProperty(
        name="Only between markers", 
        description="Simplify only between markers",
        default=False)

    bpy.types.Scene.McpErrorLoc = FloatProperty(
        name="Max loc error", 
        description="Max error for location FCurves when doing simplification",
        min=0.001,
        default=0.01)

    bpy.types.Scene.McpErrorRot = FloatProperty(
        name="Max rot error", 
        description="Max error for rotation (degrees) FCurves when doing simplification",
        min=0.001,
        default=0.1)

    # Loop
    
    bpy.types.Scene.McpLoopBlendRange = IntProperty(
        name="Blend range", 
        min=1,
        default=5)
    
    bpy.types.Scene.McpLoopLoc = BoolProperty(
        name="Loc", 
        description="Looping affects location",
        default=True)

    bpy.types.Scene.McpLoopRot = BoolProperty(
        name="Rot", 
        description="Looping affects rotation",
        default=True)

    bpy.types.Scene.McpLoopInPlace = BoolProperty(
        name="Loop in place", 
        description="Remove location F-curves",
        default=False)

    bpy.types.Scene.McpLoopZInPlace = BoolProperty(
        name="In place affects Z", 
        default=False)

    bpy.types.Scene.McpRepeatNumber = IntProperty(
        name="Repeat number", 
        min=1,
        default=1)
        
    bpy.types.Scene.McpFirstEndFrame = IntProperty(
        name="First end frame",
        default=1)
        
    bpy.types.Scene.McpSecondStartFrame = IntProperty(
        name="Second start frame",
        default=1)
        
    bpy.types.Scene.McpActionTarget = EnumProperty(
        items = [('Second to new','Second to new','Second to new'),
                 ('Extend second', 'Extend second', 'Extend second'),
                 ('Stitch new', 'Stitch new', 'Stitch new')],
        name = "Action target")

    bpy.types.Scene.McpOutputActionName = StringProperty(
        name="Output action name", 
        maxlen=24,
        default="")
       

    # Plant
    
    bpy.types.Scene.McpPlantCurrent = BoolProperty(
        name="Use current", 
        description="Plant at current",
        default=True)

    bpy.types.Scene.McpPlantLoc = BoolProperty(
        name="Loc", 
        description="Plant location keys",
        default=True)

    bpy.types.Scene.McpPlantRot = BoolProperty(
        name="Rot", 
        description="Plant rotation keys",
        default=False)

    # Props
    
    bpy.types.Scene.McpDirectory = StringProperty(
        name="Directory", 
        description="Directory", 
        maxlen=1024,
        default="")

    bpy.types.Scene.McpPrefix = StringProperty(
        name="Prefix", 
        description="Prefix", 
        maxlen=24,
        default="")

    # Manage actions
    
    bpy.types.Scene.McpFilterActions = BoolProperty(
        name="Filter", 
        description="Filter action names",
        default=False)

    bpy.types.Scene.McpReallyDelete = BoolProperty(
        name="Really delete", 
        description="Delete button deletes action permanently",
        default=False)

    bpy.types.Scene.McpActions = EnumProperty(
        items = [],
        name = "Actions")

    bpy.types.Scene.McpFirstAction = EnumProperty(
        items = [],
        name = "First action")

    bpy.types.Scene.McpSecondAction = EnumProperty(
        items = [],
        name = "Second action")

    scn = context.scene
    if scn:        
        # Load and retarget
        
        scn["McpBvhScale"] = 0.65
        scn["McpAutoScale"] = True
        scn["McpStartFrame"] = 1
        scn["McpEndFrame"] = 32000
        scn["McpRot90Anim"] = True
        scn["McpDoSimplify"] = False
        scn["McpNewIkRetarget"] = False

        # Subsample and rescale
        
        scn["McpSubsample"] = True
        scn["McpSSFactor"] = 1
        scn["McpDefaultSS"] = True
        scn["McpRescaleFactor"] = 1
        scn["McpRescale"] = False
        
        # Simplify
        
        scn["McpSimplifyVisible"] = False
        scn["McpSimplifyMarkers"] = False
        scn["McpApplyFixes"] = True
        scn["McpErrorLoc"] = 0.01
        scn["McpErrorRot"] = 0.1
        
        # Loop
    
        scn["McpLoopBlendRange"] = 5
        scn["McpLoopLoc"] = True
        scn["McpLoopRot"] = True
        scn["McpLoopInPlace"] = False
        scn["McpLoopZInPlace"] = False
        scn["McpRepeatNumber"] = 1
        scn["McpFirstEndFrame"] = 1
        scn["McpSecondStartFrame"] = 1
        scn["McpFirstAction"] = 0
        scn["McpSecondAction"] = 0
        scn["McpUseNewOutputAction"] = False
        scn["McpOutputActionName"] = ""
    
        # Plant
        
        scn["McpPlantCurrent"] = True
        scn["McpPlantLoc"] = True
        scn["McpPlantRot"] = False

        # Props
        
        scn["McpPrefix"] = "Female1_A"
        scn["McpDirectory"] = "~/makehuman/bvh/Female1_bvh"
        
        # Manage actions            
        
        scn["McpFilterActions"] = False
        scn["McpReallyDelete"] = False
        action.listAllActions(context)
        print("Default scene properties set")
    else:
        print("Warning - no scene - scene properties not set")

    bpy.types.Object.McpArmature = StringProperty()
    
    bpy.types.Object.McpTogglePoleTargets = BoolProperty(default=True)
    bpy.types.Object.McpToggleIkLimits = BoolProperty(default=False)
    bpy.types.Object.McpToggleLimitConstraints = BoolProperty(default=True)


#
#    ensureInited(context):
#

def ensureInited(context):
    try:
        context.scene["McpBvhScale"]
        inited = True
    except:
        inited = False
    if not inited:
        initInterface(context)
    return

#
#    loadDefaults(context):
#

def settingsFile():
    outdir = os.path.expanduser("~/makehuman/settings/")        
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    return os.path.join(outdir, "mocap.defaults")

def loadDefaults(context):
    if not context.scene:
        return
    filename = settingsFile()
    try:
        fp = open(filename, "r")
    except:
        print("Unable to open %s for reading" % filename)
        return
    for line in fp:
        words = line.split()
        if len(words) < 2:
            continue
        try:
            val = eval(words[1])
        except:
            val = words[1]
        context.scene[words[0]] = val
    fp.close()
    print("Defaults loaded from %s" % filename)
    return

#
#    saveDefaults(context):
#

def saveDefaults(context):
    if not context.scene:
        return
    filename = settingsFile()
    try:

        fp = open(filename, "w")
    except:
        print("Unable to open %s for writing" % filename)
        return
    for (key,value) in context.scene.items():
        if key[:3] == "Mcp":
            fp.write("%s %s\n" % (key, value))
    fp.close()
    print("Defaults saved to %s" % filename)
    return
    

########################################################################
#
#   class VIEW3D_OT_McpInitInterfaceButton(bpy.types.Operator):
#   class VIEW3D_OT_McpSaveDefaultsButton(bpy.types.Operator):
#   class VIEW3D_OT_McpLoadDefaultsButton(bpy.types.Operator):
#

class VIEW3D_OT_McpInitInterfaceButton(bpy.types.Operator):
    bl_idname = "mcp.init_interface"
    bl_label = "Initialize"

    def execute(self, context):
        initInterface(context)
        print("Interface initialized")
        return{"FINISHED"}    

class VIEW3D_OT_McpSaveDefaultsButton(bpy.types.Operator):
    bl_idname = "mcp.save_defaults"
    bl_label = "Save defaults"

    def execute(self, context):
        saveDefaults(context)
        return{"FINISHED"}    

class VIEW3D_OT_McpLoadDefaultsButton(bpy.types.Operator):
    bl_idname = "mcp.load_defaults"
    bl_label = "Load defaults"

    def execute(self, context):
        loadDefaults(context)
        return{"FINISHED"}    

#
#    class VIEW3D_OT_McpCopyAnglesIKButton(bpy.types.Operator):
#

class VIEW3D_OT_McpCopyAnglesIKButton(bpy.types.Operator):
    bl_idname = "mcp.copy_angles_fk_ik"
    bl_label = "Angles  --> IK"

    def execute(self, context):
        copyAnglesIK(context)
        print("Angles copied")
        return{"FINISHED"}    


#
#    readDirectory(directory, prefix):
#    class VIEW3D_OT_McpBatchButton(bpy.types.Operator):
#

def readDirectory(directory, prefix):
    realdir = os.path.realpath(os.path.expanduser(directory))
    files = os.listdir(realdir)
    n = len(prefix)
    paths = []
    for fileName in files:
        (name, ext) = os.path.splitext(fileName)
        if name[:n] == prefix and ext == ".bvh":
            paths.append("%s/%s" % (realdir, fileName))
    return paths

class VIEW3D_OT_McpBatchButton(bpy.types.Operator):
    bl_idname = "mcp.batch"
    bl_label = "Batch run"

    def execute(self, context):
        paths = readDirectory(context.scene["McpDirectory"], context.scene["McpPrefix"])
        trgRig = context.object
        for filepath in paths:
            context.scene.objects.active = trgRig
            loadRetargetSimplify(context, filepath)
        return{"FINISHED"}    

#
#    class PropsPanel(bpy.types.Panel):
#

class PropsPanel(bpy.types.Panel):
    bl_label = "Mocap: Init"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        if context.object and context.object.type == "ARMATURE":
            return True

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        ob = context.object
        layout.operator("mcp.init_interface")
        layout.operator("mcp.save_defaults")
        layout.operator("mcp.load_defaults")
        return
        layout.operator("mcp.copy_angles_fk_ik")

        layout.separator()
        layout.label("Batch conversion")
        layout.prop(scn, "McpDirectory")
        layout.prop(scn, "McpPrefix")
        layout.operator("mcp.batch")
        return

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()



