# We need this for gui controls
import gui3d

print("hair properties imported")

class HairPropertiesTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Hair", category.app.getThemeResource("images", "button_hair.png"))
      
    self.redSlider = gui3d.Slider(self,
      self.app.getThemeResource("images", "button_gender_macro.png"),
      self.app.getThemeResource("images", "slider.png"),
      self.app.getThemeResource("images", "slider_focused.png"),
      position = [20, 60, 9])
      
    self.redSliderLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [20, 60, 9.4])
    self.redSliderLabel.setText("Red: 0")
    
    self.greenSlider = gui3d.Slider(self,
      self.app.getThemeResource("images", "button_gender_macro.png"),
      self.app.getThemeResource("images", "slider.png"),
      self.app.getThemeResource("images", "slider_focused.png"),
      position = [20, 160, 9])
      
    self.greenSliderLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [20, 160, 9.4])
    self.greenSliderLabel.setText("Green: 0")
    
    self.blueSlider = gui3d.Slider(self,
      self.app.getThemeResource("images", "button_gender_macro.png"),
      self.app.getThemeResource("images", "slider.png"),
      self.app.getThemeResource("images", "slider_focused.png"),
      position = [20, 260, 9])
      
    self.blueSliderLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [20, 260, 9.4])
    self.blueSliderLabel.setText("Blue: 0")
    
    self.colorPreview = gui3d.Object(self, "data/3dobjs/colorpreview.obj", position = [20, 360, 9])
    
    self.colorPreviewLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [20, 350, 9.4])
    self.colorPreviewLabel.setText("Hair color")
    
    @self.redSlider.event
    def onChange(value):
      self.redSliderLabel.setText("Red: %.2f"%(value))
      self.setColor([value, self.greenSlider.getValue(), self.blueSlider.getValue()])
      
    @self.greenSlider.event
    def onChange(value):
      self.greenSliderLabel.setText("Green: %.2f"%(value))
      self.setColor([self.redSlider.getValue(), value, self.blueSlider.getValue()])
      
    @self.blueSlider.event
    def onChange(value):
      self.blueSliderLabel.setText("Blue: %.2f"%(value))
      self.setColor([self.redSlider.getValue(), self.greenSlider.getValue(), value])
      
  def setColor(self, color):
    c = [color[0] * 255, color[1] * 255, color[2] * 255, 255]
    for g in self.colorPreview.mesh.facesGroups:
      for f in g.faces:
        f.color = [c, c, c]
        f.updateColors()
    self.app.scene3d.selectedHuman.hairColor = [color[0], color[1], color[2]]
    
  def onShow(self, event):
    gui3d.TaskView.onShow(self, event)
    hairColor = self.app.scene3d.selectedHuman.hairColor;
    self.redSlider.setValue(hairColor[0])
    self.greenSlider.setValue(hairColor[1])
    self.blueSlider.setValue(hairColor[2])
    self.setColor(hairColor)

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements
def load(app):
  taskview = HairPropertiesTaskView(app.categories["Modelling"])
  
  print("hair properties loaded")
  print("Hello world")

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements
def unload(app):
  print("hair properties unloaded")