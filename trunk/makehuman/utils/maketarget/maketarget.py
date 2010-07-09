# You may use, modify and redistribute this module under the terms of the GNU GPL.
"""
Utility function for creating a morph target (part of the development functionality).

===========================  ===============================================================
Project Name:                **MakeHuman**
Product Home Page:           http://www.makehuman.org/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2010
Licensing:                   GPL3 
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

import sys
sys.path.append("./")
import os

import Blender
import maketargetlib
from Blender.BGL import *
from Blender import Draw
from Blender import Window

basePath = 'base.obj'
pairsPath = 'base.sym'
centersPath = 'base.sym.centers'
windowEditMode = Blender.Window.EditMode()

morphFactor = Draw.Create(1.0)
saveOnlySelectedVerts = Draw.Create(0)
rotationMode = Draw.Create(0)
poseMode = False
loadedTraslTarget = ""
loadedRotTarget = ""
loadedPoseTarget = ""
targetBuffer = [] #Loaded target Data
message = ""  
  
#--------SOME BLENDER SPECIFICS SHORTCUTS------------

def startEditing():
    global windowEditMode
    windowEditMode = Blender.Window.EditMode()
    Blender.Window.EditMode(0)

def endEditing():
    global windowEditMode
    Blender.Window.EditMode(windowEditMode)
    Blender.Window.RedrawAll()

def redrawAll():
    Blender.Window.RedrawAll()

def getVertices(n=0,name = None):
    if name:
        obj = Blender.Object.Get(name).getData(mesh=True)
    else:    
        obj = Blender.Object.GetSelected()[n].getData(mesh=True)
    vertices = [[v.co[0],v.co[1],v.co[2]] for v in obj.verts]
    return vertices

def getVertGroups(n=0):
    vertGroups = {}
    obj = Blender.Object.GetSelected()[n].getData(mesh=True)
    vertGroupNames = obj.getVertGroupNames()
    for n in vertGroupNames:
        vertGroups[n] = obj.getVertsFromGroup(n)
    return vertGroups

def getSelectedVertices(n=0):
    selectedVertices = []
    obj = Blender.Object.GetSelected()[n].getData(mesh=True)
    for i,v in enumerate(obj.verts):
        if v.sel == 1:
            selectedVertices.append(i)
    return selectedVertices
    
def selectVert(i, n=0):
    obj = Blender.Object.GetSelected()[n].getData(mesh=True)
    obj.verts[i].sel = 1
    obj.update()
    obj.calcNormals()

def updateVertices(vertices, n=0, name = None):
    if name:
        obj = Blender.Object.Get(name).getData(mesh=True)
    else:    
        obj = Blender.Object.GetSelected()[n].getData(mesh=True)    
    for i,v in enumerate(vertices):
       obj.verts[i].co[0], obj.verts[i].co[1],obj.verts[i].co[2] = v[0],v[1],v[2]
    obj.update()
    obj.calcNormals()
    
def colorVertices(vertColors, n=0):
    obj = Blender.Object.GetSelected()[n].getData(mesh=True)
    obj.vertexColors = True
    for f in obj.faces:
        for i, v in enumerate(f):            
            col = f.col[i]
            col2 = vertColors[v.index]
            print col2
            col.r = col2[0]
            col.g = col2[1]
            col.b = col2[2]
    obj.update()
    obj.calcNormals()

#-------MAKETARGET CALLBACKS----------------------

def loadTarget(path):
    global loadedTraslTarget,rotationMode,loadedRotTarget,loadedPoseTarget,poseMode    
    startEditing()    
    if os.path.splitext(path)[1] == ".rot":
        loadedRotTarget = path
        loadedTraslTarget = ""
        loadedPoseTarget = ""
        rotationMode.val = 1
        poseMode = False
    if os.path.splitext(path)[1] == ".target":
        loadedTraslTarget = path
        loadedRotTarget = ""
        loadedPoseTarget = ""
        rotationMode.val = 0
        poseMode = False
    if os.path.splitext(path)[1] == ".pose":
        loadedPoseTarget = path
        loadedTraslTarget = ""
        loadedRotTarget = ""
        poseMode = True    
    endEditing()
  
def applyTarget(mFactor, n=0):
    global loadedTraslTarget,rotationMode,loadedRotTarget,loadedPoseTarget
    startEditing()
    vertices = getVertices(n)
    if rotationMode.val and not poseMode:
        maketargetlib.loadRotTarget(vertices,loadedRotTarget,mFactor)
    if not rotationMode.val and not poseMode:
        maketargetlib.loadTraslTarget(vertices,loadedTraslTarget,mFactor)
    if not rotationMode.val and poseMode:        
        maketargetlib.loadPoseFromFile(vertices,loadedPoseTarget,mFactor)
    if rotationMode.val and poseMode:
        maketargetlib.loadPoseFromFile(vertices,loadedPoseTarget,mFactor,onlyRot = True)        
    updateVertices(vertices)
    endEditing()

def applyPoseFromFolder(path, n=0):
    global morphFactor
    startEditing()
    vertices = getVertices(n)
    maketargetlib.loadPoseFromFolder(vertices,path,morphFactor.val)
    updateVertices(vertices)
    endEditing()
    
def alignPCA():
    startEditing()
    vertices0 = getVertices(0)
    vertices1 = getVertices(1)    
    updateVertices(maketargetlib.align_PCA(vertices0, vertices1),1)
    endEditing()

def saveTarget(path):    
    global saveOnlySelectedVerts,basePath, message
    if os.path.exists(path):
        message =  "Error: file already exist"
        redrawAll()
        return    
    verticesTosave = []    
    vertices = getVertices()   
    if saveOnlySelectedVerts.val:
        verticesTosave = getSelectedVertices()
    else:
        verticesTosave = xrange(len(vertices))
    if os.path.splitext(path)[1] == ".rot":        
        maketargetlib.saveRotTargets(vertices, path, basePath,getSelectedVertices())
    else:
        maketargetlib.saveTraslTarget(vertices, path, basePath, verticesTosave)
    message = "Saved in %s"%(path)
    redrawAll()

def seekGroup():
    vertGroups = []
    vertSelect = getSelectedVertices()   
    vertices = getVertices()
    vertGroups  = getVertGroups()    
    maketargetlib.seekGroupName(vertices, vertSelect, vertGroups)
    
def reset():
    global basePath
    startEditing()    
    vertices = getVertices()
    maketargetlib.resetMesh(vertices, basePath)
    updateVertices(vertices)
    endEditing()
    
def symm(rightMirror, n=0):
    global pairsPath, centersPath
    startEditing() 
    vertices = getVertices(n)
    maketargetlib.symmetrise(vertices, pairsPath, centersPath, rightMirror)    
    updateVertices(vertices)
    endEditing()

def scaleRotTarget(path):
    global morphFactor,basePath
    maketargetlib.saveScaledRotTarget(path,morphFactor.val)
    
def processingTargets(path, n=0):
    global morphFactor
    startEditing() 
    vertices = getVertices(n)
    verticesTosave = xrange(len(vertices))
    maketargetlib.processingTargets(path,basePath,vertices,morphFactor.val,verticesTosave)
    updateVertices(vertices,n)
    endEditing()
    
def adapt():
    startEditing()
    base = getVertices(0)
    verticesToAdapt = getSelectedVertices(0)
    scan = getVertices(1)    
    maketargetlib.adaptMesh(base, scan, verticesToAdapt)
    updateVertices(base,0)
    endEditing()

def align():    
    startEditing()
    maskBaseVerts = getVertices(name="mask_mh")
    maskScanVerts = getVertices(name="mask_scan")
    if len(maskBaseVerts) != len(maskScanVerts):
        message = "Error: Masks with different number of vertices: %d vs %d"%(len(maskBaseVerts),len(maskScanVerts))
        return
    scanVerts = getVertices(0)    
    maketargetlib.alignScan(maskBaseVerts, maskScanVerts, scanVerts)
    updateVertices(scanVerts,0)
    updateVertices(maskScanVerts,name="mask_scan")
    message = "Alignment done!"
    endEditing()  
    
def saveSelVerts(path, n= 0):
    if os.path.exists(path):
        message =  "Error: file already exist"
        redrawAll()
        return 
    maketargetlib.saveIndexSelectedVerts(getSelectedVertices(n), path)
    
def loadSelVerts(path, n= 0):
    startEditing()
    selVerts = maketargetlib.loadIndexSelectedVerts(path)
    for i in selVerts:
        selectVert(i)
    endEditing()  
    
def analyseTarget(n=0):
    global targetBuffer
    vertices = getVertices(n)
    vertColors = maketargetlib.analyzeTarget(vertices, targetBuffer, 1)
    colorVertices(vertColors, n=0)


    
    


#-----------------BLENDER GUI------------------

def draw():
    """
    This function draws the morph target on the screen and adds buttons to
    enable utility functions to be called to process the target.

    **Parameters:** This method has no parameters.

    """
    global message
    global targetPath,morphFactor,rotVal,rotSum,currentTarget,selAxis,rotationMode
    global saveOnlySelectedVerts,loadedTraslTarget, loadedRotTarget, loadedPoseTarget
    
    glClearColor(0.5, 0.5, 0.5, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2i(10, 300)
    Draw.Text("MakeTargets v3.2")

    glColor3f(0.5, 0.0, 0.0)
    glRasterPos2i(10, 250)
    Draw.Text("Msg: %s"%(message))

    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2i(10, 230)
    Draw.Text("Target: %s"%(os.path.basename(loadedTraslTarget)))
    
    if loadedTraslTarget:
        fileText = os.path.basename(loadedTraslTarget)
    elif loadedRotTarget:
        fileText = os.path.basename(loadedRotTarget)
    elif loadedPoseTarget:
        fileText = os.path.basename(loadedPoseTarget)
    

    Draw.Button("Load", 2, 10, 200, 50, 20, "Load target")
    Draw.Button("Morph", 3, 60, 200, 50, 20, "Morph ")
    Draw.Button("<=", 5, 110, 200, 30, 20, "Make left side symetrical to right side")
    Draw.Button("Reset", 10, 140, 200, 40, 20, "Return base object to its original state")
    Draw.Button("=>", 6, 180, 200, 30, 20, "Make right side symetrical to left side")
    morphFactor = Draw.Number("Value: ", 0, 10, 180, 100, 20, morphFactor.val, -2, 2, "Insert the value to apply the target")
    Draw.Button("Save", 1, 110, 180, 100, 20, "Save target")
    saveOnlySelectedVerts = Draw.Toggle("Save only selected verts",0,10,160,200,20,saveOnlySelectedVerts.val,"The target will affect only the selected verts")
    rotationMode = Draw.Toggle("Rotations",0,10,140,200,20,rotationMode.val,"Work with rotation targets")


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
    elif event == Draw.AKEY:
        Window.FileSelector (saveSymVertsIndices, "Save Symm data")
    elif event == Draw.BKEY:
        selectSymmetricVerts()
    elif event == Draw.CKEY:
        Window.FileSelector (saveTranslationTargetAndHisSymm, "Save Target")
    elif event == Draw.DKEY:
        Window.FileSelector (loadAlloadTargetInFolder, "Load from folder")
    elif event == Draw.EKEY:
        align()
    elif event == Draw.FKEY:
        Window.FileSelector (generateTargetsDB, "Generate DB from")
    elif event == Draw.GKEY:
        Window.FileSelector (linkMaskBug, "Link Mask")
    elif event == Draw.HKEY:
        Window.FileSelector (saveSelVerts, "Save index of selected vertices")
    elif event == Draw.IKEY:
        Window.FileSelector (findClosereset, "Reconstruct")
    elif event == Draw.LKEY:
        adapt()
    elif event == Draw.MKEY:
        seekGroup()
    elif event == Draw.NKEY:
        Window.FileSelector (loadSelVerts, "Load index of verts to select")
    elif event == Draw.OKEY:
        analyseTarget()
    elif event == Draw.PKEY:
        Window.FileSelector (scaleRotTarget, "Scale Rot target")
    elif event == Draw.QKEY:
        Window.FileSelector (applyPoseFromFolder, "Load pose from folder") 
    elif event == Draw.RKEY:
        alignPCA()    
    elif event == Draw.SKEY:
        Window.FileSelector (processingTargets, "Process targets") 
        
  
        

def buttonEvents(event):
    """
    This function handles events when the morph target is being processed.

    Parameters
    ----------

    event:
        *int*. An indicator of the event to be processed

    """
    global symmPath,selAxis,morphFactor,loadedTraslTarget
    global currentTarget
    if event == 0: pass
    elif event == 1:
        Window.FileSelector (saveTarget, "Save Target",loadedTraslTarget)
    elif event == 2:
        Window.FileSelector (loadTarget, "Load Target")
    elif event == 3:
        applyTarget(morphFactor.val)
    elif event == 5:
        symm(0)
    elif event == 6:
        symm(1)
    elif event == 10:
        reset()
    elif event == 20:
        align()
    Draw.Draw()
    
Draw.Register(draw, event, buttonEvents)
