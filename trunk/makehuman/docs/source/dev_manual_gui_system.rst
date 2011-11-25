.. _gui_system:

.. highlight:: python
   :linenothreshold: 5


GUI system
===========

.. figure::  _static/guy_system.png
   :align:   center
   
Application
------------

This is the main object in a certain application, it sets up the default categories and views, and loads the plugins.

Category
---------

A category collects different tasks which work on similar aspects of the model, like modelling.

Task
-----

A task makes it possible to work on a certain aspect of the model, or implements another function in the application like saving or loading.

Object
-------

A 3d mesh which can be clicked on.

EventHandler
-------------

An EventHandler is a class which can receive events. Handlers for events can be attached to the EventHandler by defining the method in the class:

::

    class MyClass(EventHandler):
        def onMyEvent(self, event):
            print("got onMyEvent")

However sometimes it can be bothersome to create a sub class each time you need different behavior in the handler. For this you can use the event decorator:

::

    class MyParentClass:
        def __init__():
            self.myFirstClass = MyClass()
            
            @self.myFirstClass.event
            def onMyEvent(event):
                print("got onMyEvent in myFirstClass")

            self.mySecondClass = MyClass()

            @self.mySecondClass.event
            def onMyEvent(event):
                print("got onMyEvent in mySecondClass")

However note that using self here, will always give MyParentClass. If you need the self of the MyClass instance, use self.myFirstClass or self.mySecondClass in the handler.
View (EventHandler)
A view is a container holding other views and objects. When it is shown or hidden, all the views and objects it contains are shown or hidden as well (providing they are not individually hidden themselves). Views also have the notion of a focus. There is only one view which can have the focus at a time. The focussed view will receive all keyboard input.

Additional properties are:

* parent: optional, defaults to None.
* visible: optional, defaults to True.


Additional events are:

* onShow/onHide: fired when the view's visibility changes.
* onFocus/onBlur: fired when the view's focus status changes.

Widgets
========

Button (View)
--------------

A button is a standard push button. It has a selected state, which is only true when it is being pushed (between mouse down and mouse up).

Additional properties are:

* selected: boolean indicating whether a button is showing itself as selected.
* selectedTexture: a string indicating the optional texture to use when the button is selected.


Additional events are:

    onSelected: fired when the button's selected status changes.

ToggleButton (Button)
A ToggleButton is a button which stays selected after you click it once, and deselects when you click it again.

Additional properties are:

    none

RadioButton (Button)
---------------------

A RadioButton is a button which can be put in a group. When one of the RadioButtons in a group is selected, all the others are deselected.

Additional properties are:

    group: a list of RadioButtons which are exclusive.

Slider
-------

A Slider is a widget allowing the user to select a value in a certain range.

Additional properties are:

* backgroundTexture: a string indicating the texture to use as the background of the slider.
* sliderTexture: a string indicating the texture to use as the slider of the slider.
* value: optional current value, if not given defaults to 0.0.
* min: optional minimum value, if not given defaults to 0.0.
* max: optional maximum value, if not given defaults to 1.0.

Additional events are:

* onChange: fired when the slider's value changes.

ProgressBar
------------

A ProgressBar shows the progress of a lengthy operation. 

Additional properties are:

* backgroundMesh: a string indicating the mesh to use as the background of the progressbar.
* backgroundTexture: a string indicating the texture to use as the background of the progressbar.
* backgroundPosition: position of the background
* barMes : a string indicating the mesh to use as the bar of the progressbar.
* barTexture: a string indicating the texture to use as the bar of the progressbar.
* barPosition: position of the bar

Event flow
===========

Mouse event
-------------

Application -> View under mouse

Remarks:

    If left click, set focus if the view accepts focus.
    MouseUp is only received after MouseDown
    MouseDragged is between iMouseDown and MouseUp
    MouseMoved is not between iMouseDown and MouseUp

Keyboard event
Application -> Focus View



