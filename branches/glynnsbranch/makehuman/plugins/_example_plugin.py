#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d

print 'example imported'


class ExampleTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Example')

        box = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Example'))
        
        # We add a button to the current task
        # A button just fires an event when it is clicked, if a selected texture is specified,
        # it is used while the mouse is down on the button

        self.aButton = box.addView(gui3d.Button('Button'))
        
        self.pushed = 0
        self.aButtonLabel = box.addView(gui3d.TextView('Pushed 0 times'))

        @self.aButton.event
        def onClicked(event):
            self.pushed += 1
            self.aButtonLabel.setText('Pushed %d times' % self.pushed)

        # We add a toggle button to the current task
        # A toggle button fires an event when it is clicked but retains its selected state after the mouse is up,
        # if a selected texture is specified, it is used to show whether the button is toggled

        self.aToggleButton = box.addView(gui3d.ToggleButton(label='ToggleButton'))

        self.aToggleButtonLabel = box.addView(gui3d.TextView(label='Not selected'))

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
        self.aRadioButton1 = box.addView(gui3d.RadioButton(self.aRadioButtonGroup, selected=True, label='RadioButton1'))
        self.aRadioButton2 = box.addView(gui3d.RadioButton(self.aRadioButtonGroup, label='RadioButton2'))

        self.aRadioButtonLabel = box.addView(gui3d.TextView(label='Button 1 is selected'))

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
        self.aSlider = box.addView(gui3d.Slider(value=0.5, label='Slider %.2f'))

        self.aSliderLabel = box.addView(gui3d.TextView(label='Value is 0.5'))

        @self.aSlider.event
        def onChange(value):
            self.aSliderLabel.setText('Value is %f' % value)
            self.aProgressBar.setProgress(value, 1)

        # we also create a progressbar, which is updated as the slider moves

        self.aProgressBar = box.addView(gui3d.ProgressBar(style=gui3d.ProgressBarStyle._replace(width=112, margin=[2,2,2,2]), barStyle=gui3d.ProgressBarBarStyle._replace(width=112, margin=[2,2,2,2])))
        self.aProgressBar.setProgress(0.5, 0)
        
        # A text edit

        self.aTextEdit = box.addView(gui3d.TextEdit(text='Some text', style=gui3d.TextEditStyle._replace(width=112)))
        
        self.meshSlider = box.addView(gui3d.Slider(value=0.5, label='Mesh distort %0.2f'))
        
        self.meshStored = False
        @self.meshSlider.event
        def onChanging(value):
            human = gui3d.app.selectedHuman
            if self.meshStored:
                human.restoreMesh()
            else:
                human.storeMesh()
                self.meshStored = True
            for v in human.mesh.verts:
                v.co = [v.co[i] + v.no[i] * value for i in xrange(3)]
            human.mesh.update()
    
        @self.meshSlider.event
        def onChange(value):
            human = gui3d.app.selectedHuman
            human.applyAllTargets()
            self.meshStored = False
            for v in human.mesh.verts:
                v.co = [v.co[i] + v.no[i] * value for i in xrange(3)]
            human.mesh.update()

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Example')
    taskview = category.addView(ExampleTaskView(category))

    print 'example loaded'
    print 'Hello world'


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'example unloaded'


