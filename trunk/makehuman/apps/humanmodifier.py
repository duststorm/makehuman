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
        self.human.applyAllTargets(update=self.update)
        if self.postAction:
            self.postAction()

    def undo(self):
        for (target, value) in self.before.iteritems():
            self.human.setDetail(target, value)
        self.human.applyAllTargets()
        if self.postAction:
            self.postAction()


class Modifier:

    def __init__(self, human, left, right):
        self.human = human
        self.left = left
        self.right = right

    def setValue(self, value,update=1):
        value = max(-1.0, min(1.0, value))

    # print(self.left + " " + str(value))

        if not value:
            if self.human.getDetail(self.left):
                algos3d.loadTranslationTarget(self.human.meshData, self.left, -self.human.getDetail(self.left), None, update, 0)
            self.human.setDetail(self.left, None)
            if self.human.getDetail(self.right):
                algos3d.loadTranslationTarget(self.human.meshData, self.right, -self.human.getDetail(self.right), None, update, 0)
            self.human.setDetail(self.right, None)
        elif value < 0.0:
            algos3d.loadTranslationTarget(self.human.meshData, self.left, -value - self.human.getDetail(self.left), None, update, 0)
            self.human.setDetail(self.left, -value)
            if self.human.getDetail(self.right):
                algos3d.loadTranslationTarget(self.human.meshData, self.right, -self.human.getDetail(self.right), None, update, 0)
            self.human.setDetail(self.right, None)
        else:
            if self.human.getDetail(self.left):
                algos3d.loadTranslationTarget(self.human.meshData, self.left, -self.human.getDetail(self.left), None, update, 0)
            self.human.setDetail(self.left, None)
            algos3d.loadTranslationTarget(self.human.meshData, self.right, value - self.human.getDetail(self.right), None, update, 0)
            self.human.setDetail(self.right, value)

    def getValue(self):
        value = self.human.getDetail(self.left)
        if value:
            return -value
        value = self.human.getDetail(self.right)
        if value:
            return value
        else:
            return 0.0
            
    def __str__(self):
        return "%s: %f\n%s: %f" % (self.left, self.human.getDetail(self.left), self.right, self.human.getDetail(self.right))

class GenericModifier:

    def __init__(self, template):
        
        self.template = template
        self.targets = self.expandTemplate()
        self.verts = None
        self.faces = None
        
    def setValue(self, human, value, update=1):
    
        value = max(0.0, min(1.0, value))
        
        factors = self.getFactors(human)
        
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
    def expandTemplate(self):
        
        # Build target list of (targetname, [factors])
        targets = [(self.template, [])]
        targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]

        return targets
    
    def getFactors(self, human):
        
        factors = {
            'child': human.childVal,
            'young': human.youngVal,
            'old': human.oldVal,
        }
        
        return factors

class GenderAgeModifier(GenericModifier):

    def __init__(self, template):
        
        GenericModifier.__init__(self, template)
        
    # overrides
    def expandTemplate(self):
        
        # Build target list of (targetname, [factors])
        targets = [(self.template, [])]
        targets = [(Template(target[0]).safe_substitute(gender=value), target[1] + [value]) for target in targets for value in ['female', 'male']]
        targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]

        return targets
    
    def getFactors(self, human):
        
        factors = {
            'female': human.femaleVal,
            'male': human.maleVal,
            'child': human.childVal,
            'young': human.youngVal,
            'old': human.oldVal,
        }
        
        return factors
        
    class GenderAgeMuscleWeightModifier(GenericModifier):

        def __init__(self, template):
            
            GenericModifier.__init__(self, template)
            
        # overrides
        def expandTemplate(self):
            
            # Build target list of (targetname, [factors])
            targets = [(self.template, [])]
            targets = [(Template(target[0]).safe_substitute(gender=value), target[1] + [value]) for target in targets for value in ['female', 'male']]
            targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]
            targets = [(Template(target[0]).safe_substitute(tone=value), target[1] + [value or 'averageTone']) for target in targets for value in ['flaccid', '', 'muscle']]
            targets = [(Template(target[0]).safe_substitute(weight=value), target[1] + [value or 'averageWeight']) for target in targets for value in ['light', '', 'heavy']]

            # Cleanup multiple hyphens and remove a possible hyphen before a dot.
            doubleHyphen = compile(r'-+')
            hyphenDot = compile(r'-\.')
            
            targets = [(sub(hyphenDot, '.', sub(doubleHyphen, '-', target[0])), target[1]) for target in targets]

            return targets
        
        def getFactors(self, human):
            
            factors = {
                'female': human.femaleVal,
                'male': human.maleVal,
                'child': human.childVal,
                'young': human.youngVal,
                'old': human.oldVal,
                'flaccid':human.flaccidVal,
                'muscle':human.self.muscleVal,
                'averageTone':1.0 - (human.flaccidVal + human.self.muscleVal),
                'light':human.self.underweightVal,
                'heavy':human.self.overweightVal,
                'averageWeight':1.0 - (human.underweightVal + human.self.overweightVal),
            }
            
            return factors