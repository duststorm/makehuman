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
sys.path.append("./shared")
sys.path.append("./shared/mhx/templates")
sys.path.append("./shared/mhx")
sys.path=sys.path + recursiveDirNames("./apps")
sys.path.append("./core")
sys.path=sys.path + recursiveDirNames("./core")

import subprocess
import webbrowser
import glob, imp
from os.path import join, basename, splitext

import mh
import gui3d, events3d, font3d
import mh2obj, mh2bvh, mh2mhx
import human
import guimodelling, guifiles#, guirender
from aljabr import centroid
import algos3d
#import font3d

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
        
        self.settings = {
            'realtimeUpdates': True,
            'realtimeNormalUpdates': True,
            'shader': None,
            'lowspeed': 1,
            'highspeed': 5
        }
        
        self.shortcuts = {
            # Actions
            (events3d.KMOD_CTRL, events3d.SDLK_z): self.undo,
            (events3d.KMOD_CTRL, events3d.SDLK_y): self.redo,
            (events3d.KMOD_CTRL, events3d.SDLK_m): self.goToModelling,
            (events3d.KMOD_CTRL, events3d.SDLK_s): self.goToSave,
            (events3d.KMOD_CTRL, events3d.SDLK_l): self.goToLoad,
            (events3d.KMOD_CTRL, events3d.SDLK_e): self.goToExport,
            (events3d.KMOD_CTRL, events3d.SDLK_r): self.goToRendering,
            (events3d.KMOD_CTRL, events3d.SDLK_h): self.goToHelp,
            (events3d.KMOD_CTRL, events3d.SDLK_q): self.stop,
            (events3d.KMOD_CTRL, events3d.SDLK_w): self.toggleStereo,
            (events3d.KMOD_CTRL, events3d.SDLK_f): self.toggleSolid,
            (events3d.KMOD_ALT, events3d.SDLK_t): self.saveTarget,
            (events3d.KMOD_ALT, events3d.SDLK_e): self.quickExport,
            (events3d.KMOD_ALT, events3d.SDLK_s): self.toggleSubdivision,
            (events3d.KMOD_ALT, events3d.SDLK_g): self.grabScreen,
            # Camera navigation
            (0, events3d.SDLK_2): self.rotateDown,
            (0, events3d.SDLK_4): self.rotateLeft,
            (0, events3d.SDLK_6): self.rotateRight,
            (0, events3d.SDLK_8): self.rotateUp,
            (0, events3d.SDLK_UP): self.panUp,
            (0, events3d.SDLK_DOWN): self.panDown,
            (0, events3d.SDLK_RIGHT): self.panRight,
            (0, events3d.SDLK_LEFT): self.panLeft,
            (0, events3d.SDLK_PLUS): self.zoomIn,
            (0, events3d.SDLK_MINUS): self.zoomOut,
            (0, events3d.SDLK_7): self.sideView,
            (0, events3d.SDLK_1): self.frontView,
            (0, events3d.SDLK_3): self.topView,
            (0, events3d.SDLK_PERIOD): self.resetView
        }
        
        self.loadSettings()
        
        self.loadHandlers = {}
        self.saveHandlers = []
        
        # Display the initial splash screen and the progress bar during startup
        mesh = gui3d.RectangleMesh(800, 600, self.app.getThemeResource('images', 'splash.png'))
        self.splash = gui3d.Object(self, [0, 0, 9.8], mesh)
        self.progressBar = gui3d.ProgressBar(self, [800-150, 600-15, 9.85])
        self.scene3d.update()
        self.redrawNow()

    def loadBackground(self):

        self.progressBar.setProgress(0.1)

        self.upperbar = gui3d.Object(self, [0, 0, 9], gui3d.RectangleMesh(800, 32, self.getThemeResource("images", "upperbar.png")))
        self.background = gui3d.Object(self, [0, 0, -89.99], gui3d.RectangleMesh(800, 600, self.getThemeResource("images", "background.png")))
        self.lowerbar = gui3d.Object(self, [0, 32, 9], gui3d.RectangleMesh(800, 32, self.getThemeResource("images", "lowerbar.png")))
        self.statusbar = gui3d.Object(self, [0, 580, 9], gui3d.RectangleMesh(800, 32, self.getThemeResource("images", "lowerbar.png")))
        
        mh.callAsync(self.loadHuman)
        
    def loadHuman(self):   

        self.progressBar.setProgress(0.2)
        #hairObj = hair.loadHairsFile(self.scene3d, path="./data/hairs/default", update = False)
        #self.scene3d.clear(hairObj) 
        self.selectedHuman = human.Human(self.scene3d, "data/3dobjs/base.obj")
        self.selectedHuman.setTexture("data/textures/texture.tif")
        
        mh.callAsync(self.loadMainGui)
        
    def loadMainGui(self):
        
        self.progressBar.setProgress(0.3)

        self.tool = None
        self.selectedGroup = None

        self.undoStack = []
        self.redoStack = []

        @self.selectedHuman.event
        def onMouseDown(event):
          if self.tool:
            self.selectedGroup = self.app.scene3d.getSelectedFacesGroup()
            self.tool.callEvent("onMouseDown", event)
          else:
            self.currentTask.callEvent("onMouseDown", event)

        @self.selectedHuman.event
        def onMouseMoved(event):
          if self.tool:
            self.tool.callEvent("onMouseMoved", event)
          else:
            self.currentTask.callEvent("onMouseMoved", event)

        @self.selectedHuman.event
        def onMouseDragged(event):
          if self.tool:
            self.tool.callEvent("onMouseDragged", event)
          else:
            self.currentTask.callEvent("onMouseDragged", event)

        @self.selectedHuman.event
        def onMouseUp(event):
          if self.tool:
            self.tool.callEvent("onMouseUp", event)
          else:
            self.currentTask.callEvent("onMouseUp", event)

        @self.selectedHuman.event
        def onMouseEntered(event):
          if self.tool:
            self.tool.callEvent("onMouseEntered", event)
          else:
            self.currentTask.callEvent("onMouseEntered", event)

        @self.selectedHuman.event
        def onMouseExited(event):
          if self.tool:
            self.tool.callEvent("onMouseExited", event)
          else:
            self.currentTask.callEvent("onMouseExited", event)
            
        @self.selectedHuman.event
        def onChanged(event):
            
            for category in self.categories.itervalues():
                
                for task in category.tasks:
                    
                    task.callEvent('onHumanChanged', event)

        # Set up categories and tasks
        
        guimodelling.ModellingCategory(self)
        guifiles.FilesCategory(self)
        
        mh.callAsync(self.loadPlugins)
        
    def loadPlugins(self):
        
        self.progressBar.setProgress(0.4)

        # Load plugins not starting with _    
        self.modules = {}
        
        self.pluginsToLoad = glob.glob(join("plugins/",'[!_]*.py'))
        self.pluginsToLoad.reverse()
        
        mh.callAsync(self.loadNextPlugin)
    
    def loadNextPlugin(self):
        
        alreadyLoaded = len(self.modules)
        stillToLoad = len(self.pluginsToLoad)
        self.progressBar.setProgress(0.4 + (float(alreadyLoaded) / float(alreadyLoaded + stillToLoad)) * 0.4)
        
        if stillToLoad:
            
            path = self.pluginsToLoad.pop()
            try:
                name, ext = splitext(basename(path))
                module = imp.load_source(name, path)
                self.modules[name] = module
                module.load(self)
            except Exception, e:
                print('Could not load %s' % name)
                print e
                
            mh.callAsync(self.loadNextPlugin)
            
        else:
            
            mh.callAsync(self.loadGui)
                
    def loadGui(self):
        
        self.progressBar.setProgress(0.9)

        category = gui3d.Category(self, "Help", style=gui3d.CategoryButtonStyle)
        # Help button
        @category.button.event
        def onClicked(event):
          webbrowser.open(os.getcwd()+"/docs/MH_Users_Guide.pdf");
          
        # Exit button
        category = gui3d.Category(self, "Exit", style=gui3d.CategoryButtonStyle)
        @category.button.event
        def onClicked(event):
          self.stop()
          
        self.undoButton = gui3d.Button(self, [650, 508, 9.1], "Undo", style=gui3d.ButtonStyle._replace(width=40, height=16))
        self.redoButton = gui3d.Button(self, [694, 508, 9.1], "Redo", style=gui3d.ButtonStyle._replace(width=40, height=16))
        self.resetButton = gui3d.Button(self, [738, 508, 9.1], "Reset", style=gui3d.ButtonStyle._replace(width=40, height=16))
                                        
        @self.undoButton.event
        def onClicked(event):
            self.app.undo()

        @self.redoButton.event
        def onClicked(event):
            self.app.redo()

        @self.resetButton.event
        def onClicked(event):
            human = self.selectedHuman
            human.resetMeshValues()
            human.applyAllTargets(self.progress)
          
        self.globalButton = gui3d.Button(self, [650, 530, 9.2], "Global cam", style=gui3d.ButtonStyle._replace(width=128, height=20))
        self.faceButton = gui3d.Button(self, [650, 555, 9.2], "Face cam", style=gui3d.ButtonStyle._replace(width=128, height=20))
        
        @self.globalButton.event
        def onClicked(event):
          self.app.setGlobalCamera()
          
        @self.faceButton.event
        def onClicked(event):
          self.app.setFaceCamera()

        self.switchCategory("Modelling")

        self.progressBar.setProgress(1.0)
        self.progressBar.hide()
        
        mh.callAsync(self.loadFinish)
                
    def loadFinish(self):
        
        self.selectedHuman.callEvent('onChanged', human.HumanEvent(self.selectedHuman, 'reset'))
        self.selectedHuman.applyAllTargets(self.app.progress)
        self.scene3d.update()
        self.splash.hide()
        mh.updatePickingBuffer();
        self.redraw()
        
    # Events
    def onStart(self, event):
        
        mh.callAsync(self.loadBackground)
        
    def onMouseDragged(self, event):
        if self.selectedHuman.isVisible():
            leftButtonDown = event.button & 1
            middleButtonDown = event.button & 2
            rightButtonDown = event.button & 4
            
            speed = self.app.settings.get('highspeed', 5) if mh.getKeyModifiers() & events3d.KMOD_SHIFT else self.app.settings.get('lowspeed', 1)

            if leftButtonDown and rightButtonDown or middleButtonDown:
                mh.cameras[0].eyeZ += 0.05 * event.dy * speed
            elif leftButtonDown:
                human = self.selectedHuman
                rot = human.getRotation()
                rot[0] += 0.5 * event.dy * speed
                rot[1] += 0.5 * event.dx * speed
                human.setRotation(rot)
            elif rightButtonDown:
                human = self.selectedHuman
                trans = human.getPosition()
                trans = self.modelCamera.convertToScreen(trans[0], trans[1], trans[2])
                trans[0] += event.dx * speed
                trans[1] += event.dy * speed
                trans = self.modelCamera.convertToWorld3D(trans[0], trans[1], trans[2])
                human.setPosition(trans)

    def onMouseWheel(self, event):
        if self.selectedHuman.isVisible():
            if event.wheelDelta > 0:
                self.zoomOut()
            else:
                self.zoomIn()

    def onKeyDown(self, event):
        
        # Normalize modifiers
        modifiers = 0
        if (event.modifiers & events3d.KMOD_CTRL) and (event.modifiers & events3d.KMOD_ALT):
            modifiers = events3d.KMOD_CTRL | events3d.KMOD_ALT
        elif event.modifiers & events3d.KMOD_CTRL:
            modifiers = events3d.KMOD_CTRL
        elif event.modifiers & events3d.KMOD_ALT:
            modifiers = events3d.KMOD_ALT
            
        # Normalize key
        key = event.key
        if key in xrange(events3d.SDLK_KP0, events3d.SDLK_KP9 + 1):
            key = events3d.SDLK_0 + key - events3d.SDLK_KP0
        elif key == events3d.SDLK_KP_PERIOD:
            key = events3d.SDLK_PERIOD
        elif key == events3d.SDLK_KP_MINUS:
            key = events3d.SDLK_MINUS
        elif key == events3d.SDLK_KP_PLUS:
            key = events3d.SDLK_PLUS
            
        if (modifiers, key) in self.shortcuts:
            self.shortcuts[(modifiers, key)]()
            
    def onResized(self, event):

        self.upperbar.mesh.resize(event[0], 32)
        self.background.mesh.resize(event[0], event[1])
        self.lowerbar.mesh.resize(event[0], 32)
        self.statusbar.mesh.resize(event[0], 32)
        self.statusbar.setPosition((0.0, event[1]-20, 9))
        
        self.undoButton.setPosition([event[0]-150, event[1]-92, 9.1])
        self.redoButton.setPosition([event[0]-106, event[1]-92, 9.1])
        self.resetButton.setPosition([event[0]-62, event[1]-92, 9.1])
        
        self.globalButton.setPosition([event[0]-150, event[1]-70, 9.1])
        self.faceButton.setPosition([event[0]-150, event[1]-45, 9.1])
        
        self.progressBar.setPosition([event[0]-150, event[1]-15, 9.85])
        
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
        if os.path.isfile("settings.ini"):
            f = open("settings.ini", 'r')
            settings = eval(f.read())
            self.settings.update(settings)
        
        if os.path.isfile("shortcuts.ini"):
            self.shortcuts = {}
            f = open("shortcuts.ini", 'r')
            for line in f:
                modifier, key, method = line.split(' ')
                #print modifier, key, method[0:-1]
                if hasattr(self, method[0:-1]):
                    self.shortcuts[(int(modifier), int(key))] = getattr(self, method[0:-1])
        
    def saveSettings(self):
        f = open("settings.ini", 'w')
        f.write(repr(self.settings))
        
        f = open("shortcuts.ini", 'w')
        for shortcut, method in self.shortcuts.iteritems():
            f.write('%d %d %s\n' % (shortcut[0], shortcut[1], method.__name__))

    # Themes
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
        if '/' in id:
            return id
        if os.path.exists("data/themes/" + self.theme + "/" + folder + "/"+ id):
            return "data/themes/" + self.theme + "/" + folder + "/"+ id
        else:
            return "data/themes/default/" + folder + "/"+ id
      
    # Font resources
    def getFont(self, fontFamily):
        if fontFamily not in self.fonts:
            self.fonts[fontFamily] = font3d.Font("data/fonts/%s.fnt" % fontFamily)
        return self.fonts[fontFamily]

    # Global progress bar
    def progress(self, value):
        self.progressBar.setProgress(value)
        if value <= 0:
            self.progressBar.show()
        elif value >= 1.0:
            self.progressBar.hide()
      
    # Camera's
    def setGlobalCamera(self):
        self.modelCamera.eyeX = 0
        self.modelCamera.eyeY = 0
        self.modelCamera.eyeZ = 60
        self.modelCamera.focusX = 0
        self.modelCamera.focusY = 0
        self.modelCamera.focusZ = 0
  
    def setFaceCamera(self):
        human = self.selectedHuman
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
        
    # Shortcuts
    def setShortcut(self, modifier, key, method):
        
        shortcut = (modifier, key)
        
        if shortcut in self.shortcuts:
            print 'Shortcut is in use'
            return False
            
        # Remove old entry
        for s, m in self.shortcuts.iteritems():
            if m == method:
                del self.shortcuts[s]
                break
                
        self.shortcuts[shortcut] = method
        
        for shortcut, m in self.shortcuts.iteritems():
            print shortcut, m
        
        return True
        
    def getShortcut(self, method):
        
        for shortcut, m in self.shortcuts.iteritems():
            if m == method:
                return shortcut
                
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
        webbrowser.open(os.getcwd()+"/docs/MH_Users_Guide.pdf");
          
    def toggleStereo(self):
        stereoMode = mh.cameras[0].stereoMode
        stereoMode += 1
        if stereoMode > 2:
            stereoMode = 0
        mh.cameras[0].stereoMode = stereoMode

        # We need a black background for stereo
        background = self.categories["Modelling"].background
        if stereoMode:
            color = [  0,   0,   0, 255]
            self.categories["Modelling"].anaglyphsButton.setSelected(True)
        else:
            color = [255, 255, 255, 255]
            self.categories["Modelling"].anaglyphsButton.setSelected(False)
        for g in background.mesh.facesGroups:
            g.setColor(color)

        self.redraw()
        
    def toggleSolid(self):
        if self.selectedHuman.mesh.solid:
            self.selectedHuman.mesh.setSolid(0)
        else:
            self.selectedHuman.mesh.setSolid(1)
        self.redraw()
        
    def toggleSubdivision(self):
        self.selectedHuman.setSubdivided(not self.selectedHuman.isSubdivided(), True, self.app.progress)
        
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
        self.scene3d.grabScreen(180, 80, 440, 440, os.path.join(grabPath, 'grab.bmp'))
        
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
        speed = self.app.settings.get('highspeed', 5) if mh.getKeyModifiers() & events3d.KMOD_SHIFT else self.app.settings.get('lowspeed', 1)
        mh.cameras[0].eyeZ += 0.65 * speed
        self.redraw()
        
    def zoomIn(self):
        speed = self.app.settings.get('highspeed', 5) if mh.getKeyModifiers() & events3d.KMOD_SHIFT else self.app.settings.get('lowspeed', 1)
        mh.cameras[0].eyeZ -= 0.65 * speed
        self.redraw()
        
    def topView(self):
        self.selectedHuman.setRotation([90.0, 0.0, 0.0])
        self.redraw()
        
    def frontView(self):
        self.selectedHuman.setRotation([0.0, 0.0, 0.0])
        self.redraw()
        
    def sideView(self):
        self.selectedHuman.setRotation([0.0, 90.0, 0.0])
        self.redraw()
        
    def resetView(self):
        self.selectedHuman.setPosition([0.0, 0.0, 0.0])
        mh.cameras[0].eyeZ = 60.0
        self.redraw()
    
application = MHApplication()
application.run()

#import cProfile
#cProfile.run('application.run()')
