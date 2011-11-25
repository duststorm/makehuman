.. MakeHuman documentation master file, created by
   sphinx-quickstart on Sun Oct 30 12:49:31 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Preface
=========

This manual, like the MakeHuman software, is under constant construction and will change with the software. The latest edition can always be found on the makehuman website. MakeHuman is a 3d modeling tool which is build for one single purpose:
creating a professional 3d human model. 

While the software is build with usability and simplicity in mind, there will always be questions, that’s what Part I of this manual is for. It is modeled on the application and follows the menu system and options closely. 

Part II focuses on developing with MakeHuman, to create your own plugin and add functionality to the main application. This manual is provided under an Attribution-NonCommercial-NoDerivs 3.0 Unported (CC BY-NC-ND 3.0) license_.

.. _license: http://creativecommons.org/licenses/by-nc-nd/3.0/




Part 2: Developers guide
-------------------------

This document is the 'Developers Guide' for the MakeHuman application and covers key aspects of the development environment configuration and setup on the various supported platforms (Windows, Mac OS X and GNU/Linux). 

It also contains the coding standards required to develop consistently high-quality code for the MakeHuman project and details key features of the Application Programming Interface that MakeHuman developers and Plugin developers can use to maintain and extend the product.

It largely relates to the development of new features but also contains general build instructions that you may find useful if you are attempting to build a copy of the application to run on a platform that is not officially supported.

To extend the software with new features and write a plugins, **it'is comfortable the knowledge of python and the reading of first chapter**. The second chapter contains detailed information about the Python engine written in C, and it's intended for developers that want to touch the core of MH only.



Start from here: writing plugins
---------------------------------

.. toctree::
   :titlesonly:

   dev_manual_plugins   
   dev_manual_morph_target
   dev_manual_undo_redo
   dev_manual_meshes
   dev_manual_camera
   dev_manual_gui_controls
   dev_manual_layout_guidelines
   dev_manual_asynchronous


Application overview
---------------------

.. toctree::
   :titlesonly:

   dev_manual_overview
   dev_manual_integration_layer
   dev_manual_scene_data
   dev_manual_gui_system   
   dev_manual_opengl_notes   
   
Coding style, rules and environment
------------------------------------

.. toctree::
   :titlesonly:
   
   dev_manual_environment
   dev_manual_obtain_source
   

   
Modules
#######

.. toctree::
   :titlesonly:
   
   module_aljabr
   module_animation3d
   module_events3d
   module_font3d
   module_geometry3d
   module_gui3d
   module_module3d
   
Doc Writers Guide
#################

.. toctree::
   :titlesonly:
   
   appendix_1.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

