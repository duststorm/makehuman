"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010


**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TO DO

"""

__docformat__ = 'restructuredtext'

import gui3d, events3d, hairgenerator, guifiles, mh, os
from mh2obj import *
from module3d import drawQuad
from animation3d import ThreeDQBspline
from aljabr import *
from random import random
from math import radians
import os

class HairTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Hair",  category.app.getThemeResource("images", "button_hair.png"),  category.app.getThemeResource("images", "button_hair_on.png"))
    self.filechooser = gui3d.FileChooser(self, "data/hairs", "hair", "png")
    self.default = True
    self.hairsClass = hairgenerator.Hairgenerator() #this will have more points than the .hair file, as we will use curve interpolations on the controlpoints
    self.saveAsCurves = True
    self.widthFactor = 1.0
    self.oHeadCentroid = [0.0, 7.436, 0.03]
    self.oHeadBoundingBox = [[-0.84,6.409,-0.9862],[0.84,8.463,1.046]] 
    
    @self.filechooser.event
    def onFileSelected(filename,update=1):
      #hair files comes in pair, .obj and .hair.
      #.obj files contain geometric detail of the hair (can be edited by any 3rd party modelling software that opens wavefront .obj)
      #.hair files contain metadata of hair used by the makehair utility
      filename = os.path.splitext(filename)[0]
      print("Loading %s" %(filename))
      #human = self.app.scene3d.selectedHuman
      wFactor = self.app.categories["Modelling"].tasksByName["Hair"].widthSlider.getValue() 
      if (wFactor <= 100.00) and (wFactor >= 1.00): self.widthFactor = wFactor
      human = self.app.scene3d.selectedHuman
      if human.hairObj: human.scene.clear(human.hairObj)
      hairsClass = hairgenerator.Hairgenerator()
      hairsClass.humanVerts = human.mesh.verts
      human.hairObj = loadHairsFile(path="./data/hairs/"+filename, hairsClass=hairsClass, update=update)
      #human.hairObj = loadHairsFile(human.scene, path="./data/hairs/"+filename, position=self.app.scene3d.selectedHuman.getPosition(), rotation=self.app.scene3d.selectedHuman.getRotation(), hairsClass=hairsClass, update=update, widthFactor=self.widthFactor)
      #Jose: TODO collision detection
      self.app.categories["Modelling"].tasksByName["Macro modelling"].currentHair.setTexture(os.path.join('data/hairs', filename + '.png'))
      self.app.switchCategory("Modelling")
      human.setHairFile(os.path.join('data/hairs', filename + ".obj"))
      
    def loadHairsFile(path,res=0.04,  hairsClass = None, update = True):
    #scn, path,res=0.04, position=[0.0,0.0,0.0], rotation=[0.0,0.0,0.0],  hairsClass = None, update = True, widthFactor=1.0):
      human = self.app.scene3d.selectedHuman
      scn = human.scene
      position = human.getPosition()
      rotation = human.getRotation()
      widthFactor = self.widthFactor
      if hairsClass == None :
        hairsClass = hairgenerator.Hairgenerator()
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
      
      #temporary vectors    
      hairsClass.loadHairs(path)
      try: hairsClass.humanVerts
      except NameError: 
        print "No human vertices in hairsClass"
      """
      else: 
        hairsClass.adjustGuides()
        print "Hair adjusted"
      """
      headBB=calculateBoundingBox(human.headVertices)
      headCentroid = in2pts(headBB[0],headBB[1],0.5)
      delta = vsub(headCentroid,self.oHeadCentroid)
      scale = [1.0,1.0,1.0]
      scale[0] = (headBB[1][0]-headBB[0][0])/float(self.oHeadBoundingBox[1][0]-self.oHeadBoundingBox[0][0])
      scale[1] = (headBB[1][1]-headBB[0][1])/float(self.oHeadBoundingBox[1][1]-self.oHeadBoundingBox[0][1])
      scale[2] = (headBB[1][2]-headBB[0][2])/float(self.oHeadBoundingBox[1][2]-self.oHeadBoundingBox[0][2])
      #for group in hairsClass.guideGroups:
      for guide in hairsClass.guides:
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
        loadStrands(obj,guide, widthFactor, res)

        
      #HACK: set hair color to default black 
      fg.setColor([0,0,0,255]) #rgba
      obj.calcNormals()
      obj.shadeless = 1
      obj.updateIndexBuffer()
      if update:
          scn.update()
      return obj

    

  def onShow(self, event):
    # When the task gets shown, set the focus to the file chooser
    self.app.scene3d.selectedHuman.hide()
    if self.default:
      self.default = False
      self.filechooser.selectedFile = self.filechooser.files.index("default.hair")
      self.filechooser.onShow(event) 
    gui3d.TaskView.onShow(self, event)
    self.filechooser.setFocus()
    
  def onHide(self, event):
    self.app.scene3d.selectedHuman.show()
    gui3d.TaskView.onHide(self, event)
    
              
def loadStrands(obj,curve,widthFactor=1.0,res=0.04):
      headNormal = [0.0,1.0,0.0]
      headCentroid = [0.0,7.8,0.4]
      fg = obj.facesGroups[0]
      cPs = [curve[0]]
      for i in xrange(2,len(curve)-1): #piecewise continuous polynomial
        d1=vdist(curve[i-1],curve[i-2])
        d=d1+vdist(curve[i-1],curve[i])
        if i==len(curve)-1: N=int(d1/(res*4))
        else: N=int(d/(res*4))
        for j in xrange(1,N+1):
          if j==N and i==len(curve)-1 : cPs.append(curve[i-1])
          else: cPs.append(ThreeDQBspline(curve[i-2],curve[i-1],\
                           curve[i],j*res*4/d))
      uvLength=len(cPs)-3
      if (uvLength<=0): return #neglects uv for strands with less than 4 control points
      uvFactor = 1.0/uvLength 
      
      vtemp1, vtemp2 = None, None
      uvtemp1, uvtemp2 = None, None
      dist =  widthFactor*res/2
      for i in xrange(2,len(cPs)-1):
          cp1=cPs[i-1]
          cp2=cPs[i]
          verts=[[],[],[],[]]
          
          #compute ribbon plane
          #vec = vmul(vnorm(vcross(vsub(cp2,cp1), vsub(cp2,headCentroid))), dist)
          if i==2:
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
          
          #plain orientation:
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
          fg.createFace(w1, w4, w2)
          fg.faces[len(fg.faces) -1].uv= [w1.idx,w4.idx,w2.idx]
          fg.createFace(w2, w4, w3)
          fg.faces[len(fg.faces) -1].uv=[w2.idx,w4.idx,w3.idx]
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

# - out : populated hairsClass
def adjustHair(human, hairsClass):
    oHeadCentroid = [0.0, 7.436, 0.03]
    oHeadBoundingBox = [[-0.84,6.409,-0.9862],[0.84,8.463,1.046]] 
    hairsClass.loadHairs(human.hairFile)
    headBB=calculateBoundingBox(human.headVertices)
    headCentroid = in2pts(headBB[0],headBB[1],0.5)
    delta = vsub(headCentroid,oHeadCentroid)
    scale = [1.0,1.0,1.0]
    scale[0] = (headBB[1][0]-headBB[0][0])/float(oHeadBoundingBox[1][0]-oHeadBoundingBox[0][0])
    scale[1] = (headBB[1][1]-headBB[0][1])/float(oHeadBoundingBox[1][1]-oHeadBoundingBox[0][1])
    scale[2] = (headBB[1][2]-headBB[0][2])/float(oHeadBoundingBox[1][2]-oHeadBoundingBox[0][2])
    #for group in hairsClass.guideGroups:
    for guide in hairsClass.guides: #hairsClass.guideGroups[group]:
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
