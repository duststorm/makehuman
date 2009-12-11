# We need this for gui controls
import gui3d
import aljabr



class MeasurementTaskView(gui3d.TaskView):
    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, "Example", category.app.getThemeResource("images", "button_measure.png"))
        gui3d.Object(self, "data/3dobjs/background.obj", position = [400, 300, -89.98])
        self.measureList = gui3d.TextView(self, mesh = "data/3dobjs/empty.obj", position = [10, 100, 8.04])
        self.measureList.setText("");
        self.hipGirthSlider = gui3d.Slider(self,
            self.app.getThemeResource("images", "button_hip_girth.png"),
            self.app.getThemeResource("images", "slider.png"),
            self.app.getThemeResource("images", "slider_focused.png"),
            position=[10, 460, 9.04],
            # We want the slider to start from the middle
            value=0.5)
        @self.hipGirthSlider.event
        def onChange(value):
            self.hipGirthLabel.setText("Value is %f" % (value))
        self.hipGirthLabel = gui3d.TextView(self,
            mesh="data/3dobjs/empty.obj",
            position=[10, 460, 8.04])
        self.hipGirthLabel.setText("Value is 0.5")
        self.waistGirthSlider = gui3d.Slider(self,
            self.app.getThemeResource("images", "button_waist_girth.png"),
            self.app.getThemeResource("images", "slider.png"),
            self.app.getThemeResource("images", "slider_focused.png"),
            position=[10, 360, 9.04],
            # We want the slider to start from the middle
            value=0.5)

        self.waistGirthLabel = gui3d.TextView(self,
            mesh="data/3dobjs/empty.obj",
            position=[10, 360, 8.04])
        self.waistGirthLabel.setText("Value is 0.5")

        @self.waistGirthSlider.event
        def onChange(value):
            self.waistGirthLabel.setText("Value is %f" % (value))

        self.chestGirthSlider = gui3d.Slider(self,
            self.app.getThemeResource("images", "button_chest_girth.png"),
            self.app.getThemeResource("images", "slider.png"),
            self.app.getThemeResource("images", "slider_focused.png"),
            position=[10, 260, 8.04],
            # We want the slider to start from the middle
            value=0.5)

        self.chestGirthLabel = gui3d.TextView(self,
            mesh="data/3dobjs/empty.obj",
            position=[10, 260, 8.04])
        self.chestGirthLabel.setText("Value is 0.5")

        @self.chestGirthSlider.event
        def onChange(value):
            self.chestGirthLabel.setText("Value is %f" % (value))

        self.statureSlider = gui3d.Slider(self,
            self.app.getThemeResource("images", "button_stature.png"),
            self.app.getThemeResource("images", "slider.png"),
            self.app.getThemeResource("images", "slider_focused.png"),
            position=[10, 160, 8.04],
            # We want the slider to start from the middle
            value=0.5)

        self.statureLabel = gui3d.TextView(self,
            mesh="data/3dobjs/empty.obj",
            position=[10, 160, 8.04])
        self.statureLabel.setText("Value is 0.5")

        @self.statureSlider.event
        def onChange(value):
            self.statureLabel.setText("Value is %f" % (value))
            self.measureList.setText(ruler.getMeasurementsString());

        ruler = Ruler(category.app.scene3d.selectedHuman)
        self.measureList.setText(ruler.getMeasurementsString());

category = None
taskview = None
ruler = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements
def load(app):
  category = gui3d.Category(app, "Example", app.getThemeResource("images", "button_measure.png"))
  taskview = MeasurementTaskView(category)
  # Zoom the camera
  @taskview.event
  def onMouseWheel(event):
     if event.wheelDelta > 0:
        mh.cameras[0].zoom -= 0.65
        app.scene3d.redraw()
     else:
        mh.cameras[0].zoom += 0.65
        app.scene3d.redraw()
  @taskview.event
  def onMouseDragged(event):
    diff = app.scene3d.getMouseDiff()
    leftButtonDown =event.button & 1
    middleButtonDown = event.button & 2
    rightButtonDown = event.button & 4

    if (leftButtonDown and rightButtonDown) or middleButtonDown:
        mh.cameras[0].zoom += 0.05 * diff[1]
    elif leftButtonDown:
        human = app.scene3d.selectedHuman
        rot = human.getRotation()
        rot[0] += 0.5 * diff[1]
        rot[1] += 0.5 * diff[0]
        human.setRotation(rot)
    elif rightButtonDown:
        human = app.scene3d.selectedHuman
        trans = human.getPosition()
        trans[0] += 0.1 * diff[0]
        trans[1] -= 0.1 * diff[1]
        human.setPosition(trans)



# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements
def unload(app):
  print ""

class Ruler:
  """
  This class contains ...
  """

  def __init__(self, human):
    # these are tables of vertex indices for each body measurement of interest
    self.Distances = { 'NeckHeight': [1244,7577],
                   'ChestWidth': [1120, 7167],
                   'UnderBustWidth': [8829, 5488],
                   'AbdomenWidth': [8802, 5461],
                   'HipsWidth': [9041, 5700],
                   'MidThightWidth': [9035, 1140]}
    self.Measures = { 'Chest': [2553, 3574, 2634, 3466, 4148, 4435,3600, 10192, 9992,10077,
                                10305, 10303, 10957, 10976, 10218, 11055, 10060, 11054, 10044, 10115,
                                3718, 2644, 4185, 2554, 4169],
                      'Waist' : [2906, 3528, 2949, 3700, 3397, 3404, 3403, 3402, 5675, 4460,
                                 4139, 4466, 4467, 4468,
                                 6897, 9967, 9968, 10086, 10205, 9969, 9791, 7266, 7265, 7264,
                                 7267, 7242, 7290, 7246, 7314],
                       'Hips' : [7298, 2936, 3816, 3817, 3821, 4487, 3822, 3823, 3913, 3915, 4506,
                                 5688, 4505, 6860, 6785, 6859, 7094, 7096, 7188, 7189, 6878, 7190,
                                 7194, 7247, 7300]
                   }

    self.humanoid = human

  def getDistance(self, distancename):
    return 10.0 * aljabr.vdist(self.humanoid.mesh.verts[self.Distances[distancename][0]].co, self.humanoid.mesh.verts[self.Distances[distancename][1]].co)

  def getMeasure(self, measurementname):
    measure = 0
    vindex1 = self.Measures[measurementname][0]
    for vindex2 in self.Measures[measurementname]:
      measure += aljabr.vdist(self.humanoid.mesh.verts[vindex1].co, self.humanoid.mesh.verts[vindex2].co)
      vindex1 = vindex2
    return 10.0 * measure

  def getMeasurementsString(self):
    measuretext = ""

#    for key in self.Distances:
#      measuretext += key
#      measuretext += ": %.1f cm \n" % self.getDistance(key)
#    measuretext += " \n"
    for key in self.Measures:
      measuretext += key
      measuretext += ": %.1f cm \n" % self.getMeasure(key)
      measuretext += " \n"
    return measuretext