#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyright(c):**	  MakeHuman Team 2001-2010

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
MakeHuman to Collada (MakeHuman eXchange format) exporter. Collada files can be loaded into
Blender by collada_import.py.

TO DO

"""

import module3d
import aljabr
import mh
import files3d
import mh2bvh
import os, time
import mh2proxy
import mhx_rig, rig_body_25, rig_arm_25, rig_finger_25, rig_leg_25, rig_toe_25, rig_face_25, rig_panel_25
from mhx_rig import *
import read_rig

#
#	Size of end bones = 1 mm
#
Delta = [0,0.01,0]

#	Root bone
Root = 'MasterFloor'

#
# ....exportCollada(obj, filename):
#	exportCollada1(obj, filename, proxyData):
#

def exportCollada(obj, name):
	filename = name+".dae"
	print 'Writing Collada file %s' % filename
	fp = open(filename, 'w')
	exportDae(obj, fp)
	fp.close()
	print 'Collada file %s written' % filename
	return

#
#	findInHierarchy(bone, hier):
#

def findInHierarchy(bone, hier):
	if hier == []:
		return []
	for pair in hier:
		(b, children) = pair
		if b == bone:
			return pair
		else:
			b = findInHierarchy(bone, children)
			if b: return b
	return []

#
#	flatten(hier, bones):
#

def flatten(hier, bones):
	for (bone, children) in hier:
		bones.append(bone)
		flatten(children, bones)
	return

#
#	boneOK(flags, bone, parent):
#

reparents = {
	'UpArm_L' 	: 'Clavicle_L',
	'UpArm_R' 	: 'Clavicle_R',
	'UpLeg_L' 	: 'Hip_L',
	'UpLeg_R' 	: 'Hip_R',
	
	'UpArmTwist_L' 	: 'Clavicle_L',
	'UpArmTwist_R' 	: 'Clavicle_R',
	'UpLegTwist_L' 	: 'Hip_L',
	'UpLegTwist_R' 	: 'Hip_R',
}

twistBones = {
	'UpArmTwist_L' 	: 'UpArm_L',
	'UpArmTwist_R' 	: 'UpArm_R',
	'LoArmTwist_L' 	: 'LoArm_L',
	'LoArmTwist_R' 	: 'LoArm_R',
	'UpLegTwist_L' 	: 'UpLeg_L',
	'UpLegTwist_R' 	: 'UpLeg_R',
}

skipBones = [ 'Rib_L', 'Rib_R', 'Stomach_L', 'Stomach_R', 'Scapula_L', 'Scapula_R']

def boneOK(flags, bone, parent):
	if bone == Root:
		return 'None'
	elif bone in twistBones.keys():
		return None
	elif bone in skipBones:
		return None
	elif bone in reparents.keys():
		return reparents[bone]
	elif flags & F_DEF:
		return parent
	elif bone in ['HipsInv']:
		return parent
	return None
	
#
#	readSkinWeights(weights, tmplName):
#
#	VertexGroup Breathe
#	wv 2543 0.148938 ;
#

def readSkinWeights(weights, tmplName):
	tmpl = open(tmplName, "rU")
	if tmpl == None:
		print("Cannot open template "+tmplName)
		return
	for line in tmpl:
		lineSplit= line.split()
		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == 'VertexGroup':
			grp = []
			weights[lineSplit[1]] = grp
		elif lineSplit[0] == 'wv':
			grp.append((lineSplit[1],lineSplit[2]))
	return

def fixTwistWeights(fp, weights):
	for (twist, bone) in twistBones.items():
		wts = weights[twist] + weights[bone]
		wts.sort()
		nwts = []
		n = 1
		weights[bone] = nwts
		while n < len(wts):
			(v0, w0) = wts[n-1]
			(v1, w1) = wts[n]
			if v0 == v1:
				nwts.append((v0, w0+w1))
				n += 2
			else:
				nwts.append((v0, w0))
				n += 1
		fp.write("\n%s\n%s\n%s\n" % (twist, weights[twist], weights[bone]))
	return
				
#
#	writeBones(fp, bones, orig, extra, pad, stuff):
#	writeBone(fp, bone, orig, extra, pad, stuff):
#

def writeBones(fp, bones, orig, extra, pad, stuff):
	for bone in bones:
		writeBone(fp, bone, orig, extra, pad, stuff)
	return
	
def writeBone(fp, bone, orig, extra, pad, stuff):
	(name, children) = bone
	head = stuff.rigHead[name]
	vec = aljabr.vsub(head, orig)
	printNode(fp, name, vec, extra, pad)
	if children:
		writeBones(fp, children, head, '', pad+'  ', stuff)	
	'''
	else:
		tail = stuff.rigTail[name]
		#vec = aljabr.vsub(tail, head)
		vec = Delta
		printNode(fp, name+"_end", vec, '', pad+'  ')
		fp.write('\n%s        </node>' % pad)
	'''
	fp.write('\n%s      </node>' % pad)
	return
	
	
def printNode(fp, name, vec, extra, pad):
	# print(name, vec)
	if name:
		nameStr = 'sid="%s"' % name
		idStr = 'id="%s" name="%s"' % (name, name)
	else:
		nameStr = ''
		idStr = ''
	fp.write('\n'+
'%s      <node %s %s type="JOINT" %s>\n' % (pad, extra, nameStr, idStr) +
'%s        <translate sid="translate"> %.4f %.4f %.4f </translate>\n' % (pad, vec[0], -vec[2], vec[1]) +
'%s        <rotate sid="rotateZ">0 0 1 0.0</rotate>\n' % pad +
'%s        <rotate sid="rotateY">0 1 0 0.0</rotate>\n' % pad +
'%s        <rotate sid="rotateX">1 0 0 0.0</rotate>\n' % pad +
'%s        <scale sid="scale">1.0 1.0 1.0</scale>' % pad)
	


#
#	getArmatureFromMhx(obj):
#

def getArmatureFromMhx(obj):
	mhx_rig.newSetupJoints(obj, 
		rig_body_25.BodyJoints +
		rig_arm_25.ArmJoints +
		rig_finger_25.FingerJoints +
		rig_leg_25.LegJoints +
		rig_toe_25.ToeJoints +
		rig_face_25.FaceJoints,
		
		rig_body_25.BodyHeadsTails +
		rig_arm_25.ArmHeadsTails +
		rig_finger_25.FingerHeadsTails +
		rig_leg_25.LegHeadsTails +
		rig_toe_25.ToeHeadsTails +
		rig_face_25.FaceHeadsTails)
		
	hier = []
	armature = rig_body_25.BodyArmature + rig_arm_25.ArmArmature + rig_finger_25.FingerArmature + rig_leg_25.LegArmature + rig_toe_25.ToeArmature + rig_face_25.FaceArmature

	for (bone, cond, roll, parent, flags, layers, bbone) in armature:
		par = boneOK(flags, bone, parent)
		if par:
			if par == 'None':
				hier.append((bone, []))
			else:
				parHier = findInHierarchy(par, hier)
				try:
					(p, children) = parHier
				except:
					raise NameError("Did not find %s parent %s" % (bone, parent))
				children.append((bone, []))
	#print("hier", rigHier)
	
	bones = []
	flatten(hier, bones)	

	weights = {}
	readSkinWeights(weights, "data/templates/vertexgroups-minimal.mhx")	
	# fixTwistWeights(fp, weights)
	return (mhx_rig.rigHead, mhx_rig.rigTail, hier, bones, weights)

#
#	getArmatureFromRigFile(fileName, obj):	
#

def getArmatureFromRigFile(fileName, obj):	
	(locations, armature, weights) = read_rig.readRigFile(fileName, obj)
	
	hier = []
	heads = {}
	tails = {}
	for (bone, head, tail, roll, parent, options) in armature:
		heads[bone] = head
		tails[bone] = tail
		if parent == '-':
			hier.append((bone, []))
		else:
			parHier = findInHierarchy(parent, hier)
			try:
				(p, children) = parHier
			except:
				raise NameError("Did not find %s parent %s" % (bone, parent))
			children.append((bone, []))
	
	# newHier = addInvBones(hier, heads, tails)
	newHier = hier
	bones = []
	flatten(newHier, bones)
	return (heads, tails, newHier, bones, weights)

#
#	addInvBones(hier, heads, tails):
#

def addInvBones(hier, heads, tails):
	newHier = []
	for (bone, children) in hier:
		newChildren = addInvBones(children, heads, tails)
		n = len(children)
		if n == 1:
			(child, subChildren) = children[0]
			offs = vsub(tails[bone], heads[child])
		if n > 1 or (n == 1 and vlen(offs) > 1e-4):
			boneInv = bone+"Inv"
			heads[boneInv] = tails[bone]
			#tails[boneInv] = heads[bone]
			tails[boneInv] = aljabr.vadd(tails[bone], Delta)
			newHier.append( (bone, [(boneInv, newChildren)]) )
		else:
			newHier.append( (bone, newChildren) )

	return newHier

#
#	class CStuff
#

class CStuff:
	def __init__(self, name, proxy):
		self.name = name
		self.type = None
		self.bones = None
		self.rawWeights = None
		self.verts  = None
		self.vnormals = None
		self.uvValues = None
		self.faces = None
		self.weights = None
		self.targets = None
		self.vertexWeights = None
		self.skinWeights = None
		self.material = None
		if proxy:
			self.type = proxy.type
			self.material = proxy.material

	def setBones(self, amt):
		(rigHead, rigTail, rigHier, bones, rawWeights) = amt
		self.rigHead = rigHead
		self.rigTail = rigTail
		self.rigHier = rigHier
		self.bones = bones
		self.rawWeights = rawWeights

	def copyBones(self, rig):
		self.rigHead = rig.rigHead
		self.rigTail = rig.rigTail
		self.rigHier = rig.rigHier
		self.bones = rig.bones
		self.rawWeights = rig.rawWeights

	def setMesh(self, mesh):
		(verts, vnormals, uvValues, faces, weights, targets) = mesh
		self.verts = verts
		self.vnormals = vnormals
		self.uvValues = uvValues
		self.faces = faces
		self.weights = weights
		self.targets = targets
		return

#
#	filterMesh(mesh1):
#

def filterMesh(mesh1):
	(verts1, vnormals1, uvValues1, faces1, weights1, targets1) = mesh1

	killVerts = {}
	killUvs = {}
	for f in faces1:
		if len(f) == 3:
			for v in f:
				killVerts[v[0]] = True
				killUvs[v[1]] = True

	n = 0
	nv = {}
	verts2 = []
	for m,v in enumerate(verts1):
		try:
			killVerts[m]
		except:
			verts2.append(v)
			nv[m] = n
			n += 1

	vnormals2 = []
	for m,vn in enumerate(vnormals1):
		try:
			killVerts[m]
		except:
			vnormals2.append(vn)

	n = 0
	uvValues2 = []
	nuv = {}
	for m,uv in enumerate(uvValues1):
		try:
			killUvs[m]
		except:
			uvValues2.append(uv)
			nuv[m] = n
			n += 1	

	faces2 = []
	for f in faces1:
		if len(f) == 4:
			f2 = []
			for c in f:
				v2 = nv[c[0]]
				uv2 = nuv[c[1]]
				f2.append([v2, uv2])
			faces2.append(f2)

	weights2 = {}
	for (b, wts1) in weights1.items():
		wts2 = []
		for (v1,w) in wts1:
			try:
				killVerts[v1]
			except:
				wts2.append((nv[v1],w))
		weights2[b] = wts2

	targets2 = []
	for (name, morphs1) in targets1:
		morphs2 = []
		for (v1,dx) in morphs1:
			try:
				killVerts[v1]
			except:
				morphs2.append((nv[v1],dx))
		targets2.append(name, morphs2)

	return (verts2, vnormals2, uvValues2, faces2, weights2, targets2)

#
#	exportDae(obj, fp):
#

def exportDae(obj, fp):
	global theStuff
	(useMain, rig, mhxVersion, proxyList) = mh2proxy.proxyConfig()
	amt = getArmatureFromRigFile('data/templates/game.rig', obj)
	#rawTargets = loadShapeKeys("data/templates/shapekeys-facial25.mhx")
	rawTargets = []

	stuffs = []
	stuff = CStuff('Human', None)
	stuff.setBones(amt)
	theStuff = stuff
	if 'Dae' in useMain:
		mesh1 = mh2proxy.getMeshInfo(obj, None, stuff.rawWeights, rawTargets, None)
		mesh2 = filterMesh(mesh1)
		stuff.setMesh(mesh2)
		stuffs.append(stuff)

	setupProxies('Proxy', obj, stuffs, amt, rawTargets, proxyList)
	setupProxies('Clothes', obj, stuffs, amt, rawTargets, proxyList)

	if theStuff.verts == None:
		raise NameError("No rig found. Neither main mesh nor rigged proxy enabled")

	date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())

	fp.write('<?xml version="1.0" encoding="utf-8"?>\n' +
'<COLLADA version="1.4.0" xmlns="http://www.collada.org/2005/11/COLLADASchema">\n' +
'  <asset>\n' +
'    <contributor>\n' +
'      <author>www.makehuman.org</author>\n' +
'    </contributor>\n' +
'    <created>%s</created>\n' % date +
'    <modified>%s</modified>\n' % date +
'    <unit meter="0.1" name="decimeter"/>\n' +
'    <up_axis>Z_UP</up_axis>\n' +
'  </asset>\n' +
'  <library_images>\n')

	for stuff in stuffs:
		writeImages(obj, fp, stuff)

	fp.write(
'  </library_images>\n' +
'  <library_effects>\n')

	for stuff in stuffs:
		writeEffects(obj, fp, stuff)

	fp.write(
'  </library_effects>\n' +
'  <library_materials>\n')

	for stuff in stuffs:
		writeMaterials(obj, fp, stuff)

	fp.write(
'  </library_materials>\n'+
'  <library_controllers>\n')

	for stuff in stuffs:
		writeController(obj, fp, stuff)

	fp.write(
'  </library_controllers>\n'+
'  <library_geometries>\n')

	for stuff in stuffs:
		writeGeometry(obj, fp, stuff)

	fp.write(
'  </library_geometries>\n\n' +
'  <library_visual_scenes>\n' +
'    <visual_scene id="Scene" name="Scene">\n')
	writeBones(fp, theStuff.rigHier, [0,0,0], 'layer="L1"', '', theStuff)
	for stuff in stuffs:
		writeNode(obj, fp, stuff)

	fp.write(
'    </visual_scene>\n' +
'  </library_visual_scenes>\n' +
'  <scene>\n' +
'    <instance_visual_scene url="#Scene"/>\n' +
'  </scene>\n' +
'</COLLADA>\n')
	return

#
#	setupProxies(typename, obj, stuffs, amt, rawTargets, proxyList):
#

def setupProxies(typename, obj, stuffs, amt, rawTargets, proxyList):
	global theStuff
	for (typ, useObj, useMhx, useDae, proxyStuff) in proxyList:
		if useDae and typ == typename:
			proxy = mh2proxy.readProxyFile(obj, proxyStuff)
			if proxy.name:
				stuff = CStuff(proxy.name, proxy)
				if proxy.rig:
					(proxyFile, typ, layer) = proxyStuff
					amtProxy = getArmatureFromRigFile(proxy.rig, obj)
					stuff.setBones(amtProxy)
					if theStuff.verts:
						print("WARNING: Collada export with several meshes. Ignored %s" % proxy.name)
						stuff = None
					else:
						theStuff = stuff	
				elif proxy.weightfile:
					(rigname, filename) = proxy.weightfile
					if theStuff and rigname == theStuff.name:
						stuff.copyBones(theStuff)
					else:
						stuff.setBones(amt)
				else:
					stuff.setBones(amt)
					#theStuff.verts = True
				if stuff:
					if theStuff:
						stuffname = theStuff.name
					else:
						stuffname = None
					mesh = mh2proxy.getMeshInfo(obj, proxy, stuff.rawWeights, rawTargets, stuffname)
					stuff.setMesh(mesh)
					stuffs.append(stuff)
	return

#
#	writeImages(obj, fp, stuff):
#

def writeImages(obj, fp, stuff):
	if stuff.type:
		return
	dd = '~/makehuman'
	dd = 'data/textures'
	texdir = os.path.realpath(os.path.expanduser(dd))
	fp.write(
'    <image id="texture_tif">\n' +
'      <init_from>%s</init_from>\n' % ("%s/texture.tif" % texdir) +
'    </image>\n' +
'    <image id="texture_ref_tif">\n' +
'      <init_from>%s</init_from>\n' % ("%s/texture_ref.tif" % texdir) +
'    </image>\n')
	return

#
#	writeEffects(obj, fp, stuff):
#	writeColor(fp, name, color, insist):
#

def writeColor(fp, name, color, insist):
	if color:
		(r,g,b) = color
	elif insist:
		(r,g,b) = insist
	else:
		return
	fp.write(
'            <%s>\n' % name +
'              <color>%.4f %.4f %.4f 1</color>\n' % (r,g,b) +
'            </%s>\n' %name)
	return 

def writeEffects(obj, fp, stuff):
	mat = stuff.material
	if mat:
		fp.write(
'    <effect id="%s-effect">\n' % mat.name +
'      <profile_COMMON>\n' +
'        <technique sid="common">\n' +
'          <lambert>\n')
		writeColor(fp, 'diffuse', mat.diffuse_color, (0.8,0.8,0.8))
		writeColor(fp, 'specular', mat.specular_color, (1,1,1))
		writeColor(fp, 'emission', mat.emit_color, None)
		writeColor(fp, 'ambient', mat.ambient_color, None)
		fp.write(
'          </lambert>\n' +
'          <extra/>\n' +
'        </technique>\n' +
'        <extra>\n' +
'          <technique profile="GOOGLEEARTH">\n' +
'            <show_double_sided>1</show_double_sided>\n' +
'          </technique>\n' +
'        </extra>\n' +
'      </profile_COMMON>\n' +
'      <extra><technique profile="MAX3D"><double_sided>1</double_sided></technique></extra>\n' +
'    </effect>\n')
	elif not stuff.type:
		fp.write(
'    <effect id="SSS_skinshader-effect">\n' +
'      <profile_COMMON>\n' +
'        <newparam sid="texture_tif-surface">\n' +
'          <surface type="2D">\n' +
'            <init_from>texture_tif</init_from>\n' +
'          </surface>\n' +
'        </newparam>\n' +
'        <newparam sid="texture_tif-sampler">\n' +
'          <sampler2D>\n' +
'            <source>texture_tif-surface</source>\n' +
'          </sampler2D>\n' +
'        </newparam>\n' +
'        <newparam sid="texture_ref_tif-surface">\n' +
'          <surface type="2D">\n' +
'            <init_from>texture_ref_tif</init_from>\n' +
'          </surface>\n' +
'        </newparam>\n' +
'        <newparam sid="texture_ref_tif-sampler">\n' +
'          <sampler2D>\n' +
'            <source>texture_ref_tif-surface</source>\n' +
'          </sampler2D>\n' +
'        </newparam>\n' +
'        <technique sid="common">\n' +
'          <phong>\n' +
'            <emission>\n' +
'              <color>0 0 0 1</color>\n' +
'            </emission>\n' +
'            <ambient>\n' +
'              <color>0 0 0 1</color>\n' +
'            </ambient>\n' +
'            <diffuse>\n' +
'              <texture texture="texture_tif-sampler" texcoord="UVTex"/>\n' +
'            </diffuse>\n' +
'            <specular>\n' +
'              <texture texture="texture_ref_tif-sampler" texcoord="UVTex"/>\n' +
'            </specular>\n' +
'            <shininess>\n' +
'              <float>2</float>\n' +
'            </shininess>\n' +
'            <reflective>\n' +
'              <color>0 0 0 1</color>\n' +
'            </reflective>\n' +
'            <reflectivity>\n' +
'              <float>0</float>\n' +
'            </reflectivity>\n' +
'            <transparency>\n' +
'              <texture texture="texture_tif-sampler" texcoord="UVTex"/>\n' +
'            </transparency>\n' +
'            <index_of_refraction>\n' +
'              <float>1</float>\n' +
'            </index_of_refraction>\n' +
'          </phong>\n' +
'        </technique>\n' +
'      </profile_COMMON>\n' +
'    </effect>\n')
	return

#
#	writeMaterials(obj, fp, stuff):
#

def writeMaterials(obj, fp, stuff):
	mat = stuff.material
	if mat:
		fp.write(
'    <material id="%s" name="%s">\n' % (mat.name, mat.name) +
'      <instance_effect url="#%s-effect"/>\n' % mat.name +
'    </material>\n')
	elif not stuff.type:
		fp.write(
'    <material id="SSS_skinshader" name="SSS_skinshader">\n' +
'      <instance_effect url="#SSS_skinshader-effect"/>\n' +
'    </material>\n')
	return

#
#	writeController(obj, fp, stuff):
#

def writeController(obj, fp, stuff):
	stuff.vertexWeights = {}
	for (vn,v) in enumerate(stuff.verts):
		stuff.vertexWeights[vn] = []

	stuff.skinWeights = []
	wn = 0	
	for (bn,b) in enumerate(stuff.bones):
		try:
			wts = stuff.weights[b]
		except:
			wts = []
		for (vn,w) in wts:
			stuff.vertexWeights[int(vn)].append((bn,wn))
			wn += 1
		stuff.skinWeights.extend(wts)

	nVerts = len(stuff.verts)
	nUvVerts = len(stuff.uvValues)
	nNormals = nVerts
	nFaces = len(stuff.faces)
	nWeights = len(stuff.skinWeights)
	nBones = len(stuff.bones)
	nTargets = len(stuff.targets)

	fp.write('\n' +
'    <controller id="%s-skin">\n' % stuff.name +
'      <skin source="#%sMesh">\n' % stuff.name +
'        <bind_shape_matrix>\n' +
'          1.0 0.0 0.0 0.0 \n' +
'          0.0 1.0 0.0 0.0 \n' +
'          0.0 0.0 1.0 0.0 \n' +
'          0.0 0.0 0.0 1.0 \n' +
'        </bind_shape_matrix>\n' +
'        <source id="%s-skin-joints">\n' % stuff.name +
'          <IDREF_array count="%d" id="%s-skin-joints-array">\n' % (nBones,stuff.name) +
'           ')

	for b in stuff.bones:
		fp.write(' %s' % b)
	
	fp.write('\n' +
'          </IDREF_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-skin-joints-array" stride="1">\n' % (nBones,stuff.name) +
'              <param type="IDREF" name="JOINT"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="%s-skin-weights">\n' % stuff.name +
'          <float_array count="%d" id="%s-skin-weights-array">\n' % (nWeights,stuff.name) +
'           ')

	for (n,b) in enumerate(stuff.skinWeights):
		(v,w) = stuff.skinWeights[n]
		fp.write(' %s' % w)

	fp.write('\n' +
'          </float_array>\n' +	
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-skin-weights-array" stride="1">\n' % (nWeights,stuff.name) +
'              <param type="float" name="WEIGHT"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="%s-skin-poses">\n' % stuff.name +
'          <float_array count="%d" id="%s-skin-poses-array">' % (16*nBones,stuff.name))

	mat = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
	for b in stuff.bones:
		vec = stuff.rigHead[b]
		mat[0][3] = -vec[0]
		mat[1][3] = vec[2]
		mat[2][3] = -vec[1]
		fp.write('\n            ')
		for i in range(4):
			for j in range(4):
				fp.write('%.4f ' % mat[i][j])

	fp.write('\n' +
'          </float_array>\n' +	
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-skin-poses-array" stride="16">\n' % (nBones,stuff.name) +
'              <param type="float4x4"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <joints>\n' +
'          <input semantic="JOINT" source="#%s-skin-joints"/>\n' % stuff.name +
'          <input semantic="INV_BIND_MATRIX" source="#%s-skin-poses"/>\n' % stuff.name +
'        </joints>\n' +
'        <vertex_weights count="%d">\n' % nVerts +
'          <input offset="0" semantic="JOINT" source="#%s-skin-joints"/>\n' % stuff.name +
'          <input offset="1" semantic="WEIGHT" source="#%s-skin-weights"/>\n' % stuff.name +
'          <vcount>\n' +
'            ')

	for wts in stuff.vertexWeights.values():
		fp.write('%d ' % len(wts))

	fp.write('\n' +
'          </vcount>\n'
'          <v>\n' +
'           ')

	#print(stuff.vertexWeights)
	for (vn,wts) in stuff.vertexWeights.items():
		wtot = 0.0
		for (bn,wn) in wts:
			wtot += wn
		if wtot < 0.01:
			# print("wtot", vn, wtot)
			wtot = 1
		for (bn,wn) in wts:
			fp.write(' %d %d' % (bn, wn))

	fp.write('\n' +
'          </v>\n' +
'        </vertex_weights>\n' +
'      </skin>\n' +
'    </controller>\n')

	"""
	fp.write('\n' +
'   <controller id="%sMorphs" name="%sMorphs">\n' % (stuff.name,stuff.name) +
'     <morph method="NORMALIZED" source="#%sMesh">\n' % stuff.name +
'       <source id="%s-targets">\n' % stuff.name +
'         <IDREF_array id="%s-targets-array" count="%d">\n'  % (stuff.name, nTargets))

	for (name, morphs) in targets:
		fp.write(' %s' % name)

	fp.write('\n' +
'         </IDREF_array>\n' +
'         <technique_common>\n' +
'           <accessor source="%s-targets-array" count="%d" stride="1">\n' % (stuff.name,nTargets) +
'             <param name="MORPH_TARGET" type="IDREF"/>\n' +
'           </accessor>\n' +
'         </technique_common>\n' +
'       </source>\n' +
'       <source id="%s-morph_weights">\n' % name +
'         <float_array id="%s-morph_weights-array" count="%d">\n' % (stuff.name,nTargets))

	for target in targets:
		fp.write("0.0 ")

	fp.write('\n' +
'         </float_array>\n' +
'         <technique_common>\n' +
'           <accessor source="#%s-morph_weights-array" count="%d" stride="1">\n' % (stuff.name,nTargets) +

'             <param name="MORPH_WEIGHT" type="float"/>\n' +
'           </accessor>\n' +
'         </technique_common>\n' +
'       </source>\n' +
'       <targets>\n' +
'         <input semantic="MORPH_TARGET" source="#%s-targets"/>\n' % stuff.name +
'         <input semantic="MORPH_WEIGHT" source="#%s-morph_weights"/>\n' % stuff.name +
'       </targets>\n' +
'     </morph>\n' +
'   </controller>\n')
	"""
	return

#
#	writeGeometry(obj, fp, stuff):
#
		
def writeGeometry(obj, fp, stuff):
	nVerts = len(stuff.verts)
	nUvVerts = len(stuff.uvValues)
	nNormals = nVerts
	nFaces = len(stuff.faces)
	nWeights = len(stuff.skinWeights)
	nBones = len(stuff.bones)
	nTargets = len(stuff.targets)

	fp.write('\n' +
'    <geometry id="%sMesh" name="%s">\n' % (stuff.name,stuff.name) +
'      <mesh>\n' +
'        <source id="%s-Position">\n' % stuff.name +
'          <float_array count="%d" id="%s-Position-array">\n' % (3*nVerts,stuff.name) +
'          ')


	for v in stuff.verts:
		fp.write('%.6g %.6g %.6g ' % (v[0], -v[2], v[1]))

	fp.write('\n' +
'          </float_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-Position-array" stride="3">\n' % (nVerts,stuff.name) +
'              <param type="float" name="X"></param>\n' +
'              <param type="float" name="Y"></param>\n' +
'              <param type="float" name="Z"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="%s-Normals">\n' % stuff.name +
'          <float_array count="%d" id="%s-Normals-array">\n' % (3*nNormals,stuff.name) +
'          ')

	for no in stuff.vnormals:
		fp.write('%.6g %.6g %.6g ' % (no[0], -no[2], no[1]))

	fp.write('\n' +
'          </float_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-Normals-array" stride="3">\n' % (nNormals,stuff.name) +
'              <param type="float" name="X"></param>\n' +
'              <param type="float" name="Y"></param>\n' +
'              <param type="float" name="Z"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="%s-UV">\n' % stuff.name +

'          <float_array count="%d" id="%s-UV-array">\n' % (2*nUvVerts,stuff.name) +
'           ')


	for uv in stuff.uvValues:
		fp.write(" %.4f %.4f" %(uv[0], uv[1]))

	fp.write('\n' +
'          </float_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#%s-UV-array" stride="2">\n' % (nUvVerts,stuff.name) +
'              <param type="float" name="S"></param>\n' +
'              <param type="float" name="T"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <vertices id="%s-Vertex">\n' % stuff.name +
'          <input semantic="POSITION" source="#%s-Position"/>\n' % stuff.name +
'        </vertices>\n' +
'        <polygons count="%d">\n' % nFaces +
'          <input offset="0" semantic="VERTEX" source="#%s-Vertex"/>\n' % stuff.name +
'          <input offset="1" semantic="NORMAL" source="#%s-Normals"/>\n' % stuff.name +
'          <input offset="2" semantic="TEXCOORD" source="#%s-UV"/>\n' % stuff.name)

	for fc in stuff.faces:
		fp.write('          <p>')
		for vs in fc:
			v = vs[0]
			uv = vs[1]
			if v > nVerts:
				raise NameError("v %d > %d" % (v, nVerts))
			if uv > nUvVerts:
				raise NameError("uv %d > %d" % (uv, nUvVerts))			
			fp.write("%d %d %d " % (v, v, uv))
		fp.write('</p>\n')
	
	fp.write('\n' +
'        </polygons>\n' +
'      </mesh>\n' +
'    </geometry>\n')

	"""
	for target in targets:
		(name, morphs) = target
		fp.write('\n' +
'   <geometry id="%s" name="%s">\n' % (name, name) +
'     <mesh>\n' +
'       <source id="%s-positions" name="%s-position">\n' % (name, name) +
'         <float_array id="%s-positions-array" count="%d">\n' % (name, 3*nVerts) +
'          ')
		for (vn,v) in enumerate(verts):
			try:
				offs = morphs[vn]
				loc = vadd(v, offs)
			except:
				loc = v
			fp.write("%.4f %.4f %.4f " % (loc[0], -loc[2], loc[1]))

		fp.write('\n'+
'         </float_array>\n' +
'         <technique_common>\n' +
'           <accessor source="#%s-positions-array" count="%d" stride="3">\n' % (stuff.name, nVerts) +
'             <param name="X" type="float"/>\n' +
'             <param name="Y" type="float"/>\n' +
'             <param name="Z" type="float"/>\n' +
'           </accessor>\n' +
'         </technique_common>\n' +
'       </source>\n' +
'     </mesh>\n' +
'   </geometry>\n')
	"""
	return

#
#	writeNode(obj, fp, stuff):
#

def writeNode(obj, fp, stuff):	
	fp.write('\n' +
'      <node layer="L1" id="%sObject" name="%s">\n' % (stuff.name,stuff.name) +
'        <translate sid="translate">0 0 0</translate>\n' +
'        <rotate sid="rotateZ">0 0 1 0</rotate>\n' +
'        <rotate sid="rotateY">0 1 0 0</rotate>\n' +
'        <rotate sid="rotateX">1 0 0 0</rotate>\n' +
'        <scale sid="scale">1 1 1</scale>\n' +
'        <instance_controller url="#%s-skin">\n' % stuff.name +
'          <skeleton>#%s</skeleton>\n' % Root)

	if stuff.type == None:
		matname = 'SSS_skinshader'
	elif stuff.material:
		matname = stuff.material.name
	else:
		matname = None

	if matname:
		fp.write(
'          <bind_material>\n' +
'            <technique_common>\n' +
'              <instance_material symbol="%s" target="#%s">\n' % (matname, matname) +
'                <bind_vertex_input semantic="UVTex" input_semantic="TEXCOORD" input_set="0"/>\n' +
'              </instance_material>\n' +
'            </technique_common>\n' +
'          </bind_material>\n')

	fp.write(
'        </instance_controller>\n' +
'      </node>\n')
	return

#
#	loadShapeKeys(tmplName):	
#	ShapeKey BrowsDown LR toggle&T_Face
#  	sv 2139 0 0 -0.0109844
#

def loadShapeKeys(tmplName):
	tmpl = open(tmplName, "rU")
	if tmpl == None:
		print("Cannot open template "+tmplName)
		return []

	targets = []
	for line in tmpl:
		lineSplit= line.split()

		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == 'ShapeKey':
			morph = {}
			targets.append((lineSplit[1], morph))
		elif lineSplit[0] == 'wv':
			v = int(lineSplit[1])
			x = float(lineSplit[2])
			y = float(lineSplit[3])
			z = float(lineSplit[4])
			morph[v] = [x,y,z]

	tmpl.close()
	return targets

	

