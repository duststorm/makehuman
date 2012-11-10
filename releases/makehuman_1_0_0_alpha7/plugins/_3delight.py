#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
if 'nt' in sys.builtin_module_names:
    sys.path.append('./pythonmodules')
import subprocess

print '3delight imported'

povray = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):

  # Create 3delight shaders

    subprocess.Popen('shaderdl data/shaders/3delight/lightmap_3delight.sl -o data/shaders/3delight/lightmap.sdl', shell=True)
    subprocess.Popen('shaderdl data/shaders/renderman/skin.sl -o data/shaders/renderman/skin.sdl', shell=True)
    subprocess.Popen('shaderdl data/shaders/renderman/scatteringtexture.sl -o data/shaders/renderman/scatteringtexture.sdl', shell=True)
    subprocess.Popen('shaderdl data/shaders/renderman/hair.sl -o data/shaders/renderman/hair.sdl', shell=True)
    subprocess.Popen('shaderdl data/shaders/renderman/shadowspot.sl -o data/shaders/renderman/shadowspot.sdl', shell=True)

    print '3delight loaded'


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print '3delight unloaded'


