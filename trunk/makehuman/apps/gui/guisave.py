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

This module implements the 'Files > Save' tab 
"""

import os

import mh
import gui
import gui3d
import log

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
        
