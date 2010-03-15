""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009


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

class HairTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Hair",  category.app.getThemeResource("images", "button_hair.png"),  category.app.getThemeResource("images", "button_hair_on.png"))
    self.filechooser = gui3d.FileChooser(self, "data/hairs", "hair", "png")
    self.default = True
    #self.filechooser.selectedFile = 1 #This is where default.hair is located :P .. bad HACK need to improve on this, maybe a hashtable?.. TODO for marc :P
    #self.hairsClass = hairgenerator.Hairgenerator() #this will have more points than the .hair file, as we will use curve interpolations on the controlpoints
    self.saveAsCurves = True
    self.widthFactor = 1.0
    self.Delta=None
 
    #filename textbox
    self.TextEdit = gui3d.TextEdit(self, mesh='data/3dobjs/backgroundedit.obj', position=[20, 480, 9])
    self.TextEdit.setText('saved_hair.obj')
    self.refVector=None #reference vector used for fast updating of hair (e.g. when base model only changes height or age)
    #Save Button
    self.Button = gui3d.Button(self, mesh='data/3dobjs/button_standard_big.obj',\
                    texture=category.app.getThemeResource("images", "button_save_file.png"),\
                    selectedTexture=None, position=[470, 490, 9])
    #self.Button.button.setScale(1.0,5.0)
    
    #.obj save type Radiobuttons
    self.RadioButtonGroup = []
    self.RadioButton1 = gui3d.RadioButton(self, self.RadioButtonGroup, mesh='data/3dobjs/slider_cursor.obj',\
                          texture=category.app.getThemeResource('images','slider.png'),\
                          selectedTexture=category.app.getThemeResource('images', 'slider_focused.png'),\
                          position=[200,510, 9], selected=True)  # We make the first one selected
    self.RadioButtonLabel1 = gui3d.TextView(self, mesh='data/3dobjs/empty.obj', position=[220, 520, 9])
    self.RadioButtonLabel1.setText('Save hairs to Wavefront .obj as Curves')
    self.RadioButton2 = gui3d.RadioButton(self, self.RadioButtonGroup, mesh='data/3dobjs/slider_cursor.obj',\
                          texture=category.app.getThemeResource('images','slider.png'),\
                          selectedTexture=category.app.getThemeResource('images', 'slider_focused.png'),\
                          position=[200,530, 9])
    self.RadioButtonLabel2 = gui3d.TextView(self, mesh='data/3dobjs/empty.obj', position=[220, 540, 9])
    self.RadioButtonLabel2.setText('Save hairs to Wavefront .obj as Mesh')

    @self.Button.event
    def onClicked(event):
      if len(self.TextEdit.text) >= 1 and len(hairsClass.guideGroups)> 0:
        modelPath = mh.getPath('models')
        if not os.path.exists(modelPath): os.makedirs(modelPath)
        if self.RadioButton1.selected:
          hairsClass = hairgenerator.Hairgenerator()
          hairsClass.humanVerts = self.app.scene3d.selectedHuman.mesh.verts
          hairsClass.loadHairs(self.app.scene3d.selectedHuman.hairFile)
          hairsClass.adjustGuides()
          file = open(modelPath+"/"+self.TextEdit.text, 'w')
          exportAsCurves(file, hairsClass.guideGroups)
          file.close()
        else:
          exportObj(self.app.scene3d.selectedHuman.hairObj,modelPath+"/"+self.TextEdit.text)
    
    @self.filechooser.event
    def onFileSelected(filename,update=1):
      print("Loading %s" %(filename))
      #human = self.app.scene3d.selectedHuman
      wFactor = self.app.categories["Modelling"].tasksByName["Hair"].widthSlider.getValue() 
      if (wFactor <= 100.00) and (wFactor >= 1.00): self.widthFactor = wFactor
      human = self.app.scene3d.selectedHuman
      human.setHairFile("data/hairs/" + filename)    
      print "Debug: Filename.. ", filename
      human.scene.clear(human.hairObj)
      hairsClass = hairgenerator.Hairgenerator()
      hairsClass.humanVerts = human.mesh.verts
      L = loadHairsFile(human.scene, path="./data/hairs/"+filename, position=self.app.scene3d.selectedHuman.getPosition(), rotation=self.app.scene3d.selectedHuman.getRotation(), hairsClass=hairsClass, update=update, widthFactor=self.widthFactor)
      if self.refVector==None: self.refVector=L[1]
      self.Delta = L[2]
      human.hairObj=L[0]
      #Jose: TODO collision detection
      self.app.categories["Modelling"].tasksByName["Macro modelling"].currentHair.setTexture(self.app.scene3d.selectedHuman.hairFile.replace(".hair", '.png'))
      self.app.switchCategory("Modelling")
      #self.app.scene3d.redraw(update)
    
  def onShow(self, event):
    # When the task gets shown, set the focus to the file chooser
    self.app.scene3d.selectedHuman.hide()
    if self.default:
      self.default = False
      self.filechooser.selectedFile = self.filechooser.files.index("default.hair")
      self.filechooser.onShow(event) #If I dont do this, first time libraries are chosen the wrong selectedFile is shown.. TODO: marc, make eleganter :P
      #print "Debug: ", self.filechooser.selectedFile
      #print "Debug: ", self.filechooser.files
    gui3d.TaskView.onShow(self, event)
    self.filechooser.setFocus()
    # HACK: otherwise the toolbar background disappears for some weird reason
    self.app.scene3d.redraw(0)
    
  def onHide(self, event):
    self.app.scene3d.selectedHuman.show()
    gui3d.TaskView.onHide(self, event)
  
"""  
  #Note: Does not update!
  #Suggestion: Updates of objects should be done manually!
  #No rotation (e.g. different pose) change assumed on base head! only translation and scales
  def adjustHairObj(self, hairObj, humanObj): #luckily both normal and vertex index of object remains the same!
    v=humanObj.verts[int(self.Delta[0])].co[:]
    v[0]=v[0] + float(self.Delta[1])
    v[1]=v[1] + float(self.Delta[2])
    v[2]=v[2] + float(self.Delta[2])
    delta = vsub(v,self.refVector)
    for i in range(len(hairObj.verts)):
       hairObj.verts[i].co = vadd(hairObj.verts[i].co,delta)
    self.refVector=vadd(self.refVector,delta)
"""
    
def loadHairsFile(scn, path,res=0.04, position=[0.0,0.0,0.0], rotation=[0.0,0.0,0.0],  hairsClass = None, update = True, widthFactor=1.0):
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
  refVector=None
  
  #temporary vectors
  headNormal = [0.0,1.0,0.0]
  headCentroid = [0.0,7.8,0.4]
    
  hairsClass.loadHairs(path)
  try: hairsClass.humanVerts
  except NameError: 
    print "No human vertices in hairsClass"
  else: 
    hairsClass.adjustGuides()
    print "Hair adjusted"
  
  Delta = hairsClass.Delta
  for group in hairsClass.guideGroups:
    for guide in group.guides:
      cPs = [guide.controlPoints[0]]
      if refVector == None : refVector = guide.controlPoints[0][:]
      for i in xrange(2,len(guide.controlPoints)-1): #piecewise continuous polynomial
        d1=vdist(guide.controlPoints[i-1],guide.controlPoints[i-2])
        d=d1+vdist(guide.controlPoints[i-1],guide.controlPoints[i])
        if i==len(guide.controlPoints)-1: N=int(d1/(res*4))
        else: N=int(d/(res*4))
        for j in xrange(1,N+1):
          if j==N and i==len(guide.controlPoints)-1 : cPs.append(guide.controlPoints[i-1])
          else: cPs.append(ThreeDQBspline(guide.controlPoints[i-2],guide.controlPoints[i-1],\
                           guide.controlPoints[i],j*res*4/d))
      uvFactor = 1.0/(len(cPs) -3) #here obviously guides must have ctrlPts  > 4!
      uvLength=len(cPs)-3
      vtemp1, vtemp2 = None, None
      uvtemp1, uvtemp2 = None, None
      dist =  widthFactor*res/2
      for i in xrange(2,len(cPs)-1):
          cp1=cPs[i-1]
          cp2=cPs[i]
          verts=[[],[],[],[]]
          
          #compute ribbon plane
          vec = vmul(vnorm(vcross(headNormal, vsub(cp2,headCentroid))), dist)
          if i==2:
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

  #HACK: set hair color to default black 
  fg.setColor([0,0,0,255]) #rgba
  obj.updateIndexBuffer()
  obj.calcNormals()
  obj.shadeless = 1 
  if update:
      scn.update()
  return obj,refVector,Delta
              
def exportAsCurves(file, guideGroups):
  DEG_ORDER_U = 3
  # use negative indices
  for group in guideGroups:
    for guide in group.guides:
      N = len(guide.controlPoints)
      for i in xrange(0,N):
        file.write('v %.6f %.6f %.6f\n' % (guide.controlPoints[i][0], guide.controlPoints[i][1],\
                                           guide.controlPoints[i][2]))
      name = group.name+"_"+guide.name 
      file.write('g %s\n' % name)
      file.write('cstype bspline\n') # not ideal, hard coded
      file.write('deg %d\n' % DEG_ORDER_U) # not used for curves but most files have it still

      curve_ls = [-(i+1) for i in xrange(N)]
      file.write('curv 0.0 1.0 %s\n' % (' '.join( [str(i) for i in curve_ls] ))) # hair  has no U and V values for the curve

      # 'parm' keyword
      tot_parm = (DEG_ORDER_U + 1) + N
      tot_parm_div = float(tot_parm-1)
      parm_ls = [(i/tot_parm_div) for i in xrange(tot_parm)]
      #our hairs dont do endpoints.. *sigh*
      file.write('parm u %s\n' % ' '.join( [str(i) for i in parm_ls] ))

      file.write('end\n')