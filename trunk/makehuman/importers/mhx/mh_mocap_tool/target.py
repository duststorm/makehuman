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



import bpy, os, mathutils, math, time
from math import sin, cos, pi, atan
from mathutils import *
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

from . import utils, rig_mhx, rig_game, rig_rorkimaru
from . import globvar as the

Deg2Rad = math.pi/180

T_MHX = 1
T_Rorkimaru = 2
T_Game = 3
T_Custom = 4

#
#   getTrgBone(b):
#

def getTrgBone(b):
    if the.target == T_MHX:
        return b
    else:
        try:
            return the.trgBone[b]
        except:
            return None

#
#   getSrcBone(b):
#

def getSrcBone(b):
    if the.target == T_MHX:
        return b
    else:
        try:
            return the.srcBone[b]
        except:
            return None            
            
#
#   getParentName(b):
#

def getParentName(b):
    if b == None:
        return None
    elif the.target == T_MHX:
        if b == 'MasterFloor':
            return None
        else:
            return b
    elif the.target == T_Rorkimaru:
        try:
            return rig_rorkimaru.Names[b]
        except:
            return b
    elif the.target == T_Game:
        try:
            return rig_game.Names[b]
        except:
            return b
    else:
        return b

#
#   guessTargetArmature(trgRig, scn):
#

def guessTargetArmature(trgRig, scn):
    bones = trgRig.data.bones.keys()
    try:
        custom = trgRig['McpTargetRig']
    except:
        custom = False
    if custom:
        the.target = T_Custom
        name = "Custom %s" % trgRig.name
    elif 'KneePT_L' in bones:
        the.target = T_MHX
        name = "MHX"
    elif testTargetRig(bones, rig_game.Bones):
        the.target = T_Game
        name = "Game"
    elif testTargetRig(bones, rig_rorkimaru.Bones):
        the.target = T_Rorkimaru
        name = "Rorkimaru"
    else:
        print("Bones", bones)
        raise NameError("Did not recognize target armature %s" % trgRig)

    print("Target armature %s" % name)
    the.parents = {}
    the.targetRolls = {}
    the.targetMats = {}

    if the.target == T_MHX:
        the.fkBoneList = rig_mhx.FkBoneList
        the.IkBoneList = rig_mhx.IkBoneList
        the.GlobalBoneList = rig_mhx.GlobalBoneList
        the.IkParents = rig_mhx.IkParents
        for bone in trgRig.data.bones:
            """
            try:
                roll = bone['Roll']
            except:
                roll = 0
            """
            roll = utils.getRoll(bone)
            if abs(roll) > 0.1:
                the.targetRolls[bone.name] = roll
    else:
        the.fkBoneList = []
        the.GlobalBoneList = []

        the.trgBone = {}
        the.srcBone = {}
        if the.target == T_Custom:
            (bones, ikBones, the.parents, the.targetRolls, the.targetMats, the.IkBoneList, the.IkParents) = makeTargetAssoc(trgRig, scn)
        elif the.target == T_Rorkimaru:
            bones = rig_rorkimaru.Bones
            the.IkBoneList = rig_game.IkBoneList
            the.IkParents = rig_game.IkParents
        elif the.target == T_Game:
            bones = rig_game.Bones
            the.IkBoneList = rig_game.IkBoneList
            the.IkParents = rig_game.IkParents
        else:
            raise NameError("Unknown target %s" % the.target)
        for (trg,src) in bones:
            the.fkBoneList.append(trg)
            the.srcBone[trg] = src
            the.trgBone[src] = trg
            if src in rig_mhx.GlobalBoneList:
                the.GlobalBoneList.append(trg)
    return


def testTargetRig(bones, rigBones):
    for (b, mb) in rigBones:
        if b not in bones:
            print("Fail", b, mb)
            return False
    return True

###############################################################################
#
#    Target armatures
#
###############################################################################

#    (mhx bone, text)

TargetBoneNames = [
    ('Root',        'Root bone'),
    ('Spine1',        'Lower spine'),
    ('Spine2',        'Middle spine'),
    ('Spine3',        'Upper spine'),
    ('Neck',        'Neck'),
    ('Head',        'Head'),
    None,
    ('Clavicle_L',    'L clavicle'),
    ('UpArm_L',        'L upper arm'),
    ('LoArm_L',        'L forearm'),
    ('Hand_L',        'L hand'),
    None,
    ('Clavicle_R',    'R clavicle'),
    ('UpArm_R',        'R upper arm'),
    ('LoArm_R',        'R forearm'),
    ('Hand_R',        'R hand'),
    None,
    ('Hips',        'Hips'),
    None,
    ('Hip_L',        'L hip'),
    ('UpLeg_L',        'L thigh'),
    ('LoLeg_L',        'L shin'),
    ('Foot_L',        'L foot'),
    ('Toe_L',        'L toes'),
    None,
    ('Hip_R',        'R hip'),
    ('UpLeg_R',        'R thigh'),
    ('LoLeg_R',        'R shin'),
    ('Foot_R',        'R foot'),
    ('Toe_R',        'R toes'),
]

#    (mhx bone, text, fakeparent, copyRot)

TargetIkBoneNames = [ 
    ('Wrist_L',     'L wrist', 'LoArm_L', 'Hand_L'),
    ('ElbowPT_L',     'L elbow', 'UpArm_L', None),
    ('Ankle_L',     'L ankle', 'LoLeg_L', 'Foot_L'),
    ('KneePT_L',     'L knee', 'UpLeg_L', None),

    ('Wrist_R',     'R wrist', 'LoArm_R', 'Hand_R'),
    ('ElbowPT_R',     'R elbow', 'UpArm_R', None),
    ('Ankle_R',        'R ankle', 'LoLeg_R', 'Foot_R'),
    ('KneePT_R',     'R knee', 'UpLeg_R', None),
]

#
#    initTargetCharacter(rig):
#    class VIEW3D_OT_McpInitTargetCharacterButton(bpy.types.Operator):
#    class VIEW3D_OT_McpUnInitTargetCharacterButton(bpy.types.Operator):
#

def initTargetCharacter(rig):
    for bn in TargetBoneNames+TargetIkBoneNames:
        if not bn:
            continue
        try:
            (mhx, text) = bn
        except:
            (mhx, text, fakepar, copyrot) = bn
        rig[mhx] = mhx
    rig['McpTargetRig'] = True
    rig['McpArmBentDown'] = 0.0
    rig['McpLegBentOut'] = 0.0
    return
    
class VIEW3D_OT_McpInitTargetCharacterButton(bpy.types.Operator):
    bl_idname = "mcp.init_target_character"
    bl_label = "Initialize target character"
    bl_options = {'REGISTER'}

    def execute(self, context):
        initTargetCharacter(context.object)
        print("Target character initialized")
        return{'FINISHED'}    

class VIEW3D_OT_McpUnInitTargetCharacterButton(bpy.types.Operator):
    bl_idname = "mcp.uninit_target_character"
    bl_label = "Uninitialize"
    bl_options = {'REGISTER'}

    def execute(self, context):
        context.object['McpTargetRig'] = False
        print("Target character uninitialized")
        return{'FINISHED'}    

#
#    assocTargetBones(rig,, names, xtraAssoc):
#

def assocTargetBones(rig, names, xtraAssoc):
    boneAssoc = []
    for bn in names:
        if not bn:
            continue
        try:
            (mhx, text) = bn
        except:
            (mhx, text, fakePar, copyRot) = bn
        bone = rig[mhx]
        if bone != '':
            try:
                rig.data.bones[bone]
                exists = True
            except:
                exists = False
            if exists:
                boneAssoc.append((bone, mhx))
            else:
                raise NameError("Bone %s does not exist in armature %s" % (bone, rig.name))

    parAssoc = {}
    assoc = boneAssoc+xtraAssoc
    for (bname, mhx) in boneAssoc:
        bone = rig.data.bones[bname] 
        (par, stop) = realBone(bone.parent, rig, 0, assoc)
        while not stop:
            (par, stop) = realBone(par.parent, rig, 0, assoc)
        if par:
            parAssoc[bname] = par.name
        else:
            parAssoc[bname] = None

    rolls = {}
    for (bname, mhx) in boneAssoc:
        rolls[bname] = utils.getRoll(rig.data.bones[bname])

    """
    try:
        bpy.ops.object.mode_set(mode='EDIT')    
        (bname, mhx) = boneAssoc[0]
        rig.data.edit_bones[bname]
        edit = True
    except:
        edit = False
    if edit:
        for (bname, mhx) in boneAssoc:
            eb = rig.data.edit_bones[bname]
            rolls[bname] = eb.roll
        bpy.ops.object.mode_set(mode='POSE')    
        for (bname, mhx) in boneAssoc:
            bone = rig.data.bones[bname]
            bone['Roll'] = rolls[bname]
    else:
        for (bname, mhx) in boneAssoc:
            bone = rig.data.bones[bname]
            try:
                rolls[bname] = bone['Roll']
            except:
                raise NameError("Associations must be made in rig source file")
    """

    pb = rig.pose.bones[rig['Root']]
    pb.lock_location = (False,False,False)

    return (boneAssoc, parAssoc, rolls)

#
#    findFakeParent(mhx, boneAssoc):
#

def findFakeParent(mhx, boneAssoc):
    for (mhx1, text, fakeMhx, copyMhx) in TargetIkBoneNames:
        if mhx == mhx1:
            fakePar = assocKey(fakeMhx, boneAssoc)
            copyRot = assocKey(copyMhx, boneAssoc)
            return (fakePar, copyRot)
    raise NameError("Did not find fake parent %s" % mhx)

#
#    makeTargetAssoc(rig, scn):
#

def makeTargetAssoc(rig, scn):
    scn.objects.active = rig    
    (boneAssoc, parAssoc, rolls) = assocTargetBones(rig, TargetBoneNames, [])
    (ikBoneAssoc, ikParAssoc, ikRolls) = assocTargetBones(rig, TargetIkBoneNames, boneAssoc)

    ikBones = []
    ikParents = {}
    for (bone, mhx) in ikBoneAssoc:
        ikBones.append(bone)
        (fakePar, copyRot) = findFakeParent(mhx, boneAssoc)
        # bone : (realParent, fakeParent, copyRot, reverse)
        par = ikParAssoc[bone]
        ikParents[bone] = (par, fakePar, copyRot, False)
        parAssoc[bone] = par

    fixMats = createCustomFixes(rig['McpLegBentOut'], 0, rig['McpArmBentDown'], 0)

    print("Associations:")    
    print("            Bone :       Mhx bone         Parent  Roll")
    for (bname, mhx) in boneAssoc:
        roll = rolls[bname]
        print("  %14s : %14s %14s %5d" % (bname, mhx, parAssoc[bname], roll/Deg2Rad))
    print("IK bones:")
    print("            Bone :       Mhx bone    Real parent    Fake parent       Copy rot")
    for (bname, mhx) in ikBoneAssoc:
        (par, fakePar, copyRot, reverse) = ikParents[bname]
        print("  %14s : %14s %14s %14s %14s" % (bname, mhx, par, fakePar, copyRot))
    return (boneAssoc, ikBoneAssoc, parAssoc, rolls, fixMats, ikBones, ikParents)


#
#    createCustomFixes(bendLeg, rollLeg, bendArm, rollArm):
#

def createCustomFixes(bendLeg, rollLeg, bendArm, rollArm):
    fixMats = {}
    eps = 4
    if abs(bendLeg) > eps or abs(rollLeg) > eps:        
        bendLeg *= Deg2Rad
        fixMats['UpLeg_L'] = (Matrix.Rotation(-bendLeg, 3, 'Z'), rollLeg*Deg2Rad)
        fixMats['UpLeg_R'] = (Matrix.Rotation(bendLeg, 3, 'Z'), -rollLeg*Deg2Rad)
        if abs(rollLeg) > eps:
            rollLeg *= Deg2Rad
            fixMats['LoLeg_L'] = (None, rollLeg)
            fixMats['LoLeg_R'] = (None, -rollLeg)
        
    if abs(bendArm) > eps or abs(rollArm) > eps:        
        bendArm *= Deg2Rad
        fixMats['UpArm_L'] = (Matrix.Rotation(bendArm, 3, 'Z'), rollArm*Deg2Rad)
        fixMats['UpArm_R'] = (Matrix.Rotation(-bendArm, 3, 'Z'), -rollArm*Deg2Rad)
        if abs(rollArm) > eps:
            rollArm *= Deg2Rad
            fixMats['LoArm_L'] = (None, rollArm)
            fixMats['Hand_L'] = (None, rollArm)
            fixMats['LoArm_R'] = (None, -rollArm)
            fixMats['Hand_R'] = (None, -rollArm)        
    return fixMats

#
#    assocValue(name, assoc):
#    assocKey(name, assoc):
#
    
def assocValue(name, assoc):
    for (key, value) in assoc:
        if key == name:
            return value
    return None

def assocKey(name, assoc):
    for (key, value) in assoc:
        if value == name:
            return key
    return None

#
#    realBone(bone, rig, n, assoc):
#

def realBone(bone, rig, n, assoc):
    if not bone:
        return (None, True)
    if assocValue(bone.name, assoc):
        return (bone, True)
    if n > 5:
        print("Real bone overflow:", bone)
        return (bone, True)

    pb = rig.pose.bones[bone.name]
    for cns in pb.constraints:
        if (((cns.type == 'COPY_ROTATION' and cns.use_x and cns.use_z) or
             (cns.type == 'COPY_TRANSFORMS')) and
            (cns.influence > 0.6) and
            (cns.target == rig)):
            rb = rig.data.bones[cns.subtarget]
            return realBone(rb, rig, n+1, assoc)
    return (bone, False)

class VIEW3D_OT_McpMakeTargetAssocButton(bpy.types.Operator):
    bl_idname = "mcp.make_assoc"
    bl_label = "Make target associations"
    bl_options = {'REGISTER'}

    def execute(self, context):
        makeTargetAssoc(context.object, context.scene)
        print("Associations made")
        return{'FINISHED'}    

#
#
#

def unrollAll(context):
    bpy.ops.object.mode_set(mode='EDIT')
    ebones = context.object.data.edit_bones
    for eb in ebones:
        eb.roll = 0
    bpy.ops.object.mode_set(mode='POSE')
    return

class VIEW3D_OT_McpUnrollAllButton(bpy.types.Operator):
    bl_idname = "mcp.unroll_all"
    bl_label = "Unroll all"
    bl_options = {'REGISTER'}

    def execute(self, context):
        unrollAll(context)
        print("Associations made")
        return{'FINISHED'}    

#
#    saveTargetBones(context, path):
#    loadTargetBones(context, path):
#    class VIEW3D_OT_McpLoadSaveTargetBonesButton(bpy.types.Operator, ImportHelper):
#

def saveTargetBones(context, path):
    rig = context.object
    fp = open(path, "w")
    for bn in TargetBoneNames+TargetIkBoneNames:
        if not bn:
            continue
        try:
            (mhx, text) = bn
        except:
            (mhx, text, fakepar, copyrot) = bn
        bone = rig[mhx]
        if bone == '':
            fp.write("%s %s\n" % (mhx, '-'))
        else:
            fp.write("%s %s\n" % (mhx, bone))
    fp.close()
    return
        
def loadTargetBones(context, path):
    rig = context.object
    fp = open(path, "rU")
    for line in fp:
        words = line.split()
        try:
            mhx = words[0]
            bone = words[1]
        except:
            mhx = None
        if mhx:
            if bone == '-':
                bone = ''
            rig[mhx] = bone
    fp.close()
    return
        
class VIEW3D_OT_McpLoadSaveTargetBonesButton(bpy.types.Operator, ImportHelper):
    bl_idname = "mcp.load_save_target_bones"
    bl_label = "Load/save target bones"

    loadSave = bpy.props.StringProperty()
    filename_ext = ".trg"
    filter_glob = StringProperty(default="*.trg", options={'HIDDEN'})
    filepath = StringProperty(name="File Path", maxlen=1024, default="")

    def execute(self, context):
        if self.loadSave == 'save':
            saveTargetBones(context, self.properties.filepath)
        else:
            loadTargetBones(context, self.properties.filepath)
        return{'FINISHED'}    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    

#        
#    class MhxTargetBonesPanel(bpy.types.Panel):
#

class MhxTargetBonesPanel(bpy.types.Panel):
    bl_label = "Mocap: Target armature"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'ARMATURE')

    def draw(self, context):
        layout = self.layout
        rig = context.object
        try:
            inited = rig['McpTargetRig']
        except:
            inited = False

        if not inited:
            layout.operator("mcp.init_target_character", text='Initialize target character')
            return

        layout.operator("mcp.init_target_character", text='Reinitialize target character')        
        layout.operator("mcp.uninit_target_character")        
        layout.operator("mcp.load_save_target_bones", text='Load target bones').loadSave = 'load'        
        layout.operator("mcp.load_save_target_bones", text='Save target bones').loadSave = 'save'        
        layout.operator("mcp.make_assoc")        
        layout.operator("mcp.unroll_all")        
        #layout.prop(rig, '["McpArmBentDown"]', text='Arm bent down')
        #layout.prop(rig, '["McpLegBentOut"]', text='Leg bent out')

        layout.label("FK bones")
        for bn in TargetBoneNames:
            if bn:
                (mhx, text) = bn
                layout.prop(rig, '["%s"]' % mhx, text=text)
            else:
                layout.separator()
        layout.label("IK bones")
        for (mhx, text, fakePar, copyRot) in TargetIkBoneNames:
            layout.prop(rig, '["%s"]' % mhx, text=text)
        return

