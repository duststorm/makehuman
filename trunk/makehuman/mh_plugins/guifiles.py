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

import mh, files3d, animation3d, gui3d, events3d, os, mh2obj, mh2bvh, mh2mhx, humanmodifier

class SaveTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Save",  category.app.getThemeResource("images", "button_save_file.png"))
    self.fileentry = gui3d.FileEntryView(self)

    @self.fileentry.event
    def onFileSelected(filename):
      modelPath = mh.getPath("models")
      if not os.path.exists(modelPath):
        os.mkdir(modelPath)

      tags = filename
      filename = filename.split()[0]
      
      # Save the thumbnail
      leftTop = mh.cameras[0].convertToScreen(-10, 9, 0)
      rightBottom = mh.cameras[0].convertToScreen(10, -10, 0)
      self.app.scene3d.grabScreen(int(leftTop[0]), int(leftTop[1]), int(rightBottom[0] - leftTop[0]), int(rightBottom[1] - leftTop[1]), modelPath + "/" + filename + ".bmp")
      
      # Save the model
      human = self.app.scene3d.selectedHuman
      human.save(modelPath + "/" + filename + ".mhm", tags)
      
      self.app.switchCategory("Modelling")
      self.app.scene3d.redraw(1)

  def onShow(self, event):
    # When the task gets shown, set the focus to the file entry
    gui3d.TaskView.onShow(self, event)
    self.fileentry.setFocus()
    self.pan = self.app.scene3d.selectedHuman.getPosition()
    self.zoom = mh.cameras[0].zoom
    self.rotation = self.app.scene3d.selectedHuman.getRotation()
    self.app.scene3d.selectedHuman.setPosition([0, -1, 0])
    mh.cameras[0].zoom = 70.0
    self.app.scene3d.selectedHuman.setRotation([0.0, 0.0, 0.0])
    
  def onHide(self, event):
    gui3d.TaskView.onHide(self, event)
    self.app.scene3d.selectedHuman.setPosition(self.pan)
    mh.cameras[0].zoom = self.zoom
    self.app.scene3d.selectedHuman.setRotation(self.rotation)

class LoadTaskView(gui3d.TaskView):
  def __init__(self, category):
    modelPath = mh.getPath("models")
    gui3d.TaskView.__init__(self, category, "Load",  category.app.getThemeResource("images", "button_load_file.png"))
    self.filechooser = gui3d.FileChooser(self, modelPath, "mhm")
    
    @self.filechooser.event
    def onFileSelected(filename):
      print("Loading %s" %(filename))
        
      human = self.app.scene3d.selectedHuman
      
      human.load(modelPath + "/" + filename, self.app.progress)
      
      self.app.categories["Modelling"].tasksByName["Macro modelling"].syncSliders()
      self.app.categories["Modelling"].tasksByName["Macro modelling"].syncEthnics()
      self.app.categories["Modelling"].tasksByName["Macro modelling"].syncStatus()
              
      del self.app.undoStack[:]
      del self.app.redoStack[:]
      
      self.parent.tasksByName["Save"].fileentry.text = filename.replace(".mhm", "")
      self.parent.tasksByName["Save"].fileentry.textObject.setText(filename.replace(".mhm", ""))
      
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
    gui3d.TaskView.__init__(self, category, "Export",  category.app.getThemeResource("images", "button_export_file.png"))
    self.fileentry = gui3d.FileEntryView(self)

    @self.fileentry.event
    def onFileSelected(filename):
      exportPath = mh.getPath("exports")

      if not os.path.exists(exportPath):
        os.mkdir(exportPath)
        
      mh2obj.exportObj(self.app.scene3d.selectedHuman.meshData, exportPath + "/" + filename + ".obj")
      mh2bvh.exportSkeleton(self.app.scene3d.selectedHuman.meshData, exportPath + "/" + filename + ".bvh")
      mh2mhx.exportMhx(self.app.scene3d.selectedHuman.meshData, exportPath + "/" + filename + ".mhx")
      
      self.app.switchCategory("Modelling")
      self.app.scene3d.redraw(1)
      
  def onShow(self, event):
    # When the task gets shown, set the focus to the file entry
    gui3d.TaskView.onShow(self, event)
    self.fileentry.setFocus()
    self.pan = self.app.scene3d.selectedHuman.getPosition()
    self.zoom = mh.cameras[0].zoom
    self.rotation = self.app.scene3d.selectedHuman.getRotation()
    self.app.scene3d.selectedHuman.setPosition([0, -1, 0])
    mh.cameras[0].zoom = 70.0
    self.app.scene3d.selectedHuman.setRotation([0.0, 0.0, 0.0])
    
  def onHide(self, event):
    gui3d.TaskView.onHide(self, event)
    self.app.scene3d.selectedHuman.setPosition(self.pan)
    mh.cameras[0].zoom = self.zoom
    self.app.scene3d.selectedHuman.setRotation(self.rotation)

class FilesCategory(gui3d.Category):
  def __init__(self, parent):
    gui3d.Category.__init__(self, parent, "Files", parent.app.getThemeResource("images", "button_loadsave.png"))
    
    SaveTaskView(self)
    LoadTaskView(self)
    ExportTaskView(self)
    
