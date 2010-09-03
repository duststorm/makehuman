#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
if 'nt' in sys.builtin_module_names:
    sys.path.append('./pythonmodules')
import subprocess

# We need this for rendering

import mh2renderman

# We need this for gui controls

import gui3d
import mh
import os

print 'aqsis imported'

aqsis = None


# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):

    sceneToRender = mh2renderman.RMRScene(app.scene3d,app.modelCamera)

    #Create aqsis shaders
    subprocess.Popen('aqsl data/shaders/aqsis/skin.sl -o "%s"' % os.path.join(sceneToRender.usrShaderPath, 'skin.slx'), shell=True)
    subprocess.Popen('aqsl data/shaders/aqsis/hair.sl -o "%s"' % os.path.join(sceneToRender.usrShaderPath, 'hair.slx'), shell=True)

    aqsis = gui3d.TaskView(app.categories['Rendering'], 'Aqsis', app.getThemeResource('images', 'button_aqsis.png'))
    
    
    @aqsis.event
    def onShow(event):
        pass

    @aqsis.event
    def onHide(event):
        pass

    @aqsis.button.event
    def onClicked(event):        
        Area = app.categories['Rendering'].guideArea.getValue()
        fallingHair = app.categories['Rendering'].fallingHair.selected
        sceneToRender.render("scene.rib",Area,fallingHair)
        #mh2renderman.saveScene(app.modelCamera, app.scene3d, 'scena.rib', renderPath, 'aqsis', Area)
        

    print 'aqsis loaded'


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'aqsis unloaded'


