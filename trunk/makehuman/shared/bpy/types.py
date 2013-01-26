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
import os
import log

import object_collection
import export_config
from mhx import the


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
        bone.roll = self.boneInfo.rolls[bname]
        bone.parent = parent

        bone.matrixLocalFromBone()

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
        self.matrix_local = Matrix()
        self.matrix = Matrix()
        

    def getLength(self):
        vector = self.tail.vector - self.head.vector
        return sqrt(dot(vector, vector))
        
    def setLength(self):
        pass
  
    length = property(getLength, setLength)


    def matrixLocalFromBone(self):        
    
        u = self.tail.sub(self.head)
        length = sqrt(u.dot(u))
        if length < 1e-3:
            log.message("Zero-length bone %s. Removed" % self.name)
            self.matrix_local.matrix[:3,3] = self.head.vector
            return
        u = u.div(length)

        yu = Bone.ey.dot(u)        
        if abs(yu) > 0.99999:
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
        if self.roll:
            roll = tm.rotation_matrix(self.roll, Bone.ey)
            mat = dot(mat, roll)
        self.matrix_local = Matrix(mat)
        self.matrix_local.matrix[:3,3] = self.head.vector


#------------------------------------------------------------------
#   Mesh
#------------------------------------------------------------------

class Mesh(Rna):
    def __init__(self, name):
        Rna.__init__(self, name, 'MESH')
        self.vertices = []
        self.faces = []
        self.uv_layers = []
        self.materials = []
        self.shape_keys = []
        
    def fromMeshData(self, mesh):        
        self.vertices = [MeshVertex(v.idx, v.co) for v in mesh.verts]
        self.faces = [[v.idx for v in f.verts] for f in mesh.faces]

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

        if stuff.meshInfo.uvValues:
            self.uv_layers.append(UvLayer(stuff.meshInfo.uvValues, stuff.meshInfo.faces))

        if stuff.hasMaterial():
            self.materials = [Material(stuff)]
        else:
            self.materials = []

        if stuff.meshInfo.targets:
            self.shape_keys = ShapeKeys()
            keyblock = KeyBlock("Basis", {})
            self.shape_keys.key_blocks.append(keyblock)
            for (name,shape) in stuff.meshInfo.targets:
                keyblock = KeyBlock(name, shape)
                self.shape_keys.key_blocks.append(keyblock)
                
            

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

class ShapeKeys:
    def __init__(self):
        self.key_blocks = []
        
        
class KeyBlock:
    def __init__(self, name, shape):
        self.name = name
        self.data = shape
        target = list(shape.items())
        target.sort()                
        self.indexes = [t[0] for t in target]
        self.vertices = [t[1] for t in target]
        
    def __repr__(self):
        return ("<KeyBlock %s>" % self.name)
        
#------------------------------------------------------------------
#   Material and Texture
#------------------------------------------------------------------

class Material(Rna):
    def __init__(self, stuff):
        
        Rna.__init__(self, self.materialName(stuff), 'MATERIAL')  
        self.diffuse_shader = 'LAMBERT'
        
        if stuff.material:
            self.diffuse_color = stuff.material.diffuse_color
            self.diffuse_intensity = stuff.material.diffuse_intensity
            self.specular_color = stuff.material.specular_color
            self.specular_intensity = stuff.material.specular_intensity
            self.specular_hardness = stuff.material.specular_hardness
            self.transparency = stuff.material.transparency
            self.translucency = stuff.material.translucency
            self.ambient_color = stuff.material.ambient_color
            self.emit_color = stuff.material.emit_color
            self.use_transparency = stuff.material.use_transparency
            self.alpha = stuff.material.alpha
        else:
            self.diffuse_color = (0.8,0.8,0.8)
            self.diffuse_intensity = 0.8
            self.specular_color = (1,1,1)
            self.specular_intensity = 0.1
            self.specular_hardness = 25
            self.transparency = 1
            self.translucency = 0.0
            self.ambient_color = (0,0,0)
            self.emit_color = (0,0,0)
            self.use_transparency = False
            self.alpha = 1

        self.texture_slots = []
        
        if stuff.texture:
            tex = Texture(stuff.texture)
            mtex = MaterialTextureSlot(tex)
            mtex.use_map_color_diffuse = True
            self.texture_slots.append(mtex)
        
        if stuff.specular:
            tex = Texture(stuff.specular)
            mtex = MaterialTextureSlot(tex)
            mtex.use_map_color_spec = True
            self.texture_slots.append(mtex)
        
        if stuff.normal:
            tex = Texture(stuff.normal)
            mtex = MaterialTextureSlot(tex)
            mtex.use_map_normal = True
            self.texture_slots.append(mtex)
        
        if stuff.transparency:
            tex = Texture(stuff.transparency)
            mtex = MaterialTextureSlot(tex)
            mtex.use_map_alpha = True
            self.texture_slots.append(mtex)
        
        if stuff.bump:
            tex = Texture(stuff.bump)
            mtex = MaterialTextureSlot(tex)
            mtex.use_map_normal = True
            self.texture_slots.append(mtex)
        
        if stuff.displacement:
            tex = Texture(stuff.displacement)
            mtex = MaterialTextureSlot(tex)
            mtex.use_map_displacement = True
            self.texture_slots.append(mtex)


    def materialName(self, stuff):
        if stuff.material: 
            return stuff.material.name
        elif stuff.texture: 
            (folder, filename) = stuff.texture
            return os.path.splitext(filename)[0]
        else:
            return "Material"
            

class MaterialTextureSlot:

    def __init__(self, tex):
        self.use_map_diffuse = False
        self.use_map_color_diffuse = False
        self.use_map_alpha = False
        self.use_map_translucency = False

        self.use_map_specular = False
        self.use_map_color_spec = False
        self.use_map_hardness = False

        self.use_map_ambient = False
        self.use_map_emit = False
        self.use_map_mirror = False
        self.use_map_raymir = False

        self.use_map_normal = False
        self.use_map_warp = False
        self.use_map_displacement = False
        
        self.texture = tex
    

class Texture(Rna):
    def __init__(self, filepair):
        folder,filename = filepair
        Rna.__init__(self, filename, 'TEXTURE')
        self.type = 'IMAGE'
        self.image = Image(filename, folder)
        

class Image(Rna):
    def __init__(self, filename, folder):     
        Rna.__init__(self, filename, 'IMAGE')
        self.filepath = export_config.getOutFileName(filename, folder, True, the.Human, the.Config)        

        
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
        self.location = Vector((0,0,0))
        self.rotation_euler = Vector((0,0,0))
        self.scale = Vector((1,1,1))
        
        if self.data.rnaType == 'MESH':
            self.vertex_groups = []
            if stuff.meshInfo:
                index = 0
                for name,weights in stuff.meshInfo.weights.items():
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
