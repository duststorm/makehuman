#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
    
class AppShortcutEdit(gui3d.ShortcutEdit):
    def __init__(self, parent, method):
        gui3d.ShortcutEdit.__init__(self, parent, gui3d.app.getShortcut(method))
        self.method = method

    def onChanged(self, shortcut):
        if not gui3d.app.setShortcut(shortcut[0], shortcut[1], self.method):
            self.setShortcut(gui3d.app.getShortcut(self.method))

ShortcutLabelStyle = gui3d.TextViewStyle._replace(width=48)

class ShortcutsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Shortcuts')
        
        self.cameraBox = gui3d.GroupBox(self, [10, 80, 9.0], 'Camera', gui3d.GroupBoxStyle._replace(height=25+25*17+6))
        gui3d.TextView(self.cameraBox, "Turn left", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.rotateLeft)
        gui3d.TextView(self.cameraBox, "Turn up", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.rotateUp)
        gui3d.TextView(self.cameraBox, "Turn down", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.rotateDown)
        gui3d.TextView(self.cameraBox, "Turn right", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.rotateRight)
        gui3d.TextView(self.cameraBox, "Pan up", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.panUp)
        gui3d.TextView(self.cameraBox, "Pan down", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.panDown)
        gui3d.TextView(self.cameraBox, "Pan right", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.panRight)
        gui3d.TextView(self.cameraBox, "Pan left", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.panLeft)
        gui3d.TextView(self.cameraBox, "Zoom in", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.zoomIn)
        gui3d.TextView(self.cameraBox, "Zoom out", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.zoomOut)
        gui3d.TextView(self.cameraBox, "Front view", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.frontView)
        gui3d.TextView(self.cameraBox, "Right view", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.rightView)
        gui3d.TextView(self.cameraBox, "Top view", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.topView)
        gui3d.TextView(self.cameraBox, "Back view", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.backView)
        gui3d.TextView(self.cameraBox, "Left view", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.leftView)
        gui3d.TextView(self.cameraBox, "Bottom view", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.bottomView)
        gui3d.TextView(self.cameraBox, "Reset view", style=ShortcutLabelStyle);AppShortcutEdit(self.cameraBox, gui3d.app.resetView)

        y = 80
        self.actionBox = gui3d.GroupBox(self, [650, y, 9.0], 'Actions', gui3d.GroupBoxStyle._replace(height=25+25*2+6));y+=25
        gui3d.TextView(self.actionBox, "Undo", style=ShortcutLabelStyle);AppShortcutEdit(self.actionBox, gui3d.app.undo);y+=25
        gui3d.TextView(self.actionBox, "Redo", style=ShortcutLabelStyle);AppShortcutEdit(self.actionBox, gui3d.app.redo);y+=25
        y+= 10
        
        self.navigationBox = gui3d.GroupBox(self, [650, y, 9.0], 'Navigation', gui3d.GroupBoxStyle._replace(height=25+25*7+6));y+=25
        gui3d.TextView(self.navigationBox, "Modelling", style=ShortcutLabelStyle);AppShortcutEdit(self.navigationBox, gui3d.app.goToModelling);y+=25
        gui3d.TextView(self.navigationBox, "Save", style=ShortcutLabelStyle);AppShortcutEdit(self.navigationBox, gui3d.app.goToSave);y+=25
        gui3d.TextView(self.navigationBox, "Load", style=ShortcutLabelStyle);AppShortcutEdit(self.navigationBox, gui3d.app.goToLoad);y+=25
        gui3d.TextView(self.navigationBox, "Export", style=ShortcutLabelStyle);AppShortcutEdit(self.navigationBox, gui3d.app.goToExport);y+=25
        gui3d.TextView(self.navigationBox, "Rendering", style=ShortcutLabelStyle);AppShortcutEdit(self.navigationBox, gui3d.app.goToRendering);y+=25
        gui3d.TextView(self.navigationBox, "Help", style=ShortcutLabelStyle);AppShortcutEdit(self.navigationBox, gui3d.app.goToHelp);y+=25
        gui3d.TextView(self.navigationBox, "Exit", style=ShortcutLabelStyle);AppShortcutEdit(self.navigationBox, gui3d.app.promptAndExit);y+=25
    
    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.cameraBox.children[1].setFocus()
        gui3d.app.prompt('Info', 'Click on a shortcut box and press the keys of the shortcut which you would like to assign to the given action.',
            'OK', helpId='shortcutHelp')
    
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        gui3d.app.saveSettings()
        
    def onResized(self, event):
        
        self.actionBox.setPosition([event.width - 150, self.actionBox.getPosition()[1], 9.0])
        self.navigationBox.setPosition([event.width - 150, self.navigationBox.getPosition()[1], 9.0])

def load(app):
    category = app.getCategory('Settings')
    taskview = ShortcutsTaskView(category)

def unload(app):
    pass


