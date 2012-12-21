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
import mh
import qtgui as gui

print 'Gender imported'

class RangeDetailModifier(humanmodifier.GenderAgeRangeModifier):
    
    def __init__(self, template, parameterName, parameterRange, always=True):
    
        humanmodifier.GenderAgeRangeModifier.__init__(self, template, parameterName, parameterRange, always)
        
    def getValue(self, human):
        
        return getattr(human, self.parameterName)
        
    def setValue(self, human, value):
        
        setattr(human, self.parameterName, value)
        humanmodifier.GenderAgeRangeModifier.setValue(self, human, value)
        
class AsymmetricDetailModifier(humanmodifier.GenderAgeAsymmetricModifier):
    
    def __init__(self, template, parameterName, left, right, always=True):
    
        humanmodifier.GenderAgeAsymmetricModifier.__init__(self, template, parameterName, left, right, always)
        
    def getValue(self, human):
        
        return getattr(human, self.parameterName)
        
    def setValue(self, human, value):
        
        setattr(human, self.parameterName, value)
        humanmodifier.GenderAgeAsymmetricModifier.setValue(self, human, value)
        
class BreastsModifier(humanmodifier.GenericModifier):
    # This needs a custom modifier because it has two extra dimensions
    
    def __init__(self):
    
        self.breastSizes = ['breastSize%d' % size for size in xrange(1, 3)]
        humanmodifier.GenericModifier.__init__(self,
            'data/targets/breast/female-${age}-${tone}-${weight}-cup${breastSize}-firmness${breastFirmness}.target')
            
    def setValue(self, human, value):
    
        value = self.clampValue(value)
        factors = self.getFactors(human, value)
        
        for target in self.targets:
            human.setDetail(target[0], human.femaleVal * reduce(mul, [factors[factor] for factor in target[1]]))
        
    def expandTemplate(self, targets):
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]
        targets = [(Template(target[0]).safe_substitute(tone=value), target[1] + [value or 'averageTone']) for target in targets for value in ['flaccid', '', 'muscle']]
        targets = [(Template(target[0]).safe_substitute(weight=value), target[1] + [value or 'averageWeight']) for target in targets for value in ['light', '', 'heavy']]
        targets = [(Template(target[0]).safe_substitute(breastFirmness=value), target[1] + ['breastFirmness%d' % value]) for target in targets for value in xrange(0, 2)]
        targets = [(Template(target[0]).safe_substitute(breastSize=value), target[1] + ['breastSize%d' % value]) for target in targets for value in xrange(1, 3)]

        # Cleanup multiple hyphens and remove a possible hyphen before a dot.
        doubleHyphen = re.compile(r'-+')
        hyphenDot = re.compile(r'-\.')
        
        targets = [(re.sub(hyphenDot, '.', re.sub(doubleHyphen, '-', target[0])), target[1]) for target in targets]
        
        return targets
        
    def getFactors(self, human, value):
        
        factors = {
            'child': human.childVal,
            'young': human.youngVal,
            'old': human.oldVal,
            'flaccid':human.flaccidVal,
            'muscle':human.muscleVal,
            'averageTone':1.0 - (human.flaccidVal + human.muscleVal),
            'light':human.underweightVal,
            'heavy':human.overweightVal,
            'averageWeight':1.0 - (human.underweightVal + human.overweightVal),
            'breastFirmness0': 1.0 - human.breastFirmness,
            'breastFirmness1': human.breastFirmness,
            'breastSize1': -min(human.breastSize, 0.0),
            'breastSize2': max(0.0, human.breastSize)
        }
        '''
        for factor in self.breastSizes:
            factors[factor] = 0.0
        
        v = human.breastSize * (len(self.breastSizes) - 1)
        index = int(math.floor(v))
        v = v - index
        factors[self.breastSizes[index]] = 1.0 - v
        if index+1 < len(self.breastSizes):
            factors[self.breastSizes[index+1]] = v
        '''
        return factors

class BreastSizeModifier(BreastsModifier):
    
    def __init__(self):
        
        BreastsModifier.__init__(self)
        
    def getValue(self, human):
        
        return human.breastSize
        
    def setValue(self, human, value):
        
        human.breastSize = value
        BreastsModifier.setValue(self, human, value)
        
    def clampValue(self, value):
        return max(0.0, min(1.0, value))
        
class BreastFirmnessModifier(BreastsModifier):
    
    def __init__(self):
        
        BreastsModifier.__init__(self)
    
    def getValue(self, human):
        
        return human.breastFirmness
        
    def setValue(self, human, value):
        
        human.breastFirmness = value
        BreastsModifier.setValue(self, human, value)
        
    def clampValue(self, value):
        return max(0.0, min(1.0, value))

class DetailSlider(humanmodifier.ModifierSlider):
    
    def __init__(self, value, min, max, label, modifier):
        
        humanmodifier.ModifierSlider.__init__(self, value, min, max, label, modifier=modifier)

class GenderTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Gender', label='Gender')
        self.tool = None
        
        self.modifiers = {}
        
        self.modifiers['genitals'] = AsymmetricDetailModifier('data/targets/details/genitals_${gender}_${genitals}_${age}.target', 'genitals', 'feminine', 'masculine', False)
        
        self.modifiers['breastSize'] = BreastSizeModifier()
        self.modifiers['breastFirmness'] = BreastFirmnessModifier()
        self.modifiers['breastPosition'] = humanmodifier.Modifier('data/targets/breast/breast-down.target',
            'data/targets/breast/breast-up.target')
        self.modifiers['breastDistance'] = humanmodifier.Modifier('data/targets/breast/breast-dist-min.target',
            'data/targets/breast/breast-dist-max.target')
        self.modifiers['breastPoint'] = humanmodifier.Modifier('data/targets/breast/breast-point-min.target',
            'data/targets/breast/breast-point-max.target')
        
        self.sliders = []
        
        genderBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.SliderBox('Gender')))
        
        self.sliders.append(genderBox.addWidget(DetailSlider(0.0, -1.0, 1.0, "Genitalia", self.modifiers['genitals'])))
        self.sliders.append(genderBox.addWidget(DetailSlider(0.0, -1.0, 1.0, "Breast", self.modifiers['breastSize'])))
        self.sliders.append(genderBox.addWidget(DetailSlider(0.5, 0.0, 1.0, "Breast firmness", self.modifiers['breastFirmness'])))
        self.sliders.append(genderBox.addWidget(humanmodifier.ModifierSlider(0.0, -1.0, 1.0, "Breast position", modifier=self.modifiers['breastPosition'])))
        self.sliders.append(genderBox.addWidget(humanmodifier.ModifierSlider(0.0, -1.0, 1.0, "Breast distance", modifier=self.modifiers['breastDistance'])))
        self.sliders.append(genderBox.addWidget(humanmodifier.ModifierSlider(0.0, -1.0, 1.0, "Breast taper", modifier=self.modifiers['breastPoint'])))

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
    taskview = category.addView(GenderTaskView(category))

    print 'Gender loaded'

def unload(app):
    pass


