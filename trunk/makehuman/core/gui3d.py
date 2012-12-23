#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
:Authors:
    Manuel Bastioni,
    Marc Flerackers

:Version: 1.0
:Copyright: MakeHuman Team 2001-2011
:License: GPL3 

This module contains classes defined to implement widgets that provide utility functions
to the graphical user interface.
"""

import events3d
import module3d
import mh
import os
import files3d
import weakref
from catmull_clark_subdivision import createSubdivisionObject, updateSubdivisionObject
from geometry3d import NineSliceMesh, RectangleMesh, FrameMesh

# Wrapper around Object3D
class Object(events3d.EventHandler):

    """
    An object on the screen.
    
    :param position: The position in 3d space.
    :type position: list or tuple
    :param mesh: The mesh object.
    :param visible: Wether the object should be initially visible.
    :type visible: Boolean
    """

    def __init__(self, position, mesh, visible=True):
        
        if mesh.object:
            raise RuntimeException('This mesh is already attached to an object')
                
        self.mesh = mesh
        self.mesh.setLoc(*position)
        self.mesh.object = self
        self.mesh.setVisibility(visible)
        
        self._view = None
        
        self.visible = visible
        
        self.proxy = None
        
        self.__seedMesh = self.mesh
        self.__proxyMesh = None
        self.__subdivisionMesh = None
        self.__proxySubdivisionMesh = None
        
    def __del__(self):
    
        self.proxy = None
        
        self.__seedMesh = None
        self.__proxyMesh = None
        self.__subdivisionMesh = None
        self.__proxySubdivisionMesh = None
        
    def _attach(self):
    
        if self._view().isVisible() and self.visible:
            self.mesh.setVisibility(1)
        else:
            self.mesh.setVisibility(0)
            
        if self.__seedMesh:
           self.__seedMesh.attach()
        if self.__proxyMesh:
           self.__proxyMesh.attach()
        if self.__subdivisionMesh:
           self.__subdivisionMesh.attach()
        if self.__proxySubdivisionMesh:
           self.__proxySubdivisionMesh.attach()
            
    def _detach(self):
        
        self.__seedMesh.detach()
        if self.__proxyMesh:
            self.__proxyMesh.detach()
        if self.__subdivisionMesh:
            self.__subdivisionMesh.detach()
        if self.__proxySubdivisionMesh:
            self.__proxySubdivisionMesh.detach()
            
    @property
    def view(self):
        return self._view()

    def show(self):
        
        self.visible = True
        self.setVisibility(True)

    def hide(self):

        self.visible = False
        self.setVisibility(False)

    def isVisible(self):
        return self.visible
        
    def setVisibility(self, visibility):

        if self._view().isVisible() and self.visible and visibility:
            self.mesh.setVisibility(1)
        else:
            self.mesh.setVisibility(0)

    def getPosition(self):
        return [self.mesh.x, self.mesh.y, self.mesh.z]

    def setPosition(self, position):
        self.__seedMesh.setLoc(position[0], position[1], position[2])
        if self.__proxyMesh:
            self.__proxyMesh.setLoc(position[0], position[1], position[2])
        if self.__subdivisionMesh:
            self.__subdivisionMesh.setLoc(position[0], position[1], position[2])
        if self.__proxySubdivisionMesh:
            self.__proxySubdivisionMesh.setLoc(position[0], position[1], position[2])

    def getRotation(self):
        return [self.mesh.rx, self.mesh.ry, self.mesh.rz]

    def setRotation(self, rotation):
        self.__seedMesh.setRot(rotation[0], rotation[1], rotation[2])
        if self.__proxyMesh:
            self.__proxyMesh.setRot(rotation[0], rotation[1], rotation[2])
        if self.__subdivisionMesh:
            self.__subdivisionMesh.setRot(rotation[0], rotation[1], rotation[2])
        if self.__proxySubdivisionMesh:
            self.__proxySubdivisionMesh.setRot(rotation[0], rotation[1], rotation[2])
            
    def setScale(self, scale, scaleY=None, scaleZ=None):
        if scaleZ:
            self.__seedMesh.setScale(scale, scaleY, scaleZ)
            if self.__proxyMesh:
                self.__proxyMesh.setScale(scale, scaleY, scaleZ)
            if self.__subdivisionMesh:
                self.__subdivisionMesh.setScale(scale, scaleY, scaleZ)
            if self.__proxySubdivisionMesh:
                self.__proxySubdivisionMesh.setScale(scale, scaleY, scaleZ)
        elif scaleY:
            self.__seedMesh.setScale(scale, scaleY, 1)
            if self.__proxyMesh:
                self.__proxyMesh.setScale(scale, scaleY, 1)
            if self.__subdivisionMesh:
                self.__subdivisionMesh.setScale(scale, scaleY, 1)
            if self.__proxySubdivisionMesh:
                self.__proxySubdivisionMesh.setScale(scale, scaleY, 1)
        else:
            self.__seedMesh.setScale(scale, scale, 1)
            if self.__proxyMesh:
                self.__proxyMesh.setScale(scale, scale, 1)
            if self.__subdivisionMesh:
                self.__subdivisionMesh.setScale(scale, scale, 1)
            if self.__proxySubdivisionMesh:
                self.__proxySubdivisionMesh.setScale(scale, scale, 1)

    def setTexture(self, texture):
        if texture:
            self.__seedMesh.setTexture(texture)
            if self.__proxyMesh:
                self.__proxyMesh.setTexture(texture)
            if self.__subdivisionMesh:
                self.__subdivisionMesh.setTexture(texture)
            if self.__proxySubdivisionMesh:
                self.__proxySubdivisionMesh.setTexture(texture)
        else:
            self.clearTexture()
            
    def getTexture(self):
        return self.__seedMesh.texture

    def clearTexture(self):
        self.__seedMesh.clearTexture()
        if self.__proxyMesh:
            self.__proxyMesh.clearTexture()
        if self.__subdivisionMesh:
            self.__subdivisionMesh.clearTexture()
        if self.__proxySubdivisionMesh:
            self.__proxySubdivisionMesh.clearTexture()
            
    def hasTexture(self):
        return self.__seedMesh.hasTexture()
        
    def setSolid(self, solid):
        self.__seedMesh.setSolid(solid)
        if self.__proxyMesh:
            self.__proxyMesh.setSolid(solid)
        if self.__subdivisionMesh:
            self.__subdivisionMesh.setSolid(solid)
        if self.__proxySubdivisionMesh:
            self.__proxySubdivisionMesh.setSolid(solid)
            
    def isSolid(self):
        return self.__seedMesh.solid
        
    def getSeedMesh(self):
        return self.__seedMesh
        
    def getProxyMesh(self):
        return self.__proxyMesh
        
    def updateProxyMesh(self):
    
        if self.proxy and self.__proxyMesh:
            self.proxy.update(self.__proxyMesh, self.__seedMesh)
            self.__proxyMesh.update()
        
    def isProxied(self):
    
        return self.mesh == self.__proxyMesh or self.mesh == self.__proxySubdivisionMesh
        
    def setProxy(self, proxy):
    
        if self.proxy:
        
            self.proxy = None
            self.__proxyMesh.clear()
            self.__proxyMesh = None
            if self.__proxySubdivisionMesh:
                self.__proxySubdivisionMesh.clear()
                self.__proxySubdivisionMesh = None
            self.mesh = self.__seedMesh
            self.mesh.setVisibility(1)
    
        if proxy:
        
            self.proxy = proxy
            
            (folder, name) = proxy.obj_file
            
            self.__proxyMesh = files3d.loadMesh(os.path.join(folder, name))
            self.__proxyMesh.x, self.__proxyMesh.y, self.__proxyMesh.z = self.mesh.x, self.mesh.y, self.mesh.z
            self.__proxyMesh.rx, self.__proxyMesh.ry, self.__proxyMesh.rz = self.mesh.rx, self.mesh.ry, self.mesh.rz
            self.__proxyMesh.sx, self.__proxyMesh.sy, self.__proxyMesh.sz = self.mesh.sx, self.mesh.sy, self.mesh.sz
            self.__proxyMesh.visibility = self.mesh.visibility
            self.__proxyMesh.shadeless = self.mesh.shadeless
            self.__proxyMesh.pickable = self.mesh.pickable
            self.__proxyMesh.cameraMode = self.mesh.cameraMode
            self.__proxyMesh.texture = self.mesh.texture
            
            self.__proxyMesh.object = self.mesh.object
            
            self.proxy.update(self.__proxyMesh, self.__seedMesh)
            
            if self.__seedMesh.object3d:
                self.__proxyMesh.attach()
            
            self.mesh.setVisibility(0)
            self.mesh = self.__proxyMesh
            self.mesh.setVisibility(1)
            
    def getSubdivisionMesh(self, update=True, progressCallback=None):
        
        if self.isProxied():
            if not self.__proxySubdivisionMesh:
                self.__proxySubdivisionMesh = createSubdivisionObject(self.__proxyMesh, progressCallback)
                if self.__seedMesh.object3d:
                    self.__proxySubdivisionMesh.attach()
            elif update:
                updateSubdivisionObject(self.__proxySubdivisionMesh, progressCallback)
                
            return self.__proxySubdivisionMesh
        else:
            if not self.__subdivisionMesh:
                self.__subdivisionMesh = createSubdivisionObject(self.__seedMesh, progressCallback)
                if self.__seedMesh.object3d:
                    self.__subdivisionMesh.attach()
            elif update:
                updateSubdivisionObject(self.__subdivisionMesh, progressCallback)
                
            return self.__subdivisionMesh

    def isSubdivided(self):

        return self.mesh == self.__subdivisionMesh or self.mesh == self.__proxySubdivisionMesh
            
    def setSubdivided(self, flag, update=True, progressCallback=None):

        if flag == self.isSubdivided():
            return
            
        if flag:
            self.mesh.setVisibility(0)
            self.mesh = self.getSubdivisionMesh(update, progressCallback)
            self.mesh.setVisibility(1)
        else:
            self.mesh.setVisibility(0)
            self.mesh = self.__seedMesh if self.mesh == self.__subdivisionMesh else self.__proxyMesh
            if update:
                self.mesh.calcNormals()
                self.mesh.update()
            self.mesh.setVisibility(1)
            
    def updateSubdivisionMesh(self):
    
        self.getSubdivisionMesh(True)
            
    def onMouseDown(self, event):
        self._view().callEvent('onMouseDown', event)

    def onMouseMoved(self, event):
        self._view().callEvent('onMouseMoved', event)

    def onMouseDragged(self, event):
        self._view().callEvent('onMouseDragged', event)

    def onMouseUp(self, event):
        self._view().callEvent('onMouseUp', event)

    def onMouseEntered(self, event):
        self._view().callEvent('onMouseEntered', event)

    def onMouseExited(self, event):
        self._view().callEvent('onMouseExited', event)

    def onClicked(self, event):
        self._view().callEvent('onClicked', event)

    def onMouseWheel(self, event):
        self._view().callEvent('onMouseWheel', event)

    def onKeyDown(self, event):
        self._view().callEvent('onKeyDown', event)

    def onKeyUp(self, event):
        self._view().callEvent('onKeyDown', event)

class View(events3d.EventHandler):

    """
    The base view from which all widgets are derived.
    """

    def __init__(self):

        self.children = []
        self.objects = []
        self._visible = False
        self._totalVisibility = False
        self._parent = None
        self._attached = False
        self.widgets = []
        
    @property
    def parent(self):
        if self._parent:
            return self._parent();
        else:
            return None
            
    def _attach(self):
        
        self._attached = True
        
        for object in self.objects:
            object._attach()
            
        for child in self.children:
            child._attach()
        
    def _detach(self):
    
        self._attached = False
        
        for object in self.objects:
            object._detach()
            
        for child in self.children:
            child._detach()
        
    def addView(self, view):
        """
        Adds the view to this view. If this view is attached to the app, the view will also be attached.
        
        :param view: The view to be added.
        :type view: gui3d.View
        :return: The view, for convenience.
        :rvalue: gui3d.View
        """
        if view.parent:
            raise RuntimeException('The view is already added to a view')
            
        view._parent = weakref.ref(self)
        view._updateVisibility()
        if self._attached:
            view._attach()

        self.children.append(view)
            
        return view
    
    def removeView(self, view):
        """
        Removes the view from this view. If this view is attached to the app, the view will be detached.
        
        :param view: The view to be removed.
        :type view: gui3d.View
        """
        if view not in self.children:
            raise RuntimeException('The view is not a child of this view')
            
        view._parent = None
        if self._attached:
            view._detach()
            
        self.children.remove(view)
            
    def addObject(self, object):
        """
        Adds the object to the view. If the view is attached to the app, the object will also be attached and will get an OpenGL counterpart.
        
        :param object: The object to be added.
        :type object: gui3d.Object
        :return: The object, for convenience.
        :rvalue: gui3d.Object
        """
        if object._view:
            raise RuntimeException('The object is already added to a view')
            
        object._view = weakref.ref(self)
        if self._attached:
            object._attach()
            
        self.objects.append(object)
            
        return object
            
    def removeObject(self, object):
        """
        Removes the object from the view. If the object was attached to the app, its OpenGL counterpart will be removed as well.
        
        :param object: The object to be removed.
        :type object: gui3d.Object
        """
        if object not in self.objects:
            raise RuntimeException('The object is not a child of this view')
            
        object._view = None
        if self._attached:
            object._detach()
            
        self.objects.remove(object)
        
    def show(self):
        self._visible = True
        self._updateVisibility()

    def hide(self):
        self._visible = False
        self._updateVisibility()
        
    def isShown(self):
        return self._visible

    def isVisible(self):
        return self._totalVisibility

    def _updateVisibility(self):
        previousVisibility = self._totalVisibility

        self._totalVisibility = self._visible and (not self.parent or self.parent.isVisible())

        for o in self.objects:
            o.setVisibility(self._totalVisibility)

        for v in self.children:
            v._updateVisibility()

        if self._totalVisibility != previousVisibility:
            if self._totalVisibility:
                self.callEvent('onShow', None)
            else:
                self.callEvent('onHide', None)

    def onShow(self, event):
        self.show()

    def onHide(self, event):
        self.hide()

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

    def addWidget(self, widget):
        self.widgets.append(widget)
        widget._parent = self
        if self.isVisible():
            widget.show()
        else:
            widget.hide()
        return widget

    def removeWidget(self, widget):
        self.widgets.remove(widget)

    def showWidgets(self):
        for w in self.widgets:
            w.show()

    def hideWidgets(self):
        for w in self.widgets:
            w.hide()

class TaskView(View):

    def __init__(self, category, name, label=None):
        super(TaskView, self).__init__()
        self.name = name
        self.label = label
        self.focusWidget = None
        self.tab = None

    def getModifiers(self):
        return {}

    # return list of pairs of modifier names for symmetric body parts
    # each pair is defined as { 'left':<left modifier name>, 'right':<right modifier name> }
    def getSymmetricModifierPairNames(self):
        return []

    # return list of singular modifier names
    def getSingularModifierNames(self):
        return []

class Category(View):

    def __init__(self, name, label = None):
        super(Category, self).__init__()
        self.name = name
        self.label = label
        self.tasks = []
        self.tasksByName = {}
        self.tab = None
        self.tabs = None

    def _taskTab(self, task):
        if task.tab is None:
            task.tab = self.tabs.addTab(task.name, task.label or task.name)

    def realize(self, app):
        for task in self.tasks:
            self._taskTab(task)

        @self.tabs.mhEvent
        def onTabSelected(tab):
            app.switchTask(tab.name)

    def addTask(self, task):
        if task.name in self.tasksByName:
            raise KeyError('A task with this name already exists', task.name)
        self.tasks.append(task)
        self.tasksByName[task.name] = task
        self.addView(task)
        if self.tabs is not None:
            self._taskTab(task)
        return task

    def getTaskByName(self, name):
        return self.tasksByName.get(name)
 
# The application
app = None

class Application(events3d.EventHandler):
    """
   The Application.
    """
    
    singleton = None

    def __init__(self):
        global app
        app = self
        self.parent = self
        self.children = []
        self.objects = []
        self.categories = {}
        self.currentCategory = None
        self.currentTask = None
        self.mouseDownObject = None
        self.enteredObject = None
        self.fullscreen = False
        self.width = 800
        self.height = 600
        
        mh.setMouseDownCallback(self.onMouseDownCallback)
        mh.setMouseUpCallback(self.onMouseUpCallback)
        mh.setMouseMovedCallback(self.onMouseMovedCallback)
        mh.setMouseWheelCallback(self.onMouseWheelCallback)
        mh.setKeyDownCallback(self.onKeyDownCallback)
        mh.setKeyUpCallback(self.onKeyUpCallback)
        mh.setResizeCallback(self.onResizedCallback)
        mh.setQuitCallback(self.onQuitCallback)

        mh.startWindow(1)
        
    def started(self):
        self.callEvent('onStart', None)

    def run(self):
        """
        Starts the event loop
        """
        mh.callAsync(self.started)
        mh.startEventLoop()

    def stop(self):
        self.callEvent('onStop', None)
        mh.shutDown()
        
    def redraw(self):
        """
        Redraws the screen once control is returned to the event handler.
        """
        mh.redraw(1)
        
    def redrawNow(self):
        """
        Redraws immediately.
        """
        mh.redraw(0)
        
    def getWindowSize(self):
        """
        Returns the current window size.
        
        :returns: The current window size.
        :rtype: (int, int)
        """
        return mh.getWindowSize()
        
    def addObject(self, object):
        """
        Adds the object to the application. The object will also be attached and will get an OpenGL counterpart.
        
        :param object: The object to be added.
        :type object: gui3d.Object
        :return: The object, for convenience.
        :rvalue: gui3d.Object
        """
        if object._view:
            raise RuntimeException('The object is already attached to a view')
            
        object._view = weakref.ref(self)
        object._attach()
        
        self.objects.append(object)
            
        return object
            
    def removeObject(self, object):
        """
        Removes the object from the application. Its OpenGL counterpart will be removed as well.
        
        :param object: The object to be removed.
        :type object: gui3d.Object
        """
        if object not in self.objects:
            raise RuntimeException('The object is not a child of this view')
            
        object._view = None
        object._detach()
        
        self.objects.remove(object)
        
    def addView(self, view):
        """
        Adds the view to the application.The view will also be attached.
        
        :param view: The view to be added.
        :type view: gui3d.View
        :return: The view, for convenience.
        :rvalue: gui3d.View
        """
        if view.parent:
            raise RuntimeException('The view is already attached')
            
        view._parent = weakref.ref(self)
        view._updateVisibility()
        view._attach()
        
        self.children.append(view)
            
        return view
    
    def removeView(self, view):
        """
        Removes the view from the application. The view will be detached.
        
        :param view: The view to be removed.
        :type view: gui3d.View
        """
        if view not in self.children:
            raise RuntimeException('The view is not a child of this view')
            
        view._parent = None
        view._detach()
        
        self.children.remove(view)

    def isVisible(self):
        return True
            
    def getSelectedFaceGroupAndObject(self):
    
        return module3d.selectionColorMap.getSelectedFaceGroupAndObject()
        
    def getSelectedFaceGroup(self):
    
        return module3d.selectionColorMap.getSelectedFaceGroup()

    def addCategory(self, category):
        if category.name in self.categories:
            raise KeyError('A category with this name already exists', category.name)

        if category.parent:
            raise RuntimeException('The category is already attached')

        self.categories[category.name] = category
        category.tab = self.tabs.addTab(category.name, category.label or category.name)
        category.tabs = category.tab.child
        self.addView(category)
        category.realize(self)

        return category

    def switchTask(self, name):
        if self.currentTask and self.currentTask.name == name:
            return

        if self.currentTask:
            print 'hiding task %s' % self.currentTask.name
            self.currentTask.hide()
            self.currentTask.hideWidgets()

        self.currentTask = self.currentCategory.tasksByName[name]

        if self.currentTask:
            print 'showing task %s' % self.currentTask.name
            self.currentTask.show()
            self.currentTask.showWidgets()

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
            print 'hiding category %s' % self.currentCategory.name
            self.currentCategory.hide()
            self.currentCategory.hideWidgets()

        self.currentCategory = category

        print 'showing category %s' % self.currentCategory.name
        self.currentCategory.show()
        self.currentCategory.showWidgets()

        self.switchTask(category.tasks[0].name)

    # called from native

    def onMouseDownCallback(self, button, x, y):
        # Build event
        event = events3d.MouseEvent(button, x, y)

        # Get picked object
        pickedObject = self.getSelectedFaceGroupAndObject()
        if pickedObject:
            object = pickedObject[1].object
        else:
            object = self

        # It is the object which will receive the following mouse messages

        self.mouseDownObject = object

        # Send event to the object

        object.callEvent('onMouseDown', event)

    def onMouseUpCallback(self, button, x, y):
        if button == 4 or button == 5:
            return

        # Build event
        event = events3d.MouseEvent(button, x, y)

        # Get picked object
        pickedObject = self.getSelectedFaceGroupAndObject()
        if pickedObject:
            object = pickedObject[1].object
        else:
            object = self
                
        if self.mouseDownObject:
            self.mouseDownObject.callEvent('onMouseUp', event)
            if self.mouseDownObject is object:
                self.mouseDownObject.callEvent('onClicked', event)

    def onMouseMovedCallback(self, mouseState, x, y, xRel, yRel):
        
        # Build event
        event = events3d.MouseEvent(mouseState, x, y, xRel, yRel)

        # Get picked object

        picked = self.getSelectedFaceGroupAndObject()
        
        if picked:
            group = picked[0]
            object = picked[1].object or self
        else:
            group = None
            object = self

        event.object = object
        event.group = group

        if mouseState:
            if self.mouseDownObject:
                self.mouseDownObject.callEvent('onMouseDragged', event)
        else:
            if self.enteredObject != object:
                if self.enteredObject:
                    self.enteredObject.callEvent('onMouseExited', event)
                self.enteredObject = object
                self.enteredObject.callEvent('onMouseEntered', event)
            object.callEvent('onMouseMoved', event)

    def onMouseWheelCallback(self, wheelDelta, x, y):
        event = events3d.MouseWheelEvent(wheelDelta)
        if self.currentTask:
            self.currentTask.callEvent('onMouseWheel', event)

    def onKeyDownCallback(self, key, character, modifiers):
        event = events3d.KeyEvent(key, character, modifiers)
        if self.currentTask:
            self.currentTask.callEvent('onKeyDown', event)

    def onKeyUpCallback(self, key, character, modifiers):
        event = events3d.KeyEvent(key, character, modifiers)
        if self.currentTask:
            self.currentTask.callEvent('onKeyUp', event)
            
    def onResizedCallback(self, width, height, fullscreen):
        if self.fullscreen != fullscreen:
            module3d.reloadTextures()
        self.fullscreen = fullscreen
        
        event = events3d.ResizeEvent(width, height, fullscreen, width - self.width, height - self.height)
        
        self.width = width
        self.height = height
        
        self.callEvent('onResized', event)
        
        for category in self.categories.itervalues():
            
            category.callEvent('onResized', event)
            
            for task in category.tasks:
                
                task.callEvent('onResized', event)
                
    def onQuitCallback(self):
        self.callEvent('onQuit', None)
            
    def getCategory(self, name):
        category = self.categories.get(name)
        if category:
            return category
        return self.addCategory(Category(name))

