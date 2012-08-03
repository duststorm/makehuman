#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Mitsuba Export parameters.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Pedro Alcaide, aka povmaniaco

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module allows Mitsuba export parameters to be configured. 
These parameters can be changed while the MakeHuman application is running without having
to reload the application.

"""
#
print 'Mitsuba Renderer Parameter File'
       
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

