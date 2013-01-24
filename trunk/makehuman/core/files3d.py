#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Modules to handle supported 3D file formats. 

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

.. image:: ../images/files_data.png
   :align: right   
   
This Module handles the 3D file formats supported by MakeHuman. It is planned that this module 
will implement a range of functions to handle most common 3D file formats in the future. 
The functions within this module should all follow a standard pattern
designed to facilitate the implementation of new interfaces.

This module will include functions to:
   
  - Transpose imported 3D data into a standard internal format for 
    each of the 3D file formats supported by the MakeHuman import 
    functions.
  - Generate 3D data structures that correspond to 3D file formats 
    supported by the makeHuman export function.
  - Provide generic transformation utilities such as the 
    dataTo3Dobject() function which takes an object defined 
    in the standard internal format and makes it visible to the user.  

The image on the right shows the general schema for implementing new MakeHuman importers. 
The wavefrontToData_simple() function below can be used as a template for developing 
new functions. 

Each importer function must return the 3d data in a standard format 
(a list [verts,vertsSharedFaces,vertsUV,faceGroups,faceGroupsNames] ).
The dataTo3Dobject() function can then be used to convert it into an object that 
is visible to the user through the GUI.
"""

import os.path
import module3d
import numpy as np
import log

def packStringList(strings):
    text = ''
    index = []
    for string in strings:
        index.append(len(text))
        text += string
    text = np.fromstring(text, dtype='S1')
    index = np.array(index, dtype=np.uint32)
    return text, index

def unpackStringList(text, index):
    strings = []
    last = None
    for i in index:
        if last is not None:
            name = text[last:i].tostring()
            strings.append(name)
        last = i
    if last is not None:
        name = text[last:].tostring()
        strings.append(name)

    return strings

def saveBinaryMesh(obj, path):
    fgstr, fgidx = packStringList(fg.name for fg in obj._faceGroups)
    mtlstr, mtlidx = packStringList(obj._materials)

    vars = dict(
        coord = obj.coord,
        vface = obj.vface,
        nfaces = obj.nfaces,
        texco = obj.texco,
        fvert = obj.fvert,
        group = obj.group,
        fmtls = obj.fmtls,
        fgstr = fgstr,
        fgidx = fgidx,
        mtlstr = mtlstr,
        mtlidx = mtlidx)

    if obj.has_uv:
        vars['fuvs']  = obj.fuvs

    np.savez(path, **vars)

def loadBinaryMesh(obj, path):
    log.debug('loadBinaryMesh: np.load()')

    npzfile = np.load(path)

    log.debug('loadBinaryMesh: loading arrays')
    coord = npzfile['coord']
    obj.setCoords(coord)

    texco = npzfile['texco']
    obj.setUVs(texco)

    fvert = npzfile['fvert']
    fuvs = npzfile['fuvs'] if 'fuvs' in npzfile.files else None
    group = npzfile['group']
    fmtls = npzfile['fmtls']
    obj.setFaces(fvert, fuvs, group, fmtls, skipUpdate=True)

    obj.vface = npzfile['vface']
    obj.nfaces = npzfile['nfaces']

    log.debug('loadBinaryMesh: loaded arrays')

    fgstr = npzfile['fgstr']
    fgidx = npzfile['fgidx']
    for name in unpackStringList(fgstr, fgidx):
        obj.createFaceGroup(name)
    del fgstr, fgidx

    log.debug('loadBinaryMesh: unpacked facegroups')

    mtlstr = npzfile['mtlstr']
    mtlidx = npzfile['mtlidx']
    obj._materials = unpackStringList(mtlstr, mtlidx)
    del mtlstr, mtlidx

    log.debug('loadBinaryMesh: unpacked materials')

def loadTextMesh(obj, path):
    log.debug('loadTextMesh: begin')
    objFile = open(path)

    fg = None
    mtl = None

    verts = []
    uvs = []
    fverts = []
    fuvs = []
    groups = []
    fmtls = []
    has_uv = False
    materials = {}
    faceGroups = {}

    for objData in objFile:

        lineData = objData.split()
        if len(lineData) > 0:
            
            command = lineData[0]
                
            if command == 'v':
                verts.append((float(lineData[1]), float(lineData[2]), float(lineData[3])))

            elif command == 'vt':
                uvs.append((float(lineData[1]), float(lineData[2])))

            elif command == 'f':
                if not fg:
                    if 0 not in faceGroups:
                        faceGroups[0] = obj.createFaceGroup('default-dummy-group')
                    fg = faceGroups[0]

                if mtl is None:
                    if 0 not in materials:
                        materials[0] = obj.createMaterial('')
                    mtl = materials[0]
                    
                uvIndices = []
                vIndices = []
                for faceData in lineData[1:]:
                    vInfo = faceData.split('/')
                    vIdx = int(vInfo[0]) - 1  # -1 because obj is 1 based list
                    vIndices.append(vIdx)

                    # If there are other data (uv, normals, etc)
                    if len(vInfo) > 1 and vInfo[1] != '':
                        uvIndex = int(vInfo[1]) - 1  # -1 because obj is 1 based list
                        uvIndices.append(uvIndex)
                
                if len(vIndices) == 3:
                    vIndices.append(vIndices[0])
                fverts.append(tuple(vIndices))
                    
                if len(uvIndices) > 0:
                    if len(uvIndices) == 3:
                        uvIndices.append(uvIndices[0])
                    has_uv = True
                if len(uvIndices) < 4:
                    uvIndices = [0, 0, 0, 0]
                fuvs.append(tuple(uvIndices))

                groups.append(fg.idx)
                
                fmtls.append(mtl)

            elif command == 'g':
                fgName = lineData[1]
                if fgName not in faceGroups:
                    faceGroups[fgName] = obj.createFaceGroup(fgName)
                fg =  faceGroups[fgName]
                
            elif command == 'usemtl':
                mtlName = lineData[1]
                if mtlName not in materials:
                    materials[mtlName] = obj.createMaterial(mtlName)
                mtl =  materials[mtlName]
                
            elif command == 'o':
                
                obj.name = lineData[1]

    objFile.close()

    obj.setCoords(verts)
    obj.setUVs(uvs)
    obj.setFaces(fverts, fuvs if has_uv else None, groups, fmtls)

    log.debug('loadTextMesh: end')

def loadMesh(path, locX=0, locY=0, locZ=0, loadColors=1):
    """
    This function loads the specified mesh object into internal MakeHuman data 
    structures, and returns it. The loaded file should be in Wavefront OBJ 
    format.
    
    Parameters:
    -----------
   
    path:     
      *String*.  The file system path to the file containing the object to load.

    locX:
      *float* X location of loaded obj, default = 0

    locY:
      *float* Y location of loaded obj, default = 0

    locZ:
      *float* Z location of loaded obj, default = 0
    """
    name = os.path.basename(path)
    obj = module3d.Object3D(name)

    obj.path = path
    obj.x = locX
    obj.y = locY
    obj.z = locZ

    try:
        npzpath = os.path.splitext(path)[0] + '.npz'
        try:
            if not os.path.isfile(npzpath):
                log.message('compiled file missing: %s', npzpath)
                raise RuntimeError()
            if os.path.isfile(path) and os.path.getmtime(path) > os.path.getmtime(npzpath):
                log.message('compiled file out of date: %s', npzpath)
                raise RuntimeError()
            loadBinaryMesh(obj, npzpath)
        except:
            loadTextMesh(obj, path)
            try:
                saveBinaryMesh(obj, npzpath)
            except StandardError:
                log.notice('unable to save compiled mesh: %s', npzpath)
    except:
        log.error('Unable to load obj file: %s', path, exc_info=True)
        return False

    obj.updateIndexBuffer()
    obj.calcNormals()
        
    return obj
