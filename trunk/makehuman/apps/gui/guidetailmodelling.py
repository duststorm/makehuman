#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TODO
"""

__docformat__ = 'restructuredtext'

import events3d
import gui3d
import algos3d
import humanmodifier


class DetailAction:

    def __init__(self, human, method, value, postAction):
        self.name = method
        self.human = human
        self.method = method
        self.before = getattr(self.human, 'get' + self.method)()
        self.after = value
        self.postAction = postAction

    def do(self):
        getattr(self.human, 'set' + self.method)(self.after)
        self.human.applyAllTargets(self.human.app.progress)
        self.postAction()
        return True

    def undo(self):
        getattr(self.human, 'set' + self.method)(self.before)
        self.human.applyAllTargets(self.human.app.progress)
        self.postAction()
        return True


class DetailTool(events3d.EventHandler):

    def __init__(self, app, micro, left, right):
        self.app = app
        self.micro = micro
        self.left = left
        self.before = None
        self.right = right
        self.modifier = None
        self.symmetryModifier = None
        self.selectedGroups = []

    def onMouseDown(self, event):
        human = self.app.selectedHuman

    # Find the target name

        if self.micro:
            folder = 'data/targets/microdetails/'
            part = self.app.selectedGroup.name
        else:
            folder = 'data/targets/details/'
            part = human.getPartNameForGroupName(self.app.selectedGroup.name)

    # Find the targets

        leftTarget = '%s%s%s.target' % (folder, part, self.left)
        rightTarget = '%s%s%s.target' % (folder, part, self.right)

        self.modifier = None
        if not (leftTarget and rightTarget):
            print 'No targets available'
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

    def onMouseDragged(self, event):
        if not self.modifier:
            print 'No modifier available'
            
        human = self.app.selectedHuman

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
        human = self.app.selectedHuman

    # Recalculate

        human.applyAllTargets(self.app.progress)

    # Build undo item

        after = {}

        for target in self.before.iterkeys():
            after[target] = human.getDetail(target)

        self.app.did(humanmodifier.Action(human, self.before, after))

    def onMouseMoved(self, event):
        human = self.app.selectedHuman

        groups = []

        if self.micro:
            groups.append(event.group)
        else:
            part = human.getPartNameForGroupName(event.group.name)
            for g in human.mesh.facesGroups:
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
        self.app.redraw()

    def onMouseExited(self, event):
        for g in self.selectedGroups:
            g.setColor([255, 255, 255, 255])

        self.selectedGroups = []
        self.app.redraw()


class Detail3dTool(events3d.EventHandler):

    def __init__(self, app, micro, type):
        self.app = app
        self.micro = micro
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

        rot = self.app.selectedHuman.getRotation()

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
        human = self.app.selectedHuman

    # Recalculate

        human.applyAllTargets(self.app.progress)

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

        self.app.did(humanmodifier.Action(human, before, after))

    def onMouseMoved(self, event):
        human = self.app.selectedHuman

        groups = []

        if self.micro:
            print(event.group)
            groups.append(event.group)
            if human.symmetryModeEnabled:
                sg = human.getSymmetryGroup(event.group)
                if sg:
                    groups.append(sg)
        else:
            part = human.getPartNameForGroupName(event.group.name)
            for g in human.mesh.facesGroups:
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
        self.app.redraw()

    def onMouseExited(self, event):
        for g in self.selectedGroups:
            g.setColor([255, 255, 255, 255])

        self.selectedGroups = []
        self.app.redraw()


class DetailModelingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Detail modelling', label='Details')
        self.tool = None

        # details tool panel background
        
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Gender', gui3d.GroupBoxStyle._replace(height=25+36*3+6));y+=25
        
        self.genitalsSlider = gui3d.Slider(self, position=[10, y, 9.3], value=0.0, min=-1.0, max=1.0, label="Genitalia");y+=36
        self.breastSizeSlider = gui3d.Slider(self, position=[10, y, 9.2], value=0.5, min=0.0, max=1.0,label = "Breast");y+=36
        self.breastFirmnessSlider = gui3d.Slider(self, position=[10, y, 9.2], value=0.5, min=0.0, max=1.0, label ="Breast firmness");y+=36
        y+=16
        
        self.genitals = None
        
        @self.genitalsSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.genitals == None:
                    self.genitals = human.getGenitals()
                human.updateGenitals(self.genitals, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.genitals = min(max(value, -1.0), 1.0)
            
        @self.genitalsSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'Genitals', value, self.syncSliders))
            self.genitals = None

        self.breastSize = None
        
        @self.breastSizeSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.breastSize == None:
                    self.breastSize = human.getBreastSize()
                human.updateBreastSize(self.breastSize, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.breastSize = min(1.0, max(0.0, value))
            
        @self.breastSizeSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'BreastSize', value, self.syncSliders))
            self.breastSize = None

        self.breastFirmness = None
        
        @self.breastFirmnessSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.breastFirmness == None:
                    self.breastFirmness = human.getBreastFirmness()
                human.updateBreastFirmness(self.breastFirmness, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.breastFirmness = min(1.0, max(0.0, value))
        
        @self.breastFirmnessSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'BreastFirmness', value, self.syncSliders))
            self.breastFirmness = None
            
        gui3d.GroupBox(self, [10, y, 9.0], 'Face', gui3d.GroupBoxStyle._replace(height=25+36*5+6));y+=25

        self.noseSlider = gui3d.Slider(self, position=[10, y, 9.2], value=0.0, min=0.0, max=1.0, label = "Nose shape");y+=36
        self.mouthSlider = gui3d.Slider(self, position=[10, y, 9.2], value=0.0, min=0.0, max=1.0, label = "Mouth shape");y+=36
        self.eyesSlider = gui3d.Slider(self, position=[10, y, 9.2], value=0.0, min=0.0, max=1.0, label = "Eyes shape");y+=36
        self.earsSlider = gui3d.Slider(self, position=[10, y, 9.2], value=0.0, min=0.0, max=1.0, label = "Ears shape");y+=36
        self.jawSlider = gui3d.Slider(self, position=[10, y, 9.2], value=0.0, min=0.0, max=1.0, label = "Jaw shape");y+=36
        y+=16

        self.nose = None
        
        @self.noseSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.nose == None:
                    self.nose = human.getNose()
                human.updateNose(self.nose, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.nose = min(1.0, max(0.0, value))
        
        @self.noseSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'Nose', value, self.syncSliders))
            self.nose = None
            
        self.mouth = None
        
        @self.mouthSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.mouth == None:
                    self.mouth = human.getMouth()
                human.updateMouth(self.mouth, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.mouth = min(1.0, max(0.0, value))
        
        @self.mouthSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'Mouth', value, self.syncSliders))
            self.mouth = None
            
        self.eyes = None
        
        @self.eyesSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.eyes == None:
                    self.eyes = human.getEyes()
                human.updateEyes(self.eyes, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.eyes = min(1.0, max(0.0, value))
        
        @self.eyesSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'Eyes', value, self.syncSliders))
            self.eyes = None

        self.ears = None
        
        @self.earsSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.ears == None:
                    self.ears = human.getEars()
                human.updateEars(self.ears, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.ears = min(1.0, max(0.0, value))
        
        @self.earsSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'Ears', value, self.syncSliders))
            self.ears = None  
        
        self.jaw = None
        
        @self.jawSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.jaw == None:
                    self.jaw = human.getJaw()
                human.updateJaw(self.jaw, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.jaw = min(1.0, max(0.0, value))
        
        @self.jawSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'Jaw', value, self.syncSliders))
            self.jaw = None
            
        y = 80
        self.headBox = gui3d.GroupBox(self, [650, y, 9.0], 'Head', gui3d.GroupBoxStyle._replace(height=25+36*3+6));y+=25
        
        self.headShapeSlider = gui3d.Slider(self.headBox, position=[650, y, 9.2], value=0.0,min=0.0,max=1.0,label="Shape");y+=36
        self.headAgeSlider = gui3d.Slider(self.headBox, position=[650, y, 9.2], value=0.0,min=-1.0,max=1.0,label="Age");y+=36
        self.faceAngleSlider = gui3d.Slider(self.headBox, position=[650, y, 9.2], value=0.0,min=-1.0,max=1.0,label="Face angle");y+=36
        y+=16
        
        self.head = None

        @self.headShapeSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.head == None:
                    self.head = human.getHead()
                human.updateHead(self.head, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.head = min(1.0, max(0.0, value))

        @self.headShapeSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'Head', value, self.syncSliders))
            self.head = None
            
        self.headAge = None

        @self.headAgeSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.headAge == None:
                    self.headAge = human.getHeadAge()
                human.updateHeadAge(self.headAge, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.headAge = min(1.0, max(-1.0, value))

        @self.headAgeSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'HeadAge', value, self.syncSliders))
            self.headAge = None
               
        self.faceAngle = None

        @self.faceAngleSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.faceAngle == None:
                    self.faceAngle = human.getFaceAngle()
                human.updateFaceAngle(self.faceAngle, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.faceAngle = min(1.0, max(-1.0, value))

        @self.faceAngleSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'FaceAngle', value, self.syncSliders))
            self.faceAngle = None
            
        self.pelvisBox = gui3d.GroupBox(self, [650, y, 9.0], 'Pelvis', gui3d.GroupBoxStyle._replace(height=25+36*3+6));y+=25
        
        self.pelvisToneSlider = gui3d.Slider(self.pelvisBox, position=[650, y, 9.2], value=0.0, min=-1.0, max=1.0, label = "Pelvis tone");y+=36
        self.stomachSlider = gui3d.Slider(self.pelvisBox, position=[650, y, 9.2], value=0.0, min=-1.0, max=1.0, label ="Stomach");y+=36
        self.buttocksSlider = gui3d.Slider(self.pelvisBox, position=[650, y, 9.2], value=0.0, min=-1.0, max=1.0, label = "Buttocks");y+=36
        y+=16
        
        self.pelvisTone = None
        
        @self.pelvisToneSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.pelvisTone == None:
                    self.pelvisTone = human.getPelvisTone()
                human.updatePelvisTone(self.pelvisTone, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.pelvisTone = min(1.0, max(-1.0, value))
                
        @self.pelvisToneSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'PelvisTone', value, self.syncSliders))
            self.pelvisTone = None
            
        self.stomach = None
        
        @self.stomachSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.stomach == None:
                    self.stomach = human.getStomach()
                human.updateStomach(self.stomach, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.stomach = min(1.0, max(-1.0, value))
        
        @self.stomachSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'Stomach', value, self.syncSliders))
            self.stomach = None
            
        self.buttocks = None
        
        @self.buttocksSlider.event
        def onChanging(value):
            if self.app.settings.get('realtimeUpdates', True):
                human = self.app.selectedHuman
                if self.buttocks == None:
                    self.buttocks = human.getButtocks()
                human.updateButtocks(self.buttocks, value, self.app.settings.get('realtimeNormalUpdates', True))
                self.buttocks = min(1.0, max(-1.0, value))
                
        @self.buttocksSlider.event
        def onChange(value):
            human = self.app.selectedHuman
            self.app.do(DetailAction(human, 'Buttocks', value, self.syncSliders))
            self.buttocks = None
            
        self.modifiersBox = gui3d.GroupBox(self, [650, y, 9.0], 'Modifiers', gui3d.GroupBoxStyle._replace(height=25+24*3+6));y+=25
        
        modifierStyle = gui3d.ButtonStyle._replace(width=(112-4)/2, height=20)

        self.detailButtonGroup = []

        self.tool = Detail3dTool(self.app, False, 'translation')

        self.translationButton = gui3d.RadioButton(self.modifiersBox, self.detailButtonGroup, [658, y, 9.2], 'Move', True, modifierStyle)
        self.scaleButton = gui3d.RadioButton(self.modifiersBox, self.detailButtonGroup, [658+modifierStyle.width+4, y, 9.2], label='Scale', style=modifierStyle);y+=24

        @self.translationButton.event
        def onClicked(event):
            self.tool = Detail3dTool(self.app, False, 'translation')
            self.app.tool = self.tool
            gui3d.RadioButton.onClicked(self.translationButton, event)

        @self.scaleButton.event
        def onClicked(event):
            self.tool = Detail3dTool(self.app, False, 'scale')
            self.app.tool = self.tool
            gui3d.RadioButton.onClicked(self.scaleButton, event)

        self.rightSymmetryButton = gui3d.Button(self.modifiersBox, [658, y, 9.2], 'Sym<', style=modifierStyle)
        self.leftSymmetryButton = gui3d.Button(self.modifiersBox, [658+modifierStyle.width+4, y, 9.2], 'Sym>', style=modifierStyle);y+=24
        self.symmetryButton = gui3d.ToggleButton(self.modifiersBox, [658, y, 9.2], 'Sym', style=modifierStyle)

        @self.rightSymmetryButton.event
        def onClicked(event):
            human = self.app.selectedHuman
            human.applySymmetryRight()

        @self.leftSymmetryButton.event
        def onClicked(event):
            human = self.app.selectedHuman
            human.applySymmetryLeft()

        @self.symmetryButton.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.symmetryButton, event)
            human = self.app.selectedHuman
            human.symmetryModeEnabled = self.symmetryButton.selected
            self.parent.tasksByName['Micro modelling'].symmetryButton.setSelected(self.symmetryButton.selected)

    def onShow(self, event):
        self.app.tool = self.tool
        self.genitalsSlider.setFocus()
        self.syncSliders()
        gui3d.TaskView.onShow(self, event)

    def onHide(self, event):
        self.app.tool = None
        gui3d.TaskView.onHide(self, event)
        
    def onResized(self, event):
        self.headBox.setPosition([event[0] - 150, self.headBox.getPosition()[1], 9.0])
        self.pelvisBox.setPosition([event[0] - 150, self.pelvisBox.getPosition()[1], 9.0])
        self.modifiersBox.setPosition([event[0] - 150, self.modifiersBox.getPosition()[1], 9.0])

    def syncSliders(self):
        human = self.app.selectedHuman
        self.genitalsSlider.setValue(human.getGenitals())
        self.breastSizeSlider.setValue(human.getBreastSize())
        self.breastFirmnessSlider.setValue(human.getBreastFirmness())
        self.stomachSlider.setValue(human.getStomach())
        self.noseSlider.setValue(human.getNose())
        self.mouthSlider.setValue(human.getMouth())
        self.eyesSlider.setValue(human.getEyes())
        self.earsSlider.setValue(human.getEars())
        self.headShapeSlider.setValue(human.getHead())
        self.headAgeSlider.setValue(human.getHeadAge())
        self.faceAngleSlider.setValue(human.getFaceAngle())
        self.jawSlider.setValue(human.getJaw())
        self.pelvisToneSlider.setValue(human.getPelvisTone())
        self.buttocksSlider.setValue(human.getButtocks())

class MicroModelingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Micro modelling', label='Micro')
        self.tool = None
        
        y=80
        gui3d.GroupBox(self, [10, y, 9.0], 'Modifiers', gui3d.GroupBoxStyle._replace(height=25+24*3+6));y+=25
        
        modifierStyle = gui3d.ButtonStyle._replace(width=(112-4)/2, height=20)

        self.microButtonGroup = []

        self.translationButton = gui3d.RadioButton(self, self.microButtonGroup, [18, y, 9.2], 'Move', True, style=modifierStyle)
        self.scaleButton = gui3d.RadioButton(self, self.microButtonGroup, [18+modifierStyle.width+4, y, 9.2], label='Scale', style=modifierStyle);y+=24

        self.tool = Detail3dTool(self.app, True, 'translation')

        @self.translationButton.event
        def onClicked(event):
            self.tool = Detail3dTool(self.app, True, 'translation')
            self.app.tool = self.tool
            gui3d.RadioButton.onClicked(self.translationButton, event)

        @self.scaleButton.event
        def onClicked(event):
            self.tool = Detail3dTool(self.app, True, 'scale')
            self.app.tool = self.tool
            gui3d.RadioButton.onClicked(self.scaleButton, event)
            
        self.rightSymmetryButton = gui3d.Button(self, [18, y, 9.2], 'Sym<', style=modifierStyle)
        self.leftSymmetryButton = gui3d.Button(self, [18+modifierStyle.width+4, y, 9.2], 'Sym>', style=modifierStyle);y+=24
        self.symmetryButton = gui3d.ToggleButton(self, [18, y, 9.2], 'Sym', style=modifierStyle)
        
        @self.rightSymmetryButton.event
        def onClicked(event):
            human = self.app.selectedHuman
            human.applySymmetryRight()

        @self.leftSymmetryButton.event
        def onClicked(event):
            human = self.app.selectedHuman
            human.applySymmetryLeft()

        @self.symmetryButton.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.symmetryButton, event)
            human = self.app.selectedHuman
            human.symmetryModeEnabled = self.symmetryButton.selected
            self.parent.tasksByName['Detail modelling'].symmetryButton.setSelected(self.symmetryButton.selected)

    def onShow(self, event):
        self.app.tool = self.tool
        self.translationButton.setFocus()
        gui3d.TaskView.onShow(self, event)

    def onHide(self, event):
        self.app.tool = None
        gui3d.TaskView.onHide(self, event)


