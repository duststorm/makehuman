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

import module3d
import os
import algos3d
    
def loadMesh(scene, path, locX=0, locY=0, locZ=0, loadColors=1):
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
    obj = scene.newObj(name)

    obj.path = path
    obj.x = locX
    obj.y = locY
    obj.z = locZ

    fg = None
    fIndex = 0

    try:
        objFile = open(path)
    except:
        print 'Warning: obj file not found: ', path
        return False
        
    obj.uvValues = []

    for objData in objFile.readlines():

        lineData = objData.split()
        if len(lineData) > 0:
            if lineData[0] == 'g':
                
                fg =  obj.createFaceGroup(lineData[1])
                
            elif lineData[0] == 'v':

                obj.createVertex([float(lineData[1]), float(lineData[2]), float(lineData[3])])

            elif lineData[0] == 'vt':

                obj.uvValues.append([float(lineData[1]), float(lineData[2])])
                
            elif lineData[0] == 'f':
                
                if not fg:
                    currentFaceGroup =  obj.createFaceGroup('default-dummy-group')
                    
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
                f = fg.createFace([obj.verts[i] for i in vIndices])
                    
                if len(uvIndices) > 0:  # look up uv, if existing, these are in the same order as in the file
                    if len(uvIndices) == 3:
                        uvIndices.append(uvIndices[0])
                    f.uv = uvIndices[:]

                f.idx = fIndex
                fIndex += 1
                
    obj.calcNormals()
    obj.updateIndexBuffer()

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


def loadFacesIndices(path, groups=False):
    """
    This function reads an obj file and loads just the vertex indices used in each face. 
   
    The internal MakeHuman representation of mesh data uses just triangular faces, but 
    it can be useful to export the mesh data using combinations of triangles and quads. 
    To be able to recombine the triangle data into quads in a manner that maps to a 
    particular object file it is necessary to read the vertex indices from that obj file. 
    
    The vertices [v1,v2,v3,v4] of a four-sided face could be converted to triangular faces 
    in different ways. For example:
    
    Object1: 
    face1 [v1,v2,v3]
    face2 [v1,v2,v4]

    Object2: 
    face1 [v1,v3,v4]
    face2 [v2,v3,v4]

    This utility reads information from the specified obj file about \"how to recombine vertices\" 
    in such a way as to map an internal triangular mesh to the trig and quad format 
    of a particular obj file.

    This macro returns a list of lists, for example, for 2 triangles:

    [[[coIdx1,uvIdx1],[coIdx2,uvIdx2],[coIdx3,uvIdx3]],
    [coIdx1,uvIdx1],[coIdx2,uvIdx2],[coIdx3,uvIdx3]]]

    
    Parameters
    ----------
    
    path:
        *string*. The file system path to the file to be read.
        
    groups:
        *Boolean*. It True, the facegroup names are included in the list.
       
    """

    try:
        fileDescriptor = open(path)
    except:
        print 'Error opening %s file' % path
        return
    vertsIdxs = []
    for data in fileDescriptor:
        dataList = data.split()
        if groups and dataList[0] == 'g':
            vertsIdxs.append(dataList[1])
        if dataList[0] == 'f':
            vIndices = []
            for faceData in dataList[1:]:
                vInfo = faceData.split('/')
                vIdx = int(vInfo[0]) - 1  # -1 because obj is 1 based list
                if len(vInfo) > 1 and vInfo[1] != '':
                    uvIdx = int(vInfo[1]) - 1  # -1 because obj is 1 based list
                    vIndices.append([vIdx, uvIdx])
                else:
                    vIndices.append([vIdx, 0])
            vertsIdxs.append(vIndices)
    fileDescriptor.close()
    return vertsIdxs


def loadUV(path):
    """
    This function loads just face UV data from a Wavefront obj file. 
   
    It can be used to save the same mesh with different UV layouts.
    
    Parameters
    ----------
    
    path:
        *string*. The file system path to the file to be read.
       
    """

    try:
        fileDescriptor = open(path)
    except:
        print 'Error opening %s file' % path
        return
    uvIndices = []
    uvValues = []
    for data in fileDescriptor:
        dataList = data.split()
        if dataList[0] == 'vt':

            # We just take the full list of uv values as-is

            uvValues.append([float(dataList[1]), float(dataList[2])])
    fileDescriptor.close()
    return uvValues

