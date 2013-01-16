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
    print(RnaNames)
        
def safeName(name, rnaType):
    global RnaNames 
    print("safename?", name)
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


class Armature(Rna):
    def __init__(self, name, rigData):
        Rna.__init__(self, name, 'ARMATURE')
        self.bones = []
        self.edit_bones = self.bones
        
        (self.heads, self.tails, hier, bnames, self.weights) = rigData
        self.addHierarchy(hier[0], None)
        

    def addHierarchy(self, hier, parent):
        print(hier)
        
        (bname, children) = hier
        print(bname, children)
        bone = Bone(bname)
        self.bones.append(bone)
        bone.head = Vector(self.heads[bname])
        bone.tail = Vector(self.tails[bname])
        bone.parent = parent
        
        vec = bone.tail.sub(bone.head)
        length = sqrt(vec.dot(vec))
        axis = vec.div(length)
        mat = Matrix().compose(bone.head, None, None)
        if parent:
            pmat = parent.matrix_local.inverted()
            bone.matrix_local = pmat.mult(mat)
        else:
            bone.matrix_local = mat

        bone.children = []
        for child in children:
            bone.children.append( self.addHierarchy(child, bone) )
        return bone
        

class Bone(Rna):
    def __init__(self, name):
        Rna.__init__(self, name, 'BONE')
        self.head = None
        self.tail = None
        self.parent = None
        self.roll = 0
        self.children = []
        self.matrix_local = Matrix()
        
        

class Mesh(Rna):
    def __init__(self, name):
        Rna.__init__(self, name, 'MESH')
        
    def fromMeshData(self, mesh):        
        self.vertices = [v.co for v in mesh.verts]
        self.faces = [[v.idx for v in f.verts] for f in mesh.faces]
        self.uv_layers = []
        self.materials = []

    def fromStuff(self, stuff):        
        self.vertices = stuff.verts
        self.faces = [[v[0] for v in f] for f in stuff.faces]
        self.uv_layers = []
        if stuff.uvValues:
            self.uv_layers.append(UvLayer(stuff.uvValues, stuff.faces))
        self.materials = []
        """
        print("Mat", stuff.material)
        print("Tex", stuff.texture)
        if stuff.material or stuff.texture:
            mat = Material(stuff.material, stuff.texture)
            self.materials.append(mat)

        nVerts = len(stuff.verts)
        nUvVerts = len(stuff.uvValues)
        nNormals = nVerts
        nWeights = len(stuff.skinWeights)
        nBones = len(stuff.bones)
        nTargets = len(stuff.targets)
        """
            
        
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

        
class Object(Rna):
    def __init__(self, name, content):
        Rna.__init__(self, name, 'OBJECT')
        
        self.data = content
        self.type = content.rnaType
        self.parent = None
        self.matrix_world = Matrix()
        
        if self.data.rnaType == 'MESH':
            self.vertex_groups = []
        elif self.data.rnaType == 'ARMATURE':
            pass
        
    def __repr__(self):
        return ("<%s: %s type=%s data=%s parent=%s>" % (self.rnaType, self.name, self.type, self.data, self.parent))        

    
class Scene(Rna):
    def __init__(self, name="Scene"):
        Rna.__init__(self, name, 'SCENE')
        self.objects = []


class Action(Rna):           
    def __init__(self, name):
        Rna.__init__(self, name, 'ACTION')
