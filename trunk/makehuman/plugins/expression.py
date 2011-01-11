#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
from algos3d import loadTranslationTarget

print 'Expression imported'

class Action:

    def __init__(self, human, detail, before, after, postAction=None):
        self.name = 'Change expression'
        self.human = human
        self.detail = detail
        self.before = before
        self.after = after
        self.postAction = postAction

    def do(self):
        self.human.setDetail(self.detail, self.after)
        self.human.applyAllTargets()
        if self.postAction:
            self.postAction()
        return True

    def undo(self):
        self.human.setDetail(self.detail, self.before)
        self.human.applyAllTargets()
        if self.postAction:
            self.postAction()
        return True

class GroupBoxRadioButton(gui3d.RadioButton):
    def __init__(self, parent, group, y, label, groupBox, selected=False):
        gui3d.RadioButton.__init__(self, parent, group, width=112, height=20, position=[650, y, 9.1], selected=selected, label=label)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        gui3d.RadioButton.onClicked(self, event)
        self.parent.hideAllBoxes()
        self.groupBox.show()
        
class ExpressionSlider(gui3d.Slider):
    def __init__(self, parent, y, label, detail):
        human = parent.app.scene3d.selectedHuman
        gui3d.Slider.__init__(self, parent, position=[10, y, 9.1], value = human.getDetail(detail), label=label)
        self.detail = detail
        self.before = None
    
    def onChange(self, value):
        human = self.app.scene3d.selectedHuman
        self.app.do(Action(human, self.detail, self.before, value, self.update))
        self.before = None
        
    def onChanging(self, value):
        human = self.app.scene3d.selectedHuman
        if self.before is None:
            self.before = human.getDetail(self.detail)
        loadTranslationTarget(human.meshData, self.detail, -human.getDetail(self.detail), None, 0, 0)
        human.setDetail(self.detail, value)
        loadTranslationTarget(human.meshData, self.detail, value, None, 0, 0)
        #human.meshData.calcNormals(1, 1, human.headVertices, human.headFaces)
        human.meshData.update(human.headVertices)
        human.meshData.update(human.teethVertices)
        
    def update(self):
        human = self.app.scene3d.selectedHuman
        self.setValue(human.getDetail(self.detail))

class ExpressionTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Expression')


        human = self.app.scene3d.selectedHuman

        y = 80

        smile1 = gui3d.GroupBox(self, label = 'Smile1', position=[10, y, 9.0], width=128, height=320)
        smile2 = gui3d.GroupBox(self, label = 'Smile2', position=[10, y, 9.0], width=128, height=320)
        smile3 = gui3d.GroupBox(self, label = 'Smile3', position=[10, y, 9.0], width=128, height=320)
        smile4 = gui3d.GroupBox(self, label = 'Smile4', position=[10, y, 9.0], width=128, height=320)

        sadness1 = gui3d.GroupBox(self, label = 'Sadness1', position=[10, y, 9.0], width=128, height=320)
        sadness2 = gui3d.GroupBox(self, label = 'Sadness2', position=[10, y, 9.0], width=128, height=320)
        sadness3 = gui3d.GroupBox(self, label = 'Sadness3', position=[10, y, 9.0], width=128, height=320)
        sadness4 = gui3d.GroupBox(self, label = 'Sadness4', position=[10, y, 9.0], width=128, height=320)
        sadness5 = gui3d.GroupBox(self, label = 'Sadness5', position=[10, y, 9.0], width=128, height=320)

        relaxation1 = gui3d.GroupBox(self, label = 'Relaxation1', position=[10, y, 9.0], width=128, height=320)
        relaxation2 = gui3d.GroupBox(self, label = 'Relaxation2', position=[10, y, 9.0], width=128, height=320)

        surprise = gui3d.GroupBox(self, label = 'Surprise', position=[10, y, 9.0], width=128, height=320)

        anger1 = gui3d.GroupBox(self, label = 'Anger1', position=[10, y, 9.0], width=128, height=320)
        anger2 = gui3d.GroupBox(self, label = 'Anger2', position=[10, y, 9.0], width=128, height=320)
        anger3 = gui3d.GroupBox(self, label = 'Anger3', position=[10, y, 9.0], width=128, height=320)

        self.groupBoxes = [smile1,smile2,smile3,smile4,sadness1,sadness2,sadness3,sadness4,sadness5,relaxation1,relaxation2,surprise,anger1,anger2,anger3]

        self.radioButtons = []

        self.smile1RadioButton = GroupBoxRadioButton(self, self.radioButtons, y, 'Smile1', smile1, selected=True)
        self.smile2RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+22, 'Smile2', smile2)
        self.smile3RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+44, 'Smile3', smile3)
        self.smile4RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+66, 'Smile4', smile4)
        self.sadness1RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+88, 'Sadness1', sadness1)
        self.sadness2RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+110, 'Sadness2', sadness2)
        self.sadness3RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+132, 'Sadness3', sadness3)
        self.sadness4RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+154, 'Sadness4', sadness4)
        self.sadness5RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+176, 'Sadness5', sadness5)
        self.relaxation1RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+198, 'Relaxation1', relaxation1)
        self.relaxation2RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+220, 'Relaxation2', relaxation2)
        self.surpriseRadioButton = GroupBoxRadioButton(self, self.radioButtons, y+242, 'Surprise', surprise)
        self.anger1RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+264, 'Anger1', anger1)
        self.anger2RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+286, 'Anger2', anger2)
        self.anger3RadioButton = GroupBoxRadioButton(self, self.radioButtons, y+308, 'Anger3', anger3)


        self.smileSlider = ExpressionSlider(smile1, y+35, 'Smile', 'data/targets/expression/female_young/neutral_female_young_smile.target')
        self.hopefulSlider = ExpressionSlider(smile1, y+70, 'Hopeful', 'data/targets/expression/female_young/neutral_female_young_hopefull.target')
        self.innocentSlider = ExpressionSlider(smile1, y+105, 'Innocent', 'data/targets/expression/female_young/neutral_female_young_innocent.target')

        self.realsmileSlider = ExpressionSlider(smile2, y+35, 'Real Smile', 'data/targets/expression/female_young/neutral_female_young_smile.target')
        self.tenderSlider = ExpressionSlider(smile2, y+70, 'Tender', 'data/targets/expression/female_young/neutral_female_young_tender.target')
        self.seductiveSlider = ExpressionSlider(smile2, y+105, 'Seductive', 'data/targets/expression/female_young/neutral_female_young_seductive.target')

        self.grinSlider = ExpressionSlider(smile3, y+35, 'Grin', 'data/targets/expression/female_young/neutral_female_young_grin.target')
        self.excitedSlider = ExpressionSlider(smile3, y+70, 'Excited', 'data/targets/expression/female_young/neutral_female_young_excited.target')
        self.ecstaticSlider = ExpressionSlider(smile3, y+105, 'Ecstatic', 'data/targets/expression/female_young/neutral_female_young_ecstatic.target')

        self.proudSlider = ExpressionSlider(smile4, y+35, 'Proud', 'data/targets/expression/female_young/neutral_female_young_proud.target')
        self.pleasedSlider = ExpressionSlider(smile4, y+70, 'Pleased', 'data/targets/expression/female_young/neutral_female_young_pleased.target')
        self.amusedSlider = ExpressionSlider(smile4, y+105, 'Amused', 'data/targets/expression/female_young/neutral_female_young_amused.target')
        self.laughing1Slider = ExpressionSlider(smile4, y+140, 'laughing1', 'data/targets/expression/female_young/neutral_female_young_laughing1.target')
        self.laughing2Slider = ExpressionSlider(smile4, y+175, 'laughing2', 'data/targets/expression/female_young/neutral_female_young_laughing2.target')

        self.sosoSlider = ExpressionSlider(sadness1, y+35, 'So so', 'data/targets/expression/female_young/neutral_female_young_so-so.target')
        self.blueSlider = ExpressionSlider(sadness1, y+70, 'Blue', 'data/targets/expression/female_young/neutral_female_young_blue.target')
        self.depressedSlider = ExpressionSlider(sadness1, y+105, 'Depressed', 'data/targets/expression/female_young/neutral_female_young_depressed.target')

        self.sadSlider = ExpressionSlider(sadness2, y+35, 'Sad', 'data/targets/expression/female_young/neutral_female_young_sad.target')
        self.distressedSlider = ExpressionSlider(sadness2, y+70, 'Distressed', 'data/targets/expression/female_young/neutral_female_young_distressed.target')
        self.cryingSlider = ExpressionSlider(sadness2, y+105, 'Crying', 'data/targets/expression/female_young/neutral_female_young_crying.target')
        self.painSlider = ExpressionSlider(sadness2, y+140, 'Pain', 'data/targets/expression/female_young/neutral_female_young_pain.target')

        self.disappointedSlider = ExpressionSlider(sadness3, y+35, 'Disappointed', 'data/targets/expression/female_young/neutral_female_young_disappointed.target')
        self.frustratedSlider = ExpressionSlider(sadness3, y+70, 'Frustrated', 'data/targets/expression/female_young/neutral_female_young_frustrated.target')
        self.stressedSlider = ExpressionSlider(sadness3, y+105, 'Stressed', 'data/targets/expression/female_young/neutral_female_young_stressed.target')

        self.worriedSlider = ExpressionSlider(sadness4, y+35, 'Worried', 'data/targets/expression/female_young/neutral_female_young_worried.target')
        self.scaredSlider = ExpressionSlider(sadness4, y+70, 'Scared', 'data/targets/expression/female_young/neutral_female_young_scared.target')
        self.terrifiedSlider = ExpressionSlider(sadness4, y+105, 'Terrified', 'data/targets/expression/female_young/neutral_female_young_terrified.target')

        self.shySlider = ExpressionSlider(sadness5, y+35, 'Shy', 'data/targets/expression/female_young/neutral_female_young_shy.target')
        self.guiltySlider = ExpressionSlider(sadness5, y+70, 'Guilty', 'data/targets/expression/female_young/neutral_female_young_guilty.target')
        self.embarassedSlider = ExpressionSlider(sadness5, y+105, 'Embarassed', 'data/targets/expression/female_young/neutral_female_young_embarassed.target')

        self.relaxedSlider = ExpressionSlider(relaxation1, y+35, 'Relaxed', 'data/targets/expression/female_young/neutral_female_young_relaxed.target')
        self.peacefulSlider = ExpressionSlider(relaxation1, y+70, 'Peaceful', 'data/targets/expression/female_young/neutral_female_young_peaceful.target')
        self.refreshedSlider = ExpressionSlider(relaxation1, y+105, 'Refreshed', 'data/targets/expression/female_young/neutral_female_young_refreshed.target')
        self.pleasuredSlider = ExpressionSlider(relaxation1, y+140, 'Pleasured', 'data/targets/expression/female_young/neutral_female_young_pleased.target')

        self.lazySlider = ExpressionSlider(relaxation2, y+35, 'Lazy', 'data/targets/expression/female_young/neutral_female_young_lazy.target')
        self.boredSlider = ExpressionSlider(relaxation2, y+70, 'Bored', 'data/targets/expression/female_young/neutral_female_young_bored.target')
        self.tiredSlider = ExpressionSlider(relaxation2, y+105, 'Tired', 'data/targets/expression/female_young/neutral_female_young_tired.target')
        self.drainedSlider = ExpressionSlider(relaxation2, y+140, 'Drained', 'data/targets/expression/female_young/neutral_female_young_drained.target')
        self.sleepySlider = ExpressionSlider(relaxation2, y+175, 'Sleepy', 'data/targets/expression/female_young/neutral_female_young_sleepy.target')
        self.groggySlider = ExpressionSlider(relaxation2, y+210, 'Groggy', 'data/targets/expression/female_young/neutral_female_young_groggy.target')

        self.curiousSlider = ExpressionSlider(surprise, y+35, 'Curious', 'data/targets/expression/female_young/neutral_female_young_curious.target')
        self.surprisedSlider = ExpressionSlider(surprise, y+70, 'Surprised', 'data/targets/expression/female_young/neutral_female_young_surprised.target')
        self.impressedSlider = ExpressionSlider(surprise, y+105, 'Impressed', 'data/targets/expression/female_young/neutral_female_young_impressed.target')
        self.puzzledSlider = ExpressionSlider(surprise, y+140, 'Puzzled', 'data/targets/expression/female_young/neutral_female_young_puzzled.target')
        self.shockedSlider = ExpressionSlider(surprise, y+175, 'Shocked', 'data/targets/expression/female_young/neutral_female_young_shocked.target')

        self.frownSlider = ExpressionSlider(anger1, y+35, 'Frown', 'data/targets/expression/female_young/neutral_female_young_frown.target')
        self.upsetSlider = ExpressionSlider(anger1, y+70, 'Upset', 'data/targets/expression/female_young/neutral_female_young_upset.target')
        self.angrySlider = ExpressionSlider(anger1, y+105, 'Angry', 'data/targets/expression/female_young/neutral_female_young_angry.target')
        self.furiousSlider = ExpressionSlider(anger1, y+140, 'Furious', 'data/targets/expression/female_young/neutral_female_young_furious.target')
        self.enragedSlider = ExpressionSlider(anger1, y+175, 'Enraged', 'data/targets/expression/female_young/neutral_female_young_enraged.target')

        self.skepticalSlider = ExpressionSlider(anger2, y+35, 'Skeptical', 'data/targets/expression/female_young/neutral_female_young_skeptical.target')
        self.vindictiveSlider = ExpressionSlider(anger2, y+70, 'Vindictive', 'data/targets/expression/female_young/neutral_female_young_vindictive.target')
        self.poutSlider = ExpressionSlider(anger2, y+105, 'Pout', 'data/targets/expression/female_young/neutral_female_young_pout.target')
        self.furiousSlider = ExpressionSlider(anger2, y+140, 'Furious', 'data/targets/expression/female_young/neutral_female_young_furious.target')
        self.grumpySlider = ExpressionSlider(anger2, y+175, 'Grumpy', 'data/targets/expression/female_young/neutral_female_young_grumpy.target')

        self.arrogantSlider = ExpressionSlider(anger3, y+35, 'Arrogant', 'data/targets/expression/female_young/neutral_female_young_arrogant.target')
        self.sneeringSlider = ExpressionSlider(anger3, y+70, 'Sneering', 'data/targets/expression/female_young/neutral_female_young_sneering.target')
        self.haughtySlider = ExpressionSlider(anger3, y+105, 'Haughty', 'data/targets/expression/female_young/neutral_female_young_haughty.target')
        self.disgustedSlider = ExpressionSlider(anger3, y+140, 'Disgusted', 'data/targets/expression/female_young/neutral_female_young_disgusted.target')

        self.hideAllBoxes()
        smile1.show()
        
        def changeValue(self, IDName, value, realtime=False):
            """
            """

            self.setModifierValue(value, IDName)
            self.human.applyAllTargets(self.human.app.progress)

    def hideAllBoxes(self):
            for box in self.groupBoxes:
                box.hide()


category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Advanced')
    taskview = ExpressionTaskView(category)

    print 'Expression loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Expression unloaded'


