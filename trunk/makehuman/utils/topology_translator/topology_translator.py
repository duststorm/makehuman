from math import sqrt
from aljabr import *
import time
import simpleoctree



    
    
def loadVertsCoo(path, tesselate = None):
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
    print "DEBUG"
    print len(vertices)
    print len(subdividedVerts)
    print len (finalVertList)
    
    return finalVertList
    







def loadTranslationTarget(vertsList, targetPath):

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

    vertsList1 = loadVertsCoo(newMeshPath)
    vertsList2 = tesselate(oldMeshPath, loadVertsCoo(oldMeshPath))
    
    for i,v in enumerate(vertsList2):
        v.append(i)
    
    octree = soctree.SimpleOctree(vertsList2, .25)
    try:
        fileDescriptor = open(dataPath, 'w')
    except:
        print 'Unable to open %s', dataPath
        return None    

       
    for i1,v1 in enumerate(vertsList1):
        t1 = time.time() 
        #For each vert of new mesh...
              
        vIndices = []
        vDistances = [] 
        
        
        vertsList3 = octree.root.getSmallestChild(v1)        
                 

        distData = {}
        
        #... find nearest verts on old mesh
        for i2,v2 in enumerate(vertsList3.verts):            
            d = vdist(v1, v2)
            distData[d]=v2[3]

        dKeys = distData.keys()
        dKeys.sort()
        dmin = dKeys[0]

        #in case of smaller distance < 0.005 the vert is identical
        if  dKeys[0] < 0.005:
            vIndices = [distData[dKeys[0]]]
            vDistances = [dKeys[0]]           
            
        #else we get the 3 first verts with smaller distance              
        else:                
            vIndices = [distData[dKeys[0]],\
                distData[dKeys[1]],\
                distData[dKeys[2]],distData[dKeys[3]],distData[dKeys[4]],distData[dKeys[5]],distData[dKeys[6]]]
            vDistances = [dKeys[0],dKeys[1],dKeys[2],dKeys[3],dKeys[4],dKeys[5],dKeys[6]]
            
        if d < dmin:
            dmin = d                 

        if dmin > 0:
            weights = [dmin/dst for dst in vDistances]
        else:
            weights = [1]        
            
        if vIndices ==[]:
            print "error"
            break
            
        for index in vIndices:
            fileDescriptor.write('%i ' % (index))
        for weight in weights:
            fileDescriptor.write('%f ' % (weight))            
        fileDescriptor.write('\n')
        t = time.time()-t1
        print "Time remaining: %f hours"%((t*(len(vertsList1)-i1))/3600.0)  
         
        
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
        if idx == 9030:
            print "DATA: ",translationData

        
        #print "DATA: ",translationData
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
                

        vertsNew[idx] = vdiv(xSum,sumWeight)
        
        if idx == 9030:
            print "Vert sum", xSum
            print "Vert result", vertsNew[idx]
   
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


                
            
