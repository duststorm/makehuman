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

import gui3d
import mh
import gui
import log
from core import G

class LevelRadioButton(gui.RadioButton):
    def __init__(self, group, level):
        name = log.getLevelName(level).capitalize()
        super(LevelRadioButton, self).__init__(group, name, not group)
        self.level = level

    def onClicked(self, _dummy = None):
        if self.selected:
            G.app.log_window.setLevel(self.level)

class LoggingTaskView(gui3d.TaskView):
    def __init__(self, category):
        super(LoggingTaskView, self).__init__(category, 'Logs')
        self.addTopWidget(G.app.log_window)
        self.groupBox = self.addLeftWidget(gui.GroupBox('Level'))
        group = []
        for level in [log.DEBUG, log.MESSAGE, log.NOTICE, log.WARNING, log.ERROR]:
            radio = self.groupBox.addWidget(LevelRadioButton(group, level))

def load(app):
    category = app.getCategory('Develop')
    taskview = category.addTask(LoggingTaskView(category))

def unload(app):
    pass

