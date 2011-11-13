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
import os
import download
import mh

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
    'parent':gui3d.ViewStyle,
    'width':32,
    'height':32
    })

class HumanTextureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Human texture', label='Skin')
        if not os.path.exists(os.path.join(mh.getPath(''), 'data', 'skins')):
            os.makedirs(os.path.join(mh.getPath(''), 'data', 'skins'))
        self.filechooser = self.addView(gui3d.FileChooser(os.path.join(mh.getPath(''), 'data', 'skins'), 'tif', 'png'))
        self.update = self.filechooser.sortBox.addView(gui3d.Button('Check for updates'))
        self.mediaSync = None
        self.currentTexture = gui3d.app.categories['Modelling'].addView(gui3d.Button(style=HumanTextureButtonStyle._replace(left=800-252, top=600-36, zIndex=9.2, normal=gui3d.app.selectedHuman.getTexture())))

        @self.filechooser.event
        def onFileSelected(filename):
            print 'Loading %s' % filename
            
            gui3d.app.do(Action(gui3d.app.selectedHuman,
                gui3d.app.selectedHuman.getTexture(),
                os.path.join(mh.getPath(''), 'data', 'skins', filename), self.syncTexture))
            
            gui3d.app.switchCategory('Modelling')
            
        @self.currentTexture.event
        def onClicked(event):
            gui3d.app.switchCategory('Library')
            gui3d.app.switchTask("Human texture")
            
        @self.update.event
        def onClicked(event):
            self.syncMedia()
            
        gui3d.app.addLoadHandler('skinTexture', self.loadHandler)
        gui3d.app.addSaveHandler(self.saveHandler)
            
    def syncTexture(self):
        
        self.currentTexture.setTexture(gui3d.app.selectedHuman.getTexture().replace('tif', 'png'))

    def onShow(self, event):

        # When the task gets shown, set the focus to the file chooser
        gui3d.TaskView.onShow(self, event)
        gui3d.app.selectedHuman.hide()
        self.filechooser.setFocus()
        
        if not len([filename for filename in os.listdir(os.path.join(mh.getPath(''), 'data', 'skins')) if filename.lower().endswith('tif')]):    
            gui3d.app.prompt('No skins found', 'You don\'t seem to have any skins, download them from the makehuman media repository?\nNote: this can take some time depending on your connection speed.', 'Yes', 'No', self.syncMedia)

    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onResized(self, event):
        self.filechooser.onResized(event)
        self.currentTexture.setPosition([event.width-252, event.height-36, 9.2])
        
    def onHumanChanging(self, event):

        if event.change == 'reset':
            self.syncTexture()
        
    def loadHandler(self, human, values):
        
        if values[0] == 'skinTexture':
            human.setTexture(os.path.join(os.path.join(mh.getPath(''), 'data', 'skins', values[1])))
            self.syncTexture()
       
    def saveHandler(self, human, file):
        
        file.write('skinTexture %s\n' % os.path.basename(human.getTexture()))
        
    def syncMedia(self):
        
        if self.mediaSync:
            return
        self.mediaSync = download.MediaSync(gui3d.app, os.path.join(mh.getPath(''), 'data', 'skins'), 'http://www.makehuman.org/download/skins/', self.syncMediaFinished)
        self.mediaSync.start()
        
    def syncMediaFinished(self):
        
        self.mediaSync = None
        
# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addView(HumanTextureTaskView(category))

    print 'Texture chooser loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Texture chooser unloaded'

