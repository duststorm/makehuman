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
from mathutils import Vector

from . import fbx
from .fbx_basic import *
from .fbx_props import *
from .fbx_model import *
from . import fbx_mesh
from . import fbx_lamp
from . import fbx_camera
from . import fbx_material


Ftype2Btype = {
    "Mesh" : 'MESH',
    "Light" : 'LAMP',
    "Camera" : 'CAMERA',
}

Btype2Ftype = {
    'MESH' : "Mesh",
    'LAMP' : "Light",
    'CAMERA' : "Camera",
}

class CObject(CModel):

    def __init__(self, subtype):
        try:
            subtype = Btype2Ftype[subtype]
        except KeyError:
            pass
        CModel.__init__(self, subtype, 'OBJECT')
        self.data = None
        self.datanode = None
        self.dataBtype = 'EMPTY'
        self.dataFtype = 'Null'


    def parseNodes(self, pnodes):
        return CModel.parseNodes(self, pnodes)
        

    def make(self, ob):
        CModel.make(self, ob)
        self.data = ob.data
        self.dataBtype = ob.type

        self.setProps([
            ("RotationActive", 1),
            ("InheritType", 1),
            ("ScalingMax", (0,0,0)),
        ])    
        if ob.location.length > 1e-4:
            self.setProp("Lcl Translation", ob.location)
        if Vector(ob.rotation_euler).length > 1e-4:
            self.setProp("Lcl Rotation", ob.rotation_euler)
        #if ob.scale.length > 1e-4:
        #    self.setProp("Lcl Scaling", ob.scale)


        if ob.type == 'MESH':
            self.dataFtype = 'Mesh'
            self.datanode = fbx.nodes.meshes[ob.data.name]                  
            self.setProp("DefaultAttributeIndex", 0)
        elif ob.type == 'ARMATURE':
            self.subtype = self.dataFtype = 'Null'
            self.datanode = fbx.nodes.armatures[ob.data.name]                  
        elif ob.type == 'LAMP':
            self.dataFtype = 'Light'
            self.datanode = fbx.nodes.lamps[ob.data.name]
        elif ob.type == 'CAMERA':
            self.dataFtype = 'Camera'
            self.datanode = fbx.nodes.cameras[ob.data.name]
        elif self.datanode.type == 'EMPTY':
            pass
        else:
            halt
            
        if self.datanode:
            self.datanode.makeLink(self)
            
        if ob.parent:
            parent = fbx.nodes.objects[ob.parent.name]
            self.makeLink(parent)
            
    
    def build3(self):
        ob = fbx.data[self.id]
        if self.properties:
            ob.location = self.getProp("Lcl Translation")
            ob.rotation_euler = self.getProp("Lcl Rotation")
            ob.scale = self.getProp("Lcl Scaling")
        return ob    
                

