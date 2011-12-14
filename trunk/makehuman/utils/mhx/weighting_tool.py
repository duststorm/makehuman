""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
Bone weighting utility

"""
import bpy, os, mathutils
import math
from mathutils import *
from bpy.props import *

#
#    printVertNums(context):
#    class VIEW3D_OT_PrintVnumsButton(bpy.types.Operator):
#
 
def printVertNums(context):
    ob = context.object
    print("Verts in ", ob)
    for v in ob.data.vertices:
        if v.select:
            print(v.index)
    print("End")

class VIEW3D_OT_PrintVnumsButton(bpy.types.Operator):
    bl_idname = "mhw.print_vnums"
    bl_label = "Print vnums"

    def execute(self, context):
        printVertNums(context)
        return{'FINISHED'}    

#
#    selectVertNum8m(context):
#    class VIEW3D_OT_SelectVnumButton(bpy.types.Operator):
#
 
def selectVertNum(context):
    n = context.scene.MhxVertNum
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    for v in ob.data.vertices:
        v.select = False
    v = ob.data.vertices[n]
    v.select = True
    bpy.ops.object.mode_set(mode='EDIT')

class VIEW3D_OT_SelectVnumButton(bpy.types.Operator):
    bl_idname = "mhw.select_vnum"
    bl_label = "Select vnum"

    def execute(self, context):
        selectVertNum(context)
        return{'FINISHED'}    

#
#    printEdgeNums(context):
#    class VIEW3D_OT_PrintEnumsButton(bpy.types.Operator):
#
 
def printEdgeNums(context):
    ob = context.object
    print("Edges in ", ob)
    for e in ob.data.edges:
        if e.select:
            print(e.index)
    print("End")

class VIEW3D_OT_PrintEnumsButton(bpy.types.Operator):
    bl_idname = "mhw.print_enums"
    bl_label = "Print enums"

    def execute(self, context):
        printEdgeNums(context)
        return{'FINISHED'}    
#
#    printFaceNums(context):
#    class VIEW3D_OT_PrintFnumsButton(bpy.types.Operator):
#
 
def printFaceNums(context):
    ob = context.object
    print("Faces in ", ob)
    for f in ob.data.faces:
        if f.select:
            print(f.index)
    print("End")

class VIEW3D_OT_PrintFnumsButton(bpy.types.Operator):
    bl_idname = "mhw.print_fnums"
    bl_label = "Print fnums"

    def execute(self, context):
        printFaceNums(context)
        return{'FINISHED'}    

#
#    selectQuads():
#    class VIEW3D_OT_SelectQuadsButton(bpy.types.Operator):
#

def selectQuads(context):
    ob = context.object
    for f in ob.data.faces:
        if len(f.vertices) == 4:
            f.select = True
        else:
            f.select = False
    return

class VIEW3D_OT_SelectQuadsButton(bpy.types.Operator):
    bl_idname = "mhw.select_quads"
    bl_label = "Select quads"

    def execute(self, context):
        import bpy
        selectQuads(context)
        print("Quads selected")
        return{'FINISHED'}    

#
#    removeVertexGroups(context):
#    class VIEW3D_OT_RemoveVertexGroupsButton(bpy.types.Operator):
#

def removeVertexGroups(context):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.vertex_group_remove(all=True)
    return

class VIEW3D_OT_RemoveVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.remove_vertex_groups"
    bl_label = "Unvertex all"

    def execute(self, context):
        removeVertexGroups(context)
        print("All vertex groups removed")
        return{'FINISHED'}    

#
#
#

def copyVertexGroups(scn, src, trg):
    print("Copy vertex groups %s => %s" % (src.name, trg.name))
    scn.objects.active = trg
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.vertex_group_remove(all=True)
    groups = {}
    for sgrp in src.vertex_groups:
        tgrp = trg.vertex_groups.new(name=sgrp.name)
        groups[sgrp.index] = tgrp
    for vs in src.data.vertices:
        for g in vs.groups:            
            tgrp = groups[g.group]
            tgrp.add([vs.index], g.weight, 'REPLACE')
    return

class VIEW3D_OT_CopyVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.copy_vertex_groups"
    bl_label = "Copy vgroups active => selected"

    def execute(self, context):
        src = context.object
        scn = context.scene
        for ob in scn.objects:
            if ob.type == 'MESH' and ob != src:
                trg = ob
                break
        copyVertexGroups(scn, src, trg)
        print("Vertex groups copied")
        return{'FINISHED'}    

#
#    unVertexDiamonds(context):
#    class VIEW3D_OT_UnvertexDiamondsButton(bpy.types.Operator):
#

def unVertexDiamonds(context):
    ob = context.object
    print("Unvertex diamonds in %s" % ob)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    me = ob.data
    for f in me.faces:        
        if len(f.vertices) < 4:
            for vn in f.vertices:
                me.vertices[vn].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.vertex_group_remove_from(all=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    return

class VIEW3D_OT_UnvertexDiamondsButton(bpy.types.Operator):
    bl_idname = "mhw.unvertex_diamonds"
    bl_label = "Unvertex diamonds"

    def execute(self, context):
        unVertexDiamonds(context)
        print("Diamonds unvertexed")
        return{'FINISHED'}    

class VIEW3D_OT_UnvertexSelectedButton(bpy.types.Operator):
    bl_idname = "mhw.unvertex_selected"
    bl_label = "Unvertex selected"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.vertex_group_remove_from(all=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        print("Selected unvertexed")
        return{'FINISHED'}    

#
#    deleteDiamonds(context)
#    Delete joint diamonds in main mesh
#    class VIEW3D_OT_DeleteDiamondsButton(bpy.types.Operator):
#

def deleteDiamonds(context):
    ob = context.object
    print("Delete diamonds in %s" % bpy.context.object)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    me = ob.data
    for f in me.faces:        
        if len(f.vertices) < 4:
            for vn in f.vertices:
                me.vertices[vn].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    return
    
class VIEW3D_OT_DeleteDiamondsButton(bpy.types.Operator):
    bl_idname = "mhw.delete_diamonds"
    bl_label = "Delete diamonds"

    def execute(self, context):
        deleteDiamonds(context)
        print("Diamonds deleted")
        return{'FINISHED'}    
    

#
#    pairWeight(context):
#

def pairWeight(context):
    ob = context.object
    scn = context.scene
    name1 = scn['MhxBone1']
    name2 = scn['MhxBone2']
    weight = scn['MhxWeight']
    index1 = -1
    index2 = -1
    for vgrp in ob.vertex_groups:
        if vgrp.name == name1:
            index1 = vgrp.index
        if vgrp.name == name2:
            index2 = vgrp.index
    if index1 < 0 or index2 < 0:
        raise NameError("Did not find vertex groups %s or %s" % (name1, name2))
    for v in ob.data.vertices:
        if v.select:
            for grp in v.groups:
                if grp.index == index1:
                    grp.weight = weight
                elif grp.index == index2:
                    grp.weight = 1-weight
                else:
                    ob.remove_from_group(grp, v.index)
    return

class VIEW3D_OT_PairWeightButton(bpy.types.Operator):
    bl_idname = "mhw.pair_weight"
    bl_label = "Weight pair"

    def execute(self, context):
        import bpy
        pairWeight(context)
        return{'FINISHED'}    

#----------------------------------------------------------
#   setupVertexPairs(ob):
#----------------------------------------------------------

def setupVertexPairs(context):
    ob = context.object
    verts = []
    for v in ob.data.vertices:
        x = v.co[0]
        y = v.co[1]
        z = v.co[2]
        verts.append((z,y,x,v.index))
    verts.sort()        
    lverts = {}
    rverts = {}
    mverts = {}
    nmax = len(verts)
    notfound = []
    for n,data in enumerate(verts):
        (z,y,x,vn) = data
        n1 = n - 20
        n2 = n + 20
        if n1 < 0: n1 = 0
        if n2 >= nmax: n2 = nmax
        vmir = findVert(verts[n1:n2], vn, -x, y, z, notfound)
        if vmir < 0:
            mverts[vn] = vn
        elif x > Epsilon:
            rverts[vn] = vmir
        elif x < -Epsilon:
            lverts[vn] = vmir
        else:
            mverts[vn] = vmir
    if notfound:            
        print("Did not find mirror image for vertices:")
        for msg in notfound:
            print(msg)
    print("Left-right-mid", len(lverts.keys()), len(rverts.keys()), len(mverts.keys()))
    return (lverts, rverts, mverts)
    
def findVert(verts, v, x, y, z, notfound):
    for (z1,y1,x1,v1) in verts:
        dx = x-x1
        dy = y-y1
        dz = z-z1
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < Epsilon:
            return v1
    if abs(x) > Epsilon:            
        notfound.append("  %d at (%.4f %.4f %.4f)" % (v, x, y, z))
    return -1                    

#
#    symmetrizeWeights(context):
#    class VIEW3D_OT_SymmetrizeWeightsButton(bpy.types.Operator):
#

Epsilon = 1e-3

def symmetrizeWeights(context, left2right):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    scn = context.scene

    left = {}
    left01 = {}
    left02 = {}
    leftIndex = {}
    left01Index = {}
    left02Index = {}
    right = {}
    right01 = {}
    right02 = {}
    rightIndex = {}
    right01Index = {}
    right02Index = {}
    symm = {}
    symmIndex = {}
    for vgrp in ob.vertex_groups:
        if vgrp.name[-2:] in ['_L', '.L', '_l', '.l']:
            nameStripped = vgrp.name[:-2]
            left[nameStripped] = vgrp
            leftIndex[vgrp.index] = nameStripped
        elif vgrp.name[-2:] in ['_R', '.R', '_r', '.r']:
            nameStripped = vgrp.name[:-2]
            right[nameStripped] = vgrp
            rightIndex[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.L.01', '.l.01']:
            nameStripped = vgrp.name[:-5]
            left01[nameStripped] = vgrp
            left01Index[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.R.01', '.r.01']:
            nameStripped = vgrp.name[:-5]
            right01[nameStripped] = vgrp
            right01Index[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.L.02', '.l.02']:
            nameStripped = vgrp.name[:-5]
            left02[nameStripped] = vgrp
            left02Index[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.R.02', '.r.02']:
            nameStripped = vgrp.name[:-5]
            right02[nameStripped] = vgrp
            right02Index[vgrp.index] = nameStripped
        else:
            symm[vgrp.name] = vgrp
            symmIndex[vgrp.index] = vgrp.name

    printGroups('Left', left, leftIndex, ob.vertex_groups)
    printGroups('Right', right, rightIndex, ob.vertex_groups)
    printGroups('Left01', left01, left01Index, ob.vertex_groups)
    printGroups('Right01', right01, right01Index, ob.vertex_groups)
    printGroups('Left02', left02, left02Index, ob.vertex_groups)
    printGroups('Right02', right02, right02Index, ob.vertex_groups)
    printGroups('Symm', symm, symmIndex, ob.vertex_groups)

    (lverts, rverts, mverts) = setupVertexPairs(context)
    if left2right:
        factor = 1
        fleft = left
        fright = right
        groups = list(right.values()) + list(right01.values()) + list(right02.values())
        cleanGroups(ob.data, groups)
    else:
        factor = -1
        fleft = right
        fright = left
        rverts = lverts
        groups = list(left.values()) + list(left01.values()) + list(left02.values())
        cleanGroups(ob.data, groups)

    for (vn, rvn) in rverts.items():
        v = ob.data.vertices[vn]
        rv = ob.data.vertices[rvn]
        #print(v.index, rv.index)
        for rgrp in rv.groups:
            rgrp.weight = 0
        for grp in v.groups:
            rgrp = None
            for (indices, groups) in [
                (leftIndex, right), (rightIndex, left),
                (left01Index, right01), (right01Index, left01),
                (left02Index, right02), (right02Index, left02),
                (symmIndex, symm)
                ]:
                try:
                    name = indices[grp.group]
                    rgrp = groups[name]
                except:
                    pass
            if rgrp:
                #print("  ", name, grp.group, rgrp.name, rgrp.index, v.index, rv.index, grp.weight)
                rgrp.add([rv.index], grp.weight, 'REPLACE')
            else:                
                gn = grp.group
                print("*** No rgrp for %s %s %s" % (grp, gn, ob.vertex_groups[gn]))
    return len(rverts)

def printGroups(name, groups, indices, vgroups):
    print(name)
    for (nameStripped, grp) in groups.items():
        print("  ", nameStripped, grp.name, indices[grp.index])
    return

def cleanGroups(me, groups):
    for grp in groups:
        print(grp)
        for v in me.vertices:
            grp.remove([v.index])
    return
    
class VIEW3D_OT_SymmetrizeWeightsButton(bpy.types.Operator):
    bl_idname = "mhw.symmetrize_weights"
    bl_label = "Symmetrize weights"
    left2right = BoolProperty()

    def execute(self, context):
        import bpy
        n = symmetrizeWeights(context, self.left2right)
        print("Weights symmetrized, %d vertices" % n)
        return{'FINISHED'}    
        
#
#    cleanRight(context, doRight):
#    class VIEW3D_OT_CleanRightButton(bpy.types.Operator):
#

def cleanRight(context, doRight):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    (lverts, rverts, mverts) = setupVertexPairs(context)
    for vgrp in ob.vertex_groups:
        if doRight:
            if vgrp.name[-2:] in ['_L', '.L', '_l', '.l']:
                for (vn, rvn) in rverts.items():
                    vgrp.remove([rvn])
        else:                    
            if vgrp.name[-2:] in ['_R', '.R', '_r', '.r']:
                for (vn, rvn) in rverts.items():
                    vgrp.remove([vn])
    return

class VIEW3D_OT_CleanRightButton(bpy.types.Operator):
    bl_idname = "mhw.clean_right"
    bl_label = "Clean right"
    doRight = BoolProperty()

    def execute(self, context):
        cleanRight(context, self.doRight)
        return{'FINISHED'}    

#
#    symmetrizeShapes(context, left2right):
#    class VIEW3D_OT_SymmetrizeShapesButton(bpy.types.Operator):
#

def symmetrizeShapes(context, left2right):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    scn = context.scene
    (lverts, rverts, mverts) = setupVertexPairs(context)
    if not left2right:
        rverts = lverts

    for key in ob.data.shape_keys.key_blocks:
        print(key.name)
        for rvn in rverts.values():
            rv = ob.data.vertices[rvn]
            key.data[rv.index].co = rv.co

        for v in ob.data.vertices:
            try:
                rvn = rverts[v.index]
            except:
                rvn = None
            if rvn:
                lco = key.data[v.index].co
                rco = lco.copy()
                rco[0] = -rco[0]
                key.data[rvn].co = rco

    return len(rverts)

class VIEW3D_OT_SymmetrizeShapesButton(bpy.types.Operator):
    bl_idname = "mhw.symmetrize_shapes"
    bl_label = "Symmetrize shapes"
    left2right = BoolProperty()

    def execute(self, context):
        n = symmetrizeShapes(context, self.left2right)
        print("Shapes symmetrized, %d vertices" % n)
        return{'FINISHED'}    

#
#    shapekeyFromObject(ob, targ):
#    class VIEW3D_OT_ShapeKeysFromObjectsButton(bpy.types.Operator):
#

def shapekeyFromObject(ob, targ):
    verts = ob.data.vertices
    tverts = targ.data.vertices
    print("Create shapekey %s" % targ.name)
    print(len(verts), len(tverts))
    if len(verts) != len(tverts):
        print("%s and %s do not have the same number of vertices" % (ob, targ))
        return
    if not ob.data.shape_keys:
        ob.shape_key_add(name='Basis', from_mix=False)
    skey = ob.shape_key_add(name=targ.name, from_mix=False)
    for n,v in enumerate(verts):
        vt = tverts[n].co
        pt = skey.data[n].co
        pt[0] = vt[0]
        pt[1] = vt[1]
        pt[2] = vt[2]
    print("Shape %s created" % skey)
    return    

class VIEW3D_OT_ShapeKeysFromObjectsButton(bpy.types.Operator):
    bl_idname = "mhw.shapekeys_from_objects"
    bl_label = "Shapes from objects"

    def execute(self, context):
        import bpy
        ob = context.object
        for targ in context.scene.objects:
            if targ.type == 'MESH' and targ.select and targ != ob:
                shapekeyFromObject(ob, targ)
        print("Shapekeys created for %s" % ob)
        return{'FINISHED'}    

#
#    recoverDiamonds(context):
#    class VIEW3D_OT_RecoverDiamondsButton(bpy.types.Operator):
#

def recoverDiamonds(context):
    ob = context.object
    for dob in context.scene.objects:
        if dob.select and dob.type == 'MESH' and dob != ob:
            break
    if not dob:
        raise NameError("Need two selected meshes")

    if len(dob.data.vertices) < len(ob.data.vertices):
        tmp = dob
        dob = ob
        ob = tmp

    dverts = dob.data.vertices
    verts = ob.data.vertices
    Epsilon = 1e-4

    context.scene.objects.active = dob
    bpy.ops.object.vertex_group_remove(all=True)

    vassoc = {}
    dn = 0
    for v in verts:
        vec = dverts[dn].co - v.co
        while vec.length > Epsilon:
            dn += 1
            vec = dverts[dn].co - v.co
        vassoc[v.index] = dn

    for grp in ob.vertex_groups:
        group = dob.vertex_groups.new(grp.name)
        index = group.index
        for v in verts:    
            for vgrp in v.groups:
                if vgrp.group == index:
                    dn = vassoc[v.index]
                    #dob.vertex_groups.assign( [dn], group, vgrp.weight, 'REPLACE' )
                    group.add( [dn], vgrp.weight, 'REPLACE' )
                    continue

    print("Diamonds recovered")
    return
    

class VIEW3D_OT_RecoverDiamondsButton(bpy.types.Operator):
    bl_idname = "mhw.recover_diamonds"
    bl_label = "Recover diamonds"

    def execute(self, context):
        recoverDiamonds(context)
        return{'FINISHED'}    

#
#    exportVertexGroups(filePath)
#    class VIEW3D_OT_ExportVertexGroupsButton(bpy.types.Operator):
#

def exportVertexGroups(context):
    filePath = context.scene['MhxVertexGroupFile']
    fileName = os.path.expanduser(filePath)
    fp = open(fileName, "w")
    ob = context.object
    me = ob.data
    for vg in ob.vertex_groups:
        index = vg.index
        weights = []
        for v in me.vertices:
            for grp in v.groups:
                if grp.group == index and grp.weight > 0.005:
                    weights.append((v.index, grp.weight))

        exportList(context, weights, vg.name, fp)
    fp.close()
    print("Vertex groups exported to %s" % fileName)
    return

class VIEW3D_OT_ExportVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.export_vertex_groups"
    bl_label = "Export vertex groups"

    def execute(self, context):
        exportVertexGroups(context)
        return{'FINISHED'}    

#
#    exportSumGroups(context):
#    exportListAsVertexGroup(weights, name, fp):
#    class VIEW3D_OT_ExportSumGroupsButton(bpy.types.Operator):
#

def exportSumGroups(context):
    filePath = context.scene['MhxVertexGroupFile']
    fileName = os.path.expanduser(filePath)
    fp = open(fileName, "w")
    ob = context.object
    me = ob.data
    for name in ['UpArm', 'LoArm', 'UpLeg']:
        for suffix in ['_L', '_R']:
            weights = {}
            for n in range(1,4):
                vg = ob.vertex_groups["%s%d%s" % (name, n, suffix)]
                index = vg.index
                for v in me.vertices:
                    for grp in v.groups:
                        if grp.group == index:
                            try:
                                w = weights[v.index]
                            except:
                                w = 0
                            weights[v.index] = grp.weight + w
                # ob.vertex_groups.remove(vg)
            exportList(context, weights.items(), name+'3'+suffix, fp)
    fp.close()
    return

def exportList(context, weights, name, fp):
    #if len(weights) == 0:
    #    return
    if context.scene['MhxExportAsWeightFile']:
        if len(weights) > 0:
            fp.write("\n# weights %s\n" % name)
            for (vn,w) in weights:
                if w > 0.005:
                    fp.write("  %d %.3g\n" % (vn, w))
    else:
        fp.write("\n  VertexGroup %s\n" % name)
        for (vn,w) in weights:
            if w > 0.005:
                fp.write("    wv %d %.3g ;\n" % (vn, w))
        fp.write("  end VertexGroup %s\n" % name)
    return

class VIEW3D_OT_ExportSumGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.export_sum_groups"
    bl_label = "Export sum groups"

    def execute(self, context):
        exportSumGroups(context)
        return{'FINISHED'}    

#
#    exportShapeKeys(filePath)
#    class VIEW3D_OT_ExportShapeKeysButton(bpy.types.Operator):
#

def exportShapeKeys(context):
    filePath = context.scene['MhxVertexGroupFile']
    fileName = os.path.expanduser(filePath)
    fp = open(fileName, "w")
    ob = context.object
    me = ob.data
    lr = "Sym"
    for skey in me.shape_keys.key_blocks:
        name = skey.name.replace(' ','_')    
        if name == "Basis":
            continue
        print(name)
        fp.write("  ShapeKey %s %s True\n" % (name, lr))
        fp.write("    slider_min %.2f ;\n" % skey.slider_min)
        fp.write("    slider_max %.2f ;\n" % skey.slider_max)
        for (n,pt) in enumerate(skey.data):
           vert = me.vertices[n]
           dv = pt.co - vert.co
           if dv.length > Epsilon:
               fp.write("    sv %d %.4f %.4f %.4f ;\n" %(n, dv[0], dv[1], dv[2]))
        fp.write("  end ShapeKey\n")
        print(skey)
    fp.close()
    print("Shape keys exported to %s" % fileName)
    return

class VIEW3D_OT_ExportShapeKeysButton(bpy.types.Operator):
    bl_idname = "mhw.export_shapekeys"
    bl_label = "Export shapekeys"

    def execute(self, context):
        exportShapeKeys(context)
        return{'FINISHED'}    

#
#   listVertPairs(context):
#   class VIEW3D_OT_ListVertPairsButton(bpy.types.Operator):
#

def listVertPairs(context):
    filePath = context.scene['MhxVertexGroupFile']
    fileName = os.path.expanduser(filePath)
    print("Open %s" % fileName)
    fp = open(fileName, "w")
    ob = context.object
    verts = []
    for v in ob.data.vertices:
        if v.select:
            verts.append((v.co[2], v.index))
    verts.sort()
    nmax = int(len(verts)/2)
    fp.write("Pairs = (\n")
    for n in range(nmax):
        (z1, vn1) = verts[2*n]
        (z2, vn2) = verts[2*n+1]
        v1 = ob.data.vertices[vn1]
        v2 = ob.data.vertices[vn2]
        x1 = v1.co[0]
        y1 = v1.co[1]
        x2 = v2.co[0]
        y2 = v2.co[1]
        print("%d (%.4f %.4f %.4f)" % (v1.index, x1,y1,z1))
        print("%d (%.4f %.4f %.4f)\n" % (v2.index, x2,y2,z2))
        if ((abs(z1-z2) > Epsilon) or
            (abs(x1+x2) > Epsilon) or
            (abs(y1-y2) > Epsilon)):
            raise NameError("Verts %d and %d not a pair:\n  %s\n  %s\n" % (v1.index, v2.index, v1.co, v2.co))
        if x1 > x2:
            fp.write("    (%d, %d),\n" % (v1.index, v2.index))            
        else:
            fp.write("    (%d, %d),\n" % (v2.index, v1.index))            
    fp.write(")\n")
    fp.close()
    print("Wrote %s" % fileName)
    return

class VIEW3D_OT_ListVertPairsButton(bpy.types.Operator):
    bl_idname = "mhw.list_vert_pairs"
    bl_label = "List vert pairs"

    def execute(self, context):
        listVertPairs(context)
        return{'FINISHED'}    
                   
#
#
#


def joinMeshes(context):
    scn = context.scene
    base = context.object
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    clothes = []
    for ob in context.selected_objects:
        if ob != base and ob.type == 'MESH':
            clothes.append(ob)
            scn.objects.active = ob            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    print("Joining %s to %s" % (clothes, base))            

    verts = []
    faces = []    
    texfaces = []
    v0 = appendStuff(base, 0, verts, faces, texfaces)
    for clo in clothes:
        v0 = appendStuff(clo, v0, verts, faces, texfaces)
    me = bpy.data.meshes.new("NewBase")
    me.from_pydata(verts, [], faces)

    uvtex = me.uv_textures.new(name = "UVTex")
    for n,tf in enumerate(texfaces):
        print(n, tf)
        uvtex.data[n].uv = tf        
    ob = bpy.data.objects.new("NewBase", me)
    scn.objects.link(ob)
    scn.objects.active = ob
    print("Meshes joined")
    
    
    return
             
def appendStuff(ob, v0, verts, faces, texfaces):                
    for v in ob.data.vertices:
        verts.append(v.co)
    for f in ob.data.faces:
        face = []
        for vn in f.vertices:
            face.append(vn + v0)
        faces.append(face)
    v0 += len(ob.data.vertices)    
    
    if ob.data.uv_textures:
        uvtex = ob.data.uv_textures[0]
        for f in ob.data.faces:
            tf = uvtex.data[f.index].uv
            texfaces.append(tf)
    else:
        x0 = 0.99
        y0 = 0.99
        x1 = 1.0
        y1 = 1.0
        for f in ob.data.faces:
            tf = ((x0,y0),(x0,y1),(x1,y0),(x1,y1))
            texfaces.append(tf)                
    print("Done %s %d verts" % (ob.name, v0))
    return v0

class VIEW3D_OT_JoinMeshesButton(bpy.types.Operator):
    bl_idname = "mhw.join_meshes"
    bl_label = "Join meshes"

    def execute(self, context):
        joinMeshes(context)
        return{'FINISHED'}    
                 
#                 
#   fixBaseFile():
#

the3dobjFolder = "C:/home/svn/makehuman/data/3dobjs"

def fixBaseFile():
    fp = open(os.path.join(the3dobjFolder, "base0.obj"), "rU")
    grp = None
    grps = {}
    fn = 0
    for line in fp:
        words = line.split()
        if words[0] == "f":
            grps[fn] = grp
            fn += 1
        elif words[0] == "g":
            grp = words[1]
    fp.close()
    
    infp = open(os.path.join(the3dobjFolder, "base1.obj"), "rU")
    outfp = open(os.path.join(the3dobjFolder, "base2.obj"), "w")
    fn = 0
    grp = None
    for line in infp:
        words = line.split()
        if words[0] == "f":
            try:
                fgrp = grps[fn]
            except:
                fgrp = None
            if fgrp != grp:
                grp = fgrp
                outfp.write("g %s\n" % grp)
            fn += 1
        outfp.write(line)
    infp.close()
    outfp.close()
    print("Base file fixed")
    return

class VIEW3D_OT_FixBaseFileButton(bpy.types.Operator):
    bl_idname = "mhw.fix_base_file"
    bl_label = "Fix base file"

    def execute(self, context):
        fixBaseFile()
        return{'FINISHED'}    
        
        
#
#    class CProxy
#

class CProxy:
    def __init__(self):
        self.refVerts = []
        self.firstVert = 0
        return
        
    def setWeights(self, verts, grp):
        rlen = len(self.refVerts)
        mlen = len(verts)
        first = self.firstVert
        if (first+rlen) != mlen:
            raise NameError( "Bug: %d refVerts != %d meshVerts" % (first+rlen, mlen) )
        gn = grp.index
        for n in range(rlen):
            vert = verts[n+first]
            refVert = self.refVerts[n]
            if type(refVert) == tuple:
                (rv0, rv1, rv2, w0, w1, w2, d0, d1, d2) = refVert
                vw0 = CProxy.getWeight(verts[rv0], gn)
                vw1 = CProxy.getWeight(verts[rv1], gn)
                vw2 = CProxy.getWeight(verts[rv2], gn)
                vw = w0*vw0 + w1*vw1 + w2*vw2
            else:
                vw = getWeight(verts[rv0], gn)
            grp.add([vert.index], vw, 'REPLACE')
        return
        
    def getWeight(vert, gn):
        for grp in vert.groups:
            if grp.group == gn:
                return grp.weight
        return 0                

    def read(self, filepath):
        realpath = os.path.realpath(os.path.expanduser(filepath))
        folder = os.path.dirname(realpath)
        try:
            tmpl = open(filepath, "rU")
        except:
            tmpl = None
        if tmpl == None:
            print("*** Cannot open %s" % realpath)
            return None

        status = 0
        doVerts = 1
        vn = 0
        for line in tmpl:
            words= line.split()
            if len(words) == 0:
                pass
            elif words[0] == '#':
                status = 0
                if len(words) == 1:
                    pass
                elif words[1] == 'verts':
                    if len(words) > 2:
                        self.firstVert = int(words[2])                    
                    status = doVerts
                else:
                    pass
            elif status == doVerts:
                if len(words) == 1:
                    v = int(words[0])
                    self.refVerts.append(v)
                else:                
                    v0 = int(words[0])
                    v1 = int(words[1])
                    v2 = int(words[2])
                    w0 = float(words[3])
                    w1 = float(words[4])
                    w2 = float(words[5])            
                    d0 = float(words[6])
                    d1 = float(words[7])
                    d2 = float(words[8])
                    self.refVerts.append( (v0,v1,v2,w0,w1,w2,d0,d1,d2) )
        return
        
class VIEW3D_OT_ProjectWeightsButton(bpy.types.Operator):
    bl_idname = "mhw.project_weights"
    bl_label = "Project weights from proxy"

    def execute(self, context):
        ob = context.object
        proxy = CProxy()
        proxy.read(os.path.join(the3dobjFolder, "base.mhclo"))
        for grp in ob.vertex_groups:
            print(grp.name)
            proxy.setWeights(ob.data.vertices, grp)
        print("Weights projected from proxy")
        return{'FINISHED'}    

                 
#
#    initInterface(context):
#    class VIEW3D_OT_InitInterfaceButton(bpy.types.Operator):
#

def initInterface(context):
    bpy.types.Scene.MhxVertNum = IntProperty(
        name="Vert number", 
        description="Vertex number to select")

    bpy.types.Scene.MhxWeight = FloatProperty(
        name="Weight", 
        description="Weight of bone1, 1-weight of bone2", 
        min=0, max=1)

    bpy.types.Scene.MhxBone1 = StringProperty(
        name="Bone 1", 
        maxlen=40,
        default='')

    bpy.types.Scene.MhxBone2 = StringProperty(
        name="Bone 2", 
        maxlen=40,
        default='')

    bpy.types.Scene.MhxExportAsWeightFile = BoolProperty(
        name="Export as weight file", 
        default=False)

    bpy.types.Scene.MhxVertexGroupFile = StringProperty(
        name="Vertex group file", 
        maxlen=100,
        default='')


    scn = context.scene
    if scn:
        scn['MhxWeight'] = 1.0
        scn['MhxBone1'] = 'Bone1'
        scn['MhxBone2'] = 'Bone2'
        scn['MhxExportAsWeightFile'] = False
        scn['MhxVertexGroupFile'] = '/home/vgroups.txt'

    return

class VIEW3D_OT_InitInterfaceButton(bpy.types.Operator):
    bl_idname = "mhw.init_interface"
    bl_label = "Initialize"

    def execute(self, context):
        import bpy
        initInterface(context)
        print("Interface initialized")
        return{'FINISHED'}    

#
#    class MhxWeightToolsPanel(bpy.types.Panel):
#

class MhxWeightToolsPanel(bpy.types.Panel):
    bl_label = "Weight tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        layout.operator("mhw.print_vnums")
        layout.operator("mhw.print_enums")
        layout.operator("mhw.print_fnums")
        layout.operator("mhw.select_quads")
        layout.operator("mhw.copy_vertex_groups")
        layout.operator("mhw.remove_vertex_groups")
        layout.operator("mhw.unvertex_selected")
        layout.operator("mhw.unvertex_diamonds")
        layout.operator("mhw.delete_diamonds")
        layout.operator("mhw.recover_diamonds")

        layout.separator()
        layout.prop(context.scene, 'MhxVertNum')
        layout.operator("mhw.select_vnum")

        layout.separator()
        layout.operator("mhw.symmetrize_weights", text="Symm weights L=>R").left2right = True
        layout.operator("mhw.symmetrize_weights", text="Symm weights R=>L").left2right = False
        layout.operator("mhw.clean_right", text="Clean right side of left vgroups").doRight = True
        layout.operator("mhw.clean_right", text="Clean left side of right vgroups").doRight = False
        layout.operator("mhw.symmetrize_shapes", text="Symm shapes L=>R").left2right = True    
        layout.operator("mhw.symmetrize_shapes", text="Symm shapes R=>L").left2right = False

        layout.separator()
        layout.prop(context.scene, 'MhxVertexGroupFile')
        layout.prop(context.scene, 'MhxExportAsWeightFile')
        layout.operator("mhw.export_vertex_groups")    
        layout.operator("mhw.export_sum_groups")    
        
        layout.operator("mhw.list_vert_pairs")            

        layout.separator()
        layout.operator("mhw.shapekeys_from_objects")    
        layout.operator("mhw.export_shapekeys")    

        layout.label('Weight pair')
        layout.prop(context.scene, 'MhxWeight')
        layout.prop(context.scene, 'MhxBone1')
        layout.prop(context.scene, 'MhxBone2')
        layout.operator("mhw.pair_weight")
        
        layout.label("Helper construction")
        layout.operator("mhw.join_meshes")
        layout.operator("mhw.fix_base_file")
        layout.operator("mhw.project_weights")

#
#    Init and register
#

initInterface(bpy.context)

def register():
    bpy.utils.register_module(__name__)
    pass

def unregister():
    bpy.utils.unregister_module(__name__)
    pass

if __name__ == "__main__":
    register()


