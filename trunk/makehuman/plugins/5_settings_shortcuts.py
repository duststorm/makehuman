#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, events3d
    
class AppShortcutEdit(gui3d.ShortcutEdit):
    def __init__(self, parent, position, method):
        gui3d.ShortcutEdit.__init__(self, parent, position, parent.app.getShortcut(method))
        self.method = method

    def onChanged(self, shortcut):
        if not self.app.setShortcut(shortcut[0], shortcut[1], self.method):
            self.setShortcut(self.app.getShortcut(self.method))

class ShortcutsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Shortcuts')

        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Actions', gui3d.GroupBoxStyle._replace(height=80));y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Undo", 47, 2);AppShortcutEdit(self, [68,y, 9.2], self.app.undo);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Redo", 47, 2);AppShortcutEdit(self, [68,y, 9.2], self.app.redo);y+=25
        y+= 10
        
        gui3d.GroupBox(self, [10, y, 9.0], 'Navigation', gui3d.GroupBoxStyle._replace(height=205));y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Modelling", 47, 2);AppShortcutEdit(self, [68,y, 9.2], self.app.goToModelling);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Save", 47, 2);AppShortcutEdit(self, [68,y, 9.2], self.app.goToSave);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Load", 47, 2);AppShortcutEdit(self, [68,y, 9.2], self.app.goToLoad);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Export", 47, 2);AppShortcutEdit(self, [68,y, 9.2], self.app.goToExport);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Rendering", 47, 2);AppShortcutEdit(self, [68,y, 9.2], self.app.goToRendering);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Help", 47, 2);AppShortcutEdit(self, [68,y, 9.2], self.app.goToHelp);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Exit", 47, 2);AppShortcutEdit(self, [68,y, 9.2], self.app.promptAndExit);y+=25
        
        y = 80
        self.cameraBox = gui3d.GroupBox(self, [650, y, 9.0], 'Camera', gui3d.GroupBoxStyle._replace(height=380));y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Turn left", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.rotateLeft);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Turn up", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.rotateUp);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Turn down", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.rotateDown);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Turn right", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.rotateRight);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Pan up", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.panUp);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Pan down", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.panDown);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Pan right", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.panRight);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Pan left", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.panLeft);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Zoom in", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.zoomIn);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Zoom out", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.zoomOut);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Front view", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.frontView);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Top view", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.topView);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Side view", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.sideView);y+=25
        gui3d.TextView(self.cameraBox, [658,y + 5, 9.2], "Reset view", 47, 2);AppShortcutEdit(self.cameraBox, [708,y, 9.2], self.app.resetView);y+=25
    
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        self.app.saveSettings()
        
    def onResized(self, event):
        
        self.cameraBox.setPosition([event.width - 150, self.cameraBox.getPosition()[1], 9.0])

def load(app):
    category = app.getCategory('Settings')
    taskview = ShortcutsTaskView(category)
    print 'Shortcuts imported'

def unload(app):
    pass


