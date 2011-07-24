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


import bpy
from bpy.props import StringProperty, FloatProperty, IntProperty, BoolProperty, EnumProperty

from . import action

def initInterface(context):

    # Load and retarget
    
    bpy.types.Scene.MhxBvhScale = FloatProperty(
        name="Scale", 
        description="Scale the BVH by this value", 
        min=0.0001, max=1000000.0, 
        soft_min=0.001, soft_max=100.0,
        default=0.65)

    bpy.types.Scene.MhxAutoScale = BoolProperty(
        name="Auto scale",
        description="Rescale skeleton to match target",
        default=True)

    bpy.types.Scene.MhxStartFrame = IntProperty(
        name="Start Frame", 
        description="Starting frame for the animation",
        default=1)

    bpy.types.Scene.MhxEndFrame = IntProperty(
        name="Last Frame", 
        description="Last frame for the animation",
        default=32000)

    bpy.types.Scene.MhxRot90Anim = BoolProperty(
        name="Rotate 90 deg", 
        description="Rotate 90 degress so Z points up",
        default=True)

    bpy.types.Scene.MhxDoSimplify = BoolProperty(
        name="Simplify FCurves", 
        description="Simplify FCurves",
        default=True)
        
    bpy.types.Scene.MhxApplyFixes = BoolProperty(
        name="Apply found fixes", 
        description="Apply found fixes",
        default=True)

    # Subsample and rescale
    
    bpy.types.Scene.MhxSubsample = BoolProperty(
        name="Subsample",
        default=False)

    bpy.types.Scene.MhxSSFactor = IntProperty(
        name="Subsample factor", 
        description="Sample only every n:th frame",
        min=1, default=1)

    bpy.types.Scene.MhxRescale = BoolProperty(
        name="Rescale",
        description="Rescale F-curves after loading",
        default=False)

    bpy.types.Scene.MhxRescaleFactor = IntProperty(
        name="Rescale factor", 
        description="Factor for rescaling time",
        min=1, default=1)

    bpy.types.Scene.MhxDefaultSS = BoolProperty(
        name="Use default subsample",
        default=True)

    # Simplify

    bpy.types.Scene.MhxSimplifyVisible = BoolProperty(
        name="Only visible", 
        description="Simplify only visible F-curves",
        default=False)

    bpy.types.Scene.MhxSimplifyMarkers = BoolProperty(
        name="Only between markers", 
        description="Simplify only between markers",
        default=False)

    bpy.types.Scene.MhxErrorLoc = FloatProperty(
        name="Max loc error", 
        description="Max error for location FCurves when doing simplification",
        min=0.001,
        default=0.01)

    bpy.types.Scene.MhxErrorRot = FloatProperty(
        name="Max rot error", 
        description="Max error for rotation (degrees) FCurves when doing simplification",
        min=0.001,
        default=0.1)

    # Loop
    
    bpy.types.Scene.MhxLoopBlendRange = IntProperty(
        name="Blend range", 
        min=1,
        default=5)
    
    bpy.types.Scene.MhxLoopInPlace = BoolProperty(
        name="Loop in place", 
        description="Remove location F-curves",
        default=False)

    bpy.types.Scene.MhxLoopZInPlace = BoolProperty(
        name="In place affects Z", 
        default=False)

    # Plant
    
    bpy.types.Scene.MhxPlantCurrent = BoolProperty(
        name="Use current", 
        description="Plant at current",
        default=True)

    bpy.types.Scene.MhxPlantLoc = BoolProperty(
        name="Loc", 
        description="Plant location keys",
        default=True)

    bpy.types.Scene.MhxPlantRot = BoolProperty(
        name="Rot", 
        description="Plant rotation keys",
        default=False)

    # Props
    
    bpy.types.Scene.MhxDirectory = StringProperty(
        name="Directory", 
        description="Directory", 
        maxlen=1024,
        default='')

    bpy.types.Scene.MhxPrefix = StringProperty(
        name="Prefix", 
        description="Prefix", 
        maxlen=1024,
        default='')

    # Manage actions
    
    bpy.types.Scene.MhxReallyDelete = BoolProperty(
        name="Really delete action", 
        description="Delete button deletes action permanently",
        default=False)

    bpy.types.Scene.MhxActions = EnumProperty(
        items = [],
        name = "Actions")

    scn = context.scene
    if scn:        
        # Load and retarget
        
        scn['MhxBvhScale'] = 0.65
        scn['MhxAutoScale'] = True
        scn['MhxStartFrame'] = 1
        scn['MhxEndFrame'] = 32000
        scn['MhxRot90Anim'] = True
        scn['MhxDoSimplify'] = True

        # Subsample and rescale
        
        scn['MhxSubsample'] = True
        scn['MhxSSFactor'] = 1
        scn['MhxDefaultSS'] = True
        scn['MhxRescaleFactor'] = 1
        scn['MhxRescale'] = False
        
        # Simplify
        
        scn['MhxSimplifyVisible'] = False
        scn['MhxSimplifyMarkers'] = False
        scn['MhxApplyFixes'] = True
        scn['MhxErrorLoc'] = 0.01
        scn['MhxErrorRot'] = 0.1
        
        # Loop
    
        scn['MhxLoopBlendRange'] = 5
        scn['MhxLoopInPlace'] = False
        scn['MhxLoopZInPlace'] = False

        # Plant
        
        scn['MhxPlantCurrent'] = True
        scn['MhxPlantLoc'] = True
        scn['MhxPlantRot'] = False

        # Props
        
        scn['MhxPrefix'] = "Female1_A"
        scn['MhxDirectory'] = "~/makehuman/bvh/Female1_bvh"
        
        # Manage actions            
        
        scn['MhxReallyDelete'] = False
        action.listAllActions(context)
    else:
        print("Warning - no scene - scene properties not set")

    bpy.types.Object.MhxArmature = StringProperty()
    
    bpy.types.Object.MhxTogglePoleTargets = BoolProperty(default=True)
    bpy.types.Object.MhxToggleIkLimits = BoolProperty(default=False)
    bpy.types.Object.MhxToggleLimitConstraints = BoolProperty(default=True)


#
#    ensureInited(context):
#

def ensureInited(context):
    try:
        context.scene['MhxBvhScale']
        inited = True
    except:
        inited = False
    if not inited:
        initInterface(context)
    return

#
#    loadDefaults(context):
#

def loadDefaults(context):
    if not context.scene:
        return
    filename = os.path.realpath(os.path.expanduser("~/makehuman/mhx_defaults.txt"))
    try:
        fp = open(filename, "r")
    except:
        print("Unable to open %s for reading" % filename)
        return
    for line in fp:
        words = line.split()
        try:
            val = eval(words[1])
        except:
            val = words[1]
        context.scene[words[0]] = val
    fp.close()
    return

#
#    saveDefaults(context):
#

def saveDefaults(context):
    if not context.scene:
        return
    filename = os.path.realpath(os.path.expanduser("~/makehuman/mhx_defaults.txt"))
    try:

        fp = open(filename, "w")
    except:
        print("Unable to open %s for writing" % filename)
        return
    for (key,value) in context.scene.items():
        if key[:3] == 'Mhx':
            fp.write("%s %s\n" % (key, value))
    fp.close()
    return
    
#
#   getBone(rig, bone)
#

def getBone(rig, bone):
    try:
        return rig[bone]
    except:
        return bone
            

########################################################################
#
#   class VIEW3D_OT_MhxInitInterfaceButton(bpy.types.Operator):
#   class VIEW3D_OT_MhxSaveDefaultsButton(bpy.types.Operator):
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

#
#    class PropsPanel(bpy.types.Panel):
#

class PropsPanel(bpy.types.Panel):
    bl_label = "Mocap: Init"
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
        layout.label('Batch conversion')
        layout.prop(scn, "MhxDirectory")
        layout.prop(scn, "MhxPrefix")
        layout.operator("mhx.mocap_batch")
        return

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()



