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
import os.path


__docformat__ = 'restructuredtext'

import sys
sys.path.append("./")
makehuman_src = "../../"
sys.path.append(os.path.join(makehuman_src, "/utils/maketarget/") )
sys.path.append(os.path.join(makehuman_src, "/utils/svd_tools/fit/") )
sys.path.append(os.path.join(makehuman_src, "/utils/") )
sys.path.append(os.path.join(makehuman_src, "/core/") )
sys.path.append(os.path.join(makehuman_src, "/utils/topology_translator/") )
import os

import Blender
import maketargetlib
from Blender.BGL import *
from Blender import Draw
from Blender import Window
import bpy
from Blender.Mathutils import *
import blender2obj
from Blender import Types

basePath = 'base.obj'
pairsPath = 'base.sym'
centersPath = 'base.sym.centers'
windowEditMode = Blender.Window.EditMode()
GUIswitch = 1

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

def getVertices(n=0,name = None, copy = True):
    if name:
        obj = Blender.Object.Get(name).getData(mesh=True)
    else:    
        obj = Blender.Object.GetSelected()[n].getData(mesh=True)
    if copy:
        vertices = [[v.co[0],v.co[1],v.co[2]] for v in obj.verts]
    else:
        vertices = obj.verts
    return vertices

def getObjName(n=0):

    obj = Blender.Object.GetSelected()[n]
    return obj.getName()

def getVertGroups(n=0, name = None):
    vertGroups = {}
    if name:
        obj = Blender.Object.Get(name).getData(mesh=True)
    else:    
        obj = Blender.Object.GetSelected()[n].getData(mesh=True)
    vertGroupNames = obj.getVertGroupNames()
    for n in vertGroupNames:
        vertGroups[n] = obj.getVertsFromGroup(n)
    return vertGroups

def getSelectedVertices(n=0, name = None):
    selectedVertices = []
    if name:
        obj = Blender.Object.Get(name).getData(mesh=True)
    else:    
        obj = Blender.Object.GetSelected()[n].getData(mesh=True)
    for i,v in enumerate(obj.verts):
        if v.sel == 1:
            selectedVertices.append(i)
    return selectedVertices
    
def selectVert(vertsToSelect, n=0, name = None):
    if name:
        obj = Blender.Object.Get(name).getData(mesh=True)
    else:
        obj = Blender.Object.GetSelected()[n].getData(mesh=True)
    for i in vertsToSelect:
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
    
def createMesh(verts, faces, name):
    """
    Create mesh on the Blender scene
    """
    scn = bpy.data.scenes.active 
    mesh = bpy.data.meshes.new(name)
    mesh.verts.extend(verts)
    mesh.faces.extend(faces)
    ob = scn.objects.new(mesh, name)
    return ob
    
def applyTransforms():
    objs = Blender.Object.Get()
    for obj in objs:            
        if type(obj.getData(mesh=True)) == Types.MeshType:
            mesh = obj.getData(mesh=True)
            m = obj.getMatrix()           
            obj.setLocation(0,0,0)
            obj.setSize(1,1,1)
            obj.setEuler(0,0,0)
            mesh.transform(m)      # Convert verts to world space            
            mesh.update()
        

#-------MAKETARGET CALLBACKS----------------------

def checkSelectedMesh():
    global message
    name = getObjName()
    if name == "Base" or name == "scan_mask" or name == "base_mask":
        message = "WARNING: you have selected %s instead the scanner mesh"%(name)
        print message
        return 0
    else:
        return 1


def buildScan2Mesh(path):
    global message
    checkSelectedMesh()
    main_dir = os.path.dirname(path)
    target_dir = os.path.join(main_dir,"targets_db")
    if not os.path.isdir(target_dir):
        message = "The build folder must contain a 'target_db' folder with the db"
        print message
        return

    head_mesh = os.path.join(main_dir,"base_mesh.obj")
    head_mask = os.path.join(main_dir,"base_mask.obj")
    prefix = os.path.join(main_dir,"fitdata")
    maketargetlib.scan2meshBuild(target_dir, head_mesh ,head_mask,prefix)
    
def fitScan2Mesh(path):
    main_dir = os.path.dirname(path)
    #target_dir = os.path.join(main_dir,"targets_db")
    head_mesh = os.path.join(main_dir,"base_mesh.obj")
    head_mask = os.path.join(main_dir,"base_mask.obj")
    scan_mesh = os.path.join(main_dir,"scan_mesh.obj")
    scan_mask = os.path.join(main_dir,"scan_mask.obj")
    fit_verts = os.path.join(main_dir,"face.verts")
    output = os.path.join(main_dir,"result.target")
    prefix = os.path.join(main_dir,"fitdata")    
    maketargetlib.scan2meshFit(head_mesh,head_mask,scan_mesh,scan_mask,fit_verts,prefix,output)
    
def saveScanMask(path):
    mainDir = os.path.dirname(path)
    scanMask = Blender.Object.Get("scan_mask") 
    scanMaskPath = os.path.join(mainDir,"scan_mask.obj")   
    bExporter = blender2obj.Blender2obj(scanMask,1)    
    bExporter.write(scanMaskPath,1)
    
def saveBaseMask(path):
    mainDir = os.path.dirname(path)
    baseMask = Blender.Object.Get("base_mask") 
    baseMaskPath = os.path.join(mainDir,"base_mask.obj")   
    bExporter = blender2obj.Blender2obj(baseMask,1)    
    bExporter.write(baseMaskPath,1)

def saveBaseMesh(path):
    mainDir = os.path.dirname(path)
    baseMask = Blender.Object.Get("Base")
    baseMaskPath = os.path.join(mainDir,"base_mesh.obj")
    bExporter = blender2obj.Blender2obj(baseMask,1)
    bExporter.write(baseMaskPath,1)
    
def saveScanMesh(path):
    mainDir = os.path.dirname(path)
    scanMesh = Blender.Object.GetSelected()[0]    
    scanMeshPath = os.path.join(mainDir,"scan_mesh.obj")   
    bExporter = blender2obj.Blender2obj(scanMesh,1)    
    bExporter.write(scanMeshPath,1)
    
def saveScanElements(path):
    saveScanMask(path)    
    saveBaseMask(path)
    saveScanMesh(path)
    #buildScan2Mesh(path)
    loadSelVertsBase(path)
    #fitScan2Mesh(path)

def buildSVNdb(path):

    saveBaseMesh(path)
    saveBaseMask(path)
    buildScan2Mesh(path)


def scan2mh(path):
    saveScanMask(path)
    saveScanMesh(path)
    fitScan2Mesh(path)
    

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

def scanReg(scan):
    startEditing()
    (vertsM, facesM) = maketargetlib.scanRegistration(scan)
    name = scan.split('\\')[-1].split('/')[-1]
    ob = createMesh(vertsM, facesM, "scan_mesh")
    #apply rotation matrix as the base
    #matrixR = RotationMatrix(90, 4, 'x')
    #put scan on the left of base
    matrixT = TranslationMatrix(Vector(-3, 7, 0))
    ob.setMatrix(matrixT)
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
    vertSelect = getSelectedVertices()   
    vertices = getVertices()
    vertGroups  = getVertGroups()    
    maketargetlib.seekGroupName(vertices, vertSelect, vertGroups)

def saveGroups(path):    
    vertGroups  = getVertGroups().keys()
    vertGroups.sort()   
    maketargetlib.saveGroups(vertGroups, path, "joint")
    
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
    
def adapt(path):
    print "Fitting face...final step"
    if checkSelectedMesh == 0:
        return
    startEditing()
    base = getVertices(name="Base")
    verticesToAdapt = maketargetlib.loadVertsIndex(path)
    #print verticesToAdapt
    scan = getVertices(0)    
    maketargetlib.adaptMesh(base, scan, verticesToAdapt)
    updateVertices(base,name="Base")
    endEditing()

def align():
    global message
    startEditing()
    maskBaseVerts = getVertices(name="base_mask")
    maskScanVerts = getVertices(name="scan_mask")
    
    if len(maskBaseVerts) != len(maskScanVerts):
        message = "Error: Masks with different number of vertices: %d vs %d"%(len(maskBaseVerts),len(maskScanVerts))
        return
    scanVerts = getVertices(0)
    print len(scanVerts)
    maketargetlib.alignScan(maskBaseVerts, maskScanVerts, scanVerts)
    updateVertices(scanVerts,0)
    updateVertices(maskScanVerts,name="scan_mask")    
    endEditing()  
    
def saveSelVerts(path, n= 0):
    if os.path.exists(path):
        message =  "Error: file already exist"
        redrawAll()
        return 
    maketargetlib.saveIndexSelectedVerts(getSelectedVertices(n), path)
    
def loadSelVerts(path):
    startEditing()
    selVerts = maketargetlib.loadVertsIndex(path)
    selectVert(selVerts)
    endEditing()

def loadSelVertsBase(path):
    print "Loading verts to select"
    mainDir = os.path.dirname(path)
    path = os.path.join(mainDir, "face.verts")
    startEditing()
    selVerts = maketargetlib.loadVertsIndex(path)    
    selectVert(selVerts, name = "Base")
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

    if GUIswitch == 1:

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

        fileText = ""
        if loadedTraslTarget:
            fileText = os.path.basename(loadedTraslTarget)
        elif loadedRotTarget:
            fileText = os.path.basename(loadedRotTarget)
        elif loadedPoseTarget:
            fileText = os.path.basename(loadedPoseTarget)
        Draw.Text("Target: %s"%(fileText))


        Draw.Button("Load", 1, 10, 200, 50, 20, "Load target")
        Draw.Button("Morph", 2, 60, 200, 50, 20, "Morph ")
        Draw.Button("<=", 3, 110, 200, 30, 20, "Make left side symetrical to right side")
        Draw.Button("Reset", 4, 140, 200, 40, 20, "Return base object to its original state")
        Draw.Button("=>", 5, 180, 200, 30, 20, "Make right side symetrical to left side")
        morphFactor = Draw.Number("Value: ", 0, 10, 180, 100, 20, morphFactor.val, -2, 2, "Insert the value to apply the target")
        Draw.Button("Save", 6, 110, 180, 100, 20, "Save target")
        saveOnlySelectedVerts = Draw.Toggle("Save only selected verts",0,10,160,200,20,saveOnlySelectedVerts.val,"The target will affect only the selected verts")
        rotationMode = Draw.Toggle("Rotations",0,10,140,200,20,rotationMode.val,"Work with rotation targets")

    if GUIswitch == 2:

        glClearColor(0.5, 0.5, 0.5, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glColor3f(0.0, 0.0, 0.0)
        glRasterPos2i(10, 300)
        Draw.Text("ScanToMH vers. 1")

        glColor3f(0.5, 0.0, 0.0)
        glRasterPos2i(10, 250)
        Draw.Text("Msg: %s"%(message))

        glColor3f(0.0, 0.0, 0.0)
        glRasterPos2i(10, 230)

        Draw.Button("Load ob", 30, 10, 200, 80, 20, "Load wavefront obj")
        Draw.Button("Fit", 32, 90, 200, 80, 20, "Morph ")
        Draw.Button("Build", 31, 170, 200, 80, 20, "Build targets db")
        Draw.Button("Save verts", 33, 10, 180, 80, 20, "Save selected verts")
        
       
        


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
    global GUIswitch
    GUIswitchMax = 2
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
        adapt("face.verts")
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
    elif event == Draw.TKEY:
        Window.FileSelector (saveGroups, "Save vertgroups")
    elif event == Draw.UKEY:
        Window.FileSelector (scanReg, "Load scan")
    elif event == Draw.WKEY:
        Window.FileSelector (buildScan2Mesh, "build db")
    elif event == Draw.XKEY:
        Window.FileSelector (fitScan2Mesh, "svd fitting")
    elif event == Draw.YKEY:
        Window.FileSelector (saveScanElements, "save scan elements")
    elif event == Draw.KKEY:
        applyTransforms()
    elif event == Draw.PAGEDOWNKEY and not value and GUIswitch < GUIswitchMax:
        GUIswitch += 1
    elif event == Draw.PAGEUPKEY and not value and GUIswitch > 1:
        GUIswitch -= 1
    print GUIswitch
    Draw.Draw()





def buttonEvents(event):
    """
    This function handles events when the morph target is being processed.

    Parameters
    ----------

    event:
        *int*. An indicator of the event to be processed

    """
    global symmPath,selAxis,morphFactor
    global loadedTraslTarget, loadedRotTarget, loadedPoseTarget
    global currentTarget

    fileToSaveName = ""
    if loadedTraslTarget != "":
        fileToSaveName = loadedTraslTarget
    if loadedRotTarget != "":
        fileToSaveName = loadedRotTarget
    if loadedPoseTarget != "":
        fileToSaveName = loadedPoseTarget

    if event == 0: pass
    elif event == 1:
        Window.FileSelector (loadTarget, "Load Target")
    elif event == 2:
        applyTarget(morphFactor.val)
    elif event == 3:
        symm(0)
    elif event == 4:
        reset()
    elif event == 5:
        symm(1)
    elif event == 6:
        Window.FileSelector (saveTarget, "Save Target",fileToSaveName)
    elif event == 30:
        Window.FileSelector (scanReg, "Load scan")
    elif event == 31:
        Window.FileSelector (buildSVNdb, "Build svn db","build.tmp")
    elif event == 32:
        Window.FileSelector (scan2mh, "Fit scan to mh")
    elif event == 33:
        Window.FileSelector (saveSelVerts, "Save selected vert", "face.verts")
    Draw.Draw()

Draw.Register(draw, event, buttonEvents)



