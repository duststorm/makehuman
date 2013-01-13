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
from .fbx_object import CObject


#------------------------------------------------------------------
#   Armature
#------------------------------------------------------------------

class CArmature(CConnection):

    def __init__(self, subtype=''):
        CConnection.__init__(self, 'Null', subtype, 'ARMATURE')
        self.pose = None
        self.roots = []
        self.bones = {}
        self.boneList = []
        self.deformers = []
        self.object = None

    def activate(self):
        self.active = True
        
    def make(self, ob):
        CConnection.make(self, ob)
        self.object = fbx.nodes.objects[ob.name]
        for bone in ob.data.bones:
            if bone.parent == None:
                self.roots.append(bone)                
        for root in self.roots:
            self.makeBones(root, self.object)
        if self.pose:
            self.pose.make(ob, self.bones)
        for deformer in self.deformers:
            deformer.make()
        return self            
        
        
    def makeBones(self, bone, parent):
        node = CBone().make(bone, parent)
        self.bones[node.name] = node
        self.boneList.append(node)
        for child in bone.children:
            self.makeBones(child, node)


    def addDeformer(self, node, ob):
        if not self.pose:
            self.pose = CPose()
        self.deformers.append(CDeformer(self, node, ob))
    
    
    def addDefinition(self, definitions):            
        for bone in self.boneList:
            bone.addDefinition(definitions)
        if self.pose:
            self.pose.addDefinition(definitions)
        for deformer in self.deformers:
            print("DD", deformer)
            deformer.addDefinition(definitions)


    def writeProps(self, fp):
        for bone in self.boneList:
            bone.writeProps(fp)
        if self.pose:
            self.pose.writeProps(fp)            
        for deformer in self.deformers:
            deformer.writeProps(fp)

    
    def writeLinks(self, fp):
        #CModel.writeLinks(self, fp)
        #self.pose.writeLinks(fp)
        for bone in self.boneList:
            bone.writeLinks(fp)
        for deformer in self.deformers:
            deformer.writeLinks(fp)
            

    def buildArmature(self, parent):
        print("BA", self, parent)
        ob = fbx.data[parent.id]
        scn = bpy.context.scene
        old = scn.objects.active
        scn.objects.active = ob

        infos = {}
        for root in parent.children:
            BoneInfo(root, infos).collect(root, infos, None)

        bpy.ops.object.mode_set(mode='EDIT')        
        for root in parent.children:
            root.buildBone(infos, ob.data)        
        bpy.ops.object.mode_set(mode='OBJECT')        
        scn.objects.active = old

        return self
    

#------------------------------------------------------------------
#   Pose
#------------------------------------------------------------------

class CPose(CConnection):

    def __init__(self, subtype='BindPose'):
        CConnection.__init__(self, 'Pose', subtype, 'POSE')
        self.poses = []
        fbx.matrices = {}


    def parseNodes(self, pnodes):
        rest = []
        for pnode in pnodes:
            if pnode.key == 'PoseNode':
                self.pose = CPoseNode().parse(pnode)                 
            else:
                rest.append(pnode)

        return CFbx.parseNodes(self, rest)


    def make(self, ob, bones):
        CConnection.make(self, ob)
        node = fbx.nodes.armatures[ob.data.name]
        pose = CPoseNode().make(node, ob.matrix_world)
        self.poses.append(pose)
        self.makeLink(node)
        for bone in ob.data.bones:
            node = bones[bone.name]
            pose = CPoseNode().make(node, bone.matrix_local)
            self.poses.append(pose)
        return self            
        
        
    def writeHeader(self, fp):
        CConnection.writeHeader(self, fp)
        fp.write(
            '        Type: "BindPose"\n' +
            '        Version: 100\n' +
            '        NbPoseNodes: %d\n' % len(self.poses))
        for pose in self.poses:
            pose.writeProps(fp)
                        

    def build(self):
        ob = CObject.build(self)
        scn = bpy.context.scene
        old = scn.objects.active
        scn.objects.active = ob

        bpy.ops.mode_set(mode='EDIT')        
        for bone in self.boneList:
            bone.build()
        for bone in self.boneList:
            for child in bone.children:
                child.datum.parent = bone.datum

        scn.objects.active = old
        return poses

#------------------------------------------------------------------
#   PoseNode
#------------------------------------------------------------------

class CPoseNode(CFbx):

    def __init__(self):
        CFbx.__init__(self, 'PoseNode')
        self.node = None
        self.matrix = None
        
        
    def parseNodes(self, pnodes):
        rest = []
        for pnode in pnodes:
            if pnode.key == 'Node':
                self.node = pnode.values[0]
            elif pnode.key == 'Matrix':
                self.matrix.parse(pnode)
            else:
                rest.append(pnode)

        fbx.matrices[self.node.id] = self.matrix
        return CFbx.parseNodes(self, rest)


    def make(self, node, matrix):
        CFbx.make(self)
        self.node = node
        self.matrix = CArray('PoseNode', float, 4).make(matrix, csys=(True,False))
        fbx.matrices[self.node.id] = self.matrix
        return self
        
        
    def writeProps(self, fp):
        fp.write(
            '        PoseNode:  {\n' +
            '            Node: %d\n' % (self.node.id))
        self.matrix.writeProps(fp)
        fp.write('        }\n')
        
#------------------------------------------------------------------
#   Bone
#------------------------------------------------------------------

class CBoneAttribute(CNodeAttribute):
    def __init__(self, subtype='LimbNode'):
        CNodeAttribute.__init__(self, subtype, 'BONE', "Skeleton")


class CBone(CModel):

    def __init__(self, subtype='LimbNode'):
        CModel.__init__(self, subtype, 'BONE')
        self.attribute = CBoneAttribute()
        self.pose = None
            

    def make(self, bone, parent):
        CModel.make(self, bone)
        self.parent = parent
        if bone.parent:
            mat = bone.parent.matrix_local.inverted() * bone.matrix_local
        else:
            mat = bone.matrix_local
        props = transformProps(mat) + defaultProps()
        self.properties = CProperties70().make(props)
        self.attribute.make(bone, [])
        return self
        

    def addDefinition(self, definitions):            
        CModel.addDefinition(self, definitions)
        self.attribute.addDefinition(definitions)
        

    def writeLinks(self, fp):
        self.writeLink(fp, self.parent)
        self.attribute.writeLink(fp, self)

    
    def writeHeader(self, fp):
        self.attribute.writeProps(fp)
        CModel.writeHeader(self, fp)   

    
    def build(self):            
        print("BB", self)
        return None

       
    def buildBone(self, infos, amt):        
        eb = amt.edit_bones.new(self.name)
        info = infos[self.name]
        eb.head = info.head
        eb.tail = info.tail
        if info.parent:
            eb.parent = amt.edit_bones[info.parent.name]
        #eb.roll = info.roll
        for child in self.children:
            if isinstance(child, CBone):
                child.buildBone(infos, amt)
        return eb


class BoneInfo:
   
    def __init__(self, node, infos):
        self.name = node.name
        infos[self.name] = self
        self.head = None
        self.tail = None
        self.roll = None
        self.parent = None
        self.matrix_local = None
        self.matrix = None
        self.children = []
        
    def __repr__(self):
        return ("<BoneInfo %s>" % self.name)
   
   
    def collect(self, node, infos, parent):   
        trans = Vector(node.getProp("Lcl Translation", (0,0,0)))
        rot = node.getProp("Lcl Rotation", (0,0,0))
        scale = node.getProp("Lcl Scaling", (1,1,1))
        euler = Euler(Vector(rot)*R)        
        quat = euler.to_quaternion()
        rmat = euler.to_matrix()
        self.matrix_local = rmat.to_4x4() * Matrix.Translation(trans)
        if parent:
            self.matrix = self.matrix_local * parent.matrix
        else:
            self.matrix = self.matrix_local
        
        if self.name in ["Root", "Torso", "Arm_L"]:
            print("")        
            print(self)
            print(trans)
            print(rot)
            print(quat)
            print(rmat)
            print(self.matrix_local)
            print(self.matrix)
        
        self.parent = parent
        self.head = Vector( self.matrix.col[3][0:3] )

        sum = Vector((0,0,0))
        nChildren = 0
        for child in node.children:
            if isinstance(child, CBone):
                cinfo = BoneInfo(child, infos).collect(child, infos, self)
                self.children.append(cinfo)
                sum += cinfo.head
                nChildren += 1
                    
        if nChildren > 0:                    
            self.tail = self.head + sum/nChildren
        else:
            self.tail = self.head + Vector( self.matrix.col[1][:3] )

        if abs(quat.w) < 1e-4:
            self.roll = math.pi
        else:
            self.roll = -2*math.atan(quat.y/quat.w)
        
        print(self.name, self.head)
        #print("  ", self.head)
        #print("  ", self.tail)
        return self

     
#------------------------------------------------------------------
#   Deformer
#------------------------------------------------------------------

class CDeformer(CConnection):

    def __init__(self, rigNode, meshNode, ob, subtype=''):
        CConnection.__init__(self, 'Deformer', subtype, 'DEFORMER')
        self.rigNode = rigNode
        self.meshNode = meshNode
        self.object = ob
        print("CD", rigNode, meshNode)
        self.subdeformers = {}
        
        
    def make(self):
        CConnection.make(self, self.rigNode)
        for vg in self.object.vertex_groups:
            try:
                bone = self.rigNode.bones[vg.name].datum
            except KeyError:
                continue
                #bone = None
            subdef = CSubDeformer().make(self.object, vg.index, bone)
            self.subdeformers[vg.index] = subdef
        return self

    
    def addDefinition(self, definitions):     
        CConnection.addDefinition(self, definitions)
        for subdef in self.subdeformers.values():
            print("SD", subdef)
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
            subdef.writeHeader(fp)
        CConnection.writeHeader(self, fp)
        

    def build(self, ob):        
        for subdef in self.subdeformers.values():
            subdef.build(ob)
            
 
 #------------------------------------------------------------------
 #   SubDeformer
 #------------------------------------------------------------------
 
class CSubDeformer(CConnection):
 
    def __init__(self, subtype=''):
         CConnection.__init__(self, 'SubDeformer', subtype, 'DEFORMER')
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


    def make(self, ob, index, bone):
        CConnection.make(self, bone)
        vnums = []
        weights = []
        for v in ob.data.vertices:
            for g in v.groups:
                if g.group == index:
                    vnums.append(v.index)
                    weights.append(g.weight)
        self.indexes.make(vnums)
        self.weights.make(weights)
        mat = bone.matrix_local
        self.transform.make(bone.matrix_local)
        self.transformLink.make(bone.matrix_local)
        return self
         

    def writeHeader(self, fp):
        CConnection.writeHeader(self, fp)
        self.indexes.writeProps(fp)
        self.weights.writeProps(fp)
        self.transform.writeProps(fp)
        self.transformLink.writeProps(fp)
        
        
    def build(self, ob):
        vg = ob.vertex_groups.new(self.name)
        for n,vn in enumerate(self.indexes.values):
            w = self.weights.values[n]
            vg.add([vn], w, 'REPLACE')


print("fbx_armature imported")

