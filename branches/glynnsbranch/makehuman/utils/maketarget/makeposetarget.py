import Blender
import time
from Blender.BGL import *
from Blender import Draw
from Blender import Window
from Blender import Mesh
from Blender.Mathutils import *
from math import *
from aljabr import *

current_path = Blender.sys.dirname(Blender.Get('filename'))
basePath = Blender.sys.join(current_path,'base.obj')
pairsPath = Blender.sys.join(current_path,'base.sym')
centersPath = Blender.sys.join(current_path,'base.sym.centers')
morphFactor = Draw.Create(1.0)
current_target = ""
targetRotPath = ""
targetScalePath = ""
scaleMode= Draw.Create(0)
originalVerts = [] #Original base mesh coords

def axisID(axisVect):
    #TODO comments
    if fabs(axisVect[0]) > fabs(axisVect[1]) and fabs(axisVect[0]) > fabs(axisVect[2]):
        return "X"
    if fabs(axisVect[1]) > fabs(axisVect[0]) and fabs(axisVect[1]) > fabs(axisVect[2]):
        return "Y"
    if fabs(axisVect[2]) > fabs(axisVect[0]) and fabs(axisVect[2]) > fabs(axisVect[1]):
        return "Z"


def doRotMorph(mFactor):

    global originalVerts,targetRotPath

    a = time.time()
    obj = Mesh.Get("Base")
    mFactor = morphFactor.val

    try:
        f = open(targetRotPath)
        fileDescriptor = f.readlines()
        f.close()
    except:
        Draw.PupMenu("Error opening target file: %s"%(targetRotPath))
        return 0


    #Get info of axis from the first line of file
    rotAxeInfo = fileDescriptor[0].split()

    #Calculate the rotation axis vector
    axisP1  = obj.verts[int(rotAxeInfo[0])]
    axisP2  = obj.verts[int(rotAxeInfo[1])]
    axis = rotAxeInfo[2]
    #rotAxis = [axisP2.co[0]-axisP1.co[0],axisP2.co[1]-axisP1.co[1],axisP2.co[2]-axisP1.co[2]]
    #rotAxis = vunit(rotAxis)
    #axis = axisID(rotAxis)

    indicesToUpdate = []

    v1= [axisP1.co[0],axisP1.co[1],axisP1.co[2]]
    v2= [axisP2.co[0],axisP2.co[1],axisP2.co[2]]
    actualRotCenter = centroid([v1,v2])

    for stringData in fileDescriptor[1:]:
        listData = stringData.split()
        theta = float(listData[0])
        theta = theta*mFactor
        #Rmtx = makeRotMatrix(-theta, rotAxis)
        if axis == "X":
            Rmtx = makeRotEulerMtx3D(theta,0,0)
        if axis == "Y":
            Rmtx = makeRotEulerMtx3D(0,theta,0)
        if axis == "Z":
            Rmtx = makeRotEulerMtx3D(0,0,theta)

        for pIndex in listData[1:]:
            pointIndex = int(pIndex)
            indicesToUpdate.append(pointIndex)
            pointToRotate = [obj.verts[pointIndex].co[0],obj.verts[pointIndex].co[1],obj.verts[pointIndex].co[2]]
            pointRotated = rotatePoint(actualRotCenter,pointToRotate,Rmtx)

            obj.verts[pointIndex].co[0] = pointRotated[0]
            obj.verts[pointIndex].co[1] = pointRotated[1]
            obj.verts[pointIndex].co[2] = pointRotated[2]

    print "ROTATION TIME", time.time()-a

    obj.update()
    Window.RedrawAll()

    return 1


def saveRotTargets(targetFile):

    global originalVerts
    data = Mesh.Get("Base")
    rotData = {}

    vertsSelected = []
    for v in data.verts:
        if v.sel:
            vertsSelected.append(v)

    #Rotation axis is caluclated using 2 selected verts
    if len(vertsSelected) == 2:
        axisVertsIdx1 = vertsSelected[0].index
        axisVertsIdx2 = vertsSelected[1].index
    else:
        #Open Blender warning popup block
        block = []
        block.append("You must select")
        block.append("only 2 verts to define")
        block.append("the rotation axis")
        Draw.PupBlock("Error", block)
        return 0


    axeVerts = [originalVerts[axisVertsIdx1],originalVerts[axisVertsIdx2]]
    originalRotCenter = centroid(axeVerts)

    epsilon = 0.00001
    rotAxe = axisID(vsub(originalVerts[axisVertsIdx1],originalVerts[axisVertsIdx2]))

    rotAxisLabel = Draw.Create(rotAxe)
    block = []
    block.append("It's correct?")
    block.append(("Rot Axis: ", rotAxisLabel, 0, 30, "Rotation Axis"))
    Draw.PupBlock("Info", block)
    rotAxe = rotAxisLabel.val
    print "ROTAXE",rotAxe

    for index, vert in enumerate(data.verts):
        sourceVertex = originalVerts[index]
        targetVertex = [vert.co[0],vert.co[1],vert.co[2]]

        if  vdist(sourceVertex,targetVertex) > epsilon:
            pointIndex = index

            pointX = targetVertex[0]
            pointY = targetVertex[1]
            pointZ = targetVertex[2]
            if rotAxe == "X":
                originalRotCenter=[0,originalRotCenter[1],originalRotCenter[2]]
                targetPoint = [0,pointY,pointZ]
                basePoint = [0,originalVerts[pointIndex][1],originalVerts[pointIndex][2]]
            elif rotAxe == "Y":
                originalRotCenter=[originalRotCenter[0],0,originalRotCenter[2]]
                targetPoint = [pointX,0,pointZ]
                basePoint = [originalVerts[pointIndex][0],0,originalVerts[pointIndex][2]]
            elif rotAxe == "Z":
                originalRotCenter=[originalRotCenter[0],originalRotCenter[1],0]
                targetPoint = [pointX,pointY,0]
                basePoint = [originalVerts[pointIndex][0],originalVerts[pointIndex][1],0]

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
                pointToRotate = originalVerts[index]
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

    try:
        fileDescriptor = open(targetFile,'w+')
    except:
        print "Error in opening %s" %targetFile
        return 0
    #Write info about rotation: index of verts of rot axis
    fileDescriptor.write("%i %i %s #Indices of axis verts and axis\n" % (axisVertsIdx1,axisVertsIdx2,rotAxe))
    for angl, vertIndices in rotData.iteritems():
        fileDescriptor.write("%f " % (angl))
        for vertIndex in vertIndices:
            fileDescriptor.write("%i " % (vertIndex))
        fileDescriptor.write("\n")
    fileDescriptor.close()
    return 1



def scaleRot(targetRotPath1):
    global morphFactor 
    targetRotPath2 = targetRotPath1+".scaled"
    scaleFactor = morphFactor.val
    try:
        f = open(targetRotPath1)
        fileDescriptor = f.readlines()
        f.close()
    except:
        Draw.PupMenu("Error opening target file: %s"%(targetRotPath))
        return 0

    rotAxe = fileDescriptor[0].split()
    rotData = []
    for stringData in fileDescriptor[1:]:
        listData = stringData.split()
        theta = float(listData[0])*scaleFactor
        listData[0] = theta     
        rotData.append(listData)
    try:
        fileDescriptor = open(targetRotPath2,'w')
    except:
        print "Error in opening %s" %targetRotPath2
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
    return 1











def doScaleMorph(mFactor):
    global originalVerts,targetScalePath
    a = time.time()
    obj = Mesh.Get("Base")

    try:
        f = open(targetScalePath)
        fileDescriptor = f.readlines()
        f.close()
    except:
        Draw.PupMenu("Error opening target file: %s"%(targetScalePath))
        return 0

    #Get info of axis from the first line of file
    rotAxeVerts = fileDescriptor[0].split()

    #Calculate the rotation axis vector
    axisP1  = obj.verts[int(rotAxeVerts[0])]
    axisP2  = obj.verts[int(rotAxeVerts[1])]

    rotAxis = [axisP2.co[0]-axisP1.co[0],axisP2.co[1]-axisP1.co[1],axisP2.co[2]-axisP1.co[2]]
    rotAxis = vunit(rotAxis)
    axis = axisID(rotAxis)
    indicesToUpdate = []

    v1= [axisP1.co[0],axisP1.co[1],axisP1.co[2]]
    v2= [axisP2.co[0],axisP2.co[1],axisP2.co[2]]
    actualRotCenter = centroid([v1,v2])

    for stringData in fileDescriptor[1:]:
        listData = stringData.split()
        scale = float(listData[0])

        #A morph factor negative scale the object
        #in inverse direction.
        if mFactor < 0:
            scale = -1/(scale*mFactor)
        else:
            scale *= mFactor


        for pIndex in listData[1:]:
            pointIndex = int(pIndex)
            indicesToUpdate.append(pointIndex)
            originalPoint = [originalVerts[pointIndex][0],\
                            originalVerts[pointIndex][1] ,\
                            originalVerts[pointIndex][2] ]
            pointToScale = [obj.verts[pointIndex].co[0],\
                            obj.verts[pointIndex].co[1],\
                            obj.verts[pointIndex].co[2]]
            pointScaled = scalePoint(actualRotCenter,pointToScale,scale)
            obj.verts[pointIndex].co[0] = pointScaled[0]
            obj.verts[pointIndex].co[1] = pointScaled[1]
            obj.verts[pointIndex].co[2] = pointScaled[2]
    obj.update()
    Window.RedrawAll()

    return 1

def saveScaleTargets(targetFile):

    global originalVerts
    data = Mesh.Get("Base")
    rotData = {}
    scaleData = {}

    vertsSelected = []
    for v in data.verts:
        if v.sel:
            vertsSelected.append(v)

    #Rotation axis is caluclated using 2 selected verts
    if len(vertsSelected) == 2:
        axisVertsIdx1 = vertsSelected[0].index
        axisVertsIdx2 = vertsSelected[1].index
    else:
        #Open Blender warning popup block
        block = []
        block.append("You must select")
        block.append("only 2 verts to define")
        block.append("the rotation axis")
        Draw.PupBlock("Error", block)
        return 0


    originalAxePoint1 = originalVerts[axisVertsIdx1]
    originalAxePoint2 = originalVerts[axisVertsIdx2]
    axeOriginalVerts = [originalAxePoint1,originalAxePoint2]

    actualAxePoint1 = [data.verts[axisVertsIdx1].co[0],data.verts[axisVertsIdx1].co[1],data.verts[axisVertsIdx1].co[2]]
    actualAxePoint2 = [data.verts[axisVertsIdx2].co[0],data.verts[axisVertsIdx2].co[1],data.verts[axisVertsIdx2].co[2]]
    axeActualVerts = [actualAxePoint1,actualAxePoint2]

    #axeOriginalVerts = [originalVerts[axisVertsIdx1],originalVerts[axisVertsIdx2]]
    originalRotCenter = centroid(axeOriginalVerts)
    actualRotCenter = centroid(axeActualVerts)

    epsilon = 0.00001


    for index, vert in enumerate(data.verts):
        sourceVertex = originalVerts[index]
        targetVertex = [vert.co[0],vert.co[1],vert.co[2]]

        if  vdist(sourceVertex,targetVertex) > epsilon:

            V1 = vsub(sourceVertex,originalRotCenter)
            #V2 = vsub(targetVertex,originalRotCenter)
            V2 = vsub(targetVertex,actualRotCenter)
            v1 = vlen(V1)
            v2 = vlen(V2)

            #if index = 8872:
                #print "centro originale", originalRotCenter
                #print "punto originale", sourceVertex
                #print "centro attuale", originalRotCenter
                #print "punto attuale", originalRotCenter


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
                    correctionFactor = v1/0.25

                scaleFactor = v2/v1
                correctionFactor = 1
                s = round(scaleFactor,2)*correctionFactor

                #Store the results
                if s != 1.0:
                    if scaleData.has_key(s):
                        scaleData[s].append(index)
                    else:
                        scaleData[s] = [index]

            else:
                print "Problem calculating theta: v1,v2 =",v1,v2

    try:
        fileDescriptor = open(targetFile,'w+')
    except:
        print "Error in opening %s" %targetFile
        return 0
    fileDescriptor.write("%i %i #Indices of axis verts\n" % (axisVertsIdx1,axisVertsIdx2))
    for scal, vertIndices in scaleData.iteritems():
        fileDescriptor.write("%.2f " % (scal))
        for vertIndex in vertIndices:
            fileDescriptor.write("%i " % (vertIndex))
        fileDescriptor.write("\n")
    fileDescriptor.close()
    return 1

def printVertsIndices():
    data = Mesh.Get("Base")
    wem = Window.EditMode()
    Window.EditMode(0)
    for v in data.verts:
        if v.sel == 1:
            print "Index ", v.index
    Window.EditMode(wem)
    Window.RedrawAll()


def selectVertsbyIndex(Index):
    data = Mesh.Get("Base")
    data.verts[Index].sel = 1
    data.update()


def selectAxisVertices():

    global originalVerts,targetRotPath

    obj = Mesh.Get("Base")

    try:
        f = open(targetRotPath)
        fileDescriptor = f.readlines()
        f.close()
    except:
        Draw.PupMenu("Error opening target file: %s"%(targetRotPath))
        return 0


    #Get info of axis from the first line of file
    rotAxeInfo = fileDescriptor[0].split()

    #Calculate the rotation axis vector
    axisP1  = obj.verts[int(rotAxeInfo[0])]
    axisP2  = obj.verts[int(rotAxeInfo[1])]

    axisP1.sel = 1
    axisP2.sel = 1

    obj.update()





def loadInitialBaseCoords(path):
    """
    Little utility function to load only the verts data from a wavefront obj file.
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
            co = [float(dataList[1]),\
                    float(dataList[2]),\
                    float(dataList[3])]
            vertsCoo.append(co)
        data = fileDescriptor.readline()
    fileDescriptor.close()
    return vertsCoo

def loadSymVertsIndex(right=1):
    """
    Make the mesh symmetrical

    """

    global pairsPath
    global centersPath
    data = Mesh.Get("Base")
    wem = Window.EditMode()
    Window.EditMode(0)
    try:
        symmFile = open(pairsPath)
    except:
        print"File Sym not found"
        return 0
    for symmCouple in symmFile:
        leftVert = data.verts[int(symmCouple.split(',')[0])]
        rightVert = data.verts[int(symmCouple.split(',')[1])]
        if right == 1:
            rightVert.co[0] = -1*(leftVert.co[0])
            rightVert.co[1] = leftVert.co[1]
            rightVert.co[2] = leftVert.co[2]
        else:
            leftVert.co[0] = -1*(rightVert.co[0])
            leftVert.co[1] = rightVert.co[1]
            leftVert.co[2] = rightVert.co[2]
    symmFile.close()

    try:
        centerFile = open(centersPath)
    except:
        print"File Sym not found"
        return 0
    for i in centerFile:
        data.verts[int(i)].co[0] = 0.0
    symmFile.close()
    data.update()
    Window.EditMode(wem)
    Window.RedrawAll()


def resetMesh():
    """
    Restore the initial mesh coords
    """
    actual_mesh = Mesh.Get("Base")
    global originalVerts
    wem = Window.EditMode()
    Window.EditMode(0)
    for pointIndex, vCoords in enumerate(originalVerts):
        actual_mesh.verts[pointIndex].co[0] = vCoords[0]
        actual_mesh.verts[pointIndex].co[1] = vCoords[1]
        actual_mesh.verts[pointIndex].co[2] = vCoords[2]
    actual_mesh.update()
    Window.EditMode(wem)
    Window.RedrawAll()


def loadRotationPath(tPath):
    global targetRotPath
    targetRotPath = tPath

def loadScalePath(tPath):
    global targetScalePath
    targetScalePath = tPath

def draw():
    global morphFactor
    global scaleMode

    glClearColor(0.5, 0.5, 0.5, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2i(10, 150)
    Draw.Text("Make MH targets v2.1")
    glRasterPos2i(10, 140)
    Draw.Text("_____________________________________________")
    glRasterPos2i(10, 120)

    Draw.Button("Load", 2, 10, 100, 50, 20, "Load target")
    Draw.Button("Morph", 3, 60, 100, 50, 20, "Morph ")
    Draw.Button("<=", 5, 110, 100, 30, 20, "Make left side symetrical to right side")
    Draw.Button("Fix", 10, 140, 100, 40, 20, "Return base object to its original state")
    Draw.Button("=>", 6, 180, 100, 30, 20, "Make right side symetrical to left side")
    morphFactor = Draw.Number("Value: ", 0, 10, 80, 100, 20, morphFactor.val, -2, 2, "Insert the value to apply the target")
    Draw.Button("Save", 1, 110, 80, 100, 20, "Save target")
    scaleMode = Draw.Toggle("Scale Mode",0,10,60,200,20,scaleMode.val,"Load/save scale target instead rot target")

def event(event, value):
    if event == Draw.ESCKEY and not value: Draw.Exit()
    elif event == Draw.MKEY:
        Window.FileSelector (saveSymVertsIndices, "Save Symm data")
    elif event == Draw.IKEY:
        printVertsIndices()
    elif event == Draw.TKEY:
        Window.FileSelector (saveScaleTarget, "Save scale data")
    elif event == Draw.SKEY:
        Window.FileSelector (loadScaleTarget, "Load scale data")
    elif event == Draw.VKEY:
        selectAxisVertices()
    elif event == Draw.LKEY:
        Window.FileSelector (MHloadRotationTarget2, "Load rot data")
    elif event == Draw.KKEY:
        Window.FileSelector (scaleRot, "Scale rot data")


def b_event(event):
    global symmPath,selAxis
    if event == 0: pass
    elif event == 1:
        if scaleMode.val == 1:
            Window.FileSelector (saveScaleTargets, "Save Scale Target")
        else:
            Window.FileSelector (saveRotTargets, "Save Rot Target")
    elif event == 2:
        if scaleMode.val == 1:
            Window.FileSelector (loadScalePath, "Load Scale Target")
        else:
            Window.FileSelector (loadRotationPath, "Load Rot Target")
    elif event == 3:
        if scaleMode.val == 1:
            doScaleMorph(morphFactor.val)
        else:
            doRotMorph(morphFactor.val)
    elif event == 5:
        loadSymVertsIndex(0)
    elif event == 6:
        loadSymVertsIndex(1)
    elif event == 10:
        resetMesh()
    Draw.Draw()

originalVerts = loadInitialBaseCoords(basePath)
Draw.Register(draw, event, b_event)
