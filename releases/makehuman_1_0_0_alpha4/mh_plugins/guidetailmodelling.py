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

import events3d, gui3d, algos3d, humanmodifier

class GenitalsAction:
    def __init__(self, human, value, postAction):
      self.name = "Genitals"
      self.human = human
      self.before = self.human.getGenitals()
      self.after = value
      self.postAction = postAction
      
    def do(self):
      self.human.setGenitals(self.after)
      self.human.applyAllTargets(self.human.app.progress)
      self.postAction()
      return True
      
    def undo(self):
      self.human.setGenitals(self.before)
      self.human.applyAllTargets(self.human.app.progress)
      self.postAction()
      return True

class DetailTool(events3d.EventHandler):
  def __init__(self, app, micro, left, right):
    self.app = app
    self.micro = micro
    self.left = left
    self.before = None
    self.right = right
    self.modifier = None
    self.symmetryModifier = None
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
    leftTarget = "%s%s%s.target"%(folder, part, self.left)
    rightTarget = "%s%s%s.target"%(folder, part, self.right)
    
    self.modifier = None
    if not (leftTarget and rightTarget):
      print("No targets available")
      return
      
    self.modifier = humanmodifier.Modifier(human, leftTarget, rightTarget)
    
    # Save the state
    self.before = {}
    self.before[leftTarget] = human.getDetail(leftTarget)
    self.before[rightTarget] = human.getDetail(rightTarget)
    
    # Add symmetry targets if needed
    self.symmetryModifier = None
    if human.symmetryModeEnabled:
      symmetryPart = human.getSymmetryPart(part)
      if symmetryPart:
        if self.left.find("trans-in") != -1 or self.left.find("trans-out") != -1:
          leftSymmetryTarget = "%s%s%s.target"%(folder, symmetryPart, self.right)
          rightSymmetryTarget = "%s%s%s.target"%(folder, symmetryPart, self.left)
        else:
          leftSymmetryTarget = "%s%s%s.target"%(folder, symmetryPart, self.left)
          rightSymmetryTarget = "%s%s%s.target"%(folder, symmetryPart, self.right)
        self.symmetryModifier = humanmodifier.Modifier(human, leftSymmetryTarget, rightSymmetryTarget)
        # Save the state
        self.before[leftSymmetryTarget] = human.getDetail(leftSymmetryTarget)
        self.before[rightSymmetryTarget] = human.getDetail(rightSymmetryTarget)
    
  def onMouseDragged(self, event):
    if not self.modifier:
      print("No modifier available")
    
    # check which vector we need to check
    if abs(event.dx) > abs(event.dy):
      d = event.dx
    else:
      d = -event.dy
    
    if d == 0.0:
      return
      
    value = d / 20.0
    
    self.modifier.setValue(self.modifier.getValue() + value)
    if self.symmetryModifier:
      self.symmetryModifier.setValue(self.modifier.getValue())
    
  def onMouseUp(self, event):
    human = self.app.scene3d.selectedHuman
    
    # Recalculate
    human.applyAllTargets(self.app.progress)
    
    # Build undo item
    after = {}
    
    for target in self.before.iterkeys():
      after[target] = human.getDetail(target)
      
    self.app.did(humanmodifier.Action(human, self.before, after))
      
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
          if human.symmetryModeEnabled:
            sg = human.getSymmetryGroup(g)
            if sg:
              groups.append(sg)
      
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
    
  def getCameraFraming(self):
    """
    This method return a label to identify the main
    camera framing (front, back. side, top) depending
    the camera rotations.
    
    **Parameters:** This method has no parameters.
    """
    #TODO: top and botton view
    rot = self.app.scene3d.selectedHuman.getRotation()
    
    xRot = rot[0] % 360
    yRot = rot[1] % 360
    
    if (315 < yRot <= 360) or (0 <= yRot < 45):
        return "FRONTAL_VIEW"
    if (145 < yRot < 235):
        return "BACK_VIEW"
    if (45 < yRot < 145):
        return "LEFT_VIEW"
    if (235 < yRot < 315):
        return "RIGHT_VIEW"
    
  def onMouseDragged(self, event):
    viewType =  self.getCameraFraming() 
    
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
    human.applyAllTargets(self.app.progress)
    
    # Add undo item
    before = {}
    
    for target, value in self.x.before.iteritems():
      before[target] = value
    for target, value in self.y.before.iteritems():
      before[target] = value
    for target, value in self.z.before.iteritems():
      before[target] = value
      
    after = {}
    
    for target in before.iterkeys():
      after[target] = human.getDetail(target)
      
    self.app.did(humanmodifier.Action(human, before, after))
      
  def onMouseMoved(self, event):
    human = self.app.scene3d.selectedHuman
    
    groups = []
    
    if self.micro:
      groups.append(event.group)
      if human.symmetryModeEnabled:
        sg = human.getSymmetryGroup(event.group)
        if sg:
          groups.append(sg)
    else:
      part = human.getPartNameForGroupName(event.group.name)
      for g in human.mesh.facesGroups:
        if part in g.name:
          groups.append(g)
          if human.symmetryModeEnabled:
            sg = human.getSymmetryGroup(g)
            if sg:
              groups.append(sg)
      
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
    
    self.genitalsSlider = gui3d.Slider(self, self.app.getThemeResource("images", "slider_genitals.png"),
      self.app.getThemeResource("images", "slider.png"), self.app.getThemeResource("images", "slider_focused.png"), position = [10, 60, 9.2], value = 0.0)
    
    @self.genitalsSlider.event
    def onChange(value):
      human = self.app.scene3d.selectedHuman
      self.app.do(GenitalsAction(human, value, self.syncSliders))
      
    self.detailButtonGroup = []
    self.muscleDetailButton = gui3d.RadioButton(self, self.detailButtonGroup,
      texture = self.app.getThemeResource("images", "button_muscle.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_muscle_on.png"), position = [10, 160, 9],
      selected = True)
    self.weightDetailButton = gui3d.RadioButton(self, self.detailButtonGroup,
      texture = self.app.getThemeResource("images", "button_weight.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_weight_on.png"), position = [10, 260, 9])
      
    self.tool = DetailTool(self.app, False, "_flaccid", "_muscle")
      
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
      
    self.translationButton = gui3d.RadioButton(self, self.detailButtonGroup, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_translation.png"),
      selectedTexture = self.app.getThemeResource("images", "button_translation_on.png"),
      position = [630, 340, 9])
    self.scaleButton = gui3d.RadioButton(self, self.detailButtonGroup, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_scale.png"),
      selectedTexture = self.app.getThemeResource("images", "button_scale_on.png"),
      position = [690, 340, 9])
    
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
    
    self.rightSymmetryButton = gui3d.Button(self, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_symmright.png"), position = [630, 400, 9])
    self.leftSymmetryButton = gui3d.Button(self, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_symmleft.png"), position = [690, 400, 9])
    self.symmetryButton = gui3d.ToggleButton(self, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_symmetry.png"),
      selectedTexture = self.app.getThemeResource("images", "button_symmetry_on.png"), position = [750, 400, 9])
    
    @self.rightSymmetryButton.event
    def onClicked(event):
      human = self.app.scene3d.selectedHuman
      human.applySymmetryRight()
      
    @self.leftSymmetryButton.event
    def onClicked(event):
      human = self.app.scene3d.selectedHuman
      human.applySymmetryLeft()
      
    @self.symmetryButton.event
    def onClicked(event):
      gui3d.ToggleButton.onClicked(self.symmetryButton, event)
      human = self.app.scene3d.selectedHuman
      human.symmetryModeEnabled = self.symmetryButton.selected
      self.parent.tasksByName["Micro modelling"].symmetryButton.setSelected(self.symmetryButton.selected)
      
  def onShow(self, event):
    self.app.tool = self.tool
    gui3d.TaskView.onShow(self, event)
    
  def onHide(self, event):
    self.app.tool = None
    gui3d.TaskView.onHide(self, event)
    
  def syncSliders(self):
    human = self.app.scene3d.selectedHuman
    self.genitalsSlider.setValue(human.getGenitals())
    
class MicroModelingTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Micro modelling", category.app.getThemeResource("images", "micro.png"))
    self.tool = None
    
    self.microButtonGroup = []
      
    self.translationButton = gui3d.RadioButton(self, self.microButtonGroup, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_translation.png"),
      selectedTexture = self.app.getThemeResource("images", "button_translation_on.png"),
      position = [630, 340, 9])
    self.scaleButton = gui3d.RadioButton(self, self.microButtonGroup, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_scale.png"),
      selectedTexture = self.app.getThemeResource("images", "button_scale_on.png"),
      position = [690, 340, 9])
      
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
      
    self.rightSymmetryButton = gui3d.Button(self, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_symmright.png"), position = [630, 400, 9])
    self.leftSymmetryButton = gui3d.Button(self, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_symmleft.png"), position = [690, 400, 9])
    self.symmetryButton = gui3d.ToggleButton(self, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_symmetry.png"),
      selectedTexture = self.app.getThemeResource("images", "button_symmetry_on.png"), position = [750, 400, 9])
      
    @self.rightSymmetryButton.event
    def onClicked(event):
      human = self.app.scene3d.selectedHuman
      human.applySymmetryRight()
      
    @self.leftSymmetryButton.event
    def onClicked(event):
      human = self.app.scene3d.selectedHuman
      human.applySymmetryLeft()
      
    @self.symmetryButton.event
    def onClicked(event):
      gui3d.ToggleButton.onClicked(self.symmetryButton, event)
      human = self.app.scene3d.selectedHuman
      human.symmetryModeEnabled = self.symmetryButton.selected
      self.parent.tasksByName["Detail modelling"].symmetryButton.setSelected(self.symmetryButton.selected)
      
  def onShow(self, event):
    self.app.tool = self.tool
    gui3d.TaskView.onShow(self, event)
    
  def onHide(self, event):
    self.app.tool = None
    gui3d.TaskView.onHide(self, event)
