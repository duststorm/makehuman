#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thanasis Papoutsidakis

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Module that runs an external app on a separate thread and then
optianally executes a method.

"""

import threading
import subprocess

class execute(threading.Thread):
    def __init__(self,args,method=None,cwd=None):
        self.args = args
        self.callback = method
        self.dir = cwd
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        subprocess.call(self.args,cwd = self.dir,
                        shell = True if isinstance(self.args,str) else False)
        if self.callback is not None:
            self.callback()
