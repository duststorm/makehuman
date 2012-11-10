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

"""

import sys
from . import the

def setupCustomRig(): 
    joints = []
    headsTails = []
    armature = []
    props = []
    
    for (path, modname) in the.Config.customrigs:
        print("Custom rig %s %s" % (path, modname))
        if path not in sys.path:
            sys.path.append(path)
            #print(sys.path)
        try:
            sys.modules[modname]
            imported = True
        except:
            imported = False
        if True or not imported:    
            print("Importing module %s" % modname)
            mod = __import__(modname)
            sys.modules[modname] = mod
            print("%s imported" % mod)
        mod = sys.modules[modname]                
        print("Adding %s.Joints" % modname)
        joints += mod.Joints
        print("Adding %s.HeadsTails" % modname)
        headsTails += mod.HeadsTails
        print("Adding %s.Armature" % modname)
        armature += mod.Armature
        print("Adding %s.Properties" % modname)
        props += mod.Properties
        
        
    return (joints, headsTails, armature, props)



