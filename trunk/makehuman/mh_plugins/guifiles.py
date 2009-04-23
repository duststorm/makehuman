# You may use, modify and redistribute this module under the terms of the GNU GPL.
""" 
Class for handling File mode in the GUI.

===========================  ===============================================================  
Project Name:                **MakeHuman**                                                  
Module File Location:        mh_plugins/guifiles.py                                          
Product Home Page:           http://www.makehuman.org/                                      
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/                     
Authors:                     Manuel Bastioni                                            
Copyright(c):                MakeHuman Team 2001-2008                                       
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards  
===========================  ===============================================================  

This module implements the 'guifiles' class structures and methods to support GUI 
File mode operations.
File mode is invoked by selecting the File mode icon from the main GUI control bar at the top of
the screen. While in this mode, user actions (keyboard and mouse events) are passed into 
this class for processing. Having processed an event this class returns control to the 
main OpenGL/SDL/Application event handling loop.  

"""

__docformat__ = 'restructuredtext'

import files3d, animation3d
import guifileselector, datetime, os

class Guifiles:
    """
    The data structures and methods to support the File mode GUI. 
    One instance of this class (named gFile) is instantiated by main.py at 
    application startup to handle user interaction with the MakeHuman GUI 
    when in File mode.
    """

    def __init__(self, globalScene, modelling, commonGUI = None):
        """
        This is the constructor method for the guifiles class. It initializes the
        following attributes:

        - **self.guiFilesObjs**: *object list*. A list of GUI objects.
          Initialised to an empty list then populated by calls to the 
          *files3d.loadMesh* method.
        - **self.gFileSelector**: *class reference*. A reference to the 
          class used to select files. This reference is created by calling the 
          constructor method on the *guifileselector* class.
        - **self.modifiedGUIObjs**: *object list*. A list of modified GUI 
          objects.
          Default: Empty list.
        - **self.scene**: *Scene3D*. A reference to the global scene object 
          passed in as a parameter to this constructor method.
        - **self.bLoadFile**: *object reference*. A reference to the 
          'load file' GUI control object (button).
        - **self.bSaveFile**: *object reference*. A reference to the 
          'save file' GUI control object (button).
        - **self.bExportFile**: *object reference*. A reference to the 
          'export file' GUI control object (button).

        Parameters
        ----------

        globalScene:
            *Scene3D*. A reference to the global scene object.
        """

        print "GUI files initialized"
        self.guiFilesObjs = []
        self.gFileSelector = guifileselector.Guifileselector(globalScene)
        
        self.modifiedGUIObjs = set()            
        self.scene = globalScene        
        self.bLoadFile = files3d.loadMesh(self.scene, "data/3dobjs/button_load_file.obj",\
                        self.guiFilesObjs,-0.5,-0.38,9)
        self.bSaveFile = files3d.loadMesh(self.scene, "data/3dobjs/button_save_file.obj",\
                        self.guiFilesObjs,-0.358,-0.38,9)
        self.bExportFile = files3d.loadMesh(self.scene, "data/3dobjs/button_export_file.obj",\
                        self.guiFilesObjs,-0.216,-0.38,9)
        self.bFile = files3d.loadMesh(self.scene, "data/3dobjs/file.obj", self.guiFilesObjs, 0, 0, 0)
        self.bNextFile = files3d.loadMesh(self.scene, "data/3dobjs/nextfile.obj", self.guiFilesObjs, 3.0, 0.5, 0)
        self.bPreviousFile = files3d.loadMesh(self.scene, "data/3dobjs/previousfile.obj", self.guiFilesObjs, -3.0, 0.5, 0)
        self.bFileName = files3d.loadMesh(self.scene, "data/3dobjs/empty.obj", self.guiFilesObjs, -0.5, -0.7, 0)

        self.bLoadFile.setTexture("data/images/button_load_file.png")
        self.bSaveFile.setTexture("data/images/button_save_file.png")
        self.bExportFile.setTexture("data/images/button_export_file.png")
        
        self.scene.connect("LMOUSEP",self.fileLoad,self.bFile)
        self.scene.connect("LMOUSEP",self.fileLoadNext,self.bNextFile)
        self.scene.connect("LMOUSEP",self.fileLoadPrevious,self.bPreviousFile)
        
        self.pan = self.scene.getCameraTranslations()
        self.zoom = self.scene.getCameraZoom()
        self.rotation = self.scene.getCameraRotations()
        self.models = None
        self.selectedModel = 0
        
        self.modelling = modelling
        
        self.nextFileAnimation = animation3d.Timeline(0.25)
        self.nextFileAnimation.append(animation3d.PathAction(self.bFile, [[0, 0, 0], [-3.0, 0.5, 0]]))
        self.nextFileAnimation.append(animation3d.ScaleAction(self.bFile, [1.5, 1.5, 1.5], [1.0, 1.0, 1.0]))
        self.nextFileAnimation.append(animation3d.PathAction(self.bNextFile, [[3.0, 0.5, 0], [0, 0, 0]]))
        self.nextFileAnimation.append(animation3d.ScaleAction(self.bNextFile, [1.0, 1.0, 1.0], [1.5, 1.5, 1.5]))
        self.nextFileAnimation.append(animation3d.UpdateAction(self.scene))
        
        self.previousFileAnimation = animation3d.Timeline(0.25)
        self.previousFileAnimation.append(animation3d.PathAction(self.bPreviousFile, [[-3.0, 0.5, 0], [0, 0, 0]]))
        self.previousFileAnimation.append(animation3d.ScaleAction(self.bPreviousFile, [1.0, 1.0, 1.0], [1.5, 1.5, 1.5]))
        self.previousFileAnimation.append(animation3d.PathAction(self.bFile, [[0, 0, 0], [3.0, 0.5, 0],]))
        self.previousFileAnimation.append(animation3d.ScaleAction(self.bFile, [1.5, 1.5, 1.5], [1.0, 1.0, 1.0]))
        self.previousFileAnimation.append(animation3d.UpdateAction(self.scene))
   
    def fileLoadMode(self): 
    	"""
        This method invokes the *isActive* method on the *guifileselector* class.

        **Parameters:** This method has no parameters.

        """
        
        self.scene.connect("LEFT_ARROW", self.fileLoadPrevious)
        self.scene.connect("RIGHT_ARROW", self.fileLoadNext)
        self.scene.connect(self.scene.KP_RETURN, self.fileLoad)
       
        self.gFileSelector.isNotActive()
        self.scene.getObject("base.obj").setVisibility(0)
        self.models = []
        for f in os.listdir("models"):
            if os.path.splitext(f)[-1] == ".mhm":
                self.models.append(f)
        self.selectedModel = 0
        
        self.bFile.setScale(1.5, 1.5, 1.5);
        
        self.bPreviousFile.clearTexture()
        self.bPreviousFile.setVisibility(0)
        
        if self.selectedModel < len(self.models):
            self.bFile.setTexture("models/" + self.models[self.selectedModel].replace('mhm', 'bmp'))
            self.bFileName.setText(self.models[self.selectedModel].replace('.mhm', ''))
            self.bFile.setVisibility(1)
            self.bFileName.setVisibility(1)
        else:
            self.bFile.clearTexture()
            self.bFile.setVisibility(0)
            self.bFileName.setVisibility(0)
        
        if self.selectedModel + 1 < len(self.models):
            self.bNextFile.setTexture("models/" + self.models[self.selectedModel + 1].replace('mhm', 'bmp'))
            self.bNextFile.setVisibility(1)
        else:
            self.bNextFile.clearTexture()
            self.bNextFile.setVisibility(0)
            
        self.scene.redraw()
        
    def fileLoadNext(self):
    	"""
        This method displays the next file in the file 'Load' screen. It moves 
        the file displayed in the centre across to the pile on the left and 
        peels the next file off the stack on the right. 

        **Parameters:** This method has no parameters.

        """
        if self.selectedModel + 1 == len(self.models):
            return
            
        # Start animation by hiding the previous file
        self.bPreviousFile.setVisibility(0)
        
        # Animate by moving current and next file to previous and current locations
        self.nextFileAnimation.start()
        
        # End animation by resetting positions and showing new configuration
        self.bFile.setLoc(0, 0, 0)
        self.bFile.setScale(1.5, 1.5, 1.5)
        self.bNextFile.setLoc(3.0, 0.5, 0)
        self.bNextFile.setScale(1.0, 1.0, 1.0)
        
        self.selectedModel += 1
        
        self.bPreviousFile.setTexture("models/" + self.models[self.selectedModel - 1].replace('mhm', 'bmp'))
        self.bPreviousFile.setVisibility(1)
        self.bFile.setTexture("models/" + self.models[self.selectedModel].replace('mhm', 'bmp'))
        self.bFileName.setText(self.models[self.selectedModel].replace('.mhm', ''))
        self.bFile.setVisibility(1)
        
        if self.selectedModel + 1 < len(self.models):
            self.bNextFile.setTexture("models/" + self.models[self.selectedModel + 1].replace('mhm', 'bmp'))
            self.bNextFile.setVisibility(1)
        else:
            self.bNextFile.clearTexture()
            self.bNextFile.setVisibility(0)
            
        self.scene.redraw()
            
    def fileLoadPrevious(self):
    	"""
        This method displays the previous file on the file 'Load' screen. 
        It moves the file displayed in the centre back onto the pile on the 
        right and peels the previous file off the stack on the left. 

        **Parameters:** This method has no parameters.

        """
        if self.selectedModel == 0:
            return
            
        # Start animation by hiding the next file
        self.bNextFile.setVisibility(0)
        
        # Animate by moving previous and current file to current and next locations
        self.previousFileAnimation.start()
        
        # End animation by resetting positions and showing new configuration
        self.bPreviousFile.setLoc(-3.0, 0.5, 0)
        self.bPreviousFile.setScale(1.0, 1.0, 1.0)
        self.bFile.setLoc(0, 0, 0)
        self.bFile.setScale(1.5, 1.5, 1.5)
            
        self.selectedModel -= 1
        
        if self.selectedModel - 1 >= 0:
            self.bPreviousFile.setTexture("models/" + self.models[self.selectedModel - 1].replace('mhm', 'bmp'))
            self.bPreviousFile.setVisibility(1)
        else:
            self.bPreviousFile.clearTexture()
            self.bPreviousFile.setVisibility(0)
        
        self.bFile.setTexture("models/" + self.models[self.selectedModel].replace('mhm', 'bmp'))
        self.bFileName.setText(self.models[self.selectedModel].replace('.mhm', ''))
        self.bFile.setVisibility(1)
        self.bNextFile.setTexture("models/" + self.models[self.selectedModel + 1].replace('mhm', 'bmp'))
        self.bNextFile.setVisibility(1)
        
        self.scene.redraw()
        
    def fileLoad(self):
    	"""
        This method is called when the user clicks the central image on the 
        file 'Load' screen to load that model into MakeHuman.

        **Parameters:** This method has no parameters.

        """
        print("Loading " + self.models[self.selectedModel])
        
        # Load the model
        f = open("models/" + self.models[self.selectedModel], 'r')
        
        for data in f.readlines():
            lineData = data.split()
            
            if len(lineData) > 0:
                if lineData[0] == "version":
                    print("Version " + lineData[1])
                elif lineData[0] == "tags":
                    for tag in lineData:
                      print("Tag " + tag)
                elif lineData[0] == "female":
                    self.modelling.femaleVal = float(lineData[1])
                elif lineData[0] == "male":
                    self.modelling.maleVal = float(lineData[1])  
                elif lineData[0] == "child":
                    self.modelling.childVal = float(lineData[1])
                elif lineData[0] == "old":
                    self.modelling.oldVal = float(lineData[1])      
                elif lineData[0] == "flaccid":
                    self.modelling.flaccidVal = float(lineData[1])
                elif lineData[0] == "muscle":
                    self.modelling.muscleVal = float(lineData[1])
                elif lineData[0] == "overweight":
                    self.modelling.overweightVal = float(lineData[1])
                elif lineData[0] == "underweight":
                    self.modelling.underweightVal = float(lineData[1])
                elif lineData[0] == "ethnic":
                    self.modelling.ethnicTargetsValues[lineData[1]] = float(lineData[2])
                elif lineData[0] == "detail":
                    self.modelling.targetsDetailStack["data/targets/details/" + lineData[1] + ".target"] = float(lineData[2])
                elif lineData[0] == "microdetail":
                    self.modelling.targetsDetailStack["data/targets/microdetail/" + lineData[1] + ".target"] = float(lineData[2])
                
        f.close()
        
        # Sync macro interface
        self.modelling.colorFaceGroup(self.modelling.bGender, str(self.modelling.maleVal))
        self.modelling.colorFaceGroup(self.modelling.bAge, str(self.modelling.oldVal))
        self.modelling.colorFaceGroup(self.modelling.bWeight, str(self.modelling.overweightVal))
        self.modelling.colorFaceGroup(self.modelling.bMuscle, str(self.modelling.muscleVal))
        
        # Sync ethnic interface
        africa = None
        # Set all to white
        for t in self.modelling.ethnicTargetsColors.keys():
            self.modelling.ethnicTargetsColors[t] = [255, 255, 255, 255]
        # Calculate the ethnic target value, and store it in dictionary
        self.modelling.ethnicTargetsToApply = {}
        for t in self.modelling.ethnicTargetsValues.keys():
            self.modelling.ethnicTargetsToApply[t] = self.modelling.ethnicTargetsValues[t]
            #for each facegroup recalculate the color
            self.modelling.ethnicTargetsColors[t] = [int(255*self.modelling.ethnicTargetsToApply[t]),\
                                            1-int(255*self.modelling.ethnicTargetsToApply[t]),\
                                            255,255]
            if "africa" in t:
                africa = True
        self.modelling.ethnicTargetsToApply["neutral"] = 1.0 - sum(self.modelling.ethnicTargetsValues.values())

        if africa:
            self.modelling.colorEthnicGroup(self.modelling.bAfrica)
                
        self.modelling.applyCharacterTargets()
        self.bPreviousFile.setVisibility(0)
        self.bNextFile.setVisibility(0)
        self.bFile.setVisibility(0)
        self.scene.getObject("base.obj").setVisibility(0)
        self.scene.disconnect("LEFT_ARROW")
        self.scene.disconnect("RIGHT_ARROW")
        self.scene.disconnect(self.scene.KP_RETURN)
        
    def fileSaveMode(self):
    	"""
        This method invokes the *isActive* method on the *guifileselector* 
        class to display the fields the user needs to be able to save the 
        current model to the file system.

        **Parameters:** This method has no parameters.

        """
       
        self.scene.connect("LMOUSEP", self.fileSave, self.gFileSelector.bConfirm)
        self.scene.connect(self.scene.KP_RETURN, self.fileSave)
        self.gFileSelector.isActive()
        self.scene.getObject("base.obj").setVisibility(1)
        self.bPreviousFile.setVisibility(0)
        self.bNextFile.setVisibility(0)
        self.bFile.setVisibility(0)
        self.bFileName.setVisibility(0)
        
    def fileSave(self): 
    	"""
        This method is called when the user presses the confirmation button on
        the file, save screen to save the current MakeHuman model to the users
        file system.

        **Parameters:** This method has no parameters.

        """
       
        if not os.path.exists("models"):
            os.mkdir("models")

        filename = self.gFileSelector.textString.split()[0]
        
        # Save the thumbnail
        leftTop = self.scene.convertToScreen(-10, 10, 0, 1)
        rightBottom = self.scene.convertToScreen(10, -9, 0, 1)
        self.scene.grabScreen(int(leftTop[0]), int(leftTop[1]), int(rightBottom[0] - leftTop[0]), int(rightBottom[1] - leftTop[1]), "models/" + filename + ".bmp")
        
        # Save the model
        f = open("models/" + filename + ".mhm", 'w')
        f.write("# Written by makehuman 1.0.0 alpha 2\n")
        f.write("version 1.0.0\n")
        f.write("tags %s\n" %(self.gFileSelector.textString))
        f.write("female %f\n" %(self.modelling.femaleVal))
        f.write("male %f\n" %(self.modelling.maleVal))
        f.write("child %f\n" %(self.modelling.childVal))
        f.write("old %f\n" %(self.modelling.oldVal))
        f.write("flaccid %f\n" %(self.modelling.flaccidVal))
        f.write("muscle %f\n" %(self.modelling.muscleVal))
        f.write("overweight %f\n" %(self.modelling.overweightVal))
        f.write("underweight %f\n" %(self.modelling.underweightVal))
        for (target, value) in self.modelling.activeEthnicSets.iteritems():
            f.write("ethnic %s %f\n" %(target, value))
                
        for t in self.modelling.targetsDetailStack.keys():
            if "/details/" in t:
                f.write("detail %s %f\n" %(os.path.basename(t).replace('.target', ''), self.modelling.targetsDetailStack[t]))
            elif  "/microdetails/" in t:
                f.write("microdetail %s %f\n" %(os.path.basename(t).replace('.target', ''), self.modelling.targetsDetailStack[t]))
        f.close()
        
        self.gFileSelector.isNotActive()
        self.scene.getObject("base.obj").setVisibility(0)
        self.scene.disconnect(self.scene.KP_RETURN)

    def isActive(self):
    	"""
        This method activates the 'file selector' GUI control object and 
        connects it to the left mouse button. It displays the GUI controls
        appropriate to the GUI 'file mode' operations. 

        **Parameters:** This method has no parameters.

        """
        
        #connect buttons to  function
        self.scene.connect("LMOUSEP",self.fileLoadMode,self.bLoadFile)
        self.scene.connect("LMOUSEP",self.fileSaveMode,self.bSaveFile)  
        for ob in self.guiFilesObjs:                   
            ob.setCameraProjection(0)
            ob.setVisibility(1)
            ob.setShadeless(1)
        self.bFileName.setVisibility(0)
        self.bFile.setVisibility(0)
        self.bNextFile.setVisibility(0)
        self.bPreviousFile.setVisibility(0)
        self.pan = self.scene.getCameraTranslations()
        self.zoom = self.scene.getCameraZoom()
        self.rotation = self.scene.getCameraRotations()
        self.scene.setCameraTranslations(0, -1)
        self.scene.setCameraZoom(70.0)
        self.scene.setCameraRotations(0.0, 0.0)

    def isNotActive(self):        
    	"""
        This method disactivates the 'file selector' GUI control object and 
        hides the GUI controls associated with GUI 'file mode' operations. 

        **Parameters:** This method has no parameters.

        """
        self.gFileSelector.isNotActive()
        self.scene.disconnect("LMOUSEP",self.gFileSelector.bConfirm)
        self.scene.disconnect("LMOUSEP",self.bLoadFile) 
        self.scene.disconnect("LMOUSEP",self.bSaveFile) 
        self.scene.disconnect("LEFT_ARROW")
        self.scene.disconnect("RIGHT_ARROW")
        self.scene.disconnect(self.scene.KP_RETURN)
        for ob in self.guiFilesObjs:
            ob.setVisibility(0)
        self.scene.getObject("base.obj").setVisibility(0)
        if self.pan:
          self.scene.setCameraTranslations(self.pan[0], self.pan[1])
        if self.zoom:
          self.scene.setCameraZoom(self.zoom)
        if self.rotation:
          self.scene.setCameraRotations(self.rotation[0], self.rotation[1])

        

            


