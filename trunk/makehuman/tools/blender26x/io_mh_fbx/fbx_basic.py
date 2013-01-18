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
import math
import mathutils
import sys
from . import fbx

#------------------------------------------------------------------
#   Fbx Global Variables
#------------------------------------------------------------------


def resetFbx():
    fbx.idnum = 1000
    fbx.idstruct = {}
    fbx.allnodes = {}

    fbx.data = None
    fbx.nodes = None
    fbx.root = None
        
    
resetFbx()    

R = math.pi/180
D = 180/math.pi

class FbxBool:
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        if self.value:
            return "Y"
        else:
            return "N"
            
Y = FbxBool(True)
N = FbxBool(False)


def oneOf(mhCase, blenderCase):
    if fbx.usingMakeHuman:
        return mhCase
    else:
        return blenderCase

#------------------------------------------------------------------
#   CFbx
#------------------------------------------------------------------

class CFbx:

    def __init__(self, ftype):
        self.id = 0
        self.name = None
        self.ftype = ftype
        self.isModel = False

    def setid(self, id, name):
        self.id = id
        self.name = name
        fbx.idstruct[self.id] = self
        return self
        
    def parse(self, pnode):
        return self
        
    def identify(self):
        self.id = fbx.idnum
        fbx.idnum += 16
        return self
        
    def make(self):
        self.identify()        
        
    def __repr__(self):
        return ("<Node %d %s %s %s>" % (self.id, self.ftype, self.name, self.isModel))

    def writeFbx(self, fp):
        return
              
    def writeLinks(self, fp):
        return

    def build(self):
        return None
        
    def addDefinition(self, definitions):        
        try:
            defi = definitions[self.ftype]
        except KeyError:
            defi = None
        if defi is None:
            if fbx.settings.includePropertyTemplates:
                try:
                    template = self.propertyTemplate
                except:
                    template = "\n"
            else:
                template = "\n"
            defi = Definition(template, 0)
        defi.count += 1
        definitions[self.ftype] = defi           

#------------------------------------------------------------------
#   Definition
#------------------------------------------------------------------

class Definition:
    def __init__(self, template, count):
        self.template = template
        self.count = count
        
    def __repr__(self):
        return ("<Definition %d %s>" % (self.count, self.template[:40]))

#------------------------------------------------------------------
#   Array nodes
#------------------------------------------------------------------

class CArray(CFbx):

    def __init__(self, name, type, step, csys=False):
        CFbx.__init__(self, 'ARRAY')
        self.name = name
        self.subtype = type
        self.step = step
        self.size = 0
        self.csys = csys
        if type == float:
            self.format = '%s%.5g'
        elif type == int:
            self.format = '%s%d'


    def parse(self, pnode0):
        for pnode in pnode0.values[1:]:
            if pnode.key == 'a':
                self.size = len(pnode.values)
                if self.step == 1:
                    self.values = pnode.values
                elif self.step > 0:
                    count = int(self.size/self.step)
                    self.values = [pnode.values[self.step*n : self.step*(n+1)] for n in range(count)]
                else:
                    self.values = []
                    rest = pnode.values
                    while rest:
                        val = []
                        self.values.append(val)
                        while rest[0] >= 0:
                            val.append(rest[0])
                            rest = rest[1:]
                        val.append(-1-rest[0])
                        rest = rest[1:]
                
                if self.csys and fbx.settings.changeCsys:
                    self.changeCsys(csysF2B, csysB2F)
                    
        return self                
        
    
    def changeCsys(fcn, inv):                    
        if self.step == 3:
            self.values = [fcn(val) for val in self.values]
        elif self.step == 4:
            (left, right) = self.changeCsys
            if right:
                self.values = [fcn(val) for val in self.values]
            if left:
                self.values = inv(self.values)
                    

    def make(self, values):
        print("ARR", values)
        self.values = values
        self.size = len(self.flattenValues(values))
        return self
            
            
    def flattenValues(self, values):
        if self.step == 1:
            return values
        elif self.step > 0:
            vec = []
            for val in values:
                vec += list(val)
            return vec
        else:
            vec = []
            for val in values:
                vec += val[:-1] + [-1-val[-1]]
            return vec
            

    def unflattenValues(self, vec):
        if self.step == 1:
            return vec
        elif self.step > 0:
            count = self.size/self.step
            return [ vec[n, n+self.step] for n in range(count) ]
        else:
            values = []
            val = []
            for x in values:
                if x >= 0:
                    val.append(x)
                else:
                    val.append(-1-x)
                    values.append(val)
                    val = []
            return values                    


    def writeFbx(self, fp):
        if self.csys and fbx.settings.changeCsys:
            self.changeCsys(csysB2F, csysF2B)
        vec = self.flattenValues(self.values)

        fp.write(
            '            %s: *%d   {\n' % (self.name, self.size) +
            '                a: ')
        c = ''
        for x in vec:
            fp.write(self.format % (c,x))
            c = ','
        fp.write('\n            }\n')
        


#------------------------------------------------------------------
#   Coordinate system conversion
#------------------------------------------------------------------

def csysB2F(vec):
    return (vec[0], vec[2], -vec[1])


def csysF2B(vec):
    return (vec[0], -vec[2], vec[1])

#------------------------------------------------------------------
#   Parsing utilities
#------------------------------------------------------------------

def nodeInfo(pnode):
    id = pnode.values[0]
    name = nameName(pnode.values[1])
    subtype = pnode.values[2]
    return id,name,subtype
    
    
def nodeId(pnode):
    return pnode.values[0]


def nodeFromName(name):
    print("nodefromname", name)
    for node in fbx.nodes.values():
        if node.name == name:
            return node
    return None
    
    
def nameName(string):
    if string is None:
        return None
    else:
        return string.split("::")[1]


def float2int(f):
    return int(f*0x1000)
    #return int(f*1924421094.0)

print("fbx_basic imported")

