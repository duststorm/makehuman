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

class Action:

    def __init__(self, human, before, after, postAction=None):
        self.name = 'Change texture'
        self.human = human
        self.before = before
        self.after = after
        self.postAction = postAction

    def do(self):
        self.human.setTexture(self.after)
        if self.postAction:
            self.postAction()
        return True

    def undo(self):
        self.human.setTexture(self.before)
        if self.postAction:
            self.postAction()
        return True

HumanTextureButtonStyle = gui3d.Style(**{
    'width':32,
    'height':32,
    'mesh':None,
    'normal':None,
    'selected':None,
    'focused':None,
    'fontFamily':gui3d.defaultFontFamily,
    'fontSize':gui3d.defaultFontSize,
    'border':None
    })

class HumanTextureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Human texture', label='Skin')
        self.filechooser = gui3d.FileChooser(self, 'data/skins', 'tif', 'png')
        
        self.currentTexture = gui3d.Button(self.app.categories['Modelling'],
            style=HumanTextureButtonStyle._replace(left=800-252, top=600-36, zIndex=9.2, normal=self.app.selectedHuman.getTexture()))

        @self.filechooser.event
        def onFileSelected(filename):
            print 'Loading %s' % filename
            
            self.app.do(Action(self.app.selectedHuman,
                self.app.selectedHuman.getTexture(),
                os.path.join('data/skins', filename), self.syncTexture))
            
            self.app.switchCategory('Modelling')
            
        @self.currentTexture.event
        def onClicked(event):
            self.app.switchCategory('Library')
            self.app.switchTask("Human texture")
            
        self.app.addLoadHandler('skinTexture', self.loadHandler)
        self.app.addSaveHandler(self.saveHandler)
            
    def syncTexture(self):
        
        self.currentTexture.setTexture(self.app.selectedHuman.getTexture().replace('tif', 'png'))

    def onShow(self, event):

        # When the task gets shown, set the focus to the file chooser
        gui3d.TaskView.onShow(self, event)
        self.app.selectedHuman.hide()
        self.filechooser.setFocus()

    def onHide(self, event):
        self.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onResized(self, event):
        self.filechooser.onResized(event)
        self.currentTexture.setPosition([event.width-252, event.height-36, 9.2])
        
    def onHumanChanged(self, event):

        if event.change == 'reset':
            self.syncTexture()
        
    def loadHandler(self, human, values):
        
        if values[0] == 'skinTexture':
            human.setTexture(os.path.join('data/skins', values[1]))
            self.syncTexture()
       
    def saveHandler(self, human, file):
        
        file.write('skinTexture %s\n' % os.path.basename(human.getTexture()))

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = HumanTextureTaskView(category)

    print 'Texture chooser loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Texture chooser unloaded'

