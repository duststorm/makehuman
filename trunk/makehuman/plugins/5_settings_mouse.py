#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, events3d
    
class AppMouseActionEdit(gui3d.MouseActionEdit):
    def __init__(self, parent, method):
        gui3d.MouseActionEdit.__init__(self, parent, parent.app.getMouseAction(method))
        self.method = method

    def onChanged(self, shortcut):
        if not self.app.setMouseAction(shortcut[0], shortcut[1], self.method):
            self.setShortcut(self.app.getMouseAction(self.method))

MouseActionLabelStyle = gui3d.TextViewStyle._replace(width=48)

class MouseActionsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Mouse')
        
        self.mouseBox = gui3d.GroupBox(self, [10, 80, 9.0], 'Camera', gui3d.GroupBoxStyle._replace(height=25+25*3+24+6))
        gui3d.TextView(self.mouseBox, "Move", style=MouseActionLabelStyle);AppMouseActionEdit(self.mouseBox, self.app.mouseTranslate)
        gui3d.TextView(self.mouseBox, "Rotate", style=MouseActionLabelStyle);AppMouseActionEdit(self.mouseBox, self.app.mouseRotate)
        gui3d.TextView(self.mouseBox, "Zoom", style=MouseActionLabelStyle);AppMouseActionEdit(self.mouseBox, self.app.mouseZoom)
        self.invertMouseWheel = gui3d.CheckBox(self.mouseBox, "Invert wheel", self.app.settings.get('invertMouseWheel', False))
        
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


