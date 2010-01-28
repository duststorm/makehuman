#!BPY
""" 
Name: 'Makehuman (.mhx)'
Blender: 250
Group: 'Export'
Tooltip: 'Export from MakeHuman eXchange format (.mhx)'
"""

__author__= ['Thomas Larsson']
__url__ = ("www.makehuman.org")
__version__= '0.5'
__bpydoc__= '''\
MHX exporter for Blender 2.5, materials only
Compatible with MHX 0.5
'''
""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyamtht(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
MHX (MakeHuman eXchange format) exporter for Blender.

TO DO

"""

import bpy
import os
import types

MAJOR_VERSION = 0
MINOR_VERSION = 5
Epsilon = 1e-5

#MHDir = "/home/svn/"
MHDir = "/home/thomas/svn/makehuman/"


		
#
#	writeDir(thing, name, xtraskip, pad, fp, globals, locals):
#

def writeDir(thing, name, xtraskip, pad, fp, globals, locals):
	for ext in dir(thing):
		try:
			expr = name+"."+ext
			#print (expr)
			arg = eval(expr, globals, locals)
			success = True
		except:
			success = False
		if success:
			writeValue(ext, arg, xtraskip, pad, fp)
	return

#
#	writeValue(ext, arg, xtraskip, pad, fp):
#

excludeList = [\
	'bl_rna', 'fake_user', 'id_data', 'name', 'rna_type', 'tag', 'type', 'users'
]

def writeValue(ext, arg, xtraskip, pad, fp):
	global todo
	# print("%s %s" % (ext,arg))
	if len(str(arg)) == 0 or\
	   str(arg)[0] == '<' or\
	   ext[0] == '_' or\
	   arg == None or\
	   arg == [] or\
	   ext in excludeList or\
	   ext in xtraskip:
		return

	typ = type(arg)
	typeSplit = str(typ).split("'")
	if typ == int:
		fp.write("%s%s %d ;\n" % (pad, ext, arg))
	elif typ == float:
		fp.write("%s%s %g ;\n" % (pad, ext, arg))
	elif typ == bool:
		fp.write("%s%s %s ;\n" % (pad, ext, arg))
	elif typ == str:
		fp.write("%s%s '%s' ;\n" % (pad, ext, arg.replace(' ','_')))


#
#	writeMhxBases()	
#

def writeMhxBases():
	global done

	fileName = MHDir + "data/3dobjs/materials25.mhx"
	print( "Writing MHX material file " + fileName )
	fp = open(fileName, 'w')
	fp.write(
"# MHX materials for Blender 2.5x \n" +
"MHX %d %d ;\n" % (MAJOR_VERSION, MINOR_VERSION) +
"MHX249 False ; \n")

	for tex in bpy.data.textures:
		exportTexture(tex, fp)

	for mat in bpy.data.materials:
		exportMaterial(mat, fp)
	fp.write("MHX249 True ;\n\n")

	fp.close()
	print( "Material file %s written" % fileName )
	return


#
#	exportMaterial(mat, fp):
#	exportName(name, data, wrapper, fp):	
#	exportColor(name, col, fp):
#	exportRamp(name, ramp, fp):
#	exportHalo(halo, fp)
#	exportSSS(sss, fp)
#	exportMTex(index, mtex, fp):
#	exportTexture(tex, fp)
#	exportFileName(file, fp):
#	exportImage(img, fp):
#
#

MatExclude = ['active_texture', 'diffuse_color', 'diffuse_ramp', 'specular_color', 'specular_ramp', 'mirror_color', 'halo', 'physics',
	'raytrace_mirror', 'raytrace_transparency', 'strand', 'subsurface_scattering', 'textures', 'use_textures', 'volume']

def exportMaterial(mat, fp):
	fp.write("material %s \n" % mat.name.replace(' ', '_'))
	for (n,mtex) in enumerate(mat.textures):
		if mtex:
			exportMTex(n, mtex, mat.use_textures[n], fp)
	exportName("active_texture", mat.active_texture, '_texture', fp)
	exportColor("diffuse_color", mat.diffuse_color, fp)
	exportRamp("diffuse_ramp", mat.diffuse_ramp, fp)
	exportHalo(mat.halo, fp)
	exportColor("specular_color", mat.specular_color, fp)
	exportRamp("specular_ramp", mat.specular_ramp, fp)
	exportColor("mirror_color", mat.mirror_color, fp)
	exportRaytraceMirror(mat.raytrace_mirror, fp)
	exportRaytraceTransparency(mat.raytrace_transparency, fp)
	exportSSS(mat.subsurface_scattering, fp)
	exportVolume(mat.volume, fp)
	writeDir(mat, "mat", MatExclude, "  ", fp, globals(), locals())
	fp.write("end material\n\n")

def exportName(name, data, wrapper, fp):
	if data:
		fp.write("  %s %s('%s') ;\n" % (name, wrapper, data.name))


def exportColor(name, col, fp):
	if col:
		fp.write("  %s (%g,%g,%g) ;\n" % (name, col[0], col[1], col[2]))

def exportRamp(name, ramp, fp):
	if False and ramp and ramp.elements != []:
		fp.write("  colorramp %s\n" % name)
		for elt in ramp.elements:
			v = elt.col
			fp.write("    color %g %g %g %g ;\n" % (v[0], v[1], v[2], v[3]))
			fp.write("    position %g ;\n" % elt.position)
		writeDir(ramp, "ramp", ['elements'], "    ", fp, globals(), locals())
		fp.write("  end colorramp\n")


def exportHalo(halo, fp):
	if False and halo:
		fp.write("  halo\n")
		writeDir(halo, "halo", [], "    ", fp, globals(), locals())
		fp.write("  end halo\n")

def exportRaytraceMirror(rmir, fp):
	if rmir.enabled:
		fp.write("  raytrace_mirror\n")
		writeDir(rmir, "rmir", [], "    ", fp, globals(), locals())
		fp.write("  end raytrace_mirror\n")

def exportRaytraceTransparency(rtra, fp):
	if rtra:
		fp.write("  raytrace_transparency\n")
		writeDir(rtra, "rtra", [], "    ", fp, globals(), locals())
		fp.write("  end raytrace_transparency\n")


def exportSSS(sss, fp):
	if sss.enabled:
		fp.write("  subsurface_scattering\n")
		exportColor("  color", sss.color, fp)
		exportColor("  radius", sss.radius, fp)
		writeDir(sss, "sss", ['color', 'radius'], "    ", fp, globals(), locals())
		fp.write("  end subsurface_scattering\n")

def exportVolume(vol, fp):
	if False and vol:
		fp.write("  volume\n")
		exportColor("  emission_color", vol.emission_color, fp)
		exportColor("  reflection_color", vol.reflection_color, fp)
		exportColor("  transmission_color", vol.transmission_color, fp)
		writeDir(vol, "vol", ['emission_color', 'reflection_color', 'transmission_color'], "    ", fp, globals(), locals())
		fp.write("  end volume\n")

def exportMTex(index, mtex, use, fp):
	tx = mtex.texture
	fp.write("  mtex %d %s %s\n" % (index, tx.name, use))
	exportColor("  color", mtex.color, fp)
	writeDir(mtex, "mtex", ['color', 'texture'], "    ", fp, globals(), locals())
	fp.write("  end mtex\n\n")
	return

def exportTexture(tx, fp):
	print( tx )
	fp.write("\ntexture %s %s\n" % (tx.type, tx.name))
	try:
		exportImage(tx.image, fp)
	except:
		pass
	writeDir(tx, "tx", ['image', 'image_user'], "  ", fp, globals(), locals())
	fp.write("end texture\n")
	return

def exportFileName(file, fp):
	(filepath, filename) = os.path.split(file)
	fp.write("    filename %s ;\n" % (file))
	
def exportImage(img, fp):
	fp.write("  image %s\n" % img.name)
	exportFileName(img.filename, fp)
	if False:
		writeDir(img, "img", ['filename', 'size'], "    ", fp, globals(), locals())
	fp.write("  end image\n")
	return


#
#	Do export
#

writeMhxBases()

