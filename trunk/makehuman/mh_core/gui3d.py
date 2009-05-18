import events3d, files3d, animation3d, module3d
import os

# Wrapper around Object3D
class Object(events3d.EventHandler):
  def __init__(self, view, mesh, texture = None, position = [0, 0, 9], camera = 0, shadeless = 1, visible = True):
    self.app = view.app
    self.view = view
    self.mesh = files3d.loadMesh(self.app.scene3d, mesh, 0, position[0], position[1], position[2])
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
    print("Created object with mesh ", mesh, texture, position)
    
  def show(self):
    self.visible = True
    self.setVisibility(True)
    
  def hide(self):
    print("hiding ", self.meshName)
    self.visible = False
    self.setVisibility(False)
  
  def getPosition(self):
    return [self.mesh.x, self.mesh.y, self.mesh.z]
  
  def setPosition(self, position):
    self.mesh.setLoc(position[0], position[1], position[2])
    
  def setTexture(self, texture):
    self.mesh.setTexture(texture)
    
  def clearTexture(self):
    self.mesh.clearTexture()
  
  def setVisibility(self, visibility):
    print("changing visibility of ", self.meshName, "to", self.view.isVisible() and self.visible and visibility)
    if self.view.isVisible() and self.visible and visibility:
      self.mesh.setVisibility(1)
    else:
      self.mesh.setVisibility(0)
    
  def setScale(self, scale):
    self.mesh.setScale(scale, scale, 1)
    
  def setText(self, text):
    self.mesh.setText(text)
    
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
    self.button = Object(self.parent, "data/3dobjs/button_home.obj",
      texture = texture, position = [-0.5 + len(self.parent.tasks) * 0.1, -0.39, 9])
    
    category.tasks.append(self)
    category.tasksByName[self.name] = self
    
    @self.button.event
    def onClicked(event):
      self.app.switchTask(self.name)

  def onShow(self, event):
    print("onShow", self.name, event)
    pos = self.button.getPosition()
    pos[1] += 0.01
    self.button.setPosition(pos)
    self.button.setScale(1.5)
    self.show()
    
  def onHide(self, event):
    print("onHide", self.name, event)
    pos = self.button.getPosition()
    pos[1] -= 0.01
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
    self.button = Object(self.parent, "data/3dobjs/button_about.obj",
      position = [-0.5 + len(self.app.categories) * 0.1, 0.39, 9], texture = texture)
      
    parent.categories[name] = self
    
    @self.button.event
    def onClicked(event):
      self.app.switchCategory(self.name)
      
  def onShow(self, event):
    pos = self.button.getPosition()
    pos[1] -= 0.01
    self.button.setPosition(pos)
    self.button.setScale(1.5)
    self.show()
    
  def onHide(self, event):
    pos = self.button.getPosition()
    pos[1] += 0.01
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
    self.cursor = Object(self, mesh = "data/3dobjs/cursor.obj",
      texture = "data/images/cursor.png", position = [0, 0, 9.5])
    self.cursor.mesh.setPickable(0);
    self.scene3d.update()
    self.callEvent("onStart", None)
    self.scene3d.startEventLoop()
    
  def stop(self):
    self.scene3d.shutdown()

  def isVisible(self):
    return True
    
  def setFocus(self, view = None):
    if not view:
      view = self
      
    if (self.focusView != view) and view.canHaveFocus:
      if self.focusView:
        self.focusView.callEvent("onBlur", None)
        
      self.focusView = view
      self.focusView.callEvent("onFocus", None)
      self.focusObject = None
    else:
      if self.focusView:
        self.focusView.callEvent("onBlur", None)
        
      self.focusView = None
      self.focusObject = None
    
  def switchTask(self, name):
    if self.currentTask:
      self.currentTask.hide()
      
    self.currentTask = self.currentCategory.tasksByName[name]
    print("Switched task to ", name)
    
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
    print("Switched category to ", name)
    
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
      mouseDiff = self.scene3d.getMouseDiff()
      event = events3d.Event(mousePos[0], mousePos[1], mouseDiff[0], mouseDiff[1], button)
      
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
    mouseDiff = self.scene3d.getMouseDiff()
    event = events3d.Event(mousePos[0], mousePos[1], mouseDiff[0], mouseDiff[1], button)
    
    # Get picked object
    object = self.scene3d.getPickedObject()[1]
    
    if self.mouseDownObject:
      self.mouseDownObject.callEvent("onMouseUp", event)
      if self.mouseDownObject is object.object:
        self.mouseDownObject.callEvent("onClicked", event)
      
  def mouseMove(self, mouseState, x, y, xRel, yRel):
    # Move cursor
    mousePos = self.scene3d.getMousePosGUI()
    self.cursor.setPosition([mousePos[0], mousePos[1], self.cursor.mesh.z])
    
    # Build event
    mousePos = self.scene3d.getMousePos2D()
    mouseDiff = self.scene3d.getMouseDiff()
    event = events3d.Event(mousePos[0], mousePos[1], mouseDiff[0], mouseDiff[1], self.scene3d.mouseState)
    
    # Get picked object
    group = object = self.scene3d.getPickedObject()[0]
    object = self.scene3d.getPickedObject()[1]
    
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
      self.scene3d.redraw()
      
  def mouseWheel(self, wheelDelta):
    # Mouse wheel events, like key events are sent to the focus view
    mousePos = self.scene3d.getMousePos2D()
    event = events3d.Event(mousePos[0], mousePos[1], wheelDelta = wheelDelta)
    if self.focusView:
      self.focusView.callEvent("onMouseWheel", event)
    else:
      self.currentTask.callEvent("onMouseWheel", event)
    
  def keyDown(self, key, character):
    event = events3d.Event(key = self.scene3d.keyPressed, character = self.scene3d.characterPressed)
    if self.focusView:
      self.focusView.callEvent("onKeyDown", event)
    else:
      self.currentTask.callEvent("onKeyDown", event)
    
  def keyUp(self, key, character):
    event = events3d.Event(key = self.scene3d.keyPressed, character = self.scene3d.characterPressed)
    if self.focusView:
      self.focusView.callEvent("onKeyUp", event)
    else:
      self.currentTask.callEvent("onKeyDown", event)

#Widgets

# Slider widget
class Slider(View):
  def __init__(self, parent, backgroundTexture, sliderTexture, position = [0, 0, 9], value = 0.0):
    View.__init__(self, parent)
    self.background = Object(self, "data/3dobjs/button_gender.obj",
      texture = backgroundTexture, position = position)
    self.slider = Object(self, "data/3dobjs/button_about.obj",
      texture = sliderTexture, position = [position[0], position[1], position[2] + 0.01])
    self.sliderMinX = -0.5;
    self.sliderMaxX = -0.39;
    self.setValue(value)
    
  def setValue(self, value):
    self.__value = min(1, max(0, value))
    sliderPos = self.slider.getPosition()
    sliderPos[0] = self.__value * (self.sliderMaxX - self.sliderMinX) + self.sliderMinX
    self.slider.setPosition(sliderPos)
    
  def getValue(self):
    return self.__value
  
  def onMouseDragged(self, event):
    sliderPos = self.slider.getPosition()
    screenPos = self.app.scene3d.convertToScreen(sliderPos[0], sliderPos[1], sliderPos[2])
    worldPos = self.app.scene3d.convertToWorld3D(event.x, event.y, screenPos[2])
    sliderPos[0] = min(self.sliderMaxX, max(self.sliderMinX, worldPos[0]))
    self.slider.setPosition(sliderPos)
    
  def onMouseUp(self, event):
    sliderPos = self.slider.getPosition()
    screenPos = self.app.scene3d.convertToScreen(sliderPos[0], sliderPos[1], sliderPos[2])
    worldPos = self.app.scene3d.convertToWorld3D(event.x, event.y, screenPos[2])
    sliderPos[0] = min(self.sliderMaxX, max(self.sliderMinX, worldPos[0]))
    self.slider.setPosition(sliderPos)
    self.value = (sliderPos[0] - self.sliderMinX) / (self.sliderMaxX - self.sliderMinX)
    print(self.value)
    self.callEvent("onChange", self.value)
    
  def onKeyDown(self, event):
    oldValue = self.__value
    newValue = self.__value
    
    if event.key == events3d.SDLK_HOME:
      newValue = 0.0
    if event.key == events3d.SDLK_LEFT:
      newValue -= 0.1
    elif event.key == events3d.SDLK_RIGHT:
      newValue += 0.1
    if event.key == events3d.SDLK_END:
      newValue = 1.0
      
    if oldValue != newValue:
      self.setValue(newValue)
      if oldValue != self.__value:
        self.callEvent("onChange", self.__value)

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
    
  def onMouseDown(self, event):
    self.setSelected(True)
    
  def onMouseUp(self, event):
    self.setSelected(False)
      
  def setSelected(self, selected):
    print("(de)selecting", self.selected, selected)
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

# ToolbarButton widget (unused)
class ToolbarButton(RadioButton):
  def __init__(self, parent, group, texture = None, position = [0, 0, 9]):
    RadioButton.__init__(self, parent, texture, None, position)
    
  def onSelected(self, selected):
    if selected:
      self.button.setScale(1.5)
    else:
      self.button.setScale(1.0)

# FileEntryView widget
class FileEntryView(View):
  def __init__(self, parent):
    View.__init__(self, parent)
    
    Object(self, mesh = "data/3dobjs/fileselectorbar.obj", position = [0.0, 0.30, 9])
    Object(self, mesh = "data/3dobjs/backgroundtext.obj", position = [0.0, 1.3, 5.5])
    self.textObject = Object(self, mesh = "data/3dobjs/empty.obj", position = [-0.3, 0.29, 6])
    self.bConfirm = Object(self, mesh = "data/3dobjs/button_confirm.obj",
      texture = "data/images/button_confirm.png", position = [0.35, 0.28, 9.1])
    self.text = ""
    
    @self.bConfirm.event
    def onClicked(event):
      if len(self.text):
        self.onFileSelected(self.text)
      
  def onKeyDown(self, event):
    print(event)
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
  def __init__(self, parent, extension):
    View.__init__(self, parent)
    
    self.currentFile = Object(self, mesh = "data/3dobjs/file.obj", position = [0, 0, 0], visible = False)
    self.nextFile = Object(self, mesh = "data/3dobjs/nextfile.obj", position = [3.0, 0.5, 0], visible = False)
    self.previousFile = Object(self, mesh = "data/3dobjs/previousfile.obj", position = [-3.0, 0.5, 0], visible = False)
    self.filename = Object(self, mesh = "data/3dobjs/empty.obj", position = [-0.5, -0.7, 0], visible = False)
    self.extension = extension
    self.files = None
    self.selectedFile = 0
    
    self.nextFileAnimation = animation3d.Timeline(0.25)
    self.nextFileAnimation.append(animation3d.PathAction(self.currentFile.mesh, [[0, 0, 0], [-3.0, 0.5, 0]]))
    self.nextFileAnimation.append(animation3d.ScaleAction(self.currentFile.mesh, [1.5, 1.5, 1.5], [1.0, 1.0, 1.0]))
    self.nextFileAnimation.append(animation3d.PathAction(self.nextFile.mesh, [[3.0, 0.5, 0], [0, 0, 0]]))
    self.nextFileAnimation.append(animation3d.ScaleAction(self.nextFile.mesh, [1.0, 1.0, 1.0], [1.5, 1.5, 1.5]))
    self.nextFileAnimation.append(animation3d.UpdateAction(self.app.scene3d))
    
    self.previousFileAnimation = animation3d.Timeline(0.25)
    self.previousFileAnimation.append(animation3d.PathAction(self.previousFile.mesh, [[-3.0, 0.5, 0], [0, 0, 0]]))
    self.previousFileAnimation.append(animation3d.ScaleAction(self.previousFile.mesh, [1.0, 1.0, 1.0], [1.5, 1.5, 1.5]))
    self.previousFileAnimation.append(animation3d.PathAction(self.currentFile.mesh, [[0, 0, 0], [3.0, 0.5, 0],]))
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
    
  def onShow(self, event):
    self.files = []
    for f in os.listdir("models"):
        if os.path.splitext(f)[-1] == "." + self.extension:
            self.files.append(f)
    self.selectedFile = 0
    
    self.currentFile.setScale(1.5);
    
    self.previousFile.clearTexture()
    self.previousFile.hide()
    
    if self.selectedFile < len(self.files):
        self.currentFile.setTexture("models/" + self.files[self.selectedFile].replace(self.extension, 'bmp'))
        self.filename.setText(self.files[self.selectedFile].replace("." + self.extension, ""))
        self.currentFile.show()
        self.filename.show()
    else:
        self.currentFile.clearTexture()
        self.currentFile.hide()
        self.filename.hide()
    
    if self.selectedFile + 1 < len(self.files):
        self.nextFile.setTexture("models/" + self.files[self.selectedFile + 1].replace(self.extension, 'bmp'))
        self.nextFile.show()
    else:
        self.nextFile.clearTexture()
        self.nextFile.hide()
            
    self.app.scene3d.redraw()
    
  def onKeyDown(self, event):
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
    self.previousFile.setPosition([-3.0, 0.5, 0])
    self.previousFile.setScale(1.0)
    self.currentFile.setPosition([0, 0, 0])
    self.currentFile.setScale(1.5)
        
    self.selectedFile -= 1
    
    if self.selectedFile - 1 >= 0:
        self.previousFile.setTexture("models/" + self.files[self.selectedFile - 1].replace(self.extension, 'bmp'))
        self.previousFile.show()
    else:
        self.previousFile.clearTexture()
        self.previousFile.hide()
    
    self.currentFile.setTexture("models/" + self.files[self.selectedFile].replace(self.extension, 'bmp'))
    self.filename.setText(self.files[self.selectedFile].replace("." + self.extension, ""))
    self.currentFile.show()
    self.nextFile.setTexture("models/" + self.files[self.selectedFile + 1].replace(self.extension, 'bmp'))
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
    self.currentFile.setPosition([0, 0, 0])
    self.currentFile.setScale(1.5)
    self.nextFile.setPosition([3.0, 0.5, 0])
    self.nextFile.setScale(1.0)
    
    self.selectedFile += 1
    
    self.previousFile.setTexture("models/" + self.files[self.selectedFile - 1].replace(self.extension, 'bmp'))
    self.previousFile.show()
    self.currentFile.setTexture("models/" + self.files[self.selectedFile].replace(self.extension, 'bmp'))
    self.filename.setText(self.files[self.selectedFile].replace("." + self.extension, ""))
    self.currentFile.show()
    
    if self.selectedFile + 1 < len(self.files):
        self.nextFile.setTexture("models/" + self.files[self.selectedFile + 1].replace(self.extension, 'bmp'))
        self.nextFile.show()
    else:
        self.nextFile.clearTexture()
        self.nextFile.hide()
        
    self.app.scene3d.redraw()
