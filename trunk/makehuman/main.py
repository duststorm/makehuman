"""
The main MakeHuman Python Application file.

B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Manuel Bastioni, Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2011

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

if not 'STARTEDCORRECTLY' in os.environ:
    print "\nERROR ERROR ERROR"
    print "You should not run main.py directly. Please run makehuman.py instead."
    print "ERROR ERROR ERROR\n"
    sys.exit()

def printleaf(object, indent=0):

    print "%s%s %s" % (' ' * indent, object, object._Object__view)

def printtree(view, indent=0):

    print "%s%s %s" % (' ' * indent, type(view), type(view.parent))
    for child in view.children:
        printtree(child, indent+2)
    for object in view.objects:
        printleaf(object, indent+2)

def recursiveDirNames(root):
  pathlist=[]
  #root=os.path.dirname(root)
  for filename in os.listdir(root):
    path=os.path.join(root,filename)
    if not (os.path.isfile(path) or filename=="." or filename==".." or filename==".svn"):
      pathlist.append(path)
      pathlist = pathlist + recursiveDirNames(path) 
  return(pathlist)

syspath = ["./", "./lib", "./apps", "./shared", "./shared/mhx/templates", "./shared/mhx"]
syspath = syspath + recursiveDirNames("./apps")
syspath.append("./core")
syspath = syspath + recursiveDirNames("./core")
syspath.extend(sys.path)
sys.path = syspath

import glob, imp
from os.path import join, basename, splitext

from core import G
import mh
import files3d
import gui3d, events3d, font3d, animation3d
import mh2obj, mh2bvh, mh2mhx
import human
import guimodelling, guifiles#, guirender
from aljabr import centroid, vdist
import algos3d
import module3d
#import posemode
from math import tan, pi
import qtgui as gui

class Camera(events3d.EventHandler):

    def __init__(self):
    
        self.camera = mh.Camera();
        self.changedPending = False;
        
    def getProjection(self):
    
        return self.camera.projection

    def setProjection(self, value):
    
        self.camera.projection = value
        self.changed()
        
    projection = property(getProjection, setProjection)
        
    def getFovAngle(self):
    
        return self.camera.fovAngle

    def setFovAngle(self, value):
    
        self.camera.fovAngle = value
        self.changed()
        
    fovAngle = property(getFovAngle, setFovAngle)
    
    def getNearPlane(self):
    
        return self.camera.nearPlane

    def setNearPlane(self, value):
    
        self.camera.nearPlane = value
        self.changed()
        
    nearPlane = property(getNearPlane, setNearPlane)
    
    def getFarPlane(self):
    
        return self.camera.farPlane

    def setFarPlane(self, value):
    
        self.camera.farPlane = value
        self.changed()
        
    farPlane = property(getFarPlane, setFarPlane)
    
    def getEyeX(self):
    
        return self.camera.eyeX

    def setEyeX(self, value):
    
        self.camera.eyeX = value
        self.changed()
        
    eyeX = property(getEyeX, setEyeX)
        
    def getEyeY(self):
    
        return self.camera.eyeY

    def setEyeY(self, value):
    
        self.camera.eyeY = value
        self.changed()
        
    eyeY = property(getEyeY, setEyeY)
    
    def getEyeZ(self):
    
        return self.camera.eyeZ

    def setEyeZ(self, value):
    
        self.camera.eyeZ = value
        if self.camera.projection == 0:
            self.switchToOrtho();
        self.changed()
        
    eyeZ = property(getEyeZ, setEyeZ)
    
    @property
    def eye(self):
        return (self.camera.eyeX, self.camera.eyeY, self.camera.eyeZ)
        
    def getFocusX(self):
    
        return self.camera.focusX

    def setFocusX(self, value):
    
        self.camera.focusX = value
        self.changed()
        
    focusX = property(getFocusX, setFocusX)
        
    def getFocusY(self):
    
        return self.camera.focusY

    def setFocusY(self, value):
    
        self.camera.focusY = value
        self.changed()
        
    focusY = property(getFocusY, setFocusY)
    
    def getFocusZ(self):
    
        return self.camera.focusZ

    def setFocusZ(self, value):
    
        self.camera.focusZ = value
        if self.camera.projection == 0:
            self.switchToOrtho();
        self.changed()
        
    focusZ = property(getFocusZ, setFocusZ)
    
    @property
    def focus(self):
        return (self.camera.focusX, self.camera.focusY, self.camera.focusZ)
    
    def getUpX(self):
    
        return self.camera.upX

    def setUpX(self, value):
    
        self.camera.upX = value
        self.changed()
        
    upX = property(getUpX, setUpX)
        
    def getUpY(self):
    
        return self.camera.upY

    def setUpY(self, value):
    
        self.camera.upY = value
        self.changed()
        
    upY = property(getUpY, setUpY)
    
    def getUpZ(self):
    
        return self.camera.upZ

    def setUpZ(self, value):
    
        self.camera.upZ = value
        self.changed()
        
    upZ = property(getUpZ, setUpZ)
    
    @property
    def focus(self):
        return (self.camera.upX, self.camera.upY, self.camera.upZ)
        
    def getLeft(self):
    
        return self.camera.left

    def setLeft(self, value):
    
        self.camera.left = value
        self.changed()
        
    left = property(getLeft, setLeft)
    
    def getRight(self):
    
        return self.camera.right

    def setRight(self, value):
    
        self.camera.right = value
        self.changed()
        
    right = property(getRight, setRight)
    
    def getBottom(self):
    
        return self.camera.bottom

    def setBottom(self, value):
    
        self.camera.bottom = value
        self.changed()
        
    bottom = property(getBottom, setBottom)
    
    def getTop(self):
    
        return self.camera.top

    def setTop(self, value):
    
        self.camera.top = value
        self.changed()
        
    top = property(getTop, setTop)
    
    def getStereoMode(self):
    
        return self.camera.stereoMode

    def setStereoMode(self, value):
    
        self.camera.stereoMode = value
        self.changed()
        
    stereoMode = property(getStereoMode, setStereoMode)
        
    def convertToScreen(self, x, y, z, obj=None):
    
        return self.camera.convertToScreen(x, y, z, obj)
        
    def convertToWorld3D(self, x, y, z):
    
        return self.camera.convertToWorld3D(x, y, z)
        
    def changed(self):
        
        if self.changedPending:
            return
            
        self.changedPending = True
        mh.callAsync(self.callChanged)
        
    def callChanged(self):
    
        self.callEvent('onChanged', self)
        self.changedPending = False
        
    def switchToOrtho(self):
    
        self.camera.projection = 0
        
        self.camera.nearPlane = 0.001
            
        width, height = gui3d.app.getWindowSize()
        aspect = float(width) / float(height)
        fov = tan(self.camera.fovAngle * 0.5 * pi / 180.0)
        y = vdist(self.eye, self.focus) * fov
        x = y * aspect
        
        self.camera.left = -x
        self.camera.right = x
        self.camera.bottom = -y
        self.camera.top = y
        
        self.camera.nearPlane = -100.0
        
    def switchToPerspective(self):
    
        self.camera.projection = 0

class PluginCheckBox(gui.CheckBox):

    def __init__(self, module):
    
        super(PluginCheckBox, self).__init__(module, module not in gui3d.app.settings['excludePlugins'])
        self.module = module
        
    def onClicked(self, event):
        if self.selected:
            gui3d.app.settings['excludePlugins'].remove(self.module)
        else:
            gui3d.app.settings['excludePlugins'].append(self.module)
            
        gui3d.app.saveSettings()

class PluginsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Plugins')

        self.pluginsBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Plugins')))
        
        for module in gui3d.app.modules:
            check = self.pluginsBox.addWidget(PluginCheckBox(module))
        
class MHApplication(gui3d.Application):
  
    def __init__(self):
        gui3d.Application.__init__(self)

        self.modelCamera = Camera()
        
        @self.modelCamera.mhEvent
        def onChanged(event):
            for category in self.categories.itervalues():
                
                for task in category.tasks:
                    
                    task.callEvent('onCameraChanged', event)

        mh.cameras.append(self.modelCamera.camera)

        self.guiCamera = Camera()
        self.guiCamera.fovAngle = 45
        self.guiCamera.eyeZ = 10
        self.guiCamera.projection = 0
        mh.cameras.append(self.guiCamera.camera)

        self.setTheme("default")
        #self.setTheme("3d")
        self.setLanguage("english")
        
        self.fonts = {}
        
        self.settings = {
            'realtimeUpdates': True,
            'realtimeNormalUpdates': True,
            'shader': None,
            'lowspeed': 1,
            'highspeed': 5,
            'units':'metric',
            'invertMouseWheel':False,
            'font':'arial',
            'language':'english',
            'excludePlugins':[],
            'rtl': False
        }
        
        self.shortcuts = {
            # Actions
            (mh.Modifiers.CTRL, mh.Keys.z): self.undo,
            (mh.Modifiers.CTRL, mh.Keys.y): self.redo,
            (mh.Modifiers.CTRL, mh.Keys.m): self.goToModelling,
            (mh.Modifiers.CTRL, mh.Keys.s): self.goToSave,
            (mh.Modifiers.CTRL, mh.Keys.l): self.goToLoad,
            (mh.Modifiers.CTRL, mh.Keys.e): self.goToExport,
            (mh.Modifiers.CTRL, mh.Keys.r): self.goToRendering,
            (mh.Modifiers.CTRL, mh.Keys.h): self.goToHelp,
            (mh.Modifiers.CTRL, mh.Keys.q): self.promptAndExit,
            (mh.Modifiers.CTRL, mh.Keys.w): self.toggleStereo,
            (mh.Modifiers.CTRL, mh.Keys.f): self.toggleSolid,
            (mh.Modifiers.ALT, mh.Keys.t): self.saveTarget,
            (mh.Modifiers.ALT, mh.Keys.e): self.quickExport,
            (mh.Modifiers.ALT, mh.Keys.s): self.toggleSubdivision,
            (mh.Modifiers.ALT, mh.Keys.g): self.grabScreen,
            # Camera navigation
            (0, mh.Keys.N2): self.rotateDown,
            (0, mh.Keys.N4): self.rotateLeft,
            (0, mh.Keys.N6): self.rotateRight,
            (0, mh.Keys.N8): self.rotateUp,
            (0, mh.Keys.UP): self.panUp,
            (0, mh.Keys.DOWN): self.panDown,
            (0, mh.Keys.RIGHT): self.panRight,
            (0, mh.Keys.LEFT): self.panLeft,
            (0, mh.Keys.PLUS): self.zoomIn,
            (0, mh.Keys.MINUS): self.zoomOut,
            (0, mh.Keys.N1): self.frontView,
            (0, mh.Keys.N3): self.rightView,
            (0, mh.Keys.N7): self.topView,
            (mh.Modifiers.CTRL, mh.Keys.N1): self.backView,
            (mh.Modifiers.CTRL, mh.Keys.N3): self.leftView,
            (mh.Modifiers.CTRL, mh.Keys.N7): self.bottomView,
            (0, mh.Keys.PERIOD): self.resetView
        }
        
        self.mouseActions = {
            (0, mh.Buttons.RIGHT_MASK): self.mouseTranslate,
            (0, mh.Buttons.LEFT_MASK): self.mouseRotate,
            (0, mh.Buttons.MIDDLE_MASK): self.mouseZoom
        }

        self.dialog = None
        self.helpIds = []
        
        self.loadSettings()
        
        self.loadHandlers = {}
        self.saveHandlers = []
        
        # Display the initial splash screen and the progress bar during startup
        mesh = gui3d.RectangleMesh(800, 600, gui3d.app.getThemeResource('images', 'splash.png'))
        self.splash = self.addObject(gui3d.Object([0, 0, 9.8], mesh))
        self.progressBar = mh.addWidget(mh.Frame.Bottom, gui.ProgressBar())
        self.redrawNow()
        
        # self.tabs = self.addView(gui3d.TabView())
        self.tabs = G.app.mainwin.tabs
        
        @self.tabs.mhEvent
        def onTabSelected(tab):
            self.switchCategory(tab.name)

    def loadBackground(self):

        self.progressBar.setProgress(0.1)

        self.statusbar = self.addObject(gui3d.Object([0, 580, 9], gui3d.RectangleMesh(800, 32, self.getThemeResource("images", "lowerbar.png"))))
        mh.setClearColor(0.5, 0.5, 0.5, 1.0)
        
        mh.callAsync(self.loadHuman)
        
    def loadHuman(self):   

        self.progressBar.setProgress(0.2)
        #hairObj = hair.loadHairsFile(self.scene3d, path="./data/hairs/default", update = False)
        #self.scene3d.clear(hairObj) 
        self.selectedHuman = self.addObject(human.Human(files3d.loadMesh("data/3dobjs/base.obj")))
        
        mh.callAsync(self.loadMainGui)
        
    def loadMainGui(self):
        
        self.progressBar.setProgress(0.3)

        self.tool = None
        self.selectedGroup = None

        self.undoStack = []
        self.redoStack = []

        @self.selectedHuman.mhEvent
        def onMouseDown(event):
          if self.tool:
            self.selectedGroup = self.getSelectedFaceGroup()
            self.tool.callEvent("onMouseDown", event)
          else:
            self.currentTask.callEvent("onMouseDown", event)

        @self.selectedHuman.mhEvent
        def onMouseMoved(event):
          if self.tool:
            self.tool.callEvent("onMouseMoved", event)
          else:
            self.currentTask.callEvent("onMouseMoved", event)

        @self.selectedHuman.mhEvent
        def onMouseDragged(event):
          if self.tool:
            self.tool.callEvent("onMouseDragged", event)
          else:
            self.currentTask.callEvent("onMouseDragged", event)

        @self.selectedHuman.mhEvent
        def onMouseUp(event):
          if self.tool:
            self.tool.callEvent("onMouseUp", event)
          else:
            self.currentTask.callEvent("onMouseUp", event)

        @self.selectedHuman.mhEvent
        def onMouseEntered(event):
          if self.tool:
            self.tool.callEvent("onMouseEntered", event)
          else:
            self.currentTask.callEvent("onMouseEntered", event)

        @self.selectedHuman.mhEvent
        def onMouseExited(event):
          if self.tool:
            self.tool.callEvent("onMouseExited", event)
          else:
            self.currentTask.callEvent("onMouseExited", event)
            
        @self.selectedHuman.mhEvent
        def onChanging(event):
            
            for category in self.categories.itervalues():
                
                for task in category.tasks:
                    
                    task.callEvent('onHumanChanging', event)
                    
        @self.selectedHuman.mhEvent
        def onChanged(event):
            
            for category in self.categories.itervalues():
                
                for task in category.tasks:
                    
                    task.callEvent('onHumanChanged', event)
                    
        @self.selectedHuman.mhEvent
        def onTranslated(event):
            
            for category in self.categories.itervalues():
                
                for task in category.tasks:
                    
                    task.callEvent('onHumanTranslated', event)
                    
        @self.selectedHuman.mhEvent
        def onRotated(event):
            
            for category in self.categories.itervalues():
                
                for task in category.tasks:
                    
                    task.callEvent('onHumanRotated', event)
                    
        @self.selectedHuman.mhEvent
        def onShown(event):
            
            for category in self.categories.itervalues():
                
                for task in category.tasks:
                    
                    task.callEvent('onHumanShown', event)
                    
        @self.selectedHuman.mhEvent
        def onHidden(event):
            
            for category in self.categories.itervalues():
                
                for task in category.tasks:
                    
                    task.callEvent('onHumanHidden', event)

        # Set up categories and tasks
        
        self.addView(guimodelling.ModellingCategory(self))
        self.addView(guifiles.FilesCategory(self))
        
        mh.callAsync(self.loadPlugins)
        
    def loadPlugins(self):
        
        self.progressBar.setProgress(0.4)

        # Load plugins not starting with _    
        self.modules = {}
        
        self.pluginsToLoad = glob.glob(join("plugins/",'[!_]*.py'))
        self.pluginsToLoad.sort()
        self.pluginsToLoad.reverse()
        
        if self.pluginsToLoad:
            mh.callAsync(self.loadNextPlugin)
        else:
            mh.callAsync(self.loadGui)
    
    def loadNextPlugin(self):
        
        alreadyLoaded = len(self.modules)
        stillToLoad = len(self.pluginsToLoad)
        self.progressBar.setProgress(0.4 + (float(alreadyLoaded) / float(alreadyLoaded + stillToLoad)) * 0.4)
        
        if stillToLoad:
            
            path = self.pluginsToLoad.pop()
            try:
                name, ext = splitext(basename(path))
                if name not in self.settings['excludePlugins']:
                    module = imp.load_source(name, path)
                    self.modules[name] = module
                    module.load(self)
                else:
                    self.modules[name] = None
            except Exception, e:
                import traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                print('Could not load %s' % name)
                print e
                
            mh.callAsync(self.loadNextPlugin)
            
        else:
            
            mh.callAsync(self.loadGui)
            
    def unloadPlugins(self):
        
        for name, module in self.modules.iteritems():
            try:
                module.unload(self)
            except Exception, e:
                import traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                print('Could not unload %s' % name)
                print e
                
    def loadGui(self):
        
        self.progressBar.setProgress(0.9)
              
        category = self.getCategory('Settings')
        category.addView(PluginsTaskView(category))
          
        # Exit button
        category = self.addView(gui3d.Category(self, "Exit", tabStyle=gui3d.CategoryButtonStyle))
        @category.tab.mhEvent
        def onClicked(event):
            self.promptAndExit()

        self.buttonBox = mh.addWidget(mh.Frame.RightBottom, gui.GroupBox('Edit'))
        self.undoButton  = self.buttonBox.addWidget(gui.Button("Undo"),  0, 0)
        self.redoButton  = self.buttonBox.addWidget(gui.Button("Redo"),  0, 1)
        self.resetButton = self.buttonBox.addWidget(gui.Button("Reset"), 0, 2)

        @self.undoButton.mhEvent
        def onClicked(event):
            gui3d.app.undo()

        @self.redoButton.mhEvent
        def onClicked(event):
            gui3d.app.redo()

        @self.resetButton.mhEvent
        def onClicked(event):
            human = self.selectedHuman
            human.resetMeshValues()
            human.applyAllTargets(self.progress)
            

            mh.setCaption("MakeHuman r" + os.environ['SVNREVISION'] + " - [Untitled]")
          
        self.globalButton = self.buttonBox.addWidget(gui.Button("Global cam"), 1, 0, 1, -1)
        self.faceButton = self.buttonBox.addWidget(gui.Button("Face cam"), 2, 0, 1, -1)

        @self.globalButton.mhEvent
        def onClicked(event):
          gui3d.app.setGlobalCamera()
          
        @self.faceButton.mhEvent
        def onClicked(event):
          gui3d.app.setFaceCamera()

        """          
        self.poseModeBox = self.addView(gui3d.CheckBox("Pose mode", False,
            style=gui3d.CheckBoxStyle._replace(width=128, height=20, left=650, top=555, zIndex=9.1)))
        
        @self.poseModeBox.mhEvent
        def onClicked(event):
          print dir(event)
          if self.poseModeBox.selected:
            posemode.exitPoseMode()
          else:
            posemode.enterPoseMode()
        """
        
        self.switchCategory("Modelling")

        self.progressBar.setProgress(1.0)
        self.progressBar.hide()
        
        mh.callAsync(self.loadFinish)
                
    def loadFinish(self):
        
        self.selectedHuman.applyAllTargets(gui3d.app.progress)
        self.selectedHuman.callEvent('onChanged', human.HumanEvent(self.selectedHuman, 'reset'))

        self.prompt('Warning', 'This is an alpha release, which means that there are still bugs present and features missing. Use at your own risk.',
            'OK', helpId='alphaWarning')
        # self.dialog.blocker.mesh.setColor([0, 0, 0, 128])
        self.splash.hide()

        mh.setCaption("MakeHuman r" + os.environ['SVNREVISION'] + " - [Untitled]")
        
        #printtree(self)
        
        mh.updatePickingBuffer();
        self.redraw()
        
    # Events
    def onStart(self, event):
        
        mh.callAsync(self.loadBackground)
        
    def onStop(self, event):
        
        self.saveSettings()
        self.unloadPlugins()
        self.dumpMissingStrings()
        
    def onQuit(self, event):
        
        self.promptAndExit()
        
    def onMouseDragged(self, event):
        
        if self.selectedHuman.isVisible():
            
            # Normalize modifiers
            modifiers = mh.getKeyModifiers() & (mh.Modifiers.CTRL | mh.Modifiers.ALT | mh.Modifiers.SHIFT)
            
            if (modifiers, event.button) in self.mouseActions:
                self.mouseActions[(modifiers, event.button)](event)

    def onMouseWheel(self, event):
        
        if self.selectedHuman.isVisible():
            
            zoomOut = event.wheelDelta > 0
            if gui3d.app.settings.get('invertMouseWheel', False):
                zoomOut = not zoomOut
            
            if zoomOut:
                self.zoomOut()
            else:
                self.zoomIn()

    def onKeyDown(self, event):
        
        # Normalize modifiers
        modifiers = event.modifiers & (mh.Modifiers.CTRL | mh.Modifiers.ALT)
        
        if modifiers & mh.Modifiers.CTRL:
            modifiers |= mh.Modifiers.CTRL
        if modifiers & mh.Modifiers.ALT:
            modifiers |= mh.Modifiers.ALT
            
        # Normalize key
        key = event.key
            
        if (modifiers, key) in self.shortcuts:
            self.shortcuts[(modifiers, key)]()
            
    def onResized(self, event):

        # self.tabs.box.mesh.resize(event.width, 32)
        self.statusbar.mesh.resize(event.width, 32)
        self.statusbar.setPosition((0.0, event.height-20, 9))
        
    # Undo-redo
    def do(self, action):
        if action.do():
            self.undoStack.append(action)
            del self.redoStack[:]
            print("do " + action.name)
            self.redraw()

    def did(self, action):
        self.undoStack.append(action)
        del self.redoStack[:]
        print("did " + action.name)
        self.redraw()

    def undo(self):
        if self.undoStack:
            action = self.undoStack.pop()
            print("undo " + action.name)
            action.undo()
            self.redoStack.append(action)
            self.redraw()

    def redo(self):
        if self.redoStack:
            action = self.redoStack.pop()
            print("redo " + action.name)
            action.do()
            self.undoStack.append(action)
            self.redraw()
            
    # Settings
            
    def loadSettings(self):
        try:
            if os.path.isfile(os.path.join(mh.getPath(''), "settings.ini")):
                f = open(os.path.join(mh.getPath(''), "settings.ini"), 'r')
                settings = eval(f.read(), {"__builtins__":None}, {'True':True, 'False':False})
                self.settings.update(settings)
                f.close()
        except:
            print("Failed to load settings")
            
        if 'language' in gui3d.app.settings:
            self.setLanguage(gui3d.app.settings['language'])
        
        try:
            if os.path.isfile(os.path.join(mh.getPath(''), "shortcuts.ini")):
                self.shortcuts = {}
                f = open(os.path.join(mh.getPath(''), "shortcuts.ini"), 'r')
                for line in f:
                    modifier, key, method = line.split(' ')
                    #print modifier, key, method[0:-1]
                    if hasattr(self, method[0:-1]):
                        self.shortcuts[(int(modifier), int(key))] = getattr(self, method[0:-1])
                f.close()
        except:
            print("Failed to load shortcut settings")
 
        try:
            if os.path.isfile(os.path.join(mh.getPath(''), "mouse.ini")):
                self.mouseActions = {}
                f = open(os.path.join(mh.getPath(''), "mouse.ini"), 'r')
                for line in f:
                    modifier, button, method = line.split(' ')
                    #print modifier, button, method[0:-1]
                    if hasattr(self, method[0:-1]):
                        self.mouseActions[(int(modifier), int(button))] = getattr(self, method[0:-1])
                f.close()
        except:
            print("Failed to load mouse settings")
        
        try:
            if os.path.isfile(os.path.join(mh.getPath(''), "help.ini")):
                self.helpIds = []
                f = open(os.path.join(mh.getPath(''), "help.ini"), 'r')
                for line in f:
                    self.helpIds.append(line[0:-1])
                f.close()
        except:
            print("Failed to load help settings")
        
    def saveSettings(self):
        if not os.path.exists(mh.getPath('')):
            os.makedirs(mh.getPath(''))
        
        f = open(os.path.join(mh.getPath(''), "settings.ini"), 'w')
        f.write(repr(self.settings))
        f.close()
        
        f = open(os.path.join(mh.getPath(''), "shortcuts.ini"), 'w')
        for shortcut, method in self.shortcuts.iteritems():
            f.write('%d %d %s\n' % (shortcut[0], shortcut[1], method.__name__))
        f.close()
            
        f = open(os.path.join(mh.getPath(''), "mouse.ini"), 'w')
        for mouseAction, method in self.mouseActions.iteritems():
            f.write('%d %d %s\n' % (mouseAction[0], mouseAction[1], method.__name__))
        f.close()
            
        f = open(os.path.join(mh.getPath(''), "help.ini"), 'w')
        for helpId in self.helpIds:
            f.write('%s\n' % helpId)
        f.close()

    # Themes
    def setTheme(self, theme):
    
        f = open(os.path.join("data/themes/", theme + ".mht"), 'r')

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
        if '/' in id:
            return id
        path = os.path.join("data/themes/", self.theme, folder, id)
        if os.path.exists(path):
            return path
        else:
            return os.path.join("data/themes/default/", folder, id)
            
    def setLanguage(self, language):
        
        path = os.path.join("data/languages/", language + ".ini")
        if os.path.isfile(path):
            f = open(path, 'rU')
            try:
                self.languageStrings = eval(f.read(), {"__builtins__":None}, {'True':True, 'False':False})
            except:
                import traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                print('Error in language file %s' % language)
                self.languageStrings = None
            f.close()
            if self.languageStrings and '__options__' in self.languageStrings:
                if 'rtl' in self.languageStrings['__options__']:
                    self.settings['rtl'] = self.languageStrings['__options__']['rtl']
                else:
                    self.settings['rtl'] = False
            else:
                self.settings['rtl'] = False
        else:
            self.languageStrings = None
            
    def getLanguageString(self, string):
        if self.languageStrings:
            try:
                return self.languageStrings[string]
            except:
                if not hasattr(self, 'missingStrings'):
                    self.missingStrings = set();
                self.missingStrings.add(string)
                return string
        else:
            return string
            
    def dumpMissingStrings(self):
    
        if not hasattr(self, 'missingStrings'):
            return
        try:
            f = open(os.path.join("data/languages/", self.settings['language'] + ".missing"), 'w')
            for string in self.missingStrings:
                f.write("'")
                f.write(string.encode('utf8'))
                f.write("':'',\n")
            f.close()
        except:
            pass
      
    # Font resources
    def getFont(self, fontFamily):
        if fontFamily not in self.fonts:
            self.fonts[fontFamily] = font3d.Font("data/fonts/%s.fnt" % fontFamily)
            
        return self.fonts[fontFamily]
        
    # Caption
    def setCaption(self, caption):
        mh.setCaption(caption.encode('utf8'))

    # Global progress bar
    def progress(self, value, text=None):
        if text is not None:
            self.progressBar.text.setText(text)
        if value <= 0:
            self.progressBar.show()
        elif value >= 1.0:
            self.progressBar.hide()
        self.progressBar.setProgress(value)
    
    # Global dialog
    def prompt(self, title, text, button1Label, button2Label=None, button1Action=None, button2Action=None, helpId=None):
        if self.dialog is None:
            self.dialog = gui.Dialog(G.app.mainwin)
        self.dialog.prompt(title, text, button1Label, button2Label, button1Action, button2Action, helpId)

    # Camera's
    def setCameraCenterViewDistance(self, center, view='front', distance=10):
    
        human = self.selectedHuman
        tl = animation3d.Timeline(0.20)
        cam = self.modelCamera
        if view == 'front':
            tl.append(animation3d.CameraAction(self.modelCamera, None,
                [center[0], center[1], distance,
                center[0], center[1], 0,
                0, 1, 0]))
        elif view == 'top':
            tl.append(animation3d.CameraAction(self.modelCamera, None,
                [center[0], center[1] + distance, center[2],
                center[0], center[1], center[2],
                0, 0, -1]))
        elif view == 'left':
            tl.append(animation3d.CameraAction(self.modelCamera, None,
                [center[0] - distance, center[1], center[2],
                center[0], center[1], center[2],
                0, 1, 0]))
        elif view == 'right':
            tl.append(animation3d.CameraAction(self.modelCamera, None,
                [center[0] + distance, center[1], center[2],
                center[0], center[1], center[2],
                0, 1, 0]))
        tl.append(animation3d.PathAction(human, [human.getPosition(), [0.0, 0.0, 0.0]]))
        tl.append(animation3d.RotateAction(human, human.getRotation(), [0.0, 0.0, 0.0]))
        tl.append(animation3d.UpdateAction(self))
        tl.start()
        
    def setCameraGroupsViewDistance(self, groupNames, view='front', distance=10):
    
        human = self.selectedHuman
        vertices = human.meshData.getCoords(human.meshData.getVerticesForGroups(groupNames))
        center = centroid(vertices)
        
        self.setCameraCenterViewDistance(center, view, distance)
    
    def setGlobalCamera(self):
        
        human = self.selectedHuman
        
        tl = animation3d.Timeline(0.20)
        cam = self.modelCamera
        tl.append(animation3d.CameraAction(self.modelCamera, None, [0,0,60, 0,0,0, 0,1,0]))
        tl.append(animation3d.PathAction(human, [human.getPosition(), [0.0, 0.0, 0.0]]))
        tl.append(animation3d.RotateAction(human, human.getRotation(), [0.0, 0.0, 0.0]))
        tl.append(animation3d.UpdateAction(self))
        tl.start()

    def setFaceCamera(self):
        
        human = self.selectedHuman
        headNames = [group.name for group in human.meshData.faceGroups if ("head" in group.name or "jaw" in group.name)]
        self.setCameraGroupsViewDistance(headNames)
        
    def setLeftHandFrontCamera(self):
        
        human = self.selectedHuman
        leftHandNames = [group.name for group in human.meshData.faceGroups if ("l-hand" in group.name)]
        self.setCameraGroupsViewDistance(leftHandNames)
        
    def setLeftHandTopCamera(self):
        
        human = self.selectedHuman
        leftHandNames = [group.name for group in human.meshData.faceGroups if ("l-hand" in group.name)]
        self.setCameraGroupsViewDistance(leftHandNames, 'top')
        
    def setRightHandFrontCamera(self):
        
        human = self.selectedHuman
        rightHandNames = [group.name for group in human.meshData.faceGroups if ("r-hand" in group.name)]
        self.setCameraGroupsViewDistance(rightHandNames)
        
    def setRightHandTopCamera(self):
        
        human = self.selectedHuman
        rightHandNames = [group.name for group in human.meshData.faceGroups if ("r-hand" in group.name)]
        self.setCameraGroupsViewDistance(rightHandNames, 'top')
        
    def setLeftFootFrontCamera(self):
        
        human = self.selectedHuman
        leftFootNames = [group.name for group in human.meshData.faceGroups if ("l-foot" in group.name)]
        self.setCameraGroupsViewDistance(leftFootNames)
        
    def setLeftFootLeftCamera(self):
        
        human = self.selectedHuman
        leftFootNames = [group.name for group in human.meshData.faceGroups if ("l-foot" in group.name)]
        self.setCameraGroupsViewDistance(leftFootNames, 'left')
        
    def setRightFootFrontCamera(self):
        
        human = self.selectedHuman
        rightFootNames = [group.name for group in human.meshData.faceGroups if ("r-foot" in group.name)]
        self.setCameraGroupsViewDistance(rightFootNames)
        
    def setRightFootRightCamera(self):
        
        human = self.selectedHuman
        rightFootNames = [group.name for group in human.meshData.faceGroups if ("r-foot" in group.name)]
        self.setCameraGroupsViewDistance(rightFootNames, 'right')
        
    def setLeftArmFrontCamera(self):
        
        human = self.selectedHuman
        leftArmNames = [group.name for group in human.meshData.faceGroups if ("l-lowerarm" in group.name or "l-upperarm" in group.name)]
        self.setCameraGroupsViewDistance(leftArmNames, distance=30)
        
    def setLeftArmTopCamera(self):
        
        human = self.selectedHuman
        leftArmNames = [group.name for group in human.meshData.faceGroups if ("l-lowerarm" in group.name or "l-upperarm" in group.name)]
        self.setCameraGroupsViewDistance(leftArmNames, 'top', distance=30)
        
    def setRightArmFrontCamera(self):
        
        human = self.selectedHuman
        rightArmNames = [group.name for group in human.meshData.faceGroups if ("r-lowerarm" in group.name or "r-upperarm" in group.name)]
        self.setCameraGroupsViewDistance(rightArmNames, distance=30)
        
    def setRightArmTopCamera(self):
        
        human = self.selectedHuman
        rightArmNames = [group.name for group in human.meshData.faceGroups if ("r-lowerarm" in group.name or "r-upperarm" in group.name)]
        self.setCameraGroupsViewDistance(rightArmNames, 'top', distance=30)
        
    def setLeftLegFrontCamera(self):
        
        human = self.selectedHuman
        leftLegNames = [group.name for group in human.meshData.faceGroups if ("l-lowerleg" in group.name or "l-upperleg" in group.name)]
        self.setCameraGroupsViewDistance(leftLegNames, distance=30)
        
    def setLeftLegLeftCamera(self):
        
        human = self.selectedHuman
        leftLegNames = [group.name for group in human.meshData.faceGroups if ("l-lowerleg" in group.name or "l-upperleg" in group.name)]
        self.setCameraGroupsViewDistance(leftLegNames, 'left', distance=30)
        
    def setRightLegFrontCamera(self):
        
        human = self.selectedHuman
        rightLegNames = [group.name for group in human.meshData.faceGroups if ("r-lowerleg" in group.name or "r-upperleg" in group.name)]
        self.setCameraGroupsViewDistance(rightLegNames, distance=30)
        
    def setRightLegRightCamera(self):
        
        human = self.selectedHuman
        rightLegNames = [group.name for group in human.meshData.faceGroups if ("r-lowerleg" in group.name or "r-upperleg" in group.name)]
        self.setCameraGroupsViewDistance(rightLegNames, 'right', distance=30)
        
    # Shortcuts
    def setShortcut(self, modifier, key, method):
        
        shortcut = (modifier, key)
        
        if shortcut in self.shortcuts:
            self.prompt('Warning', 'This combination is already in use. Change the combination for the action which has reserved this shortcut', 'OK', helpId='shortcutWarning')
            return False
            
        # Remove old entry
        for s, m in self.shortcuts.iteritems():
            if m == method:
                del self.shortcuts[s]
                break
                
        self.shortcuts[shortcut] = method
        
        #for shortcut, m in self.shortcuts.iteritems():
        #    print shortcut, m
        
        return True
        
    def getShortcut(self, method):
        
        for shortcut, m in self.shortcuts.iteritems():
            if m == method:
                return shortcut
                
    # Mouse actions
    def setMouseAction(self, modifier, key, method):
        
        mouseAction = (modifier, key)
        
        if mouseAction in self.mouseActions:
            self.prompt('Warning', 'This combination is already in use. Change the combination for the action which has reserved this mouse action', 'OK', helpId='mouseActionWarning')
            return False
            
        # Remove old entry
        for s, m in self.mouseActions.iteritems():
            if m == method:
                del self.mouseActions[s]
                break
                
        self.mouseActions[mouseAction] = method
        
        #for mouseAction, m in self.mouseActions.iteritems():
        #    print mouseAction, m
        
        return True
        
    def getMouseAction(self, method):
        
        for mouseAction, m in self.mouseActions.iteritems():
            if m == method:
                return mouseAction
                
    # Load handlers
    
    def addLoadHandler(self, keyword, handler):
        self.loadHandlers[keyword] = handler
        
    # Save handlers
    
    def addSaveHandler(self, handler):
        self.saveHandlers.append(handler)
    
    # Shortcut methods
    
    def goToModelling(self):
        self.switchCategory("Modelling")
        self.redraw()
        
    def goToSave(self):
        self.switchCategory("Files")
        self.switchTask("Save")
        self.redraw()
        
    def goToLoad(self):
        self.switchCategory("Files")
        self.switchTask("Load")
        self.redraw()
        
    def goToExport(self):
        self.switchCategory("Files")
        self.switchTask("Export")
        self.redraw()
        
    def goToRendering(self):
        self.switchCategory("Rendering")
        self.redraw()
        
    def goToHelp(self):
        self.switchCategory("Help")
          
    def toggleStereo(self):
        stereoMode = self.modelCamera.stereoMode
        stereoMode += 1
        if stereoMode > 2:
            stereoMode = 0
        self.modelCamera.stereoMode = stereoMode

        # We need a black background for stereo
        if stereoMode:
            mh.setClearColor(0.0, 0.0, 0.0, 1.0)
            self.categories["Modelling"].anaglyphsButton.setSelected(True)
        else:
            mh.setClearColor(0.5, 0.5, 0.5, 1.0)
            self.categories["Modelling"].anaglyphsButton.setSelected(False)

        self.redraw()
        
    def toggleSolid(self):
        self.selectedHuman.setSolid(not self.selectedHuman.isSolid())
        self.redraw()
        
    def toggleSubdivision(self):
        self.selectedHuman.setSubdivided(not self.selectedHuman.isSubdivided(), True, gui3d.app.progress)
        self.redraw()
        
    def saveTarget(self):
        human = self.selectedHuman
        algos3d.saveTranslationTarget(human.meshData, "full_target.target")
        print "Full target exported"
        
    def quickExport(self):
        exportPath = mh.getPath('exports')
        if not os.path.exists(exportPath):
            os.makedirs(exportPath)
        mh2obj.exportObj(self.selectedHuman.meshData, exportPath + '/quick_export.obj')
        mh2bvh.exportSkeleton(self.selectedHuman.meshData, exportPath + '/quick_export.bvh')
        mh2mhx.exportMhx(self.selectedHuman.meshData, exportPath + '/quick_export.mhx')
        
    def grabScreen(self):
        grabPath = mh.getPath('grab')
        if not os.path.exists(grabPath):
            os.makedirs(grabPath)
        # TODO: use bbox to choose grab region
        mh.grabScreen(180, 80, 440, 440, os.path.join(grabPath, 'grab.bmp'))
        
    # Camera navigation
    def rotateDown(self):
        human = self.selectedHuman
        rot = human.getRotation()
        rot[0] += 5.0
        human.setRotation(rot)
        self.redraw()
        
    def rotateLeft(self):
        human = self.selectedHuman
        rot = human.getRotation()
        rot[1] -= 5.0
        human.setRotation(rot)
        self.redraw()
        
    def rotateRight(self):
        human = self.selectedHuman
        rot = human.getRotation()
        rot[1] += 5.0
        human.setRotation(rot)
        self.redraw()
        
    def rotateUp(self):
        human = self.selectedHuman
        rot = human.getRotation()
        rot[0] -= 5.0
        human.setRotation(rot)
        self.redraw()
        
    def panUp(self):
        human = self.selectedHuman
        trans = human.getPosition()
        trans[1] += 0.05
        human.setPosition(trans)
        self.redraw()
                    
    def panDown(self):
        human = self.selectedHuman
        trans = human.getPosition()
        trans[1] -= 0.05
        human.setPosition(trans)
        self.redraw()      
        
    def panRight(self):
        human = self.selectedHuman
        trans = human.getPosition()
        trans[0] += 0.05
        human.setPosition(trans)
        self.redraw()
        
    def panLeft(self):
        human = self.selectedHuman
        trans = human.getPosition()
        trans[0] -= 0.05
        human.setPosition(trans)
        self.redraw()
        
    def zoomOut(self):
        speed = gui3d.app.settings.get('highspeed', 5) if mh.getKeyModifiers() & mh.Modifiers.SHIFT else gui3d.app.settings.get('lowspeed', 1)
        self.modelCamera.eyeZ += 0.65 * speed
        self.redraw()
        
    def zoomIn(self):
        speed = gui3d.app.settings.get('highspeed', 5) if mh.getKeyModifiers() & mh.Modifiers.SHIFT else gui3d.app.settings.get('lowspeed', 1)
        self.modelCamera.eyeZ -= 0.65 * speed
        self.redraw()
        
    def frontView(self):
        animation3d.animate(self, 0.20, [animation3d.RotateAction(self.selectedHuman, self.selectedHuman.getRotation(), [0.0, 0.0, 0.0])])
        
    def rightView(self):
        animation3d.animate(self, 0.20, [animation3d.RotateAction(self.selectedHuman, self.selectedHuman.getRotation(), [0.0, -90.0, 0.0])])
        
    def topView(self):
        animation3d.animate(self, 0.20, [animation3d.RotateAction(self.selectedHuman, self.selectedHuman.getRotation(), [90.0, 0.0, 0.0])])
        
    def backView(self):
        animation3d.animate(self, 0.20, [animation3d.RotateAction(self.selectedHuman, self.selectedHuman.getRotation(), [0.0, 180.0, 0.0])])
        
    def leftView(self):
        animation3d.animate(self, 0.20, [animation3d.RotateAction(self.selectedHuman, self.selectedHuman.getRotation(), [0.0, 90.0, 0.0])])
        
    def bottomView(self):
        animation3d.animate(self, 0.20, [animation3d.RotateAction(self.selectedHuman, self.selectedHuman.getRotation(), [-90.0, 0.0, 0.0])])
        
    def resetView(self):
        cam = self.modelCamera
        animation3d.animate(self, 0.20, [animation3d.RotateAction(self.selectedHuman, self.selectedHuman.getRotation(), [0.0, 0.0, 0.0]),
            animation3d.CameraAction(cam, None,
            [cam.eyeX, cam.eyeY, 60.0, cam.focusX, cam.focusY, cam.focusZ, 0, 1, 0])])
        
    # Mouse actions    
    def mouseTranslate(self, event):
            
        speed = gui3d.app.settings.get('highspeed', 5) if mh.getKeyModifiers() & mh.Modifiers.SHIFT else gui3d.app.settings.get('lowspeed', 1)
        
        human = self.selectedHuman
        trans = human.getPosition()
        trans = self.modelCamera.convertToScreen(trans[0], trans[1], trans[2])
        trans[0] += event.dx * speed
        trans[1] += event.dy * speed
        trans = self.modelCamera.convertToWorld3D(trans[0], trans[1], trans[2])
        human.setPosition(trans)

    def mouseRotate(self, event):
        
        speed = gui3d.app.settings.get('highspeed', 5) if mh.getKeyModifiers() & mh.Modifiers.SHIFT else gui3d.app.settings.get('lowspeed', 1)
        
        human = self.selectedHuman
        rot = human.getRotation()
        rot[0] += 0.5 * event.dy * speed
        rot[1] += 0.5 * event.dx * speed
        human.setRotation(rot)
        
    def mouseZoom(self, event):
    
        speed = gui3d.app.settings.get('highspeed', 5) if mh.getKeyModifiers() & mh.Modifiers.SHIFT else gui3d.app.settings.get('lowspeed', 1)
        
        if gui3d.app.settings.get('invertMouseWheel', False):
            speed *= -1
        
        self.modelCamera.eyeZ -= 0.05 * event.dy * speed
        
    def promptAndExit(self):
        if self.undoStack:
            self.prompt('Exit', 'You have unsaved changes. Are you sure you want to exit the application?', 'Yes', 'No', self.stop)
        else:
            self.stop()
    
application = MHApplication()
application.run()

#import cProfile
#cProfile.run('application.run()')
