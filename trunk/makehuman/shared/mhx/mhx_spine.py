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
Code for rigging a spine

"""

import aljabr, mh2mhx, math, mhx_rig
from mhx_rig import *

S_BONE = 1
S_CURVE = 2
S_MESHCURVE = 3

SPINE = S_BONE

#
#	addSpine(fp, name, hooks):
#

def addSpine(fp, name, hooks):
	if SPINE == S_BONE:
		return
	elif SPINE == S_CURVE:
		addCurve(fp, name, hooks)
	elif SPINE == S_MESHCURVE:
		addHookEmpty(fp, hooks[1])
		addHookEmpty(fp, hooks[-1])
		for n in range(1, len(hooks)):
			addHookCube(fp, hooks[n], hooks[n-1])
			addLattice(fp, name, hooks)
			addMeshCurve(fp, name, hooks)

	return 

#
#	addHookCube(fp, name, parent):
#

def addHookCube(fp, name, parent):
	cubename = mh2mhx.theHuman+name+'Cube'
	mhx_rig.setupCubeMesh(fp, cubename, 0.2, 0)
	fp.write("\n" +
"Object %s MESH %s \n" % (cubename, cubename) +
"  layers Array 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  ;\n" +
"  parent Refer Object %s ;\n" % mh2mhx.theHuman +
"  parent_bone \"%s\" ;\n" % parent +
"  parent_type 'BONE' ;\n" +
"  show_x_ray True ;\n" +
"end Object\n")

#
#	addHookEmpty(fp, hook):
#

def addHookEmpty(fp, hook):
	fp.write("\nObject %s%sEmpty EMPTY None\n" % (mh2mhx.theHuman, hook))
	(x,y,z) = mhx_rig.rigHead[hook]
	fp.write(
"    location (%.4f,%.4f,%.4f) ;\n" % (x,-z,y) +
"  layers Array 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  ;\n" +
"  parent Refer Object %s ;\n" % mh2mhx.theHuman +
"end Object\n")
	return

#
#	addLattice(fp, name, hooks):
#

def addLattice(fp, name, hooks):
	latname = "%s%sLattice" % (mh2mhx.theHuman, name)

	fp.write(
"\nLattice %s %s \n" % (latname, latname) +
"  interpolation_type_u 'KEY_BSPLINE' ;\n" +
"  interpolation_type_v 'KEY_BSPLINE' ;\n" +
"  interpolation_type_w 'KEY_BSPLINE' ;\n" +
"  points_u 1 ;\n" +
"  points_v 1 ;\n" +
"  points_w %d ;\n" % (len(hooks)-1) +
"  Points\n")
	for hook in hooks[1:]:
		(x,y,z) = mhx_rig.rigHead[hook]
		fp.write("    pt %.4f %.4f %.4f ;\n" % (x,-z,y))
	fp.write(
"  end Points\n" +
"end Lattice\n" +
"\n" +
"Object %s LATTICE %s \n" % (latname, latname) +
"  layers Array 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  ;\n")

	for n in range(len(hooks)-1):
		addHookModifier(fp, hooks[n+1], 'Cube', n, 'LATTICE')

	fp.write(
"  parent Refer Object %s ;\n" % mh2mhx.theHuman +
"end Object\n")

#
#	addMeshCurve(fp, name, hooks):
#

def addMeshCurve(fp, name, hooks):
	addHookEmpty(fp, hooks[0])
	addHookEmpty(fp, hooks[-1])

	mename = "%s%sMesh" % (mh2mhx.theHuman, name)

	fp.write("Mesh %s %s\n  Verts\n" % (mename, mename))
	for hook in hooks:
		(x,y,z) = mhx_rig.rigHead[hook]
		fp.write("    v %.4f %.4f %.4f ;\n" % (x,-z,y))

	fp.write('  end Verts\n  Edges\n')

	npoints = len(hooks)-1
	for n in range(npoints-1):
		fp.write('    e %d %d ;\n' % (n, n+1))
	fp.write("  end Edges\n")

	for n in range(npoints):
		fp.write(
"  VertexGroup Spine%d\n" % n +
"    wv %d 1 ;\n" % n +
"  end VertexGroup\n")

	fp.write("  VertexGroup Lattice\n")
	for n in range(2,npoints):
		fp.write("    wv %d 1.0 ;\n" % n)
	fp.write(
"  end VertexGroup\n" +
"end Mesh\n" +
"\n" +
"Object %s MESH %s\n" % (mename, mename) +
"  layers Array 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  ;\n")

	latname = "%s%sLattice" % (mh2mhx.theHuman, name)
	addLatticeModifier(fp, latname, 'Lattice')
	addHookModifier(fp, hooks[1], 'Empty', 0, 'MESH')
	addHookModifier(fp, hooks[npoints], 'Empty', npoints-1, 'MESH')

	fp.write(
"  parent Refer Object %s ;\n" % mh2mhx.theHuman +
"end Object")

def addLatticeModifier(fp, latname, vgroup):
	fp.write(
"    Modifier Lattice LATTICE\n" +
"      object Refer Object %s ;\n" % latname +
"      use_apply_on_spline False ;\n" +
"      vertex_group '%s' ;\n" % vgroup +
"    end Modifier\n")
	return

#
#	addHookModifier(fp, hook, suffix, index, typ):
#

def addHookModifier(fp, hook, suffix, index, typ):
	fp.write(
"  Modifier %s HOOK\n" % hook +
"    falloff 0 ;\n" +
"    force 1 ;\n")
	if suffix:
		fp.write("    object Refer Object %s%s%s ;\n" % (mh2mhx.theHuman, hook, suffix))
	else:
		fp.write(
"    object Refer Object %s ;\n" % mh2mhx.theHuman +
"    subtarget '%s' ;\n" % hook)
	fp.write(
"    show_expanded False ;\n" +
"    use_apply_on_spline False ;\n" +
"    HookAssignNth %s %d ;\n" % (typ, index) +
"  end Modifier\n")
	return

#
#	addCurve(fp, name, hooks):
#

def addCurve(fp, name, hooks):
	cuname = "%s%sCurve" % (mh2mhx.theHuman, name)
	npoints = len(hooks)
	count = npoints-1
	order = 3

	fp.write("\n" +
"Curve %s %s\n" % (cuname,cuname) +
"  bevel_depth 0 ;\n" +
"  bevel_resolution 0 ;\n" +
"  dimensions '3D' ;\n" +
"  offset 0 ;\n" +
"  path_duration 100 ;\n" +
"  render_resolution_u 0 ;\n" +
"  render_resolution_v 0 ;\n" +
"  resolution_u 12 ;\n" +
"  resolution_v 12 ;\n" +
"  show_handles True ;\n" +
"  twist_mode 'MINIMUM' ;\n" +
"  twist_smooth 0 ;\n" +
"  use_fill_back True ;\n" +
"  use_fill_deform True ;\n" +
"  use_fill_front True ;\n" +
"  use_path True ;\n" +
"  use_path_follow False ;\n" +
"  use_radius True ;\n" +
"  use_stretch False ;\n" +
"  use_time_offset False ;\n" +
"  use_uv_as_generated False ;\n" +
"  Spline NURBS %d 1\n" % count +
"    order_u %d ;\n" % order +
"    order_v 0 ;\n")

	for hook in hooks:
		pt =  mhx_rig.rigHead[hook]
		fp.write("    pt (%.4f,%.4f,%4f,1) ;\n" % (pt[0], -pt[2], pt[1]) )
	'''
	p0 = mhx_rig.rigHead[hooks[0]]
	pn = mhx_rig.rigHead[hooks[-1]]
	h = aljabr.vsub(pn, p0)
	fac = 1.0/(npoints-1)
	dh = [h[0]*fac, h[1]*fac, h[2]*fac]
	pt = p0
	print(p0, pn, h, dh)
	for n in range(npoints):
		print(pt)
		fp.write("    pt (%.4f,%.4f,%4f,1) ;\n" % (pt[0], -pt[2], pt[1]) )
		pt = aljabr.vadd(pt, dh)
	'''

	fp.write(
"    radius_interpolation 'BSPLINE' ;\n" +
"    resolution_u 12 ;\n" +
"    resolution_v 12 ;\n" +
"    tilt_interpolation 'BSPLINE' ;\n" +
"    use_bezier_u True ;\n" +
"    use_bezier_v True ;\n" +
"    use_cyclic_u False ;\n" +
"    use_cyclic_v False ;\n" +
"    use_endpoint_u False ;\n" +
"    use_endpoint_v False ;\n" +
"    use_smooth True ;\n" +
"  end Spline\n" +
"end Curve\n" +
"\n" +
"Object %s CURVE %s\n" % (cuname,cuname) +
"  layers Array 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  ;\n")

	for n,hook in enumerate(hooks):
		addHookModifier(fp, hook, None, n, 'CURVE')

	fp.write(
"  parent Refer Object %s ;\n" % mh2mhx.theHuman +
"  show_x_ray True ;\n" +
"end Object\n")

#
#	spineDeform(fp, bone, name, flags, index, count, customShape):
#

def spineDeform(fp, bone, name, flags, index, count, customShape):
	if SPINE == S_BONE:
		mhx_rig.copyDeform(fp, bone, 0, mhx_rig.U_LOC + mhx_rig.U_ROT, customShape)
		return

	fp.write("\n  Posebone %s %s \n" % (bone, True))
	rotMode = mhx_rig.rotationMode(flags)
	fp.write("  rotation_mode '%s' ;\n" % rotMode)
	if customShape:
		fp.write("    custom_shape Refer Object %s ; \n" % customShape)


	if SPINE == S_CURVE:
		cuname = "%s%sCurve" % (mh2mhx.theHuman, name)
		if count:
			mhx_rig.addSplineIkConstraint(fp, '', flags, 1, ['SplineIK', cuname, count] )
		fp.write("  end Posebone\n")
		return

	if SPINE == S_MESHCURVE:
		"""
		mhx_rig.addChildOfConstraint(fp, C_OW_POSE+C_TG_WORLD, inf, 
			[('ChildOf', C_OW_POSE+C_TG_WORLD, inf, ['Shoulders', 'Shoulders', (0,0,0), (0,0,1), (0,0,0)])

		mhx_rig.addChildOfConstraint(fp, C_OW_POSE+C_TG_WORLD, inf, 
			('ChildOf', C_OW_POSE+C_TG_WORLD, inf, ['Spine1', 'Spine1', (0,0,0), (0,0,1), (0,0,0)])

		mhx_rig.addCopyScaleConstraint(fp, 'CopyScale', 0, 0.2, ['Scale', 'CTR_Belly_Scale', (1,1,1), False])
		"""
		mename = "%s%sMesh" % (mh2mhx.theHuman, name)
		fp.write(
"    Constraint Loc COPY_LOCATION True\n" +
"      target Refer Object %s ;\n" % mename +
"      subtarget 'Spine%d' ;\n" % index +
"      target_space 'WORLD' ;\n" +
"    end Constraint\n" +
"    Constraint Stretch STRETCH_TO True\n" +
"      target Refer Object %s ;\n" % mename +
"      keep_axis 'PLANE_X' ;\n" +
"      owner_space 'WORLD' ;\n" +
"      subtarget 'Spine%d' ;\n" % (index+1) +
"      target_space 'WORLD' ;\n" +
"      volume 'VOLUME_XZX' ;\n" + 
"    end Constraint\n")
		fp.write("  end Posebone\n")
		return


