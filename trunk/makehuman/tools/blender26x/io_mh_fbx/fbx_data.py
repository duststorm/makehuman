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
from . import fbx_null
from . import fbx_mesh
from . import fbx_armature
from . import fbx_lamp
from . import fbx_camera
from . import fbx_material
from . import fbx_texture
from . import fbx_image
from . import fbx_object
from . import fbx_scene
from . import fbx_anim


class NodeStruct:

    def __init__(self):
        self.meshes = {}
        self.armatures = {}
        self.bones = {}
        self.limbs = {}
        self.lamps = {}
        self.cameras = {}
        self.materials = {}
        self.textures = {}
        self.images = {}
        self.objects = {}
        self.scenes = {}
        self.astacks = {}
        self.alayers = {}
        self.anodes = {}
        self.acurves = {}
        
    def getAllNodes(self):
        return (
            [fbx.root] +
            list(self.images.values()) +
            list(self.textures.values()) +
            list(self.materials.values()) +
            list(self.scenes.values()) +
            list(self.objects.values()) +
            list(self.meshes.values()) +
            list(self.bones.values()) +
            list(self.limbs.values()) +
            list(self.armatures.values()) +
            list(self.lamps.values()) +
            list(self.cameras.values()) +
            list(self.astacks.values()) +
            list(self.alayers.values()) +
            list(self.anodes.values()) +
            list(self.acurves.values()) +
            []
        )
        
        
#------------------------------------------------------------------
#   Parsing
#------------------------------------------------------------------

def parseNodes(pnode):
    fbx.root = RootNode()
    fbx.nodes = {}
    
    for pnode1 in pnode.values:
        if pnode1.key == "Objects":
            pObjectsNode = pnode1
        elif pnode1.key == "Connections":
            pLinksNode = pnode1
        elif pnode1.key == "Takes":
            pTakesNode = pnode1
           

    for pnode2 in pObjectsNode.values:
        createNode(pnode2)
    for pnode2 in pLinksNode.values:
        parseLink(pnode2)
    for pnode2 in pObjectsNode.values:
        parseObjectProperty(pnode2)

        

def parseLink(pnode):
    childId = pnode.values[1]
    parId = pnode.values[2]
    childNode = fbx.idstruct[childId]
    parNode = fbx.idstruct[parId]
    childNode.makeLink(parNode)
    

def createNode(pnode):
    id,name,subtype = nodeInfo(pnode)
    print(id,name,subtype,pnode)

    node = None
    if pnode.key == 'Geometry':
        node = fbx_mesh.CGeometry(subtype)
    elif pnode.key == 'Material':
        node = fbx_material.CMaterial(subtype)
    elif pnode.key == 'Texture':
        node = fbx_texture.CTexture(subtype)
    elif pnode.key == 'Video':
        node = fbx_image.CImage(subtype)
    elif pnode.key == 'Model':
        if subtype in fbx_object.Ftype2Btype:
            node = fbx_object.CObject(subtype)
        elif subtype == "Null":
            node = fbx_null.CNull(subtype)
        elif subtype == "LimbNode":
            node = fbx_armature.CBone(subtype)
        else:
            print(pnode.key, pnode)
            halt
    elif pnode.key == 'NodeAttribute':            
        if subtype == "LimbNode":
            node = fbx_armature.CBoneAttribute()
        elif subtype == "Light":
            node = fbx_lamp.CLamp()
        elif subtype == "Camera":
            node = fbx_camera.CCamera()
    elif pnode.key == 'Pose':            
        node = fbx_armature.CPose()
    elif pnode.key == 'Bone':            
        node = fbx_armature.CBone()
    elif pnode.key == 'Deformer':     
        if subtype == 'Skin':
            node = fbx_armature.CDeformer()
        elif subtype == 'Cluster':
            node = fbx_armature.CSubDeformer()        
    elif pnode.key == 'AnimationStack':   
        node = fbx_anim.CAnimationStack(subtype)
    elif pnode.key == 'AnimationLayer':            
        node = fbx_anim.CAnimationLayer(subtype)
    elif pnode.key == 'AnimationCurveNode':            
        node = fbx_anim.CAnimationCurveNode(subtype)
    elif pnode.key == 'AnimationCurve':            
        node = fbx_anim.CAnimationCurve(subtype)

    if node:
        node.setid(id, name)
        fbx.nodes[node.id] = node
    else:
        print("Unknown node", pnode.key, pnode)
        halt
        


def parseObjectProperty(pnode):
    id,name,subtype = nodeInfo(pnode)
    fbx.nodes[id].parse(pnode)        
    
#------------------------------------------------------------------
#   Building
#------------------------------------------------------------------

    
def buildObjects(context):

    fbx.data = {}
    
    print("Creating")
    
    for node in fbx.nodes.values():
        print("  ", node)
        if node.ftype == "Geometry":
            data = bpy.data.meshes.new(node.name)
        elif node.ftype == "Material":
            data = bpy.data.materials.new(node.name)
        elif node.ftype == "Texture":
            data = bpy.data.textures.new(node.name, type='IMAGE')
        elif node.ftype == "Video":
            #bpy.data.images.new(node.name)
            pass
        elif node.ftype == "Light":
            data = bpy.data.lamps.new(node.name, type='POINT')
        elif node.ftype == "Camera":
            data = bpy.data.cameras.new(node.name)
        elif node.ftype == "AnimationStack":
            data = bpy.data.actions.new(node.name)
        elif node.ftype == "AnimationCurve":
            data = bpy.data.fcurve.new(node.name)
        else:
            continue
            
        fbx.data[node.id] = data
        
    scn = context.scene        
    for node in fbx.nodes.values():
        if node.ftype == "Model":
            if node.subtype == "Null":
                btype = node.getBtype()
                if btype == 'SCENE':
                    if fbx.settings.createNewScenes:
                        scn = bpy.data.scenes.new(node.name)
                    fbx.data[node.id] = scn

    for node in fbx.nodes.values():
        if node.ftype == "Model":
            print("MODEL", node.subtype, node)
            if node.subtype in ["LimbNode"]:
                continue
            elif node.subtype == "Null":
                btype = node.getBtype()
                if btype == 'ARMATURE':
                    amt = bpy.data.armatures.new(node.name)
                    data = bpy.data.objects.new(node.name, amt)
                    scn.objects.link(data)
                    fbx.data[node.id] = data
                elif btype == 'EMPTY':
                    data = bpy.data.objects.new(node.name, None)
                    fbx.data[node.id] = data
            else:
                print("DATA", node, node.children)
                print(fbx.data.items())
                for child in node.children:
                    print("  ", child.subtype, node.subtype)
                    if child.subtype == node.subtype:
                        data = bpy.data.objects.new(node.name, fbx.data[child.id])
                        scn.objects.link(data)
                        print("Hit", data)
                        break
                fbx.data[node.id] = data
                    
    print("Building")
    for node in fbx.nodes.values():
        if node.ftype == "Video":
            print("  ", node.ftype, node.btype)
            node.build()

    for node in fbx.nodes.values():
        if node.ftype != "Video":
            print("  ", node.ftype, node.btype)
            node.build()
        

#------------------------------------------------------------------
#   Making
#------------------------------------------------------------------

def makeNodes():

    fbx.root = RootNode()
    fbx.nodes = NodeStruct()
    
    # First pass: create nodes
    
    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            fbx.nodes.meshes[ob.data.name] = fbx_mesh.CGeometry()
        elif ob.type == 'ARMATURE':
            fbx.nodes.armatures[ob.data.name] = fbx_armature.CArmature()
        elif ob.type == 'LAMP':
            fbx.nodes.lamps[ob.data.name] = fbx_lamp.CLamp()
        elif ob.type == 'CAMERA':
            fbx.nodes.cameras[ob.data.name] = fbx_camera.CCamera()
        #elif ob.type == 'EMPTY':
        #    pass
        else:
            continue
        fbx.nodes.objects[ob.name] = fbx_object.CObject(ob.type)
        
    for mat in bpy.data.materials:
        fbx.nodes.materials[mat.name] = fbx_material.CMaterial()
    for tex in bpy.data.textures:
        if tex.type == 'IMAGE':
            fbx.nodes.textures[tex.name] = fbx_texture.CTexture()
    for img in bpy.data.images:
        fbx.nodes.images[img.name] = fbx_image.CImage()
    for scn in bpy.data.scenes:
        fbx.nodes.scenes[scn.name] = fbx_scene.CScene()
        
    for act in bpy.data.actions:        
        fbx.nodes.astacks[act.name] = fbx_anim.CAnimationStack()

    # Second pass: make the nodes
    
    for act in bpy.data.actions:        
        fbx.nodes.astacks[act.name].make(act)
            
    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            node = fbx.nodes.meshes[ob.data.name]
            node.make(ob)
            fbx.nodes.objects[ob.name].make(ob)
            rig = ob.parent
            if rig and rig.type == 'ARMATURE':
                fbx.nodes.armatures[rig.data.name].addDeformer(node, ob)             

    for ob in bpy.data.objects:
        if ob.type == 'ARMATURE':
            fbx.nodes.armatures[ob.data.name].make(ob)
            fbx.nodes.objects[ob.name].make(ob)

    for ob in bpy.data.objects:
        if ob.type == 'LAMP':
            fbx.nodes.lamps[ob.data.name].make(ob)
        elif ob.type == 'CAMERA':
            fbx.nodes.cameras[ob.data.name].make(ob)
        elif ob.type == 'EMPTY':
            pass
        else:
            continue
        fbx.nodes.objects[ob.name].make(ob)
            
    for mat in bpy.data.materials:
        fbx.nodes.materials[mat.name].make(mat)

    for tex in bpy.data.textures:
        if tex.type == 'IMAGE':
            fbx.nodes.textures[tex.name].make(tex)

    for img in bpy.data.images:
        fbx.nodes.images[img.name].make(img)

    for scn in bpy.data.scenes:
        fbx.nodes.scenes[scn.name].make(scn)
        
    # Third pass: activate
    
    for scn in bpy.data.scenes:
        fbx.nodes.scenes[scn.name].activate()
        
    for act in bpy.data.actions:        
        fbx.nodes.astacks[act.name].activate()


def makeTakes():

    fbx.takes = {}
    
    for act in bpy.data.actions:   
        fbx.takes[act.name] = fbx_anim.CTake().make(bpy.context.scene, act)
    


print("fbx_data imported")

