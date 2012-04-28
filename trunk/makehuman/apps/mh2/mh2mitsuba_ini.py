#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Mitsuba Export parameters.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Pedro Alcaide, aka povmaniaco

**Copyright(c):**      MakeHuman Team 2001-2012

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

Abstract
--------

This module allows Mitsuba export parameters to be configured. 
These parameters can be changed while the MakeHuman application is running without having
to reload the application.

"""
#
print 'Mitsuba Renderer Parameter File'

import sys
import os
import ctypes

#
MITSUBA_PATH = ''

if sys.platform == 'win32':
    MITSUBA_PATH = "H:/Mitsuba31"   # change for your own installation path
    #dllArray = ['mitsuba','zlib1','boost_python-vc100-mt-1_44', 'boost_system-vc100-mt-1_44', 'boost_filesystem-vc100-mt-1_44']
    
elif sys.platform == 'darwin':
    MITSUBA_PATH= '/home/user/programs/mitsuba'  # need revision
else:
    MITSUBA_PATH="/home/pedro/programas/mitsuba"  #change for your own installation path
       
#
sys.path.append(MITSUBA_PATH)

#for dll in dllArray:
#    try:
#        ctypes.cdll.LoadLibrary(os.path.join(MITSUBA_PATH, dll))
#    except Exception as e:
#        print("ERROR: Failed to load library " + dll + ", " + repr(e))

       
# The output path defines the standard output directory and the generated include file name.
# The default directory is pov_output, within the MakeHuman installation directory.
# The default include file name is makehuman.inc.

outputpath = 'pov_output/'

# 'gui' for use QT4 Mitsuba interface, 'console' for Mitsuba render console or 'xml' for export to .xml file
source = 'gui'

# define action : render or export
action = 'render' 

# Configure the following variable to point to the Mitsuba executable on your system.
# A number of examples for all executables are provided.
# Don't use the backslash character in the path.

mitsuba_import = MITSUBA_PATH + '/mtsimport.exe'  
mitsuba_console = MITSUBA_PATH + '/mitsuba.exe'
mitsuba_gui = MITSUBA_PATH + '/mtsgui.exe'

