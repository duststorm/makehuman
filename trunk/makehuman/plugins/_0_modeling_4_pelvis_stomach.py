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

TODO
"""

import events3d
import gui3d
import humanmodifier
from operator import mul
from string import Template
import re
import os

print 'Pelvis/Stomach imported'
   
class AsymmetricDetailModifier(humanmodifier.GenderAgeAsymmetricModifier):
    
    def __init__(self, template, parameterName, left, right, always=True):
    
        humanmodifier.GenderAgeAsymmetricModifier.__init__(self, template, parameterName, left, right, always)
        
    def getValue(self, human):
        
        return getattr(human, self.parameterName)
        
    def setValue(self, human, value):
        
        setattr(human, self.parameterName, value)
        humanmodifier.GenderAgeAsymmetricModifier.setValue(self, human, value)

class StomachModifier(AsymmetricDetailModifier):
    # This needs a custom modifier because tone and weight also need to be included
    
    def __init__(self):
    
        AsymmetricDetailModifier.__init__(self, 'data/targets/details/${gender}-${age}-${tone}-${weight}-stomach${stomach}.target', 'stomach', '1', '2', False)
        
    def expandTemplate(self, targets):
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute(gender=value), target[1] + [value]) for target in targets for value in ['female', 'male']]
        targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]
        targets = [(Template(target[0]).safe_substitute(tone=value), target[1] + [value or 'averageTone']) for target in targets for value in ['flaccid', '', 'muscle']]
        targets = [(Template(target[0]).safe_substitute(weight=value), target[1] + [value or 'averageWeight']) for target in targets for value in ['light', '', 'heavy']]
        targets = [(Template(target[0]).safe_substitute({self.parameterName:value}), target[1] + [value]) for target in targets for value in [self.left, self.right]]

        # Cleanup multiple hyphens and remove a possible hyphen before a dot.
        doubleHyphen = re.compile(r'-+')
        hyphenDot = re.compile(r'-\.')
        
        targets = [(re.sub(hyphenDot, '.', re.sub(doubleHyphen, '-', target[0])), target[1]) for target in targets]
        
        return targets
        
    def getFactors(self, human, value):
        
        factors = {
            'female': human.femaleVal,
            'male': human.maleVal,
            'child': human.childVal,
            'young': human.youngVal,
            'old': human.oldVal,
            'flaccid':human.flaccidVal,
            'muscle':human.muscleVal,
            'averageTone':1.0 - (human.flaccidVal + human.muscleVal),
            'light':human.underweightVal,
            'heavy':human.overweightVal,
            'averageWeight':1.0 - (human.underweightVal + human.overweightVal),
            self.left: -min(value, 0.0),
            self.right: max(0.0, value)
        }
        
        return factors

class DetailSlider(humanmodifier.ModifierSlider):
    
    def __init__(self, value, min, max, label, modifier):
        
        humanmodifier.ModifierSlider.__init__(self, value, min, max, label, modifier=modifier)

class PelvisStomachTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Pelvis/Stomach', label='Pelvis & Stomach')
        self.tool = None
        
        self.modifiers = {}
        
        self.modifiers['pelvisTone'] = AsymmetricDetailModifier('data/targets/details/${gender}-${age}-pelvis-tone${pelvisTone}.target', 'pelvisTone', '1', '2', False)
        self.modifiers['buttocks'] = AsymmetricDetailModifier('data/targets/details/${gender}-${age}-nates${buttocks}.target', 'buttocks', '1', '2', False)
        self.modifiers['stomach'] = StomachModifier()
        
        self.sliders = []
        
        self.pelvisBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Pelvis')))
        
        self.sliders.append(self.pelvisBox.addWidget(DetailSlider(0.0, -1.0, 1.0, "Pelvis tone", self.modifiers['pelvisTone'])))
        self.sliders.append(self.pelvisBox.addWidget(DetailSlider(0.0, -1.0, 1.0, "Stomach", self.modifiers['stomach'])))
        self.sliders.append(self.pelvisBox.addWidget(DetailSlider(0.0, -1.0, 1.0, "Buttocks", self.modifiers['buttocks'])))

    def onShow(self, event):
        self.sliders[0].setFocus()
        self.syncSliders()
        gui3d.TaskView.onShow(self, event)

    def onHide(self, event):
        gui3d.TaskView.onHide(self, event)
        
    def syncSliders(self):

        for slider in self.sliders:
            slider.update()
        
    def onHumanChanged(self, event):

        if self.isVisible():
            self.syncSliders()

def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addView(PelvisStomachTaskView(category))

    print 'Pelvis/Stomach loaded'

def unload(app):
    pass
