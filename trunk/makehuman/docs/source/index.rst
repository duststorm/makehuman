.. MakeHuman documentation master file, created by
   sphinx-quickstart on Sun Oct 30 12:49:31 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MakeHuman documentation
=============================================

This document is the 'Developers Guide' for the MakeHuman application and covers key aspects of the development environment configuration and setup on the various supported platforms (Windows, Mac OS X and GNU/Linux). It also contains the coding standards required to develop consistently high-quality code for the MakeHuman project and details key features of the Application Programming Interface that MakeHuman developers and Plugin developers can use to maintain and extend the product.
It largely relates to the development of new features but also contains general build instructions that you may find useful if you are attempting to build a copy of the application to run on a platform that is not officially supported.

The MakeHuman project is an open source project developed, managed and maintained by voluntary efforts. It is hosted on http://code.google.com/p/makehuman/ where the current source code is available for download from the SVN repository. An earlier CVS repository has been retained for reference purposes, but is no longer maintained.


Developers guide
################

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
   
Writing plugins
----------------

.. toctree::
   :titlesonly:

   dev_manual_plugins
   dev_manual_gui
   dev_manual_morph_target
   dev_manual_undo_redo
   dev_manual_meshes
   dev_manual_camera
   dev_manual_gui_controls
   dev_manual_layout_guidelines
   dev_manual_asynchronous
   
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

