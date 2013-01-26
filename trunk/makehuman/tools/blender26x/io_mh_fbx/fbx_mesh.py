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
from .fbx_geometry import *
from .fbx_deformer import *

#------------------------------------------------------------------
#   Geometry Mesh
#------------------------------------------------------------------

class FbxMesh(FbxGeometryBase):
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
        FbxGeometryBase.__init__(self, subtype, 'MESH')
        self.template = self.parseTemplate('GeometryMesh', FbxMesh.propertyTemplate)
        self.isModel = True
        self.isObjectData = True
        self.mesh = None
        self.vertices = CArray("Vertices", float, 3, csys=True)
        self.normals = CArray("Normals", float, 3, csys=True)
        self.faces = CArray("PolygonVertexIndex", float, -1)
        self.shapeKeys = {}
        self.hastex = False
        self.materials = []
        self.blendDeformer = None
        

    def parseNodes(self, pnodes):
        rest = []
        for pnode in pnodes:
            if pnode.key == 'Vertices':
                self.vertices.parse(pnode)
            elif pnode.key == 'Normals':
                self.normals.parse(pnode)
            elif pnode.key == 'PolygonVertexIndex':
                self.faces.parse(pnode)
            else:
                rest.append(pnode)

        return FbxGeometryBase.parseNodes(self, rest)

    
    def make(self, ob):        
        me = ob.data
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
            self.uvLayers.append(FbxLayerElementUV().make(uvloop, index, uvfaces))
        
        if me.shape_keys:
            baseVerts = me.vertices
            for index,skey in enumerate(me.shape_keys.key_blocks):
                if index == 0:
                    baseVerts = skey.data
                else:
                    node = FbxShape().make(skey, baseVerts)
                    self.shapeKeys[skey.name] = node
                    #node.makeLink(self)
            self.blendDeformer = FbxBlendShape().make(self, me)
            self.blendDeformer.makeLink(self)
            
        matfaces = [f.material_index for f in me.polygons]
        return FbxGeometryBase.make(self, me, ob, matfaces)
                                

    def writeHeader(self, fp):
        FbxGeometryBase.writeHeader(self, fp)            
        self.vertices.writeFbx(fp)
        self.normals.writeFbx(fp)
        self.faces.writeFbx(fp)
        fp.write(
            '       GeometryVersion: 124\n')
                

    def writeFooter(self, fp):
        FbxGeometryBase.writeFooter(self, fp)
        for node in self.shapeKeys.values():
            node.writeFbx(fp)
        if self.blendDeformer:
            self.blendDeformer.writeFbx(fp)
            

    def writeLinks(self, fp):
        FbxGeometryBase.writeLinks(self, fp)
        for node in self.shapeKeys.values():
            node.writeLinks(fp)
        if self.blendDeformer:        
            self.blendDeformer.writeLinks(fp)
            

    def build3(self):
        me = fbx.data[self.id]
        me.from_pydata(self.vertices.values, [], self.faces.values)

        obNode,_ = self.getBParent('OBJECT')
        matNodes = obNode.getBChildren('MATERIAL')
        for node,channel in matNodes:
            mat = fbx.data[node.id]
            me.materials.append(mat)
            
        return FbxGeometryBase.build(self, me)


#------------------------------------------------------------------
#   Blendshapes
#------------------------------------------------------------------

class FbxShape(FbxObject):

    def __init__(self, subtype='Shape'):
        FbxObject.__init__(self, 'Geometry', subtype, 'SHAPEKEY')
        self.indexes = CArray("Indexes", int, 1)
        self.vertices = CArray("Vertices", float, 3, csys=True)
        self.normals = CArray("Normals", float, 3, csys=True)
        self.set("Version", 100)
        

    def parseNodes(self, pnodes):
        rest = []
        for pnode in pnodes:
            if pnode.key == 'Indexes':
                self.indexes.parse(pnode)
            elif pnode.key == 'Vertices':
                self.vertices.parse(pnode)
            elif pnode.key == 'Normals':
                self.normals.parse(pnode)
            else:
                rest.append(pnode)

        return FbxGeometryBase.parseNodes(self, rest)

    
    def make(self, skey, baseVerts):        
        FbxObject.make(self, skey)
        
        if fbx.usingMakeHuman:
            self.indexes.make(skey.indexes)
            self.vertices.make(skey.vertices)
            #self.indexes.make(skey.normals)
        else:
            nVerts = len(skey.data)
            vectors = [skey.data[vn].co - v.co for vn,v in enumerate(baseVerts)]
            indexes = [vn for vn in range(nVerts) if vectors[vn].length > 1e-4]
            vertices = [vectors[vn] for vn in indexes]
        
            self.indexes.make(indexes)
            self.vertices.make(vertices)
            #self.normals.make( [normals[vn] for vn in indexes] )
        
        return self


    def writeHeader(self, fp):
        FbxObject.writeHeader(self, fp)            
        self.indexes.writeFbx(fp)
        self.vertices.writeFbx(fp)
        #self.normals.writeFbx(fp)


    def build4(self):        
        subdef,_ = self.getBParent('BLEND_CHANNEL_DEFORMER')
        deformer,_ = subdef.getBParent('BLEND_DEFORMER')
        meNode,_ = deformer.getBParent('MESH')
        me = fbx.data[meNode.id]
        obNode,_ = meNode.getBParent('OBJECT')
        ob = fbx.data[obNode.id]
        if not me.shape_keys:
            ob.shape_key_add("Basis")
        skey = ob.shape_key_add(self.name)
        n = 0
        for vn in self.indexes.values:
            dx = self.vertices.values[n]
            n += 1
            skey.data[vn].co += Vector(dx)
  
