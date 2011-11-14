
.. highlight:: python
   :linenothreshold: 5
   
.. _gui_controls:

GUI controls
============

Whether you are writing an exporter, modeling feature or mesh algorithm, sooner or
later you will need to add some controls in order to interact with the user. MakeHuman
has a lot of the usual controls which you find in in other GUI toolkits:

    * Button: A regular push button.
    * ToggleButton: A button which has two states, selected and deselected, clicking the button toggles between the states. Used for making an on/off choice.
    * CheckBox: A togglebutton, but with a check box look.
    * RadioButton: A button which is part of a group, clicking one of the buttons selects it and deselects the others. Used for a multiple choice.
    * Slider: Used to select a value from a discrete or continous range.
    * TextEdit: A one line text field.
    * TextView: A label.
    * GroupBox: Used to group a few controls together under a title.


