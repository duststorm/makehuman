#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import mh
import os
import sys
if 'nt' in sys.builtin_module_names:
    sys.path.append('./pythonmodules')
import subprocess
import mh2renderman


class AqsisTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Aqsis', category.app.getThemeResource('images', 'button_aqsis.png'), category.app.getThemeResource('images', 'button_aqsis_on.png'))

        self.sceneToRender = mh2renderman.RMRScene(self.app)
        #Create aqsis shaders
        subprocess.Popen('aqsl data/shaders/aqsis/skin.sl -o "%s"' % os.path.join(self.sceneToRender.usrShaderPath, 'skin.slx'), shell=True)
        subprocess.Popen('aqsl data/shaders/aqsis/hair.sl -o "%s"' % os.path.join(self.sceneToRender.usrShaderPath, 'hair.slx'), shell=True)

        self.renderButton = gui3d.Button(self, mesh='data/3dobjs/button_generic.obj', texture=self.app.getThemeResource('images', 'button_rendering_start.png'),
                                    selectedTexture=self.app.getThemeResource('images', 'button_rendering_start_on.png'), position=[20, 100, 9])  # getThemeResource returns a texture for a gui element according to the chosen theme

        @self.renderButton.event
        def onClicked(event):            
            self.sceneToRender.render("scene.rib")    


def load(app):
    category = app.getCategory('Rendering','button_render.png','button_render_on.png')
    taskview = AqsisTaskView(category)

def unload(app):
    pass


