""" 
The main MakeHuman Python Application file.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009

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
if 'nt' in sys.builtin_module_names:
    sys.path.append("./pythonmodules")
import mh
import os
import subprocess
import webbrowser

sys.path.append("./")
sys.path.append("./mh_plugins")
sys.path.append("./mh_core")

# Adjust the exe path for AQSIS and PIXIE acc. the various Operating Systems.
if 'darwin' in sys.platform: # For MAC OS
    aqsisPath  = "/Applications/Aqsis.app/Contents/MacOS/"
    pixiePath  = "/Library/Pixie/bin/"
else:
    aqsisPath  = ""
    pixiePath  = ""

import gui3d, events3d
import human, hair
import guimodelling, guifiles, guirender

class MHApplication(gui3d.Application):
  def __init__(self):
    gui3d.Application.__init__(self)
    
    self.setTheme("default")
    
    # Dispkay the initial splash screen and the progress bar during startup 
    self.splash = gui3d.Object(self, "data/3dobjs/splash.obj", self.getThemeResource("images", "splash.png"), position = [0, 0, 0])
    self.progressBar = gui3d.ProgressBar(self, backgroundTexture = self.getThemeResource("images", "progressbar_background.png"),
      barTexture = self.getThemeResource("images", "progressbar.png"))
    self.scene3d.update()
    self.scene3d.redraw(0)
    
    # Create aqsis shaders
    subprocess.Popen(aqsisPath + "aqsl data/shaders/aqsis/lightmap_aqsis.sl -o data/shaders/aqsis/lightmap.slx", shell=True)
    subprocess.Popen(aqsisPath + "aqsl data/shaders/renderman/skin.sl -o data/shaders/renderman/skin.slx", shell=True)
    subprocess.Popen(aqsisPath + "aqsl data/shaders/renderman/scatteringtexture.sl -o data/shaders/renderman/scatteringtexture.slx", shell=True)

    # Create pixie shaders
    subprocess.Popen(pixiePath + "sdrc data/shaders/pixie/lightmap_pixie.sl -o data/shaders/pixie/lightmap.sdr", shell=True)
    subprocess.Popen(pixiePath + "sdrc data/shaders/pixie/read2dbm_pixie.sl -o data/shaders/pixie/read2dbm.sdr", shell=True)
    subprocess.Popen(pixiePath + "sdrc data/shaders/renderman/skin.sl -o data/shaders/renderman/skin.sdr", shell=True)
    
    self.progressBar.setProgress(0.2)
    
    gui3d.Object(self, "data/3dobjs/upperbar.obj", self.getThemeResource("images", "upperbar.png"), [0, 0.39, 9])
    gui3d.Object(self, "data/3dobjs/backgroundbox.obj", position = [0, 0, -72])
    gui3d.Object(self, "data/3dobjs/lowerbar.obj", self.getThemeResource("images", "lowerbar.png"), [0, -0.39, 9])
    
    self.progressBar.setProgress(0.3)
    
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
    
    # Exit button
    category = gui3d.Category(self, "Exit", self.getThemeResource("images", "button_exit.png"))
    @category.button.event
    def onClicked(event):
      self.stop()
    
    guimodelling.ModellingCategory(self)
    self.progressBar.setProgress(0.7)
    guifiles.FilesCategory(self)
    self.progressBar.setProgress(0.8)
    guirender.RenderingCategory(self)
    
    library = gui3d.Category(self, "Library", self.getThemeResource("images", "button_library.png"))
    hair.HairTaskView(library)
    
    category = gui3d.Category(self, "Help", self.getThemeResource("images", "button_about.png"))
    # Help button
    @category.button.event
    def onClicked(event):
      webbrowser.open(os.getcwd()+"/docs/MH_1.0.A1_Users_Guide.pdf");
    
    self.switchCategory("Modelling")
    
    self.progressBar.setProgress(1.0)
    self.progressBar.hide()
    
  def onStart(self, event):
      self.splash.hide()
      self.scene3d.selectedHuman.applyAllTargets()
      
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
          webbrowser.open(os.getcwd()+"/docs/MH_1.0.A1_Users_Guide.pdf");
    
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
    
application = MHApplication()
mainScene = application.scene3d # HACK: Don't remove this, it is needed to receive events from C
application.start()

#import cProfile
#cProfile.run('application.start()')
