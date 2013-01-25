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
from .fbx_armature import *
from .fbx_object import *

#------------------------------------------------------------------
#   Constraint
#------------------------------------------------------------------

class FbxConstraint(FbxObject):
    propertyTemplate = (
"""
        PropertyTemplate: "FbxNode" {
            Properties70:  {
            }
        }
""")

    def __init__(self, subtype, btype):
        FbxObject.__init__(self, 'Model', subtype, btype)
        self.setMulti([
            ('Version', 232),
            ('Shading', Y),
            ('Culling', "CullingOff"),
        ])
        self.rna = None


    def make(self, cns, bone=None):
        FbxObject.make(self, cns)


#------------------------------------------------------------------
#   Look At
#------------------------------------------------------------------

class CLookAttribute(FbxNodeAttribute):
    propertyTemplate = (
"""    
    PropertyTemplate: "FbxLookAttribute" {
        Properties70:  {
        P: "Look", "enum", "", "",0
        }
    }
""")

    def __init__(self, subtype='Null'):
        FbxNodeAttribute.__init__(self, subtype, 'BONEATTR', "Null")
        self.template = self.parseTemplate('LookAttribute', CLookAttribute.propertyTemplate)


    def make(self, bone):
        self.bone = bone    
        FbxNodeAttribute.make(self, bone)
        self.setProps([
            ("Look", 0),
        ])
    
    
#------------------------------------------------------------------
#   IK
#------------------------------------------------------------------

class CIKEffectorAttribute(FbxNodeAttribute):
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
        FbxNodeAttribute.__init__(self, subtype, 'BONEATTR', "Marker")
        self.template = self.parseTemplate('IKEffectorAttribute', CIKEffectorAttribute.propertyTemplate)


    def make(self, bone):
        self.bone = bone    
        FbxNodeAttribute.make(self, bone)
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


    
class CIKEffector(FbxConstraint):
    propertyTemplate = (
""" 
    Properties70:  {
        P: "RotationActive", "bool", "", "",1
        P: "InheritType", "enum", "", "",1
        P: "ScalingMax", "Vector3D", "Vector", "",0,0,0
        P: "DefaultAttributeIndex", "int", "Integer", "",0
        P: "Lcl Translation", "Lcl Translation", "", "A+",0,0,0
        P: "Lcl Rotation", "Lcl Rotation", "", "A+",0,0,0
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

class CIKEffector(FbxConstraint):

    def __init__(self, subtype='IKEffector'):
        FbxConstraint.__init__(self, subtype, 'IK')
        self.template = self.parseTemplate('IKEffector', CIKEffector.propertyTemplate)
        self.attribute = CIKEffectorAttribute()
            

    def make(self, cns, bone=None, object=None):
        FbxConstraint.make(self, cns)
        self.attribute.make(cns)
        
        if bone:
            trans,rot,scale = boneTransformations(bone)
        elif object:
            trans,rot,scale = objectTransformations(object)
            
        self.setProps([
            ("RotationActive", 1),
            ("InheritType", 1),
            ("ScalingMax", (0,0,0)),
            ("DefaultAttributeIndex", 0),

            ("Lcl Translation", trans),
            ("Lcl Rotation", rot),
            ("Lcl Scaling", scale)
        ])

        self.setMulti([
            ("Version", 232),
            ("Shading", U),
            ("Culling", "CullingOff"),
        ])

 

    
#------------------------------------------------------------------
#   FK
#------------------------------------------------------------------

class CFKEffectorAttribute(FbxNodeAttribute):
    propertyTemplate = (
"""    
    Properties70:  {
        P: "Color", "ColorRGB", "Color", "",1,1,0
        P: "Look", "enum", "", "",9
        P: "Size", "double", "Number", "",10.8560544230769
    }
""")

    def __init__(self, subtype='FKEffector'):
        FbxNodeAttribute.__init__(self, subtype, 'BONEATTR', "Marker")
        self.template = self.parseTemplate('FKEffectorAttribute', CFKEffectorAttribute.propertyTemplate)


    def make(self, bone):
        self.bone = bone    
        FbxNodeAttribute.make(self, bone)
        self.setProps([
            ("Color", (1,1,0)),
            ("Look", 9),
            ("Size", bone.length),
        ])


class CFKEffector(FbxConstraint):
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
        FbxConstraint.__init__(self, subtype, 'FK')
        self.template = self.parseTemplate('FKEffector', CFKEffector.propertyTemplate)
        self.attribute = CFKEffectorAttribute()
            

    def make(self, cns, bone):
        FbxConstraint.make(self, cns)
        self.setProps([
        ])
        self.setMulti([
            ("Version", 232),
            ("Shading", U),
            ("Culling", "CullingOff"),
        ])
   