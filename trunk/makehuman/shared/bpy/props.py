#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------
Blender API mockup: bpy.props

"""

class Property:
    def __init__(self):
        pass
        
        
class StringProperty(Property):
    def __init__(self, default="", options={}):
        pass
        
class BoolProperty(Property):
    def __init__(self, default=False, options={}):
        pass
        
class IntProperty(Property):
    def __init__(self, default=0, options={}):
        pass
        
class FloatProperty(Property):
    def __init__(self, default=0.0, options={}):
        pass
