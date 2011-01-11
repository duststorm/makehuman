#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d

print 'example imported'

class GroupBoxRadioButton(gui3d.RadioButton):
    def __init__(self, parent, group, y, label, groupBox, selected=False):
        gui3d.RadioButton.__init__(self, parent, group, width=112, height=20, position=[650, y, 9.1], selected=selected, label=label)
        self.groupBox = groupBox
        
    def onClicked(self, event):
        gui3d.RadioButton.onClicked(self, event)
        self.parent.hideAllBoxes()
        self.groupBox.show()

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


        self.smileSlider = gui3d.Slider(smile1, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_smile.target'), label='Smile')
        self.hopefulSlider = gui3d.Slider(smile1, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_hopefull.target'), label='Smile')
        self.innocentSlider = gui3d.Slider(smile1, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_innocent.target'), label='Innocent')

        self.realsmileSlider = gui3d.Slider(smile2, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_smile.target'), label='Real Smile')
        self.tenderSlider = gui3d.Slider(smile2, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_hopeful.target'), label='Tender')
        self.seductiveSlider = gui3d.Slider(smile2, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_seductive.target'), label='Seductive')

        self.grinSlider = gui3d.Slider(smile3, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_grin.target'), label='Grin')
        self.excitedSlider = gui3d.Slider(smile3, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_excited.target'), label='Excited')
        self.ecstaticSlider = gui3d.Slider(smile3, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_ecstatic.target'), label='Ecstatic')

        self.proudSlider = gui3d.Slider(smile4, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_proud.target'), label='Proud')
        self.pleasedSlider = gui3d.Slider(smile4, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_pleased.target'), label='Pleased')
        self.amusedSlider = gui3d.Slider(smile4, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_amused.target'), label='Amused')
        self.laughing1Slider = gui3d.Slider(smile4, position=[10, y+140, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_laughing1.target'), label='laughing1')
        self.laughing2Slider = gui3d.Slider(smile4, position=[10, y+175, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_laughing2.target'), label='laughing2')

        self.sosoSlider = gui3d.Slider(sadness1, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_so-so.target'), label='So so')
        self.blueSlider = gui3d.Slider(sadness1, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_blue.target'), label='Blue')
        self.depressedSlider = gui3d.Slider(sadness1, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_depressed.target'), label='Depressed')

        self.sadSlider = gui3d.Slider(sadness2, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_sad.target'), label='Sad')
        self.distressedSlider = gui3d.Slider(sadness2, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_distressed.target'), label='Distressed')
        self.cryingSlider = gui3d.Slider(sadness2, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_crying.target'), label='Crying')
        self.painSlider = gui3d.Slider(sadness2, position=[10, y+140, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_pain.target'), label='Pain')

        self.disappointedSlider = gui3d.Slider(sadness3, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_disappointed.target'), label='Disappointed')
        self.frustratedSlider = gui3d.Slider(sadness3, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_frustrated.target'), label='Frustrated')
        self.stressedSlider = gui3d.Slider(sadness3, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_stressed.target'), label='Stressed')

        self.worriedSlider = gui3d.Slider(sadness4, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_worried.target'), label='Worried')
        self.scaredSlider = gui3d.Slider(sadness4, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_scared.target'), label='Scared')
        self.terrifiedSlider = gui3d.Slider(sadness4, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_terrified.target'), label='Terrified')

        self.shySlider = gui3d.Slider(sadness5, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_shy.target'), label='Shy')
        self.guiltySlider = gui3d.Slider(sadness5, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_guilty.target'), label='Guilty')
        self.embarassedSlider = gui3d.Slider(sadness5, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_embarassed.target'), label='Embarassed')

        self.relaxedSlider = gui3d.Slider(relaxation1, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_relaxed.target'), label='Relaxed')
        self.peacefulSlider = gui3d.Slider(relaxation1, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_peaceful.target'), label='Peaceful')
        self.refreshedSlider = gui3d.Slider(relaxation1, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_refreshed.target'), label='Refreshed')
        self.pleasuredSlider = gui3d.Slider(relaxation1, position=[10, y+140, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_pleased.target'), label='Pleasured')

        self.lazySlider = gui3d.Slider(relaxation2, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_lazy.target'), label='Lazy')
        self.boredSlider = gui3d.Slider(relaxation2, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_bored.target'), label='Bored')
        self.tiredSlider = gui3d.Slider(relaxation2, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_tired.target'), label='Tired')
        self.drainedSlider = gui3d.Slider(relaxation2, position=[10, y+140, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_drained.target'), label='Drained')
        self.sleepySlider = gui3d.Slider(relaxation2, position=[10, y+175, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_sleepy.target'), label='Sleepy')
        self.groggySlider = gui3d.Slider(relaxation2, position=[10, y+210, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_groggy.target'), label='Groggy')

        self.curiousSlider = gui3d.Slider(surprise, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_curious.target'), label='Curious')
        self.surprisedSlider = gui3d.Slider(surprise, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_surprised.target'), label='Surprised')
        self.impressedSlider = gui3d.Slider(surprise, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_impressed.target'), label='Impressed')
        self.puzzledSlider = gui3d.Slider(surprise, position=[10, y+140, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_puzzled.target'), label='Puzzled')
        self.shockedSlider = gui3d.Slider(surprise, position=[10, y+175, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_shocked.target'), label='Shocked')

        self.frownSlider = gui3d.Slider(anger1, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_frown.target'), label='Frown')
        self.upsetSlider = gui3d.Slider(anger1, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_upset.target'), label='Upset')
        self.angrySlider = gui3d.Slider(anger1, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_angry.target'), label='Angry')
        self.furiousSlider = gui3d.Slider(anger1, position=[10, y+140, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_furious.target'), label='Furious')
        self.enragedSlider = gui3d.Slider(anger1, position=[10, y+175, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_enraged.target'), label='Enraged')

        self.skepticalSlider = gui3d.Slider(anger2, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_skeptical.target'), label='Skeptical')
        self.vindictiveSlider = gui3d.Slider(anger2, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_vindictive.target'), label='Vindictive')
        self.poutSlider = gui3d.Slider(anger2, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_pout.target'), label='Pout')
        self.furiousSlider = gui3d.Slider(anger2, position=[10, y+140, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_furious.target'), label='Furious')
        self.grumpySlider = gui3d.Slider(anger2, position=[10, y+175, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_grumpy.target'), label='Grumpy')

        self.arrogantSlider = gui3d.Slider(anger3, position=[10, y+35, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_arrogant.target'), label='Arrogant')
        self.sneeringSlider = gui3d.Slider(anger3, position=[10, y+70, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_sneering.target'), label='Sneering')
        self.haughtySlider = gui3d.Slider(anger3, position=[10, y+105, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_haughty.target'), label='Haughty')
        self.disgustedSlider = gui3d.Slider(anger3, position=[10, y+140, 9.1], value = human.getDetail('data/targets/expression/female_young/neutral_female_young_disgusted.target'), label='Disgusted')

        self.hideAllBoxes()
        smile1.show()


        @self.disappointedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_disappointed.target', value)
            human.applyAllTargets(self.app.progress)

        @self.frustratedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_frustrated.target', value)
            human.applyAllTargets(self.app.progress)

        @self.stressedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_stressed.target', value)
            human.applyAllTargets(self.app.progress)


        @self.worriedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_worried.target', value)
            human.applyAllTargets(self.app.progress)

        @self.scaredSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_scared.target', value)
            human.applyAllTargets(self.app.progress)

        @self.terrifiedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_terrified.target', value)
            human.applyAllTargets(self.app.progress)

        @self.shySlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_shy.target', value)
            human.applyAllTargets(self.app.progress)

        @self.guiltySlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_guilty.target', value)
            human.applyAllTargets(self.app.progress)

        @self.embarassedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_embarassed.target', value)
            human.applyAllTargets(self.app.progress)

        @self.relaxedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_relaxed.target', value)
            human.applyAllTargets(self.app.progress)

        @self.peacefulSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_peaceful.target', value)
            human.applyAllTargets(self.app.progress)

        @self.refreshedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_refreshed.target', value)
            human.applyAllTargets(self.app.progress)

        @self.pleasuredSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_pleased.target', value)
            human.applyAllTargets(self.app.progress)

        @self.lazySlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_lazy.target', value)
            human.applyAllTargets(self.app.progress)

        @self.boredSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_bored.target', value)
            human.applyAllTargets(self.app.progress)

        @self.tiredSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_tired.target', value)
            human.applyAllTargets(self.app.progress)

        @self.drainedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_drained.target', value)
            human.applyAllTargets(self.app.progress)

        @self.sleepySlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_sleepy.target', value)
            human.applyAllTargets(self.app.progress)

        @self.groggySlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_groggy.target', value)
            human.applyAllTargets(self.app.progress)

        @self.curiousSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_curious.target', value)
            human.applyAllTargets(self.app.progress)

        @self.surprisedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_surprised.target', value)
            human.applyAllTargets(self.app.progress)

        @self.impressedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_impressed.target', value)
            human.applyAllTargets(self.app.progress)

        @self.puzzledSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_puzzled.target', value)
            human.applyAllTargets(self.app.progress)

        @self.shockedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_shocked.target', value)
            human.applyAllTargets(self.app.progress)

        @self.skepticalSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_skeptical.target', value)
            human.applyAllTargets(self.app.progress)

        @self.vindictiveSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_vindictive.target', value)
            human.applyAllTargets(self.app.progress)

        @self.poutSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_pout.target', value)
            human.applyAllTargets(self.app.progress)

        @self.grumpySlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_grumpy.target', value)
            human.applyAllTargets(self.app.progress)

        @self.arrogantSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_arrogant.target', value)
            human.applyAllTargets(self.app.progress)

        @self.sneeringSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_sneering.target', value)
            human.applyAllTargets(self.app.progress)

        @self.haughtySlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_haughty.target', value)
            human.applyAllTargets(self.app.progress)

        @self.disgustedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_disgusted.target', value)
            human.applyAllTargets(self.app.progress)

        @self.worriedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_worried.target', value)
            human.applyAllTargets(self.app.progress)

        @self.scaredSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_scared.target', value)
            human.applyAllTargets(self.app.progress)

        @self.terrifiedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_terrified.target', value)
            human.applyAllTargets(self.app.progress)

        @self.sadSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_sad.target', value)
            human.applyAllTargets(self.app.progress)

        @self.distressedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_distressed.target', value)
            human.applyAllTargets(self.app.progress)

        @self.cryingSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_crying.target', value)
            human.applyAllTargets(self.app.progress)

        @self.painSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_pain.target', value)
            human.applyAllTargets(self.app.progress)

        @self.sadSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_sad.target', value)
            human.applyAllTargets(self.app.progress)

        @self.distressedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_distressed.target', value)
            human.applyAllTargets(self.app.progress)

        @self.cryingSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_crying.target', value)
            human.applyAllTargets(self.app.progress)

        @self.painSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_pain.target', value)
            human.applyAllTargets(self.app.progress)

        @self.sosoSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_so-so.target', value)
            human.applyAllTargets(self.app.progress)

        @self.blueSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_blue.target', value)
            human.applyAllTargets(self.app.progress)

        @self.depressedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_depressed.target', value)
            human.applyAllTargets(self.app.progress)

        @self.smileSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_smile.target', value)
            human.applyAllTargets(self.app.progress)

        @self.innocentSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_innocent.target', value)
            human.applyAllTargets(self.app.progress)

        @self.realsmileSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_realsmile.target', value)
            human.applyAllTargets(self.app.progress)

        @self.seductiveSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_seductive.target', value)
            human.applyAllTargets(self.app.progress)

        @self.grinSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_grin.target', value)
            human.applyAllTargets(self.app.progress)

        @self.excitedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_excited.target', value)
            human.applyAllTargets(self.app.progress)

        @self.ecstaticSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_ecstatic.target', value)
            human.applyAllTargets(self.app.progress)

        @self.proudSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_proud.target', value)
            human.applyAllTargets(self.app.progress)

        @self.pleasedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_pleased.target', value)
            human.applyAllTargets(self.app.progress)

        @self.amusedSlider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_amused.target', value)
            human.applyAllTargets(self.app.progress)

        @self.laughing1Slider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_laughing1.target', value)
            human.applyAllTargets(self.app.progress)

        @self.laughing2Slider.event
        def onChange(value):
            human.setDetail('data/targets/expression/female_young/neutral_female_young_laughing2.target', value)
            human.applyAllTargets(self.app.progress)

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

    print 'example loaded'
    print 'Hello world'


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'example unloaded'


