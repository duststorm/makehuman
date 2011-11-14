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


.. figure::  _static/mh_scheme.png
   :align:   center

   This figure illustrates the two main components of the MakeHuman Application along with the integration layer that connects them. The Python code delivers MakeHuman Specific functionality. The C application provides a Python interpreter and exposes a set of generic MakeHuman functions through the integration layer. The integration layer consists of a set of C functions enabling events to be passed up to Python code and a dynamically generated Python module enabling C functions to be called from the Python code.




C code
=======

The C language is a compiled programming language, requiring developers to install a development environment in order to be able to build changes to the C source code into the application. The C layer is intended to be relatively stable and provides generic functionality to the Python code, minimising the need for C development.
The 3D graphics environment as a whole, including most of the 3D mesh handling functionality is delivered using OpenGL calls embedded within the C application code. User interaction and user events are handled using the SDL (Simple Direct Media Layer) library within the C application code. The SDL library manages low-level events (e.g. Mouse clicks, Mouse Movements, Keystrokes etc.) and makes those events available to the application event loop.

C data structure
-----------------

The principal data structures used by the C code are contained within the 'G.' global structure. This global data structure is defined in the file 'core.h' in the 'include' directory within SVN. Certain state information is held directly in 'G.', such as camera settings, viewport dimensions etc. Information required to define the 3D objects, such as the humanoid figure and the GUI controls is nested within the 'G.world.' data structure, which is a pointer to an array of object3D data structures. Each object3D data structure contains the information needed to define a single object to OpenGL (verts, norms, UV, colors etc.). 

Python code
============

Python is an interpreted language which means that you can add functionality into the Python layer without needing to recompile or rebuild the application.
The MakeHuman application incorporates a complete Python interpreter enabling you to add Python functionality to the a released version of the application without having to install any development software. To add Python functionality to the version of MakeHuman currently under development you do need a development environment to build the application from source code stored in SVN.
MakeHuman functionality is delivered through a combination of core Python modules and plugin Python modules assigned as function attributes on a Python Scene3D object that is instantiated by the main Python module (main.py) at application startup. The application is event driven using the SDL library in the C core to detect registered user events. These events are passed up to the Python functions that have been registered to handle those events on the Scene3D object. The Python event handling functions can interact with the C core through the generic MakeHuman functions exposed through the integration layer to perform the required functionality before returning control to the application event loop to await the next event reported by SDL.


Python Data Structures
-----------------------

The data used to populate the C data structures is maintained through Python code and a copy of that data is held in Python data structures. Python application components load the 3D object data required to populate the corresponding C data structures from object files. That data is loaded into instances of Python classes, that are defined in the file 'module3d.py' (in the 'mh_core' directory in SVN) before being transposed and copied down into the C data structures. These classes can be seen as being organised in a sort of hierarchical structure; A single Scene3D object holds references to the set of Object3D objects used to describe the humanoid model and the various GUI controls. Each Object3D object contains lists of references to the FaceGroup, Face and Vert objects that are used to construct a single 3D object. 


Integration Layer
====================


Specific low-level and high level functionality and events are exposed through a C/Python integration layer enabling high-level GUI operations to be delivered using interpreted Python code. The integration layer passes calls from the C code to the main Python module to handle events detected by the SDL module. These calls are made by functions in core.c which use the PyRun_SimpleString function to invoke Python functions. The integration layer also incorporates a series of C functions exposed through a Python class (named 'mh.') that is dynamically generated by main.c when the application starts. This class is created using the Py_InitModule function which registers a series of C functions as Python methods on the 'mh.' class. This provides a mechanism by which the various Python modules (called in response to an event), can interact with the generic functions and the global data structure in the C core.

Program entry
================

When the application starts, it starts by initializing all global variables. Then it prepares to call the main python entry, first setting the program name, initializing python, passing the program arguments and creating the makehuman python module.

When all that is done, main.py is called. This is done using::

    PyRun_SimpleString("execfile(\"main.py\")");

The reason this method is preferred instead of PyRun_SimpleFile is that the latter might crash on windows because of incompatible structures. Python 2.6 is compiled with Visual Studio 9, which filestructures are different from MinGW or Visual Studio 8.


Python entry
=============

The main python script starts by loading the necessary modules, and creating the scene object. This object contains a list of the objects in the scene, as well as a dictionary mapping selection color to object. After the scene is created, the base mesh as well as the GUI meshes are loaded into the scene. At that point in time, all 3D geometry has been imported into the python runtime, but not yet into OpenGL.

Thus the next logical step is to copy the geometry to the C runtime which creates the necessary OpenGL vertex buffers (and textures?). Finally the event handlers are connected and the GUI is switched to modeling mode. At that point, the Python script calls startWindow which creates the window in the C runtime and starts the event loop.
SDL event loop.

In most modern GUI's, an event loop takes control once everything is initialized. Our loop blocks on SDL_WaitEvent which waits for user input and/or timers. When an event occurs, it is translated and passed to the Python runtime. After handling the event, Python returns control to the event loop.

Redrawing is done by placing an expose event into the event queue. We don't just call draw directly because, if running on a slow system, the event queue would fill up and, after the user has finishes generating input events, a history of those events would be 'played' out. This is solved in two steps. Instead of calling draw directly, an expose event is posted in the event queue. This makes the drawing asynchronous just like the input events. This would still give the same problem, as many events would be posted, which can't be handled in time. To avoid this we mark that an expose event was put into the queue, and we don't place a new one in the queue until it is taken out of the queue and processed. This makes sense as we don't need to tell the system twice or more times to redraw, once an event is pending a redraw will occur eventually.

This way the system stays as responsive as possible, while drawing at the smoothest frame rate possible. 

::

    // The event loop
    while not finished
        wait for event
        check event type
            input: pass to python
            expose: draw and clear pending flag
            custom: call python timer
            quit: finished

    // The redraw method
    if pending flag
        return
    set pending flag
    queue expose event



A similar strategy is used for timers. instead of calling the python callback directly from the SDL timer callback, we push a custom event into the queue and only if there isn't already one in the queue. This is done because the SDL timer callback is called from another thread, which might crash the Python runtime. Once the event loop finishes, the OpenGL textures are freed. And the event loop function returns. This brings control back to the Python runtime which finishes it's main script and returns as well.

Program Exit
=============

Python is finalized and all object memory is freed.

The handler uses the dynamically created mh Python module to call mh_shutDown in main.c which in turn calls mhShutDown in glmodule.c. This issues a system exit(0) to end the application event loop. The exit performs a cleanup and control is passed back through the main function in the main.c file which issues a 'goodbye' message and exits.

Scene data
===========

 A scene is stored as a flat object list, there is no hierarchy and thus no transformations or properties are inherited. This means that if a model wears clothes, the clothes need to undergo the same transform as the model, it is not automatic. Besides the object list, the scene also contains a dictionary of 'false' colors for each object, this enables the system to work out which object the user has clicked on by comparing it with an image generated from the current camera position using these false colors.
 
Object
=======

.. warning::
    Editorial Note: to update

An object is used to represent an object that can appear on the screen. This can be the humanoid object or one of the GUI objects. An object has a name to identify it in the scene. It also holds an index to the corresponding object in the array of C objects. For transformation it holds translation, rotation and scale settings and for the purposes of selection it holds a selection color. The object includes lists of vertices, faces and facegroups to enable it to be rendered. Other object properties which affect the rendering are cameraMode, visibility, texture, hasTexture and shadeless.

Facegroup
==========

Editorial Note: to update
A face group represents a discrete, named group of faces within an object. The facegroup contains a name, a list of faces and the name of the object it belongs to.

Face
=====

.. warning::
    Editorial Note: to update
    
Each face represents an individual triangular face that goes to make up an object. A face has a list of 3 vertices (since it is always a triangle), a normal, its index in the list of faces, the name of the facegroup it belongs to, 3 vertex colors, a selection color and 3 uv coordinates.

Vertex
=======

.. warning::
    Editorial Note: to update
    
    
A vertex represents each vertex of each face of an object. A vertex contains coordinates, a normal, the index of the object this vertex belongs to, a list of indexes of faces and a list of faces which refer to this vertex, a list of corresponding C vertex indices, the index in the verts list of the object this vertex belongs to. 


GUI
====

.. figure::  _static/guy_system.png
   :align:   center



