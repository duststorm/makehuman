#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import math
from math import pi
import aljabr
import warp
import numpy
import gui3d
import warpmodifier
import log

from numpy import dot
from numpy.linalg import inv
import transformations as tm

import export_config
    
import mhx
from mhx import the
from the import *

from . import dual_quaternions

D = pi/180

#
#
#

VISIBLE_LAYERS = L_MAIN|L_UPSPNFK|L_LARMFK|L_LLEGFK|L_RARMFK|L_RLEGFK

ACTIVE_LAYERS = (
    L_MAIN|L_UPSPNFK|L_LARMFK|L_LLEGFK|L_LHANDFK|L_LHANDIK|L_RHANDIK|
    L_RARMFK|L_RLEGFK|L_RHANDFK|L_HEAD|L_LPALM|L_RPALM|
    L_TWEAK|L_HELP|L_MSCL|L_DEF
)

LayerNames = [
    (L_MAIN, "Root"),
    (L_UPSPNFK, "Spine"),
    (L_HEAD, "Head"),
    (L_TWEAK, "Tweak"),

    (L_LARMFK, "Left Arm"),
    (L_LLEGFK, "Left Leg"),
    (L_LPALM, "Left Palm"),
    (L_LHANDIK, "Left Fingers"),
    (L_LHANDFK, "Left Links"),

    (L_RARMFK, "Right Arm"),
    (L_RLEGFK, "Right Leg"),
    (L_RHANDFK, "Right Links"),
    (L_RHANDIK, "Right Fingers"),
    (L_RPALM, "Right Palm"),

    (L_HELP, "Help"),
    (L_MSCL, "Muscles"),
    (L_DEF, "Deform")
]
        
class CArmature:
    def __init__(self, human, config):
        self.name = "Armature"
        self.config = config
        self.human = human
        self.modifier = None
        self.restPosition = False
        self.dirty = True
        self.frames = []
        self.bones = {}
        self.boneList = []
        self.roots = []
        self.controls = []
        self.deforms = []
        if config.rigtype == 'mhx':
            self.visible = VISIBLE_LAYERS
            self.last = 32
        else:
            self.visible = 1
            self.last = 1

        self.matrixGlobal = tm.identity_matrix()
        self.restCoords = None
        self.boneWeights = {}
        if config.vertexWeights:
            self.vertexgroups = config.vertexWeights
        elif config.rigtype == "mhx":
            self.vertexgroups = {}
            for name in ["head", "bones", "palm"]:
                mhx.mhx_main.getVertexGroups(name, self.vertexgroups)                    

    def __repr__(self):
        return ("  <CArmature %s>" % self.name)
        
    def display(self):
        log.debug("<CArmature %s", self.name)
        for bone in self.boneList:
            bone.display()
        log.debug(">")
        

    def printLocs(self, words):
        return
        string = ""
        for word in words:
            string += ("%s " % word)
        log.debug("%s", string)
        verts = self.human.meshData.verts
        for vn in [3825]:
            x = verts[vn].co
            y = self.restCoords[vn]
            log.debug("   %d (%.4f %.4f %.4f) (%.4f %.4f %.4f)", vn, x[0], x[1], x[2], y[0], y[1], y[2])


    def assignDrivers(self, drivers):
        for drv in drivers:
            words = drv.channel.split('"')
            if words[0] == "pose.bones[":
                bone = self.bones[words[1]]
                bone.drivers.append(drv)     
                

    def listPose(self):
        for bone in self.boneList:
            quat = tm.quaternion_from_matrix(bone.matrixPose)
            log.debug("  %s %s", bone.name, quat)


    def clear(self, update=False):
        log.message("Clear armature")
        for bone in self.boneList:
            bone.matrixPose = tm.identity_matrix()
        if update:
            halt
            self.update()     
            self.removeModifier()


    def store(self):
        shadowBones = {}
        for bone in self.boneList:
            shadowBones[bone.name] = bone.matrixPose
            bone.matrixPose = tm.identity_matrix()
        #self.listPose()
        return shadowBones
        
        
    def restore(self, shadowBones):        
        for bone in self.boneList:
            bone.matrixPose = shadowBones[bone.name]
        #self.listPose()


    def adapt(self):
        shadowBones = self.store()
        self.syncRestVerts("adapt")
        self.restore(shadowBones)
        self.update()
        

    def rebuild(self, update=True):   
        log.message("Rebuild %s %s %s", self, update, self.config.rigtype)
        obj = self.human.meshData
        proxyData = {}
        mhx.mhx_rig.setupRig(obj, self.config, proxyData)
        log.debug("RHT %s %s", the.RigHead["Root"], the.RigTail["Root"])
        for bone in self.boneList:
            bone.rebuild()
            if bone.name in []:
                log.debug("%s %s %s", bone.name, bone.head, bone.tail)
                #print "R", bone.matrixRest
                #print "P", bone.matrixPose
                #print "G", bone.matrixGlobal
        if self.modifier:
            self.modifier.updateValue(self.human, 1.0)
        self.syncRestVerts("rebuild")                
        if update:
            self.update()            


    def syncRestVerts(self, caller):
        log.message("Synch rest verts: %s", caller)
        #nVerts = len(self.restVerts)
        self.restCoords[:,:3] = warpmodifier.getWarpedCoords()
        #for n in range(nVerts):
        #    self.restVerts[n].co[:3] = coords[n]
    

    def removeModifier(self):
        if self.modifier:
            self.modifier.updateValue(self.human, 0.0)
            self.modifier = None
            self.human.meshData.update()
            self.syncRestVerts("removeModifier")                
            self.printLocs(["Remove", self.modifier])

        
    def updateModifier(self):
        if self.modifier:
            self.modifier.updateValue(self.human, 1.0)
            self.human.meshData.update()
            self.syncRestVerts("updateModifier")                
            self.printLocs(["Update", self.modifier])

        
    def setModifier(self, modifier):
        self.removeModifier()
        self.modifier = modifier
        self.modifier.updateValue(self.human, 1.0)
        self.syncRestVerts("setModifier")
        self.printLocs(["setModifier", self.modifier])


    def update(self):
        human = self.human
        obj = human.meshData
        self.printLocs(["Update", self])

        for bone in self.boneList:
            bone.updateBone()
            bone.updateConstraints()
        self.printLocs(["Bones updated"])            

        self.updateObj()
        self.printLocs(["Updated", human])

        if human.proxy:
            human.updateProxyMesh()
            
        if human.hairObj and human.hairProxy:            
            mesh = human.hairObj.getSeedMesh()
            human.hairProxy.update(mesh, human.meshData)
            mesh.update()
            if human.hairObj.isSubdivided():
                human.hairObj.getSubdivisionMesh()

        for (name,clo) in human.clothesObjs.items():            
            if clo:
                mesh = clo.getSeedMesh()
                human.clothesProxies[name].update(mesh, human.meshData)
                mesh.update()
                if clo.isSubdivided():
                    clo.getSubdivisionMesh()
        
        
    def updateObj(self):
        obj = self.human.meshData
        nVerts = len(obj.verts)
        coords = numpy.zeros((nVerts,4), float)
        for bname,data in self.boneWeights.items():
            bone = self.bones[bname]
            verts,weights = data
            vec = dot(bone.matrixVerts, self.restCoords[verts].transpose())
            wvec = weights*vec
            coords[verts] += wvec.transpose()

        """   
        for vn in range(nVerts):
            vert = self.restVerts[vn]
            if vert.groups:
                mat = numpy.zeros((4,4), float)
                for bone,w in vert.groups:
                    mat += w*bone.matrixVerts
                coords[vn] = dot(mat,vert.co)[:3] 
            else:
                coords[vn] = vert.co[:3]
        """
        obj.changeCoords(coords[:,:3])
        obj.calcNormals()
        obj.update()


    def build(self):
        if self.config.exporting:
            return
        self.controls = []
        self.deforms = []

        for bone in self.boneList:
            bone.build()
            #print "Roll", bone.name, bone.roll, bone.getRoll()
            if bone.deform:
                self.deforms.append(bone)
            if bone.layers & self.visible:
                self.controls.append(bone)
            

        if not self.boneWeights:
            nVerts = len(warpmodifier.shadowCoords)
            self.restCoords = numpy.zeros((nVerts,4), float)
            self.restCoords[:,3] = 1
            self.syncRestVerts("rest")
            
            wtot = numpy.zeros(nVerts, float)
            for vgroup in self.vertexgroups.values():
                for vn,w in vgroup:
                    wtot[vn] += w

            self.boneWeights = {}
            for bname,vgroup in self.vertexgroups.items():
                weights = numpy.zeros(len(vgroup), float)
                verts = []
                n = 0
                for vn,w in vgroup:
                    verts.append(vn)
                    weights[n] = w/wtot[vn]
                    n += 1
                self.boneWeights[bname] = (verts, weights)
        else:                
            self.syncRestVerts("build")
                
                
    def checkDirty(self):                
        dirty = False
        for bone in self.boneList:
            bone.dirty = False

        for bone in self.boneList:
            bone.dirty = True
            for cns in bone.constraints:
                bnames = []
                try:
                    bnames.append( cns.subtar )
                except AttributeError:
                    pass            
                try:
                    bnames.append( cns.ptar )
                except AttributeError:
                    pass
                for bname in bnames:
                    if bname:
                        target = self.bones[bname]
                        if not target.dirty:
                            log.debug("Dirty %s before %s" % (bone.name, target.name))
                            dirty = True
        if dirty:
            raise NameError("Dirty bones encountered") 
            
            
    def readMhpFile(self, filepath):
        log.message("Mhp %s", filepath)
        fp = open(filepath, "rU")
        for line in fp:
            words = line.split()
            if len(words) < 5:
                continue
            elif words[1] in ["quat", "gquat"]:
                bone = self.bones[words[0]]
                quat = float(words[2]),float(words[3]),float(words[4]),float(words[5])
                mat = tm.quaternion_matrix(quat)
                if words[1] == "gquat":
                    mat = dot(inv(bone.matrixRelative), mat)
                bone.matrixPose[:3,:3] = mat[:3,:3]
        fp.close()
        self.update()                    


    def readBvhFile(self, filepath):
        log.message("Bvh %s", filepath)
        fp = open(filepath, "rU")
        bones = []
        motion = False
        frames = []
        for line in fp:
            words = line.split()
            if len(words) < 1:
                continue
            if motion:
                frame = []
                for word in words:
                    frame.append(float(word))
                frames.append(frame)                
            elif words[0] == "ROOT":
                joint = words[1]
                isRoot = True
            elif words[0] == "JOINT":
                try:
                    bone = self.bones[joint]
                except KeyError:
                    bone = None
                if not bone:
                    raise NameError("Missing bone: %s" % joint)
                data = (bone, offset, channels, isRoot)
                bones.append(data)
                joint = words[1]
                isRoot = False
            elif words[0] == "OFFSET":
                if isRoot:
                    offset = (float(words[1]), float(words[2]), float(words[3]))
                else:
                    offset = (0,0,0)
            elif words[0] == "CHANNELS":
                nchannels = int(words[1])
                channels = words[2:]
            elif words[0] == "Frame":
                try:
                    bone = self.bones[joint]
                except KeyError:
                    bone = None
                data = (bone, offset, channels, isRoot)
                bones.append(data)
                motion = True
        fp.close()

        frame = frames[0]
        for bone, offset, channels, isRoot in bones:
            order = ""
            angles = []
            for channel in channels:
                value = frame[0]
                if channel == "Xposition":
                    rx = value
                elif channel == "Yposition":
                    ry = value
                elif channel == "Zposition":
                    rz = value
                elif channel == "Xrotation":
                    ax = value*D
                    order = "x" + order
                    angles.append(ax)
                elif channel == "Yrotation":
                    ay = -value*D
                    order = "z" + order
                    angles.append(ay)
                elif channel == "Zrotation":
                    az = value*D
                    order = "y" + order
                    angles.append(az)
                frame = frame[1:]
            if bone:
                ak,aj,ai = angles     
                order = "s" + order
                mat1 = tm.euler_matrix(ai, aj, ak, axes=order) 
                mat2 = dot(dot(inv(bone.matrixRest), mat1), bone.matrixRest)
                bone.matrixPose[:3,:3] = mat2[:3,:3]
                if isRoot and False:
                    bone.matrixPose[0,3] = rx
                    bone.matrixPose[1,3] = ry
                    bone.matrixPose[2,3] = rz

            if bone.name in []:
                log.debug("%s %s", bone.name, order)
                log.debug("%s", str(channels))
                log.debug("%s %s %s", ax/D, ay/D, az/D)
                log.debug("R %s", bone.matrixRest)
                log.debug("M1 %s", mat1)
                log.debug("M2 %s", mat2)
                log.debug("P %s", bone.matrixPose)
                log.debug("G %s", bone.matrixGlobal)

        self.update()                    

                
class CBone:
    def __init__(self, amt, name, roll, parent, flags, layers, bbone):
        self.name = name
        self.dirty = False
        self.armature = amt
        self.head = the.RigHead[name]
        self.tail = the.RigTail[name]
        self.roll = roll
        self.length = 0
        self.yvector4 = None
        self.parent = parent
        self.children = []
        if parent:
            self.parent = amt.bones[parent]
            self.parent.children.append(self)
        else:
            self.parent = None
            amt.roots.append(self)
        self.layers = layers
        self.bbone = bbone

        self.conn = (flags & F_CON != 0)
        self.deform = (flags & F_DEF != 0)
        self.restr = (flags & F_RES != 0)
        self.wire = (flags & F_WIR != 0)
        self.lloc = (flags & F_NOLOC == 0)
        self.lock = (flags & F_LOCK != 0)
        self.cyc = (flags & F_NOCYC == 0)
    
        self.location = (0,0,0)
        self.lock_location = (False,False,False)
        self.lock_rotation = (False,False,False)
        self.lock_rotation_w = False
        self.lock_rotations_4d = False
        self.lock_scale = (False,False,False)
        
        self.constraints = []
        self.drivers = []

        # Matrices:
        # matrixRest:       4x4 rest matrix, relative world
        # matrixRelative:   4x4 rest matrix, relative parent 
        # matrixPose:       4x4 pose matrix, relative parent and own rest pose
        # matrixGlobal:     4x4 matrix, relative world
        # matrixVerts:      4x4 matrix, relative world and own rest pose
        
        self.matrixRest = None
        self.matrixRelative = None
        self.matrixPose = None
        self.matrixGlobal = None
        self.matrixVerts = None

            
    def __repr__(self):
        return ("  <CBone %s>" % self.name)
        

    def build(self):
        self.matrixPose = tm.identity_matrix()
        self.build0()
                
    def rebuild(self):
        self.head = the.RigHead[self.name]
        self.tail = the.RigTail[self.name]
        self.build0()

    def build0(self):
        x,y,z = self.head
        self.head3 = numpy.array(self.head)
        self.head4 = numpy.array((x,y,z,1.0))
        x,y,z = self.tail
        self.tail3 = numpy.array(self.tail)
        self.tail4 = numpy.array((x,y,z,1.0))
        self.length, self.matrixRest = getMatrix(self.head3, self.tail3, self.roll)
        self.vector4 = self.tail4 - self.head4
        self.yvector4 = numpy.array((0, self.length, 0, 1))

        if self.parent:
            self.matrixRelative = dot(inv(self.parent.matrixRest), self.matrixRest)
            self.matrixGlobal = dot(self.parent.matrixGlobal, self.matrixRelative)
        else:
            self.matrixRelative = self.matrixRest
            self.matrixGlobal = self.matrixRelative   
        try:
            self.matrixVerts = dot(self.matrixGlobal, inv(self.matrixRest))
        except:
            log.debug("%s %s %s", self.name, self.head, self.tail)
            log.debug("%s", self.matrixRest)
            halt
                       

    def getHead(self):
        return self.matrixGlobal[:3,3]
        
    def getTail(self):
        tail4 = dot(self.matrixGlobal, self.yvector4)
        return tail4[:3]

    def getRoll(self, R):
        #R = self.matrixRest
        qy = R[0,2] - R[2,0];
        qw = R[0,0] + R[1,1] + R[2,2] + 1;

        if qw < 1e-4:
            roll = pi
        else:
            roll = 2*math.atan2(qy, qw);
        return roll
        

    def quatAngles(self, quat):
        qw = quat[0]
        if abs(qw) < 1e-4:
            return (0,0,0)
        else:
            return ( 2*math.atan(quat[1]/qw),
                     2*math.atan(quat[2]/qw),
                     2*math.atan(quat[3]/qw)
                   )
        

    def zeroTransformation(self):
        self.matrixPose = numpy.identity(4, float)

    
    def setRotationIndex(self, index, angle, useQuat):
        if useQuat:
            quat = tm.quaternion_from_matrix(self.matrixPose)
            log.debug("%s", str(quat))
            quat[index] = angle/1000
            log.debug("%s", str(quat))
            normalizeQuaternion(quat)
            log.debug("%s", str(quat))
            self.matrixPose = tm.quaternion_matrix(quat)
            return quat[0]*1000    
        else:
            angle = angle*D
            ax,ay,az = tm.euler_from_matrix(self.matrixPose, axes='sxyz')
            if index == 1:
                ax = angle
            elif index == 2:
                ay = angle
            elif index == 3:
                az = angle
            mat = tm.euler_matrix(ax, ay, az, axes='sxyz')
            self.matrixPose[:3,:3] = mat[:3,:3]
            return 1000.0

    Axes = [
        numpy.array((1,0,0)),
        numpy.array((0,1,0)),
        numpy.array((0,0,1))
    ]

    def rotate(self, angle, axis, rotWorld):
        mat = tm.rotation_matrix(angle*D, CBone.Axes[axis])
        if rotWorld:
            mat = dot(mat, self.matrixGlobal)        
            self.matrixGlobal[:3,:3] = mat[:3,:3]
            self.matrixPose = self.getPoseFromGlobal()
        else:
            mat = dot(mat, self.matrixPose)
            self.matrixPose[:3,:3] = mat[:3,:3]


    def stretchTo(self, goal, doStretch):
        length, self.matrixGlobal = getMatrix(self.getHead(), goal, 0)
        if doStretch:
            factor = length/self.length
            self.matrixGlobal[:3,1] *= factor
        pose = self.getPoseFromGlobal()

        if 0 and self.name in ["DfmKneeBack_L", "DfmLoLeg_L"]:
            log.debug("Stretch %s", self.name)
            log.debug("G %s", goal)
            log.debug("M1 %s", self.matrixGlobal)
            log.debug("P1 %s", pose)

        az,ay,ax = tm.euler_from_matrix(pose, axes='szyx')
        rot = tm.rotation_matrix(-ay + self.roll, CBone.Axes[1])
        self.matrixGlobal[:3,:3] = dot(self.matrixGlobal[:3,:3], rot[:3,:3])
        pose2 = self.getPoseFromGlobal()
        
        if 0 and self.name in ["DfmKneeBack_L", "DfmLoLeg_L"]:
            log.debug("A %s %s %s", ax, ay, az)
            log.debug("R %s", rot)
            log.debug("M2 %s", self.matrixGlobal)
            log.debug("P2 %s", pose)
            log.debug("")


    def poleTargetCorrect(self, head, goal, pole, angle):
        yvec = goal-head
        xvec = pole-head
        xy = dot(xvec, yvec)/dot(yvec,yvec)
        xvec = xvec - xy * yvec
        xlen = math.sqrt(dot(xvec,xvec))
        if xlen > 1e-6:
            xvec = xvec / xlen
            zvec = self.matrixGlobal[:3,2]
            zlen = math.sqrt(dot(zvec,zvec))
            zvec = zvec / zlen
            angle0 = math.asin( dot(xvec,zvec) )
            rot = tm.rotation_matrix(angle - angle0, CBone.Axes[1])
            #m0 = self.matrixGlobal.copy()
            self.matrixGlobal[:3,:3] = dot(self.matrixGlobal[:3,:3], rot[:3,:3])
            
            if 0 and self.name == "DfmUpArm2_L":
                log.debug("")
                log.debug("IK %s", self.name)
                log.debug("X %s", xvec)
                log.debug("Y %s", yvec)
                log.debug("Z %s", zvec)
                log.debug("A0 %s", angle0)
                log.debug("A %s", angle)
                log.debug("R %s", rot)
                log.debug("M0 %s", m0)
                log.debug("M %s", self.matrixGlobal)


    def getPoseFromGlobal(self):
        if self.parent:
            return dot(inv(self.matrixRelative), dot(inv(self.parent.matrixGlobal), self.matrixGlobal))
        else:
            return dot(inv(self.matrixRelative), self.matrixGlobal)
        
    
    def setRotation(self, angles):
        ax,ay,az = angles
        mat = tm.euler_matrix(ax, ay, az, axes='szyx')
        self.matrixPose[:3,:3] = mat[:3,:3]

    def getRotation(self):  
        qw,qx,qy,qz = tm.quaternion_from_matrix(self.matrixPose)
        ax,ay,az = tm.euler_from_matrix(self.matrixPose, axes='sxyz')
        return (1000*qw,1000*qx,1000*qy,1000*qz, ax/D,ay/D,az/D)


    def getPoseQuaternion(self):
        return tm.quaternion_from_matrix(self.matrixPose)
                
    def setPoseQuaternion(self, quat):
        self.matrixPose = tm.quaternion_matrix(quat)
        

    def updateBone(self):
        if self.parent:
            self.matrixGlobal = dot(self.parent.matrixGlobal, dot(self.matrixRelative, self.matrixPose))
        else:
            self.matrixGlobal = dot(self.matrixRelative, self.matrixPose)
        """    
        pquat = tm.quaternion_from_matrix(self.matrixPose)
        gquat = tm.quaternion_from_matrix(self.matrixGlobal)
        print("%s (%.4f %.4f %.4f %.4f) (%.4f %.4f %.4f %.4f)" % (self.name, pquat[0], pquat[1], pquat[2], pquat[3], gquat[0], gquat[1], gquat[2], gquat[3]))
        """

    def updateConstraints(self):
        for cns in self.constraints:
            cns.update(self.armature, self)
        self.matrixVerts = dot(self.matrixGlobal, numpy.linalg.inv(self.matrixRest))
            


    #
    #   Prisms
    #
    
    PrismVectors = {
        'Prism': [
            numpy.array((0, 0, 0, 0)),
            numpy.array((0.14, 0.25, 0, 0)),
            numpy.array((0, 0.25, 0.14, 0)),
            numpy.array((-0.14, 0.25, 0, 0)),
            numpy.array((0, 0.25, -0.14, 0)),
            numpy.array((0, 1, 0, 0)),
        ],
        'Box' : [
            numpy.array((-0.10, 0, -0.10, 0)), 
            numpy.array((-0.10, 0, 0.10, 0)),
            numpy.array((-0.10, 1, -0.10, 0)),
            numpy.array((-0.10, 1, 0.10, 0)),
            numpy.array((0.10, 0, -0.10, 0)),
            numpy.array((0.10, 0, 0.10, 0)),
            numpy.array((0.10, 1, -0.10, 0)),
            numpy.array((0.10, 1, 0.10, 0)),
        ],
        'Cube' : [
            numpy.array((-1, 0, -1, 0)), 
            numpy.array((-1, 0, 1, 0)),
            numpy.array((-1, 1, -1, 0)),
            numpy.array((-1, 1, 1, 0)),
            numpy.array((1, 0, -1, 0)),
            numpy.array((1, 0, 1, 0)),
            numpy.array((1, 1, -1, 0)),
            numpy.array((1, 1, 1, 0)),
        ],
        'Line' : [    
            numpy.array((-0.03, 0, -0.03, 0)),
            numpy.array((-0.03, 0, 0.03, 0)),
            numpy.array((-0.03, 1, -0.03, 0)),
            numpy.array((-0.03, 1, 0.03, 0)),
            numpy.array((0.03, 0, -0.03, 0)),
            numpy.array((0.03, 0, 0.03, 0)),
            numpy.array((0.03, 1, -0.03, 0)),
            numpy.array((0.03, 1, 0.03, 0)),
        ]
    }

    PrismFaces = {
        'Prism': [ (0,1,4,0), (0,4,3,0), (0,4,2,0), (0,2,1,0),
                   (5,4,1,5), (5,1,2,5), (5,2,3,5), (5,3,4,5) ],
        'Box' : [ (0,1,3,2), (4,6,7,5), (0,2,6,4), 
                   (1,5,7,3), (1,0,4,5), (2,3,7,6) ],
        'Line' : [ (0,1,3,2), (4,6,7,5), (0,2,6,4), 
                   (1,5,7,3), (1,0,4,5), (2,3,7,6) ],
    }                   
    
    HeadVec = numpy.array((0,0,0,1))
         
    def prismPoints(self, type):
        if self.armature.restPosition:
            mat = self.matrixRest
            length = self.length
            self.matrixGlobal = mat
            self.yvector4[1] = length
        else:
            mat = self.matrixGlobal
            length = self.yvector4[1]
        vectors = CBone.PrismVectors[type]
        points = []
        for vec in vectors:
            p = dot(mat, (vec*length + CBone.HeadVec))
            points.append(p[:3])
        return points, CBone.PrismFaces[type]

    #
    #   Display
    #
    
    def display(self):
        log.debug("  <CBone %s", self.name)
        log.debug("    head: (%.4g %.4g %.4g)", self.head[0], self.head[1], self.head[2])
        log.debug("    tail: (%.4g %.4g %.4g)", self.tail[0], self.tail[1], self.tail[2])
        log.debug("    roll: %s", self.roll)
        log.debug("    parent: %s", self.parent)
        log.debug("    conn: %s", self.conn)
        log.debug("    deform: %s", self.deform)

        log.debug("    constraints: [")
        for cns in self.constraints:
            cns.display()        
        log.debug("    ]")
        log.debug("    drivers: [")
        for drv in self.drivers:
            drv.display()
        log.debug("    ]")
        log.debug("  >")


    def printMats(self):
        log.debug(self.name)
        log.debug("H4 %s", self.head4)
        log.debug("T4 %s", self.tail4)
        log.debug("RM %s", self.matrixRest)
        log.debug("RV %s", dot(self.matrixRest, self.yvector4))
        log.debug("P %s", self.matrixPose)
        log.debug("Rel %s", self.matrixRelative)
        log.debug("G %s", self.matrixGlobal)
        log.debug("GV %s", dot(self.matrixGlobal, self.yvector4))
            
#
#
#

YUnit = numpy.array((0,1,0))

YZRotation = numpy.array(((1,0,0,0),(0,0,1,0),(0,-1,0,0),(0,0,0,1)))
ZYRotation = numpy.array(((1,0,0,0),(0,0,-1,0),(0,1,0,0),(0,0,0,1)))

def toBlender3(vec):
    return dot(ZYRotation[:3,:3], vec)
    
def fromBlender4(mat):
    return dot(YZRotation, mat)
    
def getMatrix(head, tail, roll):
    vector = toBlender3(tail - head)
    length = math.sqrt(dot(vector, vector))
    vector = vector/length
    yproj = dot(vector, YUnit)
    
    if yproj > 1-1e-6:
        axis = YUnit
        angle = 0
    elif yproj < -1+1e-6:
        axis = YUnit
        angle = pi
    else:
        axis = numpy.cross(YUnit, vector)
        axis = axis / math.sqrt(dot(axis,axis))
        angle = math.acos(yproj)
    mat = tm.rotation_matrix(angle, axis)
    if roll:
        mat = dot(mat, tm.rotation_matrix(roll, YUnit))         
    mat = fromBlender4(mat)
    mat[:3,3] = head
    return length, mat


def normalizeQuaternion(quat):
    r2 = quat[1]*quat[1] + quat[2]*quat[2] + quat[3]*quat[3]
    if r2 > 1:
        r2 = 1
    if quat[0] >= 0:
        sign = 1
    else:
        sign = -1
    quat[0] = sign*math.sqrt(1-r2)
    
    
def checkPoints(vec1, vec2):
    return ((abs(vec1[0]-vec2[0]) < 1e-6) and 
            (abs(vec1[1]-vec2[1]) < 1e-6) and
            (abs(vec1[2]-vec2[2]) < 1e-6))
    

def createRig(human, rigtype):
    config = export_config.exportConfig(human, True)
    config.exporting = False
    config.feetonground = False
    config.rigtype = rigtype

    fp = None
    config.mhx25 = True
    obj = human.meshData
    proxyData = {}
    mhx.mhx_rig.setupRig(obj, config, proxyData)

    amt = CArmature(human, config)
    the.createdArmature = amt
    for (bname, roll, parent, flags, layers, bbone) in config.armatureBones:
        if config.exporting or layers & ACTIVE_LAYERS:
            bone = CBone(amt, bname, roll, parent, flags, layers, bbone)
            amt.boneList.append(bone)        
            amt.bones[bname] = bone
        else:
            pass
            #print "Ignore %s L %x A %x" % (bname, layers, ACTIVE_LAYERS)

    amt.build()        
    
    if rigtype != "mhx":
        return amt

    #setupCircles(fp)

    mhx.mhx_rig.writeControlPoses(fp, config)
    amt.checkDirty()
    return amt

    mhx.mhx_rig.writeAllActions(fp, config)

    drivers = mhx.mhx_rig.writeAllDrivers(fp, config)
    amt.assignDrivers(drivers)
    
    #amt.display()
    return amt
    
    

