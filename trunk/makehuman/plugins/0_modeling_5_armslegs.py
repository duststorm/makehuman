#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier
import mh
import qtgui as gui

print 'Arms and leg imported'

class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        self.parentWidget()._parent.groupBox.showWidget(self.groupBox)
        # self.parentWidget()._parent.hideAllBoxes()
        # self.groupBox.show()
        
class HeadSlider(humanmodifier.ModifierSlider):
    def __init__(self,modifier, image, view):
        
        humanmodifier.ModifierSlider.__init__(self, min=-1.0, max=1.0, modifier=modifier)
        
        self.view = getattr(gui3d.app, view)
        
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
            ('right hand', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/armslegs/images/', i[3]) for i in
                [                     
                    ('r-hand-scale-depth', 'decr', 'incr', 'setRightHandTopCamera'),
                    ('r-hand-scale-horiz', 'decr', 'incr', 'setRightHandFrontCamera'),
                    ('r-hand-scale-vert', 'decr', 'incr', 'setRightHandFrontCamera'),
                    ('r-hand-trans', 'in', 'out', 'setRightHandFrontCamera'),
                    ('r-hand-trans', 'down', 'up', 'setRightHandFrontCamera'),
                    ('r-hand-trans', 'forward', 'backward', 'setRightHandTopCamera'),                          
                                                      
                ]]),
            ('left hand', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/armslegs/images/', i[3]) for i in
                [                     
                    ('l-hand-scale-depth', 'decr', 'incr', 'setLeftHandTopCamera'),
                    ('l-hand-scale-horiz', 'decr', 'incr', 'setLeftHandFrontCamera'),
                    ('l-hand-scale-vert', 'decr', 'incr', 'setLeftHandFrontCamera'),
                    ('l-hand-trans', 'in', 'out', 'setLeftHandFrontCamera'),
                    ('l-hand-trans', 'down', 'up', 'setLeftHandFrontCamera'),
                    ('l-hand-trans', 'forward', 'backward', 'setLeftHandTopCamera'),                          
                                                      
                ]]),
            ('right foot', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/armslegs/images/', i[3]) for i in
                [                     
                    ('r-foot-scale-depth', 'decr', 'incr', 'setRightFootRightCamera'),
                    ('r-foot-scale-horiz', 'decr', 'incr', 'setRightFootFrontCamera'),
                    ('r-foot-scale-vert', 'decr', 'incr', 'setRightFootFrontCamera'),
                    ('r-foot-trans', 'in', 'out', 'setRightFootFrontCamera'),
                    ('r-foot-trans', 'down', 'up', 'setRightFootFrontCamera'),
                    ('r-foot-trans', 'forward', 'backward', 'setRightFootRightCamera'),                          
                                                      
                ]]),
            ('left foot', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/armslegs/images/', i[3]) for i in
                [                     
                    ('l-foot-scale-depth', 'decr', 'incr', 'setLeftFootLeftCamera'),
                    ('l-foot-scale-horiz', 'decr', 'incr', 'setLeftFootFrontCamera'),
                    ('l-foot-scale-vert', 'decr', 'incr', 'setLeftFootFrontCamera'),
                    ('l-foot-trans', 'in', 'out', 'setLeftFootFrontCamera'),
                    ('l-foot-trans', 'down', 'up', 'setLeftFootFrontCamera'),
                    ('l-foot-trans', 'forward', 'backward', 'setLeftFootLeftCamera'),                          
                                                      
                ]]), 
            ('left arm', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/armslegs/images/', i[3]) for i in
                [                     
                    ('l-lowerarm-scale-depth', 'decr', 'incr', 'setLeftArmTopCamera'),
                    ('l-lowerarm-scale-horiz', 'decr', 'incr', 'setLeftArmFrontCamera'),
                    ('l-lowerarm-scale-vert', 'decr', 'incr', 'setLeftArmFrontCamera'),
                    ('l-lowerarm-trans', 'in', 'out', 'setLeftArmFrontCamera'),
                    ('l-lowerarm-trans', 'down', 'up', 'setLeftArmFrontCamera'),
                    ('l-lowerarm-trans', 'forward', 'backward', 'setLeftArmTopCamera'), 
                    ('l-upperarm-scale-depth', 'decr', 'incr', 'setLeftArmTopCamera'),
                    ('l-upperarm-scale-horiz', 'decr', 'incr', 'setLeftArmFrontCamera'),
                    ('l-upperarm-scale-vert', 'decr', 'incr', 'setLeftArmFrontCamera'),
                    ('l-upperarm-trans', 'in', 'out', 'setLeftArmFrontCamera'),
                    ('l-upperarm-trans', 'down', 'up', 'setLeftArmFrontCamera'),
                    ('l-upperarm-trans', 'forward', 'backward', 'setLeftArmTopCamera'),                          
                                                      
                ]]), 
            ('right arm', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/armslegs/images/', i[3]) for i in
                [                     
                    ('r-lowerarm-scale-depth', 'decr', 'incr', 'setRightArmTopCamera'),
                    ('r-lowerarm-scale-horiz', 'decr', 'incr', 'setRightArmFrontCamera'),
                    ('r-lowerarm-scale-vert', 'decr', 'incr', 'setRightArmFrontCamera'),
                    ('r-lowerarm-trans', 'in', 'out', 'setRightArmFrontCamera'),
                    ('r-lowerarm-trans', 'down', 'up', 'setRightArmFrontCamera'),
                    ('r-lowerarm-trans', 'forward', 'backward', 'setRightArmTopCamera'), 
                    ('r-upperarm-scale-depth', 'decr', 'incr', 'setRightArmTopCamera'),
                    ('r-upperarm-scale-horiz', 'decr', 'incr', 'setRightArmFrontCamera'),
                    ('r-upperarm-scale-vert', 'decr', 'incr', 'setRightArmFrontCamera'),
                    ('r-upperarm-trans', 'in', 'out', 'setRightArmFrontCamera'),
                    ('r-upperarm-trans', 'down', 'up', 'setRightArmFrontCamera'),
                    ('r-upperarm-trans', 'forward', 'backward', 'setRightArmTopCamera'),                          
                                                      
                ]]), 
            ('left leg', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/armslegs/images/', i[3]) for i in
                [                     
                    ('l-lowerleg-scale-depth', 'decr', 'incr', 'setLeftLegLeftCamera'),
                    ('l-lowerleg-scale-horiz', 'decr', 'incr', 'setLeftLegFrontCamera'),
                    ('l-lowerleg-scale-vert', 'decr', 'incr', 'setLeftLegFrontCamera'),
                    ('l-lowerleg-trans', 'in', 'out', 'setLeftLegFrontCamera'),
                    ('l-lowerleg-trans', 'down', 'up', 'setLeftLegFrontCamera'),
                    ('l-lowerleg-trans', 'forward', 'backward', 'setLeftLegLeftCamera'), 
                    ('l-upperleg-scale-depth', 'decr', 'incr', 'setLeftLegLeftCamera'),
                    ('l-upperleg-scale-horiz', 'decr', 'incr', 'setLeftLegFrontCamera'),
                    ('l-upperleg-scale-vert', 'decr', 'incr', 'setLeftLegFrontCamera'),
                    ('l-upperleg-trans', 'in', 'out', 'setLeftLegFrontCamera'),
                    ('l-upperleg-trans', 'down', 'up', 'setLeftLegFrontCamera'),
                    ('l-upperleg-trans', 'forward', 'backward', 'setLeftLegLeftCamera'),                          
                                                      
                ]]), 
            ('right leg', [('data/targets/armslegs/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/armslegs/images/', i[3]) for i in
                [                     
                    ('r-lowerleg-scale-depth', 'decr', 'incr', 'setRightLegRightCamera'),
                    ('r-lowerleg-scale-horiz', 'decr', 'incr', 'setRightLegFrontCamera'),
                    ('r-lowerleg-scale-vert', 'decr', 'incr', 'setRightLegFrontCamera'),
                    ('r-lowerleg-trans', 'in', 'out', 'setRightLegFrontCamera'),
                    ('r-lowerleg-trans', 'down', 'up', 'setRightLegFrontCamera'),
                    ('r-lowerleg-trans', 'forward', 'backward', 'setRightLegRightCamera'), 
                    ('r-upperleg-scale-depth', 'decr', 'incr', 'setRightLegRightCamera'),
                    ('r-upperleg-scale-horiz', 'decr', 'incr', 'setRightLegFrontCamera'),
                    ('r-upperleg-scale-vert', 'decr', 'incr', 'setRightLegFrontCamera'),
                    ('r-upperleg-trans', 'in', 'out', 'setRightLegFrontCamera'),
                    ('r-upperleg-trans', 'down', 'up', 'setRightLegFrontCamera'),
                    ('r-upperleg-trans', 'forward', 'backward', 'setRightLegRightCamera'),                          
                                                      
                ]]), 
            ]

        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []
        
        self.modifiers = {}
        
        self.categoryBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Category')))
        self.groupBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.StackedBox()))
        
        for name, templates in features:
            
            for index, template in enumerate(templates):
                
                if index % 12 == 0:
                    
                    if len(templates) <= 12:
                        title = name.capitalize()
                    else:
                        title = '%s %d' % (name.capitalize(), index / 12 + 1)
                        
                    # Create box
                    box = self.groupBox.addWidget(gui.GroupBox(title))
                    self.groupBoxes.append(box)
                    
                    # Create radiobutton
                    radio = self.categoryBox.addWidget(GroupBoxRadioButton(self.radioButtons, title, box, selected=len(self.radioButtons) == 0))
            
                # Create sliders
                modifier = humanmodifier.GenderAgeEthnicAsymmetricModifier(template[0], 'value', template[2], template[3], False)
                self.modifiers['%s%d' % (name, index + 1)] = modifier

                slider = box.addWidget(HeadSlider(modifier, '%s%s-%s-%s.png' % (template[4], template[1], template[2], template[3]), template[5]))
                self.sliders.append(slider)

        self.groupBox.showWidget(self.groupBoxes[0])
        # self.hideAllBoxes()
        # self.groupBoxes[0].show()
        
    def hideAllBoxes(self):
        
        for box in self.groupBoxes:
            
            box.hide()
    
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        
        gui3d.app.setFaceCamera()
        
        for slider in self.sliders:
            slider.update()
            
    def onResized(self, event):
        
        self.categoryBox.setPosition([event.width - 150, self.categoryBox.getPosition()[1], 9.0])
        
    def onHumanChanged(self, event):

        human = event.human

        for slider in self.sliders:
            slider.update()

    def loadHandler(self, human, values):
        
        if values[0] == 'armslegs':
            modifier = self.modifiers.get(values[1].replace("-", " "), None)
            if modifier:
                modifier.setValue(human, float(values[2]))
       
    def saveHandler(self, human, file):
        
        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('armslegs %s %f\n' % (name.replace(" ", "-"), value))
    
def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addView(HeadTaskView(category))
    
    app.addLoadHandler('armslegs', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    print 'Armslegs loaded'

def unload(app):
    pass


