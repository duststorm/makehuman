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
#   Take
#------------------------------------------------------------------

class CTake(CFbx):

    def __init__(self):
        CFbx.__init__(self, "Take")
        self.name = "Take 001"
        self.filename = "Take_001.tak"
        self.localTime = (float2int(1), float2int(100))
        self.referenceTime = (float2int(1), float2int(100))


    def make(self, scn, act):
        self.name = act.name
        self.filename = act.name.replace(" ","_") + ".tak"
        begin = float2int(scn.frame_start)
        end = float2int(scn.frame_end)
        self.localTime = (begin,end)
        self.referenceTime = (begin,end)
        return self
        
        
    def writeProps(self, fp):
        return
        
    def writeTake(self, fp):
        fp.write(
            '    Take: "%s" {\n' % self.name +
            '        FileName: "%s"\n' % self.filename +
            '        LocalTime: %d,%d\n' % tuple(self.localTime) +
            '        ReferenceTime: %d,%d\n' % tuple(self.referenceTime)  +
            '    }\n')
        
        
        
#------------------------------------------------------------------
#   AnimationStack
#------------------------------------------------------------------

class CAnimationStack(CConnection):
    propertyTemplate = (
"""
        PropertyTemplate: "FbxAnimStack" {
            Properties70:  {
                P: "Description", "KString", "", "", ""
                P: "LocalStart", "KTime", "Time", "",0
                P: "LocalStop", "KTime", "Time", "",0
                P: "ReferenceStart", "KTime", "Time", "",0
                P: "ReferenceStop", "KTime", "Time", "",0
            }
        }
""")

    def __init__(self, subtype=''):
        CConnection.__init__(self, 'AnimationStack', subtype, 'ANIMATION')
        self.action = None
        self.alayers = []
                

    def activate(self):
        self.active = True
        for alayer in self.alayers:
            alayer.activate()
            
    
    def make(self, act):        
        CConnection.make(self, act)
        self.name = act.name
        self.active = True
        self.action = act        
        alayer = CAnimationLayer().make(act)
        fbx.nodes.alayers[act.name] = alayer
        print(alayer, alayer.links)
        alayer.makeLink(self)
        print("  ", alayer.links)
        self.alayers.append(alayer)
        return self
                                

    def addDefinition(self, definitions):            
        CConnection.addDefinition(self, definitions)            
        for alayer in self.alayers:
            alayer.addDefinition(definitions)


    def writeHeader(self, fp):
        for alayer in self.alayers:
            alayer.writeProps(fp)
        CConnection.writeHeader(self, fp)   

    """
    def writeLinks(self, fp):
        take = fbx.takes[self.name]
        #self.writeLink(fp, take)
        for alayer in self.alayers:
            alayer.writeLink(fp, self)
    """        

    def build(self):
        for alayer in self.alayers:
            self.action = alayer.build()
        return self.action

#------------------------------------------------------------------
#   AnimationLayer
#------------------------------------------------------------------

class CAnimationLayer(CConnection):
    propertyTemplate = (
"""
        PropertyTemplate: "FbxAnimLayer" {
            Properties70:  {
                P: "Weight", "Number", "", "A",100
                P: "Mute", "bool", "", "",0
                P: "Solo", "bool", "", "",0
                P: "Lock", "bool", "", "",0
                P: "Color", "ColorRGB", "Color", "",0.8,0.8,0.8
                P: "BlendMode", "enum", "", "",0
                P: "RotationAccumulationMode", "enum", "", "",0
                P: "ScaleAccumulationMode", "enum", "", "",0
                P: "BlendModeBypass", "ULongLong", "", "",0
            }
        }
""")

    def __init__(self, subtype=''):
        CConnection.__init__(self, 'AnimationLayer', subtype, 'ACTION')
        self.groups = {}
        self.acnodes = {}
                
    
    def activate(self):
        self.active = True
        for acnode in self.acnodes.values():
            acnode.activate()
            
            
    def make(self, act):        
        CConnection.make(self, act)
        groups = groupFcurves(act)            
        for key,group in groups.items():
            acnode = self.acnodes[key] = CAnimationCurveNode().make(group)
            acnode.makeLink(self)
        return self
                                

    def addDefinition(self, definitions):            
        CConnection.addDefinition(self, definitions)            
        for acnode in self.acnodes.values():
            acnode.addDefinition(definitions)


    def writeHeader(self, fp):
        for acnode in self.acnodes.values():
            acnode.writeProps(fp)
        CConnection.writeHeader(self, fp)            


    def writeLinks(self, fp):
        CConnection.writeLinks(self, fp)
        for acnode in self.acnodes.values():
            acnode.writeLink(fp, self, "OP",  ", " + acnode.name)
            

    def build(self):
        act = bpy.data.actions.new(self.name)
        for acnode in self.acnodes.values():
            key,group = acnode.build()
            self.groups[key] = group
            for fcu in group.fcurves.values():
                act.fcurves.append(fcu)
        return act

#------------------------------------------------------------------
#   F-curve group
#------------------------------------------------------------------

class FCurveGroup():

    def __init__(self, name):
        self.name = name
        self.type = fcurveName(name)
        self.fcurves = {}                


def fcurveType(fcu):
    return fcu.data_path.split('.')[-1].lower()
    

def fcurveName(datapath):
    words = datapath.split('"')
    if len(words) == 1:
        return words[0]
    else:
        return words[1]

    
def groupFcurves(act):        
    groups = {}
    for fcu in act.fcurves:
        print("GG", fcu.data_path, fcu.array_index)
        name = fcu.data_path
        try:
            group = groups[name]
        except KeyError:
            group = groups[name] = FCurveGroup(name)
        group.fcurves[fcu.array_index] = fcu
    return groups    
  

#------------------------------------------------------------------
#   AnimationCurveNode
#   Corresponds to a group of F-curves in Blender
#------------------------------------------------------------------

Channels = {
    'location' : ('T', 'Vector3'),
    'rotation_quaternion' : ('R', 'Vector3'), 
    'rotation_euler' : ('R', 'Vector3'), 
    'scale' : ('S', 'Vector3'),
}

XYZ = [ 'X', 'Y', 'Z' ]    

class CAnimationCurveNode(CConnection):
    propertyTemplate = (
"""
        PropertyTemplate: "FbxAnimCurveNode" {
            Properties70:  {
                P: "d", "Compound", "", ""
            }
        }
""")

    def __init__(self, subtype=''):
        CConnection.__init__(self, 'AnimationCurveNode', 'FCURVES', subtype)
        self.acurves = {}


    def activate(self):
        self.active = True
        for acu in self.acurves.values():
            acu.activate()
            
            
    def make(self, group):        
        CConnection.make(self, group)
        self.name, self.proptype = Channels[self.name]
        self.group = group
        for index,fcu in group.fcurves.items():
            acu = self.acurves[index] = CAnimationCurve().make(fcu)
            acu.makeLink(self)
            
        if self.proptype == 'Vector3':
            props = []
            for index in self.acurves.keys():
                props.append( CNumber().make("d|"+XYZ[index], 0, "A") )
        else:
            halt            
        self.properties = CProperties70().make(props)        

        return self
                                

    def addDefinition(self, definitions):            
        CConnection.addDefinition(self, definitions)            
        for acu in self.acurves.values():
            acu.addDefinition(definitions)


    def writeHeader(self, fp):
        for index,acu in self.acurves.items():
            acu.writeProps(fp)        
        CConnection.writeHeader(self, fp)            


    def writeLink(self, fp, node, oo, extra):
        CConnection.writeLink(self, fp, node, oo, extra)
        print("L", self.acurves.items())
        for index,acu in self.acurves.items():
            acu.writeLink(fp, self, "OP", ", d|"+XYZ[index])


    def build(self):
        return None

#------------------------------------------------------------------
#   AnimationCurve
#   Corresponds to a single F-curve in Blender
#------------------------------------------------------------------

# KeyAttrFlags:
TangeantUser =      0x00000008
Cubic =             0x00000040
Linear =            0x00000104
WeightedRight =     0x01000000
WeightedNextLeft =  0x02000000


KeyAttrFlags = {
    "TangeantUser"      : TangeantUser,
    "Cubic"             : Cubic,
    "WeightedRight"     : WeightedRight,
    "WeightedNextLeft"  : WeightedNextLeft,
}


class CAnimationCurve(CConnection):
    propertyTemplate = (
"""
""")

    def __init__(self, subtype=''):
        CConnection.__init__(self, 'AnimationCurve', 'FCURVE', subtype)
        self.name = ""
        self.keyTimes = CArray("KeyTime", float, 1)
        self.keyValsFloat = CArray("KeyValueFloat", float, 1)
        self.keyAttrFlags = CArray("KeyAttrFlags", int, 1)
        self.keyAttrDataFloat = CArray("KeyAttrDataFloat", int, 4)
        self.keyAttrRefCount = CArray("KeyAttrRefCount", int, 1)
        

    def parseNodes(self, pnodes):
        rest = []
        for pnode in pnodes:
            if pnode.key == 'KeyTime':
                self.keyTimes.parse(pnode)
            elif pnode.key == 'KeyValueFloat':
                self.keyValsFloat.parse(pnode)
            elif pnode.key == ';KeyAttrFlags':
                #self.keyAttrFlagsTemplate.parse(pnode)
                pass
            elif pnode.key == 'KeyAttrFlags':
                self.keyAttrFlags.parse(pnode)
                pass
            elif pnode.key == ';KeyAttrDataFloat':
                #self.keyAttrDataFloatTemplate.parse(pnode)
                pass
            elif pnode.key == 'KeyAttrDataFloat':
                self.keyAttrDataFloat.parse(pnode)
                pass
            else:
                rest.append(pnode)

        return CConnection.parseNodes(self, rest)
        
        
    def make(self, fcu):        
        CConnection.make(self, fcu)

        times = []
        values = []
        flags = []
        data = []
        refcounts = []
        
        for kp in fcu.keyframe_points:
            t = float2int(kp.co[0])
            times.append(t)
            y = kp.co[1]
            values.append(y)
            #data += [list(kp.handle_left), list(kp.handle_right)]
            data.append((0,0,0xd050d05,0))
            #flag = Cubic|TangeantUser|WeightedRight|WeightedNextLeft
            flag = Linear
            flags.append(flag)
            refcounts.append(1)

        self.keyTimes.make(times) 
        self.keyValsFloat.make(values)           
        self.keyAttrFlags.make(flags)  
        self.keyAttrDataFloat.make(data)            
        self.keyAttrRefCount.make(refcounts)       
        
        return self
        
                                
    def writeHeader(self, fp):
        CConnection.writeHeader(self, fp)   
        self.keyTimes.writeProps(fp)
        self.keyValsFloat.writeProps(fp)
        self.keyAttrFlags.writeProps(fp)
        self.keyAttrDataFloat.writeProps(fp)
        self.keyAttrRefCount.writeProps(fp)


    def build(self):
        fcu = fbx.data[self.id]
        flags = self.keyAttrFlags
        attrs = self.keyAttrDataFloat
        refcounts = self.keyAttrRefCount

        for n,t in enumerate(self.keyTimes):
            y = self.keyValsFloat[y]
            fcu.keyframe_points.append((t,y))

        return fcu            
            

  
    
    