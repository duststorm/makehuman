# You may use, modify and redistribute this module under the terms of the GNU GPL3.0.
"""
Translate a  morph target from a mesh with topology 1 to a mesh with topology 2
The shape of old and new objs must be similar. We assume the new mesh is done using a retopology tool.

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
import getopt
import os





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
    for n in range(loops):        
        faces,vertices = tessellate(faces, vertices)
    return (faces,vertices)
    
    

def tessellate(faces, vertices):
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




def saveData(objNewPath, objOldPath, dataPath):
    """
    This function link the old mesh to the new one.
    It find, for each vert of the old mesh, one or more verts (max 7) on the new mesh,
    that are the nearest to the input one. Then, each vert is saved on the data ascii file,
    with its weight calculated in function of the distance from the input vert, as well.


    Parameters
    ----------

    objNewPath:
        *string*. The path of the new wavefront obj

    objOldPath:
        *string*. The path of the old wavefront obj

    dataPath:
        *string*. The path of data file to save

    """
    print "building data..."

    #We load the old mesh coords, and then tesselate it, in order
    #to have a better result in linking new mesh.
    vertsList1 = loadVertsCoo(objNewPath)
    vertices = loadVertsCoo(objOldPath)
    faces = loadFacesIndices(objOldPath)  
    tess = subdivideObj(faces, vertices, 2)
    vertsList2 = tess[1]

    #saveTestObj(tess[0], tess[1], "foo1.obj")
    
    overwrite = 0 #Just for more elegant one-line print output progress

    for i,v in enumerate(vertsList2):
        v.append(i)

    octree = simpleoctree.SimpleOctree(vertsList2, .25)
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
    print "Data saved in %s"%(dataPath)




def convertTargets(targetPath, objNewPath, objOldPath, dataPath):

    """
    This function load the old mesh verts, morph it and transfer the
    deformations on the new mesh verts.


    Parameters
    ----------
    targetPath:
        *string*. The path of morph target to convert

    objNewPath:
        *string*. The path of the new wavefront obj

    objOldPath:
        *string*. The path of the old wavefront obj

    dataPath:
        *string*. The path of data file to save

    """

    #Load the old mesh, morph it and then tessellate
    vertsOld = loadVertsCoo(objOldPath)
    facesOld = loadFacesIndices(objOldPath)
    #morph 
    loadTranslationTarget(vertsOld, targetPath)
    #tesselate    
    tess = subdivideObj(facesOld, vertsOld, 2)  
    vertsOldTessellated = tess[1]
    
    vertsNew = loadVertsCoo(objNewPath)   
    
    try:
        fileDescriptor = open(dataPath)
    except:
        print 'Unable to open %s'%(dataPath)
        return

    
    for idx,line in enumerate(fileDescriptor):
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
            vertOld = vmul(vertsOldTessellated[index],weight)
            xSum = vadd(xSum,vertOld)

        vertsNew[idx] = vmul(xSum,1.0/sumWeight)
        
    fileDescriptor.close()
    return vertsNew



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






def saveConvertedTarget(oldTargetPath, objNewPath, objOldPath, dataPath, epsilon=0.001):

    """
    This function call the main functions in order to convert the morphing.
    Then save the target in our standard format.


    Parameters
    ----------
    oldTargetPath:
        *string*. The path of old morph target to convert    

    objNewPath:
        *string*. The path of the new wavefront obj

    objOldPath:
        *string*. The path of the old wavefront obj

    dataPath:
        *string*. The path of data file to save

    epsilon:
        *float*. The threshold to decide when consider or not a modification as
        morph to be saved.

    """
    

    #modified verts are the verts of new mesh, modified by the morphing
    modifiedVerts = convertTargets(oldTargetPath, objNewPath, objOldPath, dataPath)

    #original verts are the verts of new mesh, unmodified.
    originalVerts = loadVertsCoo(objNewPath)  

    convertDirectory = os.path.join(os.path.dirname(oldTargetPath), "converted")
    if not os.path.isdir(convertDirectory):
        os.mkdir(convertDirectory)
    newTargetPath = os.path.join(convertDirectory, os.path.basename(oldTargetPath))

    print "Conversion of %s, from %s to %s"%(oldTargetPath,objOldPath,objNewPath)
    print "Using datafile %s"%(dataPath)
    print "Saved target as %s"%(newTargetPath)
    
    modifiedVertsIndices = []
    nVertsExported = 0
    for i in range(len(modifiedVerts)):
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
        print 'Unable to open %s'%(targetPath)
        return None

    for data in modifiedVertsIndices:
        fileDescriptor.write('%d %f %f %f\n' % (data[0], data[1], data[2], data[3]))
    fileDescriptor.close()

    print 'Exported %d verts '%(nVertsExported)


#saveData("baseNew.obj", "baseOld.obj", "diff.data")
#saveConvertedTarget("test.target", "baseNew.obj", "baseOld.obj", "diff.data")
#saveConvertedTarget(oldTargetPath, objNewPath, objOldPath, dataPath, epsilon=0.001)

def usage():    
    print""
    print"NAME"
    print"    %s: a program to translate a  morph target from"%(sys.argv[0])
    print"    a mesh with topology 1 to a mesh with topology 2"
    print"    The shape of old and new objs must be similar."
    print"    We assume the new mesh is done using a retopology tool."
    print""
    print"SYNOPSIS"
    print"    %s [options]"%(sys.argv[0])
    print""
    print"OPTIONS:"
    print"    --build; -b; build the database to be used in conversion"
    print"    --target; -t; to specify the target file to convert"
    print"    --oldbase; -o; to specify the old base wavefront obj"
    print"    --newbase; -n; to specify the new base wavefront obj"
    print"    --help: -h; what you're looking at right now."
    print""
    print"AUTHOR:"
    print"    Manuel Bastioni (info@makehuman.org)"
    print""
    print"SEE ALSO:"
    print"    MakeHuman web page:"
    print"    http://www.makehuman.org"
    print""        
    exit()


def main(argv):

    target = "test.target"
    oldbase = "baseOld.obj"
    newbase = "baseNew.obj"    
    datafile = "diff.data"
    buildit = None
    testobj = None

    #handle options
    try:
        opts, args = getopt.getopt(argv, "hbt:o:n:d:w:", ["help","build","target=","oldbase=","newbase=","datafile=","testobj="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()        
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-o", "--oldbase"):
            oldbase = arg
        elif opt in ("-n", "--newbase"):
            newbase = arg
        elif opt in ("-d", "--datafile"):
            datafile = arg
        elif opt in ("-b", "--build"):
            buildit = 1
        elif opt in ("-w", "--testobj"):
            testobj = arg 
            

    if buildit:
        saveData(newbase, oldbase, datafile)
    elif testobj:
        vertices = loadVertsCoo(testobj)
        faces = loadFacesIndices(testobj)  
        tess = subdivideObj(faces, vertices, 2)               
        saveTestObj(tess[0], tess[1], testobj+".subdivided.obj")        
    else:
        saveConvertedTarget(target, newbase, oldbase, datafile)
        


if __name__ == "__main__":
    main(sys.argv[1:])

