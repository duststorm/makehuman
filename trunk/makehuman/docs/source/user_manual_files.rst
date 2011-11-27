.. _files:

.. highlight:: python
   :linenothreshold: 5

*********
Files
*********

.. figure::  _static/files.png
   :align:   center   

Save and Load
==============

Saving and loading happens in a custom and optimized format for MakeHuman with the *mhm* extension. It is advised to always save in this format also when you export models, since you can’t load any other format back into MakeHuman. 

This is important when you want to make changes at a later stage of production.

Export
-------

Wavefront (obj)
^^^^^^^^^^^^^^^

Wavefront obj is a good format when you need a simple mesh for an external renderer. It comes with an mtl ﬁle deﬁning the material.


Eyebrows
^^^^^^^^^
For some uses, like raytracing, the eyebrow geometry causes problems. If this is the case, uncheck it to avoid it from being exported.

Diamonds
^^^^^^^^^

The diamond geometry is used to keep track of the skeleton. However in most cases this is not needed. In case the diamond geometry is desired, check it to export it.

Skeleton
^^^^^^^^^

This option exports the skeleton in Biovision hierarchical data (bvh) format which is generally used for motion capture. Note however that the model is not rigged to this skeleton.

Groups
^^^^^^^

Whether groups are useful depends on the software used. Many importers also give the option to import the groups or not. Groups can be used to select speciﬁc body parts for modiﬁcation or deletion. If groups are not desired, uncheck it.

Subdivide
^^^^^^^^^^^

If a high poly mesh is needed, and the modeler or renderer used does not have a good subdivision algorithm, you can check the subdivide option to export a mesh with 4 times the amount of faces, generated with Catmull-Clark subdivision.

Hair
^^^^^

If hair is present, it can be exported as a polygon mesh or as curves. Again it depends on the software which is going to import the ﬁle whether mesh or curves is the best option.

Blender exchange (mhx)
------------------------

The Blender exchange format is a custom format designed to bring a rigged model into Blender. It comes with a skeleton, forward and inverse kinematics with limits, render materials, lip-sync and more.

Version
^^^^^^^^

Currently it is still possible to export for Blender 2.4, however this may change once Blender 2.5 is stable.

Expressions
^^^^^^^^^^^^

If checked, all expressions available within MakeHuman are exported to the mhx, this makes the export considerably bigger in size.

Rig
^^^^

Two rigs are available, mhx rig or game rig. For posing and animating the mhx rig is preferred.

Collada (dae)
-------------

To do.

Quake (md5)
------------

The md5 exporter is not yet fully functional, the skin is not correctly attached to the skeleton.

Stereolithography (stl)
------------------------

Stereolithography is a format used for 3d printing.

Format
^^^^^^^

The binary format is a lot more compact than the ASCII format. However the latter is provided for compatibility reasons.

Subdivide
^^^^^^^^^^

If a high poly mesh is needed, and the exernal modeler or renderer does not have a good subdivision algorithm, you can check the subdivide option to export a mesh with 4 times the amount of faces, generated with Catmull-Clark subdivision.


Ethnics
==========

Ethnics are models which try to closely resemble people from a speciﬁc region in the world. They are model ﬁles with a special ﬁnishing morph for features which cannot be created with the tools in MakeHuman. To load an ethnic, the main ethnic is selected, then one of the sub ethnics of that ethnic. 

The gender and age are also chosen before loading. While the these can, theoretically, be modiﬁed afterward, it is advised to choose the gender and age as close as to what you need.
