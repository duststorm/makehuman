""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
Functions shared by all rigs

"""

import aljabr, mhxbones
from aljabr import *

#
#	Bone layers
#

L_MAIN = 	0x0001
L_SKEL =	0x0002
L_ARMIK =	0x0004
L_ARMFK =	0x0008
L_LEGIK =	0x0010
L_LEGFK =	0x0020
L_HANDIK =	0x0040
L_HANDFK =	0x0080

L_PANEL	=	0x0100
L_TOE =		0x0200
L_HEAD =	0x0400

L_HLPIK	=	0x1000
L_HLPFK	=	0x2000
L_HELP	=	0x4000
L_DEF =		0x8000

#
#	Flags
#


F_CON = 0x0001
F_DEF = 0x0002
F_RES = 0x0004
F_WIR = 0x0008
F_NOSCALE = 0x0010
F_GLOC = 0x0020
F_LOCK = 0x0040
F_HID = 0x0080
F_NOCYC = 0x0100


P_LKROT4 = 0x0001
P_LKROTW = 0x0002
P_IKLIN = 0x0004
P_IKROT = 0x0008

C_OWNER = 0x0001
C_TARGET = 0x0002
C_ACT = 0x0004
C_EXP = 0x0008
C_LTRA = 0x0010
C_LOCAL = 0x0020

#
#	newSetupJoints (obj, joints, headTails):
#
def newSetupJoints (obj, joints, headTails):
	global rigHead, rigTail, locations
	locations = {}
	for (key, typ, data) in joints:
		if typ == 'j':
			loc = mhxbones.calcJointPos(obj, data)
			locations[key] = loc
			locations[data] = loc
		elif typ == 'v':
			v = int(data)
			locations[key] = obj.verts[v].co
		elif typ == 'x':
			locations[key] = [float(data[0]), float(data[2]), -float(data[1])]

	for (key, typ, data) in joints:
		if typ == 'j':
			pass
		elif typ == 'b':
			locations[key] = locations[data]
		elif typ == 'v':
			pass
		elif typ == 'x':
			pass
		elif typ == 'l':
			((k1, joint1), (k2, joint2)) = data
			locations[key] = vadd(vmul(locations[joint1], k1), vmul(locations[joint2], k2))
		elif typ == 'o':
			(joint, offs) = data
			locations[key] = vadd(locations[joint], offs)
		else:
			raise NameError("Unknown %s" % typ)

	rigHead = {}
	rigTail = {}
	for (bone, head, tail) in headTails:
		rigHead[bone] = locations[head]
		rigTail[bone] = locations[tail]
	return 

#
#	writeArmature(fp, armature, mhx25):
#	boolString(val):
#	addBone25(bone, roll, parent, flags, layers, bbone, fp):
#	addBone24(bone, roll, parent, flags, layers, bbone, fp):
#

def writeArmature(fp, armature, mhx25):
	global Mhx25
	Mhx25 = mhx25
	if Mhx25:
		for (bone, cond, roll, parent, flags, layers, bbone) in armature:
			addBone25(bone, cond, roll, parent, flags, layers, bbone, fp)
	else:
		for (bone, cond, roll, parent, flags, layers, bbone) in armature:
			addBone24(bone, cond, roll, parent, flags, layers, bbone, fp)
	return

def boolString(val):
	if val:
		return "True"
	else:
		return "False"

def addBone25(bone, cond, roll, parent, flags, layers, bbone, fp):
	global rigHead, rigTail

	conn = boolString(flags & F_CON)
	deform = boolString(flags & F_DEF)
	restr = boolString(flags & F_RES)
	wire = boolString(flags & F_WIR)
	scale = boolString(flags & F_NOSCALE == 0)
	lloc = boolString(flags & F_GLOC == 0)
	locked = boolString(flags & F_LOCK)
	hidden = boolString(flags & F_HID)
	cyc = boolString(flags & F_NOCYC == 0)
	(bin, bout, bseg) = bbone

	fp.write("\n  Bone %s %s\n" % (bone, cond))
	(x, y, z) = rigHead[bone]
	fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,-z,y))
	(x, y, z) = rigTail[bone]
	fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,-z,y))
	if parent:
		fp.write("    parent Refer Bone %s ; \n" % (parent))
	fp.write(
"    roll %.6g ; \n" % (roll)+
"    bbone_in %d ; \n" % (bin) +
"    bbone_out %d ; \n" % (bout) +
"    bbone_segments %d ; \n" % (bseg) +
"    connected %s ; \n" % (conn) +
"    cyclic_offset %s ; \n" % cyc +
"    deform %s ; \n" % (deform)+
"    hidden %s ; \n" % hidden +
"    draw_wire %s ; \n" % (wire) +
"    hinge True ; \n"+
"    inherit_scale %s ; \n" % (scale) +
"    layer Array ")

	bit = 1
	for n in range(32):
		if layers & bit:
			fp.write("1 ")
		else:
			fp.write("0 ")
		bit = bit << 1

	fp.write(" ; \n" +
"    local_location %s ; \n" % lloc +
"    locked %s ; \n" % locked +
"    multiply_vertexgroup_with_envelope False ; \n"+
"    restrict_select %s ; \n" % (restr) +
"  end Bone \n")

def addBone24(bone, cond, roll, parent, flags, layers, bbone, fp):
	global rigHead, rigTail

	flags24 = 0
	if flags & F_CON:
		flags24 += 0x001
	if flags & F_DEF == 0:
		flags24 += 0x004
	if flags & F_NOSCALE:
		flags24 += 0x0e0

	fp.write("\n\tbone %s %s %x %x\n" % (bone, parent, flags24, layers))
	(x, y, z) = rigHead[bone]
	fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,y,z))
	(x, y, z) = rigTail[bone]
	fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,y,z))
	fp.write("    roll %.6g %.6g ; \n" % (roll, roll))
	fp.write("\tend bone\n")
	return

#
#	writeBoneGroups(fp, groups):
#

def writeBoneGroups(fp, groups):
	for (name, theme) in groups:
		fp.write(
"    BoneGroup %s\n" % name +
"      color_set '%s' ;\n" % theme +
"    end BoneGroup\n")
	return


#
#	addPoseBone(fp, cond, bone, customShape, boneGroup, lockLoc, lockRot, lockScale, ik_dof, flags, constraints):
#

def addPoseBone(fp, cond, bone, customShape, boneGroup, lockLoc, lockRot, lockScale, ik_dof, flags, constraints):
	global boneGroups, Mhx25

	(lockLocX, lockLocY, lockLocZ) = lockLoc
	(lockRotX, lockRotY, lockRotZ) = lockRot
	(lockScaleX, lockScaleY, lockScaleZ) = lockScale
	(ik_dof_x, ik_dof_y, ik_dof_z) = ik_dof

	ikLin = boolString(flags & P_IKLIN)
	ikRot = boolString(flags & P_IKROT)
	lkRot4 = boolString(flags & P_LKROT4)
	lkRotW = boolString(flags & P_LKROTW)

	if Mhx25:
		fp.write("\n  Posebone %s %s \n" % (bone, cond))
	else:
		# limitX = flags & 1
		# limitY = (flags >> 1) & 1
		# limitZ = (flags >> 2) & 1
		# lockXRot = (flags >> 3) & 1
		# lockYRot = (flags >> 4) & 1
		# lockZRot = (flags >> 5) & 1
		ikFlags = 8*lockRotX + 16*lockRotY + 32*lockRotZ
		fp.write("\tposebone %s %x \n" % (bone, ikFlags))
		if customShape:
			fp.write("\t\tdisplayObject _object['%s'] ;\n" % customShape)

	for (typ, flags, data) in constraints:
		if typ == 'IK':
			addIkConstraint(fp, flags, data)
		elif typ == 'Action':
			addActionConstraint(fp, flags, data)
		elif typ == 'CopyLoc':
			addCopyLocConstraint(fp, flags, data)
		elif typ == 'CopyRot':
			addCopyRotConstraint(fp, flags, data)
		elif typ == 'CopyScale':
			addCopyScaleConstraint(fp, flags, data)
		elif typ == 'CopyTrans':
			addCopyTransConstraint(fp, flags, data)
		elif typ == 'LimitRot':
			addLimitRotConstraint(fp, flags, data)
		elif typ == 'LimitLoc':
			addLimitLocConstraint(fp, flags, data)
		elif typ == 'DampedTrack':
			addDampedTrackConstraint(fp, flags, data)
		elif typ == 'StretchTo':
			addStretchToConstraint(fp, flags, data)
		elif typ == 'LimitDist':
			addLimitDistConstraint(fp, flags, data)
		else:
			raise NameError("Unknown constraint type %s" % typ)

	if not Mhx25:
		fp.write("\tend posebone\n")
		return

	fp.write(
"    ik_dof Array %d %d %d  ; \n" % (ik_dof_x, ik_dof_y, ik_dof_z) +
"    ik_limit Array 0 0 0  ; \n"+
"    ik_stiffness Array 0.0 0.0 0.0  ; \n")
	'''
	fp.write(
"    ik_max Array 3.14159274101 3.14159274101 3.14159274101  ; \n"+
"    ik_min Array -3.14159274101 -3.14159274101 -3.14159274101  ; \n")
	fp.write(
"    ik_max Array 180 180 180 ;\n"+
"    ik_min Array -180 -180 -180 ;\n")
	'''
	#if boneGroup:
	#	fp.write("    bone_group Refer BoneGroup %s ; \n" % (boneGroup))

	if customShape:
		fp.write("    custom_shape Refer Object %s ; \n" % customShape)

	fp.write(
"    ik_lin_control %s ; \n" % ikLin +
"    ik_lin_weight 0 ; \n"+
"    ik_rot_control %s ; \n" % ikRot +
"    ik_rot_weight 0 ; \n"+
"    ik_stretch 0 ; \n"+
"    location (0,0,0) ; \n"+
"    lock_location Array %d %d %d ;\n"  % (lockLocX, lockLocY, lockLocZ)+
"    lock_rotation Array %d %d %d ;\n"  % (lockRotX, lockRotY, lockRotZ)+
"    lock_rotation_w %s ; \n" % lkRotW +
"    lock_rotations_4d %s ; \n" % lkRot4 +
"    lock_scale Array %d %d %d  ; \n" % (lockScaleX, lockScaleY, lockScaleZ)+
"  end Posebone \n")
	return

#
#	addIkConstraint(fp, flags, data)
#	addActionConstraint(fp, flags, data):
#	addCopyLocConstraint(fp, flags, data):
#	addCopyRotConstraint(fp, flags, data):
#	addCopyScaleConstraint(fp, flags, data):
#	addCopyTransConstraint(fp, flags, data):
#	addLimitRotConstraint(fp, flags, data):
#	addLimitLocConstraint(fp, flags, data):
#	addDampedTrackConstraint(fp, flags, data):
#	addStretchToConstraint(fp, flags, data):
#	addLimitDistConstraint(fp, flags, data):
#

def getSpace(flags, mask):
	if flags & mask:
		return 'LOCAL'
	else:
		return 'WORLD'

def addIkConstraint(fp, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	chainlen = data[2]
	pole = data[3]
	(useLoc, useRot) = data[4]
	inf = data[5]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	if Mhx25:
		fp.write(
"    Constraint %s IK\n" % name +
"      target Refer Object HumanRig ;\n" +
"      pos_lock Array 1 1 1  ;\n" +
"      rot_lock Array 1 1 1  ;\n" +
"      active %s ;\n" % active +
"      expanded %s ;\n" % expanded +
"      axis_reference 'BONE' ;\n" +
"      chain_length %d ;\n" % chainlen +
"      ik_type 'COPY_POSE' ;\n" +
"      influence %s ;\n" % inf +
"      iterations 500 ;\n" +
"      limit_mode 'LIMITDIST_INSIDE' ;\n" +
"      orient_weight 1 ;\n" +
"      owner_space '%s' ;\n" % ownsp)

		if pole:
			(angle, ptar) = pole
			fp.write(
"      pole_angle %.6g ;\n" % angle +
"      pole_subtarget '%s' ;\n" % ptar +
"      pole_target Refer Object HumanRig ;\n")

		fp.write(
"      proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp +
"      use_position %s ;\n" % useLoc +
"      use_rotation %s ;\n" % useRot +
"      use_stretch True ;\n" +
"      use_tail True ;\n" +
"      use_target True ;\n" +
"      weight 1 ;\n" +
"    end Constraint\n")

	else:
		fp.write("\t\tconstraint IKSOLVER %s 1.0 \n" % name)
		fp.write(
"\t\t\tCHAINLEN	int %d ; \n" % chainlen +
"\t\t\tTARGET	obj HumanRig ; \n" +
"\t\t\tBONE	str %s ; \n" % subtar +
"\t\tend constraint\n")

	return

def addActionConstraint(fp, flags, data):
	global Mhx25
	name = data[0]
	action = data[1]
	subtar = data[2]
	channel = data[3]
	(sframe, eframe) = data[4]
	(amin, amax) = data[5]
	inf = data[6]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)
	
	fp.write(
"    Constraint %s ACTION \n" % name +
"      target Refer Object HumanRig ; \n"+
"      action Refer Action %s ; \n" % action+
"      active %s ;\n" % active +
"      expanded %s ;\n" % expanded +
"      frame_start %s ; \n" % sframe +
"      frame_end %d ; \n" % eframe+
"      influence %s ; \n" % inf +
"      maximum %f ; \n" % amax +
"      minimum %f ; \n" % amin +
"      owner_space '%s' ; \n" % ownsp +
"      proxy_local False ; \n"+
"      subtarget '%s' ; \n" % subtar +
"      target_space '%s' ; \n" % targsp +
"      transform_channel '%s' ;\n" % channel +
"    end Constraint \n")
	return

def addCopyRotConstraint(fp, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	inf = data[2]
	(useX, useY, useZ) = data[3]
	(invertX, invertY, invertZ) = data[4]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	if Mhx25:
		fp.write(
"    Constraint %s COPY_ROTATION \n" % name +
"      target Refer Object HumanRig ; \n"+
"      invert Array %d %d %d ; \n" % (invertX, invertY, invertZ)+
"      use Array %d %d %d  ; \n" % (useX, useY, useZ)+
"      active %s ;\n" % active +
"      expanded %s ;\n" % expanded +
"      influence %s ; \n" % inf +
"      owner_space '%s' ; \n" % ownsp+
"      proxy_local False ; \n"+
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ; \n" % targsp+
"      use_offset False ; \n"+
"    end Constraint \n")

	else:
		copy = useX + 2*useY + 4*useZ
		fp.write(
"\t\tconstraint COPYROT %s 1.0 \n" % name +
"\t\t\tTARGET	obj HumanRig ;\n" +
"\t\t\tBONE	str %s ; \n" % subtar +
"\t\t\tCOPY	hex %x ;\n" %  copy +
"\t\tend constraint\n")
	return

def addCopyLocConstraint(fp, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	inf = data[2]
	(useX, useY, useZ) = data[3]
	(invertX, invertY, invertZ) = data[4]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	if Mhx25:
		fp.write(
"    Constraint %s COPY_LOCATION \n" % name +
"      target Refer Object HumanRig ; \n"+
"      invert Array %d %d %d ; \n" % (invertX, invertY, invertZ)+
"      use Array %d %d %d  ; \n" % (useX, useY, useZ)+
"      active %s ;\n" % active +
"      expanded %s ;\n" % expanded +
"      influence %s ; \n" % inf +
"      owner_space '%s' ; \n" % ownsp +
"      proxy_local False ; \n"+
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ; \n" % targsp+
"      use_offset False ; \n"+
"    end Constraint \n")

	else:
		fp.write(
"\t\tconstraint COPYLOC %s 1.0 \n" % name +
"\t\t\tTARGET	obj HumanRig ;\n" +
"\t\t\tBONE	str %s ; \n" % subtar +
"\t\tend constraint\n")	return

def addCopyScaleConstraint(fp, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	inf = data[2]
	(useX, useY, useZ) = data[3]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	fp.write(
"    Constraint %s COPY_SCALE\n" % name +
"      target Refer Object HumanRig ;\n" +
"      use Array %d %d %d  ; \n" % (useX, useY, useZ)+
"      active %s ;\n" % active +
"      expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      owner_space '%s' ;\n" % ownsp +
"      proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp +
"      use_offset False ;\n" +
"    end Constraint\n")
	return

def addCopyTransConstraint(fp, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	inf = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)
	
	fp.write(
"    Constraint %s COPY_TRANSFORMS\n" % name +
"      target Refer Object HumanRig ;\n" +
"      active %s ;\n" % active +
"      expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      owner_space '%s' ;\n" % ownsp +
"      proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp +
"    end Constraint\n")
	return


def addLimitRotConstraint(fp, flags, data):
	global Mhx25
	name = data[0]
	(xmin, xmax, ymin, ymax, zmin, zmax) = data[1]
	(usex, usey, usez) = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)
	ltra = boolString(flags & C_LTRA == 0)
	
	if Mhx25:
		fp.write(	
"    Constraint %s LIMIT_ROTATION \n" % name+
"      active %s ;\n" % active +
"      expanded %s ;\n" % expanded +
"      influence 1 ; \n"+
"      limit_transform %s ; \n" % ltra+
"      maximum_x %.6g ;\n" % xmax +
"      maximum_y %.6g ;\n" % ymax +
"      maximum_z %.6g ;\n" % zmax +
"      minimum_x %.6g ;\n" % xmin +
"      minimum_y %.6g ;\n" % ymin +
"      minimum_z %.6g ;\n" % zmin +
"      owner_space '%s' ; \n" % ownsp+
"      proxy_local False ; \n"+
"      target_space '%s' ; \n" % targsp+
"      use_limit_x %s ; \n" % usex +
"      use_limit_y %s ; \n" % usey +
"      use_limit_z %s ; \n" % usez +
"   end Constraint \n")

	else:
		limit = usex + 2*usey + 4*usez
		fp.write(
"\t\tconstraint LIMITROT Const 1.0 \n" +
"\t\t\tLIMIT	hex %x ;\n" % limit +
"\t\t\tOWNERSPACE       hex 1 ;\n" +
"\t\t\tXMIN       float %g ; \n" % xmin +
"\t\t\tXMAX       float %g ; \n" % xmax +
"\t\t\tYMIN       float %g ; \n" % ymin +
"\t\t\tYMAX       float %g ; \n" % ymax +
"\t\t\tZMIN       float %g ; \n" % zmin +
"\t\t\tZMAX       float %g ; \n" % zmax +
"\t\tend constraint\n")
	return

def addLimitLocConstraint(fp, flags, data):
	global Mhx25
	name = data[0]
	(xmin, xmax, ymin, ymax, zmin, zmax) = data[1]
	(useminx, usemaxx, useminy, usemaxy, useminz, usemaxz) = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)
	
	if Mhx25:
		fp.write(
"    Constraint %s LIMIT_LOCATION \n" % name +
"      active %s ;\n" % active +
"      expanded %s ;\n" % expanded +
"      influence 1 ;\n" +
"      limit_transform True ;\n" +
"      maximum_x %.6g ;\n" % xmax +
"      maximum_y %.6g ;\n" % ymax +
"      maximum_z %.6g ;\n" % zmax +
"      minimum_x %.6g ;\n" % xmin +
"      minimum_y %.6g ;\n" % ymin +
"      minimum_z %.6g ;\n" % zmin +
"      owner_space '%s' ;\n" % ownsp +
"      proxy_local False ;\n" +
"      target_space '%s' ;\n" % targsp +
"      use_maximum_x %s ;\n" % usemaxx +
"      use_maximum_y %s ;\n" % usemaxy +
"      use_maximum_z %s ;\n" % usemaxz +
"      use_minimum_x %s ;\n" % useminx +
"      use_minimum_y %s ;\n" % useminy +
"      use_minimum_z %s ;\n" % useminz +
"    end Constraint\n")

	else:
		limit = useminx + 2*useminy + 4*useminz + 8*usemaxx + 16*usemaxy + 32*usemaxz
		fp.write("\t\tconstraint LIMITLOC Const 1.0 \n")
		fp.write(
"\t\t\tLIMIT	hex %x ;\n" % limit +
"\t\t\tOWNERSPACE       hex 1 ;\n" +
"\t\t\tXMIN       float %g ; \n" % xmin +
"\t\t\tXMAX       float %g ; \n" % xmax +
"\t\t\tYMIN       float %g ; \n" % ymin +
"\t\t\tYMAX       float %g ; \n" % ymax +
"\t\t\tZMIN       float %g ; \n" % zmin +
"\t\t\tZMAX       float %g ; \n" % zmax +
"\t\tend constraint\n")

	return

def addDampedTrackConstraint(fp, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	track = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	fp.write(
"    Constraint %s DAMPED_TRACK\n" % name +
"      target Refer Object HumanRig ;\n" +
"      active %s ;\n" % active +
"      expanded %s ;\n" % expanded +
"      influence 1 ;\n" +
"      owner_space '%s' ;\n" % ownsp+
"      proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"      track '%s' ;\n" % track + 
"    end Constraint\n")
	return

def addStretchToConstraint(fp, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	axis = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	if Mhx25:
		fp.write(
"    Constraint %s STRETCH_TO\n" % name +
"      target Refer Object HumanRig ;\n" +
"      active %s ;\n" % active +
"      expanded %s ;\n" % expanded +
"      bulge 1 ;\n" +
"      influence 1 ;\n" +
"      keep_axis '%s' ;\n" % axis +
#"      original_length 0.0477343 ;\n" +
"      owner_space '%s' ;\n" % ownsp+
"      proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"      volume 'NO_VOLUME' ;\n" +
"    end Constraint\n")

	else:
		fp.write(
"\t\tconstraint STRETCHTO %s 1.0 \n" % name +
"\t\t\tTARGET	obj HumanRig ;\n" +
"\t\t\tBONE	str %s ;\n" % subtar +
"\t\t\tPLANE	hex 2 ;\n" +
"\t\tend constraint\n")	return

def addLimitDistConstraint(fp, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	if Mhx25:
		fp.write(
"    Constraint %s LIMIT_DISTANCE\n" % name +
"      target Refer Object HumanRig ;\n" +
"      active %s ;\n" % active +
"      expanded %s ;\n" % expanded +
"      influence 1 ;\n" +
"      limit_mode 'LIMITDIST_INSIDE' ;\n" +
"      owner_space '%s' ;\n" % ownsp +
"      proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"    end Constraint\n")

	else:
		fp.write(
"\t\tconstraint LIMITDIST %s 1.0 \n" % name +
"\t\t\tTARGET	obj HumanRig ;\n" +
"\t\t\tBONE	str %s ;\n" % subtar +
"\t\tend constraint\n")
	return

def constraintFlags(flags):
	ownsp = getSpace(flags, C_OWNER)
	targsp = getSpace(flags, C_TARGET)
	active = boolString(flags & C_ACT == 0)
	expanded = boolString(flags & C_EXP == 0)
	return (ownsp, targsp, active, expanded)

#
#	writeAction(fp, cond, name, action, lr, ikfk):
#	writeFCurves(fp, name, (x01, y01, z01, w01), (x21, y21, z21, w21)):
#	writeFCurve(fp, name, index, x01, x11, x21):
#

def writeAction(fp, cond, name, action, lr, ikfk):
	fp.write("Action %s %s\n" % (name,cond))
	if ikfk:
		iklist = ["IK", "FK"]
	else:
		iklist = [""]
	if lr:
		for (bone, (x01, y01, z01, w01), (x21, y21, z21, w21)) in action:
			for ik in iklist:
				writeFCurves(fp, "%s%s_L" % (bone, ik), (x01, y01, z01, w01), (x21, y21, z21, w21))
				writeFCurves(fp, "%s%s_R" % (bone, ik), (x21, y21, z21, w21), (x01, y01, z01, w01))
	else:
		for (bone, quat01, quat21) in action:
			for ik in iklist:
				writeFCurves(fp, "%s%s" % (bone, ik), quat01, quat21)
	fp.write("end Action\n\n")
	return

def writeFCurves(fp, name, (x01, y01, z01, w01), (x21, y21, z21, w21)):
	writeFCurve(fp, name, 0, x01, 1.0, x21)
	writeFCurve(fp, name, 1, y01, 0.0, y21)
	writeFCurve(fp, name, 2, z01, 0.0, z21)
	writeFCurve(fp, name, 3, w01, 0.0, w21)
	return

def writeFCurve(fp, name, index, x01, x11, x21):
	fp.write("\n" +
"  FCurve pose.bones[\"%s\"].rotation_quaternion %d\n" % (name, index) +
"    kp 1 %.6g ;\n" % (x01) +
"    kp 11 %.6g ;\n" % (x11) +
"    kp 21 %.6g ;\n" % (x21) +
"    extrapolation 'CONSTANT' ;\n" +
"  end FCurve \n")
	return

#
#	writeFkIkSwitch(fp, drivers)
#	writeDrivers(fp, cond, drivers):
#	writeDriver(fp, channel, index, expr, variables):
#

def writeFkIkSwitch(fp, drivers):
	for (bone, cnsFK, cnsIK, targ) in drivers:
		writeDriver(fp, "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsFK), -1, "1-ik",
			[("ik", 'TRANSFORMS', [('HumanRig', targ, 'LOC_X', C_LOCAL)])])
		writeDriver(fp, "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsIK), -1, "ik", 
			[("ik", 'TRANSFORMS', [('HumanRig', targ, 'LOC_X', C_LOCAL)])])

def writeDrivers(fp, cond, drivers):
	for (bone, typ, name, index, expr, variables) in drivers:
		if typ == 'INFL':
			writeDriver(fp, "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, name), index, expr, variables)
		elif typ == 'ROTE':
			writeDriver(fp, "pose.bones[\"%s\"].rotation_euler" % bone, index, expr, variables)
		elif typ == 'ROTQ':
			writeDriver(fp, "pose.bones[\"%s\"].rotation_quaternion" % bone, index, expr, variables)
		elif typ == 'LOC':
			writeDriver(fp, "pose.bones[\"%s\"].location" % bone, index, expr, variables)

def writeDriver(fp, channel, index, expr, variables):
	fp.write("\n"+
"    FCurve %s %d\n" % (channel, index) +
"      Driver\n")
	for (var, typ, targets) in variables:
		fp.write("        DriverVariable %s %s\n" % (var,typ))
		for (targ, boneTarg, ttype, flags) in targets:
			local = boolString(flags & C_LOCAL)
			fp.write(
"          Target %s OBJECT\n" % targ +
"            transform_type '%s' ;\n" % ttype)
			if boneTarg:
				fp.write("            bone_target '%s' ;\n" % boneTarg)
			fp.write(
"            use_local_space_transforms %s ;\n" % local +
"          end Target\n")
		fp.write("        end DriverVariable\n")
	fp.write(
"        expression '%s' ;\n" % expr +
"        show_debug_info False ;\n" +
"      end Driver\n" +
"      extrapolation 'CONSTANT' ;\n" +
"      locked False ;\n" +
"      selected True ;\n" +
"    end FCurve\n")
	return

#
#	setupRig(obj):
#	writeAllArmatures(fp)	
#	writeAllPoses(fp)	
#	writeAllActions(fp)	
#	writeAllDrivers(fp)	
#
import rig_body_25, rig_arm_25, rig_finger_25, rig_leg_25, rig_toe_25, rig_face_25, rig_panel_25

def setupRig(obj):
	newSetupJoints(obj, 
		rig_body_25.BodyJoints +
		rig_arm_25.ArmJoints +
		rig_finger_25.FingerJoints +
		rig_leg_25.LegJoints +
		rig_toe_25.ToeJoints +
		rig_face_25.FaceJoints +
		rig_panel_25.PanelJoints,
		
		rig_body_25.BodyHeadsTails +
		rig_arm_25.ArmHeadsTails +
		rig_finger_25.FingerHeadsTails +
		rig_leg_25.LegHeadsTails +
		rig_toe_25.ToeHeadsTails +
		rig_face_25.FaceHeadsTails +
		rig_panel_25.PanelHeadsTails)
	return
	
def writeAllArmatures(fp):
	writeArmature(fp, 
		rig_body_25.BodyArmature +
		rig_arm_25.ArmArmature +
		rig_finger_25.FingerArmature +
		rig_leg_25.LegArmature +
		rig_toe_25.ToeArmature +
		rig_face_25.FaceArmature +
		rig_panel_25.PanelArmature, True)
	return

def writeAllPoses(fp):
	rig_body_25.BodyWritePoses(fp)
	rig_arm_25.ArmWritePoses(fp)
	rig_finger_25.FingerWritePoses(fp)
	rig_leg_25.LegWritePoses(fp)
	rig_toe_25.ToeWritePoses(fp)
	rig_face_25.FaceWritePoses(fp)
	rig_panel_25.PanelWritePoses(fp)
	return
	
def writeAllActions(fp):
	rig_arm_25.ArmWriteActions(fp)
	rig_leg_25.LegWriteActions(fp)
	rig_finger_25.FingerWriteActions(fp)
	return

def writeAllDrivers(fp):
	writeFkIkSwitch(fp, rig_arm_25.ArmDrivers)
	writeFkIkSwitch(fp, rig_leg_25.LegDrivers)
	return

