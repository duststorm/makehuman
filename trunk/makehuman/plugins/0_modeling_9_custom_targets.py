#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Plugin to apply custom targets. 

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Eduardo Menezes de Morais

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TODO

"""

__docformat__ = 'restructuredtext'

import gui3d
import mh
import algos3d
import os
import humanmodifier
import qtgui as gui

class FolderButton(gui.RadioButton):

    def __init__(self, group, label, groupBox, selected=False):
        super(FolderButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        self.parentWidget()._parent.hideAllBoxes()
        self.groupBox.show()

class CustomTargetsTaskView(gui3d.TaskView):

    def __init__(self, category, app):
        self.app = app
        gui3d.TaskView.__init__(self, category, 'Custom')
        self.targetsPath = os.path.join(mh.getPath(''), 'custom')
        if not os.path.exists(self.targetsPath):
            os.makedirs(self.targetsPath)
        
        self.msg = self.addWidget(mh.addWidget(mh.Frame.Bottom, gui.TextView('No custom targets found.\nTo add a custom target, place the file in ' + self.targetsPath)))
        
        y = 80
        self.optionsBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Options')))
        rescanButton = self.optionsBox.addWidget(gui.Button("Rescan targets' folder"))

        self.folderBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Folders')))
        
        @rescanButton.mhEvent
        def onClicked(event):
            #TODO: undo any applied change here
            self.searchTargets()
           
        self.folders = [] 
            
        self.searchTargets()
        
    def searchTargets(self):
    
        self.sliders = []
        self.modifiers = {}
        
        for folder in self.folders:
            self.removeWidget(folder)
            mh.removeWidget(mh.Frame.LeftTop, folder)
        for child in self.folderBox.children[:]:
            self.folderBox.removeWidget(child)
            
        self.folders = []
        group = []
        
        for root, dirs, files in os.walk(self.targetsPath):

            groupBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Targets')))
            button = self.folderBox.addWidget(FolderButton(group, os.path.basename(root), groupBox, len(self.folderBox.children) == 0))
            self.folders.append(groupBox)

            for f in files:
                if f.endswith(".target"):
                    self.createTargetControls(groupBox, root, f)
                    
            groupBox.hide()
        
        for folder in self.folders:
            for child in folder.children:
                child.update()
            
        if self.folders:
            self.msg.hide()
            self.folderBox.children[0].setSelected(True)
            # self.folders[0].show()
            if self.folders[0].children:
                self.folders[0].children[0].setFocus()
        else:
            self.msg.show()
        
    def createTargetControls(self, box, targetPath, targetFile):
        # When the slider is dragged and released, an onChange event is fired
        # By default a slider goes from 0.0 to 1.0, and the initial position will be 0.0 unless specified

        # We want the slider to start from the middle
        targetName = os.path.splitext(targetFile)[0]
        
        modifier = humanmodifier.SimpleModifier(os.path.join(targetPath, targetFile))
        self.modifiers[targetName] = modifier
        self.sliders.append(box.addWidget(humanmodifier.ModifierSlider(value=0, label=targetName, modifier=modifier)))
        
    def syncSliders(self):
        
        for slider in self.sliders:
            slider.update()
            
    def hideAllBoxes(self):
    
        for folder in self.folders:
            folder.hide()
        
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        if self.folders:
            if self.folders[0].children:
                self.folders[0].children[0].setFocus()
        self.syncSliders()
        for button in self.folderBox.children:
            if button.selected:
                button.groupBox.show()
            else:
                button.groupBox.hide()

    def loadHandler(self, human, values):
        
        modifier = self.modifiers.get(values[1], None)
        if modifier:
            modifier.setValue(human, float(values[2]))
       
    def saveHandler(self, human, file):
        
        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('custom %s %f\n' % (name, value))

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addTask(CustomTargetsTaskView(category, app))
    
    app.addLoadHandler('custom', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    print 'Custom targets plugin loaded'


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Custom targets plugin unloaded'


