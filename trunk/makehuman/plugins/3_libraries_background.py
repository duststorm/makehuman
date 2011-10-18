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
import mh
import os

class BackgroundTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Background')
        
        self.texture = mh.Texture()
        
        mesh = gui3d.RectangleMesh(420, 420)
        self.backgroundImage = gui3d.Object(self.app.categories['Modelling'], [190, 90, 1], mesh, visible=False)
        self.opacity = 100
        
        modifierStyle = gui3d.ButtonStyle._replace(width=(112-4)/2.0, height=20)
        
        self.backgroundImageToggle = gui3d.ToggleButton(self.app.categories['Modelling'].viewBox, 'Background',
            style=modifierStyle);
            
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
                
        self.filechooser = gui3d.FileChooser(self, os.path.join(mh.getPath(''), 'backgrounds'), ['bmp', 'png', 'tif', 'tiff', 'jpg', 'jpeg'], None)

        @self.filechooser.event
        def onFileSelected(filename):
            print 'Loading %s' % filename
            self.texture.loadImage(os.path.join(mh.getPath(''), 'backgrounds', filename))

            bg = self.backgroundImage
            bg.mesh.setTexture(os.path.join(mh.getPath(''), 'backgrounds', filename))
            bg.mesh.setColor([255, 255, 255, self.opacity])
            if self.texture.width > self.texture.height:
                bg.setScale(1.0, float(self.texture.height) / float(self.texture.width))
            else:
                bg.setScale(float(self.texture.width) / float(self.texture.height), 1.0)
            bg.mesh.setPickable(0)
            bg.show()
            self.backgroundImageToggle.setSelected(True)
            self.app.switchCategory('Modelling')
            self.app.redraw()

    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.app.selectedHuman.hide()
        self.app.prompt('Info', u'Images which are placed in %s will show up here.' % os.path.join(mh.getPath(''), u'backgrounds'),
            'OK', helpId='backgroundHelp')
        self.filechooser.setFocus()

    def onHide(self, event):
        self.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onResized(self, event):
        self.filechooser.onResized(event)

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
    print 'Hair chooser unloaded'
    
    
class settingsTaskView(gui3d.TaskView) :
    
    def __init__(self, category, taskview):
        
        self.backgroundImage = taskview.backgroundImage
        self.texture = taskview.texture
                                
        gui3d.TaskView.__init__(self, category, 'Background')
        
        y = 80
        
        self.lastPos = [0, 0]
        
        self.backgroundBox = gui3d.GroupBox(self, [10, y, 9], 'Background settings', gui3d.GroupBoxStyle._replace(height=25+36*3+24*1+6));y+=25
        
        # sliders
        self.zoomSlider = gui3d.Slider(self.backgroundBox, value=1, min=0.0,max=4, label = "Zoom background")
        self.panXSlider = gui3d.Slider(self.backgroundBox, value=self.backgroundImage.getPosition()[0], min=0.0,max=500, label = "Pan X background")
        self.panYSlider = gui3d.Slider(self.backgroundBox, value=self.backgroundImage.getPosition()[1], min=0.0,max=500, label = "Pan Y background")
        self.OpacitySlider = gui3d.Slider(self.backgroundBox, value=taskview.opacity, min=0,max=255, label = "Opacity")
        
        # toggle button
        modifierStyle = gui3d.ButtonStyle._replace(width=(112-4)/2, height=20)
        self.pickableButton = gui3d.ToggleButton(self.backgroundBox, 'Drag', style=modifierStyle)
        
        @self.zoomSlider.event
        def onChanging(value):
            self.changeZoom(value)
        @self.zoomSlider.event
        def onChange(value):
            self.changeZoom(value)
        
        @self.panXSlider.event
        def onChanging(value):
            self.changePanX(value)
        @self.panXSlider.event
        def onChange(value):
            self.changePanX(value)
        
        @self.panYSlider.event
        def onChanging(value):
            self.changePanY(value)
        @self.panYSlider.event
        def onChange(value):
            self.changePanY(value)
            
        @self.OpacitySlider.event
        def onChanging(value):
            self.backgroundImage.mesh.setColor([255, 255, 255, value])
        @self.OpacitySlider.event
        def onChange(value):
            taskview.opacity = value
            self.backgroundImage.mesh.setColor([255, 255, 255, self.opacity])
            
        @self.backgroundImage.event
        def onMouseDown(event):
            self.lastPos=[event.x, event.y]
        @self.backgroundImage.event
        def onMouseDragged(event):
            self.backgroundImage.setPosition([self.backgroundImage.getPosition()[0]+event.x-self.lastPos[0], self.backgroundImage.getPosition()[1]+event.y-self.lastPos[1], 1.0])
            self.lastPos = [event.x, event.y]            
        
        @self.pickableButton.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.pickableButton, event)
            self.backgroundImage.mesh.setPickable(self.pickableButton.selected)
            
    def changeZoom(self, zoom):
        #self.backgroundImage.mesh.resize(self.backgroundImage.mesh.getSize()[0]*zoom/100 +self.backgroundImage.mesh.getSize()[0], self.backgroundImage.mesh.getSize()[1]*zoom/100 +self.backgroundImage.mesh.getSize()[1])
        #texture = self.backgroundImage.getTexture()
        if self.texture.width > self.texture.height:
            self.backgroundImage.setScale(zoom, float(self.texture.height) / float(self.texture.width)*zoom)
        else:
            self.backgroundImage.setScale(float(self.texture.height) / float(self.texture.width)*zoom, zoom)
        #print self.backgroundImage.mesh.getSize(), ' bbox : ', self.backgroundImage.getBBox()
        self.app.redraw()
            
    def changePanX(self, panX):
        x, y, z = self.backgroundImage.getPosition()
        self.backgroundImage.setPosition([panX, y, z])
        self.app.redraw()
        
    def changePanY(self, panY):
        x, y, z = self.backgroundImage.getPosition()
        self.backgroundImage.setPosition([x, panY, z])
        self.app.redraw()

    def onResized(self, event):
        x, y, z = self.backgroundImage.getPosition()
        scale = (float(event.height) / float(event.height - event.dy))
        print event
        print scale
        print x, y, x * scale, y * scale
        self.backgroundImage.setPosition([x * scale, y * scale, z])