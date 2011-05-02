#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d

print 'example imported'


class ExampleTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Example')

        y = 80
        box = gui3d.GroupBox(self, label = 'Example', position=[10, y, 9.0], style=gui3d.GroupBoxStyle._replace(height=320));y+=35
        
        # We add a button to the current task
        # A button just fires an event when it is clicked, if a selected texture is specified,
        # it is used while the mouse is down on the button

        self.aButton = gui3d.Button(box, position=[18, y, 9.1], label='Button');y+=28
        
        self.pushed = 0
        self.aButtonLabel = gui3d.TextView(box, position=[18, y, 9.1], label='Pushed 0 times');y+=28

        @self.aButton.event
        def onClicked(event):
            self.pushed += 1
            self.aButtonLabel.setText('Pushed %d times' % self.pushed)

        # We add a toggle button to the current task
        # A toggle button fires an event when it is clicked but retains its selected state after the mouse is up,
        # if a selected texture is specified, it is used to show whether the button is toggled

        self.aToggleButton = gui3d.ToggleButton(box, position=[18, y, 9.1], label='ToggleButton');y+=28

        self.aToggleButtonLabel = gui3d.TextView(box, position=[18, y, 9.1], label='Not selected');y+=28

        @self.aToggleButton.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.aToggleButton, event)
            if self.aToggleButton.selected:
                self.aToggleButtonLabel.setText('Selected')
            else:
                self.aToggleButtonLabel.setText('Not selected')

        # Next we will add some radio buttons. For this we need a group, since only one in the group can be selected
        # A radio button fires an event when it is clicked but retains its selected state after the mouse is up, and deselects all other buttons in the group
        # If a selected texture is specified, it is used to show whether the button is selected

        self.aRadioButtonGroup = []

         # We make the first one selected
        self.aRadioButton1 = gui3d.RadioButton(box, self.aRadioButtonGroup, position=[18, y, 9.1], selected=True, label='RadioButton1');y+=28
        self.aRadioButton2 = gui3d.RadioButton(box, self.aRadioButtonGroup, position=[18, y, 9.1], label='RadioButton2');y+=28

        self.aRadioButtonLabel = gui3d.TextView(box, position=[18, y, 9.1], label='Button 1 is selected');y+=18

        @self.aRadioButton1.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.aRadioButton1, event)
            self.aRadioButtonLabel.setText('Button 1 is selected')

        @self.aRadioButton2.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.aRadioButton2, event)
            self.aRadioButtonLabel.setText('Button 2 is selected')

        # When the slider is dragged and released, an onChange event is fired
        # By default a slider goes from 0.0 to 1.0, and the initial position will be 0.0 unless specified

        # We want the slider to start from the middle
        self.aSlider = gui3d.Slider(box, position=[10, y, 9.1], value=0.5, label='Slider');y+=38

        self.aSliderLabel = gui3d.TextView(box, position=[18, y, 9.1], label='Value is 0.5');y+=28

        @self.aSlider.event
        def onChange(value):
            self.aSliderLabel.setText('Value is %f' % value)
            self.aProgressBar.setProgress(value, 1)

        # we also create a progressbar, which is updated as the slider moves

        self.aProgressBar = gui3d.ProgressBar(box, position=[0,0,0], style=gui3d.ProgressBarStyle._replace(width=112, margin=[2,2,2,2]))
        self.aProgressBar.setProgress(0.5, 0)
        
        # A text edit

        self.aTextEdit = gui3d.TextEdit(box, position=[18, y, 9.1], text='Some text', style=gui3d.TextEditStyle._replace(width=112))


category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = gui3d.Category(app, 'Example')
    taskview = ExampleTaskView(category)

    print 'example loaded'
    print 'Hello world'


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'example unloaded'


