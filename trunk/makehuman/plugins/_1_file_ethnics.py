#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, os
import mh
import qtgui as gui

class EthnicsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Ethnics')

        self.ethnicGroup = []
        ethnicBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Ethnic')))
        self.africa = ethnicBox.addWidget(gui.RadioButton(self.ethnicGroup, "Africa", True))
        self.africa.name = "africa"
        
        self.subEthnicGroup = []
        subEthnicBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Sub ethnic')))
        self.aethiopid = subEthnicBox.addWidget(gui.RadioButton(self.subEthnicGroup, "Aethiopid", True))
        self.aethiopid.name = "aethiopid"
        self.center = subEthnicBox.addWidget(gui.RadioButton(self.subEthnicGroup, "Center"))
        self.center.name = "center"
        self.khoisan = subEthnicBox.addWidget(gui.RadioButton(self.subEthnicGroup, "Khoisan"))
        self.khoisan.name = "khoisan"
        self.nilotid = subEthnicBox.addWidget(gui.RadioButton(self.subEthnicGroup, "Nilotid"))
        self.nilotid.name = "nilotid"
        self.pigmy = subEthnicBox.addWidget(gui.RadioButton(self.subEthnicGroup, "Pigmy"))
        self.pigmy.name = "pigmy"
        self.sudanid = subEthnicBox.addWidget(gui.RadioButton(self.subEthnicGroup, "Sudanid"))
        self.sudanid.name = "sudanid"
        self.bantu = subEthnicBox.addWidget(gui.RadioButton(self.subEthnicGroup, "Bantu"))
        self.bantu.name = "bantu"
        
        self.genderGroup = []
        self.genderBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Gender')))
        self.female = self.genderBox.addWidget(gui.RadioButton(self.genderGroup, "Female", True))
        self.female.name = "female"
        self.male = self.genderBox.addWidget(gui.RadioButton(self.genderGroup, "Male"))
        self.male.name = "male"
        
        self.ageGroup = []
        self.ageBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Age')))
        self.child = self.ageBox.addWidget(gui.RadioButton(self.ageGroup, "Child", True))
        self.child.name = "child"
        self.young = self.ageBox.addWidget(gui.RadioButton(self.ageGroup, "Young"))
        self.young.name = "young"
        self.old = self.ageBox.addWidget(gui.RadioButton(self.ageGroup, "Old"))
        self.old = "old"
        
        self.loadBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Load')))
        self.load = self.loadBox.addWidget(gui.Button("Load"))
        
        @self.load.mhEvent
        def onClicked(event):
            ethnic = self.africa.getSelection().name
            subEthnic = self.aethiopid.getSelection().name
            gender = self.female.getSelection().name
            age = self.child.getSelection().name
            self.loadEthnic('%s-%s-%s-%s.mhm' % (ethnic, subEthnic, gender, age))
        
    def loadEthnic(self, filename):
        
        human = gui3d.app.selectedHuman

        human.load(os.path.join('data/models/ethnics', filename), False, gui3d.app.progress)
        target = os.path.join('data/models/ethnics', filename.replace('.mhm', '.target'))
        human.setDetail(target, 1.0)
        human.applyAllTargets(gui3d.app.progress)

        del gui3d.app.undoStack[:]
        del gui3d.app.redoStack[:]

        gui3d.app.categories['Files'].tasksByName['Save'].fileentry.text = filename.replace('.mhm', '')
        gui3d.app.categories['Files'].tasksByName['Save'].fileentry.edit.setText(filename.replace('.mhm', ''))

        #mh.changeCategory('Modelling')
        
    def onResized(self, event):
        
        self.genderBox.setPosition([event.width - 150, self.genderBox.getPosition()[1], 9.0])
        self.ageBox.setPosition([event.width - 150, self.ageBox.getPosition()[1], 9.0])
        self.loadBox.setPosition([event.width - 150, self.loadBox.getPosition()[1], 9.0])
        
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
    taskview = category.addView(EthnicsTaskView(category))
    
    app.addLoadHandler('ethnic', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)
    
    print 'Ethnics imported'

def unload(app):
    pass


