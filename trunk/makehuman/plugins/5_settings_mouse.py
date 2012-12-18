#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
    
class AppMouseActionEdit(gui3d.MouseActionEdit):
    def __init__(self, method):
        gui3d.MouseActionEdit.__init__(self, gui3d.app.getMouseAction(method))
        self.method = method

    def onChanged(self, shortcut):
        if not gui3d.app.setMouseAction(shortcut[0], shortcut[1], self.method):
            self.setShortcut(gui3d.app.getMouseAction(self.method))

MouseActionLabelStyle = gui3d.TextViewStyle._replace(width=48)

class MouseActionsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Mouse')
        
        self.mouseBox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Camera', gui3d.GroupBoxStyle._replace(height=25+25*3+24+6)))
        self.mouseBox.addView(gui3d.TextView("Move", style=MouseActionLabelStyle));self.mouseBox.addView(AppMouseActionEdit(gui3d.app.mouseTranslate))
        self.mouseBox.addView(gui3d.TextView("Rotate", style=MouseActionLabelStyle));self.mouseBox.addView(AppMouseActionEdit(gui3d.app.mouseRotate))
        self.mouseBox.addView(gui3d.TextView("Zoom", style=MouseActionLabelStyle));self.mouseBox.addView(AppMouseActionEdit(gui3d.app.mouseZoom))
        self.invertMouseWheel = self.mouseBox.addView(gui3d.CheckBox("Invert wheel", gui3d.app.settings.get('invertMouseWheel', False)))
        
        @self.invertMouseWheel.mhEvent
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.invertMouseWheel, event)
            gui3d.app.settings['invertMouseWheel'] = self.invertMouseWheel.selected

    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.mouseBox.children[1].setFocus()
        gui3d.app.prompt('Info', 'Click and drag on a mouse action box while holding down the modifiers and buttons which you would like to assign to the given action.',
            'OK', helpId='mouseActionHelp')
            
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        gui3d.app.saveSettings()
        
    def onResized(self, event):
        
        pass

def load(app):
    category = app.getCategory('Settings')
    taskview = category.addView(MouseActionsTaskView(category))

def unload(app):
    pass


