import os.path
#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import os
import random
import algos3d
import mh
import humanmodifier
import events3d

class AssymSlider(gui3d.Slider):
    
    def __init__(self, parent, x, y, bodypart, label):
        gui3d.Slider.__init__(self, parent, position=[x, y, 9.3], value=0.0, min=-1.0, max=1.0, label=label)
        self.bodypart = bodypart
        
    def onChange(self, value):
        self.parent.changeValue(self.bodypart, value)
        
    def onChanging(self, value):
        self.parent.changeValue(self.bodypart, value, True)

class AsymmTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Asymm')

        #Sliders
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Face', gui3d.GroupBoxStyle._replace(height=400));y+=35
        self.asymmBrowSlider = AssymSlider(self, 10, y, "brown", "Brow asymmetry");y+=40
        self.asymmCheekSlider = AssymSlider(self, 10, y, "cheek", "Cheek asymmetry");y+=40
        self.asymmEarsSlider = AssymSlider(self, 10, y,  "ear", "Ears asymmetry");y+=40
        self.asymmEyeSlider = AssymSlider(self, 10, y, "eye", "Eye asymmetry");y+=40
        self.asymmJawSlider = AssymSlider(self, 10, y, "jaw", "Jaw asymmetry");y+=40
        self.asymmMouthSlider = AssymSlider(self, 10, y, "mouth", "Mouth asymmetry");y+=40
        self.asymmNoseSlider = AssymSlider(self, 10, y, "nose", "Nose asymmetry");y+=40
        self.asymmTempleSlider = AssymSlider(self, 10, y, "temple", "Temple asymmetry");y+=40
        self.asymmTopSlider = AssymSlider(self, 10, y, "top", "Top asymmetry");y+=40 + 8
        y = 80
        gui3d.GroupBox(self, [650, y, 9.0], 'Body', gui3d.GroupBoxStyle._replace(height=120));y+=25
        self.asymmTrunkSlider = AssymSlider(self, 650, y, "trunk", "Trunk asymmetry");y+=40
        self.asymmBreastSlider = AssymSlider(self, 650, y, "breast", "Breast asymmetry")

        #Get a list with all targes (complete with path) used in asymm library
        self.asymmDataPath = "data/targets/asym/"
        self.asymmTargets = []
        for f in os.listdir(self.asymmDataPath):
            if os.path.isfile(os.path.join(self.asymmDataPath, f)):
                self.asymmTargets.append(os.path.join(self.asymmDataPath, f))

        #The human mesh
        self.human = self.app.scene3d.selectedHuman

        #Random factor from Slider
        self.randomVal = 0.5
        
        # Modifiers
        self.modifiers = {}
        for bodypart in ["brown", "cheek","ear","eye", "jaw", "mouth","nose","temple","top","trunk","breast"]:
            self.getModifiers(bodypart)
        
        # Undo memory
        self.before = None

    def changeValue(self, bodyPartName, value, realtime=False):
        """
        This function apply the targets, and inform the undo system about the changes.
        @return: None
        @type  bodyPartName: String
        @param bodyPartName: Name of the body part to asymmetrise
        @type  value: Float
        @param value: The amount of asymmetry
        """
        if realtime:
            if not self.before:
                self.before = self.getTargetsAndValues(bodyPartName)
                
            self.calcAsymm(value,bodyPartName)
        else:
            self.calcAsymm(value,bodyPartName)
            self.human.applyAllTargets(self.human.app.progress)
            
            after = self.getTargetsAndValues(bodyPartName)
            
            self.app.did(humanmodifier.Action(self.human, self.before, after, self.syncSliders))
            
            self.before = None

    def buildListOfTargetPairs(self, name):
        """
        This function scan all targets and build a list of list:
        [[target1-left,target1-right],...,[targetN-left,targetN-right]]
        @return: List of lists
        @type  name: String
        @param targets: Name of the body part to asymmetrise
        """
        pairs = []
        for f in self.asymmTargets:
            if name in f:
                dirPath = os.path.dirname(f)
                targetName = os.path.splitext(os.path.basename(f))[0]
                prefix = targetName[:-2]
                suffix = targetName[-2:]
                if suffix == "-r":
                    f2 = dirPath + "/" + prefix + "-l.target"
                    pair = [f,f2]
                    pairs.append(pair)
        return pairs


    def getTargetsAndValues(self, bodypart):
        """
        This function return a dictionary with "targetPath:val" items, getting them
        from the human details stack.
        It's used to get both "before" and "after" dictionaries.
        @return: Dictionary
        @type  targets: List
        @param targets: List of targets to get
        """
        modifiers = self.getModifiers(bodypart)
           
        targetsAndValues = {}
        for modifier in modifiers:                
            targetsAndValues[modifier.left] = self.human.getDetail(modifier.left)
            targetsAndValues[modifier.right] = self.human.getDetail(modifier.right)
        return targetsAndValues

    def calcAsymm(self, value, bodypart):
            """
            This function load all asymmetry targets for the specified part of body
            (for example brown, eyes, etc..) and return a dictionary with
            the applied targets, used as "after" parameter in undo system
            @return: Dictionary
            @type  value: Float
            @param value: The amount of asymmetry
            @type  bodypart: String
            @param bodypart: The name of part to asymmetrize.
            """
            modifiers = self.getModifiers(bodypart)
           
            for modifier in modifiers:                
                modifier.setValue(value)
                
    def getModifiers(self, bodypart):
        modifiers = self.modifiers.get(bodypart, None)
        if not modifiers:
            modifiers = []
            targets = self.buildListOfTargetPairs(bodypart)
            for pair in targets:
                modifier = humanmodifier.Modifier(self.human, pair[0], pair[1])
                modifiers.append(modifier)
            self.modifiers[bodypart] = modifiers
        return modifiers
        
    def getSliderValue(self, bodypart):
        modifiers = self.modifiers[bodypart]
        if modifiers:
            return modifiers[0].getValue()
        else:
            return 0.0
            
    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        self.asymmBrowSlider.setFocus()
        self.syncSliders()
            
    def syncSliders(self):
        self.asymmBrowSlider.setValue(self.getSliderValue('brown'))
        self.asymmCheekSlider.setValue(self.getSliderValue('cheek'))
        self.asymmEarsSlider.setValue(self.getSliderValue('ear'))
        self.asymmEyeSlider.setValue(self.getSliderValue('eye'))
        self.asymmJawSlider.setValue(self.getSliderValue('jaw'))
        self.asymmMouthSlider.setValue(self.getSliderValue('mouth'))
        self.asymmNoseSlider.setValue(self.getSliderValue('nose'))
        self.asymmTempleSlider.setValue(self.getSliderValue('temple'))
        self.asymmTopSlider.setValue(self.getSliderValue('top'))
        self.asymmTrunkSlider.setValue(self.getSliderValue('trunk'))
        self.asymmBreastSlider.setValue(self.getSliderValue('breast'))
        
    def onKeyDown(self, event):

        # Undo redo
        if event.key == events3d.SDLK_y:
            self.app.redo()
        elif event.key == events3d.SDLK_z:
            self.app.undo()
            
        gui3d.TaskView.onKeyDown(self, event)

def load(app):
    """
    Plugin load function, needed by design.
    """
    category = app.getCategory('Advanced')
    taskview = AsymmTaskView(category)
    print 'Asymm loaded'

    #Zoom and pan the camera
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
            trans = app.modelCamera.convertToScreen(trans[0], trans[1], trans[2])
            trans[0] += diff[0]
            trans[1] += diff[1]
            trans = app.modelCamera.convertToWorld3D(trans[0], trans[1], trans[2])
            human.setPosition(trans)




