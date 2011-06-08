#!/usr/bin/python
# -*- coding: utf-8 -*-

import gui3d, hair
from aljabr import *
import random
from math import sqrt, pow, log
from collision import collision
import simpleoctree

print 'makehair plugin'

class MakeHairTaskView(gui3d.TaskView):
    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'MakeHair')
        
        #member variables
        self.number = 25
        self.gravity = 1.5
        self.cP = 14
        self.length=5.0
        app = self.app
        if len(app.selectedHuman.meshStored)==0: 
            app.selectedHuman.storeMesh()
        self.octree = simpleoctree.SimpleOctree(app.selectedHuman.meshStored,0.09)   
        #sliders
        y=80
        gui3d.GroupBox(self, [10, y, 9.0], 'Options', gui3d.GroupBoxStyle._replace(height=25+36*4+24*4+6));y+=25
        self.cPSlider = gui3d.Slider(self, [10, y, 9.3], value=14,min=4,max=30,label="Control Points: %d");y+=36
        self.lengthSlider = gui3d.Slider(self, [10, y, 9.3], value=5.0,min=0.0,max=7.0,label="Strand Length: %.2f");y+=36
        self.numberSlider = gui3d.Slider(self, [10, y, 9.3], value=25,min=1,max=260,label="Strands Number: %d");y+=36
        self.gravitySlider = gui3d.Slider(self, [10, y, 9.3], value=1.5,min=0.0,max=4.0,label="Gravity Factor: %.2f");y+=36
        self.cPEntry = gui3d.TextEdit(self, [18, y, 9.3], "9,12", gui3d.TextEditStyle._replace(width=112), gui3d.floatValidator);y+=24
        
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
        self.collisionButton = gui3d.Button(self, [18, y, 9.3], "Avoid Collision");y+=24
        
        self.createButton = gui3d.Button(self, [18, y, 9.3], "Create Hair");y+=24
        self.deleteButton = gui3d.Button(self, [18, y, 9.3], "Delete Hair");y+=24
        
        @self.collisionButton.event
        def onClicked(event):
            #todo try catch when self.cPEntry has invalid values
            #showing my lambda skills..
            cPIndices = map(lambda x: int(x), self.cPEntry.text.split(","))
            for curve in self.app.selectedHuman.hairs.guides:
                collision(self.octree,curve,app.selectedHuman.meshData.verts,0.09,cPIndices,True)
            self.app.selectedHuman.hairs.reloadGuides()
        
        @self.createButton.event
        def onClicked(event):
            scn = self.app.scene3d
            if app.selectedHuman.hairObj:
                scn.clear(app.selectedHuman.hairObj)
            obj = scn.newObj("hair")
            position = app.selectedHuman.getPosition()
            rotation = app.selectedHuman.getRotation()
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

            app.selectedHuman.hairModelling = True
            #TODO  Jose: clear any hair originally created/ loaded from libraries
            mesh = app.selectedHuman.mesh
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
            obj.calcNormals()
            obj.shadeless = 1
            app.selectedHuman.hairObj = obj
            obj.updateIndexBuffer()
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
            


category = None
makehairView = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Experiments')
    makehairView = MakeHairTaskView(category)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements

def unload(app):
    print 'makehair unloaded'


