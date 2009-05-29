import gui3d, events3d

class HairTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Hair",  "data/images/button_hair.png")
    self.filechooser = gui3d.FileChooser(self, "data/hair", "mhh")
    
    @self.filechooser.event
    def onFileSelected(filename):
      print("Loading %s" %(filename))
      
      self.app.switchCategory("Modelling")
      self.app.scene3d.redraw(1)
    
  def onShow(self, event):
    # When the task gets shown, set the focus to the file chooser
    self.app.scene3d.selectedHuman.hide()
    gui3d.TaskView.onShow(self, event)
    self.filechooser.setFocus()
    # HACK: otherwise the toolbar background disappears for some weird reason
    self.app.scene3d.redraw(0)
    
  def onHide(self, event):
    self.app.scene3d.selectedHuman.show()
    gui3d.TaskView.onHide(self, event)
