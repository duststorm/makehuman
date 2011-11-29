.. MakeHuman documentation master file, created by
   sphinx-quickstart on Sun Oct 30 12:49:31 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Preface
=========

This manual, like the MakeHuman software, is under constant construction and will change with the software. The latest edition can always be found on the makehuman website. MakeHuman is a 3d modeling tool which is build for one single purpose: creating a professional 3d human model. 

While the software is build with usability and simplicity in mind, there will always be questions, that’s what Part I of this manual is for. It is modeled on the application and follows the menu system and options closely. 

Part II focuses on developing with MakeHuman, to create your own plugin and add functionality to the main application. 


This manual is provided under an Attribution-NonCommercial-NoDerivs 3.0 Unported (CC BY-NC-ND 3.0) license_.

.. _license: http://creativecommons.org/licenses/by-nc-nd/3.0/

To extend the software with new features and write a plugins, *it'is comfortable the knowledge of python and the reading of chapter "Start from here: writing plugins"*. 

The part III, "Application details", contains specific information about the Python engine written in C, and it's intended for developers that want to touch the core of MH only. 

The part III, also, contain coding style and key aspects of the development environment configuration and setup on the various supported platforms (Windows, Mac OS X and GNU/Linux). 


Part I: General usage
========================

.. toctree::
   :titlesonly:
   
   user_manual_intro.rst 
   user_manual_installation.rst 
   user_manual_view.rst  
   user_manual_modelling.rst 
   user_manual_files.rst
   user_manual_posing.rst
   user_manual_library.rst
   user_manual_rendering.rst  
   user_manual_setting.rst


Part II: Writing plugins
=============================

.. toctree::
   :titlesonly:

   dev_manual_plugins   
   dev_manual_morph_target
   dev_manual_undo_redo 
   dev_manual_camera
   dev_manual_gui_controls
   dev_manual_asynchronous


Part III: Application details
===============================

.. toctree::
   :titlesonly:

   dev_manual_overview
   dev_manual_integration_layer
   dev_manual_scene_data
   dev_manual_gui_system   
   dev_manual_opengl_notes    
   dev_manual_environment
   dev_manual_obtain_source 
   
Part IV: The Base mesh
=========================

.. toctree::
   :titlesonly:

   dev_manual_basemesh
  

Part V: MakeHuman and Blender
=============================

.. toctree::
   :titlesonly:
   
   user_manual_export_mhx.rst
   user_manual_import_mhx_249.rst
   user_manual_import_mhx_250.rst
   user_manual_cage_and_mesh-deform.rst
   
Part VI: Doc Writers Guide
=============================

.. toctree::
   :titlesonly:
   
   appendix_1.rst
   appendix_2.rst
   
   
Part VII: Modules
==================

.. toctree::
   :titlesonly:
   
   module_aljabr
   module_animation3d
   module_events3d
   module_font3d
   module_geometry3d
   module_gui3d
   module_module3d
   
Part VIII: Licensing
======================
  
.. toctree::
   :titlesonly:

   dev_manual_licensing1
   dev_manual_licensing2
   
Part IX: FAQ

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

