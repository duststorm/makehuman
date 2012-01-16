.. _files:

.. highlight:: python
   :linenothreshold: 5

############
files
############

.. figure::  _static/files.png
   :align:   center   

***************
Save and Load
***************

Saving and loading happens in a custom and optimized format for MakeHuman with the *mhm* extension. It is advised to always save in this format also when you export models, since you can’t load any other format back into MakeHuman. 

This is important when you want to make changes at a later stage of production.

***********
Export
***********

MakeHuman is a great program, but it does not exist in isolation. After designing your character in MakeHuman, you probably want to export it to some other 3D package for posing, animation, or rendering. There are currently three possibilities:

* Wavefront (obj)
* Collada (dae)
* Quake (md5)
* MakeHuman eXchange (mhx)
* Stereolithography (stl)

Wavefront (obj)
================

This is a very simple format to export the mesh, with vertices, faces and UV coordinates. Originally invented by Alias/Wavefront, all major 3D packages have OBJ importers, so this format allows you to export to the greatest range of applications. However, the character is not rigged but rather a static prop.
Wavefront obj is a good choice when you need a simple mesh for an external renderer. It comes with an mtl file defining the material.


Eyebrows
-----------
For some uses, like raytracing, the eyebrow geometry causes problems. If this is the case, uncheck it to avoid it from being exported.

Diamonds
---------

The diamond geometry is used to keep track of the skeleton. However in most cases this is not needed. In case the diamond geometry is desired, check it to export it.

Skeleton
-----------

This option exports the skeleton in Biovision hierarchical data (bvh) format which is generally used for motion capture. Note however that the model is not rigged to this skeleton.

Groups
----------

Whether groups are useful depends on the software used. Many importers also give the option to import the groups or not. Groups can be used to select specific body parts for modification or deletion. If groups are not desired, uncheck it.

Subdivide
----------

If a high poly mesh is needed, and the modeler or renderer used does not have a good subdivision algorithm, you can check the subdivide option to export a mesh with 4 times the amount of faces, generated with Catmull-Clark subdivision.

Blender exchange (mhx)
------------------------

MakeHuman eXchange format is a Blender-specific format invented by the MakeHuman team. It allows a fully rigged and textured character with shapekeys to be imported into Blender by the custom MHX importer. It does not work for any other 3D application except Blender.

A rigged character can be imported into Blender using both the MHX and DAE formats. However, the MHX rig is much more advanced. It is very difficult for a cross-platform format like Collada to handle advanced rigs, since constraints, drivers, material settings, etc. are implemented very differently on different platforms. The rigs exported with Collada are therefore of a very straightforward kind without any constraints. On the other hand, this may be desirable e.g. for games or motion capture, and it is your only option if you are not using Blender. In contrast, the MHX format allows access to almost every setting in Blender.

Version
----------

Currently it is still possible to export for Blender 2.4, however this may change once Blender 2.5 is stable.

Expressions
-------------

If checked, all expressions available within MakeHuman are exported to the mhx, this makes the export considerably bigger in size.

Rig
------

Two rigs are available, mhx rig or game rig. For posing and animating the mhx rig is preferred.

Collada (dae)
==============

Collada is a comprehensive scene description language understood by many 3D applications. It also exports a rigged and textured character.

Quake (md5)
============

The md5 exporter is not yet fully functional, the skin is not correctly attached to the skeleton.

Stereolithography (stl)
========================

Stereolithography is a format used for 3d printing.

Format
--------

The binary format is a lot more compact than the ASCII format. However the latter is provided for compatibility reasons.

Subdivide
------------

If a high poly mesh is needed, and the exernal modeler or renderer does not have a good subdivision algorithm, you can check the subdivide option to export a mesh with 4 times the amount of faces, generated with Catmull-Clark subdivision.


Ethnics
==========

Ethnics are models which try to closely resemble people from a specific region in the world. They are model files with a special finishing morph for features which cannot be created with the tools in MakeHuman. To load an ethnic, the main ethnic is selected, then one of the sub ethnics of that ethnic. 

The gender and age are also chosen before loading. While the these can, theoretically, be modified afterward, it is advised to choose the gender and age as close as to what you need.
