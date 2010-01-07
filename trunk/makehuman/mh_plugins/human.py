""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TO DO

"""

__docformat__ = 'restructuredtext'

import algos3d
import gui3d
import time
import subdivision
import files3d
import os
import mh
import humanmodifier
import math

class Human(gui3d.Object):
    
    def __init__(self, globalScene, objFilePath):
        gui3d.Object.__init__(self, globalScene.application, objFilePath, position = [0, 0, 0], camera = 0, shadeless = 0, visible = True)
        self.meshData = self.mesh
        # Uncomment the following 4 lines to use a shader
        #vertex_shader = mh.createVertexShader(open("data/shaders/glsl/skin_vertex_shader.txt").read())
        #fragment_shader = mh.createFragmentShader(open("data/shaders/glsl/skin_fragment_shader.txt").read())
        #self.mesh.setShader(mh.createShader(vertex_shader, fragment_shader))
        #self.mesh.setShaderParameter("gradientMap", mh.loadTexture("data/textures/color_temperature.png", 0))
        #self.mesh.setShaderParameter("ambientOcclusionMap", mh.loadTexture("data/textures/ambient_occlusion.png", 0))
        self.scene = globalScene
        self.targetsDetailStack = {}#All details targets applied, with their values
        self.targetsEthnicStack = {"neutral":1.0}
        self.lastTargetApplied = None
        self.lastZoneModified = None
        self.grabMode = 0
        self.editMode = "macro"
        self.modellingType = "translation" 
        self.symmetryModeEnabled = False    
        
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
        self.flaccidVal = 0.0
        self.muscleVal = 0.0
        self.overweightVal = 0.0
        self.underweightVal = 0.0
        self.genitals = 0.0
        self.breastCup = 4.5
        self.breastFirmness = 0.5
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


        self.targetFemaleFlaccidChild = "%s/universal-female-child-flaccid.target"%(targetFolder)
        self.targetFemaleFlaccidYoung = "%s/universal-female-young-flaccid.target"%(targetFolder)
        self.targetFemaleFlaccidOld = "%s/universal-female-old-flaccid.target"%(targetFolder)
        self.targetMaleFlaccidChild = "%s/universal-male-child-flaccid.target"%(targetFolder)
        self.targetMaleFlaccidYoung = "%s/universal-male-young-flaccid.target"%(targetFolder)
        self.targetMaleFlaccidOld = "%s/universal-male-old-flaccid.target"%(targetFolder)

        self.targetFemaleMuscleChild = "%s/universal-female-child-muscle.target"%(targetFolder)
        self.targetFemaleMuscleYoung = "%s/universal-female-young-muscle.target"%(targetFolder)
        self.targetFemaleMuscleOld = "%s/universal-female-old-muscle.target"%(targetFolder)
        self.targetMaleMuscleChild = "%s/universal-male-child-muscle.target"%(targetFolder)
        self.targetMaleMuscleYoung = "%s/universal-male-young-muscle.target"%(targetFolder)
        self.targetMaleMuscleOld = "%s/universal-male-old-muscle.target"%(targetFolder)       
        

        self.targetFemaleHeavyChild = "%s/universal-female-child-heavy.target"%(targetFolder)
        self.targetFemaleHeavyYoung = "%s/universal-female-young-heavy.target"%(targetFolder)
        self.targetFemaleHeavyOld = "%s/universal-female-old-heavy.target"%(targetFolder)
        self.targetMaleHeavyChild = "%s/universal-male-child-heavy.target"%(targetFolder)
        self.targetMaleHeavyYoung = "%s/universal-male-young-heavy.target"%(targetFolder)
        self.targetMaleHeavyOld = "%s/universal-male-old-heavy.target"%(targetFolder)        
        
        self.targetFemaleLightChild = "%s/universal-female-child-light.target"%(targetFolder)
        self.targetFemaleLightYoung = "%s/universal-female-young-light.target"%(targetFolder)
        self.targetFemaleLightOld = "%s/universal-female-old-light.target"%(targetFolder)
        self.targetMaleLightChild = "%s/universal-male-child-light.target"%(targetFolder)
        self.targetMaleLightYoung = "%s/universal-male-young-light.target"%(targetFolder)
        self.targetMaleLightOld = "%s/universal-male-old-light.target"%(targetFolder)
        
        targetFolder = "data/targets/details"  
        
        self.targetFemaleGenitalsChild = "%s/genitals_female_child.target"%(targetFolder)
        self.targetFemaleGenitalsYoung = "%s/genitals_female_young.target"%(targetFolder)
        self.targetFemaleGenitalsOld = "%s/genitals_female_old.target"%(targetFolder)
        self.targetMaleGenitalsChild = "%s/genitals_male_child.target"%(targetFolder)
        self.targetMaleGenitalsYoung = "%s/genitals_male_young.target"%(targetFolder)
        self.targetMaleGenitalsOld = "%s/genitals_male_old.target"%(targetFolder)

        self.hairFile = "data/hairs/default.hair"
        self.hairColor = [0.41, 0.23, 0.04]
                        
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
    
    def setGender(self, gender):
        """
        Sets the gender of the model. 0 is female, 1 is male.
        
        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """  
        self._setGenderVals(gender)
    
    def getGender(self):
        return self.maleVal 
        
    def _setGenderVals(self,amount):
        if self.maleVal == amount:
            return 
        self.maleVal =  amount
        self.femaleVal = 1 - amount       
        
    def setAge(self, age):
        """
        Sets the age of the model. 0 if 12 years old, 1 is 70. To set a particular age in years, use the
        formula age_value = (age_in_years - 12) / (70 - 12).
        
        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """  
        self._setAgeVals(-1 + 2 * age)
        
    def getAge(self):
        if self.oldVal:
            return 0.5 + self.oldVal / 2.0
        elif self.childVal:
            return 0.5 - self.childVal / 2.0
        else:
            return 0.5
        
    def _setAgeVals(self,amount):  
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
    
    def setWeight(self, weight):
        """
        Sets the amount of weight of the model. 0 for underweight, 1 for overweight.
        
        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """  
        self._setWeightVals(-1 + 2 * weight)
        
    def getWeight(self):
        if self.overweightVal:
            return 0.5 + self.overweightVal / 2.0
        elif self.underweightVal:
            return 0.5 - self.underweightVal / 2.0
        else:
            return 0.5

    def _setWeightVals(self,amount):
        if amount >= 0:
            if self.overweightVal == amount and self.underweightVal == 0:
                return 
            self.overweightVal = amount
            self.underweightVal = 0
        else:
            if self.underweightVal == -amount and self.overweightVal == 0:
                return 
            self.underweightVal = -amount
            self.overweightVal = 0        

     
    def setMuscle(self, muscle):
        """
        Sets the amount of muscle of the model. 0 for flacid, 1 for muscular.
        
        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """  
        self._setMuscleVals(-1 + 2 * muscle)
        
    def getMuscle(self):
        if self.muscleVal:
            return 0.5 + self.muscleVal / 2.0
        elif self.flaccidVal:
            return 0.5 - self.flaccidVal / 2.0
        else:
            return 0.5

    def _setMuscleVals(self, amount):
        if amount >= 0:
            if self.muscleVal == amount and self.flaccidVal == 0:
                return 
            self.muscleVal = amount
            self.flaccidVal = 0
        else:
            if self.flaccidVal == -amount and self.muscleVal == 0:
                return 
            self.flaccidVal = -amount
            self.muscleVal = 0      
      
    def setGenitals(self, value):
        """
        Sets the amount of genitals of the model. 0 for none, 1 for pronounced.
        
        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """  
        self.genitals = min(max(value, 0.0), 1.0)
        
    def getGenitals(self):
        return self.genitals
        
    def SetBreastCup(self, value):
        self.breastCup = min(8.0, max(1.0, value))
        
    def SetBreastFirmness(self, value):
        self.breastFirmness = min(1.0, max(0.0, value))
            
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
        return self.targetsEthnicStack.get(ethnic, 0.0)
            
    def setDetail(self, name, value):
        if value:
          self.targetsDetailStack[name] = value
        elif name in self.targetsDetailStack:
          del self.targetsDetailStack[name]
          
    def getDetail(self, name):
        return self.targetsDetailStack.get(name, 0.0)
          
    def setHairFile(self, filename):
        self.hairFile = filename
        
    def getSymmetryGroup(self, group):
        if group.name.find("l-", 0, 2) != -1:
          return self.mesh.getFaceGroup(group.name.replace("l-", "r-", 1))
        elif group.name.find("r-", 0, 2) != -1:
          return self.mesh.getFaceGroup(group.name.replace("r-", "l-", 1))
        else:
          return None
          
    def getSymmetryPart(self, name):
        if name.find("l-", 0, 2) != -1:
          return name.replace("l-", "r-", 1)
        elif name.find("r-", 0, 2) != -1:
          return name.replace("r-", "l-", 1)
        else:
          return None
            
    def applyAllTargets(self, progressCallback = None):

        """
        This method applies all targets, in function of age and sex
        
        **Parameters:** None.

        """
        targetName = None
        algos3d.resetObj(self.meshData)

        if progressCallback:
            progressCallback(0.0)
        progressVal = 0.0
        progressIncr = 0.3/(len(self.targetsDetailStack)+1)
        
        #As first thing, we apply all micro details
        for k, v in self.targetsDetailStack.iteritems():
            algos3d.loadTranslationTarget(self.meshData, k, v,None,0,0)
            progressVal += progressIncr
            if progressCallback:
                progressCallback(progressVal)
        a = time.time()
        #+.01 below to prevent zerodivision error
        progressIncr = (0.6/(len(self.targetsEthnicStack.keys())+.01))/6
                                                            
        #Now we apply all macro targets        
        macroTargets = {}
        
        averageWeightVal = 1-(self.underweightVal+self.overweightVal)        
        averageToneVal = 1-(self.muscleVal + self.flaccidVal)

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

        macroTargets[self.targetFemaleFlaccidChild]= self.flaccidVal*averageWeightVal*self.childVal*self.femaleVal
        macroTargets[self.targetFemaleFlaccidYoung]= self.flaccidVal*averageWeightVal*self.youngVal*self.femaleVal
        macroTargets[self.targetFemaleFlaccidOld]= self.flaccidVal*averageWeightVal*self.oldVal*self.femaleVal
        macroTargets[self.targetMaleFlaccidChild]= self.flaccidVal*averageWeightVal*self.childVal*self.maleVal
        macroTargets[self.targetMaleFlaccidYoung]= self.flaccidVal*averageWeightVal*self.youngVal*self.maleVal
        macroTargets[self.targetMaleFlaccidOld]= self.flaccidVal*averageWeightVal*self.oldVal*self.maleVal        

        macroTargets[self.targetFemaleMuscleChild]= self.muscleVal*averageWeightVal*self.childVal*self.femaleVal
        macroTargets[self.targetFemaleMuscleYoung]= self.muscleVal*averageWeightVal*self.youngVal*self.femaleVal
        macroTargets[self.targetFemaleMuscleOld]= self.muscleVal*averageWeightVal*self.oldVal*self.femaleVal
        macroTargets[self.targetMaleMuscleChild]= self.muscleVal*averageWeightVal*self.childVal*self.maleVal
        macroTargets[self.targetMaleMuscleYoung]= self.muscleVal*averageWeightVal*self.youngVal*self.maleVal
        macroTargets[self.targetMaleMuscleOld]= self.muscleVal*averageWeightVal*self.oldVal*self.maleVal

        macroTargets[self.targetFemaleHeavyChild]= averageToneVal*self.overweightVal*self.childVal*self.femaleVal
        macroTargets[self.targetFemaleHeavyYoung]= averageToneVal*self.overweightVal*self.youngVal*self.femaleVal
        macroTargets[self.targetFemaleHeavyOld]= averageToneVal*self.overweightVal*self.oldVal*self.femaleVal
        macroTargets[self.targetMaleHeavyChild]= averageToneVal*self.overweightVal*self.childVal*self.maleVal
        macroTargets[self.targetMaleHeavyYoung]= averageToneVal*self.overweightVal*self.youngVal*self.maleVal
        macroTargets[self.targetMaleHeavyOld]= averageToneVal*self.overweightVal*self.oldVal*self.maleVal

        macroTargets[self.targetFemaleLightChild]= averageToneVal*self.underweightVal*self.childVal*self.femaleVal
        macroTargets[self.targetFemaleLightYoung]= averageToneVal*self.underweightVal*self.youngVal*self.femaleVal
        macroTargets[self.targetFemaleLightOld]= averageToneVal*self.underweightVal*self.oldVal*self.femaleVal
        macroTargets[self.targetMaleLightChild]= averageToneVal*self.underweightVal*self.childVal*self.maleVal
        macroTargets[self.targetMaleLightYoung]= averageToneVal*self.underweightVal*self.youngVal*self.maleVal
        macroTargets[self.targetMaleLightOld]= averageToneVal*self.underweightVal*self.oldVal*self.maleVal

        for k, v in macroTargets.iteritems():
            if v != 0.0:         
                print "APP: %s, VAL: %f"%(k, v)
            algos3d.loadTranslationTarget(self.meshData, k, v, None, 0, 0)
            
        detailTargets = {}
        
        detailTargets[self.targetFemaleGenitalsChild]= self.genitals*self.childVal*self.femaleVal
        detailTargets[self.targetFemaleGenitalsYoung]= self.genitals*self.youngVal*self.femaleVal
        detailTargets[self.targetFemaleGenitalsOld]= self.genitals*self.oldVal*self.femaleVal
        detailTargets[self.targetMaleGenitalsChild]= self.genitals*self.childVal*self.maleVal
        detailTargets[self.targetMaleGenitalsYoung]= self.genitals*self.youngVal*self.maleVal
        detailTargets[self.targetMaleGenitalsOld]= self.genitals*self.oldVal*self.maleVal
        
        breastCup = [0 for i in xrange(0, 9)]
        i = int(math.floor(self.breastCup))
        value = self.breastCup - i
        breastCup[i] = 1 - value;
        if i < 8:
          breastCup[i+1] = value;
        
        for i in xrange(1, 9):
          detailTargets["data/targets/details/neutral_female-young-cup%i-firmness0.target"%(i)] = self.youngVal*self.femaleVal*(1.0-self.breastFirmness)*breastCup[i]
          detailTargets["data/targets/details/neutral_female-young-cup%i-firmness1.target"%(i)] = self.youngVal*self.femaleVal*self.breastFirmness*breastCup[i]
        
        for k, v in detailTargets.iteritems():
            if v != 0.0:         
                print "APP: %s, VAL: %f"%(k, v)
            algos3d.loadTranslationTarget(self.meshData, k, v, None, 0, 0)

        for ethnicGroup, ethnicVal in self.targetsEthnicStack.iteritems():
            
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

            for k, v in ethnicTargets.iteritems():              
                progressVal = progressVal + progressIncr
                if progressCallback:
                    progressCallback(progressVal)
                algos3d.loadTranslationTarget(self.meshData, k, v, None, 0, 0)

        #Update all verts
        self.meshData.calcNormals(1, 1)
        self.meshData.update()
        if progressCallback:
            progressCallback(1.0)
        
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

        for k, v in self.targetsDetailStack.iteritems():
            targetName = os.path.basename(target)
            #Reset previous targets on symm side
            if targetName[:2] == prefix2:
                algos3d.loadTranslationTarget(self.meshData, target, -v,None,1,0)
                self.targetsDetailStack[k] = 0

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
        self.flaccidVal = 0.0
        self.muscleVal = 0.0
        self.overweightVal = 0.0
        self.underweightVal = 0.0
        self.genitals = 0.0 
        
        self.activeEthnicSets = {}
        self.targetsEthnicStack = {"neutral":1.0}  
        self.targetsDetailStack = {}    

    def load(self, filename, progressCallback = None):
        self.resetMeshValues()
        
        f = open(filename, 'r')
        
        for data in f.readlines():
            lineData = data.split()
            
            if len(lineData) > 0:
                if lineData[0] == "version":
                    print("Version " + lineData[1])
                elif lineData[0] == "tags":
                    for tag in lineData:
                      print("Tag " + tag)
                elif lineData[0] == "gender":
                    self.setGender(float(lineData[1]))
                elif lineData[0] == "age":
                    self.setAge(float(lineData[1]))
                elif lineData[0] == "muscle":
                    self.setMuscle(float(lineData[1]))
                elif lineData[0] == "weight":
                    self.setWeight(float(lineData[1]))
                elif lineData[0] == "height":
                    modifier = humanmodifier.Modifier(self, "data/targets/macrodetails/universal-stature-dwarf.target",
                      "data/targets/macrodetails/universal-stature-giant.target")
                    modifier.setValue(float(lineData[1]))
                elif lineData[0] == "genitals":
                    self.setGenitals(float(lineData[1]))
                elif lineData[0] == "ethnic":
                    self.targetsEthnicStack[lineData[1]] = float(lineData[2])
                elif lineData[0] == "detail":
                    self.targetsDetailStack["data/targets/details/" + lineData[1] + ".target"] = float(lineData[2])
                elif lineData[0] == "microdetail":
                    self.targetsDetailStack["data/targets/microdetails/" + lineData[1] + ".target"] = float(lineData[2])
                
        f.close()
        
        del self.targetsEthnicStack["neutral"]
        self.targetsEthnicStack["neutral"] = 1.0 - sum(self.targetsEthnicStack.values())
                
        self.applyAllTargets(progressCallback)

    def save(self, filename, tags):
        f = open(filename, 'w')
        f.write("# Written by makehuman 1.0.0 alpha 4\n")
        f.write("version 1.0.0\n")
        f.write("tags %s\n" %(tags))
        f.write("gender %f\n" %(self.getGender()))
        f.write("age %f\n" %(self.getAge()))
        f.write("muscle %f\n" %(self.getMuscle()))
        f.write("weight %f\n" %(self.getWeight()))
        f.write("genitals %f\n" %(self.getGenitals()))
        
        modifier = humanmodifier.Modifier(self, "data/targets/macrodetails/universal-stature-dwarf.target",
          "data/targets/macrodetails/universal-stature-giant.target")
        f.write("height %f\n" %(modifier.getValue()))
        
        for (target, value) in self.targetsEthnicStack.iteritems():
            f.write("ethnic %s %f\n" %(target, value))
                
        for t in self.targetsDetailStack.keys():
            if "/details/" in t:
                f.write("detail %s %f\n" %(os.path.basename(t).replace('.target', ''), self.targetsDetailStack[t]))
            elif  "/microdetails/" in t:
                f.write("microdetail %s %f\n" %(os.path.basename(t).replace('.target', ''), self.targetsDetailStack[t]))
        f.close()