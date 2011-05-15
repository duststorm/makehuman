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
    'version': '0.8',
    'blender': (2, 5, 6),
    "api": 35774,
    "location": "View3D > UI panel > MHX Lipsync, MHX Expressions, MHX Pose",
    "description": "Lipsync, expression, pose tool for the MHX rig",
    "warning": "",
    'wiki_url': 'http://sites.google.com/site/makehumandocs/blender-export-and-mhx/pose-tool',
    "category": "3D View"}

import bpy, os, mathutils
from mathutils import *
from bpy.props import *

theRig = None
theMesh = None

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

def getVisemeSet(context):
    try:
        visset = theRig['MhxVisemeSet']
    except:
        return bodyLanguageVisemes
    if visset == 'StopStaring':
        return stopStaringVisemes
    elif visset == 'BodyLanguage':
        return bodyLanguageVisemes
    else:
        raise NameError("Unknown viseme set %s" % visset)

def setViseme(context, vis, setKey, frame):
    global theRig
    pbones = theRig.pose.bones
    try:
        scale = pbones['PFace'].bone.length
    except:
        return
    visemes = getVisemeSet(context)
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
    context.scene.objects.active = theRig
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
    context.scene.objects.active = theRig
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
        setGlobals(context)
        if theRig:
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


###################################################################################    
#
#    Expression panel
#
###################################################################################    

#
#    Expressions - the same as in read_expression.py
#

Expressions = [
    'smile',
    'hopeful',
    'innocent',
    'tender',
    'seductive',

    'grin',
    'excited',
    'ecstatic',

    'proud',
    'pleased',
    'amused',
    'laughing1',
    'laughing2',

    'so-so',
    'blue',
    'depressed',
    'sad',
    'distressed',
    'crying',
    'pain',

    'disappointed',
    'frustrated',
    'stressed',
    'worried',
    'scared',
    'terrified',

    'shy',
    'guilty',
    'embarassed',
    'relaxed',
    'peaceful',
    'refreshed',

    'lazy',
    'bored',
    'tired',
    'drained',
    'sleepy',
    'groggy',

    'curious',
    'surprised',
    'impressed',
    'puzzled',
    'shocked',
    'frown',
    'upset',
    'angry',
    'enraged',

    'skeptical',
    'vindictive',
    'pout',
    'furious',
    'grumpy',
    'arrogant',
    'sneering',
    'haughty',
    'disgusted',
]


#
#    meshHasExpressions(mesh):
#    rigHasExpressions(rig):
#
    
def meshHasExpressions(mesh):
    try:
        mesh.data.shape_keys.key_blocks['guilty']
        return True
    except:
        return False

def rigHasExpressions(rig):
    try:
        rig['guilty']
        return True
    except:
        return False

#
#    class VIEW3D_OT_MhxResetExpressionsButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxResetExpressionsButton(bpy.types.Operator):
    bl_idname = "mhx.pose_reset_expressions"
    bl_label = "Reset expressions"

    def execute(self, context):
        global theMesh
        skeys = theMesh.data.shape_keys
        if skeys:
            for name in Expressions:
                try:
                    skeys.key_blocks[name].value = 0.0
                except:
                    pass
        print("Expressions reset")
        return{'FINISHED'}    

#
#    class VIEW3D_OT_MhxResetRigExpressionsButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxResetRigExpressionsButton(bpy.types.Operator):
    bl_idname = "mhx.pose_reset_rig_expressions"
    bl_label = "Reset expressions"

    def execute(self, context):
        global theRig
        for name in Expressions:
            try:
                theRig[name] = 0.0
            except:
                pass
        print("Expressions reset")
        return{'FINISHED'}
        
#
#    createExpressionDrivers(context):    
#
#    class VIEW3D_OT_MhxCreateExpressionDriversButton(bpy.types.Operator):
#

def createExpressionDrivers(context):        
    global theMesh, theRig
    skeys = theMesh.data.shape_keys
    context.scene.objects.active = theRig
    if skeys:
        for name in Expressions:
            try:
                theRig[name] = skeys.key_blocks[name].value
                exists = True
            except:
                exists = False
            if exists:
                theRig[name].min = 0.0
                theRig[name].max = 1.0
                bpy.ops.wm.properties_edit(data_path="object", property=name, min=0, max=1)
                createExpressionDriver(name, skeys)
    return
                
def createExpressionDriver(name, skeys):
    global theRig
    print("Create driver %s" % name)
    fcu = skeys.key_blocks[name].driver_add('value')

    drv = fcu.driver
    drv.type = 'AVERAGE'
    drv.show_debug_info = True

    var = drv.variables.new()
    var.name = name
    var.type = 'SINGLE_PROP'

    trg = var.targets[0]
    trg.id = theRig
    trg.data_path = '["%s"]' % name

    return
    
class VIEW3D_OT_MhxCreateExpressionDriversButton(bpy.types.Operator):
    bl_idname = "mhx.pose_create_drivers"
    bl_label = "Create drivers"

    def execute(self, context):
        createExpressionDrivers(context)
        print("ExpressionDrivers created")
        return{'FINISHED'}    

#
#    removeExpressionDrivers(context):        
#    class VIEW3D_OT_MhxRemoveExpressionDriversButton(bpy.types.Operator):
#

def removeExpressionDrivers(context):        
    global theMesh, theRig
    skeys = theMesh.data.shape_keys
    if skeys:
        context.scene.objects.active = theRig
        for name in Expressions:            
            try:
                del(theRig[name])
                print("Removed prop", name)
            except:
                pass
            try:
                skeys.key_blocks[name].driver_remove('value')
                print("Removed driver %s" % name)
            except:
                pass
    return

class VIEW3D_OT_MhxRemoveExpressionDriversButton(bpy.types.Operator):
    bl_idname = "mhx.pose_remove_drivers"
    bl_label = "Remove drivers"

    def execute(self, context):
        removeExpressionDrivers(context)
        print("ExpressionDrivers removed")
        return{'FINISHED'}    

#
#    class VIEW3D_OT_MhxKeyExpressionButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxKeyExpressionsButton(bpy.types.Operator):
    bl_idname = "mhx.pose_key_expressions"
    bl_label = "Key expressions"

    def execute(self, context):
        global theMesh
        skeys = theMesh.data.shape_keys
        keyAll = context.scene.MhxKeyAll
        if skeys:
            keylist = findActiveFcurves(skeys.animation_data)
            frame = context.scene.frame_current
            for name in Expressions:
                try:
                    shape = skeys.key_blocks[name]
                except:
                    shape = None
                if shape and (keyAll or (name in keylist)):
                    shape.keyframe_insert("value", index=-1, frame=frame)
        return{'FINISHED'}    

def findActiveFcurves(adata):            
    if adata:
        action = adata.action
    else:
        return []
    if action:
        keylist = []
        for fcu in action.fcurves:
            words = fcu.data_path.split('"')
            keylist.append(words[1])
        return keylist
    return []
    
#
#    class VIEW3D_OT_MhxKeyExpressionButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxKeyDriversButton(bpy.types.Operator):
    bl_idname = "mhx.pose_key_drivers"
    bl_label = "Key drivers"
    keyall = bpy.props.BoolProperty()

    def execute(self, context):
        global theRig
        frame = context.scene.frame_current
        keyAll = context.scene.MhxKeyAll
        keylist = findActiveFcurves(theRig.animation_data)
        for name in Expressions:
            try:
                oldvalue = theRig[name]
                success = True
            except:
                success = False
            if success and (keyAll or (name in keylist)):
                theRig.keyframe_insert('["%s"]' % name, index=-1, frame=frame)
        return{'FINISHED'}    

#
#    class VIEW3D_OT_MhxPinExpressionButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxPinExpressionButton(bpy.types.Operator):
    bl_idname = "mhx.pose_pin_expression"
    bl_label = "Pin"
    expression = bpy.props.StringProperty()

    def execute(self, context):
        global theMesh
        skeys = theMesh.data.shape_keys
        keyAll = context.scene.MhxKeyAll
        if skeys:
            frame = context.scene.frame_current
            for name in Expressions:
                value = 1.0 if name == self.expression else 0.0
                try:
                    shape = skeys.key_blocks[name]
                except:
                    shape = None
                if shape:
                    oldvalue = shape.value
                    shape.value = value
                    if (context.tool_settings.use_keyframe_insert_auto and 
                        (keyAll or (value > 0.01) or (abs(value-oldvalue) > 0.01))):
                        shape.keyframe_insert("value", index=-1, frame=frame)
        return{'FINISHED'}    

#
#    class VIEW3D_OT_MhxPinDriverButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxPinDriverButton(bpy.types.Operator):
    bl_idname = "mhx.pose_pin_driver"
    bl_label = "Pin"
    driver = bpy.props.StringProperty()

    def execute(self, context):
        global theRig
        frame = context.scene.frame_current
        keyAll = context.scene.MhxKeyAll
        for name in Expressions:
            value = 1.0 if name == self.driver else 0.0
            try:
                oldvalue = theRig[name]
                success = True
            except:
                success = False

            if success:
                theRig[name] = value
                context.scene.update()
                if (context.tool_settings.use_keyframe_insert_auto and
                    (keyAll or (value > 0.01) or (abs(value-oldvalue) > 0.01))):
                    theRig.keyframe_insert('["%s"]' % name, index=-1, frame=frame)
        return{'FINISHED'}    

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
        setGlobals(context)
        layout = self.layout
        
        if theRig and rigHasExpressions(theRig):
            layout.separator()
            layout.label(text="Expressions (driven)")
            layout.operator("mhx.pose_reset_rig_expressions")
            if theMesh:
                layout.operator("mhx.pose_remove_drivers")
            layout.prop(context.scene, "MhxKeyAll")
            layout.operator("mhx.pose_key_drivers")
            layout.separator()
            for name in Expressions:
                try:
                    prop = theRig[name]
                except:
                    prop = -10
                if prop > -5:
                    row = layout.split(0.75)
                    row.prop(theRig, '["%s"]' % name, index=-1, text=name)
                    row.operator("mhx.pose_pin_driver").driver = name
        
        elif theMesh and meshHasExpressions(theMesh):    
            layout.separator()
            layout.label(text="Expressions")
            layout.operator("mhx.pose_reset_expressions")
            layout.operator("mhx.pose_create_drivers")
            layout.prop(context.scene, "MhxKeyAll")
            layout.operator("mhx.pose_key_expressions")
            layout.separator()
            skeys = theMesh.data.shape_keys
            if skeys:
                for name in Expressions:
                    try:
                        datum = skeys.key_blocks[name]
                    except:
                        datum = None
                    if datum:
                        row = layout.split(0.75)
                        row.prop(datum, 'value', text=name)
                        row.operator("mhx.pose_pin_expression").expression = name
        return

###################################################################################    
#
#    Posing panel
#
###################################################################################    

# 

RNA_PROPS = False

# Property types
D_ENUM = 1
D_INT = 2
D_FLOAT = 3
D_BOOL = 4
D_BOOLINV = 5
D_MULTIVAR = 6

PropTypeName = ['', 'Enum', 'Int', 'Float', 'Bool', 'Bool', '']

#    Parenting
ParentProperties = [
    ('RootParent', D_ENUM, ["Floor","Hips","Neck"], 'name="Master", description=""' ),
    ('GazeParent', D_ENUM, ['Head','World'], 'name="Gaze", description=""' ),
]

MasterDrivers = [
    ('Floor', ['RootParent'], 'x1==0'),
    ('Hips', ['RootParent'], 'x1==1'),
    ('Neck', ['RootParent'], 'x1==2')
]

ParentConstraintDrivers = {
    'Root' :        MasterDrivers,
    'Elbow_L' :        MasterDrivers,
    'Elbow_R' :        MasterDrivers,
    'Wrist_L' :        MasterDrivers,
    'Wrist_R' :        MasterDrivers,
    'LegIK_L' :        MasterDrivers,
    'LegIK_R' :        MasterDrivers,

    'Gaze' :     [
        ('Head', ['GazeParent'], 'x1==0') ,
        ('World', ['GazeParent'], 'x1==1') 
    ]
}

#
#
#

FloatProperties = [
    ('SpineIK', D_FLOAT, 0.0, 'name="Spine FK/IK", description=""' ),
]

FloatConstraintDrivers = {
    'Spine1' : [ ('Rot', ['SpineIK'], '0.4*x1')],
    'Spine2' : [ ('Rot', ['SpineIK'], '0.4*x1')],
    'Spine3' : [ ('Rot', ['SpineIK'], '0.2*x1')],
}

#    Left - right

LeftRightProperties = [
    ('ArmFkIk', D_FLOAT, 0.0, 'name="Arm FK/IK", description=""' ),
    ('ArmHinge', D_FLOAT, 0.0, 'name="Arm hinge", description=""' ),
    ('ElbowPlant', D_FLOAT, 0.0, 'name="Elbow plant", description=""' ),
    ('ForearmFkIk', D_FLOAT, 0.0, 'name="Forearm FK/IK", description=""' ),
    ('ArmStretch', D_FLOAT, 0.0, 'name="Arm stretch", description=""' ),
    ('HandFollowsWrist', D_FLOAT, 0.0, 'name="Hand follows wrist", description=""' ),

    ('LegFkIk', D_FLOAT, 0.0, 'name="Leg FK/IK", description=""' ),

    ('FingerControl', D_BOOL, True, 'name="Controlled fingers", description=""'),
]

LeftRightConstraintDrivers = {
    'UpArm' : [
        ('Elbow', ['ArmFkIk', 'ElbowPlant', 'ArmStretch'], 'max(x1*x2, x3)')
    ],

    'Elbow' : [
        ('DistShoulder', ['ArmStretch'], '0'),
    ],

    'LoArm' : [
        ('ArmIK', ['ArmFkIk', 'ElbowPlant', 'ForearmFkIk', 'ArmStretch'], 'x1*(1-x2)*(1-x3)*(1-x4)'),
        ('Wrist', ['ArmFkIk', 'ElbowPlant', 'ForearmFkIk', 'ArmStretch'], 'x1*x2*x3*(1-x4) + x4'),
    ],

    'Wrist' : [
        ('DistShoulder', ['ElbowPlant', 'ForearmFkIk', 'ArmStretch'], '(1-x1)*(1-x2)*(1-x3)'),
        ('DistElbow', ['ElbowPlant', 'ForearmFkIk', 'ArmStretch'], 'x1*x2*(1-x3)'),
    ],

    'Hand' : [
        ('FreeIK', ['ArmFkIk', 'ElbowPlant', 'ForearmFkIk'], '(1-x1)*(1-x2)*(1-x3)'),
        ('WristLoc', ['ArmFkIk', 'ForearmFkIk'], '(1-(1-x1)*(1-x2))'),
        ('WristRot', ['ArmFkIk', 'ForearmFkIk', 'HandFollowsWrist'], '(1-(1-x1)*(1-x2))*x3'),
    ],

    'ArmLoc': [
        ('Shoulder', ['ArmHinge'], '1-x1'),
        ('Root', ['ArmHinge'], 'x1'),
    ],

    'LoLeg' : [
        ('LegIK', ['LegFkIk'], 'x1'),
    ],

    'Foot' : [
        ('RevRot', ['LegFkIk'], 'x1'),
        ('RevIK', ['LegFkIk'], 'x1'),
        ('FreeIK', ['LegFkIk'], '1-x1'),
    ],

    'Toe' : [
        ('RevIK', ['LegFkIk'], 'x1'),
    ],
}

#    Finger

def defineFingerPropDrivers():
    global LeftRightConstraintDrivers
    for fnum in range(1,6):
        for lnum in range(1,4):
            if (lnum != 1 or fnum != 1):
                finger = 'Finger-%d-%d' % (fnum,lnum)
                LeftRightConstraintDrivers[finger] = [('Rot', ['FingerControl'], 'x1')]

    return

defineFingerPropDrivers()

#
#    defineProperties():
#

def defineProperties():
    if not RNA_PROPS:
        return
    for (prop, typ, value, options) in LeftRightProperties:
        defineProperty('Left'+prop, typ, value, options)
        defineProperty('Right'+prop, typ, value, options)
    for (prop, typ, value, options) in ParentProperties+FloatProperties:
        defineProperty(prop, typ, value, options)
    return

def defineRnaProperty(prop, typ, value, options):
    expr = 'bpy.types.Object.%s = %sProperty(' % (prop, PropTypeName[typ])
    if typ == D_ENUM:
        items = []
        for val in value:
            items.append( (val,val,val) )
        expr += 'items=%s, ' % items
    else:
        expr += 'default=%s, ' % value
    if typ == D_FLOAT:
        expr += '%s, min = 0.0, max = 1.0)' % options
    else:
        expr += '%s)' % options
    print(expr)
    exec(expr)
    return

#
#    resetProperties()
#    class VIEW3D_OT_MhxResetPropertiesButton(bpy.types.Operator):
#

def resetProperties():
    for (prop, typ, value, options) in LeftRightProperties:
        resetProperty('Left'+prop, typ, value, options)
        resetProperty('Right'+prop, typ, value, options)
    for (prop, typ, value, options) in ParentProperties + FloatProperties:
        resetProperty(prop, typ, value, options)
    return

def resetProperty(prop, typ, value, options):
    global theRig
    if RNA_PROPS:
        expr = "theRig.%s = 0" % prop
        exec(expr)
    elif typ == D_FLOAT:
        theRig[prop] = 0.0
        theRig["_RNA_UI"] = {prop: {"min":0.0, "max":1.0}}
    elif typ == D_INT:
        theRig[prop] = 0
    elif typ == D_BOOL:
        theRig[prop] = False
    elif typ == D_ENUM:
        theRig[prop] = 0

    #print(theRig[prop], theRig["_RNA_UI"])
    return

class VIEW3D_OT_MhxResetPropertiesButton(bpy.types.Operator):
    bl_idname = "mhx.pose_reset_properties"
    bl_label = "Reset properties"
    bl_options = {'REGISTER'}

    def execute(self, context):
        resetProperties()
        print("Properties reset")
        return{'FINISHED'}    


#
#    redefinePropDrivers():
#

def redefinePropDrivers():
    global theRig
    try:
        theRig.pose.bones
    except:
        return
    # Remove old drivers
    for pb in theRig.pose.bones:
        for cns in pb.constraints:
            try:
                cns.driver_remove('influence', -1)
            except:
                pass
    defineProperties()

    # Create new drivers
    for (bone, drivers) in LeftRightConstraintDrivers.items():
        defineDriver(bone+'_L', drivers, 'Left')
        defineDriver(bone+'_R', drivers, 'Right')
    for (bone, drivers) in ParentConstraintDrivers.items():
        defineDriver(bone, drivers, '')
    for (bone, drivers) in FloatConstraintDrivers.items():
        defineDriver(bone, drivers, '')
    return

def defineDriver(bone, drivers, prefix):
    pb = theRig.pose.bones[bone]
    for (cnsName, props, expr) in drivers:
        for cns in pb.constraints:
            if cns.name == cnsName:
                # print(pb.name, cns.name, props, expr)
                addPropDriver(cns, props, expr, prefix)
    return

def addPropDriver(cns, props, expr, prefix):
    global theRig
    fcu = cns.driver_add('influence', -1)
    drv = fcu.driver
    if expr:
        drv.type = 'SCRIPTED'
        drv.expression = expr
    else:
        drv.type = 'AVERAGE'
    drv.show_debug_info = True

    for n,prop in enumerate(props):
        var = drv.variables.new()
        var.name = 'x%d' % (n+1)
        var.type = 'SINGLE_PROP'

        targ = var.targets[0]
        targ.id = theRig
        if RNA_PROPS:
            targ.data_path = prefix+prop
        else:
            targ.data_path = '["%s"]' % (prefix+prop)
    return                


class VIEW3D_OT_MhxTogglePropButton(bpy.types.Operator):
    bl_idname = "mhx.pose_toggle_prop"
    bl_label = "Toggle"
    bl_options = {'REGISTER'}
    strprop = bpy.props.StringProperty()

    def execute(self, context):
        prop = self.strprop
        print(prop)
        if theRig[prop] < 0.5:
            theRig[prop] = 1.0
        else:
            theRig[prop] = 0.0
        if context.tool_settings.use_keyframe_insert_auto:
            scn = context.scene
            theRig.keyframe_insert('["%s"]' % prop, index=-1, frame=scn.frame_current)
        return{'FINISHED'}    


#
#    initCharacter(doReset):
#    class VIEW3D_OT_MhxInitCharacterButton(bpy.types.Operator):
#


def initCharacter(doReset):
    global theRig
    # print("Initializing")
    defineProperties()
    redefinePropDrivers()
    if doReset:    
        resetProperties()
    theRig['MhxRigInited'] = True

    for (prop, typ, value, options) in ParentProperties:
        theRig['Old'+prop] = theRig[prop]
    return

class VIEW3D_OT_MhxInitCharacterButton(bpy.types.Operator):
    bl_idname = "mhx.pose_init_character"
    bl_label = "Initialize character"
    bl_options = {'REGISTER'}
    doReset = BoolProperty()

    def execute(self, context):
        initCharacter(self.doReset)
        print("Character initialized")
        return{'FINISHED'}    

#
#    setInverse(context):
#

def setInverse(context):
    global theRig
    amt = theRig.data
    pbones = theRig.pose.bones
    for (bone, drivers) in ParentConstraintDrivers.items():
        pb = pbones[bone]
        for (cnsName, props, expr) in drivers:
            print(cnsName, expr)
            cns = pb.constraints[cnsName]
            print(cns)
            if cns.type == 'CHILD_OF' and changedProp(props):
                amt.bones.active = pb.bone
                print("Set inverse", pb.name, amt.bones.active, cns.name)
                bpy.ops.constraint.childof_set_inverse(constraint=cns.name, owner='BONE')
    for (prop, typ, value, options) in ParentProperties:
        theRig['Old'+prop] = theRig[prop]
    return

def changedProp(props):
    global theRig
    for prop in props:
        print("old", theRig['Old'+prop])
        print("new", theRig[prop])
        if theRig[prop] != theRig['Old'+prop]:
            return True
    return False
                    
class VIEW3D_OT_MhxSetInverseButton(bpy.types.Operator):
    bl_idname = "mhx.pose_set_inverse"
    bl_label = "Set inverse"

    def execute(self, context):
        setInverse(context)
        return{'FINISHED'}    
                
#
#    class MhxDriversPanel(bpy.types.Panel):
#

class MhxDriversPanel(bpy.types.Panel):
    bl_label = "MHX Drivers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return context.object

    def draw(self, context):
        setGlobals(context)
        if theRig:
            layout = self.layout
            try:
                inited = theRig['MhxRigInited']
            except:
                inited = False

            if not inited:
                layout.operator("mhx.pose_init_character", text='Initialize character').doReset = True
                return

            layout.operator("mhx.pose_init_character", text='Reinitialize character').doReset = False
            layout.operator("mhx.pose_reset_properties")
            pbones = theRig.pose.bones
            
            layout.separator()
            for (prop, typ, values, options) in ParentProperties:
                layout.prop(theRig, '["%s"]' % prop, text=prop, expand=True)
            layout.operator('mhx.pose_set_inverse')

            layout.separator()
            for (prop, typ, values, options) in FloatProperties:
                layout.prop(theRig, '["%s"]' % prop, text=prop, expand=True)

            for prefix in ['Left', 'Right']:
                layout.label(prefix)
                for (prop, typ, values, options) in LeftRightProperties:
                        lprop = prefix+prop
                        #print(lprop, typ, values, options)
                        if typ == D_ENUM:
                            layout.label(prop)
                        row = layout.split(0.75)
                        if RNA_PROPS:
                            row.prop(theRig, lprop, text=prop, expand=True)
                        else:
                            row.prop(theRig, '["%s"]' % lprop, text=prop, toggle=True, expand=True)
                        row.operator("mhx.pose_toggle_prop").strprop = lprop
        return

###################################################################################    
#
#    Layers panel
#
###################################################################################    

MhxLayers = [
    (( 0,    'Root', 'MhxRoot'),
     ( 8,    'Face', 'MhxFace')),
    (( 9,    'Varia', 'MhxVaria'),
     (10,    'Head', 'MhxHead')),
    (( 1,    'FK Spine', 'MhxFKSpine'),
     ( 17,    'IK Spine', 'MhxIKSpine')),
    ('Left', 'Right'),
    (( 2,    'IK Arm', 'MhxIKArm'),
     (18,    'IK Arm', 'MhxIKArm')),
    (( 3,    'FK Arm', 'MhxFKArm'),
     (19,    'FK Arm', 'MhxFKArm')),
    (( 4,    'IK Leg', 'MhxIKLeg'),
     (20,    'IK Leg', 'MhxIKLeg')),
    (( 5,    'FK Leg', 'MhxFKLeg'),
     (21,    'FK Leg', 'MhxFKLeg')),
    (( 6,    'Fingers', 'MhxFingers'),
     (22,    'Fingers', 'MhxFingers')),
    (( 7,    'Links', 'MhxLinks'),
     (23,    'Links', 'MhxLinks')),
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
        return context.object

    def draw(self, context):
        setGlobals(context)
        if theRig:
            layout = self.layout
            layout.operator("mhx.pose_set_all_layers", text='Enable all layers').value = True
            layout.operator("mhx.pose_set_all_layers", text='Disable all layers').value = False
            amt = theRig.data
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
        global theRig
        amt = theRig.data
        #amt.layers = 32*[False]
        for (left,right) in MhxLayers:
            if type(left) != str:
                for (n, name, prop) in [left,right]:
                    amt.layers[n] = self.value
        return{'FINISHED'}    
                
###################################################################################    
#
#    Common functions
#
###################################################################################    

#
#    hasMeshChild(rig):
#    isMhxRig(ob):    
#    setGlobals(context):
#

def hasMeshChild(rig):
    global theMesh
    for child in rig.children:
        if (child.type == 'MESH') and meshHasExpressions(child):
            theMesh = child
            return True
    return False

def isMhxRig(ob):    
    try:
        ob.data.bones['PArmIK_L']
        return True
    except:
        return False

def setGlobals(context):
    global theRig, theMesh, theScale    
    theMesh = None
    theRig = None
    if isMhxRig(context.object):
        theRig = context.object
        if not hasMeshChild(theRig):
            for child in theRig.children:
                if (child.type == 'ARMATURE') and hasMeshChild(child):
                    break
    elif context.object.type == 'MESH':
        if meshHasExpressions(context.object):
            theMesh = context.object
            parent = theMesh.parent
            if isMhxRig(parent):
                theRig = parent
            elif parent:
                grandParent = parent.parent
                if isMhxRig(grandParent):
                    theRig = grandParent
        else:
            return
    else:
        return

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

def init():
    bpy.types.Scene.MhxKeyAll = BoolProperty(
    name="Key all",
    description="Set skeys for all shapes",
    default=False)

def register():
    init()
    bpy.utils.register_module(__name__)
    pass

def unregister():
    bpy.utils.unregister_module(__name__)
    pass


if __name__ == "__main__":
    register()


