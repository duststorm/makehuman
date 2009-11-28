""" 
Class for handling Render mode in the GUI.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements the 'guirender' class structures and methods to support GUI 
Render mode operations.
Render mode is invoked by selecting the Render mode icon from the main GUI control 
bar at the top of the screen. 
While in this mode, user actions (keyboard and mouse events) are passed into 
this class for processing. Having processed an event this class returns control to the 
main OpenGL/SDL/Application event handling loop.  

"""

__docformat__ = 'restructuredtext'

import files3d, gui3d, events3d
import mh2povray
import mh2renderman

class RenderingCategory(gui3d.Category):
  def __init__(self, parent):
    gui3d.Category.__init__(self, parent, "Rendering", parent.app.getThemeResource("images", "button_render.png"))
      
    povray = gui3d.TaskView(self, "Povray",  self.app.getThemeResource("images", "button_povray.png"))
    @povray.event
    def onShow(event):
      pass
    @povray.event
    def onHide(event):
      pass
    @povray.button.event
    def onClicked(event):
      reload(mh2povray)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
      for obj in self.app.scene3d.objects:
          # print "POV-Ray Export test: ", obj.name
          # Only process the humanoid figure
          if obj.name == "base.obj":
              cameraData = self.app.scene3d.getCameraSettings()
              mh2povray.povrayExport(obj, cameraData)
          
  def onShow(self, event):
    self.setFocus()
    gui3d.Category.onShow(self, event)
