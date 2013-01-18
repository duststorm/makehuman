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
Blender API mockup: bpy.types

"""

from mathutils import *
from math import *

import object_collection

#------------------------------------------------------------------
#   Blender UI
#------------------------------------------------------------------

class Panel:    
    def __init__(self):
        pass
        
class Operator:
    def __init__(self):
        pass

#------------------------------------------------------------------
#   Init
#------------------------------------------------------------------

def initialize():
    global RnaNames 
    RnaNames = {}
    for rnaType in ['OBJECT', 'MESH', 'ARMATURE', 'MATERIAL', 'TEXTURE', 'IMAGE', 'SCENE', 'BONE']:
        RnaNames[rnaType] = {}
        
def safeName(name, rnaType):
    global RnaNames 
    names = RnaNames[rnaType]
    try:
        names[name]
    except KeyError:
        names[name] = name
        return name
    try:
        n = int(name[-3])
        name = name[:-3] + str(n+1)
    except:
        name = name + ".001"
    return safeName(name, rnaType)           

#------------------------------------------------------------------
#   RNA types
#------------------------------------------------------------------

class Rna:
    def __init__(self, name, rnaType):
        self.animation_data = []
        self.name = safeName(name, rnaType)
        self.rnaType = rnaType
        
    def __repr__(self):
        return ("<%s: %s>" % (self.rnaType, self.name))
        

class Camera(Rna):    
    def __init__(self, name):
        Rna.__init__(self, name, 'CAMERA')
    

class Lamp(Rna):
    def __init__(self, name):
        Rna.__init__(self, name, 'LAMP')


#------------------------------------------------------------------
#   Collection
#------------------------------------------------------------------

class Collection:
    def __init__(self):
        self.data = {}
        
    def __getattr__(self, attr):
        return self.data[attr]
        
    def __setattr__(self, attr, value):
        self.data[attr] = value
        
    def __iter__(self):
        return self.data.values
        
#------------------------------------------------------------------
#   Armature
#------------------------------------------------------------------

class Armature(Rna):

    def __init__(self, name, boneInfo):
        Rna.__init__(self, name, 'ARMATURE')
        self.bones = {}
        self.edit_bones = self.bones
        self.boneInfo = boneInfo
        self.addHierarchy(boneInfo.hier[0], None)
        

    def addHierarchy(self, hier, parent):
        (bname, children) = hier
        bone = Bone(bname)
        self.bones[bname] = bone
        bone.head = Vector(self.boneInfo.heads[bname])
        bone.tail = Vector(self.boneInfo.tails[bname])
        bone.roll = 0
        bone.parent = parent

        bone.matrixLocalFromBone()
        print("  ", bone)

        bone.children = []
        for child in children:
            bone.children.append( self.addHierarchy(child, bone) )
        return bone
        

class Bone(Rna):
    ex = Vector((1,0,0))
    ey = Vector((0,1,0))
    ez = Vector((0,0,1))

    def __init__(self, name):
        Rna.__init__(self, name, 'BONE')
        self.head = None
        self.tail = None
        self.parent = None
        self.roll = 0
        self.children = []
        self.matrix_local = None
        

    def matrixLocalFromBone(self):        
    
        u = self.tail.sub(self.head)
        length = sqrt(u.dot(u))
        if length < 1e-3:
            print("Zero-length bone %s. Removed" % self.name)
            self.matrix_local = tm.identity(4)
            self.matrix_local.matrix[:3,3] = self.head.vector
            return
        u = u.div(length)

        yu = Bone.ey.dot(u)        
        if abs(yu) > 0.999:
            axis = Bone.ey
            if yu > 0:
                angle = 0
            else:
                angle = pi
        else:        
            axis = Bone.ey.cross(u)
            length = sqrt(axis.dot(axis))
            axis = axis.div(length)
            angle = acos(yu)

        mat = tm.rotation_matrix(angle,axis)
        matrix = Matrix(mat)
        if self.parent:
            pmat = self.parent.matrix_local.inverted()
            self.matrix_local = matrix.mult(pmat)
        else:
            self.matrix_local = matrix
        self.matrix_local.matrix[:3,3] = self.head.vector


#------------------------------------------------------------------
#   Mesh
#------------------------------------------------------------------

class Mesh(Rna):
    def __init__(self, name):
        Rna.__init__(self, name, 'MESH')
        
    def fromMeshData(self, mesh):        
        self.vertices = [MeshVertex(v.idx, v.co) for v in mesh.verts]
        self.faces = [[v.idx for v in f.verts] for f in mesh.faces]
        self.uv_layers = []
        self.materials = []

    def fromStuff(self, stuff): 
        stuff.bones = []
        object_collection.setStuffSkinWeights(stuff)
        nVerts = len(stuff.meshInfo.verts)
        nUvVerts = len(stuff.meshInfo.uvValues)
        nNormals = nVerts
        nFaces = len(stuff.meshInfo.faces)
        nWeights = len(stuff.skinWeights)
        nBones = len(stuff.bones)
        nTargets = len(stuff.meshInfo.targets)

        self.vertices = [MeshVertex(n, v) for (n,v) in enumerate(stuff.meshInfo.verts)]
        self.polygons = [MeshPolygon(n, [v[0] for v in f]) for (n,f) in enumerate(stuff.meshInfo.faces)]
        self.uv_layers = []
        if stuff.meshInfo.uvValues:
            self.uv_layers.append(UvLayer(stuff.meshInfo.uvValues, stuff.meshInfo.faces))
        self.materials = []
            

class MeshVertex:
    def __init__(self, idx, co):
        self.index = idx
        self.co = co
        self.normal = []
        self.groups = []
        
    def addToGroup(self, index, weight):
        group = MeshGroup(index, weight)
        self.groups.append(group)

        
class VertexGroup:
    def __init__(self, name, index):
        self.name = name
        self.index = index        
        

class MeshGroup:
    def __init__(self, index, weight):
        self.group = index
        self.weight = weight

        
class MeshPolygon:
    def __init__(self, idx, verts):
        self.index = idx
        self.vertices = verts
        self.material_index = 0
        
        
class UvLayer:
    def __init__(self, uvValues, faces):
        self.uvloop = UvLoop("UVset0", uvValues)
        self.uvfaces = flattenIntList( [[v[1] for v in f] for f in faces] )


def flattenIntList(list):
    string = str(list).replace('[', '').replace(']', '')
    return [int(x) for x in string.split(',') if x.strip()]

        
class UvLoop:
    def __init__(self, name, uvValues):
        self.name = name
        self.data = uvValues

#------------------------------------------------------------------
#   Material and Texture
#------------------------------------------------------------------

class Material(Rna):
    def __init__(self, smat, stex):
        Rna.__init__(self, smat.name, 'MATERIAL')        
        self.texture_slots = []
        if stex:
            tex = Texture(stex)
            mtex = MTex(tex)
            self.texture
        print(smat.items())
        if img:
            tex = Texture(img)
        halt
        
        
class Texture(Rna):
    def __init__(self, tex):
        folder,filename = stex
        Rna.__init__(self, filename, 'TEXTURE')
        filepath = os.path.join(folder, filename)
        tex.image = img
        

class Image(Rna):
    def __init__(self, tex):
        Rna.__init__(self, tex.name, 'IMAGE')

        
#------------------------------------------------------------------
#   Object
#------------------------------------------------------------------

class Object(Rna):
    def __init__(self, name, content, stuff=None):
        Rna.__init__(self, name, 'OBJECT')
        
        self.data = content
        self.type = content.rnaType
        self.parent = None
        self.matrix_world = Matrix()
        self.select = True
        
        if self.data.rnaType == 'MESH':
            self.vertex_groups = []
            if stuff.meshInfo:
                index = 0
                for name,weights in stuff.meshInfo.weights.items():
                    print("OBJ", name, weights)
                    self.vertex_groups.append(VertexGroup(name, index))
                    for (vn,w) in weights:
                        content.vertices[vn].addToGroup(index, w)
                    index += 1
        elif self.data.rnaType == 'ARMATURE':
            pass
        
    def __repr__(self):
        return ("<%s: %s type=%s data=%s parent=%s>" % (self.rnaType, self.name, self.type, self.data, self.parent))        

   
#------------------------------------------------------------------
#   Scene and Action
#------------------------------------------------------------------

class Scene(Rna):
    def __init__(self, name="Scene"):
        Rna.__init__(self, name, 'SCENE')
        self.objects = []


class Action(Rna):           
    def __init__(self, name):
        Rna.__init__(self, name, 'ACTION')
