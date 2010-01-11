import gui3d, animation3d, humanmodifier

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
      self.human.applyAllTargets(self.human.app.progress)
      self.postAction()
      return True
      
    def undo(self):
      getattr(self.human, "set" + self.method)(self.before)
      self.human.applyAllTargets(self.human.app.progress)
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
      self.human.applyAllTargets(self.human.app.progress)
      self.postAction()
      return True
      
    def undo(self):
      self.human.setEthnic(self.ethnic, self.before)
      self.human.applyAllTargets(self.human.app.progress)
      self.postAction()
      return True

class EthnicMapButton(gui3d.RadioButton):
  def __init__(self, group, parent, mesh = "data/3dobjs/button_standard.obj", texture = None,
    selectedTexture = None, position = [0, 0, 9], selected = False):
    gui3d.RadioButton.__init__(self, group, parent, mesh, texture, selectedTexture, position, selected)
    self.button.setRotation([180, 0, 0])

  def onSelected(self, selected):
    if selected:
      pos = self.button.getPosition()
      t = animation3d.Timeline(0.250)
      t.append(animation3d.PathAction(self.button.mesh, [pos, [pos[0] - 300, pos[1] + 100, pos[2]]]))
      t.append(animation3d.ScaleAction(self.button.mesh, [1, 1, 1], [5, 5, 5]))
      t.append(animation3d.UpdateAction(self.app.scene3d))
      t.start()
    else:
      pos = self.button.getPosition()
      t = animation3d.Timeline(0.250)
      t.append(animation3d.PathAction(self.button.mesh, [pos, [pos[0] + 300, pos[1] - 100, pos[2]]]))
      t.append(animation3d.ScaleAction(self.button.mesh, [5, 5, 5], [1, 1, 1]))
      t.append(animation3d.UpdateAction(self.app.scene3d))
      t.start()
      
  def onMouseDown(self, event):
    human = self.app.scene3d.selectedHuman
    if self.selected:
      faceGroupSel = self.app.scene3d.getSelectedFacesGroup()
      faceGroupName = faceGroupSel.name
      print(faceGroupName)
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
    gui3d.TaskView.__init__(self, category, "Macro modelling", category.app.getThemeResource("images", "macro.png"),
      category.app.getThemeResource("images", "macro_on.png"))
    
    self.status = gui3d.TextView(self, mesh = "data/3dobjs/empty.obj", position = [10, 590, 9.1])
    
    gui3d.Object(self, "data/3dobjs/group_main.obj", self.app.getThemeResource("images", "group_main.png"), [10, 80, 9.0])
    gui3d.Object(category, "data/3dobjs/group_actions.obj", self.app.getThemeResource("images", "group_actions.png"), [10, 340, 9.0])
    gui3d.Object(self, "data/3dobjs/group_ethnics.obj", self.app.getThemeResource("images", "group_ethnics.png"), [10, 408, 9.0])
    
    # Macro sliders
    self.genderSlider = gui3d.Slider(self, self.app.getThemeResource("images", "button_gender_macro.png"),
      self.app.getThemeResource("images", "slider.png"), self.app.getThemeResource("images", "slider_focused.png"), position = [10, 105, 9.3], value = 0.5)
    self.ageSlider = gui3d.Slider(self, self.app.getThemeResource("images", "button_age_macro.png"),
      self.app.getThemeResource("images", "slider.png"), self.app.getThemeResource("images", "slider_focused.png"), position = [10, 145, 9.01], value = 0.5)
    self.muscleSlider = gui3d.Slider(self, self.app.getThemeResource("images", "button_muscle_macro.png"),
      self.app.getThemeResource("images", "slider.png"), self.app.getThemeResource("images", "slider_focused.png"), position = [10, 190, 9.02], value = 0.5)
    self.weightSlider = gui3d.Slider(self, self.app.getThemeResource("images", "button_weight_macro.png"),
      self.app.getThemeResource("images", "slider.png"), self.app.getThemeResource("images", "slider_focused.png"), position = [10, 235, 9.03], value = 0.5)
    self.heightSlider = gui3d.Slider(self, self.app.getThemeResource("images", "button_height_macro.png"),
      self.app.getThemeResource("images", "slider.png"), self.app.getThemeResource("images", "slider_focused.png"), position = [10, 280, 9.04], value = 0.5)
    
      
    @self.genderSlider.event
    def onChange(value):
      human = self.app.scene3d.selectedHuman
      self.app.do(MacroAction(human, "Gender", value, self.syncSliders))
      self.syncStatus()
      
    @self.ageSlider.event
    def onChange(value):
      human = self.app.scene3d.selectedHuman
      self.app.do(MacroAction(human, "Age", value, self.syncSliders))
      self.syncStatus()
      
    @self.muscleSlider.event
    def onChange(value):
      human = self.app.scene3d.selectedHuman
      self.app.do(MacroAction(human, "Muscle", value, self.syncSliders))
      self.syncStatus()
      
    @self.weightSlider.event
    def onChange(value):
      human = self.app.scene3d.selectedHuman
      self.app.do(MacroAction(human, "Weight", value, self.syncSliders))
      self.syncStatus()
      
    @self.heightSlider.event
    def onChange(value):
      human = self.app.scene3d.selectedHuman
      before = {}
      before["data/targets/macrodetails/universal-stature-dwarf.target"] = human.getDetail("data/targets/macrodetails/universal-stature-dwarf.target")
      before["data/targets/macrodetails/universal-stature-giant.target"] = human.getDetail("data/targets/macrodetails/universal-stature-giant.target")
      modifier = humanmodifier.Modifier(human, "data/targets/macrodetails/universal-stature-dwarf.target",
        "data/targets/macrodetails/universal-stature-giant.target")
      modifier.setValue(value * 2 -1)
      after = {}
      after["data/targets/macrodetails/universal-stature-dwarf.target"] = human.getDetail("data/targets/macrodetails/universal-stature-dwarf.target")
      after["data/targets/macrodetails/universal-stature-giant.target"] = human.getDetail("data/targets/macrodetails/universal-stature-giant.target")
      self.app.did(humanmodifier.Action(human, before, after, self.syncSliders))
      human.applyAllTargets(self.app.progress)
    
    # Ethnic controls
    self.ethnicMapButtonGroup = []
    self.asiaButton = EthnicMapButton(self, self.ethnicMapButtonGroup, mesh = "data/3dobjs/button_asia.obj",
      texture = self.app.getThemeResource("images", "button_asia.png"), position = [630, 150, 9])
    self.europeButton = EthnicMapButton(self, self.ethnicMapButtonGroup, mesh = "data/3dobjs/button_europe.obj",
      texture = self.app.getThemeResource("images", "button_europe.png"), position = [690, 150, 9])
    self.africaButton = EthnicMapButton(self, self.ethnicMapButtonGroup, mesh = "data/3dobjs/button_africa.obj",
      texture = self.app.getThemeResource("images", "button_africa.png"), position = [630, 210, 9])
    self.americaButton = EthnicMapButton(self, self.ethnicMapButtonGroup, mesh = "data/3dobjs/button_america.obj",
      texture = self.app.getThemeResource("images", "button_america.png"), position = [690, 210, 9])
    self.ethnicButtonGroup = []
    self.ethnicIncreaseButton = gui3d.RadioButton(self, self.ethnicButtonGroup,
      mesh = "data/3dobjs/button_standard_little.obj",
      texture = self.app.getThemeResource("images", "button_ethnincr.png"),
      selectedTexture = self.app.getThemeResource("images", "button_ethnincr_on.png"), position = [750, 140, 9],
      selected = True)
    self.ethnicDecreaseButton = gui3d.RadioButton(self, self.ethnicButtonGroup,
      mesh = "data/3dobjs/button_standard_little.obj",
      texture = self.app.getThemeResource("images", "button_ethndecr.png"),
      selectedTexture = self.app.getThemeResource("images", "button_ethndecr_on.png"), position = [750, 180, 9])
      
    # Common controls
    self.background = gui3d.Object(category, "data/3dobjs/background.obj", position = [400, 300, -89.98])
    self.undoButton = gui3d.Button(category, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_undo.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_undo_on.png"), position = [33, 371, 9.1])
    self.redoButton = gui3d.Button(category, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_redo.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_redo_on.png"), position = [68, 371, 9.1])
    self.resetButton = gui3d.Button(category, mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_reset.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_reset_on.png"), position = [103, 371,9.1])
      
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
      human.applyAllTargets(self.app.progress)
      self.syncSliders()
      self.syncEthnics()
      self.syncStatus()
      
    self.currentHair = gui3d.Button(category, mesh = "data/3dobjs/button_standard_little.obj",
      texture = self.app.scene3d.selectedHuman.hairFile.replace(".hair", '.png'), position = [600, 580, 9.2])
    
    @self.currentHair.event
    def onClicked(event):
      self.app.switchCategory("Library")
      self.app.scene3d.redraw(1)
      
    self.backgroundImage = gui3d.Object(category, "data/3dobjs/background.obj", position = [400, 300, 1], visible = False)
    self.backgroundImageToggle = gui3d.ToggleButton(category, mesh = "data/3dobjs/button_standard.obj", position = [33, 390, 9.1],texture = self.app.getThemeResource("images", "button_background_toggle.png"),selectedTexture = self.app.getThemeResource("images", "button_background_toggle_on.png"))
      
    @self.backgroundImageToggle.event
    def onClicked(event):
      if self.backgroundImage.isVisible():
        self.backgroundImage.hide()
        self.backgroundImageToggle.setSelected(False)
      elif self.backgroundImage.hasTexture():
        self.backgroundImage.show()
        self.backgroundImageToggle.setSelected(True)
      else:
        self.app.switchCategory("Library")
        self.app.switchTask("Background")
      self.app.scene3d.redraw(1)
      
    # Ethnics buttons
    self.ethnicsGroup = []
    self.asianButton = gui3d.RadioButton(self, self.ethnicsGroup, mesh = "data/3dobjs/button_standard_big.obj",
      texture = self.app.getThemeResource("images", "button_african.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_african_on.png"), position = [49, 440, 9.1])
    self.africanButton = gui3d.RadioButton(self, self.ethnicsGroup, mesh = "data/3dobjs/button_standard_big.obj",
      texture = self.app.getThemeResource("images", "button_asian.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_asian_on.png"), position = [49, 460, 9.1])
    self.caucas1Button = gui3d.RadioButton(self, self.ethnicsGroup, mesh = "data/3dobjs/button_standard_big.obj",
      texture = self.app.getThemeResource("images", "button_caucas1.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_caucas1_on.png"), position = [49, 480, 9.1])
    self.caucas2Button = gui3d.RadioButton(self, self.ethnicsGroup, mesh = "data/3dobjs/button_standard_big.obj",
      texture = self.app.getThemeResource("images", "button_caucas2.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_caucas2_on.png"), position = [49, 500, 9.1])
    self.pacificButton = gui3d.RadioButton(self, self.ethnicsGroup, mesh = "data/3dobjs/button_standard_big.obj",
      texture = self.app.getThemeResource("images", "button_pacific.png"), 
      selectedTexture = self.app.getThemeResource("images", "button_pacific_on.png"), position = [49, 520, 9.1])
    self.ethnicResetButton = gui3d.Button(self,
      mesh = "data/3dobjs/button_standard.obj",
      texture = self.app.getThemeResource("images", "button_ethnreset.png"),
      selectedTexture = self.app.getThemeResource("images", "button_ethnreset_on.png"), position = [100, 520, 9.1])     
      
    self.syncSliders()
    self.syncStatus()
      
  def syncSliders(self):
    human = self.app.scene3d.selectedHuman
    self.genderSlider.setValue(human.getGender())
    self.ageSlider.setValue(human.getAge())
    self.muscleSlider.setValue(human.getMuscle())
    self.weightSlider.setValue(human.getWeight())
    modifier = humanmodifier.Modifier(human, "data/targets/macrodetails/universal-stature-dwarf.target",
      "data/targets/macrodetails/universal-stature-giant.target")
    self.heightSlider.setValue(0.5 + modifier.getValue() / 2.0) 
    
  def syncEthnics(self):
    self.asiaButton.syncEthnics()
    self.europeButton.syncEthnics()
    self.africaButton.syncEthnics()
    self.americaButton.syncEthnics()
    
  def syncStatus(self):
    human = self.app.scene3d.selectedHuman
    status = ""
    if human.getGender() == 0.5:
      gender = "Gender: neutral, "
    else:
      gender = "Gender: %.2f%% female, %.2f%% male, " %((1.0 - human.getGender()) * 100, human.getGender() * 100)
    status += gender
    if human.getAge() < 0.5:
      age = 12 + (25 - 12) * 2 * human.getAge()
    else:
      age = 25 + (70 - 25) * 2 * (human.getAge() - 0.5)
    status += "Age: %d, " %(age)
    status += "Muscle: %.2f%%, " %(human.getMuscle() * 100.0)
    status += "Weight: %.2f%%" %(50 + (150 - 50) * human.getWeight())
    self.status.setText(status)
    
  def onShow(self, event):
    self.setFocus()
    gui3d.TaskView.onShow(self, event)
