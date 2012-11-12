#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**     MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:** http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**     MakeHuman Team 2001-2011

**Licensing:**       GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
Read mhuv file

TO DO

"""

import os

def readUvset(filename):
    try:
        fp = open(filename, "r")
    except:
        raise NameError("Cannot open %s" % filename)
        
    
