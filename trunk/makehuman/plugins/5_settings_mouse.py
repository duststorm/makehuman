#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, events3d
    
class AppMouseActionEdit(gui3d.MouseActionEdit):
    def __init__(self, parent, position, method):
        gui3d.MouseActionEdit.__init__(self, parent, position, parent.app.getMouseAction(method))
        self.method = method

    def onChanged(self, shortcut):
        if not self.app.setMouseAction(shortcut[0], shortcut[1], self.method):
            self.setShortcut(self.app.getMouseAction(self.method))

class MouseActionsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Mouse')
        
        y = 80
        self.mouseBox = gui3d.GroupBox(self, [10, y, 9.0], 'Camera', gui3d.GroupBoxStyle._replace(height=25+25*3+24+6));y+=25
        gui3d.TextView(self.mouseBox, [18,y + 5, 9.2], "Move", 47, 2);AppMouseActionEdit(self.mouseBox, [68,y, 9.2], self.app.mouseTranslate);y+=25
        gui3d.TextView(self.mouseBox, [18,y + 5, 9.2], "Rotate", 47, 2);AppMouseActionEdit(self.mouseBox, [68,y, 9.2], self.app.mouseRotate);y+=25
        gui3d.TextView(self.mouseBox, [18,y + 5, 9.2], "Zoom", 47, 2);AppMouseActionEdit(self.mouseBox, [68,y, 9.2], self.app.mouseZoom);y+=25
        self.invertMouseWheel = gui3d.CheckBox(self, [18,y,9.2], "Invert wheel", self.app.settings.get('invertMouseWheel', False));y+=24
        
        @self.invertMouseWheel.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.invertMouseWheel, event)
            self.app.settings['invertMouseWheel'] = self.invertMouseWheel.selected

    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.app.prompt('Info', 'Click and drag on a mouse action box while holding down the modifiers and buttons which you would like to assign to the given action.',
            'OK', helpId='mouseActionHelp')
            
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        self.app.saveSettings()
        
    def onResized(self, event):
        
        pass

def load(app):
    category = app.getCategory('Settings')
    taskview = MouseActionsTaskView(category)

def unload(app):
    pass


