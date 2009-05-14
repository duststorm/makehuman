__docformat__ = 'restructuredtext'

import algos3d
import widgets3d, gui3d
import time
import subdivision
import files3d
import os

class Human(gui3d.Object):
    
    def __init__(self, globalScene, objFilePath):
        gui3d.Object.__init__(self, globalScene.application, objFilePath, position = [0, 0, 0], camera = 1, shadeless = 0, visible = True)
        self.meshData = self.mesh
        #self.meshData = files3d.loadMesh(globalScene, objFilePath, loadColors = None)
        self.scene = globalScene
        self.progressBar = widgets3d.ProgressBar(self.scene)
        self.progressBar.setVisibility(0)
        self.targetsDetailStack = {}#All details targets applied, with their values
        self.targetsEthnicStack = {"neutral":1.0}
        self.lastTargetApplied = None
        self.lastZoneModified = None
        self.grabMode = 0
        self.editMode = "macro"
        self.modellingType = "translation"        
        
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
        
        self.childVal = 0.0 #child
        self.oldVal = 0.0  #old
        self.youngVal = 1.0
        self.femaleVal = 0.5 #female
        self.maleVal = 0.5  #male
        self.flaccidVal = 0.5
        self.muscleVal = 0.5
        self.overweightVal = 0.5
        self.underweightVal = 0.5
        self.childValDetails = 0.0 #child
        self.oldValDetails = 0.0  #old
        self.flaccidValDetails = 0.0
        self.muscleValDetails = 0.0
        self.overweightValDetails = 0.0
        self.underweightValDetails = 0.0
        self.femaleValDetails = 0
        self.maleValDetails = 0        
        self.bodyZones =  ["eye","jaw","nose","mouth","head","neck","torso",\
                        "hip","pelvis","r-upperarm","l-upperarm","r-lowerarm",\
                        "l-lowerarm","l-hand", "r-hand", "r-upperleg","l-upperleg",\
                        "r-lowerleg","l-lowerleg","l-foot","r-foot","ear"]
                        
        #NOTE: the "universal" targets work as addition with all other targets,
        #while the ethnic targets are absolute.
        targetFolder = "data/targets/macrodetails"        

        self.targetFemaleFlaccidHeavyChild = "%s/universal-female-child-flaccid-heavy.target"%(targetFolder)
        self.targetFemaleFlaccidHeavyYoung = "%s/universal-female-young-flaccid-heavy.target"%(targetFolder)
        self.targetFemaleFlaccidHeavyOld = "%s/universal-female-old-flaccid-heavy.target"%(targetFolder)
        self.targetMaleFlaccidHeavyChild = "%s/universal-male-child-flaccid-heavy.target"%(targetFolder)
        self.targetMaleFlaccidHeavyYoung = "%s/universal-male-young-flaccid-heavy.target"%(targetFolder)
        self.targetMaleFlaccidHeavyOld = "%s/universal-male-old-flaccid-heavy.target"%(targetFolder)

        self.targetFemaleFlaccidLightChild = "%s/universal-female-child-flaccid-light.target"%(targetFolder)
        self.targetFemaleFlaccidLightYoung = "%s/universal-female-young-flaccid-light.target"%(targetFolder)
        self.targetFemaleFlaccidLightOld = "%s/universal-female-old-flaccid-light.target"%(targetFolder)
        self.targetMaleFlaccidLightChild = "%s/universal-male-child-flaccid-light.target"%(targetFolder)
        self.targetMaleFlaccidLightYoung = "%s/universal-male-young-flaccid-light.target"%(targetFolder)
        self.targetMaleFlaccidLightOld = "%s/universal-male-old-flaccid-light.target"%(targetFolder)

        self.targetFemaleMuscleHeavyChild = "%s/universal-female-child-muscle-heavy.target"%(targetFolder)
        self.targetFemaleMuscleHeavyYoung = "%s/universal-female-young-muscle-heavy.target"%(targetFolder)
        self.targetFemaleMuscleHeavyOld = "%s/universal-female-old-muscle-heavy.target"%(targetFolder)
        self.targetMaleMuscleHeavyChild = "%s/universal-male-child-muscle-heavy.target"%(targetFolder)
        self.targetMaleMuscleHeavyYoung = "%s/universal-male-young-muscle-heavy.target"%(targetFolder)
        self.targetMaleMuscleHeavyOld = "%s/universal-male-old-muscle-heavy.target"%(targetFolder)        
        
        self.targetFemaleMuscleLightChild = "%s/universal-female-child-muscle-light.target"%(targetFolder)
        self.targetFemaleMuscleLightYoung = "%s/universal-female-young-muscle-light.target"%(targetFolder)
        self.targetFemaleMuscleLightOld = "%s/universal-female-old-muscle-light.target"%(targetFolder)
        self.targetMaleMuscleLightChild = "%s/universal-male-child-muscle-light.target"%(targetFolder)
        self.targetMaleMuscleLightYoung = "%s/universal-male-young-muscle-light.target"%(targetFolder)
        self.targetMaleMuscleLightOld = "%s/universal-male-old-muscle-light.target"%(targetFolder)        
                        
                        
    def setTexture(self, texturePath):
        self.meshData.setTexture(texturePath)
        
    def setVisibility(self, flag):
        self.meshData.setVisibility(flag)
                        
    def subdivide(self):
        """
        This method toggles between displaying the standard mesh and a
        subdivided mesh. The subdivided mesh contains 4 times the number of
        faces as the standard mesh.

        **Parameters:** None.

        """

        if self.meshData.isSubdivided:
            self.meshData.isSubdivided = None
            sob = self.scene.getObject(self.meshData.name+".sub")
            sob.setVisibility(0)
            self.meshData.setVisibility(1)
        else:
            self.meshData.isSubdivided = 1
            subdivision.subdivide(self.meshData, self.scene)
            sob = self.scene.getObject(self.meshData.name+".sub")
            sob.setVisibility(1)
            self.meshData.setVisibility(0)
        self.scene.redraw()
        
        
    def setGenderVals(self,amount):
        """
        This method applies gender attributes to the human

        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """        
        
        if self.maleVal == amount:
            return 
        self.maleVal =  amount
        self.femaleVal = 1 - amount
    
    def setGender(self, gender):
        self.setGenderVals(gender)
    
    def getGender(self):
        return self.maleVal
        
    def setAgeVals(self,amount):
        """
        This method set age attributes to the human. 

        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """     
        if amount >= 0:
            if self.oldVal == amount and self.childVal == 0:
                return 
            self.oldVal = amount
            self.childVal = 0
        else:
            if self.childVal == -amount and self.oldVal == 0:
                return 
            self.childVal = -amount
            self.oldVal = 0 
        self.youngVal = 1-(self.oldVal + self.childVal)
    
    def setAge(self, age):
        self.setAgeVals(-1 + 2 * age)
        
    def getAge(self):
        if self.oldVal:
            return 0.5 + self.oldVal / 2.0
        elif self.childVal:
            return 0.5 - self.childVal / 2.0
        else:
            return 0.5

    def setWeight(self,weight):
        """
        This method set the values for the weight targets variables:
        self.overweightVal, self.underweightVal. Note that the slider return
        a value between -1 and 1, but both self.overweightVal, self.underweightVal
        have a value between 0 and 1.

        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """   
        if self.overweightVal == weight:
            return 
        self.overweightVal =  weight
        self.underweightVal = 1 - weight
        
    def getWeight(self):
        return self.overweightVal
         

    def setMuscle(self, muscle):
        """
        This method set the values for the tone targets variables:
        self.flaccidVal, self.muscleVal. 
        
        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """  
      
        if self.muscleVal == muscle:
            return 
        self.muscleVal =  muscle
        self.flaccidVal = 1 - muscle
    
    def getMuscle(self):        
        return self.muscleVal       
      
            
    def setEthnic(self, ethnic, value):
        modified = None
        ethnics = self.targetsEthnicStack
        
        # Remove the neutral ethnic, we recalculate it later
        if "neutral" in ethnics:
          del ethnics["neutral"]
        
        if value:
            # Set the ethnic to 0, so we can can calculate the max value possible
            ethnics[ethnic] = 0.0
            ethnics[ethnic] = max(0.0, min(1.0 - sum(ethnics.values()), value))
            # In the case that we couldn't set it, remove it from the dictionary
            if ethnics[ethnic] == 0.0:
                del ethnics[ethnic]
        elif ethnic in ethnics:
            # If we need to set it to 0, remove it from the dictionary
            del ethnics[ethnic]
        
        # Recalculate the neutral ethnic
        ethnics["neutral"] = 1.0 - sum(ethnics.values())
            
    def getEthnic(self, ethnic):
        if ethnic in self.targetsEthnicStack:
            return self.targetsEthnicStack[ethnic]
        else:
            return 0.0
            
    def setDetail(self, name, value):
        if value:
          self.targetsDetailStack[name] = value
        elif name in self.targetsDetailStack:
          del self.targetsDetailStack[name]
            
    def applyAllTargets(self):

        """
        This method applies all targets, in function of age and sex
        
        **Parameters:** None.

        """
        targetName = None
        self.progressBar.setVisibility(1)
        algos3d.resetObj(self.meshData)

        self.progressBar.setProgress(0.0)
        progressVal = 0.0
        progressIncr = 0.3/(len(self.targetsDetailStack)+1)
        
        #As first thing, we apply all micro details
        for t in self.targetsDetailStack.keys():
            algos3d.loadTranslationTarget(self.meshData, t, self.targetsDetailStack[t],None,0,0)
            progressVal += progressIncr
            self.progressBar.setProgress(progressVal)
        a = time.time()
        #+.01 below to prevent zerodivision error
        progressIncr = (0.6/(len(self.targetsEthnicStack.keys())+.01))/6
                                                            
        #Now we apply all macro targets        
        macroTargets = {}        

        macroTargets[self.targetFemaleFlaccidHeavyChild]= self.flaccidVal*self.overweightVal*self.childVal*self.femaleVal
        macroTargets[self.targetFemaleFlaccidHeavyYoung]= self.flaccidVal*self.overweightVal*self.youngVal*self.femaleVal
        macroTargets[self.targetFemaleFlaccidHeavyOld]= self.flaccidVal*self.overweightVal*self.oldVal*self.femaleVal
        macroTargets[self.targetMaleFlaccidHeavyChild]= self.flaccidVal*self.overweightVal*self.childVal*self.maleVal
        macroTargets[self.targetMaleFlaccidHeavyYoung]= self.flaccidVal*self.overweightVal*self.youngVal*self.maleVal
        macroTargets[self.targetMaleFlaccidHeavyOld]= self.flaccidVal*self.overweightVal*self.oldVal*self.maleVal

        macroTargets[self.targetFemaleFlaccidLightChild]= self.flaccidVal*self.underweightVal*self.childVal*self.femaleVal
        macroTargets[self.targetFemaleFlaccidLightYoung]= self.flaccidVal*self.underweightVal*self.youngVal*self.femaleVal
        macroTargets[self.targetFemaleFlaccidLightOld]= self.flaccidVal*self.underweightVal*self.oldVal*self.femaleVal
        macroTargets[self.targetMaleFlaccidLightChild]= self.flaccidVal*self.underweightVal*self.childVal*self.maleVal
        macroTargets[self.targetMaleFlaccidLightYoung]= self.flaccidVal*self.underweightVal*self.youngVal*self.maleVal
        macroTargets[self.targetMaleFlaccidLightOld]= self.flaccidVal*self.underweightVal*self.oldVal*self.maleVal

        macroTargets[self.targetFemaleMuscleHeavyChild]= self.muscleVal*self.overweightVal*self.childVal*self.femaleVal
        macroTargets[self.targetFemaleMuscleHeavyYoung]= self.muscleVal*self.overweightVal*self.youngVal*self.femaleVal
        macroTargets[self.targetFemaleMuscleHeavyOld]= self.muscleVal*self.overweightVal*self.oldVal*self.femaleVal
        macroTargets[self.targetMaleMuscleHeavyChild]= self.muscleVal*self.overweightVal*self.childVal*self.maleVal
        macroTargets[self.targetMaleMuscleHeavyYoung]= self.muscleVal*self.overweightVal*self.youngVal*self.maleVal
        macroTargets[self.targetMaleMuscleHeavyOld]= self.muscleVal*self.overweightVal*self.oldVal*self.maleVal

        macroTargets[self.targetFemaleMuscleLightChild]= self.muscleVal*self.underweightVal*self.childVal*self.femaleVal
        macroTargets[self.targetFemaleMuscleLightYoung]= self.muscleVal*self.underweightVal*self.youngVal*self.femaleVal
        macroTargets[self.targetFemaleMuscleLightOld]= self.muscleVal*self.underweightVal*self.oldVal*self.femaleVal
        macroTargets[self.targetMaleMuscleLightChild]= self.muscleVal*self.underweightVal*self.childVal*self.maleVal
        macroTargets[self.targetMaleMuscleLightYoung]= self.muscleVal*self.underweightVal*self.youngVal*self.maleVal
        macroTargets[self.targetMaleMuscleLightOld]= self.muscleVal*self.underweightVal*self.oldVal*self.maleVal
                 

        for k in macroTargets.keys():
            tVal = macroTargets[k]
            algos3d.loadTranslationTarget(self.meshData, k,tVal,None,0,0)

        for ethnicGroup in self.targetsEthnicStack.keys():
            
            ethnicVal = self.targetsEthnicStack[ethnicGroup]
            ethnicTargets = {}
            targetFemaleChild = "data/targets/macrodetails/%s-female-child.target"%(ethnicGroup)
            targetMaleChild = "data/targets/macrodetails/%s-male-child.target"%(ethnicGroup)
            targetFemaleOld = "data/targets/macrodetails/%s-female-old.target"%(ethnicGroup)
            targetMaleOld = "data/targets/macrodetails/%s-male-old.target"%(ethnicGroup)
            targetFemaleYoung = "data/targets/macrodetails/%s-female-young.target"%(ethnicGroup)
            targetMaleYoung = "data/targets/macrodetails/%s-male-young.target"%(ethnicGroup)

            ethnicTargets[targetFemaleChild] = self.femaleVal*self.childVal*ethnicVal
            ethnicTargets[targetMaleChild] = self.maleVal*self.childVal*ethnicVal
            ethnicTargets[targetFemaleOld] = self.femaleVal*self.oldVal*ethnicVal
            ethnicTargets[targetMaleOld]= self.maleVal*self.oldVal*ethnicVal
            ethnicTargets[targetFemaleYoung]= self.femaleVal*self.youngVal*ethnicVal
            ethnicTargets[targetMaleYoung]= self.maleVal*self.youngVal*ethnicVal

            for k in ethnicTargets.keys():
                
                tVal = ethnicTargets[k]                
                progressVal = progressVal + progressIncr
                self.progressBar.setProgress(progressVal)
                algos3d.loadTranslationTarget(self.meshData, k,tVal,None,0,0)

        #Update all verts
        facesToRecalculate = range(len(self.meshData.faces))
        indicesToUpdate = range(len(self.meshData.verts))
        self.meshData.calcNormals(indicesToUpdate,facesToRecalculate,1)
        self.meshData.update(indicesToUpdate)
        self.progressBar.setProgress(1.0)
        self.progressBar.setVisibility(0)
        
        
    def applyDetailsTargets(self,targetPath,incrVal,totVal):
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
        self.targetsDetailStack[targetPath] = totVal        
        algos3d.loadTranslationTarget(self.meshData, targetPath, incrVal,None, 1, 0)
        self.lastTargetApplied = targetPath
        return True
        
    def getPartNameForGroupName(self, groupName):
        for k in self.bodyZones:
          if k in groupName:                
            return k
        return None
        
    def setDetailsTarget(self):
        """
        This method .....

        """
        
        faceGroupName = self.scene.getSelectedFacesGroup().name
            
             
        print "GROUPS SELECTED: ",faceGroupName
        if  self.editMode == "macro":
            tFolder = "data/targets/macrodetails"
        if  self.editMode == "regular":
            tFolder = "data/targets/details/"
            partName = getPartNameForGroupName(faceGroupName)
        if  self.editMode == "micro":
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


        algos3d.colorizeVerts(self.meshData, [255,255,255,255])
        #With these 2 lines the first click select, the second grab
        if partName == self.lastZoneModified:
            #clicking on already selected part, move it             
            self.grabMode = 1 #Mouse motion move the verts
        else:
            #clicking on a not selected part, just select it
            self.lastZoneModified = partName
            self.grabMode = 2 #Mouse Motion do nothing (no scene rotation too because != none)
            algos3d.analyzeTarget(self.meshData, self.detailTargetY1a)
            
            
            
    def applySymmetryLeft(self):
        """
        This method applies right to left symmetry to the currently selected 
        body parts.
        
        **Parameters:** None.

        """
        self.symmetrize("l")


    def applySymmetryRight(self):
        """
        This method applies left to right symmetry to the currently selected 
        body parts.
        
        **Parameters:** None.

        """
        self.symmetrize("r")

    def symmetrize(self,direction="r"):
        """
        This method applies either left to right or right to left symmetry to 
        the currently selected body parts.
        
        
        Parameters
        ----------

        direction:
            *string*. A string indicating whether to apply left to right 
            symmetry ("r") or right to left symmetry ("l").

        """
        if direction == "l":
            prefix1 = "l-"
            prefix2 = "r-"
        else:
            prefix1 = "r-"
            prefix2 = "l-"

        for target in self.targetsDetailStack.keys():
            targetName = os.path.basename(target)
            #Reset previous targets on symm side
            if targetName[:2] == prefix2:
                algos3d.loadTranslationTarget(self.meshData, target, -self.targetsDetailStack[target],None,1,0)
                self.targetsDetailStack[target] = 0

        #Apply symm target. For horiz movement the value must ve inverted
        for target in self.targetsDetailStack.keys():
            targetName = os.path.basename(target)
            if targetName[:2] == prefix1:
                targetSym = os.path.join(os.path.dirname(target),prefix2+targetName[2:])
                targetSymVal = self.targetsDetailStack[target]
                if "trans-in" in targetSym or "trans-out" in targetName:
                    targetSymVal *= -1

                algos3d.loadTranslationTarget(self.meshData, targetSym, targetSymVal,None, 1, 1)
                self.targetsDetailStack[targetSym] = targetSymVal

        self.scene.redraw()
        
    def resetMeshValues(self):
        self.childVal = 0.0 
        self.youngVal = 1.0
        self.oldVal = 0.0
        self.femaleVal = 0.5
        self.maleVal = 0.5
        self.flaccidVal = 0.5
        self.muscleVal = 0.5
        self.overweightVal = 0.5
        self.underweightVal = 0.5 
        
        self.activeEthnicSets = {}
        self.targetsEthnicStack = {"neutral":1.0}  
        self.targetsDetailStack = {}    

        
        
