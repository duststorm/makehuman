#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2012

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TO DO

"""

import armature
import warpmodifier

InPoseMode = False

theShadowCoords = None

def enterPoseMode(human):
    global InPoseMode, theShadowCoords
    if InPoseMode:
        return
    print "Enter pose mode"
    InPoseMode = True
    theShadowCoords = human.meshData.coord.copy()

    
def exitPoseMode(human):
    global InPoseMode, theShadowCoords
    if not InPoseMode:
        return
    print "Exit pose mode"
    
    amt = human.armature
    if amt:
        amt.clear(update=False)
        
    warpmodifier.resetWarps(human)
    InPoseMode = False
    human.warpsNeedReset = False
    human.posesNeedReset = False
    if theShadowCoords == None:
        halt
    human.meshData.changeCoords(theShadowCoords)
    human.syncShadowCoords()    
    theShadowCoords = None
    
    if amt:
        amt.update()     
        amt.removeModifier()
        human.armature = None

    
def changePoseMode(event):
    human = event.human
    print "Change pose mode %s w=%s p=%s e=%s" % (InPoseMode, human.warpsNeedReset, human.posesNeedReset, event.change)
    if human:
        if event.change != "targets" or human.warpsNeedReset or human.posesNeedReset:
            exitPoseMode(human)
            