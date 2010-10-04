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

PanelWorks = False

pi = 3.14159
deg180 = pi
deg90 = pi/2
deg80 = 4*pi/9
deg45 = pi/4
deg40 = 2*pi/9
deg20 = pi/9
deg10 = pi/18
deg1 = pi/180

yunit = [0,1,0]
zunit = [0,0,-1]

unlimited = (-pi,pi, -pi,pi, -pi,pi)

#
#	Bone layers
#

L_MAIN = 	0x0001
L_SPINE =	0x0002
L_ARMIK =	0x0004
L_ARMFK =	0x0008
L_LEGIK =	0x0010
L_LEGFK =	0x0020
L_HANDIK =	0x0040
L_HANDFK =	0x0080

L_PANEL	=	0x0100
L_TOE =		0x0200
L_HEAD =	0x0400
L_PALM =	0x0800

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
F_RES = 0
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
P_STRETCH = 0x0010

P_ROTMODE = 0x0f00
P_QUAT = 0x0000
P_XYZ = 0x0100



C_ACT = 0x0004
C_EXP = 0x0008
C_LTRA = 0x0010
C_LOCAL = 0x0020

C_OW_MASK = 0x0f00
C_OW_WORLD = 0x0000
C_OW_LOCAL = 0x0100
C_OW_LOCPAR = 0x0200
C_OW_POSE = 0x0300

C_TG_MASK = 0xf000
C_TG_WORLD = 0x0000
C_TG_LOCAL = 0x1000
C_TG_LOCPAR = 0x2000
C_TG_POSE = 0x3000

C_CHILDOF = C_OW_POSE+C_TG_WORLD

rootChildOfConstraints = [
		('ChildOf', C_CHILDOF, ['Floor', 'MasterFloor', 1.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Hips', 'MasterHips', 0.0, (1,1,1), (1,1,1), (1,1,1)]),
		('ChildOf', C_CHILDOF, ['Neck', 'MasterNeck', 0.0, (1,1,1), (1,1,1), (1,1,1)])
]

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
		elif typ == 'p':
			x = locations[data[0]]
			y = locations[data[1]]
			z = locations[data[2]]
			locations[key] = [x[0],y[1],z[2]]
		elif typ == 'v':
			pass
		elif typ == 'x':
			pass
		elif typ == 'l':
			((k1, joint1), (k2, joint2)) = data
			locations[key] = vadd(vmul(locations[joint1], k1), vmul(locations[joint2], k2))
		elif typ == 'o':
			(joint, offsSym) = data
			if type(offsSym) == str:
				offs = locations[offsSym]
			else:
				offs = offsSym
			locations[key] = vadd(locations[joint], offs)
		else:
			raise NameError("Unknown %s" % typ)

	rigHead = {}
	rigTail = {}
	for (bone, head, tail) in headTails:
		rigHead[bone] = findLocation(head)
		rigTail[bone] = findLocation(tail)
	return 

def findLocation(joint):
	try:
		(bone, offs) = joint
	except:
		offs = 0
	if offs:
		return vadd(locations[bone], offs)
	else:
		return locations[joint]

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
		for (bone, roll, parent, flags, layers, bbone) in armature:
			addBone25(bone, True, roll, parent, flags, layers, bbone, fp)
	else:
		for (bone, roll, parent, flags, layers, bbone) in armature:
			addBone24(bone, True, roll, parent, flags, layers, bbone, fp)
	return

def boolString(val):
	if val:
		return "True"
	else:
		return "False"

def addBone25(bone, cond, roll, parent, flags, layers, bbone, fp):
	global rigHead, rigTail

	#conn = boolString(flags & F_CON)
	conn = False
	deform = boolString(flags & F_DEF)
	restr = boolString(flags & F_RES)
	wire = boolString(flags & F_WIR)
	scale = boolString(flags & F_NOSCALE == 0)
	lloc = boolString(flags & F_GLOC == 0)
	lock = boolString(flags & F_LOCK)
	hide = boolString(flags & F_HID)
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
"    use_connect %s ; \n" % (conn) +
"    use_cyclic_offset %s ; \n" % cyc +
"    use_deform %s ; \n" % (deform)+
"    hide %s ; \n" % hide +
"    show_wire %s ; \n" % (wire) +
"    use_hinge True ; \n"+
"    use_inherit_scale %s ; \n" % (scale) +
"    layers Array ")

	bit = 1
	for n in range(32):
		if layers & bit:
			fp.write("1 ")
		else:
			fp.write("0 ")
		bit = bit << 1

	fp.write(" ; \n" +
"    use_local_location %s ; \n" % lloc +
"    lock %s ; \n" % lock +
"    use_envelope_multiply False ; \n"+
"    hide_select %s ; \n" % (restr) +
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
#	writeBoneGroups(fp):
#

BoneGroups = [
	('FK_L', 'THEME01'),
	('FK_R', 'THEME02'),
	('IK_L', 'THEME01'),
	('IK_R', 'THEME02'),
]

def boneGroupIndex(grp):
	index = 0
	for (name, theme) in BoneGroups:
		if name == grp:
			return index
		index += 1
	return None

def writeBoneGroups(fp):
	for (name, theme) in BoneGroups:
		fp.write(
"    BoneGroup %s\n" % name +
"      color_set '%s' ;\n" % theme +
"    end BoneGroup\n")
	return


#
#	writePoses(fp, poses)
#

def writePoses(fp, poses):
	for pose in poses:
		#print(pose)
		try:
			(typ, bone, customShape, boneGroup, lockLoc, lockRot, lockScale, ik_dof, flags, constraints) = pose
		except:
			typ = None
		if not typ:
			try:
				(typ, bone, mx) = pose
			except:
				typ = None
		if not typ:
			try:
				(typ, bone, mn, mx) = pose
			except:
				typ = None
		if not typ:
			try:
				(typ, bone, lockRot, target, limit) = pose
			except:
				typ = None
		if not typ:
			try:
				(typ, bone, ikBone, ikRot, fkBone, fkRot, cflags, pflags) = pose
			except:
				typ = None
				
		if typ == 'poseBone':
			addPoseBone(fp, bone, customShape, boneGroup, lockLoc, lockRot, lockScale, ik_dof, flags, constraints)
		elif typ == 'cSlider':
			mn = '-'+mx
			addPoseBone(fp, bone, 'MHSolid025', None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
				[('LimitLoc', C_OW_LOCAL+C_LTRA, ['Const', (mn,mx, '0','0', mn,mx), (1,1,1,1,1,1)])])
		elif typ == 'xSlider':
			addPoseBone(fp, bone, 'MHSolid025', None, (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
				[('LimitLoc', C_OW_LOCAL+C_LTRA, ['Const', (mn,mx, '0','0', mn,mx), (1,1,1,1,1,1)])])
		elif typ == 'ikHandle':
			addIKHandle(fp, bone, mn, mx)
		elif typ == 'singleIK':
			addSingleIK(fp, bone, lockRot, target, limit)
		elif typ == 'deformLimb':
			addDeformLimb(fp, bone, ikBone, ikRot, fkBone, fkRot, cflags, pflags)
		else:
			raise NameError("Unknown pose type %s" % typ)
	return
		

#
#	addIKHandle(fp, bone, customShape, limit):
#	addSingleIK(fp, bone, lockRot, target, limit):
#	addDeformLimb(fp, bone, ikBone, ikRot, fkBone, fkRot, cflags, pflags):
#

def addIKHandle(fp, bone, customShape, limit):
	if limit:
		cns = [('LimitDist', 0, ['LimitDist', 1.0, limit])]
	else:
		cns = []
	addPoseBone(fp, bone, customShape, None, (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, cns)

def addSingleIK(fp, bone, lockRot, target, limit):
	cns = [('IK', 0, ['IK', target, 1, None, (True, False, True), 1.0])]
	if limit:
		cns.append( ('LimitRot', C_OW_LOCAL, ['LimitRot', limit, (True, True, True)]) )
	addPoseBone(fp, bone, None, None, (1,1,1), lockRot, (1,1,1), (1,1,1), 0, cns)

def addDeformLimb(fp, bone, ikBone, ikRot, fkBone, fkRot, cflags, pflags):
	space = cflags & (C_OW_MASK + C_TG_MASK)
	constraints = [
		('CopyRot', space, ['RotIK', ikBone, 0.0, ikRot, (0,0,0), False]),
		('CopyRot', space, ['RotFK', fkBone, 1.0, fkRot, (0,0,0), False])
		]
	if pflags & P_STRETCH:
		constraints += [
		('CopyScale', 0, ['StretchIK', ikBone, 0.0, (0,1,0), False]),
		('CopyScale', 0, ['StretchFK', fkBone, 1.0, (0,1,0), False]),
		]		
	addPoseBone(fp, bone, None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, constraints)
	return

#
#	addPoseBone(fp, bone, customShape, boneGroup, lockLoc, lockRot, lockScale, ik_dof, flags, constraints):
#

def addPoseBone(fp, bone, customShape, boneGroup, lockLoc, lockRot, lockScale, ik_dof, flags, constraints):
	global BoneGroups, Mhx25

	(lockLocX, lockLocY, lockLocZ) = lockLoc
	(lockRotX, lockRotY, lockRotZ) = lockRot
	(lockScaleX, lockScaleY, lockScaleZ) = lockScale
	(ik_dof_x, ik_dof_y, ik_dof_z) = ik_dof

	ikLin = boolString(flags & P_IKLIN)
	ikRot = boolString(flags & P_IKROT)
	lkRot4 = boolString(flags & P_LKROT4)
	lkRotW = boolString(flags & P_LKROTW)

	if Mhx25:
		fp.write("\n  Posebone %s %s \n" % (bone, True))
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
		if boneGroup:
			index = boneGroupIndex(boneGroup)
			fp.write("\t\tbone_group_index %d ;\n" % index)

	(usex,usey,usez) = (0,0,0)
	(xmin, ymin, zmin) = (-pi, -pi, -pi)
	(xmax, ymax, zmax) = (pi, pi, pi)

	for (label, cflags, data) in constraints:
		if type(label) == str:
			typ = label
			switch = True
		else:
			(typ, switch) = label

		if typ == 'IK':
			addIkConstraint(fp, switch, cflags, data, lockLoc, lockRot)
		elif typ == 'Action':
			addActionConstraint(fp, switch, cflags, data)
		elif typ == 'CopyLoc':
			addCopyLocConstraint(fp, switch, cflags, data)
		elif typ == 'CopyRot':
			addCopyRotConstraint(fp, switch, cflags, data)
		elif typ == 'CopyScale':
			addCopyScaleConstraint(fp, switch, cflags, data)
		elif typ == 'CopyTrans':
			addCopyTransConstraint(fp, switch, cflags, data)
		elif typ == 'LimitRot':
			addLimitRotConstraint(fp, switch, cflags, data)
			(xmin, xmax, ymin, ymax, zmin, zmax) = data[1]
			(usex,usey,usez) = data[2]			
		elif typ == 'LimitLoc':
			addLimitLocConstraint(fp, switch, cflags, data)
		elif typ == 'LimitScale':
			addLimitScaleConstraint(fp, switch, cflags, data)
		elif typ == 'DampedTrack':
			addDampedTrackConstraint(fp, switch, cflags, data)
		elif typ == 'StretchTo':
			addStretchToConstraint(fp, switch, cflags, data)
		elif typ == 'LimitDist':
			addLimitDistConstraint(fp, switch, cflags, data)
		elif typ == 'ChildOf':
			addChildOfConstraint(fp, switch, cflags, data)
		else:
			print(label)
			print(typ)
			print(switch)
			raise NameError("Unknown constraint type %s" % typ)

	if not Mhx25:
		fp.write("\tend posebone\n")
		return
	'''
	fp.write(
"    ik_dof Array %d %d %d  ; \n" % (ik_dof_x, ik_dof_y, ik_dof_z) +
"    ik_limit Array %d %d %d  ; \n" % (usex,usey,usez)+
"    ik_stiffness Array 0.0 0.0 0.0  ; \n")
	fp.write(
"    ik_max Array %.4f %.4f %.4f ; \n" % (xmax, ymax, zmax) +
"    ik_min Array %.4f %.4f %.4f ; \n" % (xmin, ymin, zmin))
	'''

	if customShape:
		fp.write("    custom_shape Refer Object %s ; \n" % customShape)

	rotMode = flags & P_ROTMODE
	if rotMode == P_XYZ:
		fp.write("  rotation_mode 'XYZ' ;\n")

	fp.write(
"    use_ik_linear_control %s ; \n" % ikLin +
"    ik_linear_weight 0 ; \n"+
"    use_ik_rotation_control %s ; \n" % ikRot +
"    ik_rotation_weight 0 ; \n")
	
	if flags & P_STRETCH:
		fp.write("    ik_stretch 0.1 ; \n")
	else:
		fp.write("    ik_stretch 0 ; \n")

	fp.write(
"    location (0,0,0) ; \n"+
"    lock_location Array %d %d %d ;\n"  % (lockLocX, lockLocY, lockLocZ)+
"    lock_rotation Array %d %d %d ;\n"  % (lockRotX, lockRotY, lockRotZ)+
"    lock_rotation_w %s ; \n" % lkRotW +
"    lock_rotations_4d %s ; \n" % lkRot4 +
"    lock_scale Array %d %d %d  ; \n" % (lockScaleX, lockScaleY, lockScaleZ)+
"  end Posebone \n")
	return

#
#	addIkConstraint(fp, switch, flags, data, lockLoc, lockRot)
#	addActionConstraint(fp, switch, flags, data):
#	addCopyLocConstraint(fp, switch, flags, data):
#	addCopyRotConstraint(fp, switch, flags, data):
#	addCopyScaleConstraint(fp, switch, flags, data):
#	addCopyTransConstraint(fp, switch, flags, data):
#	addLimitRotConstraint(fp, switch, flags, data):
#	addLimitLocConstraint(fp, switch, flags, data):
#	addLimitScaleConstraint(fp, switch, flags, data):
#	addDampedTrackConstraint(fp, switch, flags, data):
#	addStretchToConstraint(fp, switch, flags, data):
#	addLimitDistConstraint(fp, switch, flags, data):
#

def addIkConstraint(fp, switch, flags, data, lockLoc, lockRot):
	global Mhx25
	name = data[0]
	subtar = data[1]
	chainlen = data[2]
	pole = data[3]
	(useLoc, useRot, useStretch) = data[4]
	inf = data[5]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)
	(lockLocX, lockLocY, lockLocZ) = lockLoc
	(lockRotX, lockRotY, lockRotZ) = lockRot

	if Mhx25:
		fp.write(
"    Constraint %s IK %s\n" % (name, switch) +
"      target Refer Object Human ;\n" +
"      pos_lock Array 1 1 1  ;\n" +
"      rot_lock Array 1 1 1  ;\n" +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      reference_axis 'BONE' ;\n" +
"      chain_count %d ;\n" % chainlen +
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
"      pole_target Refer Object Human ;\n")

		fp.write(
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp +
"      use_location %s ;\n" % useLoc +
"      use_rotation %s ;\n" % useRot +
"      use_stretch %s ;\n" % useStretch +
"      use_tail True ;\n" +
"      use_target True ;\n" +
"      weight 1 ;\n" +
"    end Constraint\n")

	else:
		fp.write("\t\tconstraint IKSOLVER %s 1.0 \n" % name)
		fp.write(
"\t\t\tCHAINLEN	int %d ; \n" % chainlen +
"\t\t\tTARGET	obj Human ; \n" +
"\t\t\tBONE	str %s ; \n" % subtar +
"\t\tend constraint\n")

	return

def addActionConstraint(fp, switch, flags, data):
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
"    Constraint %s ACTION %s\n" % (name, switch) +
"      target Refer Object Human ; \n"+
"      action Refer Action %s ; \n" % action+
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      frame_start %s ; \n" % sframe +
"      frame_end %d ; \n" % eframe+
"      influence %s ; \n" % inf)

	if channel[0:3] == 'LOC':
		fp.write(
"      maximum %.4f*theScale ; \n" % amax +
"      minimum %.4f*theScale ; \n" % amin)
	else:
		fp.write(
"      maximum %.4f ; \n" % amax +
"      minimum %.4f ; \n" % amin)
	
	fp.write(
"      owner_space '%s' ; \n" % ownsp +
"      is_proxy_local False ; \n"+
"      subtarget '%s' ; \n" % subtar +
"      target_space '%s' ; \n" % targsp +
"      transform_channel '%s' ;\n" % channel +
"    end Constraint \n")
	return

def addCopyRotConstraint(fp, switch, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	inf = data[2]
	(useX, useY, useZ) = data[3]
	(invertX, invertY, invertZ) = data[4]
	useOffs = data[5]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	if Mhx25:
		fp.write(
"    Constraint %s COPY_ROTATION %s\n" % (name, switch) +
"      target Refer Object Human ; \n"+
"      invert Array %d %d %d ; \n" % (invertX, invertY, invertZ)+
"      use Array %d %d %d  ; \n" % (useX, useY, useZ)+
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ; \n" % inf +
"      owner_space '%s' ; \n" % ownsp+
"      is_proxy_local False ; \n"+
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ; \n" % targsp+
"      use_offset %s ; \n" % useOffs +
"    end Constraint \n")

	else:
		copy = useX + 2*useY + 4*useZ
		fp.write(
"\t\tconstraint COPYROT %s 1.0 \n" % name +
"\t\t\tTARGET	obj Human ;\n" +
"\t\t\tBONE	str %s ; \n" % subtar +
"\t\t\tCOPY	hex %x ;\n" %  copy +
"\t\tend constraint\n")
	return

def addCopyLocConstraint(fp, switch, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	inf = data[2]
	(useX, useY, useZ) = data[3]
	(invertX, invertY, invertZ) = data[4]
	useOffs = data[5]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	if Mhx25:
		fp.write(
"    Constraint %s COPY_LOCATION %s\n" % (name, switch) +
"      target Refer Object Human ; \n"+
"      invert Array %d %d %d ; \n" % (invertX, invertY, invertZ)+
"      use Array %d %d %d  ; \n" % (useX, useY, useZ)+
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ; \n" % inf +
"      owner_space '%s' ; \n" % ownsp +
"      is_proxy_local False ; \n"+
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ; \n" % targsp+
"      use_offset %s ; \n" % useOffs +
"    end Constraint \n")

	else:
		fp.write(
"\t\tconstraint COPYLOC %s 1.0 \n" % name +
"\t\t\tTARGET	obj Human ;\n" +
"\t\t\tBONE	str %s ; \n" % subtar +
"\t\tend constraint\n")
	return

def addCopyScaleConstraint(fp, switch, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	inf = data[2]
	(useX, useY, useZ) = data[3]
	useOffs = data[4]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	fp.write(
"    Constraint %s COPY_SCALE %s\n" % (name, switch) +
"      target Refer Object Human ;\n" +
"      use Array %d %d %d  ; \n" % (useX, useY, useZ)+
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp +
"      use_offset %s ;\n" % useOffs +
"    end Constraint\n")
	return

def addCopyTransConstraint(fp, switch, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	inf = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)
	
	fp.write(
"    Constraint %s COPY_TRANSFORMS\n" % (name, switch) +
"      target Refer Object Human ;\n" +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp +
"    end Constraint\n")
	return


def addLimitRotConstraint(fp, switch, flags, data):
	global Mhx25
	name = data[0]
	(xmin, xmax, ymin, ymax, zmin, zmax) = data[1]
	(usex, usey, usez) = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)
	ltra = boolString(flags & C_LTRA == 0)
	
	if Mhx25:
		fp.write(	
"    Constraint %s LIMIT_ROTATION %s\n" % (name, switch) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence 1 ; \n"+
"      use_transform_limit %s ; \n" % ltra+
"      max_x %.6g ;\n" % xmax +
"      max_y %.6g ;\n" % ymax +
"      max_z %.6g ;\n" % zmax +
"      min_x %.6g ;\n" % xmin +
"      min_y %.6g ;\n" % ymin +
"      min_z %.6g ;\n" % zmin +
"      owner_space '%s' ; \n" % ownsp+
"      is_proxy_local False ; \n"+
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

def addLimitLocConstraint(fp, switch, flags, data):
	global Mhx25
	name = data[0]
	(xmin, xmax, ymin, ymax, zmin, zmax) = data[1]
	(useminx, usemaxx, useminy, usemaxy, useminz, usemaxz) = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)
	
	if Mhx25:
		fp.write(
"    Constraint %s LIMIT_LOCATION %s\n" % (name, switch) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence 1 ;\n" +
"      use_transform_limit True ;\n" +
"      max_x %s*theScale ;\n" % xmax +
"      max_y %s*theScale ;\n" % ymax +
"      max_z %s*theScale ;\n" % zmax +
"      min_x %s*theScale ;\n" % xmin +
"      min_y %s*theScale ;\n" % ymin +
"      min_z %s*theScale ;\n" % zmin +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      target_space '%s' ;\n" % targsp +
"      use_max_x %s ;\n" % usemaxx +
"      use_max_y %s ;\n" % usemaxy +
"      use_max_z %s ;\n" % usemaxz +
"      use_min_x %s ;\n" % useminx +
"      use_min_y %s ;\n" % useminy +
"      use_min_z %s ;\n" % useminz +
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

def addLimitScaleConstraint(fp, switch, flags, data):
	global Mhx25
	name = data[0]
	(xmin, xmax, ymin, ymax, zmin, zmax) = data[1]
	(usex, usey, usez) = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)
	
	if Mhx25:
		fp.write(
"    Constraint %s LIMIT_SCALE %s\n" % (name, switch) +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence 1 ;\n" +
"      use_transform_limit True ;\n" +
"      max_x %.6g ;\n" % xmax +
"      max_y %.6g ;\n" % ymax +
"      max_z %.6g ;\n" % zmax +
"      min_x %.6g ;\n" % xmin +
"      min_y %.6g ;\n" % ymin +
"      min_z %.6g ;\n" % zmin +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      target_space '%s' ;\n" % targsp +
"      use_max_x %s ;\n" % usex +
"      use_max_y %s ;\n" % usey +
"      use_max_z %s ;\n" % usez +
"      use_min_x %s ;\n" % usex +
"      use_min_y %s ;\n" % usey +
"      use_min_z %s ;\n" % usez +
"    end Constraint\n")
	return

def addDampedTrackConstraint(fp, switch, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	track = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	fp.write(
"    Constraint %s DAMPED_TRACK %s\n" % (name, switch) +
"      target Refer Object Human ;\n" +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence 1 ;\n" +
"      owner_space '%s' ;\n" % ownsp+
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"      track '%s' ;\n" % track + 
"    end Constraint\n")
	return

def addStretchToConstraint(fp, switch, flags, data):
	global Mhx25
	name = data[0]
	subtar = data[1]
	axis = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	if Mhx25:
		fp.write(
"    Constraint %s STRETCH_TO %s\n" % (name, switch) +
"      target Refer Object Human ;\n" +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      bulge 1 ;\n" +
"      influence 1 ;\n" +
"      keep_axis '%s' ;\n" % axis +
"      owner_space '%s' ;\n" % ownsp+
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"      volume 'NO_VOLUME' ;\n" +
"    end Constraint\n")

	else:
		fp.write(
"\t\tconstraint STRETCHTO %s 1.0 \n" % name +
"\t\t\tTARGET	obj Human ;\n" +
"\t\t\tBONE	str %s ;\n" % subtar +
"\t\t\tPLANE	hex 2 ;\n" +
"\t\tend constraint\n")
	return

def addLimitDistConstraint(fp, switch, flags, data):
	global Mhx25
	name = data[0]
	inf = data[1]
	subtar = data[2]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	if Mhx25:
		fp.write(
"    Constraint %s LIMIT_DISTANCE %s\n" % (name, switch) +
"      target Refer Object Human ;\n" +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      limit_mode 'LIMITDIST_INSIDE' ;\n" +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp+
"    end Constraint\n")

	else:
		fp.write(
"\t\tconstraint LIMITDIST %s 1.0 \n" % name +
"\t\t\tTARGET	obj Human ;\n" +
"\t\t\tBONE	str %s ;\n" % subtar +
"\t\tend constraint\n")
	return

def addChildOfConstraint(fp, switch, flags, data):
	global Mhx25
	# return
	name = data[0]
	subtar = data[1]
	inf = data[2]
	(locx, locy, locz) = data[3]
	(rotx, roty, rotz) = data[4]
	(scalex, scaley, scalez) = data[5]
	(ownsp, targsp, active, expanded) = constraintFlags(flags)

	if Mhx25:
		fp.write(
"    Constraint %s CHILD_OF %s\n" % (name, switch) +
"      target Refer Object Human ;\n" +
"      active %s ;\n" % active +
"      show_expanded %s ;\n" % expanded +
"      influence %s ;\n" % inf +
"      owner_space '%s' ;\n" % ownsp +
"      is_proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space '%s' ;\n" % targsp +
"      use_location_x %s ;\n" % locx +
"      use_location_y %s ;\n" % locy +
"      use_location_z %s ;\n" % locz +
"      use_rotation_x %s ;\n" % rotx +
"      use_rotation_y %s ;\n" % roty +
"      use_rotation_z %s ;\n" % rotz +
"      use_scale_x %s ;\n" % scalex +
"      use_scale_y %s ;\n" % scaley +
"      use_scale_z %s ;\n" % scalez +
"    end Constraint\n" +
"    bpyops constraint.childof_set_inverse(constraint='%s',owner='BONE') ;\n" % name)
	return


def constraintFlags(flags):
	ow = flags & C_OW_MASK
	if ow == 0:
		ownsp = 'WORLD'
	elif ow == C_OW_LOCAL:
		ownsp = 'LOCAL'
	elif ow == C_OW_LOCPAR:
		ownsp = 'LOCAL_WITH_PARENT'
	elif ow == C_OW_POSE:
		ownsp = 'POSE'

	tg = flags & C_TG_MASK
	if tg == 0:
		targsp = 'WORLD'
	elif tg == C_TG_LOCAL:
		targsp = 'LOCAL'
	elif tg == C_TG_LOCPAR:
		targsp = 'LOCAL_WITH_PARENT'
	elif tg == C_TG_POSE:
		targsp = 'POSE'

	active = boolString(flags & C_ACT == 0)
	expanded = boolString(flags & C_EXP)
	return (ownsp, targsp, active, expanded)

#
#	writeAction(fp, cond, name, action, lr, ikfk):
#	writeFCurves(fp, name, (x01, y01, z01, w01), (x21, y21, z21, w21)):
#

def writeAction(fp, cond, name, action, lr, ikfk):
	fp.write("Action %s %s\n" % (name,cond))
	if ikfk:
		iklist = ["IK", "FK"]
	else:
		iklist = [""]
	if lr:
		for (bone, quats) in action:
			rquats = []
			for (t,x,y,z,w) in rquats:
				rquats.append((t,x,y,-z,-w))
			for ik in iklist:
				writeFCurves(fp, "%s%s_L" % (bone, ik), quats)
				writeFCurves(fp, "%s%s_R" % (bone, ik), rquats)
	else:
		for (bone, quats) in action:
			for ik in iklist:
				writeFCurves(fp, "%s%s" % (bone, ik), quats)
	fp.write("end Action\n\n")
	return

def writeFCurves(fp, name, quats):
	n = len(quats)
	for index in range(4):
		fp.write("\n" +
"  FCurve pose.bones[\"%s\"].rotation_quaternion %d\n" % (name, index))
		for m in range(n):
			t = quats[m][0]
			x = quats[m][index+1]
			fp.write("    kp %d %.4g ;\n" % (t,x))
		fp.write(
"    extrapolation 'CONSTANT' ;\n" +
"  end FCurve \n")
	return

#
#	writeFkIkSwitch(fp, drivers)
#	writeDrivers(fp, cond, drivers):
#	writeDriver(fp, cond, drvdata, extra, channel, index, coeffs, variables):
#

def writeFkIkSwitch(fp, drivers):
	for (bone, cond, cnsFK, cnsIK, targ, channel, mx) in drivers:
		if PanelWorks:
			cnsData = ("ik", 'SINGLE_PROP', [('Human', targ)])
		else:
			cnsData = ("ik", 'TRANSFORMS', [('Human', targ, channel, C_LOCAL)])
		for cnsName in cnsFK:
			writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsName), -1, (mx,-mx), [cnsData])
		for cnsName in cnsIK:
			writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsName), -1, (0,mx), [cnsData])

# 'BrowsMidDown' : [('PBrows', 'LOC_Z', (0,K), 0, fullScale)]

def writeShapeDrivers(fp, drivers):
	for (shape, vlist) in drivers.items():
		drvVars = []
		(targ, channel, coeff) = vlist
		drvVars.append( (targ, 'TRANSFORMS', [('Human', targ, channel, C_LOCAL)]) )
		writeDriver(fp, 'toggle&T_Face', 'AVERAGE', "", "keys[\"%s\"].value" % (shape), -1, coeff, drvVars)
	return

def writeFKIKShapeDrivers(fp, drivers):
	for (shape, data) in drivers.items():
		(scale, fkik, fklist, iklist) = data
		drvVars = []
		vnames = ['x', 'fk', 'ik']
		vlists = [fkik, fklist, iklist]
		for n in range(3):
			vname = vnames[n]
			(targ, channel, coeff) = vlists[n]
			drvVars.append( (vname, 'TRANSFORMS', [('Human', targ, channel, C_LOCAL)]) )
		writeDriver(fp, 'toggle&T_Shape', ('SCRIPTED', '(x*ik+(1-x)*fk)/%.4f' % scale), "", "keys[\"%s\"].value" % (shape), -1, coeff, drvVars)
	return

def writeDrivers(fp, cond, drivers):
	for drv in drivers:
		(bone, typ, name, index, coeffs, variables) = drv
		if typ == 'INFL':
			writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, name), index, coeffs, variables)
		elif typ == 'ROTE':
			writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].rotation_euler" % bone, index, coeffs, variables)
		elif typ == 'ROTQ':
			writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].rotation_quaternion" % bone, index, coeffs, variables)
		elif typ == 'LOC':
			writeDriver(fp, cond, 'AVERAGE', "*theScale", "pose.bones[\"%s\"].location" % bone, index, coeffs, variables)
		elif typ == 'SCALE':
			writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].scale" % bone, index, coeffs, variables)
		else:
			print drv
			raise NameError("Unknown driver type %s" % typ)

def writeDriver(fp, cond, drvdata, extra, channel, index, coeffs, variables):
	loc = False
	try:
		(drvtype, expr) = drvdata
	except:
		drvtype = drvdata

	fp.write("\n"+
"    FCurve %s %d %s\n" % (channel, index, cond) +
"      Driver %s\n" % drvtype )

	if drvtype == 'SCRIPTED':
		fp.write("        expression '%s' ;\n" % expr)

	for (var, typ, targets) in variables:
		fp.write("        DriverVariable %s %s\n" % (var,typ))

		if typ == 'TRANSFORMS':
			for (targ, boneTarg, ttype, flags) in targets:
				if ttype[0:3] == 'LOC':
					loc = True
				local = boolString(flags & C_LOCAL)
				fp.write(
"          Target %s OBJECT\n" % targ +
"            transform_type '%s' ;\n" % ttype +
"            bone_target '%s' ;\n" % boneTarg +
"            use_local_space_transform %s ;\n" % local +
"          end Target\n")

		elif typ == 'SINGLE_PROP':
			for (targ, boneTarg) in targets:
				fp.write(
"          Target %s OBJECT\n" % targ +
"            data_path '%s' ;\n" % boneTarg +
"          end Target\n")

		else:
			raise NameError("Unknown driver type %s" % typ)

		fp.write("        end DriverVariable\n")

	fp.write(
"        show_debug_info True ;\n" +
"      end Driver\n")

	if drvtype == 'AVERAGE':
		fp.write(
"      FModifier GENERATOR \n" +
"        active False ;\n" +
"        use_additive False ;\n")

		(a0,a1) = coeffs
		if loc:
			fp.write("        coefficients Array %s %s*One%s ;\n" % (a0,a1,extra))
		else:
			fp.write("        coefficients Array %s %s%s ;\n" % (a0,a1,extra))

		fp.write(
"        show_expanded True ;\n" +
"        mode 'POLYNOMIAL' ;\n" +
"        mute False ;\n" +
"        poly_order 1 ;\n" +
"      end FModifier\n")

	fp.write(
"      extrapolation 'CONSTANT' ;\n" +
"      lock False ;\n" +
"      select False ;\n" +
"    end FCurve\n")

	return

#
#	setupRig(obj):
#	writeAllArmatures(fp)	
#	writeAllPoses(fp)	
#	writeAllActions(fp)	
#	writeAllDrivers(fp)	
#	writeAllProcesses(fp):
#
import rig_joints_25, rig_body_25, rig_arm_25, rig_finger_25, rig_leg_25, rig_toe_25, rig_face_25, rig_panel_25

def setupRig(obj):
	newSetupJoints(obj, 
		rig_joints_25.DeformJoints +
		rig_body_25.BodyJoints +
		rig_arm_25.ArmJoints +
		rig_finger_25.FingerJoints +
		rig_leg_25.LegJoints +
		#rig_toe_25.ToeJoints +
		rig_face_25.FaceJoints +
		rig_panel_25.PanelJoints,
		
		rig_body_25.BodyHeadsTails +
		rig_arm_25.ArmHeadsTails +
		rig_finger_25.FingerHeadsTails +
		rig_leg_25.LegHeadsTails +
		#rig_toe_25.ToeHeadsTails +
		rig_face_25.FaceHeadsTails +
		rig_panel_25.PanelHeadsTails)
	return
	
def writeAllArmatures(fp):
	writeArmature(fp, 
		rig_body_25.BodyArmature +
		rig_arm_25.ArmArmature +
		rig_finger_25.FingerArmature +
		rig_leg_25.LegArmature +
		#rig_toe_25.ToeArmature +
		rig_face_25.FaceArmature +
		rig_panel_25.PanelArmature, True)
	return

def writeAllPoses(fp):
	writePoses(fp, 
		rig_body_25.BodyPoses +
		rig_arm_25.ArmPoses +
		rig_finger_25.FingerPoses +
		rig_leg_25.LegPoses +
		#rig_toe_25.ToePoses +
		rig_face_25.FacePoses +
		rig_panel_25.PanelPoses)
	return
	
def writeAllActions(fp):
	#rig_arm_25.ArmWriteActions(fp)
	#rig_leg_25.LegWriteActions(fp)
	#rig_finger_25.FingerWriteActions(fp)
	return

def writeAllDrivers(fp):
	writeFkIkSwitch(fp, rig_arm_25.ArmDrivers)
	writeFkIkSwitch(fp, rig_leg_25.LegDrivers)
	rig_panel_25.FingerWriteDrivers(fp)
	rig_face_25.FaceWriteDrivers(fp)
	return

def writeAllProcesses(fp):
	#return
	
	fp.write("  EditMode ;\n")
	parents = rig_arm_25.ArmParents + rig_leg_25.LegParents
	for (bone, parent) in parents:
		fp.write("  Reparent %s %s ;\n" % (bone, parent))

	fp.write("  PoseMode ;\n")
	processes = rig_arm_25.ArmProcess + rig_leg_25.LegProcess
	for (bone, axis, angle) in processes:
		fp.write("  Bend %s %s %.6g ;\n" % (bone, axis, angle))
	fp.write("  EditMode ;\n")
	fp.write("  ObjectMode ;\n")

	fp.write("  Apply ;\n")

	fp.write("  EditMode ;\n")
	snaps = rig_arm_25.ArmSnaps + rig_leg_25.LegSnaps
	for (bone, target, rev) in snaps:
		fp.write("  Snap %s %s %s ;\n" % (bone, target, rev))

	fp.write("  ObjectMode ;\n")
	fp.write("  EditMode ;\n")
	rolls = rig_arm_25.ArmRolls + rig_leg_25.LegRolls
	for (bone, roll) in rolls:
		fp.write("  Roll %s %.4f ;\n" % (bone, roll))
	
	fp.write("  ObjectMode ;\n")

	return

def reapplyArmature(fp, name):
	fp.write("\n" +
"  Object %s  \n" % name +
"    Modifier Armature ARMATURE \n" +
"      show_expanded True ; \n" +
"      object Refer Object Human ; \n" +
"      use_bone_envelopes False ; \n" +
"      use_vertex_groups True ; \n" +
"    end Modifier \n" +
"  end Object\n")




