#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import gui
from export import Exporter

class ExporterFBX(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "Filmbox (fbx)"
        self.filter = "Filmbox (*.fbx)"

    def build(self, options):
        self.fbxEyebrows    = options.addWidget(gui.CheckBox("Eyebrows", True))
        self.fbxLashes      = options.addWidget(gui.CheckBox("Eyelashes", True))
        self.fbxHelpers     = options.addWidget(gui.CheckBox("Helper geometry", False))
        self.fbxHidden      = options.addWidget(gui.CheckBox("Keep hidden faces", True))
        self.fbxExpressions = options.addWidget(gui.CheckBox("Expressions", False))
        self.fbxCustomShapes = options.addWidget(gui.CheckBox("Custom shapes", False))
        self.fbxSkeleton    = options.addWidget(gui.CheckBox("Skeleton", True))
        self.fbxSmooth      = options.addWidget(gui.CheckBox("Subdivide", False))
        self.fbxScales      = self.addScales(options)
        self.fbxRigs        = self.addRigs(options)

    def export(self, human, filename):
        import mh2fbx

        for (button, rig) in self.fbxRigs:
            if button.selected:
                break

        options = {
            "fbxrig":       rig,
            "helpers":      self.fbxHelpers.selected,
            "hidden":       self.fbxHidden.selected,
            "eyebrows":     self.fbxEyebrows.selected,
            "lashes":       self.fbxLashes.selected,
            "expressions":  self.fbxExpressions.selected,
            "customshapes": self.fbxCustomShapes.selected,
            "scale":        self.getScale(self.fbxScales),
            "subdivide":    self.fbxSmooth.selected
        }

        mh2fbx.exportFbx(human, filename("fbx"), options)

def load(app):
    app.addExporter(ExporterFBX())

def unload(app):
    pass
