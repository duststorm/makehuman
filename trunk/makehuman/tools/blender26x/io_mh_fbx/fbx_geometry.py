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

from . import fbx
from .fbx_basic import *
from .fbx_props import *
from .fbx_model import *
from . import fbx_material

#------------------------------------------------------------------
#   Geometry
#------------------------------------------------------------------

class CGeometry(CConnection):
    propertyTemplate = (
"""
""")

    def __init__(self, subtype, btype):
        CConnection.__init__(self, 'Geometry', subtype, btype)
        self.uvLayers = []
        self.materialLayers = []
        self.textureLayers = []
        

    def parseNodes(self, pnodes):
        rest = []
        for pnode in pnodes:
            if pnode.key == 'Layer' : 
                pass
            elif pnode.key == 'LayerElementUV' : 
                self.uvLayers.append( LayerElementUVNode().parse(pnode) )
            elif pnode.key == 'LayerElementMaterial' : 
                self.materialLayers.append( LayerElementMaterialNode().parse(pnode) )
            elif pnode.key == 'LayerElementTexture' : 
                self.textureLayers.append( LayerElementTextureNode().parse(pnode) )  
            else:
                rest.append(pnode)

        return CConnection.parseNodes(self, rest)

    
    def make(self, rna, ob=None, matfaces=None):        
        CConnection.make(self, rna)
        if not hasattr(rna, "materials"):
            return self
            
        tn = 0
        layer = DummyLayer()
        self.materialLayers.append(LayerElementMaterialNode().make(layer, 0, rna.materials, matfaces))
        
        for mn,mat in enumerate(rna.materials):
            if mat:
                parent = fbx.nodes.objects[ob.name]
                fbx.nodes.materials[mat.name].makeLink(parent)
                self.materials.append(mat)
                
                for mtex in mat.texture_slots:
                    if mtex and mtex.texture:
                        tex = mtex.texture
                        if tex and tex.type == 'IMAGE':
                            self.hastex = True

        self.textureLayers.append(LayerElementTextureNode().make(layer, 0, self.hastex))            
        return self

                                
    def writeFooter(self, fp):
        if not( self.uvLayers or self.materialLayers or self.textureLayers ):
            CConnection.writeFooter(self, fp)
            return
            
        for layer in self.uvLayers:
            layer.writeFbx(fp)
        for layer in self.materialLayers:
            layer.writeFbx(fp)
        for layer in self.textureLayers:
            layer.writeFbx(fp)

        fp.write(
            '        Layer: 0 {\n' +
            '            Version: 100\n')
        if self.uvLayers:
            self.writeLayerElement(fp, "LayerElementUV")
        if self.materialLayers:
            self.writeLayerElement(fp, "LayerElementMaterial")
        if self.textureLayers:
            self.writeLayerElement(fp, "LayerElementTexture")
        fp.write('        }\n')

        CConnection.writeFooter(self, fp)         


    def writeLayerElement(self, fp, type):
        fp.write(
            '            LayerElement:  {\n' +
            '                Type: "%s"\n' % type +
            '                TypedIndex: 0\n' +
            '            }\n')
                
        
    def build(self, rna):
        for node in self.uvLayers:
            node.build(rna)
        for node in self.materialLayers:
            node.build(rna)
        for node in self.textureLayers:
            node.build(rna)                
        return rna


#------------------------------------------------------------------
#   Layers
#------------------------------------------------------------------


class DummyLayer():
    def __init__(self):
        self.name = "Dummy"

    
class LayerElementNode(CFbx):
    def __init__(self, type):
        CFbx.__init__(self, type)
        self.mappingInfoType = "NoMappingInformation"
        self.referenceInformationType = "Direct"

    def parse(self, pnode0):
        CFbx.parse(self, pnode0)
        self.index = pnode0.values[0]
        for pnode in pnode0.values[1:]:
            values = pnode.values
            if pnode.key == "Name":
                self.name = values[0]
            elif pnode.key == 'MappingInformationType':
                self.mappingInfoType = values[0]
            elif pnode.key == 'ReferenceInformationType':
                self.referenceInformationType = values[0]
        return self                
        
    def make(self, layer, index):
        self.name = layer.name
        self.index = index

    def writeStart(self, fp):
        fp.write(
            '        %s: %d { \n' % (self.ftype, self.index) +
            '            Version: 101 \n' +
            '            Name: "%s" \n' % self.name +
            '            MappingInformationType: "%s"\n' % self.mappingInfoType+
            '            ReferenceInformationType: "%s"\n' % self.referenceInformationType)

    def build(self, me, layer):
        layer.name = self.name
        return
        

#------------------------------------------------------------------
#   UV Layer
#------------------------------------------------------------------

class LayerElementUVNode(LayerElementNode):

    def __init__(self):
        LayerElementNode.__init__(self, 'LayerElementUV')
        self.mappingInfoType = "NoMappingInformation"
        self.referenceInformationType = "Direct"
        self.vertices = CArray("UV", float, 2)
        self.faces = CArray("UVIndex", int, 1)

    def parse(self, pnode0):
        LayerElementNode.parse(self, pnode0)
        for pnode in pnode0.values[1:]:
            if pnode.key == 'UV':
                self.vertices.parse(pnode)
            elif pnode.key == 'UVIndex':
                self.faces.parse(pnode)
        return self                
        
    def make(self, layer, index, faces):
        LayerElementNode.make(self, layer, index)
        if fbx.usingMakeHuman:
            verts = layer.data
        else:
            verts = [list(data.uv) for data in layer.data]
        self.vertices.make(verts)
        self.faces.make(faces)
        return self
        
    def writeFbx(self, fp):
        self.writeStart(fp)
        self.vertices.writeFbx(fp)
        self.faces.writeFbx(fp)
        fp.write('        }\n')

    def build(self, me):
        uvtex = me.uv_textures.new()
        uvloop = me.uv_layers[-1]
        LayerElementNode.build(self, me, uvtex)
        for fn,vn in enumerate(self.faces.values):            
            uvloop.data[fn].uv = self.vertices.values[vn]
        return


#------------------------------------------------------------------
#   Material Layer
#------------------------------------------------------------------

class LayerElementMaterialNode(LayerElementNode):

    def __init__(self):
        LayerElementNode.__init__(self, 'LayerElementMaterial')
        self.materials = CArray("Materials", int, 1)
                
    def parse(self, pnode0):
        LayerElementNode.parse(self, pnode0)
        for pnode in pnode0.values[1:]:
            if pnode.key == 'Materials':
                self.materials.parse(pnode)
        return self                
        
    def make(self, layer, index, mats, faces):
        LayerElementNode.make(self, layer, index)
        if len(mats) == 1:
            self.mappingInfoType = "AllSame"
            self.referenceInformationType = "IndexToDirect"
            self.materials.make( [0] )
        else:
            self.mappingInfoType = "ByPolygon"
            self.referenceInformationType = "IndexToDirect"
            self.materials.make(faces)
        return self

    def writeFbx(self, fp):
        self.writeStart(fp)
        self.materials.writeFbx(fp)
        fp.write('        }\n')

    def build(self, me):
        pass
        #LayerElementNode.build(self, me, layer)


#------------------------------------------------------------------
#   Texture Layer
#------------------------------------------------------------------

class LayerElementTextureNode(LayerElementNode):

    def __init__(self):
        LayerElementNode.__init__(self, 'LayerElementTexture')
        self.blendMode = "Translucent"
        self.textureAlpha = 1.0
        self.hastex = False

    def parse(self, pnode0):
        LayerElementNode.parse(self, pnode0)
        for pnode in pnode0.values[1:]:
            if pnode.key == 'BlendMode':
                self.blendMode = pnode.values[0]
            elif pnode.key == 'TextureAlpha':
                self.textureAlpha = pnode.values[0]
        return self                
        
    def make(self, layer, index, hastex):
        self.hastex = hastex
        LayerElementNode.make(self, layer, index)
        if hastex:
            self.mappingInfoType = "ByPolygonVertex"
            self.referenceInformationType = "IndexToDirect"
        else:
            self.mappingInfoType = "NoMappingInformation"
            self.referenceInformationType = "IndexToDirect"
            self.blendMode = "Translucent"
            self.textureAlpha = 1.0
        return self        

    def writeFbx(self, fp):
        self.writeStart(fp)
        if not self.hastex:
            fp.write(
                '            BlendMode: "%s"\n' % self.blendMode +
                '            TextureAlpha: %.4g\n' % self.textureAlpha)
        fp.write('        }\n')

    def build(self, me):
        pass
        #LayerElementNode.build(self, me, layer)
