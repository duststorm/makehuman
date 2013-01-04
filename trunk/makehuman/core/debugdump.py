#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Joel Palmius

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

This module dumps important debug information to a text file in the user's home directory
"""

import sys
import os
import re
import platform
import string
import OpenGL
import numpy
if sys.platform == 'win32':
    import _winreg

class DebugDump:

    """
    A class that dumps relevant information to a text file in the user's home directory
    """
    def __init__(this):
        this.home = os.path.expanduser('~')
        this.debugpath = this.home
        if sys.platform == 'win32':
            this.debugpath = os.path.join(os.environ['MYDOCUMENTS'],'makehuman')

        if sys.platform == 'linux2':
            this.debugpath = os.path.join(this.debugpath,"makehuman")
        
        if sys.platform.startswith("darwin"):
            this.debugpath = os.path.join(this.debugpath,"Documents")
            this.debugpath = os.path.join(this.debugpath,"MakeHuman")

        if not os.path.exists(this.debugpath):
            os.makedirs(this.debugpath)
            
        this.debugpath = os.path.join(this.debugpath, "makehuman-debug.txt")

    def reset(this):
        debug = open(this.debugpath, "w")

        debug.write("SVN REVISION: " + os.environ['SVNREVISION'] + " [" + os.environ['SVNREVISION_SOURCE'] + "]\n")
        debug.write("HOME LOCATION: " + this.home + "\n");
        version = re.sub(r"[\r\n]"," ", sys.version)
        debug.write("SYS.VERSION: " + version + "\n")
        debug.write("SYS.PLATFORM: " + sys.platform + "\n");
        debug.write("PLATFORM.MACHINE: " + platform.machine() + "\n");
        debug.write("PLATFORM.PROCESSOR: " + platform.processor() + "\n");
        debug.write("PLATFORM.UNAME.RELEASE: " + platform.uname()[2] + "\n");

        if sys.platform == 'linux2':
            debug.write("PLATFORM.LINUX_DISTRIBUTION: " + string.join(platform.linux_distribution()," ") + "\n");
            
        if sys.platform.startswith("darwin"):
            debug.write("PLATFORM.MAC_VER: " + platform.mac_ver()[0] + "\n");
            
        if sys.platform == 'win32':
            debug.write("PLATFORM.WIN32_VER: " + string.join(platform.win32_ver()," ") + "\n");

        debug.write("PYOPENGL.VERSION: " + OpenGL.__version__ + "\n");
        debug.write("NUMPY.VERSION: " + numpy.__version__ + "\n");
        debug.close()

    def appendMessage(this,message):
        debug = open(this.debugpath, "a")
        debug.write(message + "\n");
        debug.close()

