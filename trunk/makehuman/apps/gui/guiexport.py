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

This module implements the 'Files > Export' tab 
"""

import os

import mh
import gui
import gui3d
import log

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
        self.eye = camera.eye
        self.focus = camera.focus
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
        camera.eye = self.eye
        camera.focus = self.focus
        human.setRotation(self.rotation)
