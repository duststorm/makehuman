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
Pose tool for the MHX rig and Blender 2.5x.
Version 0.7

Place the script in the .blender/scripts/addons dir
Activate the script in the "Add-Ons" tab (user preferences).
Access from UI panel (N-key) when MHX rig is active.

Alternatively, run the script in the script editor (Alt-P), and access from UI panel.
"""

bl_info = {
    'name': 'MakeHuman pose tool',
    'author': 'Thomas Larsson',
    'version': '0.9',
    'blender': (2, 5, 9),
    "api": 35774,
    "location": "View3D > UI panel > MHX Lipsync, MHX Expressions, MHX Pose",
    "description": "Lipsync, expression, pose tool for the MHX rig",
    "warning": "",
    'wiki_url': 'http://sites.google.com/site/makehumandocs/blender-export-and-mhx/pose-tool',
    "category": "3D View"}

import bpy, os, mathutils
from mathutils import *
from bpy.props import *

###################################################################################    
#
#    Lipsync panel
#
###################################################################################    

#
#    visemes
#

stopStaringVisemes = ({
    'Rest' : [
        ('PMouth', (0,0)), 
        ('PUpLip', (0,-0.1)), 
        ('PLoLip', (0,0.1)), 
        ('PJaw', (0,0.05)), 
        ('PTongue', (0,0.0))], 
    'Etc' : [
        ('PMouth', (0,0)),
        ('PUpLip', (0,-0.1)),
        ('PLoLip', (0,0.1)),
        ('PJaw', (0,0.15)),
        ('PTongue', (0,0.0))], 
    'MBP' : [('PMouth', (-0.3,0)),
        ('PUpLip', (0,1)),
        ('PLoLip', (0,0)),
        ('PJaw', (0,0.1)),
        ('PTongue', (0,0.0))], 
    'OO' : [('PMouth', (-1.5,0)),
        ('PUpLip', (0,0)),
        ('PLoLip', (0,0)),
        ('PJaw', (0,0.2)),
        ('PTongue', (0,0.0))], 
    'O' : [('PMouth', (-1.1,0)),
        ('PUpLip', (0,0)),
        ('PLoLip', (0,0)),
        ('PJaw', (0,0.5)),
        ('PTongue', (0,0.0))], 
    'R' : [('PMouth', (-0.9,0)),
        ('PUpLip', (0,-0.2)),
        ('PLoLip', (0,0.2)),
        ('PJaw', (0,0.2)),
        ('PTongue', (0,0.0))], 
    'FV' : [('PMouth', (0,0)),
        ('PUpLip', (0,0)),
        ('PLoLip', (0,-0.8)),
        ('PJaw', (0,0.1)),
        ('PTongue', (0,0.0))], 
    'S' : [('PMouth', (0,0)),
        ('PUpLip', (0,-0.2)),
        ('PLoLip', (0,0.2)),
        ('PJaw', (0,0.05)),
        ('PTongue', (0,0.0))], 
    'SH' : [('PMouth', (-0.6,0)),
        ('PUpLip', (0,-0.5)),
        ('PLoLip', (0,0.5)),
        ('PJaw', (0,0)),
        ('PTongue', (0,0.0))], 
    'EE' : [('PMouth', (0.3,0)),
        ('PUpLip', (0,-0.3)),
        ('PLoLip', (0,0.3)),
        ('PJaw', (0,0.025)),
        ('PTongue', (0,0.0))], 
    'AH' : [('PMouth', (-0.1,0)),
        ('PUpLip', (0,-0.4)),
        ('PLoLip', (0,0)),
        ('PJaw', (0,0.35)),
        ('PTongue', (0,0.0))], 
    'EH' : [('PMouth', (0.1,0)),
        ('PUpLip', (0,-0.2)),
        ('PLoLip', (0,0.2)),
        ('PJaw', (0,0.2)),
        ('PTongue', (0,0.0))], 
    'TH' : [('PMouth', (0,0)),
        ('PUpLip', (0,-0.5)),
        ('PLoLip', (0,0.5)),
        ('PJaw', (-0.2,0.1)),
        ('PTongue', (0,-0.6))], 
    'L' : [('PMouth', (0,0)),
        ('PUpLip', (0,-0.2)),
        ('PLoLip', (0,0.2)),
        ('PJaw', (0.2,0.2)),
        ('PTongue', (0,-0.8))], 
    'G' : [('PMouth', (0,0)),
        ('PUpLip', (0,-0.1)),
        ('PLoLip', (0,0.1)),
        ('PJaw', (-0.3,0.1)),
        ('PTongue', (0,-0.6))], 

    'Blink' : [('PUpLid', (0,1.0)), ('PLoLid', (0,-1.0))], 
    'Unblink' : [('PUpLid', (0,0)), ('PLoLid', (0,0))], 
})

bodyLanguageVisemes = ({
    'Rest' : [
        ('PMouth', (0,0)), 
        ('PMouthMid', (0,-0.6)), 
        ('PUpLipMid', (0,0)), 
        ('PLoLipMid', (0,0)), 
        ('PJaw', (0,0)), 
        ('PTongue', (0,0))], 
    'Etc' : [
        ('PMouth', (0,0)), 
        ('PMouthMid', (0,-0.4)), 
        ('PUpLipMid', (0,0)), 
        ('PLoLipMid', (0,0)), 
        ('PJaw', (0,0)), 
        ('PTongue', (0,0))], 
    'MBP' : [
        ('PMouth', (0,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,0)), 
        ('PLoLipMid', (0,0)), 
        ('PJaw', (0,0)), 
        ('PTongue', (0,0))], 
    'OO' : [
        ('PMouth', (-1.0,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,0)), 
        ('PLoLipMid', (0,0)), 
        ('PJaw', (0,0.4)), 
        ('PTongue', (0,0))], 
    'O' : [
        ('PMouth', (-0.9,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,0)), 
        ('PLoLipMid', (0,0)), 
        ('PJaw', (0,0.8)), 
        ('PTongue', (0,0))], 
    'R' : [
        ('PMouth', (-0.5,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,-0.2)), 
        ('PLoLipMid', (0,0.2)), 
        ('PJaw', (0,0)), 
        ('PTongue', (0,0))], 
    'FV' : [
        ('PMouth', (-0.2,0)), 
        ('PMouthMid', (0,1.0)), 
        ('PUpLipMid', (0,0)), 
        ('PLoLipMid', (-0.6,-0.3)), 
        ('PJaw', (0,0)), 
        ('PTongue', (0,0))], 
    'S' : [
        ('PMouth', (0,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,-0.5)), 
        ('PLoLipMid', (0,0.7)), 
        ('PJaw', (0,0)), 
        ('PTongue', (0,0))], 
    'SH' : [
        ('PMouth', (-0.8,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,-1.0)), 
        ('PLoLipMid', (0,1.0)), 
        ('PJaw', (0,0)), 
        ('PTongue', (0,0))], 
    'EE' : [
        ('PMouth', (0.2,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,-0.6)), 
        ('PLoLipMid', (0,0.6)), 
        ('PJaw', (0,0.05)), 
        ('PTongue', (0,0))], 
    'AH' : [
        ('PMouth', (0,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,-0.4)), 
        ('PLoLipMid', (0,0)), 
        ('PJaw', (0,0.7)), 
        ('PTongue', (0,0))], 
    'EH' : [
        ('PMouth', (0,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,-0.5)), 
        ('PLoLipMid', (0,0.6)), 
        ('PJaw', (0,0.25)), 
        ('PTongue', (0,0))], 
    'TH' : [
        ('PMouth', (0,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,0)), 
        ('PLoLipMid', (0,0)), 
        ('PJaw', (0,0.2)), 
        ('PTongue', (1.0,1.0))], 
    'L' : [
        ('PMouth', (0,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,-0.5)), 
        ('PLoLipMid', (0,0.5)), 
        ('PJaw', (0,-0.2)), 
        ('PTongue', (1.0,1.0))], 
    'G' : [
        ('PMouth', (0,0)), 
        ('PMouthMid', (0,0)), 
        ('PUpLipMid', (0,-0.5)), 
        ('PLoLipMid', (0,0.5)), 
        ('PJaw', (0,-0.2)), 
        ('PTongue', (-1.0,0))], 

    'Blink' : [('PUpLid', (0,1.0)), ('PLoLid', (0,-1.0))], 
    'Unblink' : [('PUpLid', (0,0)), ('PLoLid', (0,0))], 
})

VisemeList = [
    ('Rest', 'Etc', 'AH'),
    ('MBP', 'OO', 'O'),
    ('R', 'FV', 'S'),
    ('SH', 'EE', 'EH'),
    ('TH', 'L', 'G')
]

#
#    mohoVisemes
#    magpieVisemes
#

mohoVisemes = dict({
    'rest' : 'Rest', 
    'etc' : 'Etc', 
    'AI' : 'AH', 
    'O' : 'O', 
    'U' : 'OO', 
    'WQ' : 'AH', 
    'L' : 'L', 
    'E' : 'EH', 
    'MBP' : 'MBP', 
    'FV' : 'FV', 
})

magpieVisemes = dict({
    "CONS" : "t,d,k,g,T,D,s,z,S,Z,h,n,N,j,r,tS", 
    "AI" : "i,&,V,aU,I,0,@,aI", 
    "E" : "eI,3,e", 
    "O" : "O,@U,oI", 
    "UW" : "U,u,w", 
    "MBP" : "m,b,p", 
    "L" : "l", 
    "FV" : "f,v", 
    "Sh" : "dZ", 
})

#
#    setViseme(context, vis, setKey, frame):
#    setBoneLocation(context, pbone, loc, mirror, setKey, frame):
#    class VIEW3D_OT_MhxVisemeButton(bpy.types.Operator):
#

def getVisemeSet(context, rig):
    try:
        visset = rig['MhxVisemeSet']
    except:
        return bodyLanguageVisemes
    if visset == 'StopStaring':
        return stopStaringVisemes
    elif visset == 'BodyLanguage':
        return bodyLanguageVisemes
    else:
        raise NameError("Unknown viseme set %s" % visset)

def setViseme(context, vis, setKey, frame):
    rig = getMhxRig(context.object)
    pbones = rig.pose.bones
    try:
        scale = pbones['PFace'].bone.length
    except:
        return
    visemes = getVisemeSet(context, rig)
    for (b, (x, z)) in visemes[vis]:
        loc = mathutils.Vector((float(x),0,float(z)))
        try:
            pb = pbones[b]
        except:

            pb = None
            
        if pb:
            setBoneLocation(context, pb, scale, loc, False, setKey, frame)
        else:
            setBoneLocation(context, pbones[b+'_L'], scale, loc, False, setKey, frame)
            setBoneLocation(context, pbones[b+'_R'], scale, loc, True, setKey, frame)
    return

def setBoneLocation(context, pb, scale, loc, mirror, setKey, frame):
    if mirror:
        loc[0] = -loc[0]
    pb.location = loc*scale*0.2

    if setKey or context.tool_settings.use_keyframe_insert_auto:
        for n in range(3):
            pb.keyframe_insert('location', index=n, frame=frame, group=pb.name)
    return

class VIEW3D_OT_MhxVisemeButton(bpy.types.Operator):
    bl_idname = 'mhx.pose_viseme'
    bl_label = 'Viseme'
    viseme = bpy.props.StringProperty()

    def invoke(self, context, event):
        setViseme(context, self.viseme, False, context.scene.frame_current)
        return{'FINISHED'}



#
#    openFile(context, filepath):
#    readMoho(context, filepath, offs):
#    readMagpie(context, filepath, offs):
#

def openFile(context, filepath):
    (path, fileName) = os.path.split(filepath)
    (name, ext) = os.path.splitext(fileName)
    return open(filepath, "rU")

def readMoho(context, filepath, offs):
    rig = getMhxRig(context.object)
    context.scene.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')    
    fp = openFile(context, filepath)        
    for line in fp:
        words= line.split()
        if len(words) < 2:
            pass
        else:
            vis = mohoVisemes[words[1]]
            setViseme(context, vis, True, int(words[0])+offs)
    fp.close()
    setInterpolation(context.object)
    print("Moho file %s loaded" % filepath)
    return

def readMagpie(context, filepath, offs):
    rig = getMhxRig(context.object)
    context.scene.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')    
    fp = openFile(context, filepath)        
    for line in fp: 
        words= line.split()
        if len(words) < 3:
            pass
        elif words[2] == 'X':
            vis = magpieVisemes[words[3]]
            setViseme(context, vis, True, int(words[0])+offs)
    fp.close()
    setInterpolation(context.object)
    print("Magpie file %s loaded" % filepath)
    return

# 
#    class VIEW3D_OT_MhxLoadMohoButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxLoadMohoButton(bpy.types.Operator):
    bl_idname = "mhx.pose_load_moho"
    bl_label = "Moho (.dat)"
    filepath = StringProperty(name="File Path", description="File path used for importing the file", maxlen= 1024, default= "")
    startFrame = IntProperty(name="Start frame", description="First frame to import", default=1)

    def execute(self, context):
        import bpy, os, mathutils
        readMoho(context, self.properties.filepath, self.properties.startFrame-1)        
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    

#
#    class VIEW3D_OT_MhxLoadMagpieButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxLoadMagpieButton(bpy.types.Operator):
    bl_idname = "mhx.pose_load_magpie"
    bl_label = "Magpie (.mag)"
    filepath = StringProperty(name="File Path", description="File path used for importing the file", maxlen= 1024, default= "")
    startFrame = IntProperty(name="Start frame", description="First frame to import", default=1)

    def execute(self, context):
        import bpy, os, mathutils
        readMagpie(context, self.properties.filepath, self.properties.startFrame-1)        
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    

#
#    class MhxLipsyncPanel(bpy.types.Panel):
#

class MhxLipsyncPanel(bpy.types.Panel):
    bl_label = "MHX Lipsync"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return context.object

    def draw(self, context):
        rig = getMhxRig(context.object)
        if not rig:
            return

        layout = self.layout        
        layout.label(text="Visemes")
        for (vis1, vis2, vis3) in VisemeList:
            row = layout.row()
            row.operator("mhx.pose_viseme", text=vis1).viseme = vis1
            row.operator("mhx.pose_viseme", text=vis2).viseme = vis2
            row.operator("mhx.pose_viseme", text=vis3).viseme = vis3
        layout.separator()
        row = layout.row()
        row.operator("mhx.pose_viseme", text="Blink").viseme = 'Blink'
        row.operator("mhx.pose_viseme", text="Unblink").viseme = 'Unblink'
        layout.label(text="Load file")
        row = layout.row()
        row.operator("mhx.pose_load_moho")
        row.operator("mhx.pose_load_magpie")
        return

###################################################################################    
#
#    Expression panel
#
###################################################################################    
#
#    class VIEW3D_OT_MhxResetExpressionsButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxResetExpressionsButton(bpy.types.Operator):
    bl_idname = "mhx.pose_reset_expressions"
    bl_label = "Reset expressions"

    def execute(self, context):
        rig = getMhxRig(context.object)
        props = getShapeProps(rig)
        for (prop, name) in props:
            rig[prop] = 0.0
        rig.update_tag()
        return{'FINISHED'}    

#
#    class VIEW3D_OT_MhxKeyExpressionButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxKeyExpressionsButton(bpy.types.Operator):
    bl_idname = "mhx.pose_key_expressions"
    bl_label = "Key expressions"

    def execute(self, context):
        rig = getMhxRig(context.object)
        props = getShapeProps(rig)
        frame = context.scene.frame_current
        for (prop, name) in props:
            rig.keyframe_insert('["%s"]' % prop, frame=frame)
        rig.update_tag()
        return{'FINISHED'}    
#
#    class VIEW3D_OT_MhxPinExpressionButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxPinExpressionButton(bpy.types.Operator):
    bl_idname = "mhx.pose_pin_expression"
    bl_label = "Pin"
    expression = bpy.props.StringProperty()

    def execute(self, context):
        rig = getMhxRig(context.object)
        props = getShapeProps(rig)
        if context.tool_settings.use_keyframe_insert_auto:
            frame = context.scene.frame_current
            for (prop, name) in props:
                old = rig[prop]
                if prop == self.expression:
                    rig[prop] = 1.0
                else:
                    rig[prop] = 0.0
                if abs(rig[prop] - old) > 1e-3:
                    rig.keyframe_insert('["%s"]' % prop, frame=frame)
        else:                    
            for (prop, name) in props:
                if prop == self.expression:
                    rig[prop] = 1.0
                else:
                    rig[prop] = 0.0
        rig.update_tag()
        return{'FINISHED'}    

#
#   getShapeProps(ob):        
#

def getShapeProps(rig):
    props = []        
    plist = list(rig.keys())
    plist.sort()
    for prop in plist:
        if prop[0] == '*':
            props.append((prop, prop[1:]))
    return props                

#
#    class MhxExpressionsPanel(bpy.types.Panel):
#

class MhxExpressionsPanel(bpy.types.Panel):
    bl_label = "MHX Expressions"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return context.object

    def draw(self, context):
        rig = getMhxRig(context.object)
        if not rig:
            return
        props = getShapeProps(rig)
        if not props:
            return
        layout = self.layout
        layout.label(text="Expressions")
        layout.operator("mhx.pose_reset_expressions")
        layout.operator("mhx.pose_key_expressions")
        layout.separator()
        for (prop, name) in props:
            row = layout.split(0.75)
            row.prop(rig, '["%s"]' % prop, text=name)
            row.operator("mhx.pose_pin_expression").expression = prop
        return

###################################################################################    
#
#    Posing panel
#
###################################################################################          
#
#    class MhxDriversPanel(bpy.types.Panel):
#

class MhxDriversPanel(bpy.types.Panel):
    bl_label = "MHX Drivers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return pollMhxRig(context.object)

    def draw(self, context):
        lProps = []
        rProps = []
        props = []
        plist = list(context.object.keys())
        plist.sort()
        for prop in plist:
            if prop[-2:] == '_L':
                lProps.append((prop, prop[:-2]))
            elif prop[-2:] == '_R':
                rProps.append((prop, prop[:-2]))
            elif prop[:3] == 'Mhx' or prop[0] == '_' or prop[0] == '*':
                pass
            else:
                props.append(prop)
        ob = context.object
        layout = self.layout
        for prop in props:
            layout.prop(ob, '["%s"]' % prop, text=prop)
        layout.label("Left")
        for (prop, pname) in lProps:
            layout.prop(ob, '["%s"]' % prop, text=pname)
        layout.label("Right")
        for (prop, pname) in rProps:
            layout.prop(ob, '["%s"]' % prop, text=pname)
        return

###################################################################################    
#
#    Layers panel
#
###################################################################################    

MhxLayers = [
    (( 0,    'Root', 'MhxRoot'),
     ( 8,    'Face', 'MhxFace')),
    (( 9,    'Tweak', 'MhxTweak'),
     (10,    'Head', 'MhxHead')),
    (( 1,    'FK Spine', 'MhxFKSpine'),
     (17,    'IK Spine', 'MhxIKSpine')),
    ((13,    'Inv FK Spine', 'MhxInvFKSpine'),
     (29,    'Inv IK Spine', 'MhxInvIKSpine')),
    ('Left', 'Right'),
    (( 2,    'IK Arm', 'MhxIKArm'),
     (18,    'IK Arm', 'MhxIKArm')),
    (( 3,    'FK Arm', 'MhxFKArm'),
     (19,    'FK Arm', 'MhxFKArm')),
    (( 4,    'IK Leg', 'MhxIKLeg'),
     (20,    'IK Leg', 'MhxIKLeg')),
    (( 5,    'FK Leg', 'MhxFKLeg'),
     (21,    'FK Leg', 'MhxFKLeg')),
    ((12,    'Tweak', 'MhxTweak'),
     (28,    'Tweak', 'MhxTweak')),
    (( 6,    'Fingers', 'MhxFingers'),
     (22,    'Fingers', 'MhxFingers')),
    (( 7,    'Links', 'MhxLinks'),
     (23,    'Links', 'MhxLinks')),
    ((11,    'Palm', 'MhxPalm'),
     (27,    'Palm', 'MhxPalm')),
]

#
#    class MhxLayersPanel(bpy.types.Panel):
#

class MhxLayersPanel(bpy.types.Panel):
    bl_label = "MHX Layers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return pollMhxRig(context.object)

    def draw(self, context):
        layout = self.layout
        layout.operator("mhx.pose_set_all_layers", text='Enable all layers').value = True
        layout.operator("mhx.pose_set_all_layers", text='Disable all layers').value = False
        amt = context.object.data
        for (left,right) in MhxLayers:
            row = layout.row()
            if type(left) == str:
                row.label(left)
                row.label(right)
            else:
                for (n, name, prop) in [left,right]:
                    row.prop(amt, "layers", index=n, toggle=True, text=name)
        return

class VIEW3D_OT_MhxSetAllLayersButton(bpy.types.Operator):
    bl_idname = "mhx.pose_set_all_layers"
    bl_label = "Set inverse"
    value = bpy.props.BoolProperty()

    def execute(self, context):
        rig = getMhxRig(context.object)
        for (left,right) in MhxLayers:
            if type(left) != str:
                for (n, name, prop) in [left,right]:
                    rig.data.layers[n] = self.value
        return{'FINISHED'}    
                
###################################################################################    
#
#    Common functions
#
###################################################################################    
#
#   pollMhxRig(ob):
#   getMhxRig(ob):
#

def pollMhxRig(ob):
    try:
        return (ob["MhxRig"] == "MHX")
    except:
        return False
        
def getMhxRig(ob):
    if ob.type == 'ARMATURE':
        rig = ob
    elif ob.type == 'MESH':
        rig = ob.parent
    else:
        return None
    try:        
        if (rig["MhxRig"] == "MHX"):
            return rig
        else:
            return None
    except:
        return None
    
        
#
#    setInterpolation(rig):
#

def setInterpolation(rig):
    if not rig.animation_data:
        return
    act = rig.animation_data.action
    if not act:
        return
    for fcu in act.fcurves:
        for pt in fcu.keyframe_points:
            pt.interpolation = 'LINEAR'
        fcu.extrapolation = 'CONSTANT'
    return
    

###################################################################################    
#
#    initialize and register
#
###################################################################################    

def register():
    bpy.utils.register_module(__name__)
    pass

def unregister():
    bpy.utils.unregister_module(__name__)
    pass


if __name__ == "__main__":
    register()


