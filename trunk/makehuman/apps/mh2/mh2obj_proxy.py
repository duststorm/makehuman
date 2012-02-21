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

import export_config
import mh2proxy
import mh2collada
import mhx_globals as the

#
#    exportProxyObj(human, filename):    
#

def exportProxyObj(human, name, options):
    obj = human.meshData
    cfg = export_config.exportConfig(human, False)
    the.Options = options
    (the.Stuff, stuffs) = mh2collada.setupStuff(obj, {}, [], cfg)
    (scale, unit) = options["scale"]
    filename = "%s_clothed.obj" % name
    fp = open(filename, 'w')
    fp.write(
"# MakeHuman exported OBJ with clothes\n" +
"# www.makehuman.org\n\n")
    for stuff in stuffs:
        writeGeometry(obj, fp, stuff, scale)
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
