.. _mhx249:

#######################
MHX for Blender 2.5x
#######################

*************
Preparation
*************

The MHX importer is implemented as a Blender add-on, and is distributed with Blender. However, neither MakeHuman nor Blender have yet reached a completely stable state, and it may happen that the MHX importer that comes with Blender is broken, most likely due to a change in the Python API. 

If this happens, you need to copy the MHX importer that comes with MakeHuman to the Blender addons directory, as described in TODO . The version of the MHX importer that comes with MakeHuman is always the most up-to-date one.

At the time of writing, no problems are known about the version of the MHX importer (version 1.0.3) that comes with Blender 2.56 beta. Copying the MHX importer from MakeHuman to Blender is hence not necessary.

*****************
Enable add-on
*****************

After Blender has been started, the MHX importer must be enabled before it can be used. This is described in TODO.

***********************
Importing the MHX file
***********************

Once the MHX importer has been enabled, you can import MHX files by  going to the File > Import > Import MHX menu.
 
In the file selector that appears, select the MHX file that we just  exported from MakeHuman. Since we are using version 2.56 of Blender,  the file to load is alia-25.mhx. The file alia-24.mhx is intended for the essentially obsolete Blender 2.49b.

.. figure::  _static/import-menu.png
    :align:   center
   
File > Import > Import MakeHuman (.mhx)

.. figure::  _static/import-mhx.png
    :align:   center

Select the correct MHX file and press Import
 
And after a while a rigged and dressed character appears in the viewport.
 
.. figure::  _static/alia-loaded.png
    :align:   center
   
The picture looks rather complicated, because several objects are loaded  at the same time. To have a clearer view, we select a single layer at a  time.
 
.. figure::  _static/layers.png
    :align:   center
   
The objects on the different layers

1. The high-poly character mesh.
2. The armature.
3. Low-poly proxy meshes.
4. A cage, intended for use with the mesh-deform modifier (experimental).
5. Clothes
6. More clothes
7. Reserved for even more clothes.
8. The last layer made visible by default. 

****************
Import options
****************

Scale
======

MakeHuman uses decimeters internally, so scale 1.0 means that 1 b.u. = 1 dm.  If your scene is made at another scale, the scale should be changed accordingly.  E.g. set scale = 0.1 if your unit is meters, and scale = 1/0.254 = 3.94 if it is inches. It is preferable to import with a scale rather than importing at scale = 1 and then rescaling the character in Blender, because the scale parameter affects parameters  that are not so obvious. E.g. the SSS (subsurface scattering) scale needs to be  adjusted for plausible renders. The figure illustrates what happens if you rescale  the mesh in Blender without adjusting the SSS scale.

.. figure::  _static/import-scales.png
    :align:   center

    Effect of scale factor: (a) Character imported with scale 0.1.(b) Character imported with scale 1.0, then scaled down in Blender.(c) Character imported with scale 1.0, then scaled up in Blender. 


Enforce version
================


Both the MHX importer and MHX files have a version number, whose main purpose is to keep them synchronized. An MHX file is usually incompatible with the importer if their version
numbers differ. You can try to import the MHX file anyway, but it is not recommended. A better alternative is to load the character into an updated version of MakeHuman  (you did save your character, right?) and reexport to MHX again. 
 
By default it is an error to try to import an MHX file with a different version number. You can override this default by unchecking this checkbox, but you do so at your own peril.
 
Proxies
========
As we saw in the figure above, low-poly versions (zero or more, depending on the settings in mh_export.config) of the character appeared on layer 3. These proxy meshes could  be useful for realtime game character, or perhaps for background characters in a movie.
 
Replace scene
==============

Delete all meshes, armatures and empties presently in the scene.  Other objects, such as cameras and lamps, are not affected.
 
Cage
=====

With the right configuration in mh_export.config, the MHX file can contain a cage which encloses the mesh. This feature is indended to work with Blender's mesh-deform modifier, and is further described in https://sites.google.com/site/makehumandocs/blender-export-and-mhx/mhx-import-in-blender-2-5/cage-and .
 
Clothes
========

As we saw in a figure above, the character was dressed in the MHX file, provided that the appropriate files were enabled in mh_export.config. The clothes are very simplistic and of a  boring unisex type, but at least they allow you to put your animations on youtube without being censored. More significantly, the imported clothes can be a starting point for more interesting garment.
 
Stretchy limbs
================

This is a feature most often seen in cartoony characters; Elastagirl from The Incredibles is an extreme example. Since MakeHuman characters are supposed to be realistic, this feature is disabled by default.
 
Face shapes
=============

The MHX mesh comes with shapekeys that can be used to construct facial expressions and visemes, cf. the lipsync discussion at https://sites.google.com/site/makehumandocs/blender-export-and-mhx/lipsync-tool. If you know that your character will not need to change his facial expression, you can save some time and a lot of space by disabling this feature.
 
Body shapes
==============

On several occasions I have tried to fix bad deformations by making corrective shapekeys, This has never really worked out well, especially not in the shoulder and groin regions. For now MHX files do not contain any corrective shapes, so this option does nothing.
 
Symmetric shapes
=================

Many shapekeys are asymmetric and come in a left and a right version. However, they are stored symmetrically and filtered through the Left and Right vertex groups. For those who make shapekeys for the MHX mesh (i.e. myself) it is useful to be able to import a  single symmetric shapekey to start with. If this option is checked, the character is loaded e.g. with a single Smile shape, rather than with a Smile_L and a Smile_R shape.
 
Diamonds
=============

The MakeHuman mesh has a number of little diamonds which are used for placing joints. The animator is usually not interested in seeing these diamonds, and therefore they are deleted by default when the mesh is imported into Blender. The importer can easily recognize the diamonds, because they consist of trianglular faces whereas the rest of the MakeHuman mesh is pure quad. However, there are occasions when it is necessary to include the diamonds during import, in order to maintain the correct vertex numbers. Clothes and low-poly proxy meshes are defined in terms of the vertices of the main mesh. The utility for making clothes therefore only works if the main mesh is imported with diamonds intact. 
 

Joint diamonds used for placing joints.

.. figure::  _static/diamonds.png
    :align:   center
    
Bend joints
============
In Blender, IK works best if the mesh is modelled with slightly bent elbows and knees. However, the MakeHuman mesh was not made in this way, and changing that is not an option. With this option checked, the MHX importer bends the joints at load time, giving better IK behavior.
 
Joint bending has not been tried for quite some time, and I doubt that it works anymore. Joints should not be bent in a rig intended for use with mocap, which is presently the case, so just leave this option unchecked.
