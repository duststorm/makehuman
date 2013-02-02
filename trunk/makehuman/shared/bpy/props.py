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
    def __init__(self, name="Name", description="", default="", options={}):
        pass
        
class BoolProperty(Property):
    def __init__(self, name="Name", description="", default=False, options={}):
        pass
        
class IntProperty(Property):
    def __init__(self, name="Name", description="", default=0, options={}):
        pass
        
class FloatProperty(Property):
    def __init__(self, name="Name", description="", min=0.0, max=1.0, default=0.0, options={}):
        pass
        
class EnumProperty(Property):
    def __init__(self, name="Name", items=[], description="", default='X', options={}):
        pass
