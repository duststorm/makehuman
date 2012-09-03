import os.path
#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import module3d
import os
import humanmodifier
import aljabr
import mh
import math

class MeasurementValueConverter(gui3d.ValueConverter):

    def __init__(self, task, measure, modifier):

        self.task = task
        self.measure = measure
        self.modifier = modifier
        self.value = 0.0

    def dataToDisplay(self, value):
        self.value = value
        return self.task.getMeasure(self.measure)

    def displayToData(self, value):
        goal = float(value)
        measure = self.task.getMeasure(self.measure)
        minValue = -1.0
        maxValue = 1.0
        if math.fabs(measure - goal) < 0.01:
            return self.value
        else:
            tries = 10
            while tries:
                if math.fabs(measure - goal) < 0.01:
                    break;
                if goal < measure:
                    maxValue = self.value
                    if value == minValue:
                        break
                    self.value = minValue + (self.value - minValue) / 2.0
                    self.modifier.updateValue(gui3d.app.selectedHuman, self.value, 0)
                    measure = self.task.getMeasure(self.measure)
                else:
                    minValue = self.value
                    if value == maxValue:
                        break
                    self.value = self.value + (maxValue - self.value) / 2.0
                    self.modifier.updateValue(gui3d.app.selectedHuman, self.value, 0)
                    measure = self.task.getMeasure(self.measure)
                tries -= 1
        return self.value

class GroupBoxRadioButton(gui3d.RadioButton):
    def __init__(self, group, label, groupBox, selected=False):
        gui3d.RadioButton.__init__(self, group, label, selected, style=gui3d.ButtonStyle)
        self.groupBox = groupBox

    def onClicked(self, event):
        gui3d.RadioButton.onClicked(self, event)
        self.parent.parent.hideAllBoxes()
        self.groupBox.show()
        self.groupBox.children[0].setFocus()

class MeasureSlider(humanmodifier.ModifierSlider):
    def __init__(self, label, task, measure, modifier):

        humanmodifier.ModifierSlider.__init__(self, value=0.0, min=-1.0, max=1.0,
            label=label, modifier=modifier, valueConverter=MeasurementValueConverter(task, measure, modifier))
        self.measure = measure

    def onChanging(self, value):
        humanmodifier.ModifierSlider.onChanging(self, value)
        self.updateLabel()

    def onChange(self, value):
        humanmodifier.ModifierSlider.onChange(self, value)
        self.parent.parent.syncSliderLabels()

    def onFocus(self, event):
        humanmodifier.ModifierSlider.onFocus(self, event)
        self.parent.parent.onSliderFocus()

    def onBlur(self, event):
        humanmodifier.ModifierSlider.onBlur(self, event)
        self.parent.parent.onSliderBlur()

    def updateLabel(self):
        #self.label.setText(self.template + self.parent.parent.getMeasure(self.measure))
        pass

    def update(self):
        humanmodifier.ModifierSlider.update(self)
        self.updateLabel()

class MeasureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Measure')

        self.ruler = Ruler()

        self.measureMesh = module3d.Object3D('measure', 2)
        self.measureMesh.uvValues = []
        self.measureMesh.indexBuffer = []

        fg = self.measureMesh.createFaceGroup('measure')

        count = max([len(vertIdx) for vertIdx in self.ruler.Measures.values()])

        v = [self.measureMesh.createVertex([0.0, 0.0, 0.0]) for i in xrange(count)]

        for i in xrange(count-1):
            fg.createFace((v[i], v[i+1]))

        self.measureMesh.setCameraProjection(1)
        self.measureMesh.setShadeless(1)
        self.measureMesh.setColor([255, 255, 255, 255])
        self.measureMesh.setPickable(0)
        self.measureMesh.updateIndexBuffer()

        self.measureObject = self.addObject(gui3d.Object([0, 0, 9], self.measureMesh))

        measurements = [
            ('neck', ['neckcirc', 'neckheight']),
            ('upperarm', ['upperarm', 'upperarmlenght']),
            ('lowerarm', ['lowerarmlenght', 'wrist']),
            ('torso', ['frontchest', 'bust', 'underbust', 'waist', 'napetowaist', 'waisttohip', 'shoulder']),
            ('hips', ['hips']),
            ('upperleg', ['upperlegheight', 'thighcirc']),
            ('lowerleg', ['lowerlegheight', 'calf']),
            ('ankle', ['ankle']),
        ]

        metric = gui3d.app.settings['units'] == 'metric'

        sliderLabel = {
            'neckcirc':'Neck circum: %.2f ' + 'cm' if metric else 'in',
            'neckheight':'Neck height: %.2f ' + 'cm' if metric else 'in',
            'upperarm':'Upper arm circum: %.2f ' + 'cm' if metric else 'in',
            'upperarmlenght':'Upperarm lenght: %.2f ' + 'cm' if metric else 'in',
            'lowerarmlenght':'Lowerarm lenght: %.2f ' + 'cm' if metric else 'in',
            'wrist':'Wrist circum: %.2f ' + 'cm' if metric else 'in',
            'frontchest':'Front chest dist: %.2f ' + 'cm' if metric else 'in',
            'bust':'Bust circum: %.2f ' + 'cm' if metric else 'in',
            'underbust':'Underbust circum: %.2f ' + 'cm' if metric else 'in',
            'waist':'Waist circum: %.2f ' + 'cm' if metric else 'in',
            'napetowaist':'Nape to waist: %.2f ' + 'cm' if metric else 'in',
            'waisttohip':'Waist to hip: %.2f ' + 'cm' if metric else 'in',
            'shoulder':'Shoulder dist: %.2f ' + 'cm' if metric else 'in',
            'hips':'Hips circum: %.2f ' + 'cm' if metric else 'in',
            'upperlegheight':'Upperleg height: %.2f ' + 'cm' if metric else 'in',
            'thighcirc':'Thigh circ.: %.2f ' + 'cm' if metric else 'in',
            'lowerlegheight':'Lowerleg height: %.2f ' + 'cm' if metric else 'in',
            'calf':'Calf circum: %.2f ' + 'cm' if metric else 'in',
            'ankle':'Ankle circum: %.2f ' + 'cm' if metric else 'in'
        }

        self.groupBoxes = {}
        self.radioButtons = []
        self.sliders = []

        self.modifiers = {}

        measureDataPath = "data/targets/measure/"

        y = 80
        self.categoryBox = self.addView(gui3d.GroupBox([650, y, 9.0], 'Category'));y += 25

        for name, subnames in measurements:
            # Create box
            box = self.addView(gui3d.GroupBox([10, 80, 9.0], name.capitalize(), gui3d.GroupBoxStyle._replace(height=25+36*len(subnames)+6)))
            self.groupBoxes[name] = box

            # Create radiobutton
            radio = self.categoryBox.addView(GroupBoxRadioButton(self.radioButtons, name.capitalize(), box, selected=len(self.radioButtons) == 0));y += 24

            # Create sliders
            for subname in subnames:
                modifier = humanmodifier.Modifier(
                    os.path.join(measureDataPath, "measure-%s-decrease.target" % subname),
                    os.path.join(measureDataPath, "measure-%s-increase.target" % subname))
                self.modifiers[subname] = modifier
                slider = box.addView(MeasureSlider(sliderLabel[subname], self, subname, modifier))
                self.sliders.append(slider)

        y+=16
        self.statsBox = self.addView(gui3d.GroupBox([650, y, 9.0], 'Statistics'));y += 25
        self.height = self.statsBox.addView(gui3d.TextView('Height: '));y += 20
        self.chest = self.statsBox.addView(gui3d.TextView('Chest: '));y += 20
        self.waist = self.statsBox.addView(gui3d.TextView('Waist: '));y += 20
        self.hips = self.statsBox.addView(gui3d.TextView('Hips: '));y += 20
        y+=16
        self.braBox = self.addView(gui3d.GroupBox([650, y, 9.0], 'Brassiere size'));y += 25
        self.eu = self.braBox.addView(gui3d.TextView('EU: '));y += 20
        self.jp = self.braBox.addView(gui3d.TextView('JP: '));y += 20
        self.us = self.braBox.addView(gui3d.TextView('US: '));y += 20
        self.uk = self.braBox.addView(gui3d.TextView('UK: '));y += 20
        y+=16

    def getMeasure(self, measure):

        human = gui3d.app.selectedHuman
        measure = self.ruler.getMeasure(human, measure, gui3d.app.settings['units'])
        #if gui3d.app.settings['units'] == 'metric':
        #    return '%.1f cm' % measure
        #else:
        #    return '%.1f in' % measure
        return measure

    def hideAllBoxes(self):

        for box in self.groupBoxes.values():
            box.hide()

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        self.groupBoxes['neck'].children[0].setFocus()
        self.syncSliders()

    def onResized(self, event):

        self.categoryBox.setPosition([event.width - 150, self.categoryBox.getPosition()[1], 9.0])
        self.statsBox.setPosition([event.width - 150, self.statsBox.getPosition()[1], 9.0])
        self.braBox.setPosition([event.width - 150, self.braBox.getPosition()[1], 9.0])

    def onSliderFocus(self):

        self.updateMeshes()
        self.measureObject.show()

    def onSliderBlur(self):

        self.measureObject.hide()

    def updateMeshes(self):

        human = gui3d.app.selectedHuman
        slider = gui3d.app.focusView

        if (isinstance(slider, MeasureSlider)):

            """
            # InfluenceMesh
            # Force caching of vert indices if they don't exist yet
            if not slider.modifier.verts:
                slider.modifier.updateValue(human, slider.modifier.getValue(human), 0)

            vmin, vmax = aljabr.calcBBox([human.mesh.verts[i] for i in slider.modifier.verts])

            box = [
                vmin,
                [vmax[0], vmin[1], vmin[2]],
                [vmax[0], vmax[1], vmin[2]],
                [vmin[0], vmax[1], vmin[2]],
                [vmin[0], vmin[1], vmax[2]],
                [vmax[0], vmin[1], vmax[2]],
                vmax,
                [vmin[0], vmax[1], vmax[2]]
            ]

            for i, v in enumerate(box):
                box[i] = gui3d.app.modelCamera.convertToScreen(v[0], v[1], v[2], human.mesh.object3d)

            x1, y1, x2, y2 = min([v[0] for v in box]), min([v[1] for v in box]), max([v[0] for v in box]), max([v[1] for v in box])

            self.influenceMesh.setPosition([x1, y1, 8.9])
            self.influenceMesh.mesh.resize(x2 - x1, y2 - y1)
            """

            # MeasureMesh
            vertidx = self.ruler.Measures[slider.measure]
            for i, j in enumerate(vertidx):
                # From hdusel in regard of issue 183: As agreed with marc I'll change the
                # call from packed to discrete because packed structs
                # are not available on Python 2.6.1 which is mandatory for MakeHuman to run
                # on OS X 10.5.x
                #
                # self.measureMesh.verts[i].co = gui3d.app.modelCamera.convertToScreen(*human.mesh.verts[j].co, obj=human.mesh.object3d)
                #
                self.measureMesh.verts[i].co = gui3d.app.modelCamera.convertToScreen(human.mesh.verts[j].co[0], human.mesh.verts[j].co[1], human.mesh.verts[j].co[2], obj=human.mesh.object3d)
                self.measureMesh.verts[i].co[2] = 0.0
            for i in xrange(len(vertidx), len(self.measureMesh.verts)):
                self.measureMesh.verts[i].co = self.measureMesh.verts[len(vertidx)-1].co[:]

            self.measureMesh.update()

    def onHumanChanged(self, event):

        self.updateMeshes()

    def onHumanTranslated(self, event):

        self.updateMeshes()

    def onHumanRotated(self, event):

        self.updateMeshes()

    def onCameraChanged(self, event):

        self.updateMeshes()

    def hideAllSliders(self):
        for group in self.groupBoxes.itervalues():
            group.hide()

    def syncSliders(self):

        for slider in self.sliders:
            slider.update()

        self.syncStatistics()
        self.syncBraSizes()

    def syncSliderLabels(self):

        for slider in self.sliders:
            slider.updateLabel()

        self.syncStatistics()
        self.syncBraSizes()

    def syncStatistics(self):

        human = gui3d.app.selectedHuman

        height = 10 * max(human.meshData.verts[8223].co[1] - human.meshData.verts[12361].co[1], human.meshData.verts[8223].co[1] - human.meshData.verts[13155].co[1])
        if gui3d.app.settings['units'] == 'metric':
            height = '%.2f cm' % height
        else:
            height = '%.2f in' % (height * 0.393700787)

        self.height.setTextFormat('Height: %s', height)
        self.chest.setTextFormat('Chest: %s', self.getMeasure('bust'))
        self.waist.setTextFormat('Waist: %s', self.getMeasure('waist'))
        self.hips.setTextFormat('Hips: %s', self.getMeasure('hips'))

    def syncBraSizes(self):

        human = gui3d.app.selectedHuman

        bust = self.ruler.getMeasure(human, 'bust', 'metric')
        underbust = self.ruler.getMeasure(human, 'underbust', 'metric')

        eucups = ['AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

        mod = int(underbust)%5
        band = underbust - mod if mod < 2.5 else underbust - mod + 5
        cup = max(0, int(round(((bust - underbust - 10) / 2))))
        self.eu.setText('EU: %d%s' % (band, eucups[cup]))

        jpcups = ['AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

        mod = int(underbust)%5
        band = underbust - mod if mod < 2.5 else underbust - mod + 5
        cup = max(0, int(round(((bust - underbust - 5) / 2.5))))
        self.jp.setText('JP: %d%s' % (band, jpcups[cup]))

        uscups = ['AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

        band = underbust * 0.393700787
        band = band + 5 if int(band)%2 else band + 4
        cup = max(0, int(round((bust - underbust - 10) / 2)))
        self.us.setText('US: %d%s' % (band, uscups[cup]))

        ukcups = ['AA', 'A', 'B', 'C', 'D', 'DD', 'E', 'F', 'FF', 'G', 'GG', 'H']

        self.uk.setText('UK: %d%s' % (band, ukcups[cup]))

    def loadHandler(self, human, values):

        modifier = self.modifiers.get(values[1], None)
        if modifier:
            modifier.setValue(human, float(values[2]))

    def saveHandler(self, human, file):

        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('measure %s %f\n' % (name, value))

def load(app):
    """
    Plugin load function, needed by design.
    """
    category = app.getCategory('Modelling')
    taskview = category.addView(MeasureTaskView(category))

    app.addLoadHandler('measure', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    print 'Measurement loaded'

    @taskview.event
    def onMouseDown(event):
        part = app.scene3d.getSelectedFacesGroup()
        bodyZone = app.selectedHuman.getPartNameForGroupName(part.name)
        print bodyZone
        if bodyZone in app.selectedHuman.bodyZones:
            if bodyZone == "neck":
                taskview.hideAllSliders()
                taskview.groupBoxes['neck'].show()
                taskview.groupBoxes['neck'].children[0].setFocus()
            elif (bodyZone == "r-upperarm") or (bodyZone == "l-upperarm"):
                taskview.hideAllSliders()
                taskview.groupBoxes['upperarm'].show()
                taskview.groupBoxes['upperarm'].children[0].setFocus()
            elif (bodyZone == "r-lowerarm") or (bodyZone == "l-lowerarm"):
                taskview.hideAllSliders()
                taskview.groupBoxes['lowerarm'].show()
                taskview.groupBoxes['lowerarm'].children[0].setFocus()
            elif (bodyZone == "torso") or (bodyZone == "pelvis"):
                taskview.hideAllSliders()
                taskview.groupBoxes['torso'].show()
                taskview.groupBoxes['torso'].children[0].setFocus()
            elif bodyZone == "hip":
                taskview.hideAllSliders()
                taskview.groupBoxes['hips'].show()
                taskview.groupBoxes['hips'].children[0].setFocus()
            elif (bodyZone == "l-upperleg") or (bodyZone == "r-upperleg"):
                taskview.hideAllSliders()
                taskview.groupBoxes['upperleg'].show()
                taskview.groupBoxes['upperleg'].children[0].setFocus()
            elif (bodyZone == "l-lowerleg") or (bodyZone == "r-lowerleg"):
                taskview.hideAllSliders()
                taskview.groupBoxes['lowerleg'].show()
                taskview.groupBoxes['lowerleg'].children[0].setFocus()
            elif (bodyZone == "l-foot") or (bodyZone == "r-foot"):
                taskview.hideAllSliders()
                taskview.groupBoxes['ankle'].show()
                taskview.groupBoxes['ankle'].children[0].setFocus()
            else:
                taskview.hideAllSliders()

    taskview.hideAllSliders()
    taskview.groupBoxes['neck'].show()

def unload(app):
    print 'Measurement unloaded'

class Ruler:

    """
  This class contains ...
  """

    def __init__(self):

    # these are tables of vertex indices for each body measurement of interest

        self.Measures = {}
        self.Measures['thighcirc'] = [7066,7205,7204,7192,7179,7176,7166,6886,7172,6813,7173,7101,7033,7032,7041,7232,7076,7062,7063,7229,7066]
        self.Measures['neckcirc'] = [3131,3236,3058,3059,2868,2865,3055,3137,5867,2857,3483,2856,3382,2916,2915,3417,8186,10347,10786,
                                    10785,10373,10818,10288,10817,9674,10611,10809,10806,10674,10675,10515,10614,3131]
        self.Measures['neckheight'] = [8184,8185,8186,8187,7463]
        self.Measures['upperarm']=[10701,10700,10699,10678,10337,10334,10333,10330,10280,10331,10702,10708,9671,10709,10329,10328,10701]
        self.Measures['wrist']=[9894,9895,9607,9606,9806,10512,10557,9807,9808,9809,9810,10565,9653,9682,9681,9832,10507,9894]
        self.Measures['frontchest']=[2961,10764]
        self.Measures['bust']=[6908,3559,3537,3556,3567,3557,4178,3558,4193,3561,3566,3565,3718,3563,2644,4185,2554,4169,2553,3574,2634,2653,3466,3392,
                2942,3387,4146,4433,2613,10997,9994,10078,10368,10364,10303,10380,10957,10976,10218,11055,10060,11054,10044,10966,10229,10115,
                10227,10226,10231,10036,10234,10051,10235,10225,10236,10255,10233,6908]
        self.Measures['napetowaist']=[7463,7472]
        self.Measures['waisttohip']=[4681,6575]
        self.Measures['shoulder'] = [10819,10816,10021,10821,10822,10693,10697]
        self.Measures['underbust'] = [7245,3583,6580,3582,3705,3581,3411,3401,3467,4145,2612,10998,10080,10302,10366,10356,10352,10362,10361,10350,10260,10349,7259,7245]
        self.Measures['waist'] = [6853,4682,3529,2950,3702,3594,3405,5689,3587,4466,6898,9968,10086,9970,10359,10197,10198,10130,10771,10263,6855,6853]
        self.Measures['upperlegheight'] = [6755,7026]
        self.Measures['lowerlegheight'] = [6866,13338]
        self.Measures['calf'] = [7141,7142,7137,6994,6989,6988,6995,6997,6774,6775,6999,6803,6974,6972,6971,7002,7140,7139,7141]
        self.Measures['ankle'] = [6938,6937,6944,6943,6948,6784,6935,6766,6767,6954,6799,6955,6958,6949,6952,6941,6938]
        self.Measures['upperarmlenght'] = [9945,10696]
        self.Measures['lowerarmlenght'] = [9696,9945]
        self.Measures['hips'] = [7298,2936,3527,2939,2940,3816,3817,3821,4487,3822,3823,3913,3915,4506,5688,4505,4504,4503,6858,6862,6861,6860,
                                            6785,6859,7094,7096,7188,7189,6878,7190,7194,7195,7294,7295,7247,7300,7298]

    def getMeasure(self, human, measurementname, mode):
        measure = 0
        vindex1 = self.Measures[measurementname][0]
        for vindex2 in self.Measures[measurementname]:
            measure += aljabr.vdist(human.meshData.verts[vindex1].co, human.meshData.verts[vindex2].co)
            vindex1 = vindex2

        if mode == 'metric':
            return 10.0 * measure
        else:
            return 10.0 * measure * 0.393700787






