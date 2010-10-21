#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, mh
class SettingsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Settings', category.app.getThemeResource('images', 'button_setting.png'), category.app.getThemeResource('images', 'button_setting_on.png'))

        self.shaderGroup = []
        self.shaderNo = gui3d.RadioButton(self,self.shaderGroup,mesh='data/3dobjs/button_generic_long.obj', position=[600,270,9.2],label="No shader",selected=True)
        self.shaderPhong = gui3d.RadioButton(self,self.shaderGroup,mesh='data/3dobjs/button_generic_long.obj', position=[600,300,9.2],label="Phong shader")
        self.shaderToon = gui3d.RadioButton(self,self.shaderGroup,mesh='data/3dobjs/button_generic_long.obj', position=[600,330,9.2],label="Toon shader")
        
        @self.shaderNo.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderNo, event)
            human = self.app.scene3d.selectedHuman
            human.mesh.setShader(0)
            
        @self.shaderPhong.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderPhong, event)
            self.setShader("data/shaders/glsl/phong_vertex_shader.txt", "data/shaders/glsl/phong_fragment_shader.txt")
                
        @self.shaderToon.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderToon, event)
            self.setShader("data/shaders/glsl/toon_vertex_shader.txt", "data/shaders/glsl/toon_fragment_shader.txt")
                
    def setShader(self, vertex, fragment):
            human = self.app.scene3d.selectedHuman
            try:
                human.vertex_shader = mh.createVertexShader(open(vertex).read())
                human.fragment_shader = mh.createFragmentShader(open(fragment).read())
                human.shader_program = mh.createShader(human.vertex_shader, human.fragment_shader)
                human.mesh.setShader(human.shader_program)
            except Exception as e:
                print "No shader support: " + str(e)

def load(app):
    category = app.getCategory('Settings','button_setting.png','button_setting_on.png')
    taskview = SettingsTaskView(category)
    print 'Settings imported'

def unload(app):
    pass


