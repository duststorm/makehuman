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
from os.path import basename
#
import sys


def MitsubaExport(obj, app, settings):

    print 'Mitsuba Export object: ', obj.name

    # Read settings from an ini file. This reload enables the settings to be
    # changed dynamically without forcing the user to restart the MH
    # application for the changes to take effect.

    camera = app.modelCamera
    resolution = (app.settings.get('rendering_width', 800), app.settings.get('rendering_height', 600))

    reload(mh2mitsuba_ini)

    out_path = os.path.join(mh.getPath('render'), mh2mitsuba_ini.outputpath)
    #
    source = mh2mitsuba_ini.source if settings['source'] == 'gui' else settings['source']
    action = mh2mitsuba_ini.action
    #
    outputDirectory = os.path.dirname(out_path)
    #
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    #
    # Copy the textures.png file into the output directory ?
    # because to copy, if we can use it directly from source?
    # well... Mitsuba required the image file into same folder of file .xml, atm...
    pigmentMap = 'data/textures/texture.png'
    #
    try:
        shutil.copy(pigmentMap, outputDirectory)
    except (IOError, os.error), why:
        print "Can't copy %s" % str(why)

    # The ini action option defines whether or not to attempt to render the file once
    # it's been written.
    if action == 'render':

        # exporting human mesh. Use mh2obj.py and some variances..!
        fileobj = 'human.obj'
        filename = out_path + fileobj
        previewMat = False

        #
        if not previewMat:
            exportObj(obj, filename)

        # create name for Mitsuba xml scene file
        # this name is different to the name use for command line?
        filexml = str(filename).replace('.obj','.xml')
        print filexml

        # open xml file scene
        mitsubaXmlFile(filexml)

        # create a integrator
        mitsubaIntegrator(filexml)

        # create camera
        mitsubaCamera(camera, resolution, filexml)

        # add light
        mitsubaLights(filexml)

        # add texture data
        mitsubaTexture(filexml)

        # add materials
        mitsubaMaterials(filexml)

        # add geometry (Human  or previewMat mesh)
        mitsubaGeometry(filexml, previewMat, fileobj)

        # closed scene file
        mitsubaFileClose(filexml)

        #
        xmlDataFile = str(fileobj).replace('.obj', '.xml')
        if source == 'gui':
            pathHandle = subprocess.Popen(cwd=outputDirectory, args = mh2mitsuba_ini.mitsuba_gui +' '+ xmlDataFile)
        #
        elif source == 'console':
            pathHandle = subprocess.Popen(cwd=outputDirectory, args = mh2mitsuba_ini.mitsuba_console +' '+ xmlDataFile)
        else:
            print 'nothing for renderer'

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
    # it is not necessary to create  mtllib

    for v in obj.verts:
        f.write('v %f %f %f\n' % tuple(v.co))

    if not (obj.uvValues==None):
        for uv in obj.uvValues:
            f.write('vt %f %f\n' % tuple(uv))

    for v in obj.verts:
        f.write('vn %f %f %f\n' % tuple(v.no))

    # it is not necessary to declare a texture
    #f.write('usemtl basic\n')
    f.write('s off\n') # need more info about this command

    #
    groupFilter = None
    exportGroups = False
    #
    for fg in obj.faceGroups:
        if not groupFilter or groupFilter(fg):
            if exportGroups:
                f.write('g %s\n' % fg.name)
        # filter eyebrown, lash and joint objects
        # TO Do; separate this objects for applicate a special texture values?
        if not '-eyebrown' in fg.name:
            if not '-lash' in fg.name:
                if not 'joint-' in fg.name: # if 'smmoth' option is 'ON', not show joints?
                    for face in fg.faces:
                        f.write('f')
                        for i, v in enumerate(face.verts):
                            if (obj.uvValues == None):
                                f.write(' %i//%i ' % (v.idx + 1, v.idx + 1))
                            else:
                                f.write(' %i/%i/%i ' % (v.idx + 1, face.uv[i] + 1, v.idx + 1))
                        f.write('\n')

    f.close()

    # not is need material file,  remove it?
    #
    '''
    f = open(file_mtl, 'w')
    f.write('# MakeHuman exported MTL\n')
    f.write('# www.makehuman.org\n')
    f.write('newmtl basic\n')
    f.write('Ka 1.0 1.0 1.0\n')
    f.write('Kd 1.0 1.0 1.0\n')
    f.write('Ks 0.33 0.33 0.52\n')
    f.write('illum 5\n')
    f.write('Ns 50.0\n')
    if not (obj.texture == None): f.write('map_Kd %s\n' % basename(obj.texture))
    f.close()
    '''

def mitsubaXmlFile(filexml):
    #
    # declare 'header' of .xml file
    f = open(filexml, 'w')
    f.write('<?xml version="1.0" encoding="utf-8"?>\n' +
            '<scene version="0.3.0">\n')
    f.close()

def mitsubaIntegrator(filexml):
    #
    # lack more options
    f = open(filexml, 'a')
    f.write('\n' +
            '    <integrator type="path">\n' +
            '        <integer name="maxDepth" value="8"/>\n' +
            '    </integrator>\n')
    f.close()

def mitsubaCamera(camera, resolution, filexml):
    #
    fov = 37
    f = open(filexml, 'a')
    f.write('\n' +
            '    <camera type="perspective" id="Camera01-lib">\n' +
            '        <float name="fov" value="%f"/>\n' % fov +
            '        <float name="nearClip" value="1"/>\n' +
            '        <float name="farClip" value="1000"/>\n' +
            '        <boolean name="mapSmallerSide" value="true"/>\n' +
            '        <transform name="toWorld">\n' +
            '            <scale x="-1"/>\n' +
            '            <lookAt origin="%f, %f, %f" target="%f, %f, %f" up="0, 1, 0"/>\n' % (camera.eyeX, camera.eyeY, camera.eyeZ, camera.focusX, camera.focusY, camera.focusZ) +
            '        </transform>\n' +
            '        <film type="exrfilm" id="film">\n' +
            '            <integer name="width" value="%i"/>\n'  % resolution[0] +
            '            <integer name="height" value="%i"/>\n' % resolution[1] +
            '            <rfilter type="gaussian"/>\n' +
            '        </film>\n' +
            '    </camera>\n')
    f.close()

#
def mitsubaLights(filexml):
    #
    env = False
    sky = True
    #
    '''
    f = open(filexml, 'a')
    # test for image environment lighting
    if env:
        f.write('\n' +
                '    <luminaire type="envmap" id="Area_002-light">\n' +
                '        <string name="filename" value="envmap.exr"/>\n' +
                '        <transform name="toWorld">\n' +
                '            <rotate z="1" angle="90"/>\n' +
                '            <matrix value="-0.224951 -0.000001 -0.974370 0.000000 -0.974370 0.000000 0.224951 0.000000 0.000000 1.000000 -0.000001 8.870000 0.000000 0.000000 0.000000 1.000000 "/>\n' +
                '        </transform>\n' +
                '        <float name="intensityScale" value="3"/>\n' +
                '    </luminaire>\n' )
    elif sky:
        f.write('\n'+
                '    <luminaire type="sky">\n' +
                '    </luminaire>\n')
    else:
        f.write('\n' + # test for sphere light
                '    <shape type="sphere">\n' +
                '       <point name="center" x="-1" y="4" z="60"/>\n' +
                '        <float name="radius" value="1"/>\n' +
                '            <luminaire type="area">\n' +
                '                <blackbody name="intensity" temperature="7000K"/>\n' +
                '            </luminaire>\n' +
                '    </shape>\n')
    f.close()
    '''
#
def mitsubaTexture(filexml):
    #
    f = open(filexml, 'a')
    f.write('\n' +
            '    <texture type="bitmap" id="imageh">\n' +
            '        <string name="filename" value="texture.png"/>\n' +
            '    </texture>\n')
    f.close()

def mitsubaMaterials(filexml):
    #
    f = open(filexml, 'a')
    f.write('\n' +
            '    <bsdf type="diffuse" id="humanMat">\n' + # create a 'instantiate' material definition (id)
            '        <texture type="bitmap" name="reflectance">\n' +
            '            <string name="filename" value="texture.png"/>\n' +
            '        </texture>\n' +
            '    </bsdf>\n')
    f.close()

def mitsubaGeometry(filexml, previewMat, fileobj):
    #
    pos = (0, 4, 0)
    size = 5
    f = open(filexml, 'a')
    # write plane
    '''
    f.write('    <shape type="disk">\n' +
            '        <bsdf type="diffuse">\n' +
            '            <texture name="reflectance" type="checkerboard">\n' +
            '                <float name="uvscale" value=".4"/>\n' +
            '            </texture>\n' +
            '        </bsdf>\n' +
            '    </shape>\n')

    if previewMat:
        f.write('\n' +
                '    <shape type="sphere">\n' +
                '        <point name="center" x="%f" y="%f" z="%f"/>\n' % pos +
                '        <float name="radius" value="%i"/>\n' % size +
                '        <bsdf type="diffuse"/>\n' +
                '        <ref id="humanMat"/>\n' +
                '    </shape>\n')
    #else:
    '''
    f.write('\n' +
            '    <shape type="obj">\n' +
            '        <string name="filename" value="%s"/>\n' % fileobj +
            '        <ref id="humanMat"/>\n' + # use 'instantiate' material declaration (id)
            '    </shape>\n')
    f.close()

def mitsubaFileClose(filexml):
    #
    f = open(filexml, 'a')
    f.write('</scene>')
    f.close()
