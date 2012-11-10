"""
===========================  ===============================================================
Project Name:                **MakeHuman**
Product Home Page:           http://www.makehuman.org/
Google Home Page:            http://code.google.com/p/makehuman/
Authors:                     
Copyright(c):                MakeHuman Team 2001-2011
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://sites.google.com/site/makehumandocs/developers-guide
===========================  ===============================================================
"""



import Blender
import string, os, sys, math
import random
mainPath = Blender.sys.dirname(Blender.Get('filename'))
print "MAINPATH = ",mainPath 
sys.path.append(mainPath)
from Blender.Draw import *
from Blender.BGL import *
from Blender import Scene, Types, Window, Group, Curve, Mesh, Object
from Blender.Scene import Render
from collision import collision, world2Local, local2World
import simpleoctree, subprocess, hairgenerator
mhcore = os.path.split(mainPath)[0]
mhcore = os.path.split(mhcore)[0]
mhcore = os.path.join(mhcore,"mh_core")
print "mh_core Path = ", mhcore
sys.path.append(mhcore)
from aljabr import *

humanMesh = Blender.Object.Get("Base")

hairsClass = hairgenerator.Hairgenerator()

hairDiameterClump = Create(hairsClass.hairDiameterClump)
hairDiameterMultiStrand = Create(hairsClass.hairDiameterMultiStrand)

numberOfHairsClump= Create(hairsClass.numberOfHairsClump)
numberOfHairsMultiStrand= Create(hairsClass.numberOfHairsMultiStrand)

randomFactClump= Create(hairsClass.randomFactClump)
randomFactMultiStrand= Create(hairsClass.randomFactMultiStrand)

sizeClump= Create(hairsClass.sizeClump)
sizeMultiStrand= Create(hairsClass.sizeMultiStrand)

rootColor= Create(hairsClass.rootColor[0],hairsClass.rootColor[1],hairsClass.rootColor[2])
tipColor= Create(hairsClass.tipColor[0],hairsClass.tipColor[1],hairsClass.tipColor[2])

randomPercentage = Create(hairsClass.randomPercentage)
blendDistance = Create(hairsClass.blendDistance)
isPreview = Create(1)
isCollision = Create(0)
tipMagnet = Create(hairsClass.tipMagnet)

noCPoints = Create(hairsClass.noCPoints)
noGuides = Create(hairsClass.noGuides)
gLength = Create(hairsClass.gLength)
gFactor = Create(hairsClass.gFactor)

compileComm = "aqsl shaders/hair.sl -o shaders/hair.slx"
subprocess.Popen(compileComm, shell=True)

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

def drawGuidePair(scn,curve1,curve2,name="guides"):
    cu1 = Curve.New()
    cu1.appendNurb([curve1[0][0],curve1[0][1],curve1[0][2],1]) #last variable is the weight of the bezier
    cu2 = Curve.New()
    cu2.appendNurb([curve2[0][0],curve2[0][1],curve2[0][2],1]) #last variable is the weight of the bezier
    #print "length of curve1, curve2): ", len(curve1), len(curve2)
    for i in range(1, len(curve1)):
        cu1[0].append([curve1[i][0],curve1[i][1],curve1[i][2],1])
        cu2[0].append([curve2[i][0],curve2[i][1],curve2[i][2],1])
    #ob = Object.New(name) #make curve object
    #ob.link(cu) #link curve data with this object
    #scn.link(ob) # link object into scene
    obj1 = scn.objects.new(cu1)
    obj2 = scn.objects.new(cu2)
    grp= Group.New()
    grp.objects.link(obj1)
    grp.objects.link(obj2)
    #Blender.Redraw()  #its better to do this after all curves are drawn!

def drawLine(point1,point2,name="Line"):
    coords=[point1, point2]  
    faces= [[0,1]]
    me = Mesh.New()         # create a new mesh
    me.verts.extend(coords)          # add vertices to mesh
    me.faces.extend(faces)           # add faces to the mesh (also adds edges)
    scn = Scene.GetCurrent() #get current scene
    scn.objects.new(me,name)
    #Blender.Redraw() #it´s better to do this after all lines are drawn!
    
def writeHeader(ribfile,imgFile):

    ribfile.write('Option "searchpath" "shader" "shaders:&"')

    display = Scene.GetCurrent()
    context = display.getRenderingContext()
    yResolution = context.imageSizeY()
    xResolution = context.imageSizeX()
    if xResolution >= yResolution:
        factor = yResolution / float(xResolution)
    else:
        factor = xResolution / float(yResolution)

    scene = Blender.Scene.GetCurrent()
    camobj = scene.objects.camera
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
        verticesIdx = []
        for vert in face.v:
            verticesIdx.append(vert)
        verticesIdx.reverse()
        if num == 3 or num == 4:
            for vert in verticesIdx:
                objFile.write('%s ' % vert.index)
    objFile.write("]")
    objFile.write('\n"P" [')
    for vert in mesh.verts:
        objFile.write("%s %s %s " % (vert.co[0], vert.co[1], -vert.co[2]))
    objFile.write('] ')
    #if mesh.faces[0].smooth:
        #objFile.write(' "N" [')
        #for vert in mesh.verts:
            #objFile.write("%s %s %s " % (-vert.no[0], +vert.no[1], -vert.no[2]))
        #objFile.write(']')
    #if mesh.hasVertexColours() == 1:
        #vertexcol = range(len(mesh.verts))
        #objFile.write('\n"Cs" [')
        #for face in mesh.faces:
            #num = len(face.v)
            #if num == 3 or num == 4:
                #for vi in range(len(face.v)):
                    #vertexcol[face.v[vi].index] = face.col[vi]
        #for vc in vertexcol:
            #objFile.write('%s %s %s ' % (vc.r/256.0, vc.g/256.0, vc.b/256.0))
        #objFile.write(']')

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

    global rootColor,tipColor,hairDiameter,isPreview,isCollision,hairsClass,humanMesh
    totalNumberOfHairs = 0

    blenderCurves2MHData()
    #hairsClass.generateHairStyle1()
    hairsClass.generateHairStyle2(humanMesh,isCollision==1)
    
    if isPreview == 1:
        hDiameter = hairsClass.sizeClump
        hairName = "%s/hairpreview.rib"%(ribRepository)
        hairFile = open(hairName,'w')
        for group in hairsClass.guideGroups:            
            for guide in group.guides:                
                hairFile.write('Basis "b-spline" 1 "b-spline" 1\n')
                hairFile.write('Curves "cubic" [')
                hairFile.write('%i ' % len(guide.controlPoints))
                hairFile.write('] "nonperiodic" "P" [')
                for cP in guide.controlPoints:
                    hairFile.write("%s %s %s " % (cP[0],cP[1],-cP[2]))
                hairFile.write(']  "constantwidth" [%s]\n' % (hDiameter))
        hairFile.close()
                
    else:
                
        hairName = "%s/hairs.rib"%(ribRepository)
        hairFile = open(hairName,'w')
        for hSet in hairsClass.hairStyle:

            if "clump" in hSet.name:
                hDiameter = hairsClass.hairDiameterClump*random.uniform(0.5,1)
            else:
                hDiameter = hairsClass.hairDiameterMultiStrand*random.uniform(0.5,1)  
            



            #hairFile.write('\t\tSurface "matte" ')
            hairFile.write('Basis "b-spline" 1 "b-spline" 1\n')
            hairFile.write('Curves "cubic" [')
            for hair in hSet.hairs:
                totalNumberOfHairs += 1
                hairFile.write('%i ' % len(hair.controlPoints))
            hairFile.write('] "nonperiodic" "P" [')
            for hair in hSet.hairs:
                for cP in hair.controlPoints:
                    hairFile.write("%s %s %s " % (cP[0],cP[1],-cP[2]))
            hairFile.write(']  "constantwidth" [%s]\n' % (hDiameter))
        hairFile.close()
        print "TOTAL HAIRS WRITTEN: ",totalNumberOfHairs
        print "NUMBER OF TUFTS",len(hairsClass.hairStyle)



def writeLamps(ribfile):
    ribfile.write('\tLightSource "ambientlight" 998 "intensity" [.05] "color lightcolor" [1 1 1]')
    numLamp = 0
    for obj in Blender.Object.Get():
        if obj.getType() == "Lamp":
            lamp = obj.getData()
            intensity = lamp.getEnergy()*10
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
    #ribfile.write("\t\tRotate -90 1 0 0\n")
    ribfile.write("\t\tSurface \"matte\"\n")
    ribfile.write("\t\tReadArchive \"ribObjs/base.obj.rib\"\n")
    ribfile.write("\tAttributeEnd\n")
    ribfile.write("WorldEnd\n")


def writeBody(ribfile, ribRepository):
    global nHairs,alpha
    print "Calling create objects"
    ribfile.write('\t\tDeclare "rootcolor" "color"\n')
    ribfile.write('\t\tDeclare "tipcolor" "color"\n')
    ribfile.write('\t\tSurface "hair" "rootcolor" [%s %s %s] "tipcolor" [%s %s %s]'%(rootColor.val[0],\
                    rootColor.val[1],rootColor.val[2],\
                    tipColor.val[0],tipColor.val[1],tipColor.val[2]))
    if isPreview == 1:        
        ribObj = "%s/hairpreview.rib"%(ribRepository)
    else:
        ribObj = "%s/hairs.rib"%(ribRepository)       
    ribfile.write('\tAttributeBegin\n')
    ribfile.write('\t\tReadArchive "%s"\n' %(ribObj))
    ribfile.write('\tAttributeEnd\n')

def updateHumanVerts():
    hairsClass.humanVerts = []
    for v in humanMesh.getData().verts:
        #v1 = [v.co[0],v.co[1],-v.co[2]] #-1 +z to convert in renderman coord
        hairsClass.humanVerts.append(v)

def MHData2BlenderCurves():
    for group in hairsClass.guideGroups:
        for mhGuide in group.guides:
            blenderGuide = Blender.Object.Get(mhGuide.name).getData()
            for i in range(len(mhGuide.controlPoints)):
                mhCp = mhGuide.controlPoints[i]
                cPoint = [mhCp[0],mhCp[1],mhCp[2],1]
                blenderGuide.setControlPoint(0, i, cPoint)#we assume each curve has only one nurbs
                blenderGuide.update()

def blenderCurves2MHData():
    global hairsClass
    #Note the coords are saved in global (absolute) coords.
    hairsClass.resetHairs()
    hairCounter = 0
    groups = Group.Get()
    for group in groups:
        print "GROUP",group
        g = hairsClass.addGuideGroup(group.name)
        for obj in list(group.objects):
            data = obj.getData()
            name = obj.getName()
            if type(data) == Types.CurveType:
                matr = obj.getMatrix()
                controlPoints = []
                for curnurb in data:
                    for p in curnurb:
                        p1 = [p[0],p[1],p[2]]
                        worldP = local2World(p1,matr) #convert the point in absolute coords
                        p2 = [worldP[0],worldP[1],worldP[2]] #convert from Blender coord to Renderman coords
                        controlPoints.append(p2)
                    hairsClass.addHairGuide(controlPoints, name, g)
                    hairCounter += 1


def adjustGuides():
    """

    """
    global hairsClass
    updateHumanVerts()
    hairsClass.adjustGuides()
    MHData2BlenderCurves()
    Window.RedrawAll()



def saveRib(fName):
    global hairsClass

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
    #generateHairs()
    if not os.path.isdir(objectsDirectory):
        os.mkdir(objectsDirectory)
    theFile = open(fName,'w')
    writeHuman(objectsDirectory)
    writeHairs(objectsDirectory)
    writeHeader(theFile,imageName)
    writeLamps(theFile)
    writeBody(theFile,objectsDirectory)
    writeFooter(theFile)

    theFile.close()

    hairsClass.resetHairs()

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
    updateHumanVerts()
    blenderCurves2MHData()
    hairsClass.saveHairs(path)

def loadHairsFile(path):
    global tipMagnet,hairDiameterClump,hairDiameterMultiStrand
    global numberOfHairsClump,numberOfHairsMultiStrand,randomFactClump
    global randomFactMultiStrand,randomPercentage,sizeClump,sizeMultiStrand
    global blendDistance,sizeMultiStrand,rootColor,tipColor

    hairsClass.loadHairs(path)
    scn = Scene.GetCurrent()
    for group in hairsClass.guideGroups:
        grp= Group.New(group.name)
        for guide in group.guides:
            startP = guide.controlPoints[0]
            cu = Curve.New(guide.name)
            #Note: hairs are stored using renderman coords system, so
            #z is multiplied for -1 to conver renderman coords to Blender coord
            cu.appendNurb([startP[0],startP[1],startP[2],1])
            cu_nurb= cu[0]
            for cP in guide.controlPoints[1:]:
                cu_nurb.append([cP[0],cP[1],cP[2],1])
            ob = scn.objects.new(cu)
            grp.objects.link(ob)

    tipMagnet.val = hairsClass.tipMagnet
    hairDiameterClump.val = hairsClass.hairDiameterClump
    hairDiameterMultiStrand.val = hairsClass.hairDiameterMultiStrand
    numberOfHairsClump.val= hairsClass.numberOfHairsClump
    numberOfHairsMultiStrand.val= hairsClass.numberOfHairsMultiStrand
    randomFactClump.val= hairsClass.randomFactClump
    randomFactMultiStrand.val= hairsClass.randomFactMultiStrand
    randomPercentage.val= hairsClass.randomPercentage
    sizeClump.val= hairsClass.sizeClump
    sizeMultiStrand.val= hairsClass.sizeMultiStrand
    rootColor.val = (hairsClass.rootColor[0],hairsClass.rootColor[1],hairsClass.rootColor[2])
    tipColor.val = (hairsClass.tipColor[0],hairsClass.tipColor[1],hairsClass.tipColor[2])
    blendDistance.val= hairsClass.blendDistance
    Window.RedrawAll()

def randomizeCurves(xFactor=0.05,yFactor=0.05,zFactor=0.05):

    groups = Group.Get()
    for group in groups:       
        
        for obj in list(group.objects):
            data = obj.getData()
            name = obj.getName()
            if type(data) == Types.CurveType:                
                for curnurb in data:
                    
                    for i in range(len(curnurb)):
                        p = curnurb[i]
                        newX = p[0]+ xFactor*random.uniform(-1,1)  
                        newY = p[1]+ yFactor*random.uniform(-1,1) 
                        newZ = p[2]+ zFactor*random.uniform(-1,1)                  
                        newP = [newX,newY,newZ,p[3]]
                        
                        data.setControlPoint(0, i, newP)#we assume each curve has only one nurbs
                data.update()
                        
        
    Window.RedrawAll()
                        
def printVertsIndices():
    data = Blender.Object.GetSelected()[0].getData()
    wem = Window.EditMode()
    Window.EditMode(0)
    
    if type(data) == Types.CurveType:                
        for curnurb in data:
            firstCP = curnurb[0]
            print firstCP
                        
    #for v in data.verts:
    #    if v.sel == 1:
    #        print "Index ", v.index
    Window.EditMode(wem)
    Window.RedrawAll()


def gravitize(curve,start,mat,gFactor):
    #TODO use mat to convert local to world!
    length  = vdist(curve[start],curve[len(curve)-1]) #length of hair!
    X = math.pow(math.pow(length,2.0)-math.pow(curve[start][1]-curve[len(curve)-1][1],2.0),0.5)
    X= X*math.pow(2.0,gFactor)
    c = math.pow(2.0,-8.0+gFactor)
    p0  = curve[start][:]
    p1 = curve[len(curve)-1][:]
    interval = length/(len(curve)-start-1)
    for i in range(start+1, len(curve)):
        x=math.pow(interval*(i-start)/(4*c),1.0/3.0)
        curve[i] = in2pts(p0,p1,x/X) 
        curve[i][1] = curve[i][1] - c*math.pow(x,4)

def clamp(curve1,curve2):
    l = min(len(curve1),len(curve2))
    div = 0.5/(l-1)
    for i in range(1,l-1):
        p1 = curve1[i][:]
        p2 = curve2[i][:]
        curve1[i] = in2pts(p1,p2,div*i)
        curve2[i] = in2pts(p2,p1,div*i)
    curve1[l-1] = in2pts(p2,p1,0.5)
    curve2[l-1] = curve1[l-1][:]
    
###############################INTERFACE#####################################

def draw():
    global hairDiameterClump,hairDiameterMultiStrand,alpha
    global numberOfHairsClump,numberOfHairsMultiStrand,randomFactClump,randomFactMultiStrand
    global tipMagnet,sizeMultiStrand,sizeClump,blendDistance
    global randomPercentage, rootColor,tipColor,isPreview, isCollision
    global noGuides, noCPoints, gLength, gFactor
    
    glClearColor(0.5, 0.5, 0.5, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    buttonY = 200
    
    Button("Exit", 1, 210, buttonY, 100, 20) #1
    Button("Render", 2, 10, buttonY, 100, 20) #2
    Button("Collide guides", 8, 110, buttonY, 100, 20) #8
    Button("Save", 4, 10, buttonY+20, 150, 20) #4
    Button("Load", 5, 160, buttonY+20, 150, 20) #5
    isPreview = Toggle("Preview", 6, 10, buttonY+40, 150, 20, isPreview.val, "Rendering in preview mode") #6
    #isCollision = Toggle("Collision for all strands", 7, 160, buttonY+40, 150, 20, isCollision.val, "Implement collision detection") #7

    #tipMagnet= Slider("Clump tipMagnet: ", 3, 10, buttonY+80, 300, 18, tipMagnet.val, 0, 1, 0,"How much tip of guide attract generated hairs")
    #randomFactClump= Slider("Clump Random: ", 3, 10, buttonY+100, 300, 18, randomFactClump.val, 0, 1, 0,"Random factor in clump hairs generation")
    #numberOfHairsClump= Slider("Clump hairs num.: ", 3, 10, buttonY+120, 300, 18, numberOfHairsClump.val, 1, 100, 0, "Number of generated hair for each guide. Note that value of x mean x*x hairs")
    #sizeClump= Slider("Clump size: ", 3, 10, buttonY+140, 300, 18, sizeClump.val, 0.0, 0.5, 0,"Size of clump volume")
    #hairDiameterMultiStrand = Slider("Clump hair diam.: ", 0, 10, buttonY+160, 300, 20, hairDiameterMultiStrand.val, 0, 0.05, 0,"Diameter of hairs used in strand interpolation")

    blendDistance= Slider("Strand blending dist.: ", 3, 10, buttonY+60, 300, 18, blendDistance.val, 0, 2, 0)
    randomFactMultiStrand= Slider("Strand Random: ", 3, 10, buttonY+80, 300, 18, randomFactMultiStrand.val, 0, 1, 0)
    numberOfHairsMultiStrand= Slider("Strand hairs num. ", 3, 10, buttonY+100, 300, 18, numberOfHairsMultiStrand.val, 1, 1000, 0)
    sizeMultiStrand= Slider("Strand volume: ", 3, 10, buttonY+120, 300, 18, sizeMultiStrand.val, 0.0, 0.5, 0)
    hairDiameterClump = Slider("Strand hair diam.: ", 0, 10, buttonY+140, 300, 20, hairDiameterClump.val, 0, 0.05, 0,"Diameter of hairs used in clump interpolation")

    randomPercentage= Slider("Random perc.: ", 3, 10, buttonY+160, 300, 18, randomPercentage.val, 0.0, 1.0, 0)
    rootColor = ColorPicker(3, 10, buttonY+180, 150, 20, rootColor.val,"Color of root")
    tipColor = ColorPicker(3, 160, buttonY+180, 150, 20, tipColor.val,"Color of tip")
    
    buttonY = buttonY-100
    Button("Guides along normal", 9, 10, buttonY, 150, 20) #9
    Button("Clamp Guide Pairs", 11, 160, buttonY, 150, 20) #11
    noGuides= Slider("No. Guide-pairs: ", 3, 10, buttonY+20, 300, 18, noGuides.val, 1, 260, 0, "Number of guide-pairs to draw along normal of head")
    gLength= Slider("Length of guides: ", 3, 10, buttonY+40, 300, 18, gLength.val, 0.0, 7.0, 0, "Length of each guides drawn along normal of head")
    noCPoints= Slider("Controlpoints: ", 3, 10, buttonY+60, 300, 18, noCPoints.val, 2, 20, 0, "Number of control-points for each guide")
    
    buttonY = buttonY - 60
    Button("Gravitize Selected", 10, 10, buttonY, 150, 20) #10
    gFactor= Slider("Gravity Factor: ", 3, 10, buttonY+20, 300, 18, gFactor.val, 0.0, 2.0, 0, "An exponential gravity factor")

    glColor3f(1, 1, 1)
    glRasterPos2i(10, buttonY+380)
    Text("makeHair 1.0" )

def event(evt, val):
    if (evt== QKEY and not val): Exit()

    if (evt== TKEY and not val):
        randomizeCurves()
        #MHData2BlenderCurves()
        
    elif evt == IKEY:
        printVertsIndices()       

        adjustGuides()
        
    
    #Window.RedrawAll()

def bevent(evt):
    global tipMagnet,hairDiameterClump,hairDiameterMultiStrand
    global numberOfHairsClump,numberOfHairsMultiStrand,randomFactClump
    global randomFactMultiStrand,randomPercentage,sizeClump,sizeMultiStrand
    global blendDistance,sizeMultiStrand,rootCOlor,tipCOlor, humanMesh
    global noGuides, noCPoints, gLength, gFactor

    if   (evt== 1): Exit()

    elif (evt== 2):
        saveRib("hair-test.rib")

    elif (evt== 3):

        hairsClass.tipMagnet = tipMagnet.val
        hairsClass.hairDiameterClump = hairDiameterClump.val
        hairsClass.hairDiameterMultiStrand = hairDiameterMultiStrand.val
        hairsClass.numberOfHairsClump= numberOfHairsClump.val
        hairsClass.numberOfHairsMultiStrand= numberOfHairsMultiStrand.val
        hairsClass.randomFactClump= randomFactClump.val
        hairsClass.randomFactMultiStrand= randomFactMultiStrand.val
        hairsClass.randomPercentage= randomPercentage.val
        hairsClass.sizeClump= sizeClump.val
        hairsClass.sizeMultiStrand= sizeMultiStrand.val
        hairsClass.blendDistance= blendDistance.val
        hairsClass.tipColor= tipColor.val
        hairsClass.rootColor= rootColor.val
        hairsClass.noGuides = noGuides.val
        hairsClass.noCPoints = noCPoints.val
        hairsClass.gLength = gLength.val
        hairsClass.gFactor = gFactor.val

    elif (evt== 4):
        Window.FileSelector (saveHairsFile, "Save hair data")
    elif (evt== 5):
        Window.FileSelector (loadHairsFile, "Load hair data")
    elif (evt==8):
        scn = Scene.GetCurrent() #get current scene
        mesh = humanMesh.getData()
        mat = humanMesh.getMatrix()
        verts=[]
        for v in mesh.verts: #reduces vertices for simplifying octree, improves performance
            if v.co[0]<=2 and v.co[0]>=-2 and v.co[1]<=8.6 and v.co[1]>=3.6: #2D bounding box between head and chest
                verts.append(local2World(v.co,mat)) #localspace to worldspace
        octree = simpleoctree.SimpleOctree(verts,0.09)
        for obj in scn.objects:
            if obj.type == "Curve":
                data = obj.getData()
                if data[0].isNurb():
                    mat = obj.getMatrix()
                    curve=[]
                    for p in data[0]:
                        curve.append(local2World([p[0],p[1],p[2]],mat))
                    collision(curve,humanMesh,octree.minsize,9,True) #collision will after 9th controlPoint!!!
                    N=data.getNumPoints(0)
                    if N<len(curve):
                        #Window.SetCursorPos(curve[len(curve)-1])
                        for i in range(0,len(curve)):
                            temp = world2Local(curve[i],mat)
                            if i < N: 
                                data.setControlPoint(0,i,[temp[0],temp[1],temp[2],1])
                            else: 
                                data.appendPoint(0,[temp[0],temp[1],temp[2],1])
                        #data[0].recalc()
                        data.update()
        Blender.Redraw()
    elif (evt==9):
        #noCPoints=15
        mesh = humanMesh.getData()
        #scalp = 269 vertices!
        vertIndices = mesh.getVertsFromGroup("part_head-back-skull")
        vertIndices.extend(mesh.getVertsFromGroup("part_head-upper-skull"))
        vertIndices.extend(mesh.getVertsFromGroup("part_l-head-temple"))
        vertIndices.extend(mesh.getVertsFromGroup("part_r-head-temple"))
        scalpVerts = len(vertIndices) #Collects all vertices that are part of the head where hair grows!
        interval = int(scalpVerts/noGuides.val) #variable used to randomly distribute scalp-vertices
        cPInterval = gLength.val/float(noCPoints.val) #Length between c.P. for hairs being generated
        #print "cPInterval is : ", cPInterval
        scn = Scene.GetCurrent() #get current scene
        for i in range(0,noGuides.val):
            if i==noGuides.val-1:
                r= random.randint(interval*i,scalpVerts-1)
            else:    
                r = random.randint(interval*i,interval*(i+1))
            v= mesh.verts[vertIndices[r]].co
            normal = mesh.verts[vertIndices[r]].no
            point2 = vadd(v,vmul(normal,gLength.val))
            curve=[vadd(v,vmul(normal,-0.5))]
            w,normal2,point22,curve2 =[],[],[],[]
            for j in range(0,scalpVerts):
                w=mesh.verts[vertIndices[j]].co
                dist = vdist(v,w)
                if dist>=0.05 and dist<=0.3:
                    normal2=mesh.verts[vertIndices[j]].no
                    point22 = vadd(w,vmul(normal2,gLength.val))
                    curve2=[vadd(w,vmul(normal2,-0.5))]
                    break
            curve.append(vadd(v,vmul(normal,-0.2)))
            curve2.append(vadd(w,vmul(normal2,-0.2)))
            for j in range(1,noCPoints.val-1):
                curve.append(vadd(v,vmul(normal,cPInterval*j)))
                curve2.append(vadd(w,vmul(normal2,cPInterval*j)))
            curve.append(point2)
            curve2.append(point22)
            drawGuidePair(scn,curve[:],curve2[:])
        #r= random.randint(interval*(noGuides.val-1),scalpVerts-1)
        Blender.Redraw()
    elif (evt==10):
        selected = Blender.Object.GetSelected()
        start=1 #starting c.P. to use gravity!
        for obj in selected:
            if obj.type == "Curve": #we use virtual Young's modulus
                data= obj.getData()
                if data[0].isNurb():
                    mat = obj.getMatrix()
                    curve=[]
                    for p in data[0]:
                        curve.append(local2World([p[0],p[1],p[2]],mat))
                    gravitize(curve,start,mat,gFactor.val)
                    for i in range(start,len(curve)):
                        temp = world2Local(curve[i],mat)
                        data.setControlPoint(0,i,[temp[0],temp[1],temp[2],1])
                    data.update()
        Blender.Redraw()
    elif (evt==11):
        groups = Group.Get()
        for grp in groups:
            obj1, obj2 = grp.objects[0], grp.objects[1]
            if obj1.type == "Curve" and obj2.type == "Curve":
                data1, data2 = obj1.getData(), obj2.getData()
                if data1[0].isNurb() and data2[0].isNurb():
                    mat1, mat2 = obj1.getMatrix(), obj2.getMatrix()
                    curve1,curve2=[],[]
                    l1,l2 = list(data1[0]), list(data2[0])
                    for i in range(0,len(l1)):
                        curve1.append(local2World([l1[i][0],l1[i][1],l1[i][2]],mat1))
                        curve2.append(local2World([l2[i][0],l2[i][1],l2[i][2]],mat2))
                    clamp(curve1,curve2)
                    for i in range(0, len(curve1)):
                        temp = world2Local(curve1[i],mat1)
                        data1.setControlPoint(0,i,[temp[0],temp[1],temp[2],1])
                        temp = world2Local(curve2[i],mat2)
                        data2.setControlPoint(0,i,[temp[0],temp[1],temp[2],1])
                    data1.update()
                    data2.update()
        Blender.Redraw()

Register(draw, event, bevent)

