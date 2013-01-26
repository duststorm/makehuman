#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import sys
import os
import glob
import imp
import contextlib

from core import G
import mh
import events3d
import files3d
import gui3d
import animation3d
import human
import guifiles
from aljabr import centroid
import algos3d
#import posemode
import gui
import language as lang
import log

@contextlib.contextmanager
def outFile(path):
    path = os.path.join(mh.getPath(''), path)
    tmppath = path + '.tmp'
    try:
        with open(tmppath, 'w') as f:
            yield f
        if os.path.exists(path):
            os.remove(path)
        os.rename(tmppath, path)
    except:
        if os.path.exists(tmppath):
            os.remove(tmppath)
        log.error('unable to save file %s', path, exc_info=True)

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

        self.scroll = self.addTopWidget(gui.VScrollArea())
        self.pluginsBox = gui.GroupBox('Plugins')
        self.pluginsBox.setSizePolicy(
            gui.SizePolicy.MinimumExpanding,
            gui.SizePolicy.MinimumExpanding)
        self.scroll.setWidget(self.pluginsBox)

        for module in sorted(gui3d.app.modules):
            check = self.pluginsBox.addWidget(PluginCheckBox(module))

class MHApplication(gui3d.Application, mh.Application):
    def __init__(self):
        if G.app is not None:
            raise RuntimeError('MHApplication is a singleton')
        G.app = self
        gui3d.Application.__init__(self)
        mh.Application.__init__(self)

        self.shortcuts = {
            # Actions
            'undo':		(mh.Modifiers.CTRL, mh.Keys.z),
            'redo':		(mh.Modifiers.CTRL, mh.Keys.y),
            'modelling':	(mh.Modifiers.CTRL, mh.Keys.m),
            'save':		(mh.Modifiers.CTRL, mh.Keys.s),
            'load':		(mh.Modifiers.CTRL, mh.Keys.l),
            'export':		(mh.Modifiers.CTRL, mh.Keys.e),
            'rendering':	(mh.Modifiers.CTRL, mh.Keys.r),
            'help':		(mh.Modifiers.CTRL, mh.Keys.h),
            'exit':		(mh.Modifiers.CTRL, mh.Keys.q),
            'stereo':		(mh.Modifiers.CTRL, mh.Keys.w),
            'wireframe':	(mh.Modifiers.CTRL, mh.Keys.f),
            'savetgt':		(mh.Modifiers.ALT, mh.Keys.t),
            'qexport':		(mh.Modifiers.ALT, mh.Keys.e),
            'smooth':		(mh.Modifiers.ALT, mh.Keys.s),
            'grab':		(mh.Modifiers.ALT, mh.Keys.g),
            'profiling':	(mh.Modifiers.ALT, mh.Keys.p),
            # Camera navigation
            'rotateD':		(0, mh.Keys.N2),
            'rotateL':		(0, mh.Keys.N4),
            'rotateR':		(0, mh.Keys.N6),
            'rotateU':		(0, mh.Keys.N8),
            'panU':		(0, mh.Keys.UP),
            'panD':		(0, mh.Keys.DOWN),
            'panR':		(0, mh.Keys.RIGHT),
            'panL':		(0, mh.Keys.LEFT),
            'zoomIn':		(0, mh.Keys.PLUS),
            'zoomOut':		(0, mh.Keys.MINUS),
            'front':		(0, mh.Keys.N1),
            'right':		(0, mh.Keys.N3),
            'top':		(0, mh.Keys.N7),
            'back':		(mh.Modifiers.CTRL, mh.Keys.N1),
            'left':		(mh.Modifiers.CTRL, mh.Keys.N3),
            'bottom':		(mh.Modifiers.CTRL, mh.Keys.N7),
            'resetCam':		(0, mh.Keys.PERIOD),
            # Version check
            '_versionSentinel':	(0, 0x87654321)
        }

        self.mouseActions = {
            (0, mh.Buttons.RIGHT_MASK): self.mouseTranslate,
            (0, mh.Buttons.LEFT_MASK): self.mouseRotate,
            (0, mh.Buttons.MIDDLE_MASK): self.mouseZoom
        }

        self.settings = {
            'realtimeUpdates': True,
            'realtimeNormalUpdates': True,
            'cameraAutoZoom': True,
            'shader': None,
            'lowspeed': 1,
            'highspeed': 5,
            'units':'metric',
            'invertMouseWheel':False,
            'font':'arial',
            'language':'english',
            'excludePlugins':[],
            'rtl': False,
            'sliderImages': False
        }

        self.fonts = {}

        self.loadHandlers = {}
        self.saveHandlers = []

        self.dialog = None
        self.helpIds = set()

        self.tool = None
        self.selectedGroup = None

        self.undoStack = []
        self.redoStack = []
        self.modified = False

        self.actions = None

        self.clearColor = [0.5, 0.5, 0.5]

        self.modules = {}

        self.selectedHuman = None

        self.theme = None

        self.modelCamera = mh.Camera()

        @self.modelCamera.mhEvent
        def onChanged(event):
            for category in self.categories.itervalues():
                for task in category.tasks:
                    task.callEvent('onCameraChanged', event)

        mh.cameras.append(self.modelCamera)

        self.guiCamera = mh.Camera()
        self.guiCamera._fovAngle = 45
        self.guiCamera._eyeZ = 10
        self.guiCamera._projection = 0

        mh.cameras.append(self.guiCamera)

    def _versionSentinel(self):
        # dummy method used for checking the shortcuts.ini version
        pass

    def loadHuman(self):

        self.progress(0.1)
        #hairObj = hair.loadHairsFile(self.scene3d, path="./data/hairs/default", update = False)
        #self.scene3d.clear(hairObj)
        self.selectedHuman = self.addObject(human.Human(files3d.loadMesh("data/3dobjs/base.obj")))

    def loadMainGui(self):

        self.progress(0.2)

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
        self.getCategory("Modelling")
        self.addCategory(guifiles.FilesCategory())

    def loadPlugins(self):

        self.progress(0.4)

        # Load plugins not starting with _
        self.pluginsToLoad = glob.glob(os.path.join("plugins/",'[!_]*.py'))
        self.pluginsToLoad.sort()
        self.pluginsToLoad.reverse()

        while self.pluginsToLoad:
            self.loadNextPlugin()

    def loadNextPlugin(self):

        alreadyLoaded = len(self.modules)
        stillToLoad = len(self.pluginsToLoad)
        self.progress(0.4 + (float(alreadyLoaded) / float(alreadyLoaded + stillToLoad)) * 0.4)

        if not stillToLoad:
            return

        path = self.pluginsToLoad.pop()
        try:
            name, ext = os.path.splitext(os.path.basename(path))
            if name not in self.settings['excludePlugins']:
                log.message('Importing plugin %s', name)
                module = imp.load_source(name, path)
                self.modules[name] = module
                log.message('Imported plugin %s', name)
                log.message('Loading plugin %s', name)
                module.load(self)
                log.message('Loaded plugin %s', name)
                self.processEvents()
            else:
                self.modules[name] = None
        except Exception, e:
            log.warning('Could not load %s', name, exc_info=True)

    def unloadPlugins(self):

        for name, module in self.modules.iteritems():
            if module is None:
                continue
            try:
                log.message('Unloading plugin %s', name)
                module.unload(self)
                log.message('Unloaded plugin %s', name)
            except Exception, e:
                log.warning('Could not unload %s', name, exc_info=True)

    def loadGui(self):

        self.progress(0.9)

        category = self.getCategory('Settings')
        category.addTask(PluginsTaskView(category))

        # Exit button
        category = self.getCategory("Exit")
        @category.tab.mhEvent
        def onClicked(event):
            self.promptAndExit()

        """
        self.poseModeBox = self.buttonBox.addWidget(gui.CheckBox("Pose mode", False))

        @self.poseModeBox.mhEvent
        def onClicked(event):
          print dir(event)
          if self.poseModeBox.selected:
            posemode.exitPoseMode()
          else:
            posemode.enterPoseMode()
        """

        mh.refreshLayout()

        self.switchCategory("Modelling")

        self.progress(1.0)
        # self.progressBar.hide()

    def loadFinish(self):

        self.selectedHuman.applyAllTargets(gui3d.app.progress)
        self.selectedHuman.callEvent('onChanged', events3d.HumanEvent(self.selectedHuman, 'reset'))

        self.prompt('Warning', 'This is an alpha release, which means that there are still bugs present and features missing. Use at your own risk.',
            'OK', helpId='alphaWarning')
        # self.splash.hide()

        gui3d.app.setFilenameCaption("Untitled")
        self.setFileModified(False)

        #printtree(self)

        mh.updatePickingBuffer();
        self.redraw()

    def startupSequence(self):
        self.splash.setFormat('<br><br><b><font size="48" color="#ff0000">%s</font></b>')

        log.message('Loading human')
        self.loadHuman()

        log.message('Loading main GUI')
        self.loadMainGui()

        log.message('Loading fonts')
        self.loadFonts()

        log.message('Loading plugins')
        self.loadPlugins()

        log.message('Loading GUI')
        self.loadGui()

        log.message('Loading theme')
        try:
            self.setTheme(self.settings.get('guiTheme', 'default'))
        except:
            self.setTheme("default")

        log.message('Applying targets')
        self.loadFinish()

        log.message('Loading done')
        log.message('')

        if sys.platform.startswith("darwin"):
            self.splash.resize(0,0) # work-around for mac splash-screen closing bug

        self.splash.hide()
        # self.splash.finish(self.mainwin)

    # Events
    def onStart(self, event):
        self.startupSequence()

    def onStop(self, event):

        self.saveSettings(True)
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

    # Undo-redo
    def do(self, action):
        if action.do():
            self.undoStack.append(action)
            del self.redoStack[:]
            self.setFileModified(True)
            log.message('do %s', action.name)
            self.redraw()

    def did(self, action):
        self.undoStack.append(action)
        self.setFileModified(True)
        del self.redoStack[:]
        log.message('did %s', action.name)
        self.redraw()

    def undo(self):
        if self.undoStack:
            action = self.undoStack.pop()
            log.message('undo %s', action.name)
            action.undo()
            self.redoStack.append(action)
            self.setFileModified(True)
            self.redraw()

    def redo(self):
        if self.redoStack:
            action = self.redoStack.pop()
            log.message('redo %s', action.name)
            action.do()
            self.undoStack.append(action)
            self.setFileModified(True)
            self.redraw()

    # Settings

    def loadSettings(self):
        try:
            if os.path.isfile(os.path.join(mh.getPath(''), "settings.ini")):
                with open(os.path.join(mh.getPath(''), "settings.ini"), 'r') as f:
                    settings = mh.parseINI(f.read())
                self.settings.update(settings)
        except:
            log.error('Failed to load settings')

        if 'language' in gui3d.app.settings:
            self.setLanguage(gui3d.app.settings['language'])

        gui.Slider.showImages(gui3d.app.settings['sliderImages'])

        try:
            if os.path.isfile(os.path.join(mh.getPath(''), "shortcuts.ini")):
                shortcuts = {}
                f = open(os.path.join(mh.getPath(''), "shortcuts.ini"), 'r')
                for line in f:
                    modifier, key, action = line.strip().split(' ')
                    shortcuts[action] = (int(modifier), int(key))
                f.close()
                if shortcuts.get('_versionSentinel') != (0, 0x87654321):
                    log.warning('shortcuts.ini out of date; ignoring')
                else:
                    self.shortcuts.update(shortcuts)
        except:
            log.error('Failed to load shortcut settings')

        try:
            if os.path.isfile(os.path.join(mh.getPath(''), "mouse.ini")):
                self.mouseActions = {}
                f = open(os.path.join(mh.getPath(''), "mouse.ini"), 'r')
                for line in f:
                    modifier, button, method = line.strip().split(' ')
                    if hasattr(self, method):
                        self.mouseActions[(int(modifier), int(button))] = getattr(self, method)
                f.close()
        except:
            log.error('Failed to load mouse settings')

        try:
            if os.path.isfile(os.path.join(mh.getPath(''), "help.ini")):
                self.helpIds = set()
                f = open(os.path.join(mh.getPath(''), "help.ini"), 'r')
                for line in f:
                    self.helpIds.add(line[0:-1])
                f.close()
                if self.dialog is not None:
                    self.dialog.helpIds.update(self.helpIds)
        except:
            log.error('Failed to load help settings')

    def saveSettings(self, promptOnFail=False):
        try:
            if not os.path.exists(mh.getPath('')):
                os.makedirs(mh.getPath(''))

            with outFile("settings.ini") as f:
                f.write(mh.formatINI(self.settings))

            with outFile("shortcuts.ini") as f:
                for action, shortcut in self.shortcuts.iteritems():
                    f.write('%d %d %s\n' % (shortcut[0], shortcut[1], action))

            with outFile("mouse.ini") as f:
                for mouseAction, method in self.mouseActions.iteritems():
                    f.write('%d %d %s\n' % (mouseAction[0], mouseAction[1], method.__name__))

            if self.dialog is not None:
                self.helpIds.update(self.dialog.helpIds)

            with outFile("help.ini") as f:
                for helpId in self.helpIds:
                    f.write('%s\n' % helpId)
        except:
            log.error('Failed to save settings file', exc_info=True)
            if promptOnFail:
                self.prompt('Error', 'Could not save settings file.', 'OK')

    # Themes
    def setTheme(self, theme):

        if self.theme == theme:
            return

        f = open(os.path.join("data/themes/", theme + ".mht"), 'r')

        for data in f.readlines():
            lineData = data.split()

            if len(lineData) > 0:
                if lineData[0] == "version":
                    log.message('Version %s', lineData[1])
                elif lineData[0] == "color":
                    if lineData[1] == "clear":
                        self.clearColor[:] = [float(val) for val in lineData[2:5]]
                        mh.setClearColor(float(lineData[2]), float(lineData[3]), float(lineData[4]), 1.0)
        log.debug("Loaded theme %s", 'data/themes/'+theme+'.mht')

        try:
            f = open('data/themes/%s.qss' % theme, 'r')
            qStyle = "\n".join(f.readlines())
            self.setStyleSheet(qStyle)
            # Also set stylesheet on custom slider style
            for widget in self.allWidgets():
                if isinstance(widget, gui.Slider):
                    widget.setStyleSheet(qStyle)
            log.debug("Loaded Qt style %s", 'data/themes/'+theme+'.qss')
        except:
            self.setStyleSheet("")
            # Also set stylesheet on custom slider style
            for widget in self.allWidgets():
                if isinstance(widget, gui.Slider):
                    widget.setStyleSheet("")
            '''
            if theme != "default":
                log.warning('Could not open Qt style file %s.', 'data/themes/'+theme+'.qss')
            '''

        self.theme = theme
        self.reloadIcons()
        self.redraw()

    def reloadIcons(self):
        if not self.actions:
            return
        for action in self.actions:
            action.setIcon(gui.Action.getIcon(action.name))

    def loadFonts(self):
        """
        Load custom fonts from data/fonts folder to make them available for theming.
        """
        self.customFonts = []
        fontFiles = [os.path.join('data/fonts', filename) for filename in os.listdir('data/fonts') if filename.split(os.extsep)[-1] == "ttf"]
        for font in fontFiles:
            try:
                fontHandle = gui.QtGui.QFontDatabase.addApplicationFont(font)
                log.debug("Loading font file %s", font)
                if fontHandle != -1:
                    fontFamilies = gui.QtGui.QFontDatabase.applicationFontFamilies(fontHandle)
                    for f in fontFamilies:
                        self.customFonts.append(str(f))
                        log.debug("Added font family %s", f)
            except:
                log.warning("Error loading font file %s", font)

    def getCustomFonts(self):
        """
        Returns the font family names of all custom fonts loaded from the
        data/fonts folder. These fonts can be used in custom styles.
        """
        return self.customFonts

    '''
    # Does not work well with custom themes
    def setFont(self, font):
        if font == "Default":
            return # TODO
        if font not in self.customFonts:
            log.warning("No font family with name %s loaded from data/fonts", font)
            return
        qfont = gui.QtGui.QFont(font)
        self.setFont(qfont)
        log.debug("Setting font %s", font)
    '''

    def getLookAndFeelStyles(self):
        return [ str(style) for style in gui.QtGui.QStyleFactory.keys() ]

    def setLookAndFeel(self, platform):
        style = gui.QtGui.QStyleFactory.create(platform)
        self.setStyle(style)

    def getLookAndFeel(self):
        return str(self.style().objectName())

    def getThemeResource(self, folder, id):
        if '/' in id:
            return id
        path = os.path.join("data/themes/", self.theme, folder, id)
        if os.path.exists(path):
            return path
        else:
            return os.path.join("data/themes/default/", folder, id)

    def setLanguage(self, language):
        log.debug("Setting language to %s", language)
        lang.language.setLanguage(language)
        self.settings['rtl'] = lang.language.rtl

    def getLanguageString(self, string):
        return lang.language.getLanguageString(string)

    def dumpMissingStrings(self):
        lang.language.dumpMissingStrings()

    # Caption
    def setCaption(self, caption):
        mh.setCaption(caption.encode('utf8'))

    def setFilenameCaption(self, filename):
        self.setCaption("MakeHuman r%s - [%s][*]" % (os.environ['SVNREVISION'], filename))

    def setFileModified(self, modified):
        self.modified = modified
        self.mainwin.setWindowModified(self.modified)

    # Global status bar
    def status(self, text, *args):
        if self.statusBar is None:
            return
        self.statusBar.showMessage(text, *args)

    def statusPersist(self, text, *args):
        if self.statusBar is None:
            return
        self.statusBar.setMessage(text, *args)

    # Global progress bar
    def progress(self, value, text=None):
        if text is not None:
            self.status(text)

        if self.progressBar is None:
            return

        if value >= 1.0:
            self.progressBar.reset()
        else:
            self.progressBar.setProgress(value)

        self.processEvents()

    # Global dialog
    def prompt(self, title, text, button1Label, button2Label=None, button1Action=None, button2Action=None, helpId=None):
        if self.dialog is None:
            self.dialog = gui.Dialog(self.mainwin)
            self.dialog.helpIds.update(self.helpIds)
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

    def setTargetCamera(self, names, view='front', distance=10):
        if not isinstance(names, (tuple, list)):
            names = (names,)
        human = self.selectedHuman
        groupNames = [group.name
                      for group in human.meshData.faceGroups
                      if any(name in group.name for name in names)]
        self.setCameraGroupsViewDistance(groupNames, view, distance)

    def setFaceCamera(self):
        self.setTargetCamera(("head", "jaw"))

    def setLeftHandFrontCamera(self):
        self.setTargetCamera("l-hand")

    def setLeftHandTopCamera(self):
        self.setTargetCamera("l-hand", 'top')

    def setRightHandFrontCamera(self):
        self.setTargetCamera("r-hand")

    def setRightHandTopCamera(self):
        self.setTargetCamera("r-hand", 'top')

    def setLeftFootFrontCamera(self):
        self.setTargetCamera("l-foot")

    def setLeftFootLeftCamera(self):
        self.setTargetCamera("l-foot", 'left')

    def setRightFootFrontCamera(self):
        self.setTargetCamera("r-foot")

    def setRightFootRightCamera(self):
        self.setTargetCamera("r-foot", 'right')

    def setLeftArmFrontCamera(self):
        self.setTargetCamera(("l-lowerarm", "l-upperarm"), distance=30)

    def setLeftArmTopCamera(self):
        self.setTargetCamera(("l-lowerarm", "l-upperarm"), top, distance=30)

    def setRightArmFrontCamera(self):
        self.setTargetCamera(("r-lowerarm", "r-upperarm"), distance=30)

    def setRightArmTopCamera(self):
        self.setTargetCamera(("r-lowerarm", "r-upperarm"), top, distance=30)

    def setLeftLegFrontCamera(self):
        self.setTargetCamera(("l-lowerleg", "l-upperleg"), distance=30)

    def setLeftLegLeftCamera(self):
        self.setTargetCamera(("l-lowerleg", "l-upperleg"), left, distance=30)

    def setRightLegFrontCamera(self):
        self.setTargetCamera(("r-lowerleg", "r-upperleg"), distance=30)

    def setRightLegRightCamera(self):
        self.setTargetCamera(("r-lowerleg", "r-upperleg"), right, distance=30)

    # Shortcuts
    def setShortcut(self, modifier, key, action):

        shortcut = (modifier, key)

        if shortcut in self.shortcuts.values():
            self.prompt('Warning', 'This combination is already in use.', 'OK', helpId='shortcutWarning')
            return False

        self.shortcuts[action.name] = shortcut
        mh.setShortcut(modifier, key, action)

        return True

    def getShortcut(self, action):
        return self.shortcuts.get(action.name)

    # Mouse actions
    def setMouseAction(self, modifier, key, method):

        mouseAction = (modifier, key)

        if mouseAction in self.mouseActions:
            self.prompt('Warning', 'This combination is already in use.', 'OK', helpId='mouseActionWarning')
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
        mh.changeCategory("Modelling")
        self.redraw()

    def goToSave(self):
        mh.changeTask("Files", "Save")
        self.redraw()

    def goToLoad(self):
        mh.changeTask("Files", "Load")
        self.redraw()

    def goToExport(self):
        mh.changeTask("Files", "Export")
        self.redraw()

    def goToRendering(self):
        mh.changeCategory("Rendering")
        self.redraw()

    def goToHelp(self):
        mh.changeCategory("Help")

    def setMono(self):
        self.setStereo(0)

    def setStereo1(self):
        self.setStereo(1)

    def setStereo2(self):
        self.setStereo(2)

    def setStereo(self, stereoMode):
        self.modelCamera.stereoMode = stereoMode

        # We need a black background for stereo
        if stereoMode:
            mh.setClearColor(0.0, 0.0, 0.0, 1.0)
        else:
            mh.setClearColor(self.clearColor[0], self.clearColor[1], self.clearColor[2], 1.0)

        self.redraw()

    def toggleStereo(self):
        stereoMode = self.modelCamera.stereoMode
        stereoMode += 1
        if stereoMode > 2:
            stereoMode = 0
        self.setStereo(stereoMode)
        self.updateStereoButtons()

    def updateStereoButtons(self):
        stereoMode = self.modelCamera.stereoMode
        self.actions.mono.setChecked(stereoMode == 0)
        self.actions.stereo1.setChecked(stereoMode == 1)
        self.actions.stereo2.setChecked(stereoMode == 2)

    def toggleSolid(self):
        self.selectedHuman.setSolid(not self.actions.wireframe.isChecked())
        self.redraw()

    def toggleSubdivision(self):
        self.selectedHuman.setSubdivided(self.actions.smooth.isChecked(), True, self.progress)
        self.redraw()

    def symmetryRight(self):
        human = self.selectedHuman
        human.applySymmetryRight()

    def symmetryLeft(self):
        human = self.selectedHuman
        human.applySymmetryLeft()

    def symmetry(self):
        human = self.selectedHuman
        human.symmetryModeEnabled = self.actions.symmetry.isChecked()

    def saveTarget(self):
        human = self.selectedHuman
        algos3d.saveTranslationTarget(human.meshData, "full_target.target")
        log.message("Full target exported")

    def quickExport(self):
        exportPath = mh.getPath('exports')
        if not os.path.exists(exportPath):
            os.makedirs(exportPath)
        import mh2obj
        mh2obj.exportObj(self.selectedHuman.meshData, exportPath + '/quick_export.obj')
        import mh2bvh
        mh2bvh.exportSkeleton(self.selectedHuman.meshData, exportPath + '/quick_export.bvh')
        import mh2mhx
        mh2mhx.exportMhx(self.selectedHuman.meshData, exportPath + '/quick_export.mhx')

    def grabScreen(self):
        grabPath = mh.getPath('grab')
        if not os.path.exists(grabPath):
            os.makedirs(grabPath)
        # TODO: use bbox to choose grab region
        mh.grabScreen(0, 0, G.windowWidth, G.windowHeight, os.path.join(grabPath, 'grab.png'))

    def resetHuman(self):
        human = self.selectedHuman
        human.resetMeshValues()
        human.applyAllTargets(self.progress)
        self.setFilenameCaption("Untitled")
        self.setFileModified(False)

    # Camera navigation
    def rotateCamera(self, axis, amount):
        human = self.selectedHuman
        rot = human.getRotation()
        rot[axis] += amount
        human.setRotation(rot)
        self.redraw()

    def panCamera(self, axis, amount):
        human = self.selectedHuman
        trans = human.getPosition()
        trans[axis] += amount
        human.setPosition(trans)
        self.redraw()

    def cameraSpeed(self):
        if mh.getKeyModifiers() & mh.Modifiers.SHIFT:
            return gui3d.app.settings.get('highspeed', 5)
        else:
            return gui3d.app.settings.get('lowspeed', 1)

    def zoomCamera(self, amount):
        self.modelCamera.eyeZ += amount * self.cameraSpeed()
        self.redraw()

    def rotateAction(self, axis):
        return animation3d.RotateAction(self.selectedHuman, self.selectedHuman.getRotation(), axis)

    def axisView(self, axis):
        animation3d.animate(self, 0.20, [self.rotateAction(axis)])

    def rotateDown(self):
        self.rotateCamera(0, 5.0)

    def rotateUp(self):
        self.rotateCamera(0, -5.0)

    def rotateLeft(self):
        self.rotateCamera(1, -5.0)

    def rotateRight(self):
        self.rotateCamera(1, 5.0)

    def panUp(self):
        self.panCamera(1, 0.05)

    def panDown(self):
        self.panCamera(1, -0.05)

    def panRight(self):
        self.panCamera(0, 0.05)

    def panLeft(self):
        self.panCamera(0, -0.05)

    def zoomOut(self):
        self.zoomCamera(0.65)

    def zoomIn(self):
        self.zoomCamera(-0.65)

    def frontView(self):
        self.axisView([0.0, 0.0, 0.0])

    def rightView(self):
        self.axisView([0.0, -90.0, 0.0])

    def topView(self):
        self.axisView([90.0, 0.0, 0.0])

    def backView(self):
        self.axisView([0.0, 180.0, 0.0])

    def leftView(self):
        self.axisView([0.0, 90.0, 0.0])

    def bottomView(self):
        self.axisView([-90.0, 0.0, 0.0])

    def resetView(self):
        cam = self.modelCamera
        animation3d.animate(self, 0.20, [
            self.rotateAction([0.0, 0.0, 0.0]),
            animation3d.CameraAction(cam, None, [cam.eyeX, cam.eyeY, 60.0, cam.focusX, cam.focusY, cam.focusZ, 0, 1, 0])])

    # Mouse actions
    def mouseTranslate(self, event):

        speed = self.cameraSpeed()

        human = self.selectedHuman
        trans = human.getPosition()
        trans = self.modelCamera.convertToScreen(trans[0], trans[1], trans[2])
        trans[0] += event.dx * speed
        trans[1] += event.dy * speed
        trans = self.modelCamera.convertToWorld3D(trans[0], trans[1], trans[2])
        human.setPosition(trans)

    def mouseRotate(self, event):

        speed = self.cameraSpeed()

        human = self.selectedHuman
        rot = human.getRotation()
        rot[0] += 0.5 * event.dy * speed
        rot[1] += 0.5 * event.dx * speed
        human.setRotation(rot)

    def mouseZoom(self, event):

        speed = self.cameraSpeed()

        if gui3d.app.settings.get('invertMouseWheel', False):
            speed *= -1

        if self.modelCamera.projection == 0:
            self.modelCamera.scale *= 0.995 ** (event.dy * speed)
        else:
            self.modelCamera.eyeZ -= 0.05 * event.dy * speed

    def promptAndExit(self):
        if self.modified:
            self.prompt('Exit', 'You have unsaved changes. Are you sure you want to exit the application?', 'Yes', 'No', self.stop)
        else:
            self.stop()

    def toggleProfiling(self):
        import profiler
        if self.actions.profiling.isChecked():
            profiler.start()
            log.debug('profiling started')
        else:
            profiler.stop()
            log.debug('profiling stopped')
            mh.changeTask('Develop', 'Profile')

    def createActions(self):
        self.actions = gui.Actions()

        def action(*args, **kwargs):
            action = gui.Action(*args, **kwargs)
            self.mainwin.addAction(action)
            if toolbar is not None:
                toolbar.addAction(action)
            return action

        toolbar = None

        self.actions.rendering = action('rendering', 'Rendering',     self.goToRendering)
        self.actions.modelling = action('modelling', 'Modelling',     self.goToModelling)
        self.actions.exit      = action('exit'     , 'Exit',          self.promptAndExit)
        self.actions.stereo    = action('stereo',    'Stereo',        self.toggleStereo)

        self.actions.rotateU   = action('rotateU',   'Rotate Up',     self.rotateUp)
        self.actions.rotateD   = action('rotateD',   'Rotate Down',   self.rotateDown)
        self.actions.rotateR   = action('rotateR',   'Rotate Right',  self.rotateRight)
        self.actions.rotateL   = action('rotateL',   'Rotate Left',   self.rotateLeft)
        self.actions.panU      = action('panU',      'Pan Up',        self.panUp)
        self.actions.panD      = action('panD',      'Pan Down',      self.panDown)
        self.actions.panR      = action('panR',      'Pan Right',     self.panRight)
        self.actions.panL      = action('panL',      'Pan Left',      self.panLeft)
        self.actions.zoomIn    = action('zoomIn',    'Zoom In',       self.zoomIn)
        self.actions.zoomOut   = action('zoomOut',   'Zoom Out',      self.zoomOut)

        self.actions.profiling = action('profiling', 'Profiling',     self.toggleProfiling, toggle=True)

        toolbar = self.main_toolbar = mh.addToolBar("Main")

        self.actions.undo      = action('undo',      'Undo',          self.undo)
        self.actions.redo      = action('redo',      'Redo',          self.redo)
        self.actions.reset     = action('reset',     'Reset',         self.resetHuman)
        self.actions.save      = action('save',      'Save',          self.goToSave)
        self.actions.load      = action('load',      'Load',          self.goToLoad)
        self.actions.export    = action('export',    'Export',        self.goToExport)
        self.actions.help      = action('help',      'Help',          self.goToHelp)
        self.actions.smooth    = action('smooth',    'Smooth',        self.toggleSubdivision, toggle=True)
        self.actions.savetgt   = action('savetgt',   'Save target',   self.saveTarget)
        self.actions.qexport   = action('qexport',   'Quick export',  self.quickExport)
        self.actions.grab      = action('grab',      'Grab screen',   self.grabScreen)

        toolbar = self.view_toolbar = mh.addToolBar("View")

        self.actions.mono      = action('mono',      'Mono',          self.setMono,    group='stereo')
        self.actions.stereo1   = action('stereo1',   'Stereo 1',      self.setStereo1, group='stereo')
        self.actions.stereo2   = action('stereo2',   'Stereo 2',      self.setStereo2, group='stereo')
        self.actions.wireframe = action('wireframe', 'Wireframe',     self.toggleSolid, toggle=True)

        toolbar = self.sym_toolbar = mh.addToolBar("Symmetry")

        self.actions.symmetryR = action('symm1', 'Symmmetry R>L',     self.symmetryRight)
        self.actions.symmetryL = action('symm2', 'Symmmetry L>R',     self.symmetryLeft)
        self.actions.symmetry  = action('symm',  'Symmmetry',         self.symmetry, toggle=True)

        toolbar = self.camera_toolbar = mh.addToolBar("Camera")

        self.actions.front     = action('front',     'Front view',    self.frontView)
        self.actions.back      = action('back',      'Back view',     self.backView)
        self.actions.left      = action('left',      'Left view',     self.leftView)
        self.actions.right     = action('right',     'Right view',    self.rightView)
        self.actions.top       = action('top',       'Top view',      self.topView)
        self.actions.bottom    = action('bottom',    'Bottom view',   self.bottomView)
        self.actions.globalCam = action('global',    'Global camera', self.setGlobalCamera)
        self.actions.faceCam   = action('face',      'Face camera',   self.setFaceCamera)
        self.actions.resetCam  = action('resetCam',  'Reset camera',  self.resetView)

    def createShortcuts(self):
        for action, (modifier, key) in self.shortcuts.iteritems():
            action = getattr(self.actions, action, None)
            if action is not None:
                mh.setShortcut(modifier, key, action)

    def OnInit(self):
        mh.Application.OnInit(self)

        self.setLanguage("english")

        self.loadSettings()

        # Necessary because otherwise setting back to default theme causes crash
        self.setTheme("default")
        log.debug("Using Qt system style %s", self.getLookAndFeel())

        self.createActions()
        self.updateStereoButtons()

        self.createShortcuts()

        self.splash = gui.SplashScreen(gui3d.app.getThemeResource('images', 'splash.png'))
        self.splash.show()

        self.tabs = self.mainwin.tabs

        @self.tabs.mhEvent
        def onTabSelected(tab):
            self.switchCategory(tab.name)

    def run(self):
        self.start()

    def addExporter(self, exporter):
        self.getCategory('Files').getTaskByName('Export').addExporter(exporter)
