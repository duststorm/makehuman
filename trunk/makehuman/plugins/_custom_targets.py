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

class CustomTargetsTaskView(gui3d.TaskView):

    def __init__(self, category, app):
        self.app = app
        gui3d.TaskView.__init__(self, category, 'Custom targets')
        targetsPath = os.path.join(mh.getPath(''), 'custom')
        if not os.path.exists(targetsPath):
            os.makedirs(targetsPath)
        slidersBox = gui3d.GroupBox(self, label = 'Targets', position=[10, 80, 9.0], style=gui3d.GroupBoxStyle._replace(height=320))
        
        for i in os.listdir(targetsPath):
            self.createTargetControls(slidersBox, targetsPath ,i)
        
    def createTargetControls(self, box, targetPath, targetFile):
        # When the slider is dragged and released, an onChange event is fired
        # By default a slider goes from 0.0 to 1.0, and the initial position will be 0.0 unless specified

        # We want the slider to start from the middle
        targetName = os.path.splitext(targetFile)[0]
        slider = gui3d.Slider(box, value=0, label='%s %%.2f' % targetName)
        
        @slider.event
        def onChange(value):
            human = self.app.selectedHuman
            algos3d.loadTranslationTarget(human.meshData, os.path.join(targetPath, targetFile), value - human.getDetail(targetName)) 
            human.setDetail(targetName, value)

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Modelling')
    taskview = CustomTargetsTaskView(category, app)

    print 'Custom targets plugin loaded'


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Custom targets plugin unloaded'


