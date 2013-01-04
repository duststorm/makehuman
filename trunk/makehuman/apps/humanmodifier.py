#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TO DO

"""

__docformat__ = 'restructuredtext'

import algos3d
import gui3d
from string import Template
from operator import mul
import math
import re
import numpy as np
import gui
import log

class DetailAction:

    def __init__(self, human, before, after, postAction=None,update=True):
        self.name = 'Change detail'
        self.human = human
        self.before = before
        self.after = after
        self.postAction = postAction
        self.update=update

    def do(self):
        for (target, value) in self.after.iteritems():
            self.human.setDetail(target, value)
        self.human.applyAllTargets(gui3d.app.progress, update=self.update)
        if self.postAction:
            self.postAction()
        return True

    def undo(self):
        for (target, value) in self.before.iteritems():
            self.human.setDetail(target, value)
        self.human.applyAllTargets()
        if self.postAction:
            self.postAction()
        return True

class ModifierAction:

    def __init__(self, human, modifier, before, after, postAction):
        self.name = 'Change modifier'
        self.human = human
        self.modifier = modifier
        self.before = before
        self.after = after
        self.postAction = postAction

    def do(self):
        self.modifier.setValue(self.human, self.after)
        self.human.applyAllTargets(gui3d.app.progress)
        self.postAction()
        return True

    def undo(self):
        self.modifier.setValue(self.human, self.before)
        self.human.applyAllTargets(gui3d.app.progress)
        self.postAction()
        return True
        
class ModifierSlider(gui.Slider):
    
    def __init__(self, value=0.0, min=0.0, max=1.0, label=None, modifier=None, valueConverter=None,
                 warpResetNeeded=True, image=None):
        super(ModifierSlider, self).__init__(value, min, max, label, valueConverter=valueConverter, image=image)
        self.modifier = modifier
        self.value = None
        self.warpResetNeeded = warpResetNeeded
        
    def onChanging(self, value):
        
        if gui3d.app.settings.get('realtimeUpdates', True):
            human = gui3d.app.selectedHuman
            if self.value is None:
                self.value = self.modifier.getValue(human)
                if human.isSubdivided():
                    if human.isProxied():
                        human.getProxyMesh().setVisibility(1)
                    else:
                        human.getSeedMesh().setVisibility(1)
                    human.getSubdivisionMesh(False).setVisibility(0)
            self.modifier.updateValue(human, value, gui3d.app.settings.get('realtimeNormalUpdates', True))
            human.updateProxyMesh()
            human.warpsNeedReset = self.warpResetNeeded
            
    def onChange(self, value):
        
        human = gui3d.app.selectedHuman
        if self.value != value:
            gui3d.app.do(ModifierAction(human, self.modifier, self.value, value, self.update))
        if human.isSubdivided():
            if human.isProxied():
                human.getProxyMesh().setVisibility(0)
            else:
                human.getSeedMesh().setVisibility(0)
            human.getSubdivisionMesh(False).setVisibility(1)
        self.value = None
        human.warpsNeedReset = self.warpResetNeeded
        
    def update(self):
        
        human = gui3d.app.selectedHuman
        self.setValue(self.modifier.getValue(human))

class Modifier:

    def __init__(self, left, right):
        
        self.left = left
        self.right = right
        self.verts = None
        self.faces = None

    def setValue(self, human, value, update=1):
        
        value = max(-1.0, min(1.0, value))

        left = -value if value < 0.0 else 0.0
        right = value if value > 0.0 else 0.0
        
        human.setDetail(self.left, left)
        human.setDetail(self.right, right)

    def getValue(self, human):
        
        value = human.getDetail(self.left)
        if value:
            return -value
        value = human.getDetail(self.right)
        if value:
            return value
        else:
            return 0.0

    def updateValue(self, human, value, updateNormals=1):
        
        # Collect vertex and face indices if we didn't yet
        if self.verts is None and self.faces is None:
            # Collect verts
            vmask = np.zeros(human.meshData.getVertexCount(), dtype=bool)
            for target in (self.left, self.right):
                t = algos3d.getTarget(human.meshData, target)
                vmask[t.verts] = True
            self.verts = np.argwhere(vmask)[...,0]
            del vmask

            # collect faces
            self.faces = human.meshData.getFacesForVertices(self.verts)

        # Update detail state
        old_detail = [human.getDetail(target) for target in (self.left, self.right)]
        self.setValue(human, value)
        new_detail = [human.getDetail(target) for target in (self.left, self.right)]

        # Apply changes
        for target, old, new in zip((self.left, self.right), old_detail, new_detail):
            if new == old:
                continue
            algos3d.loadTranslationTarget(human.meshData, target, new - old, None, 0, 0)
            
        # Update vertices
        if updateNormals:
            human.meshData.calcNormals(1, 1, self.verts, self.faces)
        human.meshData.update(self.verts, updateNormals)

class GenericModifier:

    def __init__(self, template):
        
        self.template = template
        self.targets = self.expandTemplate([(self.template, [])])
        self.verts = None
        self.faces = None
        
    def setValue(self, human, value):
    
        value = self.clampValue(value)
        factors = self.getFactors(human, value)
        human.warpNeedReset = True
        
        for target in self.targets:
            human.setDetail(target[0], value * reduce(mul, [factors[factor] for factor in target[1]]))
            
    def getValue(self, human):
        
        return sum([human.getDetail(target[0]) for target in self.targets])

    def updateValue(self, human, value, updateNormals=1):
        
        # Collect vertex and face indices if we didn't yet
        if self.verts is None and self.faces is None:
            # Collect verts
            vmask = np.zeros(human.meshData.getVertexCount(), dtype=bool)
            for target in self.targets:
                t = algos3d.getTarget(human.meshData, target[0])
                vmask[t.verts] = True
            self.verts = np.argwhere(vmask)[...,0]
            del vmask

            # collect faces
            self.faces = human.meshData.getFacesForVertices(self.verts)

        # Update detail state
        old_detail = [human.getDetail(target[0]) for target in self.targets]
        self.setValue(human, value)
        new_detail = [human.getDetail(target[0]) for target in self.targets]

        # Apply changes
        for target, old, new in zip(self.targets, old_detail, new_detail):
            if new == old:
                continue
            algos3d.loadTranslationTarget(human.meshData, target[0], new - old, None, 0, 0)
        
        # Update vertices
        if updateNormals:
            human.meshData.calcNormals(1, 1, self.verts, self.faces)
        human.meshData.update(self.verts, updateNormals)
        human.warpNeedReset = True

class SimpleModifier(GenericModifier):

    def __init__(self, template):
        
        GenericModifier.__init__(self, template)
        
    # overrides
    def expandTemplate(self, targets):
        
        targets = [(target[0], target[1] + ['dummy']) for target in targets]
        
        return targets
    
    def getFactors(self, human, value):
        
        factors = {
            'dummy': 1.0
        }
        
        return factors
    
    def clampValue(self, value):
        return max(0.0, min(1.0, value))

class AgeModifier(GenericModifier):

    def __init__(self, template):
        
        GenericModifier.__init__(self, template)
        
    # overrides
    def expandTemplate(self, targets):
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]

        return targets
    
    def getFactors(self, human, value):
        
        factors = {
            'child': human.childVal,
            'young': human.youngVal,
            'old': human.oldVal
        }
        
        return factors
    
    def clampValue(self, value):
        return max(0.0, min(1.0, value))

class GenderModifier(GenericModifier):

    def __init__(self, template):

        GenericModifier.__init__(self, template)
        
    # overrides
    def expandTemplate(self, targets):
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute(gender=value), target[1] + [value]) for target in targets for value in ['female', 'male']]

        return targets
    
    def getFactors(self, human, value):
        
        factors = {
            'female': human.femaleVal,
            'male': human.maleVal
        }
        
        return factors
        
    def clampValue(self, value):
        return max(0.0, min(1.0, value))

class GenderAgeModifier(GenericModifier):

    def __init__(self, template):
        
        GenericModifier.__init__(self, template)
        
    # overrides
    def expandTemplate(self, targets):
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute(gender=value), target[1] + [value]) for target in targets for value in ['female', 'male']]
        targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]

        return targets
    
    def getFactors(self, human, value):
        
        factors = {
            'female': human.femaleVal,
            'male': human.maleVal,
            'child': human.childVal,
            'young': human.youngVal,
            'old': human.oldVal
        }
        
        return factors
        
    def clampValue(self, value):
        return max(0.0, min(1.0, value))
      
class GenderEthnicModifier(GenericModifier):

    def __init__(self, template):
        
        GenericModifier.__init__(self, template)
        
    # overrides
    def expandTemplate(self, targets):
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute(gender=value), target[1] + [value]) for target in targets for value in ['female', 'male']]
        targets = [(Template(target[0]).safe_substitute(ethnic=value), target[1] + [value]) for target in targets for value in ['caucasian', 'african', 'asian']]

        return targets
    
    def getFactors(self, human, value):
        
        ethnics = [val for val in [human.africanVal, human.asianVal] if val > 0.0]
        
        factors = {
            'female': human.femaleVal,
            'male': human.maleVal,
            'african':human.africanVal / len(ethnics) if ethnics else human.africanVal,
            'asian':human.asianVal / len(ethnics) if ethnics else human.asianVal,
            'caucasian':(1.0 - sum(ethnics) / len(ethnics)) if ethnics else 1.0
        }
        
        return factors
        
    def clampValue(self, value):
        return max(0.0, min(1.0, value))
  
class GenderAgeEthnicModifier(GenericModifier):

    def __init__(self, template):
        
        GenericModifier.__init__(self, template)
        
    # overrides
    def expandTemplate(self, targets):
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute(gender=value), target[1] + [value]) for target in targets for value in ['female', 'male']]
        targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]
        targets = [(Template(target[0]).safe_substitute(ethnic=value), target[1] + [value]) for target in targets for value in ['neutral', 'african', 'asian']]

        return targets
    
    def getFactors(self, human, value):
        
        ethnics = [val for val in [human.africanVal, human.asianVal] if val > 0.0]
        
        factors = {
            'female': human.femaleVal,
            'male': human.maleVal,
            'child': human.childVal,
            'young': human.youngVal,
            'old': human.oldVal,
            'african':human.africanVal / len(ethnics) if ethnics else human.africanVal,
            'asian':human.asianVal / len(ethnics) if ethnics else human.asianVal,
            'neutral':(1.0 - sum(ethnics) / len(ethnics)) if ethnics else 1.0
        }
        
        return factors
        
    def clampValue(self, value):
        return max(0.0, min(1.0, value))
        
class GenderAgeEthnicModifier2(GenericModifier):

    def __init__(self, template):
        
        GenericModifier.__init__(self, template)
        
    # overrides
    def expandTemplate(self, targets):
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute(gender=value), target[1] + [value]) for target in targets for value in ['female', 'male']]
        targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]
        targets = [(Template(target[0]).safe_substitute(ethnic=value), target[1] + [value]) for target in targets for value in ['caucasian', 'african', 'asian']]

        return targets
    
    def getFactors(self, human, value):
        
        ethnics = [val for val in [human.africanVal, human.asianVal] if val > 0.0]
        
        factors = {
            'female': human.femaleVal,
            'male': human.maleVal,
            'child': human.childVal,
            'young': human.youngVal,
            'old': human.oldVal,
            'african':human.africanVal / len(ethnics) if ethnics else human.africanVal,
            'asian':human.asianVal / len(ethnics) if ethnics else human.asianVal,
            'caucasian':(1.0 - sum(ethnics) / len(ethnics)) if ethnics else 1.0
        }
        
        return factors
        
    def clampValue(self, value):
        return max(0.0, min(1.0, value))
        
class GenderAgeMuscleWeightModifier(GenericModifier):

    def __init__(self, template):
        
        GenericModifier.__init__(self, template)
        
    # overrides
    def expandTemplate(self, targets):
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute(gender=value), target[1] + [value]) for target in targets for value in ['female', 'male']]
        targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]
        targets = [(Template(target[0]).safe_substitute(tone=value), target[1] + [value or 'averageTone']) for target in targets for value in ['flaccid', '', 'muscle']]
        targets = [(Template(target[0]).safe_substitute(weight=value), target[1] + [value or 'averageWeight']) for target in targets for value in ['light', '', 'heavy']]

        # Cleanup multiple hyphens and remove a possible hyphen before a dot.
        doubleHyphen = re.compile(r'-+')
        hyphenDot = re.compile(r'-\.')
        
        targets = [(re.sub(hyphenDot, '.', re.sub(doubleHyphen, '-', target[0])), target[1]) for target in targets]
        
        #for target in targets:
        #    print target

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
            'averageWeight':1.0 - (human.underweightVal + human.overweightVal)
        }
        
        return factors
        
    def clampValue(self, value):
        return max(0.0, min(1.0, value))
            
class GenderAgeRangeModifier(GenderAgeModifier):
    
    def __init__(self, template, parameterName, parameterRange, always=True):
        
        self.parameterName = parameterName
        self.parameterRange = parameterRange
        self.always = always
        GenderAgeModifier.__init__(self, template)
        
    # overrides
    def expandTemplate(self, targets):
        
        targets = GenderAgeModifier.expandTemplate(self, targets)
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute({self.parameterName:str(value)}), target[1] + [str(value)]) for target in targets for value in self.parameterRange]

        return targets
        
    def getFactors(self, human, value):
        
        factors = GenderAgeModifier.getFactors(self, human, value)
        
        for factor in self.parameterRange:
            factors[str(factor)] = 0.0
        
        if self.always:
            
            # always
            # a   b    c    d
            # 0   1    2    3
            # 0.0 0.33 0.66 1.0
            
            v = value * (len(self.parameterRange) - 1)
            index = int(math.floor(v))
            v = v - index
            factors[str(self.parameterRange[index])] = 1.0 - v
            if index+1 < len(self.parameterRange):
                factors[str(self.parameterRange[index+1])] = v
        else:
            
            # not always
            #     a    b    c    d
            #     0    1    2    3
            # 0.0 0.25 0.50 0.75 1.0
            # 0   1    2    3    4
        
            v = value * len(self.parameterRange)
            index = int(math.floor(v))
            v = v - index
            if index > 0:
                factors[str(self.parameterRange[index - 1])] = 1.0 - v
            if index < len(self.parameterRange):
                factors[str(self.parameterRange[index])] = v
        
        return factors
        
    def clampValue(self, value):
        return max(0.0, min(1.0, value))
        
class GenderAgeAsymmetricModifier(GenderAgeModifier):
    
    def __init__(self, template, parameterName, left, right, always=True):
        
        self.parameterName = parameterName
        self.left = left
        self.right = right
        self.always = always
        GenderAgeModifier.__init__(self, template)
        
    # overrides
    def setValue(self, human, value):
    
        value = self.clampValue(value)
        factors = self.getFactors(human, value)
        
        for target in self.targets:
            human.setDetail(target[0], reduce(mul, [factors[factor] for factor in target[1]]))
            #print target[0], human.getDetail(target[0])
            
    def expandTemplate(self, targets):
        
        targets = GenderAgeModifier.expandTemplate(self, targets)
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute({self.parameterName:value}), target[1] + [value]) for target in targets for value in [self.left, self.right]]

        return targets
        
    def getFactors(self, human, value):
        
        factors = GenderAgeModifier.getFactors(self, human, value)
        
        factors.update({
            self.left: -min(value, 0.0),
            self.right: max(0.0, value)
        })
        
        return factors
    
    def clampValue(self, value):
        return max(-1.0, min(1.0, value))
        
class GenderAgeEthnicAsymmetricModifier(GenderAgeEthnicModifier2):
    
    def __init__(self, template, parameterName, left, right, always=True):
        
        self.parameterName = parameterName
        self.left = left
        self.right = right
        self.always = always
        GenderAgeEthnicModifier2.__init__(self, template)
        
    # overrides
    def setValue(self, human, value):
    
        value = self.clampValue(value)
        factors = self.getFactors(human, value)
        
        for target in self.targets:
            human.setDetail(target[0], reduce(mul, [factors[factor] for factor in target[1]]))
            #print target[0], human.getDetail(target[0])

    @staticmethod
    def parseTarget(target):
        return target[0].split('/')[-1].split('.')[0].split('-')

    def getValue(self, human):
        right = sum([human.getDetail(target[0]) for target in self.targets if self.right in self.parseTarget(target)])
        if right:
            return right
        else:
            return -sum([human.getDetail(target[0]) for target in self.targets if self.left in self.parseTarget(target)])

    def expandTemplate(self, targets):
        
        targets = GenderAgeEthnicModifier2.expandTemplate(self, targets)
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute({self.parameterName:value}), target[1] + [value]) for target in targets for value in [self.left, self.right]]

        return targets
        
    def getFactors(self, human, value):
        
        factors = GenderAgeEthnicModifier2.getFactors(self, human, value)
        
        factors.update({
            self.left: -min(value, 0.0),
            self.right: max(0.0, value)
        })
        
        return factors
    
    def clampValue(self, value):
        return max(-1.0, min(1.0, value))
