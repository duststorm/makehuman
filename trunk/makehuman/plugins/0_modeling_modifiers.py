#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Generic modifiers
TODO
"""

import mh
import gui
import gui3d
import humanmodifier
import log
import targets

class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, task, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        self.task = task

    def onClicked(self, event):
        self.task.groupBox.showWidget(self.groupBox)

class ModifierTaskView(gui3d.TaskView):
    _group = None
    _label = None

    def __init__(self, category):
        super(ModifierTaskView, self).__init__(category, self._name, label=self._label)

        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []
        self.modifiers = {}

        self.categoryBox = self.addRightWidget(gui.GroupBox('Category'))
        self.groupBox = self.addLeftWidget(gui.StackedBox())

        for name, base, templates in self._features:
            title = name.capitalize()

            # Create box
            box = self.groupBox.addWidget(gui.GroupBox(title))
            self.groupBoxes.append(box)

            # Create radiobutton
            radio = self.categoryBox.addWidget(GroupBoxRadioButton(self, self.radioButtons, title, box, selected = len(self.radioButtons) == 0))

            # Create sliders
            for index, template in enumerate(templates):
                macro = len(template) >= 6
                if macro:
                    tlabel, tname, tvar, tmin, tmax, tview = template
                    modifier = humanmodifier.MacroModifier(base, tname, tvar, tmin, tmax)
                    self.modifiers[tlabel] = modifier
                    slider = humanmodifier.GenericSlider(tmin, tmax, modifier, tlabel, None, tview)
                else:
                    paired = len(template) == 5
                    if paired:
                        tlabel, tname, tleft, tright, tview = template
                        left  = '-'.join([base, tname, tleft])
                        right = '-'.join([base, tname, tright])
                    else:
                        tlabel, tname, tview = template
                        left = None
                        right = '-'.join([base, tname])

                    if tlabel is None:
                        tlabel = tname.split('-')
                        if len(tlabel) > 1 and tlabel[0] == base:
                            tlabel = tlabel[1:]
                        tlabel = ' '.join([word.capitalize() for word in tlabel])

                    modifier = humanmodifier.UniversalModifier(left, right)

                    tpath = '-'.join(template[1:-1])
                    modifierName = tpath
                    clashIndex = 0
                    while modifierName in self.modifiers:
                        log.debug('modifier clash: %s', modifierName)
                        modifierName = '%s%d' % (tpath, clashIndex)
                        clashIndex += 1

                    self.modifiers[modifierName] = modifier
                    slider = humanmodifier.UniversalSlider(modifier, tlabel, '%s.png' % tpath, tview)

                box.addWidget(slider)
                self.sliders.append(slider)

        self.updateMacro()

        self.groupBox.showWidget(self.groupBoxes[0])

    def getModifiers(self):
        return self.modifiers

    def getSymmetricModifierPairNames(self):
        return [dict(left = name, right = "l-" + name[2:])
                for name in self.modifiers
                if name.startswith("r-")]

    def getSingularModifierNames(self):
        return [name
                for name in self.modifiers
                if name[:2] not in ("r-", "l-")]

    def updateMacro(self):
        human = gui3d.app.selectedHuman
        for modifier in self.modifiers.itervalues():
            if isinstance(modifier, humanmodifier.MacroModifier):
                modifier.setValue(human, modifier.getValue(human))

    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)

        if gui3d.app.settings.get('cameraAutoZoom', True):
            self.setCamera()

        for slider in self.sliders:
            slider.update()

    def onHumanChanged(self, event):
        human = event.human

        for slider in self.sliders:
            slider.update()

        if event.change in ('reset', 'load', 'random'):
            self.updateMacro()

    def loadHandler(self, human, values):
        if values[0] == self._group:
            modifier = self.modifiers.get(values[1], None)
            if modifier:
                modifier.setValue(human, float(values[2]))

    def saveHandler(self, human, file):
        for name, modifier in self.modifiers.iteritems():
            if name is None:
                continue
            value = modifier.getValue(human)
            if value:
                file.write('%s %s %f\n' % (self._group, name, value))

    def setCamera(self):
        pass

class FaceTaskView(ModifierTaskView):
    _name = 'Face'
    _group = 'face'
    _features = [
        ('head shape', 'head', [
            (None, 'head-oval', 'frontView'),
            (None, 'head-round', 'frontView'),
            (None, 'head-rectangular', 'frontView'),
            (None, 'head-square', 'frontView'),
            (None, 'head-triangular', 'frontView'),
            (None, 'head-invertedtriangular', 'frontView'),
            (None, 'head-diamond', 'frontView'),
            ]),
        ('head', 'head', [
            (None, 'head-age', 'less', 'more', 'frontView'),
            (None, 'head-angle', 'in', 'out', 'rightView'),
            (None, 'head-scale-depth', 'less', 'more', 'rightView'),
            (None, 'head-scale-horiz', 'less', 'more', 'frontView'),
            (None, 'head-scale-vert', 'more', 'less', 'frontView'),
            (None, 'head-trans', 'in', 'out', 'frontView'),
            (None, 'head-trans', 'down', 'up', 'frontView'),
            (None, 'head-trans', 'forward', 'backward', 'rightView'),
            ]),
        ('neck', 'neck', [
            (None, 'neck-scale-depth', 'less', 'more', 'rightView'),
            (None, 'neck-scale-horiz', 'less', 'more', 'frontView'),
            (None, 'neck-scale-vert', 'more', 'less', 'frontView'),
            (None, 'neck-trans', 'in', 'out', 'frontView'),
            (None, 'neck-trans', 'down', 'up', 'frontView'),
            (None, 'neck-trans', 'forward', 'backward', 'rightView'),
            ]),
        ('right eye', 'eyes', [
            (None, 'r-eye-height1', 'min', 'max', 'frontView'),
            (None, 'r-eye-height2', 'min', 'max', 'frontView'),
            (None, 'r-eye-height3', 'min', 'max', 'frontView'),
            (None, 'r-eye-push1', 'in', 'out', 'frontView'),
            (None, 'r-eye-push2', 'in', 'out', 'frontView'),
            (None, 'r-eye-move', 'in', 'out', 'frontView'),
            (None, 'r-eye-move', 'up', 'down', 'frontView'),
            (None, 'r-eye', 'small', 'big', 'frontView'),
            (None, 'r-eye-corner1', 'up', 'down', 'frontView'),
            (None, 'r-eye-corner2', 'up', 'down', 'frontView')
            ]),
        ('left eye', 'eyes', [
            (None, 'l-eye-height1', 'min', 'max', 'frontView'),
            (None, 'l-eye-height2', 'min', 'max', 'frontView'),
            (None, 'l-eye-height3', 'min', 'max', 'frontView'),
            (None, 'l-eye-push1', 'in', 'out', 'frontView'),
            (None, 'l-eye-push2', 'in', 'out', 'frontView'),
            (None, 'l-eye-move', 'in', 'out', 'frontView'),
            (None, 'l-eye-move', 'up', 'down', 'frontView'),
            (None, 'l-eye', 'small', 'big', 'frontView'),
            (None, 'l-eye-corner1', 'up', 'down', 'frontView'),
            (None, 'l-eye-corner2', 'up', 'down', 'frontView'),
            ]),
        ('nose features', 'nose', [
            (None, 'nose', 'compress', 'uncompress', 'rightView'),
            (None, 'nose', 'convex', 'concave', 'rightView'),
            (None, 'nose', 'moregreek', 'lessgreek', 'rightView'),
            (None, 'nose', 'morehump', 'lesshump', 'rightView'),
            (None, 'nose', 'potato', 'point', 'rightView'),
            (None, 'nose-nostrils', 'point', 'unpoint', 'frontView'),
            (None, 'nose-nostrils', 'up', 'down', 'rightView'),
            (None, 'nose-point', 'up', 'down', 'rightView'),
            ]),
        ('nose size details', 'nose', [
            (None, 'nose-nostril-width', 'min', 'max', 'frontView'),
            (None, 'nose-height', 'min', 'max', 'rightView'),
            (None, 'nose-width1', 'min', 'max', 'frontView'),
            (None, 'nose-width2', 'min', 'max', 'frontView'),
            (None, 'nose-width3', 'min', 'max', 'frontView'),
            (None, 'nose-width', 'min', 'max', 'frontView'),
            ]),
        ('nose size', 'nose', [
            (None, 'nose-trans', 'up', 'down', 'frontView'),
            (None, 'nose-trans', 'forward', 'backward', 'rightView'),
            (None, 'nose-trans', 'in', 'out', 'frontView'),
            (None, 'nose-scale-vert', 'incr', 'decr', 'frontView'),
            (None, 'nose-scale-horiz', 'incr', 'decr', 'frontView'),
            (None, 'nose-scale-depth', 'incr', 'decr', 'rightView'),
            ]),
        ('mouth size', 'mouth', [
            (None, 'mouth-scale-horiz', 'incr', 'decr', 'frontView'),
            (None, 'mouth-scale-vert', 'incr', 'decr', 'frontView'),
            (None, 'mouth-scale-depth', 'incr', 'decr', 'rightView'),
            (None, 'mouth-trans', 'in', 'out', 'frontView'),
            (None, 'mouth-trans', 'up', 'down', 'frontView'),
            (None, 'mouth-trans', 'forward', 'backward', 'rightView'),
            ]),
        ('mouth size details', 'mouth', [
            (None, 'mouth-lowerlip-height', 'min', 'max', 'frontView'),
            (None, 'mouth-lowerlip-middle', 'up', 'down', 'frontView'),
            (None, 'mouth-lowerlip-width', 'min', 'max', 'frontView'),
            (None, 'mouth-upperlip-height', 'min', 'max', 'frontView'),
            (None, 'mouth-upperlip-width', 'min', 'max', 'frontView'),
            ]),
        ('mouth features', 'mouth', [
            (None, 'mouth-lowerlip-ext', 'up', 'down', 'frontView'),
            (None, 'mouth-angles', 'up', 'down', 'frontView'),
            (None, 'mouth-lowerlip-middle', 'up', 'down', 'frontView'),
            (None, 'mouth-lowerlip', 'deflate', 'inflate', 'rightView'),
            (None, 'mouth-philtrum', 'up', 'down', 'frontView'),
            (None, 'mouth-philtrum', 'increase', 'decrease', 'rightView'),
            (None, 'mouth-upperlip', 'deflate', 'inflate', 'rightView'),
            (None, 'mouth-upperlip-ext', 'up', 'down', 'frontView'),
            (None, 'mouth-upperlip-middle', 'up', 'down', 'frontView'),
            ]),
        ('right ear', 'ears', [
            (None, 'r-ear', 'backward', 'forward', 'rightView'),
            (None, 'r-ear', 'big', 'small', 'rightView'),
            (None, 'r-ear', 'down', 'up', 'rightView'),
            (None, 'r-ear-height', 'min', 'max', 'rightView'),
            (None, 'r-ear-lobe', 'min', 'max', 'rightView'),
            (None, 'r-ear', 'pointed', 'triangle', 'rightView'),
            (None, 'r-ear-rot', 'backward', 'forward', 'rightView'),
            (None, 'r-ear', 'square', 'round', 'rightView'),
            (None, 'r-ear-width', 'max', 'min', 'rightView'),
            (None, 'r-ear-wing', 'out', 'in', 'frontView'),
            (None, 'r-ear-flap', 'out', 'in', 'frontView'),
            ]),
        ('left ear', 'ears', [
            (None, 'l-ear', 'backward', 'forward', 'leftView'),
            (None, 'l-ear', 'big', 'small', 'leftView'),
            (None, 'l-ear', 'down', 'up', 'leftView'),
            (None, 'l-ear-height', 'min', 'max', 'leftView'),
            (None, 'l-ear-lobe', 'min', 'max', 'leftView'),
            (None, 'l-ear', 'pointed', 'triangle', 'leftView'),
            (None, 'l-ear-rot', 'backward', 'forward', 'leftView'),
            (None, 'l-ear', 'square', 'round', 'leftView'),
            (None, 'l-ear-width', 'max', 'min', 'leftView'),
            (None, 'l-ear-wing', 'out', 'in', 'frontView'),
            (None, 'l-ear-flap', 'out', 'in', 'frontView'),
            ]),
        ('chin', 'chin', [
            (None, 'chin', 'in', 'out', 'rightView'),
            (None, 'chin-width', 'min', 'max', 'frontView'),
            (None, 'chin-height', 'min', 'max', 'frontView'),
            (None, 'chin', 'squared', 'round', 'frontView'),
            (None, 'chin', 'prognathism1', 'prognathism2', 'rightView'),
            ]),
        ('cheek', 'cheek', [
            (None, 'l-cheek', 'in', 'out', 'frontView'),
            (None, 'l-cheek-bones', 'out', 'in', 'frontView'),
            (None, 'r-cheek', 'in', 'out', 'frontView'),
            (None, 'r-cheek-bones', 'out', 'in', 'frontView'),
            ]),
        ]

    def setCamera(self):
        gui3d.app.setFaceCamera()

class TorsoTaskView(ModifierTaskView):
    _name = 'Torso'
    _group = 'torso'
    _features = [
        ('Torso', 'torso', [
            (None, 'torso-scale-depth', 'decr', 'incr', 'setGlobalCamera'),
            (None, 'torso-scale-horiz', 'decr', 'incr', 'setGlobalCamera'),
            (None, 'torso-scale-vert', 'decr', 'incr', 'setGlobalCamera'),
            (None, 'torso-trans', 'in', 'out', 'setGlobalCamera'),
            (None, 'torso-trans', 'down', 'up', 'setGlobalCamera'),
            (None, 'torso-trans', 'forward', 'backward', 'setGlobalCamera'),
            ]),
        ('Hip', 'hip', [
            (None, 'hip-scale-depth', 'decr', 'incr', 'setGlobalCamera'),
            (None, 'hip-scale-horiz', 'decr', 'incr', 'setGlobalCamera'),
            (None, 'hip-scale-vert', 'decr', 'incr', 'setGlobalCamera'),
            (None, 'hip-trans', 'in', 'out', 'setGlobalCamera'),
            (None, 'hip-trans', 'down', 'up', 'setGlobalCamera'),
            (None, 'hip-trans', 'forward', 'backward', 'setGlobalCamera'),
            ]),
        ('Stomach', 'stomach', [
            (None, 'stomach-tone', 'decr', 'incr', 'setGlobalCamera'),
            ]),
        ('Buttocks', 'buttocks', [
            (None, 'buttocks-tone', 'decr', 'incr', 'setGlobalCamera'),
            ]),
        ('Pelvis', 'pelvis', [
            (None, 'pelvis-tone', 'decr', 'incr', 'setGlobalCamera'),
            ])
        ]

class ArmsLegsTaskView(ModifierTaskView):
    _name = 'Arms and Legs'
    _group = 'armslegs'
    _features = [
        ('right hand', 'armslegs', [
            (None, 'r-hand-scale-depth', 'decr', 'incr', 'setRightHandTopCamera'),
            (None, 'r-hand-scale-horiz', 'decr', 'incr', 'setRightHandFrontCamera'),
            (None, 'r-hand-scale-vert', 'decr', 'incr', 'setRightHandFrontCamera'),
            (None, 'r-hand-trans', 'in', 'out', 'setRightHandFrontCamera'),
            (None, 'r-hand-trans', 'down', 'up', 'setRightHandFrontCamera'),
            (None, 'r-hand-trans', 'forward', 'backward', 'setRightHandTopCamera'),
            ]),
        ('left hand', 'armslegs', [
            (None, 'l-hand-scale-depth', 'decr', 'incr', 'setLeftHandTopCamera'),
            (None, 'l-hand-scale-horiz', 'decr', 'incr', 'setLeftHandFrontCamera'),
            (None, 'l-hand-scale-vert', 'decr', 'incr', 'setLeftHandFrontCamera'),
            (None, 'l-hand-trans', 'in', 'out', 'setLeftHandFrontCamera'),
            (None, 'l-hand-trans', 'down', 'up', 'setLeftHandFrontCamera'),
            (None, 'l-hand-trans', 'forward', 'backward', 'setLeftHandTopCamera'),
            ]),
        ('right foot', 'armslegs', [
            (None, 'r-foot-scale-depth', 'decr', 'incr', 'setRightFootRightCamera'),
            (None, 'r-foot-scale-horiz', 'decr', 'incr', 'setRightFootFrontCamera'),
            (None, 'r-foot-scale-vert', 'decr', 'incr', 'setRightFootFrontCamera'),
            (None, 'r-foot-trans', 'in', 'out', 'setRightFootFrontCamera'),
            (None, 'r-foot-trans', 'down', 'up', 'setRightFootFrontCamera'),
            (None, 'r-foot-trans', 'forward', 'backward', 'setRightFootRightCamera'),
            ]),
        ('left foot', 'armslegs', [
            (None, 'l-foot-scale-depth', 'decr', 'incr', 'setLeftFootLeftCamera'),
            (None, 'l-foot-scale-horiz', 'decr', 'incr', 'setLeftFootFrontCamera'),
            (None, 'l-foot-scale-vert', 'decr', 'incr', 'setLeftFootFrontCamera'),
            (None, 'l-foot-trans', 'in', 'out', 'setLeftFootFrontCamera'),
            (None, 'l-foot-trans', 'down', 'up', 'setLeftFootFrontCamera'),
            (None, 'l-foot-trans', 'forward', 'backward', 'setLeftFootLeftCamera'),
            ]),
        ('left arm', 'armslegs', [
            (None, 'l-lowerarm-scale-depth', 'decr', 'incr', 'setLeftArmTopCamera'),
            (None, 'l-lowerarm-scale-horiz', 'decr', 'incr', 'setLeftArmFrontCamera'),
            (None, 'l-lowerarm-scale-vert', 'decr', 'incr', 'setLeftArmFrontCamera'),
            (None, 'l-lowerarm-trans', 'in', 'out', 'setLeftArmFrontCamera'),
            (None, 'l-lowerarm-trans', 'down', 'up', 'setLeftArmFrontCamera'),
            (None, 'l-lowerarm-trans', 'forward', 'backward', 'setLeftArmTopCamera'),
            (None, 'l-upperarm-scale-depth', 'decr', 'incr', 'setLeftArmTopCamera'),
            (None, 'l-upperarm-scale-horiz', 'decr', 'incr', 'setLeftArmFrontCamera'),
            (None, 'l-upperarm-scale-vert', 'decr', 'incr', 'setLeftArmFrontCamera'),
            (None, 'l-upperarm-trans', 'in', 'out', 'setLeftArmFrontCamera'),
            (None, 'l-upperarm-trans', 'down', 'up', 'setLeftArmFrontCamera'),
            (None, 'l-upperarm-trans', 'forward', 'backward', 'setLeftArmTopCamera'),
            ]),
        ('right arm', 'armslegs', [
            (None, 'r-lowerarm-scale-depth', 'decr', 'incr', 'setRightArmTopCamera'),
            (None, 'r-lowerarm-scale-horiz', 'decr', 'incr', 'setRightArmFrontCamera'),
            (None, 'r-lowerarm-scale-vert', 'decr', 'incr', 'setRightArmFrontCamera'),
            (None, 'r-lowerarm-trans', 'in', 'out', 'setRightArmFrontCamera'),
            (None, 'r-lowerarm-trans', 'down', 'up', 'setRightArmFrontCamera'),
            (None, 'r-lowerarm-trans', 'forward', 'backward', 'setRightArmTopCamera'),
            (None, 'r-upperarm-scale-depth', 'decr', 'incr', 'setRightArmTopCamera'),
            (None, 'r-upperarm-scale-horiz', 'decr', 'incr', 'setRightArmFrontCamera'),
            (None, 'r-upperarm-scale-vert', 'decr', 'incr', 'setRightArmFrontCamera'),
            (None, 'r-upperarm-trans', 'in', 'out', 'setRightArmFrontCamera'),
            (None, 'r-upperarm-trans', 'down', 'up', 'setRightArmFrontCamera'),
            (None, 'r-upperarm-trans', 'forward', 'backward', 'setRightArmTopCamera'),
            ]),
        ('left leg', 'armslegs', [
            (None, 'l-lowerleg-scale-depth', 'decr', 'incr', 'setLeftLegLeftCamera'),
            (None, 'l-lowerleg-scale-horiz', 'decr', 'incr', 'setLeftLegFrontCamera'),
            (None, 'l-lowerleg-scale-vert', 'decr', 'incr', 'setLeftLegFrontCamera'),
            (None, 'l-lowerleg-trans', 'in', 'out', 'setLeftLegFrontCamera'),
            (None, 'l-lowerleg-trans', 'down', 'up', 'setLeftLegFrontCamera'),
            (None, 'l-lowerleg-trans', 'forward', 'backward', 'setLeftLegLeftCamera'),
            (None, 'l-upperleg-scale-depth', 'decr', 'incr', 'setLeftLegLeftCamera'),
            (None, 'l-upperleg-scale-horiz', 'decr', 'incr', 'setLeftLegFrontCamera'),
            (None, 'l-upperleg-scale-vert', 'decr', 'incr', 'setLeftLegFrontCamera'),
            (None, 'l-upperleg-trans', 'in', 'out', 'setLeftLegFrontCamera'),
            (None, 'l-upperleg-trans', 'down', 'up', 'setLeftLegFrontCamera'),
            (None, 'l-upperleg-trans', 'forward', 'backward', 'setLeftLegLeftCamera'),
            ]),
        ('right leg', 'armslegs', [
            (None, 'r-lowerleg-scale-depth', 'decr', 'incr', 'setRightLegRightCamera'),
            (None, 'r-lowerleg-scale-horiz', 'decr', 'incr', 'setRightLegFrontCamera'),
            (None, 'r-lowerleg-scale-vert', 'decr', 'incr', 'setRightLegFrontCamera'),
            (None, 'r-lowerleg-trans', 'in', 'out', 'setRightLegFrontCamera'),
            (None, 'r-lowerleg-trans', 'down', 'up', 'setRightLegFrontCamera'),
            (None, 'r-lowerleg-trans', 'forward', 'backward', 'setRightLegRightCamera'),
            (None, 'r-upperleg-scale-depth', 'decr', 'incr', 'setRightLegRightCamera'),
            (None, 'r-upperleg-scale-horiz', 'decr', 'incr', 'setRightLegFrontCamera'),
            (None, 'r-upperleg-scale-vert', 'decr', 'incr', 'setRightLegFrontCamera'),
            (None, 'r-upperleg-trans', 'in', 'out', 'setRightLegFrontCamera'),
            (None, 'r-upperleg-trans', 'down', 'up', 'setRightLegFrontCamera'),
            (None, 'r-upperleg-trans', 'forward', 'backward', 'setRightLegRightCamera'),
            ])
        ]

class GenderTaskView(ModifierTaskView):
    _name = 'Gender'
    _group = 'gendered'
    _features = [
        ('Genitals', 'genitals', [
            (None, 'genitals', 'feminine', 'masculine', 'noSetCamera'),
            ]),
        ('Breast', 'breast', [
            (None, 'breast', 'down', 'up', 'noSetCamera'),
            (None, 'breast-dist', 'min', 'max', 'noSetCamera'),
            (None, 'breast-point', 'min', 'max', 'noSetCamera'),
            ]),
        ('Macro', 'breast', [
            ('Breast size', None, 'breastSize', -1.0, 1.0, 'noSetCamera'),
            ('Breast firmness', None, 'breastFirmness', 0.0, 1.0, 'noSetCamera'),
            ]),
        ]

class AsymmTaskView(ModifierTaskView):
    _name = 'Asymmetry'
    _group = 'asymmetry'
    _features = [
        ('brow', 'asym', [
            (None, 'asym-brown-1', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-brown-2', 'l', 'r', 'setFaceCamera'),
            ]),
        ('cheek', 'asym', [
            (None, 'asym-cheek-1', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-cheek-2', 'l', 'r', 'setFaceCamera'),
            ]),
        ('ear', 'asym', [
            (None, 'asym-ear-1', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-ear-2', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-ear-3', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-ear-4', 'l', 'r', 'setFaceCamera'),
            ]),
        ('eye', 'asym', [
            (None, 'asym-eye-1', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-eye-2', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-eye-3', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-eye-4', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-eye-5', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-eye-6', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-eye-7', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-eye-8', 'l', 'r', 'setFaceCamera'),
            ]),
        ('jaw', 'asym', [
            (None, 'asym-jaw-1', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-jaw-2', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-jaw-3', 'l', 'r', 'setFaceCamera'),
            ]),
        ('mouth', 'asym', [
            (None, 'asym-mouth-1', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-mouth-2', 'l', 'r', 'setFaceCamera'),
            ]),
        ('nose', 'asym', [
            (None, 'asym-nose-1', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-nose-2', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-nose-3', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-nose-4', 'l', 'r', 'setFaceCamera'),
            ]),
        ('temple', 'asym', [
            (None, 'asym-temple-1', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-temple-2', 'l', 'r', 'setFaceCamera'),
            ]),
        ('top', 'asym', [
            (None, 'asym-top-1', 'l', 'r', 'setFaceCamera'),
            (None, 'asym-top-2', 'l', 'r', 'setFaceCamera'),
            ]),
        ('body', 'asym', [
            (None, 'asymm-breast-1', 'l', 'r', 'setGlobalCamera'),
            (None, 'asymm-trunk-1', 'l', 'r', 'setGlobalCamera'),
            ]),
        ]

class MacroTaskView(ModifierTaskView):
    _name = 'Macro modelling'
    _label = 'Macro'

    _features = [
        ('Macro', 'macrodetails', [
            ('Gender', None, 'Gender', 0.0, 1.0, 'noSetCamera'),
            ('Age', None, 'Age', 0.0, 1.0, 'noSetCamera'),
            ('Tone', 'universal', 'Muscle', 0.0, 1.0, 'noSetCamera'),
            ('Weight', 'universal', 'Weight', 0.0, 1.0, 'noSetCamera'),
            ('Height', 'universal-stature', 'Height', -1.0, 1.0, 'noSetCamera'),
            ('African', None, 'African', 0.0, 1.0, 'noSetCamera'),
            ('Asian', None, 'Asian', 0.0, 1.0, 'noSetCamera'),
            ('Caucasian', None, 'Caucasian', 0.0, 1.0, 'noSetCamera'),
            ]),
        ]

    def __init__(self, category):
        super(MacroTaskView, self).__init__(category)
        for race, modifier, slider in self.raceSliders():
            slider.setValue(1.0/3)

    def raceSliders(self):
        for slider in self.sliders:
            modifier = slider.modifier
            if not isinstance(modifier, humanmodifier.MacroModifier):
                continue
            variable = modifier.variable
            if variable in ('African', 'Asian', 'Caucasian'):
                yield (variable, modifier, slider)

    def syncStatus(self):
        human = gui3d.app.selectedHuman
        
        if human.getGender() == 0.0:
            gender = gui3d.app.getLanguageString('female')
        elif human.getGender() == 1.0:
            gender = gui3d.app.getLanguageString('male')
        elif abs(human.getGender() - 0.5) < 0.01:
            gender = gui3d.app.getLanguageString('neutral')
        else:
            gender = gui3d.app.getLanguageString('%.2f%% female, %.2f%% male') % ((1.0 - human.getGender()) * 100, human.getGender() * 100)
        
        if human.getAge() < 0.5:
            age = 12 + ((25 - 12) * 2) * human.getAge()
        else:
            age = 25 + ((70 - 25) * 2) * (human.getAge() - 0.5)
        
        muscle = (human.getMuscle() * 100.0)
        weight = (50 + (150 - 50) * human.getWeight())
        coords = human.meshData.getCoords([8223,12361,13155])
        height = 10 * max(coords[0][1] - coords[1][1], coords[0][1] - coords[2][1])
        if gui3d.app.settings['units'] == 'metric':
            units = 'cm'
        else:
            units = 'in'
            height *= 0.393700787

        self.setStatus('Gender: %s, Age: %d, Muscle: %.2f%%, Weight: %.2f%%, Height: %.2f %s', gender, age, muscle, weight, height, units)

    def syncRaceSliders(self, event):
        human = event.human
        for race, modifier, slider in self.raceSliders():
            slider.setValue(1.0/3)
            value = modifier.getValue(human)
            modifier.setValue(human, value)
            slider.setValue(value)

    def setStatus(self, format, *args):
        gui3d.app.statusPersist(format, *args)

    def onShow(self, event):
        self.syncStatus()
        super(MacroTaskView, self).onShow(event)

    def onHide(self, event):
        self.setStatus('')
        super(MacroTaskView, self).onHide(event)

    def onHumanChaging(self, event):
        super(MacroTaskView, self).onHumanChanging(event)
        if event.change in ('caucasian', 'asian', 'african'):
            self.syncRaceSliders(event)

    def onHumanChanged(self, event):
        super(MacroTaskView, self).onHumanChanged(event)
        if self.isVisible():
            self.syncStatus()
        if event.change in ('caucasian', 'asian', 'african'):
            self.syncRaceSliders(event)

def load(app):
    category = app.getCategory('Modelling')

    gui3d.app.noSetCamera = (lambda: None)

    for type in [MacroTaskView, GenderTaskView, FaceTaskView, TorsoTaskView, ArmsLegsTaskView, AsymmTaskView]:
        taskview = category.addTask(type(category))
        if taskview._group is not None:
            app.addLoadHandler(taskview._group, taskview.loadHandler)
            app.addSaveHandler(taskview.saveHandler)

def unload(app):
    pass
