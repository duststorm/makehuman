#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier
from string import Template
import re
import mh
import gui

class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, task, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        self.task = task

    def onClicked(self, event):
        self.task.groupBox.showWidget(self.groupBox)

class TorsoSlider(humanmodifier.ModifierSlider):
    def __init__(self,modifier, image, view):
        super(TorsoSlider, self).__init__(min=-1.0, max=1.0, modifier=modifier, image=image)

        self.view = getattr(gui3d.app, view)

    def onFocus(self, event):
        super(TorsoSlider, self).onFocus(event)
        if gui3d.app.settings.get('cameraAutoZoom', True):
            self.view()

class TorsoTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Torso')

        features = [
            ('Torso', [('data/targets/torso/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/torso/images/', i[3]) for i in
                [
                    ('torso-scale-depth', 'decr', 'incr', 'setGlobalCamera'),
                    ('torso-scale-horiz', 'decr', 'incr', 'setGlobalCamera'),
                    ('torso-scale-vert', 'decr', 'incr', 'setGlobalCamera'),
                    ('torso-trans', 'in', 'out', 'setGlobalCamera'),
                    ('torso-trans', 'down', 'up', 'setGlobalCamera'),
                    ('torso-trans', 'forward', 'backward', 'setGlobalCamera'),

                ]]),
            ('Hip', [('data/targets/hip/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/hip/images/', i[3]) for i in
                [
                    ('hip-scale-depth', 'decr', 'incr', 'setGlobalCamera'),
                    ('hip-scale-horiz', 'decr', 'incr', 'setGlobalCamera'),
                    ('hip-scale-vert', 'decr', 'incr', 'setGlobalCamera'),
                    ('hip-trans', 'in', 'out', 'setGlobalCamera'),
                    ('hip-trans', 'down', 'up', 'setGlobalCamera'),
                    ('hip-trans', 'forward', 'backward', 'setGlobalCamera'),

                ]]),
            ('Stomach', [('data/targets/stomach/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/stomach/images/', i[3]) for i in
                [
                    ('stomach-tone', 'decr', 'incr', 'setGlobalCamera'),
                ]]),
            ('Buttocks', [('data/targets/buttocks/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/buttocks/images/', i[3]) for i in
                [
                    ('buttocks-tone', 'decr', 'incr', 'setGlobalCamera'),
                ]]),
            ('Pelvis', [('data/targets/pelvis/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/pelvis/images/', i[3]) for i in
                [
                    ('pelvis-tone', 'decr', 'incr', 'setGlobalCamera'),
                ]]),
            ]

        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []

        self.modifiers = {}

        self.categoryBox = self.addRightWidget(gui.SliderBox('Category'))
        self.groupBox = self.addLeftWidget(gui.StackedBox())

        for name, templates in features:

            for index, template in enumerate(templates):

                if index % 12 == 0:

                    if len(templates) <= 12:
                        title = name.capitalize()
                    else:
                        title = '%s %d' % (name.capitalize(), index / 12 + 1)

                    # Create box
                    box = self.groupBox.addWidget(gui.GroupBox(title))
                    self.groupBoxes.append(box)

                    # Create radiobutton
                    radio = self.categoryBox.addWidget(GroupBoxRadioButton(self, self.radioButtons, title, box, selected=len(self.radioButtons) == 0))

                # Create sliders
                modifier = humanmodifier.GenderAgeEthnicAsymmetricModifier(template[0], 'value', template[2], template[3], False)
                self.modifiers['%s%d' % (name, index + 1)] = modifier

                slider = box.addWidget(TorsoSlider(modifier, '%s%s-%s-%s.png' % (template[4], template[1], template[2], template[3]), template[5]))
                self.sliders.append(slider)

        self.groupBox.showWidget(self.groupBoxes[0])
        # self.hideAllBoxes()
        # self.groupBoxes[0].show()

    def hideAllBoxes(self):

        for box in self.groupBoxes:

            box.hide()

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)

        if gui3d.app.settings.get('cameraAutoZoom', True):
            gui3d.app.setGlobalCamera()

        for slider in self.sliders:
            slider.update()

    def onHumanChanged(self, event):

        human = event.human

        for slider in self.sliders:
            slider.update()

    def loadHandler(self, human, values):

        if values[0] == 'torso':
            modifier = self.modifiers.get(values[1].replace("-", " "), None)
            if modifier:
                modifier.setValue(human, float(values[2]))

    def saveHandler(self, human, file):

        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('torso %s %f\n' % (name.replace(" ", "-"), value))

def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addTask(TorsoTaskView(category))

    app.addLoadHandler('torso', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

def unload(app):
    pass


