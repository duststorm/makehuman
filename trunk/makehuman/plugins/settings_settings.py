#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, mh
class SettingsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Settings', category.app.getThemeResource('images', 'button_setting.png'), category.app.getThemeResource('images', 'button_setting_on.png'))

        self.shaderToggle = gui3d.ToggleButton(self,mesh='data/3dobjs/button_generic_long.obj', position=[600,270,9.2],label="Use shaders")
        
        @self.shaderToggle.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.shaderToggle, event)
            human = self.app.scene3d.selectedHuman
            if self.shaderToggle.selected:
                try:
                    if not hasattr(human, 'vertex_shader') or not human.vertex_shader:
                      human.vertex_shader = mh.createVertexShader(open("data/shaders/glsl/phong_vertex_shader.txt").read())
                    if not hasattr(human, 'fragment_shader') or not human.fragment_shader:
                      human.fragment_shader = mh.createFragmentShader(open("data/shaders/glsl/phong_fragment_shader.txt").read())
                    if not hasattr(human, 'shader_program') or not human.shader_program:
                      human.shader_program = mh.createShader(human.vertex_shader, human.fragment_shader)
                    human.mesh.setShader(human.shader_program)
                except Exception as e:
                    print "No shader support: " + str(e)
            else:
                human.mesh.setShader(0)

def load(app):
    category = app.getCategory('Settings','button_setting.png','button_setting_on.png')
    taskview = SettingsTaskView(category)
    print 'Settings imported'

def unload(app):
    pass


