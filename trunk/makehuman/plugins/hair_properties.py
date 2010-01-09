# We need this for gui controls
import gui3d

print("hair properties imported")

class Action:
  def __init__(self, human, before, after, postAction = None):
    self.name = "Change hair color"
    self.human = human
    self.before = before
    self.after = after
    self.postAction = postAction
    
  def do(self):
    self.human.hairColor = self.after
    if self.postAction:
      self.postAction()
    return True
    
  def undo(self):
    self.human.hairColor = self.before
    if self.postAction:
      self.postAction()
    return True

class HairPropertiesTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Hair", category.app.getThemeResource("images", "button_hair_det.png"),
      category.app.getThemeResource("images", "button_hair_det_on.png"))
      
    self.redSlider = gui3d.Slider(self,
      self.app.getThemeResource("images", "slider_red.png"),
      self.app.getThemeResource("images", "slider.png"),
      self.app.getThemeResource("images", "slider_focused.png"),
      position = [20, 90, 9.2])
      
    self.redSliderLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [20, 90, 9.4])
    self.redSliderLabel.setText("Red: 0")
    
    self.greenSlider = gui3d.Slider(self,
      self.app.getThemeResource("images", "slider_green.png"),
      self.app.getThemeResource("images", "slider.png"),
      self.app.getThemeResource("images", "slider_focused.png"),
      position = [20, 190, 9])
      
    self.greenSliderLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [20, 190, 9.4])
    self.greenSliderLabel.setText("Green: 0")
    
    self.blueSlider = gui3d.Slider(self,
      self.app.getThemeResource("images", "slider_blue.png"),
      self.app.getThemeResource("images", "slider.png"),
      self.app.getThemeResource("images", "slider_focused.png"),
      position = [20, 290, 9])
      
    self.blueSliderLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [20, 290, 9.4])
    self.blueSliderLabel.setText("Blue: 0")
    
    self.colorPreview = gui3d.Object(self, "data/3dobjs/colorpreview.obj", position = [20, 390, 9])
    
    self.colorPreviewLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [20, 380, 9.4])
    self.colorPreviewLabel.setText("Hair color")
    
    @self.redSlider.event
    def onChange(value):
      self.changeColor([value, self.greenSlider.getValue(), self.blueSlider.getValue()])
      
    @self.greenSlider.event
    def onChange(value):
      self.changeColor([self.redSlider.getValue(), value, self.blueSlider.getValue()])
      
    @self.blueSlider.event
    def onChange(value):
      self.changeColor([self.redSlider.getValue(), self.greenSlider.getValue(), value])
      
  def changeColor(self, color):
    action = Action(self.app.scene3d.selectedHuman, self.app.scene3d.selectedHuman.hairColor, color, self.syncSliders)
    self.app.do(action)
      
  def setColor(self, color):
    c = [int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), 255]
    for g in self.colorPreview.mesh.facesGroups:
      for f in g.faces:
        f.color = [c, c, c]
        f.updateColors()
    
  def onShow(self, event):
    gui3d.TaskView.onShow(self, event)
    hairColor = self.app.scene3d.selectedHuman.hairColor;
    self.syncSliders()
    
  def syncSliders(self):
    hairColor = self.app.scene3d.selectedHuman.hairColor;
    self.redSlider.setValue(hairColor[0])
    self.redSliderLabel.setText("Red: %.2f"%(hairColor[0]))
    self.greenSlider.setValue(hairColor[1])
    self.greenSliderLabel.setText("Green: %.2f"%(hairColor[1]))
    self.blueSlider.setValue(hairColor[2])
    self.blueSliderLabel.setText("Blue: %.2f"%(hairColor[2]))
    self.setColor(hairColor)

category = None
taskview = None

def load(app):
  taskview = HairPropertiesTaskView(app.categories["Modelling"])
  print("hair properties loaded")

def unload(app):
  print("hair properties unloaded")
