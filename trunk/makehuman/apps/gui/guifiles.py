#!/usr/bin/python
# -*- coding: utf-8 -*-
# You may use, modify and redistribute this module under the terms of the GNU GPL.

""" 
Class for handling File mode in the GUI.

B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2011

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
import gui3d
import os
import mh2obj
import mh2bvh
import mh2mhx
import mh2obj_proxy
import mh2collada
import mh2md5
import mh2stl
import mh2skel
from shutil import copyfile
from os.path import basename
import qtgui as gui

class SaveTaskView(gui3d.TaskView):

    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Save')
        self.fileentry = self.addView(gui3d.FileEntryView('Save'))
        
        mesh = gui3d.FrameMesh(100, 100)
        self.selection = gui3d.app.addObject(gui3d.Object([0, 0, 9], mesh))
        mesh.setColor([0, 0, 0, 255])
        mesh.setPickable(0)
        self.selection.hide()

        @self.fileentry.mhEvent
        def onFileSelected(filename):
            
            modelPath = mh.getPath('models')
            if not os.path.exists(modelPath):
                os.makedirs(modelPath)

            tags = filename

            # Save the thumbnail

            leftTop = self.selection.getPosition()
            mh.grabScreen(int(leftTop[0]+1), int(leftTop[1]+1), int(self.selection.width-1), int(self.selection.height-1), os.path.join(modelPath, filename + '.bmp'))

            # Save the model

            human = gui3d.app.selectedHuman
            human.save(os.path.join(modelPath, filename + '.mhm'), tags)
            
            gui3d.app.setCaption("MakeHuman r" + os.environ['SVNREVISION'] + " - [" + filename + "]")

            gui3d.app.switchCategory('Modelling')

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
        
        leftTop = gui3d.app.modelCamera.convertToScreen(-10, 9, 0)
        rightBottom = gui3d.app.modelCamera.convertToScreen(10, -10, 0)
        
        self.selection.setPosition([int(leftTop[0]) + 0.5, int(leftTop[1]) + 0.5, 9])
        self.selection.width = int(rightBottom[0] - leftTop[0])
        self.selection.height = int(rightBottom[1] - leftTop[1])
        self.selection.mesh.resize(self.selection.width, self.selection.height)
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
    
        leftTop = gui3d.app.modelCamera.convertToScreen(-10, 9, 0)
        rightBottom = gui3d.app.modelCamera.convertToScreen(10, -10, 0)
        
        self.selection.setPosition([int(leftTop[0]) + 0.5, int(leftTop[1]) + 0.5, 9])
        self.selection.width = int(rightBottom[0] - leftTop[0])
        self.selection.height = int(rightBottom[1] - leftTop[1])
        self.selection.mesh.resize(self.selection.width, self.selection.height)
        
class HumanFileSort(gui3d.FileSort):
    
    def __init__(self):
        
        gui3d.FileSort.__init__(self)
        self.meta = {}
    
    def fields(self):
        
        return list(gui3d.FileSort.fields(self)) + ["gender", "age", "muscle", "weight"]
        
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
        self.filechooser = self.addView(gui3d.FileChooser(modelPath, 'mhm', sort=HumanFileSort()))

        @self.filechooser.mhEvent
        def onFileSelected(filename):

            human = gui3d.app.selectedHuman

            human.load(filename, True, gui3d.app.progress)

            del gui3d.app.undoStack[:]
            del gui3d.app.redoStack[:]
            
            name = os.path.basename(filename).replace('.mhm', '')

            self.parent.tasksByName['Save'].fileentry.text = name
            self.parent.tasksByName['Save'].fileentry.edit.setText(name)
            
            gui3d.app.setCaption("MakeHuman r" + os.environ['SVNREVISION'] + " - [" + name + "]")

            gui3d.app.switchCategory('Modelling')

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

    def onResized(self, event):
        
        self.filechooser.onResized(event)

class ExportTaskView(gui3d.TaskView):
    
    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Export')
        self.fileentry = self.addView(gui3d.FileEntryView('Export'))

        self.exportBodyGroup = []
        self.exportHairGroup = []
        
        # Formats
        self.formatBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Format')))
        self.wavefrontObj = self.formatBox.addWidget(gui.RadioButton(self.exportBodyGroup, "Wavefront obj", True))
        self.mhx = self.formatBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="Blender exchange (mhx)"))
        self.collada = self.formatBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="Collada (dae)"))
        self.md5 = self.formatBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="MD5"))
        self.stl = self.formatBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="Stereolithography (stl)"))
        self.skel = self.formatBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="Skeleton (skel)"))
            
        # OBJ options
        self.objOptions = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Options')))
        self.exportEyebrows = self.objOptions.addWidget(gui.CheckBox("Eyebrows", True))
        self.exportLashes = self.objOptions.addWidget(gui.CheckBox("Eyelashes", True))
        self.exportHelpers = self.objOptions.addWidget(gui.CheckBox("Helper geometry", False))
        self.exportHidden = self.objOptions.addWidget(gui.CheckBox("Keep hidden faces", True))
        self.exportSkeleton = self.objOptions.addWidget(gui.CheckBox("Skeleton", True))
        self.exportSmooth = self.objOptions.addWidget(gui.CheckBox( "Subdivide", False))
        scales = []
        self.objScales = self.addScales(self.objOptions, scales, "Obj", True)

        # MHX options
        """
        y = yy
        self.mhxOptionsSource = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Options source')))
        source = []
        self.mhxConfig = self.mhxOptionsSource.addWidget(gui.RadioButton(source, "Use config options"))
        self.mhxGui = self.mhxOptionsSource.addWidget(gui.RadioButton(source, "Use gui options", True))
        self.mhxOptionsSource.hide()
        y+=16
        """
        
        self.mhxOptions = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Options')))
        #self.version24 = self.mhxOptions.addWidget(gui.CheckBox("Version 2.4", False))
        #self.version25 = self.mhxOptions.addWidget(gui.CheckBox("Version 2.5", True))
        self.mhxSeparateFolder = self.mhxOptions.addWidget(gui.CheckBox("Separate folder", False))
        self.mhxFeetOnGround = self.mhxOptions.addWidget(gui.CheckBox("Feet on ground", True))
        self.mhxHidden = self.mhxOptions.addWidget(gui.CheckBox("Keep hidden faces", True))
        self.mhxExpressionUnits = self.mhxOptions.addWidget(gui.CheckBox("Expressions", False))
        #self.mhxFaceShapes = self.mhxOptions.addWidget(gui.CheckBox("Face shapes", True))
        self.mhxBodyShapes = self.mhxOptions.addWidget(gui.CheckBox("Body shapes", True))
        self.mhxCustomShapes = self.mhxOptions.addWidget(gui.CheckBox("Custom shapes", False))
        #self.mhxFacePanel = self.mhxOptions.addWidget(gui.CheckBox("Face panel", True))
        self.mhxClothes = self.mhxOptions.addWidget(gui.CheckBox("Clothes", True))
        self.mhxClothesRig = self.mhxOptions.addWidget(gui.CheckBox("Clothes rig", True))
        self.mhxCage = self.mhxOptions.addWidget(gui.CheckBox("Cage", False))
        self.mhxAdvancedSpine = self.mhxOptions.addWidget(gui.CheckBox("Advanced spine", False))
        self.mhxMaleRig = self.mhxOptions.addWidget(gui.CheckBox("Male rig", False))
        #self.mhxSkirtRig = self.mhxOptions.addWidget(gui.CheckBox("Skirt rig", False))
        rigs = []
        self.mhxMhx = self.mhxOptions.addWidget(gui.RadioButton(rigs, "Use mhx rig", True))
        self.rigifyMhx = self.mhxOptions.addWidget(gui.RadioButton(rigs, "Use rigify rig", False))
        addedRigs = self.addRigs(self.mhxOptions, rigs, "Mhx", False)
        self.mhxRigs = [(self.mhxMhx, "mhx"), (self.rigifyMhx, "rigify")] + addedRigs
        self.mhxOptions.hide()
        
        # Collada options
        self.colladaOptions = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Options')))
        self.colladaRot90X = self.colladaOptions.addWidget(gui.CheckBox("Rotate 90 X", False))
        self.colladaRot90Z = self.colladaOptions.addWidget(gui.CheckBox("Rotate 90 Z", False))
        self.colladaEyebrows = self.colladaOptions.addWidget(gui.CheckBox("Eyebrows", True))
        self.colladaLashes = self.colladaOptions.addWidget(gui.CheckBox("Eyelashes", True))
        self.colladaHelpers = self.colladaOptions.addWidget(gui.CheckBox("Helper geometry", False))
        self.colladaHidden = self.colladaOptions.addWidget(gui.CheckBox("Keep hidden faces", True))
        # self.colladaSeparateFolder = self.colladaOptions.addWidget(gui.CheckBox("Separate folder", False))
        # self.colladaPngTexture = self.colladaOptions.addWidget(gui.CheckBox("PNG texture", selected=True))
        scales = []
        self.daeScales = self.addScales(self.colladaOptions, scales, "Dae", True)
        rigs = []
        self.daeRigs = self.addRigs(self.colladaOptions, rigs, "Dae", True)
        self.colladaOptions.hide()

        # STL options
        self.stlOptions = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Options')))
        stlOptions = []
        self.stlAscii = self.stlOptions.addWidget(gui.RadioButton(stlOptions,  "Ascii", selected=True))
        self.stlBinary = self.stlOptions.addWidget(gui.RadioButton(stlOptions, "Binary"))
        self.stlSmooth = self.stlOptions.addWidget(gui.CheckBox("Subdivide", False))
        self.stlOptions.hide()

        """                    
        @self.version24.mhEvent
        def onClicked(event):
            
            if self.version24.selected and self.version25.selected:
                self.version24.setSelected(False)
            else:
                self.version24.setSelected(True)
                
        @self.version25.mhEvent
        def onClicked(event):
            
            if self.version25.selected and self.version24.selected:
                self.version25.setSelected(False)
            else:
                self.version25.setSelected(True)
        """
        
        @self.wavefrontObj.mhEvent
        def onClicked(event):
            self.updateGui()
            
        @self.mhx.mhEvent
        def onClicked(event):
            self.updateGui()
        
        @self.collada.mhEvent
        def onClicked(event):
            self.updateGui()
        
        @self.md5.mhEvent
        def onClicked(event):
            self.updateGui()
        
        @self.stl.mhEvent
        def onClicked(event):
            self.updateGui()
            
        @self.skel.mhEvent
        def onClicked(event):
            self.updateGui()
        
        @self.fileentry.mhEvent
        def onFileSelected(filename):
            
            exportPath = mh.getPath('exports')
            if not os.path.exists(exportPath):
                os.makedirs(exportPath)

            if self.wavefrontObj.selected:
                
                human = gui3d.app.selectedHuman

                options = {
                    "helpers" : self.exportHelpers.selected,
                    "hidden" : self.exportHidden.selected,
                    "eyebrows" : self.exportEyebrows.selected,
                    "lashes" : self.exportLashes.selected,
                    "scale": self.getScale(self.objScales),
                }                    
                mh2obj_proxy.exportProxyObj(human, os.path.join(exportPath, filename), options)
                
                if self.exportSkeleton.selected:
                    mh2bvh.exportSkeleton(human.meshData, os.path.join(os.path.join(exportPath, filename), filename + ".bvh"))
                    
            elif self.mhx.selected:
                #mhxversion = []
                #if self.version24.selected: mhxversion.append('24')
                #if self.version25.selected: mhxversion.append('25')
                for (button, rig) in self.mhxRigs:
                    if button.selected:
                        break
                options = {
                    'mhxversion': ["25"],  #mhxversion,
                    'hidden':self.mhxHidden.selected,
                    #'expressions':False,    #self.mhxExpressions.selected,
                    'expressionunits':self.mhxExpressionUnits.selected,
                    #'faceshapes':self.mhxFaceShapes.selected,
                    'bodyshapes':self.mhxBodyShapes.selected,
                    'customshapes':self.mhxCustomShapes.selected,
                    #'facepanel':self.mhxFacePanel.selected,
                    'clothes':self.mhxClothes.selected,
                    'cage':self.mhxCage.selected,
                    'separatefolder':self.mhxSeparateFolder.selected,
                    'feetonground':self.mhxFeetOnGround.selected,
                    'advancedspine':self.mhxAdvancedSpine.selected,
                    'malerig':self.mhxMaleRig.selected,
                    'skirtrig':False, #self.mhxSkirtRig.selected,
                    'clothesrig':self.mhxClothesRig.selected,
                    'mhxrig': rig,
                }

                mh2mhx.exportMhx(gui3d.app.selectedHuman, os.path.join(exportPath, filename + ".mhx"), options)
            elif self.collada.selected:
                for (button, rig) in self.daeRigs:
                    if button.selected:
                        break                
                options = {
                    "daerig": rig,
                    "rotate90X" : self.colladaRot90X.selected,
                    "rotate90Z" : self.colladaRot90Z.selected,
                    "eyebrows" : self.colladaEyebrows.selected,
                    "lashes" : self.colladaLashes.selected,
                    "helpers" : self.colladaHelpers.selected,
                    "hidden" : self.colladaHidden.selected,
                    "scale": self.getScale(self.daeScales),
                }
                mh2collada.exportCollada(gui3d.app.selectedHuman, os.path.join(exportPath, filename), options)
            elif self.md5.selected:
                mh2md5.exportMd5(gui3d.app.selectedHuman.meshData, os.path.join(exportPath, filename + ".md5mesh"))
            elif self.stl.selected:
                mesh = gui3d.app.selectedHuman.getSubdivisionMesh() if self.exportSmooth.selected else gui3d.app.selectedHuman.meshData
                if self.stlAscii.selected:
                    mh2stl.exportStlAscii(mesh, os.path.join(exportPath, filename + ".stl"))
                else:
                    mh2stl.exportStlBinary(mesh, os.path.join(exportPath, filename + ".stl"))
            elif self.skel.selected:
                mesh = gui3d.app.selectedHuman.getSubdivisionMesh() if self.exportSmooth.selected else gui3d.app.selectedHuman.meshData
                mh2skel.exportSkel(mesh, os.path.join(exportPath, filename + ".skel"))
                    
            gui3d.app.prompt('Info', u'The mesh has been exported to %s.' % os.path.join(mh.getPath(''), u'exports'), 'OK', helpId='exportHelp')

            gui3d.app.switchCategory('Modelling')
            
    def updateGui(self):
        
        if self.wavefrontObj.selected:
            self.objOptions.show()
        else:
            self.objOptions.hide()
            
        if self.collada.selected:
            self.colladaOptions.show()
        else:
            self.colladaOptions.hide()
            
        if self.mhx.selected:
            self.mhxOptions.show()
        else:
            self.mhxOptions.hide()
            
        if self.stl.selected:
            self.stlOptions.show()
        else:
            self.stlOptions.hide()

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
        self.exportSmooth.setSelected(human.isSubdivided())
        self.stlSmooth.setSelected(human.isSubdivided())

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
        
    def addRigs(self, options, rigs, suffix, check):
        path = "data/rigs"
        if not os.path.exists(path):
            print("Did not find directory %s" % path)
            return (y, [])
        buttons = []
        for fname in os.listdir(path):
            (name, ext) = os.path.splitext(fname)
            if ext == ".rig":
                button = options.addWidget(gui.RadioButton(rigs, "Use %s rig" % name, check))
                setattr(self, name + suffix, button)
                check = False
                buttons.append((button,name))
        return buttons

    def addScales(self, options, scales, suffix, check):
        buttons = []
        for name in ["decimeter", "meter", "inch", "centimeter"]:
            button = options.addWidget(gui.RadioButton(scales, name, check))
            setattr(self, name + suffix, button)
            check = False
            buttons.append((button,name))
        return buttons
        
    def getScale(self, buttons):
        for (button, name) in buttons:
            if button.selected:
                if name == "decimeter":
                    return (1.0, name)
                elif name == "meter":
                    return (0.1, name)
                elif name == "inch":
                    return (0.254, name)
                elif name == "centimeter":
                    return (10, name)
        return (1, "decimeter")                    
        
class FilesCategory(gui3d.Category):

    def __init__(self, parent):
        
        gui3d.Category.__init__(self, parent, 'Files')

        self.addView(SaveTaskView(self))
        self.addView(LoadTaskView(self))
        self.addView(ExportTaskView(self))


