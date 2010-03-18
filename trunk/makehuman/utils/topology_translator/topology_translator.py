# You may use, modify and redistribute this module under the terms of the GNU GPL3.0.
"""
Translate a  morph target from a mesh with topology 1 to a mesh with topology 2

===========================  ==================================================================
Project Name:                **MakeHuman**
Module File Location:        utils/topology_translator/topology_translator.py
Product Home Page:           http://www.makehuman.org/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2010
Licensing:                   GPL3 (see also: http://sites.google.com/site/makehumandocs/licensing)
Coding Standards:            See http://sites.google.com/site/makehumandocs/developers-guide#TOC-Coding-Style
===========================  ==================================================================


"""

from math import sqrt
from aljabr import *
import simpleoctree
import sys





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
    try:
        fileDescriptor = open(path)
    except:
        print 'Error opening %s file' % path
        return
    verts = []
    faces = []
    for data in fileDescriptor:
        lineData = data.split()

        if lineData[0] == 'v':
            co = [float(lineData[1]), float(lineData[2]), float(lineData[3])]
            verts.append(co)
    fileDescriptor.close()

    return verts



def tesselate(path, vertices):
    """
    This function make a very simple tesselation, based on verts only.


    Parameters
    ----------

    path:
        *string*. The wavefront obj to tesselate. It's needed to get the
        faces informations.

    vertices:
        *list*. The list of verts coords to be subdivided. They can't be loaded from
        the wavefront above, because it's supposed the coordinates are
        changed by previously applied morphs.

    """

    try:
        fileDescriptor = open(path)
    except:
        print 'Error opening %s file' % path
        return

    faces = []
    for data in fileDescriptor:
        lineData = data.split()

        if lineData[0] == 'f':
            face = []
            for faceData in lineData[1:]:
                vInfo = faceData.split('/')
                vIdx = int(vInfo[0]) - 1  # -1 because obj is 1 based list
                face.append(vIdx)
            faces.append(face)
    fileDescriptor.close()

    subdividedVerts = []
    for face in faces:
        centroidVerts = []
        if len(face) == 4:
            i0 = face[0]
            i1 = face[1]
            i2 = face[2]
            i3 = face[3]
            newVert1 = centroid([vertices[i0],vertices[i1]])
            newVert2 = centroid([vertices[i1],vertices[i2]])
            newVert3 = centroid([vertices[i2],vertices[i3]])
            newVert4 = centroid([vertices[i3],vertices[i0]])
            newVert5 = centroid([newVert1,newVert2,newVert3,newVert4])
            newVert6 = centroid([vertices[i0],newVert1,newVert5,newVert4])
            newVert7 = centroid([newVert1,vertices[i1],newVert5,newVert1])
            newVert8 = centroid([newVert5,newVert2,vertices[i2],newVert3])
            newVert9 = centroid([newVert4,newVert5,newVert3,vertices[i3]])
            newVert10 = centroid([vertices[i0],vertices[i1],newVert5])
            newVert11 = centroid([vertices[i1],vertices[i2],newVert5])
            newVert12 = centroid([vertices[i2],vertices[i3],newVert5])
            newVert13 = centroid([vertices[i3],vertices[i0],newVert5])
            subdividedVerts.extend([newVert5,newVert6,newVert7,newVert8,newVert9,newVert10,newVert11,newVert12,newVert13])
        elif len(face) == 3:
            i0 = face[0]
            i1 = face[1]
            i2 = face[2]
            newVert1 = centroid([vertices[i0],vertices[i1]])
            newVert2 = centroid([vertices[i1],vertices[i2]])
            newVert3 = centroid([vertices[i2],vertices[i0]])
            newVert4 = centroid([newVert1,newVert2,newVert3])
            newVert5 = centroid([vertices[i0],newVert1,newVert4,newVert3])
            newVert6 = centroid([newVert1,vertices[i1],newVert2,newVert4])
            newVert7 = centroid([newVert2,vertices[i2],newVert3,newVert4])
            newVert8 = centroid([vertices[i0],vertices[i1],newVert4])
            newVert9 = centroid([vertices[i1],vertices[i2],newVert4])
            newVert10 = centroid([vertices[i2],vertices[i0],newVert4])
            subdividedVerts.extend([newVert4,newVert5,newVert6,newVert7,newVert8,newVert9,newVert10])


    finalVertList = vertices + subdividedVerts
    print "ORIGINAL VERTS: %i"%(len(vertices))
    print "VERTS ADDED BY SUBDIVISION: %i"%(len(subdividedVerts))
    return finalVertList



def loadTranslationTarget(vertsList, targetPath):
    """
    This function load and apply, with value 1, a morph target.


    Parameters
    ----------

    vertsList:
        *list*. The list of verts coords to be modified by the morph.

    path:
        *string*. The wavefront obj to tesselate. It's needed to get the
        faces informations.

    vertsList:
        *list*. The vertices to be subdivided. They can't be loaded from
        the wavefront above, because it's supposed the coordinates are
        changed by previously applied morphs.

    """
    try:
        fileDescriptor = open(targetPath)
    except:
        print 'Unable to open %s', targetPath
        return

    for line in fileDescriptor:
        translationData = line.split()
        if len(translationData) == 4:
            vertIndex = int(translationData[0])
            # Adding the translation vector
            vertsList[vertIndex][0] += float(translationData[1])
            vertsList[vertIndex][1] += float(translationData[2])
            vertsList[vertIndex][2] += float(translationData[3])
    fileDescriptor.close()
    return True




def saveData(newMeshPath, oldMeshPath, dataPath):

    #We load the old mesh coords, and then tesselate it, in order
    #to have a better result in linking new mesh.
    vertsList1 = loadVertsCoo(newMeshPath)
    vertsList2 = tesselate(oldMeshPath, loadVertsCoo(oldMeshPath))

    overwrite = 0 #Just for more elegant one-line print output progress

    for i,v in enumerate(vertsList2):
        v.append(i)

    octree = simpleoctree.SimpleOctree(vertsList2, .25)
    try:
        fileDescriptor = open(dataPath, 'w')
    except:
        print 'Unable to open %s', dataPath
        return None

    #For each vert of new mesh we found the nearest verts of old one
    for i1,v1 in enumerate(vertsList1):


        vIndices = []
        vDistances = []

        #We use octree to search only on a small part of the whole old mesh.
        vertsList3 = octree.root.getSmallestChild(v1)

        #This dictionary is needed to have an ordered list of distances
        distData = {}

        #... find nearest verts on old mesh
        for i2,v2 in enumerate(vertsList3.verts):
            d = vdist(v1, v2)
            distData[d]=v2[3]

        #The trick to have an ordered list of distances, linked to the indices.
        #We use distances as keys.
        dKeys = distData.keys()
        dKeys.sort()
        dmin = dKeys[0] #The first one is the smallest.

        #in case of smaller distance < 0.005
        #new vert and old vert are coincided, so no more verts are needed.
        if  dKeys[0] < 0.005:
            vIndices = [distData[dKeys[0]]]
            vDistances = [dKeys[0]]

        #else we get the 7 first verts with smaller distance
        else:
            if len(dKeys) > 7:
                vDistances = dKeys[:7]
            else:
                vDistances = dKeys[:(len(dKeys)-1)]
            vIndices = [distData[n] for n in vDistances]

        #Now we have verts indices and distances from the input vert, so
        #we can calculate their weights
        if dmin > 0:
            weights = [dmin/dst for dst in vDistances]
        else:
            weights = [1]

        #Finally we write the data
        for index in vIndices:
            fileDescriptor.write('%i ' % (index))
        for weight in weights:
            fileDescriptor.write('%f ' % (weight))
        fileDescriptor.write('\n')


        word = "Linking verts: %.2f%c."%((float(i1)/len(vertsList1))*100, "%")
        sys.stdout.write("%s%s\r" % (word, " "*overwrite ))
        sys.stdout.flush()
        overwrite = len(word)


    fileDescriptor.close()




def translateMorph(objOldPath, targetOldPath, objNewPath, oldMeshPath, dataPath):


    vertsOld1 = loadVertsCoo(objOldPath)
    vertsNew = loadVertsCoo(objNewPath)
    loadTranslationTarget(vertsOld1, targetOldPath)
    vertsOld = tesselate(oldMeshPath, vertsOld1)

    try:
        fileDescriptor = open(dataPath)
    except:
        print 'Unable to open %s', dataPath
        return

    idx = 0
    for line in fileDescriptor:
        translationData = line.split()

        halfList = len(translationData)/2
        xIdx = translationData[:halfList]
        xWeight = translationData[halfList:]
        xSum = [0,0,0]
        sumWeight = 0
        for w in xWeight:
            sumWeight += float(w)

        for i in range(len(xIdx)):
            index = int(xIdx[i])
            weight = float(xWeight[i])

            vertOld = vmul(vertsOld[index],weight)
            xSum = vadd(xSum,vertOld)

            if idx == 9030:
                print "weight", weight
                print "vert old", vertsOld[index]

        vertsNew[idx] = vmul(xSum,1.0/sumWeight)
        idx += 1
    fileDescriptor.close()
    return vertsNew




def saveTranslationTarget(objPath, targetPath, targetVerts, epsilon=0.001):


    originalVerts = loadVertsCoo(objPath)
    modifiedVertsIndices = []
    nVertsExported = 0
    for i in range(len(targetVerts)):

        originalVertex = originalVerts[i]
        targetVertex = targetVerts[i]

        delta = vsub(targetVertex, originalVertex)
        dist = vdist(originalVertex, targetVertex)

        if dist > epsilon:
            nVertsExported += 1
            dataToExport = [i, delta[0], delta[1], delta[2]]
            modifiedVertsIndices.append(dataToExport)
    try:
        fileDescriptor = open(targetPath, 'w')
    except:
        print 'Unable to open %s', targetPath
        return None

    for data in modifiedVertsIndices:
        fileDescriptor.write('%d %f %f %f\n' % (data[0], data[1], data[2], data[3]))
    fileDescriptor.close()

    print 'Exported %d verts '%(nVertsExported)













saveData("baseNew.obj", "baseOld.obj", "diff.data")


vertsToSave = translateMorph("baseOld.obj", "test.target", "baseNew.obj","baseOld.obj", "diff.data")
saveTranslationTarget("baseNew.obj", "result.target", vertsToSave, epsilon=0.001)




