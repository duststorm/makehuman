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


TO DO

"""

import module3d, aljabr, files3d
import os


#
#	proxyConfig():
#

def proxyConfig():
	paths = ['~/makehuman/proxy.cfg', '/proxy.cfg', './proxy.cfg']
	
	fp = None
	for path in paths:
		path1 = os.path.expanduser(path)
		fileName = os.path.realpath(path1)
		try:
			fp = open(fileName, "r")
			print("Using config file %s" % fileName)
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
	doObjData = False
	theGroup = None
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
		elif lineSplit[0] == 'ObjData':
			doVerts = False		
			doObjData = True
		elif lineSplit[0] == 'Name':
			proxyName = lineSplit[1]
		elif doObjData:
			if lineSplit[0] == 'vt':
				newTexVert(1, lineSplit, proxyTexVerts)
			elif lineSplit[0] == 'f':
				newFace(1, lineSplit, theGroup, proxyFaces, proxyTexFaces)
			elif lineSplit[0] == 'g':
				theGroup = lineSplit[1]
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
			newFace(0, lineSplit, theGroup, proxyFaces, proxyTexFaces)
		elif doTexVerts:
			newTexVert(0, lineSplit, proxyTexVerts)
		elif doMaterials:
			proxyMaterials.append(int(lineSplit[0]))

	return (proxyName, proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, proxyTexVerts)

def newFace(first, lineSplit, group, proxyFaces, proxyTexFaces):
	face = []
	texface = []
	nCorners = len(lineSplit)
	for n in range(first, nCorners):
		words = lineSplit[n].split('/')
		face.append(int(words[0])-1)
		if len(words) > 1:
			texface.append(int(words[1])-1)
	proxyFaces.append((face,group))
	if texface:
		proxyTexFaces.append(texface)
		if len(face) != len(texface):
			raise NameError("texface %s %s", face, texface)
	return

def newTexVert(first, lineSplit, proxyTexVerts):
	vt = []
	nCoords = len(lineSplit)
	for n in range(first, nCoords):
		uv = float(lineSplit[n])
		vt.append(uv)
	proxyTexVerts.append(vt)
	return

def addProxyVert(v, vn, w, proxyVerts):
	try:
		proxyVerts[v].append((vn, w))
	except:
		proxyVerts[v] = [(vn,w)]
	return

#
#	proxyCoord(barycentric):
#

def proxyCoord(barycentric):
	(v0, v1, v2, w0, w1, w2) = barycentric
	x = w0*v0.co[0] + w1*v1.co[0] + w2*v2.co[0]
	y = w0*v0.co[1] + w1*v1.co[1] + w2*v2.co[1]
	z = w0*v0.co[2] + w1*v1.co[2] + w2*v2.co[2]
	return [x,y,z]

#
#	getMeshInfo(obj, proxyData, rawWeights, rawShapes):
#

def getMeshInfo(obj, proxyData, rawWeights, rawShapes):
	if proxyData == None:
		verts = []
		vnormals = []
		for v in obj.verts:
			verts.append(v.co)
			vnormals.append(v.no)
		faces = files3d.loadFacesIndices("data/3dobjs/base.obj")
		return (verts, vnormals, obj.uvValues, faces, rawWeights, rawShapes)
	else:
		(proxyName, proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, proxyTexVerts) = proxyData

		verts = []
		vnormals = []
		for bary in realVerts:
			v = proxyCoord(bary)
			verts.append(v)
			vnormals.append(v)

		faces = []
		fn = 0
		for (f,g) in proxyFaces:
			texFace = proxyTexFaces[fn]
			face = []
			for (vn,v) in enumerate(f):
				face.append((v, texFace[vn]))
			faces.append(face)
			fn += 1

		weights = getProxyWeights(rawWeights, proxyVerts)
		shapes = getProxyShapes(rawShapes, proxyVerts)
		return (verts, vnormals, proxyTexVerts, faces, weights, shapes)

#
#	getProxyWeights(rawWeights, proxyVerts):
#	fixProxyVGroup(fp, vgroup):
#

def getProxyWeights(rawWeights, proxyVerts):
	weights = {}
	for key in rawWeights.keys():
		vgroup = []
		for (v,wt) in rawWeights[key]:
			try:
				vlist = proxyVerts[v]
			except:
				vlist = []
			for (pv, w) in vlist:
				vgroup.append((pv, w*wt))
		weights[key] = fixProxyVGroup(vgroup)
	return weights

def fixProxyVGroup(vgroup):
	fixedVGroup = []
	vgroup.sort()
	pv = -1
	while vgroup:
		(pv0, wt0) = vgroup.pop()
		if pv0 == pv:
			wt += wt0
		else:
			if pv >= 0 and wt > 1e-4:
				fixedVGroup.append((pv, wt))
			(pv, wt) = (pv0, wt0)
	if pv >= 0 and wt > 1e-4:
		fixedVGroup.append((pv, wt))
	return fixedVGroup

#
#	getProxyShapes(rawShapes, proxyVerts):
#	fixProxyShape(fp, shape)
#

def getProxyShapes(rawShapes, proxyVerts):
	shapes = []
	for (key, rawShape) in rawShapes:
		shape = []
		for (v,(dx,dy,dz)) in rawShape.items():
			try:
				vlist = proxyVerts[v]
			except:
				vlist = []
			for (pv, w) in vlist:
				shape.append((pv, w*dx, w*dy, w*dz))
		fixedShape = fixProxyShape(fp, shape)

		shape = {}
		for (v,dx,dy,dz) in fixedShape:
			shape[v] = (dx,dy,dz)
		shapes.append(shape)
	return shapes

def fixProxyShape(shape):
	fixedShape = []
	shape.sort()
	pv = -1
	while shape:
		(pv0, dx0, dy0, dz0) = shape.pop()
		if pv0 == pv:
			dx += dx0
			dy += dy0
			dz += dz0
		else:
			if pv >= 0 and (dx > 1e-4 or dy > 1e-4 or dz > 1e-4):
				fixedShape.append((pv, dx, dy, dz))
			(pv, dx, dy, dz) = (pv0, dx0, dy0, dz0)		
	if pv >= 0 and (dx > 1e-4 or dy > 1e-4 or dz > 1e-4):
		fixedShape.append((pv, dx, dy, dz))
	return fixedShape

#
#	exportProxyObj(obj, filename):	
#	exportProxyObj1(obj, filename, proxyData):
#

def exportProxyObj(obj, name):
	proxyList = proxyConfig()
	for proxyFile in proxyList:
		proxyData = readProxyFile(obj.verts, proxyFile)
		(proxyName, proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, proxyTexVerts) = proxyData
		if proxyName:
			filename = "%s-%s.obj" % (name, proxyName)
			exportProxyObj1(obj, filename, proxyData)
	return

def exportProxyObj1(obj, filename, proxyData):
	(proxyName, proxyVerts, realVerts, proxyFaces, proxyMaterials, proxyTexFaces, proxyTexVerts) = proxyData
	fp = open(filename, 'w')
	fp.write(
"# MakeHuman exported OBJ for proxy mesh\n" +
"# www.makehuman.org\n\n")

	for bary in realVerts:
		(x,y,z) = proxyCoord(bary)
		fp.write("v %.6g %.6g %.6g\n" % (x, y, z))

	for uv in proxyTexVerts:
		fp.write("vt %s %s\n" % (uv[0], uv[1]))

	mat = -1
	fn = 0
	grp = None
	for (f,g) in proxyFaces:
		if proxyMaterials and proxyMaterials[fn] != mat:
			mat = proxyMaterials[fn]
			fp.write("usemtl %s\n" % matNames[mat])
		if g != grp:
			fp.write("g %s\n" % g)
			grp = g
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
	

