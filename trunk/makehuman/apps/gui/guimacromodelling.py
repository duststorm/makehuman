#!/usr/bin/python
# -*- coding: utf-8 -*-
import gui3d

class MacroAction:

    def __init__(self, human, method, value, postAction,update=True):
        self.name = method
        self.human = human
        self.method = method
        self.before = getattr(self.human, 'get' + self.method)()
        self.after = value
        self.postAction = postAction
        self.update = update

    def do(self):
        getattr(self.human, 'set' + self.method)(self.after)
        self.human.applyAllTargets(gui3d.app.progress, update=self.update)
        self.postAction()
        return True

    def undo(self):
        getattr(self.human, 'set' + self.method)(self.before)
        self.human.applyAllTargets(gui3d.app.progress)
        self.postAction()
        return True

class MacroModelingTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Macro modelling', label='Macro')

        font = gui3d.app.getFont(gui3d.TextViewStyle.fontFamily)
        self.status = self.addView(gui3d.TextView(style=gui3d.TextViewStyle._replace(width=800-20, left=10, top=600-2-font.lineHeight, zIndex=9.1)))

        self.macroBox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Main', style=gui3d.GroupBoxStyle._replace(height=25+36*5+6)))
       
        # Macro sliders

        self.genderSlider = self.macroBox.addView(gui3d.Slider(value=0.5, label = "Gender"))
        self.ageSlider = self.macroBox.addView(gui3d.Slider(value=0.5, label = "Age"))
        self.muscleSlider = self.macroBox.addView(gui3d.Slider(value=0.5, label = "Tone"))
        self.weightSlider = self.macroBox.addView(gui3d.Slider(value=0.5, label = "Weight"))
        self.heightSlider = self.macroBox.addView(gui3d.Slider(value=0.0, min=-1.0, max=1.0, label = "Height"))
        self.africanSlider = self.macroBox.addView(gui3d.Slider(value=0.0, min=0.0, max=1.0, label = "Afro"))
        self.asianSlider = self.macroBox.addView(gui3d.Slider(value=0.0, min=0.0, max=1.0, label = "Asian"))
        
        #self.radialBox = gui3d.GroupBox(self, [590, 80, 9.0], 'Radial', gui3d.GroupBoxStyle._replace(width=185+15))
        #self.radialWidget = gui3d.Radial(self.radialBox)

        #hair update only necessary for : gender, age , height
        
        @self.genderSlider.event
        def onChange(value):
            human = gui3d.app.selectedHuman
            gui3d.app.do(MacroAction(human, 'Gender', value, self.syncSliders,False))
            self.syncStatus()
            human.meshData.update()


        @self.ageSlider.event
        def onChange(value):
            human = gui3d.app.selectedHuman
            gui3d.app.do(MacroAction(human, 'Age', value, self.syncSliders,False))
            self.syncStatus()
            human.meshData.update()

        @self.muscleSlider.event
        def onChange(value):
            human = gui3d.app.selectedHuman
            gui3d.app.do(MacroAction(human, 'Muscle', value, self.syncSliders))
            self.syncStatus()

        @self.weightSlider.event
        def onChange(value):
            human = gui3d.app.selectedHuman
            gui3d.app.do(MacroAction(human, 'Weight', value, self.syncSliders))
            self.syncStatus()

        @self.heightSlider.event
        def onChange(value):
            human = gui3d.app.selectedHuman
            gui3d.app.do(MacroAction(human, 'Height', value, self.syncSliders, False))
            self.syncStatus()
            human.meshData.update()
            
        @self.africanSlider.event
        def onChange(value):
            human = gui3d.app.selectedHuman
            gui3d.app.do(MacroAction(human, 'African', value, self.syncSliders, False))
            self.syncStatus()
            human.meshData.update()
            
        @self.asianSlider.event
        def onChange(value):
            human = gui3d.app.selectedHuman
            gui3d.app.do(MacroAction(human, 'Asian', value, self.syncSliders, False))
            self.syncStatus()
            human.meshData.update()
            
        self.syncSliders()
        self.syncStatus()

    def syncSliders(self):
        human = gui3d.app.selectedHuman
        self.genderSlider.setValue(human.getGender())
        self.ageSlider.setValue(human.getAge())
        self.muscleSlider.setValue(human.getMuscle())
        self.weightSlider.setValue(human.getWeight())
        self.heightSlider.setValue(human.getHeight())
        self.africanSlider.setValue(human.getAfrican())
        self.asianSlider.setValue(human.getAsian())

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
        height = 10 * max(human.meshData.verts[8223].co[1] - human.meshData.verts[12361].co[1], human.meshData.verts[8223].co[1] - human.meshData.verts[13155].co[1])
        if gui3d.app.settings['units'] == 'metric':
            units = 'cm'
        else:
            units = 'in'
            height *= 0.393700787
        self.status.setTextFormat('Gender: %s, Age: %d, Muscle: %.2f%%, Weight: %.2f%%, Height: %.2f %s', gender, age, muscle, weight, height, units)

    def onShow(self, event):
        self.genderSlider.setFocus()
        self.syncSliders()
        self.syncStatus()
        gui3d.TaskView.onShow(self, event)
        
    def onHumanChanged(self, event):
            
        if self.isVisible():
            self.syncSliders()
            self.syncStatus()

    def onResized(self, event):
        font = gui3d.app.getFont(gui3d.TextViewStyle.fontFamily)
        self.status.setPosition([10, event.height-2-font.lineHeight, 9.1])
        #self.radialBox.setPosition([event.width - 210, self.radialBox.getPosition()[1], 9.0])
