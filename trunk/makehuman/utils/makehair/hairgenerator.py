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

        self.tipMagnet = 0.0
        self.clumptype = 1

        self.numberOfHairsClump = 90
        self.numberOfHairsMultiStrand = 90

        self.randomFactClump = 0.0
        self.randomFactMultiStrand = 0.0

        self.hairDiameterClump = 0.006
        self.hairDiameterMultiStrand = 0.006

        self.sizeClump = 0.150
        self.sizeMultiStrand = 0.150


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
            distMin = .8
            guideToInterpolate = None
            for guide2 in self.guides:
                if guide2.name != currentGuide:
                    p2 = guide2.controlPoints[samplePointIndex]
                    dist = aljabr.vdist(p1,p2)
                    #print p1
                    #print p2
                    #print "DIST BETWEEN %s ANS %s = %f"%(currentGuide,guide2.name,dist)
                    if dist < distMin:
                        #distMin = dist
                        guideToInterpolate = guide2
                        self.generateHairInterpolation2(guide,guideToInterpolate)

   
    def generateHairInterpolation1(self,guide):
        hairName = "clump%s"%(guide.name)
        hSet = HairSet(hairName)
        nVerts = len(guide.controlPoints)
        #headCentroid = [0.0,-0.570,7.318] #hardcoded...TODO
        interpFactor = 0
        switch = 0
        for n in range (self.numberOfHairsClump):
            rFact = random.uniform(0.0,1.0)*self.randomFactClump
            
            print "rFact", rFact
            interpFactor += 1.0/self.numberOfHairsMultiStrand
            h = Hair()
            vertsListToModify = []
            if switch == 0:
                switch = 1
            else:
                switch = 0
                
            for c in guide.controlPoints:
                vertsListToModify.append([c[0],c[1],c[2]])#maybe useless

            
            for i in range(nVerts):                
                if nVerts > 3:
                    clumpIndex = nVerts-2
                else:
                    clumpIndex = nVerts-1

                magnet = 1.0-(i/float(clumpIndex))                
                rFact2 = random.uniform(0.0,0.5)*self.randomFactClump
                if  i >= clumpIndex:
                    
                    offset =  self.sizeClump*magnet*interpFactor+rFact*magnet+rFact2
                    vert0 = vertsListToModify[i-2]                 
                    vert1 = vertsListToModify[i-1]
                    vert2 = vertsListToModify[i]
                    vector1 = aljabr.vsub(vert2,vert1)
                    vector2 = aljabr.vsub(vert1,vert0)
                    vector3 = aljabr.vnorm(aljabr.vcross(vector1,vector2))
                    vector4 = aljabr.vnorm(aljabr.vcross(vector1,vector3))
                elif i < 1:
                    offset =  self.sizeClump*magnet*interpFactor+rFact*magnet+rFact2
                    vert0 = vertsListToModify[0]                 
                    vert1 = vertsListToModify[1]
                    vert2 = vertsListToModify[2]
                    vector1 = aljabr.vsub(vert2,vert1)
                    vector2 = aljabr.vsub(vert1,vert0)
                    vector3 = aljabr.vnorm(aljabr.vcross(vector1,vector2))
                    vector4 = aljabr.vnorm(aljabr.vcross(vector1,vector3))
                else:
                    offset =  self.sizeClump*magnet*interpFactor+rFact*magnet+rFact2
                    vert0 = vertsListToModify[i-1]                 
                    vert1 = vertsListToModify[i]
                    vert2 = vertsListToModify[i+1]
                    vector1 = aljabr.vsub(vert2,vert1)
                    vector2 = aljabr.vsub(vert1,vert0)
                    vector3 = aljabr.vnorm(aljabr.vcross(vector1,vector2))
                    vector4 = aljabr.vnorm(aljabr.vcross(vector1,vector3))
                    
                    

                #randomHairs = random.uniform(0,self.randomFactClump)*offset
                if switch == 0:
                    h.controlPoints.append([vert1[0]+vector3[0]*offset,\
                                                    vert1[1]+vector3[1]*offset,\
                                                    -vert1[2]+vector3[2]*offset])#I should to do in Blender coords
                else:
                    h.controlPoints.append([vert1[0]+vector4[0]*offset,\
                                                        vert1[1]+vector4[1]*offset,\
                                                        -vert1[2]+vector4[2]*offset])#I should to do in Blender coords
                                                                                  
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
            
            randomHairs = random.uniform(0.0,self.randomFactMultiStrand)*random.uniform(0.0,self.sizeMultiStrand)
            interpFactor += 1.0/self.numberOfHairsMultiStrand
            for i in range(nVerts):
                vert1 = vertsListToModify1[i]
                vert2 = vertsListToModify2[i]
                newVert = aljabr.vadd(aljabr.vmul(vert1,(1-interpFactor)),aljabr.vmul(vert2,interpFactor))
                h.controlPoints.append([newVert[0]+randomHairs,\
                                                newVert[1]+randomHairs,\
                                                -newVert[2]+randomHairs]) #I should to do in Blender coords

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









