#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------
Exports proxy mesh to obj

"""

import os
import export_config
import mh2proxy
import object_collection

#
#    exportProxyObj(human, name, options):    
#

def exportProxyObj(human, name, options):
    obj = human.meshData
    cfg = export_config.exportConfig(human, True)
    cfg.separatefolder = True

    stuffs = object_collection.setupObjects(os.path.splitext(name)[0], human,
        helpers=options["helpers"], 
        hidden=options["hidden"], 
        eyebrows=options["eyebrows"], 
        lashes=options["lashes"],
        subdivide=options["subdivide"])
    
    (scale, unit) = options["scale"]   
    #name = export_config.goodName(name)
    outfile = export_config.getOutFileFolder(name, cfg)   
    (path, ext) = os.path.splitext(outfile)

    filename = "%s_clothed.obj" % path
    fp = open(filename, 'w')
    fp.write(
"# MakeHuman exported OBJ with clothes\n" +
"# www.makehuman.org\n\n" +
"mtllib %s_clothed.obj.mtl\n" % os.path.basename(path))
    for stuff in stuffs:
        writeGeometry(obj, fp, stuff, scale)
    fp.close()
    
    filename = "%s_clothed.obj.mtl" % path
    fp = open(filename, 'w')
    fp.write(
'# MakeHuman exported MTL with clothes\n' +
'# www.makehuman.org\n\n')
    for stuff in stuffs:
        writeMaterial(fp, stuff, human, cfg)
    fp.close()
    return

#
#    writeGeometry(obj, fp, stuff, scale):
#
        
def writeGeometry(obj, fp, stuff, scale):
    nVerts = len(stuff.verts)
    nUvVerts = len(stuff.uvValues)
    fp.write("usemtl %s\n" % stuff.name)
    fp.write("g %s\n" % stuff.name)    
    for v in stuff.verts:
        fp.write("v %.4g %.4g %.4g\n" % (scale*v[0], scale*v[1], scale*v[2]))
    #for no in stuff.vnormals:
    #    fp.write("vn %.4g %.4g %.4g\n" % (no[0], no[1], no[2]))
    for uv in stuff.uvValues:
        fp.write("vt %.4g %.4g\n" %(uv[0], uv[1]))
    for fc in stuff.faces:
        fp.write('f ')
        for vs in fc:
            v = vs[0]
            uv = vs[1]
            fp.write("%d/%d " % (v-nVerts, uv-nUvVerts))
        fp.write('\n')
    return        

#
#   writeMaterial(fp, stuff, human, cfg):
#

def writeMaterial(fp, stuff, human, cfg):
    fp.write("\nnewmtl %s\n" % stuff.name)
    diffuse = (1, 1, 1)
    spec = (1, 1, 1)
    diffScale = 0.8
    specScale = 0.02
    alpha = 1
    if stuff.material:
        for (key, value) in stuff.material.settings:
            if key == "diffuse_color":
                diffuse = value
            elif key == "specular_color":
                spec = value
            elif key == "diffuse_intensity":
                diffScale = value
            elif key == "specular_intensity":
                specScale = value
            elif key == "alpha":
                alpha = value
                
    fp.write(
    "Kd %.4g %.4g %.4g\n" % (diffScale*diffuse[0], diffScale*diffuse[1], diffScale*diffuse[2]) +
    "Ks %.4g %.4g %.4g\n" % (specScale*spec[0], specScale*spec[1], specScale*spec[2]) +
    "d %.4g\n" % alpha
    )
    
    if stuff.proxy:
        writeTexture(fp, "map_Kd", stuff.texture, human, cfg)
        #writeTexture(fp, "map_Tr", stuff.proxy.translucency, human, cfg)
        writeTexture(fp, "map_Disp", stuff.proxy.normal, human, cfg)
        writeTexture(fp, "map_Disp", stuff.proxy.displacement, human, cfg)
    else:        
        writeTexture(fp, "map_Kd", ("data/textures", "texture.png"), human, cfg)


def writeTexture(fp, key, texture, human, cfg):
    if not texture:
        return
    (folder, texfile) = texture
    path = export_config.getOutFileName(texfile, folder, True, human, cfg)        
    (fname, ext) = os.path.splitext(texfile)  
    name = "%s_%s" % (fname, ext[1:])
    if cfg.separatefolder:
        texpath = "textures/"+texfile
    else:
        texpath = texfile
    fp.write("%s %s\n" % (key, texpath))
    

"""    
Ka 1.0 1.0 1.0
Kd 1.0 1.0 1.0
Ks 0.33 0.33 0.52
illum 5
Ns 50.0
map_Kd texture.png
"""
