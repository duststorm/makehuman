#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np

import gui3d
import mh
import gui
import algos3d
from core import G
import log

class TargetsTree(gui.TreeView):
    def __init__(self):
        super(TargetsTree, self).__init__()
        self.root = self.addTopLevel('targets')
        self.populate(self.root, os.path.join('data', 'targets'))

    def populate(self, root, path):
        for name in os.listdir(path):
            pathname = os.path.join(path, name)
            if os.path.isdir(pathname):
                item = root.addChild(name, True)
                self.populate(item, pathname)
            elif name.lower().endswith('.target') and os.path.isfile(pathname):
                root.addChild(name)

class TargetsTaskView(gui3d.TaskView):
    def __init__(self, category):
        super(TargetsTaskView, self).__init__(category, 'Targets')
        self.targets = self.addTopWidget(TargetsTree())
        self.clear = self.addLeftWidget(gui.Button('Clear'))

        @self.targets.mhEvent
        def onActivate(item):
            path = []
            while item is not None:
                path.append(item.text)
                item = item.parent
            path = os.path.join('data', *reversed(path))
            log.message('target: %s', path)
            self.showTarget(path)
            mh.changeCategory('Modelling')

        @self.clear.mhEvent
        def onClicked(event):
            self.clearColor()
            mh.changeCategory('Modelling')

    def clearColor(self):
        mesh = G.app.selectedHuman.meshData
        mesh.color[...] = (255,255,255,255)
        mesh.markCoords(colr = True)
        mesh.sync_all()

    def showTarget(self, path):
        mesh = G.app.selectedHuman.meshData
        target = algos3d.getTarget(mesh, path)
        sizes = np.sqrt(np.sum(target.data ** 2, axis = -1))
        sizes /= np.amax(sizes)
        val = sizes * 2 - 1
        del sizes
        red = np.maximum(val, 0)
        blue = np.maximum(-val, 0)
        green = 1.0 - red - blue
        del val
        color = np.array([red,green,blue,np.ones_like(red)]).T
        color = (color * 255.99).astype(np.uint8)
        mesh.color[target.verts,:] = color
        mesh.markCoords(target.verts, colr = True)
        mesh.sync_all()

def load(app):
    category = app.getCategory('Targets')
    taskview = category.addTask(TargetsTaskView(category))

def unload(app):
    pass

