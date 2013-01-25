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
from .fbx_geometry import *

#------------------------------------------------------------------
#   Nurb geometry
#------------------------------------------------------------------

class FbxNurbs(FbxGeometryBase):
    propertyTemplate = (
"""
""")

    def __init__(self, subtype='Nurb'):
        FbxGeometryBase.__init__(self, subtype, 'CURVE')
        self.template = self.parseTemplate('GeometryNurb', FbxNurbs.propertyTemplate)
        self.isModel = True
        self.isObjectData = True
        self.points = CArray("Points", float, 3, csys=True)
        self.multiplicityU = CArray("MultiplicityU", int, 1)
        self.multiplicityV = CArray("MultiplicityV", int, 1)
        self.knotVectorU = CArray("KnotVectorU", int, 1)
        self.knotVectorV = CArray("KnotVectorV", int, 1)


    def parseNodes(self, pnodes):
        rest = []
        for pnode in pnodes:
            if pnode.key == 'Points':
                self.points.parse(pnode)
            elif pnode.key == 'MultiplicityU':
                self.multiplicityU.parse(pnode)
            elif pnode.key == 'MultiplicityV':
                self.multiplicityV.parse(pnode)
            elif pnode.key == 'KnotVectorU' : 
                self.knotVectorU.parse(pnode)
            elif pnode.key == 'KnotVectorV' : 
                self.knotVectorV.parse(pnode)
            else:
                rest.append(pnode)

        return FbxGeometryBase.parseNodes(self, rest)

    
    def make(self, ob):        
        cu = ob.data
        self.curve = cu
        self.setMulti([
            "NurbVersion", 200,
            "SurfaceDisplay", (4,1,1),
            "NurbOrder", (4,4),
            "Dimensions", (8,11),
            "Step", (1,1),
            "Form", ["Periodic", "Open"],
        ])

        self.points.make( [v.co for v in me.vertices] )
        self.multiplicityU.make( [v.normal for v in me.vertices] )
        self.multiplicityV.make( [v.normal for v in me.vertices] )
        self.knotVectorU.make( [v.normal for v in me.vertices] )
        self.knotVectorU.make( [v.normal for v in me.vertices] )

        return FbxGeometryBase.make(self, cu)
