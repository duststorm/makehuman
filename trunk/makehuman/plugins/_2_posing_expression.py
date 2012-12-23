#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier
import warpmodifier
import mh
import qtgui as gui

print 'Expression imported'

class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox

    def onClicked(self, event):
        self.parentWidget()._parent.groupBox.showWidget(self.groupBox)
        
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
        
        self.categoryBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Category')))
        self.groupBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.StackedBox()))
        
        for name, subnames in expressions:
            # Create box
            box = self.groupBox.addWidget(gui.GroupBox(name.capitalize()))
            self.groupBoxes.append(box)
            
            # Create sliders
            for subname in subnames:
                
                #modifier = humanmodifier.GenderAgeModifier('data/targets/expression/${gender}_${age}/neutral_${gender}_${age}_%s.target' % subname)
                modifier = warpmodifier.WarpModifier(
                    'data/targets/expression/${gender}_${age}/neutral_${gender}_${age}_%s.target' % subname,
                    "face",
                    "GenderAgeModifier")
                self.modifiers[subname] = modifier
                slider = box.addWidget(ExpressionSlider(subname.capitalize(), modifier))
                modifier.slider = slider
                self.sliders.append(slider)
            
            # Create radiobutton
            radio = self.categoryBox.addWidget(GroupBoxRadioButton(self.radioButtons, name.capitalize(), box, selected=len(self.radioButtons) == 0))

        self.groupBox.showWidget(self.groupBoxes[0])
    
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        for slider in self.sliders:
            slider.update()
        
    def onHumanChanged(self, event):
        
        human = event.human
        
        #print "HC", event

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
    taskview = category.addTask(ExpressionTaskView(category))
    
    app.addLoadHandler('expression', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    print 'Expression loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Expression unloaded'
