#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module containing classes to handle modelling mode GUI operations.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers, Jose Capco

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements the 'guiadvance' class structures and methods to support GUI
Advance mode operations.
Advance mode is invoked by selecting the Advance mode icon from the main GUI control
bar at the top of the screen.
While in this mode, user actions (keyboard and mouse events) are passed into
this class for processing. Having processed an event this class returns control to the
main OpenGL/SDL/Application event handling loop.


"""

__docformat__ = 'restructuredtext'

import gui3d, hair, mh
from aljabr import *
import random
from math import sqrt, pow, log


class MakeHairTaskView(gui3d.TaskView):
    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'MakeHair', category.app.getThemeResource('images', 'makehair.png'), category.app.getThemeResource('images', 'makehair_on.png'))
        
        #member variables:
        self.number = 25
        self.gravity = 1.5
        self.cP = 14
        self.length=5.0
        
        #sliders
        self.cPSlider = gui3d.Slider(self, position=[600, 100, 9.2], value=14,min=4,max=30,label="Control Points")
        self.lengthSlider = gui3d.Slider(self, position=[600, 140, 9.2], value=5.0,min=0.0,max=7.0,label="Strand Length")
        self.numberSlider = gui3d.Slider(self, position=[600, 180, 9.2], value=25,min=1,max=260,label="Strands Number")
        self.gravitySlider = gui3d.Slider(self, position=[600, 220, 9.2], value=1.5,min=0.0,max=4.0,label="Gravity Factor")
        
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

        #buttons
        self.createButton = gui3d.Button(self,mesh='data/3dobjs/button_generic_long.obj', position=[600,270,9.2],label="Create Hair")
        self.deleteButton = gui3d.Button(self,mesh='data/3dobjs/button_generic_long.obj', position=[600,290,9.2],label="Delete Hair")

        @self.createButton.event
        def onClicked(event):
            scn = self.app.scene3d
            if scn.selectedHuman.hairObj:
                scn.clear(scn.selectedHuman.hairObj)
            obj = scn.newObj("hair")
            position = scn.selectedHuman.getPosition()
            rotation = scn.selectedHuman.getRotation()
            obj.x = position[0]
            obj.y = position[1]
            obj.z = position[2]
            obj.rx = rotation[0]
            obj.ry = rotation[1]
            obj.rz = rotation[2]
            obj.sx = 1.0
            obj.sy = 1.0
            obj.sz = 1.0
            obj.visibility = 1
            obj.shadeless = 0
            obj.pickable = 0
            obj.cameraMode = 0
            obj.text = ""
            obj.uvValues = []
            obj.indexBuffer = []
            fg = obj.createFaceGroup("ribbons")

            scn.selectedHuman.hairModelling = True
            #TODO  Jose: clear any hair originally created/ loaded from libraries
            mesh = scn.selectedHuman.mesh
            verts = mesh.getVerticesAndFacesForGroups(["head-back-skull","head-upper-skull","l-head-temple",\
            "r-head-temple"])[0]
            scalpVerts = len(verts) #Collects all vertices that are part of the head where hair grows!
            interval = int(scalpVerts/self.number) #variable used to randomly distribute scalp-vertices
            cPInterval = self.length/float(self.cP) #Length between c.P. for hairs being generated
            #self.number = 1 #for debug
            for i in range(0,self.number):
                if i==self.number-1:
                    r= random.randint(interval*i,scalpVerts-1)
                else:    
                    r = random.randint(interval*i,interval*(i+1))
                #r=1 #for debug
                v= verts[r].co
                normal = verts[r].no
                point2 = vadd(v,vmul(normal,self.length))
                curve=[vadd(v,vmul(normal,-0.5))]
                w,normal2,point22,curve2 =[],[],[],[]
                curve.append(vadd(v,vmul(normal,-0.2)))
                for j in range(1,self.cP-1):
                    curve.append(vadd(v,vmul(normal,cPInterval*j)))
                curve.append(point2)
                
                #adjusting gravity of curve
                gravitize(curve,self.gravity)
 
                hair.loadStrands(obj,curve)

            fg.setColor([0,0,0,255]) #rgba
            obj.updateIndexBuffer()
            obj.calcNormals()
            obj.shadeless = 1
            scn.selectedHuman.hairObj = obj
            scn.update()
            
        #see ADD website for details
        def f(x):
            u = pow(x,1.5)
            k = 16*self.gravity*self.gravity
            asinh = sqrt(k)*pow(u,1.5)
            asinh = log(asinh + sqrt(asinh*asinh + 1)) #taking asinh(sqrt(k)*pow(u,1.5))
            return sqrt(k*u*u*u +1)*(asinh/sqrt(k*k*u*u*u+k)+pow(u,1.5))/2
        
        def f_diff(x):
            k = 16*self.gravity*self.gravity
            return sqrt(1 + k*pow(x,6))
        
        def gravitize(curve,gFactor,start=1,res=0.04):
            delta  = vdist(curve[0],curve[len(curve)-1])/(len(curve)-1) #length of hair!
            
            """
            temp = vdist(vnorm(vsub(curve[len(curve)-1],curve[start])),[0,1,0])
            delta = pow(pow(length,2.0)-pow(curve[start][1]-curve[len(curve)-1][1],2.0),0.5)
            X= delta*pow(2.0,gFactor)
            c = pow(2.0,-8.0+gFactor)
            p0  = curve[start][:]
            p1 = curve[len(curve)-1][:]
            #print "Debug: length =",length," len(curve)=", len(curve), "delta= ", delta
            interval = length/(len(curve)-start-1)
            """
            k=self.gravity
            N = len(curve) - start
            vec1 = vsub(curve[len(curve)-1], curve[start])
            l = vlen(vec1) #should be more than 0
            cost = vdot(vec1,[0,1,0])/l
            xlen = l*sqrt(1-cost*cost)
            point1 = curve[start]
            point2 = curve[len(curve)-1]
            for i in xrange(start+1, len(curve)):
                #y=g(x)
                #vec1 = vsub(curve[i],curve[i-1])
                #l = vlen(vec1) #should be more than 0
                #cost = vdot(vec1,[0,1,0])/l
                #x = l*sqrt(1-cost*cost)
                x= newton_raphson(f,f_diff, delta*(i-start),delta*(i-start))
                curve[i] = in2pts(point1,point2,x/xlen) #two coordinates remain the same, one is gravitized.. thats y-axis
                curve[i][1] = k*pow(x,4)
                #curve[i][0]= #x
                #curve{i][1]=  #y
                
            """
                x=pow(interval*(i-start)/(4*c),1.0/3.0)
                curve[i] = in2pts(p0,p1,x/X)
                if temp < 3.0:
                    #print "Debug: detected normal strand on the middle of the head"
                    curve[i][1] = curve[i][1] - 0.005*pow(x,4)#curve[0][1] - (curve[i][1] - curve[0][1])
                else:
                    curve[i][1] = curve[i][1] - c*pow(x,4)
            """
            

class AdvancedCategory(gui3d.Category):

    def __init__(self, category):
        gui3d.Category.__init__(self, category, 'Advance', category.app.getThemeResource('images', 'button_advance.png'), category.app.getThemeResource('images', 'button_advance_on.png'))
        
        makehairView = MakeHairTaskView(self);
        
        @makehairView.event
        def onMouseWheel(event):
            if event.wheelDelta > 0:
                mh.cameras[0].eyeZ -= 0.65
                self.app.scene3d.redraw()
            else:
                mh.cameras[0].eyeZ += 0.65
                self.app.scene3d.redraw()
    
        @makehairView.event
        def onMouseDragged(event):
            diff = self.app.scene3d.getMouseDiff()
            leftButtonDown = event.button & 1
            middleButtonDown = event.button & 2
            rightButtonDown = event.button & 4
    
            if leftButtonDown and rightButtonDown or middleButtonDown:
                mh.cameras[0].eyeZ += 0.05 * diff[1]
            elif leftButtonDown:
                human = self.app.scene3d.selectedHuman
                rot = human.getRotation()
                rot[0] += 0.5 * diff[1]
                rot[1] += 0.5 * diff[0]
                human.setRotation(rot)
            elif rightButtonDown:
                human = self.app.scene3d.selectedHuman
                trans = human.getPosition()
                trans[0] += 0.1 * diff[0]
                trans[1] -= 0.1 * diff[1]
                human.setPosition(trans)
    

