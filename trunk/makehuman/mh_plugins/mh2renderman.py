"""
Renderman Export functions

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni

**Copyright(c):**      MakeHuman Team 2001-2009

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
    #TODO: add the loading of wavefront obj preview



def writeHairs(ribRepository, mesh):

    totalNumberOfHairs = 0
    hairsClass.humanVerts = mesh.verts
    hairsClass.adjustGuides()
    hairsClass.generateHairStyle1()
    hairsClass.generateHairStyle2()
    print "Writing hairs"
    hairName = "%s/hairs.rib"%(ribRepository)
    hairFile = open(hairName,'w')
    for hSet in hairsClass.hairStyle:
        if "clump" in hSet.name:
            hDiameter = hairsClass.hairDiameterClump*random.uniform(0.5,1)
        else:
            hDiameter = hairsClass.hairDiameterMultiStrand*random.uniform(0.5,1)        
        hairFile.write('\t\tBasis "b-spline" 1 "b-spline" 1  ')
        hairFile.write('Curves "cubic" [')
        for hair in hSet.hairs:
            totalNumberOfHairs += 1
            hairFile.write('%i ' % len(hair.controlPoints))
        hairFile.write('] "nonperiodic" "P" [')
        for hair in hSet.hairs:
            for cP in hair.controlPoints:
                hairFile.write("%s %s %s " % (cP[0],cP[1],-cP[2]))
        hairFile.write(']  "constantwidth" [%s]\n' % (hDiameter))
    hairFile.close()
    print "Totals hairs written: ",totalNumberOfHairs
    print "Number of tufts",len(hairsClass.hairStyle)




def writePolyObj(fileName, mesh, referenceFile = None):
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
        facesUV = files3d.loadUV(referenceFile)
        facesUVindices = facesUV[0]
        facesUVvalues = facesUV[1]
    else:
        faces = []
        for face in mesh.faces:
            faces.append(face.verts[0].idx,face.verts[1].idx,face.verts[2].idx)


    objFile = file(fileName,'w')
    objFile.write('Declare "st" "facevarying float[2]"\n')
    objFile.write("PointsPolygons [")
    for face in faces:
        objFile.write('%i '%(len(face)))


    objFile.write("] ")
    objFile.write("[")
    for face in faces:
            if len(face) == 3:
                objFile.write('%i %i %i ' %(face[0],face[1],face[2]))
            if len(face) == 4:
                objFile.write('%i %i %i %i ' %(face[0],face[1],face[2],face[3]))
    objFile.write("]")

    """
    OpenGL use a coordinate system where in a front view Y is up,
    Z points into the camera and X points to the right (right-handed coordinate system). RenderMan uses a
    system where Y is up, Z points away from the camera and X points to the
    right (left-handed coordinate system).
    """
    objFile.write('\n"P" [')
    for vert in mesh.verts:
        objFile.write("%f %f %f " % (vert.co[0], vert.co[1], -vert.co[2]))
    objFile.write('] ')


    objFile.write(' "N" [')
    for vert in mesh.verts:
        objFile.write("%f %f %f " % (vert.no[0], vert.no[1], -vert.no[2]))
    objFile.write(']')


    objFile.write('\n"Cs" [')
    for v in mesh.verts:
        objFile.write('%f %f %f ' % (v.color[0]/255.0, v.color[1]/255.0, v.color[2]/255.0))
    objFile.write(']')


    objFile.write('\n"st" [')
    for faceUV in facesUVindices:
        for uvIdx in faceUV:
            uvValue = facesUVvalues[uvIdx]
            objFile.write('%s %s ' % (uvValue[0], 1-uvValue[1]))
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

def writeLightMapObj(fileName, mesh, referenceFile):
    """
    This function exports a Renderman format object that can be used as a
    light map in the rendering engine.

    A light map is a bake texture with light information already assigned
    to it.
    To enable this light map to be rendered without using a Renderman
    implementation (which is not standard practice and needs to be done in
    very different ways on different engines) we build a flattened mesh
    using the U,V coordinates as X,Y coordinates. Then we assign to each
    vertex a color calculated as pointLightCoord (in practice, this is used
    as a matte shader).
    This light map is very important as, by blurring it, we can quickly
    produce sub-surface scattering (SSS).

    Internally MakeHuman represents all objects as triangles, but
    for rendering it is better to use quads. So to export the rib we
    retrieve the face indices from the original wavefront object file
    (the reference file).

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

    objFile = file(fileName,'w')

    facesIndices = files3d.loadFacesIndices(referenceFile)
    facesUVvalues = mesh.uvValues #files3d.loadUV(referenceFile)

    facesUVcolor = []

    for i in range(len(facesUVvalues)):
        facesUVcolor.append(0)

    #These two list should be replaced by lights class in module3d.py
    pointLightCoords = [[-8, 5, -15],[8, 5, 15]]
    pointLightIntensity = [1, 1]

    indicesProcessed = set()
    for faceIndices in facesIndices:
        for idx in faceIndices:
            vertId = idx[0]
            uvId = idx[1]
            if uvId not in indicesProcessed:
                color = facesUVcolor[uvId]
                v = mesh.verts[vertId]
                for i,pointLightCoord in enumerate(pointLightCoords):
                    lightRay = aljabr.vsub(pointLightCoord,v.co)
                    lightRay = aljabr.vnorm(lightRay)
                    color += clamp(0, 1, aljabr.vdot(lightRay,v.no)*pointLightIntensity[i])
                facesUVcolor[uvId] = color
                indicesProcessed.add(uvId)

    objFile.write("PointsPolygons ");

    #Writing polygon n faces
    objFile.write("[ ")
    for face in facesIndices:
        objFile.write('%s '%(len(face)))
    objFile.write("] \n")

    #Writing face indices. Note we use UV indices as vert indices
    objFile.write("[ ")
    for face in facesIndices:
        for idx in face:
            objFile.write('%s ' % idx[1])
    objFile.write("] \n")

    #Writing verts coords. Note we use uv coords, as verts coords
    objFile.write('"P" [')
    for uv in facesUVvalues:
        objFile.write("%s %s %s \n" % (uv[0], uv[1], 0))
    objFile.write('] ')

    #Writing verts color. We use a simple Goraud matte
    objFile.write('\n"Cs" [')

    for color in facesUVcolor:
        objFile.write('%s %s %s \n' % (0, 0, color))
    objFile.write(']')

    objFile.write('\n')
    objFile.close()




def writeSubdivisionMesh(fileName, mesh, referenceFile = None):
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

    if referenceFile:
        facesIndices = files3d.loadFacesIndices(referenceFile)
        facesUVvalues = mesh.uvValues #files3d.loadUV(referenceFile)
    else:
        print "Error: no reference file"

    objFile = file(fileName,'w')
    objFile.write('Declare "st" "facevarying float[2]"\n')
    objFile.write('SubdivisionMesh "catmull-clark" [')
    for faceIdx in facesIndices:
        objFile.write('%i '%(len(faceIdx)))
    objFile.write("] ")

    objFile.write("[")
    for faceIdx in facesIndices:
            if len(faceIdx) == 3:
                objFile.write('%i %i %i ' %(faceIdx[0][0],faceIdx[1][0],faceIdx[2][0]))
            if len(faceIdx) == 4:
                objFile.write('%i %i %i %i ' %(faceIdx[0][0],faceIdx[1][0],faceIdx[2][0],faceIdx[3][0]))
    objFile.write("]")


    """
    OpenGL use a coordinate system where in a front view Y is up,
    Z points into the camera and X points to the right (right-handed coordinate system). RenderMan uses a
    system where Y is up, Z points away from the camera and X points to the
    right (left-handed coordinate system).
    """
    objFile.write('\n["interpolateboundary"] [0 0] [] []\n"P" [')
    for vert in mesh.verts:
        objFile.write("%f %f %f " % (vert.co[0], vert.co[1], -vert.co[2]))
    objFile.write('] ')


    """
    objFile.write('\n"Cs" [')
    for v in mesh.verts:
        objFile.write('%f %f %f ' % (v.color[0]/255.0, v.color[1]/255.0, v.color[2]/255.0))
    objFile.write(']')
    """

    objFile.write('\n"st" [')
    for faceIdx in facesIndices:
        for idx in faceIdx:
            uvIdx = idx[1]
            uvValue = facesUVvalues[uvIdx]
            objFile.write('%s %s ' % (uvValue[0], 1-uvValue[1]))
    objFile.write(']')


    objFile.write('\n')
    objFile.close()


def writeLightMapFrameLowRes(scene, ribfile, ribRepository):
    """
    This function creates a special scene, with only one 2d obect, obtained
    projecting the UV on the x,y plane. The rendering result is then used
    as lightmap.
    This is a workaround for a quick texture baking, but the
    resulting map is lowres because the bake is
    done using just the verts, without subdivision, without displacement
    and without interpolation.

    Parameters
    ----------

    ribfile:
        *string*. The file system path to the output file that needs to be generated.

    scene:
        *scene3D*. The scene object.

    ribRepository:
        *string*. The file system path to the rib repository.
    """
    for obj in scene.objects:
        name = obj.name
        if name == "base.obj": #TODO: attribute haveSSS

            ribPath = ribRepository + "/" + name +"_map"+ ".rib"
            objPath = "data/3dobjs/" + "base.obj"
            mapPath = ribRepository + "/" + name +"_map"+ ".tif"
            texturePath = ribRepository + "/" + name +"_map"+ ".tx"

            ribfile.write("FrameBegin 1\n")
            ribfile.write("Projection \"orthographic\"")
            ribfile.write("Option \"searchpath\" \"shader\" \"data/shaders/renderman:&\"\n")
            ribfile.write("Format %s %s 1\n" % (800, 400))
            ribfile.write("PixelFilter \"gaussian\" %s %s \n" % (3, 3))
            ribfile.write("PixelSamples %s %s\n"%(1,1))
            ribfile.write("Sides 2\n")
            ribfile.write("Display \"%s\" \"file\" \"rgba\"\n" % (mapPath))
            ribfile.write("Display \"+light_map\" \"framebuffer\" \"rgb\"\n")
            ribfile.write("\t\tScale %s %s %s\n" %(4,2,2))
            ribfile.write("\t\tTranslate %s %s %s\n" %(-0.5, -0.5, 1))
            ribfile.write('WorldBegin\n')
            ribfile.write('\tAttributeBegin\n')
            writeLightMapObj(ribPath, obj, objPath)
            ribfile.write('\tSurface "onlyci"\n')
            ribfile.write('\t\tReadArchive "%s"\n' %("data/3dobjs/quad.obj.rib"))
            ribfile.write('\tSurface "onlyci"\n')
            ribfile.write('\t\tReadArchive "%s"\n' %(ribPath))
            ribfile.write('\tAttributeEnd\n')
            ribfile.write("WorldEnd\n")
            ribfile.write("FrameEnd\n")
            ribfile.write("MakeTexture \"%s\" \"%s\" \"periodic\" \"periodic\" \"gaussian\" 1 1\n" % (mapPath,texturePath))

def writeLightMapFrameAqsis(scene, ribfile, ribRepository):
    """
    This function creates the frame definition to make an accurate
    texture baking using Aqsis. The resulting rendering is then used as lightmap.

    Parameters
    ----------

    #TODO Parameters
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
    ribfile.write("FrameBegin 1\n")
    ribfile.write("Option \"searchpath\" \"shader\" \"data/shaders/aqsis:&\"\n")
    ribfile.write("Option \"searchpath\" \"texture\" \"data/textures:&\"\n")
    ribfile.write("Projection \"perspective\" \"fov\" %f\n"%(fov))
    ribfile.write('Format %s %s 1\n' % (xResolution, yResolution))
    ribfile.write("Clipping 0.1 100\n")
    ribfile.write('PixelSamples %s %s\n'%(1,1))
    ribfile.write('ShadingRate %s \n'%(0.5))
    ribfile.write('Sides 2\n')
    ribfile.write('Display "baking sss" "framebuffer" "rgba"\n')
    ribfile.write("\t\tTranslate %s %s %s\n" %(locX, locY, zoom))
    ribfile.write("\t\tRotate %s 1 0 0\n" %(-rotX))
    ribfile.write("\t\tRotate %s 0 1 0\n" %(-rotY))
    ribfile.write('WorldBegin\n')
    ribfile.write('\tLightSource "ambientlight" 1 "intensity" [.05] "color lightcolor" [1 1 1]\n')
    ribfile.write('\tLightSource "spotlight" 2 "from" [2.39 10.64 -5] "to" [0 0 0] "intensity" 30  "coneangle" [1.0] \n')
    ribfile.write('\tLightSource "spotlight" 3 "from" [-4.14 4.84 -7.45] "to" [0 0 0] "intensity" 35  "coneangle" [1.0]\n')
    

	
	
    for obj in scene.objects:
        name = obj.name
        if name == "base.obj":  #TODO: attribute isRendered
            ribPath = ribRepository + "/" + name + ".rib"
            objPath = "data/3dobjs/" + "base.obj"

            bakePath = ribRepository + "/" + name +"_map"+ ".bake"
            lightMapTmp = ribRepository + "/" + name +"_map"+ ".tx"
            lightMapFinal = ribRepository + "/" + name +"_map"+ ".tif"
            colorTexture = "texture.tif"


            ribfile.write('\tAttributeBegin\n')
            ribfile.write("\t\tOrientation \"inside\"\n")
            ribfile.write("\t\tColor [%s %s %s]\n" %(0.8, 0.8, 0.8))
            ribfile.write("\t\tOpacity [%s %s %s]\n" %(1,1,1))
            ribfile.write("\t\tTranslate %s %s %s\n" %(0,0,0))
            ribfile.write("\t\tRotate %s 0 0 1\n" %(0))
            ribfile.write("\t\tRotate %s 0 1 0\n" %(0))
            ribfile.write("\t\tRotate %s 1 0 0\n" %(0))
            ribfile.write("\t\tScale %s %s %s\n" %(1,1,1))
            writeSubdivisionMesh(ribPath, obj, objPath)
            ribfile.write('\t\tSurface "lightmap" "string texturename" "%s" "string outputtexture" "%s"\n' % (colorTexture,bakePath))
            #ribfile.write('\t\tDisplacement "skinbump" "bumptexture" "data/textures/texture_bump.tif" "float Km" [.0025] \n')
            ribfile.write('\t\tReadArchive "%s"\n' %(ribPath))
            ribfile.write('\tAttributeEnd\n')
    ribfile.write("WorldEnd\n")
    ribfile.write("FrameEnd\n")
    ribfile.write('MakeTexture "%s" "%s" "periodic" "periodic" "box" 1 1 "float bake" 1024\n'%(bakePath, lightMapTmp))

    ribfile.write("FrameBegin 2\n")
    ribfile.write("Option \"searchpath\" \"shader\" \"data/shaders/renderman:&\"\n")
    ribfile.write("Option \"searchpath\" \"texture\" \"data/textures:&\"\n")
    #ribfile.write("DisplayChannel \"varying color Col1\"\n")
    ribfile.write("Display \"%s\" \"file\" \"rgb\"\n"%(lightMapFinal))
    ribfile.write("Display \"+light map\" \"framebuffer\" \"rgb\"\n")
    ribfile.write("Format 1024 512 1\n")
    ribfile.write("PixelSamples 2 2\n")
    #ribfile.write("PixelFilter \"gaussian\" 6 6\n")
    ribfile.write("ShadingInterpolation \"smooth\"\n")
    ribfile.write("Projection \"orthographic\"\n")
    ribfile.write("\tWorldBegin\n")
    ribfile.write("\tSides 2\n")
    ribfile.write("\tAttributeBegin\n")
    ribfile.write("\tColor [ 1 1 1 ]")
    ribfile.write("\tSurface \"scatteringtexture\" \"string texturename\" \"%s\" \"float scattering\" [1] \n"%(lightMapTmp))
    ribfile.write("\tTranslate 0 0 0.02\n")
    ribfile.write("\tPolygon \"P\" [ -2 -1 0   2 -1 0   2 1 0  -2 1 0 ]\"st\" [ 0 1  1 1  1 0  0 0  ]\n")
    ribfile.write("\tAttributeEnd\n")
    ribfile.write("WorldEnd\n")
    ribfile.write("FrameEnd\n")








def writeLightMapFramePixie(scene, ribfile, ribRepository):
    """
    This function creates the frame definition to make an accurate
    texture baking using Aqsis. The resulting rendering is then used as lightmap.

    Parameters
    ----------

    #TODO Parameters
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
    ribfile.write("FrameBegin 1\n")
    ribfile.write("Option \"searchpath\" \"shader\" \"data/shaders/pixie:&\"\n")
    ribfile.write("Option \"searchpath\" \"texture\" \"data/textures:&\"\n")
    ribfile.write("Projection \"perspective\" \"fov\" %f\n"%(fov))
    ribfile.write('Format %s %s 1\n' % (xResolution, yResolution))
    ribfile.write("Clipping 0.1 100\n")
    ribfile.write('PixelSamples %s %s\n'%(1,1))
    ribfile.write('ShadingRate %s \n'%(2))
    ribfile.write('Sides 2\n')
    ribfile.write('Display "baking sss" "framebuffer" "rgba"\n')
    ribfile.write("\t\tTranslate %s %s %s\n" %(locX, locY, zoom))
    ribfile.write("\t\tRotate %s 1 0 0\n" %(-rotX))
    ribfile.write("\t\tRotate %s 0 1 0\n" %(-rotY))
    ribfile.write('DisplayChannel "varying color BakeCol" \n')
    ribfile.write('WorldBegin\n')
    ribfile.write('\tLightSource "ambientlight" 1 "intensity" [.05] "color lightcolor" [1 1 1]\n')
    ribfile.write('\tLightSource "spotlight" 2 "from" [2.39 10.64 -5] "to" [0 0 0] "intensity" 30  "coneangle" [1.0] \n')
    ribfile.write('\tLightSource "spotlight" 3 "from" [-4.14 4.84 -7.45] "to" [0 0 0] "intensity" 35  "coneangle" [1.0]\n')

    for obj in scene.objects:
        name = obj.name
        if name == "base.obj":  #TODO: attribute isRendered
            ribPath = ribRepository + "/" + name + ".rib"
            objPath = "data/3dobjs/" + "base.obj"
            bakePath = ribRepository + "/" + name +"_map"+ ".ptc"
            lightMapFinal = ribRepository + "/" + name +"_map"+ ".tif"

            ribfile.write('\tAttributeBegin\n')
            ribfile.write("\t\tOrientation \"inside\"\n")
            ribfile.write("\t\tColor [%s %s %s]\n" %(0.8, 0.8, 0.8))
            ribfile.write("\t\tOpacity [%s %s %s]\n" %(1,1,1))
            ribfile.write("\t\tTranslate %s %s %s\n" %(0,0,0))
            ribfile.write("\t\tRotate %s 0 0 1\n" %(0))
            ribfile.write("\t\tRotate %s 0 1 0\n" %(0))
            ribfile.write("\t\tRotate %s 1 0 0\n" %(0))
            ribfile.write("\t\tScale %s %s %s\n" %(1,1,1))
            writeSubdivisionMesh(ribPath, obj, objPath)
            ribfile.write('\t\tSurface "lightmap" "pointcloudname" "%s" "string texturename" "%s" "bumptexture" ""\n' % (bakePath,"texture.tif"))
            ribfile.write('\t\tReadArchive "%s"\n' %(ribPath))
            ribfile.write('\tAttributeEnd\n')
    ribfile.write("WorldEnd\n")
    ribfile.write("FrameEnd\n")


    ribfile.write("FrameBegin 2\n")
    ribfile.write("Option \"searchpath\" \"shader\" \"data/shaders/pixie:&\"\n")
    ribfile.write("Option \"searchpath\" \"texture\" \"data/textures:&\"\n")
    ribfile.write("DisplayChannel \"varying color Col1\"\n")
    ribfile.write("Display \"%s\" \"file\" \"rgb\"\n"%(lightMapFinal))
    ribfile.write("Display \"+light map\" \"framebuffer\" \"rgb\"\n")
    ribfile.write("Format 1024 512 1\n")
    ribfile.write("PixelSamples 2 2")
    ribfile.write("PixelFilter \"gaussian\" 6 6\n")
    ribfile.write("ShadingInterpolation \"smooth\"\n")
    ribfile.write("Projection \"orthographic\"\n")
    ribfile.write("\tWorldBegin\n")
    ribfile.write("\tSides 2\n")
    ribfile.write("\tAttributeBegin\n")
    ribfile.write("\tColor [ 1 1 1 ]")
    ribfile.write("\tSurface \"read2dbm\" \"pointcloudname\" \"%s\"\n"%(bakePath))
    ribfile.write("\tTranslate 0 0 0.02\n")
    ribfile.write("\tPolygon \"P\" [ -2 -1 0   2 -1 0   2 1 0  -2 1 0 ]\"st\" [ 0 1  1 1  1 0  0 0  ]\n")
    ribfile.write("\tAttributeEnd\n")
    ribfile.write("WorldEnd\n")
    ribfile.write("FrameEnd\n")









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
    ribfile.write("FrameBegin 3\n")
    ribfile.write("Option \"statistics\" \"endofframe\" [1]\n")
    ribfile.write("Option \"searchpath\" \"shader\" \"data/shaders/renderman:&\"\n")
    ribfile.write("Option \"searchpath\" \"texture\" \"data/textures:&\"\n")
    ribfile.write("Projection \"perspective\" \"fov\" %f\n"%(fov))
    ribfile.write('Format %s %s 1\n' % (xResolution, yResolution))
    ribfile.write("Clipping 0.1 100\n")
    ribfile.write('PixelSamples %s %s\n'%(2,2))
    ribfile.write('ShadingRate %s \n'%(0.7))
    ribfile.write('Sides 2\n')
    ribfile.write('Declare "lighttexture" "string"\n')
    ribfile.write('Declare "skintexture" "string"\n')
    ribfile.write('Declare "bumptexture" "string"\n')
    ribfile.write('Display "00001.tif" "framebuffer" "rgb"\n')
    ribfile.write('Display "+rendering.tif" "file" "rgba"\n')
    ribfile.write("\t\tTranslate %s %s %s\n" %(locX, locY, zoom))
    ribfile.write("\t\tRotate %s 1 0 0\n" %(-rotX))
    ribfile.write("\t\tRotate %s 0 1 0\n" %(-rotY))
    ribfile.write('WorldBegin\n')
    ribfile.write('\tLightSource "ambientlight" 1 "intensity" [.05] "color lightcolor" [1 1 1]\n')
    ribfile.write('\tLightSource "spotlight" 2 "from" [2.39 10.64 -5] "to" [0 0 0] "intensity" 30  "coneangle" [1.0] \n')
    ribfile.write('\tLightSource "spotlight" 3 "from" [-4.14 4.84 -7.45] "to" [0 0 0] "intensity" 35  "coneangle" [1.0]\n')
   
     
	 

    for obj in scene.objects:
        name = obj.name
        if name == "base.obj":  #TODO: attribute isRendered
            ribPath = ribRepository + "/" + name + ".rib"
            objPath = "data/3dobjs/" + "base.obj"

            lightMap = ribRepository + "/" + name +"_map"+ ".tif"

            ribfile.write('\tAttributeBegin\n')
            ribfile.write("\t\tOrientation \"inside\"\n")
            ribfile.write("\t\tColor [%s %s %s]\n" %(0.8, 0.8, 0.8))
            ribfile.write("\t\tOpacity [%s %s %s]\n" %(1,1,1))
            ribfile.write("\t\tTranslate %s %s %s\n" %(0,0,0))
            ribfile.write("\t\tRotate %s 0 0 1\n" %(0))
            ribfile.write("\t\tRotate %s 0 1 0\n" %(0))
            ribfile.write("\t\tRotate %s 1 0 0\n" %(0))
            ribfile.write("\t\tScale %s %s %s\n" %(1,1,1))
            writeSubdivisionMesh(ribPath, obj, objPath)
            ribfile.write('\t\tSurface "skin" "string opacitytexture" "%s" "string texturename" "%s" "string speculartexture" "%s" "string ssstexture" "%s" "float Ks" [0.2] "float dark" [2]\n'%("texture_opacity.tif","texture.tif","texture_ref.tif",lightMap))
            #ribfile.write('Surface "matte"')
            ribfile.write('\t\tReadArchive "%s"\n' %(ribPath))
            ribfile.write('\tAttributeEnd\n')
            writeHairs(ribRepository, obj)



    ribfile.write('\tAttributeBegin\n')
    ribfile.write('\t\tDeclare "rootcolor" "color"\n')
    ribfile.write('\t\tDeclare "tipcolor" "color"\n')
    ribfile.write('\t\tSurface "hair" "rootcolor" [%s %s %s] "tipcolor" [%s %s %s]\n'%(hairsClass.rootColor[0],\
                    hairsClass.rootColor[1],hairsClass.rootColor[2],\
                    hairsClass.tipColor[0],hairsClass.tipColor[1],hairsClass.tipColor[2]))
    

    ribfile.write('\t\tReadArchive "%s/hairs.rib"\n' %(ribRepository))
    ribfile.write('\tAttributeEnd\n')

    ribfile.write("WorldEnd\n")
    ribfile.write("FrameEnd\n")



def saveScene(scene, fName, ribDir, engine):
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


    loadHairsFile("data/hairs/test.hair")
    if not os.path.isdir(ribDir):
        os.mkdir(ribDir)
    ribRepository = ribDir+"/"+"ribFiles"


    if not os.path.isdir(ribRepository):
        os.mkdir(ribRepository)
    fName = os.path.join(ribDir,fName)

    ribfile = file(fName,'w')

    if engine == "aqsis":
        writeLightMapFrameAqsis(scene, ribfile, ribRepository)
    else:
        writeLightMapFramePixie(scene, ribfile, ribRepository)

    writeMainSceneFrame(scene, ribfile, ribRepository)
    ribfile.close()

    if engine == "aqsis":
        #os.system('%s %s &'%('aqsis', fName))
        command = '%s %s'%('aqsis', fName)
    if engine == "pixie":
        command = '%s %s'%('rndr', fName)
    print "COMMAND",command
    subprocess.Popen(command, shell=True)



