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
from aljabr import *


#
#	class CProxy
#	class CMaterial
#

class CProxy:
	def __init__(self, typ, layer):
		self.name = None
		self.type = typ
		self.layer = layer
		self.material = None
		self.verts = {}
		self.realVerts = []
		self.faces = []
		self.texFaces = []
		self.texVerts = []
		self.materials = []
		self.bones = []
		self.weights = {}
		self.weighted = False
		self.wire = False
		self.cage = False
		self.modifiers = []

class CMaterial:
	def __init__(self, name):
		self.name = name
		self.diffuse_color = None
		self.diffuse_intensity = None
		self.diffuse_shader = None
		self.specular_color = None
		self.specular_intensity = None
		self.specular_shader = None
		return
#
#	Flags
#

F_CON = 0x01

#
#	proxyFilePtr(name):
#

def proxyFilePtr(name):
	for path in ['~/makehuman/', '/', './']:
		path1 = os.path.expanduser(path+name)
		fileName = os.path.realpath(path1)
		try:
			fp = open(fileName, "r")
			print("Using config file %s" % fileName)
			return fp
		except:
			print("No file %s" % fileName)
	return None
	
#
#	proxyConfig():
#

def proxyConfig():
	fp = proxyFilePtr('proxy.cfg')
	if not fp: return []	
	proxyList = []
	typ = 'Proxy'
	layer = 2
	useMhx = True
	useObj = True
	for line in fp:
		words = line.split()
		if len(words) == 0 or words[0][0] == '#':
			pass
		elif words[0] == '@':
			if words[1] == 'Obj':
				useObj = eval(words[2])
			elif words[1] == 'Mhx':
				useMhx = eval(words[2])
			else:
				typ = words[1]
				layer = int(words[2])
		else:
			proxyFile = os.path.expanduser(words[0])
			proxyList.append((typ, useObj, useMhx, (proxyFile, typ, layer)))
	fp.close()
	print(proxyList)
	return proxyList

	
#
#	readProxyFile(obj, proxyStuff):
#

def readProxyFile(obj, proxyStuff):
	if not proxyStuff:
		return CProxy('Proxy', 2)

	(proxyFile, typ, layer) = proxyStuff
	try:
		tmpl = open(proxyFile, "rU")
	except:
		tmpl = None
	if tmpl == None:
		print("Cannot open proxy file %s" % proxyFile)
		return CProxy(typ, layer)

	verts = obj.verts
	locations = {}
	tails = {}
	proxy = CProxy(typ, layer)
	proxy.name = "MyProxy"

	vn = 0
	for line in tmpl:
		words= line.split()
		if len(words) == 0:
			pass
		elif words[0] == '#':
			doVerts = False
			doFaces = False
			doMaterial = False
			doTexVerts = False
			doObjData = False
			doBones = False
			weightBone = None
			theGroup = None
			if len(words) == 1:
				pass
			elif words[1] == 'verts':
				doVerts = True
			elif words[1] == 'faces':
				doFaces = True
			elif words[1] == 'bones':
				return proxy
				doBones = True
			elif words[1] == 'weights':
				weightBone = words[2]
				proxy.weights[weightBone] = []
				proxy.weighted = True
			elif words[1] == 'material':
				doMaterial = True
				proxy.material = CMaterial(words[2])
			elif words[1] == 'texVerts':
				doTexVerts = True
			elif words[1] == 'obj_data':
				doObjData = True
			elif words[1] == 'name':
				proxy.name = words[2]
			elif words[1] == 'wire':
				proxy.wire = True
			elif words[1] == 'cage':
				proxy.cage = True
			elif words[1] == 'subsurf':
				subdiv = int(words[2])
				proxy.modifiers.append( ['subsurf', subdiv] )
			elif words[1] == 'shrinkwrap':
				offset = float(words[2])
				proxy.modifiers.append( ['shrinkwrap', offset] )
		elif doObjData:
			if words[0] == 'vt':
				newTexVert(1, words, proxy)
			elif words[0] == 'f':
				newFace(1, words, theGroup, proxy)
			elif words[0] == 'g':
				theGroup = words[1]
		elif doVerts:
			v0 = int(words[0])
			v1 = int(words[1])
			v2 = int(words[2])
			w0 = float(words[3])
			w1 = float(words[4])
			w2 = float(words[5])
			try:
				proj = float(words[6])
			except:
				proj = 0

			if proj:
				n0 = aljabr.vmul(verts[v0].no, w0)
				n1 = aljabr.vmul(verts[v1].no, w1)
				n2 = aljabr.vmul(verts[v2].no, w2)
				norm = aljabr.vadd(n0, n1)
				norm = aljabr.vadd(norm, n2)
				d0 = proj*norm[0]
				d1 = proj*norm[1]
				d2 = proj*norm[2]
			else:
				(d0, d1, d2) = (0, 0, 0)

			proxy.realVerts.append((verts[v0], verts[v1], verts[v2], w0, w1, w2, d0, d1, d2))
			addProxyVert(v0, vn, w0, proxy)
			addProxyVert(v1, vn, w1, proxy)
			addProxyVert(v2, vn, w2, proxy)
			vn += 1
		elif doFaces:
			newFace(0, words, theGroup, proxy)
		elif doTexVerts:
			newTexVert(0, words, proxy)
		elif doMaterial:
			readMaterial(line, proxy.material)
		elif doBones:
			bone = words[0]
			head = getJoint(words[1], obj, locations)
			tail = getJoint(words[2], obj, locations)
			roll = float(words[3])
			if words[4] == '-':
				parent = None
			else:
				parent = words[4]			
			tails[bone] = tail
			flags = 0
			if parent:
				offs = vsub(head, tails[parent])
				if vlen(offs) < 1e-4:
					flags |= F_CON
			proxy.bones.append((bone,head,tail,roll,parent,flags))
		elif weightBone:
			v = int(words[0])
			w = float(words[1])
			proxy.weights[weightBone].append((v,w))

	return proxy

#
#	readMaterial(line, mat):
#

def readMaterial(line, mat):
	words= line.split()
	key = words[0]
	if key == 'diffuse_color':
		mat.diffuse_color = (float(words[1]), float(words[2]), float(words[3]))
	elif key == 'diffuse_shader':
		mat.diffuse_shader = words[1]
	elif key == 'diffuse_intensity':
		mat.diffuse_intensity = float(words[1])
	elif key == 'specular_color':
		mat.specular_color = (float(words[1]), float(words[2]), float(words[3]))
	elif key == 'specular_shader':
		mat.specular_shader = words[1]
	elif key == 'specular_intensity':
		mat.specular_intensity = float(words[1])
	else:
		raise NameError("Material %s?" % key)

#
#	getLoc(joint, obj):
#

import mhxbones

def getJoint(joint, obj, locations):
	try:
		loc = locations[joint]
	except:
		loc = mhxbones.calcJointPos(obj, joint)
		locations[joint] = loc
	return loc

#
#	writeProxyArmature(fp, proxy)
#	writeProxyBone(fp, boneInfo):	
#	writeProxyPose(fp, proxy):
#	writeProxyWeights(fp, proxy):
#

def writeProxyArmature(fp, proxy):
	for boneInfo in proxy.bones:
		writeProxyBone(fp, boneInfo)
	return

def writeProxyBone(fp, boneInfo):
	(bone,head,tail,roll,parent,flags) = boneInfo

	fp.write("\n  Bone %s True\n" % bone)
	(x, y, z) = head
	fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,-z,y))
	(x, y, z) = tail
	fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,-z,y))
	if parent:
		fp.write("    parent Refer Bone %s ; \n" % (parent))

	if flags & F_CON:
		conn = True
	else:
		conn = False
	
	fp.write(
"    roll %.6g ; \n" % (roll)+
"    use_connect %s ; \n" % (conn) +
"    use_deform True ; \n" +
"  end Bone \n")
	return

def writeProxyPose(fp, proxy):
	fp.write("\nPose %s" % proxy.name)
	for boneInfo in proxy.bones:
		(bone,head,tail,roll,parent,flags) = boneInfo			
		if parent:
			fp.write("\n" +
"  Posebone %s True \n" % bone +
"    lock_location Array 1 1 1 ;\n" +
"    lock_scale Array 1 1 1  ; \n"+
"  end Posebone\n")
	fp.write("\n"+
"end Pose\n\n")

def writeProxyWeights(fp, proxy):
	for grp in proxy.weights.keys():
		fp.write("\n  VertexGroup %s\n" % grp)
		for (v,w) in proxy.weights[grp]:
			fp.write("    wv %d %.4f ;\n" % (v,w))
		fp.write("  end VertexGroup\n")
	return

#
#	newFace(first, words, group, proxy):
#	newTexVert(first, words, proxy):
#	addProxyVert(v, vn, w, proxy):
#

def newFace(first, words, group, proxy):
	face = []
	texface = []
	nCorners = len(words)
	for n in range(first, nCorners):
		numbers = words[n].split('/')
		face.append(int(numbers[0])-1)
		if len(numbers) > 1:
			texface.append(int(numbers[1])-1)
	proxy.faces.append((face,group))
	if texface:
		proxy.texFaces.append(texface)
		if len(face) != len(texface):
			raise NameError("texface %s %s", face, texface)
	return

def newTexVert(first, words, proxy):
	vt = []
	nCoords = len(words)
	for n in range(first, nCoords):
		uv = float(words[n])
		vt.append(uv)
	proxy.texVerts.append(vt)
	return

def addProxyVert(v, vn, w, proxy):
	try:
		proxy.verts[v].append((vn, w))
	except:
		proxy.verts[v] = [(vn,w)]
	return

#
#	proxyCoord(barycentric):
#

def proxyCoord(barycentric):
	(v0, v1, v2, w0, w1, w2, d0, d1, d2) = barycentric
	x = w0*v0.co[0] + w1*v1.co[0] + w2*v2.co[0] + d0
	y = w0*v0.co[1] + w1*v1.co[1] + w2*v2.co[1] + d1
	z = w0*v0.co[2] + w1*v1.co[2] + w2*v2.co[2] + d2
	return [x,y,z]

#
#	getMeshInfo(obj, proxy, rawWeights, rawShapes):
#

def getMeshInfo(obj, proxy, rawWeights, rawShapes):
	if proxy:
		verts = []
		vnormals = []
		for bary in proxy.realVerts:
			v = proxyCoord(bary)
			verts.append(v)
			vnormals.append(v)

		faces = []
		fn = 0
		for (f,g) in proxy.faces:
			texFace = proxy.texFaces[fn]
			face = []
			for (vn,v) in enumerate(f):
				face.append((v, texFace[vn]))
			faces.append(face)
			fn += 1

		if proxy.weighted:
			weights = proxy.weights
		else:
			weights = getProxyWeights(rawWeights, proxy)
		shapes = getProxyShapes(rawShapes, proxy.verts)
		return (verts, vnormals, proxy.texVerts, faces, weights, shapes)
	else:
		verts = []
		vnormals = []
		for v in obj.verts:
			verts.append(v.co)
			vnormals.append(v.no)
		faces = files3d.loadFacesIndices("data/3dobjs/base.obj")
		return (verts, vnormals, obj.uvValues, faces, rawWeights, rawShapes)

#
#	getProxyWeights(rawWeights, proxy):
#	fixProxyVGroup(fp, vgroup):
#

def getProxyWeights(rawWeights, proxy):
	weights = {}
	for key in rawWeights.keys():
		vgroup = []
		for (v,wt) in rawWeights[key]:
			try:
				vlist = proxy.verts[v]
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
#	getProxyShapes(rawShapes, proxy):
#	fixProxyShape(fp, shape)
#

def getProxyShapes(rawShapes, proxy):
	shapes = []
	for (key, rawShape) in rawShapes:
		shape = []
		for (v,(dx,dy,dz)) in rawShape.items():
			try:
				vlist = proxy.verts[v]
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
#	exportProxyObj1(obj, filename, proxy):
#

def exportProxyObj(obj, name):
	proxyList = proxyConfig()
	for (typ, useObj, useMhx, proxyStuff) in proxyList:
		if useObj:
			proxy = readProxyFile(obj, proxyStuff)
			if proxy.name:
				filename = "%s_%s.obj" % (name.lower(), proxy.name)
				exportProxyObj1(obj, filename, proxy)
	return

def exportProxyObj1(obj, filename, proxy):
	fp = open(filename, 'w')
	fp.write(
"# MakeHuman exported OBJ for proxy mesh\n" +
"# www.makehuman.org\n\n")

	for bary in proxy.realVerts:
		(x,y,z) = proxyCoord(bary)
		fp.write("v %.6g %.6g %.6g\n" % (x, y, z))

	for uv in proxy.texVerts:
		fp.write("vt %s %s\n" % (uv[0], uv[1]))

	mat = -1
	fn = 0
	grp = None
	for (f,g) in proxy.faces:
		if proxy.materials and proxy.materials[fn] != mat:
			mat = proxy.materials[fn]
			fp.write("usemtl %s\n" % matNames[mat])
		if g != grp:
			fp.write("g %s\n" % g)
			grp = g
		fp.write("f")
		if proxy.texFaces:
			ft = proxy.texFaces[fn]
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
	

