#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Pedro Alcaide, aka povmaniaco

**Copyright(c):**      MakeHuman Team 2001-2013

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
import log


def MitsubaExport(obj, app, settings):

    log.message('Mitsuba Export object: %s' % obj.name)

    # Read settings from an ini file. This reload enables the settings to be changed dynamically 
    # without forcing the user to restart the MH application for the changes to take effect.
    
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
    if os.path.exists(Mitsuba_bin):
        if action == 'render':
            # exporting human mesh.
            fileobj = 'human.obj'
            filename = out_path + fileobj
        
            #
            #exportObj(obj, filename)
            exportObj_TL(obj, filename)

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
            mitsubaCamera(camera, resolution, filexml, samplerData, obj)

            # add lights
            mitsubaLights(filexml)

            # add texture data
            mitsubaTexture(filexml)

            # add materials
            mitsubaMaterials(filexml)

            # add geometry
            subSurfaceData = mitsubaSSS()
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

def exportPly(obj, filename, exportGroups = True, groupFilter=None):
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

    f = open(filename, 'w')
    f.write("ply\n")
    f.write("format ascii 1.0\n")
    f.write("comment Mh2Ply; PLY exporter for MakeHuman\n")
    f.write("element vertex 500 \n")
    f.write("property float x\n")
    f.write("property float y\n")
    f.write("property float z\n")
    
    '''
    for vertex colors?
    f << "property uchar red\n";
    f << "property uchar green\n";
    f << "property uchar blue\n";
    '''
    f.write("property float nx\n")
    f.write("property float ny\n")
    f.write("property float nz\n")
   
    #f.write("property float u\n")
    #f.write("property float v\n")
    
    f.write("element face ""amount faces""\n")
    f.write("property list uchar uint vertex_indices\n")
    f.write("end_header\n")
   
    uvs =[u for u in obj.uvValues]
    log.debug(uvs[24])
    
    for v in obj.verts:
        # vertex
        f.write('%f %f %f' % tuple(v.co))
        
        # normals
        f.write(' %f %f %f' % tuple(v.no))

        f.write('\n')
    
    faces = [fe for fe in obj.faces 
             if not 'joint' in fe.group.name 
             and not 'helper' in fe.group.name]
    #
    for fa in faces:
        f.write('3 %s %s %s' % (fa.verts[0].idx, fa.verts[1].idx, fa.verts[2].idx))
        f.write('\n')
    
    

def exportObj(obj, filename):
    '''
    #
    This function exports a mesh object in Wavefront obj format. 
    It is assumed that obj will have at least vertices and faces,
    (exception handling for vertices/faces must be done outside this method).

    Parameters
    ----------

    obj:
      *Object3D*.  The object to export.
    filename:
      *string*.  The filename of the file to export the object to.
    '''

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
    exportGroups = True
    # basic filter..
    faces = [fa for fa in obj.faces
             if not 'joint-' in fa.group.name
             and not 'helper' in fa.group.name 
             and not 'eye-cornea' in fa.group.name]
    
    # filter eyebrown and lash for use an special material with 'alpha' value
    # SSS not work fine, cause: the geometry is not closed solid?
    faces = [fa for fa in faces 
             if not '-eyebrown' in fa.group.name 
             and not '-lash' in fa.group.name]
    #
    for face in faces:
        f.write('f')
        for i, v in enumerate(face.verts):
            if (obj.uvValues == None):
                f.write(' %i//%i ' % (v.idx + 1, v.idx + 1))
            else:
                f.write(' %i/%i/%i ' % (v.idx + 1, face.uv[i] + 1, v.idx + 1))
        #
        f.write('\n')  
    #
    f.close()

def mitsubaXmlFile(filexml):
    #
    # declare 'header' of .xml file
    f = open(filexml, 'w')
    f.write('<?xml version="1.0" encoding="utf-8"?>\n' +
            '<scene version="0.4.0">\n')
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
                      '\t        <float name="scale" value=".0002"/>\n' +
                      '\t        <string name="intIOR" value="water"/>\n' +
                      '\t        <string name="extIOR" value="air"/>\n' +
                      '\t        <rgb name="sigmaS" value="87.2, 127.2, 143.2"/>\n' +
                      '\n        <rgb name="sigmaA" value="1.04, 5.6, 11.6"/>\n' +
                      '\n        <integer name="irrSamples" value="64"/>\n' +
                      #'\t        <string name="material" value="skin1"/>\n' +
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
    #
    return samplerData
    
def mitsubaCamera(camera, resolution, filexml, samplerData, obj):
    # TODO; camera fov
    fov = 27
    f = open(filexml, 'a')
    f.write('\n' +
            '\t<sensor type="perspective" id="Camera01">\n' +
            '\t    <float name="fov" value="%f"/>\n' % fov +
            '\t    <float name="nearClip" value="1"/>\n' +
            '\t    <float name="farClip" value="1000"/>\n' +
            '\t    <boolean name="mapSmallerSide" value="true"/>\n' +
            '\t    <transform name="toWorld">\n' +
            '\t        <lookAt origin="%f, %f, %f"\n' % (camera.eyeX, camera.eyeY, camera.eyeZ) +
            '\t                target="%f, %f, %f"\n' % (camera.focusX, camera.focusY, camera.focusZ) +
            '\t                up="0, 1, 0"/>\n' + 
            '\t        <scale x="-1"/>\n' +
            '\t        <rotate x="1" angle="%f"/>\n' % -obj.rx +
            '\t        <rotate y="1" angle="%f"/>\n' % -obj.ry +
            '\t        <rotate z="1" angle="%f"/>\n' % obj.rz +
            '\t        <translate x="%f" y="%f" z="%f"/>\n' % (obj.x, -obj.y, obj.z) +
            '\t    </transform>\n' +
            '\t    <film type="hdrfilm" id="film">\n' +
            '\t        <integer name="width" value="%i"/>\n'  % resolution[0] +
            '\t        <integer name="height" value="%i"/>\n' % resolution[1] +
            '\t        <rfilter type="gaussian"/>\n' +
            '\t    </film>\n' +
            '\t    %s\n' % samplerData +
            '\t</sensor>\n')
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
                '\t<emitter type="envmap" id="Area_002-light">\n' +
                '\t    <string name="filename" value="%s"/>\n' % env_path +
                '\t    <transform name="toWorld">\n' +
                '\t        <rotate z="1" angle="-90"/>\n' +
                '\t        <matrix value="-0.224951 -0.000001 -0.974370 0.000000\n' +
                '\t                       -0.974370 0.000000 0.224951 0.000000\n' +
                '\t                       0.000000 1.000000 -0.000001 8.870000\n' +
                '\t                       0.000000 0.000000 0.000000 1.000000"/>\n' +
                '\t    </transform>\n' +
                '\t    <float name="scale" value="3"/>\n' +
                '\t</emitter>\n' )
    elif sky:
        f.write('\n'+
                '\t<emitter type="sky">\n' +
                '\t   <float name="scale" value="1"/>\n' +
                '\t</emitter>\n')
    else:
        f.write('\n' + # test for sphere light
                '\t<shape type="sphere">\n' +
                '\t    <point name="center" x="-1" y="4" z="60"/>\n' +
                '\t    <float name="radius" value="1"/>\n' +
                '\t    <emitter type="area">\n' +
                '\t        <blackbody name="intensity" temperature="4500K"/>\n' +
                '\t    </emitter>\n' +
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
            '\t<bsdf type="roughplastic" id="humanMat">\n' + #% mat_type +  
            '\t    <rgb name="specularReflectance" value="0.35, 0.25, 0.25"/>\n' +
            '\t    <ref name="diffuseReflectance" id="imageh"/>\n' + # aplic texture image to diffuse chanel
            '\t    <float name="specularSamplingWeight" value="0.1250"/>\n' +
            '\t    <float name="diffuseSamplingWeight" value="1.0"/>\n' +
            '\t    <boolean name="nonlinear" value="false"/>\n' +
            '\t    <string name="intIOR" value="water"/>\n' +
            '\t    <string name="extIOR" value="air"/>\n' +
            '\t    <float name="fdrInt" value="0.5"/>\n' +
            '\t    <float name="fdrExt" value="0.5"/>\n' +
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
    '''
    f.write('\n' +
            '\t<shape type="obj">\n' +
            '\t    <string name="filename" value="%s"/>\n' % objpath +
            '\t    <ref name="bsdf" id="__planemat"/>\n' +
            '\t</shape>\n'
            )
    '''
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
    
    
#--------------------------------------------------------------------------
#   TL: A version of exportObj that handles clothes
#--------------------------------------------------------------------------

import gui3d
import object_collection

def exportObj_TL(obj, filename):
    """
    This function exports a mesh object in Wavefront obj format. 
    It is assumed that obj will have at least vertices and faces,
    (exception handling for vertices/faces must be done outside this method).

    Parameters
    ----------

    obj:
      *Object3D*.  The object to export.
    filename:
      *string*.  The filename of the file to export the object to.
    """

    # Load all stuff to be rendered - mesh, clothes, polygon hair

    stuffs = object_collection.setupObjects("Mitsuba", gui3d.app.selectedHuman, helpers=False, hidden=False, eyebrows=False, lashes=False)

    # Write obj file
    # not is need mtl file. The material is created into Mitsuba .xml file
    # file_mtl = str(filename).replace('.obj','.mtl')

    f = open(filename, 'w')
    f.write('# MakeHuman exported OBJ for Mitsuba\n')
    f.write('# www.makehuman.org\n')
    # 

    for stuff in stuffs:
        for v in stuff.verts:
            f.write("v %.4f %.4f %.4f\n" % tuple(v))

    for stuff in stuffs:
        for uv in stuff.uvValues:
            f.write("vt %.4f %.4f\n" % tuple(uv))

    nVerts = 1
    nUvVerts = 1
    for stuff in stuffs:
        for fc in stuff.faces:
            f.write('f ')
            for vs in fc:
                f.write("%d/%d " % (vs[0]+nVerts, vs[1]+nUvVerts))
            f.write('\n')
        nVerts += len(stuff.verts)
        nUvVerts += len(stuff.uvValues)
    
    f.close()

#--------------------------------------------------------------------------
#   End TL modications
#--------------------------------------------------------------------------
    
