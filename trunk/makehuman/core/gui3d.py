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
        
        self.__view = None
        
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
        
    def __attach(self):
    
        if self.__view().isVisible() and self.visible:
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
            
    def __detach(self):
        
        self.__seedMesh.detach()
        if self.__proxyMesh:
            self.__proxyMesh.detach()
        if self.__subdivisionMesh:
            self.__subdivisionMesh.detach()
        if self.__proxySubdivisionMesh:
            self.__proxySubdivisionMesh.detach()
            
    @property
    def view(self):
        return self.__view()

    def show(self):
        
        self.visible = True
        self.setVisibility(True)

    def hide(self):

        self.visible = False
        self.setVisibility(False)

    def isVisible(self):
        return self.visible
        
    def setVisibility(self, visibility):

        if self.__view().isVisible() and self.visible and visibility:
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
            
    def getBBox(self):
        return self.mesh.calcBBox()
        
    def getWidth(self):
        bbox = self.getBBox()
        return bbox[1][0] - bbox[0][0]
        
    def getHeight(self):
        bbox = self.getBBox()
        return bbox[1][1] - bbox[0][1]
        
    def getDepth(self):
        bbox = self.getBBox()
        return bbox[1][2] - bbox[0][2]

    def onMouseDown(self, event):
        self.__view().callEvent('onMouseDown', event)

    def onMouseMoved(self, event):
        self.__view().callEvent('onMouseMoved', event)

    def onMouseDragged(self, event):
        self.__view().callEvent('onMouseDragged', event)

    def onMouseUp(self, event):
        self.__view().callEvent('onMouseUp', event)

    def onMouseEntered(self, event):
        self.__view().callEvent('onMouseEntered', event)

    def onMouseExited(self, event):
        self.__view().callEvent('onMouseExited', event)

    def onClicked(self, event):
        self.__view().callEvent('onClicked', event)

    def onMouseWheel(self, event):
        self.__view().callEvent('onMouseWheel', event)

    def onKeyDown(self, event):
        self.__view().callEvent('onKeyDown', event)

    def onKeyUp(self, event):
        self.__view().callEvent('onKeyDown', event)

class View(events3d.EventHandler):

    """
    The base view from which all widgets are derived.
    """

    def __init__(self):

        self.children = []
        self.objects = []
        self.__visible = False
        self.__totalVisibility = False
        self.__parent = None
        self.__attached = False
        self.widgets = []

    def __del__(self):
    
        del self.children[:]
        del self.objects[:]
        
    @property
    def parent(self):
        if self.__parent:
            return self.__parent();
        else:
            return None
            
    def __attach(self):
        
        self.__attached = True
        
        for object in self.objects:
            object._Object__attach()
            
        for child in self.children:
            child.__attach()
        
    def __detach(self):
    
        self.__attached = False
        
        for object in self.objects:
            object._Object__detach()
            
        for child in self.children:
            child.__detach()
        
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
            
        view.__parent = weakref.ref(self)
        view.__updateVisibility()
        if self.__attached:
            view.__attach()

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
            
        view.__parent = None
        if self.__attached:
            view.__detach()
            
        self.children.remove(view)
            
    def addObject(self, object):
        """
        Adds the object to the view. If the view is attached to the app, the object will also be attached and will get an OpenGL counterpart.
        
        :param object: The object to be added.
        :type object: gui3d.Object
        :return: The object, for convenience.
        :rvalue: gui3d.Object
        """
        if object._Object__view:
            raise RuntimeException('The object is already added to a view')
            
        object._Object__view = weakref.ref(self)
        if self.__attached:
            object._Object__attach()
            
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
            
        object._Object__view = None
        if self.__attached:
            object._Object__detach()
            
        self.objects.remove(object)
        
    def show(self):
        self.__visible = True
        self.__updateVisibility()

    def hide(self):
        self.__visible = False
        self.__updateVisibility()
        
    def isShown(self):
        return self.__visible

    def isVisible(self):
        return self.__totalVisibility

    def setFocus(self):
        app.setFocus(self)

    def hasFocus(self):
        return app.focusView is self
        
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
        View.__init__(self)
        self.name = name
        self.focusWidget = None

        if name in category.tasksByName:
            raise KeyError('A task with this name already exists', name)

        category.tasks.append(self)
        category.tasksByName[self.name] = self

        self.tab = category.tabs.addTab(name, label or name)
            
    def canFocus(self):
        return False

    def onShow(self, event):

        self.tab.setSelected(True)
        self.show()

    def onHide(self, event):

        self.tab.setSelected(False)
        self.hide()

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

    def __init__(self, app, name, label = None):
        
        View.__init__(self)
        
        self.name = name
        self.tasks = []
        self.tasksByName = {}

        if name in app.categories:
            raise KeyError('A category with this name already exists', name)

        app.categories[name] = self
        self.tab = app.tabs.addTab(name, label or name)
        
        self.tabs = self.tab.child
        
        @self.tabs.mhEvent
        def onTabSelected(tab):
            app.switchTask(tab.name)
            
    def canFocus(self):
        return False

    def onShow(self, event):
        self.tab.setSelected(True)
        self.show()

    def onHide(self, event):
        self.tab.setSelected(False)
        self.hide()

    def getViewByName(self, viewName):
        """
        Retrieve a view by name. Return the view or None if no matching view found.

        :param viewName: The name of the view to be retrieved.
        """
        for view in self.children:
            if hasattr(view, 'name'):
                if view.name == viewName:
                    return view
        
        return None
 
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
        self.focusView = None
        self.focusObject = None
        self.focusGroup = None
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
        if object._Object__view:
            raise RuntimeException('The object is already attached to a view')
            
        object._Object__view = weakref.ref(self)
        object._Object__attach()
        
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
            
        object._Object__view = None
        object._Object__detach()
        
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
            
        view._View__parent = weakref.ref(self)
        view._View__updateVisibility()
        view._View__attach()
        
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
            
        view._View__parent = None
        view._View__detach()
        
        self.children.remove(view)

    def isVisible(self):
        return True
        
    def canFocus(self):
        return False

    def setFocus(self, view=None):

        #print ('setFocus', view)

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
            
    def getSelectedFaceGroupAndObject(self):
    
        return module3d.selectionColorMap.getSelectedFaceGroupAndObject()
        
    def getSelectedFaceGroup(self):
    
        return module3d.selectionColorMap.getSelectedFaceGroup()

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

        # If we have an object
        # Try to give its view focus
        if object != self:
            self.focusObject = object
            self.focusObject.view.setFocus()

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

        # Mouse wheel events, like key events are sent to the focus view

        event = events3d.MouseWheelEvent(wheelDelta)
        if self.focusView:
            self.focusView.callEvent('onMouseWheel', event)
        elif self.currentTask:
            self.currentTask.callEvent('onMouseWheel', event)

    def onKeyDownCallback(self, key, character, modifiers):
        if key == mh.Keys.TAB:
            if self.focusView:

            # if self.focusView.wantsTab and not (modifiers & mh.Modifiers.CTRL):

                index = self.focusView.parent.children.index(self.focusView)
                if modifiers & mh.Modifiers.SHIFT:
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
        try:
            return self.categories[name]
        except:
            return self.addView(Category(self, name, None))

