#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
Redirect to new MHX location

"""

import sys
import os

mhxPath = os.path.realpath('./shared/mhx')
if mhxPath not in sys.path:
    sys.path.append(mhxPath)
    
import mhx_main    

def exportMhx(human, filename, options=None):    
    mhx_main.exportMhx(human, filename, options)


