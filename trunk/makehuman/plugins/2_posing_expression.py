#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier
import warpmodifier
import warp
import os
import mh
import posemode
import qtgui as gui
import filechooser as fc
import log

class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        self.parentWidget()._parent.groupBox.showWidget(self.groupBox)
        # self.parentWidget()._parent.hideAllBoxes()
        # self.groupBox.show()

class ExpressionSlider(posemode.PoseModifierSlider):
    def __init__(self, label, modifier):        
        posemode.PoseModifierSlider.__init__(self, label, modifier)        


class ExpressionTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Expression')
        
        self.expressions = [
            ('eyebrows-left', ['down', 'extern-up', 'inner-up', 'up']),
            ('eyebrows-right', ['down', 'extern-up', 'inner-up', 'up']),
            ('eye-left', ['closure', 'opened-up', 'slit']),
            ('eye-right', ['closure', 'opened-up', 'slit']),
            ('mouth', ['compression', 'corner-puller', 'depression', 'depression-retraction', 'elevation', 'eversion', 'parling', 'part-later', 'protusion', 'pursing', 'retraction', 'upward-retraction', 'open']),
            ('nose', ['depression', 'left-dilatation', 'left-elevation', 'right-dilatation', 'right-elevation', 'compression']),
            ('neck', ['platysma']),
            ]

        self.include = "All"
        
        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []
        
        self.modifiers = {}
        
        self.categoryBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Category')))
        self.groupBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.StackedBox()))
        
        for name, subnames in self.expressions:
            # Create box
            box = self.groupBox.addWidget(gui.SliderBox(name.capitalize()))
            self.groupBoxes.append(box)
            
            # Create sliders
            for subname in subnames:
                
                #modifier = humanmodifier.GenderAgeModifier('data/targets/expression/units/${gender}_${age}/%s-%s.target' % (name, subname))

                modifier = warpmodifier.WarpModifier(
                        'data/targets/expression/units/${ethnic}/${gender}_${age}/%s-%s.target' % (name, subname),
                        "face",
                        "GenderAgeEthnicModifier2")

                self.modifiers[name + '-' + subname] = modifier
                slider = box.addWidget(ExpressionSlider(subname.capitalize(), modifier))
                self.sliders.append(slider)
                modifier.slider = slider
            # Create radiobutton
            radio = self.categoryBox.addWidget(GroupBoxRadioButton(self.radioButtons, name.capitalize(), box, selected=len(self.radioButtons) == 0))

        self.groupBox.showWidget(self.groupBoxes[0])
        # self.hideAllBoxes()
        # self.groupBoxes[0].show()
  
    def hideAllBoxes(self):
        
        for box in self.groupBoxes:
            
            box.hide()

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        for slider in self.sliders:
            slider.update()
        
    def onHumanChanged(self, event):
        
        posemode.changePoseMode(event)        
        for slider in self.sliders:
            slider.update()
                
    def loadHandler(self, human, values):
        
        modifier = self.modifiers.get(values[1], None)
        if modifier:
            value = float(values[2])
            modifier.setValue(human, value)
            modifier.updateValue(human, value)  # Force recompilation
       
    def saveHandler(self, human, file):
        
        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('expression %s %f\n' % (name, value))


    def resetExpressions(self, include):

        human = gui3d.app.selectedHuman

        log.message("resetExpressions %s", include)

        if include == "All":
            for name, modifier in self.modifiers.iteritems():
                #print "  R", name
                modifier.setValue(human, 0.0)
                #modifier.updateValue(human, 0.0)  # Force recompilation
        else:
            for name, modifier in self.modifiers.iteritems():
                #print "  R", name
                if name in include:
                    modifier.setValue(human, 0.0)
                    

    def loadExpression(self, filename, include):

        human = gui3d.app.selectedHuman
        posemode.enterPoseMode()
        self.resetExpressions(include)

        f = open(filename, 'r')

        for data in f.readlines():

            lineData = data.split()

            if len(lineData) > 0 and not lineData[0] == '#':

                if lineData[0] == 'expression':
                    
                    modifier = self.modifiers.get(lineData[1], None)
                    
                    if modifier:

                        value = float(lineData[2])
                        modifier.setValue(human, value)
                        modifier.updateValue(human, value)  # Force recompilation

class Action:

    def __init__(self, human, filename, taskView, include, postAction=None):
        self.name = 'Load expression'
        self.human = human
        self.filename = filename
        self.taskView = taskView
        self.include = include
        self.postAction = postAction
        self.before = {}

        for name, modifier in self.taskView.modifiers.iteritems():
            self.before[name] = modifier.getValue(self.human)

    def do(self):
        self.taskView.loadExpression(self.filename, self.include)
        self.human.applyAllTargets(gui3d.app.progress, True)
        if self.human.armature:
            self.human.armature.adapt()
        for slider in self.taskView.sliders:
            slider.update()
        if self.postAction:
            self.postAction()
        return True

    def undo(self):
        for name, value in self.before.iteritems():
            self.taskView.modifiers[name].setValue(self.human, value)
        self.human.applyAllTargets(gui3d.app.progress, True)
        if self.human.armature:
            self.human.armature.update()
        for slider in self.taskView.sliders:
            slider.update()
        if self.postAction:
            self.postAction()
        return True

class MhmLoadTaskView(gui3d.TaskView):

    def __init__(self, category, mhmTaskView, mhmLabel, folder):

        gui3d.TaskView.__init__(self, category, mhmLabel, label=mhmLabel)

        self.mhmTaskView = mhmTaskView
        self.include = "All"

        self.globalMhmPath = os.path.join('data', folder)
        self.mhmPath = os.path.join(mh.getPath(''), 'data', folder)

        if not os.path.exists(self.mhmPath):
            os.makedirs(self.mhmPath)

        self.filechooser = self.addWidget(mh.addWidget(mh.Frame.Top, fc.FileChooser([self.globalMhmPath, self.mhmPath], 'mhm', 'png')))

        @self.filechooser.mhEvent
        def onFileSelected(filename):

            gui3d.app.do(Action(gui3d.app.selectedHuman, filename, self.mhmTaskView, self.include))
            
            mh.changeCategory('Modelling')

    def onShow(self, event):

        # When the task gets shown, set the focus to the file chooser
        gui3d.TaskView.onShow(self, event)
        gui3d.app.selectedHuman.hide()
        self.filechooser.setFocus()

    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)

class ExpressionLoadTaskView(MhmLoadTaskView):

    def __init__(self, category, expressionTaskView):
    
        MhmLoadTaskView.__init__(self, category, expressionTaskView, 'Expression', 'expressions')


class VisemeLoadTaskView(MhmLoadTaskView):

    def __init__(self, category, visemeTaskView):
    
        MhmLoadTaskView.__init__(self, category, visemeTaskView, 'Visemes', 'visemes')
        
        self.include = []
        for (cat, names) in visemeTaskView.expressions:
            if cat == "mouth":
                for name in names:
                    self.include.append("mouth-" + name)
                break
                        
        

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Posing')
    taskview = category.addTask(ExpressionTaskView(category))
    
    app.addLoadHandler('expression', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    category = app.getCategory('Library')
    category.addTask(ExpressionLoadTaskView(category, taskview))
    category.addTask(VisemeLoadTaskView(category, taskview))

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass
