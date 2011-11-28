
.. highlight:: python
   :linenothreshold: 5
   
.. _gui_controls:

###############
GUI controls
###############

Whether you are writing an exporter, modeling feature or mesh algorithm, sooner or later you will need to add some controls in order to interact with the user. MakeHuman has a lot of the usual controls which you find in in other GUI toolkits:

* Button: A regular push button.
* ToggleButton: A button which has two states, selected and deselected, clicking the button toggles between the states. Used for making an on/off choice.
* CheckBox: A togglebutton, but with a check box look.
* RadioButton: A button which is part of a group, clicking one of the buttons selects it and deselects the others. Used for a multiple choice.
* Slider: Used to select a value from a discrete or continous range.
* TextEdit: A one line text field.
* TextView: A label.
* GroupBox: Used to group a few controls together under a title.
  
********************    
Layout guidelines
********************

To have a consistent look, it is important that all tasks use the same layout practices. GroupBoxes on the left side have x=10. The first GroupBox starts at y=80. Controls start
25 pixels lower, and after the last control there are 6 extra pixels (besides the 4 pixels spacing from the last control). So the total height of a GroupBox is 25+content+6. Sliders start at x=10 and are 128 pixels wide, so there is no border left or right.

Buttons start at x=18 and are 112 wide, so there are 8 pixels of border on each side. Between controls there are 4 pixels. Sliders are 32 pixels high and Buttons are 20 pixels high. This means that the space to the next control for a Slider is 36, and for a Button 24. So the height of a GroupBox can be calculated as 25+36*sliders+24*buttons+6. Between GroupBoxes there are 10 pixels.

When creating a GUI, many of these rules are followed automatically. Controls have default styles assigned which take care of the margin, padding and size of the control. When using GroupBoxes, a BoxLayout will automatically place the controls in rows or columns. Only on a higher level, namely placing the GroupBoxes themselves, some custom positioning has to be done, as well as when reacting to screen resizing.

.. figure::  _static/boxmodel.png
   :align:   center
   
   Padding in yellow, spacing in fuschia, size in green.
       
   
Labels only have the first letter capitalized, unless there is an acronym that needs to be in uppercase.


