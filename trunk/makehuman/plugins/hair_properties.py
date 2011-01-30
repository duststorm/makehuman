#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, hair, font3d

print 'hair properties imported'


class Action:

    def __init__(self, human, before, after, postAction=None):
        self.name = 'Change hair color'
        self.human = human
        self.before = before
        self.after = after
        self.postAction = postAction

    def do(self):
        self.human.hairColor = self.after
        if self.postAction:
            self.postAction()
        return True

    def undo(self):
        self.human.hairColor = self.before
        if self.postAction:
            self.postAction()
        return True


class HairPropertiesTaskView(gui3d.TaskView):

    def __init__(self, category):        
        
        gui3d.TaskView.__init__(self, category, 'Hair')
        
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Hair properties', gui3d.GroupBoxStyle._replace(height=25+36*4+38+6));y+=25

        #############
        #SLIDERS
        #############
        
        self.widthSlider = gui3d.Slider(self, [10, y, 9.3], value=1.0, min=0.3,max=30.0, label = "Hair width");y+=36
        
        self.redSlider = gui3d.Slider(self, [10, y, 9.01], label='Red: 0',
            style=gui3d.SliderStyle._replace(normal='slider_red.png'),
            thumbStyle=gui3d.SliderThumbStyle._replace(normal='color_slider.png', focused='color_slider_focused.png'));y+=36

        self.greenSlider = gui3d.Slider(self, [10, y, 9.02], label='Green: 0',
            style=gui3d.SliderStyle._replace(normal='slider_green.png'),
            thumbStyle=gui3d.SliderThumbStyle._replace(normal='color_slider.png', focused='color_slider_focused.png'));y+=36

        self.blueSlider = gui3d.Slider(self, [10, y, 9.03], label='Blue: 0',
            style=gui3d.SliderStyle._replace(normal='slider_blue.png'),
            thumbStyle=gui3d.SliderThumbStyle._replace(normal='color_slider.png', focused='color_slider_focused.png'));y+=36

        mesh = gui3d.RectangleMesh(112, 32)
        self.colorPreview = gui3d.Object(self, [18, y+2, 9.04], mesh)
                    
        @self.redSlider.event
        def onChanging(value):
            self.setColor([value, self.greenSlider.getValue(), self.blueSlider.getValue()])
            
        @self.redSlider.event
        def onChange(value):
            self.changeColor([value, self.greenSlider.getValue(), self.blueSlider.getValue()])

        @self.greenSlider.event
        def onChanging(value):
            self.setColor([self.redSlider.getValue(), value, self.blueSlider.getValue()])
            
        @self.greenSlider.event
        def onChange(value):
            self.changeColor([self.redSlider.getValue(), value, self.blueSlider.getValue()])
            
        @self.blueSlider.event
        def onChanging(value):
            self.setColor([self.redSlider.getValue(), self.greenSlider.getValue(), value])

        @self.blueSlider.event
        def onChange(value):
            self.changeColor([self.redSlider.getValue(), self.greenSlider.getValue(), value])
            
        @self.widthSlider.event
        def onChanging(value):
            human = self.app.selectedHuman
            if human.hairObj and len(human.hairObj.verts)>0 : 
               hairWidthUpdate(human.scene, human.hairObj, widthFactor=self.widthSlider.getValue())
            #pass #Do something!

    def changeColor(self, color):
        action = Action(self.app.selectedHuman, self.app.selectedHuman.hairColor, color, self.syncSliders)
        self.app.do(action)
        human = self.app.selectedHuman
        c = [int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), 255]
        if human.hairObj:
            human.hairObj.facesGroups[0].setColor(c)

    def setColor(self, color):
        c = [int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), 255]
        for g in self.colorPreview.mesh.facesGroups:
            g.setColor(c)
        self.redSlider.label.setText('Red:%i' % c[0])
        self.greenSlider.label.setText('Green:%i' % c[1])
        self.blueSlider.label.setText('Blue:%i' % c[2])

    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)
        hairColor = self.app.selectedHuman.hairColor
        self.widthSlider.setFocus()
        self.syncSliders()

    def syncSliders(self):
        hairColor = self.app.selectedHuman.hairColor
        self.redSlider.setValue(hairColor[0])
        self.greenSlider.setValue(hairColor[1])
        self.blueSlider.setValue(hairColor[2])
        self.setColor(hairColor)


category = None
taskview = None

def load(app):
    taskview = HairPropertiesTaskView(app.categories['Modelling'])
    print 'hair properties loaded'

def unload(app):
    print 'hair properties unloaded'


#obj = hair object
def hairWidthUpdate(scn, obj,res=0.04, widthFactor=1.0): #luckily both normal and vertex index of object remains the same!
  N=len(obj.verts)
  origWidth = vdist(obj.verts[1].co,obj.verts[0].co)/res
  diff= (widthFactor-origWidth)*res/2
  for i in xrange(0,N/2):
      vec=vmul(vnorm(vsub(obj.verts[i*2+1].co,obj.verts[i*2].co)), diff) 
      obj.verts[i*2].co=vsub(obj.verts[i*2].co,vec)
      obj.verts[i*2+1].co=vadd(obj.verts[i*2+1].co,vec)
      obj.verts[i*2].update(updateNor=0)
      obj.verts[i*2+1].update(updateNor=0)
