import os.path
#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import module3d
import os
from aljabr import vsub, vcross, vlen

print 'Texture tool imported'

class TextureToolTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Texture tool')
        
        self.mesh = None
        self.object = None
        
        self.box = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Inspect')))
        group = []
        self.model = self.box.addWidget(gui.RadioButton(group, "Model", True))
        self.texture = self.box.addWidget(gui.RadioButton(group, "Texture"))
        self.textured = self.box.addWidget(gui.CheckBox("Textured", True))
        
        @self.model.mhEvent
        def onClicked(event):
            self.switchToModel()
            
        @self.texture.mhEvent
        def onClicked(event):
            self.switchToTexture()
            
        @self.textured.mhEvent
        def onClicked(event):
            if self.textured.selected:
                self.object.setTexture(gui3d.app.selectedHuman.mesh.texture)
            else:
                self.object.clearTexture()
            
    def switchToModel(self):
    
        human = gui3d.app.selectedHuman
        for f in self.mesh.faces:
            for i, v in enumerate(f.verts):
                v.co = human.mesh.faces[f.idx].verts[i].co[:]
        self.mesh.update()
            
    def switchToTexture(self):
    
        for f in self.mesh.faces:
            for i, v in enumerate(f.verts):
                uv = self.mesh.uvValues[f.uv[i]]
                v.co = [uv[0] * 20 - 10, uv[1] * 20 - 10, 0.0]
        self.mesh.update()
            
    def onShow(self, event):
    
        gui3d.TaskView.onShow(self, event)
        
        human = gui3d.app.selectedHuman
        human.hide()
        
        if not self.mesh:
        
            self.mesh = module3d.Object3D('texture_tool')
        
            self.mesh.uvValues = []
            self.mesh.indexBuffer = []
            
            # create group
            fg = self.mesh.createFaceGroup('texture_tool')
           
            self.mesh.area = 0.0
            for f in human.mesh.faces:
                verts = [self.mesh.createVertex(v.co) for v in f.verts]
                uv = [human.mesh.uvValues[i] for i in f.uv]
                face = fg.createFace(verts, uv)
                face.area = vlen(vcross(vsub(verts[2].co, verts[0].co), vsub(verts[3].co, verts[1].co))) / 2.0
                face.uvArea = vlen(vcross(vsub(uv[2] + [0.0], uv[0] + [0.0]), vsub(uv[3] + [0.0], uv[1] + [0.0]))) / 2.0
                self.mesh.area += face.area
                
            for f in self.mesh.faces:
                index = min(510, max(0, int(f.uvArea*510.0/(f.area/self.mesh.area))))
                if index > 255:
                    f.setColor([255 - (index - 255), 255 - (index - 255), 255, 255])
                else:
                    f.setColor([255, index, index, 255])
                
                    
            self.mesh.texture = human.mesh.texture
            self.mesh.setCameraProjection(0)
            self.mesh.setShadeless(1)
            self.mesh.updateIndexBuffer()
            
            self.object = self.addObject(gui3d.Object([0, 0, 0], self.mesh, True))
            
        else:
        
            self.mesh.area = 0.0
            for f in self.mesh.faces:
                for i, v in enumerate(f.verts):
                    v.co = human.mesh.faces[f.idx].verts[i].co[:]
                verts = f.verts
                f.area = vlen(vcross(vsub(verts[2].co, verts[0].co), vsub(verts[3].co, verts[1].co))) / 2.0
                self.mesh.area += f.area
        
            for f in self.mesh.faces:
                index = min(510, max(0, int(f.uvArea*510.0/(f.area/self.mesh.area))))
                if index > 255:
                    f.setColor([255 - (index - 255), 255 - (index - 255), 255, 255])
                else:
                    f.setColor([255, index, index, 255])
        
            self.mesh.update()
            if self.textured.selected:
                self.object.setTexture(human.mesh.texture)

    def onHide(self, event):
    
        gui3d.TaskView.onHide(self, event)

        gui3d.app.selectedHuman.show()
        
    def onMouseDragged(self, event):
        
        human = gui3d.app.selectedHuman
        
        human.show()
        self.object.hide()
        
        gui3d.TaskView.onMouseDragged(self, event)
        
        self.object.setPosition(human.getPosition())
        self.object.setRotation(human.getRotation())
            
        human.hide()
        self.object.show()
        
    def onMouseWheel(self, event):
        
        gui3d.app.selectedHuman.show()
        self.object.hide()
        
        gui3d.TaskView.onMouseWheel(self, event)
            
        gui3d.app.selectedHuman.hide()
        self.object.show()

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Experiments')
    taskview = category.addTask(TextureToolTaskView(category))
    print 'Texture tool loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements

def unload(app):
    print 'Texture tool unloaded'

