#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import mh
import qtgui as gui
    
class AppShortcutEdit(gui.ShortcutEdit):
    def __init__(self, method):
        super(AppShortcutEdit, self).__init__(gui3d.app.getShortcut(method))
        self.method = method

    def onChanged(self, shortcut):
        modifiers, key = shortcut
        if not gui3d.app.setShortcut(modifiers, key, self.method):
            self.setShortcut(gui3d.app.getShortcut(self.method))

class ShortcutsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Shortcuts')

        row = [0]
        def add(widget, name, method):
            widget.addWidget(gui.TextView(name), row[0], 0)
            widget.addWidget(AppShortcutEdit(method), row[0], 1)
            row[0] += 1

        self.cameraBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Camera')))
        add(self.cameraBox, "Turn left",    gui3d.app.rotateLeft)
        add(self.cameraBox, "Turn up",      gui3d.app.rotateUp)
        add(self.cameraBox, "Turn down",    gui3d.app.rotateDown)
        add(self.cameraBox, "Turn right",   gui3d.app.rotateRight)
        add(self.cameraBox, "Pan up",       gui3d.app.panUp)
        add(self.cameraBox, "Pan down",     gui3d.app.panDown)
        add(self.cameraBox, "Pan right",    gui3d.app.panRight)
        add(self.cameraBox, "Pan left",     gui3d.app.panLeft)
        add(self.cameraBox, "Zoom in",      gui3d.app.zoomIn)
        add(self.cameraBox, "Zoom out",     gui3d.app.zoomOut)
        add(self.cameraBox, "Front view",   gui3d.app.frontView)
        add(self.cameraBox, "Right view",   gui3d.app.rightView)
        add(self.cameraBox, "Top view",     gui3d.app.topView)
        add(self.cameraBox, "Back view",    gui3d.app.backView)
        add(self.cameraBox, "Left view",    gui3d.app.leftView)
        add(self.cameraBox, "Bottom view",  gui3d.app.bottomView)
        add(self.cameraBox, "Reset view",   gui3d.app.resetView)

        self.actionBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Actions')))
        add(self.actionBox, "Undo",         gui3d.app.undo)
        add(self.actionBox, "Redo",         gui3d.app.redo)

        self.navigationBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Navigation')))
        add(self.navigationBox, "Modelling", gui3d.app.goToModelling)
        add(self.navigationBox, "Save",      gui3d.app.goToSave)
        add(self.navigationBox, "Load",      gui3d.app.goToLoad)
        add(self.navigationBox, "Export",    gui3d.app.goToExport)
        add(self.navigationBox, "Rendering", gui3d.app.goToRendering)
        add(self.navigationBox, "Help",      gui3d.app.goToHelp)
        add(self.navigationBox, "Exit",      gui3d.app.promptAndExit)
    
    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.cameraBox.children[1].setFocus()
        gui3d.app.prompt('Info', 'Click on a shortcut box and press the keys of the shortcut which you would like to assign to the given action.',
            'OK', helpId='shortcutHelp')
    
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        gui3d.app.saveSettings()

def load(app):
    category = app.getCategory('Settings')
    taskview = category.addView(ShortcutsTaskView(category))

def unload(app):
    pass


