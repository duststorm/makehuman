#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import gui3d, mh, os
import files3d
import export_config
import mh2proxy
import gui
import filechooser as fc
import log

class UvTaskView(gui3d.TaskView):
    
    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'UV')
        uvDir = os.path.join(mh.getPath(''), 'data', 'uvs')
        if not os.path.exists(uvDir):
            os.makedirs(uvDir)
        self.filechooser = self.addTopWidget(fc.FileChooser([uvDir , 'data/uvs'], 'mhuv', 'png', 'data/uvs/notfound.thumb'))
        self.addLeftWidget(self.filechooser.sortBox)

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            
            if os.path.basename(filename) == "clear.mhuv":
                filename = None            
            self.setUv(gui3d.app.selectedHuman, filename)

            mh.changeCategory('Modelling')
        
    def setUv(self, human, filename):

        if filename is None:
            human.uvset = None
        else:
            human.uvset = mh2proxy.CUvSet(filename)
            human.uvset.read(human, filename)

    def onShow(self, event):
        # When the task gets shown, set the focus to the file chooser
        gui3d.app.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)
        self.filechooser.setFocus()

    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onHumanChanging(self, event):
        
        human = event.human
        if event.change == 'reset':
            self.setUv(human, None)
            
    def onHumanChanged(self, event):
        
        human = event.human

    def loadHandler(self, human, values):

        mhuv = values[1]
        if not os.path.exists(os.path.realpath(mhuv)):
            log.notice('UvTaskView.loadHandler: %s does not exist. Skipping.', mhuv)
            return
        self.setUv(human, mhuv)
        
    def saveHandler(self, human, file):

        if human.uvset:
            file.write('uvset %s\n' % human.uvset.filename)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addTask(UvTaskView(category))

    app.addLoadHandler('uvset', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass

