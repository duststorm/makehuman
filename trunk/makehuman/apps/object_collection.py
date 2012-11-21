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
import mh2proxy
import export_config

#
#    class CStuff
#

class CStuff:
    def __init__(self, name, proxy):
        self.name = os.path.basename(name)
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
        self.texture = None
        self.proxy = None
        if proxy:
            self.proxy = proxy
            self.type = proxy.type
            self.material = proxy.material
            self.texture = proxy.texture
            
    def __repr__(self):
        return "<CStuff %s %s mat %s tex %s>" % (self.name, self.type, self.material, self.texture)

    def setBones(self, armature):
        (rigHead, rigTail, rigHier, bones, rawWeights) = armature
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
#    filterMesh(mesh1, obj, groups, deleteVerts, helpers, eyebrows, lashes):
#

def filterMesh(mesh1, obj, deleteGroups, deleteVerts, helpers, eyebrows, lashes):
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
            
    for vn in deleteVerts:
        killVerts[vn] = True
    
    for fg in obj.faceGroups:
        if (((not helpers) and 
             (("joint" in fg.name) or ("helper" in fg.name))) or
            ((not eyebrows) and 
             (("eyebrown" in fg.name) or ("cornea" in fg.name))) or
            ((not lashes) and 
             ("lash" in fg.name)) or
             mh2proxy.deleteGroup(fg.name, deleteGroups)):
            #print("  kill %s" % fg.name) 
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

    if weights1:
        weights2 = {}
        for (b, wts1) in weights1.items():
            wts2 = []
            for (v1,w) in wts1:
                if not killVerts[v1]:
                    wts2.append((nv[v1],w))
            weights2[b] = wts2
    else:
        weights2 = weights1

    if targets1:
        targets2 = []
        for (name, morphs1) in targets1:
            morphs2 = []
            for (v1,dx) in morphs1:
                if not killVerts[v1]:
                    morphs2.append((nv[v1],dx))
            targets2.append(name, morphs2)
    else:
        targets2 = targets1

    return (verts2, vnormals2, uvValues2, faces2, weights2, targets2)

#
#   setupObjects(name, human, armature):
#

def setupObjects(name, human, armature=None, helpers=False, eyebrows=True, lashes=True):
    global theStuff, theTextures, theTexFiles, theMaterials
    
    cfg = export_config.exportConfig(human, True)
    obj = human.meshData
    theTextures = {}
    theTexFiles = {}
    theMaterials = {}
    rawTargets = []
    stuffs = []
    stuff = CStuff(name, None)
    if armature:
        stuff.setBones(armature)
    theStuff = stuff
    deleteGroups = []
    deleteVerts = []
    setupProxies('Clothes', None, obj, stuffs, armature, rawTargets, cfg.proxyList, deleteGroups, deleteVerts)
    foundProxy = setupProxies('Proxy', name, obj, stuffs, armature, rawTargets, cfg.proxyList, deleteGroups, deleteVerts)
    if not foundProxy:
        mesh1 = mh2proxy.getMeshInfo(obj, None, stuff.rawWeights, rawTargets, None)
        if (helpers and eyebrows and lashes and 
            deleteGroups == [] and
            deleteVerts == []):
            mesh2 = mesh1
        else:
            mesh2 = filterMesh(mesh1, obj, deleteGroups, deleteVerts, helpers, eyebrows, lashes)
        stuff.setMesh(mesh2)
        stuffs = [stuff] + stuffs
    return stuffs

#
#    setupProxies(typename, name, obj, stuffs, armature, rawTargets, proxyList, deleteGroups, deleteVerts):
#

def setupProxies(typename, name, obj, stuffs, armature, rawTargets, proxyList, deleteGroups, deleteVerts):
    global theStuff
    
    foundProxy = False    
    for pfile in proxyList:
        if pfile.type == typename and pfile.file:
            proxy = mh2proxy.readProxyFile(obj, pfile, True)
            if proxy and proxy.name and proxy.texVerts:
                foundProxy = True
                deleteGroups += proxy.deleteGroups
                deleteVerts = mh2proxy.multiplyDeleteVerts(proxy, deleteVerts)
                if name:
                    stuff = CStuff(name, proxy)
                else:
                    stuff = CStuff(proxy.name, proxy)
                if armature:
                    stuff.setBones(armature)
                if stuff:
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
#   getTextureNames(stuff):
#

def getTextureNames(stuff):
    global theTextures, theTexFiles, theMaterials

    if not stuff.type:
        return ("SkinShader", None, "SkinShader")
        
    try:
        texname = theTextures[stuff.name]
        texfile = theTexFiles[stuff.name]
        matname = theMaterials[stuff.name]
        return (texname, texfile, matname)
    except KeyError:
        pass
    
    texname = None
    texfile = None
    matname = None
    if stuff.texture:        
        (folder, fname) = stuff.texture
        (texname, ext) = os.path.splitext(fname)
        texfile = ("%s_%s" % (texname, ext[1:]))
        while texname in theTextures.values():
            texname = nextName(texname)
        theTextures[stuff.name] = texname
        theTexFiles[stuff.name] = texfile
    if stuff.material:
        matname = stuff.material.name
        while matname in theMaterials.values():
            matname = nextName(matname)
        theMaterials[stuff.name] = matname
    return (texname, texfile, matname)
    
    
def nextName(string):
    try:
        n = int(string[-3:])
    except:
        n = -1
    if n >= 0:
        return "%s%03d" % (string[:-3], n+1)
    else:
        return string + "_001"
        
