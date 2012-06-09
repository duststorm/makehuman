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
MakeHuman to MHX (MakeHuman eXchange format) exporter. MHX files can be loaded into Blender

"""

MAJOR_VERSION = 1
MINOR_VERSION = 13
BODY_LANGUAGE = True

import module3d
import aljabr
import mh
import mh2bvh
import os
import time

import mh2proxy
import export_config
import mhx_globals as the
import mhx_24
import mhx_rig
import rig_panel_25
import rig_shoulder_25
import rig_arm_25
import rig_leg_25
import rig_body_25
import read_expression
import read_rig

the.Human = 'Human'

#
#    exportMhx(human, filename, options):
#

def exportMhx(human, filename, options):    
    the.Config = export_config.exportConfig(human, True, options)
    (fpath, ext) = os.path.splitext(filename)

    if '24' in the.Config.mhxversion:
        mhx_24.exportMhx(human, filename, options)
   
    if '25' in the.Config.mhxversion:
        time1 = time.clock()
        fname = os.path.basename(fpath)
        the.Human = fname.capitalize().replace(' ','_')
        outfile = export_config.getOutFileFolder(filename, the.Config)        
        try:
            fp = open(outfile, 'w')
            export_config.safePrint("Writing MHX 2.5x file",  outfile )
        except:
            export_config.safePrint("Unable to open file for writing", outfile)
            fp = 0
        if fp:
            exportMhx_25(human, fp)
            fp.close()
            time2 = time.clock()
            export_config.safePrint("Wrote MHX 2.5x file in %g s:" % (time2-time1), outfile)

    return        

#
#    exportMhx_25(human, fp):
#

def exportMhx_25(human, fp):
    fp.write(
"# MakeHuman exported MHX\n" +
"# www.makehuman.org\n" +
"MHX %d %d ;\n" % (MAJOR_VERSION, MINOR_VERSION) +
"#if Blender24\n" +
"  error 'This file can only be read with Blender 2.5' ;\n" +
"#endif\n")

    obj = human.meshData
    proxyData = {}
    scanProxies(obj, proxyData)
    mhx_rig.setupRig(obj, proxyData)
    
    if not the.Config.cage:
        fp.write(
    "#if toggle&T_Cage\n" +
    "  error 'This MHX file does not contain a cage. Unselect the Cage import option.' ;\n" +
    "#endif\n")

    fp.write(
"NoScale True ;\n" +
"Object CustomShapes EMPTY None\n" +
"  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;\n" +
"end Object\n\n")

    fp.write("#if toggle&T_Armature\n")
    if the.Config.mhxrig in ['mhx', 'rigify', 'blenrig']:
        for fname in the.GizmoFiles:
            copyFile25(human, fname, fp, None, proxyData)    
        mhx_rig.setupCircles(fp)
    else:
        for (name, data) in the.CustomShapes.items():
            (typ, r) = data
            if typ == "-circ":
                mhx_rig.setupCircle(fp, name, 0.1*r)
            elif typ == "-box":
                mhx_rig.setupCube(fp, name, 0.1*r, (0,0,0))
            else:
                halt
        if the.Config.facepanel:
            mhx_rig.setupCube(fp, "MHCube025", 0.25, 0)
            mhx_rig.setupCube(fp, "MHCube05", 0.5, 0)
            copyFile25(human, "shared/mhx/templates/panel_gizmo25.mhx", fp, None, proxyData)    
            
    copyFile25(human, "shared/mhx/templates/rig-armature25.mhx", fp, None, proxyData)    
    fp.write("#endif\n")
    
    fp.write("\nNoScale False ;\n\n")

    if human.uvsetFile:
        uvset = mh2proxy.readUvset(human.uvsetFile)
        proxyData["__uvset__"] = uvset
        writeMultiMaterials(uvset, human, fp)
    else:
        copyFile25(human, "shared/mhx/templates/materials25.mhx", fp, None, proxyData)    

    if the.Config.cage:
        proxyCopy('Cage', human, proxyData, fp)
    
    if the.Config.mainmesh:
        fp.write("#if toggle&T_Mesh\n")
        copyFile25(human, "shared/mhx/templates/meshes25.mhx", fp, None, proxyData)    
        fp.write("#endif\n")

    proxyCopy('Proxy', human, proxyData, fp)
    proxyCopy('Clothes', human, proxyData, fp)

    copyFile25(human, "shared/mhx/templates/rig-poses25.mhx", fp, None, proxyData) 

    if the.Config.mhxrig == 'rigify':
        fp.write("Rigify %s ;\n" % the.Human)
    return

#
#   scanProxies(obj, proxyData)
#

def scanProxies(obj, proxyData):
    for pfile in the.Config.proxyList:
        if pfile.useMhx and pfile.file:
            proxy = mh2proxy.readProxyFile(obj, pfile, True)
            if proxy:
                proxyData[proxy.name] = proxy        
    return
    
#
#    proxyCopy(name, human, proxyData, fp)
#

def proxyCopy(name, human, proxyData, fp):
    for proxy in proxyData.values():
        if proxy.type == name:
            fp.write("#if toggle&T_%s\n" % proxy.type)
            copyFile25(human, "shared/mhx/templates/proxy25.mhx", fp, proxy, proxyData)    
            fp.write("#endif\n")
        
#
#    copyFile25(human, tmplName, fp, proxy, proxyData):
#

def copyFile25(human, tmplName, fp, proxy, proxyData):
    tmpl = open(tmplName)
    if tmpl == None:
        print("*** Cannot open "+tmplName)
        return

    obj = human.meshData
    bone = None
    faces = loadFacesIndices(obj)
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
                mhx_rig.writeArmature(fp, the.Armature, True)
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
                mhx_rig.writeControlPoses(fp)
                fp.write("  ik_solver 'LEGACY' ;\nend Pose\n")
            elif key == 'rig-actions':
                fp.write("Pose %s\nend Pose\n" % the.Human)
                mhx_rig.writeAllActions(fp)
            elif key == 'if-true':
                value = eval(words[2])
                print "if", words[2], value
                fp.write("#if %s\n" % value)
            elif key == 'rig-drivers':
                fp.write("AnimationData %s True\n" % the.Human)
                mhx_rig.writeAllDrivers(fp)
                rigDriversEnd(fp)
            elif key == 'rig-correct':
                fp.write("CorrectRig %s ;\n" % the.Human)
            elif key == 'recalc-roll':
                fp.write("  RecalcRoll %s ;\n" % the.RecalcRoll)
            elif key == 'ProxyMesh':
                writeProxyMesh(fp, proxy, proxyData)
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
                elif the.Config.cage:                    
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
                for f in faces:
                    fp.write("    f")
                    for v in f:
                        fp.write(" %d" % v[0])
                    fp.write(" ;\n")
                fp.write("#if False\n")
            elif key == 'EndFaces':
                writeFaceNumbers(fp, human, proxyData)
            elif key == 'FTTriangles':
                for (fn,f) in enumerate(faces):
                    if len(f) < 4:
                        fp.write("    mn %d 1 ;\n" % fn)
            elif key == 'ProxyUVCoords':
                layers = list(proxy.uvtexLayerName.keys())
                layers.sort()
                for layer in layers:
                    fp.write(                   
'  MeshTextureFaceLayer %s\n' % proxy.uvtexLayerName[layer] +
'    Data \n')
                    texfaces = proxy.texFacesLayers[layer]
                    texverts = proxy.texVertsLayers[layer]
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
                if human.uvsetFile:
                    uvset = proxyData["__uvset__"]
                    for ft in uvset.texFaces:
                        fp.write("    vt")
                        for vt in ft:
                            uv = uvset.texVerts[vt]
                            fp.write(" %.4g %.4g" %(uv[0], uv[1]))
                        fp.write(" ;\n")
                else:
                    for f in faces:
                        fp.write("    vt")
                        for v in f:
                            uv = obj.uvValues[v[1]]
                            fp.write(" %.4g %.4g" %(uv[0], uv[1]))
                        fp.write(" ;\n")
            elif key == 'Material':
                fp.write("Material %s%s\n" % (the.Human, words[2]))
            elif key == 'Materials':
                writeBaseMaterials(fp, human, proxyData)
            elif key == 'ProxyMaterials':
                if proxy.useBaseMaterials:
                    writeBaseMaterials(fp, human, proxyData)
                elif proxy.material:
                    fp.write("  Material %s%s ;\n" % (the.Human, proxy.material.name))
            elif key == 'VertexGroup':
                writeVertexGroups(fp, proxy)
            elif key == 'group':
                writeGroups(fp, proxyData)
            elif key == 'mesh-shapeKey':
                pass
                writeShapeKeys(fp, human, "%sMesh" % the.Human, None)
            elif key == 'proxy-shapeKey':
                fp.write("#if toggle&T_Cage\n")
                proxyShapes('Cage', human, proxyData, fp)
                fp.write("#endif\n#if toggle&T_Proxy\n")
                proxyShapes('Proxy', human, proxyData, fp)
                fp.write("#endif\n#if toggle&T_Clothes\n")
                proxyShapes('Clothes', human, proxyData, fp)
                fp.write("#endif\n")
            elif key == 'ProxyModifiers':
                writeProxyModifiers(fp, proxy)
            elif key == 'MTex':
                n = nMasks + int(words[2])
                fp.write("  MTex %d %s %s %s\n" % (n+1, words[3], words[4], words[5]))
            elif key == 'SkinStart':
                nMasks = writeSkinStart(fp, proxy, proxyData)
            elif key == 'curves':
                mhx_rig.writeAllCurves(fp)
            elif key == 'properties':
                mhx_rig.writeAllProperties(fp, words[2])
                writeHideProp(fp, the.Human)
                for proxy in proxyData.values():
                    writeHideProp(fp, proxy.name)
            elif key == 'material-drivers':
                fp.write("  use_textures Array 0")
                for n in range(nMasks):
                    fp.write(" 1")
                for n in range(3):
                    fp.write(" 1")
                fp.write(" ;\n")
                fp.write("  AnimationData %sMesh True\n" % the.Human)
                #mhx_rig.writeTextureDrivers(fp, rig_panel_25.BodyLanguageTextureDrivers)
                writeMaskDrivers(fp, proxyData)
                fp.write("  end AnimationData\n")
            elif key == 'Filename':
                file = export_config.getOutFileName(words[2], words[3], True, human, the.Config)
                fp.write("  Filename %s ;\n" % file)
            else:
                raise NameError("Unknown *** %s" % words[1])
        else:
            fp.write(line)

    print("    %s copied" % tmplName)
    tmpl.close()

    return

#
#   writeFaceNumbers(fp, human, proxyData):
#

MaterialNumbers = {
    "skin" : 0,
    "nail" : 0,
    "teeth" : 1,
    "eye": 2,
    "cornea" : 2,
    "brows" : 3,
    "joint" : 4,
    "red" : 5,
    "green" : 6,
    "blue" : 7
}
    
def writeFaceNumbers(fp, human, proxyData):
    fp.write("#else\n")
    if human.uvsetFile:
        uvset = proxyData["__uvset__"]
        for ftn in uvset.faceNumbers:
            fp.write(ftn)
    else:            
        obj = human.meshData
        fmats = {}
        for f in obj.faces:
            fmats[f.idx] = MaterialNumbers[f.mtl]
        deleteGroups = []
        deleteVerts = None
        for proxy in proxyData.values():
            deleteGroups += proxy.deleteGroups
            deleteVerts = mh2proxy.multiplyDeleteVerts(proxy, deleteVerts)
                    
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
                    
        if deleteVerts:
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
#   writeBaseMaterials(fp, human, proxyData):                    
#

def writeBaseMaterials(fp, human, proxyData):      
    if human.uvsetFile:
        uvset = proxyData["__uvset__"]
        for mat in uvset.materials:
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
    
def addMaskImage(fp, mask):            
    (folder, file) = mask
    path = export_config.getOutFileName(file, folder, True, None, the.Config)
    fp.write(
"Image %s\n" % file +
"  Filename %s ;\n" % path +
"  use_premultiply True ;\n" +
"end Image\n\n" +
"Texture %s IMAGE\n" % file  +
"  Image %s ;\n" % file +
"end Texture\n\n")
    return
    
def addMaskMTex(fp, mask, proxy, blendtype, n):            
    (dir, file) = mask
    fp.write(
"  MTex %d %s UV ALPHA\n" % (n+1, file) +
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
        fp.write("    uv_layer '%s' ;\n" %  proxy.uvtexLayerName[proxy.maskLayer])
    fp.write("  end MTex\n")
    return

#
#   writeSkinStart(fp, proxy, proxyData)
#

def writeSkinStart(fp, proxy, proxyData):
    if proxy:
        fp.write("Material %s%sSkin\n" % (the.Human, proxy.name))
        return 0
    nMasks = 0
    prxList = list(proxyData.values())
    
    for prx in prxList:
        if prx.mask:
            addMaskImage(fp, prx.mask)
            nMasks += 1
    fp.write("Material %sSkin\n" % the.Human +
"  MTex 0 diffuse UV COLOR\n" +
#"    texture Refer Texture diffuse ;\n" +
"  end MTex\n")

    n = 0    
    for prx in prxList:
        if prx.mask:
            addMaskMTex(fp, prx.mask, proxy, 'MULTIPLY', n)
            n += 1
            
    return nMasks
               
def writeMaskDrivers(fp, proxyData):
    fp.write("#if toggle&T_Clothes\n")
    n = 0
    for prx in proxyData.values():
        if prx.type == 'Clothes' and prx.mask:
            (dir, file) = prx.mask
            mhx_rig.writePropDriver(fp, ["Hide%s" % prx.name], "1-x1", 'use_textures', n+1)
            n += 1            
    fp.write("#endif\n")
    return
    
#
#   writeVertexGroups(fp, proxy):                
#

def writeVertexGroups(fp, proxy):                
    if proxy and proxy.weights:
        mh2proxy.writeRigWeights(fp, proxy.weights)
        return
    fp.write("#if toggle&T_Armature\n")
    if the.VertexWeights:
        if proxy:
            weights = mh2proxy.getProxyWeights(the.VertexWeights, proxy)
        else:
            weights = the.VertexWeights                    
        mh2proxy.writeRigWeights(fp, weights)
    else:
        for file in the.VertexGroupFiles:
            copyVertGroups(file, fp, proxy)
            
    if the.Config.mhxrig == 'mhx':            
        if the.MuscleBones:
            copyVertGroups("shared/mhx/templates/vertexgroups-muscles25.mhx", fp, proxy)    
        copyVertGroups("shared/mhx/templates/vertexgroups-tight25.mhx", fp, proxy)    
        if the.MuscleBones:
            copyVertGroups("shared/mhx/templates/vertexgroups-tight-muscles25.mhx", fp, proxy)    
        if the.Config.skirtrig == "own":
            copyVertGroups("shared/mhx/templates/vertexgroups-skirt-rigged.mhx", fp, proxy)    
        elif the.Config.skirtrig == "inh":
            copyVertGroups("shared/mhx/templates/vertexgroups-skirt25.mhx", fp, proxy)    
            if the.MuscleBones:
                copyVertGroups("shared/mhx/templates/vertexgroups-skirt-muscles25.mhx", fp, proxy)    
        if the.Config.breastrig:
            copyVertGroups("shared/mhx/templates/vertexgroups-breasts25.mhx", fp, proxy)    

    for path in the.Config.customvertexgroups:
        print("    %s" % path)
        copyVertGroups(path, fp, proxy)    

    if the.Config.cage and not (proxy and proxy.cage):
        fp.write("#if toggle&T_Cage\n")
        copyVertGroups("shared/mhx/templates/vertexgroups-cage25.mhx", fp, proxy)    
        fp.write("#endif\n")
    fp.write("#endif\n")
    copyVertGroups("shared/mhx/templates/vertexgroups-leftright25.mhx", fp, proxy)    
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
"#if toggle&T_Armature\n" +
"    ob %s ;\n" % the.Human +
"#endif\n" +
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
#   writeProxyMesh(fp, proxy, proxyData):                
#

def writeProxyMesh(fp, proxy, proxyData):                
    mat = proxy.material
    if mat:
        if proxy.material_file:
            copyProxyMaterialFile(fp, proxy.material_file, mat, proxy, proxyData)
        else:
            writeProxyMaterial(fp, mat, proxy, proxyData)
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
    "#if toggle&T_Armature\n" +
    "  parent Refer Object %s ;\n" % the.Human +
    "  hide False ;\n" +
    "  hide_render False ;\n" +
    "#endif\n")
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
    fp.write(
"  Property Hide%s False Control_%s_visibility ;\n" % (name, name) +
"  PropKeys Hide%s \"type\":'BOOLEAN',\"min\":0,\"max\":1, ;\n" % name)
    return

def writeHideAnimationData(fp, prefix, name):
    fp.write("AnimationData %s%sMesh True\n" % (prefix, name))
    mhx_rig.writePropDriver(fp, ["Hide%s" % name], "x1", "hide", -1)
    mhx_rig.writePropDriver(fp, ["Hide%s" % name], "x1", "hide_render", -1)
    fp.write("end AnimationData\n")
    return    
       
#
#   copyProxyMaterialFile(fp, pair, mat, proxy, proxyData):
#

def copyProxyMaterialFile(fp, pair, mat, proxy, proxyData):
    prxList = sortedMasks(proxyData)
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
            file = export_config.getOutFileName(words[1], folder, True, None, the.Config)
            fp.write("  Filename %s ;\n" % file)
        else:
            fp.write(line)
    tmpl.close()
    return
       
#
#   writeProxyMaterial(fp, mat, proxy, proxyData):
#

def writeProxyTexture(fp, texture, mat, extra):        
    (folder,name) = texture
    tex = os.path.join(folder,name)
    #print(the.Human)
    print("Tex", tex)
    texname = the.Human + os.path.basename(tex)
    fromDir = os.path.dirname(tex)
    texfile = export_config.getOutFileName(tex, fromDir, True, None, the.Config)
    fp.write(
"Image %s\n" % texname +
"  Filename %s ;\n" % texfile +
"  use_premultiply True ;\n" +
"end Image\n\n" +
"Texture %s IMAGE\n" % texname +
"  Image %s ;\n" % texname)
    writeProxyMaterialSettings(fp, mat.textureSettings)             
    fp.write(extra)
    fp.write("end Texture\n\n")
    return (tex, texname)
    
def writeProxyMaterial(fp, mat, proxy, proxyData):
    tex = None
    bump = None
    normal = None
    displacement = None
    transparency = None
    if proxy.texture:
        (tex,texname) = writeProxyTexture(fp, proxy.texture, mat, "")
    if proxy.bump:
        (bump,bumpname) = writeProxyTexture(fp, proxy.bump, mat, "")
    if proxy.normal:
        (normal,normalname) = writeProxyTexture(fp, proxy.normal, mat, 
            ("    use_normal_map True ;\n")
            )
    if proxy.displacement:
        (displacement,dispname) = writeProxyTexture(fp, proxy.displacement, mat, "")
    if proxy.transparency:
        (transparency,transname) = writeProxyTexture(fp, proxy.transparency, mat, "")
           
    prxList = sortedMasks(proxyData)
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
        
    if nMasks > 0 or mat.alpha < 0.99:
        fp.write(
"  use_transparency True ;\n" +
"  transparency_method 'Z_TRANSPARENCY' ;\n" +
"  alpha %3.f ;\n" % mat.alpha +
"  specular_alpha %.3f ;\n" % mat.alpha)
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
            addMaskMTex(fp, prx.mask, proxy, 'MULTIPLY', n)
            n += 1
    if not tex:            
        addMaskMTex(fp, (None,'solid'), proxy, 'MIX', n)
    return   
    
def sortedMasks(proxyData):
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
#    copyVertGroups(tmplName, fp, proxy):
#

def copyVertGroups(tmplName, fp, proxy):
    tmpl = open(tmplName)
    shapes = []
    vgroups = []

    if tmpl == None:
        print("*** Cannot open "+tmplName)
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
    print("    %s copied" % tmplName)
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
#    copyShapeKeys(tmplName, fp, proxy, doScale):
#

def copyShapeKeys(tmplName, fp, proxy, doScale):
    tmpl = open(tmplName)
    shapes = []
    vgroups = []
    scale = 1.0

    if tmpl == None:
        print("*** Cannot open "+tmplName)
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
    print("    %s copied" % tmplName)
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

#
#    writeShapeKeys(fp, human, name, proxy):
#

def writeTargets(fp, human, drivers, folder):    
    for (fname, bname, typ, targ, angle, lr) in drivers:
        expr = read_expression.readCorrective(human, "%s/%s/" % (folder,fname))
        fp.write("ShapeKey %s %s True\n" % (fname, lr))
        for (index, dr) in expr.items():
            fp.write("  sv %d %.4f %.4f %.4f ;\n" %  (index, dr[0], dr[1], dr[2]))
        fp.write("end ShapeKey\n")
    return            


def writeShapeKeys(fp, human, name, proxy):
    fp.write(
"#if toggle&T_Shapekeys\n" +
"ShapeKeys %s\n" % name +
"  ShapeKey Basis Sym True\n" +
"  end ShapeKey\n")

    if (not proxy or proxy.type == 'Proxy'):
        if the.Config.faceshapes:
            if BODY_LANGUAGE:
                copyShapeKeys("shared/mhx/templates/shapekeys-bodylanguage25.mhx", fp, proxy, True)    
            else:
                copyShapeKeys("shared/mhx/templates/shapekeys-facial25.mhx", fp, proxy, True)    

    if not proxy:
        if the.Config.expressions:
            exprList = read_expression.readExpressions(human)
            for (name, verts) in exprList:
                fp.write("ShapeKey %s Sym True\n" % name)
                for (v, r) in verts.items():
                    (dx, dy, dz) = r
                    fp.write("    sv %d %.4f %.4f %.4f ;\n" % (v, dx, dy, dz))
                fp.write("end ShapeKey\n")

    if the.Config.bodyshapes:
        writeTargets(fp, human, rig_shoulder_25.ShoulderTargetDrivers, "shoulder")                
        copyShapeKeys("shared/mhx/templates/shapekeys-body25.mhx", fp, proxy, True)

    for path in the.Config.customshapes:
        print("    %s" % path)
        copyShapeKeys(path, fp, proxy, False)   

    fp.write(
"  AnimationData None (toggle&T_Symm==0)\n")

        
    if the.Config.bodyshapes:
        mhx_rig.writeTargetDrivers(fp, rig_shoulder_25.ShoulderTargetDrivers, the.Human)
        mhx_rig.writeRotDiffDrivers(fp, rig_arm_25.ArmShapeDrivers, proxy)
        mhx_rig.writeRotDiffDrivers(fp, rig_leg_25.LegShapeDrivers, proxy)
        mhx_rig.writeShapePropDrivers(fp, rig_body_25.BodyShapes, proxy, "&")

    fp.write("#if toggle&T_ShapeDrivers\n")
    if (not proxy or proxy.type == 'Proxy'):
        if the.Config.faceshapes:
            if BODY_LANGUAGE:
                drivers = rig_panel_25.BodyLanguageShapeDrivers
            else:
                drivers = rig_panel_25.FaceShapeDrivers
            if the.Config.facepanel:
                mhx_rig.writeShapeDrivers(fp, drivers, None)
            else:
                mhx_rig.writeShapePropDrivers(fp, drivers.keys(), proxy, "&_")                

    if not proxy:
        if the.Config.expressions and not proxy:
            mhx_rig.writeShapePropDrivers(fp, read_expression.Expressions, proxy, "*")
            
        skeys = []
        for (skey, val, string, min, max) in  the.CustomProps:
            skeys.append(skey)
        mhx_rig.writeShapePropDrivers(fp, skeys, proxy, "&")    
    fp.write("#endif\n")
        
    fp.write(
"  end AnimationData\n" +
"end ShapeKeys\n" +
"#endif\n")
    return    

#
#    proxyShapes(typ, human, proxyData, fp):
#

def proxyShapes(typ, human, proxyData, fp):
    fp.write("#if toggle&T_%s\n" % typ)
    for proxy in proxyData.values():
        if proxy.name and proxy.type == typ:
            writeShapeKeys(fp, human, the.Human+proxy.name+"Mesh", proxy)
    fp.write("#endif\n")
        
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
#   loadFacesIndices(obj):
#   Copied old loadFacesIndices from files3d.
#

def loadFacesIndices(obj):
    path = "data/3dobjs/base.obj"
    try:
        fileDescriptor = open(path)
    except:
        print 'Error opening %s file' % path
        return
    vertsIdxs = []
    for data in fileDescriptor:
        dataList = data.split()
        if dataList[0] == 'f':
            vIndices = []
            for faceData in dataList[1:]:
                vInfo = faceData.split('/')
                vIdx = int(vInfo[0]) - 1  # -1 because obj is 1 based list
                if len(vInfo) > 1 and vInfo[1] != '':
                    uvIdx = int(vInfo[1]) - 1  # -1 because obj is 1 based list
                    vIndices.append([vIdx, uvIdx])
                else:
                    vIndices.append([vIdx, 0])
            vertsIdxs.append(vIndices)
    fileDescriptor.close()
    return vertsIdxs

#
#   writeMultiMaterials(uvset, human, fp):
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

def writeMultiMaterials(uvset, human, fp):
    folder = os.path.dirname(human.uvsetFile)
    print("Folder", folder)
    for mat in uvset.materials:
        for tex in mat.textures:
            name = os.path.basename(tex.file)
            fp.write("Image %s\n" % name)
            #file = export_config.getOutFileName(tex, "data/textures", True, human, the.Config)
            file = export_config.getOutFileName(name, folder, True, human, the.Config)
            fp.write(
                "  Filename %s ;\n" % file +
                "  use_premultiply True ;\n" +
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
    
    


