#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------
MHX exporter for Blender 2.49b

TODO
"""

import module3d
import aljabr
import mh
import mh2bvh
import os
import sys
import time
import log

import mh2proxy
from . import the, mhxbones

splitLeftRight = True

#
#    exportMhx(human, filename, options, config):
#

def exportMhx(human, filename, options, config):    
    (name, ext) = os.path.splitext(filename)
    the.Human = 'Human'
    time1 = time.clock()
    filename = name+"-24"+ext
    try:
        fp = open(filename, 'w')
        log.message("Writing MHX 2.4x file %s", filename )
    except:
        log.message("Unable to open file for writing %s", filename)
        fp = 0
    if fp:
        exportMhx_24(human.meshData, config, fp)
        fp.close()
        time2 = time.clock()
        log.message("Wrote MHX 2.4x file in %g s: %s", time2-time1, filename)
    return
 
 #
 #    exportMhx_24(obj, config, fp):
 #
 
def exportMhx_24(obj, config, fp):
     fp.write(
 "# MakeHuman exported MHX\n" +
 "# www.makehuman.org\n" +
 "MHX 1 0 ;\n")
 
     fp.write(
 "#if Blender25\n"+
 "  error This file can not be opened in Blender 2.5x. Try the -25 file instead. ;\n "+
 "#endif\n")
 
     copyMaterialFile("shared/mhx/templates/materials24.mhx", fp)    
     exportArmature(obj, config, fp)
     tmpl = open("shared/mhx/templates/meshes24.mhx")
     if tmpl:
         copyMeshFile249(obj, tmpl, config, fp)    
         tmpl.close()
     return
 
 #
 #    exportRawMhx(obj, config, fp)
 #
 
def exportRawMhx(obj, config, fp):
    exportArmature(obj, config, fp)
    fp.write(
"#if useMesh \n" +
"mesh HumanMesh HumanMesh \n")
    exportRawData(obj, fp)
    fp.write(
"end mesh\n" +
"\nobject HumanMesh Mesh HumanMesh \n" +
"\tlayers 1 0 ;\n" +
"end object\n" +
"end useMesh\n")
    return       

#
#    copyMeshFile249(obj, tmpl, config, fp):
#

def copyMeshFile249(obj, tmpl, config, fp):
    inZone = False
    skip = False
    mainMesh = False

    for line in tmpl:
        words= line.split()
        skipOne = False

        if len(words) == 0:
            pass
        elif words[0] == 'end':
            if words[1] == 'object' and mainMesh:
                fp.write(line)
                skipOne = True
                fp.write("#endif\n")
                mainMesh = False
                fp.write("#if useProxy\n")
                for plist in config.proxyList:
                    if plist.useMhx:
                        exportProxy24(obj, plist, fp)
                fp.write("#endif\n")
            elif words[1] == 'mesh' and mainMesh:
                fp.write("  ShapeKey Basis Sym\n  end ShapeKey\n")
                copyShapeKeys("shared/mhx/templates/shapekeys-facial25.mhx", fp, None, False)    
                copyShapeKeys("shared/mhx/templates/shapekeys-extra24.mhx", fp, None, False)    
                copyShapeKeys("shared/mhx/templates/shapekeys-body25.mhx", fp, None, False)    
                writeIpo(fp)
                fp.write(line)
                skipOne = True
                fp.write("#endif\n")
                mainMesh = False
                inZone = False
                skip = False
        elif words[0] == 'mesh' and words[1] == 'HumanMesh':
            inZone = True
            mainMesh = True
            fp.write("#if useMesh\n")
        elif words[0] == 'object' and words[1] == '%sMesh' % the.Human:
            mainMesh = True
            fp.write("#if useMesh\n")
        elif words[0] == 'vertgroup':
            copyVertGroups("shared/mhx/templates/vertexgroups-24.mhx", fp, None)    
            skipOne = True
            skip = False
        elif words[0] == 'v' and inZone:
            if not skip:
                exportRawData(obj, fp)
                skip = True
        elif words[0] == 'f' and skip:
            skip = False
            skipOne = True

        if not (skip or skipOne):
            fp.write(line)
    
    return

#
#    copyVertGroups(tmplName, fp, proxy):
#

def copyVertGroups(tmplName, fp, proxy):
    tmpl = open(tmplName)
    shapes = []
    vgroups = []

    if tmpl == None:
        log.error("*** Cannot open %s", tmplName)
        return
    if not proxy:
        for line in tmpl:
            fp.write(line)
    else:
        for line in tmpl:
            words= line.split()
            if len(words) == 0:
                fp.write(line)
            elif words[0] == 'wv':
                v = int(words[1])
                wt = float(words[2])
                try:
                    vlist = proxy.verts[v]
                except:
                    vlist = []
                for (pv, w) in vlist:
                    pw = w*wt
                    if pw > 1e-4:
                        vgroups.append((pv, pw))
            elif words[0] == 'VertexGroup':
                gname = words[1]
                vgroups = []
            elif words[0] == 'end':
                if vgroups:
                    fp.write("  VertexGroup %s\n" % gname)
                    printProxyVGroup(fp, vgroups)
                    vgroups = []
                    fp.write(line)
            else:    
                fp.write(line)
    log.message("    %s copied", tmplName)
    tmpl.close()
    return

#
#    printProxyVGroup(fp, vgroups):
#

def printProxyVGroup(fp, vgroups):
    vgroups.sort()
    pv = -1
    while vgroups:
        (pv0, wt0) = vgroups.pop()
        if pv0 == pv:
            wt += wt0
        else:
            if pv >= 0 and wt > 1e-4:
                fp.write("    wv %d %.4f ;\n" % (pv, wt))
            (pv, wt) = (pv0, wt0)
    if pv >= 0 and wt > 1e-4:
        fp.write("    wv %d %.4f ;\n" % (pv, wt))
    return

#
#    copyMaterialFile(infile, fp):
#

def copyMaterialFile(infile, fp):
    tmpl = open(infile, "rU")
    for line in tmpl:
        words= line.split()
        if len(words) == 0:
            fp.write(line)
        elif words[0] == 'filename':
            path1 = os.path.expanduser("./data/textures/")
            (path, filename) = os.path.split(words[1])
            file1 = os.path.realpath(path1+filename)
            fp.write("  filename %s ;\n" % file1)
        else:
            fp.write(line)
    tmpl.close()

#
#    exportProxy24(obj, plist, fp):
#

def exportProxy24(obj, plist, fp):
    proxy = mh2proxy.readProxyFile(obj, plist, True)
    if not proxy:
        return
    faces = mh2proxy.oldStyleFaces(obj)
    tmpl = open("shared/mhx/templates/proxy24.mhx", "rU")
    for line in tmpl:
        words= line.split()
        if len(words) == 0:
            fp.write(line)
        elif words[0] == 'mesh':
            fp.write("mesh %s %s\n" % (proxy.name, proxy.name))
        elif words[0] == 'object':
            fp.write("object %s Mesh %s\n" % (proxy.name, proxy.name))
        elif words[0] == 'v':
            for bary in proxy.realVerts:
                (x,y,z) = mh2proxy.proxyCoord(bary)
                fp.write("v %.4g %.4g %.4g ;\n" % (x, -z, y))
        elif words[0] == 'f':
            for (f,g) in proxy.faces:
                fp.write("    f")
                for v in f:
                    fp.write(" %d" % v)
                fp.write(" ;\n")
            fn = 0
            for mat in proxy.materials:
                fp.write("    fx %d %d 1 ;\n" % (fn,mat))
                fn += 1
        elif words[0] == 'vt':
            for f in proxy.texFaces:
                fp.write("    vt")
                for v in f:
                    uv = proxy.texVerts[v]
                    fp.write(" %.4g %.4g" %(uv[0], uv[1]))
                fp.write(" ;\n")
        elif words[0] == 'vertgroup':
            copyVertGroups("shared/mhx/templates/vertexgroups-24.mhx", fp, proxy)    
        elif words[0] == 'shapekey':
            fp.write("  ShapeKey Basis Sym\n  end ShapeKey\n")
            copyShapeKeys("shared/mhx/templates/shapekeys-bodylanguage25.mhx", fp, proxy, False)    
            copyShapeKeys("shared/mhx/templates/shapekeys-extra24.mhx", fp, proxy, False)    
            copyShapeKeys("shared/mhx/templates/shapekeys-body25.mhx", fp, proxy, False)    
            writeIpo(fp)
        else:
            fp.write(line)
    tmpl.close()
    return

#
#    exportRawData(obj, fp):    
#

def exportRawData(obj, fp):    
    for v in obj.verts:
        fp.write("v %.4g %.4g %.4g ;\n" %(v.co[0], v.co[1], v.co[2]))
        
    for uv in obj.texco:
        fp.write("vt %.4g %.4g ;\n" %(uv[0], uv[1]))
        
    faces = mh2proxy.oldStyleFaces(obj)
    for f in faces:
        fp.write("f")
        #print(f)
        for v in f:
            fp.write(" %i/%i " %(v[0], v[1]))
        fp.write(";\n")
    

#
#    exportArmature(obj, config, fp):
#

def exportArmature(obj, config, fp):
    oldExportArmature24(obj, config, fp)
    #newExportArmature24(obj, config, fp)
    return

def oldExportArmature24(obj, config, fp):
    mhxbones.writeJoints(obj, fp)

    fp.write(
"\n#if useArmature\n" +
"armature Human Human\n")
    mhxbones.writeBones(obj, fp)
    fp.write(
"\tlayerMask 0x515 ;\n" +
"\tautoIK false ;\n" +
"\tdelayDeform false ;\n" +
"\tdrawAxes false ;\n" +
"\tdrawNames false ;\n" +
"\tenvelopes false ;\n" +
"\tmirrorEdit true ;\n" +
"\trestPosition false ;\n" +
"\tvertexGroups true ;\n" +
"end armature\n")

    fp.write("\npose Human\n")
    mhxbones.writePose24(obj, fp)
    fp.write("end pose\n")

    fp.write(
"\nobject Human Armature Human \n" +
"\tlayers 1 0 ;\n" +
"\txRay true ;\n" +
"end object\n" +
"#endif useArmature\n")

    return 

#
#    newExportArmature4(obj, config, fp):
#
def newExportArmature24(obj, config, fp):
    mhx_rig.newSetupJoints(obj, classic_bones.ClassicJoints)
    mhx_rig.setupHeadsTails(classic_bones.ClassicHeadsTails)
    
    fp.write(
"\n#if useArmature\n" +
"armature Human Human\n")
    mhx_rig.writeArmature(fp, config, classic_bones.ClassicArmature + classic_bones.PanelArmature)
    fp.write(
"\tlayerMask 0x515 ;\n" +
"\tautoIK false ;\n" +
"\tdelayDeform false ;\n" +
"\tdrawAxes false ;\n" +
"\tdrawNames false ;\n" +
"\tenvelopes false ;\n" +
"\tmirrorEdit true ;\n" +
"\trestPosition false ;\n" +
"\tvertexGroups true ;\n" +
"end armature\n")

    fp.write("\npose Human\n")
    classic_bones.ClassicWritePoses(fp, config)
    fp.write("end pose\n")
        
    fp.write(
"\nobject Human Armature Human \n" +
"\tlayers 1 0 ;\n" +
"\txRay true ;\n" +
"end object\n" +
"#endif useArmature\n")

    return 

    
#
#    exportShapeKeys(obj, tmpl, fp, proxy):
#

def exportShapeKeys(obj, tmpl, fp, proxy):
    global splitLeftRight
    if tmpl == None:
        return
    lineNo = 0    
    store = False
    for line in tmpl:
        lineNo += 1
        words= line.split()
        if len(words) == 0:
            pass
        elif words[0] == 'end' and words[1] == 'shapekey' and store:
            if leftRightKey[shapekey] and splitLeftRight:
                writeShapeKey(fp, shapekey+"_L", shapeVerts, "Left", sliderMin, sliderMax, proxy)
                writeShapeKey(fp, shapekey+"_R", shapeVerts, "Right", sliderMin, sliderMax, proxy)
            else:
                writeShapeKey(fp, shapekey, shapeVerts, "None", sliderMin, sliderMax, proxy)
        elif words[0] == 'shapekey':
            shapekey = words[1]
            sliderMin = words[2]
            sliderMax = words[3]
            shapeVerts = []
            if shapekey[5:] == 'Bend' or shapekey[5:] == 'Shou':
                store = False
            else:
                store = True
        elif words[0] == 'sv' and store:
            shapeVerts.append(line)
    return

#
#    leftRightKey - True if shapekey comes in two parts
#

leftRightKey = {
    "Basis" : False,
    "BendElbowForward" : True,
    "BendHeadForward" : False,
    "BendKneeBack" : True,
    "BendLegBack" : True,
    "BendLegForward" : True,
    "BrowsDown" : True,
    "BrowsMidDown" : False,
    "BrowsMidUp" : False,
    "BrowsOutUp" : True,
    "BrowsSqueeze" : False,
    "CheekUp" : True,
    "Frown" : True,
    "UpLidDown" : True,
    "LoLidUp" : True,
    "Narrow" : True,
    "ShoulderDown" : True,
    "Smile" : True,
    "Sneer" : True,
    "Squint" : True,
    "TongueOut" : False,
    "ToungeUp" : False,
    "ToungeLeft" : False,
    "ToungeRight" : False,
    "UpLipUp" : True,
    "LoLipDown" : True,
    "MouthOpen" : False,
    "UpLipDown" : True,
    "LoLipUp" : True,
}

#
#    writeShapeKey(fp, shapekey, shapeVerts, vgroup, sliderMin, sliderMax, proxy):
#

def writeShapeKey(fp, shapekey, shapeVerts, vgroup, sliderMin, sliderMax, proxy):
    fp.write("shapekey %s %s %s %s\n" % (shapekey, sliderMin, sliderMax, vgroup))
    if proxy:
        shapes = []
        for line in shapeVerts:
            words = line.split()
            v = int(words[1])
            dx = float(words[2])
            dy = float(words[3])
            dz = float(words[4])
            try:
                vlist = proxy.verts[v]
            except:
                vlist = []
            for (pv,w) in vlist:
                shapes.append((pv, w*dx, w*dy, w*dz))
        printProxyShape(fp, shapes)
    else:
        for line in shapeVerts:
            fp.write(line)
    fp.write("end shapekey\n")

#
#    writeIcu(fp, shape, expr):
#

def writeIcu(fp, shape, expr):
    fp.write(
"\ticu %s 0 1\n" % shape +
"\t\tdriver 2 ;\n" +
"\t\tdriverObject _object['%sMesh' % the.Human] ;\n" +
"\t\tdriverChannel 1 ;\n" +
"\t\tdriverExpression '%s' ;\n" % expr +
"\tend icu\n")

def writeIpo(fp):
    global splitLeftRight

    mhxFile = "shared/mhx/templates/mhxipos.mhx"
    try:
        tmpl = open(mhxFile, "rU")
    except:
        log.error("*** Cannot open %s", mhxFile)
        tmpl = None

    if tmpl and splitLeftRight:
        for line in tmpl:
            fp.write(line)
    else:
        fp.write("ipo Key KeyIpo\n")
        for (shape, lr) in leftRightKey.items():
            if shape == 'Basis':
                pass
            elif lr and splitLeftRight:
                writeIcu(fp, shape+'_L', 'p.ctrl'+shape+'_L()')
                writeIcu(fp, shape+'_R', 'p.ctrl'+shape+'_R()')
            else:
                writeIcu(fp, shape, 'p.ctrl'+shape+'()')
        fp.write("end ipo\n")
    
    if tmpl:
        log.message("    %s copied", mhxFile)
        tmpl.close()

    return


def useThisShape(name, proxy):
    if not proxy:
        return True
    if proxy.type == 'Proxy':
        return True
    if name in proxy.shapekeys:
        return True
    if name[:-2] in proxy.shapekeys:
        return True
    return False

#
#    copyShapeKeys(tmplName, fp, proxy, doScale):
#

def copyShapeKeys(tmplName, fp, proxy, doScale):
    tmpl = open(tmplName)
    shapes = []
    vgroups = []
    scale = 1.0

    if tmpl == None:
        log.error("*** Cannot open %s", tmplName)
        return
    if not proxy:
        for line in tmpl:
            words = line.split()
            if len(words) == 0:
                fp.write(line)
            elif words[0] == 'sv':
                v = int(words[1])
                dx = float(words[2])*scale
                dy = float(words[3])*scale
                dz = float(words[4])*scale
                fp.write("    sv %d %.4f %.4f %.4f ;\n" % (v, dx, dy, dz))
            elif words[0] == 'ShapeKey':
                if doScale:
                    scale = setShapeScale(words)
                fp.write(line)
            else:
                fp.write(line)
    else:
        ignore = False
        for line in tmpl:
            words= line.split()
            if len(words) == 0:
                fp.write(line)
            elif words[0] == 'ShapeKey':
                if doScale:
                    scale = setShapeScale(words)
                if useThisShape(words[1], proxy):
                    fp.write(line)
                    ignore = False
                else:
                    ignore = True
            elif ignore:
                pass
            elif words[0] == 'sv':
                v = int(words[1])
                dx = float(words[2])*scale
                dy = float(words[3])*scale
                dz = float(words[4])*scale
                try:
                    vlist = proxy.verts[v]
                except:
                    vlist = []
                for (pv, w) in vlist:
                    shapes.append((pv, w*dx, w*dy, w*dz))
            elif shapes:
                printProxyShape(fp, shapes)
                shapes = []
                fp.write(line)
            else:    
                fp.write(line)
    log.message("    %s copied", tmplName)
    tmpl.close()
    return


#    setShapeScale(words):    
#

def setShapeScale(words):
    key = words[1]
    scales = None
    try:
        scales = rig_panel_25.FaceShapeKeyScale[key]
    except:
        pass
    try:
        scales = rig_body_25.BodyShapeKeyScale[key]
    except:
        pass
    if not scales:
        raise NameError("No scale for %s" % key)
    (p1, p2, length0) = scales
    x1 = the.Locations[p1]
    x2 = the.Locations[p2]
    dist = aljabr.vsub(x1, x2)
    length = aljabr.vlen(dist)
    scale = length/length0
    #print("Scale %s %f %f" % (key, length, scale))
    return scale
                
#
#    printProxyShape(fp, shapes)
#

def printProxyShape(fp, shapes):
    shapes.sort()
    pv = -1
    while shapes:
        (pv0, dx0, dy0, dz0) = shapes.pop()
        if pv0 == pv:
            dx += dx0
            dy += dy0
            dz += dz0
        else:
            if (pv >= 0 and aljabr.vlen([dx,dy,dz]) > 0):
                fp.write("    sv %d %.4f %.4f %.4f ;\n" % (pv, dx, dy, dz))
            (pv, dx, dy, dz) = (pv0, dx0, dy0, dz0)        
    if (pv >= 0 and aljabr.vlen([dx,dy,dz]) > 0):
        fp.write("    sv %d %.4f %.4f %.4f ;\n" % (pv, dx, dy, dz))
    return

 
 
