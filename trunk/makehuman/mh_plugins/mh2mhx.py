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

import module3d, aljabr, mh, files3d, mh2bvh, mhxbones, mhxbones_rigify, mhx_rig, rig_panel_25
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
#	proxyConfig():
#

def proxyConfig():
	paths = ['~/makehuman/proxy.cfg', './proxy.cfg']
	
	fp = None
	for path in paths:
		path1 = os.path.expanduser(path)
		fileName = os.path.realpath(path1)
		try:
			fp = open(fileName, "r")
			break
		except:
			print("No file %s" % fileName)

	if not fp: return []	
	proxyList = []
	for line in fp:
		lineSplit = line.split()
		if len(lineSplit) == 0 or lineSplit[0][0] == '#':
			pass
		else:
			proxyFile = os.path.expanduser(lineSplit[0])
			proxyList.append(proxyFile)
	fp.close()
	print(proxyList)
	return proxyList

	

#
#	exportMhx_25(obj, rig, fp):
#

def exportMhx_25(obj, rig, fp):
	copyFile25(obj, "data/templates/materials25.mhx", rig, fp, None, [])	

	mhx_rig.setupRig(obj)

	fp.write("if toggle&T_Armature\n")
	copyFile25(obj, "data/templates/common-armature25.mhx", rig, fp, None, [])	
	copyFile25(obj, "data/templates/%s-armature25.mhx" % rig, rig, fp, None, [])	
	fp.write("end if\n")

	proxyList = proxyConfig()
	proxyData = {}
	fp.write("if toggle&T_Proxy\n")
	for proxyFile in proxyList:
		copyFile25(obj, "data/templates/proxy25.mhx", rig, fp, proxyFile, proxyData)	
	fp.write("end if\n")

	fp.write("if toggle&T_Mesh\n")
	copyFile25(obj, "data/templates/meshes25.mhx", rig, fp, None, [])	
	fp.write("end if\n")

	fp.write("if toggle&T_Armature\n")
	copyFile25(obj, "data/templates/%s-poses25.mhx" % rig, rig, fp, None, proxyData)	
	fp.write("end if\n")
	return

		
#
#	copyFile25(obj, tmplName, rig, fp, proxyFile, proxyData):
#

def copyFile25(obj, tmplName, rig, fp, proxyFile, proxyData):
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
			elif lineSplit[1] == 'Bone':
				bone = lineSplit[2]
				fp.write("    Bone %s\n" % bone)
			#elif lineSplit[1] == 'Rigify':
			#	mhxbones_rigify.writeBones(obj, fp)
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
				fp.write("\n  ApplyArmature Human ;\n")
				for proxyName in proxyData.keys():
					if proxyName:
						fp.write("  ApplyArmature %s ;\n" % proxyName)
				mhx_rig.writeAllProcesses(fp)
				mhx_rig.reapplyArmature(fp, "Human")
				for proxyName in proxyData.keys():
					if proxyName:
						mhx_rig.reapplyArmature(fp, proxyName)
			elif lineSplit[1] == 'ProxyMesh':
				(proxyName, proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, proxyTexVerts) = readProxyFile(obj.verts, proxyFile)
				fp.write("Mesh %s %s \n" % (proxyName, proxyName))
				proxyData[proxyName] = (proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, proxyTexVerts)
			elif lineSplit[1] == 'ProxyObject':
				fp.write("Object %s MESH %s \n" % (proxyName, proxyName))
			elif lineSplit[1] == 'ProxyVerts':
				printRealVerts(fp, realVerts, True)
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
						fp.write(" %s" % v)
					fp.write(" ;\n")
				for mat in proxyMaterials:
					fp.write("    ft %d 1 ;\n" % mat)
			elif lineSplit[1] == 'Faces':
				for f in faces:
					fp.write("    f")
					for v in f:
						fp.write(" %d" % v[0])
					fp.write(" ;\n")
			elif lineSplit[1] == 'FTTriangles':
				for (fn,f) in enumerate(faces):
					if len(f) < 4:
						fp.write("    mn %d 1 ;\n" % fn)
			elif lineSplit[1] == 'ProxyUVCoords':
				for f in proxyTexFaces:
					fp.write("    vt")
					for v in f:
						uv = proxyTexVerts[v]
						fp.write(" %.6g %.6g" % (uv[0], uv[1]))
					fp.write(" ;\n")
			elif lineSplit[1] == 'TexVerts':
				for f in faces:
					fp.write("    vt")
					for v in f:
						uv = obj.uvValues[v[1]]
						fp.write(" %.6g %.6g" %(uv[0], uv[1]))
					fp.write(" ;\n")
			elif lineSplit[1] == 'VertexGroup':
				pass
				copyProxy("data/templates/vertexgroups-bones25.mhx", fp, proxyVerts)	
				copyProxy("data/templates/vertexgroups-leftright25.mhx", fp, proxyVerts)	
			elif lineSplit[1] == 'mesh-shapeKey':
				pass
				writeShapeKeys(fp, "Human", None)
			elif lineSplit[1] == 'proxy-shapeKey':
				fp.write("if toggle&T_Proxy\n")
				for (proxyName, (proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, 
					proxyTexVerts)) in proxyData.items():
					if proxyName:
						writeShapeKeys(fp, proxyName, proxyVerts)
				fp.write("end if ;\n")
			elif lineSplit[1] == 'mesh-animationData':
				writeAnimationData(fp, "Human", None)
			elif lineSplit[1] == 'proxy-animationData':
				for (proxyName, (proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, 
					proxyTexVerts)) in proxyData.items():
					if proxyName:
						writeAnimationData(fp, proxyName, proxyVerts)
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

def writeShapeKeys(fp, name, proxyVerts):
	fp.write("ShapeKeys %s\n" % name)
	fp.write("  ShapeKey Basis Sym toggle&(T_Face+T_Shape)\n  end ShapeKey\n")
	copyProxy("data/templates/shapekeys-facial25.mhx", fp, proxyVerts)	
	copyProxy("data/templates/shapekeys-body25.mhx", fp, proxyVerts)
	fp.write("  AnimationData toggle&(T_Face)\n")	
	mhx_rig.writeShapeDrivers(fp, rig_panel_25.FaceDrivers)
	fp.write("  end AnimationData\n")
	fp.write("end ShapeKeys\n")
	return

#
#	readProxyFile(verts, proxyFile):
#

def readProxyFile(verts, proxyFile):
	if not proxyFile:
		return (None, [],[],[],[],[],[])

	#tmplName = "./data/templates/%s.proxy" % proxyFile
	try:
		tmpl = open(proxyFile, "rU")
	except:
		tmpl = None
	if tmpl == None:
		print("Cannot open proxy file %s" % proxyFile)
		return (None, [],[],[],[],[],[])

	realVerts = []
	proxyFaces = []
	proxyVerts = {}
	proxyTexFaces = []
	proxyTexVerts = []
	proxyMaterials = []
	proxyName = "MyProxy"

	vn = 0
	doVerts = False
	doFaces = False
	doMaterials = False
	doTexVerts = False
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
		elif lineSplit[0] == 'TexVerts':
			doVerts = False
			doFaces = False
			doMaterials = False
			doTexVerts = True
		elif lineSplit[0] == 'Name':
			proxyName = lineSplit[1]
		elif doVerts:
			v0 = int(lineSplit[0])
			v1 = int(lineSplit[1])
			v2 = int(lineSplit[2])
			w0 = float(lineSplit[3])
			w1 = float(lineSplit[4])
			w2 = float(lineSplit[5])

			realVerts.append((verts[v0], verts[v1], verts[v2], w0, w1, w2))
			addProxyVert(v0, vn, w0, proxyVerts)
			addProxyVert(v1, vn, w1, proxyVerts)
			addProxyVert(v2, vn, w2, proxyVerts)
			vn += 1
		elif doFaces:
			face = []
			texface = []
			nCorners = len(lineSplit)
			for n in range(nCorners):
				words = lineSplit[n].split('/')
				face.append(int(words[0])-1)
				if len(words) > 1:
					texface.append(int(words[1])-1)
			proxyFaces.append(face)
			if texface:
				proxyTexFaces.append(texface)
				if len(face) != len(texface):
					raise NameError("texface %s %s", face, texface)
		elif doTexVerts:
			vt = []
			nCoords = len(lineSplit)
			for n in range(nCoords):
				uv = float(lineSplit[n])
				vt.append(uv)
			proxyTexVerts.append(vt)
		elif doMaterials:
			proxyMaterials.append(int(lineSplit[0]))

	return (proxyName, proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, proxyTexVerts)

def addProxyVert(v, vn, w, proxyVerts):
	try:
		proxyVerts[v].append((vn, w))
	except:
		proxyVerts[v] = [(vn,w)]
	return

def printRealVerts(fp, realVerts, flip):
	for (v0, v1, v2, w0, w1, w2) in realVerts:
		r0 = w0*v0.co[0] + w1*v1.co[0] + w2*v2.co[0]
		r1 = w0*v0.co[1] + w1*v1.co[1] + w2*v2.co[1]
		r2 = w0*v0.co[2] + w1*v1.co[2] + w2*v2.co[2]
		if flip:
			fp.write("v %.6g %.6g %.6g ;\n" % (r0, -r2, r1))
		else:
			fp.write("v %.6g %.6g %.6g ;\n" % (r0, r1, r2))

	
#
#	exportProxyObj(obj, filename):	
#	exportProxyObj1(obj, filename, proxyFile):
#

def exportProxyObj(obj, filename):
	(name, ext) = os.path.splitext(filename)
	proxyList = proxyConfig()
	for proxyFile in proxyList:
		(proxyName, proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, proxyTexVerts) = readProxyFile(obj.verts, proxyFile)
		if proxyName:
			filename = "%s-%s%s" % (name, proxyName, ext)
			exportProxyObj1(obj, filename, proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, proxyTexVerts)
	return

def exportProxyObj1(obj, filename, proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, proxyTexVerts):
	fp = open(filename, 'w')
	fp.write(
"# MakeHuman exported OBJ for proxy mesh\n" +
"# www.makehuman.org\n\n")

	printRealVerts(fp, realVerts, False)

	for uv in proxyTexVerts:
		fp.write("vt %s %s\n" % (uv[0], uv[1]))

	mat = -1
	fn = 0
	for f in proxyFaces:
		if proxyMaterials and proxyMaterials[fn] != mat:
			mat = proxyMaterials[fn]
			fp.write("usemtl %s\n" % matNames[mat])
		fp.write("f")
		if proxyTexFaces:
			ft = proxyTexFaces[fn]
			vn = 0
			for v in f:
				vt = ft[vn]
				fp.write(" %d/%d" % (v+1, vt+1))
				vn += 1
		else:
			for v in f:
				fp.write(" %d" % (v+1))
		fp.write("\n")
		fn += 1
	fp.close()
	return
	

#
#	copyProxy(tmplName, fp, proxyVerts):
#

def copyProxy(tmplName, fp, proxyVerts):
	print("Trying to open "+tmplName)
	tmpl = open(tmplName)
	shapes = []
	vgroups = []

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
				dx = float(lineSplit[2])
				dy = float(lineSplit[3])
				dz = float(lineSplit[4])
				try:
					vlist = proxyVerts[v]
				except:
					vlist = []
				for (pv, w) in vlist:
					shapes.append((pv, w*dx, w*dy, w*dz))
			elif lineSplit[0] == 'wv':
				v = int(lineSplit[1])
				wt = float(lineSplit[2])
				try:
					vlist = proxyVerts[v]
				except:
					vlist = []
				for (pv, w) in vlist:
					vgroups.append((pv, w*wt))
			elif shapes:
				printProxyShape(fp, shapes)
				shapes = []
				fp.write(line)
			elif vgroups:
				printProxyVGroup(fp, vgroups)
				vgroups = []
				fp.write(line)
			else:	
				fp.write(line)
	else:
		for line in tmpl:
			fp.write(line)
	print("Closing "+tmplName)
	tmpl.close()
	return

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
				fp.write("  ShapeKey Basis Sym\n  end ShapeKey\n")
				copyProxy("data/templates/shapekeys-facial25.mhx", fp, None)	
				copyProxy("data/templates/shapekeys-extra24.mhx", fp, None)	
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
	proxyTexVerts = None
	proxyTexFaces = None
	proxyList = proxyConfig()
	try:
		proxyFile = proxyList[0]
	except:
		proxyFile = None
	faces = files3d.loadFacesIndices("data/3dobjs/base.obj")
	fp.write("if useProxy\n")
	for line in tmpl:
		lineSplit= line.split()
		if len(lineSplit) == 0:
			fp.write(line)
		elif lineSplit[0] == 'v':
			(proxyName, proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, proxyTexVerts) = readProxyFile(obj.verts, proxyFile)
			printRealVerts(fp, realVerts, True)
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
			for f in proxyTexFaces:
				fp.write("    vt")
				for v in f:
					uv = proxyTexVerts[v]
					fp.write(" %.6g %.6g" %(uv[0], uv[1]))
				fp.write(" ;\n")
		elif lineSplit[0] == 'vertgroup':
			copyProxy("data/templates/vertexgroups-common25.mhx", fp, proxyVerts)	
			copyProxy("data/templates/vertexgroups-classic25.mhx", fp, proxyVerts)	
			copyProxy("data/templates/vertexgroups-toes25.mhx", fp, proxyVerts)	
		elif lineSplit[0] == 'shapekey':
			fp.write("  ShapeKey Basis Sym\n  end ShapeKey\n")
			copyProxy("data/templates/shapekeys-facial25.mhx", fp, proxyVerts)	
			copyProxy("data/templates/shapekeys-extra24.mhx", fp, proxyVerts)	
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
		shapes = []
		for line in shapeVerts:
			lineSplit = line.split()
			v = int(lineSplit[1])
			dx = float(lineSplit[2])
			dy = float(lineSplit[3])
			dz = float(lineSplit[4])
			try:
				vlist = proxyVerts[v]
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



