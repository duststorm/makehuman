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
        PropertyTemplate: "FbxMesh" {
            Properties70:  {
                P: "Color", "ColorRGB", "Color", "",0.8,0.8,0.8
                P: "BBoxMin", "Vector3D", "Vector", "",0,0,0
                P: "BBoxMax", "Vector3D", "Vector", "",0,0,0
                P: "Primary Visibility", "bool", "", "",1
                P: "Casts Shadows", "bool", "", "",1
                P: "Receive Shadows", "bool", "", "",1
            }
        }
""")

    def __init__(self, subtype='Mesh'):
        CConnection.__init__(self, 'Geometry', subtype, 'MESH')
        self.parseTemplate('Mesh', CGeometry.propertyTemplate)
        self.isModel = True
        self.isObjectData = True
        self.mesh = None
        self.vertices = CArray("Vertices", float, 3, csys=True)
        self.normals = CArray("Normals", float, 3, csys=True)
        self.faces = CArray("PolygonVertexIndex", float, -1)
        self.hastex = False
        self.materials = []
        self.uvLayers = []
        self.materialLayers = []
        self.textureLayers = []
        

    def parseNodes(self, pnodes):
        rest = []
        for pnode in pnodes:
            if pnode.key == 'Vertices':
                self.vertices.parse(pnode)
            elif pnode.key == 'Normals':
                self.normals.parse(pnode)
            elif pnode.key == 'PolygonVertexIndex':
                self.faces.parse(pnode)
            elif pnode.key == 'Layer' : 
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

    
    def make(self, ob):        
        me = ob.data
        CConnection.make(self, me)
        self.mesh = me
        
        self.vertices.make( [v.co for v in me.vertices] )
        self.normals.make( [v.normal for v in me.vertices] )
        faces = [list(f.vertices) for f in me.polygons]
        nFaces = len(me.polygons)
        self.faces.make(faces)

        for index,uvloop in enumerate(me.uv_layers):
            if fbx.usingMakeHuman:
                uvlayer = me.uv_layers[index]
                uvloop = uvlayer.uvloop
                uvfaces = uvlayer.uvfaces
            else:
                uvloop = me.uv_layers[index]
                n = 0
                uvfaces = []
                for f in me.polygons:
                    m = len(f.vertices)
                    uvfaces += [k for k in range(n, n+m)]
                    n += m
            self.uvLayers.append(LayerElementUVNode().make(uvloop, index, uvfaces))
        
        tn = 0
        matfaces = [f.material_index for f in me.polygons]
        layer = DummyLayer()
        self.materialLayers.append(LayerElementMaterialNode().make(layer, 0, me.materials, matfaces))
        
        for mn,mat in enumerate(me.materials):
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
                                

    def writeHeader(self, fp):
        CConnection.writeHeader(self, fp)            
        self.vertices.writeFbx(fp)
        #self.normals.writeFbx(fp)
        self.faces.writeFbx(fp)
        fp.write(
            '       GeometryVersion: 124\n')
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
        if not self.hastex:
            self.writeLayerElement(fp, "LayerElementTexture")
        fp.write('        }\n')


    def writeLayerElement(self, fp, type):
        fp.write(
            '            LayerElement:  {\n' +
            '                Type: "%s"\n' % type +
            '                TypedIndex: 0\n' +
            '            }\n')
                
        
    def build3(self):
        me = fbx.data[self.id]
        me.from_pydata(self.vertices.values, [], self.faces.values)

        obNode,_ = self.getBParent('OBJECT')
        matNodes = obNode.getBChildren('MATERIAL')
        for node,channel in matNodes:
            mat = fbx.data[node.id]
            me.materials.append(mat)
            
        for node in self.uvLayers:
            node.build(me)
        for node in self.materialLayers:
            node.build(me)
        for node in self.textureLayers:
            node.build(me)
                
        return me


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

