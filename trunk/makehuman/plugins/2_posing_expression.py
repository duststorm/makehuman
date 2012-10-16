#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier
import warpmodifier
import warp

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
            ('eyebrows-left', ['down', 'extern-up', 'inner-up', 'up']),
            ('eyebrows-right', ['down', 'extern-up', 'inner-up', 'up']),
            ('eye-left', ['closure', 'opened-up', 'slit']),
            ('eye-right', ['closure', 'opened-up', 'slit']),
            ('mouth', ['compression', 'corner-puller', 'depression', 'depression-retraction', 'elevation', 'eversion', 'parling', 'part-later', 'protusion', 'pursing', 'retraction', 'upward-retraction', 'open']),
            ('nose', ['depression', 'left-dilatation', 'left-elevation', 'right-dilatation', 'right-elevation', 'compression']),
            ('neck', ['platysma']),
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
                
                #modifier = humanmodifier.GenderAgeModifier('data/targets/expression/units/${gender}_${age}/%s-%s.target' % (name, subname))
                if warp.numpy:
                    modifier = warpmodifier.WarpModifier(
                        'data/targets/expression/units/${ethnic}/${gender}_${age}/%s-%s.target' % (name, subname),
                        "face",
                        "GenderAgeEthnicModifier2")
                else:
                    modifier = humanmodifier.GenderAgeEthnicModifier2('data/targets/expression/units/${ethnic}/${gender}_${age}/%s-%s.target' % (name, subname))
                self.modifiers[subname] = modifier
                slider = box.addView(ExpressionSlider(subname.capitalize(), modifier))
                self.sliders.append(slider)
                modifier.slider = slider
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
    
    #app.addLoadHandler('expression', taskview.loadHandler)
    #app.addSaveHandler(taskview.saveHandler)
    
    print 'Expression loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Expression unloaded'
