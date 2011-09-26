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

TO DO

"""

MAJOR_VERSION = 1
MINOR_VERSION = 8
BODY_LANGUAGE = True
theHuman = 'Human'

import module3d
import aljabr
import mh
import mh2bvh
import os
import time

import mh2proxy
import mhx_24
import mhx_rig
import rig_panel_25
import rig_arm_25
import rig_leg_25
import rig_body_25
import read_expression
import read_rig

#
#    exportMhx(human, filename, options):
#

def exportMhx(human, filename, options):    
    global theConfig, theHuman
    theConfig = mh2proxy.proxyConfig(human, True, options)
    (name, ext) = os.path.splitext(filename)

    if '24' in theConfig.mhxversion:
        mhx_24.exportMhx(human, filename, options)
   
    if '25' in theConfig.mhxversion:
        theHuman = os.path.basename(name).capitalize().replace(' ','_')
        time1 = time.clock()
        filename = name+"-25"+ext
        try:
            fp = open(filename, 'w')
            mh2proxy.safePrint("Writing MHX 2.5x file",  filename )
        except:
            mh2proxy.safePrint("Unable to open file for writing", filename)
            fp = 0
        if fp:
            exportMhx_25(human, fp)
            fp.close()
            time2 = time.clock()
            mh2proxy.safePrint("Wrote MHX 2.5x file in %g s:" % (time2-time1), filename)

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
    mhx_rig.setupRig(obj)

    fp.write(
"NoScale True ;\n" +
"Object CustomShapes EMPTY None\n" +
"  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;\n" +
"end Object\n\n")

    if theConfig.useRig in ['mhx', 'rigify', 'blenrig']:
        rig = theConfig.useRig
        fp.write("#if toggle&T_Armature\n")
        for fname in mhx_rig.GizmoFiles:
            copyFile25(human, fname, rig, fp, None, [])    
        mhx_rig.setupCircles(fp)
        copyFile25(human, "shared/mhx/templates/rig-armature25.mhx", rig, fp, None, [])    
        fp.write("#endif\n")
    elif theConfig.useRig in ['game']:
        rig = mh2proxy.CProxy('Rig', 0)
        rig.name = theHuman
        (locs, rig.bones, rig.weights) = read_rig.readRigFile('./data/templates/%s.rig' % theConfig.useRig, obj)
        fp.write("#if toggle&T_Armature\n")
        copyFile25(human, "shared/mhx/templates/rig-game25.mhx", rig, fp, None, [])    
        fp.write("#endif\n")
    else:
        raise NameError("Unknown base rig %s" % rig)
        
    fp.write("\nNoScale False ;\n\n")

    copyFile25(human, "shared/mhx/templates/materials25.mhx", rig, fp, None, [])    

    proxyData = {}
    proxyCopy('Cage', human, rig, theConfig.proxyList, proxyData, fp)

    if theConfig.mainmesh:
        fp.write("#if toggle&T_Mesh\n")
        copyFile25(human, "shared/mhx/templates/meshes25.mhx", rig, fp, None, proxyData)    
        fp.write("#endif\n")

    proxyCopy('Proxy', human, rig, theConfig.proxyList, proxyData, fp)
    proxyCopy('Clothes', human, rig, theConfig.proxyList, proxyData, fp)

    copyFile25(human, "shared/mhx/templates/rig-poses25.mhx", rig, fp, None, proxyData) 

    if theConfig.useRig == 'rigify':
        fp.write("Rigify %s ;\n" % theHuman)
    return

#
#    proxyCopy(name, human, rig, proxyList, proxyData, fp)
#

def proxyCopy(name, human, rig, proxyList, proxyData, fp):
    for (typ, useObj, useMhx, useDae, proxyStuff) in proxyList:
        if useMhx and typ == name:
            fp.write("#if toggle&T_%s\n" % typ)
            copyFile25(human, "shared/mhx/templates/proxy25.mhx", rig, fp, proxyStuff, proxyData)    
            fp.write("#endif\n")
        
#
#    copyFile25(human, tmplName, rig, fp, proxyStuff, proxyData):
#

def copyFile25(human, tmplName, rig, fp, proxyStuff, proxyData):
    tmpl = open(tmplName)
    if tmpl == None:
        print("*** Cannot open "+tmplName)
        return

    obj = human.meshData
    bone = None
    proxy = None
    faces = loadFacesIndices(obj)
    ignoreLine = False
    for line in tmpl:
        words= line.split()
        if len(words) == 0:
            fp.write(line)
        elif words[0] == '***':
            if ignoreLine:
                if words[1] == 'EndIgnore':
                    ignoreLine = False
            #elif words[1] == 'Bone':
            #    bone = words[2]
            #    fp.write("    Bone %s\n" % bone)
            #elif words[1] == 'Rigify':
            #    mhxbones_rigify.writeBones(obj, fp)
            #elif words[1] == 'head':
            #    (x, y, z) = mhxbones.boneHead[bone]
            #    fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,-z,y))
            #elif words[1] == 'tail':
            #    (x, y, z) = mhxbones.boneTail[bone]
            #    fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,-z,y))
            #elif words[1] == 'roll':
            #    (x, y) = mhxbones.boneRoll[bone]
            #    fp.write("    roll %.6g ;\n" % (y))
            elif words[1] == 'refer-human':
                if words[3] == 'ControlRig' or theConfig.useRig != 'mhx':
                    fp.write("    %s Refer Object %s ;\n" % (words[2], theHuman))
                elif words[3] == 'DeformRig':
                    fp.write("    %s Refer Object %sDeformRig ;\n" % (words[2], theHuman))
                else:
                    raise NameError("refer-human: %s" % line)
            elif words[1] == 'rig-bones':
                if words[2] == 'ControlRig':
                    fp.write("Armature %s %s   Normal \n" % (theHuman, theHuman))
                    if type(rig) == str:
                        mhx_rig.writeControlArmature(fp)
                    else:
                        mh2proxy.writeRigBones(fp, rig.bones)
                elif words[2] == 'DeformRig':
                    fp.write("Armature %sDeformRig %sDeformRig   Normal \n" % (theHuman, theHuman))
                    if rig == 'mhx':
                        mhx_rig.writeDeformArmature(fp)
                else:
                    raise NameError("rig-bones: %s" % line)
            elif words[1] == 'human-object':
                if words[2] == 'Mesh':
                    fp.write(
"Object %sMesh MESH %sMesh\n"  % (theHuman, theHuman) +
"  Property MhxOffsetX %.4f ;\n" % mhx_rig.Origin[0] +
"  Property MhxOffsetY %.4f ;\n" % mhx_rig.Origin[1] +
"  Property MhxOffsetZ %.4f ;\n" % mhx_rig.Origin[2])
                elif words[2] == 'ControlRig':
                    fp.write("Object %s ARMATURE %s\n"  % (theHuman, theHuman))
                else:
                    fp.write("Object %sDeformRig ARMATURE %sDeformRig\n"  % (theHuman, theHuman))
            elif words[1] == 'rig-poses':
                if words[2] == 'ControlRig':
                    if type(rig) == str:
                        fp.write("Pose %s\n" % theHuman)
                        mhx_rig.writeControlPoses(fp)
                        fp.write("  ik_solver 'LEGACY' ;\nend Pose\n")
                    else:
                        mh2proxy.writeRigPose(fp, rig.name, rig.bones)
                elif words[2] == 'DeformRig':
                    if rig == 'mhx':
                        fp.write("Pose %sDeformRig\n" % theHuman)
                        mhx_rig.writeDeformPoses(fp)
                        fp.write("  ik_solver 'LEGACY' ;\nend Pose\n")
            elif words[1] == 'rig-actions':
                if type(rig) == str:
                    fp.write("Pose %s\nend Pose\n" % theHuman)
                    mhx_rig.writeAllActions(fp)
            elif words[1] == 'rig-drivers':
                if type(rig) == str:
                    if words[2] == 'ControlRig':
                        fp.write("AnimationData %s True\n" % theHuman)
                        mhx_rig.writeAllDrivers(fp)
                        rigDriversEnd(fp)
                    elif words[2] == 'DeformRig':
                        fp.write("AnimationData %sDeformRig True\n" % theHuman)
                        mhx_rig.writeDeformDrivers(fp)
                        rigDriversEnd(fp)
                    else:
                        raise NameError("rig-drivers: %s" % line)
            elif words[1] == 'rig-correct':
                fp.write("CorrectRig %s ;\n" % theHuman)
            elif words[1] == 'recalc-roll':
                fp.write("  RecalcRoll %s ;\n" % mhx_rig.RecalcRoll)
            elif words[1] == 'ProxyRigStart':
                proxy = mh2proxy.readProxyFile(obj, proxyStuff)
                proxyData[proxy.name] = proxy
                if proxy.rig:
                    fp.write("#if True\n")
                    fp.write("Armature %s %s   Normal \n" % (proxy.name, proxy.name))
                    mh2proxy.writeProxyArmature(fp, obj, proxy)
                else:
                    fp.write("#if False\n")
            elif words[1] == 'ProxyRigObject':
                fp.write("Object %s ARMATURE %s \n" % (proxy.name, proxy.name))
                if proxy.rig:
                    fp.write("  Property MhxRigType '%s' ;\n" % proxy.name)
            elif words[1] == 'ProxyPose':
                mh2proxy.writeRigPose(fp, proxy.name, proxy.bones)
            elif words[1] == 'ProxyMesh':
                mat = proxy.material
                if mat:
                    writeProxyMaterial(fp, mat)
                fp.write("Mesh %sMesh %sMesh \n" % (proxy.name, proxy.name))
                if mat:
                    fp.write("  Material %s ;\n" % mat.name)

            elif words[1] == 'ProxyObject':
                fp.write("Object %sMesh MESH %sMesh \n" % (proxy.name, proxy.name))
                fp.write("#if toggle&T_Armature\n")
                if proxy.rig:
                    fp.write("  parent Refer Object %s ;\n" % proxy.name)
                else:
                    fp.write("  parent Refer Object %s ;\n" % theHuman)
                fp.write("#endif\n")
                if proxy.wire:
                    fp.write("  draw_type 'WIRE' ;\n")
            elif words[1] == 'ProxyLayers':
                fp.write("layers Array ")
                for n in range(20):
                    if n == proxy.layer:
                        fp.write("1 ")
                    else:
                        fp.write("0 ")
                fp.write(";\n")
            elif words[1] == 'toggleCage':
                if theConfig.cage and not (proxy and proxy.cage):
                    fp.write("  #if toggle&T_Cage\n")
                else:
                    fp.write("  #if False\n")
            elif words[1] == 'ProxyReferRig':
                if proxy.rig:
                    fp.write("      object Refer Object %s ;\n" % proxy.name)
                elif True or theConfig.useRig == 'game':
                    fp.write("      object Refer Object %s ;\n" % theHuman)
                else:
                    fp.write("      object Refer Object %sDeformRig ;\n" % theHuman)
            elif words[1] == 'ProxyVerts':
                ox = mhx_rig.Origin[0]
                oy = mhx_rig.Origin[1]
                oz = mhx_rig.Origin[2]
                for bary in proxy.realVerts:
                    (x,y,z) = mh2proxy.proxyCoord(bary)
                    fp.write("  v %.4f %.4f %.4f ;\n" % (x-ox, -z+oz, y-oy))

            elif words[1] == 'Verts':
                proxy = None
                fp.write("Mesh %sMesh %sMesh\n  Verts\n" % (theHuman, theHuman))
                ox = mhx_rig.Origin[0]
                oy = mhx_rig.Origin[1]
                oz = mhx_rig.Origin[2]
                for v in obj.verts:
                    fp.write("  v %.4f %.4f %.4f ;\n" % (v.co[0]-ox, -v.co[2]+oz, v.co[1]-oy))
            elif words[1] == 'ProxyFaces':
                for (f,g) in proxy.faces:
                    fp.write("    f")
                    for v in f:
                        fp.write(" %s" % v)
                    fp.write(" ;\n")
                for mat in proxy.materials:
                    fp.write("    ft %d 1 ;\n" % mat)
            elif words[1] == 'Faces':
                for f in faces:
                    fp.write("    f")
                    for v in f:
                        fp.write(" %d" % v[0])
                    fp.write(" ;\n")
            elif words[1] == 'FTTriangles':
                for (fn,f) in enumerate(faces):
                    if len(f) < 4:
                        fp.write("    mn %d 1 ;\n" % fn)
            elif words[1] == 'ProxyUVCoords':
                for f in proxy.texFaces:
                    fp.write("    vt")
                    for v in f:
                        uv = proxy.texVerts[v]
                        fp.write(" %.6g %.6g" % (uv[0], uv[1]))
                    fp.write(" ;\n")
            elif words[1] == 'TexVerts':
                for f in faces:
                    fp.write("    vt")
                    for v in f:
                        uv = obj.uvValues[v[1]]
                        fp.write(" %.6g %.6g" %(uv[0], uv[1]))
                    fp.write(" ;\n")
            elif words[1] == 'VertexGroup':
                if proxy and proxy.weights:
                    mh2proxy.writeRigWeights(fp, proxy.weights)
                else:
                    fp.write("#if toggle&T_Armature\n")
                    if type(rig) == str:
                        for file in mhx_rig.VertexGroupFiles:
                            copyVertGroups(file, fp, proxy)
                    else:
                        if proxy:
                            weights = mh2proxy.getProxyWeights(rig.weights, proxy)
                        else:
                            weights = rig.weights                    
                        mh2proxy.writeRigWeights(fp, weights)
                    fp.write("#endif\n")
                    if theConfig.breasts:
                        copyVertGroups("shared/mhx/templates/vertexgroups-breasts25.mhx", fp, proxy)    
                    for (path, mod) in theConfig.customvertexgroups:
                        print(path)
                        copyVertGroups(path, fp, proxy)    
                    copyVertGroups("shared/mhx/templates/vertexgroups-leftright25.mhx", fp, proxy)    
                    if theConfig.cage and not (proxy and proxy.cage):
                        fp.write("#if toggle&T_Cage\n")
                        copyVertGroups("shared/mhx/templates/vertexgroups-cage25.mhx", fp, proxy)    
                        fp.write("#endif\n")
            elif words[1] == 'group':
                fp.write(
"PostProcess %sMesh %s 0000003f 00080000 0068056b 0000c000 ;\n" % (theHuman, theHuman) + 
"Group %s\n"  % theHuman +
"  Objects\n" +
"#if toggle&T_Armature\n" +
"    ob %s ;\n" % theHuman +
#"    ob %sDeformRig ;\n" % theHuman +
#"    ob %sSpineCurve ;\n" % theHuman +
"#endif\n" +
"#if toggle&T_Mesh\n" +
"    ob %sMesh ;\n" % theHuman +
"#endif\n")
                groupProxy('Cage', fp, proxyData)
                groupProxy('Proxy', fp, proxyData)
                groupProxy('Clothes', fp, proxyData)
                fp.write(
"    ob CustomShapes ;\n" + 
"  end Objects\n" +
"  layers Array 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  ;\n" +
"end Group\n")
            elif words[1] == 'mesh-shapeKey':
                pass
                writeShapeKeys(fp, human, rig, "%sMesh" % theHuman, None)
            elif words[1] == 'proxy-shapeKey':
                fp.write("#if toggle&T_Cage\n")
                proxyShapes('Cage', human, rig, proxyData, fp)
                fp.write("#endif\n#if toggle&T_Proxy\n")
                proxyShapes('Proxy', human, rig, proxyData, fp)
                fp.write("#endif\n#if toggle&T_Clothes\n")
                proxyShapes('Clothes', human, rig, proxyData, fp)
                fp.write("#endif\n")
            elif words[1] == 'mesh-animationData':
                if rig == 'mhx':
                    writeAnimationData(fp, "%sMesh" % theHuman, None)
            elif words[1] == 'proxy-animationData':
                if rig == 'mhx':
                    for proxy in proxyData.values():
                        if proxy.name:
                            writeAnimationData(fp, proxy.name+"Mesh", proxy)
            elif words[1] == 'ProxyModifiers':
                for mod in proxy.modifiers:
                    if mod[0] == 'subsurf':
                        sslevels = mod[1]
                        fp.write(
"    Modifier SubSurf SUBSURF\n" +
"      levels %d ;\n" % sslevels +
"      render_levels %d ;\n" % (sslevels+1) +
"    end Modifier\n")
                    elif mod[0] == 'shrinkwrap':
                        offset = mod[1]
                        fp.write(
"    Modifier ShrinkWrap SHRINKWRAP\n" +
"      target Refer Object %sMesh ;\n" % theHuman +
"      offset %.4f ;\n" % offset +
"      use_keep_above_surface True ;\n" +
"    end Modifier\n")
            elif words[1] == 'curves':
                mhx_rig.writeAllCurves(fp)
            elif words[1] == 'properties':
                mhx_rig.writeAllProperties(fp, words[2])
            elif words[1] == 'material-drivers':
                if 0 and BODY_LANGUAGE:
                    fp.write("MaterialAnimationData %sMesh (toggle&T_Face==T_Face)and(toggle&T_Symm==0) 0\n" % theHuman)
                    mhx_rig.writeTextureDrivers(fp, rig_panel_25.BodyLanguageTextureDrivers)
                    fp.write("end MaterialAnimationData\n")
            elif words[1] == 'Filename':
                path1 = os.path.expanduser(words[3])
                (path, filename) = os.path.split(words[2])
                file1 = os.path.realpath(path1+filename)
                fp.write("  Filename %s ;\n" % file1)
            else:
                raise NameError("Unknown *** %s" % words[1])
        else:
            fp.write(line)

    print("    %s copied" % tmplName)
    tmpl.close()

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
#    groupProxy(typ, fp, proxyData):
#

def groupProxy(typ, fp, proxyData):
    fp.write("#if toggle&T_%s\n" % typ)
    for proxy in proxyData.values():
        if proxy.type == typ:
            fp.write("    ob %sMesh ;\n" % proxy.name)
            if proxy.rig:
                fp.write("    ob %s ;\n" % proxy.name)
    fp.write("#endif\n")
    return

#
#   writeProxyMaterial(fp, mat):
#

def writeProxyMaterial(fp, mat):
    tex = mat.texture
    if tex:
        name = os.path.basename(tex)
        fp.write(
"Image %s\n" % name +
"  Filename %s ;\n" % os.path.realpath(tex) +
"  use_premultiply True ;\n" +
"end Image\n\n" +
"Texture %s IMAGE\n" % name +
"  Image %s ;\n" % name)
        writeProxyMaterialSettings(fp, mat.textureSettings)             
        fp.write("end Texture\n")

    fp.write("Material %s \n" % mat.name)
    writeProxyMaterialSettings(fp, mat.settings)            
    if tex:
        fp.write(
"  MTex 0 diffuse UV COLOR\n" +
"    texture Refer Texture %s ;\n" % name)
        writeProxyMaterialSettings(fp, mat.mtexSettings)             
        fp.write("  end MTex\n")
    if mat.mtexSettings == []:
        fp.write(
"  use_shadows True ;\n" +
"  use_transparent_shadows True ;\n")
    fp.write("end Material\n\n")

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

#
#    copyVertGroups(tmplName, fp, proxy):
#

def copyVertGroups(tmplName, fp, proxy):
    if proxy and proxy.rig:
        return
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
                    vgroups.append((pv, w*wt))
            elif vgroups:
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
#    copyShapeKeys(tmplName, fp, proxy):
#

def copyShapeKeys(tmplName, fp, proxy, doScale):
    if proxy and proxy.rig:
        return
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
    #print('IGN', name, proxy.name)
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
    x1 = mhx_rig.locations[p1]
    x2 = mhx_rig.locations[p2]
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
#    writeShapeKeys(fp, human, rig, name, proxy):
#

def writeShapeKeys(fp, human, rig, name, proxy):
    fp.write(
"#if toggle&(T_Face+T_Shape)\n" +
"ShapeKeys %s\n" % name +
"  ShapeKey Basis Sym True\n" +
"  end ShapeKey\n")

    if (not proxy or proxy.type == 'Proxy'):
        if theConfig.faceshapes:
            fp.write("#if toggle&T_Face\n")  
            if BODY_LANGUAGE:
                copyShapeKeys("shared/mhx/templates/shapekeys-bodylanguage25.mhx", fp, proxy, True)    
            else:
                copyShapeKeys("shared/mhx/templates/shapekeys-facial25.mhx", fp, proxy, True)    
            fp.write("#endif\n")    

    if not proxy:
        if theConfig.expressions:
            exprList = read_expression.readExpressions(human)
            fp.write("#if toggle&T_Face\n")        
            for (name, verts) in exprList:
                fp.write("ShapeKey %s Sym True\n" % name)
                for (v, r) in verts.items():
                    (dx, dy, dz) = r
                    fp.write("    sv %d %.4f %.4f %.4f ;\n" % (v, dx, dy, dz))
                fp.write("end ShapeKey\n")
            fp.write("#endif\n")

    if theConfig.bodyshapes:
        fp.write("#if toggle&T_Shape\n")
        copyShapeKeys("shared/mhx/templates/shapekeys-body25.mhx", fp, proxy, True)
        fp.write("#endif\n")

    for (path, mod) in theConfig.customshapes:
        print(path)
        copyShapeKeys(path, fp, proxy, True)    

    if 0 and rig != 'mhx':
        fp.write(
"end ShapeKeys\n" +
"#endif\n")
        return

    fp.write(
"  AnimationData None (toggle&T_Symm==0)\n")

    if theConfig.bodyshapes:
        fp.write("#if toggle&T_Shape\n")
        mhx_rig.writeRotDiffDrivers(fp, rig_arm_25.ArmShapeDrivers, proxy)
        mhx_rig.writeRotDiffDrivers(fp, rig_leg_25.LegShapeDrivers, proxy)
        mhx_rig.writeShapePropDrivers(fp, rig_body_25.BodyShapes, "")
        fp.write("#endif\n")

    if (not proxy or proxy.type == 'Proxy'):
        if theConfig.faceshapes:
            fp.write("#if toggle&T_Face\n")
            if BODY_LANGUAGE:
                mhx_rig.writeShapeDrivers(fp, rig_panel_25.BodyLanguageShapeDrivers, None)
            else:
                mhx_rig.writeShapeDrivers(fp, rig_panel_25.FaceShapeDrivers, None)
            fp.write("#endif\n")

        if theConfig.expressions:
            fp.write("#if toggle&T_Face\n")
            mhx_rig.writeShapePropDrivers(fp, read_expression.Expressions, "*")
            fp.write("#endif\n")

    fp.write(
"  end AnimationData\n" +
"end ShapeKeys\n" +
"#endif\n")
    return    

#
#    proxyShapes(typ, human, rig, proxyData, fp):
#

def proxyShapes(typ, human, rig, proxyData, fp):
    fp.write("#if toggle&T_%s\n" % typ)
    for proxy in proxyData.values():
        if proxy.name and proxy.type == typ and not proxy.rig:
            writeShapeKeys(fp, human, rig, proxy.name+"Mesh", proxy)
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

"""
#
#   Can not use the face info in obj.faceGroups, because diamonds are not there
#
def loadFacesIndices(obj):
    faces = []
    print(list(obj.faceGroups))
    for fg in obj.faceGroups:
        for f in fg.faces:
            face = []
            for i,v in enumerate(f.verts):   
                face.append((v.idx, f.uv[i]))
            faces.append(face)
    return faces
"""

