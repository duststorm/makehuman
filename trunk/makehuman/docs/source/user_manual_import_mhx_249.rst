.. _mhx249:

#######################
MHX for Blender 2.49
#######################

.. note::

    The Blender 2.4 series is becoming obsolete and development has stopped. New features are only implemented for Blender 2.5x.

***********************    
Preparation of Blender
***********************

Before we can import the mhx file into Blender In the makehuman/importers/mhx/blender249 directory there is a file called ”mhx_import.py”, which you need to copy into your Blender scripts directory. Note that you need to restart Blender after the script has been copied.

.. note::

    IMPORTANT: In order for driven shapekeys to work, a file called pydrivers.py must be loaded into a text editor window in Blender. This file is also located in the makehuman/importers/mhx/blender249 directory. Note that this file should not be executed, it just needs to exist in an open text window.

Some MakeHuman installers make an attempt to copy the file to the correct place in the Blender scripts folder. If so, no preparation is necessary.

It may happen that you don’t have privileges to copy files to the Blender scripts directory; this happens on my Ubuntu box at home. If so, just open the mhx_import.py script in a text window in Blender and execute it from there.

*********************
Import into Blender
*********************

When Blender starts up, there should a new entry in the file > Imports menu which says Makehuman (.mhx). If it is not there (after you have restarted Blender), just load the mhx_import.py file into a text editor in Blender and execute it from there.

.. figure::  _static/blender-import.png
   :align:   center
   
Either way, you should now be prompted with a blue screen. Here you can select a number of options:

.. figure::  _static/mhx-choices.png
   :align:   center
   
* Should the rig have dynamic FK/IK switching? As discussed on another page, there are some problems associated with this, so only use it if you need it.
* Should the legs use IK (inverse kinematics)? This has no effect if FK/IK switch is selected.
* Should the arms use IK (inverse kinematics)? This has no effect if FK/IK switch is selected.
* Should the fingers use IK (inverse kinematics)?
* Should shapekeys for facial morphs be loaded. This takes some time and the blend file becomes quite big.
* Should body shape keys be loaded? These are used to preserve volume during deformation and to give some impression of muscle flexing. Again, there is a load-time and size penalty for loading shapekeys.
* Should the character be rotated 90 degrees, to have his head point up? MakeHuman and Blender use different conventions (Y up and Z up, respectively), so unless this button is selected, the character will come into Blender lying on her back.
* Should the character be loaded into a fresh scene? It is best to hit Ctrl-X and import into a pristine blend file. 
* Should Blender use custom display objects for bones? 
* Select a texture file with an image browser, in order to tell the import script in which directory to look for textures. The exact file does not matter, only the directory in which it is located.
* After these selections are made, press the ”Load MHX file” button, and select the mhx file in the MakeHuman exports directory with a file browser.


By default two mhx files are imported for each character, with filenames ending in -24.mhx and -25.mhx. These are meant for use with Blender 2.4x (really only 2.49b) and Blender 2.5x, respectively. Because the python API is completely different between these two Blender versions, it is not possible to load the same file into both versions. *The -24 file is meant for Blender 2.49b*.

After a number of seconds, you should see something like the image below; the character is loaded into Blender, with a panel above and beside him. We are now ready to start posing. 

How to do this is described at TODO

.. figure::  _static/oldman.png
   :align:   center

***************************
To render the character
***************************

Windows users can now render the character by hitting the F12 key, but Linux users will only see a blank blue screen. This is a Blender bug. Apparently Blender can not read TIFF files (at least not the MH textures) under Linux, although there are no problems on Windows. Unfortunately the bug seems to be present in Blender 2.50 as well. If you look at the material editor, you see that the skin shader material is invisible, and that the textures are black (except for the procedural bump).

Workaround:
=============

Convert the textures to PNG, and put them into a directory of choice. If you put them into the default export directory, ~/makehuman/exports, they will be loaded instead of the TIFF files in the release. If the new textures are located somewhere else, you need to tell the import script by pressing the Texture Directory button (10) before loading the MHX files.

Use the same procedure to modify the textures, e.g. to paint clothes on the character.

To convert a texture to PNG under Ubuntu:

1. Double-click on the TIFF file, e.g. texture.tif.
2. The file is opened in a program which calls itself Eye of GNOME - the GNOME image viewer.
3. file > Save as.
4. Change the filename to texture.png and click OK.

Texture directory
==================

The import script looks for the following files in order to find the image "texture":

* ~/makehuman/exports/texture.png
* ~/makehuman/exports/texture.tif
* ./data/textures/texture.png
* ./data/textures/texture.tif

Here "~" is the user's home directory, e.g. "/home/thomas" or "C:\Documents and Settings\Thomas", and "." is the directory where the MakeHuman program is located, e.g. "/usr/share/makehuman" or "C:\Program files\Makehuman". The first two texture files can be changed by pressing button 10, "Texture Directory" in the MHX user interface above, and choosing a file in another directory.

Note that the MakeHuman distribution comes with texture files in the TIFF format. The rationale for looking for the corresponding PNG files is to avoid the render bug on Linux mentioned above. This should not be a problem for Windows users, because the PNG files are simply ignored if they do not exist.

finally
=========

Once any texture problems have been fixed, rendering should produce an image similar to the one below. If you run into any problems, the first place to look is the MHX FAQ at TODO

.. figure::  _static/angry-old-man.png
   :align:   center
