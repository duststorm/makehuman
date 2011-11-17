
.. highlight:: python
   :linenothreshold: 5


.. _obtain_source:

Obtain MakeHuman Source
=========================

Anyone can get a copy of the MakeHuman source deck by pointing an SVN client application at the repository.

SubVersion (SVN) Client
------------------------

To be able to participate fully as a MakeHuman developer you will need an SVN client application. This will enable you to take a local copy of the MakeHuman files, regularly update your local copy from the SVN repository and (if you are member of MHteam) commit changes that you have made (and properly tested) back to the SVN repository. SVN update permissions are controlled by the MakeHuman development team, so you'll need an administrator to authorise you with write access.

Different subversion client applications are available for different Operating Systems, many of which are free to use. They each work in slightly different ways, but the differences are relatively minor. See http://subversion.tigris.org/ for a list of Third party SVN client applications.

For example, the Tortoise client for Windows acts as a Windows shell. Once installed it adds SVN client options to the popup menu that is displayed whenever you right click a file or a sub-directory in the Windows file explorer. To obtain a new copy of the MakeHuman SVN development directory structure you select the 'SVN Checkout' option from the explorer menu and enter the URL of the MakeHuman SVN repository.
Other SVN clients provide a comparable mechanism for checking out a copy of the SVN directory structure and will also require the URL:

http://makehuman.googlecode.com/svn/trunk/

Coding Style
=============

Python
-------

Python code must be written following the rules of PEP 8 and PEP 12.

    http://www.python.org/dev/peps/pep-0008/
    http://www.python.org/dev/peps/pep-0012/


Do not write Python *getters* and *setters* unless you can prove that you need something more than simple attribute access. Instead read http://dirtsimple.org/2004/12/python-is-not-java.html and use the 'built-in' property.
Getters and setters waste CPU time, but more important, they waste programmer time for those writing, testing and reading the code.

About the naming style: we use the "mixedCase", as describes in pep 008. So we write "makeHuman" instead, for example, "make_human". Of course, class names must be always capitalised.

C
--

C code must be formatted using Astyle software, from http://astyle.sourceforge.net/ (ANSI style).

Coding Rules
=============

* Indenting (astyle options for C).
* Follow the established MakeHuman naming conventions.
* Add clear and concise comments to your code. Explain what the code does in real-world terms, don't just paraphrase the code.
* Add information that can be read by the current automated API document generation utilities (see the Documentation section of this guide).


The openGL core is entirely contained within the file glmodule.c and ad heres to the following rules:

* "only-what-is-absolutely-needed" is coded in C
* pointers are avoided where at all possible
* complex patterns are avoided
* the C coding is kept stylistically as simple and readable as possible

SVN usage
===========

* Test all changes before submitting to the repository. As an absolute minimum make sure your changes won't break the build for other developers.
* Commit changes as soon as possible so that other developers aren't developing against out of date code.
* Ask for permission before writing into another persons repository. SVN write permission doesn't give you the right to write without bounds!
* Only insert files in SVN that aren't available through another place. 


Bugreports
===========

Where to report bugs?:
Check existing bug reports before submitting your own to avoid duplication. If you have additional information add a comment. Issues and bugs have to be submitted at http://code.google.com/p/makehuman/issues/list.

Bug reports should specify:

* The Operating System or systems affected, or at least the OS upon which the bug was observed.
* MakeHuman version information, including whether it is a pre-built or self-built installation.
* Precise and concise information about which modules, methods, classes etc. are involved if this is known. If you think it's down to a certain module, say so, but also say if you're not sure.
* If the bug is in a build of code that is under development, indicate the date that you downloaded it.
* If you suspect your bug is related to an existing bug report or reports, say so and indicate which ones.

