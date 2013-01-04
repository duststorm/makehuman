#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The main MakeHuman Python Application file.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

This is the main MakeHuman Python Application file which participates in the
application startup process. It contains functions that respond to events
affecting the main GUI toolbar along the top of the screen in all modes to
support switching between modes.

When the MakeHuman application is launched the *main* function from the C
application file *main.c* runs. This creates an integration layer by
dynamically generating a Python module (called 'mh'). That *main* function
then either imports this Python *main* module or executes this Python
script *main.py* (depending on platform).

This script displays a splash screen and a progress bar as it loads the
initial 3D humanoid model (the neutral base object) and adds the various
GUI sections into the scene. It creates the main toolbar that enables the
user to switch between different GUI modes and defines functions to
perform that switch for all active buttons. Active buttons are connected
to these functions by being registered to receive events.

At the end of the initiation process the splash screen is hidden and
Modelling mode is activated. The 'startEventLoop' method on the main Scene3D
object is invoked to call the OpenGL/SDL C functions that manage the
low-level event loop.

This Python module responds to high-level GUI toolbar events to switch
between different GUI modes, but otherwise events are handled by GUI mode
specific Python modules.
"""

import sys
#print sys.builtin_module_names
#if 'nt' in sys.builtin_module_names:
sys.path.append("./pythonmodules")
import os

if not 'STARTEDCORRECTLY' in os.environ:
    print "\nERROR ERROR ERROR"
    print "You should not run main.py directly. Please run makehuman.py instead."
    print "ERROR ERROR ERROR\n"
    sys.exit()

def printleaf(object, indent=0):

    print "%s%s %s" % (' ' * indent, object, object._Object__view)

def printtree(view, indent=0):

    print "%s%s %s" % (' ' * indent, type(view), type(view.parent))
    for child in view.children:
        printtree(child, indent+2)
    for object in view.objects:
        printleaf(object, indent+2)

def recursiveDirNames(root):
  pathlist=[]
  #root=os.path.dirname(root)
  for filename in os.listdir(root):
    path=os.path.join(root,filename)
    if not (os.path.isfile(path) or filename=="." or filename==".." or filename==".svn"):
      pathlist.append(path)
      pathlist = pathlist + recursiveDirNames(path) 
  return(pathlist)

syspath = ["./", "./lib", "./apps", "./shared", "./shared/mhx/templates", "./shared/mhx"]
syspath = syspath + recursiveDirNames("./apps")
syspath.append("./core")
syspath = syspath + recursiveDirNames("./core")
syspath.extend(sys.path)
sys.path = syspath

import getpath
userDir = getpath.getPath('')
if not os.path.isdir(userDir):
    os.makedirs(userDir)

import log
log.init()

from mhmain import MHApplication

application = MHApplication()
application.run()

#import cProfile
#cProfile.run('application.run()')
