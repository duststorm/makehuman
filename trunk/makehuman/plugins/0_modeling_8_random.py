#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, random, humanmodifier
class RandomTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Random')
        
        toolbox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Tools', gui3d.GroupBoxStyle._replace(height=25+24*4+6)))
        self.macro = toolbox.addView(gui3d.CheckBox("Macro", True))
        self.height = toolbox.addView(gui3d.CheckBox("Height"))
        self.face = toolbox.addView(gui3d.CheckBox("Face"))
        self.symmetry = toolbox.addView(gui3d.Slider(value=-1.0, min=-1.0, max=1.0, label="Symmetry"))
        self.amount = toolbox.addView(gui3d.Slider(value=0.5, label="Amount"))
        self.create = toolbox.addView(gui3d.Button("Replace current"))
        self.modify = toolbox.addView(gui3d.Button("Adjust current"))

        self.lastRandoms = {}
        
        @self.create.event
        def onClicked(event):
            
            human = gui3d.app.selectedHuman
            # human.resetMeshValues()
            self.lastRandoms = {}
            
            if self.macro.selected:
                self.storeLastRandom('gender', 0.5, random.random()-0.5)
                self.storeLastRandom('age', 0.5, random.random()-0.5)
                self.storeLastRandom('muscle', 0.5, random.random()-0.5)
                self.storeLastRandom('weight', 0.5, random.random()-0.5)
                
            if self.height.selected:
                self.storeLastRandom( 'height', 0, random.random()*2-1 )

            if self.face.selected:
                category = gui3d.app.getCategory('Modelling')
                taskview = category.getViewByName('Face')
                modifiers = taskview.getModifiers()
                
                symmetricModifiers = taskview.getSymmetricModifierPairNames()
                for pair in symmetricModifiers:
                    #print "symmetric: "+pair['left']+' and '+pair['right']
                    leftValue = random.gauss( 0, 0.5 ) 
                    rightValue = random.gauss(0, 0.5 )
                    # store randoms for later
                    self.storeLastRandom(pair['left'], 0, leftValue)
                    self.storeLastRandom(pair['right'], 0, rightValue)

                singularModifiers = taskview.getSingularModifierNames()                
                for modName in singularModifiers:
                    #print "singular: "+modName
                    # get random gaussian
                    value = random.gauss( 0, 0.5 ) 
                    # non-asymmetric modifiers should only go 0..1
                    m = modifiers[modName]
                    if not isinstance(m, humanmodifier.GenderAgeEthnicAsymmetricModifier):
                        value = abs(value)
                    # store for later
                    self.storeLastRandom(modName, 0, value)

            self.setModifiers()
            
        @self.modify.event
        def onClicked(event):
            human = gui3d.app.selectedHuman
            
            if self.macro.selected:
                self.storeLastRandom( 'gender', human.getGender(), random.random()-0.5 )
                self.storeLastRandom( 'age', human.getAge(), random.random()-0.5 )
                self.storeLastRandom( 'weight', human.getWeight(), random.random()-0.5 )
                self.storeLastRandom( 'muscle', human.getMuscle(), random.random()-0.5 )
                
            if self.height.selected:
                modifier = humanmodifier.Modifier('data/targets/macrodetails/universal-stature-dwarf.target',
                    'data/targets/macrodetails/universal-stature-giant.target')
                self.storeLastRandom( 'height', modifier.getValue(human), random.random()-0.5)
            
            if self.face.selected:
                category = gui3d.app.getCategory('Modelling')
                taskview = category.getViewByName('Face')
                modifiers = taskview.getModifiers()
                
                symmetricModifiers = taskview.getSymmetricModifierPairNames()
                for pair in symmetricModifiers:
                    #print "symmetric: "+pair['left']+' and '+pair['right']
                    leftValue = random.gauss( 0, 0.5 ) 
                    rightValue = random.gauss( 0, 0.5 ) 
                    # store randoms for later
                    self.storeLastRandom(pair['left'], modifiers[pair['left']].getValue(human), leftValue)
                    self.storeLastRandom(pair['right'], modifiers[pair['right']].getValue(human), rightValue)

                singularModifiers = taskview.getSingularModifierNames()                
                for modName in singularModifiers:
                    #print "singular: "+modName
                    # get random gaussian
                    value = random.gauss( 0, 0.5 ) 
                    # non-asymmetric modifiers should only go 0..1
                    m = modifiers[modName]
                    if not isinstance(m, humanmodifier.GenderAgeEthnicAsymmetricModifier):
                        value = abs(value)
                    # store for later
                    self.storeLastRandom(modName, modifiers[modName].getValue(human), value)
    
            self.setModifiers()

        @self.amount.event
        def onChange(value):
            self.setModifiers()

        @self.symmetry.event
        def onChange(value):
            self.setModifiers()

    def setModifiers(self):

        human = gui3d.app.selectedHuman
        sliderMul = self.amount.getValue()

        if self.macro.selected:
            human.setGender( self.getRandom('gender', 0, 1 ))
            human.setAge( self.getRandom('age', 0, 1 ))
            human.setWeight( self.getRandom('weight', 0, 1 ))
            human.setMuscle( self.getRandom('muscle', 0, 1 ))

        if self.height.selected:
            modifier = humanmodifier.Modifier('data/targets/macrodetails/universal-stature-dwarf.target',
                'data/targets/macrodetails/universal-stature-giant.target')
            modifier.setValue(human, self.getRandom('height'), 0 ) 

        if self.face.selected:
            category = gui3d.app.getCategory('Modelling')
            taskview = category.getViewByName('Face')
            modifiers = taskview.getModifiers()
            symmetricModifiers = taskview.getSymmetricModifierPairNames()
            symFactor = self.symmetry.getValue()
            for pair in symmetricModifiers:
                #print "applying "+pair['left']+" and "+pair['right']
                leftValue = self.getRandom(pair['left'])
                rightValue = self.getRandom(pair['right'])
                # handle symmetry
                # -1 = left value only
                # 0 = no symmetry
                # 1 = right value only
                if symFactor < 0:
                    # hold the right value constant, adjust the left value towards its target
                    rightValue = leftValue*-symFactor + rightValue*(1.0+symFactor)
                else:
                    # hold the right value constant, adjust the left value towards its target
                    leftValue = rightValue*symFactor + leftValue*(1.0-symFactor)
                # apply
                modifiers[pair['left']].setValue(human, leftValue)
                modifiers[pair['right']].setValue(human, rightValue)

            singularModifiers = taskview.getSingularModifierNames()
            for modName in singularModifiers:
                #print "applying "+modName
                modifiers[modName].setValue(human, self.getRandom(modName) )

        human.applyAllTargets(gui3d.app.progress)
        
    # get the stored random value for the given modifierName, applying amount slider
    def getRandom( self, modifierName, minVal=-1, maxVal=1 ):
        if modifierName in self.lastRandoms:
            newVal = self.lastRandoms[modifierName]['base'] + self.lastRandoms[modifierName]['value']*self.amount.getValue()
            newVal = min(maxVal,max(minVal,newVal))
            return newVal
        else:
            return 0


    def storeLastRandom( self, modifierName, baseValue, randOffset ):
        self.lastRandoms[modifierName] = { 'base':baseValue, 'value':randOffset };

def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addView(RandomTaskView(category))
    print 'Random imported'

def unload(app):
    pass


