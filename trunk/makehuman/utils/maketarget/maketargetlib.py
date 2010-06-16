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
#import scan_fit
import blenderalignjoints
from topologylib import *
import simpleoctree
import time
from blendersaveobj import *
import os



def seekGroupName(vertices, vertSelect, vertGroups):

    gNames = set()
    for i in vertSelect:
        for groupsName,groupIndices in vertGroups.items():
                idxs = set(groupIndices) #I use set of a quicker lookup
                if i in idxs:
                    gNames.add(groupsName)
    for gName in gNames:
        print gName


def applyTarget(vertices, targetBuffer, mFactor):
    """
    This function applies the currently loaded morph target to the base mesh.

    Parameters
    ----------

    mFactor:
        *float*. Morphing factor.

    """
    for vData in targetBuffer:
        vIndex = vData[0]
        vX = vData[1]
        vY = vData[2]
        vZ = vData[3]
        v = vertices[vIndex]
        v[0] += vX*mFactor
        v[1] += vY*mFactor
        v[2] += vZ*mFactor



def alignMasks():
    """
    """
    global BaseMesh
    mask_scan_data = BlenderObj("mask_scan")
    mask_mh_data = BlenderObj("mask_mh")
    scan_data = BlenderObj("scan")

    mask_scan = [[v.co[0],v.co[1],v.co[2]] for v in mask_scan_data.verts]
    mask_mh = [[v.co[0],v.co[1],v.co[2]] for v in mask_mh_data.verts]
    scan = [[v.co[0],v.co[1],v.co[2]] for v in scan_data.verts]

    aligned_verts, aligned_mask = scan_fit.align_scan(mask_scan,mask_mh,scan)

    for i,v in enumerate(aligned_verts):
        scan_data.verts[i].co[0] = v[0]
        scan_data.verts[i].co[1] = v[1]
        scan_data.verts[i].co[2] = v[2]

    for i,v in enumerate(aligned_mask):
        mask_scan_data.verts[i].co[0] = v[0]
        mask_scan_data.verts[i].co[1] = v[1]
        mask_scan_data.verts[i].co[2] = v[2]

    scan_data.update()
    mask_scan_data.update()


def loadTarget(targetPath):
    """
    This function loads a morph target file.

    Parameters
    ----------

    targetPath:
        *string*. A string containing the operating system path to the
        file to be read.

    """
    targetBuffer = []
    try:
        fileDescriptor = open(targetPath)
    except:
        print"Unable to open %s",(targetPath)
        return  None

    current_target = targetPath
    targetBuffer = []
    for vData in fileDescriptor:
        vectorData = vData.split()
        if vectorData[0].find('#')==-1:
            mainPointIndex = int(vectorData[0])
            pointX = float(vectorData[1])
            pointY = float(vectorData[2])
            pointZ = float(vectorData[3])
            targetBuffer.append([mainPointIndex, pointX,pointY,pointZ])
    fileDescriptor.close()
    return targetBuffer

    

def saveTarget(vertices, targetPath, basePath, verticesTosave):
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



def adaptMesh(base, scan, verticesToAdapt):
    """
    
    """
    kd = KDTree(scan)
    dists,neighbs = kd.query(np.array(base)[verticesToAdapt])

    for iadapt,ineighb in zip(verticesToAdapt,neighbs):
        base[iadapt][0] = scan[ineighb][0]
        base[iadapt][1] = scan[ineighb][1]
        base[iadapt][2] = scan[ineighb][2]

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
    loadTarget(targetPath)
    pathParts = os.path.split(targetPath)
    headPath = pathParts[0]
    tailPath = pathParts[1]
    nameSuffix = tailPath[1:]
    targetPath = os.path.join(headPath,"r"+nameSuffix)
    applyTarget(-1)
    saveTranslationTarget(targetPath)
    resetMesh()

def loadAllTargetInFolder(filepath):
    #Because Blender filechooser return a file
    #it's needed to extract the dirname
    folderToScan = os.path.dirname(filepath)
    targetList = os.listdir(folderToScan)
    for targetName in targetList:
        targetPath = os.path.join(folderToScan,targetName)
        loadTarget(targetPath)
        applyTarget(0.5)

def processingTargets(filepath):
    """
    This function is used to adjust little changes on base
    meshes, correcting all targets
    """


    folderToScan = os.path.dirname(filepath)
    targetList = os.listdir(folderToScan)

    for targetName in targetList:
        targetPath = os.path.join(folderToScan,targetName)
        if os.path.isfile(targetPath):
            print "Processing %s"%(targetPath)
            loadTarget(targetPath)
            applyTarget(1.0)
            saveTarget(targetPath)
            applyTarget(-1.0)



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

