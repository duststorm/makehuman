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
import sys
import math
from . import fbx
from .fbx_basic import *

#------------------------------------------------------------------
#   Properties70 nodes
#------------------------------------------------------------------

class CProperties70(CFbx):
    def __init__(self):
        CFbx.__init__(self, "Properties70")
        self.properties = {}
        
    def parse(self, pnode0):    
        global TypedNode
        for pnode in pnode0.values:
            if pnode.key == "P":
                nodeType = TypedNode[pnode.values[1]]
                node = nodeType().parse(pnode)
                self.properties[node.name] = node
        return self                

    def make(self, props):
        if None in props:
            halt
        for node in props:
            self.properties[node.name] = node
        return self
        
    def writeProps(self, fp):
        fp.write('        Properties70:  {\n')
        for prop in self.properties.values():
            prop.writeProp(fp)
        fp.write('        }\n')

    def nodes(self):        
        return self.properties.values()
        
    def getProp(self, name, default):
        try:
            return self.properties[name].value
        except KeyError:
            return default
            
#------------------------------------------------------------------
#   Property node
#------------------------------------------------------------------

class CProperty(CFbx):

    def __init__(self, type, supertype):
        CFbx.__init__(self, type)
        self.value = None
        self.supertype = supertype
        self.a = ""
        
    def parse(self, pnode0):
        values = pnode0.values
        self.name = values[0]
        self.ftype = values[1]
        self.supertype = values[2]
        self.a = values[3]
        if len(values) > 5:
            self.value = values[4:]
        else:
            self.value = values[4]
        return self    

    def make(self, name, value, a=""):
        self.name = name
        self.value = value
        self.a = a
        return self

    def writeProp(self, fp):
        print(self.name, self.ftype, self.supertype, self.a)
        print(self.value)
        fp.write('            P: "%s", "%s", "%s", "%s", %s\n' % (self.name, self.ftype, self.supertype, self.a, self.flatten()))

    def flatten(self):
        return self.value
        
    def build(self):
        return self.value


#------------------------------------------------------------------
#   Property nodes
#------------------------------------------------------------------

class CInt(CProperty):

    def __init__(self):
        CProperty.__init__(self, "int", "Integer")

    
class CBool(CProperty):

    def __init__(self):
        CProperty.__init__(self, "bool", "")

    
class CEnum(CProperty):

    def __init__(self):
        CProperty.__init__(self, "enum", "")

    
class CDouble(CProperty):

    def __init__(self, type="double", supertype="Number"):
        CProperty.__init__(self, type, supertype)


class CNumber(CProperty):

    def __init__(self):
        CProperty.__init__(self, "Number", "")


class CFieldOfView(CProperty):

    def __init__(self):
        CProperty.__init__(self, "FieldOfView", "")

    
class CString(CProperty):

    def __init__(self, type="KString", supertype=""):
        CProperty.__init__(self, type, supertype)

    def flatten(self):
        return '"%s"' % self.value

    
class CVector(CProperty):
    def __init__(self, type="Vector", supertype=""):
        CProperty.__init__(self, type, supertype)

    def flatten(self):
        print(self.value)
        return "%.3g,%.3g,%.3g" % tuple(self.value)
        

class CVector3D(CVector):
    def __init__(self):
        CVector.__init__(self, "Vector3D", "Vector")


class CLclTranslation(CVector):
    def __init__(self):
        CVector.__init__(self, "Lcl Translation", "")


class CLclRotation(CVector):
    def __init__(self):
        CVector.__init__(self, "Lcl Rotation", "")


class CLclScaling(CVector):
    def __init__(self):
        CVector.__init__(self, "Lcl Scaling", "")

    
class CColorRGB(CVector):

    def __init__(self):
        CVector.__init__(self, "ColorRGB", "Color")

   
TypedNode = {
    "ColorRGB" : CColorRGB,
    "Vector3D" : CVector3D,
    "Vector" : CVector,
    "double" : CDouble,
    "int" : CInt,
    "bool" : CBool,
    "enum" : CEnum,
    "KString" : CString,
    "Lcl Translation" : CLclTranslation,
    "Lcl Rotation" : CLclRotation,
    "Lcl Scaling" : CLclScaling,
    "FieldOfView" : CFieldOfView,
}    


#------------------------------------------------------------------
#   Popular property lists
#------------------------------------------------------------------

def transformProps(mat):
    (loc,rot,scale) = mat.decompose()
    euler = tuple(a*D for a in rot.to_euler())
    return [
        CLclTranslation().make("Lcl Translation", loc),
        CLclRotation().make("Lcl Rotation", euler),
        CLclScaling().make("Lcl Scaling", scale),
    ]


def defaultProps():
    return [
        CBool().make("RotationActive", 1),
        CEnum().make("InheritType", 1),
        CVector3D().make("ScalingMax", (0,0,0)),
        CInt().make("DefaultAttributeIndex", 0),
    ]

print("fbx_props imported")

