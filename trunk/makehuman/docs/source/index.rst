.. MakeHuman documentation master file, created by
   sphinx-quickstart on Sun Oct 30 12:49:31 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Preface
=========

MakeHuman is a 3D modelling tool which is built for one single purpose: creating a professional 3D human model.  While the software is built with usability and simplicity in mind, there will always be questions, and we hope you will be able to find the answers here.

Part I describes and explains the application, menu system and options. 

Part II focuses on developing with MakeHuman: to create your own plugins and add functionality to the main application. 
*To extend the software with new features and write a plugins, one should have a comfortable knowledge of Python and should read the part II: "Writing Plugins"*.

Part III, "Application details", contains specific information about the Python engine written in C, and it is intended for developers that want to touch the core of MH only. It also contains coding style and key aspects of the development environment configuration and setup on the various supported platforms (Windows, Mac OS X and GNU/Linux).

This manual, like the MakeHuman software, is under constant construction and will change with the software. The latest edition can always be found on the makehuman website.
This manual is provided under an Attribution-ShareAlike CC BY-SA  license_.

.. _license: http://creativecommons.org/licenses/by-sa/3.0/





Part I: User Manual
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
   user_manual_maketarget_260.rst
   
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

Part IX: History
=================
.. toctree::
  :titlesonly:

  history.rst   

Part X: FAQ
============

.. toctree::
  :titlesonly:

  user_manual_faq.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

