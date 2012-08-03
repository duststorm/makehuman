#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Pedro Alcaide, aka povmaniaco

**Copyright(c):**      MakeHuman Team 2001-2012

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This code is part of MakeHuman exported for Mitsuba Renderer

This module implements functions to export a human model in Mitsuba XML file format.
Also use parts of code from mh2obj.py

"""

import os
import string
import shutil
import subprocess
import mh2mitsuba_ini
import random
import mh
# povman
#import gui3d
# end
from os.path import basename
#
import sys


def MitsubaExport(obj, app, settings):

    print 'Mitsuba Export object: ', obj.name

    # Read settings from an ini file. This reload enables the settings to be
    # changed dynamically without forcing the user to restart the MH
    # application for the changes to take effect.

    camera = app.modelCamera
    #
    resolution = (app.settings.get('rendering_width', 800), app.settings.get('rendering_height', 600))
    #
    reload(mh2mitsuba_ini)
    #
    source = mh2mitsuba_ini.source if settings['source'] == 'gui' else settings['source']
    #
    lighting = mh2mitsuba_ini.lighting if settings['lighting'] == 'dl' else settings['lighting']
    #
    sampler = mh2mitsuba_ini.sampler if settings['sampler'] == 'low' else settings['sampler']
           
    # output directory for rendering
    # Make sure the directory exists
    out_path = os.path.join(mh.getPath('render'), mh2mitsuba_ini.outputpath)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    #
    outputDirectory = os.path.dirname(out_path)
    
    # The ini action option defines whether or not to attempt to render the file once
    # it's been written.
    action = mh2mitsuba_ini.action
    
    # Mitsuba binaries path
    Mitsuba_bin = app.settings.get('mitsuba_bin', '')
    #
    if os.path.exists(Mitsuba_bin) and action == 'render':
        
        # exporting human mesh.
        fileobj = 'human.obj'
        filename = out_path + fileobj
        
        #
        exportObj(obj, filename)

        # create name for Mitsuba xml scene file
        # this name is different to the name use for command line?
        filexml = str(filename).replace('.obj','.xml')
        #print filexml

        # open xml file scene
        mitsubaXmlFile(filexml)

        # create a integrator
        mitsubaIntegrator(filexml, lighting)
        
        # create sampler
        samplerData = mitsubaSampler(sampler)
        
        # create camera
        mitsubaCamera(camera, resolution, filexml, samplerData)

        # add lights
        mitsubaLights(filexml)

        # add texture data
        mitsubaTexture(filexml)

        # add materials
        mitsubaMaterials(filexml)

        # add geometry
        subSurfaceData = '' # mitsubaSSS()
        mitsubaGeometry(filexml, fileobj, subSurfaceData)

        # closed scene file
        mitsubaFileClose(filexml)

        #
        xmlDataFile = str(fileobj).replace('.obj', '.xml')
        #
        if source == 'gui':
            render_mode  = str(Mitsuba_bin)+'/mtsgui.exe'
            pathHandle = subprocess.Popen(cwd=outputDirectory, args = render_mode +' '+ xmlDataFile)
        #
        elif source == 'console':
            render_mode  = str(Mitsuba_bin)+'/mitsuba.exe'
            pathHandle = subprocess.Popen(cwd=outputDirectory, args = render_mode +' '+ xmlDataFile)
        #
        else:
            app.prompt('INFO ',
                       'Created .xml file in output folder.\n'\
                       'Ready to render',
                       'Close')
    
    # if not valid path
    else:
        app.prompt('WARNING!!',
                   'Path to Mitsuba is not correct or not exist.\n'\
                   'Please, enter a valid path to Mitsuba folder.',
                   'Accept')    

def exportObj(obj, filename):
    """
    This function exports a mesh object in Wavefront obj format. It is assumed that obj will have at least vertices and
    faces (exception handling for vertices/faces must be done outside this method).

    Parameters
    ----------

    obj:
      *Object3D*.  The object to export.
    filename:
      *string*.  The filename of the file to export the object to.
    """

    # Write obj file
    # not is need mtl file. The material is created into Mitsuba .xml file
    # file_mtl = str(filename).replace('.obj','.mtl')

    f = open(filename, 'w')
    f.write('# MakeHuman exported OBJ for Mitsuba\n')
    f.write('# www.makehuman.org\n')
    # 
    for v in obj.verts:
        f.write('v %f %f %f\n' % tuple(v.co))

    if not (obj.uvValues==None):
        for uv in obj.uvValues:
            f.write('vt %f %f\n' % tuple(uv))

    for v in obj.verts:
        f.write('vn %f %f %f\n' % tuple(v.no))

    #
    groupFilter = None
    exportGroups = False
    #
    for fg in obj.faceGroups:
        if not groupFilter or groupFilter(fg):
            if exportGroups:
                f.write('g %s\n' % fg.name)
            # filter eyebrown, lash and joint objects
            # TO DO; separate objects for materials?
            '''
            if 'head' in fg.name or 'nose' in fg.name or 'chin' in fg.name or 'mouth' in fg.name:
                for face in fg.faces:
                    f.write('f')
                    for i, v in enumerate(face.verts):
                        if (obj.uvValues == None):
                            f.write(' %i//%i ' % (v.idx + 1, v.idx + 1))
                        else:
                            f.write(' %i/%i/%i ' % (v.idx + 1, face.uv[i] + 1, v.idx + 1))
                    f.write('\n')
            '''
            if not '-lash' in fg.name:
                if not 'joint-' in fg.name:
                    if not '-eyebrown' in fg.name:
                        for face in fg.faces:
                            f.write('f')
                            for i, v in enumerate(face.verts):
                                if (obj.uvValues == None):
                                    f.write(' %i//%i ' % (v.idx + 1, v.idx + 1))
                                else:
                                    f.write(' %i/%i/%i ' % (v.idx + 1, face.uv[i] + 1, v.idx + 1))
                            #
                            f.write('\n')
            #'''   
    #
    f.close()

def mitsubaXmlFile(filexml):
    #
    # declare 'header' of .xml file
    f = open(filexml, 'w')
    f.write('<?xml version="1.0" encoding="utf-8"?>\n' +
            '<scene version="0.3.0">\n')
    f.close()

def mitsubaIntegrator(filexml, lighting):
    # lack more options
    f = open(filexml, 'a')
    if lighting == 'dl':
        f.write('\n' +
                '\t<integrator type="direct">\n' +
                '\t    <integer name="luminaireSamples" value="12"/>\n' +
                '\t    <integer name="bsdfSamples" value="8"/>\n' +
                '\t</integrator>\n'
                )
    else:
        f.write('\n' + 
                '\t<integrator type="path">\n' + 
                '\t    <integer name="maxDepth" value="-1"/>\n' + 
                '\t    <integer name="rrDepth" value="10"/>\n' +
                '\t    <boolean name="strictNormals" value="false"/>\n' + 
                '\t</integrator>\n'
                )
    f.close()

def mitsubaSSS():
    #subSurfaceData = ''
    subSurfaceData = ('\n' +
                      '\t    <subsurface type="dipole">\n' +
                      '\t        <float name="densityMultiplier" value=".002"/>\n' +
                      '\t        <string name="material" value="skin2"/>\n' +
                      '\t    </subsurface>\n'
                      )
    return subSurfaceData
   
def mitsubaSampler(sampler):
    #
    samplerData = ''
    if sampler == 'ind':
        samplerData =('\n' +
                      '\t    <sampler type="independent">\n' + 
                      '\t        <integer name="sampleCount" value="16"/>\n' + 
                      '\t    </sampler>\n'
                      )
    else:
        samplerData =('\n' +
                      '\t    <sampler type="ldsampler">\n' +
                      '\t        <integer name="depth" value="4"/>\n' +
                      '\t        <integer name="sampleCount" value="16"/>\n' +
                      '\t    </sampler>\n'
                      )
    return samplerData
    
def mitsubaCamera(camera, resolution, filexml, samplerData):
    #
    fov = 27
    f = open(filexml, 'a')
    f.write('\n' +
            '\t<camera type="perspective" id="Camera01-lib">\n' +
            '\t    <float name="fov" value="%f"/>\n' % fov +
            '\t    <float name="nearClip" value="1"/>\n' +
            '\t    <float name="farClip" value="1000"/>\n' +
            '\t    <boolean name="mapSmallerSide" value="true"/>\n' +
            '\t    <transform name="toWorld">\n' +
            '\t        <scale x="-1"/>\n' +
            '\t        <lookAt origin="%f, %f, %f" target="%f, %f, %f" up="0, 1, 0"/>\n' % (camera.eyeX, camera.eyeY, camera.eyeZ, camera.focusX, camera.focusY, camera.focusZ) +
            '\t    </transform>\n' +
            '\t    <film type="exrfilm" id="film">\n' +
            '\t        <integer name="width" value="%i"/>\n'  % resolution[0] +
            '\t        <integer name="height" value="%i"/>\n' % resolution[1] +
            '\t        <rfilter type="gaussian"/>\n' +
            '\t    </film>\n' +
            '\t    %s\n' % samplerData +
            '\t</camera>\n')
    f.close()

def mitsubaLights(filexml):
    # TODO: create a menu option
    env_path = os.getcwd() + '/data/mitsuba/envmap.exr'
    env = True
    sky = False
    #

    f = open(filexml, 'a')
    # test for image environment lighting
    if env:
        f.write('\n' +
                '\t<luminaire type="envmap" id="Area_002-light">\n' +
                '\t    <string name="filename" value="%s"/>\n' % env_path +
                '\t    <transform name="toWorld">\n' +
                '\t        <rotate z="1" angle="-90"/>\n' +
                '\t        <matrix value="-0.224951 -0.000001 -0.974370 0.000000 -0.974370 0.000000 0.224951 0.000000 0.000000 1.000000 -0.000001 8.870000 0.000000 0.000000 0.000000 1.000000 "/>\n' +
                '\t    </transform>\n' +
                '\t    <float name="intensityScale" value="3"/>\n' +
                '\t</luminaire>\n' )
    elif sky:
        f.write('\n'+
                '\t<luminaire type="sky">\n' +
                '\t   <float name="intensityScale" value="1"/>\n' +
                '\t</luminaire>\n')
    else:
        f.write('\n' + # test for sphere light
                '\t<shape type="sphere">\n' +
                '\t    <point name="center" x="-1" y="4" z="60"/>\n' +
                '\t    <float name="radius" value="1"/>\n' +
                '\t    <luminaire type="area">\n' +
                '\t        <blackbody name="intensity" temperature="4500K"/>\n' +
                '\t    </luminaire>\n' +
                '\t</shape>\n')
    f.close()

def mitsubaTexture(filexml):
    #pigment map
    texture_path = os.getcwd() + '/data/textures/texture.png'
        
    f = open(filexml, 'a')
    f.write('\n' +
            '\t<texture type="bitmap" id="imageh">\n' +
            '\t    <string name="filename" value="%s"/>\n' % texture_path +
            '\t</texture>\n')
    # texture for plane
    f.write('\n' +
            '\t<texture type="checkerboard" id="__planetex">\n' +
            '\t    <rgb name="darkColor" value="0.200 0.200 0.200"/>\n' +
            '\t    <rgb name="brightColor" value="0.400 0.400 0.400"/>\n' +
            '\t    <float name="uscale" value="4.0"/>\n' +
            '\t    <float name="vscale" value="4.0"/>\n' +
            '\t    <float name="uoffset" value="0.0"/>\n' +
            '\t    <float name="voffset" value="0.0"/>\n' +
            '\t</texture>\n')
    f.close()

def mitsubaMaterials(filexml):
    #
    f = open(filexml, 'a')
    # material for human mesh
    f.write('\n' +
            '\t<bsdf type="plastic" id="humanMat">\n' + #% mat_type +  
            '\t    <rgb name="specularReflectance" value="0.35, 0.25, 0.25"/>\n' +
            #'    <rgb name="diffuseReflectance" value="0.5, 0.5, 0.5"/>\n' + 
            '\t    <float name="specularSamplingWeight" value="0.50"/>\n' +
            '\t    <float name="diffuseSamplingWeight" value="1.0"/>\n' +
            '\t    <boolean name="nonlinear" value="false"/>\n' +
            '\t    <float name="intIOR" value="1.52"/>\n' +
            '\t    <float name="extIOR" value="1.000277"/>\n' +
            '\t    <float name="fdrInt" value="0.5"/>\n' +
            '\t    <float name="fdrExt" value="0.5"/>\n' +
            '\t    <ref name="diffuseReflectance" id="imageh"/>\n' + # aplic texture image to diffuse chanel
            '\t</bsdf>\n'
            )
    # simple material
    #f.write('\n' +
    #        '    <bsdf type="diffuse" id="humanMat">\n' +
    #        #'        <srgb name="reflectance" value="#6d7185"/>\n' +
    #        '        <ref name="reflectance" id="imageh"/>\n' +
    #        '    </bsdf>\n')

    # material for plane
    f.write('\n' +
            '\t<bsdf type="diffuse" id="__planemat">\n' +
            '\t    <ref name="reflectance" id="__planetex"/>\n' +
            '\t</bsdf>\n'
            )
    f.close()

def mitsubaGeometry(filexml, fileobj, subSurfaceData):
    #
    objpath = os.getcwd() + '/data/mitsuba/plane.obj'
    f = open(filexml, 'a')
    # write plane
    f.write('\n' +
            '\t<shape type="obj">\n' +
            '\t    <string name="filename" value="%s"/>\n' % objpath +
            '\t    <ref name="bsdf" id="__planemat"/>\n' +
            '\t</shape>\n'
            )
    # human mesh
    f.write('\n' +
            '\t<shape type="obj">\n' +
            '\t    <string name="filename" value="%s"/>\n' % fileobj +
            '\t    %s\n' % subSurfaceData +
            '\t    <ref id="humanMat"/>\n' + # use 'instantiate' material declaration (id)
            '\t</shape>\n'
            )
    f.close()

def mitsubaFileClose(filexml):
    #
    f = open(filexml, 'a')
    f.write('</scene>')
    f.close()
