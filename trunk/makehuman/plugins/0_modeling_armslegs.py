#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier

print 'Arms and leg imported'

class GroupBoxRadioButton(gui3d.RadioButton):
    def __init__(self, parent, group, label, groupBox, selected=False):
        gui3d.RadioButton.__init__(self, parent, group, label, selected, style=gui3d.ButtonStyle)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        gui3d.RadioButton.onClicked(self, event)
        self.parent.parent.hideAllBoxes()
        self.groupBox.show()
        
class HeadSlider(humanmodifier.ModifierSlider):
    def __init__(self, parent, modifier, image, view):
        
        humanmodifier.ModifierSlider.__init__(self, parent, min=-1.0, max=1.0, modifier=modifier, style=gui3d.SliderStyle._replace(height=56, normal=image), thumbStyle=gui3d.SliderThumbStyle._replace(height = 32, width = 32, normal="slider2.png", focused="slider2_focused.png"))
        
        self.view = getattr(self.app, view)
        
    def onFocus(self, event):
        
        humanmodifier.ModifierSlider.onFocus(self, event)
        self.view()
        
    def setPosition(self, position):
        
        humanmodifier.ModifierSlider.setPosition(self, position)
        self.thumb.setPosition([position[0], position[1] + self.style.height / 2 - self.thumbStyle.height / 2, position[2] + 0.01])
        self.setValue(self.getValue())

class HeadTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Arms and Legs')
        
        features = [
            ('right hand', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/head/images/', i[3]) for i in
                [                     
                    ('r-hand-scale-depth', 'decr', 'incr', 'rightView'),
                    ('r-hand-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('r-hand-scale-vert', 'decr', 'incr', 'frontView'),
                    ('r-hand-trans', 'in', 'out', 'frontView'),
                    ('r-hand-trans', 'down', 'up', 'frontView'),
                    ('r-hand-trans', 'forward', 'backward', 'rightView'),                          
                                                      
                ]]),
            ('left hand', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/head/images/', i[3]) for i in
                [                     
                    ('l-hand-scale-depth', 'decr', 'incr', 'rightView'),
                    ('l-hand-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('l-hand-scale-vert', 'decr', 'incr', 'frontView'),
                    ('l-hand-trans', 'in', 'out', 'frontView'),
                    ('l-hand-trans', 'down', 'up', 'frontView'),
                    ('l-hand-trans', 'forward', 'backward', 'rightView'),                          
                                                      
                ]]),
            ('right foot', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/head/images/', i[3]) for i in
                [                     
                    ('r-foot-scale-depth', 'decr', 'incr', 'rightView'),
                    ('r-foot-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('r-foot-scale-vert', 'decr', 'incr', 'frontView'),
                    ('r-foot-trans', 'in', 'out', 'frontView'),
                    ('r-foot-trans', 'down', 'up', 'frontView'),
                    ('r-foot-trans', 'forward', 'backward', 'rightView'),                          
                                                      
                ]]),
            ('left foot', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/head/images/', i[3]) for i in
                [                     
                    ('l-foot-scale-depth', 'decr', 'incr', 'rightView'),
                    ('l-foot-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('l-foot-scale-vert', 'decr', 'incr', 'frontView'),
                    ('l-foot-trans', 'in', 'out', 'frontView'),
                    ('l-foot-trans', 'down', 'up', 'frontView'),
                    ('l-foot-trans', 'forward', 'backward', 'rightView'),                          
                                                      
                ]]), 
            ('left arm', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/head/images/', i[3]) for i in
                [                     
                    ('l-lowerarm-scale-depth', 'decr', 'incr', 'rightView'),
                    ('l-lowerarm-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('l-lowerarm-scale-vert', 'decr', 'incr', 'frontView'),
                    ('l-lowerarm-trans', 'in', 'out', 'frontView'),
                    ('l-lowerarm-trans', 'down', 'up', 'frontView'),
                    ('l-lowerarm-trans', 'forward', 'backward', 'rightView'), 
                    ('l-upperarm-scale-depth', 'decr', 'incr', 'rightView'),
                    ('l-upperarm-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('l-upperarm-scale-vert', 'decr', 'incr', 'frontView'),
                    ('l-upperarm-trans', 'in', 'out', 'frontView'),
                    ('l-upperarm-trans', 'down', 'up', 'frontView'),
                    ('l-upperarm-trans', 'forward', 'backward', 'rightView'),                          
                                                      
                ]]), 
            ('right arm', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/head/images/', i[3]) for i in
                [                     
                    ('r-lowerarm-scale-depth', 'decr', 'incr', 'rightView'),
                    ('r-lowerarm-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('r-lowerarm-scale-vert', 'decr', 'incr', 'frontView'),
                    ('r-lowerarm-trans', 'in', 'out', 'frontView'),
                    ('r-lowerarm-trans', 'down', 'up', 'frontView'),
                    ('r-lowerarm-trans', 'forward', 'backward', 'rightView'), 
                    ('r-upperarm-scale-depth', 'decr', 'incr', 'rightView'),
                    ('r-upperarm-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('r-upperarm-scale-vert', 'decr', 'incr', 'frontView'),
                    ('r-upperarm-trans', 'in', 'out', 'frontView'),
                    ('r-upperarm-trans', 'down', 'up', 'frontView'),
                    ('r-upperarm-trans', 'forward', 'backward', 'rightView'),                          
                                                      
                ]]), 
            ('left leg', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/head/images/', i[3]) for i in
                [                     
                    ('l-lowerleg-scale-depth', 'decr', 'incr', 'rightView'),
                    ('l-lowerleg-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('l-lowerleg-scale-vert', 'decr', 'incr', 'frontView'),
                    ('l-lowerleg-trans', 'in', 'out', 'frontView'),
                    ('l-lowerleg-trans', 'down', 'up', 'frontView'),
                    ('l-lowerleg-trans', 'forward', 'backward', 'rightView'), 
                    ('l-upperleg-scale-depth', 'decr', 'incr', 'rightView'),
                    ('l-upperleg-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('l-upperleg-scale-vert', 'decr', 'incr', 'frontView'),
                    ('l-upperleg-trans', 'in', 'out', 'frontView'),
                    ('l-upperleg-trans', 'down', 'up', 'frontView'),
                    ('l-upperleg-trans', 'forward', 'backward', 'rightView'),                          
                                                      
                ]]), 
            ('right leg', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/head/images/', i[3]) for i in
                [                     
                    ('r-lowerleg-scale-depth', 'decr', 'incr', 'rightView'),
                    ('r-lowerleg-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('r-lowerleg-scale-vert', 'decr', 'incr', 'frontView'),
                    ('r-lowerleg-trans', 'in', 'out', 'frontView'),
                    ('r-lowerleg-trans', 'down', 'up', 'frontView'),
                    ('r-lowerleg-trans', 'forward', 'backward', 'rightView'), 
                    ('r-upperleg-scale-depth', 'decr', 'incr', 'rightView'),
                    ('r-upperleg-scale-horiz', 'decr', 'incr', 'frontView'),
                    ('r-upperleg-scale-vert', 'decr', 'incr', 'frontView'),
                    ('r-upperleg-trans', 'in', 'out', 'frontView'),
                    ('r-upperleg-trans', 'down', 'up', 'frontView'),
                    ('r-upperleg-trans', 'forward', 'backward', 'rightView'),                          
                                                      
                ]]), 
            ]

        y = 80
        
        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []
        
        self.modifiers = {}
        
        self.categoryBox = gui3d.GroupBox(self, [650, y, 9.0], 'Category')
        y += 25
        
        for name, templates in features:
            
            for index, template in enumerate(templates):
                
                if index % 12 == 0:
                    
                    if len(templates) <= 12:
                        title = name.capitalize()
                    else:
                        title = '%s %d' % (name.capitalize(), index / 12 + 1)
                        
                    # Create box
                    box = gui3d.GroupBox(self, [10, 80, 9.0], title, gui3d.GroupBoxStyle._replace(width=128+112+4))
                    self.groupBoxes.append(box)
                    
                    # Create radiobutton
                    radio = GroupBoxRadioButton(self.categoryBox, self.radioButtons, title, box, selected=len(self.radioButtons) == 0)
                    y += 24
            
                # Create sliders
                modifier = humanmodifier.GenderAgeEthnicAsymmetricModifier(template[0], 'value', template[2], template[3], False)
                self.modifiers['%s%d' % (name, index + 1)] = modifier

                slider = HeadSlider(box, modifier, '%s%s-%s-%s.png' % (template[4], template[1], template[2], template[3]), template[5])
                self.sliders.append(slider)
                
        y += 16

        self.hideAllBoxes()
        self.groupBoxes[0].show()
        
    def hideAllBoxes(self):
        
        for box in self.groupBoxes:
            
            box.hide()
    
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        
        self.app.setFaceCamera()
        
        for slider in self.sliders:
            slider.update()
            
    def onResized(self, event):
        
        self.categoryBox.setPosition([event.width - 150, self.categoryBox.getPosition()[1], 9.0])
        
    '''
    def onHumanChanged(self, event):
        
        human = event.human
        
        for slider in self.sliders:
            value = slider.modifier.getValue(human)
            if value:
                slider.modifier.setValue(human, value)
                
    def loadHandler(self, human, values):
        
        if values[0] == 'face':
            modifier = self.modifiers.get(values[1], None)
            if modifier:
                modifier.setValue(human, float(values[2]))
        elif values[0] == 'headAge':
            self.headAgeModifier.setValue(human, float(values[1]))
        elif values[0] == 'faceAngle':
            self.faceAngleModifier.setValue(human, float(values[1]))
       
    def saveHandler(self, human, file):
        
        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('face %s %f\n' % (name, value))
        
        file.write('headAge %f\n' % self.headAgeModifier.getValue(human))
        file.write('faceAngle %f\n' % self.faceAngleModifier.getValue(human))
    '''
    
def load(app):
    category = app.getCategory('Modelling')
    taskview = HeadTaskView(category)
    
    '''
    app.addLoadHandler('face', taskview.loadHandler)
    app.addLoadHandler('headAge', taskview.loadHandler)
    app.addLoadHandler('faceAngle', taskview.loadHandler)

    app.addSaveHandler(taskview.saveHandler)
    '''
    print 'Head loaded'

def unload(app):
    pass


