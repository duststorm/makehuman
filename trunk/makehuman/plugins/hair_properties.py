#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, hair, font3d
from aljabr import vdist,vnorm,vmul,vsub,vadd
import random

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
        
        #member variables:
        self.number = 25
        self.gravity = 1.5
        self.cP = 14
        self.length=5.0
        
        gui3d.TaskView.__init__(self, category, 'Hair', category.app.getThemeResource('images', 'button_hair_det.png'), category.app.getThemeResource('images',
                                'button_hair_det_on.png'))
                                
        gui3d.Object(self, 'data/3dobjs/group_128x256.obj', self.app.getThemeResource('images', 'group_hair_tool.png'), [10, 211, 9.0])

        #############
        #SLIDERS
        #############
        self.redSlider = gui3d.Slider(self, self.app.getThemeResource('images', 'slider_red.png'), self.app.getThemeResource('images', 'slider.png'),
                                      self.app.getThemeResource('images', 'slider_focused.png'), position=[10, 235, 9.2])

        self.redSliderLabel = gui3d.TextView(self, mesh='data/3dobjs/empty.obj', position=[60, 350, 9.4])
        self.redSliderLabel.setText('Red: 0')

        self.greenSlider = gui3d.Slider(self, self.app.getThemeResource('images', 'slider_green.png'), self.app.getThemeResource('images', 'slider.png'),
                                        self.app.getThemeResource('images', 'slider_focused.png'), position=[10, 265, 9.2])

        self.greenSliderLabel = gui3d.TextView(self, mesh='data/3dobjs/empty.obj', position=[60, 370, 9.4])
        self.greenSliderLabel.setText('Green: 0')

        self.blueSlider = gui3d.Slider(self, self.app.getThemeResource('images', 'slider_blue.png'), self.app.getThemeResource('images', 'slider.png'),
                                       self.app.getThemeResource('images', 'slider_focused.png'), position=[10, 295, 9.2])

        self.blueSliderLabel = gui3d.TextView(self, mesh='data/3dobjs/empty.obj', position=[60, 390, 9.4])
        self.blueSliderLabel.setText('Blue: 0')
        
        self.cPSlider = gui3d.Slider(self, position=[600, 100, 9.2], value=14,min=4,max=30,label="Control Points")
        self.lengthSlider = gui3d.Slider(self, position=[600, 140, 9.2], value=5.0,min=0.0,max=7.0,label="Strand Length")
        self.numberSlider = gui3d.Slider(self, position=[600, 180, 9.2], value=25,min=1,max=260,label="Strands Number")
        self.gravitySlider = gui3d.Slider(self, position=[600, 220, 9.2], value=1.5,min=0.0,max=2.0,label="Gravity Factor")
        
        self.widthSlider = gui3d.Slider(self, self.app.getThemeResource('images', 'slider_hairs.png'),\
        self.app.getThemeResource('images', 'slider.png'),\
        self.app.getThemeResource('images', 'slider_focused.png'), [10, 150, 9], 1.0, 1.0,30.0) 

        #############
        #BUTTONS
        #############        
        self.createButton = gui3d.Button(self,mesh='data/3dobjs/button_generic_long.obj', position=[600,270,9.2],label="Create Hair")
        self.deleteButton = gui3d.Button(self,mesh='data/3dobjs/button_generic_long.obj', position=[600,290,9.2],label="Delete Hair")
        #self.doButton = gui3d.Button(self,position=[600,270,9.2],label="Create Hair")


        self.colorPreview = gui3d.Object(self, 'data/3dobjs/colorpreview.obj', position=[20, 340, 9.4])
        
        @self.createButton.event
        def onClicked(event):
            self.app.scene3d.selectedHuman.hairModelling = True
            #TODO  Jose: clear any hair originally created/ loaded from libraries
            mesh = self.app.scene3d.selectedHuman.mesh
            vertIndices = mesh.getVerticesAndFacesForGroups(["part_head-back-skull","part_head-upper-skull","part_l-head-temple",\
            "part_r-head-temple"])
            scalpVerts = len(vertIndices) #Collects all vertices that are part of the head where hair grows!
            interval = int(scalpVerts/self.number) #variable used to randomly distribute scalp-vertices
            cPInterval = self.length/float(self.cP) #Length between c.P. for hairs being generated
            """
            for i in range(0,self.number):
                if i==self.number-1:
                    r= random.randint(interval*i,scalpVerts-1)
                else:    
                    r = random.randint(interval*i,interval*(i+1))
                #Josenow
                v= mesh.verts[vertIndices[r]].co
                normal = mesh.verts[vertIndices[r]].no
                point2 = vadd(v,vmul(normal,gLength.val))
                curve=[vadd(v,vmul(normal,-0.5))]
                w,normal2,point22,curve2 =[],[],[],[]
                for j in range(0,scalpVerts):
                    w=mesh.verts[vertIndices[j]].co
                    dist = vdist(v,w)
                    if dist>=0.05 and dist<=0.3:
                        normal2=mesh.verts[vertIndices[j]].no
                        point22 = vadd(w,vmul(normal2,gLength.val))
                        curve2=[vadd(w,vmul(normal2,-0.5))]
                        break
                curve.append(vadd(v,vmul(normal,-0.2)))
                curve2.append(vadd(w,vmul(normal2,-0.2)))
                for j in range(1,noCPoints.val-1):
                    curve.append(vadd(v,vmul(normal,cPInterval*j)))
                    curve2.append(vadd(w,vmul(normal2,cPInterval*j)))
                curve.append(point2)
                curve2.append(point22)
                drawGuidePair(scn,curve[:],curve2[:])
            #r= random.randint(interval*(noGuides.val-1),scalpVerts-1)
            Blender.Redraw()
            """
            
        @self.cPSlider.event
        def onChange(value):
            self.cP = value;

        @self.lengthSlider.event
        def onChange(value):
            self.length = value;
 
        @self.numberSlider.event
        def onChange(value):
            self.number = value;

        @self.gravitySlider.event
        def onChange(value):
            self.gravity = value;
            
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
            human = self.app.scene3d.selectedHuman
            if len(human.hairObj.verts)>0 : 
               hairWidthUpdate(human.scene, human.hairObj, widthFactor=self.widthSlider.getValue())
            #pass #Do something!

    def changeColor(self, color):
        action = Action(self.app.scene3d.selectedHuman, self.app.scene3d.selectedHuman.hairColor, color, self.syncSliders)
        self.app.do(action)
        human = self.app.scene3d.selectedHuman
        c = [int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), 255]
        human.hairObj.facesGroups[0].setColor(c)

    def setColor(self, color):
        c = [int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), 255]
        for g in self.colorPreview.mesh.facesGroups:
            g.setColor(c)
        self.redSliderLabel.setText('Red:%i' % c[0])
        self.greenSliderLabel.setText('Green:%i' % c[1])
        self.blueSliderLabel.setText('Blue:%i' % c[2])

    def onShow(self, event):
        for o in self.objects:
         print "Debug Objects: ", o.mesh.name
        gui3d.TaskView.onShow(self, event)
        hairColor = self.app.scene3d.selectedHuman.hairColor
        self.syncSliders()

    def syncSliders(self):
        hairColor = self.app.scene3d.selectedHuman.hairColor
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
