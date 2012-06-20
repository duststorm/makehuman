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

class SaveTaskView(gui3d.TaskView):

    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Save')
        self.fileentry = self.addView(gui3d.FileEntryView('Save'))
        
        mesh = gui3d.FrameMesh(100, 100)
        self.selection = gui3d.app.addObject(gui3d.Object([0, 0, 9], mesh))
        mesh.setColor([0, 0, 0, 255])
        mesh.setPickable(0)
        self.selection.hide()

        @self.fileentry.event
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
            
            gui3d.app.setCaption("MakeHuman - [%s]" % filename)

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

        @self.filechooser.event
        def onFileSelected(filename):

            human = gui3d.app.selectedHuman

            human.load(filename, True, gui3d.app.progress)

            del gui3d.app.undoStack[:]
            del gui3d.app.redoStack[:]
            
            name = os.path.basename(filename).replace('.mhm', '')

            self.parent.tasksByName['Save'].fileentry.text = name
            self.parent.tasksByName['Save'].fileentry.edit.setText(name)
            
            gui3d.app.setCaption("MakeHuman - [%s]" % name)

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
        y = 80
        self.formatBox = self.addView(gui3d.GroupBox([10, y, 9.0], 'Format', gui3d.GroupBoxStyle._replace(height=25+24*5+6)));y+=25
        self.wavefrontObj = self.formatBox.addView(gui3d.RadioButton(self.exportBodyGroup, "Wavefront obj", True, gui3d.ButtonStyle));y+=24
        self.mhx = self.formatBox.addView(gui3d.RadioButton(self.exportBodyGroup, label="Blender exchange (mhx)", style=gui3d.ButtonStyle));y+=24
        self.collada = self.formatBox.addView(gui3d.RadioButton(self.exportBodyGroup, label="Collada (dae)", style=gui3d.ButtonStyle));y+=24
        self.md5 = self.formatBox.addView(gui3d.RadioButton(self.exportBodyGroup, label="MD5", style=gui3d.ButtonStyle));y+=24
        self.stl = self.formatBox.addView(gui3d.RadioButton(self.exportBodyGroup, label="Stereolithography (stl)", style=gui3d.ButtonStyle));y+=24
        self.skel = self.formatBox.addView(gui3d.RadioButton(self.exportBodyGroup, label="Skeleton (skel)", style=gui3d.ButtonStyle));y+=24
        y+=16
            
        # OBJ options
        yy = y
        self.objOptions = self.addView(gui3d.GroupBox([10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*10+6)));y+=25
        self.exportEyebrows = self.objOptions.addView(gui3d.CheckBox("Eyebrows", True));y+=24
        self.exportLashes = self.objOptions.addView(gui3d.CheckBox("Eyelashes", True));y+=24
        self.exportDiamonds = self.objOptions.addView(gui3d.CheckBox("Diamonds", False));y+=24
        self.exportSkeleton = self.objOptions.addView(gui3d.CheckBox("Skeleton", True));y+=24
        self.exportGroups = self.objOptions.addView(gui3d.CheckBox("Groups", True));y+=24
        self.exportSmooth = self.objOptions.addView(gui3d.CheckBox( "Subdivide", False));y+=24
        self.exportHair = self.objOptions.addView(gui3d.CheckBox("Hair as mesh", selected=True));y+=24
        self.exportPngTexture = self.objOptions.addView(gui3d.CheckBox("PNG texture", selected=True));y+=24
        scales = []
        (y, self.objScales) = self.addScales( self.objOptions, scales, "Obj", True, y)

        # MHX options
        y = yy
        self.mhxOptionsSource = self.addView(gui3d.GroupBox([10, y, 9.0], 'Options source', gui3d.GroupBoxStyle._replace(height=25+24*2+6)));y+=25
        source = []
        self.mhxConfig = self.mhxOptionsSource.addView(gui3d.RadioButton(source, "Use config options"));y+=24
        self.mhxGui = self.mhxOptionsSource.addView(gui3d.RadioButton(source, "Use gui options", True));y+=24
        self.mhxOptionsSource.hide()
        y+=16
        
        self.mhxOptions = self.addView(gui3d.GroupBox([10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*14+6)));y+=25
        self.version24 = self.mhxOptions.addView(gui3d.CheckBox("Version 2.4", False));y+=24
        self.version25 = self.mhxOptions.addView(gui3d.CheckBox("Version 2.5", True));y+=24
        self.exportSeparateFolder = self.mhxOptions.addView(gui3d.CheckBox("Separate folder", False));y+=24
        self.exportFeetOnGround = self.mhxOptions.addView(gui3d.CheckBox("Feet on ground", True));y+=24
        self.exportExpressions = self.mhxOptions.addView(gui3d.CheckBox("Expressions", False));y+=24
        self.exportFaceShapes = self.mhxOptions.addView(gui3d.CheckBox("Face shapes", False));y+=24
        self.exportBodyShapes = self.mhxOptions.addView(gui3d.CheckBox("Body shapes", True));y+=24
        self.exportFacePanel = self.mhxOptions.addView(gui3d.CheckBox("Face panel", False));y+=24
        self.exportClothes = self.mhxOptions.addView(gui3d.CheckBox("Clothes", True));y+=24
        self.exportClothesRig = self.mhxOptions.addView(gui3d.CheckBox("Clothes rig", True));y+=24
        self.exportCage = self.mhxOptions.addView(gui3d.CheckBox("Cage", False));y+=24
        #self.exportBreastRig = self.mhxOptions.addView(gui3d.CheckBox("Breast rig", False));y+=24
        self.exportMaleRig = self.mhxOptions.addView(gui3d.CheckBox("Male rig", False));y+=24
        #self.exportSkirtRig = self.mhxOptions.addView(gui3d.CheckBox("Skirt rig", False));y+=24
        rigs = []
        self.mhxMhx = self.mhxOptions.addView(gui3d.RadioButton(rigs, "Use mhx rig", True));y+=24
        self.rigifyMhx = self.mhxOptions.addView(gui3d.RadioButton(rigs, "Use rigify rig", False));y+=24
        (y, addedRigs) = self.addRigs( self.mhxOptions, rigs, "Mhx", False, y)
        self.mhxRigs = [(self.mhxMhx, "mhx"), (self.rigifyMhx, "rigify")] + addedRigs
        self.mhxOptions.hide()
        
        # Collada options
        y = yy
        self.colladaOptions = self.addView(gui3d.GroupBox([10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*8+6)));y+=25
        self.colladaRot90X = self.colladaOptions.addView(gui3d.CheckBox("Rotate 90 X", False));y+=24
        self.colladaRot90Z = self.colladaOptions.addView(gui3d.CheckBox("Rotate 90 Z", False));y+=24
        self.colladaEyebrows = self.colladaOptions.addView(gui3d.CheckBox("Eyebrows", True));y+=24
        self.colladaLashes = self.colladaOptions.addView(gui3d.CheckBox("Eyelashes", True));y+=24
        self.colladaHelpers = self.colladaOptions.addView(gui3d.CheckBox("Helper geometry", False));y+=24
        # self.colladaSeparateFolder = self.colladaOptions.addView(gui3d.CheckBox("Separate folder", False));y+=24
        self.colladaPngTexture = self.colladaOptions.addView(gui3d.CheckBox("PNG texture", selected=True));y+=24
        scales = []
        (y, self.daeScales) = self.addScales( self.colladaOptions, scales, "Dae", True, y)
        rigs = []
        (y, self.daeRigs) = self.addRigs( self.colladaOptions, rigs, "Dae", True, y)
        self.colladaOptions.hide()

        # STL options
        y = yy
        self.stlOptions = self.addView(gui3d.GroupBox([10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*3+6)));y+=25
        stlOptions = []
        self.stlAscii = self.stlOptions.addView(gui3d.RadioButton(stlOptions,  "Ascii", selected=True));y+=24
        self.stlBinary = self.stlOptions.addView(gui3d.RadioButton(stlOptions, "Binary"));y+=24
        self.stlSmooth = self.stlOptions.addView(gui3d.CheckBox("Subdivide", False));y+=24
        self.stlOptions.hide()
        
        @self.mhxConfig.event
        def onClicked(event):
            
            gui3d.RadioButton.onClicked(self.mhxConfig, event)
            self.mhxOptions.hide()
            
        @self.mhxGui.event
        def onClicked(event):
            
            gui3d.RadioButton.onClicked(self.mhxGui, event)
            self.mhxOptions.show()
            
        @self.version24.event
        def onClicked(event):
            
            if self.version24.selected and self.version25.selected:
                self.version24.setSelected(False)
            else:
                self.version24.setSelected(True)
                
        @self.version25.event
        def onClicked(event):
            
            if self.version25.selected and self.version24.selected:
                self.version25.setSelected(False)
            else:
                self.version25.setSelected(True)
        
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
            
        @self.skel.event
        def onClicked(event):
            
            gui3d.RadioButton.onClicked(self.skel, event)
            self.updateGui()
        
        @self.fileentry.event
        def onFileSelected(filename):
            
            exportPath = mh.getPath('exports')
            if not os.path.exists(exportPath):
                os.makedirs(exportPath)

            if self.wavefrontObj.selected:
                
                if self.exportEyebrows.selected and self.exportDiamonds.selected:
                    filter = None
                elif self.exportEyebrows.selected:
                    filter = lambda fg: not ('joint' in fg.name or 'helper' in fg.name)
                elif self.exportDiamonds.selected:
                    filter = lambda fg: not 'eyebrown' in fg.name
                else:
                    filter = lambda fg: not ('joint' in fg.name or 'helper' in fg.name or 'eyebrown' in fg.name)
                    
                human = gui3d.app.selectedHuman
                    
                mesh = human.getSubdivisionMesh() if self.exportSmooth.selected else human.getSeedMesh()
                
                mh2obj.exportObj(mesh,
                    os.path.join(exportPath, filename + ".obj"),
                    self.exportGroups.selected,
                    filter)
                    
                options = {
                    "helpers" : self.exportDiamonds.selected,
                    "eyebrows" : self.exportEyebrows.selected,
                    "lashes" : self.exportLashes.selected,
                    "scale": self.getScale(self.objScales),
                    "pngTexture": self.exportPngTexture.selected
                }                    
                mh2obj_proxy.exportProxyObj(gui3d.app.selectedHuman, os.path.join(exportPath, filename), options)
                
                if self.exportSkeleton.selected:
                    mh2bvh.exportSkeleton(human.meshData, os.path.join(exportPath, filename + ".bvh"))
                    
                if self.exportHair.selected and human.hairObj and human.hairObj.mesh and human.hairObj.mesh.verts:
                    mesh = human.hairObj.getSubdivisionMesh() if self.exportSmooth.selected else human.hairObj.getSeedMesh()
                    mh2obj.exportObj(mesh, os.path.join(exportPath, "hair_" + filename+".obj"))
                    texturePath = os.path.join(exportPath, basename(mesh.texture))
                    if not os.path.isfile(texturePath):
                        copyfile(mesh.texture, texturePath)
                        
                texturePath = os.path.join(exportPath, basename(mesh.texture))
                if not os.path.isfile(texturePath):
                    copyfile(mesh.texture, texturePath)
                  
            elif self.mhx.selected:
                if self.mhxConfig.selected:
                    options = None
                else:
                    mhxversion = []
                    if self.version24.selected: mhxversion.append('24')
                    if self.version25.selected: mhxversion.append('25')
                    for (button, rig) in self.mhxRigs:
                        if button.selected:
                            break
                    options = {
                        'mhxversion':mhxversion,
                        'expressions':self.exportExpressions.selected,
                        'faceshapes':self.exportFaceShapes.selected,
                        'bodyshapes':self.exportBodyShapes.selected,
                        'facepanel':self.exportFacePanel.selected,
                        'clothes':self.exportClothes.selected,
                        'cage':self.exportCage.selected,
                        'separatefolder':self.exportSeparateFolder.selected,
                        'feetonground':self.exportFeetOnGround.selected,
                        'breastrig':False, #self.exportBreastRig.selected,
                        'malerig':self.exportMaleRig.selected,
                        'skirtrig':False, #self.exportSkirtRig.selected,
                        'clothesrig':self.exportClothesRig.selected,
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
                    "scale": self.getScale(self.daeScales),
                    "pngTexture": self.colladaPngTexture.selected
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
            self.mhxOptionsSource.show()
            if self.mhxGui.selected:
                self.mhxOptions.show()
        else:
            self.mhxOptionsSource.hide()
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
        
    def addRigs(self, options, rigs, suffix, check, y):
        path = "data/rigs"
        if not os.path.exists(path):
            print("Did not find directory %s" % path)
            return (y, [])
        buttons = []
        for fname in os.listdir(path):
            (name, ext) = os.path.splitext(fname)
            if ext == ".rig":
                expr = 'self.%s%s = options.addView(gui3d.RadioButton(rigs, "Use %s rig", check))' % (name, suffix, name)
                #print(expr)
                exec(expr)
                check = False
                y += 24
                button = eval('self.%s%s' % (name, suffix))
                buttons.append((button,name))
        return (y, buttons)                

    def addScales(self, options, scales, suffix, check, y):
        buttons = []
        for name in ["decimeter", "meter", "inch", "centimeter"]:
            expr = 'self.%s%s = options.addView(gui3d.RadioButton(scales, "%s", check))' % (name, suffix, name)
            #print(expr)
            exec(expr)
            check = False
            y += 24
            button = eval('self.%s%s' % (name, suffix))
            buttons.append((button,name))
        return (y, buttons)   
        
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


