#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TO DO

"""

__docformat__ = 'restructuredtext'

import gui3d
import events3d
import mh
import os
import aljabr

class BackgroundTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Background')
        
        self.backgroundsFolder = os.path.join(mh.getPath(''), 'backgrounds')
        if not os.path.exists(self.backgroundsFolder):
            os.makedirs(self.backgroundsFolder)
        
        self.texture = mh.Texture()
        
        self.filenames = {}

        mesh = gui3d.RectangleMesh(420, 420)
        self.backgroundImage = self.app.categories['Modelling'].addObject(gui3d.Object([190, 90, 1], mesh, visible=False))
        self.opacity = 100
        mesh.setColor([255, 255, 255, self.opacity])
        mesh.setPickable(0)
        
        self.backgroundImageToggle = gui3d.ToggleButton(self.app.categories['Modelling'].viewBox, 'Background');
        y = 280
        self.backgroundBox = gui3d.GroupBox(self, [10, y, 9], 'Background 2 settings', gui3d.GroupBoxStyle._replace(height=25+36*3+24*1+6));y+=25

        self.radioButtonGroup = []
        self.bgImageFrontRadioButton = gui3d.RadioButton(self.backgroundBox, self.radioButtonGroup, selected=True, label='Front')
        self.bgImageBackRadioButton = gui3d.RadioButton(self.backgroundBox, self.radioButtonGroup, selected=False, label='Back')
        self.bgImageLeftRadioButton = gui3d.RadioButton(self.backgroundBox, self.radioButtonGroup, selected=False, label='Left')
        self.bgImageRightRadioButton = gui3d.RadioButton(self.backgroundBox, self.radioButtonGroup, selected=False, label='Right')
        self.bgImageTopRadioButton = gui3d.RadioButton(self.backgroundBox, self.radioButtonGroup, selected=False, label='Top')
        self.bgImageBottomRadioButton = gui3d.RadioButton(self.backgroundBox, self.radioButtonGroup, selected=False, label='Bottom')
            
        @self.backgroundImageToggle.event
        def onClicked(event):
            if self.backgroundImage.isVisible():
                self.backgroundImage.hide()
                self.backgroundImageToggle.setSelected(False)
            elif self.backgroundImage.hasTexture():
                self.backgroundImage.show()
                self.backgroundImageToggle.setSelected(True)
            else:
                self.app.switchCategory('Library')
                self.app.switchTask('Background')
                
        self.filechooser = gui3d.FileChooser(self, self.backgroundsFolder, ['bmp', 'png', 'tif', 'tiff', 'jpg', 'jpeg'], None)

        @self.filechooser.event
        def onFileSelected(filename):
        
            self.reference = self.app.selectedHuman.getPosition()

            if self.bgImageFrontRadioButton.selected:
                self.filenames['front'] = filename
            elif self.bgImageBackRadioButton.selected:
                self.filenames['back'] = filename
            elif self.bgImageLeftRadioButton.selected:
                self.filenames['left'] = filename
            elif self.bgImageRightRadioButton.selected:
                self.filenames['right'] = filename
            elif self.bgImageTopRadioButton.selected:
                self.filenames['top'] = filename
            elif self.bgImageBottomRadioButton.selected:
                self.filenames['bottom'] = filename

            self.texture.loadImage(os.path.join(self.backgroundsFolder, filename))

            bg = self.backgroundImage
            bg.mesh.setTexture(os.path.join(self.backgroundsFolder, filename))
            
            bg.setPosition([80, 80, 8])
            bg.mesh.resize(self.texture.width, self.texture.height)
            self.backgroundWidth = self.texture.width
            self.backgroundHeight = self.texture.height

            self.fixateBackground()

            bg.show()
            self.backgroundImageToggle.setSelected(True)
            self.app.switchCategory('Modelling')
            self.app.switchTask('Background')
            self.app.redraw()
            
    def fixateBackground(self):
    
        self.reference = self.app.selectedHuman.getPosition()
        _, _, z = self.app.modelCamera.convertToScreen(*self.reference)
        x, y, _ = self.backgroundImage.getPosition()
        self.leftTop = self.app.modelCamera.convertToWorld3D(x, y, z)
        self.rightBottom = self.app.modelCamera.convertToWorld3D(x + self.backgroundWidth, y + self.backgroundHeight, z)
            
    def updateBackground(self):
    
        if self.backgroundImage.hasTexture():
        
            reference = self.app.selectedHuman.getPosition()
            diff = aljabr.vsub(reference, self.reference)
            self.leftTop = aljabr.vadd(self.leftTop, diff)
            self.rightBottom = aljabr.vadd(self.rightBottom, diff)
            
            leftTop = self.app.modelCamera.convertToScreen(*self.leftTop)
            rightBottom = self.app.modelCamera.convertToScreen(*self.rightBottom)
            
            self.backgroundImage.setPosition([leftTop[0], leftTop[1], 8])
            self.backgroundWidth = rightBottom[0]-leftTop[0]
            self.backgroundHeight = rightBottom[1]-leftTop[1]
            self.backgroundImage.mesh.resize(self.backgroundWidth, self.backgroundHeight)
            
            self.reference = reference

    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.app.selectedHuman.hide()
        self.app.prompt('Info', u'Images which are placed in %s will show up here.' % self.backgroundsFolder, 'OK', helpId='backgroundHelp')
        self.filechooser.setFocus()

    def onHide(self, event):
        
        gui3d.TaskView.onHide(self, event)
        self.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onHumanTranslated(self, event):
    
        self.updateBackground()

    def setBackgroundImage(self, side):
        filename = self.filenames.get(side)
        if filename:
            self.backgroundImage.mesh.setTexture(os.path.join(self.backgroundsFolder, filename))
	 
    def onHumanRotated(self, event):
        rot = self.app.selectedHuman.getRotation()
        if rot==[0,0,0]:
            self.setBackgroundImage('front')
        elif rot==[0,180,0]:
            self.setBackgroundImage('back')
        elif rot==[0,-90,0]:
            self.setBackgroundImage('left')
        elif rot==[0,90,0]:
            self.setBackgroundImage('right')
        elif rot==[90,0,0]:
            self.setBackgroundImage('top')
        elif rot==[-90,0,0]:
            self.setBackgroundImage('bottom')
         
        self.updateBackground()
        
    def onCameraChanged(self, event):
    
        self.updateBackground()
        
    def onResized(self, event):
        
        self.filechooser.onResized(event)
        self.updateBackground()

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = BackgroundTaskView(category)
    category = app.getCategory('Modelling')
    taskview = settingsTaskView(category, taskview)

    print 'Background chooser loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Background chooser unloaded'
    
    
class settingsTaskView(gui3d.TaskView) :
    
    def __init__(self, category, taskview):
        
        self.backgroundImage = taskview.backgroundImage
        self.texture = taskview.texture
                                
        gui3d.TaskView.__init__(self, category, 'Background')
        
        y = 80
        
        self.lastPos = [0, 0]
        
        self.backgroundBox = gui3d.GroupBox(self, [10, y, 9], 'Background settings', gui3d.GroupBoxStyle._replace(height=25+36*3+24*1+6));y+=25
        
        # sliders
        self.opacitySlider = gui3d.Slider(self.backgroundBox, value=taskview.opacity, min=0,max=255, label = "Opacity")
        
        # toggle button
        self.dragButton = gui3d.ToggleButton(self.backgroundBox, 'Move & Resize')
            
        @self.opacitySlider.event
        def onChanging(value):
            self.backgroundImage.mesh.setColor([255, 255, 255, value])
        @self.opacitySlider.event
        def onChange(value):
            taskview.opacity = value
            self.backgroundImage.mesh.setColor([255, 255, 255, value])
            
        @self.backgroundImage.event
        def onMouseDragged(event):
        
            if event.button == events3d.SDL_BUTTON_LEFT_MASK:
                x, y, z = self.backgroundImage.getPosition()
                self.backgroundImage.setPosition([x + event.dx, y + event.dy, z])
                taskview.fixateBackground()
            elif event.button == events3d.SDL_BUTTON_RIGHT_MASK:
                if abs(event.dx) > abs(event.dy):
                    taskview.backgroundHeight = taskview.backgroundHeight * (taskview.backgroundWidth + event.dx) / taskview.backgroundWidth
                    taskview.backgroundWidth += event.dx
                else:
                    taskview.backgroundWidth = taskview.backgroundWidth * (taskview.backgroundHeight + event.dy) / taskview.backgroundHeight
                    taskview.backgroundHeight += event.dy
                self.backgroundImage.mesh.resize(taskview.backgroundWidth, taskview.backgroundHeight)
                taskview.fixateBackground()
        
        @self.dragButton.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.dragButton, event)
            self.backgroundImage.mesh.setPickable(self.dragButton.selected)

    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.backgroundImage.mesh.setPickable(self.dragButton.selected)

    def onHide(self, event):
        
        gui3d.TaskView.onHide(self, event)
        self.backgroundImage.mesh.setPickable(0)
