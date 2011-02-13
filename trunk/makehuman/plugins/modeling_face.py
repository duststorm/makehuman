#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier

print 'Face imported'

class GroupBoxRadioButton(gui3d.RadioButton):
    def __init__(self, parent, group, y, label, groupBox, selected=False):
        gui3d.RadioButton.__init__(self, parent, group, [658, y, 9.1], label, selected, style=gui3d.ButtonStyle)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        gui3d.RadioButton.onClicked(self, event)
        self.parent.parent.hideAllBoxes()
        self.groupBox.show()
        
class FaceSlider(humanmodifier.ModifierSlider):
    def __init__(self, parent, y, label, modifier):
        
        humanmodifier.ModifierSlider.__init__(self, parent, [10, y, 9.1], label=label, modifier=modifier)

class FaceTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Face')

        human = self.app.selectedHuman
        
        features = [
            ('eyes', ['data/targets/details/neutral_${gender}-${age}-eye%d.target' % i for i in xrange(1, 31)]),
            ('nose', ['data/targets/details/neutral_${gender}-${age}-nose%d.target' % i for i in xrange(1, 13)]),
            ('ears', ['data/targets/details/${gender}-${age}-ears%d.target' % i for i in xrange(1, 9)]),
            ('mouth', ['data/targets/details/neutral_${gender}-${age}-mouth%d.target' % i for i in xrange(1, 14)]),
            ('jaw', ['data/targets/details/${gender}-${age}-jaw%d.target' % i for i in xrange(1, 8)]),
            ('head', ['data/targets/details/neutral_${gender}-${age}-head%d.target' % i for i in xrange(1, 9)]),
            ]

        y = 80
        
        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []
        
        self.modifiers = {}
        
        self.categoryBox = gui3d.GroupBox(self, [650, y, 9.0], 'Category', gui3d.GroupBoxStyle._replace(height=25+24*sum([(len(templates[1])/12 + (len(templates[1])%12>0)) for templates in features])+6))
        y += 25
        
        for name, templates in features:
            
            for index, template in enumerate(templates):
                
                if index % 12 == 0:
                    
                    if len(templates) <= 12:
                        title = name.capitalize()
                    else:
                        title = '%s %d' % (name.capitalize(), index / 12 + 1)
                        
                    # Create box
                    box = gui3d.GroupBox(self, [10, 80, 9.0], title, gui3d.GroupBoxStyle._replace(height=25+36*min(len(templates)-index, 12)+6))
                    self.groupBoxes.append(box)
                    
                    # Create radiobutton
                    radio = GroupBoxRadioButton(self.categoryBox, self.radioButtons, y, title, box, selected=len(self.radioButtons) == 0)
                    y += 24
                    
                    yy = 80 + 25
            
                # Create sliders
                modifier = humanmodifier.GenderAgeModifier(template)
                self.modifiers['%s%d' % (name, index + 1)] = modifier
                slider = FaceSlider(box, yy, '%s %d' % (name.capitalize(), index + 1), modifier)
                self.sliders.append(slider)
                yy += 36

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
        
        self.categoryBox.setPosition([event[0] - 150, self.categoryBox.getPosition()[1], 9.0])
        
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
                file.write('face %s %f\n' % (name, value))

def load(app):
    category = app.getCategory('Experiments')
    taskview = FaceTaskView(category)
    
    app.addLoadHandler('face', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    print 'Face loaded'

def unload(app):
    pass


