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

import gui3d, events3d, hairgenerator
from aljabr import *

class Hair(gui3d.Object):
  def __init__(self, globalScene, objFilePath):
    gui3d.Object.__init__(self, globalScene.application, objFilePath, position = [0, 0, 0], camera = 0, shadeless = 0, visible = True)

class HairTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Hair",  category.app.getThemeResource("images", "button_hair.png"))
    self.filechooser = gui3d.FileChooser(self, "data/hairs", "hair", "png")
    
    @self.filechooser.event
    def onFileSelected(filename):
      print("Loading %s" %(filename))
      #human = self.app.scene3d.selectedHuman
      human = self.app.scene3d.selectedHuman
      human.setHairFile("data/hairs/" + filename)    
      human.scene.clear(human.hairObj)
      hairsClass = hairgenerator.Hairgenerator()
      hairsClass.humanVerts = human.mesh.verts
      human.hairObj = loadHairsFile(human.scene, "./data/hairs/"+filename, position = self.app.scene3d.selectedHuman.getPosition(), rotation = self.app.scene3d.selectedHuman.getRotation(), hairsClass = hairsClass)
      #Jose: TODO collision detection
      self.app.categories["Modelling"].tasksByName["Macro modelling"].currentHair.setTexture(self.app.scene3d.selectedHuman.hairFile.replace(".hair", '.png'))
      self.app.switchCategory("Modelling")
      self.app.scene3d.redraw(1)
    
  def onShow(self, event):
    # When the task gets shown, set the focus to the file chooser
    self.app.scene3d.selectedHuman.hide()
    gui3d.TaskView.onShow(self, event)
    self.filechooser.setFocus()
    # HACK: otherwise the toolbar background disappears for some weird reason
    self.app.scene3d.redraw(0)
    
  def onHide(self, event):
    self.app.scene3d.selectedHuman.show()
    gui3d.TaskView.onHide(self, event)
  
#Draws a Quad
#TODO: account for world2local and viceversa
def drawQuad(scn, verts, name="quad", position=[0.0,0.0,0.0]):
  obj = scn.newObj(name)
  obj.x = position[0]
  obj.y = position[1]
  obj.z = position[2]
  obj.rx = 0.0
  obj.ry = 0.0
  obj.rz = 0.0
  obj.sx = 1.0
  obj.sy = 1.0
  obj.sz = 1.0
  obj.visibility = 1
  obj.shadeless = 0
  obj.pickable = 0
  obj.cameraMode = 0
  obj.text = ""
  #obj.uvValues = []
  obj.indexBuffer = []
  fg = obj.createFaceGroup("faces")
  
  # create vertices
  v1 = obj.createVertex([verts[0][0], verts[0][1], verts[0][2]])
  v2 = obj.createVertex([verts[1][0], verts[1][1], verts[1][2]])
  v3 = obj.createVertex([verts[2][0], verts[2][1], verts[2][2]])
  v4 = obj.createVertex([verts[3][0], verts[3][1], verts[3][2]])

  # create faces
  f1 = fg.createFace(v1, v4, v2)
  f2 = fg.createFace(v2, v4, v3)

  obj.updateIndexBuffer()
  scn.update()
  
def loadHairsFile(scn, path,res=0.08, position=[0.0,0.0,0.0], rotation=[0.0,0.0,0.0],  hairsClass = None):
  if hairsClass == None :
    hairsClass = hairgenerator.Hairgenerator()
  obj = scn.newObj(path)
  obj.x = position[0]
  obj.y = position[1]
  obj.z = position[2]
  obj.rx = rotation[0]
  obj.ry = rotation[1]
  obj.rz = rotation[2]
  #obj.rx = 0.0
  #obj.ry = 0.0
  #obj.rz = 0.0
  obj.sx = 1.0
  obj.sy = 1.0
  obj.sz = 1.0
  obj.visibility = 1
  obj.shadeless = 1
  obj.pickable = 0
  obj.cameraMode = 0
  obj.text = ""
  #obj.uvValues = []
  obj.indexBuffer = []
  fg = obj.createFaceGroup("ribbons")
  
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

  for group in hairsClass.guideGroups:
    for guide in group.guides:
        for i in range(2,len(guide.controlPoints)-1):
            cp1=guide.controlPoints[i-1]
            cp2=guide.controlPoints[i]
            verts=[[],[],[],[]]
            #compute ribbon plane
            vec = vmul(vnorm(vcross(headNormal, vsub(cp2,headCentroid))), res/2)
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
            w1 = obj.createVertex([verts[0][0], verts[0][1], verts[0][2]])
            w2 = obj.createVertex([verts[1][0], verts[1][1], verts[1][2]])
            w3 = obj.createVertex([verts[2][0], verts[2][1], verts[2][2]])
            w4 = obj.createVertex([verts[3][0], verts[3][1], verts[3][2]])
            fg.createFace(w1, w4, w2)
            fg.createFace(w2, w4, w3)

  #HACK: set hair color to default black 
  fg.setColor([0,0,0,255]) #rgba
  obj.updateIndexBuffer()
  scn.update()
  return obj
              