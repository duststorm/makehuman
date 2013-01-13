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
Blender API mockup: bpy
This package is used by the FBX exporter. The actual exporter is located in the tools
directory and is a Blender plugin. By adding a few classes, the exporter can be tricked
the believe that it runs under Blender when it is actually invoked by MakeHuman.

"""

from . import types
from . import props
from . import utils
from mathutils import *

import numpy
import armature
from armature import transformations as tm

#------------------------------------------------------------------
#   Data types
#------------------------------------------------------------------

class Rna:
    def __init__(self):
        self.animation_data = []
        
        
class Mesh(Rna):
    def __init__(self, name):
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
        self.materials = []
        
        
class Object(Rna):
    def __init__(self, name, content):
        Rna.__init__(self)
        data.objects.append(self)
        
        self.name = name        
        self.data = content
        self.parent = None
        self.matrix_world = Matrix()
        if isinstance(content, Mesh):
            self.type = 'MESH'

    
class Material(Rna):
    def __init__(self, name, mat):
        Rna.__init__(self)
        data.materials.append(self)
        self.name = name


class Scene(Rna):
    def __init__(self, name="Scene"):
        Rna.__init__(self)
        data.scenes.append(self)
        self.name = name
        self.objects = []
           
   
#------------------------------------------------------------------
#   Context
#------------------------------------------------------------------

class Context:
    def __init__(self, scn):
        self.scene = scn
        self.object = None
        
#------------------------------------------------------------------
#   Data
#------------------------------------------------------------------
    
class Data:
    def __init__(self):
        self.objects = []
        self.meshes = []
        self.materials = []
        self.textures = []
        self.images = []
        self.armatures = []
        self.bones = []
        self.cameras = []
        self.lamps = []
        self.scenes = []
        self.actions = []

#------------------------------------------------------------------
#   Data
#------------------------------------------------------------------

def initialize():
    global context, data
    data = Data()
    scn = Scene()
    context = Context(scn)
    
    
def addMesh(name, mesh, isStuff=True):
    me = Mesh(name)
    if isStuff:
        me.fromStuff(mesh)
    else:
        me.fromMesh(mesh)
    ob = Object(name, me)
    scn = context.scene
    scn.objects.append(ob)
    

initialize()
usingMakeHuman = True
