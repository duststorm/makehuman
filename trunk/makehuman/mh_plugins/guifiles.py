# You may use, modify and redistribute this module under the terms of the GNU GPL.
""" 
Class for handling File mode in the GUI.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements the 'guifiles' class structures and methods to support GUI 
File mode operations.
File mode is invoked by selecting the File mode icon from the main GUI control bar at the top of
the screen. While in this mode, user actions (keyboard and mouse events) are passed into 
this class for processing. Having processed an event this class returns control to the 
main OpenGL/SDL/Application event handling loop.  

"""

__docformat__ = 'restructuredtext'

import files3d, animation3d, gui3d, events3d, os, mh2obj,  mh2bvh

class SaveTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Save",  "data/images/button_save_file.png")
    self.fileentry = gui3d.FileEntryView(self)

    @self.fileentry.event
    def onFileSelected(filename):
      if not os.path.exists("models"):
        os.mkdir("models")

      tags = filename
      filename = filename.split()[0]
      
      # Save the thumbnail
      leftTop = self.app.scene3d.convertToScreen(-10, 10, 0, 1)
      rightBottom = self.app.scene3d.convertToScreen(10, -9, 0, 1)
      self.app.scene3d.grabScreen(int(leftTop[0]), int(leftTop[1]), int(rightBottom[0] - leftTop[0]), int(rightBottom[1] - leftTop[1]), "models/" + filename + ".bmp")
      
      # Save the model
      human = self.app.scene3d.selectedHuman
      f = open("models/" + filename + ".mhm", 'w')
      f.write("# Written by makehuman 1.0.0 alpha 2\n")
      f.write("version 1.0.0\n")
      f.write("tags %s\n" %(tags))
      f.write("gender %f\n" %(human.getGender()))
      f.write("age %f\n" %(human.getAge()))
      f.write("muscle %f\n" %(human.getMuscle()))
      f.write("weight %f\n" %(human.getWeight()))
      for (target, value) in human.targetsEthnicStack.iteritems():
          f.write("ethnic %s %f\n" %(target, value))
              
      for t in human.targetsDetailStack.keys():
          if "/details/" in t:
              f.write("detail %s %f\n" %(os.path.basename(t).replace('.target', ''), human.targetsDetailStack[t]))
          elif  "/microdetails/" in t:
              f.write("microdetail %s %f\n" %(os.path.basename(t).replace('.target', ''), human.targetsDetailStack[t]))
      f.close()
      
      self.app.switchCategory("Modelling")
      self.app.scene3d.redraw(1)

  def onShow(self, event):
    # When the task gets shown, set the focus to the file entry
    gui3d.TaskView.onShow(self, event)
    self.fileentry.setFocus()
    self.pan = self.app.scene3d.getCameraTranslations()
    self.zoom = self.app.scene3d.getCameraZoom()
    self.rotation = self.app.scene3d.getCameraRotations()
    self.app.scene3d.setCameraTranslations(0, -1)
    self.app.scene3d.setCameraZoom(70.0)
    self.app.scene3d.setCameraRotations(0.0, 0.0)
    
  def onHide(self, event):
    gui3d.TaskView.onHide(self, event)
    self.app.scene3d.setCameraTranslations(self.pan[0], self.pan[1])
    self.app.scene3d.setCameraZoom(self.zoom)
    self.app.scene3d.setCameraRotations(self.rotation[0], self.rotation[1])

class LoadTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Load",  "data/images/button_load_file.png")
    self.filechooser = gui3d.FileChooser(self, "models", "mhm")
    
    @self.filechooser.event
    def onFileSelected(filename):
      print("Loading %s" %(filename))
        
      human = self.app.scene3d.selectedHuman
      human.resetMeshValues()
      
      # Load the model
      f = open("models/" + filename, 'r')
      
      for data in f.readlines():
          lineData = data.split()
          
          if len(lineData) > 0:
              if lineData[0] == "version":
                  print("Version " + lineData[1])
              elif lineData[0] == "tags":
                  for tag in lineData:
                    print("Tag " + tag)
              elif lineData[0] == "gender":
                  human.setGender(float(lineData[1]))
              elif lineData[0] == "age":
                  human.setAge(float(lineData[1]))
              elif lineData[0] == "muscle":
                  human.setMuscle(float(lineData[1]))
              elif lineData[0] == "weight":
                  human.setWeight(float(lineData[1]))
              elif lineData[0] == "ethnic":
                  human.targetsEthnicStack[lineData[1]] = float(lineData[2])
              elif lineData[0] == "detail":
                  human.targetsDetailStack["data/targets/details/" + lineData[1] + ".target"] = float(lineData[2])
              elif lineData[0] == "microdetail":
                  human.targetsDetailStack["data/targets/microdetails/" + lineData[1] + ".target"] = float(lineData[2])
              
      f.close()
      
      del human.targetsEthnicStack["neutral"]
      human.targetsEthnicStack["neutral"] = 1.0 - sum(human.targetsEthnicStack.values())
      
      self.app.categories["Modelling"].tasksByName["Macro modelling"].syncSliders()
      self.app.categories["Modelling"].tasksByName["Macro modelling"].syncEthnics()
              
      human.applyAllTargets()
      del self.app.undoStack[:]
      del self.app.redoStack[:]
      
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
    
class ExportTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Export",  "data/images/button_export_file.png")
    self.fileentry = gui3d.FileEntryView(self)

    @self.fileentry.event
    def onFileSelected(filename):
      if not os.path.exists("exports"):
        os.mkdir("exports")
        
      mh2obj.exportObj(self.app.scene3d.selectedHuman.meshData, "exports/" + filename + ".obj")
      mh2bvh.exportSkeleton(self.app.scene3d.selectedHuman.meshData, "exports/" + filename + ".bvh")
      
      self.app.switchCategory("Modelling")
      self.app.scene3d.redraw(1)
      
  def onShow(self, event):
    # When the task gets shown, set the focus to the file entry
    gui3d.TaskView.onShow(self, event)
    self.fileentry.setFocus()
    self.pan = self.app.scene3d.getCameraTranslations()
    self.zoom = self.app.scene3d.getCameraZoom()
    self.rotation = self.app.scene3d.getCameraRotations()
    self.app.scene3d.setCameraTranslations(0, -1)
    self.app.scene3d.setCameraZoom(70.0)
    self.app.scene3d.setCameraRotations(0.0, 0.0)
    
  def onHide(self, event):
    gui3d.TaskView.onHide(self, event)
    self.app.scene3d.setCameraTranslations(self.pan[0], self.pan[1])
    self.app.scene3d.setCameraZoom(self.zoom)
    self.app.scene3d.setCameraRotations(self.rotation[0], self.rotation[1])

class FilesCategory(gui3d.Category):
  def __init__(self, parent):
    gui3d.Category.__init__(self, parent, "Files", "data/images/button_loadsave.png")
    
    SaveTaskView(self)
    LoadTaskView(self)
    ExportTaskView(self)
    
