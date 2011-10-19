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
from shutil import copyfile
from os.path import basename

class SaveTaskView(gui3d.TaskView):

    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Save')
        self.fileentry = gui3d.FileEntryView(self, 'Save')

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

            human = self.app.selectedHuman
            human.save(os.path.join(modelPath, filename + '.mhm'), tags)
            
            mh.setCaption("MakeHuman - [%s]" % filename)

            self.app.switchCategory('Modelling')

    def onShow(self, event):

        # When the task gets shown, set the focus to the file entry

        gui3d.TaskView.onShow(self, event)
        self.fileentry.setFocus()
        self.pan = self.app.selectedHuman.getPosition()
        self.eyeX = mh.cameras[0].eyeX
        self.eyeY = mh.cameras[0].eyeY
        self.eyeZ = mh.cameras[0].eyeZ
        self.focusX = mh.cameras[0].focusX
        self.focusY = mh.cameras[0].focusY
        self.focusZ = mh.cameras[0].focusZ
        self.rotation = self.app.selectedHuman.getRotation()
        self.app.selectedHuman.setPosition([0, -1, 0])
        self.app.setGlobalCamera();
        mh.cameras[0].eyeZ = 70
        self.app.selectedHuman.setRotation([0.0, 0.0, 0.0])

    def onHide(self, event):
        
        gui3d.TaskView.onHide(self, event)
        self.app.selectedHuman.setPosition(self.pan)
        mh.cameras[0].eyeX = self.eyeX
        mh.cameras[0].eyeY = self.eyeY
        mh.cameras[0].eyeZ = self.eyeZ
        mh.cameras[0].focusX = self.focusX
        mh.cameras[0].focusY = self.focusY
        mh.cameras[0].focusZ = self.focusZ
        self.app.selectedHuman.setRotation(self.rotation)
        
class HumanFileSort(gui3d.FileSort):
    
    def __init__(self):
        
        gui3d.FileSort.__init__(self)
        self.meta = {}
    
    def fields(self):
        
        return list(gui3d.FileSort.fields(self)) + ["gender", "age", "muscle", "weight"]
        
    def sortGender(self, path, filenames):
        
        self.updateMeta(path, filenames)
        decorated = [(self.meta[filename]['gender'], i, filename) for i, filename in enumerate(filenames)]
        decorated.sort()
        return [filename for gender, i, filename in decorated]
        
    def sortAge(self, path, filenames):
        
        self.updateMeta(path, filenames)
        decorated = [(self.meta[filename]['age'], i, filename) for i, filename in enumerate(filenames)]
        decorated.sort()
        return [filename for age, i, filename in decorated]

    def sortMuscle(self, path, filenames):
        
        self.updateMeta(path, filenames)
        decorated = [(self.meta[filename]['muscle'], i, filename) for i, filename in enumerate(filenames)]
        decorated.sort()
        return [filename for muscle, i, filename in decorated]
       
    def sortWeight(self, path, filenames):
        
        self.updateMeta(path, filenames)
        decorated = [(self.meta[filename]['weight'], i, filename) for i, filename in enumerate(filenames)]
        decorated.sort()
        return [filename for weight, i, filename in decorated]
        
    def updateMeta(self, path, filenames):
        
        for filename in filenames:
            
            if filename in self.meta:
                
                if self.meta[filename]['modified'] < os.path.getmtime(os.path.join(path, filename)):
                
                    self.meta[filename] = self.getMeta(path, filename)
                
            else:
                
                self.meta[filename] = self.getMeta(path, filename)
                
    def getMeta(self, path, filename):
        
        meta = {}
                
        meta['modified'] = os.path.getmtime(os.path.join(path, filename))
        f = open(os.path.join(path, filename))
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
        self.filechooser = gui3d.FileChooser(self, modelPath, 'mhm', sort=HumanFileSort())

        @self.filechooser.event
        def onFileSelected(filename):

            human = self.app.selectedHuman

            human.load(filename, True, self.app.progress)

            del self.app.undoStack[:]
            del self.app.redoStack[:]
            
            name = os.path.basename(filename).replace('.mhm', '')

            self.parent.tasksByName['Save'].fileentry.text = name
            self.parent.tasksByName['Save'].fileentry.edit.setText(name)
            
            mh.setCaption(("MakeHuman - [%s]" % name).encode("utf8"))

            self.app.switchCategory('Modelling')

    def onShow(self, event):

        # When the task gets shown, set the focus to the file chooser

        self.app.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)
        self.filechooser.setFocus()

        # HACK: otherwise the toolbar background disappears for some weird reason

        self.app.redraw()

    def onHide(self, event):
        
        self.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)

    def onResized(self, event):
        
        self.filechooser.onResized(event)

class GuiProxy():

    def __init__(self, options, y):
    
        proxies = []
        self.noProxy = gui3d.RadioButton(options, proxies, "No proxy", True);y+=24
        self.rorkimaru = gui3d.RadioButton(options, proxies, "Rorkimaru proxy");y+=24
        self.ascottk = gui3d.RadioButton(options, proxies, "Ascottk proxy");y+=24
        self.forsaken = gui3d.RadioButton(options, proxies, "Forsaken proxy");y+=24
        self.new_male = gui3d.RadioButton(options, proxies, "New male mesh");y+=24
        
    def getName(self):
    
        if self.rorkimaru.selected:
            return 'Rorkimaru'
        elif self.ascottk.selected:
            return'ascottk'
        elif self.forsaken.selected:
            return'forsaken'
        elif self.new_male.selected:
            return'new_male'
        else:
            return None

class ExportTaskView(gui3d.TaskView):
    
    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Export')
        self.fileentry = gui3d.FileEntryView(self, 'Export')

        self.exportBodyGroup = []
        self.exportHairGroup = []
        
        # Formats
        y = 80
        self.formatBox = gui3d.GroupBox(self, [10, y, 9.0], 'Format', gui3d.GroupBoxStyle._replace(height=25+24*5+6));y+=25
        self.wavefrontObj = gui3d.RadioButton(self.formatBox, self.exportBodyGroup, "Wavefront obj", True, gui3d.ButtonStyle);y+=24
        self.mhx = gui3d.RadioButton(self.formatBox, self.exportBodyGroup, label="Blender exchange (mhx)", style=gui3d.ButtonStyle);y+=24
        self.collada = gui3d.RadioButton(self.formatBox, self.exportBodyGroup, label="Collada (dae)", style=gui3d.ButtonStyle);y+=24
        self.md5 = gui3d.RadioButton(self.formatBox, self.exportBodyGroup, label="MD5", style=gui3d.ButtonStyle);y+=24
        self.stl = gui3d.RadioButton(self.formatBox, self.exportBodyGroup, label="Stereolithography (stl)", style=gui3d.ButtonStyle);y+=24
        y+=16
            
        # OBJ options
        yy = y
        self.objOptions = gui3d.GroupBox(self, [10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*10+6));y+=25
        self.exportEyebrows = gui3d.CheckBox(self.objOptions, "Eyebrows", True);y+=24
        self.exportDiamonds = gui3d.CheckBox(self.objOptions, "Diamonds", False);y+=24
        self.exportSkeleton = gui3d.CheckBox(self.objOptions, "Skeleton", True);y+=24
        self.exportGroups = gui3d.CheckBox(self.objOptions, "Groups", True);y+=24
        self.exportSmooth = gui3d.CheckBox(self.objOptions, "Subdivide", False);y+=24
        self.exportHair = gui3d.CheckBox(self.objOptions, "Hair as mesh", selected=True);y+=24
        self.objProxy = GuiProxy(self.objOptions, y)
        
        # MHX options
        y = yy
        self.mhxOptionsSource = gui3d.GroupBox(self, [10, y, 9.0], 'Options source', gui3d.GroupBoxStyle._replace(height=25+24*2+6));y+=25
        source = []
        self.mhxConfig = gui3d.RadioButton(self.mhxOptionsSource, source, "Use config options", True);y+=24
        self.mhxGui = gui3d.RadioButton(self.mhxOptionsSource, source, "Use gui options");y+=24
        self.mhxOptionsSource.hide()
        y+=16
        
        self.mhxOptions = gui3d.GroupBox(self, [10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*14+6));y+=25
        self.version24 = gui3d.CheckBox(self.mhxOptions, "Version 2.4", True);y+=24
        self.version25 = gui3d.CheckBox(self.mhxOptions, "Version 2.5", True);y+=24
        self.exportExpressions = gui3d.CheckBox(self.mhxOptions, "Expressions", True);y+=24
        self.exportFaceShapes = gui3d.CheckBox(self.mhxOptions, "Face shapes", True);y+=24
        self.exportBodyShapes = gui3d.CheckBox(self.mhxOptions, "Body shapes", False);y+=24
        self.exportClothes = gui3d.CheckBox(self.mhxOptions, "Clothes", True);y+=24
        self.exportCage = gui3d.CheckBox(self.mhxOptions, "Cage", False);y+=24
        rigs = []
        self.mhxRig = gui3d.RadioButton(self.mhxOptions, rigs, "Use mhx rig", True);y+=24
        self.rigifyRig = gui3d.RadioButton(self.mhxOptions, rigs, "Use rigify rig");y+=24
        self.gameRig = gui3d.RadioButton(self.mhxOptions, rigs, "Use game rig");y+=24
        self.mhxProxy = GuiProxy(self.mhxOptions, y)

        self.mhxOptions.hide()
        
        # Collada options
        y = yy
        self.colladaOptions = gui3d.GroupBox(self, [10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*8+6));y+=25
        self.colladaRot90 = gui3d.CheckBox(self.colladaOptions, "Rotate 90", False);y+=24
        self.colladaCopyImages = gui3d.CheckBox(self.colladaOptions, "Copy images", False);y+=24
        rigs = []
        self.gameDae = gui3d.RadioButton(self.colladaOptions, rigs, "Default rig", True);y+=24
        self.dazDae = gui3d.RadioButton(self.colladaOptions, rigs, "Poser/DAZ rig");y+=24
        #self.mbDae = gui3d.RadioButton(self.colladaOptions, rigs, "Motionbuilder rig");y+=24
        self.colladaProxy = GuiProxy(self.colladaOptions, y)
        self.colladaOptions.hide()

        # STL options
        y = yy
        self.stlOptions = gui3d.GroupBox(self, [10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+24*3+6));y+=25
        stlOptions = []
        self.stlAscii = gui3d.RadioButton(self.stlOptions, stlOptions,  "Ascii", selected=True);y+=24
        self.stlBinary = gui3d.RadioButton(self.stlOptions, stlOptions, "Binary");y+=24
        self.stlSmooth = gui3d.CheckBox(self.stlOptions, "Subdivide", False);y+=24
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
        
        @self.fileentry.event
        def onFileSelected(filename):
            
            exportPath = mh.getPath('exports')
            if not os.path.exists(exportPath):
                os.makedirs(exportPath)

            if self.wavefrontObj.selected:
                
                if self.exportEyebrows.selected and self.exportDiamonds.selected:
                    filter = None
                elif self.exportEyebrows.selected:
                    filter = lambda fg: not 'joint' in fg.name
                elif self.exportDiamonds.selected:
                    filter = lambda fg: not 'eyebrown' in fg.name
                else:
                    filter = lambda fg: not ('joint' in fg.name or 'eyebrown' in fg.name)
                    
                human = self.app.selectedHuman
                    
                mesh = human.getSubdivisionMesh() if self.exportSmooth.selected else human.getSeedMesh()
                
                mh2obj.exportObj(mesh,
                    os.path.join(exportPath, filename + ".obj"),
                    self.exportGroups.selected,
                    filter)
                proxy = self.objProxy.getName()
                mh2obj_proxy.exportProxyObj(human, os.path.join(exportPath, filename), proxy)
                
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
                    if self.mhxRig.selected:
                        rig = 'mhx'
                    elif self.rigifyRig.selected:
                        rig = 'rigify'
                    elif self.gameRig.selected:
                        rig = 'game'                    
                    options = {
                        'mhxversion':mhxversion,
                        'expressions':self.exportExpressions.selected,
                        'faceshapes':self.exportFaceShapes.selected,
                        'bodyshapes':self.exportBodyShapes.selected,
                        'clothes':self.exportClothes.selected,
                        'cage':self.exportCage.selected,
                        'useRig': rig,
                        'useProxy': self.mhxProxy.getName()
                    }
                # TL 2011.02.08: exportMhx uses the human instead of his meshData
                mh2mhx.exportMhx(self.app.selectedHuman, os.path.join(exportPath, filename + ".mhx"), options)
            elif self.collada.selected:
                if self.gameDae.selected:
                    rig = 'game'
                elif self.dazDae.selected:
                    rig = 'daz'
                #elif self.mbDae.selected:
                #    rig = 'mb'                    
                options = {
                    "useRig": rig,
                    "rotate90" : self.colladaRot90.selected,
                    "copyImages" : self.colladaCopyImages.selected,
                    "proxy" : self.colladaProxy.getName()
                }
                mh2collada.exportCollada(self.app.selectedHuman, os.path.join(exportPath, filename), options)
            elif self.md5.selected:
                mh2md5.exportMd5(self.app.selectedHuman.meshData, os.path.join(exportPath, filename + ".md5mesh"))
            elif self.stl.selected:
                mesh = self.app.selectedHuman.getSubdivisionMesh() if self.exportSmooth.selected else self.app.selectedHuman.meshData
                if self.stlAscii.selected:
                    mh2stl.exportStlAscii(mesh, os.path.join(exportPath, filename + ".stl"))
                else:
                    mh2stl.exportStlBinary(mesh, os.path.join(exportPath, filename + ".stl"))
                    
            self.app.prompt('Info', u'The mesh has been exported to %s.' % os.path.join(mh.getPath(''), u'exports'), 'OK', helpId='exportHelp')

            self.app.switchCategory('Modelling')
            
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

        human = self.app.selectedHuman
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
        self.app.setGlobalCamera();
        camera.eyeZ = 70
        human.setRotation([0.0, 0.0, 0.0])
        self.exportSmooth.setSelected(human.isSubdivided())
        self.stlSmooth.setSelected(human.isSubdivided())

    def onHide(self, event):
        
        gui3d.TaskView.onHide(self, event)
        
        human = self.app.selectedHuman
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

    def __init__(self, parent):
        
        gui3d.Category.__init__(self, parent, 'Files')

        SaveTaskView(self)
        LoadTaskView(self)
        ExportTaskView(self)


