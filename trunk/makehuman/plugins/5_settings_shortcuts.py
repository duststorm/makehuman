#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
    
class AppShortcutEdit(gui3d.ShortcutEdit):
    def __init__(self, method):
        gui3d.ShortcutEdit.__init__(self, gui3d.app.getShortcut(method))
        self.method = method

    def onChanged(self, shortcut):
        if not gui3d.app.setShortcut(shortcut[0], shortcut[1], self.method):
            self.setShortcut(gui3d.app.getShortcut(self.method))

ShortcutLabelStyle = gui3d.TextViewStyle._replace(width=48)

class ShortcutsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Shortcuts')
        
        self.cameraBox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Camera', gui3d.GroupBoxStyle._replace(height=25+25*17+6)))
        self.cameraBox.addView(gui3d.TextView("Turn left", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.rotateLeft))
        self.cameraBox.addView(gui3d.TextView("Turn up", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.rotateUp))
        self.cameraBox.addView(gui3d.TextView("Turn down", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.rotateDown))
        self.cameraBox.addView(gui3d.TextView("Turn right", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.rotateRight))
        self.cameraBox.addView(gui3d.TextView("Pan up", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.panUp))
        self.cameraBox.addView(gui3d.TextView("Pan down", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.panDown))
        self.cameraBox.addView(gui3d.TextView("Pan right", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.panRight))
        self.cameraBox.addView(gui3d.TextView("Pan left", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.panLeft))
        self.cameraBox.addView(gui3d.TextView("Zoom in", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.zoomIn))
        self.cameraBox.addView(gui3d.TextView("Zoom out", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.zoomOut))
        self.cameraBox.addView(gui3d.TextView("Front view", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.frontView))
        self.cameraBox.addView(gui3d.TextView("Right view", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.rightView))
        self.cameraBox.addView(gui3d.TextView("Top view", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.topView))
        self.cameraBox.addView(gui3d.TextView("Back view", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.backView))
        self.cameraBox.addView(gui3d.TextView("Left view", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.leftView))
        self.cameraBox.addView(gui3d.TextView("Bottom view", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.bottomView))
        self.cameraBox.addView(gui3d.TextView("Reset view", style=ShortcutLabelStyle));self.cameraBox.addView(AppShortcutEdit(gui3d.app.resetView))

        y = 80
        self.actionBox = self.addView(gui3d.GroupBox([650, y, 9.0], 'Actions', gui3d.GroupBoxStyle._replace(height=25+25*2+6)));y+=25
        self.actionBox.addView(gui3d.TextView("Undo", style=ShortcutLabelStyle));self.actionBox.addView(AppShortcutEdit(gui3d.app.undo));y+=25
        self.actionBox.addView(gui3d.TextView("Redo", style=ShortcutLabelStyle));self.actionBox.addView(AppShortcutEdit(gui3d.app.redo));y+=25
        y+= 10
        
        self.navigationBox = self.addView(gui3d.GroupBox([650, y, 9.0], 'Navigation', gui3d.GroupBoxStyle._replace(height=25+25*7+6)));y+=25
        self.navigationBox.addView(gui3d.TextView("Modelling", style=ShortcutLabelStyle));self.navigationBox.addView(AppShortcutEdit(gui3d.app.goToModelling));y+=25
        self.navigationBox.addView(gui3d.TextView("Save", style=ShortcutLabelStyle));self.navigationBox.addView(AppShortcutEdit(gui3d.app.goToSave));y+=25
        self.navigationBox.addView(gui3d.TextView("Load", style=ShortcutLabelStyle));self.navigationBox.addView(AppShortcutEdit(gui3d.app.goToLoad));y+=25
        self.navigationBox.addView(gui3d.TextView("Export", style=ShortcutLabelStyle));self.navigationBox.addView(AppShortcutEdit(gui3d.app.goToExport));y+=25
        self.navigationBox.addView(gui3d.TextView("Rendering", style=ShortcutLabelStyle));self.navigationBox.addView(AppShortcutEdit(gui3d.app.goToRendering));y+=25
        self.navigationBox.addView(gui3d.TextView("Help", style=ShortcutLabelStyle));self.navigationBox.addView(AppShortcutEdit(gui3d.app.goToHelp));y+=25
        self.navigationBox.addView(gui3d.TextView("Exit", style=ShortcutLabelStyle));self.navigationBox.addView(AppShortcutEdit(gui3d.app.promptAndExit));y+=25
    
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
    taskview = category.addView(ShortcutsTaskView(category))

def unload(app):
    pass


