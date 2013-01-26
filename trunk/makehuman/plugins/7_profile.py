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
import profiler
import pstats
from core import G

taskview = None

class KeyRadioButton(gui.RadioButton):
    def __init__(self, group, name, key):
        super(KeyRadioButton, self).__init__(group, name, not group)
        self.key = key

    def onClicked(self, _dummy = None):
        if self.selected:
            taskview.setSortKey(self.key)

class DirRadioButton(gui.RadioButton):
    def __init__(self, group, name, dir):
        super(DirRadioButton, self).__init__(group, name, not group)
        self.dir = dir

    def onClicked(self, _dummy = None):
        if self.selected:
            taskview.setSortDir(self.dir)

class Stat(object):
    _fields = [
        ('Primitive calls', 'prim'),
        ('Total calls', 'calls'),
        ('Total time', 'total'),
        ('Total per call', 'totalpc'),
        ('Cumulative time', 'cumul'),
        ('Cumulative per call', 'cumulpc'),
        ('Function', 'function'),
        ]

    def __init__(self, func, data):
        (self._module, self._line, self._func) = func
        (self._prim, self._calls, self._total, self._cumul, self._callers) = data

    @property
    def _totalpc(self):
        return self._total / self._calls

    @property
    def _cumulpc(self):
        return self._cumul / self._prim

    @property
    def _function(self):
        return (self._module, self._line, self._func)

    @property
    def calls(self):
        if self._prim != self._calls:
            return "%d/%d" % (self._calls, self._prim)
        else:
            return "%d" % self._calls

    @property
    def total(self):
        return "%.3f" % self._total

    @property
    def total_pc(self):
        return "%.3f" % self._totalpc

    @property
    def cumul(self):
        return "%.3f" % self._cumul

    @property
    def cumul_pc(self):
        return "%.3f" % (self._cumul / self._prim)

    @property
    def func(self):
        return pstats.func_std_string(self._function)

    @property
    def data(self):
        return (self.calls, self.total, self.total_pc, self.cumul, self.cumul_pc, self.func)

    @staticmethod
    def key(key):
        name = '_' + key
        return lambda s: getattr(s, name)

class ProfilingTaskView(gui3d.TaskView):
    _columns = [
        'Calls',
        'Total',
        'Total/Call',
        'Cumul.',
        'Cumul/Call',
        'Function'
        ]

    def __init__(self, category):
        super(ProfilingTaskView, self).__init__(category, 'Profile')

        self.sortKey = 'prim'
        self.sortDir = 0

        self.table = self.addTopWidget(gui.TableView())

        self.sortKeyBox = self.addLeftWidget(gui.GroupBox('Sort'))
        group = []
        for name, key in Stat._fields:
            radio = self.sortKeyBox.addWidget(KeyRadioButton(group, name, key))

        self.sortDirBox = self.addLeftWidget(gui.GroupBox('Sort'))
        group = []
        for name, dir in [('Descending', 0), ('Ascending', 1)]:
            radio = self.sortDirBox.addWidget(DirRadioButton(group, name, dir))

        self.table.setColumnCount(len(self._columns))
        self.table.setHorizontalHeaderLabels(self._columns)
        self.table.setColumnWidth(len(self._columns) - 1, 300)

    def setData(self, stats):
        self.data = [Stat(func, data) for func, data in stats.stats.iteritems()]
        self.update()

    def setSortKey(self, key):
        self.sortKey = key
        self.update()

    def setSortDir(self, dir):
        self.sortDir = dir
        self.update()

    def sort(self):
        self.data.sort(key = Stat.key(self.sortKey), reverse = self.sortDir == 0)

    def update(self):
        self.sort()
        self.table.setRowCount(len(self.data))
        for row, stat in enumerate(self.data):
            for col, value in enumerate(stat.data):
                self.table.setItem(row, col, value)

    def setProfile(self, profile):
        stats = pstats.Stats(profile).strip_dirs()
        self.setData(stats)

def load(app):
    global taskview
    category = app.getCategory('Develop')
    taskview = category.addTask(ProfilingTaskView(category))
    profiler.set_show(taskview.setProfile)

def unload(app):
    pass

