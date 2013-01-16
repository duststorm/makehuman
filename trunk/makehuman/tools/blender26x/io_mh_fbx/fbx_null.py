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
from . import fbx_scene
from . import fbx_armature


class CNull(CModel):

    def __init__(self, subtype='Null'):
        CModel.__init__(self, subtype, 'NULL')
        self.node = None


    def getBtype(self):
        for child in self.children:
            if child.subtype == 'LimbNode':
                self.node = child
                return 'ARMATURE'

        for child in self.children:
            if child.ftype == 'Model':
                return 'SCENE'

        return 'EMPTY'

        
    def build(self):
        btype = self.getBtype()
        if btype == 'ARMATURE':
            return fbx_armature.CArmature().buildArmature(self)
        elif btype == 'SCENE':
            return fbx_scene.CScene.build(self)
        elif btype == 'EMPTY':
            return fbx.data[self.id]

                

class CEmpty(CModel):

    def __init__(self, subtype='Null'):
        CModel.__init__(self, subtype, 'EMPTY')

    def build(self):
        ob = fbx.data[self.id]
        return ob    
                

print("fbx_object imported")

