#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier

print 'Expression 2 imported'

class Modifier(humanmodifier.GenericModifier):

    def __init__(self, template):
        
        humanmodifier.GenericModifier.__init__(self, template)
        
    # overrides
    def setValue(self, human, value):
    
        value = self.clampValue(value)
        
        for target in self.targets:
            human.setDetail(target[0], value)
    
    def expandTemplate(self, targets):
        
        return targets
    
    def getFactors(self, human, value):
        
        factors = {}
        
        return factors
    
    def clampValue(self, value):
        return max(0.0, min(1.0, value))

class GroupBoxRadioButton(gui3d.RadioButton):
    def __init__(self, parent, group, label, groupBox, selected=False):
        gui3d.RadioButton.__init__(self, parent, group, label, selected, style=gui3d.ButtonStyle)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        gui3d.RadioButton.onClicked(self, event)
        self.parent.parent.hideAllBoxes()
        self.groupBox.show()
        
class ExpressionSlider(humanmodifier.ModifierSlider):
    def __init__(self, parent, label, modifier):
        
        humanmodifier.ModifierSlider.__init__(self, parent, label=label, modifier=modifier)

class ExpressionTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Expression 2')
        
        expressions = [
            ('eyebrows-left', ['down', 'extern-up', 'inner-up', 'up']),
            ('eyebrows-right', ['down', 'extern-up', 'inner-up', 'up']),
            ('eye-left', ['closure', 'droop', 'opened-up', 'slit', 'slit2', 'slit3']),
            ('eye-right', ['closure', 'droop', 'opened-up', 'slit', 'slit2', 'slit3']),
            ('mouth', ['compression', 'corner-puller', 'depression', 'depression-retraction', 'elevation', 'eversion', 'parling', 'part-later', 'protusion', 'pursing', 'retraction', 'upward-retraction']),
            ('nose', ['depression', 'left-dilatation', 'left-elevation', 'right-dilatation', 'right-elevation', 'compression']),
            ]
        
        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []
        
        self.modifiers = {}
        
        self.categoryBox = gui3d.GroupBox(self, [650, 80, 9.0], 'Category')
        
        for name, subnames in expressions:
            # Create box
            box = gui3d.GroupBox(self, [10, 80, 9.0], name.capitalize())
            self.groupBoxes.append(box)
            
            # Create sliders
            for subname in subnames:
                
                #modifier = humanmodifier.GenderAgeModifier('data/targets/expression/units/${gender}_${age}/%s-%s.target' % (name, subname))
                modifier = Modifier('data/targets/expression/units/male_young/%s-%s.target' % (name, subname))
                self.modifiers[subname] = modifier
                slider = ExpressionSlider(box, subname.capitalize(), modifier)
                self.sliders.append(slider)
            
            # Create radiobutton
            radio = GroupBoxRadioButton(self.categoryBox, self.radioButtons, name.capitalize(), box, selected=len(self.radioButtons) == 0)

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
    taskview = ExpressionTaskView(category)
    
    #app.addLoadHandler('expression', taskview.loadHandler)
    #app.addSaveHandler(taskview.saveHandler)

    print 'Expression 2 loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Expression 2 unloaded'
