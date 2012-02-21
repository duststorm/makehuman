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
Exports proxy mesh to obj

"""

import os
import export_config
import mh2proxy
import mh2collada
import mhx_globals as the

#
#    exportProxyObj(human, filename):    
#

def exportProxyObj(human, name, options):
    obj = human.meshData
    the.Config = export_config.exportConfig(human, False)
    the.Options = options
    the.Config.separatefolder = True
    (the.Stuff, stuffs) = mh2collada.setupStuff(obj, {}, [], the.Config)
    (scale, unit) = options["scale"]    
    outfile = export_config.getOutFileFolder(name+".obj", the.Config)   
    (path, ext) = os.path.splitext(outfile)

    filename = "%s_clothed.obj" % path
    fp = open(filename, 'w')
    fp.write(
"# MakeHuman exported OBJ with clothes\n" +
"# www.makehuman.org\n\n" +
"mtllib foo_clothed.obj.mtl\n")
    for stuff in stuffs:
        print(stuff.name)
        writeGeometry(obj, fp, stuff, scale)
    fp.close()
    
    filename = "%s_clothed.obj.mtl" % path
    fp = open(filename, 'w')
    fp.write(
'# MakeHuman exported MTL with clothes\n' +
'# www.makehuman.org\n\n')
    for stuff in stuffs:
        writeMaterial(fp, stuff, human)
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
        fp.write("v %.4f %.4f %.4f\n" % (scale*v[0], scale*v[1], scale*v[2]))
    #for no in stuff.vnormals:
    #    fp.write("vn %.4f %.4f %.4f\n" % (no[0], no[1], no[2]))
    for uv in stuff.uvValues:
        fp.write("vt %.4f %.4f\n" %(uv[0], uv[1]))
    for fc in stuff.faces:
        fp.write('f ')
        for vs in fc:
            v = vs[0]
            uv = vs[1]
            fp.write("%d/%d " % (v-nVerts, uv-nUvVerts))
        fp.write('\n')
    return        

#
#   writeMaterial(fp, stuff, human):
#

def writeMaterial(fp, stuff, human):
    fp.write("newmtl %s\n" % stuff.name)
    diffuse = (0.8, 0.8, 0.8)
    spec = (1, 1, 1)
    if stuff.material:
        for (key, value) in stuff.material.settings:
            if key == "diffuse_color":
                diffuse = value
            elif key == "specular_color":
                spec = value
    fp.write(
    "Kd %.4f %.4f %.4f\n" % (diffuse[0], diffuse[1], diffuse[2]) +
    "Ks %.4f %.4f %.4f\n" % (spec[0], spec[1], spec[2])
    )
    if stuff.type:
        if stuff.texture:
            textures = [stuff.texture]
        else:
            return
    else:
        path = "data/textures"
        textures = [(path, "texture.tif")]
    for (folder, texfile) in textures:  
        path = export_config.getOutFileName(texfile, folder, True, human, the.Config)        
        (fname, ext) = os.path.splitext(texfile)  
        name = "%s_%s" % (fname, ext[1:])
        if the.Config.separatefolder:
            texpath = "textures/"+texfile
        else:
            texpath = texfile
        fp.write("map_Kd %s\n" % texpath)
    return

"""    
Ka 1.0 1.0 1.0
Kd 1.0 1.0 1.0
Ks 0.33 0.33 0.52
illum 5
Ns 50.0
map_Kd texture.png
"""