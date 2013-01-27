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

MakeHuman to MHX (MakeHuman eXchange format) exporter. MHX files can be loaded into Blender
"""

MAJOR_VERSION = 1
MINOR_VERSION = 14
BODY_LANGUAGE = True

import module3d
import aljabr
import gui3d
import os
import time
import numpy
import log

#import cProfile

import mh2proxy
import export_config
import armature
import warpmodifier
import posemode
import read_expression

from . import the
from . import mhx_rig
from . import mhx_custom
from . import mhx_24
from . import rig_panel_25
from . import rig_shoulder_25
from . import rig_arm_25
from . import rig_leg_25
from . import rig_body_25



the.Human = 'Human'

#
#    exportMhx(human, filename, options):
#

def exportMhx(human, filename, options):  
    posemode.exitPoseMode()        
    posemode.enterPoseMode()
    config = export_config.exportConfig(human, True, options)
    (fpath, ext) = os.path.splitext(filename)

    if '24' in config.mhxversion:
        mhx_24.exportMhx(human, filename, options, config)
   
    if '25' in config.mhxversion:
        time1 = time.clock()
        fname = os.path.basename(fpath)
        the.Human = fname.capitalize().replace(' ','_')
        outfile = export_config.getOutFileFolder(filename, config)        
        try:
            fp = open(outfile, 'w')
            log.message("Writing MHX 2.5x file %s", outfile )
        except:
            log.message("Unable to open file for writing %s", outfile)
            fp = 0
        if fp:
            #cProfile.runctx( 'exportMhx_25(human, config, fp)', globals(), locals())
            exportMhx_25(human, config, fp)
            fp.close()
            time2 = time.clock()
            log.message("Wrote MHX 2.5x file in %g s: %s", time2-time1, outfile)

    posemode.exitPoseMode()        
    return        

#
#    exportMhx_25(human, config, fp):
#

def exportMhx_25(human, config, fp):
    gui3d.app.progress(0, text="Exporting MHX")
    config.mhx25 = True
    log.message("Export MHX")
    
    fp.write(
"# MakeHuman exported MHX\n" +
"# www.makehuman.org\n" +
"MHX %d %d ;\n" % (MAJOR_VERSION, MINOR_VERSION) +
"#if Blender24\n" +
"  error 'This file can only be read with Blender 2.5' ;\n" +
"#endif\n")

    obj = human.meshData
    proxyData = {}
    scanProxies(obj, config, proxyData)
    mhx_rig.setupRig(obj, config, proxyData)
    
    if not config.cage:
        fp.write(
    "#if toggle&T_Cage\n" +
    "  error 'This MHX file does not contain a cage. Unselect the Cage import option.' ;\n" +
    "#endif\n")

    fp.write(
"NoScale True ;\n" +
"Object CustomShapes EMPTY None\n" +
"  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;\n" +
"end Object\n\n")

    if config.rigtype in ['mhx', 'rigify', 'blenrig']:
        for fname in config.gizmoFiles:
            copyFile25(human, fname, fp, None, config, proxyData)    
        mhx_rig.setupCircles(fp)
    else:
        for (name, data) in config.customShapes.items():
            (typ, r) = data
            if typ == "-circ":
                mhx_rig.setupCircle(fp, name, 0.1*r)
            elif typ == "-box":
                mhx_rig.setupCube(fp, name, 0.1*r, (0,0,0))
            else:
                halt
        """                
        if config.facepanel:
            mhx_rig.setupCube(fp, "MHCube025", 0.25, 0)
            mhx_rig.setupCube(fp, "MHCube05", 0.5, 0)
            copyFile25(human, "shared/mhx/templates/panel_gizmo25.mhx", fp, None, config, proxyData)    
        """            
        
    gui3d.app.progress(0.1, text="Exporting armature")
    copyFile25(human, "shared/mhx/templates/rig-armature25.mhx", fp, None, config, proxyData)    
    
    gui3d.app.progress(0.15, text="Exporting materials")    
    fp.write("\nNoScale False ;\n\n")
    if human.uvset:
        writeMultiMaterials(human.uvset, human, config, fp)
    else:
        copyFile25(human, "shared/mhx/templates/materials25.mhx", fp, None, config, proxyData)    

    if config.cage:
        proxyCopy('Cage', human, config, proxyData, fp, 0.2, 0.25)
    
    gui3d.app.progress(0.25, text="Exporting main mesh")    
    if config.mainmesh:
        fp.write("#if toggle&T_Mesh\n")
        copyFile25(human, "shared/mhx/templates/meshes25.mhx", fp, None, config, proxyData)    
        fp.write("#endif\n")

    proxyCopy('Proxy', human, config, proxyData, fp, 0.35, 0.4)
    proxyCopy('Clothes', human, config, proxyData, fp, 0.4, 0.6)

    copyFile25(human, "shared/mhx/templates/rig-poses25.mhx", fp, None, config, proxyData) 

    if config.rigtype == 'rigify':
        fp.write("Rigify %s ;\n" % the.Human)

    gui3d.app.progress(1.0)
    return

#
#   scanProxies(obj, config, proxyData)
#

def scanProxies(obj, config, proxyData):
    for pfile in config.proxyList:
        if pfile.useMhx and pfile.file:
            proxy = mh2proxy.readProxyFile(obj, pfile, True)
            if proxy:
                proxyData[proxy.name] = proxy        
    return
    
#
#    proxyCopy(type, human, config, proxyData, fp, t0, t1)
#

def proxyCopy(type, human, config, proxyData, fp, t0, t1):
    n = 0
    for proxy in proxyData.values():
        if proxy.type == type:
            n += 1
    if n == 0:
        return
        
    dt = (t1-t0)/n
    t = t0
    for proxy in proxyData.values():
        if proxy.type == type:
            gui3d.app.progress(t, text="Exporting %s" % proxy.name)
            fp.write("#if toggle&T_%s\n" % proxy.type)
            copyFile25(human, "shared/mhx/templates/proxy25.mhx", fp, proxy, config, proxyData)    
            fp.write("#endif\n")
            t += dt
        
#
#    copyFile25(human, tmplName, fp, proxy, config, proxyData):
#

def copyFile25(human, tmplName, fp, proxy, config, proxyData):
    tmpl = open(tmplName)
    if tmpl == None:
        log.error("*** Cannot open %s", tmplName)
        return

    obj = human.meshData
    bone = None
    #faces = loadFacesIndices(obj)
    ignoreLine = False
    for line in tmpl:
        words= line.split()
        if len(words) == 0:
            fp.write(line)
        elif words[0] == '***':
            key = words[1]

            if key == 'refer-human':
                if len(words) > 3:
                    suffix = words[3]
                else:
                    suffix = ""
                fp.write("    %s Refer Object %s%s ;\n" % (words[2], the.Human, suffix))

            elif key == 'rig-bones':
                fp.write("Armature %s %s   Normal \n" % (the.Human, the.Human))
                mhx_rig.writeArmature(fp, config, config.armatureBones)

            elif key == 'human-object':
                if words[2] == 'Mesh':
                    fp.write(
                        "Object %sMesh MESH %sMesh\n"  % (the.Human, the.Human) +
                        "  Property MhxOffsetX %.4f ;\n" % the.Origin[0] +
                        "  Property MhxOffsetY %.4f ;\n" % the.Origin[1] +
                        "  Property MhxOffsetZ %.4f ;\n" % the.Origin[2])
                elif words[2] == 'ControlRig':
                    fp.write(
                        "Object %s ARMATURE %s\n"  % (the.Human, the.Human) +
                        "  Property MhxVersion %d ;\n" % MINOR_VERSION)

            elif key == 'rig-poses':
                fp.write("Pose %s\n" % the.Human)
                mhx_rig.writeControlPoses(fp, config)
                fp.write("  ik_solver 'LEGACY' ;\nend Pose\n")

            elif key == 'rig-actions':
                fp.write("Pose %s\nend Pose\n" % the.Human)
                mhx_rig.writeAllActions(fp, config)

            elif key == 'if-true':
                value = eval(words[2])
                log.debug("if %s %s", words[2], value)
                fp.write("#if %s\n" % value)

            elif key == 'rig-drivers':
                if config.rigtype == "mhx":
                    fp.write("AnimationData %s True\n" % the.Human)
                    mhx_rig.writeAllDrivers(fp, config)
                    rigDriversEnd(fp)

            elif key == 'rig-correct':
                fp.write("CorrectRig %s ;\n" % the.Human)

            elif key == 'recalc-roll':
                if config.rigtype == "mhx":
                    fp.write("  RecalcRoll %s ;\n" % config.recalcRoll)

            elif key == 'ProxyMesh':
                writeProxyMesh(fp, proxy, config, proxyData)

            elif key == 'ProxyObject':
                writeProxyObject(fp, proxy)

            elif key == 'ProxyLayers':
                fp.write("layers Array ")
                for n in range(20):
                    if n == proxy.layer:
                        fp.write("1 ")
                    else:
                        fp.write("0 ")
                fp.write(";\n")

            elif key == 'MeshAnimationData':
                writeHideAnimationData(fp, "", the.Human)

            elif key == 'ProxyAnimationData':
                writeHideAnimationData(fp, the.Human, proxy.name)

            elif key == 'toggleCage':
                if proxy and proxy.cage:
                    fp.write(
                    "  draw_type 'WIRE' ;\n" +
                    "  #if False\n")
                elif config.cage:                    
                    fp.write("  #if toggle&T_Cage\n")
                else:
                    fp.write("  #if False\n")

            elif key == 'ProxyVerts':
                ox = the.Origin[0]
                oy = the.Origin[1]
                oz = the.Origin[2]
                for bary in proxy.realVerts:
                    (x,y,z) = mh2proxy.proxyCoord(bary)
                    fp.write("  v %.4f %.4f %.4f ;\n" % (x-ox, -z+oz, y-oy))

            elif key == 'Verts':
                proxy = None
                fp.write("Mesh %sMesh %sMesh\n  Verts\n" % (the.Human, the.Human))
                ox = the.Origin[0]
                oy = the.Origin[1]
                oz = the.Origin[2]
                for v in obj.verts:
                    fp.write("  v %.4f %.4f %.4f ;\n" % (v.co[0]-ox, -v.co[2]+oz, v.co[1]-oy))

            elif key == 'ProxyFaces':
                for (f,g) in proxy.faces:
                    fp.write("    f")
                    for v in f:
                        fp.write(" %s" % v)
                    fp.write(" ;\n")
                if proxy.faceNumbers:
                    for ftn in proxy.faceNumbers:
                        fp.write(ftn)
                else:
                    fp.write("    ftall 0 1 ;\n")

            elif key == 'Faces':
                for f in obj.faces:
                    fv = f.verts
                    if f.isTriangle():
                        fp.write("    f %d %d %d ;\n" % (fv[0].idx, fv[1].idx, fv[2].idx))
                    else:
                        fp.write("    f %d %d %d %d ;\n" % (fv[0].idx, fv[1].idx, fv[2].idx, fv[3].idx))
                fp.write("#if False\n")

            elif key == 'EndFaces':
                writeFaceNumbers(fp, human, config, proxyData)

            elif key == 'FTTriangles':
                for f in obj.faces:
                    if f.isTriangle():
                        fp.write("    mn %d 1 ;\n" % f.idx)

            elif key == 'ProxyUVCoords':
                layers = list(proxy.uvtexLayerName.keys())
                layers.sort()
                for layer in layers:
                    try:
                        texfaces = proxy.texFacesLayers[layer]
                        texverts = proxy.texVertsLayers[layer]
                    except KeyError:
                        continue
                    fp.write(                   
                        '  MeshTextureFaceLayer %s\n' % proxy.uvtexLayerName[layer] +
                        '    Data \n')
                    for f in texfaces:
                        fp.write("    vt")
                        for v in f:
                            uv = texverts[v]
                            fp.write(" %.4g %.4g" % (uv[0], uv[1]))
                        fp.write(" ;\n")
                    fp.write(
                        '    end Data\n' +
                        '  end MeshTextureFaceLayer\n')

            elif key == 'TexVerts':
                if human.uvset:
                    for ft in human.uvset.texFaces:
                        fp.write("    vt")
                        for vt in ft:
                            uv = human.uvset.texVerts[vt]
                            fp.write(" %.4g %.4g" %(uv[0], uv[1]))
                        fp.write(" ;\n")
                else:
                    for f in obj.faces:
                        uv0 = obj.texco[f.uv[0]]
                        uv1 = obj.texco[f.uv[1]]
                        uv2 = obj.texco[f.uv[2]]
                        if f.isTriangle():
                            fp.write("    vt %.4g %.4g %.4g %.4g %.4g %.4g ;\n" % (uv0[0], uv0[1], uv1[0], uv1[1], uv2[0], uv2[1]))
                        else:
                            uv3 = obj.texco[f.uv[3]]
                            fp.write("    vt %.4g %.4g %.4g %.4g %.4g %.4g %.4g %.4g ;\n" % (uv0[0], uv0[1], uv1[0], uv1[1], uv2[0], uv2[1], uv3[0], uv3[1]))

            elif key == 'Material':
                fp.write("Material %s%s\n" % (the.Human, words[2]))

            elif key == 'Materials':
                writeBaseMaterials(fp, human, config, proxyData)

            elif key == 'ProxyMaterials':
                if proxy.useBaseMaterials:
                    writeBaseMaterials(fp, human, config, proxyData)
                elif proxy.material:
                    fp.write("  Material %s%s ;\n" % (the.Human, proxy.material.name))

            elif key == 'VertexGroup':
                writeVertexGroups(fp, config, proxy)

            elif key == 'group':
                writeGroups(fp, proxyData)

            elif key == 'mesh-shapeKey':
                writeShapeKeys(fp, human, "%sMesh" % the.Human, config, None)

            elif key == 'proxy-shapeKey':
                fp.write("#if toggle&T_Cage\n")
                proxyShapes('Cage', human, config, proxyData, fp)
                fp.write("#endif\n#if toggle&T_Proxy\n")
                proxyShapes('Proxy', human, config, proxyData, fp)
                fp.write("#endif\n#if toggle&T_Clothes\n")
                proxyShapes('Clothes', human, config, proxyData, fp)
                fp.write("#endif\n")

            elif key == 'ProxyModifiers':
                writeProxyModifiers(fp, proxy)

            elif key == 'MTex':
                n = nMasks + int(words[2])
                fp.write("  MTex %d %s %s %s\n" % (n, words[3], words[4], words[5]))

            elif key == 'SkinStart':
                nMasks = writeSkinStart(fp, proxy, config, proxyData)

            elif key == 'curves':
                mhx_rig.writeAllCurves(fp, config)

            elif key == 'properties':
                mhx_rig.writeAllProperties(fp, words[2], config)
                writeHideProp(fp, the.Human)
                for proxy in proxyData.values():
                    writeHideProp(fp, proxy.name)
                if config.customshapes: 
                    mhx_custom.listCustomFiles(config)                            
                for path,name in config.customShapeFiles:
                    fp.write("  DefProp Float %s 0 %s  min=-1.0,max=2.0 ;\n" % (name, name[3:]))

            elif key == 'material-drivers':
                fp.write("  use_textures Array")
                for n in range(nMasks):
                    fp.write(" 1")
                for n in range(3):
                    fp.write(" 1")
                fp.write(" ;\n")
                fp.write("  AnimationData %sMesh True\n" % the.Human)
                #armature.drivers.writeTextureDrivers(fp, rig_panel_25.BodyLanguageTextureDrivers)
                writeMaskDrivers(fp, config, proxyData)
                fp.write("  end AnimationData\n")

            elif key == 'Filename':
                file = export_config.getOutFileName(words[2], words[3], True, human, config)
                fp.write("  Filename %s ;\n" % file)

            else:
                raise NameError("Unknown *** %s" % words[1])
        else:
            fp.write(line)

    log.message("    %s copied", tmplName)
    tmpl.close()

    return

#
#   writeFaceNumbers(fp, human, config, proxyData):
#

MaterialNumbers = {
    ""       : 0,     # skin
    "skin"   : 0,     # skin
    "nail"   : 0,     # nail
    "teeth"  : 1,     # teeth
    "eye"    : 2,     # eye
    "cornea" : 2,     # cornea
    "brow"   : 3,     # brows
    "joint"  : 4,     # joint
    "red"    : 5,     # red
    "green"  : 6,     # green
    "blue"   : 7      # blue
}
    
def writeFaceNumbers(fp, human, config, proxyData):
    fp.write("#else\n")
    if human.uvset:
        for ftn in human.uvset.faceNumbers:
            fp.write(ftn)
    else:            
        obj = human.meshData
        fmats = {}
        print(obj.materials.items)
        for fn,mtl in obj.materials.items():
            fmats[fn] = MaterialNumbers[mtl]
            
        if config.hidden:
            deleteVerts = None
            deleteGroups = []
        else:
            deleteGroups = []
            deleteVerts = numpy.zeros(len(obj.verts), bool)
            for proxy in proxyData.values():
                deleteGroups += proxy.deleteGroups
                deleteVerts = deleteVerts | proxy.deleteVerts
                    
        for fg in obj.faceGroups: 
            if mh2proxy.deleteGroup(fg.name, deleteGroups):
                for f in fg.faces:
                    fmats[f.idx] = 6
            elif "joint" in fg.name:
                for f in fg.faces:
                    fmats[f.idx] = 4
            elif fg.name == "helper-tights":                    
                for f in fg.faces:
                    fmats[f.idx] = 5
            elif fg.name == "helper-skirt":                    
                for f in fg.faces:
                    fmats[f.idx] = 7
            elif ("tongue" in fg.name):
                for f in fg.faces:
                    fmats[f.idx] = 1
            elif ("eyebrown" in fg.name) or ("lash" in fg.name):
                for f in fg.faces:
                    fmats[f.idx] = 3   
                    
        if deleteVerts != None:
            for f in obj.faces:
                v = f.verts[0]
                if deleteVerts[v.idx]:
                    fmats[f.idx] = 6                        
                
        mn = -1
        fn = 0
        f0 = 0
        for f in obj.faces:
            if fmats[fn] != mn:
                if fn != f0:
                    fp.write("  ftn %d %d 1 ;\n" % (fn-f0, mn))
                mn = fmats[fn]
                f0 = fn
            fn += 1
        if fn != f0:
            fp.write("  ftn %d %d 1 ;\n" % (fn-f0, mn))
    fp.write("#endif\n")

#
#   writeBaseMaterials(fp, human, config, proxyData):                    
#

def writeBaseMaterials(fp, human, config, proxyData):      
    if human.uvset:
        for mat in human.uvset.materials:
            fp.write("  Material %s_%s ;\n" % (the.Human, mat.name))
    else:
        fp.write(
"  Material %sSkin ;\n" % the.Human +
"  Material %sMouth ;\n" % the.Human +
"  Material %sEye ;\n" % the.Human +
"  Material %sBrows ;\n" % the.Human +
"  Material %sInvisio ;\n" % the.Human +
"  Material %sRed ;\n" % the.Human +
"  Material %sGreen ;\n" % the.Human +
"  Material %sBlue ;\n" % the.Human
)
    
def addMaskImage(fp, config, mask):            
    (folder, file) = mask
    path = export_config.getOutFileName(file, folder, True, None, config)
    fp.write(
"Image %s\n" % file +
"  Filename %s ;\n" % path +
"  alpha_mode 'PREMUL' ;\n" +
"end Image\n\n" +
"Texture %s IMAGE\n" % file  +
"  Image %s ;\n" % file +
"end Texture\n\n")
    return
    
def addMaskMTex(fp, mask, proxy, blendtype, n):            
    if proxy:
        try:
            uvLayer = proxy.uvtexLayerName[proxy.maskLayer]
        except KeyError:
            return n

    (dir, file) = mask
    fp.write(
"  MTex %d %s UV ALPHA\n" % (n, file) +
"    texture Refer Texture %s ;\n" % file +
"    use_map_alpha True ;\n" +
"    use_map_color_diffuse False ;\n" +
"    alpha_factor 1 ;\n" +
"    blend_type '%s' ;\n" % blendtype +
"    mapping 'FLAT' ;\n" +
"    invert True ;\n" +
"    use_stencil True ;\n" +
"    use_rgb_to_intensity True ;\n")
    if proxy:
        fp.write("    uv_layer '%s' ;\n" %  uvLayer)
    fp.write("  end MTex\n")
    return n+1

#
#   writeSkinStart(fp, proxy, config, proxyData)
#

def writeSkinStart(fp, proxy, config, proxyData):
    if not config.usemasks:
        fp.write("Material %sSkin\n" % the.Human)
        return 0
        
    if proxy:
        fp.write("Material %s%sSkin\n" % (the.Human, proxy.name))
        return 0

    nMasks = 0
    prxList = list(proxyData.values())
    
    for prx in prxList:
        if prx.mask:
            addMaskImage(fp, config, prx.mask)
            nMasks += 1
    fp.write("Material %sSkin\n" % the.Human)
             #"  MTex 0 diffuse UV COLOR\n" +
             #"    texture Refer Texture diffuse ;\n" +
             #"  end MTex\n"

    n = 0    
    for prx in prxList:
        if prx.mask:
            n = addMaskMTex(fp, prx.mask, proxy, 'MULTIPLY', n)
            
    return nMasks
               
def writeMaskDrivers(fp, config, proxyData):
    if not config.usemasks:
        return
    fp.write("#if toggle&T_Clothes\n")
    n = 0
    for prx in proxyData.values():
        if prx.type == 'Clothes' and prx.mask:
            (dir, file) = prx.mask
            armature.drivers.writePropDriver(fp, ["Mhh%s" % prx.name], "1-x1", 'use_textures', n)
            n += 1            
    fp.write("#endif\n")
    return
    
#
#   writeVertexGroups(fp, config, proxy):                
#

def writeVertexGroups(fp, config, proxy):                
    if proxy and proxy.weights:
        writeRigWeights(fp, proxy.weights)
        return

    if config.vertexWeights:
        if proxy:
            weights = mh2proxy.getProxyWeights(config.vertexWeights, proxy)
        else:
            weights = config.vertexWeights                    
        writeRigWeights(fp, weights)
    else:
        for file in config.vertexGroupFiles:
            copyVertexGroups(file, fp, proxy)
            
    #for path in config.customvertexgroups:
    #    print("    %s" % path)
    #    copyVertexGroups(path, fp, proxy)    

    if config.cage and not (proxy and proxy.cage):
        fp.write("#if toggle&T_Cage\n")
        copyVertexGroups("cage", fp, proxy)    
        fp.write("#endif\n")

    copyVertexGroups("leftright", fp, proxy)    
    copyVertexGroups("tight-leftright", fp, proxy)    
    copyVertexGroups("skirt-leftright", fp, proxy)    
    return
    
#
#    rigDriversEnd(fp):                                        
#

def rigDriversEnd(fp):                                        
    fp.write(
"  action_blend_type 'REPLACE' ;\n" +
"  action_extrapolation 'HOLD' ;\n" +
"  action_influence 1 ;\n" +
"  use_nla True ;\n" +
"end AnimationData\n")

#
#   writeGroups(fp, proxyData):                
#   groupProxy(typ, fp, proxyData):
#

def writeGroups(fp, proxyData):                
    fp.write(
"PostProcess %sMesh %s 0000003f 00080000 0068056b 0000c000 ;\n" % (the.Human, the.Human) + 
"Group %s\n"  % the.Human +
"  Objects\n" +
"    ob %s ;\n" % the.Human +
"#if toggle&T_Mesh\n" +
"    ob %sMesh ;\n" % the.Human +
"#endif\n")
    groupProxy('Cage', fp, proxyData)
    groupProxy('Proxy', fp, proxyData)
    groupProxy('Clothes', fp, proxyData)
    fp.write(
"    ob CustomShapes ;\n" + 
"  end Objects\n" +
"  layers Array 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  ;\n" +
"end Group\n")
    return
    
def groupProxy(typ, fp, proxyData):
    fp.write("#if toggle&T_%s\n" % typ)
    for proxy in proxyData.values():
        if proxy.type == typ:
            name = the.Human + proxy.name
            fp.write("    ob %sMesh ;\n" % name)
    fp.write("#endif\n")
    return

#
#   writeProxyMesh(fp, proxy, config, proxyData):                
#

def writeProxyMesh(fp, proxy, config, proxyData):                
    mat = proxy.material
    if mat:
        if proxy.material_file:
            copyProxyMaterialFile(fp, proxy.material_file, mat, proxy, config, proxyData)
        else:
            writeProxyMaterial(fp, mat, proxy, config, proxyData)
    name = the.Human + proxy.name
    fp.write("Mesh %sMesh %sMesh \n" % (name, name))
    return

#
#   writeProxyObject(fp, proxy):                
#

def writeProxyObject(fp, proxy): 
    name = the.Human + proxy.name
    fp.write(
    "Object %sMesh MESH %sMesh \n" % (name, name) +
    "  parent Refer Object %s ;\n" % the.Human +
    "  hide False ;\n" +
    "  hide_render False ;\n")
    if proxy.wire:
        fp.write("  draw_type 'WIRE' ;\n")    
    return

#
#   writeProxyModifiers(fp, proxy):
#

def writeProxyModifiers(fp, proxy):
    for mod in proxy.modifiers:
        if mod[0] == 'subsurf':
            fp.write(
"    Modifier SubSurf SUBSURF\n" +
"      levels %d ;\n" % mod[1] +
"      render_levels %d ;\n" % mod[2] +
"    end Modifier\n")
        elif mod[0] == 'shrinkwrap':
            offset = mod[1]
            fp.write(
"    Modifier ShrinkWrap SHRINKWRAP\n" +
"      target Refer Object %sMesh ;\n" % the.Human +
"      offset %.4f ;\n" % offset +
"      use_keep_above_surface True ;\n" +
"    end Modifier\n")
        elif mod[0] == 'solidify':
            thickness = mod[1]
            offset = mod[2]
            fp.write(
"    Modifier Solidify SOLIDIFY\n" +
"      thickness %.4f ;\n" % thickness +
"      offset %.4f ;\n" % offset +
"    end Modifier\n")
    return

#
#   writeHideProp(fp, name):                
#   writeHideAnimationData(fp, prefix, name):
#

def writeHideProp(fp, name):                
    fp.write("  DefProp Bool Mhh%s False Control_%s_visibility ;\n" % (name, name))
    return

def writeHideAnimationData(fp, prefix, name):
    fp.write("AnimationData %s%sMesh True\n" % (prefix, name))
    armature.drivers.writePropDriver(fp, ["Mhh%s" % name], "x1", "hide", -1)
    armature.drivers.writePropDriver(fp, ["Mhh%s" % name], "x1", "hide_render", -1)
    fp.write("end AnimationData\n")
    return    
       
#
#   copyProxyMaterialFile(fp, pair, mat, proxy, config, proxyData):
#

def copyProxyMaterialFile(fp, pair, mat, proxy, config, proxyData):
    prxList = sortedMasks(config, proxyData)
    nMasks = countMasks(proxy, prxList)
    tex = None
    
    (folder, file) = pair
    folder = os.path.realpath(os.path.expanduser(folder))
    infile = os.path.join(folder, file)
    tmpl = open(infile, "rU")
    for line in tmpl:
        words= line.split()
        if len(words) == 0:
            fp.write(line)
        elif words[0] == 'Texture':
            words[1] = the.Human + words[1]
            for word in words:
                fp.write("%s " % word)
            fp.write("\n")
            tex = os.path.join(folder,words[1])
        elif words[0] == 'Material':
            words[1] = the.Human + words[1]
            for word in words:
                fp.write("%s " % word)
            fp.write("\n")
            addProxyMaskMTexs(fp, mat, proxy, prxList, tex)
        elif words[0] == 'MTex':
            words[2] = the.Human + words[2]
            for word in words:
                fp.write("%s " % word)
            fp.write("\n")                
        elif words[0] == 'Filename':
            file = export_config.getOutFileName(words[1], folder, True, None, config)
            fp.write("  Filename %s ;\n" % file)
        else:
            fp.write(line)
    tmpl.close()
    return
       
#
#   writeProxyMaterial(fp, mat, proxy, config, proxyData):
#

def writeProxyTexture(fp, texture, mat, extra, config):        
    (folder,name) = texture
    tex = os.path.join(folder,name)
    #print(the.Human)
    log.debug("Tex %s", tex)
    texname = the.Human + os.path.basename(tex)
    fromDir = os.path.dirname(tex)
    texfile = export_config.getOutFileName(tex, fromDir, True, None, config)
    fp.write(
"Image %s\n" % texname +
"  Filename %s ;\n" % texfile +
"  alpha_mode 'PREMUL' ;\n" +
"end Image\n\n" +
"Texture %s IMAGE\n" % texname +
"  Image %s ;\n" % texname)
    writeProxyMaterialSettings(fp, mat.textureSettings)             
    fp.write(extra)
    fp.write("end Texture\n\n")
    return (tex, texname)
    
def writeProxyMaterial(fp, mat, proxy, config, proxyData):
    alpha = mat.alpha
    tex = None
    bump = None
    normal = None
    displacement = None
    transparency = None
    if proxy.texture:
        uuid = proxy.getUuid()
        human = gui3d.app.selectedHuman
        if uuid in human.clothesObjs.keys() and human.clothesObjs[uuid]:
            # Apply custom texture
            clothesObj = human.clothesObjs[uuid]
            texture = clothesObj.mesh.texture
            texPath = (os.path.dirname(texture), os.path.basename(texture))
            (tex,texname) = writeProxyTexture(fp, texPath, mat, "", config)
        else:
            (tex,texname) = writeProxyTexture(fp, proxy.texture, mat, "", config)
    if proxy.bump:
        (bump,bumpname) = writeProxyTexture(fp, proxy.bump, mat, "", config)
    if proxy.normal:
        (normal,normalname) = writeProxyTexture(fp, proxy.normal, mat, 
            ("    use_normal_map True ;\n"),
            config)
    if proxy.displacement:
        (displacement,dispname) = writeProxyTexture(fp, proxy.displacement, mat, "", config)
    if proxy.transparency:
        (transparency,transname) = writeProxyTexture(fp, proxy.transparency, mat, "", config)
           
    prxList = sortedMasks(config, proxyData)
    nMasks = countMasks(proxy, prxList)
    slot = nMasks
    
    fp.write("Material %s%s \n" % (the.Human, mat.name))
    addProxyMaskMTexs(fp, mat, proxy, prxList, tex)
    writeProxyMaterialSettings(fp, mat.settings)   
    uvlayer = proxy.uvtexLayerName[proxy.textureLayer]

    if tex:
        fp.write(
"  MTex %d %s UV COLOR\n" % (slot, texname) +
"    texture Refer Texture %s ;\n" % texname +
"    use_map_alpha True ;\n" +
"    diffuse_color_factor 1.0 ;\n" +
"    uv_layer '%s' ;\n" % uvlayer)
        writeProxyMaterialSettings(fp, mat.mtexSettings)             
        fp.write("  end MTex\n")
        slot += 1
        alpha = 0
        
    if bump:
        fp.write(
"  MTex %d %s UV NORMAL\n" % (slot, bumpname) +
"    texture Refer Texture %s ;\n" % bumpname +
"    use_map_normal True ;\n" +
"    use_map_color_diffuse False ;\n" +
"    normal_factor %.3f ;\n" % proxy.bumpStrength + 
"    use_rgb_to_intensity True ;\n" +
"    uv_layer '%s' ;\n" % uvlayer +
"  end MTex\n")
        slot += 1
        
    if normal:
        fp.write(
"  MTex %d %s UV NORMAL\n" % (slot, normalname) +
"    texture Refer Texture %s ;\n" % normalname +
"    use_map_normal True ;\n" +
"    use_map_color_diffuse False ;\n" +
"    normal_factor %.3f ;\n" % proxy.normalStrength + 
"    normal_map_space 'TANGENT' ;\n" +
"    uv_layer '%s' ;\n" % uvlayer +
"  end MTex\n")
        slot += 1
        
    if displacement:
        fp.write(
"  MTex %d %s UV DISPLACEMENT\n" % (slot, dispname) +
"    texture Refer Texture %s ;\n" % dispname +
"    use_map_displacement True ;\n" +
"    use_map_color_diffuse False ;\n" +
"    displacement_factor %.3f ;\n" % proxy.dispStrength + 
"    use_rgb_to_intensity True ;\n" +
"    uv_layer '%s' ;\n" % uvlayer +
"  end MTex\n")
        slot += 1

    if transparency:        
        fp.write(
"  MTex %d %s UV ALPHA\n" % (slot, transname) +
"    texture Refer Texture %s ;\n" % transname +
"    use_map_alpha True ;\n" +
"    use_map_color_diffuse False ;\n" +
"    invert True ;\n" +
"    use_stencil True ;\n" +
"    use_rgb_to_intensity True ;\n" +
"    uv_layer '%s' ;\n" % uvlayer +
"  end MTex\n")
        slot += 1        
        
    if nMasks > 0 or alpha < 0.99:
        fp.write(
"  use_transparency True ;\n" +
"  transparency_method 'Z_TRANSPARENCY' ;\n" +
"  alpha %3.f ;\n" % alpha +
"  specular_alpha %.3f ;\n" % alpha)
    if mat.mtexSettings == []:
        fp.write(
"  use_shadows True ;\n" +
"  use_transparent_shadows True ;\n")
    fp.write(
"  Property MhxDriven True ;\n" +
"end Material\n\n")

def writeProxyMaterialSettings(fp, settings):
    for (key, value) in settings:        
        if type(value) == list:
            fp.write("  %s Array %.4f %.4f %.4f ;\n" % (key, value[0], value[1], value[2]))
        elif type(value) == float:
            fp.write("  %s %.4f ;\n" % (key, value))
        elif type(value) == int:
            fp.write("  %s %d ;\n" % (key, value))
        else:
            fp.write("  %s '%s' ;\n" % (key, value))

def addProxyMaskMTexs(fp, mat, proxy, prxList, tex):
    n = 0  
    m = len(prxList)
    for (zdepth, prx) in prxList:
        m -= 1
        if zdepth > proxy.z_depth:
            n = addMaskMTex(fp, prx.mask, proxy, 'MULTIPLY', n)
    if not tex:            
        n = addMaskMTex(fp, (None,'solid'), proxy, 'MIX', n)
    return   
    
def sortedMasks(config, proxyData):
    if not config.usemasks:
        return []
    prxList = []
    for prx in proxyData.values():
        if prx.type == 'Clothes' and prx.mask:
            prxList.append((prx.z_depth, prx))
    prxList.sort()
    return prxList
    
def countMasks(proxy, prxList):
    n = 0
    for (zdepth, prx) in prxList:
        if prx.type == 'Clothes' and zdepth > proxy.z_depth:
            n += 1
    return n            

#
#    copyVertexGroups(name, fp, proxy):
#

def getVertexGroups(name, vgroups):
    file = os.path.join("shared/mhx/vertexgroups", name + ".vgrp")
    fp = open(file, "rU")
    vgroupList = []
    for line in fp:
        words = line.split()
        if len(words) < 2:
            continue
        elif words[1] == "weights":
            name = words[2]
            try:
                vgroup = vgroups[name]
            except KeyError:
                vgroup = []
                vgroups[name] = vgroup 
            vgroupList.append((name, vgroup))
        else:
            vgroup.append((int(words[0]), float(words[1])))
    fp.close()            
    return vgroupList            


def copyVertexGroups(name, fp, proxy):
    vgroupList = getVertexGroups(name, {})
    if not proxy:
        for (name, weights) in vgroupList:
            fp.write("  VertexGroup %s\n" % name)
            for (v,wt) in weights:
                fp.write("    wv %d %.4g ;\n" % (v,wt))
            fp.write("  end VertexGroup\n\n")
    else:
        for (name, weights) in vgroupList:
            pgroup = []
            for (v,wt) in weights:
                try:
                    vlist = proxy.verts[v]
                except:
                    vlist = []
                for (pv, w) in vlist:
                    pw = w*wt
                    if pw > 1e-4:
                        pgroup.append((pv, pw))
            if pgroup:
                fp.write("  VertexGroup %s\n" % name)
                printProxyVGroup(fp, pgroup)
                fp.write("  end VertexGroup\n\n")
    
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
#    writeShapeKeys(fp, human, name, config, proxy):
#

def writeCorrectives(fp, human, drivers, folder, landmarks, proxy, t0, t1):    
    shapeList = read_expression.readCorrectives(drivers, human, folder, landmarks, t0, t1)
    for (shape, pose, lr) in shapeList:
        writeShape(fp, pose, lr, shape, 0, 1, proxy)
    

def writeShape(fp, pose, lr, shape, min, max, proxy):
    fp.write(
        "ShapeKey %s %s True\n" % (pose, lr) +
        "  slider_min %.3g ;\n" % min +
        "  slider_max %.3g ;\n" % max)
    if proxy:
        pshape = mh2proxy.getProxyShapes([("shape",shape)], proxy)
        for (pv, dr) in pshape[0].items():
            (dx, dy, dz) = dr
            fp.write("  sv %d %.4f %.4f %.4f ;\n" %  (pv, dx, -dz, dy))
    else:
        for (vn, dr) in shape.items():
           fp.write("  sv %d %.4f %.4f %.4f ;\n" %  (vn, dr[0], -dr[2], dr[1]))
    fp.write("end ShapeKey\n")


def writeShapeKeys(fp, human, name, config, proxy):
    fp.write(
"#if toggle&T_Shapekeys\n" +
"ShapeKeys %s\n" % name +
"  ShapeKey Basis Sym True\n" +
"  end ShapeKey\n")

    """
    if (not proxy or proxy.type == 'Proxy'):        
        if config.faceshapes:
            shapeList = read_expression.readFaceShapes(human, rig_panel_25.BodyLanguageShapeDrivers, 0.6, 0.7)
            for (pose, shape, lr, min, max) in shapeList:
                writeShape(fp, pose, lr, shape, min, max, proxy)
    """
    
    if not proxy:
        if config.expressionunits:
            shapeList = read_expression.readExpressionUnits(human, 0.7, 0.9)
            for (pose, shape) in shapeList:
                writeShape(fp, pose, "Sym", shape, -1, 2, proxy)
        
    if config.bodyshapes and config.rigtype == "mhx":
        writeCorrectives(fp, human, rig_shoulder_25.ShoulderTargetDrivers, "shoulder", "shoulder", proxy, 0.88, 0.90)                
        writeCorrectives(fp, human, rig_leg_25.HipTargetDrivers, "hips", "hips", proxy, 0.90, 0.92)                
        writeCorrectives(fp, human, rig_arm_25.ElbowTargetDrivers, "elbow", "body", proxy, 0.92, 0.94)                
        writeCorrectives(fp, human, rig_leg_25.KneeTargetDrivers, "knee", "knee", proxy, 0.94, 0.96)                

    if not proxy:
        for path,name in config.customShapeFiles:
            log.message("    %s", path)
            shape = mhx_custom.readCustomTarget(path)
            writeShape(fp, name, "Sym", shape, -1, 2, proxy)                        

    fp.write(
"  AnimationData None (toggle&T_Symm==0)\n")
        
    if config.bodyshapes and config.rigtype == "mhx":
        armature.drivers.writeTargetDrivers(fp, rig_shoulder_25.ShoulderTargetDrivers, the.Human)
        armature.drivers.writeTargetDrivers(fp, rig_leg_25.HipTargetDrivers, the.Human)
        armature.drivers.writeTargetDrivers(fp, rig_arm_25.ElbowTargetDrivers, the.Human)
        armature.drivers.writeTargetDrivers(fp, rig_leg_25.KneeTargetDrivers, the.Human)

        armature.drivers.writeRotDiffDrivers(fp, rig_arm_25.ArmShapeDrivers, proxy)
        armature.drivers.writeRotDiffDrivers(fp, rig_leg_25.LegShapeDrivers, proxy)
        #armature.drivers.writeShapePropDrivers(fp, rig_body_25.BodyShapes, proxy, "Mha")

    fp.write("#if toggle&T_ShapeDrivers\n")

    if not proxy:
        for path,name in config.customShapeFiles:
            armature.drivers.writeShapePropDrivers(fp, [name], proxy, "")    

    if not proxy:
        if config.expressionunits:
            armature.drivers.writeShapePropDrivers(fp, read_expression.ExpressionUnits, proxy, "Mhs")
            
        skeys = []
        for (skey, val, string, min, max) in  config.customProps:
            skeys.append(skey)
        armature.drivers.writeShapePropDrivers(fp, skeys, proxy, "Mha")    
    fp.write("#endif\n")
        
    fp.write(
"  end AnimationData\n\n")

    if config.expressionunits and not proxy:
        exprList = read_expression.readExpressionMhm("data/expressions")
        writeExpressions(fp, exprList, "Expression")        
        visemeList = read_expression.readExpressionMhm("data/visemes")
        writeExpressions(fp, visemeList, "Viseme")        

    fp.write(
        "  end ShapeKeys\n" +
        "#endif\n")
    return    


def writeExpressions(fp, exprList, label):
    for (name, units) in exprList:
        fp.write("  %s %s\n" % (label, name))
        for (unit, value) in units:
            fp.write("    %s %s ;\n" % (unit, value))
        fp.write("  end\n")
            

def proxyShapes(typ, human, config, proxyData, fp):
    fp.write("#if toggle&T_%s\n" % typ)
    for proxy in proxyData.values():
        if proxy.name and proxy.type == typ:
            writeShapeKeys(fp, human, the.Human+proxy.name+"Mesh", config, proxy)
    fp.write("#endif\n")
        
#
#   writeMultiMaterials(uvset, human, config, fp):
#
      
TX_SCALE = 1
TX_BW = 2

TexInfo = {
    "diffuse" :     ("COLOR", "use_map_color_diffuse", "diffuse_color_factor", 0),
    "specular" :    ("SPECULAR", "use_map_specular", "specular_factor", TX_BW),
    "alpha" :       ("ALPHA", "use_map_alpha", "alpha_factor", TX_BW),
    "translucency": ("TRANSLUCENCY", "use_map_translucency", "translucency_factor", TX_BW),
    "bump" :        ("NORMAL", "use_map_normal", "normal_factor", TX_SCALE|TX_BW),
    "displacement": ("DISPLACEMENT", "use_map_displacement", "displacement_factor", TX_SCALE|TX_BW),
}    

def writeMultiMaterials(uvset, human, config, fp):
    folder = os.path.dirname(human.uvset.filename)
    log.debug("Folder %s", folder)
    for mat in uvset.materials:
        for tex in mat.textures:
            name = os.path.basename(tex.file)
            fp.write("Image %s\n" % name)
            #file = export_config.getOutFileName(tex, "data/textures", True, human, config)
            file = export_config.getOutFileName(name, folder, True, human, config)
            fp.write(
                "  Filename %s ;\n" % file +
                "  alpha_mode 'PREMUL' ;\n" +
                "end Image\n\n" +
                "Texture %s IMAGE\n" % name +
                "  Image %s ;\n" % name +
                "end Texture\n\n")
            
        fp.write("Material %s_%s\n" % (the.Human, mat.name))
        alpha = False
        for (key, value) in mat.settings:
            if key == "alpha":
                alpha = True
                fp.write(
                "  use_transparency True ;\n" +
                "  use_raytrace False ;\n" +
                "  use_shadows False ;\n" +
                "  use_transparent_shadows False ;\n" +
                "  alpha %s ;\n" % value)
            elif key in ["diffuse_color", "specular_color"]:
                fp.write("  %s Array %s %s %s ;\n" % (key, value[0], value[1], value[2]))
            elif key in ["diffuse_intensity", "specular_intensity"]:
                fp.write("  %s %s ;\n" % (key, value))
        if not alpha:
            fp.write("  use_transparent_shadows True ;\n")
                
        n = 0
        for tex in mat.textures:
            name = os.path.basename(tex.file)
            if len(tex.types) > 0:
                (key, value) = tex.types[0]
            else:
                (key, value) = ("diffuse", "1")
            (type, use, factor, flags) = TexInfo[key]
            diffuse = False
            fp.write(
                "  MTex %d %s UV %s\n" % (n, name, type) +
                "    texture Refer Texture %s ;\n" % name)            
            for (key, value) in tex.types:
                (type, use, factor, flags) = TexInfo[key]
                if flags & TX_SCALE:
                    scale = "*theScale"
                else:
                    scale = ""
                fp.write(
                "    %s True ;\n" % use +
                "    %s %s%s ;\n" % (factor, value, scale))
                if flags & TX_BW:
                    fp.write("    use_rgb_to_intensity True ;\n")
                if key == "diffuse":
                    diffuse = True
            if not diffuse:
                fp.write("    use_map_color_diffuse False ;\n")
            fp.write("  end MTex\n")
            n += 1
        fp.write("end Material\n\n")
    
#
#    writeRigWeights(fp, weights):
#

def writeRigWeights(fp, weights):
    for grp in weights.keys():
        fp.write("\n  VertexGroup %s\n" % grp)
        for (v,w) in weights[grp]:
            fp.write("    wv %d %.4f ;\n" % (v,w))
        fp.write("  end VertexGroup\n")
    return
    


