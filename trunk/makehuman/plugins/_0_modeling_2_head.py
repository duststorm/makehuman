#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier
import mh
import qtgui as gui

print 'Head imported'

class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected, style=gui3d.ButtonStyle)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        self.parentWidget()._parent.hideAllBoxes()
        self.groupBox.show()
        
class HeadSlider(humanmodifier.ModifierSlider):
    def __init__(self, modifier, image, view):
        
        humanmodifier.ModifierSlider.__init__(self, min=-1.0, max=1.0, modifier=modifier, style=gui3d.SliderStyle._replace(height=56, normal=image), thumbStyle=gui3d.SliderThumbStyle._replace(height = 32, width = 32, normal="slider2.png", focused="slider2_focused.png"))
        
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
        gui3d.TaskView.__init__(self, category, 'Head')
        
        features = [
            ('head', [('data/targets/head/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/head/images/', i[3]) for i in
                [   
                    ('head-age', 'less', 'more', 'frontView'),
                    ('head-angle', 'in', 'out', 'rightView'), 
                    ('head-scale-depth', 'less', 'more', 'rightView'),
                    ('head-scale-horiz', 'less', 'more', 'frontView'),
                    ('head-scale-vert', 'more', 'less', 'frontView'),
                    ('head-trans', 'in', 'out', 'frontView'),
                    ('head-trans', 'down', 'up', 'frontView'),
                    ('head-trans', 'forward', 'backward', 'rightView'),
                          
                                                      
                ]]), 
            ('neck', [('data/targets/neck/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/neck/images/', i[3]) for i in
                [  
                    ('neck-scale-depth', 'less', 'more', 'rightView'),
                    ('neck-scale-horiz', 'less', 'more', 'frontView'),
                    ('neck-scale-vert', 'more', 'less', 'frontView'),
                    ('neck-trans', 'in', 'out', 'frontView'),
                    ('neck-trans', 'down', 'up', 'frontView'),
                    ('neck-trans', 'forward', 'backward', 'rightView'),
                          
                                                      
                ]]),
            ]

        y = 80
        
        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []
        
        self.modifiers = {}
        
        self.categoryBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Category')))
        
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
                    radio = self.categoryBox.addWidget(GroupBoxRadioButton(self.radioButtons, title, box, selected=len(self.radioButtons) == 0))
                    y += 24
            
                # Create sliders
                modifier = humanmodifier.GenderAgeEthnicAsymmetricModifier(template[0], 'value', template[2], template[3], False)
                self.modifiers['%s%d' % (name, index + 1)] = modifier

                slider = box.addView(HeadSlider(modifier, '%s%s-%s-%s.png' % (template[4], template[1], template[2], template[3]), template[5]))
                self.sliders.append(slider)
                
        y += 16

        self.hideAllBoxes()
        self.groupBoxes[0].show()
        
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
        
        if values[0] == 'head':
            modifier = self.modifiers.get(values[1].replace("-", " "), None)
            if modifier:
                modifier.setValue(human, float(values[2]))
       
    def saveHandler(self, human, file):
        
        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('head %s %f\n' % (name.replace(" ", "-"), value))
    
def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addView(HeadTaskView(category))
    
    app.addLoadHandler('head', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    print 'Head loaded'

def unload(app):
    pass


