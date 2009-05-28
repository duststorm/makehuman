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

from Blender.Draw import *
from Blender.BGL import *
from Blender import Scene
from Blender import Types
from Blender.Scene import Render
from Blender import Window
import subprocess
import hairgenerator



hairDiameter = Create(0.006)


nHairs= Create(90)
randomFact= Create(0.0)
percOfRebels = Create(5)
clumptype = Create(1.0)
tuftSize= Create(0.10)
colors1= [Create(0.109), Create(0.037), Create(0.007)]
colors2= [Create(0.518), Create(0.325), Create(0.125)]


mainPath = Blender.sys.dirname(Blender.Get('filename'))
hairsClass = hairgenerator.hairgenerator()


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
    ribfile.write("Option \"searchpath\" \"shader\" \"data/shaders/renderman:&\"\n")
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





def writeHairs(tuft, fileObj):

    global colors1,colors2,hairDiameter,preview


    hDiameter = hairDiameter.val*random.uniform(0.5,1)

    objFile = file(fileObj,'w')
    objFile.write('\t\tDeclare "rootcolor" "color"\n')
    objFile.write('\t\tDeclare "tipcolor" "color"\n')
    objFile.write('\t\tSurface "hair" "rootcolor" [%s %s %s] "tipcolor" [%s %s %s]' % (colors1[0].val,colors1[1].val,colors1[2].val,colors2[0].val,colors2[1].val,colors2[2].val))
    objFile.write('\t\tBasis "b-spline" 1 "b-spline" 1  ')
    objFile.write('Curves "cubic" [')
    for hair in tuft:
        objFile.write('%i ' % len(hair))
    objFile.write('] "nonperiodic" "P" [')
    for hair in tuft:
        for vert in hair:
            objFile.write("%s %s %s " % (vert[0],vert[1],vert[2]))
    objFile.write(']  "constantwidth" [%s]' % (hDiameter))
    objFile.close()


def writeLamps(ribfile):
    numLamp = 0
    for obj in Blender.Object.Get():

        if obj.getType() == "Lamp":
            lamp = obj.getData()
            intensity = lamp.getEnergy()
            numLamp += 1
            (locX,locY,locZ,rotX,rotY,rotZ,sizeX,sizeY,sizeZ) = convertCoords(obj)
            ribfile.write('\tLightSource "pointlight" %s "from" [%s %s %s] "intensity" %s  "lightcolor" [%s %s %s] \n' %(numLamp,locX, locY, locZ, intensity, lamp.col[0], lamp.col[1], lamp.col[2]))


def createObjects(ribfile, ribRepository):
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

                #if (mesh.materials):
                        #try:
                            #material = Blender.Material.Get(mesh.materials[0].name)
                            #ribfile.write("\t\tColor [%s %s %s]\n" %(material.R, material.G, material.B))
                            #ribfile.write("\t\tOpacity [%s %s %s]\n" %(material.alpha, material.alpha, material.alpha))
                        #except:
                            #pass

                ribfile.write("\t\tTranslate %s %s %s\n" %(locX, locY, locZ))
                ribfile.write("\t\tRotate %s 0 0 1\n" %(rotZ))
                ribfile.write("\t\tRotate %s 0 1 0\n" %(rotY))
                ribfile.write("\t\tRotate %s 1 0 0\n" %(rotX))
                ribfile.write("\t\tScale %s %s %s\n" %(sizeX,sizeY,sizeZ))

                tuft = hairsClass.generateTuft(curnurb)
                writeHairs(tuft, ribObj)
                hairCounter += 1
                ribfile.write('\t\tReadArchive "%s"\n' %(ribObj))
                ribfile.write('\tAttributeEnd\n')

    ribfile.write("\tAttributeBegin\n")
    ribfile.write("\t\tRotate -90 1 0 0\n")
    ribfile.write("\t\tReadArchive \"ribObjs/base.obj.rib\"\n")
    ribfile.write("\tAttributeEnd\n")
    print "Exported ",nHairs.val * hairCounter, " hairs"




def saveRib(fName):
    engine = "pixie"

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

    theFile = file(fName,'w')
    writeHeader(theFile,imageName)
    ambientLight(theFile)
    writeLamps(theFile)
    createObjects(theFile,objectsDirectory)
    theFile.write("WorldEnd\n")
    theFile.close()
    print fName

    command = '%s %s'%('cd', mainPath) #To avoid spaces in path problem
    subprocess.Popen(command, shell=True) #We move into current dir

    if engine == "aqsis":
        subprocess.Popen("aqsl data/shaders/renderman/hair.sl -o data/shaders/renderman/hair.slx", shell=True)
        command = '%s %s'%('aqsis', fName)
    if engine == "pixie":
        subprocess.Popen("sdrc data/shaders/renderman/hair.sl -o data/shaders/renderman/hair.sdr", shell=True)
        command = '%s %s'%('rndr', fName)
    subprocess.Popen(command, shell=True)




###############################INTERFACE#####################################
#############################################################################

def draw():
    global hairDiameter,alpha
    global nHairs,randomFact
    global percOfRebels,tuftSize,subsurf
    global samples,clumptype,preview


    glClearColor(0.5, 0.5, 0.5, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    buttonY = 10

    Button("Exit", 1, 210, buttonY, 50, 20)
    Button("Rendering", 2, 10, buttonY, 200, 20)
    #samples= Slider("Samples: ", 3, 10, buttonY+40, 250, 18, samples.val, 2, 10, 1)



    clumptype = Slider("Clumpiness: ", 3, 10, buttonY+120, 250, 18, clumptype.val, 0.0, 1.0, 1)
    hairDiameter = Slider("Hair diamter: ", 0, 10, buttonY+140, 250, 20, hairDiameter.val, 0, 0.05, 0)
    percOfRebels= Slider("% of unkempt: ", 3, 10, buttonY+160, 250, 18, percOfRebels.val, 1, 100, 0)
    randomFact= Slider("Unkempt val: ", 3, 10, buttonY+180, 250, 18, randomFact.val, 0, 1, 0)
    nHairs= Slider("n Hairs: ", 3, 10, buttonY+200, 250, 18, nHairs.val, 1, 1000, 0)
    tuftSize= Slider("Dupl. Size: ", 3, 10, buttonY+220, 250, 18, tuftSize.val, 0.0, 0.5, 0)

    glColor3f(colors1[0].val,colors1[1].val,colors1[2].val)
    glRectf(220,buttonY+300,260,buttonY+240)

    glColor3f(colors2[0].val,colors2[1].val,colors2[2].val)
    glRectf(220,buttonY+380,260,buttonY+320)

    colors1[0]= Slider("R: ", 3, 10, buttonY+240, 200, 18, colors1[0].val, 0, 1, 1)
    colors1[1]= Slider("G: ", 3, 10, buttonY+260, 200, 18, colors1[1].val, 0, 1, 1)
    colors1[2]= Slider("B: ", 3, 10, buttonY+280, 200, 18, colors1[2].val, 0, 1, 1)

    glColor3f(1, 1, 1)
    glRasterPos2i(10, buttonY+305)
    Text("Root Color",'small' )

    colors2[0]= Slider("R: ", 3, 10, buttonY+320, 200, 18, colors2[0].val, 0, 1, 1)
    colors2[1]= Slider("G: ", 3, 10, buttonY+340, 200, 18, colors2[1].val, 0, 1, 1)
    colors2[2]= Slider("B: ", 3, 10, buttonY+360, 200, 18, colors2[2].val, 0, 1, 1)

    glColor3f(1, 1, 1)
    glRasterPos2i(10, buttonY+385)
    Text("Tip Color",'small' )

    glColor3f(1, 1, 1)
    glRasterPos2i(10, 420)
    Text("MAKEHUMAN hair tool alpha 002" )

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

    Window.RedrawAll()

Register(draw, event, bevent)
