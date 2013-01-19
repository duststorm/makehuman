#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import mh
import gui
from core import G

class LoggingTaskView(gui3d.TaskView):
    def __init__(self, category):
        super(LoggingTaskView, self).__init__(category, 'Logs')
        self.addTopWidget(G.app.log_window)

def load(app):
    category = app.getCategory('Develop')
    taskview = category.addTask(LoggingTaskView(category))

def unload(app):
    pass

