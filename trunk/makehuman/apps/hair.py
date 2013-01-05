#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

#import zipfile
import gui3d, events3d, guifiles, mh, os
from mh2obj import *
from animation3d import ThreeDQBspline
from aljabr import *
from math import radians
from os import path
from random import random, randint
from simpleoctree import SimpleOctree
import log

class Hairs:
    def __init__(self, human):
        
        self.saveAsCurves = True
        self.path = None
        self.guides = []
        self.grouping = {} #dictionary of list of guide indices
        self.widthFactor = 1.0
        self.oHeadCentroid = [0.0, 7.436, 0.03]
        self.oHeadBoundingBox = [[-0.84,6.409,-0.9862],[0.84,8.463,1.046]]
        self.hairDiameterMultiStrand = 0.006
        self.tipColor = [0.518, 0.325, 0.125]
        self.rootColor = [0.109, 0.037, 0.007]
        self.interpolationRadius = 0.09
        self.clumpInterpolationNumber = 0
        self.multiStrandNumber = 0
        self.randomness = 0.04
        self.human = human



    def reloadGuides(self):
        
        scn = self.human.scene
        scn.clear(self.human.hairObj)
        position = self.human.getPosition()
        rotation = self.human.getRotation()
        obj = scn.newObj("somehair")
        obj.x = position[0]
        obj.y = position[1]
        obj.z = position[2]
        obj.rx = rotation[0]
        obj.ry = rotation[1]
        obj.rz = rotation[2]
        obj.sx = 1.0
        obj.sy = 1.0
        obj.sz = 1.0
        obj.visibility = 1
        obj.shadeless = 0
        obj.pickable = 0
        obj.cameraMode = 0
        obj.text = ""
        obj.uvValues = []
        obj.indexBuffer = []
        fg = obj.createFaceGroup("ribbons")

        for guide in self.guides:
            loadStrands(obj,guide, self.widthFactor, 0.04)

        fg.setColor([0,0,0,255]) #rgba
        obj.calcNormals()
        obj.shadeless = 1
        obj.updateIndexBuffer()
        self.human.hairObj.update()
        self.human.hairObj = obj
        scn.update()


    def loadHair(self, path, res=0.04, update = True):
        scn = self.human.scene
        self.loadHairFile(path)        
        position = self.human.getPosition()
        rotation = self.human.getRotation()
        obj = scn.newObj(path)
        obj.x = position[0]
        obj.y = position[1]
        obj.z = position[2]
        obj.rx = rotation[0]
        obj.ry = rotation[1]
        obj.rz = rotation[2]
        obj.sx = 1.0
        obj.sy = 1.0
        obj.sz = 1.0
        obj.visibility = 1
        obj.shadeless = 0
        obj.pickable = 0
        obj.cameraMode = 0
        obj.text = ""
        obj.uvValues = []
        obj.indexBuffer = []
        fg = obj.createFaceGroup("ribbons")

        headNames = [group.name for group in self.human.meshData.faceGroups if ("head" in group.name or "jaw" in group.name or "nose" in group.name or "mouth" in group.name or "ear" in group.name or "eye" in group.name)]
        headVertices = self.human.meshData.getVerticesAndFacesForGroups(headNames)[0]

        headBB=calculateBoundingBox(headVertices)
        headCentroid = in2pts(headBB[0],headBB[1],0.5)
        delta = vsub(headCentroid,self.oHeadCentroid)
        scale = [1.0,1.0,1.0]
        scale[0] = (headBB[1][0]-headBB[0][0])/float(self.oHeadBoundingBox[1][0]-self.oHeadBoundingBox[0][0])
        scale[1] = (headBB[1][1]-headBB[0][1])/float(self.oHeadBoundingBox[1][1]-self.oHeadBoundingBox[0][1])
        scale[2] = (headBB[1][2]-headBB[0][2])/float(self.oHeadBoundingBox[1][2]-self.oHeadBoundingBox[0][2])

        for guide in self.guides:
            for cP in guide:
                #Translate
                cP[0] = cP[0] + delta[0]
                cP[1] = cP[1] + delta[1]
                cP[2] = cP[2] + delta[2]
                #Scale
                temp = cP #needed for shallow copy, as vsub and vadd methods disrupts the fun of shallow-copying
                temp = vsub(temp,headCentroid)
                temp = [temp[0]*scale[0],temp[1]*scale[1],temp[2]*scale[2]]
                temp = vadd(temp, headCentroid)
                cP[0]=temp[0]
                cP[1]=temp[1]
                cP[2]=temp[2]
            loadStrands(obj,guide, self.widthFactor, res)

        #HACK: set hair color to default black
        fg.setColor([0,0,0,255]) #rgba
        obj.calcNormals() # Do not recalculate normals for ribbons of hair, if there are lot of hairs this can be too expensive and for too curly hair our normal calc is not good
        obj.shadeless = 1
        obj.updateIndexBuffer()
        if update:
            scn.update()
        return obj
        
        

    def loadHairFile(self, name):
        try:
            name = path.splitext(name)[0]
            objFile = open(name + ".obj")
            #files = zipfile.ZipFile(name+".zip","r")
            #objFile = files.open(files.namelist()[0])
            fileDescriptor = open(name+".hair")
        except:
            log.error('Unable to load .obj and .hair file of %s', name)
            return
        
        #self.resetHairs()
        self.path = name
        for data in fileDescriptor:
            datalist = data.split()
            if datalist[0] == 'hairDiameterMultiStrand':
                self.hairDiameterMultiStrand = float(datalist[1])
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
        fileDescriptor.close()
        guidePoints=[]
        temp =[]
        self.guides = [] #set of curves
        self.grouping = {} #dictionary of list of guide indicesself.grouping 
        guideIndex=0
        for data in objFile:
            datalist = data.split()
            if datalist[0] == "v":
                for i in xrange(1,4):
                    datalist[i] = float(datalist[i])
                temp.append(datalist[1:])
            elif datalist[0] == "curv":
                for index in datalist[3:]:
                    guidePoints.append(temp[int(index)])
                temp=[]
            elif datalist[0] == "g":
                try:
                  self.grouping[datalist[1]].append(guideIndex)
                except:
                  self.grouping[datalist[1]]=[guideIndex]
                  """
                  print "Creating Hair Group: ", datalist[1]
                  print self.grouping
                  """
            elif datalist[0] == "end":
                #if guidePoints[0][1] < guidePoints[len(guidePoints)-1][1]: #is the first point lower than the last control point?
                #    guidePoints.reverse()
                guidePoints.reverse() #all hairs are exported from blender, blender particles start counting from hair tip not from hair root!
                self.guides.append(guidePoints); #apppend takes a deep copy
                guidePoints=[]
                guideIndex=guideIndex+1
        objFile.close()
        log.message("Loaded %s strands" % len(self.guides))

    def generateHairToRender(self):
        hairs = self.multiStrandInterpolation()
        hairs = hairs + self.guides
        if (self.clumpInterpolationNumber > 1):
            hairs = clumpInterpolation(hairs, self.interpolationRadius, self.clumpInterpolationNumber)
        #else:
        #    return hairs
        r = self.randomness
        for strand in hairs:
          for cp in strand:
            rx= r*random()
            ry= r*random()
            rz= r*random()
            cp=[cp[0]+rx, cp[1]+ry, cp[2]+rz]
        
        return hairs
        
            
    def multiStrandInterpolation(self):
       if self.multiStrandNumber<2: return []
       hairs=[]
       for group in self.grouping.values():
         n = len(group)
         if n==0: 
           continue
         for i in xrange(0,self.multiStrandNumber):
           
           #random point the convex hull
           tempStrand=[]
           weights=n*[0.0]
           mAx = randint(0,n-1)
           weights[mAx] = n*random() #fair distribution that doesn't cluster on the centroid
           temp = weights[mAx]
           for j in xrange(0,n):             
             if j!=mAx: 
              r=random()
              weights[j]  = r
              temp = temp + r
             #if weights[mAx] < r: mAx=j
           #normalize weight sum
           
           for j in xrange(0,n):
             weights[j]=weights[j]/temp
             
           m = len(self.guides[group[mAx]]) #length of strand with highest weight
           
           for j in xrange(0,m): #interpolated strand has controlPoints = controlPoint of the strand with heighest weight!
             tempV=[0.0,0.0,0.0]
             for k in xrange(0,n):
               index = min(j, len(self.guides[group[k]])-1)
               v = vmul(self.guides[group[k]][index],weights[k])
               tempV=vadd(tempV,v)
               
             tempStrand.append(tempV)
           hairs.append(tempStrand)
         
       log.message("%s generated hair through multistrand interpolation" % len(hairs))
       return hairs

def loadStrands(obj,curve,widthFactor=1.0,res=0.04):
    headNormal = [0.0,1.0,0.0]
    headCentroid = [0.0,7.8,0.4]
    fg = obj.faceGroups[0]
    cPs = [curve[0]]
    for i in xrange(2,len(curve)): #piecewise continuous polynomial
        d=vdist(curve[i],curve[i-1])+vdist(curve[i-1],curve[i-2])
        N=int(d/(res*4))
        for j in xrange(1,N):
            cPs.append(ThreeDQBspline(curve[i-2],curve[i-1],curve[i],j*res*4/d))
    cPs.append(curve[len(curve)-1])
    uvLength=len(cPs)-3
    if (uvLength<=0):
        return #neglects uv for strands with less than 4 control points
    uvFactor = 1.0/uvLength

    vtemp1, vtemp2 = None, None
    uvtemp1, uvtemp2 = None, None
    dist =  widthFactor*res/2
    for i in xrange(1,len(cPs)):
        cp1=cPs[i-1]
        cp2=cPs[i]
        verts=[[],[],[],[]]

        #compute ribbon plane
        if i==1:
            #trick to make normals face always outside the head
            vec = vmul(vnorm(vcross(vsub(headCentroid,cp2),vsub(cp1,cp2))), dist)
            verts[0] = vsub(cp1,vec)
            verts[1] = vadd(cp1,vec)
        else:
            verts[0]=v1[:]
            verts[1]=v2[:]

        verts[2]=vadd(cp2,vec)
        verts[3]=vsub(cp2,vec)

        v1=verts[3][:]
        v2=verts[2][:]

        #plain oc1rientation:
        # xy :  1 2      uv:   (0,v[j-1])  (1,v[j-1])
        #         4 3             (0,0)          (1,v[j])

        #please do not change the sequence of the lines here
        if vtemp1 == None:
            w1 = obj.createVertex([verts[0][0], verts[0][1], verts[0][2]])
            w2 = obj.createVertex([verts[1][0], verts[1][1], verts[1][2]])
            obj.uvValues.append([0.0,(uvLength - i+2)*uvFactor])
            obj.uvValues.append([1.0,(uvLength - i+2)*uvFactor])
        else:
            w1=vtemp1
            w2=vtemp2
        w3 = obj.createVertex([verts[2][0], verts[2][1], verts[2][2]])
        w4 = obj.createVertex([verts[3][0], verts[3][1], verts[3][2]])
        obj.uvValues.append([1.0,(uvLength - i+1)*uvFactor])
        obj.uvValues.append([0.0,(uvLength - i+1)*uvFactor])
        #end of please...

        #shallow copies used
        fg.createFace((w1, w4, w3, w2))
        fg.faces[len(fg.faces) -1].uv= [w1.idx,w4.idx,w3.idx,w2.idx]
        vtemp1=w4
        vtemp2=w3

#uses module3d vertex format!
def calculateBoundingBox(verts):
    boundingBox =  [verts[0].co[:],verts[0].co[:]]
    for v in verts:
        if v.co[0] < boundingBox[0][0]: #minX
            boundingBox[0][0] = v.co[0]
        if v.co[0] > boundingBox[1][0]: #maxX
            boundingBox[1][0] = v.co[0]
        if v.co[1] < boundingBox[0][1]: #minY
            boundingBox[0][1] = v.co[1]
        if v.co[1] > boundingBox[1][1]: #maxY
            boundingBox[1][1] = v.co[1]
        if v.co[2] < boundingBox[0][2]: #minZ
            boundingBox[0][2] = v.co[2]
        if v.co[2] > boundingBox[1][2]: #maxX
            boundingBox[1][2] = v.co[2]
    return boundingBox

def faceInterpolation(guides, scalp, n):
    """
    Suppose we have a scalp with faces and normal vector of them. We create a container for each face,
    each container will contain the guide hair attached to it (nearest neighbour thru guide roots and centroid of face).
    Once the container is created we, for each guide hair, choose a random face from the scalp. From this random face we
    choose a random guide attached to it. We then interpolate the given guide hair with this random guide on a random position
    on that particular random face we chose (having normal of that face).
    """
    hairs = []
    guideRoots = []
    for i in xrange(0,guides):
        guideRoots.append(guides[i])
    octree = SimpleOctree(guideRoots,0.09)
    container = []
    #for face in scalp:
    #for v in face:


#1 Create an octree of all guide roots
#2 Iterate thru all the gudes by i
#3 for guide i get n random colored leaf
#4 for each random colored leaf get a random guide
#5 interpolate between guide i and this random guide on that leaf.. normal should be that of random guide
def octreeInterpolation(guides, n):
    guideRoots = []
    for i in xrange(0,guides):
        guideRoots.append(guides[i])
    octree = SimpleOctree(guideRoots,0.09)
    hairs=[]
    for i in xrange(0,guides):
        hairs.append(guides[i])


# Clump-based interpolation :
# 1. A strand (guides ) is taken
# 2. The first and second control point determine a (normal) vector and a perpendicular plane
# 3. A circle is drawn on the perpendicular plane (with radius : radius)  with center othe first control point
# 4. n-hair strands paralel to the guide strand is created randumly within this radius of the plane.
def clumpInterpolation(guides, radius, n):
    hairs = []
    e = 1.0e-6
    for guide in guides:
        hairs.append(guide)
        if len(guide)<2 : continue
        v=[0.0,0.0,0.0]
        index = 0
        found = False

        while (not found) and index<len(guide): #precaution needed for very curly hair
            v = vnorm(vsub(guide[index],guide[0]))
            if vdot(v,v) > 1e-6 : found = True
            index = index + 1
        if not found:
            continue

        for i in xrange(0,n): #3,#4
            w = vmul(vnorm(randomPointFromNormal(v)), radius*random())
            child = []
            for j in xrange(0,len(guide)):
                child.append(vadd(guide[j],w))
            hairs.append(child)

    return hairs
