#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Classes for widgets (GUI utilities).

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module contains classes defined to implement widgets that provide utility functions
to the graphical user interface.

To know more about the interpolation methods used, see the following references:
  http://local.wasp.uwa.edu.au/~pbourke/miscellaneous/interpolation/
  http://en.wikipedia.org/wiki/Cubic_Hermite_spline
  http://en.wikipedia.org/wiki/Kochanek-Bartels_spline
  http://www.geometrictools.com/Documentation/KBSplines.pdf
  http://www.tinaja.com/glib/cubemath.pdf
"""

__docformat__ = 'restructuredtext'

import time
import math

# Good interpolator when you have two values to interpolate between, but doesn't give fluid animation
# when more points are involved since it follows straight lines between the points.


def linearInterpolate(v1, v2, alpha):
    return v1 + alpha * (v2 - v1)


# When you have more than 2 points two interpolate (for example following a path), this is a better
# choice than a linear interpolator.


def cosineInterpolate(v1, v2, alpha):
    alpha2 = (1 - math.cos(alpha * math.pi)) / 2
    return v1 + alpha2 * (v2 - v1)


# Cubic interpolator. Gives better continuity along the spline than the cosine interpolator,
# however needs 4 points to interpolate.


def cubicInterpolate(v0, v1, v2, v3, alpha):
    alpha2 = alpha * alpha
    a0 = (v3 - v2) - v0 + v1
    a1 = (v0 - v1) - a0
    a2 = v2 - v0
    a3 = v1

    return (a0 * alpha) * alpha2 + a1 * alpha2 + a2 * alpha + a3


# Hermite interpolator. Allows better control of the bends in the spline by providing two
# parameters to adjust them:
#   tension: 1 for high tension, 0 for normal tension and -1 for low tension.
#   bias: 1 for bias towards the next segment, 0 for even bias, -1 for bias towards the previous segment.
# Using 0 bias gives a cardinal spline with just tension, using both 0 tension and 0 bias gives a Catmul-Rom spline.


def hermiteInterpolate(v0, v1, v2, v3, alpha, tension, bias):
    alpha2 = alpha * alpha
    alpha3 = alpha2 * alpha
    m0 = (((v1 - v0) * (1 - tension)) * (1 + bias)) / 2.0
    m0 += (((v2 - v1) * (1 - tension)) * (1 - bias)) / 2.0
    m1 = (((v2 - v1) * (1 - tension)) * (1 + bias)) / 2.0
    m1 += (((v3 - v2) * (1 - tension)) * (1 - bias)) / 2.0
    a0 = 2 * alpha3 - 3 * alpha2 + 1
    a1 = alpha3 - 2 * alpha2 + alpha
    a2 = alpha3 - alpha2
    a3 = -2 * alpha3 + 3 * alpha2

    return a0 * v1 + a1 * m0 + a2 * m1 + a3 * v2


# Kochanek-Bartels interpolator. Allows even better control of the bends in the spline by providing three
# parameters to adjust them:
#   tension: 1 for high tension, 0 for normal tension and -1 for low tension.
#   continuity: 1 for inverted corners, 0 for normal corners, -1 for box corners.
#   bias: 1 for bias towards the next segment, 0 for even bias, -1 for bias towards the previous segment.
# Using 0 continuity gives a hermite spline.


def kochanekBartelsInterpolator(v0, v1, v2, v3, alpha, tension, continuity, bias):
    alpha2 = alpha * alpha
    alpha3 = alpha2 * alpha
    m0 = ((((v1 - v0) * (1 - tension)) * (1 + continuity)) * (1 + bias)) / 2.0
    m0 += ((((v2 - v1) * (1 - tension)) * (1 - continuity)) * (1 - bias)) / 2.0
    m1 = ((((v2 - v1) * (1 - tension)) * (1 - continuity)) * (1 + bias)) / 2.0
    m1 += ((((v3 - v2) * (1 - tension)) * (1 + continuity)) * (1 - bias)) / 2.0
    a0 = 2 * alpha3 - 3 * alpha2 + 1
    a1 = alpha3 - 2 * alpha2 + alpha
    a2 = alpha3 - alpha2
    a3 = -2 * alpha3 + 3 * alpha2

    return a0 * v1 + a1 * m0 + a2 * m1 + a3 * v2


# Quadratic Bezier interpolator. v0 and v2 are begin and end point respectively, v1 is a control point.
# | 1   -2    1|
# |-2    2    0|
# | 1    0    0|


def quadraticBezierInterpolator(v0, v1, v2, alpha):
    alpha2 = alpha * alpha

    return (v2 - 2 * v1 + v0) * alpha2 + ((v1 - v0) * 2) * alpha + v0


# Cubic Bezier interpolator. v0 and v3 are begin and end point respectively, v1 and v2 are control points.
# |-1    3   -3    1|
# | 3   -6    3    0|
# |-3    3    0    0|
# | 1    0    0    0|


def cubicBezierInterpolator(v0, v1, v2, v3, alpha):
    alpha2 = alpha * alpha
    alpha3 = alpha2 * alpha

    return ((v3 - 3 * v2 + 3 * v1) - x0) * alpha3 + (3 * v2 - 6 * v1 + 3 * v0) * alpha2 + (3 * v1 - 3 * v0) * alpha + v0


# Quadratic b-spline interpolator. v0 and v2 are begin and end point respectively, v1 is a control point.
# 1   | 1   -2    1|
# - * |-2    2    0|
# 2   | 1    1    0|


def quadraticBSplineInterpolator(v0, v1, v2, alpha):
    alpha2 = alpha * alpha

    return ((v2 - 2 * v1 + v0) * alpha2 + ((v1 - v0) * 2) * alpha + v0 + v1) / 2.0


# Cubic b-spline interpolator. v0 and v3 are begin and end point respectively, v1 and v2 are control points.
#     |-1    3   -3    1|
# 1   | 3   -6    3    0|
# - * |-3    0    3    0|
# 6   | 1    4    1    0|


def cubicBSplineInterpolator(v0, v1, v2, v3, alpha):
    alpha2 = alpha * alpha
    alpha3 = alpha2 * alpha

    return (((v3 - 3 * v2 + 3 * v1) - v0) * alpha3 + (3 * v2 - 6 * v1 + 3 * v0) * alpha2 + (3 * v2 - 3 * v0) * alpha + v0 + 4 * v1 + v2) / 6.0


# Cubic Catmull Rom interpolator. v0 and v3 are begin and end point respectively, v1 and v2 are control points.
#     |-1    3   -3    1|
# 1   | 2   -5    4   -1|
# - * |-1    0    1    0|
# 2   | 1    2    0    0|


def cubicCatmullRomInterpolator(v0, v1, v2, v3, alpha):
    alpha2 = alpha * alpha
    alpha3 = alpha2 * alpha

    return (((v3 - 3 * v2 + 3 * v1) - v0) * alpha3 + ((-v3 + 4 * v2) - 5 * v1 + 2 * v0) * alpha2 + (v2 - v0) * alpha + 2 * v1 + v0) / 2.0


# Cubic hermite interpolator. v0 and v3 are begin and end point respectively, v1 and v2 are control points.
#     | 2    1   -2    1|
# 1   |-3   -2    3   -1|
# - * | 0    1    0    0|
# 6   | 1    0    0    0|


def cubicHermiteInterpolator(v0, v1, v2, v3, alpha):
    alpha2 = alpha * alpha
    alpha3 = alpha2 * alpha

    return (v3 - 2 * v2 + v1 + 2 * v0) * alpha3 + (((-v3 + 3 * v2) - 2 * v1) - 3 * v0) * alpha2 + v1 * alpha + v0


def ThreeDQBspline(v0, v1, v2, alpha):
    return [quadraticBSplineInterpolator(v0[i], v1[i], v2[i], alpha) for i in xrange(len(v1))]


    # return [v1[0] + alpha * (v2[0] - v1[0]), v1[1] + alpha * (v2[1] - v1[1]), v1[2] + alpha * (v2[2] - v1[2])]

# Interpolates a whole vector at once.


def lerpVector(v0, v1, alpha, interpolator=linearInterpolate):
    return [interpolator(v0[i], v1[i], alpha) for i in xrange(len(v1))]


    # return [v1[0] + alpha * (v2[0] - v1[0]), v1[1] + alpha * (v2[1] - v1[1]), v1[2] + alpha * (v2[2] - v1[2])]


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
        if key == len(self.positions) - 1:

            # Use last value

            value = self.positions[-1]
        else:

            # Offset alpha to it's own slice, and expand the slice to 0-1

            sliceLength = 1.0 / keys
            a = (alpha - key * sliceLength) * keys

            # Interpolate between current and next using the new alpha

            value = lerpVector(self.positions[key], self.positions[key + 1], a)
        self.obj.setLoc(value[0], value[1], value[2])


class RotateAction(Action):

    def __init__(self, obj, startAngles, endAngles):
        self.obj = obj
        self.startAngle = startAngles
        self.endAngle = endAngles

    def set(self, alpha):
        value = lerpVector(self.startAngle, self.endAngle, alpha)
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


