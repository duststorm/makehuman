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
#   Data types
#------------------------------------------------------------------

data = None

class Rna:
    def __init__(self):
        self.animation_data = []
        

class Camera(Rna):    
    def __init__(self, name):
        global data
        Rna.__init__(self)
        data.cameras.append(self)        
    

class Lamp(Rna):
    def __init__(self, name):
        global data
        Rna.__init__(self)
        data.lamps.append(self)        


class Armature(Rna):
    def __init__(self, name):
        global data
        Rna.__init__(self)
        data.armatures.append(self)        


class Mesh(Rna):
    def __init__(self, name):
        global data
        Rna.__init__(self)
        data.meshes.append(self)        
        self.name = name
        
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


class Material:
    def __init__(self, smat, stex):
        global data
        Rna.__init__(self)        
        data.materials.append(self)
        self.texture_slots = []
        if stex:
            tex = Texture(stex)
            mtex = MTex(tex)
            self.texture
        print(smat.items())
        if img:
            tex = Texture(img)
        halt
        
        
class Texture:
    def __init__(self, tex):
        global data
        Rna.__init__(self)
        data.testures.append(self)
        folder,filename = stex
        filepath = os.path.join(folder, filename)
        tex.image = img
        

class Image:
    def __init__(self, tex):
        global data
        Rna.__init__(self)
        data.testures.append(self)

        
class Object(Rna):
    def __init__(self, name, content):
        global data
        Rna.__init__(self)
        data.objects.append(self)
        
        self.name = name        
        self.data = content
        self.parent = None
        self.matrix_world = Matrix()
        if isinstance(content, Mesh):
            self.type = 'MESH'

    
class Scene(Rna):
    def __init__(self, name="Scene"):
        global data
        Rna.__init__(self)
        data.scenes.append(self)
        self.name = name
        self.objects = []


class Action(Rna):           
    def __init__(self, name):
        global data
        Rna.__init__(self)
        data.actions.append(self)        
