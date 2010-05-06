#
#	Utility for creating MakeHuman bone definitions.
#

import bpy

BoneLayers = [
	'L_FK', 'L_TORSO', 'L_ARMIK', 'L_ARMFK',
	'L_LEGIK', 'L_LEGFK', 'L_HANDIK', 'L_HANDFK', 
	'L_PANEL', 'L_TOE', 'L_HEAD', 'L_NONE',
	'L_NONE', 'L_ROOT', 'L_DEFORM', 'L_HELP'
]

#
#	writeBones(character, fp):
#

def writeBones(character, fp):
	ob = bpy.data.objects['HumanRig']
	bpy.context.scene.objects.active = ob
	amt = ob.data

	bpy.ops.object.mode_set(mode='EDIT')
	bones = amt.edit_bones.values()

	# List name of deform bones, to modify vertexgroup names
	fp.write("%sDeform = {\n" % character)
	for b in bones:
		(bType, bName) = extractName(b)
		pad = doPad(len(bName), 4)
		if bType == 'DEF':
			fp.write("\t'%s':%s'%s',\n" % (bName, pad, b.name.replace(' ','_')))
	fp.write("}\n\n")
	
	# List symbolic joint locations
	joints = {}
	fp.write("%sJoints = [\n" % character)
	for b in bones:
		(bType, bName) = extractName(b)
		pad = doPad(len(bName), 6)
		writeJoint(fp, bName+"_head", b.head, pad, joints)
		writeJoint(fp, bName+"_tail", b.tail, pad, joints)
	fp.write("]\n\n")

	# List symbolic names for heads and tails
	fp.write("%sHeadsTails = [\n" % character)
	for b in bones:
		print("Bone", b.name, b.head, b.tail)
		(bType, bName) = extractName(b)
		pad = doPad(len(bName), 3)
		hfound = findJoint(bName+"_head", None, joints)
		tfound = findJoint(bName+"_tail", None, joints)
		if hfound == None or tfound == None:
			fp.write("Bone %s %s %s" % ( b.name, b.head, b.tail))
			fp.close()
			raise NameError("ht", hfound, tfound)
		(hname,hx) = hfound
		(tname,tx) = tfound
		fp.write("\t('%s',%s'%s', '%s'),\n" % (b.name.replace(' ','_'), pad, hname, tname))
	fp.write("]\n\n")

	# List bone in armature
	# (bone, roll, parent, flags, layers, bbones)
	#
	fp.write("%sArmature = [\n" % character)
	for b in bones:
		pad = doPad(len(b.name), 3)
		fp.write("\t('%s',%s" % (b.name.replace(' ','_'), pad))
		if b.roll < 1e-2 and b.roll > -1e-2:
			fp.write("0.0, ")
		else:
			fp.write("%.6g, " % b.roll)
		if b.parent:
			fp.write("'%s', " % b.parent.name.replace(' ','_'))
		else:
			fp.write("None, ")

		# Flags
		flags = ""
		if b.deform:
			flags += "+F_DEF"
		if b.connected:
			flags += "+F_CON"
		if b.draw_wire:
			flags += "+F_WIR"
		if b.restrict_select:
			flags += "+F_RES"
		if not b.inherit_scale:
			flags += "+F_NOSCALE"
		if not b.local_location:
			flags += "+F_GLOC"
		if b.locked:
			flags += "+F_LOCK"
		if b.hidden:
			flags += "+F_HID"
		if not b.cyclic_offset:
			flags += "+F_NOCYC"

		if len(flags) > 0:
			fp.write("%s, " % flags[1:])
		else:
			fp.write("0, ")

		# Layers
		'''
		(bType, bName) = extractName(b)
		if bType == 'MCP':
			fp.write("L_HELP, ")
		elif bType == 'DEF':
			fp.write("L_DEF, ")
		elif bType == 'ORG':
			fp.write("L_SKEL, ")
		elif bType == 'VIS':
			fp.write("L_MAIN, ")
		else:
			fp.write("L_PANEL, ")
		'''
		c = ""
		for n,name in enumerate(BoneLayers):
			if b.layer[n]:
				fp.write("%s%s" % (c, name))
				c = "+"
		if c == "":
			fp.write("0, ")
		else:
			fp.write(", ")		

		'''
		x = 0
		bit = 1
		for lay in b.layer:
			if lay:
				x += bit
			bit <<= 1
		fp.write(", 0x%x, " % x)
		'''

		# BBones
		fp.write("(%d,%g,%d) ),\n" % (b.bbone_in, b.bbone_out, b.bbone_segments))

	fp.write("]\n\n")

	#
	# Posebones
	#
	bpy.ops.object.mode_set(mode='POSE')
	pbones = ob.pose.bones.values()
	fp.write(
"def %sWritePoses(fp):\n" % character +
"\tglobal boneGroups\n" +
"\tboneGroups = {}\n\n")

	# addPoseBone(fp, bone, customShape, boneGroup, pb.lockLoc, pb.lockRot, pb.lockScale, flags, constraints)
	for pb in pbones:
		fp.write("\taddPoseBone(fp, '%s', " % pb.name)
		if pb.custom_shape:
			fp.write("'%s', " % pb.custom_shape.name)
		else:
			fp.write("None, ")
		if pb.bone_group:
			fp.write("'%s', " % pb.bone_group.name)
		else:
			fp.write("None, ")
		fp.write("(%d,%d,%d), " % (pb.lock_location[0], pb.lock_location[1], pb.lock_location[2]))
		fp.write("(%d,%d,%d), " % (pb.lock_rotation[0], pb.lock_rotation[1], pb.lock_rotation[2]))
		fp.write("(%d,%d,%d), " % (pb.lock_scale[0], pb.lock_scale[1], pb.lock_scale[2]))
		fp.write("(%d,%d,%d), " % (pb.ik_dof_x, pb.ik_dof_y, pb.ik_dof_z))

		# Flags
		flags = ""
		if pb.lock_rotations_4d:
			flags += "+P_LKROT4"
		if pb.lock_rotation_w:
			flags += "+P_LKROTW"
		if pb.ik_lin_control:
			flags += "+P_IKLIN"
		if pb.ik_rot_control:
			flags += "+P_IKROT"

		if len(flags) > 0:
			fp.write(flags[1:])
		else:
			fp.write("0")

		if list(pb.constraints):
			c = ",\n\t\t["
			for cns in pb.constraints:
				fp.write(c)
				writeConstraint(fp, cns)
				c = ",\n\t\t "
			fp.write("])\n\n")
		else:
			fp.write(", [])\n\n")
	fp.write("\treturn\n")

	#
	#	Animation data
	#
	
	bpy.ops.object.mode_set(mode='OBJECT')
	if ob.animation_data == None:
		return
	fp.write("\n%sDrivers = [\n" % character)
	for fcu in ob.animation_data.drivers:
		try:
			drv = fcu.driver
		except:
			pass
		words = fcu.data_path.split('"')
		bone = words[1]
		typ = ("unk", len(words))
		if len(words) == 3:
			typ = words[2].split('.')[1]
			if typ == 'rotation_euler':
				typ = 'ROTE'
			elif typ == 'rotation_quaternion':
				typ = 'ROTQ'
			elif typ == 'location':
				typ = 'LOC'
			name = None
		elif len(words) == 5:
			if words[4] == ']':
				typ = "PROP"
				name = words[3]
			elif words[4] == '].influence':
				typ = 'INFL'
				name = words[3]
			
		fp.write("  ('%s', '%s', " % (bone, typ))
		if name:
			fp.write("'%s', " % name.replace(' ','_'))
		else:
			fp.write("None, ")
		fp.write("%d, '%s', [" % (fcu.array_index, drv.expression))
		for var in drv.variables:
			fp.write("\n\t\t('%s', '%s', [" % (var.name, var.type))
			for targ in var.targets:
				if targ.use_local_space_transforms:
					flags = 'C_LOCAL'
				else:
					flags = '0'
				fp.write("('%s', '%s', '%s', %s) " % (targ.data_path, targ.bone_target, targ.transform_type, flags))
			fp.write("]),")
		fp.write("]),\n")
	fp.write("]\n\n")

	return

#
#	findJoint(jName, x, joints):
#	writeJoint(fp, jName, loc, joints):
#

def findJoint(jName, x, joints):
	try:
		found = joints[jName]
		return found
	except:
		pass
	if x == None:
		raise NameError("Cannot find joint "+jName)
	for (jy, y) in joints.values():
		if (x-y).length < 1e-3:
			return (jy, y)
	return None

def writeJoint(fp, jName, loc, pad, joints):
	found = findJoint(jName, loc, joints)
	if found:
		joints[jName] = found
	else:
		fp.write("\t('%s',%s'x', [%.6f, %.6f, %.6f]),\n" % (jName, pad, loc[0], loc[1], loc[2]))
		joints[jName] = (jName, loc)
	return

#
#
#
def addToSpace(cns, cond, flag):
	try:
		res = eval("cns."+cond)
	except:
		res = False
	if res:
		return flag
	else:
		return ""

def writeConstraint(fp, cns):
	typ = cns.type

	# Owner and target spaces
	space = "0"
	space += addToSpace(cns, "owner_space == 'LOCAL'", '+C_OWNER') 
	space += addToSpace(cns, "target_space == 'LOCAL'", '+C_TARGET') 
	space += addToSpace(cns, "active == False", '+C_ACT') 
	space += addToSpace(cns, "expanded == False", '+C_EXP') 
	space += addToSpace(cns, "limit_transform == False", '+C_LTRA') 
	
	if typ == 'IK':
		fp.write("('IK', %s, ['%s', %d, " % (space, cns.subtarget, cns.chain_length))
		if cns.pole_target:
			fp.write("(%.6g, '%s'), " % (cns.pole_angle, cns.pole_subtarget))
		else:
			fp.write("None, ")
		fp.write("(%s, %s)])" % (cns.use_position, cns.use_rotation))

	elif typ == 'ACTION':
		fp.write("('Action', %s, ['%s', '%s', '%s', %s, (%.6g, %.6g)])" % (space, cns.action.name.replace(' ','_'), cns.subtarget,
			cns.transform_channel, (cns.start_frame, cns.end_frame), cns.minimum, cns.maximum))

	elif typ == 'COPY_LOCATION':
		fp.write("('CopyLoc', %s, ['%s', '%s', %.6g, " % (space, cns.name.replace(' ','_'), cns.subtarget, cns.influence))
		fp.write("(%d,%d,%d), " % (cns.use_x, cns.use_y, cns.use_z))
		fp.write("(%d,%d,%d)])" % (cns.invert_x, cns.invert_y, cns.invert_z))

	elif typ == 'COPY_ROTATION':
		fp.write("('CopyRot', %s, ['%s', '%s', %.6g, " % (space, cns.name.replace(' ','_'), cns.subtarget, cns.influence))
		fp.write("(%d,%d,%d), " % (cns.use_x, cns.use_y, cns.use_z))
		fp.write("(%d,%d,%d)])" % (cns.invert_x, cns.invert_y, cns.invert_z))

	elif typ == 'COPY_SCALE':
		fp.write("('CopyScale', %s, ['%s', '%s', %.6g, " % (space, cns.name.replace(' ','_'), cns.subtarget, cns.influence))
		fp.write("(%d,%d,%d)])" % (cns.use_x, cns.use_y, cns.use_z))

	elif typ == 'COPY_TRANSFORMS':
		fp.write("('CopyTrans', %s, ['%s', '%s', %.6g])" % (space, cns.name.replace(' ','_'), cns.subtarget, cns.influence))

	elif typ == 'LIMIT_ROTATION':
		fp.write("('LimitRot', %s, ['%s', " % (space, cns.name.replace(' ','_')))
		fp.write("(%.6g,%.6g, %.6g,%.6g, %.6g,%.6g), " % 
			(cns.minimum_x, cns.maximum_x, cns.minimum_y, cns.maximum_y, cns.minimum_z, cns.maximum_z))
		fp.write("(%d,%d,%d)])" % (cns.use_limit_x, cns.use_limit_y, cns.use_limit_z))

	elif typ == 'LIMIT_LOCATION':
		fp.write("('LimitLoc', %s, ['%s', " % (space, cns.name.replace(' ','_')))
		fp.write("(%.6g,%.6g, %.6g,%.6g, %.6g,%.6g), " %
			(cns.minimum_x, cns.maximum_x, cns.minimum_y, cns.maximum_y, cns.minimum_z, cns.maximum_z))
		fp.write("(%d,%d,%d,%d,%d,%d)])" % 
			(cns.use_minimum_x, cns.use_maximum_x, cns.use_minimum_y, cns.use_maximum_y, cns.use_minimum_z, cns.use_maximum_z))

	elif typ == 'DAMPED_TRACK':
		fp.write("('DampedTrack', %s, ['%s', '%s', '%s'])" % (space, cns.name.replace(' ','_'), cns.subtarget, cns.track))

	elif typ == 'STRETCH_TO':
		fp.write("('StretchTo', %s, ['%s', '%s', '%s'])" % (space, cns.name.replace(' ','_'), cns.subtarget, cns.keep_axis))

	elif typ == 'LIMIT_DISTANCE':
		fp.write("('Limit', %s, ['%s', '%s'])" % (space, cns.name.replace(' ','_'), cns.subtarget))
	else:
		fp.write(typ)
		raise NameError("Unknown constraint type %s" % typ)

	return
		


def extractName(b):
	boneType = b.name[:3]
	boneName = b.name[4:]
	#boneType = 0
	print(b.name, boneType, boneName)
	if boneType == 'MCH' or boneType == 'DEF' or boneType == 'ORG' or boneType == 'VIS':
		return (boneType, boneName)
	else:
		return ('GEN', b.name)

def doPad(m, n):
	if m > n+16:
		return '\t'
	elif m > n+8:
		return '\t\t'
	elif m > n:
		return '\t\t\t'
	else:
		return '\t\t\t\t'



def writeBoneFile(character, fname):
	print("Bone file %s for character %s" % (fname, character))
	fp = open(fname, "w")
	fp.write(
"#\n" +
"#	Bone definitions for %s rig\n" % character +
"#\n" +
"import gobo_bones\n" +
"from gobo_bones import *\n")

	writeBones(character, fp)
	fp.close()
	print("Bone file %s written" % fname)
	return

#writeBoneFile('Classic', '/home/thomas/svn/makehuman/mh_plugins/classic_bones.py')
#writeBoneFile("Sintel", "/home/thomas/myblends/sintel/sintel_bones-raw.py")
#writeBoneFile("Gobo", "/home/thomas/myblends/gobo/gobo_bones-raw.py")
writeBoneFile('Test', '/home/thomas/myblends/test.py')


