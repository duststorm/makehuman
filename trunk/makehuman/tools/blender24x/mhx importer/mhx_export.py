#!BPY
""" 
Name: 'Makehuman (.mhx)'
Blender: 249
Group: 'Export'
Tooltip: 'Export from MakeHuman eXchange format (.mhx)'
"""

__author__= ['Thomas Larsson']
__url__ = ("www.makehuman.org")
__version__= '0.7'
__bpydoc__= '''\
MHX exporter for Blender
'''
""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyamtht(c):**      MakeHuman Team 2001-2013

**Licensing:**         GPL3 (see also http://www.makehuman.org/node/319)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

MHX (MakeHuman eXchange format) exporter for Blender.

TODO
"""

import Blender
from Blender import *
from Blender.Mathutils import *
import os

MAJOR_VERSION = 0
MINOR_VERSION = 7
verbosity = 1
Epsilon = 1e-6
done = 0

toggleMhxBase = 0
toggleGeoOnly = 0
MHDir = "/home/svn/"


#
#	getObject(ob):
#

def getObject(ob):
	if ob:
		return ob.name.replace(' ', '_')
	else:
		return "None"

#
#	getString(name):
#

def getString(name):
	if name:
		return name.replace(' ', '_')
	else:
		return "None"

#
#	writeList(var, list, fp, n):
#

def writeList(var, list, fp, n):
	for elt in list:
		(type,ext) = elt
		save = True
		try:
			(test, ext1) = ext
			save = False
			if getattr(var, test)
				ext = ext1
				save = True
		except:
			pass
		
		if save:
			try:
				writeTyped(type, ext, getattr(var, ext), fp, n)
			except:
				pass

#
#	writeTyped(type, key, arg, fp, n):
#

def writeTyped(type, key, arg, fp, n):
	#print "writeTyped", type, key, arg
	indent(fp, n)
	if type == "float":
		fp.write("%s %f ;\n" % (key, arg))
	elif type == "int":
		fp.write("%s %d ;\n" % (key, arg))
	elif type == "xint":
		fp.write("%s 0x%x ;\n" % (key, arg))
	elif type == "bool":
		if arg:
			fp.write("%s true ;\n" % key)
		else:
			fp.write("%s false ;\n" % key)
	elif type == "string":
		if arg != '':
			fp.write("%s '%s' ;\n" % (key, arg.replace(' ','_')))
	elif type == "object":
		fp.write("%s _object['%s'] ;\n" % (key, arg.name.replace(' ','_')))
	elif type == "ipo":
		fp.write("%s _ipo['%s'] ;\n" % (key, arg.name.replace(' ','_')))
	elif type == "texture":
		fp.write("%s _texture['%s'] ;\n" % (key, arg.name.replace(' ','_')))
	elif type == "tuple2ints":
		fp.write("%s (%x,%x) ;\n" % (key, arg[0], arg[1]))
	elif type == "tuple3ints":
		fp.write("%s (%x,%x,%x) ;\n" % (key, arg[0], arg[1], arg[2]))
	elif type == "tuple4ints":
		fp.write("%s (%x,%x,%x,%x) ;\n" % (key, arg[0], arg[1], arg[2], arg[3]))
	elif type == "tuple2floats":
		fp.write("%s (%f,%f) ;\n" % (key, arg[0], arg[1]))
	elif type == "tuple3floats":
		fp.write("%s (%f,%f,%f) ;\n" % (key, arg[0], arg[1], arg[2]))
	elif type == "tuple4floats":
		fp.write("%s (%f,%f,%f,%f) ;\n" % (key, arg[0], arg[1], arg[2], arg[3]))
	elif type == listInts:
		fp.write("%s (%d," % (key, arg[0]))
		first = False
		for arg in listInts:
			if first:
				first = false
			else:
				fp.write("%d," % arg)
		fp.write(")")
		
	else:
		raise NameError("Unknown type "+type)


#
#	writeMhxBases()	
#

def writeMhxBases():
	global done, toggleMhxBase

	toggleMhxBase = True
	
	#
	# Materials
	#
	fileName = MHDir + "data/3dobjs/materials24.mhx"
	print "Writing MHX material file " + fileName
	fp = open(fileName, 'w')
	fp.write("# MHX materials for Blender 2.49 \n")
	fp.write("\n# --------------- Textures ----------------------------- # \n \n")
	for tex in Texture.Get():
		exportTexture(tex, fp)

	fp.write("\n# --------------- Materials ----------------------------- # \n \n")
	for mat in Material.Get():
		exportMaterial(mat, fp)

	fp.close()
	print "Material file %s written" % fileName

	scn = Scene.GetCurrent()
	
	#
	# Meshes
	# 
	fileName = MHDir + "data/3dobjs/meshes24.mhx"
	print "Writing MHX meshes file " + fileName
	fp = open(fileName, 'w')
	fp.write("# MHX meshes for Blender 2.49 \n")

	for ob in scn.objects:
		if ob.type == "Mesh":
			exportObject(ob, fp)

	fp.close()
	print "Mesh file %s written" % fileName

	#
	# Shapekeys
	# 
	fileName = MHDir + "data/3dobjs/shapekeys24.mhx"
	print "Writing MHX shapekey file " + fileName
	fp = open(fileName, 'w')
	fp.write("# MHX shapekeys for Blender 2.49 \n")

	ob = Object.Get('Human')
	me = ob.getData(False, True)
	exportShapeKeys(fp, me)

	fp.close()
	print "Shapekey file %s written" % fileName

	#
	# Armature
	# 
	fileName = MHDir + "data/3dobjs/armature24.mhx"
	print "Writing MHX armature file " + fileName
	fp = open(fileName, 'w')
	fp.write("# MHX armatures for Blender 2.49 \n")

	ob = Object.Get('HumanRig')
	exportObject(ob, fp)

	fp.close()
	print "Armature file %s written" % fileName
	
	return

#
#	writeMhxFile(fileName):
#

def writeMhxFile(fileName):
	global done
	n = len(fileName)
	if fileName[n-3:] != "mhx":
		Draw.PupMenu("Error: Not a mhx file: " + fileName)
		return

	# Write MHX file
	print "Writing MHX file " + fileName
	fp = open(fileName, 'w')
	fp.write("# Blender exported MHX \n")
	fp.write("MHX %d %d ;\n" % (MAJOR_VERSION, MINOR_VERSION))
	scn = Scene.GetCurrent()

	fp.write("\n# ---------------- Groups -------------------------------- # \n \n")
	for grp in Group.Get():
		exportGroup(grp, fp)

	if not toggleGeoOnly:
		fp.write("\n# ------------------ IPOs -------------------------------- # \n \n")
		for ipo in Ipo.Get():
			exportIpo(ipo, fp, False)

		fp.write("\n# ---------------- Actions -------------------------------- # \n \n")
		for act in Armature.NLA.GetActions().values():
			print act
			exportAction(act, fp)

	fp.write("\n# --------------- Textures ----------------------------- # \n \n")
	for tex in Texture.Get():
		exportTexture(tex, fp)
	fp.write("\n# --------------- Materials ----------------------------- # \n \n")
	for mat in Material.Get():
		exportMaterial(mat, fp)

	for ob in scn.objects:
		exportObject(ob, fp)

	fp.close()
	print "MHX file %s written \n" % (fileName)
	done = 1

#
#	exportMaterial(mat, fp):
#

def listColorBand(band, name, fp):
	if band:
		fp.write("  %s\n" % name)
		for col in band:
			fp.write("    color %f %f %f %f %f ;\n" % (col[0], col[1], col[2], col[3], col[4]))
		fp.write("  end %s\n" % name)

def exportMaterial(mat, fp):
	fp.write("material %s \n" % mat.name.replace(' ', '_'))
	fp.write("  rgba %f %f %f %f ;\n" % (mat.R, mat.G, mat.B, mat.alpha))
	for (n,mtex) in enumerate(mat.textures):
		if mtex:
			exportMTex(n, mtex, fp)
	if mat.ipo:
		exportIpo(mat.ipo, fp, True)
	listColorBand(mat.colorbandDiffuse, "colorbandDiffuse", fp)
	listColorBand(mat.colorbandSpecular, "colorbandSpecular", fp)
	writeList(mat, materialList, fp, 2)
	fp.write("end material\n\n")

materialList = [
	("float", "IOR"),
	("float", "add"),
	("float", "amb"),
	("float", "anisotropy"),
	("float", ("colorbandDiffuse", "colorbandDiffuseFactor")),
	("int", ("colorbandDiffuse", "colorbandDiffuseInput")),
	("int", ("colorbandDiffuse", "colorbandDiffuseMethod")),
	("float", ("colorbandSpecular", "colorbandSpecularFactor")),
	("int", ("colorbandSpecular", "colorbandSpecularInput")),
	("int", ("colorbandSpecular", "colorbandSpecularMethod")),
	("float", "diffuseDarkness"),
	("int", "diffuseShader"),
	("float", "diffuseSize"),
	("float", "diffuseSmooth"),
	("float", "emit"),
	("bool", "enableSSS"),
	("listInts", "enabledTextures"),
	("float", "filter"),
	("float", "flareBoost"),
	("int", "flareSeed"),
	("float", "flareSize"),
	("float", "fresnelDepth"),
	("float", "fresnelDepthFac"),
	("float", "fresnelTrans"),
	("float", "fresnelTransFac"),
	("float", "glossMir"),
	("float", "glossTra"),
	("int", "haloSeed"),
	("float", "haloSize"),
	("int", "hard"),
	#("ipo", "ipo"),
	("string", "lib"),
	("group", "lightGroup"),
	("float", "mirB"),
	("tuple3floats", "mirCol"),
	("float", "mirG"),
	("float", "mirR"),
	("xint", "mode"),
	("int", "nFlares"),
	("int", "nLines"),
	("int", "nRings"),
	("int", "nStars"),
	("tuple2floats", "oopsLoc"),
	("int", "oopsSel"),
	("float", "rayMirr"),
	("int", "rayMirrDepth"),
	("float", "rbFriction"),
	("float", "rbRestitution"),
	("float", "ref"),
	("float", "refracIndex"),
	("tuple3floats", "rgbCol"),
	("float", "rms"),
	("float", "roughness"),
	("int", "sampGlossTra"),
	("int", "sampGloss_mir"),
	("float", "shadAlpha"),
	("int", "shadeMode"),
	("float", "spec"),
	("float", "specB"),
	("tuple3floats", "specCol"),
	("float", "specG"),
	("float", "specR"),
	("int", "specShader"),
	("float", "specSize"),
	("float", "specSmooth"),
	("float", "specTransp"),
	("float", "sssB"),
	("float", "sssBack"),
	("tuple3floats", "sssCol"),
	("float", "sssColorBlend"),
	("float", "sssError"),
	("float", "sssFront"),
	("float", "sssG"),
	("float", "sssIOR"),
	("float", "sssR"),
	("float", "sssRadiusBlue"),
	("float", "sssRadiusGreen"),
	("float", "sssRadiusRed"),
	("float", "sssScale"),
	("float", "sssTextureScatter"),
	("int", "strandBlendUnit"),
	("float", "strandDist"),
	("float", "strandEnd"),
	("float", "strandFade"),
	# ("float", "strandMin"),
	("float", "strandShape"),
	("float", "strandStart"),
	("int", "strandSurfDiff"),
	("int", "strandTanShad"),
	("float", "subSize"),
	("float", "threshMir"),
	("float", "threshTra"),
	("int", "transDepth"),
	("float", "translucency"),
	("string", "uvlayer"),
	("float", "zOffset")\
]

#
#
#

def exportTexture(tx, fp):
	global todo
	typename = "None"
	for (str, index) in Texture.Types.items():
		if tx.type == index:
			typename = str
			break
	if typename == "None":
		return
	fp.write("texture %s %s\n" % (typename, tx.name.replace(' ', '_')))
	if tx.image:
		exportImage(tx.image, fp)
	if tx.ipo:
		exportIpo(tx.ipo, fp, True)
	listColorBand(tx.colorband, "colorband", fp)
	writeList(tx, textureList, fp, 2)
	fp.write("end texture\n\n")
	return

textureList = [
	("int", "animFrames"),
	("int", "animOffset"),
	("int", "animStart"),
	("int", "anti"),
	("bool", "autoRefresh"),
	("float", "bamthtness"),
	("int", "calcAlpha"),
	("float", "contrast"),
	("tuple4ints", "crop"),
	("bool", "cyclic"),
	("float", "distAmnt"),
	("int", "distMetric"),
	("float", "exp"),
	("int", "extend"),
	("int", "fields"),
	("int", "fieldsPerImage"),
	("float", "filterSize"),
	("xint", "flags"),
	("float", "gain"),
	("float", "hFracDim"),
	("float", "iScale"),
	("xint", "imageFlags"),
	("int", "interpol"),
	#("ipo", "ipo"),
	("float", "lacunarity"),
	("string", "lib"),
	("int", "mipmap"),
	("int", "movie"),
	("int", "noiseBasis"),
	("int", "noiseBasis2"),
	("int", "noiseDepth"),
	("float", "noiseSize"),
	("string", "noiseType"),
	("int", "normalMap"),
	("float", "octs"),
	("float", "offset"),
	("tuple2ints", "repeat"),
	("tuple3floats", "rgbCol"),
	("int", "rot90"),
	# ("int", "saw"),
	("int", "sine"),
	("int", "stField"),
	("int", "stype"),
	# ("int", "tri"),
	("float", "turbulence"),
	("int", "useAlpha"),
	("int", "useColorband"),
	("float", "weight1"),
	("float", "weight2"),
	("float", "weight3"),
	("float", "weight4")
]

#
#
#

def exportMTex(index, mtex, fp):
	print mtex
	name = mtex.tex.name.replace(' ','_')
	fp.write("  mtex %d %s\n" % (index, name))
	fp.write("    texco 0x%x ;\n" % mtex.texco)
	fp.write("    mapto 0x%x ;\n" % mtex.mapto)    
	writeList(mtex, mTexList, fp, 2)
	fp.write("  end mtex\n")
	return

mTexList = [
	("int", "blendmode"),
	("tuple3floats", "col"),
	("float", "colfac"),
	("bool", "correctNor"),
	("float", "dispfac"),
	("float", "dvar"),
	#("ipo", "ipo"),
	("bool", "fromDupli"),
	("bool", "fromOamt"),
	("xint", "mapping"),
	#("xint", "mapto"),
	("bool", "neg"),
	("bool", "noRGB"),
	("float", "norfac"),
	("object", "object"),
	("tuple", "ofs"),
	("tuple", "size"),
	("bool", "stencil"),
	# ("texture", "tex"),
	#("xint", "texco"),
	("string", "uvlayer"),
	("float", "varfac"),
	("float", "warpfac"),
	("int", "xproj"),
	("int", "yproj"),
	("int", "zproj")
]

#
#
#

def exportImage(img, fp):
	fp.write("  image %s\n" % img.name)
	(filepath, filename) = os.path.split(img.filename)
	fp.write("    filename %s ;\n" % (filename))
	if not toggleGeoOnly:
		writeList(img, imageList, fp, 2)
	fp.write("  end image\n")
	return
	
imageList = [
	("bool", "antialias"),
	("bool", "clampX"),
	("bool", "clampY"),
	#("int", "end"),
	("bool", "fields"),
	("bool", "fields_odd"),
	("string", "lib"),
	("bool", "premul"),
	("int", "source"),
	("int", "speed"),
	("int", "start"),
	("int", "xrep"),
	("int", "yrep")
]

#
#	exportParticle(par, fp):
#

def exportParticle(par, fp):
	name = par.getName().replace(' ','_')
	fp.write("  particle %s \n" % name)
	writeList(par, particleList, fp, 3)

	'''
	for loc in par.getLoc():
		fp.write("    loc \n")
		for x in loc:
			fp.write("      v %f %f %f ;\n" % (x[0], x[1], x[2]))
		fp.write("    end loc\n")

	if par.getRot():
		for rot in par.getRot():
			fp.write("    rot \n")
			for x in rot:
				fp.write("      v %f %f %f ;\n" % (x[0], x[1], x[2]))
			fp.write("    end rot\n")
			
	for size in par.getSize():
		for x in size:
			fp.write("    size %d ;\n" % x)
	'''
				
	if par.getMat():
		mat = par.getMat()
		fp.write("    material %s ;\n" % mat.name.replace(' ','_'))
			
	for (name, n) in Particle.VERTEXGROUPS.items():
		vg = par.getVertGroup(n) 
		if vg[0]:
			fp.write("    vertGroup %s %s %d ;\n" % (name, vg[0], vg[1]))

	fp.write("  end particle\n")
	return

particleList = [
	("float",	"2d"),
	("int",	"amount"),
	("float",	"avvel"),
	("int",	"childAmount"),
	("int",	"childBranch"),
	("int",	"childBranchAnim"),
	("int",	"childBranchSymm"),
	("float",	"childBranchThre"),
	("float",	"childClump"),
	("int",	"childKink"),
	("float",	"childKinkAmp"),
	("int",	"childKinkAxis"),
	("float",	"childKinkFreq"),
	("float",	"childKinkShape"),
	("float",	"childRadius"),
	("float",	"childRand"),
	("int",	"childRenderAmount"),
	("float",	"childRough1"),
	("float",	"childRough1Size"),
	("float",	"childRough2"),
	("float",	"childRough2Size"),
	("float",	"childRough2Thresh"),
	("float",	"childRoughE"),
	("float",	"childRoughEShape"),
	("float",	"childRound"),
	("float",	"childShape"),
	("float",	"childSize"),
	("int",	"childType"),
	("int",	"displayPercentage"),
	("int",	"distribution"),
	("int",	"drawAs"),
	("object", "duplicateObject"),
	("int",	"editable"),
	("float",	"endFrame"),
	("int",	"evenDistribution"),
	("float",	"glAccX"),
	("float",	"glAccY"),
	("float",	"glAccZ"),
	("float",	"glBrown"),
	("float",	"glDamp"),
	("float",	"glDrag"),
	("float",	"groundz"),
	("int",	"hairDisplayStep"),
	("int",	"hairRenderStep"),
	("int",	"hairSegments"),
	("float",	"inVelNor"),
	("float",	"inVelObj"),
	("float",	"inVelPart"),
	("float",	"inVelRan"),
	("float",	"inVelReact"),
	("float",	"inVelRot"),
	("float",	"inVelTan"),
	("int",	"integration"),
	("int",	"invert"),
	("float",	"jitterAmount"),
	("float",	"latacc"),
	("float",	"lifetime"),
	("float",	"maxvel"),
	("int",	"multireact"),
	("object", 	"object"),
	("int",	"particleDistribution"),
	("int",	"pf"),
	("int",	"physics"),
	("int",	"randemission"),
	("float",	"randlife"),
	("float",	"reactshape"),
	("int",	"renderDied"),
	("int",	"renderEmitter"),
	("int",	"renderMatCol"),
	("int",	"renderMaterial"),
	("int",	"renderParents"),
	("int",	"renderUnborn"),
	("int",	"resolutionGrid"),
	("int",	"rotAnV"),
	("float",	"rotAnVAm"),
	("int",	"rotDyn"),
	("float",	"rotPhase"),
	("float",	"rotPhaseR"),
	("float",	"rotRand"),
	("int",	"rotation"),
	("int",	"seed"),
	("float",	"startFrame"),
	("int",	"strandRender"),
	("int",	"strandRenderAngle"),
	("float", "tanacc"),
	("object", "targetObject"),
	("int",	"targetpsys"),
	("xint",	"type")
]

#
#	exportIpo(ipo, fp, local):
#
ipoBlockTypes = dict({\
	0x424f : "Object",
	0x4143 : "Camera",
	0x4f57 : "World",
	0x414d : "Material",
	0x4554 : "Texture",
	0x414c : "Lamp",
	0x4341 : "Action",
	0x4f43 : "Constraint",
	0x5153 : "Sequence",
	0x5543 : "Curve",
	0x454b : "Key" \
})

def exportIpo(ipo, fp, local):
	if ipo == None or ipo.name == "None":
		return
	
	name = ipo.name
	typeint = ipo.getBlocktype()
	type = ipoBlockTypes[typeint]

	if local:
		if type != 'Key' and type != 'Material' and type != 'Texture':
			return
	else:
		if type == 'Key' or type == 'Material' or type == 'Texture':
			return

	fp.write("ipo %s %s \n" % (type, ipo.name.replace(' ','_')))
	for icu in ipo:
		exportIcu(icu, fp)
	fp.write("end ipo\n")
	return

#
#	exportIcu(icu, fp):
#

def exportIcu(icu, fp):
	fp.write("  icu %s %x %x \n" % (icu.name.replace(' ','_'), icu.extend, icu.interpolation))
	for bz in icu.bezierPoints:
		[h1, p, h2] = bz.vec
		fp.write("    bz2 %f %f %f %f %f %f  ;\n" % \
			(h1[0], h1[1], p[0], p[1], h2[0], h2[1]))

	writeList(icu, icuList, fp, 3)
	if icu.driver:
		print "icu ", icu.driverObject, icu.driverBone, icu.driverChannel
	fp.write("    end icu\n")

icuList = [
	("int", "driver"),
	("object", ("driverObject", "driverObject")),
	("string", ("driverObject", "driverBone")),
	("string", ("driverObject", "driverBone2")),
	("int", ("driverObject", "driverChannel")),
	("string", "driverExpression"),
	("int", "extend"),
	("int", "interpolation"),
]

#
#	exportAction(act, fp):
#

def exportAction(act, fp):
	fp.write("\naction %s \n" % act.name.replace(' ','_'))
	ipos = act.getChannelNames()
	for name in ipos:
		fp.write("  ipo %s ;\n" % name.replace(' ','_'))
	fp.write("    end action\n")
	return
		
#
#	exportActionStrip(strip, fp):
#

def exportActionStrip(strip, fp):
	fp.write("\nactionstrip %s \n" % strip.name.replace(' ','_'))
	writeList(strip, actionStripList, fp, 2)
	fp.write("    end actionstrip\n")
	return

actionStripList = [
	("action", "action"),
	("float", "actionEnd"),
	("float", "actionStart"),
	("float", "blendIn"),
	("float", "blendOut"),
	("xint", "flag"),
	("object", "groupTarget"),
	("xint", "mode"),
	("float", "repeat"),
	("int", "strideAxis"),
	("string", "strideBone"),
	("float", "strideLength"),
	("float", "stripEnd"),
	("float", "stripStart")
]

#
#	exportMatrix(A, fp):
#

def exportMatrix(A, fp):
	fp.write("  matrix \n")
	for i in range(4):
		fp.write("    row %f %f %f %f ;\n" % (A[i][0], A[i][1], A[i][2], A[i][3]))
	fp.write("  end matrix\n")

#
#	exportObject(ob, fp):
#

def exportObject(ob, fp):
	fp.write("\n# ----------------------------- %s --------------------- # \n\n" % ob.type )
	if ob.type == "Mesh":
		exportMesh(ob, fp)
	elif toggleMhxBase:
		return
	elif ob.type == "Armature":
		exportArmature(ob, fp)
	elif ob.type == "Empty":
		fp.write("empty ;\n")
	elif toggleGeoOnly:
		return
	elif ob.type == "Lattice":
		exportLattice(ob,fp)
	elif ob.type == "Lamp":
		exportLamp(ob,fp)
	elif ob.type == "Camera":
		exportCamera(ob,fp)
	elif ob.type == "Curve":
		exportCurve(ob,fp)
	elif ob.type == "Text":
		exportText(ob,fp)
	else:
		raise NameError( "Unknown type "+ob.type )

	obName = ob.name.replace(' ', '_')
	data = ob.getData()
	if data:
		datName = data.name.replace(' ', '_')
		fp.write("object %s %s %s \n" % (obName, ob.type, datName))
	else:
		fp.write("object %s %s \n" % (obName, ob.type))
	lay1 = ob.Layers & 0x3ff
	lay2 = (ob.Layers >> 10) & 0x3ff
	fp.write("  layers %x %x ;\n" % (lay1, lay2))
	A = ob.getMatrix('localspace')
	exportMatrix(A, fp)

	if ob.parent:
		if ob.parentbonename:
			extra = ob.parentbonename.replace(' ', '_')
		elif len(ob.parentVertexIndex) == 1:
			extra = str(ob.parentVertexIndex[0])
		elif len(ob.parentVertexIndex) == 3:
			extra = str(ob.parentVertexIndex[0])+\
			"_"+str(ob.parentVertexIndex[1])+\
			"_"+str(ob.parentVertexIndex[2])
		else:
			extra = "None"
		fp.write("  parent %s %x %s ;\n" % ( ob.parent.name.replace(' ', '_'), ob.parentType, extra))

	if ob.ipo:
		fp.write("  ipo %s ;\n" % ob.ipo.name.replace(' ','_'))
	
	if not toggleGeoOnly:
		writeList(ob, objectList, fp, 2)

	for cns in ob.constraints:
		exportConstraint(cns, fp)

	particles = ob.getParticleSystems()
	for par in particles:
		exportParticle(par, fp)

	for mod in ob.modifiers:
		exportModifier(mod, fp)

	fp.write("end object\n\n")
	return #exportObject2

objectList = [
	("int", "DupEnd"),
	("group", "DupGroup"),
	("int", "DupOff"),
	("int", "DupOn"),
	("int", "DupSta"),
	#("float", "LocX"),
	#("float", "LocY"),
	#("float", "LocZ"),
	#("float", "RotX"),
	#("float", "RotY"),
	#("float", "RotZ"),
	#("float", "SizeX"),
	#("float", "SizeY"),
	#("float", "SizeZ"),
	#("tuple3floats", "loc"),
	#("tuple3floats", "rot"),
	#("tuple3floats", "size"),
	("float", "SBDefaultGoal"),
	("float", "SBErrorLimit"),
	("float", "SBFriction"),
	("float", "SBGoalFriction"),
	("float", "SBGoalSpring"),
	("float", "SBGrav"),
	("float", "SBInnerSpring"),
	("float", "SBInnerSpringFrict"),
	("float", "SBMass"),
	("float", "SBMaxGoal"),
	("float", "SBMinGoal"),
	("float", "SBSpeed"),
	("bool", "SBStiffQuads"),
	("bool", "SBUseEdges"),
	("bool", "SBUseGoal"),
	("int", "activeMaterial"),
	("int", "activeShape"),
	("bool", "axis"),
	("xint", "colbits"),
	("tuple4floats", "color"),
	#("float", "dLocX"),
	#("float", "dLocY"),
	#("float", "dLocZ"),
	#("float", "dRotX"),
	#("float", "dRotY"),
	#("float", "dRotZ"),
	#("float", "dSizeX"),
	#("float", "dSizeY"),
	#("float", "dSizeZ"),
	("tuple3floats", "dloc"),
	("tuple3floats", "drot"),
	("tuple3floats", "dsize"),
	("int", "drawMode"),
	("float", "drawSize"),
	("int", "drawType"),
	#("float", "dupFacesScaleFac"),
	("bool", "enableDupFaces"),
	("bool", "enableDupFacesScale"),
	("bool", "enableDupFrames"),
	("bool", "enableDupGroup"),
	("bool", "enableDupNoSpeed"),
	("bool", "enableDupRot"),
	("bool", "enableDupVerts"),
	("bool", "enableNLAOverride"),
	("bool", "fakeUser"),
	#("ipo", "ipo"),
	#("bool", "isSoftBody"),
	("string", "lib"),
	("bool", "nameMode"),
	("tuple2floats", "oopsLoc"),
	("bool", "oopsSel"),
	#("object", "parent"),
	#("int", "parentType"),
	#("listInts", "parentVertexIndex"),
	#("string", "parentbonename"),
	("int", "passIndex"),
	("float", ("piType", "piFalloff")),
	("float", ("piType", "piMaxDist")),
	("float", ("piType", "piPermeability")),
	("float", ("piType", "piRandomDamp")),
	("float", ("piType", "piSoftbodyDamp")),
	("float", ("piType", "piSoftbodyIThick")),
	("float", ("piType", "piSoftbodyOThick")),
	("float", ("piType", "piStrength")),
	("float", ("piType", "piSurfaceDamp")),
	("int", ("piType", "piType")),
	("bool", ("piType", "piUseMaxDist")),
	("bool", ("piType", "pinShape")),
	("xint", "protectFlags"),
	("xint", "rbFlags"),
	("float", "rbMass"),
	("float", "rbRadius"),
	("int", "rbShapeBoundType"),
	("bool", "restrictDisplay"),
	("bool", "restrictRender"),
	("bool", "restrictSelect"),
	("bool", "texSpace"),
	("float", "timeOffset"),
	("object", "track"),
	("bool", "transp"),
	("bool", "wireMode"),
	("bool", "xRay")
]

#
#	exportMesh(ob, fp):
#

def exportMesh(ob, fp):
	me = ob.getData(False, True)
	meName = me.name.replace(' ', '_')
	obName = ob.name.replace(' ', '_')
	if verbosity > 0:
		print "Saving mesh "+meName

	fp.write("mesh %s %s \n" % (meName, obName))
	for mat in me.materials:
		fp.write("  material %s ;\n" % mat.name.replace(" ", "_"))
	if toggleMhxBase and obName == 'Human':
		v = me.verts[0]
		fp.write("  v %f %f %f ;\n" %(v.co[0], v.co[1], v.co[2]))
	else:
		for v in me.verts:
			fp.write("  v %f %f %f ;\n" %(v.co[0], v.co[1], v.co[2]))
	if verbosity > 1:
		print "Verts saved"

	#
	#	Vertex UV
	#
	if me.vertexUV:
		for v in me.verts:
			fp.write("  vt %f %f ;\n" %(v.uvco[0], v.uvco[1]))
		if verbosity > 1:
			print "UVs saved"

	#
	#	Faces and face UV
	#
	if me.faceUV:
		if toggleMhxBase and obName == 'Human':
			print "single face with vt"
			f = me.faces[0]
			for uv in f.uv:
				fp.write("  vt %f %f ;\n" %(uv.x, uv.y))
			fp.write("  f")
			v = f.verts[0]
			n = 0
			for v in f.verts:
				fp.write(" %d/%d" %( v.index, n ))
				n += 1
			fp.write(" ;\n")
		else:
			print "multi faces with vt"
			for f in me.faces:
				for uv in f.uv:
					fp.write("  vt %f %f ;\n" %(uv.x, uv.y))
			n = 0
			for f in me.faces:
				fp.write("  f")
				for v in f.verts:
					fp.write(" %d/%d" %( v.index, n ))
					n += 1
				fp.write(" ;\n")
		if len(me.materials) <= 1:
			fp.write("  ftall %x %x %d %d %d ;\n" % (f.flag, f.mode, f.transp, f.mat, f.smooth))
		else:
			for f in me.faces:
				fp.write("  ft %d %x %x %d %d %d ;\n" % (f.index, f.flag, f.mode, f.transp, f.mat, f.smooth))
			
	elif me.faces:
		if toggleMhxBase and obName == 'Human':
			print "single face w/o vt"
			fp.write("  f")
			f = me.faces[0]
			for v in f.verts:
				fp.write(" %i" %( v.index ))
			fp.write(" ;\n")

		else:
			print "multi faces w/o vt"
			for f in me.faces:
				fp.write("  f")
				for v in f.verts:
					fp.write(" %i" %( v.index ))
				fp.write(" ;\n")
		if len(me.materials) <= 1:
			fp.write("  fxall %d %d ;\n" %  ( f.mat, f.smooth))
		else:
			for f in me.faces:
				fp.write("  fx %d %d %d ;\n" %  ( f.index, f.mat, f.smooth))
	
	elif me.edges:
		for e in me.edges:
			fp.write("  e %d %d ;\n" % ( e.v1.index, e.v2.index) )

	if verbosity > 1:
		print "Faces saved"

	#	Vertgroups
	vertgroups = me.getVertGroupNames()
	for g in vertgroups:
		save = True
		n = len(g)
		if g[:5] in ["joint", "helpe"]:
			save = False
		#elif g[n-2:] == "_L":
		#	g1 = g[:n-2] + "_R"
		#elif g[n-2:] == "_R":
		#	g1 = g[:n-2] + "_L"
		else:
			g1 = g
			
		if save:	
			try:
				vgroup = me.getVertsFromGroup(g, True)
				fp.write("VertexGroup %s \n" % g1 )
				for (v, w) in vgroup:
					fp.write("  wv %i %f ;\n" % (v, w) )
				fp.write("end VertexGroup\n")
			except:
				pass
	if verbosity > 1:		
		print "VertexGroups saved"

	# Shape keys
	if not toggleMhxBase:
		exportShapeKeys(fp, me)

	if not toggleGeoOnly:
		writeList(me, meshList, fp, 2)
	fp.write("end mesh\n")
	return # exportMesh

meshList = [
	("string", "activeColorLayer"),
	("int", "activeFace"),
	("string", "activeGroup"),
	("string", "activeUVLayer"),
	("int", "degr"),
	("bool", "faceUV"),
	("bool", "hide"),
	("key", "key"),
	("string", "lib"),
	("xint", "mode"),
	("bool", "multires"),
	("int", ("multires", "multiresDrawLevel")),
	("int", ("multires", "multiresEdgeLevel")),
	("int", ("multires", "multiresPinLevel")),
	# ("int", ("multires", "multiresRenderLevel")),
	# ("string", "renderColorLayer"),
	("string", "renderUVLayer"),
	("tuple2ints", "subDivLevels"),
	("mesh", "texMesh"),
	("bool", "vertexColors"),
	("bool", "vertexUV")
]

#
#	exportShapeKeys(fp, me)
#

def exportShapeKeys(fp, me):	
	if me.key:
		if me.key.relative == False:
			Draw.Pupmenu("Keys should be relative")
		blocks = me.key.blocks
		for b in blocks:
			fp.write("ShapeKey %s Sym \n" % b.name)
			for (n,v) in enumerate(b.data):
				dv = v - me.verts[n].co
				if dv.length > Epsilon:
					fp.write("  sv %d %f %f %f ;\n" %(n, dv[0], dv[1], dv[2]))
			fp.write("    end shapekey\n")
		if not toggleMhxBase:
			exportIpo(me.key.ipo, fp, True)

#
#	exportArmature(ob, fp):
#

def exportArmature(ob, fp):
	amt = ob.getData()
	amtName = amt.name.replace(' ','_')
	obName = ob.name.replace(' ','_')
	
	if verbosity > 0:
		print "Saving amt "+amtName

	bones = amt.bones.values()
	fp.write("armature %s %s \n" % (amtName, obName))
	for b in bones:
		if b.parent == None:
			exportBone(fp, 2, b)
			fp.write("\n")
	if not toggleGeoOnly:
		writeList(amt, armatureList, fp, 2)
	fp.write("end armature\n")

	fp.write("pose %s \n" % (obName))	
	pose = ob.getPose()
	pbones = pose.bones.values()
	for pb in pbones:
		exportPoseBone(fp, pb)
	fp.write("end pose\n")
		
	return # exportArmature
			
armatureList = [
	("bool", "autoIK"),
	("bool", "delayDeform"),
	("bool", "drawAxes"),
	("bool", "drawNames"),
	("xint", "drawType"),
	("bool", "envelopes"),
	("bool", "ghost"),
	#("int", "ghostStep"),
	("xint", "layerMask"),
	("string", "lib"),
	("bool", "mirrorEdit"),
	("bool", "restPosition"),
	("bool", "vertexGroups")
]

#
#	indent(fp, n):
#

def indent(fp, n):
	for i in range(n):
		fp.write("  ")

#
#	exportBone(fp, n, bone):
#

boneOptions = dict ({\
	Armature.CONNECTED : 0x001,
	Armature.HINGE : 0x002,
	Armature.NO_DEFORM : 0x004,
	Armature.MULTIPLY : 0x008,
	Armature.HIDDEN_EDIT : 0x010,
	Armature.ROOT_SELECTED : 0x020,
	Armature.BONE_SELECTED : 0x040,
	Armature.TIP_SELECTED : 0x080,
	Armature.LOCKED_EDIT : 0x100 \
})

def exportBone(fp, n, bone):
	flags = 0
	for key in bone.options:		
		flags |= boneOptions[key]
	parent = getObject(bone.parent)
	fp.write("  bone %s %s %x %x \n" % (bone.name.replace(' ','_'), parent,\
		flags, bone.layerMask))
	head = bone.head['ARMATURESPACE']
	fp.write("    head %6.3f %6.3f %6.3f ;\n" % (head[0], head[1], head[2]))
	tail = bone.tail['ARMATURESPACE']
	fp.write("    tail %6.3f %6.3f %6.3f ;\n" % (tail[0], tail[1], tail[2]))
	if not toggleGeoOnly:
		writeList(bone, editboneList, fp, n+2)
	fp.write("  end bone\n\n")
	
	if bone.children:
		for child in bone.children:
			exportBone(fp, n+1, child)
	return

editboneList = [
	("float", "deformDist"),
	("float", "headRadius"),
	#("float", "length"),
	("float", "roll"),
	("int", "subdivision"),
	("float", "tailRadius"),
	("float", "weight")
]


#
#	exportPoseBone(fp, pb):
#

def exportPoseBone(fp, pb):
	flags = pb.limitX | ( pb.limitY << 1) | (pb.limitZ << 2)
	flags |= (pb.lockXRot <<3) | (pb.lockYRot <<4) | (pb.lockZRot <<5)
	fp.write("\n  posebone %s %x \n" % (pb.name.replace(' ', '_'), flags))
	if not toggleGeoOnly:
		writeList(pb, poseboneList, fp, 2)	
	for cns in pb.constraints:
		exportConstraint(cns, fp)
	fp.write("  end posebone\n")
	return

poseboneList = [
	("object", "displayObject"),
	("tuple3floats", "limitmax"),
	("tuple3floats", "limitmin"),
	("vector", "size"),
	("float", "stiffX"),
	("float", "stiffY"),
	("float", "stiffZ"),
	("float", "stretch")
]

#
#	writeTypedValue(arg, n, fp):
#

def writeTypedValue(arg, n, fp):
	indent(fp,n)
	if type(arg) == list:
		fp.write("list %d " % len(arg))
		for elt in arg:
			writeTypedValue(elt, 0, fp)
	elif type(arg) == int:
		fp.write("hex %x " % arg)
	elif type(arg) == bool:
		if arg:
			fp.write("bool true ")
		else:
			fp.write("bool false ")
	elif type(arg) == float:
		fp.write("float %f " % arg)
	elif type(arg) == str:
		fp.write("str %s " % arg.replace(' ','_'))
	elif type(arg) == Types.vectorType:
		fp.write("vec %f %f %f " % (arg[0], arg[1], arg[2]))
	elif type(arg) == Types.ObjectType:
		fp.write("obj %s " % (arg.name.replace(' ','_')))
	elif type(arg) == Types.IpoType:
		fp.write("ipo %s " % (arg.name.replace(' ','_')))
	elif type(arg) == Types.ActionType:
		fp.write("act %s " % (arg.name.replace(' ','_')))
	elif type(arg) == Types.TextureType:
		fp.write("tex %s " % (arg.name.replace(' ','_')))
	elif type(arg) == Types.TextType:
		fp.write("text foo ")		
		#fp.write("text %s " % (arg.name.replace(' ','_')))
	else:
		raise NameError("Unknown type "+str(type(arg)))

#
#	exportConstraint(cns, fp):
#

def constraintTypeOK(type):
	if type == 'PYTHON' or\
		type == 'CHILDOF':
		return False
	return True

def exportConstraint(cns, fp):
	for (typeName, type) in Constraint.Type.items():
		if cns.type == type and constraintTypeOK(type):
			fp.write("    constraint %s %s %f\n" % (typeName, cns.name.replace(' ','_'), cns.influence))
			for (key,idx) in Constraint.Settings.items():
				try:
					val = cns[idx]
				except:
					val = None
				if val and key != 'PROPERTIES':
					fp.write("    %s " % key)
					writeTypedValue(val, 3, fp)
					fp.write(";\n")
			fp.write("    end constraint\n")
	return
		
			
#
#	exportModifier(mod, fp):
#

def modifierTypeOK(type):
	if type == 'PARTICLESYSTEM':
		return False
	else:
		return True

def exportModifier(mod, fp):
	for (name, type) in Modifier.Type.items():
		if mod.type == type and modifierTypeOK(name):
			fp.write("  modifier %s\n" % name)
			for (key,idx) in Modifier.Settings.items():
				try:
					val = mod[idx]
				except:
					val = None
				if val:
					fp.write("    %s " % key)
					writeTypedValue(val, 2, fp)
					fp.write(";\n")
			fp.write("  end modifier\n")
	return

#
#	exportLattice(ob,fp):
#

def exportLattice(ob,fp):
	lat = ob.getData()
	fp.write("lattice %s \n" % lat.name.replace(' ', '_'))
	fp.write("  partitions %d %d %d ;\n" % (lat.width, lat.height, lat.depth))
	fp.write("  keytypes %s %s %s ;\n" % (lat.widthType, lat.heightType, lat.depthType))
	writeList(lat, latticeList, fp, 2)
	fp.write("end lattice\n")

latticeList = [
	("string", "lib"),
	("xint", "mode")
]

#
#	exportLamp(ob,fp):
#

lampTypes = ['Lamp', 'Sun', 'Spot', 'Hemi', 'Area', 'Photon']

def exportLamp(ob,fp):
	la = ob.getData()
	type = lampTypes[la.type]
	fp.write("lamp %s %s\n" % (type, la.name.replace(' ', '_')))

	if la.textures:
		for (n,tx) in enumerate(la.textures):
			if tx:
				fp.write("  texture %d %s\n" % tx)
	#if la.ipo:
	#	exportIpo(la.ipo, fp, True)

	writeList(la, lampList, fp, 2)
	fp.write("end lamp\n")


lampList = [
	("float", "B"),
	("float", "G"),
	("float", "R"),
	("float", "areaSizeX"),
	("float", "areaSizeY"),
	("float", "bias"),
	("int", "bufferSize"),
	("int", "bufferType"),
	("float", "clipEnd"),
	("float", "clipStart"),
	("tuple3floats", "col"),
	("float", "dist"),
	("float", "energy"),
	("int", "falloffType"),
	("float", "haloint"),
	("int", "haloStep"),
	("ipo", "ipo"),
	("string", "lib"),
	("int", "mode"),
	("float", "quad1"),
	("float", "quad2"),
	("int", "raySamplesX"),
	("int", "raySamplesY"),
	("int", "sampleBuffers"),
	("int", "samples"),
	("float", "softness"),
	("float", "spotBlend"),
	("float", "spotSize")
]

#
#	exportCamera(ob,fp):
#

def exportCamera(ob,fp):
	ca = ob.getData()
	fp.write("camera %s %s\n" % (ca.type, ca.name.replace(' ', '_')))
	#if ca.ipo:
	#	exportIpo(ca.ipo, fp, True)
	writeList(ca, cameraList, fp, 2)
	fp.write("end camera\n")
 
cameraList = [
	("float", "alpha"),
	("float", "angle"),
	("float", "clipEnd"),
	("float", "clipStart"),
	("float", "dofDist"),
	("bool", "drawLimits"),
	("bool", "drawMist"),
	("bool", "drawName"),
	("bool", "drawPassepartout"),
	("float", "drawSize"),
	("bool", "drawTileSafe"),
	("ipo", "ipo"),
	("float", "lens"),
	("string", "lib"),
	("xint", "mode"),
	("float", "scale"),
	("float", "shiftX"),
	("float", "shiftY")
]

#
#	exportCurve(ob,fp):
#

def exportCurve(ob,fp):
	cu = ob.getData()
	fp.write("curve %s \n" % cu.name.replace(' ', '_') )

	for nurb in cu:
		if nurb.type == 0:	# Poly
			fp.write("  nurb poly  \n")
			for pt in nurb:
				fp.write("    pt %f %f %f %f %f ;\n" %( pt[0], pt[1], pt[2], pt[3], pt[4] ))
			fp.write("  end nurb\n")
		elif nurb.type == 1:	# Bezier
			fp.write("  nurb bezier \n")
			for bz in nurb:
				[h1, p, h2] = bz.vec
				fp.write("    pt %f %f %f  %f %f %f  %f %f %f  ;\n" % \
					(h1[0], h1[1], h1[2], p[0], p[1], p[2], h2[0], h2[1], h2[2]))
			fp.write("  end nurb\n")
		elif nurb.type == 4:	# Nurbs
			fp.write("  nurb nurbs \n")
			for pt in nurb:
				fp.write("    pt %f %f %f %f %f ;\n" %( pt[0], pt[1], pt[2], pt[3], pt[4] ))
			fp.write("  end nurb\n")

	for mat in cu.materials:
		fp.write("  material %s\n" % mat)

	writeList(cu, curveList, fp, 2)
	fp.write("end curve\n")

curveList = [
	("object", "bevob"),
	("int", "bevresol"),
	("float", "ext1"),
	("float", "ext2"),
	("xint", "flag"),
	("key", "key"),
	("tuple3floats", "loc"),
	("int", "pathlen"),
	("int", "resolu"),
	("int", "resolv"),
	("tuple3floats", "rot"),
	("tuple3floats", "size"),
	("object", "taperob"),
	("float", "width")
]

#
#	exportText(ob, fp)
#

def exportText(ob,fp):
	te = ob.getData()
	fp.write("text %s \n" % (te.name.replace(' ', '_')))
	line = te.getText()
	fp.write('    line "%s" ;\n' % line)
	writeList(te, textList, fp, 2)
	fp.write("end text\n")

textList = [
	("int", "activeFrame"),
	("float", "frameHeight"),
	("float", "frameWidth"),
	("float", "frameX"),
	("float", "frameY"),
	("string", "lib")
]

#
#	exportGroup(grp, fp):
#

def exportGroup(grp, fp):
	fp.write("group %s\n" % grp.name)
	for ob in grp.objects:
		fp.write("  object %s ;\n" % ob.name.replace(' ','_'))
	if not toggleGeoOnly:
		writeList(grp, groupList, fp, 2)
	fp.write("end group\n")
	return

groupList = [
	("vector", "dupliOffset"),
	("xint", "layers"),
	("string", "lib") 
]

#
#
#

def exportKey(key, fp):
	fp.write("key %s\n" % key.name)
	for b in key.blocks:
		exportKeyBlock(b, fp)
	if key.ipo:
		exportIpo(key.ipo, fp, True)
	writeList(key, keyList, fp, 2)
	fp.write("end key\n")
	return

keyList = [
	("bool", "relative"),
	("xint", "type"),
	("float", "value")
]

def exportKeyBlock(block, fp):
	fp.write("  block %s\n", block.name)
	fp.write("end block\n")
	return



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
	global toggleMhxBase, toggleGeoOnly, MHDir
	if evt == 1:
		toggleMhxBase = 1 - toggleMhxBase
		if toggleMhxBase:
			toggleGeoOnly = 1
	elif evt == 2:
		toggleGeoOnly = 1 - toggleGeoOnly
		if not toggleGeoOnly:
			toggleMhxBase = 0
	elif evt == 7:
		if toggleMhxBase:
			writeMhxBases()
			Draw.Exit()
			return
		else:
			Blender.Window.FileSelector (writeMhxFile, 'SAVE MHX FILE')
	elif evt == 8:
		Draw.Exit()
		return
	if evt == 9:
		MHDir = Draw.PupStrInput("", MHDir, 100)
	Draw.Redraw(-1)

def gui():
	BGL.glClearColor(1,1,0,1)
	BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
	BGL.glColor3f(0,0,0)

	BGL.glRasterPos2i(10,170)
	Draw.Text("MHX (MakeHuman eXchange format) exporter for Blender", "large")
	BGL.glRasterPos2i(10,150)
	Draw.Text("Version %d.%d" % (MAJOR_VERSION, MINOR_VERSION), "normal")
	Draw.Toggle("Mhxbase", 1, 10, 110, 90, 20, toggleMhxBase)
	Draw.Toggle("Only geo", 2, 110, 110, 90, 20, toggleGeoOnly)
	Draw.PushButton("Export MHX file", 7, 10, 10, 150, 40)
	Draw.PushButton("Cancel", 8, 210, 10, 90, 20)
	Draw.PushButton("MH directory", 9, 210, 40, 90, 20) 
	done = 0

Draw.Register(gui, event, button_event) 
