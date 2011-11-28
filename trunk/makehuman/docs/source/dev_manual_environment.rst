
.. highlight:: python
   :linenothreshold: 5


.. _developers_environment:

##############################
The C Development Environment
##############################

.. warning::

    This chapter need revision and update
    

A development environment enables you to compile and build a new copy of MakeHuman from source code held in the MakeHuman code repository. To simply run the MakeHuman application on Windows, Mac OS-X or Linux, you should not need a development environment as you can usually just use the current released version, which comes with an installer for your operating system. The released software incorporates a Python interpreter, so plugin developers can write, test and use Python scripts without necessarily requiring a separate Python development environment (see the Plugin Development section of this guide).

You do need a development environment to:

* Participate in the development of the MakeHuman
* Build a copy of the application currently under development
* Build a copy of the application to run on a platform that is not officially supported.

To participate in the development of the MakeHuman code as a MakeHuman Team member you will also need to familiarise yourself with the Coding standard and Build Processes contained within this document.  The 'C' compiler is platform dependent. The following are recommended for MakeHuman development:

************************************
Windows 'C' Development Environment
************************************

.. note::

    Add the scons usage in windows
    
The supported environments for MakeHuman 'C' code development are MinGW and Microsoft Visual C++

* To roughly build MakeHuman, you can simply run the compile_src.bat file (maybe you need to adjust it, in order to match your local paths).
* A better result is obtained using Visual C++ (see section Mingw vs. Visual C. below). Actually there is not a VC project file in svn, but it will be added before the release 1.0 final.

Windows Visual C++ 
====================

    Get the following files:
        Python 2.6 (headers + python26.lib + python26.dll)
        SDL 1.2.13 (headers + SDLmain.lib + SDL.lib + SDL.dll)
        SDL_Image 1.2.7 (headers + SDL_Image.dll + optionally jpeg.dll, libpng12-0.dll, libtiff-3.dll, zlib1.dll)
    Create a new Win32 Console project
    Set the necessary include and library folders
    Add all .c and .h files from makehuman/src and makehuman/headers
    Build

Windows gcc
=============

* Python 2.6 (headers + libpython26.a + python26.dll)
* SDL 1.2.13 (headers + libSDLmain.a + libSDL.dll.a + SDL.dll)
* SDL_Image 1.2.7 (headers + SDL_Image.dll + optionally jpeg.dll, libpng12-0.dll, libtiff-3.dll, zlib1.dll) 

The MakeHuman application uses functions from the SDL_image libraries which needs to be linked into the program during the build. You will need to place the set of associated DLL's in a directory accessible during the build.
The DLL files are available for different platforms from http://www.libsdl.org/projects/SDL_image/release/. For example, a zip archive is available for Windows called : http://www.libsdl.org/projects/SDL_image/release/SDL_image-1.2.7-win32.zip. Just copy all of the DLL's from the archive into a directory in your build path before you build the MakeHuman application.

MinGW vs Windows Visual C++ 
============================

An SDL program needs to be linked to a static library called SDLmain, which provides the main/WinMain entry of your program. The original main entry is renamed using a #define when including SDL. The visual C++ version of this SDLMain called SDLmain.lib is compiled using --disable-stdio-redirect while the MinGW version called libSDLmain.a seems to be compiled without this flag. This makes the MinGW version redirect all output to two files, stdout.txt and stderr.txt. Python doesn't like this, and output from python will fail in this case. A workaround is to redirect Python's output itself to file before it does any output:

::

    f=open("outFile.txt", "w")
    sys.stdout = f

    .. .. 

    f.close()

Adding this redirection is implemented in main.c, only when building on windows with gcc:

::

    #if defined(__GNUC__) && defined(__WIN32__)
        err = PyRun_SimpleString("import sys\nf = open(\"outFile.txt\", \"w\")\nsys.stdout = f\nexecfile(\"main.py\")\nf.close()");
    #else
        err = PyRun_SimpleString("execfile(\"main.py\")");
    #endif

The real cause why Python fails is still to be examined.
Another workaround is rebuilding SDL for MinGW using the --disable-stdio-redirect flag.

Linux 'C' Development Environment
==================================

Linux gcc
-------------  
    
You need followin packages:

* Python 2.5 (headers + libpython2.5.a)
* SDL 1.2.13 (headers + libSDLmain.a + libSDL.a + libSDL.so)
* SDL_Image 1.2.7 (headers + libSDL_image-1.2.so.0)

Using Ubuntu or Debian, this mean you need to install, by synaptics, the following packages:

* build-essential
* python2.5-dev
* libsdl1.2-dev
* libsdl-image1.2
* scons

The compiler (of course, GCC) is included in build-essential package.
Compile under Linux is very simple. If you have all packages listed above correctly installed, you must just open the console, go in MH folder and type "scons".

SCons is a Python-based cross-platform build environment that can be used to simplify the build processes for cross-platform applications. Knowledge required to successfully build the application can be built into SCon scripts, which can validate the environment and provide user-friendly information to the person performing the build in the event that the environment is incomplete. 

A draft SConstruct build script is provided in the current MakeHuman SVN build directory, although at the time of writing it is likely still to need adapting for your particular platform. is an useful utility (http://www.scons.org/ ) and in future we will use it for Windows too.


Mac OS-X 'C' Development Environment
=====================================

The Project source files stored under SVN contains a project file for Apples (free) Developing environment named Xcode.

In addition the SVN contains a makefile (Makefile.osx) which is supposed to build MakeHuman among related tools. SVN also includes files needed to adapt the 'C' source code for Mac OS-X builds.

Whether using an Xcode project or the 'make' shell command to build MakeHuman you will need to install the Xcode Tools which include the GCC C Compiler. Xcode is not installed by default, but is part of the "OS-X Developer Tools" package which is available on your OS-X installation DVD. If you don't have the DVD you may download an image of this DVD free of charge from the Apple developer site at http://developer.apple.com.

Currently the build process uses a 'make' shell command which is unusual for OS-X. OS-X build processes usually use the 'Xcode' development system which provides a fully Integrated Development Environment (IDE) that incorporates editors, a build system, dependency generation, debugging support etc. An Xcode project file for the current source deck is under development. 

For further information about the Xcode Tools please refer to http://developer.apple.com/tools/xcode/ . The standard OS-X build process uses an Xcode project to build the source downloaded from SVN. You have two choices to compile the source deck that you download from SVN:

* Either you may use a makefile to perform the build. You can use the file ' compile_src_osx.sh' which is used to launch a 'make' command specifying the 'Makefile_osx' file as the parameter file. ie 'make -f Makefile_osx'. This command compiles and builds the C core.

* You may load the Xcode project file named MakeHuman.xcodeproj into the Xcode Development IDE and perform the build within the Development system.

Both ways assumes that you have already installed the free Xcode package which incorporates a C/C++, and Objective-C++ compiler.

NOTE: Since the latest version of MakeHuman uses Python 2.5 or above, MakeHuman will run only on Mac OS X Version 10.5. or above because prior versions will be shipped with older versions of Python and not work!

If you are using a different Interactive Development Environment (IDE) then you will need to use a text editor to adjust the makefile parameter file before launching the shell script.
In Addition the build system will use some custom Open Source Frameworks which are not maintained by the MakeHuman team. However the SVN contains these Frameworks so you don't have to bother to explicit download them.

************************************
The Python Development Environment
************************************

The vast majority of the functionality delivered by MakeHuman is written in Python which has been used to develop GUI components, service functions and even certain processor intensive functions, such as subdivision. The rationale for developing in Python is that it results in highly human readable code, it is largely free of 'silent crashes', it is easier to find coders to contribute to the development and is far easier to debug than 'C'. The price we have to pay is with the performance of some processor intensive algorithms.

The MakeHuman application incorporates a Python interpreter enabling Python plugins to be developed against a released version of the MakeHuman application without the need for a separate Python Development Environment. This Python interpreter is link-edited into the application whenever the 'C' code is compiled/built, so in order to compile and build the MakeHuman application you will need a Python Development Environment installed on your machine.

Once built, you will be able to run and test any changes made to Python code without having to rebuild the MakeHuman application. You'll simply need to restart the application to pick up your Python changes. However, to incorporate any changes to the 'C' code made by you or by other developers and downloaded by you from the SVN repository you will need to recompile and rebuild the MakeHuman application.

Python is available free from http://www.python.org/) . The Python installer is about 10MB. The installed Python interpreter occupies about 60MB of disk space.

To participate in the development of the MakeHuman code as a MakeHuman Team member you will also need to familiarise yourself with the coding standards and build processes contained within this document
