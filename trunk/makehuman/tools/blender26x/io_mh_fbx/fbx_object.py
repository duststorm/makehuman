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
        print("Ob", pnodes)
        return CModel.parseNodes(self, pnodes)
        

    def activate(self):
        self.active = True
        if self.dataBtype == 'MESH':
            node = fbx.nodes.meshes[self.data.name]
        elif self.dataBtype == 'ARMATURE':
            return
            node = fbx.nodes.armatures[self.data.name]
        elif self.dataBtype == 'LAMP':
            node = fbx.nodes.lamps[self.data.name]
        elif self.dataBtype == 'CAMERA':
            node = fbx.nodes.cameras[self.data.name]
        elif self.dataBtype == 'EMPTY':
            node = None 
        else:
            print(self, self.dataBtype, self.dataFtype)
            halt
        node.activate()
            
    
    def make(self, ob):
        CModel.make(self, ob)
        self.data = ob.data
        self.dataBtype = ob.type

        if ob.type == 'MESH':
            self.dataFtype = 'Mesh'
            self.datanode = fbx.nodes.meshes[ob.data.name]                  
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
            
        props = [
            CInt().make("DefaultAttributeIndex", 0),
            ] + transformProps(ob.matrix_world)

        self.properties = CProperties70().make(props)

        if self.datanode:
            self.datanode.makeLink(self)
            
    
    def getData(self):
        for child in self.children:
            print("  ", child)
            if child.isObjectData:
                return child.datum
        halt                
        return None
        
    
    def build(self):
        ob = fbx.data[self.id]
        if self.properties:
            print("PROP", self)
            ob.location = self.getProp("Lcl Translation", (0,0,0))
            ob.rotation_euler = self.getProp("Lcl Rotation", (0,0,0))
            ob.scale = self.getProp("Lcl Scaling", (1,1,1))
        return ob    
                

print("fbx_object imported")

