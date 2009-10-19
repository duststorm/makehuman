/** \file main.c
 *  \brief The main C application file.

 <table>
 <tr><td>Project Name:                                   </td>
     <td><b>MakeHuman</b>                                </td></tr>
 <tr><td>Product Home Page:                              </td>
     <td>http://www.makehuman.org/                       </td></tr>
 <tr><td>SourceForge Home Page:                          </td>
     <td>http://sourceforge.net/projects/makehuman/      </td></tr>
 <tr><td>Authors:                                        </td>
     <td>Manuel Bastioni, Paolo Colombo, Simone Re, Hans-Peter Dusel</td></tr>
 <tr><td>Copyright(c):                                   </td>
     <td>MakeHuman Team 2001-2008                        </td></tr>
 <tr><td>Licensing:                                      </td>
     <td>GPL3 (see also
         http://makehuman.wiki.sourceforge.net/Licensing)</td></tr>
 <tr><td>Coding Standards:                               </td>
     <td>See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
                                                         </td></tr>
 </table>

 This is the main C application file used to run the MakeHuman application.
 A large part of this file is dedicated to providing an integration layer
 between the C core application and the Python GUI control scripts.

 Much of the core C application is used to implement OpenGL library functions
 that are used to control the 3D graphics environment.
 See http://makehuman.wiki.sourceforge.net/DG_Application_Overview for a
 description of how the integration between C and Python works.

 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <SDL.h>

#ifdef _DEBUG
  #undef _DEBUG
  #include <Python.h>
  #define _DEBUG
#else
  #include <Python.h>
#endif

#include "core.h"
#include "glmodule.h"
#ifdef __APPLE__
    #include "OSXTools.h"
#endif // __APPLE__

/* Our global struct - all globals must be here */
Global G;

/** \brief Initialize Globals
 *
 *  This function initializes a small number of global settings that define
 *  the initial view of the Humanoid figure that the MakeHuman application
 *  manipulates (e.g. Field of View, Window Dimensions, Rotation Settings etc.).
 */
static void initGlobals(void)
{
    // Objects
    G.world = PyList_New(0);

    // Camera
    G.fovAngle = 25;
    G.zoom = 60;
    G.rotX = 0;
    G.rotY = 0;
    G.translX = 0;
    G.translY = 0;

    // Screen
    G.windowHeight = 600;
    G.windowWidth = 800;
    G.fullscreen = 0;
    G.clearColor[0] = 0.0;
    G.clearColor[1] = 0.0;
    G.clearColor[2] = 0.0;
    G.clearColor[3] = 0.0;
    G.pendingUpdate = 0;

    // Keyboard
    G.modifiersKeyState = 0;

    // Timer
    G.millisecTimer = 10;
    G.pendingTimer = 0;

    // Rendering
    G.fontOffset = 0;
    
    // Events
    G.loop = 1;
}

/** \brief Get an integer representing the current modifier key settings.
 *
 *  This function returns the current modifier key settings as a Python integer value
 *  (e.g. Whether the Shift or Ctrl keys are currently depressed).
 */
static PyObject* mh_getKeyModifiers(PyObject *self, PyObject *args)
{
    return Py_BuildValue("i", G.modifiersKeyState);
}

static PyObject* mh_updatePickingBuffer(PyObject *self, PyObject *unused)
{
    UpdatePickingBuffer();
    return Py_BuildValue("");
}

/** \brief Get the RGB value of the color that has been picked.
 *
 *  This function returns the color that has been picked as a Python list of 3 integers,
 *  each between 0 and 255, representing an RGB value.
 */
static PyObject* mh_getColorPicked(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[i,i,i]", G.color_picked[0], G.color_picked[1], G.color_picked[2]);
}

/** \brief Get the current camera rotation settings.
 *
 *  This function returns the current camera rotation settings as a Python
 *  list of 2 float values. This is an X and a Y rotation in degrees.
 */
static PyObject* mh_getCameraRotations(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[f,f]", G.rotX,G.rotY);
}

/** \brief Set the current camera rotation settings.
 *
 *  This function sets the current camera rotation settings as 
 *  2 float values. This is an X and a Y rotation in degrees.
 */
static PyObject* mh_setCameraRotations(PyObject *self, PyObject *args)
{
  if (!PyArg_ParseTuple(args, "ff", &G.rotX, &G.rotY))
      return NULL;
  return Py_BuildValue("");
}

/** \brief Get the current camera translation (pan) settings.
 *
 *  This function returns the current camera translation settings as a Python
 *  list of 2 float values. This is an X and a Y translation in ???.
 *  <b>EDITORIAL NOTE. Need to indicate the units used.</b>
 */
static PyObject* mh_getCameraTranslations(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[f,f]", G.translX,G.translY);
}

/** \brief Set the current camera translation (pan) settings.
 *
 *  This function returns the current camera translation settings as
 *  2 float values. This is an X and a Y translation in ???.
 *  <b>EDITORIAL NOTE. Need to indicate the units used.</b>
 */
static PyObject* mh_setCameraTranslations(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, "ff", &G.translX, &G.translY))
        return NULL;
    return Py_BuildValue("");
}

/** \brief Get the current camera zoom setting.
 *
 *  This function returns the current camera zoom setting as a Python
 *  float value.
 *  <b>EDITORIAL NOTE. Need to indicate the units used.</b>
 */
static PyObject* mh_getCameraZoom(PyObject *self, PyObject *args)
{
    return Py_BuildValue("f", G.zoom);
}

/** \brief Set the current camera zoom setting.
 *
 *  This function sets the current camera zoom setting as a Python
 *  float value.
 *  <b>EDITORIAL NOTE. Need to indicate the units used.</b>
 */
static PyObject* mh_setCameraZoom(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, "f", &G.zoom))
        return NULL;
    return Py_BuildValue("");
}

/** \brief Get the current camera settings.
 *
 *  This function returns the current camera settings as a list of 8 Python
 *  float values:
 *  1: Camera Pan X - The camera displacement in the +X direction.
 *  2: Camera Pan Y - The camera displacement in the +Y direction.
 *  3: Camera Zoom (Z) - The camera displacement in the -Z direction.
 *  4: Camera X Rotation - The camera rotation around the X axis in degrees.
 *  5: Camera Y Rotation - The camera rotation around the Y axis in degrees.
 *  6: Camera FOV - The vertical field of view angle in degrees (Y).
 *  7: Window Width - The viewport width in pixels (X).
 *  8: Window Height - The viewport height in pixels (Y).
 *
 *  Note. The camera start position is at the origin pointing straight
 *  ahead along the +Z axis.
 */
static PyObject* mh_getCameraSettings(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[f,f,f,f,f,f,i,i]",
                         G.translX, G.translY, G.zoom,
                         G.rotX, G.rotY,
                         G.fovAngle,
                         G.windowHeight, G.windowWidth);
}

static PyObject* mh_setCameraSettings(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, "f,f,f,f,f,f,i,i", &G.translX, &G.translY, &G.zoom,
        &G.rotX, &G.rotY, &G.fovAngle, &G.windowHeight, &G.windowWidth))
        return NULL;
    return Py_BuildValue("");
}

/** \brief Get the current mouse x, y cursor position on the screen, in pixels.
 *  This function retrieves the x and y mouse position in screen
 *  coordinates returning two integer values to the Python code.
 */
static PyObject* mh_getMousePos2D(PyObject *self, PyObject *args)
{
    int x, y;
    SDL_GetMouseState(&x, &y);
    return Py_BuildValue("[i,i]", x, y);
}

/** \brief Get the current mouse x, y, z cursor position in the 3D scene.
 *  This function retrieves the x, y and z mouse position in screen
 *  coordinates returning three float values to the Python code.
 */
static PyObject* mh_getMousePos3D(PyObject *self, PyObject *args)
{
    int x, y;
    double screen[2];
    double world[3];
    SDL_GetMouseState(&x, &y);
    screen[0] = x;
    screen[1] = y;
    mhConvertToWorld2D(screen, world, 1);
    return Py_BuildValue("[d,d,d]", world[0], world[1], world[2]);
}

/** \brief Get the current mouse x, y, z cursor position in the 3D GUI.
 *  This function retrieves the x, y and z mouse position in GUI
 *  coordinates returning three float values to the Python code.
 */
static PyObject* mh_getMousePosGUI(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[d,d,d]", G.mouseGUIX, G.mouseGUIY, G.mouseGUIZ);
}

static PyObject* mh_convertToScreen(PyObject *self, PyObject *args)
{
    double world[3];
    double screen[3];
    int camera;
    if (!PyArg_ParseTuple(args, "dddi", screen, screen + 1, screen + 2, &camera))
        return NULL;
    else
    {
        mhConvertToScreen(screen, world, camera);
        return Py_BuildValue("[d,d,d]", world[0], world[1], world[2]);
    }
}

static PyObject* mh_convertToWorld2D(PyObject *self, PyObject *args)
{
    double screen[2];
    double world[3];
    int camera;
    if (!PyArg_ParseTuple(args, "ddi", screen, screen + 1, &camera))
        return NULL;
    else
    {
        mhConvertToWorld2D(screen, world, camera);
        return Py_BuildValue("[d,d,d]", world[0], world[1], world[2]);
    }
}

static PyObject* mh_convertToWorld3D(PyObject *self, PyObject *args)
{
    double screen[3];
    double world[3];
    int camera;
    if (!PyArg_ParseTuple(args, "dddi", screen, screen + 1, screen + 2, &camera))
        return NULL;
    else
    {
        mhConvertToWorld3D(screen, world, camera);
        return Py_BuildValue("[d,d,d]", world[0], world[1], world[2]);
    }
}

/** \brief Get the current window (viewport) width and height in pixels.
 *  This function retrieves the current width and height of the drawable area
 *  within the MakeHuman window in pixels (the viewport size).
 */
static PyObject* mh_getWindowSize(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[i,i]", G.windowWidth, G.windowHeight);
}

/** \brief Start the GUI window at application launch.
 *
 *  This function constitutes part of the application initiation processing.
 *  It passes through the instruction to create the SDL window.
 *  It returns a null value.
 */
static PyObject* mh_startWindow(PyObject *self, PyObject *args)
{
    int useTimer = 0;
    if (!PyArg_ParseTuple(args, "i", &useTimer))
        return NULL;
    else
    {
        mhCreateWindow(useTimer);
    }
    return Py_BuildValue("");
}

/** \brief Start the event loop at application launch.
 *
 *  This function constitutes part of the application initiation processing.
 *  It passes through the instruction to launch the main event loop which
 *  will control the GUI environment until the termination of the
 *  application.
 *  It returns a null value.
 */
static PyObject* mh_startEventLoop(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ""))
        return NULL;
    else
    {
        mhEventLoop();
    }
    return Py_BuildValue("");
}

/** \brief End the GUI application.
 *
 *  This function constitutes part of the application termination processing.
 *  It passes through the instruction to exit from the main event loop which
 *  controls the GUI environment.
 *  It returns a null value.
 */
static PyObject* mh_shutDown(PyObject *self, PyObject *args)
{
    mhShutDown();
    return Py_BuildValue("");
}

/** \brief Redraws the scene in the GUI window.
 *
 *  This function passes through the instruction to the SDL module to redraw the
 *  main application GUI window. Drawing asynchronous will queue an update,
 *  drawing synchronous will render immediately.
 *  It returns a null value.
 */
static PyObject* mh_redraw(PyObject *self, PyObject *args)
{
    int async;
    if (!PyArg_ParseTuple(args, "i", &async))
        return NULL;
    if (async)
        mhQueueUpdate();
    else
        mhDraw();
    return Py_BuildValue("");
}

/** \brief Sets the fullscreen state of the GUI window.
 *
 *  This function passes through the instruction to the SDL module to set the
 *  fullscreen state of the main application GUI window.
 *  It returns a null value.
 */
static PyObject* mh_setFullscreen(PyObject *self, PyObject *args)
{
    int fullscreen;
    if (!PyArg_ParseTuple(args, "i", &fullscreen))
        return NULL;
    mhSetFullscreen(fullscreen);
    return Py_BuildValue("");
}

static PyObject *mh_setClearColor(PyObject *self, PyObject *args)
{
  float r, g, b, a;
  if (!PyArg_ParseTuple(args, "ffff",  &r, &g, &b, &a))
      return NULL;
  setClearColor(r, g, b, a);
  return Py_BuildValue("");
}

/** \brief Load texture of an object from file.
 *
 *  This function passes a string containing the file system path to a texture file
 *  into OpenGL.
 *  The texture from this file is applied to the specified object.
 *  It returns a null value.
 */
static PyObject* mh_LoadTexture(PyObject *self, PyObject *args)
{
    int texture;
    char *filename;
    if (!PyArg_ParseTuple(args, "si", &filename, &texture))
        return NULL;
    else if (!(texture = mhLoadTexture(filename, texture, NULL, NULL)))
        return NULL;
    else
        return Py_BuildValue("i", texture);
}

static PyObject* mh_CreateVertexShader(PyObject *self, PyObject *args)
{
    int shader;
    char *vertexShaderSource;
    if (!PyArg_ParseTuple(args, "s", &vertexShaderSource))
        return NULL;
    else if (!(shader = mhCreateVertexShader(vertexShaderSource)))
        return NULL;
    else
        return Py_BuildValue("i", shader);
}

static PyObject* mh_CreateFragmentShader(PyObject *self, PyObject *args)
{
    int shader;
    char *source;
    if (!PyArg_ParseTuple(args, "s", &source))
        return NULL;
    else if (!(shader = mhCreateFragmentShader(source)))
        return NULL;
    else
        return Py_BuildValue("i", shader);
}

static PyObject* mh_CreateShader(PyObject *self, PyObject *args)
{
    int shader;
    int vertexShader, fragmentShader;
    if (!PyArg_ParseTuple(args, "ii", &vertexShader, &fragmentShader))
        return NULL;
    else if (!(shader = mhCreateShader(vertexShader, fragmentShader)))
        return NULL;
    else
        return Py_BuildValue("i", shader);
}

static PyObject* mh_GrabScreen(PyObject *self, PyObject *args)
{
    int x, y, width, height;
    char *filename;
    if (!PyArg_ParseTuple(args, "iiiis", &x, &y, &width, &height, &filename))
        return NULL;
    else if (!mhGrabScreen(x, y, width, height, filename))
      return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set millisec attribute for timer func.
 *
 *  This function passes the delay function to the SDL timer
 *  It returns a null value.
 */
static PyObject* mh_setTimeTimer(PyObject *self, PyObject *args)
{
    int milliseconds;
    if (!PyArg_ParseTuple(args, "i", &milliseconds))
        return NULL;
    else
    {
        G.millisecTimer = milliseconds;
    }
    return Py_BuildValue("");
}

/** \brief Gets program specific path locations. 
 *  MakeHuman uses pathes to export objects and to (re)store exports and screen grabs. 
 *  Since the various locations depend from the system (Linux, Windows, Mac OS) the program is running 
 *  on theses pathes may be queried by this function.
 *
 *  \param type Determines which path actually has to be queried. Type has to be either 
 *   'exports', 'models' or 'grab'. NULL will be returnded if it does not fit these requirements. 
 *
 *   The symantics is as follow:
 *
 * <table cellspacing="0" cellpadding="5" border="1">
 *     <tr bgcolor="#CCCCCC">
 *       <th>type</th>
 *       <th>synopsis</th>
 *       <th>Windows</th>
 *       <th>Linux</th>
 *       <th>Mac OS X</th>
 *     </tr>
 *     <tr>
 *       <th bgcolor="#CCCCCC"><tt>&quot;exports&quot;</tt></th>
 *       <td>Declares the path to where exported to.</td>
 *       <td><tt>&quot;./exports/&quot;</tt></td>
 *       <td><tt>&quot;./exports/&quot;</tt></td>
 *       <td>From preferences<br><i>(defaults to <tt>&quot;${USER}/Documents/MakeHuman/exports/&quot;</tt>)</i></td>
 *     </tr>
 *     <tr>
 *       <th bgcolor="#CCCCCC"><tt>&quot;models&quot;</tt></th>
 *       <td>Declares the path where the models are stored to.</td>
 *       <td><tt>&quot;./models/&quot;</tt></td>
 *       <td><tt>&quot;./models/&quot;</tt></td>
 *       <td>From preferences<br><i>(defaults to <tt>&quot;${USER}/Documents/MakeHuman/models/&quot;</tt>)</i></td>
 *     </tr>
 *     <tr>
 *       <th bgcolor="#CCCCCC"><tt>&quot;grab&quot;</tt></th>
 *       <td>Declares the target for screenshots.</td>
 *       <td><tt>&quot;./&quot;</tt></td>
 *       <td><tt>&quot;./&quot;</tt></td>
 *       <td>From preferences<br><i>(defaults to <tt>&quot;${USER}/Desktop/&quot;</tt>)</i></td>
 *     </tr>
 * </table>
 *
 *  \return The Path according the property 'type'.
 *
 */
static PyObject* mh_getPath(PyObject *self, PyObject *type)
{
    const char *path = NULL;
    const char *typeStr;
    
    if (!PyString_Check(type))
    {
        PyErr_SetString(PyExc_TypeError, "String expected");
        return NULL;
    }
    
    typeStr = PyString_AsString(type);

#ifdef __APPLE__
    if (0 == strcmp(typeStr, "exports"))
    {
        path = getExportPath();
    }
    else if (0 == strcmp(typeStr, "models"))
    {
        path = getModelPath();
    }
    else if (0 == strcmp(typeStr, "grab"))
    {
        path = getGrabPath();
    }
#else  /* default as "exports/" at the current dir for Linux and Windows */
    if (0 == strcmp(typeStr, "exports"))
    {
        path = "exports/";
    }
    else if (0 == strcmp(typeStr, "models"))
    {
        path = "models/";
    }
    else if (0 == strcmp(typeStr, "grab"))
    {
        path = "./";
    }
#endif
    if (NULL == path)
    {
        PyErr_Format(PyExc_ValueError, "Unknown property %s for getPath()!", typeStr);
        return NULL;
    }
    return Py_BuildValue("s", path); 
}

/** \brief Defines a set of functions as an array that can be passed into the Py_InitModule function.
 *
 *  This array declaration is used to list a set of functions that can be called from Python.
 *  The array is passed into the Py_InitModule function when it is used to dynamically
 *  initialize the 'mh' moduleas.
 */
static PyMethodDef EmbMethods[] =
{
    {"setTimeTimer", mh_setTimeTimer, METH_VARARGS, ""},
    {"getMousePosGUI", mh_getMousePosGUI, METH_VARARGS, ""},
    {"getMousePos3D", mh_getMousePos3D, METH_VARARGS, ""},
    {"getWindowSize", mh_getWindowSize, METH_VARARGS, ""},
    {"getMousePos2D", mh_getMousePos2D, METH_VARARGS, ""},
    {"convertToScreen", mh_convertToScreen, METH_VARARGS, ""},
    {"convertToWorld2D", mh_convertToWorld2D, METH_VARARGS, ""},
    {"convertToWorld3D", mh_convertToWorld3D, METH_VARARGS, ""},
    {"getKeyModifiers", mh_getKeyModifiers, METH_VARARGS, ""},
    {"getCameraRotations", mh_getCameraRotations, METH_VARARGS, ""},
    {"setCameraRotations", mh_setCameraRotations, METH_VARARGS, ""},
    {"getCameraTranslations", mh_getCameraTranslations, METH_VARARGS, ""},
    {"setCameraTranslations", mh_setCameraTranslations, METH_VARARGS, ""},
    {"getCameraZoom", mh_getCameraZoom, METH_VARARGS, ""},
    {"setCameraZoom", mh_setCameraZoom, METH_VARARGS, ""},
    {"getCameraSettings", mh_getCameraSettings, METH_VARARGS, ""},
    {"setCameraSettings", mh_setCameraSettings, METH_VARARGS, ""},
    {"updatePickingBuffer", mh_updatePickingBuffer, METH_NOARGS, ""},
    {"getColorPicked", mh_getColorPicked, METH_VARARGS, ""},
    {"redraw", mh_redraw, METH_VARARGS, ""},
    {"setFullscreen", mh_setFullscreen, METH_VARARGS, ""},
    {"setClearColor", mh_setClearColor, METH_VARARGS, ""},
    {"loadTexture", mh_LoadTexture, METH_VARARGS, ""},
    {"createVertexShader", mh_CreateVertexShader, METH_VARARGS, ""},
    {"createFragmentShader", mh_CreateFragmentShader, METH_VARARGS, ""},
    {"createShader", mh_CreateShader, METH_VARARGS, ""},
    {"grabScreen", mh_GrabScreen, METH_VARARGS, ""},
    {"startWindow", mh_startWindow, METH_VARARGS, ""},
    {"startEventLoop", mh_startEventLoop, METH_VARARGS, ""},
    {"shutDown", mh_shutDown, METH_VARARGS, ""},
    {"getPath", mh_getPath, METH_O, ""},
    {NULL, NULL, 0, NULL}
};

/** \brief The main function initializes the MakeHuman application.
 *
 *  This function sets up the integration layer between Python and the
 *  C core application then runs the 'main' Python module to start
 *  up the MakeHuman application.
 *
 *  When the user quits the application, the SDL loop
 *  controlling user interaction with the MakeHuman GUI is terminated
 *  by the mhShutDown function from glmodule.c which issues a system exit.
 *  This function traps the exit condition and displays a goodbye message
 *  into the message window before releasing the memory used by the
 *  global variables and ending.
 *
 *  This function returns a '1'.
 */
#ifdef MAKEHUMAN_AS_MODULE
PyMODINIT_FUNC initmh()
{
    PyObject* m;

    initGlobals(); /* initialize all our globals */

    m = Py_InitModule3("mh", EmbMethods,
                       "makehuman as a module.");
}
#else /* #if !defined(MAKEHUMAN_AS_MODULE) */
int main(int argc, char *argv[])
{
    // Need to declare variables before other statements
    char str[128];
    int err;
    PyObject *module;

    if (argc >= 2)
    {
        snprintf(str, sizeof(str), "execfile(\"%s\")", argv[1]);
    }
    else
    {
        strcpy(str, "execfile(\"main.py\")");
    }
#ifdef __APPLE__ /* Since Mac OS uses app bundles all data reside in this resource bundle too. */
    int rc = adjustWorkingDir(argv[0]);
    assert(0 == rc);

    /* Adjust the environment vars for the external renderer */
    rc = adjustRenderEnvironment();
    assert(0 == rc);
#endif

    Py_SetProgramName(argv[0]);
    Py_Initialize();

    if (!Py_IsInitialized())
    {
        printf("Could not initialize Python\n");
        exit(1);
    }

    PySys_SetArgv(argc, argv);

    initGlobals(); /* initialize all our globals */
    module = Py_InitModule("mh", EmbMethods);
    RegisterObject3D(module);
    RegisterTexture(module);
    PyModule_AddObject(module, "world", G.world);

#if defined(__GNUC__) && defined(__WIN32__)
    PyRun_SimpleString("import sys\nfo = open(\"python_out.txt\", \"w\")\nsys.stdout = fo");
    PyRun_SimpleString("import sys\nfe = open(\"python_err.txt\", \"w\")\nsys.stderr = fe");
    err = PyRun_SimpleString("execfile(\"main.py\")");
    PyRun_SimpleString("fo.close()");
    PyRun_SimpleString("fe.close()");
#else
    err = PyRun_SimpleString("execfile(\"main.py\")");
#endif /* defined(__GNUC__) && defined(__WIN32__) */

    if (err != 0)
    {
        printf("Could not run main Python script\n");
        getc(stdin);
        exit(1);
    }

    Py_Finalize();

    return 1;
}
#endif /* #ifdef MAKEHUMAN_AS_MODULE */

// The following comment block is used by Doxygen to populate the main page

/** \mainpage MakeHuman - 'C' Documentation

\section intro Introduction
MakeHuman&copy; is a free interactive modelling tool for creating custom 3D human characters. These characters can be modelled very quickly and can then be exported and used with many other modelling and rendering programs to incorporate realistic human figures into computer generated images and animations. Features that make this software unique include the tetra-parametric GUI&copy; and the Natural Pose System&copy;, for advanced muscular simulation.

The home page for MakeHuman&copy; is at http://www.makehuman.org/ . The MakeHuman project is an open source project hosted on sourceforge at http://sourceforge.net/projects/makehuman/ and documented on a Wiki at http://makehuman.wiki.sourceforge.net/.

The program uses a small (but crucial) C core to support MakeHuman application functionality written in Python. These pages document the C source code that forms the core of the MakeHuman application. The Python API is documented at http://makehuman.sourceforge.net/API/ .

The C code uses OpenGL to manage the 3D graphics environment and SDL to control user interaction with the main GUI window. The C code passes events up to the Python code and provides functions to the Python code to enable it to interact with the 3D environment. The C source is contained in 4 key files and their header files (see the 'Files' tab for the full list):

<center>
<table>
<tr>
  <td class="indexkey">src/<a class="el" href="main_8c.html">main.c</a> <a href="main_8c-source.html">[code]</a></td>
  <td class="indexvalue">The main C application file </td>
</tr><tr>
  <td class="indexkey">src/<a class="el" href="glmodule_8c.html">glmodule.c</a> <a href="glmodule_8c-source.html">[code]</a></td>
  <td class="indexvalue">This module integrates with OpenGL functionality </td>
</tr><tr>
  <td class="indexkey">src/<a class="el" href="core_8c.html">core.c</a> <a href="core_8c-source.html">[code]</a></td>
  <td class="indexvalue">Integration layer between the C core and Python functions </td>
</tr>
</table>
</center>

\section startup Application Startup
When MakeHuman is launched, the C code from the 'main' function in main.c is run which dynamically creates the Python module 'mh'.
This module contains a series of embedded integration functions that map through to the other C functions in main.c, connecting the C application with the Python front-end by providing Python functions that call C functions.

For example, the "getCameraRotations" function is created as an embedded Python function on the 'mh' module that calls the C function "mh_getCameraRotations" (defined in the file main.c). This returns camera rotation angles as Python values based upon settings stored in C global variables.

Having created the 'mh' module in memory the 'main' C function loads the 'main.py' module. This displays a splash screen and a progress bar as it loads the initial 3D humanoid model (the neutral base object) and adds the various GUI sections into the scene. It creates the main toolbar that enables the user to switch between different GUI modes and defines functions to 
perform that switch for all active buttons. Active buttons are connected to these functions by being registered to receive events.
 
At the end of the initiation process the splash screen is hidden and Modelling mode is activated. The 'startEventLoop' method on the main Scene3D object is invoked to call the OpenGL/SDL C functions that manage the low-level event loop. 

This Python module responds to high-level GUI toolbar events to switch between different GUI modes, but otherwise events are handled by GUI mode specific Python modules.

\section events GUI Events
SDL manages all low-level events and mhEventLoop calls C functions to handle these events. The C functions mostly pass through the events to the corresponding Python functions that have been registered against the Scene3D object. This is handled by core.c which contains a series of C functions that call Python functions using the PyRun_SimpleString function. Some Python functions need to make calls back to the OpenGL C code to perform processing such as redraws before returning control to the C code.

Whether implemented within the C handler or bubbled up to Python, the handler performs an action and ends, returning control to mhEventLoop.


\section close Application Close
Keyboard and mouse events that are configured to end the application bubble up to the Python handlers in main.py which call mh_shutDown in main.c which in turn calls mhShutDown in glmodule.c. This issues a system exit(0) to end the SDL application loop. The exit is intercepted to enable cleanup to be performed and control to be passed back through the main function in the main.c file which issues a 'goodbye' message and exits.


*/


