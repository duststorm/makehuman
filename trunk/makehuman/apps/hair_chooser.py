"""
B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Manuel Bastioni, Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2010

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

TO DO

"""

#import zipfile
import gui3d, events3d, guifiles, mh, os
from mh2obj import *
from module3d import drawQuad
from animation3d import ThreeDQBspline
from aljabr import *
from math import radians
from os import path
from random import random
from simpleoctree import SimpleOctree

class HairTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Hair",  category.app.getThemeResource("images", "button_hair.png"),  category.app.getThemeResource("images", "button_hair_on.png"))
    self.filechooser = gui3d.FileChooser(self, "data/hairs", "hair", "png")
    self.default = True
    self.saveAsCurves = True
    self.path = None
    self.guides = []
    self.widthFactor = 1.0
    self.oHeadCentroid = [0.0, 7.436, 0.03]
    self.oHeadBoundingBox = [[-0.84,6.409,-0.9862],[0.84,8.463,1.046]]
    self.hairDiameterMultiStrand = 0.006
    self.tipColor = [0.518, 0.325, 0.125]
    self.rootColor = [0.109, 0.037, 0.007]
    self.interpolationRadius = 0.09
    self.clumpInterpolationNumber = 0
    #self.app.categories["Rendering"].hairsClass = self

    @self.filechooser.event
    def onFileSelected(filename,update=1):
      #hair files comes in pair, .obj and .hair.
      #.obj files contain geometric detail of the hair (can be edited by any 3rd party modelling software that opens wavefront .obj)
      #.hair files contain metadata of hair used by the makehair utility
      filename = path.splitext(filename)[0]
      print("Loading %s" %(filename))
      #human = self.app.scene3d.selectedHuman
      #wFactor = self.app.categories["Modelling"].tasksByName["Hair"].widthSlider.getValue()
      #if (wFactor <= 100.00) and (wFactor >= 1.00): self.widthFactor = wFactor
      human = self.app.scene3d.selectedHuman
      if human.hairObj: human.scene.clear(human.hairObj)

      #human.hairObj = self.loadHair(path="./data/hairs/"+filename, update=update)
      human.hairObj = human.hairs.loadHair(path="./data/hairs/"+filename, update=update)
      
      #self.app.categories["Modelling"].tasksByName["Macro modelling"].currentHair.setTexture(path.join('data/hairs', filename + '.png'))
      self.app.switchCategory("Modelling")
      human.setHairFile(path.join('data/hairs', filename + ".obj"))  


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


