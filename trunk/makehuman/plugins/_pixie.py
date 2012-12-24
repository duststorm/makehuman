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

aqsis = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):

  # Create pixie shaders

    subprocess.Popen('sdrc data/shaders/pixie/lightmap_pixie.sl -o data/shaders/pixie/lightmap.sdr', shell=True)
    subprocess.Popen('sdrc data/shaders/pixie/read2dbm_pixie.sl -o data/shaders/pixie/read2dbm.sdr', shell=True)
    subprocess.Popen('sdrc data/shaders/renderman/skin.sl -o data/shaders/renderman/skin.sdr', shell=True)
    subprocess.Popen('sdrc data/shaders/renderman/hair.sl -o data/shaders/renderman/hair.sdr', shell=True)

    pixie = gui3d.TaskView(app.categories['Rendering'], 'Pixie', app.getThemeResource('images', 'button_pixie.png'))

    @pixie.mhEvent
    def onShow(event):
        pass

    @pixie.mhEvent
    def onHide(event):
        pass

    @pixie.button.mhEvent
    def onClicked(event):
        mh2renderman.saveScene(app.scene3d, 'scena.rib', 'renderman_output', 'pixie')


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass
