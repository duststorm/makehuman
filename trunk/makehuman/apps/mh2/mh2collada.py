#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

MakeHuman to Collada (MakeHuman eXchange format) exporter. Collada files can be loaded into
Blender by collada_import.py.

TODO
"""

import module3d
import aljabr
import mh
import files3d
import mh2bvh
import os, time
import mh2proxy
import export_config
import object_collection
import mhx
from mhx import the
import log

#
#    Size of end bones = 1 mm
# 
Delta = [0,0.01,0]

#
# exportCollada(human, filename, options):
#

def exportCollada(human, filename, options):
    time1 = time.clock()
    the.Config = export_config.exportConfig(human, True, [])
    the.Config.separatefolder = True
    the.Rotate90X = options["rotate90X"]
    the.Rotate90Z = options["rotate90Z"]
    the.Options = options
    outfile = export_config.getOutFileFolder(filename, the.Config)        
    try:
        fp = open(outfile, 'w')
        log.message("Writing Collada file %s" % outfile)
    except:
        log.error("Unable to open file for writing %s" % outfile)
    (name,ext) = os.path.splitext(os.path.basename(outfile))
    exportDae(human, name, fp)
    fp.close()
    time2 = time.clock()
    log.message("Wrote Collada file in %g s: %s" % (time2-time1, outfile))
    return

#
#
#

def rotateLoc(loc, scale):    
    (x,y,z) = (scale*loc[0], scale*loc[1], scale*loc[2])
    if the.Rotate90X:
        yy = -z
        z = y
        y = yy
    if the.Rotate90Z:
        yy = x
        x = -y
        y = yy        
    return (x,y,z)        

#
#    boneOK(flags, bone, parent):
#
"""
Reparents = {
    'UpArm_L'     : 'Clavicle_L',
    'UpArm_R'     : 'Clavicle_R',
    'UpLeg_L'     : 'Hip_L',
    'UpLeg_R'     : 'Hip_R',
    
    'UpArmTwist_L'     : 'Clavicle_L',
    'UpArmTwist_R'     : 'Clavicle_R',
    'UpLegTwist_L'     : 'Hip_L',
    'UpLegTwist_R'     : 'Hip_R',
}

TwistBones = {
    'UpArmTwist_L'     : 'UpArm_L',
    'UpArmTwist_R'     : 'UpArm_R',
    'LoArmTwist_L'     : 'LoArm_L',
    'LoArmTwist_R'     : 'LoArm_R',
    'UpLegTwist_L'     : 'UpLeg_L',
    'UpLegTwist_R'     : 'UpLeg_R',
}

SkipBones = [ 'Rib_L', 'Rib_R', 'Stomach_L', 'Stomach_R', 'Scapula_L', 'Scapula_R']

def boneOK(flags, bone, parent, root):
    if bone == root:
        return 'None'
    elif bone in TwistBones.keys():
        return None
    elif bone in SkipBones:
        return None
    elif bone in Reparents.keys():
        return Reparents[bone]
    elif flags & F_DEF:
        return parent
    elif bone in ['HipsInv']:
        return parent
    return None
    
#
#    readSkinWeights(weights, tmplName):
#
#    VertexGroup Breathe
#    wv 2543 0.148938 ;
#

def readSkinWeights(weights, tmplName):
    tmpl = open(tmplName, "rU")
    if tmpl == None:
        log.warning("Cannot open template %s" % tmplName)
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
    for (twist, bone) in TwistBones.items():
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
"""                
#
#    writeBone(fp, bone, orig, extra, pad, stuff):
#

def writeBone(fp, bone, orig, extra, pad, stuff):
    (name, children) = bone
    head = stuff.boneInfo.heads[name]
    vec = aljabr.vsub(head, orig)
    printNode(fp, name, vec, extra, pad)
    for child in children:
        writeBone(fp, child, head, '', pad+'  ', stuff)    
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
'%s        <translate sid="translate"> ' % pad)
    (scale, name) = the.Options["scale"]
    (x,y,z) = rotateLoc(vec, scale)
    fp.write("%.4f %.4f %.4f " % (x,y,z))
    fp.write('</translate>\n' +
'%s        <rotate sid="rotateZ">0 0 1 0.0</rotate>\n' % pad +
'%s        <rotate sid="rotateY">0 1 0 0.0</rotate>\n' % pad +
'%s        <rotate sid="rotateX">1 0 0 0.0</rotate>\n' % pad +
'%s        <scale sid="scale">1.0 1.0 1.0</scale>' % pad)
    

#
#    exportDae(human, name, fp):
#

def exportDae(human, name, fp):
    cfg = export_config.exportConfig(human, True)
    obj = human.meshData
    rigfile = "data/rigs/%s.rig" % the.Options["daerig"]

    stuffs = object_collection.setupObjects(
        name, 
        human, 
        rigfile=rigfile, 
        helpers=the.Options["helpers"], 
        hidden=the.Options["hidden"], 
        eyebrows=the.Options["eyebrows"], 
        lashes=the.Options["lashes"])
    mainStuff = stuffs[0]        

    date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
    if the.Rotate90X:
        upaxis = 'Z_UP'
    else:
        upaxis = 'Y_UP'
    (scale, unit) = the.Options["scale"]        
        
    fp.write('<?xml version="1.0" encoding="utf-8"?>\n' +
'<COLLADA version="1.4.0" xmlns="http://www.collada.org/2005/11/COLLADASchema">\n' +
'  <asset>\n' +
'    <contributor>\n' +
'      <author>www.makehuman.org</author>\n' +
'    </contributor>\n' +
'    <created>%s</created>\n' % date +
'    <modified>%s</modified>\n' % date +
'    <unit meter="%.4f" name="%s"/>\n' % (0.1/scale, unit) +
'    <up_axis>%s</up_axis>\n' % upaxis+
'  </asset>\n' +
'  <library_images>\n')

    for stuff in stuffs:
        writeImages(obj, fp, stuff, human)

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
'    <visual_scene id="Scene" name="Scene">\n' +
'      <node id="Scene_root">\n')
    for root in mainStuff.boneInfo.hier:
        writeBone(fp, root, [0,0,0], 'layer="L1"', '  ', mainStuff)
    for stuff in stuffs:
        writeNode(obj, fp, "        ", stuff)

    fp.write(
'      </node>\n' +    
'    </visual_scene>\n' +
'  </library_visual_scenes>\n' +
'  <scene>\n' +
'    <instance_visual_scene url="#Scene"/>\n' +
'  </scene>\n' +
'</COLLADA>\n')
    return

#
#    writeImages(obj, fp, stuff, human):
#

def writeImages(obj, fp, stuff, human):
    if stuff.texture:
        textures = [stuff.texture]
    else:
        textures = []

    for (folder, texname) in textures: 
        path = export_config.getOutFileName(texname, folder, True, human, the.Config)        
        texfile = os.path.basename(path)
        (fname, ext) = os.path.splitext(texname)  
        name = "%s_%s" % (fname, ext[1:])
        if the.Config.separatefolder:
            texpath = "textures/"+texfile
        else:
            texpath = path
        fp.write(
        '    <image id="%s" name="%s">\n' % (name, name) +
        '      <init_from>%s</init_from>\n' % texpath +
        '    </image>\n'
        )
    return

#
#    writeEffects(obj, fp, stuff):
#

def writeColor(fp, tech, tex, color, s):
    (r,g,b) = color
    fp.write('            <%s><color>%.4f %.4f %.4f 1</color> \n' % (tech, r*s, g*s, b*s) )
    if tex:
        fp.write('              <texture texture="%s-sampler" texcoord="UVTex"/>\n' % tex)
    fp.write('            </%s>\n' % tech)
    return 
    
def writeIntensity(fp, tech, tex, value):
    fp.write('            <%s><float>%s</float>\n' % (tech, value))
    if tex:
        fp.write('              <texture texture="%s-sampler" texcoord="UVTex"/>\n' % tex)
    fp.write('            </%s>\n' % tech)
    return
    
def writeTexture(fp, tech, tex):            
    fp.write(
'            <%s>\n' % tech +
'              <texture texture="%s-sampler" texcoord="UVTex"/>\n' % tex +
'            </%s>\n' % tech)
    return    
    
BlenderDaeColor = {
    'diffuse_color' : 'diffuse',
    'specular_color' : 'specular',
    'emit_color' : 'emission',
    'ambient_color' : 'ambient',
}

BlenderDaeIntensity = {
    'specular_hardness' : 'shininess',
}

DefaultMaterialSettings = {    
    'diffuse': (0.8,0.8,0.8),
    'specular': (0.1,0.1,0.1),
    'transparency' : 1,
    'shininess' : 10,
}

def writeEffects(obj, fp, stuff):
    (texname, texfile, matname) = object_collection.getTextureNames(stuff)
    if not stuff.type:
        tex = "texture_png"
        writeEffectStart(fp, "SkinShader")
        writeSurfaceSampler(fp, tex)
        #writeSurfaceSampler(fp, "texture_ref_png")
        writePhongStart(fp)
        writeTexture(fp, 'diffuse', tex)
        writeTexture(fp, 'transparent', tex)
        writeColor(fp, 'specular', None, (1,1,1), 0.1)        
        writeIntensity(fp, 'shininess', None, 10)
        writeIntensity(fp, 'transparency', None, 0)
        writePhongEnd(fp)            
    elif matname:
        matname = matname.replace(" ", "_")
        mat = stuff.material
        writeEffectStart(fp, matname)
        writeSurfaceSampler(fp, texfile)
        writePhongStart(fp)
        doneDiffuse = False
        doneSpec = False
        diffInt = 1
        specInt = 0.1
        for (key, value) in mat.settings:
            if key == "diffuse_intensity":
                diffInt = value
            elif key == "specular_intensity":
                specInt = value
        for (key, value) in mat.settings:
            if key == "diffuse_color":
                writeColor(fp, 'diffuse', texfile, value, diffInt)
                if mat.use_transparency:
                    writeTexture(fp, 'transparent', texfile)
                    writeIntensity(fp, 'transparency', None, mat.alpha)
                doneDiffuse = True
            elif key == "specular_color":
                writeColor(fp, 'specular', None, value, specInt)
                doneSpec = True
            else:                
                try:
                    tech = BlenderDaeColor[key]
                except:
                    tech = None
                if tech:
                    writeColor(fp, tech, None, value, 1)
                try:
                    tech = BlenderDaeIntensity[tech]
                except:
                    tech = None
                if tech:
                    writeIntensity(fp, tech, None, value, 1)
        if not doneDiffuse:   
            writeColor(fp, "diffuse", texfile, (1,1,1), 0.8)
            if mat.use_transparency:
                writeTexture(fp, 'transparent', texfile)
                writeIntensity(fp, 'transparency', None, mat.alpha)
        if not doneSpec:
            writeColor(fp, 'specular', None, (1,1,1), 0.1)        
            writeIntensity(fp, 'shininess', None, 10)                
        writePhongEnd(fp)
    return

def writeEffectStart(fp, name):        
        fp.write(
'    <effect id="%s-effect">\n' % name +
'      <profile_COMMON>\n')

def writePhongStart(fp): 
        fp.write(
'        <technique sid="common">\n' +
'          <phong>\n')

def writePhongEnd(fp):        
        fp.write(
'          </phong>\n' +
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

def writeSurfaceSampler(fp, tex):
    fp.write(
'        <newparam sid="%s-surface">\n' % tex +
'          <surface type="2D">\n' +
'            <init_from>%s</init_from>\n' % tex +
'          </surface>\n' +
'        </newparam>\n' +
'        <newparam sid="%s-sampler">\n' % tex +
'          <sampler2D>\n' +
'            <source>%s-surface</source>\n' % tex +
'          </sampler2D>\n' +
'        </newparam>\n')

#
#    writeMaterials(obj, fp, stuff):
#

def writeMaterials(obj, fp, stuff):
    (texname, texfile, matname) = object_collection.getTextureNames(stuff)
    if matname:
        matname = matname.replace(" ", "_")
        fp.write(
'    <material id="%s" name="%s">\n' % (matname, matname) +
'      <instance_effect url="#%s-effect"/>\n' % matname +
'    </material>\n')
    return

#
#    writeController(obj, fp, stuff):
#

def writeController(obj, fp, stuff):
    object_collection.setStuffSkinWeights(stuff)
    nVerts = len(stuff.meshInfo.verts)
    nUvVerts = len(stuff.meshInfo.uvValues)
    nNormals = nVerts
    nFaces = len(stuff.meshInfo.faces)
    nWeights = len(stuff.skinWeights)
    nBones = len(stuff.boneInfo.bones)
    nTargets = len(stuff.meshInfo.targets)
    (scale, unit) = the.Options["scale"]

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

    for b in stuff.boneInfo.bones:
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
    for b in stuff.boneInfo.bones:
        vec = stuff.boneInfo.heads[b]
        (x,y,z) = rotateLoc(vec, scale)
        mat[0][3] = -x
        mat[1][3] = -y
        mat[2][3] = -z
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
#    writeGeometry(obj, fp, stuff):
#
        
def writeGeometry(obj, fp, stuff):
    nVerts = len(stuff.meshInfo.verts)
    nUvVerts = len(stuff.meshInfo.uvValues)
    nNormals = nVerts
    nWeights = len(stuff.skinWeights)
    nBones = len(stuff.boneInfo.bones)
    nTargets = len(stuff.meshInfo.targets)
    (scale, unit) = the.Options["scale"]

    fp.write('\n' +
'    <geometry id="%sMesh" name="%s">\n' % (stuff.name,stuff.name) +
'      <mesh>\n' +
'        <source id="%s-Position">\n' % stuff.name +
'          <float_array count="%d" id="%s-Position-array">\n' % (3*nVerts,stuff.name) +
'          ')


    for v in stuff.meshInfo.verts:
        (x,y,z) = rotateLoc(v, scale)
        fp.write("%.4f %.4f %.4f " % (x,y,z))

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

    for no in stuff.meshInfo.vnormals:
        (x,y,z) = rotateLoc(no, scale)
        fp.write("%.4f %.4f %.4f " % (x,y,z))

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


    for uv in stuff.meshInfo.uvValues:
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
'        </vertices>\n')

    checkFaces(stuff, nVerts, nUvVerts)
    #writePolygons(fp, stuff)
    writePolylist(fp, stuff)
    
    fp.write(
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
            (x,y,z) = rotateLoc(v, scale)
            fp.write("%.4f %.4f %.4f " % (x,y,z))

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
#   writePolygons(fp, stuff):
#   writePolylist(fp, stuff):
#

def writePolygons(fp, stuff):
    fp.write(        
'        <polygons count="%d">\n' % len(stuff.meshInfo.faces) +
'          <input offset="0" semantic="VERTEX" source="#%s-Vertex"/>\n' % stuff.name +
'          <input offset="1" semantic="NORMAL" source="#%s-Normals"/>\n' % stuff.name +
'          <input offset="2" semantic="TEXCOORD" source="#%s-UV"/>\n' % stuff.name)

    for fc in stuff.meshInfo.faces:
        fp.write('          <p>')
        for vs in fc:
            v = vs[0]
            uv = vs[1]
            fp.write("%d %d %d " % (v, v, uv))
        fp.write('</p>\n')
    
    fp.write('\n' +
'        </polygons>\n')
    return

def writePolylist(fp, stuff):
    fp.write(        
'        <polylist count="%d">\n' % len(stuff.meshInfo.faces) +
'          <input offset="0" semantic="VERTEX" source="#%s-Vertex"/>\n' % stuff.name +
'          <input offset="1" semantic="NORMAL" source="#%s-Normals"/>\n' % stuff.name +
'          <input offset="2" semantic="TEXCOORD" source="#%s-UV"/>\n' % stuff.name +
'          <vcount>')

    for fc in stuff.meshInfo.faces:
        fp.write('%d ' % len(fc))

    fp.write('\n' +
'          </vcount>\n'
'          <p>')

    for fc in stuff.meshInfo.faces:
        for vs in fc:
            v = vs[0]
            uv = vs[1]
            fp.write("%d %d %d " % (v, v, uv))

    fp.write(
'          </p>\n' +
'        </polylist>\n')
    return

#
#   checkFaces(stuff, nVerts, nUvVerts):
#

def checkFaces(stuff, nVerts, nUvVerts):
    for fc in stuff.meshInfo.faces:
        for vs in fc:
            v = vs[0]
            uv = vs[1]
            if v > nVerts:
                raise NameError("v %d > %d" % (v, nVerts))
            if uv > nUvVerts:
                raise NameError("uv %d > %d" % (uv, nUvVerts))            
    return 
    
#
#    writeNode(obj, fp, pad, stuff):
#

def writeNode(obj, fp, pad, stuff):    
    fp.write('\n' +
'%s<node id="%sObject" name="%s">\n' % (pad, stuff.name,stuff.name) +
'%s  <translate sid="translate">0 0 0</translate>\n' % pad +
'%s  <rotate sid="rotateZ">0 0 1 0</rotate>\n' % pad +
'%s  <rotate sid="rotateY">0 1 0 0</rotate>\n' % pad +
'%s  <rotate sid="rotateX">1 0 0 0</rotate>\n' % pad+
#'%s  <scale sid="scale">1 1 1</scale>\n' % pad+
'%s  <instance_controller url="#%s-skin">\n' % (pad, stuff.name) +
'%s    <skeleton>#%s</skeleton>\n' % (pad, stuff.boneInfo.root))

    (texname, texfile, matname) = object_collection.getTextureNames(stuff)    
    if matname:
        matname = matname.replace(" ", "_")    
        fp.write(
'%s    <bind_material>\n' % pad +
'%s      <technique_common>\n' % pad +
'%s        <instance_material symbol="%s" target="#%s">\n' % (pad, matname, matname) +
'%s          <bind_vertex_input semantic="UVTex" input_semantic="TEXCOORD" input_set="0"/>\n' % pad +
'%s        </instance_material>\n' % pad +
'%s      </technique_common>\n' % pad +
'%s    </bind_material>\n' % pad)

    fp.write(
'%s  </instance_controller>\n' % pad +
'%s</node>\n' % pad)
    return

#
#    loadShapeKeys(tmplName):    
#    ShapeKey BrowsDown LR toggle&T_Face
#      sv 2139 0 0 -0.0109844
#

def loadShapeKeys(tmplName):
    tmpl = open(tmplName, "rU")
    if tmpl == None:
        log.warning("Cannot open template %s" % tmplName)
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

    

