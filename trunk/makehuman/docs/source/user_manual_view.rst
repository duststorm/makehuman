.. _theview:

.. highlight:: python
   :linenothreshold: 5

*********
The view
*********

Mouse movement
===============

The model can be freely moved and rotated using the mouse. Keep the left button pressed to rotate the model. Keep the right button pressed to translate the model. Zooming can be done by using the scroll wheel, or by keeping both the left and right button
pressed. If the manipulation speed is too slow, hold shift to speed up movement.


Keyboard movement
==================

The following keyboard navigation is the standard navigation. It can be customized in settings, shortcuts. Use the arrow keys to move the model around. Use the 2, 4, 6 and 8 keys to rotate the model. Use the + and - keys to zoom. There are 3 standard views
which have shortcut keys. For a side view press 7, for a front view press 1 and for a top view press 3. The . key resets both position and zoom.


View options
=============

There are 4 view options which might help during modeling: background, anaglyphs, wireframe and smooth.

Background
-----------

The background mode shows an image ﬁle on top of the model. This is useful when the model should resemble an existing sketch, photograph or render. The ﬁrst time it is activated, it shows a list of ﬁles from the ~/makehuman/backgrounds folder to choose from. 

Afterward the background button toggles the background on and off. To choose another image go to library, background.

Anaglyphs
----------

Anaglyphs mode renders the view from two viewpoints in red and cyan. When viewing this using red-cyan 3d glasses you can see the model in real 3d. There are two anaglyphs modes which use a slightly different method to render both views, so it takes two presses of the button to turn it back off.

Wireframe
----------

Wireframe mode is good to see the topology and how vertices and faces are changed by certain modiﬁcations. 

Smooth
-------

Smooth view might be too slow to work with on some systems. It subdivides the mesh with Catmull-Clark subdivision and keeps this subdivided mesh updated when modifying the model.


Cameras
========

There are two camera viewpoints between which can be quickly toggled, global camera and face camera.

Undo, redo and reset
=====================

These are not view options, but they appear throughout the application. Undo and redo are quite straightforward, they undo the last modiﬁcation or redo the last undone modiﬁcation. Reset removes all modiﬁcations, be careful as it is impossible to undo this action.


*********
Modeling
*********

.. figure::  _static/modelling.png
   :align:   center

Macro modeling
===============

Macro modeling is the roughest step in modeling a human, but it also has the biggest impact on the resulting mesh. Macro modeling has 5 sliders. The ﬁrst 4 sliders modify the 4 main dimensions of the human: gender, age, muscle and weight. 

The last slider, height, modiﬁes the proportions. The functionality of the gender and age sliders are straightforward. Gender goes from female to male, initially it is at 50% of each, which gives a neutral gender. 

Age goes from 12 years old to 70 years old, initially it is at 25 years old. The muscle and weight sliders inﬂuence each other. Only increasing muscle you doesn't create a bodybuilder, that also requires weight. 

Similarly only increasing weight doesn't create a really fat model, that also requires less muscle. Finally as said before the height slider doesn't just scale the model vertically, but it changes the
