#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Modules to handle supported 3D file formats. 

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

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

import os
import algos3d
import module3d
import numpy as np

originalVertexCache = {}

def loadMesh(path, locX=0, locY=0, locZ=0, loadColors=1):
    """
    This function loads the specified mesh objects into internal MakeHuman data structures,
    and return it.
    
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

    fg = None
    mtl = ''

    try:
        objFile = open(path)
    except:
        print 'Warning: obj file not found: ', path
        return False

    verts = []
    uvs = []
    fverts = []
    fuvs = []
    groups = []
    has_uv = False

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
                    fg =  obj.createFaceGroup('default-dummy-group')
                    
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

            elif command == 'g':
                
                fg =  obj.createFaceGroup(lineData[1])
                
            elif command == 'usemtl':
            
                mtl = lineData[1]
                
            elif command == 'o':
                
                obj.name = lineData[1]

    obj.setCoords(verts)
    obj.setUVs(uvs)
    obj.setFaces(fverts, fuvs if has_uv else None, groups)

    originalVertexCache[path] = obj.coord.copy()

    obj.updateIndexBuffer()
    obj.calcNormals()

    objFile.close()

    if loadColors:
        colorPath = path + '.colors'
        algos3d.loadVertsColors(obj, colorPath, None)
        
    return obj
    
originalVertexCoordinates = []

def loadVertsCoo(path):
    """
    This function serves as a small utility function to load just the vertex
    data from a WaveFront object file.
   
    It is used for example to build the original vertex data
    or to reset mesh modifications to their pre-modified state.
    
    Parameters
    ----------
    
    path:
        *string*. The file system path to the file to be read.
       
    """

    if path in originalVertexCache:
        return originalVertexCache[path]

    global originalVertexCoordinates

    if originalVertexCoordinates:
        return originalVertexCoordinates

    try:
        fileDescriptor = open(path)
    except:
        print 'Error opening %s file' % path
        return
    originalVertexCoordinates = []
    for data in fileDescriptor:
        dataList = data.split()
        if len(dataList) == 4:
            if dataList[0] == 'v':
                co = (float(dataList[1]), float(dataList[2]), float(dataList[3]))
                originalVertexCoordinates.append(co)
    fileDescriptor.close()
    return originalVertexCoordinates
