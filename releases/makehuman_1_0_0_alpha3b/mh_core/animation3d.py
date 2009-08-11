"""
Classes for widgets (GUI utilities).

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module contains classes defined to implement widgets that provide utility functions
to the graphical user interface.

"""

__docformat__ = 'restructuredtext'

import time

def lerp(v1, v2, alpha):
    return v1 + alpha * (v2 - v1)

def lerpVector(v1, v2, alpha):
    return [v1[0] + alpha * (v2[0] - v1[0]), v1[1] + alpha * (v2[1] - v1[1]), v1[2] + alpha * (v2[2] - v1[2])]

class Action:
    def __init__():
        pass

    def set(self, alpha):
        pass

class PathAction(Action):
    def __init__(self, obj, positions):
        self.obj = obj
        self.positions = positions

    def set(self, alpha):
        keys = float(len(self.positions) - 1)
        key = int(alpha * keys)
        if key == (len(self.positions) - 1):
            # Use last value
            value = self.positions[-1]
        else:
            # Offset alpha to it's own slice, and expand the slice to 0-1
            sliceLength = 1.0 / keys
            a = (alpha - key * sliceLength) * keys
            # Interpolate between current and next using the new alpha
            value = lerpVector(self.positions[key], self.positions[key+1], a)
        self.obj.setLoc(value[0], value[1], value[2])

class RotateAction(Action):
    def __init__(self, obj, startAngles, endAngles):
        self.obj = obj
        self.startAngle = startAngles
        self.endAngle = endAngles

    def set(self, alpha):
        value = (lerpVector(self.startAngle, self.endAngle, alpha))
        self.obj.setRot(value[0], value[1], value[2])

class ScaleAction(Action):
    def __init__(self, obj, startScale, endScale):
        self.obj = obj
        self.startScale = startScale
        self.endScale = endScale

    def set(self, alpha):
        value = lerpVector(self.startScale, self.endScale, alpha)
        self.obj.setScale(value[0], value[1], value[2])

class UpdateAction(Action):
    def __init__(self, scene):
        self.scene = scene

    def set(self, alpha):
        self.scene.redraw(0)

class Timeline:
    def __init__(self, seconds):
        self.length = seconds
        self.actions = []

    def append(self, action):
        self.actions.append(action)

    def start(self):
        reference = time.time()
        t = 0
        while t < self.length:
            a = t / self.length
            for action in self.actions:
                action.set(a)
            t = time.time() - reference
        for action in self.actions:
            action.set(1.0)

