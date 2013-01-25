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

class ExporterMD5(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "MD5"
        self.filter = "MD5 (*.md5)"

    def export(self, human, filename):
        import mh2md5
        mh2md5.exportMd5(human.meshData, filename("md5mesh"))

def load(app):
    app.addExporter(ExporterMD5())

def unload(app):
    pass
