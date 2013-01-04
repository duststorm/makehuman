#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Mitsuba Export parameters.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Pedro Alcaide, aka povmaniaco

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

This module allows Mitsuba export parameters to be configured. 
These parameters can be changed while the MakeHuman application is running without having
to reload the application.

"""

import log

#
log.message('Mitsuba Renderer Parameter File')
       
# The output path defines the standard output directory and the generated include file name.
# The default directory is mitsuba_output, within the MakeHuman installation directory.

outputpath = 'mitsuba_output/'

# use 'gui' for use QT4 Mitsuba interface, 'console' for Mitsuba render console or 'xml' for export to .xml file

source = 'gui'

# define  light integrator ( direct light, path tracer or photon mapping

lighting = 'dl'

# define sampler used; low discrepance, independent, etc..

sampler = 'low'

# define action : render or export

action = 'render' 

