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


