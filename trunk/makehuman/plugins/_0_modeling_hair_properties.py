#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import colorsys
import gui3d
from aljabr import vdist, vmul, vnorm, vsub, vadd

def rgbToHsl(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    return [int(h * 359.0), int(s * 100.0), int(l * 100.0)]
    
def hslToRgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 359.0, l / 100.0, s / 100.0)
    return [int(r * 255.0), int(g * 255.0), int(b * 255.0)]

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
        gui3d.GroupBox(self, [10, y, 9.0], 'Hair properties', gui3d.GroupBoxStyle._replace(height=25+36*7+38+6));y+=25

        #############
        #SLIDERS
        #############
        
        self.widthSlider = gui3d.Slider(self, [10, y, 9.3], 1.0, 0.3, 30.0, "Hair width: %.2f");y+=36
        
        self.redSlider = gui3d.Slider(self, [10, y, 9.01], 0, 0, 255, 'Red: %d',
            gui3d.SliderStyle._replace(normal='color_slider_background.png'),
            gui3d.SliderThumbStyle._replace(normal='color_slider.png', focused='color_slider_focused.png'));y+=36

        self.greenSlider = gui3d.Slider(self, [10, y, 9.02], 0, 0, 255, 'Green: %d',
            gui3d.SliderStyle._replace(normal='color_slider_background.png'),
            gui3d.SliderThumbStyle._replace(normal='color_slider.png', focused='color_slider_focused.png'));y+=36

        self.blueSlider = gui3d.Slider(self, [10, y, 9.03], 0, 0, 255, 'Blue: %d',
            gui3d.SliderStyle._replace(normal='color_slider_background.png'),
            gui3d.SliderThumbStyle._replace(normal='color_slider.png', focused='color_slider_focused.png'));y+=36
        
        self.hueSlider = gui3d.Slider(self, [10, y, 9.04], 0, 0, 359, 'Hue: %d');y+=36
        self.saturationSlider = gui3d.Slider(self, [10, y, 9.05], 0, 0, 100, 'Saturation: %d',
            gui3d.SliderStyle._replace(normal='color_slider_background.png'),
            gui3d.SliderThumbStyle._replace(normal='color_slider.png', focused='color_slider_focused.png'));y+=36
        self.lightnessSlider = gui3d.Slider(self, [10, y, 9.06], 0, 0, 100, 'Lightness: %d');y+=36

        mesh = gui3d.NineSliceMesh(112, 32, self.app.getThemeResource('images', 'color_preview.png'), [4,4,4,4])
        self.colorPreview = gui3d.Object(self, [18, y+2, 9.07], mesh)
                    
        @self.redSlider.mhEvent
        def onChanging(value):
            self.setColor([value, self.greenSlider.getValue(), self.blueSlider.getValue()])
            
        @self.redSlider.mhEvent
        def onChange(value):
            self.changeColor([value, self.greenSlider.getValue(), self.blueSlider.getValue()])

        @self.greenSlider.mhEvent
        def onChanging(value):
            self.setColor([self.redSlider.getValue(), value, self.blueSlider.getValue()])
            
        @self.greenSlider.mhEvent
        def onChange(value):
            self.changeColor([self.redSlider.getValue(), value, self.blueSlider.getValue()])
            
        @self.blueSlider.mhEvent
        def onChanging(value):
            self.setColor([self.redSlider.getValue(), self.greenSlider.getValue(), value])

        @self.blueSlider.mhEvent
        def onChange(value):
            self.changeColor([self.redSlider.getValue(), self.greenSlider.getValue(), value])
            
        @self.hueSlider.mhEvent
        def onChanging(value):
            self.setColor(hslToRgb(value, self.saturationSlider.getValue(), self.lightnessSlider.getValue()), False)

        @self.hueSlider.mhEvent
        def onChange(value):
            self.changeColor(hslToRgb(value, self.saturationSlider.getValue(), self.lightnessSlider.getValue()), False)
            
        @self.saturationSlider.mhEvent
        def onChanging(value):
            self.setColor(hslToRgb(self.hueSlider.getValue(), value, self.lightnessSlider.getValue()), False)

        @self.saturationSlider.mhEvent
        def onChange(value):
            self.changeColor(hslToRgb(self.hueSlider.getValue(), value, self.lightnessSlider.getValue()), False)
            
        @self.lightnessSlider.mhEvent
        def onChanging(value):
            self.setColor(hslToRgb(self.hueSlider.getValue(), self.saturationSlider.getValue(), value), False)

        @self.lightnessSlider.mhEvent
        def onChange(value):
            self.changeColor(hslToRgb(self.hueSlider.getValue(), self.saturationSlider.getValue(), value), False)
            
        @self.widthSlider.mhEvent
        def onChanging(value):
            human = self.app.selectedHuman
            if human.hairObj and len(human.hairObj.verts) > 0: 
               hairWidthUpdate(human.scene, human.hairObj, widthFactor=self.widthSlider.getValue())
            #pass #Do something!

    def changeColor(self, color, syncHsl=True):
        
        human = self.app.selectedHuman
        action = Action(self.app.selectedHuman, human.hairColor, [c/255.0 for c in color], self.syncSliders)
        self.app.do(action)
        if human.hairObj:
            human.hairObj.facesGroups[0].setColor(color, syncHsl)

    def setColor(self, color, syncHsl=True):
        
        red, green, blue = color
        
        self.colorPreview.mesh.setColor([red, green, blue, 255])
            
        f = self.redSlider.background.mesh.faces[0]
        f.color = [
            [0, green, blue, 255],
            [255, green, blue, 255],
            [255, green, blue, 255],
            [0, green, blue, 255]
        ]
        f.updateColors()
        
        f = self.greenSlider.background.mesh.faces[0]
        f.color = [
            [red, 0, blue, 255],
            [red, 255, blue, 255],
            [red, 255, blue, 255],
            [red, 0, blue, 255]
        ]
        f.updateColors()
        
        f = self.blueSlider.background.mesh.faces[0]
        f.color = [
            [red, green, 0, 255],
            [red, green, 255, 255],
            [red, green, 255, 255],
            [red, green, 0, 255]
        ]
        f.updateColors()
        
        h, s, l = rgbToHsl(red, green, blue)
        
        f = self.saturationSlider.background.mesh.faces[0]
        s0 = hslToRgb(h, 0, l)
        s1 = hslToRgb(h, 100, l)
        f.color = [
            s0 + [255],
            s1 + [255],
            s1 + [255],
            s0 + [255]
        ]
        f.updateColors()
        
        if syncHsl:
            self.hueSlider.setValue(h)
            self.saturationSlider.setValue(s)
            self.lightnessSlider.setValue(l)
        else:
            self.redSlider.setValue(red)
            self.greenSlider.setValue(green)
            self.blueSlider.setValue(blue)

    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)
        self.widthSlider.setFocus()
        self.syncSliders()

    def syncSliders(self):
        color = [int(c*255) for c in self.app.selectedHuman.hairColor]
        self.redSlider.setValue(color[0])
        self.greenSlider.setValue(color[1])
        self.blueSlider.setValue(color[2])
        self.setColor(color)

category = None
taskview = None

def load(app):
    category = app.categories['Modelling']
    taskview = category.addView(HairPropertiesTaskView())
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
