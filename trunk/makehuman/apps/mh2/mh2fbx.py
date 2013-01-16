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

import os
import sys
import export_config
import object_collection
import mh2collada


fbxpath = "tools/blender26x"
if fbxpath not in sys.path:
    sys.path.append(fbxpath)
    
import io_mh_fbx
# bpy must be imported after io_mh_fbx
import bpy


def exportFbx(human, filepath, options):
    cfg = export_config.exportConfig(human, True)
    cfg.separatefolder = True

    rigfile = "data/rigs/%s.rig" % options["fbxrig"]
    print("Using rig file %s" % rigfile)
    amt = mh2collada.getArmatureFromRigFile(rigfile, human.meshData)

    stuffs = object_collection.setupObjects(os.path.splitext(filepath)[0], human,
        helpers=options["helpers"], 
        hidden=options["hidden"], 
        eyebrows=options["eyebrows"], 
        lashes=options["lashes"],
        subdivide=options["subdivide"])
    
    (scale, unit) = options["scale"]   
    outfile = export_config.getOutFileFolder(filepath, cfg)   
    (path, ext) = os.path.splitext(outfile)

    bpy.initialize()
    name = os.path.splitext(os.path.basename(filepath))[0]
    rig = bpy.addRig(name, amt)
    for stuff in stuffs:
        ob = bpy.addMesh(stuff.name, stuff, True)
        ob.parent = rig
        
    #name = os.path.splitext(os.path.basename(filepath))[0]
    #bpy.addMesh(name, human.meshData, False)
    
    filename = "%s.fbx" % path
    print("Mh2Fbx", bpy.context.scene.objects)
    io_mh_fbx.fbx_export.exportFbxFile(bpy.context, filename)
    return

