#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Modules to handle supported 3D file formats. 

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010

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

__docformat__ = 'restructuredtext'

import time
import module3d
import os
import algos3d


def isFile(path):
    """
    This function tests whether the specified path points to a file on the file system.
    If the file exists it returns a 1. Otherwise it returns 0.

    Parameters
    ----------
    
    path:
        *string*. The file system path to the file to be checked.
    
    """

    # because os module is not in standard python dll

    try:
        fileDescriptor = open(path, 'r')
        fileDescriptor.close()
        return 1
    except:
        return None


def dataTo3Dobject(obj, data, addSharedFaces=1):
    """
    This function creates a 3D object based upon a standardised input data stream.
    The object created is held in memory in the standard internal MakeHuman data format.
    
    Parameters
    ----------
    
    obj:
        *3D object*. The object to create.

    data:
        *list of various data*. The data to be used to fill the object.

    addSharedFaces:
        *int flag*. Whether or not to perform the 'shared faces' analysis (1=Yes, 0=No).
        
    """

    time1 = time.time()
    if not data:
        return None

    verts = data[0]  # vertex index -> coords [x, y, z]
    vertsSharedFaces = data[1]  # vertex index -> faceindices
    uvValues = data[2]  # uv index -> uv [u, v]
    faceGroups = data[3]  # group name -> faces [co_index1, co_index2, co_index3]
    faceGroupsNames = data[4]  # group names
    uvFaceData = data[5]  # face index -> uv face [uv_index1, uv_index2, uv_index3]

    # print "DEBUG FACEGROUP",faceGroupsNames

    for (i, v) in enumerate(verts):
        v = module3d.Vert(v, i, obj)
        obj.verts.append(v)

    gIndex = 0
    fIndex = 0
    fullArrayIndex = 0

    obj.uvValues = uvValues

    for groupName in faceGroupsNames:
        group = faceGroups[groupName]
        groupVerts = {}

        fg = module3d.FaceGroup(groupName)  # create group with name groupName
        obj.addFaceGroup(fg)  # add group to object
        for face in group:  # for each face in the group [co_index1, co_index2, co_index3, co_index4]
            v0 = obj.verts[face[0]]  # look up vertices, these are in the same order as in the file
            v1 = obj.verts[face[1]]
            v2 = obj.verts[face[2]]
            v3 = obj.verts[face[3]]
            
            f = fg.createFace(v0, v1, v2, v3)

            if len(uvFaceData) > 0:  # look up uv, if existing, these are in the same order as in the file
                uvIndices = uvFaceData[fIndex]
                f.uv = uvIndices[:]

            f.idx = fIndex
            fIndex += 1

    if addSharedFaces:
        for v in obj.verts:
            for i in vertsSharedFaces[v.idx]:

                # print i, len(obj.faces), obj.name, vertsSharedFaces[v.idx]

                v.sharedFaces.append(obj.faces[i])

    #print 'time to build mesh: ', time.time() - time1

    obj.calcNormals()
    obj.updateIndexBuffer()

def wavefrontToData(path):
    """
    This function reads a file containing data in WaveFront format and loads it
    into a standardised intermediate data structure.

    Note: This function converts all polygonal faces into triangles.

    Developers note: Need to be modified in order to load sparse face groups data.

    Parameters
    ----------
    
    path:
        *string*. The file system path to the file to be imported.

    """

    t1 = time.time()

    vertsUV = []
    faceGroupsNames = []

    faceGroups = {}
    currentFaceGroup = 'default-dummy-group'
    faceGroups[currentFaceGroup] = []

    verts = []
    vertsSharedFaces = []
    faceIndex = 0
    uvValues = []
    uvFaceData = []

    try:
        ObjFile = open(path)
    except:
        print 'Warning: obj file not found: ', path
        return None

    for objData in ObjFile.readlines():

        lineData = objData.split()
        if len(lineData) > 0:
            if lineData[0] == 'g':
                name = lineData[1]
                currentFaceGroup = name
                faceGroups[currentFaceGroup] = []
                faceGroupsNames.append(currentFaceGroup)
            elif lineData[0] == 'v':

                vData = [float(lineData[1]), float(lineData[2]), float(lineData[3])]
                verts.append(vData)
                vertsUV.append([0, 0])

                # For each vert, append an empty list to vertsSharedFaces

                vertsSharedFaces.append([])
            elif lineData[0] == 'vt':

                # We just take the full list of uv values as-is

                uvValues.append([float(lineData[1]), float(lineData[2])])
            elif lineData[0] == 'f':

                faceIndices = []
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

                # Four sided polygons need to be split into triangles in exactly the same
                # sequence as is done for verts coords.

                if len(uvIndices) == 4:
                    uvFaceData.append([uvIndices[0], uvIndices[1], uvIndices[2], uvIndices[3]])
                elif len(uvIndices) == 3:
                    uvFaceData.append([uvIndices[0], uvIndices[1], uvIndices[2], uvIndices[0]])

                # Split quads in trigs

                if len(vIndices) == 4:
                    vertsSharedFaces[vIndices[0]].append(faceIndex)
                    vertsSharedFaces[vIndices[1]].append(faceIndex)
                    vertsSharedFaces[vIndices[2]].append(faceIndex)
                    vertsSharedFaces[vIndices[3]].append(faceIndex)
                    faceGroups[currentFaceGroup].append(vIndices)
                    faceIndex += 1
                elif len(vIndices) == 3:

                    vertsSharedFaces[vIndices[0]].append(faceIndex)
                    vertsSharedFaces[vIndices[1]].append(faceIndex)
                    vertsSharedFaces[vIndices[2]].append(faceIndex)
                    faceGroups[currentFaceGroup].append([vIndices[0], vIndices[1], vIndices[2], vIndices[0]])
                    faceIndex += 1
                else:
                    print 'Warning, malformed faces in %s' % path

    ObjFile.close()
    if len(faceGroupsNames) == 0:
        faceGroupsNames.append('default-dummy-group')

    #print 'loading wavefront %s in %f sec' % (path, time.time() - t1)
    return [verts, vertsSharedFaces, uvValues, faceGroups, faceGroupsNames, uvFaceData]


def saveWavefrontObj(ob, path):
    """
    This function reads the vertex and face information (including face groups)
    from an object in memory and writes a file in WaveFront format. 
    The internal MakeHuman data structures are used to construct a WaveFront file. 
    
    Parameters
    ----------
    
    ob:
        *3D object*. The object from which to read vertex and face information.
    
    path:
        *string*. The file system path to the file to be written.

    """

    print 'Saving wavefront obj...verts n.', len(ob.verts)
    t1 = time.time()
    try:
        fileDescriptor = open(path, 'w')
    except:
        print 'Impossible to save %s' % path

    fileDescriptor.write('#Exported from MakeHuman\n')
    fileDescriptor.write('#http://www.makehuman.org\n')

    for v in ob.verts:
        fileDescriptor.write('v %f %f %f\n' % (v.co[0], v.co[1], v.co[2]))

    for v in ob.verts:
        fileDescriptor.write('vt %f %f\n' % (v.uv[0], v.uv[1]))

    for g in ob.facesGroups:
        fileDescriptor.write('g %s\n' % g.name)
        for f in g.faces:
            fileDescriptor.write('f ')
            for v in f.verts:

                # +1 because wavefront obj is "1 based" list

                fileDescriptor.write('%i/%i ' % (v.idx + 1, v.idx + 1))
            fileDescriptor.write('\n')
    fileDescriptor.close()
    print 'Wavefront obj exported in %s sec.' % (time.time() - t1)


def wavefrontToData_simple(path):
    """
    This function serves as a template upon which other importers should be 
    based. Other importers should also follow the same naming convention
    (e.g. 3dsToData, lightwaveToData, etc.). See the wavefrontToData function 
    above for a worked example.
    
    This function reads a file containing data in WaveFront format and loads it
    into a standardised intermediate data structure.
    Note: This function converts all polygonal faces into triangles.

    Parameters
    ----------
    
    path:
        *string*. The file system path to the file to be imported.
    """

    verts = []
    vertsSharedFaces = []
    fg = []
    vertsUV = []
    t1 = time.time()
    try:
        ObjFile = open(path)
    except:
        print 'Warning: obj file not found'

    objData = ObjFile.readline()
    while objData:
        lineData = objData.split()
        if len(lineData) > 0:

            if lineData[0] == 'v':
                vData = [float(lineData[1]), float(lineData[2]), float(lineData[3])]
                verts.append(vData)
                vertsUV.append([0, 0])
                vertsSharedFaces.append([])
            elif lineData[0] == 'f':

                uvIndices = []
                vIndices = []
                for faceData in lineData[1:]:
                    vInfo = faceData.split('/')
                    vIdx = int(vInfo[0]) - 1  # -1 because obj is 1 based list
                    vIndices.append(vIdx)
                fg.append(vIndices)

        objData = ObjFile.readline()
    ObjFile.close()
    #print 'loading wavefront in s.', time.time() - t1
    return [verts, vertsSharedFaces, vertsUV, [fg], ['dummy']]


originalVertexCoordinates = None


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

    data = wavefrontToData(path)

    if data is None:
        return

    objName = os.path.basename(path)
    ob = scene.newObj(objName)

    ob.path = path
    ob.x = locX
    ob.y = locY
    ob.z = locZ
    dataTo3Dobject(ob, data)
    if loadColors:
        colorPath = path + '.colors'
        algos3d.loadVertsColors(ob, colorPath, None)
    return ob


