#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, mh, os, random, humanmodifier
class RandomTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Random')
        
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Tools', gui3d.GroupBoxStyle._replace(height=25+24*4+6));y+=25
        self.macro = gui3d.CheckBox(self, [18, y, 9.2], "Macro", True);y+=24
        self.height = gui3d.CheckBox(self, [18, y, 9.2], "Height");y+=24
        self.create = gui3d.Button(self, [18, y, 9.2], "Create new");y+=24
        self.modify = gui3d.Button(self, [18, y, 9.2], "Modify current");y+=24
        
        @self.create.event
        def onClicked(event):
            human = self.app.selectedHuman
            human.resetMeshValues()
            
            if self.macro.selected:
                human.setGender(random.random())
                human.setAge(random.random())
                human.setMuscle(random.random())
                human.setWeight(random.random())
                
            if self.height.selected:
                modifier = humanmodifier.Modifier(human, 'data/targets/macrodetails/universal-stature-dwarf.target',
                                                      'data/targets/macrodetails/universal-stature-giant.target')
                modifier.setValue(random.random() * 2 - 1, 0)
            
            human.applyAllTargets(self.app.progress)
            
        @self.modify.event
        def onClicked(event):
            human = self.app.selectedHuman
            
            if self.macro.selected:
                human.setGender(human.getGender() + random.random() - 0.5)
                human.setAge(human.getAge() + random.random() - 0.5)
                human.setMuscle(human.getMuscle() + random.random() - 0.5)
                human.setWeight(human.getWeight() + random.random() - 0.5)
                
            if self.height.selected:
                modifier = humanmodifier.Modifier(human, 'data/targets/macrodetails/universal-stature-dwarf.target',
                                                      'data/targets/macrodetails/universal-stature-giant.target')
                modifier.setValue(modifier.getValue() + random.random() - 0.5, 0)
                
            human.applyAllTargets(self.app.progress)

        '''
        self.ethnicGroup = []
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Ethnic', gui3d.GroupBoxStyle._replace(height=128));y+=25
        self.africa = gui3d.RadioButton(self,self.ethnicGroup, [18,y, 9.2], "Africa", True, gui3d.ButtonStyle);y+=25
        y+=90
        
        self.subEthnicGroup = []
        gui3d.GroupBox(self, [10, y, 9.0], 'Sub ethnic', gui3d.GroupBoxStyle._replace(height=200));y+=25
        self.aethiopid = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Aethiopid", True, gui3d.ButtonStyle);y+=25
        self.center = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Center", style = gui3d.ButtonStyle);y+=25
        self.khoisan = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Khoisan", style = gui3d.ButtonStyle);y+=25
        self.nilotid = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Nilotid", style = gui3d.ButtonStyle);y+=25
        self.pigmy = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Pigmy", style = gui3d.ButtonStyle);y+=25
        self.sudanid = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Sudanid", style = gui3d.ButtonStyle);y+=25
        
        self.genderGroup = []
        y = 80
        gui3d.GroupBox(self, [650, y, 9.0], 'Gender', gui3d.GroupBoxStyle._replace(height=100));y+=25
        self.female = gui3d.RadioButton(self, self.genderGroup, [658,y, 9.2], "Female", True, gui3d.ButtonStyle);y+=25
        self.male = gui3d.RadioButton(self, self.genderGroup, [658,y, 9.2], "Male", style = gui3d.ButtonStyle);y+=25
        y+=35
        
        self.ageGroup = []
        gui3d.GroupBox(self, [650, y, 9.0], 'Age', gui3d.GroupBoxStyle._replace(height=120));y+=25
        self.child = gui3d.RadioButton(self, self.ageGroup, [658,y, 9.2], "Child", True, gui3d.ButtonStyle);y+=25
        self.young = gui3d.RadioButton(self, self.ageGroup, [658,y, 9.2], "Young", style = gui3d.ButtonStyle);y+=25
        self.old = gui3d.RadioButton(self, self.ageGroup, [658,y, 9.2], "Old", style = gui3d.ButtonStyle);y+=25
        y+=35
        
        gui3d.GroupBox(self, [650, y, 9.0], 'Load', gui3d.GroupBoxStyle._replace(height=120));y+=25
        self.load = gui3d.Button(self, [658,y, 9.2], "Load");y+=25
        
        @self.load.event
        def onClicked(event):
            ethnic = self.africa.getSelection().getLabel().lower()
            subEthnic = self.aethiopid.getSelection().getLabel().lower()
            gender = self.female.getSelection().getLabel().lower()
            age = self.child.getSelection().getLabel().lower()
            self.loadEthnic('%s-%s-%s-%s.mhm' % (ethnic, subEthnic, gender, age))
        '''
        
    def loadEthnic(self, filename):
        
        human = self.app.selectedHuman

        human.load(os.path.join('data/models/ethnics', filename), self.app.progress)
        human.setDetail(os.path.join('data/models/ethnics', filename.replace('.mhm', '.target')), 1.0)

        del self.app.undoStack[:]
        del self.app.redoStack[:]

        self.app.categories['Files'].tasksByName['Save'].fileentry.text = filename.replace('.mhm', '')
        self.app.categories['Files'].tasksByName['Save'].fileentry.edit.setText(filename.replace('.mhm', ''))

        #self.app.switchCategory('Modelling')

def load(app):
    category = app.getCategory('Experiments')
    taskview = RandomTaskView(category)
    print 'Random imported'

def unload(app):
    pass


