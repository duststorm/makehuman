"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TODO
"""

__docformat__ = 'restructuredtext'

import events3d, gui3d, algos3d

class DetailAction:
  def __init__(self, human, leftTarget, rightTarget, leftBefore, rightBefore, leftAfter, rightAfter):
    self.name = "Change detail"
    self.human = human
    self.leftTarget = leftTarget
    self.rightTarget = rightTarget
    self.leftBefore = leftBefore
    self.rightBefore = rightBefore
    self.leftAfter = leftAfter
    self.rightAfter = rightAfter
    
  def do(self):
    self.human.setDetail(self.leftTarget, self.leftAfter)
    self.human.setDetail(self.rightTarget, self.rightAfter)
    self.human.applyAllTargets()
    
  def undo(self):
    self.human.setDetail(self.leftTarget, self.leftBefore)
    self.human.setDetail(self.rightTarget, self.rightBefore)
    self.human.applyAllTargets()

class DetailTool(events3d.EventHandler):
  def __init__(self, app, micro, left, right):
    self.app = app
    self.micro = micro
    self.left = left
    self.right = right
    self.leftTarget = None
    self.rightTarget = None
    self.selectedGroups = []
    
  def onMouseDown(self, event):
    human = self.app.scene3d.selectedHuman
    
    # Find the target name
    if self.micro:
      folder = "data/targets/microdetails/"
      part = self.app.selectedGroup.name
    else:
      folder = "data/targets/details/"
      part = human.getPartNameForGroupName(self.app.selectedGroup.name)
      
    # Find the targets
    self.leftTarget = "%s%s%s.target"%(folder, part, self.left)
    self.rightTarget = "%s%s%s.target"%(folder, part, self.right)
    
    if self.leftTarget in human.targetsDetailStack:
      self.leftBefore = human.targetsDetailStack[self.leftTarget]
    else:
      self.leftBefore = 0
    if self.rightTarget in human.targetsDetailStack:
      self.rightBefore = human.targetsDetailStack[self.rightTarget]
    else:
      self.rightBefore = 0
    
  def onMouseDragged(self, event):
    human = self.app.scene3d.selectedHuman
    
    if not (self.leftTarget and self.rightTarget):
      print("No targets available")
    
    # check which vector we need to check
    if abs(event.dx) > abs(event.dy):
      d = event.dx
    else:
      d = -event.dy
    
    if d > 0:
      add = self.rightTarget
      remove = self.leftTarget
    elif d < 0:
      add = self.leftTarget
      remove = self.rightTarget
    else:
      return
      
    value = abs(d) / 20.0
    
    # Check whether we need to add or remove from the target
    if remove in human.targetsDetailStack.keys():
      if human.targetsDetailStack[remove] > 0.1:
        prev = human.targetsDetailStack[remove]
        next = max(0.0, human.targetsDetailStack[remove] - value)
        human.targetsDetailStack[remove] = next
      else:
        prev = human.targetsDetailStack[remove]
        next = 0.0
        del human.targetsDetailStack[remove]
      algos3d.loadTranslationTarget(human.meshData, remove, next - prev, None, 1, 0)
    else:
      if add in human.targetsDetailStack.keys():
        prev = human.targetsDetailStack[add]
        next = min(1.0, human.targetsDetailStack[add] + value)
      else:
        prev = 0.0
        next = min(1.0, value)
      human.targetsDetailStack[add] = next
      algos3d.loadTranslationTarget(human.meshData, add, next - prev, None, 1, 0)
    
  def onMouseUp(self, event):
    human = self.app.scene3d.selectedHuman
    
    # Recalculate
    human.applyAllTargets()
    
    # Add undo item
    if self.leftTarget in human.targetsDetailStack:
      leftAfter = human.targetsDetailStack[self.leftTarget]
    else:
      leftAfter = 0
    if self.rightTarget in human.targetsDetailStack:
      rightAfter = human.targetsDetailStack[self.rightTarget]
    else:
      rightAfter = 0
      
    self.app.did(DetailAction(human, self.leftTarget, self.rightTarget,
      self.leftBefore, self.rightBefore,  leftAfter, rightAfter))
      
  def onMouseMoved(self, event):
    human = self.app.scene3d.selectedHuman
    
    groups = []
    
    if self.micro:
      groups.append(event.group)
    else:
      part = human.getPartNameForGroupName(event.group.name)
      for g in human.mesh.facesGroups:
        if part in g.name:
          groups.append(g)
      
    for g in self.selectedGroups:
      if g not in groups:
        for f in g.faces:
          f.color = [[255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255]]
          f.updateColors()
            
    for g in groups:
      if g not in self.selectedGroups:
        for f in g.faces:
          f.color = [[0,255,0, 255], [0,255,0, 255], [0,255,0, 255]]
          f.updateColors()
        
    self.selectedGroups = groups
    self.app.scene3d.redraw()
    
  def onMouseExited(self, event):
    for g in self.selectedGroups:
      for f in g.faces:
        f.color = [[255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255]]
        f.updateColors()
        
    self.selectedGroups = []
    self.app.scene3d.redraw()

class Detail3dAction:
  def __init__(self, human,
      leftTargetX, rightTargetX, leftBeforeX, rightBeforeX, leftAfterX, rightAfterX,
      leftTargetY, rightTargetY, leftBeforeY, rightBeforeY, leftAfterY, rightAfterY,
      leftTargetZ, rightTargetZ, leftBeforeZ, rightBeforeZ, leftAfterZ, rightAfterZ):
    self.name = "Change detail"
    self.human = human
    self.leftTargetX = leftTargetX
    self.rightTargetX = rightTargetX
    self.leftBeforeX = leftBeforeX
    self.rightBeforeX = rightBeforeX
    self.leftAfterX = leftAfterX
    self.rightAfterX = rightAfterX
    self.leftTargetY = leftTargetY
    self.rightTargetY = rightTargetY
    self.leftBeforeY = leftBeforeY
    self.rightBeforeY = rightBeforeY
    self.leftAfterY = leftAfterY
    self.rightAfterY = rightAfterY
    self.leftTargetZ = leftTargetZ
    self.rightTargetZ = rightTargetZ
    self.leftBeforeZ = leftBeforeZ
    self.rightBeforeZ = rightBeforeZ
    self.leftAfterZ = leftAfterZ
    self.rightAfterZ = rightAfterZ
    
  def do(self):
    self.human.setDetail(self.leftTargetX, self.leftAfterX)
    self.human.setDetail(self.rightTargetX, self.rightAfterX)
    self.human.setDetail(self.leftTargetY, self.leftAfterY)
    self.human.setDetail(self.rightTargetY, self.rightAfterY)
    self.human.setDetail(self.leftTargetZ, self.leftAfterZ)
    self.human.setDetail(self.rightTargetZ, self.rightAfterZ)
    self.human.applyAllTargets()
    
  def undo(self):
    self.human.setDetail(self.leftTargetX, self.leftBeforeX)
    self.human.setDetail(self.rightTargetX, self.rightBeforeX)
    self.human.setDetail(self.leftTargetY, self.leftBeforeY)
    self.human.setDetail(self.rightTargetY, self.rightBeforeY)
    self.human.setDetail(self.leftTargetZ, self.leftBeforeZ)
    self.human.setDetail(self.rightTargetZ, self.rightBeforeZ)
    self.human.applyAllTargets()

class Detail3dTool(events3d.EventHandler):
  def __init__(self, app, micro, type):
    self.app = app
    self.micro = micro
    if type == "scale":
      self.x = DetailTool(app, micro, "-scale-horiz-decr", "-scale-horiz-incr")
      self.y = DetailTool(app, micro, "-scale-vert-decr", "-scale-vert-incr")
      self.z = DetailTool(app, micro, "-scale-depth-decr", "-scale-depth-incr")
    elif type == "translation":
      self.x = DetailTool(app, micro, "-trans-in", "-trans-out")
      self.y = DetailTool(app, micro, "-trans-down", "-trans-up")
      self.z = DetailTool(app, micro, "-trans-backward", "-trans-forward")
    self.selectedGroups = []
  
  def onMouseDown(self, event):
    self.x.onMouseDown(event)
    self.y.onMouseDown(event)
    self.z.onMouseDown(event)
    
  def onMouseDragged(self, event):
    viewType =  self.app.scene3d.getCameraFraming() 
    
    if viewType == "FRONTAL_VIEW":
      d = event.dy
      event.dy = 0.0
      self.x.onMouseDragged(event)
      event.dy = d
      d = event.dx
      event.dx = 0.0
      self.y.onMouseDragged(event)
      event.dx = d
    elif viewType == "BACK_VIEW":
      d = event.dy
      event.dy = 0.0
      event.dx = -event.dx
      self.x.onMouseDragged(event)
      event.dy = d
      d = -event.dx
      event.dx = 0.0
      self.y.onMouseDragged(event)
      event.dx = d
    elif viewType == "LEFT_VIEW":
      d = event.dy
      event.dy = 0.0
      self.z.onMouseDragged(event)
      event.dy = d
      d = event.dx
      event.dx = 0.0
      self.y.onMouseDragged(event)
      event.dx = d
    elif viewType == "RIGHT_VIEW":
      d = event.dy
      event.dy = 0.0
      event.dx = -event.dx
      self.z.onMouseDragged(event)
      event.dy = d
      d = -event.dx
      event.dx = 0.0
      self.y.onMouseDragged(event)
      event.dx = d
    
  def onMouseUp(self, event):
    human = self.app.scene3d.selectedHuman
    
    # Recalculate
    human.applyAllTargets()
    
    # Add undo item
    if self.x.leftTarget in human.targetsDetailStack:
      leftAfterX = human.targetsDetailStack[self.x.leftTarget]
    else:
      leftAfterX = 0
    if self.x.rightTarget in human.targetsDetailStack:
      rightAfterX = human.targetsDetailStack[self.x.rightTarget]
    else:
      rightAfterX = 0
      
    if self.y.leftTarget in human.targetsDetailStack:
      leftAfterY = human.targetsDetailStack[self.y.leftTarget]
    else:
      leftAfterY = 0
    if self.y.rightTarget in human.targetsDetailStack:
      rightAfterY = human.targetsDetailStack[self.y.rightTarget]
    else:
      rightAfterY = 0
      
    if self.z.leftTarget in human.targetsDetailStack:
      leftAfterZ = human.targetsDetailStack[self.z.leftTarget]
    else:
      leftAfterZ = 0
    if self.z.rightTarget in human.targetsDetailStack:
      rightAfterZ = human.targetsDetailStack[self.z.rightTarget]
    else:
      rightAfterZ = 0
      
    self.app.did(Detail3dAction(human, self.x.leftTarget, self.x.rightTarget,
      self.x.leftBefore, self.x.rightBefore,  leftAfterX, rightAfterX,
      self.y.leftTarget, self.y.rightTarget,
      self.y.leftBefore, self.y.rightBefore,  leftAfterY, rightAfterY,
      self.z.leftTarget, self.z.rightTarget,
      self.z.leftBefore, self.z.rightBefore,  leftAfterZ, rightAfterZ))
      
  def onMouseMoved(self, event):
    human = self.app.scene3d.selectedHuman
    
    groups = []
    
    if self.micro:
      groups.append(event.group)
    else:
      part = human.getPartNameForGroupName(event.group.name)
      for g in human.mesh.facesGroups:
        if part in g.name:
          groups.append(g)
      
    for g in self.selectedGroups:
      if g not in groups:
        for f in g.faces:
          f.color = [[255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255]]
          f.updateColors()
            
    for g in groups:
      if g not in self.selectedGroups:
        for f in g.faces:
          f.color = [[0,255,0, 255], [0,255,0, 255], [0,255,0, 255]]
          f.updateColors()
        
    self.selectedGroups = groups
    self.app.scene3d.redraw()
    
  def onMouseExited(self, event):    
    for g in self.selectedGroups:
      for f in g.faces:
        f.color = [[255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255]]
        f.updateColors()
        
    self.selectedGroups = []
    self.app.scene3d.redraw()

class DetailModelingTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Detail modelling", category.app.getThemeResource("images", "details.png"))
    self.tool = None
    
    self.detailButtonGroup = []
    self.genderDetailButton = gui3d.RadioButton(self, self.detailButtonGroup,
      texture = self.app.getThemeResource("images", "button_gender.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_gender_on.png"), position = [-0.45, 0.25, 9],
      selected = True)
    self.ageDetailButton = gui3d.RadioButton(self, self.detailButtonGroup,
      texture = self.app.getThemeResource("images", "button_age.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_age_on.png"), position = [-0.45, 0.1, 9])
    self.muscleDetailButton = gui3d.RadioButton(self, self.detailButtonGroup,
      texture = self.app.getThemeResource("images", "button_muscle.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_muscle_on.png"), position = [-0.45,-0.05,9])
    self.weightDetailButton = gui3d.RadioButton(self, self.detailButtonGroup,
      texture = self.app.getThemeResource("images", "button_weight.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_weight_on.png"), position = [-0.45,-0.20,9])
      
    self.tool = DetailTool(self.app, False, "_female", "_male")
      
    @self.genderDetailButton.event
    def onClicked(event):
      self.tool = DetailTool(self.app, False, "_female", "_male")
      self.app.tool = self.tool
      gui3d.RadioButton.onClicked(self.genderDetailButton, event)
      
    @self.ageDetailButton.event
    def onClicked(event):
      self.tool = DetailTool(self.app, False, "_child", "_old")
      self.app.tool = self.tool
      gui3d.RadioButton.onClicked(self.ageDetailButton, event)
      
    @self.muscleDetailButton.event
    def onClicked(event):
      self.tool = DetailTool(self.app, False, "_flaccid", "_muscle")
      self.app.tool = self.tool
      gui3d.RadioButton.onClicked(self.muscleDetailButton, event)
      
    @self.weightDetailButton.event
    def onClicked(event):
      self.tool = DetailTool(self.app, False, "_underweight", "_overweight")
      self.app.tool = self.tool
      gui3d.RadioButton.onClicked(self.weightDetailButton, event)
      
    self.translationButton = gui3d.RadioButton(self, self.detailButtonGroup, mesh = "data/3dobjs/button_transl.obj",
      texture = self.app.getThemeResource("images", "button_translation.png"),
      selectedTexture = self.app.getThemeResource("images", "button_translation_on.png"),
      position = [0.37, 0.12, 9])
    self.scaleButton = gui3d.RadioButton(self, self.detailButtonGroup, mesh = "data/3dobjs/button_scale.obj",
      texture = self.app.getThemeResource("images", "button_scale.png"),
      selectedTexture = self.app.getThemeResource("images", "button_scale_on.png"),
      position = [0.45, 0.12, 9])
    
    @self.translationButton.event
    def onClicked(event):
      self.tool = Detail3dTool(self.app, False, "translation")
      self.app.tool = self.tool
      gui3d.RadioButton.onClicked(self.translationButton, event)
      
    @self.scaleButton.event
    def onClicked(event):
      self.tool = Detail3dTool(self.app, False, "scale")
      self.app.tool = self.tool
      gui3d.RadioButton.onClicked(self.scaleButton, event)
    
    self.rightSymmetryButton = gui3d.Button(self, mesh = "data/3dobjs/button_symmright.obj",
      texture = self.app.getThemeResource("images", "button_symmright.png"), position = [0.37, 0.04, 9])
    self.leftSymmetryButton = gui3d.Button(self, mesh = "data/3dobjs/button_symmleft.obj",
      texture = self.app.getThemeResource("images", "button_symmleft.png"), position = [0.45, 0.04, 9])
      
    @self.rightSymmetryButton.event
    def onClicked(event):
      human = self.app.scene3d.selectedHuman
      human.applySymmetryRight()
      
    @self.leftSymmetryButton.event
    def onClicked(event):
      human = self.app.scene3d.selectedHuman
      human.applySymmetryLeft()
      
  def onShow(self, event):
    self.app.tool = self.tool
    gui3d.TaskView.onShow(self, event)
    
  def onHide(self, event):
    self.app.tool = None
    gui3d.TaskView.onHide(self, event)
    
class MicroModelingTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Micro modelling", category.app.getThemeResource("images", "micro.png"))
    self.tool = None
    
    self.microButtonGroup = []
      
    self.translationButton = gui3d.RadioButton(self, self.microButtonGroup, mesh = "data/3dobjs/button_transl.obj",
      texture = self.app.getThemeResource("images", "button_translation.png"),
      selectedTexture = self.app.getThemeResource("images", "button_translation_on.png"),
      position = [0.37, 0.12, 9], selected = True)
    self.scaleButton = gui3d.RadioButton(self, self.microButtonGroup, mesh = "data/3dobjs/button_scale.obj",
      texture = self.app.getThemeResource("images", "button_scale.png"),
      selectedTexture = self.app.getThemeResource("images", "button_scale_on.png"),
      position = [0.45, 0.12, 9])
      
    self.tool = Detail3dTool(self.app, True, "translation")
      
    @self.translationButton.event
    def onClicked(event):
      self.tool = Detail3dTool(self.app, True, "translation")
      self.app.tool = self.tool
      gui3d.RadioButton.onClicked(self.translationButton, event)
      
    @self.scaleButton.event
    def onClicked(event):
      self.tool = Detail3dTool(self.app, True, "scale")
      self.app.tool = self.tool
      gui3d.RadioButton.onClicked(self.scaleButton, event)
      
    self.rightSymmetryButton = gui3d.Button(self, mesh = "data/3dobjs/button_symmright.obj",
      texture = self.app.getThemeResource("images", "button_symmright.png"), position = [0.37, 0.04, 9])
    self.leftSymmetryButton = gui3d.Button(self, mesh = "data/3dobjs/button_symmleft.obj",
      texture = self.app.getThemeResource("images", "button_symmleft.png"), position = [0.45, 0.04, 9])
      
    @self.rightSymmetryButton.event
    def onClicked(event):
      human = self.app.scene3d.selectedHuman
      human.applySymmetryRight()
      
    @self.leftSymmetryButton.event
    def onClicked(event):
      human = self.app.scene3d.selectedHuman
      human.applySymmetryLeft()
      
  def onShow(self, event):
    self.app.tool = self.tool
    gui3d.TaskView.onShow(self, event)
    
  def onHide(self, event):
    self.app.tool = None
    gui3d.TaskView.onHide(self, event)
