# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; eithe.r version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the.
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
#from math import sin, cos
from mathutils import *
from bpy.props import *
from bpy_extras.io_utils import ImportHelper

from . import target
from . import globvar as the
       
#
#    guessSrcArmature(rig):
#

def guessSrcArmature(rig):
    bestMisses = 1000
    misses = {}
    bones = rig.data.bones
    for name in the.armatureList:
        amt = the.armatures[name]
        nMisses = 0
        for bone in bones:
            try:
                amt[bone.name.lower()]
            except:
                nMisses += 1
        misses[name] = nMisses
        if nMisses < bestMisses:
            best = amt
            bestName = name
            bestMisses = nMisses
    if bestMisses > 0:
        for bone in bones:
            print("'%s'" % bone.name)
        for (name, n) in misses.items():
            print(name, n)
        raise NameError('Did not find matching armature. nMisses = %d' % bestMisses)
    return (best, bestName)

#
#   findSrcArmature(context, rig):
#

def findSrcArmature(context, rig):
    if useCustomSrcRig(context):
        (the.armature, name, fixes) = buildSrcArmature(context, rig)
        the.armatures[name] = the.armature
        the.fixesList[name] = fixes
    else:
        (the.armature, name) = guessSrcArmature(rig)
    rig['McpArmature'] = name
    print("Using matching armature %s." % name)
    return

#
#    setArmature(rig)
#

def setArmature(rig):
    try:
        name = rig['McpArmature']
    except:
        print("***", rig)
        raise NameError("No armature set")
    the.armature = the.armatures[name]
    print("Set armature %s" % name)
    return
    
###############################################################################
#
#    Source armatures
#
###############################################################################

the.sourceProps = []

#
#    defaultEnums():
#    setSourceProp(scn, prop, mhx, enums):
#    makeSourceBoneList(scn, rig):
#

def defaultEnums():
    enums = [('None','None','None')]
    for bn in target.TargetBoneNames:
        if not bn:
            continue
        (mhx, text) = bn
        enum = (mhx, text, mhx)
        enums.append(enum)
    return enums

def setSourceProp(scn, prop, mhx, enums):
    scn[prop] = 0
    n = 0
    for (mhx1, text1, mhx2) in enums:
        if mhx == mhx1: 
            scn[prop] = n
            return
        n += 1
    return

def makeSourceBoneList(scn, rig):
    root = None
    for bone in rig.data.bones:
        if bone.parent == None:
            root = bone
            break
    if root:
        print("Root bone %s", root)
    else:        
        print("Did not find root bone")
        return
            
    enums = defaultEnums()
    props = []
    makeSourceBones(scn, root, enums, props)
    for prop in props:
        name = prop[2:].lower()
        mhx = guessSourceBone(name)
        setSourceProp(scn, prop, mhx, enums)
    return (props, enums)

#
#    makeSourceBones(scn, bone, enums, props):
#    defineSourceProp(name, enums):
#

def makeSourceBones(scn, bone, enums, props):
    prop = defineSourceProp(bone.name, enums)
    props.append(prop)
    for child in bone.children:
        makeSourceBones(scn, child, enums, props)
    return

def defineSourceProp(name, enums):
    qname = name.replace(' ','_')
    expr = 'bpy.types.Scene.S_%s = EnumProperty(items = enums, name = "%s")' % (qname, name)
    exec(expr)
    return 'S_'+qname

#
#    guessSourceBone(name):
#

def guessSourceBone(name):
    for amtname in the.armatureList:
        amt = the.armatures[amtname]
        try:
            mhx = amt[name]
            return mhx
        except:
            pass
    return ''

#
#    useCustomSrcRig(context):
#

def useCustomSrcRig(context):
    if the.sourceProps:
        try:
            guess = context.scene.McpGuessSrcRig
        except:
            guess = True
        return not guess
    return False

#
#    buildSrcArmature(context, rig):
#

def buildSrcArmature(context, rig):
    amt = {}
    used = {}
    scn = context.scene
    for prop in the.sourceProps:
        name = prop[2:].lower()
        (mhx1, text, mhx2) = the.sourceEnums[scn[prop]]
        if mhx1 == 'None':
            amt[name] = None
            continue
        amt[name] = mhx1
        try:
            user = used[mhx1]
        except:
            user = None
        if user:
            raise NameError("Source bones %s and %s both assigned to %s" % (user, name, mhx1))
        used[mhx1] = name
    fixes = target.createCustomFixes(scn['McpSrcLegBentOut'], scn['McpSrcLegRoll'], scn['McpSrcArmBentDown'], scn['McpSrcArmRoll'])
    return (amt, "MySource", fixes)

#
#    ensureSourceInited(context):
#

def ensureSourceInited(context):
    scn = context.scene
    try:
        scn.McpGuessSrcRig
        return
    except:
        pass
    expr = 'bpy.types.Scene.McpGuessSrcRig = BoolProperty(name = "Guess source rig")'
    exec(expr)    
    scn.McpGuessSrcRig = False
    return

#
#    class VIEW3D_OT_McpScanRigButton(bpy.types.Operator):
#

class VIEW3D_OT_McpScanRigButton(bpy.types.Operator):
    bl_idname = "mcp.scan_rig"
    bl_label = "Scan source rig"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scn = context.scene
        (the.sourceProps, the.sourceEnums) = makeSourceBoneList(scn,  context.object)
        scn['McpSrcArmBentDown'] = 0.0
        scn['McpSrcArmRoll'] = 0.0
        scn['McpSrcLegBentOut'] = 0.0
        scn['McpSrcLegRoll'] = 0.0
        ensureSourceInited(context)
        return{'FINISHED'}    

#
#    saveSourceBones(context, path):
#    loadSourceBones(context, path):
#    class VIEW3D_OT_McpLoadSaveSourceBonesButton(bpy.types.Operator, ImportHelper):
#

def saveSourceBones(context, path):
    scn = context.scene
    fp = open(path, "w")
    fp.write("Settings\n")
    for prop in ['McpSrcArmBentDown','McpSrcArmRoll','McpSrcLegBentOut','McpSrcLegRoll']:
        fp.write("%s %s\n" % (prop, scn[prop]))
    fp.write("Bones\n")
    for prop in the.sourceProps:
        (mhx1, text, mhx2) = the.sourceEnums[scn[prop]]
        fp.write("%s %s\n" % (prop, mhx1))
    fp.close()
    return
        
def loadSourceBones(context, path):
    scn = context.scene
    the.sourceEnums = defaultEnums()
    the.sourceProps = []
    fp = open(path, "rU")
    status = 0
    for line in fp:
        words = line.split()
        if len(words) == 1:

            status = words[0]
        elif status == 'Settings':
            prop = words[0]
            value = float(words[1])
            scn[prop] = value
        elif status == 'Bones':
            prop = words[0]
            the.sourceProps.append(prop)
            mhx = words[1]
            setSourceProp(scn, prop, mhx, the.sourceEnums)
            print(prop, scn[prop], mhx)
    fp.close()
    
    for prop in the.sourceProps:
        defineSourceProp(prop[2:], the.sourceEnums)
    return
        
class VIEW3D_OT_McpLoadSaveSourceBonesButton(bpy.types.Operator, ImportHelper):
    bl_idname = "mcp.load_save_source_bones"
    bl_label = "Load/save source bones"

    loadSave = bpy.props.StringProperty()
    filename_ext = ".txt"
    #filter_glob = StringProperty(default="*.txt", options={'HIDDEN'})
    filepath = StringProperty(name="File Path", maxlen=1024, default="")

    def execute(self, context):
        ensureSourceInited(context)
        if self.loadSave == 'save':
            saveSourceBones(context, self.properties.filepath)
        else:
            loadSourceBones(context, self.properties.filepath)
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    
