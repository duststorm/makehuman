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

class HairGroup:
    """
    HairGroup is basically a set of hair objects. 
    """
    def __init__(self,name):
        self.name = name
        self.hairs = []
        
class GuideGroup:
    """
    GuideGroup is basically a set of guide objects. 
    """
    def __init__(self,name):
        self.name = name
        self.guides = []

class Hairgenerator:
    """
    Hair generator make a series of hair sets, one for each hairguide.
    The sum of all hair sets (think of it as tufts) is called hairstyle.
    """

    def __init__(self):

        self.hairStyle = []

        self.tipMagnet = 0.9        

        self.numberOfHairsClump = 10
        self.numberOfHairsMultiStrand = 20

        self.randomFactClump = 0.5
        self.randomFactMultiStrand = 0.5
        self.randomPercentage = 0.5

        self.hairDiameterClump = 0.006
        self.hairDiameterMultiStrand = 0.006

        self.sizeClump = 0.200
        self.sizeMultiStrand = 0.200
        self.blendDistance = 0.8


        self.tipColor = [0.518,0.325,0.125]
        self.rootColor = [0.109, 0.037, 0.007]
        self.guideGroups = []
        self.version = "1.0 alpha 2"
        self.tags = []
        self.humanVerts = []
        #self.octree = simpleoctree.SimpleOctree(humanMesh.verts)# not used yet
        
    def resetHairs(self):
        self.hairStyle = []
        self.guideGroups = []

        
    def addGuideGroup(self,name):        
        g = GuideGroup(name)
        self.guideGroups.append(g)
        return g
        
    def adjustGuides(self,path):
        """

        """ 
        try:
            fileDescriptor = open(path)
        except:
            print "Impossible to load %s"%(path)
            return

        #Guides and Deltas have the same name, so it's
        #easy to associate them. Anyway we must a dd a check to
        #be sure the hairs to adjust are the same as saved in
        #the file. 
        deltaGuides = {}
        for data in fileDescriptor:
            datalist = data.split()
            if datalist[0] == "delta":
                name = datalist[1]
                guidesDelta = datalist[2:]
                deltaGuides[name] = self.extractSubList(guidesDelta,4)

        for group in self.guideGroups:
            for guide in group.guides:                
                deltaVector = deltaGuides[guide.name]                
                for i in range(len(deltaVector)):
                    cpDelta = deltaVector[i]
                    cpGuide = guide.controlPoints[i]                   
                    v = self.humanVerts[int(cpDelta[0])]                    
                    cpGuide[0] = v[0] + float(cpDelta[1])
                    cpGuide[1] = v[1] + float(cpDelta[2])
                    cpGuide[2] = v[2] + float(cpDelta[3])                      

    def addHairGuide(self,guidePoints, guideName, guideGroup):
 
        g = HairGuide(guideName)        
        for p in guidePoints:
            g.controlPoints.append([p[0],p[1],p[2]])
        guideGroup.guides.append(g)
        

    def generateHairStyle1(self):
        """
        Calling this function, for each guide in each guideGroup, 
        a new hairtuft will be added to the hairstyle.

        Parameters
        ----------

        No parameters
        """
        for guideGroup in self.guideGroups:
            for guide in guideGroup.guides:
                self.generateHairInterpolation1(guide)

    def generateHairStyle2(self):
        """
        Calling this function, each guide is interpolated with all other guides
        (that are in a radius < blendDistance) to add a new strand of hairs to
        the hairstyle.

        Parameters
        ----------

        No parameters
        """
        near = 0.08
        far = 1.6
                 
        
        for guideGroup in self.guideGroups:            
            for guide1 in guideGroup.guides: 
                samplePointIndex1 = int(len(guide1.controlPoints)/2)
                p1 = guide1.controlPoints[samplePointIndex1]
                for guide2 in guideGroup.guides:
                    if guide2.name != guide1.name:
                        samplePointIndex2 = int(len(guide2.controlPoints)/2) 
                        p2 = guide2.controlPoints[samplePointIndex2]
                        dist = aljabr.vdist(p1,p2)   
                        if dist < self.blendDistance:                     
                            self.generateHairInterpolation2(guide1,guide2)


    def generateHairInterpolation1(self,guide):
        hairName = "clump%s"%(guide.name)
        hSet = HairGroup(hairName)
        nVerts = len(guide.controlPoints)
        interpFactor1 = 0
        incr = 1.0/(self.numberOfHairsClump)
        

        
        for n in range (self.numberOfHairsClump):
            interpFactor1 += incr
            interpFactor2 = 0
            
            xRand = self.sizeClump*random.random()
            yRand = self.sizeClump*random.random()
            zRand = self.sizeClump*random.random()
            offsetVector = [xRand,yRand,zRand]
            
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
                        xRand = self.sizeClump*random.random()*self.randomFactClump
                        yRand = self.sizeClump*random.random()*self.randomFactClump
                        zRand = self.sizeClump*random.random()*self.randomFactClump
                        randomVect = [xRand,yRand,zRand]
                    else:                        
                        randomVect = [0,0,0]
                    
                    vert1 = guide.controlPoints[i]
                    h.controlPoints.append([vert1[0]+offsetVector[0]*magnet+randomVect[0],\
                                            vert1[1]+offsetVector[1]*magnet+randomVect[1],\
                                            vert1[2]+offsetVector[2]*magnet+randomVect[2]])
                hSet.hairs.append(h)
        self.hairStyle.append(hSet)


    def generateHairInterpolation2(self,guide1,guide2):
        hairName = "strand%s-%s"%(guide1.name,guide2.name)
        hSet = HairGroup(hairName)
       
        if len(guide1.controlPoints)>= len(guide2.controlPoints):
            longerGuide = guide1
            shorterGuide = guide2            
        else:
            longerGuide = guide2
            shorterGuide = guide1        
        
        nVerts = min([len(guide1.controlPoints),len(guide2.controlPoints)])        
        interpFactor = 0
        vertsListToModify1 = []
        vertsListToModify2 = []       

        for n in range (self.numberOfHairsMultiStrand):
            h = Hair()            
            interpFactor += 1.0/self.numberOfHairsMultiStrand
            for i in range(len(longerGuide.controlPoints)):
                if random.random() < self.randomPercentage: 
                    xRand = self.sizeMultiStrand*random.random()*self.randomFactMultiStrand
                    yRand = self.sizeMultiStrand*random.random()*self.randomFactMultiStrand
                    zRand = self.sizeMultiStrand*random.random()*self.randomFactMultiStrand
                    randomVect = [xRand,yRand,zRand]
                else:
                    randomVect = [0,0,0]
                
                if i == 0: 
                    i2 = 0
                if i == len(longerGuide.controlPoints)-1:
                    i2 = len(shorterGuide.controlPoints)-1
                else:
                    i2 = int(round(i*len(shorterGuide.controlPoints)/len(longerGuide.controlPoints)))                   
                    
                vert1 = longerGuide.controlPoints[i]
                vert2 = shorterGuide.controlPoints[i2]

                #Slerp
                angleBetweenGuides = math.acos(aljabr.vdot(aljabr.vnorm(vert1),aljabr.vnorm(vert2)))
                f1 = math.sin((1-interpFactor)*angleBetweenGuides)/math.sin(angleBetweenGuides)
                f2 = math.sin(interpFactor*angleBetweenGuides)/math.sin(angleBetweenGuides)
                newVert = aljabr.vadd(aljabr.vmul(vert1,f1),aljabr.vmul(vert2,f2))

                #Uncomment the following line we use lerp instead slerp
                #newVert = aljabr.vadd(aljabr.vmul(vert1,(1-interpFactor)),aljabr.vmul(vert2,interpFactor))
                h.controlPoints.append([newVert[0]+randomVect[0],\
                                                newVert[1]+randomVect[1],\
                                                newVert[2]+randomVect[2]])
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
        
        fileDescriptor.write("tipMagnet %f\n"%(self.tipMagnet))
        fileDescriptor.write("numberOfHairsClump %i\n"%(self.numberOfHairsClump))
        fileDescriptor.write("numberOfHairsMultiStrand %i\n"%(self.numberOfHairsMultiStrand))
        fileDescriptor.write("randomFactClump %f\n"%(self.randomFactClump))
        fileDescriptor.write("randomFactMultiStrand %f\n"%(self.randomFactMultiStrand))
        fileDescriptor.write("randomPercentage %f\n"%(self.randomPercentage))
        fileDescriptor.write("hairDiameterClump %f\n"%(self.hairDiameterClump))
        fileDescriptor.write("hairDiameterMultiStrand %f\n"%(self.hairDiameterMultiStrand))
        fileDescriptor.write("sizeClump %f\n"%(self.sizeClump))
        fileDescriptor.write("sizeMultiStrand %f\n"%(self.sizeMultiStrand))
        fileDescriptor.write("blendDistance %f\n"%(self.blendDistance))        
        
        fileDescriptor.write("tipcolor %f %f %f\n"%(self.tipColor[0],self.tipColor[1],self.tipColor[2]))
        fileDescriptor.write("rootcolor %f %f %f\n"%(self.rootColor[0],self.rootColor[1],self.rootColor[2]))

        for guideGroup in self.guideGroups:            
            fileDescriptor.write("guideGroup %s\n"%(guideGroup.name))        
            for guide in guideGroup.guides:
                fileDescriptor.write("guide %s "%(guide.name))
                #Write points coord
                for cP in guide.controlPoints:
                    fileDescriptor.write("%f %f %f "%(cP[0],cP[1],cP[2]))
                fileDescriptor.write("\n")

        for guideGroup in self.guideGroups:
            print "guidegroup",guideGroup.name
            for guide in guideGroup.guides:
                fileDescriptor.write("delta %s "%(guide.name))
                #Write points nearest body verts
                for cP in guide.controlPoints:
                    distMin = 1000
                    for i in range(len(self.humanVerts)): #later we optimize this using octree
                        v = self.humanVerts[i]
                        dist = aljabr.vdist(cP,v)                        
                        if dist < distMin:
                            distMin = dist
                            nearVert = v
                            nearVertIndex = i
                    delta = aljabr.vsub(cP,nearVert)
                    fileDescriptor.write("%i %f %f %f "%(nearVertIndex, delta[0],delta[1],delta[2]))
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

        self.resetHairs()
        for data in fileDescriptor:
            datalist = data.split()
            if datalist[0] == "written":
                pass
            elif datalist[0] == "version":
                pass
            elif datalist[0] == "tags":
                pass
            elif datalist[0] == "tipMagnet":
                self.tipMagnet = float(datalist[1])
            elif datalist[0] == "numberOfHairsClump":
                self.numberOfHairsClump = float(datalist[1])
            elif datalist[0] == "numberOfHairsMultiStrand":
                self.numberOfHairsMultiStrand = float(datalist[1])
            elif datalist[0] == "randomFactClump":
                self.randomFactClump = float(datalist[1])
            elif datalist[0] == "randomFactMultiStrand":
                self.randomFactMultiStrand = float(datalist[1])
            elif datalist[0] == "randomPercentage":
                self.randomPercentage = float(datalist[1])
            elif datalist[0] == "hairDiameterClump":
                self.hairDiameterClump = float(datalist[1])
            elif datalist[0] == "hairDiameterMultiStrand":
                self.hairDiameterMultiStrand = float(datalist[1])
            elif datalist[0] == "sizeClump":
                self.sizeClump = float(datalist[1])
            elif datalist[0] == "sizeMultiStrand":
                self.sizeMultiStrand = float(datalist[1])
            elif datalist[0] == "blendDistance":
                self.blendDistance = float(datalist[1])                
                
            elif datalist[0] == "tipcolor":
                self.tipColor[0] = float(datalist[1])
                self.tipColor[1] = float(datalist[2])
                self.tipColor[2] = float(datalist[3])
            elif datalist[0] == "rootcolor":
                self.rootColor[0] = float(datalist[1])
                self.rootColor[1] = float(datalist[2])
                self.rootColor[2] = float(datalist[3])
            elif datalist[0] == "guideGroup":
                currentGroup = self.addGuideGroup(datalist[1])
            elif datalist[0] == "guide":
                guideName = datalist[1]
                controlPointsCoo = datalist[2:]
                for i in range(len(controlPointsCoo)):
                    controlPointsCoo[i] = float(controlPointsCoo[i])
                guidePoints = self.extractSubList(controlPointsCoo,3)
                self.addHairGuide(guidePoints, guideName, currentGroup)
                
        fileDescriptor.close()









