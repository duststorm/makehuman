#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module containing classes to handle modelling mode GUI operations.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements the 'guimodelling' class structures and methods to support GUI
Modelling mode operations.
Modelling mode is invoked by selecting the Modelling mode icon from the main GUI control
bar at the top of the screen.
While in this mode, user actions (keyboard and mouse events) are passed into
this class for processing. Having processed an event this class returns control to the
main OpenGL/SDL/Application event handling loop.


"""

__docformat__ = 'restructuredtext'

import mh
import events3d
import gui3d
import guimacromodelling
import guidetailmodelling
import mh2obj
import mh2bvh
import mh2mhx
import os


class ModellingCategory(gui3d.Category):

    def __init__(self, parent):
        gui3d.Category.__init__(self, parent, 'Modelling', parent.app.getThemeResource('images', 'button_home.png'), parent.app.getThemeResource('images',
                                'button_home_on.png'))
        guimacromodelling.MacroModelingTaskView(self)
        guidetailmodelling.DetailModelingTaskView(self)
        guidetailmodelling.MicroModelingTaskView(self)

    # Rotate and pan the camera

    def onMouseDragged(self, event):
        diff = self.app.scene3d.getMouseDiff()
        leftButtonDown = event.button & 1
        middleButtonDown = event.button & 2
        rightButtonDown = event.button & 4

        if leftButtonDown and rightButtonDown or middleButtonDown:
            mh.cameras[0].zoom += 0.05 * diff[1]
        elif leftButtonDown:
            human = self.app.scene3d.selectedHuman
            rot = human.getRotation()
            rot[0] += 0.5 * diff[1]
            rot[1] += 0.5 * diff[0]
            human.setRotation(rot)
        elif rightButtonDown:
            human = self.app.scene3d.selectedHuman
            trans = human.getPosition()
            trans[0] += 0.1 * diff[0]
            trans[1] -= 0.1 * diff[1]
            human.setPosition(trans)

    # Zoom the camera

    def onMouseWheel(self, event):
        if event.wheelDelta > 0:
            mh.cameras[0].zoom -= 0.65
            self.app.scene3d.redraw()
        else:
            mh.cameras[0].zoom += 0.65
            self.app.scene3d.redraw()

    def onKeyDown(self, event):

      # Other keybindings

        if event.key == events3d.SDLK_e:
            exportPath = mh.getPath('exports')
            if not os.path.exists(exportPath):
                os.makedirs(exportPath)
            mh2obj.exportObj(self.app.scene3d.selectedHuman.meshData, exportPath + '/quick_export.obj', 'data/3dobjs/base.obj')
            mh2bvh.exportSkeleton(self.app.scene3d.selectedHuman.meshData, exportPath + '/quick_export.bvh')
            mh2mhx.exportMhx(self.app.scene3d.selectedHuman.meshData, exportPath + '/quick_export.mhx')
        elif event.key == events3d.SDLK_g:
            grabPath = mh.getPath('grab')
            self.app.scene3d.grabScreen(180, 80, 440, 440, grabPath + '/grab.bmp')
        elif event.key == events3d.SDLK_q:
            self.app.stop()
        elif event.key == events3d.SDLK_s:
            print 'subdividing'
            self.app.scene3d.selectedHuman.subdivide()
        elif event.key == events3d.SDLK_y:
            self.app.redo()
        elif event.key == events3d.SDLK_z:
            self.app.undo()
        else:
            if not event.modifiers:

          # Camera rotation

                if event.key == events3d.SDLK_2 or event.key == events3d.SDLK_KP2:
                    human = self.app.scene3d.selectedHuman
                    rot = human.getRotation()
                    rot[0] += 5.0
                    human.setRotation(rot)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_4 or event.key == events3d.SDLK_KP4:
                    human = self.app.scene3d.selectedHuman
                    rot = human.getRotation()
                    rot[1] -= 5.0
                    human.setRotation(rot)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_6 or event.key == events3d.SDLK_KP6:
                    human = self.app.scene3d.selectedHuman
                    rot = human.getRotation()
                    rot[1] += 5.0
                    human.setRotation(rot)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_8 or event.key == events3d.SDLK_KP8:
                    human = self.app.scene3d.selectedHuman
                    rot = human.getRotation()
                    rot[0] -= 5.0
                    human.setRotation(rot)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_UP:

          # Camera pan

                    human = self.app.scene3d.selectedHuman
                    trans = human.getPosition()
                    trans[1] += 0.05
                    human.setPosition(trans)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_DOWN:
                    human = self.app.scene3d.selectedHuman
                    trans = human.getPosition()
                    trans[1] -= 0.05
                    human.setPosition(trans)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_RIGHT:
                    human = self.app.scene3d.selectedHuman
                    trans = human.getPosition()
                    trans[0] += 0.05
                    human.setPosition(trans)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_LEFT:
                    human = self.app.scene3d.selectedHuman
                    trans = human.getPosition()
                    trans[0] -= 0.05
                    human.setPosition(trans)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_PLUS or event.key == events3d.SDLK_KP_PLUS:

          # Camera zoom

                    mh.cameras[0].zoom += 0.65
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_MINUS or event.key == events3d.SDLK_KP_MINUS:
                    mh.cameras[0].zoom -= 0.65
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_7 or event.key == events3d.SDLK_KP7:

          # Camera views

                    self.app.scene3d.selectedHuman.setRotation([90.0, 0.0, 0.0])
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_1 or event.key == events3d.SDLK_KP1:
                    self.app.scene3d.selectedHuman.setRotation([0.0, 0.0, 0.0])
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_3 or event.key == events3d.SDLK_KP3:
                    self.app.scene3d.selectedHuman.setRotation([0.0, 90.0, 0.0])
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_PERIOD or event.key == events3d.SDLK_KP_PERIOD:
                    self.app.scene3d.selectedHuman.setPosition([0.0, 0.0, 0.0])
                    mh.cameras[0].zoom = 60.0
                    self.app.scene3d.redraw()
            elif event.modifiers == events3d.KMOD_NUM:

          # Camera rotation

                if event.key == events3d.SDLK_KP2:
                    human = self.app.scene3d.selectedHuman
                    rot = human.getRotation()
                    rot[0] += 5.0
                    human.setRotation(rot)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_KP4:
                    human = self.app.scene3d.selectedHuman
                    rot = human.getRotation()
                    rot[1] -= 5.0
                    human.setRotation(rot)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_KP6:
                    human = self.app.scene3d.selectedHuman
                    rot = human.getRotation()
                    rot[1] += 5.0
                    human.setRotation(rot)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_KP8:
                    human = self.app.scene3d.selectedHuman
                    rot = human.getRotation()
                    rot[0] -= 5.0
                    human.setRotation(rot)
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_KP7:

          # Camera views

                    self.app.scene3d.selectedHuman.setRotation([90.0, 0.0, 0.0])
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_KP1:
                    self.app.scene3d.selectedHuman.setRotation([0.0, 0.0, 0.0])
                    self.app.scene3d.redraw()
                elif event.key == events3d.SDLK_KP3:
                    self.app.scene3d.selectedHuman.setRotation([0.0, 90.0, 0.0])
                    self.app.scene3d.redraw()

        gui3d.Category.onKeyDown(self, event)


