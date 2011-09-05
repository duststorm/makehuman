#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import humanmodifier

print 'Face imported'

class GroupBoxRadioButton(gui3d.RadioButton):
    def __init__(self, parent, group, label, groupBox, selected=False):
        gui3d.RadioButton.__init__(self, parent, group, label, selected, style=gui3d.ButtonStyle)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        gui3d.RadioButton.onClicked(self, event)
        self.parent.parent.hideAllBoxes()
        self.groupBox.show()
        
class FaceSlider(humanmodifier.ModifierSlider):
    def __init__(self, parent, modifier, left, right):
        
        humanmodifier.ModifierSlider.__init__(self, parent, min=-1.0, max=1.0, modifier=modifier, style=gui3d.SliderStyle._replace(height=56))
        
        mesh = gui3d.RectangleMesh(self.style.width / 2, self.style.height, left)
        self.left = gui3d.Object(self, [self.style.left, self.style.top, self.style.zIndex + 0.005], mesh)
        
        mesh = gui3d.RectangleMesh(self.style.width / 2, self.style.height, right)
        self.right = gui3d.Object(self, [self.style.left + self.style.width / 2, self.style.top, self.style.zIndex + 0.005], mesh)

class FaceTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Face2')
        
        features = [
            ('eyes', [('data/targets/eyes/${ethnic}/${gender}_${age}/%s-${%s}.target' % (i[0], i[1]), i[0], i[1], i[2], i[3], 'data/targets/eyes/images/') for i in
                [('eye-dist', 'eyedist', 'min', 'max'), ('eye-move', 'eyemove', 'down', 'up'), ('l-eye', 'leye', 'small', 'big'), ('l-eye-height1', 'leyeheight1', 'min', 'max'), ('l-eye-height2', 'leyeheight2', 'min', 'max'),
                 ('l-eye-height3', 'leyeheight3', 'min', 'max'), ('l-eye-push', 'leyepush', 'in', 'out'), ('r-eye', 'reye', 'small', 'big'), ('r-eye-height1', 'reyeheight1', 'min', 'max'), ('r-eye-height2', 'reyeheight2', 'min', 'max'),
                 ('r-eye-height3', 'reyeheight3', 'min', 'max'), ('r-eye-push', 'reyepush', 'in', 'out')]]),
            ('nose', [('data/targets/nose/${ethnic}/${gender}_${age}/%s-${%s}.target' % (i[0], i[1]), i[0], i[1], i[2], i[3], 'data/targets/nose/images/') for i in
                [('nose', 'nose', 'concave', 'convex'), ('nose-height', 'noseheight', 'min', 'max'), ('nose-nostrils', 'nosenostrils', 'down', 'up'), ('nose-nostril-width', 'nosenostrilwidth', 'min', 'max'),
                ('nose-point', 'nosepoint', 'down', 'up'), ('nose', 'noselength', 'short', 'long'), ('nose-width', 'nosewidth', 'min', 'max')]]),
            ]

        y = 80
        
        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []
        
        self.modifiers = {}
        
        self.categoryBox = gui3d.GroupBox(self, [650, y, 9.0], 'Category', gui3d.GroupBoxStyle._replace(height=25+24*sum([(len(templates[1])/10 + (len(templates[1])%10>0)) for templates in features])+6))
        y += 25
        
        for name, templates in features:
            
            for index, template in enumerate(templates):
                
                if index % 6 == 0:
                    
                    if len(templates) <= 6:
                        title = name.capitalize()
                    else:
                        title = '%s %d' % (name.capitalize(), index / 6 + 1)
                        
                    # Create box
                    box = gui3d.GroupBox(self, [10, 80, 9.0], title, gui3d.GroupBoxStyle._replace(height=25+36*min(len(templates)-index, 10)+6))
                    self.groupBoxes.append(box)
                    
                    # Create radiobutton
                    radio = GroupBoxRadioButton(self.categoryBox, self.radioButtons, title, box, selected=len(self.radioButtons) == 0)
                    y += 24
            
                # Create sliders
                modifier = humanmodifier.GenderAgeEthnicAsymmetricModifier(template[0], template[2], template[3], template[4], False)
                self.modifiers['%s%d' % (name, index + 1)] = modifier
                slider = FaceSlider(box, modifier, '%s%s-%s.png' % (template[5], template[1], template[3]), '%s%s-%s.png' % (template[5], template[1], template[4]))
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
    taskview = FaceTaskView(category)
    
    '''
    app.addLoadHandler('face', taskview.loadHandler)
    app.addLoadHandler('headAge', taskview.loadHandler)
    app.addLoadHandler('faceAngle', taskview.loadHandler)

    app.addSaveHandler(taskview.saveHandler)
    '''
    print 'Face loaded'

def unload(app):
    pass


