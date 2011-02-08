#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TO DO

"""

__docformat__ = 'restructuredtext'

import algos3d
from string import Template
from operator import mul
import math
import re

class Action:

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
        self.human.applyAllTargets(self.human.app.progress, update=self.update)
        if self.postAction:
            self.postAction()

    def undo(self):
        for (target, value) in self.before.iteritems():
            self.human.setDetail(target, value)
        self.human.applyAllTargets()
        if self.postAction:
            self.postAction()


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
        if not (self.verts or self.faces):
            # Collect verts
            self.verts = []
            for target in (self.left, self.right):
                t = algos3d.getTarget(human.mesh, target)
                self.verts.extend(t.verts)
            self.verts = list(set(self.verts))
            
            # collect faces
            self.faces = []
            for vindex in self.verts:
                self.faces += [face.idx for face in human.mesh.verts[vindex].sharedFaces]
            self.faces = list(set(self.faces))
        
        # Remove old targets
        algos3d.loadTranslationTarget(human.meshData, self.left, -human.getDetail(self.left), None, 0, 0)
        algos3d.loadTranslationTarget(human.meshData, self.right, -human.getDetail(self.right), None, 0, 0)
        
        # Update detail state
        self.setValue(human, value)
        
        # Add new targets
        algos3d.loadTranslationTarget(human.meshData, self.left, human.getDetail(self.left), None, 0, 0)
        algos3d.loadTranslationTarget(human.meshData, self.right, human.getDetail(self.right), None, 0, 0)
            
        # Update vertices
        faces = [human.mesh.faces[i] for i in self.faces]
        vertices = [human.mesh.verts[i] for i in self.verts]
        if updateNormals:
            human.mesh.calcNormals(1, 1, vertices, faces)
        human.mesh.update(vertices)

class GenericModifier:

    def __init__(self, template):
        
        self.template = template
        self.targets = self.expandTemplate([(self.template, [])])
        self.verts = None
        self.faces = None
        
    def setValue(self, human, value):
    
        value = self.clampValue(value)
        factors = self.getFactors(human, value)
        
        for target in self.targets:
            human.setDetail(target[0], value * reduce(mul, [factors[factor] for factor in target[1]]))
            
    def getValue(self, human):
        
        return sum([human.getDetail(target[0]) for target in self.targets])
        
    def updateValue(self, human, value, updateNormals=1):
        
        # Collect vertex and face indices if we didn't yet
        if not (self.verts or self.faces):
            # Collect verts
            self.verts = []
            for target in self.targets:
                t = algos3d.getTarget(human.mesh, target[0])
                self.verts.extend(t.verts)
            self.verts = list(set(self.verts))
            
            # collect faces
            self.faces = []
            for vindex in self.verts:
                self.faces += [face.idx for face in human.mesh.verts[vindex].sharedFaces]
            self.faces = list(set(self.faces))
        
        # Remove old targets
        for target in self.targets:
            algos3d.loadTranslationTarget(human.meshData, target[0], -human.getDetail(target[0]), None, 0, 0)
        
        # Update detail state
        self.setValue(human, value)
        
        # Add new targets
        for target in self.targets:
            algos3d.loadTranslationTarget(human.meshData, target[0], human.getDetail(target[0]), None, 0, 0)
            
        # Update vertices
        faces = [human.mesh.faces[i] for i in self.faces]
        vertices = [human.mesh.verts[i] for i in self.verts]
        if updateNormals:
            human.mesh.calcNormals(1, 1, vertices, faces)
        human.mesh.update(vertices)

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
        
class GenderAgeMuscleWeightModifier(GenericModifier):

    def __init__(self, template):
        
        GenericModifier.__init__(self, template)
        
    # overrides
    def expandTemplate(self, targets):
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute(gender=value), target[1] + [value]) for target in targets for value in ['female', 'male']]
        targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]
        targets = [(Template(target[0]).safe_substitute(tone=value), target[1] + [value]) for target in targets for value in ['flaccid', 'muscle']]
        targets = [(Template(target[0]).safe_substitute(weight=value), target[1] + [value]) for target in targets for value in ['light', 'heavy']]

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
            'light':human.underweightVal,
            'heavy':human.overweightVal,
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