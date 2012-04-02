# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the. terms of the. GNU General Public License
#  as published by the. Free Software Foundation; eithe.r version 2
#  of the. License, or (at your option) any later version.
#
#  This program is distributed in the. hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the. implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the.
#  GNU General Public License for more details.
#
#  You should have received a copy of the. GNU General Public License
#  along with this program; if not, write to the. Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Project Name:        MakeHuman
# Product Home Page:   http://www.makehuman.org/
# Code Home Page:      http://code.google.com/p/makehuman/
# Authors:             Thomas Larsson
# Script copyright (C) MakeHuman Team 2001-2011
# Coding Standards:    See http://sites.google.com/site/makehumandocs/developers-guide



import bpy, os, mathutils, math, time
from math import sin, cos
from mathutils import *
from bpy_extras.io_utils import ImportHelper
from bpy.props import *

from . import utils, props, target, source
from . import globvar as the

###################################################################################
#    BVH importer. 
#    The importer that comes with Blender had memory leaks which led to instability.
#    It also creates a weird skeleton from CMU data, with hands the.at start at the. wrist
#    and ends at the elbow.
#

#
#    class CNode:
#

class CNode:
    def __init__(self, words, parent):
        name = words[1]
        for word in words[2:]:
            name += ' '+word
        
        self.name = name
        self.parent = parent
        self.children = []
        self.head = Vector((0,0,0))
        self.offset = Vector((0,0,0))
        if parent:
            parent.children.append(self)
        self.channels = []
        self.matrix = None
        self.inverse = None
        return

    def __repr__(self):
        return "CNode %s" % (self.name)

    def display(self, pad):
        vec = self.offset
        if vec.length < Epsilon:
            c = '*'
        else:
            c = ' '
        print("%s%s%10s (%8.3f %8.3f %8.3f)" % (c, pad, self.name, vec[0], vec[1], vec[2]))
        for child in self.children:
            child.display(pad+"  ")
        return

    def build(self, amt, orig, parent):
        self.head = orig + self.offset
        if not self.children:
            return self.head
        
        zero = (self.offset.length < Epsilon)
        eb = amt.edit_bones.new(self.name)        
        if parent:
            eb.parent = parent
        eb.head = self.head
        tails = Vector((0,0,0))
        for child in self.children:
            tails += child.build(amt, self.head, eb)
        n = len(self.children)
        eb.tail = tails/n
        #self.matrix = eb.matrix.rotation_part()
        (loc, rot, scale) = eb.matrix.decompose()
        self.matrix = rot.to_matrix()
        self.inverse = self.matrix.copy()
        self.inverse.invert()        
        if zero:
            return eb.tail
        else:        
            return eb.head

#
#    readBvhFile(context, filepath, scn, scan):
#    Custom importer
#

Location = 1
Rotation = 2
Hierarchy = 1
Motion = 2
Frames = 3

Deg2Rad = math.pi/180
Epsilon = 1e-5

def readBvhFile(context, filepath, scn, scan):
    props.ensureInited(context)
    scale = scn.McpBvhScale
    startFrame = scn.McpStartFrame
    endFrame = scn.McpEndFrame
    rot90 = scn.McpRot90Anim
    if (scn.McpSubsample):
        ssFactor = scn.McpSSFactor
    else:
        ssFactor = 1
    defaultSS = scn.McpDefaultSS

    fileName = os.path.realpath(os.path.expanduser(filepath))
    (shortName, ext) = os.path.splitext(fileName)
    if ext.lower() != ".bvh":
        raise NameError("Not a bvh file: " + fileName)
    print( "Loading BVH file "+ fileName )

    trgRig = context.object
    bpy.ops.object.mode_set(mode='POSE')
    trgPbones = trgRig.pose.bones

    time1 = time.clock()
    level = 0
    nErrors = 0
    scn = context.scene
            
    fp = open(fileName, "rU")
    print( "Reading skeleton" )
    lineNo = 0
    for line in fp: 
        words= line.split()
        lineNo += 1
        if len(words) == 0:
            continue
        key = words[0].upper()
        if key == 'HIERARCHY':
            status = Hierarchy
        elif key == 'MOTION':
            if level != 0:
                raise NameError("Tokenizer out of kilter %d" % level)    
            if scan:
                return root
            amt = bpy.data.armatures.new("BvhAmt")
            rig = bpy.data.objects.new("BvhRig", amt)
            scn.objects.link(rig)
            scn.objects.active = rig
            scn.update()
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.mode_set(mode='EDIT')
            root.build(amt, Vector((0,0,0)), None)
            #root.display('')
            bpy.ops.object.mode_set(mode='OBJECT')
            status = Motion
            print("Reading motion")
        elif status == Hierarchy:
            if key == 'ROOT':    
                node = CNode(words, None)
                root = node
                nodes = [root]
            elif key == 'JOINT':
                node = CNode(words, node)
                nodes.append(node)
            elif key == 'OFFSET':
                (x,y,z) = (float(words[1]), float(words[2]), float(words[3]))
                if rot90:                    
                    node.offset = scale*Vector((x,-z,y))
                else:
                    node.offset = scale*Vector((x,y,z))
            elif key == 'END':
                node = CNode(words, node)
            elif key == 'CHANNELS':
                oldmode = None
                for word in words[2:]:
                    if rot90:
                        (index, mode, sign) = channelZup(word)
                    else:
                        (index, mode, sign) = channelYup(word)
                    if mode != oldmode:
                        indices = []
                        node.channels.append((mode, indices))
                        oldmode = mode
                    indices.append((index, sign))
            elif key == '{':
                level += 1
            elif key == '}':
                level -= 1
                node = node.parent
            else:
                raise NameError("Did not expect %s" % words[0])
        elif status == Motion:
            if key == 'FRAMES:':
                nFrames = int(words[1])
            elif key == 'FRAME' and words[1].upper() == 'TIME:':
                frameTime = float(words[2])
                frameFactor = int(1.0/(25*frameTime) + 0.49)
                if defaultSS:
                    ssFactor = frameFactor
                status = Frames
                frame = 0
                frameno = 1

                #source.findSrcArmature(context, rig)
                bpy.ops.object.mode_set(mode='POSE')
                pbones = rig.pose.bones
                for pb in pbones:
                    #try:
                    #    trgName = the.armature[pb.name.lower()]
                    #    pb.rotation_mode = trgPbones[trgName].rotation_mode
                    #except:
                    pb.rotation_mode = 'QUATERNION'
        elif status == Frames:
            if (frame >= startFrame and
                frame <= endFrame and
                frame % ssFactor == 0):
                addFrame(words, frameno, nodes, pbones, scale)
                if frameno % 200 == 0:
                    print(frame)
                frameno += 1
            frame += 1

    fp.close()
    utils.setInterpolation(rig)
    time2 = time.clock()
    print("Bvh file %s loaded in %.3f s" % (filepath, time2-time1))
    renameBvhRig(rig, filepath)
    return (rig, trgRig)

#
#    addFrame(words, frame, nodes, pbones, scale):
#

def addFrame(words, frame, nodes, pbones, scale):
    m = 0
    first = True
    for node in nodes:
        name = node.name
        try:
            pb = pbones[name]
        except:
            pb = None
        if pb:
            for (mode, indices) in node.channels:
                if mode == Location:
                    vec = Vector((0,0,0))
                    for (index, sign) in indices:
                        vec[index] = sign*float(words[m])
                        m += 1
                    if first:
                        pb.location = node.inverse * (scale * vec - node.head)
                        for n in range(3):
                            pb.keyframe_insert('location', index=n, frame=frame, group=name)
                    first = False
                elif mode == Rotation:
                    mats = []
                    for (axis, sign) in indices:
                        angle = sign*float(words[m])*Deg2Rad
                        mats.append(Matrix.Rotation(angle, 3, axis))
                        m += 1
                    mat = node.inverse * mats[0] * mats[1] * mats[2] * node.matrix
                    utils.setRotation(pb, mat, frame, name)

    return

#
#    channelYup(word):
#    channelZup(word):
#

def channelYup(word):
    if word == 'Xrotation':
        return ('X', Rotation, +1)
    elif word == 'Yrotation':
        return ('Y', Rotation, +1)
    elif word == 'Zrotation':
        return ('Z', Rotation, +1)
    elif word == 'Xposition':
        return (0, Location, +1)
    elif word == 'Yposition':
        return (1, Location, +1)
    elif word == 'Zposition':
        return (2, Location, +1)

def channelZup(word):
    if word == 'Xrotation':
        return ('X', Rotation, +1)
    elif word == 'Yrotation':
        return ('Z', Rotation, +1)
    elif word == 'Zrotation':
        return ('Y', Rotation, -1)
    elif word == 'Xposition':
        return (0, Location, +1)
    elif word == 'Yposition':
        return (2, Location, +1)
    elif word == 'Zposition':
        return (1, Location, -1)

#
#   end BVH importer
#
###################################################################################


###################################################################################

#            
#    class CEditBone():
#

class CEditBone():
    def __init__(self, bone):
        self.name = bone.name
        self.head = bone.head.copy()
        self.tail = bone.tail.copy()
        self.roll = bone.roll
        if bone.parent:
            self.parent = target.getParentName(bone.parent.name)
        else:
            self.parent = None
        if self.parent:
            self.use_connect = bone.use_connect
        else:
            self.use_connect = False
        #self.matrix = bone.matrix.copy().rotation_part()
        (loc, rot, scale) = bone.matrix.decompose()
        self.matrix = rot.to_matrix()
        self.inverse = self.matrix.copy()
        self.inverse.invert()

    def __repr__(self):
        return ("%s p %s\n  h %s\n  t %s\n" % (self.name, self.parent, self.head, self.tail))

#
#    renameBones(srcRig, scn):
#

def renameBones(srcRig, scn):
    srcBones = []
    trgBones = {}

    scn.objects.active = srcRig
    scn.update()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='EDIT')
    print("Ren", bpy.context.object, srcRig.mode)
    ebones = srcRig.data.edit_bones
    for bone in ebones:
        srcBones.append( CEditBone(bone) )
    
    setbones = []
    action = srcRig.animation_data.action
    for srcBone in srcBones:
        srcName = srcBone.name
        lname = srcName.lower()
        try:
            trgName = the.armature[lname]
        except:
            trgName = the.armature[lname.replace(' ','_')]
        eb = ebones[srcName]
        if trgName:
            eb.name = trgName
            trgBones[trgName] = CEditBone(eb)
            grp = action.groups[srcName]
            grp.name = trgName

            setbones.append((eb, trgName))
        else:
            eb.name = '_' + srcName

    for (eb, name) in setbones:
        eb.name = name
    #createExtraBones(ebones, trgBones)
    bpy.ops.object.mode_set(mode='POSE')
    return

#
#    createExtraBones(ebones, trgBones):
#

def createExtraBones(ebones, trgBones):
    for suffix in ['_L', '_R']:
        try:
            foot = ebones['Foot'+suffix]
        except:
            foot = None
        try:
            toe = ebones['Toe'+suffix]
        except:
            toe = None

        if not toe:
            nameSrc = 'Toe'+suffix
            toe = ebones.new(name=nameSrc)
            toe.head = foot.tail
            toe.tail = toe.head - Vector((0, 0.5*foot.length, 0))
            toe.parent = foot
            trgBones[nameSrc] = CEditBone(toe)
            
        nameSrc = 'Leg'+suffix
        eb = ebones.new(name=nameSrc)
        eb.head = 2*toe.head - toe.tail
        eb.tail = 4*toe.head - 3*toe.tail
        eb.parent = toe
        trgBones[nameSrc] = CEditBone(eb)

        nameSrc = 'Ankle'+suffix
        eb = ebones.new(name=nameSrc)
        eb.head = foot.head
        eb.tail = 2*foot.head - foot.tail
        eb.parent = ebones['LoLeg'+suffix]
        trgBones[nameSrc] = CEditBone(eb)
    return

#
#    renameBvhRig(srcRig, filepath):
#

def renameBvhRig(srcRig, filepath):
    base = os.path.basename(filepath)
    (filename, ext) = os.path.splitext(base)
    print("File", filename, len(filename))
    if len(filename) > 12:
        words = filename.split('_')
        if len(words) == 1:
            words = filename.split('-')
        name = 'Y_'
        if len(words) > 1:
            words = words[1:]
        for word in words:
            name += word
    else:
        name = 'Y_' + filename
    print("Name", name)

    srcRig.name = name
    action = srcRig.animation_data.action
    action.name = name
    return 
    
#
#    deleteSourceRig(context, rig, prefix):
#

def deleteSourceRig(context, rig, prefix):
    ob = context.object
    scn = context.scene
    scn.objects.active = rig
    bpy.ops.object.mode_set(mode='OBJECT')
    scn.objects.active = ob    
    scn.objects.unlink(rig)
    if rig.users == 0:
        bpy.data.objects.remove(rig)
    if bpy.data.actions:
        for act in bpy.data.actions:
            if act.name[0:2] == prefix:
                act.use_fake_user = False
                if act.users == 0:
                    bpy.data.actions.remove(act)
                    del act
    return
    

#
#    copyAnglesIK():
#
"""
def copyAnglesIK(context):
    trgRig = context.object
    target.guessTargetArmature(trgRig. context.scene)
    trgAnimations = createTargetAnimation(context, trgRig)
    insertAnimation(context, trgRig, trgAnimations, the.fkBoneList)
    onoff = toggleLimitConstraints(trgRig)
    setLimitConstraints(trgRig, 0.0)
    poseTrgIkBones(context, trgRig, trgAnimations)
    utils.setInterpolation(trgRig)
    if onoff == 'OFF':
        setLimitConstraints(trgRig, 1.0)
    else:
        setLimitConstraints(trgRig, 0.0)
    return
"""    
#
#    rescaleRig(scn, trgRig, srcRig):
#

def rescaleRig(scn, trgRig, srcRig):
    if not scn.McpAutoScale:
        return
    upleg = target.getTrgBone('UpLeg_L')
    trgScale = trgRig.data.bones[upleg].length
    srcScale = srcRig.data.bones['UpLeg_L'].length
    scale = trgScale/srcScale
    print("Rescale %s with factor %f" % (scn.objects.active, scale))
    scn.McpBvhScale = scale
    
    bpy.ops.object.mode_set(mode='EDIT')
    ebones = srcRig.data.edit_bones
    for eb in ebones:
        oldlen = eb.length
        eb.head *= scale
        eb.tail *= scale
    bpy.ops.object.mode_set(mode='POSE')
    action = srcRig.animation_data.action
    for fcu in action.fcurves:
        words = fcu.data_path.split('.')
        if words[-1] == 'location':
            for kp in fcu.keyframe_points:
                kp.co[1] *= scale
    return


#
#    renameAndRescaleBvh(context, srcRig, trgRig):
#

def renameAndRescaleBvh(context, srcRig, trgRig):
    try:
        if srcRig["McpRenamed"]:
            print("%s already renamed and rescaled." % srcRig.name)
            return
    except:
        pass
        
    scn = context.scene
    scn.objects.active = srcRig
    scn.update()
    #(srcRig, srcBones, action) =  renameBvhRig(rig, filepath)
    target.guessTargetArmature(trgRig, scn)
    source.findSrcArmature(context, srcRig)
    renameBones(srcRig, scn)
    utils.setInterpolation(srcRig)
    rescaleRig(context.scene, trgRig, srcRig)
    srcRig["McpRenamed"] = True
    return 

########################################################################
#
#   class VIEW3D_OT_LoadBvhButton(bpy.types.Operator, ImportHelper):
#

class VIEW3D_OT_LoadBvhButton(bpy.types.Operator, ImportHelper):
    bl_idname = "mcp.load_bvh"
    bl_label = "Load BVH file (.bvh)"

    filename_ext = ".bvh"
    filter_glob = StringProperty(default="*.bvh", options={'HIDDEN'})
    filepath = StringProperty(name="File Path", description="Filepath used for importing the BVH file", maxlen=1024, default="")

    def execute(self, context):
        readBvhFile(context, self.properties.filepath, context.scene, False)        
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    

#
#   class VIEW3D_OT_RenameBvhButton(bpy.types.Operator):
#

class VIEW3D_OT_RenameBvhButton(bpy.types.Operator):
    bl_idname = "mcp.rename_bvh"
    bl_label = "Rename and rescale BVH rig"

    def execute(self, context):
        scn = context.scene
        srcRig = context.object
        trgRig = None
        for ob in scn.objects:
            if ob.type == 'ARMATURE' and ob.select and ob != srcRig:
                trgRig = ob
                break
        if not trgRig:
            print("No target rig selected")
            return
        renameAndRescaleBvh(context, srcRig, trgRig)
        if scn.McpRescale:
            simplify.rescaleFCurves(context, srcRig, scn.McpRescaleFactor)
        print("%s renamed" % srcRig.name)
        return{'FINISHED'}    

#
#   class VIEW3D_OT_LoadAndRenameBvhButton(bpy.types.Operator, ImportHelper):
#

class VIEW3D_OT_LoadAndRenameBvhButton(bpy.types.Operator, ImportHelper):
    bl_idname = "mcp.load_and_rename_bvh"
    bl_label = "Load and rename BVH file (.bvh)"

    filename_ext = ".bvh"
    filter_glob = StringProperty(default="*.bvh", options={'HIDDEN'})
    filepath = StringProperty(name="File Path", description="Filepath used for importing the BVH file", maxlen=1024, default="")

    def execute(self, context):
        (srcRig, trgRig) = readBvhFile(context, self.properties.filepath, context.scene, False)        
        renameAndRescaleBvh(context, srcRig, trgRig)
        if context.scene.McpRescale:
            simplify.rescaleFCurves(context, srcRig, scn.McpRescaleFactor)
        print("%s loaded and renamed" % srcRig.name)
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    
