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

#
#    exportProxyObj(human, filename, proxyName):    
#    exportProxyObj1(obj, filename, proxy):
#

def exportProxyObj(human, name, proxyName):
    obj = human.meshData
    if proxyName:
        pfile = export_config.CProxyFile()
        pfile.type = 'Proxy'
        pfile.file = "./data/templates/%s.proxy" % proxyName.lower()
        proxy = mh2proxy.readProxyFile(obj, pfile)
        if proxy and proxy.name:
            filename = "%s_%s.obj" % (name.lower(), proxy.name)
            exportProxyObj1(obj, filename, proxy)
    
    cfg = export_config.exportConfig(human, False)
    for pfile in cfg.proxyList:
        if pfile.useObj and pfile.type != 'Proxy':
            proxy = mh2proxy.readProxyFile(obj, pfile)
            if proxy and proxy.name:
                filename = "%s_%s.obj" % (name.lower(), proxy.name)
                exportProxyObj1(obj, filename, proxy)
    return

def exportProxyObj1(obj, filename, proxy):
    fp = open(filename, 'w')
    fp.write(
"# MakeHuman exported OBJ for proxy mesh\n" +
"# www.makehuman.org\n\n")

    print("OBJ", len(proxy.realVerts))
    for bary in proxy.realVerts:
        (x,y,z) = mh2proxy.proxyCoord(bary)
        fp.write("v %.4f %.4f %.4f\n" % (x, y, z))

    for uv in proxy.texVerts:
        fp.write("vt %s %s\n" % (uv[0], uv[1]))

    mat = -1
    fn = 0
    grp = None
    for (f,g) in proxy.faces:
        if proxy.materials and proxy.materials[fn] != mat:
            mat = proxy.materials[fn]
            fp.write("usemtl %s\n" % matNames[mat])
        if g != grp:
            fp.write("g %s\n" % g)
            grp = g
        fp.write("f")
        if proxy.texFaces:
            ft = proxy.texFaces[fn]
            vn = 0
            for v in f:
                vt = ft[vn]
                fp.write(" %d/%d" % (v+1, vt+1))
                vn += 1
        else:
            for v in f:
                fp.write(" %d" % (v+1))
        fp.write("\n")
        fn += 1
    fp.close()
    return
    

