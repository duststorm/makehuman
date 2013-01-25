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
    
if usingMakeHuman:

    import log
    from log import message, debug

else:    
    def message(string):
        print(string)

    def debug(string):
        print(string)
    

nodes = {}
data = {}
takes = {}
root = None
idnum = 1000
idstruct = {}
allNodes = {}

templates = {}


class Settings:
    def __init__(self):
        self.createNewScenes = False
        self.writeAllNodes = True
        self.changeCsys = False
        self.includePropertyTemplates = True
        self.makeSceneNode = False
        self.selectedOnly = True
       
            
settings = Settings()


