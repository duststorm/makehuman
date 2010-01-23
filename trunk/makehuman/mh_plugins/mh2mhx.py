#!/usr/bin/python
# -*- coding: utf-8 -*-

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
MakeHuman to MHX (MakeHuman eXchange format) exporter. MHX files can be loaded into
Blender by mhx_import.py.

TO DO

"""

import module3d
import aljabr
import mh
import files3d
import mh2bvh
import mhxbones
import os

#
# ....exportMhx(obj, filename):
#


def exportMhx(obj, filename):
    print 'Writing MHX file'
    fp = open(filename, 'w')
    mhxFile = 'data/3dobjs/mhxbase.mhx'
    try:
        print 'Trying to open ' + mhxFile
        tmpl = open(mhxFile, 'r')
    except:
        print 'Failed to open ' + mhxFile
        tmpl = None
    if tmpl:
        exportFromMhxTemplate(obj, tmpl, fp)
        print mhxFile + ' closed'
    else:
        exportRawMesh(obj, fp)
        exportArmature(obj, fp)
    fp.close()
    print 'MHX file written'
    return


def exportRawData(obj, fp):

    # Ugly klugdy fix of extra vert

    x1 = aljabr.vadd(obj.verts[11137].co, obj.verts[11140].co)
    x2 = aljabr.vadd(obj.verts[11162].co, obj.verts[11178].co)
    x = aljabr.vadd(x1, x2)
    obj.verts[14637].co = aljabr.vmul(x, 0.25)

    # end ugly kludgy

    for v in obj.verts:
        fp.write('v %f %f %f ;\n' % (v.co[0], v.co[1], v.co[2]))

    for uv in obj.uvValues:
        fp.write('vt %f %f ;\n' % (uv[0], uv[1]))

    faces = files3d.loadFacesIndices('data/3dobjs/base.obj')
    for f in faces:
        fp.write('f')
        for v in f:
            fp.write(' %i/%i ' % (v[0], v[1]))
        fp.write(';\n')


def exportRawMesh(obj, fp):
    fp.write('''# MakeHuman exported MHX
# www.makehuman.org
MHX 0 3 ;

''')

    fp.write("""if useMesh 
\
mesh Human Human 
""")
    exportRawData(obj, fp)
    fp.write("""end mesh
\

object Human Mesh Human 
\
\tlayers 1 0 ;
\
end object
\
end useMesh
""")
    return


#
# ....exportArmature(obj, fp):
#


def exportArmature(obj, fp):
    mhxbones.writeJoints(obj, fp)
    fp.write('''
armature HumanRig HumanRig
''')
    mhxbones.writeBones(obj, fp)
    fp.write("""\tlayerMask 0x101 ;
\
\tautoIK false ;
\
\tdelayDeform false ;
\
\tdrawAxes false ;
\
\tdrawNames false ;
\
\tenvelopes false ;
\
\tmirrorEdit true ;
\
\trestPosition false ;
\
\tvertexGroups true ;
\
end armature
""")

    fp.write('''
pose HumanRig
''')
    mhxbones.writePose(obj, fp)
    fp.write('end pose\n')

    fp.write("""
\
object HumanRig Armature HumanRig 
\
\tlayers 1 0 ;
\
\txRay true ;
\
end object
""")

    # mhxbones.writeEmpties(fp)

    return exportArmature


#
# ....exportFromMhxTemplate(obj, tmpl, fp):
#

splitLeftRight = True


def exportFromMhxTemplate(obj, tmpl, fp):
    global splitLeftRight

    inZone = False
    skip = False
    lineNo = 0
    mainMesh = False

    for line in tmpl:
        lineNo += 1
        lineSplit = line.split()
        skipOne = False

        if len(lineSplit) == 0:
            pass
        elif lineSplit[0] == 'end':
            if lineSplit[1] == 'object' and mainMesh:
                fp.write('end if\n')
                mainMesh = False
            elif lineSplit[1] == 'mesh' and mainMesh:
                fp.write('end if\n')
                mainMesh = False
                inZone = False
                skip = False
            elif lineSplit[1] == 'armature' or lineSplit[1] == 'pose':
                mainMesh = False
                inZone = False
                skip = False
                skipOne = True
            elif lineSplit[1] == 'shapekey':
                if 0 and shapekey != 'Basis' and shapekey != 'Smile' and shapekey != 'Narrow' and shapekey != 'MouthOpen':
                    pass
                elif leftRightKey[shapekey] and splitLeftRight:
                    writeShapeKey(fp, shapekey + '_L', shapeVerts, 'Left', sliderMin, sliderMax)
                    writeShapeKey(fp, shapekey + '_R', shapeVerts, 'Right', sliderMin, sliderMax)
                else:
                    writeShapeKey(fp, shapekey, shapeVerts, 'None', sliderMin, sliderMax)
                skip = False
                skipOne = True
            elif lineSplit[1] == 'ipo':
                skip = False
                skipOne = True
        elif lineSplit[0] == 'mesh' and lineSplit[1] == 'Human':
            inZone = True
            mainMesh = True
            exportArmature(obj, fp)
            fp.write('if useMesh\n')
        elif lineSplit[0] == 'object' and lineSplit[1] == 'Human':
            mainMesh = True
            fp.write('if useMesh\n')
        elif lineSplit[0] == 'armature' and lineSplit[2] == 'HumanRig':
            skip = True
        elif lineSplit[0] == 'pose' and lineSplit[1] == 'HumanRig':
            skip = True
        elif lineSplit[0] == 'v' and inZone:
            if not skip:
                exportRawData(obj, fp)
                skip = True
        elif lineSplit[0] == 'f' and skip:
            skip = False
            skipOne = True
        elif lineSplit[0] == 'shapekey' and mainMesh:
            shapekey = lineSplit[1]
            sliderMin = lineSplit[2]
            sliderMax = lineSplit[3]
            shapeVerts = []
            skip = True
        elif lineSplit[0] == 'sv' and skip:
            shapeVerts.append(line)
        elif lineSplit[0] == 'ipo' and mainMesh:
            writeIpo(fp)
            skip = True
        elif lineSplit[0] == 'filename':
            (path, filename) = os.path.split(lineSplit[1])

            # texPath = mh.getPath("textures")

            MHpath = os.path.realpath('.')
            fp.write('  filename %s ;\n' % (MHpath + '/data/textures/' + filename))
            skipOne = True

        if not (skip or skipOne):
            fp.write(line)

    return


#
# ....leftRightKey - True if shapekey comes in two parts
#

leftRightKey = dict({'Basis': False, 'BendElbowForward': True, 'BendHeadForward': False, 'BendKneeBack': True, 'BendLegBack': True, 'BendLegForward': True, 'BrowsDown'
                    : True, 'BrowsMidDown': False, 'BrowsMidUp': False, 'BrowsOutUp': True, 'BrowsSqueeze': False, 'CheekUp': True, 'Frown': True, 'UpLidDown': True,
                    'LoLidUp': True, 'Narrow': True, 'ShoulderDown': True, 'Smile': True, 'Sneer': True, 'Squint': True, 'TongueOut': False, 'ToungeUp': False,
                    'ToungeLeft': False, 'ToungeRight': False, 'UpLipUp': True, 'LoLipDown': True, 'MouthOpen': False, 'UpLipDown': True, 'LoLipUp': True})

#
# ....writeShapeKey(fp, shapekey, shapeVerts, vgroup, sliderMin, sliderMax):
#


def writeShapeKey(fp, shapekey, shapeVerts, vgroup, sliderMin, sliderMax):
    fp.write('shapekey %s %s %s %s\n' % (shapekey, sliderMin, sliderMax, vgroup))
    for line in shapeVerts:
        fp.write(line)
    fp.write('end shapekey\n')


#
# ....writeIcu(fp, shape, expr):
#


def writeIcu(fp, shape, expr):
    fp.write("""\ticu %s 0 1
 \
\t\tdriver 2 ;
\
\t\tdriverObject _object['Human'] ;
\
\t\tdriverChannel 1 ;
\
\t\tdriverExpression '%s' ;
\
\tend icu
""" % (shape,
             expr))


def writeIpo(fp):
    global splitLeftRight

    mhxFile = 'data/3dobjs/mhxipos.mhx'
    try:
        print 'Trying to open ' + mhxFile
        tmpl = open(mhxFile, 'r')
    except:
        print 'Failed to open ' + mhxFile
        tmpl = None

    if tmpl and splitLeftRight:
        for line in tmpl:
            fp.write(line)
    else:
        fp.write('ipo Key KeyIpo\n')
        for (shape, lr) in leftRightKey.items():
            if shape == 'Basis':
                pass
            elif lr and splitLeftRight:
                writeIcu(fp, shape + '_L', 'p.ctrl' + shape + '_L()')
                writeIcu(fp, shape + '_R', 'p.ctrl' + shape + '_R()')
            else:
                writeIcu(fp, shape, 'p.ctrl' + shape + '()')
        fp.write('end ipo\n')

    if tmpl:
        print mhxFile + ' closed'
        tmpl.close()


