#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
POV-Ray Export parameters.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Chris Bartlett

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module allows POV-Ray export parameters to be configured. 
These parameters can be changed while the MakeHuman application is running without having
to reload the application.

"""

print 'POV-Ray Export Parameter File'

# The output path defines the standard output directory and the generated include file name.
# The default directory is pov_output, within the MakeHuman installation directory.
# The default include file name is makehuman.inc.

outputpath = 'pov_output/makehuman.inc'

# The export routine can generate a simple mesh2 object that is quick to render, but
# quite inflexible, or it can generate an array based format along with various macros
# that can be used in a wide variety of ways, but which is slower to render.

format = 'mesh2'  # "array" or "mesh2"

# The POV-Ray export function can just export the object or it can also call POV-Ray to
# render a scene file. By default the scene file will be the generated sample scene file.

action = 'export'  # "export" or "render"

# By default the "render" action renders the generated POV scene file, but you can
# specify a scene file to render instead.

renderscenefile = ''  # Use "" to render the default scene file.

# Configure the type of binarie file. 
# Single Processor Version :  'win32'     (pvengine.exe)
# MultiProcessor Version :    'win32sse2' (pvengine-sse2.exe)
# AMD64 systems :             'win64'     (pvengine64.exe)

bintype = 'win32'

