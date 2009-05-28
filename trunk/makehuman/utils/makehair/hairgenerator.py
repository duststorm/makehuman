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


class hairgenerator:

    def __init__(self):

        self.hairs = []
        self.numberOfHairs = 90
        self.percOfRebels = 1.0
        self.clumptype = 1.0
        self.tuftSize = 0.150
        self.randomFact = 0.0
        self.hairDiameter = 0.006



    def generateTuft(self,curve):
        tuft = []
        p =int(100/self.percOfRebels)
        nVerts = len(curve)
        rebelHair = range(0,nVerts,p)
        
        for n in range (self.numberOfHairs):
            hairControlPoints = []
            vertsListToModify = []
            for v in curve:
                vertsListToModify.append([v[0],v[1],v[2]])

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
                    hairControlPoints.append([vert[0]+delta1+rebelVal,\
                                                vert[1]+delta2+rebelVal,\
                                                -vert[2]+delta3+rebelVal])
                else:
                    hairControlPoints.append([vert[0]+delta1*tipMagnet,\
                                                vert[1]+delta2*tipMagnet,\
                                                -vert[2]+delta3*tipMagnet])
            tuft.append(hairControlPoints)
        self.hairs.append(tuft)
        return tuft

            

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
        
        fileDescriptor.close()
         
        
        

        

    def getHairs(self):
        return self.hairs
