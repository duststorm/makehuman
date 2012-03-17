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
#   checkObjectOK(ob, context):
#

def checkObjectOK(ob, context):
    old = context.object
    context.scene.objects.active = ob
    word = None
    error = False
    epsilon = 1e-4
    if ob.location.length > epsilon:
        word = "object translation"
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    eu = ob.rotation_euler
    if abs(eu.x) + abs(eu.y) + abs(eu.z) > epsilon:
        word = "object rotation"
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    vec = ob.scale - Vector((1,1,1))
    if vec.length > epsilon:
        word = "object scaling"
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if ob.constraints:
        word = "constraints"
        error = True
    if ob.parent:
        word = "parent"
        ob.parent = None
    if word:
        msg = "Object %s can not be used for rig creation because it has %s.\n" % (ob.name, word)
        if error:
            msg +=  "Apply or delete before continuing.\n"
            print(msg)
            raise NameError(msg)
        else:
            print(msg)
            print("Fixed automatically")
    context.scene.objects.active = old
    return    

#
#   exportRigFile(context):
#

def exportRigFile(context):
    (rig,ob) = getRigAndMesh(context)
    checkObjectOK(rig, context)
    checkObjectOK(ob, context)
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
    bpy.ops.mesh.select_all(action='INVERT')
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
#    unVertexDiamonds(context):
#

def unVertexDiamonds(context):
    ob = context.object
    print("Unvertex diamonds in %s" % ob)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    me = ob.data
    for f in me.faces:        
        if len(f.vertices) < 4:
            for vn in f.vertices:
                me.vertices[vn].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.vertex_group_remove_from(all=True)
    bpy.ops.object.mode_set(mode='OBJECT')
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
    #outpath = '%s/%s' % (context.scene.MRDirectory, name)
    outpath = os.path.realpath(os.path.expanduser(context.scene.MRDirectory))
    if not os.path.exists(outpath):
        print("Creating directory %s" % outpath)
        os.mkdir(outpath)
    outfile = os.path.join(outpath, "%s.%s" % (name, ext))
    return (outpath, outfile)

#
#    symmetrizeWeights(context):
#    class VIEW3D_OT_SymmetrizeWeightsButton(bpy.types.Operator):
#

Epsilon = 1e-3

def symmetrizeWeights(context, left2right):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    scn = context.scene

    left = {}
    left01 = {}
    left02 = {}
    leftIndex = {}
    left01Index = {}
    left02Index = {}
    right = {}
    right01 = {}
    right02 = {}
    rightIndex = {}
    right01Index = {}
    right02Index = {}
    symm = {}
    symmIndex = {}
    for vgrp in ob.vertex_groups:
        if vgrp.name[-2:] in ['_L', '.L', '_l', '.l']:
            nameStripped = vgrp.name[:-2]
            left[nameStripped] = vgrp
            leftIndex[vgrp.index] = nameStripped
        elif vgrp.name[-2:] in ['_R', '.R', '_r', '.r']:
            nameStripped = vgrp.name[:-2]
            right[nameStripped] = vgrp
            rightIndex[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.L.01', '.l.01']:
            nameStripped = vgrp.name[:-5]
            left01[nameStripped] = vgrp
            left01Index[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.R.01', '.r.01']:
            nameStripped = vgrp.name[:-5]
            right01[nameStripped] = vgrp
            right01Index[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.L.02', '.l.02']:
            nameStripped = vgrp.name[:-5]
            left02[nameStripped] = vgrp
            left02Index[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.R.02', '.r.02']:
            nameStripped = vgrp.name[:-5]
            right02[nameStripped] = vgrp
            right02Index[vgrp.index] = nameStripped
        else:
            symm[vgrp.name] = vgrp
            symmIndex[vgrp.index] = vgrp.name

    printGroups('Left', left, leftIndex, ob.vertex_groups)
    printGroups('Right', right, rightIndex, ob.vertex_groups)
    printGroups('Left01', left01, left01Index, ob.vertex_groups)
    printGroups('Right01', right01, right01Index, ob.vertex_groups)
    printGroups('Left02', left02, left02Index, ob.vertex_groups)
    printGroups('Right02', right02, right02Index, ob.vertex_groups)
    printGroups('Symm', symm, symmIndex, ob.vertex_groups)

    (lverts, rverts, mverts) = setupVertexPairs(context)
    if left2right:
        factor = 1
        fleft = left
        fright = right
        groups = list(right.values()) + list(right01.values()) + list(right02.values())
        cleanGroups(ob.data, groups)
    else:
        factor = -1
        fleft = right
        fright = left
        rverts = lverts
        groups = list(left.values()) + list(left01.values()) + list(left02.values())
        cleanGroups(ob.data, groups)

    for (vn, rvn) in rverts.items():
        v = ob.data.vertices[vn]
        rv = ob.data.vertices[rvn]
        #print(v.index, rv.index)
        for rgrp in rv.groups:
            rgrp.weight = 0
        for grp in v.groups:
            rgrp = None
            for (indices, groups) in [
                (leftIndex, right), (rightIndex, left),
                (left01Index, right01), (right01Index, left01),
                (left02Index, right02), (right02Index, left02),
                (symmIndex, symm)
                ]:
                try:
                    name = indices[grp.group]
                    rgrp = groups[name]
                except:
                    pass
            if rgrp:
                #print("  ", name, grp.group, rgrp.name, rgrp.index, v.index, rv.index, grp.weight)
                rgrp.add([rv.index], grp.weight, 'REPLACE')
            else:                
                gn = grp.group
                print("*** No rgrp for %s %s %s" % (grp, gn, ob.vertex_groups[gn]))
    return len(rverts)

def printGroups(name, groups, indices, vgroups):
    print(name)
    for (nameStripped, grp) in groups.items():
        print("  ", nameStripped, grp.name, indices[grp.index])
    return

def cleanGroups(me, groups):
    for grp in groups:
        print(grp)
        for v in me.vertices:
            grp.remove([v.index])
    return
    
#----------------------------------------------------------
#   setupVertexPairs(ob):
#----------------------------------------------------------

def setupVertexPairs(context):
    ob = context.object
    verts = []
    for v in ob.data.vertices:
        x = v.co[0]
        y = v.co[1]
        z = v.co[2]
        verts.append((z,y,x,v.index))
    verts.sort()        
    lverts = {}
    rverts = {}
    mverts = {}
    nmax = len(verts)
    notfound = []
    for n,data in enumerate(verts):
        (z,y,x,vn) = data
        n1 = n - 20
        n2 = n + 20
        if n1 < 0: n1 = 0
        if n2 >= nmax: n2 = nmax
        vmir = findVert(verts[n1:n2], vn, -x, y, z, notfound)
        if vmir < 0:
            mverts[vn] = vn
        elif x > Epsilon:
            rverts[vn] = vmir
        elif x < -Epsilon:
            lverts[vn] = vmir
        else:
            mverts[vn] = vmir
    if notfound:            
        print("Did not find mirror image for vertices:")
        for msg in notfound:
            print(msg)
    print("Left-right-mid", len(lverts.keys()), len(rverts.keys()), len(mverts.keys()))
    return (lverts, rverts, mverts)
    
def findVert(verts, v, x, y, z, notfound):
    for (z1,y1,x1,v1) in verts:
        dx = x-x1
        dy = y-y1
        dz = z-z1
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < Epsilon:
            return v1
    if abs(x) > Epsilon:            
        notfound.append("  %d at (%.4f %.4f %.4f)" % (v, x, y, z))
    return -1                    

#
#   readDefaultSettings(context):
#   saveDefaultSettings(context):
#

def settingsFile():
    outdir = os.path.expanduser("~/makehuman/settings/")        
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    return os.path.join(outdir, "make_rig.settings")

def readDefaultSettings(context):
    fname = settingsFile() 
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
    fname = settingsFile() 
    fp = open(fname, "w")
    scn = context.scene
    for (prop, value) in scn.items():
        if prop[0:2] == "MR":
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
   