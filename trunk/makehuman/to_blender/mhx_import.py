#!BPY
""" 
Name: 'Makehuman (.mhx)'
Blender: 249
Group: 'Import'
Tooltip: 'Import from MakeHuman eXchange format (.mhx)'
"""

__author__= ['Thomas Larsson']
__url__ = ("www.makehuman.org")
__version__= '0.1'
__bpydoc__= '''\
MHX importer
0.1 First version
'''
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
MHX (MakeHuman eXchange format) importer for Blender.

TO DO

"""

import Blender
from Blender import *
from Blender.Constraint import *
from Blender.Mathutils import *
import os
import bpy

MAJOR_VERSION = 0
MINOR_VERSION = 1

#
#	Bone flags
#

F_CON = 0x01
F_NODEF = 0x02

#
#	Texture channels
#

T_COLOR	= 0x01
T_REF	= 0x02
T_ALPHA	= 0x04
T_MIX	= 0x08

#
#	Button flags
#

toggleArmIK = 0
toggleLegIK = 0
toggleFingerIK = 0
toggleDispObs = 1
toggleRot90 = 0
toggleShape = 0

#
#	Global variables
#

verts_loc = []
verts_tex = []
edges = []
faces = []
tex_faces = []
vertgroups = []
shapekeys = []
joints = []
materials = []

layer1 = 0x001		# Bit 1-10
layer2 = 0x000		# Bit 11-20

drawType = Object.DrawTypes.SOLID


#
#	readMhxFile(fileName):
#

def readMhxFile(fileName):
	global verts_loc, verts_tex, edges, faces, tex_faces, vertgroups, shapekeys
	global layer1, layer2, drawType
	global TexDir
	
	line_nr = 0
	mat_nr = -1
	first = 1
	ignore = False
	obType = "None"
	mainMesh = False

	file= open(fileName, "rU")
	for line in file: 
		line_nr = line_nr + 1
		line_split= line.split()

		if (len(line_split) == 0):
			pass
		elif (line_split[0] == '#'):
			pass

		elif (line_split[0] == "MHX"):
			if first:
				if (int(line_split[1]) != MAJOR_VERSION or int(line_split[2]) != MINOR_VERSION):
					Draw.PupMenu("Warning: \nThis file was created with another version of MHX\n")
				first = 0
				
		elif (line_split[0] == 'object'):
			# Create previous object
			if (obType == "Mesh"):
				meshOb = addMesh(meshName)
			elif (obType == "Rig"):
				rigOb = addRig(rigName, bones, constraints, meshOb)
			# Start new object
			objName = line_split[1]
			layer1 = int(line_split[2])
			layer2 = int(line_split[3])
			ignore = False
			obType = "None"
			if (line_split[4] == "keep"):
				scn = Scene.GetCurrent()
				for ob in scn.objects:
					if (ob.name == objName):
						print "Ignoring "+ob.name
						ignore = True
				drawType = Object.DrawTypes.WIRE
				mainMesh = False
			else:
				drawType = Object.DrawTypes.SOLID
				mainMesh = True

			print "object", objName

		elif (ignore):
			pass
		
		elif (line_split[0] == 'v'):
			if toggleRot90 and mainMesh:
				verts_loc.append( (float(line_split[1]), -float(line_split[3]), float(line_split[2])) )
			else:
				verts_loc.append( (float(line_split[1]), float(line_split[2]), float(line_split[3])) )
			
		elif (line_split[0] == 'vn'):
			pass
		
		elif (line_split[0] == 'vt'):
			verts_tex.append( (float(line_split[1]), float(line_split[2])) ) 

		elif (line_split[0] == 'wv'):
			verts_group.append( (int(line_split[1]), float(line_split[2])) ) 

		elif (line_split[0] == 'sv'):
			if (toggleShape == 0):
				pass
			elif toggleRot90 and mainMesh:
				verts_key.append( (int(line_split[1]), float(line_split[2]), -float(line_split[4]), float(line_split[3])) )
			else:
				verts_key.append( (int(line_split[1]), float(line_split[2]), float(line_split[3]), float(line_split[4])) )

		elif (line_split[0] == 'e'):
			edges.append((int(line_split[1]), int(line_split[2])))

		elif (line_split[0] == 'f'):
			line_split= line[2:].split()
			face_vert_loc_indices= []
			face_vert_tex_indices= []
							
			for v in line_split:
				obj_vert= v.split('/')
				face_vert_loc_indices.append( int(obj_vert[0]) )
				if len(obj_vert)>1 and obj_vert[1]:
					face_vert_tex_indices.append( int(obj_vert[1]) )

			faces.append( face_vert_loc_indices );
			if (face_vert_tex_indices != []):
				tex_faces.append( face_vert_tex_indices );
			
		elif (line_split[0] == 'j'):
			if toggleRot90:
				offset = Vector( float(line_split[4]), -float(line_split[6]), float(line_split[5]) )
			else:
				offset = Vector( float(line_split[4]), float(line_split[5]), float(line_split[6]) )
			joints.append( (int(line_split[1]), line_split[2], int(line_split[3]), offset) ) 

		elif (line_split[0] == 'vertgroup'):
			verts_group = []
			vertgroups.append( (line_split[1], verts_group) )
		
		elif (line_split[0] == 'shapekey'):
			if (toggleShape):
				verts_key = []
				shapekeys.append( (line_split[1], float(line_split[2]), float(line_split[3]), line_split[4], verts_key) )
		
		elif (line_split[0] == 'mesh'):
			if first:
					Draw.PupMenu("Warning: obsolete MHX file")
					first = 0
			meshName = line_split[1]
			obType = "Mesh"
			print "mesh", meshName
		
		elif (line_split[0] == 'armature'):
			rigName = line_split[1]
			obType = "Rig"
			print "armature", rigName
			bones = []
			constraints = []
			dispObs = []

		elif (line_split[0] == 'bone'):
			head = []
			tail = []
			bone = ( line_split[1], line_split[2], head, tail, float(line_split[3]), int(line_split[4]), int(line_split[5])) 
			bones.append(bone)

		elif (line_split[0] == 'head'):
			if toggleRot90:
				head.append( Vector(float(line_split[1]), -float(line_split[3]), float(line_split[2])) )
			else:
				head.append( Vector(float(line_split[1]), float(line_split[2]), float(line_split[3])) )

		elif (line_split[0] == 'tail'):
			if toggleRot90:
				tail.append( Vector(float(line_split[1]), -float(line_split[3]), float(line_split[2])) )
			else:
				tail.append( Vector(float(line_split[1]), float(line_split[2]), float(line_split[3])) )
				
		elif (line_split[0] == 'dispob'):
			dispObs.append( (line_split[1], line_split[2]) )

		elif (line_split[0] == 'constraint'):
			bone = line_split[1]
			type = line_split[2]
			target = line_split[3]
			driver = line_split[4]
			if (type == "IK"):
				param = [int(line_split[5])]
			elif (type == "CopyRot"):
				param = []
			elif (type == "LimitDist"):
				param = []
			else:
				print "Unknown constraint "+type
			constraint = ( bone, type, target, driver, param )
			constraints.append(constraint)

		elif (line_split[0] == 'material'):
			material = Material.New(line_split[1])
			mat_nr = mat_nr + 1
			text_nr = 0
			materials.append(material)
			
		elif (line_split[0] == 'color'):
			material.rgbCol = [ float(line_split[1]),  float(line_split[2]),  float(line_split[3])]

		elif (line_split[0] == 'alpha'):
			material.setAlpha( float(line_split[1]) )

		elif (line_split[0] == 'specular'):
			pass

		elif (line_split[0] == 'texture'):
			tex = Texture.New( line_split[1] ) 
			tex.setType('Image')           
			imgName = TexDir + line_split[2]
			try: 
				img = Image.Load( imgName) 
				tex.image = img
			except:
				Draw.PupMenu("Warning: Failed to load image " + imgName)

			flags = int(line_split[3])
			mflags = 0
			bflags = 0
			if flags & T_COLOR:
				mflags |= Texture.MapTo.COL
			if flags & T_ALPHA:
				mflags |= Texture.MapTo.ALPHA
			if flags & T_REF:
				mflags |= Texture.MapTo.REF
			if flags & T_MIX:
				pass

			material.setTexture(text_nr, tex, Texture.TexCo.UV, mflags)
			material.specTransp = 0.0
			text_nr += 1
			material.mode |= Material.Modes.ZTRANSP    
		else:
			print( "Unknown tag %s" % ( line_split[0] ))

	file.close()
	if (obType == "Mesh"):
		meshOb = addMesh(meshName)
	elif (obType == "Rig"):
		rigOb = addRig(rigName, bones, constraints, dispObs, meshOb)

	
#
#	addMesh ():
#

def addMesh (meshName):
	global verts_loc, verts_tex, edges, faces, tex_faces, vertgroups, shapekeys
	global layer1, layer2, drawType
	
	print "adding mesh %s" % (meshName)
	editmode = Window.EditMode()   
	if editmode: Window.EditMode(0)
	me = bpy.data.meshes.new(meshName)
	me.verts.extend(verts_loc)   
	if faces:
		me.faces.extend(faces)    
	else:
		print edges
		me.edges.extend(edges)
	scn = bpy.data.scenes.active     # link object to current scene
	meshOb = scn.objects.new(me, meshName)
	meshOb.Layers = (layer2 << 10) | (layer1 & 0x3ff)
	meshOb.drawType = drawType
	meshOb.setMaterials(materials)
	me.materials = materials
	meshOb.activeMaterial = 0

	# Vertgroups
	for (g, vlist) in vertgroups:
#		print "adding vert group %s" % (g)
		me.addVertGroup(g)
		for (v, w) in vlist:
			me.assignVertsToGroup(g, [v], w, Mesh.AssignModes.REPLACE)

	# Shapekeys
	for (name, min, max, vg, keys) in shapekeys:
		print "adding shape key %s %f %f %s" % (name, min, max, vg)
		meshOb.insertShapeKey()
		me.key.relative = True
		block = me.key.blocks[-1]
		block.name = name
		block.slidermax = max
		block.slidermin = min
		if vg != "None":
			block.vgroup = vg
		for (i, x, y, z) in keys:
			block.data[i] += Vector(x,y,z)
			
	# UVs
	if tex_faces != [] and me.faces:
		me.faceUV= 1
		for n,ft in enumerate(tex_faces):
			for i,uv in enumerate(me.faces[n].uv):
				(uv.x, uv.y) = verts_tex[ft[i]]
		
	verts_loc = []
	verts_tex = []
	edges = []
	faces = []
	tex_faces = []
	vertgroups = []
	shapekeys = []
	return meshOb

#
#	addRig (rigName, bones, constraints, dispObs, meshOb)
#

def addRig (rigName, bones, constraints, dispObs, meshOb):
	global layer1, layer2
	
	scn = bpy.data.scenes.active
	scn.objects.selected = []
	
	rigData= bpy.data.armatures.new(rigName)
	rigOb = scn.objects.new(rigData)
	rigOb.Layers = (layer2 << 10) | (layer1 & 0x3ff)
	rigOb.xRay = True
	scn.objects.context = [rigOb]
	scn.objects.active = rigOb
	
	buildRig(rigData, bones)
	constrainRig(rigOb, constraints, dispObs)
#	return rigOb
	
	#
	#	Parent the mesh to the rig.
	#	Have not yet succeeded to apply the armature modifier
	#
	rigOb.makeParentDeform([meshOb])
	mods = meshOb.modifiers
	for mod in mods:
		print mod, mod.name
		if mod.name == "Armature":
			mod[Modifier.Settings.VGROUPS] = true
			mod[Modifier.Settings.ENVELOPES] = false

	return rigOb

#
#	buildRig(rigData, bones):
#

def buildRig(rigData, bones):
	rigData.makeEditable()
	for (name, parName, head, tail, roll, flags, layers) in bones:
		bone = Armature.Editbone()		
		bone.name = name
		rigData.bones[name] = bone
		bone.head = head[0]
		bone.tail = tail[0]
		bone.roll = roll
		bone.layerMask = layers
		if (parName != "None"):
			parent = rigData.bones[parName]
			bone.parent = parent
		if (flags & F_CON):
			bone.options = [Armature.CONNECTED]
		if (flags & F_NODEF):
			bone.options = [Armature.NO_DEFORM]	
	rigData.update()

#
#	Constrain the rig
#
def constrainRig(rigOb, constraints, dispObs):
	pbones = rigOb.getPose().bones
	for (name, type, tarName, driver, param) in constraints:
		pbone = pbones[name]
		if toggleArmIK == 0 and driver == "ArmIK-switch":
			print "Constraint "+name+" ignored."
		elif toggleLegIK == 0 and driver == "LegIK-switch":
			print "Constraint "+name+" ignored."
		elif toggleFingerIK == 0 and driver == "FingerIK-switch":
			print "Constraint "+name+" ignored."
		elif (type == "IK"):
			cns = pbone.constraints.append(Type.IKSOLVER)
			cns[Settings.TARGET] = rigOb
			cns[Settings.BONE] = tarName 
			cns[Settings.CHAINLEN] = param[0]
		elif (type == "CopyRot"):
			cns = pbone.constraints.append(Type.COPYROT)
			cns[Settings.TARGET] = rigOb
			cns[Settings.BONE] = tarName 
		elif (type == "LimitDist"):
			cns = pbone.constraints.append(Type.LIMITDIST)
			cns[Settings.TARGET] = rigOb
			cns[Settings.BONE] = tarName 
			cns[Settings.LIMITMODE] = Settings.LIMIT_INSIDE
		else:
			print "Unknown constraint "+type

	if toggleDispObs:			
		for (bone, obName) in dispObs:
			pbone = pbones[bone]
			obj = Object.Get(obName)
			pbone.displayObject = obj
		
		
		
#		if driver != "None":
#			ipo = addIpo(cns, rigOb, driver)
			
	rigOb.getPose().update()

#
#	addIpo(rigOb, name): 
#	
#
	
def addIpo(rigOb, cns, name): 
	print "Adding ipo for "+name
	ipo = Ipo.New("Constraint", name)
	print ipo
	icu = ipo.addCurve("Inf")
	print icu
	icu[0.0] = 0.0
	icu[1.0] = 1.0
#	icu.append((0.0, 0.0))
#	icu.append((1.0, 1.0))
	icu.extend = IpoCurve.ExtendTypes.CONST
	icu.interpolation = IpoCurve.InterpTypes.LINEAR
	icu.recalc()
	rigOb.setIpo(ipo)
#	icu.driver = 1
	print icu
	print icu.driver
	icu.driverBone = name
	icu.driverChannel = IpoCurve.LOC_X
	return ipo


#
#	main(fileName):
#

done = 0
msg = "This cannot happen"

def main(fileName):
	global done, msg, meshOb, rigOb
	
	n = len(fileName)
	if fileName[n-3:] != "mhx":
		Draw.PupMenu("Error: Not a mhx file: " + fileName)
		return
	
	print "Opening MHX file "+ fileName
	if fileName == None:
		print "What??"
	readMhxFile(fileName)
	msg = "MHX file " + fileName + " imported."
	done = 1

	
#
#	User interface
#

def event(evt, val):   
	global msg
	if done:
		Draw.PupMenu(msg)
		Draw.Exit()               
		return		
	if not val:  # val = 0: it's a key/mbutton release
		if evt in [Draw.LEFTMOUSE, Draw.MIDDLEMOUSE, Draw.RIGHTMOUSE]:
			Draw.Redraw(1)
		return
	if evt == Draw.ESCKEY:
		Draw.Exit()               
		return
	else: 
		return
	Draw.Redraw(1)

def button_event(evt): 
	global toggleArmIK, toggleLegIK, toggleFingerIK, toggleDispObs
	global toggleRot90, toggleShape
	global TexDir
	if evt == 1:
		toggleArmIK = 1 - toggleArmIK
	elif evt == 2:
		toggleLegIK = 1 - toggleLegIK
	elif evt == 3:
		toggleFingerIK = 1 - toggleFingerIK
	elif evt == 4:
		toggleDispObs = 1 - toggleDispObs
	elif evt == 5:
		toggleRot90 = 1 - toggleRot90
	elif evt == 6:
		toggleShape = 1 - toggleShape
	elif evt == 7:
		Blender.Window.FileSelector (main, 'OPEN MHX FILE')
	elif evt == 8:
		Draw.Exit()
		return
	if evt == 9:
		TexDir = Draw.PupStrInput("Texture directory:", TexDir, 100)
	Draw.Redraw(1)

def gui():
	BGL.glClearColor(0,0,1,1)
	BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
	BGL.glColor3f(1,1,1)

	BGL.glRasterPos2i(10,170)
	Draw.Text("MHX (MakeHuman eXchange format) importer for Blender", "large")
	BGL.glRasterPos2i(10,150)
	Draw.Text("Version %d.%d" % (MAJOR_VERSION, MINOR_VERSION), "normal")
	Draw.Toggle("Arm IK", 1, 10, 110, 90, 20, toggleArmIK,"Arm IK")
	Draw.Toggle("Leg IK", 2, 110, 110, 90, 20, toggleLegIK,"Leg IK")
	Draw.Toggle("Finger IK", 3, 210, 110, 90, 20, toggleFingerIK,"Finger IK")
	Draw.Toggle("Display objs", 4, 210, 80, 90, 20, toggleDispObs,"Display objects")
	Draw.Toggle("Rot 90", 5, 110, 80, 90, 20, toggleRot90,"Rotate mesh 90 degrees")
	Draw.Toggle("Shapekeys", 6, 10, 80, 90, 20, toggleShape,"Load shape keys")
	Draw.PushButton("Load MHX file", 7, 10, 10, 150, 40)
	Draw.PushButton("Cancel", 8, 210, 10, 90, 20)
	Draw.PushButton("Texture directory", 9, 210, 40, 90, 20) 

Draw.Register(gui, event, button_event) 

#
#	The variable TexDir points to the directory where you can find the
#	textures. It defaults to the standard place in the Makehuman directory.
#	Change it to fit your configuration
#

TexDir = "/home/thomas/makehuman/data/textures/"