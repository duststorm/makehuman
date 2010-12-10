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
MakeHuman to MHX (MakeHuman eXchange format) exporter. MHX files can be loaded into
Blender by mhx_import.py.

TO DO

"""

MAJOR_VERSION = 1
MINOR_VERSION = 0
splitLeftRight = True
BODY_LANGUAGE = True

import module3d, aljabr, mh, files3d, mh2bvh, os

import sys
mhxPath = os.path.realpath('./shared/mhx')
if mhxPath not in sys.path:
	sys.path.append(mhxPath)
import mh2proxy, mhxbones, mhx_rig, rig_panel_25, rig_arm_25, rig_leg_25, rig_body_25

#
#	exportMhx(obj, filename):
#
def exportMhx(obj, filename):	
	(name, ext) = os.path.splitext(filename)
	
	filename = name+"-24"+ext
	#print("Writing MHX 2.4x file " + filename )
	fp = open(filename, 'w')
	exportMhx_24(obj, fp)
	fp.close()
	#print("MHX 2.4x file %s written" % filename)
	
	filename = name+"-25"+ext
	#print("Writing MHX 2.5x file " + filename )
	fp = open(filename, 'w')
	exportMhx_25(obj, "rig", fp)
	fp.close()
	#print("MHX 2.5x file %s written" % filename)

	return

#
#	exportMhx_24(obj,fp):
#

def exportMhx_24(obj, fp):
	fp.write(
"# MakeHuman exported MHX\n" +
"# www.makehuman.org\n" +
"MHX 1 0 ;\n")

	fp.write(
"#if Blender25\n"+
"  error This file can not be opened in Blender 2.5x. Try the -25 file instead. ;\n "+
"#endif\n")

	copyMaterialFile("shared/mhx/templates/materials24.mhx", fp)	
	exportArmature(obj, fp)
	tmpl = open("shared/mhx/templates/meshes24.mhx")
	if tmpl:
		copyMeshFile249(obj, tmpl, fp)	
		tmpl.close()
	return

#
#	exportRawMhx(obj, fp)
#

def exportRawMhx(obj, fp):
	exportArmature(obj, fp)
	fp.write(
"#if useMesh \n" +
"mesh HumanMesh HumanMesh \n")
	exportRawData(obj, fp)
	fp.write(
"end mesh\n" +
"\nobject HumanMesh Mesh HumanMesh \n" +
"\tlayers 1 0 ;\n" +
"end object\n" +
"end useMesh\n")
	return

#
#	exportMhx_25(obj, rig, fp):
#

def exportMhx_25(obj, rig, fp):
	fp.write(
"# MakeHuman exported MHX\n" +
"# www.makehuman.org\n" +
"MHX %d %d ;\n" % (MAJOR_VERSION, MINOR_VERSION) +
"#if Blender24\n" +
"  error 'This file can only be read with Blender 2.5' ;\n" +
"#endif\n")

	mhx_rig.setupRig(obj)

	fp.write("#if toggle&T_Armature\n")
	copyFile25(obj, "shared/mhx/templates/common-armature25.mhx", rig, fp, None, [])	
	copyFile25(obj, "shared/mhx/templates/%s-armature25.mhx" % rig, rig, fp, None, [])	
	fp.write("#endif\n")

	fp.write("\nNoScale False ;\n\n")

	copyFile25(obj, "shared/mhx/templates/materials25.mhx", rig, fp, None, [])	

	proxyList = mh2proxy.proxyConfig()
	proxyData = {}
	proxyCopy('Cage', obj, rig, proxyList, proxyData, fp)

	fp.write("#if toggle&T_Mesh\n")
	copyFile25(obj, "shared/mhx/templates/meshes25.mhx", rig, fp, None, proxyData)	
	fp.write("#endif\n")

	proxyCopy('Proxy', obj, rig, proxyList, proxyData, fp)
	proxyCopy('Clothes', obj, rig, proxyList, proxyData, fp)

	fp.write("#if toggle&T_Armature\n")
	copyFile25(obj, "shared/mhx/templates/%s-poses25.mhx" % rig, rig, fp, None, proxyData)	
	fp.write("#endif\n")
	return

#
#	proxyCopy(name, obj, rig, proxyList, proxyData, fp)
#

def proxyCopy(name, obj, rig, proxyList, proxyData, fp):
	for (typ, useObj, useMhx, proxyStuff) in proxyList:
		if useMhx and typ == name:
			fp.write("#if toggle&T_%s\n" % typ)
			copyFile25(obj, "shared/mhx/templates/proxy25.mhx", rig, fp, proxyStuff, proxyData)	
			fp.write("#endif\n")
		
#
#	copyFile25(obj, tmplName, rig, fp, proxyStuff, proxyData):
#

def copyFile25(obj, tmplName, rig, fp, proxyStuff, proxyData):
	print("Trying to open "+tmplName)
	tmpl = open(tmplName)
	if tmpl == None:
		print("Cannot open "+tmplName)
		return

	bone = None
	proxy = None
	faces = files3d.loadFacesIndices("data/3dobjs/base.obj")
	ignoreLine = False
	for line in tmpl:
		words= line.split()
		if len(words) == 0:
			fp.write(line)
		elif words[0] == '***':
			if ignoreLine:
				if words[1] == 'EndIgnore':
					ignoreLine = False
			elif words[1] == 'Bone':
				bone = words[2]
				fp.write("    Bone %s\n" % bone)
			#elif words[1] == 'Rigify':
			#	mhxbones_rigify.writeBones(obj, fp)
			elif words[1] == 'head':
				(x, y, z) = mhxbones.boneHead[bone]
				fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,-z,y))
			elif words[1] == 'tail':
				(x, y, z) = mhxbones.boneTail[bone]
				fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,-z,y))
			elif words[1] == 'roll':
				(x, y) = mhxbones.boneRoll[bone]
				fp.write("    roll %.6g ;\n" % (y))
			elif words[1] == 'rig-bones':
				mhx_rig.writeAllArmatures(fp)
			elif words[1] == 'rig-poses':
				mhx_rig.writeAllPoses(fp)
			elif words[1] == 'rig-actions':
				mhx_rig.writeAllActions(fp)
			elif words[1] == 'rig-drivers':
				mhx_rig.writeAllDrivers(fp)
			elif words[1] == 'rig-process':
				fp.write("\n  ApplyArmature HumanMesh ;\n")
				for proxy in proxyData.values():
					if proxy.name and not proxy.bones:
						fp.write("  ApplyArmature %sMesh ;\n" % proxy.name)
				mhx_rig.writeAllProcesses(fp)
				mhx_rig.reapplyArmature(fp, "HumanMesh")
				for proxy in proxyData.values():
					if proxy.name and not proxy.bones:
						mhx_rig.reapplyArmature(fp, proxy.name)
			elif words[1] == 'ProxyRigStart':
				proxy = mh2proxy.readProxyFile(obj, proxyStuff)
				proxyData[proxy.name] = proxy
				if proxy.bones:
					fp.write("#if True\n")
				else:
					fp.write("#if False\n")
				fp.write("Armature %s %s   Normal \n" % (proxy.name, proxy.name))
				mh2proxy.writeProxyArmature(fp, proxy)
			elif words[1] == 'ProxyRigObject':
				fp.write("Object %s ARMATURE %s \n" % (proxy.name, proxy.name))
			elif words[1] == 'ProxyPose':
				mh2proxy.writeProxyPose(fp, proxy)
			elif words[1] == 'ProxyMesh':
				mat = proxy.material
				if mat:
					col = mat.diffuse_color
					spc = mat.specular_color
					fp.write(
"Material %s \n" % mat.name +
"  diffuse_color Array %.4f %.4f %.4f ;\n" % (col[0], col[1], col[2]) +
"  diffuse_shader '%s' ;\n" % mat.diffuse_shader +
"  diffuse_intensity %.4f ;\n" % mat.diffuse_intensity +
"  specular_color Array %.4f %.4f %.4f ;\n" % (spc[0], spc[1], spc[2]) +
"  specular_shader '%s' ;\n" % mat.specular_shader +
"  specular_intensity %.4f ;\n" % mat.specular_intensity +
"end Material\n\n")
				fp.write("Mesh %sMesh %sMesh \n" % (proxy.name, proxy.name))
				if mat:
					fp.write("  Material %s ;\n" % mat.name)

			elif words[1] == 'ProxyObject':
				fp.write("Object %sMesh MESH %sMesh \n" % (proxy.name, proxy.name))
				if proxy.wire:
					fp.write("  draw_type 'WIRE' ;\n")
			elif words[1] == 'ProxyLayers':
				fp.write("layers Array ")
				for n in range(20):
					if n == proxy.layer:
						fp.write("1 ")
					else:
						fp.write("0 ")
				fp.write(";\n")
				if proxy.cage:
					fp.write("  #if False\n")
				else:
					fp.write("  #if toggle&T_Cage\n")
			elif words[1] == 'ProxyReferRig':
				if proxy.bones:
					fp.write("      object Refer Object %s ;\n" % proxy.name)
				else:
					fp.write("      object Refer Object Human ;\n")
			elif words[1] == 'ProxyVerts':
				for bary in proxy.realVerts:
					(x,y,z) = mh2proxy.proxyCoord(bary)
					fp.write("v %.6g %.6g %.6g ;\n" % (x, -z, y))
			elif words[1] == 'Verts':
				proxy = None
				for v in obj.verts:
					fp.write("    v %.6g %.6g %.6g ;\n" %(v.co[0], -v.co[2], v.co[1]))
			elif words[1] == 'ProxyFaces':
				for (f,g) in proxy.faces:
					fp.write("    f")
					for v in f:
						fp.write(" %s" % v)
					fp.write(" ;\n")
				for mat in proxy.materials:
					fp.write("    ft %d 1 ;\n" % mat)
			elif words[1] == 'Faces':
				for f in faces:
					fp.write("    f")
					for v in f:
						fp.write(" %d" % v[0])
					fp.write(" ;\n")
			elif words[1] == 'FTTriangles':
				for (fn,f) in enumerate(faces):
					if len(f) < 4:
						fp.write("    mn %d 1 ;\n" % fn)
			elif words[1] == 'ProxyUVCoords':
				for f in proxy.texFaces:
					fp.write("    vt")
					for v in f:
						uv = proxy.texVerts[v]
						fp.write(" %.6g %.6g" % (uv[0], uv[1]))
					fp.write(" ;\n")
			elif words[1] == 'TexVerts':
				for f in faces:
					fp.write("    vt")
					for v in f:
						uv = obj.uvValues[v[1]]
						fp.write(" %.6g %.6g" %(uv[0], uv[1]))
					fp.write(" ;\n")
			elif words[1] == 'VertexGroup':
				if proxy and proxy.weighted:
					mh2proxy.writeProxyWeights(fp, proxy)
				else:
					copyVertGroups("shared/mhx/templates/vertexgroups-bones25.mhx", fp, proxy)	
					copyVertGroups("shared/mhx/templates/vertexgroups-leftright25.mhx", fp, proxy)	
					if not (proxy and proxy.cage):
						fp.write("#if toggle&T_Cage\n")
						copyVertGroups("shared/mhx/templates/vertexgroups-cage25.mhx", fp, proxy)	
						fp.write("#endif\n")
			elif words[1] == 'mesh-shapeKey':
				pass
				writeShapeKeys(fp, "HumanMesh", None)
			elif words[1] == 'proxy-shapeKey':
				fp.write("#if toggle&T_Proxy\n")
				for proxy in proxyData.values():
					if proxy.name and proxy.type == 'Proxy' and not proxy.bones:
						writeShapeKeys(fp, proxy.name+"Mesh", proxy)
				fp.write("#endif\n")
			elif words[1] == 'mesh-animationData':
				writeAnimationData(fp, "HumanMesh", None)
			elif words[1] == 'proxy-animationData':
				for proxy in proxyData.values():
					if proxy.name:
						writeAnimationData(fp, proxy.name+"Mesh", proxy)
			elif words[1] == 'ProxyModifiers':
				for mod in proxy.modifiers:
					if mod[0] == 'subsurf':
						sslevels = mod[1]
						fp.write(
"    Modifier SubSurf SUBSURF\n" +
"      levels %d ;\n" % sslevels +
"      render_levels %d ;\n" % (sslevels+1) +
"    end Modifier\n")
					elif mod[0] == 'shrinkwrap':
						offset = mod[1]
						fp.write(
"    Modifier ShrinkWrap SHRINKWRAP\n" +
"      target Refer Object HumanMesh ;\n" +
"      offset %.4f ;\n" % offset +
"      use_keep_above_surface True ;\n" +
"    end Modifier\n")
			elif words[1] == 'material-drivers':
				if BODY_LANGUAGE:
					mhx_rig.writeTextureDrivers(fp, rig_panel_25.BodyLanguageTextureDrivers)
			elif words[1] == 'Filename':
				path1 = os.path.expanduser(words[3])
				(path, filename) = os.path.split(words[2])
				file1 = os.path.realpath(path1+filename)
				fp.write("  Filename %s ;\n" % file1)
			else:
				raise NameError("Unknown *** %s" % words[1])
		else:
			fp.write(line)

	print("Closing "+tmplName)
	tmpl.close()

	return

#
#	copyVertGroups(tmplName, fp, proxy):
#

def copyVertGroups(tmplName, fp, proxy):
	print("Trying to open "+tmplName)
	tmpl = open(tmplName)
	shapes = []
	vgroups = []

	if tmpl == None:
		print("Cannot open "+tmplName)
		return
	if not proxy:
		for line in tmpl:
			fp.write(line)
	#elif proxy.bones:
	#	pass
	else:
		for line in tmpl:
			words= line.split()
			if len(words) == 0:
				fp.write(line)
			elif words[0] == 'wv':
				v = int(words[1])
				wt = float(words[2])
				try:
					vlist = proxy.verts[v]
				except:
					vlist = []
				for (pv, w) in vlist:
					vgroups.append((pv, w*wt))
			elif vgroups:
				printProxyVGroup(fp, vgroups)
				vgroups = []
				fp.write(line)
			else:	
				fp.write(line)
	print("Closing "+tmplName)
	tmpl.close()
	return

#
#	printProxyVGroup(fp, vgroups):
#

def printProxyVGroup(fp, vgroups):
	vgroups.sort()
	pv = -1
	while vgroups:
		(pv0, wt0) = vgroups.pop()
		if pv0 == pv:
			wt += wt0
		else:
			if pv >= 0 and wt > 1e-4:
				fp.write("    wv %d %.4f ;\n" % (pv, wt))
			(pv, wt) = (pv0, wt0)
	if pv >= 0 and wt > 1e-4:
		fp.write("    wv %d %.4f ;\n" % (pv, wt))
	return

#
#	copyShapeKeys(tmplName, fp, proxy):
#

eyeDist = 0.598002
mouthDist = 0.478831
tongueDist = 0.283124

ShapeKeyScale = {
	'BendElbowForward' 	: ('r-shoulder', 'r-hand', 4.705061),
	'BendKneeBack'		: ('r-upper-leg', 'r-ankle', 8.207247),
	'BendArmDown'		: ('r-shoulder', 'l-shoulder', 3.388347),
	'BendArmUp'		: ('r-shoulder', 'l-shoulder', 3.388347),

	'BrowsDown'		: ('r-eye', 'l-eye', eyeDist),
	'BrowsMidDown'		: ('r-eye', 'l-eye', eyeDist),
	'BrowsMidUp'		: ('r-eye', 'l-eye', eyeDist),
	'BrowsOutUp'		: ('r-eye', 'l-eye', eyeDist),
	'BrowsSqueeze'		: ('r-eye', 'l-eye', eyeDist),
	'Frown'			: ('r-mouth', 'l-mouth', mouthDist),
	'Narrow'		: ('r-mouth', 'l-mouth', mouthDist),
	'Smile'			: ('r-mouth', 'l-mouth', mouthDist),
	'Sneer'			: ('r-mouth', 'l-mouth', mouthDist),
	'Squint'		: ('r-eye', 'l-eye', eyeDist),
	'TongueOut'		: ('tongue-1', 'tongue-2', tongueDist),
	'TongueUp'		: ('tongue-1', 'tongue-2', tongueDist),
	'UpLipUp'		: ('r-mouth', 'l-mouth', mouthDist),
	'LoLipDown'		: ('r-mouth', 'l-mouth', mouthDist),
	'MouthOpen'		: ('r-mouth', 'l-mouth', mouthDist),
	'UpLipDown'		: ('r-mouth', 'l-mouth', mouthDist),
	'LoLipUp'		: ('r-mouth', 'l-mouth', mouthDist),
	'CheekUp'		: ('r-mouth', 'l-mouth', mouthDist),
	'TongueLeft'		: ('tongue-1', 'tongue-2', tongueDist),
	'TongueRight'		: ('tongue-1', 'tongue-2', tongueDist),

}

def copyShapeKeys(tmplName, fp, proxy, doScale):
	print("Trying to open "+tmplName)
	tmpl = open(tmplName)
	shapes = []
	vgroups = []
	scale = 1.0

	if tmpl == None:
		print("Cannot open "+tmplName)
		return
	if not proxy:
		for line in tmpl:
			words = line.split()
			if len(words) == 0:
				fp.write(line)
			elif words[0] == 'sv':
				v = int(words[1])
				dx = float(words[2])*scale
				dy = float(words[3])*scale
				dz = float(words[4])*scale
				fp.write("    sv %d %.4f %.4f %.4f ;\n" % (v, dx, dy, dz))
			elif words[0] == 'ShapeKey':
				if doScale:
					scale = setShapeScale(words)
				fp.write(line)
			else:
				fp.write(line)
	#elif proxy.bones:
	#	pass
	else:
		for line in tmpl:
			words= line.split()
			if len(words) == 0:
				fp.write(line)
			elif words[0] == 'sv':
				v = int(words[1])
				dx = float(words[2])*scale
				dy = float(words[3])*scale
				dz = float(words[4])*scale
				try:
					vlist = proxy.verts[v]
				except:
					vlist = []
				for (pv, w) in vlist:
					shapes.append((pv, w*dx, w*dy, w*dz))
			elif words[0] == 'ShapeKey':
				if doScale:
					scale = setShapeScale(words)
				fp.write(line)
			elif shapes:
				printProxyShape(fp, shapes)
				shapes = []
				fp.write(line)
			else:	
				fp.write(line)
	print("Closing "+tmplName)
	tmpl.close()
	return

#
#	setShapeScale(words):	
#

def setShapeScale(words):
	key = words[1]
	try:
		(p1, p2, length0) = ShapeKeyScale[key]
	except:
		#print('No scale	%s' % key)
		return 1.0
	x1 = mhx_rig.locations[p1]
	x2 = mhx_rig.locations[p2]
	dist = aljabr.vsub(x1, x2)
	length = aljabr.vlen(dist)
	scale = length/length0
	#print("Scale %s %f %f" % (key, length, scale))
	return scale
				
#
#	printProxyShape(fp, shapes)
#

def printProxyShape(fp, shapes):
	shapes.sort()
	pv = -1
	while shapes:
		(pv0, dx0, dy0, dz0) = shapes.pop()
		if pv0 == pv:
			dx += dx0
			dy += dy0
			dz += dz0
		else:
			if pv >= 0 and (dx > 1e-4 or dy > 1e-4 or dz > 1e-4):
				fp.write("    sv %d %.4f %.4f %.4f ;\n" % (pv, dx, dy, dz))
			(pv, dx, dy, dz) = (pv0, dx0, dy0, dz0)		
	if pv >= 0 and (dx > 1e-4 or dy > 1e-4 or dz > 1e-4):
		fp.write("    sv %d %.4f %.4f %.4f ;\n" % (pv, dx, dy, dz))
	return

#
#	writeShapeKeys(fp, name, proxy):
#

def writeShapeKeys(fp, name, proxy):
	fp.write(
"#if toggle&(T_Face+T_Shape)\n" +
"ShapeKeys %s\n" % name +
"  ShapeKey Basis Sym toggle&(T_Face+T_Shape)\n" +
"  end ShapeKey\n" +
"#endif\n" +

"#if toggle&T_Face\n")
	if BODY_LANGUAGE:
		copyShapeKeys("shared/mhx/templates/shapekeys-bodylanguage25.mhx", fp, proxy, True)	
	else:
		copyShapeKeys("shared/mhx/templates/shapekeys-facial25.mhx", fp, proxy, True)	
	fp.write(
"#endif\n" +

"#if toggle&T_Shape\n")
	copyShapeKeys("shared/mhx/templates/shapekeys-body25.mhx", fp, proxy, True)
	fp.write(
"#endif\n" +

"#if toggle&(T_Face+T_Shape)\n" +
"  AnimationData None (toggle&T_Symm==0)\n" +
"#if toggle&T_Shape\n")
	mhx_rig.writeRotDiffDrivers(fp, rig_arm_25.ArmShapeDrivers)
	mhx_rig.writeRotDiffDrivers(fp, rig_leg_25.LegShapeDrivers)
	mhx_rig.writeShapeDrivers(fp, rig_body_25.BodyShapeDrivers)
	fp.write(
"#endif\n" +
"#if toggle&T_Face\n")
	if BODY_LANGUAGE:
		mhx_rig.writeShapeDrivers(fp, rig_panel_25.BodyLanguageShapeDrivers)
	else:
		mhx_rig.writeShapeDrivers(fp, rig_panel_25.FaceShapeDrivers)
	fp.write(
"#endif\n" +
"  end AnimationData\n" +
"end ShapeKeys\n" +
"#endif\n")
	return	

#
#	copyMaterialFile(infile, fp):
#

def copyMaterialFile(infile, fp):
	tmpl = open(infile, "rU")
	for line in tmpl:
		words= line.split()
		if len(words) == 0:
			fp.write(line)
		elif words[0] == 'filename':
			path1 = os.path.expanduser("./data/textures/")
			(path, filename) = os.path.split(words[1])
			file1 = os.path.realpath(path1+filename)
			fp.write("  filename %s ;\n" % file1)
		else:
			fp.write(line)
	tmpl.close()

#
#	copyMeshFile249(obj, tmpl, fp):
#

def copyMeshFile249(obj, tmpl, fp):
	inZone = False
	skip = False
	mainMesh = False

	for line in tmpl:
		words= line.split()
		skipOne = False

		if len(words) == 0:
			pass
		elif words[0] == 'end':
			if words[1] == 'object' and mainMesh:
				fp.write(line)
				skipOne = True
				fp.write("#endif\n")
				mainMesh = False
				proxyList = mh2proxy.proxyConfig()
				fp.write("#if useProxy\n")
				for (typ, useObj, useMhx, proxyStuff) in proxyList:
					if useObj:
						exportProxy24(obj, proxyStuff, fp)
				fp.write("#endif\n")
			elif words[1] == 'mesh' and mainMesh:
				fp.write("  ShapeKey Basis Sym\n  end ShapeKey\n")
				copyShapeKeys("shared/mhx/templates/shapekeys-facial25.mhx", fp, None, False)	
				copyShapeKeys("shared/mhx/templates/shapekeys-extra24.mhx", fp, None, False)	
				copyShapeKeys("shared/mhx/templates/shapekeys-body25.mhx", fp, None, False)	
				writeIpo(fp)
				fp.write(line)
				skipOne = True
				fp.write("#endif\n")
				mainMesh = False
				inZone = False
				skip = False
		elif words[0] == 'mesh' and words[1] == 'HumanMesh':
			inZone = True
			mainMesh = True
			fp.write("#if useMesh\n")
		elif words[0] == 'object' and words[1] == 'HumanMesh':
			mainMesh = True
			fp.write("#if useMesh\n")
		elif words[0] == 'vertgroup':
			copyVertGroups("shared/mhx/templates/vertexgroups-common25.mhx", fp, None)	
			copyVertGroups("shared/mhx/templates/vertexgroups-classic25.mhx", fp, None)	
			copyVertGroups("shared/mhx/templates/vertexgroups-toes25.mhx", fp, None)	
			skipOne = True
			skip = False
		elif words[0] == 'v' and inZone:
			if not skip:
				exportRawData(obj, fp)
				skip = True
		elif words[0] == 'f' and skip:
			skip = False
			skipOne = True

		if not (skip or skipOne):
			fp.write(line)
	
	return

#
#	exportProxy24(obj, proxyStuff, fp):
#

def exportProxy24(obj, proxyStuff, fp):
	proxy = mh2proxy.readProxyFile(obj, proxyStuff)
	faces = files3d.loadFacesIndices("data/3dobjs/base.obj")
	tmpl = open("shared/mhx/templates/proxy24.mhx", "rU")
	for line in tmpl:
		words= line.split()
		if len(words) == 0:
			fp.write(line)
		elif words[0] == 'mesh':
			fp.write("mesh %s %s\n" % (proxy.name, proxy.name))
		elif words[0] == 'object':
			fp.write("object %s Mesh %s\n" % (proxy.name, proxy.name))
		elif words[0] == 'v':
			for bary in proxy.realVerts:
				(x,y,z) = mh2proxy.proxyCoord(bary)
				fp.write("v %.6g %.6g %.6g ;\n" % (x, -z, y))
		elif words[0] == 'f':
			for (f,g) in proxy.faces:
				fp.write("    f")
				for v in f:
					fp.write(" %d" % v)
				fp.write(" ;\n")
			fn = 0
			for mat in proxy.materials:
				fp.write("    fx %d %d 1 ;\n" % (fn,mat))
				fn += 1
		elif words[0] == 'vt':
			for f in proxy.texFaces:
				fp.write("    vt")
				for v in f:
					uv = proxy.texVerts[v]
					fp.write(" %.6g %.6g" %(uv[0], uv[1]))
				fp.write(" ;\n")
		elif words[0] == 'vertgroup':
			copyVertGroups("shared/mhx/templates/vertexgroups-common25.mhx", fp, proxy)	
			copyVertGroups("shared/mhx/templates/vertexgroups-classic25.mhx", fp, proxy)	
			copyVertGroups("shared/mhx/templates/vertexgroups-toes25.mhx", fp, proxy)	
		elif words[0] == 'shapekey':
			fp.write("  ShapeKey Basis Sym\n  end ShapeKey\n")
			if BODY_LANGUAGE:
				copyShapeKeys("shared/mhx/templates/shapekeys-bodylanguage25.mhx", fp, proxy, False)	
			else:
				copyShapeKeys("shared/mhx/templates/shapekeys-facial25.mhx", fp, proxy, False)	
			copyShapeKeys("shared/mhx/templates/shapekeys-extra24.mhx", fp, proxy, False)	
			copyShapeKeys("shared/mhx/templates/shapekeys-body25.mhx", fp, proxy, False)	
			writeIpo(fp)
		else:
			fp.write(line)
	tmpl.close()
	return

#
#	exportRawData(obj, fp):	
#
def exportRawData(obj, fp):	
	# Ugly klugdy fix of extra vert
	x1 = aljabr.vadd(obj.verts[11137].co, obj.verts[11140].co)
	x2 = aljabr.vadd(obj.verts[11162].co, obj.verts[11178].co)
	x = aljabr.vadd(x1,x2)
	obj.verts[14637].co = aljabr.vmul(x, 0.25)
	# end ugly kludgy
	for v in obj.verts:
		fp.write("v %.6g %.6g %.6g ;\n" %(v.co[0], v.co[1], v.co[2]))
		
	for uv in obj.uvValues:
		fp.write("vt %.6g %.6g ;\n" %(uv[0], uv[1]))
	faces = files3d.loadFacesIndices("data/3dobjs/base.obj")
	for f in faces:
		fp.write("f")
		for v in f:
			fp.write(" %i/%i " %(v[0], v[1]))
		fp.write(";\n")
#
#	exportArmature(obj, fp):
#

def exportArmature(obj, fp):
	oldExportArmature24(obj, fp)
	#newExportArmature24(obj, fp)
	return

def oldExportArmature24(obj, fp):
	mhxbones.writeJoints(obj, fp)

	fp.write(
"\n#if useArmature\n" +
"armature Human Human\n")
	mhxbones.writeBones(obj, fp)
	fp.write(
"\tlayerMask 0x515 ;\n" +
"\tautoIK false ;\n" +
"\tdelayDeform false ;\n" +
"\tdrawAxes false ;\n" +
"\tdrawNames false ;\n" +
"\tenvelopes false ;\n" +
"\tmirrorEdit true ;\n" +
"\trestPosition false ;\n" +
"\tvertexGroups true ;\n" +
"end armature\n")

	fp.write("\npose Human\n")
	mhxbones.writePose24(obj, fp)
	fp.write("end pose\n")

	fp.write(
"\nobject Human Armature Human \n" +
"\tlayers 1 0 ;\n" +
"\txRay true ;\n" +
"end object\n" +
"#endif useArmature\n")

	return 

#
#	newExportArmature4(obj, fp):
#
def newExportArmature24(obj, fp):
	mhx_rig.newSetupJoints(obj, classic_bones.ClassicJoints, classic_bones.ClassicHeadsTails)

	fp.write(
"\n#if useArmature\n" +
"armature Human Human\n")
	mhx_rig.writeArmature(fp, classic_bones.ClassicArmature + classic_bones.PanelArmature, False)
	fp.write(
"\tlayerMask 0x515 ;\n" +
"\tautoIK false ;\n" +
"\tdelayDeform false ;\n" +
"\tdrawAxes false ;\n" +
"\tdrawNames false ;\n" +
"\tenvelopes false ;\n" +
"\tmirrorEdit true ;\n" +
"\trestPosition false ;\n" +
"\tvertexGroups true ;\n" +
"end armature\n")

	fp.write("\npose Human\n")
	classic_bones.ClassicWritePoses(fp)
	fp.write("end pose\n")
		
	fp.write(
"\nobject Human Armature Human \n" +
"\tlayers 1 0 ;\n" +
"\txRay true ;\n" +
"end object\n" +
"#endif useArmature\n")

	return 

	
#
#	exportShapeKeys(obj, tmpl, fp, proxy):
#

def exportShapeKeys(obj, tmpl, fp, proxy):
	global splitLeftRight
	if tmpl == None:
		return
	lineNo = 0	
	store = False
	for line in tmpl:
		lineNo += 1
		words= line.split()
		if len(words) == 0:
			pass
		elif words[0] == 'end' and words[1] == 'shapekey' and store:
			if leftRightKey[shapekey] and splitLeftRight:
				writeShapeKey(fp, shapekey+"_L", shapeVerts, "Left", sliderMin, sliderMax, proxy)
				writeShapeKey(fp, shapekey+"_R", shapeVerts, "Right", sliderMin, sliderMax, proxy)
			else:
				writeShapeKey(fp, shapekey, shapeVerts, "None", sliderMin, sliderMax, proxy)
		elif words[0] == 'shapekey':
			shapekey = words[1]
			sliderMin = words[2]
			sliderMax = words[3]
			shapeVerts = []
			if shapekey[5:] == 'Bend' or shapekey[5:] == 'Shou':
				store = False
			else:
				store = True
		elif words[0] == 'sv' and store:
			shapeVerts.append(line)
	return

#
#	leftRightKey - True if shapekey comes in two parts
#

leftRightKey = {
	"Basis" : False,
	"BendElbowForward" : True,
	"BendHeadForward" : False,
	"BendKneeBack" : True,
	"BendLegBack" : True,
	"BendLegForward" : True,
	"BrowsDown" : True,
	"BrowsMidDown" : False,
	"BrowsMidUp" : False,
	"BrowsOutUp" : True,
	"BrowsSqueeze" : False,
	"CheekUp" : True,
	"Frown" : True,
	"UpLidDown" : True,
	"LoLidUp" : True,
	"Narrow" : True,
	"ShoulderDown" : True,
	"Smile" : True,
	"Sneer" : True,
	"Squint" : True,
	"TongueOut" : False,
	"ToungeUp" : False,
	"ToungeLeft" : False,
	"ToungeRight" : False,
	"UpLipUp" : True,
	"LoLipDown" : True,
	"MouthOpen" : False,
	"UpLipDown" : True,
	"LoLipUp" : True,
}

#
#	writeShapeKey(fp, shapekey, shapeVerts, vgroup, sliderMin, sliderMax, proxy):
#

def writeShapeKey(fp, shapekey, shapeVerts, vgroup, sliderMin, sliderMax, proxy):
	fp.write("shapekey %s %s %s %s\n" % (shapekey, sliderMin, sliderMax, vgroup))
	if proxy:
		shapes = []
		for line in shapeVerts:
			words = line.split()
			v = int(words[1])
			dx = float(words[2])
			dy = float(words[3])
			dz = float(words[4])
			try:
				vlist = proxy.verts[v]
			except:
				vlist = []
			for (pv,w) in vlist:
				shapes.append((pv, w*dx, w*dy, w*dz))
		printProxyShape(fp, shapes)
	else:
		for line in shapeVerts:
			fp.write(line)
	fp.write("end shapekey\n")

#
#	writeIcu(fp, shape, expr):
#

def writeIcu(fp, shape, expr):
	fp.write(
"\ticu %s 0 1\n" % shape +
"\t\tdriver 2 ;\n" +
"\t\tdriverObject _object['HumanMesh'] ;\n" +
"\t\tdriverChannel 1 ;\n" +
"\t\tdriverExpression '%s' ;\n" % expr +
"\tend icu\n")

def writeIpo(fp):
	global splitLeftRight

	mhxFile = "shared/mhx/templates/mhxipos.mhx"
	try:
		print("Trying to open "+mhxFile)
		tmpl = open(mhxFile, "rU")
	except:
		print("Failed to open "+mhxFile)
		tmpl = None

	if tmpl and splitLeftRight:
		for line in tmpl:
			fp.write(line)
	else:
		fp.write("ipo Key KeyIpo\n")
		for (shape, lr) in leftRightKey.items():
			if shape == 'Basis':
				pass
			elif lr and splitLeftRight:
				writeIcu(fp, shape+'_L', 'p.ctrl'+shape+'_L()')
				writeIcu(fp, shape+'_R', 'p.ctrl'+shape+'_R()')
			else:
				writeIcu(fp, shape, 'p.ctrl'+shape+'()')
		fp.write("end ipo\n")
	
	if tmpl:
		print(mhxFile+" closed")
		tmpl.close()

	return



