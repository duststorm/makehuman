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

import gui3d
import armature
import warpmodifier
import humanmodifier
import log

def resetPoseMode():
    global InPoseMode, theShadowBones
    log.message("Reset pose mode")
    InPoseMode = False
    theShadowBones = {}
    if gui3d.app:
        human = gui3d.app.selectedHuman
        if human:
            human.armature = None
    
resetPoseMode()    


def printVert(human):
    for vn in [8202]:
        x = human.meshData.coord[vn]
        if warpmodifier.shadowCoords is None:
            y = (0,0,0)
        else:
            y = warpmodifier.shadowCoords[vn]
        log.debug("  %d: (%.3f %.3f %.3f) (%.3f %.3f %.3f)", vn,x[0],x[1],x[2],y[0],y[1],y[2])
        
        
def enterPoseMode():
    global InPoseMode, theShadowBones
    if InPoseMode:
        return
    log.message("Enter pose mode")
    human = gui3d.app.selectedHuman
    printVert(human)
    InPoseMode = True
    warpmodifier.shadowCoords = human.meshData.coord.copy()
    warpmodifier.clearRefObject()
    human.warpsNeedReset = False
    if False and theShadowBones:
        amt = armature.rigdefs.createRig(human, "Soft1", False)
        human.armature = amt
        amt.restore(theShadowBones)
        amt.update()
    log.message("Pose mode entered")
    #gui3d.app.poseModeBox.selected = True
    printVert(human)

    
def exitPoseMode():
    global InPoseMode, theShadowBones
    if not InPoseMode:
        return
    log.message("Exit pose mode")
    human = gui3d.app.selectedHuman
    printVert(human)
    
    amt = human.armature
    obj = human.meshData
    if amt:
        theShadowBones = amt.store()

    InPoseMode = False
    if warpmodifier.shadowCoords == None:
        halt
    warpmodifier.removeAllWarpTargets(human)        
    obj.changeCoords(warpmodifier.shadowCoords)
    obj.calcNormals()
    obj.update()
    
    if amt:
        amt.update()     
        amt.dirty = True
        #amt.removeModifier()
        human.armature = None    
    warpmodifier.shadowCoords = None    
    log.message("Pose mode exited")
    #gui3d.app.poseModeBox.selected = False
    printVert(human)
    
    
def changePoseMode(event):
    human = event.human
    #log.debug("Change pose mode %s w=%s e=%s", InPoseMode, human.warpsNeedReset, event.change)
    if human and human.warpsNeedReset:
        exitPoseMode()
    elif event.change not in ["targets", "warp"]:
        exitPoseMode()
    if event.change == "reset":
        resetPoseMode()     
     
#----------------------------------------------------------
#   class PoseModifierSlider
#----------------------------------------------------------

class PoseModifierSlider(humanmodifier.ModifierSlider):
    def __init__(self, label, modifier):        
        humanmodifier.ModifierSlider.__init__(self, label=label, modifier=modifier, warpResetNeeded=False)
        
    def onChanging(self, value):   
        enterPoseMode()
        humanmodifier.ModifierSlider.onChanging(self, value)
            
    def onChange(self, value):    
        enterPoseMode()
        humanmodifier.ModifierSlider.onChange(self, value)
       
