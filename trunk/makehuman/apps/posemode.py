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

import gui3d
import armature
import warpmodifier
import humanmodifier

InPoseMode = False

def printVert(human):
    for vn in [8202]:
        x = human.meshData.coord[vn]
        if warpmodifier.ShadowCoords is None:
            y = (0,0,0)
        else:
            y = warpmodifier.ShadowCoords[vn]
        print "  %d: (%.3f %.3f %.3f) (%.3f %.3f %.3f)" % (vn,x[0],x[1],x[2],y[0],y[1],y[2])
        
        
def enterPoseMode(human):
    global InPoseMode
    if InPoseMode:
        return
    print "Enter pose mode"
    printVert(human)
    InPoseMode = True
    warpmodifier.ShadowCoords = human.meshData.coord.copy()
    warpmodifier.clearRefObject()
    human.warpsNeedReset = False
    print "Pose mode entered"
    printVert(human)

    
def exitPoseMode(human):
    global InPoseMode
    if not InPoseMode:
        return
    print "Exit pose mode"
    printVert(human)
    
    amt = human.armature
    if amt:
        amt.clear(update=False)
        
    InPoseMode = False
    if warpmodifier.ShadowCoords == None:
        halt
    human.meshData.changeCoords(warpmodifier.ShadowCoords)
    warpmodifier.ShadowCoords = None
    
    if amt:
        amt.update()     
        amt.removeModifier()
        human.armature = None
        
    print "Pose mode exited"    
    printVert(human)
    
    
def changePoseMode(event):
    human = event.human
    print "Change pose mode %s w=%s e=%s" % (InPoseMode, human.warpsNeedReset, event.change)
    if human:
        if event.change != "targets" or human.warpsNeedReset:
            exitPoseMode(human)
     
     
#----------------------------------------------------------
#   class PoseModifierSlider
#----------------------------------------------------------

class PoseModifierSlider(humanmodifier.ModifierSlider):
    def __init__(self, label, modifier):        
        humanmodifier.ModifierSlider.__init__(self, label=label, modifier=modifier)
        
    def onChanging(self, value):   
        enterPoseMode(gui3d.app.selectedHuman)
        humanmodifier.ModifierSlider.onChanging(self, value)
            
    def onChange(self, value):    
        enterPoseMode(gui3d.app.selectedHuman)
        humanmodifier.ModifierSlider.onChange(self, value)
       