.. _coding_intro:

.. highlight:: python
   :linenothreshold: 5

********************
Coding Introduction
********************

.. _application_overview:

Application overview
=====================


MakeHuman is constructed using two main application components:

* The python interpreter that includes an OpenGL based 3D engine and forms the intentionally small core of the application is written in C.
* The vast majority of the functional components, including the GUI and service functions are written in Python

Retaining this very small, highly optimised and stable C core avoids the need for pyopenGL and therefore avoids the need for Windows users to install the full Python package and to manually install a series of extra packages with associated dependencies and consequent installation issues.
Although the majority of the development effort is focused on Python code (which is an interpreted language so it doesn't require the application to be rebuilt for each code change), the C core does result in developers having to install the C development environment in order that they can perform a complete build.
The application is written in a layered fashion as detailed below.





















