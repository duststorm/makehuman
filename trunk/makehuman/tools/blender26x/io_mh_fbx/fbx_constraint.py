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
#   Constraint
#------------------------------------------------------------------

class CConstraint(CConnection):
    propertyTemplate = (
"""
        PropertyTemplate: "FbxNode" {
            Properties70:  {
            }
        }
""")

    def __init__(self, subtype, btype):
        CConnection.__init__(self, 'Model', subtype, btype)
        self.setMulti([
            ('Version', 232),
            ('Shading', Y),
            ('Culling', "CullingOff"),
        ])
        self.rna = None


    def make(self, cns, bone=None):
        CConnection.make(self, cns)


#------------------------------------------------------------------
#   Look At
#------------------------------------------------------------------

class CLookAttribute(CNodeAttribute):
    propertyTemplate = (
"""    
    PropertyTemplate: "FbxLookAttribute" {
        Properties70:  {
        P: "Look", "enum", "", "",0
        }
    }
""")

    def __init__(self, subtype='Null'):
        CNodeAttribute.__init__(self, subtype, 'BONEATTR', "Null")
        self.template = self.parseTemplate('LookAttribute', CLookAttribute.propertyTemplate)


    def make(self, bone):
        self.bone = bone    
        CNodeAttribute.make(self, bone)
        self.setProps([
            ("Look", 0),
        ])
    
    
#------------------------------------------------------------------
#   IK
#------------------------------------------------------------------

class CIKEffectorAttribute(CNodeAttribute):
    propertyTemplate = (
"""    
    Properties70:  {
        P: "Color", "ColorRGB", "Color", "",1,0.25,0.25
        P: "Look", "enum", "", "",3
        P: "Size", "double", "Number", "",43.4242176923077
        P: "IK Reach Translation", "IK Reach Translation", "", "A",100
        P: "IK Reach Rotation", "IK Reach Rotation", "", "A",100
    }
""")

    def __init__(self, subtype='IKEffector'):
        CNodeAttribute.__init__(self, subtype, 'BONEATTR', "Marker")
        self.template = self.parseTemplate('IKEffectorAttribute', CIKEffectorAttribute.propertyTemplate)


    def make(self, bone):
        self.bone = bone    
        CNodeAttribute.make(self, bone)
        self.setProps([
            ("Color", (1,0.25,0.25)),
            ("Look", 3),
            ("Size", bone.length),
            ("IK Reach Translation", 100),
            ("IK Reach Rotation", 100),
        ])
        self.setMulti([
            ("Version", 232),
            ("Shading", U),
            ("Culling", "CullingOff"),
        ])


    
class CIKEffector(CConstraint):
    propertyTemplate = (
""" 
    Properties70:  {
        P: "RotationActive", "bool", "", "",1
        P: "InheritType", "enum", "", "",1
        P: "ScalingMax", "Vector3D", "Vector", "",0,0,0
        P: "DefaultAttributeIndex", "int", "Integer", "",0
        P: "Lcl Translation", "Lcl Translation", "", "A+",-2.38418579101563e-007,12.4463262557983,-0.0435358583927155
        P: "Lcl Rotation", "Lcl Rotation", "", "A+",3.65929906262582,-4.63946712446924e-008,1.1487226493973e-007
        P: "Lcl Scaling", "Lcl Scaling", "", "A+",1,1,1
        P: "MultiTake", "int", "Integer", "",1
        P: "ManipulationMode", "enum", "", "",0
        P: "ScalingPivotUpdateOffset", "Vector3D", "Vector", "",0,0,0
        P: "SetPreferedAngle", "Action", "", "",0
        P: "PivotsVisibility", "enum", "", "",1
        P: "RotationLimitsVisibility", "bool", "", "",0
        P: "LocalTranslationRefVisibility", "bool", "", "",0
        P: "RotationRefVisibility", "bool", "", "",0
        P: "RotationAxisVisibility", "bool", "", "",0
        P: "ScalingRefVisibility", "bool", "", "",0
        P: "HierarchicalCenterVisibility", "bool", "", "",0
        P: "GeometricCenterVisibility", "bool", "", "",0
        P: "ReferentialSize", "double", "Number", "",12
        P: "DefaultKeyingGroup", "int", "Integer", "",0
        P: "DefaultKeyingGroupEnum", "enum", "", "",0
        P: "Pickable", "bool", "", "",1
        P: "Transformable", "bool", "", "",1
        P: "CullingMode", "enum", "", "",0
        P: "ShowTrajectories", "bool", "", "",0
        P: "LookUI", "enum", "", "",3
        P: "ResLevel", "enum", "", "",0
        P: "Length", "double", "Number", "",200
        P: "IKSync", "bool", "", "",1
        P: "ShowReach", "bool", "", "",1
        P: "pull", "Number", "", "AU",0,0,10000
        P: "stiffness", "Number", "", "AU",0,0,1
        P: "PullOverride", "Bool", "", "AU",0
        P: "ResistOverride", "Bool", "", "AU",0
    }
""")

class CIKEffector(CConstraint):

    def __init__(self, subtype='IKEffector'):
        CConstraint.__init__(self, subtype, 'IK')
        self.template = self.parseTemplate('IKEffector', CIKEffector.propertyTemplate)
        self.attribute = CIKEffectorAttribute()
            

    def make(self, cns, bone=None):
        CConstraint.make(self, cns)
        self.setProps([
        ])
        self.setMulti([
            ("Version", 232),
            ("Shading", U),
            ("Culling", "CullingOff"),
        ])

 

    
#------------------------------------------------------------------
#   FK
#------------------------------------------------------------------

class CFKEffectorAttribute(CNodeAttribute):
    propertyTemplate = (
"""    
    Properties70:  {
        P: "Color", "ColorRGB", "Color", "",1,1,0
        P: "Look", "enum", "", "",9
        P: "Size", "double", "Number", "",10.8560544230769
    }
""")

    def __init__(self, subtype='FKEffector'):
        CNodeAttribute.__init__(self, subtype, 'BONEATTR', "Marker")
        self.template = self.parseTemplate('FKEffectorAttribute', CFKEffectorAttribute.propertyTemplate)


    def make(self, bone):
        self.bone = bone    
        CNodeAttribute.make(self, bone)
        self.setProps([
            ("Color", (1,1,0)),
            ("Look", 9),
            ("Size", bone.length),
        ])


class CFKEffector(CConstraint):
    propertyTemplate = (
""" 
        Properties70:  {
            P: "RotationActive", "bool", "", "",1
            P: "InheritType", "enum", "", "",1
            P: "ScalingMax", "Vector3D", "Vector", "",0,0,0
            P: "DefaultAttributeIndex", "int", "Integer", "",0
            P: "Lcl Translation", "Lcl Translation", "", "A+",3.50746280908254e-007,-1.13542262327789,2.2554818967785
            P: "Lcl Rotation", "Lcl Rotation", "", "A+",7.30690044982444e-006,-1.30020513155814e-007,2.79452068481266e-008
            P: "Lcl Scaling", "Lcl Scaling", "", "A+",0.999999761579218,0.999999761579008,0.999999761579105
            P: "MultiTake", "int", "Integer", "",1
            P: "ManipulationMode", "enum", "", "",0
            P: "ScalingPivotUpdateOffset", "Vector3D", "Vector", "",0,0,0
            P: "SetPreferedAngle", "Action", "", "",0
            P: "PivotsVisibility", "enum", "", "",1
            P: "RotationLimitsVisibility", "bool", "", "",0
            P: "LocalTranslationRefVisibility", "bool", "", "",0
            P: "RotationRefVisibility", "bool", "", "",0
            P: "RotationAxisVisibility", "bool", "", "",0
            P: "ScalingRefVisibility", "bool", "", "",0
            P: "HierarchicalCenterVisibility", "bool", "", "",0
            P: "GeometricCenterVisibility", "bool", "", "",0
            P: "ReferentialSize", "double", "Number", "",12
            P: "DefaultKeyingGroup", "int", "Integer", "",0
            P: "DefaultKeyingGroupEnum", "enum", "", "",0
            P: "Pickable", "bool", "", "",1
            P: "Transformable", "bool", "", "",1
            P: "CullingMode", "enum", "", "",0
            P: "ShowTrajectories", "bool", "", "",0
            P: "LookUI", "enum", "", "",1
            P: "ResLevel", "enum", "", "",0
            P: "Length", "double", "Number", "",200
            P: "IKSync", "bool", "", "",1
            P: "ShowReach", "bool", "", "",1
        }    
""")

    def __init__(self, subtype='FKEffector'):
        CConstraint.__init__(self, subtype, 'FK')
        self.template = self.parseTemplate('FKEffector', CFKEffector.propertyTemplate)
        self.attribute = CFKEffectorAttribute()
            

    def make(self, cns, bone):
        CConstraint.make(self, cns)
        self.setProps([
        ])
        self.setMulti([
            ("Version", 232),
            ("Shading", U),
            ("Culling", "CullingOff"),
        ])
   