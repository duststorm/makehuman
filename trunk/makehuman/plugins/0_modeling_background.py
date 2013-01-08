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

TODO

"""

__docformat__ = 'restructuredtext'

import gui3d
import events3d
import mh
import os
from aljabr import vsub, vadd, vdot, mtransform
from math import floor, ceil, pi, sqrt, exp
import projection
import gui
import filechooser as fc
import log

def pointInRect(point, rect):

    if point[0] < rect[0] or point[0] > rect[2] or point[1] < rect[1] or point[1] > rect[3]:
        return False
    else:
        return True

class BackgroundTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Background')

        self.backgroundsFolder = os.path.join(mh.getPath(''), 'backgrounds')
        if not os.path.exists(self.backgroundsFolder):
            os.makedirs(self.backgroundsFolder)

        self.texture = mh.Texture()

        self.filenames = {}

        mesh = gui3d.RectangleMesh(420, 420)
        self.backgroundImage = gui3d.app.categories['Modelling'].addObject(gui3d.Object([190, 90, 1], mesh, visible=False))
        self.opacity = 100
        mesh.setColor([255, 255, 255, self.opacity])
        mesh.setPickable(False)
        log.debug("Enabling shadeless rendering on body")
        mesh.setShadeless(True)
        mesh.setDepthless(True)
        mesh.priority = -90

        self.backgroundImageToggle = gui3d.app.categories['Modelling'].viewBox.addWidget(gui.ToggleButton('Background'), 3);

        @self.backgroundImageToggle.mhEvent
        def onClicked(event):
            if self.backgroundImage.isVisible():
                self.backgroundImage.hide()
                self.backgroundImageToggle.setSelected(False)
            elif self.backgroundImage.hasTexture():
                self.backgroundImage.show()
                self.backgroundImageToggle.setSelected(True)
            else:
                mh.changeTask('Library', 'Background')

        self.filechooser = self.addTopWidget(fc.FileChooser(self.backgroundsFolder, ['bmp', 'png', 'tif', 'tiff', 'jpg', 'jpeg'], None))
        self.addLeftWidget(self.filechooser.sortBox)

        self.backgroundBox = self.addLeftWidget(gui.GroupBox('Background 2 settings'))

        self.radioButtonGroup = []
        self.bgImageFrontRadioButton  = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Front', selected=True))
        self.bgImageBackRadioButton   = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Back'))
        self.bgImageLeftRadioButton   = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Left'))
        self.bgImageRightRadioButton  = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Right'))
        self.bgImageTopRadioButton    = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Top'))
        self.bgImageBottomRadioButton = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Bottom'))

        @self.filechooser.mhEvent
        def onFileSelected(filename):

            self.reference = gui3d.app.selectedHuman.getPosition()

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

            self.texture.loadImage(mh.Image(os.path.join(self.backgroundsFolder, filename)))

            bg = self.backgroundImage
            bg.mesh.setTexture(os.path.join(self.backgroundsFolder, filename))

            bg.setPosition([80, 80, 8])
            bg.mesh.resize(self.texture.width, self.texture.height)
            self.backgroundWidth = self.texture.width
            self.backgroundHeight = self.texture.height
            self.originalWidth = self.texture.width
            self.originalHeight = self.texture.height

            self.fixateBackground()

            bg.show()
            self.backgroundImageToggle.setSelected(True)

            mh.changeTask('Modelling', 'Background')
            gui3d.app.redraw()

            # Switch to orthogonal view
            # gui3d.app.modelCamera.switchToOrtho()

    def fixateBackground(self):

        self.reference = gui3d.app.selectedHuman.getPosition()
        _, _, z = gui3d.app.modelCamera.convertToScreen(*self.reference)
        x, y, _ = self.backgroundImage.getPosition()
        self.leftTop = gui3d.app.modelCamera.convertToWorld3D(x, y, z)
        self.rightBottom = gui3d.app.modelCamera.convertToWorld3D(x + self.backgroundWidth, y + self.backgroundHeight, z)

    def updateBackground(self):

        if self.backgroundImage.hasTexture():

            reference = gui3d.app.selectedHuman.getPosition()
            diff = vsub(reference, self.reference)
            self.leftTop = vadd(self.leftTop, diff)
            self.rightBottom = vadd(self.rightBottom, diff)

            leftTop = gui3d.app.modelCamera.convertToScreen(*self.leftTop)
            rightBottom = gui3d.app.modelCamera.convertToScreen(*self.rightBottom)

            self.backgroundImage.setPosition([leftTop[0], leftTop[1], 8])
            self.backgroundWidth = rightBottom[0]-leftTop[0]
            self.backgroundHeight = rightBottom[1]-leftTop[1]
            self.backgroundImage.mesh.resize(self.backgroundWidth, self.backgroundHeight)

            self.reference = reference
        
    def projectBackground(self):
        if not hasattr(self, "leftTop"):
            gui3d.app.prompt("Warning", "You need to load a background before you can project it.", "OK")
            return

        mesh = gui3d.app.selectedHuman.getSeedMesh()

        self.fixateBackground()

        # for all quads, project vertex to screen
        # if one vertex falls in bg rect, project screen quad into uv quad
        # warp image region into texture
        leftTop = gui3d.app.modelCamera.convertToScreen(*self.leftTop)
        rightBottom = gui3d.app.modelCamera.convertToScreen(*self.rightBottom)

        dstImg = projection.mapImage(mh.Image(self.backgroundImage.getTexture()))

        dstImg.save(os.path.join(mh.getPath(''), 'data', 'skins', 'projection.png'))
        gui3d.app.selectedHuman.setTexture(os.path.join(mh.getPath(''), 'data', 'skins', 'projection.png'))

    def projectLighting(self):
        dstImg = projection.mapLighting()
        #dstImg.resize(128, 128)
        dstImg.save(os.path.join(mh.getPath(''), 'data', 'skins', 'lighting.png'))

        gui3d.app.selectedHuman.setTexture(os.path.join(mh.getPath(''), 'data', 'skins', 'lighting.png'))
        mesh.setShadeless(1) # Remember to reset this when lighting projection is done.
        
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        gui3d.app.selectedHuman.hide()
        gui3d.app.prompt('Info', u'Images which are placed in %s will show up here.' % self.backgroundsFolder, 'OK', helpId='backgroundHelp')
        self.filechooser.setFocus()

    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)

    def onHumanTranslated(self, event):

        self.updateBackground()

    def setBackgroundImage(self, side):
        filename = self.filenames.get(side)
        if filename:
            self.backgroundImage.mesh.setTexture(os.path.join(self.backgroundsFolder, filename))

    def onHumanRotated(self, event):
        rot = gui3d.app.selectedHuman.getRotation()
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
        self.updateBackground()

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addTask(BackgroundTaskView(category))
    category = app.getCategory('Modelling')
    taskview = category.addTask(settingsTaskView(category, taskview))

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass


class settingsTaskView(gui3d.TaskView) :

    def __init__(self, category, taskview):

        self.backgroundImage = taskview.backgroundImage
        self.texture = taskview.texture

        gui3d.TaskView.__init__(self, category, 'Background')

        y = 80

        self.lastPos = [0, 0]

        self.backgroundBox = self.addLeftWidget(gui.GroupBox('Background settings'))

        # sliders
        self.opacitySlider = self.backgroundBox.addWidget(gui.Slider(value=taskview.opacity, min=0,max=255, label = "Opacity: %d"))

        @self.opacitySlider.mhEvent
        def onChanging(value):
            self.backgroundImage.mesh.setColor([255, 255, 255, value])
        @self.opacitySlider.mhEvent
        def onChange(value):
            taskview.opacity = value
            self.backgroundImage.mesh.setColor([255, 255, 255, value])

        @self.backgroundImage.mhEvent
        def onMouseDragged(event):

            if event.button == mh.Buttons.LEFT_MASK:
                x, y, z = self.backgroundImage.getPosition()
                self.backgroundImage.setPosition([x + event.dx, y + event.dy, z])
                taskview.fixateBackground()
            elif event.button == mh.Buttons.RIGHT_MASK:
                if abs(event.dx) > abs(event.dy):
                    taskview.backgroundWidth += event.dx
                    taskview.backgroundHeight = taskview.originalHeight * taskview.backgroundWidth / taskview.originalWidth
                else:
                    taskview.backgroundHeight += event.dy
                    taskview.backgroundWidth = taskview.originalWidth * taskview.backgroundHeight / taskview.originalHeight
                self.backgroundImage.mesh.resize(taskview.backgroundWidth, taskview.backgroundHeight)
                taskview.fixateBackground()

        self.dragButton = self.backgroundBox.addWidget(gui.ToggleButton('Move && Resize'))

        @self.dragButton.mhEvent
        def onClicked(event):
            self.backgroundImage.mesh.setPickable(self.dragButton.selected)

        self.projectBackgroundButton = self.backgroundBox.addWidget(gui.Button('Project background'))

        @self.projectBackgroundButton.mhEvent
        def onClicked(event):
            taskview.projectBackground()

        self.projectLightingButton = self.backgroundBox.addWidget(gui.Button('Project lighting'))

        @self.projectLightingButton.mhEvent
        def onClicked(event):
            taskview.projectLighting()

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        self.backgroundImage.mesh.setPickable(self.dragButton.selected)

    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        self.backgroundImage.mesh.setPickable(0)
