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
import log

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
        
    def _attach(self):
    
        if self._view().isVisible() and self.visible:
            self.mesh.setVisibility(1)
        else:
            self.mesh.setVisibility(0)

        for mesh in self._meshes():
            mesh.attach()
            
    def _detach(self):
        for mesh in self._meshes():
            mesh.detach()

    def _meshes(self):
        for mesh in (self.__seedMesh,
                     self.__proxyMesh,
                     self.__subdivisionMesh,
                     self.__proxySubdivisionMesh):
            if mesh is not None:
                yield mesh

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
        for mesh in self._meshes():
            mesh.setLoc(position[0], position[1], position[2])

    def getRotation(self):
        return [self.mesh.rx, self.mesh.ry, self.mesh.rz]

    def setRotation(self, rotation):
        for mesh in self._meshes():
            mesh.setRot(rotation[0], rotation[1], rotation[2])
            
    def setScale(self, scale, scaleY=None, scaleZ=1):
        if scaleY is None:
            scaleY = scale
        for mesh in self._meshes():
            mesh.setScale(scale, scaleY, scaleZ)

    def setTexture(self, texture):
        if texture:
            for mesh in self._meshes():
                mesh.setTexture(texture)
        else:
            self.clearTexture()
            
    def getTexture(self):
        return self.__seedMesh.texture

    def clearTexture(self):
        for mesh in self._meshes():
            mesh.clearTexture()
            
    def hasTexture(self):
        return self.__seedMesh.hasTexture()
        
    def setSolid(self, solid):
        for mesh in self._meshes():
            mesh.setSolid(solid)
            
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
            for attr in ('x', 'y', 'z', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz',
                         'visibility', 'shadeless', 'pickable', 'cameraMode', 'texture'):
                setattr(self.__proxyMesh, attr, getattr(self.mesh, attr))
            
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

    def addTopWidget(self, widget):
        mh.addTopWidget(widget)
        self.widgets.append(widget)
        widget._parent = self
        if self.isVisible():
            widget.show()
        else:
            widget.hide()
        return widget

    def removeTopWidget(self, widget):
        self.widgets.remove(widget)
        mh.removeTopWidget(widget)

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
        self.left, self.right = mh.addPanels()

    def getModifiers(self):
        return {}

    # return list of pairs of modifier names for symmetric body parts
    # each pair is defined as { 'left':<left modifier name>, 'right':<right modifier name> }
    def getSymmetricModifierPairNames(self):
        return []

    # return list of singular modifier names
    def getSingularModifierNames(self):
        return []

    def showWidgets(self):
        super(TaskView, self).showWidgets()
        mh.showPanels(self.left, self.right)

    def addLeftWidget(self, widget):
        return self.left.addWidget(widget)

    def addRightWidget(self, widget):
        return self.right.addWidget(widget)

    def removeLeftWidget(self, widget):
        self.left.removeWidget(widget)

    def removeRightWidget(self, widget):
        self.right.removeWidget(widget)

class Category(View):

    def __init__(self, name, label = None):
        super(Category, self).__init__()
        self.name = name
        self.label = label
        self.tasks = []
        self.tasksByName = {}
        self.tab = None
        self.tabs = None
        self.panel = None
        self.task = None

    def _taskTab(self, task):
        if task.tab is None:
            task.tab = self.tabs.addTab(task.name, task.label or task.name)

    def realize(self, app):
        for task in self.tasks:
            self._taskTab(task)

        @self.tabs.mhEvent
        def onTabSelected(tab):
            self.task = tab.name
            app.switchTask(tab.name)

    def addTask(self, task):
        if task.name in self.tasksByName:
            raise KeyError('A task with this name already exists', task.name)
        self.tasks.append(task)
        self.tasksByName[task.name] = task
        self.addView(task)
        if self.tabs is not None:
            self._taskTab(task)
        if self.task is None:
            self.task = task.name
        return task

    def getTaskByName(self, name):
        return self.tasksByName.get(name)

    def showWidgets(self):
        super(Category, self).showWidgets()
        mh.showPanelBottomLeft(self.panel)

    def addBottomWidget(self, widget):
        if self.panel is None:
            self.panel = mh.addPanelBottomLeft()
        return self.panel.addWidget(widget)

    def removeBottomWidget(self, widget):
        self.panel.removeWidget(widget)
 
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
        newTask = self.currentCategory.tasksByName[name]

        if self.currentTask and self.currentTask is newTask:
            return

        if self.currentTask:
            log.debug('hiding task %s', self.currentTask.name)
            self.currentTask.hide()
            self.currentTask.hideWidgets()

        self.currentTask = self.currentCategory.tasksByName[name]

        if self.currentTask:
            log.debug('showing task %s', self.currentTask.name)
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
            log.debug('hiding category %s', self.currentCategory.name)
            self.currentCategory.hide()
            self.currentCategory.hideWidgets()

        self.currentCategory = category

        log.debug('showing category %s', self.currentCategory.name)
        self.currentCategory.show()
        self.currentCategory.showWidgets()

        self.switchTask(category.task)

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

