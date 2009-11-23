import gui3d

class MeasurementTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Measurement", category.app.getThemeResource("images", "button_measure.png"))

category = None
taskview = None

def load(app):
  category = gui3d.Category(app, "Measurement", app.getThemeResource("images", "button_measure.png"))
  taskview = MeasurementTaskView(category)
  print("Measurement loaded")
  
def unload(app):
  pass
  # Remove taskview
  # Remove category
  print("Measurement unloaded")

print("Measurement imported")