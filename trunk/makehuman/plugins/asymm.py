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



class AsymmAction:

    def __init__(self, human, callback, before, after):
        """
        Init function.

        @return: None
        @type  human: Human object
        @param human: The makehuman human model.
        @type  callback: Function
        @param callback: The function to be called in do and undo
        @type  before: Dictionary
        @param before: A dictionary with the target:value pairs, before the action
        @type  before: Dictionary
        @param before: A dictionary with the target:value pairs, after the action
        """
        self.name = "asymm"
        self.human = human
        self.before = before
        self.callback = callback
        self.after = after

    def do(self):
        self.callback(self.after)
        return True

    def undo(self):
        self.callback(self.before)
        return True


class AsymmTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Asymm', category.app.getThemeResource('images', 'button_asymm.png'), category.app.getThemeResource('images', 'button_asymm_on.png'))

        #Sliders       
        self.asymmBrownSlider = gui3d.Slider(self,  position=[20, 80, 9.3], value=0.0, min=-1.0, max=1.0, label="Brown asymmetry")
        self.asymmCheekSlider = gui3d.Slider(self,  position=[20, 120, 9.3], value=0.0, min=-1.0, max=1.0, label="Cheek asymmetry")
        self.asymmEarsSlider = gui3d.Slider(self,  position=[20, 160, 9.3], value=0.0, min=-1.0, max=1.0, label="Ears asymmetry")
        self.asymmEyeSlider = gui3d.Slider(self,  position=[20, 200, 9.3], value=0.0, min=-1.0, max=1.0, label="Eye asymmetry")
        self.asymmJawSlider = gui3d.Slider(self,  position=[20, 240, 9.3], value=0.0, min=-1.0, max=1.0, label="Jaw asymmetry")
        self.asymmMouthSlider = gui3d.Slider(self,  position=[20, 280, 9.3], value=0.0, min=-1.0, max=1.0, label="Mouth asymmetry")
        self.asymmNoseSlider = gui3d.Slider(self,  position=[20, 320, 9.3], value=0.0, min=-1.0, max=1.0, label="Nose asymmetry")
        self.asymmTempleSlider = gui3d.Slider(self,  position=[20, 360, 9.3], value=0.0, min=-1.0, max=1.0, label="Temple asymmetry")
        self.asymmTopSlider = gui3d.Slider(self,  position=[20, 400, 9.3], value=0.0, min=-1.0, max=1.0, label="Top asymmetry")
        self.asymmTrunkSlider = gui3d.Slider(self,  position=[20, 440, 9.3], value=0.0, min=-1.0, max=1.0, label="Trunk asymmetry")

        #Get a list with all targes (complete with path) used in asymm library
        self.asymmDataPath = "data/targets/asym/"
        self.asymmTargets = []
        for dir in os.listdir(self.asymmDataPath):
            if os.path.isdir(os.path.join(self.asymmDataPath, dir)) and dir != "svn":
                for f in os.listdir(os.path.join(self.asymmDataPath, dir)):
                    if os.path.isfile(os.path.join(self.asymmDataPath, dir, f)):
                        self.asymmTargets.append(os.path.join(self.asymmDataPath, dir, f))

        #The human mesh
        self.human = self.app.scene3d.selectedHuman

        #Random factor from Slider
        self.randomVal = 0.5

        #Sliders events

        @self.asymmBrownSlider.event
        def onChange(value):
            self.changeValue("brown",value)

        @self.asymmCheekSlider.event
        def onChange(value):
            self.changeValue("cheek",value)

        @self.asymmEarsSlider.event
        def onChange(value):
            self.changeValue("ear",value)

        @self.asymmEyeSlider.event
        def onChange(value):
            self.changeValue("eye",value)

        @self.asymmJawSlider.event
        def onChange(value):
            self.changeValue("jaw",value)

        @self.asymmMouthSlider.event
        def onChange(value):
            self.changeValue("mouth",value)

        @self.asymmNoseSlider.event
        def onChange(value):
            self.changeValue("nose",value)

        @self.asymmTempleSlider.event
        def onChange(value):
            self.changeValue("temple",value)

        @self.asymmTopSlider.event
        def onChange(value):
            self.changeValue("top",value)

        @self.asymmTrunkSlider.event
        def onChange(value):
            self.changeValue("trunk",value)


    def changeValue(self,bodyPartName,value):
        """
        This function apply the targets, and inform the undo system about the changes.
        @return: None
        @type  bodyPartName: String
        @param bodyPartName: Name of the body part to asymmetrise
        @type  value: Float
        @param value: The amount of asymmetry
        """
        before = self.getTargetsAndValues(self.asymmTargets)
        self.applyAsymm(self.calcAsymm(value,bodyPartName))
        after = self.getTargetsAndValues(self.asymmTargets)
        self.app.did(AsymmAction(self.human, self.applyAsymm, before, after))

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
                    f2 = os.path.join(dirPath, prefix+"-l.target")
                    pair = [f,f2]
                    pairs.append(pair)
        return pairs


    def getTargetsAndValues(self, targets):
        """
        This function return a dictionary with "targetPath:val" items, getting them
        from the human details stack.
        It's used to get both "before" and "after" dictionaries.
        @return: Dictionary
        @type  targets: List
        @param targets: List of targets to get
        """

        targetsAndValues = {}
        for t in targets:
            v = self.human.getDetail(t)
            targetsAndValues[t] = v
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
            targets = self.buildListOfTargetPairs(bodypart)
            targetsAndValues = {}
            for pair in targets:                
                humanmodifier.Modifier(self.human, pair[0], pair[1]).setValue(value)
                targetsAndValues[pair[0]] = self.human.getDetail(pair[0])
                targetsAndValues[pair[1]] = self.human.getDetail(pair[1])
            return targetsAndValues


    def applyAsymm(self,asymDict):
        """
        This function apply on the human the asymmetry targets, passed using
        a dictionary,  and update the human target stack.
        @return: None
        @type  asymDict: Dictonary
        @param asymDict: A dictionary with "targetpath:val" items.
        """
        for k, v in asymDict.items():
            self.human.targetsDetailStack[k] = v
        self.human.applyAllTargets(self.human.app.progress)



def load(app):
    """
    Plugin load function, needed by design.
    """
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




