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

import module3d, aljabr, mh, files3d, mh2bvh, mhxbones, mhxbones_rigify, mhx_rig
import classic_bones, gobo_bones #, sintel_bones
import os


splitLeftRight = True

#
#	exportMhx(obj, filename):
#
def exportMhx(obj, filename):	
	(name, ext) = os.path.splitext(filename)

	filename = name+"-24"+ext
	print("Writing MHX 2.4x file " + filename )
	fp = open(filename, 'w')
	exportMhx_24(obj, fp)
	fp.close()
	print("MHX 2.4x file %s written" % filename)

	filename = name+"-25"+ext
	print("Writing MHX 2.5x file " + filename )
	fp = open(filename, 'w')
	exportMhx_25(obj, "rig", fp)
	fp.close()
	print("MHX 2.5x file %s written" % filename)

	'''
	filename = name+"-classic-25"+ext
	print("Writing MHX 2.5x file " + filename )
	fp = open(filename, 'w')
	exportMhx_25(obj, "classic", fp)
	fp.close()
	print("MHX 2.5x file %s written" % filename)

	filename = name+"-gobo-25"+ext
	print("Writing MHX 2.5x file " + filename )
	fp = open(filename, 'w')
	exportMhx_25(obj, "gobo", fp)
	fp.close()
	print("MHX 2.5x file %s written" % filename)

	filename = name+"-sintel-25"+ext
	print("Writing MHX 2.5x file " + filename )
	fp = open(filename, 'w')
	exportMhx_25(obj, "sintel", fp)
	fp.close()
	print("MHX 2.5x file %s written" % filename)
	
	filename = name+"-rigify-25"+ext
	print("Writing MHX 2.5x file " + filename )
	fp = open(filename, 'w')
	exportMhx_25(obj, "rigify", fp)
	fp.close()
	print("MHX 2.5x file %s written" % filename)
	'''

	return

#
#	exportMhx_24(obj,fp):
#

def exportMhx_24(obj, fp):
	fp.write(
"# MakeHuman exported MHX\n" +
"# www.makehuman.org\n" +
"MHX 0 7 ;\n")

	fp.write(
"if Blender25\n"+
"  error This file can not be opened in Blender 2.5x. Try the -classic25 file instead. ;\n "+
"end if\n")

	copyMaterialFile("data/templates/materials24.mhx", fp)	
	exportArmature(obj, fp)
	tmpl = open("data/templates/meshes24.mhx")
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
"if useMesh \n" +
"mesh Human Human \n")
	exportRawData(obj, fp)
	fp.write(
"end mesh\n" +
"\nobject Human Mesh Human \n" +
"\tlayers 1 0 ;\n" +
"end object\n" +
"end useMesh\n")
	return

#
#	exportMhx_25(obj, rig, fp):
#

def exportMhx_25(obj, rig, fp):
	copyFile25(obj, "data/templates/materials25.mhx", rig, fp)	

	if rig == 'gobo':
		mhx_rig.newSetupJoints(obj, gobo_bones.GoboJoints +  classic_bones.FaceJoints +  classic_bones.PanelJoints, 
			gobo_bones.GoboHeadsTails + classic_bones.FaceHeadsTails + classic_bones.PanelHeadsTails)
	elif rig == 'sintel':
		mhx_rig.newSetupJoints(obj, sintel_bones.SintelJoints, sintel_bones.SintelHeadsTails)
		copyFile25(obj, "data/templates/sintel-armature25.mhx", rig, fp)
		return
	elif rig == 'classic':
		mhx_rig.newSetupJoints(obj, classic_bones.ClassicJoints +  classic_bones.FaceJoints +  classic_bones.PanelJoints,
			classic_bones.ClassicHeadsTails + classic_bones.FaceHeadsTails + classic_bones.PanelHeadsTails)
		#mhxbones.setupBones(obj)
	elif rig == 'rig':
		mhx_rig.setupRig(obj)

	fp.write("if toggle&T_Armature\n")
	copyFile25(obj, "data/templates/common-armature25.mhx", rig, fp)	
	copyFile25(obj, "data/templates/%s-armature25.mhx" % rig, rig, fp)	
	fp.write("end if\n")
	fp.write("if toggle&T_Proxy\n")
	copyFile25(obj, "data/templates/proxy25.mhx", rig, fp)	
	fp.write("end if\n")
	fp.write("if toggle&T_Mesh\n")
	copyFile25(obj, "data/templates/meshes25.mhx", rig, fp)	
	fp.write("end if\n")
	fp.write("if toggle&T_Armature\n")
	copyFile25(obj, "data/templates/%s-poses25.mhx" % rig, rig, fp)	
	fp.write("end if\n")
	return

		
#
#	copyFile25(obj, tmplName, rig, fp):
#

def copyFile25(obj, tmplName, rig, fp):
	print("Trying to open "+tmplName)
	tmpl = open(tmplName)
	if tmpl == None:
		print("Cannot open "+tmplName)
		return

	bone = None
	faces = files3d.loadFacesIndices("data/3dobjs/base.obj")
	proxyVerts = None
	realVerts = None
	proxyFaces = None
	ignoreLine = False
	for line in tmpl:
		lineSplit= line.split()
		if len(lineSplit) == 0:
			fp.write(line)
		elif lineSplit[0] == '***':
			if ignoreLine:
				if lineSplit[1] == 'EndIgnore':
					ignoreLine = False
			elif lineSplit[1] == 'Particles':
				if writeHairCurves(hair, hairStep, amount, fp):
					ignoreLine = True
			elif lineSplit[1] == 'ParticleSystem':
				pass
				# copyFile25(obj, "data/templates/particles25.mhx", rig, fp)	
			elif lineSplit[1] == 'Bone':
				bone = lineSplit[2]
				fp.write("    Bone %s\n" % bone)
			elif lineSplit[1] == 'Rigify':
				mhxbones_rigify.writeBones(obj, fp)
			elif lineSplit[1] == 'head':
				(x, y, z) = mhxbones.boneHead[bone]
				fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,-z,y))
			elif lineSplit[1] == 'tail':
				(x, y, z) = mhxbones.boneTail[bone]
				fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,-z,y))
			elif lineSplit[1] == 'roll':
				(x, y) = mhxbones.boneRoll[bone]
				fp.write("    roll %.6g ;\n" % (y))
			elif lineSplit[1] == 'rig-bones':
				mhx_rig.writeAllArmatures(fp)
			elif lineSplit[1] == 'rig-poses':
				mhx_rig.writeAllPoses(fp)
			elif lineSplit[1] == 'rig-actions':
				mhx_rig.writeAllActions(fp)
			elif lineSplit[1] == 'rig-drivers':
				mhx_rig.writeAllDrivers(fp)
			elif lineSplit[1] == 'rig-process':
				mhx_rig.writeAllProcesses(fp)
			elif lineSplit[1] == 'classic-bones':
				mhx_rig.writeArmature(fp, classic_bones.ClassicArmature + classic_bones.FaceArmature + classic_bones.PanelArmature, True)
			elif lineSplit[1] == 'classic-poses':
				classic_bones.ClassicWritePoses(fp)
				classic_bones.FaceWritePoses(fp)
				classic_bones.PanelWritePoses(fp)
			elif lineSplit[1] == 'classic-drivers':
				pass
			elif lineSplit[1] == 'gobo-bones':
				mhx_rig.writeArmature(fp, gobo_bones.GoboArmature + classic_bones.FaceArmature + classic_bones.PanelArmature, True)
			elif lineSplit[1] == 'gobo-poses':
				gobo_bones.GoboWritePoses(fp)
				classic_bones.FaceWritePoses(fp)
				classic_bones.PanelWritePoses(fp)
			elif lineSplit[1] == 'gobo-actions':
				gobo_bones.GoboWriteActions(fp)
			elif lineSplit[1] == 'gobo-constraint-drivers':
				gobo_bones.GoboWriteDrivers(fp)
			elif lineSplit[1] == 'sintel-bones':
				mhx_rig.writeArmature(fp, sintel_bones.SintelArmature, True)
			elif lineSplit[1] == 'sintel-poses':
				sintel_bones.SintelWritePoses(fp)
			elif lineSplit[1] == 'sintel-drivers':
				mhx_rig.writeDrivers(fp, sintel_bones.SintelDrivers)
			elif lineSplit[1] == 'ProxyVerts':
				(proxyVerts, realVerts, proxyFaces, proxyMaterials) = readProxyFile(obj.verts)
				for v in realVerts:
					fp.write("    v %.6g %.6g %.6g ;\n" %(v.co[0], -v.co[2], v.co[1]))
			elif lineSplit[1] == 'Verts':
				proxyVerts = None
				realVerts = None
				proxyFaces = None
				proxyMaterials = None
				for v in obj.verts:
					fp.write("    v %.6g %.6g %.6g ;\n" %(v.co[0], -v.co[2], v.co[1]))
			elif lineSplit[1] == 'ProxyFaces':
				for f in proxyFaces:
					fp.write("    f")
					for v in f:
						fp.write(" %d" % v)
					fp.write(" ;\n")
				for mat in proxyMaterials:
					fp.write("    ft %d 1 ;\n" % mat)
			elif lineSplit[1] == 'Faces':
				for f in faces:
					fp.write("    f")
					for v in f:
						fp.write(" %d" % v[0])
					fp.write(" ;\n")
			elif lineSplit[1] == 'ProxyTexVerts':
				for f in proxyFaces:
					fp.write("    vt")
					for v0 in f:
						v = realVerts[v0]
						uv = obj.uvValues[v.idx]
						fp.write(" %.6g %.6g" %(uv[0], uv[1]))
					fp.write(" ;\n")
			elif lineSplit[1] == 'TexVerts':
				for f in faces:
					fp.write("    vt")
					for v in f:
						uv = obj.uvValues[v[1]]
						fp.write(" %.6g %.6g" %(uv[0], uv[1]))
					fp.write(" ;\n")
			elif lineSplit[1] == 'VertexGroup':
				if rig == 'rig':
					copyProxy("data/templates/vertexgroups-common25.mhx", fp, proxyVerts)	
					copyProxy("data/templates/vertexgroups-classic25.mhx", fp, proxyVerts)	
					copyProxy("data/templates/vertexgroups-toes25.mhx", fp, proxyVerts)	
					copyProxy("data/templates/vertexgroups-foot25.mhx", fp, proxyVerts)
				elif rig == 'classic':
					copyProxy("data/templates/vertexgroups-common25.mhx", fp, proxyVerts)	
					copyProxy("data/templates/vertexgroups-classic25.mhx", fp, proxyVerts)	
					copyProxy("data/templates/vertexgroups-toes25.mhx", fp, proxyVerts)	
				elif rig == 'gobo':
					copyProxy("data/templates/vertexgroups-common25.mhx", fp, proxyVerts)	
					copyProxy("data/templates/vertexgroups-classic25.mhx", fp, proxyVerts)	
					copyProxy("data/templates/vertexgroups-foot25.mhx", fp, proxyVerts)	
				elif rig == 'rigify':
					copyProxy("data/templates/vertexgroups-common25.mhx", fp, proxyVerts)	
					copyProxy("data/templates/vertexgroups-rigify25.mhx", fp, proxyVerts)	
					copyProxy("data/templates/vertexgroups-foot25.mhx", fp, proxyVerts)	
			elif lineSplit[1] == 'ShapeKey':
				fp.write("  ShapeKey Basis Sym\n  end ShapeKey\n")
				copyProxy("data/templates/shapekeys-facial25.mhx", fp, proxyVerts)	
				copyProxy("data/templates/shapekeys-body25.mhx", fp, proxyVerts)	
			elif lineSplit[1] == 'Filename':
				path1 = os.path.expanduser("./data/textures/")
				(path, filename) = os.path.split(lineSplit[2])
				file1 = os.path.realpath(path1+filename)
				fp.write("  Filename %s ;\n" % file1)
			else:
				raise NameError("Unknown *** %s" % lineSplit[1])
		else:
			fp.write(line)

	print("Closing "+tmplName)
	tmpl.close()

	return

#
#	readProxyFile(verts):
#

def readProxyFile(verts):
	tmplName = "./data/templates/proxy_mesh.txt"
	tmpl = open(tmplName, "rU")
	if tmpl == None:
		print("Cannot open proxy template "+tmplName)
		return (None, None, None)

	realVerts = []
	proxyFaces = []
	proxyVerts = {}
	proxyMaterials = []
	vn = 0
	doVerts = False
	doFaces = False
	doMaterials = False
	for line in tmpl:
		lineSplit= line.split()
		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == 'Verts':
			doVerts = True
		elif lineSplit[0] == 'Faces':
			doVerts = False
			doFaces = True
		elif lineSplit[0] == 'Materials':
			doVerts = False
			doFaces = False
			doMaterials = True
		elif doVerts:
			v = int(lineSplit[0])
			realVerts.append(verts[v])
			proxyVerts[v] = vn
			vn += 1
		elif doFaces:
			face = []
			for n in range(len(lineSplit)):
				f = int(lineSplit[n])
				face.append(f)
			proxyFaces.append(face)
		elif doMaterials:
			proxyMaterials.append(int(lineSplit[0]))

	return (proxyVerts, realVerts, proxyFaces, proxyMaterials)
	
#
#	exportProxyObj(obj, filename):	
#

def exportProxyObj(obj, filename):
	(name, ext) = os.path.splitext(filename)
	(proxyVerts, realVerts, proxyFaces, proxyMaterials) = readProxyFile(obj.verts)
	matNames = ['ProxySkin', 'ProxyWhite', 'ProxyRed', 'ProxyGum', 'ProxyBlue', 'ProxyBlack']

	fp = open(filename, 'w')
	fp.write(
"# MakeHuman exported OBJ for proxy mesh\n" +
"# www.makehuman.org\n" +
"mtllib %s.mtl\n" % name)

	for v in realVerts:
		fp.write("v %.6g %.6g %.6g\n" %(v.co[0], v.co[1], v.co[2]))

	mat = -1
	n = 0
	for f in proxyFaces:
		if proxyMaterials[n] != mat:
			mat = proxyMaterials[n]
			fp.write("usemtl %s\n" % matNames[mat])
		n += 1
		fp.write("f")
		for v in f:
			fp.write(" %d" % (v+1))
		fp.write("\n")
	fp.close()

	fp = open(name + ".mtl", 'w')
	fp.write(
"# MakeHuman exported MTL for proxy\n"+
"# www.makehuman.org\n"+
"newmtl ProxySkin \n"+
"Kd 0.92 0.73 0.58\n"+ 
"\n"+
"newmtl ProxyWhite\n"+ 
"Kd 1.0 1.0 1.0 \n"+
"\n"+
"newmtl ProxyRed \n"+
"Kd 1.0 0.0 0.0\n"+
"\n"+
"newmtl ProxyGum \n"+
"Kd 0.6 0.2 0.3 \n"+
"\n"+
"newmtl ProxyBlue \n"+
"Kd 0.0 0.0 1.0\n"+
"\n"+
"newmtl ProxyBlack\n"+
"Kd 0.0 0.0 0.0 \n")
	fp.close()
	return
	

#
#	copyProxy(tmplName, fp, proxyVerts):
#

def copyProxy(tmplName, fp, proxyVerts):
	print("Trying to open "+tmplName)
	tmpl = open(tmplName)

	if tmpl == None:
		print("Cannot open "+tmplName)
		return
	if proxyVerts:
		for line in tmpl:
			lineSplit= line.split()
			if len(lineSplit) == 0:
				fp.write(line)
			elif lineSplit[0] == 'sv':
				v = int(lineSplit[1])
				try:
					pv = proxyVerts[v]
					fp.write("    sv %d %s %s %s ;\n" % (pv, lineSplit[2], lineSplit[3], lineSplit[4]))
				except:
					pass
			elif lineSplit[0] == 'wv':
				v = int(lineSplit[1])
				try:
					pv = proxyVerts[v]
					fp.write("    wv %d %s ;\n" % (pv, lineSplit[2]))
				except:
					pass
			else:
				fp.write(line)
	else:
		for line in tmpl:
			fp.write(line)
	print("Closing "+tmplName)
	tmpl.close()
	return

#
#	copyMaterialFile(infile, fp):
#

def copyMaterialFile(infile, fp):
	tmpl = open(infile, "rU")
	for line in tmpl:
		lineSplit= line.split()
		if len(lineSplit) == 0:
			fp.write(line)
		elif lineSplit[0] == 'filename':
			path1 = os.path.expanduser("./data/textures/")
			(path, filename) = os.path.split(lineSplit[1])
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
		lineSplit= line.split()
		skipOne = False

		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == 'end':
			if lineSplit[1] == 'object' and mainMesh:
				fp.write(line)
				skipOne = True
				fp.write("end if\n")
				mainMesh = False
				exportProxy24(obj, fp)
			elif lineSplit[1] == 'mesh' and mainMesh:
				#shpfp = open("data/templates/shapekeys24.mhx", "rU")
				#exportShapeKeys(obj, shpfp, fp, None)
				#shpfp.close()
				fp.write("  ShapeKey Basis Sym\n  end ShapeKey\n")
				copyProxy("data/templates/shapekeys-facial25.mhx", fp, None)	
				copyProxy("data/templates/shapekeys-body25.mhx", fp, None)	
				writeIpo(fp)
				fp.write(line)
				skipOne = True
				fp.write("end if\n")
				mainMesh = False
				inZone = False
				skip = False
		elif lineSplit[0] == 'mesh' and lineSplit[1] == 'Human':
			inZone = True
			mainMesh = True
			fp.write("if useMesh\n")
		elif lineSplit[0] == 'object' and lineSplit[1] == 'Human':
			mainMesh = True
			fp.write("if useMesh\n")
		elif lineSplit[0] == 'vertgroup':
			copyProxy("data/templates/vertexgroups-common25.mhx", fp, None)	
			copyProxy("data/templates/vertexgroups-classic25.mhx", fp, None)	
			copyProxy("data/templates/vertexgroups-toes25.mhx", fp, None)	
			skipOne = True
			skip = False
		elif lineSplit[0] == 'v' and inZone:
			if not skip:
				exportRawData(obj, fp)
				skip = True
		elif lineSplit[0] == 'f' and skip:
			skip = False
			skipOne = True

		if not (skip or skipOne):
			fp.write(line)
	
	return

#
#	exportProxy24(obj, fp):
#

def exportProxy24(obj, fp):
	tmpl = open("data/templates/proxy24.mhx", "rU")
	proxyVerts = None
	realVerts = None
	proxyFaces = None
	proxyMaterials = None
	faces = files3d.loadFacesIndices("data/3dobjs/base.obj")
	fp.write("if useProxy\n")
	for line in tmpl:
		lineSplit= line.split()
		if len(lineSplit) == 0:
			fp.write(line)
		elif lineSplit[0] == 'v':
			(proxyVerts, realVerts, proxyFaces, proxyMaterials) = readProxyFile(obj.verts)
			for v in realVerts:
				fp.write("    v %.6g %.6g %.6g ;\n" %(v.co[0], -v.co[2], v.co[1]))
		elif lineSplit[0] == 'f':
			for f in proxyFaces:
				fp.write("    f")
				for v in f:
					fp.write(" %d" % v)
				fp.write(" ;\n")
			fn = 0
			for mat in proxyMaterials:
				fp.write("    fx %d %d 1 ;\n" % (fn,mat))
				fn += 1
		elif lineSplit[0] == 'vt':
			for f in proxyFaces:
				fp.write("    vt")
				for v0 in f:
					v = realVerts[v0]
					uv = obj.uvValues[v.idx]
					fp.write(" %.6g %.6g" %(uv[0], uv[1]))
				fp.write(" ;\n")
		elif lineSplit[0] == 'vertgroup':
			copyProxy("data/templates/vertexgroups-common25.mhx", fp, proxyVerts)	
			copyProxy("data/templates/vertexgroups-classic25.mhx", fp, proxyVerts)	
			copyProxy("data/templates/vertexgroups-toes25.mhx", fp, proxyVerts)	
			# copyProxy("data/templates/vertexgroups24.mhx", fp, proxyVerts)	
		elif lineSplit[0] == 'shapekey':
			# shpfp = open("data/templates/shapekeys24.mhx", "rU")
			# exportShapeKeys(obj, shpfp, fp, proxyVerts)
			# shpfp.close()
			fp.write("  ShapeKey Basis Sym\n  end ShapeKey\n")
			copyProxy("data/templates/shapekeys-facial25.mhx", fp, proxyVerts)	
			copyProxy("data/templates/shapekeys-body25.mhx", fp, proxyVerts)	
			writeIpo(fp)
		else:
			fp.write(line)
	tmpl.close()
	fp.write("end if\n")
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
"\nif useArmature\n" +
"armature HumanRig HumanRig\n")
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

	fp.write("\npose HumanRig\n")
	mhxbones.writePose24(obj, fp)
	fp.write("end pose\n")

	fp.write(
"\nobject HumanRig Armature HumanRig \n" +
"\tlayers 1 0 ;\n" +
"\txRay true ;\n" +
"end object\n" +
"end useArmature\n")

	return 

#
#	newExportArmature4(obj, fp):
#
def newExportArmature24(obj, fp):
	mhx_rig.newSetupJoints(obj, classic_bones.ClassicJoints, classic_bones.ClassicHeadsTails)

	fp.write(
"\nif useArmature\n" +
"armature HumanRig HumanRig\n")
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

	fp.write("\npose HumanRig\n")
	classic_bones.ClassicWritePoses(fp)
	fp.write("end pose\n")
		
	fp.write(
"\nobject HumanRig Armature HumanRig \n" +
"\tlayers 1 0 ;\n" +
"\txRay true ;\n" +
"end object\n" +
"end useArmature\n")

	return 

	
#
#	exportShapeKeys(obj, tmpl, fp, proxyVerts):
#

def exportShapeKeys(obj, tmpl, fp, proxyVerts):
	global splitLeftRight
	if tmpl == None:
		return
	lineNo = 0	
	store = False
	for line in tmpl:
		lineNo += 1
		lineSplit= line.split()
		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == 'end' and lineSplit[1] == 'shapekey' and store:
			if leftRightKey[shapekey] and splitLeftRight:
				writeShapeKey(fp, shapekey+"_L", shapeVerts, "Left", sliderMin, sliderMax, proxyVerts)
				writeShapeKey(fp, shapekey+"_R", shapeVerts, "Right", sliderMin, sliderMax, proxyVerts)
			else:
				writeShapeKey(fp, shapekey, shapeVerts, "None", sliderMin, sliderMax, proxyVerts)
		elif lineSplit[0] == 'shapekey':
			shapekey = lineSplit[1]
			sliderMin = lineSplit[2]
			sliderMax = lineSplit[3]
			shapeVerts = []
			if shapekey[5:] == 'Bend' or shapekey[5:] == 'Shou':
				store = False
			else:
				store = True
		elif lineSplit[0] == 'sv' and store:
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
#	writeShapeKey(fp, shapekey, shapeVerts, vgroup, sliderMin, sliderMax, proxyVerts):
#

def writeShapeKey(fp, shapekey, shapeVerts, vgroup, sliderMin, sliderMax, proxyVerts):
	fp.write("shapekey %s %s %s %s\n" % (shapekey, sliderMin, sliderMax, vgroup))
	if proxyVerts:
		for line in shapeVerts:
			lineSplit = line.split()
			v = int(lineSplit[1])
			try:
				pv = proxyVerts[v]
				fp.write("    sv %d %s %s %s ;\n" % (pv, lineSplit[2], lineSplit[3], lineSplit[4]))
			except:
				pass
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
"\t\tdriverObject _object['Human'] ;\n" +
"\t\tdriverChannel 1 ;\n" +
"\t\tdriverExpression '%s' ;\n" % expr +
"\tend icu\n")

def writeIpo(fp):
	global splitLeftRight

	mhxFile = "data/templates/mhxipos.mhx"
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



