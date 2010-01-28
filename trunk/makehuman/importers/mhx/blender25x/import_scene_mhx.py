""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyamtht(c):**      MakeHuman Team 2001-2010

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
MHX (MakeHuman eXchange format) importer for Blender 2.5x.

"""

__author__= ['Thomas Larsson']
__url__ = ("www.makehuman.org")
__version__= '0.5'
__bpydoc__= '''\
MHX importer for Blender 2.5
0.5 Fifth version
'''
#
#	Default locations - change to fit your machine
#

TexDir = "~/makehuman/exports"

#
#
#

import bpy
import os
import time
import Mathutils
from Mathutils import *
import Geometry
import string

MAJOR_VERSION = 0
MINOR_VERSION = 5
MHX249 = True
Blender24 = False
Blender25 = True

#
#	Button flags
#

T_ArmIK = 0x01
T_LegIK = 0x02
T_FKIK = 0x04
T_FingerIK = 0x08
T_DispObs = 0x10
T_Replace = 0x20
T_Face = 0x40
T_Shape = 0x80
T_Rot90 = 0x100

toggle = T_Replace + T_ArmIK + T_LegIK

useMesh = 1
doSmash = 1
verbosity = 2
warnedTextureDir = False
warnedVersion = False


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
_image = dict()
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
#	loadMhx(filePath, context, flags):
#

def loadMhx(filePath, context, flags):
	global toggle 
	toggle = flags
	readMhxFile(filePath)
	return

#
#	readMhxFile(filePath):
#

def readMhxFile(filePath):
	global todo, nErrors
	
	fileName = os.path.expanduser(filePath)
	(shortName, ext) = os.path.splitext(fileName)
	if ext != ".mhx":
		print("Error: Not a mhx file: " + fileName)
		return
	print( "Opening MHX file "+ fileName )
	time1 = time.clock()

	ignore = False
	stack = []
	tokens = []
	key = "toplevel"
	level = 0
	nErrors = 0

	file= open(fileName, "rU")
	print( "Tokenizing" )
	lineNo = 0
	for line in file: 
		lineSplit= line.split()
		lineNo += 1
		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == '#':
			pass
		elif lineSplit[0] == 'end':
			try:
				sub = tokens
				tokens = stack.pop()
				if tokens:
					tokens[-1][2] = sub
				level -= 1
			except:
				print( "Tokenizer error at or before line %d" % lineNo )
				print( line )
				dummy = stack.pop()
		elif lineSplit[-1] == ';':
			key = lineSplit[0]
			tokens.append([key,lineSplit[1:-1],[]])
		else:
			key = lineSplit[0]
			tokens.append([key,lineSplit[1:],[]])
			stack.append(tokens)
			level += 1
			tokens = []
	file.close()

	if level != 0:
		raise NameError("Tokenizer out of kilter %d" % level)	
	clearScene()
	print( "Parsing" )
	parse(tokens)
	
	for (expr, globals, locals) in todo:
		try:
			exec(expr, globals, locals)
		except:
			msg = "Failed: "+expr
			# print( msg )
			nErrors += 1
			#raise NameError(msg)

	time2 = time.clock()
	msg = "File %s loaded in %g s" % (fileName, time2-time1)
	if nErrors:
		msg += " but there where %d errors. " % (nErrors)
	print(msg)
	print("Toggle was 0x%x\n" % toggle)
	return	# loadMhx

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
	return

#
#	parseDefault(data, tokens):
#

def parseDefault(data, tokens):
	for (key, val, sub) in tokens:	
		defaultKey(key, val, "data", globals(), locals())

#
#
#

def Bool(string):
	if string == 'True':
		return True
	elif string == 'False':
		return False
	else:
		raise NameError("Bool %s?" % string)
		
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
#	parse(tokens):
#

def parse(tokens):
	global warnedVersion
	
	for (key, val, sub) in tokens:	
		data = None
		if key == 'MHX':
			if int(val[0]) != MAJOR_VERSION and int(val[1]) != MINOR_VERSION and not warnedVersion:
				print("Warning: \nThis file was created with another version of MHX\n")
				warnedVersion = True

		elif key == 'MHX249':
			MHX249 = eval(val[0])
			print("Blender 2.49 compatibility mode is %s\n" % MHX249)

		elif key == 'if':
			try:
				res = eval(val[0])
			except:
				res = False
			if res:
				parse(sub)
		elif key == 'print':
			msg = concatList(val)
			print(msg)
		elif key == 'warn':
			msg = concatList(val)
			print(msg)
		elif key == 'error':
			msg = concatList(val)
			raise NameError(msg)			
		elif key == "object":
			parseObject(val, sub)
		elif key == "joints":
			parseJoints(val, sub)
		elif key == "mesh":
			data = parseMesh(val, sub)
		elif key == "armature":
			data = parseArmature(val, sub)
		elif key == "pose":
			data = parsePose(val, sub)
		elif key == "material":
			data = parseMaterial(val, sub)
		elif key == "texture":
			data = parseTexture(val, sub)
		elif key == "image":
			data = parseImage(val, sub)
		if data:
			print( data )
	return
	
#
#	concatList(elts)
#

def concatList(elts):
	string = ""
	for elt in elts:
		string += " %s" % elt
	return string

#
#	buildLayerMask(mask, n, list):
#

def buildLayerMask(mask, n, list):
	for i in range(n):
		if mask & 1:
			list.append(True)
		else:
			list.append(False)
		mask = mask >> 1
	#print("Layer %x -> %s" % (mask, list))
	return list

#
#	parseObject(args, tokens):
#

ObjectTranslation = {
	'xRay' : 'x_ray'
}

def parseObject(args, tokens):
	if verbosity > 2:
		print( "Parsing object %s" % args )
	name = args[0]
	type = args[1]
	
	try:
		datName = args[2]
	except:
		datName = None

	#print("Objects %s" % _object)
	#print("Meshes %s" % _mesh)
	#print("Amts %s" % _armature)

	if type == "Mesh":
		data = _mesh[datName]
	elif type == "Armature":
		data = _armature[datName]
	else:
		return

	ob = _object[name]

	for (key, val, sub) in tokens:
		if key == "layers":
			layers = buildLayerMask(int(val[0], 16) & 0x3ff, 10, [])
			layers = buildLayerMask(int(val[1], 16) & 0x3ff, 10, layers)
			ob.layers = layers
		elif key == "matrix":
			ob.matrix = parseMatrix(val, sub)
		elif key == "modifier":
			parseModifier(ob, val,sub)
		elif key == "parent":
			parseParent(ob, val,sub)
		elif key == "constraint":
			parseConstraint(ob.constraints, val, sub, name)
		elif MHX249:
			try:
				key1 = ObjectTranslation[key]
				defaultKey(key1, val, "ob", globals(), locals())
			except:
				pass
		else:
			defaultKey(key, val, "ob", globals(), locals())
	return
#
#	createObject(type, name, data):
#

def createObject(type, name, data):
	if verbosity > 2:
		print( "Creating object %s %s %s" % (type, name, data) )
	ob = bpy.data.objects.new(type.upper(), name)
	if data:
		ob.data = data
	ob.name = name
	_object[name] = ob
	scn = bpy.context.scene
	print("Scene %s %s" % (scn, ob))
	print("Objs %s %s " % (scn.objects, scn.objects.values()))
	scn.objects.link(ob)
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
	#parentType = int(args[1])
	parentType = 'BONE'
	extra = args[2]
	expr = None

	if parentType == 'OBJECT': 
		expr = "ob.parent = _object[parent]"
	elif parentType == 'CURVE':
		expr = "ob.parent = _object[parent]"
	elif parentType == 'LATTICE':
		expr = "ob.parent = _object[parent]"
	elif parentType == 'ARMATURE':
		expr = "ob.parent = _object[parent]"
	elif parentType == 'VERTEX': 
		expr = "ob.parent_vertices = extra"
	elif parentType == 'VERTEX_3': 
		verts = extra.split("_")
		if (ob.type != "Empty"):
			expr = "ob.parent_vertices = verts"
	elif parentType == 'BONE': 
		if extra != "None":
			expr = "ob.parent_bone = parent"

	if expr:
		try:
			exec(expr)
		except:
			todo.append((expr, globals(), locals()))
	return

#
#	parseMaterial(args, ext, tokens):
#

def parseMaterial(args, tokens):
	global todo
	name = args[0]
	mat = bpy.data.materials.new(name)
	if mat == None:
		return None
	_material[name] = mat
	print("Mat1 %s" % mat)
	for (key, val, sub) in tokens:
		if key == 'mtex':
			parseMTex(mat, val, sub)
		#elif key == 'active_texture':
		#	mat.active_texture = _texture[val[0]]
		elif key == 'diffuse_ramp':
			mat.diffuse_ramp = parseRamp(sub)
		elif key == 'halo': 
			parseDefault(mat.halo, sub)
		elif key == 'specular_ramp':
			mat.specular_ramp = parseRamp(sub)
		elif key == 'raytrace_mirror':
			parseDefault(mat.raytrace_mirror, sub)
		elif key == 'raytrace_transparency':
			parseDefault(mat.raytrace_transparency, sub)
		elif key == 'subsurface_scattering':
			parseDefault(mat.subsurface_scattering, sub)
		elif key == 'volume':
			parseDefault(mat.volume, sub)
		else:			
			defaultKey(key, val, 'mat', globals(), locals())
	return mat

#
#	parseRamp(ramp, tokens):
#

def parseRamp(ramp, tokens):
	global todo
	for (key,val,sub) in tokens:
		if key == 'elements':
			pass
		else:
			defaultKey(key, val, "ramp", globals(), locals())

#
#	parseMTex(mtex, args, tokens):
#

def parseMTex(mat, args, tokens):
	global todo
	if verbosity > 2:
		print( "Parsing MTex %s" % args )

	index = int(args[0])
	texname = args[1]
	#use = Bool(args[2])
		
	mat.add_texture()
	mtex = mat.textures[index]
	mtex.texture = _texture[texname]
	#mat.use_textures[index] = use

	for (key, val, sub) in tokens:
		defaultKey(key, val, "mtex", globals(), locals())

	return mtex

			
			
#
#	parseTexture(args, tokens):
#

def parseTexture(args, tokens):
	global todo
	if verbosity > 2:
		print( "Parsing texture %s" % args )
	typename = args[0].upper()
	name = args[1]
	tex = bpy.data.textures.new(name)
	tex.type = typename
	tex = tex.recast_type()
	_texture[name] = tex
	
	for (key, val, sub) in tokens:
		if key == 'image':
			img = parseImage(val, sub)
			tex.image = img
		else:
			pass
			#defaultKey(key, val, "tex", globals(), locals())

	return tex
	
#
#	doLoadImage(filepath):
#	loadImage(filepath):
#	parseImage(args, tokens):
#

def doLoadImage(filepath):		
	path1 = os.path.expanduser(filepath)
	file1 = os.path.realpath(path1)
	if os.path.isfile(file1):
		print( "Found file "+file1 )
		try:
			img = bpy.data.add_image(file1)
			#bpy.ops.images.open(file1)
			#img = bpy.data.images[-1]
			return img
		except:
			print( "Cannot read image" )
			return None
	else:
		print( "No file "+file1 )
		return None


def loadImage(filepath):
	global TexDir, warnedTextureDir
	texDir = os.path.expanduser(TexDir)
	path1 = os.path.expanduser(filepath)
	file1 = os.path.realpath(path1)
	(path, filename) = os.path.split(file1)
	(name, ext) = os.path.splitext(filename)
	print( "Loading ", filepath, " = ", filename )

	img = doLoadImage(texDir+"/"+name+".png")
	if img:
		return img

	img = doLoadImage(texDir+"/"+filename)
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
	return None
	TexDir = Draw.PupStrInput("TexDir? ", path, 100)

	texDir = os.path.expanduser(TexDir)
	img =  doLoadImage(texDir+"/"+name+".png")
	if img:
		return img

	img = doLoadImage(TexDir+"/"+filename)
	return img
	
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
	print ("Image %s" % img )
	return img

#
#	rot90(x, y, z, doRot)
#

def rot90(x, y, z, doRot):
	global toggle
	if (toggle & T_Rot90) and doRot:
		return (float(x), -float(z), float(y))
	else:
		return (float(x), float(y), float(z))

#
#	unpackList(list_of_tuples):
#

def unpackList(list_of_tuples):
	l = []
	for t in list_of_tuples:
		l.extend(t)
	return l

#
#	parseMesh (args, tokens):
#

def parseMesh (args, tokens):
	global todo
	if verbosity > 2:
		print( "Parsing mesh %s" % args )

	mename = args[0]
	obname = args[1]

	# Create object here
	bpy.ops.object.add(type='MESH')
	ob = bpy.context.scene.objects.active
	ob.name = obname
	_object[obname] = ob
	me = ob.data
	me.name = mename
	_mesh[mename] = me

	if mename == 'Human':
		mainMesh = True
	else:
		mainMesh = False

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
			if len(faceLocVerts) < 4:
				faceLocVerts.append(0)
			if len(faceTexVerts) < 4:
				faceTexVerts.append(0)
			if len(v) == 1:
				faces.append( faceLocVerts )
			else:
				faces.append( faceLocVerts )
				texFaces.append( faceTexVerts )

		elif key == 'vt':
			vertsTex.append( (float(val[0]), float(val[1])) ) 

	if faces:
		me.add_geometry(len(verts), 0, len(faces))
		me.verts.foreach_set("co", unpackList(verts))
		me.faces.foreach_set("verts_raw", unpackList(faces))
	else:
		me.add_geometry(len(verts), len(edges), 0)
		me.verts.foreach_set("co", unpackList(verts))
		me.edges.foreach_set("verts", unpackList(edges))

	# UVs
	
	if texFaces != [] and me.faces:
		#me.faceUV= 1
		me.add_uv_texture()
		tfaces = me.uv_textures[-1].data
		for n,ft in enumerate(texFaces):
			tfaces[n].uv1= vertsTex[ft[0]]
			tfaces[n].uv2= vertsTex[ft[1]]
			tfaces[n].uv3= vertsTex[ft[2]]
			if len(ft)==4:
				tfaces[n].uv4= vertsTex[ft[3]]
	me.update()
		
	mats = []
	for (key, val, sub) in tokens:
		if key == 'v' or \
			 key == 'e' or \
			 key == 'f' or \
			 key == 'vt':
				pass

		elif key == 'fx':
			f = me.faces[int(val[0])]
			f.material_index = int(val[1])
			f.smooth = int(val[2])

		elif key == 'fxall':
			mat = int(val[0])
			smooth = int(val[1])
			for f in me.faces:
				f.material_index = mat
				f.smooth = smooth

		elif key == 'vertgroup':
			parseVertGroup(ob, me, val, sub)
		elif key == 'shapekey':
			if doShape(val[0]):
				parseShapeKey(ob, me, val, sub)
		elif key == 'ipo':
			if (toggle & T_Shape) or (toggle & T_Face):
				parseShapeIpo(val, sub, ob)
		elif key == 'material':
			try:
				mat = _material[val[0]]
				me.add_material(mat)
			except:
				pass
		else:
			defaultKey(key, val, "me", globals(), locals())

	return me

#
#	parseVertGroup(ob, me, args, tokens):
#

def parseVertGroup(ob, me, args, tokens):
	if verbosity > 2:
		print( "Parsing vertgroup %s" % args )
	grp = args[0]
	group = ob.add_vertex_group(grp)
	group.name = grp
	for (key, val, sub) in tokens:
		if key == 'wv':
			ob.add_vertex_to_group( int(val[0]), group, float(val[1]), 'REPLACE')


#
#	parseShapeKey(ob, me, args, tokens):
#

def doShape(name):
	if ((toggle & T_Shape) or (toggle & T_Face)) and (name == 'Basis'):
		return True
	elif name[0:4] in ["Bend", "Shou"]:
		return (toggle & T_Shape)
	else:
		return (toggle & T_Face)

def parseShapeKey(ob, me, args, tokens):
	name = args[0]
	if verbosity > 0:
		print( "Parsing shape %s" % name )
	#block = ob.add_shape_key(name, False)
	bpy.ops.object.shape_key_add(False)
	block = ob.active_shape_key
	if name != 'Basis':
		block.relative_key = _block['Basis']
	block.name = name
	_block[name] = block
	block.slider_min = float(args[1])
	block.slider_max = float(args[2])
	if args[3] != "None":
		block.vertex_group = args[3]

	for (key, val, sub) in tokens:
		if key == 'sv':
			index = int(val[0])
			pt = block.data[index].co
			(x,y,z) = rot90(float(val[1]), float(val[2]), float(val[3]), True)
			pt[0] += x
			pt[1] += y
			pt[2] += z
	return	

#  icu BrowsOutUp_L 0 2 
#      driver 2 ;
#      driverObject _object['Human'] ;
#      driverChannel 1 ;
#      driverExpression 'p.ctrlBrowsOutUp_L()' ;
#    end icu
#
#  icu BendElbowForward_L 0 1 
#      bz2 -3.508294 0.000000 0.000000 0.000000 3.508294 0.000000  ;
#      bz2 5.491706 1.000000 9.000000 1.000000 12.508294 1.000000  ;
#      driver 1 ;
#      driverObject _object['HumanRig'] ;
#      driverBone 'LoArmTwist_L' ;
#      driverChannel 7 ;
#      extend 0 ;
#      interpolation 1 ;
#    end icu

#
#	parseShapeIpo(args, tokens, ob)
#	parseShapeIcu(args, tokens, ob)
#

DriverChannels = [0, 'LOC_X', 'LOC_Y', 'LOC_Z', 'SCALE_X', 'SCALE_Y', 'SCALE_Z', 'ROT_X', 'ROT_Y', 'ROT_Z']

def parseShapeIpo(args, tokens, ob):
	for (key, val, sub) in tokens:
		if key == 'icu':
			parseShapeIcu(val, sub, ob)
	return

def parseShapeIcu(args, tokens, ob):
	name = args[0]
	if not doShape(name):
		return
	fcurve = ob.data.shape_keys.keys[name].driver_add("value", 0)
	print("%s %s" % (name, fcurve))

	var = fcurve.driver.variables.new()
	var.name = name
	var.targets[0].id_type = 'OBJECT'
	var.targets[0].data_path ='keys["' + name + '"].value'

	mod = fcurve.modifiers[0]
	mod.poly_order = 2
	mod.coefficients[0] = 0.0
	mod.coefficients[1] = 1.0
	for (key, val, sub) in tokens:
		arg = eval(val[0])
		if key == 'driver':
			if arg == 1:
				fcurve.driver.type = 'AVERAGE'
			elif arg == 2:
				fcurve.driver.type = 'SCRIPTED'
			else:
				raise NameError("Unknown driver %s" % val)
		elif key == 'driverObject':
			
			var.targets[0].id = arg
		elif key == 'driverChannel':
			var.targets[0].transform_type = DriverChannels[arg]
		elif key == 'driverExpression':
			fcurve.driver.expression = arg[2:]	# skip p.
		#elif key == 'driverBone':
		#	var.targets[0].name = arg
	return
	
#
#	parseArmature (obName, args, tokens)
#

rigify = False

def parseArmature (args, tokens):
	global rigify
	if verbosity > 2:
		print( "Parsing armature %s" % args )
	
	(key,val,sub) = tokens[0]
	if key == 'rigify':
		bpy.ops.object.armature_human_advanced_add()
		rigify = True
	else:
		bpy.ops.object.armature_add()
		rigify = False

	name = args[1]
	ob = bpy.context.scene.objects.active
	ob.name = name
	_object[name] = ob

	amt = ob.data
	name = args[0]
	amt.name = name
	_armature[name] = amt
	bones = dict()

	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.mode_set(mode='EDIT')

	if not rigify:
		layer1 = [False for n in range(16)]
		layer2 = buildLayerMask(0x0101, 16, [])
		amt.layer = layer2+layer1
		print(amt.layer)
	#	amt.bones[0].name = '__Unused__'

	for (key, val, sub) in tokens:
		if key == 'bone':
			parseBone(amt, bones, val, sub)
		elif key == 'rigify':
			pass
		else:
			defaultKey(key, val, "amt", globals(), locals())

	bpy.ops.object.mode_set(mode='OBJECT')
	
	return amt

#
#	parseBone(amt, bones, args, tokens):
#

OPT_CONNECTED = 0x001
OPT_NODEFORM = 0x004

def parseBone(amt, bones, args, tokens):
	global todo, rigify

	name = args[0]
	if rigify:
		print("Find bone %s" % name)
		bone = amt.edit_bones[name]
		print("Found %s" %bone)
	else:
		bpy.ops.armature.bone_primitive_add(name="Bone")
		bone = amt.edit_bones[-1]
		bone.name = name
		bones[bone.name] = bone
		parName = args[1]
		if (parName != "None"):
			parent = bones[parName]
			bone.parent = parent
		flags = int(args[2],16)
		bone.connected = flags & OPT_CONNECTED
		bone.deform = not (flags & OPT_NODEFORM)
		bone.draw_wire = True
		layer1 = [False for n in range(16)]
		layer2 = buildLayerMask(int(args[3], 16) & 0xffff, 16, [])
		bone.layer = layer2+layer1

	for (key, val, sub) in tokens:
		if key == "head":
			bone.head = jointLoc(val)
		elif key == "tail":
			bone.tail = jointLoc(val)
		elif key == "roll":
			if (toggle & T_Rot90):
				bone.roll = float(val[1])
			else:
				bone.roll = float(val[0])
		else:
			defaultKey(key, val, "bone", globals(), locals())

	return bone

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
				print( "%s %s %s" % (args, vec, offs) )
			return vec+offs			
	else:
		coord = rot90(args[0], args[1], args[2], True)
		return Vector(coord)

#
#	parsePose (args, tokens):
#

def parsePose (args, tokens):
	global todo, rigify
	if rigify:
		return
	name = args[0]
	ob = _object[name]
	bpy.ops.object.mode_set(mode='POSE')
	pbones = ob.pose.bones	
	for (key, val, sub) in tokens:
		if key == 'posebone':
			poseBone(pbones, val, sub)
	#ob.pose.update()
	bpy.ops.object.mode_set(mode='OBJECT')
	return ob


#
#	poseBone(pbones, args, tokens):
#

def poseBone(pbones, args, tokens):
	global todo
	if verbosity > 2:
		print( "Parsing posebone %s" % args )
	name = args[0]
	pb = pbones[name]

	flags = int(args[1],16)
	pb.ik_limit_x = flags & 1
	pb.ik_limit_y = (flags >> 1) & 1
	pb.ik_limit_z = (flags >> 2) & 1
	pb.ik_dof_x = not ((flags >> 3) & 1)
	pb.ik_dof_y = not ((flags >> 4) & 1)
	pb.ik_dof_z = not ((flags >> 5) & 1)

	for (key, val, sub) in tokens:
		if key == 'constraint':
			parseConstraint(pb.constraints, val, sub, name)
		elif key == 'type':
			pb.set("type", val[0])
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
		if arg == 'True':
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
		print( msg )
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
		return False

	if (toggle & T_FKIK):
		fcurve = cns.driver_add("influence", 0)
		fcurve.driver.type = 'AVERAGE'

		var = fcurve.driver.variables.new()
		var.name = bone
		var.targets[0].id_type = 'OBJECT'
		var.targets[0].id = getObject('HumanRig', 'var.targets[0].id', globals(), locals())
		var.targets[0].bone_target = bone
		var.targets[0].transform_type = 'LOC_X'
		# controller_path = fk_chain.arm_p.path_to_id()
		#var.targets[0].data_path = controller_path + '["hinge"]'

		mod = fcurve.modifiers[0]
		mod.poly_order = 2
		mod.coefficients[0] = 0.0
		mod.coefficients[1] = 1.0
	elif bone == 'PArmIK_L' or bone == 'PArmIK_R':
		if (toggle & T_ArmIK):
			cns.influence = 1.0
		else:
			cns.influence = 0.0
	elif bone == 'PLegIK_L' or bone == 'PLegIK_R':
		if (toggle & T_LegIK):
			cns.influence = 1.0
		else:
			cns.influence = 0.0

	return True

#
#	parseConstraint(constraints, args, tokens, name):
#


def parseConstraint(constraints, args, tokens, name):
	global todo, nErrors
	if verbosity > 2:
		print( "Parsing constraint %s" % args )
	typeName = args[0]	

	try:
		cns = constraints.new(typeName)
	except:
		msg = "Unable to add constraint %s (%s) %s" % (typeName, typeName, args[1])
		print( msg )
		nErrors += 1
		#raise NameError(msg)
		return
	cns.name = args[1]
	cns.influence = float(args[2])

	for (key,val,sub) in tokens:
		if key == 'driver':
			if insertInfluenceIpo(cns, val[0]):
				pass
			elif val[0] == "FingerIK_L" or val[0] == "FingerIK_R":
				if (toggle & T_FingerIK) == 0:
					if verbosity > 2:
						print("Constraint "+name+" ignored.")
					cns.influence = 0.0
		elif key == '-':
			pass

		elif key == 'LIMIT':
			n = int(val[1],16)
			if typeName == 'LIMIT_LOCATION':
				cns.use_minimum_x = n & 1
				n = n >> 1
				cns.use_minimum_y = n & 1
				n = n >> 1
				cns.use_minimum_z = n & 1
				n = n >> 1
				cns.use_maximum_x = n & 1
				n = n >> 1
				cns.use_maximum_y = n & 1
				n = n >> 1
				cns.use_maximum_z = n & 1
			elif typeName == 'LIMIT_ROTATION':
				cns.use_limit_x = n & 1
				n = n >> 1
				cns.use_limit_y = n & 1
				n = n >> 1
				cns.use_limit_z = n & 1
			else:
				raise NameError("LIMIT %s" % typeName)

		elif key == 'COPY':
			n = int(val[1],16)
			cns.use_x = n & 1
			n = n >> 1
			cns.use_y = n & 1
			n = n >> 1
			cns.use_z = n & 1
			n = n >> 1
			cns.invert_x = n & 1
			n = n >> 1
			cns.invert_y = n & 1
			n = n >> 1
			cns.invert_z = n & 1

		else:
			x = readTypedValue(val[0], val[1], val, "cns.%s" % (key), globals(), locals())
			try:
				exec("cns.%s = x" % (key))
			except:
				pass



#
#
#

ModifierTypeName = dict({\

})

#
#	parseModifiers(ob, args, tokens):		
#

ModifierSettingsName = dict({\
	'RENDER' : 'render',
	'OBJECT' : 'object',
	'REALTIME' : 'realtime',
	'VGROUPS' : 'use_vertex_groups',
	'ENVELOPES' : 'use_bone_envelopes',
	'EDITMODE' : 'editmode',
	'ONCAGE' : 'on_cage',

})

def skipModifier(type):
	if type == 'LATTICE':
		return False
	else:
		return False

def parseModifier(ob, args, tokens):
	global todo, nErrors
	if verbosity > 2:
		print( "Parsing modifier %s" % args )
	typeName = args[0]
	if skipModifier(typeName):
		print( "Skipping modifier " + typeName )
		nErrors += 1
		return None
	mod = ob.modifiers.new("mod", typeName)
	for (key,val,sub) in tokens:
		try:
			if MHX249:
				ext = ModifierSettingsName[key]
			else:
				ext = key
			x = readTypedValue(val[0], val[1], val, "mod.%s" % ext, globals(), locals())
			expr = "mod.%s = x" % (ext)
			exec(expr)
		except:
			print("modifer setting %s = %s failed" % (key, val))

	return mod

#
#	parseParticle(ob, args, tokens):
#

def parseParticle(ob, args, tokens):
	global todo
	if verbosity > 2:
		print( "Parsing particle %s" % args )
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
#	clearScene():
#
	
def clearScene():
	global toggle
	scn = bpy.context.scene
	print("clearScene %s %s" % ((toggle & T_Replace), scn))
	if not (toggle & T_Replace):
		return scn
	for ob in scn.objects:
		if ob.type == 'MESH' or ob.type == 'ARMATURE':
			scn.objects.unlink(ob)
			del ob
	scn.render_data.render_raytracing = False
	return scn

#
#	User interface
#

DEBUG= False
from bpy.props import *

class IMPORT_OT_makehuman_mhx(bpy.types.Operator):
	'''Import from MHX file format (.mhx)'''
	bl_idname = "import_scene.makehuman_mhx"
	bl_label = 'Import MHX'

	path = StringProperty(name="File Path", description="File path used for importing the MHX file", maxlen= 1024, default= "")

	armik = BoolProperty(name="Arm IK", description="Use arm IK", default= False)
	legik = BoolProperty(name="Leg IK", description="Use leg IK", default= False)
	fkik = BoolProperty(name="FK/IK switch", description="Use FK/IK switching", default= False)
	fingerik = BoolProperty(name="Finger IK", description="Use finger IK", default= False)
	dispobs = BoolProperty(name="DispObs", description="Display objects", default= True)
	replace = BoolProperty(name="Replace scene", description="Replace scene", default= True)
	face = BoolProperty(name="Face shapes", description="Include facial shapekeys", default= True)
	shape = BoolProperty(name="Body shapes", description="Include body shapekeys", default= False)
	rot90 = BoolProperty(name="Rot 90", description="Rotate X 90.", default= False)

	def execute(self, context):
		loadMhx(self.properties.path, 
			context, 
			self.properties.armik +
			(self.properties.legik << 1) +
			(self.properties.fkik << 2) +
			(self.properties.fingerik << 3) +
			(self.properties.dispobs << 4) +
			(self.properties.replace << 5) +
			(self.properties.face << 6) +
			(self.properties.shape << 7) +
			(self.properties.rot90 << 8)
			)
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.manager
		wm.add_fileselect(self)
		return {'RUNNING_MODAL'}

bpy.types.register(IMPORT_OT_makehuman_mhx)

menu_func = lambda self, context: self.layout.operator(IMPORT_OT_makehuman_mhx.bl_idname, text="MakeHuman (.mhx)...")
bpy.types.INFO_MT_file_import.append(menu_func)
"""

#
#	Testing
#
#readMhxFile("C:/Documents and Settings/xxxxxxxxxxxxxxxxxxxx/Mina dokument/makehuman/exports/foo.mhx")
#readMhxFile("/home/svn/data/3dobjs/materials25.mhx")
readMhxFile("/home/thomas/makehuman/exports/foo.mhx")
#readMhxFile("/home/thomas/svn/makehuman/data/3dobjs/materials25.mhx")
#bump
"""




