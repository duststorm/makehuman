#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
from algos3d import getTarget

print 'Expression imported'

class Action:

    def __init__(self, human, detail, before, after, postAction=None):
        self.name = 'Change expression'
        self.human = human
        self.detail = detail
        self.before = before
        self.after = after
        self.postAction = postAction

    def do(self):
        self.human.setDetail(self.detail, self.after)
        self.human.applyAllTargets()
        if self.postAction:
            self.postAction()
        return True

    def undo(self):
        self.human.setDetail(self.detail, self.before)
        self.human.applyAllTargets()
        if self.postAction:
            self.postAction()
        return True

class GroupBoxRadioButton(gui3d.RadioButton):
    def __init__(self, parent, group, y, label, groupBox, selected=False):
        gui3d.RadioButton.__init__(self, parent, group, [658, y, 9.1], label, selected, style=gui3d.ButtonStyle)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        gui3d.RadioButton.onClicked(self, event)
        self.parent.parent.hideAllBoxes()
        self.groupBox.show()
        
class ExpressionSlider(gui3d.Slider):
    def __init__(self, parent, y, label, detail):
        human = parent.app.selectedHuman
        gui3d.Slider.__init__(self, parent, position=[10, y, 9.1], value = human.getDetail(detail), label=label)
        self.target = getTarget(human.meshData, detail)
        self.before = None
    
    def onChange(self, value):
        human = self.app.selectedHuman
        self.app.do(Action(human, self.target.name, self.before, value, self.update))
        self.before = None
        
    def onChanging(self, value):
        if self.app.settings.get('realtimeUpdates', True):
            human = self.app.selectedHuman
            if self.before is None:
                self.before = human.getDetail(self.target.name)
            self.target.apply(human.meshData, -human.getDetail(self.target.name), False, False)
            human.setDetail(self.target.name, value)
            self.target.apply(human.meshData, value, True,
                self.app.settings.get('realtimeNormalUpdates', True))
        
    def update(self):
        human = self.app.selectedHuman
        self.setValue(human.getDetail(self.target.name))

class ExpressionTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Expression')

        human = self.app.selectedHuman
        
        expressions = [
            ('smile1', ['smile', 'hopeful', 'innocent']),
            ('smile2', ['realsmile', 'tender', 'seductive']),
            ('smile3', ['grin', 'excited', 'ecstatic']),
            ('smile4', ['proud', 'pleased', 'amused', 'laughing1', 'laughing2']),
            ('sadness1', ['so-so', 'blue', 'depressed']),
            ('sadness2', ['sad', 'distressed', 'crying', 'pain']),
            ('sadness3', ['disappointed', 'frustrated', 'stressed']),
            ('sadness4', ['worried', 'scared', 'terrified']),
            ('sadness5', ['shy', 'guilty', 'embarassed']),
            ('relaxation1', ['relaxed', 'peaceful', 'refreshed', 'pleasured']),
            ('relaxation2', ['lazy','tired', 'drained', 'sleepy', 'groggy']),
            ('surprise', ['curious', 'surprised', 'impressed', 'puzzled', 'shocked']),
            ('anger1', ['frown', 'upset', 'angry', 'furious', 'enraged']),
            ('anger2', ['skeptical', 'vindictive', 'pout', 'furious', 'grumpy']),
            ('anger3', ['arrogant', 'sneering', 'haughty', 'disgusted'])
            ]

        y = 80
        
        self.groupBoxes = []
        self.radioButtons = []
        
        self.categoryBox = gui3d.GroupBox(self, [650, y, 9.0], 'Category', gui3d.GroupBoxStyle._replace(height=360))
        y += 25
        
        for name, subnames in expressions:
            # Create box
            box = gui3d.GroupBox(self, [10, 80, 9.0], name.capitalize(), gui3d.GroupBoxStyle._replace(height=320))
            self.groupBoxes.append(box)
            
            # Create sliders
            yy = 80 + 35
            
            for subname in subnames:
                slider = ExpressionSlider(box, yy, subname.capitalize(), 'data/targets/expression/female_young/neutral_female_young_%s.target' % subname)
                yy += 35
            
            # Create radiobutton
            radio = GroupBoxRadioButton(self.categoryBox, self.radioButtons, y, name.capitalize(), box, selected=len(self.radioButtons) == 0)
            y += 22

        self.hideAllBoxes()
        self.groupBoxes[0].show()
        
    def hideAllBoxes(self):
        for box in self.groupBoxes:
            box.hide()
            
    def onResized(self, event):
        
        self.categoryBox.setPosition([event[0] - 150, self.categoryBox.getPosition()[1], 9.0])

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Advanced')
    taskview = ExpressionTaskView(category)

    print 'Expression loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Expression unloaded'


