#!BPY
""" 
Name: 'Makehuman (.mhx)'
Blender: 249
Group: 'Import'
Tooltip: 'Import from MakeHuman eXchange format (.mhx)'
"""

__author__= ['Thomas Larsson']
__url__ = ("www.makehuman.org")
__version__= '1.0'
__bpydoc__= '''\
MHX exporter for Blender
'''
""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         GPL3 (see also http://www.makehuman.org/node/319)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

MHX (MakeHuman eXchange format) importer for Blender.

TODO
"""

import Blender
from Blender import *
from Blender.Mathutils import *
import os
import bpy
import string

#
#	Default locations - change to fit your machine
#

TexDir = os.path.expanduser("~/makehuman/exports")

#
#
#

MAJOR_VERSION = 1
MINOR_VERSION = 0

#
#	Button flags
#

toggleArmIK = 0
toggleLegIK = 0
toggleFKIK = 0
toggleFingerIK = 0
toggleDispObs = 1
toggleReplace = 1
toggleFace = 1
toggleShape = 0
toggleRot90 = 1
useMesh = 1
useArmature = 1
useProxy = 0
doSmash = 1
warnedTextureDir = False
Blender24 = True
Blender25 = False


#
#	Dictionaries
#

true = True
false = False
Epsilon = 1e-6
nErrors = 0

_object = dict()
_mesh = dict()
_block = dict()
_armature = dict()
_lamp = dict()
_camera = dict()
_lattice = dict()
_particle = dict()
_material = dict()
_texture = dict()
_curve = dict()
_lattice = dict()
_text3d = dict()
_action = dict()
_ipo = dict()
_icu = dict()
_group = dict()
_joint = dict()

todo = []

#
#	readMhxFile(fileName):
#

def readMhxFile(fileName):
	global todo, nErrors, Blender25, Blender24
	
	scn = Scene.GetCurrent()
	scn = clearScene(scn)

	ignore = False
	stack = []
	tokens = []
	key = "toplevel"
	level = 0
	nErrors = 0
	comment = 0
	nesting = 0

	print "Opening MHX file "+ fileName
	file= open(fileName, "rU")
	print "Tokenizing"
	lineNo = 0
	for line in file: 
		lineSplit= line.split()
		lineNo += 1
		if len(lineSplit) == 0:
			pass
		elif lineSplit[0][0] == '#':
			if lineSplit[0] == '#if':
				if comment == nesting:
					print('eval', line, nesting, comment)
					try:
						res = eval(lineSplit[1])
					except:
						res = False
					print('res', res)
					if res:
						comment += 1
				nesting += 1
				print(line, nesting, comment)
			elif lineSplit[0] == '#else':
				if comment == nesting-1:
					comment += 1
				elif comment == nesting:
					comment -= 1
				print(line, nesting, comment)
			elif lineSplit[0] == '#endif':
				if comment == nesting:
					comment -= 1
				nesting -= 1
				print(line, nesting, comment)
		elif comment < nesting:
			#print(line)
			pass
		elif lineSplit[0] == 'end':
			try:
				sub = tokens
				tokens = stack.pop()
				if tokens:
					tokens[-1][2] = sub
				level -= 1
				#(key,val,sub) = tokens[-1]
				#print "pop  ", level+1, key
				#if stack == []:
				#	parse(scn, tokens)
				#	tokens = []
			except:
				print "Tokenizer error at or before line", lineNo
				print line
				dummy = stack.pop()
		elif lineSplit[-1] == ';':
			key = lineSplit[0]
			tokens.append([key,lineSplit[1:-1],[]])
		else:
			key = lineSplit[0]
			tokens.append([key,lineSplit[1:],[]])
			stack.append(tokens)
			level += 1
			#print "push ", level, key
			tokens = []
	file.close()

	if level != 0:
		raise NameError("Tokenizer out of kilter %d" % level)	
	print "Parsing"
	parse(scn, tokens)
	
	for (expr, globals, locals) in todo:
		try:
			exec(expr, globals, locals)
		except:
			msg = "Failed: "+expr
			print msg
			nErrors += 1
			#raise NameError(msg)

	#postProcess()
	scn.update()
	context = scn.getRenderingContext()
	context.rayTracing = False
	
	for ob in scn.objects:
		ob.sel = 1
		Window.EditMode(1)
		Window.EditMode(0)
		ob.sel = 0
	
	msg = "File "+fileName+" loaded"
	if nErrors:
		msg += " but there where %d errors. " % (nErrors)
	print(msg)
	#Draw.PupMenu(msg)
	return	# readMhxFile

#
#	defaultKey(ext, val, var, globals, locals):
#

def defaultKey(ext, val, var, globals, locals):
	nargs = len(val)-1
	if nargs == 0:
		expr = var+"."+ext+" = "+val[0]
		try:
			exec(expr, globals, locals)
		except:
			todo.append((expr, globals, locals))
	else:
		for n in range(nargs):
			expr  = var+"."+ext+"["+str(n)+"] = "+val[n]
			try:
				exec(expr, globals, locals)
			except:
				todo.append((expr, globals, locals))

#
#	getObject(name, var, globals, locals):
#

def getObject(name, var, globals, locals):
	try:
		ob = _object[name]
	except:
		if name != "None":
			expr = var+" = _object['"+name+"']"
			todo.append((expr, globals, locals))
		ob = None
	return ob

#
#	getIpo(name, var, globals, locals):
#

def getIpo(name, var, globals, locals):
	try:
		ipo = _ipo[name]
	except:
		if name != "None":
			expr = var+" = _ipo['"+name+"']"
			todo.append((expr, globals, locals))
		ipo = None
	return ipo

#
#	getAction(name, var, globals, locals):
#

def getAction(name, var, globals, locals):
	try:
		act = _action[name]
	except:
		if False and name != "None":
			expr = var+" = _action['"+name+"']"
			todo.append((expr, globals, locals))
		act = None
	# print "getact ", act
	return act

#
#	parse(tokens):
#

def parse(scn, tokens):
	for (key, val, sub) in tokens:	
		if key == 'MHX':
			if (int(val[0]) != MAJOR_VERSION or int(val[1]) != MINOR_VERSION):
				Draw.PupMenu("Warning: \nThis file was created with another version of MHX\n")
			data = None
		#elif key == 'if':
		#	try:
		#		res = eval(val[0])
		#	except:
		#		res = False
		#	if res:
		#		parse(val, sub)
		elif key == 'print':
			msg = concatList(val)
			print(msg)
		elif key == 'warn':
			msg = concatList(val)
			Draw.PupMenu("Warning: %s" % msg)
			print(msg)
		elif key == 'error':
			msg = concatList(val)
			raise NameError(msg)			
		elif key == "action":
			data = parseAction(val, sub)
		elif key == "ipo":
			data = parseIpo(val, sub)
		elif key == "material":
			data = parseMaterial(val, sub)
		elif key == "texture":
			data = parseTexture(val, sub)
		elif key == "pose":
			data = parsePose(val, sub)
		elif key == "mesh":
			data = parseMesh(val, sub)
		elif key == "armature":
			data = parseArmature(val, sub)
		elif key == "camera":
			data = parseCamera(val, sub)
		elif key == "lamp":
			data = parseLamp(val, sub)
		elif key == "lattice":
			data = parseLattice(val, sub)
		elif key == "curve":
			data = parseCurve(val, sub)
		elif key == "text":
			data = parseText(val, sub)
		elif key == "empty":
			data = None
		elif key == "group":
			data = parseGroup(val, sub)
		elif key == "object":
			parseObject(scn, val, sub)
			data = None
		elif key == "joints":
			parseJoints(val, sub)
			data = None
		else:
			raise NameError( "parse: unknown key: " + key )
		
		if data:
			print data

#
#	concatList(elts)
#

def concatList(elts):
	string = ""
	for elt in elts:
		string += " %s" % elt
	return string

#
#	parseObject(scn, args, tokens):
#

def parseObject(scn, args, tokens):
	name = args[0]
	type = args[1]
	
	try:
		datName = args[2]
	except:
		datName = None

	if type == "Mesh":
		data = _mesh[datName]
	elif type == "Armature":
		data = _armature[datName]
	elif type == "Camera":
		data = _camera[datName]
	elif type == "Lamp":
		data = _lamp[datName]
	elif type == "Curve":
		data = _curve[datName]
	elif type == "Lattice":
		data = _lattice[datName]
	elif type == "Text":
		data = _text3d[datName]
	elif type == "Empty":
		data = None
	else:
		raise NameError("Unknown object type "+type)

	if type == "Mesh" or type == "Armature":
		ob = _object[name]
	else:
		ob = createObject(name, data)

	for (key, val, sub) in tokens:
		if key == "layers":
			lay1 = int(val[0], 16) & 0x3ff
			lay2 = int(val[1], 16) & 0x3ff
			ob.Layers = lay1 | (lay2 << 10)
		elif key == "matrix":
			matrix = parseMatrix(val, sub)
			ob.setMatrix(matrix)
		elif key == 'ipo':
			ob.setIpo(_ipo[val[0]])
		elif key == "modifier":
			parseModifier(ob, val,sub)
		elif key == "parent":
			parseParent(ob, val,sub)
		elif key == "constraint":
			parseConstraint(ob.constraints, val, sub, name)
		elif key == "particle":
			parseParticle(ob, val, sub)
		else:
			defaultKey(key, val, "ob", globals(), locals())

#
#	createObject(scn, name, data):
#

def createObject(name, data):
	scn = Scene.GetCurrent()
	if data:
		ob = scn.objects.new(data)
	else:
		ob = scn.objects.new('Empty')
	ob.name = name
	_object[name] = ob
	print ob
	return ob

#
#	parseMatrix(args, tokens)
#

def parseMatrix(args, tokens):
	matrix = Matrix( [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1] )
	i = 0
	for (key, val, sub) in tokens:
		if key == 'row':	
			matrix[i][0] = float(val[0])
			matrix[i][1] = float(val[1])
			matrix[i][2] = float(val[2])
			matrix[i][3] = float(val[3])
			i += 1
	return matrix

#
#	parseParent(ob, args, tokens):
#

def parseParent(ob, args, tokens):
	global todo
	parent = args[0]
	parentType = int(args[1])
	extra = args[2]
	expr = None

	if parentType == Object.ParentTypes.OBJECT: 
		expr = "_object[parent].makeParent([ob])"
	elif parentType == Object.ParentTypes.CURVE:
		expr = "_object[parent].makeParentDeform([ob])"
	elif parentType == Object.ParentTypes.LATTICE:
		expr = "_object[parent].makeParentDeform([ob])"
	elif parentType == Object.ParentTypes.ARMATURE:
		expr = "_object[parent].makeParentDeform([ob])"
	elif parentType == Object.ParentTypes.VERT1: 
		expr = "_object[parent].makeParentVertex([ob], (int(extra)))"
	elif parentType == Object.ParentTypes.VERT3: 
		verts = extra.split("_")
		if (ob.type != "Empty"):
			expr = "_object[parent].makeParentVertex([ob], (int(verts[0]), int(verts[1]), int(verts[2])) )"
	elif parentType == Object.ParentTypes.BONE: 
		if extra != "None":
			expr = "_object[parent].makeParentBone([ob], extra)"

	if expr:
		try:
			exec(expr)
		except:
			todo.append((expr, globals(), locals()))

#
#	parseAction(args, tokens):
#

def parseAction(args, tokens):
	global todo
	name = args[0]
	act = Armature.NLA.NewAction(name)
	_action[name] = act
	for (key, val, sub) in tokens:
		if key == 'ipo':
			# act.append(_ipo[val[0]])
			pass
		else:
			defaultKey(key, val, "act", globals(), locals())
	return act

#
#	parseIpo(args, tokens):
#

def parseIpo(args, tokens):
	global todo
	typeName = args[0]
	name = args[1]
	ipo = Ipo.New(typeName,name)
	_ipo[name] = ipo
	
	for (key, val, sub) in tokens:
		if key == 'icu':
			parseIcu(ipo, val, sub)
		else:
			defaultKey(key, val, "ipo", globals(), locals())
	return ipo

def parseLocalIpo(args, tokens, owner, ipoType):
	global todo
	typeName = args[0]
	name = args[1]
	owner.ipo = Ipo.New(ipoType, name)
	ipo = owner.ipo
	_ipo[name] = ipo
	
	for (key, val, sub) in tokens:
		if key == 'icu':
			if (typeName != 'Key' or doShape(val[0])):
				parseIcu(ipo, val, sub)
		else:
			defaultKey(key, val, "ipo", globals(), locals())
	return ipo

#
#	parseIcu(ipo, args, tokens):
#

def parseIcu(ipo, args, tokens):
	global todo
	name = args[0]
	try:
		icu = ipo.addCurve(name)
		_icu[name] = icu
	except:
		print "Cannot add Ipo-curve %s" % name
		return

	for (key, val, sub) in tokens:
		if key == 'bz2':
			h1x = float(val[0])
			h1y = float(val[1])
			px = float(val[2])
			py = float(val[3])
			h2x = float(val[4])
			h2y = float(val[5])
			#bz = BezTriple.New(h1x,h1y,0, px,py,0, h2x,h2y,0)
			#icu.bezierPoints.append((px,py))
			icu.addBezier((px,py))
		elif key == 'driverBone':
			try:
				defaultKey(key, val, "icu", globals(), locals())
			except:
				blenderWarning()

		else:
			defaultKey(key, val, "icu", globals(), locals())

	return icu

#
#	parseMaterial(args, tokens):
#

def parseMaterial(args, tokens):
	global todo
	name = args[0]
	mat = Material.New(name)
	_material[name] = mat
	for (key, val, sub) in tokens:
		if key == 'rgba':
			mat.R = float(val[0])
			mat.G = float(val[1])
			mat.B = float(val[2])
			mat.alpha = float(val[3])
		elif key == 'mtex':
			index = int(val[0])
			texname = val[1]
			mat.setTexture(index, _texture[texname])
			mtex = mat.textures[index]
			parseMTex(mtex, val, sub)
		elif key == 'ipo':
			parseLocalIpo(val, sub, mat, 'Material')
		elif key == 'colorbandDiffuse':
			mat.colorbandDiffuse = parseColorBand(sub)
		elif key == 'colorbandSpecular':
			mat.colorbandSpecular = parseColorBand(sub)
		else:
			defaultKey(key, val, "mat", globals(), locals())

#
#
#

def parseMTex(mtex, args, tokens):
	global todo
	name = args[1]
	for (key, val, sub) in tokens:
		if key == 'ipo':
			mtex.setIpo(_ipo[val[0]]) 
		else:
			defaultKey(key, val, "mtex", globals(), locals())
	return mtex

			
			
#
#	parseTexture(args, tokens):
#

def parseTexture(args, tokens):
	global todo
	typename = args[0]
	name = args[1]
	tex = Texture.New( name ) 
	tex.type = Texture.Types[typename]
	_texture[name] = tex
	for (key, val, sub) in tokens:
		if key == 'colorband':
			tex.colorband = parseColorBand(sub)
		elif key == 'image':
			tex.image = parseImage(val, sub)
		elif key == 'ipo':
			parseLocalIpo(val, sub, tex, 'Texture')
		else:
			defaultKey(key, val, "tex", globals(), locals())
	return tex

def parseColorBand(args):
	list = []
	for (key, val, sub) in args:
		list.append([float(val[0]), float(val[1]), float(val[2]), float(val[3]), float(val[4])])
	return list
	
#
#	parseFileName(filepath, dir):
#

def doLoadImage(filepath):		
	path1 = os.path.expanduser(filepath)
	file1 = os.path.realpath(path1)
	if os.path.isfile(file1):
		print "Found file "+file1
		try:
			img = Image.Load(file1)
			return img
		except:
			print "Cannot read image"
			return None
	else:
		print "No file "+file1
		return None


def loadImage(filepath):
	global TexDir, warnedTextureDir
	path1 = os.path.expanduser(filepath)
	file1 = os.path.realpath(path1)
	(path, filename) = os.path.split(file1)
	(name, ext) = os.path.splitext(filename)
	print "Loading ", filepath, " = ", filename

	img = doLoadImage(TexDir+"/"+name+".png")
	if img:
		return img

	img = doLoadImage(TexDir+"/"+filename)
	if img:
		return img

	img = doLoadImage(path+"/"+name+".png")
	if img:
		return img

	img = doLoadImage(path+"/"+filename)
	if img:
		return img

	if warnedTextureDir:
		return None
	warnedTextureDir = True
	TexDir = Draw.PupStrInput("TexDir? ", path, 100)

	img =  doLoadImage(TexDir+"/"+name+".png")
	if img:
		return img

	img = doLoadImage(TexDir+"/"+filename)
	return img
	
#
#	parseImage(args, tokens):
#

def parseImage(args, tokens):
	global todo
	img = None
	for (key, val, sub) in tokens:
		if key == 'filename':
			filename = val[0]
			for n in range(len(val)-1):
				filename += " " + val[n+1]
			img = loadImage(filename)
		else:
			defaultKey(key, val, "img", globals(), locals())
	print "Image ", img
	return img

#
#	rot90(x, y, z, doRot)
#

def rot90(x, y, z, doRot):
	global toggleRot90
	if toggleRot90 and doRot:
		return (float(x), -float(z), float(y))
	else:
		return (float(x), float(y), float(z))


#
#	parseMesh (args, tokens):
#

def parseMesh (args, tokens):
	global todo
	print "parsing mesh %s" % (args[0])
	editmode = Window.EditMode()   
	if editmode: Window.EditMode(0)

	name = args[0]
	me = bpy.data.meshes.new(name)
	if name == 'HumanMesh':
		mainMesh = True
	else:
		mainMesh = False
	_mesh[name] = me
	verts = []
	edges = []
	faces = []
	vertsTex = []
	texFaces = []

	for (key, val, sub) in tokens:
		if key == 'v':
			coords = rot90(val[0], val[1], val[2], mainMesh)
			verts.append( coords )
		elif key == 'e':
			edges.append((int(val[0]), int(val[1])))
		elif key == 'f':
			faceLocVerts = []
			faceTexVerts = []
			for vv in val:
				v = vv.split('/')
				faceLocVerts.append(int(v[0]))
				if len(v) > 1 and v[1]:
					faceTexVerts.append(int(v[1]))
			if len(v) == 1:
				faces.append( faceLocVerts )
			else:
				faces.append( faceLocVerts )
				texFaces.append( faceTexVerts )

		elif key == 'vt':
			vertsTex.append( (float(val[0]), float(val[1])) ) 

	me.verts.extend(verts)   
	if faces:
		me.faces.extend(faces)    
	else:
		me.edges.extend(edges)

	# UVs
	
	if texFaces != [] and me.faces:
		me.faceUV= 1
		for n,ft in enumerate(texFaces):
			for i,uv in enumerate(me.faces[n].uv):
				(uv.x, uv.y) = vertsTex[ft[i]]
	

	# Create object here
	ob = createObject(args[1], me)

	mats = []
	noShapes = True
	for (key, val, sub) in tokens:
		if key == 'v' or \
			 key == 'e' or \
			 key == 'f' or \
			 key == 'vt':
				pass

		elif key == 'ft':
			f = me.faces[int(val[0])]
			f.flag = int(val[1],16)
			f.mode = int(val[2],16)
			f.transp = int(val[3])
			f.mat = int(val[4])
			f.smooth = int(val[5])

		elif key == 'ftall':
			flag = int(val[0],16)
			mode = int(val[1],16)
			transp = int(val[2])
			mat = int(val[3])
			smooth = int(val[4])
			for f in me.faces:
				f.flag = flag
				f.mode = mode
				f.transp = transp
				f.mat = mat
				f.smooth = smooth

		elif key == 'fx':
			f = me.faces[int(val[0])]
			f.mat = int(val[1])
			f.smooth = int(val[2])

		elif key == 'fxall':
			mat = int(val[0])
			smooth = int(val[1])
			for f in me.faces:
				f.mat = mat
				f.smooth = smooth

		elif key == 'VertexGroup':
			parseVertGroup(me, val, sub)
		elif key == 'ShapeKey':
			if doShape(val[0]):
				noShapes = False
				parseShapeKey(ob, me, val, sub)
		elif key == 'ipo':
			if toggleShape or toggleFace:
				parseLocalIpo(val, sub, me.key, 'Key')
		elif key == 'material':
			mat = _material[val[0]]
			mats.append(mat)
		else:
			defaultKey(key, val, "me", globals(), locals())

	me.materials = mats
	if mainMesh and noShapes:
		deleteDiamonds(me)

	return me

#
#	deleteDiamonds(me):
#	Unfortunately verts cannot be removed from a mesh with shape keys
#

def deleteDiamonds(me):
	vnums = {}
	for f in me.faces:		
		if len(f.verts) < 4:
			for v in f.verts:
				vnums[v.index] = True
	verts = list(vnums.keys())
	verts.sort()
	#print(verts)
	me.verts.delete(verts)
	return


def doShape(name):
	if (toggleShape or toggleFace) and (name == 'Basis'):
		return True
	elif name[0:4] in ["Bend", "Shou"]:
		return toggleShape
	else:
		return toggleFace

#
#	parseShapeKey(ob, me, args, tokens):
#

def parseShapeKey(ob, me, args, tokens):
	name = args[0]
	lr = args[1]
	if lr == 'Sym':
		addShapeKey(ob, me, name, None, tokens)
	elif lr == 'LR':
		addShapeKey(ob, me, name+'_L', 'Left', tokens)
		addShapeKey(ob, me, name+'_R', 'Right', tokens)
	else:
		raise NameError("ShapeKey L/R %s" % lr)
	return

def addShapeKey(ob, me, name, vgroup, tokens):
	print "parsing shape ", name
	ob.insertShapeKey()
	me.key.relative = True
	block = me.key.blocks[-1]
	block.name = name
	_block[name] = block
	if vgroup:
		block.vgroup = vgroup

	for (key, val, sub) in tokens:
		if key == 'sv':
			index = int(val[0])
			#coord = rot90(float(val[1]), float(val[2]), float(val[3]), True)
			coord = (float(val[1]), float(val[2]), float(val[3]))
			block.data[index] += Vector(coord)
		elif key == 'slider_min':
			block.slidermin = float(val[0])
		elif key == 'slider_max':
			block.slidermax = float(val[0])
	

#
#	parseVertGroup(me, args, tokens):
#

def parseVertGroup(me, args, tokens):
	grp = args[0]
	if (useArmature) or (grp in ['Eye_L', 'Eye_R', 'Gums', 'Head', 'Jaw', 'Left', 'Middle', 'Right', 'Scalp']):
		me.addVertGroup(grp)
		for (key, val, sub) in tokens:
			if key == 'wv':
				me.assignVertsToGroup(grp, [int(val[0])], float(val[1]), Mesh.AssignModes.REPLACE)

#
#	parseArmature (obName, args, tokens)
#

def parseArmature (args, tokens):
	name = args[0]
	scn = bpy.data.scenes.active
	amt = bpy.data.armatures.new(name)
	_armature[name] = amt

	amt.makeEditable()
	for (key, val, sub) in tokens:
		if key == 'bone':
			parseBone(amt.bones, val, sub)
		else:
			defaultKey(key, val, "amt", globals(), locals())

	# Create object here
	print args
	ob = createObject(args[1], amt)
	amt.update()
	
	return amt

#
#	parseJoints(args, tokens):
#

def parseJoints(args, tokens):
	for (key,val,sub) in tokens:
		if key == 'j':
			coord = rot90(val[1], val[2], val[3], True)
			_joint[val[0]] = Vector(coord)

def jointLoc(args):
	global _joint
	if args[0] == 'joint':
		vec = _joint[args[1]]
		if len(args) <= 2:
			return vec
		else:
			if args[2] != '+':
				raise NameError("joint "+args)
			coord = rot90(args[3], args[4], args[5], True)
			offs = Vector(coord)
			if offs.length < Epsilon:
				print args, vec, offs
			return vec+offs			
	else:
		coord = rot90(args[0], args[1], args[2], True)
		return Vector(coord)

#
#	parsePose (args, tokens):
#

def parsePose (args, tokens):
	global todo
	name = args[0]
	ob = _object[name]
	pbones = ob.getPose().bones	
	for (key, val, sub) in tokens:
		if key == 'posebone':
			poseBone(pbones, val, sub)
	ob.getPose().update()
	return ob

#
#	parseBone(amt, args, tokens):
#

boneOptions = dict ({\
	Armature.CONNECTED : 0x001, \
	Armature.HINGE : 0x002, \
	Armature.NO_DEFORM : 0x004, \
	Armature.MULTIPLY : 0x008, \
	Armature.HIDDEN_EDIT : 0x010, \
	Armature.ROOT_SELECTED : 0x020, \
	Armature.BONE_SELECTED : 0x040, \
	Armature.TIP_SELECTED : 0x080, \
	Armature.LOCKED_EDIT : 0x100 \
})

def parseBone(bones, args, tokens):
	global todo
	name = args[0]
	bone = Armature.Editbone()		
	bone.name = name
	bones[bone.name] = bone
	parName = args[1]
	if (parName != "None"):
		parent = bones[parName]
		bone.parent = parent
	flags = int(args[2],16)
	bone.layerMask = int(args[3],16)

	for (key, val, sub) in tokens:
		if key == "head":
			bone.head = jointLoc(val)
		elif key == "tail":
			bone.tail = jointLoc(val)
		elif key == "roll":
			if toggleRot90:
				bone.roll = float(val[1])
			else:
				bone.roll = float(val[0])
		else:
			defaultKey(key, val, "bone", globals(), locals())

	options = []
	for (key, val) in boneOptions.items():
		if (flags & val):
			options.append(key)
	bone.options = options
	return bone

#
#	poseBone(pbones, args, tokens):
#

def poseBone(pbones, args, tokens):
	global todo
	name = args[0]
	flags = int(args[1],16)

	pb = pbones[name]
	pb.limitX = flags & 1
	pb.limitY = (flags >> 1) & 1
	pb.limitZ = (flags >> 2) & 1
	pb.lockXRot = (flags >> 3) & 1
	pb.lockYRot = (flags >> 4) & 1
	pb.lockZRot = (flags >> 5) & 1

	for (key, val, sub) in tokens:
		if key == 'constraint':
			parseConstraint(pb.constraints, val, sub, name)
		elif key == 'smash':
			cns = pb.constraints[-1]
			if doSmash:
				todo.append(("cns.%s" % val[0], globals(), locals()))
		else:
			defaultKey(key, val, "pb", globals(), locals())

#
#	readTypedValue(type, arg, tokens, name, globals, locals):
#

def readTypedValue(type, arg, tokens, name, globals, locals):
	if type == 'list':
		n = int(arg)
		list = []
		for i in range(n):
			elt = readTypedValue(tokens[2*i+2], tokens[2*i+3], [], name, globals, locals)
			list.append(elt)
		return list
	elif type == 'int':
		return int(arg)
	elif type == 'hex':
		return int(arg,16)
	elif type == 'bool':
		if arg == 'true':
			return True
		else:
			return False
	elif type == 'float':
		return float(arg)
	elif type == 'vec':
		return Vector(float(arg[0]), float(arg[1]), float(arg[2]))
	elif type == 'str':
		return arg
	elif type == 'obj':
		return getObject(arg, name, globals, locals)
	elif type == 'ipo':
		return getIpo(arg, name, globals, locals)
	elif type == 'act':
		return getAction(arg, name, globals, locals)
	elif type == 'tex':
		return _texture[arg[0]]
	elif type == 'text':
		try:
			txt = _text3d[arg]
		except:
			txt = None
		return txt
	else:
		msg = "Unknown type "+type+" "+arg
		print msg
		raise NameError(msg)

#
#	parseConstraint(constraints, args, tokens, name)
#

def skipConstraint(type):
	if type == 'PYTHON':
		return True
	elif type == 'CHILDOF':
		return False
	return False

def insertInfluenceIpo(cns, bone):
	global todo
	if bone != 'PArmIK_L' and bone != 'PArmIK_R' and bone != 'PLegIK_L' and bone != 'PLegIK_R':
		#print "Skipped ", bone
		return False

	if toggleFKIK:
		cns.influence = 0.0
		cns.insertKey(0)
		cns.influence = 1.0
		cns.insertKey(1)
		n = -1
		notyetfound = True
		while notyetfound:
			ipo = Ipo.Get()[n]
			try:
				icu = ipo[Ipo.CO_INF]
				notyetfound = False
			except:
				n -= 1
		icu.driver = 1
		icu.driverObject = getObject('Human', 'icu.driverObject', globals(), locals())
		try:
			icu.driverBone = bone
		except:
			blenderWarning()
		icu.driverChannel = IpoCurve.LOC_X
		icu.extend = 0
		icu.interpolation = 1
	elif bone == 'PArmIK_L' or bone == 'PArmIK_R':
		if toggleArmIK:
			cns.influence = 1.0
		else:
			cns.influence = 0.0
	elif bone == 'PLegIK_L' or bone == 'PLegIK_R':
		if toggleLegIK:
			cns.influence = 1.0
		else:
			cns.influence = 0.0

	return True

warnedBlenderVersion = False

def blenderWarning():
	global warnedBlenderVersion
	if not warnedBlenderVersion:
		Draw.PupMenu("MHX only works properly with Blender 2.49b")
		warnedBlenderVersion = True
	return
	

def parseConstraint(constraints, args, tokens, name):
	global todo, nErrors
	typeName = args[0]	
	if skipConstraint(typeName):
		print "Skipping constraint " + typeName
		nErrors += 1
		return None
	try:
		typeCns = Constraint.Type[typeName]
	except:
		raise NameError("Unknown constraint type " + typeName)

	try:
		cns = constraints.append(typeCns)
	except:
		msg = "Unable to add constraint %s (%d) %s" % (typeName, typeCns, args[1])
		print msg
		nErrors += 1
		# raise NameError(msg)
		return
	cns.name = args[1]
	cns.influence = float(args[2])

	for (key,val,sub) in tokens:
		if key == 'driver':
			if insertInfluenceIpo(cns, val[0]):
				pass
			elif val[0] == "FingerIK_L" or val[0] == "FingerIK_R":
				if toggleFingerIK == 0:
					print "Constraint "+name+" ignored."
					cns.influence = 0.0
						
		else:
			idx = Constraint.Settings[key]
			x = readTypedValue(val[0], val[1], val, "cns[idx]", globals(), locals())
			try:
				if type(x) == list:
					for n in range(len(x)):
						cns[idx][n] = x[n]
				else:
					cns[idx] = x
				failed = False
			except:
				failed = True
			if type(x) == float:
				pass
			elif cns[idx] != x or failed:
				cns.influence = 0.0
				print "Ignoring: ", typeName, key, cns[idx], " != ", x
				nErrors += 1

	return cns



#
#	parseModifiers(ob, args, tokens):		
#

def skipModifier(type):
	if type == 'LATTICE':
		return False
	else:
		return False

def parseModifier(ob, args, tokens):
	global todo, nErrors
	typeName = args[0]
	if skipModifier(typeName):
		print "Skipping modifier " + typeName
		nErrors += 1
		return None
	type = Modifier.Types[typeName]
	mod = ob.modifiers.append(type)
	for (key,val,sub) in tokens:
		try:
			idx = Modifier.Settings[key]
			mod[idx] = readTypedValue(val[0], val[1], val, "mod[idx]", globals(), locals())
		except:
			pass
	return mod

#
#	parseParticle(ob, args, tokens):
#

def parseParticle(ob, args, tokens):
	global todo
	par = Particle.New(ob)
	name = args[0]
	par.setName(name)
	_particle[name] = par
	for (key, val, sub) in tokens:
		if key == 'loc':
			pass
			#for (key1, val1, sub1) in sub:
			#	if key1 == 'v':
			#		par.setLoc(float(val1[0]), float(val1[1]), float(val1[2]))
		elif key == 'rot':
			for (key1, val1, sub1) in sub:
				if key1 == 'v':
					par.setRot(float(val1[0]), float(val1[1]), float(val1[2]))
		elif key == 'material':
			mat = Material.Get(val[0])
			par.setMat(mat)
		elif key == 'size':
			par.setSize(int(val[0]))
		elif key == 'vertGroup':
			n = Particle.VERTEXGROUPS[val[0]]
			par.setVertGroup(val[1], n, int(val[2]))
		else:
			defaultKey(key, val, "par", globals(), locals())
			
	return par

#
#	parseCamera(args, tokens):
#

def parseCamera(args, tokens):
	global todo
	type = args[0]
	name = args[1]
	ca = Camera.New(type, name)
	_camera[name] = ca
	for (key, val, sub) in tokens:
		defaultKey(key, val, "ca", globals(), locals())
	
	return ca

#
#	parseLamp(args, tokens):
#

def parseLamp(args, tokens):
	global todo
	type = args[0]
	name = args[1]
	la = Lamp.New(type, name)
	_lamp[name] = la
	for (key, val, sub) in tokens:
		defaultKey(key, val, "la", globals(), locals())
	
	return la

#
#	parseLattice(args, tokens):
#

latKeyType = dict({
	"Cardinal" : Lattice.CARDINAL, \
	"Linear" : Lattice.LINEAR, \
	"Bspline" : Lattice.BSPLINE \
})

def parseLattice(args, tokens):
	global todo
	name = args[0]
	lat = Lattice.New(name)
	_lattice[name] = lat
	for (key, val, sub) in tokens:
		if key == "partitions":
			x = int(val[0])
			y = int(val[1])
			z = int(val[2])
			if x >= 2 and y >= 2 and z >= 2:
				lat.setPartitions(x, y, z)
			else:
				print "Illegal lattice with partitions ", x, y, z
				nErrors += 1
				_lattice[name] = None
				return None
		elif key == "keytypes":
			lat.setKeyTypes(latKeyType[val[0]], latKeyType[val[1]], latKeyType[val[2]])
		else:
			defaultKey(key, val, "lat", globals(), locals())	
	return lat

#
#	parseCurve(args, tokens):
#

def parseCurve(args, tokens):
	global todo
	name = args[0]
	cu = Curve.New(name)
	_curve[name] = cu

	for (key, val, sub) in tokens:
		if key == 'nurb':
			parseNurb(cu, val, sub)
		else:
			defaultKey(key, val, "cu", globals(), locals())
			
	return cu

#
#	parseNurb(cu, args, tokens):
#

def parseNurb(cu, args, tokens):
	nurb = None
	type = args[0]
	for (key, val, sub) in tokens:
		if key == 'pt':
			if type == "bezier":
				pt = BezTriple.New(\
					float(val[0]), float(val[1]), float(val[2]), \
					float(val[3]), float(val[4]), float(val[5]), \
					float(val[6]), float(val[7]), float(val[8]))
			elif type == "poly":
				pt = (float(val[0]), float(val[1]), float(val[2]), float(val[3]), float(val[4]))
	
			if nurb:
				nurb.append(pt)
			else:
				nurb = cu.appendNurb(pt)
	
	return nurb

#
#	parseText(args, tokens):
#

def parseText(args, tokens):
	global todo
	name = args[0]
	te = Text3d.New(name)
	_text3d[name] = te
	for (key, val, sub) in tokens:
		if key == 'line':
			te.setText(val[0])
		else:
			defaultKey(key, val, "te", globals(), locals())

	return te

#
#	parseGroup(args, tokens):
#

def parseGroup(args, tokens):
	global todo
	name = args[0]
	grp = Group.New(name)
	_group[name] = grp
	for (key, val, sub) in tokens:
		if key == 'object':
			name = val[0]
			expr = "add2Group(grp, '"+name+"')"
			todo.append((expr,globals(), locals()))
		else:
			defaultKey(key, val, "grp", globals(), locals())
	return grp
	
def add2Group(grp, name):
	grp.objects.link(_object[name])

#
#	parseEmpty(args, tokens):
#

def parseEmpty(args, tokens):	
	return

#
#	postProcess():
#

'''
def postProcess():
	global toggleArmIK, toggleLegIK, toggleFKIK, toggleFingerIK
	fingerBones = []
	fingerBonesIK = []
	fingerBonesFK = []
	for i in range(1,6):
		for j in range(1,4):
			fingerBones.extend(['Finger-%d-%d_L' % (i,j), 'Finger-%d-%d_R' % (i,j)])
			fingerBonesIK.extend(['Finger-%d-%d_ik_L' % (i,j), 'Finger-%d-%d_ik_R' % (i,j)])
			fingerBonesFK.extend(['Finger-%d-%d_fk_L' % (i,j), 'Finger-%d-%d_fk_R' % (i,j)])

	armBones = ['UpArm_L', 'LoArm_L', 'Hand_L', 'UpArm_R', 'LoArm_R', 'Hand_R']
	if toggleArmIK:
		setInfluence(armBones, 'CopyRotIK', 1.0)
		setInfluence(armBones, 'CopyRotFK', 0.0)
		setInfluence(armBones, 'Const', 1.0)
	else:
		setInfluence(armBones, 'CopyRotIK', 0.0)
		setInfluence(armBones, 'CopyRotFK', 1.0)
		setInfluence(armBones, 'Const', 0.0)

	legBones = ['UpLeg_L', 'LoLeg_L', 'Foot_L', 'Toe_L', 'UpLeg_R', 'LoLeg_R', 'Foot_R', 'Toe_R']
	if toggleLegIK:
		setInfluence(legBones, 'CopyRotIK', 1.0)
		setInfluence(legBones, 'IK', 1.0)
		setInfluence(legBones, 'CopyRotFK', 0.0)
		setInfluence(legBones, 'Const', 1.0)
	else:
		setInfluence(legBones, 'CopyRotIK', 0.0)
		setInfluence(legBones, 'IK', 0.0)
		setInfluence(legBones, 'CopyRotFK', 1.0)
		setInfluence(legBones, 'Const', 0.0)

	if toggleFingerIK:
		setInfluence(fingerBones, 'Const', 1.0)
		setInfluence(fingerBonesIK, 'Action', 1.0)
		setInfluence(fingerBonesFK, 'Action', 1.0)
	else:
		setInfluence(fingerBones, 'Const', 0.0)
		setInfluence(fingerBonesIK, 'Action', 0.0)
		setInfluence(fingerBonesFK, 'Action', 0.0)
	
def setInfluence(bones, cnsName, w):
	ob = _object['Human']
	pbones = ob.getPose().bones	
	for pb in pbones.values():
		if pb.name in bones:
			for cns in pb.constraints:
				if cns.name == cnsName:
					cns.influence = w
	return
'''
#
#	main(fileName):
#


done = 0

def main(filePath):
	global done
	fileName = os.path.expanduser(filePath)
	(shortName, ext) = os.path.splitext(fileName)
	if ext != ".mhx":
		Draw.PupMenu("Error: Not a mhx file: " + fileName)
		return
	readMhxFile(fileName)
	done = 1

#
#	clearScene(scn):
#
	
def clearScene(scn):
	global toggleReplace

	if not toggleReplace:
		return scn

	for ob in scn.objects:
		if ob.type == 'Mesh' or ob.type == 'Armature':
			scn.objects.unlink(ob)
			del ob
	return scn

	oldScn = scn
	scn = Scene.New()
	scn.makeCurrent()
	Scene.Unlink(oldScn)
	del oldScn

	return scn

#
#	User interface
#

def event(evt, val):   
	if done:
		Draw.Exit()               
		return		
	if not val:  # val = 0: it's a key/mbutton release
		if evt in [Draw.LEFTMOUSE, Draw.MIDDLEMOUSE, Draw.RIGHTMOUSE]:
			Draw.Redraw(-1)
		return
	if evt == Draw.ESCKEY:
		Draw.Exit()               
		return
	else: 
		return
	Draw.Redraw(-1)

def button_event(evt): 
	global toggleArmIK, toggleLegIK, toggleFKIK, toggleFingerIK, toggleDispObs
	global toggleReplace, toggleShape, toggleFace, toggleRot90
	global useMesh, useArmature, useProxy
	global TexDir
	if evt == 1:
		toggleShape = 1 - toggleShape
	elif evt == 2:
		toggleFace = 1 - toggleFace
	elif evt == 11:
		toggleArmIK = 1 - toggleArmIK
	elif evt == 12:
		toggleLegIK = 1 - toggleLegIK
	elif evt == 13:
		toggleFKIK = 1 - toggleFKIK
	elif evt == 14:
		useMesh = 1 - useMesh
	elif evt == 15:
		useArmature = 1 - useArmature
	elif evt == 16:
		useProxy = 1 - useProxy
	elif evt == 3:
		toggleFingerIK = 1 - toggleFingerIK
	elif evt == 4:
		toggleDispObs = 1 - toggleDispObs
	elif evt == 5:
		toggleReplace = 1 - toggleReplace
	elif evt == 7:
		Blender.Window.FileSelector (main, 'OPEN MHX FILE')
	elif evt == 8:
		Draw.Exit()
		return
	elif evt == 9:
		#TexDir = Draw.PupStrInput("TexDir? ", TexDir, 100)
		Blender.Window.ImageSelector (setTexDir, 'CHOOSE TEXTURE')
	elif evt == 10:
		#toggleRot90 = 1 - toggleRot90
		pass
	Draw.Redraw(-1)

def setTexDir(filepath):
	global TexDir
	path1 = os.path.expanduser(filepath)
	file1 = os.path.realpath(path1)
	(TexDir,f) = os.path.split(file1)
	return

def gui():
	global b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15
	global t1, t2, t3, t4

	BGL.glClearColor(0,0,1,1)
	BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
	BGL.glColor3f(1,1,1)

	BGL.glRasterPos2i(10,240)
	t1 = Draw.Text("MHX (MakeHuman eXchange format) importer for Blender", "large")
	BGL.glRasterPos2i(10,220)
	t2 = Draw.Text("Version %d.%d" % (MAJOR_VERSION, MINOR_VERSION), "normal")
	BGL.glRasterPos2i(10,200)
	t3 = Draw.Text("Make sure that pydrivers.py is loaded", "large")
	BGL.glRasterPos2i(10,180)
	t4 = Draw.Text("Otherwise shape keys will not work", "normal")

	b13 = Draw.Toggle("Mesh", 14, 10, 140, 90, 20, useMesh,"Use mesh")
	b14 = Draw.Toggle("Armature", 15, 110, 140, 90, 20, useArmature,"Use armature")
	b15 = Draw.Toggle("Proxy", 16, 210, 140, 90, 20, useProxy,"Use proxy")

	b2 = Draw.Toggle("Body shapes", 1, 10, 110, 90, 20, toggleShape,"Load body shape keys")
	b3 = Draw.Toggle("Facial shapes", 2, 110, 110, 90, 20, toggleFace,"Load facial shape keys")
	b10 = Draw.Toggle("Arm IK", 11, 310, 110, 90, 20, toggleArmIK,"Toggle arm IK")
	b11 = Draw.Toggle("Leg IK", 12, 310, 80, 90, 20, toggleLegIK,"Toggle leg IK")
	b12 = Draw.Toggle("FK/IK switch", 13, 310, 50, 90, 20, toggleFKIK,"Toggle FK/IK switch")
	b4 = Draw.Toggle("Finger IK", 3, 210, 110, 90, 20, toggleFingerIK,"Toggle finger IK")
	b1 = Draw.Toggle("Rot90", 10, 10, 80, 90, 20, toggleRot90,"Rotate mesh 90 degrees (Z up)")
	b6 = Draw.Toggle("Replace scene", 5, 110, 80, 90, 20, toggleReplace,"Delete old scene")
	b5 = Draw.Toggle("Display objs", 4, 210, 80, 90, 20, toggleDispObs,"Display objects")
	b7 = Draw.PushButton("Load MHX file", 7, 10, 10, 150, 40)
	b8 = Draw.PushButton("Cancel", 8, 210, 10, 90, 20)
	b9 = Draw.PushButton("Texture directory", 9, 210, 40, 90, 20) 

Draw.Register(gui, event, button_event) 

#main("/home/thomas/mhx3/test.mhx")
#main("/program/makehuman/exports/foo.mhx")
