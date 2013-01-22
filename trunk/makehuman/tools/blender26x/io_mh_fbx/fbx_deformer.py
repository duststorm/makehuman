# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from mathutils import *
import math

from . import fbx
from .fbx_basic import *
from .fbx_props import *
from .fbx_model import *

#------------------------------------------------------------------
#   Deformer
#------------------------------------------------------------------

class CSkinDeformer(CConnection):

    def __init__(self, subtype='Skin'):
        CConnection.__init__(self, 'Deformer', subtype, 'SKIN_DEFORMER')
        self.rigNode = None
        self.meshNode = None
        self.object = None
        self.subdeformers = {}
        
   
    def set(self, rigNode, meshNode, ob):
        self.rigNode = rigNode
        self.meshNode = meshNode
        self.object = ob
        return self
    
    
    def make(self, ob):
        CConnection.make(self, ob)
        
        amtNode = fbx.nodes.armatures[ob.data.name]
        for vgroup in self.object.vertex_groups:
            try:
                boneNode = amtNode.bones[vgroup.name]
            except KeyError:
                boneNode = None
            if boneNode:
                subdef = CClusterSubDeformer().make(vgroup, boneNode, self.object)
                self.subdeformers[vgroup.index] = subdef

        return self

    
    def addDefinition(self, definitions):     
        CConnection.addDefinition(self, definitions)
        for subdef in self.subdeformers.values():
            subdef.addDefinition(definitions)


    def writeLinks(self, fp):
        self.writeLink(fp, self.meshNode)
        for subdef in self.subdeformers.values():
            subdef.writeLink(fp, self)
            try:
                bone = self.rigNode.bones[subdef.name]
            except KeyError:
                continue
            bone.writeLink(fp, subdef)

    
    def writeHeader(self, fp):
        for subdef in self.subdeformers.values():
            subdef.writeFbx(fp)
        CConnection.writeHeader(self, fp)
        

    def build5(self):            
        meNode,_ = self.getBParent('MESH')
        obNode,_ = meNode.getBParent('OBJECT') 
        ob = fbx.data[obNode.id]

        rigNode,_ = obNode.getFParent2('Model', 'Null')
        if rigNode:
            rig = fbx.data[rigNode.id]
            mod = ob.modifiers.new(rig.name, 'ARMATURE')
            mod.object = rig
            mod.use_bone_envelopes = False
            mod.use_vertex_groups = True
        
        for child,_ in self.children:
            child.buildVertGroups(ob)
            
 

class CClusterSubDeformer(CConnection):
 
    def __init__(self, subtype='Cluster'):
         CConnection.__init__(self, 'Deformer', subtype, 'DEFORMER')
         self.indexes = CArray('Indexes', int, 1)
         self.weights = CArray('Weights', float, 1)
         self.transform = CArray('Transform', float, 4)
         self.transformLink = CArray('TransformLink', float, 4)

         
    def parseNodes(self, pnodes):
        rest = []
        for pnode in pnodes:
            if pnode.key == 'Indexes':
                self.indexes.parse(pnode)
            elif pnode.key == 'Weights':
                self.weights.parse(pnode)
            elif pnode.key == 'Transform':
                self.transform.parse(pnode)
            elif pnode.key == 'TransformLink':
                self.transformLink.parse(pnode)
            else:
                rest.append(pnode)
        return CConnection.parseNodes(self, rest)


    def make(self, vgroup, boneNode, ob):
        CConnection.make(self, vgroup)
        vnums = []
        weights = []
        for v in ob.data.vertices:
            for g in v.groups:
                if g.group == vgroup.index:
                    vnums.append(v.index)
                    weights.append(g.weight)
        self.indexes.make(vnums)
        self.weights.make(weights)
        self.transform.make(boneNode.transform)
        self.transformLink.make(boneNode.transformLink)
        return self
         

    def writeFooter(self, fp):
        self.indexes.writeFbx(fp)
        self.weights.writeFbx(fp)
        self.transform.writeFbx(fp)
        self.transformLink.writeFbx(fp)
        CConnection.writeFooter(self, fp)
        
        
    def buildVertGroups(self, ob):
        vg = ob.vertex_groups.new(self.name)
        for n,vn in enumerate(self.indexes.values):        
            w = self.weights.values[n]
            vg.add([vn], w, 'REPLACE')

 #------------------------------------------------------------------
 #   BlendShapeDeformer
 #------------------------------------------------------------------
 
class CBlendShapeDeformer(CConnection):

    def __init__(self, subtype='BlendShape'):
        CConnection.__init__(self, 'Deformer', subtype, 'BLEND_DEFORMER')
        self.mesh = None
        self.subdeformers = []
        
   
    def make(self, meshNode, me):
        CConnection.make(self, me)
        self.meshNode = meshNode
        self.mesh = me
        
        for index,skey in enumerate(me.shape_keys.key_blocks):
            if index > 0:
                skeyNode = meshNode.shapeKeys[skey.name]
                subdef = CBlendShapeChannelSubDeformer().make(skey)
                self.subdeformers.append(subdef)
                subdef.makeLink(self)
                skeyNode.makeLink(subdef)

        return self

    
    def addDefinition(self, definitions):     
        CConnection.addDefinition(self, definitions)
        for subdef in self.subdeformers:
            subdef.addDefinition(definitions)


    def writeLinks(self, fp):
        CConnection.writeLinks(self, fp)
        for subdef in self.subdeformers:
            subdef.writeLinks(fp)

    

    def writeFooter(self, fp):
        CConnection.writeFooter(self, fp)
        for subdef in self.subdeformers:
            subdef.writeFbx(fp)
        

    def build5(self):        
        meNode,_ = self.getBParent('MESH')
        obNode,_ = meNode.getBParent('OBJECT') 
        ob = fbx.data[obNode.id]
            

class CBlendShapeChannelSubDeformer(CConnection):
 
    def __init__(self, subtype='BlendShapeChannel'):
         CConnection.__init__(self, 'Deformer', subtype, 'DEFORMER')
         self.fullWeights = CArray('FullWeights', int, 1)

         
    def parseNodes(self, pnodes):
        rest = []
        for pnode in pnodes:
            if pnode.key == 'FullWeights':
                self.fullWeights.parse(pnode)
            else:
                rest.append(pnode)
        return CConnection.parseNodes(self, rest)


    def make(self, skey):
        CConnection.make(self, skey)
        self.fullWeights.make([100])
        self.set("DeformPercent", 0)
        return self
         

    def writeHeader(self, fp):
        CConnection.writeHeader(self, fp)
        self.fullWeights.writeFbx(fp) 

