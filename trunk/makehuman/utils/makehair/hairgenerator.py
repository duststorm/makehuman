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

import random
import math

class HairGuide:
    def __init__(self,name):
        self.name = name
        self.controlPoints = []

class HairSet:
    def __init__(self,name):
        self.name = name
        self.hairs = []        

class Hairgenerator:

    def __init__(self):

        self.hairs = []
        self.numberOfHairs = 90
        self.percOfRebels = 1.0
        self.clumptype = 1.0
        self.tuftSize = 0.150
        self.randomFact = 0.0
        self.hairDiameter = 0.006
        self.tipColor = (0.518,0.325,0.125)
        self.rootColor = (0.109, 0.037, 0.007)
        self.guides = []

    def addHairGuide(self,curve, curveName):
        g = HairGuide(curveName)
        g.name = curveName
        for p in curve:
            g.controlPoints.append([p[0],p[1],p[2]])
        self.guides.append(g)

    def generateHairStyle(self):
        for guide in self.guides:            
            self.generateHairSets(guide)

    def generateHairSets(self,guide):
        hSet = HairSet(guide.name)
        p =int(100/self.percOfRebels)
        nVerts = len(guide.controlPoints)
        rebelHair = range(0,nVerts,p)

        for n in range (self.numberOfHairs):
            hair = []
            vertsListToModify = []
            for c in guide.controlPoints:
                vertsListToModify.append([c[0],c[1],c[2]])

            delta1= self.tuftSize*random.uniform(-1.0,1.0)
            delta2= self.tuftSize*random.uniform(-1.0,1.0)
            delta3= self.tuftSize*random.uniform(-1.0,1.0)

            rebelVal = random.uniform(0,self.randomFact)
            for i in range(nVerts):
                vert = vertsListToModify[i]
                #Position is an in index that show the position along the hair
                #because all verts have a incremental number, from the root of the hair to the tip.
                index = float(i)/nVerts
                tipMagnet = 1.0-index+(index*self.clumptype)
                if n in rebelHair:
                    hair.append([vert[0]+delta1+rebelVal,\
                                                vert[1]+delta2+rebelVal,\
                                                -vert[2]+delta3+rebelVal])
                else:
                    hair.append([vert[0]+delta1*tipMagnet,\
                                                vert[1]+delta2*tipMagnet,\
                                                -vert[2]+delta3*tipMagnet])
            hSet.hairs.append(hair)
        self.hairs.append(hSet)


    def saveHairs(self,path):
        try:
            fileDescriptor = open(path, "w")
        except:
            print "Impossible to save %s"%(path)
            return
        fileDescriptor.write("%i %f %f %f %f\n" % (self.numberOfHairs,\
                                                self.percOfRebels,\
                                                self.clumptype,\
                                                self.tuftSize,\
                                                self.randomFact,\
                                                self.hairDiameter))
        fileDescriptor.write("%f %f %f %f %f %f\n"% (self.tipColor[0],\
                                                    self.tipColor[1],\
                                                   self.tipColor[2]))


        #for tuft in self.hairs:
            #for controlPoint in tuft:
                #fileDescriptor.write("%f %f %f"%(





        fileDescriptor.close()


