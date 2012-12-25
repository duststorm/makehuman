#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier
import mh
import qtgui as gui

class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        self.parentWidget()._parent.groupBox.showWidget(self.groupBox)
        
class HeadSlider(humanmodifier.ModifierSlider):
    def __init__(self, modifier, image, view):
        
        super(HeadSlider, self).__init__(min=-1.0, max=1.0, modifier=modifier, image=image)
        
        self.view = getattr(gui3d.app, view)
        
    def onFocus(self, event):
        super(HeadSlider, self).onFocus(event)
        if gui3d.app.settings.get('cameraAutoZoom', True):
            self.view()

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
        
    def hideAllBoxes(self):
        
        for box in self.groupBoxes:
            
            box.hide()
    
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        
        if gui3d.app.settings.get('cameraAutoZoom', True):
            gui3d.app.setFaceCamera()
        
        for slider in self.sliders:
            slider.update()
        
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
    taskview = category.addTask(HeadTaskView(category))
    
    app.addLoadHandler('head', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

def unload(app):
    pass


