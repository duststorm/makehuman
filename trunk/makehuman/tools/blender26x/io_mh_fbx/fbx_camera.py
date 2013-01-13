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
#   Camera
#------------------------------------------------------------------

class CCamera(CNodeAttribute):

    def __init__(self):
        CNodeAttribute.__init__(self, "Camera", "Camera", 'CAMERA')
        self.isObjectData = True
        self.camera = None

    def make(self, ob):
        self.camera = ob.data
        
        props = [
            CVector().make("InterestPosition", (0,0,-1)),
            CDouble().make("AspectHeight", 180.0),
            CDouble().make("FilmWidth", 1.088000136),
            CDouble().make("FilmAspectRatio", 1.7777),
            CEnum().make("ApertureMode", 1),
            CFieldOfView().make("FieldOfView", 49.13434),
            CDouble().make("NearPlane", 0.1),
            CDouble().make("FarPlane", 100),
            CDouble().make("FocusDistance", 5),
        ]            
        CNodeAttribute.make(self, ob.data, props)
        self.struct["Position"] = (0,0,-50)
        self.struct["Up"] = (0,1,0)
        self.struct["LookAt"] = (0,0,-1)
        self.struct["ShowInfoOnMoving"] =  1
        self.struct["ShowAudio"] =  0
        self.struct["AudioColor"] =  (0,1,0)
        self.struct["CameraOrthoZoom"] =  1
        

    def build(self):
        cam = fbx.data[self.id]
        return cam
