#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import aljabr
import humanmodifier
import mh


class MeasurementTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Example', category.app.getThemeResource('images', 'button_measure.png'), category.app.getThemeResource('images',
                                'button_measure_on.png'))
        gui3d.Object(self, 'data/3dobjs/background.obj', position=[400, 300, -89.98])
        self.measureList = gui3d.TextView(self, mesh='data/3dobjs/empty.obj', position=[10, 100, 9.4])
        self.measureList.setText('')

        human = self.app.scene3d.selectedHuman
        self.waistModifier = humanmodifier.Modifier(human, 'data/targets/details/hip_underweight.target', 'data/targets/details/hip_overweight.target')
        self.heightModifier = humanmodifier.Modifier(human, 'data/targets/macrodetails/universal-stature-dwarf.target',
                                                     'data/targets/macrodetails/universal-stature-giant.target')

        # Height

        self.statureSlider = gui3d.Slider(self, position=[10, 220, 8.04], value=0.0, min=-1.0, max=1.0, label='Stature')  # We want the slider to start from the middle

        @self.statureSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman
            before = {}
            before['data/targets/macrodetails/universal-stature-dwarf.target'] = human.getDetail('data/targets/macrodetails/universal-stature-dwarf.target')
            before['data/targets/macrodetails/universal-stature-giant.target'] = human.getDetail('data/targets/macrodetails/universal-stature-giant.target')
            self.heightModifier.setValue(value)
            after = {}
            after['data/targets/macrodetails/universal-stature-dwarf.target'] = human.getDetail('data/targets/macrodetails/universal-stature-dwarf.target')
            after['data/targets/macrodetails/universal-stature-giant.target'] = human.getDetail('data/targets/macrodetails/universal-stature-giant.target')
            self.app.did(humanmodifier.Action(human, before, after, self.syncSliders))
            human.applyAllTargets(self.app.progress)
            self.measureList.setText(self.ruler.getMeasurementsString())

        self.ruler = Ruler(category.app.scene3d.selectedHuman)
        self.measureList.setText(self.ruler.getMeasurementsString())

        # Chest

        self.chestGirthSlider = self.chestGirthSlider = gui3d.Slider(self, position=[10, 270, 8.04], value=0.0, min=-1.0, max=1.0, label='Chest')  # We want the slider to start from the middle

        # self.chestGirthLabel = gui3d.TextView(self,
        #    mesh="data/3dobjs/empty.obj",
        #    position=[10, 290, 8.04])

        @self.chestGirthSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman

            # self.chestGirthLabel.setText("Value is %f" % (value))

            modifier = humanmodifier.Modifier(human, 'data/targets/details/torso-scale-horiz-decr.target', 'data/targets/details/torso-scale-horiz-incr.target')
            modifier.setValue(value)
            modifier = humanmodifier.Modifier(human, 'data/targets/details/torso-scale-depth-decr.target', 'data/targets/details/torso-scale-depth-incr.target')
            modifier.setValue(value)
            human.applyAllTargets(self.app.progress)
            self.measureList.setText(self.ruler.getMeasurementsString())

        # Waist

        self.waistGirthSlider = gui3d.Slider(self, position=[10, 320, 9.04], value=0.0, min=-1.0, max=1.0, label='Waist')  # We want the slider to start from the middle

        # self.waistGirthLabel = gui3d.TextView(self,
        #    mesh="data/3dobjs/empty.obj",
        #    position=[10, 390, 8.04])
        # self.waistGirthLabel.setText("Value is 0.5")

        @self.waistGirthSlider.event
        def onChange(value):
            human = self.app.scene3d.selectedHuman

            # self.chestGirthLabel.setText("Value is %f" % (value))

            self.waistModifier.setValue(value)
            human.applyAllTargets(self.app.progress)
            self.measureList.setText(self.ruler.getMeasurementsString())

        # Hips

        self.hipGirthSlider = gui3d.Slider(self, position=[10, 370, 9.04], value=0.0, min=-1.0, max=1.0, label='Hip')  #  We want the slider to start from the middle

        @self.hipGirthSlider.event
        def onChange(value):

            # self.hipGirthLabel.setText("Value is %f" % (value))

            human = self.app.scene3d.selectedHuman

            # self.chestGirthLabel.setText("Value is %f" % (value))

            modifier = humanmodifier.Modifier(human, 'data/targets/details/pelvis_underweight.target', 'data/targets/details/pelvis_overweight.target')
            modifier.setValue(value)
            modifier = humanmodifier.Modifier(human, 'data/targets/details/r-upperleg_underweight.target', 'data/targets/details/r-upperleg_overweight.target')
            modifier.setValue(value)
            modifier = humanmodifier.Modifier(human, 'data/targets/details/l-upperleg_underweight.target', 'data/targets/details/l-upperleg_overweight.target')
            modifier.setValue(value)
            human.applyAllTargets(self.app.progress)
            self.measureList.setText(self.ruler.getMeasurementsString())

        # self.hipGirthLabel = gui3d.TextView(self,
        #    mesh="data/3dobjs/empty.obj",
        #    position=[10, 490, 8.04])
        # self.hipGirthLabel.setText("Value is 0.5")

    def onShow(self, event):

    # When the task gets shown, set the focus to the file entry

        gui3d.TaskView.onShow(self, event)
        self.measureList.setText(self.ruler.getMeasurementsString())
        self.syncSliders()

    def syncSliders(self):
        human = self.app.scene3d.selectedHuman
        self.waistGirthSlider.setValue(self.waistModifier.getValue())
        self.statureSlider.setValue(self.heightModifier.getValue())


# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = gui3d.Category(app, 'Measurement', app.getThemeResource('images', 'button_measure.png'), app.getThemeResource('images', 'button_measure_on.png'))
    taskview = MeasurementTaskView(category)

  # Zoom the camera

    @taskview.event
    def onMouseWheel(event):
        if event.wheelDelta > 0:
            mh.cameras[0].eyeZ -= 0.65
            app.scene3d.redraw()
        else:
            mh.cameras[0].eyeZ += 0.65
            app.scene3d.redraw()

    @taskview.event
    def onMouseDragged(event):
        diff = app.scene3d.getMouseDiff()
        leftButtonDown = event.button & 1
        middleButtonDown = event.button & 2
        rightButtonDown = event.button & 4

        if leftButtonDown and rightButtonDown or middleButtonDown:
            mh.cameras[0].eyeZ += 0.05 * diff[1]
        elif leftButtonDown:
            human = app.scene3d.selectedHuman
            rot = human.getRotation()
            rot[0] += 0.5 * diff[1]
            rot[1] += 0.5 * diff[0]
            human.setRotation(rot)
        elif rightButtonDown:
            human = app.scene3d.selectedHuman
            trans = human.getPosition()
            trans[0] += 0.1 * diff[0]
            trans[1] -= 0.1 * diff[1]
            human.setPosition(trans)


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print ''


class Ruler:

    """
  This class contains ...
  """

    def __init__(self, human):

    # these are tables of vertex indices for each body measurement of interest

        self.Distances = {'NeckHeight': [1244, 7577], 'ChestWidth': [1120, 7167], 'UnderBustWidth': [8829, 5488], 'AbdomenWidth': [8802, 5461], 'HipsWidth': [9041,
                          5700], 'MidThightWidth': [9035, 1140]}
        self.Measures = {'Chest': [2553, 3574, 2634, 3466, 4148, 4435, 3600, 10192, 9992, 10077, 10305, 10303, 10957, 10976, 10218, 11055, 10060, 11054, 10044, 10115,
                         3718, 2644, 4185, 2554, 4169], 'Waist': [2906, 3528, 2949, 3700, 3397, 3404, 3403, 3402, 5675, 4460, 4139, 4466, 4467, 4468, 6897, 9967, 9968,
                         10086, 10205, 9969, 9791, 7266, 7265, 7264, 7267, 7242, 7290, 7246, 7314], 'Hips': [7298, 2936, 3816, 3817, 3821, 4487, 3822, 3823, 3913, 3915,
                         4506, 5688, 4505, 6860, 6785, 6859, 7094, 7096, 7188, 7189, 6878, 7190, 7194, 7247, 7300], 'Stature': [8224, 13675]}

        self.humanoid = human

    def getDistance(self, distancename):
        return 10.0 * aljabr.vdist(self.humanoid.mesh.verts[self.Distances[distancename][0]].co, self.humanoid.mesh.verts[self.Distances[distancename][1]].co)

    def getMeasure(self, measurementname):
        measure = 0
        vindex1 = self.Measures[measurementname][0]
        for vindex2 in self.Measures[measurementname]:
            measure += aljabr.vdist(self.humanoid.mesh.verts[vindex1].co, self.humanoid.mesh.verts[vindex2].co)
            vindex1 = vindex2
        return 10.0 * measure

    def getMeasurementsString(self):
        measuretext = ''

#    for key in self.Distances:
#      measuretext += key
#      measuretext += ": %.1f cm \n" % self.getDistance(key)
#    measuretext += " \n"

        for key in self.Measures:
            measuretext += key
            measuretext += ': %.1f cm \n' % self.getMeasure(key)
            measuretext += ' \n'
        return measuretext


# for example setDetail("data/targets/details/torso-scale-horiz-incr.target", 1.0)?
