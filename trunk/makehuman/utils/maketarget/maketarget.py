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
  
#--------SOME BLENDER SPECIFICS SHORTCUT------------

def startEditing():
    global windowEditMode
    windowEditMode = Blender.Window.EditMode()
    Blender.Window.EditMode(0)

def endEditing():
    global windowEditMode
    Blender.Window.EditMode(windowEditMode)
    Blender.Window.RedrawAll()

def getVertices():
    obj = Blender.Object.GetSelected()[0].getData(mesh=True)
    vertices = [[v.co[0],v.co[1],v.co[2]] for v in obj.verts]
    return vertices

def getVertGroups():
    vertGroups = {}
    obj = Blender.Object.GetSelected()[0].getData(mesh=True)
    vertGroupNames = obj.getVertGroupNames()
    for n in vertGroupNames:
        vertGroups[n] = obj.getVertsFromGroup(n)
    return vertGroups

def getSelectedVertices():
    selectedVertices = []
    obj = Blender.Object.GetSelected()[0].getData(mesh=True)
    for i,v in enumerate(obj.verts):
        if v.sel == 1:
            selectedVertices.append(i)
    return selectedVertices

def updateVertices(vertices):
    obj = Blender.Object.GetSelected()[0].getData(mesh=True)
    for i,v in enumerate(vertices):
       obj.verts[i].co[0], obj.verts[i].co[1],obj.verts[i].co[2] = v[0],v[1],v[2]
    obj.update()

#-------MAKETARGET CALLBACKS----------------------
  
def lTarget(path):
    global targetBuffer     
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
    elif event == Draw.SKEY:
        Window.FileSelector (saveSymVertsIndices, "Save Symm data")
    elif event == Draw.DKEY:
        selectSymmetricVerts()
    elif event == Draw.TKEY:
        Window.FileSelector (saveTranslationTargetAndHisSymm, "Save Target")
    elif event == Draw.LKEY:
        Window.FileSelector (loadAllTargetInFolder, "Load from folder")
    elif event == Draw.CKEY:
        alignMasks()
    elif event == Draw.HKEY:
        Window.FileSelector (generateTargetsDB, "Generate DB from")
    elif event == Draw.UKEY:
        Window.FileSelector (linkMaskBug, "Link Mask")
    elif event == Draw.PKEY:
        Window.FileSelector (saveIndexSelectedVerts, "Save index of selected vertices")
    elif event == Draw.AKEY:
        Window.FileSelector (findCloserMesh, "Reconstruct")
    elif event == Draw.JKEY:
        Window.FileSelector (utility6, "adjust foints")
    elif event == Draw.KKEY:
        sGroupName()

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
        loadSymVertsIndex(0)
    elif event == 6:
        loadSymVertsIndex(1)
    elif event == 10:
        rMesh()
    elif event == 20:
        alignMasks()
    Draw.Draw()
Draw.Register(draw, event, b_event)
