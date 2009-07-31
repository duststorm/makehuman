""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TO DO

"""

__docformat__ = 'restructuredtext'

import gui3d, events3d

class HairTaskView(gui3d.TaskView):
  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, "Hair",  category.app.getThemeResource("images", "button_hair.png"))
    self.filechooser = gui3d.FileChooser(self, "data/hairs", "hair")
    
    @self.filechooser.event
    def onFileSelected(filename):
      print("Loading %s" %(filename))
      self.app.scene3d.selectedHuman.setHairFile("data/hairs/" + filename)
      self.app.categories["Modelling"].tasksByName["Macro modelling"].currentHair.setTexture(self.app.scene3d.selectedHuman.hairFile.replace(".hair", '.bmp'))
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
