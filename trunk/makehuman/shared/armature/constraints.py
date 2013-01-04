""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
Constraints

"""

import math
import numpy
from numpy import dot
from numpy.linalg import inv
import transformations as tm
import log

import mhx
from mhx import the
from the import *

#
#   Master class
#


class CConstraint:
    def __init__(self, type, name, flags, inf):
        self.name = name
        self.type = type
        self.influence = inf
        self.active = (flags & C_ACT == 0)
        self.expanded = (flags & C_EXP != 0)
        
        ow = flags & C_OW_MASK
        if ow == 0:
            self.ownsp = 'WORLD'
        elif ow == C_OW_LOCAL:
            self.ownsp = 'LOCAL'
        elif ow == C_OW_LOCPAR:
            self.ownsp = 'LOCAL_WITH_PARENT'
        elif ow == C_OW_POSE:
            self.ownsp = 'POSE'

        tg = flags & C_TG_MASK
        if tg == 0:
            self.targsp = 'WORLD'
        elif tg == C_TG_LOCAL:
            self.targsp = 'LOCAL'
        elif tg == C_TG_LOCPAR:
            self.targsp = 'LOCAL_WITH_PARENT'
        elif tg == C_TG_POSE:
            self.targsp = 'POSE'


    def update(self, amt, bone):
        raise NameError("Unknown constraint: bone %s cns %s type %s" % (bone.name, self.name, self.type))


    def display(self):
        log.debug("    <Constraint %s %s %.3g>" % (self.type, self.name, self.influence))
        

    def write25(self, fp):
        fp.write(
            "      influence %s ;\n" % self.influence +
            "      is_proxy_local False ;\n" +
            "      active %s ;\n" % self.active +
            "      show_expanded %s ;\n" % self.expanded +
            "      target_space '%s' ;\n" % self.targsp +
            "      owner_space '%s' ;\n" % self.ownsp +
            "    end Constraint\n")
        
#
#   Constraint subclasses
#

class CIkConstraint(CConstraint):
    def __init__(self, flags, inf, data, lockLoc, lockRot):
        CConstraint.__init__(self, "IK", data[0], flags, inf)
        self.subtar = data[1]
        self.chainlen = data[2]
        self.pole = data[3]
        if self.pole:
            (self.angle, self.ptar) = self.pole
        else:
            (self.angle, self.ptar) = (0, None)
        (self.useLoc, self.useRot, self.useStretch) = data[4]
        self.lockLoc = lockLoc
        self.lockRot = lockRot
        (lockRotX, lockRotY, lockRotZ) = lockRot
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s IK True\n" % self.name)

        if self.subtar:
            fp.write(
            "      target Refer Object %s ;\n" % (the.Human) +
            "      subtarget '%s' ;\n" % self.subtar +
            "      use_tail True ;\n")
        else:
            fp.write(
            "      use_tail False ;\n")

        fp.write(
            "      pos_lock Array 1 1 1  ;\n" +
            "      rot_lock Array 1 1 1  ;\n" +
            "      reference_axis 'BONE' ;\n" +
            "      chain_count %d ;\n" % self.chainlen +
            "      ik_type 'COPY_POSE' ;\n" +
            "      iterations 500 ;\n" +
            "      limit_mode 'LIMITDIST_INSIDE' ;\n" +
            "      orient_weight 1 ;\n")

        if self.pole:
            fp.write(
            "      pole_angle %.6g ;\n" % self.angle +
            "      pole_subtarget '%s' ;\n" % self.ptar +
            "      pole_target Refer Object %s ;\n" % (the.Human))

        fp.write(
            "      use_location %s ;\n" % self.useLoc +
            "      use_rotation %s ;\n" % self.useRot +
            "      use_stretch %s ;\n" % self.useStretch +
            "      weight 1 ;\n")
        CConstraint.write25(self, fp)
        
        
    def update(self, amt, bone):
        if self.chainlen == 1:
            target = amt.bones[self.subtar]
            head = bone.getHead()
            goal = target.getHead()
            vec = goal - head
            dist = math.sqrt(dot(vec,vec))
            goal = head + vec*(bone.length/dist)
            bone.stretchTo(goal, False)

            if self.ptar:               
                pole = amt.bones[self.ptar].getHead()
                bone.poleTargetCorrect(head, goal, pole, self.angle)
        else:
            raise NameError("IK chainlen %d %s" % (self.chainlen, bone.name))
        
        
class CActionConstraint(CConstraint):    
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "Action", data[0], flags, inf)
        self.type = "Action"
        self.action = data[1]
        self.subtar = data[2]
        self.channel = data[3]
        (self.sframe, self.eframe) = data[4]
        (self.amin, self.amax) = data[5]
    
    def write25(self, fp):        
        fp.write(
            "    Constraint %s ACTION True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human)+
            "      action Refer Action %s ; \n" % self.action+
            "      frame_start %s ; \n" % self.sframe +
            "      frame_end %d ; \n" % self.eframe)
        if channel[0:3] == 'LOC':
            fp.write(
            "      maximum %.4f*theScale ; \n" % self.amax +
            "      minimum %.4f*theScale ; \n" % self.amin)
        else:
            fp.write(
            "      maximum %.4f ; \n" % self.amax +
            "      minimum %.4f ; \n" % self.amin)    
        fp.write(
            "      subtarget '%s' ; \n" % self.subtar +
            "      transform_channel '%s' ;\n" % self.channel)
        CConstraint.write25(self, fp)


class CCopyRotConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "CopyRot", data[0], flags, inf)
        self.subtar = data[1]
        (self.usex, self.usey, self.usez) = data[2]
        (self.invertX, self.invertY, self.invertZ) = data[3]
        self.useOffs = data[4]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s COPY_ROTATION True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human)+
            "      invert Array %d %d %d ; \n" % (self.invertX, self.invertY, self.invertZ)+
            "      use Array %d %d %d  ; \n" % (self.usex, self.usey, self.usez)+
            "      subtarget '%s' ;\n" % self.subtar +
            "      use_offset %s ; \n" % self.useOffs)
        CConstraint.write25(self, fp)

    def update(self, amt, bone):
        target = amt.bones[self.subtar]
        if self.ownsp == 'WORLD':
            mat = target.matrixGlobal
            bone.matrixGlobal[0,:3] += self.influence*(mat[:3,:3] - bone.matrixGlobal[:3,:3])
        else:
            ay,ax,az = tm.euler_from_matrix(bone.matrixPose, axes='syxz')
            by,bx,bz = tm.euler_from_matrix(target.matrixPose, axes='syxz')
            if self.usex:
                ax += self.influence*(bx-ax)
            if self.usey:
                ay += self.influence*(by-ay)
            if self.usez:
                az += self.influence*(bz-az)
            testbones = ["DfmUpArm1_L", "DfmUpArm2_L", "DfmLoArm1_L", "DfmLoArm2_L", "DfmLoArm3_L"]
            if bone.name in testbones:
                log.debug("%s %s" % (bone.name, target.name))
                log.debug(str(bone.matrixPose))
                log.debug(str(target.matrixPose))
            bone.matrixPose = tm.euler_matrix(ay, ax, az, axes='syxz')
            if bone.name in testbones:
                log.debug(str(bone.matrixPose))
            bone.updateBone()
        


class CCopyLocConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "CopyLoc", data[0], flags, inf)
        self.subtar = data[1]
        (self.usex, self.usey, self.usez) = data[2]
        (self.invertX, self.invertY, self.invertZ) = data[3]
        self.head_tail = data[4]
        self.useOffs = data[5]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s COPY_LOCATION True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human)+
            "      invert Array %d %d %d ; \n" % (self.invertX, self.invertY, self.invertZ)+
            "      use Array %d %d %d  ; \n" % (self.usex, self.usey, self.usez)+
            "      head_tail %.3f ;\n" % self.head_tail +
            "      subtarget '%s' ;\n" % self.subtar +
            "      use_offset %s ; \n" % self.useOffs)
        CConstraint.write25(self, fp)

    def update(self, amt, bone):
        target = amt.bones[self.subtar]
        if self.ownsp == 'WORLD':
            mat = target.matrixGlobal
            bone.matrixGlobal[:3,3] += self.influence*(mat[:3,3] - bone.matrixGlobal[:3,3])
        else:
            halt
            mat = target.matrixPose
            bone.matrixPose[:3,3] += self.influence*(mat[:3,3] - bone.matrixPose[:3,3])
            bone.updateBone()


class CCopyScaleConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "CopyScale", data[0], flags, inf)
        self.subtar = data[1]
        (self.usex, self.usey, self.usez) = data[2]
        self.useOffs = data[3]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s COPY_ROTATION True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human) +
            "      use Array %d %d %d  ; \n" % (self.usex, self.usey, self.usez)+
            "      subtarget '%s' ;\n" % self.subtar +
            "      use_offset %s ;\n" % self.useOffs)
        CConstraint.write25(self, fp)

    def update(self, amt, bone):
        target = amt.bones[self.subtar]
        if self.ownsp == 'WORLD':
            mat = target.matrixGlobal
            bone.matrixGlobal[3,:3] += self.influence*(mat[3,:3] - bone.matrixGlobal[3,:3])
        else:
            halt
            mat = target.matrixPose
            if self.usex:
                bone.matrixPose[3,0] += self.influence*(mat[3,0] - bone.matrixPose[3,0])
            if self.usey:
                bone.matrixPose[3,1] += self.influence*(mat[3,1] - bone.matrixPose[3,1])
            if self.usez:
                bone.matrixPose[3,2] += self.influence*(mat[3,2] - bone.matrixPose[3,2])
            bone.updateBone()


class CCopyTransConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "CopyTrans", data[0], flags, inf)
        self.subtar = data[1]
        self.head_tail = data[2]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s COPY_TRANSFORMS True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human) +
            "      head_tail %.3f ;\n" % self.head_tail +
            "      subtarget '%s' ;\n" % self.subtar)
        CConstraint.write25(self, fp)

    def update(self, amt, bone):
        if self.ownsp == 'WORLD':
            mat = amt.bones[self.subtar].matrixGlobal
            bone.matrixGlobal += self.influence*(mat - bone.matrixGlobal)
        else:
            mat = amt.bones[self.subtar].matrixPose
            bone.matrixPose = self.influence*(mat - bone.matrixPose)
            bone.updateBone()


class CLimitRotConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "LimitRot", data[0], flags, inf)
        (self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax) = data[1]
        (self.usex, self.usey, self.usez) = data[2]
        self.ltra = (flags & C_LTRA != 0)
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s LIMIT_ROTATION True\n" % self.name +
            "      use_transform_limit %s ; \n" % self.ltra+
            "      max_x %.6g ;\n" % self.xmax +
            "      max_y %.6g ;\n" % self.ymax +
            "      max_z %.6g ;\n" % self.zmax +
            "      min_x %.6g ;\n" % self.xmin +
            "      min_y %.6g ;\n" % self.ymin +
            "      min_z %.6g ;\n" % self.zmin +
            "      use_limit_x %s ; \n" % self.usex +
            "      use_limit_y %s ; \n" % self.usey +
            "      use_limit_z %s ; \n" % self.usez)
        CConstraint.write25(self, fp)

    def update(self, amt, bone):
        quat = bone.getPoseQuaternion()
        rx,ry,rz = bone.quatAngles(quat)
        if self.usex:
            if rx > self.xmax: 
                quat[1] = math.tan(self.xmax/2)
            if rx < self.xmin: 
                quat[1] = math.tan(self.xmin/2)
        if self.usey:
            if ry > self.ymax: 
                quat[2] = math.tan(self.ymax/2)
            if ry < self.ymin: 
                quat[2] = math.tan(self.ymin/2)
        if self.usez:
            if rz > self.zmax: 
                quat[3] = math.tan(self.zmax/2)
            if rz < self.zmin: 
                quat[3] = math.tan(self.zmin/2)
        bone.setPoseQuaternion(quat)
        bone.updateBone()


class CLimitLocConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "LimitLoc", data[0], flags, inf)
        (self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax) = data[1]
        (self.useminx, self.usemaxx, self.useminy, self.usemaxy, self.useminz, self.usemaxz) = data[2]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s LIMIT_LOCATION True\n" % self.name +
            "      use_transform_limit True ;\n" +
            "      max_x %s*theScale ;\n" % self.xmax +
            "      max_y %s*theScale ;\n" % self.ymax +
            "      max_z %s*theScale ;\n" % self.zmax +
            "      min_x %s*theScale ;\n" % self.xmin +
            "      min_y %s*theScale ;\n" % self.ymin +
            "      min_z %s*theScale ;\n" % self.zmin +
            "      use_max_x %s ;\n" % self.usemaxx +
            "      use_max_y %s ;\n" % self.usemaxy +
            "      use_max_z %s ;\n" % self.usemaxz +
            "      use_min_x %s ;\n" % self.useminx +
            "      use_min_y %s ;\n" % self.useminy +
            "      use_min_z %s ;\n" % self.useminz)
        CConstraint.write25(self, fp)
        
    def update(self, amt, bone):
        pass

        
class CLimitScaleConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "LimitScale", data[0], flags, inf)
        (self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax) = data[1]
        (self.usex, self.usey, self.usez) = data[2]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s LIMIT_SCALE True\n" % self.name +
            "      max_x %.6g ;\n" % self.xmax +
            "      max_y %.6g ;\n" % self.ymax +
            "      max_z %.6g ;\n" % self.zmax +
            "      min_x %.6g ;\n" % self.xmin +
            "      min_y %.6g ;\n" % self.ymin +
            "      min_z %.6g ;\n" % self.zmin +
            "      use_max_x %s ;\n" % self.usex +
            "      use_max_y %s ;\n" % self.usey +
            "      use_max_z %s ;\n" % self.usez +
            "      use_min_x %s ;\n" % self.usex +
            "      use_min_y %s ;\n" % self.usey +
            "      use_min_z %s ;\n" % self.usez)
        CConstraint.write25(self, fp)

    def update(self, amt, bone):
        pass


class CTransformConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "Transform", data[0], flags, inf)
        self.subtar = data[1]
        self.map_from = data[2]
        self.from_min = data[3]
        self.from_max = data[4]
        self.map_to_from = data[5]
        self.map_to = data[6]
        self.to_min = data[7]
        self.to_max = data[8]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s TRANSFORM True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human) +
            "      subtarget '%s' ;\n" % self.subtar +
            "      map_from '%s' ;\n" % self.map_from + 
            "      from_min_x %s ;\n" % self.from_min[0] + 
            "      from_min_y %s ;\n" % self.from_min[1] + 
            "      from_min_z %s ;\n" % self.from_min[2] + 
            "      from_max_x %s ;\n" % self.from_max[0] + 
            "      from_max_y %s ;\n" % self.from_max[1] + 
            "      from_max_z %s ;\n" % self.from_max[2] + 
            "      map_to '%s' ;\n" % self.map_to + 
            "      map_to_x_from '%s' ;\n" % self.map_to_from[0] +
            "      map_to_y_from '%s' ;\n" % self.map_to_from[1] +
            "      map_to_z_from '%s' ;\n" % self.map_to_from[2] +
            "      to_min_x %s ;\n" % self.to_min[0] + 
            "      to_min_y %s ;\n" % self.to_min[1] + 
            "      to_min_z %s ;\n" % self.to_min[2] + 
            "      to_max_x %s ;\n" % self.to_max[0] + 
            "      to_max_y %s ;\n" % self.to_max[1] + 
            "      to_max_z %s ;\n" % self.to_max[2])
        CConstraint.write25(self, fp)

    def update(self, amt, bone):
        target = amt.bones[self.subtar]
        if self.ownsp == 'WORLD':
            halt
        else:
            if self.map_from != 'ROTATION' or self.map_to != 'ROTATION':
                halt
            brad = tm.euler_from_matrix(target.matrixPose, axes='sxyz')
            arad = []
            for n in range(3):
                if self.from_max[n] == self.from_min[n]:
                    cdeg = self.from_max[n]
                else:
                    bdeg = brad[n]/D
                    if bdeg < self.from_min[n]: bdeg = self.from_min[n]
                    if bdeg > self.from_max[n]: bdeg = self.from_max[n]
                    slope = (self.to_max[n] - self.to_min[n])/float(self.from_max[n] - self.from_min[n])
                    adeg = slope*(bdeg - self.from_min[n]) + self.to_min[n]
                arad.append( adeg*D )
            mat = tm.euler_matrix(arad[0], arad[1], arad[2], axes='sxyz') 
            bone.matrixPose[:3,:3] = mat[:3,:3]
            bone.updateBone()
        return            
        log.debug("Transform %s %s" % (bone.name, target.name))
        log.debug("Arad %s" % arad)
        log.debug("Brad %s" % brad)
        log.debug("P %s" % bone.matrixPose)
        log.debug("R %s" % bone.matrixRest)
        log.debug("G %s" % bone.matrixGlobal)
        pass


class CDampedTrackConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "DampedTrack", data[0], flags, inf)
        self.subtar = data[1]
        self.track = data[2]
        self.headtail = data[3]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s DAMPED_TRACK True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human) +
            "      subtarget '%s' ;\n" % self.subtar +
            "      head_tail %d ;\n" % self.headtail +
            "      track_axis '%s' ;\n" % self.track)
        CConstraint.write25(self, fp)


class CLockedTrackConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "LockedTrack", data[0], flags, inf)
        self.subtar = data[1]
        self.trackAxis = data[2]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s LOCKED_TRACK True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human) +
            "      subtarget '%s' ;\n" % self.subtar +
            "      track_axis '%s' ;\n" % self.trackAxis)
        CConstraint.write25(self, fp)


class CStretchToConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "StretchTo", data[0], flags, inf)
        self.subtar = data[1]
        self.head_tail = data[2]
        self.bulge = data[3]
        if len(data) > 4:
            self.rest_length = data[4]
        else:
            self.rest_length = None
        if flags & C_STRVOL:
            self.volume = 'VOLUME_XZX'
        else:
            self.volume = 'NO_VOLUME'
        if flags & C_PLANEZ:
            self.axis = 'PLANE_Z'
        else:
            self.axis = 'PLANE_X'

    def write25(self, fp):        
        fp.write(
            "    Constraint %s STRETCH_TO True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human) +
            "      bulge %.2f ;\n" % self.bulge +
            "      head_tail %s ;\n" % self.head_tail +
            "      keep_axis '%s' ;\n" % self.axis +
            "      subtarget '%s' ;\n" % self.subtar +
            "      volume '%s' ;\n" % self.volume)
        if self.rest_length != None:
            fp.write("      rest_length %s ;\n" % self.rest_length)
        CConstraint.write25(self, fp)

    def update(self, amt, bone):
        target = amt.bones[self.subtar]
        goal = (1-self.head_tail)*target.getHead() + self.head_tail*target.getTail()
        bone.stretchTo(goal, True)
        

class CTrackToConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "TrackTo", data[0], flags, inf)
        self.subtar = data[1]
        self.head_tail = data[2]
        self.track_axis = data[3]
        self.up_axis = data[4]
        self.use_target_z = data[5]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s TRACK_TO True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human) +
            "      head_tail %s ;\n" % self.head_tail +
            "      track_axis '%s' ;\n" % self.track_axis +
            "      up_axis '%s' ;\n" % self.up_axis +
            "      subtarget '%s' ;\n" % self.subtar +
            "      use_target_z %s ;\n" % self.use_target_z)
        CConstraint.write25(self, fp)


class CLimitDistConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "LimitDist", data[0], flags, inf)
        self.subtar = data[1]
        self.limit_mode = data[2]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s LIMIT_DISTANCE True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human) +
            "      limit_mode '%s' ;\n" % self.limit_mode +
            "      subtarget '%s' ;\n" % self.subtar)
        CConstraint.write25(self, fp)

    def update(self, amt, bone):
        pass


class CChildOfConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "ChildOf", data[0], flags, inf)
        subtar = data[1]
        (self.locx, self.locy, self.locz) = data[2]
        (self.rotx, self.roty, self.rotz) = data[3]
        (self.scalex, self.scaley, self.scalez) = data[4]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s CHILD_OF True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human) +
            "      subtarget '%s' ;\n" % self.subtar +
            "      use_location_x %s ;\n" % self.locx +
            "      use_location_y %s ;\n" % self.locy +
            "      use_location_z %s ;\n" % self.locz +
            "      use_rotation_x %s ;\n" % self.rotx +
            "      use_rotation_y %s ;\n" % self.roty +
            "      use_rotation_z %s ;\n" % self.rotz +
            "      use_scale_x %s ;\n" % self.scalex +
            "      use_scale_y %s ;\n" % self.scaley +
            "      use_scale_z %s ;\n" % self.scalez)
        CConstraint.write25(self, fp)


class CSplineIkConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "SplineIk", data[0], flags, inf)
        self.target = data[1]
        self.count = data[2]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s SPLINE_IK True\n" % self.name +
            "      target Refer Object %s ;\n" % self.target +
            "      chain_count %d ;\n" % self.count +
            "      use_chain_offset False ;\n" +
            "      use_curve_radius True ;\n" +
            "      use_even_divisions False ;\n" +
            "      use_y_stretch True ;\n" +
            "      xz_scale_mode 'NONE' ;\n")
        CConstraint.write25(self, fp)


class CFloorConstraint(CConstraint):
    def __init__(self, flags, inf, data):
        CConstraint.__init__(self, "Floor", data[0], flags, inf)
        self.subtar = data[1]
        self.floor_location = data[2]
        self.offset = data[3]
        self.use_rotation = data[4]
        self.use_sticky = data[5]
        
    def write25(self, fp):        
        fp.write(
            "    Constraint %s FLOOR True\n" % self.name +
            "      target Refer Object %s ;\n" % (the.Human) +
            "      floor_location '%s' ;\n" % self.floor_location +
            "      offset %.4f ;\n" % self.offset +
            "      subtarget '%s' ;\n" % self.subtar +
            "      use_rotation %s ;\n" % self.use_rotation +
            "      use_sticky %s ;\n" % self.use_sticky)
        CConstraint.write25(self, fp)

#
#    writeConstraints(fp, config, bname, constraints, lockLoc, lockRot)
#

def writeConstraints(fp, config, bname, constraints, lockLoc, lockRot):
    uses = (0,0,0)
    mins = (-pi, -pi, -pi)
    maxs = (pi, pi, pi)

    for (label, flags, inf, data) in constraints:
        if type(label) == str:
            typ = label
        else:
            raise NameError("Switch in", bname)

        if typ == 'IK':
            cns = CIkConstraint(flags, inf, data, lockLoc, lockRot)
            if config.mhx25:
                cns.write25(fp)
            else:
                fp.write(
                    "\t\tconstraint IKSOLVER %s 1.0 \n" % self.name +
                    "\t\t\tCHAINLEN    int %d ; \n" % cns.chainlen +
                    "\t\t\tTARGET    obj the.Human ; \n" +
                    "\t\t\tBONE    str %s ; \n" % cns.subtar +
                    "\t\tend constraint\n")
        elif typ == 'Action':
            cns = CActionConstraint(flags, inf, data)
            cns.write25(fp)
        elif typ == 'CopyRot':
            cns = CCopyRotConstraint(flags, inf, data)
            if config.mhx25:
                cns.write25(fp)
            else:
                copy = cns.usex + 2*cns.usey + 4*cns.usez
                fp.write(
                    "\t\tconstraint COPYROT %s 1.0 \n" % cns.name +
                    "\t\t\tTARGET    obj the.Human ;\n" +
                    "\t\t\tBONE    str %s ; \n" % cns.subtar +
                    "\t\t\tCOPY    hex %x ;\n" %  copy +
                    "\t\tend constraint\n")
        elif typ == 'CopyLoc':
            cns = CCopyLocConstraint(flags, inf, data)
            if config.mhx25:
                cns.write25(fp)
            else:
                fp.write(
                    "\t\tconstraint COPYLOC %s 1.0 \n" % self.name +
                    "\t\t\tTARGET    obj the.Human ;\n" +
                    "\t\t\tBONE    str %s ; \n" % self.subtar +
                    "\t\tend constraint\n")
        elif typ == 'CopyScale':
            cns = CCopyScaleConstraint(flags, inf, data)
            cns.write25(fp)
        elif typ == 'CopyTrans':
            cns = CCopyTransConstraint(flags, inf, data)
            cns.write25(fp)
        elif typ == 'LimitRot':
            cns = CLimitRotConstraint(flags, inf, data)
            if config.mhx25:
                cns.write25(fp)
            else:
                limit = usex + 2*usey + 4*usez
                fp.write(
                    "\t\tconstraint LIMITROT Const 1.0 \n" +
                    "\t\t\tLIMIT    hex %x ;\n" % limit +
                    "\t\t\tOWNERSPACE       hex 1 ;\n" +
                    "\t\t\tXMIN       float %g ; \n" % xmin +
                    "\t\t\tXMAX       float %g ; \n" % xmax +
                    "\t\t\tYMIN       float %g ; \n" % ymin +
                    "\t\t\tYMAX       float %g ; \n" % ymax +
                    "\t\t\tZMIN       float %g ; \n" % zmin +
                    "\t\t\tZMAX       float %g ; \n" % zmax +
                    "\t\tend constraint\n")
            mins = (cns.xmin, cns.ymin, cns.zmin)
            maxs = (cns.xmax, cns.ymax, cns.zmax)
        elif typ == 'LimitLoc':
            cns = CLimitLocConstraint(flags, inf, data)
            if config.mhx25:
                cns.write25(fp)
            else:
                limit = cns.useminx + 2*cns.useminy + 4*cns.useminz + 8*cns.usemaxx + 16*cns.usemaxy + 32*cns.usemaxz
                fp.write("\t\tconstraint LIMITLOC Const 1.0 \n")
                fp.write(
                    "\t\t\tLIMIT    hex %x ;\n" % limit +
                    "\t\t\tOWNERSPACE       hex 1 ;\n" +
                    "\t\t\tXMIN       float %g ; \n" % cns.xmin +
                    "\t\t\tXMAX       float %g ; \n" % cns.xmax +
                    "\t\t\tYMIN       float %g ; \n" % cns.ymin +
                    "\t\t\tYMAX       float %g ; \n" % cns.ymax +
                    "\t\t\tZMIN       float %g ; \n" % cns.zmin +
                    "\t\t\tZMAX       float %g ; \n" % cns.zmax +
                    "\t\tend constraint\n")
        elif typ == 'LimitScale':
            cns = CLimitScaleConstraint(flags, inf, data)
            cns.write25(fp)
        elif typ == 'Transform':
            cns = CTransformConstraint(flags, inf, data)
            cns.write25(fp)
        elif typ == 'LockedTrack':
            cns = CLockedTrackConstraint(flags, inf, data)
            cns.write25(fp)
        elif typ == 'DampedTrack':
            cns = CDampedTrackConstraint(flags, inf, data)
            cns.write25(fp)
        elif typ == 'StretchTo':
            cns = CStretchToConstraint(flags, inf, data)
            if config.mhx25:
                cns.write25(fp)
            else:
                fp.write(
                    "\t\tconstraint STRETCHTO %s 1.0 \n" % self.name +
                    "\t\t\tTARGET    obj the.Human ;\n" +
                    "\t\t\tBONE    str %s ;\n" % subtar +
                    "\t\t\tPLANE    hex 2 ;\n" +
                    "\t\tend constraint\n")
        elif typ == 'TrackTo':
            cns = CTrackToConstraint(flags, inf, data)
            cns.write25(fp)
        elif typ == 'LimitDist':
            cns = CLimitDistConstraint(flags, inf, data)
            if config.mhx25:
                cns.write25(fp)
            else:
                fp.write(
                    "\t\tconstraint LIMITDIST %s 1.0 \n" % self.name +
                    "\t\t\tTARGET    obj the.Human ;\n" +
                    "\t\t\tBONE    str %s ;\n" % subtar +
                    "\t\tend constraint\n")
        elif typ == 'ChildOf':
            cns = CChildOfConstraint(flags, inf, data)
            cns.write25(fp)
        elif typ == 'SplineIK':
            cns = CSplineIkConstraint(flags, inf, data)
            cns.write25(fp)
        elif typ == 'Floor':
            cns = CFloorConstraint(flags, inf, data)
            cns.write25(fp)
        else:
            log.message(label)
            log.message(typ)
            raise NameError("Unknown constraint type %s" % typ)
    return (uses, mins, maxs)


#
#    getConstraints(bname, cdefs, lockLoc, lockRot)
#

def getConstraints(bname, cdefs, lockLoc, lockRot):
    constraints = []

    for (label, flags, inf, data) in cdefs:
        if inf == 0:
            continue
        
        if type(label) == str:
            typ = label
        else:
            raise NameError("Switch in", bname)

        if typ == 'IK':
            cns = CIkConstraint(flags, inf, data, lockLoc, lockRot)
        elif typ == 'Action':
            cns = CActionConstraint(flags, inf, data)
        elif typ == 'CopyRot':
            cns = CCopyRotConstraint(flags, inf, data)
        elif typ == 'CopyLoc':
            cns = CCopyLocConstraint(flags, inf, data)
        elif typ == 'CopyScale':
            cns = CCopyScaleConstraint(flags, inf, data)
        elif typ == 'CopyTrans':
            cns = CCopyTransConstraint(flags, inf, data)
        elif typ == 'LimitRot':
            cns = CLimitRotConstraint(flags, inf, data)
        elif typ == 'LimitLoc':
            cns = CLimitLocConstraint(flags, inf, data)
        elif typ == 'LimitScale':
            cns = CLimitScaleConstraint(flags, inf, data)
        elif typ == 'Transform':
            cns = CTransformConstraint(flags, inf, data)
        elif typ == 'LockedTrack':
            cns = CLockedTrackConstraint(flags, inf, data)
        elif typ == 'DampedTrack':
            cns = CDampedTrackConstraint(flags, inf, data)
        elif typ == 'StretchTo':
            cns = CStretchToConstraint(flags, inf, data)
        elif typ == 'TrackTo':
            cns = CTrackToConstraint(flags, inf, data)
        elif typ == 'LimitDist':
            cns = CLimitDistConstraint(flags, inf, data)
        elif typ == 'ChildOf':
            cns = CChildOfConstraint(flags, inf, data)
        elif typ == 'SplineIK':
            cns = CSplineIkConstraint(flags, inf, data)
        elif typ == 'Floor':
            cns = CFloorConstraint(flags, inf, data)
        else:
            log.message(label)
            log.message(typ)
            raise NameError("Unknown constraint type %s" % typ)
            
        constraints.append(cns)
    
    return constraints
    


