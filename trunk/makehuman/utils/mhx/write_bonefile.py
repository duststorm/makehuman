""" 
**Project Name:**     MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:** http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**     MakeHuman Team 2001-2013

**Licensing:**       AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------
Utility for making rig creation files

"""
#
#   Utility for creating MakeHuman bone definitions.
#

import bpy, os
from bpy.props import *

BoneLayers = [
    'L_FK', 'L_TORSO', 'L_ARMIK', 'L_ARMFK',
    'L_LEGIK', 'L_LEGFK', 'L_HANDIK', 'L_HANDFK', 
    'L_PANEL', 'L_TOE', 'L_HEAD', 'L_NONE',
    'L_NONE', 'L_ROOT', 'L_DEFORM', 'L_HELP'
]

#
#   writeBones(character, scale, fp):
#

def writeBones(character, scale, fp):
    amt = None
    me = None
    for ob in bpy.context.scene.objects:
        if ob.select:
            if ob.type == 'ARMATURE':
                if amt:
                    raise NameError("Two armatures selected")
                rig = ob
                amt = rig.data
            elif ob.type == 'MESH':
                if me:
                    raise NameError("Two meshes selected")
                me = ob.data
    if amt and me:
        print("Using %s and %s" % (amt, me))
    else:
        raise NameError("Must select one mesh and one armature")
    bpy.context.scene.objects.active = rig

    bpy.ops.object.mode_set(mode='EDIT')
    bones = amt.edit_bones.values()

    # List name of deform bones, to modify vertexgroup names
    """
    fp.write("%sDeform = {\n" % character)
    for b in bones:
        (bType, bName) = extractName(b)
        pad = doPad(len(bName), 4)
        if bType == 'DEF':
            fp.write("\t'%s':%s'%s',\n" % (bName, pad, b.name.replace(' ','_')))
    fp.write("}\n\n")
    """
    
    # List symbolic joint locations
    joints = {}
    fp.write("%sJoints = [\n" % character)
    for b in bones:
        (bType, bName) = extractName(b)
        pad = doPad(len(bName), 6)
        writeJoint(fp, bName+"_head", b.head, pad, joints, me)
        writeJoint(fp, bName+"_tail", b.tail, pad, joints, me)
    fp.write("]\n\n")

    # List symbolic names for heads and tails
    fp.write("%sHeadsTails = [\n" % character)
    for b in bones:
        print("Bone", b.name, b.head, b.tail)
        (bType, bName) = extractName(b)
        pad = doPad(len(bName), 3)
        hfound = findJoint(bName+"_head", None, joints)
        tfound = findJoint(bName+"_tail", None, joints)
        if hfound == None or tfound == None:
            fp.write("Bone %s %s %s" % ( b.name, b.head, b.tail))
            fp.close()
            raise NameError("ht", hfound, tfound)
        (hname,hx) = hfound
        (tname,tx) = tfound
        fp.write("\t('%s',%s'%s', '%s'),\n" % (b.name.replace(' ','_'), pad, hname, tname))
    fp.write("]\n\n")

    # List bone in armature
    # (bone, roll, parent, flags, layers, bbones)
    #
    fp.write("%sArmature = [\n" % character)
    for b in bones:
        pad = doPad(len(b.name), 3)
        fp.write("\t('%s',%s" % (b.name.replace(' ','_'), pad))
        if b.roll < 1e-2 and b.roll > -1e-2:
            fp.write("0.0, ")
        else:
            fp.write("%.3g, " % b.roll)
        if b.parent:
            fp.write("'%s', " % b.parent.name.replace(' ','_'))
        else:
            fp.write("None, ")

        # Flags
        flags = ""
        if b.use_deform:
            flags += "+F_DEF"
        if b.use_connect:
            flags += "+F_CON"
        #if b.draw_wire:
        #    flags += "+F_WIR"
        if b.hide_select:
            flags += "+F_RES"
        if not b.use_inherit_scale:
            flags += "+F_NOSCALE"
        if not b.use_inherit_rotation:
            flags += "+F_NOROT"
        if not b.use_local_location:
            flags += "+F_GLOC"
        if b.lock:
            flags += "+F_LOCK"
        if b.hide:
            flags += "+F_HID"
        if not b.use_cyclic_offset:
            flags += "+F_NOCYC"

        if len(flags) > 0:
            fp.write("%s, " % flags[1:])
        else:
            fp.write("0, ")

        # Layers
        '''
        c = ""
        for n,name in enumerate(BoneLayers):
            if b.layers[n]:
                fp.write("%s%s" % (c, name))
                c = "+"
        if c == "":
            fp.write("0, ")
        else:
            fp.write(", ")      

        '''
        x = 0
        bit = 1
        for lay in b.layers:
            if lay:
                x += bit
            bit <<= 1
        fp.write("0x%x, " % x)

        # BBones
        fp.write("(%d,%d,%d) ),\n" % (b.bbone_in, b.bbone_out, b.bbone_segments))

    fp.write("]\n\n")

    #
    # Posebones
    #
    bpy.ops.object.mode_set(mode='POSE')
    pbones = rig.pose.bones.values()
    fp.write(
"def %sWritePoses(fp):\n" % character +
"\tglobal boneGroups\n" +
"\tboneGroups = {}\n\n")

    # addPoseBone(fp, bone, customShape, boneGroup, pb.lockLoc, pb.lockRot, pb.lockScale, flags, constraints)
    for pb in pbones:
        fp.write("\tmhx_rig.addPoseBone(fp, '%s', " % pb.name.replace(' ','_'))
        if pb.custom_shape:
            fp.write("'%s', " % pb.custom_shape.name.replace(' ','_'))
        else:
            fp.write("None, ")
        if pb.bone_group:
            fp.write("'%s', " % pb.bone_group.name.replace(' ','_'))
        else:
            fp.write("None, ")
        fp.write("(%d,%d,%d), " % (pb.lock_location[0], pb.lock_location[1], pb.lock_location[2]))
        fp.write("(%d,%d,%d), " % (pb.lock_rotation[0], pb.lock_rotation[1], pb.lock_rotation[2]))
        fp.write("(%d,%d,%d), " % (pb.lock_scale[0], pb.lock_scale[1], pb.lock_scale[2]))
        fp.write("(%d,%d,%d), " % (not pb.lock_ik_x, not pb.lock_ik_y, not pb.lock_ik_z))

        # Flags
        flags = ""
        if pb.lock_rotations_4d:
            flags += "+P_LKROT4"
        if pb.lock_rotation_w:
            flags += "+P_LKROTW"
        if pb.use_ik_linear_control:
            flags += "+P_IKLIN"
        if pb.use_ik_rotation_control:
            flags += "+P_IKROT"

        if len(flags) > 0:
            fp.write(flags[1:])
        else:
            fp.write("0")

        if list(pb.constraints):
            c = ",\n\t\t["
            for cns in pb.constraints:
                fp.write(c)
                writeConstraint(fp, cns, scale)
                c = ",\n\t\t "
            fp.write("])\n\n")
        else:
            fp.write(", [])\n\n")
    fp.write("\treturn\n")
    
    #
    #   Properties
    #

    bpy.ops.object.mode_set(mode='OBJECT')
    fp.write("\n%sObjectProps = [" % character)
    print_props(fp, amt)
    fp.write("\n]\n\n%sArmatureProps = [" % character)
    print_props(fp, rig)
    fp.write("]\n\n")

    #
    #   Animation data
    #
    
    bpy.ops.object.mode_set(mode='OBJECT')
    if rig.animation_data == None:
        return
    fp.write("\ndef get%sDrivers():\n\thuman = mh2mhx.theHuman\n\treturn [\n" % character)
    for fcu in rig.animation_data.drivers:
        try:
            drv = fcu.driver
        except:
            pass
        words = fcu.data_path.split('"')
        bone = words[1]
        typ = ("unk", len(words))
        if len(words) == 3:
            typ = words[2].split('.')[1]
            index = fcu.array_index
            if typ == 'rotation_euler':
                typ = 'ROTE'
            elif typ == 'rotation_quaternion':
                typ = 'ROTQ'
            elif typ == 'location':
                typ = 'LOC'
            name = None
        elif len(words) == 5:
            index = -1
            if words[4] == ']':
                typ = "PROP"
                name = words[3]
            elif words[4] == '].influence':
                typ = 'INFL'
                name = words[3]
            
        fp.write("  ('%s', '%s', " % (bone, typ))
        if drv.type == 'SCRIPTED':
            fp.write('("SCRIPTED","%s")' % drv.expression)
        else:
            fp.write("'%s', " % drv.type)
        if name:
            fp.write("'%s', " % name.replace(' ','_'))
        else:
            fp.write("None, ")

        fp.write("%d, " % index)        

        try:
            mod = fcu.modifiers[0]
        except:
            mod = None
        if mod:
            a0 = mod.coefficients[0]
            a1 = mod.coefficients[1]
            fp.write("(%.3g,%.3g), [" % (a0, a1))        
        else:
            fp.write("None, [")
        
        for var in drv.variables:
            fp.write("\n\t\t('%s', '%s', [" % (var.name, var.type))
            for targ in var.targets:
                if targ.use_local_space_transform:
                    flags = 'C_LOCAL'
                else:
                    flags = '0'
                if var.type == 'TRANSFORMS':
                    fp.write("('%s', human, '%s', '%s', %s) " % 
                        (targ.id_type, targ.bone_target, targ.transform_type, flags))
                elif var.type == 'ROTATION_DIFF':
                    fp.write("('%s', human, '%s', %s) " % 
                        (targ.id_type, targ.bone_target, flags))
                elif var.type == 'SINGLE_PROP':
                    fp.write("('%s', human, '%s') " % 
                        (targ.id_type, targ.data_path))
                else:
                    raise NameError("Illegal driver var type %s" % var.type)                    
            fp.write("]),")
        fp.write("]),\n")
    fp.write("]\n\n")

    return

#
#   print_props(fp, rna):
#

def print_props(fp, rna):
    for (key,value) in rna.items():
        if type(value) == float:
            fp.write("\n\t('%s', %.3f)," % (key,value))
        elif type(value) == int:
            fp.write("\n\t('%s', %d)," % (key,value))
        elif type(value) == str:
            fp.write("\n\t('%s', '\"%s\"')," % (key,value))
    return

#
#   findJoint(jName, x, joints):
#   writeJoint(fp, jName, loc, joints, me):
#

def findJoint(jName, x, joints):
    try:
        found = joints[jName]
        return found
    except:
        pass
    if x == None:
        raise NameError("Cannot find joint "+jName)
    for (jy, y) in joints.values():
        if (x-y).length < 1e-3:
            return (jy, y)
    return None

def writeJoint(fp, jName, loc, pad, joints, me):
    found = findJoint(jName, loc, joints)
    if found:
        joints[jName] = found
    else:
        #fp.write("\t('%s',%s'x', [%.6f, %.6f, %.6f]),\n" % (jName, pad, loc[0], loc[1], loc[2]))
        joints[jName] = (jName, loc)
        v = closestVert(loc, me)
        offs = loc - v.co
        fp.write("\t('%s',%s'vo', [%d, %.6f, %.6f, %.6f]),\n" % (jName, pad, v.index, offs[0], offs[1], offs[2]))
    return
    
def closestVert(loc, me):
    mindist = 1e6
    for v in me.vertices:
        offs = loc - v.co
        if offs.length < mindist:
            best = v
            mindist = offs.length
    return best

#
#
#
def addToSpace(cns, cond, flag):
    try:
        res = getattr(cns, cond)
    except:
        res = False
    if res:
        return flag
    else:
        return ""

def writeConstraint(fp, cns, scale):
    typ = cns.type
    name = cns.name.replace(' ','_')
    inf = cns.influence
    print(typ)

    # Owner and target spaces
    space = "0"
    space += addToSpace(cns, "owner_space == 'LOCAL'", '+C_OW_LOCAL') 
    space += addToSpace(cns, "target_space == 'LOCAL'", '+C_TG_LOCAL') 
    space += addToSpace(cns, "active == False", '+C_ACT') 
    space += addToSpace(cns, "expanded == False", '+C_EXP') 
    space += addToSpace(cns, "limit_transform == False", '+C_LTRA') 
    
    if typ == 'IK':
        fp.write("('IK', %s, %.2g, ['%s', '%s', %d, " % (space, inf, name, cns.subtarget, cns.chain_count))
        if cns.pole_target:
            fp.write("(%.3g, '%s'), " % (cns.pole_angle, cns.pole_subtarget))
        else:
            fp.write("None, ")
        fp.write("(%s,%s,%s)])" % (cns.use_location, cns.use_rotation, cns.use_stretch))

    elif typ == 'ACTION':
        fp.write("('Action', %s, %.2g, ['%s', '%s', '%s', '%s', %s, (%.3g, %.3g)])" % 
            (space, inf, name, cns.action.name.replace(' ','_'), cns.subtarget,
            cns.transform_channel, (cns.start_frame, cns.end_frame), cns.minimum, cns.maximum))
            
    elif typ == 'COPY_LOCATION':
        fp.write("('CopyLoc', %s, %.2g, ['%s', '%s', " % 
        (space, inf, name, cns.subtarget))
        fp.write("(%d,%d,%d), " % (cns.use_x, cns.use_y, cns.use_z))
        fp.write("(%d,%d,%d), %.3g, %s])" % (cns.invert_x, cns.invert_y, cns.invert_z, cns.head_tail, cns.use_offset))

    elif typ == 'COPY_ROTATION':
        fp.write("('CopyRot', %s, %.2g, ['%s', '%s', " % (space, inf, name, cns.subtarget))
        fp.write("(%d,%d,%d), " % (cns.use_x, cns.use_y, cns.use_z))
        fp.write("(%d,%d,%d), %s])" % (cns.invert_x, cns.invert_y, cns.invert_z, cns.use_offset))

    elif typ == 'COPY_SCALE':
        fp.write("('CopyScale', %s, %.2g, ['%s', '%s', " % (space, inf, name, cns.subtarget))
        fp.write("(%d,%d,%d), %s])" % (cns.use_x, cns.use_y, cns.use_z, cns.use_offset))

    elif typ == 'COPY_TRANSFORMS':
        fp.write("('CopyTrans', %s, %.2g, ['%s', '%s', %.3g])" % (space, inf, name, cns.subtarget, cns.head_tail))

    elif typ == 'LIMIT_ROTATION':
        fp.write("('LimitRot', %s, %.2g, ['%s', " % (space, inf, name))
        fp.write("(%.3g,%.3g, %.3g,%.3g, %.3g,%.3g), " % 
            (cns.min_x, cns.max_x, cns.min_y, cns.max_y, cns.min_z, cns.max_z))
        fp.write("(%d,%d,%d)])" % (cns.use_limit_x, cns.use_limit_y, cns.use_limit_z))

    elif typ == 'LIMIT_LOCATION':
        fp.write("('LimitLoc', %s, %.2g, ['%s', " % (space, inf, name))
        fp.write("(%.3g,%.3g, %.3g,%.3g, %.3g,%.3g), " %
            (cns.min_x, cns.max_x, cns.min_y, cns.max_y, cns.min_z, cns.max_z))
        fp.write("(%d,%d,%d,%d,%d,%d)])" % 
            (cns.use_min_x, cns.use_max_x, cns.use_min_y, cns.use_max_y, cns.use_min_z, cns.use_max_z))

    elif typ == 'LIMIT_SCALE':
        fp.write("('LimitLoc', %s, %.2g, ['%s', " % (space, inf, name))
        fp.write("(%.3g,%.3g, %.3g,%.3g, %.3g,%.3g), " %
            (cns.min_x, cns.max_x, cns.min_y, cns.max_y, cns.min_z, cns.max_z))
        fp.write("(%d,%d,%d,%d,%d,%d)])" % 
            (cns.use_min_x, cns.use_max_x, cns.use_min_y, cns.use_max_y, cns.use_min_z, cns.use_max_z))

    elif typ == 'DAMPED_TRACK':
        fp.write("('DampedTrack', %s, %.2g, ['%s', '%s', '%s'])" % (space, inf, name, cns.subtarget, cns.track))

    elif typ == 'STRETCH_TO':
        fp.write("('StretchTo', %s, %.2g, ['%s', '%s', %.3g])" % (space, inf, name, cns.subtarget, cns.head_tail))

    elif typ == 'TRACK_TO':
        fp.write("('TrackTo', %s, %.2g, ['%s', '%s', %.3g, '%s', '%s', %s])" % (space, inf, name, 
        cns.subtarget, cns.head_tail, cns.track_axis, cns.up_axis, cns.use_target_z))

    elif typ == 'FLOOR':
        fp.write("('Floor', %s, %.2g, ['%s', '%s', '%s', %.3g, %s, %s])" % (space, inf, name, 
        cns.subtarget, cns.floor_location, cns.offset, cns.use_rotation, cns.use_sticky))

    elif typ == 'LIMIT_DISTANCE':
        fp.write("('LimitDist', %s, %.2g, ['%s', '%s', '%s'])" % (space, inf, name, cns.subtarget, cns.limit_mode))

    elif typ == 'TRANSFORM':
        fp.write("('Transform', %s, %.2g, \n" % (space, inf))
        fp.write("\t\t\t['%s', '%s', '%s', "% (name, cns.subtarget.replace(' ','_'), cns.map_from))
        transformWrite(fp, scale, cns.map_from, cns.from_min_x, cns.from_min_y, cns.from_min_z)
        transformWrite(fp, scale, cns.map_from, cns.from_max_x, cns.from_max_y, cns.from_max_z)
        fp.write("('%s','%s','%s'),\n\t\t\t'%s', " % (cns.map_to_x_from, cns.map_to_y_from, cns.map_to_x_from, cns.map_to))
        transformWrite(fp, scale, cns.map_to, cns.to_min_x, cns.to_min_y, cns.to_min_z)
        transformWrite(fp, scale, cns.map_to, cns.to_max_x, cns.to_max_y, cns.to_max_z)
        fp.write("])")
        
    elif typ == 'LOCKED_TRACK':
        fp.write("('LockedTrack', %s, %.2g, ['%s', '%s','%s'])" % (space, inf, name, cns.subtarget, cns.track_axis))
            
    elif typ == 'DAMPED_TRACK':
        fp.write("('LockedTrack', %s, %.2g, ['%s', '%s','%s'])" % (space, inf, name, cns.subtarget, cns.track))
    
    else:
        fp.write(typ)
        raise NameError("Unknown constraint type %s" % typ)

    return
        
def transformWrite(fp, scale, channel, x, y, z):
    print("  * ",channel, scale)
    if channel == 'LOCATION':
        fp.write("(%.3g,%.3g,%.3g), " % (scale*x, scale*y, scale*z))
    else:
        fp.write("(%.3g,%.3g,%.3g), " % (x,y,z))
    return

def extractName(b):
    boneType = b.name[:3]
    boneName = b.name[4:]
    #boneType = 0
    print(b.name, boneType, boneName)
    if boneType == 'MCH' or boneType == 'DEF' or boneType == 'ORG' or boneType == 'VIS':
        return (boneType, boneName)
    else:
        return ('GEN', b.name)

def doPad(m, n):
    if m > n+16:
        return '\t'
    elif m > n+8:
        return '\t\t'
    elif m > n:
        return '\t\t\t'
    else:
        return '\t\t\t\t'

###################################################################
#
#   User interface
#

#
#   writeBoneFile(character, scale, fname):
#    class OBJECT_OT_WriteBoneFile(bpy.types.Operator):
#

def writeBoneFile(character, scale, fname):
    fpath = os.path.realpath(os.path.expanduser(fname))
    print("Bone file %s for character %s" % (fpath, character))
    fp = open(fpath, "w")
    fp.write(
"#\n" +
"#  Bone definitions for %s rig\n" % character +
"#\n" +
"import mhx_globals as the\n")

    writeBones(character, scale, fp)
    fp.close()
    print("Bone file %s written" % fpath)
    return

class OBJECT_OT_WriteBoneFile(bpy.types.Operator):
    bl_idname = "wbf.write_bone_file"
    bl_label = "Write bonefile"

    def execute(self, context):
        scale = context.scene['BoneFileScale']
        name = context.object.name
        writeBoneFile(name, scale, "%s/%s_rig.py" % (context.scene['BoneFileDir'], name.lower()))
        return{'FINISHED'}    

#
#   writeWeightFile(ob, src, fname):
#   class OBJECT_OT_WriteWeightFiles(bpy.types.Operator):
#

def writeWeightFile(ob, src, fname):
    fpath = os.path.realpath(os.path.expanduser(fname))
    print("Weight file %s for character %s" % (fpath, ob))
    fp = open(fpath, "w")

    minheight = 1e6
    maxheight = -1e6
    for sv in src.data.vertices:
        z = sv.co[2]
        if z < minheight:
            minheight = z
        if z > maxheight:
            maxheight = z

    splices = {}
    fac = 20/(maxheight - minheight)
    for sv in src.data.vertices:
        z = int(fac*(sv.co[2] - minheight))
        try:
            splices[z].append(sv)
        except:
            splices[z] = [sv]

    table = {}
    for v in ob.data.vertices:
        zv = int(fac*(v.co[2] - minheight))
        mindist = 1e6
        for z in [zv-1,z,zv+1]:
            try:
                splice = splices[z]
            except:
                splice = []
            for sv in splice:
                offs = v.co - sv.co
                if offs.length < mindist:
                    best = sv
                    mindist = offs.length
        table[v.index] = best
        print(v.index, best.index)

    """
    for f in ob.data.faces:
        if len(f.vertices) == 3:
            for v in f.vertices:
                table[v] = None
    """

    for vg in src.vertex_groups:
        name = vg.name.replace(' ','_')
        print(name)
        fp.write("  VertexGroup %s\n" % name)
        for v in ob.data.vertices:
            sv = table[v.index]
            if sv:
                for g in sv.groups:
                    if g.group == vg.index and g.weight > 1e-4:
                        fp.write("    vw %d %.4g ;\n" % (v.index, g.weight))
        fp.write("  end VertexGroup\n")

    fp.close()
    print("Weight file %s written" % fpath)
    return

class OBJECT_OT_WriteWeightFiles(bpy.types.Operator):
    bl_idname = "wbf.write_weight_files"
    bl_label = "Write weight files"

    def execute(self, context):
        scn = context.scene
        dir = context.scene['BoneFileDir']
        src = context.object
        for ob in context.scene.objects:
            if ob.select and ob.type == 'MESH' and ob != src:            	
                writeWeightFile(ob, src, "%s/%s_weights.mhx" % (dir, ob.name.lower()))
        return{'FINISHED'}    


#
#   class WriteBoneFilePanel(bpy.types.Panel):
#

class WriteBoneFilePanel(bpy.types.Panel):
    bl_label = "Write bonefile"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return (context.object and 
            (context.object.type == 'ARMATURE' or context.object.type == 'MESH'))

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "BoneFileScale")
        layout.prop(context.scene, "BoneFileDir")
        layout.operator("wbf.write_bone_file")
        layout.operator("wbf.write_weight_files")
        return

#
#    Init and register
#

def initInterface(scn):
    bpy.types.Scene.BoneFileDir = StringProperty(
        name="Directory", 
        maxlen=1024)
    scn['BoneFileDir'] = "~/svn/mh/shared/mhx"

    bpy.types.Scene.BoneFileScale = FloatProperty(name="Scale")
    scn['BoneFileScale'] = 10.0
    return

initInterface(bpy.context.scene)

def register():
    bpy.utils.register_module(__name__)
    pass

def unregister():
    bpy.utils.unregister_module(__name__)
    pass

if __name__ == "__main__":
    register()


#writeBoneFile("Sintel", 10, "/home/thomas/myblends/sintel/sintel_bones-raw.py")
#writeBoneFile("Blenrig", 10, "/home/svn/mh/makehuman/shared/mhx/blenrig_bones_raw.py")
#writeBoneFile("Zepam", 10, "/home/thomas/svn/mh/shared/mhx/zepam_rig.py")




