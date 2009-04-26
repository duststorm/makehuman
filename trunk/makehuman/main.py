# You may use, modify and redistribute this module under the terms of the GNU GPL.
""" 
The main MakeHuman Python Application file.

===========================  ==================================================================  
Project Name:                **MakeHuman**                                                  
Module File Location:        main.py                                          
Product Home Page:           http://www.makehuman.org/                                      
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/                     
Authors:                     Manuel Bastioni (individual developers look into the AUTHORS file)                                       
Copyright(c):                MakeHuman Team 2001-2008                                       
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards  
===========================  ==================================================================  

This is the main MakeHuman Python Application file which participates in the 
application startup process. It contains functions that respond to events 
affecting the main GUI toolbar along the top of the screen in all modes to
support switching between modes. 

When the MakeHuman application is launched the *main* function from the C 
application file *main.c* runs. This creates an integration layer by 
dynamically generating a Python module (called 'mh'). That *main* function 
then either imports this Python *main* module or executes this Python 
script *main.py* (depending on platform). 

This script displays a splash screen and a progress bar as it loads the 
initial 3D humanoid model (the neutral base object) and adds the various
GUI sections into the scene. It creates the main toolbar that enables the
user to switch between different GUI modes and defines functions to 
perform that switch for all active buttons. Active buttons are connected
to these functions by being registered to receive events.
 
At the end of the initiation process the splash screen is hidden and 
Modelling mode is activated. The 'startEventLoop' method on the main Scene3D 
object is invoked to call the OpenGL/SDL C functions that manage the 
low-level event loop. 

This Python module responds to high-level GUI toolbar events to switch 
between different GUI modes, but otherwise events are handled by GUI mode
specific Python modules.

"""

__docformat__ = 'restructuredtext'

import sys
sys.path.append("./")
sys.path.append("./mh_plugins")
sys.path.append("./mh_core")

if 'nt' in sys.builtin_module_names:
    sys.path.append("./pythonmodules")

import os
import webbrowser
import module3d
import files3d
import widgets3d
import human

#GUI sections are plugins
import guicommon
import guitoolbar
import guimodelling
import guifiles
import guirender

# Global element shared between more than one gui section
mainScene = module3d.Scene3D()
mainScene.startWindow() #Use scene.startWindow(1) to enable animation

# Dispkay the initial splash screen and the progress bar during startup 
splash = files3d.loadMesh(mainScene, "data/3dobjs/splash.obj", loadColors = None)
splash.setTexture("data/images/splash.png")
splash.setShadeless(1)
splash.setCameraProjection(0)
progressBar = widgets3d.ProgressBar(mainScene)
mainScene.update()

progressBar.setProgress(0.1)

# Create aqsis shaders
os.system("aqsl data/shaders/aqsis/lightmap_aqsis.sl -o data/shaders/aqsis/lightmap.slx")
os.system("aqsl data/shaders/renderman/skin.sl -o data/shaders/renderman/skin.slx")

# Create pixie shaders
os.system("sdrc data/shaders/pixie/lightmap_pixie.sl -o data/shaders/pixie/lightmap.sdr")
os.system("sdrc data/shaders/pixie/read2dbm_pixie.sl -o data/shaders/pixie/read2dbm.sdr")
os.system("sdrc data/shaders/renderman/skin.sl -o data/shaders/renderman/skin.sdr")

progressBar.setProgress(0.2)

# Load the base humanoid mesh
humanMesh = human.Human(mainScene, "data/3dobjs/base.obj")
mainScene.selectedHuman = humanMesh

progressBar.setProgress(0.5)

# Add GUI sections into the main Scene3D object
gToolbar = guitoolbar.Guitoolbar(mainScene)
progressBar.setProgress(0.6)
gModelling = guimodelling.Guimodelling(mainScene)
progressBar.setProgress(0.7)
gFile = guifiles.Guifiles(mainScene, gModelling)
progressBar.setProgress(0.8)
gRender = guirender.Guirender(mainScene)
progressBar.setProgress(0.9)
gCommon = guicommon.Guicommon(mainScene)
progressBar.setProgress(1.0)

# Call the update method on the Scene3D object to send the GUI elements to 
# the 3D engine. Then remove the splash screen and progress bar.
mainScene.update()
humanMesh.setTexture("data/textures/texture.tif")
splash.setVisibility(0)
progressBar.setVisibility(0)

# Toolbar functions. 
# The toolbar is the common GUI element present along the top of the screen in
# all of the different GUI modes. A function for each active toolbar function 
# needs to be declared here so that it can be invoked no matter which mode the 
# GUI is currently in.
#
def exitMode():
    """
    This function is called when the exit toolbar button is pressed to terminate 
    the application.
    
    **Parameters:** This function has no parameters.
 
    """
    mainScene.shutdown();

def fileMode():
    """
    This function is called when the fileMode toolbar button is pressed to activate
    the file mode GUI elements and to disactivate other toolbar-controlled modes. 
  
    **Parameters:** This function has no parameters.
 
    """
    gToolbar.buttonsMotion()
    #gToolbar.isNotActive()         
    gRender.isNotActive()
    gModelling.isNotActive()
    gFile.isActive()

def renderMode():
    """
    This function is called when the renderMode toolbar button is pressed to activate
    the render mode GUI elements and to disactivate other toolbar-controlled modes. 
  
    **Parameters:** This function has no parameters.
 
    """
    gToolbar.buttonsMotion()
    #gToolbar.isNotActive() 
    gFile.isNotActive()        
    gModelling.isNotActive()  
    gRender.isActive()  

def modellingMode():
    """
    This function is called when the modellingMode toolbar button (Home) is pressed to
    activate the modelling Mode GUI elements and to disactivate other toolbar-controlled modes. 
  
    **Parameters:** This function has no parameters.
 
    """    
    gToolbar.buttonsMotion()
    gToolbar.isActive() 
    gFile.isNotActive()
    gRender.isNotActive()    
    gModelling.isActive()

def helpMode():
    """
    This function is called when the help toolbar button is pressed to display the Users Guide 
    pdf file.
    
    **Parameters:** This function has no parameters.
 
    """
    webbrowser.open(os.getcwd()+"/docs/MH_1.0.A1_Users_Guide.pdf");
    
# Connect the toolbar functions to the toolbar button mouse click events.
mainScene.connect("LMOUSEP",exitMode,gToolbar.bExit)
mainScene.connect("LMOUSEP",fileMode,gToolbar.bFile)
mainScene.connect("LMOUSEP",modellingMode,gToolbar.bHome)
mainScene.connect("LMOUSEP",renderMode,gToolbar.bRend)
mainScene.connect("LMOUSEP",helpMode,gToolbar.bAbou)
mainScene.setTimeTimer(100)#If animation is enabled this is the framerate in millisec

# Make sure the GUI toolbar is active and in modelling mode. 
gCommon.isActive()
modellingMode()

# Initiate the main low-level event loop (controlled by OpenGL/SDL in glmodule.c)
mainScene.startEventLoop()
