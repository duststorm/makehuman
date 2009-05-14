# You may use, modify and redistribute this module under the terms of the GNU GPL.
"""
Classes for widgets (GUI utilities). 

===========================  ===============================================================
Project Name:                **MakeHuman**                                                  
Module File Location:        mh_core/widgets3d.py                                           
Product Home Page:           http://www.makehuman.org/                                      
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/                     
Authors:                     Manuel Bastioni, Marc Flerackers                               
Copyright(c):                MakeHuman Team 2001-2009                                       
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards  
===========================  ===============================================================

This module contains classes defined to implement widgets that provide utility functions 
to the graphical user interface.

"""

import files3d

class ProgressBar:
    """
    A ProgressBar widget. This widget can be used to show the user the progress of a 
    lengthy operation.
    """
    
    def __init__(self, scene):
        """
        This is the constructor method for the ProgressBar class. It initializes the
        following attributes:

        - **self.scene**: *scene reference*. The scene the widget is part of.
        - **self.background**: *Object3D*. The background object.
        - **self.bar**: *Object3D*. The bar object.
        """
        
        self.scene = scene
        self.background = files3d.loadMesh(scene, "data/3dobjs/progressbar_background.obj")
        self.bar = files3d.loadMesh(scene, "data/3dobjs/progressbar.obj", loadColors = None)
        self.background.setCameraProjection(0)
        self.background.setVisibility(1)
        self.bar.setCameraProjection(0)
        self.bar.setVisibility(1)
        self.background.setLoc(0.0, -0.20, 9.1)
        self.bar.setLoc(-0.08, -0.178, 9.2)
        self.background.setTexture("data/images/progressbar_background.png")
        self.background.setShadeless(1)
        self.bar.setTexture("data/images/progressbar.png")
        self.bar.setShadeless(1)

        #TODO: Add setLocation, setScale, etc.. methods

    def setProgress(self, progress, redraw = 1):
        """
        This method updates the progress and optionally updates the screen

        Parameters
        ----------

        progress:
            *float* The progress from 0.0 to 1.0.
        redraw:
            *int* 1 if a redraw is needed, 0 otherwise.
        """
        
        self.bar.setScale(progress, 1.0, 1.0);
        if redraw:
          self.scene.redraw(0)

    def setVisibility(self, visible):
        """
        This method updates the visibility flag of the widget

        Parameters
        ----------

        visible:
            *int* 1 for visible, 0 otherwise.
        """
        
        self.background.setVisibility(visible);
        self.bar.setVisibility(visible);
