#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import mh
import qtgui as gui
    
class AppMouseActionEdit(gui.MouseActionEdit):
    def __init__(self, method):
        super(AppMouseActionEdit, self).__init__(gui3d.app.getMouseAction(method))
        self.method = method

    def onChanged(self, shortcut):
        modifiers, button = shortcut
        if not gui3d.app.setMouseAction(modifiers, button, self.method):
            self.setShortcut(gui3d.app.getMouseAction(self.method))

class MouseActionsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Mouse')

        row = [0]
        def add(widget, name, method):
            widget.addWidget(gui.TextView(name), row[0], 0)
            widget.addWidget(AppMouseActionEdit(method), row[0], 1)
            row[0] += 1
        
        self.mouseBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Camera')))

        add(self.mouseBox, "Move",   gui3d.app.mouseTranslate)
        add(self.mouseBox, "Rotate", gui3d.app.mouseRotate)
        add(self.mouseBox, "Zoom",   gui3d.app.mouseZoom)

        self.invertMouseWheel = self.mouseBox.addWidget(gui.CheckBox("Invert wheel", gui3d.app.settings.get('invertMouseWheel', False)))
        
        @self.invertMouseWheel.mhEvent
        def onClicked(event):
            gui3d.app.settings['invertMouseWheel'] = self.invertMouseWheel.selected

    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.mouseBox.children[1].setFocus()
        gui3d.app.prompt('Info', 'Click and drag on a mouse action box while holding down the modifiers and buttons which you would like to assign to the given action.',
            'OK', helpId='mouseActionHelp')
            
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        gui3d.app.saveSettings()

def load(app):
    category = app.getCategory('Settings')
    taskview = category.addTask(MouseActionsTaskView(category))

def unload(app):
    pass


