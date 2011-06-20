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


TO DO

"""

import module3d, aljabr
import os
from aljabr import *
import read_rig, mhx_rig, mh2mhx


#
#    safePrint( string, filename ):
#    Utility for evading encoding errors
#

def safePrint( string, filename ):
    try:
        print("%s %s" % (string, filename))
        return
    except:
        success = False
    if not success:
        ascii = ""
        space = ord(' ')
        z = ord('z')
        for c in filename:
            d = ord(c)
            if d < space or d > z:
                ascii += "\\x%x " % d
            else:
                ascii += chr(d)
        print("%s %s" % (string, ascii))

#
#    class CProxy
#

class CProxy:
    def __init__(self, typ, layer):
        self.name = None
        self.type = typ
        self.rig = None
        self.layer = layer
        self.material = None
        self.verts = {}
        self.realVerts = []
        self.faces = []
        self.texFaces = []
        self.texVerts = []
        self.materials = []
        self.constraints = []
        self.wire = False
        self.cage = False
        self.weightfile = None
        self.modifiers = []
        self.shapekeys = []
        self.bones = []
        self.weights = None
        return

#
#    class CMaterial
#

class CMaterial:
    def __init__(self, name):
        self.name = name
        self.settings = []
        self.texture = None
        self.textureSettings = []
        self.mtexSettings = []
        return
"""
        self.diffuse_color = None
        self.diffuse_intensity = None
        self.diffuse_shader = None
        self.specular_color = None
        self.specular_intensity = None
        self.specular_shader = None
        self.translucency = 0.0
        self.ambient_color = None
        self.emit_color = None
        return
"""
#
#    Flags
#

F_CON = 0x01

#
#    proxyFilePtr(name):
#

import mh

def proxyFilePtr(name):
    head = os.path.normpath(mh.getPath(''))
    for path in [head, './']:
        filename = os.path.realpath( os.path.join(path, name) )
        try:
            fp = open(filename, "r")
            safePrint("    Using config file", filename )
            return fp
        except:
            safePrint("*** Cannot open",  filename )
    return None
    
#
#    proxyConfig():
#

class CProxyConfig:
    def __init__(self):
        self.mainmesh = ['obj', 'mhx', 'dae']
        self.useRig = 'mhx'
        self.mhxversion = ['24', '25']
        self.proxyList = []
        self.expressions = True
        self.faceshapes = True
        self.bodyshapes = True
        self.cage = False

#[('mhxversion', ['25']), ('expressions', True), ('useRig', 'mhx')]
#[('mhxversion', ['24', '25']), ('expressions', False), ('useRig', 'game')]

def proxyConfig(options=None):
    cfg = CProxyConfig()
    typ = 'Proxy'
    layer = 2
    useMhx = True
    useObj = True
    useDae = True

    if options:
        print(options)
        cfg.mhxversion = options['mhxversion']
        cfg.expressions = options['expressions']
        cfg.useRig = options['useRig']
        fp = 0
    else:    
        fp = proxyFilePtr('proxy.cfg')

    if not fp: 
        for name in ['sweater', 'jeans']:
            proxyFile = os.path.expanduser("./data/templates/%s.mhclo" % name)
            cfg.proxyList.append(('Clothes', True, True, True, (proxyFile, 'Clothes', 4)))
        for name in ['Rorkimaru', 'ascottk']:
            proxyFile = os.path.expanduser("./data/templates/%s.proxy" % name)
            cfg.proxyList.append(('Proxy', True, True, True, (proxyFile, 'Proxy', 3)))
        return cfg

    for line in fp:
        words = line.split()
        if len(words) == 0 or words[0][0] == '#':
            pass
        elif words[0] == '@':
            key = words[1].lower()
            if key in ['mainmesh', 'mhxversion']:
                try:
                    exec("cfg.%s = words[2:]" % key)
                except:
                    pass
            elif key in ['expressions', 'faceshapes', 'bodyshapes']:
                try:
                    exec("cfg.%s = %s" % (key, words[2]))
                except:
                    pass
            elif key == 'rig':
                try:
                    cfg.useRig = words[2].lower()
                except:
                    pass
            elif key == 'obj':
                try:
                    useObj = eval(words[2])
                except:
                    pass
            elif key == 'mhx':
                try:
                    useMhx = eval(words[2])
                except:
                    pass
            elif key == 'dae':
                try:
                    useDae = eval(words[2])
                except:
                    pass
            elif key == 'proxy':
                typ = 'Proxy'
                typ = key.capitalize()
                layer = int(words[2])
            elif key == 'cage':
                typ = 'Cage'
                typ = key.capitalize()
                layer = int(words[2])
            elif key == 'clothes':
                typ = 'Clothes'
                typ = key.capitalize()
                layer = int(words[2])
            else:
                raise NameError('Unrecognized command %s in proxy.cfg' % words[1])
        else:
            proxyFile = os.path.expanduser(words[0])
            if typ == 'Cage':
                cfg.cage = True
            cfg.proxyList.append((typ, useObj, useMhx, useDae, (proxyFile, typ, layer)))
    fp.close()
    print "Proxy configuration: Use %s" % cfg.mainmesh
    for elt in cfg.proxyList:
        print "  ", elt
    return cfg

    
#
#    readProxyFile(obj, proxyStuff):
#

def readProxyFile(obj, proxyStuff):
    if not proxyStuff:
        return CProxy('Proxy', 2)

    (proxyFile, typ, layer) = proxyStuff
    try:
        tmpl = open(proxyFile, "rU")
    except:
        tmpl = None
    if tmpl == None:
        print("*** Cannot open %s" % proxyFile)
        return CProxy(typ, layer)

    verts = obj.verts
    locations = {}
    tails = {}
    proxy = CProxy(typ, layer)
    proxy.name = "MyProxy"

    status = 0
    doVerts = 1
    doFaces = 2
    doMaterial = 3
    doTexVerts = 4
    doObjData = 5
    doWeights = 6

    vn = 0
    for line in tmpl:
        words= line.split()
        if len(words) == 0:
            pass
        elif words[0] == '#':
            theGroup = None
            if len(words) == 1:
                pass
            elif words[1] == 'verts':
                status = doVerts
            elif words[1] == 'faces':
                status = doFaces
            elif words[1] == 'weights':
                status = doWeights
                if proxy.weights == None:
                    proxy.weights = {}
                weights = []
                proxy.weights[words[2]] = weights
            elif words[1] == 'material':
                status = doMaterial
                proxy.material = CMaterial(words[2])
            elif words[1] == 'texVerts':
                status = doTexVerts
            elif words[1] == 'obj_data':
                status = doObjData
            elif words[1] == 'name':
                proxy.name = words[2]
            elif words[1] == 'rig':
                proxy.rig = words[2]
            elif words[1] == 'wire':
                proxy.wire = True
            elif words[1] == 'cage':
                proxy.cage = True
            elif words[1] == 'weightfile':
                proxy.weightfile = (words[2], words[3])
            elif words[1] == 'subsurf':
                subdiv = int(words[2])
                proxy.modifiers.append( ['subsurf', subdiv] )
            elif words[1] == 'shrinkwrap':
                offset = float(words[2])
                proxy.modifiers.append( ['shrinkwrap', offset] )
            elif words[1] == 'shapekey':
                proxy.shapekeys.append( words[2] )
        elif status == doObjData:
            if words[0] == 'vt':
                newTexVert(1, words, proxy)
            elif words[0] == 'f':
                newFace(1, words, theGroup, proxy)
            elif words[0] == 'g':
                theGroup = words[1]
        elif status == doVerts:
            v0 = int(words[0])
            v1 = int(words[1])
            v2 = int(words[2])
            w0 = float(words[3])
            w1 = float(words[4])
            w2 = float(words[5])
            try:
                proj = float(words[6])
            except:
                proj = 0

            if proj:
                n0 = aljabr.vmul(verts[v0].no, w0)
                n1 = aljabr.vmul(verts[v1].no, w1)
                n2 = aljabr.vmul(verts[v2].no, w2)
                norm = aljabr.vadd(n0, n1)
                norm = aljabr.vadd(norm, n2)
                d0 = proj*norm[0]
                d1 = proj*norm[1]
                d2 = proj*norm[2]
            else:
                (d0, d1, d2) = (0, 0, 0)

            proxy.realVerts.append((verts[v0], verts[v1], verts[v2], w0, w1, w2, d0, d1, d2))
            addProxyVert(v0, vn, w0, proxy)
            addProxyVert(v1, vn, w1, proxy)
            addProxyVert(v2, vn, w2, proxy)
            vn += 1
        elif status == doFaces:
            newFace(0, words, theGroup, proxy)
        elif status == doTexVerts:
            newTexVert(0, words, proxy)
        elif status == doMaterial:
            readMaterial(line, proxy.material)
        elif status == doWeights:
            v = int(words[0])
            w = float(words[1])
            weights.append((v,w))

    return proxy

#
#    readMaterial(line, mat):
#

def readMaterial(line, mat):
    words= line.split()
    key = words[0]
    if key in ['diffuse_color', 'specular_color', 'ambient_color', 'emit_color']:
        mat.settings.append( (key, [float(words[1]), float(words[2]), float(words[3])]) )
    elif key in ['diffuse_shader', 'specular_shader']:
        mat.settings.append( (key, words[1]) )
    elif key in ['use_shadows', 'use_transparent_shadows', 'use_transparency']:
        mat.settings.append( (key, int(words[1])) )
    elif key in ['diffuse_intensity', 'specular_intensity', 'specular_hardness', 'translucency', 
        'alpha', 'specular_alpha']:
        mat.settings.append( (key, float(words[1])) )
    elif key == 'texture':
        mat.texture = words[1]
    elif key in ['diffuse_color_factor', 'alpha_factor', 'translucency_factor']:
        mat.mtexSettings.append( (key, float(words[1])) )
    elif key in ['use_map_color_diffuse', 'use_map_alpha']:
        mat.mtexSettings.append( (key, int(words[1])) )
    elif key in ['use_alpha']:
        mat.textureSettings.append( (key, int(words[1])) )
    else:
        raise NameError("Material %s?" % key)

#
#    getLoc(joint, obj):
#

import mhxbones

def getJoint(joint, obj, locations):
    try:
        loc = locations[joint]
    except:
        loc = mhxbones.calcJointPos(obj, joint)
        locations[joint] = loc
    return loc

#
#    writeProxyArmature(fp, obj, proxy)
#    writeRigBones(fp, bones):
#    writeRigPose(fp, name, bones):
#    writeRigWeights(fp, weights):
#

def writeProxyArmature(fp, obj, proxy):
    if not proxy.rig:
        return
    (locs, proxy.bones, proxy.weights) = read_rig.readRigFile(proxy.rig, obj)
    writeRigBones(fp, proxy.bones)
    return

def writeRigBones(fp, bones):
    ox = mhx_rig.Origin[0]
    oy = mhx_rig.Origin[1]
    oz = mhx_rig.Origin[2]
    for (bone, head, tail, roll, parent, options) in bones:
        fp.write("\n  Bone %s True\n" % bone)
        (x, y, z) = head
        fp.write("    head  %.4f %.4f %.4f  ;\n" % (x-ox,-z+oz,y-oy))
        (x, y, z) = tail
        fp.write("    tail %.4f %.4f %.4f  ;\n" % (x-ox,-z+oz,y-oy))
        if parent and parent != '-':
            fp.write("    parent Refer Bone %s ;\n" % parent)
        fp.write(
    "    roll %.4f ; \n" % (roll)+
    "    use_connect False ; \n")
        if ('-circ' in options.keys() or '-box' in options.keys()):
            fp.write("    show_wire True ;\n")
        try:
            options['-nd']
            fp.write("    use_deform False ; \n")
        except:
            fp.write("    use_deform True ; \n")
        fp.write("  end Bone \n")
    return

def getRadius(key, options):
    try:
        val = options[key]
        return int(val[0])
    except:
        return None

def writeRigPose(fp, name, bones):
    circles = []
    cubes = []
    for (bone, head, tail, roll, parent, options) in bones:
        r = getRadius('-circ', options)
        if r and not (r in circles):
            mhx_rig.setupCircle(fp, "RigCircle%02d" % r, 0.1*r)
            circles.append(r)
        r = getRadius('-box', options)
        if r and not (r in cubes):
            mhx_rig.setupCube(fp, "RigCube%02d" % r, 0.1*r, 0)
            cubes.append(r)

    fp.write("\nPose %s\n" % name)
    for (bone, head, tail, roll, parent, options) in bones:
        fp.write("  Posebone %s True \n" % bone)

        # IK constraint
        try:
            val = options['-ik']
        except:
            val = None
        if val:
            (subtar, chainlen, inf) = val
            fp.write(
"    Constraint IK IK True\n")
            if subtar:
                fp.write(
"      target Refer Object %s ;\n" % name +
"      subtarget '%s' ;\n" % subtar +
"      use_tail True ;\n" +
"      use_target True ;\n")
            else:
                fp.write(
"      use_tail False ;\n" +
"      use_target True ;\n")
            fp.write(
"      chain_count %s ;\n" % chainlen +
"      influence %s ;\n" % inf +
"    end Constraint\n")

        # Not connected
        try:
            options['-nc']
        except:
            fp.write(
"    lock_location Array 1 1 1 ;\n" +
"    lock_scale Array 1 1 1  ; \n")

        # Circle custom shape
        r = getRadius('-circ', options)
        if r:
            fp.write(
"    custom_shape Refer Object RigCircle%02d ; \n" % r)

        # Box custom shape
        r = getRadius('-box', options)
        if r:
            fp.write(
"    custom_shape Refer Object RigCube%02d ; \n" % r)

        fp.write("  end Posebone\n")
    fp.write("end Pose\n\n")

def writeRigWeights(fp, weights):
    for grp in weights.keys():
        fp.write("\n  VertexGroup %s\n" % grp)
        for (v,w) in weights[grp]:
            fp.write("    wv %d %.4f ;\n" % (v,w))
        fp.write("  end VertexGroup\n")
    return

#
#    newFace(first, words, group, proxy):
#    newTexVert(first, words, proxy):
#    addProxyVert(v, vn, w, proxy):
#

def newFace(first, words, group, proxy):
    face = []
    texface = []
    nCorners = len(words)
    for n in range(first, nCorners):
        numbers = words[n].split('/')
        face.append(int(numbers[0])-1)
        if len(numbers) > 1:
            texface.append(int(numbers[1])-1)
    proxy.faces.append((face,group))
    if texface:
        proxy.texFaces.append(texface)
        if len(face) != len(texface):
            raise NameError("texface %s %s", face, texface)
    return

def newTexVert(first, words, proxy):
    vt = []
    nCoords = len(words)
    for n in range(first, nCoords):
        uv = float(words[n])
        vt.append(uv)
    proxy.texVerts.append(vt)
    return

def addProxyVert(v, vn, w, proxy):
    try:
        proxy.verts[v].append((vn, w))
    except:
        proxy.verts[v] = [(vn,w)]
    return

#
#    proxyCoord(barycentric):
#

def proxyCoord(barycentric):
    (v0, v1, v2, w0, w1, w2, d0, d1, d2) = barycentric
    x = w0*v0.co[0] + w1*v1.co[0] + w2*v2.co[0] + d0
    y = w0*v0.co[1] + w1*v1.co[1] + w2*v2.co[1] + d1
    z = w0*v0.co[2] + w1*v1.co[2] + w2*v2.co[2] + d2
    return [x,y,z]

#
#    getMeshInfo(obj, proxy, rawWeights, rawShapes, rigname):
#

def getMeshInfo(obj, proxy, rawWeights, rawShapes, rigname):
    if proxy:
        verts = []
        vnormals = []
        for bary in proxy.realVerts:
            v = proxyCoord(bary)
            verts.append(v)
            vnormals.append(v)

        faces = []
        fn = 0
        for (f,g) in proxy.faces:
            texFace = proxy.texFaces[fn]
            face = []
            for (vn,v) in enumerate(f):
                face.append((v, texFace[vn]))
            faces.append(face)
            fn += 1

        weights = None
        shapes = []
        if proxy.rig:
            weights = rawWeights
            shapes = rawShapes
        elif rigname and proxy.weightfile:
            (name, fileName) = proxy.weightfile
            if rigname == name:
                (locs, amt, weights) = read_rig.readRigFile(fileName, obj)

        if not weights:
            weights = getProxyWeights(rawWeights, proxy)
            shapes = getProxyShapes(rawShapes, proxy.verts)
        return (verts, vnormals, proxy.texVerts, faces, weights, shapes)
    else:
        verts = []
        vnormals = []
        for v in obj.verts:
            verts.append(v.co)
            vnormals.append(v.no)
        faces = mh2mhx.loadFacesIndices(obj)
        return (verts, vnormals, obj.uvValues, faces, rawWeights, rawShapes)

#
#    getProxyWeights(rawWeights, proxy):
#    fixProxyVGroup(fp, vgroup):
#

def getProxyWeights(rawWeights, proxy):
    weights = {}
    for key in rawWeights.keys():
        vgroup = []
        for (v,wt) in rawWeights[key]:
            try:
                vlist = proxy.verts[v]
            except:
                vlist = []
            for (pv, w) in vlist:
                vgroup.append((pv, w*wt))
        weights[key] = fixProxyVGroup(vgroup)
    return weights

def fixProxyVGroup(vgroup):
    fixedVGroup = []
    vgroup.sort()
    pv = -1
    while vgroup:
        (pv0, wt0) = vgroup.pop()
        if pv0 == pv:
            wt += wt0
        else:
            if pv >= 0 and wt > 1e-4:
                fixedVGroup.append((pv, wt))
            (pv, wt) = (pv0, wt0)
    if pv >= 0 and wt > 1e-4:
        fixedVGroup.append((pv, wt))
    return fixedVGroup

#
#    getProxyShapes(rawShapes, proxy):
#    fixProxyShape(fp, shape)
#

def getProxyShapes(rawShapes, proxy):
    shapes = []
    for (key, rawShape) in rawShapes:
        shape = []
        for (v,(dx,dy,dz)) in rawShape.items():
            try:
                vlist = proxy.verts[v]
            except:
                vlist = []
            for (pv, w) in vlist:
                shape.append((pv, w*dx, w*dy, w*dz))
        fixedShape = fixProxyShape(fp, shape)

        shape = {}
        for (v,dx,dy,dz) in fixedShape:
            shape[v] = (dx,dy,dz)
        shapes.append(shape)
    return shapes

def fixProxyShape(shape):
    fixedShape = []
    shape.sort()
    pv = -1
    while shape:
        (pv0, dx0, dy0, dz0) = shape.pop()
        if pv0 == pv:
            dx += dx0
            dy += dy0
            dz += dz0
        else:
            if pv >= 0 and (dx > 1e-4 or dy > 1e-4 or dz > 1e-4):
                fixedShape.append((pv, dx, dy, dz))
            (pv, dx, dy, dz) = (pv0, dx0, dy0, dz0)        
    if pv >= 0 and (dx > 1e-4 or dy > 1e-4 or dz > 1e-4):
        fixedShape.append((pv, dx, dy, dz))
    return fixedShape

#
#    exportProxyObj(obj, filename):    
#    exportProxyObj1(obj, filename, proxy):
#

def exportProxyObj(obj, name):
    cfg = proxyConfig()
    for (typ, useObj, useMhx, useDae, proxyStuff) in cfg.proxyList:
        if useObj:
            proxy = readProxyFile(obj, proxyStuff)
            if proxy.name:
                filename = "%s_%s.obj" % (name.lower(), proxy.name)
                exportProxyObj1(obj, filename, proxy)
    return

def exportProxyObj1(obj, filename, proxy):
    fp = open(filename, 'w')
    fp.write(
"# MakeHuman exported OBJ for proxy mesh\n" +
"# www.makehuman.org\n\n")

    for bary in proxy.realVerts:
        (x,y,z) = proxyCoord(bary)
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
    

