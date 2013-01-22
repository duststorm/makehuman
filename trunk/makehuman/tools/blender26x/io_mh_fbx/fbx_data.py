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
from . import fbx_deformer
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
        self.actions = {}
        
        self.astacks = {}
        self.alayers = {}
        #self.anodes = {}
        #self.acurves = {}
        
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
            list(self.actions.values()) +

            list(self.astacks.values()) +
            list(self.alayers.values()) +
            #list(self.anodes.values()) +
            #list(self.acurves.values()) +
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
    if len(pnode.values) > 3:
        channel = pnode.values[3]
    else:
        channel = None
    childNode = fbx.idstruct[childId]
    parNode = fbx.idstruct[parId]
    childNode.makeChannelLink(parNode, channel)
    

def createNode(pnode):
    id,name,subtype = nodeInfo(pnode)
    #print(id,name,subtype,pnode)

    node = None
    if pnode.key == 'Geometry':
        if subtype == 'Mesh':
            node = fbx_mesh.CGeometryMesh(subtype)
        elif subtype == 'Shape':
            node = fbx_mesh.CGeometryShape(subtype)
        elif subtype == 'Nurb':
            node = fbx_nurb.CGeometryNurb(subtype)
        else:
            print(pnode.key, pnode)
            halt
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
            node = fbx_lamp.CLampAttribute()
        elif subtype == "Camera":
            node = fbx_camera.CCameraAttribute()
        elif subtype == "IKEffector":
            node = fbx_camera.CIKEffectorAttribute()
        elif subtype == "FKEffector":
            node = fbx_camera.CFKEffectorAttribute()
        elif subtype == "Camera":
            node = fbx_camera.CCameraAttribute()
        elif subtype == "Camera":
            node = fbx_camera.CCameraAttribute()
    elif pnode.key == 'Pose':            
        node = fbx_armature.CPose()
    elif pnode.key == 'Bone':            
        node = fbx_armature.CBone()
    elif pnode.key == 'Deformer':     
        if subtype == 'Skin':
            node = fbx_deformer.CSkinDeformer()
        elif subtype == 'Cluster':
            node = fbx_deformer.CClusterSubDeformer()        
        elif subtype == 'BlendShape':
            node = fbx_deformer.CBlendShapeDeformer()        
        elif subtype == 'BlendShapeChannel':
            node = fbx_deformer.CBlendShapeChannelSubDeformer()        
        else:
            print("Unknown deformer: %s", pnode.key)
            halt
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
    
    print("Creating nodes")
    
    for node in fbx.nodes.values():
        if node.ftype == "Geometry":
            data = bpy.data.meshes.new(node.name)
        elif node.ftype == "Material":
            data = bpy.data.materials.new(node.name)
        elif node.ftype == "Texture":
            data = bpy.data.textures.new(node.name, type='IMAGE')
        elif node.ftype == "Video":
            continue
            bpy.data.images.new(node.name)
        elif node.ftype == "AnimationStack":
            data = bpy.data.actions.new(node.name)
        elif node.ftype == "AnimationCurve":
            data = bpy.data.fcurves.new(node.name)
        elif node.ftype == "Pose":
            data = node
        elif node.ftype == "NodeAttribute":
            if node.typeflags == "Light":
                data = bpy.data.lamps.new(node.name, type='POINT')
            elif node.typeflags == "Camera":
                data = bpy.data.cameras.new(node.name)
            else:
                #print("Skipped", node)
                continue
        else:
            #print("Skipped", node)
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
                for child,channel in node.children:
                    if child.subtype == node.subtype:
                        data = bpy.data.objects.new(node.name, fbx.data[child.id])
                        scn.objects.link(data)
                        break
                fbx.data[node.id] = data
                    
    print("Building objects")
    for node in fbx.nodes.values():
        node.build1()
    for node in fbx.nodes.values():
        node.build2()
    for node in fbx.nodes.values():
        node.build3()
    for node in fbx.nodes.values():
        node.build4()
    for node in fbx.nodes.values():
        node.build5()               

#------------------------------------------------------------------
#   Activating
#------------------------------------------------------------------

def activateData(datum):
    #print("ACT", datum, isinstance(datum, bpy.types.Armature))

    if datum is None:
        return
        
    elif isinstance(datum, bpy.types.Object):
        if (not fbx.settings.selectedOnly) or datum.select:
            fbx.active.objects[datum.name] = datum        
            activateData(datum.data)

    elif isinstance(datum, bpy.types.Mesh):
        fbx.active.meshes[datum.name] = datum        
        for mat in datum.materials:
            activateData(mat)

    elif isinstance(datum, bpy.types.Armature):
        fbx.active.armatures[datum.name] = datum        

    elif isinstance(datum, bpy.types.Material):
        fbx.active.materials[datum.name] = datum        
        for mtex in datum.texture_slots:
            if mtex:
                tex = mtex.texture
                if tex and tex.type == 'IMAGE':
                    activateData(tex)

    elif isinstance(datum, bpy.types.Texture):
        fbx.active.textures[datum.name] = datum      
        img = datum.image
        if img:
            activateData(img)

    elif isinstance(datum, bpy.types.Image):
        fbx.active.images[datum.name] = datum        

    elif isinstance(datum, bpy.types.Camera):
        fbx.active.cameras[datum.name] = datum        

    elif isinstance(datum, bpy.types.Lamp):
        fbx.active.lamps[datum.name] = datum        

    elif isinstance(datum, bpy.types.Scene):
        if fbx.settings.makeSceneNode:
            fbx.active.scenes[datum.name] = datum         
        for ob in datum.objects:
            activateData(ob)

    if hasattr(datum, "animation_data") and datum.animation_data:
        act = datum.animation_data.action
        if act:
            fbx.active.actions[act.name] = act

#------------------------------------------------------------------
#   Making
#------------------------------------------------------------------

def makeNodes(context):

    fbx.root = RootNode()
    fbx.nodes = NodeStruct()
    fbx.active = NodeStruct()
    
    # First pass: activate
    
    activateData(context.scene)
    
    # Second pass: create nodes
    
    for ob in fbx.active.objects.values():
        if ob.type == 'MESH':
            fbx.nodes.meshes[ob.data.name] = fbx_mesh.CGeometryMesh()
        elif ob.type == 'ARMATURE':
            fbx.nodes.armatures[ob.data.name] = fbx_armature.CArmature()
        elif ob.type == 'LAMP':
            fbx.nodes.lamps[ob.data.name] = fbx_lamp.CLampAttribute()
        elif ob.type == 'CAMERA':
            fbx.nodes.cameras[ob.data.name] = fbx_camera.CCameraAttribute()
        #elif ob.type == 'EMPTY':
        #    pass
        else:
            print("Unrecognized object", ob)
            halt
            continue
        fbx.nodes.objects[ob.name] = fbx_object.CObject(ob.type)
        
    for mat in fbx.active.materials.values():
        fbx.nodes.materials[mat.name] = fbx_material.CMaterial()

    for tex in fbx.active.textures.values():
        if tex.type == 'IMAGE':
            fbx.nodes.textures[tex.name] = fbx_texture.CTexture()

    for img in fbx.active.images.values():
        fbx.nodes.images[img.name] = fbx_image.CImage()

    for scn in fbx.active.scenes.values():
        fbx.nodes.scenes[scn.name] = fbx_scene.CScene()
        
    for act in fbx.active.actions.values():        
        fbx.nodes.astacks[act.name] = fbx_anim.CAnimationStack()

    # Third pass: make the nodes
    
    for act in fbx.active.actions.values():        
        fbx.nodes.astacks[act.name].make(act)
            
    for ob in fbx.active.objects.values():
        if ob.type == 'MESH':
            node = fbx.nodes.meshes[ob.data.name]
            node.make(ob)
            fbx.nodes.objects[ob.name].make(ob)
            rig = ob.parent
            if rig and rig.type == 'ARMATURE':
                fbx.nodes.armatures[rig.data.name].addDeformer(node, ob)             

    for ob in fbx.active.objects.values():
        if ob.type == 'ARMATURE':
            amt = fbx.nodes.armatures[ob.data.name]
            amt.make(ob)
            fbx.nodes.objects[ob.name].make(ob)

    for ob in fbx.active.objects.values():
        if ob.type == 'LAMP':
            fbx.nodes.lamps[ob.data.name].make(ob)
        elif ob.type == 'CAMERA':
            fbx.nodes.cameras[ob.data.name].make(ob)
        elif ob.type == 'EMPTY':
            pass
        else:
            continue
        fbx.nodes.objects[ob.name].make(ob)
            
    for mat in fbx.active.materials.values():
        fbx.nodes.materials[mat.name].make(mat)

    for tex in fbx.active.textures.values():
        if tex.type == 'IMAGE':
            fbx.nodes.textures[tex.name].make(tex)

    for img in fbx.active.images.values():
        fbx.nodes.images[img.name].make(img)

    for scn in fbx.active.scenes.values():
        fbx.nodes.scenes[scn.name].make(scn)
       

    # Fourth pass: link actions
    """
    nodes = fbx.nodes.getAllNodes()
    for node in nodes:
        
        if node.datum and node.datum.animation_data:
            act = node.data.animation_data.action
            if act:
                fbx.nodes.astacks[act.name].makeLink(node)
    """            

def makeTakes(context):

    fbx.takes = {}
    
    for act in fbx.active.actions.values():   
        fbx.takes[act.name] = fbx_anim.CTake().make(context.scene, act)
    

