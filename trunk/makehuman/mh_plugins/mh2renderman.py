#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Renderman Export functions

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements functions to export a human model in Renderman format and render it
using either the Aqsis or Renderman engine.

The MakeHuman data structures are transposed into renderman objects.

"""

__docformat__ = 'restructuredtext'

import os
import aljabr
import files3d
import subprocess
import hairgenerator
import random

hairsClass = hairgenerator.Hairgenerator()


def loadHairsFile(path):

    hairsClass.loadHairs(path)


    # TODO: add the loading of wavefront obj preview


def writeHairs(ribRepository, mesh):

    # Write the full hairstyle

    totalNumberOfHairs = 0
    hairsClass.humanVerts = mesh.verts
    hairsClass.adjustGuides()

    # hairsClass.generateHairStyle1()

    hairsClass.generateHairStyle2()
    print 'Writing hairs'
    hairName = os.path.join(ribRepository, 'hairs.rib')
    hairFile = open(hairName, 'w')
    for hSet in hairsClass.hairStyle:
        if 'clump' in hSet.name:
            hDiameter = hairsClass.hairDiameterClump * random.uniform(0.5, 1)
        else:
            hDiameter = hairsClass.hairDiameterMultiStrand * random.uniform(0.5, 1)
        hairFile.write('\t\tBasis "b-spline" 1 "b-spline" 1\n')
        

            
           
        
        for hair in hSet.hairs:
            totalNumberOfHairs += 1
            hairFile.write('Curves "cubic" [%i] "nonperiodic" "P" ['% len(hair.controlPoints))
            
            for cP in hair.controlPoints:
                hairFile.write('%s %s %s ' % (cP[0], cP[1], -cP[2]))  # z * -1 blender  to renderman coords
           
            if random.randint(0, 3) >= 1:
                hairFile.write(']\n"N" [') 
                for cP in hair.controlPoints:
                        hairFile.write('0 1 0 ')  # arbitrary normals  
            hairFile.write(']  "constantwidth" [%s]\n' % hDiameter)    
       
            
        
    hairFile.close()
    print 'Totals hairs written: ', totalNumberOfHairs
    print 'Number of tufts', len(hairsClass.hairStyle)


def writePolyObj(fileName, mesh, referenceFile=None):
    """
    NOTE: This function is a template and does not actually work.

    This function provides a template for the development of export and
    rendering functions.

    Parameters
    ----------

    fileName:
        *string*. The file system path to the output file that needs to be generated.

    mesh:
        *3D object*. The object to export.

    referenceFile:
        *string*. The file system path to a reference file.
    """

    if referenceFile:
        faces = files3d.loadFacesIndices(referenceFile)
        facesUVindices = files3d.loadUV(referenceFile)
    else:

        # facesUVindices = facesUV[0]
        # facesUVvalues = facesUV[1]

        faces = []
        for face in mesh.faces:
            faces.append(face.verts[0].idx, face.verts[1].idx, face.verts[2].idx)

    objFile = file(fileName, 'w')
    objFile.write('Declare "st" "facevarying float[2]"\n')
    objFile.write('PointsPolygons [')
    for face in faces:
        objFile.write('%i ' % len(face))

    objFile.write('] ')
    objFile.write('[')
    for face in faces:
        if len(face) == 3:
            objFile.write('%i %i %i ' % (face[0], face[1], face[2]))
        if len(face) == 4:
            objFile.write('%i %i %i %i ' % (face[0], face[1], face[2], face[3]))
    objFile.write(']')

    objFile.write('\n"P" [')
    for vert in mesh.verts:
        objFile.write('%f %f %f ' % (vert.co[0], vert.co[1], -vert.co[2]))
    objFile.write('] ')

    objFile.write(' "N" [')
    for vert in mesh.verts:
        objFile.write('%f %f %f ' % (vert.no[0], vert.no[1], -vert.no[2]))
    objFile.write(']')

    objFile.write('\n"Cs" [')
    for v in mesh.verts:
        objFile.write('%f %f %f ' % (v.color[0] / 255.0, v.color[1] / 255.0, v.color[2] / 255.0))
    objFile.write(']')

    objFile.write('\n"st" [')
    for faceUV in facesUVindices:
        for uvIdx in faceUV:
            uvValue = facesUVvalues[uvIdx]
            objFile.write('%s %s ' % (uvValue[0], 1 - uvValue[1]))
    objFile.write(']')

    objFile.write('\n')
    objFile.close()


def clamp(min, max, val):
    """
    This function clips a value so that it is no less and no greater than the
    minimum and maximum values specified.  This only works within the decimal
    accuracy limits of the comparison operation, so the returned value could be
    very slightly smaller or greater than the min and max values specified.

    Parameters
    ----------

    min:
        *decimal*. The minimum permitted value.

    max:
        *decimal*. The maximum permitted value.

    val:
        *decimal*. The value to be clipped.
    """

    if val > max:
        val = max
    if val < min:
        val = min
    return val



def sssColor(mesh, referenceFile, pointLightCoords, pointLightIntensity, refl = 0.5, sssSteps = 2):
    """
    ...

    """

    facesIndices = files3d.loadFacesIndices(referenceFile)
    facesColor = []
    vertsColor = []
    indicesProcessed = set()

    for v in mesh.verts:
        color = 0
        for (i, pointLightCoord) in enumerate(pointLightCoords):
            lightRay = aljabr.vsub(pointLightCoord, v.co)
            lightRay = aljabr.vnorm(lightRay)
            color += clamp(0, 1, aljabr.vdot(lightRay, v.no) * pointLightIntensity[i] * refl)
        vertsColor.append(color)
        
    sssIterations = [vertsColor]
    
    for n in range(sssSteps):
        colorsToScatter = sssIterations[-1]
        sssColors = []
        for v in mesh.verts:
            sharedColors = []
            scattering = 0
            for v2 in v.vertsShared():
                sharedColors.append(colorsToScatter[v2.idx])
                sharedColors.sort()
            if colorsToScatter[v.idx] < sharedColors[-1]:
                scattering = (colorsToScatter[v.idx] + sharedColors[-1])/2
            else:
                scattering = vertsColor[v.idx]
            sssColors.append(scattering)
        sssIterations.append(sssColors)
    vertsColorSSS = sssIterations[-1]

    for f in facesIndices:
        for idx in f:
            color = vertsColorSSS[idx[0]]
            facesColor.append(color)
    return facesColor


















































def writeSubdivisionMesh(fileName, mesh, referenceFile=None, group = None, vertColors = None):
    """
    This function exports a Renderman format object from the MakeHuman
    subdivided mesh object (smoothed).

    Parameters
    ----------

    fileName:
        *string*. The file system path to the output file that needs to be generated.

    mesh:
        *3D object*. The object to export.

    referenceFile:
        *string*. The file system path to a reference file (the wavefront
        base object).
    """

    if referenceFile and group:
        facesIndices = files3d.loadFacesIndices(referenceFile, True)
        facesUVvalues = mesh.uvValues  # files3d.loadUV(referenceFile)
    elif referenceFile:
        facesIndices = files3d.loadFacesIndices(referenceFile)
        facesUVvalues = mesh.uvValues  # files3d.loadUV(referenceFile)
    else:
        print 'Error: no reference file'

    if group != None:
        gFlag = False
        gFacesIndices = []
        for faceIdx in facesIndices:
            if isinstance(faceIdx, str):
                print faceIdx
                if faceIdx == group:
                    gFlag = True
                else:
                    gFlag = False
            if gFlag == True:
                if not isinstance(faceIdx, types.StringType):
                    gFacesIndices.append(faceIdx)

        facesIndices = gFacesIndices







    objFile = file(fileName, 'w')
    objFile.write('Declare "st" "facevarying float[2]"\n')
    objFile.write('Declare "Cs" "facevarying color"\n')
    objFile.write('SubdivisionMesh "catmull-clark" [')
    for faceIdx in facesIndices:
        objFile.write('%i ' % len(faceIdx))
    objFile.write('] ')

    objFile.write('[')
    for faceIdx in facesIndices:
        if len(faceIdx) == 3:
            objFile.write('%i %i %i ' % (faceIdx[0][0], faceIdx[1][0], faceIdx[2][0]))
        if len(faceIdx) == 4:
            objFile.write('%i %i %i %i ' % (faceIdx[0][0], faceIdx[1][0], faceIdx[2][0], faceIdx[3][0]))
    objFile.write(']')

    objFile.write('''
["interpolateboundary"] [0 0] [] []
"P" [''')
    for vert in mesh.verts:
        objFile.write('%f %f %f ' % (vert.co[0], vert.co[1], -vert.co[2]))
    objFile.write('] ')



    objFile.write('\n"st" [')
    for faceIdx in facesIndices:
        for idx in faceIdx:
            uvIdx = idx[1]
            uvValue = facesUVvalues[uvIdx]
            objFile.write('%s %s ' % (uvValue[0], 1 - uvValue[1]))
    objFile.write(']')



    objFile.write('\n"Cs" [')
    for color in vertColors:
        objFile.write('%s %s %s \n' % (color, color, color))
    objFile.write(']')
    objFile.write('\n')


    objFile.close()



def writeMainSceneFrame(scene, ribfile, ribRepository):
    """
    This function creates the frame definition for a Renderman scene.

    Parameters
    ----------

    scene:
        *scene3D*. The scene object.

    ribfile:
        *string*. The file system path to the output file that needs to be generated.

    ribRepository:
        *string*. The file system path to the rib repository.
    """

    cameraData = scene.getCameraSettings()
    yResolution = cameraData[6]
    xResolution = cameraData[7]
    fov = cameraData[5]
    locX = cameraData[0]
    locY = cameraData[1]
    zoom = cameraData[2]
    rotX = cameraData[3]
    rotY = cameraData[4]
    ribfile.write('FrameBegin 4\n')
    ribfile.write('Option "statistics" "endofframe" [1]\n')
    ribfile.write('Option "searchpath" "shader" "data/shaders/renderman:&"\n')
    ribfile.write('Option "searchpath" "texture" "data/textures:&"\n')
    ribfile.write('Projection "perspective" "fov" %f\n' % fov)
    ribfile.write('Format %s %s 1\n' % (xResolution, yResolution))
    ribfile.write('Clipping 0.1 100\n')
    ribfile.write('PixelSamples %s %s\n' % (2, 2))
    ribfile.write('ShadingRate %s \n' % 2)

    # ribfile.write('Sides 2\n')

    ribfile.write('Declare "lighttexture" "string"\n')
    ribfile.write('Declare "skintexture" "string"\n')
    ribfile.write('Declare "bumptexture" "string"\n')
    ribfile.write('Declare "shadowname" "string"\n')
    ribfile.write('Declare "blur" "float"\n')
    ribfile.write('Declare "falloff" "float"\n')
    ribfile.write('Display "00001.tif" "framebuffer" "rgb"\n')
    ribfile.write('Display "+rendering.tif" "file" "rgba"\n')
    ribfile.write('\t\tTranslate %s %s %s\n' % (locX, locY, zoom))
    ribfile.write('\t\tRotate %s 1 0 0\n' % -rotX)
    ribfile.write('\t\tRotate %s 0 1 0\n' % -rotY)
    ribfile.write('WorldBegin\n')
    ribfile.write('\tLightSource "ambientlight" 1 "intensity" [.05] "color lightcolor" [1 1 1]\n')
    ribfile.write('\tLightSource "shadowspot" 2 "shadowname" "%s" "from" [9.39 12.80 -25.80] "to" [0 0 0] "intensity" 600  "coneangle" [0.785] "blur" [0.005] "float width" [1]\n'
                   % (ribRepository + '/zmap.shad'))

    # ribfile.write('\tLightSource "spotlight" 2 "from" [2.39 10.64 -5] "to" [0 0 0] "intensity" 30  "coneangle" [1.0] \n')
    # ribfile.write('\tLightSource "spotlight" 3 "from" [-4.14 4.84 -7.45] "to" [0 0 0] "intensity" 35  "coneangle" [1.0]\n')

    for obj in scene.objects:
        name = obj.name
        if name == 'base.obj':  # TODO: attribute isRendered
            ribPath = os.path.join(ribRepository, name + '.rib')
            objPath = os.path.join('data/3dobjs', base.obj)

            lightMap = os.path.join(ribRepository, 'textures', name + '_map' + '.tif')

            ribfile.write('\tAttributeBegin\n')
            ribfile.write('\t\tColor [%s %s %s]\n' % (0.8, 0.8, 0.8))
            ribfile.write('\t\tOpacity [%s %s %s]\n' % (1, 1, 1))
            ribfile.write('\t\tTranslate %s %s %s\n' % (0, 0, 0))
            ribfile.write('\t\tRotate %s 0 0 1\n' % 0)
            ribfile.write('\t\tRotate %s 0 1 0\n' % 0)
            ribfile.write('\t\tRotate %s 1 0 0\n' % 0)
            ribfile.write('\t\tScale %s %s %s\n' % (1, 1, 1))
            writeSubdivisionMesh(ribPath, obj, objPath)
            ribfile.write('\t\tSurface "skin" "string opacitytexture" "%s" "string texturename" "%s" "string speculartexture" "%s" "string ssstexture" "%s" "float Ks" [.4] "float dark" [2]\n'
                           % ('texture_opacity.tif', 'texture.tif', 'texture_ref.tif', lightMap))
            ribfile.write('\t\tReadArchive "%s"\n' % ribPath)
            ribfile.write('\tAttributeEnd\n')

    ribfile.write('\tAttributeBegin\n')
    ribfile.write('\t\tDeclare "rootcolor" "color"\n')
    ribfile.write('\t\tDeclare "tipcolor" "color"\n')
    ribfile.write('\t\tSurface "hair" "rootcolor" [%s %s %s] "tipcolor" [%s %s %s]\n' % (hairsClass.rootColor[0], hairsClass.rootColor[1], hairsClass.rootColor[2],
                  hairsClass.tipColor[0], hairsClass.tipColor[1], hairsClass.tipColor[2]))

    ribfile.write('\t\tReadArchive "%s"\n' % os.path.join(ribRepository, 'hairs.rib'))
    ribfile.write('\tAttributeEnd\n')

    ribfile.write('WorldEnd\n')
    ribfile.write('FrameEnd\n')



def mh2Aqsis(camera, scene, fName, ribRepository):
    """
    This function creates the frame definition for a Renderman scene.

    Parameters
    ----------

    scene:
        *scene3D*. The scene object.

    ribfile:
        *string*. The file system path to the output file that needs to be generated.

    ribRepository:
        *string*. The file system path to the rib repository.
    """

    ribfile = file(fName, 'w')
    print 'RENDERING IN AQSIS'
    applicationPath = os.getcwd()  # TODO: this may not always return the app folder
    appTexturePath = os.path.join(applicationPath, 'data', 'textures')
    appObjectPath = os.path.join(applicationPath, 'data', '3dobjs')
    usrShaderPath = os.path.join(ribRepository, 'shaders')
    usrTexturePath = os.path.join(ribRepository, 'textures')
    shadowPath1 = os.path.join(ribRepository, 'zbuffer.tif')
    shadowPath2 = os.path.join(ribRepository, 'zmap.shad')

    xResolution, yResolution = scene.getWindowSize()
    human = scene.selectedHuman
    locX = human.getPosition()[0]
    locY = human.getPosition()[1]
    rotX = human.getRotation()[0]
    rotY = human.getRotation()[1]


    # These two list should be replaced by lights class in module3d.py

    pointLightCoords = [[-8, 10, 15], [1, 10, 15], [1, 15, -8], [-8, 0, 0]]
    pointLightIntensity = [.66, .26, .9, .13]
    #pointLightIntensity = [0, 0, 0, .9]
    ribfile.write('MakeTexture "%s" "%s" "periodic" "periodic" "box" 1 1\n' % (os.path.join(appTexturePath, 'texture.tif').replace('\\', '/'),
                  os.path.join(usrTexturePath, 'texture.texture').replace('\\', '/')))
    ribfile.write('MakeTexture "%s" "%s" "periodic" "periodic" "box" 1 1\n' % (os.path.join(appTexturePath, 'texture_ref.tif').replace('\\', '/'),
                  os.path.join(usrTexturePath, 'texture_ref.texture').replace('\\', '/')))

    # FINAL RENDERING

    ribfile.write('FrameBegin 1\n')
    ribfile.write('ScreenWindow -1.333 1.333 -1 1\n')
    ribfile.write('Option "statistics" "endofframe" [1]\n')
    ribfile.write('Option "searchpath" "shader" "%s:&"\n' % usrShaderPath.replace('\\', '/'))
    ribfile.write('Option "searchpath" "texture" "%s:&"\n' % usrTexturePath.replace('\\', '/'))
    ribfile.write('Projection "perspective" "fov" %f\n' % camera.fovAngle)
    ribfile.write('Format %s %s 1\n' % (xResolution, yResolution))
    ribfile.write('Clipping 0.1 100\n')
    ribfile.write('PixelSamples %s %s\n' % (2, 2))
    ribfile.write('ShadingRate %s \n' % 2)
    ribfile.write('Declare "refltexture" "string"\n')
    ribfile.write('Declare "skintexture" "string"\n')
    ribfile.write('Declare "bumptexture" "string"\n')
    ribfile.write('Declare "shadowname" "string"\n')
    ribfile.write('Declare "blur" "float"\n')
    ribfile.write('Declare "falloff" "float"\n')
    ribfile.write('Display "Final pass" "framebuffer" "rgb"\n')
    ribfile.write('Display "+%s" "file" "rgba"\n' % os.path.join(ribRepository, 'rendering.tif').replace('\\', '/'))
    ribfile.write('\t\tTranslate %s %s %s\n' % (camera.eyeX, -camera.eyeY, camera.eyeZ)) # Camera
    ribfile.write('\t\tTranslate %s %s %s\n' % (locX, locY, 0.0)) # Model
    ribfile.write('\t\tRotate %s 1 0 0\n' % -rotX)
    ribfile.write('\t\tRotate %s 0 1 0\n' % -rotY)
    ribfile.write('WorldBegin\n')
    ribfile.write('\tLightSource "ambientlight" 1 "intensity" [.02] "color lightcolor" [1 1 1]\n')

    # ribfile.write('\tLightSource "envlight" 1 "string filename" "data/textures/occlmap.sm" "float intensity" [ 0.9 ] "float samples" [ 32 ] "float blur" [ 0.025 ]\n')
    # ribfile.write('\tLightSource "pointlight" 2 "from" [%f %f %f] "intensity" 1000\n'%(spot1Pos[0],spot1Pos[1],spot1Pos[2]))
    # ribfile.write('\tLightSource "shadowspot" 2 "shadowname" "%s" "from" [%f %f %f] "to" [0 0 0] "intensity" 1000  "coneangle" [0.785] "blur" [0.005] "float width" [1]\n'%(ribRepository + "/zmap.shad",spot1Pos[0],spot1Pos[1],spot1Pos[2]))

    for i in range(len(pointLightCoords)):
        ribfile.write('\tLightSource "pointlight" %i  "from" [%f %f %f] "intensity" %f\n' % (i, pointLightCoords[i][0], pointLightCoords[i][1], -pointLightCoords[i][2],
                      pointLightIntensity[i] * 75))

        # note z has the negative sign of renderman light because opengl->renderman
        # factor 75 is just an empirical. TODO: modify it in proportion of light distance

    headCentr = [0, 0, 0]
    for obj in scene.objects:
        name = obj.name
        if name == 'base.obj':  # TODO: attribute isRendered
            ribPath = os.path.join(ribRepository, name + '.rib')
            objPath = os.path.join('data/3dobjs', 'base.obj')

            vcolors = sssColor(obj, objPath, pointLightCoords, pointLightIntensity)

            ribfile.write('\tAttributeBegin\n')
            ribfile.write('\t\tColor [%s %s %s]\n' % (0.8, 0.8, 0.8))
            ribfile.write('\t\tOpacity [%s %s %s]\n' % (1, 1, 1))
            ribfile.write('\t\tTranslate %s %s %s\n' % (0, 0, 0))
            ribfile.write('\t\tRotate %s 0 0 1\n' % 0)
            ribfile.write('\t\tRotate %s 0 1 0\n' % 0)
            ribfile.write('\t\tRotate %s 1 0 0\n' % 0)
            ribfile.write('\t\tScale %s %s %s\n' % (1, 1, 1))
            #writeSubdivisionMesh(ribPath, obj, objPath, "l-eye-ball")
            writeSubdivisionMesh(ribPath, obj, objPath, vertColors = vcolors)
#Surface "skin2" "string texturename" "texture.tif"
            ribfile.write('\t\tSurface "skin" "skintexture" "%s" "string refltexture" "%s" "float Ks" [2.5] \n'% ('texture.texture','texture_ref.texture'))
            #ribfile.write('\t\tSurface "constant"')
            ribfile.write('\t\tReadArchive "%s"\n' % ribPath.replace('\\', '/'))
            ribfile.write('\tAttributeEnd\n')
            writeHairs(ribRepository, obj)


    ribfile.write('\tAttributeBegin\n')
    ribfile.write('\tReverseOrientation #<<-- required\n')
    ribfile.write('\t\tColor [%f %f %f]\n' % (scene.selectedHuman.hairColor[0], scene.selectedHuman.hairColor[1], scene.selectedHuman.hairColor[2]))
    ribfile.write('\t\tSurface "hair" "float Kd" [8] "float Ks" [8] \n')
    ribfile.write('\t\tReadArchive "%s"\n' % os.path.join(ribRepository, 'hairs.rib').replace('\\', '/'))
    ribfile.write('\tAttributeEnd\n')
    ribfile.write('WorldEnd\n')
    ribfile.write('FrameEnd\n')
    ribfile.close()

def saveScene(camera, scene, fName, ribDir, engine):
    """
    This function exports a Renderman format scene and then invokes either
    Aqsis or Renderman to render it.

    Parameters
    ----------

    scene:
        *scene3D*. The scene object.

    fName:
        *string*. The file system path to the output file that needs to be generated.

    ribDir:
        *string*. The file system path to the rib directory.

    engine:
        *string*. A text string indicating whether Aqsis or Renderman
        should be used to render the exported file.

    """

    loadHairsFile(scene.selectedHuman.hairFile)
    if not os.path.isdir(ribDir):
        os.makedirs(ribDir)
    ribRepository = os.path.join(ribDir, 'ribFiles')
    usrTexturePath = os.path.join(ribRepository, 'textures')

    if not os.path.isdir(ribRepository):
        os.makedirs(ribRepository)
    if not os.path.isdir(usrTexturePath):
        os.makedirs(usrTexturePath)
    fName = os.path.join(ribDir, fName)

    # ribfile = file(fName,'w')
    # writeShadowScene(scene, ribfile, ribRepository)

    if engine == 'aqsis':
        mh2Aqsis(camera, scene, fName, ribRepository)
    if engine == 'pixie':
        print 'write pixie'
        mh2Pixie(scene, fName, ribRepository)
    if engine == '3delight':
        mh23delight(scene, fName, ribRepository)
    if engine == 'aqsis':
        command = '%s "%s"' % ('aqsis -progress', fName)
    if engine == 'pixie':
        command = '%s %s' % ('rndr', fName)
    if engine == '3delight':
        command = '%s %s' % ('renderdl', fName)

    print 'COMMAND', command
    subprocess.Popen(command, shell=True)


