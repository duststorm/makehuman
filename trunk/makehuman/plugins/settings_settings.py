#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, mh
class SettingsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Settings')

        self.shaderGroup = []
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Shader', gui3d.GroupBoxStyle._replace(height=140));y+=35
        self.shaderNo = gui3d.RadioButton(self,self.shaderGroup, [18,y, 9.2], "No shader", True);y+=25
        self.shaderPhong = gui3d.RadioButton(self,self.shaderGroup, [18,y,9.2], "Phong shader");y+=25
        self.shaderToon = gui3d.RadioButton(self,self.shaderGroup, [18,y,9.2], "Toon shader");y+=25
        self.shaderSkin = gui3d.RadioButton(self,self.shaderGroup, [18,y,9.2], "Skin shader");y+=35
        
        gui3d.GroupBox(self, [10, y, 9.0], 'Slider behavior', gui3d.GroupBoxStyle._replace(height=128));y+=35
        self.realtimeUpdates = gui3d.CheckBox(self, [18,y, 9.2], "Update real-time",
            self.app.settings.get('realtimeUpdates', True));y+=25
        self.realtimeNormalUpdates = gui3d.CheckBox(self, [18,y,9.2], "Update normals",
            self.app.settings.get('realtimeNormalUpdates', True));y+=25
        
        @self.shaderNo.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderNo, event)
            human = self.app.selectedHuman
            human.mesh.setShader(0)
            
        @self.shaderPhong.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderPhong, event)
            self.setShader("data/shaders/glsl/phong_vertex_shader.txt", "data/shaders/glsl/phong_fragment_shader.txt")
                
        @self.shaderToon.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderToon, event)
            self.setShader("data/shaders/glsl/toon_vertex_shader.txt", "data/shaders/glsl/toon_fragment_shader.txt")
            
        @self.shaderSkin.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderSkin, event)
            self.setShader("data/shaders/glsl/skin_vertex_shader.txt", "data/shaders/glsl/skin_fragment_shader.txt")
            self.app.selectedHuman.mesh.setShaderParameter("gradientMap", mh.loadTexture("data/textures/color_temperature.png", 0))
            self.app.selectedHuman.mesh.setShaderParameter("ambientOcclusionMap", mh.loadTexture("data/textures/female_young.tif", 0))
                
        @self.realtimeUpdates.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.realtimeUpdates, event)
            self.app.settings['realtimeUpdates'] = self.realtimeUpdates.selected
            
        @self.realtimeNormalUpdates.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.realtimeNormalUpdates, event)
            self.app.settings['realtimeNormalUpdates'] = self.realtimeNormalUpdates.selected
                
    def setShader(self, vertex, fragment):
            human = self.app.selectedHuman
            try:
                human.vertex_shader = mh.createVertexShader(open(vertex).read())
                human.fragment_shader = mh.createFragmentShader(open(fragment).read())
                human.shader_program = mh.createShader(human.vertex_shader, human.fragment_shader)
                human.mesh.setShader(human.shader_program)
            except Exception, e:
                print "No shader support: " + str(e)

def load(app):
    category = app.getCategory('Settings')
    taskview = SettingsTaskView(category)
    print 'Settings imported'

def unload(app):
    pass


