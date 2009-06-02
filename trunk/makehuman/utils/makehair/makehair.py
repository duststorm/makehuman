"""
===========================  ===============================================================
Project Name:                **MakeHuman**
Product Home Page:           http://www.makehuman.org/
Google Home Page:            http://code.google.com/p/makehuman/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2009
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://sites.google.com/site/makehumandocs/developers-guide
===========================  ===============================================================
"""



import Blender
import string
import os
import sys
import math
import random
mainPath = Blender.sys.dirname(Blender.Get('filename'))
sys.path.append(mainPath)
from Blender.Draw import *
from Blender.BGL import *
from Blender import Scene
from Blender import Types
from Blender.Scene import Render
from Blender import Window
import subprocess
import hairgenerator

humanMesh = Blender.Object.Get("Base")

hairsClass = hairgenerator.Hairgenerator(humanMesh.getData())
hairDiameter = Create(hairsClass.hairDiameter)
nHairs= Create(hairsClass.numberOfHairs)
randomFact= Create(hairsClass.randomFact)
percOfRebels = Create(hairsClass.percOfRebels)
clumptype = Create(hairsClass.clumptype)
tuftSize= Create(hairsClass.tuftSize)
rootColor= Create(hairsClass.rootColor[0],hairsClass.rootColor[1],hairsClass.rootColor[2])
tipColor= Create(hairsClass.tipColor[0],hairsClass.tipColor[1],hairsClass.tipColor[2])


def convertCoords(obj):

    #print "NAME: ",obj.getName()
    R2D = 57.2957 #Radiant to degree
    objLoc = obj.getLocation()
    objRot = obj.getEuler()
    objSize = obj.getSize()

    LocX =  objLoc[0]
    LocY =  objLoc[1]
    LocZ =  objLoc[2]

    RotX = objRot[0]*R2D
    RotY = objRot[1]*R2D
    RotZ = objRot[2]*R2D

    SizeX = objSize[0]
    SizeY = objSize[1]
    SizeZ = objSize[2]

    #Convert Blender Coords in Renderman Coords
    #rightHandled in leftHandled

    locX = LocX
    locY = LocY
    locZ = -LocZ

    rotX = -RotX
    rotY = -RotY
    rotZ = RotZ

    sizeX = SizeX
    sizeY = SizeY
    sizeZ = SizeZ

    return (locX,locY,locZ,rotX,rotY,rotZ,sizeX,sizeY,sizeZ)




def writeHeader(ribfile,imgFile):

    #ribfile.write('Option "searchpath" "texture" ["%s"]\n'%(texturesdir + ":" + shadowdir))

    display = Scene.GetCurrent()
    context = display.getRenderingContext()
    yResolution = context.imageSizeY()
    xResolution = context.imageSizeX()
    if xResolution >= yResolution:
        factor = yResolution / float(xResolution)
    else:
        factor = xResolution / float(yResolution)

    scene = Blender.Scene.GetCurrent()
    camobj = scene.getCurrentCamera()
    (locX,locY,locZ,rotX,rotY,rotZ,sizeX,sizeY,sizeZ) = convertCoords(camobj)
    camera = Blender.Camera.Get(camobj.getData().name)

    ribfile.write('Option "statistics" "endofframe" [1]\n')
    #ribfile.write("Option \"searchpath\" \"shader\" \"data/shaders/renderman:&\"\n")
    ribfile.write('Projection "perspective" "fov" [%s]\n'%(360.0 * math.atan(factor * 16.0 / camera.lens) /math.pi))
    ribfile.write('Format %s %s 1\n' % (xResolution, yResolution))
    ribfile.write("Clipping %s %s\n" % (camera.clipStart, camera.clipEnd))
    ribfile.write('PixelSamples %s %s\n'%(2, 2))
    ribfile.write('Sides 2\n')
    ribfile.write('Display "00001.tif" "framebuffer" "rgb"\n')
    ribfile.write('Display "+%s" "file" "rgba"\n' % imgFile)

    ribfile.write("\t\tRotate %s 1 0 0\n" %(-rotX))
    ribfile.write("\t\tRotate %s 0 1 0\n" %(-rotY))
    ribfile.write("\t\tRotate %s 0 0 1\n" %(-rotZ))
    ribfile.write("\t\tTranslate %s %s %s\n" %(-locX, -locY, -locZ))

    ribfile.write('WorldBegin\n')


def ambientLight(ribfile):
    if Blender.World.Get() != []:
        world = Blender.World.Get()[0]
        aR = world.amb[0]
        aG = world.amb[1]
        aB = world.amb[2]
        ribfile.write('\tLightSource "ambientlight" 998 "intensity" [1] "color lightcolor" [%s %s %s]\n\n'%(aR, aG, aB))

def writePolyObj(fileObj, mesh): 
	
	objFile = file(fileObj,'w')
	index = 0
	facenum = len(mesh.faces)
	
	if mesh.hasFaceUV() == 1:
			objFile.write('Declare "st" "facevarying float[2]"\n')
			
	objFile.write("PointsPolygons [");
	for face in mesh.faces:
		objFile.write('%s '%(len(face.v)))
		index = index + 1
	
	objFile.write("] ")
	objFile.write("[ ")
	for face in mesh.faces:
		num = len(face.v)
		if num == 3 or num == 4:
			for vert in face.v:
				objFile.write('%s ' % vert.index)
	objFile.write("]")
	objFile.write('\n"P" [')
	for vert in mesh.verts:
		objFile.write("%s %s %s " % (vert.co[0], vert.co[1], -vert.co[2]))
	objFile.write('] ')
	if mesh.faces[0].smooth:
		objFile.write(' "N" [')
		for vert in mesh.verts:
			objFile.write("%s %s %s " % (-vert.no[0], +vert.no[1], -vert.no[2]))
		objFile.write(']')
	if mesh.hasVertexColours() == 1:
		vertexcol = range(len(mesh.verts))
		objFile.write('\n"Cs" [')
		for face in mesh.faces:
			num = len(face.v)
			if num == 3 or num == 4:
				for vi in range(len(face.v)):
					vertexcol[face.v[vi].index] = face.col[vi]
		for vc in vertexcol:
			objFile.write('%s %s %s ' % (vc.r/256.0, vc.g/256.0, vc.b/256.0))
		objFile.write(']')
	
	if mesh.hasFaceUV() == 1:
		objFile.write('\n"st" [')
		for face in mesh.faces:
			num = len(face.v)
			if num == 3 or num == 4:
				for vi in range(len(face.v)):
					objFile.write('%s %s ' % (face.uv[vi][0], 1.0 - face.uv[vi][1]))
		objFile.write(']')	
	objFile.write('\n')
	objFile.close()

    
def writeSubdividedObj(ribPath, mesh):

	objFile = open(ribPath,'w')
	if mesh.hasFaceUV() == 1:
		objFile.write('Declare "st" "facevarying float[2]"\n')
	objFile.write('SubdivisionMesh "catmull-clark" [')
	for face in mesh.faces:
		num = len(face.v)
		objFile.write('%s '%(num))
	objFile.write(']\n[')
	for face in mesh.faces:
		for vert in face.v:
			objFile.write('%s ' % vert.index)
	objFile.write(']\n["interpolateboundary"] [0 0] [] []\n"P" [') 
	for vert in mesh.verts:
		objFile.write("%s %s %s " % (vert.co[0], vert.co[1], -vert.co[2]))
	objFile.write(']')

	if mesh.hasFaceUV() == 1:
		objFile.write('\n"st" [')
		for face in mesh.faces:
			num = len(face.v)
			if num == 3 or num == 4:
				for vi in range(len(face.v)):
					objFile.write('%s %s ' % (face.uv[vi][0], 1.0 - face.uv[vi][1]))
		objFile.write(']')
	if mesh.hasVertexColours() == 1:
		vertexcol = range(len(mesh.verts))
		objFile.write('\n"Cs" [')
		for face in mesh.faces:
			num = len(face.v)
			if num == 3 or num == 4:
				for vi in range(len(face.v)):
					vertexcol[face.v[vi].index] = face.col[vi]
		for vc in vertexcol:
			objFile.write('%s %s %s ' % (vc.r/256.0, vc.g/256.0, vc.b/256.0))
		objFile.write(']')
	objFile.write('\n')


def writeHairs(ribRepository):

    global rootColor,tipColor,hairDiameter,preview,hairsClass
    hDiameter = hairsClass.hairDiameter*random.uniform(0.5,1)    
    for hSet in hairsClass.hairStyle:        
        hairName = "%s/%s.rib"%(ribRepository,hSet.name)
        
        hairFile = open(hairName,'w')        
        hairFile.write('\t\tDeclare "rootcolor" "color"\n')
        hairFile.write('\t\tDeclare "tipcolor" "color"\n')
        hairFile.write('\t\tSurface "hair" "rootcolor" [%s %s %s] "tipcolor" [%s %s %s]'%(rootColor.val[0],\
                    rootColor.val[1],rootColor.val[2],\
                    tipColor.val[0],tipColor.val[1],tipColor.val[2]))
        hairFile.write('\t\tBasis "b-spline" 1 "b-spline" 1  ')
        hairFile.write('Curves "cubic" [')    
        for hair in hSet.hairs:
            hairFile.write('%i ' % len(hair.controlPoints))
        hairFile.write('] "nonperiodic" "P" [')
        for hair in hSet.hairs:
            for cP in hair.controlPoints:
                hairFile.write("%s %s %s " % (cP[0],cP[1],cP[2]))
        hairFile.write(']  "constantwidth" [%s]' % (hDiameter))
        hairFile.close()


def writeLamps(ribfile):
    ribfile.write('\tLightSource "ambientlight" 998 "intensity" [1] "color lightcolor" [1 1 1]')
    numLamp = 0
    for obj in Blender.Object.Get():
        if obj.getType() == "Lamp":
            lamp = obj.getData()
            intensity = lamp.getEnergy()
            numLamp += 1
            (locX,locY,locZ,rotX,rotY,rotZ,sizeX,sizeY,sizeZ) = convertCoords(obj)
            ribfile.write('\tLightSource "pointlight" %s "from" [%s %s %s] "intensity" %s  "lightcolor" [%s %s %s] \n' %(numLamp,locX, locY, locZ, intensity, lamp.col[0], lamp.col[1], lamp.col[2]))


def writeHuman(ribRepository):    

    global humanMesh
    meshData = humanMesh.getData()
    ribPath = "%s/base.obj.rib"%(ribRepository)
    writePolyObj(ribPath, meshData)
    
def writeFooter(ribfile):
    ribfile.write("\tAttributeBegin\n")
    ribfile.write("\t\tRotate -90 1 0 0\n")
    ribfile.write("\t\tReadArchive \"ribObjs/base.obj.rib\"\n")
    ribfile.write("\tAttributeEnd\n")
    ribfile.write("WorldEnd\n")

    
def writeBody(ribfile, ribRepository):
    global nHairs,subsurf,alpha
    print "Calling create objects"
    hairCounter = 0
    for obj in Blender.Object.Get():
        data = obj.getData()
        name = obj.getName()
        if type(data) == Types.CurveType:
            for curnurb in data:
                ribObj = "%s/%s.rib"%(ribRepository,name)
                print "RIBOBJ",ribObj
                (locX,locY,locZ,rotX,rotY,rotZ,sizeX,sizeY,sizeZ) = convertCoords(obj)
                ribfile.write('\tAttributeBegin\n')
                ribfile.write("\t\tTranslate %s %s %s\n" %(locX, locY, locZ))
                ribfile.write("\t\tRotate %s 0 0 1\n" %(rotZ))
                ribfile.write("\t\tRotate %s 0 1 0\n" %(rotY))
                ribfile.write("\t\tRotate %s 1 0 0\n" %(rotX))
                ribfile.write("\t\tScale %s %s %s\n" %(sizeX,sizeY,sizeZ))                
                ribfile.write('\t\tReadArchive "%s"\n' %(ribObj))
                ribfile.write('\tAttributeEnd\n')
                hairsClass.addHairGuide(curnurb, name)
                hairCounter += 1
   
    print "Exported ",nHairs.val * hairCounter, " hairs"




def saveRib(fName):
    engine = "aqsis"

    #d0 is [path,filename]
    #d1 is [name,extension]

    d0 = os.path.split(fName)
    d1 = os.path.splitext(d0[1])

    imageName = d1[0]+'.tif'
    fName = d1[0]+'.rib'

    print "Saved rib in ",  fName
    print "Saved image in ", imageName
    objectsDirectory = 'ribObjs'

    if not os.path.isdir(objectsDirectory):
        os.mkdir(objectsDirectory)

    theFile = open(fName,'w')
    
    writeHuman(objectsDirectory)
    writeHeader(theFile,imageName)    
    writeLamps(theFile)
    writeBody(theFile,objectsDirectory)
    hairsClass.generateHairStyle()
    writeFooter(theFile) 
    writeHairs(objectsDirectory)  
    theFile.close()
    print fName

    command = '%s %s'%('cd', mainPath) #To avoid spaces in path problem
    subprocess.Popen(command, shell=True) #We move into current dir

    if engine == "aqsis":
        subprocess.Popen("aqsl hair.sl -o hair.slx", shell=True)
        command = '%s %s'%('aqsis', fName)
    if engine == "pixie":
        subprocess.Popen("sdrc hair.sl -o hair.sdr", shell=True)
        command = '%s %s'%('rndr', fName)
    subprocess.Popen(command, shell=True)

def saveHairsFile(path):
    hairsClass.saveHairs(path)

def loadHairsFile(path):
    hairsClass.loadHairs(path)
###############################INTERFACE#####################################
#############################################################################

def draw():
    global hairDiameter,alpha
    global nHairs,randomFact
    global percOfRebels,tuftSize,subsurf
    global samples,clumptype,preview
    global rootColor,tipColor


    glClearColor(0.5, 0.5, 0.5, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    buttonY = 10

    Button("Exit", 1, 210, buttonY, 50, 20)
    Button("Rendering", 2, 10, buttonY, 200, 20)

    clumptype = Slider("Clumpiness: ", 3, 10, buttonY+20, 250, 18, clumptype.val, 0.0, 1.0, 1)
    hairDiameter = Slider("Hair diameter: ", 0, 10, buttonY+40, 250, 20, hairDiameter.val, 0, 0.05, 0)
    percOfRebels= Slider("% of unkempt: ", 3, 10, buttonY+60, 250, 18, percOfRebels.val, 1, 100, 0)
    randomFact= Slider("Unkempt dist: ", 3, 10, buttonY+80, 250, 18, randomFact.val, 0, 1, 0)
    nHairs= Slider("Number of hairs: ", 3, 10, buttonY+100, 250, 18, nHairs.val, 1, 1000, 0)
    tuftSize= Slider("Tuft area: ", 3, 10, buttonY+120, 250, 18, tuftSize.val, 0.0, 0.5, 0)
    rootColor = ColorPicker(3, 10, buttonY+140, 125, 20, rootColor.val,"Color of root")
    tipColor = ColorPicker(3, 135, buttonY+140, 125, 20, tipColor.val,"Color of tip")
    Button("Save", 4, 10, buttonY+200, 100, 20)
    Button("Load", 5, 110, buttonY+200, 100, 20)

    glColor3f(1, 1, 1)
    glRasterPos2i(10, buttonY+180)
    Text("makeHair 1.0 beta" )

def event(evt, val):
    if (evt== QKEY and not val): Exit()

def bevent(evt):
    global tuftSize, clumptype
    global nHairs, percOfRebels, randomFact

    if   (evt== 1): Exit()

    elif (evt== 2):
        saveRib("hair-test.rib")

    elif (evt== 3):
        hairsClass.tuftSize = tuftSize.val
        hairsClass.numberOfHairs = nHairs.val
        hairsClass.percOfRebels = percOfRebels.val
        hairsClass.clumptype = clumptype.val
        hairsClass.randomFact = randomFact.val
        hairsClass.hairDiameter = hairDiameter.val

    elif (evt== 4):
        Window.FileSelector (saveHairsFile, "Save hair data")
    elif (evt== 5):
        Window.FileSelector (loadHairsFile, "Load hair data")

    Window.RedrawAll()

Register(draw, event, bevent)
