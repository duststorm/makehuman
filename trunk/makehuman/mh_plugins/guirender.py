""" 
Class for handling Render mode in the GUI.

===========================  ===============================================================  
Project Name:                **MakeHuman**                                                  
Module File Location:        mh_plugins/guirender.py                                          
Product Home Page:           http://www.makehuman.org/                                      
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/                     
Authors:                     Manuel Bastioni                                            
Copyright(c):                MakeHuman Team 2001-2008                                       
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards  
===========================  ===============================================================  

This module implements the 'guirender' class structures and methods to support GUI 
Render mode operations.
Render mode is invoked by selecting the Render mode icon from the main GUI control 
bar at the top of the screen. 
While in this mode, user actions (keyboard and mouse events) are passed into 
this class for processing. Having processed an event this class returns control to the 
main OpenGL/SDL/Application event handling loop.  

"""

__docformat__ = 'restructuredtext'


import files3d
import mh2povray
import mh2renderman



class Guirender:
    """
    The data structures and methods to support the Render mode GUI. 
    One instance of this class (named gRender) is instantiated by main.py 
    at application startup to handle user interaction with the MakeHuman GUI 
    when in Render mode.
    """

    def __init__(self, globalScene, commonGUI = None):
        """
        This is the constructor method for the guirender class. 
        It initializes the following attributes:

        - **self.renderGuiObjs**: *object list*. A list of GUI objects.
          Initialised to an empty list then populated by calls to the 
          *files3d.loadMesh* method.
        - **self.modifiedGUIObjs**: *object list*. A list of modified GUI 
          objects.
          Default: Empty list.
        - **self.scene**: *Scene3D*. A reference to the global scene object 
          passed in as a parameter to this constructor method.
        - **self.bAqsis**: *object reference*. A reference to the 
          'Render using Aqsis' GUI control object (button).
        - **self.bPixie**: *object reference*. A reference to the 
          'Render using Pixie' GUI control object (button).
        - **self.bPovray**: *object reference*. A reference to the 
          'Render using POV-Ray' GUI control object (button).

        Parameters
        ----------

        globalScene:
            *Scene3D*. A reference to the global scene object.
        """
        print "GUI render initialized"
        self.renderGuiObjs = []
        self.modifiedGUIObjs = set()        
        self.scene = globalScene 
        self.bAqsis = files3d.loadMesh(self.scene,"data/3dobjs/button_aqsis.obj",\
                    self.renderGuiObjs,-0.5,-0.37,9)
        self.bPixie = files3d.loadMesh(self.scene,"data/3dobjs/button_pixie.obj",\
                    self.renderGuiObjs,-0.358,-0.37,9)
        self.bPovray = files3d.loadMesh(self.scene,"data/3dobjs/button_povray.obj",\
                    self.renderGuiObjs,-0.216,-0.37,9)

        self.bAqsis.setTexture("data/images/button_aqsis.png")
        self.bPixie.setTexture("data/images/button_pixie.png")
        self.bPovray.setTexture("data/images/button_povray.png")

    def povExport(self):        
    	"""
        This method calls the POV-Ray export plugin by invoking the 
        povrayExport function from the mh2povray module.

        **Parameters:** This method has no parameters.

        """
        reload(mh2povray)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
        for obj in self.scene.objects:
            # print "POV-Ray Export test: ", obj.name
            # Only process the humanoid figure
            if obj.name == "base.obj":
                cameraData = self.scene.getCameraSettings()
                mh2povray.povrayExport(obj,cameraData)

    def rendermanExportA(self):        
    	"""
        This method calls the Renderman export plugin with the Aqsis option
        by invoking the saveScene function from the mh2renderman module.

        **Parameters:** This method has no parameters.

        """
        mh2renderman.saveScene(self.scene, "scena.rib", "renderman_output", "aqsis")

    def rendermanExportP(self):        
    	"""
        This method calls the Renderman export plugin with the Pixie option
        by invoking the saveScene function from the mh2renderman module.

        **Parameters:** This method has no parameters.

        """
        mh2renderman.saveScene(self.scene, "scena.rib", "renderman_output", "pixie")
    

    def isActive(self):
    	"""
        This method activates the 'Render Mode' GUI controls and 
        connects events to them and to the handler methods of this
        class. 

        **Parameters:** This method has no parameters.

        """
        #connect buttons to  function
        self.scene.connect("LMOUSEP",self.povExport,self.bPovray)
        self.scene.connect("LMOUSEP",self.rendermanExportA,self.bAqsis)
        self.scene.connect("LMOUSEP",self.rendermanExportP,self.bPixie)
        for ob in self.renderGuiObjs:            
            ob.setCameraProjection(0)
            ob.setVisibility(1)
            ob.setShadeless(1)                
         

    def isNotActive(self):        
    	"""
        This method disactivates the 'Render Mode' GUI controls. 

        **Parameters:** This method has no parameters.

        """
        
        for ob in self.renderGuiObjs:
            ob.setVisibility(0)


