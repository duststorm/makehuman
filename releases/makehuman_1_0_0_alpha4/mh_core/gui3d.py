"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TODO

"""

__docformat__ = 'restructuredtext'

import events3d, files3d, animation3d, module3d, types, mh
import os

# Wrapper around Object3D
class Object(events3d.EventHandler):
  def __init__(self, view, mesh, texture = None, position = [0, 0, 9], camera = 1, shadeless = 1, visible = True):
    self.app = view.app
    self.view = view
    self.mesh = files3d.loadMesh(self.app.scene3d, mesh, position[0], position[1], position[2])
    self.texture = texture
    self.meshName = mesh
    if texture:
      self.mesh.setTexture(texture)
    view.objects.append(self)
    self.mesh.setCameraProjection(camera)
    if view.isVisible() and visible:
      self.mesh.setVisibility(1)
    else:
      self.mesh.setVisibility(0)
    self.mesh.setShadeless(shadeless)
    self.visible = visible
    self.mesh.object = self
    #print("Created object with mesh ", mesh, texture, position)
    
  def show(self):
    self.visible = True
    self.setVisibility(True)
    
  def hide(self):
    #print("hiding ", self.meshName)
    self.visible = False
    self.setVisibility(False)
    
  def isVisible(self):
    return self.visible
  
  def getPosition(self):
    return [self.mesh.x, self.mesh.y, self.mesh.z]
  
  def setPosition(self, position):
    self.mesh.setLoc(position[0], position[1], position[2])
    
  def getRotation(self):
    return [self.mesh.rx, self.mesh.ry, self.mesh.rz]
  
  def setRotation(self, rotation):
    self.mesh.setRot(rotation[0], rotation[1], rotation[2])
    
  def setTexture(self, texture):
    if texture:
      self.mesh.setTexture(texture)
    else:
      self.mesh.clearTexture()
    
  def clearTexture(self):
    self.mesh.clearTexture()
    
  def hasTexture(self):
    return self.mesh.hasTexture()
  
  def setVisibility(self, visibility):
    #print("changing visibility of ", self.meshName, "to", self.view.isVisible() and self.visible and visibility)
    if self.view.isVisible() and self.visible and visibility:
      self.mesh.setVisibility(1)
    else:
      self.mesh.setVisibility(0)
    
  def setScale(self, scale, scaleY = None):
    if scaleY:
      self.mesh.setScale(scale, scaleY, 1)
    else:
      self.mesh.setScale(scale, scale, 1)
    
  def setText(self, text):
    self.mesh.setText(text)
    
  def getText(self, text):
    self.mesh.text
    
  def onMouseDown(self, event):
    self.view.callEvent("onMouseDown", event)
    
  def onMouseMoved(self, event):
    self.view.callEvent("onMouseMoved", event)
    
  def onMouseDragged(self, event):
    self.view.callEvent("onMouseDragged", event)
    
  def onMouseUp(self, event):
    self.view.callEvent("onMouseUp", event)
    
  def onMouseEntered(self, event):
    self.view.callEvent("onMouseEntered", event)
    
  def onMouseExited(self, event):
    self.view.callEvent("onMouseExited", event)
    
  def onClicked(self, event):
    self.view.callEvent("onClicked", event)
    
  def onMouseWheel(self, event):
    self.view.callEvent("onMouseWheel", event)
    
  def onKeyDown(self, event):
    self.view.callEvent("onKeyDown", event)
    
  def onKeyUp(self, event):
    self.view.callEvent("onKeyDown", event)

# Generic view
class View(events3d.EventHandler):
  def __init__(self, parent = None, visible = True):
    self.app = parent.app
    self.parent = parent
    self.children = []
    self.objects = []
    self.canHaveFocus = True
    self.__visible = visible
    self.__totalVisibility = parent.isVisible() and visible
    
    parent.children.append(self)
    
  def show(self):
    self.__visible = True
    self.__updateVisibility()
    
  def hide(self):
    self.__visible = False
    self.__updateVisibility()
    
  def isVisible(self):
    return self.__totalVisibility
    
  def setFocus(self):
    self.app.setFocus(self)
    
  def hasFocus(self):
    return self.app.focusView is self
      
  def __updateVisibility(self):
    previousVisibility = self.__totalVisibility
    if self.parent:
      self.__totalVisibility = self.parent.isVisible() and self.__visible
    else:
      self.__totalVisibility = self.__visible
    if self.__totalVisibility:
      for o in self.objects:
        o.setVisibility(True)
    else:
      for o in self.objects:
        o.setVisibility(False)
    for v in self.children:
      v.__updateVisibility()
      
    if self.__totalVisibility != previousVisibility:
      if self.__totalVisibility:
        self.callEvent("onShow", None)
      else:
        self.callEvent("onHide", None)
        
  def onMouseDown(self, event):
    self.parent.callEvent("onMouseDown", event)
    
  def onMouseMoved(self, event):
    self.parent.callEvent("onMouseMoved", event)
    
  def onMouseDragged(self, event):
    self.parent.callEvent("onMouseDragged", event)
    
  def onMouseUp(self, event):
    self.parent.callEvent("onMouseUp", event)
    
  def onMouseEntered(self, event):
    self.parent.callEvent("onMouseEntered", event)
    
  def onMouseExited(self, event):
    self.parent.callEvent("onMouseExited", event)
    
  def onClicked(self, event):
    self.parent.callEvent("onClicked", event)
    
  def onMouseWheel(self, event):
    self.parent.callEvent("onMouseWheel", event)
    
  def onKeyDown(self, event):
    self.parent.callEvent("onKeyDown", event)
    
  def onKeyUp(self, event):
    self.parent.callEvent("onKeyUp", event)

# A View representing a specific task
class TaskView(View):
  def __init__(self, category, name, texture):
    View.__init__(self, parent = category, visible = False)
    self.canHaveFocus = False
    self.name = name
    self.focusWidget = None
    
    # The button is attached to the parent, as it stays visible when the category is hidden
    self.button = Object(self.parent, "data/3dobjs/button_standard.obj",
      texture = texture, position = [50 + len(self.parent.tasks) * 80, 600.0 - 17.0, 9.1])
      
    if name in category.tasksByName:
      raise KeyError("The task with this name already exists", name)
    
    category.tasks.append(self)
    category.tasksByName[self.name] = self
    
    @self.button.event
    def onClicked(event):
      self.app.switchTask(self.name)

  def onShow(self, event):
    #print("onShow", self.name, event)
    pos = self.button.getPosition()
    pos[1] -= 10.0
    self.button.setPosition(pos)
    self.button.setScale(1.5)
    self.show()
    
  def onHide(self, event):
    #print("onHide", self.name, event)
    pos = self.button.getPosition()
    pos[1] += 10.0
    self.button.setPosition(pos)
    self.button.setScale(1.0)
    self.hide()

# A category grouping similar tasks
class Category(View):
  def __init__(self, parent, name, texture):
    View.__init__(self, parent, visible = False)
    self.canHaveFocus = False
    self.name = name
    self.tasks = []
    self.tasksByName = {}
    
    # The button is attached to the parent, as it stays visible when the category is hidden
    self.button = Object(self.parent, "data/3dobjs/button_standard_big.obj",
      position = [50 + len(self.app.categories) * 80, 20.0, 9.1], texture = texture)
      
    if name in parent.categories:
      raise KeyError("The category with this name already exists", name)
      
    parent.categories[name] = self
    
    @self.button.event
    def onClicked(event):
      self.app.switchCategory(self.name)
      
  def onShow(self, event):
    pos = self.button.getPosition()
    pos[1] += 10
    self.button.setPosition(pos)
    self.button.setScale(1.5)
    self.show()
    
  def onHide(self, event):
    pos = self.button.getPosition()
    pos[1] -= 10
    self.button.setPosition(pos)
    self.button.setScale(1.0)
    self.hide()

# The application, a wrapper around Scene3D
class Application(events3d.EventHandler):
  def __init__(self):
    self.scene3d = module3d.Scene3D()
    self.scene3d.application = self
    self.app = self
    self.canHaveFocus = False
    self.children = []
    self.objects = []
    self.categories = {}
    self.currentCategory = None
    self.currentTask = None
    self.focusView = None
    self.focusObject = None
    self.focusGroup = None
    self.mouseDownObject = None
    self.enteredObject = None
    
    self.scene3d.startWindow()

  def start(self):
    #self.cursor = Object(self, mesh = "data/3dobjs/cursor.obj",
    #  texture = self.getThemeResource("images", "cursor.png"), position = [0, 0, 9.5])
    #self.cursor.mesh.setPickable(0);
    self.scene3d.update()
    self.callEvent("onStart", None)
    self.scene3d.startEventLoop()
    
  def stop(self):
    self.scene3d.shutdown()

  def isVisible(self):
    return True
    
  def setFocus(self, view = None):
    #print("setFocus", view)
    if self.focusView == view:
      return
      
    if not view:
      view = self
      
    if view.canHaveFocus:
      event = events3d.FocusEvent(self.focusView, view)
      
      if self.focusView:
        self.focusView.callEvent("onBlur", event)
        
      self.focusView = view
      self.focusView.callEvent("onFocus", event)
      self.focusObject = None
    else:
      event = events3d.FocusEvent(self.focusView, None)
      
      if self.focusView:
        self.focusView.callEvent("onBlur", event)
        
      self.focusView = None
      self.focusObject = None
    
  def switchTask(self, name):
    if self.currentTask:
      self.currentTask.hide()
      
    self.currentTask = self.currentCategory.tasksByName[name]
    #print("Switched task to ", name)
    
    if self.currentTask:
      self.currentTask.show()
    
  def switchCategory(self, name):
    # Do we need to switch at all
    if self.currentCategory and self.currentCategory.name ==  name:
      return
    
    # Does the category exist
    if not name in self.categories:
      return
      
    category = self.categories[name]
    
    # Does the category have at least one view
    if len(category.tasks) == 0:
      return
      
    if self.currentCategory:
      self.currentCategory.hide()
    
    self.currentCategory = category
    #print("Switched category to ", name)
    
    self.currentCategory.show()
    
    self.switchTask(category.tasks[0].name)
  
  '''
  Rules for mouse events:
  mousePressed -> Sent to the view under the mouse
  mouseDragged -> Sent to the view which received mousePressed
  mouseReleased -> Sent to the view which received mousePressed
  mouseClicked -> Sent to the view which received mousePressed if mouseReleased happened in the same view
  mouseEntered -> Sent to the view under the mouse, which has been entered
  mouseExited -> Sent to the view previously entered
  mouseMoved -> Sent to the view under the mouse
  
  mouseWheelMoved -> Sent to the view under the mouse or focussed view?
  '''
  
  # called from native
  def mouseDown(self, button, x, y):
    if button == 4:
      self.mouseWheel(1)
    elif button == 5:
      self.mouseWheel(-1)
    else:
      # Build event
      mousePos = self.scene3d.getMousePos2D()
      event = events3d.MouseEvent(button, mousePos[0], mousePos[1])
      
      # Get picked object
      object = self.scene3d.getPickedObject()[1]
      
      # If we have an object
      if object:
        # Try to give its view focus
        self.focusObject = object.object
        self.focusObject.view.setFocus()
        # It is the object which will receive the following mouse messages
        self.mouseDownObject = object.object
        # Send event to the object
        object.object.callEvent("onMouseDown", event)
    
  def mouseUp(self, button, x, y):
    if button == 4 or button == 5:
      return
    # Build event
    mousePos = self.scene3d.getMousePos2D()
    event = events3d.MouseEvent(button, mousePos[0], mousePos[1])
    
    # Get picked object
    object = self.scene3d.getPickedObject()[1]
    
    if self.mouseDownObject:
      self.mouseDownObject.callEvent("onMouseUp", event)
      if self.mouseDownObject is object.object:
        self.mouseDownObject.callEvent("onClicked", event)
      
  def mouseMove(self, mouseState, x, y, xRel, yRel):
    # Move cursor
    #mousePos = self.scene3d.getMousePosGUI()
    #self.cursor.setPosition([mousePos[0], mousePos[1], self.cursor.mesh.z])
    
    # Build event
    mousePos = self.scene3d.getMousePos2D()
    mouseDiff = self.scene3d.getMouseDiff()
    event = events3d.MouseEvent(self.scene3d.mouseState, mousePos[0], mousePos[1], mouseDiff[0], mouseDiff[1])
    
    # Get picked object
    picked = self.scene3d.getPickedObject()
    if not picked:
      #self.scene3d.redraw()
      return
    group = object = picked[0]
    object = picked[1]
    
    event.object = object
    event.group = group
      
    if self.scene3d.mouseState:
      if self.mouseDownObject:
        self.mouseDownObject.callEvent("onMouseDragged", event)
    else:
      if object and object.object:
        if self.enteredObject != object.object:
          if self.enteredObject:
            self.enteredObject.callEvent("onMouseExited", event)
          self.enteredObject = object.object
          self.enteredObject.callEvent("onMouseEntered", event)
        object.object.callEvent("onMouseMoved", event)
      #self.scene3d.redraw()
      
  def mouseWheel(self, wheelDelta):
    # Mouse wheel events, like key events are sent to the focus view
    mousePos = self.scene3d.getMousePos2D()
    event = events3d.MouseWheelEvent(wheelDelta)
    if self.focusView:
      self.focusView.callEvent("onMouseWheel", event)
    else:
      self.currentTask.callEvent("onMouseWheel", event)
    
  def keyDown(self, key, character, modifiers):
    if key == events3d.SDLK_TAB:
      if self.focusView:
        #if self.focusView.wantsTab and not (modifiers & events3d.KMOD_CTRL):
          index = self.focusView.parent.children.index(self.focusView)
          if modifiers & events3d.KMOD_SHIFT:
            if index > 0:
              self.focusView.parent.children[index - 1].setFocus()
            else:
              self.focusView.parent.children[len(self.focusView.parent.children) - 1].setFocus()
          else:
            if index + 1 < len(self.focusView.parent.children):
              self.focusView.parent.children[index + 1].setFocus()
            else:
              self.focusView.parent.children[0].setFocus()
          self.scene3d.redraw()
          return
    event = events3d.KeyEvent(key, character, modifiers)
    if self.focusView:
      self.focusView.callEvent("onKeyDown", event)
    else:
      self.currentTask.callEvent("onKeyDown", event)
    
  def keyUp(self, key, character, modifiers):
    event = events3d.KeyEvent(key, character, modifiers)
    if self.focusView:
      self.focusView.callEvent("onKeyUp", event)
    else:
      self.currentTask.callEvent("onKeyUp", event)

#Widgets

# Slider widget
class Slider(View):
  def __init__(self, parent, backgroundTexture, sliderTexture, focusedSliderTexture = None, position = [0, 0, 15], value = 0.0, min = 0.0, max = 1.0):
    View.__init__(self, parent)
    self.background = Object(self, "data/3dobjs/slider_background.obj",
      texture = backgroundTexture, position = position)
    self.slider = Object(self, "data/3dobjs/slider_cursor.obj",
      texture = sliderTexture, position = [position[0], position[1] + 35, position[2] + 0.01])
    self.sliderTexture = sliderTexture
    self.focusedSliderTexture = focusedSliderTexture
    self.sliderMinX = position[0] + 18;
    self.sliderMaxX = position[0] + 122;
    self.min = min
    self.max = max
    self.setValue(value)
    
  def setValue(self, value):
    self.__value = min(self.max, max(self.min, value))
    sliderPos = self.slider.getPosition()
    value = (self.__value - self.min) / (self.max - self.min) 
    sliderPos[0] = value * (self.sliderMaxX - self.sliderMinX) + self.sliderMinX
    self.slider.setPosition(sliderPos)
    
  def getValue(self):
    return self.__value
  
  def onMouseDragged(self, event):
    sliderPos = self.slider.getPosition()
    screenPos = mh.cameras[1].convertToScreen(sliderPos[0], sliderPos[1], sliderPos[2])
    worldPos = mh.cameras[1].convertToWorld3D(event.x, event.y, screenPos[2])
    sliderPos[0] = min(self.sliderMaxX, max(self.sliderMinX, worldPos[0]))
    self.slider.setPosition(sliderPos)
    
  def onMouseUp(self, event):
    sliderPos = self.slider.getPosition()
    screenPos = mh.cameras[1].convertToScreen(sliderPos[0], sliderPos[1], sliderPos[2])
    worldPos = mh.cameras[1].convertToWorld3D(event.x, event.y, screenPos[2])
    sliderPos[0] = min(self.sliderMaxX, max(self.sliderMinX, worldPos[0]))
    self.slider.setPosition(sliderPos)
    value = (sliderPos[0] - self.sliderMinX) / (self.sliderMaxX - self.sliderMinX)
    self.__value = value * (self.max - self.min) + self.min
    #print(value, self.__value)
    self.callEvent("onChange", self.__value)
    
  def onKeyDown(self, event):
    oldValue = self.__value
    newValue = self.__value
    
    if event.key == events3d.SDLK_HOME:
      newValue = 0.0
    elif event.key == events3d.SDLK_LEFT:
      newValue -= 0.1
    elif event.key == events3d.SDLK_RIGHT:
      newValue += 0.1
    elif event.key == events3d.SDLK_END:
      newValue = 1.0
    else:
      View.onKeyDown(self, event)
      
    if oldValue != newValue:
      self.setValue(newValue)
      if oldValue != self.__value:
        self.callEvent("onChange", self.__value)
        
  def onFocus(self, event):
    if self.focusedSliderTexture:
      self.slider.setTexture(self.focusedSliderTexture)
  
  def onBlur(self, event):
    if self.focusedSliderTexture:
      self.slider.setTexture(self.sliderTexture)

# Button widget
class Button(View):
  def __init__(self, parent, mesh = "data/3dobjs/button_gender.obj", texture = None,
    selectedTexture = None, position = [0, 0, 9], selected = False):
    View.__init__(self, parent)
    if selectedTexture and selected:
      t = selectedTexture
    else:
      t = texture
    self.button = Object(self, mesh, texture = t, position = position)
    self.texture = texture
    self.selectedTexture = selectedTexture
    self.selected = selected
    
  def setTexture(self, texture):
    self.texture = texture
    self.button.setTexture(texture)
    
  def onMouseDown(self, event):
    self.setSelected(True)
    
  def onMouseUp(self, event):
    self.setSelected(False)
    
  def onKeyDown(self, event):
    if event.key == events3d.SDLK_RETURN or event.key == events3d.SDLK_KP_ENTER:
      self.setSelected(True)
      self.app.scene3d.redraw()
    else:
      View.onKeyDown(self, event)
      
  def onKeyUp(self, event):
    if event.key == events3d.SDLK_RETURN or event.key == events3d.SDLK_KP_ENTER:
      self.setSelected(False)
      self.callEvent("onClicked", event)
      self.app.scene3d.redraw()
      
  def setSelected(self, selected):
    #print("(de)selecting", self.selected, selected)
    if self.selected != selected:
      self.selected = selected
      self.onSelected(selected)
    
  def onSelected(self, selected):
    if selected and self.selectedTexture:
      self.button.setTexture(self.selectedTexture)
    else:
      self.button.setTexture(self.texture)

# RadioButton widget
class RadioButton(Button):
  def __init__(self, parent, group, mesh = "data/3dobjs/button_gender.obj",
      texture = None, selectedTexture = None, position = [0, 0, 9], selected = False):
    Button.__init__(self, parent, mesh, texture, selectedTexture, position, selected)
    self.group = group
    self.group.append(self)
    
  def onClicked(self, event):
      self.setSelected(True)
    
  def setSelected(self, selected):
    if selected:
      for radio in self.group:
        if radio.selected and radio != self:
          radio.setSelected(False)
    Button.setSelected(self, selected)
    
  def onSelected(self, selected):
    if selected and self.selectedTexture:
      self.button.setTexture(self.selectedTexture)
    else:
      self.button.setTexture(self.texture)
      
# ToggleButton widget
class ToggleButton(Button):
  def __init__(self, parent, mesh = "data/3dobjs/button_gender.obj",
      texture = None, selectedTexture = None, position = [0, 0, 9], selected = False):
    Button.__init__(self, parent, mesh, texture, selectedTexture, position, selected)
    
  def onClicked(self, event):
    if self.selected:
      self.setSelected(False)
    else:
      self.setSelected(True)
  
  def onMouseDown(self, event):
    pass
    
  def onMouseUp(self, event):
    pass

# ToolbarButton widget (unused)
class ToolbarButton(RadioButton):
  def __init__(self, parent, group, texture = None, position = [0, 0, 9]):
    RadioButton.__init__(self, parent, texture, None, position)
    
  def onSelected(self, selected):
    if selected:
      self.button.setScale(1.5)
    else:
      self.button.setScale(1.0)
      
class ProgressBar(View):
  """
  A ProgressBar widget. This widget can be used to show the user the progress of a 
  lengthy operation.
  """
  
  def __init__(self, parent, backgroundMesh = "data/3dobjs/progressbar_background.obj",
    backgroundTexture = None,
    backgroundPosition = [300, 520, 9.1],
    barMesh = "data/3dobjs/progressbar.obj",
    barTexture = None,
    barPosition = [300, 520, 9.2], visible = True):
    """
    This is the constructor method for the ProgressBar class. It initializes the
    following attributes:

    - **self.scene**: *scene reference*. The scene the widget is part of.
    - **self.backgroundMesh**: *String*. The background object.
    - **self.backgroundTexture**: *String*. The background texture.
    - **self.barMesh**: *String*. The bar object.
    - **self.barTexture**: *String*. The bar texture.
    """
    
    View.__init__(self, parent, visible)
    self.background = Object(self, backgroundMesh, texture = backgroundTexture, position = backgroundPosition)
    self.bar = Object(self, barMesh, texture = barTexture, position = barPosition)
    self.bar.mesh.setScale(0.0, 1.0, 1.0);

  def setProgress(self, progress, redraw = 1):
    """
    This method updates the progress and optionally updates the screen

    Parameters
    ----------

    progress:
        *float* The progress from 0.0 to 1.0.
    redraw:
        *int* 1 if a redraw is needed, 0 otherwise.
    """
    
    self.bar.mesh.setScale(progress, 1.0, 1.0);
    if redraw:
      self.app.scene3d.redraw(0)

# TextView widget
class TextView(View):
  def __init__(self, parent, mesh = "data/3dobjs/empty.obj", texture = None, position = [0, 0, 9]):
    View.__init__(self, parent)
    self.object = Object(self, mesh, texture = texture, position = position)
    
  def setText(self, text):
    self.object.setText(text)
    
# TextEdit widget
class TextEdit(View):
  def __init__(self, parent, mesh = "data/3dobjs/empty.obj", texture = None, position = [0, 0, 9]):
    View.__init__(self, parent)
    Object(self, mesh = "data/3dobjs/backgroundedit.obj", position = position)
    self.textObject = Object(self, mesh, texture = texture, position = [position[0] + 10.0, position[1] + 12.0, position[2] + 0.1])
    self.text = ""
    
  def __updateTextObject(self):
    lenText = len(self.text)
    if lenText > 100:
        text = self.text[(lenText-100):]
    else:
        text = self.text
    self.textObject.setText(text)
    
  def setText(self, text):
    self.text = text
    self.__updateTextObject()
    
  def getText(self):
    self.textObject.getText()
    
  def onKeyDown(self, event):
    if event.modifiers & events3d.KMOD_CTRL:
      View.onKeyDown(self, event)
      return
    print(event)
    if event.key == events3d.SDLK_BACKSPACE:
      self.text = self.text[:-1]
    elif event.key == events3d.SDLK_RETURN:
      if len(self.text):
        pass
        #self.onFileSelected(self.text)
      return
    elif event.key < 256:
      self.text += event.character     
        
    self.__updateTextObject()
    self.app.scene3d.redraw()

# FileEntryView widget
class FileEntryView(View):
  def __init__(self, parent):
    View.__init__(self, parent)
    
    Object(self, mesh = "data/3dobjs/fileselectorbar.obj", position = [0.0, 0.30, 9])
    Object(self, mesh = "data/3dobjs/backgroundtext.obj", position = [200, 80, 5.5])
    self.textObject = Object(self, mesh = "data/3dobjs/empty.obj", position = [210, 95, 5.6])
    self.bConfirm = Object(self, mesh = "data/3dobjs/button_confirm.obj",
      texture = self.app.getThemeResource("images", "button_confirm.png"), position = [610, 70, 9.1])
    self.text = ""
    
    @self.bConfirm.event
    def onClicked(event):
      if len(self.text):
        self.onFileSelected(self.text)
      
  def onKeyDown(self, event):
    if event.modifiers & events3d.KMOD_CTRL:
      View.onKeyDown(self, event)
      return
    #print(event)
    if event.key == 8:
      self.text = self.text[:-1]
    elif event.key == 13:
      if len(self.text):
        self.onFileSelected(self.text)
      return
    elif event.key < 256 and event.key != 13:
      self.text += event.character     
        
    lenText = len(self.text)
    if lenText > 100:
        textToVisualize = self.text[(lenText-100):]
    else:
        textToVisualize = self.text
    self.textObject.setText(textToVisualize)    
    self.app.scene3d.redraw()
    

# FileChooser widget
class FileChooser(View):
  def __init__(self, parent, path, extension, previewExtension = "bmp"):
    View.__init__(self, parent)
    
    self.currentPos = [400, 300, 0]
    self.nextPos = [550, 250, 0]
    self.previousPos = [250, 250, 0]
    self.currentFile = Object(self, mesh = "data/3dobjs/file.obj", position = self.currentPos, visible = False)
    self.nextFile = Object(self, mesh = "data/3dobjs/nextfile.obj", position = self.nextPos, visible = False)
    self.previousFile = Object(self, mesh = "data/3dobjs/previousfile.obj", position = self.previousPos, visible = False)
    self.filename = Object(self, mesh = "data/3dobjs/empty.obj", position = [330, 390, 0], visible = False)
    self.path = path
    self.extension = extension
    self.previewExtension = previewExtension
    self.files = None
    self.selectedFile = 0
    
    self.nextFileAnimation = animation3d.Timeline(0.25)
    self.nextFileAnimation.append(animation3d.PathAction(self.currentFile.mesh, [self.currentPos, self.previousPos]))
    self.nextFileAnimation.append(animation3d.ScaleAction(self.currentFile.mesh, [1.5, 1.5, 1.5], [1.0, 1.0, 1.0]))
    self.nextFileAnimation.append(animation3d.PathAction(self.nextFile.mesh, [self.nextPos, self.currentPos]))
    self.nextFileAnimation.append(animation3d.ScaleAction(self.nextFile.mesh, [1.0, 1.0, 1.0], [1.5, 1.5, 1.5]))
    self.nextFileAnimation.append(animation3d.UpdateAction(self.app.scene3d))
    
    self.previousFileAnimation = animation3d.Timeline(0.25)
    self.previousFileAnimation.append(animation3d.PathAction(self.previousFile.mesh, [self.previousPos, self.currentPos]))
    self.previousFileAnimation.append(animation3d.ScaleAction(self.previousFile.mesh, [1.0, 1.0, 1.0], [1.5, 1.5, 1.5]))
    self.previousFileAnimation.append(animation3d.PathAction(self.currentFile.mesh, [self.currentPos, self.nextPos]))
    self.previousFileAnimation.append(animation3d.ScaleAction(self.currentFile.mesh, [1.5, 1.5, 1.5], [1.0, 1.0, 1.0]))
    self.previousFileAnimation.append(animation3d.UpdateAction(self.app.scene3d))
    
    @self.previousFile.event
    def onClicked(event):
      self.goPrevious()

    @self.currentFile.event
    def onClicked(event):
      self.onFileSelected(self.files[self.selectedFile])
      
    @self.nextFile.event
    def onClicked(event):
      self.goNext()
      
  def getPreview(self, filename):
    preview = filename
    if self.previewExtension:
      preview = filename.replace(os.path.splitext(filename)[-1], "." + self.previewExtension)
    return preview
    
  def updateText(self):
    text = self.files[self.selectedFile]
    text = text.replace(os.path.splitext(text)[-1], "")
    self.filename.setText(text)
    
  def onShow(self, event):
    self.files = []
    if type(self.extension) is types.StringType:
      for f in os.listdir(self.path):
          if f.endswith("." + self.extension):
              self.files.append(f)
    elif type(self.extension) is types.ListType:
      for f in os.listdir(self.path):
          for ext in self.extension:
              if f.endswith("." + ext):
                  self.files.append(f)
    self.selectedFile = 0
    
    self.currentFile.setScale(1.5);
    
    self.previousFile.clearTexture()
    self.previousFile.hide()
    
    if self.selectedFile < len(self.files):
        self.currentFile.setTexture(self.path + "/" + self.getPreview(self.files[self.selectedFile]))
        self.updateText()
        self.currentFile.show()
        self.filename.show()
    else:
        self.currentFile.clearTexture()
        self.currentFile.hide()
        self.filename.hide()
    
    if self.selectedFile + 1 < len(self.files):
        self.nextFile.setTexture(self.path + "/" + self.getPreview(self.files[self.selectedFile + 1]))
        self.nextFile.show()
    else:
        self.nextFile.clearTexture()
        self.nextFile.hide()
            
    self.app.scene3d.redraw()
    
  def onKeyDown(self, event):
    if event.modifiers & events3d.KMOD_CTRL:
      View.onKeyDown(self, event)
      return
    if event.key == 276:
      self.goPrevious()
    elif event.key == 275:
      self.goNext()
    elif event.key == 271 or event.key == 13:
      self.onFileSelected(self.files[self.selectedFile])
      
  def goPrevious(self):
    if self.selectedFile == 0:
      return
        
    # Start animation by hiding the next file
    self.nextFile.hide()
    
    # Animate by moving previous and current file to current and next locations
    self.previousFileAnimation.start()
    
    # End animation by resetting positions and showing new configuration
    self.previousFile.setPosition(self.previousPos)
    self.previousFile.setScale(1.0)
    self.currentFile.setPosition(self.currentPos)
    self.currentFile.setScale(1.5)
        
    self.selectedFile -= 1
    
    if self.selectedFile - 1 >= 0:
        self.previousFile.setTexture(self.path + "/" + self.getPreview(self.files[self.selectedFile - 1]))
        self.previousFile.show()
    else:
        self.previousFile.clearTexture()
        self.previousFile.hide()
    
    self.currentFile.setTexture(self.path + "/" + self.getPreview(self.files[self.selectedFile]))
    self.updateText()
    self.currentFile.show()
    self.nextFile.setTexture(self.path + "/" + self.getPreview(self.files[self.selectedFile + 1]))
    self.nextFile.show()
    
    self.app.scene3d.redraw()
    
  def goNext(self):
    if self.selectedFile + 1 == len(self.files):
      return
        
    # Start animation by hiding the previous file
    self.previousFile.hide()
    
    # Animate by moving current and next file to previous and current locations
    self.nextFileAnimation.start()
    
    # End animation by resetting positions and showing new configuration
    self.currentFile.setPosition(self.currentPos)
    self.currentFile.setScale(1.5)
    self.nextFile.setPosition(self.nextPos)
    self.nextFile.setScale(1.0)
    
    self.selectedFile += 1
    
    self.previousFile.setTexture(self.path + "/" + self.getPreview(self.files[self.selectedFile - 1]))
    self.previousFile.show()
    self.currentFile.setTexture(self.path + "/" + self.getPreview(self.files[self.selectedFile]))
    self.updateText()
    self.currentFile.show()
    
    if self.selectedFile + 1 < len(self.files):
        self.nextFile.setTexture(self.path + "/" + self.getPreview(self.files[self.selectedFile + 1]))
        self.nextFile.show()
    else:
        self.nextFile.clearTexture()
        self.nextFile.hide()
        
    self.app.scene3d.redraw()
