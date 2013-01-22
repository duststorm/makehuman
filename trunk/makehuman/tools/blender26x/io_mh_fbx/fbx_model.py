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
from . import fbx
from .fbx_basic import *
from .fbx_props import *

#------------------------------------------------------------------
#   Connection node
#------------------------------------------------------------------

Prefix = {
    "Model" : "Model", 
    "Geometry" : "Geometry", 
    "Material" : "Material", 
    "Texture" : "Texture", 
    "Video" : "Video", 
    "AnimationStack" : "AnimStack", 
    "AnimationLayer" : "AnimLayer", 
    "AnimationCurveNode" : "AnimCurveNode", 
    "AnimationCurve" : "AnimCurve", 
    "NodeAttribute" : "NodeAttribute", 
    "Pose" : "Pose", 

    "Null" : None
}
    
Prefix2 = {
    "Deformer" : {
        "Skin" : "Deformer", 
        "Cluster" : "SubDeformer",
        "BlendShape" : "Deformer", 
        "BlendShapeChannel" : "SubDeformer",
    },
}

class CConnection(CFbx):

    def __init__(self, type, subtype, btype):
        CFbx.__init__(self, type)
        self.subtype = subtype
        self.rna = None
        try:
            self.prefix = Prefix[type]
        except KeyError:
            self.prefix = Prefix2[type][subtype]
        self.btype = btype
        self.links = []
        self.children = []
        self.active = False
        self.isObjectData = False
        self.properties = CProperties70()
        self.template = {}
        self.struct = {}


    def __repr__(self):
        return ("<CNode %d %s %s %s %s %s %s>" % (self.id, self.ftype, self.subtype, self.name, self.isModel, self.active, self.btype))

    # Struct        

    def get(self, key):
        try:
            return self.struct[key]
        except KeyError:
            #print("Unrecognized key", key)
            return None
        
    def set(self, key, value):
        self.struct[key] = value
        
    def setMulti(self, list):
        for key,value in list:
            self.struct[key] = value
            
    # Properties

    def setProp(self, key, value):
        self.properties.setProp(key, value, self.template)
        
    def getProp(self, key):
        return self.properties.getProp(key, self.template)
        
    def setProps(self, list):
        for key,value in list:
            self.setProp(key, value)
            
    def parseTemplate(self, ftype, template):
        template = self.properties.parseTemplate(ftype, template)        
        for key,value in template.items():
            self.template[key] = value
        return template            
        
    # Overwrites
    
    def parse(self, pnode):     
        self.parseNodes(pnode.values[3:])
        return self


    def parseNodes(self, pnodes): 
        for pnode in pnodes:
            try:
                elt = self.struct[pnode.key]
            except KeyError:
                elt = None
            
            if elt and isinstance(elt, CFbx):
                elt.parse(pnode)
            elif pnode.key == 'Properties70':
                self.properties.parse(pnode)
            elif len(pnode.values) == 1:
                self.struct[pnode.key] = pnode.values[0]
            elif len(pnode.values) > 1:
                self.struct[pnode.key] = pnode.values  
            else:
                print(pnode)
                pnode.write()
                halt
        return self    


    def make(self, rna):
        CFbx.make(self)
        try:
            self.name = rna.name
        except AttributeError:
            pass

        self.rna = rna
        try:
            adata = rna.animation_data
        except AttributeError:
            adata = None
        if adata:
            act = adata.action
            if act:
                alayer = fbx.nodes.alayers[act.name]
                CConnection.makeLink(alayer, self)
        return self                
        
                
    def makeChannelLink(self, parent, channel):
        if self == parent:
            print("Linking to self", self)
            return
            halt
        self.links.append((parent,channel))
        parent.children.append((self,channel))

        
    def makeLink(self, parent):
        self.makeChannelLink(parent, None)


    def getBParent(self, btype):
        for link in self.links:
            if link[0].btype == btype:
                return link
        return None                
        

    def getFParent(self, ftype):
        for link in self.links:
            if link[0].ftype == ftype:
                return link
        return None                
        

    def getFParent2(self, ftype, subtype):
        for link in self.links:
            if (link[0].ftype == ftype) and (link[0].subtype == subtype):
                return link
        return None                
        
    def getBChildren(self, btype):
        links = []
        for link in self.children:
            if link[0].btype == btype:
                links.append(link)
        return links
                
    def writeHeader(self, fp):
        fp.write('    %s: %d, "%s::%s", "%s" {\n' % (self.ftype, self.id, self.prefix, self.name, self.subtype))

    def writeFooter(self, fp):
        fp.write('    }\n')
        
    def writeProps(self, fp):        
        self.properties.write(fp, self.template)
        
    def writeStruct(self, fp):
        for key,value in self.struct.items():
            if isinstance(value, CFbx):
                value.writeFbx(fp)
            elif isinstance(value, str):
                fp.write('        %s: "%s"\n' % (key,value))
            elif isinstance(value, list) or isinstance(value, tuple):
                fp.write('        %s' % key)
                c = ' '
                for x in value:
                    fp.write('%s %s' % (c,x))
                    c = ','
                fp.write('\n')
            else:
                fp.write('        %s: %s\n' % (key,value))
    

    def writeFbx(self, fp):
        self.writeHeader(fp)
        self.writeProps(fp)
        self.writeStruct(fp)
        self.writeFooter(fp)


    def writeLinks(self, fp):
        if self.links:
            links = self.links
        else:
            links = [(fbx.root, None)]
        for link in links:
            node,channel = link
            if channel:
                self.writeChannelLink(fp, node, channel)
            else:
                self.writeLink(fp, node)
            

    def writeChannelLink(self, fp, node, channel):
        fp.write(
            '    ;%s::%s, %s::%s\n' % (self.prefix, self.name, node.prefix, node.name) +
            '    C: "OP",%d,%d, "%s"\n\n' % (self.id, node.id, channel) )


    def writeLink(self, fp, node):
        fp.write(
            '    ;%s::%s, %s::%s\n' % (self.prefix, self.name, node.prefix, node.name) +
            '    C: "OO",%d,%d\n\n' % (self.id, node.id) )


#------------------------------------------------------------------
#   Root node
#------------------------------------------------------------------

class RootNode(CConnection):

    def __init__(self):
        CConnection.__init__(self, "Model", "", None)
        self.name = "RootNode"
        self.id = 0
        fbx.idstruct[0] = self
        self.active = True
        
    def writeFbx(self, fp):
        return

    def writeLinks(self, fp):
        return

#------------------------------------------------------------------
#   Node Attribute node
#------------------------------------------------------------------

class CNodeAttribute(CConnection):

    def __init__(self, subtype, btype, typeflags=None):
        CConnection.__init__(self, 'NodeAttribute', subtype, btype)
        if typeflags:
            self.struct['TypeFlags'] = typeflags


    def parseNodes(self, pnodes):
        for pnode in pnodes:
            if pnode.key == 'Properties70':
                self.properties.parse(pnode)
            elif pnode.key == 'TypeFlags':
                self.typeflags = pnode.values[0]
        return self    

                    
            
#------------------------------------------------------------------
#   Model node
#------------------------------------------------------------------

class CModel(CConnection):
    propertyTemplate = (
"""
        PropertyTemplate: "FbxNode" {
            Properties70:  {
                P: "QuaternionInterpolate", "enum", "", "",0
                P: "RotationOffset", "Vector3D", "Vector", "",0,0,0
                P: "RotationPivot", "Vector3D", "Vector", "",0,0,0
                P: "ScalingOffset", "Vector3D", "Vector", "",0,0,0
                P: "ScalingPivot", "Vector3D", "Vector", "",0,0,0
                P: "TranslationActive", "bool", "", "",0
                P: "TranslationMin", "Vector3D", "Vector", "",0,0,0
                P: "TranslationMax", "Vector3D", "Vector", "",0,0,0
                P: "TranslationMinX", "bool", "", "",0
                P: "TranslationMinY", "bool", "", "",0
                P: "TranslationMinZ", "bool", "", "",0
                P: "TranslationMaxX", "bool", "", "",0
                P: "TranslationMaxY", "bool", "", "",0
                P: "TranslationMaxZ", "bool", "", "",0
                P: "RotationOrder", "enum", "", "",0
                P: "RotationSpaceForLimitOnly", "bool", "", "",0
                P: "RotationStiffnessX", "double", "Number", "",0
                P: "RotationStiffnessY", "double", "Number", "",0
                P: "RotationStiffnessZ", "double", "Number", "",0
                P: "AxisLen", "double", "Number", "",10
                P: "PreRotation", "Vector3D", "Vector", "",0,0,0
                P: "PostRotation", "Vector3D", "Vector", "",0,0,0
                P: "RotationActive", "bool", "", "",0
                P: "RotationMin", "Vector3D", "Vector", "",0,0,0
                P: "RotationMax", "Vector3D", "Vector", "",0,0,0
                P: "RotationMinX", "bool", "", "",0
                P: "RotationMinY", "bool", "", "",0
                P: "RotationMinZ", "bool", "", "",0
                P: "RotationMaxX", "bool", "", "",0
                P: "RotationMaxY", "bool", "", "",0
                P: "RotationMaxZ", "bool", "", "",0
                P: "InheritType", "enum", "", "",0
                P: "ScalingActive", "bool", "", "",0
                P: "ScalingMin", "Vector3D", "Vector", "",0,0,0
                P: "ScalingMax", "Vector3D", "Vector", "",1,1,1
                P: "ScalingMinX", "bool", "", "",0
                P: "ScalingMinY", "bool", "", "",0
                P: "ScalingMinZ", "bool", "", "",0
                P: "ScalingMaxX", "bool", "", "",0
                P: "ScalingMaxY", "bool", "", "",0
                P: "ScalingMaxZ", "bool", "", "",0
                P: "GeometricTranslation", "Vector3D", "Vector", "",0,0,0
                P: "GeometricRotation", "Vector3D", "Vector", "",0,0,0
                P: "GeometricScaling", "Vector3D", "Vector", "",1,1,1
                P: "MinDampRangeX", "double", "Number", "",0
                P: "MinDampRangeY", "double", "Number", "",0
                P: "MinDampRangeZ", "double", "Number", "",0
                P: "MaxDampRangeX", "double", "Number", "",0
                P: "MaxDampRangeY", "double", "Number", "",0
                P: "MaxDampRangeZ", "double", "Number", "",0
                P: "MinDampStrengthX", "double", "Number", "",0
                P: "MinDampStrengthY", "double", "Number", "",0
                P: "MinDampStrengthZ", "double", "Number", "",0
                P: "MaxDampStrengthX", "double", "Number", "",0
                P: "MaxDampStrengthY", "double", "Number", "",0
                P: "MaxDampStrengthZ", "double", "Number", "",0
                P: "PreferedAngleX", "double", "Number", "",0
                P: "PreferedAngleY", "double", "Number", "",0
                P: "PreferedAngleZ", "double", "Number", "",0
                P: "LookAtProperty", "object", "", ""
                P: "UpVectorProperty", "object", "", ""
                P: "Show", "bool", "", "",1
                P: "NegativePercentShapeSupport", "bool", "", "",1
                P: "DefaultAttributeIndex", "int", "Integer", "",-1
                P: "Freeze", "bool", "", "",0
                P: "LODBox", "bool", "", "",0
                P: "Lcl Translation", "Lcl Translation", "", "A",0,0,0
                P: "Lcl Rotation", "Lcl Rotation", "", "A",0,0,0
                P: "Lcl Scaling", "Lcl Scaling", "", "A",1,1,1
                P: "Visibility", "Visibility", "", "A",1
                P: "Visibility Inheritance", "Visibility Inheritance", "", "",1
            }
        }
""")

    def __init__(self, subtype, btype):
        CConnection.__init__(self, 'Model', subtype, btype)
        self.template = self.parseTemplate('Model', CModel.propertyTemplate)
        self.setMulti([
            ('Version', 232),
            ('Shading', Y),
            ('Culling', "CullingOff"),
        ])
        self.rna = None


    def parseNodes(self, pnodes):
        for pnode in pnodes:
            if pnode.key == 'Properties70':
                self.properties.parse(pnode)
        return self    

        

