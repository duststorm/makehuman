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

TODO
"""

import sys
import os
import mh
from . import the
import log


def listCustomFiles(config):                    
    config.customShapeFiles = []
    if config.customshapes: 
        folder = os.path.join(mh.getPath(''), 'custom')
        readCustomFolder(folder, config)
        
        
def readCustomFolder(folder, config):        
    for file in os.listdir(folder):            
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            readCustomFolder(path, config)
        else:
            (fname, ext) = os.path.splitext(file)
            if ext == ".target":
                path = os.path.join(folder, file)
                name = "Mhc" + fname.capitalize().replace(" ","_").replace("-","_")
                config.customShapeFiles.append((path, name))


def readCustomTarget(path):
    try:
        fp = open(path, "rU")
    except:
        return []
    shape = {}
    for line in fp:
        words = line.split()
        try:
            shape[int(words[0])] = (float(words[1]), float(words[2]), float(words[3]))
        except:
            return {}
    fp.close()
    return shape
        

def setupCustomRig(config): 
    return [],[],[],[]
    
    joints = []
    headsTails = []
    armature = []
    props = []
    
    for (path, modname) in config.customrigs:
        log.message("Custom rig %s %s" % (path, modname))
        if path not in sys.path:
            sys.path.append(path)
            #print(sys.path)
        try:
            sys.modules[modname]
            imported = True
        except:
            imported = False
        if True or not imported:    
            log.message("Importing module %s" % modname)
            mod = __import__(modname)
            sys.modules[modname] = mod
            log.message("%s imported" % mod)
        mod = sys.modules[modname]                
        log.message("Adding %s.Joints" % modname)
        joints += mod.Joints
        log.message("Adding %s.HeadsTails" % modname)
        headsTails += mod.HeadsTails
        log.message("Adding %s.Armature" % modname)
        armature += mod.Armature
        log.message("Adding %s.Properties" % modname)
        props += mod.Properties
        
        
    return (joints, headsTails, armature, props)



