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
    usrShaderPath = os.path.join(mh.getPath('render'), 'ribFiles', 'shaders')
    if not os.path.isdir(usrShaderPath):
        os.makedirs(usrShaderPath)

  # Create aqsis shaders
  # subprocess.Popen("aqsl data/shaders/aqsis/lightmap_aqsis.sl -o %s" % (os.path.join(usrShaderPath, "lightmap.slx")), shell=True)

    subprocess.Popen('aqsl data/shaders/renderman/skin.sl -o "%s"' % os.path.join(usrShaderPath, 'skin.slx'), shell=True)
    subprocess.Popen('aqsl data/shaders/renderman/onlyci.sl -o "%s"' % os.path.join(usrShaderPath, 'onlyci.slx'), shell=True)
    subprocess.Popen('aqsl data/shaders/renderman/lightmap.sl -o "%s"' % os.path.join(usrShaderPath, 'lightmap.slx'), shell=True)
    subprocess.Popen('aqsl data/shaders/renderman/hair.sl -o "%s"' % os.path.join(usrShaderPath, 'hair.slx'), shell=True)
    subprocess.Popen('aqsl data/shaders/renderman/shadowspot.sl -o "%s"' % os.path.join(usrShaderPath, 'shadowspot.slx'), shell=True)

    aqsis = gui3d.TaskView(app.categories['Rendering'], 'Aqsis', app.getThemeResource('images', 'button_aqsis.png'))

    @aqsis.event
    def onShow(event):
        pass

    @aqsis.event
    def onHide(event):
        pass

    @aqsis.button.event
    def onClicked(event):
        renderPath = mh.getPath('render')
        if not os.path.exists(renderPath):
            os.makedirs(renderPath)
        mh2renderman.saveScene(app.scene3d, 'scena.rib', renderPath, 'aqsis')

    print 'aqsis loaded'


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'aqsis unloaded'


