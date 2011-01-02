#!/usr/bin/python
# -*- coding: utf-8 -*-
# You may use, modify and redistribute this module under the terms of the GNU GPL.

""" 
Class for handling File mode in the GUI.

B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2010

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

This module implements the 'guifiles' class structures and methods to support GUI 
File mode operations.
File mode is invoked by selecting the File mode icon from the main GUI control bar at the top of
the screen. While in this mode, user actions (keyboard and mouse events) are passed into 
this class for processing. Having processed an event this class returns control to the 
main OpenGL/SDL/Application event handling loop.  

"""

import mh
import files3d
import animation3d
import gui3d
import events3d
import os
import mh2obj
import mh2bvh
import mh2mhx
import mh2proxy
import mh2collada
import mh2md5
import mh2stl
import hair

class SaveTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Save', category.app.getThemeResource('images', 'button_save_file.png'), category.app.getThemeResource('images', 'button_save_file_on.png'))
        self.fileentry = gui3d.FileEntryView(self)

        @self.fileentry.event
        def onFileSelected(filename):
            modelPath = mh.getPath('models')
            if not os.path.exists(modelPath):
                os.makedirs(modelPath)

            tags = filename
            filename = filename.split()[0]

      # Save the thumbnail

            leftTop = mh.cameras[0].convertToScreen(-10, 9, 0)
            rightBottom = mh.cameras[0].convertToScreen(10, -10, 0)
            self.app.scene3d.grabScreen(int(leftTop[0]), int(leftTop[1]), int(rightBottom[0] - leftTop[0]), int(rightBottom[1] - leftTop[1]), os.path.join(modelPath, filename + '.bmp'))

      # Save the model

            human = self.app.scene3d.selectedHuman
            human.save(os.path.join(modelPath, filename + '.mhm'), tags)

            self.app.switchCategory('Modelling')
            self.app.scene3d.redraw(1)

    def onShow(self, event):

    # When the task gets shown, set the focus to the file entry

        gui3d.TaskView.onShow(self, event)
        self.fileentry.setFocus()
        self.pan = self.app.scene3d.selectedHuman.getPosition()
        self.eyeX = mh.cameras[0].eyeX
        self.eyeY = mh.cameras[0].eyeY
        self.eyeZ = mh.cameras[0].eyeZ
        self.focusX = mh.cameras[0].focusX
        self.focusY = mh.cameras[0].focusY
        self.focusZ = mh.cameras[0].focusZ
        self.rotation = self.app.scene3d.selectedHuman.getRotation()
        self.app.scene3d.selectedHuman.setPosition([0, -1, 0])
        self.app.setGlobalCamera();
        mh.cameras[0].eyeZ = 70
        self.app.scene3d.selectedHuman.setRotation([0.0, 0.0, 0.0])

    def onHide(self, event):
        gui3d.TaskView.onHide(self, event)
        self.app.scene3d.selectedHuman.setPosition(self.pan)
        mh.cameras[0].eyeX = self.eyeX
        mh.cameras[0].eyeY = self.eyeY
        mh.cameras[0].eyeZ = self.eyeZ
        mh.cameras[0].focusX = self.focusX
        mh.cameras[0].focusY = self.focusY
        mh.cameras[0].focusZ = self.focusZ
        self.app.scene3d.selectedHuman.setRotation(self.rotation)


class LoadTaskView(gui3d.TaskView):

    def __init__(self, category):
        modelPath = mh.getPath('models')
        gui3d.TaskView.__init__(self, category, 'Load', category.app.getThemeResource('images', 'button_load_file.png'), category.app.getThemeResource('images', 'button_load_file_on.png'))
        self.filechooser = gui3d.FileChooser(self, modelPath, 'mhm')

        @self.filechooser.event
        def onFileSelected(filename):

            human = self.app.scene3d.selectedHuman

            human.load(os.path.join(modelPath, filename), self.app.progress)

            self.app.categories['Modelling'].tasksByName['Macro modelling'].syncSliders()
            self.app.categories['Modelling'].tasksByName['Macro modelling'].syncEthnics()
            self.app.categories['Modelling'].tasksByName['Macro modelling'].syncStatus()
            self.app.categories['Modelling'].tasksByName['Detail modelling'].syncSliders()

            del self.app.undoStack[:]
            del self.app.redoStack[:]

            self.parent.tasksByName['Save'].fileentry.text = filename.replace('.mhm', '')
            self.parent.tasksByName['Save'].fileentry.edit.setText(filename.replace('.mhm', ''))

            self.app.switchCategory('Modelling')
            self.app.scene3d.redraw(1)

    def onShow(self, event):

    # When the task gets shown, set the focus to the file chooser

        self.app.scene3d.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)
        self.filechooser.setFocus()

    # HACK: otherwise the toolbar background disappears for some weird reason

        self.app.scene3d.redraw(0)

    def onHide(self, event):
        self.app.scene3d.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)


class ExportTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Export', category.app.getThemeResource('images', 'button_export_file.png'), category.app.getThemeResource('images', 'button_export_file_on.png'))
        #gui3d.Object(self, 'data/3dobjs/unit_square.obj', self.app.getThemeResource('images', 'group_export_option.png'), [10, 80, 9.0], 158, 256)
        self.fileentry = gui3d.FileEntryView(self)

        self.exportBodyGroup = []
        self.exportHairGroup = []
        
        #### BODY EXPORT #######
        self.wavefrontObj = gui3d.RadioButton(self, self.exportBodyGroup, 'data/3dobjs/button_generic_long.obj', position=[25, 140, 9.2], label="Wavefront obj", selected=True)
        self.mhx = gui3d.RadioButton(self, self.exportBodyGroup, mesh='data/3dobjs/button_generic_long.obj', position=[25, 170, 9.2], label="Blender exchange")
        self.collada = gui3d.RadioButton(self, self.exportBodyGroup, mesh='data/3dobjs/button_generic_long.obj', position=[25, 200, 9.2], label="Collada")
        self.md5 = gui3d.RadioButton(self, self.exportBodyGroup, mesh='data/3dobjs/button_generic_long.obj', position=[25, 230, 9.2], label="MD5")
        self.stl = gui3d.RadioButton(self, self.exportBodyGroup, mesh='data/3dobjs/button_generic_long.obj', position=[25, 260, 9.2], label="STL")
                                         
        self.exportSkeleton = gui3d.ToggleButton(self, mesh='data/3dobjs/button_generic_long.obj', position=[625, 140, 9.2], label="Skeleton", selected=True)
                                                 
        self.exportGroups = gui3d.ToggleButton(self, mesh='data/3dobjs/button_generic_long.obj', position=[625, 170, 9.2], label="Groups", selected=True)

        ####### HAIR EXPORT ###################
        self.hairMesh = gui3d.RadioButton(self, self.exportHairGroup, mesh='data/3dobjs/button_generic_long.obj', position=[625, 200, 9.2], label="Hair as mesh", selected=True)

        self.hairCurves = gui3d.RadioButton(self, self.exportHairGroup, mesh='data/3dobjs/button_generic_long.obj', position=[625, 230, 9.2], label="Hair as curves")
        
        @self.wavefrontObj.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.wavefrontObj, event)
            self.updateGui()
            
        @self.mhx.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.mhx, event)
            self.updateGui()
        
        @self.collada.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.collada, event)
            self.updateGui()
        
        @self.md5.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.md5, event)
            self.updateGui()
        
        @self.stl.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.stl, event)
            self.updateGui()
        
        @self.fileentry.event
        def onFileSelected(filename):
            exportPath = mh.getPath('exports')
            if not os.path.exists(exportPath):
                os.makedirs(exportPath)

            if self.wavefrontObj.selected:
                mh2obj.exportObj(self.app.scene3d.selectedHuman.meshData, os.path.join(exportPath, filename + ".obj"), 'data/3dobjs/base.obj', self.exportGroups.selected)
                mh2proxy.exportProxyObj(self.app.scene3d.selectedHuman.meshData, os.path.join(exportPath, filename))
                
                if self.exportSkeleton.selected:
                    mh2bvh.exportSkeleton(self.app.scene3d.selectedHuman.meshData, os.path.join(exportPath, filename + ".bvh"))
                    
                if len(filename)> 0 and self.app.scene3d.selectedHuman.hairObj and len(self.app.scene3d.selectedHuman.hairObj.verts) > 0:
                    if self.hairMesh.selected:
                        mh2obj.exportObj(self.app.scene3d.selectedHuman.hairObj, os.path.join(exportPath, "hair_" + filename+".obj"))
                    else:
                        hairsClass = self.app.scene3d.selectedHuman.hairs
                        #hairsClass = self.app.categories["Library"].tasksByName["Hair"]
                        #hair.adjustHair(self.app.scene3d.selectedHuman, hairsClass)
                        file = open(os.path.join(exportPath, "hair_" + filename + ".obj"), 'w')
                        mh2obj.exportAsCurves(file, hairsClass.guides)
                        file.close()
                  
            elif self.mhx.selected:
                mh2mhx.exportMhx(self.app.scene3d.selectedHuman.meshData, os.path.join(exportPath, filename + ".mhx"))
            elif self.collada.selected:
                mh2collada.exportCollada(self.app.scene3d.selectedHuman.meshData, os.path.join(exportPath, filename))
            elif self.md5.selected:
                mh2md5.exportMd5(self.app.scene3d.selectedHuman.meshData, os.path.join(exportPath, filename + ".md5mesh"))
            elif self.stl.selected:
                mh2stl.exportStlBinary(self.app.scene3d.selectedHuman.meshData, os.path.join(exportPath, filename + ".stl"))

            self.app.switchCategory('Modelling')
            self.app.scene3d.redraw(1)
            
    def updateGui(self):
        if self.wavefrontObj.selected:
            self.exportSkeleton.show()
            self.exportGroups.show()
            self.hairMesh.show()
            self.hairCurves.show()
        else:
            self.exportSkeleton.hide()
            self.exportGroups.hide()
            self.hairMesh.hide()
            self.hairCurves.hide()

    def onShow(self, event):

    # When the task gets shown, set the focus to the file entry

        gui3d.TaskView.onShow(self, event)
        self.fileentry.setFocus()
        self.pan = self.app.scene3d.selectedHuman.getPosition()
        self.eyeX = mh.cameras[0].eyeX
        self.eyeY = mh.cameras[0].eyeY
        self.eyeZ = mh.cameras[0].eyeZ
        self.focusX = mh.cameras[0].focusX
        self.focusY = mh.cameras[0].focusY
        self.focusZ = mh.cameras[0].focusZ
        self.rotation = self.app.scene3d.selectedHuman.getRotation()
        self.app.scene3d.selectedHuman.setPosition([0, -1, 0])
        self.app.setGlobalCamera();
        mh.cameras[0].eyeZ = 70
        self.app.scene3d.selectedHuman.setRotation([0.0, 0.0, 0.0])

    def onHide(self, event):
        gui3d.TaskView.onHide(self, event)
        self.app.scene3d.selectedHuman.setPosition(self.pan)
        mh.cameras[0].eyeX = self.eyeX
        mh.cameras[0].eyeY = self.eyeY
        mh.cameras[0].eyeZ = self.eyeZ
        mh.cameras[0].focusX = self.focusX
        mh.cameras[0].focusY = self.focusY
        mh.cameras[0].focusZ = self.focusZ
        self.app.scene3d.selectedHuman.setRotation(self.rotation)


class FilesCategory(gui3d.Category):

    def __init__(self, parent):
        gui3d.Category.__init__(self, parent, 'Files', parent.app.getThemeResource('images', 'button_files.png'), parent.app.getThemeResource('images',
                                'button_files_on.png'))

        SaveTaskView(self)
        LoadTaskView(self)
        ExportTaskView(self)


