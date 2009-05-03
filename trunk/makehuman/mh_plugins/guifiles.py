# You may use, modify and redistribute this module under the terms of the GNU GPL.
""" 
Class for handling File mode in the GUI.

===========================  ===============================================================  
Project Name:                **MakeHuman**                                                  
Module File Location:        mh_plugins/guifiles.py                                          
Product Home Page:           http://www.makehuman.org/                                      
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/                     
Authors:                     Manuel Bastioni                                            
Copyright(c):                MakeHuman Team 2001-2008                                       
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards  
===========================  ===============================================================  

This module implements the 'guifiles' class structures and methods to support GUI 
File mode operations.
File mode is invoked by selecting the File mode icon from the main GUI control bar at the top of
the screen. While in this mode, user actions (keyboard and mouse events) are passed into 
this class for processing. Having processed an event this class returns control to the 
main OpenGL/SDL/Application event handling loop.  

"""

__docformat__ = 'restructuredtext'

import files3d, animation3d, gui3d, os

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
      f.write("female %f\n" %(human.femaleVal))
      f.write("male %f\n" %(human.maleVal))
      f.write("child %f\n" %(human.childVal))
      f.write("old %f\n" %(human.oldVal))
      f.write("flaccid %f\n" %(human.flaccidVal))
      f.write("muscle %f\n" %(human.muscleVal))
      f.write("overweight %f\n" %(human.overweightVal))
      f.write("underweight %f\n" %(human.underweightVal))
      for (target, value) in human.targetsEthnicStack.iteritems():
          f.write("ethnic %s %f\n" %(target, value))
              
      for t in human.targetsDetailStack.keys():
          if "/details/" in t:
              f.write("detail %s %f\n" %(os.path.basename(t).replace('.target', ''), human.targetsDetailStack[t]))
          elif  "/microdetails/" in t:
              f.write("microdetail %s %f\n" %(os.path.basename(t).replace('.target', ''), human.targetsDetailStack[t]))
      f.close()
      
      self.app.switchCategory("modelling")
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
    self.filechooser = gui3d.FileChooser(self)
    
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
              elif lineData[0] == "female":
                  human.femaleVal = float(lineData[1])
              elif lineData[0] == "male":
                  human.maleVal = float(lineData[1])  
              elif lineData[0] == "child":
                  human.childVal = float(lineData[1])
              elif lineData[0] == "old":
                  human.oldVal = float(lineData[1])      
              elif lineData[0] == "flaccid":
                  human.flaccidVal = float(lineData[1])
              elif lineData[0] == "muscle":
                  human.muscleVal = float(lineData[1])
              elif lineData[0] == "overweight":
                  human.overweightVal = float(lineData[1])
              elif lineData[0] == "underweight":
                  human.underweightVal = float(lineData[1])
              elif lineData[0] == "ethnic":
                  human.targetsEthnicStack[lineData[1]] = float(lineData[2])
              elif lineData[0] == "detail":
                  human.targetsDetailStack["data/targets/details/" + lineData[1] + ".target"] = float(lineData[2])
              elif lineData[0] == "microdetail":
                  human.targetsDetailStack["data/targets/microdetails/" + lineData[1] + ".target"] = float(lineData[2])
              
      f.close()
      
      del human.targetsEthnicStack["neutral"]
      human.targetsEthnicStack["neutral"] = 1.0 - sum(human.targetsEthnicStack.values())
      
      self.app.categories["modelling"].tasksByName["Macro modelling"].syncSliders()
      self.app.categories["modelling"].tasksByName["Macro modelling"].syncEthnics()
              
      human.applyAllTargets()
      
      self.app.switchCategory("modelling")
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

class FilesCategory(gui3d.Category):
  def __init__(self, parent):
    gui3d.Category.__init__(self, parent, "Files", "data/images/button_loadsave.png")
    
    SaveTaskView(self)
    LoadTaskView(self)
    gui3d.TaskView(self, "Export",  "data/images/button_export_file.png")
    

            


