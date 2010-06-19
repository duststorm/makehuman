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
loadedTarget = ""
targetBuffer = [] #Loaded target Data    
  
#--------SOME BLENDER SPECIFICS SHORTCUTS------------

def startEditing():
    global windowEditMode
    windowEditMode = Blender.Window.EditMode()
    Blender.Window.EditMode(0)

def endEditing():
    global windowEditMode
    Blender.Window.EditMode(windowEditMode)
    Blender.Window.RedrawAll()

def getVertices(n=0):
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

def updateVertices(vertices, n=0):
    obj = Blender.Object.GetSelected()[n].getData(mesh=True)
    for i,v in enumerate(vertices):
       obj.verts[i].co[0], obj.verts[i].co[1],obj.verts[i].co[2] = v[0],v[1],v[2]
    obj.update()
    obj.calcNormals()

#-------MAKETARGET CALLBACKS----------------------
  
def lTarget(path):
    global targetBuffer,loadedTarget     
    targetBuffer = maketargetlib.loadTarget(path)
    loadedTarget = path

def aTarget(mFactor):
    global targetBuffer
    startEditing()
    vertices = getVertices()
    maketargetlib.applyTarget(vertices, targetBuffer, mFactor)
    updateVertices(vertices)
    endEditing()

def sTarget(path):
    global saveOnlySelectedVerts,basePath
    verticesTosave = []    
    vertices = getVertices()   
    if saveOnlySelectedVerts.val:
        verticesTosave = getSelectedVertices()
    else:
        verticesTosave = xrange(len(vertices))
    maketargetlib.saveTarget(vertices, path, basePath, verticesTosave)

def sGroupName():
    vertGroups = []
    vertSelect = getSelectedVertices()   
    vertices = getVertices()
    vertGroups  = getVertGroups()    
    maketargetlib.seekGroupName(vertices, vertSelect, vertGroups)
    
def rMesh():
    global basePath
    startEditing()    
    vertices = getVertices()
    maketargetlib.resetMesh(vertices, basePath)
    updateVertices(vertices)
    endEditing()
    
def symm(rightMirror):
    global pairsPath, centersPath
    startEditing() 
    vertices = getVertices()
    maketargetlib.symmetrise(vertices, pairsPath, centersPath, rightMirror)    
    updateVertices(vertices)
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
    maskBaseVerts = getVertices(0)
    maskScanVerts = getVertices(1)
    scanVerts = getVertices(2)    
    maketargetlib.alignScan(maskBaseVerts, maskScanVerts, scanVerts)
    updateVertices(scanVerts,2)
    updateVertices(maskScanVerts,1)
    endEditing()  
    
def saveSelVerts(path, n= 0):
    maketargetlib.saveIndexSelectedVerts(getSelectedVertices(n), path)
    
def loadSelVerts(path, n= 0):
    startEditing()
    selVerts = maketargetlib.loadIndexSelectedVerts(path)
    for i in selVerts:
        selectVert(i)
    endEditing()  
    


#-----------------BLENDER GUI------------------

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
    Draw.Text("Make MH targets v3.0")
    
    glRasterPos2i(10, 120)

    Draw.Button("Align", 20, 10, 150, 50, 20, "Align scans")

    Draw.Button("Load", 2, 10, 100, 50, 20, "Load target")
    Draw.Button("Morph", 3, 60, 100, 50, 20, "Morph ")
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
    elif event == Draw.AKEY:
        Window.FileSelector (saveSymVertsIndices, "Save Symm data")
    elif event == Draw.BKEY:
        selectSymmetricVerts()
    elif event == Draw.CKEY:
        Window.FileSelector (saveTranslationTargetAndHisSymm, "Save Target")
    elif event == Draw.DKEY:
        Window.FileSelector (loadAllTargetInFolder, "Load from folder")
    elif event == Draw.EKEY:
        alignMasks()
    elif event == Draw.FKEY:
        Window.FileSelector (generateTargetsDB, "Generate DB from")
    elif event == Draw.GKEY:
        Window.FileSelector (linkMaskBug, "Link Mask")
    elif event == Draw.HKEY:
        Window.FileSelector (saveSelVerts, "Save index of selected vertices")
    elif event == Draw.IKEY:
        Window.FileSelector (findCloserMesh, "Reconstruct")
    elif event == Draw.LKEY:
        adapt()
    elif event == Draw.MKEY:
        sGroupName()
    elif event == Draw.NKEY:
        Window.FileSelector (loadSelVerts, "Load index of verts to select")

def b_event(event):
    """
    This function handles events when the morph target is being processed.

    Parameters
    ----------

    event:
        *int*. An indicator of the event to be processed

    """
    global symmPath,selAxis,morphFactor
    global current_target
    if event == 0: pass
    elif event == 1:
        Window.FileSelector (sTarget, "Save Target",loadedTarget)
    elif event == 2:
        Window.FileSelector (lTarget, "Load Target")
    elif event == 3:
        aTarget(morphFactor.val)
    elif event == 5:
        symm(0)
    elif event == 6:
        symm(1)
    elif event == 10:
        rMesh()
    elif event == 20:
        align()
    Draw.Draw()
    
Draw.Register(draw, event, b_event)
