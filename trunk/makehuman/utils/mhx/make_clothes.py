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

Used to be called defineProxy.py, because a proxy is just a full-body
dress. Below the word clothes refers both to proxies, make-deform
cages, and proper clothes.

Import a MH character *with the joint diamonds present*. In the MHX
importer the Diamonds option must be selected; the OBJ file is
probably useless, because I think that the diamonds have been filtered
out.

Model your clothes over the reference character. It does not really
matter which character you use as reference, but the final result will
probably look better on characters which do not deviate too much from
the reference. The clothing may optionally be UV-unwrapped.

Both the clothes and the character must be given vertex groups with
the same names. If the character has been brought into Blender with
the mhx importer, it is a good idea to first delete all bone groups.
Each clothing vertex must belong to a single group (more precisely,
any additional group is ignored), whereas character verts can belong
to several groups. The character mesh, but not the clothes, should
also be triangulated (Ctrl-T in Edit mode) for best results.

The algorithm assigns each clothing vertex to the "best" triangle in
the character mesh. The face number and the verts barycentric
coordinates (a weighted sum of the corner coordinates) are stored in
the mhclo file. The best triangle is charactized by a small distance
between the vert and face, and that the projection onto the
face falls within the face (all weights lie between 0 and 1), or
almost so. The normal distance between the vertex and the face is
also recorded.

Finding the best face for each vertex is sometimes difficult in
regions where separate parts of the character mesh are very close or
overlap. The mouth area is especially tricky, for proxy meshes with
articulate tongue, teeth, and inner mouth wall. For trousers it can be
difficult to distinguish between the groin area and the left and right
inner thighs. You can help the script distinguish between different
body parts by assigning vertex groups. The algorithm only looks for
the best triangle within the given vertex group.

At the very least the mesh should be divided into a Left, Right and
Mid (with x = 0) group. Joint diamonds should not be assigned to any
group at all, to ensure that the clothing does not follow the
diamonds.

Vertex groups can also be used to prune the search tree and speed
up the program. 

-------

Access this script from the UI panel (N-key).

Assign vertex groups to the main character and to all clothes or
proxies. The name of the vertex groups must match exactly.

Select all clothes or proxies that you want to export, then select the
character to make it active.

Press the Make clothes button.

A separate .mhclo file for each piece of clothing will now be created
in the specified directory.

The file proxy.cfg defines which clothes will be exported with the
character. This file is located in the MakeHuman's main program
directory, but MH will first look for this files in the ~/makehuman/
and C:/ folders. In this way you can keep your own private version of
proxy.cfg. The syntax is described in the beginning of the file.

------
Making clothes with offset.

Make a copy of the clothe and shrinkwrap it to the base mesh. 

Make a clothes file for the shrinked copy as above.

Select offset clothes, then shift select the shrinked copy to make it active.

Press Make offset button.

A new .mhclo file is created for the offset clothes in the specified directory.

"""

bl_addon_info = {
    "name": "Make clothes to MakeHuman",
    "author": "Thomas Larsson",
    "version": 0.3,
    "blender": (2, 5, 4),
    "api": 31913,
    "location": "View3D > Properties > Make MH clothes",
    "description": "Make clothes for MakeHuman characters",
    "warning": "",
    "category": "3D View"}


import bpy, os, mathutils

theThreshold = -0.2
theListLength = 3
Epsilon = 1e-4


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

        name = pob.vertex_groups[pindex].name
        bindex = None
        for bvg in bob.vertex_groups:
            if bvg.name == name:
                bindex = bvg.index
        if bindex == None:
            raise NameError("Did not find vertex group %s in base mesh" % name)

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
                print(pv.index, mv.index, mindist, name, pindex, bindex)
            #log.write("%d %d %.5f %s %d %d\n" % (pv.index, mv.index, mindist, name, pindex, bindex))
            #printMverts("  ", mverts)
        else:
            raise NameError("Failed to find vert %d in group %s %d %d" % (pv.index, name, pindex, bindex))
        if mindist > 5:
            raise NameError("Minimal distance %f > 5.0. Check base and proxy scales." % mindist)

        bestVerts.append((pv, exact, mverts, []))

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
    for (pv, exact, mverts, fcs) in bestVerts:
        print(pv.index)
        if exact:
            continue
        for (bv,mdist) in mverts:
            if bv:
                for f in vfaces[bv.index]:
                    r0 = base.vertices[f[0]].co
                    r1 = base.vertices[f[1]].co
                    r2 = base.vertices[f[2]].co
                    wts = cornerWeights(pv, r0, r1, r2, pob)
                    fcs.append((f, wts))

    print("Finding best weights")
    alwaysOutside = scn['MakeClothesOutside']
    minOffset = scn['MakeClothesMinOffset']
    useProjection = scn['MakeClothesUseProjection']
    bestFaces = []
    for (pv, exact, mverts, fcs) in bestVerts:
        #print(pv.index)
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
            if scn['MakeClothesForbidFailures']:
                vn = pv.index
                selectVert(context, vn, pob)
                print("Tried", mverts)
                raise NameError("Did not find optimal triangle for %s vert %d" % (pob.name, pv))
            (mv, mdist) = mverts[0]
            bVerts = [mv.index,0,1]
            bWts = [1,0,0]

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
    for path in ['~/makehuman/', '/']:
        path1 = os.path.expanduser(path+name)
        fileName = os.path.realpath(path1)
        try:
            fp = open(fileName, "r")
            print("Using header file %s" % fileName)
            return fp
        except:
            print("No file %s" % fileName)
    return None

#
#    printClothes(context, path, bob, pob, data):    
#
        
def printClothes(context, path, bob, pob, data):
    file = os.path.expanduser(path)
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

    printScale(fp, bob, scn, 'x_scale', 0, 'MakeClothesX1', 'MakeClothesX2')
    printScale(fp, bob, scn, 'z_scale', 1, 'MakeClothesY1', 'MakeClothesY2')
    printScale(fp, bob, scn, 'y_scale', 2, 'MakeClothesZ1', 'MakeClothesZ2')

    me = pob.data

    if me.materials and scn['MakeClothesMaterials']:
        mat = me.materials[0]
        fp.write("# material %s\n" % mat.name)
        writeColor(fp, 'diffuse_color', mat.diffuse_color)
        fp.write('diffuse_shader %s\n' % mat.diffuse_shader)
        fp.write('diffuse_intensity %.4f\n' % mat.diffuse_intensity)
        writeColor(fp, 'specular_color', mat.specular_color)
        fp.write('specular_shader %s\n' % mat.specular_shader)
        fp.write('specular_intensity %.4f\n' % mat.specular_intensity)

    useProjection = scn['MakeClothesUseProjection']
    fp.write("# use_projection %d\n" % useProjection)
    fp.write("# verts\n")
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

    fp.write("# obj_data\n")
    if me.uv_textures:
        uvtex = me.uv_textures[0]
        #fp.write("# texverts\n")
        fn = 0
        for uvdata in uvtex.data.values():
            uv = uvdata.uv_raw
            f = me.faces[fn]
            for n in range(len(f.vertices)):
                fp.write("vt %.4f %.4f\n" % (uv[2*n], uv[2*n+1]))

    #fp.write("# faces\n")

    if me.uv_textures:
        n = 1
        for f in me.faces:
            fp.write("f ")
            for v in f.vertices:
                fp.write("%d/%d " % (v+1, n))
                n += 1
            fp.write("\n")
    else:
        for f in me.faces:
            fp.write("f ")
            for v in f.vertices:
                fp.write("%d " % (v+1))
            fp.write("\n")

    fp.write('\n')
    fp.close()
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
#    makeClothes(context):
#

def makeClothes(context):
    bob = context.object
    for pob in context.selected_objects:
        if pob.type == 'MESH' and bob.type == 'MESH' and pob != bob:
            outpath = '%s/%s.mhclo' % (context.scene['MakeClothesDirectory'], pob.name.lower())
            outfile = os.path.realpath(os.path.expanduser(outpath))
            print("Creating clothes file %s" % outfile)
            logpath = '%s/clothes.log' % context.scene['MakeClothesDirectory']
            logfile = os.path.realpath(os.path.expanduser(logpath))
            log = open(logfile, "w")
            data = findClothes(context, bob, pob, log)
            log.close()
            printClothes(context, outpath, bob, pob, data)
            print("%s done" % outpath)
        
#
#   offsetClothes(context):
#   offsetCloth(bob, pob, context):
#

def offsetClothes(context):
    bob = context.object
    for pob in context.selected_objects:
        if pob.type == 'MESH' and bob.type == 'MESH' and pob != bob:
            offsetCloth(bob, pob, context)
    return

def offsetCloth(bob, pob, context):
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
#    User interface
#
#    initInterface()
#

from bpy.props import *

def initInterface(scn):
    bpy.types.Scene.MakeClothesDirectory = StringProperty(
        name="Directory", 
        description="Directory", 
        maxlen=1024)
    #scn['MakeClothesDirectory'] = "/home/svn/makehuman/data/hairstyles"
    scn['MakeClothesDirectory'] = "~/documents/makehuman/clothes"
    bpy.types.Scene.MakeClothesMaterials = BoolProperty(
        name="Materials", 
        description="Use materials")
    scn['MakeClothesMaterials'] = False

    bpy.types.Scene.MakeClothesHairMaterial = BoolProperty(
        name="Hair material", 
        description="Fill in hair material")
    scn['MakeClothesHairMaterial'] = False

    bpy.types.Scene.MakeClothesUseProjection = BoolProperty(
        name="Use projection", 
        description="Vert normal to face")
    scn['MakeClothesUseProjection'] = False

    bpy.types.Scene.MakeClothesOutside = BoolProperty(
        name="Always outside", 
        description="Invert projection if negative")
    scn['MakeClothesOutside'] = True

    bpy.types.Scene.MakeClothesMinOffset = FloatProperty(
        name="Min offset", 
        description="Mininum offset from base mesh")
    scn['MakeClothesMinOffset'] = 0.0

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

    bpy.types.Scene.MakeClothesForbidFailures = BoolProperty(
        name="Forbid failures", 
        description="Raise error if not found optimal triangle")
    scn['MakeClothesForbidFailures'] = True

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
    scn['MakeClothesZ2'] = 8223

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
        layout.operator("mhclo.init_interface")
        layout.prop(scn, "MakeClothesDirectory")
        layout.prop(scn, "MakeClothesMaterials")
        layout.prop(scn, "MakeClothesHairMaterial")
        layout.prop(scn, "MakeClothesUseProjection")
        layout.prop(scn, "MakeClothesOutside")
        layout.prop(scn, "MakeClothesMinOffset")
        layout.prop(scn, "MakeClothesThreshold")
        layout.prop(scn, "MakeClothesListLength")
        layout.prop(scn, "MakeClothesForbidFailures")
        layout.operator("mhclo.make_clothes")
        layout.separator()
        layout.label("Scaling verts")
        layout.prop(scn, "MakeClothesX1")
        layout.prop(scn, "MakeClothesX2")
        layout.prop(scn, "MakeClothesY1")
        layout.prop(scn, "MakeClothesY2")
        layout.prop(scn, "MakeClothesZ1")
        layout.prop(scn, "MakeClothesZ2")        
        layout.separator()
        layout.prop(scn, "MakeClothesVertexGroups")
        layout.operator("mhclo.offset_clothes")
        return

#
#    class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
#

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
    bl_idname = "mhclo.init_interface"
    bl_label = "Initialize"

    def execute(self, context):
        import bpy
        initInterface(context.scene)
        print("Interface initialized")
        return{'FINISHED'}    

#
#    class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
#

class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.make_clothes"
    bl_label = "Make clothes"

    def execute(self, context):
        import bpy, mathutils
        makeClothes(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_OffsetClothesButton(bpy.types.Operator):
#

class OBJECT_OT_OffsetClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.offset_clothes"
    bl_label = "Offset clothes"

    def execute(self, context):
        import bpy, mathutils
        offsetClothes(context)
        return{'FINISHED'}    

#
#    Init and register
#

initInterface(bpy.context.scene)

def register():
    bpy.utils.register_module(__name__)
    pass

def unregister():
    bpy.utils.unregister_module(__name__)
    pass

if __name__ == "__main__":
    register()



