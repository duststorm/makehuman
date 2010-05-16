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
import mhx_rig, rig_body_25, rig_arm_25, rig_finger_25, rig_leg_25, rig_toe_25, rig_face_25, rig_panel_25
from mhx_rig import *

#
# ....exportCollada(obj, filename):
#


def exportCollada(obj, filename):
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

def boneOK(flags, bone, parent):
	if bone == 'Root':
		return 'None'
	#elif bone in twistBones.keys():
	#	return None
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
#	writeBone(fp, bone, orig, extra, pad):
#

def writeBones(fp, bones, orig, extra, pad):
	for bone in bones:
		writeBone(fp, bone, orig, extra, pad)
	return
	
def writeBone(fp, bone, orig, extra, pad):
	global rigHead, rigTail
	(name, children) = bone
	head = rigHead[name]
	vec = aljabr.vsub(head, orig)
	printNode(fp, name, vec, extra, pad)
	if children:
		writeBones(fp, children, head, '', pad+'  ')	
	else:
		tail = rigTail[name]
		vec = aljabr.vsub(tail, head)
		printNode(fp, name+"_end", vec, '', pad+'  ')
		fp.write('\n%s        </node>' % pad)
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
#	exportDae(obj, fp):
#

def exportDae(obj, fp):
	global rigHead, rigTail

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
		
	rigHead = mhx_rig.rigHead
	rigTail = mhx_rig.rigTail
	
	rigHier = []
	armature = rig_body_25.BodyArmature + rig_arm_25.ArmArmature + rig_finger_25.FingerArmature + rig_leg_25.LegArmature + rig_toe_25.ToeArmature + rig_face_25.FaceArmature

	for (bone, cond, roll, parent, flags, layers, bbone) in armature:
		par = boneOK(flags, bone, parent)
		if par:
			if par == 'None':
				rigHier.append((bone, []))
			else:
				#print("find", bone, par, rigHier)
				(p, children) = findInHierarchy(par, rigHier)
				children.append((bone, []))
	#print("hier", rigHier)
	
	bones = []
	flatten(rigHier, bones)	
	nBones = len(bones)

	weights = {}
	readSkinWeights(weights, "data/templates/vertexgroups-bones25.mhx")	
	# fixTwistWeights(fp, weights)
	
	vertexWeights = {}
	for (vn,v) in enumerate(obj.verts):
		vertexWeights[vn] = []

	skinWeights = []
	wn = 0	
	for (bn,b) in enumerate(bones):
		try:
			wts = weights[b]
		except:
			wts = []
		for (vn,w) in wts:
			vertexWeights[int(vn)].append((bn,wn))
			wn += 1
		skinWeights.extend(wts)
	nWeights = len(skinWeights)

	faces = files3d.loadFacesIndices("data/3dobjs/base.obj")

	nVerts = len(obj.verts)
	nUvVerts = len(obj.uvValues)
	nNormals = nVerts
	nFaces = len(faces)

	texture = os.path.expanduser("~/makehuman/texture.tif")
	texture_ref = os.path.expanduser("~/makehuman/texture_ref.tif")	
	date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())

#
#	Images, materials and effects
#

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
'  <library_images>\n' +
'    <image id="texture_tif">\n' +
'      <init_from>%s</init_from>\n' % texture +
'    </image>\n' +
'    <image id="texture_ref_tif">\n' +
'      <init_from>%s</init_from>\n' % texture_ref +
'    </image>\n' +
'  </library_images>\n' +
'  <library_effects>\n' +
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
'    </effect>\n' +
'  </library_effects>\n' +
'  <library_materials>\n' +
'    <material id="SSS_skinshader" name="SSS_skinshader">\n' +
'      <instance_effect url="#SSS_skinshader-effect"/>\n' +
'    </material>\n' +
'  </library_materials>\n')

#
#	Controllers
#

	fp.write('\n' +
'    <library_controllers>\n' +
'    <controller id="Human-skin">\n' +
'      <skin source="#HumanMesh">\n' +
'        <bind_shape_matrix>\n' +
'          1.0 0.0 0.0 0.0 \n' +
'          0.0 1.0 0.0 0.0 \n' +
'          0.0 0.0 1.0 0.0 \n' +
'          0.0 0.0 0.0 1.0 \n' +
'        </bind_shape_matrix>\n' +
'        <source id="Human-skin-joints">\n' +
'          <IDREF_array count="%d" id="Human-skin-joints-array">\n' % nBones +
'           ')

	for b in bones:
		fp.write(' %s' % b)
	
	fp.write('\n' +
'          </IDREF_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#Human-skin-joints-array" stride="1">\n' % nBones +
'              <param type="IDREF" name="JOINT"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="Human-skin-weights">\n' +
'          <float_array count="%d" id="Human-skin-weights-array">\n' % nWeights +
'           ')

	for (n,b) in enumerate(skinWeights):
		(v,w) = skinWeights[n]
		fp.write(' %s' % w)

	fp.write('\n' +
'          </float_array>\n' +	
'          <technique_common>\n' +
'            <accessor count="%d" source="#Human-skin-weights-array" stride="1">\n' % nWeights +
'              <param type="float" name="WEIGHT"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="Human-skin-poses">\n' +
'          <float_array count="%d" id="Human-skin-poses-array">' % (16*nBones))

	mat = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
	for b in bones:
		vec = rigHead[b]
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
'            <accessor count="%d" source="#Human-skin-poses-array" stride="16">\n' % nBones +
'              <param type="float4x4"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <joints>\n' +
'          <input semantic="JOINT" source="#Human-skin-joints"/>\n' +
'          <input semantic="INV_BIND_MATRIX" source="#Human-skin-poses"/>\n' +
'        </joints>\n' +
'        <vertex_weights count="%d">\n' % nVerts +
'          <input offset="0" semantic="JOINT" source="#Human-skin-joints"/>\n' +
'          <input offset="1" semantic="WEIGHT" source="#Human-skin-weights"/>\n' +
'          <vcount>\n' +
'            ')

	for wts in vertexWeights.values():
		fp.write('%d ' % len(wts))

	fp.write('\n' +
'          </vcount>\n'
'          <v>\n' +
'           ')

	#print(vertexWeights)
	for (vn,wts) in vertexWeights.items():
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
	targets = loadShapeKeys("data/templates/shapekeys-facial25.mhx")
	nTargets = len(targets)
	fp.write('\n' +
'   <controller id="HumanMorphs" name="HumanMorphs">\n' +
'     <morph method="NORMALIZED" source="#HumanMesh">\n' +
'       <source id="Human-targets">\n' +
'         <IDREF_array id="Human-targets-array" count="%d">\n' % nTargets)

	for (name, morphs) in targets:
		fp.write(' %s' % name)

	fp.write('\n' +
'         </IDREF_array>\n' +
'         <technique_common>\n' +
'           <accessor source="Human-targets-array" count="%d" stride="1">\n' % nTargets +
'             <param name="MORPH_TARGET" type="IDREF"/>\n' +
'           </accessor>\n' +
'         </technique_common>\n' +
'       </source>\n' +
'       <source id="Human-morph_weights">\n' +
'         <float_array id="Human-morph_weights-array" count="%d">\n' % nTargets)

	for target in targets:
		fp.write("0.0 ")

	fp.write('\n' +
'         </float_array>\n' +
'         <technique_common>\n' +
'           <accessor source="#Human-morph_weights-array" count="%d" stride="1">\n' % nTargets +
'             <param name="MORPH_WEIGHT" type="float"/>\n' +
'           </accessor>\n' +
'         </technique_common>\n' +
'       </source>\n' +
'       <targets>\n' +
'         <input semantic="MORPH_TARGET" source="#Human-targets"/>\n' +
'         <input semantic="MORPH_WEIGHT" source="#Human-morph_weights"/>\n' +
'       </targets>\n' +
'     </morph>\n' +
'   </controller>\n')
	"""
	fp.write('\n' +
'  </library_controllers>\n')

#
#	Geometries
#

	fp.write('\n' +
'  <library_geometries>\n' +
'    <geometry id="HumanMesh" name="Human">\n' +
'      <mesh>\n' +
'        <source id="Human-Position">\n' +
'          <float_array count="%d" id="Human-Position-array">\n' % (3*nVerts) +
'          ')

	for v in obj.verts:
		fp.write('%.6g %.6g %.6g ' % (v.co[0], -v.co[2], v.co[1]))

	fp.write('\n' +
'          </float_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#Human-Position-array" stride="3">\n' % nVerts +
'              <param type="float" name="X"></param>\n' +
'              <param type="float" name="Y"></param>\n' +
'              <param type="float" name="Z"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="Human-Normals">\n' +
'          <float_array count="%d" id="Human-Normals-array">\n' % (3*nNormals) +
'          ')

	for v in obj.verts:
		fp.write('%.6g %.6g %.6g ' % (v.no[0], -v.no[2], v.no[1]))

	fp.write('\n' +
'          </float_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#Human-Normals-array" stride="3">\n' % nNormals +
'              <param type="float" name="X"></param>\n' +
'              <param type="float" name="Y"></param>\n' +
'              <param type="float" name="Z"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <source id="Human-UV">\n' +

'          <float_array count="%d" id="Human-UV-array">\n' % (2*nUvVerts) +
'           ')


	for uv in obj.uvValues:
		fp.write(" %.4f %.4f" %(uv[0], uv[1]))

	fp.write('\n' +
'          </float_array>\n' +
'          <technique_common>\n' +
'            <accessor count="%d" source="#Human-UV-array" stride="2">\n' % nUvVerts +
'              <param type="float" name="S"></param>\n' +
'              <param type="float" name="T"></param>\n' +
'            </accessor>\n' +
'          </technique_common>\n' +
'        </source>\n' +
'        <vertices id="Human-Vertex">\n' +
'          <input semantic="POSITION" source="#Human-Position"/>\n' +
'        </vertices>\n' +
'        <polygons count="%d">\n' % nFaces +
'          <input offset="0" semantic="VERTEX" source="#Human-Vertex"/>\n' +
'          <input offset="1" semantic="NORMAL" source="#Human-Normals"/>\n' +
'          <input offset="2" semantic="TEXCOORD" source="#Human-UV"/>\n')

	for fc in faces:
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
		for (vn,v) in enumerate(obj.verts):
			try:
				offs = morphs[vn]
				loc = vadd(v.co, offs)
			except:
				loc = v.co
			fp.write("%.4f %.4f %.4f " % (loc[0], -loc[2], loc[1]))

		fp.write('\n'+
'         </float_array>\n' +
'         <technique_common>\n' +
'           <accessor source="#%s-positions-array" count="%d" stride="3">\n' % (name, nVerts) +
'             <param name="X" type="float"/>\n' +
'             <param name="Y" type="float"/>\n' +
'             <param name="Z" type="float"/>\n' +
'           </accessor>\n' +
'         </technique_common>\n' +
'       </source>\n' +
'     </mesh>\n' +
'   </geometry>\n')
	"""
	fp.write('\n' +
'  </library_geometries>\n')

#
#	Visual scenes
#

	fp.write('\n' +
'  <library_visual_scenes>\n' +
'    <visual_scene id="Scene" name="Scene">\n')

	writeBones(fp, rigHier, [0,0,0], 'layer="L1"', '')
	
	fp.write('\n' +
'      <node layer="L1" id="HumanObject" name="Human">\n' +
'        <translate sid="translate">0 0 0</translate>\n' +
'        <rotate sid="rotateZ">0 0 1 0</rotate>\n' +
'        <rotate sid="rotateY">0 1 0 0</rotate>\n' +
'        <rotate sid="rotateX">1 0 0 0</rotate>\n' +
'        <scale sid="scale">1 1 1</scale>\n' +
'        <instance_controller url="#Human-skin">\n' +
'          <skeleton>#Root</skeleton>\n' +
'          <bind_material>\n' +
'            <technique_common>\n' +
'              <instance_material symbol="SSS_skinshader" target="#SSS_skinshader">\n' +
'                <bind_vertex_input semantic="UVTex" input_semantic="TEXCOORD" input_set="0"/>\n' +
'              </instance_material>\n' +
'            </technique_common>\n' +
'          </bind_material>\n' +
'        </instance_controller>\n' +
'      </node>\n' +
'    </visual_scene>\n' +
'  </library_visual_scenes>\n' +
'  <scene>\n' +
'    <instance_visual_scene url="#Scene"/>\n' +
'  </scene>\n' +
'</COLLADA>\n')

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

	

