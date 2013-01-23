#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import events3d
import gui3d
import humanmodifier
from operator import mul
from string import Template
import re
import os
import mh
import gui
import log

class DetailTool(events3d.EventHandler):

    def __init__(self, app, micro, left, right):
        gui3d.app = app
        self.micro = micro
        self.left = left
        self.before = None
        self.right = right
        self.modifier = None
        self.symmetryModifier = None
        self.selectedGroups = []

    def onMouseDown(self, event):
        human = gui3d.app.selectedHuman

    # Find the target name

        if self.micro:
            folder = 'data/targets/microdetails/'
            part = gui3d.app.selectedGroup.name
        else:
            folder = 'data/targets/details/'
            part = human.getPartNameForGroupName(gui3d.app.selectedGroup.name)

    # Find the targets

        leftTarget = '%s%s%s.target' % (folder, part, self.left)
        rightTarget = '%s%s%s.target' % (folder, part, self.right)

        self.modifier = None
        if not (leftTarget and rightTarget):
            log.notice('No targets available')
            return

        self.modifier = humanmodifier.Modifier(leftTarget, rightTarget)

        # Save the state

        self.before = {}
        self.before[leftTarget] = human.getDetail(leftTarget)
        self.before[rightTarget] = human.getDetail(rightTarget)

        # Add symmetry targets if needed

        self.symmetryModifier = None
        if human.symmetryModeEnabled:
            symmetryPart = human.getSymmetryPart(part)
            if symmetryPart:
                if self.left.find('trans-in') != -1 or self.left.find('trans-out') != -1:
                    leftSymmetryTarget = '%s%s%s.target' % (folder, symmetryPart, self.right)
                    rightSymmetryTarget = '%s%s%s.target' % (folder, symmetryPart, self.left)
                else:
                    leftSymmetryTarget = '%s%s%s.target' % (folder, symmetryPart, self.left)
                    rightSymmetryTarget = '%s%s%s.target' % (folder, symmetryPart, self.right)
                self.symmetryModifier = humanmodifier.Modifier(leftSymmetryTarget, rightSymmetryTarget)

                # Save the state
                
                self.before[leftSymmetryTarget] = human.getDetail(leftSymmetryTarget)
                self.before[rightSymmetryTarget] = human.getDetail(rightSymmetryTarget)
                
        if human.isSubdivided():
            human.meshData.setVisibility(1)
            human.getSubdivisionMesh(False).setVisibility(0)

    def onMouseDragged(self, event):
        if not self.modifier:
            log.notice('No modifier available')
            
        human = gui3d.app.selectedHuman

        # check which vector we need to check

        if abs(event.dx) > abs(event.dy):
            d = event.dx
        else:
            d = -event.dy

        if d == 0.0:
            return

        value = d / 20.0

        self.modifier.updateValue(human, self.modifier.getValue(human) + value)
        if self.symmetryModifier:
            self.symmetryModifier.updateValue(human, self.modifier.getValue(human))

    def onMouseUp(self, event):
        human = gui3d.app.selectedHuman

        # Recalculate

        human.applyAllTargets(gui3d.app.progress)
        
        if human.isSubdivided():
            human.meshData.setVisibility(0)
            human.getSubdivisionMesh(False).setVisibility(1)

        # Build undo item

        after = {}

        for target in self.before.iterkeys():
            after[target] = human.getDetail(target)

        gui3d.app.did(humanmodifier.DetailAction(human, self.before, after))

    def onMouseMoved(self, event):
        human = gui3d.app.selectedHuman

        groups = []

        if self.micro:
            groups.append(event.group)
        else:
            part = human.getPartNameForGroupName(event.group.name)
            for g in human.mesh.faceGroups:
                if part in g.name:
                    groups.append(g)
                    if human.symmetryModeEnabled:
                        sg = human.getSymmetryGroup(g)
                        if sg:
                            groups.append(sg)

        for g in self.selectedGroups:
            if g not in groups:
                g.setColor([255, 255, 255, 255])

        for g in groups:
            if g not in self.selectedGroups:
                g.setColor([0, 255, 0, 255])

        self.selectedGroups = groups
        mh.redraw()

    def onMouseExited(self, event):
        for g in self.selectedGroups:
            g.setColor([255, 255, 255, 255])

        self.selectedGroups = []
        mh.redraw()


class Detail3dTool(events3d.EventHandler):

    def __init__(self, app, micro, type):
        gui3d.app = app
        self.micro = micro
        self.type = type
        if type == 'scale':
            self.x = DetailTool(app, micro, '-scale-horiz-decr', '-scale-horiz-incr')
            self.y = DetailTool(app, micro, '-scale-vert-decr', '-scale-vert-incr')
            self.z = DetailTool(app, micro, '-scale-depth-decr', '-scale-depth-incr')
        elif type == 'translation':
            self.x = DetailTool(app, micro, '-trans-in', '-trans-out')
            self.y = DetailTool(app, micro, '-trans-down', '-trans-up')
            self.z = DetailTool(app, micro, '-trans-backward', '-trans-forward')
        self.selectedGroups = []

    def onMouseDown(self, event):
        self.x.onMouseDown(event)
        self.y.onMouseDown(event)
        self.z.onMouseDown(event)

    def getCameraFraming(self):
        """
    This method return a label to identify the main
    camera framing (front, back. side, top) depending
    the camera rotations.
    
    **Parameters:** This method has no parameters.
    """

    # TODO: top and botton view

        rot = gui3d.app.selectedHuman.getRotation()

        xRot = rot[0] % 360
        yRot = rot[1] % 360

        if 315 < yRot <= 360 or 0 <= yRot < 45:
            return 'FRONTAL_VIEW'
        if 145 < yRot < 235:
            return 'BACK_VIEW'
        if 45 < yRot < 145:
            return 'LEFT_VIEW'
        if 235 < yRot < 315:
            return 'RIGHT_VIEW'

    def onMouseDragged(self, event):
        viewType = self.getCameraFraming()

        if viewType == 'FRONTAL_VIEW':
            d = event.dy
            event.dy = 0.0
            self.x.onMouseDragged(event)
            event.dy = d
            d = event.dx
            event.dx = 0.0
            self.y.onMouseDragged(event)
            event.dx = d
        elif viewType == 'BACK_VIEW':
            d = event.dy
            event.dy = 0.0
            event.dx = -event.dx
            self.x.onMouseDragged(event)
            event.dy = d
            d = -event.dx
            event.dx = 0.0
            self.y.onMouseDragged(event)
            event.dx = d
        elif viewType == 'LEFT_VIEW':
            d = event.dy
            event.dy = 0.0
            self.z.onMouseDragged(event)
            event.dy = d
            d = event.dx
            event.dx = 0.0
            self.y.onMouseDragged(event)
            event.dx = d
        elif viewType == 'RIGHT_VIEW':
            d = event.dy
            event.dy = 0.0
            event.dx = -event.dx
            self.z.onMouseDragged(event)
            event.dy = d
            d = -event.dx
            event.dx = 0.0
            self.y.onMouseDragged(event)
            event.dx = d

    def onMouseUp(self, event):
        human = gui3d.app.selectedHuman

    # Recalculate

        human.applyAllTargets(gui3d.app.progress)
        
        if human.isSubdivided():
            human.meshData.setVisibility(0)
            human.getSubdivisionMesh(False).setVisibility(1)

    # Add undo item

        before = {}

        for (target, value) in self.x.before.iteritems():
            before[target] = value
        for (target, value) in self.y.before.iteritems():
            before[target] = value
        for (target, value) in self.z.before.iteritems():
            before[target] = value

        after = {}

        for target in before.iterkeys():
            after[target] = human.getDetail(target)

        gui3d.app.did(humanmodifier.DetailAction(human, before, after))

    def onMouseMoved(self, event):
        human = gui3d.app.selectedHuman

        groups = []

        if self.micro:
            log.debug("%s", event.group)
            groups.append(event.group)
            if human.symmetryModeEnabled:
                sg = human.getSymmetryGroup(event.group)
                if sg:
                    groups.append(sg)
        else:
            part = human.getPartNameForGroupName(event.group.name)
            for g in human.mesh.faceGroups:
                if part in g.name:
                    groups.append(g)
                    if human.symmetryModeEnabled:
                        sg = human.getSymmetryGroup(g)
                        if sg:
                            groups.append(sg)

        for g in self.selectedGroups:
            if g not in groups:
                g.setColor([255, 255, 255, 255])

        for g in groups:
            if g not in self.selectedGroups:
                g.setColor([0, 255, 0, 255])

        self.selectedGroups = groups
        mh.redraw()

    def onMouseExited(self, event):
        for g in self.selectedGroups:
            g.setColor([255, 255, 255, 255])

        self.selectedGroups = []
        mh.redraw()

class DetailModelingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Detail modelling', label='Micro')
        self.tool = None
        
        self.sliders = []

        self.modifiersBox = self.addLeftWidget(gui.GroupBox('Modifiers'))

        self.detailButtonGroup = []

        self.tool = Detail3dTool(gui3d.app, True, 'translation')

        self.translationButton = self.modifiersBox.addWidget(gui.RadioButton(self.detailButtonGroup, 'Move', True))
        self.scaleButton = self.modifiersBox.addWidget(gui.RadioButton(self.detailButtonGroup, label='Scale'))

        @self.translationButton.mhEvent
        def onClicked(event):
            self.tool = Detail3dTool(gui3d.app, True, 'translation')
            gui3d.app.tool = self.tool

        @self.scaleButton.mhEvent
        def onClicked(event):
            self.tool = Detail3dTool(gui3d.app, True, 'scale')
            gui3d.app.tool = self.tool

        #self.microButton = self.modifiersBox.addWidget(gui.ToggleButton('Micro'))

        """    
        @self.microButton.mhEvent
        def onClicked(event):
            self.tool = Detail3dTool(gui3d.app, self.microButton.selected, self.tool.type)
            gui3d.app.tool = self.tool
        """
    def onShow(self, event):
        gui3d.app.tool = self.tool
        self.translationButton.setFocus()
        gui3d.TaskView.onShow(self, event)

    def onHide(self, event):
        gui3d.app.tool = None
        gui3d.TaskView.onHide(self, event)

    def syncSliders(self):

        for slider in self.sliders:
            slider.update()
        
    def onHumanChanged(self, event):
        
        human = event.human
            
        if self.isVisible():
            self.syncSliders()
        
    def loadHandler(self, human, values):
        
        if values[0] == 'detail':
            human.setDetail('data/targets/details/' + values[1] + '.target', float(values[2]))
        elif values[0] == 'microdetail':
            human.setDetail('data/targets/microdetails/' + values[1] + '.target', float(values[2]))
       
    def saveHandler(self, human, file):
        
        for t in human.targetsDetailStack.keys():
            if '/details' in t and ('trans' in t or 'scale' in t):
                file.write('detail %s %f\n' % (os.path.basename(t).replace('.target', ''), human.targetsDetailStack[t]))
            elif '/microdetails' in t:
                file.write('microdetail %s %f\n' % (os.path.basename(t).replace('.target', ''), human.targetsDetailStack[t]))

def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addTask(DetailModelingTaskView(category))

    app.addLoadHandler('detail', taskview.loadHandler)
    app.addLoadHandler('microdetail', taskview.loadHandler)

    app.addSaveHandler(taskview.saveHandler)

def unload(app):
    pass
