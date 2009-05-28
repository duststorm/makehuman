import gui3d, animation3d

class MacroAction:
    def __init__(self, human, method, value, postAction):
      self.name = method
      self.human = human
      self.method = method
      self.before = getattr(self.human, "get" + self.method)()
      self.after = value
      self.postAction = postAction
      
    def do(self):
      getattr(self.human, "set" + self.method)(self.after)
      self.human.applyAllTargets()
      self.postAction()
      return True
      
    def undo(self):
      getattr(self.human, "set" + self.method)(self.before)
      self.human.applyAllTargets()
      self.postAction()
      return True
      
class EthnicAction:
    def __init__(self, human, ethnic, value, postAction):
      self.name = "Change %s to %d" %(ethnic, value)
      self.human = human
      self.ethnic = ethnic
      self.before = human.getEthnic(ethnic)
      self.after = value
      self.postAction = postAction
      
    def do(self):
      self.human.setEthnic(self.ethnic, self.after)
      self.human.applyAllTargets()
      self.postAction()
      return True
      
    def undo(self):
      self.human.setEthnic(self.ethnic, self.before)
      self.human.applyAllTargets()
      self.postAction()
      return True

class EthnicMapButton(gui3d.RadioButton):
  def __init__(self, group, parent, mesh = "data/3dobjs/button_gender.obj", texture = None,
    selectedTexture = None, position = [0, 0, 9], selected = False):
    gui3d.RadioButton.__init__(self, group, parent, mesh, texture, selectedTexture, position, selected)

  def onSelected(self, selected):
    if selected:
      pos = self.button.getPosition()
      t = animation3d.Timeline(0.250)
      t.append(animation3d.PathAction(self.button.mesh, [pos, [pos[0] - 0.40, pos[1] - 0.15, pos[2]]]))
      t.append(animation3d.ScaleAction(self.button.mesh, [1, 1, 1], [5, 5, 5]))
      t.append(animation3d.UpdateAction(self.app.scene3d))
      t.start()
    else:
      pos = self.button.getPosition()
      t = animation3d.Timeline(0.250)
      t.append(animation3d.PathAction(self.button.mesh, [pos, [pos[0] + 0.40, pos[1] + 0.15, pos[2]]]))
      t.append(animation3d.ScaleAction(self.button.mesh, [5, 5, 5], [1, 1, 1]))
      t.append(animation3d.UpdateAction(self.app.scene3d))
      t.start()
      
  def onMouseDown(self, event):
    human = self.app.scene3d.selectedHuman
    if self.selected:
      faceGroupSel = self.app.scene3d.getSelectedFacesGroup()
      faceGroupName = faceGroupSel.name
      if "dummy" in faceGroupName:
        self.setSelected(False)
      else:
        if self.parent.ethnicIncreaseButton.selected:
          self.app.do(EthnicAction(human, faceGroupName,
            human.getEthnic(faceGroupName) + 0.1, self.syncEthnics))
        elif self.parent.ethnicDecreaseButton.selected:
          self.app.do(EthnicAction(human, faceGroupName,
            human.getEthnic(faceGroupName) - 0.1, self.syncEthnics))
        else:
          self.app.do(EthnicAction(human, faceGroupName,
            0.0, self.syncEthnics))
    else:
      self.setSelected(True)

  def onBlur(self, event):
    pass
    #self.setSelected(False)
      
  def onMouseUp(self, event):
    pass

  def syncEthnics(self):
    human = self.app.scene3d.selectedHuman
    ethnics = human.targetsEthnicStack
    
    #Calculate the ethnic target value, and store it in dictionary
    obj = self.button.mesh
    # We first clear the non applied ethnics
    for g in obj.facesGroups:
      if g.name not in ethnics:
        color =[255,255,255,255]
        for f in g.faces:
          f.color = [color,color,color]
          f.updateColors()
    # Then we color the applied ethnics, doing it in two steps makes sure we don't erase our coloring
    for g in obj.facesGroups:
      if g.name in ethnics:
        color = [int(255*ethnics[g.name]), 1-int(255*ethnics[g.name]), 255, 255]
        for f in g.faces:
          f.color = [color,color,color]
          f.updateColors()

class MacroModelingTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Macro modelling", "data/images/macro.png")
    
    # Macro sliders
    self.genderSlider = gui3d.Slider(self, "data/images/button_gender_macro.png",
      "data/images/slider.png", "data/images/slider_focused.png", position = [-0.45, 0.25, 9], value = 0.5)
    self.ageSlider = gui3d.Slider(self, "data/images/button_age_macro.png",
      "data/images/slider.png", "data/images/slider_focused.png", position = [-0.45, 0.1, 9], value = 0.5)
    self.muscleSlider = gui3d.Slider(self, "data/images/button_muscle_macro.png",
      "data/images/slider.png", "data/images/slider_focused.png", position = [-0.45, -0.05, 9], value = 0.5)
    self.weightSlider = gui3d.Slider(self, "data/images/button_weight_macro.png",
      "data/images/slider.png", "data/images/slider_focused.png", position = [-0.45, -0.20, 9], value = 0.5)
      
    @self.genderSlider.event
    def onChange(value):
      human = self.app.scene3d.selectedHuman
      self.app.do(MacroAction(human, "Gender", value, self.syncSliders))
      
    @self.ageSlider.event
    def onChange(value):
      human = self.app.scene3d.selectedHuman
      self.app.do(MacroAction(human, "Age", value, self.syncSliders))
      
    @self.muscleSlider.event
    def onChange(value):
      human = self.app.scene3d.selectedHuman
      self.app.do(MacroAction(human, "Muscle", value, self.syncSliders))
      
    @self.weightSlider.event
    def onChange(value):
      human = self.app.scene3d.selectedHuman
      self.app.do(MacroAction(human, "Weight", value, self.syncSliders))
    
    # Ethnic controls
    self.ethnicMapButtonGroup = []
    self.asiaButton = EthnicMapButton(self, self.ethnicMapButtonGroup, mesh = "data/3dobjs/button_asia.obj",
      texture = "data/images/button_asia.png", position = [0.45, 0.12, 9])
    self.europeButton = EthnicMapButton(self, self.ethnicMapButtonGroup, mesh = "data/3dobjs/button_europe.obj",
      texture = "data/images/button_europe.png", position = [0.37, 0.12, 9])
    self.africaButton = EthnicMapButton(self, self.ethnicMapButtonGroup, mesh = "data/3dobjs/button_africa.obj",
      texture = "data/images/button_africa.png", position = [0.37, 0.04, 9])
    self.americaButton = EthnicMapButton(self, self.ethnicMapButtonGroup, mesh = "data/3dobjs/button_america.obj",
      texture = "data/images/button_america.png", position = [0.45, 0.04, 9])
    self.ethnicButtonGroup = []
    self.ethnicIncreaseButton = gui3d.RadioButton(self, self.ethnicButtonGroup,
      mesh = "data/3dobjs/button_ethnincr.obj",
      texture = "data/images/button_ethnincr.png",
      selectedTexture = "data/images/button_ethnincr_on.png", position = [0.52, 0.12, 9],
      selected = True)
    self.ethnicDecreaseButton = gui3d.RadioButton(self, self.ethnicButtonGroup,
      mesh = "data/3dobjs/button_ethndecr.obj",
      texture = "data/images/button_ethndecr.png",
      selectedTexture = "data/images/button_ethndecr_on.png", position = [0.52, 0.07, 9])
    self.ethnicResetButton = gui3d.RadioButton(self, self.ethnicButtonGroup,
      mesh = "data/3dobjs/button_ethnreset.obj",
      texture = "data/images/button_ethnreset.png",
      selectedTexture = "data/images/button_ethnreset_on.png", position = [0.52, 0.02, 9])
      
    # Common controls
    self.background = gui3d.Object(category, "data/3dobjs/background.obj", position = [0, 0, -70])
    self.undoButton = gui3d.Button(category, mesh = "data/3dobjs/button_redo.obj",
      texture = "data/images/button_undo.png", 
      selectedTexture = "data/images/button_undo_on.png", position = [0.37,0.20,9])
    self.redoButton = gui3d.Button(category, mesh = "data/3dobjs/button_undo.obj",
      texture = "data/images/button_redo.png", 
      selectedTexture = "data/images/button_redo_on.png", position = [0.45,0.20,9])
    self.resetButton = gui3d.Button(category, mesh = "data/3dobjs/button_new.obj",
      texture = "data/images/button_new.png", 
      selectedTexture = "data/images/button_new_on.png", position = [0.52,0.20,9])
    
    @self.undoButton.event
    def onClicked(event):
      self.app.undo()
      
    @self.redoButton.event
    def onClicked(event):
      self.app.redo()
    
    @self.resetButton.event
    def onClicked(event):
      human = self.app.scene3d.selectedHuman
      human.resetMeshValues()
      human.applyAllTargets()
      self.syncSliders()
      self.syncEthnics()
      
    self.syncSliders()
      
  def syncSliders(self):
    human = self.app.scene3d.selectedHuman
    self.genderSlider.setValue(human.getGender())
    self.ageSlider.setValue(human.getAge())
    self.muscleSlider.setValue(human.getMuscle())
    self.weightSlider.setValue(human.getWeight())
    
  def syncEthnics(self):
    self.asiaButton.syncEthnics()
    self.europeButton.syncEthnics()
    self.africaButton.syncEthnics()
    self.americaButton.syncEthnics()
    
  def onShow(self, event):
    self.setFocus()
    gui3d.TaskView.onShow(self, event)