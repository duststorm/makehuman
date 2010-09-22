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
        human = self.app.scene3d.selectedHuman

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

        self.modifier = humanmodifier.Modifier(human, leftTarget, rightTarget)

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
                self.symmetryModifier = humanmodifier.Modifier(human, leftSymmetryTarget, rightSymmetryTarget)

        # Save the state

                self.before[leftSymmetryTarget] = human.getDetail(leftSymmetryTarget)
                self.before[rightSymmetryTarget] = human.getDetail(rightSymmetryTarget)

    def onMouseDragged(self, event):
        if not self.modifier:
            print 'No modifier available'

    # check which vector we need to check

        if abs(event.dx) > abs(event.dy):
            d = event.dx
        else:
            d = -event.dy

        if d == 0.0:
            return

        value = d / 20.0

        self.modifier.setValue(self.modifier.getValue() + value)
        if self.symmetryModifier:
            self.symmetryModifier.setValue(self.modifier.getValue())

    def onMouseUp(self, event):
        human = self.app.scene3d.selectedHuman

    # Recalculate

        human.applyAllTargets(self.app.progress)

    # Build undo item

        after = {}

        for target in self.before.iterkeys():
            after[target] = human.getDetail(target)

        self.app.did(humanmodifier.Action(human, self.before, after))

    def onMouseMoved(self, event):
        human = self.app.scene3d.selectedHuman

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
        self.app.scene3d.redraw()

    def onMouseExited(self, event):
        for g in self.selectedGroups:
            g.setColor([255, 255, 255, 255])

        self.selectedGroups = []
        self.app.scene3d.redraw()


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

        rot = self.app.scene3d.selectedHuman.getRotation()

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
        human = self.app.scene3d.selectedHuman

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
        human = self.app.scene3d.selectedHuman

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
        self.app.scene3d.redraw()

    def onMouseExited(self, event):
        for g in self.selectedGroups:
            g.setColor([255, 255, 255, 255])

        self.selectedGroups = []
        self.app.scene3d.redraw()


class DetailModelingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Detail modelling', category.app.getThemeResource('images', 'details.png'), category.app.getThemeResource('images',
                                'details_on.png'))
        self.tool = None

        # details tool panel background

        gui3d.Object(self, 'data/3dobjs/unit_square.obj', self.app.getThemeResource('images', 'group_details_gender.png'), [10, 80, 9.0],128,128)
        gui3d.Object(self, 'data/3dobjs/unit_square.obj', self.app.getThemeResource('images', 'group_details_face.png'), [10, 211, 9.0],128,256)
        gui3d.Object(self, 'data/3dobjs/unit_square.obj', self.app.getThemeResource('images','group_details_pelvis.png'),[650, 211, 9.0],128,128)
        gui3d.Object(self, 'data/3dobjs/unit_square.obj', self.app.getThemeResource('images', 'group_details_head.png'), [650, 80, 9.0],128,128)
        gui3d.Object(self, 'data/3dobjs/unit_square.obj', self.app.getThemeResource('images', 'group_details_modifiers.png'), [650, 342, 9.0],128,128)

        self.genitalsSlider = gui3d.Slider(self, position=[10, 105, 9.3], value=0.0, min=-1.0, max=1.0, label="Genitalia")

        self.genitals = None
        
        @self.genitalsSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.genitals == None:
                    self.genitals = human.getGenitals()
                human.updateGenitals(self.genitals, value, self.app.settings.realtimeNormalUpdates)
                self.genitals = min(max(value, -1.0), 1.0)
            
        @self.genitalsSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'Genitals', value, self.syncSliders))
            self.genitals = None

        self.breastSizeSlider = gui3d.Slider(self, position=[10, 139, 9.2], value=0.5, min=0.0, max=1.0,label = "Breast")

        self.breastSize = None
        
        @self.breastSizeSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.breastSize == None:
                    self.breastSize = human.getBreastSize()
                human.updateBreastSize(self.breastSize, value, self.app.settings.realtimeNormalUpdates)
                self.breastSize = min(1.0, max(0.0, value))
            
        @self.breastSizeSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'BreastSize', value, self.syncSliders))
            self.breastSize = None

        self.breastFirmnessSlider = gui3d.Slider(self, position=[10, 173, 9.2], value=0.5, min=0.0, max=1.0, label ="Breast firmness")
        
        self.breastFirmness = None
        
        @self.breastFirmnessSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.breastFirmness == None:
                    self.breastFirmness = human.getBreastFirmness()
                human.updateBreastFirmness(self.breastFirmness, value, self.app.settings.realtimeNormalUpdates)
                self.breastFirmness = min(1.0, max(0.0, value))
        
        @self.breastFirmnessSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'BreastFirmness', value, self.syncSliders))
            self.breastFirmness = None
            
        self.stomachSlider = gui3d.Slider(self, position=[650, 269, 9.2], value=0.0, min=-1.0, max=1.0, label ="Stomach")
        
        self.stomach = None
        
        @self.stomachSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.stomach == None:
                    self.stomach = human.getStomach()
                human.updateStomach(self.stomach, value, self.app.settings.realtimeNormalUpdates)
                self.stomach = min(1.0, max(-1.0, value))
        
        @self.stomachSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'Stomach', value, self.syncSliders))
            self.stomach = None

        self.noseSlider = gui3d.Slider(self, position=[10, 235, 9.2], value=0.0, min=0.0, max=1.0, label = "Nose shape")

        self.nose = None
        
        @self.noseSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.nose == None:
                    self.nose = human.getNose()
                human.updateNose(self.nose, value, self.app.settings.realtimeNormalUpdates)
                self.nose = min(1.0, max(0.0, value))
        
        @self.noseSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'Nose', value, self.syncSliders))
            self.nose = None
            
        self.mouthSlider = gui3d.Slider(self, position=[10, 269, 9.2], value=0.0, min=0.0, max=1.0, label = "Mouth shape")

        self.mouth = None
        
        @self.mouthSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.mouth == None:
                    self.mouth = human.getMouth()
                human.updateMouth(self.mouth, value, self.app.settings.realtimeNormalUpdates)
                self.mouth = min(1.0, max(0.0, value))
        
        @self.mouthSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'Mouth', value, self.syncSliders))
            self.mouth = None
            
        self.eyesSlider = gui3d.Slider(self, position=[10, 303, 9.2], value=0.0, min=0.0, max=1.0, label = "Eyes shape")

        self.eyes = None
        
        @self.eyesSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.eyes == None:
                    self.eyes = human.getEyes()
                human.updateEyes(self.eyes, value, self.app.settings.realtimeNormalUpdates)
                self.eyes = min(1.0, max(0.0, value))
        
        @self.eyesSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'Eyes', value, self.syncSliders))
            self.eyes = None

        self.earsSlider = gui3d.Slider(self, position=[10, 337, 9.2], value=0.0, min=0.0, max=1.0, label = "Ears shape")

        self.ears = None
        
        @self.earsSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.ears == None:
                    self.ears = human.getEars()
                human.updateEars(self.ears, value, self.app.settings.realtimeNormalUpdates)
                self.ears = min(1.0, max(0.0, value))
        
        @self.earsSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'Ears', value, self.syncSliders))
            self.ears = None

        self.headShapeSlider = gui3d.Slider(self, position=[650, 106, 9.2], value=0.0,min=0.0,max=1.0,label="Shape")

        self.head = None

        @self.headShapeSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.head == None:
                    self.head = human.getHead()
                human.updateHead(self.head, value, self.app.settings.realtimeNormalUpdates)
                self.head = min(1.0, max(0.0, value))

        @self.headShapeSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'Head', value, self.syncSliders))
            self.head = None
            
        self.headAgeSlider = gui3d.Slider(self, position=[650, 140, 9.2], value=0.0,min=-1.0,max=1.0,label="Age")
            
        self.headAge = None

        @self.headAgeSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.headAge == None:
                    self.headAge = human.getHeadAge()
                human.updateHeadAge(self.headAge, value, self.app.settings.realtimeNormalUpdates)
                self.headAge = min(1.0, max(-1.0, value))

        @self.headAgeSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'HeadAge', value, self.syncSliders))
            self.headAge = None
            
        self.faceAngleSlider = gui3d.Slider(self, position=[650, 174, 9.2], value=0.0,min=-1.0,max=1.0,label="Face angle")
            
        self.faceAngle = None

        @self.faceAngleSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.faceAngle == None:
                    self.faceAngle = human.getFaceAngle()
                human.updateFaceAngle(self.faceAngle, value, self.app.settings.realtimeNormalUpdates)
                self.faceAngle = min(1.0, max(-1.0, value))

        @self.faceAngleSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'FaceAngle', value, self.syncSliders))
            self.faceAngle = None
            
        self.jawSlider = gui3d.Slider(self, position=[10, 374, 9.2], value=0.0, min=0.0, max=1.0, label = "Jaw shape")

        self.jaw = None
        
        @self.jawSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.jaw == None:
                    self.jaw = human.getJaw()
                human.updateJaw(self.jaw, value, self.app.settings.realtimeNormalUpdates)
                self.jaw = min(1.0, max(0.0, value))
        
        @self.jawSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'Jaw', value, self.syncSliders))
            self.jaw = None
            
        self.pelvisToneSlider = gui3d.Slider(self, position=[650, 235, 9.2], value=0.0, min=-1.0, max=1.0, label = "Pelvis tone")

        self.pelvisTone = None
        
        @self.pelvisToneSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.pelvisTone == None:
                    self.pelvisTone = human.getPelvisTone()
                human.updatePelvisTone(self.pelvisTone, value, self.app.settings.realtimeNormalUpdates)
                self.pelvisTone = min(1.0, max(-1.0, value))
                
        @self.pelvisToneSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'PelvisTone', value, self.syncSliders))
            self.pelvisTone = None
            
        self.buttocksSlider = gui3d.Slider(self, position=[650, 303, 9.2], value=0.0, min=-1.0, max=1.0, label = "Buttocks")

        self.buttocks = None
        
        @self.buttocksSlider.event
        def onChanging(value):
            if self.app.settings.realtimeUpdates:
                human = self.app.scene3d.selectedHuman
                if self.buttocks == None:
                    self.buttocks = human.getButtocks()
                human.updateButtocks(self.buttocks, value, self.app.settings.realtimeNormalUpdates)
                self.buttocks = min(1.0, max(-1.0, value))
                
        @self.buttocksSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            self.app.do(DetailAction(human, 'Buttocks', value, self.syncSliders))
            self.buttocks = None

        self.detailButtonGroup = []
        
        '''
        self.muscleDetailButton = gui3d.RadioButton(self, self.detailButtonGroup, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images',
                                                    'button_muscle.png'), selectedTexture=self.app.getThemeResource('images', 'button_muscle_on.png'), position=[673,
                                                    373, 9.2], selected=True)
        self.weightDetailButton = gui3d.RadioButton(self, self.detailButtonGroup, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images',
                                                    'button_weight.png'), selectedTexture=self.app.getThemeResource('images', 'button_weight_on.png'), position=[708,
                                                    373, 9.2])
        '''

        self.tool = Detail3dTool(self.app, False, 'translation')
        
        '''
        @self.muscleDetailButton.event
        def onClicked(event):
            self.tool = DetailTool(self.app, False, '_flaccid', '_muscle')
            self.app.tool = self.tool
            gui3d.RadioButton.onClicked(self.muscleDetailButton, event)

        @self.weightDetailButton.event
        def onClicked(event):
            self.tool = DetailTool(self.app, False, '_underweight', '_overweight')
            self.app.tool = self.tool
            gui3d.RadioButton.onClicked(self.weightDetailButton, event)
        '''

        self.translationButton = gui3d.RadioButton(self, self.detailButtonGroup, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images',
                                                   'button_translation.png'), selectedTexture=self.app.getThemeResource('images', 'button_translation_on.png'),
                                                   position=[673, 393, 9.2], selected=True)
        self.scaleButton = gui3d.RadioButton(self, self.detailButtonGroup, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images',
                                             'button_scale.png'), selectedTexture=self.app.getThemeResource('images', 'button_scale_on.png'), position=[708, 393, 9.2])

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

        self.rightSymmetryButton = gui3d.Button(self, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images', 'button_symmright.png'),
                                                selectedTexture=self.app.getThemeResource('images', 'button_symmright_on.png'),position=[673, 410, 9.2])
        self.leftSymmetryButton = gui3d.Button(self, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images', 'button_symmleft.png'),
                                               selectedTexture=self.app.getThemeResource('images', 'button_symmleft_on.png'),position=[708, 410, 9.2])
        self.symmetryButton = gui3d.ToggleButton(self, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images', 'button_symmetry.png'),
                                                 selectedTexture=self.app.getThemeResource('images', 'button_symmetry_on.png'), position=[743, 410, 9.2])

        @self.rightSymmetryButton.event
        def onClicked(event):
            human = self.app.scene3d.selectedHuman
            human.applySymmetryRight()

        @self.leftSymmetryButton.event
        def onClicked(event):
            human = self.app.scene3d.selectedHuman
            human.applySymmetryLeft()

        @self.symmetryButton.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.symmetryButton, event)
            human = self.app.scene3d.selectedHuman
            human.symmetryModeEnabled = self.symmetryButton.selected
            self.parent.tasksByName['Micro modelling'].symmetryButton.setSelected(self.symmetryButton.selected)

    def onShow(self, event):
        self.app.tool = self.tool
        gui3d.TaskView.onShow(self, event)

    def onHide(self, event):
        self.app.tool = None
        gui3d.TaskView.onHide(self, event)

    def syncSliders(self):
        human = self.app.scene3d.selectedHuman
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
        gui3d.TaskView.__init__(self, category, 'Micro modelling', category.app.getThemeResource('images', 'micro.png'), category.app.getThemeResource('images',
                                'micro_on.png'))
        self.tool = None
        

        gui3d.Object(self, 'data/3dobjs/unit_square.obj', self.app.getThemeResource('images', 'group_details_modifiers.png'), [10, 339, 9.0],128,128)

        self.microButtonGroup = []

        self.translationButton = gui3d.RadioButton(self, self.microButtonGroup, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images',
                                                   'button_translation.png'), selectedTexture=self.app.getThemeResource('images', 'button_translation_on.png'),
                                                   position=[33, 370, 9.2])
        self.scaleButton = gui3d.RadioButton(self, self.microButtonGroup, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images',
                                             'button_scale.png'), selectedTexture=self.app.getThemeResource('images', 'button_scale_on.png'), position=[68, 370, 9.2])

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

        self.rightSymmetryButton = gui3d.Button(self, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images', 'button_symmright.png'),
                                                selectedTexture=self.app.getThemeResource('images', 'button_symmright_on.png'), position=[33, 390, 9.2])
        self.leftSymmetryButton = gui3d.Button(self, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images', 'button_symmleft.png'),
                                                selectedTexture=self.app.getThemeResource('images', 'button_symmleft_on.png'), position=[68, 390, 9.2])
        self.symmetryButton = gui3d.ToggleButton(self, mesh='data/3dobjs/button_standard.obj', texture=self.app.getThemeResource('images', 'button_symmetry.png'),
                                                 selectedTexture=self.app.getThemeResource('images', 'button_symmetry_on.png'), position=[103, 390, 9.2])

        @self.rightSymmetryButton.event
        def onClicked(event):
            human = self.app.scene3d.selectedHuman
            human.applySymmetryRight()

        @self.leftSymmetryButton.event
        def onClicked(event):
            human = self.app.scene3d.selectedHuman
            human.applySymmetryLeft()

        @self.symmetryButton.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.symmetryButton, event)
            human = self.app.scene3d.selectedHuman
            human.symmetryModeEnabled = self.symmetryButton.selected
            self.parent.tasksByName['Detail modelling'].symmetryButton.setSelected(self.symmetryButton.selected)

    def onShow(self, event):
        self.app.tool = self.tool
        gui3d.TaskView.onShow(self, event)

    def onHide(self, event):
        self.app.tool = None
        gui3d.TaskView.onHide(self, event)


