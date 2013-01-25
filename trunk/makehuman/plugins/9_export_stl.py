#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers, Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import gui
from export import Exporter

class ExporterSTL(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "Stereolithography (stl)"
        self.filter = "Stereolithography (*.stl)"

    def build(self, options):
        stlOptions = []
        self.stlAscii = options.addWidget(gui.RadioButton(stlOptions,  "Ascii", selected=True))
        self.stlBinary = options.addWidget(gui.RadioButton(stlOptions, "Binary"))
        self.stlSmooth = options.addWidget(gui.CheckBox("Subdivide", False))

    def export(self, human, filename):
        import mh2stl

        mesh = human.getSubdivisionMesh() if self.stlSmooth.selected else human.meshData

        if self.stlAscii.selected:
            mh2stl.exportStlAscii(mesh, filename("stl"))
        else:
            mh2stl.exportStlBinary(mesh, filename("stl"))

def load(app):
    app.addExporter(ExporterSTL())

def unload(app):
    pass
