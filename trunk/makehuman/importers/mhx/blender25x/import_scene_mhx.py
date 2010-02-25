""" 
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyright(c):**	  MakeHuman Team 2001-2010

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
MHX (MakeHuman eXchange format) importer for Blender 2.5x.
Version 0.5

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
MHX249 = False
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

T_Rigify = 0x1000

toggle = T_Replace + T_ArmIK + T_LegIK 

theScale = 1.0
useMesh = 1
doSmash = 1
verbosity = 2
warnedTextureDir = False
warnedVersion = False


true = True
false = False
Epsilon = 1e-6
nErrors = 0
theTempDatum = None

todo = []

#
#	Dictionaries
#

loadedData = {
	'NONE' : {},

	'Object' : {},
	'Mesh' : {},
	'Armature' : {},
	'Lamp' : {},
	'Camera' : {},
	'Lattice' : {},
	'Curve' : {},

	'Material' : {},
	'Image' : {},
	'MaterialTextureSlot' : {},
	'Texture' : {},
	
	'Bone' : {},
	'BoneGroup' : {},
	'Rigify' : {},

	'Action' : {},
	'Group' : {},

	'MeshTextureFaceLayer' : {},
	'MeshColorLayer' : {},
	'VertexGroup' : {},
	'ShapeKey' : {},
	'ParticleSystem' : {},

	'ObjectConstraints' : {},
	'ObjectModifiers' : {},
	'MaterialSlot' : {},
}

Plural = {
	'Object' : 'objects',
	'Mesh' : 'meshes',
	'Lattice' : 'lattices',
	'Curve' : 'curves',
	'Group' : 'groups',
	'Empty' : 'empties',
	'Armature' : 'armatures',
	'Bone' : 'bones',
	'BoneGroup' : 'bone_groups',
	'Pose' : 'poses',
	'PoseBone' : 'pose_bones',
	'Material' : 'materials',
	'Texture' : 'textures',
	'Image' : 'images',
	'Camera' : 'cameras',
	'Lamp' : 'lamps',
	'World' : 'worlds',
}

#
#	Creators
#

def uvtexCreator(me, name):
	print("uvtexCreator", me, name)
	me.add_uv_texture()
	uvtex = me.uv_textures[-1]
	uvtex.name = name
	return uvtex


def vertcolCreator(me, name):
	print("vertcolCreator", me, name)
	me.add_vertex_color()
	vcol = me.vertex_colors[-1]
	vcol.name = name
	return vcol
		

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
		# print(line)
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
			if lineSplit[0] == '\\':
				key = lineSplit[1]
				tokens.append([key,lineSplit[2:-1],[]])
			else:
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
	
	for (expr, glbals, lcals) in todo:
		try:
			#print("Doing %s" % expr)
			exec(expr, glbals, lcals)
		except:
			msg = "Failed: "+expr
			print( msg )
			nErrors += 1
			#raise NameError(msg)

	postProcess()
	time2 = time.clock()
	msg = "File %s loaded in %g s" % (fileName, time2-time1)
	if nErrors:
		msg += " but there where %d errors. " % (nErrors)
	print(msg)
	return	# loadMhx

#
#	getObject(name, var, glbals, lcals):
#

def getObject(name, var, glbals, lcals):
	try:
		ob = loadedData['Object'][name]
	except:
		if name != "None":
			expr = "%s = loadedData['Object'][name]" % var
			print("Todo ", expr)
			todo.append((expr, glbals, lcals))
		ob = None
	return ob

#
#	parse(tokens):
#

def parse(tokens):
	global warnedVersion, MHX249
	
	for (key, val, sub) in tokens:	
		print("Parse %s" % key)
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

		elif MHX249:
			pass

		elif key == 'print':
			msg = concatList(val)
			print(msg)
		elif key == 'warn':
			msg = concatList(val)
			print(msg)
		elif key == 'error':
			msg = concatList(val)
			raise NameError(msg)			
		elif key == "Object":
			parseObject(val, sub)
		elif key == "Mesh":
			data = parseMesh(val, sub)
		elif key == "Curve":
			data = parseCurve(val, sub)
		elif key == "Lattice":
			data = parseLattice(val, sub)
		elif key == "Group":
			data = parseGroup(val, sub)
		elif key == "Armature":
			data = parseArmature(val, sub)
		elif key == "Pose":
			data = parsePose(val, sub)
		elif key == "Action":
			data = parseAction(val, sub)
		elif key == "Material":
			data = parseMaterial(val, sub)
		elif key == "Texture":
			data = parseTexture(val, sub)
		elif key == "Image":
			data = parseImage(val, sub)
		else:
			data = parseDefaultType(key, val, sub)				

		if data:
			print( data )
	return

#
#	parseDefaultType(typ, args, tokens):
#

def parseDefaultType(typ, args, tokens):
	global todo

	name = args[0]
	data = None
	expr = "bpy.data.%s.new('%s')" % (Plural[typ], name)
	print(expr)
	data = eval(expr)
	print("  ok", data)

	bpyType = typ.capitalize()
	print(bpyType, name, data)
	loadedData[bpyType][name] = data
	if data == None:
		return None

	for (key, val, sub) in tokens:
		#print("%s %s" % (key, val))
		defaultKey(key, val, sub, 'data', [], globals(), locals())
	print("Done ", data)
	return data
	
#
#	concatList(elts)
#

def concatList(elts):
	string = ""
	for elt in elts:
		string += " %s" % elt
	return string

#
#	parseAnimationData(anim, args, tokens):
#	parseAction(args, tokens):
#	parseFCurve(fcu, args, tokens):
#	parseKeyFramePoint(pt, args, tokens):
#
#	parseDriver(drv, args, tokens):
#	parseDriverVariable(var, args, tokens):
#

def parseAnimationData(anim, args, tokens):
	for (key, val, sub) in tokens:
		if key == 'FCurve':
			fcu = parseFCurve(anim.fcurves, val, sub)
		else:
			defaultKey(key, val, sub, 'anim', [], globals(), locals())
	return act

def parseAction(args, tokens):
	name = args[0].replace(' ', '_')
	act = bpy.data.actions.new(name)
	loadedData['Action'][name] = act
	#act.animation_data_create()
	#bpy.context.scene.actions.active = act
	bpy.ops.action.keyframe_insert(type='ALL')
	for (key, val, sub) in tokens:
		if key == 'FCurve':
			fcu = parseFCurve(act.fcurves, val, sub)
		else:
			defaultKey(key, val, sub, 'act', [], globals(), locals())
	return act

'''
bpy.ops.anim.keyframe_insert_menu(type=-2, confirm_success=False, always_prompt=False)
bpy.ops.action.select_border(gesture_mode=3, xmin=33, xmax=73, ymin=319, ymax=370, axis_range=False)
bpy.ops.action.duplicate(mode=17)
bpy.ops.transform.transform(mode='TIME_TRANSLATE', value=(20, 0, 0, 0), axis=(0, 0, 0), proportional='DISABLED', proportional_editing_falloff='SMOOTH', proportional_size=1, mirror=False, constraint_axis=(False, False, False), constraint_orientation='GLOBAL')
'''

def parseFCurve(fcurves, args, tokens):
	print(fcurves)
	return
	fcu.data_path = args[0]
	fcu.array_index = int(args[1])

	for (key, val, sub) in tokens:
		if key == 'kp':
			bpy.ops.anim.keyframe_insert_menu(type=-2, confirm_success=False, always_prompt=False)
			pt = fcu.keyframe_points.new()
			pt = parseKeyFramePoint(pt, val, sub)
		else:
			defaultKey(key, val, sub, 'fcu', [], globals(), locals())
	return fcu

def parseDriver(drv, args, tokens):
	for (key, val, sub) in tokens:
		if key == 'DriverVariable':
			var = drv.variables.new()
			var = parseDriverVariable(var, val, sub)
		else:
			defaultKey(key, val, sub, 'drv', [], globals(), locals())
	return drv

def parseDriverVariable(var, args, tokens):
	for (key, val, sub) in tokens:
		if key == 'Targets':
			pass
		else:
			defaultKey(key, val, sub, 'var', [], globals(), locals())
	return var


def parseKeyFramePoint(pt, args, tokens):
	pt.co = eval(args[0])
	pt.handle1 = eval(args[1])
	pt.handle2 = eval(args[2])
	return pt
	
#
#	parseMaterial(args, ext, tokens):
#	parseMTex(mat, args, tokens):
#	parseTexture(args, tokens):
#

def parseMaterial(args, tokens):
	global todo
	name = args[0]
	#print("Parse material "+name)
	mat = bpy.data.materials.new(name)
	if mat == None:
		return None
	loadedData['Material'][name] = mat
	#print("Material %s %s %s" % (mat, name, loadedData['Material'][name]))
	for (key, val, sub) in tokens:
		if key == 'MTex':
			#print("MTEX", val)
			parseMTex(mat, val, sub)
			#print("MTEX done")
		elif key == 'Ramp':
			parseRamp(mat, val, sub)
		else:
			defaultKey(key, val, sub, 'mat', ['specular_intensity', 'tangent_shading'], globals(), locals())
	#print("Done ", mat)
	
	return mat

def parseMTex(mat, args, tokens):
	global todo
	index = int(args[0])
	texname = args[1]
	texco = args[2]
	mapto = args[3]

	mat.add_texture(texture = loadedData['Texture'][texname], texture_coordinates = texco, map_to = mapto)
	mtex = mat.texture_slots[index]
	#mat.use_textures[index] = Bool(use)

	for (key, val, sub) in tokens:
		defaultKey(key, val, sub, "mtex", [], globals(), locals())

	return mtex

def parseTexture(args, tokens):
	global todo
	if verbosity > 2:
		print( "Parsing texture %s" % args )
	name = args[0]
	tex = bpy.data.textures.new(name)
	typ = args[1]
	tex.type = typ
	print("RECASTING", tex, typ)
	tex = tex.recast_type()
	print("RECAST OK", tex, typ)
	loadedData['Texture'][name] = tex
	
	for (key, val, sub) in tokens:
		print("TEX", key, val)
		if key == 'Image':
			try:
				imgName = val[0]
				img = loadedData['Image'][imgName]
				tex.image = img
			except:
				msg = "Unable to load image '%s'" % val[0]
		elif key == 'Ramp':
			parseRamp(tex, val, sub)
		else:
			defaultKey(key, val,  sub, "tex", ['use_nodes', 'use_textures', 'contrast'], globals(), locals())

	return tex

def parseRamp(data, args, tokens):
	return
	nvar = "data.%s" % args[0]
	print(data, dir(data))
	print(nvar, eval(nvar))
	for (key, val, sub) in tokens:
		print("Ramp", key, val)
		if key == 'Element':
			expr = "%s.color = %s" % (nvar, val[0])
			print(expr)
			exec(expr)
			expr = "%s.position = %s" % (nvar, val[1])
			print(expr)
			exec(expr)
		else:
			defaultKey(key, val,  sub, "tex", ['use_nodes', 'use_textures', 'contrast'], globals(), locals())
	

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
	global TexDir, warnedTextureDir, loadedData

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
	imgName = args[0]
	img = None
	for (key, val, sub) in tokens:
		if key == 'Filename':
			filename = val[0]
			for n in range(1,len(val)):
				filename += " " + val[n]
			img = loadImage(filename)
			if img == None:
				return None
			img.name = imgName
		else:
			defaultKey(key, val,  sub, "img", ['depth', 'dirty', 'has_data', 'size', 'type'], globals(), locals())
	print ("Image %s" % img )
	loadedData['Image'][imgName] = img
	return img

#
#	parseObject(args, tokens):
#	createObject(type, name, data):
#	createObjectAndData(args, typ):
#
	
def parseObject(args, tokens):
	if verbosity > 2:
		print( "Parsing object %s" % args )
	name = args[0]
	type = args[1]
	datName = args[2]
	try:
		data = loadedData[type.capitalize()][datName]	
	except:
		data = None

	if data == None and type != 'EMPTY':
		print("Failed to find data: %s %s %s" % (name, type, datName))
		return

	try:
		ob = loadedData['Object'][name]
		bpy.context.scene.objects.active = ob
		print("Found data")
	except:
		ob = createObject(type, name, data)
	if bpy.context.object != ob:
		print("Context", ob, bpy.context.object, bpy.context.scene.objects.active)
		# ob = foo 

	for (key, val, sub) in tokens:
		if key == 'Modifier':
			parseModifier(ob, val, sub)
		elif key == 'Constraint':
			parseConstraint(ob.constraints, val, sub)
		elif key == 'ParticleSystem':
			parseParticleSystem(ob, val, sub)
		else:
			print(key,val)
			defaultKey(key, val, sub, "ob", ['type', 'data'], globals(), locals())
	return

def createObject(type, name, data):
	if verbosity > 2:
		print( "Creating object %s %s %s" % (type, name, data) )
	ob = bpy.data.objects.new(name, type.upper())
	if data:
		ob.data = data
	ob.name = name
	loadedData['Object'][name] = ob
	bpy.context.scene.objects.link(ob)
	bpy.context.scene.objects.active = ob
	return ob

def createObjectAndData(args, typ):
	datName = args[0]
	obName = args[1]
	bpy.ops.object.add(type=typ.upper())
	ob = bpy.context.object
	ob.name = obName
	ob.data.name = datName
	loadedData[typ][datName] = ob.data
	loadedData['Object'][obName] = ob
	return ob.data


#
#	parseModifier(ob, args, tokens):
#

def parseModifier(ob, args, tokens):
	name = args[0]
	typ = args[1]
	if typ == 'PARTICLE_SYSTEM':
		return None
	print("MOD", name, typ)
	mod = ob.modifiers.new(name, typ)
	for (key, val, sub) in tokens:
		defaultKey(key, val, sub, 'mod', [], globals(), locals())
	print("MOD2", mod)
	return mod

#
#	parseParticleSystem(ob, args, tokens):
#	parseParticles(particles, args, tokens):
#	parseParticle(par, args, tokens):
#

def parseParticleSystem(ob, args, tokens):
	print(ob, bpy.context.object)
	pss = ob.particle_systems
	print(pss, pss.values())
	name = args[0]
	typ = args[1]
	#psys = pss.new(name, typ)
	bpy.ops.object.particle_system_add()
	print(pss, pss.values())
	psys = pss[-1]
	psys.name = name
	psys.settings.type = typ
	loadedData['ParticleSystem'][name] = psys
	print("Psys", psys)

	for (key, val, sub) in tokens:
		if key == 'Particles':
			parseParticles(psys, val, sub)
		else:
			defaultKey(key, val, sub, 'psys', [], globals(), locals())
	return psys

def parseParticles(psys, args, tokens):
	particles = psys.particles
	bpy.ops.particle.particle_edit_toggle()
	n = 0
	for (key, val, sub) in tokens:
		if key == 'Particle':
			parseParticle(particles[n], val, sub)
			n += 1
		else:
			for par in particles:
				defaultKey(key, val, sub, 'par', [], globals(), locals())
	bpy.ops.particle.particle_edit_toggle()
	return particles

def parseParticle(par, args, tokens):
	n = 0
	for (key, val, sub) in tokens:
		if key == 'h':
			h = par.hair[n]
			h.location = eval(val[0])
			h.time = int(val[1])
			h.weight = float(val[2])
			n += 1
		elif key == 'location':
			par.location = eval(val[0])
	return

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
	me = bpy.data.meshes.new(mename)
	loadedData['Mesh'][mename] = me
	ob = createObject('Mesh', obname, me)
	print("Mesh", me, ob)

	verts = []
	edges = []
	faces = []
	vertsTex = []
	texFaces = []

	for (key, val, sub) in tokens:
		if key == 'Verts':
			verts = parseVerts(sub)
		elif key == 'Edges':
			edges = parseEdges(sub)
		elif key == 'Faces':
			faces = parseFaces(sub)

	if faces:
		#x = me.from_pydata(verts, [], faces)
		me.add_geometry(len(verts), 0, len(faces))
		me.verts.foreach_set("co", unpackList(verts))
		me.faces.foreach_set("verts_raw", unpackList(faces))
	else:
		#x = me.from_pydata(verts, edges, [])
		me.add_geometry(len(verts), len(edges), 0)
		me.verts.foreach_set("co", unpackList(verts))
		me.edges.foreach_set("verts", unpackList(edges))
	#print(x)
	me.update()
	print(me)
		
	mats = []
	for (key, val, sub) in tokens:
		if key == 'Verts' or \
		   key == 'Edges':
				pass
		elif key == 'Faces':
			parseFaces2(sub, me)
		elif key == 'MeshTextureFaceLayer':
			parseUvTexture(val, sub, me)
		elif key == 'MeshColorLayer':
			parseVertColorLayer(val, sub, me)
		elif key == 'VertexGroup':
			parseVertexGroup(ob, me, val, sub)
		elif key == 'ShapeKey':
			if doShape(val[0]):
				parseShapeKey(ob, me, val, sub)
		elif key == 'Material':
			try:
				me.add_material(loadedData['Material'][val[0]])
			except:
				print("Could not add material", val[0])
		else:
			defaultKey(key, val,  sub, "me", [], globals(), locals())

	return me

#
#	parseVerts(tokens):
#	parseEdges(tokens):
#	parseFaces(tokens):
#	parseFaces2(tokens, me):		
#

def parseVerts(tokens):
	verts = []
	for (key, val, sub) in tokens:
		if key == 'v':
			coords = rot90(val[0], val[1], val[2], True)
			verts.append( coords )
	return verts

def parseEdges(tokens):
	edges = []
	for (key, val, sub) in tokens:
		if key == 'e':
			edges.append((int(val[0]), int(val[1])))
	return edges
	
def parseFaces(tokens):	
	faces = []
	for (key, val, sub) in tokens:
		if key == 'f':
			if len(val) == 3:
				face = [int(val[0]), int(val[1]), int(val[2]), 0]
			elif len(val) == 4:
				face = [int(val[0]), int(val[1]), int(val[2]), int(val[3])]
			faces.append(face)
	return faces

def parseFaces2(tokens, me):	
	n = 0
	for (key, val, sub) in tokens:
		if key == 'ft':
			f = me.faces[n]
			f.material_index = int(val[0])
			f.smooth = int(val[1])
			n += 1
		elif key == 'ftall':
			mat = int(val[0])
			smooth = int(val[1])
			for f in me.faces:
				f.material_index = mat
				f.smooth = smooth
	return


#
#	parseUvTexture(args, tokens, me):
#	parseUvTexData(args, tokens, uvdata):
#

def parseUvTexture(args, tokens, me):
	me.add_uv_texture()
	uvtex = me.uv_textures[-1]
	name = args[0]
	uvtex.name = name
	loadedData['MeshTextureFaceLayer'][name] = uvtex
	for (key, val, sub) in tokens:
		if key == 'Data':
			parseUvTexData(val, sub, uvtex.data)
		else:
			defaultKey(key, val,  sub, "uvtex", [], globals(), locals())
	return

def parseUvTexData(args, tokens, data):
	n = 0
	for (key, val, sub) in tokens:
		if key == 'vt':
			data[n].uv1 = (float(val[0]), float(val[1]))
			data[n].uv2 = (float(val[2]), float(val[3]))
			data[n].uv3 = (float(val[4]), float(val[5]))
			if len(val) > 6:
				data[n].uv4 = (float(val[6]), float(val[7]))
			n += 1	
		else:
			pass
			#for i in range(n):
			#	defaultKey(key, val,  sub, "data[i]", [], globals(), locals())
	return

#
#	parseVertColorLayer(args, tokens, me):
#	parseVertColorData(args, tokens, data):
#

def parseVertColorLayer(args, tokens, me):
	name = args[0]
	print("VertColorLayer", name)
	me.add_vertex_color()
	vcol = me.vertex_colors[-1]
	vcol.name = name
	loadedData['MeshColorLayer'][name] = vcol
	for (key, val, sub) in tokens:
		if key == 'Data':
			parseVertColorData(val, sub, vcol.data)
		else:
			defaultKey(key, val,  sub, "vcol", [], globals(), locals())
	return

def parseVertColorData(args, tokens, data):
	n = 0
	for (key, val, sub) in tokens:
		if key == 'cv':
			data[n].color1 = eval(val[0])
			data[n].color2 = eval(val[1])
			data[n].color3 = eval(val[2])
			data[n].color4 = eval(val[3])
			n += 1	
	return


#
#	parseVertexGroup(ob, me, args, tokens):
#

def parseVertexGroup(ob, me, args, tokens):
	if verbosity > 2:
		print( "Parsing vertgroup %s" % args )
	grpName = args[0]
	group = ob.add_vertex_group(grpName)
	group.name = grpName
	loadedData['VertexGroup'][grpName] = group
	for (key, val, sub) in tokens:
		if key == 'wv':
			ob.add_vertex_to_group( int(val[0]), group, float(val[1]), 'REPLACE')


#
#	parseShapeKey(ob, me, args, tokens):
#	addShapeKey(ob, name, vgroup, tokens):
#	doShape(name):
#

def doShape(name):
	if (toggle & T_Shape+T_Face) and (name == 'Basis'):
		return True
	else:
		return (toggle & T_Face)

def parseShapeKey(ob, me, args, tokens):
	if verbosity > 0:
		print( "Parsing shape %s" % args[0] )
	name = args[0]
	lr = args[1]
	# bpy.context.scene.objects.active = ob
	if lr == 'Sym':
		addShapeKey(ob, name, None, tokens)
	elif lr == 'LR':
		addShapeKey(ob, name+'_L', 'Left', tokens)
		addShapeKey(ob, name+'_R', 'Right', tokens)
	else:
		raise NameError("ShapeKey L/R %s" % lr)
	return

def addShapeKey(ob, name, vgroup, tokens):
	bpy.ops.object.shape_key_add(False)
	skey = ob.active_shape_key
	if name != 'Basis':
		skey.relative_key = loadedData['ShapeKey']['Basis']
	skey.name = name
	if vgroup:
		skey.vertex_group = vgroup
	loadedData['ShapeKey'][name] = skey

	for (key, val, sub) in tokens:
		if key == 'sv':
			index = int(val[0])
			pt = skey.data[index].co
			(x,y,z) = rot90(float(val[1]), float(val[2]), float(val[3]), True)
			pt[0] += x
			pt[1] += y
			pt[2] += z
		else:
			defaultKey(key, val,  sub, "skey", [], globals(), locals())

	return	

	
#
#	parseArmature (obName, args, tokens)
#

def parseArmature (args, tokens):
	global toggle
	if verbosity > 2:
		print( "Parsing armature %s" % args )
	
	amtname = args[0]
	obname = args[1]
	mode = args[2]

	if mode == 'Rigify':
		toggle |= T_Rigify
		(key,val,sub) = tokens[0]
		if key != 'MetaRig':
			raise NameError("Expected MetaRig")
		typ = val[0]
		print("Metarig ", typ)
		if typ == "human":
			bpy.ops.object.armature_human_advanced_add()
		else:
			bpy.ops.pose.metarig_sample_add(type = typ)
		ob = bpy.context.object
		amt = ob.data
		loadedData['Rigify'][obname] = ob
	else:
		toggle &= ~T_Rigify
		amt = bpy.data.armatures.new(amtname)
		ob = createObject('Armature', obname, amt)	
		# bpy.context.scene.objects.active = ob

	loadedData['Armature'][amtname] = amt
	loadedData['Object'][obname] = ob
	print("Armature", amt, ob)

	bones = {}

	#bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.mode_set(mode='EDIT')
	'''
	fp = open("/home/thomas/test.txt", "w")
	fp.write("Editbones\n")
	for b in amt.edit_bones.keys():
		fp.write("%s\t%s\n" % (b, amt.edit_bones[b]))
	fp.write("\nBones\n")
	for b in amt.bones.keys():
		fp.write("%s\t%s\n" % (b, amt.bones[b]))
	fp.close()
	'''

	heads = {}
	tails = {}
	for (key, val, sub) in tokens:
		if key == 'Bone':
			parseBone(amt, bones, val, sub, heads, tails)
		else:
			defaultKey(key, val,  sub, "amt", ['MetaRig'], globals(), locals())

	bpy.ops.object.mode_set(mode='OBJECT')

	return amt

#
#	parseBone(amt, bones, args, tokens):
#

def parseBone(amt, bones, args, tokens, heads, tails):
	global todo

	name = args[0]
	if toggle & T_Rigify:
		try:
			bone = amt.edit_bones[name]
		except:
			print("Did not find bone %s" %name)
			return None
	else:
		bone = amt.edit_bones.new(name)
	
	loadedData['Bone'][name] = bone

	for (key, val, sub) in tokens:
		if key == "head":
			old = rot90rig(bone.head, True)
			bone.head = rot90(val[0], val[1], val[2], True) 
			heads[name] = bone.head - old
		elif key == "tail":
			old = rot90rig(bone.tail, True)
			bone.tail = rot90(val[0], val[1], val[2], True) 
			tails[name] = bone.tail - old
		elif key == "head-as":
			print("head", val[0], heads[val[0]], bone.head)
			if val[1] == 'head':
				bone.head = rot90rig(bone.head, True) + heads[val[0]]
			elif val[1] == 'tail':
				bone.head = rot90rig(bone.head, True) + tails[val[0]]
			else:
				raise NameError("head-as %s" % val)
			print("  ", bone.head)
		elif key == "tail-as":
			print("tail", val[0], tails[val[0]], bone.tail)
			if val[1] == 'head':
				bone.tail = rot90rig(bone.tail, True) + heads[val[0]]
			elif val[1] == 'tail':
				bone.tail = rot90rig(bone.tail, True) + tails[val[0]]
			else:
				raise NameError("tail-as %s" % val)
			print("  ", bone.tail)
		elif key == "roll":
			if (toggle & T_Rot90):
				bone.roll = float(val[1])
			else:
				bone.roll = float(val[0])
		else:
			defaultKey(key, val,  sub, "bone", [], globals(), locals())

	return bone


#
#	postProcess()
#

def postProcess():
	if toggle & T_Rigify:
		return
		for ob in loadedData['Rigify'].values():
			bpy.context.scene.objects.active = ob
			bpy.ops.pose.metarig_generate()
			bpy.context.scene.objects.unlink(ob)
			ob = bpy.context.object
			print("Rigged", ob)

	else:
		if toggle & T_ArmIK:
			setInfluence(['UpArm_L', 'LoArm_L', 'Hand_L', 'UpArm_R', 'LoArm_R', 'Hand_R'], 1.0)
		if toggle & T_LegIK:
			setInfluence(['UpLeg_L', 'LoLeg_L', 'Foot_L', 'Toe_L', 'UpLeg_R', 'LoLeg_R', 'Foot_R', 'Toe_R'], 1.0)
		if toggle & T_FingerIK:
			for i in range(5):
				for j in range(3):
					setInfluence(['Finger-%d-%d_L' % (i,j), 'Finger-%d-%d_R' % (i,j)], 1.0)
	return

def setInfluence(bones, w):
	ob = loadedData['Object']['HumanRig']
	bpy.context.scene.objects.active = ob
	bpy.ops.object.mode_set(mode='POSE')
	pbones = ob.pose.bones	
	for pb in pbones:
		if pb.name in bones:
			print("setinfl", pb.name)
			for cns in pb.constraints:
				cns.influence = w
	bpy.ops.object.mode_set(mode='OBJECT')
	return

		
	


#
#	parsePose (args, tokens):
#

def parsePose (args, tokens):
	global todo
	if toggle & T_Rigify:
		return
	name = args[0]
	ob = loadedData['Object'][name]
	bpy.context.scene.objects.active = ob
	bpy.ops.object.mode_set(mode='POSE')
	pbones = ob.pose.bones	
	for (key, val, sub) in tokens:
		if key == 'Posebone':
			poseBone(pbones, val, sub)
		else:
			defaultKey(key, val,  sub, "pbones", [], globals(), locals())
	bpy.ops.object.mode_set(mode='OBJECT')
	return ob


#
#	poseBone(pbones, args, tokens):
#	parseArray(list, args):
#

def poseBone(pbones, args, tokens):
	global todo
	if verbosity > 2:
		print( "Parsing posebone %s" % args )
	name = args[0]
	pb = pbones[name]
	for (key, val, sub) in tokens:
		if key == 'Constraint':
			parseConstraint(pb.constraints, val, sub)
		elif key == 'ik_dof':
			parseArray([pb.ik_dof_x, pb.ik_dof_y, pb.ik_dof_z], val)
		elif key == 'ik_limit':
			parseArray([pb.ik_limit_x, pb.ik_limit_y, pb.ik_limit_z], val)
		elif key == 'ik_max':
			parseArray([pb.ik_max_x, pb.ik_max_y, pb.ik_max_z], val)
		elif key == 'ik_min':
			parseArray([pb.ik_min_x, pb.ik_min_y, pb.ik_min_z], val)
		elif key == 'ik_stiffness':
			parseArray([pb.ik_stiffness_x, pb.ik_stiffness_y, pb.ik_stiffness_z], val)
		else:
			defaultKey(key, val,  sub, "pb", [], globals(), locals())
	return

def parseArray(list, args):
	n = 1
	for elt in enumerate(list):
		elt = eval(args[n])
		
#
#	parseConstraint(constraints, args, tokens)
#

def parseConstraint(constraints, args, tokens):
	cns = constraints.new(args[1])
	cns.name = args[0]
	for (key,val,sub) in tokens:
		if key == 'invert':
			parseArray([cns.invert_x, cns.invert_y, cns.invert_z], val)
		elif key == 'use':
			parseArray([cns.use_x, cns.use_y, cns.use_z], val)
		else:
			defaultKey(key, val,  sub, "cns", [], globals(), locals())
	return 
	
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
		if toggle & T_ArmIK:
			cns.influence = 1.0
		else:
			cns.influence = 0.0
	elif bone == 'PLegIK_L' or bone == 'PLegIK_R':
		if toggle & T_LegIK:
			cns.influence = 1.0
		else:
			cns.influence = 0.0

	return True

#
#	parseCurve (args, tokens):
#	parseNurb(cu, nNurbs, args, tokens):
#	parseBezier(nurb, n, args, tokens):
#

def parseCurve (args, tokens):
	global todo
	if verbosity > 2:
		print( "Parsing curve %s" % args )
	cu = createObjectAndData(args, 'Curve')

	nNurbs = 0
	for (key, val, sub) in tokens:
		if key == 'Nurb':
			parseNurb(cu, nNurbs, val, sub)
			nNurbs += 1
		else:
			defaultKey(key, val, sub, "cu", [], globals(), locals())
	return

def parseNurb(cu, nNurbs, args, tokens):
	if nNurbs > 0:
		bpy.ops.object.curve_add(type='BEZIER_CURVE')
	print(cu.splines, list(cu.splines), nNurbs)
	nurb = cu.splines[nNurbs]
	nPoints = int(args[0])
	print(nurb, nPoints)
	for n in range(2, nPoints):
		bpy.ops.curve.extrude(mode=1)		

	n = 0
	for (key, val, sub) in tokens:
		if key == 'bz':
			parseBezier(nurb, n, val, sub)
			n += 1
		elif key == 'pt':
			parsePoint(nurb, n, val, sub)
			n += 1
		else:
			defaultKey(key, val, sub, "nurb", [], globals(), locals())
	return
	
def parseBezier(nurb, n, args, tokens):
	bez = nurb[n]
	bez.co = eval(args[0])	
	bez.handle1 = eval(args[1])	
	bez.handle1_type = args[2]
	bez.handle2 = eval(args[3])	
	bez.handle2_type = args[4]
	return

def parsePoint(nurb, n, args, tokens):
	pt = nurb[n]
	pt.co = eval(args[0])
	return

#
#	parseLattice (args, tokens):
#

def parseLattice (args, tokens):
	global todo
	if verbosity > 2:
		print( "Parsing lattice %s" % args )
	lat = createObjectAndData(args, 'Lattice')	
	for (key, val, sub) in tokens:
		if key == 'Points':
			parseLatticePoints(val, sub, lat.points)
		else:
			defaultKey(key, val, sub, "lat", [], globals(), locals())
	return

def parseLatticePoints(args, tokens, points):
	global todo
	n = 0
	for (key, val, sub) in tokens:
		if key == 'pt':
			v = points[n].co
			(x,y,z) = eval(val[0])
			v.x = x
			v.y = y
			v.z = z

			v = points[n].deformed_co
			(x,y,z) = eval(val[1])
			v.x = x
			v.y = y
			v.z = z

			n += 1
	return

#
#	parseGroup (args, tokens):
#

def parseGroup (args, tokens):
	global todo
	if verbosity > 2:
		print( "Parsing group %s" % args )

	grpName = args[0]
	grp = bpy.data.groups.new(grpName)
	loadedData['Group'][grpName] = grp
	for (key, val, sub) in tokens:
		if key == 'Objects':
			parseGroupObjects(val, sub, grp)
		else:
			defaultKey(key, val, sub, "grp", [], globals(), locals())
	return

def parseGroupObjects(args, tokens, grp):
	global todo
	for (key, val, sub) in tokens:
		if key == 'ob':
			try:
				ob = loadedData['Object'][val[0]]
				grp.objects.link(ob)
				print("add", ob)
			except:
				pass
	return

#
#	defaultKey(ext, args, tokens, var, exclude, glbals, lcals):
#

def defaultKey(ext, args, tokens, var, exclude, glbals, lcals):
	global todo

	if ext == 'Property':
		expr = "%s['%s'] = %s" % (var, args[0], args[1])
		print("Property", expr, eval(var, glbals, lcals))
		exec(expr, glbals, lcals)
		return
		
	nvar = "%s.%s" % (var, ext)
	# print(ext)
	if ext in exclude:
		return
	#print("D", nvar)

	if len(args) == 0:
		raise NameError("Key length 0: %s" % ext)
		
	rnaType = args[0]
	if rnaType == 'Add':
		print("*** Cannot Add yet ***")
		return

	elif rnaType == 'Refer':
		typ = args[1]
		name = args[2]
		data = "loadedData['%s']['%s']" % (typ, name)

	elif rnaType == 'Struct' or rnaType == 'Define':
		typ = args[1]
		name = args[2]
		try:
			data = eval(nvar, glbals, lcals)
		except:
			data = None			
		print("Old structrna", nvar, data)

		if data == None:
			try:
				creator = args[3]
			except:
				creator = None
			print("Creator", creator, eval(var,glbals,lcals))

			try:
				rna = eval(var,glbals,lcals)
				data = eval(creator)
			except:
				data = None	
			print("New struct", nvar, typ, data)

		if rnaType == 'Define':
			loadedData[typ][name] = data

		if data:
			for (key, val, sub) in tokens:
				defaultKey(key, val, sub, "data", [], globals(), locals())

		print("Struct done", nvar)
		return

	elif rnaType == 'PropertyRNA':
		raise NameError("PropertyRNA!")
		#print("PropertyRNA ", ext, var)
		for (key, val, sub) in tokens:
			defaultKey(ext, val, sub, nvar, [], glbals, lcals)
		return

	elif rnaType == 'Array':
		for n in range(1, len(args)):
			expr = "%s[%d] = %s" % (nvar, n-1, args[n])
			exec(expr, glbals, lcals)
		return
		
	elif rnaType == 'List':
		data = []
		for (key, val, sub) in tokens:
			print(key, val, sub, nvar)
			#defaultKey(key, val, sub, nvar, [], glbals, lcals)
			elt = eval(val[1], glbals, lcals)
			data.append(elt)

	elif rnaType == 'Matrix':
		i = 0
		n = len(tokens)
		for (key, val, sub) in tokens:
			if key == 'row':	
				for j in range(n):
					expr = "%s[%d][%d] = %g" % (nvar, i, j, float(val[j]))
					exec(expr, glbals, lcals)
				i += 1
		return

	else:
		try:
			data = loadedData[rnaType][args[1]]
			#print("From loaded", rnaType, args[1], data)
			return data
		except:
			data = rnaType

	#print(var, ext, data)
	expr = "%s = %s" % (nvar, data)
	try:
		exec(expr, glbals, lcals)
	except:
		#print("Failed ",expr)
		todo.append((expr, glbals, lcals))
	return
			
#
#	parseBoolArray(mask):
#

def parseBoolArray(mask):
	list = []
	for c in mask:
		if c == '0':			
			list.append(False)
		else:
			list.append(True)
	return list

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
#	parseDefault(data, tokens, exclude):
#

def parseDefault(data, tokens):
	for (key, val, sub) in tokens:	
		defaultKey(key, val, sub, "data", exclude, globals(), locals())


#
#	Utilities	
#

#
#	extractBpyType(data):
#

def extractBpyType(data):
	typeSplit = str(type(data)).split("'")
	if typeSplit[0] != '<class ':
		return None
	classSplit = typeSplit[1].split(".")
	if classSplit[0] == 'bpy' and classSplit[1] == 'types':
		return classSplit[2]
	elif classSplit[0] == 'bpy_types':
		return classSplit[1]
	else:
		return None

#
#	rot90(x, y, z, doRot)
#	rot90rig(vec, doRot):
#

def rot90(x, y, z, doRot):
	global toggle, theScale
	if (toggle & T_Rot90) and doRot:
		return Vector(float(x)*theScale, -float(z)*theScale, float(y)*theScale)
	else:
		return Vector(float(x)*theScale, float(y)*theScale, float(z)*theScale)


def rot90rig(vec, doRot):
	global toggle, theScale
	scale = 10*theScale
	if (toggle & T_Rot90) and doRot:
		return Vector(vec.x*scale, -vec.z*scale, vec.y*scale)
	else:
		return Vector(vec.x*scale, vec.y*scale, vec.z*scale)

#
#	Bool(string):
#

def Bool(string):
	if string == 'True':
		return True
	elif string == 'False':
		return False
	else:
		raise NameError("Bool %s?" % string)
		
	
#
#	clearScene(context):
#
	
def clearScene():
	global toggle
	scn = bpy.context.scene
	print("clearScene %s %s" % (toggle & T_Replace, scn))
	if not toggle & T_Replace:
		return scn
	for ob in scn.objects:
		if ob.type == "MESH" or ob.type == "ARMATURE":
			scn.objects.unlink(ob)
			del ob
	#print(scn.objects)
	return scn

#
#	User interface
#

DEBUG= False
from bpy.props import *

def check(flag):
	global toggle
	if toggle & flag:
		return "CHECKBOX_HLT"
	else:
		return "CHECKBOX_DEHLT"

class IMPORT_PT_makehuman_mhx(bpy.types.Panel):
	bl_label = "Import MHX"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "scene"

	def draw(self, context):
		row = self.layout.row()
		col = []
		split = row.split(percentage = 1.0/3)
		col.append(split.column())
		col[0].operator("mhxArmIK", icon=check(T_ArmIK))
		col.append(split.column())
		col[1].operator("mhxLegIK", icon=check(T_LegIK))
		col.append(split.column())
		col[2].operator("mhxFingerIK", icon=check(T_FingerIK))

		row = self.layout.row()
		col = []
		split = row.split(percentage = 1.0/3)
		col.append(split.column())
		col[0].operator("mhxFKIK", icon=check(T_FKIK))
		col.append(split.column())
		col[1].operator("mhxDispObs", icon=check(T_DispObs))
		col.append(split.column())
		col[2].operator("mhxReplace", icon=check(T_Replace))

		row = self.layout.row()
		col = []
		split = row.split(percentage = 1.0/3)
		col.append(split.column())
		col[0].operator("mhxShapes", icon=check(T_Face))
		col.append(split.column())
		col[1].operator("mhxRot90", icon=check(T_Rot90))
		col.append(split.column())
		col[2].operator("mhxTexDir")

		row = self.layout.row()
		row.operator("mhxImport")

		return

class OBJECT_OT_mhx_arm_ik(bpy.types.Operator):
	bl_label = "Arm IK"
	bl_idname = "mhxArmIK"
	bl_description = "Arm IK"

	def invoke(self, context, event):
		global toggle
		toggle ^= T_ArmIK
		return{'FINISHED'}

class OBJECT_OT_mhx_leg_ik(bpy.types.Operator):
	bl_label = "Leg IK"
	bl_idname = "mhxLegIK"
	bl_description = "Leg IK"

	def invoke(self, context, event):
		global toggle
		toggle ^= T_LegIK
		return{'FINISHED'}

class OBJECT_OT_mhx_finger_ik(bpy.types.Operator):
	bl_label = "Finger IK"
	bl_idname = "mhxFingerIK"
	bl_description = "Finger IK"

	def invoke(self, context, event):
		global toggle
		toggle ^= T_FingerIK
		return{'FINISHED'}

class OBJECT_OT_mhx_fkik(bpy.types.Operator):
	bl_label = "FK/IK"
	bl_idname = "mhxFKIK"
	bl_description = "FK/IK switch"

	def invoke(self, context, event):
		global toggle
		toggle ^= T_FKIK
		return{'FINISHED'}

class OBJECT_OT_mhx_dispobs(bpy.types.Operator):
	bl_label = "Dispobs"
	bl_idname = "mhxDispObs"
	bl_description = "Display objects"

	def invoke(self, context, event):
		global toggle
		toggle ^= T_DispObs
		return{'FINISHED'}

class OBJECT_OT_mhx_replace(bpy.types.Operator):
	bl_label = "Replace scene"
	bl_idname = "mhxReplace"
	bl_description = "Replace scene"

	def invoke(self, context, event):
		global toggle
		toggle ^= T_Replace
		return{'FINISHED'}


class OBJECT_OT_mhx_shapes(bpy.types.Operator):
	bl_label = "Shapes"
	bl_idname = "mhxShapes"
	bl_description = "Shape keys"

	def invoke(self, context, event):
		global toggle
		toggle ^= T_Face
		return{'FINISHED'}

class OBJECT_OT_mhx_rot90(bpy.types.Operator):
	bl_label = "Rot 90"
	bl_idname = "mhxRot90"
	bl_description = "Rotate 90 degrees (Y up)"

	def invoke(self, context, event):
		global toggle
		toggle ^= T_Rot90
		return{'FINISHED'}

class OBJECT_OT_mhx_texdir(bpy.types.Operator):
	bl_label = "Tex dir"
	bl_idname = "mhxTexDir"
	bl_description = "Choose texture directory"

	def invoke(self, context, event):
		return{'FINISHED'}

class OBJECT_OT_mhx_import(bpy.types.Operator):
	bl_label = "Import MHX file"
	bl_idname = "mhxImport"
	bl_description = "Import MHX file"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"

	path = StringProperty(name="File Path", description="File path used for importing the MHX file", maxlen= 1024, default= "")

	def execute(self, context):
		readMhxFile(self.properties.path)
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.manager
		wm.add_fileselect(self)
		return {'RUNNING_MODAL'}


bpy.types.register(OBJECT_OT_mhx_arm_ik)
bpy.types.register(OBJECT_OT_mhx_leg_ik)
bpy.types.register(OBJECT_OT_mhx_finger_ik)
bpy.types.register(OBJECT_OT_mhx_fkik)
bpy.types.register(OBJECT_OT_mhx_dispobs)
bpy.types.register(OBJECT_OT_mhx_replace)
bpy.types.register(OBJECT_OT_mhx_shapes)
bpy.types.register(OBJECT_OT_mhx_rot90)
bpy.types.register(OBJECT_OT_mhx_texdir)
bpy.types.register(OBJECT_OT_mhx_import)
bpy.types.register(IMPORT_PT_makehuman_mhx)


"""
class IMPORT_OT_makehuman_mhx(bpy.types.Operator):
	'''Import from MHX file format (.mhx)'''
	bl_idname = "import_scene.makehuman_mhx"
	bl_description = 'Import from MHX file format (.mhx)'
	bl_label = "Import MHX"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"

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
		readMhxFile(self.properties.path)
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.manager
		wm.add_fileselect(self)
		return {'RUNNING_MODAL'}

bpy.types.register(IMPORT_OT_makehuman_mhx)
menu_func = lambda self, context: self.layout.operator(IMPORT_OT_makehuman_mhx.bl_idname, text="MakeHuman (.mhx)...")
bpy.types.INFO_MT_file_import.append(menu_func)

#
#	Testing
#
theScale = 1.0
toggle = T_Replace + T_ArmIK + T_LegIK + T_Face
toggle = T_Replace + T_Face
readMhxFile("/home/thomas/makehuman/exports/foo-classic-25.mhx")
#readMhxFile("/home/thomas/makehuman/exports/foo-rigify-25.mhx")
#readMhxFile("C:/Documents and Settings/xxxxxxxxxxxxxxxxxxxx/Mina dokument/makehuman/exports/foo-classic-25.mhx")
#readMhxFile("/home/thomas/mhx5/test1.mhx")
#readMhxFile("/home/thomas/myblends/mhx4/test1.mhx")
"""




