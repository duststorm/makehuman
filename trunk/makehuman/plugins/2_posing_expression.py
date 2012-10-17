#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier
import warpmodifier
import warp
import os
import mh

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
                self.modifiers[name + '-' + subname] = modifier
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
            print name, value
            if value:
                print name, value
                file.write('expression %s %f\n' % (name, value))

    def resetExpressions(self):

        human = gui3d.app.selectedHuman

        for name, modifier in self.modifiers.iteritems():
            modifier.setValue(human, 0.0)

    def loadExpression(self, filename):

        human = gui3d.app.selectedHuman

        self.resetExpressions()

        f = open(filename, 'r')

        for data in f.readlines():

            lineData = data.split()

            if len(lineData) > 0 and not lineData[0] == '#':

                if lineData[0] == 'expression':

                    modifier = self.modifiers.get(lineData[1], None)
                    
                    if modifier:

                        modifier.setValue(human, float(lineData[2]))

class Action:

    def __init__(self, human, filename, expressionTaskView, postAction=None):
        self.name = 'Load expression'
        self.human = human
        self.filename = filename
        self.expressionTaskView = expressionTaskView
        self.postAction = postAction
        self.before = {}

        for name, modifier in self.expressionTaskView.modifiers.iteritems():
            self.before[name] = modifier.getValue(self.human)

    def do(self):
        self.expressionTaskView.loadExpression(self.filename)
        self.human.applyAllTargets(gui3d.app.progress, True)
        if self.postAction:
            self.postAction()
        return True

    def undo(self):
        for name, value in self.before.iteritems():
            self.expressionTaskView.modifiers[name].setValue(self.human, value)
        self.human.applyAllTargets(gui3d.app.progress, True)
        if self.postAction:
            self.postAction()
        return True

class ExpressionLoadTaskView(gui3d.TaskView):

    def __init__(self, category, expressionTaskView):

        gui3d.TaskView.__init__(self, category, 'Expression', label='Expression')

        self.expressionTaskView = expressionTaskView

        self.globalExpressionPath = os.path.join('data', 'expressions')
        self.expressionPath = os.path.join(mh.getPath(''), 'data', 'expressions')

        if not os.path.exists(self.expressionPath):
            os.makedirs(self.expressionPath)

        self.filechooser = self.addView(gui3d.FileChooser([self.globalExpressionPath, self.expressionPath], 'mhm', 'png'))

        @self.filechooser.event
        def onFileSelected(filename):

            gui3d.app.do(Action(gui3d.app.selectedHuman, filename, self.expressionTaskView))
            
            gui3d.app.switchCategory('Modelling')

    def onShow(self, event):

        # When the task gets shown, set the focus to the file chooser
        gui3d.TaskView.onShow(self, event)
        gui3d.app.selectedHuman.hide()
        self.filechooser.setFocus()

    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onResized(self, event):
        self.filechooser.onResized(event)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Posing')
    taskview = category.addView(ExpressionTaskView(category))
    
    app.addLoadHandler('expression', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    category = app.getCategory('Library')
    category.addView(ExpressionLoadTaskView(category, taskview))
    
    print 'Expression loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Expression unloaded'
