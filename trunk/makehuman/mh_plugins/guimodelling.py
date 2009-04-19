"""
Module containing classes to handle modelling mode GUI operations.

===========================  ===============================================================
Project Name:                **MakeHuman**
Module File Location:        mh_plugins/guimodelling.py
Product Home Page:           http://www.makehuman.org/
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2008
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
===========================  ===============================================================

This module implements the 'guimodelling' class structures and methods to support GUI
Modelling mode operations.
Modelling mode is invoked by selecting the Modelling mode icon from the main GUI control
bar at the top of the screen.
While in this mode, user actions (keyboard and mouse events) are passed into
this class for processing. Having processed an event this class returns control to the
main OpenGL/SDL/Application event handling loop.

**IMPORTANT NOTE (13 mar 2009): Most parts of this plugin have been written quickly 
to respect the planned roadmap. Later we will clean it or even refactorize it.**

"""

__docformat__ = 'restructuredtext'


import files3d
import algos3d
import widgets3d, animation3d
import time
import subdivision
import mh2obj
import mh2bvh
import math
import os

class Action:
  """
  A short utility class to channel all operations through a single point so
  that a standardised undo and redo operation can be maintained.
  """
  def __init__(self, name, do, undo):
    """
    This is the constructor method for the action class. An instance of this 
    class is created each time the user performs an action affecting the model.
    That instance contains enough information to perform the action and enough 
    information to be able to undo the action.
    
    This method initializes the following attributes:

    - **self.name**: *string*. A string describing this action.
    - **self.do**: *string*. A string containing a method call and a set
      of parameters to perform an action on the model.
      Initialised to an the value passed on the method call.
    - **self.undo**: *string*. A string containing a method call and a set
      of parameters to undo an action on the model.

    Parameters
    ----------

    name:
        *string*. A string describing this action.
    do:
        *string*. A string containing a function name and a set
        of parameters to perform an action on the model.
    undo:
        *string*. A string containing a function name and a set
        of parameters to undo an action on the model.
        
    """
    self.name = name
    self.do = do
    self.undo = undo

   

class ListAction(Action):
    def __init__(self):
        self.actions=[]
        self.name = "foo"
    def append(self, action):
        self.actions.append(action)
    def do(self):        
        for action in self.actions:
            action.do()        
    def undo(self):        
        for action in self.actions:
            print(action.name)             
            action.undo()        
    def printActions(self):        
        for action in self.actions:
            print "Action: ", action.name
        
        


gModelling = None



class Guimodelling:
    """
    The data structures and methods to support the Modelling mode GUI.
    One instance of this class (named gModelling) is instantiated by main.py
    at application startup to handle user interaction with the MakeHuman GUI
    when in Modelling mode.
    """

    def __init__(self, globalScene, commonGUI = None):
        """
        This is the constructor method for the guimodelling class.
        It initializes the following attributes:

        - **self.modellingGUIObjs**: *object list*. A list of GUI objects.
          Initialised to an empty list then populated by calls to the
          *files3d.loadMesh* method.
        - **self.modifiedGUIObjs**: *object list*. A list of modified GUI
          objects.
          Default: Empty list.
        - **self.scene**: *Scene3D*. A reference to the global scene object
          passed in as a parameter to this constructor method.
        - **self.modellingTool**: *string*. A string to indicate modelling
          tool currently active.
        - **self.modellingType**: *string*. A string to indicate the type of 
          modelling currently being performed. 
          Initial value = "translation".        
        - **self.grabMode**: *??*. A?? (TBC). 
          Initial value = None.
        - **self.lastTargetTime**: *float*. A decimal value storing the time 
          since the mouse button was pressed on a target (TBC).
          Initial value = 0.
        - **self.totalmove**: *list of ints*. A list of 2 ints holding the x 
          and y movement since the mouse button was pressed (TBC).
          Initial value = [0,0].
        - **self.detailsMode**: *string*. A string indicating whether 
          the application is currently in "Macro", "Detail" or "MicroDetail" 
          Mode. 
          Initial value = "macro".
        - **self.ethnicMode**: *string*. A string indicating which 
          ethnic mode is currently selected (TBC). 
          Initial value = None.
        - **self.ethnicTargetsValues**: *array??*. An array containing the set 
          of ethnic targets currently applied (TBC). 
          Initial value = Empty array.
        - **self.ethnicTargetsToApply**: *dictionary*. An array containing the set 
          of ethnic targets to be applied (TBC). 
          Initial value = {"neutral":1.0}.
        - **self.ethnicTargetsColors**: *dictionary*. An array containing the set 
          of colors of ethnic targets to be applied (TBC). 
          Initial value = Empty array.
        - **self.ethnicIncreaseMode**: *int*. An integer indicating whether 
          the 'increase' or 'decrease' mode is currently set. 
          Initial value = 1.
        - **self.ethnicResetMode**: *string??*. An indicator showing 
          whether the ethnicity reset mode is currently selected. 
          Initial value = None.
        - **self.initMeshDone**: *string??*. An indicator showing 
          whether the mesh has been initialized. 
          Initial value = None.
        - **self.childVal**: *float*. A value, usually between 0 
          and 1 showing what proportion of the features of the current figure 
          are taken from the 'child' version of the morph target. 
          Initial value = 0.0.
        - **self.oldVal**: *float*. A value, usually between 0 
          and 1 showing what proportion of the features of the current figure 
          are taken from the 'old' version of the morph target.
          Initial value = 0.0.
        - **self.femaleVal**: *float*. A value, usually between 0 
          and 1 showing what proportion of the features of the current figure 
          are taken from the 'female' version of the morph target.
          Initial value = 0.57.
        - **self.maleVal**: *float*. A value, usually between 0 
          and 1 showing what proportion of the features of the current figure 
          are taken from the 'male' version of the morph target.
          Initial value = 0.57.
        - **self.flaccidVal**: *float*. A value, usually between 0 
          and 1 showing what proportion of the features of the current figure 
          are taken from the 'flaccid' version of the morph target.
          Initial value = 0.0.
        - **self.muscleVal**: *float*. A value, usually between 0 
          and 1 showing what proportion of the features of the current figure 
          are taken from the 'muscle' version of the morph target.
          Initial value = 0.0.
        - **self.overweightVal**: *float*. A value, usually between 0 
          and 1 showing what proportion of the features of the current figure 
          are taken from the 'overweight' version of the morph target.
          Initial value = 0.0.
        - **self.underweightVal**: *float*. A value, usually between 0 
          and 1 showing what proportion of the features of the current figure 
          are taken from the 'underweight' version of the morph target.
          Initial value = 0.0.
        - **self.childValDetails**: *float*. A value, usually between 0 
          and 1 showing what proportion of the detailed features of the current 
          figure are taken from the 'child' version of the morph target.
          Initial value = 0.0.
        - **self.oldValDetails**: *float*. A value, usually between 0 
          and 1 showing what proportion of the detailed features of the current 
          figure are taken from the 'old' version of the morph target.
          Initial value = 0.0.
        - **self.flaccidValDetails**: *float*. A value, usually between 0 
          and 1 showing what proportion of the detailed features of the current 
          figure are taken from the 'flaccid' version of the morph target.
          Initial value = 0.0.
        - **self.muscleValDetails**: *float*. A value, usually between 0 
          and 1 showing what proportion of the detailed features of the current 
          figure are taken from the 'muscle' version of the morph target.
          Initial value = 0.0.
        - **self.overweightValDetails**: *float*. A value, usually between 0 
          and 1 showing what proportion of the detailed features of the current 
          figure are taken from the 'overweight' version of the morph target.
          Initial value = 0.0.
        - **self.underweightValDetails**: *float*. A value, usually between 0 
          and 1 showing what proportion of the detailed features of the current 
          figure are taken from the 'underweight' version of the morph target.
          Initial value = 0.0.
        - **self.femaleValDetails**: *float*. A value, usually between 0 
          and 1 showing what proportion of the detailed features of the current 
          figure are taken from the 'female' version of the morph target.
          Initial value = 0.
        - **self.maleValDetails**: *float*. A value, usually between 0 
          and 1 showing what proportion of the detailed features of the current 
          figure are taken from the 'male' version of the morph target.
          Initial value = 0.
        - **self.undoStack**: *list of operations*. A list of 
          operations performed on the model by the user. 
          Initial value = Empty List.
        - **self.redoStack**: *list of operations*. A list of
          operations that have been undone by the user. Initial value = Empty List.
        - **self.targetsStack**: *dictionary*. A dict to all targets 
          applied, with their values. Initial value = Empty Dictionary.
        - **self.lastColoredFaces**: *list of faces*. A list of most 
          recently colored faces (TBC). Initial value = Empty List.
        - **self.bodyZones**: *dictionary*. A dictionary of the zones
          on the body to which detailed changes can be applied in modelling mode.
          Each dictionary entry contains a list of the faceGroups that that go to
          make up that zone on the body. 
          Initial value = Empty Dictionary.
        - **self.lastTargetApplied**: *index??*. A reference to the morph 
          target most recently applied (TBC). 
          Initial value = None.        
        - **self.bUndo**: *Object3D*. A reference to the GUI object 
          representing the Undo button.
        - **self.bAsia**: *Object3D*. A reference to the GUI object 
          representing the Asia button.
        - **self.bEurope**: *Object3D*. A reference to the GUI object 
          representing the Europe button.
        - **self.bAfrica**: *Object3D*. A reference to the GUI object 
          representing the Africa button.
        - **self.bAmerica**: *Object3D*. A reference to the GUI object 
          representing the America button.
        - **self.bEthnicIncr**: *Object3D*. A reference to the GUI object 
          representing the EthnicIncrbutton.
        - **self.bEthnicDecr**: *Object3D*. A reference to the GUI object 
          representing the EthnicDecr button.
        - **self.bEthnicReset**: *Object3D*. A reference to the GUI object 
          representing the EthnicReset button.
        - **self.bGender**: *Object3D*. A reference to the GUI object 
          representing the Gender button.
        - **self.bAge**: *Object3D*. A reference to the GUI object 
          representing the Age button.
        - **self.bMuscle**: *Object3D*. A reference to the GUI object 
          representing the Muscle button.
        - **self.bWeight**: *Object3D*. A reference to the GUI object 
          representing the Weight button.
        - **self.bMacroDetails**: *Object3D*. A reference to the GUI object 
          representing the MacroDetails tab.
        - **self.bDetails**: *Object3D*. A reference to the GUI object 
          representing the Details tab.
        - **self.bMicroDetails**: *Object3D*. A reference to the GUI object 
          representing the MicroDetails tab.
        - **self.prompt**: *Object3D*. A reference to the GUI object 
          representing the prompt ???(TBC).
        - **self.bTranslation**: *Object3D*. A reference to the GUI object 
          representing the Translation button.
        - **self.bScale**: *Object3D*. A reference to the GUI object 
          representing the Scale button.
        - **self.bSymmR**: *Object3D*. A reference to the GUI object 
          representing the SymmR button (Left to Right symmetry).
        - **self.bSymmL**: *Object3D*. A reference to the GUI object 
          representing the SymmL button (Right to Left symmetry).
        - **self.basemesh**:      *Object3D*. A reference to the
          base humanoid mesh object.

        Parameters
        ----------

        globalScene:
            *Scene3D*. A reference to the global scene object.
        commonGUI:
            *??*. Not Currently Used?. Default=None.
            
        """
        #TODO: validate comments of __init_:

        print "GUI modeling initialized"
        self.modellingGUIObjs = []
        self.modifiedGUIObjs = set()
        self.scene = globalScene
        
        self.listAction = ListAction()
        
        self.detailTargetX1a = None
        self.detailTargetX2a = None
        self.detailTargetY1a = None
        self.detailTargetY2a = None
        self.detailTargetZ1a = None
        self.detailTargetZ2a = None
        self.detailTargetX1b = None
        self.detailTargetX2b = None
        self.detailTargetY1b = None
        self.detailTargetY2b = None
        self.detailTargetZ1b = None
        self.detailTargetZ2b = None
        
        self.detailTarget1 = None
        self.detailTarget2 = None
        
        self.horizDeltaMov = []
        self.vertiDeltaMov = []

        self.modellingTool =  "trans-right"
        self.modellingType = "translation"
        self.viewType =  "FRONT_VIEW"

        self.grabMode = None
        self.lastTargetTime = 0
        self.totalmove = [0,0]
        

        self.detailsMode = "macro"
        self.ethnicMode = None
        self.ethnicTargetsValues = {}
        self.ethnicTargetsToApply = {"neutral":1.0}
        self.ethnicTargetsColors = {}
        self.ethnicIncreaseMode = 1
        self.ethnicResetMode = None
        self.initMeshDone = None
        self.childVal = 0.0 #child
        self.oldVal = 0.0  #old
        self.femaleVal = 0.57 #female
        self.maleVal = 0.57  #male
        self.flaccidVal = 0.0
        self.muscleVal = 0.0
        self.overweightVal = 0.0
        self.underweightVal = 0.0
        self.childValDetails = 0.0 #child
        self.oldValDetails = 0.0  #old
        self.flaccidValDetails = 0.0
        self.muscleValDetails = 0.0
        self.overweightValDetails = 0.0
        self.underweightValDetails = 0.0
        self.femaleValDetails = 0
        self.maleValDetails = 0
        self.undoStack = []
        self.redoStack = []
        self.targetsStack = {}#A dict to all targets applied, with their values
        self.lastColoredFaces = []
        self.bodyZones = {}
        self.lastTargetApplied = None


        self.bodyZones =  ["eye","jaw","nose","mouth","head","neck","torso",\
                        "hip","pelvis","r-upperarm","l-upperarm","r-lowerarm",\
                        "l-lowerarm","l-hand", "r-hand", "r-upperleg","l-upperleg",\
                        "r-lowerleg","l-lowerleg","l-foot","r-foot","ear"]



        self.background = files3d.loadMesh(self.scene,"data/3dobjs/background.obj", self.modellingGUIObjs,0,0,-70)
        self.bRedo = files3d.loadMesh(self.scene,"data/3dobjs/button_undo.obj",\
                            self.modellingGUIObjs,0.45,0.20,9)
        self.bUndo = files3d.loadMesh(self.scene,"data/3dobjs/button_redo.obj",\
                            self.modellingGUIObjs,0.37,0.20,9)
        self.bNew = files3d.loadMesh(self.scene,"data/3dobjs/button_new.obj",\
                            self.modellingGUIObjs,0.52,0.20,9)
        self.bAsia = files3d.loadMesh(self.scene,"data/3dobjs/button_asia.obj",\
                            self.modellingGUIObjs,0.45,0.12,9)
        self.bEurope = files3d.loadMesh(self.scene,"data/3dobjs/button_europe.obj",\
                            self.modellingGUIObjs,0.37,0.12,9)
        self.bAfrica = files3d.loadMesh(self.scene,"data/3dobjs/button_africa.obj",\
                            self.modellingGUIObjs,0.37,0.04,9)
        self.bAmerica = files3d.loadMesh(self.scene,"data/3dobjs/button_america.obj",\
                            self.modellingGUIObjs,0.45,0.04,9)
        self.bEthnicIncr = files3d.loadMesh(self.scene,"data/3dobjs/button_ethnincr.obj",\
                            self.modellingGUIObjs,0.52,0.12,9)
        self.bEthnicDecr = files3d.loadMesh(self.scene,"data/3dobjs/button_ethndecr.obj",\
                            self.modellingGUIObjs,0.52,0.07,9)
        self.bEthnicReset = files3d.loadMesh(self.scene,"data/3dobjs/button_ethnreset.obj",\
                            self.modellingGUIObjs,0.52,0.02,9)
        self.bGender = files3d.loadMesh(self.scene,"data/3dobjs/button_gender.obj", self.modellingGUIObjs,-0.45,0.25,9)
        self.bAge = files3d.loadMesh(self.scene,"data/3dobjs/button_age.obj", self.modellingGUIObjs,-0.45,0.1,9)
        self.bMuscle = files3d.loadMesh(self.scene,"data/3dobjs/button_muscle.obj", self.modellingGUIObjs,-0.45,-0.05,9)
        self.bWeight = files3d.loadMesh(self.scene,"data/3dobjs/button_weight.obj", self.modellingGUIObjs,-0.45,-0.20,9)
        self.bMacroDetails = files3d.loadMesh(self.scene,"data/3dobjs/button_macrodetails.obj",\
                            self.modellingGUIObjs,0.37,0.3,9)
        self.bDetails = files3d.loadMesh(self.scene,"data/3dobjs/button_details.obj",\
                            self.modellingGUIObjs,0.4425,0.3,9)
        self.bMicroDetails = files3d.loadMesh(self.scene,"data/3dobjs/button_microdetails.obj",\
                            self.modellingGUIObjs,0.515,0.3,9)
        self.prompt = files3d.loadMesh(self.scene,"data/3dobjs/prompt.obj",\
                            self.modellingGUIObjs,-0.51,0.33,6)
        self.bTranslation = files3d.loadMesh(self.scene,"data/3dobjs/button_transl.obj",\
                            self.modellingGUIObjs,0.37,0.12,9)
        self.bScale = files3d.loadMesh(self.scene,"data/3dobjs/button_scale.obj",\
                            self.modellingGUIObjs,0.45,0.12,9)
        self.bSymmR = files3d.loadMesh(self.scene,"data/3dobjs/button_symmright.obj",\
                            self.modellingGUIObjs,0.37,0.04,9)
        self.bSymmL = files3d.loadMesh(self.scene,"data/3dobjs/button_symmleft.obj",\
                            self.modellingGUIObjs,0.45,0.04,9)
        self.bGender.setTexture("data/images/button_gender_macro.png")
        self.bAge.setTexture("data/images/button_age_macro.png")
        self.bWeight.setTexture("data/images/button_weight_macro.png")
        self.bMuscle.setTexture("data/images/button_muscle_macro.png")
        self.bAfrica.setTexture("data/images/button_africa.png")
        self.bEurope.setTexture("data/images/button_europe.png")
        self.bAsia.setTexture("data/images/button_asia.png")
        self.bAmerica.setTexture("data/images/button_america.png")
        self.bEthnicIncr.setTexture("data/images/button_ethnincr.png")
        self.bEthnicDecr.setTexture("data/images/button_ethndecr.png")
        self.bEthnicReset.setTexture("data/images/button_ethnreset.png")
        self.bMicroDetails.setTexture("data/images/button_microdetails.png")
        self.bDetails.setTexture("data/images/button_details.png")
        self.bMacroDetails.setTexture("data/images/button_macrodetails.png")
        self.bTranslation.setTexture("data/images/button_translation_on.png")
        self.bScale.setTexture("data/images/button_scale.png")
        self.bSymmR.setTexture("data/images/button_symmright.png")
        self.bSymmL.setTexture("data/images/button_symmleft.png")
        self.bNew.setTexture("data/images/button_new.png")
        self.progressBar = widgets3d.ProgressBar(self.scene)#TODO Verify waht happen with multiple load of same obj

        self.bUndo.setTexture("data/images/button_undo.png")
        self.bRedo.setTexture("data/images/button_redo.png")

        self.progressBar.setVisibility(0)
        self.prompt.setText("Info:")
        self.basemesh = self.scene.getObject("base.obj")



    def grabVerts(self):
        """
        This method ....

        **Parameters:** This method has no parameters.

        """           
        
        
        leftButtonDown = self.scene.mouseState & 1

        if leftButtonDown:

            #if (0 < self.scene.mouseX < 760) and (0 < self.scene.mouseY) < 560:                
            diff = self.scene.getMouseDiff() 
            
            self.horizDeltaMov.append(diff[0])
            self.vertiDeltaMov.append(diff[1])
            
            self.totalmove[0] = sum(self.horizDeltaMov[-5:])
            self.totalmove[1] = sum(self.vertiDeltaMov[-5:])

            horizMov = math.fabs(self.totalmove[0])
            vertiMov = math.fabs(self.totalmove[1])

            mouseDirection = None           
            if self.viewType == "FRONTAL_VIEW":                    
                if horizMov > vertiMov:                        
                    if self.totalmove[0] > 0:
                        mouseDirection = "X-"
                    else:
                        mouseDirection = "X+"                            
                elif horizMov < vertiMov:                        
                    if self.totalmove[1] > 0:
                        mouseDirection = "Y-"
                    else:
                        mouseDirection = "Y+"                             
            if self.viewType == "BACK_VIEW":
                if horizMov > vertiMov:                        
                    if self.totalmove[0] > 0:
                        mouseDirection = "X+"
                    else:
                        mouseDirection = "X-"                            
                elif horizMov < vertiMov:                        
                    if self.totalmove[1] > 0:
                        mouseDirection = "Y-"
                    else:
                        mouseDirection = "Y+"
            if self.viewType == "LEFT_VIEW":
                if horizMov > vertiMov:                       
                    if self.totalmove[0] > 0:
                        mouseDirection = "Z+"
                    else:
                        mouseDirection = "Z-"                            
                elif horizMov < vertiMov:                        
                    if self.totalmove[1] > 0:
                        mouseDirection = "Y-"
                    else:
                        mouseDirection = "Y+"                            
            if self.viewType == "RIGHT_VIEW":
                if horizMov > vertiMov:                        
                    if self.totalmove[0] > 0:
                        mouseDirection = "Z-"
                    else:
                        mouseDirection = "Z+"
                elif horizMov < vertiMov:                        
                    if self.totalmove[1] > 0:
                        mouseDirection = "Y-"
                    else:
                        mouseDirection = "Y+"
                        
            if mouseDirection == "X+":
                self.detailTarget1 = self.detailTargetX1a
                self.detailTarget2 = self.detailTargetX2a
            elif mouseDirection == "X-":
                self.detailTarget1 = self.detailTargetX1b
                self.detailTarget2 = self.detailTargetX2b
            elif mouseDirection == "Y+":
                self.detailTarget1 = self.detailTargetY1a
                self.detailTarget2 = self.detailTargetY2a
            elif mouseDirection == "Y-":
                self.detailTarget1 = self.detailTargetY1b
                self.detailTarget2 = self.detailTargetY2b
            elif mouseDirection == "Z+":
                self.detailTarget1 = self.detailTargetZ1a
                self.detailTarget2 = self.detailTargetZ2a
            elif mouseDirection == "Z-":
                self.detailTarget1 = self.detailTargetZ1b
                self.detailTarget2 = self.detailTargetZ2b
                       
           
                         
        if time.time()-self.lastTargetTime > 0.025:          
            if self.detailTarget1 and self.detailTarget2:
                #if self.detailTarget2 is present, decrement it
                if self.detailTarget2 in self.targetsStack.keys() and self.targetsStack[self.detailTarget2] > 0:
                    prevVal = self.targetsStack[self.detailTarget2]
                    newVal = max(0.0, prevVal-0.1)
                    if newVal <= 0.0:
                        del self.targetsStack[self.detailTarget2]
                    actionName = self.detailTarget2
                    act = Action(actionName,lambda:self.setDetailsTarget(actionName,newVal-prevVal,newVal),\
                        lambda:self.setDetailsTarget(actionName,prevVal-newVal,prevVal))
                        
                    act.do()
                    self.listAction.append(act)

                #if value self.detailTarget2 is not present, increment the self.detailTarget1
                else:            

                    if self.detailTarget1 in self.targetsStack.keys():
                        prevVal = self.targetsStack[self.detailTarget1]
                        newVal = min(1.0, prevVal+0.1)
                    else:
                        prevVal = 0
                        newVal = 0.1
                    if newVal <= 1.0 and (newVal - prevVal) > 0.001:
                        print(prevVal, newVal)
                        actionName = self.detailTarget1                        
                        act = Action(actionName,lambda:self.setDetailsTarget(actionName,newVal-prevVal,newVal),\
                            lambda:self.setDetailsTarget(actionName,prevVal-newVal,prevVal))
                        act.do()
                        self.listAction.append(act)
            self.lastTargetTime = time.time()
                


    def resetScene(self):
        
        print "RESET THE SCENE"
        self.childVal = 0.0 
        self.oldVal = 0.0
        self.femaleVal = 0.57
        self.maleVal = 0.57
        self.flaccidVal = 0.0
        self.muscleVal = 0.0
        self.overweightVal = 0.0
        self.underweightVal = 0.0        


        if self.detailsMode == "macro":
            self.colorFaceGroup(self.bGender,"0.57")
            self.colorFaceGroup(self.bAge,"0.0")
            self.colorFaceGroup(self.bWeight,"0.0")
            self.colorFaceGroup(self.bMuscle,"0.0")
            

        if self.detailsMode == "regular":
            self.bGender.setTexture("data/images/button_gender.png")
            self.bWeight.setTexture("data/images/button_weight.png")
            self.bMuscle.setTexture("data/images/button_muscle.png")
            self.bAge.setTexture("data/images/button_age.png")
            self.bScale.setTexture("data/images/button_scale.png")
            self.cursor.setTexture("data/images/cursor_age.png")
        
        for t in self.ethnicTargetsValues.keys():
            self.ethnicTargetsValues[t] = 0.0            
                
        for t in self.targetsStack.keys():
            self.targetsStack[t] = 0.0

        
        self.applyCharacterTargets()
        self.applyDetailsTargets()

     



    def releaseLeftButton(self):
        """
        This method handles the release of the mouse button when in modelling 
        mode. If the user has been moving a body part it sets the resulting 
        position of that body part.

        **Parameters:** This method has no parameters.

        """
        self.bUndo.setTexture("data/images/button_undo.png")
        self.bRedo.setTexture("data/images/button_redo.png")
        if self.grabMode:
            self.grabMode = None
            #algos3d.loadTranslationTarget(self.basemesh, self.lastTargetApplied, 0.001,None, 1, 1)
            print "grab mode set to off"
            self.undoStack.append(self.listAction)
            self.listAction.printActions()
            self.listAction = None    
        self.totalmove = [0,0] 
        self.horizDeltaMov = []
        self.vertiDeltaMov = []
        
         




    def sceneMotion(self):
        """
        This method handles movements applied to the ?????.

        **Parameters:** This method has no parameters.

        """
        diff = self.scene.getMouseDiff()
        leftButtonDown = self.scene.mouseState & 1
        middleButtonDown = self.scene.mouseState & 2
        rightButtonDown = self.scene.mouseState & 4

        if not self.grabMode:
            if (leftButtonDown and rightButtonDown) or middleButtonDown:
                self.scene.setCameraZoom(self.scene.getCameraZoom() + 0.05 * diff[1])
            elif leftButtonDown:
                rot = self.scene.getCameraRotations()
                self.scene.setCameraRotations(rot[0] + 0.5 * diff[1], rot[1] + 0.5 * diff[0])
            elif rightButtonDown:
                trans = self.scene.getCameraTranslations()
                self.scene.setCameraTranslations(trans[0] + 0.05 * diff[0], trans[1] - 0.05 * diff[1])
        else:
            self.grabVerts()


    def subdivideBaseMesh(self):
        """
        This method toggles between displaying the standard mesh and a
        subdivided mesh. The subdivided mesh contains 4 times the number of
        faces as the standard mesh.

        **Parameters:** None.

        """

        if self.basemesh.isSubdivided:
            self.basemesh.isSubdivided = None
            sob = self.scene.getObject(self.basemesh.name+".sub")
            sob.setVisibility(0)
            self.basemesh.setVisibility(1)
        else:
            self.basemesh.isSubdivided = 1
            subdivision.subdivide(self.basemesh, self.scene)
            sob = self.scene.getObject(self.basemesh.name+".sub")
            sob.setVisibility(1)
            self.basemesh.setVisibility(0)
        self.scene.redraw()

    def colorFaceGroup(self, obj,faceGroupName):
        """
        This method applies a color to each face a face group and resets the 
        colors of any faces not in that face group.

        Parameters
        ----------

        obj:
            *Object3D*. The humanoid object.

        faceGroupName:
            *string*. The name of the face group to apply the color to.

        """
        found = False
        for faceGroup in obj.facesGroups:
            if float(faceGroup.name) == float(faceGroupName):
                for f in faceGroup.faces:
                    f.color = [[150,150,150,255], [150,150,150,255], [150,150,150,255]]
                    f.updateColors()
                found = True
            else:
                for f in faceGroup.faces:
                    f.color = f.color = [[255,255,255,255], [255,255,255,255], [255,255,255, 255]]
                    f.updateColors()
        self.scene.redraw()
        if not found:
            print("Warning, face group " + faceGroupName + " not found in " + obj.name + " possible values are")
            for faceGroup in obj.facesGroups:
                print(faceGroup.name)



    def changeCursorAndIcons(self,mode):
        """
        This method changes the cursor graphic and sets the icon graphics to
        correspond to the icon currently selected by the user.

        Parameters
        ----------

        mode:
            *string*. A string describing the GUI control that has just 
            been clicked.

        """
        #reset all icons
        self.bGender.setTexture("data/images/button_gender.png")
        self.bAge.setTexture("data/images/button_age.png")
        self.bWeight.setTexture("data/images/button_weight.png")
        self.bMuscle.setTexture("data/images/button_muscle.png")

        if mode == "male-incr":
            self.bGender.setTexture("data/images/button_gender_incr.png")
            self.cursor.setTexture("data/images/cursor_male_incr.png")
        if mode == "female-incr":
            self.bGender.setTexture("data/images/button_gender_decr.png")
            self.cursor.setTexture("data/images/cursor_female_incr.png")
        if mode == "age-incr":
            self.bAge.setTexture("data/images/button_age_incr.png")
            self.cursor.setTexture("data/images/cursor_age_incr.png")
        if mode == "age-decr":
            self.bAge.setTexture("data/images/button_age_decr.png")
            self.cursor.setTexture("data/images/cursor_age_decr.png")
        if mode == "weight-incr":
            self.bWeight.setTexture("data/images/button_weight_incr.png")
            self.cursor.setTexture("data/images/cursor_weight_incr.png")
        if mode == "weight-decr":
            self.bWeight.setTexture("data/images/button_weight_decr.png")
            self.cursor.setTexture("data/images/cursor_weight_decr.png")
        if mode == "muscle-incr":
            self.bMuscle.setTexture("data/images/button_muscle_incr.png")
            self.cursor.setTexture("data/images/cursor_muscle_incr.png")
        if mode == "muscle-decr":
            self.bMuscle.setTexture("data/images/button_muscle_decr.png")
            self.cursor.setTexture("data/images/cursor_muscle_decr.png")



    def setGenderVals(self,amount,faceGroupName):
        """
        This method applies gender attributes to a whole figure or, when 
        in details mode, to a selected part of a figure.

        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.

        faceGroupName:
            *string*. The name of the face group to apply the attribute
            to when in detail mode.


        """
        #TODO validate comment
        if self.detailsMode == "macro":
            if self.maleVal == amount:
                return False
            self.maleVal =  amount
            self.femaleVal = 1 - amount
            self.colorFaceGroup(self.bGender,faceGroupName)
            self.applyCharacterTargets()

        if self.detailsMode == "regular":
            self.bAge.setTexture("data/images/button_age.png")
            self.bWeight.setTexture("data/images/button_weight.png")
            self.bMuscle.setTexture("data/images/button_muscle.png")
            self.bGender.setTexture("data/images/button_gender_on.png")
            self.bTranslation.setTexture("data/images/button_translation.png")
            self.bScale.setTexture("data/images/button_scale.png")
            self.cursor.setTexture("data/images/cursor_gender.png")
            self.modellingType = "gender"
        return True

    def setAgeVals(self,amount,faceGroupName):
        """
        This method applies age attributes to a whole figure or, when 
        in details mode, to a selected part of a figure.

        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.

        faceGroupName:
            *string*. The name of the face group to apply the attribute
            to when in detail mode.


        """
        #TODO validate comment
        if self.detailsMode == "macro":
            if amount >= 0:
                if self.oldVal == amount and self.childVal == 0:
                    return False
                self.oldVal = amount
                self.childVal = 0
            else:
                if self.childVal == -amount and self.oldVal == 0:
                    return False
                self.childVal = -amount
                self.oldVal = 0
            self.modellingTool = None
            self.applyCharacterTargets()
            self.colorFaceGroup(self.bAge,faceGroupName)

        if self.detailsMode == "regular":
            self.bGender.setTexture("data/images/button_gender.png")
            self.bWeight.setTexture("data/images/button_weight.png")
            self.bMuscle.setTexture("data/images/button_muscle.png")
            self.bAge.setTexture("data/images/button_age_on.png")
            self.bTranslation.setTexture("data/images/button_translation.png")
            self.bScale.setTexture("data/images/button_scale.png")
            self.cursor.setTexture("data/images/cursor_age.png")
            self.modellingType = "age"
        return True

    def setWeightVals(self,amount,faceGroupName):
        """
        This method applies weight attributes to a whole figure or, when 
        in details mode, to a selected part of a figure.

        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.

        faceGroupName:
            *string*. The name of the face group to apply the attribute
            to when in detail mode.
        """
        #TODO validate comment

        if self.detailsMode == "macro":
            if amount >= 0:
                if self.overweightVal == amount and self.underweightVal == 0:
                    return False
                self.overweightVal = amount
                self.underweightVal = 0
            else:
                if self.underweightVal == -amount and self.overweightVal == 0:
                    return False
                self.underweightVal = -amount
                self.overweightVal = 0
            self.modellingTool = None
            self.colorFaceGroup(self.bWeight,faceGroupName)
            self.applyCharacterTargets()

        if self.detailsMode == "regular":
            self.bGender.setTexture("data/images/button_gender.png")
            self.bAge.setTexture("data/images/button_age.png")
            self.bMuscle.setTexture("data/images/button_muscle.png")
            self.bWeight.setTexture("data/images/button_weight_on.png")
            self.bTranslation.setTexture("data/images/button_translation.png")
            self.bScale.setTexture("data/images/button_scale.png")
            self.cursor.setTexture("data/images/cursor_weight.png")
            self.modellingType = "weight"
        return True

    def setToneVals(self, amount, faceGroupName):
        """
        This method applies muscle tone attributes to a whole figure or, when 
        in details mode, to a selected part of a figure.

        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.

        faceGroupName:
            *string*. The name of the face group to apply the attribute
            to when in detail mode.
        """
        #TODO validate comment
        print("setToneVals", amount, faceGroupName)

        if self.detailsMode == "macro":
            if amount >= 0:
                if self.muscleVal == amount and self.flaccidVal == 0:
                    return False
                self.muscleVal = amount
                self.flaccidVal = 0
            else:
                if self.flaccidVal == -amount and self.muscleVal == 0:
                    return False
                self.flaccidVal = -amount
                self.muscleVal = 0

            self.modellingTool = None
            self.colorFaceGroup(self.bMuscle,faceGroupName)
            self.applyCharacterTargets()
        if self.detailsMode == "regular":
            self.bGender.setTexture("data/images/button_gender.png")
            self.bAge.setTexture("data/images/button_age.png")
            self.bWeight.setTexture("data/images/button_weight.png")
            self.bMuscle.setTexture("data/images/button_muscle_on.png")
            self.bTranslation.setTexture("data/images/button_translation.png")
            self.bScale.setTexture("data/images/button_scale.png")
            self.cursor.setTexture("data/images/cursor_tone.png")
            self.modellingType = "muscle"
        return True

    def modifyGender(self):
        """
        This method applies gender attributes to a whole figure. 
        It creates a new instance of the Action class containing a method 
        definition that sets a new gender value and a method definition to 
        undo that change. It then calls the 'do' method on this class to 
        perform the action and to push the action onto the undo stack.
        
        The new gender value is picked up from the part of the GUI control 
        that has been selected. For example, the part of the GUI control 
        representing 28% Male is named '0.28', so that name is taken from 
        the currently selected face group on the control and converted 
        into a numeric value.

        **Parameters:** None.

        """
        faceGroupName = self.scene.getSelectedFacesGroup().name

        prevVal = self.maleVal
        newVal = float(faceGroupName)
        self.do(Action("Modify Gender",\
                lambda:self.setGenderVals(newVal,faceGroupName),\
                lambda:self.setGenderVals(prevVal,str(prevVal))))
        self.scene.redraw()

    def modifyAge(self):
        """
        This method applies age attributes to a whole figure. 
        It creates a new instance of the Action class containing a method 
        definition that sets a new age value and a method definition to 
        undo that change. It then calls the 'do' method on this class to 
        perform the action and to push the action onto the undo stack.
        
        The new age value is picked up from the part of the GUI control 
        that has been selected. For example, the part of the GUI control 
        representing 25 years old is named '25', so that name is taken from 
        the currently selected face group on the control and converted 
        into a numeric value.

        **Parameters:** None.

        """
        #TODO validate comment
        faceGroupName = self.scene.getSelectedFacesGroup().name
        if self.oldVal:
            prevVal = self.oldVal
        elif self.childVal:
            prevVal = -self.childVal
        else:
            prevVal = 0.0
        newVal = float(faceGroupName)
        self.do(Action("Modify Age",\
               lambda:self.setAgeVals(newVal,faceGroupName),\
               lambda:self.setAgeVals(prevVal,str(prevVal))))
        self.scene.redraw()

    def modifyWeight(self):
        """
        This method applies weight attributes to a whole figure. 
        It creates a new instance of the Action class containing a method 
        definition that sets a new weight value and a method definition to 
        undo that change. It then calls the 'do' method on this class to 
        perform the action and to push the action onto the undo stack.
        
        The new weight value is picked up from the part of the GUI control 
        that has been selected. For example, the part of the GUI control 
        representing 75% fat is named '0.75', so that name is taken from 
        the currently selected face group on the control and converted 
        into a numeric value.

        **Parameters:** None.

        """
        #TODO validate comment
        faceGroupName = self.scene.getSelectedFacesGroup().name
        if self.overweightVal:
            prevVal = self.overweightVal
        elif self.underweightVal:
            prevVal = -self.underweightVal
        else:
            prevVal = 0.0
        newVal = float(faceGroupName)
        self.do(Action("Modify Weight",\
                lambda:self.setWeightVals(newVal,faceGroupName),\
                lambda:self.setWeightVals(prevVal,str(prevVal))))
        self.scene.redraw()

    def modifyTone(self):
        """
        This method applies body tone attributes to a whole figure. 
        It creates a new instance of the Action class containing a method 
        definition that sets a new body tone value and a method definition to 
        undo that change. It then calls the 'do' method on this class to 
        perform the action and to push the action onto the undo stack.
        
        The new body tone value is picked up from the part of the GUI control 
        that has been selected. For example, the part of the GUI control 
        representing 25% good muscle tone is named '0.25', so that name is 
        taken from the currently selected face group on the control and 
        converted into a numeric value.

        **Parameters:** None.

        """
        #TODO validate comment
        faceGroupName = self.scene.getSelectedFacesGroup().name

        if self.muscleVal:
            prevVal = self.muscleVal
        elif self.flaccidVal:
            prevVal = -self.flaccidVal
        else:
            prevVal = 0.0
        newVal = float(faceGroupName)
        self.do(Action("Modify Tone",\
                lambda:self.setToneVals(newVal,faceGroupName),\
                lambda:self.setToneVals(prevVal,str(prevVal))))
        self.scene.redraw()

    def macroDetailsOn(self):
        """
        This method sets up the modelling mode screen with GUI elements 
        appropriate to large scale modelling and is invoked when
        the Macro tab is used in modelling mode (the default).

        **Parameters:** None.

        """
        #TODO validate comment

        self.prompt.setText("Mode: Macro Details")
        self.detailsMode = "macro"
        self.bMicroDetails.setTexture("data/images/button_microdetails.png")
        self.bDetails.setTexture("data/images/button_details.png")
        self.bMacroDetails.setTexture("data/images/button_macrodetails_over.png")
        self.bAge.setTexture("data/images/button_age_macro.png")
        self.bWeight.setTexture("data/images/button_weight_macro.png")
        self.bMuscle.setTexture("data/images/button_muscle_macro.png")
        self.bGender.setTexture("data/images/button_gender_macro.png")
        self.cursor.setTexture("data/images/cursor.png")
        self.colorFaceGroup(self.bGender,str(self.maleVal))
        self.colorFaceGroup(self.bAge,str(self.oldVal))
        self.colorFaceGroup(self.bWeight,str(self.overweightVal))
        self.colorFaceGroup(self.bMuscle,str(self.muscleVal))

        self.bAsia.setVisibility(1)
        self.bEurope.setVisibility(1)
        self.bAfrica.setVisibility(1)
        self.bAmerica.setVisibility(1)
        self.bTranslation.setVisibility(0)
        self.bScale.setVisibility(0)
        self.bEthnicIncr.setVisibility(1)
        self.bEthnicDecr.setVisibility(1)
        self.bEthnicReset.setVisibility(1)
        self.bSymmR.setVisibility(0)
        self.bSymmL.setVisibility(0)

        self.bGender.setVisibility(1)
        self.bAge.setVisibility(1)
        self.bWeight.setVisibility(1)
        self.bMuscle.setVisibility(1)
        
        algos3d.colorizeVerts(self.basemesh, [255,255,255,255], self.lastTargetApplied)

        self.scene.redraw()

    def microDetailsOn(self):
        """
        This method sets up the modelling mode screen with GUI elements 
        appropriate to micro-detail modelling and is invoked when the user 
        hits the MicroDetails tab when in modelling mode.

        **Parameters:** None.

        """
        #TODO validate comment
        self.prompt.setText("Mode: Micro Details")
        self.detailsMode = "micro"
        self.bMicroDetails.setTexture("data/images/button_microdetails_over.png")
        self.bDetails.setTexture("data/images/button_details.png")
        self.bMacroDetails.setTexture("data/images/button_macrodetails.png")
        #self.cursor.setTexture("data/images/cursor.png")

        self.bAsia.setVisibility(0)
        self.bEurope.setVisibility(0)
        self.bAfrica.setVisibility(0)
        self.bAmerica.setVisibility(0)
        self.bEthnicIncr.setVisibility(0)
        self.bEthnicDecr.setVisibility(0)
        self.bEthnicReset.setVisibility(0)
        self.bTranslation.setVisibility(1)
        self.bScale.setVisibility(1)
        self.bSymmR.setVisibility(1)
        self.bSymmL.setVisibility(1)

        self.bGender.setVisibility(0)
        self.bAge.setVisibility(0)
        self.bWeight.setVisibility(0)
        self.bMuscle.setVisibility(0)
        
        self.translateModeOn()
        algos3d.colorizeVerts(self.basemesh, [255,255,255,255], self.lastTargetApplied)
        self.scene.redraw()

    def detailsOn(self):
        """
        This method sets up the modelling mode screen with GUI elements 
        appropriate to detailed modelling and is invoked when the user hits
        the Details tab when in modelling mode.

        **Parameters:** None.

        """
        #TODO validate comment
        self.prompt.setText("Mode: Details")
        self.detailsMode = "regular"
        self.bMicroDetails.setTexture("data/images/button_microdetails.png")
        self.bDetails.setTexture("data/images/button_details_over.png")
        self.bMacroDetails.setTexture("data/images/button_macrodetails.png")
        self.bAge.setTexture("data/images/button_age.png")
        self.bWeight.setTexture("data/images/button_weight.png")
        self.bMuscle.setTexture("data/images/button_muscle.png")
        self.bGender.setTexture("data/images/button_gender.png")
        #self.cursor.setTexture("data/images/cursor.png")
        self.colorFaceGroup(self.bMuscle,"100") #face group 100 does not exist, so it reset the color
        self.colorFaceGroup(self.bAge,"100") #face group 100 does
        self.colorFaceGroup(self.bWeight,"100") #face group 100 does
        self.colorFaceGroup(self.bGender,"100") #face group 100 does

        self.bAsia.setVisibility(0)
        self.bEurope.setVisibility(0)
        self.bAfrica.setVisibility(0)
        self.bAmerica.setVisibility(0)
        self.bEthnicIncr.setVisibility(0)
        self.bEthnicDecr.setVisibility(0)
        self.bEthnicReset.setVisibility(0)
        self.bTranslation.setVisibility(1)
        self.bScale.setVisibility(1)
        self.bSymmR.setVisibility(1)
        self.bSymmL.setVisibility(1)

        self.bGender.setVisibility(1)
        self.bAge.setVisibility(1)
        self.bWeight.setVisibility(1)
        self.bMuscle.setVisibility(1)
        self.translateModeOn()
        algos3d.colorizeVerts(self.basemesh, [255,255,255,255], self.lastTargetApplied)
        self.scene.redraw()

    def translateModeOn(self):
        """
        This method records that the 'translate' button on the Details or the 
        MicroDetails tab in modelling mode has been pressed, so that
        subsequent user operations can be interpreted as translations of 
        selected body parts.

        **Parameters:** None.

        """
        #TODO validate comment
        self.prompt.setText("Mode: Transl Mode")
        self.modellingType = "translation"
        self.bTranslation.setTexture("data/images/button_translation_on.png")
        self.bScale.setTexture("data/images/button_scale.png")
        self.cursor.setTexture("data/images/cursor_trans.png")

    def scaleModeOn(self):
        """
        This method records that the 'scale' button on the Details or the 
        MicroDetails tab in modelling mode has been pressed, so that
        subsequent user operations on selected body parts can be 
        interpreted as 'scale' operations
        
        **Parameters:** None.

        """
        #TODO validate comment
        self.prompt.setText("Mode: Scale Mode")
        self.modellingType = "scale"
        self.bTranslation.setTexture("data/images/button_translation.png")
        self.bScale.setTexture("data/images/button_scale_on.png")
        self.cursor.setTexture("data/images/cursor_scale.png")



    def ethnicModeOn(self,button = None):
        """
        This method records that one of the 'ethnicity' maps or buttons has been 
        pressed on the Macro tab in modelling mode. If one of the maps has been 
        pressed it moves it to the centre of the screen and zooms in so that the 
        ethnic groups shown on the map become visible.       

        Parameters
        ----------

        button:
            *button*. A reference to the ethnicity button that has been pressed.

        """
        #TODO validate comment
        if self.ethnicIncreaseMode:
            self.cursor.setTexture("data/images/cursor_dna_incr.png")
        if self.ethnicResetMode:
            self.cursor.setTexture("data/images/cursor_dna_reset.png")
        if not self.ethnicResetMode and not self.ethnicIncreaseMode:
            self.cursor.setTexture("data/images/cursor_dna_decr.png")

        if not self.ethnicMode and button:
            t = animation3d.Timeline(0.250)
            t.append(animation3d.PathAction(button, [[button.x, button.y, button.z], [button.x - 0.40, button.y - 0.15, button.z]]))
            t.append(animation3d.ScaleAction(button, [1, 1, 1], [5, 5, 5]))
            t.append(animation3d.UpdateAction(self.scene))
            t.start()
            self.ethnicMode = 1

    def ethnicModeOff(self,button = None):
        """
        This method records that the 'close' button on a zoomed-in ethnic map 
        on the Macro tab in modelling mode has been pressed, returning that 
        map to its original position and zooming out so that it fits back 
        into its original location.
        
        Parameters
        ----------

        button:
            *button*. A reference to the ethnicity button that has been pressed.

        """
        #TODO validate comment
        if self.ethnicMode and button:
            #restore the original size
            t = animation3d.Timeline(0.250)
            t.append(animation3d.PathAction(button, [[button.x, button.y, button.z], [button.x + 0.40, button.y + 0.15, button.z]]))
            t.append(animation3d.ScaleAction(button, [5, 5, 5], [1, 1, 1]))
            t.append(animation3d.UpdateAction(self.scene))
            t.start()
            self.ethnicMode = None
            self.cursor.setTexture("data/images/cursor.png")

    def ethnicIncreaseModeOn(self):
        """
        This method records that the 'increase' button (the plus sign) next to 
        the ethnic map on the Macro tab in modelling mode has been pressed so
        that subsequent mouse clicks on a particular ethnic group will increase
        the proportion of ethnicity from that group in the current figure.
        
        **Parameters:** None.

        """
        #TODO validate comment
        self.bEthnicIncr.setTexture("data/images/button_ethnincr_on.png")
        self.bEthnicDecr.setTexture("data/images/button_ethndecr.png")
        self.bEthnicReset.setTexture("data/images/button_ethnreset.png")
        if self.ethnicMode:
            self.cursor.setTexture("data/images/cursor_dna_incr.png")
        self.ethnicIncreaseMode = 1
        self.ethnicResetMode = None

    def ethnicDecreaseModeOn(self):
        """
        This method records that the 'decrease' button (the minus sign) next to 
        the ethnic map on the Macro tab in modelling mode has been pressed so
        that subsequent mouse clicks on a particular ethnic group will decrease
        the proportion of ethnicity from that group in the current figure.
        
        **Parameters:** None.

        """
        self.bEthnicIncr.setTexture("data/images/button_ethnincr.png")
        self.bEthnicDecr.setTexture("data/images/button_ethndecr_on.png")
        self.bEthnicReset.setTexture("data/images/button_ethnreset.png")
        if self.ethnicMode:
            self.cursor.setTexture("data/images/cursor_dna_decr.png")
        self.ethnicIncreaseMode = None
        self.ethnicResetMode = None

    def ethnicResetModeOn(self):
        """
        This method records that the 'reset' button (the circular symbol) next 
        to the ethnic map on the Macro tab in modelling mode has been pressed 
        so that subsequent mouse clicks on a particular ethnic group will 
        remove any ethnicity from that group in the current figure.
        
        **Parameters:** None.

        """
        self.bEthnicIncr.setTexture("data/images/button_ethnincr.png")
        self.bEthnicDecr.setTexture("data/images/button_ethndecr.png")
        self.bEthnicReset.setTexture("data/images/button_ethnreset_on.png")
        if self.ethnicMode:
            self.cursor.setTexture("data/images/cursor_dna_reset.png")
        self.ethnicIncreaseMode = None
        self.ethnicResetMode = 1

    def applyCharacterTargets(self):

        """
        This method applies all targets, in function of age and sex
        
        **Parameters:** None.

        """

        targetName = None
        self.progressBar.setVisibility(1)
        algos3d.resetObj(self.basemesh)

        self.progressBar.setProgress(0.0)
        progressVal = 0.0
        progressIncr = 0.3/(len(self.targetsStack)+1)
        for t in self.targetsStack.keys():
            algos3d.loadTranslationTarget(self.basemesh, t, self.targetsStack[t],None,0,0)
            progressVal += progressIncr
            self.progressBar.setProgress(progressVal)
        a = time.time()
        #+.01 below to prevent zerodivision error
        progressIncr = (0.6/(len(self.ethnicTargetsToApply.keys())+.01))/6
        realAgeVal = 25
        if self.childVal > 0:
            realAgeVal = 25-(13*self.childVal)
        if self.oldVal > 0:
            realAgeVal = 25+(45*self.oldVal)
        infoText = "Male: %.2f; Female: %.2f; Age: %.2f "% (self.maleVal,\
                                                            self.femaleVal,\
                                                            realAgeVal)
        youngVal = 1-(self.oldVal + self.childVal)

        #NOTE: the "universal" targets work as addition with all other targets,
        #while the ethnic targets are absolute.
        targetFolder = "data/targets/macrodetails"
        targetsGeneral = {}

        targetFemaleFlaccidChild = "%s/universal-female-child-flaccid.target"%(targetFolder)
        targetFemaleFlaccidYoung = "%s/universal-female-young-flaccid.target"%(targetFolder)
        targetFemaleFlaccidOld = "%s/universal-female-old-flaccid.target"%(targetFolder)
        targetMaleFlaccidChild = "%s/universal-male-child-flaccid.target"%(targetFolder)
        targetMaleFlaccidYoung = "%s/universal-male-young-flaccid.target"%(targetFolder)
        targetMaleFlaccidOld = "%s/universal-male-old-flaccid.target"%(targetFolder)

        targetFemaleMuscleChild = "%s/universal-female-child-muscle.target"%(targetFolder)
        targetFemaleMuscleYoung = "%s/universal-female-young-muscle.target"%(targetFolder)
        targetFemaleMuscleOld = "%s/universal-female-old-muscle.target"%(targetFolder)
        targetMaleMuscleChild = "%s/universal-male-child-muscle.target"%(targetFolder)
        targetMaleMuscleYoung = "%s/universal-male-young-muscle.target"%(targetFolder)
        targetMaleMuscleOld = "%s/universal-male-old-muscle.target"%(targetFolder)

        targetFemaleOverweightChild = "%s/universal-female-child-overweight.target"%(targetFolder)
        targetFemaleOverweightYoung = "%s/universal-female-young-overweight.target"%(targetFolder)
        targetFemaleOverweightOld = "%s/universal-female-old-overweight.target"%(targetFolder)
        targetMaleOverweightChild = "%s/universal-male-child-overweight.target"%(targetFolder)
        targetMaleOverweightYoung = "%s/universal-male-young-overweight.target"%(targetFolder)
        targetMaleOverweightOld = "%s/universal-male-old-overweight.target"%(targetFolder)

        targetFemaleUnderweightChild = "%s/universal-female-child-underweight.target"%(targetFolder)
        targetFemaleUnderweightYoung = "%s/universal-female-young-underweight.target"%(targetFolder)
        targetFemaleUnderweightOld = "%s/universal-female-old-underweight.target"%(targetFolder)
        targetMaleUnderweightChild = "%s/universal-male-child-underweight.target"%(targetFolder)
        targetMaleUnderweightYoung = "%s/universal-male-young-underweight.target"%(targetFolder)
        targetMaleUnderweightOld = "%s/universal-male-old-underweight.target"%(targetFolder)

        targetsGeneral[targetFemaleFlaccidChild]= self.flaccidVal*self.childVal*self.femaleVal
        targetsGeneral[targetFemaleFlaccidYoung]= self.flaccidVal*youngVal*self.femaleVal
        targetsGeneral[targetFemaleFlaccidOld]= self.flaccidVal*self.oldVal*self.femaleVal
        targetsGeneral[targetMaleFlaccidChild]= self.flaccidVal*self.childVal*self.maleVal
        targetsGeneral[targetMaleFlaccidYoung]= self.flaccidVal*youngVal*self.maleVal
        targetsGeneral[targetMaleFlaccidOld]= self.flaccidVal*self.oldVal*self.maleVal

        targetsGeneral[targetFemaleMuscleChild]= self.muscleVal*self.childVal*self.femaleVal
        targetsGeneral[targetFemaleMuscleYoung]= self.muscleVal*youngVal*self.femaleVal
        targetsGeneral[targetFemaleMuscleOld]= self.muscleVal*self.oldVal*self.femaleVal
        targetsGeneral[targetMaleMuscleChild]= self.muscleVal*self.childVal*self.maleVal
        targetsGeneral[targetMaleMuscleYoung]= self.muscleVal*youngVal*self.maleVal
        targetsGeneral[targetMaleMuscleOld]= self.muscleVal*self.oldVal*self.maleVal

        targetsGeneral[targetFemaleOverweightChild]= self.overweightVal*self.childVal*self.femaleVal
        targetsGeneral[targetFemaleOverweightYoung]= self.overweightVal*youngVal*self.femaleVal
        targetsGeneral[targetFemaleOverweightOld]= self.overweightVal*self.oldVal*self.femaleVal
        targetsGeneral[targetMaleOverweightChild]= self.overweightVal*self.childVal*self.maleVal
        targetsGeneral[targetMaleOverweightYoung]= self.overweightVal*youngVal*self.maleVal
        targetsGeneral[targetMaleOverweightOld]= self.overweightVal*self.oldVal*self.maleVal

        targetsGeneral[targetFemaleUnderweightChild]= self.underweightVal*self.childVal*self.femaleVal
        targetsGeneral[targetFemaleUnderweightYoung]= self.underweightVal*youngVal*self.femaleVal
        targetsGeneral[targetFemaleUnderweightOld]= self.underweightVal*self.oldVal*self.femaleVal
        targetsGeneral[targetMaleUnderweightChild]= self.underweightVal*self.childVal*self.maleVal
        targetsGeneral[targetMaleUnderweightYoung]= self.underweightVal*youngVal*self.maleVal
        targetsGeneral[targetMaleUnderweightOld]= self.underweightVal*self.oldVal*self.maleVal

        for k in targetsGeneral.keys():
            tVal = targetsGeneral[k]
            algos3d.loadTranslationTarget(self.basemesh, k,tVal,None,0,0)

        for ethnicGroup in self.ethnicTargetsToApply.keys():
            ethnicVal = self.ethnicTargetsToApply[ethnicGroup]
            targetsEthnic = {}

            targetFemaleChild = "data/targets/macrodetails/%s-female-child.target"%(ethnicGroup)
            targetMaleChild = "data/targets/macrodetails/%s-male-child.target"%(ethnicGroup)
            targetFemaleOld = "data/targets/macrodetails/%s-female-old.target"%(ethnicGroup)
            targetMaleOld = "data/targets/macrodetails/%s-male-old.target"%(ethnicGroup)
            targetFemaleYoung = "data/targets/macrodetails/%s-female-young.target"%(ethnicGroup)
            targetMaleYoung = "data/targets/macrodetails/%s-male-young.target"%(ethnicGroup)

            targetsEthnic[targetFemaleChild] = self.femaleVal*self.childVal*ethnicVal
            targetsEthnic[targetMaleChild] = self.maleVal*self.childVal*ethnicVal
            targetsEthnic[targetFemaleOld] = self.femaleVal*self.oldVal*ethnicVal
            targetsEthnic[targetMaleOld]= self.maleVal*self.oldVal*ethnicVal
            targetsEthnic[targetFemaleYoung]= self.femaleVal*youngVal*ethnicVal
            targetsEthnic[targetMaleYoung]= self.maleVal*youngVal*ethnicVal

            for k in targetsEthnic.keys():
                tVal = targetsEthnic[k]
                progressVal = progressVal + progressIncr
                self.progressBar.setProgress(progressVal)
                algos3d.loadTranslationTarget(self.basemesh, k,tVal,None,0,0)

        #Update all verts
        facesToRecalculate = range(len(self.basemesh.faces))
        indicesToUpdate = range(len(self.basemesh.verts))
        self.basemesh.calcNormals(indicesToUpdate,facesToRecalculate,1)
        self.basemesh.update(indicesToUpdate)

        self.progressBar.setProgress(1.0)
        self.progressBar.setVisibility(0)
        for (k,v) in self.ethnicTargetsToApply.items():
            infoText += ", %s: %.2f"%(k,v)
        self.prompt.setText(infoText)

    def colorEthnicGroup(self, obj):
        """
        This method applies ethnic colors to the figure.
        
        Parameters
        ----------

        obj:
            *Object3D*. A reference to the humanoid figure.

        """
        #TODO validate and expand comment
        for faceGroupName in self.ethnicTargetsColors.keys():
            if "neutral" not in faceGroupName:
                faceGroup = obj.getFaceGroup(faceGroupName)
                color = self.ethnicTargetsColors[faceGroupName]
                for f in faceGroup.faces:
                    f.color = [color,color,color]
                    f.updateColors()

    def modifyEthnicFeature(self):
        """
        This method modifies an ethnic feature.
        
        **Parameters:** None.

        """
        #TODO validate and expand comment
        faceGroupSel = self.scene.getSelectedFacesGroup()
        faceGroupName = faceGroupSel.name
        #STEP1: Recognize the button
        if "africa" in faceGroupName:
            button = self.bAfrica
        #STEP2: If ethnicmode, work on character, else, active ethnicmode
        if self.ethnicMode:
            #STEP3; if not dummy zone, work on character, else ethnicModeOff
            if "dummy" not in faceGroupName:
                #Increase or decrease depending by ethnicIncreaseMode
                if self.ethnicIncreaseMode:
                    self.do(Action("Increase " + faceGroupName, self.modifyEthnicAction(faceGroupName, "increase"), self.modifyEthnicAction(faceGroupName, "decrease")))
                elif self.ethnicResetMode:
                    self.do(Action("Remove " + faceGroupName, self.modifyEthnicAction(faceGroupName, "reset"), self.modifyEthnicAction(faceGroupName, "reset")))
                else:
                    self.do(Action("Decrease " + faceGroupName, self.modifyEthnicAction(faceGroupName, "decrease"), self.modifyEthnicAction(faceGroupName, "increase")))
                self.applyCharacterTargets()
            else:
                self.ethnicModeOff(button)
        else:
            self.ethnicModeOn(button)

    def modifyEthnic(self, ethnic, amount):
        """
        This method modifies the amount of ethnicity that the model inherits 
        from a particular selected ethnic group.
        
        Parameters
        ----------

        ethnic:
            *target*. A particular ethnic group.

        amount:
            *float*. The amount of ethnicity to inherit from this group.

        """
        #TODO validate comment
        modified = None
        if amount > 0.0:
            if sum(self.ethnicTargetsValues.values()) < 1.0:
                if ethnic in self.ethnicTargetsValues:
                    self.ethnicTargetsValues[ethnic] = min(round(self.ethnicTargetsValues[ethnic] + amount, 1), 1.0)
                else:
                    self.ethnicTargetsValues[ethnic] = round(min(amount, 1.0 - sum(self.ethnicTargetsValues.values())), 1)
                modified = True
        else:
            if ethnic in self.ethnicTargetsValues:
                self.ethnicTargetsValues[ethnic] = max(round(self.ethnicTargetsValues[ethnic] + amount, 1), 0.0)
                if self.ethnicTargetsValues[ethnic] < 0.1:
                    del self.ethnicTargetsValues[ethnic]
                modified = True

        if modified:
            self.ethnicTargetsToApply = {}
            #Calculate the ethnic target value, and store it in dictionary
            for t in self.ethnicTargetsValues.keys():
                self.ethnicTargetsToApply[t] = self.ethnicTargetsValues[t]
                #for each facegroup recalculate the color
                self.ethnicTargetsColors[t] = [int(255*self.ethnicTargetsToApply[t]),\
                                                1-int(255*self.ethnicTargetsToApply[t]),\
                                                255,255]
            self.ethnicTargetsToApply["neutral"] = 1.0 - sum(self.ethnicTargetsValues.values())

            print(self.ethnicTargetsValues)
            print(self.ethnicTargetsToApply)

            #If the group was completely removed, the color is white
            if ethnic not in self.ethnicTargetsValues:
                self.ethnicTargetsColors[ethnic] = [255,255,255,255]

            if "africa" in ethnic:
                self.colorEthnicGroup(self.bAfrica)

            return True

        return False

    def modifyEthnicAction(self, ethnic, action):
        """
        This method modifies the amount of ethnicity that the model inherits 
        from a particular selected ethnic group.
        
        Parameters
        ----------

        ethnic:
            *target*. A particular ethnic group.

        action:
            *string*. A string indicating whether to increase, decrease or reset 
            the amount of ethnicity inherited from this group.

        """
        #TODO validate comment
        if action == "increase":
            return lambda: self.modifyEthnic(ethnic, 0.1)
        elif action == "decrease":
            return lambda: self.modifyEthnic(ethnic, -0.1)
        elif action == "reset":
            return lambda: self.modifyEthnic(ethnic, -1.0)

    def setDetailsTarget(self,targetPath,incrVal,totVal):
        """
        This method .....
        
        Parameters
        ----------

        targetPath:
            *path*. The full file system path to a target file.

        incrVal:
            *float*. The amount by which each change alters the model.

        totVal:
            *float*. ????.

        """
        #TODO insert comment
        print "DEBUG SETDETAILS",targetPath, incrVal
        self.targetsStack[targetPath] = totVal
        print "loading target %s with value %f"%(targetPath,incrVal)
        algos3d.loadTranslationTarget(self.basemesh, targetPath, incrVal,None, 1, 0)
        self.lastTargetApplied = targetPath
        return True


    def selectDetailTarget(self):
        """
        This method .....
        
        Parameters
        ----------

        partName:
            *???*. ???.

        """
        
        faceGroupName = self.scene.getSelectedFacesGroup().name
        print "Facegroup selected",faceGroupName
        self.grabMode = 1 
        self.viewType =  self.scene.getCameraFraming() 
        self.listAction = ListAction()        
        
        if  self.detailsMode == "macro":
            tFolder = "data/targets/macrodetails"
        if  self.detailsMode == "regular":
            tFolder = "data/targets/details/"
            for k in self.bodyZones:
                if k in faceGroupName:                
                    partName = k
                    break        
        if  self.detailsMode == "micro":
            tFolder = "data/targets/microdetails/"
            partName = faceGroupName

        if self.modellingType == "scale":
            #Targets X direction positive
            self.detailTargetX1a = "%s%s-scale-horiz-incr.target"%(tFolder,partName)
            self.detailTargetX2a = "%s%s-scale-horiz-decr.target"%(tFolder,partName)
            #Targets X direction negative
            self.detailTargetX1b = "%s%s-scale-horiz-decr.target"%(tFolder,partName)
            self.detailTargetX2b = "%s%s-scale-horiz-incr.target"%(tFolder,partName)
            #Targets Y direction positive
            self.detailTargetY1a = "%s%s-scale-vert-incr.target"%(tFolder,partName)
            self.detailTargetY2a = "%s%s-scale-vert-decr.target"%(tFolder,partName)
            #Targets Y direction negative
            self.detailTargetY1b = "%s%s-scale-vert-decr.target"%(tFolder,partName)
            self.detailTargetY2b = "%s%s-scale-vert-incr.target"%(tFolder,partName)
            #Targets Z direction positive
            self.detailTargetZ1a = "%s%s-scale-depth-incr.target"%(tFolder,partName)
            self.detailTargetZ2a = "%s%s-scale-depth-decr.target"%(tFolder,partName)
            #Targets Z direction negative
            self.detailTargetZ1b = "%s%s-scale-depth-decr.target"%(tFolder,partName)
            self.detailTargetZ2b = "%s%s-scale-depth-incr.target"%(tFolder,partName)               
            
        if self.modellingType == "translation":
            #Targets X direction positive
            self.detailTargetX1a = "%s%s-trans-in.target"%(tFolder,partName)
            self.detailTargetX2a = "%s%s-trans-out.target"%(tFolder,partName)
            #Targets X direction negative
            self.detailTargetX1b = "%s%s-trans-out.target"%(tFolder,partName)
            self.detailTargetX2b = "%s%s-trans-in.target"%(tFolder,partName)
            #Targets Y direction positive
            self.detailTargetY1a = "%s%s-trans-up.target"%(tFolder,partName)
            self.detailTargetY2a = "%s%s-trans-down.target"%(tFolder,partName)
            #Targets Y direction negative
            self.detailTargetY1b = "%s%s-trans-down.target"%(tFolder,partName)
            self.detailTargetY2b = "%s%s-trans-up.target"%(tFolder,partName)
            #Targets Z direction positive
            self.detailTargetZ1a = "%s%s-trans-forward.target"%(tFolder,partName)
            self.detailTargetZ2a = "%s%s-trans-backward.target"%(tFolder,partName)
            #Targets Z direction negative
            self.detailTargetZ1b = "%s%s-trans-backward.target"%(tFolder,partName)
            self.detailTargetZ2b = "%s%s-trans-forward.target"%(tFolder,partName)
            
        #OLD-YOUNG-FAT-SKNNY-FLABBY-MUSCLE BUTTONS
        if self.modellingType == "gender":
            #Targets X direction positive
            self.detailTargetX1a = "%s%s_male.target"%(tFolder,partName)
            self.detailTargetX2a = "%s%s_female.target"%(tFolder,partName)
            #Targets X direction positive
            self.detailTargetX1b = "%s%s_female.target"%(tFolder,partName)
            self.detailTargetX2b = "%s%s_male.target"%(tFolder,partName)
            #Same targets assigned to y and z mouse movements
            self.detailTargetY1a = self.detailTargetX1a
            self.detailTargetY2a = self.detailTargetX2a
            self.detailTargetY1b = self.detailTargetX1b
            self.detailTargetY2b = self.detailTargetX2b
            self.detailTargetZ1a = self.detailTargetZ1a
            self.detailTargetZ2a = self.detailTargetZ2a
            self.detailTargetZ1b = self.detailTargetZ1b
            self.detailTargetZ2b = self.detailTargetZ2b                

        if self.modellingType == "age":
            #Targets X direction positive
            self.detailTargetX1a = "%s%s_old.target"%(tFolder,partName)
            self.detailTargetX2a = "%s%s_child.target"%(tFolder,partName)
            #Targets X direction positive
            self.detailTargetX1b = "%s%s_child.target"%(tFolder,partName)
            self.detailTargetX2b = "%s%s_old.target"%(tFolder,partName)
            #Same targets assigned to y and z mouse movements
            self.detailTargetY1a = self.detailTargetX1a
            self.detailTargetY2a = self.detailTargetX2a
            self.detailTargetY1b = self.detailTargetX1b
            self.detailTargetY2b = self.detailTargetX2b
            self.detailTargetZ1a = self.detailTargetZ1a
            self.detailTargetZ2a = self.detailTargetZ2a
            self.detailTargetZ1b = self.detailTargetZ1b
            self.detailTargetZ2b = self.detailTargetZ2b          
           

        if self.modellingType == "muscle":
            #Targets X direction positive
            self.detailTargetX1a = "%s%s_muscle.target"%(tFolder,partName)
            self.detailTargetX2a = "%s%s_flaccid.target"%(tFolder,partName)
            #Targets X direction positive
            self.detailTargetX1b = "%s%s_flaccid.target"%(tFolder,partName)
            self.detailTargetX2b = "%s%s_muscle.target"%(tFolder,partName)
            #Same targets assigned to y and z mouse movements
            self.detailTargetY1a = self.detailTargetX1a
            self.detailTargetY2a = self.detailTargetX2a
            self.detailTargetY1b = self.detailTargetX1b
            self.detailTargetY2b = self.detailTargetX2b
            self.detailTargetZ1a = self.detailTargetZ1a
            self.detailTargetZ2a = self.detailTargetZ2a
            self.detailTargetZ1b = self.detailTargetZ1b
            self.detailTargetZ2b = self.detailTargetZ2b  


        if self.modellingType == "weight":                
            #Targets X direction positive
            self.detailTargetX1a = "%s%s_overweight.target"%(tFolder,partName)
            self.detailTargetX2a = "%s%s_underweight.target"%(tFolder,partName)
            #Targets X direction positive
            self.detailTargetX1b = "%s%s_underweight.target"%(tFolder,partName)
            self.detailTargetX2b = "%s%s_overweight.target"%(tFolder,partName)
            #Same targets assigned to y and z mouse movements
            self.detailTargetY1a = self.detailTargetX1a
            self.detailTargetY2a = self.detailTargetX2a
            self.detailTargetY1b = self.detailTargetX1b
            self.detailTargetY2b = self.detailTargetX2b
            self.detailTargetZ1a = self.detailTargetZ1a
            self.detailTargetZ2a = self.detailTargetZ2a
            self.detailTargetZ1b = self.detailTargetZ1b
            self.detailTargetZ2b = self.detailTargetZ2b               
        
        algos3d.colorizeVerts(self.basemesh, [255,255,255,255])
        algos3d.analyzeTarget(self.basemesh, self.detailTargetY1a)
        
       

            

    def applySymmetryLeft(self):
        """
        This method applies right to left symmetry to the currently selected 
        body parts.
        
        **Parameters:** None.

        """
        self.symmetrizeMicroDetails("l")
        #self.do(Action("Modify Tone",\
                #lambda:self.symmetrizeMicroDetails(newVal,faceGroupName),\
                #lambda:self.symmetrizeMicroDetails(prevVal,str(prevVal))))

    def applySymmetryRight(self):
        """
        This method applies left to right symmetry to the currently selected 
        body parts.
        
        **Parameters:** None.

        """
        self.symmetrizeMicroDetails("r")

    def symmetrizeMicroDetails(self,direction="r"):
        """
        This method applies either left to right or right to left symmetry to 
        the currently selected body parts.
        
        
        Parameters
        ----------

        direction:
            *string*. A string indicating whether to apply left to right 
            symmetry ("r") or right to left symmetry ("l").

        """
        #print "SYMMETRIZE START"
        if direction == "l":
            prefix1 = "l-"
            prefix2 = "r-"
        else:
            prefix1 = "r-"
            prefix2 = "l-"

        for target in self.targetsStack.keys():
            targetName = os.path.basename(target)
            #Reset previous targets on symm side
            if targetName[:2] == prefix2:
                algos3d.loadTranslationTarget(self.basemesh, target, -self.targetsStack[target],None,1,0)
                self.targetsStack[target] = 0

        #Apply symm target. For horiz movement the value must ve inverted
        for target in self.targetsStack.keys():
            targetName = os.path.basename(target)
            if targetName[:2] == prefix1:
                targetSym = os.path.join(os.path.dirname(target),prefix2+targetName[2:])
                targetSymVal = self.targetsStack[target]
                if "trans-in" in targetSym or "trans-out" in targetName:
                    targetSymVal *= -1

                algos3d.loadTranslationTarget(self.basemesh, targetSym, targetSymVal,None, 1, 1)
                self.targetsStack[targetSym] = targetSymVal

        self.scene.redraw()

   
        

    def isActive(self):
        """
        This method activates the 'Modelling Mode' GUI controls and
        connects events to them and to the handler methods of this
        class.

        **Parameters:** This method has no parameters.

        """
        #init of mesh gender and modelling mode: must be do only the first time
        self.cursor = self.scene.getObject("cursor.obj")
        if not self.initMeshDone:
            self.macroDetailsOn()
            self.ethnicIncreaseModeOn()
            targetFemale = "data/targets/macrodetails/neutral-female-young.target"
            targetMale = "data/targets/macrodetails/neutral-male-young.target"
            algos3d.loadTranslationTarget(self.basemesh, targetFemale,self.femaleVal)
            algos3d.loadTranslationTarget(self.basemesh, targetMale,self.maleVal)
            self.initMeshDone = 1

            self.colorFaceGroup(self.bGender,str(self.maleVal))
            self.colorFaceGroup(self.bAge,str(self.oldVal))
            self.colorFaceGroup(self.bWeight,str(self.overweightVal))
            self.colorFaceGroup(self.bMuscle,str(self.muscleVal))


        self.scene.connect("LMOUSEP",self.ethnicIncreaseModeOn,self.bEthnicIncr)
        self.scene.connect("LMOUSEP",self.ethnicResetModeOn,self.bEthnicReset)
        self.scene.connect("LMOUSEP",self.ethnicDecreaseModeOn,self.bEthnicDecr)
        self.scene.connect("LMOUSEP",self.selectDetailTarget,self.basemesh)
        self.scene.connect("LMOUSEP",self.macroDetailsOn,self.bMacroDetails)
        self.scene.connect("LMOUSEP",self.detailsOn,self.bDetails)
        self.scene.connect("LMOUSEP",self.microDetailsOn,self.bMicroDetails)
        self.scene.connect("LMOUSEP",self.modifyEthnicFeature,self.bAfrica)
        self.scene.connect("LMOUSEP",self.modifyAge,self.bAge)
        self.scene.connect("LMOUSEP",self.modifyWeight,self.bWeight)
        self.scene.connect("LMOUSEP",self.modifyTone,self.bMuscle)
        self.scene.connect("LMOUSEP",self.modifyGender,self.bGender)
        self.scene.connect("LMOUSEP",self.scaleModeOn,self.bScale)
        self.scene.connect("LMOUSEP",self.translateModeOn,self.bTranslation)
        self.scene.connect("LMOUSEP",self.doUndo,self.bUndo)
        self.scene.connect("LMOUSEP",self.doRedo,self.bRedo)
        self.scene.connect("LMOUSEP",self.applySymmetryLeft,self.bSymmL)
        self.scene.connect("LMOUSEP",self.applySymmetryRight,self.bSymmR)
        self.scene.connect("LMOUSEP",self.resetScene,self.bNew)


        #connect scene events to functions
        self.scene.connect("MOTION", self.sceneMotion)
        self.scene.connect("LMOUSER", self.releaseLeftButton)
        self.scene.connect("MOUSEWHEELDOWN", self.zoomIn)
        self.scene.connect("MOUSEWHEELUP", self.zoomOut)
        self.scene.connect("s", self.subdivideBaseMesh)
        self.scene.connect("q", self.scene.shutdown)
        self.scene.connect("z", self.undo)
        self.scene.connect("y", self.redo)
        self.scene.connect("e", self.export)
        self.scene.connect("8", self.rotateUp)
        self.scene.connect(self.scene.KP8, self.rotateUp)
        self.scene.connect("2", self.rotateDown)
        self.scene.connect(self.scene.KP2, self.rotateDown)
        self.scene.connect("4", self.rotateLeft)
        self.scene.connect(self.scene.KP4, self.rotateLeft)
        self.scene.connect("6", self.rotateRight)
        self.scene.connect(self.scene.KP6, self.rotateRight)
        self.scene.connect("UP_ARROW", self.panUp)
        self.scene.connect("DOWN_ARROW", self.panDown)
        self.scene.connect("LEFT_ARROW", self.panLeft)
        self.scene.connect("RIGHT_ARROW", self.panRight)
        self.scene.connect("+", self.zoomIn)
        self.scene.connect(self.scene.KP_PLUS, self.zoomIn)
        self.scene.connect("-", self.zoomOut)
        self.scene.connect(self.scene.KP_MINUS, self.zoomOut)
        self.scene.connect("7", self.topView)
        self.scene.connect(self.scene.KP7, self.topView)
        self.scene.connect("1", self.frontView)
        self.scene.connect(self.scene.KP1, self.frontView)
        self.scene.connect("3", self.sideView)
        self.scene.connect(self.scene.KP3, self.sideView)
        self.scene.connect(".", self.resetView)
        self.scene.connect(self.scene.KP_PERIOD, self.resetView)
        self.scene.connect("g", self.grabScreen)
        self.scene.connect("r", self.symmetrizeMicroDetails)



        self.bGender.setShadeless(1)
        self.bAge.setShadeless(1)
        self.bWeight.setShadeless(1)
        self.bMuscle.setShadeless(1)
        self.bAfrica.setShadeless(1)
        self.bEurope.setShadeless(1)
        self.bAsia.setShadeless(1)
        self.bAmerica.setShadeless(1)
        self.bMicroDetails.setShadeless(1)
        self.bDetails.setShadeless(1)
        self.bMacroDetails.setShadeless(1)
        self.prompt.setShadeless(1)
        self.bEthnicIncr.setShadeless(1)
        self.bEthnicDecr.setShadeless(1)
        self.bEthnicReset.setShadeless(1)
        self.bScale.setShadeless(1)
        self.bTranslation.setShadeless(1)
        self.bUndo.setShadeless(1)
        self.bRedo.setShadeless(1)
        self.bSymmL.setShadeless(1)
        self.bSymmR.setShadeless(1)
        self.background.setShadeless(1)
        self.bNew.setShadeless(1)

        for ob in self.modellingGUIObjs:
            ob.setCameraProjection(0)
            ob.setVisibility(1)

        self.bTranslation.setVisibility(0)
        self.bScale.setVisibility(0)
        self.bSymmR.setVisibility(0)
        self.bSymmL.setVisibility(0)

        self.basemesh.setVisibility(1)

    def isNotActive(self):
        """
        This method disactivates the 'Modelling Mode' GUI controls and
        disconnects events from them and from the handler methods of this
        class.

        **Parameters:** This method has no parameters.

        """
        #disconnect scene events to functions
        self.basemesh.setVisibility(0)
        self.scene.disconnect("MOTION")
        self.scene.disconnect("IDLE")
        self.scene.disconnect("s")
        self.scene.disconnect("q")
        self.scene.disconnect("z")
        self.scene.disconnect("y")
        self.scene.disconnect("e")
        self.scene.disconnect("8")
        self.scene.disconnect(self.scene.KP8)
        self.scene.disconnect("2")
        self.scene.disconnect(self.scene.KP2)
        self.scene.disconnect("4")
        self.scene.disconnect(self.scene.KP4)
        self.scene.disconnect("6")
        self.scene.disconnect(self.scene.KP6)
        self.scene.disconnect("UP_ARROW")
        self.scene.disconnect("DOWN_ARROW")
        self.scene.disconnect("LEFT_ARROW")
        self.scene.disconnect("RIGHT_ARROW")
        self.scene.disconnect("+")
        self.scene.disconnect(self.scene.KP_PLUS)
        self.scene.disconnect("-")
        self.scene.disconnect(self.scene.KP_MINUS)
        self.scene.disconnect("7")
        self.scene.disconnect(self.scene.KP7)
        self.scene.disconnect("1")
        self.scene.disconnect(self.scene.KP1)
        self.scene.disconnect("3")
        self.scene.disconnect(self.scene.KP3)
        self.scene.disconnect(".")
        self.scene.disconnect(self.scene.KP_PERIOD)

        for ob in self.modellingGUIObjs:
            ob.setVisibility(0)

        for ob in self.modellingGUIObjs:
            ob.setVisibility(0)

    def do(self, action):
        """
        This method provides a common wrapper for calling other methods so that
        the undo stack can be consistently maintained. An instance of the 
        Action class will have been defined during the call to this method so 
        that it contains a method call to perform an action and a method call to
        undo that action. The 'do' method is called straight away and the action
        is appended to the undo stack so that the 'undo' method can be used if 
        required. The redo stack is reset.  
                
        Parameters
        ----------

        action:
            *Action*. An instance of the Action class containing a 'do' method
            and an 'undo' method.

        """
        if action.do():
          self.undoStack.append(action)
          del self.redoStack[:]
          print("do " + action.name)
          self.scene.redraw()

    def undo(self):
        """
        This method responds to a Ctrl-Z keystroke, retrieving the last action 
        performed on the model from a stack and reversing that action to 
        implement undo functionality (see the 'doUndo' method for the 
        GUI button equivalent). 
        It also adds the action to the redo stack.
        
        **Parameters:** This method has no parameters.
    
        """
        if self.scene.getKeyModifiers() & (64 + 128):
            if self.undoStack:
                action = self.undoStack.pop()
                print("undo " + action.name)
                action.undo()
                self.redoStack.append(action)
                self.scene.redraw()
    
    def redo(self):
        """
        This method responds to a Ctrl-Y keystroke, retrieving the last 
        action undone and redoing that action on the model (see the 
        'doRedo' method for the GUI button equivalent). 
        It also adds the action to the undo stack.
        
        **Parameters:** This method has no parameters.
    
        """
        if self.scene.getKeyModifiers() & (64 + 128):
            if self.redoStack:
                action = self.redoStack.pop()
                print("redo " + action.name)
                action.do()
                self.undoStack.append(action)
                self.scene.redraw()

    def doUndo(self):
        """
        This method responds to the GUI undo button being pressed, retrieving
        the last action performed on the model from a stack and reversing that 
        action to implement undo functionality (see the 'undo' method for the 
        keystroke equivalent). 
        It also adds the action to the redo stack.
        
        **Parameters:** This method has no parameters.

        """
        self.bUndo.setTexture("data/images/button_undo_on.png")
        if self.undoStack:
            action = self.undoStack.pop()
            print("undo " + action.name)
            action.undo()
            self.redoStack.append(action)
            self.scene.redraw()

    def doRedo(self):
        """
        This method responds to the GUI redo button being pressed, retrieving 
        the last action undone and redoing that action on the model (see the 
        'redo' method for the keystroke equivalent).  
        It also adds the action to the undo stack.
        
        **Parameters:** This method has no parameters.

        """
        self.bRedo.setTexture("data/images/button_redo_on.png")
        if self.redoStack:
            action = self.redoStack.pop()
            print("redo " + action.name)
            action.do()
            self.undoStack.append(action)
            self.scene.redraw()

    def export(self):
        """
        This method exports the current model as an obj file and the 
        skeleton as a BVH file. 
        
        **Parameters:** This method has no parameters.

        """
        mh2obj.exportObj(self.basemesh, "export.obj")
        mh2bvh.exportSkeleton(self.basemesh, "export.bvh")

    def rotateUp(self):
        """
        This method rotates the camera by -5 degrees around the x-axis.
        
        **Parameters:** This method has no parameters.

        """
        rot = self.scene.getCameraRotations()
        self.scene.setCameraRotations(rot[0] - 5.0, rot[1])
        #self.updateTransformer()
        self.scene.redraw()

    def rotateDown(self):
        """
        This method rotates the camera by +5 degrees around the x-axis.
        
        **Parameters:** This method has no parameters.

        """
        rot = self.scene.getCameraRotations()
        self.scene.setCameraRotations(rot[0] + 5.0, rot[1])
        #self.updateTransformer()
        self.scene.redraw()

    def rotateLeft(self):
        """
        This method rotates the camera by -5 degrees around the y-axis.
        
        **Parameters:** This method has no parameters.

        """
        rot = self.scene.getCameraRotations()
        self.scene.setCameraRotations(rot[0], rot[1] - 5.0)
        #self.updateTransformer()
        self.scene.redraw()

    def rotateRight(self):
        """
        This method rotates the camera by +5 degrees around the y-axis.
        
        **Parameters:** This method has no parameters.

        """
        rot = self.scene.getCameraRotations()
        self.scene.setCameraRotations(rot[0], rot[1] + 5.0)
        #self.updateTransformer()
        self.scene.redraw()

    def panUp(self):
        """
        This method pans the camera by +0.05 units along the y-axis.
        
        **Parameters:** This method has no parameters.

        """
        trans = self.scene.getCameraTranslations()
        self.scene.setCameraTranslations(trans[0], trans[1] + 0.05)
        self.scene.redraw()

    def panDown(self):
        """
        This method pans the camera by -0.05 units along the y-axis.
        
        **Parameters:** This method has no parameters.

        """
        trans = self.scene.getCameraTranslations()
        self.scene.setCameraTranslations(trans[0], trans[1] - 0.05)
        self.scene.redraw()

    def panLeft(self):
        """
        This method pans the camera by -0.05 units along the x-axis.
        
        **Parameters:** This method has no parameters.

        """
        trans = self.scene.getCameraTranslations()
        self.scene.setCameraTranslations(trans[0] - 0.05, trans[1])
        self.scene.redraw()

    def panRight(self):
        """
        This method pans the camera by +0.05 units along the x-axis.
        
        **Parameters:** This method has no parameters.

        """
        trans = self.scene.getCameraTranslations()
        self.scene.setCameraTranslations(trans[0] + 0.05, trans[1])
        self.scene.redraw()

    def zoomIn(self):
        """
        This method zooms the camera by + 0.65 units along the z-axis. 
        The camera is in the +Z direction, so this moves the camera closer to
        the figure.
        
        **Parameters:** This method has no parameters.

        """
        self.scene.setCameraZoom(self.scene.getCameraZoom() + 0.65)
        self.scene.redraw()

    def zoomOut(self):
        """
        This method zooms the camera by - 0.65 units along the z-axis.
        The camera is in the +Z direction, so this moves the camera further 
        from the figure.
        
        **Parameters:** This method has no parameters.

        """
        self.scene.setCameraZoom(self.scene.getCameraZoom() - 0.65)
        self.scene.redraw()

    def topView(self):
        """
        This method sets the camera to a predefined position above the figure
        looking straight down on it.
        
        **Parameters:** This method has no parameters.

        """
        self.scene.setCameraRotations(90.0, 0.0)
        #self.updateTransformer()
        self.scene.redraw()

    def frontView(self):
        """
        This method sets the camera to a predefined position in front of the 
        figure looking straight back at it from along the +z-axis.
        
        **Parameters:** This method has no parameters.

        """
        self.scene.setCameraRotations(0.0, 0.0)
        #self.updateTransformer()
        self.scene.redraw()

    def sideView(self):
        """
        This method sets the camera to a predefined position out along the
        +x-axis looking straight back at the figure from the figures right 
        hand side.
        
        **Parameters:** This method has no parameters.

        """
        self.scene.setCameraRotations(0.0, 90.0)
        #self.updateTransformer()
        self.scene.redraw()

    def resetView(self):
        """
        This method resets the camera to its initial starting position.
        
        **Parameters:** This method has no parameters.

        """
        self.scene.setCameraTranslations(0.0, 0.0)
        self.scene.setCameraZoom(30.0)
        self.scene.redraw()

    def grabScreen(self):
        self.scene.grabScreen(180, 80, 440, 440, "grab.bmp")
