#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

This module implements the 'Files > Load' tab 
"""

import os

import mh
import gui3d
import filechooser as fc
import log

class HumanFileSort(fc.FileSort):
    
    def __init__(self):
        
        super(HumanFileSort, self).__init__()
        self.meta = {}
    
    def fields(self):
        
        return list(super(HumanFileSort, self).fields()) + ["gender", "age", "muscle", "weight"]
        
    def sortGender(self, filenames):
        
        self.updateMeta(filenames)
        decorated = [(self.meta[filename]['gender'], i, filename) for i, filename in enumerate(filenames)]
        decorated.sort()
        return [filename for gender, i, filename in decorated]
        
    def sortAge(self, filenames):
        
        self.updateMeta(filenames)
        decorated = [(self.meta[filename]['age'], i, filename) for i, filename in enumerate(filenames)]
        decorated.sort()
        return [filename for age, i, filename in decorated]

    def sortMuscle(self, filenames):
        
        self.updateMeta(filenames)
        decorated = [(self.meta[filename]['muscle'], i, filename) for i, filename in enumerate(filenames)]
        decorated.sort()
        return [filename for muscle, i, filename in decorated]
       
    def sortWeight(self, filenames):
        
        self.updateMeta(filenames)
        decorated = [(self.meta[filename]['weight'], i, filename) for i, filename in enumerate(filenames)]
        decorated.sort()
        return [filename for weight, i, filename in decorated]
        
    def updateMeta(self, filenames):
        
        for filename in filenames:
            
            if filename in self.meta:
                
                if self.meta[filename]['modified'] < os.path.getmtime(filename):
                
                    self.meta[filename] = self.getMeta(filename)
                
            else:
                
                self.meta[filename] = self.getMeta(filename)
                
    def getMeta(self, filename):
        
        meta = {}
                
        meta['modified'] = os.path.getmtime(filename)
        f = open(filename)
        for line in f:
            lineData = line.split()
            field = lineData[0]
            if field in ["gender", "age", "muscle", "weight"]:
                meta[field] = float(lineData[1])
        f.close()
        
        return meta

class LoadTaskView(gui3d.TaskView):

    def __init__(self, category):
        
        modelPath = mh.getPath('models')
        gui3d.TaskView.__init__(self, category, 'Load', )
        self.filechooser = self.addTopWidget(fc.FileChooser(modelPath, 'mhm', 'thumb', 'data/notfound.thumb', sort=HumanFileSort()))
        self.addLeftWidget(self.filechooser.sortBox)

        @self.filechooser.mhEvent
        def onFileSelected(filename):

            human = gui3d.app.selectedHuman

            human.load(filename, True, gui3d.app.progress)

            del gui3d.app.undoStack[:]
            del gui3d.app.redoStack[:]
            gui3d.app.modified = False

            name = os.path.basename(filename).replace('.mhm', '')

            self.parent.tasksByName['Save'].fileentry.text = name
            self.parent.tasksByName['Save'].fileentry.edit.setText(name)
            
            gui3d.app.setFilenameCaption(filename)
            gui3d.app.setFileModified(False)

            mh.changeCategory('Modelling')

    def onShow(self, event):

        # When the task gets shown, set the focus to the file chooser

        gui3d.app.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)
        self.filechooser.setFocus()

        # HACK: otherwise the toolbar background disappears for some weird reason

        gui3d.app.redraw()

    def onHide(self, event):
        
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)

class FilesCategory(gui3d.Category):

    def __init__(self):
        super(FilesCategory, self).__init__('Files')

        self.addTask(SaveTaskView(self))
        self.addTask(LoadTaskView(self))
        self.addTask(ExportTaskView(self))
