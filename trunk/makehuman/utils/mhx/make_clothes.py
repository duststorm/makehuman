""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
Utility for making clothes to MH characters.

For more info see: http://sites.google.com/site/makehumandocs/blender-export-and-mhx/making-clothes

"""

bl_addon_info = {
    "name": "Make clothes to MakeHuman",
    "author": "Thomas Larsson",
    "version": 0.5,
    "blender": (2, 5, 9),
    "api": 40000,
    "location": "View3D > Properties > Make MH clothes",
    "description": "Make clothes for MakeHuman characters",
    "warning": "",
    "category": "3D View"}


import bpy
import os
import mathutils
import random

#
#   Global variables
#

theThreshold = -0.2
theListLength = 3
Epsilon = 1e-4
# Number of verts which are body, not clothes
NBodyVerts = 15340


#
#   isHuman(ob):
#   isClothing(ob):
#   getHuman(context):
#   getClothing(context):
#   getObjectPair(context):
#

def isHuman(ob):
    try:
        return ob["MhxMesh"]
    except:
        return False                
        
def isClothing(ob):
    return ((ob.type == 'MESH') and (not isHuman(ob)))
    
def getHuman(context):
    ob = context.object
    if not isHuman(ob):
        raise NameError("Object %s is not human" % ob.name)
    return ob
        
def getClothing(context):        
    ob = context.object
    if isHuman(ob):
        raise NameError("Object %s is a human, not a clothing" % ob.name)
    return ob
    
def getObjectPair(context):
    human = None
    clothing = None
    scn = context.scene
    for ob in scn.objects:
        if ob.select:
            if isHuman(ob):
                if human:
                    raise NameError("Two humans selected: %s and %s" % (human.name, ob.name))
                else:
                    human = ob
            elif ob.type == 'MESH':
                if clothing:
                    raise NameError("Two pieces of clothing selected: %s and %s" % (clothing.name, ob.name))
                else:
                    clothing = ob
    if not human:
        raise NameError("No human selected")
    if scn["MakeClothesSelfClothed"]:
        if clothing:
            raise NameError("Clothing %s selected but human %s is self-clothed" % (clothing.name, human.name))
        checkObjectOK(human, context)
        nverts = len(human.data.vertices)
        clothing = copyObject(human, NBodyVerts, nverts, context, "Clothing")
        base = copyObject(human, 0, NBodyVerts, context, "Base")
        return (base, clothing)
    elif not clothing:
        raise NameError("No clothing selected")
    return (human, clothing)  
    
def copyObject(human, n0, n1, context, name):
    scn = context.scene
    for ob in scn.objects:
        ob.select = False
    human.select = True
    scn.objects.active = human
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.duplicate(linked=False)
    ob = context.object
    ob.name = name
    ob.data.name = name
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    print(context.object, context.object.data)
    for n in range(n0,n1):
        ob.data.vertices[n].select = False
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    return ob

#
#    printMverts(stuff, mverts):
#

def printMverts(stuff, mverts):
    for n in range(theListLength):
        (v,dist) = mverts[n]
        if v:
            print(stuff, v.index, dist)

#
#    selectVert(context, vn, ob):
#

def selectVert(context, vn, ob):
    context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    ob.data.vertices[vn].select = True
    return    

#
#   goodName(name):    
#   getFileName(pob, context, ext):            
#

def goodName(name):    
    newName = name.replace('-','_')
    return newName.lower()
    
def getFileName(pob, context, ext):            
    name = goodName(pob.name)
    outpath = '%s/%s' % (context.scene['MakeClothesDirectory'], name)
    outpath = os.path.realpath(os.path.expanduser(outpath))
    if not os.path.exists(outpath):
        print("Creating directory %s" % outpath)
        os.mkdir(outpath)
    outfile = os.path.join(outpath, "%s.%s" % (name, ext))
    return (outpath, outfile)
    
#
#
#

ShapeKeys = [
    'Breathe',
    ]

#
#    findClothes(context, bob, pob, log):
#

def findClothes(context, bob, pob, log):
    base = bob.data
    proxy = pob.data
    scn = context.scene
    
    bestVerts = []
    for pv in proxy.vertices:
        try:
            pindex = pv.groups[0].group
        except:
            pindex = -1
        if pindex < 0:
            vn = pv.index
            selectVert(context, vn, pob)
            raise NameError("Clothes %s vert %d not member of any group" % (pob.name, vn))

        gname = pob.vertex_groups[pindex].name
        bindex = None
        for bvg in bob.vertex_groups:
            if bvg.name == gname:
                bindex = bvg.index
        if bindex == None:
            raise NameError("Did not find vertex group %s in base mesh" % gname)            

        mverts = []
        for n in range(theListLength):
            mverts.append((None, 1e6))

        exact = False
        for bv in base.vertices:
            if exact:
                break
            for grp in bv.groups:
                if grp.group == bindex:
                    vec = pv.co - bv.co
                    n = 0
                    for (mv,mdist) in mverts:
                        if vec.length < Epsilon:
                            mverts[0] = (bv, -1)
                            exact = True
                            break
                        if vec.length < mdist:
                            for k in range(n+1, theListLength):
                                j = theListLength-k+n
                                mverts[j] = mverts[j-1]
                            mverts[n] = (bv, vec.length)
                            #print(bv.index)
                            #printMverts(bv.index, mverts)
                            break
                        n += 1

        (mv, mindist) = mverts[0]
        if mv:
            if pv.index % 10 == 0:
                print(pv.index, mv.index, mindist, gname, pindex, bindex)
            if log:
                log.write("%d %d %.5f %s %d %d\n" % (pv.index, mv.index, mindist, gname, pindex, bindex))
            #printMverts("  ", mverts)
        else:
            print("*** %d (%.4f %.4f %.4f) %s" % (pv.index, pv.co[0], pv.co[1], pv.co[2], gname))
            raise NameError("Failed to find vert %d in group %s %d %d" % (pv.index, gname, pindex, bindex))
        if mindist > 5:
            print("*** %d (%.4f %.4f %.4f) %s" % (pv.index, pv.co[0], pv.co[1], pv.co[2], gname))
            raise NameError("Minimal distance %f > 5.0. Check base and proxy scales." % mindist)

        if gname[0:3] != "Mid":
            bindex = -1
        bestVerts.append((pv, bindex, exact, mverts, []))

    print("Setting up face table")
    vfaces = {}
    for v in base.vertices:
        vfaces[v.index] = []            
    for f in base.faces:
        v0 = f.vertices[0]
        v1 = f.vertices[1]
        v2 = f.vertices[2]
        if len(f.vertices) == 4:
            v3 = f.vertices[3]
            t0 = [v0,v1,v2]
            t1 = [v1,v2,v3]
            t2 = [v2,v3,v0]
            t3 = [v3,v0,v1]
            vfaces[v0].extend( [t0,t2,t3] )
            vfaces[v1].extend( [t0,t1,t3] )
            vfaces[v2].extend( [t0,t1,t2] )
            vfaces[v3].extend( [t1,t2,t3] )
        else:
            t = [v0,v1,v2]
            vfaces[v0].append(t)
            vfaces[v1].append(t)
            vfaces[v2].append(t)
    
    print("Finding weights")
    for (pv, bindex, exact, mverts, fcs) in bestVerts:
        if exact:
            continue
        for (bv,mdist) in mverts:
            if bv:
                for f in vfaces[bv.index]:
                    v0 = base.vertices[f[0]]
                    v1 = base.vertices[f[1]]
                    v2 = base.vertices[f[2]]
                    if (bindex >= 0) and (pv.co[0] < 0.01) and (pv.co[0] > -0.01):
                        wts = midWeights(pv, bindex, v0, v1, v2, pob)    
                    else:
                        wts = cornerWeights(pv, v0.co, v1.co, v2.co, pob)
                    fcs.append((f, wts))

    print("Finding best weights")
    alwaysOutside = False
    minOffset = 0.0
    useProjection = False
    
    bestFaces = []
    print("Optimal triangles not found for the following verts")
    for (pv, bindex, exact, mverts, fcs) in bestVerts:
        #print(pv.index)
        pv.select = False
        if exact:
            bestFaces.append((pv, True, mverts, 0, 0))
            continue
        minmax = -1e6
        for (fverts, wts) in fcs:
            w = minWeight(wts)
            if w > minmax:
                minmax = w
                bWts = wts
                bVerts = fverts
        if minmax < theThreshold:
            print(pv.index)
            pv.select = True
            """
            if scn['MakeClothesForbidFailures']:
                vn = pv.index
                selectVert(context, vn, pob)
                print("Tried", mverts)
                msg = (
                "Did not find optimal triangle for %s vert %d.\n" % (pob.name, vn) +
                "Avoid the message by unchecking Forbid failures.")
                raise NameError(msg)
            """
            (mv, mdist) = mverts[0]
            bVerts = [mv.index,0,1]
            bWts = (1,0,0)

        v0 = base.vertices[bVerts[0]]
        v1 = base.vertices[bVerts[1]]
        v2 = base.vertices[bVerts[2]]
    
        est = bWts[0]*v0.co + bWts[1]*v1.co + bWts[2]*v2.co
        norm = bWts[0]*v0.normal + bWts[1]*v1.normal + bWts[2]*v2.normal
        diff = pv.co - est
        if useProjection:
            proj = diff.dot(norm)
            if alwaysOutside and proj < minOffset:
                proj = minOffset
            bestFaces.append((pv, False, bVerts, bWts, proj))    
        else:
            bestFaces.append((pv, False, bVerts, bWts, diff))    

    print("Done")
    return bestFaces

#
#    minWeight(wts)
#

def minWeight(wts):
    best = 1e6
    for w in wts:
        if w < best:
            best = w
    return best

#
#    cornerWeights(pv, r0, r1, r2, pob):
#
#    px = w0*x0 + w1*x1 + w2*x2
#    py = w0*y0 + w1*y1 + w2*y2
#    pz = w0*z0 + w1*z1 + w2*z2
#
#    w2 = 1-w0-w1
#
#    w0*(x0-x2) + w1*(x1-x2) = px-x2
#    w0*(y0-y2) + w1*(y1-y2) = py-y2
#
#    a00*w0 + a01*w1 = b0
#    a10*w0 + a11*w1 = b1
#
#    det = a00*a11 - a01*a10
#
#    det*w0 = a11*b0 - a01*b1
#    det*w1 = -a10*b0 + a00*b1
#

def cornerWeights(pv, r0, r1, r2, pob):
    u01 = r1-r0
    u02 = r2-r0
    n = u01.cross(u02)
    n.normalize()

    u = pv.co-r0
    r = r0 + u - n*u.dot(n)

    '''
    print(list(pv))
    print(" r  ", list(r))
    print(" r0 ", list(r0))
    print(" r1 ", list(r1))
    print(" r2 ", list(r2))
    print(" n  ", list(n))
    '''

    a00 = r0[0]-r2[0]
    a01 = r1[0]-r2[0]
    a10 = r0[1]-r2[1]
    a11 = r1[1]-r2[1]
    b0 = r[0]-r2[0]
    b1 = r[1]-r2[1]
    
    det = a00*a11 - a01*a10
    if abs(det) < 1e-20:
        print("Clothes vert %d mapped to degenerate triangle (det = %g) with corners" % (pv.index, det))
        print("r0", r0[0], r0[1], r0[2])
        print("r1", r1[0], r1[1], r1[2])
        print("r2", r2[0], r2[1], r2[2])
        highlight(pv, pob)
        raise NameError("Singular matrix in cornerWeights")

    w0 = (a11*b0 - a01*b1)/det
    w1 = (-a10*b0 + a00*b1)/det
    
    return (w0, w1, 1-w0-w1)

#
#   midWeights(pv, bindex, v0, v1, v2, pob):
#

def midWeights(pv, bindex, v0, v1, v2, pob):
    #print("Mid", pv.index, bindex)
    pv.select = True
    if isInGroup(v0, bindex):
        v0.select = True
        if isInGroup(v1, bindex):
            v1.select = True    
            return midWeight(pv, v0.co, v1.co)
        elif isInGroup(v2, bindex):
            (w1, w0, w2) = midWeight(pv, v0.co, v2.co)
            v2.select = True
            return (w0, w1, w2)
    elif isInGroup(v1, bindex) and isInGroup(v2, bindex):            
        (w1, w2, w0) = midWeight(pv, v1.co, v2.co)
        v1.select = True
        v2.select = True
        return (w0, w1, w2)
    #print("  Failed mid")
    return cornerWeights(pv, v0.co, v1.co, v2.co, pob)
    
def isInGroup(v, bindex):
    for g in v.groups:
        if g.group == bindex:
            return True
    return False            
    
def midWeight(pv, r0, r1):
    u01 = r1-r0    
    d01 = u01.length
    u = pv.co-r0
    s = u.dot(u01)
    w = s/(d01*d01)
    return (1-w, w, 0)

#
#    highlight(pv, ob):
#

def highlight(pv, ob):
    me = ob.data
    for v in me.vertices:
        v.select = False
    pv.select = True
    return
    
#
#    proxyFilePtr(name):
#

def proxyFilePtr(name):
    for path in ['~/makehuman/', '~/documents/makehuman/', '/']:
        fileName = os.path.realpath(os.path.expanduser(path+name))
        try:
            fp = open(fileName, "r")
            print("Using header file %s" % fileName)
            return fp
        except:
            print("No file %s" % fileName)
    return None

#
#    printClothes(context, path, file, bob, pob, data):    
#
        
def printClothes(context, path, file, bob, pob, data):
    scn = context.scene
    fp= open(file, "w")

    infp = proxyFilePtr('proxy_header.txt')
    if infp:
        for line in infp:
            fp.write('# '+line)
    else:
        fp.write(
"# author Unknown\n" +
"# license GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)\n" +
"# homepage http://www.makehuman.org/\n")

    fp.write("# name %s\n" % pob.name)
    fp.write("# obj_file %s.obj\n" % goodName(pob.name))
    printScale(fp, bob, scn, 'x_scale', 0, 'MakeClothesX1', 'MakeClothesX2')
    printScale(fp, bob, scn, 'z_scale', 1, 'MakeClothesY1', 'MakeClothesY2')
    printScale(fp, bob, scn, 'y_scale', 2, 'MakeClothesZ1', 'MakeClothesZ2')

    if scn["MakeClothesSelfClothed"]:
        firstVert = NBodyVerts
    else:
        printStuff(fp, pob, scn)
        firstVert = 0
    useProjection = False
    fp.write("# use_projection %d\n" % useProjection)
    fp.write("# verts %d\n" % firstVert)
    if useProjection:
        for (pv, exact, verts, wts, proj) in data:
            if exact:
                (bv, dist) = verts[0]
                fp.write("%5d\n" % bv.index)
            else:
                fp.write("%5d %5d %5d %.5f %.5f %.5f %.5f\n" % (
                    verts[0], verts[1], verts[2], wts[0], wts[1], wts[2], proj))
    else:                
        for (pv, exact, verts, wts, diff) in data:
            if exact:
                (bv, dist) = verts[0]
                fp.write("%5d\n" % bv.index)
            else:
                fp.write("%5d %5d %5d %.5f %.5f %.5f %.5f %.5f %.5f\n" % (
                    verts[0], verts[1], verts[2], wts[0], wts[1], wts[2], diff[0], diff[2], -diff[1]))
    fp.write('\n')
    fp.close()
    return
      
#
#   printStuff(fp, pob, scn):    
#

def printStuff(fp, pob, scn):    
    fp.write("# z_depth %d\n" % scn["MakeClothesZDepth"])
    
    for mod in pob.modifiers:
        if mod.type == 'SHRINKWRAP':
            fp.write("# shrinkwrap %.3f\n" % (mod.offset))
        elif mod.type == 'SUBSURF':
            fp.write("# subsurf %d %d\n" % (mod.levels, mod.render_levels))
            
    for skey in ShapeKeys:            
        if scn['MakeClothes' + skey]:
            fp.write("# shapekey %s\n" % skey)            
            
    fp.write("# texture %s_texture.tif\n" % pob.name.lower())
    #if scn['MakeClothesMask']:
    fp.write("# mask %s_mask.png\n" % pob.name.lower())
           
    if scn['MakeClothesHairMaterial']:
        fp.write(
"# material %s\n" % pob.name +
"texture data/hairstyles/%s_texture.tif\n" % pob.name +
"diffuse_intensity 0.8\n" +
"specular_intensity 0.0\n" +
"specular_hardness 1\n" +
"use_shadows 1\n" +
"use_transparent_shadows 1\n" +
"use_raytrace 0\n" +
"use_transparency 1\n" +
"alpha 0.0\n" +
"specular_alpha 0.0\n" +
"use_map_color_diffuse 1\n" +
"use_map_alpha 1\n" +
"use_alpha 1\n" +
"diffuse_color_factor 1.0\n" +
"alpha_factor 1.0\n")

    me = pob.data

    useMats = scn['MakeClothesMaterials']
    useBlender = scn['MakeClothesBlenderMaterials']
    if me.materials and (useMats or useBlender) and me.materials[0]:
        mat = me.materials[0]
        fp.write("# material %s\n" % mat.name)
        if useMats:
            writeColor(fp, 'diffuse_color', mat.diffuse_color)
            fp.write('diffuse_shader %s\n' % mat.diffuse_shader)
            fp.write('diffuse_intensity %.4f\n' % mat.diffuse_intensity)
            writeColor(fp, 'specular_color', mat.specular_color)
            fp.write('specular_shader %s\n' % mat.specular_shader)
            fp.write('specular_intensity %.4f\n' % mat.specular_intensity)
        if useBlender:
            mhxfile = exportBlenderMaterial(me, path)
            fp.write("# material_file %s\n" % mhxfile)
    return            

#
#   exportObjFile(context):
#

def exportObjFile(context):
    ob = getClothing(context)
    (objpath, objfile) = getFileName(ob, context, "obj")
    print("Open", objfile)
    fp = open(objfile, "w")
    fp.write("# Exported from make_clothes.py\n")
    
    scn = context.scene
    me = ob.data
    for v in me.vertices:
        fp.write("v %.4f %.4f %.4f\n" % (v.co[0], v.co[2], -v.co[1]))
        
    for v in me.vertices:
        fp.write("vn %.4f %.4f %.4f\n" % (v.normal[0], v.normal[2], -v.normal[1]))
        
    if me.uv_textures:
        (vertEdges, vertFaces, edgeFaces, faceEdges, faceNeighbors, uvFaceVerts, texVerts, nTexVerts) = setupTexVerts(ob)
        for vtn in range(nTexVerts):
                vt = texVerts[vtn]
                fp.write("vt %.4f %.4f\n" % (vt[0], vt[1]))
        for f in me.faces:
            uvVerts = uvFaceVerts[f.index]
            fp.write("f ")
            for n,v in enumerate(f.vertices):
                (vt, uv) = uvVerts[n]
                fp.write("%d/%d " % (v+1, vt+1))
            fp.write("\n")
    else:
        for f in me.faces:
            fp.write("f ")
            for v in f.vertices:
                fp.write("%d " % (v+1))
            fp.write("\n")

    fp.close()
    print(objfile, "closed")
    return

def writeColor(fp, string, color):
    fp.write("%s %.4f %.4f %.4f\n" % (string, color[0], color[1], color[2]))

def printScale(fp, bob, scn, name, index, prop1, prop2):
    verts = bob.data.vertices
    n1 = scn[prop1]
    n2 = scn[prop2]
    if n1 >=0 and n2 >= 0:
        x1 = verts[n1].co[index]     
        x2 = verts[n2].co[index]
        fp.write("# %s %d %d %.4f\n" % (name, n1, n2, abs(x1-x2)))
    return

#
#   setupTexVerts(ob):
#

def setupTexVerts(ob):
    vertEdges = {}
    vertFaces = {}
    for v in ob.data.vertices:
        vertEdges[v.index] = []
        vertFaces[v.index] = []
    for e in ob.data.edges:
        for vn in e.vertices:
            vertEdges[vn].append(e)
    for f in ob.data.faces:
        for vn in f.vertices:
            vertFaces[vn].append(f)
    
    edgeFaces = {}
    for e in ob.data.edges:
        edgeFaces[e.index] = []
    faceEdges = {}
    for f in ob.data.faces:
        faceEdges[f.index] = []
    for f in ob.data.faces:
        for vn in f.vertices:
            for e in vertEdges[vn]:
                v0 = e.vertices[0]
                v1 = e.vertices[1]
                if (v0 in f.vertices) and (v1 in f.vertices):
                    if f not in edgeFaces[e.index]:
                        edgeFaces[e.index].append(f)
                    if e not in faceEdges[f.index]:
                        faceEdges[f.index].append(e)
            
    faceNeighbors = {}
    uvFaceVerts = {}
    for f in ob.data.faces:
        faceNeighbors[f.index] = []
        uvFaceVerts[f.index] = []
    for f in ob.data.faces:
        for e in faceEdges[f.index]:
            for f1 in edgeFaces[e.index]:
                if f1 != f:
                    faceNeighbors[f.index].append((e,f1))

    uvtex = ob.data.uv_textures[0]
    vtn = 0
    texVerts = {}    
    for f in ob.data.faces:
        uvf = uvtex.data[f.index]
        vtn = findTexVert(uvf.uv1, vtn, f, faceNeighbors, uvFaceVerts, texVerts, ob)
        vtn = findTexVert(uvf.uv2, vtn, f, faceNeighbors, uvFaceVerts, texVerts, ob)
        vtn = findTexVert(uvf.uv3, vtn, f, faceNeighbors, uvFaceVerts, texVerts, ob)
        if len(f.vertices) > 3:
            vtn = findTexVert(uvf.uv4, vtn, f, faceNeighbors, uvFaceVerts, texVerts, ob)
    return (vertEdges, vertFaces, edgeFaces, faceEdges, faceNeighbors, uvFaceVerts, texVerts, vtn)     

def findTexVert(uv, vtn, f, faceNeighbors, uvFaceVerts, texVerts, ob):
    for (e,f1) in faceNeighbors[f.index]:
        for (vtn1,uv1) in uvFaceVerts[f1.index]:
            vec = uv - uv1
            if vec.length < Epsilon:
                uvFaceVerts[f.index].append((vtn1,uv))                
                return vtn
    uvFaceVerts[f.index].append((vtn,uv))
    texVerts[vtn] = uv
    return vtn+1

#
#   storeData(pob, bob, data):
#   restoreData(context):    
#

def storeData(pob, bob, data):
    fname = os.path.realpath(os.path.expanduser("~/mh_makeclo_stored.txt"))
    fp = open(fname, "w")
    fp.write("%s\n" % pob.name)
    fp.write("%s\n" % bob.name)
    for (pv, exact, verts, wts, diff) in data:
        #print(pv,exact)
        fp.write("%d %d\n" % (pv.index, exact))
        #print(verts)
        fp.write("%s\n" % verts)
        if not exact:
            #print(wts)
            fp.write("(%s,%s,%s)\n" % wts)
            #print(diff)
            fp.write("(%s,%s,%s)\n" % (diff[0],diff[1],diff[2]))
    fp.close()
    return
    
def restoreData(context): 
    (bob, pob) = getObjectPair(context)
    fname = os.path.realpath(os.path.expanduser("~/mh_makeclo_stored.txt"))
    fp = open(fname, "rU")
    status = 0
    data = []
    for line in fp:
        #print(line)
        words = line.split()
        if status == 0:
            pname = words[0]
            if pname != pob.name:
                raise NameError(
                "Restore error: stored data for %s does not match selected object %s\n" % (pname, pob.name) +
                "Make clothes for %s first\n" % pob.name)
            status = 10
        elif status == 10:
            bname = words[0]
            if bname != bob.name:
                raise NameError(
                "Restore error: stored human %s does not match selected human %s\n" % (bname, bob.name) +
                "Make clothes for %s first\n" % pob.name)
            status = 1
        elif status == 1:
            pv = pob.data.vertices[int(words[0])]
            exact = int(words[1])
            status = 2
        elif status == 2:
            verts = eval(line)
            if exact:
                data.append((pv, exact, verts, 0, 0))
                status = 1
            else:
                status = 3
        elif status == 3:
            wts = eval(line)
            status = 4
        elif status == 4:
            diff = mathutils.Vector( eval(line) )
            data.append((pv, exact, verts, wts, diff))
            status = 1
    bob = context.scene.objects[bname]
    return (bob, data)

#
#   unwrapObject(ob, context):
#

def unwrapObject(ob, context):
    scn = context.scene
    old = scn.objects.active
    scn.objects.active = ob
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', fill_holes=True, correct_aspect=True)
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    scn.objects.active = old
    return

#
#   projectUVs(bob, pob, context):
#   setUvLoc(pv, puv, table):
#   getUvLoc(v, f, uvface):
#

def projectUVs(bob, pob, context):
    (bob1, data) = restoreData(context)
    print("Projecting %s => %s" % (bob.name, pob.name))

    (bVertEdges, bVertFaces, bEdgeFaces, bFaceEdges, bFaceNeighbors, bUvFaceVerts, bTexVerts, bNTexVerts) = setupTexVerts(bob)
    table = {}
    bUvTex = bob.data.uv_textures[0].data
    for (pv, exact, verts, wts, diff) in data:
        if exact:
            print("Exact", pv.index)
            vn0 = verts[0]
            for f0 in bVertFaces[vn0]:
                uv0 = getUvLoc(v0, f0.vertices, bUvTex[f.index])
                table[pv.index] = (1, uv0, 1)
                print(pv.index, table[pv.index])
                break
        else:
            vn0 = verts[0]
            vn1 = verts[1]
            vn2 = verts[2]
            if (vn1 == 0) and (vn2 == 1) and (abs(wts[0]-1) < Epsilon):
                uvVerts = []
                for f0 in bVertFaces[vn0]:
                    uv0 = getUvLoc(vn0, f0.vertices, bUvTex[f0.index])
                    uvVerts.append(uv0)
                table[pv.index] = (2, uvVerts, wts)
                continue
            for f0 in bVertFaces[vn0]:
                for f1 in bVertFaces[vn1]:
                    if (f1 == f0):
                        for f2 in bVertFaces[vn2]:
                            if (f2 == f0):
                                uv0 = getUvLoc(vn0, f0.vertices, bUvTex[f0.index])
                                uv1 = getUvLoc(vn1, f0.vertices, bUvTex[f0.index])
                                uv2 = getUvLoc(vn2, f0.vertices, bUvTex[f0.index])
                                table[pv.index] = (0, [uv0,uv1,uv2], wts)
        
    (pVertEdges, pVertFaces, pEdgeFaces, pFaceEdges, pFaceNeighbors, pUvFaceVerts, pTexVerts, pNTexVerts) = setupTexVerts(pob)
    (pSeamEdgeFaces, pSeamVertEdges, pBoundaryVertEdges, pVertTexVerts) = getSeamData(pob.data, pUvFaceVerts, pEdgeFaces)
    pTexVertUv = {}
    for vtn in range(pNTexVerts):
        pTexVertUv[vtn] = None

    pUvtex = pob.data.uv_textures[0]
    pverts = pob.data.vertices
    bverts = bob.data.vertices
    bedges = bob.data.edges
    remains = {}
    zero = (0,0)
    for pf in pob.data.faces:
        fn = pf.index
        rmd = {}
        rmd[0] = None
        rmd[1] = None
        rmd[2] = None
        rmd[3] = None
        remains[fn] = rmd
        
        pvn0 = pf.vertices[0]
        pvn1 = pf.vertices[1]
        pvn2 = pf.vertices[2]    
        uv0 = getSingleUvLoc(pvn0, table)
        uv1 = getSingleUvLoc(pvn1, table)
        uv2 = getSingleUvLoc(pvn2, table)
        if len(pf.vertices) > 3:
            pvn3 = pf.vertices[3]
            uv3 = getSingleUvLoc(pvn3, table)
        else:
            uv3 = zero
            
        uvf = pUvtex.data[fn]

        uv0 = trySetUv(pvn0, fn, uvf, rmd, 0, uv0, pVertTexVerts, pTexVertUv, pSeamVertEdges)
        if uv0: 
            uvf.uv1 = uv0
            
        uv1 = trySetUv(pvn1, fn, uvf, rmd, 1, uv1, pVertTexVerts, pTexVertUv, pSeamVertEdges)
        if uv1: 
            uvf.uv2 = uv1

        uv2 = trySetUv(pvn2, fn, uvf, rmd, 2, uv2, pVertTexVerts, pTexVertUv, pSeamVertEdges)
        if uv2:
            uvf.uv3 = uv2

        if len(pf.vertices) > 3:
            uv3 = trySetUv(pvn3, fn, uvf, rmd, 3, uv3, pVertTexVerts, pTexVertUv, pSeamVertEdges)
            if uv3:
                uvf.uv4 = uv3

    #(bSeamEdgeFaces, bSeamVertEdges, bBoundaryVertEdges) = getSeamData(bob.data, bUvFaceVerts, bEdgeFaces)
    (bVertList, bPairList, bEdgeList) = getSeams(bob, context.scene)  
    for (en,fcs) in pSeamEdgeFaces.items():
        pe = pob.data.edges[en]
        for m in range(2):
            pv = pverts[pe.vertices[m]]
            be = findClosestEdge(pv, bEdgeList, bverts, bedges)
            for pf in fcs:
                fn = pf.index
                for (n, rmd) in remains[fn].items():
                    if rmd:
                        (uvf, pvn, vt, uv0) = rmd
                        if pv.index == pvn:
                            if pTexVertUv[vt]:
                                uv = pTexVertUv[vt]
                            else:
                                uv = getSeamVertFaceUv(pv, pe, pf, pVertTexVerts, pTexVertUv, be, bEdgeFaces, bUvTex, pverts, bverts)
                                pTexVertUv[vt] = uv
                            setUvVert(uvf, n, uv)
                            remains[fn][n] = None
                            #pverts[pvn].select = True
    
    for pf in pob.data.faces:
        rmd = remains[pf.index]
        for n in range(4):
            if rmd[n]:
                (uvf, pvn, vt, uv) = rmd[n]
                pverts[pvn].select = True
                if pTexVertUv[vt]:
                    uv = pTexVertUv[vt]
                else:
                    pTexVertUv[vt] = uv
                setUvVert(uvf, n, uv)
    
    print("Projection %s => %s done" % (bob.name, pob.name))
    return
 
#
#   trySetUv(pv, fn, uvf, rmd, n, uv, vertTexVerts, texVertUv, seamVertEdges):        
#

def trySetUv(pvn, fn, uvf, rmd, n, uv, vertTexVerts, texVertUv, seamVertEdges):        
    (vt, uv_old) = vertTexVerts[pvn][fn]
    if texVertUv[vt]:
        return texVertUv[vt]
    elif not seamVertEdges[pvn]:
        texVertUv[vt] = uv
        return uv
    else:
        rmd[n] = (uvf, pvn, vt, uv)
        return None

#
#   findClosestEdge(pv, edgeList, verts, edges):
#

def findClosestEdge(pv, edgeList, verts, edges):
    mindist = 1e6
    for e in edgeList:
        vec0 = pv.co - verts[e.vertices[0]].co
        vec1 = pv.co - verts[e.vertices[1]].co
        dist = vec0.length + vec1.length
        if dist < mindist:
            mindist = dist
            best = e
    return best
        

#
#   getSeamVertFaceUv(pv, pe, pf, pVertTexVerts, pTexVertUv, be, bEdgeFaces, bUvTex, pverts, bverts):       
#

def getSeamVertFaceUv(pv, pe, pf, pVertTexVerts, pTexVertUv, be, bEdgeFaces, bUvTex, pverts, bverts):
    dist = {}
    for bf in bEdgeFaces[be.index]:
        dist[bf.index] = 0
    for pvn in pf.vertices:
        (vt, uv_old) = pVertTexVerts[pvn][pf.index]
        puv = pTexVertUv[vt]
        if puv:
            for bf in bEdgeFaces[be.index]:
                for n,bvn in enumerate(bf.vertices):
                    buvf = bUvTex[bf.index]
                    buv = getUvVert(buvf, n)
                    duv = buv - puv
                    dist[bf.index] += duv.length

    mindist = 1e6
    for bf in bEdgeFaces[be.index]:
        if dist[bf.index] < mindist:
            mindist = dist[bf.index]
            best = bf
            
    bv0 = bverts[be.vertices[0]]
    bv1 = bverts[be.vertices[1]]
    m0 = getFaceIndex(bv0.index, best)
    m1 = getFaceIndex(bv1.index, best)
    buvf = bUvTex[best.index]
    buv0 = getUvVert(buvf, m0)
    buv1 = getUvVert(buvf, m1)
    vec0 = pv.co - bv0.co
    vec1 = pv.co - bv1.co
    vec = bv0.co - bv1.co
    dist0 = abs(vec.dot(vec0))
    dist1 = abs(vec.dot(vec1))
    eps = dist1/(dist0+dist1)    
    uv = eps*buv0 + (1-eps)*buv1
    return uv
    
    best.select = True
    pf.select = True
    bv0.select = True
    bv1.select = True
    pv.select = True
    print(uv)
    print("  ", buv0)
    print("  ", buv1)
    foo
    
    return uv
    
def getFaceIndex(vn, f):
    n = 0
    for vn1 in f.vertices:
        if vn1 == vn:
            #print(v.index, n, list(f.vertices))            
            return n
        n += 1
    raise NameError("Vert %d not in face %d %s" % (vn, f.index, list(f.vertices)))

#
#   setUvVert(uvf, n, uv):                
#   getUvVert(uvf, n):   
#

def setUvVert(uvf, n, uv):                
    if n == 0:
        uvf.uv1 = uv
    elif n == 1:
        uvf.uv2 = uv
    elif n == 2:
        uvf.uv3 = uv
    elif n == 3:
        uvf.uv4 = uv        
    return
    
def getUvVert(uvf, n):   
    if n == 0:
        return uvf.uv1
    elif n == 1:
        return uvf.uv2
    elif n == 2:
        return uvf.uv3
    elif n == 3:
        return uvf.uv4
    return
    
#
#   getSeamData(me, uvFaceVerts, edgeFaces):    
#

def getSeamData(me, uvFaceVerts, edgeFaces):    
    seamEdgeFaces = {}
    seamVertEdges = {}
    boundaryEdges = {}
    vertTexVerts = {}
    verts = me.vertices

    for v in me.vertices:
        vn = v.index
        seamVertEdges[vn] = []
        vertTexVerts[vn] = {}
        v.select = False

    for f in me.faces:
        fn = f.index
        for vn in f.vertices:
            n = getFaceIndex(vn, f)
            uvf = uvFaceVerts[fn]
            vertTexVerts[vn][fn]= uvf[n]

    for e in me.edges:
        en = e.index
        fcs = edgeFaces[en]
        if len(fcs) < 2:
            boundaryEdges[en] = True
            e.select = False
        else:
            vn0 = e.vertices[0]
            vn1 = e.vertices[1]
            if isSeam(vn0, vn1, fcs[0], fcs[1], vertTexVerts):
                #e.select = True
                seamEdgeFaces[en] = fcs
                seamVertEdges[vn0].append(e)
                seamVertEdges[vn1].append(e)
            else:
                e.select = False
    return (seamEdgeFaces, seamVertEdges, boundaryEdges, vertTexVerts)            

def isSeam(vn0, vn1, f0, f1, vertTexVerts):
    (vt00, uv00) = vertTexVerts[vn0][f0.index]
    (vt01, uv01) = vertTexVerts[vn1][f0.index]
    (vt10, uv10) = vertTexVerts[vn0][f1.index]
    (vt11, uv11) = vertTexVerts[vn1][f1.index]
    d00 = uv00-uv10
    d11 = uv01-uv11
    d01 = uv00-uv11
    d10 = uv01-uv10
    #test1 = ((vt00 == vt10) and (vt01 == vt11))
    #test2 = ((vt00 == vt11) and (vt01 == vt10))
    test1 = ((d00.length < Epsilon) and (d11.length < Epsilon))
    test2 = ((d01.length < Epsilon) and (d10.length < Epsilon))
    if (test1 or test2):
        return False
    else:
        return True
        print("%d %s" % (vt00, uv00))
        print("%d %s" % (vt01, uv01))
        print("%d %s" % (vt10, uv10))
        print("%d %s" % (vt11, uv11))

#
#
#

def createFaceTable(verts, faces):
    table = {}
    for v in verts:
        table[v.index] = []
    for f in faces:
        for v in f.vertices:
            table[v].append(f)
    return table            

def getSingleUvLoc(vn, table):
    (exact, buvs, wts) = table[vn]
    if exact == 1:
        return buvs
    elif exact == 2:
        return buvs[0]
    else:
        return buvs[0]*wts[0] + buvs[1]*wts[1] + buvs[2]*wts[2] 
 
def getUvLoc(v, f, uvface):
    if v == f[0]:
        return uvface.uv1
    if v == f[1]:
        return uvface.uv2
    if v == f[2]:
        return uvface.uv3
    if v == f[3]:
        return uvface.uv4
    raise NameError("Vertex %d not in face %d??" % (v,f))


#
#   recoverSeams(context):
#

def recoverSeams(context):
    ob = getHuman(context)
    scn = context.scene
    (vertList, pairList, edgeList) = getSeams(ob, scn)
    vcoList = coordList(vertList, ob.data.vertices)
    sme = bpy.data.meshes.new("Seams")
    sme.from_pydata(vcoList, pairList, [])
    sme.update(calc_edges=True)
    sob = bpy.data.objects.new("Seams", sme)
    sob.show_x_ray = True
    scn.objects.link(sob)            
    print("Seams recovered for object %s\n" % ob.name)
    return    
            
def coordList(vertList, verts):
    coords = []
    for vn in vertList:
        coords.append(verts[vn].co)
    return coords        
    
def getSeams(ob, scn):
    verts = ob.data.vertices
    uvtex = ob.data.uv_textures[0]
    faceTable = createFaceTable(ob.data.vertices, ob.data.faces)
    onEdges = {}
    for v in verts:
        onEdges[v.index] = False
    for v in ob.data.vertices:
        if isOnEdge(v, faceTable, uvtex):
            onEdges[v.index] = True

    vertList = []
    edgeList = []
    pairList = []
    n = 0
    for e in ob.data.edges:
        v0 = e.vertices[0]
        v1 = e.vertices[1]
        e.use_seam = (onEdges[v0] and onEdges[v1])
        if e.use_seam:
            vertList += [v0, v1]
            pairList.append((n,n+1))            
            n += 2
            edgeList.append(e)
    return (vertList, pairList, edgeList)            
        
def isOnEdge(v, faceTable, uvtex):            
    uvloc = None
    for f in faceTable[v.index]:
        uvface = uvtex.data[f.index]
        for n,vn in enumerate(f.vertices):
            if vn == v.index:
                if n == 0:
                    uvnloc = uvface.uv1
                elif n == 1:
                    uvnloc = uvface.uv2
                elif n == 2:
                    uvnloc = uvface.uv3
                elif n == 3:
                    uvnloc = uvface.uv4
                if uvloc:
                    dist = uvnloc - uvloc
                    if dist.length > 0.01:
                        return True
                else:
                    uvloc = uvnloc
    return False                            

#
#    makeClothes(context):
#

def makeClothes(context):
    (bob, pob) = getObjectPair(context)
    scn = context.scene
    checkObjectOK(bob, context)
    checkAndVertexDiamonds(bob)
    checkObjectOK(pob, context)
    checkSingleVGroups(pob)
    (outpath, outfile) = getFileName(pob, context, "mhclo")
    print("Creating clothes file %s" % outfile)
    if scn['MakeClothesLogging']:
        logfile = '%s/clothes.log' % scn['MakeClothesDirectory']
        log = open(logfile, "w")
    else:
        log = None
    data = findClothes(context, bob, pob, log)
    storeData(pob, bob, data)
    printClothes(context, outpath, outfile, bob, pob, data)
    if log:
        log.close()
    if scn["MakeClothesSelfClothed"]:
        scn.objects.unlink(bob)
        scn.objects.unlink(pob)
    print("%s done" % outfile)
    return
    
#
#   checkObjectOK(ob, context):
#

def checkObjectOK(ob, context):
    old = context.object
    context.scene.objects.active = ob
    word = None
    error = False
    if ob.location.length > Epsilon:
        word = "object translation"
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    eu = ob.rotation_euler
    if abs(eu.x) + abs(eu.y) + abs(eu.z) > Epsilon:
        word = "object rotation"
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    vec = ob.scale - mathutils.Vector((1,1,1))
    if vec.length > Epsilon:
        word = "object scaling"
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if ob.constraints:
        word = "constraints"
        error = True
    for mod in ob.modifiers:
        if (mod.type in ['CHILD_OF', 'ARMATURE']) and mod.show_viewport:
            word = "an enabled %s modifier" % mod.type
            mod.show_viewport = False
    if ob.parent:
        word = "parent"
        ob.parent = None
    if word:
        msg = "Object %s can not be used for clothes creation because it has %s.\n" % (ob.name, word)
        if error:
            msg +=  "Apply or delete before continuing.\n"
            print(msg)
            raise NameError(msg)
        else:
            print(msg)
            print("Fixed automatically")
    context.scene.objects.active = old
    return    

#
#   checkSingleVGroups(pob):
#

def checkSingleVGroups(pob):
    for v in pob.data.vertices:
        n = 0
        for g in v.groups:
            #print("Key", g.group, g.weight)
            n += 1
        if n != 1:
            v.select = True
            raise NameError("Vertex %d in %s belongs to %d groups. Must be exactly one" % (v.index, pob.name, n))
    return            
        
#
#   offsetCloth(context):
#

def offsetCloth(context):
    (bob, pob) = getObjectPair(context)
    bverts = bob.data.vertices
    pverts = pob.data.vertices    
    print("Offset %s to %s" % (bob.name, pob.name))

    inpath = '%s/%s.mhclo' % (context.scene['MakeClothesDirectory'], bob.name.lower())
    infile = os.path.realpath(os.path.expanduser(inpath))
    outpath = '%s/%s.mhclo' % (context.scene['MakeClothesDirectory'], pob.name.lower())
    outfile = os.path.realpath(os.path.expanduser(outpath))
    print("Modifying clothes file %s => %s" % (infile, outfile))
    infp = open(infile, "r")
    outfp = open(outfile, "w")

    status = 0
    alwaysOutside = context.scene['MakeClothesOutside']
    minOffset = context.scene['MakeClothesMinOffset']

    for line in infp:
        words = line.split()
        if len(words) < 1:
            outfp.write(line)
        elif words[0] == "#":    
            if len(words) < 2:
                status = 0
                outfp.write(line)
            elif words[1] == "verts":
                status = 1
                outfp.write(line)
            elif words[1] == "obj_data":
                if context.scene['MakeClothesVertexGroups']:
                    infp.close()
                    writeFaces(pob, outfp) 
                    writeVertexGroups(pob, outfp)
                    outfp.close()
                    print("Clothes file modified %s => %s" % (infile, outfile))
                    return
                outfp.write(line)
                status = 0
            elif words[1] == "name":
                outfp.write("# name %s\n" % pob.name)
            else:
                outfp.write(line)
            vn = 0
        elif status == 1:
            # 4715  5698  5726 0.00000 1.00000 -0.00000 0.00921
            verts = [int(words[0]), int(words[1]), int(words[2])]
            wts = [float(words[3]), float(words[4]), float(words[5])]
            bv = bverts[vn]
            pv = pverts[vn]
            diff = pv.co - bv.co
            proj = diff.dot(bv.normal)
            print(diff, proj)
            if alwaysOutside and proj < minOffset:
                proj = minOffset
            outfp.write("%5d %5d %5d %.5f %.5f %.5f %.5f\n" % (
                verts[0], verts[1], verts[2], wts[0], wts[1], wts[2], proj))
            # print(vn, bv.co, pv.co)
            vn += 1
        else:
            outfp.write(line)

    infp.close()
    outfp.close()
    print("Clothes file modified %s => %s" % (infile, outfile))
    return

def writeFaces(pob, fp):
    fp.write("# faces\n")
    for f in pob.data.faces:
        for v in f.vertices:
            fp.write(" %d" % (v+1))
        fp.write("\n")
    return

def writeVertexGroups(pob, fp):
    for vg in pob.vertex_groups:
        fp.write("# weights %s\n" % vg.name)
        for v in pob.data.vertices:
            for g in v.groups:
                if g.group == vg.index and g.weight > 1e-4:
                    fp.write(" %d %.4g \n" % (v.index, g.weight))
    return

###################################################################################    
#
#   Export of clothes material
#
###################################################################################    

def exportBlenderMaterial(me, path):
    mats = []
    texs = []
    for mat in me.materials:
        if mat:
            mats.append(mat)
            for mtex in mat.texture_slots:
                if mtex:
                    tex = mtex.texture
                    if tex and (tex not in texs):
                        texs.append(tex)
    
    matname = goodName(mats[0].name)
    mhxfile = "%s_material.mhx" % matname
    mhxpath = os.path.join(path, mhxfile)
    print("Open %s" % mhxpath)
    fp = open(mhxpath, "w")
    for tex in texs:
        exportTexture(tex, matname, fp)
    for mat in mats:
        exportMaterial(mat, fp)
    fp.close()
    return "%s" % mhxfile

#
#    exportMaterial(mat, fp):
#    exportMTex(index, mtex, use, fp):
#    exportTexture(tex, fp):
#    exportImage(img, fp)
#

def exportMaterial(mat, fp):
    fp.write("Material %s \n" % mat.name)
    for (n,mtex) in enumerate(mat.texture_slots):
        if mtex:
            exportMTex(n, mtex, mat.use_textures[n], fp)
    prio = ['diffuse_color', 'diffuse_shader', 'diffuse_intensity', 
        'specular_color', 'specular_shader', 'specular_intensity']
    writePrio(mat, prio, "  ", fp)
    exportRamp(mat.diffuse_ramp, 'diffuse_ramp', fp)
    exportRamp(mat.specular_ramp, 'specular_ramp', fp)
    exclude = []
    exportDefault("Halo", mat.halo, [], [], exclude, [], '  ', fp)
    exclude = []
    exportDefault("RaytraceTransparency", mat.raytrace_transparency, [], [], exclude, [], '  ', fp)
    exclude = []
    exportDefault("SSS", mat.subsurface_scattering, [], [], exclude, [], '  ', fp)
    exclude = ['use_surface_diffuse']
    exportDefault("Strand", mat.strand, [], [], exclude, [], '  ', fp)
    writeDir(mat, prio+['texture_slots', 'volume', 'node_tree',
        'diffuse_ramp', 'specular_ramp', 'use_diffuse_ramp', 'use_specular_ramp', 
        'halo', 'raytrace_transparency', 'subsurface_scattering', 'strand'], "  ", fp)
    fp.write("end Material\n\n")
    return

MapToTypes = {
    'use_map_alpha' : 'ALPHA',
    'use_map_ambient' : 'AMBIENT',
    'use_map_color_diffuse' : 'COLOR',
    'use_map_color_emission' : 'COLOR_EMISSION',
    'use_map_color_reflection' : 'COLOR_REFLECTION',
    'use_map_color_spec' : 'COLOR_SPEC',
    'use_map_color_transmission' : 'COLOR_TRANSMISSION',
    'use_map_density' : 'DENSITY',
    'use_map_diffuse' : 'DIFFUSE',
    'use_map_displacement' : 'DISPLACEMENT',
    'use_map_emission' : 'EMISSION',
    'use_map_emit' : 'EMIT', 
    'use_map_hardness' : 'HARDNESS',
    'use_map_mirror' : 'MIRROR',
    'use_map_normal' : 'NORMAL',
    'use_map_raymir' : 'RAYMIR',
    'use_map_reflect' : 'REFLECTION',
    'use_map_scatter' : 'SCATTERING',
    'use_map_specular' : 'SPECULAR_COLOR', 
    'use_map_translucency' : 'TRANSLUCENCY',
    'use_map_warp' : 'WARP',
}

def exportMTex(index, mtex, use, fp):
    tex = mtex.texture
    texname = tex.name.replace(' ','_')
    mapto = None
    prio = []
    for ext in MapToTypes.keys():
        if eval("mtex.%s" % ext):
            if mapto == None:
                mapto = MapToTypes[ext]
            prio.append(ext)    
    fp.write("  MTex %d %s %s %s\n" % (index, texname, mtex.texture_coords, mapto))
    writePrio(mtex, ['texture']+prio, "    ", fp)
    writeDir(mtex, list(MapToTypes.keys()) + ['texture', 'type', 'texture_coords', 'offset'], "    ", fp)
    fp.write("  end MTex\n\n")
    return

def exportTexture(tex, matname, fp):
    if not tex:
        return
    if tex.type == 'IMAGE' and tex.image:
        exportImage(tex.image, matname, fp)
        fp.write("Texture %s %s\n" % (tex.name, tex.type))
        fp.write("  Image %s ;\n" % tex.image.name)
    else:
        fp.write("Texture %s %s\n" % (tex.name, tex.type))

    exportRamp(tex.color_ramp, "color_ramp", fp)
    writeDir(tex, ['color_ramp', 'node_tree', 'image_user', 'use_nodes', 'use_textures', 'type', 'users_material'], "  ", fp)
    fp.write("end Texture\n\n")

def exportImage(img, matname, fp):
    imgName = img.name
    if imgName == 'Render_Result':
        return
    fp.write("Image %s\n" % imgName)
    fp.write("  Filename %s ;\n" % os.path.basename(img.filepath))
    writeDir(img, ['bindcode', 'filename','filepath', 'filepath_raw', 'is_dirty'], "  ", fp)
    fp.write("end Image\n\n")

def exportRamp(ramp, name, fp):
    if ramp == None:
        return
    print(ramp)
    fp.write("  Ramp %s\n" % name)

    for elt in ramp.elements:
        col = elt.color
        fp.write("    Element (%.3f,%.3f,%.3f,%.3f) %.3f ;\n" % (col[0], col[1], col[2], col[3], elt.position))
    writeDir(ramp, ['elements'], "    ", fp)
    fp.write("  end Ramp\n")


#
#    writePrio(data, prio, pad, fp):
#    writeDir(data, exclude, pad, fp):
#

def writePrio(data, prio, pad, fp):
    for ext in prio:
        writeExt(ext, "data", [], pad, 0, fp, globals(), locals())

def writeDir(data, exclude, pad, fp):
    for ext in dir(data):
        writeExt(ext, "data", exclude, pad, 0, fp, globals(), locals())

def writeQuoted(arg, fp):
    typ = type(arg)
    if typ == int or typ == float or typ == bool:
        fp.write("%s" % arg)
    elif typ == str:
        fp.write("'%s'"% stringQuote(arg))
    elif len(arg) > 1:
        c = '['
        for elt in arg:
            fp.write(c)
            writeQuoted(elt, fp)
            c = ','
        fp.write("]")
    else:
        raise NameError("Unknown property %s %s" % (arg, typ))
        fp.write('%s' % arg)

def stringQuote(string):
    s = ""
    for c in string:
        if c == '\\':
            s += "\\\\"
        elif c == '\"':
            s += "\\\""
        elif c == '\'':
            s += "\\\'"
        else:
            s += c
    return s
        
            
#
#    writeExt(ext, name, exclude, pad, depth, fp, globals, locals):        
#

def writeExt(ext, name, exclude, pad, depth, fp, globals, locals):        
    expr = name+"."+ext
    try:
        arg = eval(expr, globals, locals)
        success = True
    except:
        success = False
        arg = None
    if success:
        writeValue(ext, arg, exclude, pad, depth, fp)
    return

#
#    writeValue(ext, arg, exclude, pad, depth, fp):
#

excludeList = [
    'bl_rna', 'fake_user', 'id_data', 'rna_type', 'name', 'tag', 'users', 'type'
]

def writeValue(ext, arg, exclude, pad, depth, fp):
    if (len(str(arg)) == 0 or
        arg == None or
        arg == [] or
        ext[0] == '_' or
        ext in excludeList or
        ext in exclude):
        return
        
    if ext == 'end':
        print("RENAME end", arg)
        ext = '\\ end'

    typ = type(arg)
    if typ == int:
        fp.write("%s%s %d ;\n" % (pad, ext, arg))
    elif typ == float:
        fp.write("%s%s %.3f ;\n" % (pad, ext, arg))
    elif typ == bool:
        fp.write("%s%s %s ;\n" % (pad, ext, arg))
    elif typ == str:
        fp.write("%s%s '%s' ;\n" % (pad, ext, stringQuote(arg.replace(' ','_'))))
    elif typ == list:
        fp.write("%s%s List\n" % (pad, ext))
        n = 0
        for elt in arg:
            writeValue("[%d]" % n, elt, [], pad+"  ", depth+1, fp)
            n += 1
        fp.write("%send List\n" % pad)
    elif typ == mathutils.Vector:
        c = '('
        fp.write("%s%s " % (pad, ext))
        for elt in arg:
            fp.write("%s%.3f" % (c,elt))
            c = ','
        fp.write(") ;\n")
    else:
        try:
            r = arg[0]
            g = arg[1]
            b = arg[2]
        except:
            return
        if (type(r) == float) and (type(g) == float) and (type(b) == float):
            fp.write("%s%s (%.4f,%.4f,%.4f) ;\n" % (pad, ext, r, g, b))
            print(ext, arg)
    return 

#
#    exportDefault(typ, data, header, prio, exclude, arrays, pad, fp):
#

def exportDefault(typ, data, header, prio, exclude, arrays, pad, fp):
    if not data:
        return
    try:
        if not data.enabled:
            return
    except:
        pass
    try:
        name = data.name
    except:
        name = ''

    fp.write("%s%s %s" % (pad, typ, name))
    for val in header:
        fp.write(" %s" % val)
    fp.write("\n")
    writePrio(data, prio, pad+"  ", fp)

    for (arrname, arr) in arrays:
        #fp.write(%s%s\n" % (pad, arrname))
        for elt in arr:
            exportDefault(arrname, elt, [], [], [], [], pad+'  ', fp)

    writeDir(data, prio+exclude+arrays, pad+"  ", fp)
    fp.write("%send %s\n" % (pad,typ))
    return

###################################################################################    
#
#   Boundary parts
#
###################################################################################    

BodyPartVerts = [
    ((4302, 8697), (8208, 8220), (8223, 6827)), # Head
    ((3464, 10305), (6930, 7245), (14022, 14040)), # Torso
    ((14058, 14158), (4550, 4555), (4543, 4544)), # Arm
    ((14058, 15248), (3214, 3264), (4629, 5836)), # Hand
    ((3936, 3972), (3840, 3957), (14165, 14175)), # Leg
    ((4909, 4943), (5728, 12226), (4684, 5732)), # Foot
    ]

def setBoundaryVerts(scn):
    (x, y, z) = BodyPartVerts[scn['MakeClothesBodyPart']]
    setAxisVerts(scn, 'MakeClothesX1', 'MakeClothesX2', x)
    setAxisVerts(scn, 'MakeClothesY1', 'MakeClothesY2', y)
    setAxisVerts(scn, 'MakeClothesZ1', 'MakeClothesZ2', z)
    
def setAxisVerts(scn, prop1, prop2, x):
    (x1, x2) = x
    scn[prop1] = x1
    scn[prop2] = x2
    
def selectBoundary(ob, scn):
    verts = ob.data.vertices
    bpy.ops.object.mode_set(mode='OBJECT')
    for v in verts:
        v.select = False
    for xyz in ['X','Y','Z']:
        for n in [1,2]:
            n = scn['MakeClothes%s%d' % (xyz, n)]
            print(n)
            verts[n].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    return                    

###################################################################################    
#
#   Z depth
#
###################################################################################    

#
#   getZDepthItems():
#   setZDepth(scn):    
#    class OBJECT_OT_SetZDepthButton(bpy.types.Operator):
#

ZDepth = {
    "Body" : 0,
    "Underwear and lingerie" : 20,
    "Socks and stockings" : 30,
    "Shirt and trousers" : 40,
    "Sweater" : 50,
    "Indoor jacket" : 60,
    "Shoes and boots" : 70,
    "Coat" : 80,
    "Backpack" : 100,
    }
    
def setZDepthItems():
    global ZDepthItems
    zlist = sorted(list(ZDepth.items()), key=lambda z: z[1])
    ZDepthItems = []
    for (name, val) in zlist:
        ZDepthItems.append((name,name,name))
    return            

def setZDepth(scn):    
    global ZDepthItems
    (name1, name2, name3) = ZDepthItems[scn["MakeClothesZDepthName"]]
    print(name1)
    scn["MakeClothesZDepth"] = ZDepth[name1]
    return
    
class OBJECT_OT_SetZDepthButton(bpy.types.Operator):
    bl_idname = "mhclo.set_zdepth"
    bl_label = "Set Z depth"

    def execute(self, context):
        setZDepth(context.scene)
        return{'FINISHED'}    
    
###################################################################################    
#
#   Utilities
#
###################################################################################    
#
#    printVertNums(context):
#    class VIEW3D_OT_MhxPrintVnumsButton(bpy.types.Operator):
#
 
def printVertNums(context):
    ob = context.object
    print("Verts in ", ob)
    for v in ob.data.vertices:
        if v.select:
            print(v.index)
    print("End verts")

class VIEW3D_OT_MhxPrintVnumsButton(bpy.types.Operator):
    bl_idname = "mhclo.print_vnums"
    bl_label = "Print vertex numbers"

    def execute(self, context):
        printVertNums(context)
        return{'FINISHED'}    

#
#    removeVertexGroups(context):
#    class VIEW3D_OT_MhxRemoveVertexGroupsButton(bpy.types.Operator):
#

def removeVertexGroups(context):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.vertex_group_remove(all=True)
    return

class VIEW3D_OT_MhxRemoveVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhclo.remove_vertex_groups"
    bl_label = "Remove vertex groups"

    def execute(self, context):
        removeVertexGroups(context)
        print("All vertex groups removed")
        return{'FINISHED'}    

#
#   autoVertexGroups(context):
#   class VIEW3D_OT_MhxAutoVertexGroupsButton(bpy.types.Operator):
#

def autoVertexGroups(context):
    ob = context.object
    ishuman = isHuman(ob)
    mid = ob.vertex_groups.new("Mid")
    left = ob.vertex_groups.new("Left")
    right = ob.vertex_groups.new("Right")
    for v in ob.data.vertices:
        vn = v.index
        if v.co[0] > 0.01:
            left.add([vn], 1.0, 'REPLACE')
        elif v.co[0] < -0.01:
            right.add([vn], 1.0, 'REPLACE')
        else:
            mid.add([vn], 1.0, 'REPLACE')
            if ishuman and (vn < NBodyVerts):
                left.add([vn], 1.0, 'REPLACE')
                right.add([vn], 1.0, 'REPLACE')
    return

class VIEW3D_OT_MhxAutoVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhclo.auto_vertex_groups"
    bl_label = "Auto vertex groups"

    def execute(self, context):
        removeVertexGroups(context)
        autoVertexGroups(context)
        print("Vertex groups auto assigned")
        return{'FINISHED'}    

#
#   checkAndVertexDiamonds(ob):
#

def checkAndVertexDiamonds(ob):
    print("Unvertex diamonds in %s" % ob)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    me = ob.data
    hasDiamonds = False
    for f in me.faces:        
        if len(f.vertices) < 4:
            hasDiamonds = True
            for vn in f.vertices:
                me.vertices[vn].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.vertex_group_remove_from(all=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    if not hasDiamonds:
        raise NameError("Base object %s does not have any joint diamonds" % ob.name)
    return            

###################################################################################    
#    User interface
#
#    initInterface()
#
###################################################################################    

from bpy.props import *

#
#   readDefaultSettings(context):
#   saveDefaultSettings(context):
#

def readDefaultSettings(context):
    fname = os.path.realpath(os.path.expanduser("~/make_clothes.settings"))
    try:
        fp = open(fname, "rU")
    except:
        print("Did not find %s. Using default settings" % fname)
        return
    
    scn = context.scene
    for line in fp:
        words = line.split()
        prop = words[0]
        type = words[1]        
        if type == "int":
            scn[prop] = int(words[2])
        elif type == "float":
            scn[prop] = float(words[2])
        elif type == "str":
            scn[prop] = words[2]
    fp.close()
    return
    
def saveDefaultSettings(context):
    fname = os.path.realpath(os.path.expanduser("~/make_clothes.settings"))
    fp = open(fname, "w")
    scn = context.scene
    for (prop, value) in scn.items():
        if prop[0:11] == "MakeClothes":
            if type(value) == int:
                fp.write("%s int %s\n" % (prop, value))
            elif type(value) == float:
                fp.write("%s float %.4f\n" % (prop, value))
            elif type(value) == str:
                fp.write("%s str %s\n" % (prop, value))
    fp.close()
    return
    
def isInited(scn):
    try:
        scn["MakeClothesDirectory"]
        return True
    except:
        return False
    
###################################################################################    
#    User interface
#
#    initInterface()
#
###################################################################################    

from bpy.props import *

def initInterface(scn):
    global ZDepthItems

    for skey in ShapeKeys:
        expr = (
    'bpy.types.Scene.MakeClothes%s = BoolProperty(\n' % skey +
    '   name="%s", \n' % skey +
    '   description="Shapekey %s affects clothes")' % skey)
        #print(expr)
        exec(expr)
        scn['MakeClothes%s' % skey] = False

    bpy.types.Scene.MakeClothesDirectory = StringProperty(
        name="Directory", 
        description="Directory", 
        maxlen=1024)
    scn['MakeClothesDirectory'] = "~"
    
    bpy.types.Scene.MakeClothesMaterials = BoolProperty(
        name="Materials", 
        description="Use materials")
    scn['MakeClothesMaterials'] = False

    bpy.types.Scene.MakeClothesBlenderMaterials = BoolProperty(
        name="Blender materials", 
        description="Save materials as mhx file")
    scn['MakeClothesBlenderMaterials'] = False

    bpy.types.Scene.MakeClothesHairMaterial = BoolProperty(
        name="Hair material", 
        description="Fill in hair material")
    scn['MakeClothesHairMaterial'] = False

    bpy.types.Scene.MakeClothesVertexGroups = BoolProperty(
        name="Save vertex groups", 
        description="Save vertex groups but not texverts")
    scn['MakeClothesVertexGroups'] = True

    bpy.types.Scene.MakeClothesThreshold = FloatProperty(
        name="Threshold", 
        description="Minimal allowed value of normal-vector dot product",
        min=-1.0, max=0.0)
    scn['MakeClothesThreshold'] = theThreshold

    bpy.types.Scene.MakeClothesListLength = IntProperty(
        name="List length", 
        description="Max number of verts considered")
    scn['MakeClothesListLength'] = theListLength

    """
    bpy.types.Scene.MakeClothesForbidFailures = BoolProperty(
        name="Forbid failures", 
        description="Raise error if not found optimal triangle")
    scn['MakeClothesForbidFailures'] = True
    """
    
    bpy.types.Scene.MakeClothesLogging = BoolProperty(
        name="Log", 
        description="Write a log file for debugging")
    scn['MakeClothesLogging'] = False

    bpy.types.Scene.MakeClothesSelfClothed = BoolProperty(
        name="Self clothed", 
        description="Clothes included in body mesh")
    scn['MakeClothesSelfClothed'] = False

    bpy.types.Scene.MakeClothesX1 = IntProperty(
        name="X1", 
        description="First X vert for clothes rescaling")
    scn['MakeClothesX1'] = 4302

    bpy.types.Scene.MakeClothesX2 = IntProperty(
        name="X2", 
        description="Second X vert for clothes rescaling")
    scn['MakeClothesX2'] = 8697

    bpy.types.Scene.MakeClothesY1 = IntProperty(
        name="Y1", 
        description="First Y vert for clothes rescaling")
    scn['MakeClothesY1'] = 8208

    bpy.types.Scene.MakeClothesY2 = IntProperty(
        name="Y2", 
        description="Second Y vert for clothes rescaling")
    scn['MakeClothesY2'] = 8220

    bpy.types.Scene.MakeClothesZ1 = IntProperty(
        name="Z1", 
        description="First Z vert for clothes rescaling")
    scn['MakeClothesZ1'] = 8289

    bpy.types.Scene.MakeClothesZ2 = IntProperty(
        name="Z2", 
        description="Second Z vert for clothes rescaling")
    
    bpy.types.Scene.MakeClothesExamineBoundary = BoolProperty(
        name="Examine", 
        description="Examine boundary when set")
    scn['MakeClothesExamineBoundary'] = False

    bpy.types.Scene.MakeClothesBodyPart = EnumProperty(
        items = [('Head', 'Head', 'Head'),
                 ('Torso', 'Torso', 'Torso'),
                 ('Arm', 'Arm', 'Arm'),
                 ('Hand', 'Hand', 'Hand'),
                 ('Leg', 'Leg', 'Leg'),
                 ('Foot', 'Foot', 'Foot')]
        )
    scn['MakeClothesBodyPart'] = 0
    setBoundaryVerts(scn)

    setZDepthItems()
    bpy.types.Scene.MakeClothesZDepthName = EnumProperty(
        items = ZDepthItems)
    scn['MakeClothesZDepthName'] = 4

    bpy.types.Scene.MakeClothesZDepth = IntProperty(
        name="Z depth", 
        description="Location in the Z buffer")
    setZDepth(scn)

    return

#
#   readDefaultSettings(context):
#   saveDefaultSettings(context):
#

def readDefaultSettings(context):
    fname = os.path.realpath(os.path.expanduser("~/make_clothes.settings"))
    try:
        fp = open(fname, "rU")
    except:
        print("Did not find %s. Using default settings" % fname)
        return
    
    scn = context.scene
    for line in fp:
        words = line.split()
        prop = words[0]
        type = words[1]        
        if type == "int":
            scn[prop] = int(words[2])
        elif type == "float":
            scn[prop] = float(words[2])
        elif type == "str":
            scn[prop] = words[2]
    fp.close()
    return
    
def saveDefaultSettings(context):
    fname = os.path.realpath(os.path.expanduser("~/make_clothes.settings"))
    fp = open(fname, "w")
    scn = context.scene
    for (prop, value) in scn.items():
        if prop[0:11] == "MakeClothes":
            if type(value) == int:
                fp.write("%s int %s\n" % (prop, value))
            elif type(value) == float:
                fp.write("%s float %.4f\n" % (prop, value))
            elif type(value) == str:
                fp.write("%s str %s\n" % (prop, value))
    fp.close()
    return
    
#
#    class MakeClothesPanel(bpy.types.Panel):
#

class MakeClothesPanel(bpy.types.Panel):
    bl_label = "Make clothes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'MESH')

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label("Initialization")
        layout.operator("mhclo.init_interface")
        if not isInited(scn):
            return
        layout.operator("mhclo.save_settings")
        layout.label("Utilities")
        layout.operator("mhclo.print_vnums")
        layout.operator("mhclo.remove_vertex_groups")
        layout.operator("mhclo.auto_vertex_groups")
        layout.operator("mhclo.copy_vert_locs")
        layout.label("UVs")
        layout.operator("mhclo.recover_seams")
        layout.operator("mhclo.project_uvs")
        layout.label("Make clothes")
        layout.prop(scn, "MakeClothesDirectory")
        layout.prop(scn, "MakeClothesMaterials")
        layout.prop(scn, "MakeClothesBlenderMaterials")
        layout.prop(scn, "MakeClothesHairMaterial")
        layout.prop(scn, "MakeClothesListLength")
        layout.prop(scn, "MakeClothesLogging")
        layout.prop(scn, "MakeClothesSelfClothed")
        layout.operator("mhclo.make_human", text="Make Human").isHuman = True
        layout.operator("mhclo.make_human", text="Make Clothing").isHuman = False
        
        layout.separator()
        layout.operator("mhclo.make_clothes")
        layout.operator("mhclo.export_obj_file")
        layout.operator("mhclo.export_blender_material")
        
        layout.label("Shapekeys")
        for skey in ShapeKeys:
            layout.prop(scn, "MakeClothes%s" % skey)   
        
        layout.label("Z depth")
        layout.prop(scn, "MakeClothesZDepthName")   
        layout.operator("mhclo.set_zdepth")
        layout.prop(scn, "MakeClothesZDepth")   


        layout.label("Boundary")
        layout.prop(scn, "MakeClothesBodyPart")   
        layout.prop(scn, "MakeClothesExamineBoundary")           
        layout.operator("mhclo.set_boundary")        
        layout.prop(scn, "MakeClothesX1")
        layout.prop(scn, "MakeClothesX2")
        layout.prop(scn, "MakeClothesY1")
        layout.prop(scn, "MakeClothesY2")
        layout.prop(scn, "MakeClothesZ1")
        layout.prop(scn, "MakeClothesZ2")   
        return
        layout.separator()
        layout.prop(scn, "MakeClothesVertexGroups")
        layout.operator("mhclo.offset_clothes")
        return

#
#    class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
#

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
    bl_idname = "mhclo.init_interface"
    bl_label = "Reinitialize"

    def execute(self, context):
        initInterface(context.scene)
        readDefaultSettings(context)
        print("Interface initialized")
        return{'FINISHED'}    

#
#    class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
#

class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
    bl_idname = "mhclo.save_settings"
    bl_label = "Save settings"

    def execute(self, context):
        saveDefaultSettings(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_RecoverSeamsButton(bpy.types.Operator):
#

class OBJECT_OT_RecoverSeamsButton(bpy.types.Operator):
    bl_idname = "mhclo.recover_seams"
    bl_label = "Recover seams"

    def execute(self, context):
        recoverSeams(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
#

class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.make_clothes"
    bl_label = "Make clothes"

    def execute(self, context):     
        makeClothes(context)
        return{'FINISHED'}    
        
#
#    class OBJECT_OT_ProjectUVsButton(bpy.types.Operator):
#

class OBJECT_OT_ProjectUVsButton(bpy.types.Operator):
    bl_idname = "mhclo.project_uvs"
    bl_label = "Project UVs"

    def execute(self, context):
        (human, clothing) = getObjectPair(context)
        unwrapObject(clothing, context)
        projectUVs(human, clothing, context)
        return{'FINISHED'}    
        
#
#   class OBJECT_OT_CopyVertLocsButton(bpy.types.Operator):
#

class OBJECT_OT_CopyVertLocsButton(bpy.types.Operator):
    bl_idname = "mhclo.copy_vert_locs"
    bl_label = "Copy vertex locations"

    def execute(self, context):
        src = context.object
        for trg in context.scene.objects:
            if trg != src and trg.select and trg.type == 'MESH':
                print("Copy vertex locations from %s to %s" % (src.name, trg.name))
                for n,sv in enumerate(src.data.vertices):
                    tv = trg.data.vertices[n]
                    tv.co = sv.co
                print("Vertex locations copied")
        return{'FINISHED'}    

        
#
#   class OBJECT_OT_ExportObjFileButton(bpy.types.Operator):
#

class OBJECT_OT_ExportObjFileButton(bpy.types.Operator):
    bl_idname = "mhclo.export_obj_file"
    bl_label = "Export Obj file"

    def execute(self, context):
        exportObjFile(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_ExportBlenderMaterialsButton(bpy.types.Operator):
#

class OBJECT_OT_ExportBlenderMaterialButton(bpy.types.Operator):
    bl_idname = "mhclo.export_blender_material"
    bl_label = "Export Blender material"

    def execute(self, context):
        pob = getClothing(context)
        (outpath, outfile) = getFileName(pob, context, "mhx")
        exportBlenderMaterial(pob.data, outpath)
        return{'FINISHED'}    

#
#    class OBJECT_OT_MakeHumanButton(bpy.types.Operator):
#

class OBJECT_OT_MakeHumanButton(bpy.types.Operator):
    bl_idname = "mhclo.make_human"
    bl_label = "Make human"
    isHuman = BoolProperty()

    def execute(self, context):
        ob = context.object
        ob["MhxMesh"] = self.isHuman
        print("Object %s: Human = %s" % (ob.name, ob["MhxMesh"]))
        return{'FINISHED'}    

#
#    class OBJECT_OT_SetBoundaryButton(bpy.types.Operator):
#

class OBJECT_OT_SetBoundaryButton(bpy.types.Operator):
    bl_idname = "mhclo.set_boundary"
    bl_label = "Set boundary"

    def execute(self, context):
        scn = context.scene
        setBoundaryVerts(scn)
        if scn['MakeClothesExamineBoundary']:
            ob = getHuman(context)
            selectBoundary(ob, scn)
        return{'FINISHED'}    

#
#    class OBJECT_OT_OffsetClothesButton(bpy.types.Operator):
#

class OBJECT_OT_OffsetClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.offset_clothes"
    bl_label = "Offset clothes"

    def execute(self, context):     
        offsetCloth(context)
        return{'FINISHED'}    

#
#    Init and register
#


def register():
    initInterface(bpy.context.scene)
    readDefaultSettings(bpy.context)
    bpy.utils.register_module(__name__)
    pass

def unregister():
    bpy.utils.unregister_module(__name__)
    pass

if __name__ == "__main__":
    register()



