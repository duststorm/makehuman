#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier
from string import Template
import re

print 'Arms and leg imported'

class AsymmetricDetailModifier(humanmodifier.GenderAgeAsymmetricModifier):
    
    def __init__(self, template, parameterName, left, right, always=True):
    
        humanmodifier.GenderAgeAsymmetricModifier.__init__(self, template, parameterName, left, right, always)
        
    def getValue(self, human):
        
        return getattr(human, self.parameterName)
        
    def setValue(self, human, value):
        
        setattr(human, self.parameterName, value)
        humanmodifier.GenderAgeAsymmetricModifier.setValue(self, human, value)

class StomachModifier(AsymmetricDetailModifier):
    # This needs a custom modifier because tone and weight also need to be included
    
    def __init__(self):
    
        AsymmetricDetailModifier.__init__(self, 'data/targets/details/${gender}-${age}-${tone}-${weight}-stomach${stomach}.target', 'stomach', '1', '2', False)
        
    def expandTemplate(self, targets):
        
        # Build target list of (targetname, [factors])
        targets = [(Template(target[0]).safe_substitute(gender=value), target[1] + [value]) for target in targets for value in ['female', 'male']]
        targets = [(Template(target[0]).safe_substitute(age=value), target[1] + [value]) for target in targets for value in ['child', 'young', 'old']]
        targets = [(Template(target[0]).safe_substitute(tone=value), target[1] + [value or 'averageTone']) for target in targets for value in ['flaccid', '', 'muscle']]
        targets = [(Template(target[0]).safe_substitute(weight=value), target[1] + [value or 'averageWeight']) for target in targets for value in ['light', '', 'heavy']]
        targets = [(Template(target[0]).safe_substitute({self.parameterName:value}), target[1] + [value]) for target in targets for value in [self.left, self.right]]

        # Cleanup multiple hyphens and remove a possible hyphen before a dot.
        doubleHyphen = re.compile(r'-+')
        hyphenDot = re.compile(r'-\.')
        
        targets = [(re.sub(hyphenDot, '.', re.sub(doubleHyphen, '-', target[0])), target[1]) for target in targets]
        
        return targets
        
    def getFactors(self, human, value):
        
        factors = {
            'female': human.femaleVal,
            'male': human.maleVal,
            'child': human.childVal,
            'young': human.youngVal,
            'old': human.oldVal,
            'flaccid':human.flaccidVal,
            'muscle':human.muscleVal,
            'averageTone':1.0 - (human.flaccidVal + human.muscleVal),
            'light':human.underweightVal,
            'heavy':human.overweightVal,
            'averageWeight':1.0 - (human.underweightVal + human.overweightVal),
            self.left: -min(value, 0.0),
            self.right: max(0.0, value)
        }
        
        return factors

class DetailSlider(humanmodifier.ModifierSlider):
    
    def __init__(self, value, min, max, label, modifier):
        
        humanmodifier.ModifierSlider.__init__(self, value, min, max, label, modifier=modifier)

class GroupBoxRadioButton(gui3d.RadioButton):
    def __init__(self, group, label, groupBox, selected=False):
        gui3d.RadioButton.__init__(self, group, label, selected, style=gui3d.ButtonStyle)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        gui3d.RadioButton.onClicked(self, event)
        self.parent.parent.hideAllBoxes()
        self.groupBox.show()
        
class TorsoSlider(humanmodifier.ModifierSlider):
    def __init__(self,modifier, image, view):
        
        humanmodifier.ModifierSlider.__init__(self, min=-1.0, max=1.0, modifier=modifier, style=gui3d.SliderStyle._replace(height=56, normal=image), thumbStyle=gui3d.SliderThumbStyle._replace(height = 32, width = 32, normal="slider2.png", focused="slider2_focused.png"))
        
        self.view = getattr(gui3d.app, view)
        
    def onFocus(self, event):
        
        humanmodifier.ModifierSlider.onFocus(self, event)
        self.view()
        
    def setPosition(self, position):
        
        humanmodifier.ModifierSlider.setPosition(self, position)
        self.thumb.setPosition([position[0], position[1] + self.style.height / 2 - self.thumbStyle.height / 2, position[2] + 0.01])
        self.setValue(self.getValue())

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
            ]

        y = 80
        
        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []
        
        self.modifiers = {}
        
        self.categoryBox = self.addView(gui3d.GroupBox([650, y, 9.0], 'Category'))
        y += 25
        
        for name, templates in features:
            
            for index, template in enumerate(templates):
                
                if index % 12 == 0:
                    
                    if len(templates) <= 12:
                        title = name.capitalize()
                    else:
                        title = '%s %d' % (name.capitalize(), index / 12 + 1)
                        
                    # Create box
                    box = self.addView(gui3d.GroupBox([10, 80, 9.0], title, gui3d.GroupBoxStyle._replace(width=128+112+4)))
                    self.groupBoxes.append(box)
                    
                    # Create radiobutton
                    radio = self.categoryBox.addView(GroupBoxRadioButton(self.radioButtons, title, box, selected=len(self.radioButtons) == 0))
                    y += 24
            
                # Create sliders
                modifier = humanmodifier.GenderAgeEthnicAsymmetricModifier(template[0], 'value', template[2], template[3], False)
                self.modifiers['%s%d' % (name, index + 1)] = modifier

                slider = box.addView(TorsoSlider(modifier, '%s%s-%s-%s.png' % (template[4], template[1], template[2], template[3]), template[5]))
                self.sliders.append(slider)
                
        y += 16

        self.specialModifiers = {}

        self.specialModifiers['pelvisTone'] = AsymmetricDetailModifier('data/targets/details/${gender}-${age}-pelvis-tone${pelvisTone}.target', 'pelvisTone', '1', '2', False)
        self.specialModifiers['buttocks'] = AsymmetricDetailModifier('data/targets/details/${gender}-${age}-nates${buttocks}.target', 'buttocks', '1', '2', False)
        self.specialModifiers['stomach'] = StomachModifier()
        
        slider = DetailSlider(0.0, -1.0, 1.0, "Pelvis tone", self.specialModifiers['pelvisTone']);
        self.sliders.append(slider)
        self.categoryBox.addView(slider);
        slider = DetailSlider(0.0, -1.0, 1.0, "Stomach", self.specialModifiers['stomach']);
        self.sliders.append(slider)
        self.categoryBox.addView(slider);
        slider = DetailSlider(0.0, -1.0, 1.0, "Buttocks", self.specialModifiers['buttocks']);
        self.sliders.append(slider)
        self.categoryBox.addView(slider);

        self.hideAllBoxes()
        self.groupBoxes[0].show()
        
    def hideAllBoxes(self):
        
        for box in self.groupBoxes:
            
            box.hide()
    
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        
        gui3d.app.setGlobalCamera()
        
        for slider in self.sliders:
            slider.update()
            
    def onResized(self, event):
        
        self.categoryBox.setPosition([event.width - 150, self.categoryBox.getPosition()[1], 9.0])
        
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
    taskview = category.addView(TorsoTaskView(category))
    
    app.addLoadHandler('torso', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    print 'Torso loaded'

def unload(app):
    pass


