# You may use, modify and redistribute this module under the terms of the GNU AGPL3.0.
"""
Translate a  morph target from a mesh with topology 1 to a mesh with topology 2
The shape of old and new objs must be similar. We assume the new mesh is done using a retopology tool.

===========================  ==================================================================
Project Name:                **MakeHuman**
Module File Location:        utils/topology_translator/topologylib.py
Product Home Page:           http://www.makehuman.org/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2013
Licensing:                   AGPL3 (see also: http://www.makehuman.org/node/318)
Coding Standards:            See http://www.makehuman.org/node/165#TOC-Coding-Style
===========================  ==================================================================


"""
import sys
sys.path.append("../../core/")
from math import sqrt
from aljabr import *
import simpleoctree
import sys
import os
import copy





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
        if len(lineData) > 2:
            if lineData[0] == 'v':
                co = [float(lineData[1]), float(lineData[2]), float(lineData[3])]
                verts.append(co)
    fileDescriptor.close()

    return verts


def loadFacesIndices(path):
    """
    This function serves as a small utility function to load just the  face indices
    data from a WaveFront object file.

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

    faces = []
    for data in fileDescriptor:
        lineData = data.split()
        if len(lineData) > 2:
            if lineData[0] == 'f':
                face = []
                for faceData in lineData[1:]:
                    vInfo = faceData.split('/')
                    vIdx = int(vInfo[0]) - 1  # -1 because obj is 1 based list
                    face.append(vIdx)
                faces.append(face)
    fileDescriptor.close()
    return faces

def subdivideObj(faces, vertices, loops):
    for n in xrange(loops):
        faces,vertices = tessellate(faces, vertices)
    return (faces,vertices)



def tessellate(faces, vertices):
    """
    This function make a very simple tesselation, based on verts only.


    Parameters
    ----------
    faces:
        *list*. Each "face" is a list with the index of face verts. Faces is a list of these lists.
    

    vertices:
        *list*. The list of verts coords to be subdivided. They can't be loaded from
        the wavefront above, because it's supposed the coordinates are
        changed by previously applied morphs.

    """

    subdividedVerts = []
    subdividedFaces = []

    idx = len(vertices)-1
    vertsUsed = {}
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

            k1 = [i0,i1]
            k2 = [i1,i2]
            k3 = [i2,i3]
            k4 = [i3,i0]
            k5 = [i0,i1,i2,i3]

            k1.sort()
            k2.sort()
            k3.sort()
            k4.sort()
            k5.sort()

            key1 = str(k1)
            key2 = str(k2)
            key3 = str(k3)
            key4 = str(k4)
            key5 = str(k5)


            if not vertsUsed.has_key(key1):
                idx += 1
                vertsUsed[key1] = idx
                subdividedVerts.append(newVert1)
                n1 = idx
            else:
                n1 = vertsUsed[key1]

            if not vertsUsed.has_key(key2):
                idx += 1
                vertsUsed[key2] = idx
                subdividedVerts.append(newVert2)
                n2 = idx
            else:
                n2 = vertsUsed[key2]

            if not vertsUsed.has_key(key3):
                idx += 1
                vertsUsed[key3] = idx
                subdividedVerts.append(newVert3)
                n3 = idx
            else:
                n3 = vertsUsed[key3]

            if not vertsUsed.has_key(key4):
                idx += 1
                vertsUsed[key4] = idx
                subdividedVerts.append(newVert4)
                n4 = idx
            else:
                n4 = vertsUsed[key4]

            if not vertsUsed.has_key(key5):
                idx += 1
                vertsUsed[key5] = idx
                subdividedVerts.append(newVert5)
                n5 = idx
            else:
                n5 = vertsUsed[key5]

            newFace1 = [i0,n1,n5,n4]
            newFace2 = [n1,i1,n2,n5]
            newFace3 = [n5,n2,i2,n3]
            newFace4 = [n5,n3,i3,n4]

            subdividedFaces.extend([newFace1,newFace2,newFace3,newFace4])

        elif len(face) == 3:
            i0 = face[0]
            i1 = face[1]
            i2 = face[2]

            newVert1 = centroid([vertices[i0],vertices[i1]])
            newVert2 = centroid([vertices[i1],vertices[i2]])
            newVert3 = centroid([vertices[i2],vertices[i0]])
            newVert4 = centroid([newVert1,newVert2,newVert3])

            #Create an unique ID of each new vert, using a sorted list of
            #vert indices used to calculate it.
            k1 = [i0,i1]
            k2 = [i1,i2]
            k3 = [i2,i0]
            k4 = [i0,i1,i2]
            k1.sort()
            k2.sort()
            k3.sort()
            k4.sort()
            key1 = str(k1)
            key2 = str(k2)
            key3 = str(k3)
            key4 = str(k4)



            if not vertsUsed.has_key(key1):
                idx += 1
                vertsUsed[key1] = idx
                subdividedVerts.append(newVert1)
                n1 = idx
            else:
                n1 = vertsUsed[key1]

            if not vertsUsed.has_key(key2):
                idx += 1
                vertsUsed[key2] = idx
                subdividedVerts.append(newVert2)
                n2 = idx
            else:
                n2 = vertsUsed[key2]

            if not vertsUsed.has_key(key3):
                idx += 1
                vertsUsed[key3] = idx
                subdividedVerts.append(newVert3)
                n3 = idx
            else:
                n3 = vertsUsed[key3]

            if not vertsUsed.has_key(key4):
                idx += 1
                vertsUsed[key4] = idx
                subdividedVerts.append(newVert4)
                n4 = idx
            else:
                n4 = vertsUsed[key4]

            newFace1 = [i0,n1,n4]
            newFace2 = [n1,i1,n4]
            newFace3 = [i1,n2,n4]
            newFace4 = [n2,i2,n4]
            newFace5 = [i2,n3,n4]
            newFace6 = [n3,i0,n4]
            subdividedFaces.extend([newFace1,newFace2,newFace3,newFace4,newFace5,newFace6])

    finalVertList = vertices + subdividedVerts
    finalFacesList = subdividedFaces
    print "ORIGINAL VERTS: %i"%(len(vertices))
    print "VERTS ADDED BY SUBDIVISION: %i"%(len(subdividedVerts))
    print "TOTAL VERTICES ADDED %i"%len(finalVertList)
    return (finalFacesList, finalVertList)







def applyMorph(vertsList, targetPath):
    """
    This function load and apply, with value 1, a morph target.


    Parameters
    ----------

    vertsList:
        *list*. The list of verts coords to be modified by the morph.

    path:
        *string*. The wavefront obj to tesselate. It's needed to get the
        faces informations.

    """
    newVertsList = copy.deepcopy(vertsList)
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
            newVertsList[vertIndex][0] = vertsList[vertIndex][0] + float(translationData[1])
            newVertsList[vertIndex][1] = vertsList[vertIndex][1] + float(translationData[2])
            newVertsList[vertIndex][2] = vertsList[vertIndex][2] + float(translationData[3])
    fileDescriptor.close()
    return newVertsList




def meshComparison(vertsList1, vertsList2, faces2, indexListPath = None):
    """
    This function measure the similarity of 2 meshes.
    Instead to have ray intersection to measure the surfaces differences,
    we subdivide the mesh2, in order to in increase the density, and then
    we use the vert to vert distance.


    Parameters
    ----------

    mesh1:
        *string*. The path of the new wavefront obj

    mesh2:
        *string*. The path of the old wavefront obj
   

    """  

    if indexListPath:
        indexList = []
        try:
            fileDescriptor = open(indexListPath)
        except:
            print 'Error opening %s file' % path
            return        
        for data in fileDescriptor:
            lineData = data.split()            
            i = int(lineData[0])
            indexList.append(i)
        fileDescriptor.close()
    else:
        indexList = xrange(len(vertsList1))

    tess = subdivideObj(faces2, vertsList2, 2)  

    overwrite = 0 #Just for more elegant one-line print output progress
    
    #Init of the octree
    octree = simpleoctree.SimpleOctree(tess[1] , .25)   

    #For each vert of new mesh we found the nearest verts of old one
    vDistances = []
    for i1 in indexList:
        v1 = vertsList1[i1]       

        #We use octree to search only on a small part of the whole old mesh.
        vertsList3 = octree.root.getSmallestChild(v1)

        #... find nearest verts on old mesh
        dMin = 100
        for v2 in vertsList3.verts:
            d = vdist(v1, v2)            
            if d < dMin:
                dMin = d

        vDistances.append(dMin)
        

        word = "Linking verts: %.2f%c."%((float(i1)/len(vertsList1))*100, "%")
        sys.stdout.write("%s%s\r" % (word, " "*overwrite ))
        sys.stdout.flush()
        overwrite = len(word)

    dSum = 0
    for d in vDistances:
        dSum += d

    averageDist = dSum/len(vDistances)

    print "Average distance %s %s = %s"%(mesh1,mesh2,averageDist)
    return averageDist
        

def saveData(vertsList1, vertsList2, faces2, dataPath, epsilon = 0.2):
    """
    This function link the mesh1 to the mesh2.
    It find, for each vert of the mesh2, one or more verts (max 7) on the mesh1,
    that are the nearest to the input one. Then, each vert is saved on the data ascii file,
    with its weight calculated in function of the distance from the input vert, as well.


    Parameters
    ----------

    mesh1:
        *string*. The path of the new wavefront obj

    mesh2:
        *string*. The path of the old wavefront obj

    dataPath:
        *string*. The path of data file to save

    epsilon:
        *float*. Threshold

    """
    print "building data..."

    #We load the old mesh coords, and then tesselate it, in order
    #to have a better result in linking new mesh.
    tess = subdivideObj(faces2, vertsList2, 2)    
    vertsList2Tesselated = tess[1]
    
    deltaVectors = []
    notLinked = 0

    overwrite = 0 #Just for more elegant one-line print output progress

    #We need to add index information to each vert.    
    for i,v in enumerate(vertsList2Tesselated):
        v.append(i)

    #Init of the octree
    octree = simpleoctree.SimpleOctree(vertsList2Tesselated, .25)

    try:
        fileDescriptor = open(dataPath, 'w')
    except:
        print 'Unable to open %s'%(dataPath)
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
            distData[d]=v2[3] #v2[3] is the vert index

        #The trick to have an ordered list of distances, linked to the indices.
        #We use distances as keys.
        dKeys = distData.keys()
        dKeys.sort()
        dmin = dKeys[0] #The first one is the smallest.

        if dmin < epsilon: #A vert is found in the given epsilon

            #in case of smaller distance < 0.005
            #new vert and old vert are coincided, so no more verts are needed.
            if  dKeys[0] < 0.005:
                vIndices = [distData[dKeys[0]]]
                vDistances = [dKeys[0]]
                weights = [1]

            #else we get the 7 first verts with smaller distance
            else:
                if len(dKeys) > 7:
                    vDistances = dKeys[:7]
                else:
                    vDistances = dKeys[:(len(dKeys)-1)]
                vIndices = [distData[n] for n in vDistances]
                weights = [dmin/dst for dst in vDistances]

            #The delta vector, between the vert of v1 and the centroid of neighbours verts of v2
            vx = centroid([vertsList2Tesselated[vIndx] for vIndx in vIndices])
            deltaVect = vsub(vx,v1)
            deltaVectors.append(deltaVect)

            #Finally we write the data
            for index in vIndices:
                fileDescriptor.write('%i ' % (index))
            for weight in weights:
                fileDescriptor.write('%f ' % (weight))
            fileDescriptor.write('\n')
        else:
            fileDescriptor.write('%i\n' % (-1))
            deltaVectors.append(-1)
            notLinked += 1

        word = "Linking verts: %.2f%c."%((float(i1)/len(vertsList1))*100, "%")
        sys.stdout.write("%s%s\r" % (word, " "*overwrite ))
        sys.stdout.flush()
        overwrite = len(word)

    fileDescriptor.close()

    try:
        fileDescriptor = open(dataPath+".delta", 'w')
    except:
        print 'Unable to open %s'%(dataPath)
        return None

    for delta in deltaVectors:
        if delta != -1:
            fileDescriptor.write('%f %f %f\n' % (delta[0], delta[1], delta[2]))
        else:
            fileDescriptor.write('-1 \n')
    fileDescriptor.close()

    print "Data saved in %s"%(dataPath)
    print "Verts not linked with a epsilon radius of %f: %i"%(epsilon,notLinked)




def fitMesh(verts1, verts2, faces2, dataPath, targetPath=None):

    """
    This function load the mesh1 and the mesh2, and then fit
    the mesh1 to the mesh2. No targets are required, because
    mesh2 is supposed to be already morphed. So I call this function
    convert Direct, because the convertion is directly from mesh2
    to mesh1.


    Parameters
    ----------

    mesh1:
        *string*. The path of the obj to fit

    mesh2:
        *string*. The path of mold obj

    targetPath:
        *string*. The path of data file to use for fitting. If noe, it's
        assumed that mesh2 is the final form of mesh1.

    """

    #apply target, in case
    if targetPath:
        morphedVerts = set() #Set of indices of vertices affected by target
        verts2U = copy.deepcopy(verts2) #unmorphed verts
        verts2 = applyMorph(verts2, targetPath) #morphed verts

        #We need to consider only verts that get deformed by the morph
        vertTessU = subdivideObj(faces2, verts2U, 2)[1] #unmorphed subdivided verts
        vertTess = subdivideObj(faces2, verts2, 2)[1] #morphed subdivided verts

        #Fill the list of verts affected by the target
        for i in xrange(len(vertTessU)):
            if vertTessU[i] != vertTess[i]:
                morphedVerts.add(i)
    else:
        #tesselate
        vertTess = subdivideObj(faces2, verts2, 2)[1]

    try:
        fileDescriptor = open(dataPath)
    except:
        print 'Unable to open %s'%(dataPath)
        return

    fileData =  fileDescriptor.readlines()
    fileDescriptor.close()

    try:
        fileDescriptor = open(dataPath+".delta")
    except:
        print 'Unable to open %s'%(dataPath)
        return

    fileDelta =  fileDescriptor.readlines()
    fileDescriptor.close()

    #The datafile must have the same lines as the verts of mesh1
    if len(fileData) != len(verts1):
        print "ERROR: data file was done for a different meshtofit"
        return None

    for idx,line in enumerate(fileData):
        translationData = line.split()

        deltaData = fileDelta[idx].split()
        if deltaData[0] != '-1':

            deltaVect = (float(deltaData[0]), float(deltaData[1]), float(deltaData[2]))

        halfList = len(translationData)/2

        #The first half of line are verts Indices
        xIdx = translationData[:halfList]
        #The second half of line are verts weight
        xWeight = translationData[halfList:]

        xSum = [0,0,0]
        sumWeight = 0
        for w in xWeight:
            sumWeight += float(w)

        isMorphed = False
        for i in xrange(len(xIdx)):
            index = int(xIdx[i])
            if targetPath: #If target, we must check the vert is affected by it
                if index in morphedVerts:
                    isMorphed = True
            else:
                isMorphed = True  #If not target, all verts are assumed as morphed
            weight = float(xWeight[i])
            try:
                linkedVert = vmul(vertTess[index],weight)
            except:
                print "ERROR: wrong datafile used"
                return None
            xSum = vadd(xSum,linkedVert)

        if isMorphed:
            #verts1[idx] = vmul(xSum,1.0/sumWeight)
            verts1[idx] = vsub(vmul(xSum,1.0/sumWeight),deltaVect)


    return verts1






def saveTestObj(faces, verts, objTestPath):

    """
    This function load the old mesh verts, morph it and transfer the
    deformations on the new mesh verts.


    Parameters
    ----------


    """

    try:
        fileDescriptor = open(objTestPath, 'w')
    except:
        print 'Unable to open %s'%(objTestPath)
        return

    for v in verts:
        fileDescriptor.write('v %f %f %f\n' % (v[0], v[1], v[2]))
    for f in faces:
        if len(f) == 4:
            fileDescriptor.write('f %i %i %i %i\n' % (f[0]+1, f[1]+1, f[2]+1, f[3]+1))
        if len(f) == 3:
            fileDescriptor.write('f %i %i %i\n' % (f[0]+1, f[1]+1, f[2]+1))
    print "Saved a test obj in %s"%(objTestPath)

    fileDescriptor.close()




def convertFile(vertList1, vertList2, faces2, dataPath, originalVerts, convertedName, targetbase = None, targetToConvert = None, epsilon=0.001):

    """
    This function call the main functions in order to convert the morphing.
    Then save the target in our standard format.


    Parameters
    ----------
    targetToConvert:
        *string*. The path of old morph target to convert

    targetbase:
        *string*. The obj to use as target base.

    mesh1:
        *string*. The path of the new wavefront obj

    mesh2:
        *string*. The path of the old wavefront obj

    dataPath:
        *string*. The path of data file to save

    epsilon:
        *float*. The threshold to decide when consider or not a modification as
        morph to be saved.

    """
    convertDirectory = os.path.join(os.path.dirname(dataPath), "converted")
    if not os.path.isdir(convertDirectory):
        os.mkdir(convertDirectory)

    if targetToConvert:
        #verts are modified by target
        #The new target has the same name, but it's saved in the "converted" directory
        newTargetPath = os.path.join(convertDirectory, os.path.basename(targetToConvert))
        modifiedVerts = fitMesh(vertList1, vertList2, faces2, dataPath, targetToConvert)
    else:
        #verts are modified by direct fitting
        #Because the target is from scratch it has the name assigned by convertedname variable
        print "DEBUG-NAME",convertedName
        newTargetPath = os.path.join(convertDirectory, os.path.basename(convertedName))
        modifiedVerts = fitMesh(vertList1, vertList2, faces2, dataPath)

    if modifiedVerts:
        #If not target base, we assume to save the target for a mesh1 base.
        
        print "Using datafile %s"%(dataPath)
        print "Saved target as %s"%(convertedName)

        modifiedVertsIndices = []
        nVertsExported = 0
        for i in xrange(len(modifiedVerts)):
            originalVertex = originalVerts[i]
            targetVertex = modifiedVerts[i]
            delta = vsub(targetVertex, originalVertex)
            dist = vdist(originalVertex, targetVertex)
            if dist > epsilon:
                nVertsExported += 1
                dataToExport = [i, delta[0], delta[1], delta[2]]
                modifiedVertsIndices.append(dataToExport)
        try:
            fileDescriptor = open(newTargetPath, 'w')
        except:
            print 'Unable to open %s'%(newTargetPath)
            return None

        for data in modifiedVertsIndices:
            fileDescriptor.write('%d %f %f %f\n' % (data[0], data[1], data[2], data[3]))
        fileDescriptor.close()

        print 'Exported %d verts '%(nVertsExported)
    else:
        print "ERROR in fitting mesh, file not converted"




