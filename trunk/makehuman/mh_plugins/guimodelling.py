"""
Module containing classes to handle modelling mode GUI operations.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements the 'guimodelling' class structures and methods to support GUI
Modelling mode operations.
Modelling mode is invoked by selecting the Modelling mode icon from the main GUI control
bar at the top of the screen.
While in this mode, user actions (keyboard and mouse events) are passed into
this class for processing. Having processed an event this class returns control to the
main OpenGL/SDL/Application event handling loop.


"""

__docformat__ = 'restructuredtext'

import events3d, gui3d, guimacromodelling, guidetailmodelling, mh2obj,  mh2bvh, os

class ModellingCategory(gui3d.Category):
    def __init__(self, parent):
      gui3d.Category.__init__(self,  parent, "Modelling", parent.app.getThemeResource("images", "button_home.png"))
      guimacromodelling.MacroModelingTaskView(self)
      guidetailmodelling.DetailModelingTaskView(self)
      guidetailmodelling.MicroModelingTaskView(self)
      gui3d.TaskView(self, "Anime modeling",  self.app.getThemeResource("images", "button_expressions.png"))
      
    # Rotate and pan the camera
    def onMouseDragged(self, event):
        diff = self.app.scene3d.getMouseDiff()
        leftButtonDown =event.button & 1
        middleButtonDown = event.button & 2
        rightButtonDown = event.button & 4

        if (leftButtonDown and rightButtonDown) or middleButtonDown:
            self.app.scene3d.setCameraZoom(self.app.scene3d.getCameraZoom() + 0.05 * diff[1])
        elif leftButtonDown:
            rot = self.app.scene3d.getCameraRotations()
            self.app.scene3d.setCameraRotations(rot[0] + 0.5 * diff[1], rot[1] + 0.5 * diff[0])
        elif rightButtonDown:
            trans = self.app.scene3d.getCameraTranslations()
            self.app.scene3d.setCameraTranslations(trans[0] + 0.05 * diff[0], trans[1] - 0.05 * diff[1])
        
    # Zoom the camera
    def onMouseWheel(self, event):
      if event.wheelDelta > 0:
        self.app.scene3d.setCameraZoom(self.app.scene3d.getCameraZoom() - 0.65)
        self.app.scene3d.redraw()
      else:
        self.app.scene3d.setCameraZoom(self.app.scene3d.getCameraZoom() + 0.65)
        self.app.scene3d.redraw()
        
    def onKeyDown(self, event):
      if not event.modifiers:
        # Camera rotation
        if event.key == events3d.SDLK_2 or event.key == events3d.SDLK_KP2:
          rot = self.app.scene3d.getCameraRotations()
          self.app.scene3d.setCameraRotations(rot[0] + 5.0, rot[1])
          self.app.scene3d.redraw()
        elif event.key == events3d.SDLK_4 or event.key == events3d.SDLK_KP4:
          rot = self.app.scene3d.getCameraRotations()
          self.app.scene3d.setCameraRotations(rot[0], rot[1] - 5.0)
          self.app.scene3d.redraw()
        elif event.key == events3d.SDLK_6 or event.key == events3d.SDLK_KP6:
          rot = self.app.scene3d.getCameraRotations()
          self.app.scene3d.setCameraRotations(rot[0], rot[1] + 5.0)
          self.app.scene3d.redraw()
        elif event.key == events3d.SDLK_8 or event.key == events3d.SDLK_KP8:
          rot = self.app.scene3d.getCameraRotations()
          self.app.scene3d.setCameraRotations(rot[0] - 5.0, rot[1])
          self.app.scene3d.redraw()
        # Camera pan
        elif event.key == events3d.SDLK_UP:
          trans = self.app.scene3d.getCameraTranslations()
          self.app.scene3d.setCameraTranslations(trans[0], trans[1] + 0.05)
          self.app.scene3d.redraw()
        elif event.key == events3d.SDLK_DOWN:
          trans = self.app.scene3d.getCameraTranslations()
          self.app.scene3d.setCameraTranslations(trans[0], trans[1] - 0.05)
          self.app.scene3d.redraw()
        elif event.key == events3d.SDLK_RIGHT:
          trans = self.app.scene3d.getCameraTranslations()
          self.app.scene3d.setCameraTranslations(trans[0] + 0.05, trans[1])
          self.app.scene3d.redraw()
        elif event.key == events3d.SDLK_LEFT:
          trans = self.app.scene3d.getCameraTranslations()
          self.app.scene3d.setCameraTranslations(trans[0] - 0.05, trans[1])
          self.app.scene3d.redraw()
        # Camera zoom
        elif event.key == events3d.SDLK_PLUS or event.key == events3d.SDLK_KP_PLUS:
          self.app.scene3d.setCameraZoom(self.app.scene3d.getCameraZoom() + 0.65)
          self.app.scene3d.redraw()
        elif event.key == events3d.SDLK_MINUS or event.key == events3d.SDLK_KP_MINUS:
          self.app.scene3d.setCameraZoom(self.app.scene3d.getCameraZoom() - 0.65)
          self.app.scene3d.redraw()
        # Camera views
        elif event.key == events3d.SDLK_7 or event.key == events3d.SDLK_KP7:
          self.app.scene3d.setCameraRotations(90.0, 0.0)
          self.app.scene3d.redraw()
        elif event.key == events3d.SDLK_1 or event.key == events3d.SDLK_KP1:
          self.app.scene3d.setCameraRotations(0.0, 0.0)
          self.app.scene3d.redraw()
        elif event.key == events3d.SDLK_3 or event.key == events3d.SDLK_KP3:
          self.app.scene3d.setCameraRotations(0.0, 90.0)
          self.app.scene3d.redraw()
        elif event.key == events3d.SDLK_PERIOD or event.key == events3d.SDLK_KP_PERIOD:
          self.app.scene3d.setCameraTranslations(0.0, 0.0)
          self.app.scene3d.setCameraZoom(60.0)
          self.app.scene3d.redraw()
        # Other keybindings
        elif event.key == events3d.SDLK_e:
            if not os.path.exists("exports"):
              os.mkdir("exports")
            mh2obj.exportObj(self.app.scene3d.selectedHuman.meshData, "exports/quick_export.obj")
            mh2bvh.exportSkeleton(self.app.scene3d.selectedHuman.meshData, "exports/quick_export.bvh")
        elif event.key == events3d.SDLK_g:
          self.app.scene3d.grabScreen(180, 80, 440, 440, "grab.bmp")
        elif event.key == events3d.SDLK_q:
          self.app.stop()
        elif event.key == events3d.SDLK_s:
            print("subdividing")
            self.app.scene3d.selectedHuman.subdivide()
        elif event.key == events3d.SDLK_y:
          self.app.redo()
        elif event.key == events3d.SDLK_z:
          self.app.undo()
        
      gui3d.Category.onKeyDown(self, event)
