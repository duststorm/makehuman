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
from math import pi
from mathutils import *
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


def oneOf(mhCase, blenderCase):
    if fbx.usingMakeHuman:
        return mhCase
    else:
        return blenderCase

#------------------------------------------------------------------
#   FbxPlug
#------------------------------------------------------------------

class FbxPlug:

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
        fbx.debug("Unparsed pnode %s" % pnode)
        halt
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
        halt
        return
              
    def writeLinks(self, fp):
        return

    # Build
    
    def build1(self):
        return None
        
    def build2(self):
        return None
        
    def build3(self):
        return None
        
    def build4(self):
        return None
        
    def build5(self):
        return None
        
    # Add definition
    
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

class CArray(FbxPlug):

    def __init__(self, name, type, step):
        FbxPlug.__init__(self, 'ARRAY')
        self.name = name
        self.values = []
        self.subtype = type
        self.step = step
        self.size = 0
        if type == float:
            self.format = '%s%.6g'
        elif type == int:
            self.format = '%s%ld'


    def parse(self, pnode):     
        return self.parseNodes(pnode.values[1:])


    def parseNodes(self, pnodes):
        for pnode in pnodes:
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
                
        return self                
        
    
    def make(self, values):
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
        vec = self.flattenValues(self.values)

        fp.write(
            '            %s: *%d   {\n' % (self.name, self.size) +
            '                a: ')
        c = ''
        for x in vec:
            fp.write(self.format % (c,round(x)))
            c = ','
        fp.write('\n            }\n')

       
def round(x):
    if abs(x) < 1e-5:
        return 0
    else:
        return x

def dist(x,y):
    d = x-y
    return d.length
    
#------------------------------------------------------------------
#   Coordinate system conversion
#------------------------------------------------------------------


def b2fYup(vec):
    return Vector((vec[0], vec[2], -vec[1]))

def f2bYup(vec):
    return Vector((vec[0], -vec[2], vec[1]))
    
def b2fEulerYup(eu):
    return Vector((eu[0], eu[2], -eu[1]))

def f2bEulerYup(eu):
    return Vector((eu[0], -eu[2], eu[1]))
    
def b2fRot4Yup(mat):
    return b2fGlobRot * mat * b2fLocRot
    
def f2bRot4Yup(mat):
    return f2bGlobRot * mat * f2bLocRot
    
  
def b2fZup(vec):
    return vec

def f2bZup(vec):
    return vec

def b2fEulerZup(eu):
    return eu

def f2bEulerZup(eu):
    return eu

def b2fRot4Zup(mat):
    return mat
    
def f2bRot4Zup(mat):
    return mat


# string : (fIndex, bIndex, factor)

BTransIndexYup = {
    "d|X" : (0, 0, 1),
    "d|Y" : (1, 2, -1),
    "d|Z" : (2, 1, 1),
}

BRotIndexYup = {
    "d|X" : (0, 0, 1),
    "d|Y" : (1, 2, -1),
    "d|Z" : (2, 1, 1),
}

# bIndex : (string, fIndex, factor)

FRotChannelYup = {
    0 : ("d|X", 0, 1),
    1 : ("d|Z", 2, 1),
    2 : ("d|Y", 1, -1),
}

FTransChannelYup = {
    0 : ("d|X", 0, 1),
    1 : ("d|Z", 2, 1),
    2 : ("d|Y", 1, -1),
}

BTransIndexZup = {
    "d|X" : (0, 0, 1),
    "d|Y" : (1, 1, 1),
    "d|Z" : (2, 2, 1),
}

BRotIndexZup = {
    "d|X" : (0, 0, 1),
    "d|Y" : (1, 1, 1),
    "d|Z" : (2, 2, 1),
}

FRotChannelZup = {
    0 : ("d|X", 0, 1),
    1 : ("d|Y", 1, 1),
    2 : ("d|Z", 2, 1),
}

FTransChannelZup = {
    0 : ("d|X", 0, 1),
    1 : ("d|Y", 1, 1),
    2 : ("d|Z", 2, 1),
}


def setCsysChangers():
    global b2f, f2b, b2fEuler, f2bEuler, b2fRot4, f2bRot4 
    global f2bGlobRot, b2fGlobRot, f2bLocRot, b2fLocRot
    global BTransIndex, BRotIndex, FRotChannel, FTransChannel
   
    if fbx.settings.yUp:
        f2bGlobRot = Matrix.Rotation(pi/2, 4, 'X')
        b2fGlobRot = Matrix.Rotation(-pi/2, 4, 'X')
        f2bLocRot = Matrix.Rotation(0, 4, 'Z')
        b2fLocRot = Matrix.Rotation(0, 4, 'Z')

        b2f = b2fYup
        f2b = f2bYup
        b2fEuler = b2fEulerYup
        f2bEuler = f2bEulerYup
        b2fRot4 = b2fRot4Yup
        f2bRot4 = f2bRot4Yup
        
        BTransIndex = BTransIndexYup
        BRotIndex = BRotIndexYup
        FRotChannel = FRotChannelYup
        FTransChannel = FTransChannelYup
        
    else:
        b2f = b2fZup
        f2b = f2bZup
        b2fEuler = b2fEulerZup
        f2bEuler = f2bEulerZup
        b2fRot4 = b2fRot4Zup
        f2bRot4 = f2bRot4Zup

        BTransIndex = BTransIndexZup
        BRotIndex = BRotIndexZup
        FRotChannel = FRotChannelZup
        FTransChannel = FTransChannelZup
        

setCsysChangers()

#------------------------------------------------------------------
#   Literals
#------------------------------------------------------------------

R = pi/180
D = 180/pi

class FbxLiteral:
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return self.value


T = FbxLiteral("T")            
U = FbxLiteral("U")            
V = FbxLiteral("V")            
W = FbxLiteral("W")            
X = FbxLiteral("X")            
Y = FbxLiteral("Y")            
Z = FbxLiteral("Z")            

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
    #return int(f*0x1000)
    return int(f*1924421094.0)

def int2float(d):
    #return int(f*0x1000)
    return float(d/1924421094.0)


