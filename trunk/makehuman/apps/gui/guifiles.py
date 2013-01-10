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
from shutil import copyfile, move
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
            mh.grabScreen(int(x0+1), int(y1+1), int(x1-x0-1), int(y0-y1-1), os.path.join(dir, name + '.png'))
            move(os.path.join(dir, name + '.png'), os.path.join(dir, name + '.thumb'))

            # Save the model

            human = gui3d.app.selectedHuman
            human.save(path, name)
            gui3d.app.modified = False
            
            gui3d.app.setCaption("MakeHuman r" + os.environ['SVNREVISION'] + " - [" + filename + "]")

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
            
            gui3d.app.setCaption("MakeHuman r" + os.environ['SVNREVISION'] + " - [" + name + "]")

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

        exportPath = mh.getPath('exports')

        self.fileentry = self.addTopWidget(gui.FileEntryView('Export'))
        self.fileentry.setDirectory(exportPath)
        self.fileentry.setFilter('All Files (*.*)')

        self.exportBodyGroup = []
        self.exportHairGroup = []
        
        # Mesh Formats
        self.formatBox = self.addLeftWidget(gui.GroupBox('Mesh Format'))
        self.wavefrontObj = self.formatBox.addWidget(gui.RadioButton(self.exportBodyGroup, "Wavefront obj", True))
        self.mhx = self.formatBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="Blender exchange (mhx)"))
        self.collada = self.formatBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="Collada (dae)"))
        self.md5 = self.formatBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="MD5"))
        self.stl = self.formatBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="Stereolithography (stl)"))

        # Rig formats
        self.rigBox = self.addLeftWidget(gui.GroupBox('Rig format'))
        self.skel = self.rigBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="Skeleton (skel)"))

        # Map formats
        self.mapsBox = self.addLeftWidget(gui.GroupBox('Maps'))
        self.lightmap = self.mapsBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="Lightmap"))
        self.uvmap = self.mapsBox.addWidget(gui.RadioButton(self.exportBodyGroup, label="UV map"))

        self.optionsBox = self.addRightWidget(gui.StackedBox())

        # OBJ options
        self.objOptions = self.optionsBox.addWidget(gui.GroupBox('Options'))
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
        self.mhxOptionsSource = self.optionsBox.addWidget(gui.GroupBox('Options source'))
        source = []
        self.mhxConfig = self.mhxOptionsSource.addWidget(gui.RadioButton(source, "Use config options"))
        self.mhxGui = self.mhxOptionsSource.addWidget(gui.RadioButton(source, "Use gui options", True))
        self.mhxOptionsSource.hide()
        y+=16
        """
        
        self.mhxOptions = self.optionsBox.addWidget(gui.GroupBox('Options'))
        #self.version24 = self.mhxOptions.addWidget(gui.CheckBox("Version 2.4", False))
        #self.version25 = self.mhxOptions.addWidget(gui.CheckBox("Version 2.5", True))
        self.mhxSeparateFolder = self.mhxOptions.addWidget(gui.CheckBox("Separate folder", False))
        self.mhxFeetOnGround = self.mhxOptions.addWidget(gui.CheckBox("Feet on ground", True))
        self.mhxExpressionUnits = self.mhxOptions.addWidget(gui.CheckBox("Expressions", False))
        #self.mhxFaceShapes = self.mhxOptions.addWidget(gui.CheckBox("Face shapes", True))
        self.mhxBodyShapes = self.mhxOptions.addWidget(gui.CheckBox("Body shapes", True))
        self.mhxCustomShapes = self.mhxOptions.addWidget(gui.CheckBox("Custom shapes", False))
        #self.mhxFacePanel = self.mhxOptions.addWidget(gui.CheckBox("Face panel", True))
        self.mhxClothes = self.mhxOptions.addWidget(gui.CheckBox("Clothes", True))
        self.mhxMasks = self.mhxOptions.addWidget(gui.CheckBox("Clothes masks", False))
        self.mhxHidden = self.mhxOptions.addWidget(gui.CheckBox("Keep hidden faces", True))
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
        
        # Collada options
        self.colladaOptions = self.optionsBox.addWidget(gui.GroupBox('Options'))
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

        # STL options
        self.stlOptions = self.optionsBox.addWidget(gui.GroupBox('Options'))
        stlOptions = []
        self.stlAscii = self.stlOptions.addWidget(gui.RadioButton(stlOptions,  "Ascii", selected=True))
        self.stlBinary = self.stlOptions.addWidget(gui.RadioButton(stlOptions, "Binary"))
        self.stlSmooth = self.stlOptions.addWidget(gui.CheckBox("Subdivide", False))

        self.md5Options = self.optionsBox.addWidget(gui.GroupBox('Options'))
        self.skelOptions = self.optionsBox.addWidget(gui.GroupBox('Options'))

        # Lightmap options
        self.lightmapOptions = self.optionsBox.addWidget(gui.GroupBox('Options'))
        lightmapOptions = []
        self.lightmapDisplay = self.lightmapOptions.addWidget(gui.RadioButton(lightmapOptions,  "Display on human", selected=False))

        # Lightmap options
        self.uvmapOptions = self.optionsBox.addWidget(gui.GroupBox('Options'))
        uvmapOptions = []
        self.uvmapDisplay = self.uvmapOptions.addWidget(gui.RadioButton(uvmapOptions,  "Display on human", selected=False))

        self.updateGui()

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
            self.fileentry.setFilter('Wavefront (*.obj)')
            
        @self.mhx.mhEvent
        def onClicked(event):
            self.updateGui()
            self.fileentry.setFilter('Blender Exchange (*.mhx)')
        
        @self.collada.mhEvent
        def onClicked(event):
            self.updateGui()
            self.fileentry.setFilter('Collada (*.dae)')
        
        @self.md5.mhEvent
        def onClicked(event):
            self.updateGui()
            self.fileentry.setFilter('MD5 (*.md5)')
        
        @self.stl.mhEvent
        def onClicked(event):
            self.updateGui()
            self.fileentry.setFilter('Stereolithography (*.stl)')
            
        @self.skel.mhEvent
        def onClicked(event):
            self.updateGui()
            self.fileentry.setFilter('Skeleton (*.skel)')

        @self.lightmap.mhEvent
        def onClicked(event):
            self.updateGui()
            self.fileentry.setFilter('PNG (*.png)')

        @self.uvmap.mhEvent
        def onClicked(event):
            self.updateGui()
            self.fileentry.setFilter('PNG (*.png)')
        
        @self.fileentry.mhEvent
        def onFileSelected(filename):
            import mh2obj, mh2bvh, mh2mhx, mh2obj_proxy, mh2collada, mh2md5, mh2stl, mh2skel

            path = os.path.normpath(os.path.join(exportPath, filename))
            dir, name = os.path.split(path)
            name, ext = os.path.splitext(name)

            if not os.path.exists(dir):
                os.makedirs(dir)

            def filename(targetExt, different = False):
                if not different and ext != '' and ('.' + targetExt.lower()) != ext.lower():
                    log.warning("expected extension '.%s' but got '%s'", targetExt, ext)
                return os.path.join(dir, name + '.' + targetExt)

            if self.wavefrontObj.selected:
                
                human = gui3d.app.selectedHuman

                options = {
                    "helpers" : self.exportHelpers.selected,
                    "hidden" : self.exportHidden.selected,
                    "eyebrows" : self.exportEyebrows.selected,
                    "lashes" : self.exportLashes.selected,
                    "scale": self.getScale(self.objScales),
                    "subdivide": self.exportSmooth.selected
                }                    
                mh2obj_proxy.exportProxyObj(human, filename("obj"), options)
                
                if self.exportSkeleton.selected:
                    mh2bvh.exportSkeleton(human.meshData, filename("bvh", True))
                    
            elif self.mhx.selected:
                #mhxversion = []
                #if self.version24.selected: mhxversion.append('24')
                #if self.version25.selected: mhxversion.append('25')
                for (button, rig) in self.mhxRigs:
                    if button.selected:
                        break
                options = {
                    'mhxversion': ["25"],  #mhxversion,
                    'usemasks':self.mhxMasks.selected,
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

                mh2mhx.exportMhx(gui3d.app.selectedHuman, filename("mhx"), options)
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
                mh2collada.exportCollada(gui3d.app.selectedHuman, filename("dae"), options)
            elif self.md5.selected:
                mh2md5.exportMd5(gui3d.app.selectedHuman.meshData, filename("md5mesh"))
            elif self.stl.selected:
                mesh = gui3d.app.selectedHuman.getSubdivisionMesh() if self.exportSmooth.selected else gui3d.app.selectedHuman.meshData
                if self.stlAscii.selected:
                    mh2stl.exportStlAscii(mesh, filename("stl"))
                else:
                    mh2stl.exportStlBinary(mesh, filename("stl"))
            elif self.skel.selected:
                mesh = gui3d.app.selectedHuman.getSubdivisionMesh() if self.exportSmooth.selected else gui3d.app.selectedHuman.meshData
                mh2skel.exportSkel(mesh, filename("skel"))
            elif self.lightmap.selected:
                import projection
                human = gui3d.app.selectedHuman
                dstImg = projection.mapLighting()
                filepath = filename("png")
                dstImg.save(filepath)
                if self.lightmapDisplay:
                    human.setTexture(filepath)
                    log.debug("Enabling shadeless rendering on body")
                    human.mesh.setShadeless(True)
            elif self.uvmap.selected:
                import projection
                human = gui3d.app.selectedHuman
                dstImg = projection.mapUV()
                filepath = filename("png")
                dstImg.save(filepath)
                if self.uvmapDisplay:
                    human.setTexture(filepath)
                    log.debug("Enabling shadeless rendering on body")
                    human.mesh.setShadeless(True)
            else:
                log.error("Unknown export format selected!")
                return

            gui3d.app.prompt('Info', u'The mesh has been exported to %s.' % dir, 'OK', helpId='exportHelp')

            mh.changeCategory('Modelling')
            
    def updateGui(self):
        if self.wavefrontObj.selected:
            self.optionsBox.showWidget(self.objOptions)
        elif self.mhx.selected:
            self.optionsBox.showWidget(self.mhxOptions)
        elif self.collada.selected:
            self.optionsBox.showWidget(self.colladaOptions)
        elif self.md5.selected:
            self.optionsBox.showWidget(self.md5Options)
        elif self.stl.selected:
            self.optionsBox.showWidget(self.stlOptions)
        elif self.skel.selected:
            self.optionsBox.showWidget(self.skelOptions)
        elif self.lightmap.selected:
            self.optionsBox.showWidget(self.lightmapOptions)
        elif self.uvmap.selected:
            self.optionsBox.showWidget(self.uvmapOptions)

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
            log.message("Did not find directory %s", path)
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

    def __init__(self):
        super(FilesCategory, self).__init__('Files')

        self.addTask(SaveTaskView(self))
        self.addTask(LoadTaskView(self))
        self.addTask(ExportTaskView(self))
