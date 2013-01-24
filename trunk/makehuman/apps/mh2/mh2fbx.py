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
Fbx exporter

"""

import os.path
import sys

import export_config
import object_collection
import read_expression
import posemode
from mhx import the, mhx_custom
import log

fbxpath = "tools/blender26x"
if fbxpath not in sys.path:
    sys.path.append(fbxpath)
    
import io_mh_fbx
# bpy must be imported after io_mh_fbx
import bpy


def exportFbx(human, filepath, options):
    posemode.exitPoseMode()        
    posemode.enterPoseMode()
    
    the.Human = human        
    the.Config = export_config.exportConfig(human, True, [])
    the.Config.separatefolder = True
    outfile = export_config.getOutFileFolder(filepath, the.Config)        
    (outpath, ext) = os.path.splitext(outfile)

    log.message("Write FBX file %s" % outfile)

    rawTargets = []
    if options["expressions"]:
        shapeList = read_expression.readExpressionUnits(human, 0, 1)
        rawTargets += shapeList

    if options["customshapes"]:
        the.Config.customshapes = True
        mhx_custom.listCustomFiles(the.Config)                            

        log.message("Custom shapes:")    
        for path,name in the.Config.customShapeFiles:
            log.message("    %s", path)
            shape = mhx_custom.readCustomTarget(path)
            target = (name,shape)
            rawTargets.append(target)

    rigfile = "data/rigs/%s.rig" % options["fbxrig"]
    stuffs = object_collection.setupObjects(
        os.path.splitext(outfile)[0], 
        human, 
        rigfile, 
        rawTargets=rawTargets,
        helpers=options["helpers"], 
        hidden=options["hidden"], 
        eyebrows=options["eyebrows"], 
        lashes=options["lashes"])

    (scale, unit) = options["scale"]   

    bpy.initialize()
    name = os.path.splitext(os.path.basename(filepath))[0]
    boneInfo = stuffs[0].boneInfo
    rig = bpy.addRig(name, boneInfo)
    for stuff in stuffs:
        ob = bpy.addMesh(stuff.name, stuff, True)
        ob.parent = rig
        
    #name = os.path.splitext(os.path.basename(filepath))[0]
    #bpy.addMesh(name, human.meshData, False)
    
    filename = "%s.fbx" % outpath
    io_mh_fbx.fbx_export.exportFbxFile(bpy.context, filename)
    posemode.exitPoseMode()        
    return

