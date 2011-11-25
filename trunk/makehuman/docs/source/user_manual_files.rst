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
