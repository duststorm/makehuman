#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

class Globals(object):
    def __init__(self):
        self.app = None
        self.world = []
        self.cameras = []
        self.windowHeight = 600
        self.windowWidth = 800
        self.color_picked = (0, 0, 0)
        self.clearColor = (0.0, 0.0, 0.0, 0.0)
        self.swapBuffers = None

G = Globals()
