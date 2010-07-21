#!/usr/bin/python
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
===========================  ===============================================================
Project Name:                **MakeHuman**
Product Home Page:           http://www.makehuman.org/
Google Home Page:            http://code.google.com/p/makehuman/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2010
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
from collision import collision
from os import path

"""
class Hair: #this is just a strand aka. curve!

    def __init__(self):
        self.controlPoints = []


class HairGuide(Hair): # a curve!


    def __init__(self, name):
        Hair.__init__(self)
        self.name = name


class HairGroup:

    def __init__(self, name):
        self.name = name
        self.hairs = []


class GuideGroup: #contains 2 curves (2 guides)

    def __init__(self, name):
        self.name = name
        self.guides = []

"""

class Hairgenerator:

    """
    Hair generator make a series of hair sets, one for each hairguide.
    The sum of all hair sets (think of it as tufts) is called hairstyle.
    """

    def __init__(self):
        #simplifying the class... removed 
        self.hairStyle = [] #this will become a list of n-tuples of guides (after the interpolation)

        self.tipMagnet = 0.9
         
        self.numberOfHairsClump = 10
        self.numberOfHairsMultiStrand = 20

        self.randomFactClump = 0.5
        self.randomFactMultiStrand = 0.5
        self.randomPercentage = 0.5

        self.hairDiameterClump = 0.006
        self.hairDiameterMultiStrand = 0.006

        self.sizeClump = 0.20
        self.sizeMultiStrand = 0.200
        self.blendDistance = 0.8

        self.tipColor = [0.518, 0.325, 0.125]
        self.rootColor = [0.109, 0.037, 0.007]
        #we use dictionary because if we save the obj with groups we need some kind of container that understands the group-name
        #Dictionary's hash  with keyvalues is an appropriate container
        self.guideGroups = dict() #dictionary of guide tuple (guidegroup)
        self.version = '1.0 alpha 2'
        self.tags = []
        self.humanVerts = []
        self.path = None

        self.noGuides = 25
        self.gLength = 5.0
        self.noCPoints = 15
        self.gFactor = 1.5
        self.Delta=None #Delta of the very first controlpoint of the very first guide in our guide list! This will be used as a reference

    def adjustGuides(self): 

        try:
            fileDescriptor = open(self.path)
        except:
            print 'Impossible to load %s' % self.path
            return

        # Guides and Deltas have the same name, so it's
        # easy to associate them. Anyway we must a dd a check to
        # be sure the hairs to adjust are the same as saved in
        # the file.

        for data in fileDescriptor:
            datalist = data.split()
            if datalist[0] == 'delta':
                name = datalist[1]
                guidesDelta = datalist[2:]

        for group in self.guideGroups:
            for guide in self.guideGroups[group]:
                for i in range(len(deltaVector)):
                    cpDelta = deltaVector[i]
                    if self.Delta == None:
                       self.Delta=cpDelta[:]
                    cpGuide = guide[i]
                    v = self.humanVerts[int(cpDelta[0])]
                    cpGuide[0] = v.co[0] + float(cpDelta[1])
                    cpGuide[1] = v.co[1] + float(cpDelta[2])
                    cpGuide[2] = v.co[2] + float(cpDelta[3])

    def generateHairStyle1(self):
        """
        Calling this function, for each guide in each guideGroup,
        a new hairtuft will be added to the hairstyle.

        Parameters
        ----------

        No parameters
        """
     
        for guideGroup in self.guideGroups: #taking tuples from list of tuples of curves
            for guide in guideGroup.guides: #taking curves from a tuple of curves
                self.generateHairInterpolation1(guide) #guide is a curve

    def getFromListbyName(self, list, name):
        """
        We should use a dictionary, but for a quick test this function is ok
        """

        for i in list:
            if i.name == name:
                return i
        return None

    def generateHairStyle2(self, humanMesh=None, isCollision=False):
        """
        Calling this function, each guide is interpolated with all other guides
        to add a new strand of hairs to the hairstyle.

        Parameters
        ----------

        No parameters
        """

        # near = 0.08
        # far = 1.6

        if humanMesh == None:
            isCollision = False
        for guideGroup in self.guideGroups:
            if len(guideGroup) > 0:

                # Find the bounding box of the cloud of controlPoints[2]

                print 'WORKING ON GROUP %s' % guideGroup
                guideOrder = {}
                xMin = 1000
                xMax = -1000
                yMin = 1000
                yMax = -1000
                zMin = 1000
                zMax = -1000
                for guide in self.guideGroups[guideGroup]:
                    p = guide[2]
                    #print guide.name, p
                    if p[0] < xMin:
                        xMin = p[0]
                    if p[0] > xMax:
                        xMax = p[0]

                    if p[1] < yMin:
                        yMin = p[1]
                    if p[1] > yMax:
                        yMax = p[1]

                    if p[2] < zMin:
                        zMin = p[2]
                    if p[2] > zMax:
                        zMax = p[2]
                diffX = xMax - xMin
                diffY = yMax - yMin
                diffZ = zMax - zMin

                # print "DIFF",diffX,diffY,diffZ

                # Find the main dimension of bounding box

                if diffX > diffY and diffX > diffZ:
                    mainDirection = 0
                if diffY > diffX and diffY > diffZ:
                    mainDirection = 1
                if diffZ > diffX and diffZ > diffY:
                    mainDirection = 2

                print 'MaindDirection', mainDirection

                # Order the guides along the main dimension

                for guide1 in self.guideGroups[guideGroup]:
                    p1 = guide1[2]
                    guideOrder[p1[mainDirection]] = guide1

                guideKeys = guideOrder.keys()
                guideKeys.sort()
                for i in range(len(guideKeys) - 1):
                    k1 = guideKeys[i]
                    k2 = guideKeys[i + 1]
                    guide1 = guideOrder[k1]
                    guide2 = guideOrder[k2]
                    #print 'INTERP. GUIDE', guide1.name, guide2.name
                    self.generateHairInterpolation2(guide1, guide2, humanMesh, isCollision)

    def generateHairInterpolation1(self, guide):
        #hairName = 'clump%s' % guide.name
        hSet = [] #empty list of list of curves  #HairGroup(hairName).. one whole group of hairstrands
        nVerts = len(guide)
        interpFactor1 = 0
        incr = 1.0 / self.numberOfHairsClump

        for n in xrange(self.numberOfHairsClump):
            interpFactor1 += incr
            interpFactor2 = 0

            xRand = self.sizeClump * random.random()
            yRand = self.sizeClump * random.random()
            zRand = self.sizeClump * random.random()
            offsetVector = [xRand, yRand, zRand]

            for n2 in xrange(self.numberOfHairsClump):
                h = [] #an empty strand (curve) with nVerts controlpoints, we make this as a list of triples.. triples cannot be reassigned! but we need to assign only once anyway
                interpFactor2 += incr
                for i in range(nVerts):
                    if nVerts > 3:
                        clumpIndex = nVerts - 2
                    else:
                        clumpIndex = nVerts - 1

                    magnet = 1.0 - (i / float(clumpIndex)) * self.tipMagnet
                    if random.random() < self.randomPercentage:
                        xRand = (self.sizeClump * random.random()) * self.randomFactClump
                        yRand = (self.sizeClump * random.random()) * self.randomFactClump
                        zRand = (self.sizeClump * random.random()) * self.randomFactClump
                        randomVect = [xRand, yRand, zRand]
                    else:
                        randomVect = [0, 0, 0]

                    vert1 = guide[i]
                    h.append([vert1[0] + offsetVector[0] * magnet + randomVect[0], vert1[1] + offsetVector[1] * magnet + randomVect[1], vert1[2]
                                            + offsetVector[2] * magnet + randomVect[2]])
                hSet.append(h)
        self.hairStyle.append(hSet) #list of (list of curves) clumps

    # humanMesh is a blender object.. the format can be changed later on if the necessity arises!
    # for the time being we have a blender object and gravity direction is [0,-1,0]

    #Josenow
    def generateHairInterpolation2(self, guide1, guide2, humanMesh, isCollision, startIndex=9, gravity=True):
        if isCollision:
            octree = simpleoctree.SimpleOctree(humanMesh.getData().verts, 0.08)
        #hairName = 'strand%s-%s' % (guide1.name, guide2.name)
        hSet = [] #HairGroup(hairName)

        if len(guide1) >= len(guide2):
            longerGuide = guide1
            shorterGuide = guide2
        else:
            longerGuide = guide2
            shorterGuide = guide1

        nVerts = min([len(guide1), len(guide2)])
        interpFactor = 0
        vertsListToModify1 = []
        vertsListToModify2 = []

        for n in range(self.numberOfHairsMultiStrand):
            h = []
            interpFactor += 1.0 / self.numberOfHairsMultiStrand
            for i in range(len(longerGuide)):
                if random.random() < self.randomPercentage:
                    xRand = (self.sizeMultiStrand * random.random()) * self.randomFactMultiStrand
                    yRand = (self.sizeMultiStrand * random.random()) * self.randomFactMultiStrand
                    zRand = (self.sizeMultiStrand * random.random()) * self.randomFactMultiStrand
                    randomVect = [xRand, yRand, zRand]
                else:
                    randomVect = [0, 0, 0]

                if i == 0:
                    i2 = 0
                if i == len(longerGuide) - 1:
                    i2 = len(shorterGuide) - 1
                else:
                    i2 = int(round((i * len(shorterGuide)) / len(longerGuide)))

                vert1 = longerGuide[i]
                vert2 = shorterGuide[i2]

                # Slerp

                dotProd = aljabr.vdot(aljabr.vnorm(vert1), aljabr.vnorm(vert2))

                # Python has a very very bad numerical accuracy.. we need to do this for very small angle between guides
                # this occurs when we do collision detection

                if dotProd > 1:
                    angleBetweenGuides = 0.0
                else:
                    angleBetweenGuides = math.acos(aljabr.vdot(aljabr.vnorm(vert1), aljabr.vnorm(vert2)))
                denom = math.sin(angleBetweenGuides)
                if denom == 0.0:  # controlpoints of some guides coincide
                    vert1[0] = ((self.randomPercentage * self.sizeMultiStrand) * random.random()) * self.randomFactMultiStrand + vert1[0]
                    vert1[1] = ((self.randomPercentage * self.sizeMultiStrand) * random.random()) * self.randomFactMultiStrand + vert1[1]
                    vert1[2] = ((self.randomPercentage * self.sizeMultiStrand) * random.random()) * self.randomFactMultiStrand + vert1[2]
                    vert1 = aljabr.vadd(vert1, randomVect)
                    angleBetweenGuides = math.acos(aljabr.vdot(aljabr.vnorm(vert1), aljabr.vnorm(vert2)))
                    denom = math.sin(angleBetweenGuides)
                f1 = math.sin((1 - interpFactor) * angleBetweenGuides) / denom
                f2 = math.sin(interpFactor * angleBetweenGuides) / denom
                newVert = aljabr.vadd(aljabr.vmul(vert1, f1), aljabr.vmul(vert2, f2))

                # Uncomment the following line we use lerp instead slerp
                # newVert = aljabr.vadd(aljabr.vmul(vert1,(1-interpFactor)),aljabr.vmul(vert2,interpFactor))

                h.append((newVert[0] + randomVect[0], newVert[1] + randomVect[1], newVert[2] + randomVect[2]))
            if isCollision:
                print 'h is: ', h
                for j in (0, len(h)):

                    # print "h.controlPts is : ", h.controlPoints[i]
                    # print "h.controlPts[i] length is: ", len(h.controlPoints[i])

                    h[i][2] = -h[i][2]  # Renderman to Blender coordinates!
                collision(h, humanMesh, octree.minsize, startIndex, gravity)
                for j in (0, len(h)):
                    h[i][2] = -h[i][2]  # Blender to Renderman coordinates!
            hSet.append(h)
        self.hairStyle.append(hSet)

    def saveHairs(self, path):
        """
        Save a file containing the info needed to build the hairstyle,
        strating from the hair guides and using some parameters.
        """

        try:
            fileDescriptor = open(path, 'w')
        except:
            print 'Impossible to save %s' % path
            return

        fileDescriptor.write('written by makehair 1.0\n')
        fileDescriptor.write('version %s\n' % self.version)
        fileDescriptor.write('tags ')
        for tag in self.tags:
            fileDescriptor.write('%s ' % tag)
        fileDescriptor.write('\n')

        fileDescriptor.write('tipMagnet %f\n' % self.tipMagnet)
        fileDescriptor.write('numberOfHairsClump %i\n' % self.numberOfHairsClump)
        fileDescriptor.write('numberOfHairsMultiStrand %i\n' % self.numberOfHairsMultiStrand)
        fileDescriptor.write('randomFactClump %f\n' % self.randomFactClump)
        fileDescriptor.write('randomFactMultiStrand %f\n' % self.randomFactMultiStrand)
        fileDescriptor.write('randomPercentage %f\n' % self.randomPercentage)
        fileDescriptor.write('hairDiameterClump %f\n' % self.hairDiameterClump)
        fileDescriptor.write('hairDiameterMultiStrand %f\n' % self.hairDiameterMultiStrand)
        fileDescriptor.write('sizeClump %f\n' % self.sizeClump)
        fileDescriptor.write('sizeMultiStrand %f\n' % self.sizeMultiStrand)
        fileDescriptor.write('blendDistance %f\n' % self.blendDistance)

        fileDescriptor.write('tipcolor %f %f %f\n' % (self.tipColor[0], self.tipColor[1], self.tipColor[2]))
        fileDescriptor.write('rootcolor %f %f %f\n' % (self.rootColor[0], self.rootColor[1], self.rootColor[2]))

        for guideGroup in self.guideGroups:
            fileDescriptor.write('guideGroup %s\n' % guideGroup)
            for guide in guideGroup.guides:
                #fileDescriptor.write('guide %s ' % guide.name)

                # Write points coord

                for cP in guide.controlPoints:
                    fileDescriptor.write('%f %f %f ' % (cP[0], cP[1], cP[2]))
                fileDescriptor.write('\n')

        for guideGroup in self.guideGroups:
            print 'guidegroup', guideGroup
            for guide in self.guideGroups[guideGroup]:
                #fileDescriptor.write('delta %s ' % guide.name)

                # Write points nearest body verts

                for cP in guide:
                    distMin = 1000
                    for i in range(len(self.humanVerts)):  # later we optimize this using octree
                        v = self.humanVerts[i]
                        dist = aljabr.vdist(cP, v)
                        if dist < distMin:
                            distMin = dist
                            nearVert = v
                            nearVertIndex = i
                    delta = aljabr.vsub(cP, nearVert)
                    fileDescriptor.write('%i %f %f %f ' % (nearVertIndex, delta[0], delta[1], delta[2]))
                fileDescriptor.write('\n')
        fileDescriptor.close()

    def extractSubList(self, listToSplit, sublistLength):
        listOfLists = []
        for i in xrange(0, len(listToSplit), sublistLength):
            listOfLists.append(listToSplit[i:i + sublistLength])
        return listOfLists

    def loadHairs(self, name):
        try:
            name = path.splitext(name)[0]
            objFile = open(name + ".obj")
            fileDescriptor = open(name+".hair")
        except:
            print 'Unable to load .obj and .hair file of %s' % name
            return

        #self.resetHairs()
        self.path = name
        for data in fileDescriptor:
            datalist = data.split()
            if datalist[0] == 'written':
                pass
            elif datalist[0] == 'version':
                pass
            elif datalist[0] == 'tags':
                pass
            elif datalist[0] == 'tipMagnet':
                self.tipMagnet = float(datalist[1])
            elif datalist[0] == 'numberOfHairsClump':
                self.numberOfHairsClump = int(datalist[1])
            elif datalist[0] == 'numberOfHairsMultiStrand':
                self.numberOfHairsMultiStrand = int(datalist[1])
            elif datalist[0] == 'randomFactClump':
                self.randomFactClump = float(datalist[1])
            elif datalist[0] == 'randomFactMultiStrand':
                self.randomFactMultiStrand = float(datalist[1])
            elif datalist[0] == 'randomPercentage':
                self.randomPercentage = float(datalist[1])
            elif datalist[0] == 'hairDiameterClump':
                self.hairDiameterClump = float(datalist[1])
            elif datalist[0] == 'hairDiameterMultiStrand':
                self.hairDiameterMultiStrand = float(datalist[1])
            elif datalist[0] == 'sizeClump':
                self.sizeClump = float(datalist[1])
            elif datalist[0] == 'sizeMultiStrand':
                self.sizeMultiStrand = float(datalist[1])
            elif datalist[0] == 'blendDistance':
                self.blendDistance = float(datalist[1])
            elif datalist[0] == 'tipcolor':

                self.tipColor[0] = float(datalist[1])
                self.tipColor[1] = float(datalist[2])
                self.tipColor[2] = float(datalist[3])
            elif datalist[0] == 'rootcolor':
                self.rootColor[0] = float(datalist[1])
                self.rootColor[1] = float(datalist[2])
                self.rootColor[2] = float(datalist[3])
                
            """
            elif datalist[0] == 'guideGroup':
                currentGroup = self.addGuideGroup(datalist[1])
            elif datalist[0] == 'guide':
                guideName = datalist[1]
                controlPointsCoo = datalist[2:]
                for i in range(len(controlPointsCoo)):
                    controlPointsCoo[i] = float(controlPointsCoo[i])
                guidePoints = self.extractSubList(controlPointsCoo, 3)
                self.addHairGuide(guidePoints, guideName, currentGroup)
            """

        fileDescriptor.close()
        
        guidePoints=[]
        temp =[]
        #currentGroup=None
        #guideName = None
        guides = [] #set of curves
        #Forget the format of manuel make your own!
        reGroup = True
        for data in objFile:
            datalist = data.split()
            if datalist[0] == "v":
                for i in xrange(1,4):
                    datalist[i] = float(datalist[i])
                temp.append(datalist[1:])
            elif datalist[0] == "curv":
                #n = len(datalist[3:])
                #guidePoints=[None]*n
                for index in datalist[3:]:
                    guidePoints.append(temp[int(index)])
                temp=[]
            elif datalist[0] == "g":
                #datalist[1] = datalist[1].split("_") #first entry = group, second entry= guidename)
                #Josenow! Todo Guidegroup problem adding
                #currentGroup = self.addGuideGroup(datalist[1][0])
                #if len(datalist[1])>1: guideName = datalist[1][1]
                if datalist[1] in self.guideGroups :
                    self.guideGroups[datalist[1]].append(guidePoints)
                    self.guideGroups[datalist[1]] = tuple(self.guideGroups[datalist[1]])
                    reGroup = False
                else:
                    self.guideGroups[datalist[1]] = [guidePoints]
                    reGroup = True
            elif datalist[0] == "end":
                guides.append(guidePoints); #apppend takes a deep copy
                #self.addHairGuide(guidePoints, guideName,currentGroup)
                #if currentGroup == None: reGroup = True;
                guidePoints=[]
        objFile.close()
        if reGroup: self.populateGuideGroups(guides,0.6)

    #guides is of type list of curves
    #self.guideGroups is a list of tuples (as in pairs) of guides (curves)
    def populateGuideGroups(self,guides,Area):
        self.guideGroups.clear()
        Summarize = 0
        S = set() #emptyset of indices.. hashing trick
        for i in xrange(0,len(guides)):
            if i in S: continue
            else: S.add(i)
            k=0
            A=[] #ordered as infinity!
            for j in xrange(0,len(guides)):
                if (j != i):
                    B = curvePairArea(guides[i],guides[j])
                    if B==0: continue #duplicate strands can occur!
                    if A>B and B>=Area:
                        k=j
                        A=B
            S.add(k)
            Summarize = Summarize + A
            self.guideGroups[str(i)] = (guides[i],guides[k])
        print "Debug Average Area: ", Summarize/len(guides)

def curvePairArea(c1, c2):
    n=min(len(c1),len(c2))
    A=0
    temp=0
    for i in xrange(1,n):
        try:
            temp = aljabr.convexQuadrilateralArea(c1[i-1],c2[i-1],c2[i],c1[i])
        except:
            return 0
        A = A+temp
    return A
