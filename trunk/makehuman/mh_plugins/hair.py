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
      self.app.scene3d.selectedHuman.setHairFile("data/hairs/" + filename)
      #Josenow: TODO load .obj hair into model!
      #Josenow: TODO collision detection button?
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
  obj.shadeless = 1
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
  
def loadHairsFile(scn, path,res=0.08):
  hairsClass = hairgenerator.Hairgenerator()
  hairsClass.loadHairs(path)
  for group in hairsClass.guideGroups:
      for guide in group.guides:
          for i in range(2,len(guide.controlPoints)-1):
              cp1=guide.controlPoints[i-1]
              cp2=guide.controlPoints[i]
              verts=[cp1[:],cp1[:],cp2[:],cp2[:]]
              verts[0][0]=cp1[0]-res/2
              verts[1][0]=cp1[0]+res/2
              verts[2][0]=cp2[0]+res/2
              verts[3][0]=cp2[0]-res/2
              drawQuad(scn,verts, "currentHair")
