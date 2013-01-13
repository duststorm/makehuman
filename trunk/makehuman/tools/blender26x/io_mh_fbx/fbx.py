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

try:
    bpy.usingMakeHuman
    usingMakeHuman = True
except:
    usingMakeHuman = False
    

nodes = []
data = []
root = None
idnum = 1000
idstruct = {}
allNodes = {}


class Settings:
    def __init__(self):
        self.createNewScenes = False
        self.writeAllNodes = True
        self.changeCsys = False
       

    def getStruct(self):
        return {
            "createNewScenes" : self.createNewScenes,
            "writeAllNodes" : self.writeAllNodes,
            "changeCsys" : self.changeCsys,        
        }
        
    def setStruct(self, struct):
        for key,value in struct.items():
            self.set(key, value)
        
        
    def set(self, key, value):
        if key == "createNewScenes":
            self.createNewScenes = value
        elif key == "writeAllNodes":
            self.writeAllNodes = value
        elif key == "changeCsys":
            self.changeCsys = value
            
settings = Settings()


