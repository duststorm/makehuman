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

class FolderButton(gui3d.RadioButton):

    def __init__(self, group, label, groupBox, selected=False):
        gui3d.RadioButton.__init__(self, group, label, selected, style=gui3d.ButtonStyle)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        gui3d.RadioButton.onClicked(self, event)
        self.parent.parent.hideAllBoxes()
        self.groupBox.show()

class CustomTargetsTaskView(gui3d.TaskView):

    def __init__(self, category, app):
        self.app = app
        gui3d.TaskView.__init__(self, category, 'Custom')
        self.targetsPath = os.path.join(mh.getPath(''), 'custom')
        if not os.path.exists(self.targetsPath):
            os.makedirs(self.targetsPath)
        
        self.msg = self.addView(gui3d.TextView(label='No custom targets found.\nTo add a custom target, place the file in ' + self.targetsPath, \
                                            style=gui3d.TextViewStyle._replace(left=10, top=80, width=320)))
        
        y = 80
        self.optionsBox = self.addView(gui3d.GroupBox(label = 'Options', position=[650, 80, 9.0], style=gui3d.GroupBoxStyle._replace(margin=[10,0,0,10])));y += 25
        rescanButton = self.optionsBox.addView(gui3d.Button(label="Rescan targets' folder"));y += 20
        y+=16
        self.folderBox = self.addView(gui3d.GroupBox(label = 'Folders', position=[650, y, 9.0], style=gui3d.GroupBoxStyle._replace(margin=[10,0,0,10])))
        
        @rescanButton.event
        def onClicked(event):
            #TODO: undo any applied change here
            self.searchTargets()
           
        self.folders = [] 
            
        self.searchTargets()
        
    def searchTargets(self):
    
        self.sliders = []
        self.modifiers = {}
        
        for folder in self.folders:
            self.removeView(folder)
        for child in self.folderBox.children[:]:
            self.folderBox.removeView(child)
            
        self.folders = []
        group = []
        
        for root, dirs, files in os.walk(self.targetsPath):

            groupBox = self.addView(gui3d.GroupBox(label = 'Targets', position = [10, 80, 9.0]))
            button = self.folderBox.addView(FolderButton(group, os.path.basename(root), groupBox, self.folderBox.children == 0))
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
            self.folders[0].show()
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
        self.sliders.append(box.addView(humanmodifier.ModifierSlider(value=0, label=targetName, modifier=modifier)))
        
    def syncSliders(self):
        
        for slider in self.sliders:
            slider.update()
            
    def hideAllBoxes(self):
    
        for folder in self.folders:
            folder.hide()
        
    def onResized(self, event):
        
        self.optionsBox.setPosition([event.width - 150, self.optionsBox.getPosition()[1], 9.0])
        
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        if self.folders:
            if self.folders[0].children:
                self.folders[0].children[0].setFocus()
        self.syncSliders()
        
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
    taskview = category.addView(CustomTargetsTaskView(category, app))
    
    app.addLoadHandler('custom', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    print 'Custom targets plugin loaded'


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Custom targets plugin unloaded'


