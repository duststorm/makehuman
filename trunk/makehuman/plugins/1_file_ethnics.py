#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, mh, os
from algos3d import getTarget

class EthnicsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Ethnics')

        self.ethnicGroup = []
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Ethnic', gui3d.GroupBoxStyle._replace(height=25+24*1+6));y+=25
        self.africa = gui3d.RadioButton(self,self.ethnicGroup, [18,y, 9.2], "Africa", True, gui3d.ButtonStyle);y+=24
        y+=16
        
        self.subEthnicGroup = []
        gui3d.GroupBox(self, [10, y, 9.0], 'Sub ethnic', gui3d.GroupBoxStyle._replace(height=25+24*7+6));y+=25
        self.aethiopid = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Aethiopid", True, gui3d.ButtonStyle);y+=24
        self.center = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Center", style = gui3d.ButtonStyle);y+=24
        self.khoisan = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Khoisan", style = gui3d.ButtonStyle);y+=24
        self.nilotid = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Nilotid", style = gui3d.ButtonStyle);y+=24
        self.pigmy = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Pigmy", style = gui3d.ButtonStyle);y+=24
        self.sudanid = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Sudanid", style = gui3d.ButtonStyle);y+=24
        self.bantu = gui3d.RadioButton(self, self.subEthnicGroup, [18,y, 9.2], "Bantu", style = gui3d.ButtonStyle);y+=24
        
        self.genderGroup = []
        y = 80
        self.genderBox = gui3d.GroupBox(self, [650, y, 9.0], 'Gender', gui3d.GroupBoxStyle._replace(height=25+24*2+6));y+=25
        self.female = gui3d.RadioButton(self.genderBox, self.genderGroup, [658,y, 9.2], "Female", True, gui3d.ButtonStyle);y+=24
        self.male = gui3d.RadioButton(self.genderBox, self.genderGroup, [658,y, 9.2], "Male", style = gui3d.ButtonStyle);y+=24
        y+=16
        
        self.ageGroup = []
        self.ageBox = gui3d.GroupBox(self, [650, y, 9.0], 'Age', gui3d.GroupBoxStyle._replace(height=25+24*3+6));y+=25
        self.child = gui3d.RadioButton(self.ageBox, self.ageGroup, [658,y, 9.2], "Child", True, gui3d.ButtonStyle);y+=24
        self.young = gui3d.RadioButton(self.ageBox, self.ageGroup, [658,y, 9.2], "Young", style = gui3d.ButtonStyle);y+=24
        self.old = gui3d.RadioButton(self.ageBox, self.ageGroup, [658,y, 9.2], "Old", style = gui3d.ButtonStyle);y+=24
        y+=16
        
        self.loadBox = gui3d.GroupBox(self, [650, y, 9.0], 'Load', gui3d.GroupBoxStyle._replace(height=25+24*1+6));y+=25
        self.load = gui3d.Button(self.loadBox, [658,y, 9.2], "Load");y+=24
        
        @self.load.event
        def onClicked(event):
            ethnic = self.africa.getSelection().getLabel().lower()
            subEthnic = self.aethiopid.getSelection().getLabel().lower()
            gender = self.female.getSelection().getLabel().lower()
            age = self.child.getSelection().getLabel().lower()
            self.loadEthnic('%s-%s-%s-%s.mhm' % (ethnic, subEthnic, gender, age))
        
    def loadEthnic(self, filename):
        
        human = self.app.selectedHuman

        human.load(os.path.join('data/models/ethnics', filename), False, self.app.progress)
        target = os.path.join('data/models/ethnics', filename.replace('.mhm', '.target'))
        human.setDetail(target, 1.0)
        human.applyAllTargets(self.app.progress)

        del self.app.undoStack[:]
        del self.app.redoStack[:]

        self.app.categories['Files'].tasksByName['Save'].fileentry.text = filename.replace('.mhm', '')
        self.app.categories['Files'].tasksByName['Save'].fileentry.edit.setText(filename.replace('.mhm', ''))

        #self.app.switchCategory('Modelling')
        
    def onResized(self, event):
        
        self.genderBox.setPosition([event[0] - 150, self.genderBox.getPosition()[1], 9.0])
        self.ageBox.setPosition([event[0] - 150, self.ageBox.getPosition()[1], 9.0])
        self.loadBox.setPosition([event[0] - 150, self.loadBox.getPosition()[1], 9.0])
        
    def loadHandler(self, human, values):
        
        target = '%s.target' % os.path.join('data/models/ethnics', values[1])
        print target
        human.setDetail(target, float(values[2]))
       
    def saveHandler(self, human, file):
        
        for name, value in human.targetsDetailStack.iteritems():
            if 'ethnics' in name:
                target = os.path.basename(name).replace('.target', '')
                file.write('ethnic %s %f\n' % (target, value))

def load(app):
    category = app.getCategory('Files')
    taskview = EthnicsTaskView(category)
    
    app.addLoadHandler('ethnic', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)
    
    print 'Ethnics imported'

def unload(app):
    pass


