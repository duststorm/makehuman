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

This module implements the 'guifiles' class structures and methods to support GUI 
File mode operations.
File mode is invoked by selecting the File mode icon from the main GUI control bar at the top of
the screen. While in this mode, user actions (keyboard and mouse events) are passed into 
this class for processing. Having processed an event this class returns control to the 
main OpenGL/Application event handling loop.
"""

import mh
import gui3d
import os
from os.path import basename
import gui
import filechooser as fc
import log
import numpy as np

class SaveTaskView(gui3d.TaskView):

    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Save')

        modelPath = mh.getPath('models')

        self.fileentry = self.addTopWidget(gui.FileEntryView('Save'))
        self.fileentry.setDirectory(modelPath)
        self.fileentry.setFilter('MakeHuman Models (*.mhm)')

        self.selection_width = 1.2
        self.selection_height = 1.3
        mesh = gui3d.FrameMesh(self.selection_width, self.selection_height)
        mesh.move(-self.selection_width/2, -self.selection_height/2)

        self.selection = gui3d.app.addObject(gui3d.Object([0, 0, 9], mesh))
        mesh.setColor([0, 0, 0, 255])
        mesh.setPickable(False)
        mesh.setShadeless(True)
        mesh.setDepthless(True)
        mesh.priority = 90
        self.selection.hide()

        @self.fileentry.mhEvent
        def onFileSelected(filename):
            if not filename.lower().endswith('.mhm'):
                filename += '.mhm'

            path = os.path.normpath(os.path.join(modelPath, filename))

            dir, name = os.path.split(path)
            name, ext = os.path.splitext(name)

            if not os.path.exists(dir):
                os.makedirs(dir)

            # Save the thumbnail

            ((x0,y0,z0),(x1,y1,z1)) = self.selection.mesh.calcBBox()
            x0,y0,z0 = gui3d.app.guiCamera.convertToScreen(x0, y0, 0)
            x1,y1,z1 = gui3d.app.guiCamera.convertToScreen(x1, y1, 0)
            log.debug('grab rectangle: %d %d %d %d', x0, y0, x1, y1)
            mh.grabScreen(int(x0+1), int(y1+1), int(x1-x0-1), int(y0-y1-1), os.path.join(dir, name + '.thumb'))

            # Save the model

            human = gui3d.app.selectedHuman
            human.save(path, name)
            gui3d.app.modified = False
            
            gui3d.app.setFilenameCaption(filename)
            gui3d.app.setFileModified(False)

            mh.changeCategory('Modelling')

    def onShow(self, event):

        # When the task gets shown, set the focus to the file entry

        gui3d.TaskView.onShow(self, event)
        self.fileentry.setFocus()
        self.pan = gui3d.app.selectedHuman.getPosition()
        self.eyeX = gui3d.app.modelCamera.eyeX
        self.eyeY = gui3d.app.modelCamera.eyeY
        self.eyeZ = gui3d.app.modelCamera.eyeZ
        self.focusX = gui3d.app.modelCamera.focusX
        self.focusY = gui3d.app.modelCamera.focusY
        self.focusZ = gui3d.app.modelCamera.focusZ
        self.rotation = gui3d.app.selectedHuman.getRotation()
        gui3d.app.selectedHuman.setPosition([0, -1, 0])
        gui3d.app.setGlobalCamera();
        gui3d.app.modelCamera.eyeZ = 70
        gui3d.app.selectedHuman.setRotation([0.0, 0.0, 0.0])
        self.selection.show()

    def onHide(self, event):
        
        gui3d.TaskView.onHide(self, event)
        gui3d.app.selectedHuman.setPosition(self.pan)
        gui3d.app.modelCamera.eyeX = self.eyeX
        gui3d.app.modelCamera.eyeY = self.eyeY
        gui3d.app.modelCamera.eyeZ = self.eyeZ
        gui3d.app.modelCamera.focusX = self.focusX
        gui3d.app.modelCamera.focusY = self.focusY
        gui3d.app.modelCamera.focusZ = self.focusZ
        gui3d.app.selectedHuman.setRotation(self.rotation)
        self.selection.hide()
        
    def onResized(self, event):
        pass
        
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

class ExportTaskView(gui3d.TaskView):
    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Export')

        self.formats = []

        exportPath = mh.getPath('exports')

        self.fileentry = self.addTopWidget(gui.FileEntryView('Export'))
        self.fileentry.setDirectory(exportPath)
        self.fileentry.setFilter('All Files (*.*)')

        self.exportBodyGroup = []
        self.exportHairGroup = []
        
        # Mesh Formats
        self.formatBox = self.addLeftWidget(gui.GroupBox('Mesh Format'))

        # Rig formats
        self.rigBox = self.addLeftWidget(gui.GroupBox('Rig format'))

        # Map formats
        self.mapsBox = self.addLeftWidget(gui.GroupBox('Maps'))

        self.boxes = {
            'mesh': self.formatBox,
            'rig': self.rigBox,
            'map': self.mapsBox
            }

        self.empty = True

        self.optionsBox = self.addRightWidget(gui.StackedBox())

        self.updateGui()
        
        @self.fileentry.mhEvent
        def onFileSelected(filename):
            import mh2obj, mh2bvh, mh2mhx, mh2obj_proxy, mh2collada, mh2md5, mh2stl, mh2skel, mh2fbx

            path = os.path.normpath(os.path.join(exportPath, filename))
            dir, name = os.path.split(path)
            name, ext = os.path.splitext(name)

            if not os.path.exists(dir):
                os.makedirs(dir)

            def filename(targetExt, different = False):
                if not different and ext != '' and ('.' + targetExt.lower()) != ext.lower():
                    log.warning("expected extension '.%s' but got '%s'", targetExt, ext)
                return os.path.join(dir, name + '.' + targetExt)

            found = False
            for exporter, radio, options in self.formats:
                if radio.selected:
                    exporter.export(gui3d.app.selectedHuman, filename)
                    found = True
                    break

            if not found:
                log.error("Unknown export format selected!")
                return

            gui3d.app.prompt('Info', u'The mesh has been exported to %s.' % dir, 'OK', helpId='exportHelp')

            mh.changeCategory('Modelling')
            
    def addExporter(self, exporter):
        radio = self.boxes[exporter.group].addWidget(gui.RadioButton(self.exportBodyGroup, exporter.name, self.empty))
        options = self.optionsBox.addWidget(gui.GroupBox('Options'))
        exporter.build(options)
        self.empty = False
        self.formats.append((exporter, radio, options))

        @radio.mhEvent
        def onClicked(event):
            self.updateGui()
            self.fileentry.setFilter(exporter.filter)
    
    def updateGui(self):
        for exporter, radio, options in self.formats:
            if radio.selected:
                self.optionsBox.showWidget(options)
                break

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        
        self.fileentry.setFocus()

        human = gui3d.app.selectedHuman
        camera = mh.cameras[0]
        
        self.pan = human.getPosition()
        self.eyeX = camera.eyeX
        self.eyeY = camera.eyeY
        self.eyeZ = camera.eyeZ
        self.focusX = camera.focusX
        self.focusY = camera.focusY
        self.focusZ = camera.focusZ
        self.rotation = human.getRotation()
        human.setPosition([0, -1, 0])
        gui3d.app.setGlobalCamera();
        camera.eyeZ = 70
        human.setRotation([0.0, 0.0, 0.0])

    def onHide(self, event):
        
        gui3d.TaskView.onHide(self, event)
        
        human = gui3d.app.selectedHuman
        camera = mh.cameras[0]
        
        human.setPosition(self.pan)
        camera.eyeX = self.eyeX
        camera.eyeY = self.eyeY
        camera.eyeZ = self.eyeZ
        camera.focusX = self.focusX
        camera.focusY = self.focusY
        camera.focusZ = self.focusZ
        human.setRotation(self.rotation)
        
class FilesCategory(gui3d.Category):

    def __init__(self):
        super(FilesCategory, self).__init__('Files')

        self.addTask(SaveTaskView(self))
        self.addTask(LoadTaskView(self))
        self.addTask(ExportTaskView(self))
