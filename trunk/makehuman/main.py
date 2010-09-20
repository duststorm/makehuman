"""
The main MakeHuman Python Application file.

B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Manuel Bastioni, Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2010

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

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

import sys
#print sys.builtin_module_names
#if 'nt' in sys.builtin_module_names:
sys.path.append("./pythonmodules")
import os

def recursiveDirNames(root):
  pathlist=[]
  #root=os.path.dirname(root)
  for filename in os.listdir(root):
    path=os.path.join(root,filename)
    if not (os.path.isfile(path) or filename=="." or filename==".." or filename==".svn"):
      pathlist.append(path)
      pathlist = pathlist + recursiveDirNames(path) 
  return(pathlist)

sys.path.append("./")
sys.path.append("./apps")
sys.path=sys.path + recursiveDirNames("./apps")
sys.path.append("./core")
sys.path=sys.path + recursiveDirNames("./core")

import subprocess
import webbrowser
import glob, imp
from os.path import join, basename, splitext

import mh
import gui3d, events3d, font3d
import human, hair, background, human_texture
import guimodelling, guifiles, guirender
from aljabr import centroid
#import font3d

class Settings:
    def __init__():
        pass

class MHApplication(gui3d.Application):
  def __init__(self):
    gui3d.Application.__init__(self)

    self.modelCamera = mh.Camera()

    mh.cameras.append(self.modelCamera)

    self.guiCamera = mh.Camera()
    self.guiCamera.fovAngle = 45
    self.guiCamera.eyeZ = 10
    self.guiCamera.projection = 0
    mh.cameras.append(self.guiCamera)

    self.setTheme("default")
    #self.setTheme("3d")
    
    self.fonts = {}
    
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
    #hairObj = hair.loadHairsFile(self.scene3d, path="./data/hairs/default", update = False)
    #self.scene3d.clear(hairObj) 
    self.scene3d.selectedHuman = human.Human(self.scene3d, "data/3dobjs/base.obj")
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
    human_texture.HumanTextureTaskView(library)

    # Load plugins not starting with _    
    self.modules = {}
    for path in glob.glob(join("plugins/",'[!_]*.py')):
        try:
            name, ext = splitext(basename(path))
            module = imp.load_source(name, path)
            self.modules[name] = module
            module.load(self)
        except Exception, e:
            print('Could not load %s' % name)
            print e

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
    if os.path.exists("data/themes/" + self.theme + "/" + folder + "/"+ id):
      return "data/themes/" + self.theme + "/" + folder + "/"+ id
    else:
      return "data/themes/default/" + folder + "/"+ id
      
  def getFont(self, fontFamily):
    if fontFamily not in self.fonts:
      self.fonts[fontFamily] = font3d.Font("data/fonts/%s.fnt" % fontFamily)
    return self.fonts[fontFamily]

  def progress(self, value):
    self.progressBar.setProgress(value)
    if value <= 0:
      self.progressBar.show()
    elif value >= 1.0:
      self.progressBar.hide()
      
  def setGlobalCamera(self):
    self.modelCamera.eyeX = 0
    self.modelCamera.eyeY = 0
    self.modelCamera.eyeZ = 60
    self.modelCamera.focusX = 0
    self.modelCamera.focusY = 0
    self.modelCamera.focusZ = 0
  
  def setFaceCamera(self):
    human = self.scene3d.selectedHuman
    headNames = [group.name for group in human.meshData.facesGroups if ("head" in group.name or "jaw" in group.name)]
    self.headVertices, self.headFaces = human.meshData.getVerticesAndFacesForGroups(headNames)
    center = centroid([v.co for v in self.headVertices])
    self.modelCamera.eyeX = center[0]
    self.modelCamera.eyeY = center[1]
    self.modelCamera.eyeZ = 10
    self.modelCamera.focusX = center[0]
    self.modelCamera.focusY = center[1]
    self.modelCamera.focusZ = 0
    human.setPosition([0.0, 0.0, 0.0])
    human.setRotation([0.0, 0.0, 0.0])
    
application = MHApplication()
mainScene = application.scene3d # HACK: Don't remove this, it is needed to receive events from C
application.start()

#import cProfile
#cProfile.run('application.start()')
