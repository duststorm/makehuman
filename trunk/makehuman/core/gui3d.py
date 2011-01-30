#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Manuel Bastioni, Marc Flerackers

**Copyright(c):**	  MakeHuman Team 2001-2010

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TODO

"""

__docformat__ = 'restructuredtext'

import events3d
import files3d
import animation3d
import module3d
import mh
import os
import font3d

from collections import namedtuple

defaultFontSize = 1.0
defaultFontFamily = 'arial'

Style = namedtuple('Style', 'width height mesh normal selected focused fontSize border')

# Wrapper around Object3D
class Object(events3d.EventHandler):

    def __init__(self, view, position, mesh, texture=None, visible=True):
        self.app = view.app
        self.view = view
        if isinstance(mesh, str):
            self.mesh = files3d.loadMesh(self.app.scene3d, mesh, position[0], position[1], position[2])
            self.meshName = mesh
        else: # It's of type module3d.Object3D
            self.mesh=mesh
            self.app.scene3d.objects.append(mesh)
            self.meshName = mesh.name
            self.mesh.setLoc(position[0], position[1], position[2])
        
        # TL: added this to avoid crash on startup
        if not self.mesh:
            return
            
        view.objects.append(self)
        
        if texture:
            self.mesh.setTexture(texture)
        
        if view.isVisible() and visible:
            self.mesh.setVisibility(1)
        else:
            self.mesh.setVisibility(0)
   
        self.visible = visible
        self.mesh.object = self
        self.__bbox = None

    def show(self):
        
        self.visible = True
        self.setVisibility(True)

    def hide(self):

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

        if self.view.isVisible() and self.visible and visibility:
            self.mesh.setVisibility(1)
        else:
            self.mesh.setVisibility(0)

    def setScale(self, scale, scaleY=None):
        if scaleY:
            self.mesh.setScale(scale, scaleY, 1)
        else:
            self.mesh.setScale(scale, scale, 1)
            
    def getBBox():
        if not self.__bbox:
            self.__bbox = self.mesh.calcBBox()
        return self.__bbox

    def onMouseDown(self, event):
        self.view.callEvent('onMouseDown', event)

    def onMouseMoved(self, event):
        self.view.callEvent('onMouseMoved', event)

    def onMouseDragged(self, event):
        self.view.callEvent('onMouseDragged', event)

    def onMouseUp(self, event):
        self.view.callEvent('onMouseUp', event)

    def onMouseEntered(self, event):
        self.view.callEvent('onMouseEntered', event)

    def onMouseExited(self, event):
        self.view.callEvent('onMouseExited', event)

    def onClicked(self, event):
        self.view.callEvent('onClicked', event)

    def onMouseWheel(self, event):
        self.view.callEvent('onMouseWheel', event)

    def onKeyDown(self, event):
        self.view.callEvent('onKeyDown', event)

    def onKeyUp(self, event):
        self.view.callEvent('onKeyDown', event)


class TextObject(Object):
    def __init__(self, view, position, text = '', fontFamily = defaultFontFamily, fontSize = defaultFontSize):
        self.font = view.app.getFont(fontFamily)
        self.mesh = font3d.createMesh(self.font, text);
        self.mesh.setCameraProjection(1)
        self.mesh.setShadeless(1)
        self.mesh.setScale(fontSize, fontSize, fontSize)
        Object.__init__(self, view, position, self.mesh)
        self.text = text
        self.fontSize = fontSize
        
    def setText(self, text):
        if self.text == text:
            return
        self.text = text
        self.app.scene3d.clear(self.mesh)
        self.mesh = font3d.createMesh(self.font, text, self.mesh);
        self.mesh.setCameraProjection(1)
        self.mesh.setShadeless(1)
        self.app.scene3d.update()
        
    def getText(self):
        return self.text
        

# Generic view


class View(events3d.EventHandler):

    def __init__(self, parent=None, visible=True):
        self.app = parent.app
        self.parent = parent
        self.children = []
        self.objects = []
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
        
    def canFocus(self):
        return True
        
    def getBBox(self):
        if not self.objects:
            return 0
        
        bbox = self.objects[0].getBBox()
        for i in xrange(1, len(self.objects)):
            bb = self.objects[i].getBBox()
            bbox = [[min(bbox[0], bb[0]), min(bbox[1], bb[1]), min(bbox[2], bb[2])],
                [max(bbox[0], bb[0]), max(bbox[1], bb[1]), max(bbox[2], bb[2])]]
                
        return bbox
        
    def getWidth(self):
        bbox = self.getBBox()
        return bbox[1][0] - bbox[0][0]
        
    def getHeight(self):
        bbox = self.getBBox()
        return bbox[1][1] - bbox[0][1]
        
    def getDepth(self):
        bbox = self.getBBox()
        return bbox[1][2] - bbox[0][2]

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
                self.callEvent('onShow', None)
            else:
                self.callEvent('onHide', None)

    def onMouseDown(self, event):
        self.parent.callEvent('onMouseDown', event)

    def onMouseMoved(self, event):
        self.parent.callEvent('onMouseMoved', event)

    def onMouseDragged(self, event):
        self.parent.callEvent('onMouseDragged', event)

    def onMouseUp(self, event):
        self.parent.callEvent('onMouseUp', event)

    def onMouseEntered(self, event):
        self.parent.callEvent('onMouseEntered', event)

    def onMouseExited(self, event):
        self.parent.callEvent('onMouseExited', event)

    def onClicked(self, event):
        self.parent.callEvent('onClicked', event)

    def onMouseWheel(self, event):
        self.parent.callEvent('onMouseWheel', event)

    def onKeyDown(self, event):
        self.parent.callEvent('onKeyDown', event)

    def onKeyUp(self, event):
        self.parent.callEvent('onKeyUp', event)


# A View representing a specific task
TaskTabStyle = Style(**{
    'width':64,
    'height':26,
    'mesh':None,
    'normal':'button_tab2.png',
    'selected':'button_tab2_on.png',
    'focused':'button_tab2_focused.png',
    'fontSize':defaultFontSize,
    'border':[7,7,7,7]
    })

class TaskView(View):

    def __init__(self, category, name, label = None, style=TaskTabStyle):
        View.__init__(self, parent=category, visible=False)
        self.name = name
        self.focusWidget = None

        # The button is attached to the parent, as it stays visible when the task is hidden

        self.button = ToggleButton(self.parent, [2 + len(self.parent.tasks) * 66, 38.0, 9.2], (label or name), style=style)

        if name in category.tasksByName:
            raise KeyError('The task with this name already exists', name)

        category.tasks.append(self)
        category.tasksByName[self.name] = self

        @self.button.event
        def onClicked(event):
            self.app.switchTask(self.name)
            
    def canFocus(self):
        return False

    def onShow(self, event):

        self.button.setSelected(True)
        self.show()

    def onHide(self, event):

        self.button.setSelected(False)
        self.hide()


# A category grouping similar tasks
CategoryTabStyle = Style(**{
    'width':64,
    'height':26,
    'mesh':None,
    'normal':'button_tab.png',
    'selected':'button_tab_on.png',
    'focused':'button_tab_focused.png',
    'fontSize':defaultFontSize,
    'border':[7,7,7,7]
    })
    
CategoryButtonStyle = Style(**{
    'width':64,
    'height':22,
    'mesh':None,
    'normal':'button_tab3.png',
    'selected':'button_tab3_on.png',
    'focused':'button_tab3_focused.png',
    'fontSize':defaultFontSize,
    'border':[7,7,7,7]
    })

class Category(View):

    def __init__(self, parent, name, label = None, style=CategoryTabStyle):
        View.__init__(self, parent, visible = False)
        self.name = name
        self.tasks = []
        self.tasksByName = {}

        # The button is attached to the parent, as it stays visible when the category is hidden

        self.button = ToggleButton(self.parent, [2 + len(self.app.categories) * 66, 6.0, 9.6], (label or name), style = style)

        if name in parent.categories:
            raise KeyError('The category with this name already exists', name)

        parent.categories[name] = self

        @self.button.event
        def onClicked(event):
            self.app.switchCategory(self.name)
            
    def canFocus(self):
        return False

    def onShow(self, event):
        self.button.setSelected(True)
        self.show()

    def onHide(self, event):
        self.button.setSelected(False)
        self.hide()


# The application, a wrapper around Scene3D


class Application(events3d.EventHandler):

    def __init__(self):
        self.scene3d = module3d.Scene3D()
        self.scene3d.application = self
        self.app = self
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
        self.fullscreen = False
        
        mh.setMouseDownCallback(self.onMouseDownCallback)
        mh.setMouseUpCallback(self.onMouseUpCallback)
        mh.setMouseMovedCallback(self.onMouseMovedCallback)
        mh.setKeyDownCallback(self.onKeyDownCallback)
        mh.setKeyUpCallback(self.onKeyUpCallback)
        mh.setResizeCallback(self.onResizedCallback)

        mh.startWindow(0)
        
    def started(self):
        self.callEvent('onStart', None)

    def run(self):
        mh.callAsync(self.started)
        mh.startEventLoop()

    def stop(self):
        mh.shutDown()
        
    def redraw(self):
        mh.redraw(1)
        
    def redrawNow(self):
        mh.redraw(0)

    def isVisible(self):
        return True
        
    def canFocus(self):
        return False

    def setFocus(self, view=None):

        print ('setFocus', view)

        if self.focusView == view:
            return

        if not view:
            view = self

        if view.canFocus():
            event = events3d.FocusEvent(self.focusView, view)

            if self.focusView:
                self.focusView.callEvent('onBlur', event)

            self.focusView = view
            self.focusView.callEvent('onFocus', event)
            self.focusObject = None
        else:
            event = events3d.FocusEvent(self.focusView, None)

            if self.focusView:
                self.focusView.callEvent('onBlur', event)

            self.focusView = None
            self.focusObject = None

    def switchTask(self, name):
        if self.currentTask:
            self.currentTask.hide()

        self.currentTask = self.currentCategory.tasksByName[name]

        if self.currentTask:
            self.currentTask.show()

    def switchCategory(self, name):

        # Do we need to switch at all

        if self.currentCategory and self.currentCategory.name == name:
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

        self.currentCategory.show()

        self.switchTask(category.tasks[0].name)

    # called from native

    def onMouseDownCallback(self, button, x, y):
        if button == 4:
            self.onMouseWheelCallback(1)
        elif button == 5:
            self.onMouseWheelCallback(-1)
        else:

            # Build event
            event = events3d.MouseEvent(button, x, y)

            # Get picked object

            pickedObject = self.scene3d.getPickedObject()
            if not pickedObject: return
            object = self.scene3d.getPickedObject()[1]
               
            # If we have an object
            # Try to give its view focus
   
            self.focusObject = object.object
            self.focusObject.view.setFocus()
   
            # It is the object which will receive the following mouse messages
   
            self.mouseDownObject = object.object
   
            # Send event to the object
   
            object.object.callEvent('onMouseDown', event)

    def onMouseUpCallback(self, button, x, y):
        if button == 4 or button == 5:
            return

        # Build event
        event = events3d.MouseEvent(button, x, y)

        # Get picked object
        
        pickedObject = self.scene3d.getPickedObject()
        if not pickedObject: return
        object = pickedObject[1]
        if self.mouseDownObject:
            self.mouseDownObject.callEvent('onMouseUp', event)
            if self.mouseDownObject is object.object:
                self.mouseDownObject.callEvent('onClicked', event)

    def onMouseMovedCallback(self, mouseState, x, y, xRel, yRel):
        
        # Build event
        event = events3d.MouseEvent(mouseState, x, y, xRel, yRel)

        # Get picked object

        picked = self.scene3d.getPickedObject()
        if not picked:

            return
        group = object = picked[0]
        object = picked[1]

        event.object = object
        event.group = group

        if mouseState:
            if self.mouseDownObject:
                self.mouseDownObject.callEvent('onMouseDragged', event)
        else:
            if object and object.object:
                if self.enteredObject != object.object:
                    if self.enteredObject:
                        self.enteredObject.callEvent('onMouseExited', event)
                    self.enteredObject = object.object
                    self.enteredObject.callEvent('onMouseEntered', event)
                object.object.callEvent('onMouseMoved', event)

    def onMouseWheelCallback(self, wheelDelta):

        # Mouse wheel events, like key events are sent to the focus view

        event = events3d.MouseWheelEvent(wheelDelta)
        if self.focusView:
            self.focusView.callEvent('onMouseWheel', event)
        else:
            self.currentTask.callEvent('onMouseWheel', event)

    def onKeyDownCallback(self, key, character, modifiers):
        if key == events3d.SDLK_TAB:
            if self.focusView:

            # if self.focusView.wantsTab and not (modifiers & events3d.KMOD_CTRL):

                index = self.focusView.parent.children.index(self.focusView)
                if modifiers & events3d.KMOD_SHIFT:
                    start = index
                    index = index - 1 if index > 0 else len(self.focusView.parent.children) - 1
                    while start != index:
                        child = self.focusView.parent.children[index]
                        if child.canFocus():
                            child.setFocus()
                            break
                        index = index - 1 if index > 0 else len(self.focusView.parent.children) - 1
                else:
                    start = index
                    index = index + 1 if index < len(self.focusView.parent.children) - 1 else 0
                    while start != index:
                        child = self.focusView.parent.children[index]
                        if child.canFocus():
                            child.setFocus()
                            break
                        index = index + 1 if index < len(self.focusView.parent.children) - 1 else 0
                self.redraw()
                return
        event = events3d.KeyEvent(key, character, modifiers)
        if self.focusView:
            self.focusView.callEvent('onKeyDown', event)
        else:
            self.currentTask.callEvent('onKeyDown', event)

    def onKeyUpCallback(self, key, character, modifiers):
        event = events3d.KeyEvent(key, character, modifiers)
        if self.focusView:
            self.focusView.callEvent('onKeyUp', event)
        else:
            self.currentTask.callEvent('onKeyUp', event)
            
    def onResizedCallback(self, width, height, fullscreen):
        if self.fullscreen != fullscreen:
            self.scene3d.reloadTextures()
        self.fullscreen = fullscreen
        
        event = (width, height, fullscreen)
        
        self.callEvent('onResized', event)
        
        for category in self.categories.itervalues():
            
            category.callEvent('onResized', event)
            
            for task in category.tasks:
                
                task.callEvent('onResized', event)
            
    def getCategory(self, name, style=CategoryTabStyle):
        try:
            return self.categories[name]
        except:
            return Category(self, name, None, style)

# Widgets

# Slider widget
SliderStyle = Style(**{
    'width':128,
    'height':32,
    'mesh':None,
    'normal':'slider_generic.png',
    'selected':None,
    'focused':None,
    'fontSize':defaultFontSize,
    'border':None
    })
    
SliderThumbStyle = Style(**{
    'width':16,
    'height':16,
    'mesh':None,
    'normal':'slider.png',
    'selected':None,
    'focused':'slider_focused.png',
    'fontSize':defaultFontSize,
    'border':None
    })

class Slider(View):
    
    """
    A slider widget. This widget can be used to choose between a continuous (float) or discrete (int) range.
    The onChange event is triggered when the slider is released, with the new value as parameter.
    For real-time feedback the onChanging event is triggered when the slider is being moved, with the
    current value as parameter.
    """

    def __init__(self, parent, position, value=0.0, min=0.0, max=1.0, label=None,
        style=SliderStyle, thumbStyle=SliderThumbStyle):
        
        """
        This is the constructor for the Button class.

        @param parent: The parent view.
        @type parent: L{View}
        @param position: The position.
        @type position: C{list}
        @param value: The original value.
        @type value: C{int} or C{float}
        @param min: The minimum value.
        @type min: C{int} or C{float}
        @param max: The maximum value.
        @type max: C{int} or C{float}
        @param label: The label.
        @type label: C{str}
        @param style: The style.
        @type style: L{Style}
        """
        
        View.__init__(self, parent)
        
        self.style = style
        self.thumbStyle = thumbStyle
        
        self.thumbTexture = self.app.getThemeResource('images', thumbStyle.normal)
        self.focusedThumbTexture = self.app.getThemeResource('images', thumbStyle.focused)
        
        mesh = RectangleMesh(style.width, style.height, self.app.getThemeResource('images', style.normal))
        self.background = Object(self, position, mesh)
        
        mesh = RectangleMesh(thumbStyle.width, thumbStyle.height, self.thumbTexture)
        self.thumb = Object(self, [position[0], position[1]+16, position[2] + 0.01], mesh)
            
        if isinstance(label, str):
            self.label = TextObject(self, [position[0]+10,position[1]+8-6,position[2]+0.2], label, fontSize = style.fontSize)
            
        self.thumbMinX = position[0] + thumbStyle.width / 2
        self.thumbMaxX = position[0] + style.width - thumbStyle.width - thumbStyle.width / 2
        self.min = min
        self.max = max
        self.setValue(value)
    
    def getPosition(self):
        return self.background.getPosition()
        
    def setPosition(self, position):
        self.background.setPosition(position)
        self.thumbMinX = position[0] + self.thumbStyle.width / 2
        self.thumbMaxX = position[0] + self.style.width - self.thumbStyle.width - self.thumbStyle.width / 2
        self.setValue(self.getValue())
        self.label.setPosition([position[0]+10,position[1]-2,position[2]+0.2])

    def setValue(self, value):
        self.__value = min(self.max, max(self.min, value))
        thumbPos = self.thumb.getPosition()
        #for values that are integer we need a float denominator
        value = (self.__value - self.min) / float(self.max - self.min)
        thumbPos[0] = value * (self.thumbMaxX - self.thumbMinX) + self.thumbMinX
        self.thumb.setPosition(thumbPos)

    def getValue(self):
        return self.__value

    def onMouseDragged(self, event):
        thumbPos = self.thumb.getPosition()
        screenPos = mh.cameras[1].convertToScreen(thumbPos[0], thumbPos[1], thumbPos[2])
        worldPos = mh.cameras[1].convertToWorld3D(event.x, event.y, screenPos[2])
        thumbPos[0] = min(self.thumbMaxX, max(self.thumbMinX, worldPos[0] - self.thumbStyle.width / 2))
        self.thumb.setPosition(thumbPos)
        value = (thumbPos[0] - self.thumbMinX) / float(self.thumbMaxX - self.thumbMinX)
        self.__value = value * (self.max - self.min) + self.min
        if isinstance(self.min, int):
            self.__value = int(self.__value)

        self.callEvent('onChanging', self.__value)

    def onMouseUp(self, event):
        thumbPos = self.thumb.getPosition()
        screenPos = mh.cameras[1].convertToScreen(thumbPos[0], thumbPos[1], thumbPos[2])
        worldPos = mh.cameras[1].convertToWorld3D(event.x, event.y, screenPos[2])
        thumbPos[0] = min(self.thumbMaxX, max(self.thumbMinX, worldPos[0] - self.thumbStyle.width / 2))
        self.thumb.setPosition(thumbPos)
        value = (thumbPos[0] - self.thumbMinX) / float(self.thumbMaxX - self.thumbMinX)
        self.__value = value * (self.max - self.min) + self.min
        if isinstance(self.min, int):
            self.__value = int(self.__value)

        self.callEvent('onChange', self.__value)

    def onKeyDown(self, event):
        oldValue = self.__value
        newValue = self.__value

        if event.key == events3d.SDLK_HOME:
            newValue = self.min
        elif event.key == events3d.SDLK_LEFT:
            newValue -= (self.max - self.min) / 10.0
        elif event.key == events3d.SDLK_RIGHT:
            newValue += (self.max - self.min) / 10.0
        elif event.key == events3d.SDLK_END:
            newValue = self.max
        else:
            View.onKeyDown(self, event)

        if oldValue != newValue:
            self.setValue(newValue)
            if oldValue != self.__value:
                self.callEvent('onChange', self.__value)

    def onFocus(self, event):
        if self.focusedThumbTexture:
            self.thumb.setTexture(self.focusedThumbTexture)

    def onBlur(self, event):
        if self.focusedThumbTexture:
            self.thumb.setTexture(self.thumbTexture)


# Button widget
ButtonStyle = Style(**{
    'width':112,
    'height':20,
    'mesh':None,
    'normal':'button_unselected.png',
    'selected':'button_selected.png',
    'focused':'button_focused.png',
    'fontSize':defaultFontSize,
    'border':[2, 2, 2, 2]
    })

class Button(View):
    
    """
    A push button widget. This widget can be used to trigger an action by catching the onClicked event.
    The onClicked event is triggered when the button is clicked and the mouse is released while being
    over the widget.
    """

    def __init__(self, parent, position, label=None, selected=False, style=ButtonStyle):
        
        """
        This is the constructor for the Button class.

        @param parent: The parent view.
        @type parent: L{View}
        @param position: The position.
        @type position: C{list}
        @param label: The label.
        @type label: C{str}
        @param selected: The selected state.
        @type selected: C{Boolean} 
        @param style: The style.
        @type style: L{Style}
        """
        
        View.__init__(self, parent)
        
        self.label = None
        
        self.texture = self.app.getThemeResource('images', style.normal)
        self.selectedTexture = self.app.getThemeResource('images', style.selected) if style.selected else None
        self.focusedTexture = self.app.getThemeResource('images', style.focused) if style.focused else None
        
        if selected and self.selectedTexture:
            t = self.selectedTexture
        else:
            t = self.texture
            
        width = style.width
        height = style.height
        fontSize = style.fontSize
        border = style.border
        
        self.style = style
            
        if style.mesh:
            self.button = Object(self, position, style.mesh, texture=t)
            if isinstance(label, str):
                #assumes button obj origin is upper left corner
                #TODO text should be in the middle of button, calculate this from text length
                self.label = TextObject(self, [position[0]+5,position[1]-7,position[2]+0.001], label, fontSize = fontSize)
        else:
            if border:
                mesh = NineSliceMesh(width, height, t, border)
            else:
                mesh = RectangleMesh(width, height, t)
            self.button = Object(self, position, mesh)
            if isinstance(label, str):
                self.label = TextObject(self, [position[0] + border[0] + 3,position[1]+height/2-6,position[2]+0.001], label, fontSize = fontSize)
            
        self.selected = selected
        
    def getPosition(self):
        return self.button.getPosition()
    
    def setPosition(self, position):
        self.button.setPosition(position)
        if getattr(self, 'label'):
            self.label.setPosition([position[0] + self.style.border[0] + 3,position[1]+self.style.height/2-6,position[2]+0.001])

    def setTexture(self, texture):
        self.texture = texture
        self.button.setTexture(texture)
        
    def getLabel(self):
        if self.label:
            return self.label.getText()
        else:
            return ''

    def onMouseDown(self, event):
        self.setSelected(True)

    def onMouseUp(self, event):
        self.setSelected(False)
        
    def onMouseDragged(self, event):
        pass

    def onKeyDown(self, event):
        if event.key == events3d.SDLK_RETURN or event.key == events3d.SDLK_KP_ENTER:
            self.setSelected(True)
            self.app.redraw()
        else:
            View.onKeyDown(self, event)

    def onKeyUp(self, event):
        if event.key == events3d.SDLK_RETURN or event.key == events3d.SDLK_KP_ENTER:
            self.setSelected(False)
            self.callEvent('onClicked', event)
            self.app.redraw()

    def setSelected(self, selected):
        if self.selected != selected:
            self.selected = selected
            self.onSelected(selected)

    def onSelected(self, selected):
        if selected and self.selectedTexture:
            self.button.setTexture(self.selectedTexture)
        elif self.hasFocus() and self.focusedTexture:
            self.button.setTexture(self.focusedTexture)
        else:
            self.button.setTexture(self.texture)

    def onFocus(self, event):
        if not self.selected and self.focusedTexture:
            self.button.setTexture(self.focusedTexture)

    def onBlur(self, event):
        if self.selected and self.selectedTexture:
            self.button.setTexture(self.selectedTexture)
        else:
            self.button.setTexture(self.texture)


# RadioButton widget
RadioButtonStyle = Style(**{
    'width':112,
    'height':20,
    'mesh':None,
    'normal':'radio_off.png',
    'selected':'radio_on.png',
    'focused':'radio_focus.png',
    'fontSize':defaultFontSize,
    'border':[19, 19, 4, 1]
    })

class RadioButton(Button):

    """
    A radio button widget. This widget is used when there is more than one exclusive option to be chosen from.
    Several radio button widgets form a group when they are created with the same group list.
    The onClicked event can be used to know when the user changes his/her choice, though generally this choice
    is determined in an action by checking each radio button's selected property.
    """
    
    def __init__(self, parent, group, position, label=None, selected=False, style=RadioButtonStyle):
            
        """
        This is the constructor for the RadioButton class.

        @param parent: The parent view.
        @type parent: L{View}
        @param group: The group.
        @type group: C{list}
        @param position: The position.
        @type position: C{list}
        @param label: The label.
        @type label: C{str}
        @param selected: The selected state.
        @type selected: C{Boolean} 
        @param style: The style.
        @type style: L{Style}
        """
        
        Button.__init__(self, parent, position, label, selected, style)
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
            
    def getSelection(self):
        for radio in self.group:
            if radio.selected:
                return radio

# ToggleButton widget


class ToggleButton(Button):
    
    """
    A toggle button widget. This widget is used when there is a stat which can be turned on or off.
    The onClicked event can be used to know when the user changes his/her choice, though generally this choice
    is determined in an action by checking the toggle button's selected property.
    """

    def __init__(self, parent, position, label=None, selected=False, style=ButtonStyle):
            
        """
        This is the constructor for the ToggleButton class.

        @param parent: The parent view.
        @type parent: L{View}
        @param position: The position.
        @type position: C{list}
        @param label: The label.
        @type label: C{str}
        @param selected: The selected state.
        @type selected: C{Boolean} 
        @param style: The style.
        @type style: L{Style}
        """

        Button.__init__(self, parent, position, label, selected, style)

    def onClicked(self, event):
        if self.selected:
            self.setSelected(False)
        else:
            self.setSelected(True)

    def onMouseDown(self, event):
        pass

    def onMouseUp(self, event):
        pass
        
    def onSelected(self, selected):
        if selected and self.selectedTexture:
            self.button.setTexture(self.selectedTexture)
        else:
            self.button.setTexture(self.texture)

CheckBoxStyle = Style(**{
    'width':112,
    'height':20,
    'mesh':None,
    'normal':'check_off.png',
    'selected':'check_on.png',
    'focused':'check_focus.png',
    'fontSize':defaultFontSize,
    'border':[18, 18, 4, 2]
    })
            
class CheckBox(ToggleButton):
    
    def __init__(self, parent, position, label=None, selected=False, style=CheckBoxStyle):
        
        """
        This is the constructor for the CheckBox class.

        @param parent: The parent view.
        @type parent: L{View}
        @param position: The position.
        @type position: C{list}
        @param label: The label.
        @type label: C{str}
        @param selected: The selected state.
        @type selected: C{Boolean} 
        @param style: The style.
        @type style: L{Style}
        """
        
        Button.__init__(self, parent, position, label, selected, style)

ProgressBarStyle = Style(**{
    'width':128,
    'height':4,
    'mesh':None,
    'normal':'progressbar_background.png',
    'selected':None,
    'focused':None,
    'fontSize':defaultFontSize,
    'border':None
    })
    
ProgressBarBarStyle = Style(**{
    'width':128,
    'height':4,
    'mesh':None,
    'normal':'progressbar.png',
    'selected':None,
    'focused':None,
    'fontSize':defaultFontSize,
    'border':None
    })

class ProgressBar(View):

    """
    A ProgressBar widget. This widget can be used to show the user the progress of a 
    lengthy operation.
    """

    def __init__(self, parent, position, style=ProgressBarStyle, barStyle=ProgressBarBarStyle, visible=True):
    
        """
        This is the constructor for the ProgressBar class. It takes the following parameters:

        @param parent: The parent view.
        @type parent: L{View}
        @param position: The position.
        @type position: C{list}
        @param style: The style.
        @type style: L{Style}
        @param barStyle: The bar style.
        @type barStyle: L{Style}
        """

        View.__init__(self, parent, visible)
        
        mesh = RectangleMesh(style.width, style.height, self.app.getThemeResource('images', style.normal))
        self.background = Object(self, position, mesh)
        mesh = RectangleMesh(barStyle.width, barStyle.height, self.app.getThemeResource('images', barStyle.normal))
        self.bar = Object(self, [position[0], position[1], position[2]+0.05], mesh)
        self.bar.mesh.setScale(0.0, 1.0, 1.0)
        
    def canFocus(self):
        return False
        
    def setPosition(self, position):
        self.background.setPosition(position)
        self.bar.setPosition([position[0], position[1], position[2] + 0.05])

    def setProgress(self, progress, redraw=True):
        """
    This method updates the progress and optionally updates the screen

    Parameters
    ----------

    progress:
        *float* The progress from 0.0 to 1.0.
    redraw:
        *int* 1 if a redraw is needed, 0 otherwise.
    """

        self.bar.mesh.setScale(progress, 1.0, 1.0)
        if redraw:
            self.app.redrawNow()


# TextView widget


class TextView(View):
    
    """
    A TextView widget. This widget can be used as a label. The text is not editable by the user.
    """

    def __init__(self, parent, position=[0, 0, 9], label = '', fontSize = defaultFontSize):
        View.__init__(self, parent)
        self.textObject = TextObject(self, position, label, fontSize = fontSize)
            
    def canFocus(self):
        return False
        
    def getPosition(self):
        return self.textObject.getPosition()
        
    def setPosition(self, position):
        self.textObject.setPosition(position)

    def setText(self, text):
        self.textObject.setText(text)


# TextEdit widget
TextEditStyle = Style(**{
    'width':400,
    'height':20,
    'mesh':None,
    'normal':'texedit_off.png',
    'selected':None,
    'focused':'texedit_on.png',
    'fontSize':defaultFontSize,
    'border':[4, 4, 4, 4]
    })

class TextEdit(View):
    
    """
    A TextEdit widget. This widget can be used to let the user enter some text.
    """

    def __init__(self, parent, position, text='', style=TextEditStyle):
        View.__init__(self, parent)
        
        self.texture = self.app.getThemeResource('images', 'texedit_off.png')
        self.focusedTexture = self.app.getThemeResource('images', 'texedit_on.png')

        mesh = NineSliceMesh(style.width, style.height, self.texture, style.border)
        self.background = Object(self, position, mesh)
            
        self.textObject = TextObject(self, [position[0] + 10.0, position[1] + 4.0, position[2] + 0.1], fontSize = style.fontSize)

        self.text = text
        self.__position = len(self.text)
        self.__cursor = False
        
        self.__updateTextObject()
    
    def __showCursor(self):
        if self.__cursor:
            return
            
        if self.__position == len(self.text):
            self.text = self.text + '|'
        else:
            self.text = self.text[:self.__position] + '|' + self.text[self.__position:]
        
        self.__cursor = True

    def __hideCursor(self):
        if not self.__cursor:
            return

        if self.__position == len(self.text) - 1:
            self.text = self.text[:self.__position]
        else:
            self.text = self.text[:self.__position] + self.text[self.__position + 1:]
        
        self.__cursor = False
    
    def __addText(self, text):
        self.__hideCursor()
        self.text = self.text[:self.__position] + text + self.text[self.__position:]
        self.__position += len(text)
        self.__showCursor()
    
    def __delText(self, size = 1):
        self.__hideCursor()
        if self.__position > 0:
            size = min(size, self.__position)
            self.text = self.text[:self.__position-size] + self.text[self.__position:]
            self.__position -= size
        self.__showCursor()

    def __updateTextObject(self):
        size = len(self.text)
        if size > 100:
            text = self.text[size - 100:]
        else:
            text = self.text
        self.textObject.setText(text)

    def setText(self, text):
        self.text = text
        self.__position = len(self.text)
        if self.__cursor:
            self.cursor = False # To force showing the cursor
            self.__showCursor()
        self.__updateTextObject()

    def getText(self):
        self.__hideCursor()
        text = self.text
        self.__showCursor()
        return text
        
    def onMouseDragged(self, event):
        pass

    def onKeyDown(self, event):
        if event.modifiers & events3d.KMOD_CTRL:
            View.onKeyDown(self, event)
            return

        # print event #only for DEBUG

        if event.key == events3d.SDLK_BACKSPACE:
            self.__delText()
        elif event.key == events3d.SDLK_RETURN:
            if len(self.text):
                View.onKeyDown(self, event)

            return
        elif event.key == events3d.SDLK_RIGHT:
            if self.__position<len(self.text)-1:
                self.__hideCursor()
                self.__position += 1
                self.__showCursor()
        elif event.key == events3d.SDLK_LEFT:
            if self.__position > 0:
                self.__hideCursor()
                self.__position -= 1
                self.__showCursor()
        elif event.key < 256:
            self.__addText(event.character)

        self.__updateTextObject()
        self.app.redraw()

    def onFocus(self, event):
        if self.focusedTexture:
            self.background.setTexture(self.focusedTexture)
            self.__showCursor()
            self.__updateTextObject()

    def onBlur(self, event):
        if self.focusedTexture:
            self.background.setTexture(self.texture)
            self.__hideCursor()
            self.__updateTextObject()


# FileEntryView widget


class FileEntryView(View):
    
    """
    A FileEntryView widget. This widget can be used to let the user enter a filename.
    """

    def __init__(self, parent, buttonLabel):
        View.__init__(self, parent)

        self.edit = TextEdit(self, [200, 90, 9.5])
        self.bConfirm = Button(self, [610, 90, 9.1], buttonLabel, style=ButtonStyle._replace(width=40, height=20))

        @self.bConfirm.event
        def onClicked(event):
            if len(self.edit.getText()):
                self.onFileSelected(self.edit.getText())
                
    def onKeyDown(self, event):
        if event.modifiers & events3d.KMOD_CTRL:
            View.onKeyDown(self, event)
            return

        if event.key == events3d.SDLK_RETURN:
            self.onFileSelected(self.edit.getText())
            self.app.redraw()
                
    def onFocus(self, event):
        self.edit.setFocus()


# FileChooser widget


class FileChooser(View):
    
    """
    A FileEntryView widget. This widget can be used to let the user choose an existing file.
    """

    def __init__(self, parent, path, extension, previewExtension='bmp'):
        View.__init__(self, parent)

        self.currentPos = [800 / 2 - 50 * 1.5, 250, 0]
        self.nextPos = [800 - 800 / 4 - 50, 200, 0]
        self.previousPos = [800 / 4 - 50, 200, 0]
        self.currentFile = Object(self, self.currentPos, RectangleMesh(100, 100), visible=False)
        self.nextFile = Object(self, self.nextPos, RectangleMesh(100, 100), visible=False)
        self.previousFile = Object(self, self.previousPos, RectangleMesh(100, 100), visible=False)
        self.filename = TextObject(self, [self.currentPos[0], self.currentPos[1] + 100 * 1.5 + 10, 0])
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
        self.nextFileAnimation.append(animation3d.UpdateAction(self.app))

        self.previousFileAnimation = animation3d.Timeline(0.25)
        self.previousFileAnimation.append(animation3d.PathAction(self.previousFile.mesh, [self.previousPos, self.currentPos]))
        self.previousFileAnimation.append(animation3d.ScaleAction(self.previousFile.mesh, [1.0, 1.0, 1.0], [1.5, 1.5, 1.5]))
        self.previousFileAnimation.append(animation3d.PathAction(self.currentFile.mesh, [self.currentPos, self.nextPos]))
        self.previousFileAnimation.append(animation3d.ScaleAction(self.currentFile.mesh, [1.5, 1.5, 1.5], [1.0, 1.0, 1.0]))
        self.previousFileAnimation.append(animation3d.UpdateAction(self.app))

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
            preview = filename.replace(os.path.splitext(filename)[-1], '.' + self.previewExtension)
        return preview

    def updateText(self):
        text = self.files[self.selectedFile]
        text = text.replace(os.path.splitext(text)[-1], '')
        self.filename.setText(text)

    def onShow(self, event):
        self.files = []
        if isinstance(self.extension, str):
            for f in os.listdir(self.path):
                if f.endswith('.' + self.extension):
                    self.files.append(f)
        elif isinstance(self.extension, list):
            for f in os.listdir(self.path):
                for ext in self.extension:
                    if f.endswith('.' + ext):
                        self.files.append(f)
        """				
        if self.selectedFile > len(self.files) or self.selectedFile < 0:
            self.selectedFile = 0  # Im not sure if this happens but Ill check
            print "Debug: Something weird just happened with the selected files!"
        """
        
        if len(self.files):

          self.currentFile.setScale(1.5)

          # self.previousFile.clearTexture()
          # self.previousFile.hide()

          if self.selectedFile > 0:
              self.previousFile.setTexture(self.path + '/' + self.getPreview(self.files[self.selectedFile - 1]))
              self.previousFile.show()
          else:
              self.previousFile.clearTexture()
              self.previousFile.hide()
              
          self.currentFile.setTexture(self.path + '/' + self.getPreview(self.files[self.selectedFile]))
          self.updateText()
          self.currentFile.show()
          self.filename.setVisibility(1)

          """
          if self.selectedFile < len(self.files):
              self.currentFile.setTexture(self.path + '/' + self.getPreview(self.files[self.selectedFile]))
              self.updateText()
              self.currentFile.show()
              self.filename.setVisibility(1)
          else:
              self.currentFile.clearTexture()
              self.currentFile.hide()
              self.filename.setVisibility(0)
          """

          if self.selectedFile + 1 < len(self.files):
              self.nextFile.setTexture(self.path + '/' + self.getPreview(self.files[self.selectedFile + 1]))
              self.nextFile.show()
          else:
              self.nextFile.clearTexture()
              self.nextFile.hide()

        self.app.redraw()

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
            self.previousFile.setTexture(self.path + '/' + self.getPreview(self.files[self.selectedFile - 1]))
            self.previousFile.show()
        else:
            self.previousFile.clearTexture()
            self.previousFile.hide()

        self.currentFile.setTexture(self.path + '/' + self.getPreview(self.files[self.selectedFile]))
        self.updateText()
        self.currentFile.show()
        self.nextFile.setTexture(self.path + '/' + self.getPreview(self.files[self.selectedFile + 1]))
        self.nextFile.show()

        self.app.redraw()

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

        self.previousFile.setTexture(self.path + '/' + self.getPreview(self.files[self.selectedFile - 1]))
        self.previousFile.show()
        self.currentFile.setTexture(self.path + '/' + self.getPreview(self.files[self.selectedFile]))
        self.updateText()
        self.currentFile.show()

        if self.selectedFile + 1 < len(self.files):
            self.nextFile.setTexture(self.path + '/' + self.getPreview(self.files[self.selectedFile + 1]))
            self.nextFile.show()
        else:
            self.nextFile.clearTexture()
            self.nextFile.hide()

        self.app.redraw()
        
GroupBoxStyle = Style(**{
    'width':128,
    'height':64,
    'mesh':None,
    'normal':'group_box.png',
    'selected':None,
    'focused':None,
    'fontSize':defaultFontSize,
    'border':[8, 24, 8, 8]
    }) 
        
class GroupBox(View):
    
    """
    A group box widget. This widget can be used to show which widgets belong together.
    """

    def __init__(self, parent, position=[0, 0, 9], label=None, style=GroupBoxStyle):
        
        """
        This is the constructor for the GroupBox class.

        @param parent: The parent view.
        @type parent: L{View}
        @param position: The position, a list of 4 C{int} or C{float} elements.
        @type position: C{list}
        @param label: The label.
        @type label: C{str}
        @param style: The style.
        @type style: L{Style}
        """
        
        View.__init__(self, parent)
        
        texture = self.app.getThemeResource('images', style.normal)
        
        self.style = style
        
        mesh = NineSliceMesh(style.width, style.height, texture, style.border)
        self.box = Object(self, position, mesh)
        
        if isinstance(label, str):
            self.label = TextObject(self,
                [position[0]+style.border[0],position[1]+style.border[1]/2-6,position[2]+0.001],
                label,
                fontSize = style.fontSize)
    
    def getPosition(self):
        return self.box.getPosition()
    
    def setPosition(self, position):
        
        dx, dy, dz = self.getPosition()
        dx = position[0] - dx
        dy = position[1] - dy
        dz = position[2] - dz
        
        self.box.setPosition(position)
        self.label.setPosition([position[0]+self.style.border[0],position[1]+self.style.border[1]/2-6,position[2]+0.001])
        
        for child in self.children:
            x, y, z = child.getPosition()
            child.setPosition([x+dx,y+dy,z+dz])
        
    def canFocus(self):
        return False
        
    def onMouseDragged(self, event):
        pass
        
class ShortcutEdit(View):
    
    """
    An edit control for entering shortcuts.
    """
    
    def __init__(self, parent, position, shortcut):
        
        """
        This is the constructor for the ShortcutEdit class.

        @param parent: The parent view.
        @type parent: L{View}
        @param position: The position, a list of 4 C{int} or C{float} elements.
        @type position: C{list}
        @param shortcut: The position, a C{tuple} of modifiers and a key.
        @type shortcut: C{tuple}
        """
        
        View.__init__(self, parent)
        
        self.texture = self.app.getThemeResource('images', 'button_tab3_on.png')
        self.focusedTexture = self.app.getThemeResource('images', 'button_tab3_focused.png')
        
        mesh = NineSliceMesh(64, 22, self.texture, [7,7,7,7])
        self.background = Object(self, position, mesh)
        self.label = TextObject(self,
            [position[0] + 7 + 3,position[1]+22/2-6,position[2]+0.001],
            self.shortcutToLabel(shortcut[0], shortcut[1]))
            
    def getPosition(self):
        return self.background.getPosition()
    
    def setPosition(self, position):
        self.background.setPosition(position)
        self.label.setPosition([position[0] + 7 + 3,position[1]+22/2-6,position[2]+0.001])
            
    def setShortcut(self, shortcut):
        self.label.setText(self.shortcutToLabel(shortcut[0], shortcut[1]))
        self.app.redraw()
        
    def canFocus(self):
        return True
        
    def onFocus(self, event):
        self.background.setTexture(self.focusedTexture)

    def onBlur(self, event):
        self.background.setTexture(self.texture)
        
    def onMouseDragged(self, event):
        pass
        
    def onKeyDown(self, event):
        
        print event.key, event.character, event.modifiers
            
        self.label.setText(self.shortcutToLabel(event.modifiers, event.key))
        self.app.redraw()
        
        if event.key not in [events3d.SDLK_RCTRL, events3d.SDLK_LCTRL, events3d.SDLK_RALT, events3d.SDLK_LALT]:
            m = 0
        
            if event.modifiers & events3d.KMOD_CTRL:
                m |= events3d.KMOD_CTRL
                
            if event.modifiers & events3d.KMOD_ALT:
                m |= events3d.KMOD_ALT
                
            self.callEvent('onChanged', (m, event.key))
        
    def shortcutToLabel(self, modifiers, key):
        
        label = ''
        
        if modifiers & events3d.KMOD_CTRL:
            label += 'Ctl-'
            
        if modifiers & events3d.KMOD_ALT:
            label += 'Alt-'
            
        if key in self.keyNames:
            label += self.keyNames[key]
        elif key < 256:
            label += chr(key)
            
        return label
        
    def onChanged(self, shortcut):
        pass
        
    keyNames = {
        events3d.SDLK_BACKSPACE:'Bck',
        events3d.SDLK_RETURN:'Enter',
        events3d.SDLK_PAUSE:'Pause',
        
        events3d.SDLK_ESCAPE:'Esc',
        
        events3d.SDLK_DELETE:'Del',
        
        events3d.SDLK_UP:'Up',
        events3d.SDLK_DOWN:'Down',
        events3d.SDLK_RIGHT:'Right',
        events3d.SDLK_LEFT:'Left',
        events3d.SDLK_INSERT:'Ins',
        events3d.SDLK_HOME:'Home',
        events3d.SDLK_END:'End',
        events3d.SDLK_PAGEUP:'PgUp',
        events3d.SDLK_PAGEDOWN:'PgDn',

        events3d.SDLK_F1:'F1',
        events3d.SDLK_F2:'F2',
        events3d.SDLK_F3:'F3',
        events3d.SDLK_F4:'F4',
        events3d.SDLK_F5:'F5',
        events3d.SDLK_F6:'F6',
        events3d.SDLK_F7:'F7',
        events3d.SDLK_F8:'F8',
        events3d.SDLK_F9:'F9',
        events3d.SDLK_F10:'F10',
        events3d.SDLK_F11:'F11',
        events3d.SDLK_F12:'F12',
        events3d.SDLK_F13:'F13',
        events3d.SDLK_F14:'F14',
        events3d.SDLK_F15:'F15',
        
        events3d.SDLK_RCTRL:'Ctl',
        events3d.SDLK_LCTRL:'Ctl',
        events3d.SDLK_RALT:'Alt',
        events3d.SDLK_LALT:'Alt'
    }

class NineSliceMesh(module3d.Object3D):
    
    """
    A 9 slice mesh. It is a mesh with fixed size borders and a resizeable center.
    This makes sure the borders of a group box are not stretched.
    """
    
    def __init__(self, width, height, texture, border):
    
        """
        This is the constructor for the NineSliceMesh class.

        @param width: The width.
        @type width: C{int} or C{float}
        @param height: The height.
        @type height: C{int} or C{float}
        @param texture: The texture.
        @type texture: C{str}
        @param border: The border, a list of 4 C{int} or C{float} elements.
        @type border: C{list}
        """
        
        module3d.Object3D.__init__(self, '9slice_' + texture + '_' + str(border))
        
        t = module3d.getTexture(texture)
        
        # Make sure fractions are calculated correctly
        textureWidth = float(t.width)
        textureHeight = float(t.height)
            
        outer=[[0, 0], [width, height]]
        inner=[[border[0], border[1]], [width - border[2], height - border[3]]]
            
        self.uvValues = []
        self.indexBuffer = []
        
        # create group
        fg = self.createFaceGroup('9slice')
        
        xc = [outer[0][0], inner[0][0], inner[1][0], outer[1][0]]
        yc = [outer[0][1], inner[0][1], inner[1][1], outer[1][1]]
        xuv = [0.0, border[0] / textureWidth, (textureWidth - border[2]) / textureWidth, 1.0]
        yuv = [1.0, 1.0 - border[1] / textureHeight, 1.0 - (textureHeight - border[3]) / textureHeight, 0.0]
        
        # The 16 vertices
        v = []
        for y in yc:
            for x in xc:  
                v.append(self.createVertex([x, y, 0.0]))
        
        # The 16 uv values
        uv = []
        for y in yuv:
            for x in xuv:  
                uv.append([x, y])
        
        # The 18 faces (9 quads)
        for y in xrange(3):
            for x in xrange(3):
                o = x + y * 4
                fg.createFace(v[o+4], v[o+5], v[o+1], v[o], uv=(uv[o+4], uv[o+5], uv[o+1], uv[o]))
                
        self.texture = texture
        self.setCameraProjection(1)
        self.setShadeless(1)
        self.updateIndexBuffer()
    
    def resize(self, width, height):
        
        outer=[[0, 0], [width, height]]
        inner=[[border[0], border[1]], [width - border[2], height - border[3]]]
        
        xc = [outer[0][0], inner[0][0], inner[1][0], outer[1][0]]
        yc = [outer[0][1], inner[0][1], inner[1][1], outer[1][1]]
        
        i = 0
        for y in yc:
            for x in xc:  
                self.verts[i].co = [x, y, 0.0]
                i += 1
        
        self.update()
    
class RectangleMesh(module3d.Object3D):
            
    def __init__(self, width, height, texture=None):
        
        
        """
        This is the constructor for the RectangleMesh class.

        @param width: The width.
        @type width: C{int} or C{float}
        @param height: The height.
        @type height: C{int} or C{float}
        @param texture: The texture.
        @type texture: C{str}
        """
        
        module3d.Object3D.__init__(self, 'rectangle_%s' % texture)
        
        self.uvValues = []
        self.indexBuffer = []
        
        # create group
        fg = self.createFaceGroup('rectangle')
        
        # The 4 vertices
        v = []
        v.append(self.createVertex([0.0, 0.0, 0.0]))
        v.append(self.createVertex([width, 0.0, 0.0]))
        v.append(self.createVertex([width, height, 0.0]))
        v.append(self.createVertex([0.0, height, 0.0]))
        
        # The 4 uv values
        uv = ([0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0])
        
        # The face
        fg.createFace(v[0], v[1], v[2], v[3], uv=uv)
                
        self.texture = texture
        self.setCameraProjection(1)
        self.setShadeless(1)
        self.updateIndexBuffer()
        
    def resize(self, width, height):
        
        self.verts[1].co[0] = width
        self.verts[2].co[0] = width
        self.verts[2].co[1] = height
        self.verts[3].co[1] = height
        self.update()
        