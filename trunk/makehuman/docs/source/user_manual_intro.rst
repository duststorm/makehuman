.. _intro:



*********************
Introduction
*********************

What's Makehuman?
===================


MakeHuman|copy| is an open source (so it's completely free), innovative and professional software for the modelling of 3-Dimensional humanoid characters. Features that make this software unique include a new, highly intuitive GUI and a high quality mesh, optimized to work in subdivision surface mode. 

Using MakeHuman, a photorealistic character can be modeled in less than 2 minutes; MakeHuman is released under an Open Source Licence (GPL3.0) , and is available for Windows, Mac OS X and Linux.

The first version of MakeHuman was published in 2000, as Blender script, introducing the concept of universal mesh and prompting considerable community feedback. In 2004 MH win the Suzanne Award as better python script, and in 2005 it "move" outside Blender as standalone written in C.

Development effort is currently focused on the 1.0 Release, based on a new GUI and a 4th generation mesh. This release also incorporates considerable changes to the code base which now uses a small, efficient core application written in C, with most of the user functionality being implemented in Python. Because Python is an interpreted scripting language, this means that a wide range of scripts, plugins and utilities can be added without needing to rebuild the application. 

.. |copy| unicode:: U+000A9

An intuitive GUI
=================

The GUI incorporates modelling controls based upon Ethnicity, Gender, Age, Muscle Tone and Body Mass. It incorporates a small number of standardised 'intelligent' tools designed to minimise the learning curve for new users while providing powerful features to enable all users to rapidly model a character that meets their needs. 

Knowledge has been built into the tools so that, for example, if a female figure is being modelled (as defined by the Gender tool), then any body mass added to the model will accumulate fat in those areas of the body where a woman typically accumulates fat.

A professional mesh
====================

All MakeHuman humanoid figures are based on a single, highly optimized, light and professional mesh. Modelling of the mesh is performed by deforming the mesh rather than altering its topology. The mesh has been through a series of iterations to improve the structure so that deformations can be realistically applied while maintaining a low polygon count to minimise processing overheads. 

The mesh supports subdivision to enable higher density, smoothed meshes to be exported for high quality rendering. A considerable number of mesh deformation targets have been created by artists to provide you with a large number of realistic starting points from which to model particular ethnic, gender, age and body mass figures of your own design.

Python Scripting
==================

The MakeHuman application has been structured to expose a great many of the program internals through the Application Programming Interface (API). This open structure has been documented and published to encourage the development of new scripts and plugin functionality that will help the application to develop and rapidly adapt to the needs of the user community.

External rendering
===================

MakeHuman incorporates a range of plugins to export a modelled and posed figure in 3D graphics formats supported by a very wide range of external modellers and rendering engines. These export functions have been written as Python plugins that can easily be extended and can serve as examples to enable other interfaces to be readily constructed. Support for the Renderman format is built into the MakeHuman application. Aqsis is the officially supported Renderman format renderer, but export to other formats and other renderers is also provided. 
