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

#------------------------------------------------------------------
#   Material
#------------------------------------------------------------------

class CMaterial(CConnection):
    propertyTemplate = ( 
"""
        PropertyTemplate: "FbxSurfacePhong" {
            Properties70:  {
                P: "ShadingModel", "KString", "", "", "Phong"
                P: "MultiLayer", "bool", "", "",0
                P: "EmissiveColor", "Color", "", "A",0,0,0
                P: "EmissiveFactor", "Number", "", "A",1
                P: "AmbientColor", "Color", "", "A",0.2,0.2,0.2
                P: "AmbientFactor", "Number", "", "A",1
                P: "DiffuseColor", "Color", "", "A",0.8,0.8,0.8
                P: "DiffuseFactor", "Number", "", "A",1
                P: "Bump", "Vector3D", "Vector", "",0,0,0
                P: "NormalMap", "Vector3D", "Vector", "",0,0,0
                P: "BumpFactor", "double", "Number", "",1
                P: "TransparentColor", "Color", "", "A",0,0,0
                P: "TransparencyFactor", "Number", "", "A",0
                P: "DisplacementColor", "ColorRGB", "Color", "",0,0,0
                P: "DisplacementFactor", "double", "Number", "",1
                P: "VectorDisplacementColor", "ColorRGB", "Color", "",0,0,0
                P: "VectorDisplacementFactor", "double", "Number", "",1
                P: "SpecularColor", "Color", "", "A",0.2,0.2,0.2
                P: "SpecularFactor", "Number", "", "A",1
                P: "ShininessExponent", "Number", "", "A",20
                P: "ReflectionColor", "Color", "", "A",0,0,0
                P: "ReflectionFactor", "Number", "", "A",1
            }
        }
""")

    def __init__(self, subtype=''):
        CConnection.__init__(self, 'Material', subtype, 'MATERIAL')        
        self.parseTemplate('Material', CMaterial.propertyTemplate)
        self.isModel = True        
        self.textures = []


    def make(self, mat):
        CConnection.make(self, mat)
        
        for mtex in mat.texture_slots:
            if mtex:
                tex = mtex.texture
                if tex.type == 'IMAGE':
                    self.textures.append(tex)
                    fbx.nodes.textures[tex.name].makeLink(self)

        d = mat.diffuse_intensity
        s = mat.specular_intensity
       
        self.setProps([
            ("ShadingModel", "Phong"),
            ("MultiLayer", 0),
            ("DiffuseColor", mat.diffuse_color),
            ("SpecularColor", mat.specular_color),
            ("DiffuseFactor", mat.diffuse_intensity),
            ("SpecularFactor", mat.specular_intensity),
            ("ShininessExponent", mat.specular_hardness),
            ("TransparencyFactor", mat.alpha),
        ])
    
    
    def build(self):
        mat = fbx.data[self.id]
        mat.diffuse_intensity = 1
        mat.specular_intensity = 1

        for node in self.properties.nodes():
            value = node.build()
            if node.name == "DiffuseColor":
                mat.diffuse_color = value
            elif node.name == "SpecularColor":
                mat.specular_color = value
            elif node.name == "Shininess":
                mat.specular_hardness = value
            elif node.name == "Opacity":
                mat.alpha = value

        texNodes = self.getBChildren('TEXTURE')
        for node in texNodes:
            tex = fbx.data[node.id]
            mtex = mat.texture_slots.add()
            mtex.texture = tex

        return mat
