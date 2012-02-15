""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract: 
Bone weighting utility

"""
import bpy, os, mathutils
import math
from mathutils import *
from bpy.props import *


BodyVert = 3000
SkirtVert = 16000
TightsVert = 18000

#
#   writeBones(character, scale, fp):
#

def getRigAndMesh(context):
    rig = None
    me = None
    for ob in bpy.context.scene.objects:
        if ob.select:
            if ob.type == 'ARMATURE':
                if rig:
                    raise NameError("Two armatures selected")
                rig = ob
            elif ob.type == 'MESH':
                if me:
                    raise NameError("Two meshes selected")
                me = ob
    if rig and me:
        print("Using rig %s and mesh %s" % (rig, me))
    else:
        raise NameError("Must select one mesh and one armature")
    return (rig, me)
    

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

def writeJoint(fp, jName, loc, joints, me):
    found = findJoint(jName, loc, joints)
    if found:
        joints[jName] = found
    else:
        joints[jName] = (jName, loc)
        v = closestVert(loc, me)
        offs = loc - v.co
        fp.write("  %s voffset %d %.4g %.4g %.4g\n" % (jName, v.index, offs[0], offs[1], offs[2]))
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
#   writeBones(fp, rig, me):
#

def writeBones(fp, rig, me):
    bpy.context.scene.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')
    
    # List symbolic joint locations
    joints = {}
    fp.write("\n# locations\n")
    for eb in rig.data.edit_bones:
        ebName = eb.name.replace(" ","_")
        writeJoint(fp, ebName+"_head", eb.head, joints, me)
        writeJoint(fp, ebName+"_tail", eb.tail, joints, me)
    fp.write("\n")
    
    # List symbolic names for heads and tails
    fp.write("# bones\n")
    for eb in rig.data.edit_bones:
        #print("Bone", eb.name, eb.head, eb.tail)
        ebName = eb.name.replace(" ","_")
        hfound = findJoint(ebName+"_head", None, joints)
        tfound = findJoint(ebName+"_tail", None, joints)
        if hfound == None or tfound == None:
            fp.write("  %s %s %s" % ( ebName, eb.head, eb.tail))
            fp.close()
            raise NameError("ht", hfound, tfound)
        (hname,hx) = hfound
        (tname,tx) = tfound
        fp.write(" %s %s %s " % (ebName, hname, tname))
        if eb.roll < 0.02 and eb.roll > -0.02:
            fp.write("0 ")
        else:
            fp.write("%.3f " % eb.roll)
        if eb.parent:
            fp.write("%s " % eb.parent.name.replace(' ','_'))
        else:
            fp.write("- ")

        if not eb.use_deform:
            fp.write("-nd ")
        if not eb.use_connect:
            fp.write("-nc ")
        fp.write("\n")

#
#    writeVertexGroups(filePath)
#

def writeVertexGroups(fp, ob):
    for vg in ob.vertex_groups:
        index = vg.index
        weights = []
        for v in ob.data.vertices:
            for grp in v.groups:
                if grp.group == index and grp.weight > 0.005:
                    weights.append((v.index, grp.weight))    
        exportList(fp, weights, vg.name, 0)
    return
    
def exportList(fp, weights, name, offset):
    if len(weights) == 0:
        return
    if len(weights) > 0:
        fp.write("\n# weights %s\n" % name)
        for (vn,w) in weights:
            if w > 0.005:
                fp.write("  %d %.3g\n" % (vn+offset, w))
    

#
#   exportRigFile(context):
#

def exportRigFile(context):
    (rig,ob) = getRigAndMesh(context)
    (rigpath, rigfile) = getFileName(rig, context, "rig")
    print("Open", rigfile)
    fp = open(rigfile, "w")
    scn = context.scene
    fp.write(
        "# author %s\n" % scn.MRAuthor +
        "# license %s\n" % scn.MRLicense +
        "# homepage %s\n" % scn.MRHomePage)
    writeBones(fp, rig, ob.data)
    writeVertexGroups(fp, ob)
    fp.close()
    return
    
#
#   autoWeightBody(context)
#

def autoWeightBody(context):
    (rig,ob) = getRigAndMesh(context)
    scn = context.scene
    scn.objects.active = ob

    # Clean up original mesh
    for mod in ob.modifiers:
        if mod.type == 'ARMATURE':
            ob.modifiers.remove(mod)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.vertex_group_remove(all=True)
    
    # Copy mesh and autoweight duplicate
    rig.select = False
    ob.select = True
    bpy.ops.object.duplicate()
    dupliob = scn.objects.active
    for vn in [BodyVert]:
        dupliob.data.vertices[vn].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_linked(limit=False)
    bpy.ops.mesh.select_inverse()
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    rig.select = True
    scn.objects.active = rig
    print("Parent", ob, "to", rig)
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    
    # Copy vertex weights back from duplicate
    vgroups = {}
    for dgrp in dupliob.vertex_groups:
        vgrp = ob.vertex_groups.new(dgrp.name)
        vgroups[dgrp.index] = vgrp
    vn = -1
    for dv in dupliob.data.vertices:
        dist = 1000
        while dist > 0.001:
            vn += 1
            v = ob.data.vertices[vn]
            vec = v.co - dv.co
            dist = vec.length
        for dg in dv.groups:
            vgroups[dg.group].add([vn], dg.weight, 'REPLACE')
            
    ob.parent = rig
    mod = ob.modifiers.new("Armature", 'ARMATURE')
    mod.object = rig
    mod.use_vertex_groups = True
    mod.use_bone_envelopes = False
    scn.objects.unlink(dupliob)    
    return
     
#
#    class CProxy
#

class CProxy:
    def __init__(self):
        self.refVerts = []
        self.firstVert = 0
        return
        
    def setWeights(self, verts, grp):
        rlen = len(self.refVerts)
        mlen = len(verts)
        first = self.firstVert
        if (first+rlen) != mlen:
            raise NameError( "Bug: %d refVerts != %d meshVerts" % (first+rlen, mlen) )
        gn = grp.index
        for n in range(rlen):
            vert = verts[n+first]
            refVert = self.refVerts[n]
            if type(refVert) == tuple:
                (rv0, rv1, rv2, w0, w1, w2, d0, d1, d2) = refVert
                vw0 = CProxy.getWeight(verts[rv0], gn)
                vw1 = CProxy.getWeight(verts[rv1], gn)
                vw2 = CProxy.getWeight(verts[rv2], gn)
                vw = w0*vw0 + w1*vw1 + w2*vw2
            else:
                vw = getWeight(verts[refVert], gn)
            grp.add([vert.index], vw, 'REPLACE')
        return
   
    def getWeight(vert, gn):
        for grp in vert.groups:
            if grp.group == gn:
                return grp.weight
        return 0             
        
    def read(self, filepath):
        realpath = os.path.realpath(os.path.expanduser(filepath))
        folder = os.path.dirname(realpath)
        try:
            tmpl = open(filepath, "rU")
        except:
            tmpl = None
        if tmpl == None:
            print("*** Cannot open %s" % realpath)
            return None

        status = 0
        doVerts = 1
        vn = 0
        for line in tmpl:
            words= line.split()
            if len(words) == 0:
                pass
            elif words[0] == '#':
                status = 0
                if len(words) == 1:
                    pass
                elif words[1] == 'verts':
                    if len(words) > 2:
                        self.firstVert = int(words[2])                    
                    status = doVerts
                else:
                    pass
            elif status == doVerts:
                if len(words) == 1:
                    v = int(words[0])
                    self.refVerts.append(v)
                else:                
                    v0 = int(words[0])
                    v1 = int(words[1])
                    v2 = int(words[2])
                    w0 = float(words[3])
                    w1 = float(words[4])
                    w2 = float(words[5])            
                    d0 = float(words[6])
                    d1 = float(words[7])
                    d2 = float(words[8])
                    self.refVerts.append( (v0,v1,v2,w0,w1,w2,d0,d1,d2) )
        return
        
def autoWeightHelpers(context):
    ob = context.object
    proxy = CProxy()
    scn = context.scene
    path = os.path.join(scn.MRMakeHumanDir, "data/3dobjs/base.mhclo")
    proxy.read(path)
    for grp in ob.vertex_groups:
        print(grp.name)
        proxy.setWeights(ob.data.vertices, grp)
    print("Weights projected from proxy")
    return     
    
#
#   goodName(name):    
#   getFileName(pob, context, ext):            
#

def goodName(name):    
    newName = name.replace('-','_').replace(' ','_')
    return newName.lower()
    
def getFileName(ob, context, ext):            
    name = goodName(ob.name)
    outpath = '%s/%s' % (context.scene.MRDirectory, name)
    outpath = os.path.realpath(os.path.expanduser(outpath))
    if not os.path.exists(outpath):
        print("Creating directory %s" % outpath)
        os.mkdir(outpath)
    outfile = os.path.join(outpath, "%s.%s" % (name, ext))
    return (outpath, outfile)

#
#   readDefaultSettings(context):
#   saveDefaultSettings(context):
#

def readDefaultSettings(context):
    fname = os.path.realpath(os.path.expanduser("~/make_rig.settings"))
    try:
        fp = open(fname, "rU")
    except:
        print("Did not find %s. Using default settings" % fname)
        return
    
    scn = context.scene
    for line in fp:
        words = line.split()
        prop = words[0]
        type = words[1]        
        if type == "int":
            scn[prop] = int(words[2])
        elif type == "float":
            scn[prop] = float(words[2])
        elif type == "str":
            string = words[2]
            for word in words[3:]:
                string += " " + word
            scn[prop] = string
    fp.close()
    return
    
def saveDefaultSettings(context):
    fname = os.path.realpath(os.path.expanduser("~/make_rig.settings"))
    fp = open(fname, "w")
    scn = context.scene
    for (prop, value) in scn.items():
        if prop[0:2] == "MC":
            if type(value) == int:
                fp.write("%s int %s\n" % (prop, value))
            elif type(value) == float:
                fp.write("%s float %.4f\n" % (prop, value))
            elif type(value) == str:
                fp.write("%s str %s\n" % (prop, value))
    fp.close()
    return
    
#
#   initInterface():
#

def initInterface():
    bpy.types.Scene.MRDirectory = StringProperty(
        name="Directory", 
        description="Directory", 
        maxlen=1024,
        default="~")
        
    bpy.types.Scene.MRMakeHumanDir = StringProperty(
        name="MakeHuman directory", 
        description="The directory where MakeHuman is installed", 
        maxlen=1024,
        default="/home/svn/makehuman")        
    
    bpy.types.Scene.MRAuthor = StringProperty(
        name="Author", 
        default="Unknown",
        maxlen=32)
    
    bpy.types.Scene.MRLicense = StringProperty(
        name="License", 
        default="GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)",
        maxlen=256)
    
    bpy.types.Scene.MRHomePage = StringProperty(
        name="HomePage", 
        default="http://www.makehuman.org/",
        maxlen=256)
    

    return
   