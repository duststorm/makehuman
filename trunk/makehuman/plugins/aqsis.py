import sys
if 'nt' in sys.builtin_module_names:
    sys.path.append("./pythonmodules")
import subprocess
# We need this for rendering
import mh2renderman
# We need this for gui controls
import gui3d

print("aqsis imported")

aqsis = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements
def load(app):
  # Create aqsis shaders
  #subprocess.Popen("aqsl data/shaders/aqsis/lightmap_aqsis.sl -o data/shaders/aqsis/lightmap.slx", shell=True)
  subprocess.Popen("aqsl data/shaders/renderman/skin.sl -o data/shaders/renderman/skin.slx", shell=True)
  subprocess.Popen("aqsl data/shaders/renderman/onlyci.sl -o data/shaders/renderman/onlyci.slx", shell=True)
  subprocess.Popen("aqsl data/shaders/renderman/lightmap.sl -o data/shaders/renderman/lightmap.slx", shell=True)
  subprocess.Popen("aqsl data/shaders/renderman/hair.sl -o data/shaders/renderman/hair.slx", shell=True)
  subprocess.Popen("aqsl data/shaders/renderman/shadowspot.sl -o data/shaders/renderman/shadowspot.slx", shell=True)
    
  aqsis = gui3d.TaskView(app.categories["Rendering"], "Aqsis",  app.getThemeResource("images", "button_aqsis.png"))
    
  @aqsis.event
  def onShow(event):
    pass
  @aqsis.event
  def onHide(event):
    pass
  @aqsis.button.event
  def onClicked(event):
    mh2renderman.saveScene(app.scene3d, "scena.rib", "renderman_output", "aqsis")
  
  print("aqsis loaded")

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements
def unload(app):
  print("aqsis unloaded")
