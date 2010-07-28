#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import mh
import os
import algos3d
import aljabr
import math




class Limb():

    def __init__(self, name, character, dataPath = "data/targets/poseengine/joint-r-shoulder"):

        self.name = name
        self.examplesRot = []
        self.examplesTrasl = []
        self.trasl = {}
        self.rotx = {}
        self.roty = {}
        self.rotz = {}
        self.character = character
        self.dataPath = dataPath
        self.angle = [0,0,0]
        self.rotOrder = "xyz"


        try:
            fileDescriptor = open(os.path.join(dataPath,"rot.dat"))
        except:
            #print "File %s not found"%(os.path.join(dataPath,"rot.dat"))
            #print "Limb %s init fail"%(name)
            return
        for data in fileDescriptor:
            sample = [float(x) for x in data.split()]
            if len(sample) == 3:
                self.examplesRot.append(sample)
        fileDescriptor.close()

        fileDescriptor = open(os.path.join(dataPath,"trasl.dat"))
        for data in fileDescriptor:
            sample = [float(x) for x in data.split()]
            if len(sample) == 3:
                self.examplesTrasl.append(sample)
        fileDescriptor.close()

        self.angleMax = [-500,-500,-500]
        self.angleMin = [500,500,500]

        for s in self.examplesRot:
            if s[0] < self.angleMin[0]:
                self.angleMin[0] = s[0]
            if s[0] > self.angleMax[0]:
                self.angleMax[0] = s[0]

            if s[1] < self.angleMin[1]:
                self.angleMin[1] = s[1]
            if s[1] > self.angleMax[1]:
                self.angleMax[1] = s[1]

            if s[2] < self.angleMin[2]:
                self.angleMin[2] = s[2]
            if s[2] > self.angleMax[2]:
                self.angleMax[2] = s[2]


    def equalize(self,d1,d2,d3):

        D = d1+d2+d3
        D1 = D/(d1+0.0001)
        D2 = D/(d2+0.0001)
        D3 = D/(d3+0.0001)
        Dtot = D1+D2+D3
        IAS1 = D1/Dtot
        IAS2 = D2/Dtot
        IAS3 = D3/Dtot
        return IAS1,IAS2,IAS3


    def chooseRotSamples(self):

        rotExamples = []
        rotValues = []
        rotAxis = []
        for n in range(3):
            sample = [0,0,0]
            sampleVal = 0
            sampleAxi = "x"
            if self.angle[n] < 0:
                sample[n] = self.angleMin[n]
                sampleVal = float(self.angle[n])/self.angleMin[n]
            if self.angle[n] > 0:
                sample[n] = self.angleMax[n]
                sampleVal = float(self.angle[n])/self.angleMax[n]
            if sample[0]!= 0:
                sampleAxi = "x"
            if sample[1]!= 0:
                sampleAxi = "y"
            if sample[2]!= 0:
                sampleAxi = "z"
            rotAxis.append(sampleAxi)
            rotExamples.append(sample)
            rotValues.append(sampleVal)

        return (rotExamples[0],rotExamples[1],rotExamples[2],rotValues[0],rotValues[1],rotValues[2],rotAxis[0],rotAxis[1],rotAxis[2])


    def chooseTraslSamples(self):
        direction = aljabr.vnorm(self.angle)
        similarity = {}
        if self.angle != [0.0,0.0,0.0]:
            for sample in self.examplesTrasl:
                direction2 = aljabr.vnorm(sample)
                sampleDistance1 = aljabr.vdist(direction,direction2)
                sampleDistance2 = math.fabs(aljabr.vlen(aljabr.vsub(self.angle,sample)))
                similarity[sampleDistance1+sampleDistance2] = sample
            d = similarity.keys()
            d.sort()
            nearestSample1 = similarity[d[0]]
            nearestSample2 = similarity[d[1]]
            nearestSample3 = similarity[d[2]]
            factor1,factor2,factor3 = self.equalize(d[0],d[1],d[2])
            return (nearestSample1,nearestSample2,nearestSample3,factor1,factor2,factor3)
        else:
            return ([0,0,0],[0,0,0],[0,0,0],0,0,0)





    def loadTargets(self):

        traslExamples = {}

        #Generation of paths, in order to find the data according the
        #character parameters
        humanCategories = [ "_flaccid",
                            "_muscle",
                            "_heavy",
                            "_light",
                            "_flaccid_heavy",
                            "_flaccid_light",
                            "_muscle_heavy",
                            "_muscle_light"]        
        humanAges = ["_young", "_old","_child"]        
        humanTypes = ["female","male"]

        #Generation of values, in order to apply the corrections data
        #according the character parameters
        averageWeightVal = 1 - (self.character.underweightVal + self.character.overweightVal)
        averageToneVal = 1 - (self.character.muscleVal + self.character.flaccidVal)
        humanCategoriesVal = [self.character.flaccidVal*averageWeightVal,
                            self.character.muscleVal*averageWeightVal,
                            self.character.overweightVal*averageToneVal,
                            self.character.underweightVal*averageToneVal,
                            self.character.flaccidVal*self.character.overweightVal,
                            self.character.flaccidVal*self.character.underweightVal,
                            self.character.muscleVal*self.character.overweightVal,
                            self.character.muscleVal*self.character.underweightVal]
        humanTypesVal = [self.character.femaleVal,self.character.maleVal]
        humanAgesVal = [self.character.youngVal,self.character.oldVal,self.character.childVal]


        for n1,h1 in enumerate(humanTypes):
            for n2,h2 in enumerate(humanAges):
                targetLabel1 = h1+h2
                targetValue1 = humanTypesVal[n1]*humanAgesVal[n2]
                traslExamples[targetLabel1] = targetValue1                
                for n3,h3 in enumerate(humanCategories):
                    targetLabel2 = h1+h2+h3
                    targetValue2 = humanTypesVal[n1]*humanAgesVal[n2]*humanCategoriesVal[n3]
                    traslExamples[targetLabel2] = targetValue2
                    


        #translations
        samplesTrasl = self.chooseTraslSamples()
        targetTrasl1 = "_".join([str(int(x)) for x in samplesTrasl[0]])
        targetTrasl2 = "_".join([str(int(x)) for x in samplesTrasl[1]])
        targetTrasl3 = "_".join([str(int(x)) for x in samplesTrasl[2]])
        morphTraslVal1 = samplesTrasl[3]
        morphTraslVal2 = samplesTrasl[4]
        morphTraslVal3 = samplesTrasl[5]

        #I'LL DECOMMENT THIS AS SOON WE HAVE MORE DATA
        #for k,i in traslExamples.iteritems():
            #traslDir = os.path.join(self.dataPath,"translations",k)
            #pathTrasl1 = os.path.join(traslDir,targetTrasl1)
            #pathTrasl2 = os.path.join(traslDir,targetTrasl2)
            #pathTrasl3 = os.path.join(traslDir,targetTrasl3)
            #self.decomposeSamples(pathTrasl1,morphTraslVal1*i)
            #self.decomposeSamples(pathTrasl2,morphTraslVal2*i)
            #self.decomposeSamples(pathTrasl3,morphTraslVal3*i)


        #THIS IS HARDCODED TO USE ONLY DATA IN FEMALE_YOUNG FOLDER
        traslDir = os.path.join(self.dataPath,"translations","female_young")
        i = 1
        pathTrasl1 = os.path.join(traslDir,targetTrasl1)
        pathTrasl2 = os.path.join(traslDir,targetTrasl2)
        pathTrasl3 = os.path.join(traslDir,targetTrasl3)
        self.decomposeSamples(pathTrasl1,morphTraslVal1*i)
        self.decomposeSamples(pathTrasl2,morphTraslVal2*i)
        self.decomposeSamples(pathTrasl3,morphTraslVal3*i)


        #rotations
        rotDir = os.path.join(self.dataPath,"rotations")
        samplesRot = self.chooseRotSamples()
        targetRot1 = "_".join([str(int(x)) for x in samplesRot[0]])
        targetRot2 = "_".join([str(int(x)) for x in samplesRot[1]])
        targetRot3 = "_".join([str(int(x)) for x in samplesRot[2]])
        morphRotVal1 = samplesRot[3]
        morphRotVal2 = samplesRot[4]
        morphRotVal3 = samplesRot[5]
        axeRot1 = samplesRot[6]
        axeRot2 = samplesRot[7]
        axeRot3 = samplesRot[8]
        pathRot1 = os.path.join(rotDir,targetRot1)
        pathRot2 = os.path.join(rotDir,targetRot2)
        pathRot3 = os.path.join(rotDir,targetRot3)
        self.decomposeSamples(pathRot1,morphRotVal1,axeRot1)
        self.decomposeSamples(pathRot2,morphRotVal2,axeRot2)
        self.decomposeSamples(pathRot3,morphRotVal3,axeRot3)

        print "-------"
        print "SAMPLES USED FOR ", self.angle
        print "------- ROTATIONS-------"
        print os.path.basename(pathRot1),morphRotVal1
        print os.path.basename(pathRot2),morphRotVal2
        print os.path.basename(pathRot3),morphRotVal3
        print "------- TRASLATIONS-------"
        print os.path.basename(pathTrasl1),morphTraslVal1
        print os.path.basename(pathTrasl2),morphTraslVal2
        print os.path.basename(pathTrasl3),morphTraslVal3



    def decomposeSamples(self,path,morphFactor,axis = None):

        if os.path.isdir(path):
            targets = os.listdir(path)
            for t in targets:
                if "svn" not in t:
                    tpath = os.path.join(path,t)
                    if axis =="x":
                         self.rotx[tpath] = morphFactor
                    if axis =="y":
                         self.roty[tpath] = morphFactor
                    if axis =="z":
                         self.rotz[tpath] = morphFactor

        else:
            self.trasl[path+".target"] = morphFactor



    def applyPose(self):

        self.rotx = {}
        self.roty = {}
        self.rotz = {}
        self.trasl = {}

        self.character.restoreMesh() #restore the mesh without rotations
        self.loadTargets()

        if self.rotOrder == "xyz":
            rotSequence = [self.rotx,self.roty,self.rotz]
        if self.rotOrder == "xzy":
            rotSequence = [self.rotx,self.rotz,self.roty]
        if self.rotOrder == "zyx":
            rotSequence = [self.rotz,self.roty,self.rotx]
        if self.rotOrder == "zxy":
            rotSequence = [self.rotz,self.rotx,self.roty]
        if self.rotOrder == "yxz":
            rotSequence = [self.roty,self.rotx,self.rotz]
        if self.rotOrder == "yzx":
            rotSequence = [self.roty,self.rotz,self.rotx]

        traslPaths = self.trasl.keys()
        traslPaths.sort()
        for targetPath in traslPaths:
            morphFactor = self.trasl[targetPath]
            algos3d.loadTranslationTarget(self.character.meshData, targetPath, morphFactor, None, 1, 0)

        for rotation in rotSequence:
            rotPaths = rotation.keys()
            rotPaths.sort()
            for targetPath in rotPaths:

                morphFactor = rotation[targetPath]
                algos3d.loadRotationTarget(self.character.meshData, targetPath, morphFactor)

        self.character.meshData.calcNormals(facesToUpdate=[f for f in self.character.meshData.faces])
        self.character.meshData.update()


class Poseengine():


    def __init__(self,character,dataBase = "data/targets/poseengine" ):
        self.limbs = []
        try:
            fileDescriptor = open(os.path.join("data/targets/poseengine","group_hierarchy.dat"))
        except:
            print "Unable to open hierarchy file %s",(filePath)
            return  None
        for line in fileDescriptor:
            l = line.strip()
            if len(l) > 0 and "#" not in l:
                self.limbs.append(Limb(l,character,os.path.join("data","targets","poseengine",l)))
        fileDescriptor.close()

    def getLimb(self,limbName):
        for l in self.limbs:
            print repr(l.name),repr(limbName)
            if l.name == limbName:
                return l






