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
import aljabr

class MeasureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Measure')

        self.ruler = Ruler(category.app.scene3d.selectedHuman)


        #Sliders

        self.neckGroup = gui3d.GroupBox(self, label = 'Neck', position=[10, 80, 9.0], width=128, height=128)
        
        lbl = "Neck circum.: cm "+ str(round(self.ruler.getMeasure("neckcirc")))
        self.neckCircumferenceSlider = gui3d.Slider(self.neckGroup,  position=[10, 115, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        lbl = "Neck height: cm "+ str(round(self.ruler.getMeasure("neckheight")))
        self.neckHeightSlider = gui3d.Slider(self.neckGroup,  position=[10, 155, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        self.upperArmGroup = gui3d.GroupBox(self, label = 'Upper arm', position=[10, 80, 9.0], width=128, height=128)
        
        lbl = "Upper arm circum.: cm "+ str(round(self.ruler.getMeasure("upperarm")))
        self.upperArmCircumferenceSlider = gui3d.Slider(self.upperArmGroup,  position=[10, 115, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        lbl = "Upperarm lenght: cm "+ str(round(self.ruler.getMeasure("upperarmlenght")))
        self.upperArmLenghtSlider = gui3d.Slider(self.upperArmGroup,  position=[10, 155, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)
        
        self.lowerArmGroup = gui3d.GroupBox(self, label = 'Lower arm', position=[10, 80, 9.0], width=128, height=128)

        lbl = "Lowerarm lenght: cm "+ str(round(self.ruler.getMeasure("lowerarmlenght")))
        self.lowerarmLenghtSlider = gui3d.Slider(self.lowerArmGroup,  position=[10, 115, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        lbl = "Wrist circum.: cm "+ str(round(self.ruler.getMeasure("wrist")))
        self.wristCircumferenceSlider = gui3d.Slider(self.lowerArmGroup,  position=[10, 155, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        self.torsoGroup = gui3d.GroupBox(self, label = 'Torso', position=[10, 80, 9.0], width=128, height=370)
        
        lbl = "Front chest dist: cm "+ str(round(self.ruler.getMeasure("frontchest")))
        self.frontChestSlider = gui3d.Slider(self.torsoGroup,  position=[10, 115, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        lbl = "Bust circ.: cm "+ str(round(self.ruler.getMeasure("bust")))
        self.bustCircumferenceSlider = gui3d.Slider(self.torsoGroup,  position=[10, 155, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        lbl = "Underbust circ.: cm "+ str(round(self.ruler.getMeasure("underbust")))
        self.underBustCircumferenceSlider = gui3d.Slider(self.torsoGroup,  position=[10, 205, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        lbl = "Waist circ.: cm "+ str(round(self.ruler.getMeasure("waist")))
        self.waistCircumferenceSlider = gui3d.Slider(self.torsoGroup,  position=[10, 255, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        lbl = "Nape to waist: cm "+ str(round(self.ruler.getMeasure("napetowaist")))
        self.napeToWaistSlider = gui3d.Slider(self.torsoGroup,  position=[10, 305, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        lbl = "Waist to hip: cm "+ str(round(self.ruler.getMeasure("waisttohip")))
        self.waistToHipSlider = gui3d.Slider(self.torsoGroup,  position=[10, 355, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        lbl = "Shoulder Dist.: cm "+ str(round(self.ruler.getMeasure("shoulder")))
        self.shoulderDistanceSlider = gui3d.Slider(self.torsoGroup,  position=[10, 405, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)
        
        self.hipsGroup = gui3d.GroupBox(self, label = 'Hips', position=[10, 80, 9.0], width=128, height=80)
        
        lbl = "Hips circ.: cm "+ str(round(self.ruler.getMeasure("hips")))
        self.hipsSlider = gui3d.Slider(self.hipsGroup,  position=[10, 115, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl )
        
        self.upperLegGroup = gui3d.GroupBox(self, label = 'Upper leg', position=[10, 80, 9.0], width=128, height=128)

        lbl = "Upperleg height: cm "+ str(round(self.ruler.getMeasure("upperlegheight")))
        self.upperLegHeightSlider = gui3d.Slider(self.upperLegGroup,  position=[10, 115, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        lbl = "Thigh circ.: cm "+ str(round(self.ruler.getMeasure("thighcirc")))
        self.upperThighSlider = gui3d.Slider(self.upperLegGroup,  position=[10, 155, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl )
        
        self.lowerLegGroup = gui3d.GroupBox(self, label = 'Lower leg', position=[10, 80, 9.0], width=128, height=128)

        lbl = "Lowerleg height: cm "+ str(round(self.ruler.getMeasure("lowerlegheight")))
        self.lowerLegHeightSlider = gui3d.Slider(self.lowerLegGroup,  position=[10, 115, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)

        lbl = "Calf circ.: cm "+ str(round(self.ruler.getMeasure("calf")))
        self.calfSlider = gui3d.Slider(self.lowerLegGroup,  position=[10, 155, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)
        
        self.ankleGroup = gui3d.GroupBox(self, label = 'Ankle', position=[10, 80, 9.0], width=128, height=80)

        lbl = "Ankle circ.: cm "+ str(round(self.ruler.getMeasure("ankle")))
        self.ankleSlider = gui3d.Slider(self.ankleGroup,  position=[10, 115, 9.3], value=0.0, min=-1.0, max=1.0, label=lbl)      


        #Get a list with all targes (complete with path) used in measureData library
        self.measureDataPath = "data/targets/measure/"
        self.measureTargets = []
        for f in os.listdir(self.measureDataPath):
            if os.path.isfile(os.path.join(self.measureDataPath, f)):
                self.measureTargets.append(os.path.join(self.measureDataPath, f))

        #The human mesh
        self.human = self.app.scene3d.selectedHuman

        # Modifiers
        self.modifiers = {}
        for IDName in ["neckcirc", "neckheight","upperarm","upperarmlenght", "lowerarmlenght", "wrist", "frontchest", "bust", "underbust","waist", "napetowaist", "waisttohip",
                        "shoulder", "upperlegheight", "lowerlegheight", "calf", "ankle", "thighcirc", "hips"]:
            self.getModifiers(IDName)

        # Undo memory
        self.before = None

        #Sliders events
        @self.neckCircumferenceSlider.event
        def onChange(value):
            self.changeValue("neckcirc",value)
            self.updateMeasures()

        @self.neckCircumferenceSlider.event
        def onChanging(value):
            self.changeValue("neckcirc",value,True)
            lbl = "Neck circum.: cm "+ str(round(self.ruler.getMeasure("neckcirc")))
            self.neckCircumferenceSlider.label.setText(lbl)

        @self.neckHeightSlider.event
        def onChange(value):
            self.changeValue("neckheight",value)
            self.updateMeasures()

        @self.neckHeightSlider.event
        def onChanging(value):
            self.changeValue("neckheight",value,True)
            lbl = "Neck height: cm "+ str(round(self.ruler.getMeasure("neckheight")))
            self.neckHeightSlider.label.setText(lbl)

        @self.upperArmCircumferenceSlider.event
        def onChange(value):
            self.changeValue("upperarm",value)
            self.updateMeasures()

        @self.upperArmCircumferenceSlider.event
        def onChanging(value):
            self.changeValue("upperarm",value,True)
            lbl = "Upper arm circum.: cm "+ str(round(self.ruler.getMeasure("upperarm")))
            self.upperArmCircumferenceSlider.label.setText(lbl)

        @self.upperArmLenghtSlider.event
        def onChange(value):
            self.changeValue("upperarmlenght",value)
            self.updateMeasures()

        @self.upperArmLenghtSlider.event
        def onChanging(value):
            self.changeValue("upperarmlenght",value,True)
            lbl = "Upperarm lenght: cm "+ str(round(self.ruler.getMeasure("upperarmlenght")))
            self.upperArmLenghtSlider.label.setText(lbl)

        @self.lowerarmLenghtSlider.event
        def onChange(value):
            self.changeValue("lowerarmlenght",value)
            self.updateMeasures()

        @self.lowerarmLenghtSlider.event
        def onChanging(value):
            self.changeValue("lowerarmlenght",value,True)
            lbl = "Lowerarm lenght: cm "+ str(round(self.ruler.getMeasure("lowerarmlenght")))
            self.lowerarmLenghtSlider.label.setText(lbl)

        @self.wristCircumferenceSlider.event
        def onChange(value):
            self.changeValue("wrist",value)
            self.updateMeasures()

        @self.wristCircumferenceSlider.event
        def onChanging(value):
            self.changeValue("wrist",value,True)
            lbl = "Wrist circum.: cm "+ str(round(self.ruler.getMeasure("wrist")))
            self.wristCircumferenceSlider.label.setText(lbl)

        @self.frontChestSlider.event
        def onChange(value):
            self.changeValue("frontchest",value)
            self.updateMeasures()

        @self.frontChestSlider.event
        def onChanging(value):
            self.changeValue("frontchest",value,True)
            lbl = "Front chest dist: cm "+ str(round(self.ruler.getMeasure("frontchest")))
            self.frontChestSlider.label.setText(lbl)

        @self.bustCircumferenceSlider.event
        def onChange(value):
            self.changeValue("bust",value)
            self.updateMeasures()

        @self.bustCircumferenceSlider.event
        def onChanging(value):
            self.changeValue("bust",value,True)
            lbl = "Bust circ.: cm "+ str(round(self.ruler.getMeasure("bust")))
            self.bustCircumferenceSlider.label.setText(lbl)

        @self.underBustCircumferenceSlider.event
        def onChange(value):
            self.changeValue("underbust",value)
            self.updateMeasures()

        @self.underBustCircumferenceSlider.event
        def onChanging(value):
            self.changeValue("underbust",value,True)
            lbl = "Underbust circ.: cm "+ str(round(self.ruler.getMeasure("underbust")))
            self.underBustCircumferenceSlider.label.setText(lbl)

        @self.waistCircumferenceSlider.event
        def onChange(value):
            self.changeValue("waist",value)
            self.updateMeasures()

        @self.waistCircumferenceSlider.event
        def onChanging(value):
            self.changeValue("waist",value,True)
            lbl = "Waist circ.: cm "+ str(round(self.ruler.getMeasure("waist")))
            self.waistCircumferenceSlider.label.setText(lbl)

        @self.napeToWaistSlider.event
        def onChange(value):
            self.changeValue("napetowaist",value)
            self.updateMeasures()

        @self.napeToWaistSlider.event
        def onChanging(value):
            self.changeValue("napetowaist",value,True)
            lbl = "Nape to waist: cm "+ str(round(self.ruler.getMeasure("napetowaist")))
            self.napeToWaistSlider.label.setText(lbl)

        @self.waistToHipSlider.event
        def onChange(value):
            self.changeValue("waisttohip",value)
            self.updateMeasures()

        @self.waistToHipSlider.event
        def onChanging(value):
            self.changeValue("waisttohip",value,True)
            lbl = "Waist to hip: cm "+ str(round(self.ruler.getMeasure("waisttohip")))
            self.waistToHipSlider.label.setText(lbl)

        @self.shoulderDistanceSlider.event
        def onChange(value):
            self.changeValue("shoulder",value)
            self.updateMeasures()

        @self.shoulderDistanceSlider.event
        def onChanging(value):
            self.changeValue("shoulder",value,True)
            lbl = "Shoulder Dist.: cm "+ str(round(self.ruler.getMeasure("shoulder")))
            self.shoulderDistanceSlider.label.setText(lbl)

        @self.upperLegHeightSlider.event
        def onChange(value):
            self.changeValue("upperlegheight",value)
            self.updateMeasures()

        @self.upperLegHeightSlider.event
        def onChanging(value):
            self.changeValue("upperlegheight",value,True)
            lbl = "Upperleg height: cm "+ str(round(self.ruler.getMeasure("upperlegheight")))
            self.upperLegHeightSlider.label.setText(lbl)

        @self.lowerLegHeightSlider.event
        def onChange(value):
            self.changeValue("lowerlegheight",value)
            self.updateMeasures()

        @self.lowerLegHeightSlider.event
        def onChanging(value):
            self.changeValue("lowerlegheight",value,True)
            lbl = "Lowerleg height: cm "+ str(round(self.ruler.getMeasure("lowerlegheight")))
            self.lowerLegHeightSlider.label.setText(lbl)

        @self.calfSlider.event
        def onChange(value):
            self.changeValue("calf",value)
            self.updateMeasures()

        @self.calfSlider.event
        def onChanging(value):
            self.changeValue("calf",value,True)
            lbl = "Calf circ.: cm "+ str(round(self.ruler.getMeasure("calf")))
            self.calfSlider.label.setText(lbl)

        @self.ankleSlider.event
        def onChange(value):
            self.changeValue("ankle",value)
            self.updateMeasures()

        @self.ankleSlider.event
        def onChanging(value):
            self.changeValue("ankle",value,True)
            lbl = "Ankle circ.: cm "+ str(round(self.ruler.getMeasure("ankle")))
            self.ankleSlider.label.setText(lbl)

        @self.upperThighSlider.event
        def onChange(value):
            self.changeValue("thighcirc",value)
            self.updateMeasures()

        @self.upperThighSlider.event
        def onChanging(value):
            self.changeValue("thighcirc",value,True)
            lbl = "Thigh circ.: cm "+ str(round(self.ruler.getMeasure("thighcirc")))
            self.upperThighSlider.label.setText(lbl)

        @self.hipsSlider.event
        def onChange(value):
            self.changeValue("hips",value)
            self.updateMeasures()

        @self.hipsSlider.event
        def onChanging(value):
            self.changeValue("hips",value,True)
            lbl = "Hips circ.: cm "+ str(round(self.ruler.getMeasure("hips")))
            self.hipsSlider.label.setText(lbl)

    def updateMeasures(self):

        lbl = "Neck circum.: cm "+ str(round(self.ruler.getMeasure("neckcirc")))
        self.neckCircumferenceSlider.label.setText(lbl)

        lbl = "Neck height: cm "+ str(round(self.ruler.getMeasure("neckheight")))
        self.neckHeightSlider.label.setText(lbl)

        lbl = "Upper arm circum.: cm "+ str(round(self.ruler.getMeasure("upperarm")))
        self.upperArmCircumferenceSlider.label.setText(lbl)

        lbl = "Upperarm lenght: cm "+ str(round(self.ruler.getMeasure("upperarmlenght")))
        self.upperArmLenghtSlider.label.setText(lbl)

        lbl = "Lowerarm lenght: cm "+ str(round(self.ruler.getMeasure("lowerarmlenght")))
        self.lowerarmLenghtSlider.label.setText(lbl)

        lbl = "Wrist circum.: cm "+ str(round(self.ruler.getMeasure("wrist")))
        self.wristCircumferenceSlider.label.setText(lbl)

        lbl = "Front chest dist: cm "+ str(round(self.ruler.getMeasure("frontchest")))
        self.frontChestSlider.label.setText(lbl)

        lbl = "Bust circ.: cm "+ str(round(self.ruler.getMeasure("bust")))
        self.bustCircumferenceSlider.label.setText(lbl)

        lbl = "Underbust circ.: cm "+ str(round(self.ruler.getMeasure("underbust")))
        self.underBustCircumferenceSlider.label.setText(lbl)

        lbl = "Waist circ.: cm "+ str(round(self.ruler.getMeasure("waist")))
        self.waistCircumferenceSlider.label.setText(lbl)

        lbl = "Nape to waist: cm "+ str(round(self.ruler.getMeasure("napetowaist")))
        self.napeToWaistSlider.label.setText(lbl)

        lbl = "Waist to hip: cm "+ str(round(self.ruler.getMeasure("waisttohip")))
        self.waistToHipSlider.label.setText(lbl)

        lbl = "Shoulder Dist.: cm "+ str(round(self.ruler.getMeasure("shoulder")))
        self.shoulderDistanceSlider.label.setText(lbl)

        lbl = "Upperleg height: cm "+ str(round(self.ruler.getMeasure("upperlegheight")))
        self.upperLegHeightSlider.label.setText(lbl)

        lbl = "Lowerleg height: cm "+ str(round(self.ruler.getMeasure("lowerlegheight")))
        self.lowerLegHeightSlider.label.setText(lbl)

        lbl = "Calf circ.: cm "+ str(round(self.ruler.getMeasure("calf")))
        self.calfSlider.label.setText(lbl)

        lbl = "Ankle circ.: cm "+ str(round(self.ruler.getMeasure("ankle")))
        self.ankleSlider.label.setText(lbl)

        lbl = "Thigh circ.: cm "+ str(round(self.ruler.getMeasure("thighcirc")))
        self.upperThighSlider.label.setText(lbl)

        lbl = "Hips circ.: cm "+ str(round(self.ruler.getMeasure("hips")))
        self.hipsSlider.label.setText(lbl)


    def changeValue(self, IDName, value, realtime=False):
        """
        This function applies the targets, and informs the undo system about the changes.
        @return: None
        @type  IDName: String
        @param IDName: Name of the body part to asymmetrise
        @type  value: Float
        @param value: The amount of asymmetry
        """
        if realtime:
            if not self.before:
                self.before = self.getTargetsAndValues(IDName)

            self.setModifierValue(value, IDName)
        else:
            self.setModifierValue(value, IDName)
            self.human.applyAllTargets(self.human.app.progress)

            after = self.getTargetsAndValues(IDName)

            self.app.did(humanmodifier.Action(self.human, self.before, after, self.syncSliders))

            self.before = None

    def buildListOfTargetPairs(self, name):
        """
        This function scans all targets and builds a list of lists:
        [[target1-left,target1-right],...,[targetN-left,targetN-right]]
        @return: List of lists
        @type  name: String
        @param targets: Name of the body part to asymmetrise
        """
        pairs = []
        fName1 = "measure-"+name+"-decrease.target"
        fName2 = "measure-"+name+"-increase.target"

        file1 = os.path.join(self.measureDataPath, fName1)
        file2 = os.path.join(self.measureDataPath, fName2)

        pair = (file1,file2)
        pairs.append(pair)
        return pairs


    def getTargetsAndValues(self, IDName):
        """
        This function returns a dictionary with "targetPath:val" items, getting them
        from the human details stack.
        It's used to get both "before" and "after" dictionaries.
        @return: Dictionary
        @type  targets: List
        @param targets: List of targets to get
        """
        modifiers = self.getModifiers(IDName)

        targetsAndValues = {}
        for modifier in modifiers:
            targetsAndValues[modifier.left] = self.human.getDetail(modifier.left)
            targetsAndValues[modifier.right] = self.human.getDetail(modifier.right)
        return targetsAndValues

    def setModifierValue(self, value, IDName):
            """
            This function loads all asymmetry targets for the specified part of body
            (for example brown, eyes, etc..) and returns a dictionary with
            the applied targets, used as "after" parameter in undo system
            @return: Dictionary
            @type  value: Float
            @param value: The amount of asymmetry
            @type  IDName: String
            @param IDName: The name of part to asymmetrize.
            """
            modifiers = self.getModifiers(IDName)

            for modifier in modifiers:
                modifier.setValue(value)

    def getModifiers(self, IDName):
        modifiers = self.modifiers.get(IDName, None)
        if not modifiers:
            modifiers = []
            targets = self.buildListOfTargetPairs(IDName)
            for pair in targets:
                modifier = humanmodifier.Modifier(self.human, pair[0], pair[1])
                modifiers.append(modifier)
            self.modifiers[IDName] = modifiers
        return modifiers

    def getSliderValue(self, IDName):
        modifiers = self.modifiers[IDName]
        if modifiers:
            return modifiers[0].getValue()
        else:
            return 0.0

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        self.neckCircumferenceSlider.setFocus()
        self.syncSliders()

        #Update the measures when the measure mode is activated
        self.updateMeasures()

    def syncSliders(self):
        self.neckCircumferenceSlider.setValue(self.getSliderValue('neckcirc'))
        self.neckHeightSlider.setValue(self.getSliderValue('neckheight'))
        self.upperArmCircumferenceSlider.setValue(self.getSliderValue('upperarm'))
        self.wristCircumferenceSlider.setValue(self.getSliderValue('wrist'))
        self.frontChestSlider.setValue(self.getSliderValue('frontchest'))
        self.bustCircumferenceSlider.setValue(self.getSliderValue('bust'))
        self.underBustCircumferenceSlider.setValue(self.getSliderValue('underbust'))
        self.waistCircumferenceSlider.setValue(self.getSliderValue('waist'))
        self.napeToWaistSlider.setValue(self.getSliderValue('napetowaist'))
        self.waistToHipSlider.setValue(self.getSliderValue('waisttohip'))
        self.shoulderDistanceSlider.setValue(self.getSliderValue('shoulder'))
        self.upperLegHeightSlider.setValue(self.getSliderValue('upperlegheight'))
        self.lowerLegHeightSlider.setValue(self.getSliderValue('lowerlegheight'))
        self.calfSlider.setValue(self.getSliderValue('calf'))
        self.ankleSlider.setValue(self.getSliderValue('ankle'))
        self.upperArmLenghtSlider.setValue(self.getSliderValue('upperarmlenght'))
        self.lowerarmLenghtSlider.setValue(self.getSliderValue('lowerarmlenght'))
        self.upperThighSlider.setValue(self.getSliderValue('thighcirc'))


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
    taskview = MeasureTaskView(category)
    
    print 'Asymm loaded'
    allSliders = [taskview.neckGroup,
                    taskview.upperArmGroup,
                    taskview.lowerArmGroup,
                    taskview.torsoGroup,
                    taskview.upperLegGroup,
                    taskview.lowerLegGroup,
                    taskview.ankleGroup,
                    taskview.hipsGroup]

    def hideAllSliders():
        for slider in allSliders:
            slider.hide()

    def showAllSliders():
        for slider in allSliders:
            slider.show()

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
            trans[0] += 0.1 * diff[0]
            trans[1] -= 0.1 * diff[1]
            human.setPosition(trans)

    @taskview.event
    def onMouseDown(event):        
        part = app.scene3d.getSelectedFacesGroup()
        bodyZone = app.scene3d.selectedHuman.getPartNameForGroupName(part.name)
        print bodyZone
        if bodyZone in app.scene3d.selectedHuman.bodyZones:            
            if bodyZone == "neck":
                hideAllSliders()
                taskview.neckGroup.show()
            elif (bodyZone == "r-upperarm") or (bodyZone == "l-upperarm"):
                hideAllSliders()
                taskview.upperArmGroup.show()
            elif (bodyZone == "r-lowerarm") or (bodyZone == "l-lowerarm"):
                hideAllSliders()
                taskview.lowerArmGroup.show()
            elif (bodyZone == "torso") or (bodyZone == "pelvis"):
                hideAllSliders()
                taskview.torsoGroup.show()               
            elif bodyZone == "hip":
                hideAllSliders()
                taskview.hipsGroup.show() 
            elif (bodyZone == "l-upperleg") or (bodyZone == "r-upperleg"):
                hideAllSliders()
                taskview.upperLegGroup.show() 
            elif (bodyZone == "l-lowerleg") or (bodyZone == "r-lowerleg"):
                hideAllSliders()
                taskview.lowerLegGroup.show() 
            elif (bodyZone == "l-foot") or (bodyZone == "r-foot"):
                hideAllSliders()
                taskview.ankleGroup.show() 
            else:
                hideAllSliders()
                
    hideAllSliders()
    taskview.torsoGroup.show()



class Ruler:

    """
  This class contains ...
  """

    def __init__(self, human):

    # these are tables of vertex indices for each body measurement of interest

        self.Measures = {}
        self.Measures['thighcirc'] = [7066,7205,7204,7192,7179,7176,7166,6886,7172,6813,7173,7101,7033,7032,7041,7232,7076,7062,7063,7229,7066]
        self.Measures['neckcirc'] = [3131,3236,3058,3059,2868,2865,3055,3137,5867,2857,3483,2856,3382,2916,2915,3417,8186,10347,10786,
                                    10785,10373,10818,10288,10817,9674,10611,10809,10806,10674,10675,10515,10614]
        self.Measures['neckheight'] = [8184,8185,8186,8187,7463]
        self.Measures['upperarm']=[10701,10700,10699,10678,10337,10334,10333,10330,10280,10331,10702,10708,9671,10709,10329,10328]
        self.Measures['wrist']=[9894,9895,9607,9606,9806,10512,10557,9807,9808,9809,9810,10565,9653,9682,9681,9832,10507]
        self.Measures['frontchest']=[2961,10764]
        self.Measures['bust']=[6908,3559,3537,3556,3567,3557,4178,3558,4193,3561,3566,3565,3718,3563,2644,4185,2554,4169,2553,3574,2634,2653,3466,3392,
                2942,3387,4146,4433,2613,10997,9994,10078,10368,10364,10303,10380,10957,10976,10218,11055,10060,11054,10044,10966,10229,10115,
                10227,10226,10231,10036,10234,10051,10235,10225,10236,10255,10233]
        self.Measures['napetowaist']=[7463,7472]
        self.Measures['waisttohip']=[4681,6575]
        self.Measures['shoulder'] = [10819,10816,10021,10821,10822,10693,10697]
        self.Measures['underbust'] = [7245,3583,6580,3582,3705,3581,3411,3401,3467,4145,2612,10998,10080,10302,10366,10356,10352,10362,10361,10350,10260,10349,7259]
        self.Measures['waist'] = [6853,4682,3529,2950,3702,3594,3405,5689,3587,4466,6898,9968,10086,9970,10359,10197,10198,10130,10771,10263,6855]
        self.Measures['upperlegheight'] = [6755,7026]
        self.Measures['lowerlegheight'] = [6866,13338]
        self.Measures['calf'] = [7141,7142,7137,6994,6989,6988,6995,6997,6774,6775,6999,6803,6974,6972,6971,7002,7140,7139]
        self.Measures['ankle'] = [6938,6937,6944,6943,6948,6784,6935,6766,6767,6954,6799,6955,6958,6949,6952,6941]
        self.Measures['upperarmlenght'] = [9945,10696]
        self.Measures['lowerarmlenght'] = [9696,9945]
        self.Measures['hips'] = [7298,2936,3527,2939,2940,3816,3817,3821,4487,3822,3823,3913,3915,4506,5688,4505,4504,4503,6858,6862,6861,6860,
                                            6785,6859,7094,7096,7188,7189,6878,7190,7194,7195,7294,7295,7247,7300]

        self.humanoid = human

    def getMeasure(self, measurementname):
        measure = 0
        vindex1 = self.Measures[measurementname][0]
        for vindex2 in self.Measures[measurementname]:
            measure += aljabr.vdist(self.humanoid.mesh.verts[vindex1].co, self.humanoid.mesh.verts[vindex2].co)
            vindex1 = vindex2
        return 10.0 * measure






