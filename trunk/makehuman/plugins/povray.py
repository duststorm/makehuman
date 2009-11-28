import sys
if 'nt' in sys.builtin_module_names:
    sys.path.append("./pythonmodules")
import subprocess
# We need this for rendering
import mh2povray
# We need this for gui controls
import gui3d

print("povray imported")

povray = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements
def load(app):
  povray = gui3d.TaskView(app.categories["Rendering"], "Povray",  app.getThemeResource("images", "button_povray.png"))
    
  @povray.event
  def onShow(event):
    pass
  @povray.event
  def onHide(event):
    pass
  @povray.button.event
  def onClicked(event):
    reload(mh2povray)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
    for obj in app.scene3d.objects:
      # print "POV-Ray Export test: ", obj.name
      # Only process the humanoid figure
      if obj.name == "base.obj":
        cameraData = app.scene3d.getCameraSettings()
        mh2povray.povrayExport(obj, cameraData)
      
  print("povray loaded")

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements
def unload(app):
  print("povray unloaded")