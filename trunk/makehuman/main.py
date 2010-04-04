"""
The main MakeHuman Python Application file.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This is the main MakeHuman Python Application file which participates in the
application startup process. It contains functions that respond to events
affecting the main GUI toolbar along the top of the screen in all modes to
support switching between modes.

When the MakeHuman application is launched the *main* function from the C
application file *main.c* runs. This creates an integration layer by
dynamically generating a Python module (called 'mh'). That *main* function
then either imports this Python *main* module or executes this Python
script *main.py* (depending on platform).

This script displays a splash screen and a progress bar as it loads the
initial 3D humanoid model (the neutral base object) and adds the various
GUI sections into the scene. It creates the main toolbar that enables the
user to switch between different GUI modes and defines functions to
perform that switch for all active buttons. Active buttons are connected
to these functions by being registered to receive events.

At the end of the initiation process the splash screen is hidden and
Modelling mode is activated. The 'startEventLoop' method on the main Scene3D
object is invoked to call the OpenGL/SDL C functions that manage the
low-level event loop.

This Python module responds to high-level GUI toolbar events to switch
between different GUI modes, but otherwise events are handled by GUI mode
specific Python modules.

"""

__docformat__ = 'restructuredtext'

import sys
#print sys.builtin_module_names
#if 'nt' in sys.builtin_module_names:
sys.path.append("./pythonmodules")
import mh
import os
import subprocess
import webbrowser
import glob, imp
from os.path import join, basename, splitext

sys.path.append("./")
sys.path.append("./mh_plugins")
sys.path.append("./mh_core")

import gui3d, events3d
import human, hair, background
import guimodelling, guifiles, guirender
#import font3d

class Settings:
    def __init__():
        pass

class MHApplication(gui3d.Application):
  def __init__(self):
    gui3d.Application.__init__(self)

    modelCamera = mh.Camera()

    mh.cameras.append(modelCamera)

    guiCamera = mh.Camera()
    guiCamera.fovAngle = 45
    guiCamera.zoom = 10
    guiCamera.projection = 0
    mh.cameras.append(guiCamera)

    self.setTheme("default")
    
    self.settings = Settings
    self.settings.realtimeUpdates = True
    self.settings.realtimeNormalUpdates = True

    # Display the initial splash screen and the progress bar during startup
    self.splash = gui3d.Object(self, "data/3dobjs/splash.obj", self.getThemeResource("images", "splash.png"), position = [0, 0, 0])
    self.progressBar = gui3d.ProgressBar(self, backgroundTexture = self.getThemeResource("images", "progressbar_background.png"),
      barTexture = self.getThemeResource("images", "progressbar.png"))
    self.scene3d.update()
    self.scene3d.redraw(0)

    self.progressBar.setProgress(0.2)

    gui3d.Object(self, "data/3dobjs/upperbar.obj", self.getThemeResource("images", "upperbar.png"), [0, 0, 9])
    gui3d.Object(self, "data/3dobjs/backgroundbox.obj", position = [0, 0, -89.99])
    gui3d.Object(self, "data/3dobjs/lowerbar.obj", self.getThemeResource("images", "lowerbar.png"), [0, 32, 9])
    gui3d.Object(self, "data/3dobjs/lowerbar2.obj", self.getThemeResource("images", "lowerbar2.png"), [0, 568, 9])

    self.progressBar.setProgress(0.3)
    hairObj = hair.loadHairsFile(self.scene3d, path="./data/hairs/default.hair", update = False)
    #self.scene3d.clear(hairObj)
    self.scene3d.selectedHuman = human.Human(self.scene3d, "data/3dobjs/base.obj", hairObj)
    self.scene3d.selectedHuman.setTexture("data/textures/texture.tif")
    self.progressBar.setProgress(0.6)

    self.tool = None
    self.selectedGroup = None

    self.undoStack = []
    self.redoStack = []

    @self.scene3d.selectedHuman.event
    def onMouseDown(event):
      if self.tool:
        self.selectedGroup = self.app.scene3d.getSelectedFacesGroup()
        self.tool.callEvent("onMouseDown", event)
      else:
        self.currentTask.callEvent("onMouseDown", event)

    @self.scene3d.selectedHuman.event
    def onMouseMoved(event):
      if self.tool:
        self.tool.callEvent("onMouseMoved", event)
      else:
        self.currentTask.callEvent("onMouseMoved", event)

    @self.scene3d.selectedHuman.event
    def onMouseDragged(event):
      if self.tool:
        self.tool.callEvent("onMouseDragged", event)
      else:
        self.currentTask.callEvent("onMouseDragged", event)

    @self.scene3d.selectedHuman.event
    def onMouseUp(event):
      if self.tool:
        self.tool.callEvent("onMouseUp", event)
      else:
        self.currentTask.callEvent("onMouseUp", event)

    @self.scene3d.selectedHuman.event
    def onMouseEntered(event):
      if self.tool:
        self.tool.callEvent("onMouseEntered", event)
      else:
        self.currentTask.callEvent("onMouseEntered", event)

    @self.scene3d.selectedHuman.event
    def onMouseExited(event):
      if self.tool:
        self.tool.callEvent("onMouseExited", event)
      else:
        self.currentTask.callEvent("onMouseExited", event)

    # Set up categories and tasks
    
    guimodelling.ModellingCategory(self)
    self.progressBar.setProgress(0.7)
    guifiles.FilesCategory(self)
    self.progressBar.setProgress(0.8)
    guirender.RenderingCategory(self)

    library = gui3d.Category(self, "Library", self.getThemeResource("images", "button_library.png"),
      self.getThemeResource("images", "button_library_on.png"))
    hair.HairTaskView(library)
    background.BackgroundTaskView(library)

    # Load plugins not starting with _
    self.modules = {}
    for path in glob.glob(join("plugins/",'[!_]*.py')):
        name, ext = splitext(basename(path))
        module = imp.load_source(name, path)
        self.modules[name] = module
        module.load(self)

    category = gui3d.Category(self, "Help", self.getThemeResource("images", "button_about.png"),
      self.getThemeResource("images", "button_about_on.png"))
    # Help button
    @category.button.event
    def onClicked(event):
      webbrowser.open(os.getcwd()+"/docs/MH_Users_Guide.pdf");
      
    # Exit button
    category = gui3d.Category(self, "Exit", self.getThemeResource("images", "button_exit.png"),
      self.getThemeResource("images", "button_exit_on.png"))
    @category.button.event
    def onClicked(event):
      self.stop()

    self.switchCategory("Modelling")

    self.progressBar.setProgress(1.0)
    self.progressBar.hide()
    
    #font = font3d.Font("data/fonts/arial.fnt")
    #font3d.createMesh(self.scene3d, font, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", [60, 540, 9.6]);

  def onStart(self, event):
      self.splash.hide()
      self.scene3d.selectedHuman.applyAllTargets(self.app.progress)
      mh.updatePickingBuffer();

  def onKeyDown(self, event):
    if event.modifiers & events3d.KMOD_CTRL:
      if event.key == events3d.SDLK_m:
          self.app.switchCategory("Modelling")
          self.app.scene3d.redraw()
      elif event.key == events3d.SDLK_s:
          self.app.switchCategory("Files")
          self.app.switchTask("Save")
          self.app.scene3d.redraw()
      elif event.key == events3d.SDLK_l:
          self.app.switchCategory("Files")
          self.app.switchTask("Load")
      elif event.key == events3d.SDLK_e:
          self.app.switchCategory("Files")
          self.app.switchTask("Export")
          self.app.scene3d.redraw()
      elif event.key == events3d.SDLK_r:
          self.app.switchCategory("Rendering")
          self.app.scene3d.redraw()
      elif event.key == events3d.SDLK_q:
          self.app.scene3d.shutdown()
      elif event.key == events3d.SDLK_h:
          webbrowser.open(os.getcwd()+"/docs/MH_Users_Guide.pdf");
      elif event.key == events3d.SDLK_w:
          stereoMode = mh.cameras[0].stereoMode
          stereoMode += 1
          if stereoMode > 2:
            stereoMode = 0
          mh.cameras[0].stereoMode = stereoMode

          # We need a black background for stereo
          background = self.app.categories["Modelling"].tasksByName["Macro modelling"].background
          if stereoMode:
            color = [  0,   0,   0, 255]
          else:
            color = [100, 100, 100, 255]
          for g in background.mesh.facesGroups:
            g.setColor(color)

          self.app.scene3d.redraw()

  def do(self, action):
    if action.do():
      self.undoStack.append(action)
      del self.redoStack[:]
      print("do " + action.name)
      self.scene3d.redraw()

  def did(self, action):
    self.undoStack.append(action)
    del self.redoStack[:]
    print("did " + action.name)
    self.scene3d.redraw()

  def undo(self):
    if self.undoStack:
      action = self.undoStack.pop()
      print("undo " + action.name)
      action.undo()
      self.redoStack.append(action)
      self.scene3d.redraw()

  def redo(self):
    if self.redoStack:
      action = self.redoStack.pop()
      print("redo " + action.name)
      action.do()
      self.undoStack.append(action)
      self.scene3d.redraw()

  def setTheme(self, theme):
    f = open("data/themes/" + theme + ".mht", 'r')

    for data in f.readlines():
      lineData = data.split()

      if len(lineData) > 0:
        if lineData[0] == "version":
          print("Version " + lineData[1])
        elif lineData[0] == "color":
          if lineData[1] == "clear":
            mh.setClearColor(float(lineData[2]), float(lineData[3]), float(lineData[4]), float(lineData[5]))

    self.theme = theme

  def getThemeResource(self, folder, id):
    return "data/themes/" + self.theme + "/" + folder + "/"+ id

  def progress(self, value):
    self.progressBar.setProgress(value)
    if value <= 0:
      self.progressBar.show()
    elif value >= 1.0:
      self.progressBar.hide()

application = MHApplication()
mainScene = application.scene3d # HACK: Don't remove this, it is needed to receive events from C
application.start()

#import cProfile
#cProfile.run('application.start()')
