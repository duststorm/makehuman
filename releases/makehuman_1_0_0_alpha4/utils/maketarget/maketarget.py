# You may use, modify and redistribute this module under the terms of the GNU GPL.
"""
Utility function for creating a morph target (part of the development functionality).

===========================  ===============================================================
Project Name:                **MakeHuman**
Module File Location:        utils/maketarget/maketarget.py
Product Home Page:           http://www.makehuman.org/
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2008
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
===========================  ===============================================================

The MakeHuman application uses predefined morph target files to distort 
the humanoid model when physiological changes or changes to the pose are
applied by the user. The morph target files contain extreme mesh 
deformations for individual joints and features which can used 
proportionately to apply less extreme deformations and which can be 
combined to provide a very wide range of options to the user of the
application.

This module contains a set of functions used by 3d artists during the 
development cycle to create these extreme morph target files from 
hand-crafted models.

"""


__docformat__ = 'restructuredtext'


import Blender
import math
import time
try:
    import os
    from os import path
except:
    print "os module not found: some advanced functions are not available"
from Blender.BGL import *
from Blender import Draw
from Blender import Window
from Blender.Mathutils import *

current_path = Blender.sys.dirname(Blender.Get('filename'))
basePath = Blender.sys.join(current_path,'base.obj')
pairsPath = Blender.sys.join(current_path,'base.sym')
centersPath = Blender.sys.join(current_path,'base.sym.centers')
morphFactor = Draw.Create(1.0)
saveOnlySelectedVerts = Draw.Create(0)
current_target = ""
loadFile = ""
targetBuffer = [] #Last target loaded
originalVerts = [] #Original base mesh coords


#Some math stuff
def vsub(vect1,vect2):
    """
    This utility function returns a list of 3 float values containing the 
    difference between two 3D vectors (vect1-vect2).

    Parameters
    ----------

    vect1:
        *list of floats*. A list of 3 floats containing the x, y and z 
        coordinates of a vector.

    vect2:
        *list of floats*. A list of 3 floats containing the x, y and z 
        coordinates of a vector.
        
    """
    return [vect1[0]-vect2[0], vect1[1]-vect2[1], vect1[2]-vect2[2]]

def vdist(vect1,vect2):
    """
    This utility function returns a single float value containing the 
    euclidean distance between two coordinate vectors (the length of 
    the line between them).

    Parameters
    ----------

    vect1:
        *list of floats*. A list of 3 floats containing the x, y and z 
        coordinates of a vector.

    vect2:
        *list of floats*. A list of 3 floats containing the x, y and z 
        coordinates of a vector.

    """
    joiningVect = vsub(vect1,vect2)
    return vlen(joiningVect)

def vlen(vect):
    """
    This utility function returns a single float value containing the length 
    of a vector [x,y,z].

    Parameters
    ----------

    vect:
        *list of floats*. A list of 3 floats containing the x, y and z 
        coordinates of a vector.

    """
    return math.sqrt(vdot(vect,vect))

def vdot(vect1,vect2):

    """
    This utility function returns a single float value containing the dot 
    (scalar) product of two vectors.

    Parameters
    ----------

    vect1:
        *list of floats*. A list of 3 floats containing the x, y and z 
        coordinates of a vector.

    vect2:
        *list of floats*. A list of 3 floats containing the x, y and z 
        coordinates of a vector.
    
    """
    return vect1[0]*vect2[0] + vect1[1]*vect2[1] + vect1[2]*vect2[2]


#Starting maketarget specific functions

def doMorph(mFactor):
    """
    This function applies the currently loaded morph target to the base mesh.
    
    Parameters
    ----------

    mFactor:
        *float*. Morphing factor.
    
    """
    t1 = time.time()
    global targetBuffer
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    obj = activeObj.getData(mesh=True)
    for vData in targetBuffer:
        mainPointIndex = vData[0]
        pointX = vData[1]
        pointY = vData[2]
        pointZ = vData[3]
        v = obj.verts[mainPointIndex]
        v.co[0] += pointX*mFactor
        v.co[1] += pointY*mFactor
        v.co[2] += pointZ*mFactor
    obj.update()
    obj.calcNormals()
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()
    print "Target time", time.time() - t1



def loadTranslationTarget(targetPath):
    """
    This function loads a morph target file.

    Parameters
    ----------

    targetPath:
        *string*. A string containing the operating system path to the 
        file to be read.

    """
    global targetBuffer,current_target
    try:
        fileDescriptor = open(targetPath)
    except:
        Draw.PupMenu("Unable to open %s",(targetPath))        
        return  None
    activeObjs = Blender.Object.GetSelected()
    if len(activeObjs) > 0:
        activeObj = activeObjs[0]
    else:
        Draw.PupMenu("No object selected")
        return None    
    
    obj = activeObj.getData(mesh=True)    
    try:
        obj.verts
    except:
        Draw.PupMenu("The selected obj is not a mesh")
        return None
        
    #check mesh version
    if len(obj.verts) == 11787:
        print "Working on Mesh MH1.0.0prealpha"
        if len(obj.verts) < 11787:
            Draw.PupMenu("The selected obj is not last version of MHmesh")
            if len(obj.verts) == 11751:
                print "Working on Mesh MH0.9.2NR"
            elif len(obj.verts) < 11751:
                print "Working on Mesh 0.9.1 or earlier"
        
   
    current_target = targetPath
    targetData = fileDescriptor.readlines()
    fileDescriptor.close()
    targetBuffer = []
    maxIndexOfVerts = len(obj.verts)        
    for vData in targetData:
        vectorData = vData.split()
        if vectorData[0].find('#')==-1:
            if len(vectorData) < 4:
                vectorData = vData.split(',') #compatible old format
            mainPointIndex = int(vectorData[0])
            if mainPointIndex < maxIndexOfVerts:
                pointX = float(vectorData[1])
                pointY = float(vectorData[2])
                pointZ = float(vectorData[3])
                targetBuffer.append([mainPointIndex, pointX,pointY,pointZ])
            else:                
                Draw.PupMenu("WARNING: target has more verts than Base mesh")
    return 1

def saveTranslationTarget(targetPath):
    """
    This function saves a morph target file containing the difference between 
    the *originalVerts* positions and the actual vertex coordinates.

    Parameters
    ----------

    targetPath:
        *string*. A string containing the operating system path to the 
        file to be written.

    epsilon:
        *float*. The max value of difference between original vert and
        actual vert. If the distance is over epsilon, the vert is
        considered as modificated, so to save as target morph.
        ** EDITORIAL NOTE** This parameter is not implemented. 
        
    """

    global originalVerts
    global saveOnlySelectedVerts
    onlySelection = saveOnlySelectedVerts.val
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    epsilon = 0.001
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    obj = activeObj.getData(mesh=True)
    #obj = Mesh.Get("Base")
    modifiedVertsIndices = []
    groupToSave = None #TODO
    if not groupToSave:
        vertsToSave = range(len(obj.verts))
    else:
        pass #TODO verts from group

    nVertsExported = 0
    for index in vertsToSave:
        originalVertex = originalVerts[index]
        targetVertex = obj.verts[index]
        delta = vsub(targetVertex.co,originalVertex)
        dist =  vdist(originalVertex,targetVertex.co)
        if dist > epsilon:
            nVertsExported += 1
            dataToExport =  [index,delta[0],delta[1],delta[2]]
            if onlySelection == 1:
                if targetVertex.sel == 1:
                    modifiedVertsIndices.append(dataToExport)
            else:
                modifiedVertsIndices.append(dataToExport)

    try:
        fileDescriptor = open(targetPath, "w")
    except:
        print "Unable to open %s",(targetPath)
        return  None
  
    for data in modifiedVertsIndices:
        fileDescriptor.write("%d %f %f %f\n" % (data[0],data[1],data[2],data[3]))
    fileDescriptor.close()

    if nVertsExported == 0:
        print "Warning%t|Zero verts exported in file "+targetPath

    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()

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
    loadTranslationTarget(targetPath)
    pathParts = os.path.split(targetPath)
    headPath = pathParts[0]
    tailPath = pathParts[1]
    nameSuffix = tailPath[1:]
    targetPath = os.path.join(headPath,"r"+nameSuffix)
    doMorph(-1)
    saveTranslationTarget(targetPath)
    resetMesh()

def loadAllTargetInFolder(filepath):
    #Because Blender filechooser return a file
    #it's needed to extract the dirname
    folderToScan = os.path.dirname(filepath)
    targetList = os.listdir(folderToScan)
    for targetName in targetList:
        targetPath = os.path.join(folderToScan,targetName)
        loadTranslationTarget(targetPath)
        doMorph(0.5)


    

def loadInitialBaseCoords(path):
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

def loadSymVertsIndex(right=1):
    """
    Make the mesh symmetrical by reflecting the existing vertices across 
    to the left or right. By default this function reflects left to right.

    Parameters
    ----------

    right:
        *int*. A flag to indicate whether the new vertices will be reflected 
        across to the left or right. (1=right, 0=left)

    """

    global pairsPath
    global centersPath
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
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()


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

    
def resetMesh():
    """
    This function restores the initial base mesh coordinates.
    
    **Parameters:** This method has no parameters.
    
    """
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    actual_mesh = activeObj.getData(mesh=True)
    global originalVerts
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    for pointIndex, vCoords in enumerate(originalVerts):
        actual_mesh.verts[pointIndex].co[0] = vCoords[0]
        actual_mesh.verts[pointIndex].co[1] = vCoords[1]
        actual_mesh.verts[pointIndex].co[2] = vCoords[2]
    actual_mesh.update()
    actual_mesh.calcNormals()
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()


def absoluteToRelative(path):
    """
    It resave all targets in path from absolute (it mean
    the targets are referred to base neutral mesh) from relative (it mean the
    targets are referred to a different morph of base mesh). In example
    the target female_young_nilotid is saved not from base mesh, but from
    female_young. In other words, it's needed to apply female_young before apply
    female_young_nilotid.
    
    Parameters
    ----------
   
    path:     
      *path*.  Path of folder to examine.   
    """
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    data = activeObj.getData(mesh=True)  
    path = os.path.split(path)[0] 
    
    targetsFiles = os.listdir(path)
    targetsNames = []
    for targetFile in targetsFiles:
        if targetFile != "base_female.target" and \
            targetFile != "base_male.target":
                
            #targetFile != "base_female_child.target" and \
            #targetFile != "base_male_child.target" and \
            #targetFile != "base_female_old.target" and \
            #targetFile != "base_male_old.target":
            fileName = os.path.splitext(targetFile)
            targetName = fileName[0]
            targetPath = os.path.join(path, targetFile)
            if "female" in targetName:
                absoluteTarget = os.path.join(path,"base_female.target")                    
            else:
                absoluteTarget = os.path.join(path,"base_male.target")
            loadTranslationTarget(targetPath)
            doMorph(1.0)
            loadTranslationTarget(absoluteTarget)
            doMorph(-1.0)            
            saveTranslationTarget(targetPath)#Note it overwrite
            resetMesh()

originalVerts = loadInitialBaseCoords(basePath)







def draw():
    """
    This function draws the morph target on the screen and adds buttons to 
    enable utility functions to be called to process the target.

    **Parameters:** This method has no parameters.
    
    """
    global targetPath,morphFactor,rotVal,rotSum,current_target,selAxis
    global saveOnlySelectedVerts

    glClearColor(0.5, 0.5, 0.5, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2i(10, 150)
    Draw.Text("Make MH targets v2.2")
    glRasterPos2i(10, 140)
    Draw.Text("_____________________________________________")
    glRasterPos2i(10, 120)

    Draw.Button("Load", 2, 10, 100, 50, 20, "Load target")
    Draw.Button("Morph", 3, 60, 100, 50, 20, "Morph "+current_target.replace(current_path,""))
    Draw.Button("<=", 5, 110, 100, 30, 20, "Make left side symetrical to right side")
    Draw.Button("Reset", 10, 140, 100, 40, 20, "Return base object to its original state")
    Draw.Button("=>", 6, 180, 100, 30, 20, "Make right side symetrical to left side")
    morphFactor = Draw.Number("Value: ", 0, 10, 80, 100, 20, morphFactor.val, -1, 1, "Insert the value to apply the target")
    Draw.Button("Save", 1, 110, 80, 100, 20, "Save target")
    saveOnlySelectedVerts = Draw.Toggle("Save only selected verts",0,10,60,200,20,saveOnlySelectedVerts.val,"The target will affect only the selected verts")


def event(event, value):
    """
    This function handles keyboard events when the escape key or the 's' key 
    is pressed to exit or save the morph target file.

    Parameters
    ----------

    event:
        *int*. An indicator of the event to be processed
    value:
        *int*. A value **EDITORIAL NOTE: Need to find out what this is used for**

    """
    if event == Draw.ESCKEY and not value: Draw.Exit()
    elif event == Draw.SKEY:
        Window.FileSelector (saveSymVertsIndices, "Save Symm data")
    elif event == Draw.DKEY:
        selectSymmetricVerts()
    elif event == Draw.TKEY:
        Window.FileSelector (saveTranslationTargetAndHisSymm, "Save Target")
    elif event == Draw.LKEY:
        Window.FileSelector (loadAllTargetInFolder, "Load from folder")
    elif event == Draw.CKEY:
        Window.FileSelector (absoluteToRelative, "Select base_female")


def b_event(event):
    """
    This function handles events when the morph target is being processed.

    Parameters
    ----------

    event:
        *int*. An indicator of the event to be processed

    """
    global symmPath,selAxis,morphFactor
    if event == 0: pass
    elif event == 1:
        Window.FileSelector (saveTranslationTarget, "Save Target")
    elif event == 2:
        Window.FileSelector (loadTranslationTarget, "Load Target")
    elif event == 3:
        if current_target == "":
            Draw.PupMenu("No target loaded")
        elif current_target > "":
            doMorph(morphFactor.val)
    elif event == 5:
        loadSymVertsIndex(0)
    elif event == 6:
        loadSymVertsIndex(1)
    elif event == 10:
        resetMesh()
    Draw.Draw()
Draw.Register(draw, event, b_event)
