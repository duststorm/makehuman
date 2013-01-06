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

# Gender[0..1]
# -
# maleVal = Gender
# femaleVal = 1 - Gender
# -
# male : maleVal
# female : femaleVal

# Age [0..1]
# -
# childVal = max(0, 1 - 2 * Age)
# youngVal = 1 - abs(2 * Age - 1)
# oldVal = max(0, 2 * Age - 1)
# -
# child : childVal
# young : youngVal
# old : oldVal

# Weight [0..1]
# -
# underweightVal = max(0, 1 - 2 * Weight)
# overweightVal = max(0, 2 * Weight - 1)
# -
# heavy : overweightVal
# [averageWeight] : 1 - underweightVal - overweightVal
# light : underweightVal

# Muscle [0..1]
# -
# muscleVal = max(0, 2 * Muscle - 1)
# flaccidVal = max(0, 1 - 2 * weight)
# -
# flaccid : flaccidVal
# [averageTone] : 1 - flaccidVal - muscleVal
# muscle : muscleVal

# African [0..1]
# -
# africanVal = african
# -
# african : africanVal / len(ethnics)

# Asian [0..1]
# -
# asianVal = asian
# -
# asian : asianVal / len(ethnics)

# ... [0..1]
# -
# ...
# -
# caucasian : (1 - (africanVal + asianVal) / len(ethnics))

# Height [-1..1]
# ...
# -
# dwarf : -min(0, height)
# giant :  max(0, height)

# ... [0..1]
# -
# breastFirmness
# -
# firmness0 : 1 - breastFirmness
# firmness1 : breastFirmness

# ... [-1..1]
# -
# breastSize
# -
# cup1 : -min(0, breastSize)
# cup2 :  max(0, breastSize)

_targets = None

def getTargets():
    global _targets
    if _targets is None:
        _targets = targets.Targets('data/targets')
    return _targets

class GenericModifier(humanmodifier.GenericModifier):
    @staticmethod
    def findTargets(path):
        if path is None:
            return []
        path = tuple(path.split('-'))
        targets = []
        if path not in getTargets().groups:
            log.debug('missing target %s', path)
        for target in getTargets().groups.get(path, []):
            keys = [var
                    for var in target.data.itervalues()
                    if var is not None]
            keys.append('-'.join(target.key))
            targets.append((target.path, keys))
        return targets

    def __init__(self, left, right, center=None):
        self.left = left
        self.right = right
        self.center = center

        self.l_targets = self.findTargets(left)
        self.r_targets = self.findTargets(right)
        self.c_targets = self.findTargets(center)

        self.targets = self.l_targets + self.r_targets + self.c_targets

        self.verts = None
        self.faces = None

    def clampValue(self, value):
        value = min(1.0, value)
        if self.left is not None:
            value = max(-1.0, value)
        else:
            value = max( 0.0, value)
        return value

    def setValue(self, human, value):
        value = self.clampValue(value)
        factors = self.getFactors(human, value)

        for tpath, tfactors in self.targets:
            human.setDetail(tpath, reduce((lambda x, y: x * y), [factors[factor] for factor in tfactors]))

    @staticmethod
    def parseTarget(target):
        return target[0].split('/')[-1].split('.')[0].split('-')

    def getValue(self, human):
        right = sum([human.getDetail(target[0]) for target in self.r_targets])
        if right:
            return right
        else:
            return -sum([human.getDetail(target[0]) for target in self.l_targets])

    def getFactors(self, human, value):
        ethnics = [val for val in [human.africanVal, human.asianVal] if val > 0.0]
        height = human.getHeight()
        
        factors = {
            'female': human.femaleVal,
            'male': human.maleVal,
            'child': human.childVal,
            'young': human.youngVal,
            'old': human.oldVal,
            'african': human.africanVal / len(ethnics) if ethnics else human.africanVal,
            'asian': human.asianVal / len(ethnics) if ethnics else human.asianVal,
            'caucasian': (1.0 - sum(ethnics) / len(ethnics)) if ethnics else 1.0,
            'flaccid': human.flaccidVal,
            'muscle': human.muscleVal,
            'averageTone': 1.0 - (human.flaccidVal + human.muscleVal),
            'light': human.underweightVal,
            'heavy': human.overweightVal,
            'averageWeight': 1.0 - (human.underweightVal + human.overweightVal),
            'dwarf': -min(height, 0.0),
            'giant': max(0.0, height),
            'firmness0': 1.0 - human.breastFirmness,
            'firmness1': human.breastFirmness,
            'cup1': -min(human.breastSize, 0.0),
            'cup2': max(0.0, human.breastSize)
            }

        return factors

class UniversalModifier(GenericModifier):
    def getFactors(self, human, value):
        factors = GenericModifier.getFactors(self, human, value)

        if self.left is not None:
            factors[self.left] = -min(value, 0.0)
        if self.center is not None:
            factors[self.center] = 1.0 - abs(value)
        factors[self.right] = max(0.0, value)

        return factors

class MacroModifier(GenericModifier):
    def __init__(self, base, name, variable, min, max):
        self.name = '-'.join(atom
                             for atom in (base, name)
                             if atom is not None)
        self.variable = variable
        self.min = min
        self.max = max

        self.targets = self.findTargets(self.name)

        self.verts = None
        self.faces = None

    def getValue(self, human):
        getter = 'get' + self.variable
        if hasattr(human, getter):
            return getattr(human, getter)()
        else:
            return getattr(human, self.variable)

    def setValue(self, human, value):
        value = self.clampValue(value)
        setter = 'set' + self.variable
        if hasattr(human, setter):
            getattr(human, setter)(value)
        else:
            setattr(human, self.variable, value)
        GenericModifier.setValue(self, human, value)

    def clampValue(self, value):
        return max(self.min, min(self.max, value))

    def getFactors(self, human, value):
        factors = GenericModifier.getFactors(self, human, value)
        factors[self.name] = 1.0
        return factors

class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, task, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        self.task = task

    def onClicked(self, event):
        self.task.groupBox.showWidget(self.groupBox)

class GenericSlider(humanmodifier.ModifierSlider):
    @staticmethod
    def findImage(name):
        if name is None:
            return None
        name = name.lower()
        return getTargets().images.get(name, name)

    def __init__(self, min, max, modifier, label, image, view):
        image = self.findImage(image)
        super(GenericSlider, self).__init__(min=min, max=1.0, label=label, modifier=modifier, image=image)
        self.view = getattr(gui3d.app, view)

    def onFocus(self, event):
        super(GenericSlider, self).onFocus(event)
        if gui3d.app.settings.get('cameraAutoZoom', True):
            self.view()

class UniversalSlider(GenericSlider):
    def __init__(self, modifier, label, image, view):
        min = -1.0 if modifier.left is not None else 0.0
        super(UniversalSlider, self).__init__(min, 1.0, modifier, label, image, view)

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
                macro = len(template) > 4
                if macro:
                    tname, tvar, tlabel, tmin, tmax, tview = template
                    modifier = MacroModifier(base, tname, tvar, tmin, tmax)
                    self.modifiers[tname] = modifier
                    slider = GenericSlider(tmin, tmax, modifier, tlabel, None, tview)
                else:
                    paired = len(template) == 4
                    if paired:
                        tname, tleft, tright, tview = template
                        left  = '-'.join([base, tname, tleft])
                        right = '-'.join([base, tname, tright])
                    else:
                        tname, tview = template
                        left = None
                        right = '-'.join([base, tname])

                    modifier = UniversalModifier(left, right)

                    tpath = '-'.join(template[:-1])
                    modifierName = tpath
                    clashIndex = 0
                    while modifierName in self.modifiers:
                        log.debug('modifier clash: %s', modifierName)
                        modifierName = '%s%d' % (tpath, clashIndex)
                        clashIndex += 1

                    self.modifiers[modifierName] = modifier
                    slider = UniversalSlider(modifier, None, '%s.png' % tpath, tview)

                box.addWidget(slider)
                self.sliders.append(slider)

        self.groupBox.showWidget(self.groupBoxes[0])

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

    def loadHandler(self, human, values):
        if values[0] == self._group:
            modifier = self.modifiers.get(values[1].replace("-", " "), None)
            if modifier:
                modifier.setValue(human, float(values[2]))

    def saveHandler(self, human, file):
        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('%s %s %f\n' % (self._group, name.replace(" ", "-"), value))

    def setCamera(self):
        pass

class FaceTaskView(ModifierTaskView):
    _name = 'Face'
    _group = 'face'
    _features = [
        ('head shape', 'head', [
            ('head-oval', 'frontView'),
            ('head-round', 'frontView'),
            ('head-rectangular', 'frontView'),
            ('head-square', 'frontView'),
            ('head-triangular', 'frontView'),
            ('head-invertedtriangular', 'frontView'),
            ('head-diamond', 'frontView'),
            ]),
        ('head', 'head', [
            ('head-age', 'less', 'more', 'frontView'),
            ('head-angle', 'in', 'out', 'rightView'),
            ('head-scale-depth', 'less', 'more', 'rightView'),
            ('head-scale-horiz', 'less', 'more', 'frontView'),
            ('head-scale-vert', 'more', 'less', 'frontView'),
            ('head-trans', 'in', 'out', 'frontView'),
            ('head-trans', 'down', 'up', 'frontView'),
            ('head-trans', 'forward', 'backward', 'rightView'),
            ]),
        ('neck', 'neck', [
            ('neck-scale-depth', 'less', 'more', 'rightView'),
            ('neck-scale-horiz', 'less', 'more', 'frontView'),
            ('neck-scale-vert', 'more', 'less', 'frontView'),
            ('neck-trans', 'in', 'out', 'frontView'),
            ('neck-trans', 'down', 'up', 'frontView'),
            ('neck-trans', 'forward', 'backward', 'rightView'),
            ]),
        ('right eye', 'eyes', [
            ('r-eye-height1', 'min', 'max', 'frontView'),
            ('r-eye-height2', 'min', 'max', 'frontView'),
            ('r-eye-height3', 'min', 'max', 'frontView'),
            ('r-eye-push1', 'in', 'out', 'frontView'),
            ('r-eye-push2', 'in', 'out', 'frontView'),
            ('r-eye-move', 'in', 'out', 'frontView'),
            ('r-eye-move', 'up', 'down', 'frontView'),
            ('r-eye', 'small', 'big', 'frontView'),
            ('r-eye-corner1', 'up', 'down', 'frontView'),
            ('r-eye-corner2', 'up', 'down', 'frontView')
            ]),
        ('left eye', 'eyes', [
            ('l-eye-height1', 'min', 'max', 'frontView'),
            ('l-eye-height2', 'min', 'max', 'frontView'),
            ('l-eye-height3', 'min', 'max', 'frontView'),
            ('l-eye-push1', 'in', 'out', 'frontView'),
            ('l-eye-push2', 'in', 'out', 'frontView'),
            ('l-eye-move', 'in', 'out', 'frontView'),
            ('l-eye-move', 'up', 'down', 'frontView'),
            ('l-eye', 'small', 'big', 'frontView'),
            ('l-eye-corner1', 'up', 'down', 'frontView'),
            ('l-eye-corner2', 'up', 'down', 'frontView'),
            ]),
        ('nose features', 'nose', [
            ('nose', 'compress', 'uncompress', 'rightView'),
            ('nose', 'convex', 'concave', 'rightView'),
            ('nose', 'moregreek', 'lessgreek', 'rightView'),
            ('nose', 'morehump', 'lesshump', 'rightView'),
            ('nose', 'potato', 'point', 'rightView'),
            ('nose-nostrils', 'point', 'unpoint', 'frontView'),
            ('nose-nostrils', 'up', 'down', 'rightView'),
            ('nose-point', 'up', 'down', 'rightView'),
            ]),
        ('nose size details', 'nose', [
            ('nose-nostril-width', 'min', 'max', 'frontView'),
            ('nose-height', 'min', 'max', 'rightView'),
            ('nose-width1', 'min', 'max', 'frontView'),
            ('nose-width2', 'min', 'max', 'frontView'),
            ('nose-width3', 'min', 'max', 'frontView'),
            ('nose-width', 'min', 'max', 'frontView'),
            ]),
        ('nose size', 'nose', [
            ('nose-trans', 'up', 'down', 'frontView'),
            ('nose-trans', 'forward', 'backward', 'rightView'),
            ('nose-trans', 'in', 'out', 'frontView'),
            ('nose-scale-vert', 'incr', 'decr', 'frontView'),
            ('nose-scale-horiz', 'incr', 'decr', 'frontView'),
            ('nose-scale-depth', 'incr', 'decr', 'rightView'),
            ]),
        ('mouth size', 'mouth', [
            ('mouth-scale-horiz', 'incr', 'decr', 'frontView'),
            ('mouth-scale-vert', 'incr', 'decr', 'frontView'),
            ('mouth-scale-depth', 'incr', 'decr', 'rightView'),
            ('mouth-trans', 'in', 'out', 'frontView'),
            ('mouth-trans', 'up', 'down', 'frontView'),
            ('mouth-trans', 'forward', 'backward', 'rightView'),
            ]),
        ('mouth size details', 'mouth', [
            ('mouth-lowerlip-height', 'min', 'max', 'frontView'),
            ('mouth-lowerlip-middle', 'up', 'down', 'frontView'),
            ('mouth-lowerlip-width', 'min', 'max', 'frontView'),
            ('mouth-upperlip-height', 'min', 'max', 'frontView'),
            ('mouth-upperlip-width', 'min', 'max', 'frontView'),
            ]),
        ('mouth features', 'mouth', [
            ('mouth-lowerlip-ext', 'up', 'down', 'frontView'),
            ('mouth-angles', 'up', 'down', 'frontView'),
            ('mouth-lowerlip-middle', 'up', 'down', 'frontView'),
            ('mouth-lowerlip', 'deflate', 'inflate', 'rightView'),
            ('mouth-philtrum', 'up', 'down', 'frontView'),
            ('mouth-philtrum', 'increase', 'decrease', 'rightView'),
            ('mouth-upperlip', 'deflate', 'inflate', 'rightView'),
            ('mouth-upperlip-ext', 'up', 'down', 'frontView'),
            ('mouth-upperlip-middle', 'up', 'down', 'frontView'),
            ]),
        ('right ear', 'ears', [
            ('r-ear', 'backward', 'forward', 'rightView'),
            ('r-ear', 'big', 'small', 'rightView'),
            ('r-ear', 'down', 'up', 'rightView'),
            ('r-ear-height', 'min', 'max', 'rightView'),
            ('r-ear-lobe', 'min', 'max', 'rightView'),
            ('r-ear', 'pointed', 'triangle', 'rightView'),
            ('r-ear-rot', 'backward', 'forward', 'rightView'),
            ('r-ear', 'square', 'round', 'rightView'),
            ('r-ear-width', 'max', 'min', 'rightView'),
            ('r-ear-wing', 'out', 'in', 'frontView'),
            ('r-ear-flap', 'out', 'in', 'frontView'),
            ]),
        ('left ear', 'ears', [
            ('l-ear', 'backward', 'forward', 'leftView'),
            ('l-ear', 'big', 'small', 'leftView'),
            ('l-ear', 'down', 'up', 'leftView'),
            ('l-ear-height', 'min', 'max', 'leftView'),
            ('l-ear-lobe', 'min', 'max', 'leftView'),
            ('l-ear', 'pointed', 'triangle', 'leftView'),
            ('l-ear-rot', 'backward', 'forward', 'leftView'),
            ('l-ear', 'square', 'round', 'leftView'),
            ('l-ear-width', 'max', 'min', 'leftView'),
            ('l-ear-wing', 'out', 'in', 'frontView'),
            ('l-ear-flap', 'out', 'in', 'frontView'),
            ]),
        ('chin', 'chin', [
            ('chin', 'in', 'out', 'rightView'),
            ('chin-width', 'min', 'max', 'frontView'),
            ('chin-height', 'min', 'max', 'frontView'),
            ('chin', 'squared', 'round', 'frontView'),
            ('chin', 'prognathism1', 'prognathism2', 'rightView'),
            ]),
        ('cheek', 'cheek', [
              ('l-cheek', 'in', 'out', 'frontView'),
              ('l-cheek-bones', 'out', 'in', 'frontView'),
              ('r-cheek', 'in', 'out', 'frontView'),
              ('r-cheek-bones', 'out', 'in', 'frontView'),
             ]),
        ]

    def setCamera(self):
        gui3d.app.setFaceCamera()

class TorsoTaskView(ModifierTaskView):
    _name = 'Torso'
    _group = 'torso'
    _features = [
        ('Torso', 'torso', [
            ('torso-scale-depth', 'decr', 'incr', 'setGlobalCamera'),
            ('torso-scale-horiz', 'decr', 'incr', 'setGlobalCamera'),
            ('torso-scale-vert', 'decr', 'incr', 'setGlobalCamera'),
            ('torso-trans', 'in', 'out', 'setGlobalCamera'),
            ('torso-trans', 'down', 'up', 'setGlobalCamera'),
            ('torso-trans', 'forward', 'backward', 'setGlobalCamera'),
            ]),
        ('Hip', 'hip', [
            ('hip-scale-depth', 'decr', 'incr', 'setGlobalCamera'),
            ('hip-scale-horiz', 'decr', 'incr', 'setGlobalCamera'),
            ('hip-scale-vert', 'decr', 'incr', 'setGlobalCamera'),
            ('hip-trans', 'in', 'out', 'setGlobalCamera'),
            ('hip-trans', 'down', 'up', 'setGlobalCamera'),
            ('hip-trans', 'forward', 'backward', 'setGlobalCamera'),
            ]),
        ('Stomach', 'stomach', [
            ('stomach-tone', 'decr', 'incr', 'setGlobalCamera'),
            ]),
        ('Buttocks', 'buttocks', [
            ('buttocks-tone', 'decr', 'incr', 'setGlobalCamera'),
            ]),
        ('Pelvis', 'pelvis', [
            ('pelvis-tone', 'decr', 'incr', 'setGlobalCamera'),
            ])
        ]

class ArmsLegsTaskView(ModifierTaskView):
    _name = 'Arms and Legs'
    _group = 'armslegs'
    _features = [
        ('right hand', 'armslegs', [
                ('r-hand-scale-depth', 'decr', 'incr', 'setRightHandTopCamera'),
                ('r-hand-scale-horiz', 'decr', 'incr', 'setRightHandFrontCamera'),
                ('r-hand-scale-vert', 'decr', 'incr', 'setRightHandFrontCamera'),
                ('r-hand-trans', 'in', 'out', 'setRightHandFrontCamera'),
                ('r-hand-trans', 'down', 'up', 'setRightHandFrontCamera'),
                ('r-hand-trans', 'forward', 'backward', 'setRightHandTopCamera'),

            ]),
        ('left hand', 'armslegs', [
                ('l-hand-scale-depth', 'decr', 'incr', 'setLeftHandTopCamera'),
                ('l-hand-scale-horiz', 'decr', 'incr', 'setLeftHandFrontCamera'),
                ('l-hand-scale-vert', 'decr', 'incr', 'setLeftHandFrontCamera'),
                ('l-hand-trans', 'in', 'out', 'setLeftHandFrontCamera'),
                ('l-hand-trans', 'down', 'up', 'setLeftHandFrontCamera'),
                ('l-hand-trans', 'forward', 'backward', 'setLeftHandTopCamera'),

            ]),
        ('right foot', 'armslegs', [
                ('r-foot-scale-depth', 'decr', 'incr', 'setRightFootRightCamera'),
                ('r-foot-scale-horiz', 'decr', 'incr', 'setRightFootFrontCamera'),
                ('r-foot-scale-vert', 'decr', 'incr', 'setRightFootFrontCamera'),
                ('r-foot-trans', 'in', 'out', 'setRightFootFrontCamera'),
                ('r-foot-trans', 'down', 'up', 'setRightFootFrontCamera'),
                ('r-foot-trans', 'forward', 'backward', 'setRightFootRightCamera'),

            ]),
        ('left foot', 'armslegs', [
                ('l-foot-scale-depth', 'decr', 'incr', 'setLeftFootLeftCamera'),
                ('l-foot-scale-horiz', 'decr', 'incr', 'setLeftFootFrontCamera'),
                ('l-foot-scale-vert', 'decr', 'incr', 'setLeftFootFrontCamera'),
                ('l-foot-trans', 'in', 'out', 'setLeftFootFrontCamera'),
                ('l-foot-trans', 'down', 'up', 'setLeftFootFrontCamera'),
                ('l-foot-trans', 'forward', 'backward', 'setLeftFootLeftCamera'),

            ]),
        ('left arm', 'armslegs', [
                ('l-lowerarm-scale-depth', 'decr', 'incr', 'setLeftArmTopCamera'),
                ('l-lowerarm-scale-horiz', 'decr', 'incr', 'setLeftArmFrontCamera'),
                ('l-lowerarm-scale-vert', 'decr', 'incr', 'setLeftArmFrontCamera'),
                ('l-lowerarm-trans', 'in', 'out', 'setLeftArmFrontCamera'),
                ('l-lowerarm-trans', 'down', 'up', 'setLeftArmFrontCamera'),
                ('l-lowerarm-trans', 'forward', 'backward', 'setLeftArmTopCamera'),
                ('l-upperarm-scale-depth', 'decr', 'incr', 'setLeftArmTopCamera'),
                ('l-upperarm-scale-horiz', 'decr', 'incr', 'setLeftArmFrontCamera'),
                ('l-upperarm-scale-vert', 'decr', 'incr', 'setLeftArmFrontCamera'),
                ('l-upperarm-trans', 'in', 'out', 'setLeftArmFrontCamera'),
                ('l-upperarm-trans', 'down', 'up', 'setLeftArmFrontCamera'),
                ('l-upperarm-trans', 'forward', 'backward', 'setLeftArmTopCamera'),

            ]),
        ('right arm', 'armslegs', [
                ('r-lowerarm-scale-depth', 'decr', 'incr', 'setRightArmTopCamera'),
                ('r-lowerarm-scale-horiz', 'decr', 'incr', 'setRightArmFrontCamera'),
                ('r-lowerarm-scale-vert', 'decr', 'incr', 'setRightArmFrontCamera'),
                ('r-lowerarm-trans', 'in', 'out', 'setRightArmFrontCamera'),
                ('r-lowerarm-trans', 'down', 'up', 'setRightArmFrontCamera'),
                ('r-lowerarm-trans', 'forward', 'backward', 'setRightArmTopCamera'),
                ('r-upperarm-scale-depth', 'decr', 'incr', 'setRightArmTopCamera'),
                ('r-upperarm-scale-horiz', 'decr', 'incr', 'setRightArmFrontCamera'),
                ('r-upperarm-scale-vert', 'decr', 'incr', 'setRightArmFrontCamera'),
                ('r-upperarm-trans', 'in', 'out', 'setRightArmFrontCamera'),
                ('r-upperarm-trans', 'down', 'up', 'setRightArmFrontCamera'),
                ('r-upperarm-trans', 'forward', 'backward', 'setRightArmTopCamera'),

            ]),
        ('left leg', 'armslegs', [
                ('l-lowerleg-scale-depth', 'decr', 'incr', 'setLeftLegLeftCamera'),
                ('l-lowerleg-scale-horiz', 'decr', 'incr', 'setLeftLegFrontCamera'),
                ('l-lowerleg-scale-vert', 'decr', 'incr', 'setLeftLegFrontCamera'),
                ('l-lowerleg-trans', 'in', 'out', 'setLeftLegFrontCamera'),
                ('l-lowerleg-trans', 'down', 'up', 'setLeftLegFrontCamera'),
                ('l-lowerleg-trans', 'forward', 'backward', 'setLeftLegLeftCamera'),
                ('l-upperleg-scale-depth', 'decr', 'incr', 'setLeftLegLeftCamera'),
                ('l-upperleg-scale-horiz', 'decr', 'incr', 'setLeftLegFrontCamera'),
                ('l-upperleg-scale-vert', 'decr', 'incr', 'setLeftLegFrontCamera'),
                ('l-upperleg-trans', 'in', 'out', 'setLeftLegFrontCamera'),
                ('l-upperleg-trans', 'down', 'up', 'setLeftLegFrontCamera'),
                ('l-upperleg-trans', 'forward', 'backward', 'setLeftLegLeftCamera'),

            ]),
        ('right leg', 'armslegs', [
                ('r-lowerleg-scale-depth', 'decr', 'incr', 'setRightLegRightCamera'),
                ('r-lowerleg-scale-horiz', 'decr', 'incr', 'setRightLegFrontCamera'),
                ('r-lowerleg-scale-vert', 'decr', 'incr', 'setRightLegFrontCamera'),
                ('r-lowerleg-trans', 'in', 'out', 'setRightLegFrontCamera'),
                ('r-lowerleg-trans', 'down', 'up', 'setRightLegFrontCamera'),
                ('r-lowerleg-trans', 'forward', 'backward', 'setRightLegRightCamera'),
                ('r-upperleg-scale-depth', 'decr', 'incr', 'setRightLegRightCamera'),
                ('r-upperleg-scale-horiz', 'decr', 'incr', 'setRightLegFrontCamera'),
                ('r-upperleg-scale-vert', 'decr', 'incr', 'setRightLegFrontCamera'),
                ('r-upperleg-trans', 'in', 'out', 'setRightLegFrontCamera'),
                ('r-upperleg-trans', 'down', 'up', 'setRightLegFrontCamera'),
                ('r-upperleg-trans', 'forward', 'backward', 'setRightLegRightCamera'),
            ])
        ]

class GenderTaskView(ModifierTaskView):
    _name = 'Gender'
    _features = [
        ('Genitals', 'genitals', [
            ('genitals', 'feminine', 'masculine', 'noSetCamera'),
            ]),
        ('Breast', 'breast', [
            ('breast', 'down', 'up', 'noSetCamera'),
            ('breast-dist', 'min', 'max', 'noSetCamera'),
            ('breast-point', 'min', 'max', 'noSetCamera'),
            ]),
        ('Macro', 'breast', [
            (None, 'breastSize', 'Breast size', -1.0, 1.0, 'noSetCamera'),
            (None, 'breastFirmness', 'Breast firmness', 0.0, 1.0, 'noSetCamera'),
            ]),
        ]

class AsymmTaskView(ModifierTaskView):
    _name = 'Asymmetry'
    _features = [
        ('brow', 'asym', [
            ('asym-brown-1', 'l', 'r', 'setFaceCamera'),
            ('asym-brown-2', 'l', 'r', 'setFaceCamera'),
            ]),
        ('cheek', 'asym', [
            ('asym-cheek-1', 'l', 'r', 'setFaceCamera'),
            ('asym-cheek-2', 'l', 'r', 'setFaceCamera'),
            ]),
        ('ear', 'asym', [
            ('asym-ear-1', 'l', 'r', 'setFaceCamera'),
            ('asym-ear-2', 'l', 'r', 'setFaceCamera'),
            ('asym-ear-3', 'l', 'r', 'setFaceCamera'),
            ('asym-ear-4', 'l', 'r', 'setFaceCamera'),
            ]),
        ('eye', 'asym', [
            ('asym-eye-1', 'l', 'r', 'setFaceCamera'),
            ('asym-eye-2', 'l', 'r', 'setFaceCamera'),
            ('asym-eye-3', 'l', 'r', 'setFaceCamera'),
            ('asym-eye-4', 'l', 'r', 'setFaceCamera'),
            ('asym-eye-5', 'l', 'r', 'setFaceCamera'),
            ('asym-eye-6', 'l', 'r', 'setFaceCamera'),
            ('asym-eye-7', 'l', 'r', 'setFaceCamera'),
            ('asym-eye-8', 'l', 'r', 'setFaceCamera'),
            ]),
        ('jaw', 'asym', [
            ('asym-jaw-1', 'l', 'r', 'setFaceCamera'),
            ('asym-jaw-2', 'l', 'r', 'setFaceCamera'),
            ('asym-jaw-3', 'l', 'r', 'setFaceCamera'),
            ]),
        ('mouth', 'asym', [
            ('asym-mouth-1', 'l', 'r', 'setFaceCamera'),
            ('asym-mouth-2', 'l', 'r', 'setFaceCamera'),
            ]),
        ('nose', 'asym', [
            ('asym-nose-1', 'l', 'r', 'setFaceCamera'),
            ('asym-nose-2', 'l', 'r', 'setFaceCamera'),
            ('asym-nose-3', 'l', 'r', 'setFaceCamera'),
            ('asym-nose-4', 'l', 'r', 'setFaceCamera'),
            ]),
        ('temple', 'asym', [
            ('asym-temple-1', 'l', 'r', 'setFaceCamera'),
            ('asym-temple-2', 'l', 'r', 'setFaceCamera'),
            ]),
        ('top', 'asym', [
            ('asym-top-1', 'l', 'r', 'setFaceCamera'),
            ('asym-top-2', 'l', 'r', 'setFaceCamera'),
            ]),
        ('body', 'asym', [
            ('asymm-breast-1', 'l', 'r', 'setGlobalCamera'),
            ('asymm-trunk-1', 'l', 'r', 'setGlobalCamera'),
            ]),
        ]

class MacroTaskView(ModifierTaskView):
    _name = 'Macro modelling'
    _label = 'Macro'

    _features = [
        ('Macro', 'macrodetails', [
            (None, 'Gender', 'Gender', 0.0, 1.0, 'noSetCamera'),
            (None, 'Age', 'Age', 0.0, 1.0, 'noSetCamera'),
            ('universal', 'Muscle', 'Tone', 0.0, 1.0, 'noSetCamera'),
            ('universal', 'Weight', 'Weight', 0.0, 1.0, 'noSetCamera'),
            ('universal-stature', 'Height', 'Height', -1.0, 1.0, 'noSetCamera'),
            (None, 'African', 'Afro', 0.0, 1.0, 'noSetCamera'),
            (None, 'Asian', 'Asian', 0.0, 1.0, 'noSetCamera'),
            ]),
        ]

def load(app):
    category = app.getCategory('Modelling2')

    gui3d.app.noSetCamera = (lambda: None)

    for type in [MacroTaskView, GenderTaskView, FaceTaskView, TorsoTaskView, ArmsLegsTaskView, AsymmTaskView]:
        taskview = category.addTask(type(category))
        if taskview._group is not None:
            app.addLoadHandler(taskview._group, taskview.loadHandler)
            app.addSaveHandler(taskview.saveHandler)

def unload(app):
    pass
