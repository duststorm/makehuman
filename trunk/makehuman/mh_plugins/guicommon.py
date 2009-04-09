""" 
Class for handling common GUI functions.

===========================  ===============================================================  
Project Name:                **MakeHuman**                                                  
Module File Location:        mh_plugins/guicommon.py                                          
Product Home Page:           http://www.makehuman.org/                                      
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/                     
Authors:                     Manuel Bastioni, Marc Flerackers                                            
Copyright(c):                MakeHuman Team 2001-2009                                       
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards  
===========================  ===============================================================  

This module implements the 'Guicommon' class structures and methods to support functions
shared by all GUI plugins.

User actions (keyboard and mouse events) are passed into 
the appropriate class for processing. 

Having processed an event this class returns control to the 
OpenGL/SDL/Application event handling loop.  

"""

__docformat__ = 'restructuredtext'

import files3d

class Guicommon:
    """
    The data structures and methods to support the shared GUI functions. 
    One instance of this class (named gCommon) is instantiated by main.py 
    at application startup. 
    """

    def __init__(self, globalScene):
        """
        This is the constructor method for the guitoolbar class. 
        It initializes the following attributes:

        - **self.toolbarGuiObjs**: *object list*. A list of GUI objects.
          Initialised to an empty list then populated by calls to the 
          *files3d.loadMesh* method.
        - **self.modifiedGUIObjs**: *object list*. A list of modified GUI 
          objects.
          Default: Empty list.        
        - **self.scene**: *Scene3D*. A reference to the global scene object 
          passed in as a parameter to this constructor method.
        - **self.bExit**: *object reference*. A reference to the 
          'Exit' GUI control object (button).
        - **self.bHome**: *object reference*. A reference to the 
          'Home Mode' GUI control object (button).
        - **self.bFile**: *object reference*. A reference to the 
          'File Mode' GUI control object (button).
        - **self.bExpr**: *object reference*. A reference to the 
          'Expression Mode' GUI control object (button).
        - **self.bPose**: *object reference*. A reference to the 
          'Pose Mode' GUI control object (button).
        - **self.bRend**: *object reference*. A reference to the 
          'Render Mode' GUI control object (button).
        - **self.bMeas**: *object reference*. A reference to the 
          'Measurements Mode' GUI control object (button).


        Parameters
        ----------

        globalScene:
            *Scene3D*. A reference to the global scene object.
        """
        print "GUI common initialized"
        self.scene = globalScene
        self.commonGuiObjs = []        
        self.modifiedObjs = set()

        #The cursor is shared in all GUI, so it's loaded as common element
        self.cursor = files3d.loadMesh(self.scene,"data/3dobjs/cursor.obj",\
                        self.commonGuiObjs,0.0,0.0,9.5)
        self.cursor.setTexture("data/images/cursor.png")
                        

    def cursorMotion(self):
        """
        This method sets the current cursor position based upon the current
        position of the mouse.

        **Parameters:** None.

        """        
        mousePos = self.scene.getMousePosGUI()
        self.cursor.setLoc(mousePos[0],mousePos[1],self.cursor.z)        
        self.scene.redraw()        

    def faceGroupSelection(self):
        """
        This method calls the selectObject method on the Scene3D class to first 
        deselect any objects in the scene that are currently selected, then, if 
        an object was selected by the current operation, to mark that object as 
        selected.
        
        Although run as part of the guicommon module, this method is run 
        whenever a left mouse click is detected and not just on elements that 
        constitute common GUI objects. Both Guicommon and Mode-specific 
        GUI elements will be called separately based upon the GUI object 
        set by this method.

        **Parameters:** None.

        """
        
        #TODO Maybe it's better to link separate functions to each button,
        #defined in the separate files, instead define a general one here.
        self.scene.selectObject()
        ob = self.scene.getSelectedObject()        
        faceGroupSel = ob.faceGroupSelected
  
        #print "DEBUG FACEGROUP SEL",faceGroupSel.name


    def isActive(self):
    	"""
        This method activates the objects common to all plugins and registers 
        application-level event handling functions. 
        
        First it registers the Guicommon faceGroupSelection method to receive all right 
        and left mouse click events (whether related to the Guicommon objects or not). 
        It then registers the Guicommon cursorMotion method to receive all mouse 
        movement events (whether related to the Guicommon objects or not).
        Finally it makes the Guicommon objects visible.

        **Parameters:** This method has no parameters.

        """

        #connect scene events to functions
        self.scene.connect("LMOUSEP",self.faceGroupSelection) #TODO This must be well underlined in doc
        self.scene.connect("RMOUSEP",self.faceGroupSelection) #TODO This must be well underlined in doc
        self.scene.connect("PMOTION",self.cursorMotion)        
        for ob in self.commonGuiObjs:            
            ob.setCameraProjection(0)
            ob.setVisibility(1)
            ob.setShadeless(1)       

    def isNotActive(self):        
    	"""
        This method disactivates the toolbar and hides the controls. 

        **Parameters:** This method has no parameters.

        """

        for ob in self.commonGuiObjs:
            ob.setVisibility(0)

    

        

            


