""" 
Class for handling the main GUI toolbar.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements the 'guitoolbar' class structures and methods to support GUI 
toolbar operations.

The main GUI control bar at the top of the screen is used to switch between the different 
operational modes that the GUI supports.

User actions (keyboard and mouse events) are passed into 
the appropriate class for processing. 

Having processed an event this class returns control to the 
main OpenGL/SDL/Application event handling loop.  

"""

__docformat__ = 'restructuredtext'


import files3d


class Guitoolbar:
    """
    The data structures and methods to support the GUI toolbar. 
    One instance of this class (named gToolbar) is instantiated by main.py 
    at application startup to handle user interaction with the MakeHuman GUI 
    toolbar. This mostly involves switching between the different operational
    modes supported by the application by calling methods on the appropriate
    classes to activate and deactivate different modes of operation.
    """

    def __init__(self, globalScene, commonGUI = None):
        """
        This is the constructor method for the guitoolbar class. 
        It initializes the following attributes:

        - **self.toolbarGuiObjs**: *object list*. A list of GUI objects.
          Initialised to an empty list then populated by calls to the 
          *files3d.loadMesh* method.
        - **self.modifiedGUIObjs**: *object list*. A list of modified GUI 
          objects.
          Default: Empty list.
        - **self.sleepCounter**: *integer*. An integer recording the **???**.
          Default: 0.
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
        - **self.cursor**: *object reference*. A reference to the 
          cursor object.

        Parameters
        ----------

        globalScene:
            *Scene3D*. A reference to the global scene object.
        """
        print "GUI toolbar initialized"
        self.toolbarGuiObjs = []        
        self.modifiedGUIObjs = set()            
        self.scene = globalScene

        
        #Load all objs of default GUI
        self.bUpperbar = files3d.loadMesh(self.scene,"data/3dobjs/upperbar.obj", self.toolbarGuiObjs,0,0.39,9)
        files3d.loadMesh(self.scene,"data/3dobjs/backgroundbox.obj", self.toolbarGuiObjs,0,0,-72)
        self.bLowerbar = files3d.loadMesh(self.scene,"data/3dobjs/lowerbar.obj", self.toolbarGuiObjs,0,-0.39,9)        
        self.bExit = files3d.loadMesh(self.scene,"data/3dobjs/button_exit.obj",\
                        self.toolbarGuiObjs,0.5,0.39,9)
        self.bHome = files3d.loadMesh(self.scene,"data/3dobjs/button_home.obj",\
                        self.toolbarGuiObjs,-0.5,0.39,9)
        self.bFile = files3d.loadMesh(self.scene,"data/3dobjs/button_loadsave.obj",\
                        self.toolbarGuiObjs,-0.358,0.39,9)
        self.bExpr = files3d.loadMesh(self.scene,"data/3dobjs/button_expressions.obj",\
                        self.toolbarGuiObjs,-0.216,0.39,9)
        self.bPose = files3d.loadMesh(self.scene,"data/3dobjs/button_poses.obj",\
                        self.toolbarGuiObjs,-0.074,0.39,9)
        self.bRend = files3d.loadMesh(self.scene,"data/3dobjs/button_render.obj",\
                        self.toolbarGuiObjs,0.074,0.39,9)
        self.bMeas = files3d.loadMesh(self.scene,"data/3dobjs/button_measure.obj",\
                        self.toolbarGuiObjs,0.216,0.39,9)
        self.bAbou = files3d.loadMesh(self.scene,"data/3dobjs/button_about.obj",\
                        self.toolbarGuiObjs,0.358,0.39,9)
                        
        self.bUpperbar.setTexture("data/images/upperbar.png")
        self.bLowerbar.setTexture("data/images/lowerbar.png")
        self.bExit.setTexture("data/images/button_exit.png")
        self.bHome.setTexture("data/images/button_home.png")
        self.bFile.setTexture("data/images/button_loadsave.png")
        self.bExpr.setTexture("data/images/button_expressions.png")
        self.bPose.setTexture("data/images/button_poses.png")
        self.bRend.setTexture("data/images/button_render.png")
        self.bMeas.setTexture("data/images/button_measure.png")
        self.bAbou.setTexture("data/images/button_about.png")
        
        
    def buttonsMotion(self):
        """
        This method enables a GUI button to be scaled and for any button
        previously scaled to be reset to its original size.

        **Parameters:** None.

        """
        #First reset the position of other buttons
        for n in range(len(self.modifiedGUIObjs)):
            name = self.modifiedGUIObjs.pop()
            objToReset = self.scene.getObject(name)
            y = objToReset.y + .0075 #TODO: add an attribute with defult coord
            objToReset.setLoc(objToReset.x, y, objToReset.z)
            objToReset.setScale(1,1,1)

        #Then move the button selected
        ob = self.scene.getSelectedObject()
        if ob:
            if ob.name not in self.modifiedGUIObjs:
                s = 1
                #translate and scale the selected button
                for i in range(3):
                    s += .15
                    y = ob.y - .0025
                    ob.setLoc(ob.x, y, ob.z)
                    ob.setScale(s,s,s)
                    self.scene.redraw()
                self.modifiedGUIObjs.add(ob.name)

    def isActive(self):
    	"""
        This method activates the toolbar.

        **Parameters:** This method has no parameters.

        """

        for ob in self.toolbarGuiObjs:            
            ob.setCameraProjection(0)            
            ob.setVisibility(1)
            ob.setShadeless(1)       

    def isNotActive(self):        
    	"""
        This method disactivates the toolbar and hides the controls. 

        **Parameters:** This method has no parameters.

        """

        for ob in self.toolbarGuiObjs:
            ob.setVisibility(0)

        

            


