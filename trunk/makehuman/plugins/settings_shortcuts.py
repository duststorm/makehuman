#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, events3d
    
class AppShortcutEdit(gui3d.ShortcutEdit):
    def __init__(self, parent, position, method):
        gui3d.ShortcutEdit.__init__(self, parent, position, parent.app.getShortcut(method))
        self.method = method

    def onChanged(self, shortcut):
        self.app.setShortcut(shortcut[0], shortcut[1], self.method)

class ShortcutsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Shortcuts')

        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Actions', gui3d.GroupBoxStyle._replace(height=80));y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Undo");AppShortcutEdit(self, [68,y, 9.2], self.app.undo);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Redo");AppShortcutEdit(self, [68,y, 9.2], self.app.redo);y+=25
        y+= 10
        
        gui3d.GroupBox(self, [10, y, 9.0], 'Navigation', gui3d.GroupBoxStyle._replace(height=205));y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Modelling");AppShortcutEdit(self, [68,y, 9.2], self.app.goToModelling);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Save");AppShortcutEdit(self, [68,y, 9.2], self.app.goToSave);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Load");AppShortcutEdit(self, [68,y, 9.2], self.app.goToLoad);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Export");AppShortcutEdit(self, [68,y, 9.2], self.app.goToExport);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Rendering");AppShortcutEdit(self, [68,y, 9.2], self.app.goToRendering);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Help");AppShortcutEdit(self, [68,y, 9.2], self.app.stop);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Exit");AppShortcutEdit(self, [68,y, 9.2], self.app.goToHelp);y+=25

def load(app):
    category = app.getCategory('Settings')
    taskview = ShortcutsTaskView(category)
    print 'Shortcuts imported'

def unload(app):
    pass


