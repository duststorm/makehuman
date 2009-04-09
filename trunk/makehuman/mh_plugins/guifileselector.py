# You may use, modify and redistribute this module under the terms of the GNU GPL.
""" 
Class for handling the file selector used in File mode in the GUI.

===========================  ===============================================================  
Project Name:                **MakeHuman**                                                  
Module File Location:        mh_plugins/guifileselector.py                                          
Product Home Page:           http://www.makehuman.org/                                      
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/                     
Authors:                     Manuel Bastioni                                            
Copyright(c):                MakeHuman Team 2001-2008                                       
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards  
===========================  ===============================================================  

This module implements the 'guifileselector' class structures and methods to support the 
file selector object which is used when the application GUI is in File mode.
File mode is invoked by selecting the File mode icon from the main GUI control bar at the 
top of the screen. 
While in this mode, user actions (keyboard and mouse events) are passed into 
the guifiles class for processing. 
User actions related to this control are passed through to this class to be handled.

Having processed an event control is returned to the main OpenGL/SDL/Application event handling loop.  

"""

__docformat__ = 'restructuredtext'

import files3d

class Guifileselector:
    """
    The data structures and methods to support the File selector object that is 
    active when the GUI is in File mode. 
    
    One instance of this class (named guifiles.gFileSelector) is instantiated 
    by guifiles.py when the guifiles constructor class is instantiated at 
    application startup.
    """

    def __init__(self, globalScene, commonGUI = None):
        """
        This is the constructor method for the guifileselector class. 
        It initializes the following attributes:

        - **self.selectorGuiObjs**: *object list*. A list of GUI objects.
          Initialised to an empty list then populated by calls to the 
          *files3d.loadMesh* method.
        - **self.modifiedGUIObjs**: *object list*. A list of modified GUI 
          objects.
          Default: Empty list.

        - **self.textString**: *string*. A text string. 
          Default: Empty string.

        - **self.scene**: *Scene3D*. A reference to the global scene object 
          passed in as a parameter to this constructor method.
        - **self.empty**: *object reference*. A reference to the 
          'empty' GUI control object.
        - **self.bConfirm**: *object reference*. A reference to the 
          'confirm' GUI control object (button).

        Parameters
        ----------

        globalScene:
            *Scene3D*. A reference to the global scene object.
        """
        print "GUI selector initialized"
        self.selectorGuiObjs = []
        self.modifiedGUIObjs = set()        
        self.textString = ""
        self.scene = globalScene        
        files3d.loadMesh(self.scene,"data/3dobjs/fileselectorbar.obj", self.selectorGuiObjs,0.0,0.30,9)
        files3d.loadMesh(self.scene,"data/3dobjs/backgroundtext.obj", self.selectorGuiObjs,0.0,1.3,5.5)
        self.empty = files3d.loadMesh(self.scene,"data/3dobjs/empty.obj", self.selectorGuiObjs,-0.3,0.29,6)
        self.bConfirm = files3d.loadMesh(self.scene,"data/3dobjs/button_confirm.obj", self.selectorGuiObjs,0.35,0.28,9.1)
        self.bConfirm.setTexture("data/images/button_confirm.png")
        

    def typeText(self):
    	"""
        This method adds text to the 'empty' object associated with the 
        'file selector' GUI control object.

        **Parameters:** This method has no parameters.

        """
         
        lenText = len(self.textString)    
        if self.scene.keyPressed == 8:
            self.textString = self.textString[:-1]
        elif self.scene.keyPressed < 256 and self.scene.keyPressed != 13:
            self.textString += self.scene.characterPressed        
            
        lenText = len(self.textString)
        if lenText > 100:
            textToVisualize = self.textString[(lenText-100):]
        else:
            textToVisualize = self.textString
        self.empty.setText(textToVisualize)    
        self.scene.redraw()

    def isActive(self):
    	"""
        This method activates the 'file selector' GUI control object.

        **Parameters:** This method has no parameters.

        """

        self.scene.connect("KEYBOARD",self.typeText)

        for ob in self.selectorGuiObjs:            
            ob.setCameraProjection(0)
            ob.setVisibility(1)
            ob.setShadeless(1)
                 
        self.empty.setText(self.textString)   

    def isNotActive(self):        
    	"""
        This method disactivates the 'file selector' GUI control object
        and hides the controls.

        **Parameters:** This method has no parameters.

        """
        self.scene.disconnect("KEYBOARD")
        for ob in self.selectorGuiObjs:
            ob.setVisibility(0)
