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


This module contain the classes needed to load, save and generate (from guides)
makehuman hairs.
"""

import random
import math
import simpleoctree
import aljabr


class Hair:
    """
    Hair is just a sequence of control points, to be rendered as a
    spline.
    """
    def __init__(self):
        self.controlPoints = []

class HairGuide(Hair):
   """
   Hair guide is a special hair type. It's used as a parent hair to
   generate an hair set (tuft). On the contrary of the normal hair,
   hairguide has a name.
   """
   def __init__(self,name):
       Hair.__init__(self)
       self.name = name

class HairSet:
    """
    Hairset is basically a set of hair object. Usually they are randomly
    generated upon a hair guide.
    """
    def __init__(self,name):
        self.name = name
        self.hairs = []

class Hairgenerator:
    """
    Hair generator make a series of hair sets, one for each hairguide.
    The sum of all hair sets (think of it as tufts) is called hairstyle.
    """

    def __init__(self, humanMesh):

        self.hairStyle = []

        self.tipMagnet = 0.9
        self.clumptype = 1

        self.numberOfHairsClump = 10
        self.numberOfHairsMultiStrand = 90

        self.randomFactClump = 0.5
        self.randomFactMultiStrand = 0.5
        self.randomPercentage = 0.5

        self.hairDiameterClump = 0.006
        self.hairDiameterMultiStrand = 0.006

        self.sizeClump = 0.200
        self.sizeMultiStrand = 0.150
        self.blendDistance = 0.8


        self.tipColor = [0.518,0.325,0.125]
        self.rootColor = [0.109, 0.037, 0.007]
        self.guides = []
        self.version = "1.0 alpha 2"
        self.tags = []
        self.octree = simpleoctree.SimpleOctree(humanMesh.verts)

    def addHairGuide(self,curve, curveName):
        g = HairGuide(curveName)
        g.name = curveName
        for p in curve:
            g.controlPoints.append([p[0],p[1],p[2]])
        self.guides.append(g)

    def generateHairStyle1(self):
        for guide in self.guides:
            self.generateHairInterpolation1(guide)

    def generateHairStyle2(self):
        for guide in self.guides:
            samplePointIndex = int(len(guide.controlPoints)/2)
            p1 = guide.controlPoints[samplePointIndex]
            currentGuide = guide.name            
            guideToInterpolate = None
            for guide2 in self.guides:
                if guide2.name != currentGuide:
                    p2 = guide2.controlPoints[samplePointIndex]
                    dist = aljabr.vdist(p1,p2)                    
                    if dist < self.blendDistance:                        
                        guideToInterpolate = guide2
                        self.generateHairInterpolation2(guide,guideToInterpolate)


    def generateHairInterpolation1(self,guide):
        hairName = "clump%s"%(guide.name)
        hSet = HairSet(hairName)
        nVerts = len(guide.controlPoints)
        #headCentroid = [0.0,-0.570,7.318] #hardcoded...TODO
        interpFactor1 = 0
        incr = 1.0/(self.numberOfHairsClump)
        for n in range (self.numberOfHairsClump):
            interpFactor1 += incr
            vertsListToModify = []
            for c in guide.controlPoints:
                vertsListToModify.append([c[0],c[1],c[2]])#maybe useless
            interpFactor2 = 0
            for n2 in range (self.numberOfHairsClump):
                h = Hair()
                interpFactor2 += incr
                for i in range(nVerts):
                    if nVerts > 3:
                        clumpIndex = nVerts-2
                    else:
                        clumpIndex = nVerts-1

                    magnet = 1.0-(i/float(clumpIndex))*self.tipMagnet
                    if random.random() < self.randomPercentage:                        
                        xRand = self.sizeClump*random.random()*self.randomFactClump*magnet
                        yRand = self.sizeClump*random.random()*self.randomFactClump*magnet
                        zRand = self.sizeClump*random.random()*self.randomFactClump*magnet
                        randomVect = [xRand,yRand,zRand]
                    else:                        
                        randomVect = [0,0,0]

                    offset1 =  self.sizeClump*interpFactor1*magnet
                    offset2 =  self.sizeClump*interpFactor2*magnet
                    if  i >= clumpIndex:
                        vert0 = vertsListToModify[i-1]
                        vert1 = vertsListToModify[i]
                        vert2 = vertsListToModify[nVerts-1]
                    elif i < 1:
                        vert0 = vertsListToModify[0]
                        vert1 = vertsListToModify[1]
                        vert2 = vertsListToModify[2]
                    else:
                        vert0 = vertsListToModify[i-1]
                        vert1 = vertsListToModify[i]
                        vert2 = vertsListToModify[i+1]

                    vector1 = aljabr.vsub(vert2,vert1)
                    vector2 = aljabr.vsub(vert1,vert0)
                    vector3 = aljabr.vnorm(aljabr.vcross(vector1,vector2))
                    vector4 = aljabr.vnorm(aljabr.vcross(vector1,vector3))

                    #Vector3 and vector4 are perpendicular between them,
                    #and both are perpendicular to line vert1-vert2. This happen
                    #because vector3 is the cross product of vector1 and vector2
                    #so it's perpendicular to them, and vector4 is the cross product
                    #of vector1 and vector3, so it's perpendicular to them.
                    #So using these 2 vector we build a prims vector3*vector4*guideLenght.

                    offsetVector1 = aljabr.vmul(vector3,offset1)
                    offsetVector2 = aljabr.vmul(vector4,offset2)
                    offsetVector3 = aljabr.vadd(offsetVector1,offsetVector2)
                    offsetVector = aljabr.vadd(offsetVector3,randomVect)

                    h.controlPoints.append([vert1[0]+offsetVector[0],\
                                            vert1[1]+offsetVector[1],\
                                            -vert1[2]+offsetVector[2]])#I should to do in Blender coords

                hSet.hairs.append(h)


        self.hairStyle.append(hSet)


    def generateHairInterpolation2(self,guide1,guide2):
        hairName = "strand%s-%s"%(guide1.name,guide2.name)
        hSet = HairSet(hairName)
        print "INT.",hairName
        nVerts = min([len(guide1.controlPoints),len(guide2.controlPoints)])
        headCentroid = [0.0,-0.570,7.318] #hardcoded...TODO
        interpFactor = 0
        vertsListToModify1 = []
        vertsListToModify2 = []
        for c in guide1.controlPoints:
            vertsListToModify1.append([c[0],c[1],c[2]]) #TODOmaybe this is useless
        for c in guide2.controlPoints:
            vertsListToModify2.append([c[0],c[1],c[2]]) #TODOmaybe this is useless

        for n in range (self.numberOfHairsMultiStrand):
            h = Hair()

            #randomHairs = random.uniform(0.0,self.randomFactMultiStrand)*random.uniform(0.0,self.sizeMultiStrand)
            
            
            
            interpFactor += 1.0/self.numberOfHairsMultiStrand
            for i in range(nVerts):
                if random.random() < self.randomPercentage: 
                    xRand = self.sizeMultiStrand*random.random()*self.randomFactMultiStrand
                    yRand = self.sizeMultiStrand*random.random()*self.randomFactMultiStrand
                    zRand = self.sizeMultiStrand*random.random()*self.randomFactMultiStrand
                    randomVect = [xRand,yRand,zRand]
                else:
                    randomVect = [0,0,0]
                
                vert1 = vertsListToModify1[i]
                vert2 = vertsListToModify2[i]
                newVert = aljabr.vadd(aljabr.vmul(vert1,(1-interpFactor)),aljabr.vmul(vert2,interpFactor))
                h.controlPoints.append([newVert[0]+randomVect[0],\
                                                newVert[1]+randomVect[1],\
                                                -newVert[2]+randomVect[2]]) #I should to do in Blender coords

            hSet.hairs.append(h)

        self.hairStyle.append(hSet)











    def saveHairs(self,path):
        """
        Save a file containing the info needed to build the hairstyle,
        strating from the hair guides and using some parameters.
        """
        try:
            fileDescriptor = open(path, "w")
        except:
            print "Impossible to save %s"%(path)
            return

        fileDescriptor.write("written by makehair 1.0\n")
        fileDescriptor.write("version %s\n"%(self.version))
        fileDescriptor.write("tags ")
        for tag in self.tags:
            fileDescriptor.write("%s "%(tag))
        fileDescriptor.write("\n")
        fileDescriptor.write("numberofhairs %i\n"%(self.numberOfHairs))
        fileDescriptor.write("tipMagnet %f\n"%(self.tipMagnet))
        fileDescriptor.write("clumptype %f\n"%(self.clumptype))
        fileDescriptor.write("tuftsize %f\n"%(self.tuftSize))
        fileDescriptor.write("randomfact %f\n"%(self.randomFact))
        fileDescriptor.write("hairdiameter %f\n"%(self.hairDiameter))
        fileDescriptor.write("tipcolor %f %f %f\n"%(self.tipColor[0],self.tipColor[1],self.tipColor[2]))
        fileDescriptor.write("rootcolor %f %f %f\n"%(self.rootColor[0],self.rootColor[1],self.rootColor[2]))

        for guide in self.guides:
            fileDescriptor.write("%s "%(guide.name))
            for cP in guide.controlPoints:
                fileDescriptor.write("%f %f %f "%(cP[0],cP[1],cP[2]))
            fileDescriptor.write("\n")
        fileDescriptor.close()

    def extractSubList(self,listToSplit,sublistLength):
        listOfLists = []
        for i in xrange(0, len(listToSplit), sublistLength):
            listOfLists.append(listToSplit[i: i+sublistLength])
        return listOfLists



    def loadHairs(self, path):
        try:
            fileDescriptor = open(path)
        except:
            print "Impossible to load %s"%(path)
            return

        self.guides = []
        for data in fileDescriptor:
            datalist = data.split()
            if datalist[0] == "written":
                pass
            elif datalist[0] == "version":
                pass
            elif datalist[0] == "tags":
                pass
            elif datalist[0] == "numberofhairs":
                self.numberOfHairs = int(datalist[1])
            elif datalist[0] == "tipMagnet":
                self.tipMagnet = float(datalist[1])
            elif datalist[0] == "clumptype":
                self.clumpyype = float(datalist[1])
            elif datalist[0] == "tuftsize":
                self.tuftSize = float(datalist[1])
            elif datalist[0] == "randomfact":
                self.randomFact = float(datalist[1])
            elif datalist[0] == "hairdiameter":
                self.hairDiameter = float(datalist[1])
            elif datalist[0] == "tipcolor":
                self.tipColor[0] = float(datalist[1])
                self.tipColor[1] = float(datalist[2])
                self.tipColor[2] = float(datalist[3])
            elif datalist[0] == "rootcolor":
                self.rootColor[0] = float(datalist[1])
                self.rootColor[1] = float(datalist[2])
                self.rootColor[2] = float(datalist[3])
            else:
                controlPointsCoo = datalist[1:]
                for i in range(len(controlPointsCoo)):
                    controlPointsCoo[i] = float(controlPointsCoo[i])
                guidePoints = self.extractSubList(controlPointsCoo,3)
                self.addHairGuide(guidePoints, datalist[0])
        fileDescriptor.close()









