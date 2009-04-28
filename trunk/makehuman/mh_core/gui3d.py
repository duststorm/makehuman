import events3d, files3d, animation3d, module3d
import os

# Wrapper around Object3D
class Object(events3d.EventHandler):
  def __init__(self, view, mesh, texture = None, position = [0, 0, 9], camera = 0, shadeless = 1, visible = True):
    self.scene = view.scene
    self.view = view
    self.mesh = files3d.loadMesh(self.scene.scene3d, mesh, 0, position[0], position[1], position[2])
    if texture:
      self.texture = texture
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
    if self.view.isVisible() and self.visible and visibility:
      self.mesh.setVisibility(1)
    else:
      self.mesh.setVisibility(0)
    
  def setScale(self, scale):
    self.mesh.setScale(scale, scale, 1)
    
  def setText(self, text):
    self.mesh.setText(text)

# Generic view
class View(events3d.EventHandler):
  def __init__(self, parent = None, visible = True):
    self.scene = parent.scene
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
    self.scene.setFocus(self)
    
  def hasFocus(self):
    return self.scene.focusView is self
      
  def __updateVisibility(self):
    previousVisibility = self.__totalVisibility
    if self.parent:
      self.__totalVisibility = self.parent.isVisible() and self.__visible
    else:
      self.__totalVisibility = self.__visible
    if self.__totalVisibility:
      for o in self.objects:
        o.setVisibility(1)
    else:
      for o in self.objects:
        o.setVisibility(0)
    for v in self.children:
      v.__updateVisibility()
      
    if self.__totalVisibility != previousVisibility:
      if self.__totalVisibility:
        self.callEvent("onShow", None)
      else:
        self.callEvent("onHide", None)

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
    def onClick(event):
      self.scene.switchTask(self.name)

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
      position = [-0.5 + len(self.scene.categories) * 0.1, 0.39, 9], texture = texture)
      
    parent.categories[name] = self
    
    @self.button.event
    def onClick(event):
      self.scene.switchCategory(self.name)
      
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
    self.scene = self
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
    
    self.scene3d.startWindow()
    
    self.scene3d.connect("LMOUSEP", self.lMouseDown)
    self.scene3d.connect("LMOUSER", self.lMouseUp)
    self.scene3d.connect("MOUSEWHEELDOWN", self.mouseWheelDown)
    self.scene3d.connect("MOUSEWHEELUP", self.mouseWheelUp)
    self.scene3d.connect("MOTION", self.mouseMove)
    self.scene3d.connect("PMOTION", self.mouseMove)
    self.scene3d.connect("KEYBOARD", self.keyDown)

  def start(self):
    self.cursor = Object(self, mesh = "data/3dobjs/cursor.obj",
      texture = "data/images/cursor.png", position = [0, 0, 9.5])
    self.scene3d.update()
    self.scene3d.startEventLoop()
    
  def stop(self):
    self.scene3d.shutdown()
    
  def lMouseDown(self):
    self.mouseDown(1)
  def lMouseUp(self):
    self.mouseUp(1)
  def mouseWheelDown(self):
    self.mouseWheel(-1)
  def mouseWheelUp(self):
    self.mouseWheel(1)

  def isVisible(self):
    return True
    
  def setFocus(self, view = None):
    if not view:
      view = self
    if self.focusView is not view and view.canHaveFocus:
      print("focussing ", view)
      if self.focusView:
        self.focusView.callEvent("onBlur", None)
      self.focusView = view
      self.focusView.callEvent("onFocus", None)
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
    
  def callPropagatedEvent(self, eventType, event):
    self.callEvent(eventType, event)
    if self.currentTask:
      self.currentTask.callEvent(eventType, event)
      
    if self.focusView:
      print("Sending", eventType, "to", self.focusView)
      self.focusView.callEvent(eventType, event)
    elif self.currentCategory:
      self.currentCategory.callEvent(eventType, event)
      
    if self.focusObject:
      print("Sending", eventType, "to", self.focusObject)
      self.focusObject.callEvent(eventType, event)
      
  # called from native
  def mouseDown(self, b):
    mousePos = self.scene3d.getMousePos2D()
    object = self.scene3d.getPickedObject()[1]
    if object:
      self.focusObject = object.object
      self.focusView = self.focusObject.view
    else:
      self.focusObject = None
    self.mouseDownObject = self.focusObject
    
    event = events3d.Event(mousePos[0], mousePos[1], b)
    self.callPropagatedEvent("onMouseDown", event)
    
    # Set focus to clicked view
    if self.mouseDownObject and self.mouseDownObject.view:
      self.mouseDownObject.view.setFocus()
    
  def mouseUp(self, b):
    mousePos = self.scene3d.getMousePos2D()
    object = self.scene3d.getPickedObject()[1]
    if object:
      self.focusObject = object.object
    else:
      self.focusObject = None
    
    event = events3d.Event(mousePos[0], mousePos[1], b)
    self.callPropagatedEvent("onMouseUp", event)
    if self.mouseDownObject and self.mouseDownObject is self.focusObject:
      self.mouseDownObject.view.callEvent("onClick", event)
      self.mouseDownObject.callEvent("onClick", event)
      
  def mouseWheel(self, wheelDelta):
    mousePos = self.scene3d.getMousePos2D()
    event = events3d.Event(mousePos[0], mousePos[1], wheelDelta = wheelDelta)
    self.callPropagatedEvent("onMouseWheel", event)
      
  def mouseMove(self):
    mousePos = self.scene3d.getMousePosGUI()
    self.cursor.setPosition([mousePos[0], mousePos[1], self.cursor.mesh.z])
      
    if self.scene3d.mouseState:
      mousePos = self.scene3d.getMousePos2D()
      object = self.scene3d.getPickedObject()[1]
      if object:
        self.focusObject = object.object
      else:
        self.focusObject = None
      event = events3d.Event(mousePos[0], mousePos[1], self.scene3d.mouseState)
      self.callPropagatedEvent("onMouseMove", event)
    else:
      self.scene3d.redraw()
    
  def keyDown(self):
    event = events3d.Event(key = self.scene3d.keyPressed, character = self.scene3d.characterPressed)
    self.callPropagatedEvent("onKeyDown", event)

#Widgets

# Slider widget
class Slider(View):
  def __init__(self, parent, backgroundTexture, sliderTexture, position = [0, 0, 9], value = 0.0):
    View.__init__(self, parent)
    self.background = Object(self, "data/3dobjs/button_gender.obj",
      texture = backgroundTexture, position = position)
    self.slider = Object(self, "data/3dobjs/button_about.obj",
      texture = sliderTexture, position = [position[0], position[1], position[2] + 0.1])
    self.setValue(value)
    
  def setValue(self, value):
    self.__value = min(1, max(0, value))
    sliderPos = self.slider.getPosition()
    sliderPos[0] = self.__value * (0.45 - 0.365) - 0.45
    self.slider.setPosition(sliderPos)
    
  def getValue(self, value):
    return self.__value
  
  def onMouseMove(self, event):
    sliderPos = self.slider.getPosition()
    screenPos = self.scene.scene3d.convertToScreen(sliderPos[0], sliderPos[1], sliderPos[2])
    worldPos = self.scene.scene3d.convertToWorld3D(event.x, event.y, screenPos[2])
    sliderPos[0] = min(-0.365, max(-0.45, worldPos[0]))
    self.slider.setPosition(sliderPos)
    
  def onMouseUp(self, event):
    sliderPos = self.slider.getPosition()
    screenPos = self.scene.scene3d.convertToScreen(sliderPos[0], sliderPos[1], sliderPos[2])
    worldPos = self.scene.scene3d.convertToWorld3D(event.x, event.y, screenPos[2])
    sliderPos[0] = min(-0.365, max(-0.45, worldPos[0]))
    self.slider.setPosition(sliderPos)
    self.value = (sliderPos[0] + 0.45) / (0.45 - 0.365)
    print(self.value)
    self.callEvent("onChange", self.value)

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
    
  def onMouseUp(self, event):
    if self.scene.focusObject is self.button:
      self.setSelected(True)
    else:
      self.setSelected(False)
    
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
      
  def onKeyDown(self, event):
    print(event)
    if event.key == 8:
        self.text = self.text[:-1]
    elif event.key < 256 and event.key != 13:
        self.text += event.character      
        
    lenText = len(self.text)
    if lenText > 100:
        textToVisualize = self.text[(lenText-100):]
    else:
        textToVisualize = self.text
    self.textObject.setText(textToVisualize)    
    self.scene.scene3d.redraw()

# FileChooser widget
class FileChooser(View):
  def __init__(self, parent):
    View.__init__(self, parent)
    
    self.currentFile = Object(self, mesh = "data/3dobjs/file.obj", position = [0, 0, 0], visible = False)
    self.nextFile = Object(self, mesh = "data/3dobjs/nextfile.obj", position = [3.0, 0.5, 0], visible = False)
    self.previousFile = Object(self, mesh = "data/3dobjs/previousfile.obj", position = [-3.0, 0.5, 0], visible = False)
    self.filename = Object(self, mesh = "data/3dobjs/empty.obj", position = [-0.5, -0.7, 0], visible = False)
    self.files = None
    self.selectedFile = 0
    
    self.nextFileAnimation = animation3d.Timeline(0.25)
    self.nextFileAnimation.append(animation3d.PathAction(self.currentFile.mesh, [[0, 0, 0], [-3.0, 0.5, 0]]))
    self.nextFileAnimation.append(animation3d.ScaleAction(self.currentFile.mesh, [1.5, 1.5, 1.5], [1.0, 1.0, 1.0]))
    self.nextFileAnimation.append(animation3d.PathAction(self.nextFile.mesh, [[3.0, 0.5, 0], [0, 0, 0]]))
    self.nextFileAnimation.append(animation3d.ScaleAction(self.nextFile.mesh, [1.0, 1.0, 1.0], [1.5, 1.5, 1.5]))
    self.nextFileAnimation.append(animation3d.UpdateAction(self.scene.scene3d))
    
    self.previousFileAnimation = animation3d.Timeline(0.25)
    self.previousFileAnimation.append(animation3d.PathAction(self.previousFile.mesh, [[-3.0, 0.5, 0], [0, 0, 0]]))
    self.previousFileAnimation.append(animation3d.ScaleAction(self.previousFile.mesh, [1.0, 1.0, 1.0], [1.5, 1.5, 1.5]))
    self.previousFileAnimation.append(animation3d.PathAction(self.currentFile.mesh, [[0, 0, 0], [3.0, 0.5, 0],]))
    self.previousFileAnimation.append(animation3d.ScaleAction(self.currentFile.mesh, [1.5, 1.5, 1.5], [1.0, 1.0, 1.0]))
    self.previousFileAnimation.append(animation3d.UpdateAction(self.scene.scene3d))
    
    @self.previousFile.event
    def onClick(event):
      self.goPrevious()
      
    @self.nextFile.event
    def onClick(event):
      self.goNext()
    
  def onShow(self, event):
    self.files = []
    for f in os.listdir("models"):
        if os.path.splitext(f)[-1] == ".mhm":
            self.files.append(f)
    self.selectedFile = 0
    
    self.currentFile.setScale(1.5);
    
    self.previousFile.clearTexture()
    self.previousFile.hide()
    
    if self.selectedFile < len(self.files):
        self.currentFile.setTexture("models/" + self.files[self.selectedFile].replace('mhm', 'bmp'))
        self.filename.setText(self.files[self.selectedFile].replace('.mhm', ''))
        self.currentFile.show()
        self.filename.show()
    else:
        self.currentFile.clearTexture()
        self.currentFile.hide()
        self.filename.hide()
    
    if self.selectedFile + 1 < len(self.files):
        self.nextFile.setTexture("models/" + self.files[self.selectedFile + 1].replace('mhm', 'bmp'))
        self.nextFile.show()
    else:
        self.nextFile.clearTexture()
        self.nextFile.hide()
            
    self.scene.scene3d.redraw()
    
  def onKeyDown(self, event):
    if event.key == 276:
      self.goPrevious()
    elif event.key == 275:
      self.goNext()
    elif event.key == 271:
      self.LoadCurrent()
      
  def goPrevious(self):
    if self.selectedFile == 0:
      return
        
    # Start animation by hiding the next file
    self.nextFile.setVisibility(0)
    
    # Animate by moving previous and current file to current and next locations
    self.previousFileAnimation.start()
    
    # End animation by resetting positions and showing new configuration
    self.previousFile.setPosition([-3.0, 0.5, 0])
    self.previousFile.setScale(1.0)
    self.currentFile.setPosition([0, 0, 0])
    self.currentFile.setScale(1.5)
        
    self.selectedFile -= 1
    
    if self.selectedFile - 1 >= 0:
        self.previousFile.setTexture("models/" + self.files[self.selectedFile - 1].replace('mhm', 'bmp'))
        self.previousFile.show()
    else:
        self.previousFile.clearTexture()
        self.previousFile.hide()
    
    self.currentFile.setTexture("models/" + self.files[self.selectedFile].replace('mhm', 'bmp'))
    self.filename.setText(self.files[self.selectedFile].replace('.mhm', ''))
    self.currentFile.show()
    self.nextFile.setTexture("models/" + self.files[self.selectedFile + 1].replace('mhm', 'bmp'))
    self.nextFile.show()
    
    self.scene.scene3d.redraw()
    
  def goNext(self):
    if self.selectedFile + 1 == len(self.files):
      return
        
    # Start animation by hiding the previous file
    self.previousFile.setVisibility(0)
    
    # Animate by moving current and next file to previous and current locations
    self.nextFileAnimation.start()
    
    # End animation by resetting positions and showing new configuration
    self.currentFile.setPosition([0, 0, 0])
    self.currentFile.setScale(1.5)
    self.nextFile.setPosition([3.0, 0.5, 0])
    self.nextFile.setScale(1.0)
    
    self.selectedFile += 1
    
    self.previousFile.setTexture("models/" + self.files[self.selectedFile - 1].replace('mhm', 'bmp'))
    self.previousFile.show()
    self.currentFile.setTexture("models/" + self.files[self.selectedFile].replace('mhm', 'bmp'))
    self.filename.setText(self.files[self.selectedFile].replace('.mhm', ''))
    self.currentFile.show()
    
    if self.selectedFile + 1 < len(self.files):
        self.nextFile.setTexture("models/" + self.files[self.selectedFile + 1].replace('mhm', 'bmp'))
        self.nextFile.show()
    else:
        self.nextFile.clearTexture()
        self.nextFile.hide()
        
    self.scene.scene3d.redraw()