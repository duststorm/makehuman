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
from mathutils import *

from . import fbx
from .fbx_basic import *
from .fbx_props import *
from .fbx_model import *

#------------------------------------------------------------------
#   Take
#------------------------------------------------------------------

class FbxTake(FbxStuff):

    def __init__(self):
        FbxStuff.__init__(self, "Take")
        self.name = "Take 001"
        frameStart = float2int(1)
        frameEnd = float2int(100)
        self.setMulti([
            ("FileName", self.name),
            ("LocalTime", (frameStart, frameEnd)),
            ("ReferenceTime", (frameStart, frameEnd)),
        ])


    def parse(self, pnode):
        self.name = pnode.values[0]
        return self.parseNodes(pnode.values[1:])
        
        
    def make(self, scn, name):
        self.name = name.replace(" ","_")
        frameStart = float2int(scn.frame_start)
        frameEnd = float2int(scn.frame_end)
        self.setMulti([
            ("FileName", self.name + ".tak"),
            ("LocalTime", (frameStart, frameEnd)),
            ("ReferenceTime", (frameStart, frameEnd)),
        ])
        return self


    def writeHeader(self, fp):
        fp.write('    Take: "%s" {\n' % self.name)
    

    def build(self):
        if fbx.settings.createNewScenes:
            name = self.name.split(".")[0]
            scn = bpy.data.scenes.new(name)
            bpy.context.scene = scn
        else:
            scn = bpy.context.scene
        
        frameStart, frameEnd = self.get("LocalTime")
        scn.frame_start = int2float(frameStart)
        scn.frame_end = int2float(frameEnd)
        
        
#------------------------------------------------------------------
#   AnimationStack
#------------------------------------------------------------------

class CAnimationStack(FbxObject):
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
        FbxObject.__init__(self, 'AnimationStack', subtype, 'ANIMATION')
        self.template = self.parseTemplate('AnimationStack', CAnimationStack.propertyTemplate)
        self.name = "Take 001"
                

    def make(self, act):        
        FbxObject.make(self, act)
        return self
        

    def writeLinks(self, fp):
        return
                         
                         
#------------------------------------------------------------------
#   AnimationLayer
#------------------------------------------------------------------

class CAnimationLayer(FbxObject):
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
        FbxObject.__init__(self, 'AnimationLayer', subtype, 'ACTION')
        self.template = self.parseTemplate('AnimationLayer', CAnimationLayer.propertyTemplate)
        self.name = "Layer0"
        self.groups = {}
        self.acnodes = {}
        self.users = []
                
    
    def make(self, act):        
        FbxObject.make(self, act)
        groups = groupFcurves(act)            
        for key,group in groups.items():
            acnode = self.acnodes[key] = FbxAnimationCurveNode().make(group)
            acnode.makeLink(self)
            for user in self.users:
                if group.pose:
                    if user.btype == 'ARMATURE':
                        boneNode = user.bones[group.bone]
                        acnode.makeChannelLink(boneNode, acnode.channel)
                else:
                    acnode.makeChannelLink(user, acnode.channel)
        return self
                                

    def addDefinition(self, definitions):            
        FbxObject.addDefinition(self, definitions)            
        for acnode in self.acnodes.values():
            acnode.addDefinition(definitions)


    def writeFooter(self, fp):
        FbxObject.writeFooter(self, fp)            
        for acnode in self.acnodes.values():
            acnode.writeFbx(fp)


    def writeLinks(self, fp):
        FbxObject.writeLinks(self, fp)
        for acnode in self.acnodes.values():
            acnode.writeLinks(fp)


    def build4(self):
        for acnode,_ in self.children:
            if acnode.ftype == 'AnimationCurveNode':
                acnode.build()

#------------------------------------------------------------------
#   F-curve group
#------------------------------------------------------------------

class FCurveGroup():

    def __init__(self, datapath):
        self.name = datapath
        words = datapath.split('.')
        self.channel = words[-1].lower()
        self.pose = (words[0] == "pose")
        if self.pose:
            words = datapath.split('"')
            self.bone = words[1]
        else:
            self.bone = None
        self.fcurves = {}                

    def __repr__(self):
        return ("<FCurveGroup %p\n   c %s p %s b %s>" % 
                    (self.datapath, self.channel, self.pose, self.bone))
                    
    
def groupFcurves(act):        
    groups = {}
    for fcu in act.fcurves:
        try:
            group = groups[fcu.data_path]
        except KeyError:
            group = groups[fcu.data_path] = FCurveGroup(fcu.data_path)
        group.fcurves[fcu.array_index] = fcu
    return groups    
  
  
def getDataPath(channel, btype, rna):
    datapaths = {
        'Lcl Translation' : 'location',
        'Lcl Rotation' : 'rotation_euler',
        #'Lcl Rotation' : 'rotation_quaternion',
        'Lcl Scaling' : 'scale'
    }
    bchannel = datapaths[channel]
    if btype == 'BONE':
        return bchannel,('pose.bones["%s"].%s' % (rna.name, bchannel))
    elif btype == 'OBJECT':
        return bchannel,bchannel
    else:
        fbx.debug("getDataPath %s %s %s" % (channel, btype, rna))
        halt

#------------------------------------------------------------------
#   AnimationCurveNode
#   Corresponds to a group of F-curves in Blender
#------------------------------------------------------------------

Channels = {
    'location' : ('T', 'Lcl Translation', 'Vector3', (0,0,0)),
    'rotation_quaternion' : ('R', 'Lcl Rotation', 'Vector3', (0,0,0)), 
    'rotation_euler' : ('R', 'Lcl Rotation', 'Vector3', (0,0,0)), 
    'scale' : ('S', 'Lcl Scaling', 'Vector3', (1,1,1)),
}

XYZ = ['X', 'Y', 'Z']

Index = {
    "d|X" : 0,
    "d|Y" : 1,
    "d|Z" : 2,
}




class FbxAnimationCurveNode(FbxObject):
    propertyTemplate = (
"""
        PropertyTemplate: "FbxAnimCurveNode" {
            Properties70:  {
                P: "d", "Compound", "", "A"
            }
        }
""")

    def __init__(self, subtype=''):
        FbxObject.__init__(self, 'AnimationCurveNode', '', subtype)
        self.template = self.parseTemplate('AnimationCurveNode', FbxAnimationCurveNode.propertyTemplate)
        self.acurves = {}


    def make(self, group):        
        FbxObject.make(self, group)
        channel = self.name.split(".")[-1]
        self.name, self.channel, self.proptype, kvec = Channels[channel]
        self.group = group
        if self.channel in ["Lcl Rotation"]:
            deg = D
        else:
            deg = 1

        if channel == 'rotation_quaternion':
            fcurves = quat2euler(group.fcurves)
        else:
            fcurves = group.fcurves
    
        for index,fcu in fcurves.items():
            acu = self.acurves[index] = FbxAnimationCurve().make(fcu, deg)
            acu.makeChannelLink(self, ("d|%s" % XYZ[index]))

        self.setProps([("d", kvec)])
        return self
                                

    def addDefinition(self, definitions):            
        FbxObject.addDefinition(self, definitions)            
        for acu in self.acurves.values():
            acu.addDefinition(definitions)


    def writeFooter(self, fp):
        FbxObject.writeFooter(self, fp)            
        for index,acu in self.acurves.items():
            acu.writeFbx(fp)        


    def writeLinks(self, fp):
        FbxObject.writeLinks(self, fp)
        for index,acu in self.acurves.items():
            acu.writeLinks(fp)


    def build(self):
        rna = None
        group = None
        for btype in ['BONE', 'OBJECT']:        
            node,channel = self.getBParent(btype)
            if node:
                rna = node.datum
                ob = node.object
                group = rna.name
                break

        if channel in ["Lcl Rotation"]:
            rad = R
        else:
            rad = 1

        
        for child,idx in self.children:       
            index = Index[idx]
            bchannel,datapath = getDataPath(channel, btype, rna)
            ob.keyframe_insert(datapath, index, frame=0, group=group)
            act = ob.animation_data.action
            fcu = getFCurveFromAction(act, datapath, index)
            child.build(fcu, rad)
            

def getFCurveFromAction(act, datapath, index):
    for fcu in act.fcurves:
        if fcu.data_path == datapath and fcu.array_index == index:
            return fcu
    return None

  
#------------------------------------------------------------------
#   Quaternion -> Euler for F-curves
#------------------------------------------------------------------

class FbxFCurve:
    def __init__(self):
        self.keyframe_points = []

        
class KP:
    def __init__(self, t, y):
        self.co = [t,y]
        
        
def quat2euler(fcurves):
    wfcu = fcurves[0]
    xfcu = fcurves[1]
    yfcu = fcurves[2]
    zfcu = fcurves[3]
    times = []
    eulerFCurves = {
        0 : FbxFCurve(),
        1 : FbxFCurve(),
        2 : FbxFCurve(),
    }
    
    for kp in wfcu.keyframe_points:
        t = kp.co[0]
        quat = Quaternion((wfcu.evaluate(t), xfcu.evaluate(t), yfcu.evaluate(t), zfcu.evaluate(t)))
        euler = quat.to_euler('XYZ')
        for n in range(3):
            eulerFCurves[n].keyframe_points.append(KP(t, euler[n]))
        
    return eulerFCurves        
        
#------------------------------------------------------------------
#   AnimationCurve
#   Corresponds to a single F-curve in Blender
#------------------------------------------------------------------

#Cubic|TangeantAuto|GenericTimeIndependent|GenericClampProgressive
#6108

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


class FbxAnimationCurve(FbxObject):

    def __init__(self, subtype=''):
        FbxObject.__init__(self, 'AnimationCurve', '', subtype)
        self.name = ""
        self.setMulti([
            ('Default', 0),
            ('KeyVer', 4008),
            ('KeyTime', CArray("KeyTime", int, 1)),
            ('KeyValueFloat', CArray("KeyValueFloat", float, 1)),
            ('KeyAttrFlags', CArray("KeyAttrFlags", int, 1)),
            ('KeyAttrDataFloat', CArray("KeyAttrDataFloat", int, 4)),
            ('KeyAttrRefCount', CArray("KeyAttrRefCount", int, 1)),
        ])
       
    def make(self, fcu, deg):        

        times = []
        values = []
        flags = []
        data = []
        refcounts = []
        
        for kp in fcu.keyframe_points:
            t = float2int(kp.co[0])
            times.append(t)
            y = kp.co[1]*deg
            values.append(y)
            #data += [list(kp.handle_left), list(kp.handle_right)]
            data.append((0,0,0xd050d05,0))
            #flag = Cubic|TangeantUser|WeightedRight|WeightedNextLeft
            flag = Linear
            flags.append(flag)
            refcounts.append(1)

        self.get('KeyTime').make(times)
        self.get('KeyValueFloat').make(values)
        self.get('KeyAttrFlags').make(flags)
        self.get('KeyAttrDataFloat').make(data)
        self.get('KeyAttrRefCount').make(refcounts)
        
        return FbxObject.make(self, fcu)
        
        
    def build(self, fcu, rad):
        times = self.get('KeyTime')
        yvals = self.get('KeyValueFloat')
        for n,t in enumerate(times.values):
            yval = yvals.values[n]
            fcu.keyframe_points.insert(int2float(t), yval*rad, options={'FAST'})

        return fcu            
            

  
    
    