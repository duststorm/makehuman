#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
MHX exporter for Blender 2.49b

TO DO

"""
import module3d
import aljabr
import mh
import mh2bvh
import os
import sys
import time

import mh2proxy
import mhxbones 
import mhx_main

splitLeftRight = True

#
#    exportMhx(human, filename, options):
#

def exportMhx(human, filename, options):    
    (name, ext) = os.path.splitext(filename)
    mhx_main.theHuman = 'Human'
    time1 = time.clock()
    filename = name+"-24"+ext
    try:
        fp = open(filename, 'w')
        mh2proxy.safePrint("Writing MHX 2.4x file",  filename )
    except:
        mh2proxy.safePrint("Unable to open file for writing", filename)
        fp = 0
    if fp:
        exportMhx_24(human.meshData, fp)
        fp.close()
        time2 = time.clock()
        mh2proxy.safePrint("Wrote MHX 2.4x file in %g s:" % (time2-time1), filename)
    return
 
 #
 #    exportMhx_24(obj, fp):
 #
 
def exportMhx_24(obj, fp):
     fp.write(
 "# MakeHuman exported MHX\n" +
 "# www.makehuman.org\n" +
 "MHX 1 0 ;\n")
 
     fp.write(
 "#if Blender25\n"+
 "  error This file can not be opened in Blender 2.5x. Try the -25 file instead. ;\n "+
 "#endif\n")
 
     mhx_main.copyMaterialFile("shared/mhx/templates/materials24.mhx", fp)    
     exportArmature(obj, fp)
     tmpl = open("shared/mhx/templates/meshes24.mhx")
     if tmpl:
         copyMeshFile249(obj, tmpl, fp)    
         tmpl.close()
     return
 
 #
 #    exportRawMhx(obj, fp)
 #
 
def exportRawMhx(obj, fp):
    exportArmature(obj, fp)
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
#    copyMeshFile249(obj, tmpl, fp):
#

def copyMeshFile249(obj, tmpl, fp):
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
                for (typ, useObj, useMhx, useDae, proxyStuff) in mhx_main.theConfig.proxyList:
                    if useMhx:
                        exportProxy24(obj, proxyStuff, fp)
                fp.write("#endif\n")
            elif words[1] == 'mesh' and mainMesh:
                fp.write("  ShapeKey Basis Sym\n  end ShapeKey\n")
                mhx_main.copyShapeKeys("shared/mhx/templates/shapekeys-facial25.mhx", fp, None, False)    
                mhx_main.copyShapeKeys("shared/mhx/templates/shapekeys-extra24.mhx", fp, None, False)    
                mhx_main.copyShapeKeys("shared/mhx/templates/shapekeys-body25.mhx", fp, None, False)    
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
        elif words[0] == 'object' and words[1] == '%sMesh' % mhx_main.theHuman:
            mainMesh = True
            fp.write("#if useMesh\n")
        elif words[0] == 'vertgroup':
            mhx_main.copyVertGroups("shared/mhx/templates/vertexgroups-common25.mhx", fp, None)    
            mhx_main.copyVertGroups("shared/mhx/templates/vertexgroups-classic25.mhx", fp, None)    
            mhx_main.copyVertGroups("shared/mhx/templates/vertexgroups-toes25.mhx", fp, None)    
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
#    exportProxy24(obj, proxyStuff, fp):
#

def exportProxy24(obj, proxyStuff, fp):
    proxy = mh2proxy.readProxyFile(obj, proxyStuff)
    faces = mhx_main.loadFacesIndices(obj)
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
                fp.write("v %.6g %.6g %.6g ;\n" % (x, -z, y))
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
                    fp.write(" %.6g %.6g" %(uv[0], uv[1]))
                fp.write(" ;\n")
        elif words[0] == 'vertgroup':
            mhx_main.copyVertGroups("shared/mhx/templates/vertexgroups-common25.mhx", fp, proxy)    
            mhx_main.copyVertGroups("shared/mhx/templates/vertexgroups-classic25.mhx", fp, proxy)    
            mhx_main.copyVertGroups("shared/mhx/templates/vertexgroups-toes25.mhx", fp, proxy)    
        elif words[0] == 'shapekey':
            fp.write("  ShapeKey Basis Sym\n  end ShapeKey\n")
            if mhx_main.BODY_LANGUAGE:
                mhx_main.copyShapeKeys("shared/mhx/templates/shapekeys-bodylanguage25.mhx", fp, proxy, False)    
            else:
                mhx_main.copyShapeKeys("shared/mhx/templates/shapekeys-facial25.mhx", fp, proxy, False)    
            mhx_main.copyShapeKeys("shared/mhx/templates/shapekeys-extra24.mhx", fp, proxy, False)    
            mhx_main.copyShapeKeys("shared/mhx/templates/shapekeys-body25.mhx", fp, proxy, False)    
            writeIpo(fp)
        else:
            fp.write(line)
    tmpl.close()
    return

#
#    exportRawData(obj, fp):    
#
def exportRawData(obj, fp):    
    # Ugly klugdy fix of extra vert
    x1 = aljabr.vadd(obj.verts[11137].co, obj.verts[11140].co)
    x2 = aljabr.vadd(obj.verts[11162].co, obj.verts[11178].co)
    x = aljabr.vadd(x1,x2)
    obj.verts[14637].co = aljabr.vmul(x, 0.25)
    # end ugly kludgy
    for v in obj.verts:
        fp.write("v %.6g %.6g %.6g ;\n" %(v.co[0], v.co[1], v.co[2]))
        
    for uv in obj.uvValues:
        fp.write("vt %.6g %.6g ;\n" %(uv[0], uv[1]))
    faces = mhx_main.loadFacesIndices(obj)
    for f in faces:
        fp.write("f")
        #print(f)
        for v in f:
            fp.write(" %i/%i " %(v[0], v[1]))
        fp.write(";\n")
    

#
#    exportArmature(obj, fp):
#

def exportArmature(obj, fp):
    oldExportArmature24(obj, fp)
    #newExportArmature24(obj, fp)
    return

def oldExportArmature24(obj, fp):
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
#    newExportArmature4(obj, fp):
#
def newExportArmature24(obj, fp):
    mhx_rig.newSetupJoints(obj, classic_bones.ClassicJoints, classic_bones.ClassicHeadsTails, False)

    fp.write(
"\n#if useArmature\n" +
"armature Human Human\n")
    mhx_rig.writeArmature(fp, classic_bones.ClassicArmature + classic_bones.PanelArmature, False)
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
    classic_bones.ClassicWritePoses(fp)
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
"\t\tdriverObject _object['%sMesh' % mhx_main.theHuman] ;\n" +
"\t\tdriverChannel 1 ;\n" +
"\t\tdriverExpression '%s' ;\n" % expr +
"\tend icu\n")

def writeIpo(fp):
    global splitLeftRight

    mhxFile = "shared/mhx/templates/mhxipos.mhx"
    try:
        tmpl = open(mhxFile, "rU")
    except:
        print("*** Cannot open "+mhxFile)
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
        print("    %s copied" % mhxFile)
        tmpl.close()

    return


    