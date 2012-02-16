#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
MakeHuman to Collada (MakeHuman eXchange format) exporter. Collada files can be loaded into
Blender by collada_import.py.

TO DO

"""

import module3d
import aljabr
import mh
import files3d
import mh2bvh
import os, time
import shutil
import mh2proxy, mh2mhx
import export_config
import mhx_rig, rig_body_25, rig_arm_25, rig_finger_25, rig_leg_25, rig_toe_25, rig_face_25, rig_panel_25
from mhx_rig import *
import read_rig

#
#    Size of end bones = 1 mm
# 
Delta = [0,0.01,0]

#
# exportCollada(human, filename, options):
#

def exportCollada(human, name, options):
    global useRotate90, theOptions
    useRotate90 = options["rotate90"]
    theOptions = options
    filename = name+".dae"
    time1 = time.clock()
    try:
        fp = open(filename, 'w')
        export_config.safePrint("Writing Collada file", filename)
    except:
        export_config.safePrint("Unable to open file for writing", filename)
    exportDae(human, fp)
    fp.close()
    time2 = time.clock()
    export_config.safePrint("Wrote Collada file in %g s:" % (time2-time1), filename)
    return

#
#    findInHierarchy(bone, hier):
#

def findInHierarchy(bone, hier):
    if hier == []:
        return []
    for pair in hier:
        (b, children) = pair
        if b == bone:
            return pair
        else:
            b = findInHierarchy(bone, children)
            if b: return b
    return []

#
#    flatten(hier, bones):
#

def flatten(hier, bones):
    for (bone, children) in hier:
        bones.append(bone)
        flatten(children, bones)
    return

#
#
#

def printLoc(fp, loc):
    global useRotate90
    if useRotate90:
        fp.write("%.4f %.4f %.4f " % (loc[0], -loc[2], loc[1]))
    else:
        fp.write("%.4f %.4f %.4f " % (loc[0], loc[1], loc[2]))

#
#    boneOK(flags, bone, parent):
#

reparents = {
    'UpArm_L'     : 'Clavicle_L',
    'UpArm_R'     : 'Clavicle_R',
    'UpLeg_L'     : 'Hip_L',
    'UpLeg_R'     : 'Hip_R',
    
    'UpArmTwist_L'     : 'Clavicle_L',
    'UpArmTwist_R'     : 'Clavicle_R',
    'UpLegTwist_L'     : 'Hip_L',
    'UpLegTwist_R'     : 'Hip_R',
}

twistBones = {
    'UpArmTwist_L'     : 'UpArm_L',
    'UpArmTwist_R'     : 'UpArm_R',
    'LoArmTwist_L'     : 'LoArm_L',
    'LoArmTwist_R'     : 'LoArm_R',
    'UpLegTwist_L'     : 'UpLeg_L',
    'UpLegTwist_R'     : 'UpLeg_R',
}

skipBones = [ 'Rib_L', 'Rib_R', 'Stomach_L', 'Stomach_R', 'Scapula_L', 'Scapula_R']

def boneOK(flags, bone, parent):
    if bone == Root:
        return 'None'
    elif bone in twistBones.keys():
        return None
    elif bone in skipBones:
        return None
    elif bone in reparents.keys():
        return reparents[bone]
    elif flags & F_DEF:
        return parent
    elif bone in ['HipsInv']:
        return parent
    return None
    
#
#    readSkinWeights(weights, tmplName):
#
#    VertexGroup Breathe
#    wv 2543 0.148938 ;
#

def readSkinWeights(weights, tmplName):
    tmpl = open(tmplName, "rU")
    if tmpl == None:
        print("Cannot open template "+tmplName)
        return
    for line in tmpl:
        lineSplit= line.split()
        if len(lineSplit) == 0:
            pass
        elif lineSplit[0] == 'VertexGroup':
            grp = []
            weights[lineSplit[1]] = grp
        elif lineSplit[0] == 'wv':
            grp.append((lineSplit[1],lineSplit[2]))
    return

def fixTwistWeights(fp, weights):
    for (twist, bone) in twistBones.items():
        wts = weights[twist] + weights[bone]
        wts.sort()
        nwts = []
        n = 1
        weights[bone] = nwts
        while n < len(wts):
            (v0, w0) = wts[n-1]
            (v1, w1) = wts[n]
            if v0 == v1:
                nwts.append((v0, w0+w1))
                n += 2
            else:
                nwts.append((v0, w0))
                n += 1
        fp.write("\n%s\n%s\n%s\n" % (twist, weights[twist], weights[bone]))
    return
                
#
#    writeBone(fp, bone, orig, extra, pad, stuff):
#

def writeBone(fp, bone, orig, extra, pad, stuff):
    (name, children) = bone
    head = stuff.rigHead[name]
    vec = aljabr.vsub(head, orig)
    printNode(fp, name, vec, extra, pad)
    for child in children:
        writeBone(fp, child, head, '', pad+'  ', stuff)    
    fp.write('\n%s      </node>' % pad)
    return
    
    
def printNode(fp, name, vec, extra, pad):
    # print(name, vec)
    if name:
        nameStr = 'sid="%s"' % name
        idStr = 'id="%s" name="%s"' % (name, name)
    else:
        nameStr = ''
        idStr = ''
    fp.write('\n'+
'%s      <node %s %s type="JOINT" %s>\n' % (pad, extra, nameStr, idStr) +
'%s        <translate sid="translate"> ' % pad)
    printLoc(fp, vec)
    fp.write('</translate>\n' +
'%s        <rotate sid="rotateZ">0 0 1 0.0</rotate>\n' % pad +
'%s        <rotate sid="rotateY">0 1 0 0.0</rotate>\n' % pad +
'%s        <rotate sid="rotateX">1 0 0 0.0</rotate>\n' % pad +
'%s        <scale sid="scale">1.0 1.0 1.0</scale>' % pad)
    

#
#    getArmatureFromRigFile(fileName, obj):    
#

def getArmatureFromRigFile(fileName, obj):
    global Root
    (locations, armature, weights) = read_rig.readRigFile(fileName, obj)
    
    hier = []
    heads = {}
    tails = {}
    Root = None
    for (bone, head, tail, roll, parent, options) in armature:
        heads[bone] = head
        tails[bone] = tail
        if parent == '-':
            hier.append((bone, []))
            if not Root:
                Root = bone
        else:
            parHier = findInHierarchy(parent, hier)
            try:
                (p, children) = parHier
            except:
                raise NameError("Did not find %s parent %s" % (bone, parent))
            children.append((bone, []))
    
    if not Root:
        raise NameError("No root bone found in rig file %s" % fileName)
    # newHier = addInvBones(hier, heads, tails)
    newHier = hier
    bones = []
    flatten(newHier, bones)
    return (heads, tails, newHier, bones, weights)

#
#    addInvBones(hier, heads, tails):
#

def addInvBones(hier, heads, tails):
    newHier = []
    for (bone, children) in hier:
        newChildren = addInvBones(children, heads, tails)
        n = len(children)
        if n == 1:
            (child, subChildren) = children[0]
            offs = vsub(tails[bone], heads[child])
        if n > 1 or (n == 1 and vlen(offs) > 1e-4):
            boneInv = bone+"Inv"
            heads[boneInv] = tails[bone]
            #tails[boneInv] = heads[bone]
            tails[boneInv] = aljabr.vadd(tails[bone], Delta)
            newHier.append( (bone, [(boneInv, newChildren)]) )
        else:
            newHier.append( (bone, newChildren) )

    return newHier

#
#    class CStuff
#

class CStuff:
    def __init__(self, name, proxy):
        self.name = name
        self.type = None
        self.bones = None
        self.rawWeights = None
        self.verts  = None
        self.vnormals = None
        self.uvValues = None
        self.faces = None
        self.weights = None
        self.targets = None
        self.vertexWeights = None
        self.skinWeights = None
        self.material = None
        if proxy:
            self.type = proxy.type
            self.material = proxy.material

    def setBones(self, amt):
        (rigHead, rigTail, rigHier, bones, rawWeights) = amt
        self.rigHead = rigHead
        self.rigTail = rigTail
        self.rigHier = rigHier
        self.bones = bones
        self.rawWeights = rawWeights

    def copyBones(self, rig):
        self.rigHead = rig.rigHead
        self.rigTail = rig.rigTail
        self.rigHier = rig.rigHier
        self.bones = rig.bones
        self.rawWeights = rig.rawWeights

    def setMesh(self, mesh):
        (verts, vnormals, uvValues, faces, weights, targets) = mesh
        self.verts = verts
        self.vnormals = vnormals
        self.uvValues = uvValues
        self.faces = faces
        self.weights = weights
        self.targets = targets
        return

#
#    filterMesh(mesh1, obj):
#

def filterMesh(mesh1, obj):
    (verts1, vnormals1, uvValues1, faces1, weights1, targets1) = mesh1
    
    killVerts = {}
    killUvs = {}
    killFaces = {}    
    for v in obj.verts:
        killVerts[v.idx] = False
    for f in obj.faces:
        killFaces[f.idx] = False        
        for vt in f.uv:
            killUvs[vt] = False
    
    for fg in obj.faceGroups:
        if ("joint" in fg.name) or ("helper" in fg.name):
            for f in fg.faces:
                killFaces[f.idx] = True
                for v in f.verts:
                    killVerts[v.idx] = True
                for vt in f.uv:                    
                    killUvs[vt] = True
    
    n = 0
    nv = {}
    verts2 = []
    for m,v in enumerate(verts1):
        if not killVerts[m]:
            verts2.append(v)
            nv[m] = n
            n += 1

    vnormals2 = []
    for m,vn in enumerate(vnormals1):
        if not killVerts[m]:
            vnormals2.append(vn)

    n = 0
    uvValues2 = []
    nuv = {}
    for m,uv in enumerate(uvValues1):
        if not killUvs[m]:
            uvValues2.append(uv)
            nuv[m] = n
            n += 1    

    faces2 = []
    for fn,f in enumerate(faces1):
        if not killFaces[fn]:
            f2 = []
            for c in f:
                v2 = nv[c[0]]
                uv2 = nuv[c[1]]
                f2.append([v2, uv2])
            faces2.append(f2)

    weights2 = {}
    for (b, wts1) in weights1.items():
        wts2 = []
        for (v1,w) in wts1:
            if not killVerts[v1]:
                wts2.append((nv[v1],w))
        weights2[b] = wts2

    targets2 = []
    for (name, morphs1) in targets1:
        morphs2 = []
        for (v1,dx) in morphs1:
            if not killVerts[v1]:
                morphs2.append((nv[v1],dx))
        targets2.append(name, morphs2)

    return (verts2, vnormals2, uvValues2, faces2, weights2, targets2)

#
#    exportDae(human, fp):
#

def exportDae(human, fp):
    global theStuff, Root, useRotate90, theOptions
    cfg = export_config.exportConfig(human, True)
    obj = human.meshData
    rigfile = "data/rigs/%s.rig" % theOptions["daerig"]
    print("Using rig file %s" % rigfile)
    amt = getArmatureFromRigFile(rigfile, obj)
    #rawTargets = loadShapeKeys("data/templates/shapekeys-facial25.mhx")
    rawTargets = []

    stuffs = []
    stuff = CStuff('Human', None)
    stuff.setBones(amt)
    theStuff = stuff
    foundProxy = setupProxies('Proxy', obj, stuffs, amt, rawTargets, cfg.proxyList)
    if not foundProxy:
        mesh1 = mh2proxy.getMeshInfo(obj, None, stuff.rawWeights, rawTargets, None)
        if theOptions["keepHelpers"]:
            mesh2 = mesh1
        else:
            mesh2 = filterMesh(mesh1, obj)
        stuff.setMesh(mesh2)
        stuffs.append(stuff)
    setupProxies('Clothes', obj, stuffs, amt, rawTargets, cfg.proxyList)

    if theStuff.verts == None:
        raise NameError("No rig found. Neither main mesh nor rigged proxy enabled")
        
    date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
    if useRotate90:
        upaxis = 'Z_UP'
    else:
        upaxis = 'Y_UP'
        
    fp.write('<?xml version="1.0" encoding="utf-8"?>\n' +
'<COLLADA version="1.4.0" xmlns="http://www.collada.org/2005/11/COLLADASchema">\n' +
'  <asset>\n' +
'    <contributor>\n' +
'      <author>www.makehuman.org</author>\n' +
'    </contributor>\n' +
'    <created>%s</created>\n' % date +
'    <modified>%s</modified>\n' % date +
'    <unit meter="0.1" name="decimeter"/>\n' +
'    <up_axis>%s</up_axis>\n' % upaxis+
'  </asset>\n' +
'  <library_images>\n')

    for stuff in stuffs:
        writeImages(obj, fp, stuff)

    fp.write(
'  </library_images>\n' +
'  <library_effects>\n')

    for stuff in stuffs:
        writeEffects(obj, fp, stuff)

    fp.write(
'  </library_effects>\n' +
'  <library_materials>\n')

    for stuff in stuffs:
        writeMaterials(obj, fp, stuff)

    fp.write(
'  </library_materials>\n'+
'  <library_controllers>\n')

    for stuff in stuffs:
        writeController(obj, fp, stuff)

    fp.write(
'  </library_controllers>\n'+
'  <library_geometries>\n')

    for stuff in stuffs:
        writeGeometry(obj, fp, stuff)

    fp.write(
'  </library_geometries>\n\n' +
'  <library_visual_scenes>\n' +
'    <visual_scene id="Scene" name="Scene">\n' +
'      <node id="Scene_root">\n')
    for root in theStuff.rigHier:
        writeBone(fp, root, [0,0,0], 'layer="L1"', '  ', theStuff)
    for stuff in stuffs:
        writeNode(obj, fp, "        ", stuff)

    fp.write(
'      </node>\n' +    
'    </visual_scene>\n' +
'  </library_visual_scenes>\n' +
'  <scene>\n' +
'    <instance_visual_scene url="#Scene"/>\n' +
'  </scene>\n' +
'</COLLADA>\n')
    return

#
#    setupProxies(typename, obj, stuffs, amt, rawTargets, proxyList):
#

def setupProxies(typename, obj, stuffs, amt, rawTargets, proxyList):
    global theStuff
    foundProxy = False    
    for pfile in proxyList:
        if pfile.useDae and pfile.type == typename:
            proxy = mh2proxy.readProxyFile(obj, pfile, True)
            if proxy and proxy.name and proxy.texVerts:
                foundProxy = True
                stuff = CStuff(proxy.name, proxy)
                print(proxy.name, proxy.rig, proxy.weightfile)
                if proxy.rig:
                    amtProxy = getArmatureFromRigFile(proxy.rig, obj)
                    stuff.setBones(amtProxy)
                    if theStuff.verts:
                        print("WARNING: Collada export with several meshes. Ignored %s" % proxy.name)
                        stuff = None
                    else:
                        theStuff = stuff    
                elif proxy.weightfile:
                    (rigname, filename) = proxy.weightfile
                    if theStuff and rigname == theStuff.name:
                        print("copy")
                        stuff.copyBones(theStuff)
                    else:
                        print("amt")
                        stuff.setBones(amt)
                else:
                    print("amt2")
                    stuff.setBones(amt)
                    #theStuff.verts = True
                if stuff:
                    print("Stuff", stuff.name, theStuff.name)
                    if pfile.type == 'Proxy':
                        theStuff = stuff
                    if theStuff:
                        stuffname = theStuff.name
                    else:
                        stuffname = None
                    mesh = mh2proxy.getMeshInfo(obj, proxy, stuff.rawWeights, rawTargets, stuffname)
                    stuff.setMesh(mesh)
                    stuffs.append(stuff)
    return foundProxy

#
#    writeImages(obj, fp, stuff):
#

def writeImages(obj, fp, stuff):
    global theOptions
    if stuff.type:
        return
    for fname in ["texture", "texture_ref"]:
        srcfile = os.path.realpath(os.path.expanduser("data/textures/%s.tif" % fname))
        print("Image %s" % srcfile)
        if theOptions["copyImages"]:    
            destdir = mh.getPath('exports')
            #destdir = "/Users/Thomas/Documents"
            destfile = os.path.realpath(os.path.expanduser("%s/%s.tif" % (destdir,fname)))
            texfile = "./%s.tif" % (fname)
            shutil.copy2(srcfile, destfile)
            print("  copied to export directory")
        else:
            texfile = srcfile
            
        fp.write(
'    <image id="%s_tif" name="%s_tif">\n' % (fname, fname) +
'      <init_from>"%s"</init_from>\n' % texfile +
'    </image>\n')
    return

#
#    writeEffects(obj, fp, stuff):
#    writeColor(fp, name, color, insist):
#

def writeColor(fp, name, color, insist):
    if color:
        (r,g,b) = color
    elif insist:
        (r,g,b) = insist
    else:
        return
    fp.write(
'            <%s>\n' % name +
'              <color>%.4f %.4f %.4f 1</color>\n' % (r,g,b) +
'            </%s>\n' %name)
    return 

def writeEffects(obj, fp, stuff):
    mat = stuff.material
    if mat:
        fp.write(
'    <effect id="%s-effect">\n' % mat.name +
'      <profile_COMMON>\n' +
'        <technique sid="common">\n' +
'          <phong>\n')
        BlenderDaeColor = {
            'diffuse_color' : 'diffuse',
            'specular_color' : 'specular',
            'emit_color' : 'emission',
            'ambient_color' : 'ambient'
        }
        for (key, value) in mat.settings:
            try:
                daeKey = BlenderDaeColor[key]
            except:
                daeKey = None
            if daeKey:
                writeColor(fp, daeKey, value, (0.8,0.8,0.8))
        fp.write(
'          </phong>\n' +
'          <extra/>\n' +
'        </technique>\n' +
'        <extra>\n' +
'          <technique profile="GOOGLEEARTH">\n' +
'            <show_double_sided>1</show_double_sided>\n' +
'          </technique>\n' +
'        </extra>\n' +
'      </profile_COMMON>\n' +
'      <extra><technique profile="MAX3D"><double_sided>1</double_sided></technique></extra>\n' +
'    </effect>\n')
    elif not stuff.type:
        fp.write(
'    <effect id="SSS_skinshader-effect">\n' +
'      <profile_COMMON>\n' +
'        <newparam sid="texture_tif-surface">\n' +
'          <surface type="2D">\n' +
'            <init_from>texture_tif</init_from>\n' +
'          </surface>\n' +
'        </newparam>\n' +
'        <newparam sid="texture_tif-sampler">\n' +
'          <sampler2D>\n' +
'            <source>texture_tif-surface</source>\n' +
'          </sampler2D>\n' +
'        </newparam>\n' +
'        <newparam sid="texture_ref_tif-surface">\n' +
'          <surface type="2D">\n' +
'            <init_from>texture_ref_tif</init_from>\n' +
'          </surface>\n' +
'        </newparam>\n' +
'        <newparam sid="texture_ref_tif-sampler">\n' +
'          <sampler2D>\n' +
'            <source>texture_ref_tif-surface</source>\n' +
'          </sampler2D>\n' +
'        </newparam>\n' +
'        <technique sid="common">\n' +
'          <lambert>\n' +
'            <diffuse>\n' +
'              <texture texture="texture_tif-sampler" texcoord="UVTex"/>\n' +
'            </diffuse>\n' +
'            <transparency>\n' +
'              <texture texture="texture_tif-sampler" texcoord="UVTex"/>\n' +
'            </transparency>\n' +
'            <index_of_refraction>\n' +
'              <float>1</float>\n' +
'            </index_of_refraction>\n' +
'          </lambert>\n' +
'        </technique>\n' +
'      </profile_COMMON>\n' +
'    </effect>\n')
    return

#
#    writeMaterials(obj, fp, stuff):
#

def writeMaterials(obj, fp, stuff):
    mat = stuff.material
    if mat:
        fp.write(
'    <material id="%s" name="%s">\n' % (mat.name, mat.name) +
'      <instance_effect url="#%s-effect"/>\n' % mat.name +
'    </material>\n')
    elif not stuff.type:
        fp.write(
'    <material id="SSS_skinshader" name="SSS_skinshader">\n' +
'      <instance_effect url="#SSS_skinshader-effect"/>\n' +
'    </material>\n')
    return

#
#   setStuffSkinWeights(stuff):
#

def setStuffSkinWeights(stuff):
    stuff.vertexWeights = {}
    for (vn,v) in enumerate(stuff.verts):
        stuff.vertexWeights[vn] = []

    stuff.skinWeights = []
    wn = 0    
    for (bn,b) in enumerate(stuff.bones):
        try:
            wts = stuff.weights[b]
        except:
            wts = []
        for (vn,w) in wts:
            stuff.vertexWeights[int(vn)].append((bn,wn))
            wn += 1
        stuff.skinWeights.extend(wts)
    return
    
#
#    writeController(obj, fp, stuff):
#

def writeController(obj, fp, stuff):
    setStuffSkinWeights(stuff)
    nVerts = len(stuff.verts)
    nUvVerts = len(stuff.uvValues)
    nNormals = nVerts
    nFaces = len(stuff.faces)
    nWeights = len(stuff.skinWeights)
    nBones = len(stuff.bones)
    nTargets = len(stuff.targets)

    fp.write('\n' +
'    <controller id="%s-skin">\n' % stuff.name +
'      <skin source="#%sMesh">\n' % stuff.name +
'        <bind_shape_matrix>\n' +
'          1.0 0.0 0.0 0.0 \n' +
'          0.0 1.0 0.0 0.0 \n' +
'          0.0 0.0 1.0 0.0 \n' +
'          0.0 0.0 0.0 1.0 \n' +
'        </bind_shape_matrix>\n' +
'        <source id="%s-skin-joints">\n' % stuff.name +
'          <IDREF_array count="%d" id="%s-skin-joints-array">\n' % (nBones,stuff.name) +
'           ')

    for b in stuff.bones:
        fp.write(' %s' % b)
    
    fp.write('\n' +
'          </IDREF_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-skin-joints-array" stride="1">\n' % (nBones,stuff.name) +
'              <param type="IDREF" name="JOINT"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="%s-skin-weights">\n' % stuff.name +
'          <float_array count="%d" id="%s-skin-weights-array">\n' % (nWeights,stuff.name) +
'           ')

    for (n,b) in enumerate(stuff.skinWeights):
        (v,w) = stuff.skinWeights[n]
        fp.write(' %s' % w)

    fp.write('\n' +
'          </float_array>\n' +    
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-skin-weights-array" stride="1">\n' % (nWeights,stuff.name) +
'              <param type="float" name="WEIGHT"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="%s-skin-poses">\n' % stuff.name +
'          <float_array count="%d" id="%s-skin-poses-array">' % (16*nBones,stuff.name))

    mat = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    for b in stuff.bones:
        vec = stuff.rigHead[b]
        if useRotate90:
            mat[0][3] = -vec[0]
            mat[1][3] = vec[2]
            mat[2][3] = -vec[1]
        else:            
            mat[0][3] = -vec[0]
            mat[1][3] = -vec[1]
            mat[2][3] = -vec[2]
        fp.write('\n            ')
        for i in range(4):
            for j in range(4):
                fp.write('%.4f ' % mat[i][j])

    fp.write('\n' +
'          </float_array>\n' +    
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-skin-poses-array" stride="16">\n' % (nBones,stuff.name) +
'              <param type="float4x4"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <joints>\n' +
'          <input semantic="JOINT" source="#%s-skin-joints"/>\n' % stuff.name +
'          <input semantic="INV_BIND_MATRIX" source="#%s-skin-poses"/>\n' % stuff.name +
'        </joints>\n' +
'        <vertex_weights count="%d">\n' % nVerts +
'          <input offset="0" semantic="JOINT" source="#%s-skin-joints"/>\n' % stuff.name +
'          <input offset="1" semantic="WEIGHT" source="#%s-skin-weights"/>\n' % stuff.name +
'          <vcount>\n' +
'            ')

    for wts in stuff.vertexWeights.values():
        fp.write('%d ' % len(wts))

    fp.write('\n' +
'          </vcount>\n'
'          <v>\n' +
'           ')

    #print(stuff.vertexWeights)
    for (vn,wts) in stuff.vertexWeights.items():
        wtot = 0.0
        for (bn,wn) in wts:
            wtot += wn
        if wtot < 0.01:
            # print("wtot", vn, wtot)
            wtot = 1
        for (bn,wn) in wts:
            fp.write(' %d %d' % (bn, wn))

    fp.write('\n' +
'          </v>\n' +
'        </vertex_weights>\n' +
'      </skin>\n' +
'    </controller>\n')

    """
    fp.write('\n' +
'   <controller id="%sMorphs" name="%sMorphs">\n' % (stuff.name,stuff.name) +
'     <morph method="NORMALIZED" source="#%sMesh">\n' % stuff.name +
'       <source id="%s-targets">\n' % stuff.name +
'         <IDREF_array id="%s-targets-array" count="%d">\n'  % (stuff.name, nTargets))

    for (name, morphs) in targets:
        fp.write(' %s' % name)

    fp.write('\n' +
'         </IDREF_array>\n' +
'         <technique_common>\n' +
'           <accessor source="%s-targets-array" count="%d" stride="1">\n' % (stuff.name,nTargets) +
'             <param name="MORPH_TARGET" type="IDREF"/>\n' +
'           </accessor>\n' +
'         </technique_common>\n' +
'       </source>\n' +
'       <source id="%s-morph_weights">\n' % name +
'         <float_array id="%s-morph_weights-array" count="%d">\n' % (stuff.name,nTargets))

    for target in targets:
        fp.write("0.0 ")

    fp.write('\n' +
'         </float_array>\n' +
'         <technique_common>\n' +
'           <accessor source="#%s-morph_weights-array" count="%d" stride="1">\n' % (stuff.name,nTargets) +

'             <param name="MORPH_WEIGHT" type="float"/>\n' +
'           </accessor>\n' +
'         </technique_common>\n' +
'       </source>\n' +
'       <targets>\n' +
'         <input semantic="MORPH_TARGET" source="#%s-targets"/>\n' % stuff.name +
'         <input semantic="MORPH_WEIGHT" source="#%s-morph_weights"/>\n' % stuff.name +
'       </targets>\n' +
'     </morph>\n' +
'   </controller>\n')
    """
    return

#
#    writeGeometry(obj, fp, stuff):
#
        
def writeGeometry(obj, fp, stuff):
    nVerts = len(stuff.verts)
    nUvVerts = len(stuff.uvValues)
    nNormals = nVerts
    nWeights = len(stuff.skinWeights)
    nBones = len(stuff.bones)
    nTargets = len(stuff.targets)

    fp.write('\n' +
'    <geometry id="%sMesh" name="%s">\n' % (stuff.name,stuff.name) +
'      <mesh>\n' +
'        <source id="%s-Position">\n' % stuff.name +
'          <float_array count="%d" id="%s-Position-array">\n' % (3*nVerts,stuff.name) +
'          ')


    for v in stuff.verts:
        printLoc(fp, v)

    fp.write('\n' +
'          </float_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-Position-array" stride="3">\n' % (nVerts,stuff.name) +
'              <param type="float" name="X"></param>\n' +
'              <param type="float" name="Y"></param>\n' +
'              <param type="float" name="Z"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="%s-Normals">\n' % stuff.name +
'          <float_array count="%d" id="%s-Normals-array">\n' % (3*nNormals,stuff.name) +
'          ')

    for no in stuff.vnormals:
        printLoc(fp, no)

    fp.write('\n' +
'          </float_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-Normals-array" stride="3">\n' % (nNormals,stuff.name) +
'              <param type="float" name="X"></param>\n' +
'              <param type="float" name="Y"></param>\n' +
'              <param type="float" name="Z"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="%s-UV">\n' % stuff.name +

'          <float_array count="%d" id="%s-UV-array">\n' % (2*nUvVerts,stuff.name) +
'           ')


    for uv in stuff.uvValues:
        fp.write(" %.4f %.4f" %(uv[0], uv[1]))

    fp.write('\n' +
'          </float_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-UV-array" stride="2">\n' % (nUvVerts,stuff.name) +
'              <param type="float" name="S"></param>\n' +
'              <param type="float" name="T"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <vertices id="%s-Vertex">\n' % stuff.name +
'          <input semantic="POSITION" source="#%s-Position"/>\n' % stuff.name +
'        </vertices>\n')

    checkFaces(stuff, nVerts, nUvVerts)
    #writePolygons(fp, stuff)
    writePolylist(fp, stuff)
    
    fp.write(
'      </mesh>\n' +
'    </geometry>\n')

    """
    for target in targets:
        (name, morphs) = target
        fp.write('\n' +
'   <geometry id="%s" name="%s">\n' % (name, name) +
'     <mesh>\n' +
'       <source id="%s-positions" name="%s-position">\n' % (name, name) +
'         <float_array id="%s-positions-array" count="%d">\n' % (name, 3*nVerts) +
'          ')
        for (vn,v) in enumerate(verts):
            try:
                offs = morphs[vn]
                loc = vadd(v, offs)
            except:
                loc = v
            printLoc(fp, loc)

        fp.write('\n'+
'         </float_array>\n' +
'         <technique_common>\n' +
'           <accessor source="#%s-positions-array" count="%d" stride="3">\n' % (stuff.name, nVerts) +
'             <param name="X" type="float"/>\n' +
'             <param name="Y" type="float"/>\n' +
'             <param name="Z" type="float"/>\n' +
'           </accessor>\n' +
'         </technique_common>\n' +
'       </source>\n' +
'     </mesh>\n' +
'   </geometry>\n')
    """
    return
    
#
#   writePolygons(fp, stuff):
#   writePolylist(fp, stuff):
#

def writePolygons(fp, stuff):
    fp.write(        
'        <polygons count="%d">\n' % len(stuff.faces) +
'          <input offset="0" semantic="VERTEX" source="#%s-Vertex"/>\n' % stuff.name +
'          <input offset="1" semantic="NORMAL" source="#%s-Normals"/>\n' % stuff.name +
'          <input offset="2" semantic="TEXCOORD" source="#%s-UV"/>\n' % stuff.name)

    for fc in stuff.faces:
        fp.write('          <p>')
        for vs in fc:
            v = vs[0]
            uv = vs[1]
            fp.write("%d %d %d " % (v, v, uv))
        fp.write('</p>\n')
    
    fp.write('\n' +
'        </polygons>\n')
    return

def writePolylist(fp, stuff):
    fp.write(        
'        <polylist count="%d">\n' % len(stuff.faces) +
'          <input offset="0" semantic="VERTEX" source="#%s-Vertex"/>\n' % stuff.name +
'          <input offset="1" semantic="NORMAL" source="#%s-Normals"/>\n' % stuff.name +
'          <input offset="2" semantic="TEXCOORD" source="#%s-UV"/>\n' % stuff.name +
'          <vcount>')

    for fc in stuff.faces:
        fp.write('%d ' % len(fc))

    fp.write('\n' +
'          </vcount>\n'
'          <p>')

    for fc in stuff.faces:
        for vs in fc:
            v = vs[0]
            uv = vs[1]
            fp.write("%d %d %d " % (v, v, uv))

    fp.write(
'          </p>\n' +
'        </polylist>\n')
    return

#
#   checkFaces(stuff, nVerts, nUvVerts):
#

def checkFaces(stuff, nVerts, nUvVerts):
    for fc in stuff.faces:
        for vs in fc:
            v = vs[0]
            uv = vs[1]
            if v > nVerts:
                raise NameError("v %d > %d" % (v, nVerts))
            if uv > nUvVerts:
                raise NameError("uv %d > %d" % (uv, nUvVerts))            
    return 
    
#
#    writeNode(obj, fp, pad, stuff):
#

def writeNode(obj, fp, pad, stuff):    
    fp.write('\n' +
'%s<node id="%sObject" name="%s">\n' % (pad, stuff.name,stuff.name) +
'%s  <translate sid="translate">0 0 0</translate>\n' % pad +
'%s  <rotate sid="rotateZ">0 0 1 0</rotate>\n' % pad +
'%s  <rotate sid="rotateY">0 1 0 0</rotate>\n' % pad +
'%s  <rotate sid="rotateX">1 0 0 0</rotate>\n' % pad+
#'%s  <scale sid="scale">1 1 1</scale>\n' % pad+
'%s  <instance_controller url="#%s-skin">\n' % (pad, stuff.name) +
'%s    <skeleton>#%s</skeleton>\n' % (pad, Root))

    if stuff.type == None:
        matname = 'SSS_skinshader'
    elif stuff.material:
        matname = stuff.material.name
    else:
        matname = None

    if matname:
        fp.write(
'%s    <bind_material>\n' % pad +
'%s      <technique_common>\n' % pad +
'%s        <instance_material symbol="%s" target="#%s">\n' % (pad, matname, matname) +
'%s          <bind_vertex_input semantic="UVTex" input_semantic="TEXCOORD" input_set="0"/>\n' % pad +
'%s        </instance_material>\n' % pad +
'%s      </technique_common>\n' % pad +
'%s    </bind_material>\n' % pad)

    fp.write(
'%s  </instance_controller>\n' % pad +
'%s</node>\n' % pad)
    return

#
#    loadShapeKeys(tmplName):    
#    ShapeKey BrowsDown LR toggle&T_Face
#      sv 2139 0 0 -0.0109844
#

def loadShapeKeys(tmplName):
    tmpl = open(tmplName, "rU")
    if tmpl == None:
        print("Cannot open template "+tmplName)
        return []

    targets = []
    for line in tmpl:
        lineSplit= line.split()

        if len(lineSplit) == 0:
            pass
        elif lineSplit[0] == 'ShapeKey':
            morph = {}
            targets.append((lineSplit[1], morph))
        elif lineSplit[0] == 'wv':
            v = int(lineSplit[1])
            x = float(lineSplit[2])
            y = float(lineSplit[3])
            z = float(lineSplit[4])
            morph[v] = [x,y,z]

    tmpl.close()
    return targets

    

