import os.path
#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import os
import random
import algos3d
import mh



class AsymmAction:

    def __init__(self, human, targets, values):
        """
        Init function.

        @return: None
        @type  human: Human object
        @param human: The makehuman human model.
        @type  targets: List
        @param targets: A list with the names of targets used for the asymmetry action.
        """
        self.name = "asymm"
        self.human = human
        self.before ={}
        for t in targets:
            try:
                v = self.human.targetsDetailStack[t]
            except:
                v = 0
            self.before[t] = v            
        self.after = values
        

    def applyAsymm(self,asymDict):
        """
        This function apply all asymmetry targets, passed using a dictionary,
        and update the human target stack.

        @return: None
        @type  asymDict: Dictonary
        @param asymDict: A dictionary with targetpath:val items.
        """
        for k, v in asymDict.items():           
            self.human.targetsDetailStack[k] = v
        self.human.applyAllTargets(self.human.app.progress)

    def do(self):
        self.applyAsymm(self.after)
        return True

    def undo(self):
        self.applyAsymm(self.before)
        return True


class AsymmTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Asymm', category.app.getThemeResource('images', 'button_asymm.png'), category.app.getThemeResource('images', 'button_asymm_on.png'))

        #Sliders
        self.asymmFaceSlider = gui3d.Slider(self,  position=[20, 150, 9.3], value=0.5, label="Face asymmetry")

        self.asymmDataPath = "data/targets/asym/"
        self.asymmetryAllTargets = []
        self.asymmetryFaceTargets = []

        @self.asymmFaceSlider.event
        def onChange(value):
            self.app.do(AsymmAction(self.app.scene3d.selectedHuman, self.asymmetryAllTargets, self.calcAsymm(value,"face")))




    def calcAsymm(self, value, bodypart):
        """
        This function load all asymmetryc targets for the specified part of body
        (for example face, trunk, etc..) and return a dictionary with targetPath:val items.
        The targets are randomly applyed, using the val coefficient.

        @return: Dictonary
        @type  value: Float
        @param value: The amount of asymmetry
        @type  bodypart: String
        @param bodypart: The name of part to asymmetrize. Note it must be the same of the folder
                        that contain the asymmetry targets.
        """

        #We use a set to overwrite double targets, in order to avoid left and right are applied in the same time.
        asymmZones = set()
        asymmDataPartPath = os.path.join(self.asymmDataPath,bodypart)
        targetsList = os.listdir(asymmDataPartPath)
        for t in targetsList:
            tPath = os.path.join(asymmDataPartPath, t)
            if os.path.isfile(tPath):
                self.asymmetryFaceTargets.append(tPath)
                self.asymmetryAllTargets.append(tPath)
                nameData = t.split("-")
                asymmZones.add(nameData[1]+"-"+ nameData[2])

        asymmPathAndVal = {}
        for t in asymmZones:
            asymmType = random.randint(1,2) #1 = left, 2 = right
            asymmValue = random.random()* value
            a = os.path.join(asymmDataPartPath,"asym-"+t+"-"+str(asymmType)+".target")
            asymmPathAndVal[a] = asymmValue
        return asymmPathAndVal


def load(app):
    category = app.getCategory('Advanced','button_advance.png','button_advance_on.png')
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
            trans[0] += 0.1 * diff[0]
            trans[1] -= 0.1 * diff[1]
            human.setPosition(trans)




