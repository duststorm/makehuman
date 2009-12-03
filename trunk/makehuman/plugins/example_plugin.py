# We need this for gui controls
import gui3d

print("example imported")

class ExampleTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Example", category.app.getThemeResource("images", "button_expressions.png"))
    
    # We add a button to the current task
    # A button just fires an event when it is clicked, if a selected texture is specified, it is used while the mouse is down on the button
    self.aButton = gui3d.Button(self,
      mesh = "data/3dobjs/button_ethnreset.obj",
      texture = self.app.getThemeResource("images", "button_ethnreset.png"),
      # getThemeResource returns a texture for a gui element according to the chosen theme
      selectedTexture = self.app.getThemeResource("images", "button_ethnreset_on.png"),
      position = [20, 60, 9])
    
    self.pushed = 0
    self.aButtonLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [120, 80, 9])
    self.aButtonLabel.setText("Pushed 0 times")
    
    @self.aButton.event
    def onClicked(event):
      self.pushed += 1
      self.aButtonLabel.setText("Pushed %d times"%(self.pushed))
    
    # We add a toggle button to the current task
    # A toggle button fires an event when it is clicked but retains its selected state after the mouse is up, if a selected texture is specified, it is used to show whether the button is toggled
    self.aToggleButton = gui3d.ToggleButton(self,
      mesh = "data/3dobjs/button_ethnreset.obj",
      texture = self.app.getThemeResource("images", "button_ethnreset.png"),
      selectedTexture = self.app.getThemeResource("images", "button_ethnreset_on.png"),
      position = [20, 120, 9])
      
    self.aToggleButtonLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [120, 140, 9])
    self.aToggleButtonLabel.setText("Not selected")
      
    @self.aToggleButton.event
    def onClicked(event):
      gui3d.ToggleButton.onClicked(self.aToggleButton, event)
      if self.aToggleButton.selected:
        self.aToggleButtonLabel.setText("Selected")
      else:
        self.aToggleButtonLabel.setText("Not selected")
        
    # Next we will add some radio buttons. For this we need a group, since only one in the group can be selected
    # A radio button fires an event when it is clicked but retains its selected state after the mouse is up, and deselects all other buttons in the group
    # If a selected texture is specified, it is used to show whether the button is selected
    self.aRadioButtonGroup = []
    
    self.aRadioButton1 = gui3d.RadioButton(self,
      self.aRadioButtonGroup,
      mesh = "data/3dobjs/button_ethnreset.obj",
      texture = self.app.getThemeResource("images", "button_ethnreset.png"),
      selectedTexture = self.app.getThemeResource("images", "button_ethnreset_on.png"),
      position = [20, 180, 9],
      # We make the first one selected
      selected = True)
      
    self.aRadioButtonLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [120, 200, 9])
    self.aRadioButtonLabel.setText("Button 1 is selected")
    
    self.aRadioButton2 = gui3d.RadioButton(self,
      self.aRadioButtonGroup,
      mesh = "data/3dobjs/button_ethnreset.obj",
      texture = self.app.getThemeResource("images", "button_ethnreset.png"),
      selectedTexture = self.app.getThemeResource("images", "button_ethnreset_on.png"),
      position = [20, 220, 9])
      
    @self.aRadioButton1.event
    def onClicked(event):
      gui3d.RadioButton.onClicked(self.aRadioButton1, event)
      self.aRadioButtonLabel.setText("Button 1 is selected")
      
    @self.aRadioButton2.event
    def onClicked(event):
      gui3d.RadioButton.onClicked(self.aRadioButton2, event)
      self.aRadioButtonLabel.setText("Button 2 is selected")
      
    # A slider needs both a background texture and a slider button texture
    # When the slider is dragged and released, an onChange event is fired
    # By default a slider goes from 0.0 to 1.0, and the initial position will be 0.0 unless specified
    self.aSlider = gui3d.Slider(self,
      self.app.getThemeResource("images", "button_gender_macro.png"),
      self.app.getThemeResource("images", "slider.png"),
      self.app.getThemeResource("images", "slider_focused.png"),
      position = [20, 250, 9],
      # We want the slider to start from the middle
      value = 0.5)
      
    self.aSliderLabel = gui3d.TextView(self,
      mesh = "data/3dobjs/empty.obj",
      position = [120, 240, 9])
    self.aSliderLabel.setText("Value is 0.5")
    
    @self.aSlider.event
    def onChange(value):
      self.aSliderLabel.setText("Value is %f"%(value))
      self.aProgressBar.setProgress(value, 1)
    
    # we also create a progressbar, which is updated as the slider moves
    self.aProgressBar = gui3d.ProgressBar(self,
      backgroundTexture = self.app.getThemeResource("images", "progressbar_background.png"),
      backgroundPosition = [20, 380, 9.1],
      barTexture = self.app.getThemeResource("images", "progressbar.png"),
      barPosition = [20, 380, 9.2])
    self.aProgressBar.setProgress(0.5, 0)
    
    self.aTextEdit = gui3d.TextEdit(self,
      mesh = "data/3dobjs/empty.obj",
      position = [20, 420, 9])
    self.aTextEdit.setText("Some text")

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements
def load(app):
  category = gui3d.Category(app, "Example", app.getThemeResource("images", "button_expressions.png"))
  taskview = ExampleTaskView(category)
  
  print("example loaded")
  print("Hello world")

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements
def unload(app):
  print("example unloaded")