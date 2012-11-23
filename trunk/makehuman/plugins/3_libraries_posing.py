#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
MakeHuman to Collada (MakeHuman eXchange format) exporter. Collada files can be loaded into
Blender by collada_import.py.

TO DO

"""

print 'importing Pose armature plugin'

import os
import numpy as np
import gui3d
import module3d
import mh
import aljabr

import armature
from armature import transformations as tm
import warpmodifier
import humanmodifier

#
#   Pose library
#

class PoseLoadTaskView(gui3d.TaskView):

    def __init__(self, category):

        self.systemPoses = os.path.join('data', 'poses')
        self.userPoses = os.path.join(mh.getPath(''), 'data', 'poses')

        self.human = gui3d.app.selectedHuman
        self.armature = None
        self.modifier = None
        self.dirty = False
        self.modifiers = {}
        
        gui3d.TaskView.__init__(self, category, 'Poses')
        if not os.path.exists(self.userPoses):
            os.makedirs(self.userPoses)
        self.filechooser = self.addView(gui3d.FileChooser([self.systemPoses, self.userPoses], 'bvh', 'png', 'data/clothes/notfound.png'))
        self.update = self.filechooser.sortBox.addView(gui3d.Button('Check for updates'))
        self.mediaSync = None

        @self.filechooser.event
        def onFileSelected(filepath):

            self.loadBvhFile(filepath)
            
            gui3d.app.switchCategory('Modelling')
            
        @self.update.event
        def onClicked(event):
            self.syncMedia()
 
 
    def loadBvhFile(self, filepath): 
    
        if not self.armature:
            self.armature = armature.rigdefs.createRig(self.human, "Rigid", False)
        
        if self.modifier:
            print "Clear", self.modifier
            self.armature.removeModifier()      
            self.modifier = None

        if os.path.basename(filepath) == "clear.bvh":
            self.armature.clear()
            self.armature.update()
            return
    
        self.armature.readBvhFile(filepath)

        folder = os.path.dirname(filepath)
        (fname, ext) = os.path.splitext(os.path.basename(filepath))
        modpath = '%s/${ethnic}-${gender}-${age}-%s.target' % (folder, fname)
        print filepath, modpath
        
        try:
            self.modifier = self.modifiers[filepath]
        except KeyError:
            self.modifier = None
        if not self.modifier:
            #self.modifier = warpmodifier.WarpModifier(modpath, "body", "GenderAgeEthnicModifier2")
            self.modifier = humanmodifier.GenderAgeEthnicModifier2(modpath)
            self.modifiers[filepath] = self.modifier
            
        self.armature.setModifier(self.modifier)      

 
    def onShow(self, event):

        # When the task gets shown, set the focus to the file chooser
        gui3d.TaskView.onShow(self, event)
        gui3d.app.selectedHuman.hide()
        self.filechooser.setFocus()


    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
                
    def onResized(self, event):
        self.filechooser.onResized(event)

                
    def onHumanChanged(self, event):
        if self.armature:
            print "Rebuild", self.armature
            self.armature.rebuild()            

        elif self.modifier:
            print "Remove", self.modifier
            self.modifier.updateValue(0.0)
            self.modifier = None


    def loadHandler(self, human, values):
        pass
        
    def saveHandler(self, human, file):
        pass

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addView(PoseLoadTaskView(category))

    app.addLoadHandler('poses', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass


print("Pose library loaded")
