import sys
sys.path.append("../")
sys.path.append("./")
sys.path.append("../svd_tools/fit")
sys.path.append("../../mh_core")
sys.path.append("../topology_translator")

import aljabr
import scipy
from scipy.spatial import KDTree
import numpy as np
import scan_fit
import blenderalignjoints
from topologylib import *
import simpleoctree
import time
from blendersaveobj import *
import os
from math import *
from scipy.linalg import eigh,pinv


def analyzeTarget(vertices, targetBuffer, scale=0.5):

    vertColors = [[0,0,0] for x in vertices]
    lenMax = 0
    for vect in targetBuffer:
         lenght = vlen([vect[1],vect[2],vect[3]])
         if  lenght > lenMax:
             lenMax = lenght
    for vect in targetBuffer:
         lenght = vlen([vect[1],vect[2],vect[3]])
         colorR = int(255*(lenght/lenMax))
         colorG = 255-int(255*(lenght/(lenMax*scale)))
         vertColors[vect[0]] = [colorR,colorG,0]
    return vertColors



def turn_around(vertices,axis,angle):
    """
        Rotate vertices around 'axis' with angle value 'angle'
    """

    P = np.dot(axis[:,np.newaxis],axis[np.newaxis,:])
    I = np.identity(len(axis))
    Q = np.array([
        [   0     , -axis[2] , axis[1] ],
        [ axis[2] ,     0    , -axis[0]],
        [-axis[1] ,  axis[0] ,   0     ]])
    cosa = np.cos(angle)
    sina = np.sin(angle)
    return P + (I-P)*cosa + Q*sina

def compute_distance(vertices0, vertices1):
    kd = KDTree(vertices0)
    dist,indx = kd.query(vertices1)
    return sum(dist)

def align_PCA(vertices0, vertices1):
    """
     it accepts and returns lists of lists
     vertices0 can be either MH mesh
     or the concatenation of a few manually aligned scans
    """
    vertices0 = np.array(vertices0)
    vertices1 = np.array(vertices1)

    # Computes the barycenter
    mean0 = np.mean(vertices0,0)
    mean1 = np.mean(vertices1,0)

    # computes covariance matrix and principal axes
    cov0 = np.cov(vertices0.T)
    w0,u0 = eigh(cov0)

    cov1 = np.cov(vertices1.T)
    w1,u1 = eigh(cov1)

    # Computes rotation matrix to go from 1 to 0
    R = np.dot(u0,pinv(u1))

    #apply the transformation
    vertices = w0[-1]/w1[-1]*np.dot(vertices1-mean1,R.T)
    
    # axis can be arbitrarily oriented so we have to check if some rotations
    # around main axes are needed
    dmin = None
    amin = bmin = cmin = None
    
    for a in [0,np.pi]:
        if a != 0 : va = turn_around(vertices[::10],u0[:,0],a)
        else : va = vertices[::2]
        for b in [0,np.pi] :
            if b != 0 : vb = turn_around(va,u0[:,1],b)
            else : vb = va
            for c in [0,np.pi] :
                if c != 0 : vc = turn_around(vb,u0[:,2],c)
                else : vc = vb
                dist = compute_distance(vc+mean0,vertices0)
                if dmin is None or dist < dmin :
                    dmin = dist
                    amin = a
                    bmin = b
                    cmin = c

    if amin : vertices = turn_around(vertices,u0[:,0],amin)
    if bmin : vertices = turn_around(vertices,u0[:,1],bmin)
    if cmin : vertices = turn_around(vertices,u0[:,2],cmin)
        
    return vertices + mean0


def axisID(axisVect):
    #TODO comments
    if fabs(axisVect[0]) > fabs(axisVect[1]) and fabs(axisVect[0]) > fabs(axisVect[2]):
        return "X"
    if fabs(axisVect[1]) > fabs(axisVect[0]) and fabs(axisVect[1]) > fabs(axisVect[2]):
        return "Y"
    if fabs(axisVect[2]) > fabs(axisVect[0]) and fabs(axisVect[2]) > fabs(axisVect[1]):
        return "Z"

def loadRotTarget(vertices,targetRotPath,mFactor):

    try:
        f = open(targetRotPath)
        fileDescriptor = f.readlines()
        f.close()
    except:
        print "Error opening target file: %s"%(targetRotPath)
        return 0

    print  "ROT: ",targetRotPath,mFactor
    #Get info of axis from the first line of file
    rotAxeInfo = fileDescriptor[0].split()

    #Calculate the rotation axis vector
    axisP1  = vertices[int(rotAxeInfo[0])]
    axisP2  = vertices[int(rotAxeInfo[1])]
    axis = rotAxeInfo[2]
    indicesToUpdate = []
    v1= [axisP1[0],axisP1[1],axisP1[2]]
    v2= [axisP2[0],axisP2[1],axisP2[2]]
    actualRotCenter = centroid([v1,v2])

    for stringData in fileDescriptor[1:]:
        listData = stringData.split()
        theta = float(listData[0])
        theta = theta*mFactor

        if axis == "X":
            Rmtx = makeRotEulerMtx3D(theta,0,0)
        if axis == "Y":
            Rmtx = makeRotEulerMtx3D(0,theta,0)
        if axis == "Z":
            Rmtx = makeRotEulerMtx3D(0,0,theta)

        for pIndex in listData[1:]:
            pointIndex = int(pIndex)
            indicesToUpdate.append(pointIndex)
            pointToRotate = [vertices[pointIndex][0],vertices[pointIndex][1],vertices[pointIndex][2]]
            pointRotated = rotatePoint(actualRotCenter,pointToRotate,Rmtx)
            vertices[pointIndex][0] = pointRotated[0]
            vertices[pointIndex][1] = pointRotated[1]
            vertices[pointIndex][2] = pointRotated[2]





def seekGroupName(vertices, vertSelect, vertGroups):

    gNames = set()
    for i in vertSelect:
        for groupsName,groupIndices in vertGroups.items():
                idxs = set(groupIndices) #I use set of a quicker lookup
                if i in idxs:
                    gNames.add(groupsName)
    for gName in gNames:
        print gName




def loadTraslTarget(vertices,targetPath,mFactor):
    """
    This function loads a morph target file.

    Parameters
    ----------

    targetPath:
        *string*. A string containing the operating system path to the
        file to be read.

    """
    try:
        fileDescriptor = open(targetPath)
    except:
        print"Unable to open %s",(targetPath)
        return  None

    current_target = targetPath
    #print  targetPath,mFactor 
    for vData in fileDescriptor:
        vectorData = vData.split()
        if vectorData[0].find('#')==-1:
            vIndex = int(vectorData[0])
            vX = float(vectorData[1])
            vY = float(vectorData[2])
            vZ = float(vectorData[3])
            v = vertices[vIndex]
            v[0] += vX*mFactor
            v[1] += vY*mFactor
            v[2] += vZ*mFactor
    fileDescriptor.close()




def alignScan(maskBaseVerts, maskScanVerts, scanVerts):
    """
    """

    aligned_verts, aligned_mask = scan_fit.align_scan(maskScanVerts,maskBaseVerts,scanVerts)

    for i,v in enumerate(aligned_verts):
        scanVerts[i][0] = v[0]
        scanVerts[i][1] = v[1]
        scanVerts[i][2] = v[2]

    for i,v in enumerate(aligned_mask):
        maskScanVerts[i][0] = v[0]
        maskScanVerts[i][1] = v[1]
        maskScanVerts[i][2] = v[2]



def saveTraslTarget(vertices, targetPath, basePath, verticesTosave):
    """
    This function saves a morph target file containing the difference between
    the *originalVerts* positions and the actual vertex coordinates.

    Parameters
    ----------

    targetPath:
        *string*. A string containing the operating system path to the
        file to be written.

    """
    epsilon = 0.001
    originalVertices = loadVertices(basePath)
    nVertsExported = 0

    try:
        fileDescriptor = open(targetPath, "w")
    except:
        print "Unable to open %s",(targetPath)
        return  None
    print "saving %s"%(targetPath)
    for index in verticesTosave:
        originalVertex = originalVertices[index]
        targetVertex = vertices[index]
        delta = vsub(targetVertex,originalVertex)
        dist =  vdist(originalVertex,targetVertex)
        if dist > epsilon:
            nVertsExported += 1
            fileDescriptor.write("%d %f %f %f\n" % (index,delta[0],delta[1],delta[2]))
    fileDescriptor.close()

    if nVertsExported == 0:
        print "Warning: Zero verts exported in file %s"%(targetPath)



def saveRotTargets(vertices, targetPath, basePath, vertsSelected):

    epsilon = 0.00001
    originalVertices = loadVertices(basePath)
    rotData = {}

    #Rotation axis is caluclated using 2 selected verts
    if len(vertsSelected) == 2:
        axisVertsIdx1 = vertsSelected[0]
        axisVertsIdx2 = vertsSelected[1]
    else:

        print"You must select only 2 verts to define the rotation axis"
        return 0

    axeVerts = [originalVertices[axisVertsIdx1],originalVertices[axisVertsIdx2]]
    originalRotCenter = centroid(axeVerts)
    rotAxe = axisID(vsub(originalVertices[axisVertsIdx1],originalVertices[axisVertsIdx2]))

    print "ROTAXE",rotAxe

    for index, vert in enumerate(vertices):
        sourceVertex = originalVertices[index]
        targetVertex = vertices[index]

        if  vdist(sourceVertex,targetVertex) > epsilon:
            pointIndex = index
            pointX = targetVertex[0]
            pointY = targetVertex[1]
            pointZ = targetVertex[2]
            if rotAxe == "X":
                originalRotCenter=[0,originalRotCenter[1],originalRotCenter[2]]
                targetPoint = [0,pointY,pointZ]
                basePoint = [0,originalVertices[pointIndex][1],originalVertices[pointIndex][2]]
            elif rotAxe == "Y":
                originalRotCenter=[originalRotCenter[0],0,originalRotCenter[2]]
                targetPoint = [pointX,0,pointZ]
                basePoint = [originalVertices[pointIndex][0],0,originalVertices[pointIndex][2]]
            elif rotAxe == "Z":
                originalRotCenter=[originalRotCenter[0],originalRotCenter[1],0]
                targetPoint = [pointX,pointY,0]
                basePoint = [originalVertices[pointIndex][0],originalVertices[pointIndex][1],0]

            V1 = vsub(basePoint,originalRotCenter)
            V2 = vsub(targetPoint,originalRotCenter)
            v1 = vlen(V1)
            v2 = vlen(V2)

            if v1 != 0 and v2 != 0:
                #This method return some artifacts when
                #the distance between rotation center and
                #point is near to zero. For this reason
                #I've added a correction factor, that reduce
                #to zero the transformations near the rotation
                #point
                if v1 > 0.25:
                    correctionFactor = 1
                else:
                    correctionFactor = v1/0.25#ODO try to not reduce completely to 0

                #Some trigonometry stuff to get the rotation angle
                cos_theta = (vdot(V1,V2)/(v1*v2))
                if cos_theta < -1: cos_theta = -1
                if cos_theta > 1: cos_theta = 1
                theta = acos(cos_theta)

                #As polar coords, we need angle and a distance.
                #in our case, we use a scale factor to indicate

                scaleFactor = v2/v1

                #This is just a test to check the sign of rotation
                if rotAxe == "X":
                    Rmtx1 = makeRotEulerMtx3D(theta,0,0)
                    Rmtx2 = makeRotEulerMtx3D(-theta,0,0)
                if rotAxe == "Y":
                    Rmtx1 = makeRotEulerMtx3D(0,theta,0)
                    Rmtx2 = makeRotEulerMtx3D(0,-theta,0)
                if rotAxe == "Z":
                    Rmtx1 = makeRotEulerMtx3D(0,0,theta)
                    Rmtx2 = makeRotEulerMtx3D(0,0,-theta)
                pointToRotate = originalVertices[index]
                actualPoint = [pointX,pointY,pointZ]
                rotatedP1_1 = rotatePoint(originalRotCenter,pointToRotate,Rmtx1)
                rotatedP1_2 = rotatePoint(originalRotCenter,pointToRotate,Rmtx2)
                testVect1 = vsub(actualPoint,rotatedP1_1)
                testVect2 = vsub(actualPoint,rotatedP1_2)
                if vlen(testVect1) < vlen(testVect2):
                    Rmtx =  Rmtx1
                else:
                    Rmtx =  Rmtx2
                    theta = -theta
                #Round the results, and apply correction factor
                k = round(theta,2)#*correctionFactor
                #Store the results
                if rotData.has_key(k):
                    rotData[k].append(pointIndex)
                else:
                    rotData[k] = [pointIndex]
            else:
                print "Problem calculating theta: v1,v2 =",v1,v2

    
    fileDescriptor = open(targetPath,'w+')
    
    #Write info about rotation: index of verts of rot axis
    fileDescriptor.write("%i %i %s #Indices of axis verts and axis\n" % (axisVertsIdx1,axisVertsIdx2,rotAxe))
    for angl, vertIndices in rotData.iteritems():
        fileDescriptor.write("%f " % (angl))
        for vertIndex in vertIndices:
            fileDescriptor.write("%i " % (vertIndex))
        fileDescriptor.write("\n")
    fileDescriptor.close()
    return 1


def adaptMesh(base, scan, verticesToAdapt):
    """

    """
    kd = KDTree(scan)
    dists,neighbs = kd.query(np.array(base)[verticesToAdapt])

    for iadapt,ineighb in zip(verticesToAdapt,neighbs):
        base[iadapt][0] = scan[ineighb][0]
        base[iadapt][1] = scan[ineighb][1]
        base[iadapt][2] = scan[ineighb][2]


def loadPoseFromFile(vertices,path,scale = 1,onlyRot = False):
    fileDescriptor = open(path)
    poseData = fileDescriptor.readlines()
    fileDescriptor.close()
    if scale < 0:
        poseData.reverse()
    for data in poseData:
        targetdata = data.split()
        fileName = os.path.basename(targetdata[0])
        mFactor = float(os.path.basename(targetdata[1]))

        mFactor = scale*mFactor
        ext = os.path.splitext(fileName)[1]
        if ext == ".rot":
            #It assume script is called from makehuman/utils/maketarget
            targetRotPath = os.path.join("../../",targetdata[0])
            loadRotTarget(vertices,targetRotPath,mFactor)            
        if ext == ".target" and not onlyRot:
            targetPath = os.path.join("../../",targetdata[0])
            loadTraslTarget(vertices,targetPath,mFactor)
            


def loadPoseFromFolder(vertices,path,mFactor = 1,onlyRot = False):
    folderToScan = os.path.dirname(path)#because Blender fselector always return a file
    targetList = os.listdir(folderToScan)
    translTargets = []
    rotTargets = []
    targetList.sort()
    
    if mFactor < 0:
        targetList.reverse()
    for fileName in targetList:
        ext = os.path.splitext(fileName)[1]
        if ext == ".rot":            
            targetRotPath = os.path.join(folderToScan,fileName)
            rotTargets.append(targetRotPath)
                      
        if ext == ".target" and not onlyRot:
            targetTraslPath = os.path.join(folderToScan,fileName)
            translTargets.append(targetTraslPath)

    if mFactor > 0:
        for targetPath in translTargets:
            loadTraslTarget(vertices,targetPath,mFactor)
        for targetPath in rotTargets:
            loadRotTarget(vertices,targetPath,mFactor)

    if mFactor < 0:        
        for targetPath in rotTargets:
            loadRotTarget(vertices,targetPath,mFactor)
        for targetPath in translTargets:
            loadTraslTarget(vertices,targetPath,mFactor)
            



def saveScaledRotTarget(path,scaleFactor):

    path2 = path+".scaled"
    try:
        f = open(path)
        fileDescriptor = f.readlines()
        f.close()
    except:
        print "Error opening target file: %s"%(path)
        return 0

    rotAxe = fileDescriptor[0].split()
    rotData = []
    for stringData in fileDescriptor[1:]:
        listData = stringData.split()
        theta = float(listData[0])*scaleFactor
        listData[0] = theta
        rotData.append(listData)
    try:
        fileDescriptor = open(path2,'w')
    except:
        print "Error in opening %s" %path2
        return 0
    #Write info about rotation: index of verts of rot axis
    fileDescriptor.write("%s %s %s #Indices of axis verts and axis\n" % (rotAxe[0],\
                                                                        rotAxe[1],\
                                                                        rotAxe[2]))
    for rData in rotData:
        fileDescriptor.write("%f " % (rData[0]))
        for vertIndex in rData[1:]:
            fileDescriptor.write("%s " % (vertIndex))
        fileDescriptor.write("\n")
    fileDescriptor.close()


def saveGroups(vertGroups, path, filter = None):
    """
    This function saves the indices of selected verts

    Parameters
    ----------

    filePath:
        *string*. A string containing the operating system path to the
        file to be written.

    """
    try:
        fileDescriptor = open(path, "w")
    except:
        print "Unable to open %s",(path)
        return  None
    for g in vertGroups:
        if filter:
            if filter in g:
                fileDescriptor.write("%s\n"%(g))
        else:
            fileDescriptor.write("%s\n"%(g))
    fileDescriptor.close()


def saveIndexSelectedVerts(selectVerts, path):
    """
    This function saves the indices of selected verts

    Parameters
    ----------

    filePath:
        *string*. A string containing the operating system path to the
        file to be written.

    """
    try:
        fileDescriptor = open(path, "w")
    except:
        print "Unable to open %s",(path)
        return  None
    for v in selectVerts:
        fileDescriptor.write("%d\n"%(v))
    fileDescriptor.close()

def loadIndexSelectedVerts(path):
    """
    This function load the indices of selected verts

    Parameters
    ----------

    filePath:
        *string*. A string containing the operating system path to the
        file to be written.

    """
    selectedIndices = []
    try:
        fileDescriptor = open(path)
    except:
        print "Unable to open %s",(path)
        return  None
    for vData in fileDescriptor:
        i = int(vData.split()[0])
        selectedIndices.append(i)
    fileDescriptor.close()
    return selectedIndices


def saveTranslationTargetAndHisSymm(targetPath):
    """
    This function saves a morph target file and his symmetric.
    In example, saving l-ear-move-up.target, will be automatically
    calculated and saved r-ear-move-up.target

    Parameters
    ----------

    targetPath:
        *string*. A string containing the operating system path to the
        file to be written. Must start with "l-" prefix.

    """

    saveTranslationTarget(targetPath)
    loadSymVertsIndex(1)
    loadTraslTarget(targetPath)
    pathParts = os.path.split(targetPath)
    headPath = pathParts[0]
    tailPath = pathParts[1]
    nameSuffix = tailPath[1:]
    targetPath = os.path.join(headPath,"r"+nameSuffix)
    applyTarget(-1)
    saveTranslationTarget(targetPath)
    resetMesh()


def processingTargets(path,basePath,vertices,mFactor,verticesTosave):
    """
    This function is used to adjust little changes on base
    meshes, correcting all targets
    """

    targetDir = os.path.dirname(path)
    targetToApply = os.path.basename(path)
    targetsList = os.listdir(targetDir)

    for targetName in targetsList:
        if targetName != targetToApply:
            targetPath = os.path.join(targetDir,targetName)
            if os.path.isfile(targetPath):
                #print "Processing %s"%(targetPath)
                loadTraslTarget(vertices,targetPath,1.0)                
                loadTraslTarget(vertices,path,mFactor) 
                saveTraslTarget(vertices, targetPath+".mod.target", basePath, verticesTosave)
                loadTraslTarget(vertices,path,-mFactor) 
                loadTraslTarget(vertices,targetPath,-1.0)                



def loadVertices(path):
    """
    This function is a little utility function to load only the vertex data
    from a wavefront obj file.

    Parameters
    ----------

    path:
        *string*. A string containing the operating system path to the
        file that contains the wavefront obj.

    """
    try:
        fileDescriptor = open(path)
    except:
        print "Error opening %s file"%(path)
        return
    data = fileDescriptor.readline()
    vertsCoo = []
    while data:
        dataList = data.split()
        if dataList[0] == "v":
            co = (float(dataList[1]),\
                    float(dataList[2]),\
                    float(dataList[3]))
            vertsCoo.append(co)
        data = fileDescriptor.readline()
    fileDescriptor.close()
    return vertsCoo


def saveSymVertsIndices(filePath):
    """
    This function identifies and saves symmetric pairs of vertices.
    If a symmetric vertex is not found, the lone vertex is selected
    and processing is halted so that the problem can be fixed.

    Parameters
    ----------

    filePath:
        *string*. A string containing the operating system path to the
        file that will contain the new or updated morph target.

    """

    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    data = activeObj.getData(mesh=True)
    leftVerts = []
    rightVerts = []
    listOfSymmIndex = []
    listOfCentralIndex = []
    for v in data.verts:
        if abs(v.co[0]) > 0.001:
            if v.co[0] < 0:
                leftVerts.append(v)
            if v.co[0] > 0:
                rightVerts.append(v)
        else:
            listOfCentralIndex.append(v.index)
    print "left verts, right verts, central verts"
    print "---------------------------------------"
    print len(leftVerts),len(rightVerts),len(listOfCentralIndex)
    print "sum: ",len(leftVerts)+len(rightVerts)+len(listOfCentralIndex)
    progress = 0.0
    progress2 = len(leftVerts)
    Window.DrawProgressBar(0, "Start")

    for v1 in leftVerts:
        v1.sel = 0
        v1Flipped = [-v1.co[0],v1.co[1],v1.co[2]]
        delta = 0.00001
        isFoundSymm = 0
        progress += 1.0
        Window.DrawProgressBar((progress/progress2), str(progress/progress2))

        while isFoundSymm == 0:
            for v2 in rightVerts:
                if vdist(v1Flipped,v2.co) < delta:

                    listOfSymmIndex.append([v1.index,v2.index])
                    rightVerts.remove(v2)
                    isFoundSymm = 1
                    break
            delta += 0.0001
            if delta > 0.005:
                print "WARNING: nos sym found", vdist(v1Flipped,v2.co),delta,v1.index,v2.index
                v1.sel = 1
                break

    Window.DrawProgressBar(1, "Done")
    file = open(filePath, 'w')
    for couple in listOfSymmIndex:
        file.write(str(couple[0]) + "," +str(couple[1]) + "\n")
    file.close()
    file = open(filePath+".centers", 'w')
    for index in listOfCentralIndex:
        file.write(" %i \n"%(index))
    file.close()
    data.update()

def symmetrise(vertices, pairsPath, centersPath, rightMirror):
    """
    Make the mesh symmetrical by reflecting the existing vertices across
    to the left or right. By default this function reflects left to right.

    Parameters
    ----------

    right:
        *int*. A flag to indicate whether the new vertices will be reflected
        across to the left or right. (1=right, 0=left)

    """

    try:
        symmFile = open(pairsPath)
    except:
        print"File Sym not found"
        return 0
    for symmCouple in symmFile:
        leftVert = vertices[int(symmCouple.split(',')[0])]
        rightVert = vertices[int(symmCouple.split(',')[1])]
        if rightMirror == 1:
            rightVert[0] = -1*(leftVert[0])
            rightVert[1] = leftVert[1]
            rightVert[2] = leftVert[2]
        else:
            leftVert[0] = -1*(rightVert[0])
            leftVert[1] = rightVert[1]
            leftVert[2] = rightVert[2]
    symmFile.close()

    try:
        centerFile = open(centersPath)
    except:
        print"File Sym not found"
        return 0
    for i in centerFile:
        vertices[int(i)][0] = 0.0
    symmFile.close()



def selectSymmetricVerts():
    """
    Select symmetrical verts  by reflecting the existing selection across
    to the left or right. This function reflects left to right.

    Parameters
    ----------

    right:
        *int*. A flag to indicate whether the new vertices will be reflected
        across to the left or right. (1=right, 0=left)

    """

    global pairsPath
    print "selecting symm"
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    data = activeObj.getData(mesh=True)
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    try:
        symmFile = open(pairsPath)
    except:
        print"File Sym not found"
        return 0
    for symmCouple in symmFile:
        leftVert = data.verts[int(symmCouple.split(',')[0])]
        rightVert = data.verts[int(symmCouple.split(',')[1])]

        if leftVert.sel == 1:
            leftVert.sel = 0
            rightVert.sel = 1
    symmFile.close()

    data.update()
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()


def selectVerts(listOfIndices):
    """


    """

    global pairsPath
    print "selecting symm"
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    data = activeObj.getData(mesh=True)
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    for i in listOfIndices:
        vertToSelect = data.verts[i]
        vertToSelect.sel = 1


    data.update()
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()


def resetMesh(vertices, basePath):
    """
    This function restores the initial base mesh coordinates.

    **Parameters:** This method has no parameters.

    """
    originalVertices = loadVertices(basePath)
    for pointIndex, vCoords in enumerate(originalVertices):
        vertices[pointIndex][0] = vCoords[0]
        vertices[pointIndex][1] = vCoords[1]
        vertices[pointIndex][2] = vCoords[2]




#originalVerts = loadInitialBaseCoords(basePath)

