""" 
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyright(c):**	  MakeHuman Team 2001-2010

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
Utility for making clothes to MH characters.

Used to be called defineProxy.py, because a proxy is just a full-body
dress. Below the word clothes refers both to proxies, make-deform
cages, and proper clothes.

Import a MH character *with the joint diamonds present*. In the MHX
importer the Diamonds option must be selected; the OBJ file is
probably useless, because I think that the diamonds have been filtered
out.

Model your clothes over the reference character. It does not really
matter which character you use as reference, but the final result will
probably look better on characters which do not deviate too much from
the reference. The clothing may optionally be UV-unwrapped.

Both the clothes and the character must be given vertex groups with
the same names. If the character has been brought into Blender with
the mhx importer, it is a good idea to first delete all bone groups.
Each clothing vertex must belong to a single group (more precisely,
any additional group is ignored), whereas character verts can belong
to several groups. The character mesh, but not the clothes, should
also be triangulated (Ctrl-T in Edit mode) for best results.

The algorithm assigns each clothing vertex to the "best" triangle in
the character mesh. The face number and the verts barycentric
coordinates (a weighted sum of the corner coordinates) are stored in
the mhclo file. The best triangle is charactized by a small distance
between the vert and face, and that the projection onto the
face falls within the face (all weights lie between 0 and 1), or
almost so. The normal distance between the vertex and the face is
also recorded.

Finding the best face for each vertex is sometimes difficult in
regions where separate parts of the character mesh are very close or
overlap. The mouth area is especially tricky, for proxy meshes with
articulate tongue, teeth, and inner mouth wall. For trousers it can be
difficult to distinguish between the groin area and the left and right
inner thighs. You can help the script distinguish between different
body parts by assigning vertex groups. The algorithm only looks for
the best triangle within the given vertex group.

At the very least the mesh should be divided into a Left, Right and
Mid (with x = 0) group. Joint diamonds should not be assigned to any
group at all, to ensure that the clothing does not follow the
diamonds.

Vertex groups can also be used to prune the search tree and speed
up the program. 

-------

Access this script from the UI panel (N-key).

Assign vertex groups to the main character and to all clothes or
proxies. The name of the vertex groups must match exactly.

Select all clothes or proxies that you want to export, then select the
character to make it active.

Press the Make clothes button.

A separate .mhclo file for each piece of clothing will now be created
in the specified directory.

The file proxy.cfg defines which clothes will be exported with the
character. This file is located in the MakeHuman's main program
directory, but MH will first look for this files in the ~/makehuman/
and C:/ folders. In this way you can keep your own private version of
proxy.cfg. The syntax is described in the beginning of the file.

"""
bl_addon_info = {
    "name": "Make clothes to MakeHuman",
    "author": "Thomas Larsson",
    "version": 0.2,
    "blender": (2, 5, 4),
    "api": 31913,
    "location": "View3D > Properties > Make MH clothes",
    "description": "Make clothes for MakeHuman characters",
    "warning": "",
    "category": "3D View"}


import bpy, os, mathutils

threshold = -0.2
mListLength = 2


#
#	printMverts(stuff, mverts):
#

def printMverts(stuff, mverts):
	for n in range(mListLength):
		(v,dist) = mverts[n]
		if v:
			print(stuff, v.index, dist)

#
#	selectVert(context, vn, ob):
#

def selectVert(context, vn, ob):
	context.scene.objects.active = ob
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.select_all(action='DESELECT')
	bpy.ops.object.mode_set(mode='OBJECT')
	ob.data.vertices[vn].select = True
	return	

#
#	findClothes(context, bob, pob, log):
#

def findClothes(context, bob, pob, log):
	base = bob.data
	proxy = pob.data
	
	bestVerts = []
	for pv in proxy.vertices:
		try:
			pindex = pv.groups[0].group
		except:
			pindex = -1
		if pindex < 0:
			vn = pv.index
			selectVert(context, vn, pob)
			raise NameError("Clothes vert %d not member of any group" % vn)

		name = pob.vertex_groups[pindex].name
		bindex = None
		for bvg in bob.vertex_groups:
			if bvg.name == name:
				bindex = bvg.index
		if bindex == None:
			raise NameError("Did not find vertex group %s in base mesh" % name)

		mverts = []
		for n in range(mListLength):
			mverts.append((None, 1e6))

		for bv in base.vertices:
			for grp in bv.groups:
				if grp.group == bindex:
					vec = pv.co - bv.co
					n = 0
					for (mv,mdist) in mverts:
						if vec.length < mdist:
							for k in range(n+1, mListLength):
								j = mListLength-k+n
								mverts[j] = mverts[j-1]
							mverts[n] = (bv, vec.length)
							#print(bv.index)
							#printMverts(bv.index, mverts)
							break
						n += 1

		(mv, mindist) = mverts[0]
		if mv:
			print(pv.index, mv.index, mindist, name, pindex, bindex)
			log.write("%d %d %.5f %s %d %d\n" % (pv.index, mv.index, mindist, name, pindex, bindex))
			#printMverts("  ", mverts)
		else:
			raise NameError("Failed to find vert %d in group %s %d %d" % (pv.index, name, pindex, bindex))
		if mindist > 5:
			raise NameError("Minimal distance %f > 5.0. Check base and proxy scales." % mindist)

		bestVerts.append((pv, mverts, []))

	print("Setting up face table")
	vfaces = {}
	for f in base.faces:
		for v in f.vertices:
			try:
				vfaces[v].append(f)
			except:
				vfaces[v] = [f]
	
	print("Finding weights")
	for (pv, mverts, fcs) in bestVerts:
		print(pv.index)
		for (bv,mdist) in mverts:
			if bv:
				for f in vfaces[bv.index]:
					verts = []
					for v in f.vertices:
						verts.append(base.vertices[v].co)
					wts = cornerWeights(pv, verts, pob)
					fcs.append((f.vertices, wts))

	print("Finding best weights")
	alwaysOutside = context.scene['MakeClothesOutside']
	bestFaces = []
	for (pv, mverts, fcs) in bestVerts:
		#print(pv.index)
		minmax = -1e6
		for (fverts, wts) in fcs:
			w = minWeight(wts)
			if w > minmax:
				minmax = w
				bWts = wts
				bVerts = fverts
		if minmax < threshold:
			(mv, mdist) = mverts[0]
			bVerts = [mv.index,0,1]
			bWts = [1,0,0]

		v0 = base.vertices[bVerts[0]]
		v1 = base.vertices[bVerts[1]]
		v2 = base.vertices[bVerts[2]]

		est = bWts[0]*v0.co + bWts[1]*v1.co + bWts[2]*v2.co
		norm = bWts[0]*v0.normal + bWts[1]*v1.normal + bWts[2]*v2.normal
		diff = pv.co - est
		proj = diff.dot(norm)
		if proj < 0 and alwaysOutside:
			proj = -proj
		bestFaces.append((pv, bVerts, bWts, proj))	
				
	print("Done")
	return bestFaces

#
#	minWeight(wts)
#

def minWeight(wts):
	best = 1e6
	for w in wts:
		if w < best:
			best = w
	return best

#
#	cornerWeights(pv, verts, pob):
#
#	px = w0*x0 + w1*x1 + w2*x2
#	py = w0*y0 + w1*y1 + w2*y2
#	pz = w0*z0 + w1*z1 + w2*z2
#
#	w2 = 1-w0-w1
#
#	w0*(x0-x2) + w1*(x1-x2) = px-x2
#	w0*(y0-y2) + w1*(y1-y2) = py-y2
#
#	a00*w0 + a01*w1 = b0
#	a10*w0 + a11*w1 = b1
#
#	det = a00*a11 - a01*a10
#
#	det*w0 = a11*b0 - a01*b1
#	det*w1 = -a10*b0 + a00*b1
#

def cornerWeights(pv, verts, pob):
	r0 = verts[0]
	r1 = verts[1]
	r2 = verts[2]

	u01 = r1-r0
	u02 = r2-r0
	n = u01.cross(u02)
	n.normalize()

	u = pv.co-r0
	r = r0 + u - n*u.dot(n)

	'''
	print(list(pv))
	print(" r  ", list(r))
	print(" r0 ", list(r0))
	print(" r1 ", list(r1))
	print(" r2 ", list(r2))
	print(" n  ", list(n))
	'''

	a00 = r0[0]-r2[0]
	a01 = r1[0]-r2[0]
	a10 = r0[1]-r2[1]
	a11 = r1[1]-r2[1]
	b0 = r[0]-r2[0]
	b1 = r[1]-r2[1]
	
	det = a00*a11 - a01*a10
	if abs(det) < 1e-20:
		print("Clothes vert %d mapped to degenerate triangle (det = %g) with corners" % (pv.index, det))
		print("r0", r0[0], r0[1], r0[2])
		print("r1", r1[0], r1[1], r1[2])
		print("r2", r2[0], r2[1], r2[2])
		highlight(pv, pob)
		raise NameError("Singular matrix in cornerWeights")

	w0 = (a11*b0 - a01*b1)/det
	w1 = (-a10*b0 + a00*b1)/det
	
	return (w0, w1, 1-w0-w1)

#
#	highlight(pv, ob):
#

def highlight(pv, ob):
	me = ob.data
	for v in me.vertices:
		v.select = False
	pv.select = True
	return
	
#
#	proxyFilePtr(name):
#

def proxyFilePtr(name):
	for path in ['~/makehuman/', '/']:
		path1 = os.path.expanduser(path+name)
		fileName = os.path.realpath(path1)
		try:
			fp = open(fileName, "r")
			print("Using header file %s" % fileName)
			return fp
		except:
			print("No file %s" % fileName)
	return None

#
#	printClothes(path, pob, data):	
#
		
def printClothes(path, pob, data):
	file = os.path.expanduser(path)
	fp= open(file, "w")

	infp = proxyFilePtr('proxy_header.txt')
	if infp:
		for line in infp:
			fp.write('# '+line)
	else:
		fp.write(
"# author Unknown\n" +
"# license GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)\n" +
"# homepage http://www.makehuman.org/\n")

	fp.write("# name %s\n" % pob.name)
	me = pob.data

	if me.materials:
		mat = me.materials[0]
		fp.write("# material %s\n" % mat.name)
		writeColor(fp, 'diffuse_color', mat.diffuse_color)
		fp.write('diffuse_shader %s\n' % mat.diffuse_shader)
		fp.write('diffuse_intensity %.4f\n' % mat.diffuse_intensity)
		writeColor(fp, 'specular_color', mat.specular_color)
		fp.write('specular_shader %s\n' % mat.specular_shader)
		fp.write('specular_intensity %.4f\n' % mat.specular_intensity)

	fp.write("# verts\n")
	for (pv, verts, wts, proj) in data:
		#print(pv.index,verts,wts)
		fp.write("%5d %5d %5d %.5f %.5f %.5f %.5f\n" % (
			verts[0], verts[1], verts[2], wts[0], wts[1], wts[2], proj))

	fp.write("# obj_data\n")
	if me.uv_textures:
		uvtex = me.uv_textures[0]
		#fp.write("# texverts\n")
		fn = 0
		for uvdata in uvtex.data.values():
			uv = uvdata.uv_raw
			f = me.faces[fn]
			for n in range(len(f.vertices)):
				fp.write("vt %.4f %.4f\n" % (uv[2*n], uv[2*n+1]))

	#fp.write("# faces\n")

	if me.uv_textures:
		n = 1
		for f in me.faces:
			fp.write("f ")
			for v in f.vertices:
				fp.write("%d/%d " % (v+1, n))
				n += 1
			fp.write("\n")
	else:
		for f in me.faces:
			fp.write("f ")
			for v in f.vertices:
				fp.write("%d " % (v+1))
			fp.write("\n")

	fp.write('\n')
	fp.close()
	return

def writeColor(fp, string, color):
	fp.write("%s %.4f %.4f %.4f\n" % (string, color[0], color[1], color[2]))

#
#	makeClothes(context):
#

def makeClothes(context):
	bob = context.object
	for pob in context.selected_objects:
		if pob.type == 'MESH' and bob.type == 'MESH' and pob != bob:
			outpath = '%s/%s.mhclo' % (context.scene['MakeClothesDirectory'], pob.name.lower())
			outfile = os.path.realpath(os.path.expanduser(outpath))
			print("Creating clothes file %s" % outfile)
			logpath = '%s/clothes.log' % context.scene['MakeClothesDirectory']
			logfile = os.path.realpath(os.path.expanduser(logpath))
			log = open(logfile, "w")
			data = findClothes(context, bob, pob, log)
			log.close()
			printClothes(outpath, pob, data)
			print("%s done" % outpath)
		

###################################################################################	
#	User interface
#
#	initInterface()
#

from bpy.props import *

def initInterface(scn):
	bpy.types.Scene.MakeClothesDirectory = StringProperty(
		name="Directory", 
		description="Directory", 
		maxlen=1024)
	scn['MakeClothesDirectory'] = "~/makehuman"

	bpy.types.Scene.MakeClothesOutside = BoolProperty(
		name="Always outside", 
		description="Invert projection if negative")
	scn['MakeClothesOutside'] = True

	return

initInterface(bpy.context.scene)

#
#	class MakeClothesPanel(bpy.types.Panel):
#

class MakeClothesPanel(bpy.types.Panel):
	bl_label = "Make clothes"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	@classmethod
	def poll(cls, context):
		return (context.object and context.object.type == 'MESH')

	def draw(self, context):
		layout = self.layout
		layout.operator("object.InitInterfaceButton")
		layout.prop(context.scene, "MakeClothesDirectory")
		layout.prop(context.scene, "MakeClothesOutside")
		layout.operator("object.MakeClothesButton")
		return

#
#	class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
#

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_InitInterfaceButton"
	bl_label = "Initialize"

	def execute(self, context):
		import bpy
		initInterface(context.scene)
		print("Interface initialized")
		return{'FINISHED'}	

#
#	class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
#

class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_MakeClothesButton"
	bl_label = "Make clothes"

	def execute(self, context):
		import bpy, mathutils
		makeClothes(context)
		return{'FINISHED'}	


