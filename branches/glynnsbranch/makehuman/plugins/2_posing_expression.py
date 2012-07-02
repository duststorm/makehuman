#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier

print 'Expression imported'

class GroupBoxRadioButton(gui3d.RadioButton):
    def __init__(self, group, label, groupBox, selected=False):
        gui3d.RadioButton.__init__(self, group, label, selected, style=gui3d.ButtonStyle)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        gui3d.RadioButton.onClicked(self, event)
        self.parent.parent.hideAllBoxes()
        self.groupBox.show()
        
class ExpressionSlider(humanmodifier.ModifierSlider):
    def __init__(self, label, modifier):
        
        humanmodifier.ModifierSlider.__init__(self, label=label, modifier=modifier)

class ExpressionTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Expression')
        
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
        
        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []
        
        self.modifiers = {}
        
        self.categoryBox = self.addView(gui3d.GroupBox([650, 80, 9.0], 'Category'))
        
        for name, subnames in expressions:
            # Create box
            box = self.addView(gui3d.GroupBox([10, 80, 9.0], name.capitalize()))
            self.groupBoxes.append(box)
            
            # Create sliders
            for subname in subnames:
                
                modifier = humanmodifier.GenderAgeModifier('data/targets/expression/${gender}_${age}/neutral_${gender}_${age}_%s.target' % subname)
                self.modifiers[subname] = modifier
                slider = box.addView(ExpressionSlider(subname.capitalize(), modifier))
                self.sliders.append(slider)
            
            # Create radiobutton
            radio = self.categoryBox.addView(GroupBoxRadioButton(self.radioButtons, name.capitalize(), box, selected=len(self.radioButtons) == 0))

        self.hideAllBoxes()
        self.groupBoxes[0].show()
        
    def hideAllBoxes(self):
        
        for box in self.groupBoxes:
            
            box.hide()
    
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        for slider in self.sliders:
            slider.update()
            
    def onResized(self, event):
        
        self.categoryBox.setPosition([event.width - 150, self.categoryBox.getPosition()[1], 9.0])
        
    def onHumanChanged(self, event):
        
        human = event.human
        
        for slider in self.sliders:
            value = slider.modifier.getValue(human)
            if value:
                slider.modifier.setValue(human, value)
                
    def loadHandler(self, human, values):
        
        modifier = self.modifiers.get(values[1], None)
        if modifier:
            modifier.setValue(human, float(values[2]))
       
    def saveHandler(self, human, file):
        
        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('expression %s %f\n' % (name, value))

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Posing')
    taskview = category.addView(ExpressionTaskView(category))
    
    app.addLoadHandler('expression', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    print 'Expression loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Expression unloaded'
